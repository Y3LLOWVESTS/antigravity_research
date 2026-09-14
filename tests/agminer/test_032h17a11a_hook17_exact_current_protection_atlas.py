"""Regressions for 032H17A11A."""

from __future__ import annotations

from antigravity_research.agminer.hook17_exact_current_protection_atlas import (
    em_like_exact_current_gminus2_gate,
    f2_provenance_gate,
    h17a11a_summary,
    neutral_ordinary_vector_current_theorem,
    optimistic_energy_coupling_floor,
    pauli_derivative_current_gate,
    pauli_source_shape_identity,
    perturbative_heavy_radial_higgs_gate,
)


def test_f2_red_naturalness_and_strict_payload_green_are_preserved():
    result = f2_provenance_gate()

    assert result[
        "pass"
    ] is True

    assert result[
        "strict_reduced_eft_payload_survives"
    ] is True

    assert result[
        "current_wheeler_marzo_realization_blocked"
    ] is True

    assert result[
        "hook17_open"
    ] is True


def test_incomplete_energy_floor_requires_nontrivial_source_coupling():
    result = optimistic_energy_coupling_floor()

    assert (
        4.9e-4
        <
        result[
            "minimum_effective_constituent_coupling_for_partial_sub10mj"
        ]
        <
        5.1e-4
    )

    assert result[
        "floor_is_optimistic"
    ] is True

    assert result[
        "complete_energy_established"
    ] is False


def test_simple_heavy_radial_perturbative_higgs_has_no_energy_overlap():
    result = perturbative_heavy_radial_higgs_gate()

    assert (
        result[
            "maximum_g_with_perturbative_radial_at_or_above_electron_threshold"
        ]
        <
        2.0e-12
    )

    assert (
        result[
            "energy_to_higgs_coupling_gap"
        ]
        >
        2.0e8
    )

    assert result[
        "heavy_radial_energy_overlap_exists"
    ] is False

    assert result[
        "simple_perturbative_heavy_radial_higgs_closed"
    ] is True


def test_higgs_closeout_is_scoped_not_global():
    result = perturbative_heavy_radial_higgs_gate()

    assert result[
        "light_radial_higgs_completion_closed"
    ] is False

    assert result[
        "strongly_coupled_higgs_completion_closed"
    ] is False

    assert result[
        "composite_higgs_completion_closed"
    ] is False


def test_a10f1_source_shape_is_exact_curl_of_compact_magnetization():
    result = pauli_source_shape_identity()

    assert result[
        "source_shape_identity_pass"
    ] is True

    assert result[
        "derivative_current_identically_conserved"
    ] is True


def test_dimension5_pauli_exact_current_has_no_energy_eft_overlap():
    result = pauli_derivative_current_gate()

    assert (
        result[
            "optimistic_effective_g_max"
        ]
        <
        4.0e-13
    )

    assert (
        result[
            "energy_to_pauli_coupling_gap"
        ]
        >
        1.0e9
    )

    assert result[
        "energy_eft_overlap_exists"
    ] is False

    assert result[
        "simple_dimension5_pauli_current_valid_through_electron_threshold_closed"
    ] is True

    assert result[
        "explicit_uv_completion_below_electron_threshold_closed"
    ] is False


def test_arbitrary_neutral_matter_silence_forces_em_like_epn_charge():
    result = neutral_ordinary_vector_current_theorem()

    assert result[
        "q_n_zero"
    ] is True

    assert result[
        "q_p_equals_minus_q_e"
    ] is True

    assert result[
        "ordinary_e_p_n_solution_dimension"
    ] == 1

    assert result[
        "solution_em_like_up_to_overall_normalization"
    ] is True


def test_rubidium_electron_gminus2_bound_is_far_below_energy_need():
    result = em_like_exact_current_gminus2_gate()

    assert (
        2.2e-5
        <
        result[
            "epsilon_rb_95"
        ]
        <
        2.4e-5
    )

    assert (
        result[
            "energy_to_rb_bound_gap"
        ]
        >
        70.0
    )

    assert result[
        "rb_energy_overlap_exists"
    ] is False


def test_cesium_electron_gminus2_bound_is_even_stronger():
    result = em_like_exact_current_gminus2_gate()

    assert (
        8.0e-6
        <
        result[
            "epsilon_cs_95"
        ]
        <
        9.5e-6
    )

    assert (
        result[
            "energy_to_cs_bound_gap"
        ]
        >
        180.0
    )

    assert result[
        "cs_energy_overlap_exists"
    ] is False


def test_em_like_exact_current_rescue_is_closed_but_hidden_currents_are_not():
    result = em_like_exact_current_gminus2_gate()

    assert result[
        "rb_cs_treated_as_alternative_inputs_not_combined"
    ] is True

    assert result[
        "minimal_em_like_exact_current_rescue_closed_by_electron_gminus2"
    ] is True

    assert result[
        "source_only_hidden_current_closed"
    ] is False

    assert result[
        "nonstandard_noether_current_closed"
    ] is False


def test_a11a_closes_easy_repairs_and_promotes_new_k2_gate_only():
    result = h17a11a_summary()

    assert result[
        "three_minimal_source_protection_repairs_closed"
    ] is True

    assert result[
        "ordinary_dirac_wheeler_marzo_realization_remains_closed"
    ] is True

    assert result[
        "all_higgsed_noether_completions_closed"
    ] is False

    assert result[
        "all_exact_conserved_current_completions_closed"
    ] is False

    assert result[
        "k3_historical_direct_clean_source_route_reopened"
    ] is False

    assert result[
        "k2_source_ward_projector_overlap_established"
    ] is False

    assert result[
        "hook17_closed"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False

    assert result[
        "expensive_payload_run_authorized"
    ] is False

    assert result[
        "next"
    ] == (
        "032H17A11B_K2_MASSLESS_TORSION_VECTOR_"
        "ENGINEERED_DIRAC_EXACT_SOURCE_WARD_PROJECTOR_GATE"
    )
