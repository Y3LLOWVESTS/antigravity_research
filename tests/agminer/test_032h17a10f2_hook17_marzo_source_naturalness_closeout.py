"""Regressions for 032H17A10F2."""

from __future__ import annotations

import math

from antigravity_research.agminer.hook17_marzo_source_naturalness_closeout import (
    fermion_threshold_mass_nda,
    h17a10f2_summary,
    hypothetical_weak_current_escape,
    longitudinal_stueckelberg_diagnostic,
    microscopic_coupling_lower_bound,
    naturalness_suppression_requirement,
    strict_payload_floor_rescale,
    stueckelberg_protection_audit,
)


def test_strict_payload_rescale_raises_local_minimum_to_one_g():
    result = strict_payload_floor_rescale()

    assert (
        result[
            "original_local_min_acceleration_m_s2"
        ]
        <
        9.80665
    )

    assert math.isclose(
        result[
            "strict_local_min_acceleration_m_s2"
        ],
        9.80665,
        rel_tol=0.0,
        abs_tol=1.0e-11,
    )

    assert (
        result[
            "strict_minimum_local_payload_floor_pass"
        ]
        is True
    )


def test_strict_payload_amplitude_and_energy_scaling_are_exact():
    result = strict_payload_floor_rescale()

    assert (
        2.62
        <
        result[
            "required_acceleration_energy_scale"
        ]
        <
        2.63
    )

    assert (
        1.61
        <
        result[
            "required_field_source_amplitude_scale"
        ]
        <
        1.63
    )

    assert (
        5.5e5
        <
        result[
            "strict_field_loading_energy_j"
        ]
        <
        5.8e5
    )


def test_strict_reduced_eft_payload_now_passes_1g_1m_floor():
    result = strict_payload_floor_rescale()

    assert math.isclose(
        result[
            "geometric_external_standoff_m"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert (
        result[
            "reduced_eft_1g_1m_strict_payload_performance_pass"
        ]
        is True
    )


def test_strict_partial_energy_keeps_electron_corridor_and_narrow_proton_corridor():
    result = strict_payload_floor_rescale()

    assert (
        result[
            "strict_field_plus_electron_rest_partial_j"
        ]
        <
        1.0e6
    )

    assert (
        9.0e6
        <
        result[
            "strict_field_plus_proton_rest_partial_j"
        ]
        <
        1.0e7
    )

    assert result[
        "electron_partial_below_10mj"
    ] is True

    assert result[
        "proton_mass_comparator_partial_below_10mj"
    ] is True

    assert result[
        "partial_energy_is_complete_energy"
    ] is False


def test_corrected_pair_coupling_implies_order_one_constituent_lower_bound():
    result = microscopic_coupling_lower_bound()

    assert math.isclose(
        result[
            "canonical_engineered_pair_pole_coupling"
        ],
        2.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "constituent_coupling_lower_bound"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert (
        result[
            "at_least_one_constituent_order_unity"
        ]
        is True
    )

    assert (
        result[
            "current_action_has_free_small_source_coupling"
        ]
        is False
    )


def test_stueckelberg_symmetry_does_not_by_itself_forbid_mass_operator():
    result = stueckelberg_protection_audit()

    assert (
        result[
            "stueckelberg_completion_required"
        ]
        is True
    )

    assert (
        result[
            "stueckelberg_completed_ward_pass"
        ]
        is True
    )

    assert (
        result[
            "B_squared_mass_operator_stueckelberg_invariant"
        ]
        is True
    )

    assert (
        result[
            "tiny_B_squared_coefficient_forbidden_by_current_symmetry"
        ]
        is False
    )

    assert (
        result[
            "operator_level_exact_engineered_current_conservation_established"
        ]
        is False
    )


def test_longitudinal_electron_scale_hierarchy_is_enormous():
    result = longitudinal_stueckelberg_diagnostic()

    assert (
        result[
            "electron_energy_over_f"
        ]
        >
        1.0e12
    )

    assert (
        result[
            "longitudinal_enhancement_gE_over_f_at_electron_threshold"
        ]
        >
        1.0e12
    )

    assert (
        result[
            "electron_mass_over_nominal_perturbative_scale"
        ]
        >
        1.0e11
    )

    assert (
        result[
            "macroscopic_device_source_q_over_f"
        ]
        ==
        0.5
    )

    assert (
        result[
            "exact_unitarity_cutoff_computed"
        ]
        is False
    )


def test_nominal_electron_threshold_nda_is_catastrophic():
    result = fermion_threshold_mass_nda(
        loop_coefficient=
            1.0
    )

    assert (
        result[
            "nda_delta_mass_squared_over_target"
        ]
        >
        1.0e22
    )

    assert (
        result[
            "technical_naturalness_pass"
        ]
        is False
    )

    assert result[
        "exact_beta_function"
    ] is False


def test_even_one_trillionth_loop_coefficient_fails_nda():
    result = fermion_threshold_mass_nda(
        loop_coefficient=
            1.0e-12
    )

    assert (
        result[
            "nda_delta_mass_squared_over_target"
        ]
        >
        1.0e10
    )

    assert (
        result[
            "technical_naturalness_pass"
        ]
        is False
    )


def test_required_unexplained_loop_suppression_is_below_1e_minus_20():
    result = naturalness_suppression_requirement()

    assert (
        result[
            "all_tested_loop_coefficients_fail"
        ]
        is True
    )

    assert (
        2.0e-23
        <
        result[
            "loop_coefficient_required_for_delta_m2_at_most_target"
        ]
        <
        3.0e-23
    )

    assert (
        result[
            "required_suppression_below_1e_minus_20"
        ]
        is True
    )


def test_hypothetical_small_coupling_has_energy_naturalness_collision():
    result = hypothetical_weak_current_escape()

    assert (
        result[
            "hypothetical_epsilon_exists_in_current_action"
        ]
        is False
    )

    assert (
        4.0e-4
        <
        result[
            "epsilon_energy_min_for_electron_partial_below_10mj"
        ]
        <
        6.0e-4
    )

    assert (
        result[
            "epsilon_naturalness_max_for_c_loop_1"
        ]
        <
        5.0e-12
    )

    assert (
        result[
            "all_tested_coefficients_have_no_energy_naturalness_overlap"
        ]
        is True
    )

    assert (
        result[
            "loop_coefficient_needed_before_simple_epsilon_overlap"
        ]
        <
        1.0e-16
    )


def test_a10f2_stops_current_realization_but_preserves_hook17_knowledge():
    result = h17a10f2_summary()

    assert (
        result[
            "strict_reduced_eft_1g_1m_payload_performance_survives"
        ]
        is True
    )

    assert (
        result[
            "current_ordinary_dirac_source_technical_naturalness_certified"
        ]
        is False
    )

    assert (
        result[
            "current_ordinary_dirac_wheeler_marzo_realization_blocked"
        ]
        is True
    )

    assert (
        result[
            "current_realization_full_certification_stops_here"
        ]
        is True
    )

    assert (
        result[
            "expensive_full_nonlinear_bvp_authorized"
        ]
        is False
    )

    assert (
        result[
            "a10d_healthy_pole_overlap_preserved"
        ]
        is True
    )

    assert (
        result[
            "a10f1_finite_reduced_eft_payload_witness_preserved"
        ]
        is True
    )

    assert (
        result[
            "marzo_protected_1minus_family_globally_closed"
        ]
        is False
    )

    assert result[
        "hook17_closed"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False
