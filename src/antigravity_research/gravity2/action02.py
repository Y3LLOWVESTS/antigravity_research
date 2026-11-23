"""GRAVITY2-02 bounded action candidate CLI."""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
from datetime import datetime, timezone

from . import action02_core as core
from .action01 import supervise
from .engine import (
    ROOT, atomic_json, atomic_text, bytes_under, digest,
)
from .policy import PRESETS, GLOBAL_MIB

BASE = ROOT/"results"/"gravity2"/"action02_runs"
RUN_RE = re.compile(
    r"^g202_\d{8}T\d{6}Z_[0-9a-f]{8}$"
)
FILES = (
    "action02_core.py",
    "action02.py",
    "action02_verify.py",
)
MIB = 1024*1024


def run_path(name):
    if not RUN_RE.fullmatch(name):
        raise ValueError("invalid run ID")
    return BASE/name


def code_hashes():
    package = Path(__file__).resolve().parent
    return {
        n: digest(package/n)
        for n in FILES
    }


def execute(args):
    if args.level != "L0" or args.workers != 1:
        raise ValueError(
            "GRAVITY2-02: only L0 and one worker permitted"
        )

    cap, memory, disk = PRESETS[args.preset]
    seconds = 60*args.minutes

    if (
        not math.isfinite(seconds)
        or not 0 < seconds <= cap
    ):
        raise ValueError("invalid time/preset budget")

    if args.dry_run:
        print(json.dumps({
            "program": "GRAVITY2-02",
            "operation": "DRY_RUN_NO_WRITES",
            "level": "L0",
            "seconds": seconds,
            "workers": 1,
            "memory_soft_limit_mib": memory,
            "disk_soft_limit_mib": disk,
            "candidate_templates": len(core.CANDIDATES),
            "PDE": "DISABLED",
            "legacy_imports": "NONE",
        },indent=2))
        return 0

    if bytes_under(
        ROOT/"results"/"gravity2"
    ) > (GLOBAL_MIB-disk)*MIB:
        raise ValueError(
            "global 200 MiB budget reserve exhausted"
        )

    BASE.mkdir(parents=True,exist_ok=True,mode=0o700)

    rid = (
        datetime.now(timezone.utc).strftime(
            "g202_%Y%m%dT%H%M%SZ_"
        )
        +secrets.token_hex(4)
    )
    directory = run_path(rid)
    directory.mkdir(mode=0o700)

    manifest = {
        "program": "GRAVITY2-02",
        "run_id": rid,
        "level": args.level,
        "preset": args.preset,
        "max_seconds": seconds,
        "workers": 1,
        "rss_soft_limit_mib": memory,
        "disk_soft_limit_mib": disk,
        "producer_sha256": code_hashes(),
        "legacy_AGMINER": "READ_ONLY_HASH_NO_EXECUTION",
        "GRAVITY2_00_01": "NOT_MODIFIED",
    }
    atomic_json(directory/"manifest.json",manifest)

    env = dict(os.environ)
    env.update({
        "PYTHONPATH": str(ROOT/"src"),
        "PYTHONDONTWRITEBYTECODE": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "OMP_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "VECLIB_MAXIMUM_THREADS": "1",
    })

    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "antigravity_research.gravity2.action02",
            "_worker",
            "--output",str(directory/"_worker.json"),
        ],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=True,
        env=env,
    )
    reason,exitcode,elapsed,peak,monitor = supervise(
        proc,directory,seconds,memory,disk
    )

    evidence = None
    if reason=="COMPLETED" and exitcode==0:
        try:
            evidence=json.loads(
                (directory/"_worker.json").read_text()
            )
        except (OSError,ValueError):
            reason="WORKER_BAD_JSON"
    elif reason=="COMPLETED":
        reason="WORKER_ERROR"

    (directory/"_worker.json").unlink(
        missing_ok=True
    )

    if evidence is None:
        evidence={
            "decision":"INCOMPLETE_NO_SCIENTIFIC_RESULT",
            "gates":{"G00_PARENT":"NOT_RUN"},
            "qualified_survivors":0,
            "complete_action":"NOT_DERIVED",
        }

    science={
        "program":"GRAVITY2-02",
        "run_id":rid,
        "execution_status":reason,
        "evidence":evidence,
        "complete_covariant_action":"NOT_DERIVED",
        "qualified_physical_survivors":0,
        "whole_craft_lift":"NOT_DERIVED",
        "complete_energy":"NOT_CERTIFIED",
        "006D_replaced":False,
        "full_regression":"NOT_RUN",
        "resource":{
            "elapsed_seconds":elapsed,
            "worker_peak_rss_mib":peak,
            "rss_monitor":monitor,
            "limit_kind":"APPLICATION_SOFT_WATCHDOG",
            "worker_exit_code":exitcode,
        },
    }
    atomic_json(directory/"science.json",science)
    atomic_text(
        directory/"hashes.sha256",
        digest(directory/"manifest.json")
        +"  manifest.json\n"
        +digest(directory/"science.json")
        +"  science.json\n",
    )

    print("GRAVITY2_02_RUN="+rid)
    print("EXECUTION="+reason)
    print("DECISION="+evidence["decision"])
    print("CANDIDATES="+str(
        len(evidence.get("candidates",[]))
    ))
    print("QUALIFIED_SURVIVORS=0")
    print(
        "SCIENCE_SHA256="
        +digest(directory/"science.json")
    )
    print("RUN_DIR="+str(directory))
    return 0 if reason=="COMPLETED" else 3


def main():
    parser=argparse.ArgumentParser(
        prog="gravity2.action02"
    )
    sub=parser.add_subparsers(
        dest="command",required=True
    )

    run=sub.add_parser("run")
    run.add_argument(
        "--preset",choices=tuple(PRESETS),default="quick"
    )
    run.add_argument(
        "--level",
        choices=("L0","L1","L2","L3","L4"),
        default="L0",
    )
    run.add_argument("--minutes",type=float,default=1)
    run.add_argument("--workers",type=int,default=1)
    run.add_argument("--dry-run",action="store_true")

    worker=sub.add_parser("_worker")
    worker.add_argument("--output",required=True)

    verify=sub.add_parser("verify")
    verify.add_argument("--run-id",required=True)

    report=sub.add_parser("report")
    report.add_argument("--run-id",required=True)

    args=parser.parse_args()

    try:
        if args.command=="run":
            return execute(args)

        if args.command=="_worker":
            output=Path(args.output)
            if (
                output.name!="_worker.json"
                or output.parent.parent.resolve()!=BASE.resolve()
                or not RUN_RE.fullmatch(output.parent.name)
            ):
                raise ValueError(
                    "worker output outside GRAVITY2-02"
                )
            atomic_json(output,core.audit(ROOT))
            return 0

        if args.command=="verify":
            from .action02_verify import verify_run
            return verify_run(run_path(args.run_id))

        if args.command=="report":
            data=json.loads(
                (run_path(args.run_id)/"science.json").read_text()
            )
            e=data["evidence"]
            print("EXECUTION =",data["execution_status"])
            print("DECISION =",e["decision"])
            for c in e.get("candidates",[]):
                print(
                    "CANDIDATE =",c["id"],
                    "|",c["classification"]
                )
            for name,status in e["gates"].items():
                print("GATE =",name,"|",status)
            print("COMPLETE_ACTION =",data["complete_covariant_action"])
            print("WHOLE_CRAFT =",data["whole_craft_lift"])
            print("COMPLETE_ENERGY =",data["complete_energy"])
            return 0
    except (
        OSError,ValueError,KeyError,AssertionError
    ) as exc:
        print(
            "GRAVITY2_02_HOLD="+repr(exc),
            file=sys.stderr
        )
        return 2
    return 2


if __name__=="__main__":
    raise SystemExit(main())
