import math

from scipy.optimize import brentq

from antigravity_research.geometry.finite_tension_disk import (
    axial_acceleration_m_s2,
    dimensionless_axis_factor,
    integrated_spatial_stress_j,
    mass_coefficient_for_target,
    membrane_active_mass_kg,
    rim_active_mass_kg,
    total_active_mass_kg,
    total_rest_mass_kg,
)

from antigravity_research.geometry.relativistic_wall import (
    domain_wall_minimum_surface_energy_j_m2,
)


G0 = 9.80665


def test_support_restores_von_laue_stress_balance():
    membrane, rim, total = (
        integrated_spatial_stress_j(
            2.0,
            1.0e20,
            0.8,
        )
    )

    assert membrane < 0.0
    assert rim > 0.0

    scale = max(
        abs(membrane),
        abs(rim),
    )

    assert abs(total) < scale * 1.0e-14


def test_membrane_active_mass_is_negative_for_domain_wall():
    membrane = membrane_active_mass_kg(
        1.0,
        1.0e20,
        1.0,
    )

    assert membrane < 0.0


def test_rim_active_mass_is_positive():
    rim = rim_active_mass_kg(
        1.0,
        1.0e20,
        1.0,
    )

    assert rim > 0.0


def test_total_active_mass_equals_total_rest_mass():
    active = total_active_mass_kg(
        1.0,
        1.0e20,
        0.9,
    )

    rest = total_rest_mass_kg(
        1.0,
        1.0e20,
        0.9,
    )

    assert math.isclose(
        active,
        rest,
        rel_tol=1.0e-14,
    )


def test_domain_wall_surface_reconstructs_one_g():
    u = domain_wall_minimum_surface_energy_j_m2(
        G0
    )

    acceleration = axial_acceleration_m_s2(
        0.0,
        1.0,
        u,
        1.0,
    )

    assert math.isclose(
        acceleration,
        G0,
        rel_tol=1.0e-14,
    )


def test_domain_wall_repulsive_zone_root():
    root = brentq(
        lambda x:
            dimensionless_axis_factor(
                1.0,
                x,
            ),
        1.0e-12,
        2.0,
    )

    assert math.isclose(
        root,
        0.393319893190329,
        rel_tol=1.0e-11,
    )


def test_repulsive_below_root_and_attractive_above():
    assert (
        dimensionless_axis_factor(
            1.0,
            0.20,
        )
        > 0.0
    )

    assert (
        dimensionless_axis_factor(
            1.0,
            0.60,
        )
        < 0.0
    )


def test_far_field_is_attractive():
    u = 1.0e20

    acceleration = axial_acceleration_m_s2(
        100.0,
        1.0,
        u,
        1.0,
    )

    assert acceleration < 0.0


def test_q1_beats_q09_near_their_optimized_regions():
    q1 = mass_coefficient_for_target(
        1.0,
        0.25,
    )

    q09 = mass_coefficient_for_target(
        0.9,
        0.22,
    )

    assert q1 < q09
