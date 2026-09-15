"""Regressions for 032H17A11C exact on-shell Dirac / K2 closeout."""

from __future__ import annotations

import sympy as sp

from antigravity_research.agminer.hook17_k2_onshell_dirac_bilinear import (
    FULL_K2_WITNESS_ROWS,
    TRANSITION_LABELS,
    breit_transition_source_basis,
    exact_breit_k2_theorem,
    h17a11c_summary,
    k2_full_source_constraint_count_validation,
    operator_reconstruction_validation,
)


def test_wheeler_operator_reconstruction_is_exact():
    result = operator_reconstruction_validation()

    assert result[
        "operator_reconstruction_pass"
    ] is True

    assert result[
        "maximum_operator_reconstruction_error"
    ] < 1.0e-12


def test_breit_basis_spans_all_same_frequency_spin_transitions():
    basis = breit_transition_source_basis()

    assert tuple(
        label
        for label, _ in basis
    ) == TRANSITION_LABELS

    assert len(
        basis
    ) == 8


def test_k2_source_representation_reconstructs_21_constraints():
    result = (
        k2_full_source_constraint_count_validation()
    )

    assert result[
        "pair_antisymmetric_source_dimension"
    ] == 24

    assert result[
        "trace_vector_subspace_dimension"
    ] == 4

    assert result[
        "pure_trace_constraint_rank"
    ] == 20

    assert result[
        "current_conservation_additional_rank"
    ] == 1

    assert result[
        "full_k2_independent_constraint_rank"
    ] == 21

    assert result[
        "k2_admissible_source_dimension_at_nonzero_breit_q"
    ] == 3

    assert result[
        "published_constraint_count_match"
    ] is True


def test_particle_only_nonrest_source_has_no_finite_ward_escape():
    result = exact_breit_k2_theorem()

    assert result[
        "particle_only_necessary_ward_determinant"
    ] == (
        "-z**3*(z - 1)*(z + 1)*(z**2 + 3)/4"
    )


def test_antiparticle_only_nonrest_source_has_no_finite_ward_escape():
    result = exact_breit_k2_theorem()

    assert result[
        "antiparticle_only_necessary_ward_determinant"
    ] == (
        "z*(z - 1)*(z + 1)*(3*z**2 + 1)/4"
    )


def test_a11b_necessary_ward_alone_has_false_nonrest_survivors():
    result = exact_breit_k2_theorem()

    assert result[
        "combined_necessary_ward_rank"
    ] == 4

    assert result[
        "combined_necessary_ward_nullity"
    ] == 4

    assert result[
        "combined_necessary_ward_source_image_rank"
    ] == 4

    assert result[
        "necessary_ward_nonzero_survivors_exist"
    ] is True


def test_exact_minor_proves_full_rank_for_every_finite_transfer():
    result = exact_breit_k2_theorem()

    assert result[
        "full_k2_witness_rows"
    ] == list(
        FULL_K2_WITNESS_ROWS
    )

    assert result[
        "full_k2_witness_identity_pass"
    ] is True

    assert result[
        "full_k2_witness_determinant"
    ] == (
        "z**2*(z - 1)**4*(z + 1)**4*(z**2 + 1)**2/2592"
    )

    assert result[
        "full_k2_witness_real_roots_inside_0_1"
    ] == []

    assert result[
        "full_k2_rank_is_eight_for_every_finite_nonzero_transfer"
    ] is True

    assert result[
        "nonzero_full_k2_admissible_onshell_dirac_source_exists"
    ] is False


def test_exact_sample_ranks_match_global_theorem():
    result = exact_breit_k2_theorem()

    assert len(
        result[
            "sample_rank_checks"
        ]
    ) == 5

    for row in result[
        "sample_rank_checks"
    ]:
        assert row[
            "full_k2_constraint_rank"
        ] == 8

        assert row[
            "full_k2_nullity"
        ] == 0

        assert sp.Rational(
            row[
                "witness_minor"
            ]
        ) != 0


def test_only_rank_losses_are_unusable_boundaries():
    result = exact_breit_k2_theorem()

    assert result[
        "z0_full_constraint_rank"
    ] == 6

    assert result[
        "z0_full_constraint_nullity"
    ] == 2

    assert result[
        "z0_interpretation"
    ] == (
        "ZERO_MOMENTUM_TRANSFER_NO_STANDOFF_GRADIENT"
    )

    assert result[
        "z1_full_constraint_rank"
    ] == 4

    assert result[
        "z1_full_constraint_nullity"
    ] == 4

    assert result[
        "z1_interpretation"
    ] == (
        "INFINITE_RAPIDITY_INFINITE_Q_OVER_M_BOUNDARY"
    )


def test_a11c_closes_only_direct_ordinary_dirac_k2_route():
    result = h17a11c_summary()

    assert result[
        "a11b_provenance"
    ] is True

    assert result[
        "important_intermediate_fact_a11b_necessary_ward_can_be_cancelled_nonrest"
    ] is True

    assert result[
        "important_final_fact_full_k2_constraints_remove_all_finite_nonzero_survivors"
    ] is True

    assert result[
        "direct_k2_ordinary_dirac_onshell_wheeler_route_closed"
    ] is True

    assert result[
        "k2_with_other_microscopic_sources_closed"
    ] is False

    assert result[
        "derivative_or_composite_source_completions_closed"
    ] is False

    assert result[
        "noether_compensated_source_completions_closed"
    ] is False

    assert result[
        "interacting_bound_state_dirac_sources_closed"
    ] is False

    assert result[
        "all_massless_torsion_vector_families_closed"
    ] is False

    assert result[
        "healthy_pole_evaluation_authorized"
    ] is False

    assert result[
        "metric_gate_authorized"
    ] is False

    assert result[
        "payload_gate_authorized"
    ] is False

    assert result[
        "energy_optimization_authorized"
    ] is False

    assert result[
        "hook17_closed"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False

    assert result[
        "next"
    ] == (
        "032H17A12_PROTECTED_SOURCE_FAMILY_RERANK_AFTER_DIRECT_K2_"
        "ORDINARY_DIRAC_CLOSEOUT"
    )
