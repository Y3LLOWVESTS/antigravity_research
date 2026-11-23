"""GRAVITY2-04 generated action atlas with bounded autonomous L1 gates.

No finite source, Einstein solution or loaded solver is claimed.
Legacy modules and previous GRAVITY2 checkpoints remain untouched.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
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
    ROOT, atomic_json, atomic_text, bytes_under, digest,
)
from .policy import PRESETS, GLOBAL_MIB
from . import miner2_math as physics
from . import miner as oldminer


BASE = ROOT/"results/gravity2/miner2_runs"
ID_RE = re.compile(
    r"g2v2_\d{8}T\d{6}Z_[a-f0-9]{8}\Z"
)
SOURCES = (
    "miner2_math.py",
    "miner2.py",
    "miner2_check.py",
)
MIB = 1024*1024

PARENTS = {
    "G03A_SCIENCE": (
        "results/gravity2/bridge03a_runs/"
        "g203a_20261121T043515Z_4d15503e/science.json",
        "3ab38bcb8aad876fec46b76a713d8769aa345902f4f2c8ee0c4d1619b65227a6",
    ),
    "G03A_VERIFICATION": (
        "results/gravity2/bridge03a_runs/"
        "g203a_20261121T043515Z_4d15503e/verification.json",
        "261080c5be930767817179b34447d7cb989b89c603dc6b081f79d8a9732da89e",
    ),
    "G2M1_SCIENCE": (
        "results/gravity2/miner_runs/"
        "g2m_20261121T044838Z_1457cdfc/science.json",
        "1376376ddabafce1e987d8f462eacca42ea4392931e6efedfc9fbc60743b6af1",
    ),
    "G2M1_VERIFICATION": (
        "results/gravity2/miner_runs/"
        "g2m_20261121T044838Z_1457cdfc/verification.json",
        "5901c074d21bae364c1295886aa3272bf56cb8cc0b2ad01e91e1d5b731317004",
    ),
}


def run_dir(run_id):
    if not ID_RE.fullmatch(run_id):
        raise ValueError("invalid GRAVITY2-04 run ID")
    return BASE/run_id


def code_hashes():
    pkg = Path(__file__).resolve().parent
    return {
        name: digest(pkg/name)
        for name in SOURCES
    }


def locks():
    return {
        name: {
            "path": rel,
            "expected_sha256": sha,
            "actual_sha256":
                digest(ROOT/rel)
                if (ROOT/rel).is_file()
                else None,
        }
        for name, (rel,sha) in PARENTS.items()
    }


def lock_pass(p):
    return all(
        x["expected_sha256"] == x["actual_sha256"]
        for x in p.values()
    )


def parent_digest(p):
    return hashlib.sha256(
        json.dumps(p,sort_keys=True).encode()
    ).hexdigest()


def reusable(card, pfinger, code):
    """Reuse only sealed, independently verified matching evidence."""
    if not BASE.is_dir():
        return None

    for folder in sorted(
        BASE.glob("g2v2_*"),
        reverse=True,
    ):
        if not ID_RE.fullmatch(folder.name):
            continue

        try:
            man = json.loads(
                (folder/"manifest.json").read_text()
            )
            sc = json.loads(
                (folder/"science.json").read_text()
            )
            verified = json.loads(
                (folder/"verification.json").read_text()
            )

            if (
                man["code_sha256"] != code
                or man["parent_fingerprint"] != pfinger
                or sc["execution_status"] != "COMPLETED"
                or verified["status"]
                    != "PASS_SCOPED_ACTION_GENERATION_ONLY"
                or verified["science_sha256"]
                    != digest(folder/"science.json")
            ):
                continue

            item = folder/"cases"/(card["id"]+".json")

            if item.is_file():
                data = json.loads(item.read_text())

                if (
                    data["fingerprint"]
                        == card["fingerprint"]
                    and data["parent_fingerprint"] == pfinger
                ):
                    return {
                        "relative_path":
                            str(item.relative_to(ROOT)),
                        "sha256": digest(item),
                        "from_run": folder.name,
                    }

        except (OSError,ValueError,KeyError):
            continue

    return None


def worker(cid,out):
    cards = {
        x["id"]:x
        for x in physics.registry()
    }

    if (
        cid not in cards
        or not ID_RE.fullmatch(out.parent.name)
    ):
        raise ValueError("unrecognized candidate or run")

    if (
        out.name != "_"+cid+".json"
        or out.parent.parent.resolve()
            != BASE.resolve()
    ):
        raise ValueError(
            "worker destination outside owned run"
        )

    atomic_json(
        out,
        physics.evaluate(cards[cid]),
    )


def run(args,continuation=None):
    if args.level != "L1" or args.workers != 1:
        raise ValueError(
            "GRAVITY2-04 supports L1 one worker only; "
            "L2-L4 locked"
        )

    sec = args.minutes*60
    cap,ram,disk = PRESETS[args.preset]

    if not math.isfinite(sec) or not 0 < sec <= cap:
        raise ValueError(
            "requested runtime outside preset limit"
        )

    cards = physics.registry()

    if args.dry_run:
        print(json.dumps({
            "level": "L1",
            "seconds_cap": sec,
            "workers": 1,
            "generated_actions": [
                x["id"] for x in cards
            ],
            "L2_L4": "NOT_AUTHORIZED",
            "writes": "NONE",
        },indent=2))
        return 0

    if not oldminer._rss_available():
        raise ValueError(
            "L1 requires psutil resource monitor"
        )

    if bytes_under(
        ROOT/"results/gravity2"
    ) > (GLOBAL_MIB-disk)*MIB:
        raise ValueError(
            "global GRAVITY2 storage reserve exhausted"
        )

    p = locks()
    pf = parent_digest(p)
    code = code_hashes()
    old = None

    if continuation:
        old = run_dir(continuation)
        previous = json.loads(
            (old/"science.json").read_text()
        )
        former = json.loads(
            (old/"manifest.json").read_text()
        )

        if previous["execution_status"] == "COMPLETED":
            raise ValueError(
                "complete runs cannot be resumed"
            )

        if (
            former["parent_fingerprint"] != pf
            or former["code_sha256"] != code
        ):
            raise ValueError(
                "resume parent/code drift"
            )

    rid = (
        datetime.now(timezone.utc).strftime(
            "g2v2_%Y%m%dT%H%M%SZ_"
        )
        +secrets.token_hex(4)
    )

    folder = run_dir(rid)
    (folder/"cases").mkdir(
        parents=True,
        mode=0o700,
    )

    manifest = {
        "program":
            "GRAVITY2-04_GENERATED_SOURCE_FRAMES",
        "run_id": rid,
        "created_utc":
            datetime.now(timezone.utc).isoformat(),
        "level": "L1",
        "preset": args.preset,
        "max_seconds": sec,
        "workers": 1,
        "memory_soft_mib": ram,
        "disk_soft_mib": disk,
        "code_sha256": code,
        "parent_fingerprint": pf,
        "continuation_of": continuation,
        "old_AGMINER":
            "READ_ONLY_NO_EXECUTION",
        "previous_GRAVITY2_producers":
            "NOT_MODIFIED",
    }

    atomic_json(
        folder/"manifest.json",
        manifest,
    )

    state = (
        "COMPLETED"
        if lock_pass(p)
        else "PARENT_HOLD"
    )

    entries = []
    deadline = time.monotonic()+sec

    print("GRAVITY2_04_RUN="+rid,flush=True)
    print(
        "PARENTS="
        +("LOCKED" if lock_pass(p) else "HOLD"),
        flush=True,
    )

    try:
        if state == "COMPLETED":
            for card in cards:
                cid = card["id"]

                if time.monotonic() >= deadline:
                    state = "TIME_BUDGET_EXCEEDED"
                    break

                if (folder/"stop.request").exists():
                    state = "USER_STOP"
                    break

                if bytes_under(
                    ROOT/"results/gravity2"
                ) > (GLOBAL_MIB-disk)*MIB:
                    state = "STORAGE_LIMIT"
                    break

                ref = None

                if not args.fresh and old:
                    f = old/"cases"/(cid+".json")

                    if f.is_file():
                        obj = json.loads(f.read_text())

                        if (
                            obj["fingerprint"]
                                == card["fingerprint"]
                            and obj.get(
                                "parent_fingerprint"
                            ) == pf
                        ):
                            ref = {
                                "relative_path":
                                    str(f.relative_to(ROOT)),
                                "sha256": digest(f),
                                "from_run": old.name,
                            }

                if not args.fresh and ref is None:
                    ref = reusable(card,pf,code)

                if ref is not None:
                    status = "REUSED_VERIFIED_EVIDENCE"

                else:
                    tmp = folder/("_"+cid+".json")
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
                            "antigravity_research.gravity2.miner2",
                            "_worker",
                            "--candidate",
                            cid,
                            "--output",
                            str(tmp),
                        ],
                        cwd=ROOT,
                        env=env,
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        start_new_session=True,
                    )

                    reason,exitcode,peak,output,trunc = (
                        oldminer.supervise(
                            child,folder,deadline,ram,disk
                        )
                    )

                    if (
                        reason != "COMPLETED"
                        or exitcode != 0
                        or not tmp.is_file()
                    ):
                        state = (
                            reason
                            if reason != "COMPLETED"
                            else "WORKER_ERROR"
                        )

                        atomic_text(
                            folder/(
                                "worker_error_"+cid+".log"
                            ),
                            output[-2048:],
                        )
                        break

                    result = json.loads(
                        tmp.read_text()
                    )
                    tmp.unlink(missing_ok=True)

                    if (
                        result["fingerprint"]
                            != card["fingerprint"]
                        or result["id"] != cid
                    ):
                        state = "WORKER_EVIDENCE_MISMATCH"
                        break

                    result["parent_fingerprint"] = pf

                    target = (
                        folder/"cases"/(cid+".json")
                    )

                    atomic_json(target,result)

                    ref = {
                        "relative_path":
                            str(target.relative_to(ROOT)),
                        "sha256": digest(target),
                        "from_run": rid,
                    }

                    status = result["decision"]

                entries.append({
                    "candidate_id": cid,
                    "fingerprint":
                        card["fingerprint"],
                    "status": status,
                    "evidence_ref": ref,
                })

                print(
                    cid+":"+status,
                    flush=True,
                )

    except KeyboardInterrupt:
        state = "USER_INTERRUPT"

    finally:
        science = {
            "program":
                "GRAVITY2-04_GENERATED_SOURCE_FRAMES",
            "run_id": rid,
            "execution_status": state,
            "parent_locks": p,
            "generated_actions": cards,
            "historical_exclusions":
                list(physics.HISTORICAL_EXCLUSIONS),
            "processed": entries,
            "pending": [
                x["id"]
                for x in cards
                if x["id"] not in {
                    a["candidate_id"]
                    for a in entries
                }
            ],
            "physical_survivors": [],
            "finite_stable_source":
                "NOT_ESTABLISHED",
            "complete_action": "NOT_DERIVED",
            "whole_craft_lift": "NOT_DERIVED",
            "complete_energy": "NOT_CERTIFIED",
            "006D_replaced": False,
            "full_regression": "NOT_RUN",
            "loaded_PDE": "NOT_AUTHORIZED",
            "scientific_scope":
                "EXACT_CHARGED_SOURCE_FRAME_AND_"
                "EXTERIOR_VEV_PREFLIGHT_ONLY",
        }

        atomic_json(
            folder/"science.json",
            science,
        )

        atomic_text(
            folder/"hashes.sha256",
            digest(folder/"manifest.json")
            +"  manifest.json\n"
            +digest(folder/"science.json")
            +"  science.json\n",
        )

    print("EXECUTION="+state)
    print(
        "PROCESSED="
        +str(len(entries))
        +"/"+str(len(cards))
    )
    print(
        "PHYSICAL_SURVIVORS=0; FULL_ACTION=NOT_DERIVED"
    )
    print(
        "SCIENCE_SHA256="
        +digest(folder/"science.json")
    )

    return 0 if state == "COMPLETED" else 3


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="gravity2.miner2"
    )

    subs = parser.add_subparsers(
        dest="cmd",
        required=True,
    )

    for name in ("run","resume"):
        r = subs.add_parser(name)

        if name == "resume":
            r.add_argument(
                "--run-id",
                required=True,
            )

        r.add_argument(
            "--level",
            choices=("L0","L1","L2","L3","L4"),
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
            default=1,
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
        r.add_argument(
            "--fresh",
            action="store_true",
        )

    for name in ("verify","report","stop"):
        subs.add_parser(name).add_argument(
            "--run-id",
            required=True,
        )

    subs.add_parser("candidates")
    subs.add_parser("status")
    subs.add_parser("top")

    w = subs.add_parser("_worker")
    w.add_argument(
        "--candidate",
        required=True,
    )
    w.add_argument(
        "--output",
        required=True,
    )

    a = parser.parse_args(argv)

    try:
        if a.cmd == "run":
            return run(a)

        if a.cmd == "resume":
            return run(
                a,
                continuation=a.run_id,
            )

        if a.cmd == "_worker":
            worker(
                a.candidate,
                Path(a.output),
            )
            return 0

        if a.cmd == "verify":
            from .miner2_check import verify
            return verify(run_dir(a.run_id))

        if a.cmd == "report":
            sc = json.loads(
                (
                    run_dir(a.run_id)
                    /"science.json"
                ).read_text()
            )

            print(
                "EXECUTION=",
                sc["execution_status"],
            )

            for x in sc["processed"]:
                print(
                    "CANDIDATE=",
                    x["candidate_id"],
                    "STATUS=",
                    x["status"],
                )

            print(
                "UNRESOLVED=FINITE_SUPPORTED_SOURCE, "
                "EINSTEIN, LOADING, ENERGY, REACTION"
            )
            return 0

        if a.cmd == "stop":
            folder = run_dir(a.run_id)

            if (
                not folder.is_dir()
                or (folder/"science.json").exists()
            ):
                raise ValueError(
                    "only active unsealed runs can be stopped"
                )

            atomic_text(
                folder/"stop.request",
                "STOP_REQUESTED\n",
            )
            return 0

        if a.cmd == "candidates":
            for c in physics.registry():
                print(
                    c["id"],
                    c["family"],
                    c["fingerprint"][:16],
                )
            return 0

        if a.cmd == "top":
            print(
                "PHYSICAL_SURVIVORS=0; "
                "NO_SOURCED_LIFT"
            )
            return 0

        if a.cmd == "status":
            if BASE.is_dir():
                for folder in sorted(
                    BASE.iterdir(),
                    reverse=True,
                )[:12]:
                    if (
                        ID_RE.fullmatch(folder.name)
                        and (
                            folder/"science.json"
                        ).is_file()
                    ):
                        sc = json.loads(
                            (
                                folder/"science.json"
                            ).read_text()
                        )

                        print(
                            folder.name,
                            sc["execution_status"],
                            len(sc["processed"]),
                        )
            return 0

    except (
        OSError,ValueError,KeyError,AssertionError
    ) as exc:
        print(
            "GRAVITY2_04_HOLD="+repr(exc),
            file=sys.stderr,
        )
        return 2

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
