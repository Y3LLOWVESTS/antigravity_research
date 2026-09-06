"""032V12 local metric-active source operator atlas."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.operator_atlas import (
    OperatorRecord,
    canonical_derivative_metric_coefficient,
    kinetic_conformal_outward_for_localized_gradient,
    operator_prefield_open,
    static_kinetic_conformal_acceleration,
    static_pure_disformal_g00_shift,
)
from antigravity_research.agminer.policy import current_energy_policy


ROOT = Path(__file__).resolve().parents[1]

V4 = ROOT / "results" / "data" / "032v4_ghost_condensate_effective_charge_normalization_summary.json"
V10 = ROOT / "results" / "data" / "032v10_kernel_aware_collective_promotion_summary.json"
V11 = ROOT / "results" / "data" / "032v11_asymmetron_bubble_sign_stability_summary.json"

OUT = ROOT / "results" / "data" / "032v12_local_metric_active_operator_atlas_summary.json"
CSV_OUT = ROOT / "results" / "data" / "032v12_local_metric_active_operator_atlas.csv"

STRICT_TARGET_J = 1.0e7

policy = current_energy_policy()
assert float(policy["limit_j"]) == STRICT_TARGET_J
assert str(policy["comparison"]) == "LT"

for path in (V4, V10, V11):
    if not path.exists():
        raise FileNotFoundError(str(path))

v4 = json.loads(V4.read_text(encoding="utf-8"))
v10 = json.loads(V10.read_text(encoding="utf-8"))
v11 = json.loads(V11.read_text(encoding="utf-8"))

assert v4["decision"] == "RED_MINIMAL_GHOST_KAPPA_LEVER_NORMALIZATION_REDUNDANT"
assert v10["hopf"]["collective_promotion_allowed"] is False
assert v11["project_scope"]["published_minimal_asymmetron_bubble_external_repulsion_closed"] is True

# ============================================================
# 1. OPERATOR ATLAS
# ============================================================

rows = [
    {
        "priority": 1,
        "operator_id": "SHIFT_SYMMETRIC_X_DEPENDENT_CONFORMAL_METRIC",
        "schematic_metric": "gphys=C(X)g+D(X)dphi_dphi",
        "local_covariant": True,
        "one_physical_metric": True,
        "static_g00_response": True,
        "stand_off_structurally_possible": True,
        "symmetry_protection_available": True,
        "separate_charge_mediator_required": False,
        "canonical_normalization_guard_required": True,
        "static_outward_sign_structurally_possible": True,
        "empirical_status": "EXACT_DERIVATIVE_MATTER_OPERATOR_MATCH_REQUIRED",
        "source_realization_status": "OPEN",
        "project_status": "OPEN_TOP_PREFIELD_CANDIDATE",
        "reason": "STATIC_SPATIAL_X_GRADIENT_DIRECTLY_CHANGES_PHYSICAL_G00_WHILE_SHIFT_SYMMETRY_CAN_PROTECT_SCALAR",
    },
    {
        "priority": 2,
        "operator_id": "SHIFT_SYMMETRIC_X_DEPENDENT_DISFORMAL_TIME_GRADIENT",
        "schematic_metric": "gphys=C(X)g+D(X)dphi_dphi_phi_equals_qt_plus_psi",
        "local_covariant": True,
        "one_physical_metric": True,
        "static_g00_response": True,
        "stand_off_structurally_possible": True,
        "symmetry_protection_available": True,
        "separate_charge_mediator_required": False,
        "canonical_normalization_guard_required": True,
        "static_outward_sign_structurally_possible": "UNRESOLVED",
        "empirical_status": "EXACT_OPERATOR_MATCH_REQUIRED",
        "source_realization_status": "TIME_GRADIENT_RESERVOIR_REQUIRED",
        "project_status": "OPEN_SECONDARY_DYNAMIC_BACKGROUND",
        "reason": "KNOWN_SHIFT_SYMMETRIC_DISFORMAL_STAR_BRANCHES_ALLOW_TIME_LINEAR_SCALAR_BUT_CONTROL_ENERGY_IS_ADDITIONAL",
    },
    {
        "priority": 3,
        "operator_id": "FIELD_VALUE_CONFORMAL_SCALAR_METRIC",
        "schematic_metric": "gphys=A(phi)^2g",
        "local_covariant": True,
        "one_physical_metric": True,
        "static_g00_response": True,
        "stand_off_structurally_possible": True,
        "symmetry_protection_available": False,
        "separate_charge_mediator_required": False,
        "canonical_normalization_guard_required": True,
        "static_outward_sign_structurally_possible": True,
        "empirical_status": "031F0_NATURALNESS_FATAL_FOR_TESTED_ULTRALIGHT_REALIZATION",
        "source_realization_status": "031_CLASSICAL_REALIZATION_EXISTED",
        "project_status": "DEMOTED_UNPROTECTED_LIGHT_SCALAR",
        "reason": "CLASSICALLY_POWERFUL_BUT_ORDINARY_MATTER_METRIC_COUPLING_DESTROYED_ULTRALIGHT_NATURALNESS_IN_031F0",
    },
    {
        "priority": 4,
        "operator_id": "PURE_STATIC_DISFORMAL_DPHI_DPHI",
        "schematic_metric": "gphys=g+D(X)dphi_dphi_static_phi",
        "local_covariant": True,
        "one_physical_metric": True,
        "static_g00_response": False,
        "stand_off_structurally_possible": False,
        "symmetry_protection_available": True,
        "separate_charge_mediator_required": False,
        "canonical_normalization_guard_required": True,
        "static_outward_sign_structurally_possible": False,
        "empirical_status": "NOT_RELEVANT_TO_STATIC_G00_FAILURE",
        "source_realization_status": "STATIC_BRANCH",
        "project_status": "CLOSED_STATIC_BY_032F_AND_014_015_SCOPE",
        "reason": "D0PHI_ZERO_IMPLIES_NO_DIRECT_STATIC_G00_METRIC_RESPONSE",
    },
    {
        "priority": 5,
        "operator_id": "STANDARD_STATIC_SCALAR_TENSOR_YUKAWA",
        "schematic_metric": "F(phi)R_plus_universal_Jordan_metric",
        "local_covariant": True,
        "one_physical_metric": True,
        "static_g00_response": True,
        "stand_off_structurally_possible": True,
        "symmetry_protection_available": "MODEL_DEPENDENT",
        "separate_charge_mediator_required": False,
        "canonical_normalization_guard_required": True,
        "static_outward_sign_structurally_possible": False,
        "empirical_status": "MODEL_DEPENDENT",
        "source_realization_status": "KNOWN",
        "project_status": "TESTED_STATIC_BRANCHES_ATTRACTIVE_OR_ZERO_032P_032L_032M",
        "reason": "KNOWN_TESTED_STATIC_UNIVERSAL_BRANCHES_HAVE_NONNEGATIVE_ATTRACTIVE_STRENGTH",
    },
    {
        "priority": 6,
        "operator_id": "SECONDARY_TOPOLOGICAL_CHARGE_PORTAL",
        "schematic_metric": "HOPF_OR_CS_CHARGE_PLUS_ADDED_METRIC_MEDIATOR",
        "local_covariant": False,
        "one_physical_metric": False,
        "static_g00_response": False,
        "stand_off_structurally_possible": False,
        "symmetry_protection_available": True,
        "separate_charge_mediator_required": True,
        "canonical_normalization_guard_required": True,
        "static_outward_sign_structurally_possible": "SOURCE_ONLY",
        "empirical_status": "UNRESOLVED",
        "source_realization_status": "GLOBAL_SCALING_LEARNING_ONLY",
        "project_status": "DEMOTED_BY_032V9_032V10",
        "reason": "GLOBAL_Q_SCALING_NOT_LOCAL_FINITE_PAYLOAD_METRIC_ACTIVE_CHARGE",
    },
    {
        "priority": 7,
        "operator_id": "VECTOR_METRIC_PORTAL",
        "schematic_metric": "gphys=g_plus_vector_structures",
        "local_covariant": True,
        "one_physical_metric": "MODEL_DEPENDENT",
        "static_g00_response": True,
        "stand_off_structurally_possible": True,
        "symmetry_protection_available": "TESTED_PROTECTIONS_FAILED",
        "separate_charge_mediator_required": False,
        "canonical_normalization_guard_required": True,
        "static_outward_sign_structurally_possible": "MODEL_DEPENDENT",
        "empirical_status": "PREVIOUSLY_SCREENED",
        "source_realization_status": "CLOSED_TESTED_IMPLEMENTATIONS",
        "project_status": "CLOSED_THROUGH_022A_ABSENT_GENUINELY_NEW_PROTECTION",
        "reason": "DO_NOT_REOPEN_PROTECTED_VECTOR_IMPLEMENTATIONS",
    },
    {
        "priority": 8,
        "operator_id": "MINIMAL_TORSION_OR_HYPERMOMENTUM",
        "schematic_metric": "connection_source",
        "local_covariant": True,
        "one_physical_metric": True,
        "static_g00_response": False,
        "stand_off_structurally_possible": False,
        "symmetry_protection_available": True,
        "separate_charge_mediator_required": False,
        "canonical_normalization_guard_required": True,
        "static_outward_sign_structurally_possible": False,
        "empirical_status": "NOT_RELEVANT",
        "source_realization_status": "MINIMAL_BRANCHES_CLOSED",
        "project_status": "CLOSED_OR_BLOCKED_032Q_032T_032U",
        "reason": "ALGEBRAIC_CONNECTION_OR_NO_UNIVERSAL_ORDINARY_MATTER_PORTAL",
    },
    {
        "priority": 9,
        "operator_id": "MATTER_TRIGGERED_PFORM",
        "schematic_metric": "pform_spontaneous_growth",
        "local_covariant": True,
        "one_physical_metric": True,
        "static_g00_response": "AFTER_TRIGGER",
        "stand_off_structurally_possible": "MODEL_DEPENDENT",
        "symmetry_protection_available": "MODEL_DEPENDENT",
        "separate_charge_mediator_required": False,
        "canonical_normalization_guard_required": True,
        "static_outward_sign_structurally_possible": "UNRESOLVED",
        "empirical_status": "UNRESOLVED",
        "source_realization_status": "10MJ_TRIGGER_DOMAIN_FAILED",
        "project_status": "DECLARED_032R_DOMAIN_CLOSED_FULL_CLASS_OPEN",
        "reason": "EVEN_PLANCK_RADIUS_10MJ_ORACLE_REQUIRED_COUPLING_ABOVE_DECLARED_RANGE",
    },
    {
        "priority": 10,
        "operator_id": "PURE_GR_STRESS_ENERGY",
        "schematic_metric": "Einstein_equation_Tmunu",
        "local_covariant": True,
        "one_physical_metric": True,
        "static_g00_response": True,
        "stand_off_structurally_possible": True,
        "symmetry_protection_available": True,
        "separate_charge_mediator_required": False,
        "canonical_normalization_guard_required": True,
        "static_outward_sign_structurally_possible": True,
        "empirical_status": "STANDARD_GR",
        "source_realization_status": "006D_EXISTS",
        "project_status": "PRACTICAL_SUB10MJ_CLOSED_BY_1_OVER_G_BURDEN",
        "reason": "NO_TESTED_PURE_GR_MECHANISM_ESCAPES_E_EQUALS_C_A_C2_H2_OVER_G",
    },
]

# ============================================================
# 2. STRUCTURAL SIGN TEST FOR THE NEW TOP CLASS
# ============================================================

DY_DR = -1.0e-16
DLNC_DY = 1.0

KINETIC_CONFORMAL_ACCEL = static_kinetic_conformal_acceleration(
    DLNC_DY,
    DY_DR,
)

KINETIC_CONFORMAL_OUTWARD = (
    KINETIC_CONFORMAL_ACCEL > 0.0
)

assert KINETIC_CONFORMAL_OUTWARD
assert kinetic_conformal_outward_for_localized_gradient(1.0)

# The previously tested purely static induced/disformal metric remains zero.
STATIC_PURE_DISFORMAL_G00 = static_pure_disformal_g00_shift(
    0.0,
    1.0e30,
)

assert STATIC_PURE_DISFORMAL_G00 == 0.0

# ============================================================
# 3. NORMALIZATION GUARD
# ============================================================

KAPPA = 3.0
Z = 2.0
FIELD_RESCALE = 7.0

KAPPA_CANONICAL = canonical_derivative_metric_coefficient(
    KAPPA,
    Z,
)

KAPPA_CANONICAL_RESCALED = canonical_derivative_metric_coefficient(
    KAPPA/(FIELD_RESCALE**2),
    Z/(FIELD_RESCALE**2),
)

NORMALIZATION_RELERR = abs(
    KAPPA_CANONICAL_RESCALED-KAPPA_CANONICAL
) / abs(KAPPA_CANONICAL)

assert NORMALIZATION_RELERR < 1.0e-15

# ============================================================
# 4. FORMAL PREFIELD PROMOTION
# ============================================================

top_record = OperatorRecord(
    operator_id="SHIFT_SYMMETRIC_X_DEPENDENT_CONFORMAL_METRIC",
    local_covariant=True,
    one_physical_metric=True,
    static_g00_response=True,
    external_standoff_structurally_possible=True,
    symmetry_protection_available=True,
    separate_propagating_charge_mediator_required=False,
    project_closed=False,
)

TOP_PREFIELD_OPEN = operator_prefield_open(top_record)

assert TOP_PREFIELD_OPEN

# This is an operator preflight, not physical-model promotion.
PHYSICAL_MODEL_FOUND = False
CERTIFIED_SUB10MJ = False

# ============================================================
# 5. WRITE ATLAS
# ============================================================

CSV_OUT.parent.mkdir(parents=True, exist_ok=True)

with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(rows[0].keys()),
    )
    writer.writeheader()
    writer.writerows(rows)

decision = (
    "GREEN_OPERATOR_ATLAS_KINETIC_CONFORMAL_X_METRIC_TOP_PREFIELD_CLASS"
)

next_step = (
    "032V13_SHIFT_SYMMETRIC_KINETIC_CONFORMAL_FINITE_PAYLOAD_ENERGY_EMPIRICAL_ORACLE"
)

result = {
    "branch": "032V12_LOCAL_METRIC_ACTIVE_SOURCE_OPERATOR_ATLAS",
    "claim_class": "OPERATOR_LEVEL_RERANK_NOT_PHYSICAL_FIELD",
    "strict_target_j": STRICT_TARGET_J,
    "strict_policy_changed": False,
    "top_operator": {
        "operator_id": top_record.operator_id,
        "schematic_physical_metric": "gphys=C(X)g+D(X)dphi_dphi",
        "shift_symmetry": "phi_to_phi_plus_constant",
        "static_spatial_gradient_changes_g00": True,
        "static_outward_sign_possible": KINETIC_CONFORMAL_OUTWARD,
        "example_dlnc_dy": DLNC_DY,
        "example_dy_dr_per_m": DY_DR,
        "example_acceleration_mps2": KINETIC_CONFORMAL_ACCEL,
        "separate_charge_mediator_required": False,
        "prefield_operator_open": TOP_PREFIELD_OPEN,
        "physical_source_realized": False,
        "finite_payload_energy_computed": False,
        "complete_operating_ledger": False,
        "empirical_operator_matching_complete": False,
    },
    "normalization_guard": {
        "canonical_coefficient_rule": "kappa_canonical=kappa_raw/Z",
        "example_canonical_coefficient": KAPPA_CANONICAL,
        "example_after_field_rescale": KAPPA_CANONICAL_RESCALED,
        "relative_error": NORMALIZATION_RELERR,
        "arbitrary_raw_kappa_is_independent_physical_lever": False,
    },
    "closed_scope_preservation": {
        "032f_static_pure_disformal_g00_shift": STATIC_PURE_DISFORMAL_G00,
        "032f_static_pure_disformal_reopened": False,
        "031f0_unprotected_ultralight_scalar_reopened": False,
        "hopf_promoted_to_finite_payload_oracle": False,
        "published_asymmetron_bubble_reopened": False,
        "protected_vectors_reopened": False,
        "pure_gr_practical_branch_reopened": False,
    },
    "why_top_class_is_distinct": [
        "C_DEPENDS_ON_KINETIC_INVARIANT_X",
        "STATIC_SPATIAL_GRADIENT_MODIFIES_PHYSICAL_G00",
        "SHIFT_SYMMETRY_CAN_REMAIN_EXACT",
        "NO_ULTRALIGHT_SCALAR_POTENTIAL_MASS_REQUIRED_AT_OPERATOR_LEVEL",
        "NO_SEPARATE_PROPAGATING_CHARGE_MEDIATOR_REQUIRED",
    ],
    "major_open_gates": [
        "EXPLICIT_SOURCE_REALIZATION",
        "FINITE_PAYLOAD_KERNEL",
        "COMPLETE_POSITIVE_ENERGY_LEDGER",
        "CANONICAL_WILSON_COEFFICIENT_RANGE",
        "DHOST_OR_EQUIVALENT_HEALTH_CONDITIONS",
        "INVERTIBILITY_OF_PHYSICAL_METRIC_MAP",
        "EMPIRICAL_COLLIDER_PULSAR_AND_EP_OPERATOR_MATCHING",
        "REACTION_AND_BACKREACTION",
        "NONLINEAR_STABILITY",
    ],
    "operator_atlas": rows,
    "physical_antigravity_model_found": PHYSICAL_MODEL_FOUND,
    "certified_sub10mj_model_found": CERTIFIED_SUB10MJ,
    "decision": decision,
    "next": next_step,
}

OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032V12 RESULT ===")
print("TOP_OPERATOR=" + top_record.operator_id)
print("TOP_OPERATOR_PREFIELD_OPEN=" + str(TOP_PREFIELD_OPEN))
print("STATIC_KINETIC_CONFORMAL_G00_RESPONSE=True")
print("LOCALIZED_GRADIENT_DY_DR_SIGN=NEGATIVE")
print("OUTWARD_REQUIRES_DLN_C_DY_POSITIVE=True")
print("KINETIC_CONFORMAL_EXAMPLE_ACCEL_MPS2=" + format(KINETIC_CONFORMAL_ACCEL, ".12e"))

print("STATIC_PURE_DISFORMAL_G00_SHIFT=" + format(STATIC_PURE_DISFORMAL_G00, ".12e"))
print("032F_STATIC_PURE_DISFORMAL_REOPENED=False")

print("CANONICAL_KAPPA_OVER_Z=" + format(KAPPA_CANONICAL, ".12e"))
print("CANONICAL_RESCALE_RELERR=" + format(NORMALIZATION_RELERR, ".12e"))
print("RAW_KAPPA_AS_INDEPENDENT_LEVER=False")

print("SHIFT_SYMMETRY_PROTECTION_AVAILABLE=True")
print("SEPARATE_CHARGE_MEDIATOR_REQUIRED=False")
print("EMPIRICAL_OPERATOR_MATCHING_COMPLETE=False")
print("FINITE_PAYLOAD_ENERGY_COMPUTED=False")
print("PHYSICAL_ANTIGRAVITY_MODEL_FOUND=NO")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=NO")
print("DECISION=" + decision)
print("NEXT=" + next_step)
