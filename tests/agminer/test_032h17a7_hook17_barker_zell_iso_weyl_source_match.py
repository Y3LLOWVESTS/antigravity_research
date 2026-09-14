"""Regressions for 032H17A7 Barker-Zell iso-Weyl source matching."""

import math

from antigravity_research.agminer.hook17_barker_zell_iso_weyl_source_match import (
    HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    a6r2_provenance_gate,
    barker_zell_iso_weyl_family_gate,
    barker_zell_iw_clean_source_match_gate,
    clean_v24_pair_axial_torsion_gate,
    clean_v24_pair_weyl_trace_gate,
    generic_dirac_iw_escape_gate,
    h17a7_summary,
    iw_nondynamical_mixing_source_theorem,
    post_iso_weyl_rerank,
    preserved_productive_source_gate,
    prior_barker_zell_ep_gate,
)


def test_a6r2_provenance_is_green_and_productive_even_sectors_survive():
    result = a6r2_provenance_gate()

    assert (
        result[
            "a6r2_provenance_pass"
        ]
        is True
    )

    assert (
        result[
            "marzo2022_direct_clean_1minus_closed"
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


def test_prior_ep_pseudoscalar_is_not_accidentally_repeated():
    result = prior_barker_zell_ep_gate()

    assert (
        result[
            "ep_pseudoscalar_direct_bridge_already_closed"
        ]
        is True
    )

    assert (
        result[
            "all_ep_or_iw_models_closed_by_v24b"
        ]
        is False
    )

    assert (
        result[
            "iw_was_preserved_by_v24b"
        ]
        is True
    )

    assert (
        result[
            "repeat_ep_pseudoscalar_authorized"
        ]
        is False
    )


def test_barker_zell_iw_is_distinct_vector_family():
    result = barker_zell_iso_weyl_family_gate()

    assert (
        result[
            "distinct_from_extended_projective_branch"
        ]
        is True
    )

    assert (
        result[
            "propagating_vector"
        ]
        ==
        "Q_MU"
    )

    assert (
        result[
            "t_hat_is_nondynamical"
        ]
        is True
    )

    assert (
        result[
            "reduced_vector_theory"
        ]
        ==
        "EINSTEIN_PROCA_OR_MAXWELL"
    )


def test_clean_pair_nonmetricity_is_nonzero_but_weyl_trace_is_zero():
    result = clean_v24_pair_weyl_trace_gate()

    assert (
        result[
            "pair_nonmetricity_tensor_nonzero"
        ]
        is True
    )

    assert (
        result[
            "pair_nonmetricity_adds"
        ]
        is True
    )

    assert (
        result[
            "pair_weyl_trace_zero"
        ]
        is True
    )

    assert (
        result[
            "identified_iw_q_vector_channel_zero"
        ]
        is True
    )

    assert math.isclose(
        result[
            "pair_weyl_trace_norm"
        ],
        0.0,
        abs_tol=
            1.0e-12,
    )


def test_clean_pair_full_torsion_cancellation_kills_axial_channel():
    result = clean_v24_pair_axial_torsion_gate()

    assert (
        result[
            "particle_antiparticle_torsion_opposite_sign"
        ]
        is True
    )

    assert (
        result[
            "full_pair_torsion_response_zero"
        ]
        is True
    )

    assert (
        result[
            "identified_iw_t_hat_channel_zero"
        ]
        is True
    )

    assert (
        result[
            "axial_torsion_channel_zero_by_linearity"
        ]
        is True
    )


def test_nondynamical_iw_mixing_cannot_create_source_from_zero_zero():
    result = iw_nondynamical_mixing_source_theorem()

    assert (
        result[
            "identified_j_q_zero"
        ]
        is True
    )

    assert (
        result[
            "identified_j_t_hat_zero"
        ]
        is True
    )

    assert (
        result[
            "mixing_can_create_nonzero_source_from_zero_zero"
        ]
        is False
    )

    assert (
        result[
            "effective_q_source_zero_for_all_finite_b3_over_b2"
        ]
        is True
    )

    assert (
        result[
            "singular_b2_zero_used_as_gain"
        ]
        is False
    )


def test_direct_clean_iw_route_closes_but_full_iw_family_does_not():
    result = barker_zell_iw_clean_source_match_gate()

    assert (
        result[
            "direct_clean_v24_barker_zell_iw_vector_route_closed"
        ]
        is True
    )

    assert (
        result[
            "full_barker_zell_iw_family_closed"
        ]
        is False
    )

    assert (
        result[
            "same_action_v24_dirac_iw_completion_closed"
        ]
        is False
    )

    assert (
        result[
            "static_offshell_iw_response_closed"
        ]
        is False
    )


def test_generic_dirac_states_remain_open_after_clean_pair_theorem():
    result = generic_dirac_iw_escape_gate()

    assert (
        result[
            "clean_pair_torsion_cancellation"
        ]
        is True
    )

    assert (
        result[
            "clean_pair_cancellation_is_generic_dirac_identity"
        ]
        is False
    )

    assert (
        result[
            "generic_dirac_axial_source_proved_zero"
        ]
        is False
    )

    assert (
        result[
            "generic_dirac_iw_vector_route_closed"
        ]
        is False
    )

    assert (
        result[
            "generic_dirac_source_state_engineering_open"
        ]
        is True
    )


def test_clean_v24_productive_1plus_and_2plus_are_preserved():
    result = preserved_productive_source_gate()

    assert (
        result[
            "clean_hook_1plus_support_nonzero"
        ]
        is True
    )

    assert (
        result[
            "clean_hook_2plus_support_nonzero"
        ]
        is True
    )

    assert math.isclose(
        result[
            "clean_hook_1plus_norm2"
        ],
        32.0,
    )

    assert math.isclose(
        result[
            "clean_hook_2plus_norm2"
        ],
        14.222222222222221,
    )


def test_h17a7_summary_is_scoped_red_but_hook17_remains_open():
    result = h17a7_summary()

    assert (
        result[
            "decision"
        ].startswith(
            "RED_SCOPED_A7_"
        )
    )

    assert (
        result[
            "direct_clean_v24_barker_zell_iw_vector_route_closed"
        ]
        is True
    )

    assert (
        result[
            "full_barker_zell_iw_family_closed"
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
            "protected_2plus_closed"
        ]
        is False
    )


def test_h17a7_preserves_capacity_reference_and_blocks_energy_work():
    result = h17a7_summary()

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
            "capacity_recalculation_authorized"
        ]
        is False
    )

    assert (
        result[
            "energy_optimization_authorized"
        ]
        is False
    )

    assert (
        result[
            "sub100j_capacity_tuning_authorized"
        ]
        is False
    )

    assert (
        result[
            "h17b_authorized"
        ]
        is False
    )


def test_h17a7_does_not_promote_a_physical_model_or_device():
    result = h17a7_summary()

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
            "practical_device_found"
        ]
        is False
    )

    assert (
        result[
            "v26d_fallback_status"
        ]
        ==
        "PRESERVED"
    )


def test_post_iw_rerank_moves_to_native_protected_2plus_first():
    result = h17a7_summary()

    rows = post_iso_weyl_rerank()

    assert rows[
        0
    ][
        "family"
    ] == "NATIVE_PROTECTED_MAG_2PLUS"

    assert rows[
        0
    ][
        "status"
    ] == "OPEN_HIGHEST_PRIORITY"

    assert result[
        "next"
    ] == "032H17A8_NATIVE_PROTECTED_2PLUS_ACTION_SOURCE_WARD_ATLAS"
