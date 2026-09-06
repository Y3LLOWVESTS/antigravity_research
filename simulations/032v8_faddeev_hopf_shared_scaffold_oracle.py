"""032V8 Faddeev-Hopf shared-scaffold source oracle."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.policy import current_energy_policy
from antigravity_research.agminer.reporting import rebuild_summaries
from antigravity_research.agminer.storage import Storage
from antigravity_research.agminer.families.family_032v8_faddeev_hopf_shared_scaffold import (
    FaddeevHopfSharedScaffoldFamily,
    conditional_reference_equivalent_energy,
)


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "results" / "agminer" / "agminer.sqlite3"
OUT = ROOT / "results" / "data" / "032v8_faddeev_hopf_shared_scaffold_summary.json"
CSV_OUT = ROOT / "results" / "data" / "032v8_faddeev_hopf_scaling_requirements.csv"
V4 = ROOT / "results" / "data" / "032v4_ghost_condensate_effective_charge_normalization_summary.json"
V7 = ROOT / "results" / "data" / "032v7_shared_scaffold_compact_charge_summary.json"

STRICT_TARGET_J = 1.0e7
STRETCH_TARGET_J = 1.0e6

policy = current_energy_policy()
assert float(policy["limit_j"]) == STRICT_TARGET_J
assert str(policy["comparison"]) == "LT"

for path in (V4, V7):
    if not path.exists():
        raise FileNotFoundError(str(path))

v4 = json.loads(V4.read_text(encoding="utf-8"))
v7 = json.loads(V7.read_text(encoding="utf-8"))

CANONICAL_REFERENCE_J = float(
    v4["canonical_minimal_branch"]["minimum_optimistic_floor_j"]
)

GAIN_REQUIRED_10MJ = CANONICAL_REFERENCE_J / STRICT_TARGET_J
GAIN_REQUIRED_1MJ = CANONICAL_REFERENCE_J / STRETCH_TARGET_J

V7_DELTA = float(v7["source_family"]["efficiency_exponent"])
V7_GAIN_1E12 = float(v7["scaling"]["gain_at_charge_scale_1e12"])

assert abs(V7_DELTA - 1.0/6.0) < 1e-12
assert abs(V7_GAIN_1E12 - 100.0) < 1e-9

family = FaddeevHopfSharedScaffoldFamily()

params = {
    "source_architecture": "FADDEEV_SKYRME_HOPF_SHARED_SCAFFOLD",
    "energy_exponent": family.energy_exponent,
    "conditional_response_exponent": family.conditional_response_exponent,
    "gravitational_portal": "NOT_ESTABLISHED",
    "large_q_realization": "NOT_CERTIFIED",
}

candidate = Candidate(
    family_id=family.family_id,
    family_version=family.family_version,
    params=params,
    physical_model_version="SOURCE_ORACLE_ONLY_NO_METRIC_PORTAL",
    energy_ledger_version="TOPOLOGICAL_SCALING_ONLY_V1",
)

oracle = family.action_oracle(params, {})
scaling = family.collective_scaling_probe(params, {})

assert scaling.beneficial_collective_scaling is True
assert oracle.trusted_for_reachability is False

Q_REQUIRED_10MJ = family.required_charge_scale(GAIN_REQUIRED_10MJ)
Q_REQUIRED_1MJ = family.required_charge_scale(GAIN_REQUIRED_1MJ)

dynamic_ranges = [
    1.0e6,
    1.0e9,
    1.0e12,
    1.0e15,
    1.0e18,
]

rows = []

for qscale in dynamic_ranges:
    gain = family.efficiency_gain(qscale)
    equiv_j = conditional_reference_equivalent_energy(
        CANONICAL_REFERENCE_J,
        qscale,
    )

    rows.append({
        "hopf_charge_dynamic_range": qscale,
        "conditional_source_efficiency_gain": gain,
        "conditional_reference_equivalent_energy_j": equiv_j,
        "conditional_reference_equivalent_energy_mj": equiv_j/1.0e6,
        "remaining_gain_for_10mj": GAIN_REQUIRED_10MJ/gain,
        "remaining_gain_for_1mj": GAIN_REQUIRED_1MJ/gain,
        "max_total_tax_to_stay_under_10mj": STRICT_TARGET_J/equiv_j,
        "max_total_tax_to_stay_under_1mj": STRETCH_TARGET_J/equiv_j,
        "conditional_10mj_crossed_before_tax": equiv_j < STRICT_TARGET_J,
        "conditional_1mj_crossed_before_tax": equiv_j < STRETCH_TARGET_J,
        "physical_energy_prediction": False,
    })

GAIN_1E12 = family.efficiency_gain(1.0e12)
EQUIV_1E12_J = conditional_reference_equivalent_energy(
    CANONICAL_REFERENCE_J,
    1.0e12,
)

GAIN_1E15 = family.efficiency_gain(1.0e15)
EQUIV_1E15_J = conditional_reference_equivalent_energy(
    CANONICAL_REFERENCE_J,
    1.0e15,
)

GAIN_1E18 = family.efficiency_gain(1.0e18)
EQUIV_1E18_J = conditional_reference_equivalent_energy(
    CANONICAL_REFERENCE_J,
    1.0e18,
)

V8_OVER_V7_GAIN_AT_1E12 = GAIN_1E12 / V7_GAIN_1E12

storage = Storage(DB)

storage.record_candidate(
    candidate,
    state="SOURCE_ORACLE_ONLY_UNTRUSTED_FOR_ANTIGRAVITY",
    tier=0,
    run_id="032V8",
)

storage.record_action_oracle(
    candidate.candidate_id,
    oracle,
)

storage.record_collective_scaling(
    family=family.family_id,
    family_version=family.family_version,
    probe_id="HOPF_Q_SHARED_SCAFFOLD_CONDITIONAL_LINEAR_RESPONSE",
    assessment=scaling,
    proof_reference=family.proof_reference,
)

reporting = rebuild_summaries(
    storage,
    ROOT / "results" / "agminer",
)

oracle_rows = [
    row for row in storage.oracle_rows()
    if row["candidate_id"] == candidate.candidate_id
]

scaling_rows = [
    row for row in storage.collective_scaling_rows()
    if row["family"] == family.family_id
]

mechanism_rows = [
    row for row in storage.mechanism_rows()
    if row["family"] == family.family_id
]

assert len(oracle_rows) == 1
assert len(scaling_rows) == 1
assert len(mechanism_rows) == 0

assert oracle_rows[0]["trusted_for_reachability"] == 0
assert scaling_rows[0]["beneficial_collective_scaling"] == 1

storage.close()

CSV_OUT.parent.mkdir(parents=True, exist_ok=True)

with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(rows[0].keys()),
    )
    writer.writeheader()
    writer.writerows(rows)

decision = (
    "GREEN_HOPF_Q3OVER4_SOURCE_SCALING_STRONG_ENOUGH_CONDITIONALLY"
)

next_step = (
    "032V9_TOPOLOGICAL_CHARGE_TO_UNIVERSAL_METRIC_PORTAL_PREFLIGHT"
)

result = {
    "branch": "032V8_FADDEEV_HOPF_SHARED_SCAFFOLD_ORACLE",
    "claim_class": "SOURCE_SCALING_ORACLE_NOT_PHYSICAL_ANTIGRAVITY_MODEL",
    "strict_target_j": STRICT_TARGET_J,
    "stretch_target_j": STRETCH_TARGET_J,
    "canonical_reference_j": CANONICAL_REFERENCE_J,
    "gain_required_10mj": GAIN_REQUIRED_10MJ,
    "gain_required_1mj": GAIN_REQUIRED_1MJ,
    "source_family": {
        "family_id": family.family_id,
        "energy_exponent": family.energy_exponent,
        "conditional_response_exponent": family.conditional_response_exponent,
        "efficiency_exponent": family.efficiency_exponent,
        "normalization_invariant_scaling": oracle.normalization_invariant,
        "universal_metric_screened": oracle.universal_metric_screened,
        "naturalness_screened": oracle.naturalness_screened,
        "trusted_for_reachability": oracle.trusted_for_reachability,
        "large_q_realization_certified": False,
    },
    "scaling": {
        "response_exponent": scaling.response_exponent,
        "energy_exponent": scaling.energy_exponent,
        "efficiency_exponent": scaling.efficiency_exponent,
        "beneficial_collective_scaling": scaling.beneficial_collective_scaling,
        "q_required_10mj": Q_REQUIRED_10MJ,
        "q_required_1mj": Q_REQUIRED_1MJ,
        "gain_at_q_1e12": GAIN_1E12,
        "gain_at_q_1e15": GAIN_1E15,
        "gain_at_q_1e18": GAIN_1E18,
        "v8_over_v7_gain_at_q_1e12": V8_OVER_V7_GAIN_AT_1E12,
    },
    "conditional_design_translation": {
        "q_1e12_equivalent_j": EQUIV_1E12_J,
        "q_1e12_equivalent_mj": EQUIV_1E12_J/1.0e6,
        "q_1e12_max_tax_to_10mj": STRICT_TARGET_J/EQUIV_1E12_J,
        "q_1e15_equivalent_j": EQUIV_1E15_J,
        "q_1e15_equivalent_mj": EQUIV_1E15_J/1.0e6,
        "q_1e15_max_tax_to_10mj": STRICT_TARGET_J/EQUIV_1E15_J,
        "q_1e15_max_tax_to_1mj": STRETCH_TARGET_J/EQUIV_1E15_J,
        "q_1e18_equivalent_j": EQUIV_1E18_J,
        "q_1e18_equivalent_mj": EQUIV_1E18_J/1.0e6,
        "physical_energy_prediction": False,
        "cross_theory_certification_claim": False,
    },
    "portal": {
        "hopf_charge_to_gravitational_charge_established": False,
        "universal_physical_metric_established": False,
        "finite_payload_outward_response_established": False,
        "reciprocity_established": False,
        "naturalness_established": False,
    },
    "reporting": reporting,
    "mechanism_metrics_recorded": False,
    "reason_mechanism_metrics_absent": "NO_PHYSICAL_METRIC_RESPONSE_EXISTS_YET",
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

print("=== 032V8 RESULT ===")
print("CANONICAL_REFERENCE_GJ=" + format(CANONICAL_REFERENCE_J/1e9, ".12e"))
print("GAIN_REQUIRED_10MJ=" + format(GAIN_REQUIRED_10MJ, ".12e"))
print("GAIN_REQUIRED_1MJ=" + format(GAIN_REQUIRED_1MJ, ".12e"))

print("HOPF_ENERGY_EXPONENT=" + format(family.energy_exponent, ".12e"))
print("CONDITIONAL_RESPONSE_EXPONENT=" + format(family.conditional_response_exponent, ".12e"))
print("HOPF_EFFICIENCY_EXPONENT=" + format(family.efficiency_exponent, ".12e"))

print("Q_REQUIRED_10MJ=" + format(Q_REQUIRED_10MJ, ".12e"))
print("Q_REQUIRED_1MJ=" + format(Q_REQUIRED_1MJ, ".12e"))

print("GAIN_Q1E12=" + format(GAIN_1E12, ".12e"))
print("V8_OVER_V7_GAIN_Q1E12=" + format(V8_OVER_V7_GAIN_AT_1E12, ".12e"))
print("Q1E12_REFERENCE_EQUIV_MJ=" + format(EQUIV_1E12_J/1e6, ".12e"))
print("Q1E12_MAX_TAX_TO_10MJ=" + format(STRICT_TARGET_J/EQUIV_1E12_J, ".12e"))

print("GAIN_Q1E15=" + format(GAIN_1E15, ".12e"))
print("Q1E15_REFERENCE_EQUIV_MJ=" + format(EQUIV_1E15_J/1e6, ".12e"))
print("Q1E15_MAX_TAX_TO_10MJ=" + format(STRICT_TARGET_J/EQUIV_1E15_J, ".12e"))
print("Q1E15_MAX_TAX_TO_1MJ=" + format(STRETCH_TARGET_J/EQUIV_1E15_J, ".12e"))

print("GAIN_Q1E18=" + format(GAIN_1E18, ".12e"))
print("Q1E18_REFERENCE_EQUIV_MJ=" + format(EQUIV_1E18_J/1e6, ".12e"))

print("REFERENCE_EQUIVALENT_IS_PHYSICAL_ENERGY=False")
print("HOPF_TO_METRIC_PORTAL_ESTABLISHED=False")
print("LARGE_Q_REALIZATION_CERTIFIED=False")
print("MECHANISM_METRICS_RECORDED=False")
print("PHYSICAL_ANTIGRAVITY_MODEL_FOUND=NO")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=NO")
print("DECISION=" + decision)
print("NEXT=" + next_step)
