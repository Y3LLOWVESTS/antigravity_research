"""Regression tests for 032H17A9R2."""

import math

from antigravity_research.agminer.hook17_projective_dirac_completion import (
    HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    a9r1_provenance_gate,
    all_probe_projective_completion_gate,
    clean_projected_source_gate,
    conventional_projective_dirac_literature_gate,
    conventional_vector_1plus_no_go_gate,
    h17a9r2_summary,
    projected_wheeler_action_scaffold_gate,
    projector_algebra_gate,
)


def test_a9r1_provenance_is_green_for_projective_completion():
    result = a9r1_provenance_gate()

    assert result[
        "a9r1_provenance_pass"
    ] is True

    assert result[
        "unmodified_wheeler_closed"
    ] is True

    assert result[
        "clean_pole_preserved"
    ] is True

    assert result[
        "projective_completion_open"
    ] is True


def test_conventional_projective_dirac_is_vector_irrep_matter_class():
    result = conventional_projective_dirac_literature_gate()

    assert result[
        "projectively_invariant"
    ] is True

    assert result[
        "direct_nonmetricity_q_vector_source"
    ] is True

    assert result[
        "direct_nonmetricity_qhat_vector_source"
    ] is True

    assert result[
        "direct_pure_tensor_nonmetricity_source"
    ] is False

    assert result[
        "torsion_free_ps_axial_torsion_available"
    ] is False


def test_projective_projector_is_idempotent_and_local():
    result = projector_algebra_gate()

    assert result[
        "projector_is_local_algebraic"
    ] is True

    assert result[
        "inverse_derivative_used"
    ] is False

    assert result[
        "inverse_momentum_used"
    ] is False

    assert result[
        "projector_idempotent"
    ] is True

    assert result[
        "projector_idempotence_error"
    ] <= 1.0e-12


def test_projector_annihilates_gauge_image_and_trace():
    result = projector_algebra_gate()

    assert result[
        "projector_annihilates_projective_gauge_image"
    ] is True

    assert result[
        "projector_output_projective_trace_zero"
    ] is True

    assert result[
        "projector_gauge_annihilation_error"
    ] <= 1.0e-12

    assert result[
        "projector_output_trace_norm"
    ] <= 1.0e-12


def test_projector_is_self_adjoint_and_preserves_tf_symmetry():
    result = projector_algebra_gate()

    assert result[
        "projector_self_adjoint"
    ] is True

    assert result[
        "projector_preserves_first_third_symmetry"
    ] is True

    assert result[
        "projector_self_adjoint_error"
    ] <= 1.0e-12


def test_single_action_projector_makes_all_16_wheeler_probes_projective():
    result = all_probe_projective_completion_gate()

    assert result[
        "probe_count"
    ] == 16

    assert result[
        "all_16_projected_wheeler_probes_projective_compatible"
    ] is True

    assert result[
        "single_fixed_projector_used_for_all_sources"
    ] is True

    assert result[
        "state_by_state_parameter_fitting_used"
    ] is False

    assert result[
        "maximum_projected_trace_norm"
    ] <= 1.0e-11


def test_clean_a9_source_is_exactly_unchanged_by_projective_completion():
    result = clean_projected_source_gate()

    assert result[
        "clean_source_already_projective_traceless"
    ] is True

    assert result[
        "clean_nonzero_components_have_all_distinct_indices"
    ] is True

    assert result[
        "projective_completion_leaves_clean_source_unchanged"
    ] is True

    assert math.isclose(
        result[
            "projected_minus_clean_norm"
        ],
        0.0,
        abs_tol=1.0e-12,
    )


def test_clean_a9_exact_pole_numerator_survives_completion():
    result = clean_projected_source_gate()

    assert result[
        "projected_clean_1plus_pole_numerator_nonzero"
    ] is True

    assert result[
        "a9_numerator_preserved_exactly"
    ] is True

    assert math.isclose(
        result[
            "projected_clean_1plus_pole_numerator"
        ],
        1.44,
        abs_tol=1.0e-11,
    )


def test_conventional_projective_vector_source_class_has_zero_physical_1plus():
    result = conventional_vector_1plus_no_go_gate()

    assert result[
        "vector_basis_count"
    ] == 4

    assert result[
        "most_general_parity_even_tf_projective_vector_source_tested"
    ] is True

    assert result[
        "all_vector_basis_physical_1plus_currents_zero"
    ] is True

    assert result[
        "standard_projective_lorentz_dirac_vector_class_1plus_closed"
    ] is True

    assert result[
        "maximum_vector_basis_1plus_numerator"
    ] <= 1.0e-12


def test_vector_no_go_does_not_close_clean_tensor_source():
    result = conventional_vector_1plus_no_go_gate()

    assert result[
        "clean_a9_tensor_source_closed"
    ] is False

    clean = clean_projected_source_gate()

    assert clean[
        "projected_clean_1plus_pole_numerator_nonzero"
    ] is True


def test_declared_projected_wheeler_action_scaffold_is_partial_green():
    result = projected_wheeler_action_scaffold_gate()

    assert result[
        "projector_local"
    ] is True

    assert result[
        "projector_self_adjoint"
    ] is True

    assert result[
        "all_wheeler_probe_sources_projective_after_variation"
    ] is True

    assert result[
        "clean_source_unchanged"
    ] is True

    assert result[
        "clean_1plus_numerator_preserved"
    ] is True

    assert result[
        "linearized_local_projective_matter_action_scaffold_exists"
    ] is True

    assert result[
        "nonlinear_covariant_world_spinor_lift_established"
    ] is False

    assert result[
        "same_action_hook17_complete"
    ] is False


def test_a9r2_summary_preserves_claim_and_energy_discipline():
    result = h17a9r2_summary()

    assert result[
        "partial_green"
    ] is True

    assert result[
        "decision"
    ].startswith(
        "GREEN_PARTIAL_A9R2_"
    )

    assert result[
        "standard_projective_lorentz_dirac_vector_class_1plus_closed"
    ] is True

    assert result[
        "linearized_local_projective_matter_action_scaffold_exists"
    ] is True

    assert result[
        "clean_a9_1plus_pole_numerator_preserved"
    ] is True

    assert result[
        "nonlinear_covariant_world_spinor_lift_established"
    ] is False

    assert result[
        "same_action_hook17_complete"
    ] is False

    assert result[
        "hook17_closed"
    ] is False

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

    assert result[
        "h17b_authorized"
    ] is False

    assert result[
        "next"
    ] == (
        "032H17A9R3_COVARIANT_PROJECTIVE_WORLD_SPINOR_"
        "ACTION_AND_METRIC_STRESS_GATE"
    )
