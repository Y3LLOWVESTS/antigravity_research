"""GRAVITY2-05 bounded Jordan-source stationarity/reciprocity gate.

Only L0, one worker and a time-limited child process. Legacy AGMINER and
all earlier GRAVITY2 producers are read-only. No loaded field solver.
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
from . import bridge05_core as core


BASE = ROOT / "results/gravity2/bridge05_runs"
MIB = 1024*1024

IDRE = re.compile(
    r"g205_\d{8}T\d{6}Z_[0-9a-f]{8}\Z"
)

SOURCES = (
    "bridge05_core.py",
    "bridge05.py",
    "bridge05_check.py",
)

PARENTS = {
    "G04_SCIENCE": (
        "results/gravity2/miner2_runs/"
        + core.PARENT_ID
        + "/science.json",
        core.PARENT_SCIENCE_SHA,
    ),
    "G04_VERIFIER": (
        "results/gravity2/miner2_runs/"
        + core.PARENT_ID
        + "/verification.json",
        core.PARENT_VERIFY_SHA,
    ),
}


def directory(run_id):
    if not IDRE.fullmatch(run_id):
        raise ValueError(
            "invalid GRAVITY2-05 run ID"
        )

    return BASE/run_id


def code_hashes():
    p = Path(__file__).resolve().parent

    return {
        name:digest(p/name)
        for name in SOURCES
    }


def parent_report():
    prev = {}

    for name,(relative,expected) in PARENTS.items():
        path = ROOT/relative

        actual = (
            digest(path)
            if path.is_file() and not path.is_symlink()
            else None
        )

        prev[name] = {
            "path": relative,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "status":
                "MATCH" if actual == expected
                else "HOLD",
        }

    hist,_ = read_pinned(ROOT)

    return {
        "previous": prev,
        "historical": hist,
        "all_match":
            all(
                x["status"] == "MATCH"
                for x in prev.values()
            )
            and all(
                x["status"] == "MATCH"
                for x in hist.values()
            ),
    }


def run(args):
    if args.level != "L0" or args.workers != 1:
        raise ValueError(
            "GRAVITY2-05 allows L0 one worker only; "
            "L1-L4 locked"
        )

    cap,ram,disk = PRESETS[args.preset]
    seconds = 60*args.minutes

    if (
        not math.isfinite(seconds)
        or not 0 < seconds <= cap
    ):
        raise ValueError(
            "time budget outside preset"
        )

    if args.dry_run:
        print(json.dumps({
            "program": "GRAVITY2-05",
            "mode": "L0_JORDAN_THEOREM_PREFLIGHT",
            "seconds_cap": seconds,
            "workers": 1,
            "memory_soft_mib": ram,
            "disk_soft_mib": disk,
            "historical_AGMINER": "READ_ONLY",
            "Einstein_and_PDE": "NOT_AUTHORIZED",
            "write_artifacts": False,
        },indent=2))

        return 0

    if not _rss_available():
        raise ValueError(
            "psutil required for bounded "
            "GRAVITY2-05 worker RSS"
        )

    if bytes_under(
        ROOT/"results/gravity2"
    ) > (GLOBAL_MIB-disk)*MIB:
        raise ValueError(
            "global GRAVITY2 storage budget exhausted"
        )

    parent = parent_report()

    BASE.mkdir(
        parents=True,
        exist_ok=True,
        mode=0o700,
    )

    rid = (
        datetime.now(timezone.utc).strftime(
            "g205_%Y%m%dT%H%M%SZ_"
        )
        + secrets.token_hex(4)
    )

    folder = directory(rid)
    folder.mkdir(mode=0o700)

    manifest = {
        "program": "GRAVITY2-05",
        "run_id": rid,
        "created_utc":
            datetime.now(timezone.utc).isoformat(),
        "preset": args.preset,
        "level": args.level,
        "workers": args.workers,
        "time_limit_seconds": seconds,
        "RSS_soft_mib": ram,
        "disk_soft_mib": disk,
        "producer_sha256": code_hashes(),
        "prior_modification": "NONE",
        "legacy_AGMINER":
            "READ_ONLY_HASH_NO_EXECUTION",
    }

    atomic_json(
        folder/"manifest.json",
        manifest,
    )

    result = None
    reason = "PARENT_HOLD"
    runtime = 0.0
    peak = None
    exit_code = None
    worker_log = ""

    if parent["all_match"]:
        env = dict(os.environ)

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
                "antigravity_research.gravity2.bridge05",
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
        deadline = start+seconds

        reason,exit_code,peak,worker_log,_ = supervise(
            child,
            folder,
            deadline,
            ram,
            disk,
        )

        runtime = round(
            time.monotonic()-start,
            5,
        )

        if reason == "COMPLETED" and exit_code == 0:
            try:
                result = json.loads(
                    (folder/"_worker.json").read_text()
                )
            except (OSError,ValueError):
                reason = "WORKER_BAD_JSON"

        elif reason == "COMPLETED":
            reason = "WORKER_ERROR"

        (folder/"_worker.json").unlink(
            missing_ok=True
        )

    atomic_text(
        folder/"worker.log",
        worker_log[-2048:],
    )

    if result is None:
        result = {
            "decision":
                "INCOMPLETE_NO_SCIENTIFIC_CLASSIFICATION",
            "survivors": 0,
        }

    sci = {
        "program": "GRAVITY2-05",
        "run_id": rid,
        "execution_status": reason,
        "parent_locks": parent,
        "evidence": result,
        "full_gravitational_action": "NOT_DERIVED",
        "real_source": "NOT_ESTABLISHED",
        "physical_lift": "NOT_DERIVED",
        "complete_energy": "NOT_CERTIFIED",
        "physical_survivors": 0,
        "loaded_PDE": "NOT_AUTHORIZED",
        "006D_replaced": False,
        "full_regression": "NOT_RUN",
        "resource": {
            "worker_elapsed_s": runtime,
            "peak_RSS_mib": peak,
            "memory_policy":
                "SOFT_PSUTIL_PROCESS_WATCHDOG",
            "worker_exit_code": exit_code,
        },
    }

    atomic_json(
        folder/"science.json",
        sci,
    )

    atomic_text(
        folder/"hashes.sha256",
        digest(folder/"manifest.json")
        +"  manifest.json\n"
        +digest(folder/"science.json")
        +"  science.json\n",
    )

    print("GRAVITY2_05_RUN="+rid)
    print("EXECUTION="+reason)

    print(
        "PARENTS="
        +(
            "LOCKED"
            if parent["all_match"]
            else "HOLD"
        )
    )

    print("DECISION="+result["decision"])
    print("PHYSICAL_SURVIVORS=0")

    print(
        "SCIENCE_SHA256="
        +digest(folder/"science.json")
    )

    return 0 if reason == "COMPLETED" else 3


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="gravity2.bridge05"
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    run_parser = sub.add_parser("run")

    run_parser.add_argument(
        "--level",
        choices=("L0","L1","L2","L3","L4"),
        default="L0",
    )

    run_parser.add_argument(
        "--preset",
        choices=tuple(PRESETS),
        default="quick",
    )

    run_parser.add_argument(
        "--minutes",
        type=float,
        default=.5,
    )

    run_parser.add_argument(
        "--workers",
        type=int,
        default=1,
    )

    run_parser.add_argument(
        "--dry-run",
        action="store_true",
    )

    for action in ("verify","report"):
        sub.add_parser(action).add_argument(
            "--run-id",
            required=True,
        )

    work = sub.add_parser("_worker")
    work.add_argument("--output",required=True)

    args = parser.parse_args(argv)

    try:
        if args.command == "run":
            return run(args)

        if args.command == "_worker":
            target = Path(args.output)

            if (
                target.name != "_worker.json"
                or not IDRE.fullmatch(target.parent.name)
                or target.parent.parent.resolve()
                    != BASE.resolve()
            ):
                raise ValueError(
                    "worker target not in owned run"
                )

            atomic_json(
                target,
                core.scientific_evidence(),
            )

            return 0

        folder = directory(args.run_id)

        if args.command == "verify":
            from .bridge05_check import verify
            return verify(folder)

        sci = json.loads(
            (folder/"science.json").read_text()
        )

        ev = sci["evidence"]

        print(json.dumps({
            "run_id": sci["run_id"],
            "execution": sci["execution_status"],
            "decision": ev["decision"],
            "static_obstruction":
                ev.get("weighted_static_source"),
            "source_portal_Hessian":
                ev.get("Jordan_trace_and_reciprocity"),
            "Higgs_erratum":
                ev.get("historical_Higgs_classification_erratum"),
            "gates": ev.get("gates"),
            "physical_lift": sci["physical_lift"],
        },indent=2))

        return 0

    except (
        OSError,
        ValueError,
        KeyError,
        AssertionError,
    ) as exc:
        print(
            "GRAVITY2_05_HOLD="+repr(exc),
            file=sys.stderr,
        )

        return 2

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
