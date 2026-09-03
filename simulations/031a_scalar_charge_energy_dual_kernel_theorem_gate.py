"""
031A — Scalar-charge energy / dual-kernel / morphology theorem gate
===================================================================

Purpose
-------
Cheaply derive and independently reconstruct the exact weak-field normalization
for Activated Scalar-Metric Charge Antigravity before any large microscopic PDE.

The run asks whether a canonical positive-energy scalar can mediate true
one-sided finite-payload repulsion at an absolute energy scale below the pure-GR
1/G stress-engineering burden, and—equally important—what scalar charge per
source joule is then required.

This file is a theorem/oracle gate. It does NOT construct an activated source,
B7 dressing, Q-ball, gate field, or practical device.

Declared action convention
--------------------------
In natural units, use the Einstein-frame scaffold

    S = ∫ d^4x sqrt(-g) [ Mbar_Pl^2 R/2
                          - (∂phi)^2/2
                          - m_phi^2 phi^2/2
                          + L_X(X,phi) + L_chi(chi,phi) ]
        + S_SM[A(phi,chi)^2 g_{mu nu}, Psi_SM]

with one physical Jordan metric for ordinary matter,

    g_tilde_{mu nu} = A(phi,chi)^2 g_{mu nu}.

At a fixed operating background define

    alpha_m = Mbar_Pl ∂ ln A / ∂phi

and for a solved source

    alpha_X = Mbar_Pl ∂ ln E_X / ∂phi_infinity.

The project derivative charge is

    Q_phi = -∂E_X/∂phi_infinity.

For weak-field SI calculations define the signed mass-equivalent scalar charge

    q_X = alpha_X M_X,

and a scalar potential-like field psi [kg/m] obeying

    (∇^2 - mu^2) psi = -4 pi rho_q,
    mu = 1/lambda_phi.

Ordinary matter experiences the scalar contribution

    Phi_phi = -2 G alpha_m psi,
    a_phi   = +2 G alpha_m ∇psi.

Therefore alpha_m*q_X < 0 gives repulsion.  For two compact bodies the scalar
piece is the usual Yukawa interaction proportional to 2 alpha_A alpha_B.

Canonical scalar-field energy
-----------------------------

    E_phi = G/(4 pi) ∫ [ |∇psi|^2 + mu^2 psi^2 ] d^3x
          = G ∫ rho_q psi d^3x

for a solved static field vanishing at infinity.  This sector is manifestly
positive.  No negative interaction-energy credit is used in this oracle gate.

Finite spherical payload
------------------------
For a uniform spherical payload of radius R_P in a source-free Helmholtz region,
its center-of-mass response differs from the center gradient by

    F_P(x) = 3 i_1(x)/x,
    x = mu R_P,

where i_1 is the modified spherical Bessel function.

Theorem 1 — payload-centered source-free cavity
-----------------------------------------------
If all source support lies outside a ball B_d centered on the payload, d>R_P,
the least scalar-field energy INSIDE that empty ball for a fixed payload CM
acceleration is the regular l=1 Helmholtz mode:

    E_cavity >=
        a_CM^2 d^3 / [4 G alpha_m^2 F_P(mu R_P)^2]
        * 3 i_1(mu d) i_1'(mu d)/(mu d).

Massless limit:

    E_cavity >= a_CM^2 d^3/(12 G alpha_m^2).

This is morphology independent but permits boundary data on all sides of the
payload, so it is too optimistic for conservative true stand-off.

Theorem 2 — conservative one-sided half-space
---------------------------------------------
Now require ALL source support to lie behind a plane z<=-d, with payload center
at z=0.  Fourier decomposition in the source-free half-space gives the sharper
exact bound

    E_half >=
        a_CM^2 d^3 / [2 G alpha_m^2 F_P(mu R_P)^2]
        * exp(2 mu d)/(2(mu d)^2 + 2 mu d + 1).

Massless limit:

    E_half >= a_CM^2 d^3/(2 G alpha_m^2)

which is exactly six times the spherical-cavity floor.

Theorem 3 — absolute source-charge lower bound
----------------------------------------------
For source support at least distance d from the payload center,

    Q_abs = ∫ |rho_q| d^3x

must satisfy

    Q_abs >=
        a_CM d^2 exp(mu d)
        / [2 G |alpha_m| F_P(mu R_P)(1+mu d)].

Massless limit:

    Q_abs >= a_CM d^2/(2 G |alpha_m|).

If positive source/core energy E_X has bounded sensitivity

    Q_abs <= |alpha_X| E_X/c^2,

then, for total energy target E_target and no omitted positive costs,

    |alpha_X| >= Q_abs c^2/(E_target-E_half).

Even before paying scalar field energy,

    |alpha_m alpha_X|
    >= a_CM d^2 c^2/(2 G E_target)

in the massless optimistic limit.  This is the exact charge-per-joule burden
that 031 is trying to realize rather than hide inside a guessed G_eff.

GR ledger warning
-----------------
Do NOT turn E_phi/c^2 into a dust attraction.  A static canonical scalar has
nontrivial pressure; its gradient contribution cancels from rho+sum_i p_i.
The microscopic X/chi/support stress tensor and scalar potential contribution
must be included later from the actual action.  This theorem run ignores those
extra costs, making all energy conclusions optimistic lower bounds.

Validation
----------
The run independently checks:

- cavity closed form vs direct l=1 energy quadrature;
- half-space closed form vs independent Fourier-k quadrature;
- finite-payload form factor vs direct volume averaging;
- uniform-sphere Yukawa far field and self-energy vs radial Green integration;
- ideal thin-shell self-energy vs direct field-energy integration;
- a finite-thickness shell field-energy integral vs source identity.

Promotion boundary
------------------
GREEN means only that 031 survives the theorem/normalization gate and authorizes
one-sided morphology optimization using BOTH field energy and absolute charge.
It does not authorize a microscopic PDE or a practical claim.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import csv
import json
import math

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import minimize_scalar
from scipy.special import spherical_in


# -----------------------------------------------------------------------------
# Constants and declared benchmarks
# -----------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DATA = ROOT / "results" / "data"
RESULTS_DATA.mkdir(parents=True, exist_ok=True)

G = 6.67430e-11
C_LIGHT = 299_792_458.0
G0 = 9.80665
REDUCED_PLANCK_GEV = 2.435e18

PRIMARY_ACCEL = G0
PRIMARY_PAYLOAD_RADIUS = 0.10
PRIMARY_CLEARANCE = 1.00
PRIMARY_D = PRIMARY_PAYLOAD_RADIUS + PRIMARY_CLEARANCE
PRIMARY_TARGET_J = 1.0e12
STRONG_TARGET_J = 1.0e11

# Secondary buildplan benchmark, made explicitly finite-payload.
SECONDARY_ACCEL = 0.1 * G0
SECONDARY_PAYLOAD_RADIUS = 0.001
SECONDARY_CLEARANCE = 0.010
SECONDARY_D = SECONDARY_PAYLOAD_RADIUS + SECONDARY_CLEARANCE
SECONDARY_TARGET_J = 1.0e15

# Long-range Brans-Dicke reference only.  Living Reviews (2024) quotes
# omega_BD > 1.4e5 from J0337+1715.  With THIS project's force convention
# F/F_GR = 1+2 alpha_m^2, alpha_m^2 = 1/(4 omega_BD+6).
OMEGA_BD_LONG_RANGE_REFERENCE = 1.4e5
ALPHA_M_BD_LONG_RANGE_REFERENCE = math.sqrt(
    1.0 / (4.0 * OMEGA_BD_LONG_RANGE_REFERENCE + 6.0)
)

RELERR_TOL_STRICT = 3.0e-5
RELERR_TOL_RADIAL = 4.0e-3


@dataclass
class Check:
    name: str
    a: float
    b: float
    relerr: float
    passed: bool


def relerr(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0e-300)


# -----------------------------------------------------------------------------
# Modified-spherical-Bessel helpers and finite-payload factor
# -----------------------------------------------------------------------------

def i1(x: float) -> float:
    if abs(x) < 1.0e-4:
        return x / 3.0 + x**3 / 30.0 + x**5 / 840.0 + x**7 / 45360.0
    return float(spherical_in(1, x))


def i1p(x: float) -> float:
    if abs(x) < 1.0e-4:
        return 1.0 / 3.0 + x**2 / 10.0 + x**4 / 168.0 + x**6 / 6480.0
    return float(spherical_in(1, x, derivative=True))


def payload_factor(mu: float, radius: float) -> float:
    x = mu * radius
    if abs(x) < 1.0e-12:
        return 1.0
    return 3.0 * i1(x) / x


# -----------------------------------------------------------------------------
# The three analytical lower bounds
# -----------------------------------------------------------------------------

def cavity_energy(a: float, d: float, rp: float, alpha_m: float, lam: float) -> float:
    if math.isinf(lam):
        return a**2 * d**3 / (12.0 * G * alpha_m**2)
    mu = 1.0 / lam
    xd = mu * d
    fp = payload_factor(mu, rp)
    return (
        a**2
        * d**3
        / (4.0 * G * alpha_m**2 * fp**2)
        * (3.0 * i1(xd) * i1p(xd) / xd)
    )


def halfspace_energy(a: float, d: float, rp: float, alpha_m: float, lam: float) -> float:
    if math.isinf(lam):
        return a**2 * d**3 / (2.0 * G * alpha_m**2)
    mu = 1.0 / lam
    xd = mu * d
    fp = payload_factor(mu, rp)
    penalty = math.exp(2.0 * xd) / (2.0 * xd**2 + 2.0 * xd + 1.0)
    return a**2 * d**3 / (2.0 * G * alpha_m**2 * fp**2) * penalty


def qabs_lower(a: float, d: float, rp: float, alpha_m: float, lam: float) -> float:
    if math.isinf(lam):
        return a * d**2 / (2.0 * G * abs(alpha_m))
    mu = 1.0 / lam
    xd = mu * d
    fp = payload_factor(mu, rp)
    return (
        a
        * d**2
        * math.exp(xd)
        / (2.0 * G * abs(alpha_m) * fp * (1.0 + xd))
    )


def dual_source_bound(
    a: float,
    d: float,
    rp: float,
    alpha_m: float,
    lam: float,
    target_j: float,
) -> dict[str, float] | None:
    ephi = halfspace_energy(a, d, rp, alpha_m, lam)
    if ephi >= target_j:
        return None
    qabs = qabs_lower(a, d, rp, alpha_m, lam)
    ex_budget = target_j - ephi
    alpha_x = qabs * C_LIGHT**2 / ex_budget
    return {
        "field_energy_floor_j": ephi,
        "source_energy_budget_max_j": ex_budget,
        "qabs_floor_kg": qabs,
        "abs_alpha_x_floor": alpha_x,
        "alpha_product_floor_with_field": abs(alpha_m) * alpha_x,
        "fx_scale_gev_max": REDUCED_PLANCK_GEV / alpha_x,
        "qabs_per_source_joule_floor_kg_per_j": qabs / ex_budget,
    }


def coupling_product_floor(a: float, d: float, target_j: float) -> float:
    return a * d**2 * C_LIGHT**2 / (2.0 * G * target_j)


# -----------------------------------------------------------------------------
# Independent theorem reconstructions
# -----------------------------------------------------------------------------

def cavity_direct(a: float, d: float, rp: float, alpha_m: float, lam: float) -> float:
    if math.isinf(lam):
        gpsi = a / (2.0 * G * abs(alpha_m))
        return G * gpsi**2 * d**3 / 3.0

    mu = 1.0 / lam
    fp = payload_factor(mu, rp)
    g0 = a / (2.0 * G * abs(alpha_m) * fp)
    amp = 3.0 * g0 / mu

    nodes, weights = np.polynomial.legendre.leggauss(800)
    r = 0.5 * d * (nodes + 1.0)
    w = 0.5 * d * weights
    x = mu * r
    iv = np.array([i1(float(v)) for v in x])
    ip = np.array([i1p(float(v)) for v in x])

    # Direct volume energy after analytical angular integration.
    radial = (4.0 * math.pi / 3.0) * amp**2 * mu**2 * ip**2 * r**2
    angular = (8.0 * math.pi / 3.0) * amp**2 * iv**2
    mass = (4.0 * math.pi / 3.0) * amp**2 * mu**2 * iv**2 * r**2
    integral = float(np.sum(w * (radial + angular + mass)))
    return G * integral / (4.0 * math.pi)


def halfspace_direct_k(a: float, d: float, rp: float, alpha_m: float, lam: float) -> float:
    mu = 0.0 if math.isinf(lam) else 1.0 / lam
    fp = payload_factor(mu, rp)
    g0 = a / (2.0 * G * abs(alpha_m) * fp)

    kmax = 40.0 / d + 8.0 * mu
    k = np.linspace(0.0, kmax, 160_000)
    kap = np.sqrt(k**2 + mu**2)
    # I = ∫ d^2k/(2pi)^2 kappa exp(-2 kappa d)
    I = float(np.trapezoid(k * kap * np.exp(-2.0 * kap * d) / (2.0 * math.pi), k))
    norm_min = g0**2 / I
    return G * norm_min / (4.0 * math.pi)


def payload_average_direct(mu: float, rp: float) -> float:
    if mu == 0.0:
        return 1.0
    g0 = 1.0
    amp = 3.0 * g0 / mu
    rn, rw = np.polynomial.legendre.leggauss(120)
    un, uw = np.polynomial.legendre.leggauss(120)
    r = 0.5 * rp * (rn + 1.0)
    rw = 0.5 * rp * rw
    volume = 4.0 * math.pi * rp**3 / 3.0
    total = 0.0
    for rr, wr in zip(r, rw, strict=True):
        x = mu * float(rr)
        radial_coeff = amp * mu * i1p(x)
        tangential = amp * i1(x) / float(rr)
        dz = radial_coeff * un**2 + tangential * (1.0 - un**2)
        total += float(wr) * float(rr) ** 2 * 2.0 * math.pi * float(np.sum(uw * dz))
    return total / volume


# -----------------------------------------------------------------------------
# Finite spherical-source reconstructions
# -----------------------------------------------------------------------------

def sphere_form(x: float) -> float:
    if abs(x) < 1.0e-3:
        return 1.0 + x**2 / 10.0 + x**4 / 280.0 + x**6 / 15120.0
    return 3.0 * (x * math.cosh(x) - math.sinh(x)) / x**3


def sphere_self_factor(x: float) -> float:
    if abs(x) < 0.08:
        return 6.0 / 5.0 - x + 18.0 * x**2 / 35.0 - x**3 / 5.0 + 4.0 * x**4 / 63.0
    return (
        3.0 / x**2
        - 9.0 * (1.0 + x) * math.exp(-x)
        * (x * math.cosh(x) - math.sinh(x)) / x**5
    )


def shell_self_factor(x: float) -> float:
    if abs(x) < 0.08:
        return 1.0 - x + 2.0 * x**2 / 3.0 - x**3 / 3.0 + 2.0 * x**4 / 15.0
    return math.exp(-x) * math.sinh(x) / x


def reverse_cumtrap(values: np.ndarray, r: np.ndarray) -> np.ndarray:
    return -cumulative_trapezoid(values[::-1], r[::-1], initial=0.0)[::-1]


def radial_green(r: np.ndarray, rho: np.ndarray, mu: float) -> np.ndarray:
    if mu == 0.0:
        inner = cumulative_trapezoid(4.0 * math.pi * r**2 * rho, r, initial=0.0)
        outer = reverse_cumtrap(4.0 * math.pi * r * rho, r)
        psi = np.empty_like(r)
        psi[0] = outer[0]
        psi[1:] = inner[1:] / r[1:] + outer[1:]
        return psi

    inner = cumulative_trapezoid(r * rho * np.sinh(mu * r), r, initial=0.0)
    outer = reverse_cumtrap(r * rho * np.exp(-mu * r), r)
    psi = np.empty_like(r)
    psi[0] = 4.0 * math.pi * outer[0]
    rr = r[1:]
    psi[1:] = 4.0 * math.pi * (
        np.exp(-mu * rr) * inner[1:] / (mu * rr)
        + np.sinh(mu * rr) * outer[1:] / (mu * rr)
    )
    return psi


def radial_ledger(r: np.ndarray, rho: np.ndarray, psi: np.ndarray, mu: float) -> tuple[float, float, float]:
    dpsi = np.gradient(psi, r, edge_order=2)
    e_field = G * float(np.trapezoid(r**2 * (dpsi**2 + mu**2 * psi**2), r))
    rmax = float(r[-1])
    e_field += G * rmax**2 * (mu + 1.0 / rmax) * float(psi[-1]) ** 2
    e_source = G * float(np.trapezoid(4.0 * math.pi * r**2 * rho * psi, r))
    qfar = float(psi[-1] * rmax * math.exp(mu * rmax))
    return e_field, e_source, qfar


def normalize_rho(r: np.ndarray, rho: np.ndarray) -> np.ndarray:
    q = float(np.trapezoid(4.0 * math.pi * r**2 * rho, r))
    return rho / q


def validate_finite_sources() -> list[Check]:
    checks: list[Check] = []
    R = 1.0
    for x in (0.0, 1.0, 3.0):
        mu = x / R
        rmax = 40.0 if mu == 0.0 else max(12.0, 12.0 / mu)
        r = np.linspace(0.0, rmax, 24_001)

        # Uniform sphere.
        rho = normalize_rho(r, np.where(r <= R, 1.0, 0.0))
        psi = radial_green(r, rho, mu)
        ef, es, qfar = radial_ledger(r, rho, psi, mu)
        exact_e = G / R * sphere_self_factor(x)
        exact_q = sphere_form(x)
        for name, a, b in (
            (f"SPHERE_FIELD_VS_SOURCE_X{x:g}", ef, es),
            (f"SPHERE_SOURCE_VS_EXACT_X{x:g}", es, exact_e),
            (f"SPHERE_QFAR_VS_EXACT_X{x:g}", qfar, exact_q),
        ):
            er = relerr(a, b)
            checks.append(Check(name, a, b, er, er <= RELERR_TOL_RADIAL))

        # Finite-thickness shell: source identity only.
        rho2 = normalize_rho(r, np.where((r >= 0.75 * R) & (r <= R), 1.0, 0.0))
        psi2 = radial_green(r, rho2, mu)
        ef2, es2, _ = radial_ledger(r, rho2, psi2, mu)
        er = relerr(ef2, es2)
        checks.append(Check(f"FINITE_SHELL_FIELD_VS_SOURCE_X{x:g}", ef2, es2, er, er <= RELERR_TOL_RADIAL))

        # Ideal thin shell: direct piecewise field-energy integration.
        if mu == 0.0:
            psi3 = 1.0 / np.maximum(r, R)
        else:
            inside = r <= R
            psi3 = np.empty_like(r)
            y = mu * r[inside]
            i0 = np.ones_like(y)
            mask = np.abs(y) > 1.0e-12
            i0[mask] = np.sinh(y[mask]) / y[mask]
            psi3[inside] = math.exp(-x) / R * i0
            rout = r[~inside]
            psi3[~inside] = (math.sinh(x) / x) * np.exp(-mu * rout) / rout
        dp = np.gradient(psi3, r, edge_order=2)
        enum = G * float(np.trapezoid(r**2 * (dp**2 + mu**2 * psi3**2), r))
        enum += G * rmax**2 * (mu + 1.0 / rmax) * float(psi3[-1]) ** 2
        eexact = G / R * shell_self_factor(x)
        er = relerr(enum, eexact)
        checks.append(Check(f"THIN_SHELL_NUM_VS_EXACT_X{x:g}", enum, eexact, er, er <= RELERR_TOL_RADIAL))

    return checks


# -----------------------------------------------------------------------------
# Cheap morphology comparators (not optimized physical sources)
# -----------------------------------------------------------------------------

def optimized_uniform_disk(a: float, d: float, alpha_m: float) -> dict[str, float]:
    """Massless uniform thin disk in the strict plane z=-d."""
    c_disk = 16.0 / (3.0 * math.pi)  # scalar field-energy coefficient
    gpsi = a / (2.0 * G * abs(alpha_m))

    def coeff(logx: float) -> float:
        x = math.exp(logx)
        denom = 2.0 * (1.0 - 1.0 / math.sqrt(1.0 + x**2))
        qdim = x**2 / denom
        return c_disk * qdim**2 / x

    opt = minimize_scalar(coeff, bounds=(math.log(0.02), math.log(50.0)), method="bounded")
    x = math.exp(float(opt.x))
    denom = 2.0 * (1.0 - 1.0 / math.sqrt(1.0 + x**2))
    qdim = x**2 / denom
    qabs = qdim * gpsi * d**2
    R = x * d
    ephi = c_disk * G * qabs**2 / R
    return {"radius_m": R, "radius_over_d": x, "qabs_kg": qabs, "field_energy_j": ephi}


def embedded_neutral_shell(a: float, d: float, alpha_m: float) -> dict[str, float]:
    """Two-sided sigma~cos(theta) shell control; NOT true stand-off."""
    gpsi = a / (2.0 * G * abs(alpha_m))
    ecav = G * gpsi**2 * d**3 / 3.0
    return {
        "field_energy_j": 3.0 * ecav,
        "qabs_kg": 1.5 * gpsi * d**2,
        "net_charge_kg": 0.0,
        "over_cavity": 3.0,
    }


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    print("=== 031A SCALAR-CHARGE ENERGY / DUAL-KERNEL THEOREM GATE ===")
    print("CLAIM_CLASS=ANALYTIC_AND_NUMERICAL_PREFLIGHT")
    print("TRUE_ANTIGRAVITY_TARGET=YES_ONE_PHYSICAL_METRIC")
    print("MICROSCOPIC_SOURCE=NO")
    print("PRACTICAL_DEVICE=NO")
    print(f"PRIMARY_D_M={PRIMARY_D:.15e}")
    print(f"PRIMARY_PAYLOAD_RADIUS_M={PRIMARY_PAYLOAD_RADIUS:.15e}")

    checks: list[Check] = []

    print("\n=== A — THEOREM RECONSTRUCTION ===")
    for lam in (math.inf, 3.0 * PRIMARY_D, PRIMARY_D, 0.5 * PRIMARY_D):
        c1 = cavity_energy(PRIMARY_ACCEL, PRIMARY_D, PRIMARY_PAYLOAD_RADIUS, 1.0, lam)
        c2 = cavity_direct(PRIMARY_ACCEL, PRIMARY_D, PRIMARY_PAYLOAD_RADIUS, 1.0, lam)
        er = relerr(c1, c2)
        checks.append(Check(f"CAVITY_LAMBDA_{lam}", c1, c2, er, er <= RELERR_TOL_STRICT))

        h1 = halfspace_energy(PRIMARY_ACCEL, PRIMARY_D, PRIMARY_PAYLOAD_RADIUS, 1.0, lam)
        h2 = halfspace_direct_k(PRIMARY_ACCEL, PRIMARY_D, PRIMARY_PAYLOAD_RADIUS, 1.0, lam)
        er = relerr(h1, h2)
        checks.append(Check(f"HALFSPACE_LAMBDA_{lam}", h1, h2, er, er <= RELERR_TOL_STRICT))

    for lam in (3.0 * PRIMARY_D, PRIMARY_D, 0.5 * PRIMARY_D):
        mu = 1.0 / lam
        p1 = payload_factor(mu, PRIMARY_PAYLOAD_RADIUS)
        p2 = payload_average_direct(mu, PRIMARY_PAYLOAD_RADIUS)
        er = relerr(p1, p2)
        checks.append(Check(f"PAYLOAD_FACTOR_LAMBDA_{lam}", p1, p2, er, er <= RELERR_TOL_STRICT))

    checks.extend(validate_finite_sources())
    for c in checks:
        print(f"{c.name}: A={c.a:.15e} B={c.b:.15e} RELERR={c.relerr:.3e} PASS={c.passed}")
    normalization_pass = all(c.passed for c in checks)
    print(f"NORMALIZATION_RECONSTRUCTION={'PASS' if normalization_pass else 'FAIL'}")

    print("\n=== B — PRIMARY 1g / 1m CLEARANCE THEOREMS ===")
    ecav1 = cavity_energy(PRIMARY_ACCEL, PRIMARY_D, PRIMARY_PAYLOAD_RADIUS, 1.0, math.inf)
    ehalf1 = halfspace_energy(PRIMARY_ACCEL, PRIMARY_D, PRIMARY_PAYLOAD_RADIUS, 1.0, math.inf)
    product0 = coupling_product_floor(PRIMARY_ACCEL, PRIMARY_D, PRIMARY_TARGET_J)
    print(f"CAVITY_FLOOR_ALPHA1_J={ecav1:.15e}")
    print(f"TRUE_STANDOFF_HALFSPACE_FLOOR_ALPHA1_J={ehalf1:.15e}")
    print(f"HALFSPACE_OVER_CAVITY={ehalf1/ecav1:.15e}")
    print(f"ALPHA_M_MIN_FIELD_ONLY_1TJ={math.sqrt(ehalf1/PRIMARY_TARGET_J):.15e}")
    print(f"ALPHA_M_MIN_FIELD_ONLY_1E11J={math.sqrt(ehalf1/STRONG_TARGET_J):.15e}")
    print(f"ALPHA_M_ALPHA_X_PRODUCT_FLOOR_IGNORE_FIELD={product0:.15e}")
    print(f"EQUAL_SPLIT_SQRT_PRODUCT={math.sqrt(product0):.15e}")
    print(f"LONG_RANGE_BD_REFERENCE_ALPHA_M={ALPHA_M_BD_LONG_RANGE_REFERENCE:.15e}")

    rows: list[dict[str, float | str]] = []
    physical_alphas = (1.0, 2.0, 3.0, 5.0, 10.0)
    blind_wildcards = (0.625, 1.6, 1.875, 3.125, 5.0)
    for label, alphas in (("PHYSICAL", physical_alphas), ("BLIND_WILDCARD", blind_wildcards)):
        for alpha_m in alphas:
            row = dual_source_bound(
                PRIMARY_ACCEL,
                PRIMARY_D,
                PRIMARY_PAYLOAD_RADIUS,
                alpha_m,
                math.inf,
                PRIMARY_TARGET_J,
            )
            if row is None:
                print(f"{label}_ALPHA_M={alpha_m:g} DUAL_BOUND=FIELD_FLOOR_EXCEEDS_1TJ")
                rows.append({"scan": label, "alpha_m": alpha_m, "status": "field_floor_exceeds_target"})
            else:
                print(
                    f"{label}_ALPHA_M={alpha_m:g} "
                    f"E_FIELD_J={row['field_energy_floor_j']:.15e} "
                    f"QABS_KG={row['qabs_floor_kg']:.15e} "
                    f"ALPHA_X_MIN={row['abs_alpha_x_floor']:.15e} "
                    f"FX_GEV_MAX={row['fx_scale_gev_max']:.15e}"
                )
                rows.append({"scan": label, "alpha_m": alpha_m, "status": "ok", **row})

    print("\n=== C — RANGE / LEAKAGE TENSION ===")
    qmassless = qabs_lower(PRIMARY_ACCEL, PRIMARY_D, PRIMARY_PAYLOAD_RADIUS, 1.0, math.inf)
    for ratio in (10.0, 3.0, 1.0, 0.5, 0.3, 0.2, 0.1):
        lam = ratio * PRIMARY_D
        e = halfspace_energy(PRIMARY_ACCEL, PRIMARY_D, PRIMARY_PAYLOAD_RADIUS, 1.0, lam)
        q = qabs_lower(PRIMARY_ACCEL, PRIMARY_D, PRIMARY_PAYLOAD_RADIUS, 1.0, lam)
        print(
            f"LAMBDA_OVER_D={ratio:g} "
            f"E_OVER_MASSLESS={e/ehalf1:.15e} "
            f"QABS_OVER_MASSLESS={q/qmassless:.15e}"
        )

    print("\n=== D — SIMPLE MORPHOLOGY COMPARATORS ===")
    disk = optimized_uniform_disk(PRIMARY_ACCEL, PRIMARY_D, 1.0)
    embedded = embedded_neutral_shell(PRIMARY_ACCEL, PRIMARY_D, 1.0)
    print(f"UNIFORM_DISK_OPT_RADIUS_OVER_D={disk['radius_over_d']:.15e}")
    print(f"UNIFORM_DISK_E_ALPHA1_J={disk['field_energy_j']:.15e}")
    print(f"UNIFORM_DISK_OVER_HALFSPACE={disk['field_energy_j']/ehalf1:.15e}")
    print(f"UNIFORM_DISK_ALPHA_M_MIN_1TJ={math.sqrt(disk['field_energy_j']/PRIMARY_TARGET_J):.15e}")
    print(f"EMBEDDED_NEUTRAL_SHELL_E_ALPHA1_J={embedded['field_energy_j']:.15e}")
    print("EMBEDDED_NEUTRAL_SHELL_TRUE_STANDOFF=NO_TWO_SIDED_CONTROL")

    print("\n=== E — SECONDARY 0.1g / 1cm / 1PJ BENCHMARK ===")
    sec_e = halfspace_energy(
        SECONDARY_ACCEL, SECONDARY_D, SECONDARY_PAYLOAD_RADIUS, 1.0, math.inf
    )
    sec_prod = coupling_product_floor(SECONDARY_ACCEL, SECONDARY_D, SECONDARY_TARGET_J)
    sec_dual = dual_source_bound(
        SECONDARY_ACCEL,
        SECONDARY_D,
        SECONDARY_PAYLOAD_RADIUS,
        1.0,
        math.inf,
        SECONDARY_TARGET_J,
    )
    print(f"SECONDARY_HALFSPACE_E_ALPHA1_J={sec_e:.15e}")
    print(f"SECONDARY_COUPLING_PRODUCT_FLOOR={sec_prod:.15e}")
    if sec_dual is not None:
        print(f"SECONDARY_ALPHA_X_MIN_ALPHA_M1={sec_dual['abs_alpha_x_floor']:.15e}")
        print(f"SECONDARY_FX_GEV_MAX_ALPHA_M1={sec_dual['fx_scale_gev_max']:.15e}")

    print("\n=== F — DECISION ===")
    halfspace_1tj_possible = ehalf1 < PRIMARY_TARGET_J
    disk_alpha1_1tj = disk["field_energy_j"] < PRIMARY_TARGET_J
    print(f"NORMALIZATION_PASS={normalization_pass}")
    print(f"TRUE_STANDOFF_HALFSPACE_ALPHA1_BELOW_1TJ={halfspace_1tj_possible}")
    print(f"UNIFORM_DISK_ALPHA1_BELOW_1TJ={disk_alpha1_1tj}")
    print("SOURCE_CHARGE_GATING_ALONE_WITH_TINY_PAYLOAD_ALPHA=NO")
    print("ON_STATE_RANGE_MUCH_SHORTER_THAN_STANDOFF_ENERGY_EFFICIENT=NO")
    print("DYNAMICAL_COUPLING_OR_RANGE_ACTIVATION_REQUIRED_IF_OFF_STATE_IS_SMALL=YES")
    print("MICROSCOPIC_B7_OR_QBALL_PROMOTION=NO_NOT_YET")

    if not normalization_pass:
        classification = "RED_NORMALIZATION_FAILURE"
        next_action = "DIAGNOSE_031A_NORMALIZATION"
    elif not halfspace_1tj_possible:
        classification = "RED_TRUE_STANDOFF_ORACLE_FIELD_FLOOR"
        next_action = "DEMOTE_CANONICAL_031_ROUTE"
    else:
        classification = "GREEN_FOR_ONE_SIDED_PARETO_MORPHOLOGY_ONLY"
        next_action = "031A_R2_ONE_SIDED_LENS_PARETO_ENERGY_QABS_LEAKAGE"

    print(f"031A_CLASSIFICATION={classification}")
    print(f"NEXT={next_action}")

    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "classification": classification,
        "next": next_action,
        "normalization_pass": normalization_pass,
        "primary": {
            "acceleration_m_s2": PRIMARY_ACCEL,
            "payload_radius_m": PRIMARY_PAYLOAD_RADIUS,
            "clearance_m": PRIMARY_CLEARANCE,
            "d_m": PRIMARY_D,
            "target_j": PRIMARY_TARGET_J,
            "cavity_floor_alpha1_j": ecav1,
            "halfspace_floor_alpha1_j": ehalf1,
            "halfspace_over_cavity": ehalf1 / ecav1,
            "alpha_m_min_field_only_1tj": math.sqrt(ehalf1 / PRIMARY_TARGET_J),
            "alpha_m_min_field_only_1e11j": math.sqrt(ehalf1 / STRONG_TARGET_J),
            "alpha_product_floor_ignore_field": product0,
            "long_range_bd_reference_alpha_m": ALPHA_M_BD_LONG_RANGE_REFERENCE,
            "dual_scan": rows,
            "uniform_disk": disk,
            "embedded_neutral_shell_control": embedded,
        },
        "secondary": {
            "acceleration_m_s2": SECONDARY_ACCEL,
            "payload_radius_m": SECONDARY_PAYLOAD_RADIUS,
            "clearance_m": SECONDARY_CLEARANCE,
            "d_m": SECONDARY_D,
            "target_j": SECONDARY_TARGET_J,
            "halfspace_floor_alpha1_j": sec_e,
            "alpha_product_floor_ignore_field": sec_prod,
            "dual_alpha_m1": sec_dual,
        },
        "checks": [asdict(c) for c in checks],
        "claim_limits": [
            "No microscopic source or activation field is constructed.",
            "All theorem energies are optimistic lower bounds.",
            "No negative interaction-energy cancellation is credited.",
            "The half-space optimum need not be attainable by a finite compact source.",
            "The uniform disk is a comparator, not an optimized physical realization.",
            "The embedded neutral shell is explicitly two-sided and cannot be promoted as true stand-off.",
            "Full source/scalar/gate/support T_munu, GR backreaction, stability, EFT and empirical leakage remain mandatory.",
        ],
    }

    summary_path = RESULTS_DATA / "031a_scalar_charge_energy_dual_kernel_theorem_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    csv_path = RESULTS_DATA / "031a_scalar_charge_dual_bound_scan.csv"
    fieldnames = sorted({key for row in rows for key in row})
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"SUMMARY_JSON={summary_path}")
    print(f"DUAL_SCAN_CSV={csv_path}")
    return 0 if normalization_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
