"""Scientific regressions for 032V24D non-removable metric bridge gates."""

from __future__ import annotations

import json
import math

import numpy as np

from antigravity_research.agminer.nonremovable_vector_metric_bridge import (
    bms_2025_torsionlike_ir_metric_gate,
    independent_conserved_metric_source_demo,
    marzo_2026_linear_bridge_gate,
    maxwell_gradient_shift_diagnostic,
    persist_v24d_region_rules,
    pure_vector_ward_compensated_source,
    source_ward_diagonalization,
    stueckelberg_gauge_invariant_vector_residual,
    stueckelberg_square_coefficients,
    stueckelberg_square_numeric_identity,
    v24d_frontier_rerank,
)
from antigravity_research.agminer.storage import Storage


def test_marzo_mixed_block_has_exact_completed_square_coefficients():
    result = stueckelberg_square_coefficients(
        3.0
    )

    assert math.isclose(
        result[
            "v_squared"
        ],
        9.0,
    )

    assert math.isclose(
        result[
            "v_dot_gradient_h"
        ],
        -3.0,
    )

    assert math.isclose(
        result[
            "gradient_h_squared"
        ],
        0.25,
    )


def test_marzo_stueckelberg_square_numeric_identity():
    result = stueckelberg_square_numeric_identity(
        mass_scale=
            4.1,

        v_squared=
            1.7,

        v_dot_gradient_h=
            -0.6,

        gradient_h_squared=
            0.9,
    )

    assert result[
        "identity_pass"
    ] is True

    assert result[
        "relative_error"
    ] < 1.0e-14


def test_maxwell_kinetic_is_invariant_under_gradient_shift():
    result = maxwell_gradient_shift_diagnostic(
        vector_up=
            np.array(
                [
                    0.4,
                    -0.3,
                    1.2,
                    0.7,
                ]
            ),

        wavevector_cov=
            np.array(
                [
                    0.8,
                    0.6,
                    -0.2,
                    1.1,
                ]
            ),

        shift=
            0.51,
    )

    assert result[
        "gradient_shift_invariant"
    ] is True

    assert result[
        "relative_error"
    ] < 1.0e-12


def test_redefined_vector_is_invariant_under_shared_linear_gauge_symmetry():
    result = stueckelberg_gauge_invariant_vector_residual(
        gradient_parameter_cov=
            np.array(
                [
                    0.2,
                    -0.8,
                    0.4,
                    1.3,
                ]
            ),

        mass_scale=
            2.2,
    )

    assert result[
        "gauge_invariant"
    ] is True

    assert result[
        "delta_w_norm"
    ] < 1.0e-14


def test_conserved_vector_source_has_no_induced_linear_metric_source():
    result = source_ward_diagonalization(
        wavevector_cov=
            np.array(
                [
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                ]
            ),

        vector_current_up=
            np.array(
                [
                    1.0,
                    0.0,
                    0.7,
                    -0.3,
                ]
            ),

        metric_source_upup=
            np.zeros(
                (
                    4,
                    4,
                )
            ),

        mass_scale=
            2.5,
    )

    assert abs(
        result[
            "current_divergence"
        ]
    ) < 1.0e-14

    assert result[
        "source_ward_identity_pass"
    ] is True

    assert result[
        "transformed_metric_source_norm"
    ] < 1.0e-14


def test_nonconserved_vector_current_requires_metric_ward_compensator():
    result = pure_vector_ward_compensated_source(
        wavevector_cov=
            np.array(
                [
                    0.0,
                    1.0,
                    2.0,
                    -0.5,
                ]
            ),

        vector_current_up=
            np.array(
                [
                    0.4,
                    0.8,
                    -0.2,
                    0.3,
                ]
            ),

        mass_scale=
            3.2,
    )

    assert abs(
        result[
            "current_divergence"
        ]
    ) > 1.0e-3

    assert result[
        "source_ward_identity_pass"
    ] is True


def test_nonconserved_vector_ward_compensator_cancels_induced_metric_source():
    result = pure_vector_ward_compensated_source(
        wavevector_cov=
            np.array(
                [
                    0.0,
                    1.0,
                    2.0,
                    -0.5,
                ]
            ),

        vector_current_up=
            np.array(
                [
                    0.4,
                    0.8,
                    -0.2,
                    0.3,
                ]
            ),

        mass_scale=
            3.2,
    )

    assert result[
        "compensator_transforms_to_zero_metric_source"
    ] is True

    assert result[
        "transformed_metric_source_norm"
    ] < 1.0e-12


def test_ward_compatible_source_transforms_to_conserved_metric_source():
    result = pure_vector_ward_compensated_source(
        wavevector_cov=
            np.array(
                [
                    0.3,
                    1.0,
                    -0.7,
                    0.4,
                ]
            ),

        vector_current_up=
            np.array(
                [
                    0.2,
                    -0.4,
                    0.9,
                    0.1,
                ]
            ),

        mass_scale=
            1.8,
    )

    assert result[
        "source_ward_identity_pass"
    ] is True

    assert result[
        "transformed_metric_source_conserved"
    ] is True


def test_independent_conserved_metric_source_is_not_closed():
    result = independent_conserved_metric_source_demo()

    assert result[
        "current_is_conserved"
    ] is True

    assert result[
        "source_ward_identity_pass"
    ] is True

    assert result[
        "independent_metric_source_nonzero"
    ] is True

    assert result[
        "transformed_source_equals_original"
    ] is True


def test_ward_incompatible_external_source_is_detected():
    source = np.zeros(
        (
            4,
            4,
        )
    )

    source[
        1,
        1,
    ] = 4.0

    result = source_ward_diagonalization(
        wavevector_cov=
            np.array(
                [
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                ]
            ),

        vector_current_up=
            np.array(
                [
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                ]
            ),

        metric_source_upup=
            source,

        mass_scale=
            2.0,
    )

    assert result[
        "source_ward_identity_pass"
    ] is False

    assert result[
        "ward_residual_norm"
    ] > 1.0


def test_marzo_gate_closes_nonremovable_linear_vector_metric_portal():
    result = marzo_2026_linear_bridge_gate()

    assert result[
        "mixed_block_is_exact_stueckelberg_square"
    ] is True

    assert result[
        "maxwell_term_gradient_shift_invariant"
    ] is True

    assert result[
        "redefined_vector_gauge_invariant"
    ] is True

    assert result[
        "nonremovable_linear_vector_to_metric_cross_source"
    ] is False


def test_marzo_gate_does_not_close_nonlinear_completion_or_model():
    result = marzo_2026_linear_bridge_gate()

    assert result[
        "cubic_quartic_interactions_closed"
    ] is False

    assert result[
        "background_dependent_mixing_closed"
    ] is False

    assert result[
        "full_marzo_model_closed"
    ] is False

    assert result[
        "direct_dirac_hook_source_match_closed"
    ] is False


def test_bms_universal_ir_torsionlike_action_has_healthy_vectors():
    result = bms_2025_torsionlike_ir_metric_gate()

    assert result[
        "healthy_vector_torsion_modes_exist"
    ] is True

    assert result[
        "universal_ir_flat_space_action"
    ] is True


def test_bms_declared_universal_ir_action_has_no_metric_bridge():
    result = bms_2025_torsionlike_ir_metric_gate()

    assert result[
        "metric_perturbation_present_as_dynamical_field"
    ] is False

    assert result[
        "direct_universal_physical_metric_bridge_in_declared_ir_action"
    ] is False


def test_bms_gate_preserves_nonlinear_and_background_completions():
    result = bms_2025_torsionlike_ir_metric_gate()

    assert result[
        "nonlinear_poincare_completion_closed"
    ] is False

    assert result[
        "nonlinear_metric_affine_completion_closed"
    ] is False

    assert result[
        "background_dependent_metric_torsion_mixing_closed"
    ] is False

    assert result[
        "dirac_hook_source_closed"
    ] is False


def test_v24d_rerank_promotes_nonremovable_crosspropagator_search():
    rows = {
        row[
            "branch"
        ]:
            row
        for row
        in v24d_frontier_rerank()
    }

    assert rows[
        "NONREMOVABLE_INTRINSIC_SOURCE_TO_UNIVERSAL_METRIC_CROSS_PROPAGATOR"
    ][
        "priority"
    ] == 1

    assert rows[
        "NONREMOVABLE_INTRINSIC_SOURCE_TO_UNIVERSAL_METRIC_CROSS_PROPAGATOR"
    ][
        "status"
    ] == "HIGHEST_PRIORITY_GLOBAL_AGMINER_TARGET"


def test_v24d_rerank_preserves_dirac_hook_as_source_knowledge():
    rows = {
        row[
            "branch"
        ]:
            row
        for row
        in v24d_frontier_rerank()
    }

    result = rows[
        "DIRAC_HOOK_TORSIONLIKE_SOURCE"
    ]

    assert result[
        "status"
    ] == "PRESERVED_AS_SOURCE_KNOWLEDGE_NOT_ACTIVE_MODEL"

    assert result[
        "source_closed"
    ] is False

    assert result[
        "universal_metric_bridge_established"
    ] is False


def test_v24d_region_rules_are_idempotent(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    try:
        first = persist_v24d_region_rules(
            storage
        )

        second = persist_v24d_region_rules(
            storage
        )

        assert first == 2
        assert second == 0

    finally:
        storage.close()


def test_v24d_rules_create_no_candidates_rejections_or_promotions(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    try:
        persist_v24d_region_rules(
            storage
        )

        counts = {}

        for table in (
            "models",
            "rejections",
            "action_oracles",
            "mechanism_metrics",
        ):
            counts[
                table
            ] = int(
                storage.connection.execute(
                    f"SELECT COUNT(*) AS count FROM {table}"
                ).fetchone()[
                    "count"
                ]
            )

        assert counts == {
            "models":
                0,

            "rejections":
                0,

            "action_oracles":
                0,

            "mechanism_metrics":
                0,
        }

        rows = storage.connection.execute(
            """
            SELECT rule_json
            FROM region_rules
            ORDER BY rule_id
            """
        ).fetchall()

        assert len(
            rows
        ) == 2

        for row in rows:
            rule = json.loads(
                row[
                    "rule_json"
                ]
            )

            assert rule[
                "policy_specific"
            ] is False

            assert rule.get(
                "full_marzo_model_closed",
                False,
            ) is False

            assert rule.get(
                "full_torsionlike_theory_space_closed",
                False,
            ) is False

    finally:
        storage.close()
