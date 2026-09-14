"""Regressions for 032H17A10C.

These tests protect the distinction between:

- representation support;
- direct source Ward compatibility;
- symmetry-forced Stueckelberg completion;
- exact physical pole overlap.

Passing this file must not be interpreted as a complete HOOK17 model.
"""

from __future__ import annotations

import numpy as np

from antigravity_research.agminer.hook17_marzo2022_engineered_stueckelberg_noether import (
    all_rank3_pair_traces,
    completed_marzo_abelian_ward_residual,
    direct_marzo_abelian_ward_residual,
    engineered_pair_noether_gate,
    engineered_pair_ps_tau,
    engineered_totally_symmetric_1minus_trace,
    h17a10c_summary,
    marzo_trace_covector,
    ps_tau_to_marzo_torsionfree_source,
    stueckelberg_invariant_combination_gate,
)
from antigravity_research.agminer.hook17_marzo2022_massive_source_match import (
    marzo2022_published_family_gate,
)


def test_marzo_family_is_published_protected_stueckelberg_1minus():
    result = marzo2022_published_family_gate()

    assert (
        result[
            "explicit_metric_affine_action_published"
        ]
        is True
    )

    assert (
        result[
            "protecting_abelian_symmetry_published"
        ]
        is True
    )

    assert (
        result[
            "stueckelberg_scalar_extension_published"
        ]
        is True
    )

    assert (
        result[
            "massive_extension_preserves_abelian_protection"
        ]
        is True
    )

    assert (
        result[
            "published_massive_physical_pole_sector"
        ]
        ==
        "1_MINUS"
    )


def test_engineered_source_maps_between_torsionfree_index_conventions():
    for pair_id in (
        "U1_V1",
        "U2_V2",
    ):
        tau = engineered_pair_ps_tau(
            pair_id
        )

        assert np.allclose(
            tau,
            np.swapaxes(
                tau,
                0,
                2,
            ),
            atol=
                1.0e-12,
            rtol=
                0.0,
        )

        source = (
            ps_tau_to_marzo_torsionfree_source(
                tau
            )
        )

        assert np.allclose(
            source,
            np.swapaxes(
                source,
                0,
                1,
            ),
            atol=
                1.0e-12,
            rtol=
                0.0,
        )


def test_engineered_marzo_trace_vectors_are_exact_equal_opposites():
    minus = marzo_trace_covector(
        ps_tau_to_marzo_torsionfree_source(
            engineered_pair_ps_tau(
                "U1_V1"
            )
        )
    )

    plus = marzo_trace_covector(
        ps_tau_to_marzo_torsionfree_source(
            engineered_pair_ps_tau(
                "U2_V2"
            )
        )
    )

    assert np.allclose(
        minus,
        np.array(
            [
                0.0,
                -4.0,
                0.0,
                0.0,
            ]
        ),
        atol=
            1.0e-12,
        rtol=
            0.0,
    )

    assert np.allclose(
        plus,
        -minus,
        atol=
            1.0e-12,
        rtol=
            0.0,
    )


def test_all_pair_trace_conventions_are_nonzero_and_collinear():
    result = all_rank3_pair_traces(
        engineered_pair_ps_tau(
            "U1_V1"
        )
    )

    assert np.allclose(
        result[
            "trace_01"
        ],
        np.array(
            [
                0.0,
                -2.0,
                0.0,
                0.0,
            ]
        ),
        atol=
            1.0e-12,
        rtol=
            0.0,
    )

    assert np.allclose(
        result[
            "trace_02"
        ],
        np.array(
            [
                0.0,
                -4.0,
                0.0,
                0.0,
            ]
        ),
        atol=
            1.0e-12,
        rtol=
            0.0,
    )

    assert np.allclose(
        result[
            "trace_12"
        ],
        np.array(
            [
                0.0,
                -2.0,
                0.0,
                0.0,
            ]
        ),
        atol=
            1.0e-12,
        rtol=
            0.0,
    )


def test_direct_pure_connection_source_fails_generic_abelian_ward():
    trace = np.array(
        [
            0.0,
            -4.0,
            0.0,
            0.0,
        ]
    )

    residual = (
        direct_marzo_abelian_ward_residual(
            trace,
            np.array(
                [
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                ]
            ),
        )
    )

    assert residual == -4.0


def test_stueckelberg_combination_is_exactly_invariant():
    result = (
        stueckelberg_invariant_combination_gate()
    )

    assert (
        result[
            "all_pass"
        ]
        is True
    )

    assert (
        result[
            "fixed_relative_coefficient"
        ]
        ==
        "MINUS_1_OVER_F"
    )

    assert (
        result[
            "state_dependent_source_surgery"
        ]
        is False
    )


def test_completed_source_ward_identity_holds_for_multiple_f_values():
    trace = np.array(
        [
            0.0,
            -4.0,
            0.0,
            0.0,
        ]
    )

    q = np.array(
        [
            0.7,
            -0.4,
            0.2,
            1.1,
        ]
    )

    for f in (
        1.0,
        -2.5,
        7.0,
    ):
        residual = (
            completed_marzo_abelian_ward_residual(
                trace,
                q,
                f,
            )
        )

        assert abs(
            residual
        ) < 1.0e-12


def test_engineered_1minus_representation_survives_completion():
    minus = (
        engineered_totally_symmetric_1minus_trace(
            "U1_V1"
        )
    )

    plus = (
        engineered_totally_symmetric_1minus_trace(
            "U2_V2"
        )
    )

    assert np.allclose(
        minus,
        np.array(
            [
                -8.0 / 3.0,
                0.0,
                0.0,
            ]
        ),
        atol=
            1.0e-12,
        rtol=
            0.0,
    )

    assert np.allclose(
        plus,
        -minus,
        atol=
            1.0e-12,
        rtol=
            0.0,
    )


def test_a10c_green_is_scaffold_only_not_exact_pole_or_torsion_claim():
    result = h17a10c_summary()

    assert (
        result[
            "partial_green"
        ]
        is True
    )

    assert (
        result[
            "linearized_local_abelian_invariant_matter_interaction_scaffold_exists"
        ]
        is True
    )

    assert (
        result[
            "full_covariant_dirac_matter_action_established"
        ]
        is False
    )

    assert (
        result[
            "full_engineered_wheeler_torsion_source_reconstructed"
        ]
        is False
    )

    assert (
        result[
            "exact_marzo_constrained_source_projector_evaluated"
        ]
        is False
    )

    assert (
        result[
            "exact_physical_1minus_pole_overlap_established"
        ]
        is False
    )


def test_a10c_promotes_only_exact_pole_gate_not_energy():
    result = h17a10c_summary()

    assert (
        result[
            "energy_optimization_authorized"
        ]
        is False
    )

    assert (
        result[
            "geometry_optimization_authorized"
        ]
        is False
    )

    assert (
        result[
            "agminer_database_mutation_authorized"
        ]
        is False
    )

    assert (
        result[
            "physical_antigravity_model_found"
        ]
        is False
    )

    assert (
        result[
            "certified_sub10mj_model_found"
        ]
        is False
    )

    assert (
        result[
            "hook17_closed"
        ]
        is False
    )

    assert (
        result[
            "next"
        ]
        ==
        (
            "032H17A10D_MARZO2022_EXACT_CONSTRAINED_1MINUS_"
            "SOURCE_PROJECTOR_RESIDUE_AND_CANONICAL_OVERLAP_GATE"
        )
    )
