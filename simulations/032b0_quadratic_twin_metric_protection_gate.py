"""
032B0 — Quadratic-twin pNGB metric-embedding pre-field gate.

Purpose
-------
Test only the structural protection idea and hard dimensional requirements.

This script does not solve field equations and does not establish a viable
antigravity source.

Working hypothesis
------------------
A pNGB coordinate theta is shared by a visible sector and a mirror twin
sector. Their leading quadratic threshold dependence is exchanged under
theta -> pi/2 - theta. The visible sector must couple universally through
one Jordan metric. All twin/source/control energy must enter the complete
operating ledger.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from antigravity_research.agminer.policy import current_energy_policy


HBAR_C_EV_M = 1.973269804e-7

MODEL031_ORACLE_J = 82.75e9
MODEL031_EDGE_J = 96.141e9
MODEL031_ACTIVATED_CONSERVATIVE_J = 127.7824385182716e9

theta, epsilon = sp.symbols("theta epsilon", real=True)

s2 = sp.sin(theta) ** 2
c2 = sp.cos(theta) ** 2

visible_threshold = 1 + epsilon * s2
twin_threshold = 1 + epsilon * c2

threshold_sum = sp.expand_trig(
    sp.simplify(visible_threshold + twin_threshold)
)

linear_theta_derivative = sp.simplify(
    sp.diff(threshold_sum, theta)
)

quadratic_loop_proxy = sp.expand(
    visible_threshold ** 2 + twin_threshold ** 2
)

series = sp.series(
    quadratic_loop_proxy,
    epsilon,
    0,
    3,
).removeO().expand()

order1 = sp.simplify(series.coeff(epsilon, 1))
order2 = sp.simplify(series.coeff(epsilon, 2))

order1_theta_derivative = sp.simplify(
    sp.diff(order1, theta)
)

order2_theta_derivative = sp.simplify(
    sp.diff(order2, theta)
)

leading_cancellation = (
    linear_theta_derivative == 0
    and order1_theta_derivative == 0
)

residual_starts_quadratic = order2_theta_derivative != 0

policy = current_energy_policy()
target_j = float(policy["limit_j"])

strict_sub_10_mj = (
    target_j == 1.0e7
    and str(policy["comparison"]) == "LT"
)

improvement_from_oracle = MODEL031_ORACLE_J / target_j
improvement_from_edge = MODEL031_EDGE_J / target_j
improvement_from_activated = (
    MODEL031_ACTIVATED_CONSERVATIVE_J / target_j
)

mass_1m_ev = HBAR_C_EV_M / 1.0
mass_3p3m_ev = HBAR_C_EV_M / 3.3

family_contract = {
    "family_id": "032B_QUADRATIC_TWIN_PNGB_METRIC",
    "family_version": "0_PRE_FIELD",
    "claim_class": "THEORY_DEFINITION_ONLY",
    "protection": "PNGB_PLUS_MIRROR_Z2_QUADRATIC_TWIN",
    "visible_payload_metric": "ONE_UNIVERSAL_JORDAN_METRIC_REQUIRED",
    "visible_metric_form": "gJ_vis = A_vis(theta)^2 gE",
    "twin_sector": "EXPLICIT_HIDDEN_MIRROR_SECTOR_REQUIRED",
    "spatially_prescribed_coupling": False,
    "spatially_prescribed_mass": False,
    "complete_energy_ledger": True,
    "twin_energy_counted": True,
    "source_energy_counted": True,
    "activation_energy_counted": True,
    "support_control_energy_counted": True,
    "negative_binding_can_game_objective": False,
    "field_solution_established": False,
    "finite_payload_repulsion_established": False,
    "stability_established": False,
    "empirical_consistency_established": False,
}

result = {
    "branch": "032B0",
    "family_contract": family_contract,
    "leading_order_twin_cancellation": bool(leading_cancellation),
    "residual_theta_dependence_at_order_epsilon_squared": bool(residual_starts_quadratic),
    "threshold_sum": str(sp.simplify(threshold_sum)),
    "order_epsilon_term": str(order1),
    "order_epsilon_squared_term": str(order2),
    "energy_policy_id": str(policy["policy_id"]),
    "energy_target_j": target_j,
    "strict_sub_10_mj": bool(strict_sub_10_mj),
    "031_oracle_energy_gap_x": improvement_from_oracle,
    "031_edge_energy_gap_x": improvement_from_edge,
    "031_activated_energy_gap_x": improvement_from_activated,
    "mediator_mass_for_1m_range_ev": mass_1m_ev,
    "mediator_mass_for_3p3m_range_ev": mass_3p3m_ev,
    "naturalness_problem_solved_for_complete_032b_theory": False,
    "metric_embedding_proven": False,
    "complete_032b_action_derived": False,
}

structural_green = (
    leading_cancellation
    and residual_starts_quadratic
    and strict_sub_10_mj
)

result["032B0_PROTECTION_STRUCTURE"] = (
    "GREEN_TO_EXACT_THEORY_DERIVATION"
    if structural_green
    else "RED"
)

output = Path(
    "results/data/032b0_quadratic_twin_metric_protection_summary.json"
)

output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032B0 QUADRATIC-TWIN pNGB PRE-FIELD GATE ===")
print("CLAIM_CLASS=THEORY_DEFINITION_ONLY")
print("REAL_FIELD_SOLUTION=NO")
print("ANTIGRAVITY_CANDIDATE_CERTIFIED=NO")
print("LEADING_O_EPSILON_TWIN_CANCELLATION=" + str(leading_cancellation))
print("RESIDUAL_STARTS_AT_O_EPSILON2=" + str(residual_starts_quadratic))
print("THRESHOLD_SUM=" + str(sp.simplify(threshold_sum)))
print("O_EPSILON_TERM=" + str(order1))
print("O_EPSILON2_TERM=" + str(order2))
print("ENERGY_TARGET_J=" + str(target_j))
print("STRICT_SUB_10_MJ=" + str(strict_sub_10_mj))
print("031_ORACLE_GAP_X=" + format(improvement_from_oracle, ".6f"))
print("031_EDGE_GAP_X=" + format(improvement_from_edge, ".6f"))
print("031_ACTIVATED_GAP_X=" + format(improvement_from_activated, ".6f"))
print("MASS_FOR_1M_RANGE_EV=" + format(mass_1m_ev, ".12e"))
print("MASS_FOR_3P3M_RANGE_EV=" + format(mass_3p3m_ev, ".12e"))
print("VISIBLE_PAYLOAD_METRIC=ONE_UNIVERSAL_JORDAN_METRIC_REQUIRED")
print("TWIN_SOURCE_CONTROL_ENERGY_MUST_BE_COUNTED=YES")
print("TWIN_PROTECTION_ALONE_SOLVES_ENERGY_GAP=NO")
print("032B0_PROTECTION_STRUCTURE=" + result["032B0_PROTECTION_STRUCTURE"])

if structural_green:
    print("NEXT=032B1_EXACT_METRIC_TWIN_ACTION_AND_ONE_LOOP_NATURALNESS_BOUND")
else:
    print("NEXT=REJECT_032B_BEFORE_FIELD_SOLVE")
