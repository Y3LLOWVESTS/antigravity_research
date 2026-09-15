"""Regressions for 032H17A12D0 low-capacity F^2 completion atlas."""

from __future__ import annotations

import math

from antigravity_research.agminer.hook17_low_capacity_f2_completion_atlas import (
    completion_combination_atlas,
    field_sector_portal_atlas,
    frozen_low_capacity_reference,
    h17a12d0_summary,
    open_completion_rerank,
    provenance_gate,
    quadratic_fieldstrength_metric_basis_theorem,
    source_completion_atlas,
)


def test_provenance_chain_preserves_all_relevant_closures_and_greens():
    result = provenance_gate()

    assert result[
        "pass"
    ] is True

    assert result[
        "a11a_derivative_composite_space_open"
    ] is True

    assert result[
        "a11a_full_noether_space_open"
    ] is True

    assert result[
        "a11c_direct_k2_ordinary_dirac_closed"
    ] is True

    assert result[
        "a12a_unmodified_axial_iw_maxwell_closed"
    ] is True

    assert result[
        "a12b_protected_massless_carrier_open"
    ] is True

    assert result[
        "a12c_ordinary_em_like_route_closed"
    ] is True

    assert result[
        "hook17_open"
    ] is True


def test_a12c_low_capacity_reference_is_frozen_exactly():
    result = (
        frozen_low_capacity_reference()
    )

    assert result[
        "reference_kernel_frozen"
    ] is True

    assert math.isclose(
        result[
            "field_energy_j"
        ],
        2.6568591420597114,
        rel_tol=1.0e-12,
        abs_tol=0.0,
    )

    assert math.isclose(
        result[
            "geometric_external_standoff_m"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert result[
        "strict_whole_payload_1g_pass"
    ] is True

    assert result[
        "invariant_tidal_response_nonzero"
    ] is True

    assert result[
        "complete_energy_established"
    ] is False


def test_low_capacity_reference_improves_field_term_by_over_200k():
    result = (
        frozen_low_capacity_reference()
    )

    assert (
        result[
            "field_energy_improvement_factor_vs_a10f2"
        ]
        >
        2.0e5
    )

    assert result[
        "field_term_below_100j"
    ] is True

    assert result[
        "field_efficiency_optimization_authorized"
    ] is False


def test_quadratic_fieldstrength_tensor_identities_are_exact():
    result = (
        quadratic_fieldstrength_metric_basis_theorem()
    )

    assert result[
        "basis_exhaustive_within_declared_scope"
    ] is True

    assert result[
        "odd_rank2_identity_pass"
    ] is True

    assert result[
        "dualdual_identity_pass"
    ] is True

    assert result[
        "parity_even_independent_dimension"
    ] == 2

    assert result[
        "parity_odd_independent_dimension"
    ] == 1


def test_pure_magnetostatic_quadratic_algebraic_g00_portal_is_unique():
    result = (
        quadratic_fieldstrength_metric_basis_theorem()
    )

    assert result[
        "magnetostatic_disformal_g00"
    ] == "0"

    assert result[
        "magnetostatic_pseudoscalar"
    ] == "0"

    assert result[
        "pure_magnetostatic_useful_static_g00_basis_dimension"
    ] == 1

    assert result[
        "pure_magnetostatic_unique_quadratic_algebraic_g00_portal"
    ] == "g_mn*F_ab*F^ab"

    assert result[
        "pure_magnetostatic_unique_g00_result_pass"
    ] is True


def test_field_sector_atlas_retains_electric_and_mixed_escapes():
    rows = (
        field_sector_portal_atlas()
    )

    assert len(
        rows
    ) == 9

    open_rows = [
        row
        for row in rows
        if not row[
            "structurally_closed"
        ]
    ]

    assert len(
        open_rows
    ) == 6

    assert any(
        row[
            "portal_id"
        ]
        ==
        "ELECTROSTATIC_DISFORMAL_FF"
        for row in open_rows
    )

    assert any(
        row[
            "portal_id"
        ]
        ==
        "MIXED_EB_PARITY_ODD"
        for row in open_rows
    )


def test_source_atlas_preserves_permanent_closed_routes():
    rows = (
        source_completion_atlas()
    )

    by_id = {
        row[
            "source_id"
        ]:
            row
        for row in rows
    }

    assert by_id[
        "ORDINARY_EM_LIKE_VECTOR"
    ][
        "current_status"
    ].startswith(
        "CLOSED_A12C"
    )

    assert by_id[
        "DIRECT_K2_WHEELER_ORDINARY_DIRAC"
    ][
        "current_status"
    ].startswith(
        "CLOSED_A11C"
    )

    assert by_id[
        "UNMODIFIED_IW_AXIAL_DIRAC"
    ][
        "current_status"
    ].startswith(
        "CLOSED_A12A"
    )


def test_pauli_source_is_first_exact_shape_completion_to_recheck():
    rows = (
        source_completion_atlas()
    )

    pauli = next(
        row
        for row in rows
        if row[
            "source_id"
        ]
        ==
        "ELECTRON_PAULI_MAGNETIZATION"
    )

    assert pauli[
        "current_status"
    ] == (
        "OPEN_REEVALUATE_AGAINST_A12C_LOW_CAPACITY_KERNEL"
    )

    assert pauli[
        "exact_conservation"
    ] == "YES_IDENTICAL"

    assert pauli[
        "source_shape_reference_compatibility"
    ] == "EXACT"

    assert pauli[
        "a11a_exact_shape_pass"
    ] is True

    assert pauli[
        "a11a_identically_conserved"
    ] is True

    assert pauli[
        "old_a11a_energy_closeout_transfers_automatically"
    ] is False


def test_unobserved_hidden_matter_is_not_promoted():
    rows = (
        source_completion_atlas()
    )

    hidden = next(
        row
        for row in rows
        if row[
            "source_id"
        ]
        ==
        "UNOBSERVED_HIDDEN_EXOTIC_MATTER"
    )

    assert hidden[
        "project_policy_authorized"
    ] is False

    assert hidden[
        "priority_base"
    ] == 0


def test_completion_atlas_does_not_promote_closed_metric_or_source_rows():
    rows = (
        completion_combination_atlas()
    )

    for row in rows:
        if row[
            "status"
        ] != "OPEN_PRE_BVP":
            assert row[
                "priority_score_not_probability"
            ] == 0


def test_top_ranked_completion_preserves_exact_a12c_kernel():
    rows = (
        open_completion_rerank()
    )

    assert len(
        rows
    ) > 0

    top = rows[
        0
    ]

    assert top[
        "source_id"
    ] == "ELECTRON_PAULI_MAGNETIZATION"

    assert top[
        "portal_id"
    ] == "MAGNETOSTATIC_CONFORMAL_F2"

    assert top[
        "exact_a12c_kernel_reuse"
    ] is True

    assert top[
        "priority_score_not_probability"
    ] > 0


def test_a12d0_is_documentation_ready_but_not_a_device_claim():
    result = (
        h17a12d0_summary()
    )

    assert result[
        "low_capacity_mechanism_reference_preserved"
    ] is True

    assert result[
        "a12b_exact_massless_carrier_preserved"
    ] is True

    assert result[
        "a12c_f2_metric_mechanism_preserved"
    ] is True

    assert result[
        "a12c_ordinary_em_like_route_remains_closed"
    ] is True

    assert result[
        "metric_basis_globally_exhausted"
    ] is False

    assert result[
        "source_space_globally_exhausted"
    ] is False

    assert result[
        "new_physics_discovery_claim"
    ] is False

    assert result[
        "project_level_mechanism_result"
    ] is True

    assert result[
        "documentation_update_authorized"
    ] is True

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False

    assert result[
        "practical_device_found"
    ] is False

    assert result[
        "field_efficiency_optimization_authorized"
    ] is False

    assert result[
        "new_bvp_authorized_immediately"
    ] is False

    assert result[
        "decision"
    ].startswith(
        "GREEN_SCOPED_A12D0_LOW_CAPACITY_F2_MECHANISM_FROZEN"
    )

    assert result[
        "next"
    ] == (
        "032H17A12D1_PAULI_MAGNETIZATION_SOURCE_ENERGY_"
        "UV_RADIATIVE_MIXING_AND_EMPIRICAL_GATE"
    )
