"""Regressions for 032H17A12B concurrent-IW enhanced-U(1) source gate."""

from __future__ import annotations

from antigravity_research.agminer.hook17_concurrent_iw_exact_source import (
    a12a_provenance_gate,
    concurrent_c4_exact_reduction,
    enhanced_u1_symmetry_gate,
    h17a12b_summary,
    rational_corridor_witness,
)


def test_a12a_provenance_is_exact():
    result = a12a_provenance_gate()

    assert result["pass"] is True

    assert result["a12a_next"] == (
        "032H17A12B_FULL_SAME_ACTION_IW_EXACT_SOURCE_PROTECTION_GATE"
    )


def test_exact_elimination_finds_axial_decoupling_and_massless_conditions():
    result = concurrent_c4_exact_reduction()

    assert result["nondynamical_hessian_determinant"] == (
        "4*b2*b4 - b6**2"
    )

    assert result["axial_decoupling_condition"] == (
        "2*b3*b4-b5*b6 = 0"
    )

    assert result["massless_condition_after_axial_decoupling"] == (
        "4*b1*b4-b5**2 = 0"
    )

    assert result["corridor_w_t_hat"] == "0"
    assert result["corridor_mass_coefficient"] == "0"


def test_exact_corridor_sources_only_the_vector_noether_current():
    result = concurrent_c4_exact_reduction()

    assert result["corridor_w_zc"] == "b5/(2*b4)"

    assert result["corridor_effective_source"] == (
        "J_N*(2*b4 - b5)/(2*b4)"
    )

    assert result["null_vector_identity_pass"] is True


def test_projective_aligned_c_equal_one_is_a_source_cancellation_boundary():
    result = concurrent_c4_exact_reduction()

    assert result["projective_aligned_c1_source_cancels"] is True
    assert result["generic_c_not_1_source_can_be_nonzero"] is True


def test_projective_plus_iw_gradient_reconstructs_massless_gauge_direction():
    result = enhanced_u1_symmetry_gate()

    assert result["delta_q_coefficient"] == "1"
    assert result["delta_zc_coefficient"] == "-c"
    assert result["delta_zep_coefficient"] == "1 - c"
    assert result["delta_t_hat_coefficient"] == "0"


def test_beta_zero_turns_jn_into_exact_massive_dirac_vector_current():
    result = enhanced_u1_symmetry_gate()

    assert result["beta_nm"] == 0

    assert result[
        "massive_dirac_vector_current_classically_conserved"
    ] is True

    assert result[
        "isolated_vectorlike_dirac_current_has_axial_mass_divergence_problem"
    ] is False


def test_dirac_phase_exactly_cancels_geometric_source_variation():
    result = enhanced_u1_symmetry_gate()

    assert result["matter_variation_cancels_exactly"] is True
    assert result["fermion_mass_term_phase_invariant"] is True

    assert result[
        "classical_same_action_gauge_completion_in_declared_subfamily"
    ] is True


def test_enhanced_u1_forbids_the_holst_square_on_generic_c_not_one_branch():
    result = enhanced_u1_symmetry_gate()

    assert result[
        "holst_square_allowed_by_generic_c_not_1_enhanced_u1"
    ] is False

    assert result[
        "enhanced_u1_forbids_holst_square_for_generic_c_not_1"
    ] is True


def test_rational_witness_is_far_from_nondynamical_singularity():
    result = rational_corridor_witness()

    assert result["c"] == "1/2"

    assert result["nondynamical_hessian_determinant"] == "4"

    assert result["nondynamical_hessian_eigenvalues"] == [
        "2",
        "2",
    ]

    assert result["positive_nondynamical_margins"] is True
    assert result["gain_from_near_singular_mixing"] is False


def test_rational_witness_has_one_exact_gauge_null_and_nonzero_source():
    result = rational_corridor_witness()

    assert result["full_vector_mass_hessian_eigenvalues"] == [
        "0",
        "2",
        "5/2",
    ]

    assert result["gauge_null_residual"] == [
        "0",
        "0",
        "0",
    ]

    assert result["effective_j_n_fraction"] == "1/2"

    assert result[
        "masslessness_is_exact_symmetry_null_not_small_eigenvalue"
    ] is True


def test_a12b_promotes_only_to_canonical_source_and_empirical_gate():
    result = h17a12b_summary()

    assert result[
        "classical_protected_same_action_massless_source_corridor_exists"
    ] is True

    assert result["ultralight_proca_mass_required"] is False

    assert result[
        "masslessness_protected_by_declared_exact_gauge_symmetry_classically"
    ] is True

    assert result[
        "exact_massive_dirac_vector_noether_current_available_classically"
    ] is True

    assert result["near_singular_gain_used"] is False

    assert result[
        "canonical_source_empirical_gate_authorized"
    ] is True

    assert result["canonical_source_normalization_established"] is False
    assert result["full_standard_model_anomaly_free_embedding_established"] is False
    assert result["neutral_payload_direct_force_silence_established"] is False
    assert result["empirical_consistency_established"] is False

    assert result["metric_gate_authorized"] is False
    assert result["payload_gate_authorized"] is False
    assert result["complete_energy_optimization_authorized"] is False

    assert result["hook17_closed"] is False
    assert result["physical_antigravity_model_found"] is False
    assert result["certified_sub10mj_model_found"] is False

    assert result["decision"].startswith(
        "GREEN_SCOPED_A12B_CONCURRENT_IW_ENHANCED_U1_"
    )

    assert result["next"] == (
        "032H17A12C_CONCURRENT_U1_CANONICAL_SOURCE_CHARGE_"
        "ANOMALY_PAYLOAD_SILENCE_EMPIRICAL_GATE"
    )
