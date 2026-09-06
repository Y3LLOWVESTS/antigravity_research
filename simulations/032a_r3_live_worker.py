"""Live AGMINER infrastructure worker.

This is synthetic software validation only.
It performs no real antigravity physics search.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.control import StopController
from antigravity_research.agminer.storage import Storage


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--total", type=int, default=80)
    parser.add_argument("--delay", type=float, default=0.03)
    parser.add_argument("--reset-stop", action="store_true")
    parser.add_argument("--restart-zero", action="store_true")
    arguments = parser.parse_args()

    path = Path(arguments.db)
    storage = Storage(path)
    controller = StopController(storage)

    if arguments.reset_stop:
        storage.clear_stop()
        storage.set_metadata("stop_source", "")

    def signal_callback() -> None:
        storage.set_metadata("stop_source", "signal")
        print("SIGNAL_STOP_REQUESTED=YES", flush=True)

    controller.install_signal_handlers(signal_callback)

    saved_index = int(storage.get_metadata("live_next_index", "0"))

    if arguments.restart_zero:
        start_index = 0
    else:
        start_index = saved_index

    storage.set_metadata("live_total", str(arguments.total))

    storage.start_run(
        run_id="032A_R3_LIVE",
        family="R3_SYNTHETIC_LIVE",
        family_version="1",
        config_fingerprint="R3_LIVE",
        sampler_seed=3201,
    )

    new_completed = 0
    known_skips = 0
    stopped = False

    print("WORKER_START_INDEX=" + str(start_index), flush=True)
    print("WORKER_TOTAL=" + str(arguments.total), flush=True)

    for index in range(start_index, arguments.total):
        if controller.requested():
            stopped = True
            break

        candidate = Candidate(
            family_id="032A_R3_SYNTHETIC_LIVE",
            family_version="1",
            params={"index": index},
            physical_model_version="INFRASTRUCTURE_ONLY",
            energy_ledger_version="CONSERVATIVE_COMPLETE_V1",
        )

        if storage.is_terminal(candidate.candidate_id):
            known_skips += 1
            storage.set_metadata("live_next_index", str(index + 1))
            continue

        storage.record_candidate(
            candidate,
            state="TIER0_RUNNING",
            tier=0,
            run_id="032A_R3_LIVE",
        )

        time.sleep(arguments.delay)

        storage.reject(
            candidate.candidate_id,
            state="REJECTED_NATURALNESS",
            failure_code="N003",
            gate="synthetic_live_naturalness",
            energy_j=8.0e6,
            run_id="032A_R3_LIVE",
        )

        new_completed += 1
        storage.set_metadata("live_next_index", str(index + 1))

    if controller.requested():
        stopped = True

    if stopped:
        source = storage.get_metadata("stop_source", "unknown")

        if source == "cli":
            storage.set_metadata("seen_cli_stop", "1")

        if source == "signal":
            storage.set_metadata("seen_signal_stop", "1")

        storage.finish_run("032A_R3_LIVE", status="STOPPED")
    else:
        storage.finish_run("032A_R3_LIVE", status="COMPLETED")

    if arguments.restart_zero:
        storage.set_metadata("restart_zero_skips", str(known_skips))

    storage.set_metadata("last_new_completed", str(new_completed))
    storage.set_metadata("last_known_skips", str(known_skips))
    storage.checkpoint_wal()

    print("NEW_COMPLETED=" + str(new_completed), flush=True)
    print("KNOWN_SKIPS=" + str(known_skips), flush=True)
    print("STOPPED=" + str(stopped), flush=True)
    print(
        "NEXT_INDEX="
        + str(storage.get_metadata("live_next_index", "0")),
        flush=True,
    )

    storage.close()


if __name__ == "__main__":
    main()
