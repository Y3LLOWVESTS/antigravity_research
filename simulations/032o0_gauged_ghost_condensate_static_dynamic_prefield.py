"""
032O0 — gauged ghost-condensate static/dynamic prefield gate.

Published low-energy longitudinal/gravity quadratic action:

  L = 1/2 (sigma H) K (sigma H)^T

  K11 = omega^2 k^2 - alpha g^2 k^4
  K12 = -i epsilon omega k^2
  K22 = -k^2 (1-epsilon^2)

with

  epsilon = M / (sqrt(2) g Mpl).

The corresponding H propagator contains

  R(omega,k) =
    1 - alpha g^2 epsilon^2 k^2
        / [omega^2 - alpha g^2 (1-epsilon^2) k^2].

At omega=0:

  R_static = 1/(1-epsilon^2).

Thus every healthy point epsilon^2<1 keeps the static sign attractive.

Immediately above the longitudinal pole, R can reverse sign, but only
within a narrow frequency band.

This run measures the largest possible reversal bandwidth subject to the
published optimistic phenomenological bound

  M < min(1e12 GeV, g^2 1e15 GeV).

It deliberately does NOT port the ungauged ghost-condensate charge/energy
relation to the gauged theory. A dynamic sign window is therefore only a
response-level signal, not an energy-qualified source or field solution.
"""

from __future__ import annotations

import csv
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import qmc


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "data" / "032o0_gauged_ghost_condensate_static_dynamic_prefield_summary.json"
TOP_OUT = ROOT / "results" / "data" / "032o0_gauged_ghost_dynamic_top_candidates.csv"

SAMPLES = 10_000_000
CHUNK = 250_000
TOP_KEEP = 100

C = 299792458.0
MPL_GEV = 2.435e18

PAYLOAD_RADIUS_M = 0.10
DEVICE_SCALE_M = 2.0 * PAYLOAD_RADIUS_M
TARGET_ACCEL = 9.80665
ENERGY_TARGET_J = 1.0e7

# Dimensionless Newtonian-potential scale needed for ~1g over 20 cm.
PHI_TARGET = TARGET_ACCEL * DEVICE_SCALE_M / C ** 2
SQRT_PHI_TARGET = math.sqrt(PHI_TARGET)

# Search domains.
LOG10_G_MIN = math.log10(max(1.0e-9, SQRT_PHI_TARGET * 1.000001))
LOG10_G_MAX = 0.0
LOG10_M_FRACTION_MIN = -12.0
LOG10_M_FRACTION_MAX = 0.0
LOG10_ALPHA_MIN = -2.0
LOG10_ALPHA_MAX = 1.0


def published_mmax_gev(g):
    return np.minimum(1.0e12, g * g * 1.0e15)


def epsilon_value(m_gev, g):
    return m_gev / (math.sqrt(2.0) * g * MPL_GEV)


def static_ratio(epsilon):
    return 1.0 / (1.0 - epsilon * epsilon)


def reversal_fractional_bandwidth(epsilon):
    e2 = epsilon * epsilon
    if e2 <= 0.0 or e2 >= 1.0:
        return 0.0

    # Pole:
    #   omega_p^2 = alpha g^2 (1-e2) k^2.
    #
    # Zero of R above the pole:
    #   omega_zero / omega_p = 1/sqrt(1-e2).
    #
    # R<0 between the pole and this zero.
    return 1.0 / math.sqrt(1.0 - e2) - 1.0


def required_q(epsilon):
    width = reversal_fractional_bandwidth(epsilon)
    if width <= 0.0:
        return float("inf")
    return 1.0 / width


def pole_frequency_hz(g, alpha, epsilon, length_m):
    cs2 = alpha * g * g * (1.0 - epsilon * epsilon)
    if cs2 <= 0.0:
        return float("nan")
    cs = math.sqrt(cs2)
    omega = cs * C / length_m
    return omega / (2.0 * math.pi)


def analytic_eps_at_envelope(log10_g):
    g = 10.0 ** float(log10_g)
    m = min(1.0e12, g * g * 1.0e15)
    eps = epsilon_value(m, g)
    if g <= SQRT_PHI_TARGET:
        return -1.0
    if eps >= 1.0:
        return -1.0
    return eps


opt = minimize_scalar(
    lambda x: -analytic_eps_at_envelope(x),
    bounds=(LOG10_G_MIN, LOG10_G_MAX),
    method="bounded",
    options={"xatol": 1.0e-14},
)

g_opt = 10.0 ** float(opt.x)
m_opt = min(1.0e12, g_opt * g_opt * 1.0e15)
eps_opt = epsilon_value(m_opt, g_opt)
width_opt = reversal_fractional_bandwidth(eps_opt)
q_opt = required_q(eps_opt)

# Exact cusp where the two published M bounds meet.
g_cusp = math.sqrt(1.0e12 / 1.0e15)
m_cusp = 1.0e12
eps_cusp = epsilon_value(m_cusp, g_cusp)
width_cusp = reversal_fractional_bandwidth(eps_cusp)
q_cusp = required_q(eps_cusp)

# Reference pole frequency at alpha=1 and payload-diameter scale.
f_cusp_alpha1 = pole_frequency_hz(
    g_cusp,
    1.0,
    eps_cusp,
    DEVICE_SCALE_M,
)
linewidth_cusp_hz = f_cusp_alpha1 * width_cusp

start = time.perf_counter()
sampler = qmc.Sobol(d=3, scramble=True, seed=32040)

top = []
evaluated = 0
healthy = 0
static_reversal = 0
dynamic_window = 0

print("=== 032O0 TEN-MILLION FRONTIER ===")
print("LOG10_G_RANGE=" + str((LOG10_G_MIN, LOG10_G_MAX)))
print("PUBLISHED_M_BOUND=MIN_1E12_GEV_OR_G2_1E15_GEV")
print("SQRT_PHI_TARGET=" + format(SQRT_PHI_TARGET, ".12e"))

while evaluated < SAMPLES:
    count = min(CHUNK, SAMPLES - evaluated)
    u = sampler.random(count)

    logg = LOG10_G_MIN + u[:, 0] * (LOG10_G_MAX - LOG10_G_MIN)
    g = 10.0 ** logg

    mmax = published_mmax_gev(g)
    log_fraction = (
        LOG10_M_FRACTION_MIN
        + u[:, 1]
        * (LOG10_M_FRACTION_MAX - LOG10_M_FRACTION_MIN)
    )
    m = mmax * 10.0 ** log_fraction

    logalpha = (
        LOG10_ALPHA_MIN
        + u[:, 2]
        * (LOG10_ALPHA_MAX - LOG10_ALPHA_MIN)
    )
    alpha = 10.0 ** logalpha

    eps = m / (math.sqrt(2.0) * g * MPL_GEV)
    eps2 = eps * eps
    cs2 = alpha * g * g * (1.0 - eps2)

    good = (
        (g > SQRT_PHI_TARGET)
        & (eps2 < 1.0)
        & (cs2 > 0.0)
        & (cs2 <= 1.0)
    )

    healthy += int(np.count_nonzero(good))

    rstatic = np.full(count, np.nan)
    rstatic[good] = 1.0 / (1.0 - eps2[good])

    static_reversal += int(
        np.count_nonzero(good & (rstatic < 0.0))
    )

    width = np.zeros(count)
    width[good] = (
        1.0 / np.sqrt(1.0 - eps2[good]) - 1.0
    )

    dyn = good & (width > 0.0)
    dynamic_window += int(np.count_nonzero(dyn))

    q = np.full(count, np.inf)
    q[dyn] = 1.0 / width[dyn]

    local_keep = min(TOP_KEEP, count)
    idx = np.argpartition(q, local_keep - 1)[:local_keep]

    for i in idx:
        if not math.isfinite(float(q[i])):
            continue

        f_ref = pole_frequency_hz(
            float(g[i]),
            float(alpha[i]),
            float(eps[i]),
            DEVICE_SCALE_M,
        )

        top.append(
            {
                "sample_index": evaluated + int(i),
                "g": float(g[i]),
                "m_gev": float(m[i]),
                "mmax_gev": float(mmax[i]),
                "alpha": float(alpha[i]),
                "epsilon": float(eps[i]),
                "static_response_ratio": float(rstatic[i]),
                "reversal_fractional_bandwidth": float(width[i]),
                "required_q": float(q[i]),
                "pole_frequency_hz_20cm": float(f_ref),
                "linewidth_hz_20cm": float(f_ref * width[i]),
            }
        )

    top.sort(
        key=lambda row: (
            row["required_q"],
            -row["epsilon"],
            row["sample_index"],
        )
    )
    del top[TOP_KEEP:]

    evaluated += count

    if evaluated % 1_000_000 == 0 or evaluated == SAMPLES:
        best_q = top[0]["required_q"] if top else float("inf")
        print(
            "PROGRESS"
            + " evaluated=" + str(evaluated)
            + " static_reversal=" + str(static_reversal)
            + " best_required_q=" + format(best_q, ".12e"),
            flush=True,
        )

elapsed = time.perf_counter() - start

best = top[0]

# Static result is exact, not statistical.
static_healthy_sign_reversal_possible = False

# This is a response-level resonance only. No source-energy claim.
dynamic_response_sign_reversal_possible = width_cusp > 0.0

# A Q this large is not itself a theorem-level failure, but it must be
# carried into the next source/damping/control-energy gate.
if dynamic_response_sign_reversal_possible:
    decision = "STATIC_BRANCH_RED_DYNAMIC_RESONANT_BRANCH_OPEN"
    next_step = "032O1_FINITE_DURATION_DAMPING_SOURCE_ENERGY_GATE"
else:
    decision = "GAUGED_LINEAR_BRANCH_RED"
    next_step = "RERANK_FRONTIER"

with TOP_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(top[0].keys()))
    writer.writeheader()
    writer.writerows(top)

result = {
    "branch": "032O0_GAUGED_GHOST_CONDENSATE_PREFIELD",
    "claim_class": "LINEAR_PROPAGATOR_STATIC_DYNAMIC_PREFIELD",
    "literature_action_reconstructed": True,
    "ungauged_charge_energy_law_reused": False,
    "samples": SAMPLES,
    "healthy_samples": healthy,
    "payload_radius_m": PAYLOAD_RADIUS_M,
    "device_scale_m": DEVICE_SCALE_M,
    "target_acceleration_mps2": TARGET_ACCEL,
    "target_dimensionless_phi": PHI_TARGET,
    "sqrt_phi_target": SQRT_PHI_TARGET,
    "published_parameter_bound": "M_LT_MIN_1E12_GEV_G2_1E15_GEV",
    "static": {
        "response_ratio_formula": "1/(1-epsilon^2)",
        "healthy_requires_epsilon2_lt_1": True,
        "sampled_sign_reversals": static_reversal,
        "healthy_static_sign_reversal_possible": static_healthy_sign_reversal_possible,
        "interpretation": "STATIC_LIMIT_ONLY_RENORMALIZES_NEWTON_CONSTANT",
    },
    "dynamic": {
        "pole_formula": "omega2=alpha*g2*(1-epsilon2)*k2",
        "sign_reversal_above_pole": dynamic_response_sign_reversal_possible,
        "analytic_max_epsilon": eps_cusp,
        "analytic_max_fractional_bandwidth": width_cusp,
        "analytic_min_required_q": q_cusp,
        "analytic_opt_g": g_cusp,
        "analytic_opt_m_gev": m_cusp,
        "alpha1_pole_frequency_hz_20cm": f_cusp_alpha1,
        "alpha1_reversal_linewidth_hz_20cm": linewidth_cusp_hz,
        "numeric_optimizer_g": g_opt,
        "numeric_optimizer_m_gev": m_opt,
        "numeric_optimizer_epsilon": eps_opt,
        "numeric_optimizer_bandwidth": width_opt,
        "numeric_optimizer_q": q_opt,
        "best_sobol": best,
    },
    "dynamic_source_energy_computed": False,
    "finite_duration_computed": False,
    "damping_computed": False,
    "radiation_computed": False,
    "complete_operating_ledger": False,
    "field_solution": False,
    "certified_antigravity_model": False,
    "full_gauged_ghost_condensate_family_closed": False,
    "decision": decision,
    "next": next_step,
    "seconds": elapsed,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("")
print("=== 032O0 RESULT ===")
print("SAMPLES=" + str(SAMPLES))
print("HEALTHY_SAMPLES=" + str(healthy))
print("STATIC_SIGN_REVERSALS=" + str(static_reversal))
print("STATIC_HEALTHY_SIGN_REVERSAL_POSSIBLE=False")
print("STATIC_RESULT=ATTRACTIVE_G_RENORMALIZATION_ONLY")
print("ANALYTIC_OPT_G=" + format(g_cusp, ".12e"))
print("ANALYTIC_OPT_M_GEV=" + format(m_cusp, ".12e"))
print("ANALYTIC_MAX_EPSILON=" + format(eps_cusp, ".12e"))
print("ANALYTIC_MAX_REVERSAL_BANDWIDTH=" + format(width_cusp, ".12e"))
print("ANALYTIC_MIN_REQUIRED_Q=" + format(q_cusp, ".12e"))
print("ALPHA1_POLE_FREQUENCY_HZ_20CM=" + format(f_cusp_alpha1, ".12e"))
print("ALPHA1_LINEWIDTH_HZ_20CM=" + format(linewidth_cusp_hz, ".12e"))
print("SOBOL_BEST_Q=" + format(best["required_q"], ".12e"))
print("SOBOL_BEST_G=" + format(best["g"], ".12e"))
print("SOBOL_BEST_M_GEV=" + format(best["m_gev"], ".12e"))
print("UNGAUGED_M4_ENERGY_SCALING_PORTED=NO")
print("DYNAMIC_SOURCE_ENERGY_COMPUTED=NO")
print("COMPLETE_OPERATING_LEDGER=NO")
print("CERTIFIED_ANTIGRAVITY_MODEL=NO")
print("FULL_GAUGED_GHOST_CONDENSATE_FAMILY_CLOSED=NO")
print("DECISION=" + decision)
print("NEXT=" + next_step)
