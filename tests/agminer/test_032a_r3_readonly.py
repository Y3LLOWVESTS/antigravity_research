"""Read-only live-inspection regression tests."""

from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.readonly import readonly_write_probe
from antigravity_research.agminer.readonly import status_snapshot
from antigravity_research.agminer.storage import Storage


def test_readonly_snapshot_works_while_writer_connection_open(tmp_path):
    path = tmp_path / "miner.sqlite3"
    storage = Storage(path)
    candidate = Candidate(
        family_id="READONLY_TEST",
        family_version="1",
        params={"x": 1},
        physical_model_version="P1",
        energy_ledger_version="L1",
    )
    storage.record_candidate(candidate)
    snapshot = status_snapshot(path)
    assert snapshot["models"] == 1
    storage.close()


def test_readonly_connection_rejects_write(tmp_path):
    path = tmp_path / "miner.sqlite3"
    storage = Storage(path)
    storage.close()
    assert readonly_write_probe(path)
