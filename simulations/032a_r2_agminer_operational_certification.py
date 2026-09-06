"""032A-R2 operational infrastructure validation.

This validates AGMINER controls and storage only.
No real 032 physical theory is searched.
"""

from pathlib import Path
import tempfile

from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.pareto import pareto_frontier
from antigravity_research.agminer.policy import current_energy_policy
from antigravity_research.agminer.reporting import rebuild_summaries
from antigravity_research.agminer.sampler import SobolSampler
from antigravity_research.agminer.storage import Storage


policy = current_energy_policy()

print("=== 032A-R2 OPERATIONAL CERTIFICATION ===")
print("REAL_032_PHYSICS_SEARCH=NO")
print("ENERGY_POLICY=" + str(policy["comparison"]) + "_" + str(policy["value"]) + "_" + str(policy["unit"]))

with tempfile.TemporaryDirectory(prefix="agminer_r2_") as temp:
    root = Path(temp)
    db = root / "agminer.sqlite3"
    summaries = root / "summaries"
    storage = Storage(db)

    storage.start_run(
        run_id="032A_R2",
        family="SYNTHETIC_INFRASTRUCTURE",
        family_version="1",
        config_fingerprint="R2",
        sampler_seed=3201,
    )

    bounds = {
        "x": (0.0, 1.0),
        "y": (0.0, 1.0),
    }

    sampler = SobolSampler(bounds)
    samples = sampler.sample(64)
    sampler_position = sampler.index
    storage.set_metadata("sampler_index", str(sampler_position))

    completed_ids = []

    for index, params in enumerate(samples[:32]):
        candidate = Candidate(
            family_id="R2_SYNTHETIC",
            family_version="1",
            params=params,
            physical_model_version="INFRASTRUCTURE_ONLY",
            energy_ledger_version="CONSERVATIVE_COMPLETE_V1",
        )
        storage.record_candidate(candidate, state="TIER0_RUNNING", run_id="032A_R2")
        storage.reject(
            candidate.candidate_id,
            state="REJECTED_NATURALNESS",
            failure_code="N003",
            gate="naturalness",
            energy_j=8.0e6,
            run_id="032A_R2",
        )
        completed_ids.append(candidate.candidate_id)

    interrupted = Candidate(
        family_id="R2_SYNTHETIC",
        family_version="1",
        params=samples[32],
        physical_model_version="INFRASTRUCTURE_ONLY",
        energy_ledger_version="CONSERVATIVE_COMPLETE_V1",
    )

    storage.record_candidate(
        interrupted,
        state="TIER1_RUNNING",
        run_id="032A_R2",
    )

    storage.request_stop()
    stop_persisted_before_close = storage.stop_requested()
    storage.close()

    resumed = Storage(db)
    stop_persisted_after_reopen = resumed.stop_requested()
    recovered = resumed.recover_interrupted_candidates()
    interrupted_state = resumed.candidate_state(interrupted.candidate_id)

    duplicate_skips = sum(resumed.is_terminal(candidate_id) for candidate_id in completed_ids)

    saved_index = int(resumed.get_metadata("sampler_index", "0"))
    continuation = SobolSampler(bounds, index=saved_index)
    resumed_samples = continuation.sample(16)
    reference = SobolSampler(bounds).sample(80)[64:80]
    sampler_resume_match = resumed_samples == reference

    resumed.clear_stop()
    stop_cleared = not resumed.stop_requested()

    survivor_rows = [
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

    pareto_a = pareto_frontier(survivor_rows)
    pareto_b = pareto_frontier(list(reversed(survivor_rows)))
    pareto_reproducible = pareto_a == pareto_b

    summary = rebuild_summaries(resumed, summaries)

    resumed.finish_run("032A_R2", status="COMPLETED_GREEN")
    resumed.checkpoint_wal()
    resumed.close()

    database_bytes = 0
    for suffix in ("", "-wal", "-shm"):
        path = Path(str(db) + suffix)
        if path.exists():
            database_bytes += path.stat().st_size

    print("STOP_PERSISTED_BEFORE_CLOSE=" + str(stop_persisted_before_close))
    print("STOP_PERSISTED_AFTER_REOPEN=" + str(stop_persisted_after_reopen))
    print("STOP_CLEARED_ON_RESUME=" + str(stop_cleared))
    print("CRASH_RECOVERED_COUNT=" + str(recovered))
    print("INTERRUPTED_STATE=" + str(interrupted_state))
    print("COMPLETED_DUPLICATE_SKIPS=" + str(duplicate_skips))
    print("EXPECTED_COMPLETED_DUPLICATE_SKIPS=32")
    print("SAMPLER_INDEX_SAVED=" + str(saved_index))
    print("SAMPLER_RESUME_MATCH=" + str(sampler_resume_match))
    print("PARETO_REPRODUCIBLE=" + str(pareto_reproducible))
    print("PARETO_IDS=" + ",".join(row["candidate_id"] for row in pareto_a))
    print("SUMMARY_MODEL_COUNT=" + str(summary["model_count"]))
    print("DATABASE_BYTES=" + str(database_bytes))

    green = (
        stop_persisted_before_close
        and stop_persisted_after_reopen
        and stop_cleared
        and recovered == 1
        and interrupted_state == "REJECTED_NUMERICAL"
        and duplicate_skips == 32
        and saved_index == 64
        and sampler_resume_match
        and pareto_reproducible
        and database_bytes < 10 * 1024 * 1024
    )

    print("032A_R2_OPERATIONAL_CERTIFICATION=" + ("GREEN" if green else "RED"))
