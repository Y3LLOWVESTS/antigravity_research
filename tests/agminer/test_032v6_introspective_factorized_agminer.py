"""032V6 Introspective-factorized AGMINER infrastructure tests."""

from __future__ import annotations

import math

from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.discovery import diagnose_candidate
from antigravity_research.agminer.mechanism import (
    MechanismMetrics,
    mechanism_loss_factors,
)
from antigravity_research.agminer.normalization import (
    canonical_invariant_fingerprint,
    normalization_equivalent,
)
from antigravity_research.agminer.oracle import (
    ActionOracle,
    LEDGER_COMPLETE_RELAXED,
    assess_collective_scaling,
    assess_oracle,
)
from antigravity_research.agminer.pareto import mechanism_pareto_frontier
from antigravity_research.agminer.reporting import rebuild_summaries
from antigravity_research.agminer.storage import Storage


def make_candidate() -> Candidate:
    return Candidate(
        family_id="032V6_TEST",
        family_version="1",
        params={"x": 1.0},
        physical_model_version="TEST",
        energy_ledger_version="CONSERVATIVE_COMPLETE_V1",
    )


def make_metrics(*, energy_j: float = 60.0e6) -> MechanismMetrics:
    return MechanismMetrics(
        net_response=10.0,
        gross_response=12.0,
        productive_charge_abs=4.0,
        productive_energy_j=12.0e6,
        complete_energy_j=energy_j,
        kernel_geometric_max=4.0,
        charge_units="TEST_CHARGE",
    )


def test_factorization_identity_is_exact_to_roundoff():
    metrics = make_metrics()
    assert metrics.identity_relative_error < 1.0e-15
    assert math.isclose(metrics.productive_participation, 0.2)
    assert math.isclose(metrics.cancellation_ratio, 1.2)
    assert math.isclose(metrics.kernel_effective, 3.0)
    assert math.isclose(metrics.kernel_relative, 0.75)
    assert math.isclose(metrics.organization_headroom, 8.0)


def test_candidate_internal_headrooms_do_not_use_historical_multipliers():
    loss = mechanism_loss_factors(make_metrics())
    assert math.isclose(loss["participation_headroom"], 5.0)
    assert math.isclose(loss["cancellation_headroom"], 1.2)
    assert math.isclose(loss["kernel_headroom"], 4.0 / 3.0)
    assert math.isclose(loss["organization_headroom"], 8.0)


def test_normalization_fingerprint_detects_equivalent_parameterizations():
    first = {"m_physical_gev": 480.3529517838922}
    second = {"m_physical_gev": 480.3529517838922}
    third = {"m_physical_gev": 100.0}

    assert normalization_equivalent(
        family_id="GHOST_TEST",
        family_version="1",
        first_invariants=first,
        second_invariants=second,
    )
    assert not normalization_equivalent(
        family_id="GHOST_TEST",
        family_version="1",
        first_invariants=first,
        second_invariants=third,
    )
    assert canonical_invariant_fingerprint(
        family_id="GHOST_TEST",
        family_version="1",
        invariants=first,
    ).startswith("CANON_")


def test_action_oracle_separates_intrinsic_and_realization_gap():
    oracle = ActionOracle(
        canonical_invariant_id="CANON_TEST",
        proof_reference="TEST",
        proven_lower_bound_j=1.0e6,
        relaxed_complete_energy_j=2.0e6,
        realized_complete_energy_j=60.0e6,
        ledger_scope=LEDGER_COMPLETE_RELAXED,
        normalization_invariant=True,
        naturalness_screened=True,
        universal_metric_screened=True,
    )
    assessment = assess_oracle(oracle, target_j=10.0e6)
    assert assessment.trusted_for_reachability
    assert assessment.priority == "REALIZATION_LIMITED_HIGH_PRIORITY"
    assert math.isclose(assessment.realization_gap, 30.0)


def test_collective_scaling_promotes_only_response_faster_than_energy():
    good = assess_collective_scaling(
        [1.0, 2.0, 4.0, 8.0],
        [1.0, 4.0, 16.0, 64.0],
        [1.0, 2.0, 4.0, 8.0],
        scaffold_energy_values=[1.0, 1.5, 2.25, 3.375],
    )
    assert good.beneficial_collective_scaling
    assert good.response_exponent > good.energy_exponent
    assert good.efficiency_exponent > 0.9

    bad = assess_collective_scaling(
        [1.0, 2.0, 4.0, 8.0],
        [1.0, 2.0, 4.0, 8.0],
        [1.0, 4.0, 16.0, 64.0],
    )
    assert not bad.beneficial_collective_scaling


def test_discovery_diagnosis_identifies_realization_limited_case():
    oracle = ActionOracle(
        canonical_invariant_id="CANON_TEST",
        proof_reference="TEST",
        proven_lower_bound_j=1.0e6,
        relaxed_complete_energy_j=2.0e6,
        realized_complete_energy_j=60.0e6,
        ledger_scope=LEDGER_COMPLETE_RELAXED,
        normalization_invariant=True,
        naturalness_screened=True,
        universal_metric_screened=True,
    )
    diagnosis = diagnose_candidate(
        current_complete_energy_j=60.0e6,
        oracle=oracle,
        mechanism=make_metrics(),
        target_j=10.0e6,
    )
    assert diagnosis.bottleneck == "MICROSCOPIC_REALIZATION_GAP"
    assert diagnosis.next_action == "OPTIMIZE_SOURCE_SCAFFOLD_AND_MORPHOLOGY"
    assert math.isclose(diagnosis.realization_gap, 30.0)


def test_storage_persists_factorized_metrics_oracle_and_scaling(tmp_path):
    storage = Storage(tmp_path / "miner.sqlite3")
    candidate = make_candidate()
    storage.record_candidate(candidate)
    storage.record_survivor(
        candidate.candidate_id,
        state="TIER1_SURVIVOR",
        tier=1,
        energy_j=60.0e6,
        payload_cm=10.0,
        payload_surface_min=9.9,
        naturalness_margin=3.0,
        stability_margin=2.0,
        leakage=1.0e-5,
        backreaction=1.0e-4,
    )

    metrics = make_metrics()
    storage.record_mechanism_metrics(candidate.candidate_id, metrics)

    oracle = ActionOracle(
        canonical_invariant_id="CANON_TEST",
        proof_reference="TEST",
        proven_lower_bound_j=1.0e6,
        relaxed_complete_energy_j=2.0e6,
        realized_complete_energy_j=60.0e6,
        ledger_scope=LEDGER_COMPLETE_RELAXED,
        normalization_invariant=True,
        naturalness_screened=True,
        universal_metric_screened=True,
    )
    storage.record_action_oracle(candidate.candidate_id, oracle)

    scaling = assess_collective_scaling(
        [1.0, 2.0, 4.0],
        [1.0, 4.0, 16.0],
        [1.0, 2.0, 4.0],
    )
    storage.record_collective_scaling(
        family=candidate.family_id,
        family_version=candidate.family_version,
        probe_id="TEST",
        assessment=scaling,
        proof_reference="TEST",
    )

    mechanism_rows = storage.mechanism_rows()
    oracle_rows = storage.oracle_rows()
    scaling_rows = storage.collective_scaling_rows()

    assert len(mechanism_rows) == 1
    assert len(oracle_rows) == 1
    assert len(scaling_rows) == 1
    assert mechanism_rows[0]["kernel_relative"] == 0.75
    assert oracle_rows[0]["priority"] == "REALIZATION_LIMITED_HIGH_PRIORITY"
    assert scaling_rows[0]["beneficial_collective_scaling"] == 1

    output = tmp_path / "summary"
    summary = rebuild_summaries(storage, output)
    assert summary["mechanism_metric_count"] == 1
    assert summary["action_oracle_count"] == 1
    assert summary["collective_scaling_count"] == 1
    assert (output / "mechanism_frontier.csv").exists()
    assert (output / "oracle_learning.csv").exists()
    assert (output / "collective_scaling.csv").exists()

    storage.close()


def test_mechanism_pareto_uses_interpretable_factorized_objectives():
    rows = [
        {
            "candidate_id": "A",
            "energy_j": 20.0e6,
            "response_per_complete_joule": 2.0,
            "productive_participation": 0.8,
            "kernel_relative": 0.9,
            "cancellation_ratio": 1.1,
            "scaffolding_fraction": 0.2,
            "realization_gap": 2.0,
        },
        {
            "candidate_id": "B",
            "energy_j": 30.0e6,
            "response_per_complete_joule": 1.0,
            "productive_participation": 0.5,
            "kernel_relative": 0.7,
            "cancellation_ratio": 1.5,
            "scaffolding_fraction": 0.5,
            "realization_gap": 3.0,
        },
    ]
    frontier = mechanism_pareto_frontier(rows)
    assert [row["candidate_id"] for row in frontier] == ["A"]
