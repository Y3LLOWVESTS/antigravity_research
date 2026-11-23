"""G01-L immutable runner for GRAVITY2 source/action audit.

Exact SHA-256 parent locks, independent science checker,
immutable JSON, test logs, SHA ledger and single archive.

Does not overwrite G01-J/K results. A scoped action audit
is not a physical gravitational survivor.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from antigravity_research.gravity2 import g01l_core as core

PARENTS = core.PARENTS
CAPACITY = core.CAPACITY
HISTORICAL_INWARD = core.HISTORICAL_INWARD
BASE = ROOT / "results/gravity2/g01l_runs"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, data: dict) -> None:
    payload = (
        json.dumps(
            data, indent=2, sort_keys=True, allow_nan=False
        ) + "\n"
    ).encode()

    with path.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


def load_parents():
    found = {}

    for name, (relative, expected) in PARENTS.items():
        path = ROOT / relative

        if (
            not path.is_file()
            or path.is_symlink()
            or sha(path) != expected
        ):
            raise ValueError(
                "LOCKED_PARENT_MISSING_OR_SHA_DRIFT:" + name
            )

        if name.endswith("_SCIENCE"):
            found[name] = json.loads(path.read_text())

    k = found["G01K_SCIENCE"]
    j = found["G01J_SCIENCE"]

    if (
        k["status"]
        != "PASS_SCOPED_LOCAL_STATIC_SOURCE_RESPONSE_NOT_GRAVITY"
        or k["protected_R3B_capacity_J"] != CAPACITY
        or k["historical_loaded_min_m_s2"]
        != HISTORICAL_INWARD
        or k["physical_survivors"] != 0
        or j["R3B_prescribed_field_capacity_J"] != CAPACITY
        or len(k["modes"]) != 12
        or len(j["modes"]) != 12
    ):
        raise ValueError("PARENT_SCIENTIFIC_CLAIM_DRIFT")

    return k, j


def valid_pytest_log(path):
    if not path:
        return {"status": "NOT_RUN"}

    p = Path(path).resolve()

    if not p.is_file() or p.is_symlink():
        raise ValueError("TEST_LOG_MISSING_OR_SYMLINK")

    contents = p.read_text(errors="replace")

    matches = re.findall(
        r"(?m)^\s*(\d+) passed"
        r"(?:, [^\n]*)? in \d+(?:\.\d+)?s\s*$",
        contents,
    )

    if (
        len(matches) != 1
        or "FAILED" in contents
        or "ERROR" in contents
    ):
        raise ValueError("TEST_LOG_UNVERIFIED")

    return {
        "status": "PASS_SCOPED_SOFTWARE",
        "passed": int(matches[0]),
        "sha256": sha(p),
        "origin": str(p),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--focused-log")
    parser.add_argument("--full-log")
    args = parser.parse_args()

    if sys.flags.optimize:
        raise RuntimeError("OPTIMIZED_PYTHON_FORBIDDEN")

    if BASE.is_symlink():
        raise RuntimeError("RESULTS_SYMLINK_FORBIDDEN")

    BASE.mkdir(parents=True, exist_ok=True)

    rid = (
        datetime.now(timezone.utc).strftime(
            "g01l_%Y%m%dT%H%M%SZ_"
        )
        + secrets.token_hex(4)
    )

    out = BASE / rid
    out.mkdir(mode=0o700)

    source_paths = (
        "scripts/g01l_source_v1.py",
        "scripts/g01l_check_v1.py",
        "src/antigravity_research/gravity2/g01l_core.py",
    )

    manifest = {
        "run_id": rid,
        "schema": "gravity2.g01l.manifest.v1",
        "source_shas": {
            rel: sha(ROOT / rel)
            for rel in source_paths
        },
        "parent_shas": {
            name: entry[1]
            for name, entry in PARENTS.items()
        },
        "focused": valid_pytest_log(
            args.focused_log
        ),
        "full": valid_pytest_log(
            args.full_log
        ),
    }

    save(out / "manifest.json", manifest)

    try:
        import g01l_check_v1

        k, j = load_parents()
        science = core.compute(k, j)

        save(out / "science.json", science)

        independent = g01l_check_v1.review(
            science, k, j
        )

        independent["science_sha256"] = sha(
            out / "science.json"
        )

        save(out / "verification.json", independent)

        verdict = "ACTION_INCOMPLETE"

    except Exception as exc:
        verdict = "HOLD"

        save(
            out / "hold.json",
            {
                "status": "HOLD",
                "exception": repr(exc),
            },
        )

    for key, source in (
        ("focused", args.focused_log),
        ("full", args.full_log),
    ):
        if source:
            with (out / (key + ".log")).open("xb") as dest:
                dest.write(Path(source).read_bytes())

    names = sorted(
        p.name for p in out.iterdir()
        if p.is_file()
    )

    ledger = "".join(
        sha(out / name) + "  " + name + "\n"
        for name in names
    )

    with (out / "SHA256SUMS.txt").open("xb") as f:
        f.write(ledger.encode())

    archive = out / (rid + "_UPLOAD.tar.gz")

    with tarfile.open(archive, "x:gz") as tar:
        for name in names + ["SHA256SUMS.txt"]:
            tar.add(
                out / name,
                arcname=rid + "/" + name,
            )

    print("G01L_RUN=" + rid)
    print("G01L_VERDICT=" + verdict)
    print("G01L_EVIDENCE=" + str(out))
    print("G01L_ARCHIVE=" + str(archive))
    print("G01L_ARCHIVE_SHA256=" + sha(archive))
    print("PHYSICAL_SURVIVORS=0")
    print("GRAVITATIONAL_LIFT=NOT_DERIVED")

    return 0 if verdict == "ACTION_INCOMPLETE" else 3


if __name__ == "__main__":
    raise SystemExit(main())
