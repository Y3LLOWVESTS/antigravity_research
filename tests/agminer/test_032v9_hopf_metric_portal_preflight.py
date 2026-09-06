import math

from antigravity_research.agminer.families.family_032v9_hopf_metric_portal_preflight import (
    HopfPortalStructure,
    asymptotic_efficiency_exponent,
    fixed_response_ratio_linear_portal,
    linear_portal_asymptotic_exponent,
    maximum_mediator_coefficient_for_ratio,
    minimum_ratio_linear_portal,
    optimum_charge_scale_linear_portal,
    quadratic_metric_portal_asymptotic_exponent,
)


def test_032v9_hopf_secondary_locality_structure():
    x = HopfPortalStructure()
    assert x.hopf_is_secondary_invariant is True
    assert x.h3_s2_zero is True
    assert x.local_target_space_three_form_density_exists is False
    assert x.auxiliary_connection_required_for_cs_density is True


def test_032v9_direct_minimal_portals_do_not_supply_static_hopf_scalar_charge():
    x = HopfPortalStructure()
    assert x.direct_minimal_einstein_hopf_charge_portal is False
    assert x.derivative_scalar_current_static_bulk_source is False


def test_032v9_linear_canonical_mediator_kills_asymptotic_gain():
    assert math.isclose(
        linear_portal_asymptotic_exponent(),
        -1.0,
        rel_tol=1e-15,
    )


def test_032v9_quadratic_metric_response_saturates():
    assert math.isclose(
        quadratic_metric_portal_asymptotic_exponent(),
        0.0,
        abs_tol=1e-15,
    )


def test_032v9_linear_portal_closed_form_optimum():
    mu = 1.0e-15
    q = optimum_charge_scale_linear_portal(mu)
    direct = fixed_response_ratio_linear_portal(q, mu)
    analytic = minimum_ratio_linear_portal(mu)
    assert math.isclose(direct, analytic, rel_tol=1e-13)


def test_032v9_10mj_portal_coefficient_requirement():
    reference = 5324046687.1599865
    target_ratio = 1.0e7 / reference
    mu = maximum_mediator_coefficient_for_ratio(target_ratio)
    assert 1.90e-15 < mu < 1.93e-15


def test_032v9_1mj_portal_coefficient_requirement():
    reference = 5324046687.1599865
    target_ratio = 1.0e6 / reference
    mu = maximum_mediator_coefficient_for_ratio(target_ratio)
    assert 1.90e-20 < mu < 1.93e-20
