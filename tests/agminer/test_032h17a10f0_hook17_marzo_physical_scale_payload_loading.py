"""Regressions for 032H17A10F0 physical-scale/loading gate."""

from __future__ import annotations

import math

from antigravity_research.agminer.hook17_marzo_physical_scale_payload_loading import (
    SELECTED_M_INSIDE_R,
    capacity_10mj_loading_threshold,
    empirical_quadratic_metric_gate,
    h17a10f0_summary,
    lambda_for_loading_target,
    loading_capacity_scan,
    payload_loading_metrics,
    physical_planck_normalized_family,
    scalar_yukawa_capacity_comparator,
    source_stueckelberg_gradient_control,
    symbolic_marzo_scale_identity,
)


def test_selected_marzo_family_has_exact_range_identity():
    result = symbolic_marzo_scale_identity()

    assert result[
        "mass_identity_pass"
    ] is True

    assert result[
        "mass_squared_exact"
    ] == "d1**2/c7"

    assert result[
        "independent_of_a0"
    ] is True

    assert result[
        "independent_of_a4"
    ] is True


def test_planck_normalized_one_metre_family_is_healthy_branch_ii():
    result = physical_planck_normalized_family()

    assert result[
        "published_health_branch_II_pass"
    ] is True

    assert result[
        "range_reproduced"
    ] is True

    assert result[
        "health_A_over_planck_squared"
    ] < -10.9

    assert result[
        "planck_normalization_requires_huge_c7"
    ] is False


def test_canonical_source_overlap_is_not_planck_suppressed_at_c7_one():
    result = physical_planck_normalized_family()

    assert math.isclose(
        result[
            "pole_derivative_norm"
        ],
        1.5,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    assert math.isclose(
        result[
            "source_saturated_residue"
        ],
        16.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "canonical_source_coupling_magnitude"
        ],
        4.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert result[
        "canonical_source_coupling_planck_suppressed"
    ] is False


def test_quadratic_vector_portal_has_three_polarization_penalty():
    result = empirical_quadratic_metric_gate()

    assert result[
        "trace_M_squared"
    ] == 12.0

    assert result[
        "active_background_coefficient_abs"
    ] == 2.0

    assert result[
        "projector_penalty"
    ] == 3.0

    assert (
        2.7e-25
        <
        result[
            "lambda_empirical_max_ev_m2"
        ]
        <
        2.9e-25
    )


def test_empirical_portal_limit_would_strongly_load_one_kg_payload():
    empirical = empirical_quadratic_metric_gate()

    result = payload_loading_metrics(
        lambda_ev_m2=
            empirical[
                "lambda_empirical_max_ev_m2"
            ]
    )

    assert result[
        "vacuum_mR"
    ] == 0.1

    assert result[
        "inside_mR"
    ] > 300.0

    assert result[
        "penetration_length_m"
    ] < 5.0e-4


def test_moderate_loading_target_requires_much_smaller_lambda():
    selected = lambda_for_loading_target(
        target_inside_mR=
            SELECTED_M_INSIDE_R
    )

    empirical = empirical_quadratic_metric_gate()[
        "lambda_empirical_max_ev_m2"
    ]

    assert (
        5.0e-32
        <
        selected
        <
        6.5e-32
    )

    assert (
        empirical
        /
        selected
        >
        4.0e6
    )

    load = payload_loading_metrics(
        lambda_ev_m2=
            selected
    )

    assert math.isclose(
        load[
            "inside_mR"
        ],
        0.20,
        rel_tol=2.0e-14,
    )


def test_load_controlled_field_amplitude_and_capacity_remain_below_10mj():
    selected = lambda_for_loading_target(
        target_inside_mR=
            0.20
    )

    result = scalar_yukawa_capacity_comparator(
        lambda_ev_m2=
            selected
    )

    assert (
        2.5e7
        <
        result[
            "payload_canonical_amplitude_ev"
        ]
        <
        3.5e7
    )

    assert (
        4.0e5
        <
        result[
            "scalar_yukawa_capacity_energy_j"
        ]
        <
        6.0e5
    )

    assert result[
        "scalar_yukawa_capacity_energy_j"
    ] < 1.0e7

    assert result[
        "this_is_complete_energy"
    ] is False


def test_two_metre_source_has_subunity_stueckelberg_gradient_ratio():
    result = source_stueckelberg_gradient_control()

    assert math.isclose(
        result[
            "q_over_f"
        ],
        0.5,
        rel_tol=2.0e-15,
    )

    assert result[
        "q_over_f_at_most_one"
    ] is True

    assert result[
        "this_is_full_source_eft_control"
    ] is False


def test_capacity_crosses_10mj_only_just_above_vacuum_loading():
    result = capacity_10mj_loading_threshold()

    assert math.isclose(
        result[
            "vacuum_mR"
        ],
        0.1,
        rel_tol=2.0e-15,
    )

    assert (
        0.106
        <
        result[
            "capacity_10mj_crossing_mR"
        ]
        <
        0.109
    )

    assert math.isclose(
        result[
            "capacity_at_crossing_j"
        ],
        1.0e7,
        rel_tol=5.0e-12,
    )


def test_scan_contains_broad_partial_capacity_corridor():
    rows = loading_capacity_scan()

    row = next(
        item
        for item in rows
        if item[
            "target_inside_mR"
        ]
        ==
        0.20
    )

    assert row[
        "capacity_below_strict_10mj"
    ] is True

    assert row[
        "empirical_lambda_over_selected_lambda"
    ] > 4.0e6


def test_a10f0_is_corridor_only_and_promotes_exact_bvp_gate():
    result = h17a10f0_summary()

    assert result[
        "partial_green"
    ] is True

    assert result[
        "planck_normalization_kills_one_metre_carrier"
    ] is False

    assert result[
        "huge_c7_required_for_one_metre_range"
    ] is False

    assert result[
        "canonical_source_overlap_planck_suppressed"
    ] is False

    assert result[
        "payload_loading_is_stronger_than_inverse_cube_empirical_limit"
    ] is True

    assert result[
        "empirical_portal_limit_is_finite_payload_safe"
    ] is False

    assert result[
        "load_controlled_partial_capacity_corridor_open"
    ] is True

    assert result[
        "finite_payload_established"
    ] is False

    assert result[
        "complete_energy_established"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False

    assert result[
        "next"
    ] == (
        "032H17A10F1_EXACT_FINITE_TRANSVERSE_VECTOR_SOURCE_"
        "FINITE_PAYLOAD_BVP_SOURCE_ENERGY_EMPIRICAL_UV_"
        "AND_COMPLETE_LEDGER_KILL_GATE"
    )
