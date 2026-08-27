import math

from antigravity_research.geometry.relativistic_wall import (
    domain_wall_minimum_surface_energy_j_m2,
    evaluate_wall_energy_conditions,
    outward_planar_acceleration_m_s2,
    phi4_v_gev_for_tension,
    required_surface_energy_j_m2,
)


G0 = 9.80665


def test_dust_sheet_is_attractive():
    result = outward_planar_acceleration_m_s2(
        1.0e20,
        0.0,
    )

    assert result < 0.0


def test_half_tension_is_zero_gravity_threshold():
    u = 1.0e20

    result = outward_planar_acceleration_m_s2(
        u,
        0.5 * u,
    )

    assert result == 0.0


def test_three_quarter_tension_repels():
    u = 1.0e20

    result = outward_planar_acceleration_m_s2(
        u,
        0.75 * u,
    )

    assert result > 0.0


def test_three_quarter_tension_passes_energy_conditions():
    u = 1.0e20
    tau = 0.75 * u

    conditions = evaluate_wall_energy_conditions(
        u,
        tau,
    )

    assert conditions.nec
    assert conditions.wec
    assert conditions.dec


def test_domain_wall_saturates_nec_and_dec_and_repels():
    u = 1.0e20
    tau = u

    conditions = evaluate_wall_energy_conditions(
        u,
        tau,
    )

    acceleration = outward_planar_acceleration_m_s2(
        u,
        tau,
    )

    assert conditions.nec
    assert conditions.wec
    assert conditions.dec
    assert acceleration > 0.0


def test_super_domain_wall_tension_violates_nec_dec():
    u = 1.0e20
    tau = 1.1 * u

    conditions = evaluate_wall_energy_conditions(
        u,
        tau,
    )

    assert not conditions.nec
    assert not conditions.wec
    assert not conditions.dec


def test_required_energy_reconstructs_one_g():
    q = 0.8

    u = required_surface_energy_j_m2(
        G0,
        q,
    )

    result = outward_planar_acceleration_m_s2(
        u,
        q * u,
    )

    assert math.isclose(
        result,
        G0,
        rel_tol=1.0e-14,
    )


def test_domain_wall_is_minimum_energy_within_dec_family():
    minimum = (
        domain_wall_minimum_surface_energy_j_m2(
            G0
        )
    )

    for q in (
        0.51,
        0.6,
        0.75,
        0.9,
    ):
        required = required_surface_energy_j_m2(
            G0,
            q,
        )

        assert required > minimum


def test_one_g_phi4_scale_is_electroweak_order_for_lambda_one():
    u = domain_wall_minimum_surface_energy_j_m2(
        G0
    )

    v = phi4_v_gev_for_tension(
        u,
        1.0,
    )

    assert 50.0 < v < 150.0
