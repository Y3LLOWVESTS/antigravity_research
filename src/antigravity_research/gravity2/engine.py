"""GRAVITY2-00 safe runner: provenance only, no candidate physics solvers.

All mutable program state is confined to results/gravity2. Legacy AGMINER is
never imported, executed, or written to. The worker is isolated in a new process
session. Memory and disk limits are soft watchdog limits, not OS sandbox quotas.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import secrets
import signal
import sqlite3
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

from .policy import (
    ANCHORS, GATES, GLOBAL_MIB, HISTORICAL_FAILURES,
    LOG_MAX_BYTES, OPTIONAL_RESULTS, PARENTS, PRESETS,
    PROGRAM, SCHEMA, SCRATCH_MIB,
)

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "results" / "gravity2"
RUNS = OUTPUT / "runs"
RUN_RE = re.compile(r"^g2_\d{8}T\d{6}Z_[0-9a-f]{8}$")
MIB = 1024 * 1024


def digest(path: Path) -> str:
    """Compute SHA-256 once at an evidence boundary."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def bytes_under(path: Path) -> int:
    """Count only files within GRAVITY2-owned paths."""
    if not path.exists():
        return 0

    total = 0
    for base, dirs, files in os.walk(path, followlinks=False):
        dirs[:] = [
            d for d in dirs
            if not (Path(base) / d).is_symlink()
        ]

        for name in files:
            p = Path(base) / name
            if p.is_file() and not p.is_symlink():
                total += p.stat().st_size

    return total


def atomic_json(path: Path, obj: dict) -> None:
    """Publish strict JSON atomically without overwriting old evidence."""

    def native(value):
        # Support NumPy scalar/bool values without accepting arrays.
        if hasattr(value, "item"):
            scalar = value.item()
            if isinstance(scalar, (bool, int, float, str, type(None))):
                return scalar
        raise TypeError(
            "unsupported JSON type: " + type(value).__name__
        )

    text = json.dumps(
        obj,
        sort_keys=True,
        indent=2,
        allow_nan=False,
        default=native,
    ) + "\n"

    fd, temp = tempfile.mkstemp(
        prefix=".pending_",
        dir=path.parent,
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())

        # An existing immutable destination cannot be replaced.
        os.link(temp, path)

    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def atomic_text(path: Path, text: str) -> None:
    """Create text evidence using the same no-clobber policy."""
    fd, temp = tempfile.mkstemp(
        prefix=".pending_",
        dir=path.parent,
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())

        os.link(temp, path)

    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def utc() -> str:
    return datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def source_hashes() -> dict:
    """Record producing-code hashes without storing duplicate code."""
    here = Path(__file__).resolve().parent

    return {
        name: digest(here / name)
        for name in (
            "__init__.py",
            "policy.py",
            "engine.py",
            "independent.py",
        )
    }


def parent_audit() -> dict:
    """Read-only SHA inspection; never import the old AGMINER."""
    parents = {}

    for label, (rel, expected) in PARENTS.items():
        path = ROOT / rel
        actual = digest(path) if path.is_file() else None

        parents[label] = {
            "path_relative_to_repo": rel,
            "sha256_expected": expected,
            "sha256_actual": actual,
            "status": (
                "MATCH" if actual == expected
                else "MISSING" if actual is None
                else "DRIFT"
            ),
            "mandatory": True,
        }

    # Only look one level into known F0 result directories.
    # No recursive scan of the historical repository.
    for label, (pattern, filename, expected) in OPTIONAL_RESULTS.items():
        matches = [
            p
            for p in (ROOT / "results" / "data").glob(pattern)
            if (p / filename).is_file()
        ]

        matched = next(
            (
                p / filename
                for p in sorted(matches)
                if digest(p / filename) == expected
            ),
            None,
        )

        parents[label] = {
            "path_relative_to_repo": (
                str(matched.relative_to(ROOT))
                if matched else None
            ),
            "sha256_expected": expected,
            "sha256_actual": (
                digest(matched) if matched else None
            ),
            "status": (
                "MATCH" if matched else "OPTIONAL_NOT_VERIFIED"
            ),
            "mandatory": False,
        }

    return parents


def connect_db() -> sqlite3.Connection:
    """Open GRAVITY2's own database; never open AGMINER's database."""
    OUTPUT.mkdir(
        parents=True,
        exist_ok=True,
        mode=0o700,
    )

    db = sqlite3.connect(
        OUTPUT / "gravity2.sqlite3",
        timeout=2,
    )

    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=2000")

    db.execute(
        """CREATE TABLE IF NOT EXISTS runs(
            run_id TEXT PRIMARY KEY,
            state TEXT NOT NULL,
            level TEXT NOT NULL,
            preset TEXT NOT NULL,
            start_utc TEXT NOT NULL,
            continuation_of TEXT,
            science_sha256 TEXT
        )"""
    )

    db.commit()
    return db


def db_set(db, manifest, state, science_sha=None):
    """Parent process is the sole SQLite writer."""
    db.execute(
        """INSERT INTO runs(
            run_id,state,level,preset,start_utc,
            continuation_of,science_sha256
        ) VALUES(?,?,?,?,?,?,?)
        ON CONFLICT(run_id) DO UPDATE SET
            state=excluded.state,
            science_sha256=excluded.science_sha256""",
        (
            manifest["run_id"],
            state,
            manifest["level"],
            manifest["preset"],
            manifest["created_utc"],
            manifest["continuation_of"],
            science_sha,
        ),
    )
    db.commit()


def run_id_path(run_id: str) -> Path:
    """Prevent path traversal through user-supplied run IDs."""
    if not RUN_RE.fullmatch(run_id):
        raise ValueError("invalid GRAVITY2 run ID")
    return RUNS / run_id


def worker_audit(output_file: Path, delay: float):
    """Private worker: only G00 and a declared G01 completeness HOLD."""
    if delay:
        time.sleep(delay)

    parents = parent_audit()

    good = all(
        v["status"] == "MATCH"
        for v in parents.values()
        if v["mandatory"]
    )

    status = (
        "PARENT_LOCKED_SOURCE_FILES_ONLY"
        if good else "PARENT_HOLD"
    )

    gates = {
        gate: "NOT_RUN"
        for gate in GATES
    }

    gates["G00_PARENT"] = (
        "PASS_SCOPED" if good else "UNDERDETERMINED"
    )

    if good:
        gates["G01_ACTION"] = "UNDERDETERMINED"

    problems = [
        k + ":" + v["status"]
        for k, v in parents.items()
        if v["mandatory"] and v["status"] != "MATCH"
    ]

    payload = {
        "worker_status": status,
        "parents": parents,
        "gates": gates,
        "historical_anchors": ANCHORS,
        "historical_anchors_provenance":
            "RECORDED_ONLY_NOT_RECOMPUTED",
        "candidate": {
            "id": "R3B-NULL",
            "is_negative_control": True,
            "source_action": "NOT_DERIVED",
            "source_currents": "PRESCRIBED_NOT_PHYSICALIZED",
            "outcome": "NEVER_A_PHYSICAL_SURVIVOR",
        },
        "missing_requirements": (
            [
                "complete covariant R3B source, Earth and supports action",
                "metric/Hodge and source/current/neutral variation",
                "fully reciprocal loaded source and Einstein response",
                "dynamical health, exterior convergence, Earth/craft force",
                "complete non-double-counted SI energy",
            ]
            if good else problems
        ),
        "science_claims": "NONE_NEW",
    }

    atomic_json(output_file, payload)

    print(
        "WORKER_G00=",
        gates["G00_PARENT"],
        flush=True,
    )


def rss_tree_mib(pid: int):
    """Get worker and child RSS using psutil, if installed."""
    try:
        import psutil
    except ImportError:
        return None

    try:
        p = psutil.Process(pid)
        descendants = [p] + p.children(recursive=True)

        return sum(
            x.memory_info().rss
            for x in descendants
            if x.is_running()
        ) / MIB

    except psutil.Error:
        return 0.0


def terminate_group(proc: subprocess.Popen):
    """Terminate only this miner's subprocess process group."""
    if proc.poll() is not None:
        return

    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return

    try:
        proc.wait(timeout=0.4)

    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

        proc.wait(timeout=1)


def supervise(
    proc,
    rdir: Path,
    seconds: float,
    mem_mib: int,
    disk_mib: int,
    started: float,
):
    """Watch time, memory, disk, user stop and bounded worker output."""
    assert proc.stdout is not None

    os.set_blocking(proc.stdout.fileno(), False)

    captured = bytearray()
    total_log_bytes = 0
    peak = 0.0

    monitor = (
        "PSUTIL_RSS_SOFT_LIMIT"
        if rss_tree_mib(proc.pid) is not None
        else "RSS_NOT_MONITORED_L0_ONLY"
    )

    reason = "COMPLETED"

    try:
        while True:
            try:
                chunk = os.read(
                    proc.stdout.fileno(),
                    16384,
                )

                total_log_bytes += len(chunk)

                if chunk and len(captured) < LOG_MAX_BYTES:
                    captured.extend(
                        chunk[:LOG_MAX_BYTES-len(captured)]
                    )

            except BlockingIOError:
                pass

            mem = rss_tree_mib(proc.pid)

            if mem is not None:
                peak = max(peak, mem)

                if mem > mem_mib:
                    reason = "MEMORY_LIMIT"
                    break

            if (rdir / "stop.request").exists():
                reason = "USER_STOP"
                break

            if bytes_under(rdir) > min(disk_mib, SCRATCH_MIB) * MIB:
                reason = "STORAGE_LIMIT"
                break

            if time.monotonic() - started >= seconds:
                reason = "TIME_BUDGET_EXCEEDED"
                break

            if proc.poll() is not None:
                break

            time.sleep(0.04)

    except KeyboardInterrupt:
        reason = "USER_INTERRUPT"

    finally:
        if reason != "COMPLETED":
            terminate_group(proc)

        try:
            proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            terminate_group(proc)

        try:
            while True:
                chunk = os.read(
                    proc.stdout.fileno(),
                    16384,
                )

                if not chunk:
                    break

                total_log_bytes += len(chunk)

                if len(captured) < LOG_MAX_BYTES:
                    captured.extend(
                        chunk[:LOG_MAX_BYTES-len(captured)]
                    )

        except (BlockingIOError, OSError):
            pass

        proc.stdout.close()

    atomic_text(
        rdir / "worker.log",
        captured.decode("utf-8", errors="replace"),
    )

    return (
        reason,
        peak,
        monitor,
        proc.returncode,
        len(captured),
        total_log_bytes > LOG_MAX_BYTES,
    )


def run_job(args, continuation_of=None):
    """Run one bounded infrastructure audit, never a physics solver."""

    if args.level != "L0":
        raise ValueError(
            "GRAVITY2-00 implements L0 only; L1-L4 are NOT authorized"
        )

    if args.workers != 1:
        raise ValueError(
            "GRAVITY2-00 permits exactly one worker"
        )

    cap, memory_mib, output_mib = PRESETS[args.preset]
    seconds = float(args.minutes) * 60

    if (
        not math.isfinite(seconds)
        or seconds <= 0
        or seconds > cap
    ):
        raise ValueError(
            "minutes must be positive and within preset cap"
        )

    if args.dry_run:
        print(
            json.dumps(
                {
                    "program": PROGRAM,
                    "execution": "DRY_RUN_NO_WRITES",
                    "level": args.level,
                    "preset": args.preset,
                    "seconds": seconds,
                    "worker": 1,
                    "memory_soft_mib": memory_mib,
                    "per_run_disk_mib": output_mib,
                    "legacy_AGMINER_writes": False,
                    "science": "G00 SOURCE FILE HASH AUDIT ONLY",
                },
                indent=2,
            )
        )
        return 0

    # Application-level global storage reserve.
    # No existing evidence is ever automatically deleted.
    if bytes_under(OUTPUT) > (GLOBAL_MIB-output_mib) * MIB:
        raise ValueError(
            "GRAVITY2 global storage reserve exhausted; no automatic pruning"
        )

    RUNS.mkdir(
        parents=True,
        exist_ok=True,
        mode=0o700,
    )

    name = (
        datetime.now(timezone.utc).strftime(
            "g2_%Y%m%dT%H%M%SZ_"
        )
        + secrets.token_hex(4)
    )

    rdir = run_id_path(name)
    rdir.mkdir(mode=0o700)

    manifest = {
        "schema": SCHEMA,
        "program": PROGRAM,
        "run_id": name,
        "created_utc": utc(),
        "level": args.level,
        "preset": args.preset,
        "requested_seconds": seconds,
        "workers": 1,
        "rss_soft_limit_mib": memory_mib,
        "disk_soft_limit_mib": output_mib,
        "global_disk_soft_limit_mib": GLOBAL_MIB,
        "continuation_of": continuation_of,
        "producer_sources_sha256": source_hashes(),
        "runtime_python": sys.version.split()[0],
        "regression": "NOT_RUN",
        "science_scope": "PROVENANCE_AND_NEGATIVE_CONTROL_ONLY",
        "legacy_miner_access":
            "READ_ONLY_SOURCE_SHA_NO_EXECUTION_OR_WRITES",
    }

    atomic_json(
        rdir / "manifest.json",
        manifest,
    )

    with connect_db() as db:
        db_set(db, manifest, "ACTIVE")

        print(f"GRAVITY2_RUN={name}", flush=True)
        print(
            f"BOUND={seconds:.1f}s "
            f"RSS_SOFT={memory_mib}MiB "
            f"DISK_SOFT={output_mib}MiB",
            flush=True,
        )

        worker_out = rdir / "_worker.json"

        env = dict(os.environ)
        env.update(
            {
                "PYTHONPATH": str(ROOT / "src"),
                "OPENBLAS_NUM_THREADS": "1",
                "OMP_NUM_THREADS": "1",
                "MKL_NUM_THREADS": "1",
                "VECLIB_MAXIMUM_THREADS": "1",
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )

        cmd = [
            sys.executable,
            "-m",
            "antigravity_research.gravity2",
            "_worker",
            "--output",
            str(worker_out),
            "--sleep-test",
            str(args.test_sleep),
        ]

        started = time.monotonic()

        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            env=env,
            cwd=ROOT,
        )

        (
            reason,
            peak,
            monitor,
            returncode,
            log_bytes,
            log_truncated,
        ) = supervise(
            proc,
            rdir,
            seconds,
            memory_mib,
            output_mib,
            started,
        )

        payload = None

        if (
            reason == "COMPLETED"
            and returncode == 0
            and worker_out.is_file()
        ):
            try:
                payload = json.loads(
                    worker_out.read_text()
                )
            except (ValueError, OSError):
                reason = "SOFTWARE_ERROR"

        elif reason == "COMPLETED":
            reason = "SOFTWARE_ERROR"

        worker_out.unlink(missing_ok=True)

        if not payload:
            payload = {
                "parents": {},
                "gates": {
                    x: "NOT_RUN"
                    for x in GATES
                },
                "missing_requirements": [reason],
                "science_claims": "NONE_NEW",
                "worker_status": "NO_RESULT",
            }

        science = {
            "schema": SCHEMA,
            "program": PROGRAM,
            "run_id": name,
            "execution_status": reason,
            "parent_audit_status": payload["worker_status"],
            "parents": payload["parents"],
            "gates": payload["gates"],
            "historical_anchors": payload.get(
                "historical_anchors",
                ANCHORS,
            ),
            "historical_anchors_provenance":
                "RECORDED_ONLY_NOT_RECOMPUTED",
            "candidate": payload.get(
                "candidate",
                {
                    "id": "R3B-NULL",
                    "status": "NOT_RUN",
                },
            ),
            "missing_requirements":
                payload["missing_requirements"],
            "physical_success": False,
            "full_regression": "NOT_RUN",
            "Einstein_source_to_metric_bridge": "NOT_DERIVED",
            "whole_craft_force": "NOT_DERIVED",
            "certified_complete_energy_j": None,
            "physical_research_percentage_promotion": "NONE",
            "resource": {
                "seconds_elapsed": round(
                    time.monotonic() - started,
                    6,
                ),
                "peak_worker_tree_rss_mib": (
                    round(peak, 3)
                    if monitor.startswith("PSUTIL")
                    else None
                ),
                "rss_monitoring": monitor,
                "worker_exit_code": returncode,
                "worker_log_bytes": log_bytes,
                "worker_log_truncated": log_truncated,
                "disk_soft_policy":
                    "APPLICATION_WATCHDOG_NOT_KERNEL_QUOTA",
            },
        }

        atomic_json(
            rdir / "science.json",
            science,
        )

        atomic_text(
            rdir / "hashes.sha256",
            digest(rdir / "manifest.json")
            + "  manifest.json\n"
            + digest(rdir / "science.json")
            + "  science.json\n",
        )

        size = bytes_under(rdir)

        db_set(
            db,
            manifest,
            reason,
            digest(rdir / "science.json"),
        )

        db.execute(
            "PRAGMA wal_checkpoint(TRUNCATE)"
        )

        if size > output_mib * MIB:
            print(
                "WARNING: per-run output cap exceeded; "
                "run retained, investigate",
                flush=True,
            )

        print("GRAVITY2_STATUS=", reason)
        print(
            "G00_PARENT=",
            science["gates"]["G00_PARENT"],
        )
        print(
            "G01_ACTION=",
            science["gates"]["G01_ACTION"],
        )
        print(
            "SOURCE_ACTION=NOT_DERIVED; PHYSICAL_SUCCESS=NO"
        )
        print("RUN_DIR=", rdir)
        print(
            "SCIENCE_SHA256=",
            digest(rdir / "science.json"),
        )

        return 0 if reason == "COMPLETED" else 3


def status_cmd(args):
    db = OUTPUT / "gravity2.sqlite3"

    if not db.is_file():
        print("NO_GRAVITY2_RUNS")
        return 0

    with sqlite3.connect(db) as con:
        for row in con.execute(
            "SELECT run_id,state,level,preset,science_sha256 "
            "FROM runs ORDER BY start_utc DESC LIMIT ?",
            (args.max,),
        ):
            print(" | ".join(str(v) for v in row))

    return 0


def stop_cmd(args):
    rdir = run_id_path(args.run_id)

    if (
        not rdir.is_dir()
        or (rdir / "science.json").exists()
    ):
        raise ValueError(
            "run missing or already sealed; no stop requested"
        )

    atomic_text(
        rdir / "stop.request",
        "GRAVITY2_STOP_REQUEST\n",
    )

    print("STOP_REQUESTED", args.run_id)
    return 0


def resume_cmd(args):
    old_dir = run_id_path(args.run_id)
    old = json.loads(
        (old_dir / "science.json").read_text()
    )

    if old["execution_status"] == "COMPLETED":
        raise ValueError(
            "cannot resume completed run: start a new run instead"
        )

    return run_job(
        args,
        continuation_of=args.run_id,
    )


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="gravity2",
        description=PROGRAM + " (GRAVITY2-00 infrastructure only)",
    )

    sp = p.add_subparsers(
        dest="command",
        required=True,
    )

    def budget_options(cmd):
        cmd.add_argument(
            "--level",
            choices=["L0", "L1", "L2", "L3", "L4"],
            default="L0",
        )
        cmd.add_argument(
            "--preset",
            choices=list(PRESETS),
            default="quick",
        )
        cmd.add_argument(
            "--minutes",
            type=float,
            default=1,
        )
        cmd.add_argument(
            "--workers",
            type=int,
            default=1,
        )
        cmd.add_argument(
            "--dry-run",
            action="store_true",
        )
        cmd.add_argument(
            "--test-sleep",
            type=float,
            default=0,
            help=argparse.SUPPRESS,
        )

    run = sp.add_parser(
        "run",
        help="safe L0 parent audit",
    )
    budget_options(run)

    resume = sp.add_parser(
        "resume",
        help="new immutable continuation after incomplete run",
    )
    resume.add_argument(
        "--run-id",
        required=True,
    )
    budget_options(resume)

    stop = sp.add_parser(
        "stop",
        help="request bounded worker stop",
    )
    stop.add_argument(
        "--run-id",
        required=True,
    )

    status = sp.add_parser(
        "status",
        help="list GRAVITY2 runs only",
    )
    status.add_argument(
        "--max",
        type=int,
        default=5,
    )

    verify = sp.add_parser(
        "verify",
        help="independently check immutable evidence",
    )
    verify.add_argument(
        "--run-id",
        required=True,
    )

    sp.add_parser(
        "list-candidates",
        help="show explicit source-action slots",
    )
    sp.add_parser(
        "top",
        help="physical survivor list (empty until demonstrated)",
    )

    failures = sp.add_parser(
        "failures",
        help="historical negative controls",
    )
    failures.add_argument(
        "--max",
        type=int,
        default=10,
    )

    worker = sp.add_parser(
        "_worker",
        help=argparse.SUPPRESS,
    )
    worker.add_argument(
        "--output",
        required=True,
    )
    worker.add_argument(
        "--sleep-test",
        type=float,
        default=0,
    )

    args = p.parse_args(argv)

    try:
        if args.command == "_worker":
            worker_audit(
                Path(args.output),
                args.sleep_test,
            )
            return 0

        if args.command == "run":
            return run_job(args)

        if args.command == "resume":
            return resume_cmd(args)

        if args.command == "stop":
            return stop_cmd(args)

        if args.command == "status":
            return status_cmd(args)

        if args.command == "verify":
            from .independent import verify_run
            return verify_run(
                run_id_path(args.run_id)
            )

        if args.command == "list-candidates":
            print(
                "R3B-NULL: prescribed-current negative control only"
            )
            print(
                "R3B-SRC-A/B: NOT INSTANTIATED; "
                "no invented source actions"
            )
            return 0

        if args.command == "top":
            print(
                "TOP_PHYSICAL_SURVIVORS=NONE (GRAVITY2-00)"
            )
            return 0

        if args.command == "failures":
            for i, item in enumerate(
                HISTORICAL_FAILURES[:max(0, args.max)],
                1,
            ):
                print(f"{i:02d}. {item}")
            return 0

    except (
        ValueError,
        OSError,
        sqlite3.Error,
        KeyError,
        FileExistsError,
    ) as exc:
        print(
            "GRAVITY2_HOLD:",
            type(exc).__name__,
            str(exc),
            file=sys.stderr,
        )
        return 2

    return 2
