"""Scientific regressions for 032V25D large-KX source reaction."""

from __future__ import annotations

import math

import pytest

from antigravity_research.agminer.kx_source_reaction_gate import (
    canonical_source_normalization,
    fixed_gradient_gain_preserving_scaling,
    fixed_source_gain_preserving_scaling,
    historical_v16_kx_gate,
    local_constant_kx_theorem,
    persist_v25d_metadata,
    persist_v25d_region_rule,
    required_kappa_for_fixed_gradient_control,
    v25d_gate,
)
from antigravity_research.agminer.storage import (
    Storage,
)


BASELINE = 0.19423543641148613


def test_kappa_must_be_at_least_one():
    with pytest.raises(
        ValueError
    ):
        canonical_source_normalization(
            0.5
        )


def test_canonical_hidden_source_coupling_scales_inverse_sqrt_kappa():
    result = canonical_source_normalization(
        100.0
    )

    assert math.isclose(
        result[
            "canonical_hidden_source_coupling_relative"
        ],
        0.1,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )


def test_fixed_source_background_gradient_scales_inverse_kappa():
    result = fixed_source_gain_preserving_scaling(
        kappa=
            10.0,

        baseline_control_ratio=
            BASELINE,
    )

    assert math.isclose(
        result[
            "background_gradient_relative"
        ],
        0.1,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )


def test_fixed_source_canonical_gradient_scales_inverse_sqrt_kappa():
    result = fixed_source_gain_preserving_scaling(
        kappa=
            100.0,

        baseline_control_ratio=
            BASELINE,
    )

    assert math.isclose(
        result[
            "canonical_background_gradient_relative"
        ],
        0.1,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )


def test_fixed_source_required_linear_g3_grows_kappa_five_halves():
    result = fixed_source_gain_preserving_scaling(
        kappa=
            10.0,

        baseline_control_ratio=
            BASELINE,
    )

    assert math.isclose(
        result[
            "required_linear_g3_coefficient_relative"
        ],
        316.22776601683796,
        rel_tol=1.0e-14,
    )


def test_fixed_source_local_control_gets_worse_with_kappa():
    result = fixed_source_gain_preserving_scaling(
        kappa=
            10.0,

        baseline_control_ratio=
            BASELINE,
    )

    assert math.isclose(
        result[
            "control_ratio"
        ],
        0.09015610327394591,
        rel_tol=1.0e-14,
    )

    assert (
        result[
            "control_ratio"
        ]
        <
        BASELINE
    )


def test_fixed_source_kappa1000_is_even_worse():
    result = fixed_source_gain_preserving_scaling(
        kappa=
            1000.0,

        baseline_control_ratio=
            BASELINE,
    )

    assert math.isclose(
        result[
            "control_ratio"
        ],
        0.01942354364114862,
        rel_tol=1.0e-14,
    )


def test_fixed_gradient_source_drive_scales_as_kappa():
    result = fixed_gradient_gain_preserving_scaling(
        kappa=
            10.0,

        baseline_control_ratio=
            BASELINE,
    )

    assert math.isclose(
        result[
            "source_drive_multiplier"
        ],
        10.0,
    )


def test_fixed_gradient_linear_g3_coefficient_grows_sqrt_kappa():
    result = fixed_gradient_gain_preserving_scaling(
        kappa=
            100.0,

        baseline_control_ratio=
            BASELINE,
    )

    assert math.isclose(
        result[
            "required_linear_g3_coefficient_relative"
        ],
        10.0,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )


def test_fixed_gradient_local_scale_improves_only_cube_root():
    result = fixed_gradient_gain_preserving_scaling(
        kappa=
            1000.0,

        baseline_control_ratio=
            BASELINE,
    )

    assert math.isclose(
        result[
            "local_canonical_scale_relative"
        ],
        10.0,
        rel_tol=1.0e-14,
    )


def test_unit_control_requires_about_136x_source_drive():
    result = required_kappa_for_fixed_gradient_control(
        baseline_control_ratio=
            BASELINE,

        target_control_ratio=
            1.0,
    )

    assert math.isclose(
        result[
            "required_kappa"
        ],
        136.46290206205185,
        rel_tol=1.0e-13,
    )

    assert (
        result[
            "required_source_drive_multiplier"
        ]
        >
        136.0
    )


def test_fivefold_control_margin_requires_about_17058x_source_drive():
    result = required_kappa_for_fixed_gradient_control(
        baseline_control_ratio=
            BASELINE,

        target_control_ratio=
            5.0,
    )

    assert math.isclose(
        result[
            "required_kappa"
        ],
        17057.86275775648,
        rel_tol=1.0e-13,
    )


def test_required_kappa_reconstructs_target_ratio():
    result = required_kappa_for_fixed_gradient_control(
        baseline_control_ratio=
            BASELINE,

        target_control_ratio=
            1.0,
    )

    assert math.isclose(
        result[
            "reconstructed_control_ratio"
        ],
        1.0,
        rel_tol=1.0e-14,
    )


def test_large_kappa_also_suppresses_canonical_source_coupling():
    result = required_kappa_for_fixed_gradient_control(
        baseline_control_ratio=
            BASELINE,

        target_control_ratio=
            5.0,
    )

    assert (
        result[
            "canonical_source_coupling_relative"
        ]
        <
        0.008
    )


def test_declared_power_law_theorem_preserves_nonlinear_escape_routes():
    result = local_constant_kx_theorem()

    assert math.isclose(
        result[
            "fixed_source_local_scale_exponent"
        ],
        -1.0 / 3.0,
    )

    assert (
        result[
            "nonlinear_kxx_closed"
        ]
        is False
    )

    assert (
        result[
            "nonlinear_g3xx_closed"
        ]
        is False
    )


def test_historical_v16_gate_closes_only_fixed_source_constant_kx_rescue():
    result = historical_v16_kx_gate()

    assert (
        result[
            "unchanged_source_large_constant_kx_rescue_closed"
        ]
        is True
    )

    assert (
        result[
            "nonlinear_kxx_closed"
        ]
        is False
    )

    assert (
        result[
            "nonlinear_g3xx_closed"
        ]
        is False
    )


def test_source_drive_multiplier_is_not_mislabeled_as_energy():
    result = historical_v16_kx_gate()

    assert (
        result[
            "source_energy_multiplier_established"
        ]
        is False
    )


def test_v25d_gate_makes_no_model_or_energy_claim():
    result = v25d_gate()

    assert (
        result[
            "source_energy_cost_established"
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


def test_v25d_region_rule_is_idempotent(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    try:
        first = persist_v25d_region_rule(
            storage
        )

        second = persist_v25d_region_rule(
            storage
        )

        assert first == 1
        assert second == 0

    finally:
        storage.close()


def test_v25d_rule_metadata_mutate_no_science_tables(
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

        persist_v25d_region_rule(
            storage
        )

        persist_v25d_metadata(
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
                "032v25d_action_oracle_authorized"
            )
            ==
            "0"
        )

    finally:
        storage.close()
