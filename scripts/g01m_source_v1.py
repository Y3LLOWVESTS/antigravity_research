"""G01-M immutable runner.

Pins G01-L/G01-K evidence, runs a genuinely dynamical effective
source model, independently verifies, writes immutable JSON/SHA
and creates an upload archive.

Focused tests only by default. No full regression required.
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

from antigravity_research.gravity2.g01m_core import assemble
from g01m_check_v1 import independent_review


PARENTS = {
    "G01L_SCIENCE": (
        "results/gravity2/g01l_runs/"
        "g01l_20261122T002340Z_d286fcf8/science.json",
        "ab878109e7811ecdd3852f3b5eab72d3bf19420ba8b44f25e7a17536fb95f3e2",
    ),
    "G01L_VERIFICATION": (
        "results/gravity2/g01l_runs/"
        "g01l_20261122T002340Z_d286fcf8/verification.json",
        "5beeb43cbcde9954f15777204f7aa9594b62d3f0fbc312df8f55ce42d3494983",
    ),
    "G01L_MANIFEST": (
        "results/gravity2/g01l_runs/"
        "g01l_20261122T002340Z_d286fcf8/manifest.json",
        "6a4b68b2bbea9067dcdf29ae535c4ce8307dd51d9ea44155c69d8d149e7ad7c4",
    ),
    "G01K_SOURCE": (
        "scripts/g01k_source_v1.py",
        "cb6bc822e2dd363c48982f677c7d852317392098e4e7f610f3506e68e9468112",
    ),
}

BASE = ROOT / "results/gravity2/g01m_runs"

SOURCES = [
    "src/antigravity_research/gravity2/g01m_core.py",
    "scripts/g01m_check_v1.py",
    "scripts/g01m_source_v1.py",
    "tests/gravity2/test_g01m.py",
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    payload = (
        json.dumps(
            data, indent=2,
            sort_keys=True, allow_nan=False
        ) + "\n"
    ).encode()

    with path.open("xb") as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())


def load_parent():
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

        if name.startswith("G01L_"):
            found[name] = json.loads(path.read_bytes())

    science = found["G01L_SCIENCE"]
    verified = found["G01L_VERIFICATION"]
    manifest = found["G01L_MANIFEST"]

    if (
        verified["status"] !=
        "PASS_INDEPENDENT_SCOPED_TWO_SIDED_MAXWELL_AND_METRIC_AUDIT"
        or verified["science_sha256"] !=
        PARENTS["G01L_SCIENCE"][1]
        or manifest["full"]["status"] != "NOT_RUN"
        or manifest["focused"]["passed"] != 5
        or science["R3B_prescribed_capacity_J"]
        != 1.5429162116460216
        or science["historical_loaded_acceleration_m_s2"]
        != -129.67185782242464
        or science["physical_survivors"] != 0
    ):
        raise ValueError("G01L_PARENT_CLAIM_HOLD")

    return science


def focused_evidence(path):
    p = Path(path).resolve()

    if not p.is_file() or p.is_symlink():
        raise ValueError("FOCUSED_LOG_MISSING")

    body = p.read_text(errors="replace")

    found = re.findall(
        r"(?m)^\s*(\d+) passed"
        r"(?:, [^\n]*)? in \d+(?:\.\d+)?s\s*$",
        body,
    )

    if (
        len(found) != 1
        or "FAILED" in body
        or "ERROR" in body
    ):
        raise ValueError("FOCUSED_TEST_EVIDENCE_INVALID")

    return {
        "status": "PASS_SCOPED",
        "passed": int(found[0]),
        "sha256": sha(p),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--focused-log", required=True)
    args = parser.parse_args()

    if sys.flags.optimize:
        raise RuntimeError("OPTIMIZED_PYTHON_FORBIDDEN")

    if BASE.is_symlink():
        raise RuntimeError("RESULTS_SYMLINK_FORBIDDEN")

    BASE.mkdir(parents=True, exist_ok=True)

    rid = (
        datetime.now(timezone.utc).strftime(
            "g01m_%Y%m%dT%H%M%SZ_"
        )
        + secrets.token_hex(4)
    )

    out = BASE / rid
    out.mkdir(mode=0o700)

    verdict = "HOLD"

    try:
        focused = focused_evidence(args.focused_log)

        if focused["passed"] < 8:
            raise ValueError("INSUFFICIENT_FOCUSED_TESTS")

        parent = load_parent()

        save(out / "manifest.json", {
            "run_id": rid,
            "schema": "gravity2.g01m.manifest.v1",
            "parent_shas": {
                name: entry[1]
                for name, entry in PARENTS.items()
            },
            "source_shas": {
                rel: sha(ROOT / rel)
                for rel in SOURCES
            },
            "focused": focused,
            "full_regression": "NOT_RUN",
            "claim":
                "HYPOTHETICAL_EFFECTIVE_SOURCE_NOT_GRAVITATIONAL_ENGINE",
        })

        science = assemble(parent)
        save(out / "science.json", science)

        verification = independent_review(
            science, parent
        )

        verification["science_sha256"] = sha(
            out / "science.json"
        )

        save(
            out / "verification.json",
            verification,
        )

        verdict = "EFFECTIVE_SOURCE_ON_SHELL_TARGET_MISMATCH"

    except Exception as exc:
        save(out / "hold.json", {
            "status": "HOLD",
            "error_type": type(exc).__name__,
            "reason": str(exc),
        })

    with (out / "focused.log").open("xb") as dest:
        dest.write(
            Path(args.focused_log).read_bytes()
        )

    files = sorted(
        p.name for p in out.iterdir()
        if p.is_file()
    )

    ledger = "".join(
        sha(out / name) + "  " + name + "\n"
        for name in files
    )

    with (out / "SHA256SUMS.txt").open("xb") as f:
        f.write(ledger.encode())

    archive = out / (rid + "_UPLOAD.tar.gz")

    with tarfile.open(archive, "x:gz") as tf:
        for name in files + ["SHA256SUMS.txt"]:
            tf.add(
                out / name,
                arcname=rid + "/" + name,
            )

    print("G01M_RUN=" + rid)
    print("G01M_VERDICT=" + verdict)
    print("G01M_EVIDENCE=" + str(out))
    print("G01M_ARCHIVE=" + str(archive))
    print("G01M_ARCHIVE_SHA256=" + sha(archive))
    print("FULL_REGRESSION=NOT_RUN")
    print("PHYSICAL_SURVIVORS=0")
    print("WHOLE_CRAFT_GRAVITY=NOT_DERIVED")

    return 0 if verdict != "HOLD" else 2


if __name__ == "__main__":
    raise SystemExit(main())
