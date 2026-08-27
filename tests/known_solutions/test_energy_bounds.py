import math

from antigravity_research.geometry.energy_bounds import (
    active_energy_j,
    evaluate_integrated_type_i_dec,
    pointwise_dec_mass_lower_bound_kg,
    static_laue_dec_mass_lower_bound_kg,
)


G0 = 9.80665


def test_vacuum_stress_is_maximally_negative_dec_source():
    e = 10.0

    result = evaluate_integrated_type_i_dec(
        e,
        -e,
        -e,
        -e,
    )

    assert result.satisfied

    assert math.isclose(
        result.active_energy_j,
        -2.0 * e,
    )


def test_domain_wall_like_stress_has_minus_one_active_ratio():
    e = 10.0

    s = active_energy_j(
        e,
        0.0,
        -e,
        -e,
    )

    assert s == -e


def test_stiff_positive_stress_has_maximum_positive_active_ratio():
    e = 10.0

    result = evaluate_integrated_type_i_dec(
        e,
        e,
        e,
        e,
    )

    assert result.satisfied
    assert result.active_energy_j == 4.0 * e


def test_pressure_beyond_energy_fails_dec():
    result = evaluate_integrated_type_i_dec(
        1.0,
        -1.01,
        0.0,
        0.0,
    )

    assert not result.satisfied


def test_static_bound_is_twice_pointwise_bound():
    pointwise = pointwise_dec_mass_lower_bound_kg(
        G0,
        1.0,
    )

    static = static_laue_dec_mass_lower_bound_kg(
        G0,
        1.0,
    )

    assert math.isclose(
        static,
        2.0 * pointwise,
        rel_tol=1e-15,
    )


def test_bounds_scale_as_distance_squared():
    one_m = static_laue_dec_mass_lower_bound_kg(
        G0,
        1.0,
    )

    one_cm = static_laue_dec_mass_lower_bound_kg(
        G0,
        0.01,
    )

    assert math.isclose(
        one_cm / one_m,
        1.0e-4,
        rel_tol=1e-15,
    )
