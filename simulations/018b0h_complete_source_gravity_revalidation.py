#!/usr/bin/env python3
"""Simulation 018B-0H — complete corrected-source gravity revalidation.

PURPOSE
-------
Close the source-level realization program for the literature-backed two-current
stationary rim plus nonthermal KLS wall after the fully coupled local junction
was solved in 018B-0G2.

SCIENTIFIC QUESTION
-------------------
Using the *measured junction-corrected worldsheet tensor* rather than the old
018B-0F provisional EOS, does there exist a robust exact dual-integer stationary
loop that simultaneously satisfies:

- positive wall-supporting azimuthal pressure;
- exact closed-loop integer winding for both current carriers;
- near-exact membrane/rim mechanical balance;
- large separation between loop radius and microscopic wall/rim widths;
- positive total far-field active mass;
- outward finite-payload gravity with finite wall thickness included;
- survival under conservative rim-core smearing;
- survival under a declared source-ledger perturbation stress test;
- a finite repulsive payload-height operating basin;
- complete inclusion of the measured local junction correction.

This is the final source-level closeout before the true global toroidal 018B
Euler-Lagrange solve.  A GREEN result authorizes that solve.  It does not itself
constitute 018B GREEN.

UPSTREAM PHYSICS
----------------
018B-0D supplies the two-current phase gradients.  Their Lorentz invariants
fix the transverse straight-string microstate.

018B-0F0 supplies the common-gauge KLS wall tension, active source, wall width,
and rim-core width proxy.

018B-0G2 supplies the fully coupled matched local junction correction and the
corrected 1+1 worldsheet tensor in the original zero-momentum reference frame:

    U_c,
    T_c,
    J_c.

The local junction changed the EOS, so the old 018B-0F integer pair is NOT a
promotion input.  Exact stationarity is re-solved from scratch here.

WORLDSHEET TRANSFORMATION
-------------------------
Write the corrected reference-frame stress as

    T^{ab} = [[U, J], [J, -T]].

Under a boost v along the string,

    E' = gamma^2 [U - v^2 T - 2 v J],

    P' = gamma^2 [-T + v^2 U - 2 v J],

    J' = gamma^2 [(1+v^2)J - v(U-T)].

The gravitoelectric active line source is

    Lambda_active = E' + P'.

Exact dual-integer closure uses the boosted phase gradients

    k_i' = gamma (k_i - v omega_i)

with

    k_Phi' R   = N_Phi,
    k_Sigma' R = N_Sigma.

For every coprime base winding pair, the common boost is solved algebraically.
A common integer multiplier is then chosen to satisfy wall balance.

FINITE-THICKNESS WALL GRAVITY
-----------------------------
Unlike the earlier 018B-0F scout, the primary gravity evaluation reconstructs
the planar microscopic H-A wall profile and integrates its actual active-source
density through the wall thickness.

For the static planar scalar wall,

    S_wall(z) = rho + p_x + p_y + p_z = -2 V(z).

For each z slice of a finite disk of radius R, the axial outward contribution
is evaluated with the exact disk kernel and integrated numerically.

The wall integral is independently evaluated by both Simpson quadrature and
Gauss-Legendre quadrature.  Their agreement is a numerical cross-check.

RIM FINITE-SIZE ENVELOPE
------------------------
The actual curved rim core is not yet solved.  Therefore the complete positive
rim line active source is placed at the most attractive point of a conservative
cross-section envelope

    Delta r = 0, +/- 2 core_width,
    Delta z = 0, +/- 2 core_width.

A secondary stress diagnostic repeats this with +/-3 core widths.

FINITE PAYLOAD
--------------
The payload is a uniform sphere with radius

    a = 0.25 h.

Candidates must keep the payload bottom at least five measured wall widths from
the wall center.  The reconstructed wall tail above the payload bottom is also
integrated explicitly; it must be negligible.  With the source outside the
payload volume, the harmonic mean-value identity makes the payload CM axial
acceleration equal to the center acceleration in linearized gravity.

The code additionally maps the adverse source-level repulsive h/R basin and
reports its upper sign-change boundary.

ROBUSTNESS
----------
The nominal candidate is not enough.

A 3^4 = 81 source-ledger stress test independently varies

    corrected U,
    corrected T,
    wall tension,
    wall active source

by factors

    0.995, 1.000, 1.005.

For every stress corner the code re-solves the exact dual-integer loop; it does
not freeze the nominal winding pair.

This +/-0.5 percent stress is deliberately much larger than the measured 0G2
corrected-active-line numerical spread.  It is a conservative source-ledger
sensitivity test, NOT a microscopic parameter scan and NOT evidence of a new
physical basin in Lagrangian parameter space.

A separate blind wildcard height diagnostic uses the project's requested
numbers 0.625, 1.6, 1.875, 3.125, and 5.0 as multipliers of the selected h/R.
Those values are explicitly excluded from selection and promotion.

ENERGY COEFFICIENT
------------------
At source level,

    E_total/R = pi sigma_W R + 2 pi E'_rim.

The projected payload coefficient is

    C_eff = (E_total/R) / [F_payload (h/R)^2].

The fully coupled local junction is included through the corrected worldsheet
EOS.  However the curved global toroidal fields, frame dragging, and nonlinear
Einstein-matter solution are still absent.  Therefore any C reported here is

    SOURCE_LEVEL_PROJECTED_NOT_GLOBAL_018B_VALIDATED.

ANGULAR MOMENTUM
----------------
Because the surviving architecture is stationary rather than static, report

    J_total = 2 pi R^2 J'_line.

This is carried forward to the later stationary/frame-dragging gate.  It is not
ignored or canceled by assumption.

PROMOTION CONDITION
-------------------
018B-0H is GREEN only if all of the following hold:

- upstream 018B-0D, 018B-0F0, and 018B-0G2 are GREEN;
- finite wall profile reconstructs the logged wall tension/active source;
- at least one exact dual-integer stationary candidate survives;
- wall balance error <= 1e-4;
- |v| <= 0.99;
- R/wall_width90 >= 10;
- finite-payload adverse force is outward;
- total active mass is positive;
- Simpson and Gauss-Legendre gravity reconstructions agree;
- the repulsive operating basin has nonzero clearance-safe width;
- all 81 source-ledger stress cases possess a surviving exact-integer candidate;
- the measured fully coupled junction correction is included.

If GREEN, the next action is the true global 018B finite-thickness toroidal
Euler-Lagrange solve required by RESEARCH_BUILDPLAN.md.

FALSIFICATION / STOP RULE
-------------------------
If exact integer reoptimization fails, the finite-thickness wall reverses the
gravity sign, positive far active mass is lost, or the 81-corner ledger stress
fails broadly, do not launch the global toroidal solve merely because the old
018B-0F pair looked favorable.  Classify the failed gate first.

CLAIM LIMITS
------------
A GREEN result does NOT establish:

- the global curved toroidal matter-field solution;
- global Euler-Lagrange residual convergence;
- full local covariant conservation of the curved source;
- full composite dynamical stability;
- frame-dragging consistency;
- nonlinear Einstein-matter consistency;
- practical energy scaling;
- experimental antigravity;
- a practical antigravity device;
- new physics or novelty.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018B0H_COMPLETE_CORRECTED_SOURCE_GRAVITY_REVALIDATION
"""

from __future__ import annotations

from dataclasses import dataclass
import itertools
import math
from pathlib import Path
import re

import numpy as np
from scipy.integrate import simpson, solve_bvp
from scipy.optimize import brentq, minimize_scalar


ROOT = Path(__file__).resolve().parents[1]

D_LOG = ROOT / "results/logs/018b0d_literature_two_current_counterflow_gate.log"
F0_LOG = ROOT / "results/logs/018b0f0_lilley_kls_same_gauge_normalization_wall_bridge.log"
G2_LOG = ROOT / "results/logs/018b0g2_fully_coupled_two_current_matched_2d_junction.log"

BASE_WINDING_MAX = 1000
MAX_ABS_V = 0.99
BALANCE_REL_TOL = 1.0e-4
MIN_R_OVER_WALL90 = 10.0
MIN_PAYLOAD_BOTTOM_OVER_WALL90 = 5.0
PAYLOAD_RADIUS_OVER_H = 0.25
X_MIN = 0.01
X_MAX = 0.45

RIM_ENVELOPE_MULTIPLIER = 2.0
SEVERE_RIM_ENVELOPE_MULTIPLIER = 3.0

LEDGER_STRESS_LEVELS = (0.995, 1.0, 1.005)

WILDCARD_X_FACTORS = (0.625, 1.6, 1.875, 3.125, 5.0)

VALIDATED_C = 1.774169582609975e6
VALIDATED_MASS_1G_1M = 2.606814218315347e17
VALIDATED_ENERGY_1G_1M = 2.342887778715687e34

LAMBDA_H = 1.0
F_A = 0.075
H_LOCK = 0.010
LAMBDA_A = 1.0
C_H = H_LOCK * F_A * F_A
C_A = 2.0 * H_LOCK
V0 = 2.0 * H_LOCK * F_A * F_A


@dataclass(frozen=True)
class Inputs:
    """All measured quantities required by the 018B-0H closeout."""

    omega_phi: float
    k_phi: float
    omega_sigma: float
    k_sigma: float

    U: float
    T: float
    J: float

    wall_tension: float
    wall_active: float
    wall_width90: float
    core_width: float

    g2_resolution_active_spread: float
    g2_patch_active_spread: float
    g2_blend_active_spread: float


@dataclass(frozen=True)
class BaseClosure:
    """One coprime dual-winding ratio and its exact closure boost."""

    n_phi: int
    n_sigma: int
    v: float
    gamma: float
    radius_unit: float


@dataclass
class Candidate:
    """One exact dual-integer stationary source-level candidate."""

    base_phi: int
    base_sigma: int
    multiplier: int
    n_phi: int
    n_sigma: int

    v: float
    gamma: float
    radius: float

    E_line: float
    P_line: float
    J_line: float
    active_line: float

    omega_phi_lab: float
    k_phi_lab: float
    omega_sigma_lab: float
    k_sigma_lab: float

    balance_rel: float

    x: float = math.nan
    projected_c: float = math.inf
    net_outward: float = -math.inf
    active_mass_per_r: float = -math.inf
    payload_clearance: float = -math.inf


@dataclass(frozen=True)
class WallProfile:
    """Reconstructed planar microscopic wall profile."""

    z: np.ndarray
    H: np.ndarray
    A: np.ndarray
    potential: np.ndarray
    active_density: np.ndarray
    tension: float
    active: float
    max_rms: float


def require_marker(path: Path, marker: str) -> None:
    """Require an upstream GREEN marker before inheriting its results."""

    if not path.exists():
        raise RuntimeError(f"Missing required upstream log: {path}")

    text = path.read_text(errors="replace")

    if marker not in text:
        raise RuntimeError(f"Missing upstream marker {marker!r} in {path}")


def scalar(path: Path, label: str) -> float:
    """Read one finite floating-point scalar immediately following a label."""

    text = path.read_text(errors="replace")
    number = r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
    match = re.search(re.escape(label) + number, text)

    if match is None:
        raise RuntimeError(f"Could not find {label!r} in {path}")

    value = float(match.group(1))

    if not math.isfinite(value):
        raise RuntimeError(f"Nonfinite {label!r} in {path}")

    return value


def load_inputs() -> Inputs:
    """Load only quantities explicitly produced by GREEN upstream gates."""

    require_marker(D_LOG, "018B0D_TWO_CURRENT_COUNTERFLOW_GATE=GREEN")
    require_marker(F0_LOG, "018B0F0_LILLEY_KLS_NORMALIZATION_WALL_BRIDGE=GREEN")
    require_marker(
        G2_LOG,
        "018B0G2_FULLY_COUPLED_TWO_CURRENT_2D_STRING_WALL_JUNCTION=GREEN",
    )

    return Inputs(
        omega_phi=scalar(D_LOG, "OMEGA_PHI="),
        k_phi=scalar(D_LOG, "K_PHI="),
        omega_sigma=scalar(D_LOG, "OMEGA_SIGMA="),
        k_sigma=scalar(D_LOG, "K_SIGMA="),
        U=scalar(G2_LOG, "CORRECTED_EIGENFRAME_U="),
        T=scalar(G2_LOG, "CORRECTED_EIGENFRAME_T="),
        J=scalar(G2_LOG, "CORRECTED_EIGENFRAME_J="),
        wall_tension=scalar(F0_LOG, "NEW_WALL_TENSION="),
        wall_active=scalar(F0_LOG, "NEW_WALL_ACTIVE_SOURCE="),
        wall_width90=scalar(F0_LOG, "NEW_WALL_WIDTH90="),
        core_width=scalar(F0_LOG, "NEW_STRING_GAUGE_CORE_INVERSE_MASS_PROXY="),
        g2_resolution_active_spread=scalar(
            G2_LOG,
            "RESOLUTION_CORRECTED_ACTIVE_LINE_REL_SPREAD=",
        ),
        g2_patch_active_spread=scalar(
            G2_LOG,
            "PATCH_CORRECTED_ACTIVE_LINE_REL_SPREAD=",
        ),
        g2_blend_active_spread=scalar(
            G2_LOG,
            "BLEND_CORRECTED_ACTIVE_LINE_REL_SPREAD=",
        ),
    )


def wall_potential(H, A):
    """Return the H-A KLS wall potential on the zero-carrier wall branch."""

    return (
        LAMBDA_H / 8.0 * (H * H - 1.0) ** 2
        + LAMBDA_A / 4.0 * (A * A - F_A * F_A) ** 2
        - 2.0 * H_LOCK * H * A * A
        + C_H * (H * H - 1.0)
        + C_A * (A * A - F_A * F_A)
        + V0
    )


def solve_wall_profile() -> WallProfile:
    """Independently reconstruct the planar microscopic wall and active profile."""

    k_trial = F_A * math.sqrt(LAMBDA_A) / 2.0
    half_domain = 14.0 / k_trial

    z = np.linspace(0.0, half_domain, 600)

    def ode(_z, y):
        H, Hp, A, Ap = y

        Hpp = (
            0.5 * LAMBDA_H * H * (H * H - 1.0)
            - 2.0 * H_LOCK * A * A
            + 2.0 * C_H * H
        )

        # The complex A kinetic term gives the real-amplitude normalization
        # used by the already-validated 018B-0F0 planar wall.
        App = (
            0.5 * LAMBDA_A * A * (A * A - F_A * F_A)
            - 2.0 * H_LOCK * H * A
            + C_A * A
        )

        return np.vstack((Hp, Hpp, Ap, App))

    def bc(ya, yb):
        return np.array((ya[1], ya[2], yb[0] - 1.0, yb[2] - F_A))

    A0 = F_A * np.tanh(k_trial * z)
    y0 = np.vstack(
        (
            np.ones_like(z),
            np.zeros_like(z),
            A0,
            F_A * k_trial / np.cosh(k_trial * z) ** 2,
        )
    )

    solution = solve_bvp(
        ode,
        bc,
        z,
        y0,
        tol=2.0e-8,
        max_nodes=30000,
    )

    if solution.status != 0:
        raise RuntimeError(f"Planar wall BVP failed: {solution.message}")

    dense_half = np.linspace(0.0, half_domain, 16001)
    Hh, Hph, Ah, Aph = solution.sol(dense_half)

    # Mirror with H even and A odd.
    z_full = np.concatenate((-dense_half[:0:-1], dense_half))
    H = np.concatenate((Hh[:0:-1], Hh))
    Hp = np.concatenate((-Hph[:0:-1], Hph))
    A = np.concatenate((-Ah[:0:-1], Ah))
    Ap = np.concatenate((Aph[:0:-1], Aph))

    potential = wall_potential(H, A)
    kinetic = 0.5 * Hp * Hp + Ap * Ap

    tension = float(simpson(kinetic + potential, x=z_full))

    # For the static planar wall, the active source is -2V.
    active_density = -2.0 * potential
    active = float(simpson(active_density, x=z_full))

    return WallProfile(
        z=z_full,
        H=H,
        A=A,
        potential=potential,
        active_density=active_density,
        tension=tension,
        active=active,
        max_rms=float(np.max(solution.rms_residuals)),
    )


def transform_worldsheet(U: float, T: float, J: float, v: float):
    """Lorentz-transform a general symmetric 1+1 worldsheet stress tensor."""

    gamma = 1.0 / math.sqrt(1.0 - v * v)
    gamma2 = gamma * gamma
    P0 = -T

    E_lab = gamma2 * (U + v * v * P0 - 2.0 * v * J)
    P_lab = gamma2 * (P0 + v * v * U - 2.0 * v * J)
    J_lab = gamma2 * ((1.0 + v * v) * J - v * (U + P0))

    return gamma, E_lab, P_lab, J_lab, E_lab + P_lab


def exact_v(inputs: Inputs, n_phi: int, n_sigma: int):
    """Return the exact boost required by one coprime winding ratio."""

    denominator = (
        inputs.omega_phi * n_sigma
        - inputs.omega_sigma * n_phi
    )

    if abs(denominator) < 1.0e-15:
        return None

    return (
        inputs.k_phi * n_sigma
        - inputs.k_sigma * n_phi
    ) / denominator


def precompute_base_closures(inputs: Inputs) -> list[BaseClosure]:
    """Precompute exact closure boosts independent of the corrected EOS."""

    closures: list[BaseClosure] = []

    # The corrected transverse threshold is close to the historical one.  The
    # loose 0.93 prefilter only saves work; the exact T/U test is applied later.
    loose_v2_floor = 0.93

    for n_phi in range(-BASE_WINDING_MAX, BASE_WINDING_MAX + 1):
        if n_phi == 0:
            continue

        for n_sigma in range(-BASE_WINDING_MAX, BASE_WINDING_MAX + 1):
            if n_sigma == 0:
                continue

            if math.gcd(abs(n_phi), abs(n_sigma)) != 1:
                continue

            v = exact_v(inputs, n_phi, n_sigma)

            if (
                v is None
                or not math.isfinite(v)
                or abs(v) >= MAX_ABS_V
                or v * v <= loose_v2_floor
            ):
                continue

            gamma = 1.0 / math.sqrt(1.0 - v * v)

            k_phi_lab = gamma * (inputs.k_phi - v * inputs.omega_phi)
            k_sigma_lab = gamma * (inputs.k_sigma - v * inputs.omega_sigma)

            if abs(k_phi_lab) < 1.0e-15 or abs(k_sigma_lab) < 1.0e-15:
                continue

            radius_phi = n_phi / k_phi_lab
            radius_sigma = n_sigma / k_sigma_lab

            if radius_phi <= 0.0 or radius_sigma <= 0.0:
                continue

            radius_rel = abs(radius_phi - radius_sigma) / max(
                abs(radius_phi),
                abs(radius_sigma),
                1.0e-30,
            )

            if radius_rel > 2.0e-12:
                continue

            closures.append(
                BaseClosure(
                    n_phi=n_phi,
                    n_sigma=n_sigma,
                    v=v,
                    gamma=gamma,
                    radius_unit=0.5 * (radius_phi + radius_sigma),
                )
            )

    return closures


def wall_disk_kernel(radius: float, vertical: np.ndarray) -> np.ndarray:
    """Axis kernel for a unit-active-density finite disk slice."""

    return 2.0 * math.pi * radius * (
        1.0
        - vertical / np.sqrt(radius * radius + vertical * vertical)
    )


def wall_outward_simpson(
    profile: WallProfile,
    radius: float,
    h_payload: float,
) -> float:
    """Integrate the finite-thickness negative wall source by Simpson rule."""

    vertical = h_payload - profile.z
    kernel = wall_disk_kernel(radius, vertical)

    # active_density is negative.  Positive return value means outward.
    return float(
        simpson(
            (-profile.active_density) * kernel,
            x=profile.z,
        )
    )


def wall_outward_gauss(
    profile: WallProfile,
    radius: float,
    h_payload: float,
    order: int = 256,
) -> float:
    """Independent Gauss-Legendre reconstruction of finite wall gravity."""

    nodes, weights = np.polynomial.legendre.leggauss(order)

    z_min = float(profile.z[0])
    z_max = float(profile.z[-1])

    z = 0.5 * (z_max - z_min) * nodes + 0.5 * (z_max + z_min)
    w = 0.5 * (z_max - z_min) * weights

    active = np.interp(z, profile.z, profile.active_density)
    vertical = h_payload - z
    kernel = wall_disk_kernel(radius, vertical)

    return float(np.sum(w * (-active) * kernel))


def ring_kernel(radius: float, z_source: float, h_payload: float) -> float:
    """Positive-magnitude axial Green kernel for a circular source ring."""

    vertical = h_payload - z_source
    return vertical / (radius * radius + vertical * vertical) ** 1.5


def gravity_fast(
    inputs: Inputs,
    candidate: Candidate,
    x: float,
    *,
    rim_envelope_multiplier: float,
):
    """Cheap thin-wall search kernel used only for candidate enumeration.

    The full finite-thickness wall profile is evaluated after selection.  This
    search approximation uses the already reconstructed integrated wall active
    source at z=0 and the same conservative rim-core envelope.  018B-0H
    explicitly checks the selected-point thin/full difference before GREEN.
    """

    radius = candidate.radius
    h_payload = x * radius

    wall_kernel = 1.0 - h_payload / math.sqrt(
        radius * radius + h_payload * h_payload
    )

    wall_outward = (
        2.0
        * math.pi
        * (-inputs.wall_active)
        * radius
        * wall_kernel
    )

    q_rim = 2.0 * math.pi * radius * candidate.active_line
    envelope = rim_envelope_multiplier * inputs.core_width

    inward_kernel = max(
        ring_kernel(radius + dr, dz, h_payload)
        for dr in (-envelope, 0.0, envelope)
        for dz in (-envelope, 0.0, envelope)
        if radius + dr > 0.0
    )

    rim_inward = radius * q_rim * inward_kernel
    net_outward = wall_outward - rim_inward

    active_mass_per_r = (
        2.0 * math.pi * candidate.active_line
        + math.pi * inputs.wall_active * radius
    )

    energy_per_r = (
        math.pi * inputs.wall_tension * radius
        + 2.0 * math.pi * candidate.E_line
    )

    projected_c = (
        energy_per_r / (net_outward * x * x)
        if net_outward > 0.0
        else math.inf
    )

    payload_bottom = (1.0 - PAYLOAD_RADIUS_OVER_H) * h_payload
    clearance = payload_bottom / inputs.wall_width90

    return {
        "net_outward": net_outward,
        "projected_c": projected_c,
        "active_mass_per_r": active_mass_per_r,
        "payload_clearance": clearance,
        "wall_outward": wall_outward,
        "rim_inward": rim_inward,
    }


def gravity(
    inputs: Inputs,
    profile: WallProfile,
    candidate: Candidate,
    x: float,
    *,
    rim_envelope_multiplier: float,
):
    """Evaluate finite-wall plus conservative finite-rim source-level gravity."""

    radius = candidate.radius
    h_payload = x * radius

    wall_simpson = wall_outward_simpson(profile, radius, h_payload)
    wall_gauss = wall_outward_gauss(profile, radius, h_payload)

    wall_relerr = abs(wall_simpson - wall_gauss) / max(
        abs(wall_simpson),
        abs(wall_gauss),
        1.0e-30,
    )

    q_rim = 2.0 * math.pi * radius * candidate.active_line

    envelope = rim_envelope_multiplier * inputs.core_width

    inward_kernel = max(
        ring_kernel(radius + dr, dz, h_payload)
        for dr in (-envelope, 0.0, envelope)
        for dz in (-envelope, 0.0, envelope)
        if radius + dr > 0.0
    )

    rim_inward = radius * q_rim * inward_kernel
    net_outward = wall_simpson - rim_inward

    active_mass_per_r = (
        2.0 * math.pi * candidate.active_line
        + math.pi * inputs.wall_active * radius
    )

    energy_per_r = (
        math.pi * inputs.wall_tension * radius
        + 2.0 * math.pi * candidate.E_line
    )

    projected_c = (
        energy_per_r / (net_outward * x * x)
        if net_outward > 0.0
        else math.inf
    )

    payload_bottom = (1.0 - PAYLOAD_RADIUS_OVER_H) * h_payload
    clearance = payload_bottom / inputs.wall_width90

    # Exponentially small wall tail entering the nominal payload region.
    tail_mask = profile.z >= payload_bottom

    if np.any(tail_mask):
        tail_active = float(
            simpson(
                np.abs(profile.active_density[tail_mask]),
                x=profile.z[tail_mask],
            )
        )
    else:
        tail_active = 0.0

    tail_fraction = tail_active / max(abs(profile.active), 1.0e-30)

    return {
        "net_outward": net_outward,
        "projected_c": projected_c,
        "active_mass_per_r": active_mass_per_r,
        "payload_clearance": clearance,
        "wall_outward": wall_simpson,
        "wall_outward_gauss": wall_gauss,
        "wall_gravity_relerr": wall_relerr,
        "rim_inward": rim_inward,
        "tail_fraction": tail_fraction,
    }


def candidate_invariants(inputs: Inputs, candidate: Candidate):
    """Independently verify phase and integer closure invariants."""

    w_phi_before = inputs.omega_phi**2 - inputs.k_phi**2
    w_phi_after = candidate.omega_phi_lab**2 - candidate.k_phi_lab**2

    w_sigma_before = inputs.omega_sigma**2 - inputs.k_sigma**2
    w_sigma_after = candidate.omega_sigma_lab**2 - candidate.k_sigma_lab**2

    phi_rel = abs(w_phi_after - w_phi_before) / max(abs(w_phi_before), 1.0e-30)
    sigma_rel = abs(w_sigma_after - w_sigma_before) / max(abs(w_sigma_before), 1.0e-30)

    r_phi = candidate.n_phi / candidate.k_phi_lab
    r_sigma = candidate.n_sigma / candidate.k_sigma_lab

    radius_rel = abs(r_phi - r_sigma) / max(abs(r_phi), abs(r_sigma), 1.0e-30)

    return phi_rel, sigma_rel, radius_rel


def search_candidates(
    inputs: Inputs,
    profile: WallProfile,
    closures: list[BaseClosure],
    *,
    U: float,
    T: float,
    J: float,
    wall_tension: float,
    wall_active: float,
    optimize_gravity: bool,
) -> list[Candidate]:
    """Re-solve exact integer stationarity for one declared source ledger."""

    # A temporary input object allows the ledger stress to vary wall quantities
    # without mutating the measured upstream values.
    local_inputs = Inputs(
        omega_phi=inputs.omega_phi,
        k_phi=inputs.k_phi,
        omega_sigma=inputs.omega_sigma,
        k_sigma=inputs.k_sigma,
        U=U,
        T=T,
        J=J,
        wall_tension=wall_tension,
        wall_active=wall_active,
        wall_width90=inputs.wall_width90,
        core_width=inputs.core_width,
        g2_resolution_active_spread=inputs.g2_resolution_active_spread,
        g2_patch_active_spread=inputs.g2_patch_active_spread,
        g2_blend_active_spread=inputs.g2_blend_active_spread,
    )

    # Scale the reconstructed wall active profile so the stress test changes
    # the integrated wall active source but preserves its measured shape.
    profile_scale = wall_active / inputs.wall_active

    local_profile = WallProfile(
        z=profile.z,
        H=profile.H,
        A=profile.A,
        potential=profile.potential,
        active_density=profile.active_density * profile_scale,
        tension=profile.tension * (wall_tension / inputs.wall_tension),
        active=profile.active * profile_scale,
        max_rms=profile.max_rms,
    )

    ct2 = T / U
    found: dict[tuple[int, int], Candidate] = {}

    for closure in closures:
        v = closure.v

        if v * v <= ct2:
            continue

        gamma, E_line, P_line, J_line, active_line = transform_worldsheet(U, T, J, v)

        if P_line <= 0.0 or active_line <= 0.0:
            continue

        multiplier_target = P_line / (wall_tension * closure.radius_unit)
        multiplier_center = int(round(multiplier_target))

        for multiplier in range(
            max(1, multiplier_center - 2),
            max(1, multiplier_center + 2) + 1,
        ):
            radius = multiplier * closure.radius_unit

            if radius / inputs.wall_width90 < MIN_R_OVER_WALL90:
                continue

            wall_load = wall_tension * radius
            balance_rel = abs(P_line - wall_load) / max(
                abs(P_line),
                abs(wall_load),
                1.0e-30,
            )

            if balance_rel > BALANCE_REL_TOL:
                continue

            omega_phi_lab = gamma * (inputs.omega_phi - v * inputs.k_phi)
            k_phi_lab = gamma * (inputs.k_phi - v * inputs.omega_phi)
            omega_sigma_lab = gamma * (inputs.omega_sigma - v * inputs.k_sigma)
            k_sigma_lab = gamma * (inputs.k_sigma - v * inputs.omega_sigma)

            candidate = Candidate(
                base_phi=closure.n_phi,
                base_sigma=closure.n_sigma,
                multiplier=multiplier,
                n_phi=closure.n_phi * multiplier,
                n_sigma=closure.n_sigma * multiplier,
                v=v,
                gamma=gamma,
                radius=radius,
                E_line=E_line,
                P_line=P_line,
                J_line=J_line,
                active_line=active_line,
                omega_phi_lab=omega_phi_lab,
                k_phi_lab=k_phi_lab,
                omega_sigma_lab=omega_sigma_lab,
                k_sigma_lab=k_sigma_lab,
                balance_rel=balance_rel,
            )

            x_floor = (
                MIN_PAYLOAD_BOTTOM_OVER_WALL90
                * inputs.wall_width90
                / ((1.0 - PAYLOAD_RADIUS_OVER_H) * radius)
            )

            x_low = max(X_MIN, x_floor)

            if x_low >= X_MAX:
                continue

            if optimize_gravity:
                def objective(x_value):
                    result = gravity_fast(
                        local_inputs,
                        candidate,
                        float(x_value),
                        rim_envelope_multiplier=RIM_ENVELOPE_MULTIPLIER,
                    )

                    value = result["projected_c"]
                    return value if math.isfinite(value) else 1.0e300

                result = minimize_scalar(
                    objective,
                    bounds=(x_low, X_MAX),
                    method="bounded",
                    options={"xatol": 1.0e-9},
                )

                if not result.success or float(result.fun) >= 1.0e299:
                    continue

                candidate.x = float(result.x)

            else:
                # The stress test only needs a robust physical passer.  Use a
                # deterministic coarse-to-fine h/R search rather than biasing
                # the gate toward the nominal optimum.
                grid = np.linspace(x_low, X_MAX, 72)
                best_x = None
                best_c = math.inf

                for x_value in grid:
                    result = gravity_fast(
                        local_inputs,
                        candidate,
                        float(x_value),
                        rim_envelope_multiplier=RIM_ENVELOPE_MULTIPLIER,
                    )

                    if (
                        result["net_outward"] > 0.0
                        and result["active_mass_per_r"] > 0.0
                        and result["projected_c"] < best_c
                    ):
                        best_c = result["projected_c"]
                        best_x = float(x_value)

                if best_x is None:
                    continue

                candidate.x = best_x

            g = gravity_fast(
                local_inputs,
                candidate,
                candidate.x,
                rim_envelope_multiplier=RIM_ENVELOPE_MULTIPLIER,
            )

            if g["net_outward"] <= 0.0 or g["active_mass_per_r"] <= 0.0:
                continue

            candidate.projected_c = g["projected_c"]
            candidate.net_outward = g["net_outward"]
            candidate.active_mass_per_r = g["active_mass_per_r"]
            candidate.payload_clearance = g["payload_clearance"]

            key = (candidate.n_phi, candidate.n_sigma)
            previous = found.get(key)

            if previous is None or candidate.projected_c < previous.projected_c:
                found[key] = candidate

    return sorted(found.values(), key=lambda item: item.projected_c)


def repulsive_basin_upper(
    inputs: Inputs,
    profile: WallProfile,
    candidate: Candidate,
):
    """Map the clearance-safe adverse repulsive h/R interval."""

    x_floor = (
        MIN_PAYLOAD_BOTTOM_OVER_WALL90
        * inputs.wall_width90
        / ((1.0 - PAYLOAD_RADIUS_OVER_H) * candidate.radius)
    )

    x_start = max(X_MIN, x_floor)

    def net(x_value):
        return gravity(
            inputs,
            profile,
            candidate,
            float(x_value),
            rim_envelope_multiplier=RIM_ENVELOPE_MULTIPLIER,
        )["net_outward"]

    if net(x_start) <= 0.0:
        return x_start, math.nan

    grid = np.linspace(x_start, 0.8, 1201)
    previous_x = float(grid[0])
    previous_y = net(previous_x)

    for x_value in grid[1:]:
        x_value = float(x_value)
        value = net(x_value)

        if previous_y * value < 0.0:
            upper = brentq(net, previous_x, x_value)
            return x_start, float(upper)

        previous_x = x_value
        previous_y = value

    return x_start, math.nan


def main() -> None:
    """Run the complete corrected-source revalidation."""

    print("=== 018B-0H — COMPLETE CORRECTED SOURCE / GRAVITY REVALIDATION ===")

    inputs = load_inputs()

    print("\n=== CORRECTED FULLY COUPLED JUNCTION EOS ===")
    print(f"CORRECTED_EIGENFRAME_U={inputs.U:+.15e}")
    print(f"CORRECTED_EIGENFRAME_T={inputs.T:+.15e}")
    print(f"CORRECTED_EIGENFRAME_J={inputs.J:+.15e}")
    print(f"CORRECTED_CT2={inputs.T / inputs.U:+.15e}")
    print(f"CORRECTED_CT={math.sqrt(inputs.T / inputs.U):+.15e}")
    print("MEASURED_FULLY_COUPLED_JUNCTION_INCLUDED=YES")

    print("\n=== 0G2 NUMERICAL-SPREAD AUDIT ===")
    max_active_spread = max(
        inputs.g2_resolution_active_spread,
        inputs.g2_patch_active_spread,
        inputs.g2_blend_active_spread,
    )
    print(
        "G2_MAX_CORRECTED_ACTIVE_LINE_REL_SPREAD="
        f"{max_active_spread:.15e}"
    )
    print("LEDGER_STRESS_FRACTION=5.000000000000000e-03")
    print(
        "LEDGER_STRESS_OVER_G2_ACTIVE_SPREAD="
        f"{0.005 / max(max_active_spread, 1.0e-30):.15e}"
    )
    print("LEDGER_STRESS_IS_MICROSCOPIC_PARAMETER_ROBUSTNESS=NO")

    print("\n=== INDEPENDENT FINITE WALL RECONSTRUCTION ===")
    profile = solve_wall_profile()

    tension_rel = abs(profile.tension - inputs.wall_tension) / abs(inputs.wall_tension)
    active_rel = abs(profile.active - inputs.wall_active) / abs(inputs.wall_active)

    wall_reconstruction_pass = (
        tension_rel < 2.0e-6
        and active_rel < 2.0e-6
        and profile.max_rms < 1.0e-6
    )

    print(f"WALL_PROFILE_TENSION={profile.tension:+.15e}")
    print(f"WALL_LOG_TENSION={inputs.wall_tension:+.15e}")
    print(f"WALL_TENSION_RECONSTRUCTION_RELERR={tension_rel:.15e}")
    print(f"WALL_PROFILE_ACTIVE={profile.active:+.15e}")
    print(f"WALL_LOG_ACTIVE={inputs.wall_active:+.15e}")
    print(f"WALL_ACTIVE_RECONSTRUCTION_RELERR={active_rel:.15e}")
    print(f"WALL_PROFILE_MAX_RMS={profile.max_rms:.15e}")
    print(
        "FINITE_WALL_PROFILE_RECONSTRUCTION="
        + ("PASS" if wall_reconstruction_pass else "FAIL")
    )

    print("\n=== EXACT DUAL-INTEGER REOPTIMIZATION ===")
    closures = precompute_base_closures(inputs)
    print(f"BASE_WINDING_MAX={BASE_WINDING_MAX}")
    print(f"EXACT_CLOSURE_BASE_STATES={len(closures)}")

    candidates = search_candidates(
        inputs,
        profile,
        closures,
        U=inputs.U,
        T=inputs.T,
        J=inputs.J,
        wall_tension=inputs.wall_tension,
        wall_active=inputs.wall_active,
        optimize_gravity=True,
    )

    print(f"EXACT_INTEGER_CORRECTED_EOS_PASSERS={len(candidates)}")

    if not candidates:
        print("018B0H_COMPLETE_SOURCE_GRAVITY_REVALIDATION=RED")
        print("NEXT=CLASSIFY_EXACT_INTEGER_OR_GRAVITY_FAILURE_BEFORE_TRUE_018B")
        print("CURRENT_HEURISTIC=APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY")
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
        return

    selected = candidates[0]

    phi_rel, sigma_rel, radius_rel = candidate_invariants(inputs, selected)

    print("\n=== SELECTED CORRECTED-EOS INTEGER LOOP ===")
    print(f"BASE_N_PHI={selected.base_phi}")
    print(f"BASE_N_SIGMA={selected.base_sigma}")
    print(f"COMMON_MULTIPLIER={selected.multiplier}")
    print(f"N_PHI={selected.n_phi}")
    print(f"N_SIGMA={selected.n_sigma}")
    print(f"BOOST_V={selected.v:+.15e}")
    print(f"BOOST_GAMMA={selected.gamma:.15e}")
    print(f"LIGHTCONE_MARGIN_1_MINUS_ABS_V={1.0 - abs(selected.v):.15e}")
    print(f"RADIUS={selected.radius:.15e}")
    print(f"R_OVER_WALL90={selected.radius / inputs.wall_width90:.15e}")
    print(f"LAB_ENERGY_LINE={selected.E_line:+.15e}")
    print(f"LAB_P_PARALLEL={selected.P_line:+.15e}")
    print(f"LAB_MOMENTUM_LINE={selected.J_line:+.15e}")
    print(f"LAB_ACTIVE_LINE={selected.active_line:+.15e}")
    print(f"WALL_LOAD={inputs.wall_tension * selected.radius:+.15e}")
    print(f"WALL_BALANCE_RELERR={selected.balance_rel:.15e}")
    print(f"SELECTED_H_OVER_R={selected.x:.15e}")
    print(f"PAYLOAD_BOTTOM_OVER_WALL90={selected.payload_clearance:.15e}")
    print(f"PHI_PHASE_INVARIANT_RELERR={phi_rel:.15e}")
    print(f"SIGMA_PHASE_INVARIANT_RELERR={sigma_rel:.15e}")
    print(f"DUAL_INTEGER_RADIUS_RELERR={radius_rel:.15e}")

    invariants_pass = max(phi_rel, sigma_rel, radius_rel) < 2.0e-12
    print("EXACT_INTEGER_AND_PHASE_INVARIANTS=" + ("PASS" if invariants_pass else "FAIL"))

    # Refine the search-selected h/R using the actual finite wall profile.
    x_floor_refine = (
        MIN_PAYLOAD_BOTTOM_OVER_WALL90
        * inputs.wall_width90
        / ((1.0 - PAYLOAD_RADIUS_OVER_H) * selected.radius)
    )
    x_low_refine = max(X_MIN, x_floor_refine)

    def full_c_objective(x_value):
        radius = selected.radius
        h_payload = float(x_value) * radius
        wall_out = wall_outward_simpson(profile, radius, h_payload)
        q_rim = 2.0 * math.pi * radius * selected.active_line
        envelope = RIM_ENVELOPE_MULTIPLIER * inputs.core_width
        inward_kernel = max(
            ring_kernel(radius + dr, dz, h_payload)
            for dr in (-envelope, 0.0, envelope)
            for dz in (-envelope, 0.0, envelope)
            if radius + dr > 0.0
        )
        rim_in = radius * q_rim * inward_kernel
        net = wall_out - rim_in
        energy_per_r = (
            math.pi * inputs.wall_tension * radius
            + 2.0 * math.pi * selected.E_line
        )
        if net <= 0.0:
            return 1.0e300
        return energy_per_r / (net * float(x_value) * float(x_value))

    refined = minimize_scalar(
        full_c_objective,
        bounds=(x_low_refine, X_MAX),
        method="bounded",
        options={"xatol": 1.0e-10},
    )

    if refined.success and float(refined.fun) < 1.0e299:
        selected.x = float(refined.x)

    primary = gravity(
        inputs,
        profile,
        selected,
        selected.x,
        rim_envelope_multiplier=RIM_ENVELOPE_MULTIPLIER,
    )

    severe = gravity(
        inputs,
        profile,
        selected,
        selected.x,
        rim_envelope_multiplier=SEVERE_RIM_ENVELOPE_MULTIPLIER,
    )

    print("\n=== COMPLETE FINITE-WALL / FINITE-RIM GRAVITY ===")
    thin_selected = gravity_fast(
        inputs,
        selected,
        selected.x,
        rim_envelope_multiplier=RIM_ENVELOPE_MULTIPLIER,
    )
    thin_full_force_relerr = abs(
        thin_selected["net_outward"] - primary["net_outward"]
    ) / max(abs(primary["net_outward"]), 1.0e-30)

    print(f"FINITE_WALL_OUTWARD_SIMPSON={primary['wall_outward']:+.15e}")
    print(f"FINITE_WALL_OUTWARD_GAUSS={primary['wall_outward_gauss']:+.15e}")
    print(f"FINITE_WALL_GRAVITY_RELERR={primary['wall_gravity_relerr']:.15e}")
    print(f"FINITE_RIM_INWARD_2CORE={primary['rim_inward']:+.15e}")
    print(f"FINITE_PAYLOAD_OUTWARD_2CORE={primary['net_outward']:+.15e}")
    print(f"TOTAL_ACTIVE_MASS_PER_R={primary['active_mass_per_r']:+.15e}")
    print(f"PROJECTED_C_EFF_COMPLETE_SOURCE={primary['projected_c']:.15e}")
    print(f"WALL_TAIL_INSIDE_PAYLOAD_FRACTION={primary['tail_fraction']:.15e}")
    print(f"FINITE_PAYLOAD_OUTWARD_3CORE_STRESS={severe['net_outward']:+.15e}")
    print(f"PROJECTED_C_3CORE_STRESS={severe['projected_c']:.15e}")
    print(f"THIN_SEARCH_VS_FULL_FORCE_RELERR={thin_full_force_relerr:.15e}")

    gravity_crosscheck_pass = (
        primary["wall_gravity_relerr"] < 2.0e-6
        and thin_full_force_relerr < 5.0e-3
    )
    gravity_sign_pass = (
        primary["net_outward"] > 0.0
        and severe["net_outward"] > 0.0
        and primary["active_mass_per_r"] > 0.0
        and primary["tail_fraction"] < 1.0e-10
    )

    print(
        "INDEPENDENT_FINITE_WALL_GRAVITY_RECONSTRUCTION="
        + ("PASS" if gravity_crosscheck_pass else "FAIL")
    )
    print("FINITE_PAYLOAD_REPULSION_COMPLETE_SOURCE=" + ("PASS" if gravity_sign_pass else "FAIL"))
    print("POSITIVE_TOTAL_ACTIVE_MASS=" + ("PASS" if primary["active_mass_per_r"] > 0.0 else "FAIL"))

    print("\n=== REPULSIVE PAYLOAD-HEIGHT BASIN ===")
    basin_lower, basin_upper = repulsive_basin_upper(inputs, profile, selected)
    basin_pass = math.isfinite(basin_upper) and basin_upper > basin_lower

    print(f"CLEARANCE_SAFE_H_OVER_R_LOWER={basin_lower:.15e}")
    print(f"ADVERSE_REPULSIVE_H_OVER_R_UPPER={basin_upper:.15e}")
    print(
        "ADVERSE_REPULSIVE_H_OVER_R_WIDTH="
        f"{(basin_upper - basin_lower) if basin_pass else math.nan:.15e}"
    )
    print("FINITE_REPULSIVE_OPERATING_BASIN=" + ("PASS" if basin_pass else "FAIL"))

    print("\n=== 3^4 SOURCE-LEDGER STRESS ===")
    stress_total = 0
    stress_pass = 0
    stress_min_force = math.inf
    stress_min_active_mass = math.inf
    stress_max_c = 0.0
    stress_max_abs_v = 0.0
    stress_min_lightcone_margin = math.inf

    for f_u, f_t, f_wall_t, f_wall_a in itertools.product(
        LEDGER_STRESS_LEVELS,
        repeat=4,
    ):
        stress_total += 1

        stress_candidates = search_candidates(
            inputs,
            profile,
            closures,
            U=inputs.U * f_u,
            T=inputs.T * f_t,
            J=inputs.J,
            wall_tension=inputs.wall_tension * f_wall_t,
            wall_active=inputs.wall_active * f_wall_a,
            optimize_gravity=False,
        )

        if not stress_candidates:
            continue

        best = stress_candidates[0]
        stress_pass += 1
        stress_min_force = min(stress_min_force, best.net_outward)
        stress_min_active_mass = min(stress_min_active_mass, best.active_mass_per_r)
        stress_max_c = max(stress_max_c, best.projected_c)
        stress_max_abs_v = max(stress_max_abs_v, abs(best.v))
        stress_min_lightcone_margin = min(
            stress_min_lightcone_margin,
            1.0 - abs(best.v),
        )

    stress_gate = stress_pass == stress_total

    print(f"SOURCE_LEDGER_STRESS_PASS={stress_pass}/{stress_total}")
    print(f"SOURCE_LEDGER_STRESS_MIN_OUTWARD={stress_min_force:+.15e}")
    print(f"SOURCE_LEDGER_STRESS_MIN_ACTIVE_MASS_PER_R={stress_min_active_mass:+.15e}")
    print(f"SOURCE_LEDGER_STRESS_MAX_PROJECTED_C={stress_max_c:.15e}")
    print(f"SOURCE_LEDGER_STRESS_MAX_ABS_V={stress_max_abs_v:.15e}")
    print(f"SOURCE_LEDGER_STRESS_MIN_LIGHTCONE_MARGIN={stress_min_lightcone_margin:.15e}")
    print("SOURCE_LEDGER_STRESS_ROBUSTNESS=" + ("PASS" if stress_gate else "FAIL"))

    print("\n=== ANGULAR MOMENTUM LEDGER ===")
    total_angular_momentum = 2.0 * math.pi * selected.radius**2 * selected.J_line
    angular_momentum_per_r2 = 2.0 * math.pi * selected.J_line

    print(f"TOTAL_ANGULAR_MOMENTUM_MODEL_UNITS={total_angular_momentum:+.15e}")
    print(f"ANGULAR_MOMENTUM_PER_R2={angular_momentum_per_r2:+.15e}")
    print("SOURCE_CLASSIFICATION=STATIONARY_NOT_STATIC")
    print("FRAME_DRAGGING_REQUIRED_LATER=YES")

    print("\n=== ENERGY SCALING — SOURCE LEVEL ONLY ===")
    improvement = VALIDATED_C / primary["projected_c"]
    projected_mass = VALIDATED_MASS_1G_1M / improvement
    projected_energy = VALIDATED_ENERGY_1G_1M / improvement

    print(f"CURRENT_VALIDATED_C={VALIDATED_C:.15e}")
    print(f"SOURCE_LEVEL_PROJECTED_C={primary['projected_c']:.15e}")
    print(f"SOURCE_LEVEL_PROJECTED_IMPROVEMENT_FACTOR={improvement:.15e}")
    print(f"SOURCE_LEVEL_PROJECTED_ONE_G_ONE_M_MASS_KG={projected_mass:.15e}")
    print(f"SOURCE_LEVEL_PROJECTED_ONE_G_ONE_M_ENERGY_J={projected_energy:.15e}")
    print("PROJECTED_C_STATUS=SOURCE_LEVEL_NOT_GLOBAL_018B_VALIDATED")

    print("\n=== BLIND WILDCARD HEIGHT DIAGNOSTIC — NOT EVIDENCE ===")
    for factor in WILDCARD_X_FACTORS:
        x_value = selected.x * factor

        if x_value <= 0.0 or x_value >= 1.0:
            print(f"WILDCARD_X_FACTOR={factor:.6f} STATUS=OUTSIDE_DOMAIN")
            continue

        result = gravity(
            inputs,
            profile,
            selected,
            x_value,
            rim_envelope_multiplier=RIM_ENVELOPE_MULTIPLIER,
        )

        print(
            f"WILDCARD_X_FACTOR={factor:.6f} "
            f"X={x_value:.9e} "
            f"F_OUT={result['net_outward']:+.9e} "
            f"OUTWARD={'YES' if result['net_outward'] > 0.0 else 'NO'}"
        )

    print("WILDCARD_VALUES_USED_AS_EVIDENCE=NO")

    overall = (
        wall_reconstruction_pass
        and invariants_pass
        and selected.balance_rel <= BALANCE_REL_TOL
        and abs(selected.v) <= MAX_ABS_V
        and selected.radius / inputs.wall_width90 >= MIN_R_OVER_WALL90
        and primary["payload_clearance"] >= MIN_PAYLOAD_BOTTOM_OVER_WALL90
        and gravity_crosscheck_pass
        and gravity_sign_pass
        and basin_pass
        and stress_gate
        and math.isfinite(primary["projected_c"])
    )

    print("\n=== DECISION ===")

    if overall:
        print("018B0H_COMPLETE_SOURCE_GRAVITY_REVALIDATION=GREEN")
        print("CORRECTED_EOS_EXACT_INTEGER_STATIONARITY=PASS")
        print("COMPLETE_MEASURED_LOCAL_JUNCTION_LEDGER=INCLUDED")
        print("FINITE_THICKNESS_WALL_GRAVITY=PASS")
        print("FINITE_RIM_CORE_ENVELOPE=PASS")
        print("FINITE_PAYLOAD_CM_REPULSION=PASS")
        print("POSITIVE_FAR_ACTIVE_MASS=PASS")
        print("SOURCE_LEVEL_ROBUSTNESS=PASS")
        print("TRUE_018B_GLOBAL_TOROIDAL_SOLVE=AUTHORIZED")
        print("NEXT=TRUE_018B_GLOBAL_TOROIDAL_EULER_LAGRANGE_SOLVE")
        print("NEXT_AFTER_TRUE_018B_GREEN=018B_INDEPENDENT_RECONSTRUCTION_THEN_018C_STABILITY")
    else:
        print("018B0H_COMPLETE_SOURCE_GRAVITY_REVALIDATION=RED")
        print("TRUE_018B_GLOBAL_TOROIDAL_SOLVE=NOT_AUTHORIZED_BY_THIS_GATE")
        print("NEXT=CLASSIFY_018B0H_FAILURE_BEFORE_GLOBAL_ESCALATION")

    print("CURRENT_HEURISTIC=APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY")
    print("HEURISTIC_INCREASE_FROM_THIS_GATE=NO_SOURCE_LEVEL_CLOSEOUT_ONLY")
    print("GLOBAL_TOROIDAL_FIELD_SOLUTION=NOT_YET_RUN")
    print("FULL_COMPOSITE_STABILITY=NOT_ESTABLISHED")
    print("FRAME_DRAGGING=NOT_INCLUDED")
    print("NONLINEAR_EINSTEIN_MATTER=NOT_ESTABLISHED")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018B0H_COMPLETE_CORRECTED_SOURCE_GRAVITY_REVALIDATION"
    )


if __name__ == "__main__":
    main()
