"""Scientific regressions for 032V25C WBG multiscale gate."""

from __future__ import annotations

import math

from antigravity_research.agminer.kgb_strong_coupling_source_gate import (
    V16_SOURCE_C_M,
    historical_source_compatibility,
)
from antigravity_research.agminer.storage import (
    Storage,
)
from antigravity_research.agminer.wbg_multiscale_gate import (
    historical_v16_wbg_corridor,
    parent_rescaling_invariance_scout,
    persist_v25c_metadata,
    persist_v25c_region_rule,
    required_linear_g3_coefficient,
    v25c_gate,
)


def test_parent_lambda3_z1():
    result = historical_v16_wbg_corridor()

    assert math.isclose(
        result[
            "lambda3_parent_ev"
        ],
        0.1040622609492028,
        rel_tol=
            1.0e-12,
    )


def test_parent_lambda3_is_far_above_source_momentum():
    result = historical_v16_wbg_corridor()

    assert (
        result[
            "lambda3_parent_over_source_k"
        ]
        >
        5.0e4
    )


def test_parent_lambda2_is_mev_scale():
    result = historical_v16_wbg_corridor()

    assert math.isclose(
        result[
            "lambda2_ev"
        ],
        1287047.823580776,
        rel_tol=
            1.0e-12,
    )


def test_parent_x_is_extremely_small():
    result = historical_v16_wbg_corridor()

    assert math.isclose(
        result[
            "x_wbg"
        ],
        1.1088762446784983e-19,
        rel_tol=
            1.0e-12,
    )


def test_order_one_local_linear_g3_gain_is_negligible():
    result = historical_v16_wbg_corridor()

    assert (
        result[
            "order_one_g3_gain_times_planck"
        ]
        <
        1.0e-18
    )


def test_a1e3_requires_huge_local_g3x():
    result = historical_v16_wbg_corridor()

    assert math.isclose(
        result[
            "a1e3_required_abs_g3x"
        ],
        1.8036259768400656e16,
        rel_tol=
            1.0e-12,
    )


def test_a1e3_effective_control_ratio_matches_v25b():
    result = historical_v16_wbg_corridor()

    assert math.isclose(
        result[
            "a1e3_local_scale_over_k"
        ],
        0.19423543641148616,
        rel_tol=
            1.0e-12,
    )


def test_parent_rescaling_invariance_across_z_values():
    historical = (
        historical_source_compatibility()
    )

    result = (
        parent_rescaling_invariance_scout(
            gradient_ev2=
                historical[
                    "gradient_ev2"
                ],

            length_m=
                V16_SOURCE_C_M,

            gain_times_planck=
                1.0e-3,

            z_values=
                (
                    0.01,
                    0.1,
                    1.0,
                ),
        )
    )

    assert (
        result[
            "parent_rescaling_invariant"
        ]
        is True
    )


def test_parent_rescaling_matches_v25b_to_machine_precision():
    result = historical_v16_wbg_corridor()

    assert (
        result[
            "a1e3_matches_v25b_ratio_error"
        ]
        <
        1.0e-14
    )


def test_planck_strength_gain_has_even_worse_control_ratio():
    result = historical_v16_wbg_corridor()

    assert (
        result[
            "a1_local_scale_over_k"
        ]
        <
        0.02
    )


def test_wbg_parent_corridor_itself_exists():
    result = v25c_gate()

    assert (
        result[
            "wbg_two_scale_parent_corridor_exists"
        ]
        is True
    )


def test_locally_linear_parent_scale_rescue_closes():
    result = v25c_gate()

    assert (
        result[
            "locally_linear_g3_parent_scale_rescue_closed"
        ]
        is True
    )


def test_nonlinear_g3_remains_open():
    result = v25c_gate()

    assert (
        result[
            "generalized_nonlinear_g3_closed"
        ]
        is False
    )


def test_large_healthy_kx_remains_open():
    result = v25c_gate()

    assert (
        result[
            "large_healthy_kx_closed"
        ]
        is False
    )


def test_wbg_g4_g5_remain_open():
    result = v25c_gate()

    assert (
        result[
            "full_wbg_g4_g5_closed"
        ]
        is False
    )


def test_alternative_hidden_source_remains_open():
    result = v25c_gate()

    assert (
        result[
            "alternative_hidden_source_closed"
        ]
        is False
    )


def test_no_action_oracle_or_blind_scan():
    result = v25c_gate()

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


def test_no_sign_payload_or_model_claim():
    result = v25c_gate()

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
            "physical_antigravity_model_found"
        ]
        is False
    )


def test_region_rule_is_idempotent(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    try:
        first = persist_v25c_region_rule(
            storage
        )

        second = persist_v25c_region_rule(
            storage
        )

        assert first == 1
        assert second == 0

    finally:
        storage.close()


def test_rule_and_metadata_mutate_no_science_tables(
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

        persist_v25c_region_rule(
            storage
        )

        persist_v25c_metadata(
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
                "032v25c_action_oracle_authorized"
            )
            ==
            "0"
        )

    finally:
        storage.close()
