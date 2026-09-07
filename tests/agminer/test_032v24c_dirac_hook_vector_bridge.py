"""Scientific regressions for 032V24C Dirac hook/vector bridge rerank."""

from __future__ import annotations

import math

import numpy as np

from antigravity_research.agminer.dirac_hook_vector_bridge import (
    generic_bms_spin1_trace_witness,
    hook_to_torsionlike,
    hook_torsionlike_map_diagnostics,
    marzo_2026_vector_graviton_bridge_template,
    persist_v24c_region_rules,
    pure_trace_symmetric_embedding,
    rest_pair_bms_spin1_trace_gate,
    rest_pair_source_parts,
    torsionlike_to_hook,
    trace_carrier_coupling_identity,
    v24c_frontier_rerank,
)
from antigravity_research.agminer.storage import Storage


def test_rest_pair_total_symmetric_trace_is_exactly_zero():
    result = rest_pair_bms_spin1_trace_gate()

    assert result[
        "rest_pair_total_symmetric_source_nonzero"
    ] is True

    assert result[
        "lorentz_trace_zero"
    ] is True

    assert result[
        "lorentz_trace_covector_norm"
    ] < 1.0e-12


def test_rest_pair_has_zero_direct_trace_carrier_overlap():
    result = rest_pair_bms_spin1_trace_gate()

    assert result[
        "direct_trace_carrier_overlap_zero"
    ] is True

    assert result[
        "maximum_direct_trace_carrier_overlap"
    ] < 1.0e-12


def test_trace_carrier_identity_holds_for_nontrivial_vector():
    source = rest_pair_source_parts()[
        "totally_symmetric"
    ]

    result = trace_carrier_coupling_identity(
        source,
        np.array(
            [
                0.3,
                -0.2,
                0.7,
                1.1,
            ]
        ),
    )

    assert result[
        "identity_pass"
    ] is True

    assert result[
        "relative_error"
    ] < 1.0e-12


def test_pure_trace_embedding_is_totally_symmetric():
    tensor = pure_trace_symmetric_embedding(
        np.array(
            [
                0.2,
                0.4,
                -0.1,
                0.8,
            ]
        )
    )

    assert np.allclose(
        tensor,
        np.transpose(
            tensor,
            (
                1,
                0,
                2,
            ),
        ),
    )

    assert np.allclose(
        tensor,
        np.transpose(
            tensor,
            (
                2,
                1,
                0,
            ),
        ),
    )


def test_rest_pair_direct_bms_spin1_closes_only_narrow_route():
    result = rest_pair_bms_spin1_trace_gate()

    assert result[
        "rest_pair_direct_bms_protected_spin1_source_closed"
    ] is True

    assert result[
        "generic_dirac_spin1_source_closed"
    ] is False

    assert result[
        "indirect_metric_mixing_source_closed"
    ] is False


def test_generic_dirac_algebraic_witness_has_nonzero_symmetric_trace():
    result = generic_bms_spin1_trace_witness()

    assert result[
        "generic_algebraic_trace_carrier_nonzero"
    ] is True

    assert result[
        "trace_covector_norm"
    ] > 1.0


def test_generic_trace_witness_is_not_promoted_to_physical_source():
    result = generic_bms_spin1_trace_witness()

    assert result[
        "spinor_is_on_shell_localized_stationary_source"
    ] is False

    assert result[
        "source_ward_identity_established"
    ] is False

    assert result[
        "support_energy_established"
    ] is False

    assert result[
        "generic_dirac_protected_spin1_closed"
    ] is False


def test_rest_pair_hook_source_is_nonzero():
    result = hook_torsionlike_map_diagnostics()

    assert result[
        "rest_pair_hook_source_nonzero"
    ] is True

    assert result[
        "rest_pair_hook_component_norm"
    ] > 1.0


def test_hook_maps_to_pair_antisymmetric_torsionlike_tensor():
    result = hook_torsionlike_map_diagnostics()

    assert result[
        "torsionlike_first_pair_antisymmetric"
    ] is True


def test_hook_torsionlike_map_is_invertible_for_rest_pair():
    result = hook_torsionlike_map_diagnostics()

    assert result[
        "pair_hook_roundtrip_relative_error"
    ] < 1.0e-12

    assert result[
        "representation_map_invertible_on_declared_hook_space"
    ] is True


def test_hook_torsionlike_map_is_invertible_for_generic_source():
    result = hook_torsionlike_map_diagnostics()

    assert result[
        "generic_hook_roundtrip_relative_error"
    ] < 1.0e-12


def test_rest_particle_antiparticle_same_sign_survives_hook_map():
    result = hook_torsionlike_map_diagnostics()

    assert result[
        "electron_positron_hook_same_sign"
    ] is True

    assert result[
        "electron_positron_torsionlike_same_sign"
    ] is True


def test_rest_pair_torsionlike_carrier_doubles_single_source():
    result = hook_torsionlike_map_diagnostics()

    assert result[
        "pair_torsionlike_equals_two_single"
    ] is True

    assert math.isclose(
        result[
            "pair_torsionlike_component_norm_over_single"
        ],
        2.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_representation_map_does_not_claim_action_or_energy_match():
    result = hook_torsionlike_map_diagnostics()

    assert result[
        "component_norm_is_lorentz_invariant"
    ] is False

    assert result[
        "component_norm_is_source_energy"
    ] is False

    assert result[
        "representation_map_is_physical_action_match"
    ] is False

    assert result[
        "healthy_propagating_vector_match_established"
    ] is False


def test_marzo_2026_template_has_quadratic_metric_vector_mixing_and_health():
    result = marzo_2026_vector_graviton_bridge_template()

    assert result[
        "quadratic_vector_graviton_mixing"
    ] is True

    assert result[
        "massless_spin2_propagates"
    ] is True

    assert result[
        "massive_spin1_propagates"
    ] is True

    assert result[
        "unitary_open_region_reported"
    ] is True


def test_marzo_2026_template_has_quartic_consistency_but_no_dirac_match():
    result = marzo_2026_vector_graviton_bridge_template()

    assert result[
        "consistent_cubic_deformation_found"
    ] is True

    assert result[
        "consistent_quartic_order_noether_test_passed"
    ] is True

    assert result[
        "external_dirac_source_coupling_derived"
    ] is False

    assert result[
        "vector_identified_with_v24c_hook_torsionlike_mode"
    ] is False

    assert result[
        "promotion_status"
    ] == "BRIDGE_TEMPLATE_ONLY"


def test_v24c_rerank_places_hook_and_marzo_bridge_at_top():
    rows = {
        row[
            "branch"
        ]:
            row
        for row
        in v24c_frontier_rerank()
    }

    assert rows[
        "DIRAC_HOOK_TO_TORSIONLIKE_PROTECTED_VECTOR_ACTION_MATCH"
    ][
        "priority"
    ] == 1

    assert rows[
        "MARZO_2026_QUADRATIC_VECTOR_GRAVITON_MIXING"
    ][
        "priority"
    ] == 1

    assert rows[
        "BMS_PROTECTED_TS_SPIN1_CLEAN_REST_PAIR_DIRECT"
    ][
        "status"
    ] == "CLOSED_ZERO_TRACE_SOURCE_OVERLAP"


def test_v24c_rule_is_idempotent_and_creates_no_models(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    try:
        first = persist_v24c_region_rules(
            storage
        )

        second = persist_v24c_region_rules(
            storage
        )

        assert first == 1
        assert second == 0

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

    finally:
        storage.close()
