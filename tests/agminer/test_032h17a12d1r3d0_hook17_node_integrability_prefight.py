"""Regression tests for 032H17A12D1R3D0."""

from __future__ import annotations

import math

import numpy as np

from antigravity_research.agminer.hook17_fdual_f_r3d0_node_integrability import (
    BRANCH,
    BVP_AUTHORIZATION_DRIVER_RATIO,
    GRID_SPACINGS_M,
    LMAX_VALUES,
    R3C1_FINE_CRITICAL_LOADING,
    closed_surface_integrability_gate,
    decision_from_atlas,
    exterior_energy_j,
    generalized_trace_modes,
    shape_library,
)


def test_branch_name():
    assert (
        BRANCH
        ==
        "032H17A12D1R3D0"
    )


def test_exact_closed_node_is_not_claimed_possible():
    gate = (
        closed_surface_integrability_gate()
    )

    assert gate[
        "exact_nontrivial_single_field_closed_node"
    ] is False

    assert gate[
        "approximate_node_still_open"
    ] is True


def test_cross_topological_fallback_is_preserved():
    assert (
        closed_surface_integrability_gate()[
            "cross_topological_fallback_preserved"
        ]
        is True
    )


def test_r3c1_finest_threshold_is_frozen():
    assert math.isclose(
        R3C1_FINE_CRITICAL_LOADING,
        1.0396081544458862e-5,
        rel_tol=0.0,
        abs_tol=1.0e-18,
    )


def test_bvp_authorization_is_not_looser_than_one_e_minus_four():
    assert (
        BVP_AUTHORIZATION_DRIVER_RATIO
        <=
        1.0e-4
    )


def test_preflight_resolves_interface_with_at_least_four_cells():
    assert (
        min(
            0.1
            /
            h
            for h in GRID_SPACINGS_M
        )
        >=
        4.0
    )


def test_lmax_sequence_is_monotone_and_reaches_20():
    assert (
        tuple(
            sorted(
                LMAX_VALUES
            )
        )
        ==
        LMAX_VALUES
    )

    assert (
        max(
            LMAX_VALUES
        )
        >=
        20
    )


def test_generalized_trace_mode_finds_exact_synthetic_null():
    total = np.eye(
        2
    )

    bad = np.diag(
        [
            0.0,
            1.0,
        ]
    )

    result = (
        generalized_trace_modes(
            bad,
            total,
        )
    )

    assert (
        result[
            "fractions_squared"
        ][
            0
        ]
        <
        1.0e-10
    )


def test_shape_library_is_nonempty():
    modes = {
        "vectors":
            np.eye(
                4
            ),

        "total_regularized":
            np.eye(
                4
            ),
    }

    assert (
        len(
            shape_library(
                modes
            )
        )
        >=
        4
    )


def test_exterior_energy_is_positive():
    assert (
        exterior_energy_j(
            np.array(
                [
                    1.0,
                    0.0,
                    0.0,
                ]
            )
        )
        >
        0.0
    )


def _mock(
    driver: float,
    energy: float = 1.0,
):
    return {
        "best":
            {
                "driver_ratio_vs_r3b":
                    driver,

                "sub100j_exterior_capacity":
                    energy
                    <
                    100.0,

                "exterior_canonical_energy_j":
                    energy,
            }
    }


def test_decision_promotes_only_two_grid_near_node_candidate():
    atlas = []

    for h in GRID_SPACINGS_M:
        for lmax in LMAX_VALUES:
            row = {
                "grid_spacing_m":
                    h,

                "lmax":
                    lmax,

                "best":
                    None,
            }

            if (
                lmax
                ==
                max(
                    LMAX_VALUES
                )
            ):
                row.update(
                    _mock(
                        5.0e-5
                    )
                )

            atlas.append(
                row
            )

    result = (
        decision_from_atlas(
            atlas
        )
    )

    assert result[
        "authorize_single_field_loaded_r3d1"
    ] is True

    assert result[
        "authorize_cross_topological_r3x0"
    ] is False


def test_decision_pivots_when_node_target_is_missed():
    atlas = []

    for h in GRID_SPACINGS_M:
        for lmax in LMAX_VALUES:
            row = {
                "grid_spacing_m":
                    h,

                "lmax":
                    lmax,

                "best":
                    None,
            }

            if (
                lmax
                ==
                max(
                    LMAX_VALUES
                )
            ):
                row.update(
                    _mock(
                        2.0e-3
                    )
                )

            atlas.append(
                row
            )

    result = (
        decision_from_atlas(
            atlas
        )
    )

    assert result[
        "authorize_single_field_loaded_r3d1"
    ] is False

    assert result[
        "authorize_cross_topological_r3x0"
    ] is True

    assert result[
        "006d_replaced"
    ] is False
