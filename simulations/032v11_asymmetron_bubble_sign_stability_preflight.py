"""032V11 published-asymmetron bubble sign/stability preflight."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from antigravity_research.agminer.asymmetron_sign import (
    C_LIGHT,
    asymmetron_vacua,
    euclidean_bounce_radius,
    leading_weyl_factor,
    radial_fifth_acceleration,
    static_bubble_critical_radius,
    static_bubble_energy,
    static_bubble_second_derivative_at_critical,
)
from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.policy import current_energy_policy
from antigravity_research.agminer.reporting import rebuild_summaries
from antigravity_research.agminer.storage import Storage


ROOT = Path(__file__).resolve().parents[1]

V10 = ROOT / "results" / "data" / "032v10_kernel_aware_collective_promotion_summary.json"
OUT = ROOT / "results" / "data" / "032v11_asymmetron_bubble_sign_stability_summary.json"
CSV_OUT = ROOT / "results" / "data" / "032v11_asymmetron_force_sign_scan.csv"
DB = ROOT / "results" / "agminer" / "agminer.sqlite3"

STRICT_TARGET_J = 1.0e7

policy = current_energy_policy()
assert float(policy["limit_j"]) == STRICT_TARGET_J
assert str(policy["comparison"]) == "LT"

if not V10.exists():
    raise FileNotFoundError(str(V10))

v10 = json.loads(V10.read_text(encoding="utf-8"))

assert v10["highest_priority_open_structure"] == "2026_ASYMMETRON_BUBBLE_BRANCH"

# ============================================================
# 1. EXACT VACUUM SIGN STRUCTURE
# ============================================================

ratios = [
    1.0e-6,
    1.0e-4,
    1.0e-2,
    0.1,
    1.0,
    10.0,
]

vacuum_rows = []

for ratio in ratios:
    v = asymmetron_vacua(1.0, ratio)

    vacuum_rows.append({
        "kappa_over_lambda": ratio,
        "phi_plus_over_phi0": v.phi_plus,
        "phi_minus_over_phi0": v.phi_minus,
        "phi_plus_positive": v.phi_plus > 0.0,
        "phi_minus_negative": v.phi_minus < 0.0,
        "opposite_sign_vacua": v.phi_plus*v.phi_minus < 0.0,
    })

assert all(row["opposite_sign_vacua"] for row in vacuum_rows)

# ============================================================
# 2. POINTWISE WALL SIGN THEOREM
# ============================================================

# True vacuum inside, false vacuum outside:
# phi decreases through zero as r increases.

inner_true_side_accel = radial_fifth_acceleration(
    +0.5,
    -1.0,
    2.0,
)

outer_false_side_accel = radial_fifth_acceleration(
    -0.5,
    -1.0,
    2.0,
)

assert inner_true_side_accel > 0.0
assert outer_false_side_accel < 0.0

# Reverse orientation:
# false inside, true outside, phi increases through zero.

inner_false_side_accel = radial_fifth_acceleration(
    -0.5,
    +1.0,
    2.0,
)

outer_true_side_accel = radial_fifth_acceleration(
    +0.5,
    +1.0,
    2.0,
)

assert inner_false_side_accel > 0.0
assert outer_true_side_accel < 0.0

# In both orientations the force points toward the phi=0 wall.

external_true_repulsion_found = False
external_finite_payload_surface_can_be_uniformly_outward = False

# ============================================================
# 3. FREE BUBBLE STABILITY THEOREM
# ============================================================

sigma_demo = 1.0
epsilon_demo = 1.0

static_rc_demo = static_bubble_critical_radius(
    sigma_demo,
    epsilon_demo,
)

static_curvature_demo = static_bubble_second_derivative_at_critical(
    sigma_demo,
)

assert static_curvature_demo < 0.0

free_static_bubble_stable = False

# ============================================================
# 4. PUBLISHED LAB PARAMETER BENCHMARK
# ============================================================

# Representative parameter choice used in the 2026 paper when discussing
# a laboratory vacuum chamber.

MU_GEV = 2.0e-13
M_GEV = 100.0
LAMBDA = 1.0e-10
KAPPA_OVER_LAMBDA = 1.0e-2
KAPPA = KAPPA_OVER_LAMBDA * LAMBDA

GEV_TO_J = 1.602176634e-10
HBARC_GEV_M = 1.973269804e-16

PHI0_GEV = MU_GEV / math.sqrt(LAMBDA)
vac = asymmetron_vacua(
    PHI0_GEV,
    KAPPA_OVER_LAMBDA,
)

L0_M = (
    1.0 / (math.sqrt(2.0)*MU_GEV)
) * HBARC_GEV_M

SIGMA_GEV3 = (
    2.0*math.sqrt(2.0)*MU_GEV**3
    / (3.0*LAMBDA)
)

GEV3_TO_J_PER_M2 = GEV_TO_J / (HBARC_GEV_M**2)
SIGMA_J_M2 = SIGMA_GEV3 * GEV3_TO_J_PER_M2

# Published thin-wall Euclidean bounce radius:
# R0 = 3 sqrt(2)/mu * lambda/kappa.

R_EUCLIDEAN_M = (
    3.0*math.sqrt(2.0)
    / MU_GEV
    * (LAMBDA/KAPPA)
    * HBARC_GEV_M
)

EPSILON_J_M3 = 3.0*SIGMA_J_M2/R_EUCLIDEAN_M

R_STATIC_M = static_bubble_critical_radius(
    SIGMA_J_M2,
    EPSILON_J_M3,
)

STATIC_BARRIER_J = static_bubble_energy(
    R_STATIC_M,
    SIGMA_J_M2,
    EPSILON_J_M3,
)

STATIC_SECOND_DERIVATIVE = static_bubble_second_derivative_at_critical(
    SIGMA_J_M2,
)

WALL_SURFACE_ENERGY_AT_EUCLIDEAN_RADIUS_J = (
    4.0*math.pi*R_EUCLIDEAN_M**2*SIGMA_J_M2
)

# Use log1p because the conformal contrasts are extremely small.

lnA_true = math.log1p(
    vac.phi_plus**2/(2.0*M_GEV**2)
)

lnA_false = math.log1p(
    vac.phi_minus**2/(2.0*M_GEV**2)
)

DELTA_LNA_VACUA = lnA_true - lnA_false

# Leading symmetric thin-wall profile:
# phi = -phi0*tanh(x), x=(r-R)/(2L0).
# The external-side peak occurs at |tanh x|=1/sqrt(3).

y_peak = 1.0/math.sqrt(3.0)
phi_outer_peak = -PHI0_GEV*y_peak
dphi_outer_peak_dr = (
    -PHI0_GEV
    / (2.0*L0_M)
    * (1.0-y_peak*y_peak)
)

OUTER_PEAK_ACCEL_MPS2 = radial_fifth_acceleration(
    phi_outer_peak,
    dphi_outer_peak_dr,
    M_GEV,
)

assert OUTER_PEAK_ACCEL_MPS2 < 0.0
assert STATIC_SECOND_DERIVATIVE < 0.0

# ============================================================
# 5. AGMINER REJECTION MEMORY
# ============================================================

params = {
    "model": "2026_ASYMMETRON_BUBBLE",
    "weyl_factor": "1+phi^2/(2M^2)",
    "explicit_breaking": "CUBIC_BARE_POTENTIAL",
    "external_payload_geometry": "PAYLOAD_OUTSIDE_DOMAIN_WALL",
    "kappa_over_lambda_benchmark": KAPPA_OVER_LAMBDA,
}

candidate = Candidate(
    family_id="032V11_2026_ASYMMETRON_BUBBLE",
    family_version="1",
    params=params,
    physical_model_version="AQEEL_BURRAGE_GOULD_SAFFIN_2026_LEADING_WEYL",
    energy_ledger_version="SIGN_PREFLIGHT_NO_COMPLETE_LEDGER",
)

storage = Storage(DB)

if storage.candidate_state(candidate.candidate_id) is None:
    storage.record_candidate(
        candidate,
        state="TIER0_RUNNING",
        tier=0,
        run_id="032V11",
    )

if not storage.is_terminal(candidate.candidate_id):
    storage.reject(
        candidate.candidate_id,
        state="REJECTED_PAYLOAD",
        failure_code="P001",
        gate="asymmetron_external_wall_sign",
        energy_j=None,
        run_id="032V11",
    )

assert storage.candidate_state(candidate.candidate_id) == "REJECTED_PAYLOAD"

reporting = rebuild_summaries(
    storage,
    ROOT / "results" / "agminer",
)

storage.close()

# ============================================================
# 6. WRITE OUTPUT
# ============================================================

CSV_OUT.parent.mkdir(parents=True, exist_ok=True)

with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(vacuum_rows[0].keys()),
    )
    writer.writeheader()
    writer.writerows(vacuum_rows)

minimal_published_asymmetron_external_repulsion_branch_closed = True
full_asymmetron_family_closed = False

decision = (
    "RED_PUBLISHED_ASYMMETRON_BUBBLE_EXTERNAL_FORCE_ATTRACTS_TO_WALL"
)

next_step = (
    "032V12_LOCAL_METRIC_ACTIVE_SOURCE_OPERATOR_ATLAS"
)

result = {
    "branch": "032V11_ASYMMETRON_BUBBLE_SIGN_STABILITY_PREFLIGHT",
    "claim_class": "ANALYTIC_SIGN_AND_FREE_BUBBLE_STABILITY_CLOSEOUT",
    "strict_target_j": STRICT_TARGET_J,
    "strict_policy_changed": False,
    "published_model_structure": {
        "weyl_factor": "A=1+phi^2/(2M^2)+higher_even_terms",
        "explicit_breaking_location": "BARE_POTENTIAL_CUBIC",
        "physical_force": "a5=-c^2 grad ln A",
        "vacua_opposite_sign": True,
        "weyl_minimum_at_phi_zero": True,
    },
    "force_sign": {
        "true_inside_inner_side": "OUTWARD_TOWARD_WALL",
        "true_inside_external_side": "INWARD_TOWARD_WALL",
        "false_inside_inner_side": "OUTWARD_TOWARD_WALL",
        "false_inside_external_side": "INWARD_TOWARD_WALL",
        "wall_force_character": "ATTRACTIVE_TO_ZERO_CROSSING_FROM_BOTH_SIDES",
        "external_true_repulsion_found": external_true_repulsion_found,
        "external_finite_payload_uniformly_outward_possible": external_finite_payload_surface_can_be_uniformly_outward,
    },
    "free_bubble_stability": {
        "spatial_energy": "4*pi*sigma*R^2-(4*pi/3)*epsilon*R^3",
        "static_critical_radius": "2*sigma/epsilon",
        "euclidean_bounce_radius": "3*sigma/epsilon",
        "critical_second_derivative_negative": True,
        "free_static_bubble_stable": free_static_bubble_stable,
    },
    "published_lab_benchmark": {
        "mu_gev": MU_GEV,
        "m_gev": M_GEV,
        "lambda": LAMBDA,
        "kappa_over_lambda": KAPPA_OVER_LAMBDA,
        "phi0_gev": PHI0_GEV,
        "wall_compton_length_m": L0_M,
        "surface_tension_j_m2": SIGMA_J_M2,
        "euclidean_bounce_radius_m": R_EUCLIDEAN_M,
        "static_critical_radius_m": R_STATIC_M,
        "scalar_static_barrier_j": STATIC_BARRIER_J,
        "wall_surface_energy_at_euclidean_radius_j": WALL_SURFACE_ENERGY_AT_EUCLIDEAN_RADIUS_J,
        "delta_lnA_true_minus_false": DELTA_LNA_VACUA,
        "leading_outer_side_peak_accel_mps2": OUTER_PEAK_ACCEL_MPS2,
        "leading_outer_side_peak_accel_over_g": OUTER_PEAK_ACCEL_MPS2/9.80665,
        "energy_is_complete_operating_ledger": False,
    },
    "agminer": {
        "candidate_id": candidate.candidate_id,
        "state": "REJECTED_PAYLOAD",
        "failure_code": "P001",
        "gate": "asymmetron_external_wall_sign",
        "reporting": reporting,
    },
    "project_scope": {
        "standard_symmetron_014a_reopened": False,
        "published_minimal_asymmetron_bubble_external_repulsion_closed": minimal_published_asymmetron_external_repulsion_branch_closed,
        "all_possible_modified_asymmetron_weyl_factors_closed": False,
        "full_asymmetron_family_closed": full_asymmetron_family_closed,
    },
    "physical_antigravity_model_found": False,
    "certified_sub10mj_model_found": False,
    "decision": decision,
    "next": next_step,
}

OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032V11 RESULT ===")
print("VACUA_OPPOSITE_SIGN=True")
print("TRUE_INSIDE_EXTERNAL_FORCE=INWARD_TOWARD_WALL")
print("FALSE_INSIDE_EXTERNAL_FORCE=INWARD_TOWARD_WALL")
print("DOMAIN_WALL_FORCE=ATTRACTIVE_TO_PHI_ZERO_CORE")
print("EXTERNAL_TRUE_REPULSION_FOUND=False")
print("EXTERNAL_FINITE_PAYLOAD_UNIFORMLY_OUTWARD=False")

print("FREE_STATIC_BUBBLE_STABLE=False")
print("STATIC_CRITICAL_SECOND_DERIVATIVE_SIGN=NEGATIVE")

print("BENCHMARK_L0_M=" + format(L0_M, ".12e"))
print("BENCHMARK_SIGMA_J_M2=" + format(SIGMA_J_M2, ".12e"))
print("BENCHMARK_EUCLIDEAN_RADIUS_M=" + format(R_EUCLIDEAN_M, ".12e"))
print("BENCHMARK_STATIC_CRITICAL_RADIUS_M=" + format(R_STATIC_M, ".12e"))
print("BENCHMARK_SCALAR_STATIC_BARRIER_J=" + format(STATIC_BARRIER_J, ".12e"))
print("BENCHMARK_WALL_SURFACE_ENERGY_J=" + format(WALL_SURFACE_ENERGY_AT_EUCLIDEAN_RADIUS_J, ".12e"))
print("BENCHMARK_OUTER_PEAK_ACCEL_MPS2=" + format(OUTER_PEAK_ACCEL_MPS2, ".12e"))
print("BENCHMARK_OUTER_PEAK_ACCEL_OVER_G=" + format(OUTER_PEAK_ACCEL_MPS2/9.80665, ".12e"))
print("BENCHMARK_ENERGY_IS_COMPLETE_LEDGER=False")

print("AGMINER_STATE=REJECTED_PAYLOAD")
print("AGMINER_FAILURE_CODE=P001")
print("PUBLISHED_MINIMAL_ASYMMETRON_BUBBLE_EXTERNAL_REPULSION=CLOSED")
print("FULL_ASYMMETRON_FAMILY=CLOSED_NO")
print("PHYSICAL_ANTIGRAVITY_MODEL_FOUND=NO")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=NO")
print("DECISION=" + decision)
print("NEXT=" + next_step)
