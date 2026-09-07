"""Scientific regressions for 032V24A Dirac hypermomentum irrep preflight.

These tests protect the exact algebraic reconstruction and claim boundaries of
V24A. Passing them does not establish a propagating nonmetricity mode, a
universal metric bridge, finite-payload antigravity, or a sub-10-MJ model.
"""

from __future__ import annotations

import math

import numpy as np

from antigravity_research.agminer.dirac_hypermomentum_irrep import (
    direct_structureless_payload_gate,
    literature_intersection_atlas,
    persist_v24a_region_rules,
    quadratic_mixing_reciprocity,
    rest_spinup_special_case,
    source_irrep_diagnostics,
    weak_mixing_scaling_scout,
)
from antigravity_research.agminer.storage import Storage


GENERIC_SPINOR = np.array(
    [
        1.0 + 0.2j,
        0.3 - 0.4j,
        -0.2 + 0.9j,
        0.5 + 0.1j,
    ],
    dtype=np.complex128,
)


def test_wheeler_source_is_nonzero_and_symmetric_in_nonmetricity_pair():
    result = source_irrep_diagnostics(
        GENERIC_SPINOR
    )

    assert result[
        "nonmetricity_response_nonzero"
    ] is True

    assert result[
        "last_pair_symmetric"
    ] is True


def test_wheeler_source_has_exact_zero_weyl_dilation_trace():
    result = source_irrep_diagnostics(
        GENERIC_SPINOR
    )

    assert result[
        "weyl_dilation_trace_overlap_zero"
    ] is True

    assert result[
        "lorentz_trace_norm"
    ] < 1.0e-12

    assert result[
        "exact_propagating_spin_projector_overlap_established"
    ] is False


def test_rest_spinup_electron_matches_published_nonmetricity_case():
    result = rest_spinup_special_case()

    assert result[
        "electron_nonmetricity_matches_published_special_case"
    ] is True


def test_rest_spinup_positron_matches_and_has_same_nonmetricity_sign():
    result = rest_spinup_special_case()

    assert result[
        "positron_nonmetricity_matches_published_special_case"
    ] is True

    assert result[
        "equal_amplitude_particle_antiparticle_same_nonmetricity_sign"
    ] is True


def test_rest_pair_cancels_torsion_response_but_adds_nonmetricity_response():
    result = rest_spinup_special_case()

    assert result[
        "equal_amplitude_particle_antiparticle_opposite_torsion_sign"
    ] is True

    assert result[
        "pair_torsion_response_cancels"
    ] is True

    assert result[
        "pair_nonmetricity_response_adds"
    ] is True

    assert math.isclose(
        result[
            "pair_nonmetricity_component_norm_over_single"
        ],
        2.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_pair_witness_does_not_claim_hidden_charge_or_energy_closure():
    result = rest_spinup_special_case()

    assert result[
        "pair_hidden_vector_charge_cancellation_established"
    ] is False

    assert result[
        "pair_total_spin_cancellation_established"
    ] is False

    assert result[
        "pair_support_cost_established"
    ] is False

    assert result[
        "pair_source_energy_established"
    ] is False


def test_rest_source_contains_both_total_symmetric_and_hook_carriers():
    result = (
        rest_spinup_special_case()[
            "electron_irrep"
        ]
    )

    assert result[
        "totally_symmetric_carrier_nonzero"
    ] is True

    assert result[
        "hook_symmetric_carrier_nonzero"
    ] is True


def test_rest_source_component_norm_split_is_one_third_two_thirds():
    result = (
        rest_spinup_special_case()[
            "electron_irrep"
        ]
    )

    assert math.isclose(
        result[
            "component_totally_symmetric_norm_fraction"
        ],
        1.0
        /
        3.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "component_hook_symmetric_norm_fraction"
        ],
        2.0
        /
        3.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert result[
        "component_norm_is_lorentz_invariant"
    ] is False

    assert result[
        "component_norm_is_field_energy"
    ] is False


def test_algebraic_decomposition_reconstructs_and_is_component_orthogonal():
    result = source_irrep_diagnostics(
        GENERIC_SPINOR
    )

    assert result[
        "decomposition_reconstruction_relative_error"
    ] < 1.0e-12

    assert abs(
        result[
            "decomposition_orthogonality_relative_inner_product"
        ]
    ) < 1.0e-12


def test_intersection_atlas_closes_only_the_exactly_killed_routes():
    rows = {
        row[
            "sector"
        ]:
            row

        for row
        in literature_intersection_atlas()
    }

    assert rows[
        "WEYL_DILATION_TRACE"
    ][
        "status"
    ] == (
        "CLOSED_FOR_EXPLICIT_WHEELER_DIRAC_SOURCE"
    )

    assert rows[
        "WEYL_DILATION_TRACE"
    ][
        "wheeler_dirac_algebraic_overlap"
    ] is False

    assert rows[
        "TOTALLY_SYMMETRIC_TRACEFREE"
    ][
        "status"
    ] == (
        "OPEN_FOR_EXACT_PROJECTOR_AND_METRIC_BRIDGE_TEST"
    )

    assert rows[
        "HOOK_SYMMETRIC_TRACEFREE"
    ][
        "status"
    ] == (
        "OPEN_FOR_EXACT_PROJECTOR_AND_METRIC_BRIDGE_TEST"
    )

    assert rows[
        "TOTALLY_SYMMETRIC_TRACEFREE"
    ][
        "exact_spin_projector_overlap_established"
    ] is False

    assert rows[
        "HOOK_SYMMETRIC_TRACEFREE"
    ][
        "exact_spin_projector_overlap_established"
    ] is False


def test_structureless_payload_direct_connection_force_is_not_universal_bridge():
    result = (
        direct_structureless_payload_gate()
    )

    assert result[
        "payload_intrinsic_hypermomentum"
    ] is False

    assert result[
        "direct_post_riemannian_microstructure_force_available"
    ] is False

    assert result[
        "usual_riemannian_geodesic_recovered"
    ] is True

    assert result[
        "universal_metric_backreaction_closed"
    ] is False

    assert result[
        "universal_physical_metric_bridge_established"
    ] is False


def test_quadratic_mixing_reciprocity_identity_is_exact_for_healthy_block():
    result = (
        quadratic_mixing_reciprocity(
            visible_inverse_propagator=
                2.0,

            hidden_inverse_propagator=
                3.0,

            mixing=
                0.4,
        )
    )

    assert result[
        "healthy_positive_quadratic_block"
    ] is True

    assert result[
        "reciprocity_identity_relative_error"
    ] < 1.0e-12

    assert result[
        "weak_mixing_cross_order"
    ] == 1

    assert result[
        "weak_mixing_visible_offstate_order"
    ] == 2

    assert result[
        "physical_action_match_established"
    ] is False


def test_weak_mixing_cross_is_linear_while_visible_offstate_is_quadratic():
    rows = (
        weak_mixing_scaling_scout(
            (
                1.0e-2,
                1.0e-3,
            )
        )
    )

    cross_ratio = (
        rows[
            0
        ][
            "abs_cross_response"
        ]
        /
        rows[
            1
        ][
            "abs_cross_response"
        ]
    )

    offstate_ratio = (
        rows[
            0
        ][
            "visible_offstate_correction"
        ]
        /
        rows[
            1
        ][
            "visible_offstate_correction"
        ]
    )

    assert (
        9.9
        <
        cross_ratio
        <
        10.1
    )

    assert (
        99.0
        <
        offstate_ratio
        <
        101.0
    )


def test_unhealthy_quadratic_mixing_block_is_rejected_before_inversion_claims():
    result = (
        quadratic_mixing_reciprocity(
            visible_inverse_propagator=
                1.0,

            hidden_inverse_propagator=
                1.0,

            mixing=
                1.1,
        )
    )

    assert result[
        "healthy_positive_quadratic_block"
    ] is False

    assert result[
        "cross_response"
    ] is None

    assert result[
        "visible_offstate_correction"
    ] is None


def test_v24a_region_rules_are_idempotent(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    try:
        first = (
            persist_v24a_region_rules(
                storage
            )
        )

        second = (
            persist_v24a_region_rules(
                storage
            )
        )

        assert first == 2
        assert second == 0

    finally:
        storage.close()


def test_v24a_failure_memory_does_not_create_models_or_promotions(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    try:
        persist_v24a_region_rules(
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

    finally:
        storage.close()
