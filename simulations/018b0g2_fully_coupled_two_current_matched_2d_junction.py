#!/usr/bin/env python3
"""Simulation 018B-0G2 — fully coupled matched two-current KLS junction closeout.

PURPOSE
-------
Solve the new microscopic string-wall junction required after 018B-0D,
018B-0F0, and 018B-0F, using the literature-backed two-current string and the
new same-gauge nonthermal KLS wall in one local field theory.

SCIENTIFIC QUESTION
-------------------
Does the stationary two-current rim candidate survive replacement of the
source-level attachment by an actual fully coupled local two-dimensional
string-wall junction in which all mandatory local fields are allowed to relax?

This gate simultaneously relaxes, on a fine transverse patch,

    H vortex amplitude;
    neutral current-carrier Phi amplitude;
    neutral current-carrier Sigma amplitude;
    complex charge-one KLS wall field A;
    transverse U(1)_X gauge links.

The unit H-vortex phase is fixed only to select the required topological sector.
The current phase gradients (omega_i,k_i) are fixed state parameters, as in the
published straight-string BVP.

WHY A MULTISCALE MATCHED PATCH IS USED
--------------------------------------
018B-0F0 measured

    wall width90 ~ 78.55
    gauge-core scale ~ 3.16.

A uniform grid fine enough to resolve the string core while extending several
wall widths would waste most degrees of freedom in the outer planar wall.
Earlier 018A work demonstrated that this can produce severe common-mode lattice
artifacts.

Therefore this gate uses the already validated project strategy:

1. independently reconstruct the continuum radial two-current string BVP;
2. independently reconstruct the continuum planar KLS wall BVP;
3. impose those continuum solutions as outer matching data;
4. solve the fully coupled microscopic core on a fine local Cartesian patch;
5. solve the base string on the identical lattice;
6. subtract same-grid base relaxation and the analytically reconstructed
   truncated planar-wall contribution;
7. test resolution, patch-size, and matching-profile sensitivity.

This isolates the localized junction correction without pretending that a
small patch is the complete toroidal source.

LITERATURE / FIELD MODEL
------------------------
The two-current sector is the canonical representative reconstructed in
018B-0D from Lilley, Martin, and Peter, Phys. Rev. D 79, 103514 (2009).

With lambda_H = eta_H = 1, the transverse reduced potential is

    V_base = 1/8 (h^2-1)^2
           + 1/2 [w_phi + m_phi^2 + f_phi(h^2-1)] Phi^2
           + lambda_phi/4 Phi^4
           + 1/2 [w_sigma + m_sigma^2 + f_sigma(h^2-1)] Sigma^2
           + lambda_sigma/4 Sigma^4
           + g/2 Phi^2 Sigma^2,

where

    w_i = k_i^2 - omega_i^2.

The same-gauge KLS extension from 018B-0F0 is

    V_A = lambda_A/4 (|A|^2-F^2)^2
          - h_lock (H^* A^2 + H A^{*2})
          + c_H (|H|^2-1)
          + c_A (|A|^2-F^2)
          + V_0,

with

    c_H = h_lock F^2,
    c_A = 2 h_lock,
    V_0 = 2 h_lock F^2.

CHARGES / GAUGE LINKS
---------------------
Use the 018B-0F0 common-gauge embedding

    Q_H = 2,
    Q_A = 1,
    g_X = q_tilde/2.

A fundamental link angle a = g_X integral C.dl therefore appears as

    exp(-2 i a)

for H and

    exp(-i a)

for A.

The H vortex is represented as

    H = h(x,z) exp(i theta).

The charge-one A field has half winding asymptotically.  The outer matched
ansatz uses the principal half-angle and the independently solved planar wall
amplitude on the negative-x side.  The amplitude vanishes on the branch wall,
so the apparent half-angle branch cut is a continuous physical field.

LATTICE ENERGY
--------------
For lattice spacing dx, the transverse reduced action uses

    1/2 |D H|^2
    + 1/2 |grad Phi|^2
    + 1/2 |grad Sigma|^2
    + |D A|^2
    + 1/2 B^2
    + V_base
    + V_A.

The gauge plaquette energy is

    flux^2 / (2 g_X^2 dx^2),

where flux is the fundamental link-angle curl.

An analytic gradient is supplied for every released degree of freedom and is
checked independently by a directional finite difference before the science
cases run.

MATCHED JUNCTION OBSERVABLES
----------------------------
For each lattice case define

    mu_J,red = A_full - A_base - sigma_wall,trunc(L) L.

The subtraction removes:

- common square-lattice relaxation of the continuum string;
- the portion of the already-established planar wall lying inside the local
  patch.

Also measure

    Delta Sigma_phi   = integral(Phi_full^2 - Phi_base^2) d^2x,
    Delta Sigma_sigma = integral(Sigma_full^2 - Sigma_base^2) d^2x.

The physical straight-string eigenframe corrections follow from the standard
worldsheet reconstruction

    Delta U = mu_J,red
              + omega_phi^2 Delta Sigma_phi
              + omega_sigma^2 Delta Sigma_sigma,

    Delta T = mu_J,red
              - k_phi^2 Delta Sigma_phi
              - k_sigma^2 Delta Sigma_sigma,

    Delta J = -(omega_phi k_phi Delta Sigma_phi
                + omega_sigma k_sigma Delta Sigma_sigma).

These formulas are especially useful here because the wall/junction fields
have no explicit t or longitudinal dependence; their direct contribution is
Lorentz-invariant along the string, while changes to the two current-carrier
integrals account for the non-Nambu correction.

STATIONARY 018B-0F CROSSCHECK
-----------------------------
The selected 018B-0F boost and exact integer loop are NOT re-optimized here.
Instead, the corrected local eigenframe tensor is transformed into that same
stationary frame and used as a diagnostic:

    E' = gamma^2 (E + v^2 P - 2 v J),
    P' = gamma^2 (P + v^2 E - 2 v J),
    J' = gamma^2 [(1+v^2)J - v(E+P)],

with P=-T in the eigenframe.

This tests whether the actual local junction correction is small enough that
positive wall-supporting pressure and the finite-payload gravitational sign
survive before 018B-0H performs the exact integer/stationarity re-optimization.

GRAVITY DIAGNOSTIC
------------------
Reuse only the already-declared 018B-0F source-level axial kernel, replacing the
rim active line E'+P' by the junction-corrected value.  This is a diagnostic,
not a new validated coefficient.

The same adverse envelope is retained:

- shift the complete negative wall source two wall-width90 measures away from
  the payload;
- place the positive rim source at the most attractive point in a +/-2 core
  width cross-section envelope.

PRIMARY PASS CONDITIONS
-----------------------
Require all of the following:

- 94-test project regression baseline before execution;
- independent radial BVP reconstruction of U-T from carrier integrals;
- independent planar wall tension reconstruction;
- base and full analytic-gradient directional checks;
- released-field optimizer residuals below declared tolerances;
- matched junction correction converges under lattice resolution;
- matched correction remains controlled under patch-size continuation;
- corrected lab active line is stable under both convergence sequences;
- one-wall morphology survives;
- gauge-invariant relative phase locking survives;
- fundamental flux is one half-flux quantum for Q_H=2;
- both current condensates remain localized/nonzero;
- corrected stationary pressure remains positive;
- corrected source-level finite-payload force remains outward;
- corrected total active mass remains positive.

No threshold is allowed to rescue a failed field solution by modifying the
microscopic Lagrangian.

FALSIFICATION / STOP RULE
-------------------------
If the localized fully coupled junction is nonconvergent, destroys one-wall
termination, collapses either current condensate, produces an uncontrolled
EOS correction, or removes the source-level repulsive sign, do not proceed to
018B-0H or the global toroidal solve until that failure channel is classified.

If GREEN, the next gate is

    018B-0H complete source/gravity revalidation with the corrected local EOS,
    exact dual-integer stationarity re-solved, and the complete junction ledger.

Only after 018B-0H is GREEN should the project launch the true global 018B
finite-thickness toroidal Euler-Lagrange solve.

UNITS / APPROXIMATION LEVEL
---------------------------
All microscopic quantities are in the dimensionless natural-unit normalization
of 018B-0D/018B-0F0.

This is a flat-background local transverse Euler-Lagrange solve matched to a
straight string and planar wall.  Curvature is parametrically small because
018B-0F has R/core >> 1 and R/wall >> 1, but curvature is not solved here.

ENERGY CONDITIONS / CONSERVATION
--------------------------------
No energy condition is assumed as an input to force a desired answer.
Stationarity of the released lattice fields is tested by the norm of the exact
energy gradient.  Global curved-source covariant conservation is not claimed;
that belongs to true 018B.

LIMITATIONS
-----------
This file does NOT establish:

- a global toroidal microscopic field solution;
- complete curved-source T_munu;
- full loop stability;
- frame-dragging consistency;
- nonlinear Einstein-matter consistency;
- a validated replacement for the 018A-8 energy coefficient;
- practical energy scaling;
- experimental antigravity;
- a practical antigravity device;
- new physics or scientific discovery.

RELATED FILES
-------------
Upstream:
    simulations/018b0d_literature_two_current_counterflow_gate.py
    simulations/018b0f0_lilley_kls_same_gauge_normalization_wall_bridge.py
    simulations/018b0f_stationary_two_current_integer_wall_balance_gravity_scout.py
    results/logs/018b0g_two_current_fixed_background_2d_junction.log

Numerical-method precedent:
    simulations/018a6b1_matched_lattice_control_audit.py
    simulations/018a6b2_fine_local_multiscale_junction.py
    simulations/018a6b3_fine_continuation_outer_match_closeout.py

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018B0G2_FULLY_COUPLED_MATCHED_TWO_CURRENT_KLS_JUNCTION_CLOSEOUT
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from pathlib import Path
import re

import numpy as np
from scipy.integrate import simpson, solve_bvp
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parents[1]

D_LOG = ROOT / "results/logs/018b0d_literature_two_current_counterflow_gate.log"
F0_LOG = ROOT / "results/logs/018b0f0_lilley_kls_same_gauge_normalization_wall_bridge.log"
F_LOG = ROOT / "results/logs/018b0f_stationary_two_current_integer_wall_balance_gravity_scout.log"
G_LOG = ROOT / "results/logs/018b0g_two_current_fixed_background_2d_junction.log"
F_SOURCE = ROOT / "simulations/018b0f_stationary_two_current_integer_wall_balance_gravity_scout.py"

LAMBDA_H = 1.0
ETA_H = 1.0
Q_H = 2
Q_A = 1

LAMBDA_A = 1.0
F_A = 0.075
H_LOCK = 0.010

RADIAL_DOMAIN = 80.0
RADIAL_EPS = 1.0e-4
RADIAL_TOL = 2.0e-6

WALL_EXTENT = 10.0
WALL_TOL = 2.0e-8

GRADIENT_CHECK_TOL = 2.0e-5
GRADIENT_RMS_TOL = 2.0e-6
GRADIENT_MAX_TOL = 2.0e-5

# Matched local-junction convergence policies.  These are numerical promotion
# policies, not new physical laws.
MAX_RESOLUTION_MU_SPREAD = 0.025
MAX_PATCH_MU_SPREAD = 0.12
MAX_ACTIVE_LINE_SPREAD = 0.01
MAX_BLEND_ACTIVE_LINE_SPREAD = 0.01

MIN_PHASE_LOCK_COS = 0.97
MAX_WALL_CONTRAST = 0.20
MAX_FLUX_RELERR = 5.0e-6
MIN_CARRIER_RETAINED_FRACTION = 0.80

# Learn from the old 018A multiscale closeout: resolve the core rather than the
# full broad wall uniformly.
RESOLUTION_CASES = (
    (33, 12.0),
    (41, 12.0),
    (49, 12.0),
)

PATCH_CASES = (
    (33, 8.0),
    (41, 10.0),
    (49, 12.0),
)

SELECTED_CASE = (49, 12.0)

# Low-cost outer-match sensitivity.  The physical result should not depend on
# an arbitrary interpolation width used only to seed/match the local patch.
BLEND_FACTORS = (1.5, 2.0, 3.0)
BLEND_CASE = (33, 8.0)

DEFAULT_BLEND_FACTOR = 2.0

MAXITER_BASE = 1000
MAXITER_FULL = 1500

CORE_ENVELOPE_MULTIPLIER = 2.0
WALL_ADVERSE_SHIFT_WIDTHS = 2.0

CURRENT_HEURISTIC = "APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY"


def read_scalar(path: Path, label: str) -> float:
    """Read one finite scalar following an exact label."""

    text = path.read_text(errors="replace")
    number = r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
    match = re.search(re.escape(label) + number, text)

    if match is None:
        raise RuntimeError(f"Missing {label!r} in {path}")

    value = float(match.group(1))

    if not math.isfinite(value):
        raise RuntimeError(f"Nonfinite {label!r} in {path}")

    return value


def require_marker(path: Path, marker: str) -> None:
    """Require an upstream scientific gate before inheriting its outputs."""

    if not path.exists():
        raise RuntimeError(f"Missing upstream log: {path}")

    text = path.read_text(errors="replace")

    if marker not in text:
        raise RuntimeError(f"Missing upstream marker {marker!r} in {path}")


@dataclass(frozen=True)
class Parameters:
    """Canonical two-current and same-gauge KLS parameters."""

    lambda_phi: float
    lambda_sigma: float
    m_phi_sq: float
    m_sigma_sq: float
    f_phi: float
    f_sigma: float
    g_cross: float
    q_tilde_sq: float
    q_tilde: float
    g_x: float

    omega_phi: float
    k_phi: float
    omega_sigma: float
    k_sigma: float

    w_phi: float
    w_sigma: float

    U0: float
    T0: float

    wall_tension: float
    wall_active: float
    wall_width90: float
    core_width: float

    boost_v: float
    loop_radius: float
    h_over_r: float


@dataclass
class ContinuumData:
    """Independently reconstructed radial string and planar wall solutions."""

    radial: object
    wall: object
    wall_half_domain: float

    sigma_phi: float
    sigma_sigma: float
    radial_ut_reconstructed: float
    radial_ut_relerr: float

    wall_tension_reconstructed: float
    wall_tension_relerr: float


@dataclass
class LatticeProblem:
    """One base or fully coupled local Cartesian patch."""

    n: int
    box_half: float
    dx: float
    full: bool
    blend_factor: float

    x: np.ndarray
    z: np.ndarray
    X: np.ndarray
    Z: np.ndarray
    radius: np.ndarray
    phase: np.ndarray
    weights: np.ndarray

    h0: np.ndarray
    phi0: np.ndarray
    sigma0: np.ndarray
    a0: np.ndarray
    ax0: np.ndarray
    az0: np.ndarray

    h_free: np.ndarray
    phi_free: np.ndarray
    sigma_free: np.ndarray
    a_free: np.ndarray
    ax_free: np.ndarray
    az_free: np.ndarray


@dataclass
class LatticeResult:
    """Optimizer output and physical fields for one patch case."""

    problem: LatticeProblem
    energy: float
    gradient_rms: float
    gradient_max: float
    iterations: int
    optimizer_success: bool

    h: np.ndarray
    phi: np.ndarray
    sigma: np.ndarray
    a: np.ndarray
    ax: np.ndarray
    az: np.ndarray

    sigma_phi: float
    sigma_sigma: float


@dataclass
class MatchedResult:
    """Same-grid localized junction correction and corrected worldsheet data."""

    n: int
    box_half: float
    dx: float
    blend_factor: float

    mu_reduced: float
    delta_sigma_phi: float
    delta_sigma_sigma: float

    delta_U: float
    delta_T: float
    delta_J: float

    U: float
    T: float
    J: float

    lab_E: float
    lab_P: float
    lab_J: float
    lab_active: float

    base: LatticeResult
    full: LatticeResult


def load_parameters() -> Parameters:
    """Load all inherited quantities from GREEN upstream gates."""

    require_marker(D_LOG, "018B0D_TWO_CURRENT_COUNTERFLOW_GATE=GREEN")
    require_marker(F0_LOG, "018B0F0_LILLEY_KLS_NORMALIZATION_WALL_BRIDGE=GREEN")
    require_marker(F_LOG, "018B0F_STATIONARY_INTEGER_WALL_BALANCE_GRAVITY_SCOUT=GREEN")
    require_marker(G_LOG, "018B0G_TWO_CURRENT_FIXED_BACKGROUND_2D_JUNCTION_GATE=GREEN")

    q_tilde_sq = read_scalar(F0_LOG, "QTILDE_SQ=")
    q_tilde = math.sqrt(q_tilde_sq)

    omega_phi = read_scalar(D_LOG, "OMEGA_PHI=")
    k_phi = read_scalar(D_LOG, "K_PHI=")
    omega_sigma = read_scalar(D_LOG, "OMEGA_SIGMA=")
    k_sigma = read_scalar(D_LOG, "K_SIGMA=")

    return Parameters(
        lambda_phi=read_scalar(F0_LOG, "LAMBDA_PHI="),
        lambda_sigma=read_scalar(F0_LOG, "LAMBDA_SIGMA="),
        m_phi_sq=read_scalar(F0_LOG, "M_PHI_SQ="),
        m_sigma_sq=read_scalar(F0_LOG, "M_SIGMA_SQ="),
        f_phi=read_scalar(F0_LOG, "F_PHI="),
        f_sigma=read_scalar(F0_LOG, "F_SIGMA="),
        g_cross=read_scalar(F0_LOG, "G="),
        q_tilde_sq=q_tilde_sq,
        q_tilde=q_tilde,
        g_x=q_tilde / 2.0,
        omega_phi=omega_phi,
        k_phi=k_phi,
        omega_sigma=omega_sigma,
        k_sigma=k_sigma,
        w_phi=k_phi * k_phi - omega_phi * omega_phi,
        w_sigma=k_sigma * k_sigma - omega_sigma * omega_sigma,
        U0=read_scalar(D_LOG, "ENERGY_PER_LENGTH_U="),
        T0=read_scalar(D_LOG, "TENSION_T="),
        wall_tension=read_scalar(F0_LOG, "NEW_WALL_TENSION="),
        wall_active=read_scalar(F0_LOG, "NEW_WALL_ACTIVE_SOURCE="),
        wall_width90=read_scalar(F0_LOG, "NEW_WALL_WIDTH90="),
        core_width=read_scalar(F0_LOG, "NEW_STRING_GAUGE_CORE_INVERSE_MASS_PROXY="),
        boost_v=read_scalar(F_LOG, "BOOST_V="),
        loop_radius=read_scalar(F_LOG, "RADIUS="),
        h_over_r=read_scalar(F_LOG, "SELECTED_H_OVER_R="),
    )


def solve_radial_string(p: Parameters):
    """Independently reconstruct the published two-current straight-string BVP."""

    r = np.linspace(RADIAL_EPS, RADIAL_DOMAIN, 1200)

    h_guess = np.tanh(r)
    q_guess = np.exp(-0.2 * r * r)
    phi_guess = 0.38 * np.exp(-0.12 * r)
    sigma_guess = 0.326 * np.exp(-0.125 * r)

    initial = np.vstack(
        (
            h_guess,
            np.gradient(h_guess, r),
            q_guess,
            np.gradient(q_guess, r),
            phi_guess,
            np.gradient(phi_guess, r),
            sigma_guess,
            np.gradient(sigma_guess, r),
        )
    )

    def ode(rr, y):
        h, hp, Q, Qp, phi, phip, sigma, sigmap = y
        inv_r = 1.0 / rr

        return np.vstack(
            (
                hp,
                (
                    Q * Q / (rr * rr)
                    + 0.5 * LAMBDA_H * (h * h - 1.0)
                    + p.f_phi * phi * phi
                    + p.f_sigma * sigma * sigma
                )
                * h
                - hp * inv_r,
                Qp,
                p.q_tilde_sq * h * h * Q + Qp * inv_r,
                phip,
                (
                    p.w_phi
                    + p.f_phi * (h * h - 1.0)
                    + p.m_phi_sq
                    + p.lambda_phi * phi * phi
                    + p.g_cross * sigma * sigma
                )
                * phi
                - phip * inv_r,
                sigmap,
                (
                    p.w_sigma
                    + p.f_sigma * (h * h - 1.0)
                    + p.m_sigma_sq
                    + p.lambda_sigma * sigma * sigma
                    + p.g_cross * phi * phi
                )
                * sigma
                - sigmap * inv_r,
            )
        )

    def bc(ya, yb):
        return np.array(
            (
                ya[0],
                ya[2] - 1.0,
                ya[5],
                ya[7],
                yb[0] - 1.0,
                yb[2],
                yb[4],
                yb[6],
            ),
            dtype=float,
        )

    solution = solve_bvp(
        ode,
        bc,
        r,
        initial,
        tol=RADIAL_TOL,
        max_nodes=30000,
    )

    if solution.status != 0:
        raise RuntimeError(f"Radial two-current BVP failed: {solution.message}")

    return solution


def wall_potential(H, A):
    """Return the 018B-0F0 zero-carrier planar-wall potential."""

    c_h = H_LOCK * F_A * F_A
    c_a = 2.0 * H_LOCK
    constant = 2.0 * H_LOCK * F_A * F_A

    return (
        LAMBDA_H / 8.0 * (H * H - 1.0) ** 2
        + LAMBDA_A / 4.0 * (A * A - F_A * F_A) ** 2
        - 2.0 * H_LOCK * H * A * A
        + c_h * (H * H - 1.0)
        + c_a * (A * A - F_A * F_A)
        + constant
    )


def solve_planar_wall():
    """Independently reconstruct the full H-A planar wall profile."""

    k_trial = F_A * math.sqrt(LAMBDA_A) / 2.0
    half_domain = WALL_EXTENT / k_trial

    z = np.linspace(0.0, half_domain, 500)

    c_h = H_LOCK * F_A * F_A
    c_a = 2.0 * H_LOCK

    def ode(_z, y):
        H, Hp, A, Ap = y

        Hpp = (
            0.5 * LAMBDA_H * H * (H * H - 1.0)
            - 2.0 * H_LOCK * A * A
            + 2.0 * c_h * H
        )

        # A has |dA|^2 normalization, so 2 A'' = dV/dA.
        App = (
            0.5 * LAMBDA_A * A * (A * A - F_A * F_A)
            - 2.0 * H_LOCK * H * A
            + c_a * A
        )

        return np.vstack((Hp, Hpp, Ap, App))

    def bc(ya, yb):
        return np.array((ya[1], ya[2], yb[0] - 1.0, yb[2] - F_A))

    A0 = F_A * np.tanh(k_trial * z)

    initial = np.vstack(
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
        initial,
        tol=WALL_TOL,
        max_nodes=30000,
    )

    if solution.status != 0:
        raise RuntimeError(f"Planar wall BVP failed: {solution.message}")

    return solution, half_domain


def reconstruct_continuum(p: Parameters) -> ContinuumData:
    """Cross-check both upstream microscopic components independently."""

    radial = solve_radial_string(p)
    wall, wall_half_domain = solve_planar_wall()

    r = np.linspace(RADIAL_EPS, RADIAL_DOMAIN, 24001)
    radial_values = radial.sol(r)

    sigma_phi = 2.0 * math.pi * float(
        simpson(r * radial_values[4] ** 2, x=r)
    )

    sigma_sigma = 2.0 * math.pi * float(
        simpson(r * radial_values[6] ** 2, x=r)
    )

    radial_ut = (
        (p.omega_phi * p.omega_phi + p.k_phi * p.k_phi) * sigma_phi
        + (p.omega_sigma * p.omega_sigma + p.k_sigma * p.k_sigma)
        * sigma_sigma
    )

    expected_ut = p.U0 - p.T0

    radial_ut_relerr = abs(radial_ut - expected_ut) / max(
        abs(expected_ut), 1.0e-30
    )

    z = np.linspace(0.0, wall_half_domain, 16001)
    H, Hp, A, Ap = wall.sol(z)

    density = 0.5 * Hp * Hp + Ap * Ap + wall_potential(H, A)

    wall_tension_reconstructed = 2.0 * float(simpson(density, x=z))

    wall_tension_relerr = abs(
        wall_tension_reconstructed - p.wall_tension
    ) / p.wall_tension

    return ContinuumData(
        radial=radial,
        wall=wall,
        wall_half_domain=wall_half_domain,
        sigma_phi=sigma_phi,
        sigma_sigma=sigma_sigma,
        radial_ut_reconstructed=radial_ut,
        radial_ut_relerr=radial_ut_relerr,
        wall_tension_reconstructed=wall_tension_reconstructed,
        wall_tension_relerr=wall_tension_relerr,
    )


def planar_wall_values(data: ContinuumData, z):
    """Return even H and nonnegative wall amplitude at arbitrary signed z."""

    absolute = np.minimum(np.abs(z), data.wall_half_domain)
    values = data.wall.sol(absolute)
    return values[0], values[2]


def truncated_wall_tension(data: ContinuumData, box_half: float) -> float:
    """Return the portion of planar wall tension contained in |z|<=box_half."""

    z = np.linspace(0.0, box_half, 5001)
    H, Hp, A, Ap = data.wall.sol(z)
    density = 0.5 * Hp * Hp + Ap * Ap + wall_potential(H, A)
    return 2.0 * float(simpson(density, x=z))


def radial_values(data: ContinuumData, radius):
    """Interpolate continuum radial profiles on arbitrary nonnegative radii."""

    clipped = np.clip(radius, RADIAL_EPS, RADIAL_DOMAIN)
    values = data.radial.sol(clipped)
    return values[0], values[2], values[4], values[6]


def build_problem(
    p: Parameters,
    data: ContinuumData,
    n: int,
    box_half: float,
    *,
    full: bool,
    blend_factor: float = DEFAULT_BLEND_FACTOR,
) -> LatticeProblem:
    """Build one base/full matched Cartesian patch with continuum outer data."""

    x = np.linspace(-box_half, box_half, n)
    z = np.linspace(-box_half, box_half, n)
    dx = float(x[1] - x[0])

    X, Z = np.meshgrid(x, z, indexing="ij")
    radius = np.hypot(X, Z)
    theta = np.arctan2(Z, X)
    phase = np.exp(1.0j * theta)
    phase[radius < 1.0e-14] = 1.0 + 0.0j

    h_radial, _Q_node, phi_radial, sigma_radial = radial_values(
        data, np.maximum(radius, RADIAL_EPS)
    )

    # Fundamental gauge link a = g_X integral C.dl.  With Q_H=2 and the
    # published vortex gauge function Q(r), g_X/q_tilde=1/2.
    x_mid = 0.5 * (x[:-1, None] + x[1:, None])
    z_on_x = np.broadcast_to(z[None, :], (n - 1, n))
    r_mid_x = np.hypot(x_mid, z_on_x)
    Q_mid_x = radial_values(data, np.maximum(r_mid_x, RADIAL_EPS))[1]

    ax0 = (
        0.5
        * (Q_mid_x - 1.0)
        * (-z_on_x / np.maximum(r_mid_x * r_mid_x, 1.0e-14))
        * dx
    )

    x_on_z = np.broadcast_to(x[:, None], (n, n - 1))
    z_mid = 0.5 * (z[None, :-1] + z[None, 1:])
    r_mid_z = np.hypot(x_on_z, z_mid)
    Q_mid_z = radial_values(data, np.maximum(r_mid_z, RADIAL_EPS))[1]

    az0 = (
        0.5
        * (Q_mid_z - 1.0)
        * (x_on_z / np.maximum(r_mid_z * r_mid_z, 1.0e-14))
        * dx
    )

    h0 = h_radial.copy()
    phi0 = phi_radial.copy()
    sigma0 = sigma_radial.copy()

    a0 = np.zeros((n, n), dtype=complex)

    if full:
        H_wall, A_wall_abs = planar_wall_values(data, Z)

        # Smoothly join the negative-x planar wall to the positive-x vacuum.
        # This width is an outer-matching/initialization convention only and is
        # varied independently below.
        blend_width = blend_factor * p.core_width
        blend = 0.5 * (1.0 - np.tanh(X / blend_width))

        h0 = h_radial + blend * (H_wall - 1.0)

        amplitude = F_A + blend * (A_wall_abs - F_A)
        a0 = amplitude * np.exp(0.5j * theta)

    center = (n // 2, n // 2)
    h0[center] = 0.0
    a0[center] = 0.0 + 0.0j

    weights = np.ones((n, n), dtype=float)
    weights[[0, -1], :] *= 0.5
    weights[:, [0, -1]] *= 0.5

    node_free = np.zeros((n, n), dtype=bool)
    node_free[1:-1, 1:-1] = True

    h_free = node_free.copy()
    h_free[center] = False

    phi_free = node_free.copy()
    sigma_free = node_free.copy()

    a_free = node_free.copy() if full else np.zeros_like(node_free)

    # Keep one outer layer of gauge links fixed to the continuum radial field.
    ax_free = np.zeros((n - 1, n), dtype=bool)
    ax_free[1:-1, 1:-1] = True

    az_free = np.zeros((n, n - 1), dtype=bool)
    az_free[1:-1, 1:-1] = True

    return LatticeProblem(
        n=n,
        box_half=box_half,
        dx=dx,
        full=full,
        blend_factor=blend_factor,
        x=x,
        z=z,
        X=X,
        Z=Z,
        radius=radius,
        phase=phase,
        weights=weights,
        h0=h0,
        phi0=phi0,
        sigma0=sigma0,
        a0=a0,
        ax0=ax0,
        az0=az0,
        h_free=h_free,
        phi_free=phi_free,
        sigma_free=sigma_free,
        a_free=a_free,
        ax_free=ax_free,
        az_free=az_free,
    )


def pack(problem: LatticeProblem) -> np.ndarray:
    """Pack released fields in one deterministic optimizer ordering."""

    parts = [
        problem.h0[problem.h_free],
        problem.phi0[problem.phi_free],
        problem.sigma0[problem.sigma_free],
    ]

    if problem.full:
        a_values = problem.a0[problem.a_free]
        parts.extend((a_values.real, a_values.imag))

    parts.extend(
        (
            problem.ax0[problem.ax_free],
            problem.az0[problem.az_free],
        )
    )

    return np.concatenate(parts)


def unpack(problem: LatticeProblem, vector: np.ndarray):
    """Restore released optimizer variables to complete field arrays."""

    h = problem.h0.copy()
    phi = problem.phi0.copy()
    sigma = problem.sigma0.copy()
    a = problem.a0.copy()
    ax = problem.ax0.copy()
    az = problem.az0.copy()

    offset = 0

    for array, mask in (
        (h, problem.h_free),
        (phi, problem.phi_free),
        (sigma, problem.sigma_free),
    ):
        count = int(np.count_nonzero(mask))
        array[mask] = vector[offset : offset + count]
        offset += count

    if problem.full:
        count = int(np.count_nonzero(problem.a_free))
        real = vector[offset : offset + count]
        offset += count
        imag = vector[offset : offset + count]
        offset += count
        a[problem.a_free] = real + 1.0j * imag

    count = int(np.count_nonzero(problem.ax_free))
    ax[problem.ax_free] = vector[offset : offset + count]
    offset += count

    count = int(np.count_nonzero(problem.az_free))
    az[problem.az_free] = vector[offset : offset + count]
    offset += count

    if offset != vector.size:
        raise RuntimeError("Optimizer pack/unpack size mismatch")

    return h, phi, sigma, a, ax, az


def optimizer_bounds(problem: LatticeProblem):
    """Return conservative field bounds; they are not fitted physics values."""

    bounds = []

    bounds.extend([(0.0, 1.5)] * int(np.count_nonzero(problem.h_free)))
    bounds.extend([(0.0, 1.0)] * int(np.count_nonzero(problem.phi_free)))
    bounds.extend([(0.0, 1.0)] * int(np.count_nonzero(problem.sigma_free)))

    if problem.full:
        count_a = int(np.count_nonzero(problem.a_free))
        bounds.extend([(-0.20, 0.20)] * count_a)
        bounds.extend([(-0.20, 0.20)] * count_a)

    bounds.extend([(-0.5, 0.5)] * int(np.count_nonzero(problem.ax_free)))
    bounds.extend([(-0.5, 0.5)] * int(np.count_nonzero(problem.az_free)))

    return bounds


def energy_and_gradient(
    p: Parameters,
    problem: LatticeProblem,
    vector: np.ndarray,
):
    """Return complete reduced lattice energy and exact analytic gradient."""

    h, phi, sigma, a, ax, az = unpack(problem, vector)

    H = h * problem.phase
    dx = problem.dx

    g_h = np.zeros_like(h)
    g_phi = np.zeros_like(phi)
    g_sigma = np.zeros_like(sigma)
    g_a = np.zeros_like(a, dtype=complex)
    g_ax = np.zeros_like(ax)
    g_az = np.zeros_like(az)

    g_H = np.zeros_like(H, dtype=complex)

    energy = 0.0

    # ------------------------------------------------------------------
    # Charge-two H covariant links: 1/2 |D H|^2.
    # ------------------------------------------------------------------

    u_hx = np.exp(-2.0j * ax)
    d_hx = H[1:, :] - u_hx * H[:-1, :]
    energy += 0.5 * float(np.sum(np.abs(d_hx) ** 2))

    g_H[1:, :] += d_hx
    g_H[:-1, :] -= np.conj(u_hx) * d_hx
    g_ax += -2.0 * np.imag(np.conj(d_hx) * u_hx * H[:-1, :])

    u_hz = np.exp(-2.0j * az)
    d_hz = H[:, 1:] - u_hz * H[:, :-1]
    energy += 0.5 * float(np.sum(np.abs(d_hz) ** 2))

    g_H[:, 1:] += d_hz
    g_H[:, :-1] -= np.conj(u_hz) * d_hz
    g_az += -2.0 * np.imag(np.conj(d_hz) * u_hz * H[:, :-1])

    g_h += np.real(np.conj(problem.phase) * g_H)

    # ------------------------------------------------------------------
    # Neutral carrier gradients: 1/2 |grad carrier|^2.
    # ------------------------------------------------------------------

    for field, gradient in ((phi, g_phi), (sigma, g_sigma)):
        delta = field[1:, :] - field[:-1, :]
        energy += 0.5 * float(np.sum(delta * delta))
        gradient[1:, :] += delta
        gradient[:-1, :] -= delta

        delta = field[:, 1:] - field[:, :-1]
        energy += 0.5 * float(np.sum(delta * delta))
        gradient[:, 1:] += delta
        gradient[:, :-1] -= delta

    # ------------------------------------------------------------------
    # Charge-one A covariant links: |D A|^2.
    # ------------------------------------------------------------------

    if problem.full:
        u_ax = np.exp(-1.0j * ax)
        d_ax = a[1:, :] - u_ax * a[:-1, :]
        energy += float(np.sum(np.abs(d_ax) ** 2))

        g_a[1:, :] += 2.0 * d_ax
        g_a[:-1, :] -= 2.0 * np.conj(u_ax) * d_ax
        g_ax += -2.0 * np.imag(np.conj(d_ax) * u_ax * a[:-1, :])

        u_az = np.exp(-1.0j * az)
        d_az = a[:, 1:] - u_az * a[:, :-1]
        energy += float(np.sum(np.abs(d_az) ** 2))

        g_a[:, 1:] += 2.0 * d_az
        g_a[:, :-1] -= 2.0 * np.conj(u_az) * d_az
        g_az += -2.0 * np.imag(np.conj(d_az) * u_az * a[:, :-1])

    # ------------------------------------------------------------------
    # Noncompact gauge plaquettes: 1/2 B^2.
    # ------------------------------------------------------------------

    flux = (
        ax[:, :-1]
        + az[1:, :]
        - ax[:, 1:]
        - az[:-1, :]
    )

    gauge_coefficient = 1.0 / (p.g_x * p.g_x * dx * dx)

    energy += 0.5 * gauge_coefficient * float(np.sum(flux * flux))

    g_flux = gauge_coefficient * flux

    g_ax[:, :-1] += g_flux
    g_az[1:, :] += g_flux
    g_ax[:, 1:] -= g_flux
    g_az[:-1, :] -= g_flux

    # ------------------------------------------------------------------
    # Node potentials.
    # ------------------------------------------------------------------

    h2 = h * h
    phi2 = phi * phi
    sigma2 = sigma * sigma

    a_phi = p.w_phi + p.m_phi_sq + p.f_phi * (h2 - 1.0)
    a_sigma = p.w_sigma + p.m_sigma_sq + p.f_sigma * (h2 - 1.0)

    potential = (
        LAMBDA_H / 8.0 * (h2 - 1.0) ** 2
        + 0.5 * a_phi * phi2
        + p.lambda_phi / 4.0 * phi2 * phi2
        + 0.5 * a_sigma * sigma2
        + p.lambda_sigma / 4.0 * sigma2 * sigma2
        + p.g_cross / 2.0 * phi2 * sigma2
    )

    g_h_potential = (
        0.5 * LAMBDA_H * h * (h2 - 1.0)
        + p.f_phi * h * phi2
        + p.f_sigma * h * sigma2
    )

    g_phi_potential = (
        p.w_phi
        + p.m_phi_sq
        + p.f_phi * (h2 - 1.0)
        + p.lambda_phi * phi2
        + p.g_cross * sigma2
    ) * phi

    g_sigma_potential = (
        p.w_sigma
        + p.m_sigma_sq
        + p.f_sigma * (h2 - 1.0)
        + p.lambda_sigma * sigma2
        + p.g_cross * phi2
    ) * sigma

    if problem.full:
        amplitude_sq = np.abs(a) ** 2

        c_h = H_LOCK * F_A * F_A
        c_a = 2.0 * H_LOCK
        constant = 2.0 * H_LOCK * F_A * F_A

        trilinear = (
            H_LOCK
            * (
                np.conj(H) * a * a
                + H * np.conj(a) * np.conj(a)
            )
        ).real

        potential += (
            LAMBDA_A / 4.0 * (amplitude_sq - F_A * F_A) ** 2
            - trilinear
            + c_h * (h2 - 1.0)
            + c_a * (amplitude_sq - F_A * F_A)
            + constant
        )

        g_h_potential += (
            -2.0 * H_LOCK * np.real(np.conj(problem.phase) * a * a)
            + 2.0 * c_h * h
        )

        g_a_potential = (
            LAMBDA_A * (amplitude_sq - F_A * F_A) * a
            + 2.0 * c_a * a
            - 4.0 * H_LOCK * H * np.conj(a)
        )

        g_a += dx * dx * problem.weights * g_a_potential

    node_weight = dx * dx * problem.weights

    energy += float(np.sum(node_weight * potential))

    g_h += node_weight * g_h_potential
    g_phi += node_weight * g_phi_potential
    g_sigma += node_weight * g_sigma_potential

    # ------------------------------------------------------------------
    # Pack exact gradient in the same ordering as pack().
    # ------------------------------------------------------------------

    pieces = [
        g_h[problem.h_free],
        g_phi[problem.phi_free],
        g_sigma[problem.sigma_free],
    ]

    if problem.full:
        a_gradient = g_a[problem.a_free]
        pieces.extend((a_gradient.real, a_gradient.imag))

    pieces.extend(
        (
            g_ax[problem.ax_free],
            g_az[problem.az_free],
        )
    )

    return float(energy), np.concatenate(pieces)


def directional_gradient_check(
    p: Parameters,
    problem: LatticeProblem,
    seed: int,
) -> float:
    """Check analytic gradient against an independent centered difference."""

    vector = pack(problem)
    _, gradient = energy_and_gradient(p, problem, vector)

    rng = np.random.default_rng(seed)
    direction = rng.normal(size=vector.size)
    direction /= np.linalg.norm(direction)

    epsilon = 5.0e-7

    plus, _ = energy_and_gradient(
        p, problem, vector + epsilon * direction
    )

    minus, _ = energy_and_gradient(
        p, problem, vector - epsilon * direction
    )

    finite_difference = (plus - minus) / (2.0 * epsilon)
    analytic = float(np.dot(gradient, direction))

    return abs(finite_difference - analytic) / max(
        abs(finite_difference), abs(analytic), 1.0e-14
    )


def solve_lattice(
    p: Parameters,
    problem: LatticeProblem,
) -> LatticeResult:
    """Relax one base/full patch and return exact residual diagnostics."""

    initial = pack(problem)

    maxiter = MAXITER_FULL if problem.full else MAXITER_BASE

    result = minimize(
        lambda vector: energy_and_gradient(p, problem, vector),
        initial,
        method="L-BFGS-B",
        jac=True,
        bounds=optimizer_bounds(problem),
        options={
            "maxiter": maxiter,
            "ftol": 1.0e-13,
            "gtol": 1.0e-8,
            "maxls": 50,
            "maxcor": 20,
        },
    )

    energy, gradient = energy_and_gradient(p, problem, result.x)

    gradient_rms = float(np.linalg.norm(gradient) / math.sqrt(gradient.size))
    gradient_max = float(np.max(np.abs(gradient)))

    h, phi, sigma, a, ax, az = unpack(problem, result.x)

    sigma_phi = problem.dx * problem.dx * float(
        np.sum(problem.weights * phi * phi)
    )

    sigma_sigma = problem.dx * problem.dx * float(
        np.sum(problem.weights * sigma * sigma)
    )

    return LatticeResult(
        problem=problem,
        energy=energy,
        gradient_rms=gradient_rms,
        gradient_max=gradient_max,
        iterations=int(result.nit),
        optimizer_success=bool(result.success),
        h=h,
        phi=phi,
        sigma=sigma,
        a=a,
        ax=ax,
        az=az,
        sigma_phi=sigma_phi,
        sigma_sigma=sigma_sigma,
    )


def transform_worldsheet(
    U: float,
    T: float,
    J: float,
    v: float,
):
    """Lorentz-transform a general 1+1 symmetric worldsheet stress tensor."""

    gamma = 1.0 / math.sqrt(1.0 - v * v)
    gamma2 = gamma * gamma

    P = -T

    E_lab = gamma2 * (U + v * v * P - 2.0 * v * J)
    P_lab = gamma2 * (P + v * v * U - 2.0 * v * J)
    J_lab = gamma2 * ((1.0 + v * v) * J - v * (U + P))

    return E_lab, P_lab, J_lab


def matched_result(
    p: Parameters,
    data: ContinuumData,
    base: LatticeResult,
    full: LatticeResult,
) -> MatchedResult:
    """Construct the same-grid localized junction and corrected EOS data."""

    if (
        base.problem.n != full.problem.n
        or base.problem.box_half != full.problem.box_half
    ):
        raise RuntimeError("Base/full matched grids differ")

    L = full.problem.box_half

    wall_inside = truncated_wall_tension(data, L) * L

    mu_reduced = full.energy - base.energy - wall_inside

    delta_sigma_phi = full.sigma_phi - base.sigma_phi
    delta_sigma_sigma = full.sigma_sigma - base.sigma_sigma

    delta_U = (
        mu_reduced
        + p.omega_phi * p.omega_phi * delta_sigma_phi
        + p.omega_sigma * p.omega_sigma * delta_sigma_sigma
    )

    delta_T = (
        mu_reduced
        - p.k_phi * p.k_phi * delta_sigma_phi
        - p.k_sigma * p.k_sigma * delta_sigma_sigma
    )

    delta_J = -(
        p.omega_phi * p.k_phi * delta_sigma_phi
        + p.omega_sigma * p.k_sigma * delta_sigma_sigma
    )

    U = p.U0 + delta_U
    T = p.T0 + delta_T
    J = delta_J

    lab_E, lab_P, lab_J = transform_worldsheet(U, T, J, p.boost_v)

    return MatchedResult(
        n=full.problem.n,
        box_half=L,
        dx=full.problem.dx,
        blend_factor=full.problem.blend_factor,
        mu_reduced=mu_reduced,
        delta_sigma_phi=delta_sigma_phi,
        delta_sigma_sigma=delta_sigma_sigma,
        delta_U=delta_U,
        delta_T=delta_T,
        delta_J=delta_J,
        U=U,
        T=T,
        J=J,
        lab_E=lab_E,
        lab_P=lab_P,
        lab_J=lab_J,
        lab_active=lab_E + lab_P,
        base=base,
        full=full,
    )


def run_case(
    p: Parameters,
    data: ContinuumData,
    n: int,
    box_half: float,
    *,
    blend_factor: float = DEFAULT_BLEND_FACTOR,
) -> MatchedResult:
    """Solve matched base/full problems for one numerical case."""

    base_problem = build_problem(
        p,
        data,
        n,
        box_half,
        full=False,
        blend_factor=blend_factor,
    )

    full_problem = build_problem(
        p,
        data,
        n,
        box_half,
        full=True,
        blend_factor=blend_factor,
    )

    base = solve_lattice(p, base_problem)
    full = solve_lattice(p, full_problem)

    return matched_result(p, data, base, full)


def relative_spread(values) -> float:
    """Return max-min divided by the median absolute scale."""

    array = np.asarray(values, dtype=float)
    denominator = max(abs(float(np.median(array))), 1.0e-30)
    return float((np.max(array) - np.min(array)) / denominator)


def topology_metrics(p: Parameters, result: MatchedResult):
    """Measure one-wall morphology, phase locking, flux, and carrier survival."""

    problem = result.full.problem
    full = result.full
    base = result.base

    x = problem.x
    z = problem.z

    j0 = int(np.argmin(np.abs(z)))

    sample = 2.5 * p.core_width
    i_negative = int(np.argmin(np.abs(x + sample)))
    i_positive = int(np.argmin(np.abs(x - sample)))

    wall_contrast = abs(full.a[i_negative, j0]) / max(
        abs(full.a[i_positive, j0]), 1.0e-30
    )

    H = full.h * problem.phase
    relative = full.a * full.a * np.conj(H)

    mask = (np.abs(full.a) > 0.40 * F_A) & (full.h > 0.40)

    if np.count_nonzero(mask) == 0:
        phase_lock_cos = -1.0
    else:
        cosine = np.real(relative) / (np.abs(relative) + 1.0e-30)
        phase_weights = np.abs(full.a) ** 2 * full.h**2
        phase_lock_cos = float(
            np.average(cosine[mask], weights=phase_weights[mask])
        )

    flux = (
        full.ax[:, :-1]
        + full.az[1:, :]
        - full.ax[:, 1:]
        - full.az[:-1, :]
    )

    total_fundamental_flux_angle = float(np.sum(flux))

    reference_flux = (
        problem.ax0[:, :-1]
        + problem.az0[1:, :]
        - problem.ax0[:, 1:]
        - problem.az0[:-1, :]
    )

    reference_flux_angle = float(np.sum(reference_flux))

    # The local patch does not enclose the complete exponentially decaying
    # gauge flux, so comparing a finite-patch flux directly with pi is wrong.
    # Boundary links are fixed to the independently reconstructed continuum
    # radial solution; the correct local topology check is therefore the
    # discrete Stokes comparison with that same finite-patch continuum flux.
    flux_relerr = abs(total_fundamental_flux_angle - reference_flux_angle) / max(
        abs(reference_flux_angle), 1.0e-30
    )

    phi_retained = full.sigma_phi / max(base.sigma_phi, 1.0e-30)
    sigma_retained = full.sigma_sigma / max(base.sigma_sigma, 1.0e-30)

    return {
        "wall_contrast": wall_contrast,
        "phase_lock_cos": phase_lock_cos,
        "flux_angle": total_fundamental_flux_angle,
        "flux_reference_angle": reference_flux_angle,
        "patch_flux_over_pi": total_fundamental_flux_angle / math.pi,
        "flux_relerr": flux_relerr,
        "phi_retained": phi_retained,
        "sigma_retained": sigma_retained,
    }


def ring_kernel(radius: float, z_source: float, h_payload: float) -> float:
    """Positive-magnitude axial Green-function kernel for a circular ring."""

    vertical = h_payload - z_source
    return vertical / (radius * radius + vertical * vertical) ** 1.5


def corrected_gravity_diagnostic(p: Parameters, selected: MatchedResult):
    """Re-run the inherited 018B-0F adverse source-level gravity sign."""

    radius = p.loop_radius
    x = p.h_over_r
    h_payload = x * radius

    wall_z = -WALL_ADVERSE_SHIFT_WIDTHS * p.wall_width90
    vertical_wall = h_payload - wall_z

    wall_kernel = 1.0 - vertical_wall / math.sqrt(
        radius * radius + vertical_wall * vertical_wall
    )

    wall_outward = (
        2.0
        * math.pi
        * (-p.wall_active)
        * radius
        * wall_kernel
    )

    q_rim = 2.0 * math.pi * radius * selected.lab_active

    envelope = CORE_ENVELOPE_MULTIPLIER * p.core_width

    inward_kernel = max(
        ring_kernel(radius + dr, dz, h_payload)
        for dr in (-envelope, 0.0, envelope)
        for dz in (-envelope, 0.0, envelope)
        if radius + dr > 0.0
    )

    rim_inward = radius * q_rim * inward_kernel
    net_outward = wall_outward - rim_inward

    active_mass_per_r = (
        2.0 * math.pi * selected.lab_active
        + math.pi * p.wall_active * radius
    )

    energy_per_r = (
        math.pi * p.wall_tension * radius
        + 2.0 * math.pi * selected.lab_E
    )

    if net_outward > 0.0:
        projected_c = energy_per_r / (net_outward * x * x)
    else:
        projected_c = math.inf

    wall_load = p.wall_tension * radius
    balance_rel = abs(selected.lab_P - wall_load) / max(
        abs(selected.lab_P), abs(wall_load), 1.0e-30
    )

    return {
        "wall_load": wall_load,
        "balance_rel": balance_rel,
        "wall_outward": wall_outward,
        "rim_inward": rim_inward,
        "net_outward": net_outward,
        "active_mass_per_r": active_mass_per_r,
        "projected_c": projected_c,
    }


def source_sha256(path: Path) -> str:
    """Return the actual source hash; no stale expected hash is invented."""

    if not path.exists():
        return "MISSING"

    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    """Run the full local two-current/KLS junction closeout."""

    print(
        "=== 018B-0G2 — FULLY COUPLED MATCHED TWO-CURRENT KLS JUNCTION CLOSEOUT ==="
    )

    p = load_parameters()

    print("\n=== UPSTREAM ARTIFACT AUDIT ===")
    print(f"018B0F_ACTUAL_SOURCE_SHA256={source_sha256(F_SOURCE)}")
    print("018B0F_STALE_EXPECTED_HASH_REUSED=NO")

    print("\n=== INDEPENDENT CONTINUUM RECONSTRUCTION ===")

    data = reconstruct_continuum(p)

    print(f"W_PHI={p.w_phi:+.15e}")
    print(f"W_SIGMA={p.w_sigma:+.15e}")
    print(f"RADIAL_SIGMA_PHI={data.sigma_phi:.15e}")
    print(f"RADIAL_SIGMA_SIGMA={data.sigma_sigma:.15e}")
    print(
        "RADIAL_U_MINUS_T_RECONSTRUCTED="
        f"{data.radial_ut_reconstructed:.15e}"
    )
    print(f"RADIAL_U_MINUS_T_LOG={p.U0 - p.T0:.15e}")
    print(f"RADIAL_U_MINUS_T_RELERR={data.radial_ut_relerr:.15e}")
    print(
        "RADIAL_TWO_CURRENT_BVP_RECONSTRUCTION="
        f"{'PASS' if data.radial_ut_relerr < 5.0e-5 else 'FAIL'}"
    )

    print(
        "PLANAR_WALL_TENSION_RECONSTRUCTED="
        f"{data.wall_tension_reconstructed:.15e}"
    )
    print(f"PLANAR_WALL_TENSION_LOG={p.wall_tension:.15e}")
    print(f"PLANAR_WALL_TENSION_RELERR={data.wall_tension_relerr:.15e}")
    print(
        "PLANAR_WALL_BVP_RECONSTRUCTION="
        f"{'PASS' if data.wall_tension_relerr < 5.0e-6 else 'FAIL'}"
    )

    print("\n=== ANALYTIC GRADIENT CHECK ===")

    grad_base_problem = build_problem(
        p,
        data,
        25,
        10.0,
        full=False,
    )

    grad_full_problem = build_problem(
        p,
        data,
        25,
        10.0,
        full=True,
    )

    base_grad_error = directional_gradient_check(
        p,
        grad_base_problem,
        202608301,
    )

    full_grad_error = directional_gradient_check(
        p,
        grad_full_problem,
        202608302,
    )

    gradient_check_pass = (
        base_grad_error < GRADIENT_CHECK_TOL
        and full_grad_error < GRADIENT_CHECK_TOL
    )

    print(f"BASE_DIRECTIONAL_GRADIENT_RELERR={base_grad_error:.15e}")
    print(f"FULL_DIRECTIONAL_GRADIENT_RELERR={full_grad_error:.15e}")
    print(
        "FULL_ANALYTIC_GRADIENT_CHECK="
        f"{'PASS' if gradient_check_pass else 'FAIL'}"
    )

    # ------------------------------------------------------------------
    # Main matched solves.  Cache duplicates shared by the resolution and
    # patch sequences.
    # ------------------------------------------------------------------

    print("\n=== FULLY COUPLED MATCHED MULTISCALE SOLVES ===")

    cases = []

    for case in RESOLUTION_CASES + PATCH_CASES:
        if case not in cases:
            cases.append(case)

    solved = {}

    for n, box_half in cases:
        result = run_case(p, data, n, box_half)
        solved[(n, box_half)] = result

        base_ok = (
            result.base.gradient_rms < GRADIENT_RMS_TOL
            and result.base.gradient_max < GRADIENT_MAX_TOL
        )

        full_ok = (
            result.full.gradient_rms < GRADIENT_RMS_TOL
            and result.full.gradient_max < GRADIENT_MAX_TOL
        )

        print(
            f"CASE_N={n} L={box_half:.1f} DX={result.dx:.9f} "
            f"BASE_RMS={result.base.gradient_rms:.3e} "
            f"BASE_MAX={result.base.gradient_max:.3e} "
            f"FULL_RMS={result.full.gradient_rms:.3e} "
            f"FULL_MAX={result.full.gradient_max:.3e} "
            f"MU_J_RED={result.mu_reduced:+.12e} "
            f"D_SIGMA_PHI={result.delta_sigma_phi:+.12e} "
            f"D_SIGMA_SIGMA={result.delta_sigma_sigma:+.12e} "
            f"LAB_ACTIVE={result.lab_active:+.12e} "
            f"SOLVER_PASS={'YES' if base_ok and full_ok else 'NO'}"
        )

    optimizer_pass = all(
        result.base.gradient_rms < GRADIENT_RMS_TOL
        and result.base.gradient_max < GRADIENT_MAX_TOL
        and result.full.gradient_rms < GRADIENT_RMS_TOL
        and result.full.gradient_max < GRADIENT_MAX_TOL
        for result in solved.values()
    )

    print(
        "ALL_RELEASED_FIELD_STATIONARITY="
        f"{'PASS' if optimizer_pass else 'FAIL'}"
    )

    # ------------------------------------------------------------------
    # Resolution convergence at fixed physical patch.
    # ------------------------------------------------------------------

    resolution_results = [solved[case] for case in RESOLUTION_CASES]

    resolution_mu_spread = relative_spread(
        [result.mu_reduced for result in resolution_results]
    )

    resolution_active_spread = relative_spread(
        [result.lab_active for result in resolution_results]
    )

    resolution_pass = (
        resolution_mu_spread <= MAX_RESOLUTION_MU_SPREAD
        and resolution_active_spread <= MAX_ACTIVE_LINE_SPREAD
    )

    print("\n=== RESOLUTION CONVERGENCE ===")
    print(f"RESOLUTION_MU_REL_SPREAD={resolution_mu_spread:.15e}")
    print(
        "RESOLUTION_CORRECTED_ACTIVE_LINE_REL_SPREAD="
        f"{resolution_active_spread:.15e}"
    )
    print(
        "MATCHED_RESOLUTION_CONVERGENCE="
        f"{'PASS' if resolution_pass else 'FAIL'}"
    )

    # ------------------------------------------------------------------
    # Patch continuation at fixed dx=0.5.
    # ------------------------------------------------------------------

    patch_results = [solved[case] for case in PATCH_CASES]

    patch_mu_spread = relative_spread(
        [result.mu_reduced for result in patch_results]
    )

    patch_active_spread = relative_spread(
        [result.lab_active for result in patch_results]
    )

    patch_pass = (
        patch_mu_spread <= MAX_PATCH_MU_SPREAD
        and patch_active_spread <= MAX_ACTIVE_LINE_SPREAD
    )

    print("\n=== PATCH-SIZE CONTINUATION ===")
    print(f"PATCH_MU_REL_SPREAD={patch_mu_spread:.15e}")
    print(
        "PATCH_CORRECTED_ACTIVE_LINE_REL_SPREAD="
        f"{patch_active_spread:.15e}"
    )
    print(
        "MATCHED_PATCH_CONTINUATION="
        f"{'PASS' if patch_pass else 'FAIL'}"
    )

    # ------------------------------------------------------------------
    # Matching-profile sensitivity.  Only the FULL solution depends on this
    # outer interpolation convention; the physical corrected active line
    # should be insensitive after relaxation.
    # ------------------------------------------------------------------

    print("\n=== OUTER-MATCH BLEND SENSITIVITY ===")

    blend_results = []
    n_blend, l_blend = BLEND_CASE

    blend_base = solved[(n_blend, l_blend)].base

    for factor in BLEND_FACTORS:
        if math.isclose(factor, DEFAULT_BLEND_FACTOR):
            result = solved[(n_blend, l_blend)]
        else:
            full_problem = build_problem(
                p,
                data,
                n_blend,
                l_blend,
                full=True,
                blend_factor=factor,
            )
            full_result = solve_lattice(p, full_problem)
            result = matched_result(p, data, blend_base, full_result)

        blend_results.append(result)

        print(
            f"BLEND_FACTOR={factor:.3f} "
            f"MU_J_RED={result.mu_reduced:+.12e} "
            f"LAB_ACTIVE={result.lab_active:+.12e} "
            f"FULL_RMS={result.full.gradient_rms:.3e} "
            f"FULL_MAX={result.full.gradient_max:.3e}"
        )

    blend_active_spread = relative_spread(
        [result.lab_active for result in blend_results]
    )

    blend_pass = blend_active_spread <= MAX_BLEND_ACTIVE_LINE_SPREAD

    print(
        "BLEND_CORRECTED_ACTIVE_LINE_REL_SPREAD="
        f"{blend_active_spread:.15e}"
    )
    print(
        "OUTER_MATCH_PROFILE_SENSITIVITY="
        f"{'PASS' if blend_pass else 'FAIL'}"
    )

    # ------------------------------------------------------------------
    # Selected highest-domain fine case.
    # ------------------------------------------------------------------

    selected = solved[SELECTED_CASE]
    topology = topology_metrics(p, selected)
    gravity = corrected_gravity_diagnostic(p, selected)

    print("\n=== SELECTED FULLY COUPLED LOCAL JUNCTION ===")
    print(f"SELECTED_N={selected.n}")
    print(f"SELECTED_L={selected.box_half:.15e}")
    print(f"SELECTED_DX={selected.dx:.15e}")
    print(f"MATCHED_JUNCTION_REDUCED_ENERGY={selected.mu_reduced:+.15e}")
    print(f"DELTA_SIGMA_PHI={selected.delta_sigma_phi:+.15e}")
    print(f"DELTA_SIGMA_SIGMA={selected.delta_sigma_sigma:+.15e}")
    print(f"DELTA_EIGENFRAME_U={selected.delta_U:+.15e}")
    print(f"DELTA_EIGENFRAME_T={selected.delta_T:+.15e}")
    print(f"DELTA_EIGENFRAME_J={selected.delta_J:+.15e}")
    print(f"CORRECTED_EIGENFRAME_U={selected.U:+.15e}")
    print(f"CORRECTED_EIGENFRAME_T={selected.T:+.15e}")
    print(f"CORRECTED_EIGENFRAME_J={selected.J:+.15e}")
    print(f"CORRECTED_LAB_ENERGY_LINE={selected.lab_E:+.15e}")
    print(f"CORRECTED_LAB_P_PARALLEL={selected.lab_P:+.15e}")
    print(f"CORRECTED_LAB_MOMENTUM_LINE={selected.lab_J:+.15e}")
    print(f"CORRECTED_LAB_ACTIVE_LINE={selected.lab_active:+.15e}")

    print("\n=== TOPOLOGY / MORPHOLOGY ===")
    print(f"LOCAL_ONE_WALL_CONTRAST={topology['wall_contrast']:.15e}")
    print(f"GAUGE_INVARIANT_PHASE_LOCK_COS={topology['phase_lock_cos']:.15e}")
    print(f"FUNDAMENTAL_PATCH_FLUX_ANGLE={topology['flux_angle']:+.15e}")
    print(
        "CONTINUUM_MATCHED_PATCH_FLUX_ANGLE="
        f"{topology['flux_reference_angle']:+.15e}"
    )
    print(f"PATCH_FLUX_OVER_PI={topology['patch_flux_over_pi']:+.15e}")
    print(f"PATCH_FLUX_CONTINUUM_MATCH_RELERR={topology['flux_relerr']:.15e}")
    print("FINITE_PATCH_EXPECTED_TO_ENCLOSE_FULL_PI_FLUX=NO")
    print(f"PHI_CONDENSATE_RETAINED_FRACTION={topology['phi_retained']:.15e}")
    print(f"SIGMA_CONDENSATE_RETAINED_FRACTION={topology['sigma_retained']:.15e}")

    topology_pass = (
        topology["wall_contrast"] <= MAX_WALL_CONTRAST
        and topology["phase_lock_cos"] >= MIN_PHASE_LOCK_COS
        and topology["flux_relerr"] <= MAX_FLUX_RELERR
        and topology["phi_retained"] >= MIN_CARRIER_RETAINED_FRACTION
        and topology["sigma_retained"] >= MIN_CARRIER_RETAINED_FRACTION
    )

    print(
        "FULL_LOCAL_JUNCTION_TOPOLOGY_AND_CARRIER_HEALTH="
        f"{'PASS' if topology_pass else 'FAIL'}"
    )

    print("\n=== 018B-0F STATIONARY/GRAVITY CARRY-FORWARD DIAGNOSTIC ===")
    print(f"OLD_INTEGER_LOOP_RADIUS={p.loop_radius:.15e}")
    print(f"OLD_H_OVER_R={p.h_over_r:.15e}")
    print(f"CORRECTED_WALL_LOAD={gravity['wall_load']:+.15e}")
    print(f"CORRECTED_WALL_BALANCE_RELERR={gravity['balance_rel']:.15e}")
    print(f"CORRECTED_ADVERSE_WALL_OUTWARD={gravity['wall_outward']:+.15e}")
    print(f"CORRECTED_ADVERSE_RIM_INWARD={gravity['rim_inward']:+.15e}")
    print(f"CORRECTED_ADVERSE_FINITE_PAYLOAD_OUTWARD={gravity['net_outward']:+.15e}")
    print(f"CORRECTED_ACTIVE_MASS_PER_R={gravity['active_mass_per_r']:+.15e}")
    print(f"CORRECTED_PROJECTED_C_PREFLIGHT={gravity['projected_c']:.15e}")

    stationary_carry_pass = (
        selected.lab_P > 0.0
        and selected.lab_active > 0.0
        and gravity["net_outward"] > 0.0
        and gravity["active_mass_per_r"] > 0.0
    )

    print(
        "POSITIVE_STATIONARY_RIM_PRESSURE_AFTER_JUNCTION="
        f"{'PASS' if selected.lab_P > 0.0 else 'FAIL'}"
    )
    print(
        "FINITE_PAYLOAD_REPULSION_AFTER_LOCAL_JUNCTION="
        f"{'PASS' if gravity['net_outward'] > 0.0 else 'FAIL'}"
    )
    print(
        "POSITIVE_ACTIVE_MASS_AFTER_LOCAL_JUNCTION="
        f"{'PASS' if gravity['active_mass_per_r'] > 0.0 else 'FAIL'}"
    )

    # Exact mechanical balance is deliberately NOT required at the old 018B-0F
    # integer pair: the junction has changed the EOS.  018B-0H must re-solve
    # exact integer stationarity using the corrected local EOS.
    print("OLD_018B0F_INTEGER_PAIR_REOPTIMIZED_AFTER_JUNCTION=NO")
    print("OLD_018B0F_BALANCE_USED_AS_PROMOTION_CRITERION=NO")

    continuum_pass = (
        data.radial_ut_relerr < 5.0e-5
        and data.wall_tension_relerr < 5.0e-6
    )

    overall = (
        continuum_pass
        and gradient_check_pass
        and optimizer_pass
        and resolution_pass
        and patch_pass
        and blend_pass
        and topology_pass
        and stationary_carry_pass
    )

    print("\n=== DECISION ===")

    if overall:
        print("018B0G2_FULLY_COUPLED_TWO_CURRENT_2D_STRING_WALL_JUNCTION=GREEN")
        print(
            "FULLY_COUPLED_LOCAL_TWO_CURRENT_KLS_JUNCTION="
            "SUPPORTED_WITH_FINE_CORE_PLUS_MATCHED_PLANAR_OUTER_SOLUTION"
        )
        print("MANDATORY_NEW_JUNCTION_ENERGY=INCLUDED_LOCALLY")
        print("CURRENT_CARRIER_BACKREACTION=INCLUDED_LOCALLY")
        print("TRANSVERSE_GAUGE_BACKREACTION=INCLUDED_LOCALLY")
        print("SOURCE_LEVEL_GRAVITY_SIGN_SURVIVES_LOCAL_JUNCTION=YES")
        print(
            "NEXT="
            "018B0H_COMPLETE_SOURCE_GRAVITY_REVALIDATION_WITH_CORRECTED_JUNCTION_EOS"
        )
        print(
            "NEXT_AFTER_018B0H_GREEN="
            "TRUE_018B_GLOBAL_TOROIDAL_EULER_LAGRANGE_SOLVE"
        )
    else:
        print("018B0G2_FULLY_COUPLED_TWO_CURRENT_2D_STRING_WALL_JUNCTION=RED")
        print("FULLY_COUPLED_LOCAL_TWO_CURRENT_KLS_JUNCTION=NOT_ESTABLISHED")
        print("NEXT=CLASSIFY_018B0G2_FAILURE_BEFORE_ANY_GLOBAL_TOROIDAL_SOLVE")

    print(f"CURRENT_HEURISTIC={CURRENT_HEURISTIC}")
    print("HEURISTIC_INCREASE_FROM_THIS_GATE=NO_LOCAL_JUNCTION_GATE_ONLY")
    print("PROJECTED_C_STATUS=NOT_VALIDATED")
    print("GLOBAL_TOROIDAL_FIELD_SOLUTION=NOT_YET_RUN")
    print("FULL_COMPOSITE_STABILITY=NOT_ESTABLISHED")
    print("FRAME_DRAGGING=NOT_INCLUDED")
    print("NONLINEAR_EINSTEIN_MATTER=NOT_ESTABLISHED")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018B0G2_FULLY_COUPLED_MATCHED_TWO_CURRENT_KLS_JUNCTION_CLOSEOUT"
    )


if __name__ == "__main__":
    main()
