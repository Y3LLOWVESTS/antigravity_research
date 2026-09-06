"""032V9 Hopf metric portal locality and mediator self-energy gate."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.policy import current_energy_policy
from antigravity_research.agminer.families.family_032v9_hopf_metric_portal_preflight import (
    HopfPortalStructure,
    fixed_response_ratio_linear_portal,
    linear_portal_asymptotic_exponent,
    maximum_mediator_coefficient_for_ratio,
    minimum_ratio_linear_portal,
    optimum_charge_scale_linear_portal,
    quadratic_metric_portal_asymptotic_exponent,
)


ROOT = Path(__file__).resolve().parents[1]
V8 = ROOT / "results" / "data" / "032v8_faddeev_hopf_shared_scaffold_summary.json"
OUT = ROOT / "results" / "data" / "032v9_hopf_metric_portal_preflight_summary.json"
CSV_OUT = ROOT / "results" / "data" / "032v9_hopf_metric_portal_matrix.csv"

STRICT_TARGET_J = 1.0e7
STRETCH_TARGET_J = 1.0e6

policy = current_energy_policy()
assert float(policy["limit_j"]) == STRICT_TARGET_J
assert str(policy["comparison"]) == "LT"

if not V8.exists():
    raise FileNotFoundError(str(V8))

v8 = json.loads(V8.read_text(encoding="utf-8"))

assert v8["decision"] == "GREEN_HOPF_Q3OVER4_SOURCE_SCALING_STRONG_ENOUGH_CONDITIONALLY"
assert v8["portal"]["hopf_charge_to_gravitational_charge_established"] is False
assert v8["physical_antigravity_model_found"] is False

REFERENCE_J = float(v8["canonical_reference_j"])
R10 = STRICT_TARGET_J / REFERENCE_J
R1 = STRETCH_TARGET_J / REFERENCE_J

structure = HopfPortalStructure()

MU_MAX_10 = maximum_mediator_coefficient_for_ratio(R10)
MU_MAX_1 = maximum_mediator_coefficient_for_ratio(R1)

QOPT_10 = optimum_charge_scale_linear_portal(MU_MAX_10)
QOPT_1 = optimum_charge_scale_linear_portal(MU_MAX_1)

RMIN_10 = minimum_ratio_linear_portal(MU_MAX_10)
RMIN_1 = minimum_ratio_linear_portal(MU_MAX_1)

assert abs(RMIN_10 - R10) / R10 < 1e-12
assert abs(RMIN_1 - R1) / R1 < 1e-12

Q_V8_10 = float(v8["scaling"]["q_required_10mj"])
Q_V8_1 = float(v8["scaling"]["q_required_1mj"])

Q_PROBE_10 = 1.0e12
Q_PROBE_1 = 1.0e15

SOURCE_RATIO_Q1E12 = Q_PROBE_10 ** (-0.25)
SOURCE_RATIO_Q1E15 = Q_PROBE_1 ** (-0.25)

MU_AT_Q1E12_10 = (
    R10 - SOURCE_RATIO_Q1E12
) / Q_PROBE_10

MU_AT_Q1E15_1 = (
    R1 - SOURCE_RATIO_Q1E15
) / Q_PROBE_1

assert MU_AT_Q1E12_10 > 0.0
assert MU_AT_Q1E15_1 > 0.0

LINEAR_ASYMPTOTIC = linear_portal_asymptotic_exponent()
QUADRATIC_ASYMPTOTIC = quadratic_metric_portal_asymptotic_exponent()

rows = [
    {
        "portal": "MINIMAL_EINSTEIN_STRESS_ENERGY",
        "static_hopf_charge_source": False,
        "local_covariant": True,
        "universal_metric": True,
        "canonical_mediator_energy_exponent": "",
        "metric_response_exponent": "",
        "asymptotic_efficiency_exponent": "",
        "status": "RED_NO_INDEPENDENT_HOPF_GRAVITATIONAL_CHARGE",
        "reason": "METRIC_SEES_T_MUNU_NOT_SIGNED_HOPF_CHARGE",
    },
    {
        "portal": "SCALAR_DERIVATIVE_HOPF_CURRENT",
        "static_hopf_charge_source": False,
        "local_covariant": True,
        "universal_metric": "POSSIBLE_AFTER_SCALAR_EXISTS",
        "canonical_mediator_energy_exponent": 2.0,
        "metric_response_exponent": 1.0,
        "asymptotic_efficiency_exponent": LINEAR_ASYMPTOTIC,
        "status": "RED_STATIC_BULK_SOURCE",
        "reason": "DERIVATIVE_COUPLING_TO_CONSERVED_CURRENT_REDUCES_TO_BOUNDARY_OR_TOPOLOGY_CHANGE",
    },
    {
        "portal": "PSEUDOSCALAR_LOCAL_F_DUAL_F",
        "static_hopf_charge_source": False,
        "local_covariant": True,
        "universal_metric": "POSSIBLE_AFTER_SCALAR_EXISTS",
        "canonical_mediator_energy_exponent": 2.0,
        "metric_response_exponent": 1.0,
        "asymptotic_efficiency_exponent": LINEAR_ASYMPTOTIC,
        "status": "RED_FOR_STATIC_PURELY_SPATIAL_HOPF_SECTOR",
        "reason": "FOUR_DIMENSIONAL_PSEUDOSCALAR_DENSITY_REQUIRES_TIME_OR_ELECTRIC_COMPONENT",
    },
    {
        "portal": "AUXILIARY_VECTOR_TIMES_HOPF_CURRENT",
        "static_hopf_charge_source": True,
        "local_covariant": "REQUIRES_AUXILIARY_CONNECTION_OR_LIFT",
        "universal_metric": "NOT_ESTABLISHED",
        "canonical_mediator_energy_exponent": 2.0,
        "metric_response_exponent": 1.0,
        "asymptotic_efficiency_exponent": LINEAR_ASYMPTOTIC,
        "status": "OPEN_STRUCTURALLY_BUT_Q1OVER4_GAIN_LOST_WITH_CANONICAL_LINEAR_RESPONSE",
        "reason": "MEDIATOR_SELF_ENERGY_GROWS_Q_SQUARED",
    },
    {
        "portal": "AUXILIARY_VECTOR_QUADRATIC_PHYSICAL_METRIC",
        "static_hopf_charge_source": True,
        "local_covariant": "REQUIRES_AUXILIARY_CONNECTION_OR_LIFT",
        "universal_metric": "NOT_ESTABLISHED",
        "canonical_mediator_energy_exponent": 2.0,
        "metric_response_exponent": 2.0,
        "asymptotic_efficiency_exponent": QUADRATIC_ASYMPTOTIC,
        "status": "OPEN_BUT_EFFICIENCY_SATURATES",
        "reason": "Q_SQUARED_RESPONSE_AND_Q_SQUARED_MEDIATOR_ENERGY_REMOVE_TOPOLOGICAL_SCALING_GAIN",
    },
    {
        "portal": "PURE_TOPOLOGICAL_BF_OR_CS_SECTOR",
        "static_hopf_charge_source": "FORMALLY_POSSIBLE",
        "local_covariant": "THEORY_DEPENDENT",
        "universal_metric": False,
        "canonical_mediator_energy_exponent": 0.0,
        "metric_response_exponent": 0.0,
        "asymptotic_efficiency_exponent": 0.0,
        "status": "RED_AS_STANDALONE_FORCE_PORTAL",
        "reason": "PURE_TOPOLOGICAL_SECTOR_HAS_NO_LOCAL_PROPAGATING_STATIC_FORCE;KINETIC_COMPLETION_REINTRODUCES_ENERGY",
    },
]

CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

minimal_local_static_portal_preserving_qquarter_found = False
full_topological_portal_class_closed = False

decision = "RED_MINIMAL_LOCAL_HOPF_PORTALS_DO_NOT_PRESERVE_Q1OVER4_ADVANTAGE"
next_step = "032V10_LOCAL_COVARIANT_METRIC_ACTIVE_CHARGE_WITH_SUBLINEAR_SCAFFOLD_RERANK"

result = {
    "branch": "032V9_HOPF_METRIC_PORTAL_PREFLIGHT",
    "claim_class": "PORTAL_LOCALITY_AND_SELF_ENERGY_SCALING_PREFLIGHT",
    "strict_target_j": STRICT_TARGET_J,
    "stretch_target_j": STRETCH_TARGET_J,
    "reference_j": REFERENCE_J,
    "source_result_preserved": {
        "hopf_source_energy_exponent": 0.75,
        "conditional_source_efficiency_exponent": 0.25,
        "source_only_q_required_10mj": Q_V8_10,
        "source_only_q_required_1mj": Q_V8_1,
        "source_only_result_invalidated": False,
        "source_only_result_is_physical_antigravity": False,
    },
    "hopf_locality": {
        "secondary_invariant": structure.hopf_is_secondary_invariant,
        "h3_s2_zero": structure.h3_s2_zero,
        "local_target_space_three_form_density_exists": structure.local_target_space_three_form_density_exists,
        "auxiliary_connection_required_for_cs_density": structure.auxiliary_connection_required_for_cs_density,
        "direct_minimal_einstein_hopf_charge_portal": structure.direct_minimal_einstein_hopf_charge_portal,
        "derivative_scalar_current_static_bulk_source": structure.derivative_scalar_current_static_bulk_source,
    },
    "canonical_linear_mediator": {
        "fixed_response_ratio": "Q^(-1/4)+mu*Q",
        "mediator_energy_exponent": 2.0,
        "linear_metric_response_exponent": 1.0,
        "asymptotic_efficiency_exponent": LINEAR_ASYMPTOTIC,
        "mu_max_10mj": MU_MAX_10,
        "mu_max_1mj": MU_MAX_1,
        "optimal_q_at_10mj_threshold": QOPT_10,
        "optimal_q_at_1mj_threshold": QOPT_1,
        "mu_max_at_fixed_q1e12_for_10mj": MU_AT_Q1E12_10,
        "mu_max_at_fixed_q1e15_for_1mj": MU_AT_Q1E15_1,
    },
    "quadratic_metric_portal": {
        "metric_response_exponent": 2.0,
        "mediator_energy_exponent": 2.0,
        "asymptotic_efficiency_exponent": QUADRATIC_ASYMPTOTIC,
        "topological_scaling_provides_unbounded_gain": False,
    },
    "portal_matrix": rows,
    "minimal_local_static_portal_preserving_qquarter_found": minimal_local_static_portal_preserving_qquarter_found,
    "full_topological_portal_class_closed": full_topological_portal_class_closed,
    "physical_antigravity_model_found": False,
    "certified_sub10mj_model_found": False,
    "decision": decision,
    "next": next_step,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032V9 RESULT ===")
print("REFERENCE_GJ=" + format(REFERENCE_J/1e9, ".12e"))
print("TARGET_RATIO_10MJ=" + format(R10, ".12e"))
print("TARGET_RATIO_1MJ=" + format(R1, ".12e"))

print("HOPF_SECONDARY_INVARIANT=" + str(structure.hopf_is_secondary_invariant))
print("LOCAL_TARGET_SPACE_3FORM_DENSITY_EXISTS=" + str(structure.local_target_space_three_form_density_exists))
print("AUXILIARY_CONNECTION_REQUIRED=" + str(structure.auxiliary_connection_required_for_cs_density))

print("LINEAR_MEDIATOR_ASYMPTOTIC_EFFICIENCY_EXPONENT=" + format(LINEAR_ASYMPTOTIC, ".12e"))
print("QUADRATIC_METRIC_ASYMPTOTIC_EFFICIENCY_EXPONENT=" + format(QUADRATIC_ASYMPTOTIC, ".12e"))

print("MU_MAX_10MJ=" + format(MU_MAX_10, ".12e"))
print("Q_OPT_10MJ=" + format(QOPT_10, ".12e"))
print("MU_MAX_Q1E12_10MJ=" + format(MU_AT_Q1E12_10, ".12e"))

print("MU_MAX_1MJ=" + format(MU_MAX_1, ".12e"))
print("Q_OPT_1MJ=" + format(QOPT_1, ".12e"))
print("MU_MAX_Q1E15_1MJ=" + format(MU_AT_Q1E15_1, ".12e"))

print("MINIMAL_LOCAL_STATIC_PORTAL_PRESERVING_Q1OVER4_FOUND=False")
print("FULL_TOPOLOGICAL_PORTAL_CLASS_CLOSED=False")
print("PHYSICAL_ANTIGRAVITY_MODEL_FOUND=NO")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=NO")
print("DECISION=" + decision)
print("NEXT=" + next_step)
