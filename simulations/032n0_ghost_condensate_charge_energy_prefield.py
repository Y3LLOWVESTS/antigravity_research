"""
032N0 — minimal ghost-condensate gravitational-charge prefield gate.

Scientific basis:
  Small ghost-condensate fluctuations have positive conserved particle-
  physics energy while the gravitational T00 begins linearly in pi_dot.
  This permits opposite-sign gravitational charge without opposite-sign
  inertial energy at the level of the low-energy EFT.

This run tests an optimistic finite cylindrical source adjacent to a
finite spherical payload.

It is NOT a field solution.
It is NOT a microscopic source realization.
It is NOT a certified antigravity device.

Omitted positive costs include:
  localization-gradient energy,
  source/generator energy,
  activation/control energy,
  reaction/backreaction,
  compensation needed for positive far-field active mass,
  support and stabilization.

Therefore a failure of the optimistic bulk floor is strong evidence
against this particular minimal uniform-cylinder branch.
A success is only headroom and requires stronger reconstruction.
"""

from __future__ import annotations

import csv
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution
from scipy.stats import qmc


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "data" / "032n0_ghost_condensate_charge_energy_prefield_summary.json"
TOP_OUT = ROOT / "results" / "data" / "032n0_ghost_condensate_top_candidates.csv"

SAMPLES = 10_000_000
CHUNK = 250_000
TOP_KEEP = 100

G = 6.67430e-11
C = 299792458.0
HBARC_GEV_M = 1.973269804e-16
GEV_TO_J = 1.602176634e-10
GEV4_TO_J_M3 = GEV_TO_J / HBARC_GEV_M ** 3

PAYLOAD_RADIUS_M = 0.10
TARGET_ACCEL_MPS2 = 9.80665
ENERGY_TARGET_J = 1.0e7

# Favorable upper edge of the minimal ghost-condensate phenomenological
# scale quoted by the nonlinear follow-up literature.
M_GEV = 100.0

# Broad device-scale geometry box.
LOG10_R_MIN = -3.0
LOG10_R_MAX = 2.0
LOG10_L_MIN = -3.0
LOG10_L_MAX = 2.0
LOG10_GAP_MIN = -4.0
LOG10_GAP_MAX = -1.0

# kappa parametrizes deliberately favorable O(1)-to-10 uncertainty in
# the gravitational-charge normalization T00 = kappa M^2 pi_dot.
LOG10_KAPPA_MIN = 0.0
LOG10_KAPPA_MAX = 1.0


def physical_from_unit(unit):
    log_r = LOG10_R_MIN + unit[:, 0] * (LOG10_R_MAX - LOG10_R_MIN)
    log_l = LOG10_L_MIN + unit[:, 1] * (LOG10_L_MAX - LOG10_L_MIN)
    log_gap = LOG10_GAP_MIN + unit[:, 2] * (LOG10_GAP_MAX - LOG10_GAP_MIN)
    log_kappa = LOG10_KAPPA_MIN + unit[:, 3] * (LOG10_KAPPA_MAX - LOG10_KAPPA_MIN)

    return (
        10.0 ** log_r,
        10.0 ** log_l,
        10.0 ** log_gap,
        10.0 ** log_kappa,
    )


def evaluate_arrays(radius_m, thickness_m, gap_m, kappa):
    # Source occupies a cylinder ending at z=0.
    # The spherical payload begins at z=gap.
    # The adverse payload surface is its farthest point from the source.
    z_far = gap_m + 2.0 * PAYLOAD_RADIUS_M

    lever_m = (
        thickness_m
        - np.sqrt((z_far + thickness_m) ** 2 + radius_m ** 2)
        + np.sqrt(z_far ** 2 + radius_m ** 2)
    )

    healthy = lever_m > 0.0
    safe_lever = np.where(healthy, lever_m, np.nan)

    # Exact Newtonian axial field of a uniform finite cylinder:
    # a = 2 pi G rho_active * lever.
    rho_active_kg_m3 = (
        TARGET_ACCEL_MPS2
        / (2.0 * math.pi * G * safe_lever)
    )

    active_t00_j_m3 = rho_active_kg_m3 * C ** 2
    active_t00_gev4 = active_t00_j_m3 / GEV4_TO_J_M3

    # Optimistic ghost-condensate bulk relation:
    # T00 = kappa M^2 pi_dot
    # E_pp = 1/2 pi_dot^2
    # => E_pp density = T00^2 / (2 kappa^2 M^4).
    epp_density_gev4 = (
        active_t00_gev4 ** 2
        / (2.0 * kappa ** 2 * M_GEV ** 4)
    )

    volume_m3 = math.pi * radius_m ** 2 * thickness_m
    volume_gev_minus3 = volume_m3 / HBARC_GEV_M ** 3

    epp_j = epp_density_gev4 * volume_gev_minus3 * GEV_TO_J

    active_mass_kg = rho_active_kg_m3 * volume_m3
    active_energy_abs_j = active_mass_kg * C ** 2

    epp_j = np.where(healthy, epp_j, np.inf)

    return (
        epp_j,
        rho_active_kg_m3,
        active_mass_kg,
        active_energy_abs_j,
        lever_m,
    )


def scalar_energy(log_params):
    radius_m = 10.0 ** float(log_params[0])
    thickness_m = 10.0 ** float(log_params[1])
    gap_m = 10.0 ** float(log_params[2])
    kappa = 10.0 ** float(log_params[3])

    z_far = gap_m + 2.0 * PAYLOAD_RADIUS_M
    lever_m = (
        thickness_m
        - math.sqrt((z_far + thickness_m) ** 2 + radius_m ** 2)
        + math.sqrt(z_far ** 2 + radius_m ** 2)
    )

    if lever_m <= 0.0:
        return 1.0e300

    rho_active = TARGET_ACCEL_MPS2 / (2.0 * math.pi * G * lever_m)
    t00_j_m3 = rho_active * C ** 2
    t00_gev4 = t00_j_m3 / GEV4_TO_J_M3
    epp_density = t00_gev4 ** 2 / (2.0 * kappa ** 2 * M_GEV ** 4)
    volume = math.pi * radius_m ** 2 * thickness_m
    volume_g = volume / HBARC_GEV_M ** 3
    return epp_density * volume_g * GEV_TO_J


start = time.perf_counter()
sampler = qmc.Sobol(d=4, scramble=True, seed=32032)

top = []
passing = 0
evaluated = 0

print("=== 032N0 SOBOL FRONTIER ===")
print("SAMPLES=" + str(SAMPLES))
print("M_GEV=" + format(M_GEV, ".12e"))
print("KAPPA_RANGE=1_TO_10")
print("FINITE_PAYLOAD_ADVERSE_SURFACE=YES")

while evaluated < SAMPLES:
    count = min(CHUNK, SAMPLES - evaluated)
    unit = sampler.random(count)
    radius_m, thickness_m, gap_m, kappa = physical_from_unit(unit)

    (
        energy_j,
        rho_active,
        active_mass,
        active_energy,
        lever_m,
    ) = evaluate_arrays(radius_m, thickness_m, gap_m, kappa)

    finite = np.isfinite(energy_j)
    passing += int(np.count_nonzero(finite & (energy_j < ENERGY_TARGET_J)))

    local_keep = min(TOP_KEEP, count)
    indices = np.argpartition(energy_j, local_keep - 1)[:local_keep]

    for i in indices:
        if not math.isfinite(float(energy_j[i])):
            continue
        top.append(
            {
                "sample_index": evaluated + int(i),
                "energy_j": float(energy_j[i]),
                "radius_m": float(radius_m[i]),
                "thickness_m": float(thickness_m[i]),
                "gap_m": float(gap_m[i]),
                "kappa": float(kappa[i]),
                "rho_active_kg_m3": float(rho_active[i]),
                "active_mass_abs_kg": float(active_mass[i]),
                "active_energy_abs_j": float(active_energy[i]),
                "lever_m": float(lever_m[i]),
            }
        )

    top.sort(key=lambda row: (row["energy_j"], row["sample_index"]))
    del top[TOP_KEEP:]

    evaluated += count

    if evaluated % 1_000_000 == 0 or evaluated == SAMPLES:
        best_now = top[0]["energy_j"] if top else float("inf")
        print(
            "PROGRESS"
            + " evaluated=" + str(evaluated)
            + " passing=" + str(passing)
            + " best_j=" + format(best_now, ".12e"),
            flush=True,
        )

sobol_seconds = time.perf_counter() - start

print("")
print("=== INDEPENDENT CONTINUOUS OPTIMIZATION ===")

bounds = [
    (LOG10_R_MIN, LOG10_R_MAX),
    (LOG10_L_MIN, LOG10_L_MAX),
    (LOG10_GAP_MIN, LOG10_GAP_MAX),
    (LOG10_KAPPA_MIN, LOG10_KAPPA_MAX),
]

opt_start = time.perf_counter()
opt = differential_evolution(
    scalar_energy,
    bounds,
    seed=32033,
    popsize=24,
    maxiter=500,
    tol=1.0e-10,
    atol=0.0,
    polish=True,
    workers=1,
    updating="immediate",
)
opt_seconds = time.perf_counter() - opt_start

opt_r = 10.0 ** float(opt.x[0])
opt_l = 10.0 ** float(opt.x[1])
opt_gap = 10.0 ** float(opt.x[2])
opt_kappa = 10.0 ** float(opt.x[3])
opt_energy = float(opt.fun)

(
    opt_energy_arr,
    opt_rho_arr,
    opt_mass_arr,
    opt_active_arr,
    opt_lever_arr,
) = evaluate_arrays(
    np.asarray([opt_r]),
    np.asarray([opt_l]),
    np.asarray([opt_gap]),
    np.asarray([opt_kappa]),
)

opt_rho = float(opt_rho_arr[0])
opt_mass = float(opt_mass_arr[0])
opt_active = float(opt_active_arr[0])
opt_lever = float(opt_lever_arr[0])

best_sobol = top[0]
reconstruction_relerr = abs(best_sobol["energy_j"] - scalar_energy([
    math.log10(best_sobol["radius_m"]),
    math.log10(best_sobol["thickness_m"]),
    math.log10(best_sobol["gap_m"]),
    math.log10(best_sobol["kappa"]),
])) / best_sobol["energy_j"]

# Remove the deliberately favorable kappa=10 oracle to reconstruct the
# same optimized geometry at the natural order-unity normalization.
unit_kappa_energy = scalar_energy([
    math.log10(opt_r),
    math.log10(opt_l),
    math.log10(opt_gap),
    0.0,
])

required_kappa_for_10mj = opt_kappa * math.sqrt(opt_energy / ENERGY_TARGET_J)

# Because E_pp scales as M^-4, reconstruct the M that would be needed
# at the optimized geometry and kappa=10 to touch the strict objective.
required_m_gev_for_10mj = M_GEV * (opt_energy / ENERGY_TARGET_J) ** 0.25

# Likewise at the order-unity kappa normalization.
required_m_gev_kappa1 = M_GEV * (unit_kappa_energy / ENERGY_TARGET_J) ** 0.25

with TOP_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(top[0].keys()))
    writer.writeheader()
    writer.writerows(top)

raw_charge_energy_separation = True
strict_pass = opt_energy < ENERGY_TARGET_J

if strict_pass:
    decision = "HEADROOM_PRESENT_REQUIRES_LOCALIZATION_AND_SOURCE_REALIZATION"
    next_step = "032N1_LOCALIZATION_GRADIENT_AND_CONSERVATION_GATE"
else:
    decision = "RED_UNIFORM_CYLINDER_MINIMAL_GHOST_CONDENSATE_BULK_FLOOR"
    next_step = "032N1_VARIATIONAL_MORPHOLOGY_BEFORE_FAMILY_DEMOTION"

result = {
    "branch": "032N0_GHOST_CONDENSATE_GRAVITATIONAL_CHARGE",
    "claim_class": "PREFIELD_FINITE_PAYLOAD_OPTIMISTIC_ENERGY_GATE",
    "literature_structure": {
        "shift_symmetry": True,
        "positive_small_fluctuation_particle_energy": True,
        "opposite_sign_gravitational_t00_possible": True,
        "neutral_matter_can_respond_via_gravity_without_direct_portal": True,
        "minimal_theory_m_cap_gev_used": M_GEV,
    },
    "samples": SAMPLES,
    "payload_radius_m": PAYLOAD_RADIUS_M,
    "target_acceleration_mps2": TARGET_ACCEL_MPS2,
    "energy_target_j": ENERGY_TARGET_J,
    "strict_lt_target": True,
    "geometry": "UNIFORM_FINITE_CYLINDER_AXIS_TO_SPHERICAL_PAYLOAD",
    "adverse_surface_enforced": True,
    "parameter_box": {
        "radius_m": [10.0 ** LOG10_R_MIN, 10.0 ** LOG10_R_MAX],
        "thickness_m": [10.0 ** LOG10_L_MIN, 10.0 ** LOG10_L_MAX],
        "gap_m": [10.0 ** LOG10_GAP_MIN, 10.0 ** LOG10_GAP_MAX],
        "kappa": [10.0 ** LOG10_KAPPA_MIN, 10.0 ** LOG10_KAPPA_MAX],
    },
    "sobol": {
        "passing_points": passing,
        "best": best_sobol,
        "seconds": sobol_seconds,
        "independent_reconstruction_relerr": reconstruction_relerr,
    },
    "continuous_optimization": {
        "success": bool(opt.success),
        "message": str(opt.message),
        "energy_j": opt_energy,
        "radius_m": opt_r,
        "thickness_m": opt_l,
        "gap_m": opt_gap,
        "kappa": opt_kappa,
        "rho_active_kg_m3": opt_rho,
        "active_mass_abs_kg": opt_mass,
        "active_energy_abs_j": opt_active,
        "lever_m": opt_lever,
        "seconds": opt_seconds,
    },
    "order_unity_kappa_same_geometry_energy_j": unit_kappa_energy,
    "required_kappa_for_10mj_at_m100gev": required_kappa_for_10mj,
    "required_m_gev_for_10mj_at_best_kappa": required_m_gev_for_10mj,
    "required_m_gev_for_10mj_at_kappa1": required_m_gev_kappa1,
    "raw_charge_energy_separation_signal": raw_charge_energy_separation,
    "strict_sub10mj_bulk_candidate": strict_pass,
    "omitted_positive_costs": [
        "localization_gradient_energy",
        "source_generator_energy",
        "activation_control_energy",
        "reaction_backreaction",
        "positive_far_field_active_mass_compensation",
        "support_stabilization",
        "nonlinear_field_reconstruction",
    ],
    "field_solution": False,
    "microscopic_source": False,
    "stability_certified": False,
    "complete_operating_ledger": False,
    "certified_antigravity_model": False,
    "full_ghost_condensate_family_closed": False,
    "decision": decision,
    "next": next_step,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("SOBOL_EVALUATED=" + str(evaluated))
print("SOBOL_SUB10MJ_POINTS=" + str(passing))
print("SOBOL_BEST_J=" + format(best_sobol["energy_j"], ".12e"))
print("SOBOL_BEST_R_M=" + format(best_sobol["radius_m"], ".12e"))
print("SOBOL_BEST_L_M=" + format(best_sobol["thickness_m"], ".12e"))
print("SOBOL_BEST_GAP_M=" + format(best_sobol["gap_m"], ".12e"))
print("SOBOL_BEST_KAPPA=" + format(best_sobol["kappa"], ".12e"))
print("SOBOL_RECONSTRUCTION_RELERR=" + format(reconstruction_relerr, ".12e"))
print("OPT_SUCCESS=" + str(bool(opt.success)))
print("OPT_BEST_J=" + format(opt_energy, ".12e"))
print("OPT_R_M=" + format(opt_r, ".12e"))
print("OPT_L_M=" + format(opt_l, ".12e"))
print("OPT_GAP_M=" + format(opt_gap, ".12e"))
print("OPT_KAPPA=" + format(opt_kappa, ".12e"))
print("OPT_ACTIVE_MASS_ABS_KG=" + format(opt_mass, ".12e"))
print("OPT_ACTIVE_ENERGY_ABS_J=" + format(opt_active, ".12e"))
print("KAPPA1_SAME_GEOMETRY_J=" + format(unit_kappa_energy, ".12e"))
print("REQUIRED_KAPPA_FOR_10MJ_M100GEV=" + format(required_kappa_for_10mj, ".12e"))
print("REQUIRED_M_GEV_FOR_10MJ_BEST_KAPPA=" + format(required_m_gev_for_10mj, ".12e"))
print("REQUIRED_M_GEV_FOR_10MJ_KAPPA1=" + format(required_m_gev_kappa1, ".12e"))
print("RAW_CHARGE_ENERGY_SEPARATION_SIGNAL=PRESENT")
print("FIELD_SOLUTION=NO")
print("COMPLETE_OPERATING_LEDGER=NO")
print("CERTIFIED_ANTIGRAVITY_MODEL=NO")
print("FULL_GHOST_CONDENSATE_FAMILY_CLOSED=NO")
print("DECISION=" + decision)
print("NEXT=" + next_step)
