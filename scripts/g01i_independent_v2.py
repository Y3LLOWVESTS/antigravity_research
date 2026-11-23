"""G01-I v2: scoped independent audit with bounded float comparisons.

Never rewrites the original G01-I evidence. Floats may differ only
within stated tolerances. Structural data, source hashes, categorical
claims, integer counts and parent provenance must match exactly.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import re
import secrets
import sys
import tarfile

import numpy as np
from numpy.polynomial.legendre import leggauss, legval

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import g01i_r3b_source_v1 as producer
import g01i_independent_v1 as previous

RUNS = ROOT / "results/gravity2/g01i_runs"
AUDITS = ROOT / "results/gravity2/g01i_v2_audits"

RUN_RE = re.compile(
    r"g01i_\d{8}T\d{6}Z_[a-f0-9]{8}\Z"
)

SOURCE_LOCKS = {
    "g01i_r3b_source_v1.py":
        "40bda623ebd3781725e25200e67d4662362e761affca4fea103238574d46b252",
    "g01i_independent_v1.py":
        "ae454466db8074dcc58cff4a2c8c689396b163247ab00d2ad865658d82529fff",
}


def hash_file(path):
    return sha256(path.read_bytes()).hexdigest()


def encode(obj):
    return (
        json.dumps(
            obj, sort_keys=True, indent=2, allow_nan=False
        ) + "\n"
    ).encode()


def immutable(path, content):
    if path.exists() or path.is_symlink():
        raise ValueError("IMMUTABLE_OUTPUT_EXISTS")

    with path.open("xb") as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())


def compare(a, b, path, differences):
    if type(a) is not type(b):
        raise ValueError(
            "TYPE_DRIFT:" + path
            + ":" + type(a).__name__
            + "/" + type(b).__name__
        )

    if isinstance(a, dict):
        if a.keys() != b.keys():
            raise ValueError(
                "SCHEMA_KEYS_DRIFT:" + path
                + ":" + repr(set(a) ^ set(b))
            )

        for key in sorted(a):
            compare(
                a[key], b[key],
                path + "." + key, differences
            )

    elif isinstance(a, list):
        if len(a) != len(b):
            raise ValueError("ARRAY_LENGTH_DRIFT:" + path)

        for index, (x, y) in enumerate(zip(a, b)):
            compare(
                x, y, f"{path}[{index}]", differences
            )

    elif isinstance(a, float):
        if not math.isfinite(a) or not math.isfinite(b):
            raise ValueError("NONFINITE_FLOAT:" + path)

        delta = abs(a - b)
        limit = max(
            2e-12,
            2e-12 * max(abs(a), abs(b))
        )

        if path.endswith(".net_charge_proxy"):
            # A cancellation residual compared with a much larger
            # absolute-charge proxy. Neutrality is checked separately.
            limit = max(limit, 1e-8)

        if delta > limit:
            raise ValueError(
                "NUMERIC_DRIFT:" + path
                + ":recomputed=" + repr(a)
                + ":saved=" + repr(b)
                + ":difference=" + repr(delta)
                + ":limit=" + repr(limit)
            )

        if a != b:
            differences.append({
                "path": path,
                "recomputed": a,
                "saved": b,
                "abs_delta": delta,
                "allowed": limit,
            })

    elif a != b:
        raise ValueError(
            "NONNUMERIC_DRIFT:" + path
            + ":" + repr(a)
            + "/" + repr(b)
        )


def charge_reversal_control(modes, norm, conv, target):
    mu, weights = leggauss(384)

    charge = np.zeros_like(mu)
    potential = np.zeros_like(mu)
    R = producer.R

    for mode in modes:
        ell = mode["ell"]
        amplitude = mode["amplitude"]

        coefficients = np.zeros(ell + 1)
        coefficients[-1] = 1.0

        polynomial = legval(mu, coefficients)

        potential -= (
            amplitude * polynomial / np.sqrt(2)
        )

        charge -= (
            (2 * ell + 1) * amplitude * polynomial
            / (np.sqrt(2) * R)
        )

    area = 2 * np.pi * R**2 * weights

    original = float(
        0.5 * np.dot(
            area, charge * potential
        ) * conv * norm
    )

    reversed_both = float(
        0.5 * np.dot(
            area, (-charge) * (-potential)
        ) * conv * norm
    )

    if not math.isclose(
        original, target,
        rel_tol=1e-10,
        abs_tol=1e-11,
    ):
        raise ValueError(
            "CHARGE_REVERSAL_ENERGY_RECONSTRUCTION_HOLD"
        )

    if not math.isclose(
        original, reversed_both,
        rel_tol=1e-14,
        abs_tol=1e-14,
    ):
        raise ValueError(
            "SELF_CONSISTENT_CHARGE_REVERSAL_FAIL"
        )

    return {
        "original_energy_J": original,
        "reversed_charge_and_potential_energy_J":
            reversed_both,
        "physical_reversal_energy_sign": "UNCHANGED",
        "historical_charge_only_control":
            "INVALID_AS_PHYSICAL_NEGATIVE_CONTROL",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()

    if not RUN_RE.fullmatch(args.run_id):
        raise ValueError("INVALID_RUN_ID")

    folder = RUNS / args.run_id

    if not folder.is_dir() or folder.is_symlink():
        raise ValueError("ORIGINAL_RUN_MISSING")

    names = (
        "manifest.json",
        "science.json",
        "mode_scan.json",
    )

    for name in names:
        path = folder / name

        if path.is_symlink() or not path.is_file():
            raise ValueError(
                "ORIGINAL_EVIDENCE_MISSING:" + name
            )

    for name, expected in SOURCE_LOCKS.items():
        path = SCRIPTS / name

        if (
            not path.is_file()
            or path.is_symlink()
            or hash_file(path) != expected
        ):
            raise ValueError(
                "V1_SOURCE_SHA_HOLD:" + name
            )

    manifest = json.loads(
        (folder / "manifest.json").read_text()
    )

    science = json.loads(
        (folder / "science.json").read_text()
    )

    rows = json.loads(
        (folder / "mode_scan.json").read_text()
    )

    parents, modes, norm, conv = producer.parent()

    if (
        manifest["parent_sha256"] != parents
        or manifest["source_sha256"] != SOURCE_LOCKS
        or manifest["run_id"] != args.run_id
    ):
        raise ValueError(
            "ORIGINAL_MANIFEST_PROVENANCE_DRIFT"
        )

    recomputed, scan = producer.evaluate(
        modes, norm, conv
    )

    differences = []

    compare(
        recomputed, science,
        "science", differences
    )

    compare(
        scan, rows,
        "rows", differences
    )

    independent_stored = previous.review(
        science, rows, modes, norm, conv
    )

    independent_recomputed = previous.review(
        recomputed, scan, modes, norm, conv
    )

    if (
        independent_stored["status"]
        != independent_recomputed["status"]
    ):
        raise ValueError(
            "INDEPENDENT_REVIEW_DISAGREEMENT"
        )

    if (
        len(rows) != 96
        or science["scanned_cases"] != 96
        or science["protected_prescribed_R3B_capacity_J"]
        != producer.REF
    ):
        raise ValueError("R3B_CASE_OR_PARENT_DRIFT")

    for row in rows:
        if (
            row["net_over_absolute_charge"] >= 1e-9
            or row["energy_relative_error"] >= 5e-8
            or row["stress_traction_scaled_error"] >= 1e-11
        ):
            raise ValueError(
                "INDEPENDENT_SHELL_IDENTITY_HOLD"
            )

    reversal = charge_reversal_control(
        modes,
        norm,
        conv,
        science["electric_mirror_shell_energy_J"],
    )

    result = {
        "schema": "gravity2.g01i.independent.v2",
        "status":
            "PASS_SCOPED_FLOAT_TOLERANT_SHELL_AUDIT_NOT_GRAVITY",
        "original_run_id": args.run_id,
        "original_v1_verification":
            "HOLD_SCIENCE_RECOMPUTATION_DRIFT_PRESERVED",
        "source_v1_sha256": SOURCE_LOCKS,
        "auditor_v2_sha256":
            hash_file(Path(__file__)),
        "original_evidence_sha256": {
            name: hash_file(folder / name)
            for name in names
        },
        "parent_sha256": parents,
        "float_comparison": {
            "rel_tol": 2e-12,
            "abs_tol": 2e-12,
            "net_charge_proxy_abs_tol": 1e-8,
            "accepted_numeric_differences":
                len(differences),
            "maximum_absolute_difference": max(
                (entry["abs_delta"] for entry in differences),
                default=0.0,
            ),
            "first_differences": differences[:20],
            "all_nonfloat_values_exact": True,
        },
        "independently_reviewed_cases":
            independent_stored[
                "independently_checked_cases"
            ],
        "correction_charge_reversal": reversal,
        "accepted_negative_controls":
            "ORIGINAL_FOUR_OTHER_LOGICAL_CONTROLS_SCOPED_ONLY",
        "physical_source": "NOT_DERIVED",
        "loaded_response":
            "HISTORICAL_INWARD_FAILURE",
        "Einstein_gravity": "NOT_DERIVED",
        "whole_craft_lift": "NOT_DERIVED",
        "complete_operating_energy":
            "NOT_CERTIFIED",
        "006D_replaced": False,
        "physical_survivors": 0,
        "next_gate":
            "G01_COMPLETE_SOURCED_COVARIANT_ACTION",
    }

    if AUDITS.is_symlink():
        raise ValueError("AUDIT_BASE_SYMLINK")

    AUDITS.mkdir(parents=True, exist_ok=True)

    audit_id = (
        datetime.now(timezone.utc).strftime(
            "g01iaudit2_%Y%m%dT%H%M%SZ_"
        ) + secrets.token_hex(4)
    )

    dest = AUDITS / audit_id
    dest.mkdir(mode=0o700)

    for name in names:
        original_bytes = (folder / name).read_bytes()

        immutable(
            dest / name,
            original_bytes
        )

        if hash_file(dest / name) != hash_file(folder / name):
            raise ValueError("EVIDENCE_COPY_DRIFT")

    immutable(
        dest / "audit_v2.json",
        encode(result)
    )

    archived_names = (
        *names,
        "audit_v2.json",
    )

    ledger = "".join(
        hash_file(dest / name)
        + "  " + name + "\n"
        for name in archived_names
    )

    immutable(
        dest / "SHA256SUMS.txt",
        ledger.encode()
    )

    archive = dest / (
        audit_id + "_UPLOAD.tar.gz"
    )

    with tarfile.open(
        archive, mode="x:gz"
    ) as bundle:
        for name in (
            *archived_names,
            "SHA256SUMS.txt",
        ):
            bundle.add(
                dest / name,
                arcname=audit_id + "/" + name,
            )

    print(
        "G01I_V2_NUMERIC_DIFFERENCES="
        + str(len(differences))
    )

    for item in differences[:10]:
        print(
            "DIFF=" + item["path"]
            + " delta=" + str(item["abs_delta"])
        )

    print(
        "G01I_CHARGE_REVERSAL="
        "INVARIANT_CORRECTED"
    )

    print(
        "G01I_V2_AUDIT="
        + result["status"]
    )

    print("G01I_V2_RUN_DIR=" + str(dest))
    print("UPLOAD_ARCHIVE=" + str(archive))
    print(
        "UPLOAD_ARCHIVE_SHA256="
        + hash_file(archive)
    )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(
            "G01I_V2_HOLD=" + repr(exc),
            file=sys.stderr,
        )
        raise SystemExit(3)
