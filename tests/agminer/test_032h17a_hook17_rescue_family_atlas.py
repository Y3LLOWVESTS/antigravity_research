"""Regression tests for 032H17A HOOK17 rescue-family theorem/action atlas.

These tests protect claim boundaries as strongly as the algebra.  In
particular, a kinematic Stueckelberg Ward repair must never be promoted into a
same-action physical HOOK17 model without the exact healthy-mode projector,
metric bridge, canonicalization, and complete action.
"""

import math

from antigravity_research.agminer.hook17_rescue_family_atlas import (
    HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    STRICT_COMPLETE_OPERATING_TARGET_J,
    compensated_hook17_ward_rescue_gate,
    curtright_representation_gate,
    h17a_summary,
    hook17_family_atlas,
    massive_curtright_pole_prefilter,
    mikura_percacci_hook_projector_prefilter,
    v24_longitudinal_support_gate,
    v24_clean_rest_o3_hook_irrep_gate,
)


def test_v24_hook_maps_exactly_to_curtright_representation():
    result = curtright_representation_gate()
    assert result["first_pair_antisymmetric"] is True
    assert result["curtright_cyclic_identity"] is True
    assert result["representation_roundtrip_pass"] is True
    assert result["representation_match_is_action_match"] is False


def test_clean_rest_pair_has_exactly_one_longitudinal_index_support():
    result = v24_longitudinal_support_gate()
    assert result["one_longitudinal_only"] is True
    assert result["all_one_longitudinal_placements_present"] is True
    assert math.isclose(result["one_longitudinal_fraction"], 1.0, abs_tol=1e-12)
    assert result["support_statement_is_exact_projector_overlap"] is False


def test_clean_rest_o3_decomposition_has_spin2_and_spin1_but_no_spin0():
    result = v24_clean_rest_o3_hook_irrep_gate()
    assert result["A_symmetric"] is True
    assert result["hook_young_relation_pass"] is True
    assert result["spin2_plus_support_nonzero"] is True
    assert result["spin1_plus_support_nonzero"] is True
    assert result["spin0_plus_support_nonzero"] is False
    assert math.isclose(result["spin2_plus_support_norm2"], 128.0 / 9.0, rel_tol=1e-12)
    assert math.isclose(result["spin1_plus_support_norm2"], 32.0, rel_tol=1e-12)


def test_curtright_rest_frame_five_dof_pole_support_is_zero_but_offshell_open():
    result = massive_curtright_pole_prefilter()
    assert result["massive_curtright_dof_4d"] == 5
    assert result["clean_rest_pair_rest_frame_pole_support_zero"] is True
    assert result["massive_curtright_has_massive_spin2_duality_provenance"] is True
    assert result["029_massive_spin2_route_automatically_recloses_hook17"] is False
    assert result["static_offshell_projector_evaluated"] is False


def test_hook_mag_o3_prefilter_keeps_only_spin2plus_and_spin1plus():
    result = mikura_percacci_hook_projector_prefilter()
    assert result["o3_irrep_support_survivors"] == [
        "HOOK_2_PLUS",
        "HOOK_1_PLUS",
    ]
    assert result["o3_irrep_exact_zeros"] == [
        "HOOK_2_MINUS",
        "HOOK_1_MINUS",
        "HOOK_0_PLUS",
    ]
    assert result["exact_canonical_residue_required_for_survivors"] is True
    assert result["same_action_complete"] is False


def test_compensated_invariant_hook_repairs_v26c_ward_obstruction_kinematically():
    result = compensated_hook17_ward_rescue_gate()
    assert result["raw_v26c_source_ward_pass"] is False
    assert result["raw_v26c_metric_ward_pass"] is False
    assert result["published_compensator_count"] == 3
    assert result["compensated_source_ward_pass_by_invariance"] is True
    assert result["compensated_quadratic_metric_ward_pass_by_invariance"] is True
    assert result["kinematic_ward_obstruction_repaired"] is True


def test_compensated_unitary_gauge_retains_v26b1_active_offstate_algebra():
    result = compensated_hook17_ward_rescue_gate()
    assert result["unitary_gauge_recovers_v26b1_hook"] is True
    assert result["v26b1_quadratic_metric_nonzero"] is True
    assert result["v26b1_active_degree_two_identity_pass"] is True
    assert result["v26b1_offstate_first_variation_zero"] is True


def test_kinematic_ward_rescue_is_not_misreported_as_same_action_completion():
    result = compensated_hook17_ward_rescue_gate()
    assert result["complete_same_action_established"] is False
    assert result["healthy_mode_projector_established"] is False
    assert result["field_redefinition_survival_established"] is False
    assert result["complete_energy_established"] is False


def test_family_atlas_has_required_primary_families_and_closed_v26c_control():
    atlas = hook17_family_atlas()
    ids = {row["FAMILY_ID"] for row in atlas}
    assert {
        "H17-F1",
        "H17-F2",
        "H17-F3",
        "H17-F4",
        "H17-F5",
        "H17-F6",
        "H17-CONTROL-V26C",
    }.issubset(ids)

    control = next(row for row in atlas if row["FAMILY_ID"] == "H17-CONTROL-V26C")
    assert control["STATUS"] == "CLOSED"
    assert control["FAILURE_CODE"] == "SOURCE_WARD_FAIL_AND_METRIC_WARD_FAIL"


def test_atlas_does_not_claim_any_same_action_complete_survivor():
    atlas = hook17_family_atlas()
    assert all(row["SAME_ACTION_COMPLETE"] is False for row in atlas)


def test_h17f2_is_promoted_only_to_exact_projector_action_matching_not_h17b():
    atlas = hook17_family_atlas()
    f2 = next(row for row in atlas if row["FAMILY_ID"] == "H17-F2")
    assert f2["STATUS"] == "HIGHEST_PRIORITY_EXACT_PROJECTOR_ACTION_MATCHING_FAMILY"
    assert f2["SAME_ACTION_COMPLETE"] is False
    assert "HOOK_2_PLUS" in f2["SOURCE_PROJECTOR_STATUS"]
    assert "HOOK_2_MINUS" in f2["SOURCE_PROJECTOR_STATUS"]


def test_h17f1_records_duality_and_rest_pole_warning_without_false_closure():
    atlas = hook17_family_atlas()
    f1 = next(row for row in atlas if row["FAMILY_ID"] == "H17-F1")
    assert "DUAL_MASSIVE_SPIN2" in f1["FIELD_REDEFINITION_STATUS"]
    assert "REST_FRAME_PHYSICAL_POLE_ZERO" in f1["SOURCE_PROJECTOR_STATUS"]
    assert f1["STATUS"].startswith("KINEMATIC_WARD_RESCUE_SURVIVES")
    assert f1["STATUS"] != "CLOSED"


def test_energy_policy_and_hook17_capacity_claim_boundary_are_preserved():
    summary = h17a_summary()
    assert math.isclose(
        summary["hook17_reference_capacity_rp1e12_j"],
        HOOK17_REFERENCE_CAPACITY_RP1E12_J,
        rel_tol=0.0,
        abs_tol=1e-12,
    )
    assert summary["hook17_complete_energy_j"] is None
    assert summary["strict_complete_operating_target_j"] == STRICT_COMPLETE_OPERATING_TARGET_J
    assert summary["exactly_target_passes"] is False


def test_h17a_fail_closed_promotion_logic():
    summary = h17a_summary()
    assert summary["same_action_complete_survivor_count"] == 0
    assert summary["h17a_full_survivor"] is False
    assert summary["h17b_authorized"] is False
    assert summary["energy_optimization_authorized"] is False
    assert summary["mass_candidate_campaign_authorized"] is False
    assert summary["action_oracle_authorized"] is False


def test_h17a_selects_f2_projector_and_f1_offshell_duality_audit_next():
    summary = h17a_summary()
    assert summary["most_informative_next_family"] == "H17-F2"
    assert summary["most_informative_next_modes"] == [
        "HOOK_2_PLUS",
        "HOOK_1_PLUS",
    ]
    assert summary["permanent_clean_rest_pole_zeros"] == [
        "HOOK_2_MINUS",
        "HOOK_1_MINUS",
        "HOOK_0_PLUS",
    ]
    assert summary["curtright_kinematic_ward_rescue_is_real"] is True
    assert summary["curtright_complete_same_action_model_exists"] is False
    assert summary["curtright_static_offshell_response_closed"] is False
    assert summary["next"].startswith("032H17A2_")


def test_no_false_physical_model_claim():
    summary = h17a_summary()
    assert summary["physical_antigravity_model_found"] is False
    assert summary["certified_sub10mj_model_found"] is False
    assert summary["practical_device_found"] is False
    assert summary["v26d_fallback_status"] == "PRESERVED_PAUSED_V26E_NOT_ACTIVATED_YET"
