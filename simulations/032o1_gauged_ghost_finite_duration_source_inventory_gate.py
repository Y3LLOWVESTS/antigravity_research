"""
032O1 — finite-duration source-inventory gate for the published linear
gauged-ghost-condensate metric resonance.

Scope:
  ordinary positive-energy external source coupled through T00,
  one coherent longitudinal mode,
  linear gauged-ghost propagator,
  finite 0.10-m-radius payload,
  strict total source inventory below 10 MJ.

From the published propagator,

  R(omega,k)
    = 1 - A / (omega^2 - omega_p^2),

  A = alpha g^2 epsilon^2 c^2 k^2,

  omega_p^2
    = alpha g^2 (1-epsilon^2) c^2 k^2.

The resonant correction obeys the forced-oscillator equation.
For any bounded drive whose Fourier-mode source amplitude never exceeds
the source amplitude used to define the ordinary Newtonian field,
zero damping and zero initial excitation give the absolute time-domain bound

  |Delta R(T)|
    <= [epsilon^2/(1-epsilon^2)] omega_p T.

This is intentionally over-favorable.

Additional optimistic assumptions:
  - all 10 MJ may be ordinary source rest energy;
  - zero source/payload gap;
  - point-source kernel used at the adverse far payload surface;
  - no kinetic energy is charged for source motion;
  - no generator/control energy;
  - no damping or radiation;
  - perfect phase and frequency control;
  - no nonlinear saturation;
  - causal-oracle comparison permits cs=c even when that requires
    coefficients outside the declared O(1)-like scan.

The main scan restricts alpha to 0.01..10 and enforces the published
preferred-frame PPN alpha_2 bound.

Failure therefore closes only the practical finite-duration ordinary-source
single-mode resonance branch, not every possible gauged-ghost excitation.
"""

from __future__ import annotations

import csv
import json
import math
import time
import warnings
from pathlib import Path

import numpy as np
from scipy.stats import qmc


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "data" / "032o1_gauged_ghost_finite_duration_source_inventory_summary.json"
TOP_OUT = ROOT / "results" / "data" / "032o1_finite_duration_top_candidates.csv"
DURATION_OUT = ROOT / "results" / "data" / "032o1_duration_source_inventory.csv"
O0 = ROOT / "results" / "data" / "032o0_gauged_ghost_condensate_static_dynamic_prefield_summary.json"

SAMPLES = 10_000_000
CHUNK = 250_000
TOP_KEEP = 100

G_NEWTON = 6.67430e-11
C = 299792458.0
MPL_GEV = 2.435e18
YEAR_S = 365.25 * 24.0 * 3600.0
AGE_UNIVERSE_YR = 13.8e9

PAYLOAD_RADIUS_M = 0.10
PAYLOAD_DIAMETER_M = 0.20
ZERO_GAP_FAR_SURFACE_M = PAYLOAD_DIAMETER_M
TARGET_ACCEL = 9.80665
ENERGY_TARGET_J = 1.0e7

# Maximum ordinary positive source mass if the entire strict energy budget
# is unrealistically assigned to source rest mass.
SOURCE_MASS_BUDGET_KG = ENERGY_TARGET_J / C ** 2

# The adverse far-surface Newtonian acceleration from a point source at
# zero gap. This maximizes one-sided kernel leverage per unit source mass.
NEWTONIAN_ACCEL_BUDGET = (
    G_NEWTON
    * SOURCE_MASS_BUDGET_KG
    / ZERO_GAP_FAR_SURFACE_M ** 2
)

# Net outward >=1g requires the resonant correction not only to cancel
# ordinary attraction but then exceed it by TARGET_ACCEL.
REQUIRED_CORRECTION_RATIO = (
    1.0 + TARGET_ACCEL / NEWTONIAN_ACCEL_BUDGET
)

# A single sinusoidal acceleration mode can keep one sign throughout the
# payload diameter only if the phase excursion from center to either edge
# stays below pi/2. This gives k R <= pi/2.
KR_MAX = math.pi / 2.0
K_MAX_PER_M = KR_MAX / PAYLOAD_RADIUS_M

# Published parameter envelope.
LOG10_G_MIN = -9.0
LOG10_G_MAX = 0.0
LOG10_M_FRACTION_MIN = -12.0
LOG10_M_FRACTION_MAX = 0.0
LOG10_ALPHA_MIN = -2.0
LOG10_ALPHA_MAX = 1.0
LOG10_KR_MIN = -4.0
LOG10_KR_MAX = math.log10(KR_MAX)

PPN_ALPHA2_MAX = 4.0e-7


def mmax_gev(g):
    return np.minimum(1.0e12, g * g * 1.0e15)


def finite_time_rate(epsilon, omega_p):
    e2 = epsilon * epsilon
    return e2 * omega_p / (1.0 - e2)


def required_time(rate):
    if rate <= 0.0:
        return float("inf")
    return REQUIRED_CORRECTION_RATIO / rate


def minimum_source_energy_for_duration(rate, duration_s):
    #
    # Net outward bound:
    #
    #   a_out <= a_N [rate*T - 1].
    #
    # If rate*T <= 1 even the sign cannot reverse, irrespective of mass.
    factor = rate * duration_s - 1.0
    if factor <= 0.0:
        return float("inf")

    return (
        TARGET_ACCEL
        * C ** 2
        * ZERO_GAP_FAR_SURFACE_M ** 2
        / (G_NEWTON * factor)
    )


def analytic_point(g, m_gev, alpha, kr):
    gc = m_gev / (math.sqrt(2.0) * MPL_GEV)
    epsilon = m_gev / (math.sqrt(2.0) * g * MPL_GEV)
    cs2 = alpha * (g * g - gc * gc)

    if cs2 <= 0.0 or cs2 > 1.0 or epsilon * epsilon >= 1.0:
        return None

    ppn = (
        m_gev ** 2
        / (
            2.0
            * alpha
            * g ** 4
            * (1.0 - epsilon ** 2) ** 2
            * MPL_GEV ** 2
        )
    )

    if ppn >= PPN_ALPHA2_MAX:
        return None

    cs = math.sqrt(cs2)
    k = kr / PAYLOAD_RADIUS_M
    omega = cs * C * k
    rate = finite_time_rate(epsilon, omega)

    return {
        "g": g,
        "m_gev": m_gev,
        "alpha": alpha,
        "kr": kr,
        "epsilon": epsilon,
        "cs_over_c": cs,
        "ppn_alpha2": ppn,
        "omega_p_rad_s": omega,
        "frequency_hz": omega / (2.0 * math.pi),
        "growth_rate_per_s": rate,
        "required_time_s": required_time(rate),
    }


# Analytic maximum epsilon occurs at the cusp of the two M envelopes.
G_CUSP = math.sqrt(1.0e12 / 1.0e15)
M_CUSP_GEV = 1.0e12
EPSILON_MAX = M_CUSP_GEV / (
    math.sqrt(2.0) * G_CUSP * MPL_GEV
)

# Best declared alpha<=10 point.
ALPHA_MAX = 10.0
analytic_best = analytic_point(
    G_CUSP,
    M_CUSP_GEV,
    ALPHA_MAX,
    KR_MAX,
)

if analytic_best is None:
    raise RuntimeError("analytic best point unexpectedly failed")

# More favorable than the declared theory scan: preserve epsilon_max and
# finite-payload k_max but allow the longitudinal mode to propagate at c.
OMEGA_CAUSAL = C * K_MAX_PER_M
RATE_CAUSAL = finite_time_rate(EPSILON_MAX, OMEGA_CAUSAL)
TREQ_CAUSAL = required_time(RATE_CAUSAL)

# Alpha=1 reference at the same published cusp.
alpha1 = analytic_point(
    G_CUSP,
    M_CUSP_GEV,
    1.0,
    KR_MAX,
)

if alpha1 is None:
    raise RuntimeError("alpha=1 cusp unexpectedly failed")

start = time.perf_counter()
sampler = qmc.Sobol(d=4, scramble=True, seed=32041)
warnings.filterwarnings(
    "ignore",
    message="The balance properties of Sobol.*",
)

evaluated = 0
healthy = 0
ppn_reject = 0
top = []

print("=== 032O1 TEN-MILLION FINITE-DURATION FRONTIER ===")
print("SOURCE_MASS_BUDGET_KG=" + format(SOURCE_MASS_BUDGET_KG, ".12e"))
print("NEWTONIAN_ACCEL_AT_FAR_SURFACE=" + format(NEWTONIAN_ACCEL_BUDGET, ".12e"))
print("REQUIRED_CORRECTION_RATIO=" + format(REQUIRED_CORRECTION_RATIO, ".12e"))
print("KR_MAX=" + format(KR_MAX, ".12e"))

while evaluated < SAMPLES:
    count = min(CHUNK, SAMPLES - evaluated)
    u = sampler.random(count)

    logg = LOG10_G_MIN + u[:, 0] * (LOG10_G_MAX - LOG10_G_MIN)
    g = 10.0 ** logg

    mmax = mmax_gev(g)
    logmf = (
        LOG10_M_FRACTION_MIN
        + u[:, 1]
        * (LOG10_M_FRACTION_MAX - LOG10_M_FRACTION_MIN)
    )
    m = mmax * 10.0 ** logmf

    logalpha = (
        LOG10_ALPHA_MIN
        + u[:, 2]
        * (LOG10_ALPHA_MAX - LOG10_ALPHA_MIN)
    )
    alpha = 10.0 ** logalpha

    logkr = (
        LOG10_KR_MIN
        + u[:, 3]
        * (LOG10_KR_MAX - LOG10_KR_MIN)
    )
    kr = 10.0 ** logkr

    gc = m / (math.sqrt(2.0) * MPL_GEV)
    epsilon = m / (math.sqrt(2.0) * g * MPL_GEV)
    eps2 = epsilon * epsilon
    cs2 = alpha * (g * g - gc * gc)

    basic = (
        (g > gc)
        & (eps2 < 1.0)
        & (cs2 > 0.0)
        & (cs2 <= 1.0)
    )

    ppn = np.full(count, np.inf)
    ppn[basic] = (
        m[basic] ** 2
        / (
            2.0
            * alpha[basic]
            * g[basic] ** 4
            * (1.0 - eps2[basic]) ** 2
            * MPL_GEV ** 2
        )
    )

    good = basic & (ppn < PPN_ALPHA2_MAX)
    ppn_reject += int(np.count_nonzero(basic & ~good))
    healthy += int(np.count_nonzero(good))

    cs = np.zeros(count)
    cs[good] = np.sqrt(cs2[good])

    k = kr / PAYLOAD_RADIUS_M
    omega = cs * C * k

    rate = np.zeros(count)
    rate[good] = (
        eps2[good]
        * omega[good]
        / (1.0 - eps2[good])
    )

    treq = np.full(count, np.inf)
    positive = good & (rate > 0.0)
    treq[positive] = REQUIRED_CORRECTION_RATIO / rate[positive]

    local_keep = min(TOP_KEEP, count)
    idx = np.argpartition(treq, local_keep - 1)[:local_keep]

    for i in idx:
        if not math.isfinite(float(treq[i])):
            continue

        top.append(
            {
                "sample_index": evaluated + int(i),
                "g": float(g[i]),
                "m_gev": float(m[i]),
                "mmax_gev": float(mmax[i]),
                "alpha": float(alpha[i]),
                "kr": float(kr[i]),
                "epsilon": float(epsilon[i]),
                "cs_over_c": float(cs[i]),
                "ppn_alpha2": float(ppn[i]),
                "frequency_hz": float(omega[i] / (2.0 * math.pi)),
                "growth_rate_per_s": float(rate[i]),
                "required_time_s": float(treq[i]),
                "required_time_years": float(treq[i] / YEAR_S),
            }
        )

    top.sort(
        key=lambda row: (
            row["required_time_s"],
            row["sample_index"],
        )
    )
    del top[TOP_KEEP:]

    evaluated += count

    if evaluated % 1_000_000 == 0 or evaluated == SAMPLES:
        print(
            "PROGRESS"
            + " evaluated=" + str(evaluated)
            + " healthy=" + str(healthy)
            + " best_years="
            + format(top[0]["required_time_years"], ".12e"),
            flush=True,
        )

elapsed = time.perf_counter() - start
best = top[0]

durations = [
    ("1_SECOND", 1.0),
    ("1_MINUTE", 60.0),
    ("1_HOUR", 3600.0),
    ("1_DAY", 86400.0),
    ("1_YEAR", YEAR_S),
    ("100_YEARS", 100.0 * YEAR_S),
    ("AGE_UNIVERSE", AGE_UNIVERSE_YR * YEAR_S),
]

duration_rows = []

for label, duration_s in durations:
    e_declared = minimum_source_energy_for_duration(
        analytic_best["growth_rate_per_s"],
        duration_s,
    )
    e_causal = minimum_source_energy_for_duration(
        RATE_CAUSAL,
        duration_s,
    )

    duration_rows.append(
        {
            "duration_label": label,
            "duration_s": duration_s,
            "declared_alpha10_min_source_j": e_declared,
            "declared_alpha10_over_10mj": (
                e_declared / ENERGY_TARGET_J
                if math.isfinite(e_declared)
                else float("inf")
            ),
            "causal_oracle_min_source_j": e_causal,
            "causal_oracle_over_10mj": (
                e_causal / ENERGY_TARGET_J
                if math.isfinite(e_causal)
                else float("inf")
            ),
        }
    )

with TOP_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(top[0].keys()))
    writer.writeheader()
    writer.writerows(top)

with DURATION_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(duration_rows[0].keys()))
    writer.writeheader()
    writer.writerows(duration_rows)

o0 = None
o0_q = None
o0_linewidth_hz = None
o0_fourier_time_s = None

if O0.exists():
    o0 = json.loads(O0.read_text(encoding="utf-8"))
    o0_q = float(o0["dynamic"]["analytic_min_required_q"])
    o0_linewidth_hz = float(
        o0["dynamic"]["alpha1_reversal_linewidth_hz_20cm"]
    )
    o0_fourier_time_s = 1.0 / o0_linewidth_hz

age_row = next(
    row for row in duration_rows
    if row["duration_label"] == "AGE_UNIVERSE"
)

declared_t_years = analytic_best["required_time_s"] / YEAR_S
causal_t_years = TREQ_CAUSAL / YEAR_S

practical_declared_red = declared_t_years > AGE_UNIVERSE_YR
practical_causal_red = causal_t_years > AGE_UNIVERSE_YR

decision = (
    "RED_PRACTICAL_FINITE_DURATION_ORDINARY_SOURCE_RESONANCE"
    if practical_declared_red and practical_causal_red
    else "FINITE_DURATION_BRANCH_REQUIRES_DEEPER_AUDIT"
)

result = {
    "branch": "032O1_GAUGED_GHOST_FINITE_DURATION_SOURCE_INVENTORY",
    "claim_class": "OPTIMISTIC_LINEAR_FINITE_DURATION_UPPER_BOUND",
    "samples": SAMPLES,
    "healthy_samples": healthy,
    "ppn_rejections": ppn_reject,
    "energy_target_j": ENERGY_TARGET_J,
    "source_mass_budget_kg": SOURCE_MASS_BUDGET_KG,
    "payload_radius_m": PAYLOAD_RADIUS_M,
    "zero_gap_far_surface_m": ZERO_GAP_FAR_SURFACE_M,
    "newtonian_accel_from_10mj_source_mps2": NEWTONIAN_ACCEL_BUDGET,
    "required_metric_correction_ratio": REQUIRED_CORRECTION_RATIO,
    "single_mode_sign_coherence_kr_max": KR_MAX,
    "published_ppn_alpha2_max": PPN_ALPHA2_MAX,
    "analytic_declared_alpha10": analytic_best,
    "analytic_alpha1_reference": alpha1,
    "causal_oracle": {
        "model_point": False,
        "epsilon": EPSILON_MAX,
        "cs_over_c": 1.0,
        "kr": KR_MAX,
        "omega_p_rad_s": OMEGA_CAUSAL,
        "frequency_hz": OMEGA_CAUSAL / (2.0 * math.pi),
        "growth_rate_per_s": RATE_CAUSAL,
        "required_time_s": TREQ_CAUSAL,
        "required_time_years": causal_t_years,
    },
    "sobol_best": best,
    "duration_inventory": duration_rows,
    "o0_detuning_q": o0_q,
    "o0_alpha1_linewidth_hz_20cm": o0_linewidth_hz,
    "o0_fourier_linewidth_time_s": o0_fourier_time_s,
    "age_universe_years_used": AGE_UNIVERSE_YR,
    "age_universe_declared_alpha10_min_source_j": age_row["declared_alpha10_min_source_j"],
    "age_universe_causal_oracle_min_source_j": age_row["causal_oracle_min_source_j"],
    "declared_10mj_required_time_years": declared_t_years,
    "causal_oracle_10mj_required_time_years": causal_t_years,
    "zero_damping_assumed": True,
    "perfect_phase_control_assumed": True,
    "drive_kinetic_energy_omitted": True,
    "generator_control_energy_omitted": True,
    "nonlinear_saturation_omitted": True,
    "field_mode_energy_not_added": True,
    "complete_operating_ledger": False,
    "field_solution": False,
    "certified_antigravity_model": False,
    "published_static_branch_closed": True,
    "practical_finite_duration_ordinary_source_branch_closed": (
        practical_declared_red and practical_causal_red
    ),
    "mathematical_infinite_time_zero_damping_branch_closed": False,
    "full_gauged_ghost_condensate_family_closed": False,
    "decision": decision,
    "next": "RERANK_FRONTIER_AFTER_032O1",
    "seconds": elapsed,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("")
print("=== 032O1 RESULT ===")
print("SAMPLES=" + str(SAMPLES))
print("HEALTHY_SAMPLES=" + str(healthy))
print("PPN_REJECTIONS=" + str(ppn_reject))
print("SOURCE_MASS_BUDGET_KG=" + format(SOURCE_MASS_BUDGET_KG, ".12e"))
print("NEWTONIAN_ACCEL_10MJ_SOURCE=" + format(NEWTONIAN_ACCEL_BUDGET, ".12e"))
print("REQUIRED_CORRECTION_RATIO=" + format(REQUIRED_CORRECTION_RATIO, ".12e"))
print("ANALYTIC_ALPHA10_G=" + format(analytic_best["g"], ".12e"))
print("ANALYTIC_ALPHA10_M_GEV=" + format(analytic_best["m_gev"], ".12e"))
print("ANALYTIC_ALPHA10_EPSILON=" + format(analytic_best["epsilon"], ".12e"))
print("ANALYTIC_ALPHA10_CS_OVER_C=" + format(analytic_best["cs_over_c"], ".12e"))
print("ANALYTIC_ALPHA10_PPN=" + format(analytic_best["ppn_alpha2"], ".12e"))
print("ANALYTIC_ALPHA10_GROWTH_RATE_PER_S=" + format(analytic_best["growth_rate_per_s"], ".12e"))
print("ANALYTIC_ALPHA10_REQUIRED_YEARS=" + format(declared_t_years, ".12e"))
print("CAUSAL_ORACLE_GROWTH_RATE_PER_S=" + format(RATE_CAUSAL, ".12e"))
print("CAUSAL_ORACLE_REQUIRED_YEARS=" + format(causal_t_years, ".12e"))
print("SOBOL_BEST_REQUIRED_YEARS=" + format(best["required_time_years"], ".12e"))
print("AGE_UNIVERSE_ALPHA10_MIN_SOURCE_J=" + format(age_row["declared_alpha10_min_source_j"], ".12e"))
print("AGE_UNIVERSE_CAUSAL_MIN_SOURCE_J=" + format(age_row["causal_oracle_min_source_j"], ".12e"))

if o0_q is not None:
    print("O0_DETUNING_Q=" + format(o0_q, ".12e"))
    print("O0_LINEWIDTH_HZ=" + format(o0_linewidth_hz, ".12e"))
    print("O0_FOURIER_LINEWIDTH_TIME_S=" + format(o0_fourier_time_s, ".12e"))

print("ZERO_DAMPING_ASSUMED=YES")
print("FIELD_MODE_ENERGY_ADDED=NO")
print("COMPLETE_OPERATING_LEDGER=NO")
print("CERTIFIED_ANTIGRAVITY_MODEL=NO")
print("PRACTICAL_FINITE_DURATION_ORDINARY_SOURCE_BRANCH_CLOSED=" + str(practical_declared_red and practical_causal_red))
print("INFINITE_TIME_ZERO_DAMPING_BRANCH_CLOSED=False")
print("FULL_GAUGED_GHOST_CONDENSATE_FAMILY_CLOSED=False")
print("DECISION=" + decision)
print("NEXT=RERANK_FRONTIER_AFTER_032O1")
