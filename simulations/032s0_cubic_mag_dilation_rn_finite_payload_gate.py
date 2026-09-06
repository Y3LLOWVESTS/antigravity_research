"""
032S0 — cubic metric-affine dilation-charge RN-like finite-payload gate.

Literature structure:

  Psi(r) = 1 - 2m/r + Q_MAG/r^2

with the dilation contribution

  Q_d = 1/2 kappa_d^2
        (2 a6 - 4 a2 - 8 a14 - d1).

Ghost-free vector/axial conditions of the exact solution include

  d1 <= 0
  a6 <= -2 a2
  a14 <= (2 a6 - 4 a2 - d1)/8.

Write

  a14 = (2 a6 - 4 a2 - d1)/8 - w

with w >= 0. Then identically

  Q_d = 4 w kappa_d^2 >= 0.

Thus any strictly interior stability margin w>0 gives the RN-like
repulsive sign for the dilation contribution.

For a neutral test body momentarily at rest in

  ds^2 = Psi c^2 dt^2 - dr^2/Psi - r^2 dOmega^2,

the exact instantaneous radial geodesic acceleration is

  a_r = -GM/r^2 + c^2 Q/r^3.

This run asks whether the exact metric can meet the finite payload target
and then quantifies the still-missing microscopic charge-per-joule burden.

Important:
  The canonical Maxwell-like exterior-field energy calculation below is
  only a normalization benchmark.
  It is NOT asserted to be a lower bound on cubic MAG.
  The actual cubic-MAG Hamiltonian/source-charge relation remains open.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar
from numpy.polynomial.legendre import leggauss


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "data" / "032s0_cubic_mag_dilation_rn_finite_payload_summary.json"
SURFACE_OUT = ROOT / "results" / "data" / "032s0_cubic_mag_payload_surface_scan.csv"

G = 6.67430e-11
C = 299792458.0

ENERGY_TARGET_J = 1.0e7
TARGET_ACCEL = 9.80665
PAYLOAD_RADIUS_M = 0.10

# Give the entire objective inventory to positive ADM/source mass.
# This is conservative for the required repulsive Q because positive mass
# slightly increases the Q necessary to overcome attraction.
ADM_ENERGY_J = ENERGY_TARGET_J
ADM_MASS_KG = ADM_ENERGY_J / C ** 2
M_GEO_M = G * ADM_MASS_KG / C ** 2

# Contact is used as the favorable non-overlap infimum.
GAP_M = 0.0


def dilation_coefficient_from_stability_margin(w):
    #
    # Exact consequence of
    # a14 = bound - w.
    return 4.0 * w


def q_required_for_far_surface(source_radius_m):
    r_far = (
        source_radius_m
        + GAP_M
        + 2.0 * PAYLOAD_RADIUS_M
    )
    return (
        TARGET_ACCEL * r_far ** 3 / C ** 2
        + G * ADM_MASS_KG * r_far / C ** 2
    )


def canonical_rn_exterior_energy_j(source_radius_m):
    #
    # Maxwell-like RN benchmark:
    #
    # Q_metric = G q^2/(4 pi eps0 c^4)
    # E_outside(R) = q^2/(8 pi eps0 R)
    #              = Q_metric c^4/(2 G R).
    q = q_required_for_far_surface(source_radius_m)
    return q * C ** 4 / (2.0 * G * source_radius_m)


# Independent scalar optimization of the canonical RN benchmark.
opt = minimize_scalar(
    canonical_rn_exterior_energy_j,
    bounds=(1.0e-6, 10.0),
    method="bounded",
    options={"xatol": 1.0e-14},
)

R_SOURCE = float(opt.x)
Q_REQUIRED = q_required_for_far_surface(R_SOURCE)
E_CANONICAL = float(opt.fun)

D_CENTER = R_SOURCE + GAP_M + PAYLOAD_RADIUS_M
R_NEAR = D_CENTER - PAYLOAD_RADIUS_M
R_FAR = D_CENTER + PAYLOAD_RADIUS_M


def psi(r):
    return 1.0 - 2.0 * M_GEO_M / r + Q_REQUIRED / r ** 2


def radial_accel(r):
    return (
        -G * ADM_MASS_KG / r ** 2
        + C ** 2 * Q_REQUIRED / r ** 3
    )


def axial_accel(z, rho):
    r2 = z * z + rho * rho
    r = np.sqrt(r2)
    return (
        -G * ADM_MASS_KG * z / r ** 3
        + C ** 2 * Q_REQUIRED * z / r ** 4
    )


# Dense complete payload-surface angular scan.
N_SURFACE = 1_000_001
mu = np.linspace(-1.0, 1.0, N_SURFACE)
z_surface = D_CENTER + PAYLOAD_RADIUS_M * mu
rho_surface = PAYLOAD_RADIUS_M * np.sqrt(np.maximum(0.0, 1.0 - mu * mu))
a_surface = axial_accel(z_surface, rho_surface)

imin = int(np.argmin(a_surface))
imax = int(np.argmax(a_surface))

SURFACE_MIN = float(a_surface[imin])
SURFACE_MAX = float(a_surface[imax])
SURFACE_MIN_MU = float(mu[imin])

# Write a compact 1001-row view rather than the million-point internal scan.
write_idx = np.linspace(0, N_SURFACE - 1, 1001).astype(int)

with SURFACE_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["mu","z_m","rho_m","axial_accel_mps2"])
    for i in write_idx:
        writer.writerow([
            float(mu[i]),
            float(z_surface[i]),
            float(rho_surface[i]),
            float(a_surface[i]),
        ])

# Independent Gauss-Legendre volume integration for payload CM acceleration.
NS = 180
NMU = 220
xs, ws = leggauss(NS)
xm, wm = leggauss(NMU)

s = 0.5 * PAYLOAD_RADIUS_M * (xs + 1.0)
ws_phys = 0.5 * PAYLOAD_RADIUS_M * ws

cm_integral = 0.0

for sj, wj in zip(s, ws_phys):
    z = D_CENTER + sj * xm
    rho = sj * np.sqrt(np.maximum(0.0, 1.0 - xm * xm))
    az = axial_accel(z, rho)
    cm_integral += (
        2.0 * math.pi
        * sj ** 2
        * wj
        * float(np.sum(wm * az))
    )

payload_volume = 4.0 * math.pi * PAYLOAD_RADIUS_M ** 3 / 3.0
CM_ACCEL = cm_integral / payload_volume

# Exact metric-level diagnostics.
FAR_ACCEL = radial_accel(R_FAR)
NEAR_ACCEL = radial_accel(R_NEAR)
PSI_SOURCE_SURFACE = psi(R_SOURCE)
PSI_PAYLOAD_FAR = psi(R_FAR)
Q_OVER_RFAR2 = Q_REQUIRED / R_FAR ** 2

# Radius where Q/r^3 repulsion and positive-mass 1/r^2 attraction balance.
TURNOVER_RADIUS_M = (
    C ** 2 * Q_REQUIRED / (G * ADM_MASS_KG)
)

# Required effective geometric charge amplitude.
SQRT_Q_REQUIRED_M = math.sqrt(Q_REQUIRED)

# Compare with a canonically normalized positive Maxwell-like RN field.
CANONICAL_OVER_TARGET = E_CANONICAL / ENERGY_TARGET_J

# Equivalently compare Q delivered per joule.
REQUIRED_Q_PER_J = Q_REQUIRED / ENERGY_TARGET_J
CANONICAL_Q_PER_J = (
    2.0 * G * R_SOURCE / C ** 4
)
REQUIRED_EFFICIENCY_ENHANCEMENT = (
    REQUIRED_Q_PER_J / CANONICAL_Q_PER_J
)

# Algebraic stability-sign verification over arbitrary random-looking values.
# The result is actually exact and independent of these values.
w_values = np.logspace(-18.0, 18.0, 10001)
hd_values = np.array([
    dilation_coefficient_from_stability_margin(float(w))
    for w in w_values
])
MIN_HD = float(np.min(hd_values))
ALL_HD_POSITIVE = bool(np.all(hd_values > 0.0))

# Strict stability boundary w=0 gives zero dilation metric charge.
HD_BOUNDARY = dilation_coefficient_from_stability_margin(0.0)

adverse_surface_pass = SURFACE_MIN >= TARGET_ACCEL * (1.0 - 1.0e-10)
cm_pass = CM_ACCEL >= TARGET_ACCEL
positive_adm = ADM_MASS_KG > 0.0
exterior_horizon_free = PSI_SOURCE_SURFACE > 0.0

metric_level_green = (
    adverse_surface_pass
    and cm_pass
    and positive_adm
    and exterior_horizon_free
    and ALL_HD_POSITIVE
)

# No complete source ledger exists yet.
complete_source_ledger = False
certified_sub10mj = False

result = {
    "branch": "032S0_CUBIC_MAG_DILATION_RN_FINITE_PAYLOAD",
    "claim_class": "EXACT_EXTERIOR_METRIC_AND_SOURCE_EFFICIENCY_PREFLIGHT",
    "literature_structure": {
        "cubic_mag_exact_rn_like_solution": True,
        "propagating_torsion_nonmetricity": True,
        "vector_axial_stability_conditions_used": True,
        "dilation_charge_metric_coefficient": (
            "0.5*(2*a6-4*a2-8*a14-d1)"
        ),
        "stability_margin_parameterization": (
            "a14=(2*a6-4*a2-d1)/8-w"
        ),
        "dilation_coefficient_after_substitution": "4*w",
        "strict_stability_margin_repulsive_sign": True,
    },
    "energy_target_j": ENERGY_TARGET_J,
    "positive_adm_energy_j": ADM_ENERGY_J,
    "positive_adm_mass_kg": ADM_MASS_KG,
    "payload_radius_m": PAYLOAD_RADIUS_M,
    "target_acceleration_mps2": TARGET_ACCEL,
    "optimized_source_radius_m": R_SOURCE,
    "zero_gap_infimum": True,
    "payload_center_radius_m": D_CENTER,
    "payload_near_radius_m": R_NEAR,
    "payload_far_radius_m": R_FAR,
    "required_q_metric_m2": Q_REQUIRED,
    "sqrt_required_q_metric_m": SQRT_Q_REQUIRED_M,
    "q_over_rfar_squared": Q_OVER_RFAR2,
    "near_surface_radial_accel_mps2": NEAR_ACCEL,
    "far_surface_radial_accel_mps2": FAR_ACCEL,
    "surface_scan_points": N_SURFACE,
    "surface_min_axial_accel_mps2": SURFACE_MIN,
    "surface_min_mu": SURFACE_MIN_MU,
    "surface_max_axial_accel_mps2": SURFACE_MAX,
    "payload_cm_axial_accel_mps2": CM_ACCEL,
    "psi_source_surface": PSI_SOURCE_SURFACE,
    "psi_payload_far": PSI_PAYLOAD_FAR,
    "positive_adm_mass": positive_adm,
    "exterior_horizon_free": exterior_horizon_free,
    "turnover_to_far_field_attraction_radius_m": TURNOVER_RADIUS_M,
    "finite_payload_metric_level_green": metric_level_green,
    "canonical_maxwell_like_benchmark": {
        "is_cubic_mag_lower_bound": False,
        "optimized_exterior_energy_j": E_CANONICAL,
        "energy_over_10mj": CANONICAL_OVER_TARGET,
        "canonical_q_per_j_m2_per_j": CANONICAL_Q_PER_J,
        "required_q_per_j_m2_per_j": REQUIRED_Q_PER_J,
        "required_efficiency_enhancement": REQUIRED_EFFICIENCY_ENHANCEMENT,
    },
    "source_charge_hamiltonian_derived": False,
    "finite_matter_source_matched_to_exterior": False,
    "source_creation_energy_included": False,
    "support_control_energy_included": False,
    "nonlinear_source_stability_certified": False,
    "complete_operating_ledger": complete_source_ledger,
    "certified_sub10mj_model": certified_sub10mj,
    "full_cubic_mag_family_closed": False,
    "decision": (
        "GREEN_EXACT_METRIC_REPULSION_SOURCE_LEDGER_OPEN"
        if metric_level_green
        else "RED_METRIC_LEVEL"
    ),
    "next": (
        "032S1_CUBIC_MAG_DILATION_CHARGE_HAMILTONIAN_SOURCE_LEDGER"
        if metric_level_green
        else "GLOBAL_RERANK"
    ),
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032S0 RESULT ===")
print("DILATION_COEFF_STABILITY_FORM=4*w")
print("DILATION_COEFF_STRICT_MARGIN_POSITIVE=" + str(ALL_HD_POSITIVE))
print("DILATION_COEFF_BOUNDARY_W0=" + format(HD_BOUNDARY, ".12e"))
print("POSITIVE_ADM_MASS_KG=" + format(ADM_MASS_KG, ".12e"))
print("OPT_SOURCE_RADIUS_M=" + format(R_SOURCE, ".12e"))
print("PAYLOAD_FAR_RADIUS_M=" + format(R_FAR, ".12e"))
print("REQUIRED_Q_METRIC_M2=" + format(Q_REQUIRED, ".12e"))
print("SQRT_REQUIRED_Q_M=" + format(SQRT_Q_REQUIRED_M, ".12e"))
print("Q_OVER_RFAR2=" + format(Q_OVER_RFAR2, ".12e"))
print("FAR_SURFACE_ACCEL=" + format(FAR_ACCEL, ".12e"))
print("SURFACE_MIN_ACCEL=" + format(SURFACE_MIN, ".12e"))
print("SURFACE_MIN_MU=" + format(SURFACE_MIN_MU, ".12e"))
print("PAYLOAD_CM_ACCEL=" + format(CM_ACCEL, ".12e"))
print("PSI_SOURCE_SURFACE=" + format(PSI_SOURCE_SURFACE, ".16e"))
print("TURNOVER_RADIUS_M=" + format(TURNOVER_RADIUS_M, ".12e"))
print("POSITIVE_FAR_FIELD_ACTIVE_MASS=YES")
print("FINITE_PAYLOAD_METRIC_LEVEL_GREEN=" + str(metric_level_green))
print("CANONICAL_MAXWELL_LIKE_BENCHMARK_J=" + format(E_CANONICAL, ".12e"))
print("CANONICAL_BENCHMARK_OVER_10MJ=" + format(CANONICAL_OVER_TARGET, ".12e"))
print("REQUIRED_CHARGE_PER_J_ENHANCEMENT=" + format(REQUIRED_EFFICIENCY_ENHANCEMENT, ".12e"))
print("CANONICAL_BENCHMARK_IS_CUBIC_MAG_BOUND=NO")
print("SOURCE_CHARGE_HAMILTONIAN_DERIVED=NO")
print("FINITE_SOURCE_MATCHING_COMPLETED=NO")
print("COMPLETE_OPERATING_LEDGER=NO")
print("CERTIFIED_SUB10MJ_MODEL=NO")
print("FULL_CUBIC_MAG_FAMILY_CLOSED=NO")
print("DECISION=" + result["decision"])
print("NEXT=" + result["next"])
