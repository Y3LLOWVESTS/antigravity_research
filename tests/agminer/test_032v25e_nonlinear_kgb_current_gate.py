"""Scientific regressions for 032V25E nonlinear KGB current gate."""

from __future__ import annotations

import math

import pytest

from antigravity_research.agminer.nonlinear_kgb_current_gate import (
    FOUR_PI,
    integrated_source_charge,
    local_static_response,
    monotone_source_aligned_theorem,
    persist_v25e_metadata,
    persist_v25e_region_rule,
    pure_k_linear_in_s,
    required_static_margin_for_response_gain,
    source_aligned_current,
    source_current_jacobian,
    v25e_gate,
)
from antigravity_research.agminer.storage import (
    Storage,
)


def test_canonical_free_scalar_current():
    result = source_aligned_current(
        u=
            1.0,

        radius=
            2.0,

        a_value=
            1.0,

        b_value=
            0.0,
    )

    assert math.isclose(
        result,
        1.0,
    )


def test_canonical_free_scalar_jacobian():
    result = source_current_jacobian(
        u=
            1.0,

        radius=
            2.0,

        a_value=
            1.0,

        a_s=
            0.0,

        b_value=
            0.0,

        b_s=
            0.0,
    )

    assert math.isclose(
        result,
        1.0,
    )


def test_integrated_source_charge_is_four_pi_r2_f():
    result = integrated_source_charge(
        u=
            1.0,

        radius=
            2.0,

        a_value=
            1.0,

        b_value=
            0.0,
    )

    assert math.isclose(
        result,
        16.0
        *
        math.pi,
    )


def test_local_response_is_inverse_current_jacobian():
    result = local_static_response(
        u=
            1.0,

        radius=
            2.0,

        a_value=
            2.0,

        a_s=
            0.5,

        b_value=
            0.3,

        b_s=
            0.2,
    )

    expected = (
        1.0
        /
        (
            FOUR_PI
            *
            4.0
            *
            result[
                "jacobian"
            ]
        )
    )

    assert math.isclose(
        result[
            "d_u_d_q"
        ],
        expected,
        rel_tol=
            1.0e-14,
    )


def test_monotone_difference_identity():
    result = monotone_source_aligned_theorem(
        u=
            1.0,

        radius=
            2.0,

        a_value=
            2.0,

        a_s=
            0.5,

        b_value=
            0.3,

        b_s=
            0.2,
    )

    assert (
        result[
            "difference_identity_error"
        ]
        <
        1.0e-14
    )


def test_monotone_source_aligned_branch_has_elasticity_at_least_one():
    result = monotone_source_aligned_theorem(
        u=
            1.0,

        radius=
            2.0,

        a_value=
            2.0,

        a_s=
            0.5,

        b_value=
            0.3,

        b_s=
            0.2,
    )

    assert (
        result[
            "elasticity"
        ]
        >=
        1.0
    )

    assert (
        result[
            "monotone_branch_cannot_antiscreen_source_current"
        ]
        is True
    )


def test_pure_k_positive_slope_is_screening():
    result = monotone_source_aligned_theorem(
        u=
            1.0,

        radius=
            1.0,

        a_value=
            1.5,

        a_s=
            0.5,

        b_value=
            0.0,

        b_s=
            0.0,
    )

    assert (
        result[
            "elasticity"
        ]
        >
        1.0
    )


def test_positive_monotone_g3_piece_is_screening():
    result = monotone_source_aligned_theorem(
        u=
            1.0,

        radius=
            1.0,

        a_value=
            1.0,

        a_s=
            0.0,

        b_value=
            0.5,

        b_s=
            0.2,
    )

    assert (
        result[
            "elasticity"
        ]
        >
        1.0
    )


def test_nonmonotone_pure_k_can_antiscreen_algebraically():
    result = pure_k_linear_in_s(
        alpha=
            0.5,
    )

    assert (
        result[
            "static_branch_regular"
        ]
        is True
    )

    assert (
        result[
            "elasticity"
        ]
        <
        1.0
    )

    assert (
        result[
            "response_gain_over_canonical_baseline"
        ]
        >
        1.0
    )


def test_alpha_066_gives_about_100x_static_response():
    result = pure_k_linear_in_s(
        alpha=
            0.66,
    )

    assert math.isclose(
        result[
            "jacobian"
        ],
        0.01,
        rel_tol=0.0,
        abs_tol=2.0e-15,
    )

    assert math.isclose(
        result[
            "response_gain_over_canonical_baseline"
        ],
        100.0,
        rel_tol=2.0e-13,
    )


def test_alpha_066_canonical_source_coupling_is_10x():
    result = pure_k_linear_in_s(
        alpha=
            0.66,
    )

    assert math.isclose(
        result[
            "radial_static_canonical_source_coupling_relative"
        ],
        10.0,
        rel_tol=2.0e-13,
    )


def test_pure_k_branch_degenerates_at_two_thirds():
    result = pure_k_linear_in_s(
        alpha=
            2.0
            /
            3.0,
    )

    assert (
        result[
            "static_branch_regular"
        ]
        is False
    )

    assert abs(
        result[
            "jacobian"
        ]
    ) < 1.0e-14


def test_beyond_two_thirds_is_static_branch_negative():
    result = pure_k_linear_in_s(
        alpha=
            0.68,
    )

    assert (
        result[
            "static_branch_regular"
        ]
        is False
    )

    assert (
        result[
            "jacobian"
        ]
        <
        0.0
    )


def test_1000x_response_requires_jacobian_1e3():
    result = required_static_margin_for_response_gain(
        1000.0
    )

    assert math.isclose(
        result[
            "required_static_radial_jacobian"
        ],
        1.0e-3,
    )


def test_1000x_response_implies_sqrt1000_canonical_source_factor():
    result = required_static_margin_for_response_gain(
        1000.0
    )

    assert math.isclose(
        result[
            "radial_static_canonical_source_coupling_relative"
        ],
        math.sqrt(
            1000.0
        ),
        rel_tol=1.0e-14,
    )


def test_response_gain_below_one_is_rejected():
    with pytest.raises(
        ValueError
    ):
        required_static_margin_for_response_gain(
            0.5
        )


def test_v25e_closes_only_monotone_source_antiscreening():
    result = v25e_gate()

    assert (
        result[
            "monotone_source_aligned_no_antiscreen_theorem"
        ]
        is True
    )

    assert (
        result[
            "nonmonotone_kxx_closed"
        ]
        is False
    )

    assert (
        result[
            "nonmonotone_g3xx_closed"
        ]
        is False
    )


def test_v25e_does_not_claim_metric_numerator_or_full_stability():
    result = v25e_gate()

    assert (
        result[
            "metric_braiding_numerator_analyzed"
        ]
        is False
    )

    assert (
        result[
            "full_tensor_stability_certified"
        ]
        is False
    )


def test_v25e_makes_no_sign_payload_energy_or_model_claim():
    result = v25e_gate()

    assert (
        result[
            "outward_sign_established"
        ]
        is False
    )

    assert (
        result[
            "finite_payload_response_established"
        ]
        is False
    )

    assert (
        result[
            "complete_operating_energy_established"
        ]
        is False
    )

    assert (
        result[
            "physical_antigravity_model_found"
        ]
        is False
    )


def test_v25e_region_rule_is_idempotent(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    try:
        first = persist_v25e_region_rule(
            storage
        )

        second = persist_v25e_region_rule(
            storage
        )

        assert first == 1
        assert second == 0

    finally:
        storage.close()


def test_v25e_rule_metadata_mutate_no_science_tables(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    tables = (
        "models",
        "rejections",
        "survivors",
        "action_oracles",
        "collective_scaling",
        "mechanism_metrics",
    )

    try:
        before = {
            table:
                int(
                    storage.connection.execute(
                        f"""
                        SELECT COUNT(*) AS count
                        FROM {table}
                        """
                    ).fetchone()[
                        "count"
                    ]
                )
            for table
            in tables
        }

        persist_v25e_region_rule(
            storage
        )

        persist_v25e_metadata(
            storage
        )

        after = {
            table:
                int(
                    storage.connection.execute(
                        f"""
                        SELECT COUNT(*) AS count
                        FROM {table}
                        """
                    ).fetchone()[
                        "count"
                    ]
                )
            for table
            in tables
        }

        assert before == after

        assert (
            storage.get_metadata(
                "032v25e_action_oracle_authorized"
            )
            ==
            "0"
        )

    finally:
        storage.close()


def test_v25e_next_gate_is_full_metric_numerator_and_branch_stability():
    result = v25e_gate()

    assert result[
        "next"
    ] == (
        "032V25F_NONMONOTONE_KX_G3XX_FULL_TENSOR_METRIC_"
        "NUMERATOR_AND_BRANCH_STABILITY_GATE"
    )

    assert (
        result[
            "action_oracle_authorized"
        ]
        is False
    )

    assert (
        result[
            "blind_parameter_scan_authorized"
        ]
        is False
    )
