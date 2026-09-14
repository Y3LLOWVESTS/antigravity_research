"""Regression tests for 032V26E1B1."""

import math

from antigravity_research.agminer.v26e1b1_quadratic_active_state_escape import (
    historical_overlap_suppression_gate,
    matched_power_activation,
    nda_family_gate,
    power_family_gate,
    quadratic_activation_gate,
    quadratic_candidate_classification,
    technical_naturalness_gate,
    v26e1b0_provenance_gate,
    v26e1b1_summary,
    wilsonian_nda_descendant,
)


def test_e1b0_provenance_closes_linear_but_not_all_v26d():
    result = v26e1b0_provenance_gate()

    assert result[
        "v26e1b0_provenance_pass"
    ] is True

    assert result[
        "linear_completion_closed"
    ] is True

    assert result[
        "all_v26d_closed"
    ] is False

    assert result[
        "new_completion_authorized"
    ] is True


def test_quadratic_active_match_has_exact_simple_rational_values():
    result = quadratic_activation_gate()

    assert result[
        "exact_quadratic_active_match"
    ] is True

    assert math.isclose(
        result[
            "eta"
        ],
        100.0 / 41.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "A_active"
        ],
        42.0 / 41.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "D_map_active"
        ],
        40.0 / 41.0,
        abs_tol=1.0e-12,
    )


def test_quadratic_preserves_active_beta_but_switches_it_off_at_origin():
    result = quadratic_activation_gate()

    assert math.isclose(
        result[
            "beta_reconstructed"
        ],
        1.0 / 21.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "beta_offstate"
        ],
        0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "A_x_offstate"
        ],
        0.0,
        abs_tol=1.0e-12,
    )

    assert result[
        "active_offstate_separation"
    ] is True


def test_quadratic_removes_tree_r5_vertex_without_margin_collapse():
    result = quadratic_activation_gate()

    assert result[
        "tree_two_scalar_matter_vertex_present"
    ] is False

    assert result[
        "r5_tree_two_scalar_vertex_absent"
    ] is True

    assert result[
        "leading_matter_scalar_leg_count"
    ] == 4

    assert result[
        "map_invertible_active"
    ] is True

    assert result[
        "field_redefinition_margin_collapse"
    ] is False

    assert math.isclose(
        result[
            "tensor_worst_relative_margin"
        ],
        146.0 / 147.0,
        abs_tol=1.0e-12,
    )


def test_power_two_three_four_all_classically_escape_linear_r5_vertex():
    result = power_family_gate()

    assert result[
        "power_count"
    ] == 3

    assert result[
        "powers"
    ] == [
        2,
        3,
        4,
    ]

    assert result[
        "all_match_active_beta"
    ] is True

    assert result[
        "all_active_maps_invertible"
    ] is True

    assert result[
        "all_remove_tree_r5_two_scalar_vertex"
    ] is True

    assert result[
        "all_tensor_margins_positive"
    ] is True

    assert result[
        "family_classical_escape_pass"
    ] is True


def test_old_v19r6_collision_only_needed_small_relative_suppression():
    result = historical_overlap_suppression_gate()

    assert result[
        "old_overlap_was_narrow"
    ] is True

    assert result[
        "maximum_relative_offstate_c1_to_reopen_old_overlap"
    ] < 1.0

    assert result[
        "maximum_relative_offstate_c1_to_reopen_old_overlap"
    ] > 0.98

    assert result[
        "exact_old_energy_boundary_transfers_to_new_completion"
    ] is False


def test_quadratic_wilsonian_nda_descendant_has_large_historical_headroom():
    result = wilsonian_nda_descendant(
        power=2
    )

    assert result[
        "wilsonian_loop_order_to_xT"
    ] == 1

    assert result[
        "nda_only"
    ] is True

    assert result[
        "exact_beta_function"
    ] is False

    assert result[
        "uv_matching_computed"
    ] is False

    assert result[
        "nda_below_old_overlap_threshold"
    ] is True

    assert result[
        "historical_overlap_reopens_under_nda_assumptions"
    ] is True

    assert result[
        "nda_relative_offstate_to_active_coupling"
    ] < 0.04

    assert result[
        "multiplicative_nda_uncertainty_headroom_before_old_overlap_closes"
    ] > 20.0


def test_higher_powers_push_wilsonian_descendant_to_higher_loop_order():
    result = nda_family_gate()

    assert result[
        "row_count"
    ] == 3

    rows = result[
        "rows"
    ]

    assert rows[
        0
    ][
        "wilsonian_loop_order_to_xT"
    ] == 1

    assert rows[
        1
    ][
        "wilsonian_loop_order_to_xT"
    ] == 2

    assert rows[
        2
    ][
        "wilsonian_loop_order_to_xT"
    ] == 3

    assert result[
        "all_tested_powers_reopen_old_overlap_under_nda_assumptions"
    ] is True

    assert result[
        "nda_is_quantum_certification"
    ] is False


def test_declared_symmetries_do_not_technically_protect_missing_xT():
    result = technical_naturalness_gate()

    assert result[
        "diffeomorphism_symmetry_allows_xT"
    ] is True

    assert result[
        "shift_symmetry_allows_xT"
    ] is True

    assert result[
        "phi_Z2_allows_xT"
    ] is True

    assert result[
        "setting_xT_coefficient_zero_increases_declared_symmetry"
    ] is False

    assert result[
        "declared_symmetry_forbids_xT_but_allows_x2T"
    ] is False

    assert result[
        "technical_naturalness_certified"
    ] is False

    assert result[
        "uv_threshold_can_generate_xT"
    ] is True


def test_quadratic_candidate_is_promising_conditional_not_model():
    result = quadratic_candidate_classification()

    assert result[
        "classical_escape_from_exact_e1b0_r5_collision"
    ] is True

    assert result[
        "same_active_beta_1_as_representative_v26d"
    ] is True

    assert result[
        "tree_r5_two_scalar_vertex_absent"
    ] is True

    assert result[
        "nda_radiative_headroom_present"
    ] is True

    assert result[
        "technical_naturalness_certified"
    ] is False

    assert result[
        "full_scalar_health_established"
    ] is False

    assert result[
        "physical_g00_cross_response_established"
    ] is False

    assert result[
        "candidate_status"
    ] == "PROMISING_CONDITIONAL_ACTIVE_STATE_COMPLETION"

    assert result[
        "physical_model"
    ] is False


def test_e1b1_summary_promotes_only_next_physical_gate():
    result = v26e1b1_summary()

    assert result[
        "decision"
    ].startswith(
        "YELLOW_PROMISING_V26E1B1_"
    )

    assert result[
        "quadratic_active_state_classical_escape"
    ] is True

    assert result[
        "quadratic_tree_r5_two_scalar_vertex_absent"
    ] is True

    assert result[
        "quadratic_nda_radiative_headroom_present"
    ] is True

    assert result[
        "technical_naturalness_certified"
    ] is False

    assert result[
        "full_static_spacelike_scalar_health_established"
    ] is False

    assert result[
        "physical_g00_cross_response_established"
    ] is False

    assert result[
        "outward_sign_established"
    ] is False

    assert result[
        "finite_payload_established"
    ] is False

    assert result[
        "minimum_required_outward_acceleration_m_s2"
    ] == 9.80665

    assert result[
        "minimum_required_true_standoff_m"
    ] == 1.0

    assert result[
        "performance_above_floor_is_favorable"
    ] is True

    assert result[
        "v26d_complete_energy_j"
    ] is None

    assert result[
        "energy_optimization_authorized"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "quadratic_candidate_promoted_to_next_physical_gate"
    ] is True

    assert result[
        "next"
    ] == (
        "032V26E1B2_QUADRATIC_ACTIVE_STATE_HEALTHY_SCALAR_"
        "PHYSICAL_G00_CROSSPROP_AND_UV_DESCENDANT_GATE"
    )
