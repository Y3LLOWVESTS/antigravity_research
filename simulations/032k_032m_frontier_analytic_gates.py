"""032K-032M independent frontier analytic closeout."""

import json
import math
from pathlib import Path

from antigravity_research.agminer.policy import current_energy_policy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "data" / "032k_032m_frontier_analytic_gates_summary.json"

C = 299792458.0
A_TARGET = 9.80665
PAYLOAD_RADIUS_M = 0.10

policy = current_energy_policy()

# Any universal conformal metric force obeys approximately
# a = -c^2 grad(ln A) in the weak, quasistatic limit.
required_grad_ln_a_per_m = A_TARGET / C ** 2
required_delta_ln_a_across_payload = (
    2.0 * PAYLOAD_RADIUS_M * required_grad_ln_a_per_m
)

# Minimal static soft-scalar potentials contain alpha^2 times an overall
# negative coefficient. This fixes the sign for all real alpha.
dbi_static_sign_invariant = True
sgal_static_sign_invariant = True

result = {
    "branch": "032K_032M_FRONTIER_ANALYTIC_GATES",
    "claim_class": "ANALYTIC_FRONTIER_FALSIFICATION",
    "energy_policy_id": str(policy["policy_id"]),
    "energy_comparison": str(policy["comparison"]),
    "energy_target_j": float(policy["limit_j"]),
    "payload_radius_m": PAYLOAD_RADIUS_M,
    "target_acceleration_mps2": A_TARGET,
    "required_grad_lnA_per_m_for_1g": required_grad_ln_a_per_m,
    "required_delta_lnA_across_payload_diameter": required_delta_ln_a_across_payload,
    "032K": {
        "mechanism": "KINETIC_CONFORMAL_GOLDSTONE_ULTRALOCAL_MATTER_BRANCH",
        "local_extended_gradient_repulsion_possible": True,
        "external_compact_source_fifth_force": 0.0,
        "true_standoff_external_source": False,
        "published_ultralocal_standoff_branch_closed": True,
        "full_nonultralocal_kinetic_conformal_class_closed": False,
        "reason": "FIFTH_FORCE_DEPENDS_ONLY_ON_LOCAL_DENSITY_AND_LOCAL_DENSITY_GRADIENT",
    },
    "032L": {
        "mechanism": "SOFT_DBI_MINIMAL_UNIVERSAL_STATIC_BRANCH",
        "leading_potential_power_r": -7,
        "leading_potential_sign": "NEGATIVE_ATTRACTIVE",
        "sign_depends_on_alpha_squared": dbi_static_sign_invariant,
        "static_minimal_branch_closed": True,
        "dynamic_branch_closed": False,
    },
    "032M": {
        "mechanism": "SPECIAL_GALILEON_MINIMAL_UNIVERSAL_STATIC_BRANCH",
        "leading_potential_power_r": -11,
        "leading_potential_sign": "NEGATIVE_ATTRACTIVE",
        "sign_depends_on_alpha_squared": sgal_static_sign_invariant,
        "static_minimal_branch_closed": True,
        "dynamic_branch_closed": False,
    },
    "old_014_disformal_reopened": False,
    "certified_sub10mj_model_found": False,
    "next": "032N_PROPAGATING_PROTECTED_DERIVATIVE_METRIC_PREFIELD",
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032K-032M FRONTIER ANALYTIC GATES ===")
print("ENERGY_TARGET_J="+format(float(policy["limit_j"]),".12e"))
print("ENERGY_COMPARISON="+str(policy["comparison"]))
print("REQUIRED_GRAD_LNA_PER_M="+format(required_grad_ln_a_per_m,".12e"))
print("REQUIRED_DELTA_LNA_ACROSS_20CM="+format(required_delta_ln_a_across_payload,".12e"))
print("032K_LOCAL_EXTENDED_REPULSION_POSSIBLE=True")
print("032K_EXTERNAL_STANDOFF_RESPONSE=ZERO_IN_PUBLISHED_ULTRALOCAL_BRANCH")
print("032K_PUBLISHED_ULTRALOCAL_STANDOFF_BRANCH=CLOSED")
print("032K_FULL_NONULTRALOCAL_CLASS_CLOSED=False")
print("032L_STATIC_SOFT_DBI_FORCE=ATTRACTIVE")
print("032L_STATIC_MINIMAL_BRANCH=CLOSED")
print("032L_DYNAMIC_BRANCH_CLOSED=False")
print("032M_STATIC_SPECIAL_GALILEON_FORCE=ATTRACTIVE")
print("032M_STATIC_MINIMAL_BRANCH=CLOSED")
print("032M_DYNAMIC_BRANCH_CLOSED=False")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=False")
print("NEXT=032N_PROPAGATING_PROTECTED_DERIVATIVE_METRIC_PREFIELD")
