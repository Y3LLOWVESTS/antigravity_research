"""
032N1 — minimal ghost-condensate one-sided continuum morphology bound.

For small ghost-condensate fluctuations:

    E_pp density = T00^2 / (2 kappa^2 M^4)

while gravitational acceleration is linear in T00.

Writing q >= 0 for the magnitude of negative active mass density,

    E_pp = beta integral q^2 dV

and at a payload point

    a_z = G integral q K_z dV.

Cauchy-Schwarz gives

    integral q^2 dV >= (a/G)^2 / integral K_z^2 dV.

For the complete one-sided half-space below a plane, with the adverse
far payload surface a height h above that plane,

    integral_halfspace K_z^2 dV = pi / (2 h).

This is a global morphology infimum for the declared branch.

It is deliberately over-favorable:
  - zero source/payload gap is allowed as an infimum;
  - the source may extend to infinite radius and depth;
  - only the necessary far-surface vertical-acceleration constraint is used;
  - localization, creation, compensation, support and control are omitted;
  - positive far-field active-mass restoration is omitted.

Therefore failure of this floor decisively removes morphology-only rescue
for the declared minimal one-sided small-fluctuation branch.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from scipy.integrate import quad


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "data" / "032n1_ghost_condensate_halfspace_continuum_bound_summary.json"
SCAN = ROOT / "results" / "data" / "032n1_halfspace_convergence.csv"
N0 = ROOT / "results" / "data" / "032n0_ghost_condensate_charge_energy_prefield_summary.json"

G = 6.67430e-11
C = 299792458.0
HBARC_GEV_M = 1.973269804e-16
GEV_TO_J = 1.602176634e-10
GEV4_TO_J_M3 = GEV_TO_J / HBARC_GEV_M ** 3

M_GEV = 100.0
KAPPA_MAX = 10.0
KAPPA_REFERENCE = 1.0

PAYLOAD_RADIUS_M = 0.10
PAYLOAD_DIAMETER_M = 2.0 * PAYLOAD_RADIUS_M
TARGET_ACCEL = 9.80665
ENERGY_TARGET_J = 1.0e7

# Zero gap is the most favorable one-sided non-overlap infimum.
H_M = PAYLOAD_DIAMETER_M


def beta_j_m3_per_kg2(m_gev, kappa):
    return (
        C ** 4
        / (
            2.0
            * kappa ** 2
            * m_gev ** 4
            * GEV4_TO_J_M3
        )
    )


def kernel_l2_exact(h_m):
    return math.pi / (2.0 * h_m)


def energy_bound_j(m_gev, kappa, h_m):
    beta = beta_j_m3_per_kg2(m_gev, kappa)
    kernel_l2 = kernel_l2_exact(h_m)
    return beta * (TARGET_ACCEL / G) ** 2 / kernel_l2


def radial_integral_closed(a_m, radius_m):
    return (
        math.pi
        / 2.0
        * (
            1.0 / a_m ** 2
            - a_m ** 2 / (a_m ** 2 + radius_m ** 2) ** 2
        )
    )


def kernel_l2_finite(radius_m, depth_m, h_m):
    value, error = quad(
        lambda s: radial_integral_closed(h_m + s, radius_m),
        0.0,
        depth_m,
        epsabs=1.0e-13,
        epsrel=1.0e-12,
        limit=400,
    )
    return value, error


def kernel_l1_finite(radius_m, depth_m, h_m):
    def integrand(s):
        a = h_m + s
        return 2.0 * math.pi * (
            1.0 - a / math.sqrt(a * a + radius_m * radius_m)
        )

    value, error = quad(
        integrand,
        0.0,
        depth_m,
        epsabs=1.0e-12,
        epsrel=1.0e-11,
        limit=400,
    )
    return value, error


def direct_double_kernel_l2(radius_m, depth_m, h_m):
    def outer(s):
        a = h_m + s
        inner, _ = quad(
            lambda r: (
                2.0
                * math.pi
                * r
                * a ** 2
                / (r * r + a * a) ** 3
            ),
            0.0,
            radius_m,
            epsabs=1.0e-12,
            epsrel=1.0e-10,
            limit=300,
        )
        return inner

    value, error = quad(
        outer,
        0.0,
        depth_m,
        epsabs=1.0e-11,
        epsrel=1.0e-9,
        limit=300,
    )
    return value, error


i_exact = kernel_l2_exact(H_M)
e_floor_k10 = energy_bound_j(M_GEV, KAPPA_MAX, H_M)
e_floor_k1 = energy_bound_j(M_GEV, KAPPA_REFERENCE, H_M)

ratio_to_target_k10 = e_floor_k10 / ENERGY_TARGET_J
ratio_to_target_k1 = e_floor_k1 / ENERGY_TARGET_J

kappa_required = KAPPA_MAX * math.sqrt(
    e_floor_k10 / ENERGY_TARGET_J
)

m_required_k10 = M_GEV * (
    e_floor_k10 / ENERGY_TARGET_J
) ** 0.25

m_required_k1 = M_GEV * (
    e_floor_k1 / ENERGY_TARGET_J
) ** 0.25

# Exact minimum-norm profile for the single far-surface constraint:
# q(x) = lambda K(x).
lambda_opt = (TARGET_ACCEL / G) / i_exact
qmax_kg_m3 = lambda_opt / H_M ** 2

t00_max_j_m3 = qmax_kg_m3 * C ** 2
t00_max_gev4 = t00_max_j_m3 / GEV4_TO_J_M3
pi_dot_max_gev2 = t00_max_gev4 / (KAPPA_MAX * M_GEV ** 2)
small_fluctuation_ratio = pi_dot_max_gev2 / M_GEV ** 2
derivative_ratio = HBARC_GEV_M / (H_M * M_GEV)

boxes = [
    0.25,
    0.50,
    1.0,
    2.0,
    4.0,
    8.0,
    16.0,
    32.0,
]

rows = []

for extent in boxes:
    i_box, i_err = kernel_l2_finite(extent, extent, H_M)
    j_box, j_err = kernel_l1_finite(extent, extent, H_M)

    e_box = (
        beta_j_m3_per_kg2(M_GEV, KAPPA_MAX)
        * (TARGET_ACCEL / G) ** 2
        / i_box
    )

    lambda_box = (TARGET_ACCEL / G) / i_box
    active_mass_box = lambda_box * j_box

    rows.append(
        {
            "extent_m": extent,
            "kernel_l2": i_box,
            "kernel_l2_rel_to_exact": i_box / i_exact,
            "energy_j": e_box,
            "energy_rel_to_exact": e_box / e_floor_k10,
            "active_mass_abs_kg": active_mass_box,
            "kernel_l2_quad_error": i_err,
            "kernel_l1_quad_error": j_err,
        }
    )

direct_i, direct_err = direct_double_kernel_l2(2.0, 2.0, H_M)
closed_i_2m, _ = kernel_l2_finite(2.0, 2.0, H_M)
direct_relerr = abs(direct_i - closed_i_2m) / closed_i_2m

n0 = None
n0_uniform_best_j = None
n0_uniform_k1_j = None
n0_to_continuum_gain = None

if N0.exists():
    n0 = json.loads(N0.read_text(encoding="utf-8"))
    n0_uniform_best_j = float(
        n0["continuous_optimization"]["energy_j"]
    )
    n0_uniform_k1_j = float(
        n0["order_unity_kappa_same_geometry_energy_j"]
    )
    n0_to_continuum_gain = n0_uniform_best_j / e_floor_k10

geometry_rescue_to_target_possible = e_floor_k10 < ENERGY_TARGET_J

declared_minimal_branch_closed = (
    not geometry_rescue_to_target_possible
    and M_GEV <= 100.0
    and KAPPA_MAX <= 10.0
)

with SCAN.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

result = {
    "branch": "032N1_GHOST_CONDENSATE_ONE_SIDED_CONTINUUM_BOUND",
    "claim_class": "ANALYTIC_CONTINUUM_ENERGY_LOWER_BOUND",
    "theory_scope": (
        "MINIMAL_SMALL_FLUCTUATION_GHOST_CONDENSATE_ONE_SIDED_HALFSPACE"
    ),
    "payload_radius_m": PAYLOAD_RADIUS_M,
    "far_surface_height_zero_gap_infimum_m": H_M,
    "target_acceleration_mps2": TARGET_ACCEL,
    "energy_target_j": ENERGY_TARGET_J,
    "strict_lt_target": True,
    "m_gev": M_GEV,
    "kappa_max": KAPPA_MAX,
    "kernel_l2_exact": i_exact,
    "global_halfspace_floor_kappa10_j": e_floor_k10,
    "global_halfspace_floor_kappa1_j": e_floor_k1,
    "floor_over_target_kappa10": ratio_to_target_k10,
    "floor_over_target_kappa1": ratio_to_target_k1,
    "required_kappa_at_m100gev_for_10mj": kappa_required,
    "required_m_gev_at_kappa10_for_10mj": m_required_k10,
    "required_m_gev_at_kappa1_for_10mj": m_required_k1,
    "optimal_profile_qmax_kg_m3": qmax_kg_m3,
    "small_fluctuation_pi_dot_over_m2_max": small_fluctuation_ratio,
    "derivative_ratio_1_over_hm": derivative_ratio,
    "finite_box_convergence": rows,
    "independent_2m_double_integral": {
        "direct": direct_i,
        "closed_radial": closed_i_2m,
        "relative_error": direct_relerr,
        "quad_error": direct_err,
    },
    "n0_uniform_best_kappa10_j": n0_uniform_best_j,
    "n0_uniform_same_geometry_kappa1_j": n0_uniform_k1_j,
    "maximum_morphology_gain_vs_n0_uniform": n0_to_continuum_gain,
    "geometry_only_rescue_to_sub10mj_possible": geometry_rescue_to_target_possible,
    "minimal_m_le_100gev_kappa_le_10_one_sided_branch_closed": declared_minimal_branch_closed,
    "optimistic_features": [
        "zero_gap_infimum",
        "infinite_source_extent_allowed",
        "only_far_surface_necessary_constraint_used",
        "negative_active_mass_compensation_omitted",
        "localization_energy_omitted",
        "generator_energy_omitted",
        "support_control_energy_omitted",
        "nonlinear_backreaction_omitted",
    ],
    "field_solution": False,
    "complete_operating_ledger": False,
    "full_ghost_condensate_family_closed": False,
    "next": (
        "032O_GAUGED_GHOST_CONDENSATE_PREFIELD"
        if declared_minimal_branch_closed
        else "032N2_FULL_FINITE_PAYLOAD_VARIATIONAL_RECONSTRUCTION"
    ),
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032N1 CONTINUUM BOUND ===")
print("KERNEL_L2_EXACT=" + format(i_exact, ".12e"))
print("GLOBAL_FLOOR_KAPPA10_J=" + format(e_floor_k10, ".12e"))
print("GLOBAL_FLOOR_KAPPA10_MJ=" + format(e_floor_k10 / 1.0e6, ".12e"))
print("GLOBAL_FLOOR_KAPPA1_J=" + format(e_floor_k1, ".12e"))
print("FLOOR_OVER_TARGET_KAPPA10=" + format(ratio_to_target_k10, ".12e"))
print("REQUIRED_KAPPA_M100GEV=" + format(kappa_required, ".12e"))
print("REQUIRED_M_GEV_KAPPA10=" + format(m_required_k10, ".12e"))
print("REQUIRED_M_GEV_KAPPA1=" + format(m_required_k1, ".12e"))
print("QMAX_KG_M3=" + format(qmax_kg_m3, ".12e"))
print("PI_DOT_OVER_M2_MAX=" + format(small_fluctuation_ratio, ".12e"))
print("DERIVATIVE_RATIO=" + format(derivative_ratio, ".12e"))
print("DIRECT_2M_INTEGRAL_RELERR=" + format(direct_relerr, ".12e"))

if n0_to_continuum_gain is not None:
    print("N0_UNIFORM_TO_GLOBAL_MORPHOLOGY_GAIN_MAX=" + format(n0_to_continuum_gain, ".12e"))

print("GEOMETRY_ONLY_RESCUE_TO_SUB10MJ=" + str(geometry_rescue_to_target_possible))
print("MINIMAL_MLE100GEV_KAPPALE10_ONE_SIDED_BRANCH_CLOSED=" + str(declared_minimal_branch_closed))
print("FIELD_SOLUTION=NO")
print("COMPLETE_OPERATING_LEDGER=NO")
print("FULL_GHOST_CONDENSATE_FAMILY_CLOSED=NO")
print("NEXT=" + result["next"])
