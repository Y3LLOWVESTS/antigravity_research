"""
032C Tier-0B reciprocal twin-matter source-flux audit.

This audits the existing DBI headroom points with a specific microscopic
source realization: reciprocal twin matter carrying scalar charge per
energy alpha/Mpl and supplying a one-sided field over at least the
projected payload disk.

It is NOT a no-go theorem for every possible DBI source architecture.
"""

from __future__ import annotations

import json
import math
import sqlite3
import sys
from pathlib import Path

from antigravity_research.agminer.policy import current_energy_policy

MPL_REDUCED_GEV = 2.435e18
TOP_MASS_GEV = 172.76
HBARC_GEV_M = 1.973269804e-16
HBARC_EV_M = 1.973269804e-7
GEV_TO_J = 1.602176634e-10
C_LIGHT = 299792458.0

root = Path(__file__).resolve().parents[1]
db_path = Path(sys.argv[1])
config = json.loads(
    (root / "config" / "agminer_032a.json").read_text(encoding="utf-8")
)
policy = current_energy_policy()
target_j = float(policy["limit_j"])
radius_m = float(config["payload_radius_m"])
accel = float(config["target_cm_accel_mps2"])

connection = sqlite3.connect(db_path)
connection.row_factory = sqlite3.Row

columns = {
    row["name"]
    for row in connection.execute("PRAGMA table_info(models)").fetchall()
}

param_candidates = [
    "params_json_compact",
    "params_json",
    "parameters_json",
    "params",
]

param_column = next(
    (name for name in param_candidates if name in columns),
    None,
)

if param_column is None:
    raise RuntimeError("Could not locate compact parameter column")

query = (
    "SELECT candidate_id, "
    + param_column
    + " AS params_json, energy_j "
    + "FROM models "
    + "WHERE family=? AND state=?"
)

rows = connection.execute(
    query,
    (
        "032C_TWIN_PNGB_DBI_METRIC",
        "TIER0_HEADROOM_ONLY_INCOMPLETE_LEDGER",
    ),
).fetchall()

connection.close()

area_gev_minus2 = (
    math.pi
    * (radius_m / HBARC_GEV_M) ** 2
)

def audit_point(row):
    params = json.loads(row["params_json"])
    alpha = 10.0 ** float(params["log10_alpha"])
    scale_ev = 10.0 ** float(params["log10_dbi_scale_ev"])
    scale_gev = scale_ev * 1.0e-9

    gradient = (
        MPL_REDUCED_GEV
        / alpha
        * accel
        / C_LIGHT ** 2
        * HBARC_GEV_M
    )

    scale_sq = scale_gev ** 2
    ratio = gradient / scale_sq

    displacement = (
        gradient
        / math.sqrt(1.0 + ratio ** 2)
    )

    source_charge = displacement * area_gev_minus2

    source_energy_j = (
        source_charge
        * MPL_REDUCED_GEV
        / alpha
        * GEV_TO_J
    )

    payload_floor_j = float(row["energy_j"])
    partial_total_j = source_energy_j + payload_floor_j

    return {
        "candidate_id": str(row["candidate_id"]),
        "alpha": alpha,
        "dbi_scale_ev": scale_ev,
        "gradient_over_scale_squared": ratio,
        "payload_field_floor_j": payload_floor_j,
        "reciprocal_source_floor_j": source_energy_j,
        "partial_total_floor_j": partial_total_j,
        "passes_10mj": partial_total_j < target_j,
    }

audited = [audit_point(row) for row in rows]
audited.sort(key=lambda item: item["partial_total_floor_j"])

passing = [
    item for item in audited if item["passes_10mj"]
]

best = audited[0] if audited else None

# Independent domain-edge optimistic check under the current plugin gates.
range_min_m = 0.20
cutoff_min_gev = 10.0 ** 2.24

mediator_mass_ev = HBARC_EV_M / range_min_m
loop_mass_per_alpha_ev = (
    TOP_MASS_GEV
    * cutoff_min_gev
    / (2.0 * math.pi * MPL_REDUCED_GEV)
    * 1.0e9
)
alpha_domain_max = mediator_mass_ev / loop_mass_per_alpha_ev

probe_momentum_ev = HBARC_EV_M / min(radius_m, range_min_m)
strong_scale_min_ev = 10.0 * max(probe_momentum_ev, mediator_mass_ev)
strong_scale_min_gev = strong_scale_min_ev * 1.0e-9

gradient_domain = (
    MPL_REDUCED_GEV
    / alpha_domain_max
    * accel
    / C_LIGHT ** 2
    * HBARC_GEV_M
)

ratio_domain = gradient_domain / strong_scale_min_gev ** 2
displacement_domain = (
    gradient_domain
    / math.sqrt(1.0 + ratio_domain ** 2)
)

domain_source_floor_j = (
    displacement_domain
    * area_gev_minus2
    * MPL_REDUCED_GEV
    / alpha_domain_max
    * GEV_TO_J
)

result = {
    "branch": "032C_TIER0B",
    "claim_class": "SOURCE_AWARE_ANALYTIC_AUDIT",
    "source_realization": (
        "RECIPROCAL_TWIN_MATTER_ONE_SIDED_PROJECTED_DISK"
    ),
    "full_032c_family_closed": False,
    "audited_headroom_points": len(audited),
    "points_below_10mj_after_source_floor": len(passing),
    "target_j": target_j,
    "best_sample": best,
    "domain_optimistic_alpha_max": alpha_domain_max,
    "domain_optimistic_strong_scale_min_ev": strong_scale_min_ev,
    "domain_optimistic_gradient_ratio": ratio_domain,
    "domain_optimistic_source_floor_j": domain_source_floor_j,
    "domain_optimistic_source_floor_over_target": (
        domain_source_floor_j / target_j
    ),
    "simple_reciprocal_source_closed_over_declared_domain": (
        domain_source_floor_j >= target_j
    ),
    "omitted_positive_costs": [
        "source_internal_structure",
        "twin_sector_rest_energy_beyond_charge_floor",
        "potential",
        "activation",
        "support",
        "control",
        "backreaction",
    ],
}

output = (
    root
    / "results"
    / "data"
    / "032c_tier0b_reciprocal_source_flux_audit_summary.json"
)

output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032C TIER-0B SOURCE-FLUX AUDIT ===")
print("AUDITED_HEADROOM_POINTS=" + str(len(audited)))
print("POINTS_LT_10MJ_AFTER_SOURCE_FLOOR=" + str(len(passing)))

if best is not None:
    print("BEST_CANDIDATE=" + best["candidate_id"])
    print(
        "BEST_PAYLOAD_FIELD_FLOOR_J="
        + format(best["payload_field_floor_j"], ".12e")
    )
    print(
        "BEST_SOURCE_FLOOR_J="
        + format(best["reciprocal_source_floor_j"], ".12e")
    )
    print(
        "BEST_PARTIAL_TOTAL_J="
        + format(best["partial_total_floor_j"], ".12e")
    )
    print(
        "BEST_GRADIENT_OVER_M2="
        + format(best["gradient_over_scale_squared"], ".12e")
    )

print(
    "DOMAIN_OPTIMISTIC_SOURCE_FLOOR_J="
    + format(domain_source_floor_j, ".12e")
)
print(
    "DOMAIN_SOURCE_FLOOR_OVER_10MJ="
    + format(domain_source_floor_j / target_j, ".12e")
)
print(
    "SIMPLE_RECIPROCAL_SOURCE_CLOSED="
    + str(domain_source_floor_j >= target_j)
)
print("FULL_032C_FAMILY_CLOSED=False")
