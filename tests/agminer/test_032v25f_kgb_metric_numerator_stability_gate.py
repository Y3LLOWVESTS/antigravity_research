"""Scientific regressions for 032V25F."""

from __future__ import annotations

import math

from antigravity_research.agminer.kgb_metric_numerator_stability_gate import (
    INV_SQRT_6,
    local_kgb_components,
    minimal_cubic_from_y,
    persist_v25f_metadata,
    persist_v25f_region_rule,
    planar_local_components,
    radial_braiding_bound,
    required_radial_margin_for_transfer,
    source_aligned_efficiency_theorem,
    v25f_gate,
)
from antigravity_research.agminer.storage import (
    Storage,
)


def test_minimal_cubic_reproduces_v25a_z_time():
    result = minimal_cubic_from_y(
        0.25
    )

    assert math.isclose(
        result[
            "z_time"
        ],
        0.75,
        abs_tol=1.0e-14,
    )


def test_minimal_cubic_reproduces_v25a_z_radial():
    result = minimal_cubic_from_y(
        0.25
    )

    assert math.isclose(
        result[
            "z_radial"
        ],
        1.75,
        abs_tol=1.0e-14,
    )


def test_minimal_cubic_reproduces_v25a_canonical_gain():
    result = minimal_cubic_from_y(
        2.0
        /
        3.0
    )

    assert math.isclose(
        result[
            "canonical_matter_gain_times_mpl"
        ],
        1.0,
        rel_tol=1.0e-12,
    )


def test_radial_backreaction_identity():
    result = planar_local_components(
        a_value=
            2.0,

        d_value=
            0.1,

        q_value=
            0.5,
    )

    assert math.isclose(
        result[
            "z_radial"
        ]
        -
        result[
            "d_value"
        ],
        1.5
        *
        0.5**2,
        abs_tol=1.0e-14,
    )


def test_pure_k_antiscreen_has_zero_metric_braiding_numerator():
    result = planar_local_components(
        a_value=
            0.67,

        d_value=
            0.01,

        q_value=
            0.0,
    )

    assert (
        result[
            "metric_numerator_times_mpl"
        ]
        ==
        0.0
    )


def test_nonzero_braiding_can_regularize_small_fixed_metric_d():
    result = planar_local_components(
        a_value=
            2.0,

        d_value=
            0.0,

        q_value=
            0.5,
    )

    assert (
        result[
            "source_branch_regular"
        ]
        is False
    )

    assert (
        result[
            "scalar_principal_healthy"
        ]
        is True
    )


def test_radial_canonical_bound_saturates_at_d_zero():
    result = radial_braiding_bound(
        d_value=
            0.0,

        q_value=
            0.5,
    )

    assert math.isclose(
        math.sqrt(
            result[
                "numerator_squared_over_z_radial"
            ]
        ),
        INV_SQRT_6,
        rel_tol=1.0e-14,
    )


def test_radial_canonical_bound_is_strict_for_positive_d():
    result = radial_braiding_bound(
        d_value=
            0.01,

        q_value=
            0.5,
    )

    assert (
        result[
            "numerator_squared_over_z_radial"
        ]
        <
        1.0
        /
        6.0
    )

    assert (
        result[
            "bound_one_sixth"
        ]
        is True
    )


def test_1000x_two_vertex_transfer_requires_tiny_radial_margin():
    result = required_radial_margin_for_transfer(
        1000.0
    )

    assert math.isclose(
        result[
            "necessary_maximum_z_radial"
        ],
        1.0
        /
        6.0e6,
        rel_tol=1.0e-14,
    )


def test_100x_two_vertex_transfer_requires_small_radial_margin():
    result = required_radial_margin_for_transfer(
        100.0
    )

    assert (
        result[
            "necessary_maximum_z_radial"
        ]
        <
        2.0e-5
    )


def test_source_aligned_absolute_efficiency_bound():
    result = source_aligned_efficiency_theorem(
        u=
            1.0,

        radius=
            1.0,

        mpl=
            1.0,

        a_value=
            1.0,

        b_value=
            0.5,
    )

    assert (
        result[
            "efficiency_bound_pass"
        ]
        is True
    )

    assert (
        result[
            "geometry_normalized_efficiency"
        ]
        <
        1.0
    )


def test_spherical_local_healthy_example():
    result = local_kgb_components(
        u=
            1.0,

        radius=
            2.0,

        mpl=
            1.0,

        a_value=
            2.0,

        a_s=
            -1.0,

        b_value=
            0.2,

        b_s=
            0.0,

        u_prime=
            0.0,
    )

    assert (
        result[
            "scalar_principal_healthy"
        ]
        is True
    )


def test_temporal_principal_failure_detected():
    result = planar_local_components(
        a_value=
            0.1,

        d_value=
            1.0,

        q_value=
            1.0,
    )

    assert (
        result[
            "scalar_principal_healthy"
        ]
        is False
    )


def test_angular_failure_detected_in_spherical_branch():
    result = local_kgb_components(
        u=
            1.0,

        radius=
            1.0,

        mpl=
            1.0,

        a_value=
            0.1,

        a_s=
            0.0,

        b_value=
            -0.5,

        b_s=
            0.0,
    )

    assert (
        result[
            "z_angular"
        ]
        <
        0.0
    )


def test_radial_failure_detected():
    result = planar_local_components(
        a_value=
            2.0,

        d_value=
            -1.0,

        q_value=
            0.1,
    )

    assert (
        result[
            "z_radial"
        ]
        <
        0.0
    )


def test_fixed_metric_source_degeneracy_and_full_principal_health_are_distinct():
    result = planar_local_components(
        a_value=
            2.0,

        d_value=
            0.0,

        q_value=
            0.5,
    )

    assert (
        result[
            "source_branch_regular"
        ]
        is False
    )

    assert (
        result[
            "scalar_principal_healthy"
        ]
        is True
    )


def test_gate_closes_source_aligned_free_metric_gain_only():
    result = v25f_gate()

    assert (
        result[
            "source_aligned_nonmonotone_current_tuning_free_metric_gain_closed"
        ]
        is True
    )

    assert (
        result[
            "exact_metric_braiding_numerator_analyzed"
        ]
        is True
    )


def test_sign_reversed_branch_remains_open():
    result = v25f_gate()

    assert (
        result[
            "sign_reversed_b_branch_closed"
        ]
        is False
    )

    assert (
        result[
            "cancellation_branch_closed"
        ]
        is False
    )


def test_g4_g5_and_new_source_remain_open():
    result = v25f_gate()

    assert (
        result[
            "g4_g5_wbg_closed"
        ]
        is False
    )

    assert (
        result[
            "alternative_hidden_source_closed"
        ]
        is False
    )


def test_no_energy_payload_or_model_claim():
    result = v25f_gate()

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
            "action_oracle_authorized"
        ]
        is False
    )

    assert (
        result[
            "physical_antigravity_model_found"
        ]
        is False
    )


def test_v25f_region_rule_is_idempotent(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    try:
        first = persist_v25f_region_rule(
            storage
        )

        second = persist_v25f_region_rule(
            storage
        )

        assert first == 1
        assert second == 0

    finally:
        storage.close()


def test_v25f_metadata_mutates_no_science_tables(
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

        persist_v25f_region_rule(
            storage
        )

        persist_v25f_metadata(
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
                "032v25f_global_rerank_recommended"
            )
            ==
            "1"
        )

    finally:
        storage.close()
