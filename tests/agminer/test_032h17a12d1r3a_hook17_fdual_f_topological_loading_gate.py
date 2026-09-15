"""Regressions for 032H17A12D1R3A topological F·Fdual rescue gate."""

from __future__ import annotations

import math

from antigravity_research.agminer.hook17_fdual_f_topological_loading_gate import (
    A12C_REFERENCE_FIELD_ENERGY_J,
    BRANCH,
    affine_bulk_cancellation_theorem,
    health_and_ward_gate,
    ideal_capacity_equivalence_gate,
    interface_gate,
    loading_structure_gate,
    parity_gate,
    planar_interface_penalty,
    provenance_gate,
    rescue_portal_atlas,
    r3a_summary,
    same_action_variation_gate,
)


def test_branch_name_is_frozen():
    assert BRANCH == "032H17A12D1R3A"


def test_provenance_preserves_r2b1_scoped_closeout_and_a12_backbone():
    result = provenance_gate()

    assert result[
        "pass"
    ] is True

    assert result[
        "r2b1_few_joule_source_shaping_ruled_out"
    ] is True

    assert result[
        "a12b_carrier_preserved"
    ] is True

    assert result[
        "a12c_mechanism_preserved"
    ] is True


def test_same_action_variation_has_factor_two_and_bianchi_reduction():
    result = same_action_variation_gate()

    assert "2/M^4" in result[
        "delta_sigma"
    ]

    assert result[
        "bianchi_identity"
    ] == "nabla_m Fdual^(mn)=0"

    assert result[
        "leading_constant_trace_bulk_loading_zero"
    ] is True


def test_exact_constant_trace_has_only_nonlinear_residual_not_exact_zero():
    result = same_action_variation_gate()

    assert result[
        "exact_constant_trace_bulk_loading_zero"
    ] is False

    assert "exp(4*sigma)" in result[
        "exact_residual_origin"
    ]


def test_affine_linear_p_is_unique_nontrivial_local_bulk_cancellation():
    result = affine_bulk_cancellation_theorem()

    assert result[
        "linear_P_unique_nontrivial_local_fP_bulk_cancellation"
    ] is True

    assert result[
        "general_solution"
    ] == "f(P)=a+b*P"

    assert result[
        "P_squared_preserves_bulk_cancellation"
    ] is False


def test_nontrivial_parity_even_analytic_single_vector_fP_conflicts_with_affine_cancellation():
    theorem = affine_bulk_cancellation_theorem()

    parity = parity_gate()

    assert theorem[
        "nontrivial_analytic_parity_even_fP_can_be_affine"
    ] is False

    assert parity[
        "parity_even_single_vector_and_exact_leading_topological_cancellation_compatible_without_extra_structure"
    ] is False


def test_ideal_mirror_field_exactly_preserves_a12c_sigma_and_energy():
    result = ideal_capacity_equivalence_gate()

    assert math.isclose(
        result[
            "mirror_sigma_over_a12c_sigma"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    assert math.isclose(
        result[
            "mirror_canonical_energy_over_a12c_energy"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    assert result[
        "ideal_capacity_exactly_equal_to_a12c"
    ] is True

    assert math.isclose(
        result[
            "ideal_mixed_EB_field_energy_j"
        ],
        A12C_REFERENCE_FIELD_ENERGY_J,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_mirror_field_is_only_locally_integrable_in_payload_not_global_source():
    result = ideal_capacity_equivalence_gate()

    assert result[
        "payload_entirely_outside_current_support"
    ] is True

    assert result[
        "local_electrostatic_mirror_integrable_in_payload_region"
    ] is True

    assert result[
        "global_electrostatic_mirror_integrable_through_current_source"
    ] is False

    assert result[
        "global_mirror_field_solution_established"
    ] is False


def test_topological_uniform_bulk_residual_is_tiny_at_a12c_sigma():
    result = loading_structure_gate()

    assert result[
        "f2_peak_bulk_loading_epsilon"
    ] > 1.0e4

    assert result[
        "exact_uniform_bulk_nonlinear_principal_proxy_peak"
    ] < 1.0e-8

    assert result[
        "nonlinear_bulk_proxy_pass"
    ] is True

    assert result[
        "f2_bulk_vs_topological_residual_suppression_factor"
    ] > 1.0e12


def test_interface_beta_remains_large_even_when_bulk_term_cancels():
    result = loading_structure_gate()

    assert result[
        "topological_beta_peak_magnitude"
    ] > 1.0e4

    assert result[
        "density_gradient_coefficient_remains_large"
    ] is True

    assert result[
        "dominant_loaded_problem_changes_from_bulk_to_interface"
    ] is True


def test_planar_interface_favorable_penalty_is_below_unfavorable_penalty():
    result = planar_interface_penalty(
        1000.0
    )

    assert result[
        "favorable_energy_density_factor"
    ] > 0.0

    assert (
        result[
            "favorable_energy_density_factor"
        ]
        <
        result[
            "unfavorable_energy_density_factor"
        ]
    )


def test_positive_sigma_nonrelativistic_matter_selects_favorable_interface_sign():
    result = interface_gate()

    assert result[
        "positive_sigma_and_nonrelativistic_T_select_favorable_sign"
    ] is True

    assert result[
        "heuristic_global_energy_is_rigorous_bound"
    ] is False

    assert result[
        "full_interface_loaded_BVP_required"
    ] is True


def test_parity_cp_obstruction_is_real_but_not_mathematical_inconsistency():
    result = parity_gate()

    assert result[
        "ordinary_vector_P_is_parity_odd"
    ] is True

    assert result[
        "ordinary_vector_P_is_CP_odd"
    ] is True

    assert result[
        "bare_linear_P_metric_preserves_parity"
    ] is False

    assert result[
        "parity_problem_is_mathematical_inconsistency"
    ] is False

    assert result[
        "repair_requires_additional_parity_odd_structure"
    ] is True


def test_gauge_ward_and_derivative_order_survive():
    result = health_and_ward_gate()

    assert result[
        "portal_is_gauge_invariant"
    ] is True

    assert result[
        "matter_induced_current_identically_conserved"
    ] is True

    assert result[
        "off_state_F_zero_implies_portal_source_zero"
    ] is True

    assert result[
        "field_equations_second_order"
    ] is True

    assert result[
        "higher_time_derivative_ostrogradsky_from_portal"
    ] is False


def test_rescue_atlas_ranks_linear_p_then_parity_repairs_not_more_f2_shaping():
    atlas = rescue_portal_atlas()

    assert atlas[
        0
    ][
        "portal"
    ] == "SINGLE_VECTOR_LINEAR_P_MECHANISM_DIAGNOSTIC"

    assert atlas[
        1
    ][
        "portal"
    ] == "PSEUDOSCALAR_COMPENSATED_LINEAR_P"

    assert atlas[
        2
    ][
        "portal"
    ] == "VECTOR_AXIAL_CROSS_TOPOLOGICAL"

    assert "CLOSED_SCOPED" in atlas[
        -1
    ][
        "status"
    ]


def test_summary_authorizes_r3b_but_not_full_loaded_bvp_or_physical_claim():
    result = r3a_summary()

    assert result[
        "structural_rescue_survives_cheap_gate"
    ] is True

    assert result[
        "r3b_authorized"
    ] is True

    assert result[
        "full_loaded_EB_BVP_authorized_immediately"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False

    assert result[
        "006d_replaced"
    ] is False

    assert result[
        "hook17_closed"
    ] is False
