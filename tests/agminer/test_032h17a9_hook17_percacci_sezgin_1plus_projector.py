"""Regression tests for 032H17A9."""

import math

import numpy as np

from antigravity_research.agminer.hook17_percacci_sezgin_1plus_projector import (
    HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    a8_provenance_gate,
    diffeomorphism_ward_gate,
    exact_ps_1plus_pole_source_gate,
    h17a9_summary,
    percacci_sezgin_case_i_gate,
    projected_projective_trace_gate,
    torsion_free_projection_identity_gate,
    torsion_free_ps_source,
    torsion_free_source_gate,
    wheeler_ps_source_map_gate,
    wheeler_to_ps_raw_source,
)


def test_a8_provenance_is_green():
    result = a8_provenance_gate()

    assert result["a8_provenance_pass"] is True
    assert result["projective_trace_prefilter_pass"] is True
    assert result["clean_1plus_nonzero"] is True
    assert result["exact_1plus_source_match_authorized"] is True


def test_percacci_sezgin_case_i_is_healthy():
    result = percacci_sezgin_case_i_gate()

    assert result["case_i_relations_pass"] is True

    assert math.isclose(
        result["m_plus_squared"],
        9.0 / 50.0,
    )

    assert math.isclose(
        result["r_plus"],
        9.0 / 25.0,
    )

    assert result["massive_1plus_tachyon_free"] is True
    assert result["massive_1plus_residue_positive"] is True


def test_wheeler_to_ps_variational_source_map_reconstructs_clean_raw_source():
    result = wheeler_ps_source_map_gate()

    assert result["response_final_pair_symmetric"] is True
    assert result["raw_source_matches_clean_response_in_this_state"] is True
    assert result["raw_expected_components_pass"] is True

    assert (
        result[
            "wheeler_to_ps_variational_source_map_convention_matched"
        ]
        is True
    )

    raw = wheeler_to_ps_raw_source()

    assert math.isclose(
        raw[2, 0, 3],
        8.0,
    )

    assert math.isclose(
        raw[2, 3, 0],
        8.0,
    )


def test_torsion_free_source_projection_has_required_symmetry_and_components():
    result = torsion_free_source_gate()

    assert result["torsion_free_first_third_symmetric"] is True
    assert result["torsion_free_expected_components_pass"] is True
    assert result["torsion_free_projection_reconstructed"] is True

    source = torsion_free_ps_source()

    assert np.allclose(
        source,
        np.swapaxes(
            source,
            0,
            2,
        ),
        atol=1.0e-12,
        rtol=0.0,
    )

    assert math.isclose(
        result["torsion_free_source_norm"],
        8.0,
    )


def test_torsion_free_projection_preserves_allowed_source_coupling():
    result = torsion_free_projection_identity_gate()

    assert result["test_field_first_third_symmetric"] is True

    assert (
        result[
            "torsion_free_source_projection_identity_pass"
        ]
        is True
    )

    assert math.isclose(
        result["contraction_difference"],
        0.0,
        abs_tol=1.0e-12,
    )


def test_projected_source_passes_both_projective_trace_constraints():
    result = projected_projective_trace_gate()

    assert (
        result[
            "projective_constraint_tau_nu_nu_mu_pass"
        ]
        is True
    )

    assert (
        result[
            "projective_constraint_tau_mu_nu_nu_pass"
        ]
        is True
    )

    assert (
        result[
            "both_projective_source_trace_constraints_pass"
        ]
        is True
    )

    assert math.isclose(
        result["trace_first_second_norm"],
        0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result["trace_second_third_norm"],
        0.0,
        abs_tol=1.0e-12,
    )


def test_required_torsion_free_projection_changes_rest_pole_current():
    result = exact_ps_1plus_pole_source_gate()

    assert result["naive_raw_rest_1plus_current_zero"] is True

    assert (
        result[
            "torsion_free_projected_rest_1plus_current_nonzero"
        ]
        is True
    )


def test_exact_div1_antisymmetric_current_matches_rest_prediction():
    result = exact_ps_1plus_pole_source_gate()

    assert result["current_23_matches"] is True
    assert result["current_32_matches"] is True

    assert math.isclose(
        result[
            "torsion_free_antisymmetric_div1_norm2"
        ],
        8.0
        *
        result[
            "m_plus_squared"
        ],
    )


def test_exact_ps_1plus_on_shell_numerator_is_positive():
    result = exact_ps_1plus_pole_source_gate()

    assert result["on_shell_transverse_projector_pass"] is True
    assert result["exact_numerator_matches_8m2"] is True
    assert result["exact_ps_1plus_pole_numerator_nonzero"] is True

    assert math.isclose(
        result["exact_ps_1plus_pole_numerator"],
        1.44,
    )


def test_pole_coefficient_proxy_positive_but_not_energy():
    result = exact_ps_1plus_pole_source_gate()

    assert (
        result[
            "full_propagator_pole_coefficient_proxy_positive"
        ]
        is True
    )

    assert math.isclose(
        result[
            "full_propagator_pole_coefficient_proxy"
        ],
        0.36,
    )

    assert (
        result[
            "pole_coefficient_proxy_is_physical_coupling"
        ]
        is False
    )

    assert (
        result[
            "pole_coefficient_proxy_is_physical_energy"
        ]
        is False
    )

    assert (
        result[
            "overall_wheeler_source_normalization_omitted"
        ]
        is True
    )


def test_full_diffeomorphism_ward_remains_open():
    result = diffeomorphism_ward_gate()

    assert result["massive_rest_connection_term_zero"] is True
    assert result["generic_connection_term_nonzero"] is True

    assert (
        result[
            "metric_source_sigma_required_for_generic_ward"
        ]
        is True
    )

    assert (
        result[
            "sigma_from_same_wheeler_projective_action_derived"
        ]
        is False
    )

    assert (
        result[
            "full_diffeomorphism_matter_ward_established"
        ]
        is False
    )


def test_a9_summary_is_partial_green_not_complete_model():
    result = h17a9_summary()

    assert result["partial_green"] is True

    assert result["decision"].startswith(
        "GREEN_PARTIAL_A9_"
    )

    assert (
        result[
            "exact_projective_1plus_pole_overlap_established"
        ]
        is True
    )

    assert (
        result[
            "projective_source_trace_constraints_pass"
        ]
        is True
    )

    assert (
        result[
            "full_diffeomorphism_matter_ward_established"
        ]
        is False
    )

    assert (
        result[
            "projective_symmetry_of_combined_wheeler_matter_action_established"
        ]
        is False
    )

    assert result["same_action_hook17_complete"] is False
    assert result["hook17_closed"] is False

    assert math.isclose(
        result[
            "hook17_reference_capacity_rp1e12_j"
        ],
        HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    )

    assert result["hook17_complete_energy_j"] is None
    assert result["energy_optimization_authorized"] is False
    assert result["h17b_authorized"] is False

    assert result[
        "next"
    ] == (
        "032H17A9R1_PERCACCI_SEZGIN_WHEELER_"
        "SAME_ACTION_MATTER_NOETHER_GATE"
    )
