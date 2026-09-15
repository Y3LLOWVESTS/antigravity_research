"""Regressions for 032H17A12D1R2B1 grid-complete source certificate."""

from __future__ import annotations

import math

import numpy as np

from antigravity_research.agminer.hook17_f2_1kev_grid_complete_source_bound import (
    A12C_REFERENCE_CAPACITY_J,
    BRANCH,
    CERTIFICATE_GRID_SPACINGS_M,
    PORTAL_SCALE_EV,
    acceleration_bilinear_matrix,
    certificate_payload_points,
    claim_policy_gate,
    classify_capacity_targets,
    prior_bottleneck_point,
    provenance_gate,
    source_support_unknown_indices,
    target_efficiency_m_s2_per_j,
)
from antigravity_research.agminer.hook17_f2_strong_payload_loading_rescue import (
    _grid,
)


def test_branch_name_is_frozen():
    assert BRANCH == "032H17A12D1R2B1"


def test_provenance_detects_prior_decision_string_inconsistency():
    result = provenance_gate()

    assert result[
        "pass"
    ] is True

    assert result[
        "r2b_numeric_a12c_target_ruled_out"
    ] is True

    assert result[
        "r2b_decision_string_claimed_few_joule_headroom"
    ] is True

    assert result[
        "r2b_decision_string_logic_inconsistent"
    ] is True


def test_certificate_points_include_prior_bottleneck():
    points = certificate_payload_points()

    bottleneck = prior_bottleneck_point()

    distance = np.min(
        np.linalg.norm(
            points
            -
            bottleneck[
                None,
                :
            ],
            axis=1,
        )
    )

    assert distance < 1.0e-12


def test_grid_source_support_contains_many_independent_cells():
    rhos, zs, _, _ = _grid(
        0.4,
        4.0,
        -4.0,
        5.0,
    )

    indices = source_support_unknown_indices(
        rhos,
        zs,
    )

    assert len(
        indices
    ) > 20

    assert len(
        np.unique(
            indices
        )
    ) == len(
        indices
    )


def test_acceleration_bilinear_matrix_is_symmetric_and_indefinite():
    matrix = acceleration_bilinear_matrix(
        PORTAL_SCALE_EV
    )

    assert np.allclose(
        matrix,
        matrix.T,
    )

    eigenvalues = np.linalg.eigvalsh(
        matrix
    )

    assert eigenvalues[
        0
    ] < 0.0

    assert eigenvalues[
        -1
    ] > 0.0


def test_original_2p656859j_target_requires_about_3p69_response_per_joule():
    efficiency = target_efficiency_m_s2_per_j(
        A12C_REFERENCE_CAPACITY_J
    )

    assert (
        3.68
        <
        efficiency
        <
        3.70
    )


def test_capacity_classification_uses_upper_bound_in_correct_direction():
    targets = classify_capacity_targets(
        0.01
    )

    assert targets[
        "100.0"
    ][
        "ruled_out_by_pointwise_upper_bound"
    ] is True

    assert targets[
        "1000.0"
    ][
        "mathematically_allowed_by_pointwise_upper_bound"
    ] is True


def test_two_grid_spacings_are_declared():
    assert CERTIFICATE_GRID_SPACINGS_M == (
        0.125,
        0.100,
    )


def test_exact_1kev_is_frozen():
    assert PORTAL_SCALE_EV == 1000.0


def test_claim_policy_preserves_scope_and_few_joule_priority():
    result = claim_policy_gate()

    assert result[
        "few_joule_branch_priority"
    ] is True

    assert result[
        "every_axisymmetric_source_grid_cell_free"
    ] is True

    assert result[
        "grid_source_space_more_permissive_than_smooth_physical_current"
    ] is True

    assert result[
        "local_current_conservation_preserved"
    ] is True

    assert result[
        "continuous_source_space_exhausted"
    ] is False

    assert result[
        "all_possible_source_shapes_closed"
    ] is False

    assert result[
        "complete_energy_established"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "006d_replaced"
    ] is False
