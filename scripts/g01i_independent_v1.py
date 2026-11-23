"""Independent R3B surface-charge energy and evidence verification."""
from __future__ import annotations

from hashlib import sha256
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
R = 2.0


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def encode(obj):
    return (
        json.dumps(obj, indent=2, sort_keys=True, allow_nan=False)
        + "\n"
    ).encode()


def review(science, rows, modes, normalization, conversion):
    reference = science["protected_prescribed_R3B_capacity_J"]

    if reference != 1.5429162116460216:
        raise ValueError("R3B_CAPACITY_CHANGED")

    if not rows or len(rows) != science["scanned_cases"]:
        raise ValueError("SOURCE_SCAN_INCOMPLETE")

    # Independent Legendre-mode orthogonality.
    for row in rows:
        subset = modes[:row["l_max"]]

        independent_energy = normalization * sum(
            math.pi * R * mode["amplitude"]**2 * conversion
            for mode in subset
        )

        archived_energy = normalization * sum(
            mode["electric_total_energy_j"]
            for mode in subset
        )

        if not math.isclose(
            independent_energy,
            archived_energy,
            rel_tol=1e-8,
            abs_tol=1e-11,
        ):
            raise ValueError("INDEPENDENT_MODE_ENERGY_FAIL")

        if not math.isclose(
            row["surface_charge_energy_J"],
            independent_energy,
            rel_tol=1e-8,
            abs_tol=1e-11,
        ):
            raise ValueError("SHELL_ENERGY_IDENTITY_FAIL")

        if (
            row["net_over_absolute_charge"] > 1e-9
            or row["stress_traction_scaled_error"] > 1e-11
        ):
            raise ValueError("CHARGE_OR_TRACTION_FAIL")

    if not math.isclose(
        science["electric_mirror_shell_energy_J"],
        rows[-1]["expected_energy_J"],
        rel_tol=1e-10,
    ):
        raise ValueError("TOTAL_ELECTRIC_ENERGY_DRIFT")

    if not math.isclose(
        science["conditional_DEC_remainder_energy_min_J"],
        reference / 3,
        abs_tol=1e-12,
    ):
        raise ValueError("DEC_TRACE_BOUND_DRIFT")

    if (
        science["conditional_field_plus_remainder_min_J"]
        != reference + reference / 3
    ):
        raise ValueError("DEC_TOTAL_BOUND_DRIFT")

    if (
        science["gates"]["G01_COMPLETE_COVARIANT_ACTION"] != "MISSING"
        or science["gates"]["G06_LOADED_RESPONSE"]
        != "HISTORICAL_INWARD_FAILURE"
        or science["physical_survivors"] != 0
        or science["whole_craft_lift"] != "NOT_DERIVED"
    ):
        raise ValueError("FALSE_PHYSICAL_PROMOTION")

    if (
        science["historical_loaded_failure"][
            "strong_loaded_minimum_acceleration_m_s2"
        ] >= 0
    ):
        raise ValueError("HISTORICAL_SIGN_CHANGED")

    controls = science["negative_controls"]

    if (
        len(controls) != 5
        or not all(type(v) is bool and v for v in controls.values())
    ):
        raise ValueError("NEGATIVE_CONTROL_INVALID")

    return {
        "status":
            "PASS_R3B_NECESSARY_SHELL_OBLIGATIONS_NO_LIFT",
        "independently_checked_cases": len(rows),
        "negative_controls": len(controls),
        "physical_survivors": 0,
        "source_action": "MISSING",
        "maximum_relative_energy_error": max(
            row["energy_relative_error"] for row in rows
        ),
    }


def verify(folder):
    try:
        import g01i_r3b_source_v1 as producer

        if folder.is_symlink() or not folder.is_dir():
            raise ValueError("UNSAFE_RESULT_DIRECTORY")

        manifest = json.loads(
            (folder / "manifest.json").read_text()
        )

        science = json.loads(
            (folder / "science.json").read_text()
        )

        rows = json.loads(
            (folder / "mode_scan.json").read_text()
        )

        parents, modes, normalization, conversion = producer.parent()

        if (
            manifest["parent_sha256"] != parents
            or manifest["run_id"] != folder.name
        ):
            raise ValueError("PARENT_PROVENANCE_DRIFT")

        source_sha = {
            name: digest(ROOT / "scripts" / name)
            for name in (
                "g01i_r3b_source_v1.py",
                "g01i_independent_v1.py",
            )
        }

        if manifest["source_sha256"] != source_sha:
            raise ValueError("SOURCE_CODE_DRIFT")

        recomputed, scan = producer.evaluate(
            modes, normalization, conversion
        )

        if recomputed != science or scan != rows:
            raise ValueError("SCIENCE_RECOMPUTATION_DRIFT")

        verdict = review(
            science, rows, modes, normalization, conversion
        )

        verdict.update({
            "manifest_sha256":
                digest(folder / "manifest.json"),
            "science_sha256":
                digest(folder / "science.json"),
            "mode_scan_sha256":
                digest(folder / "mode_scan.json"),
        })

        destination = folder / "verification.json"
        encoded = encode(verdict)

        if destination.exists():
            if (
                destination.is_symlink()
                or destination.read_bytes() != encoded
            ):
                raise ValueError("VERIFICATION_IMMUTABILITY_HOLD")
        else:
            with destination.open("xb") as stream:
                stream.write(encoded)

        print("G01I_INDEPENDENT_VERIFY=" + verdict["status"])
        return 0

    except Exception as exc:
        print("G01I_VERIFY_HOLD=" + repr(exc))
        return 3


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()

    if not re.fullmatch(
        r"g01i_\d{8}T\d{6}Z_[a-f0-9]{8}",
        args.run_id,
    ):
        raise SystemExit("UNSAFE_RUN_ID")

    folder = (
        ROOT / "results/gravity2/g01i_runs"
        / args.run_id
    )

    raise SystemExit(verify(folder))
