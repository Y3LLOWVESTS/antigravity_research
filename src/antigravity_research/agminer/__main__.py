"""AGMINER command-line interface."""

from __future__ import annotations

import argparse
from pathlib import Path

from .pareto import pareto_frontier
from .policy import current_energy_policy
from .readonly import failure_counts
from .readonly import status_snapshot
from .readonly import survivor_rows
from .readonly import top_rows
from .storage import Storage


DEFAULT_DB = Path("results/agminer/agminer.sqlite3")


def command_policy() -> None:
    policy = current_energy_policy()

    print("AGMINER ENERGY POLICY")
    print("policy_id=" + str(policy["policy_id"]))
    print("value=" + str(policy["value"]))
    print("unit=" + str(policy["unit"]))
    print("comparison=" + str(policy["comparison"]))
    print("target_j=" + str(policy["limit_j_text"]))
    print("ledger=" + str(policy["ledger"]))


def command_status(path: Path) -> None:
    if not path.exists():
        print("AGMINER_DATABASE_MISSING=" + str(path))
        return

    snapshot = status_snapshot(path)

    print("AGMINER STATUS")
    print("database=" + str(path))
    print("models=" + str(snapshot["models"]))
    print("rejections=" + str(snapshot["rejections"]))
    print("region_rules=" + str(snapshot["region_rules"]))
    print("survivors=" + str(snapshot["survivors"]))
    print("stop_requested=" + str(snapshot["stop_requested"]))
    print("database_bytes=" + str(path.stat().st_size))
    print("inspection_mode=READ_ONLY")


def command_failures(path: Path) -> None:
    if not path.exists():
        print("AGMINER_DATABASE_MISSING=" + str(path))
        return

    rows = failure_counts(path)

    print("AGMINER FAILURES")
    print("inspection_mode=READ_ONLY")

    if not rows:
        print("NONE")
        return

    for row in rows:
        print(
            str(row["failure_code"])
            + " gate="
            + str(row["gate"])
            + " count="
            + str(row["count"])
        )


def command_top(path: Path, limit: int) -> None:
    if not path.exists():
        print("AGMINER_DATABASE_MISSING=" + str(path))
        return

    rows = top_rows(path, limit)

    print("AGMINER TOP")
    print("inspection_mode=READ_ONLY")

    if not rows:
        print("NONE")
        return

    for rank, row in enumerate(rows, start=1):
        energy_gj = float(row["energy_j"]) / 1.0e9
        print(
            str(rank)
            + " "
            + str(row["candidate_id"])
            + " family="
            + str(row["family"])
            + " energy_gj="
            + format(energy_gj, ".9f")
            + " state="
            + str(row["state"])
        )


def command_pareto(path: Path) -> None:
    if not path.exists():
        print("AGMINER_DATABASE_MISSING=" + str(path))
        return

    rows = pareto_frontier(survivor_rows(path))

    print("AGMINER PARETO")
    print("inspection_mode=READ_ONLY")

    if not rows:
        print("NONE")
        return

    for row in rows:
        print(
            str(row["candidate_id"])
            + " energy_j="
            + str(row["energy_j"])
        )


def command_stop(path: Path) -> None:
    storage = Storage(path)

    try:
        storage.set_metadata("stop_source", "cli")
        storage.request_stop()
        storage.checkpoint_wal()
        print("AGMINER_STOP_REQUESTED=YES")
        print("STOP_SOURCE=CLI")
    finally:
        storage.close()


def command_resume(path: Path) -> None:
    storage = Storage(path)

    try:
        storage.clear_stop()
        storage.set_metadata("stop_source", "")
        storage.checkpoint_wal()
        print("AGMINER_STOP_REQUESTED=NO")
        print("AGMINER_RESUME_STATE=READY")
    finally:
        storage.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m antigravity_research.agminer"
    )

    parser.add_argument(
        "--db",
        default=str(DEFAULT_DB),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser("policy")
    subparsers.add_parser("status")
    subparsers.add_parser("failures")
    subparsers.add_parser("pareto")
    subparsers.add_parser("stop")
    subparsers.add_parser("resume")

    top_parser = subparsers.add_parser("top")
    top_parser.add_argument("--top", type=int, default=10)

    arguments = parser.parse_args()
    path = Path(arguments.db)

    if arguments.command == "policy":
        command_policy()
    elif arguments.command == "status":
        command_status(path)
    elif arguments.command == "failures":
        command_failures(path)
    elif arguments.command == "top":
        command_top(path, arguments.top)
    elif arguments.command == "pareto":
        command_pareto(path)
    elif arguments.command == "stop":
        command_stop(path)
    elif arguments.command == "resume":
        command_resume(path)


if __name__ == "__main__":
    main()
