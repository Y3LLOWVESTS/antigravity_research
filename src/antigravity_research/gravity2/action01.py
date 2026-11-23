"""GRAVITY2-01 bounded action provenance CLI.

Separate from GRAVITY2-00 and the legacy AGMINER.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import secrets
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone

from . import action01_core as core
from .engine import (
    ROOT, atomic_json, atomic_text, bytes_under, digest,
)
from .policy import PRESETS, GLOBAL_MIB


BASE = ROOT / "results" / "gravity2" / "action01_runs"
IDRE = re.compile(r"^g201_\d{8}T\d{6}Z_[0-9a-f]{8}$")
SOURCES = (
    "action01.py",
    "action01_core.py",
    "action01_verify.py",
)
MIB = 1024 * 1024


def hashes():
    root = Path(__file__).resolve().parent
    return {
        f: digest(root/f)
        for f in SOURCES
    }


def checked_id(name):
    if not IDRE.fullmatch(name):
        raise ValueError("invalid GRAVITY2-01 run ID")
    return BASE/name


def worker(out: Path):
    if (
        out.name != "_worker.json"
        or out.parent.parent.resolve() != BASE.resolve()
    ):
        raise ValueError(
            "worker destination outside GRAVITY2-01 runs"
        )

    result = core.audit(ROOT)
    atomic_json(out, result)

    print(
        "G01_WORKER_DECISION=" + result["decision"],
        flush=True,
    )


def rss_mib(pid):
    try:
        import psutil
    except ImportError:
        return None

    try:
        p = psutil.Process(pid)

        return sum(
            x.memory_info().rss
            for x in [p, *p.children(recursive=True)]
            if x.is_running()
        ) / MIB

    except psutil.Error:
        return 0.0


def kill_own_group(p):
    if p.poll() is not None:
        return

    try:
        os.killpg(p.pid, signal.SIGTERM)
    except ProcessLookupError:
        return

    try:
        p.wait(timeout=0.5)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

        p.wait(timeout=1)


def supervise(p, outdir, sec, memory_mib, disk_mib):
    assert p.stdout is not None

    os.set_blocking(p.stdout.fileno(), False)

    start = time.monotonic()
    buf = bytearray()
    peak = None
    reason = "COMPLETED"
    rss_available = rss_mib(p.pid) is not None

    try:
        while True:
            try:
                chunk = os.read(
                    p.stdout.fileno(), 4096
                )

                if len(buf) < 16384:
                    buf.extend(
                        chunk[:16384-len(buf)]
                    )
            except BlockingIOError:
                pass

            ram = rss_mib(p.pid)

            if ram is not None:
                peak = max(peak or 0, ram)

                if ram > memory_mib:
                    reason = "MEMORY_SOFT_LIMIT"
                    break

            if bytes_under(outdir) > min(
                disk_mib, 8
            ) * MIB:
                reason = "DISK_SOFT_LIMIT"
                break

            if time.monotonic()-start >= sec:
                reason = "TIME_BUDGET_EXCEEDED"
                break

            if p.poll() is not None:
                break

            time.sleep(0.04)

    except KeyboardInterrupt:
        reason = "INTERRUPTED"

    finally:
        if reason != "COMPLETED":
            kill_own_group(p)

        try:
            p.wait(timeout=1)
        except subprocess.TimeoutExpired:
            kill_own_group(p)

        try:
            while len(buf) < 16384:
                chunk = os.read(
                    p.stdout.fileno(), 4096
                )
                if not chunk:
                    break

                buf.extend(
                    chunk[:16384-len(buf)]
                )
        except (OSError, BlockingIOError):
            pass

        p.stdout.close()

    atomic_text(
        outdir/"worker.log",
        buf.decode("utf-8", "replace"),
    )

    return (
        reason,
        p.returncode,
        round(time.monotonic()-start, 4),
        round(peak, 3) if peak is not None else None,
        (
            "PSUTIL_SOFT_LIMIT"
            if rss_available
            else "RSS_UNMONITORED_L0_ONLY"
        ),
    )


def run(args):
    if args.level != "L0":
        raise ValueError(
            "GRAVITY2-01 is L0 only; L1+ disabled"
        )

    if args.workers != 1:
        raise ValueError(
            "GRAVITY2-01 permits one worker only"
        )

    cap, mem, disk = PRESETS[args.preset]
    seconds = args.minutes * 60

    if not (0 < seconds <= cap):
        raise ValueError(
            "minute request outside preset cap"
        )

    if args.dry_run:
        print(json.dumps({
            "mode": "GRAVITY2-01_READ_ONLY_AST",
            "preset": args.preset,
            "seconds_cap": seconds,
            "workers": 1,
            "rss_soft_mib": mem,
            "disk_per_run_soft_mib": disk,
            "no_legacy_imports": True,
            "no_PDE": True,
            "full_regression": "NOT_RUN",
        }, indent=2))

        return 0

    if bytes_under(
        ROOT/"results"/"gravity2"
    ) > (GLOBAL_MIB-disk)*MIB:
        raise ValueError(
            "GRAVITY2 storage budget exhausted; "
            "no evidence auto-deleted"
        )

    BASE.mkdir(
        parents=True,
        exist_ok=True,
        mode=0o700,
    )

    ident = (
        datetime.now(timezone.utc).strftime(
            "g201_%Y%m%dT%H%M%SZ_"
        )
        + secrets.token_hex(4)
    )

    directory = checked_id(ident)
    directory.mkdir(mode=0o700)

    man = {
        "program": "GRAVITY2-01",
        "run_id": ident,
        "utc": datetime.now(timezone.utc).isoformat(),
        "preset": args.preset,
        "level": args.level,
        "time_limit_s": seconds,
        "rss_soft_limit_mib": mem,
        "disk_soft_limit_mib": disk,
        "codes_sha256": hashes(),
        "legacy_AGMINER_write_or_execution": "NONE",
        "old_GRAVITY2_00_code_modified": False,
        "science_claim":
            "ACTION_PROVENANCE_INVENTORY_ONLY",
    }

    atomic_json(
        directory/"manifest.json", man
    )

    env = os.environ.copy()

    env.update({
        "PYTHONPATH": str(ROOT/"src"),
        "PYTHONDONTWRITEBYTECODE": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "OMP_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "VECLIB_MAXIMUM_THREADS": "1",
    })

    p = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "antigravity_research.gravity2.action01",
            "_worker",
            "--output",
            str(directory/"_worker.json"),
        ],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=True,
        env=env,
    )

    (
        reason,
        exitcode,
        elapsed,
        peak,
        memmode,
    ) = supervise(
        p, directory, seconds, mem, disk
    )

    evidence = None

    if reason == "COMPLETED" and exitcode == 0:
        try:
            evidence = json.loads(
                (directory/"_worker.json").read_text()
            )
        except (OSError, ValueError):
            reason = "WORKER_BAD_JSON"

    elif reason == "COMPLETED":
        reason = "WORKER_ERROR"

    (directory/"_worker.json").unlink(
        missing_ok=True
    )

    if evidence is None:
        evidence = {
            "decision":
                "INCOMPLETE_NO_SCIENTIFIC_CLASSIFICATION",
            "gates": {
                "G00_PARENT": "NOT_RUN",
                "G01_ACTION": "NOT_RUN",
                "G02_VARIATION": "NOT_RUN",
            },
        }

    sci = {
        "program": "GRAVITY2-01",
        "run_id": ident,
        "execution_status": reason,
        "evidence": evidence,
        "complete_covariant_action": "NOT_DERIVED",
        "physical_lift": "NOT_DERIVED",
        "complete_energy": "NOT_CERTIFIED",
        "new_source_action_survivors": 0,
        "006D_replaced": False,
        "full_regression": "NOT_RUN",
        "resource": {
            "elapsed_s": elapsed,
            "peak_worker_RSS_MiB": peak,
            "memory_monitor": memmode,
            "limit_class":
                "APPLICATION_WATCHDOG_SOFT_LIMITS",
            "worker_exit_code": exitcode,
        },
    }

    atomic_json(
        directory/"science.json", sci
    )

    atomic_text(
        directory/"hashes.sha256",
        digest(directory/"manifest.json")
        + "  manifest.json\n"
        + digest(directory/"science.json")
        + "  science.json\n",
    )

    print("GRAVITY2_01_RUN=" + ident)
    print("EXECUTION=" + reason)
    print("DECISION=" + evidence["decision"])
    print(
        "G00=" + evidence["gates"]["G00_PARENT"]
    )
    print(
        "G01=" + evidence["gates"]["G01_ACTION"]
    )
    print(
        "SCIENCE_SHA256="
        + digest(directory/"science.json")
    )
    print("RUN_DIR=" + str(directory))

    return 0 if reason == "COMPLETED" else 3


def main():
    parser = argparse.ArgumentParser(
        prog="gravity2.action01",
        description="Read-only bounded R3B action provenance",
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    runp = sub.add_parser("run")
    runp.add_argument(
        "--level",
        default="L0",
        choices=("L0", "L1", "L2", "L3", "L4"),
    )
    runp.add_argument(
        "--preset",
        default="quick",
        choices=tuple(PRESETS),
    )
    runp.add_argument(
        "--minutes",
        default=1.,
        type=float,
    )
    runp.add_argument(
        "--workers",
        default=1,
        type=int,
    )
    runp.add_argument(
        "--dry-run",
        action="store_true",
    )

    verify = sub.add_parser("verify")
    verify.add_argument("--run-id", required=True)

    report = sub.add_parser("report")
    report.add_argument("--run-id", required=True)

    workerp = sub.add_parser("_worker")
    workerp.add_argument("--output", required=True)

    args = parser.parse_args()

    try:
        if args.command == "run":
            return run(args)

        if args.command == "_worker":
            worker(Path(args.output))
            return 0

        if args.command == "verify":
            from .action01_verify import verify_run
            return verify_run(
                checked_id(args.run_id)
            )

        if args.command == "report":
            s = json.loads(
                (
                    checked_id(args.run_id)
                    / "science.json"
                ).read_text()
            )

            print(json.dumps({
                "run_id": s["run_id"],
                "execution": s["execution_status"],
                "gates": s["evidence"]["gates"],
                "decision": s["evidence"]["decision"],
                "missing_action_terms":
                    s["evidence"].get(
                        "action_terms", {}
                    ),
                "model_separation":
                    s["evidence"].get(
                        "historical_classification_correction",
                        {},
                    ),
            }, indent=2))

            return 0

    except (
        OSError,
        ValueError,
        KeyError,
        AssertionError,
    ) as exc:
        print(
            "GRAVITY2_01_HOLD=" + repr(exc),
            file=sys.stderr,
        )
        return 2

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
