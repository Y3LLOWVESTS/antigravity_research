import math

from antigravity_research.geometry.kottler import C

from antigravity_research.geometry.vacuum_energy_core import (
    compactness,
    de_sitter_horizon_radius_m,
    de_sitter_metric_derivative_per_m,
    de_sitter_metric_f,
    effective_lambda_m2,
    enclosed_energy_mass_kg,
    schwarzschild_metric_derivative_per_m,
    schwarzschild_metric_f,
    tov_pressure_gradient_pa_per_m,
    vacuum_energy_density_for_rate,
    weak_field_exterior_acceleration_m_s2,
)


def test_effective_lambda_matches_rate_identity():
    rate = 3.0

    epsilon = vacuum_energy_density_for_rate(
        rate
    )

    lam = effective_lambda_m2(
        epsilon
    )

    expected = (
        3.0
        * rate
        / C**2
    )

    assert math.isclose(
        lam,
        expected,
        rel_tol=1e-14,
    )


def test_de_sitter_and_schwarzschild_metric_values_match_at_boundary():
    radius = 2.0
    rate = 0.4

    epsilon = vacuum_energy_density_for_rate(
        rate
    )

    mass = enclosed_energy_mass_kg(
        radius,
        epsilon,
    )

    f_in = de_sitter_metric_f(
        radius,
        epsilon,
    )

    f_out = schwarzschild_metric_f(
        radius,
        mass,
    )

    assert math.isclose(
        f_in,
        f_out,
        rel_tol=1e-14,
        abs_tol=1e-15,
    )


def test_metric_derivatives_do_not_match_at_boundary():
    radius = 2.0
    rate = 0.4

    epsilon = vacuum_energy_density_for_rate(
        rate
    )

    mass = enclosed_energy_mass_kg(
        radius,
        epsilon,
    )

    inside = de_sitter_metric_derivative_per_m(
        radius,
        epsilon,
    )

    outside = schwarzschild_metric_derivative_per_m(
        radius,
        mass,
    )

    assert inside < 0.0
    assert outside > 0.0

    assert math.isclose(
        inside / outside,
        -2.0,
        rel_tol=1e-13,
    )


def test_w_minus_one_tov_gradient_is_zero():
    radius = 1.0
    rate = 1.0

    epsilon = vacuum_energy_density_for_rate(
        rate
    )

    pressure = -epsilon

    mass = enclosed_energy_mass_kg(
        radius,
        epsilon,
    )

    gradient = tov_pressure_gradient_pa_per_m(
        radius,
        mass,
        epsilon,
        pressure,
    )

    assert gradient == 0.0


def test_positive_energy_core_has_positive_mass():
    epsilon = vacuum_energy_density_for_rate(
        1.0
    )

    mass = enclosed_energy_mass_kg(
        1.0,
        epsilon,
    )

    assert epsilon > 0.0
    assert mass > 0.0


def test_positive_mass_exterior_is_inward_in_weak_field():
    epsilon = vacuum_energy_density_for_rate(
        1.0
    )

    mass = enclosed_energy_mass_kg(
        1.0,
        epsilon,
    )

    acceleration = (
        weak_field_exterior_acceleration_m_s2(
            2.0,
            mass,
        )
    )

    assert acceleration < 0.0


def test_compactness_matches_rate_radius_identity():
    radius = 4.0
    rate = 0.25

    epsilon = vacuum_energy_density_for_rate(
        rate
    )

    mass = enclosed_energy_mass_kg(
        radius,
        epsilon,
    )

    result = compactness(
        radius,
        mass,
    )

    expected = (
        rate
        * radius**2
        / C**2
    )

    assert math.isclose(
        result,
        expected,
        rel_tol=1e-14,
    )


def test_horizon_radius_gives_unit_compactness():
    rate = 2.0

    horizon = de_sitter_horizon_radius_m(
        rate
    )

    epsilon = vacuum_energy_density_for_rate(
        rate
    )

    mass = enclosed_energy_mass_kg(
        horizon,
        epsilon,
    )

    result = compactness(
        horizon,
        mass,
    )

    assert math.isclose(
        result,
        1.0,
        rel_tol=1e-14,
    )
