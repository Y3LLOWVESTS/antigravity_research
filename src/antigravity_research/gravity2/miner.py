"""Bounded autonomous GRAVITY2 source-existence miner (operational L0/L1).

Standalone module so GRAVITY2-00/01/02/03A producer SHAs remain immutable.
It NEVER imports or executes historical AGMINER. Long L2-L4 solvers remain
hard-disabled until physically justified, separately implemented and verified.
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
import time
from datetime import datetime, timezone

from . import miner_cases as cases
from .engine import (
    ROOT, atomic_json, atomic_text, bytes_under, digest,
)
from .policy import PRESETS, GLOBAL_MIB

BASE = ROOT / "results/gravity2/miner_runs"
DBPATH = ROOT / "results/gravity2/miner.sqlite3"
ID_RE = re.compile(r"g2m_\d{8}T\d{6}Z_[0-9a-f]{8}\Z")
MIB = 1024 * 1024
SOURCE_FILES = ("miner_cases.py", "miner.py", "miner_verify.py")

PARENTS = {
    "G02_SCIENCE": (
        "results/gravity2/action02_runs/"
        "g202_20261121T042518Z_9a7f5402/science.json",
        "f87f925417b36f8a9b319eb4fb3c54547d9d13e1e106e9c26fcf7e997895fe61",
    ),
    "G02_VERIFY": (
        "results/gravity2/action02_runs/"
        "g202_20261121T042518Z_9a7f5402/verification.json",
        "b2c91f6be46c532154e5dec211af7bbd942c6c720ba0afd9fac1f184843e2b28",
    ),
    "G03A_SCIENCE": (
        "results/gravity2/bridge03a_runs/"
        "g203a_20261121T043515Z_4d15503e/science.json",
        "3ab38bcb8aad876fec46b76a713d8769aa345902f4f2c8ee0c4d1619b65227a6",
    ),
    "G03A_VERIFY": (
        "results/gravity2/bridge03a_runs/"
        "g203a_20261121T043515Z_4d15503e/verification.json",
        "261080c5be930767817179b34447d7cb989b89c603dc6b081f79d8a9732da89e",
    ),
}


def producer_hashes():
    p = Path(__file__).resolve().parent
    return {
        name: digest(p / name)
        for name in SOURCE_FILES
    }


def run_dir(rid):
    if not ID_RE.fullmatch(rid):
        raise ValueError("invalid GRAVITY2 miner run ID")
    return BASE / rid


def parent_locks():
    from .action01_core import read_pinned

    source_locks, _ = read_pinned(ROOT)
    parents = {}

    for name, (rel, expected) in PARENTS.items():
        p = ROOT / rel
        actual = (
            digest(p)
            if p.is_file() and not p.is_symlink()
            else None
        )

        parents[name] = {
            "path": rel,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "match": actual == expected,
        }

    locked = (
        all(p["match"] for p in parents.values())
        and all(
            v["status"] == "MATCH"
            for v in source_locks.values()
        )
    )

    return {
        "reports": parents,
        "historical_sources": source_locks,
        "all_match": locked,
    }


def connection():
    DBPATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    db = sqlite3.connect(DBPATH, timeout=2)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=2000")

    db.execute(
        "CREATE TABLE IF NOT EXISTS runs ("
        "run_id TEXT PRIMARY KEY, "
        "state TEXT NOT NULL, "
        "level TEXT NOT NULL, "
        "created TEXT NOT NULL, "
        "continuation_of TEXT, "
        "science_sha TEXT)"
    )

    db.execute(
        "CREATE TABLE IF NOT EXISTS gates ("
        "run_id TEXT NOT NULL, "
        "candidate TEXT NOT NULL, "
        "fingerprint TEXT NOT NULL, "
        "verdict TEXT NOT NULL, "
        "evidence_sha TEXT NOT NULL, "
        "PRIMARY KEY(run_id,candidate))"
    )

    db.execute(
        "CREATE TABLE IF NOT EXISTS failures ("
        "fingerprint TEXT PRIMARY KEY, "
        "theorem TEXT NOT NULL, "
        "evidence_run TEXT NOT NULL, "
        "evidence_sha TEXT NOT NULL)"
    )

    db.commit()
    return db


def set_run(db, m, state, sha=None):
    db.execute(
        "INSERT INTO runs("
        "run_id,state,level,created,continuation_of,science_sha"
        ") VALUES(?,?,?,?,?,?) "
        "ON CONFLICT(run_id) DO UPDATE SET "
        "state=excluded.state, "
        "science_sha=excluded.science_sha",
        (
            m["run_id"],
            state,
            m["level"],
            m["created_utc"],
            m["continuation_of"],
            sha,
        ),
    )
    db.commit()


def _rss(pid):
    try:
        import psutil
    except ImportError:
        return None

    try:
        root = psutil.Process(pid)
        return sum(
            p.memory_info().rss
            for p in [root] + root.children(recursive=True)
            if p.is_running()
        ) / MIB
    except psutil.Error:
        return 0.0


def _rss_available():
    try:
        import psutil
        return True
    except ImportError:
        return False


def _kill_group(p):
    if p.poll() is not None:
        return

    try:
        os.killpg(p.pid, signal.SIGTERM)
    except ProcessLookupError:
        return

    try:
        p.wait(timeout=0.35)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        p.wait(timeout=1)


def supervise(p, folder, deadline, ram_mib, disk_mib):
    """Soft watchdog that owns only its own child process group."""
    assert p.stdout

    os.set_blocking(p.stdout.fileno(), False)

    log = bytearray()
    truncated = False
    peak = 0.
    reason = "COMPLETED"

    try:
        while True:
            try:
                chunk = os.read(
                    p.stdout.fileno(), 8192
                )

                if len(log) + len(chunk) > 16384:
                    truncated = True

                log.extend(
                    chunk[:max(0, 16384-len(log))]
                )
            except BlockingIOError:
                pass

            mem = _rss(p.pid)

            if mem is not None:
                peak = max(peak, mem)
                if mem > ram_mib:
                    reason = "MEMORY_LIMIT"
                    break

            if (folder / "stop.request").exists():
                reason = "USER_STOP"
                break

            if bytes_under(folder) > min(disk_mib, 32)*MIB:
                reason = "STORAGE_LIMIT"
                break

            if time.monotonic() >= deadline:
                reason = "TIME_BUDGET_EXCEEDED"
                break

            if p.poll() is not None:
                break

            time.sleep(.03)

    except KeyboardInterrupt:
        reason = "USER_INTERRUPT"

    finally:
        if reason != "COMPLETED":
            _kill_group(p)

        try:
            p.wait(timeout=.5)
        except subprocess.TimeoutExpired:
            reason = "WORKER_UNRESPONSIVE"
            _kill_group(p)

        try:
            while True:
                b = os.read(
                    p.stdout.fileno(), 8192
                )

                if not b:
                    break

                if len(log) + len(b) > 16384:
                    truncated = True

                log.extend(
                    b[:max(0, 16384-len(log))]
                )
        except (OSError, BlockingIOError):
            pass

        p.stdout.close()

    return (
        reason,
        p.returncode,
        round(peak, 3) if _rss_available() else None,
        log.decode("utf-8", "replace"),
        truncated,
    )


def _run_worker(
    candidate, level, folder,
    deadline, ram_mib, disk_mib, sleep=0,
):
    target = folder / ("_" + candidate + ".json")

    env = dict(os.environ)
    env.update({
        "PYTHONPATH": str(ROOT / "src"),
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
            "antigravity_research.gravity2.miner",
            "_worker",
            "--candidate", candidate,
            "--level", level,
            "--output", str(target),
            "--test-sleep", str(sleep),
        ],
        cwd=ROOT,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )

    reason, code, peak, output, trunc = supervise(
        p, folder, deadline, ram_mib, disk_mib
    )

    result = None

    if (
        reason == "COMPLETED"
        and code == 0
        and target.is_file()
    ):
        try:
            result = json.loads(target.read_text())
        except (OSError, ValueError):
            reason = "WORKER_BAD_JSON"
    elif reason == "COMPLETED":
        reason = "WORKER_ERROR"

    target.unlink(missing_ok=True)

    return (
        reason,
        result,
        {
            "exit_code": code,
            "rss_peak_mib": peak,
            "log_truncated": trunc,
            "log_tail": output[-1024:],
        },
    )


def _source_reference(db, fingerprint, parent_digest):
    row = db.execute(
        "SELECT theorem,evidence_run,evidence_sha "
        "FROM failures WHERE fingerprint=?",
        (fingerprint,),
    ).fetchone()

    if not row:
        return None

    theorem, rid, sha = row

    old = (
        run_dir(rid)
        / "cases"
        / "C1_STATIC_NO_A0.json"
    )

    if not old.is_file() or digest(old) != sha:
        return None

    old_manifest = run_dir(rid) / "manifest.json"

    if (
        not old_manifest.is_file()
        or json.loads(old_manifest.read_text()).get(
            "producer_sha256"
        ) != producer_hashes()
    ):
        return None

    item = json.loads(old.read_text())

    if (
        item.get("parent_fingerprint") != parent_digest
        or item.get("gate_G05", {}).get("theorem") != theorem
    ):
        return None

    return {
        "from_run": rid,
        "sha256": sha,
        "theorem": theorem,
        "relative_path": str(old.relative_to(ROOT)),
    }


def _resume_refs(previous, manifest, fresh):
    if previous is None or fresh:
        return {}

    old_dir = run_dir(previous)

    old_man = json.loads(
        (old_dir / "manifest.json").read_text()
    )

    if (
        old_man["producer_sha256"]
            != manifest["producer_sha256"]
        or old_man["parent_fingerprint"]
            != manifest["parent_fingerprint"]
        or old_man["level"] != manifest["level"]
    ):
        raise ValueError(
            "resume requires identical source/action/"
            "level/parent fingerprints"
        )

    refs = {}

    for entry in (old_dir / "cases").glob("*.json"):
        value = json.loads(entry.read_text())

        if (
            value.get("candidate_id")
                in {c["id"] for c in cases.registry()}
            and value.get("parent_fingerprint")
                == manifest["parent_fingerprint"]
        ):
            refs[value["candidate_id"]] = {
                "relative_path": str(
                    entry.relative_to(ROOT)
                ),
                "sha256": digest(entry),
                "from_run": previous,
            }

    return refs


def run(args, previous=None):
    if args.level not in ("L0", "L1") or args.workers != 1:
        raise ValueError(
            "L2-L4 not implemented or authorized; "
            "L0/L1 and 1 worker only"
        )

    cap, ram, disk = PRESETS[args.preset]
    seconds = args.minutes * 60

    if not math.isfinite(seconds) or not 0 < seconds <= cap:
        raise ValueError(
            "minutes must fit the named time preset"
        )

    if args.dry_run:
        print(json.dumps({
            "run": "GRAVITY2-AUTONOMOUS",
            "level": args.level,
            "preset": args.preset,
            "seconds": seconds,
            "workers": 1,
            "candidates": [
                c["id"] for c in cases.registry()
            ],
            "science": "RESTRICTED_SOURCE_THEOREMS_ONLY",
            "L2_L4": "DISABLED",
            "writes": "NONE",
        }, indent=2))
        return 0

    if args.level == "L1" and not _rss_available():
        raise ValueError(
            "L1 requires psutil for soft RSS watchdog"
        )

    if sum(
        p.stat().st_size
        for p in (
            DBPATH,
            Path(str(DBPATH)+"-wal"),
            Path(str(DBPATH)+"-shm"),
        )
        if p.exists()
    ) > 64*MIB:
        raise ValueError(
            "miner SQLite storage exceeds 64 MiB; "
            "preserve old evidence"
        )

    if bytes_under(
        ROOT / "results/gravity2"
    ) > (GLOBAL_MIB-disk)*MIB:
        raise ValueError(
            "GRAVITY2 global storage reserve exceeded; "
            "no automatic deletion"
        )

    locks = parent_locks()

    parent_fp = hashlib.sha256(
        json.dumps(locks, sort_keys=True).encode()
    ).hexdigest()

    rid = (
        datetime.now(timezone.utc).strftime(
            "g2m_%Y%m%dT%H%M%SZ_"
        )
        + secrets.token_hex(4)
    )

    folder = run_dir(rid)
    (folder / "cases").mkdir(
        parents=True,
        mode=0o700,
    )

    manifest = {
        "program": "GRAVITY2_AUTONOMOUS_V1",
        "schema": cases.SCHEMA,
        "run_id": rid,
        "level": args.level,
        "preset": args.preset,
        "max_seconds": seconds,
        "workers": 1,
        "memory_soft_mib": ram,
        "disk_soft_mib": disk,
        "created_utc":
            datetime.now(timezone.utc).isoformat(),
        "producer_sha256": producer_hashes(),
        "parent_fingerprint": parent_fp,
        "continuation_of": previous,
        "algorithm": "DETERMINISTIC_THEOREM_FIRST",
        "scope":
            "ONLY_EXPLICIT_R3B_SOURCE_ACTION_ANSATZE; NO_L2_L4",
    }

    atomic_json(
        folder / "manifest.json",
        manifest,
    )

    db = connection()
    set_run(db, manifest, "ACTIVE")

    deadline = time.monotonic() + seconds
    entries = []
    state = (
        "COMPLETED"
        if locks["all_match"]
        else "PARENT_HOLD"
    )

    print("GRAVITY2_MINER_RUN=" + rid, flush=True)
    print(
        "PARENTS="
        + ("LOCKED" if locks["all_match"] else "HOLD"),
        flush=True,
    )

    try:
        prior_refs = _resume_refs(
            previous, manifest, args.fresh
        )

        if state == "COMPLETED":
            for card in cases.registry():
                cid = card["id"]

                if (folder / "stop.request").exists():
                    state = "USER_STOP"
                    break

                if time.monotonic() >= deadline:
                    state = "TIME_BUDGET_EXCEEDED"
                    break

                if bytes_under(
                    ROOT / "results/gravity2"
                ) > (GLOBAL_MIB-disk)*MIB:
                    state = "STORAGE_LIMIT"
                    break

                if cid in prior_refs:
                    # Immutable continuation, not an overwrite.
                    entry = {
                        "candidate_id": cid,
                        "fingerprint": card["fingerprint"],
                        "status": "RESUMED_PREVIOUS_EVIDENCE",
                        "evidence_ref": prior_refs[cid],
                    }

                else:
                    reuse = (
                        None
                        if args.fresh or cid != "C1_STATIC_NO_A0"
                        else _source_reference(
                            db,
                            card["fingerprint"],
                            parent_fp,
                        )
                    )

                    if reuse:
                        entry = {
                            "candidate_id": cid,
                            "fingerprint": card["fingerprint"],
                            "status": "CACHED_SCOPED_FAILURE",
                            "evidence_ref": reuse,
                        }

                    else:
                        reason, result, metrics = _run_worker(
                            cid, args.level, folder,
                            deadline, ram, disk,
                            args.test_sleep,
                        )

                        if reason != "COMPLETED" or result is None:
                            state = reason
                            print(
                                "STOP=" + state
                                + " candidate=" + cid,
                                flush=True,
                            )
                            break

                        if (
                            result.get("candidate_id") != cid
                            or result.get("fingerprint")
                                != card["fingerprint"]
                        ):
                            state = "WORKER_EVIDENCE_MISMATCH"
                            break

                        result["parent_fingerprint"] = parent_fp

                        path = (
                            folder / "cases" / (cid + ".json")
                        )

                        atomic_json(path, result)
                        sha = digest(path)

                        entry = {
                            "candidate_id": cid,
                            "fingerprint": card["fingerprint"],
                            "status":
                                result["gate_G05"]["verdict"],
                            "gate":
                                result["gate_G05"]["theorem"],
                            "evidence_ref": {
                                "relative_path":
                                    str(path.relative_to(ROOT)),
                                "sha256": sha,
                                "from_run": rid,
                            },
                            "worker": metrics,
                        }

                        db.execute(
                            "INSERT OR IGNORE INTO gates("
                            "run_id,candidate,fingerprint,verdict,evidence_sha"
                            ") VALUES(?,?,?,?,?)",
                            (
                                rid, cid, card["fingerprint"],
                                entry["status"], sha,
                            ),
                        )

                        if (
                            cid == "C1_STATIC_NO_A0"
                            and entry["status"] == "FAIL_SCOPED"
                        ):
                            db.execute(
                                "INSERT INTO failures("
                                "fingerprint,theorem,evidence_run,evidence_sha"
                                ") VALUES(?,?,?,?) "
                                "ON CONFLICT(fingerprint) DO UPDATE SET "
                                "theorem=excluded.theorem, "
                                "evidence_run=excluded.evidence_run, "
                                "evidence_sha=excluded.evidence_sha",
                                (
                                    card["fingerprint"],
                                    entry["gate"],
                                    rid, sha,
                                ),
                            )

                        db.commit()

                entries.append(entry)

                print(
                    cid + ":" + entry["status"],
                    flush=True,
                )

    except KeyboardInterrupt:
        state = "USER_INTERRUPT"

    finally:
        science = {
            "program": "GRAVITY2_AUTONOMOUS_V1",
            "schema": cases.SCHEMA,
            "run_id": rid,
            "execution_status": state,
            "parent_locks": locks,
            "candidate_action": cases.ACTION,
            "candidate_registry": cases.registry(),
            "processed": entries,
            "pending": [
                c["id"]
                for c in cases.registry()
                if c["id"] not in {
                    e["candidate_id"] for e in entries
                }
            ],
            "physical_survivors": [],
            "physical_lift": "NOT_DERIVED",
            "real_finite_supported_source": "NOT_ESTABLISHED",
            "complete_covariant_action": "NOT_DERIVED",
            "Einstein_exterior_force": "NOT_DERIVED",
            "complete_energy_SI": "NOT_CERTIFIED",
            "006D_replaced": False,
            "full_regression": "NOT_RUN",
            "high_level_solvers":
                "DISABLED_UNTIL_INDEPENDENT_SOURCE_ACTION",
            "science_limit": (
                "Theorems are scoped to stated source ansatz; "
                "L1 stationary bound is only necessary."
            ),
        }

        atomic_json(
            folder / "science.json", science
        )

        atomic_text(
            folder / "hashes.sha256",
            digest(folder / "manifest.json")
            + "  manifest.json\n"
            + digest(folder / "science.json")
            + "  science.json\n",
        )

        set_run(
            db, manifest, state,
            digest(folder / "science.json"),
        )

        db.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        db.close()

    print("EXECUTION=" + state)
    print(
        "PROCESSED="
        + str(len(entries))
        + "/"
        + str(len(cases.REGISTRY))
    )
    print(
        "PHYSICAL_SURVIVORS=0; COMPLETE_ACTION=NOT_DERIVED"
    )
    print(
        "SCIENCE_SHA256="
        + digest(folder / "science.json")
    )

    return 0 if state == "COMPLETED" else 3


def cli(argv=None):
    p = argparse.ArgumentParser(
        prog="gravity2.miner",
        description=(
            "Self-contained R3B bounded source-action "
            "mining and failure memory"
        ),
    )

    subs = p.add_subparsers(
        dest="cmd",
        required=True,
    )

    def budget(cmd):
        cmd.add_argument(
            "--level",
            choices=("L0", "L1", "L2", "L3", "L4"),
            default="L1",
        )
        cmd.add_argument(
            "--preset",
            choices=tuple(PRESETS),
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
            "--fresh",
            action="store_true",
            help="do not reuse scoped theorem evidence",
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

    budget(subs.add_parser("run"))

    r = subs.add_parser("resume")
    r.add_argument("--run-id", required=True)
    budget(r)

    for sub in ("verify", "stop", "report"):
        subs.add_parser(sub).add_argument(
            "--run-id", required=True
        )

    subs.add_parser("status")
    subs.add_parser("failures")
    subs.add_parser("top")
    subs.add_parser("candidates")

    w = subs.add_parser("_worker")
    w.add_argument("--candidate", required=True)
    w.add_argument("--level", required=True)
    w.add_argument("--output", required=True)
    w.add_argument("--test-sleep", type=float, default=0)

    args = p.parse_args(argv)

    try:
        if args.cmd == "run":
            return run(args)

        if args.cmd == "resume":
            old = run_dir(args.run_id)
            sci = json.loads(
                (old / "science.json").read_text()
            )

            if sci["execution_status"] == "COMPLETED":
                raise ValueError(
                    "completed run cannot be resumed"
                )

            return run(args, previous=args.run_id)

        if args.cmd == "_worker":
            dest = Path(args.output)

            if (
                dest.name != "_" + args.candidate + ".json"
                or not ID_RE.fullmatch(dest.parent.name)
                or dest.parent.parent.resolve() != BASE.resolve()
            ):
                raise ValueError(
                    "worker target outside owned run"
                )

            if (
                args.test_sleep < 0
                or not math.isfinite(args.test_sleep)
            ):
                raise ValueError("invalid worker delay")

            if args.test_sleep:
                time.sleep(args.test_sleep)

            atomic_json(
                dest,
                cases.evaluate(args.candidate, args.level),
            )
            return 0

        if args.cmd == "verify":
            from .miner_verify import verify
            return verify(run_dir(args.run_id))

        if args.cmd == "stop":
            folder = run_dir(args.run_id)

            if (
                not folder.is_dir()
                or (folder / "science.json").exists()
            ):
                raise ValueError(
                    "run not active or already sealed"
                )

            atomic_text(
                folder / "stop.request",
                "STOP_REQUESTED\n",
            )

            print("STOP_REQUESTED=" + args.run_id)
            return 0

        if args.cmd == "report":
            sci = json.loads(
                (
                    run_dir(args.run_id) / "science.json"
                ).read_text()
            )

            print(json.dumps({
                k: sci[k]
                for k in (
                    "run_id",
                    "execution_status",
                    "processed",
                    "pending",
                    "real_finite_supported_source",
                    "complete_covariant_action",
                    "physical_lift",
                    "complete_energy_SI",
                )
            }, indent=2))
            return 0

        if args.cmd == "candidates":
            for c in cases.registry():
                print(
                    c["id"],
                    "|",
                    c["family"],
                    "|",
                    c["fingerprint"][:12],
                )
            return 0

        if args.cmd == "top":
            print(
                "QUALIFIED_PHYSICAL_SURVIVORS=0; "
                "NO_REAL_FINITE_SOURCE"
            )
            return 0

        if args.cmd in ("status", "failures"):
            if not DBPATH.exists():
                print("NO_MINER_HISTORY")
                return 0

            db = sqlite3.connect(
                f"file:{DBPATH}?mode=ro",
                uri=True,
            )

            sql = (
                "SELECT run_id,state,level,science_sha "
                "FROM runs ORDER BY created DESC LIMIT 12"
                if args.cmd == "status"
                else
                "SELECT theorem,evidence_run,evidence_sha "
                "FROM failures ORDER BY theorem LIMIT 12"
            )

            for row in db.execute(sql):
                print(" | ".join(map(str, row)))

            db.close()
            return 0

    except (
        OSError,
        ValueError,
        KeyError,
        sqlite3.Error,
        AssertionError,
    ) as exc:
        print(
            "GRAVITY2_MINER_HOLD=" + repr(exc),
            file=sys.stderr,
        )
        return 2

    return 2


if __name__ == "__main__":
    raise SystemExit(cli())
