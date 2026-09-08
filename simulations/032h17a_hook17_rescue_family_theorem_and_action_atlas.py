#!/usr/bin/env python3
"""032H17A — HOOK17 rescue-family theorem and action atlas.

PURPOSE
-------
Execute the theorem-first H17A family gate.  This run produces only family
status, projector-support prefilters, and exact next falsifiers.  It does not
scan energy parameters and does not mutate the AGMINER model database.

OUTPUTS
-------
results/data/032h17a_hook17_rescue_family_summary.json
results/data/032h17a_hook17_family_atlas.csv
results/data/032h17a_hook17_projector_prefilter.csv

SUCCESS INTERPRETATION
----------------------
A useful H17A result can be yellow rather than green: identifying a concrete
Ward rescue and pruning healthy-mode projectors is progress even when no
same-action complete family has yet earned H17B promotion.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_rescue_family_atlas import h17a_summary


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "data"
DATA.mkdir(parents=True, exist_ok=True)

SUMMARY_JSON = DATA / "032h17a_hook17_rescue_family_summary.json"
ATLAS_CSV = DATA / "032h17a_hook17_family_atlas.csv"
PROJECTOR_CSV = DATA / "032h17a_hook17_projector_prefilter.csv"


summary = h17a_summary()

with SUMMARY_JSON.open("w", encoding="utf-8") as handle:
    json.dump(summary, handle, indent=2, sort_keys=True)
    handle.write("\n")

atlas = summary["atlas"]
with ATLAS_CSV.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(atlas[0].keys()))
    writer.writeheader()
    writer.writerows(atlas)

projector_rows = summary["hook_mag_projector_prefilter"]["modes"]
with PROJECTOR_CSV.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(projector_rows[0].keys()))
    writer.writeheader()
    writer.writerows(projector_rows)

print(f"032H17A_DECISION={summary['decision']}", flush=True)
print(f"NEXT={summary['next']}", flush=True)
print(
    "CURTRIGHT_KINEMATIC_WARD_RESCUE="
    f"{summary['curtright_kinematic_ward_rescue_is_real']}",
    flush=True,
)
print(
    "CURTRIGHT_REST_FRAME_POLE_OVERLAP_ZERO="
    f"{summary['curtright_rest_frame_pole_overlap_zero']}",
    flush=True,
)
print(
    "HOOK_MAG_SUPPORT_SURVIVORS="
    + ",".join(summary["most_informative_next_modes"]),
    flush=True,
)
print(
    "HOOK_MAG_EXACT_SUPPORT_ZEROS="
    + ",".join(summary["permanent_clean_rest_pole_zeros"]),
    flush=True,
)
print(
    "SAME_ACTION_COMPLETE_SURVIVORS="
    f"{summary['same_action_complete_survivor_count']}",
    flush=True,
)
print(f"H17B_AUTHORIZED={summary['h17b_authorized']}", flush=True)
print(
    f"ENERGY_OPTIMIZATION_AUTHORIZED={summary['energy_optimization_authorized']}",
    flush=True,
)
print(
    "HOOK17_REFERENCE_CAPACITY_RP1E12_J="
    f"{summary['hook17_reference_capacity_rp1e12_j']:.12f}",
    flush=True,
)
print("HOOK17_COMPLETE_ENERGY_J=UNKNOWN", flush=True)
print("PHYSICAL_ANTIGRAVITY_MODEL_FOUND=NO", flush=True)
print("CERTIFIED_SUB10MJ_MODEL_FOUND=NO", flush=True)
print("PRACTICAL_DEVICE_FOUND=NO", flush=True)
print(f"SUMMARY_JSON={SUMMARY_JSON}", flush=True)
print(f"ATLAS_CSV={ATLAS_CSV}", flush=True)
print(f"PROJECTOR_CSV={PROJECTOR_CSV}", flush=True)
