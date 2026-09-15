"""Regressions for 032H17A12A engineered Dirac -> iso-Weyl vector gate."""

from __future__ import annotations

from antigravity_research.agminer.hook17_iw_engineered_axial_source import (
    engineered_iw_reopening_theorem,
    engineered_iw_source_atlas,
    h17a12a_summary,
    iw_maxwell_source_ward_gate,
    iw_proca_protection_gate,
)


def test_historical_clean_pair_remains_zero_axial_source():
    rows = engineered_iw_source_atlas()

    clean = next(
        row
        for row in rows
        if row[
            "historical_clean_pair"
        ]
    )

    assert clean[
        "pair_id"
    ] == "U1_V2"

    assert clean[
        "j_t_hat_nonzero"
    ] is False

    assert clean[
        "j_t_hat_norm"
    ] == 0.0


def test_a10_engineered_pairs_reopen_axial_torsion_channel():
    result = (
        engineered_iw_reopening_theorem()
    )

    assert result[
        "a7_generic_dirac_source_state_engineering_was_open"
    ] is True

    assert result[
        "engineered_nonzero_axial_pair_ids"
    ] == [
        "U1_V1",
        "U2_V2",
    ]

    assert result[
        "engineered_nonzero_axial_pair_count"
    ] == 2

    assert result[
        "engineered_dirac_reopens_a7_t_hat_channel"
    ] is True


def test_engineered_axial_sources_are_equal_and_opposite():
    result = (
        engineered_iw_reopening_theorem()
    )

    assert result[
        "u1_v1_u2_v2_axial_sources_equal_and_opposite"
    ] is True


def test_direct_weyl_q_trace_remains_zero_for_all_four_rest_pairs():
    result = (
        engineered_iw_reopening_theorem()
    )

    assert result[
        "all_tested_weyl_q_direct_traces_zero"
    ] is True


def test_finite_iw_mixing_converts_axial_source_into_effective_q_source():
    result = (
        engineered_iw_reopening_theorem()
    )

    assert result[
        "finite_nonzero_mixing_reopens_effective_q_source"
    ] is True

    assert result[
        "same_action_iw_matter_completion_established"
    ] is False


def test_unmodified_massive_dirac_source_fails_iw_maxwell_ward():
    result = (
        iw_maxwell_source_ward_gate()
    )

    assert result[
        "effective_q_source_reopened"
    ] is True

    assert result[
        "mass_term_breaks_axial_current_conservation"
    ] is True

    assert result[
        "unmodified_massive_dirac_axial_source_is_exact_conserved_current"
    ] is False

    assert result[
        "direct_maxwell_source_ward_pass"
    ] is False

    assert result[
        "direct_engineered_dirac_iw_maxwell_branch_closed"
    ] is True


def test_state_specific_static_silence_is_not_operator_identity():
    result = (
        iw_maxwell_source_ward_gate()
    )

    assert result[
        "state_specific_static_divergence_zero_is_operator_ward_identity"
    ] is False

    assert result[
        "full_noether_completed_iw_maxwell_source_closed"
    ] is False


def test_iw_alone_does_not_protect_meter_range_proca_mass():
    result = (
        iw_proca_protection_gate()
    )

    assert result[
        "iw_symmetry_forbids_vector_mass_terms"
    ] is False

    assert result[
        "electron_mass_over_meter_vector_mass"
    ] > 1.0e12

    assert result[
        "meter_scale_proca_mass_technically_protected_by_iw_alone"
    ] is False

    assert result[
        "a10f2_loop_coefficient_transferred_to_iw"
    ] is False


def test_a12a_does_not_authorize_metric_payload_or_energy_work():
    result = (
        h17a12a_summary()
    )

    assert result[
        "engineered_iw_source_channel_reopened"
    ] is True

    assert result[
        "unmodified_ordinary_dirac_iw_route_promoted"
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


def test_a12a_promotes_only_genuinely_new_same_action_source_protection():
    result = (
        h17a12a_summary()
    )

    assert result[
        "decision"
    ].startswith(
        "YELLOW_A12A_ENGINEERED_DIRAC_REOPENS"
    )

    assert result[
        "full_barker_zell_iw_family_closed"
    ] is False

    assert result[
        "full_same_action_iw_noether_completion_closed"
    ] is False

    assert result[
        "rerank"
    ][
        0
    ][
        "family"
    ] == (
        "FULL_SAME_ACTION_IW_NOETHER_OR_EXACT_CONSERVED_CURRENT"
    )

    assert result[
        "next"
    ] == (
        "032H17A12B_FULL_SAME_ACTION_IW_EXACT_SOURCE_PROTECTION_GATE"
    )
