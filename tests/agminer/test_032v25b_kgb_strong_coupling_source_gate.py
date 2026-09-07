"""Scientific regressions for 032V25B KGB source-scale control."""

from __future__ import annotations

import math

from antigravity_research.agminer.kgb_strong_coupling_source_gate import (
    V16_SOURCE_C_M,
    gain_to_y,
    historical_source_compatibility,
    historical_v16_source_benchmark,
    max_gain_for_gradient_cap,
    persist_v25b_metadata,
    persist_v25b_region_rule,
    positive_2x2_mixing_diagnostics,
    protection_rg_scope,
    required_gradient_for_control,
    v25b_gate,
    y_to_gain,
)
from antigravity_research.agminer.storage import (
    Storage,
)


def test_gain_y_roundtrip():
    for gain in (
        1.0e-6,
        1.0e-3,
        0.1,
        1.0,
        10.0,
    ):
        assert math.isclose(
            y_to_gain(
                gain_to_y(
                    gain
                )
            ),
            gain,
            rel_tol=
                2.0e-12,
        )


def test_v16_gradient_reconstruction():
    result = historical_v16_source_benchmark()

    assert math.isclose(
        result[
            "gradient_ev2"
        ],
        551.6084480921974,
        rel_tol=
            1.0e-14,
    )


def test_v16_source_momentum_reconstruction():
    result = historical_v16_source_benchmark()

    assert math.isclose(
        result[
            "source_variation_momentum_ev"
        ],
        2.042908256505853e-6,
        rel_tol=
            1.0e-14,
    )


def test_v16_a1e3_local_control_ratio_is_below_one():
    result = historical_source_compatibility()

    assert math.isclose(
        result[
            "a1e3_lambda_eff_over_source_k"
        ],
        0.19423543641148613,
        rel_tol=
            2.0e-12,
    )

    assert (
        result[
            "a1e3_lambda_eff_over_source_k"
        ]
        <
        1.0
    )


def test_actual_v16_gradient_max_controlled_gain():
    result = historical_source_compatibility()

    assert math.isclose(
        result[
            "actual_gradient_max_controlled_gain_times_planck"
        ],
        7.328013583046044e-6,
        rel_tol=
            2.0e-9,
    )


def test_hard_margin_proxy_max_controlled_gain():
    result = historical_source_compatibility()

    assert math.isclose(
        result[
            "hard_margin_proxy_max_controlled_gain_times_planck"
        ],
        7.875181868209245e-5,
        rel_tol=
            2.0e-9,
    )


def test_relaxed_cutoff_max_controlled_gain():
    result = historical_source_compatibility()

    assert math.isclose(
        result[
            "relaxed_cutoff_max_controlled_gain_times_planck"
        ],
        0.002064809831590992,
        rel_tol=
            2.0e-9,
    )


def test_hard_margin_proxy_margin5_is_tiny():
    result = historical_source_compatibility()

    assert math.isclose(
        result[
            "hard_margin_proxy_margin5_max_gain_times_planck"
        ],
        6.300145572707496e-7,
        rel_tol=
            3.0e-9,
    )


def test_relaxed_cutoff_margin5_remains_small():
    result = historical_source_compatibility()

    assert math.isclose(
        result[
            "relaxed_cutoff_margin5_max_gain_times_planck"
        ],
        1.6518619494786622e-5,
        rel_tol=
            3.0e-9,
    )


def test_required_gradient_for_a1e3_exceeds_historical_gradient():
    required = required_gradient_for_control(
        length_m=
            V16_SOURCE_C_M,

        gain_times_planck=
            1.0e-3,
    )

    assert required > 6000.0


def test_required_gradient_for_planck_strength_is_large():
    required = required_gradient_for_control(
        length_m=
            V16_SOURCE_C_M,

        gain_times_planck=
            1.0,
    )

    assert required > 3.0e5


def test_required_gradient_grows_with_requested_gain():
    low = required_gradient_for_control(
        length_m=
            V16_SOURCE_C_M,

        gain_times_planck=
            0.1,
    )

    high = required_gradient_for_control(
        length_m=
            V16_SOURCE_C_M,

        gain_times_planck=
            1.0,
    )

    assert low < high


def test_positive_2x2_inverse_cross_identity():
    result = positive_2x2_mixing_diagnostics(
        metric_kinetic=
            2.0,

        scalar_kinetic=
            3.0,

        mixing=
            0.5,
    )

    assert result[
        "healthy"
    ] is True

    assert result[
        "normalized_identity_error"
    ] < 1.0e-14


def test_large_normalized_mixing_approaches_kinetic_degeneracy():
    result = positive_2x2_mixing_diagnostics(
        metric_kinetic=
            1.0,

        scalar_kinetic=
            1.0,

        mixing=
            0.99,
    )

    assert result[
        "absolute_rho"
    ] < 1.0

    assert result[
        "smallest_eigenvalue"
    ] < 0.02

    assert result[
        "arbitrarily_large_normalized_cross_without_degeneracy"
    ] is False


def test_unhealthy_2x2_block_is_detected():
    result = positive_2x2_mixing_diagnostics(
        metric_kinetic=
            1.0,

        scalar_kinetic=
            1.0,

        mixing=
            1.1,
    )

    assert result[
        "healthy"
    ] is False


def test_wbg_protection_context_is_partial_not_full_rg_certificate():
    result = protection_rg_scope()

    assert result[
        "constant_shift_exact"
    ] is True

    assert result[
        "bulk_weakly_broken_galileon_protection_context"
    ] is True

    assert result[
        "hidden_axial_source_preserves_full_galileon_shift_phi_to_phi_plus_bx"
    ] is False

    assert result[
        "full_source_coupled_naturalness_certified"
    ] is False


def test_v25b_gate_is_narrow_red_and_preserves_generalized_kgb():
    result = v25b_gate()

    assert result[
        "unchanged_v16_minimal_cubic_transplant_closed"
    ] is True

    assert result[
        "generalized_kx_g3_closed"
    ] is False

    assert result[
        "wbg_multiscale_kgb_closed"
    ] is False

    assert result[
        "action_oracle_authorized"
    ] is False


def test_v25b_gate_makes_no_sign_payload_or_device_claim():
    result = v25b_gate()

    assert result[
        "outward_sign_established"
    ] is False

    assert result[
        "finite_payload_response_established"
    ] is False

    assert result[
        "source_charge_per_joule_established"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False


def test_v25b_region_rule_is_idempotent(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    try:
        first = persist_v25b_region_rule(
            storage
        )

        second = persist_v25b_region_rule(
            storage
        )

        assert first == 1
        assert second == 0

    finally:
        storage.close()


def test_v25b_rule_and_metadata_mutate_no_science_tables(
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

        persist_v25b_region_rule(
            storage
        )

        persist_v25b_metadata(
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

        region_count = int(
            storage.connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM region_rules
                """
            ).fetchone()[
                "count"
            ]
        )

        assert region_count == 1

        assert (
            storage.get_metadata(
                "032v25b_action_oracle_authorized"
            )
            ==
            "0"
        )

    finally:
        storage.close()
