"""
032A AGMINER infrastructure certification tests.

These tests certify software invariants only.
They make no claim about a new physical antigravity theory.
"""

from __future__ import annotations

from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.energy import (
    hard_energy_gate,
)
from antigravity_research.agminer.families.family_031_control import (
    historical_energy_controls,
)
from antigravity_research.agminer.families.family_mock_validation import (
    unprotected_sub10_control,
)
from antigravity_research.agminer.fingerprint import (
    candidate_fingerprint,
)
from antigravity_research.agminer.naturalness import (
    naturalness_gate,
)
from antigravity_research.agminer.pareto import (
    pareto_frontier,
)
from antigravity_research.agminer.sampler import (
    SobolSampler,
)
from antigravity_research.agminer.scheduler import (
    evaluate_mock_tier0,
)
from antigravity_research.agminer.storage import Storage


def test_fingerprint_is_parameter_order_invariant():
    common = {
        "family_id": "TEST",
        "family_version": "1",
        "physical_model_version": "P1",
        "energy_ledger_version": "L1",
    }

    first = candidate_fingerprint(
        params={
            "alpha": 1.0,
            "beta": 2.0,
        },
        **common,
    )

    second = candidate_fingerprint(
        params={
            "beta": 2.0,
            "alpha": 1.0,
        },
        **common,
    )

    assert first == second


def test_fingerprint_changes_when_physics_version_changes():
    first = candidate_fingerprint(
        family_id="TEST",
        family_version="1",
        params={"alpha": 1.0},
        physical_model_version="P1",
        energy_ledger_version="L1",
    )

    second = candidate_fingerprint(
        family_id="TEST",
        family_version="1",
        params={"alpha": 1.0},
        physical_model_version="P2",
        energy_ledger_version="L1",
    )

    assert first != second


def test_energy_9_999999_mj_passes():
    result = hard_energy_gate(
        9.999999e6
    )

    assert result.passed


def test_energy_exactly_10_mj_rejects():
    result = hard_energy_gate(
        10.000000e6
    )

    assert not result.passed
    assert result.failure_code == "E002"


def test_energy_10_000001_mj_rejects():
    result = hard_energy_gate(
        10.000001e6
    )

    assert not result.passed
    assert result.failure_code == "E002"


def test_analytic_lower_bound_at_10_mj_rejects():
    result = hard_energy_gate(
        9.0e6,
        lower_j=10.0e6,
        upper_j=11.0e6,
    )

    assert not result.passed
    assert result.failure_code == "E001"


def test_unprotected_candidate_fails_naturalness():
    result = naturalness_gate(
        protection_specified=False,
        margin=1000.0,
    )

    assert not result.passed
    assert result.failure_code == "N003"


def test_sqlite_rejection_persists(tmp_path):
    path = tmp_path / "agminer.sqlite3"

    candidate = Candidate(
        family_id="TEST",
        family_version="1",
        params={"energy": 12.0},
        physical_model_version="P1",
        energy_ledger_version="L1",
    )

    first = Storage(path)
    first.record_candidate(candidate)

    first.reject(
        candidate.candidate_id,
        state=str(hard_energy_gate(12.0e6).state),
        failure_code="E002",
        gate="energy",
        energy_j=12.0e6,
        run_id="TEST",
    )

    first.close()

    second = Storage(path)

    assert second.is_terminal(
        candidate.candidate_id
    )

    second.close()


def test_terminal_candidate_is_not_recomputed(tmp_path):
    path = tmp_path / "agminer.sqlite3"
    storage = Storage(path)

    candidate = Candidate(
        family_id="TEST",
        family_version="1",
        params={
            "energy_estimate_j": 12.0e9,
            "protection_specified": True,
            "naturalness_margin": 100.0,
        },
        physical_model_version="P1",
        energy_ledger_version="L1",
    )

    first = evaluate_mock_tier0(
        storage,
        candidate,
        run_id="TEST",
    )

    second = evaluate_mock_tier0(
        storage,
        candidate,
        run_id="TEST",
    )

    assert first.action == "REJECT"
    assert second.action == "SKIP_KNOWN"

    storage.close()


def test_exact_rejection_does_not_create_region_rule(tmp_path):
    path = tmp_path / "agminer.sqlite3"
    storage = Storage(path)

    candidate = Candidate(
        family_id="TEST",
        family_version="1",
        params={"energy": 12.0},
        physical_model_version="P1",
        energy_ledger_version="L1",
    )

    storage.record_candidate(candidate)

    storage.reject(
        candidate.candidate_id,
        state=str(hard_energy_gate(12.0e6).state),
        failure_code="E002",
        gate="energy",
        energy_j=12.0e6,
        run_id="TEST",
    )

    assert storage.region_rule_count() == 0

    storage.close()


def test_pareto_frontier_removes_dominated_point():
    rows = [
        {
            "candidate_id": "A",
            "energy_j": 4.0e9,
            "payload_surface_min": 10.0,
            "naturalness_margin": 100.0,
            "stability_margin": 10.0,
            "leakage": 0.1,
            "backreaction": 0.1,
        },
        {
            "candidate_id": "B",
            "energy_j": 5.0e9,
            "payload_surface_min": 9.0,
            "naturalness_margin": 50.0,
            "stability_margin": 5.0,
            "leakage": 0.2,
            "backreaction": 0.2,
        },
        {
            "candidate_id": "C",
            "energy_j": 3.0e9,
            "payload_surface_min": 8.0,
            "naturalness_margin": 200.0,
            "stability_margin": 20.0,
            "leakage": 0.05,
            "backreaction": 0.05,
        },
    ]

    ids = {
        row["candidate_id"]
        for row in pareto_frontier(rows)
    }

    assert "B" not in ids
    assert "A" in ids
    assert "C" in ids


def test_sobol_resume_reproduces_continuation():
    bounds = {
        "x": (0.0, 1.0),
        "y": (-1.0, 1.0),
    }

    continuous = SobolSampler(bounds)
    all_rows = continuous.sample(8)

    first = SobolSampler(bounds)
    first_rows = first.sample(3)

    resumed = SobolSampler(
        bounds,
        index=3,
    )

    remaining_rows = resumed.sample(5)

    assert first_rows == all_rows[:3]
    assert remaining_rows == all_rows[3:]


def test_stop_flag_round_trip(tmp_path):
    storage = Storage(
        tmp_path / "agminer.sqlite3"
    )

    assert not storage.stop_requested()

    storage.request_stop()
    assert storage.stop_requested()

    storage.clear_stop()
    assert not storage.stop_requested()

    storage.close()


def test_all_historical_031_energy_controls_exceed_10_gj():
    controls = historical_energy_controls()

    assert len(controls) == 7

    for control in controls:
        decision = hard_energy_gate(
            control.energy_j
        )

        assert not decision.passed
        assert decision.failure_code == "E002"


def test_unprotected_sub10_control_fails_before_energy_gate(tmp_path):
    storage = Storage(
        tmp_path / "agminer.sqlite3"
    )

    candidate = unprotected_sub10_control()

    result = evaluate_mock_tier0(
        storage,
        candidate,
        run_id="TEST",
    )

    assert result.action == "REJECT"
    assert (
        storage.candidate_state(
            candidate.candidate_id
        )
        == "REJECTED_NATURALNESS"
    )

    failures = storage.failure_counts()

    assert len(failures) == 1
    assert failures[0]["failure_code"] == "N003"
    assert failures[0]["gate"] == "naturalness"

    storage.close()
