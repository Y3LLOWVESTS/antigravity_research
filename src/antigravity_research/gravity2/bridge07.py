"""GRAVITY2-07 bounded two-dimensional numerical Y-field preflight.

Seals manifest.json, science.json, fields.npz and SHA-256 provenance.
No AGMINER execution, no modification of previous GRAVITY2 checkpoints.
No physical source, Einstein solution or spacecraft lift is asserted.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import time

import numpy as np

from .engine import (
    ROOT,
    atomic_json,
    atomic_text,
    digest,
    bytes_under,
)
from .policy import PRESETS, GLOBAL_MIB
from .miner import supervise, _rss_available
from .action01_core import read_pinned
from . import bridge07_core as core


BASE = ROOT / "results/gravity2/bridge07_runs"

RUN_RE = re.compile(
    r"g207_\d{8}T\d{6}Z_[0-9a-f]{8}\Z"
)

SOURCE_FILES = (
    "src/antigravity_research/gravity2/bridge07_core.py",
    "src/antigravity_research/gravity2/bridge07.py",
    "src/antigravity_research/gravity2/bridge07_check.py",
    "tests/gravity2/test_bridge07.py",
)

MIB = 1024*1024

PARENTS = {
    "G06_SCIENCE": (
        "results/gravity2/bridge06_runs/"
        "g206_20261121T063924Z_a430c5c5/science.json",
        "e2a8a141b86e2168912a4110cc258ec0cec65cae909bc9da999f30216901b1a5",
    ),
    "G06_VERIFICATION": (
        "results/gravity2/bridge06_runs/"
        "g206_20261121T063924Z_a430c5c5/verification.json",
        "ef9c9ebff7c3c3b32bf40bbaee140bbd62bf3998f37abf698ed84ce36150b883",
    ),
}


def owned(run_id):
    if not RUN_RE.fullmatch(run_id):
        raise ValueError(
            "invalid GRAVITY2-07 run ID"
        )

    return BASE/run_id


def sources():
    return {
        name: digest(ROOT/name)
        for name in SOURCE_FILES
    }


def parents():
    locks = {}

    for name, (relative, sha) in PARENTS.items():
        path = ROOT/relative

        actual = (
            digest(path)
            if path.is_file() and not path.is_symlink()
            else None
        )

        locks[name] = {
            "path": relative,
            "expected_sha256": sha,
            "actual_sha256": actual,
            "status":
                "MATCH" if actual == sha else "HOLD",
        }

    historical, _ = read_pinned(ROOT)

    return {
        "previous": locks,
        "historical": historical,
        "all_match":
            all(
                x["status"] == "MATCH"
                for x in locks.values()
            )
            and all(
                x["status"] == "MATCH"
                for x in historical.values()
            ),
    }


def worker(output):
    target = Path(output)

    if (
        target.name != "_worker.json"
        or not RUN_RE.fullmatch(target.parent.name)
        or target.parent.parent.resolve()
            != BASE.resolve()
    ):
        raise ValueError(
            "worker escaped owned run directory"
        )

    result, archive = core.scientific_run()

    field_file = target.parent/"fields.npz"

    # O_EXCL: do not overwrite existing archives.
    with field_file.open("xb") as handle:
        np.savez_compressed(handle, **archive)
        handle.flush()
        os.fsync(handle.fileno())

    atomic_json(target, result)


def run(args):
    if args.level != "L1" or args.workers != 1:
        raise ValueError(
            "GRAVITY2-07 permits L1/one worker only; "
            "L2-L4 remain locked"
        )

    cap, ram, disk = PRESETS[args.preset]
    seconds = args.minutes*60

    if (
        not math.isfinite(seconds)
        or not 0 < seconds <= cap
    ):
        raise ValueError(
            "time budget outside preset"
        )

    if args.dry_run:
        print(json.dumps({
            "program": "GRAVITY2-07",
            "scope":
                "2D_PORTAL_Y_EULER_ONLY_"
                "FROZEN_SOURCE_AND_X",
            "grids": core.GRIDS,
            "seconds_ceiling": seconds,
            "rss_soft_mib": ram,
            "disk_soft_mib": disk,
            "worker_count": 1,
            "L2_to_L4": "LOCKED",
            "writes": False,
        }, indent=2))

        return 0

    if not _rss_available():
        raise ValueError(
            "psutil required for soft RSS watchdog"
        )

    if bytes_under(
        ROOT/"results/gravity2"
    ) > (GLOBAL_MIB-disk)*MIB:
        raise ValueError(
            "global GRAVITY2 storage limit exceeded; "
            "no automatic pruning"
        )

    lock = parents()

    BASE.mkdir(
        parents=True,
        exist_ok=True,
        mode=0o700,
    )

    run_id = (
        datetime.now(timezone.utc).strftime(
            "g207_%Y%m%dT%H%M%SZ_"
        )
        + secrets.token_hex(4)
    )

    folder = owned(run_id)
    folder.mkdir(mode=0o700)

    manifest = {
        "program": "GRAVITY2-07",
        "run_id": run_id,
        "created_utc":
            datetime.now(timezone.utc).isoformat(),
        "preset": args.preset,
        "level": "L1",
        "workers": 1,
        "time_ceiling_s": seconds,
        "rss_soft_mib": ram,
        "disk_soft_mib": disk,
        "producer_sha256": sources(),
        "previous_source_modification": "NONE",
        "AGMINER":
            "READ_ONLY_PINNED_HASHES_NOT_EXECUTED",
        "solver":
            "2D_PERIODIC_ODE_INVERSION_AND_"
            "NONLINEAR_FIXED_POINT",
        "field_geometry":
            "A_X0=a(x,z) fixed; A_Yy=b(x,z) solved; "
            "scalar f fixed",
    }

    atomic_json(
        folder/"manifest.json",
        manifest,
    )

    status = "PARENT_HOLD"
    result = None
    elapsed = 0.0
    peak = None
    exitcode = None
    workerlog = ""

    if lock["all_match"]:
        env = os.environ.copy()

        env.update({
            "PYTHONPATH": str(ROOT/"src"),
            "PYTHONDONTWRITEBYTECODE": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1",
            "MKL_NUM_THREADS": "1",
            "VECLIB_MAXIMUM_THREADS": "1",
        })

        child = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "antigravity_research.gravity2.bridge07",
                "_worker",
                "--output",
                str(folder/"_worker.json"),
            ],
            cwd=ROOT,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

        start = time.monotonic()

        (
            status,
            exitcode,
            peak,
            workerlog,
            _,
        ) = supervise(
            child,
            folder,
            start+seconds,
            ram,
            disk,
        )

        elapsed = round(
            time.monotonic()-start, 5
        )

        if status == "COMPLETED" and exitcode == 0:
            try:
                result = json.loads(
                    (folder/"_worker.json").read_text()
                )

                if not (folder/"fields.npz").is_file():
                    status = "ARCHIVE_MISSING"

            except (OSError, ValueError):
                status = "WORKER_BAD_JSON"

        elif status == "COMPLETED":
            status = "WORKER_ERROR"

        (folder/"_worker.json").unlink(
            missing_ok=True
        )

    atomic_text(
        folder/"worker.log",
        workerlog[-2048:],
    )

    if status != "COMPLETED":
        result = {
            "decision": "INCOMPLETE_NO_SCIENCE",
            "physical_survivors": 0,
        }

    archive_sha = (
        digest(folder/"fields.npz")
        if (folder/"fields.npz").is_file()
        else None
    )

    science = {
        "program": "GRAVITY2-07",
        "run_id": run_id,
        "execution_status": status,
        "parents": lock,
        "evidence": result,
        "field_archive_sha256": archive_sha,
        "source_still_prescribed": True,
        "real_finite_source": "NOT_ESTABLISHED",
        "source_support_Earth": "NOT_DERIVED",
        "physical_exterior": "NOT_SOLVED",
        "full_Lorentzian_mode_health":
            "NOT_DERIVED",
        "Einstein_gravity": "NOT_SOLVED",
        "whole_craft_lift": "NOT_DERIVED",
        "complete_energy_SI": "NOT_CERTIFIED",
        "006D_replaced": False,
        "qualified_survivors": 0,
        "full_repository_regression": "NOT_RUN",
        "L2_authorized": False,
        "resource": {
            "elapsed_s": elapsed,
            "worker_peak_rss_mib": peak,
            "worker_exit_code": exitcode,
            "watchdog": "SOFT_PSUTIL_PROCESS",
        },
    }

    atomic_json(
        folder/"science.json",
        science,
    )

    records = [
        "manifest.json",
        "science.json",
    ]

    if archive_sha is not None:
        records.append("fields.npz")

    atomic_text(
        folder/"hashes.sha256",
        "".join(
            digest(folder/name)
            + "  "
            + name
            + "\n"
            for name in records
        ),
    )

    print("GRAVITY2_07_RUN=" + run_id)
    print("EXECUTION=" + status)

    print(
        "PARENTS="
        + ("LOCKED" if lock["all_match"] else "HOLD")
    )

    print("DECISION=" + result["decision"])

    if status == "COMPLETED":
        for row in result["rows"]:
            print(
                "GRID_N=" + str(row["n"])
                + " RESIDUAL="
                + str(row["equation_residual_relative"])
                + " BIANCHI="
                + str(row["bianchi_max_abs"])
                + " Y_MAX="
                + str(row["y_field_max_abs"])
            )

    print(
        "PHYSICAL_SURVIVORS=0; "
        "SOURCE_AND_X_PRESCRIBED=YES"
    )

    print(
        "SCIENCE_SHA256="
        + digest(folder/"science.json")
    )

    return 0 if status == "COMPLETED" else 3


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="gravity2.bridge07"
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    r = sub.add_parser("run")

    r.add_argument(
        "--level",
        choices=("L0", "L1", "L2", "L3", "L4"),
        default="L1",
    )

    r.add_argument(
        "--preset",
        choices=tuple(PRESETS),
        default="quick",
    )

    r.add_argument(
        "--minutes",
        type=float,
        default=.5,
    )

    r.add_argument(
        "--workers",
        type=int,
        default=1,
    )

    r.add_argument(
        "--dry-run",
        action="store_true",
    )

    for name in ("verify", "report"):
        sub.add_parser(name).add_argument(
            "--run-id",
            required=True,
        )

    child = sub.add_parser("_worker")
    child.add_argument(
        "--output",
        required=True,
    )

    args = parser.parse_args(argv)

    try:
        if args.command == "run":
            return run(args)

        if args.command == "_worker":
            worker(args.output)
            return 0

        folder = owned(args.run_id)

        if args.command == "verify":
            from .bridge07_check import verify
            return verify(folder)

        science = json.loads(
            (folder/"science.json").read_text()
        )

        print(json.dumps({
            "run_id": args.run_id,
            "status": science["execution_status"],
            "decision": science["evidence"]["decision"],
            "rows":
                science["evidence"].get("rows", []),
            "controls":
                science["evidence"].get("controls", {}),
            "source": science["real_finite_source"],
            "lift": science["whole_craft_lift"],
        }, indent=2))

        return 0

    except (
        OSError,
        ValueError,
        KeyError,
        RuntimeError,
        AssertionError,
    ) as exc:
        print(
            "GRAVITY2_07_HOLD=" + repr(exc),
            file=sys.stderr,
        )

        return 2

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
