import math

from antigravity_research.agminer.oracle import assess_oracle
from antigravity_research.agminer.families.family_032v7_cpn_shared_scaffold_source import (
    SharedScaffoldCPNSourceFamily,
    required_exponent_advantage,
)


def test_032v7_efficiency_exponent_is_one_sixth():
    family = SharedScaffoldCPNSourceFamily()
    assert math.isclose(family.energy_exponent, 5.0/6.0)
    assert math.isclose(family.efficiency_exponent, 1.0/6.0)


def test_032v7_scaling_is_beneficial_but_weak():
    family = SharedScaffoldCPNSourceFamily()
    result = family.collective_scaling_probe({}, {})
    assert result.beneficial_collective_scaling is True
    assert math.isclose(result.response_exponent, 1.0, rel_tol=1e-12)
    assert math.isclose(result.energy_exponent, 5.0/6.0, rel_tol=1e-12)
    assert math.isclose(result.efficiency_exponent, 1.0/6.0, rel_tol=1e-12)


def test_032v7_532_gain_requires_enormous_charge_dynamic_range():
    family = SharedScaffoldCPNSourceFamily()
    scale = family.required_charge_scale(532.4046687159987)
    assert scale > 2.0e16
    assert scale < 2.5e16


def test_032v7_one_trillion_charge_scale_only_gives_100x():
    family = SharedScaffoldCPNSourceFamily()
    gain = family.efficiency_gain(1.0e12)
    assert math.isclose(gain, 100.0, rel_tol=1e-12)


def test_032v7_oracle_is_not_trusted_as_antigravity_reachability():
    family = SharedScaffoldCPNSourceFamily()
    oracle = family.action_oracle({}, {})
    assessment = assess_oracle(oracle)
    assert oracle.normalization_invariant is True
    assert oracle.naturalness_screened is False
    assert oracle.universal_metric_screened is False
    assert oracle.trusted_for_reachability is False
    assert assessment.priority == "ORACLE_PROVENANCE_INCOMPLETE"


def test_032v7_required_exponent_advantage_for_1e12_dynamic_range():
    delta = required_exponent_advantage(
        532.4046687159987,
        1.0e12,
    )
    assert 0.227 < delta < 0.228
