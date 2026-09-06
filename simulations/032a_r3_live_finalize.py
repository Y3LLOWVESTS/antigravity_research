"""Finalize 032A-R3 live operational certification."""

from __future__ import annotations

import json
import os
from pathlib import Path

from antigravity_research.agminer.readonly import readonly_write_probe
from antigravity_research.agminer.readonly import status_snapshot
from antigravity_research.agminer.storage import Storage


database = Path(os.environ["AGMINER_LIVE_DB"])
output = Path("results/agminer/032a_r3_live_certification_summary.json")

storage = Storage(database)

models = storage.model_count()
rejections = storage.rejection_count()
seen_cli_stop = storage.get_metadata("seen_cli_stop", "0") == "1"
seen_signal_stop = storage.get_metadata("seen_signal_stop", "0") == "1"
next_index = int(storage.get_metadata("live_next_index", "0"))
restart_zero_skips = int(storage.get_metadata("restart_zero_skips", "0"))
stop_requested = storage.stop_requested()

running_row = storage.connection.execute(
    """
    SELECT COUNT(*)
    FROM models
    WHERE state IN (
        "TIER0_RUNNING",
        "TIER1_RUNNING",
        "TIER2_RUNNING"
    )
    """
).fetchone()

running_count = int(running_row[0])

storage.checkpoint_wal()
storage.close()

readonly_blocked_write = readonly_write_probe(database)
snapshot = status_snapshot(database)

database_bytes = 0

for suffix in ("", "-wal", "-shm"):
    path = Path(str(database) + suffix)
    if path.exists():
        database_bytes += path.stat().st_size

concurrent_status_ok = os.environ.get("CONCURRENT_STATUS_OK") == "1"
concurrent_failures_ok = os.environ.get("CONCURRENT_FAILURES_OK") == "1"
cli_stop_rc_ok = os.environ.get("CLI_STOP_OK") == "1"
sigterm_send_ok = os.environ.get("SIGTERM_SEND_OK") == "1"
workers_ok = os.environ.get("WORKERS_OK") == "1"

green = all(
    [
        models == 80,
        rejections == 80,
        seen_cli_stop,
        seen_signal_stop,
        next_index == 80,
        restart_zero_skips == 80,
        not stop_requested,
        running_count == 0,
        readonly_blocked_write,
        snapshot["models"] == 80,
        snapshot["rejections"] == 80,
        concurrent_status_ok,
        concurrent_failures_ok,
        cli_stop_rc_ok,
        sigterm_send_ok,
        workers_ok,
        database_bytes < 10 * 1024 * 1024,
    ]
)

summary = {
    "models": models,
    "rejections": rejections,
    "seen_cli_stop": seen_cli_stop,
    "seen_signal_stop": seen_signal_stop,
    "next_index": next_index,
    "restart_zero_skips": restart_zero_skips,
    "stop_requested": stop_requested,
    "running_count": running_count,
    "readonly_blocked_write": readonly_blocked_write,
    "concurrent_status_ok": concurrent_status_ok,
    "concurrent_failures_ok": concurrent_failures_ok,
    "cli_stop_rc_ok": cli_stop_rc_ok,
    "sigterm_send_ok": sigterm_send_ok,
    "workers_ok": workers_ok,
    "database_bytes": database_bytes,
    "certification": "GREEN" if green else "RED",
    "real_032_physics_search": False,
}

output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(
    json.dumps(summary, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("MODEL_COUNT=" + str(models))
print("REJECTION_COUNT=" + str(rejections))
print("SEEN_CLI_STOP=" + str(seen_cli_stop))
print("SEEN_SIGTERM=" + str(seen_signal_stop))
print("FINAL_NEXT_INDEX=" + str(next_index))
print("RESTART_ZERO_SKIPS=" + str(restart_zero_skips))
print("RUNNING_COUNT=" + str(running_count))
print("READONLY_WRITE_BLOCKED=" + str(readonly_blocked_write))
print("CONCURRENT_STATUS_OK=" + str(concurrent_status_ok))
print("CONCURRENT_FAILURES_OK=" + str(concurrent_failures_ok))
print("DATABASE_BYTES=" + str(database_bytes))
print("032A_R3_LIVE_CERTIFICATION=" + ("GREEN" if green else "RED"))

if not green:
    raise RuntimeError("032A-R3 live certification failed")
