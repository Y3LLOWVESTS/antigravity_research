"""Scientific regressions for 032V24B protected Dirac metric bridge gates."""

from __future__ import annotations

import json

from antigravity_research.agminer.protected_dirac_metric_bridge import (
    bms_dimension5_metric_mixing_scout,
    einstein_stress_bridge_bound,
    extended_projective_bridge_gate,
    generic_dirac_algebraic_carrier_witness,
    persist_v24b_region_rules,
    protected_mode_rerank,
    rest_pair_fronsdal_ward_scout,
    rest_pair_so3_screen,
)
from antigravity_research.agminer.storage import Storage


def test_rest_pair_so3_screen_has_zero_spin1_but_is_not_hard_exclusion():
    result = rest_pair_so3_screen()

    assert result[
        "rest_frame_spin1_screen_zero"
    ] is True

    assert result[
        "combined_spin1_carrier_norm"
    ] < 1.0e-12

    assert result[
        "rest_frame_so3_screen_closes_protected_spin1_spin3"
    ] is False


def test_rest_pair_so3_screen_has_zero_spin3_but_not_exact_helicity_projection():
    result = rest_pair_so3_screen()

    assert result[
        "rest_frame_spin3_screen_zero"
    ] is True

    assert result[
        "spin3_spatial_stf_norm"
    ] < 1.0e-12

    assert result[
        "rest_frame_so3_screen_is_exact_pole_projection"
    ] is False


def test_rest_pair_so3_screen_has_nonzero_spin2_carrier():
    result = rest_pair_so3_screen()

    assert result[
        "rest_frame_spin2_carrier_nonzero"
    ] is True

    assert result[
        "spin2_zero_ij_stf_norm"
    ] > 1.0

    assert result[
        "full_dirac_source_family_closed"
    ] is False


def test_generic_algebraic_dirac_source_contains_spin1_and_spin3_carriers():
    result = generic_dirac_algebraic_carrier_witness()

    assert result[
        "algebraic_spin1_carrier_nonzero"
    ] is True

    assert result[
        "algebraic_spin3_carrier_nonzero"
    ] is True

    assert result[
        "spinor_is_claimed_on_shell_stationary_source"
    ] is False

    assert result[
        "protecting_gauge_ward_identity_established"
    ] is False


def test_rest_pair_fronsdal_direct_source_fails_some_spatial_directions():
    result = rest_pair_fronsdal_ward_scout()

    assert result[
        "direction_results"
    ][
        "x"
    ][
        "standard_fronsdal_source_ward_pass"
    ] is True

    assert result[
        "direction_results"
    ][
        "y"
    ][
        "standard_fronsdal_source_ward_pass"
    ] is False

    assert result[
        "direction_results"
    ][
        "z"
    ][
        "standard_fronsdal_source_ward_pass"
    ] is False


def test_rest_pair_fronsdal_failure_closes_only_direct_uncompensated_realization():
    result = rest_pair_fronsdal_ward_scout()

    assert result[
        "all_tested_spatial_directions_pass"
    ] is False

    assert result[
        "direct_factorized_localized_rest_pair_without_compensator_closed"
    ] is True

    assert result[
        "compensating_current_or_more_general_source_closed"
    ] is False

    assert result[
        "all_massless_spin3_dirac_sources_closed"
    ] is False


def test_bms_first_metric_mixing_is_dimension5_three_derivative():
    result = bms_dimension5_metric_mixing_scout()

    assert result[
        "metric_distortion_mixing_first_dimension"
    ] == 5

    assert result[
        "metric_distortion_mixing_derivative_order"
    ] == 3

    assert result[
        "dominant_distortion_kinetic_dimension"
    ] == 4

    assert result[
        "mixing_subleading_in_declared_eft"
    ] is True


def test_natural_planck_suppressed_bms_mixing_is_tiny_at_10cm():
    result = bms_dimension5_metric_mixing_scout()

    assert result[
        "natural_dimension5_mixing_ratio"
    ] < 1.0e-30

    assert result[
        "matched_bms_wilson_coefficient_established"
    ] is False

    assert result[
        "naturalness_no_go_established"
    ] is False


def test_millipercent_bms_mixing_requires_enormous_dimensionless_wilson():
    result = bms_dimension5_metric_mixing_scout()

    row = next(
        item
        for item
        in result[
            "target_rows"
        ]
        if item[
            "target_mixing"
        ] == 1.0e-3
    )

    assert row[
        "required_dimensionless_wilson"
    ] > 1.0e29

    assert row[
        "effective_suppression_length_m"
    ] > 1.0e-5


def test_einstein_stress_only_bridge_is_far_below_1g_at_10mj_10cm():
    result = einstein_stress_bridge_bound()

    assert result[
        "acceleration_upper_bound_m_s2"
    ] < 1.0e-17

    assert result[
        "target_acceleration_m_s2"
    ] > result[
        "acceleration_upper_bound_m_s2"
    ]

    assert result[
        "uses_exact_10mj_fail_boundary_as_optimistic_supremum"
    ] is True


def test_einstein_stress_only_gap_exceeds_1e18_without_closing_new_portals():
    result = einstein_stress_bridge_bound()

    assert result[
        "target_to_upper_bound_ratio"
    ] > 1.0e18

    assert result[
        "energy_required_at_same_bound_j"
    ] > 1.0e25

    assert result[
        "nonminimal_metric_portal_closed_by_this_bound"
    ] is False


def test_extended_projective_pseudoscalar_is_protected_but_not_direct_metric_portal():
    result = extended_projective_bridge_gate()

    assert result[
        "dirac_motivated_protecting_symmetry"
    ] is True

    assert result[
        "published_reduced_metric_form"
    ] == "EINSTEIN_HILBERT_PLUS_CANONICAL_PSEUDOSCALAR"

    assert result[
        "direct_universal_neutral_matter_metric_portal_identified"
    ] is False

    assert result[
        "universal_bridge_in_declared_reduced_action"
    ] == "EINSTEIN_STRESS_ENERGY_ONLY"


def test_extended_projective_declared_direct_bridge_closes_but_extensions_remain_open():
    result = extended_projective_bridge_gate()

    assert result[
        "strict_sub10mj_reference_gap_reaches_1g"
    ] is False

    assert result[
        "declared_ep_pseudoscalar_direct_antigravity_bridge_closed"
    ] is True

    assert result[
        "all_extended_projective_or_iso_weyl_models_closed"
    ] is False

    assert result[
        "new_added_universal_metric_portal_closed"
    ] is False


def test_rerank_closes_fronsdal_rest_pair_and_ep_only():
    rows = {
        row[
            "branch"
        ]:
            row
        for row
        in protected_mode_rerank()
    }

    assert rows[
        "STANDARD_FRONSDAL_F4_SPIN3_DIRECT_REST_PAIR"
    ][
        "status"
    ] == "CLOSED_WITHOUT_COMPENSATING_CURRENT"

    assert rows[
        "BARKER_ZELL_EXTENDED_PROJECTIVE_PSEUDOSCALAR"
    ][
        "status"
    ] == "CLOSED_AS_DECLARED_DIRECT_SUB10MJ_UNIVERSAL_BRIDGE"

    assert rows[
        "BMS_TOTALLY_SYMMETRIC_PROTECTED_SPIN1_REST_PAIR"
    ][
        "status"
    ] == "OPEN_EXACT_SPIN1_SOURCE_CONSTRAINT_REQUIRED"


def test_rerank_preserves_spin1_compensated_spin3_and_broader_hook_frontiers():
    rows = {
        row[
            "branch"
        ]:
            row
        for row
        in protected_mode_rerank()
    }

    assert rows[
        "BMS_PROTECTED_TOTALLY_SYMMETRIC_SPIN1_ONSHELL_DIRAC"
    ][
        "status"
    ] == "HIGHEST_PRIORITY_OPEN_PROTECTED_TS_ROUTE"

    assert rows[
        "BMS_OR_CATALOGUE_SPIN3_WITH_COMPENSATED_ONSHELL_DIRAC_SOURCE"
    ][
        "status"
    ] == "OPEN_ONLY_WITH_WARD_COMPATIBLE_SOURCE_AND_METRIC_BRIDGE"

    assert rows[
        "BROADER_HOOK_OR_MIXED_SYMMETRY_MAG_WITH_PROTECTED_LOWER_SPIN_METRIC_ACTIVE_MODE"
    ][
        "status"
    ] == "OPEN_NEW_ACTION_REQUIRED"


def test_v24b_region_rules_are_idempotent(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    try:
        first = persist_v24b_region_rules(
            storage,
            energy_policy_id=
                "ENERGY_TEST",
        )

        second = persist_v24b_region_rules(
            storage,
            energy_policy_id=
                "ENERGY_TEST",
        )

        assert first == 2
        assert second == 0

        row = storage.connection.execute(
            "SELECT rule_json FROM region_rules WHERE rule_type=?",
            (
                "STRESS_ONLY_UNIVERSAL_BRIDGE_FAILS_SUB10MJ_10CM_STANDOFF",
            ),
        ).fetchone()

        rule = json.loads(
            row[
                "rule_json"
            ]
        )

        assert rule[
            "policy_specific"
        ] is True

        assert rule[
            "energy_policy_id"
        ] == "ENERGY_TEST"

    finally:
        storage.close()


def test_v24b_rules_create_no_candidates_rejections_or_promotions(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    try:
        persist_v24b_region_rules(
            storage,
            energy_policy_id=
                "ENERGY_TEST",
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
