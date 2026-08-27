import math

from antigravity_research.geometry.kottler import (
    C,
    static_radius,
)

from antigravity_research.geometry.kottler_tidal import (
    radial_tidal_eigenvalue_s2,
    tidal_trace_s2,
    transverse_tidal_eigenvalue_s2,
)


def test_schwarzschild_tidal_trace_is_zero():
    trace = tidal_trace_s2(
        radius_m=1.0e22,
        mass_kg=1.0e40,
        cosmological_constant_m2=0.0,
    )

    assert math.isclose(
        trace,
        0.0,
        abs_tol=1e-45,
    )


def test_de_sitter_tidal_field_is_isotropic():
    radius = 1.0e22
    cosmological_constant = 1.0e-52

    radial = radial_tidal_eigenvalue_s2(
        radius,
        0.0,
        cosmological_constant,
    )

    transverse = transverse_tidal_eigenvalue_s2(
        radius,
        0.0,
        cosmological_constant,
    )

    assert math.isclose(
        radial,
        transverse,
        rel_tol=1e-15,
    )


def test_positive_lambda_trace_equals_lambda_c_squared():
    cosmological_constant = 1.0e-52

    trace = tidal_trace_s2(
        radius_m=1.0e22,
        mass_kg=1.0e40,
        cosmological_constant_m2=cosmological_constant,
    )

    expected = cosmological_constant * C**2

    assert math.isclose(
        trace,
        expected,
        rel_tol=1e-12,
    )


def test_transverse_mode_zero_at_static_radius():
    mass = 1.0e42
    cosmological_constant = 1.0e-52

    radius = static_radius(
        mass,
        cosmological_constant,
    )

    transverse = transverse_tidal_eigenvalue_s2(
        radius,
        mass,
        cosmological_constant,
    )

    scale = cosmological_constant * C**2 / 3.0

    assert abs(transverse) < scale * 1e-12


def test_above_static_radius_all_three_spatial_modes_stretch():
    mass = 1.0e42
    cosmological_constant = 1.0e-52

    radius = 2.0 * static_radius(
        mass,
        cosmological_constant,
    )

    radial = radial_tidal_eigenvalue_s2(
        radius,
        mass,
        cosmological_constant,
    )

    transverse = transverse_tidal_eigenvalue_s2(
        radius,
        mass,
        cosmological_constant,
    )

    assert radial > 0.0
    assert transverse > 0.0
