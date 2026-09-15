"""Regressions for 032H17A12D1R3C loaded topological homotopy."""

from __future__ import annotations

import math

from antigravity_research.agminer.hook17_fdual_f_loaded_payload_homotopy import (
    BRANCH,
    GRID_SPACINGS_M,
    LOADING_HOMOTOPY,
    claim_policy_gate,
    critical_loading_fraction,
    energy_factor_for_one_g,
    node_geometry_burden,
    provenance_gate,
    source_amplitude_factor_for_one_g,
    suppression_target_from_critical_fraction,
)


def test_branch_name_is_frozen():
    assert BRANCH == "032H17A12D1R3C"


def test_provenance_requires_r3a_and_r3b_green_scoped_results():
    result = provenance_gate()

    assert result[
        "pass"
    ] is True

    assert result[
        "r3a_structural_rescue_survives"
    ] is True

    assert result[
        "r3b_low_joule_class_preserved"
    ] is True

    assert result[
        "r3b_net_electric_charge_zero"
    ] is True


def test_r3a_exact_bulk_residual_is_far_below_interface_order():
    result = provenance_gate()

    assert result[
        "r3a_exact_bulk_residual"
    ] < 1.0e-8


def test_grid_sequence_reuses_r3b_coarse_and_fine_resolutions():
    assert GRID_SPACINGS_M == (
        0.075,
        0.050,
    )


def test_homotopy_begins_unloaded_and_ends_fully_loaded():
    assert LOADING_HOMOTOPY[
        0
    ] == 0.0

    assert LOADING_HOMOTOPY[
        -1
    ] == 1.0


def test_homotopy_resolves_small_interface_loading():
    assert 1.0e-4 in LOADING_HOMOTOPY
    assert 1.0e-3 in LOADING_HOMOTOPY
    assert 1.0e-2 in LOADING_HOMOTOPY


def test_source_amplitude_scaling_is_square_root_of_acceleration_ratio():
    factor = (
        source_amplitude_factor_for_one_g(
            4.903325
        )
    )

    assert math.isclose(
        factor,
        math.sqrt(
            2.0
        ),
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_energy_scaling_is_linear_in_required_acceleration_ratio():
    factor = (
        energy_factor_for_one_g(
            4.903325
        )
    )

    assert math.isclose(
        factor,
        2.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_negative_minimum_acceleration_cannot_be_amplitude_rescaled():
    assert (
        source_amplitude_factor_for_one_g(
            -1.0
        )
        is None
    )

    assert (
        energy_factor_for_one_g(
            -1.0
        )
        is None
    )


def test_critical_loading_interpolates_sign_crossing():
    rows = [
        {
            "loading_fraction": 0.0,
            "solve_success": True,
            "minimum_payload_acceleration_m_s2": 10.0,
        },
        {
            "loading_fraction": 0.5,
            "solve_success": True,
            "minimum_payload_acceleration_m_s2": 5.0,
        },
        {
            "loading_fraction": 1.0,
            "solve_success": True,
            "minimum_payload_acceleration_m_s2": -5.0,
        },
    ]

    result = critical_loading_fraction(
        rows
    )

    assert result[
        "sign_crossing_found"
    ] is True

    assert math.isclose(
        result[
            "critical_loading_fraction"
        ],
        0.75,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_full_outward_loading_returns_unit_critical_lower_bound():
    rows = [
        {
            "loading_fraction": 0.0,
            "solve_success": True,
            "minimum_payload_acceleration_m_s2": 9.80665,
        },
        {
            "loading_fraction": 1.0,
            "solve_success": True,
            "minimum_payload_acceleration_m_s2": 2.0,
        },
    ]

    result = critical_loading_fraction(
        rows
    )

    assert result[
        "full_loading_outward"
    ] is True

    assert result[
        "critical_loading_fraction"
    ] == 1.0


def test_suppression_target_converts_critical_fraction_to_cancellation():
    result = (
        suppression_target_from_critical_fraction(
            0.1
        )
    )

    assert math.isclose(
        result[
            "minimum_interface_cancellation_fraction"
        ],
        0.9,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    assert result[
        "angular_tolerance_is_rigorous"
    ] is False


def test_node_geometry_corrects_four_point_six_degree_interpretation():
    result = node_geometry_burden()

    assert (
        40.0
        <
        result[
            "approx_gross_reorientation_to_establish_node_deg"
        ]
        <
        50.0
    )

    assert (
        4.0
        <
        result[
            "node_centered_additional_rotation_across_taper_deg"
        ]
        <
        5.0
    )


def test_node_gross_rotation_is_much_larger_than_taper_gradient_rotation():
    result = node_geometry_burden()

    assert (
        result[
            "approx_gross_reorientation_to_establish_node_deg"
        ]
        >
        5.0
        *
        result[
            "node_centered_additional_rotation_across_taper_deg"
        ]
    )


def test_claim_policy_forbids_premature_model_promotion():
    result = claim_policy_gate()

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
        "complete_energy_established"
    ] is False


def test_run_is_declared_session_closeout_gate():
    result = claim_policy_gate()

    assert result[
        "final_exploratory_run_before_session_notes"
    ] is True

    assert result[
        "session_closeout_ready_after_run"
    ] is True
