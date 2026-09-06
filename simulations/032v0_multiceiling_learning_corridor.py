"""
032V0 — feasibility-first multi-ceiling learning corridor.

Goals:

1. Preserve strict <10 MJ success policy unchanged.
2. Add non-success learning bands for 10-100 MJ and 100 MJ-1 GJ.
3. Replay known project controls.
4. Search the existing AGMINER SQLite database for energy-objective
   rejections lying inside the learning corridor.
5. Never convert a lower bound or prefield estimate into a certified model.
"""

from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path

from antigravity_research.agminer.learning import (
    BAND_ARCHIVE,
    BAND_MECHANISM,
    BAND_NEAR,
    BAND_TARGET,
    MECHANISM_CEILING_J,
    NEAR_MISS_CEILING_J,
    STRICT_TARGET_J,
    assess_energy,
)
from antigravity_research.agminer.policy import current_energy_policy


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "results" / "agminer" / "agminer.sqlite3"
OUT = ROOT / "results" / "data" / "032v0_multiceiling_learning_corridor_summary.json"
CSV_OUT = ROOT / "results" / "agminer" / "learning_corridor.csv"


policy = current_energy_policy()
policy_limit = float(policy["limit_j"])
policy_comparison = str(policy["comparison"])
policy_id = str(policy["policy_id"])

assert policy_limit == STRICT_TARGET_J
assert policy_comparison == "LT"


def assessment_dict(assessment):
    return {
        "energy_j": assessment.energy_j,
        "band": assessment.band,
        "target_factor": assessment.target_factor,
        "strict_energy_success": assessment.strict_energy_success,
        "certification_energy_eligible": assessment.certification_energy_eligible,
        "learning_priority": assessment.learning_priority,
        "proof_backed_floor_j": assessment.proof_backed_floor_j,
        "same_declared_branch_can_reach_target": assessment.same_declared_branch_can_reach_target,
        "removable_energy_above_floor_j": assessment.removable_energy_above_floor_j,
        "maximum_proven_reduction_factor": assessment.maximum_proven_reduction_factor,
    }


# ------------------------------------------------------------
# Historical controls.
# ------------------------------------------------------------

historical_specs = [
    {
        "name": "032N1_MINIMAL_GHOST_HALFSPACE_FLOOR",
        "energy_j": 53_240_466.87160,
        "proof_backed_floor_j": 53_240_466.87160,
        "status": "DECLARED_MINIMAL_BRANCH_CLOSED",
        "lesson": "ONLY_5P324X_FROM_TARGET_BUT_GEOMETRY_ONLY_RESCUE_CLOSED",
    },
    {
        "name": "032N0_UNIFORM_GHOST_CYLINDER_PREFIELD",
        "energy_j": 130_695_209.0,
        "proof_backed_floor_j": None,
        "status": "SUPERSEDED_BY_032N1_MORPHOLOGY_BOUND",
        "lesson": "RAW_CHARGE_ENERGY_SEPARATION_AND_2P45X_MORPHOLOGY_GAIN",
    },
    {
        "name": "031A_R4S_PRESCRIBED_ORACLE",
        "energy_j": 82_750_000_000.0,
        "proof_backed_floor_j": None,
        "status": "PRESCRIBED_SOURCE_NOT_MICROSCOPIC",
        "lesson": "SCALAR_METRIC_CHARGE_CAN_BE_LARGE_BUT_MICROSCOPIC_REALIZATION_COST_DOMINATES",
    },
    {
        "name": "031_QBALL_96GJ_HISTORICAL",
        "energy_j": 96_141_000_000.0,
        "proof_backed_floor_j": None,
        "status": "031_FAMILY_LATER_CLOSED_BY_RADIATIVE_NATURALNESS",
        "lesson": "FIELD_AND_STABILITY_DO_NOT_IMPLY_NATURAL_UV_COMPLETION",
    },
]

historical = []

for spec in historical_specs:
    a = assess_energy(
        spec["energy_j"],
        proof_backed_floor_j=spec["proof_backed_floor_j"],
    )
    row = dict(spec)
    row["assessment"] = assessment_dict(a)
    historical.append(row)

assert historical[0]["assessment"]["band"] == BAND_NEAR
assert historical[0]["assessment"]["target_factor"] > 5.32
assert historical[0]["assessment"]["target_factor"] < 5.33
assert historical[0]["assessment"]["same_declared_branch_can_reach_target"] is False

assert historical[1]["assessment"]["band"] == BAND_MECHANISM
assert historical[2]["assessment"]["band"] == BAND_ARCHIVE
assert historical[3]["assessment"]["band"] == BAND_ARCHIVE

# ------------------------------------------------------------
# Scan existing AGMINER energy-objective rejects.
# ------------------------------------------------------------

db_rows = []
db_counts = {
    BAND_NEAR: 0,
    BAND_MECHANISM: 0,
    BAND_ARCHIVE: 0,
}

current_energy_state = "REJECTED_ENERGY_OBJECTIVE:" + policy_id

if DB.exists():
    uri = "file:" + str(DB) + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row

    columns = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(models)").fetchall()
    }

    required = {"candidate_id", "family", "state", "energy_j"}

    if not required.issubset(columns):
        missing = sorted(required - columns)
        raise RuntimeError("models table missing columns: " + str(missing))

    optional = []
    for name in ("version", "family_version", "params_json", "params_json_compact"):
        if name in columns:
            optional.append(name)

    select_columns = [
        "candidate_id",
        "family",
        "state",
        "energy_j",
    ] + optional

    sql = (
        "SELECT "
        + ",".join(select_columns)
        + " FROM models "
        + "WHERE state=? AND energy_j IS NOT NULL AND energy_j>=? "
        + "ORDER BY energy_j ASC"
    )

    raw = conn.execute(
        sql,
        (current_energy_state, STRICT_TARGET_J),
    ).fetchall()

    for r in raw:
        energy = float(r["energy_j"])
        a = assess_energy(energy)

        if a.band == BAND_TARGET:
            continue

        db_counts[a.band] = db_counts.get(a.band, 0) + 1

        if a.band not in (BAND_NEAR, BAND_MECHANISM):
            continue

        item = {
            "candidate_id": str(r["candidate_id"]),
            "family": str(r["family"]),
            "state": str(r["state"]),
            "energy_j": energy,
            "energy_mj": energy / 1.0e6,
            "target_factor": a.target_factor,
            "band": a.band,
            "learning_priority": a.learning_priority,
            "energy_semantics": "AGMINER_STORED_ENERGY_AT_OBJECTIVE_REJECTION",
            "certified_model": False,
        }

        for name in optional:
            value = r[name]
            if value is not None:
                item[name] = str(value)

        db_rows.append(item)

    conn.close()

# Retain only the best compact learning set.
db_rows.sort(key=lambda row: (row["energy_j"], row["family"], row["candidate_id"]))
top_db_rows = db_rows[:250]

# ------------------------------------------------------------
# Family-level closest near misses.
# ------------------------------------------------------------

family_best = {}

for row in db_rows:
    family = row["family"]
    previous = family_best.get(family)
    if previous is None or row["energy_j"] < previous["energy_j"]:
        family_best[family] = row

family_best_rows = sorted(
    family_best.values(),
    key=lambda row: row["energy_j"],
)

# ------------------------------------------------------------
# Compact CSV, overwritten each run.
# ------------------------------------------------------------

CSV_OUT.parent.mkdir(parents=True, exist_ok=True)

fieldnames = [
    "candidate_id",
    "family",
    "state",
    "energy_j",
    "energy_mj",
    "target_factor",
    "band",
    "learning_priority",
    "energy_semantics",
    "certified_model",
]

with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(top_db_rows)

# ------------------------------------------------------------
# Decide next strategy.
# ------------------------------------------------------------

near_count = db_counts.get(BAND_NEAR, 0)
mechanism_count = db_counts.get(BAND_MECHANISM, 0)

if near_count > 0:
    next_step = "032V1_RECONSTRUCT_AND_DECOMPOSE_CLOSEST_10_TO_100MJ_DB_NEAR_MISSES"
elif mechanism_count > 0:
    next_step = "032V1_DECOMPOSE_100MJ_TO_1GJ_MECHANISM_LEADERS_THEN_GENERATE_NEAR_MISS_ACTIONS"
else:
    next_step = "032V1_FEASIBILITY_FIRST_PHYSICAL_ACTION_TEMPLATE_GENERATOR"

result = {
    "branch": "032V0_FEASIBILITY_FIRST_MULTI_CEILING_LEARNING",
    "claim_class": "SEARCH_STRATEGY_AND_KNOWLEDGE_RETENTION_INFRASTRUCTURE",
    "strict_policy": {
        "policy_id": policy_id,
        "comparison": policy_comparison,
        "target_j": policy_limit,
        "changed": False,
        "exact_10mj_is_success": False,
    },
    "learning_bands": {
        BAND_TARGET: {
            "lower_j": 0.0,
            "upper_j": STRICT_TARGET_J,
            "upper_inclusive": False,
            "certification_energy_eligible": True,
        },
        BAND_NEAR: {
            "lower_j": STRICT_TARGET_J,
            "upper_j": NEAR_MISS_CEILING_J,
            "lower_inclusive": True,
            "upper_inclusive": False,
            "certification_energy_eligible": False,
        },
        BAND_MECHANISM: {
            "lower_j": NEAR_MISS_CEILING_J,
            "upper_j": MECHANISM_CEILING_J,
            "lower_inclusive": True,
            "upper_inclusive": True,
            "certification_energy_eligible": False,
        },
        BAND_ARCHIVE: {
            "lower_j": MECHANISM_CEILING_J,
            "lower_exclusive": True,
            "certification_energy_eligible": False,
        },
    },
    "historical_controls": historical,
    "database": {
        "path": str(DB.relative_to(ROOT)),
        "current_energy_objective_state": current_energy_state,
        "band_counts": db_counts,
        "learning_rows_total": len(db_rows),
        "learning_rows_retained_csv": len(top_db_rows),
        "family_best_count": len(family_best_rows),
        "family_best": family_best_rows[:50],
    },
    "rules": {
        "higher_energy_learning_case_is_success": False,
        "higher_energy_learning_case_is_certification_ready": False,
        "proof_backed_reducibility_required_for_target_reachability_claim": True,
        "optimization_alone_does_not_establish_removability": True,
        "closed_or_superseded_model_can_still_supply_transferable_lesson": True,
        "closed_or_superseded_model_is_not_reopened_by_learning_status": True,
    },
    "next": next_step,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032V0 RESULT ===")
print("STRICT_POLICY_ID=" + policy_id)
print("STRICT_TARGET_J=" + format(policy_limit, ".12e"))
print("STRICT_COMPARISON=" + policy_comparison)
print("STRICT_POLICY_CHANGED=False")
print("EXACT_10MJ_IS_SUCCESS=False")

print("HISTORICAL_032N1_BAND=" + historical[0]["assessment"]["band"])
print("HISTORICAL_032N1_TARGET_FACTOR=" + format(historical[0]["assessment"]["target_factor"], ".12e"))
print("HISTORICAL_032N1_SAME_BRANCH_TARGET_REACHABLE=" + str(historical[0]["assessment"]["same_declared_branch_can_reach_target"]))

print("HISTORICAL_032N0_BAND=" + historical[1]["assessment"]["band"])
print("HISTORICAL_032N0_TARGET_FACTOR=" + format(historical[1]["assessment"]["target_factor"], ".12e"))

print("DB_NEAR_MISS_COUNT=" + str(near_count))
print("DB_MECHANISM_COUNT=" + str(mechanism_count))
print("DB_ARCHIVE_ENERGY_REJECT_COUNT=" + str(db_counts.get(BAND_ARCHIVE, 0)))
print("DB_LEARNING_ROWS_TOTAL=" + str(len(db_rows)))
print("DB_FAMILY_BEST_COUNT=" + str(len(family_best_rows)))

if family_best_rows:
    best = family_best_rows[0]
    print("DB_CLOSEST_FAMILY=" + best["family"])
    print("DB_CLOSEST_ENERGY_MJ=" + format(best["energy_mj"], ".12e"))
    print("DB_CLOSEST_TARGET_FACTOR=" + format(best["target_factor"], ".12e"))
    print("DB_CLOSEST_BAND=" + best["band"])
else:
    print("DB_CLOSEST_FAMILY=NONE")

print("HIGHER_ENERGY_LEARNING_IS_SUCCESS=False")
print("CLOSED_MODELS_REOPENED=False")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=NO")
print("NEXT=" + next_step)
