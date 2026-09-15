"""Regression tests for 032H17A12D1 same-action finite-matter loading."""

from __future__ import annotations

from antigravity_research.agminer.hook17_pauli_f2_same_action_loading import (
    a12c_reference_gate,
    controlled_portal_window_gate,
    h17a12d1_summary,
    maximum_local_loading_lower_bound,
    necessary_portal_scale_for_global_loading_bound,
    pauli_loading_overlap_gate,
    payload_average_density_gate,
    provenance_gate,
    same_action_variation_gate,
)


def test_same_action_variation_has_independent_factor_two_reconstruction():
    result = (
        same_action_variation_gate()
    )

    assert result[
        "factor_two_independently_reconstructed"
    ] is True

    assert result[
        "finite_matter_quadratic_loading_present"
    ] is True

    assert result[
        "metric_portal_has_linear_off_state_source"
    ] is False


def test_a12c_explicitly_omitted_loaded_matter_backreaction():
    result = (
        provenance_gate()
    )

    assert result[
        "pass"
    ] is True

    assert result[
        "a12c_loaded_matter_backreaction_included"
    ] is False

    assert result[
        "source_shape_reuse_preserved"
    ] is True

    assert result[
        "same_action_loaded_kernel_reuse_established"
    ] is False


def test_payload_average_density_gives_rigorous_local_loading_lower_bound():
    result = (
        payload_average_density_gate()
    )

    assert (
        0.78
        <
        result[
            "payload_geometric_volume_m3"
        ]
        <
        0.80
    )

    assert (
        1.0e17
        <
        result[
            "average_payload_rest_energy_density_j_m3"
        ]
        <
        1.2e17
    )

    assert (
        5.0e15
        <
        result[
            "average_payload_rest_energy_density_ev4"
        ]
        <
        6.0e15
    )

    assert result[
        "nonnegative_density_implies_max_ge_average"
    ] is True

    assert result[
        "weak_loading_if_bound_passes_is_sufficient"
    ] is False


def test_a12c_one_kev_probe_reference_fails_even_order_one_loading_bound():
    result = (
        maximum_local_loading_lower_bound(
            1.0e3
        )
    )

    assert (
        1.0e4
        <
        result[
            "maximum_local_epsilon_load_lower_bound"
        ]
        <
        1.2e4
    )

    assert result[
        "global_loading_le_1_not_ruled_out"
    ] is False


def test_necessary_loading_scales_are_about_10_18_32_kev():
    order_one = (
        necessary_portal_scale_for_global_loading_bound(
            1.0
        )
    )

    ten_percent = (
        necessary_portal_scale_for_global_loading_bound(
            0.1
        )
    )

    one_percent = (
        necessary_portal_scale_for_global_loading_bound(
            0.01
        )
    )

    assert (
        1.00e4
        <
        order_one
        <
        1.05e4
    )

    assert (
        1.80e4
        <
        ten_percent
        <
        1.85e4
    )

    assert (
        3.20e4
        <
        one_percent
        <
        3.30e4
    )


def test_a12c_has_optimistic_loading_controlled_field_only_candidate_window():
    result = (
        controlled_portal_window_gate()
    )

    reference = (
        a12c_reference_gate()
    )

    assert (
        4.0e4
        <
        reference[
            "field_only_strict_10mj_portal_scale_ev"
        ]
        <
        4.5e4
    )

    assert result[
        "order_one_candidate_interval_nonempty"
    ] is True

    assert result[
        "ten_percent_candidate_interval_nonempty"
    ] is True

    assert result[
        "one_percent_candidate_interval_nonempty"
    ] is True

    assert (
        result[
            "maximum_local_loading_lower_bound_at_field_upper"
        ]
        <
        0.01
    )

    assert result[
        "intervals_are_loaded_solutions"
    ] is False

    assert result[
        "loaded_bvp_required_for_promotion"
    ] is True


def test_minimal_pauli_sub10mj_corridor_has_no_order_one_loading_overlap():
    result = (
        pauli_loading_overlap_gate()
    )

    assert result[
        "pauli_sub10mj_and_global_order_one_loading_overlap_exists"
    ] is False

    assert result[
        "minimal_electron_pauli_perturbative_kernel_reuse_closed"
    ] is True

    assert (
        result[
            "order_one_loading_scale_over_pauli_10mj_boundary"
        ]
        >
        1.0e10
    )

    assert (
        result[
            "maximum_local_loading_lower_bound_at_pauli_10mj_boundary"
        ]
        >
        1.0e40
    )

    assert (
        result[
            "pauli_partial_energy_at_order_one_loading_scale"
        ][
            "optimistic_electron_rest_floor_j"
        ]
        >
        1.0e28
    )

    assert result[
        "strongly_loaded_pauli_solution_closed"
    ] is False


def test_a12d1_closeout_is_scoped_and_preserves_the_mechanism():
    result = (
        h17a12d1_summary()
    )

    assert result[
        "minimal_electron_pauli_perturbative_kernel_reuse_closed"
    ] is True

    assert result[
        "a12c_2p656859j_probe_limit_capacity_reference_preserved"
    ] is True

    assert result[
        "a12c_2p656859j_same_action_loaded_payload_solution"
    ] is False

    assert result[
        "all_electron_pauli_realizations_closed"
    ] is False

    assert result[
        "strongly_loaded_pauli_rescue_closed"
    ] is False

    assert result[
        "a12b_exact_massless_carrier_closed"
    ] is False

    assert result[
        "a12c_gauge_invariant_f2_metric_mechanism_closed"
    ] is False

    assert result[
        "source_independent_loading_controlled_candidate_window_exists"
    ] is True

    assert result[
        "new_bvp_authorized_for_minimal_electron_pauli"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False

    assert result[
        "hook17_closed"
    ] is False

    assert result[
        "decision"
    ].startswith(
        "RED_SCOPED_A12D1_"
    )
