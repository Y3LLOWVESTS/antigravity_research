"""Regression tests for 032H17A9R3."""

import math

from antigravity_research.agminer.hook17_covariant_projective_stress_protection import (
    HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    a9r2_provenance_gate,
    case_i_protection_audit,
    clean_covariant_source_gate,
    clean_same_action_diffeomorphism_ward_gate,
    covariant_projector_geometry_gate,
    covariant_projector_gl_equivariance_gate,
    flat_covariant_projector_regression_gate,
    h17a9r3_summary,
    same_action_clean_metric_stress_gate,
)


def test_a9r2_provenance_is_green():
    result = a9r2_provenance_gate()

    assert result[
        "a9r2_provenance_pass"
    ] is True

    assert result[
        "linearized_projective_scaffold"
    ] is True

    assert result[
        "all_16_sources_projective"
    ] is True

    assert result[
        "clean_pole_preserved"
    ] is True


def test_covariant_projector_works_on_nonflat_lorentzian_metric():
    result = covariant_projector_geometry_gate()

    assert result[
        "lorentzian_metric"
    ] is True

    assert result[
        "metric_signature_negative_positive"
    ] == [
        1,
        3,
    ]

    assert result[
        "covariant_trace_zero"
    ] is True

    assert result[
        "covariant_idempotent"
    ] is True

    assert result[
        "covariant_gauge_image_annihilated"
    ] is True

    assert result[
        "covariant_tf_symmetry_preserved"
    ] is True

    assert result[
        "covariant_self_adjoint"
    ] is True


def test_covariant_projector_is_gl4_equivariant():
    result = covariant_projector_gl_equivariance_gate()

    assert result[
        "basis_change_invertible"
    ] is True

    assert result[
        "gl4_equivariance_pass"
    ] is True

    assert result[
        "gl4_equivariance_error"
    ] <= 1.0e-11


def test_covariant_projector_reduces_to_a9r2_flat_projector():
    result = flat_covariant_projector_regression_gate()

    assert result[
        "flat_covariant_projector_matches_a9r2"
    ] is True

    assert result[
        "flat_reduction_error"
    ] <= 1.0e-11


def test_clean_source_and_exact_1plus_pole_survive_covariant_lift():
    result = clean_covariant_source_gate()

    assert result[
        "clean_source_unchanged"
    ] is True

    assert result[
        "exact_1plus_pole_numerator_nonzero"
    ] is True

    assert result[
        "a9_numerator_preserved"
    ] is True

    assert math.isclose(
        result[
            "exact_1plus_pole_numerator"
        ],
        1.44,
        abs_tol=1.0e-11,
    )


def test_same_action_lc_metric_variation_matches_unique_a9r1_sigma():
    result = same_action_clean_metric_stress_gate()

    assert result[
        "same_action_linearized_clean_metric_stress_matches_a9r1"
    ] is True

    assert math.isclose(
        result[
            "action_derived_s032"
        ],
        4.0,
        abs_tol=1.0e-10,
    )

    assert math.isclose(
        result[
            "action_derived_s302"
        ],
        4.0,
        abs_tol=1.0e-10,
    )

    assert result[
        "maximum_other_action_derived_coefficient"
    ] <= 1.0e-10

    assert result[
        "action_vs_a9r1_sigma_maximum_difference"
    ] <= 1.0e-10


def test_action_derived_clean_sigma_satisfies_linearized_diffeo_ward():
    result = clean_same_action_diffeomorphism_ward_gate()

    assert result[
        "witness_count"
    ] == 4

    assert result[
        "all_clean_same_action_linearized_diffeo_witnesses_pass"
    ] is True

    assert result[
        "maximum_clean_same_action_diffeo_residual"
    ] <= 1.0e-10

    assert result[
        "full_nonlinear_matter_noether_identity_established"
    ] is False


def test_case_i_health_relations_are_two_independent_extra_conditions():
    result = case_i_protection_audit()

    assert result[
        "case_i_relations_exact"
    ] is True

    assert result[
        "case_i_constraint_jacobian_rank"
    ] == 2

    assert result[
        "case_i_health_surface_codimension_in_declared_coordinates"
    ] == 2

    assert result[
        "projective_symmetry_exists_before_case_i_relations"
    ] is True

    assert result[
        "projective_symmetry_alone_enforces_case_i_relations"
    ] is False


def test_case_i_suppression_is_not_new_gauge_null_in_reduced_blocks():
    result = case_i_protection_audit()

    assert math.isclose(
        result[
            "two_minus_case_i_q2_coefficient"
        ],
        0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "two_minus_case_i_constant_operator"
        ],
        0.5,
    )

    assert math.isclose(
        result[
            "one_minus_case_i_q2_determinant_factor"
        ],
        0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "one_minus_case_i_constant_determinant_term"
        ],
        -96.0 / 25.0,
    )

    assert result[
        "case_i_removes_unwanted_momentum_dependence"
    ] is True

    assert result[
        "case_i_reduced_unwanted_blocks_remain_nondegenerate"
    ] is True

    assert result[
        "case_i_mode_removal_established_as_new_gauge_null_direction"
    ] is False


def test_a9r3_blocks_current_ps_case_i_and_authorizes_v26d_fallback():
    result = h17a9r3_summary()

    assert result[
        "decision"
    ].startswith(
        "YELLOW_BLOCKED_A9R3_"
    )

    assert result[
        "covariant_geometric_projector_established"
    ] is True

    assert result[
        "same_action_linearized_clean_metric_stress_derived"
    ] is True

    assert result[
        "same_action_clean_linearized_diffeomorphism_ward_pass"
    ] is True

    assert result[
        "geometric_and_clean_linearized_noether_partial_green"
    ] is True

    assert result[
        "case_i_technical_naturalness_gate_pass"
    ] is False

    assert result[
        "current_ps_case_i_candidate_promotion_authorized"
    ] is False

    assert result[
        "current_ps_case_i_branch_status"
    ] == "BLOCKED_TECHNICAL_NATURALNESS"

    assert result[
        "unknown_protected_case_i_completion_globally_closed"
    ] is False

    assert result[
        "hook17_closed"
    ] is False

    assert result[
        "v26d_resume_authorized"
    ] is True

    assert result[
        "next"
    ] == "032V26D_RESUME_PROTECTED_CT1_DHOST_KMM"

    assert math.isclose(
        result[
            "hook17_reference_capacity_rp1e12_j"
        ],
        HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    )

    assert result[
        "hook17_complete_energy_j"
    ] is None

    assert result[
        "energy_optimization_authorized"
    ] is False
