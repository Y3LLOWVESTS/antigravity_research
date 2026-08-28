"""Regression tests for the 008B canonical-scalar representability gate.

These tests protect:

- the canonical scalar kinetic-Gram identity;
- domain-wall and transfer-annulus decompositions;
- the three-gradient requirement in the finite support collar;
- smooth 006D collar termination;
- pointwise Gram positivity;
- the azimuthal-gradient obstruction to strictly axisymmetric scalar fields;
- the 006D Laue / canonical-scalar virial identity;
- the negative Derrick dilation mode.

Passing these tests does not establish a global scalar Lagrangian realization.
"""

from __future__ import annotations

import math

import pytest

from antigravity_research.geometry.canonical_scalar_representability import (
    ALPHA_006D,
    BETA_006D,
    FINEST_SCALE_006D,
    canonical_scalar_derrick_diagnostics,
    decompose_diagonal_stress,
    integrated_006d_energy_and_pressure_trace,
    regularized_006d_q_and_prime,
    regularized_006d_surface_stress,
    strictly_axisymmetric_scalars_sufficient,
)


def test_domain_wall_core_is_rank_one_canonical_scalar_state() -> None:
    """The 006D core has the standard domain-wall kinetic structure."""

    state = decompose_diagonal_stress(
        epsilon=1.0,
        p_r=-1.0,
        p_phi=-1.0,
        p_z=0.0,
    )

    assert state.gram_r == pytest.approx(0.0)
    assert state.gram_phi == pytest.approx(0.0)
    assert state.gram_z == pytest.approx(1.0)

    assert state.potential == pytest.approx(0.5)

    assert state.rank() == 1
    assert state.is_positive_semidefinite()


def test_transfer_annulus_requires_azimuthal_gradient_sector() -> None:
    """The conserved annulus is rank two and cannot use axisymmetric scalars."""

    u = 0.4

    state = decompose_diagonal_stress(
        epsilon=u,
        p_r=-u,
        p_phi=+u,
        p_z=0.0,
    )

    assert state.gram_r == pytest.approx(0.0)
    assert state.gram_phi == pytest.approx(2.0 * u)
    assert state.gram_z == pytest.approx(u)

    assert state.rank() == 2

    assert not strictly_axisymmetric_scalars_sufficient(
        state
    )


def test_outer_collar_requires_three_local_gradient_directions() -> None:
    """The midpoint of the 006D finite collar has full-rank scalar Gram data."""

    radius = (
        BETA_006D
        + 0.5 * FINEST_SCALE_006D
    )

    stress = regularized_006d_surface_stress(
        radius
    )

    decomposition = (
        stress.scalar_decomposition()
    )

    assert decomposition.is_positive_semidefinite()
    assert decomposition.rank() == 3

    assert decomposition.gram_r > 0.0
    assert decomposition.gram_phi > 0.0
    assert decomposition.gram_z > 0.0


def test_outer_006d_collar_terminates_q_and_q_prime() -> None:
    """No hidden line force remains at the independent 006D outer boundary."""

    radius = (
        BETA_006D
        + FINEST_SCALE_006D
    )

    q, qp = regularized_006d_q_and_prime(
        radius
    )

    assert q == pytest.approx(
        0.0,
        abs=1.0e-12,
    )

    assert qp == pytest.approx(
        0.0,
        abs=1.0e-9,
    )


def test_dense_006d_profile_has_positive_semidefinite_scalar_gram() -> None:
    """DEC-saturated 006D remains locally scalar-Gram compatible."""

    outer = (
        BETA_006D
        + FINEST_SCALE_006D
    )

    for index in range(4001):
        radius = (
            outer
            * index
            / 4000.0
        )

        decomposition = (
            regularized_006d_surface_stress(
                radius
            ).scalar_decomposition()
        )

        assert decomposition.is_positive_semidefinite(
            tolerance=1.0e-10
        )


def test_strictly_axisymmetric_real_scalars_fail_somewhere_in_006d() -> None:
    """The transfer annulus has M_phiphi > 0 and requires angular structure."""

    radius = (
        0.5
        * (
            ALPHA_006D
            + BETA_006D
        )
    )

    decomposition = (
        regularized_006d_surface_stress(
            radius
        ).scalar_decomposition()
    )

    assert decomposition.gram_phi > 0.0

    assert not strictly_axisymmetric_scalars_sufficient(
        decomposition
    )


def test_006d_laue_balance_becomes_scalar_virial_stationarity() -> None:
    """Independent 006D integration gives K/E=3/2 and U/E=-1/2."""

    energy, pressure_trace = (
        integrated_006d_energy_and_pressure_trace()
    )

    diagnostics = (
        canonical_scalar_derrick_diagnostics(
            energy,
            pressure_trace,
        )
    )

    assert abs(
        pressure_trace / energy
    ) < 1.0e-10

    assert (
        diagnostics.gradient_energy / energy
        == pytest.approx(
            1.5,
            rel=1.0e-10,
        )
    )

    assert (
        diagnostics.potential_energy / energy
        == pytest.approx(
            -0.5,
            rel=1.0e-10,
        )
    )

    assert diagnostics.stationary()


def test_006d_pure_static_canonical_scalar_has_negative_derrick_mode() -> None:
    """The stationary scalar reconstruction is unstable to uniform dilation."""

    energy, pressure_trace = (
        integrated_006d_energy_and_pressure_trace()
    )

    diagnostics = (
        canonical_scalar_derrick_diagnostics(
            energy,
            pressure_trace,
        )
    )

    assert (
        diagnostics.second_scaling_derivative
        < 0.0
    )

    assert (
        diagnostics.second_scaling_derivative
        / energy
        == pytest.approx(
            -3.0,
            rel=1.0e-10,
        )
    )

    assert not (
        diagnostics.stable_against_uniform_scaling()
    )

    assert math.isfinite(
        diagnostics.second_scaling_derivative
    )
