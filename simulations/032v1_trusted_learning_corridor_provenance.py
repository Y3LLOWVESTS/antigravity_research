"""
032V1 — trusted learning corridor.

This run separates:

  raw stored near misses,
  superseded quantitative rows,
  current trusted active learning candidates,
  verified historical controls.

No row is deleted from SQLite.
No closed family is reopened.
The strict <10 MJ objective remains unchanged.
"""

from __future__ import annotations

import csv
import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

from antigravity_research.agminer.learning import (
    BAND_ARCHIVE,
    BAND_MECHANISM,
    BAND_NEAR,
    BAND_TARGET,
    STRICT_TARGET_J,
    assess_energy,
)
from antigravity_research.agminer.learning_provenance import (
    PROVENANCE_SUPERSEDED,
    assess_family_provenance,
)
from antigravity_research.agminer.policy import current_energy_policy


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "results" / "agminer" / "agminer.sqlite3"
RAW_CSV = ROOT / "results" / "agminer" / "learning_corridor.csv"
TRUSTED_CSV = ROOT / "results" / "agminer" / "trusted_learning_corridor.csv"
HISTORY_CSV = ROOT / "results" / "agminer" / "trusted_learning_controls.csv"
OUT = ROOT / "results" / "data" / "032v1_trusted_learning_corridor_summary.json"


policy = current_energy_policy()
assert float(policy["limit_j"]) == 10_000_000.0
assert str(policy["comparison"]) == "LT"


# ------------------------------------------------------------
# 1. Inspect V0 compact CSV.
# ------------------------------------------------------------

raw_csv_rows = []

if RAW_CSV.exists():
    with RAW_CSV.open("r", encoding="utf-8", newline="") as handle:
        raw_csv_rows = list(csv.DictReader(handle))

csv_family_counts = Counter(
    row["family"] for row in raw_csv_rows
)

csv_superseded = 0
csv_current = 0

for row in raw_csv_rows:
    p = assess_family_provenance(row["family"])
    if p.status == PROVENANCE_SUPERSEDED:
        csv_superseded += 1
    else:
        csv_current += 1

# ------------------------------------------------------------
# 2. Reconstruct the full database learning corridor.
# ------------------------------------------------------------

raw_db_rows = []
trusted_active_rows = []
superseded_rows = []

state = "REJECTED_ENERGY_OBJECTIVE:" + str(policy["policy_id"])

if not DB.exists():
    raise FileNotFoundError(str(DB))

uri = "file:" + str(DB) + "?mode=ro"
conn = sqlite3.connect(uri, uri=True)
conn.row_factory = sqlite3.Row

columns = {
    row["name"]
    for row in conn.execute("PRAGMA table_info(models)").fetchall()
}

needed = {"candidate_id", "family", "state", "energy_j"}
if not needed.issubset(columns):
    raise RuntimeError(
        "missing models columns: " + str(sorted(needed - columns))
    )

optional = [
    name for name in (
        "version",
        "family_version",
        "params_json",
        "params_json_compact",
    )
    if name in columns
]

select = [
    "candidate_id",
    "family",
    "state",
    "energy_j",
] + optional

sql = (
    "SELECT "
    + ",".join(select)
    + " FROM models "
    + "WHERE state=? AND energy_j IS NOT NULL "
    + "AND energy_j>=? AND energy_j<=? "
    + "ORDER BY energy_j ASC"
)

rows = conn.execute(
    sql,
    (state, STRICT_TARGET_J, 1.0e9),
).fetchall()

for r in rows:
    energy = float(r["energy_j"])
    family = str(r["family"])
    a = assess_energy(energy)
    p = assess_family_provenance(family)

    item = {
        "candidate_id": str(r["candidate_id"]),
        "family": family,
        "energy_j": energy,
        "energy_mj": energy/1.0e6,
        "target_factor": a.target_factor,
        "band": a.band,
        "provenance": p.status,
        "provenance_reason": p.reason,
        "replacement_program": p.replacement_program or "",
        "active_learning_eligible": p.usable_for_active_energy_ranking,
        "certified_model": False,
    }

    for name in optional:
        value = r[name]
        if value is not None:
            item[name] = str(value)

    raw_db_rows.append(item)

    if p.usable_for_active_energy_ranking:
        trusted_active_rows.append(item)
    else:
        superseded_rows.append(item)

conn.close()

# ------------------------------------------------------------
# 3. Historical verified controls.
# ------------------------------------------------------------

# These are learning controls, not active candidates.
# Their values come from completed project runs.

historical_specs = [
    {
        "name": "032N1_GHOST_CONDENSATE_CONTINUUM_FLOOR",
        "energy_j": 53_240_466.87159985,
        "status": "VERIFIED_NEAR_MISS_DECLARED_BRANCH_CLOSED",
        "active_candidate": False,
        "reopen": False,
        "lesson": "MORPHOLOGY_GAIN_2P4548X_BUT_GEOMETRY_ONLY_RESCUE_CLOSED",
    },
    {
        "name": "032N0_GHOST_CONDENSATE_UNIFORM_PREFIELD",
        "energy_j": 130_695_209.44851829,
        "status": "VERIFIED_MECHANISM_CONTROL_SUPERSEDED_BY_032N1_BOUND",
        "active_candidate": False,
        "reopen": False,
        "lesson": "RAW_CHARGE_ENERGY_SEPARATION_PRESENT",
    },
    {
        "name": "032H_SOURCE_AWARE_DBI_50M_BEST",
        "energy_j": 1_920_927_824_985.0078,
        "status": "CORRECTED_SOURCE_AWARE_QUANTITATIVE_CONTROL",
        "active_candidate": False,
        "reopen": False,
        "lesson": "PRELIMINARY_032C_032E_LOW_ENERGIES_DO_NOT_SURVIVE_SOURCE_AWARE_LEDGER",
    },
    {
        "name": "032G_SOURCE_AWARE_CANONICAL_50M_BEST",
        "energy_j": 9.369541760768323e25,
        "status": "CORRECTED_SOURCE_AWARE_QUANTITATIVE_CONTROL",
        "active_candidate": False,
        "reopen": False,
        "lesson": "CANONICAL_COLLECTIVE_SOURCE_COST_DOMINATES",
    },
]

historical = []

for spec in historical_specs:
    a = assess_energy(spec["energy_j"])
    row = dict(spec)
    row["energy_mj"] = spec["energy_j"]/1.0e6
    row["target_factor"] = a.target_factor
    row["band"] = a.band
    row["certified_model"] = False
    historical.append(row)

# Known quantitative controls.
assert historical[0]["band"] == BAND_NEAR
assert historical[1]["band"] == BAND_MECHANISM
assert historical[2]["band"] == BAND_ARCHIVE
assert historical[3]["band"] == BAND_ARCHIVE

# ------------------------------------------------------------
# 4. Trusted active corridor CSV.
# ------------------------------------------------------------

trusted_active_rows.sort(
    key=lambda x: (x["energy_j"], x["family"], x["candidate_id"])
)

TRUSTED_CSV.parent.mkdir(parents=True, exist_ok=True)

trusted_fields = [
    "candidate_id",
    "family",
    "energy_j",
    "energy_mj",
    "target_factor",
    "band",
    "provenance",
    "provenance_reason",
    "replacement_program",
    "active_learning_eligible",
    "certified_model",
]

with TRUSTED_CSV.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=trusted_fields,
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(trusted_active_rows[:1000])

history_fields = [
    "name",
    "energy_j",
    "energy_mj",
    "target_factor",
    "band",
    "status",
    "active_candidate",
    "reopen",
    "lesson",
    "certified_model",
]

with HISTORY_CSV.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=history_fields)
    writer.writeheader()
    writer.writerows(historical)

# ------------------------------------------------------------
# 5. Statistics and decision.
# ------------------------------------------------------------

raw_family_counts = Counter(
    row["family"] for row in raw_db_rows
)
superseded_family_counts = Counter(
    row["family"] for row in superseded_rows
)
trusted_family_counts = Counter(
    row["family"] for row in trusted_active_rows
)

raw_band_counts = Counter(row["band"] for row in raw_db_rows)
trusted_band_counts = Counter(
    row["band"] for row in trusted_active_rows
)

trusted_near = trusted_band_counts.get(BAND_NEAR, 0)
trusted_mechanism = trusted_band_counts.get(BAND_MECHANISM, 0)

if trusted_near > 0:
    next_step = "032V2_RECONSTRUCT_TRUSTED_ACTIVE_10_TO_100MJ_NEAR_MISSES"
elif trusted_mechanism > 0:
    next_step = "032V2_DECOMPOSE_TRUSTED_100MJ_TO_1GJ_MECHANISM_LEADS"
else:
    next_step = "032V2_FEASIBILITY_FIRST_PHYSICAL_ACTION_TEMPLATE_GENERATOR"

result = {
    "branch": "032V1_TRUSTED_LEARNING_CORRIDOR_PROVENANCE",
    "claim_class": "SEARCH_MEMORY_PROVENANCE_AND_STALE_RESULT_SCRUB",
    "strict_policy": {
        "policy_id": str(policy["policy_id"]),
        "target_j": float(policy["limit_j"]),
        "comparison": str(policy["comparison"]),
        "changed": False,
    },
    "v0_compact_csv": {
        "rows": len(raw_csv_rows),
        "family_counts": dict(csv_family_counts),
        "superseded_rows": csv_superseded,
        "current_rows": csv_current,
    },
    "database_corridor": {
        "raw_rows_10mj_to_1gj": len(raw_db_rows),
        "raw_band_counts": dict(raw_band_counts),
        "raw_family_counts": dict(raw_family_counts),
        "superseded_rows": len(superseded_rows),
        "superseded_family_counts": dict(superseded_family_counts),
        "trusted_active_rows": len(trusted_active_rows),
        "trusted_band_counts": dict(trusted_band_counts),
        "trusted_family_counts": dict(trusted_family_counts),
    },
    "historical_verified_controls": historical,
    "rules": {
        "sqlite_history_deleted": False,
        "superseded_rows_used_for_active_ranking": False,
        "superseded_rows_retained_as_history": True,
        "closed_models_reopened": False,
        "corrected_source_aware_controls_override_preliminary_energy_claims": True,
        "higher_energy_learning_equals_success": False,
    },
    "certified_sub10mj_model_found": False,
    "next": next_step,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032V1 RESULT ===")
print("STRICT_POLICY_CHANGED=False")
print("V0_COMPACT_ROWS=" + str(len(raw_csv_rows)))
print("V0_COMPACT_SUPERSEDED_ROWS=" + str(csv_superseded))
print("V0_COMPACT_CURRENT_ROWS=" + str(csv_current))

for family,count in sorted(csv_family_counts.items()):
    print("V0_CSV_FAMILY_" + family + "=" + str(count))

print("RAW_DB_CORRIDOR_ROWS=" + str(len(raw_db_rows)))
print("SUPERSEDED_DB_CORRIDOR_ROWS=" + str(len(superseded_rows)))
print("TRUSTED_ACTIVE_CORRIDOR_ROWS=" + str(len(trusted_active_rows)))
print("TRUSTED_ACTIVE_NEAR_MISS_COUNT=" + str(trusted_near))
print("TRUSTED_ACTIVE_MECHANISM_COUNT=" + str(trusted_mechanism))

for family,count in sorted(superseded_family_counts.items()):
    print("SUPERSEDED_FAMILY_" + family + "=" + str(count))

if trusted_active_rows:
    best = trusted_active_rows[0]
    print("TRUSTED_CLOSEST_FAMILY=" + best["family"])
    print("TRUSTED_CLOSEST_ENERGY_MJ=" + format(best["energy_mj"], ".12e"))
    print("TRUSTED_CLOSEST_FACTOR=" + format(best["target_factor"], ".12e"))
else:
    print("TRUSTED_CLOSEST_FAMILY=NONE")

print("CONTROL_032N1_MJ=" + format(historical[0]["energy_mj"], ".12e"))
print("CONTROL_032N1_FACTOR=" + format(historical[0]["target_factor"], ".12e"))
print("CONTROL_032N1_REOPEN=False")

print("CONTROL_032H_CORRECTED_50M_MJ=" + format(historical[2]["energy_mj"], ".12e"))
print("CONTROL_032H_CORRECTED_FACTOR=" + format(historical[2]["target_factor"], ".12e"))

print("SQLITE_HISTORY_DELETED=False")
print("CLOSED_MODELS_REOPENED=False")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=NO")
print("NEXT=" + next_step)
