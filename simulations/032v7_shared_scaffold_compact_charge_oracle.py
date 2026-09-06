"""032V7 shared-scaffold compact-charge oracle."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.policy import current_energy_policy
from antigravity_research.agminer.reporting import rebuild_summaries
from antigravity_research.agminer.storage import Storage
from antigravity_research.agminer.families.family_032v7_cpn_shared_scaffold_source import (
    SharedScaffoldCPNSourceFamily,
    required_exponent_advantage,
)


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "results" / "agminer" / "agminer.sqlite3"
OUT = ROOT / "results" / "data" / "032v7_shared_scaffold_compact_charge_summary.json"
CSV_OUT = ROOT / "results" / "data" / "032v7_shared_scaffold_gain_requirements.csv"
V4 = ROOT / "results" / "data" / "032v4_ghost_condensate_effective_charge_normalization_summary.json"

STRICT_TARGET_J = 1.0e7
STRETCH_TARGET_J = 1.0e6

policy = current_energy_policy()
assert float(policy["limit_j"]) == STRICT_TARGET_J
assert str(policy["comparison"]) == "LT"

if not V4.exists():
    raise FileNotFoundError(str(V4))

v4 = json.loads(V4.read_text(encoding="utf-8"))

CANONICAL_REFERENCE_J = float(
    v4["canonical_minimal_branch"]["minimum_optimistic_floor_j"]
)

GAIN_10MJ = CANONICAL_REFERENCE_J / STRICT_TARGET_J
GAIN_1MJ = CANONICAL_REFERENCE_J / STRETCH_TARGET_J

family = SharedScaffoldCPNSourceFamily()

params = {
    "source_architecture": "MULTICOMPONENT_CP_N_COMPACT_SHARED_SCAFFOLD",
    "energy_exponent": family.energy_exponent,
    "conditional_response_exponent": family.conditional_response_exponent,
    "gravitational_portal": "NOT_ESTABLISHED",
}

candidate = Candidate(
    family_id=family.family_id,
    family_version=family.family_version,
    params=params,
    physical_model_version="SOURCE_ORACLE_ONLY_NO_PHYSICAL_METRIC_PORTAL",
    energy_ledger_version="SOURCE_SCALING_ONLY_V1",
)

oracle = family.action_oracle(params, {})
scaling = family.collective_scaling_probe(params, {})

assert scaling.beneficial_collective_scaling is True
assert oracle.trusted_for_reachability is False

Q_REQUIRED_10MJ = family.required_charge_scale(GAIN_10MJ)
Q_REQUIRED_1MJ = family.required_charge_scale(GAIN_1MJ)

dynamic_ranges = [
    1.0e3,
    1.0e6,
    1.0e9,
    1.0e12,
    1.0e15,
    1.0e18,
]

rows = []

for scale in dynamic_ranges:
    gain = family.efficiency_gain(scale)
    rows.append({
        "charge_dynamic_range": scale,
        "efficiency_gain_at_alpha_5_over_6": gain,
        "enough_for_10mj_gap": gain >= GAIN_10MJ,
        "enough_for_1mj_gap": gain >= GAIN_1MJ,
        "required_delta_for_10mj": required_exponent_advantage(GAIN_10MJ, scale),
        "required_delta_for_1mj": required_exponent_advantage(GAIN_1MJ, scale),
        "cpn_delta": family.efficiency_exponent,
    })

storage = Storage(DB)

storage.record_candidate(
    candidate,
    state="SOURCE_ORACLE_ONLY_UNTRUSTED_FOR_ANTIGRAVITY",
    tier=0,
    run_id="032V7",
)

storage.record_action_oracle(
    candidate.candidate_id,
    oracle,
)

storage.record_collective_scaling(
    family=family.family_id,
    family_version=family.family_version,
    probe_id="NOETHER_Q_SHARED_SCAFFOLD_CONDITIONAL_LINEAR_RESPONSE",
    assessment=scaling,
    proof_reference=family.proof_reference,
)

summary_reporting = rebuild_summaries(
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

oracle_row = oracle_rows[0]
scaling_row = scaling_rows[0]

assert oracle_row["trusted_for_reachability"] == 0
assert oracle_row["priority"] == "ORACLE_PROVENANCE_INCOMPLETE"
assert scaling_row["beneficial_collective_scaling"] == 1

storage.close()

CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

delta_10_at_1e12 = required_exponent_advantage(GAIN_10MJ, 1.0e12)
delta_1_at_1e12 = required_exponent_advantage(GAIN_1MJ, 1.0e12)

gain_at_1e12 = family.efficiency_gain(1.0e12)

cpn_alone_10mj_with_q_le_1e12 = gain_at_1e12 >= GAIN_10MJ
cpn_alone_1mj_with_q_le_1e12 = gain_at_1e12 >= GAIN_1MJ

decision = "GREEN_SHARED_SCAFFOLD_SCALING_REAL_BUT_TOO_WEAK_ALONE_AT_1E12_Q_RANGE"
next_step = "032V8_COOPERATIVE_CHARGE_PLUS_SHARED_SCAFFOLD_ACTION_PREFLIGHT"

result = {
    "branch": "032V7_SHARED_SCAFFOLD_COMPACT_CHARGE_ORACLE",
    "claim_class": "SOURCE_SIDE_ACTION_SCALING_ORACLE_NOT_ANTIGRAVITY_MODEL",
    "strict_target_j": STRICT_TARGET_J,
    "stretch_target_j": STRETCH_TARGET_J,
    "canonical_reference_j": CANONICAL_REFERENCE_J,
    "gain_required_10mj": GAIN_10MJ,
    "gain_required_1mj": GAIN_1MJ,
    "source_family": {
        "family_id": family.family_id,
        "canonical_invariant_id": oracle.canonical_invariant_id,
        "energy_exponent": family.energy_exponent,
        "conditional_response_exponent": family.conditional_response_exponent,
        "efficiency_exponent": family.efficiency_exponent,
        "normalization_invariant": oracle.normalization_invariant,
        "naturalness_screened": oracle.naturalness_screened,
        "universal_metric_screened": oracle.universal_metric_screened,
        "trusted_for_reachability": oracle.trusted_for_reachability,
    },
    "scaling": {
        "response_exponent": scaling.response_exponent,
        "energy_exponent": scaling.energy_exponent,
        "efficiency_exponent": scaling.efficiency_exponent,
        "beneficial_collective_scaling": scaling.beneficial_collective_scaling,
        "required_charge_scale_10mj": Q_REQUIRED_10MJ,
        "required_charge_scale_1mj": Q_REQUIRED_1MJ,
        "gain_at_charge_scale_1e12": gain_at_1e12,
        "required_delta_10mj_at_1e12": delta_10_at_1e12,
        "required_delta_1mj_at_1e12": delta_1_at_1e12,
    },
    "declared_dynamic_range_probe": {
        "charge_scale_limit": 1.0e12,
        "cpn_alone_10mj": cpn_alone_10mj_with_q_le_1e12,
        "cpn_alone_1mj": cpn_alone_1mj_with_q_le_1e12,
        "this_is_a_theorem_beyond_declared_range": False,
    },
    "reporting": summary_reporting,
    "mechanism_metrics_recorded": False,
    "reason_mechanism_metrics_absent": "NO_PHYSICAL_METRIC_GRAVITATIONAL_RESPONSE_ESTABLISHED",
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

print("=== 032V7 RESULT ===")
print("CANONICAL_REFERENCE_GJ=" + format(CANONICAL_REFERENCE_J/1e9, ".12e"))
print("GAIN_REQUIRED_10MJ=" + format(GAIN_10MJ, ".12e"))
print("GAIN_REQUIRED_1MJ=" + format(GAIN_1MJ, ".12e"))

print("CPN_ENERGY_EXPONENT=" + format(family.energy_exponent, ".12e"))
print("CONDITIONAL_RESPONSE_EXPONENT=" + format(family.conditional_response_exponent, ".12e"))
print("EFFICIENCY_EXPONENT=" + format(family.efficiency_exponent, ".12e"))

print("Q_SCALE_REQUIRED_10MJ=" + format(Q_REQUIRED_10MJ, ".12e"))
print("Q_SCALE_REQUIRED_1MJ=" + format(Q_REQUIRED_1MJ, ".12e"))

print("GAIN_AT_Q_SCALE_1E12=" + format(gain_at_1e12, ".12e"))
print("DELTA_REQUIRED_10MJ_AT_1E12=" + format(delta_10_at_1e12, ".12e"))
print("DELTA_REQUIRED_1MJ_AT_1E12=" + format(delta_1_at_1e12, ".12e"))

print("COLLECTIVE_SCALING_BENEFICIAL=" + str(scaling.beneficial_collective_scaling))
print("ORACLE_TRUSTED_FOR_ANTIGRAVITY_REACHABILITY=" + str(oracle.trusted_for_reachability))
print("MECHANISM_METRICS_RECORDED=False")
print("PHYSICAL_ANTIGRAVITY_MODEL_FOUND=NO")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=NO")
print("DECISION=" + decision)
print("NEXT=" + next_step)
