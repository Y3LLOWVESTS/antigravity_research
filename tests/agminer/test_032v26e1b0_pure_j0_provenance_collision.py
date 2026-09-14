"""Regression tests for 032V26E1B0."""

import math

from antigravity_research.agminer.v26e1b0_pure_j0_provenance_collision import (
    canonical_rescaling_gate,
    identical_v17_completion_gate,
    inherited_v19r6_failure_memory,
    inverse_conformal_series_gate,
    novelty_requirements_gate,
    offstate_two_scalar_force_gate,
    pure_j0_operator_gate,
    source_operator_provenance_gate,
    v17_coefficient_match_gate,
    v26e1a_provenance_gate,
    v26e1b0_summary,
)


def test_e1a_exact_nonsingular_map_is_required_provenance():
    result = v26e1a_provenance_gate()

    assert result[
        "v26e1a_provenance_pass"
    ] is True

    assert result[
        "eh_equivalent"
    ] is True

    assert result[
        "map_invertible"
    ] is True

    assert math.isclose(
        result[
            "map_jacobian_margin"
        ],
        1.0,
        abs_tol=1.0e-12,
    )

    assert result[
        "near_singular"
    ] is False


def test_inverse_conformal_metric_generates_pure_trace_operator():
    result = inverse_conformal_series_gate(
        kappa=0.5,
    )

    assert math.isclose(
        result[
            "linear_metric_coefficient"
        ],
        -0.5,
        abs_tol=1.0e-12,
    )

    assert result[
        "leading_metric_deformation_pure_conformal"
    ] is True

    assert result[
        "leading_metric_deformation_contains_j2"
    ] is False

    assert result[
        "leading_matter_operator_pure_trace_j0"
    ] is True


def test_metric_coefficient_magnitude_maps_to_v17_c1_by_factor_two():
    result = v17_coefficient_match_gate(
        kappa=0.5,
    )

    assert result[
        "metric_coefficient_magnitude_match"
    ] is True

    assert math.isclose(
        result[
            "v17_equivalent_abs_c1"
        ],
        0.25,
        abs_tol=1.0e-12,
    )

    assert result[
        "sign_translation_required"
    ] is True

    assert result[
        "offstate_force_depends_on_c1_squared"
    ] is True


def test_v26d_leading_matter_operator_collides_with_pure_j0_class():
    result = pure_j0_operator_gate()

    assert result[
        "ordinary_matter_universal"
    ] is True

    assert result[
        "leading_operator_j0"
    ] is True

    assert result[
        "independent_j2_generated_at_same_order"
    ] is False

    assert result[
        "v17_v19_low_energy_operator_class_collision"
    ] is True


def test_v26d_hidden_source_is_same_derivative_axial_operator_class():
    result = source_operator_provenance_gate()

    assert result[
        "v26d_derivative_axial_current_operator"
    ] is True

    assert result[
        "same_hidden_source_operator_class"
    ] is True

    assert result[
        "same_microscopic_source_state_established"
    ] is False

    assert result[
        "same_source_energy_functional_established"
    ] is False


def test_r5_two_scalar_force_is_nonzero_and_sign_even():
    result = offstate_two_scalar_force_gate()

    assert result[
        "coefficient_reconstructed"
    ] is True

    assert result[
        "trace_pair_force_coefficient"
    ] > 0.0

    assert result[
        "force_requires_classical_background_X"
    ] is False

    assert result[
        "force_is_even_under_c1_sign_flip"
    ] is True

    assert result[
        "canonical_unscreened_pure_j0_has_r5_type_quantum_descendant"
    ] is True


def test_wavefunction_rescaling_does_not_remove_c1_f2_invariant():
    result = canonical_rescaling_gate()

    assert result[
        "c1_f2_invariant"
    ] is True

    assert result[
        "relative_error"
    ] <= 1.0e-12

    assert result[
        "wavefunction_rescaling_alone_evades_failure_memory"
    ] is False


def test_v19r6_failure_memory_is_scoped_not_global():
    result = inherited_v19r6_failure_memory()

    assert result[
        "empirical_energy_overlap_exists"
    ] is False

    assert result[
        "tested_v17_hidden_axial_pure_j0_implementation_closed"
    ] is True

    assert result[
        "all_kinetic_conformal_theories_closed"
    ] is False

    assert result[
        "exact_r6_energy_boundary_transfers_to_arbitrary_v26d_source"
    ] is False

    assert result[
        "empirical_metric_min_ev"
    ] > result[
        "strict_energy_metric_max_ev"
    ]


def test_identical_v17_completion_closes_without_closing_arbitrary_v26d():
    result = identical_v17_completion_gate()

    assert result[
        "leading_matter_operator_class_matches_v17_v19"
    ] is True

    assert result[
        "hidden_source_operator_class_matches_v17_v19"
    ] is True

    assert result[
        "exact_v17_equivalent_completion_closed"
    ] is True

    assert result[
        "arbitrary_v26d_source_closed"
    ] is False

    assert result[
        "arbitrary_v26d_lower_derivative_scalar_sector_closed"
    ] is False


def test_e1b0_redirects_only_to_genuinely_new_completion_physics():
    novelty = novelty_requirements_gate()

    assert novelty[
        "plain_canonical_pure_j0_recomputation_counts_as_new_physics"
    ] is False

    assert novelty[
        "new_route_must_recheck_r5_material_force"
    ] is True

    assert novelty[
        "new_route_must_hit_at_least_1g_at_1m"
    ] is True

    result = v26e1b0_summary()

    assert result[
        "decision"
    ].startswith(
        "RED_SCOPED_V26E1B0_"
    )

    assert result[
        "v17_v19_operator_class_collision"
    ] is True

    assert result[
        "exact_v17_equivalent_completion_closed"
    ] is True

    assert result[
        "all_v26d_completions_globally_closed"
    ] is False

    assert result[
        "plain_canonical_e1b_crossprop_recomputation_as_new_candidate_authorized"
    ] is False

    assert result[
        "genuinely_new_v26d_completion_rerank_authorized"
    ] is True

    assert result[
        "physical_g00_cross_response_established"
    ] is False

    assert result[
        "v26d_complete_energy_j"
    ] is None

    assert result[
        "energy_optimization_authorized"
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
        "next"
    ] == (
        "032V26E1B1_PROTECTED_ACTIVE_STATE_SCALAR_"
        "COMPLETION_RERANK_GATE"
    )
