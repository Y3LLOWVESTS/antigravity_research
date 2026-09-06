"""
032B1 — Universal-metric quadratic-twin pNGB analytic gate.

Claim class
-----------
Analytic pre-field falsification.

This run does not solve nonlinear field equations and does not certify
an antigravity source.

It combines the published quadratic-twin one-loop mass correction with
the additional ANTIGRAVITY_RESEARCH requirement that visible neutral
matter responds through one universal Jordan metric.

The simple reciprocal twin-matter source is tested first because it is
the cheapest realization to falsify.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import sympy as sp

from antigravity_research.agminer.policy import current_energy_policy


# Physical constants.
MPL_REDUCED_GEV = 2.435e18
TOP_MASS_GEV = 172.76
CUTOFF_GEV = 1.0e4
HBAR_C_EV_M = 1.973269804e-7
G_NEWTON = 6.67430e-11
C_LIGHT = 299792458.0
G_STANDARD = 9.80665

# Historical scalar range used by the strongest 031 realization.
RANGE_M = 3.3

# Favorable point-source scout separation.
SEPARATION_M = 1.0


policy = current_energy_policy()
energy_limit_j = float(policy["limit_j"])

# Use the formal boundary value as an optimistic upper bound even though
# the current LT policy requires strictly less energy.
source_energy_j = energy_limit_j
source_mass_kg = source_energy_j / C_LIGHT ** 2

# ------------------------------------------------------------------
# Exact mirror embedding identities.
# ------------------------------------------------------------------

theta, kappa = sp.symbols("theta kappa", real=True)

sigma_visible_sq = sp.sin(theta) ** 2
sigma_twin_sq = sp.cos(theta) ** 2

A_visible = sp.exp(kappa * sigma_visible_sq)
A_twin = sp.exp(kappa * sigma_twin_sq)

mirror_sum = sp.simplify(
    sigma_visible_sq + sigma_twin_sq
)

mirror_swap_visible = sp.simplify(
    sigma_visible_sq.subs(
        theta,
        sp.pi / 2 - theta,
    )
    - sigma_twin_sq
)

mirror_swap_twin = sp.simplify(
    sigma_twin_sq.subs(
        theta,
        sp.pi / 2 - theta,
    )
    - sigma_visible_sq
)

metric_positive = True
mirror_identity_green = (
    mirror_sum == 1
    and mirror_swap_visible == 0
    and mirror_swap_twin == 0
)

# ------------------------------------------------------------------
# Match universal metric coupling to published d^(2) normalization.
#
# Near phi=0:
#   delta m / m = kappa phi^2/f^2
# while the quadratic-twin normalization gives
#   delta m / m = d2 phi^2/(2 Mpl^2).
# Therefore
#   d2 = 2 kappa Mpl^2/f^2.
#
# Published twin result:
#   delta m_phi^2 =
#       d2^2 mpsi^2 f^2 Lambda^2 /(16 pi^2 Mpl^4).
#
# Substitution gives
#   delta m_phi =
#       |kappa| mpsi Lambda /(2 pi f).
#
# At arbitrary operating angle:
#   alpha_vis =
#       Mpl kappa sin(2 theta)/f.
#
# Hence, using |sin(2 theta)| <= 1:
#   delta m_phi >=
#       |alpha_vis| mpsi Lambda /(2 pi Mpl).
# ------------------------------------------------------------------

mediator_mass_target_ev = HBAR_C_EV_M / RANGE_M

loop_mass_per_alpha_ev = (
    TOP_MASS_GEV
    * CUTOFF_GEV
    / (2.0 * math.pi * MPL_REDUCED_GEV)
    * 1.0e9
)

alpha_naturalness_max = (
    mediator_mass_target_ev
    / loop_mass_per_alpha_ev
)

# Most favorable operating angle sin(2 theta)=1.
alpha_visible_max = alpha_naturalness_max
alpha_twin_max = -alpha_naturalness_max

# Standard Einstein-frame scalar-tensor normalization:
# |F_scalar/F_Newton| = 2 |alpha_source alpha_payload|.
force_ratio_max = (
    2.0
    * abs(alpha_visible_max * alpha_twin_max)
)

# Yukawa force factor for range lambda:
# (1 + r/lambda) exp(-r/lambda).
yukawa_factor = (
    (1.0 + SEPARATION_M / RANGE_M)
    * math.exp(-SEPARATION_M / RANGE_M)
)

newton_accel_from_source = (
    G_NEWTON
    * source_mass_kg
    / SEPARATION_M ** 2
)

max_repulsive_accel = (
    force_ratio_max
    * newton_accel_from_source
    * yukawa_factor
)

acceleration_shortfall = (
    G_STANDARD / max_repulsive_accel
)

energy_required_j = (
    source_energy_j
    * acceleration_shortfall
)

alpha_required_at_energy_limit = math.sqrt(
    G_STANDARD
    * SEPARATION_M ** 2
    / (
        2.0
        * G_NEWTON
        * source_mass_kg
        * yukawa_factor
    )
)

alpha_gap = (
    alpha_required_at_energy_limit
    / alpha_visible_max
)

# ------------------------------------------------------------------
# Decisions.
# ------------------------------------------------------------------

naturalness_formula_finite = (
    math.isfinite(alpha_naturalness_max)
    and alpha_naturalness_max > 0.0
)

simple_twin_source_pass = (
    max_repulsive_accel >= G_STANDARD
)

simple_twin_source_decision = (
    "GREEN"
    if simple_twin_source_pass
    else "RED_ENERGY_AND_CHARGE_PER_JOULE"
)

# Failure of simple twin matter does not prove every nonlinear
# pNGB configuration impossible.
full_032b_family_closed = False

field_solver_authorized = False

if simple_twin_source_pass:
    next_step = (
        "032B2_COMPLETE_SOURCE_LEDGER_BEFORE_FIELD_SOLVE"
    )
else:
    next_step = (
        "032B2_ANALYTIC_NONLINEAR_FIELD_CHARGE_PER_JOULE_BOUND"
    )

result = {
    "branch": "032B1",
    "claim_class": "ANALYTIC_PRE_FIELD_FALSIFICATION",
    "energy_policy_id": str(policy["policy_id"]),
    "energy_limit_j": energy_limit_j,
    "energy_comparison": str(policy["comparison"]),
    "range_m": RANGE_M,
    "separation_m": SEPARATION_M,
    "mediator_mass_target_ev": mediator_mass_target_ev,
    "top_mass_gev": TOP_MASS_GEV,
    "cutoff_gev": CUTOFF_GEV,
    "mirror_identity_green": bool(mirror_identity_green),
    "metric_factor_positive": bool(metric_positive),
    "loop_mass_per_alpha_ev": loop_mass_per_alpha_ev,
    "alpha_visible_naturalness_max": alpha_visible_max,
    "alpha_twin_naturalness_max": alpha_twin_max,
    "force_ratio_to_newton_max": force_ratio_max,
    "yukawa_factor_at_1m": yukawa_factor,
    "source_mass_equivalent_kg_at_limit": source_mass_kg,
    "max_repulsive_accel_mps2": max_repulsive_accel,
    "target_accel_mps2": G_STANDARD,
    "acceleration_shortfall_x": acceleration_shortfall,
    "energy_required_j_point_source_optimistic": energy_required_j,
    "alpha_required_at_energy_limit": alpha_required_at_energy_limit,
    "alpha_required_over_naturalness_max": alpha_gap,
    "simple_reciprocal_twin_matter_source": simple_twin_source_decision,
    "full_032b_family_closed": full_032b_family_closed,
    "field_solver_authorized": field_solver_authorized,
    "next": next_step,
}

output = Path(
    "results/data/032b1_metric_twin_naturalness_charge_summary.json"
)

output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032B1 UNIVERSAL-METRIC TWIN NATURALNESS / CHARGE GATE ===")
print("CLAIM_CLASS=ANALYTIC_PRE_FIELD_FALSIFICATION")
print("REAL_FIELD_SOLUTION=NO")
print("MIRROR_IDENTITY=" + str(mirror_identity_green))
print("METRIC_FACTOR_POSITIVE=" + str(metric_positive))
print("RANGE_M=" + str(RANGE_M))
print("MEDIATOR_MASS_TARGET_EV=" + format(mediator_mass_target_ev, ".12e"))
print("TOP_MASS_GEV=" + str(TOP_MASS_GEV))
print("CUTOFF_GEV=" + str(CUTOFF_GEV))
print("LOOP_MASS_PER_ALPHA_EV=" + format(loop_mass_per_alpha_ev, ".12e"))
print("ALPHA_VISIBLE_NATURALNESS_MAX=" + format(alpha_visible_max, ".12e"))
print("ALPHA_TWIN_NATURALNESS_MAX=" + format(alpha_twin_max, ".12e"))
print("MAX_FORCE_RATIO_TO_NEWTON=" + format(force_ratio_max, ".12e"))
print("YUKAWA_FACTOR_AT_1M=" + format(yukawa_factor, ".12e"))
print("SOURCE_ENERGY_BOUND_J=" + format(source_energy_j, ".12e"))
print("MAX_REPULSIVE_ACCEL_MPS2=" + format(max_repulsive_accel, ".12e"))
print("TARGET_ACCEL_MPS2=" + format(G_STANDARD, ".12e"))
print("ACCELERATION_SHORTFALL_X=" + format(acceleration_shortfall, ".12e"))
print("ENERGY_REQUIRED_J_OPTIMISTIC=" + format(energy_required_j, ".12e"))
print("ALPHA_REQUIRED_AT_ENERGY_LIMIT=" + format(alpha_required_at_energy_limit, ".12e"))
print("ALPHA_REQUIRED_OVER_NATURALNESS_MAX=" + format(alpha_gap, ".12e"))
print("SIMPLE_RECIPROCAL_TWIN_MATTER_SOURCE=" + simple_twin_source_decision)
print("FULL_032B_FAMILY_CLOSED=" + str(full_032b_family_closed))
print("FIELD_SOLVER_AUTHORIZED=" + str(field_solver_authorized))
print("NEXT=" + next_step)
