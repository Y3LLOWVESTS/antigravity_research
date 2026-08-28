"""Regression tests for the 008A wall-current-loop effective gate.

These tests protect the equilibrium derivation, radial stability, effective
DEC, gravitational source, and the independent recovery of the Simulation
005B disk-plus-minimum-rim architecture.

They do not establish full vorton field-theory stability or a practical
antigravity source.
"""

from __future__ import annotations

import math

import pytest

from antigravity_research.geometry.axisymmetric_thin_stress import (
    uniform_disk_ring_field_factor,
    uniform_disk_ring_mass_coefficient,
)
from antigravity_research.geometry.wall_current_loop import (
    equilibrium_boundary_state_j_m,
    equilibrium_current_parameter_j_m,
    field_factor,
    mass_coefficient,
    optimize_mass_coefficient,
    total_energy_derivative_j_m,
    total_energy_second_derivative_j_m2,
)


def test_equilibrium_current_makes_first_derivative_zero() -> None:
    sigma = 7.0
    mu = 2.0
    radius = 3.0

    j = equilibrium_current_parameter_j_m(
        sigma,
        mu,
        radius,
    )

    assert total_energy_derivative_j_m(
        sigma,
        mu,
        j,
        radius,
    ) == pytest.approx(0.0, abs=1.0e-12)


def test_equilibrium_radial_mode_is_locally_stable() -> None:
    sigma = 7.0
    mu = 2.0
    radius = 3.0

    j = equilibrium_current_parameter_j_m(
        sigma,
        mu,
        radius,
    )

    assert total_energy_second_derivative_j_m2(
        sigma,
        j,
        radius,
    ) > 0.0


def test_equilibrium_boundary_provides_required_compression() -> None:
    sigma = 11.0
    mu = 5.0
    radius = 2.0

    energy, tension, active = (
        equilibrium_boundary_state_j_m(
            sigma,
            mu,
            radius,
        )
    )

    assert tension == pytest.approx(
        -sigma * radius
    )

    assert energy == pytest.approx(
        sigma * radius + 2.0 * mu
    )

    assert active == pytest.approx(
        2.0 * (sigma * radius + mu)
    )


def test_effective_boundary_dec_holds_for_nonnegative_bare_energy() -> None:
    for mu in (0.0, 0.1, 1.0, 10.0):
        energy, tension, _ = (
            equilibrium_boundary_state_j_m(
                3.0,
                mu,
                2.0,
            )
        )

        assert energy >= 0.0
        assert abs(tension) <= energy + 1.0e-14


def test_zero_bare_string_field_matches_independent_005b_expression() -> None:
    for x in (2.5, 4.0, 4.7, 8.0):
        assert field_factor(
            x,
            0.0,
        ) == pytest.approx(
            uniform_disk_ring_field_factor(x),
            rel=1.0e-14,
            abs=1.0e-14,
        )


def test_zero_bare_string_mass_matches_independent_005b_expression() -> None:
    for x in (3.0, 4.0, 5.0, 8.0):
        assert mass_coefficient(
            x,
            0.0,
        ) == pytest.approx(
            uniform_disk_ring_mass_coefficient(x),
            rel=1.0e-14,
        )


def test_zero_bare_string_optimum_recovers_005b() -> None:
    x, coefficient = optimize_mass_coefficient(
        0.0
    )

    assert x == pytest.approx(
        4.00614973,
        abs=2.0e-6,
    )

    assert coefficient == pytest.approx(
        79.753148116012,
        rel=1.0e-11,
    )


def test_positive_bare_string_energy_only_worsens_optimum() -> None:
    _, baseline = optimize_mass_coefficient(
        0.0
    )

    previous = baseline

    for m in (0.01, 0.05, 0.10, 0.25):
        _, coefficient = optimize_mass_coefficient(
            m
        )

        assert coefficient > previous
        previous = coefficient

    assert math.isfinite(previous)
