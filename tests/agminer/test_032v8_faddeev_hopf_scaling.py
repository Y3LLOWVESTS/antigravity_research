import math

from antigravity_research.agminer.oracle import assess_oracle
from antigravity_research.agminer.families.family_032v8_faddeev_hopf_shared_scaffold import (
    FaddeevHopfSharedScaffoldFamily,
    conditional_reference_equivalent_energy,
)


def test_032v8_hopf_efficiency_exponent_is_one_quarter():
    family = FaddeevHopfSharedScaffoldFamily()
    assert math.isclose(family.energy_exponent, 0.75)
    assert math.isclose(family.efficiency_exponent, 0.25)


def test_032v8_collective_scaling_is_beneficial():
    family = FaddeevHopfSharedScaffoldFamily()
    result = family.collective_scaling_probe({}, {})
    assert result.beneficial_collective_scaling is True
    assert math.isclose(result.response_exponent, 1.0, rel_tol=1e-12)
    assert math.isclose(result.energy_exponent, 0.75, rel_tol=1e-12)
    assert math.isclose(result.efficiency_exponent, 0.25, rel_tol=1e-12)


def test_032v8_q_1e12_gives_1000x_source_efficiency():
    family = FaddeevHopfSharedScaffoldFamily()
    assert math.isclose(
        family.efficiency_gain(1.0e12),
        1000.0,
        rel_tol=1e-12,
    )


def test_032v8_10mj_required_charge_scale():
    family = FaddeevHopfSharedScaffoldFamily()
    q = family.required_charge_scale(532.4046687159987)
    assert 8.0e10 < q < 8.1e10


def test_032v8_1mj_required_charge_scale():
    family = FaddeevHopfSharedScaffoldFamily()
    q = family.required_charge_scale(5324.0466871599865)
    assert 8.0e14 < q < 8.1e14


def test_032v8_reference_translation_is_not_oracle_certification():
    family = FaddeevHopfSharedScaffoldFamily()
    oracle = family.action_oracle({}, {})
    assessment = assess_oracle(oracle)
    translated = conditional_reference_equivalent_energy(
        5324046687.1599865,
        1.0e12,
    )
    assert 5.32e6 < translated < 5.33e6
    assert oracle.trusted_for_reachability is False
    assert assessment.priority == "ORACLE_PROVENANCE_INCOMPLETE"
