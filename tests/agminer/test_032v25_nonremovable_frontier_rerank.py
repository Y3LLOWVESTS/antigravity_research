"""Scientific regressions for 032V25 current-frontier rerank."""

from __future__ import annotations

from antigravity_research.agminer.nonremovable_frontier_rerank import (
    FAILED,
    VERIFIED,
    active_frontier_rows,
    family_row,
    frontier_rows,
    historical_reference_lessons,
    hypothetical_fully_verified_row,
    persist_v25_metadata,
    tier0_promotion_policy,
)
from antigravity_research.agminer.storage import (
    Storage,
)


def test_v25_top_target_is_intrinsic_source_active_state_metric_synthesis():
    row = (
        active_frontier_rows()[
            0
        ]
    )

    assert (
        row.family_id
        ==
        "INTRINSIC_SOURCE_ACTIVE_STATE_UNIVERSAL_METRIC_SYNTHESIS"
    )

    assert (
        row.research_rank
        ==
        "A1"
    )

    assert (
        row.action_oracle_authorized
        is False
    )


def test_active_state_descreening_is_second_current_target():
    row = (
        active_frontier_rows()[
            1
        ]
    )

    assert (
        row.family_id
        ==
        "ACTIVE_STATE_DEPENDENT_KINETIC_METRIC_DESCREENING"
    )

    assert (
        row.research_rank
        ==
        "A2"
    )

    assert (
        "OFFSTATE"
        in row.reason
    )


def test_shift_protected_goldstone_is_open_but_must_not_reuse_pure_j0():
    row = (
        active_frontier_rows()[
            2
        ]
    )

    assert (
        row.family_id
        ==
        "SHIFT_PROTECTED_GOLDSTONE_KINETIC_METRIC_WITH_R5_EVASION"
    )

    assert (
        row.research_rank
        ==
        "A3"
    )

    assert (
        row.protection_or_naturalness
        ==
        VERIFIED
    )

    assert (
        "PURE_J0_LIMIT_CLOSED_R5_R6"
        in row.inherited_blockers
    )


def test_dirac_intrinsic_source_is_preserved_but_not_promoted():
    row = family_row(
        "INTRINSIC_DIRAC_HYPERMOMENTUM_NONREMOVABLE_METRIC_BRIDGE"
    )

    assert (
        row.microscopic_source
        ==
        VERIFIED
    )

    assert (
        row.independent_productive_charge
        ==
        VERIFIED
    )

    assert (
        row.closed
        is False
    )

    assert (
        row.action_oracle_authorized
        is False
    )


def test_no_real_active_frontier_row_is_action_oracle_authorized():
    rows = active_frontier_rows()

    assert rows

    assert all(
        not row.action_oracle_authorized
        for row
        in rows
    )


def test_missing_microscopic_source_blocks_tier0_authorization():
    row = family_row(
        "ACTIVE_STATE_DEPENDENT_KINETIC_METRIC_DESCREENING"
    )

    assert (
        "microscopic_source"
        in row.tier0_missing()
    )

    assert (
        row.action_oracle_authorized
        is False
    )


def test_missing_universal_metric_blocks_dirac_source_promotion():
    row = family_row(
        "INTRINSIC_DIRAC_HYPERMOMENTUM_NONREMOVABLE_METRIC_BRIDGE"
    )

    assert (
        "universal_physical_metric"
        in row.tier0_missing()
    )

    assert (
        row.action_oracle_authorized
        is False
    )


def test_v24_marzo_removable_crosspropagator_is_hard_tier0_failure():
    row = family_row(
        "V24_MARZO_LINEAR_VECTOR_GRAVITON_PORTAL"
    )

    assert (
        row.nonremovable_crosspropagator
        ==
        FAILED
    )

    assert (
        row.closed
        is True
    )

    assert (
        row.action_oracle_authorized
        is False
    )


def test_hypothetical_fully_verified_row_can_authorize_oracle():
    row = (
        hypothetical_fully_verified_row()
    )

    assert (
        row.tier0_missing()
        ==
        ()
    )

    assert (
        row.action_oracle_authorized
        is True
    )


def test_v21_stationary_q_branch_remains_closed():
    row = family_row(
        "V21_STATIONARY_Q_TIME_GRADIENT_DISFORMAL"
    )

    assert (
        row.closed
        is True
    )

    assert (
        "STATIONARITY"
        in row.status
    )


def test_v22_unprotected_single_scale_localization_remains_closed():
    row = family_row(
        "V22_UNPROTECTED_SINGLE_SCALE_LOCALIZED_DISFORMAL"
    )

    assert (
        row.closed
        is True
    )

    assert (
        row.protection_or_naturalness
        ==
        FAILED
    )

    assert (
        "275_MJ"
        in row.energy_status
    )


def test_v23_ordinary_stress_derivative_route_remains_closed():
    row = family_row(
        "V23_ORDINARY_STRESS_DERIVATIVE_HYPERMOMENTUM"
    )

    assert (
        row.closed
        is True
    )

    assert (
        row.independent_productive_charge
        ==
        FAILED
    )

    assert (
        "NO_INDEPENDENT_CHARGE"
        in row.reason
    )


def test_v24_marzo_closure_is_narrow_not_full_nonlinear_closeout():
    row = family_row(
        "V24_MARZO_LINEAR_VECTOR_GRAVITON_PORTAL"
    )

    assert (
        row.closed
        is True
    )

    assert (
        "NONLINEAR_COMPLETION_ONLY"
        in row.next_gate
    )


def test_v24_bms_ir_closure_preserves_nonlinear_mag_remainder():
    row = family_row(
        "V24_BMS_UNIVERSAL_IR_TORSIONLIKE_VECTOR_METRIC_BRIDGE"
    )

    assert (
        row.closed
        is True
    )

    assert (
        "NONLINEAR_MAG_COMPLETION_ONLY"
        in row.next_gate
    )


def test_029_massive_spin2_is_not_reopened_by_global_rerank():
    row = family_row(
        "029_TESTED_MASSIVE_SPIN2_PORTAL"
    )

    assert (
        row.closed
        is True
    )

    assert (
        "DO_NOT_REOPEN"
        in row.reason
    )


def test_031f0_unprotected_ultralight_scalar_is_not_reopened():
    row = family_row(
        "031F0_UNPROTECTED_ULTRALIGHT_SCALAR"
    )

    assert (
        row.closed
        is True
    )

    assert (
        row.protection_or_naturalness
        ==
        FAILED
    )

    assert (
        "GENUINELY_NEW_PROTECTION"
        in row.next_gate
    )


def test_current_pure_j0_hidden_axial_implementation_remains_closed():
    row = family_row(
        "CURRENT_HIDDEN_AXIAL_PURE_J0_KINETIC_CONFORMAL"
    )

    assert (
        row.closed
        is True
    )

    assert (
        row.active_offstate_separation
        ==
        FAILED
    )

    assert (
        "59P4197_KJ"
        in row.energy_status
    )


def test_pure_gr_practical_route_closed_while_006d_anchor_is_preserved():
    row = family_row(
        "PURE_GR_PRACTICAL_LT10MJ"
    )

    lessons = (
        historical_reference_lessons()
    )

    assert (
        row.closed
        is True
    )

    assert (
        lessons[
            "006d"
        ][
            "coefficient_c"
        ]
        ==
        23.591586299249
    )

    assert (
        lessons[
            "006d"
        ][
            "true_standoff"
        ]
        is True
    )


def test_v17_historical_low_partial_is_preserved_without_device_claim():
    lessons = (
        historical_reference_lessons()
    )

    assert (
        abs(
            lessons[
                "v17"
            ][
                "partial_energy_j"
            ]
            -
            5.94197e4
        )
        <
        1.0
    )

    assert (
        lessons[
            "v17"
        ][
            "finite_payload_partial"
        ]
        is True
    )

    assert (
        lessons[
            "v17"
        ][
            "current_physical_implementation_closed"
        ]
        is True
    )


def test_global_policy_requires_nonremovable_bridge_and_forbids_blind_scan():
    policy = (
        tier0_promotion_policy()
    )

    assert (
        policy[
            "nonremovable_crosspropagator_required"
        ]
        is True
    )

    assert (
        policy[
            "source_ward_compatibility_required"
        ]
        is True
    )

    assert (
        policy[
            "one_universal_physical_metric_required"
        ]
        is True
    )

    assert (
        policy[
            "blind_parameter_scan_authorized"
        ]
        is False
    )

    assert (
        policy[
            "energy_optimization_before_tier0"
        ]
        is False
    )


def test_family_ids_are_unique():
    identifiers = [
        row.family_id
        for row
        in frontier_rows()
    ]

    assert (
        len(
            identifiers
        )
        ==
        len(
            set(
                identifiers
            )
        )
    )


def test_v25_metadata_is_idempotent_and_mutates_no_science_tables(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    try:
        tables = (
            "models",
            "rejections",
            "survivors",
            "region_rules",
            "action_oracles",
            "collective_scaling",
            "mechanism_metrics",
        )

        before = {
            table:
                int(
                    storage.connection.execute(
                        f"""
                        SELECT COUNT(*) AS count
                        FROM {table}
                        """
                    ).fetchone()[
                        "count"
                    ]
                )
            for table
            in tables
        }

        persist_v25_metadata(
            storage
        )

        persist_v25_metadata(
            storage
        )

        after = {
            table:
                int(
                    storage.connection.execute(
                        f"""
                        SELECT COUNT(*) AS count
                        FROM {table}
                        """
                    ).fetchone()[
                        "count"
                    ]
                )
            for table
            in tables
        }

        assert (
            after
            ==
            before
        )

        assert (
            storage.get_metadata(
                "032v25_ranking_version"
            )
            ==
            "NONREMOVABLE_CROSSPROPAGATOR_V1"
        )

        assert (
            storage.get_metadata(
                "032v25_action_oracle_authorized"
            )
            ==
            "0"
        )

        assert (
            storage.get_metadata(
                "032v25_blind_parameter_scan_authorized"
            )
            ==
            "0"
        )

    finally:
        storage.close()
