"""Regression tests for 032H17A8."""

import math

from antigravity_research.agminer.hook17_native_protected_2plus_atlas import (
    HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    a7_provenance_gate,
    bms_pair_antisymmetric_spin2_protection_gate,
    clean_v24_projective_spin_rerank_gate,
    clean_v24_projective_trace_gate,
    h17a8_summary,
    mikura_percacci_hook_2plus_gate,
    percacci_sezgin_projective_family_gate,
    protected_2plus_atlas_rows,
)


def test_a7_provenance_is_green():
    result = a7_provenance_gate()

    assert (
        result[
            "a7_provenance_pass"
        ]
        is True
    )

    assert (
        result[
            "iw_direct_clean_route_closed"
        ]
        is True
    )

    assert (
        result[
            "clean_1plus_survives"
        ]
        is True
    )

    assert (
        result[
            "clean_2plus_survives"
        ]
        is True
    )


def test_bms_catalogue_has_no_assessed_symmetry_protected_spin2():
    result = bms_pair_antisymmetric_spin2_protection_gate()

    assert (
        result[
            "candidate_symmetric_ir_foundations"
        ]
        ==
        206
    )

    assert (
        result[
            "confirmed_unitary_models"
        ]
        ==
        22
    )

    assert (
        result[
            "confirmed_unitary_modes_vector_only"
        ]
        is True
    )

    assert (
        result[
            "symmetry_supporting_spin_two_found"
        ]
        is False
    )

    assert (
        result[
            "protected_2plus_survivor_in_assessed_catalogue"
        ]
        is False
    )


def test_bms_result_is_scoped_not_global():
    result = bms_pair_antisymmetric_spin2_protection_gate()

    assert (
        result[
            "all_possible_protected_spin2_globally_closed"
        ]
        is False
    )

    assert (
        result[
            "parity_violating_extensions_closed"
        ]
        is False
    )

    assert (
        result[
            "nonlinear_completions_closed"
        ]
        is False
    )


def test_mikura_percacci_has_healthy_but_unprotected_2plus():
    result = mikura_percacci_hook_2plus_gate()

    assert (
        result[
            "healthy_massive_2plus_exists"
        ]
        is True
    )

    assert (
        result[
            "published_ghost_free_condition_m1qq_negative"
        ]
        is True
    )

    assert (
        result[
            "published_ghost_free_condition_b6qq_negative"
        ]
        is True
    )

    assert (
        result[
            "analysis_assumes_only_diffeomorphism_gauge_symmetry"
        ]
        is True
    )


def test_mikura_percacci_2plus_does_not_pass_hook17_protection_gate():
    result = mikura_percacci_hook_2plus_gate()

    assert (
        result[
            "additional_gauge_symmetry_protects_2plus_tuning"
        ]
        is False
    )

    assert (
        result[
            "radiative_protection_of_single_state_tuning_established"
        ]
        is False
    )

    assert (
        result[
            "hook17_protection_gate_pass"
        ]
        is False
    )

    assert (
        result[
            "energy_scan_authorized"
        ]
        is False
    )


def test_percacci_sezgin_projective_family_has_no_extra_massive_2plus():
    result = percacci_sezgin_projective_family_gate()

    assert (
        result[
            "projective_invariance"
        ]
        is True
    )

    assert (
        result[
            "ghost_tachyon_free_subclass_exists"
        ]
        is True
    )

    assert (
        result[
            "massless_graviton_2plus_propagates"
        ]
        is True
    )

    assert (
        result[
            "massive_2plus_propagates"
        ]
        is False
    )

    assert (
        result[
            "massive_2minus_propagates"
        ]
        is True
    )

    assert (
        result[
            "massive_1plus_propagates"
        ]
        is True
    )


def test_clean_v24_passes_both_projective_source_trace_constraints():
    result = clean_v24_projective_trace_gate()

    assert (
        result[
            "source_nonzero"
        ]
        is True
    )

    assert (
        result[
            "projective_constraint_tau_nu_nu_mu_pass"
        ]
        is True
    )

    assert (
        result[
            "projective_constraint_tau_mu_nu_nu_pass"
        ]
        is True
    )

    assert (
        result[
            "both_projective_source_trace_constraints_pass"
        ]
        is True
    )

    assert math.isclose(
        result[
            "trace_first_second_norm"
        ],
        0.0,
        abs_tol=
            1.0e-12,
    )

    assert math.isclose(
        result[
            "trace_second_third_norm"
        ],
        0.0,
        abs_tol=
            1.0e-12,
    )


def test_projective_rerank_preserves_1plus_but_rejects_2minus_clean_route():
    result = clean_v24_projective_spin_rerank_gate()

    assert (
        result[
            "projective_source_trace_constraints_pass"
        ]
        is True
    )

    assert (
        result[
            "clean_hook_2minus_support_zero"
        ]
        is True
    )

    assert (
        result[
            "direct_clean_v24_projective_2minus_route_supported"
        ]
        is False
    )

    assert (
        result[
            "clean_hook_1plus_support_nonzero"
        ]
        is True
    )

    assert (
        result[
            "projective_1plus_exact_source_match_authorized"
        ]
        is True
    )

    assert (
        result[
            "projective_1plus_already_certified"
        ]
        is False
    )


def test_current_protected_2plus_atlas_has_zero_survivors():
    rows = protected_2plus_atlas_rows()

    survivors = [
        row
        for row in rows
        if row[
            "protected_2plus_survivor"
        ]
    ]

    assert survivors == []


def test_a8_summary_is_scoped_red_and_promotes_projective_1plus():
    result = h17a8_summary()

    assert (
        result[
            "decision"
        ].startswith(
            "RED_SCOPED_A8_"
        )
    )

    assert (
        result[
            "current_declared_protected_2plus_atlas_survivor_count"
        ]
        ==
        0
    )

    assert (
        result[
            "current_declared_protected_2plus_atlas_closed"
        ]
        is True
    )

    assert (
        result[
            "all_possible_protected_2plus_globally_closed"
        ]
        is False
    )

    assert (
        result[
            "clean_v24_projective_source_trace_constraints_pass"
        ]
        is True
    )

    assert (
        result[
            "projective_1plus_exact_source_match_authorized"
        ]
        is True
    )

    assert result[
        "next"
    ] == (
        "032H17A9_PERCACCI_SEZGIN_PROJECTIVE_"
        "1PLUS_EXACT_SOURCE_PROJECTOR_WARD_GATE"
    )


def test_a8_preserves_hook17_capacity_and_blocks_energy_optimization():
    result = h17a8_summary()

    assert math.isclose(
        result[
            "hook17_reference_capacity_rp1e12_j"
        ],
        HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    )

    assert (
        result[
            "hook17_complete_energy_j"
        ]
        is None
    )

    assert (
        result[
            "energy_optimization_authorized"
        ]
        is False
    )

    assert (
        result[
            "capacity_recalculation_authorized"
        ]
        is False
    )

    assert (
        result[
            "h17b_authorized"
        ]
        is False
    )

    assert (
        result[
            "hook17_closed"
        ]
        is False
    )
