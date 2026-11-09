"""Regressions for 032H17A12D1R3C1 reciprocity and ultra-small validation."""

from __future__ import annotations

import math

import numpy as np
from scipy.sparse import csr_matrix

from antigravity_research.agminer.hook17_fdual_f_r3c1_validation import (
    BRANCH,
    DIRECT_VALIDATION_GRIDS_M,
    GRID_SPACINGS_M,
    ULTRASMALL_LOADING,
    _relative_sparse_difference,
    action_axis_weight_ratio,
    final_decision,
    provenance_gate,
    sign_change_brackets,
)


def test_branch_name_is_frozen():
    assert (
        BRANCH
        ==
        "032H17A12D1R3C1"
    )


def test_r3c_provenance_is_required():
    result = (
        provenance_gate()
    )

    assert result[
        "pass"
    ] is True

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "006d_replaced"
    ] is False


def test_variational_axis_weight_is_h_over_8_not_h_over_4():
    result = (
        action_axis_weight_ratio()
    )

    assert math.isclose(
        result[
            "required_w0_over_w1"
        ],
        0.125,
    )

    assert math.isclose(
        result[
            "variational_w0_over_w1"
        ],
        0.125,
    )

    assert math.isclose(
        result[
            "r3c_diagnostic_w0_over_w1"
        ],
        0.25,
    )


def test_ultrasmall_scan_directly_samples_unresolved_region():
    required = (
        1.0e-9,
        3.0e-9,
        1.0e-8,
        3.0e-8,
        1.0e-7,
        3.0e-7,
        1.0e-6,
        3.0e-6,
        1.0e-5,
        3.0e-5,
        1.0e-4,
    )

    assert (
        ULTRASMALL_LOADING[
            0
        ]
        ==
        0.0
    )

    for value in required:
        assert (
            value
            in
            ULTRASMALL_LOADING
        )


def test_original_r3c_grids_receive_direct_full_solve_validation():
    assert (
        DIRECT_VALIDATION_GRIDS_M
        ==
        (
            0.075,
            0.050,
        )
    )

    assert (
        GRID_SPACINGS_M[
            :2
        ]
        ==
        DIRECT_VALIDATION_GRIDS_M
    )

    assert (
        0.040
        in
        GRID_SPACINGS_M
    )


def test_relative_sparse_difference_is_scale_normalized():
    lhs = csr_matrix(
        np.diag(
            [
                1.0e9,
                2.0e9,
            ]
        )
    )

    rhs = csr_matrix(
        np.diag(
            [
                1.0e9
                +
                1.0e-3,
                2.0e9,
            ]
        )
    )

    result = (
        _relative_sparse_difference(
            lhs,
            rhs,
        )
    )

    assert (
        result[
            "max_abs"
        ]
        >
        0.0
    )

    assert (
        result[
            "relative_max_abs"
        ]
        <
        1.0e-11
    )


def test_sign_change_brackets_require_directly_sampled_opposite_signs():
    rows = [
        {
            "loading_fraction":
                0.0,

            "solve_success":
                True,

            "minimum_payload_acceleration_m_s2":
                9.8,
        },
        {
            "loading_fraction":
                3.0e-7,

            "solve_success":
                True,

            "minimum_payload_acceleration_m_s2":
                1.0,
        },
        {
            "loading_fraction":
                1.0e-6,

            "solve_success":
                True,

            "minimum_payload_acceleration_m_s2":
                -2.0,
        },
    ]

    brackets = (
        sign_change_brackets(
            rows
        )
    )

    assert len(
        brackets
    ) == 1

    assert (
        brackets[
            0
        ][
            "lambda_left"
        ]
        ==
        3.0e-7
    )

    assert (
        brackets[
            0
        ][
            "lambda_right"
        ]
        ==
        1.0e-6
    )

    assert (
        brackets[
            0
        ][
            "direction"
        ]
        ==
        "OUTWARD_TO_INWARD"
    )


def _green_mock_item(
    h: float,
) -> dict:
    return {
        "grid_spacing_m":
            h,

        "variational_certificate":
            {
                "complete_variational_same_action_pass":
                    True,
            },

        "direct_vs_woodbury":
            (
                [
                    {
                        "pass":
                            True,
                    }
                ]
                if h
                in
                DIRECT_VALIDATION_GRIDS_M
                else
                []
            ),

        "sign_change_brackets":
            [
                {
                    "direction":
                        "OUTWARD_TO_INWARD",
                }
            ],

        "refined_sign_change_brackets":
            [
                {
                    "lambda_midpoint":
                        5.0e-7,
                }
            ],

        "ultrasmall_scan":
            [
                {
                    "loading_fraction":
                        1.0e-4,

                    "solve_success":
                        True,

                    "minimum_payload_acceleration_m_s2":
                        -1.0,
                }
            ],
    }


def test_final_decision_only_authorizes_node_prefight_after_all_validation_gates():
    grids = {
        str(
            h
        ):
            _green_mock_item(
                h
            )
        for h in GRID_SPACINGS_M
    }

    result = (
        final_decision(
            grids
        )
    )

    assert result[
        "authorize_r3d0_node_integrability_prefight"
    ] is True

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "006d_replaced"
    ] is False


def test_final_decision_holds_if_variational_certificate_fails():
    grids = {
        str(
            h
        ):
            _green_mock_item(
                h
            )
        for h in GRID_SPACINGS_M
    }

    grids[
        str(
            0.050
        )
    ][
        "variational_certificate"
    ][
        "complete_variational_same_action_pass"
    ] = False

    result = (
        final_decision(
            grids
        )
    )

    assert result[
        "authorize_r3d0_node_integrability_prefight"
    ] is False

    assert (
        result[
            "next"
        ]
        ==
        "REPAIR_R3C1_VARIATIONAL_DISCRETIZATION"
    )


def test_no_claim_promotion_from_validation_run():
    grids = {
        str(
            h
        ):
            _green_mock_item(
                h
            )
        for h in GRID_SPACINGS_M
    }

    result = (
        final_decision(
            grids
        )
    )

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False

    assert result[
        "complete_energy_established"
    ] is False
