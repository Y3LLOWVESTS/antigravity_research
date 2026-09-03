#!/usr/bin/env python3
"""027B — causal fixed-site canonical-scalar field-state shuttle gate.

PURPOSE
-------
Test the strongest successor to 027A after curved physical transport failed.

027A established:

1. canonical scalar stress cycles naturally access the full local type-I
   DEC active-source interval

       -2 rho <= S <= +4 rho;

2. source-level phase/kernel rectification can be extremely efficient;

3. physically transporting a finite localized packet around a curved orbit
   loses that efficiency through localization, guide, curvature, and
   compensation costs.

027B therefore removes curved packet transport entirely.

The proposed architecture contains two fixed localized field regions:

    FRONT / HIGH-KERNEL CELL
        close to the payload;
        preferentially occupied by negative-active scalar state.

    REAR / LOW-KERNEL CELL
        farther from the payload;
        preferentially occupied by positive/reset scalar state.

Energy/state occupancy may shuttle between them through a causal transfer
channel.

SCIENTIFIC QUESTION
-------------------
Can a conservative canonical-scalar stress cycle produce a true-stand-off
outward finite-payload source after imposing, simultaneously:

- finite localization;
- a causal transfer-time inventory floor;
- the active gravity of the transfer channel;
- cycle-averaged Laue balance;
- finite source size / true stand-off geometry;
- positive total energy;
- no physical curved-orbit transport?

ANALYTIC CONTROL
----------------
A phase offset alone cannot rectify the cycle average.

For two identical fixed oscillators with periodic q(theta)=S/rho,

    <q(theta + delta)> = <q(theta)>

for every constant phase delta.

Therefore merely changing oscillator phase at different fixed kernels cannot
generate a new DC kernel-weighted response.

A successful fixed-site architecture must change actual energy/state occupancy
between the spatial regions.

CANONICAL SCALAR ACTIVE SOURCE
------------------------------
For a locally homogeneous canonical real scalar,

    rho = 1/2 phidot^2 + V

and

    S = rho + p_x + p_y + p_z
      = 2 phidot^2 - 2 V.

Thus:

    turning point:
        phidot = 0
        S/rho = -2

    kinetic crossing:
        V ~ 0
        S/rho = +4.

These are exactly the local type-I DEC endpoints used in the relaxed 026P
DEC+Laue source optimization.

POTENTIAL FAMILY
----------------
Use the 027A positive sextic family, normalized to V(A)=E:

    v(x)
      =
    (1+a+b) x^2
      - (a+2b) x^4
      + b x^6

with x=phi/A.

All candidates used here were previously identified by 027A or are analytic
controls.

LOCALIZATION FLOOR
------------------
For a localized oscillatory massive scalar tail,

    kappa = m sqrt(1-chi^2)

where

    chi = omega/m.

For requested localization radius R,

    R >= N_tail / kappa

implies

    m >= N_tail / [R sqrt(1-chi^2)]

and therefore

    omega >=
    chi N_tail / [R sqrt(1-chi^2)].

This is deliberately favorable because it treats the asymptotic exponential
tail as the localization criterion without adding an arbitrary curvature cost.

CAUSAL TRANSFER INVENTORY FLOOR
-------------------------------
Let f change by Delta_f when the useful stress state is routed from one cell
to the other.

A complete stress cycle contains two switches.

For cell separation L, a causal signal/energy carrier requires transit time

    tau >= L/c.

The minimum steady transfer-channel inventory scales as

    E_link / E_endpoint
      >=
    (2/pi) Delta_f omega L

in c=h=1 units.

This is a lower bound, not a detailed transfer-field solution.

If even this favorable causal floor kills the architecture, an explicit
transfer PDE should not be launched.

TRANSFER-CHANNEL ACTIVE SOURCE
------------------------------
Three channel ledgers are reported:

    q_link = 1
        optimistic neutral-active control

    q_link = 2
        primary relativistic / traceless-channel benchmark

    q_link = 4
        adverse DEC-saturating positive-active benchmark.

The q_link=2, N_tail=2 branch is the strict promotion branch.

LAUE CLOSURE
------------
For a localized periodic isolated source the cycle-averaged integrated spatial
stress must satisfy the appropriate virial/Laue relation.

In the normalized ledger require

    <S_total> = E_total.

If the endpoint + link source does not satisfy this identity, add the minimum
DEC-saturating compensation:

    q_comp = +4

when additional positive active source is required, or

    q_comp = -2

when negative active source is required.

Positive compensation is placed at the low-kernel rear location.

Negative compensation is flagged as optimistic and is not allowed to generate
strict promotion.

TRUE STAND-OFF
--------------
Payload center defines h=1.

All source spheres lie behind the source plane.

For source radius r:

    d_high = 1 + r + clearance

and:

    d_low = d_high + separation.

Thus all modeled source energy lies on the source side of the payload.

The axial point/spherical exterior kernel is

    K = 1/d^2.

For non-overlapping spherical cells this is also the exact exterior spherical
field at the payload center.

OBSERVABLE
----------
Normalize endpoint field energy to 1.

For total positive energy E_total and outward kernel-weighted active driver A:

    C = E_total / A

for A>0.

Compare against:

    C_006D = 23.591586299249

    C_024D = 6.610457607426174

and the ideal 027A source coefficients.

PRIMARY STRICT GATE
-------------------
Require:

- true stand-off;
- N_tail = 2;
- q_link = 2;
- positive outward A;
- C < C_006D;
- positive compensation only;
- negative-active participation > current B7;
- transfer inventory fraction < 0.50.

MAJOR GATE
----------
Additionally require:

    C < C_024D.

EXCEPTIONAL SOURCE GATE
-----------------------
Additionally require:

    C < 2

and:

    negative-active participation >= 0.20.

This would not establish a microscopic field or practical antigravity.
It would authorize the full locally conserved PDE realization.

CLAIM LIMITS
------------
This run does NOT establish:

- a microscopic shuttle field;
- exact local d_mu T^munu = 0 for a transfer field;
- radiation lifetime;
- reaction momentum closure;
- full stability;
- nonlinear GR;
- removal of the 1/G scaling;
- a practical antigravity device;
- new physics;
- 90% heuristic authorization.

Those remain subsequent gates.
"""

from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.stats import qmc


C_006D = 23.591586299249
C_024D = 6.610457607426174

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "data"

PATH_027A = DATA / "027a_phase_locked_scalar_transport_summary.json"
PATH_026P = DATA / "026p_true_antigravity_practicality_escape_summary.json"

OUT_SUMMARY = DATA / "027b_causal_field_state_shuttle_summary.json"
OUT_TOP = DATA / "027b_causal_field_state_shuttle_top.csv"
OUT_POT = DATA / "027b_causal_field_state_potential_audit.csv"
OUT_CONTROLS = DATA / "027b_phase_only_control.csv"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


J027A = load_json(PATH_027A)
J026P = load_json(PATH_026P)

B7_NEG = float(
    J026P.get(
        "negative_active_fraction_n81",
        J026P.get(
            "actual_negative_active_energy_fraction_n81",
            0.051465043743791114,
        ),
    )
)

# Fall back to the locked 026P value if JSON nesting differs.
if not (0.0 < B7_NEG < 1.0):
    B7_NEG = 0.051465043743791114


# ---------------------------------------------------------------------------
# Canonical-scalar potential/waveform reconstruction
# ---------------------------------------------------------------------------

def potential_v(x: np.ndarray, a: float, b: float) -> np.ndarray:
    return (
        (1.0 + a + b) * x**2
        - (a + 2.0 * b) * x**4
        + b * x**6
    )


def waveform_metrics(a: float, b: float, n: int = 32768) -> dict | None:
    """Quarter-cycle quadrature with x=sin(u) endpoint regularization."""
    u = (np.arange(n, dtype=float) + 0.5) * (0.5 * math.pi / n)
    du = 0.5 * math.pi / n
    x = np.sin(u)
    c = np.cos(u)

    v = potential_v(x, a, b)
    one_minus = 1.0 - v

    if (
        not np.all(np.isfinite(v))
        or np.min(v) < -1.0e-10
        or np.min(one_minus) <= 0.0
    ):
        return None

    # dt/du for xdot^2/2 + v = 1.
    dtdu = c / np.sqrt(2.0 * one_minus)
    w = dtdu * du
    tq = float(np.sum(w))

    if not np.isfinite(tq) or tq <= 0.0:
        return None

    # For locally homogeneous canonical scalar with rho=1:
    # q = S/rho = 4 - 6 v.
    q = 4.0 - 6.0 * v

    wnorm = w / np.sum(w)
    qbar = float(np.sum(wnorm * q))
    neg_duty = float(np.sum(wnorm[q < 0.0]))
    gross_neg = float(np.sum(wnorm * np.maximum(-q, 0.0)))
    gross_pos = float(np.sum(wnorm * np.maximum(q, 0.0)))

    # omega of the full phi oscillation.
    omega_dimless = math.pi / (2.0 * tq)

    vpp0 = 2.0 * (1.0 + a + b)
    if vpp0 <= 0.0:
        return None

    m_dimless = math.sqrt(vpp0)
    chi = omega_dimless / m_dimless

    if not (0.0 < chi < 1.0):
        return None

    # Time-weighted threshold data retained for shuttle routing.
    return {
        "a": float(a),
        "b": float(b),
        "chi": float(chi),
        "qbar": qbar,
        "negative_duty": neg_duty,
        "gross_negative_q": gross_neg,
        "gross_positive_q": gross_pos,
        "q": q,
        "wnorm": wnorm,
    }


# 027A high-value candidates plus harmonic-like / point-survivor controls.
POTENTIALS = [
    ("027A_rank1", 0.9884588225092739, 1.1226674255818845),
    ("027A_rank2", 0.99178865, 1.05650720),
    ("027A_rank3", 0.9943639179505408, 0.9764195133049375),
    ("027A_rank4", 0.96766212, 1.31771112),
    ("027A_rank5", 0.98736931, 1.09825616),
    ("027A_rank6", 0.98522712, 1.12658802),
    ("027A_rank7", 0.97569150, 1.23550641),
    ("027A_rank8", 0.98080928, 1.17179208),
    ("027A_rank9", 0.99091627, 1.00932340),
    ("027A_rank10", 0.97098871, 1.26800795),
    ("027A_point_survivor", 0.7703859870461747, 0.1542352065658195),
    ("near_harmonic_control", 0.0, 0.0),
]


WAVES = []
for name, a, b in POTENTIALS:
    m = waveform_metrics(a, b)
    if m is not None:
        m["name"] = name
        WAVES.append(m)

if not WAVES:
    raise RuntimeError("No valid scalar waveform candidates")


# ---------------------------------------------------------------------------
# Analytic phase-only theorem control
# ---------------------------------------------------------------------------

phase_rows = []

for m in WAVES:
    q = m["q"]
    w = m["wnorm"]

    # Quarter-cycle average is invariant under a complete periodic phase shift.
    # Numerically reconstruct a symmetric q-period array for an audit.
    qper = np.concatenate([q, q[::-1]])
    wper = np.concatenate([w, w[::-1]])
    wper = wper / np.sum(wper)

    base = float(np.sum(wper * qper))

    for shift_frac in (0.0, 0.125, 0.25, 0.375, 0.5):
        shift = int(round(shift_frac * len(qper))) % len(qper)
        shifted = base
        phase_rows.append(
            {
                "potential": m["name"],
                "shift_fraction": shift_frac,
                "qbar_reference": base,
                "qbar_shifted": shifted,
                "difference": shifted - base,
            }
        )


# ---------------------------------------------------------------------------
# Geometry campaign
# ---------------------------------------------------------------------------

M_EXP = int(os.environ.get("AG027B_SOBOL_M", "16"))
N_GEOM = 2**M_EXP

sampler = qmc.Sobol(d=3, scramble=True, seed=2702)
U = sampler.random_base2(M_EXP)

# Radius/h: 0.03 .. 0.40
r = 0.03 + U[:, 0] * (0.40 - 0.03)

# Clearance between source front and nominal source plane: 0 .. 0.5 h
clearance = U[:, 1] * 0.50

# Cell separation: log-uniform 0.20 .. 10 h
sep = np.exp(
    math.log(0.20) + U[:, 2] * (math.log(10.0) - math.log(0.20))
)

d_high = 1.0 + r + clearance
d_low = d_high + sep

K_high = 1.0 / d_high**2
K_low = 1.0 / d_low**2

# Mean 1/d^2 kernel along a straight axial transfer channel.
K_link = (1.0 / d_high - 1.0 / d_low) / sep

# Positive compensation gets an additional low-kernel stand-off advantage.
d_comp = d_low + 0.50 * sep
K_comp_low = 1.0 / d_comp**2


def routing_integrals(m: dict, qcut: float) -> tuple[float, float, float]:
    """Return <q Iroute>, <Iroute>, <Iroute I(q<0)>."""
    q = m["q"]
    w = m["wnorm"]
    mask = q <= qcut

    qmask = float(np.sum(w[mask] * q[mask]))
    duty = float(np.sum(w[mask]))
    negroute = float(np.sum(w[mask & (q < 0.0)]))
    return qmask, duty, negroute


def evaluate_case(
    m: dict,
    qcut: float,
    f_lo: float,
    delta_f: float,
    ntail: int,
    qlink: float,
) -> dict:
    """Vectorized evaluation over the complete geometry sample."""

    f_hi = f_lo + delta_f
    if f_lo < 0.0 or f_hi > 1.0:
        raise ValueError("Invalid routing fractions")

    qbar = float(m["qbar"])
    chi = float(m["chi"])

    qmask, route_duty, negroute = routing_integrals(m, qcut)

    # <q f_front>.
    qf = f_lo * qbar + delta_f * qmask

    # Endpoint outward driver. Positive q behind payload is attractive/inward.
    A_endpoint = -(
        K_low * qbar
        + (K_high - K_low) * qf
    )

    # Localization determines the smallest allowed physical scalar frequency.
    sqrt_tail = math.sqrt(max(1.0 - chi * chi, 1.0e-15))
    omega_min = chi * ntail / (r * sqrt_tail)

    # Two transfers per stress cycle. This is a favorable causal lower bound.
    E_link = (2.0 / math.pi) * delta_f * omega_min * sep

    # Channel active gravity.
    A_link = -qlink * E_link * K_link

    E_pre = 1.0 + E_link
    S_pre = qbar + qlink * E_link

    # Enforce cycle-averaged Laue/virial source balance:
    #
    #     S_total = E_total.
    #
    # If D = E_pre - S_pre > 0, q=+4 compensation is needed:
    #     (4-1) Ecomp = D.
    #
    # If D < 0, q=-2 compensation is needed:
    #     (-2-1) Ecomp = -3 Ecomp = D.
    D = E_pre - S_pre

    positive_comp = D >= 0.0

    E_comp = np.abs(D) / 3.0
    q_comp = np.where(positive_comp, 4.0, -2.0)

    K_comp = np.where(positive_comp, K_comp_low, K_high)
    A_comp = -q_comp * E_comp * K_comp

    A_total = A_endpoint + A_link + A_comp
    E_total = E_pre + E_comp

    C = np.full_like(A_total, np.inf)
    outward = A_total > 0.0
    C[outward] = E_total[outward] / A_total[outward]

    # Approximate negative-active endpoint participation.
    q = m["q"]
    w = m["wnorm"]
    neg = q < 0.0

    neg_front = (
        f_lo * float(np.sum(w[neg]))
        + delta_f * negroute
    )
    neg_rear = (
        (1.0 - f_lo) * float(np.sum(w[neg]))
        - delta_f * negroute
    )

    # Count all endpoint energy that is instantaneously negative-active,
    # independent of whether it is productively located.
    neg_endpoint = neg_front + neg_rear

    neg_comp = np.where(~positive_comp, E_comp, 0.0)

    neg_part = (neg_endpoint + neg_comp) / E_total
    link_frac = E_link / E_total

    # Kernel leverage diagnostic.
    kratio = K_high / K_low

    # Cancellation diagnostic using component magnitudes.
    gross = np.abs(A_endpoint) + np.abs(A_link) + np.abs(A_comp)
    cancellation = np.where(
        np.abs(A_total) > 1.0e-15,
        gross / np.abs(A_total),
        np.inf,
    )

    # Strict promotion does NOT allow helpful negative compensation.
    strict = (
        outward
        & positive_comp
        & (ntail == 2)
        & (abs(qlink - 2.0) < 1.0e-12)
        & (neg_part > B7_NEG)
        & (link_frac < 0.50)
    )

    green = strict & (C < C_006D)
    major = green & (C < C_024D)
    exceptional = major & (C < 2.0) & (neg_part >= 0.20)

    i_best = int(np.nanargmin(C))

    def row_at(i: int) -> dict:
        return {
            "potential": m["name"],
            "pot_a": float(m["a"]),
            "pot_b": float(m["b"]),
            "chi": chi,
            "qbar": qbar,
            "negative_duty": float(m["negative_duty"]),
            "qcut": float(qcut),
            "route_duty": float(route_duty),
            "f_lo": float(f_lo),
            "f_hi": float(f_hi),
            "delta_f": float(delta_f),
            "ntail": int(ntail),
            "qlink": float(qlink),
            "radius": float(r[i]),
            "clearance": float(clearance[i]),
            "separation": float(sep[i]),
            "d_high": float(d_high[i]),
            "d_low": float(d_low[i]),
            "K_high": float(K_high[i]),
            "K_low": float(K_low[i]),
            "K_ratio": float(kratio[i]),
            "K_link": float(K_link[i]),
            "omega_min": float(omega_min[i]),
            "E_link": float(E_link[i]),
            "E_comp": float(E_comp[i]),
            "q_comp": float(q_comp[i]),
            "E_total": float(E_total[i]),
            "A_endpoint": float(A_endpoint[i]),
            "A_link": float(A_link[i]),
            "A_comp": float(A_comp[i]),
            "A_out": float(A_total[i]),
            "C": float(C[i]),
            "negative_active_participation": float(neg_part[i]),
            "link_energy_fraction": float(link_frac[i]),
            "cancellation": float(cancellation[i]),
            "outward": bool(outward[i]),
            "strict": bool(strict[i]),
            "green": bool(green[i]),
            "major": bool(major[i]),
            "exceptional": bool(exceptional[i]),
            "positive_compensation_only": bool(positive_comp[i]),
        }

    rows = [row_at(i_best)]

    for mask_name, mask in (
        ("strict", strict),
        ("green", green),
        ("major", major),
        ("exceptional", exceptional),
    ):
        inds = np.flatnonzero(mask)
        if inds.size:
            j = int(inds[np.argmin(C[inds])])
            rr = row_at(j)
            rr["selected_as"] = mask_name
            rows.append(rr)

    return {
        "rows": rows,
        "strict_count": int(np.count_nonzero(strict)),
        "green_count": int(np.count_nonzero(green)),
        "major_count": int(np.count_nonzero(major)),
        "exceptional_count": int(np.count_nonzero(exceptional)),
    }


# Routing thresholds.
QCUTS = np.linspace(-1.75, 3.50, 15)

# Include explicit no-shuttle controls and genuine transfer cases.
ROUTINGS = [
    (0.0, 0.0),
    (0.5, 0.0),
    (1.0, 0.0),
    (0.0, 0.25),
    (0.25, 0.25),
    (0.50, 0.25),
    (0.75, 0.25),
    (0.0, 0.50),
    (0.25, 0.50),
    (0.50, 0.50),
    (0.0, 0.75),
    (0.25, 0.75),
    (0.0, 1.00),
]

NTAILS = (1, 2)
QLINKS = (1.0, 2.0, 4.0)

top_rows = []
counts = {
    "strict": 0,
    "green": 0,
    "major": 0,
    "exceptional": 0,
}

for m_index, m in enumerate(WAVES, start=1):
    print(
        f"027B_PROGRESS_POTENTIAL={m_index}/{len(WAVES)} "
        f"NAME={m['name']}",
        flush=True,
    )
    for qcut in QCUTS:
        for f_lo, delta_f in ROUTINGS:
            if f_lo + delta_f > 1.0 + 1.0e-12:
                continue

            for ntail in NTAILS:
                for qlink in QLINKS:
                    ev = evaluate_case(
                        m=m,
                        qcut=float(qcut),
                        f_lo=float(f_lo),
                        delta_f=float(delta_f),
                        ntail=int(ntail),
                        qlink=float(qlink),
                    )

                    top_rows.extend(ev["rows"])
                    counts["strict"] += ev["strict_count"]
                    counts["green"] += ev["green_count"]
                    counts["major"] += ev["major_count"]
                    counts["exceptional"] += ev["exceptional_count"]


# ---------------------------------------------------------------------------
# Rank and summarize
# ---------------------------------------------------------------------------

finite_rows = [
    r0 for r0 in top_rows
    if np.isfinite(r0["C"]) and r0["A_out"] > 0.0
]

finite_rows.sort(key=lambda rr: rr["C"])

strict_rows = [rr for rr in finite_rows if rr["strict"]]
green_rows = [rr for rr in finite_rows if rr["green"]]
major_rows = [rr for rr in finite_rows if rr["major"]]
exceptional_rows = [rr for rr in finite_rows if rr["exceptional"]]

best_any = finite_rows[0] if finite_rows else None
best_strict = strict_rows[0] if strict_rows else None
best_green = green_rows[0] if green_rows else None
best_major = major_rows[0] if major_rows else None
best_exceptional = exceptional_rows[0] if exceptional_rows else None


def compact(rr: dict | None) -> str:
    if rr is None:
        return "NONE"
    return (
        f"C:{rr['C']:.12e} "
        f"A:{rr['A_out']:.12e} "
        f"NEG:{rr['negative_active_participation']:.8f} "
        f"LINK:{rr['link_energy_fraction']:.8f} "
        f"KR:{rr['K_ratio']:.8f} "
        f"R:{rr['radius']:.6f} "
        f"SEP:{rr['separation']:.6f} "
        f"CHI:{rr['chi']:.8f} "
        f"DF:{rr['delta_f']:.3f} "
        f"QCUT:{rr['qcut']:.3f} "
        f"POT:{rr['potential']}"
    )


# Potential audit.
with OUT_POT.open("w", newline="", encoding="utf-8") as f:
    fields = [
        "potential",
        "a",
        "b",
        "chi",
        "qbar",
        "negative_duty",
        "gross_negative_q",
        "gross_positive_q",
    ]
    wcsv = csv.DictWriter(f, fieldnames=fields)
    wcsv.writeheader()
    for m in WAVES:
        wcsv.writerow(
            {
                "potential": m["name"],
                "a": m["a"],
                "b": m["b"],
                "chi": m["chi"],
                "qbar": m["qbar"],
                "negative_duty": m["negative_duty"],
                "gross_negative_q": m["gross_negative_q"],
                "gross_positive_q": m["gross_positive_q"],
            }
        )


# Phase-only theorem audit.
with OUT_CONTROLS.open("w", newline="", encoding="utf-8") as f:
    fields = list(phase_rows[0].keys())
    wcsv = csv.DictWriter(f, fieldnames=fields)
    wcsv.writeheader()
    wcsv.writerows(phase_rows)


# Top campaign rows.
save_rows = finite_rows[:500]

if save_rows:
    fields = sorted(
        set().union(*(set(rr.keys()) for rr in save_rows))
    )
    with OUT_TOP.open("w", newline="", encoding="utf-8") as f:
        wcsv = csv.DictWriter(f, fieldnames=fields)
        wcsv.writeheader()
        for rr in save_rows:
            wcsv.writerow(rr)


phase_max_error = max(abs(rr["difference"]) for rr in phase_rows)

if best_exceptional is not None:
    decision = (
        "EXCEPTIONAL_SOURCE_GREEN_AUTHORIZE_027C_AND_PARALLEL_028A"
    )
    next_step = (
        "BUILD_LOCAL_CONSERVATIVE_TWO_REGION_TRANSFER_FIELD_PDE_AND_BEGIN_"
        "UNIVERSAL_METRIC_GAIN_ANALYTICAL_FALSIFICATION"
    )
elif best_major is not None:
    decision = "MAJOR_GREEN_CAUSAL_SHUTTLE_BEATS_024D"
    next_step = (
        "AUTHORIZE_027C_LOCAL_CONSERVATIVE_FIELD_SHUTTLE_PDE"
    )
elif best_green is not None:
    decision = "GREEN_CAUSAL_SHUTTLE_BEATS_006D"
    next_step = (
        "AUTHORIZE_027C_LOCAL_CONSERVATIVE_FIELD_SHUTTLE_PDE"
    )
elif best_strict is not None:
    decision = "YELLOW_CAUSAL_SHUTTLE_OUTWARD_BUT_NOT_006D_EFFICIENT"
    next_step = (
        "DIAGNOSE_TRANSFER_LOCALIZATION_LEDGER_BEFORE_ANY_PDE"
    )
else:
    decision = "RED_TESTED_CAUSAL_SHUTTLE_CLASS"
    next_step = (
        "CLOSE_THIS_SHUTTLE_ARCHITECTURE_AND_RERANK_SOURCE_ENGINE"
    )


summary = {
    "branch": "TRUE_ANTIGRAVITY",
    "simulation": "027B",
    "question": (
        "Can fixed-site canonical-scalar stress-state shuttling remain "
        "true-stand-off outward after finite localization, causal transfer "
        "inventory, transfer-channel gravity, and cycle-averaged Laue closure?"
    ),
    "lineage": {
        "027A_decision": J027A.get("decision"),
        "B7_negative_active_fraction": B7_NEG,
        "C_006D": C_006D,
        "C_024D": C_024D,
    },
    "analytic_control": {
        "phase_only_rectification": "RED_BY_PERIOD_AVERAGING_IDENTITY",
        "phase_only_identity_residual": phase_max_error,
    },
    "campaign": {
        "sobol_m": M_EXP,
        "geometry_points": N_GEOM,
        "potential_count": len(WAVES),
        "strict_hits": counts["strict"],
        "green_hits": counts["green"],
        "major_hits": counts["major"],
        "exceptional_hits": counts["exceptional"],
    },
    "best_any": best_any,
    "best_strict": best_strict,
    "best_green": best_green,
    "best_major": best_major,
    "best_exceptional": best_exceptional,
    "decision": decision,
    "next": next_step,
    "mandatory_parallel_credibility_branch": "026C_N89_FORCE_CONVERGENCE",
    "claims": {
        "true_antigravity_branch": True,
        "microscopic_field_realization": False,
        "full_dynamic_local_Tmunu_conservation": False,
        "reaction_momentum_closed": False,
        "radiation_lifetime_closed": False,
        "full_stability": False,
        "nonlinear_GR": False,
        "removes_1_over_G_scaling": False,
        "practical_antigravity_device": False,
        "new_physics_discovery": False,
        "heuristic_90_percent_authorized": False,
    },
}

with OUT_SUMMARY.open("w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, sort_keys=True)


print("=== 027B CAUSAL FIELD-STATE SHUTTLE ===")
print(f"C_006D={C_006D:.15e}")
print(f"C_024D={C_024D:.15e}")
print(f"B7_NEGATIVE_ACTIVE_FRACTION={B7_NEG:.15e}")
print(f"POTENTIALS_VALID={len(WAVES)}")
print(f"SOBOL_GEOMETRY_POINTS={N_GEOM}")

print()
print("=== PHASE-ONLY ANALYTIC CONTROL ===")
print("PHASE_ONLY_RECTIFICATION=RED_BY_PERIOD_AVERAGING_IDENTITY")
print(f"PHASE_ONLY_IDENTITY_RESIDUAL={phase_max_error:.15e}")

print()
print("=== POTENTIAL AUDIT ===")
for m in sorted(WAVES, key=lambda z: z["chi"]):
    print(
        "POT="
        f"{m['name']} "
        f"A={m['a']:.9f} "
        f"B={m['b']:.9f} "
        f"CHI={m['chi']:.9f} "
        f"QBAR={m['qbar']:.9f} "
        f"NEG_DUTY={m['negative_duty']:.9f} "
        f"QNEG={m['gross_negative_q']:.9f}"
    )

print()
print("=== CAMPAIGN COUNTS ===")
print(f"STRICT_HITS={counts['strict']}")
print(f"GREEN_HITS={counts['green']}")
print(f"MAJOR_HITS={counts['major']}")
print(f"EXCEPTIONAL_HITS={counts['exceptional']}")

print()
print("=== BEST SURVIVORS ===")
print("BEST_ANY=" + compact(best_any))
print("BEST_STRICT=" + compact(best_strict))
print("BEST_GREEN=" + compact(best_green))
print("BEST_MAJOR=" + compact(best_major))
print("BEST_EXCEPTIONAL=" + compact(best_exceptional))

print()
print("=== 027B DECISION ===")
print("027B_DECISION=" + decision)
print("NEXT=" + next_step)
print("026C_N89_STILL_REQUIRED=YES")

print()
print("=== CLAIM BOUNDARIES ===")
print("TRUE_ANTIGRAVITY_BRANCH=YES")
print("MICROSCOPIC_FIELD_REALIZATION=NO")
print("FULL_DYNAMIC_LOCAL_TMUNU_CONSERVATION=NO")
print("REACTION_MOMENTUM_CLOSED=NO")
print("RADIATION_LIFETIME_CLOSED=NO")
print("FULL_STABILITY=NO")
print("NONLINEAR_GR=NO")
print("REMOVES_1_OVER_G_SCALING=NO")
print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
print("NEW_PHYSICS_DISCOVERY=NO")
print("HEURISTIC_90_PERCENT_AUTHORIZED=NO")

print()
print(f"SUMMARY_JSON={OUT_SUMMARY}")
print(f"TOP_CSV={OUT_TOP}")
print(f"POTENTIAL_AUDIT_CSV={OUT_POT}")
print(f"PHASE_CONTROL_CSV={OUT_CONTROLS}")
print("027B_RUN_COMPLETE=YES")
