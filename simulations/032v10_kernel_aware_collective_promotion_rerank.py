"""032V10 kernel-aware collective promotion and portal-ready rerank."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.kernel_scaling import (
    assess_collective_promotion,
    maximum_combined_tax,
    minimum_retention_fraction,
    net_efficiency_exponent,
    required_kernel_exponent,
    source_gain,
)
from antigravity_research.agminer.policy import current_energy_policy


ROOT = Path(__file__).resolve().parents[1]

V8 = ROOT / "results" / "data" / "032v8_faddeev_hopf_shared_scaffold_summary.json"
V9 = ROOT / "results" / "data" / "032v9_hopf_metric_portal_preflight_summary.json"

OUT = ROOT / "results" / "data" / "032v10_kernel_aware_collective_promotion_summary.json"
CSV_OUT = ROOT / "results" / "data" / "032v10_kernel_headroom_budget.csv"
MATRIX_OUT = ROOT / "results" / "data" / "032v10_portal_ready_rerank.csv"

STRICT_TARGET_J = 1.0e7
STRETCH_TARGET_J = 1.0e6

policy = current_energy_policy()
assert float(policy["limit_j"]) == STRICT_TARGET_J
assert str(policy["comparison"]) == "LT"

for path in (V8, V9):
    if not path.exists():
        raise FileNotFoundError(str(path))

v8 = json.loads(V8.read_text(encoding="utf-8"))
v9 = json.loads(V9.read_text(encoding="utf-8"))

assert v8["physical_antigravity_model_found"] is False
assert v9["decision"] == "RED_MINIMAL_LOCAL_HOPF_PORTALS_DO_NOT_PRESERVE_Q1OVER4_ADVANTAGE"

REFERENCE_J = float(v8["canonical_reference_j"])
G10 = REFERENCE_J / STRICT_TARGET_J
G1 = REFERENCE_J / STRETCH_TARGET_J

SOURCE_DELTA = float(v8["source_family"]["efficiency_exponent"])
assert abs(SOURCE_DELTA - 0.25) < 1e-12

# Published numerical morphology evidence only, not a continuum theorem:
# Sutcliffe 2007 found Hopf-string length approximately proportional
# to Q^(3/4) for the studied Q<=16 configurations.
HOPF_STRING_LENGTH_EXPONENT_DIAGNOSTIC = 0.75

FIXED_PRODUCTIVE_SEGMENT_KERNEL_EXPONENT = -HOPF_STRING_LENGTH_EXPONENT_DIAGNOSTIC

FIXED_SEGMENT_NET_EXPONENT = net_efficiency_exponent(
    SOURCE_DELTA,
    FIXED_PRODUCTIVE_SEGMENT_KERNEL_EXPONENT,
)

assert abs(FIXED_SEGMENT_NET_EXPONENT + 0.5) < 1e-12

headroom_rows = []

for qscale in (1.0e9, 1.0e12, 1.0e15, 1.0e18):
    gain = source_gain(qscale, SOURCE_DELTA)

    headroom_rows.append({
        "charge_scale": qscale,
        "global_source_gain": gain,
        "max_combined_tax_10mj": maximum_combined_tax(gain, G10),
        "minimum_retention_10mj": minimum_retention_fraction(gain, G10),
        "required_kernel_exponent_10mj": required_kernel_exponent(SOURCE_DELTA, G10, qscale),
        "max_combined_tax_1mj": maximum_combined_tax(gain, G1),
        "minimum_retention_1mj": minimum_retention_fraction(gain, G1),
        "required_kernel_exponent_1mj": required_kernel_exponent(SOURCE_DELTA, G1, qscale),
    })

hopf_promotion = assess_collective_promotion(
    local_covariant_charge=False,
    physical_vacuum_portal=False,
    finite_payload_response_derived=False,
    complete_portal_energy_scaling_derived=False,
    normalization_invariant=True,
    naturalness_screened=False,
)

assert hopf_promotion.promotable is False

portal_rows = [
    {
        "priority": 1,
        "family": "2026_ASYMMETRON_BUBBLE_BRANCH",
        "local_covariant_metric_active_field": True,
        "universal_physical_metric": True,
        "separate_charge_mediator_required": False,
        "finite_payload_outward_response_established": False,
        "complete_operating_energy_established": False,
        "naturalness_certified": False,
        "status": "OPEN_HIGHEST_PRIORITY_PORTAL_READY_STRUCTURE",
        "reason": "FIELD_ITSELF_IS_UNIVERSAL_METRIC_ACTIVE_AND_BUBBLE_BRANCH_IS_DISTINCT_FROM_STANDARD_SCREENED_BODY",
    },
    {
        "priority": 2,
        "family": "LOCAL_NOETHER_CHARGE_PLUS_NONLINEAR_PROTECTED_METRIC_FIELD",
        "local_covariant_metric_active_field": "SOURCE_CURRENT_LOCAL_PORTAL_NOT_FOUND",
        "universal_physical_metric": "REQUIRED",
        "separate_charge_mediator_required": True,
        "finite_payload_outward_response_established": False,
        "complete_operating_energy_established": False,
        "naturalness_certified": False,
        "status": "OPEN_IF_MEDIATOR_SCALING_BEATS_CANONICAL_Q2_TAX",
        "reason": "QBALL_NOETHER_CURRENT_IS_LOCAL_BUT_STANDOFF_REQUIRES_VACUUM_PROPAGATION",
    },
    {
        "priority": 3,
        "family": "SCALARIZED_BOSON_STAR_SCALAR_TENSOR",
        "local_covariant_metric_active_field": True,
        "universal_physical_metric": True,
        "separate_charge_mediator_required": False,
        "finite_payload_outward_response_established": False,
        "complete_operating_energy_established": False,
        "naturalness_certified": False,
        "status": "OPEN_LOW_PRIORITY_COMPACTNESS_DEPENDENT",
        "reason": "PHYSICAL_SCALARIZATION_EXISTS_BUT_KNOWN_REALIZATIONS_ARE_SELF_GRAVITATING_COMPACT_OBJECTS",
    },
    {
        "priority": 4,
        "family": "SHIFT_SYMMETRIC_SCALAR_GAUSS_BONNET_STAR",
        "local_covariant_metric_active_field": True,
        "universal_physical_metric": True,
        "separate_charge_mediator_required": False,
        "finite_payload_outward_response_established": False,
        "complete_operating_energy_established": False,
        "naturalness_certified": "SHIFT_SYMMETRY_PRESENT",
        "status": "RED_STAR_SCALAR_CHARGE_ZERO",
        "reason": "REGULAR_STARS_HAVE_ZERO_LONG_RANGE_SCALAR_CHARGE_IN_SHIFT_SYMMETRIC_LINEAR_GB_BRANCH",
    },
    {
        "priority": 5,
        "family": "HOPF_GLOBAL_TOPOLOGICAL_CHARGE",
        "local_covariant_metric_active_field": False,
        "universal_physical_metric": False,
        "separate_charge_mediator_required": True,
        "finite_payload_outward_response_established": False,
        "complete_operating_energy_established": False,
        "naturalness_certified": False,
        "status": "DEMOTED_GLOBAL_SOURCE_SCALING_LEARNING_ONLY",
        "reason": "SECONDARY_INVARIANT_AND_NO_LOCAL_PORTAL_PRESERVING_Q1OVER4_FOUND",
    },
    {
        "priority": 6,
        "family": "MINIMAL_MAG_OR_ALGEBRAIC_TORSION_HYPERMOMENTUM",
        "local_covariant_metric_active_field": True,
        "universal_physical_metric": "MINIMAL_PAYLOAD_RESPONSE_INSUFFICIENT",
        "separate_charge_mediator_required": False,
        "finite_payload_outward_response_established": False,
        "complete_operating_energy_established": False,
        "naturalness_certified": "NOT_RELEVANT_TO_CLOSED_MINIMAL_BRANCH",
        "status": "RED_OR_BLOCKED_BY_032Q_032T_032U",
        "reason": "ALGEBRAIC_CONNECTION_HAS_NO_EXTERNAL_STANDOFF_OR_ORDINARY_MATTER_PORTAL_IS_ABSENT",
    },
]

CSV_OUT.parent.mkdir(parents=True, exist_ok=True)

with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(headroom_rows[0].keys()))
    writer.writeheader()
    writer.writerows(headroom_rows)

with MATRIX_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(portal_rows[0].keys()))
    writer.writeheader()
    writer.writerows(portal_rows)

q12 = next(row for row in headroom_rows if row["charge_scale"] == 1.0e12)
q15 = next(row for row in headroom_rows if row["charge_scale"] == 1.0e15)

decision = "GREEN_KERNEL_AWARE_PROMOTION_GATE_HOPF_DEMOTED_TO_GLOBAL_SCALING_LEARNING"
next_step = "032V11_ASYMMETRON_BUBBLE_FINITE_PAYLOAD_SIGN_ENERGY_PREFLIGHT"

result = {
    "branch": "032V10_KERNEL_AWARE_COLLECTIVE_PROMOTION",
    "claim_class": "MINER_PROMOTION_DISCIPLINE_AND_PORTAL_READY_RERANK",
    "strict_target_j": STRICT_TARGET_J,
    "stretch_target_j": STRETCH_TARGET_J,
    "reference_j": REFERENCE_J,
    "required_gain_10mj": G10,
    "required_gain_1mj": G1,
    "hopf": {
        "global_source_efficiency_exponent": SOURCE_DELTA,
        "global_scaling_result_preserved": True,
        "global_scaling_is_finite_payload_oracle": False,
        "collective_promotion_allowed": hopf_promotion.promotable,
        "promotion_failures": list(hopf_promotion.reasons),
        "published_string_length_exponent_diagnostic": HOPF_STRING_LENGTH_EXPONENT_DIAGNOSTIC,
        "string_length_exponent_is_continuum_theorem": False,
        "fixed_productive_segment_kernel_exponent_diagnostic": FIXED_PRODUCTIVE_SEGMENT_KERNEL_EXPONENT,
        "fixed_productive_segment_net_efficiency_exponent_diagnostic": FIXED_SEGMENT_NET_EXPONENT,
    },
    "headroom_examples": {
        "q1e12_minimum_retention_10mj": q12["minimum_retention_10mj"],
        "q1e12_max_combined_tax_10mj": q12["max_combined_tax_10mj"],
        "q1e12_required_kernel_exponent_10mj": q12["required_kernel_exponent_10mj"],
        "q1e15_minimum_retention_10mj": q15["minimum_retention_10mj"],
        "q1e15_max_combined_tax_10mj": q15["max_combined_tax_10mj"],
        "q1e15_minimum_retention_1mj": q15["minimum_retention_1mj"],
        "q1e15_max_combined_tax_1mj": q15["max_combined_tax_1mj"],
        "q1e15_required_kernel_exponent_1mj": q15["required_kernel_exponent_1mj"],
    },
    "portal_ready_rerank": portal_rows,
    "highest_priority_open_structure": "2026_ASYMMETRON_BUBBLE_BRANCH",
    "physical_antigravity_model_found": False,
    "certified_sub10mj_model_found": False,
    "decision": decision,
    "next": next_step,
}

OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032V10 RESULT ===")
print("REFERENCE_GJ=" + format(REFERENCE_J/1e9, ".12e"))
print("REQUIRED_GAIN_10MJ=" + format(G10, ".12e"))
print("REQUIRED_GAIN_1MJ=" + format(G1, ".12e"))

print("HOPF_GLOBAL_SOURCE_DELTA=" + format(SOURCE_DELTA, ".12e"))
print("HOPF_GLOBAL_SCALING_IS_FINITE_PAYLOAD_ORACLE=False")
print("HOPF_COLLECTIVE_PROMOTION_ALLOWED=" + str(hopf_promotion.promotable))

print("Q1E12_MIN_RETENTION_10MJ=" + format(q12["minimum_retention_10mj"], ".12e"))
print("Q1E12_MAX_TOTAL_TAX_10MJ=" + format(q12["max_combined_tax_10mj"], ".12e"))
print("Q1E12_KERNEL_EXPONENT_FLOOR_10MJ=" + format(q12["required_kernel_exponent_10mj"], ".12e"))

print("Q1E15_MIN_RETENTION_10MJ=" + format(q15["minimum_retention_10mj"], ".12e"))
print("Q1E15_MAX_TOTAL_TAX_10MJ=" + format(q15["max_combined_tax_10mj"], ".12e"))
print("Q1E15_MIN_RETENTION_1MJ=" + format(q15["minimum_retention_1mj"], ".12e"))
print("Q1E15_MAX_TOTAL_TAX_1MJ=" + format(q15["max_combined_tax_1mj"], ".12e"))
print("Q1E15_KERNEL_EXPONENT_FLOOR_1MJ=" + format(q15["required_kernel_exponent_1mj"], ".12e"))

print("HOPF_STRING_LENGTH_Q3OVER4=NUMERICAL_DIAGNOSTIC_NOT_THEOREM")
print("FIXED_PRODUCTIVE_SEGMENT_NET_DELTA=" + format(FIXED_SEGMENT_NET_EXPONENT, ".12e"))

print("HIGHEST_PRIORITY_OPEN_STRUCTURE=2026_ASYMMETRON_BUBBLE_BRANCH")
print("PHYSICAL_ANTIGRAVITY_MODEL_FOUND=NO")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=NO")
print("DECISION=" + decision)
print("NEXT=" + next_step)
