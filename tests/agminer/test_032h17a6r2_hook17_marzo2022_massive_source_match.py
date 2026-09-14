"""Regressions for 032H17A6R2 Marzo-2022 massive MAG source matching.

These tests protect both the new source-support theorem and its deliberately
narrow claim boundary.
"""

import math

from antigravity_research.agminer.hook17_marzo2022_massive_source_match import (
    HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    clean_v24_full_1minus_source_gate,
    clean_v24_hook_parity_gate,
    clean_v24_totally_symmetric_parity_gate,
    generic_dirac_escape_gate,
    h17a6r2_summary,
    marzo2022_clean_v24_source_match_gate,
    marzo2022_published_family_gate,
    r1_provenance_gate,
)


def test_r1_provenance_is_required_and_green():
    result = r1_provenance_gate()

    assert (
        result[
            "r1_provenance_pass"
        ]
        is True
    )

    assert (
        result[
            "exact_massless_single_compensator_closed"
        ]
        is True
    )

    assert (
        result[
            "massive_or_higgsed_open"
        ]
        is True
    )

    assert (
        result[
            "marzo_family_open_at_r1"
        ]
        is True
    )


def test_marzo2022_family_is_real_published_protected_massive_action():
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
            "published_ghost_tachyon_free_massive_regions_exist"
        ]
        is True
    )


def test_marzo2022_physical_massive_pole_is_unique_1minus():
    result = marzo2022_published_family_gate()

    assert (
        result[
            "published_massive_physical_pole_count"
        ]
        ==
        1
    )

    assert (
        result[
            "published_massive_physical_pole_sector"
        ]
        ==
        "1_MINUS"
    )


def test_clean_total_symmetric_source_is_nonzero_and_only_one_time_index():
    result = clean_v24_totally_symmetric_parity_gate()

    assert (
        result[
            "source_norm"
        ]
        >
        1.0
    )

    assert (
        result[
            "totally_symmetric"
        ]
        is True
    )

    assert (
        result[
            "nonzero_component_count"
        ]
        ==
        6
    )

    assert (
        result[
            "all_nonzero_components_have_exactly_one_time_index"
        ]
        is True
    )

    assert (
        result[
            "time_index_count_histogram"
        ][
            "1"
        ]
        ==
        6
    )


def test_clean_total_symmetric_s00i_is_zero():
    result = clean_v24_totally_symmetric_parity_gate()

    assert (
        result[
            "s_00i_zero"
        ]
        is True
    )

    assert math.isclose(
        result[
            "s_00i_norm2"
        ],
        0.0,
        abs_tol=
            1.0e-12,
    )


def test_clean_total_symmetric_spatial_tensor_is_zero():
    result = clean_v24_totally_symmetric_parity_gate()

    assert (
        result[
            "s_ijk_zero"
        ]
        is True
    )

    assert math.isclose(
        result[
            "s_ijk_norm2"
        ],
        0.0,
        abs_tol=
            1.0e-12,
    )


def test_clean_total_symmetric_1minus_zero_but_even_spin2_survives():
    result = clean_v24_totally_symmetric_parity_gate()

    assert (
        result[
            "totally_symmetric_1minus_support_zero"
        ]
        is True
    )

    assert (
        result[
            "s_0ij_spin2_support_nonzero"
        ]
        is True
    )

    assert (
        result[
            "s_0ij_spin2_norm2"
        ]
        >
        1.0
    )

    assert (
        result[
            "s_0ij_spin0_support_nonzero"
        ]
        is False
    )


def test_clean_hook_1minus_zero_while_1plus_2plus_survive():
    result = clean_v24_hook_parity_gate()

    assert (
        result[
            "hook_1minus_support_zero"
        ]
        is True
    )

    assert (
        result[
            "hook_2minus_support_zero"
        ]
        is True
    )

    assert (
        result[
            "hook_1plus_support_nonzero"
        ]
        is True
    )

    assert (
        result[
            "hook_2plus_support_nonzero"
        ]
        is True
    )


def test_full_clean_v24_1minus_support_is_zero():
    result = clean_v24_full_1minus_source_gate()

    assert (
        result[
            "totally_symmetric_1minus_support_zero"
        ]
        is True
    )

    assert (
        result[
            "hook_1minus_support_zero"
        ]
        is True
    )

    assert (
        result[
            "full_clean_v24_1minus_support_zero"
        ]
        is True
    )

    assert (
        result[
            "full_clean_v24_1minus_support_nonzero"
        ]
        is False
    )

    assert (
        result[
            "productive_even_parity_support_survives"
        ]
        is True
    )


def test_trace_vector_crosscheck_is_zero_for_clean_rest_pair():
    result = marzo2022_clean_v24_source_match_gate()

    assert (
        result[
            "clean_rest_pair_lorentz_trace_zero_crosscheck"
        ]
        is True
    )

    assert (
        result[
            "clean_rest_pair_direct_trace_carrier_overlap_zero_crosscheck"
        ]
        is True
    )

    assert (
        result[
            "direct_clean_v24_healthy_massive_pole_source_zero"
        ]
        is True
    )

    assert (
        result[
            "direct_clean_v24_marzo2022_massive_1minus_closed"
        ]
        is True
    )


def test_generic_dirac_family_is_not_closed_by_clean_rest_pair():
    result = generic_dirac_escape_gate()

    assert (
        result[
            "generic_algebraic_trace_carrier_nonzero"
        ]
        is True
    )

    assert (
        result[
            "generic_spinor_on_shell_localized_stationary"
        ]
        is False
    )

    assert (
        result[
            "generic_source_ward_identity_established"
        ]
        is False
    )

    assert (
        result[
            "generic_dirac_protected_spin1_closed"
        ]
        is False
    )

    assert (
        result[
            "source_state_engineering_remains_open"
        ]
        is True
    )


def test_a6r2_summary_is_scoped_red_and_moves_to_barker_zell():
    result = h17a6r2_summary()

    assert (
        result[
            "decision"
        ].startswith(
            "RED_SCOPED_A6R2_"
        )
    )

    assert (
        result[
            "direct_clean_v24_marzo2022_massive_1minus_closed"
        ]
        is True
    )

    assert (
        result[
            "static_offshell_marzo2022_response_closed"
        ]
        is False
    )

    assert (
        result[
            "generic_dirac_marzo2022_source_closed"
        ]
        is False
    )

    assert (
        result[
            "all_higgsed_or_massive_hook_closed"
        ]
        is False
    )

    assert (
        result[
            "productive_clean_v24_1plus_survives"
        ]
        is True
    )

    assert (
        result[
            "productive_clean_v24_2plus_survives"
        ]
        is True
    )

    assert (
        result[
            "hook17_closed"
        ]
        is False
    )

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
            "h17b_authorized"
        ]
        is False
    )

    assert result[
        "next"
    ] == (
        "032H17A7_BARKER_ZELL_EXTENDED_PROJECTIVE_"
        "DIRAC_SOURCE_MATCH_GATE"
    )
