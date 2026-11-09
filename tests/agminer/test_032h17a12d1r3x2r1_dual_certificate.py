"""Regression tests for normalized maximin and dual source-cone logic."""

from __future__ import annotations

import numpy as np

from antigravity_research.agminer.hook17_fdual_f_r3x2r1_dual_certificate import (
    BRANCH,
    whiten_source_cone,
    verify_dual,
    verify_primal,
    decide,
)


def test_branch():
    assert BRANCH == "032H17A12D1R3X2R1"


def test_whitening_preserves_acceleration_per_physical_joule():
    h = np.diag([4.0, 9.0])
    a = np.array([h, 2.0 * h])

    white = whiten_source_cone(a, h)

    assert white["full_energy_rank_retained"] is True
    assert white["energy_rank"] == 2

    assert np.allclose(
        white["normalized_forms"][0],
        0.5 * np.eye(2),
    )

    assert np.allclose(
        white["normalized_forms"][1],
        np.eye(2),
    )


def test_negative_dual_reconstructed_from_weights_not_solver_status():
    b = np.array([
        -np.eye(2),
        -2.0 * np.eye(2),
    ])

    checked = verify_dual(
        b,
        np.array([1.0, 0.0]),
    )

    assert checked["strict_negative_dual_witness"] is True

    assert (
        checked["verified_dual_upper_scaled_per_j"]
        == -1.0
    )


def test_positive_dual_cannot_close_source_family():
    b = np.array([
        np.eye(2),
        np.eye(2),
    ])

    checked = verify_dual(
        b,
        np.array([0.5, 0.5]),
    )

    assert checked["strict_negative_dual_witness"] is False


def test_primal_trace_and_psd_verification():
    b = np.array([np.eye(2)])

    checked = verify_primal(
        b,
        0.5 * np.eye(2),
    )

    assert checked["primal_psd_trace_check"] is True

    assert abs(
        checked["minimum_acceleration_scaled_per_j"]
        - 1.0
    ) < 1.0e-15


def test_invalid_negative_dual_weights_rejected():
    b = np.array([
        -np.eye(2),
        -np.eye(2),
    ])

    checked = verify_dual(
        b,
        np.array([-0.4, 1.4]),
    )

    assert checked["valid_simplex"] is False
    assert checked["strict_negative_dual_witness"] is False


def _mock_grid(
    h: float,
    certified: bool,
):
    return {
        "h_m": h,
        "catalogs": {
            "shell_only": {
                "finite_grid_declared_cone_outward_impossibility_certificate":
                    certified,
            },
        },
    }


def test_certificate_does_not_close_all_independent_source_families():
    outcome = decide([
        _mock_grid(0.075, True),
        _mock_grid(0.05, True),
    ])

    assert outcome[
        "declared_shell_cone_dual_excluded_both_grids"
    ] is True

    assert outcome[
        "genuinely_independent_source_families_all_closed"
    ] is False

    assert outcome["006d_replaced"] is False


def test_no_closure_without_fine_grid_dual():
    outcome = decide([
        _mock_grid(0.075, True),
        _mock_grid(0.05, False),
    ])

    assert outcome["decision"].startswith(
        "YELLOW_R3X2R1_NO_STRICT"
    )

    assert outcome["complete_energy_established"] is False
