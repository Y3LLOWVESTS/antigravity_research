"""032A-R2 AGMINER operational certification tests."""

from pathlib import Path

from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.checkpoint import enforce_checkpoint_limit
from antigravity_research.agminer.pareto import pareto_frontier
from antigravity_research.agminer.reporting import configure_logging
from antigravity_research.agminer.sampler import SobolSampler
from antigravity_research.agminer.storage import Storage


def make_candidate(index: int) -> Candidate:
    return Candidate(
        family_id="032A_R2_SYNTHETIC",
        family_version="1",
        params={"index": index},
        physical_model_version="INFRASTRUCTURE_ONLY",
        energy_ledger_version="CONSERVATIVE_COMPLETE_V1",
    )


def test_crash_recovery_marks_running_as_numerical_not_physics(tmp_path):
    storage = Storage(tmp_path / "miner.sqlite3")
    candidate = make_candidate(1)
    storage.record_candidate(candidate, state="TIER1_RUNNING")
    recovered = storage.recover_interrupted_candidates()
    assert recovered == 1
    assert storage.candidate_state(candidate.candidate_id) == "REJECTED_NUMERICAL"
    storage.close()


def test_crash_recovery_does_not_touch_completed_rejection(tmp_path):
    storage = Storage(tmp_path / "miner.sqlite3")
    candidate = make_candidate(2)
    storage.record_candidate(candidate)
    storage.reject(
        candidate.candidate_id,
        state="REJECTED_NATURALNESS",
        failure_code="N003",
        gate="naturalness",
        energy_j=8.0e6,
        run_id="TEST",
    )
    recovered = storage.recover_interrupted_candidates()
    assert recovered == 0
    assert storage.candidate_state(candidate.candidate_id) == "REJECTED_NATURALNESS"
    storage.close()


def test_stop_flag_persists_restart(tmp_path):
    path = tmp_path / "miner.sqlite3"
    first = Storage(path)
    first.request_stop()
    first.close()
    second = Storage(path)
    assert second.stop_requested()
    second.clear_stop()
    second.close()
    third = Storage(path)
    assert not third.stop_requested()
    third.close()


def test_resume_sampler_index_is_reproducible():
    bounds = {
        "x": (0.0, 1.0),
        "y": (-2.0, 2.0),
        "z": (5.0, 9.0),
    }
    continuous = SobolSampler(bounds)
    expected = continuous.sample(32)
    first = SobolSampler(bounds)
    prefix = first.sample(11)
    resumed = SobolSampler(bounds, index=11)
    suffix = resumed.sample(21)
    assert prefix + suffix == expected


def test_pareto_reconstruction_is_order_independent():
    rows = [
        {
            "candidate_id": "A",
            "energy_j": 2.0e6,
            "payload_surface_min": 10.0,
            "naturalness_margin": 10.0,
            "stability_margin": 3.0,
            "leakage": 1.0e-6,
            "backreaction": 1.0e-5,
        },
        {
            "candidate_id": "B",
            "energy_j": 3.0e6,
            "payload_surface_min": 20.0,
            "naturalness_margin": 20.0,
            "stability_margin": 5.0,
            "leakage": 1.0e-7,
            "backreaction": 1.0e-6,
        },
        {
            "candidate_id": "C",
            "energy_j": 4.0e6,
            "payload_surface_min": 9.0,
            "naturalness_margin": 5.0,
            "stability_margin": 1.0,
            "leakage": 1.0e-4,
            "backreaction": 1.0e-3,
        },
    ]
    forward = pareto_frontier(rows)
    reverse = pareto_frontier(list(reversed(rows)))
    assert forward == reverse
    assert [row["candidate_id"] for row in forward] == ["A", "B"]


def test_checkpoint_retention_is_bounded(tmp_path):
    checkpoint_dir = tmp_path / "checkpoints"
    checkpoint_dir.mkdir()
    for index in range(30):
        path = checkpoint_dir / f"candidate_{index:03d}.npz"
        path.write_bytes(b"x")
    removed = enforce_checkpoint_limit(checkpoint_dir, limit=25)
    remaining = list(checkpoint_dir.iterdir())
    assert len(removed) == 5
    assert len(remaining) == 25


def test_rotating_log_is_bounded(tmp_path):
    path = tmp_path / "agminer_current.log"
    logger = configure_logging(path, max_mb=1, backup_count=2)
    for _ in range(5000):
        logger.info("R2 " + ("x" * 300))
    for handler in logger.handlers:
        handler.flush()
    files = list(tmp_path.glob("agminer_current.log*"))
    total = sum(path.stat().st_size for path in files)
    assert len(files) <= 3
    assert total < 4 * 1024 * 1024


def test_sqlite_growth_stays_compact_for_5000_failures(tmp_path):
    path = tmp_path / "miner.sqlite3"
    storage = Storage(path)
    for index in range(5000):
        candidate = make_candidate(index)
        storage.record_candidate(candidate)
        storage.reject(
            candidate.candidate_id,
            state="REJECTED_NATURALNESS",
            failure_code="N003",
            gate="naturalness",
            energy_j=8.0e6,
            run_id="R2",
        )
    storage.checkpoint_wal()
    storage.close()
    total = 0
    for suffix in ("", "-wal", "-shm"):
        candidate_path = Path(str(path) + suffix)
        if candidate_path.exists():
            total += candidate_path.stat().st_size
    assert total < 10 * 1024 * 1024
