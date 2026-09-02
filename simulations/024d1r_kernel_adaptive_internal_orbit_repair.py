#!/usr/bin/env python3
"""024D1R — kernel-adaptive internal-orbit repair and decisive gate.

PURPOSE
-------
Repair the principal test-design weakness in 024D1 and decide whether internal
poloidal/helical transport contains genuine source-level gravitational leverage.

024D1 prescribed the negative-active interaction at the geometric top of a
torus and the compensating reset at the geometric bottom.  For an on-axis
payload, however, the actual gravitational kernel

    K = (1-z) / [rho^2 + (1-z)^2]^(3/2)

is generally maximized and minimized away from those geometric extrema.

024D1R therefore separates three increasingly physical levels:

1. POINT-EXTREMA UPPER BOUND
   Negative stress may use K_max and positive reset may use K_min.  This is an
   optimistic placement bound.  If even this fails, that parameter row is dead.

2. OPTIMAL CONTIGUOUS WINDOWS
   At fixed interaction/reset duties, choose the best contiguous arclength
   windows on the closed orbit.  This is the principal physical prefilter.

3. RELAXED BATHTUB SUBSET BOUND
   Permit noncontiguous high-K / low-K subsets at the same duties.  This
   diagnoses whether localization, rather than the stress ledger itself, is the
   remaining obstruction.

The run also repairs another 024D1 overreach: Fenchel's theorem proves

    integral kappa ds >= 2*pi

for a closed space curve, but does NOT by itself prove that support energy must
scale linearly with total curvature.  024D1R therefore evaluates both:

    DEC_FLOOR:
        minimum local counterflow support energy beta^2 E,

and

    CURVATURE_PROXY:
        an explicitly heuristic engineering penalty using total curvature.

The two are never conflated.

SCIENTIFIC QUESTION
-------------------
Can kernel-adaptive poloidal/helical transport, with complete positive-energy
inventory, DEC-compatible support floor, full-cycle virial compensation and
finite reset windows, produce a robust finite-payload outward response that:

    C < C_006D = 23.591586299249

and possibly improve the relaxed 024D scalar result:

    C_024D_scalar = 6.610457607426174?

SECONDARY QUESTION
------------------
Does internal spin improve a KINETICALLY LIMITED orbiting converter once spin
energy and its own DEC support energy are included?

ANALYTIC CONTROLS
-----------------
Pure toroidal orbit (q=0):

    rho = constant,
    z = constant,
    K = constant.

The virial reset exactly cancels the conversion stress at the same kernel:

    d D K - d_reset C_reset K = 0.

Therefore only the positive baseline remains and the full-cycle axial response
is inward.  Pure toroidal transport is an exact RED control for the stationary
on-axis payload in this model.

For q>0, K is independent of toroidal azimuth phi for an on-axis payload.  The
p winding therefore cannot create new instantaneous kernel values; it can only
change arclength dwell and curvature.  This makes pure poloidal transport the
natural low-complexity benchmark.

STRESS-CONVERSION LEDGER
------------------------
Normalize non-spin mobile orbital energy to 1.  Let:

    beta_o = orbital speed,
    s      = spin energy / orbital mobile energy,
    beta_s = internal spin speed.

Mobile energy:

    E_m = 1 + s.

Mobile active source before conversion:

    S_m = (1+beta_o^2) + s(1+beta_s^2).

Define:

    r_m = S_m / E_m.

A canonical-scalar-like potential-dominated converter is parameterized by:

    S_conv / rho = -q_s,
    0 <= q_s <= 2.

If fraction f of mobile energy converts, the active-source decrease is:

    D = f E_m (q_s + r_m).

The same change in spatial trace must be repaid over a closed cycle.  The most
favorable DEC-saturating positive reset has trace/rho = +3, giving reset
capacity relative to the mobile state:

    C_reset = E_m (4-r_m).

Thus:

    d_reset = d_int D / C_reset.

The interaction and reset windows must be disjoint and satisfy:

    d_int + d_reset <= 1.

DEC SUPPORT FLOOR
-----------------
For counterpropagating orbiting streams, the tangential kinetic pressure is
beta_o^2 E.  The optimistic local support floor retained from 024D is:

    E_guide >= beta_o^2 E.

At equality, guide energy plus required tension is active-neutral in the
one-dimensional support direction.  Extra support energy is positive-active.

Internal spin receives the analogous floor:

    E_spin_guide >= s beta_s^2.

CURVATURE PROXY
---------------
Compute exact numerical total curvature:

    Kappa_total = integral kappa ds.

Define:

    curvature_norm = Kappa_total/(2*pi) >= 1.

A separate engineering-proxy family multiplies the support floor by
curvature_norm and scanned support multipliers.  This is deliberately labeled
HEURISTIC_PROXY rather than a theorem.

GEOMETRY
--------
Standard toroidal path:

    theta(u) = q u + delta,
    phi(u)   = p u,

    rho(u) = R + a cos(theta),

    x = rho cos(phi),
    y = rho sin(phi),

    z = -g - a + a sin(theta),

with:

    R > a > 0,
    g >= 0,
    0 <= u < 2*pi.

All sources remain at z<=0.  The payload center is at (0,0,1).

WINDINGS
--------
Test:

    (1,0)   pure toroidal control
    (0,1)   pure poloidal
    (1,1)
    (2,1)
    (3,1)
    (1,2)
    (2,3)
    (3,2)
    (5,2)
    (5,3)

LARGE SCAN
----------
Use 2^20 = 1,048,576 scrambled Sobol geometries/field ledgers.

The first stage uses exact per-orbit K_max, K_min and <K> to compute the best
POINT-EXTREMA placement bound analytically.  No arbitrary geometric top/bottom
phase is used.

Promising rows receive:

    4096-point medium contiguous-window optimization,
    16384-point high refinement,
    65536-point independent final reconstruction of the best survivor.

The contiguous optimizer works in arclength probability measure and allows
partial endpoint cells, so requested duties are represented accurately.

MODEL FAMILIES
--------------
1. IDEAL_KERNEL_ADAPTIVE_DEC_FLOOR

   q_s = 2,
   f = 1,
   no spin,
   no converter overhead,
   DEC support floor only.

   This is a source-level ceiling, not a field realization.

2. SCALAR_DEC_FLOOR_NO_SPIN

   scanned q_s and f,
   scanned active-neutral scalar-gradient/localization overhead,
   DEC support floor.

3. SCALAR_CURVATURE_PROXY_NO_SPIN

   same scalar converter,
   heuristic total-curvature support penalty.

4. KINETIC_DEC_FLOOR_NO_SPIN

   conversion fraction limited by relativistic kinetic fraction:

       f <= 1-sqrt(1-beta_o^2).

   converter overhead is positive-active.

5. KINETIC_DEC_FLOOR_WITH_SPIN

   mobile spin energy included.
   Convertible fraction is limited by the combined orbital and spin kinetic
   reservoirs.

6. ELASTIC_CURVATURE_PROXY_WITH_SPIN

   scanned scalar conversion with curvature/concentration support penalties and
   additional implementation overhead.  This is a generic elastic-field
   prefilter, not the old 018B KLS realization.

REPAIR WITNESS
--------------
Before the large campaign, independently evaluate the diagnostic geometry:

    R=1,
    a=0.65,
    g=0,
    (p,q)=(0,1),
    beta_o=0.05,
    q_s=2,
    f=1.

Compare:

    geometric top/bottom windows

against:

    kernel-adaptive contiguous windows.

This case is a REPAIR REGRESSION ONLY.  It cannot earn scientific promotion.
It exists to prove that the new algorithm actually addresses the diagnosed
024D1 phase-placement bug.

FINITE PAYLOAD
--------------
Payload radius:

    R_p/h = 0.043298860805059215.

All source points remain outside the spherical payload.  In source-free
linearized gravity each acceleration component is harmonic inside the sphere,
so the payload-center value equals the uniform sphere COM average by the
mean-value property.

DIRECTIONAL BUNDLES
-------------------
For the best high-resolution survivor, rotate identical orbit/source profiles
around the z-axis in bundles:

    N = 1, 2, 4, 8.

Total energy remains fixed.  Evaluate a target disk through r/h=0.5 and report
axial flatness and maximum transverse/axial response.

SPIN AUDIT
----------
If a no-spin scalar orbit survives, hold its geometry and scalar conversion
strength fixed.  Use a 2^15 Sobol spin/orbit population to compare:

    unrestricted conversion

and

    kinetic-limited conversion.

Only the kinetic-limited branch can promote spin as a physical enabler.

PROMOTION CONDITIONS
--------------------
A source-level orbit survivor requires:

    refined contiguous A > 0,
    finite disjoint reset window,
    virial compensation satisfied,
    payload clear,
    C_high < C_006D,
    medium/high coefficient convergence <= 10%,
    independent 65536-point reconstruction <= 3%.

A major source-headroom result additionally requires:

    C_high < C_024D_scalar.

An orbital-topology promotion requires q>0 and improvement over the exact pure
q=0 control.

A genuine spin promotion additionally requires:

    kinetic-limited orbit+spin C < C_006D,
    spin fraction >= 0.10,
    beta_spin >= 0.25,
    >= 5% improvement over the no-spin kinetic-limited optimum.

FALSIFIERS / STOP RULE
----------------------
If even IDEAL_KERNEL_ADAPTIVE_DEC_FLOOR has no positive refined contiguous
case, close internal-orbit transport strongly.

If the point-extrema ceiling is positive but every contiguous realization is
negative, record LOCALIZATION_OBSTRUCTION and close this orbital path class.

If only DEC-floor families survive while every curvature/elastic proxy is much
worse, retain source-level geometry headroom but do not promote a microscopic
field.

If unrestricted scalar survives but kinetic-limited families do not, return to
the minimal canonical-scalar converter: stress conversion and kernel placement
are the drivers, not orbit kinetic energy.

If a robust constrained orbit survives, only then authorize a microscopic
poloidal/helical field prefilter.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_KERNEL_ADAPTIVE_INTERNAL_ORBIT_REPAIR_PREFILTER

DOES NOT ESTABLISH
------------------
- a microscopic field solution;
- dynamic local T_munu conservation through conversion/reset;
- stability;
- nonlinear GR;
- escape from 1/G scaling;
- experimental antigravity;
- reactionless propulsion;
- a practical device.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import qmc


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results/data"

INPUT = DATA / "024d1_internal_toroidal_orbit_and_spin_summary.json"

OUT_SUMMARY = DATA / "024d1r_kernel_adaptive_internal_orbit_repair_summary.json"
OUT_TOP = DATA / "024d1r_kernel_adaptive_internal_orbit_repair_top.csv"
OUT_WINDING = DATA / "024d1r_kernel_adaptive_winding_summary.csv"
OUT_SPIN = DATA / "024d1r_kernel_adaptive_spin_audit.csv"
OUT_NPZ = DATA / "024d1r_kernel_adaptive_best_profiles.npz"

C006D = 23.591586299249
C024D_SCALAR = 6.610457607426174
PAYLOAD_RADIUS_OVER_H = 0.043298860805059215

SOBOL_POWER = 20
N_CASES = 2 ** SOBOL_POWER
COARSE_NPHASE = 512
MEDIUM_NPHASE = 4096
HIGH_NPHASE = 16384
INDEPENDENT_NPHASE = 65536
VECTOR_NPHASE = 32768
BATCH = 512

TOP_OVERALL_MEDIUM = 30
TOP_PER_WINDING_MEDIUM = 3
TOP_HIGH_PER_FAMILY = 8

CONVERGENCE_TOL = 0.10
INDEPENDENT_TOL = 0.03

WINDINGS = (
    (1, 0),
    (0, 1),
    (1, 1),
    (2, 1),
    (3, 1),
    (1, 2),
    (2, 3),
    (3, 2),
    (5, 2),
    (5, 3),
)

FAMILIES = (
    "IDEAL_KERNEL_ADAPTIVE_DEC_FLOOR",
    "SCALAR_DEC_FLOOR_NO_SPIN",
    "SCALAR_CURVATURE_PROXY_NO_SPIN",
    "KINETIC_DEC_FLOOR_NO_SPIN",
    "KINETIC_DEC_FLOOR_WITH_SPIN",
    "ELASTIC_CURVATURE_PROXY_WITH_SPIN",
)

BUNDLE_COUNTS = (1, 2, 4, 8)

BLIND_WILDCARDS = (0.625, 1.6, 1.875, 3.125, 5.0)


@dataclass(frozen=True)
class Ledger:
    family: str
    beta_orbit: float
    spin_fraction: float
    beta_spin: float
    q_scalar: float
    f: float
    guide_orbit_factor: float
    guide_spin_factor: float
    overhead: float
    overhead_active_ratio: float


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def relerr(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0e-300)


def kinetic_fraction(beta: np.ndarray | float) -> np.ndarray | float:
    return 1.0 - np.sqrt(np.maximum(0.0, 1.0 - np.asarray(beta) ** 2))


def build_parameters() -> dict[str, np.ndarray]:
    """One million broad geometry/ledger samples."""

    sampler = qmc.Sobol(d=13, scramble=True, seed=240111)
    u = sampler.random_base2(SOBOL_POWER)

    major = 10.0 ** (
        math.log10(0.25)
        + (math.log10(10.0) - math.log10(0.25)) * u[:, 0]
    )

    minor_ratio = 0.05 + (0.92 - 0.05) * u[:, 1]
    minor = major * minor_ratio
    gap = 1.5 * u[:, 2]

    winding_index = np.minimum(
        (u[:, 3] * len(WINDINGS)).astype(int),
        len(WINDINGS) - 1,
    )

    p = np.asarray([WINDINGS[i][0] for i in winding_index], dtype=float)
    q_winding = np.asarray([WINDINGS[i][1] for i in winding_index], dtype=float)

    phase = 2.0 * math.pi * u[:, 4]
    beta_orbit = 0.01 + (0.9995 - 0.01) * u[:, 5]
    spin_fraction = 3.0 * u[:, 6]
    beta_spin = 0.999 * u[:, 7]
    q_scalar = 2.0 * u[:, 8]
    f_raw = u[:, 9]
    guide_multiplier = 1.0 + 2.0 * u[:, 10]
    spin_guide_multiplier = 1.0 + 2.0 * u[:, 11]
    overhead = 2.0 * u[:, 12]

    return {
        "major": major,
        "minor": minor,
        "minor_ratio": minor_ratio,
        "gap": gap,
        "winding_index": winding_index,
        "p": p,
        "q_winding": q_winding,
        "phase": phase,
        "beta_orbit": beta_orbit,
        "spin_fraction": spin_fraction,
        "beta_spin": beta_spin,
        "q_scalar": q_scalar,
        "f_raw": f_raw,
        "guide_multiplier": guide_multiplier,
        "spin_guide_multiplier": spin_guide_multiplier,
        "overhead": overhead,
    }


def coarse_geometry(pset: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Kernel extrema/average and exact geometric curvature diagnostics."""

    n = len(pset["major"])

    k_avg = np.empty(n)
    k_max = np.empty(n)
    k_min = np.empty(n)
    curvature_norm = np.empty(n)
    curvature_concentration = np.empty(n)
    min_payload_distance = np.empty(n)

    u = np.linspace(0.0, 2.0 * math.pi, COARSE_NPHASE, endpoint=False)[None, :]
    du = 2.0 * math.pi / COARSE_NPHASE

    for start in range(0, n, BATCH):
        stop = min(start + BATCH, n)

        R = pset["major"][start:stop, None]
        a = pset["minor"][start:stop, None]
        g = pset["gap"][start:stop, None]
        p = pset["p"][start:stop, None]
        q = pset["q_winding"][start:stop, None]
        phase = pset["phase"][start:stop, None]

        theta = q * u + phase
        phi = p * u

        st = np.sin(theta)
        ct = np.cos(theta)
        sp = np.sin(phi)
        cp = np.cos(phi)

        rho = R + a * ct
        z = -g - a + a * st

        drho = -a * q * st
        d2rho = -a * q * q * ct
        dz = a * q * ct
        d2z = -a * q * q * st

        dx = drho * cp - rho * p * sp
        dy = drho * sp + rho * p * cp

        d2x = d2rho * cp - 2.0 * drho * p * sp - rho * p * p * cp
        d2y = d2rho * sp + 2.0 * drho * p * cp - rho * p * p * sp

        speed = np.sqrt(dx * dx + dy * dy + dz * dz)

        # q=0,p=0 is not present in WINDINGS; all paths are regular.
        if np.any(speed <= 1.0e-14):
            raise RuntimeError("Encountered non-regular coarse orbit.")

        weights = speed / np.sum(speed, axis=1)[:, None]

        dzp = 1.0 - z
        d2 = rho * rho + dzp * dzp
        kernel = dzp / d2 ** 1.5

        k_avg[start:stop] = np.sum(weights * kernel, axis=1)
        k_max[start:stop] = np.max(kernel, axis=1)
        k_min[start:stop] = np.min(kernel, axis=1)
        min_payload_distance[start:stop] = np.sqrt(np.min(d2, axis=1))

        cx = dy * d2z - dz * d2y
        cy = dz * d2x - dx * d2z
        cz = dx * d2y - dy * d2x

        curvature = np.sqrt(cx * cx + cy * cy + cz * cz) / speed ** 3
        length = np.sum(speed, axis=1) * du
        total_curvature = np.sum(curvature * speed, axis=1) * du

        c_norm = total_curvature / (2.0 * math.pi)
        c_mean = total_curvature / np.maximum(length, 1.0e-300)
        c_conc = np.max(curvature, axis=1) / np.maximum(c_mean, 1.0e-300)

        curvature_norm[start:stop] = c_norm
        curvature_concentration[start:stop] = c_conc

    return {
        "k_avg": k_avg,
        "k_max": k_max,
        "k_min": k_min,
        "curvature_norm": curvature_norm,
        "curvature_concentration": curvature_concentration,
        "min_payload_distance": min_payload_distance,
    }


def family_arrays(
    family: str,
    pset: dict[str, np.ndarray],
    geom: dict[str, np.ndarray],
) -> dict[str, np.ndarray]:
    """Return complete vectorized ledger and best point-extrema bound."""

    beta_o = pset["beta_orbit"]
    s_scan = pset["spin_fraction"]
    beta_s_scan = pset["beta_spin"]
    q_scan = pset["q_scalar"]
    f_scan = pset["f_raw"]

    ones = np.ones_like(beta_o)
    zeros = np.zeros_like(beta_o)

    if family == "IDEAL_KERNEL_ADAPTIVE_DEC_FLOOR":
        s = zeros
        beta_s = zeros
        q_scalar = 2.0 * ones
        f = ones
        guide_o = ones
        guide_s = ones
        overhead = zeros
        overhead_active_ratio = 0.0

    elif family == "SCALAR_DEC_FLOOR_NO_SPIN":
        s = zeros
        beta_s = zeros
        q_scalar = q_scan
        f = f_scan
        guide_o = ones
        guide_s = ones
        overhead = pset["overhead"]
        # Favorable canonical-scalar gradient/localization bookkeeping.
        overhead_active_ratio = 0.0

    elif family == "SCALAR_CURVATURE_PROXY_NO_SPIN":
        s = zeros
        beta_s = zeros
        q_scalar = q_scan
        f = f_scan
        guide_o = (
            pset["guide_multiplier"]
            * np.maximum(geom["curvature_norm"], 1.0)
        )
        guide_s = ones
        overhead = pset["overhead"]
        overhead_active_ratio = 0.0

    elif family == "KINETIC_DEC_FLOOR_NO_SPIN":
        s = zeros
        beta_s = zeros
        q_scalar = q_scan
        f = np.minimum(f_scan, kinetic_fraction(beta_o))
        guide_o = ones
        guide_s = ones
        overhead = 0.20 + pset["overhead"]
        overhead_active_ratio = 1.0

    elif family == "KINETIC_DEC_FLOOR_WITH_SPIN":
        s = s_scan
        beta_s = beta_s_scan
        q_scalar = q_scan
        mobile = 1.0 + s
        accessible = kinetic_fraction(beta_o) + s * kinetic_fraction(beta_s)
        f = np.minimum(f_scan, accessible / mobile)
        guide_o = ones
        guide_s = ones
        overhead = 0.20 + pset["overhead"]
        overhead_active_ratio = 1.0

    elif family == "ELASTIC_CURVATURE_PROXY_WITH_SPIN":
        s = s_scan
        beta_s = beta_s_scan
        q_scalar = q_scan
        f = f_scan
        cn = np.maximum(geom["curvature_norm"], 1.0)
        cc = np.maximum(geom["curvature_concentration"], 1.0)
        guide_o = pset["guide_multiplier"] * cn * np.sqrt(cc)
        guide_s = pset["spin_guide_multiplier"] * np.sqrt(cc)
        overhead = 0.50 + pset["overhead"]
        overhead_active_ratio = 0.5

    else:
        raise RuntimeError(f"Unknown family: {family}")

    bo2 = beta_o * beta_o
    bs2 = beta_s * beta_s

    mobile_energy = 1.0 + s
    mobile_active = 1.0 + bo2 + s * (1.0 + bs2)
    mobile_ratio = mobile_active / mobile_energy

    orbit_guide_energy = guide_o * bo2
    spin_guide_energy = guide_s * s * bs2

    # At support-floor equality the necessary tension cancels the corresponding
    # kinetic-pressure active contribution.  Only guide energy above the floor
    # is positive-active overhead.
    baseline_active = (
        mobile_active
        + np.maximum(guide_o - 1.0, 0.0) * bo2
        + np.maximum(guide_s - 1.0, 0.0) * s * bs2
        + overhead_active_ratio * overhead
    )

    inventory = mobile_energy + orbit_guide_energy + spin_guide_energy + overhead

    D = f * mobile_energy * (q_scalar + mobile_ratio)
    reset_capacity = mobile_energy * (4.0 - mobile_ratio)

    ratio = np.divide(
        D,
        reset_capacity,
        out=np.full_like(D, np.inf),
        where=reset_capacity > 1.0e-12,
    )

    # Maximum legal interaction duty before interaction+reset fill the cycle.
    d_max = np.divide(
        0.995,
        1.0 + ratio,
        out=np.zeros_like(ratio),
        where=np.isfinite(ratio),
    )

    placement_slope = (
        D * (geom["k_max"] - geom["k_min"])
        - overhead_active_ratio * overhead * geom["k_max"]
    )

    A_point = -baseline_active * geom["k_avg"] + d_max * placement_slope

    pure_toroidal = pset["q_winding"] == 0.0
    payload_clear = geom["min_payload_distance"] > PAYLOAD_RADIUS_OVER_H

    # Exact q=0 control: constant kernel, so numerical noise cannot create a
    # false positive.
    A_point = np.where(pure_toroidal, -baseline_active * geom["k_avg"], A_point)

    C_point = np.where(
        payload_clear & (A_point > 0.0),
        inventory / A_point,
        np.inf,
    )

    return {
        "beta_orbit": beta_o,
        "spin_fraction": s,
        "beta_spin": beta_s,
        "q_scalar": q_scalar,
        "f": f,
        "guide_orbit_factor": guide_o,
        "guide_spin_factor": guide_s,
        "overhead": overhead,
        "overhead_active_ratio": np.full_like(beta_o, overhead_active_ratio),
        "mobile_energy": mobile_energy,
        "mobile_active_ratio": mobile_ratio,
        "baseline_active": baseline_active,
        "inventory": inventory,
        "D": D,
        "reset_capacity": reset_capacity,
        "d_point": d_max,
        "A_point": A_point,
        "C_point": C_point,
    }


def top_indices(values: np.ndarray, count: int) -> np.ndarray:
    finite = np.flatnonzero(np.isfinite(values))
    if finite.size == 0:
        return np.asarray([], dtype=int)
    if finite.size <= count:
        return finite[np.argsort(values[finite])]
    local = np.argpartition(values[finite], count - 1)[:count]
    chosen = finite[local]
    return chosen[np.argsort(values[chosen])]


def candidate_from_index(
    family: str,
    index: int,
    pset: dict[str, np.ndarray],
    geom: dict[str, np.ndarray],
    result: dict[str, np.ndarray],
) -> dict[str, Any]:
    wi = int(pset["winding_index"][index])
    winding = WINDINGS[wi]

    keys_pset = (
        "major",
        "minor",
        "minor_ratio",
        "gap",
        "phase",
    )

    out: dict[str, Any] = {
        "family": family,
        "index": int(index),
        "winding_index": wi,
        "p": int(winding[0]),
        "q_winding": int(winding[1]),
    }

    for key in keys_pset:
        out[key] = float(pset[key][index])

    for key in (
        "beta_orbit",
        "spin_fraction",
        "beta_spin",
        "q_scalar",
        "f",
        "guide_orbit_factor",
        "guide_spin_factor",
        "overhead",
        "overhead_active_ratio",
        "mobile_energy",
        "mobile_active_ratio",
        "baseline_active",
        "inventory",
        "D",
        "reset_capacity",
        "d_point",
        "A_point",
        "C_point",
    ):
        out[key] = float(result[key][index])

    for key in (
        "k_avg",
        "k_max",
        "k_min",
        "curvature_norm",
        "curvature_concentration",
        "min_payload_distance",
    ):
        out[key] = float(geom[key][index])

    return out


def choose_medium_candidates(
    family: str,
    pset: dict[str, np.ndarray],
    geom: dict[str, np.ndarray],
    result: dict[str, np.ndarray],
) -> list[dict[str, Any]]:
    chosen: set[int] = set(
        int(i)
        for i in top_indices(result["C_point"], TOP_OVERALL_MEDIUM)
    )

    for wi in range(len(WINDINGS)):
        mask = pset["winding_index"] == wi
        indices = np.flatnonzero(mask & np.isfinite(result["C_point"]))
        if indices.size == 0:
            continue
        count = min(TOP_PER_WINDING_MEDIUM, indices.size)
        local = top_indices(result["C_point"][indices], count)
        for li in local:
            chosen.add(int(indices[int(li)]))

    return [
        candidate_from_index(family, i, pset, geom, result)
        for i in sorted(chosen)
    ]


def orbit_arrays(candidate: dict[str, Any], nphase: int) -> dict[str, Any]:
    """Complete high-resolution torus path and kernel."""

    u = np.linspace(0.0, 2.0 * math.pi, nphase, endpoint=False)

    R = float(candidate["major"])
    a = float(candidate["minor"])
    g = float(candidate["gap"])
    p = float(candidate["p"])
    q = float(candidate["q_winding"])
    phase = float(candidate["phase"])

    theta = q * u + phase
    phi = p * u

    st = np.sin(theta)
    ct = np.cos(theta)
    sp = np.sin(phi)
    cp = np.cos(phi)

    rho = R + a * ct
    x = rho * cp
    y = rho * sp
    z = -g - a + a * st

    drho = -a * q * st
    d2rho = -a * q * q * ct
    dz = a * q * ct
    d2z = -a * q * q * st

    dx = drho * cp - rho * p * sp
    dy = drho * sp + rho * p * cp
    d2x = d2rho * cp - 2.0 * drho * p * sp - rho * p * p * cp
    d2y = d2rho * sp + 2.0 * drho * p * cp - rho * p * p * sp

    speed = np.sqrt(dx * dx + dy * dy + dz * dz)
    if np.any(speed <= 1.0e-14):
        raise RuntimeError("Non-regular refined orbit.")

    weights = speed / np.sum(speed)

    dzp = 1.0 - z
    d2 = x * x + y * y + dzp * dzp
    kernel = dzp / d2 ** 1.5

    cx = dy * d2z - dz * d2y
    cy = dz * d2x - dx * d2z
    cz = dx * d2y - dy * d2x
    curvature = np.sqrt(cx * cx + cy * cy + cz * cz) / speed ** 3

    du = 2.0 * math.pi / nphase
    length = float(np.sum(speed) * du)
    total_curvature = float(np.sum(curvature * speed) * du)

    return {
        "u": u,
        "theta": theta,
        "phi": phi,
        "x": x,
        "y": y,
        "z": z,
        "weights": weights,
        "kernel": kernel,
        "k_avg": float(np.sum(weights * kernel)),
        "k_max": float(np.max(kernel)),
        "k_min": float(np.min(kernel)),
        "imax": int(np.argmax(kernel)),
        "imin": int(np.argmin(kernel)),
        "length": length,
        "curvature_norm": total_curvature / (2.0 * math.pi),
        "curvature_concentration": float(
            np.max(curvature)
            / max(total_curvature / length, 1.0e-300)
        ),
        "min_payload_distance": float(np.sqrt(np.min(d2))),
    }


def build_profile_from_interval(
    n: int,
    start: int,
    full_end: int,
    partial_fraction: float,
) -> np.ndarray:
    """Fractional occupancy of one circular contiguous interval."""

    profile = np.zeros(n, dtype=float)

    count_full = full_end - start
    if count_full > 0:
        idx = np.arange(start, full_end) % n
        profile[idx] = 1.0

    if partial_fraction > 0.0:
        profile[full_end % n] = max(
            profile[full_end % n],
            min(1.0, partial_fraction),
        )

    return profile


def best_contiguous_window(
    kernel: np.ndarray,
    weights: np.ndarray,
    target_duty: float,
    *,
    maximize: bool,
    forbidden: np.ndarray | None = None,
) -> dict[str, Any] | None:
    """Best circular contiguous window of exact arclength-probability duty."""

    n = len(kernel)

    if not (0.0 < target_duty < 1.0):
        return None

    k2 = np.concatenate((kernel, kernel))
    w2 = np.concatenate((weights, weights))

    cw = np.concatenate(([0.0], np.cumsum(w2)))
    cwk = np.concatenate(([0.0], np.cumsum(w2 * k2)))

    starts = np.arange(n, dtype=int)
    targets = cw[starts] + target_duty
    ends = np.searchsorted(cw, targets, side="left")
    ends = np.minimum(ends, starts + n)

    full_end = np.maximum(ends - 1, starts)
    duty_before = cw[full_end] - cw[starts]
    remaining = np.maximum(0.0, target_duty - duty_before)

    last_weights = w2[full_end]
    partial = np.divide(
        remaining,
        np.maximum(last_weights, 1.0e-300),
    )
    partial = np.clip(partial, 0.0, 1.0)

    ksum = (
        cwk[full_end]
        - cwk[starts]
        + remaining * k2[full_end]
    )

    averages = ksum / target_duty

    if forbidden is not None:
        forbidden_bool = np.asarray(forbidden > 1.0e-12, dtype=float)
        f2 = np.concatenate((forbidden_bool, forbidden_bool))
        cwf = np.concatenate(([0.0], np.cumsum(w2 * f2)))
        overlap = cwf[full_end] - cwf[starts]
        overlap += remaining * f2[full_end]
        invalid = overlap > 1.0e-12
    else:
        invalid = np.zeros(n, dtype=bool)

    if np.all(invalid):
        return None

    if maximize:
        scores = np.where(invalid, -np.inf, averages)
        best = int(np.argmax(scores))
    else:
        scores = np.where(invalid, np.inf, averages)
        best = int(np.argmin(scores))

    if not np.isfinite(scores[best]):
        return None

    profile = build_profile_from_interval(
        n,
        int(starts[best]),
        int(full_end[best]),
        float(partial[best]),
    )

    actual_duty = float(np.sum(weights * profile))
    actual_k = float(
        np.sum(weights * profile * kernel)
        / max(actual_duty, 1.0e-300)
    )

    return {
        "profile": profile,
        "duty": actual_duty,
        "kernel": actual_k,
        "start": int(starts[best]),
        "end": int(full_end[best] % n),
        "partial": float(partial[best]),
    }


def best_relaxed_subset(
    kernel: np.ndarray,
    weights: np.ndarray,
    target_duty: float,
    *,
    maximize: bool,
    forbidden: np.ndarray | None = None,
) -> dict[str, Any] | None:
    """Bathtub-principle noncontiguous subset at exact weighted duty."""

    if not (0.0 < target_duty < 1.0):
        return None

    allowed = np.ones(len(kernel), dtype=bool)
    if forbidden is not None:
        allowed &= forbidden <= 1.0e-12

    indices = np.flatnonzero(allowed)
    if indices.size == 0:
        return None

    order_local = np.argsort(kernel[indices])
    if maximize:
        order_local = order_local[::-1]
    order = indices[order_local]

    profile = np.zeros(len(kernel), dtype=float)
    remaining = target_duty

    for idx in order:
        if remaining <= 1.0e-15:
            break
        take = min(float(weights[idx]), remaining)
        profile[idx] = take / max(float(weights[idx]), 1.0e-300)
        remaining -= take

    if remaining > 5.0e-12:
        return None

    duty = float(np.sum(weights * profile))
    kval = float(
        np.sum(weights * profile * kernel)
        / max(duty, 1.0e-300)
    )

    return {
        "profile": profile,
        "duty": duty,
        "kernel": kval,
    }


def duty_grid(max_duty: float, count: int) -> np.ndarray:
    if max_duty <= 0.006:
        return np.asarray([], dtype=float)

    low_end = min(0.10, 0.70 * max_duty)
    parts = []

    if low_end > 0.005:
        parts.append(np.geomspace(0.005, low_end, max(12, count // 3)))

    start = max(0.01, low_end)
    if max_duty > start:
        parts.append(np.linspace(start, max_duty, max(20, 2 * count // 3)))

    if not parts:
        return np.asarray([], dtype=float)

    return np.unique(np.concatenate(parts))


def optimize_orbit(
    candidate: dict[str, Any],
    nphase: int,
    *,
    mode: str,
    duty_count: int,
) -> dict[str, Any]:
    """Optimize exact finite interaction/reset windows."""

    orbit = orbit_arrays(candidate, nphase)

    if candidate["q_winding"] == 0:
        return {
            **candidate,
            "nphase": nphase,
            "mode": mode,
            "C": math.inf,
            "A": -float(candidate["baseline_active"]) * orbit["k_avg"],
            "orbit": orbit,
            "reason": "PURE_TOROIDAL_CONSTANT_KERNEL",
        }

    D = float(candidate["D"])
    cap = float(candidate["reset_capacity"])
    baseline = float(candidate["baseline_active"])
    inventory = float(candidate["inventory"])
    overhead = float(candidate["overhead"])
    overhead_active_ratio = float(candidate["overhead_active_ratio"])

    if cap <= 1.0e-12 or D <= 0.0:
        return {
            **candidate,
            "nphase": nphase,
            "mode": mode,
            "C": math.inf,
            "A": -baseline * orbit["k_avg"],
            "orbit": orbit,
            "reason": "NO_CONVERSION_CAPACITY",
        }

    reset_ratio = D / cap
    max_duty = 0.995 / (1.0 + reset_ratio)

    best: dict[str, Any] | None = None

    for d in duty_grid(max_duty, duty_count):
        r = d * reset_ratio

        if d + r >= 0.9999:
            continue

        if mode == "CONTIGUOUS":
            top = best_contiguous_window(
                orbit["kernel"],
                orbit["weights"],
                float(d),
                maximize=True,
            )
            if top is None:
                continue
            reset = best_contiguous_window(
                orbit["kernel"],
                orbit["weights"],
                float(r),
                maximize=False,
                forbidden=top["profile"],
            )
        elif mode == "RELAXED_BATHTUB":
            top = best_relaxed_subset(
                orbit["kernel"],
                orbit["weights"],
                float(d),
                maximize=True,
            )
            if top is None:
                continue
            reset = best_relaxed_subset(
                orbit["kernel"],
                orbit["weights"],
                float(r),
                maximize=False,
                forbidden=top["profile"],
            )
        else:
            raise RuntimeError(f"Unknown optimization mode: {mode}")

        if reset is None:
            continue

        A = (
            -baseline * orbit["k_avg"]
            + top["duty"] * D * top["kernel"]
            - reset["duty"] * cap * reset["kernel"]
            - top["duty"]
            * overhead_active_ratio
            * overhead
            * top["kernel"]
        )

        C = inventory / A if A > 0.0 else math.inf

        row = {
            **candidate,
            "nphase": nphase,
            "mode": mode,
            "C": float(C),
            "A": float(A),
            "interaction_duty": float(top["duty"]),
            "reset_duty": float(reset["duty"]),
            "interaction_kernel": float(top["kernel"]),
            "reset_kernel": float(reset["kernel"]),
            "top_profile": top["profile"],
            "reset_profile": reset["profile"],
            "orbit": orbit,
            "payload_clear": bool(
                orbit["min_payload_distance"] > PAYLOAD_RADIUS_OVER_H
            ),
            "beats_006D": bool(C < C006D),
            "beats_024D_scalar": bool(C < C024D_SCALAR),
        }

        if best is None or row["C"] < best["C"]:
            best = row

    if best is None:
        return {
            **candidate,
            "nphase": nphase,
            "mode": mode,
            "C": math.inf,
            "A": -baseline * orbit["k_avg"],
            "orbit": orbit,
            "reason": "NO_FINITE_DISJOINT_WINDOW_SURVIVOR",
        }

    return best


def fixed_center_window(
    orbit: dict[str, Any],
    target_duty: float,
    center_angle: float,
    phase_array_name: str,
) -> dict[str, Any] | None:
    """Old geometric-top/bottom style window for repair witness."""

    phase = np.asarray(orbit[phase_array_name], dtype=float)
    weights = np.asarray(orbit["weights"], dtype=float)
    kernel = np.asarray(orbit["kernel"], dtype=float)

    lo = 0.0
    hi = math.pi

    for _ in range(60):
        mid = 0.5 * (lo + hi)
        dist = np.abs((phase - center_angle + math.pi) % (2.0 * math.pi) - math.pi)
        mask = dist <= mid
        duty = float(np.sum(weights[mask]))
        if duty < target_duty:
            lo = mid
        else:
            hi = mid

    dist = np.abs((phase - center_angle + math.pi) % (2.0 * math.pi) - math.pi)
    mask = dist <= hi
    duty = float(np.sum(weights[mask]))

    if duty <= 0.0:
        return None

    return {
        "profile": mask.astype(float),
        "duty": duty,
        "kernel": float(np.sum(weights[mask] * kernel[mask]) / duty),
    }


def repair_witness() -> dict[str, Any]:
    """Directly demonstrate the phase-placement correction."""

    beta = 0.05
    candidate = {
        "family": "REPAIR_REGRESSION_ONLY",
        "p": 0,
        "q_winding": 1,
        "major": 1.0,
        "minor": 0.65,
        "minor_ratio": 0.65,
        "gap": 0.0,
        "phase": 0.0,
        "beta_orbit": beta,
        "spin_fraction": 0.0,
        "beta_spin": 0.0,
        "q_scalar": 2.0,
        "f": 1.0,
        "guide_orbit_factor": 1.0,
        "guide_spin_factor": 1.0,
        "overhead": 0.0,
        "overhead_active_ratio": 0.0,
    }

    mobile_energy = 1.0
    mobile_active_ratio = 1.0 + beta * beta
    candidate["mobile_energy"] = mobile_energy
    candidate["mobile_active_ratio"] = mobile_active_ratio
    candidate["baseline_active"] = 1.0 + beta * beta
    candidate["inventory"] = 1.0 + beta * beta
    candidate["D"] = 2.0 + mobile_active_ratio
    candidate["reset_capacity"] = 4.0 - mobile_active_ratio
    candidate["C_point"] = math.nan
    candidate["A_point"] = math.nan
    candidate["d_point"] = math.nan

    adaptive = optimize_orbit(
        candidate,
        32768,
        mode="CONTIGUOUS",
        duty_count=120,
    )

    orbit = adaptive["orbit"]
    D = float(candidate["D"])
    cap = float(candidate["reset_capacity"])
    baseline = float(candidate["baseline_active"])
    inventory = float(candidate["inventory"])

    best_old_C = math.inf
    best_old_A = -math.inf
    best_old_d = math.nan

    max_duty = 0.995 / (1.0 + D / cap)

    for d in duty_grid(max_duty, 120):
        r = d * D / cap
        top = fixed_center_window(orbit, float(d), 0.5 * math.pi, "theta")
        reset = fixed_center_window(orbit, float(r), 1.5 * math.pi, "theta")
        if top is None or reset is None:
            continue

        overlap = np.any((top["profile"] > 0.0) & (reset["profile"] > 0.0))
        if overlap:
            continue

        A = (
            -baseline * orbit["k_avg"]
            + top["duty"] * D * top["kernel"]
            - reset["duty"] * cap * reset["kernel"]
        )

        C = inventory / A if A > 0.0 else math.inf

        if C < best_old_C:
            best_old_C = C
            best_old_A = A
            best_old_d = d

    return {
        "geometry": {
            "R": 1.0,
            "a": 0.65,
            "g": 0.0,
            "p": 0,
            "q": 1,
        },
        "k_max": orbit["k_max"],
        "k_min": orbit["k_min"],
        "k_avg": orbit["k_avg"],
        "kernel_max_u": float(orbit["u"][orbit["imax"]]),
        "kernel_min_u": float(orbit["u"][orbit["imin"]]),
        "geometric_top_u": 0.5 * math.pi,
        "geometric_bottom_u": 1.5 * math.pi,
        "old_geometric_best_C": best_old_C,
        "old_geometric_best_A": best_old_A,
        "old_geometric_best_duty": best_old_d,
        "adaptive_best_C": adaptive["C"],
        "adaptive_best_A": adaptive["A"],
        "adaptive_interaction_duty": adaptive.get("interaction_duty", math.nan),
        "adaptive_reset_duty": adaptive.get("reset_duty", math.nan),
        "adaptive_interaction_kernel": adaptive.get("interaction_kernel", math.nan),
        "adaptive_reset_kernel": adaptive.get("reset_kernel", math.nan),
        "adaptive_positive": bool(adaptive["A"] > 0.0),
    }


def public_row(row: dict[str, Any]) -> dict[str, Any]:
    """Strip large arrays for CSV/JSON."""

    out = {}
    for key, value in row.items():
        if key in ("orbit", "top_profile", "reset_profile"):
            continue
        if isinstance(value, np.generic):
            value = value.item()
        if isinstance(value, (str, int, float, bool)) or value is None:
            out[key] = value
    return out


def medium_refinement(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    for i, candidate in enumerate(candidates):
        if i % 40 == 0:
            print(f"MEDIUM_REFINEMENT_PROGRESS={i}/{len(candidates)}", flush=True)
        rows.append(
            optimize_orbit(
                candidate,
                MEDIUM_NPHASE,
                mode="CONTIGUOUS",
                duty_count=72,
            )
        )
    return rows


def choose_high_candidates(
    medium_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    chosen: dict[tuple[str, int], dict[str, Any]] = {}

    for family in FAMILIES:
        rows = [
            r for r in medium_rows
            if r["family"] == family and math.isfinite(float(r["C"]))
        ]
        rows.sort(key=lambda r: float(r["C"]))

        for row in rows[:TOP_HIGH_PER_FAMILY]:
            chosen[(family, int(row["index"]))] = row

        for winding in WINDINGS:
            local = [
                r for r in rows
                if int(r["p"]) == winding[0]
                and int(r["q_winding"]) == winding[1]
            ]
            if local:
                row = local[0]
                chosen[(family, int(row["index"]))] = row

    return list(chosen.values())


def high_refinement(
    medium_selected: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    for i, medium in enumerate(medium_selected):
        if i % 20 == 0:
            print(f"HIGH_REFINEMENT_PROGRESS={i}/{len(medium_selected)}", flush=True)
        candidate = {
            key: value
            for key, value in medium.items()
            if key not in (
                "orbit",
                "top_profile",
                "reset_profile",
                "nphase",
                "mode",
                "C",
                "A",
                "interaction_duty",
                "reset_duty",
                "interaction_kernel",
                "reset_kernel",
                "payload_clear",
                "beats_006D",
                "beats_024D_scalar",
                "reason",
            )
        }
        high = optimize_orbit(
            candidate,
            HIGH_NPHASE,
            mode="CONTIGUOUS",
            duty_count=112,
        )
        high["C_medium"] = float(medium["C"])
        high["A_medium"] = float(medium["A"])
        high["medium_high_relerr"] = (
            relerr(float(medium["C"]), float(high["C"]))
            if math.isfinite(float(high["C"]))
            else math.inf
        )
        rows.append(high)
    return rows


def bathtub_for_best(high: dict[str, Any]) -> dict[str, Any]:
    candidate = {
        key: value
        for key, value in high.items()
        if key not in (
            "orbit",
            "top_profile",
            "reset_profile",
            "nphase",
            "mode",
            "C",
            "A",
            "interaction_duty",
            "reset_duty",
            "interaction_kernel",
            "reset_kernel",
            "payload_clear",
            "beats_006D",
            "beats_024D_scalar",
            "C_medium",
            "A_medium",
            "medium_high_relerr",
        )
    }

    relaxed = optimize_orbit(
        candidate,
        HIGH_NPHASE,
        mode="RELAXED_BATHTUB",
        duty_count=112,
    )

    return relaxed


def independent_reconstruction(high: dict[str, Any]) -> dict[str, Any]:
    candidate = {
        key: value
        for key, value in high.items()
        if key not in (
            "orbit",
            "top_profile",
            "reset_profile",
            "nphase",
            "mode",
            "C",
            "A",
            "interaction_duty",
            "reset_duty",
            "interaction_kernel",
            "reset_kernel",
            "payload_clear",
            "beats_006D",
            "beats_024D_scalar",
            "C_medium",
            "A_medium",
            "medium_high_relerr",
        )
    }

    independent = optimize_orbit(
        candidate,
        INDEPENDENT_NPHASE,
        mode="CONTIGUOUS",
        duty_count=160,
    )

    independent["C_high_reference"] = float(high["C"])
    independent["relative_difference"] = (
        relerr(float(high["C"]), float(independent["C"]))
        if math.isfinite(float(independent["C"]))
        else math.inf
    )
    independent["pass"] = bool(
        math.isfinite(float(independent["C"]))
        and independent["relative_difference"] <= INDEPENDENT_TOL
    )

    return independent


def vector_bundle_audit(high: dict[str, Any], bundle_count: int) -> dict[str, Any]:
    """3-D field morphology for a rotated bundle with total energy fixed."""

    # Rebuild at a dedicated resolution and re-optimize there.
    candidate = {
        key: value
        for key, value in high.items()
        if key not in (
            "orbit",
            "top_profile",
            "reset_profile",
            "nphase",
            "mode",
            "C",
            "A",
            "interaction_duty",
            "reset_duty",
            "interaction_kernel",
            "reset_kernel",
            "payload_clear",
            "beats_006D",
            "beats_024D_scalar",
            "C_medium",
            "A_medium",
            "medium_high_relerr",
        )
    }

    row = optimize_orbit(
        candidate,
        VECTOR_NPHASE,
        mode="CONTIGUOUS",
        duty_count=128,
    )

    if not math.isfinite(float(row["C"])):
        return {
            "bundle_count": bundle_count,
            "valid": False,
        }

    orbit = row["orbit"]
    weights = np.asarray(orbit["weights"], dtype=float)
    source = np.full(len(weights), float(row["baseline_active"]), dtype=float)

    source -= float(row["D"]) * np.asarray(row["top_profile"], dtype=float)
    source += float(row["reset_capacity"]) * np.asarray(row["reset_profile"], dtype=float)
    source += (
        float(row["overhead_active_ratio"])
        * float(row["overhead"])
        * np.asarray(row["top_profile"], dtype=float)
    )

    x0 = np.asarray(orbit["x"], dtype=float)
    y0 = np.asarray(orbit["y"], dtype=float)
    z0 = np.asarray(orbit["z"], dtype=float)

    target_radii = (0.0, 0.125, 0.25, 0.375, 0.5)
    target_phis = np.linspace(0.0, 2.0 * math.pi, 12, endpoint=False)

    all_axial = []
    max_transverse_fraction = 0.0
    per_radius = []

    for tr in target_radii:
        local_axial = []
        local_transverse = []

        for tp in target_phis:
            tx = tr * math.cos(tp)
            ty = tr * math.sin(tp)
            tz = 1.0

            acc = np.zeros(3, dtype=float)

            for b in range(bundle_count):
                angle = 2.0 * math.pi * b / bundle_count
                ca = math.cos(angle)
                sa = math.sin(angle)

                sx = ca * x0 - sa * y0
                sy = sa * x0 + ca * y0

                dx = sx - tx
                dy = sy - ty
                dz = z0 - tz
                invd3 = (dx * dx + dy * dy + dz * dz) ** -1.5

                common = (
                    weights
                    * source
                    * invd3
                    / bundle_count
                )

                acc[0] += float(np.sum(common * dx))
                acc[1] += float(np.sum(common * dy))
                acc[2] += float(np.sum(common * dz))

            axial = float(acc[2])
            transverse = float(math.hypot(acc[0], acc[1]))

            local_axial.append(axial)
            local_transverse.append(transverse)
            all_axial.append(axial)

            if abs(axial) > 1.0e-300:
                max_transverse_fraction = max(
                    max_transverse_fraction,
                    transverse / abs(axial),
                )

        per_radius.append({
            "radius": tr,
            "axial_min": float(np.min(local_axial)),
            "axial_max": float(np.max(local_axial)),
            "axial_mean": float(np.mean(local_axial)),
            "transverse_max": float(np.max(local_transverse)),
        })

    amin = float(np.min(all_axial))
    amax = float(np.max(all_axial))
    amean = float(np.mean(all_axial))
    flatness = (amax - amin) / max(abs(amean), 1.0e-300)
    on_axis = per_radius[0]["axial_mean"]

    return {
        "bundle_count": bundle_count,
        "valid": True,
        "all_axial_outward": bool(amin > 0.0),
        "minimum_axial": amin,
        "maximum_axial": amax,
        "mean_axial": amean,
        "axial_flatness": flatness,
        "maximum_transverse_fraction": max_transverse_fraction,
        "on_axis_A": on_axis,
        "scalar_A": float(row["A"]),
        "on_axis_relative_error": relerr(on_axis, float(row["A"])),
        "per_radius": per_radius,
    }


def spin_audit(best_no_spin: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """2^15 fixed-geometry orbit/spin test with point prefilter and exact refinement."""

    sampler = qmc.Sobol(d=4, scramble=True, seed=240112)
    u = sampler.random_base2(15)

    beta_o = 0.01 + (0.999 - 0.01) * u[:, 0]
    s = 3.0 * u[:, 1]
    beta_s = 0.999 * u[:, 2]
    f_nominal = u[:, 3]

    orbit = orbit_arrays(best_no_spin, 8192)
    kavg = orbit["k_avg"]
    kmax = orbit["k_max"]
    kmin = orbit["k_min"]

    output_rows: list[dict[str, Any]] = []
    best_summary: dict[str, Any] = {}

    for mode in ("UNRESTRICTED", "KINETIC_LIMITED"):
        mobile = 1.0 + s
        bo2 = beta_o * beta_o
        bs2 = beta_s * beta_s
        mobile_active = 1.0 + bo2 + s * (1.0 + bs2)
        ratio_mobile = mobile_active / mobile

        if mode == "UNRESTRICTED":
            f = f_nominal
        else:
            accessible = kinetic_fraction(beta_o) + s * kinetic_fraction(beta_s)
            f = np.minimum(f_nominal, accessible / mobile)

        D = f * mobile * (float(best_no_spin["q_scalar"]) + ratio_mobile)
        cap = mobile * (4.0 - ratio_mobile)

        baseline = mobile_active
        inventory = mobile + bo2 + s * bs2

        reset_ratio = np.divide(
            D,
            cap,
            out=np.full_like(D, np.inf),
            where=cap > 1.0e-12,
        )
        dmax = 0.995 / (1.0 + reset_ratio)
        A_bound = -baseline * kavg + dmax * D * (kmax - kmin)
        C_bound = np.where(A_bound > 0.0, inventory / A_bound, np.inf)

        selected = top_indices(C_bound, 100)
        refined_rows = []

        for idx in selected:
            candidate = {
                **{
                    key: value
                    for key, value in best_no_spin.items()
                    if key not in (
                        "orbit",
                        "top_profile",
                        "reset_profile",
                        "nphase",
                        "mode",
                        "C",
                        "A",
                        "interaction_duty",
                        "reset_duty",
                        "interaction_kernel",
                        "reset_kernel",
                        "payload_clear",
                        "beats_006D",
                        "beats_024D_scalar",
                        "C_medium",
                        "A_medium",
                        "medium_high_relerr",
                    )
                },
                "family": f"SPIN_AUDIT_{mode}",
                "beta_orbit": float(beta_o[idx]),
                "spin_fraction": float(s[idx]),
                "beta_spin": float(beta_s[idx]),
                "f": float(f[idx]),
                "guide_orbit_factor": 1.0,
                "guide_spin_factor": 1.0,
                "overhead": 0.0,
                "overhead_active_ratio": 0.0,
                "mobile_energy": float(mobile[idx]),
                "mobile_active_ratio": float(ratio_mobile[idx]),
                "baseline_active": float(baseline[idx]),
                "inventory": float(inventory[idx]),
                "D": float(D[idx]),
                "reset_capacity": float(cap[idx]),
                "A_point": float(A_bound[idx]),
                "C_point": float(C_bound[idx]),
                "d_point": float(dmax[idx]),
            }

            refined = optimize_orbit(
                candidate,
                8192,
                mode="CONTIGUOUS",
                duty_count=80,
            )
            refined_rows.append(refined)
            output_rows.append(public_row(refined))

        finite = [r for r in refined_rows if math.isfinite(float(r["C"]))]
        finite.sort(key=lambda r: float(r["C"]))

        if finite:
            best = finite[0]
            best_summary[mode] = public_row(best)
        else:
            best_summary[mode] = None

    return output_rows, best_summary


def main() -> None:
    print("=== 024D1R KERNEL-ADAPTIVE INTERNAL-ORBIT REPAIR ===", flush=True)

    require(INPUT)
    prior = json.loads(INPUT.read_text(encoding="utf-8"))

    prior_decision = prior.get("decision", {}).get("024D1")
    if prior_decision != "RED_INTERNAL_TOROIDAL_ORBIT_AND_SPIN_NO_USEFUL_SOURCE_ADVANCE":
        raise RuntimeError(f"Unexpected 024D1 predecessor decision: {prior_decision}")

    print("\n=== A — ANALYTIC / MODEL REPAIRS ===")
    print(f"C_006D={C006D:.15f}")
    print(f"C_024D_SCALAR={C024D_SCALAR:.15f}")
    print("PURE_TOROIDAL_CONSTANT_KERNEL_NO_GO=YES")
    print("ONAXIS_KERNEL_INDEPENDENT_OF_TOROIDAL_AZIMUTH=YES")
    print("GEOMETRIC_TOP_EQUALS_KERNEL_MAX_IN_GENERAL=NO")
    print("FENCHEL_TOTAL_CURVATURE_BOUND=KAPPA_INTEGRAL_GE_2PI")
    print("FENCHEL_BOUND_DIRECTLY_IMPLIES_LINEAR_SUPPORT_ENERGY_MULTIPLIER=NO")
    print("DEC_SUPPORT_FLOOR_AND_CURVATURE_PROXY_SEPARATED=YES")
    print("FULL_CYCLE_VIRIAL_RESET=MANDATORY")
    print("OLD_018B_KLS_REALIZATION_REOPENED=NO")

    print("\n=== B — REPAIR REGRESSION WITNESS ===", flush=True)
    witness = repair_witness()

    print(f"WITNESS_K_MAX={witness['k_max']:.15e}")
    print(f"WITNESS_K_MIN={witness['k_min']:.15e}")
    print(f"WITNESS_K_AVG={witness['k_avg']:.15e}")
    print(f"WITNESS_KERNEL_MAX_U={witness['kernel_max_u']:.15e}")
    print(f"WITNESS_GEOMETRIC_TOP_U={witness['geometric_top_u']:.15e}")
    print(f"WITNESS_OLD_GEOMETRIC_BEST_C={witness['old_geometric_best_C']:.15e}")
    print(f"WITNESS_ADAPTIVE_BEST_C={witness['adaptive_best_C']:.15e}")
    print(f"WITNESS_ADAPTIVE_BEST_A={witness['adaptive_best_A']:+.15e}")
    print(
        "WITNESS_KERNEL_ADAPTIVE_POSITIVE="
        + ("PASS" if witness["adaptive_positive"] else "FAIL")
    )

    if not witness["adaptive_positive"]:
        raise RuntimeError("Kernel-adaptive repair witness did not become positive.")

    print("\n=== C — BUILD 2^20 POINT-EXTREMA CAMPAIGN ===", flush=True)
    pset = build_parameters()
    print(f"BASE_SOBOL_CASES={N_CASES}")
    print(f"FAMILY_POINT_BOUND_EVALUATIONS={N_CASES * len(FAMILIES)}")
    print("GEOMETRY_FEATURE_BUILD=BEGIN", flush=True)
    geom = coarse_geometry(pset)
    print("GEOMETRY_FEATURE_BUILD=PASS", flush=True)

    min_curv = float(np.min(geom["curvature_norm"]))
    print(f"CURVATURE_NORM_MIN={min_curv:.15e}")
    print(f"CURVATURE_NORM_MAX={float(np.max(geom['curvature_norm'])):.15e}")
    print(f"CURVATURE_CONCENTRATION_MAX={float(np.max(geom['curvature_concentration'])):.15e}")
    print(f"MIN_PAYLOAD_DISTANCE_MIN={float(np.min(geom['min_payload_distance'])):.15e}")

    if min_curv < 0.97:
        raise RuntimeError("Fenchel numerical diagnostic failed unexpectedly.")

    point_results: dict[str, dict[str, np.ndarray]] = {}
    medium_candidates: list[dict[str, Any]] = []
    winding_point_rows = []

    print("\n=== D — POINT-EXTREMA UPPER-BOUND FAMILY RESULTS ===", flush=True)

    for family in FAMILIES:
        result = family_arrays(family, pset, geom)
        point_results[family] = result

        C = result["C_point"]
        positive = int(np.count_nonzero(np.isfinite(C)))
        beat006d = int(np.count_nonzero(C < C006D))
        beat024d = int(np.count_nonzero(C < C024D_SCALAR))

        best_idx = int(np.argmin(C)) if positive else -1
        best_c = float(C[best_idx]) if positive else math.inf

        print(f"{family}_POINT_BOUND_POSITIVE_CASES={positive}")
        print(f"{family}_POINT_BOUND_BEATS_006D_CASES={beat006d}")
        print(f"{family}_POINT_BOUND_BEATS_024D_SCALAR_CASES={beat024d}")
        print(f"{family}_BEST_POINT_BOUND_C={best_c:.15e}")

        if positive:
            print(
                f"{family}_BEST_POINT_BOUND_WINDING="
                f"{int(pset['p'][best_idx])},{int(pset['q_winding'][best_idx])}"
            )

        for wi, winding in enumerate(WINDINGS):
            mask = pset["winding_index"] == wi
            local = C[mask]
            local_positive = int(np.count_nonzero(np.isfinite(local)))
            local_best = float(np.min(local)) if local_positive else math.inf

            winding_point_rows.append({
                "stage": "POINT_BOUND",
                "family": family,
                "p": winding[0],
                "q": winding[1],
                "positive_cases": local_positive,
                "best_C": local_best,
                "beats_006D": bool(local_best < C006D),
                "beats_024D_scalar": bool(local_best < C024D_SCALAR),
            })

        medium_candidates.extend(
            choose_medium_candidates(family, pset, geom, result)
        )

    print(f"MEDIUM_CANDIDATE_COUNT={len(medium_candidates)}")

    print("\n=== E — 4096-PHASE OPTIMAL CONTIGUOUS WINDOWS ===", flush=True)
    medium_rows = medium_refinement(medium_candidates)

    for family in FAMILIES:
        rows = [
            r for r in medium_rows
            if r["family"] == family and math.isfinite(float(r["C"]))
        ]
        rows.sort(key=lambda r: float(r["C"]))

        print(f"{family}_MEDIUM_CONTIGUOUS_POSITIVE_CASES={len(rows)}")

        if rows:
            best = rows[0]
            print(f"{family}_BEST_MEDIUM_CONTIGUOUS_C={float(best['C']):.15e}")
            print(
                f"{family}_BEST_MEDIUM_CONTIGUOUS_WINDING="
                f"{best['p']},{best['q_winding']}"
            )
            print(f"{family}_BEST_MEDIUM_INTERACTION_DUTY={float(best['interaction_duty']):.15e}")
            print(f"{family}_BEST_MEDIUM_RESET_DUTY={float(best['reset_duty']):.15e}")

    high_candidates = choose_high_candidates(medium_rows)
    print(f"HIGH_CANDIDATE_COUNT={len(high_candidates)}")

    print("\n=== F — 16384-PHASE HIGH REFINEMENT ===", flush=True)
    high_rows = high_refinement(high_candidates)

    high_by_family: dict[str, list[dict[str, Any]]] = {}
    winding_high_rows = []

    for family in FAMILIES:
        rows = [
            r for r in high_rows
            if r["family"] == family and math.isfinite(float(r["C"]))
        ]
        rows.sort(key=lambda r: float(r["C"]))
        high_by_family[family] = rows

        print(f"{family}_HIGH_CONTIGUOUS_POSITIVE_CASES={len(rows)}")

        if rows:
            best = rows[0]
            print(f"{family}_BEST_HIGH_C={float(best['C']):.15e}")
            print(f"{family}_BEST_HIGH_A={float(best['A']):+.15e}")
            print(f"{family}_BEST_HIGH_WINDING={best['p']},{best['q_winding']}")
            print(f"{family}_BEST_HIGH_MAJOR_R={float(best['major']):.15e}")
            print(f"{family}_BEST_HIGH_MINOR_R={float(best['minor']):.15e}")
            print(f"{family}_BEST_HIGH_GAP={float(best['gap']):.15e}")
            print(f"{family}_BEST_HIGH_BETA_ORBIT={float(best['beta_orbit']):.15e}")
            print(f"{family}_BEST_HIGH_SPIN_FRACTION={float(best['spin_fraction']):.15e}")
            print(f"{family}_BEST_HIGH_BETA_SPIN={float(best['beta_spin']):.15e}")
            print(f"{family}_BEST_HIGH_Q_SCALAR={float(best['q_scalar']):.15e}")
            print(f"{family}_BEST_HIGH_F={float(best['f']):.15e}")
            print(f"{family}_BEST_HIGH_INTERACTION_DUTY={float(best['interaction_duty']):.15e}")
            print(f"{family}_BEST_HIGH_RESET_DUTY={float(best['reset_duty']):.15e}")
            print(f"{family}_BEST_HIGH_K_INTERACTION={float(best['interaction_kernel']):.15e}")
            print(f"{family}_BEST_HIGH_K_RESET={float(best['reset_kernel']):.15e}")
            print(f"{family}_BEST_HIGH_CURVATURE_NORM={float(best['orbit']['curvature_norm']):.15e}")
            print(f"{family}_BEST_HIGH_MEDIUM_RELERR={float(best['medium_high_relerr']):.15e}")
            print(
                f"{family}_BEST_HIGH_BEATS_006D="
                + ("YES" if float(best["C"]) < C006D else "NO")
            )
            print(
                f"{family}_BEST_HIGH_BEATS_024D_SCALAR="
                + ("YES" if float(best["C"]) < C024D_SCALAR else "NO")
            )

        for winding in WINDINGS:
            local = [
                r for r in rows
                if int(r["p"]) == winding[0]
                and int(r["q_winding"]) == winding[1]
            ]
            best_c = float(local[0]["C"]) if local else math.inf
            winding_high_rows.append({
                "stage": "HIGH_CONTIGUOUS",
                "family": family,
                "p": winding[0],
                "q": winding[1],
                "positive_cases": len(local),
                "best_C": best_c,
                "beats_006D": bool(best_c < C006D),
                "beats_024D_scalar": bool(best_c < C024D_SCALAR),
            })

    # Best physically interesting source among non-ideal families.
    nonideal_high = [
        r
        for family, rows in high_by_family.items()
        if family != "IDEAL_KERNEL_ADAPTIVE_DEC_FLOOR"
        for r in rows
    ]
    nonideal_high.sort(key=lambda r: float(r["C"]))

    ideal_rows = high_by_family["IDEAL_KERNEL_ADAPTIVE_DEC_FLOOR"]
    ideal_best = ideal_rows[0] if ideal_rows else None
    best_nonideal = nonideal_high[0] if nonideal_high else None

    print("\n=== G — BATHTUB RELAXED BOUNDS / LOCALIZATION PENALTY ===", flush=True)
    relaxed_by_family = {}

    for family, rows in high_by_family.items():
        if not rows:
            relaxed_by_family[family] = None
            continue

        contiguous = rows[0]
        relaxed = bathtub_for_best(contiguous)
        relaxed_by_family[family] = relaxed

        print(f"{family}_BEST_RELAXED_BATHTUB_C={float(relaxed['C']):.15e}")

        if math.isfinite(float(relaxed["C"])):
            penalty = float(contiguous["C"]) / float(relaxed["C"])
        else:
            penalty = math.inf

        print(f"{family}_LOCALIZATION_PENALTY={penalty:.15e}")

    print("\n=== H — 65536-PHASE INDEPENDENT FINAL RECONSTRUCTION ===", flush=True)

    if best_nonideal is not None:
        independent = independent_reconstruction(best_nonideal)
        print(f"INDEPENDENT_FAMILY={best_nonideal['family']}")
        print(f"INDEPENDENT_HIGH_C_REFERENCE={float(best_nonideal['C']):.15e}")
        print(f"INDEPENDENT_65536_C={float(independent['C']):.15e}")
        print(f"INDEPENDENT_RELATIVE_DIFFERENCE={float(independent['relative_difference']):.15e}")
        print("INDEPENDENT_RECONSTRUCTION=" + ("PASS" if independent["pass"] else "FAIL"))
    elif ideal_best is not None:
        independent = independent_reconstruction(ideal_best)
        print("INDEPENDENT_FAMILY=IDEAL_ONLY")
        print(f"INDEPENDENT_HIGH_C_REFERENCE={float(ideal_best['C']):.15e}")
        print(f"INDEPENDENT_65536_C={float(independent['C']):.15e}")
        print(f"INDEPENDENT_RELATIVE_DIFFERENCE={float(independent['relative_difference']):.15e}")
        print("INDEPENDENT_RECONSTRUCTION=" + ("PASS" if independent["pass"] else "FAIL"))
    else:
        independent = None
        print("INDEPENDENT_RECONSTRUCTION=NOT_RUN_NO_HIGH_SURVIVOR")

    print("\n=== I — DIRECTIONAL BUNDLE AUDIT ===", flush=True)
    bundle_audits = {}

    directional_source = best_nonideal if best_nonideal is not None else ideal_best

    if directional_source is not None:
        for count in BUNDLE_COUNTS:
            audit = vector_bundle_audit(directional_source, count)
            bundle_audits[str(count)] = audit
            if audit.get("valid"):
                print(
                    f"BUNDLE_N={count} "
                    f"ALL_OUTWARD={'YES' if audit['all_axial_outward'] else 'NO'} "
                    f"FLATNESS={float(audit['axial_flatness']):.15e} "
                    f"TRANSVERSE={float(audit['maximum_transverse_fraction']):.15e} "
                    f"ONAXIS_RELERR={float(audit['on_axis_relative_error']):.15e}"
                )
            else:
                print(f"BUNDLE_N={count} VALID=NO")
    else:
        print("BUNDLE_AUDIT=NOT_RUN_NO_SURVIVOR")

    print("\n=== J — FIXED-GEOMETRY SPIN AUDIT ===", flush=True)

    scalar_floor_rows = high_by_family["SCALAR_DEC_FLOOR_NO_SPIN"]

    if scalar_floor_rows:
        spin_rows, spin_summary = spin_audit(scalar_floor_rows[0])

        for mode in ("UNRESTRICTED", "KINETIC_LIMITED"):
            best = spin_summary.get(mode)
            if best is None:
                print(f"SPIN_AUDIT_{mode}_POSITIVE_CASES=0")
            else:
                print(f"SPIN_AUDIT_{mode}_BEST_C={float(best['C']):.15e}")
                print(f"SPIN_AUDIT_{mode}_BEST_BETA_ORBIT={float(best['beta_orbit']):.15e}")
                print(f"SPIN_AUDIT_{mode}_BEST_SPIN_FRACTION={float(best['spin_fraction']):.15e}")
                print(f"SPIN_AUDIT_{mode}_BEST_BETA_SPIN={float(best['beta_spin']):.15e}")
    else:
        spin_rows = []
        spin_summary = {"UNRESTRICTED": None, "KINETIC_LIMITED": None}
        print("SPIN_AUDIT=NOT_RUN_NO_SCALAR_DEC_FLOOR_SURVIVOR")

    print("\n=== K — BLIND WILDCARD DIAGNOSTICS ===")
    for value in BLIND_WILDCARDS:
        print(
            f"WILDCARD_MAJOR_RADIUS_OVER_H={value:.6f} "
            "ROLE=BLIND_WILDCARD_NOT_PHYSICS_PRIOR"
        )
    print("WILDCARDS_USED_FOR_SELECTION=NO")

    print("\n=== L — DECISION ===")

    ideal_positive = bool(ideal_best is not None and float(ideal_best["A"]) > 0.0)
    ideal_beats_006d = bool(ideal_best is not None and float(ideal_best["C"]) < C006D)

    scalar_floor_best = (
        high_by_family["SCALAR_DEC_FLOOR_NO_SPIN"][0]
        if high_by_family["SCALAR_DEC_FLOOR_NO_SPIN"]
        else None
    )
    curvature_scalar_best = (
        high_by_family["SCALAR_CURVATURE_PROXY_NO_SPIN"][0]
        if high_by_family["SCALAR_CURVATURE_PROXY_NO_SPIN"]
        else None
    )
    kinetic_no_spin_best = (
        high_by_family["KINETIC_DEC_FLOOR_NO_SPIN"][0]
        if high_by_family["KINETIC_DEC_FLOOR_NO_SPIN"]
        else None
    )
    kinetic_spin_best = (
        high_by_family["KINETIC_DEC_FLOOR_WITH_SPIN"][0]
        if high_by_family["KINETIC_DEC_FLOOR_WITH_SPIN"]
        else None
    )

    scalar_floor_beats_006d = bool(
        scalar_floor_best is not None and float(scalar_floor_best["C"]) < C006D
    )
    scalar_floor_beats_024d = bool(
        scalar_floor_best is not None and float(scalar_floor_best["C"]) < C024D_SCALAR
    )
    curvature_proxy_beats_006d = bool(
        curvature_scalar_best is not None and float(curvature_scalar_best["C"]) < C006D
    )
    kinetic_no_spin_beats_006d = bool(
        kinetic_no_spin_best is not None and float(kinetic_no_spin_best["C"]) < C006D
    )
    kinetic_spin_beats_006d = bool(
        kinetic_spin_best is not None and float(kinetic_spin_best["C"]) < C006D
    )

    if kinetic_no_spin_best is not None and kinetic_spin_best is not None:
        spin_improvement = float(kinetic_no_spin_best["C"]) / float(kinetic_spin_best["C"])
    else:
        spin_improvement = 0.0

    genuine_spin = bool(
        kinetic_spin_best is not None
        and kinetic_spin_beats_006d
        and float(kinetic_spin_best["spin_fraction"]) >= 0.10
        and float(kinetic_spin_best["beta_spin"]) >= 0.25
        and spin_improvement >= 1.05
    )

    convergence_pass = bool(
        best_nonideal is not None
        and float(best_nonideal.get("medium_high_relerr", math.inf)) <= CONVERGENCE_TOL
    )
    independent_pass = bool(independent is not None and independent.get("pass", False))

    if not ideal_positive:
        decision = "RED_KERNEL_ADAPTIVE_INTERNAL_ORBIT_IDEAL_CONTIGUOUS_CEILING_FAILS"
        next_action = "CLOSE_INTERNAL_ORBIT_BRANCH_AND_RETURN_TO_MINIMAL_SCALAR_CONVERTER_OR_ANALOGUE_ANTIGRAVITY"
        interpretation = "NO_CONTIGUOUS_ORBITAL_KERNEL_LEVERAGE_EVEN_AFTER_PHASE_REPAIR"
    elif ideal_positive and not ideal_beats_006d:
        decision = "RED_ORBITAL_KERNEL_RECTIFICATION_EXISTS_BUT_IDEAL_CEILING_DOES_NOT_BEAT_006D"
        next_action = "CLOSE_INTERNAL_ORBIT_EFFICIENCY_BRANCH_AND_RETURN_TO_MINIMAL_SCALAR_CONVERTER"
        interpretation = "SIGN_RECOVERED_BUT_SOURCE_EFFICIENCY_TOO_WEAK"
    elif genuine_spin and convergence_pass and independent_pass:
        decision = "YELLOW_GENUINE_ORBIT_PLUS_SPIN_KINETIC_SURVIVOR"
        next_action = "024D2_MINIMAL_MICROSCOPIC_POLoidal_ORBIT_PLUS_SPIN_FIELD_PREFLIGHT"
        interpretation = "ORBITAL_KERNEL_TRANSPORT_AND_SPIN_BOTH_SURVIVE_EFFECTIVE_LEDGER"
    elif kinetic_no_spin_beats_006d and convergence_pass and independent_pass:
        decision = "YELLOW_KINETIC_LIMITED_KERNEL_ADAPTIVE_ORBIT_SURVIVOR_SPIN_NOT_REQUIRED"
        next_action = "024D2_MINIMAL_MICROSCOPIC_POLoidal_TRANSPORT_AND_SCALAR_CONVERSION_PREFLIGHT"
        interpretation = "ORBITAL_KERNEL_TRANSPORT_SURVIVES_WITH_KINEMATIC_ENERGY_LIMIT"
    elif scalar_floor_beats_006d and convergence_pass and independent_pass:
        decision = "YELLOW_KERNEL_ADAPTIVE_SCALAR_ORBIT_HEADROOM_KINETIC_DRIVER_NOT_PROMOTED"
        next_action = "024D2_MINIMAL_CANONICAL_SCALAR_POLoidal_TRANSPORT_FIELD_PREFLIGHT"
        interpretation = "STRESS_CONVERSION_PLUS_KERNEL_PLACEMENT_SURVIVES_SPIN_KINETICS_DO_NOT"
    elif ideal_beats_006d:
        decision = "YELLOW_IDEAL_ORBITAL_HEADROOM_ONLY_PHYSICAL_LEDGER_NOT_SURVIVED"
        next_action = "RETURN_TO_MINIMAL_SCALAR_CONVERTER_UNLESS_NEW_SUPPORT_PHYSICS_JUSTIFIES_ORBITAL_LEDGER"
        interpretation = "RELAXED_ORBITAL_PLACEMENT_HEADROOM_EXISTS_WITHOUT_CONSTRAINED_PROMOTION"
    else:
        decision = "RED_KERNEL_ADAPTIVE_INTERNAL_ORBIT_NO_PROMOTABLE_ADVANCE"
        next_action = "RETURN_TO_MINIMAL_SCALAR_CONVERTER_OR_ANALOGUE_ANTIGRAVITY"
        interpretation = "NO_NEW_PROMOTABLE_ORBITAL_OR_SPIN_LEVERAGE"

    print("024D1_GEOMETRIC_TOP_BOTTOM_INTERPRETATION=SUPERSEDED_BY_KERNEL_ADAPTIVE_REPAIR")
    print("PURE_TOROIDAL_ORBIT=RED_EXACT_CONSTANT_KERNEL")
    print("KERNEL_ADAPTIVE_IDEAL_POSITIVE=" + ("YES" if ideal_positive else "NO"))
    print("KERNEL_ADAPTIVE_IDEAL_BEATS_006D=" + ("YES" if ideal_beats_006d else "NO"))
    print("SCALAR_DEC_FLOOR_BEATS_006D=" + ("YES" if scalar_floor_beats_006d else "NO"))
    print("SCALAR_DEC_FLOOR_BEATS_024D_SCALAR=" + ("YES" if scalar_floor_beats_024d else "NO"))
    print("CURVATURE_PROXY_SCALAR_BEATS_006D=" + ("YES" if curvature_proxy_beats_006d else "NO"))
    print("KINETIC_LIMITED_NO_SPIN_BEATS_006D=" + ("YES" if kinetic_no_spin_beats_006d else "NO"))
    print("KINETIC_LIMITED_WITH_SPIN_BEATS_006D=" + ("YES" if kinetic_spin_beats_006d else "NO"))
    print(f"SPIN_CONSTRAINED_IMPROVEMENT_FACTOR={spin_improvement:.15e}")
    print("GENUINE_SPIN_PROMOTION=" + ("YES" if genuine_spin else "NO"))
    print("BEST_NONIDEAL_CONVERGENCE=" + ("PASS" if convergence_pass else "FAIL"))
    print("BEST_NONIDEAL_INDEPENDENT=" + ("PASS" if independent_pass else "FAIL"))
    print(f"024D1R_INTERPRETATION={interpretation}")
    print(f"024D1R_DECISION={decision}")
    print(f"NEXT={next_action}")
    print("MICROSCOPIC_FIELD_REALIZATION=NO")
    print("DYNAMIC_LOCAL_TMUNU_CONSERVATION=NOT_ESTABLISHED")
    print("FULL_STABILITY=NO")
    print("NONLINEAR_GR=NO")
    print("REMOVES_1_OVER_G_SCALING=NO")
    print("CURRENT_KNOWLEDGE_HEURISTIC=70_TO_71_PERCENT_RETAIN_UNLESS_LATER_MICROSCOPIC_PROMOTION_IS_EARNED")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")

    # ------------------------------------------------------------
    # Persist compact artifacts.
    # ------------------------------------------------------------

    csv_rows = [public_row(r) for r in medium_rows] + [public_row(r) for r in high_rows]
    if csv_rows:
        fields = sorted({key for row in csv_rows for key in row})
        with OUT_TOP.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(csv_rows)

    all_winding_rows = winding_point_rows + winding_high_rows
    with OUT_WINDING.open("w", encoding="utf-8", newline="") as handle:
        fields = [
            "stage",
            "family",
            "p",
            "q",
            "positive_cases",
            "best_C",
            "beats_006D",
            "beats_024D_scalar",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_winding_rows)

    if spin_rows:
        fields = sorted({key for row in spin_rows for key in row})
        with OUT_SPIN.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(spin_rows)

    profile_payload = {}
    if directional_source is not None and math.isfinite(float(directional_source["C"])):
        orbit = directional_source["orbit"]
        for key in ("u", "x", "y", "z", "weights", "kernel"):
            profile_payload[key] = np.asarray(orbit[key])
        profile_payload["top_profile"] = np.asarray(directional_source["top_profile"])
        profile_payload["reset_profile"] = np.asarray(directional_source["reset_profile"])

    if profile_payload:
        np.savez_compressed(OUT_NPZ, **profile_payload)

    summary = {
        "claim_classification": "PROJECT_DERIVED_KERNEL_ADAPTIVE_INTERNAL_ORBIT_REPAIR_PREFILTER",
        "anchors": {
            "C_006D": C006D,
            "C_024D_scalar": C024D_SCALAR,
            "payload_radius_over_h": PAYLOAD_RADIUS_OVER_H,
        },
        "repairs": {
            "geometric_top_bottom_replaced_by_kernel_adaptive_windows": True,
            "fenchel_bound_used_as_geometry_diagnostic_not_energy_theorem": True,
            "DEC_floor_and_curvature_proxy_separated": True,
            "pure_toroidal_constant_kernel_no_go": True,
        },
        "repair_witness": witness,
        "scan": {
            "sobol_cases": N_CASES,
            "families": list(FAMILIES),
            "point_bound_family_evaluations": N_CASES * len(FAMILIES),
            "coarse_phase_points": COARSE_NPHASE,
            "medium_phase_points": MEDIUM_NPHASE,
            "high_phase_points": HIGH_NPHASE,
            "independent_phase_points": INDEPENDENT_NPHASE,
            "windings": [list(w) for w in WINDINGS],
        },
        "best_high": {
            family: (public_row(rows[0]) if rows else None)
            for family, rows in high_by_family.items()
        },
        "relaxed_bathtub": {
            family: (public_row(row) if row is not None else None)
            for family, row in relaxed_by_family.items()
        },
        "independent": (public_row(independent) if independent is not None else None),
        "bundle_audits": bundle_audits,
        "spin_audit": spin_summary,
        "decision": {
            "ideal_positive": ideal_positive,
            "ideal_beats_006D": ideal_beats_006d,
            "scalar_DEC_floor_beats_006D": scalar_floor_beats_006d,
            "scalar_DEC_floor_beats_024D_scalar": scalar_floor_beats_024d,
            "curvature_proxy_scalar_beats_006D": curvature_proxy_beats_006d,
            "kinetic_no_spin_beats_006D": kinetic_no_spin_beats_006d,
            "kinetic_spin_beats_006D": kinetic_spin_beats_006d,
            "genuine_spin_promotion": genuine_spin,
            "convergence_pass": convergence_pass,
            "independent_pass": independent_pass,
            "interpretation": interpretation,
            "024D1R": decision,
            "next": next_action,
            "practical_antigravity_device": False,
        },
        "claim_limits": [
            "NO_MICROSCOPIC_FIELD_SOLUTION",
            "NO_DYNAMIC_LOCAL_TMUNU_CONSERVATION_PROOF",
            "NO_FULL_STABILITY",
            "NO_NONLINEAR_GR",
            "NO_1_OVER_G_SCALING_ESCAPE",
            "NO_EXPERIMENT",
            "NO_REACTIONLESS_PROPULSION",
            "NO_PRACTICAL_DEVICE",
        ],
    }

    OUT_SUMMARY.write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=True) + "\n",
        encoding="utf-8",
    )

    print(f"SUMMARY_JSON={OUT_SUMMARY.relative_to(ROOT)}")
    print(f"TOP_CSV={OUT_TOP.relative_to(ROOT)}")
    print(f"WINDING_CSV={OUT_WINDING.relative_to(ROOT)}")
    if OUT_SPIN.is_file():
        print(f"SPIN_CSV={OUT_SPIN.relative_to(ROOT)}")
    if OUT_NPZ.is_file():
        print(f"BEST_PROFILES_NPZ={OUT_NPZ.relative_to(ROOT)}")
    print("024D1R_RUN_COMPLETE=YES")


if __name__ == "__main__":
    main()
