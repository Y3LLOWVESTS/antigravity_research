import math

from antigravity_research.geometry.kottler import (
    G,
    cosmological_acceleration,
    static_radius,
    weak_field_attractive_acceleration,
    weak_field_radial_acceleration,
)


def test_zero_lambda_recovers_newtonian_gravity():
    radius = 1.0e20
    mass = 1.0e40

    expected = -(G * mass) / radius**2

    actual = weak_field_radial_acceleration(
        radius,
        mass,
        0.0,
    )

    assert math.isclose(
        actual,
        expected,
        rel_tol=1e-15,
    )


def test_positive_lambda_term_is_outward():
    result = cosmological_acceleration(
        radius_m=1.0e22,
        cosmological_constant_m2=1.0e-52,
    )

    assert result > 0.0


def test_mass_term_is_inward():
    result = weak_field_attractive_acceleration(
        radius_m=1.0e22,
        mass_kg=1.0e40,
    )

    assert result < 0.0


def test_static_radius_balances_terms():
    mass = 1.0e42
    cosmological_constant = 1.0e-52

    radius = static_radius(
        mass,
        cosmological_constant,
    )

    attractive = weak_field_attractive_acceleration(
        radius,
        mass,
    )

    outward = cosmological_acceleration(
        radius,
        cosmological_constant,
    )

    assert math.isclose(
        abs(attractive),
        outward,
        rel_tol=1e-12,
    )


def test_static_radius_scales_as_cube_root_of_mass():
    cosmological_constant = 1.0e-52

    r1 = static_radius(
        1.0e40,
        cosmological_constant,
    )

    r2 = static_radius(
        8.0e40,
        cosmological_constant,
    )

    assert math.isclose(
        r2 / r1,
        2.0,
        rel_tol=1e-12,
    )
