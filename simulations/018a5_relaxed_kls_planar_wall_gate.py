#!/usr/bin/env python3
"""Simulation 018A-5 — relaxed same-gauge KLS planar-wall gate.

PURPOSE
-------
Replace the fixed-amplitude phase-wall trial estimate used in 018A-4 with an
actual microscopic zero-temperature planar wall solution of the selected
same-gauge U(1) -> Z2 -> 1 field theory.

018A-4 established at preflight level:

    - exact charge/holonomy arithmetic forcing a wall on the 017P vortex;
    - one effective Z2 branch sheet for the minimal string;
    - preservation of the local 017P Phi/gauge coupling;
    - absence of the previous global-string logarithmic tail;
    - a nonempty physically motivated coarse basin;
    - 125/125 selected +/-10 percent robustness.

However, 018A-4 deliberately used a fixed-amplitude relative-phase wall trial
path. Its wall tension was therefore NOT the fully relaxed microscopic wall
tension.

This file closes that cheaper prerequisite before any true 2D string-wall
junction calculation.

SCIENTIFIC QUESTION
-------------------
Does the selected same-gauge discrete-remnant model possess a finite,
positive-energy, zero-temperature planar wall solution with:

    - relaxed Phi and A amplitudes;
    - finite microscopic tension;
    - finite thickness;
    - negative integrated active gravitational source;
    - a positive transverse-complex-field stability preflight;
    - finite 017P charge, winding, and radius matching;
    - a robust parameter neighborhood?

MODEL
-----
The high-scale charge-2 string field is Phi.

The low-scale charge-1 wall field is A.

Far from the string core choose a gauge in which

    Phi = f

is real.

For the real wall section write

    A = x.

The potential inherited from 018A-4 is

    V =
        lambda_Phi/4 (f^2-v^2)^2
        + lambda_A/4 (x^2-F^2)^2
        - 2 h f x^2
        + c_Phi (f^2-v^2)
        + c_A (x^2-F^2)
        + C

with

    c_Phi = h F^2 / v
    c_A   = 2 h v
    C     = 2 h v F^2.

These terms make

    f=v
    x=+/-F

degenerate zero-energy stationary vacua in this gauge.

PLANAR WALL EQUATIONS
---------------------
For static z-dependent real amplitudes, in the field normalization used by
the project,

    epsilon = f'^2 + x'^2 + V.

Variation gives

    f'' = 1/2 dV/df

    x'' = 1/2 dV/dx.

Boundary conditions are

    f(-infinity) = v
    f(+infinity) = v

    x(-infinity) = -F
    x(+infinity) = +F.

FROZEN-PHI ANALYTIC SOLUTION
----------------------------
If f=v is frozen, the real section reduces exactly to

    V =
        lambda_A/4 (x^2-F^2)^2.

Then

    x(z)
      =
      F tanh(k z)

with

    k =
      F sqrt(lambda_A) / 2.

Its exact tension is

    sigma_Ising
      =
      4/3 F^3 sqrt(lambda_A).

The characteristic inverse-slope thickness is

    delta_char
      =
      1/k
      =
      2 / [F sqrt(lambda_A)].

The 90-percent amplitude width is

    width_90
      =
      2 atanh(0.9) / k.

This exact solution is used as an independent analytic reference for the
fully coupled numerical f-x wall.

WHY THIS CAN BE LOWER THAN THE 018A-4 TRIAL
-------------------------------------------
018A-4 fixed both amplitudes and rotated the gauge-invariant relative phase.

That produced the trial tension

    sigma_phase
      =
      8 sqrt(2 C_delta B_delta)

with

    C_delta =
      v^2 F^2 / (4 v^2 + F^2)

and

    B_delta =
      2 h v F^2.

The real wall can instead pass through A=0.

The actual field theory is free to choose the lower-action path.

Therefore the fixed-amplitude result was an upper-bound trial path, not a
prediction that the microscopic wall must retain constant |A|.

TRANSVERSE COMPLEX-FIELD STABILITY PREFLIGHT
--------------------------------------------
Restore the imaginary component

    A = x + i y.

Around the real wall, the quadratic energy in y contains

    y'^2 + U_y(z) y^2

where

    U_y =
      lambda_A/2 (x^2-F^2)
      + 2 h f
      + c_A.

For frozen f=v and the analytic kink, the fluctuation operator is a
Pöschl-Teller problem whose lowest eigenvalue is

    lambda_y,min
      =
      4 h v
      - lambda_A F^2 / 4.

Thus the frozen-f real wall is stable against this imaginary-A deformation
when

    h >
      lambda_A F^2 / (16 v).

The coupled numerical wall is independently tested by discretizing its
actual U_y(z) and calculating the lowest eigenvalue.

This is a NECESSARY local wall-stability preflight, not the final stability
proof of the full string-wall-vorton composite.

ACTIVE GRAVITATIONAL SOURCE
---------------------------
For a static planar canonical wall,

    epsilon =
      K + V

    p_x = p_y =
      -epsilon

    p_z =
      K - V

where

    K =
      f'^2 + x'^2.

Therefore

    S =
      epsilon + p_x + p_y + p_z
      =
      -2 V.

For a stationary wall connecting degenerate vacua, the first-integral/virial
identity gives

    integral K dz
      =
      integral V dz.

Hence

    integral S dz
      =
      -sigma_W.

The numerical wall must reproduce this identity.

017P SCALE CLOSURE
------------------
Use the previously reconstructed 017P selected-point values

    Q/N =
      6.628230560688

    ell = L/Q =
      0.4257542346286

    w_stat =
      12.66497926067.

Once the microscopic tension sigma_W is known,

    Q_req =
      w_stat / sigma_W

    N_req =
      Q_req / (Q/N)

    R_req =
      Q_req ell / (2 pi).

Both the characteristic wall thickness and the more conservative 90-percent
width are checked against R.

The new string/junction line energy is still not solved here and remains a
mandatory future bookkeeping term.

ROBUSTNESS
----------
The selected point is

    F = 0.075
    h = 0.010
    lambda_A = 1.

The exact frozen-f wall formulas are applied to:

    - the original 30-point physically motivated F-h scan;
    - a 5^3 = 125 point +/-10 percent selected robustness lattice.

The coupled BVP itself is domain-converged at the selected point.

The analytic basin is only a preflight because full coupled BVP robustness
will belong to the true 2D junction stage if this gate passes.

BLIND WILDCARD POLICY
---------------------
The user's blind values

    1.6
    1.875
    3.125
    0.625
    5

are used only afterward as multiplicative h checks.

They are not physics priors and cannot determine the decision.

VALIDATION
----------
The selected wall must satisfy:

    - BVP convergence on multiple domain sizes;
    - numerical tension agreement with the frozen-Phi analytic scale;
    - extremely small virial residual;
    - integrated active source approximately -sigma;
    - positive lowest imaginary-A fluctuation eigenvalue;
    - finite Q, N, R;
    - strong R / wall-thickness separation;
    - integer-winding compatibility;
    - robust selected analytic neighborhood.

FALSIFICATION
-------------
This same-gauge wall model should be demoted before the 2D junction if:

    - no converged planar wall exists;
    - the relaxed wall develops negative total tension;
    - the transverse A mode is unstable throughout the healthy basin;
    - scale closure fails;
    - robustness collapses under ordinary parameter variation.

LIMITATIONS
-----------
A green result does NOT establish:

    - the true 2D string-wall junction;
    - full coupled Phi/A/gauge/sigma relaxation near the rim;
    - new junction line energy;
    - the perturbed 017P equation of state;
    - complete junction stress-energy;
    - finite-payload gravity with the new sector;
    - full dynamical stability;
    - nonlinear Einstein-matter consistency;
    - practical energy scaling;
    - a practical antigravity device.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018A_RELAXED_KLS_PLANAR_WALL_GATE
"""

from __future__ import annotations

from dataclasses import dataclass
import itertools
import math

import numpy as np
from scipy.integrate import simpson
from scipy.integrate import solve_bvp
from scipy.linalg import eigh_tridiagonal


# ============================================================================
# Existing 017P / 018A-4 anchors.
# ============================================================================

V_PHI = 1.0
LAMBDA_PHI = 1.0

F_SELECTED = 0.075
H_SELECTED = 0.010
LAMBDA_A_SELECTED = 1.0

G_017P = 0.1414213562373095

Q_OVER_N = 6.628230560688
ELL = 0.4257542346286
W_STAT = 12.66497926067


# ============================================================================
# Preflight scan sets.
# ============================================================================

F_SCAN = (
    0.050,
    0.075,
    0.100,
    0.125,
    0.150,
)

H_SCAN = (
    0.0025,
    0.0050,
    0.0100,
    0.0200,
    0.0400,
    0.0800,
)

ROBUST_FACTORS = (
    0.90,
    0.95,
    1.00,
    1.05,
    1.10,
)

WILDCARD_VALUES = (
    1.6,
    1.875,
    3.125,
    0.625,
    5.0,
)


# ============================================================================
# Numerical gates.
# ============================================================================

DOMAIN_MULTIPLIERS = (
    8.0,
    10.0,
    12.0,
    16.0,
)

BVP_TOL = 1.0e-8
BVP_MAX_NODES = 30000

MIN_SCALE_SEPARATION = 10.0
MAX_GAUGE_MASS_SQ_SHIFT = 0.01

MAX_TENSION_DOMAIN_REL_SPREAD = 1.0e-5
MAX_VIRIAL_ABS = 1.0e-5
MAX_ACTIVE_RELERR = 1.0e-5

MIN_PHASE_EIGENVALUE = 0.0

INHERITED_GAUGE_CORE_PROXY = (
    1.0
    /
    (
        math.sqrt(2.0)
        *
        G_017P
    )
)


@dataclass(frozen=True)
class WallResult:
    """Selected numerical coupled-wall diagnostics."""

    domain_multiplier: float

    tension: float
    active_integral: float
    active_over_tension: float

    virial_residual: float

    f_min: float
    f_max_abs_deviation: float

    width_90: float
    characteristic_width: float

    min_potential: float
    max_potential: float

    max_rms_residual: float

    solution: object


@dataclass(frozen=True)
class AnalyticPoint:
    """Cheap exact/frozen-Phi wall and scale diagnostics."""

    F: float
    h: float
    lambda_a: float

    phase_eigenvalue_fixed_phi: float

    sigma_real_exact: float

    delta_char: float
    width_90: float

    q_req: float
    n_req: float
    radius_req: float

    radius_over_delta_char: float
    radius_over_width_90: float
    radius_over_core: float

    gauge_mass_sq_shift: float

    passed: bool


def coefficients(
    F: float,
    h: float,
) -> tuple[float, float, float]:
    """Return vacuum-preserving mass shifts and additive constant."""

    c_phi = (
        h
        *
        F
        *
        F
        /
        V_PHI
    )

    c_a = (
        2.0
        *
        h
        *
        V_PHI
    )

    constant = (
        2.0
        *
        h
        *
        V_PHI
        *
        F
        *
        F
    )

    return (
        c_phi,
        c_a,
        constant,
    )


def potential_real(
    f: np.ndarray,
    x: np.ndarray,
    *,
    F: float,
    h: float,
    lambda_a: float,
) -> np.ndarray:
    """Evaluate the real-section target-preserving potential."""

    (
        c_phi,
        c_a,
        constant,
    ) = coefficients(
        F,
        h,
    )

    return (
        LAMBDA_PHI
        /
        4.0
        *
        (
            f
            *
            f
            -
            V_PHI
            *
            V_PHI
        ) ** 2

        +
        lambda_a
        /
        4.0
        *
        (
            x
            *
            x
            -
            F
            *
            F
        ) ** 2

        -
        2.0
        *
        h
        *
        f
        *
        x
        *
        x

        +
        c_phi
        *
        (
            f
            *
            f
            -
            V_PHI
            *
            V_PHI
        )

        +
        c_a
        *
        (
            x
            *
            x
            -
            F
            *
            F
        )

        +
        constant
    )


def analytic_k(
    F: float,
    lambda_a: float,
) -> float:
    """Return inverse characteristic width of the frozen-Phi real kink."""

    return (
        F
        *
        math.sqrt(
            lambda_a
        )
        /
        2.0
    )


def analytic_sigma_real(
    F: float,
    lambda_a: float,
) -> float:
    """Exact frozen-Phi real-kink tension."""

    return (
        4.0
        /
        3.0
        *
        F**3
        *
        math.sqrt(
            lambda_a
        )
    )


def analytic_phase_trial_sigma(
    F: float,
    h: float,
) -> float:
    """Return the 018A-4 fixed-amplitude phase-wall trial tension."""

    c_delta = (
        V_PHI
        *
        V_PHI
        *
        F
        *
        F
        /
        (
            4.0
            *
            V_PHI
            *
            V_PHI
            +
            F
            *
            F
        )
    )

    b_delta = (
        2.0
        *
        h
        *
        V_PHI
        *
        F
        *
        F
    )

    return (
        8.0
        *
        math.sqrt(
            2.0
            *
            c_delta
            *
            b_delta
        )
    )


def fixed_phi_phase_eigenvalue(
    F: float,
    h: float,
    lambda_a: float,
) -> float:
    """Exact lowest imaginary-A eigenvalue for the frozen-Phi real kink."""

    return (
        4.0
        *
        h
        *
        V_PHI

        -
        lambda_a
        *
        F
        *
        F
        /
        4.0
    )


def solve_coupled_wall(
    *,
    F: float,
    h: float,
    lambda_a: float,
    domain_multiplier: float,
) -> WallResult:
    """Solve the coupled f-x planar wall BVP."""

    (
        c_phi,
        c_a,
        _,
    ) = coefficients(
        F,
        h,
    )

    k = analytic_k(
        F,
        lambda_a,
    )

    characteristic_width = (
        1.0
        /
        k
    )

    half_extent = (
        domain_multiplier
        *
        characteristic_width
    )

    z = np.linspace(
        -half_extent,
        half_extent,
        900,
    )

    kz = (
        k
        *
        z
    )

    x_guess = (
        F
        *
        np.tanh(
            kz
        )
    )

    x_prime_guess = (
        F
        *
        k
        /
        np.cosh(
            np.clip(
                kz,
                -40.0,
                40.0,
            )
        ) ** 2
    )

    f_guess = np.full_like(
        z,
        V_PHI,
    )

    f_prime_guess = np.zeros_like(
        z
    )

    y_guess = np.vstack(
        [
            f_guess,
            f_prime_guess,
            x_guess,
            x_prime_guess,
        ]
    )

    def ode(
        _: np.ndarray,
        y: np.ndarray,
    ) -> np.ndarray:
        f = y[0]
        f_prime = y[1]

        x = y[2]
        x_prime = y[3]

        dV_df = (
            LAMBDA_PHI
            *
            f
            *
            (
                f
                *
                f
                -
                V_PHI
                *
                V_PHI
            )

            -
            2.0
            *
            h
            *
            x
            *
            x

            +
            2.0
            *
            c_phi
            *
            f
        )

        dV_dx = (
            lambda_a
            *
            x
            *
            (
                x
                *
                x
                -
                F
                *
                F
            )

            -
            4.0
            *
            h
            *
            f
            *
            x

            +
            2.0
            *
            c_a
            *
            x
        )

        return np.vstack(
            [
                f_prime,
                0.5
                *
                dV_df,

                x_prime,
                0.5
                *
                dV_dx,
            ]
        )

    def boundary(
        ya: np.ndarray,
        yb: np.ndarray,
    ) -> np.ndarray:
        return np.array(
            [
                ya[0]
                -
                V_PHI,

                yb[0]
                -
                V_PHI,

                ya[2]
                +
                F,

                yb[2]
                -
                F,
            ]
        )

    solution = solve_bvp(
        ode,
        boundary,
        z,
        y_guess,
        tol=BVP_TOL,
        max_nodes=BVP_MAX_NODES,
    )

    if solution.status != 0:
        raise RuntimeError(
            "Coupled KLS planar wall BVP failed: "
            f"{solution.message}"
        )

    z_eval = np.linspace(
        -half_extent,
        half_extent,
        10000,
    )

    (
        f,
        f_prime,
        x,
        x_prime,
    ) = solution.sol(
        z_eval
    )

    potential = potential_real(
        f,
        x,
        F=F,
        h=h,
        lambda_a=lambda_a,
    )

    kinetic = (
        f_prime
        *
        f_prime

        +
        x_prime
        *
        x_prime
    )

    energy_density = (
        kinetic
        +
        potential
    )

    tension = float(
        simpson(
            energy_density,
            x=z_eval,
        )
    )

    kinetic_integral = float(
        simpson(
            kinetic,
            x=z_eval,
        )
    )

    potential_integral = float(
        simpson(
            potential,
            x=z_eval,
        )
    )

    active_integral = float(
        simpson(
            -2.0
            *
            potential,
            x=z_eval,
        )
    )

    virial_residual = (
        kinetic_integral
        -
        potential_integral
    ) / tension

    target_lo = (
        -0.9
        *
        F
    )

    target_hi = (
        +0.9
        *
        F
    )

    z_lo = float(
        np.interp(
            target_lo,
            x,
            z_eval,
        )
    )

    z_hi = float(
        np.interp(
            target_hi,
            x,
            z_eval,
        )
    )

    width_90 = (
        z_hi
        -
        z_lo
    )

    return WallResult(
        domain_multiplier=domain_multiplier,

        tension=tension,
        active_integral=active_integral,
        active_over_tension=(
            active_integral
            /
            tension
        ),

        virial_residual=virial_residual,

        f_min=float(
            np.min(
                f
            )
        ),

        f_max_abs_deviation=float(
            np.max(
                np.abs(
                    f
                    -
                    V_PHI
                )
            )
        ),

        width_90=width_90,
        characteristic_width=characteristic_width,

        min_potential=float(
            np.min(
                potential
            )
        ),

        max_potential=float(
            np.max(
                potential
            )
        ),

        max_rms_residual=float(
            np.max(
                solution.rms_residuals
            )
        ),

        solution=solution,
    )


def transverse_imaginary_mode(
    wall: WallResult,
    *,
    F: float,
    h: float,
    lambda_a: float,
) -> float:
    """Numerically reconstruct the lowest imaginary-A fluctuation eigenvalue."""

    (
        _,
        c_a,
        _,
    ) = coefficients(
        F,
        h,
    )

    k = analytic_k(
        F,
        lambda_a,
    )

    half_extent = (
        8.0
        /
        k
    )

    point_count = 1800

    z = np.linspace(
        -half_extent,
        half_extent,
        point_count,
    )

    (
        f,
        _,
        x,
        _,
    ) = wall.solution.sol(
        z
    )

    potential_coefficient = (
        lambda_a
        /
        2.0
        *
        (
            x
            *
            x
            -
            F
            *
            F
        )

        +
        2.0
        *
        h
        *
        f

        +
        c_a
    )

    dz = float(
        z[1]
        -
        z[0]
    )

    interior = (
        potential_coefficient[
            1:-1
        ]
    )

    diagonal = (
        2.0
        /
        (
            dz
            *
            dz
        )

        +
        interior
    )

    off_diagonal = (
        -1.0
        /
        (
            dz
            *
            dz
        )
        *
        np.ones(
            len(
                diagonal
            )
            -
            1,
            dtype=float,
        )
    )

    eigenvalues = eigh_tridiagonal(
        diagonal,
        off_diagonal,
        select="i",
        select_range=(
            0,
            2,
        ),
        eigvals_only=True,
    )

    return float(
        eigenvalues[
            0
        ]
    )


def analytic_point(
    F: float,
    h: float,
    lambda_a: float,
) -> AnalyticPoint:
    """Evaluate the cheap exact real-wall scale/stability preflight."""

    k = analytic_k(
        F,
        lambda_a,
    )

    delta_char = (
        1.0
        /
        k
    )

    width_90 = (
        2.0
        *
        math.atanh(
            0.9
        )
        /
        k
    )

    sigma = analytic_sigma_real(
        F,
        lambda_a,
    )

    phase_eigenvalue = (
        fixed_phi_phase_eigenvalue(
            F,
            h,
            lambda_a,
        )
    )

    q_req = (
        W_STAT
        /
        sigma
    )

    n_req = (
        q_req
        /
        Q_OVER_N
    )

    radius_req = (
        q_req
        *
        ELL
        /
        (
            2.0
            *
            math.pi
        )
    )

    new_a_core = (
        1.0
        /
        (
            F
            *
            math.sqrt(
                lambda_a
            )
        )
    )

    max_core = max(
        INHERITED_GAUGE_CORE_PROXY,
        new_a_core,
    )

    gauge_mass_sq_shift = (
        F
        *
        F
        /
        4.0
    )

    passed = (
        phase_eigenvalue
        >
        MIN_PHASE_EIGENVALUE

        and
        radius_req
        /
        delta_char
        >=
        MIN_SCALE_SEPARATION

        and
        radius_req
        /
        width_90
        >=
        MIN_SCALE_SEPARATION

        and
        radius_req
        /
        max_core
        >=
        MIN_SCALE_SEPARATION

        and
        gauge_mass_sq_shift
        <=
        MAX_GAUGE_MASS_SQ_SHIFT

        and
        V_PHI
        /
        F
        >=
        5.0
    )

    return AnalyticPoint(
        F=F,
        h=h,
        lambda_a=lambda_a,

        phase_eigenvalue_fixed_phi=(
            phase_eigenvalue
        ),

        sigma_real_exact=sigma,

        delta_char=delta_char,
        width_90=width_90,

        q_req=q_req,
        n_req=n_req,
        radius_req=radius_req,

        radius_over_delta_char=(
            radius_req
            /
            delta_char
        ),

        radius_over_width_90=(
            radius_req
            /
            width_90
        ),

        radius_over_core=(
            radius_req
            /
            max_core
        ),

        gauge_mass_sq_shift=(
            gauge_mass_sq_shift
        ),

        passed=passed,
    )


def print_analytic_point(
    label: str,
    point: AnalyticPoint,
) -> None:
    """Print one compact analytic real-wall preflight point."""

    print(
        f"{label} "
        f"F={point.F:.9f} "
        f"H={point.h:.9f} "
        f"LAMBDA_A={point.lambda_a:.9f} "
        f"PHASE_EIG_FIXED={point.phase_eigenvalue_fixed_phi:+.12e} "
        f"SIGMA_REAL={point.sigma_real_exact:.12e} "
        f"DELTA_CHAR={point.delta_char:.9f} "
        f"WIDTH90={point.width_90:.9f} "
        f"Q_REQ={point.q_req:.9f} "
        f"N_REQ={point.n_req:.9f} "
        f"R_REQ={point.radius_req:.9f} "
        f"R_OVER_DELTA={point.radius_over_delta_char:.9f} "
        f"R_OVER_WIDTH90={point.radius_over_width_90:.9f} "
        f"R_OVER_CORE={point.radius_over_core:.9f} "
        f"GAUGE_M2_SHIFT={point.gauge_mass_sq_shift:.9e} "
        f"PASS={'YES' if point.passed else 'NO'}"
    )


def main() -> None:
    """Execute the relaxed planar-wall gate."""

    print(
        "=== ANTIGRAVITY_RESEARCH 018A-5 ==="
    )

    print(
        "QUESTION="
        "DOES_THE_SAME_GAUGE_KLS_CLASS_HAVE_A_RELAXED_STABLE_MICROSCOPIC_PLANAR_WALL"
    )

    print(
        "\n=== ANALYTIC WALL BRANCHES ==="
    )

    sigma_phase = (
        analytic_phase_trial_sigma(
            F_SELECTED,
            H_SELECTED,
        )
    )

    sigma_real = (
        analytic_sigma_real(
            F_SELECTED,
            LAMBDA_A_SELECTED,
        )
    )

    k_selected = (
        analytic_k(
            F_SELECTED,
            LAMBDA_A_SELECTED,
        )
    )

    phase_eig_fixed = (
        fixed_phi_phase_eigenvalue(
            F_SELECTED,
            H_SELECTED,
            LAMBDA_A_SELECTED,
        )
    )

    h_critical = (
        LAMBDA_A_SELECTED
        *
        F_SELECTED
        *
        F_SELECTED
        /
        (
            16.0
            *
            V_PHI
        )
    )

    print(
        f"SIGMA_PHASE_TRIAL_018A4={sigma_phase:.15e}"
    )

    print(
        f"SIGMA_REAL_EXACT_FROZEN_PHI={sigma_real:.15e}"
    )

    print(
        "REAL_OVER_PHASE_TENSION="
        f"{sigma_real / sigma_phase:.15e}"
    )

    print(
        f"K_REAL={k_selected:.15e}"
    )

    print(
        "DELTA_CHAR_REAL="
        f"{1.0 / k_selected:.15e}"
    )

    print(
        f"H_CRITICAL_FIXED_PHI={h_critical:.15e}"
    )

    print(
        f"H_SELECTED={H_SELECTED:.15e}"
    )

    print(
        "PHASE_EIGENVALUE_FIXED_PHI="
        f"{phase_eig_fixed:+.15e}"
    )

    print(
        "FROZEN_PHI_REAL_WALL_PHASE_STABILITY="
        f"{'PASS' if phase_eig_fixed > 0.0 else 'FAIL'}"
    )

    print(
        "\n=== COUPLED PHI + A PLANAR WALL DOMAIN CONVERGENCE ==="
    )

    wall_results = []

    for multiplier in DOMAIN_MULTIPLIERS:

        wall = solve_coupled_wall(
            F=F_SELECTED,
            h=H_SELECTED,
            lambda_a=LAMBDA_A_SELECTED,
            domain_multiplier=multiplier,
        )

        wall_results.append(
            wall
        )

        print(
            "WALL_DOMAIN "
            f"MULT={multiplier:.1f} "
            f"SIGMA={wall.tension:.15e} "
            f"ACTIVE_OVER_SIGMA={wall.active_over_tension:+.12f} "
            f"VIRIAL={wall.virial_residual:+.6e} "
            f"F_MIN={wall.f_min:.12f} "
            f"F_MAX_ABS_DEV={wall.f_max_abs_deviation:.12e} "
            f"WIDTH90={wall.width_90:.12f} "
            f"MIN_V={wall.min_potential:+.6e} "
            f"MAX_V={wall.max_potential:.6e} "
            f"MAX_RMS={wall.max_rms_residual:.6e}"
        )

    reference_wall = wall_results[
        2
    ]

    tensions = np.array(
        [
            wall.tension
            for wall
            in wall_results[
                1:
            ]
        ],
        dtype=float,
    )

    tension_spread = (
        float(
            np.max(
                tensions
            )
            -
            np.min(
                tensions
            )
        )
        /
        reference_wall.tension
    )

    print(
        "WALL_TENSION_DOMAIN_REL_SPREAD="
        f"{tension_spread:.15e}"
    )

    domain_pass = (
        tension_spread
        <=
        MAX_TENSION_DOMAIN_REL_SPREAD
    )

    print(
        "RELAXED_WALL_DOMAIN_CONVERGENCE="
        f"{'PASS' if domain_pass else 'FAIL'}"
    )

    active_pass = (
        abs(
            reference_wall.active_over_tension
            +
            1.0
        )
        <=
        MAX_ACTIVE_RELERR
    )

    virial_pass = (
        abs(
            reference_wall.virial_residual
        )
        <=
        MAX_VIRIAL_ABS
    )

    print(
        "RELAXED_WALL_ACTIVE_SOURCE_EQUALS_MINUS_TENSION="
        f"{'PASS' if active_pass else 'FAIL'}"
    )

    print(
        "RELAXED_WALL_VIRIAL="
        f"{'PASS' if virial_pass else 'FAIL'}"
    )

    analytic_relerr = (
        abs(
            reference_wall.tension
            -
            sigma_real
        )
        /
        sigma_real
    )

    print(
        "RELAXED_VS_FROZEN_REAL_TENSION_RELERR="
        f"{analytic_relerr:.15e}"
    )

    print(
        "PHI_RELAXATION_MAX_ABS="
        f"{reference_wall.f_max_abs_deviation:.15e}"
    )

    print(
        "\n=== TRANSVERSE COMPLEX-A MODE ==="
    )

    numeric_phase_eig = (
        transverse_imaginary_mode(
            reference_wall,
            F=F_SELECTED,
            h=H_SELECTED,
            lambda_a=LAMBDA_A_SELECTED,
        )
    )

    print(
        "PHASE_EIGENVALUE_NUMERIC_COUPLED_WALL="
        f"{numeric_phase_eig:+.15e}"
    )

    print(
        "PHASE_EIGENVALUE_FIXED_PHI_ANALYTIC="
        f"{phase_eig_fixed:+.15e}"
    )

    print(
        "TRANSVERSE_A_IMAGINARY_MODE_PREFLIGHT="
        f"{'PASS' if numeric_phase_eig > 0.0 else 'FAIL'}"
    )

    print(
        "\n=== MICROSCOPIC 017P SCALE CLOSURE ==="
    )

    sigma_selected = (
        reference_wall.tension
    )

    q_req = (
        W_STAT
        /
        sigma_selected
    )

    n_req = (
        q_req
        /
        Q_OVER_N
    )

    n_integer = max(
        1,
        int(
            round(
                n_req
            )
        ),
    )

    q_integer = (
        n_integer
        *
        Q_OVER_N
    )

    radius_req = (
        q_req
        *
        ELL
        /
        (
            2.0
            *
            math.pi
        )
    )

    new_core_width = (
        1.0
        /
        (
            F_SELECTED
            *
            math.sqrt(
                LAMBDA_A_SELECTED
            )
        )
    )

    max_core_width = max(
        INHERITED_GAUGE_CORE_PROXY,
        new_core_width,
    )

    integer_load_mismatch = (
        abs(
            sigma_selected
            *
            q_integer
            -
            W_STAT
        )
        /
        W_STAT
    )

    print(
        f"SIGMA_W_RELAXED={sigma_selected:.15e}"
    )

    print(
        f"Q_REQ={q_req:.15e}"
    )

    print(
        f"N_REQ={n_req:.15e}"
    )

    print(
        f"N_INTEGER={n_integer}"
    )

    print(
        f"R_REQ={radius_req:.15e}"
    )

    print(
        "R_OVER_DELTA_CHAR="
        f"{radius_req / reference_wall.characteristic_width:.12f}"
    )

    print(
        "R_OVER_WIDTH90="
        f"{radius_req / reference_wall.width_90:.12f}"
    )

    print(
        "R_OVER_CORE="
        f"{radius_req / max_core_width:.12f}"
    )

    print(
        "INTEGER_LOAD_MISMATCH="
        f"{integer_load_mismatch:.15e}"
    )

    scale_pass = (
        radius_req
        /
        reference_wall.characteristic_width
        >=
        MIN_SCALE_SEPARATION

        and
        radius_req
        /
        reference_wall.width_90
        >=
        MIN_SCALE_SEPARATION

        and
        radius_req
        /
        max_core_width
        >=
        MIN_SCALE_SEPARATION

        and
        integer_load_mismatch
        <
        1.0e-3
    )

    print(
        "RELAXED_MICROSCOPIC_SCALE_CLOSURE="
        f"{'PASS' if scale_pass else 'FAIL'}"
    )

    print(
        "\n=== ORIGINAL 30-POINT ANALYTIC REAL-WALL BASIN ==="
    )

    coarse_results = []

    for (
        F,
        h,
    ) in itertools.product(
        F_SCAN,
        H_SCAN,
    ):

        point = analytic_point(
            F,
            h,
            LAMBDA_A_SELECTED,
        )

        coarse_results.append(
            point
        )

        print_analytic_point(
            "COARSE",
            point,
        )

    coarse_pass = [
        point
        for point
        in coarse_results
        if point.passed
    ]

    print(
        f"COARSE_TOTAL={len(coarse_results)}"
    )

    print(
        f"COARSE_PASS={len(coarse_pass)}"
    )

    if coarse_pass:
        print(
            "COARSE_MIN_PHASE_EIG="
            f"{min(p.phase_eigenvalue_fixed_phi for p in coarse_pass):.15e}"
        )

        print(
            "COARSE_MIN_R_OVER_WIDTH90="
            f"{min(p.radius_over_width_90 for p in coarse_pass):.12f}"
        )

        print(
            "COARSE_MIN_R_OVER_CORE="
            f"{min(p.radius_over_core for p in coarse_pass):.12f}"
        )

    print(
        "\n=== SELECTED +/-10 PERCENT 5^3 REAL-WALL ROBUSTNESS ==="
    )

    robust_results = []

    for (
        f_mult,
        h_mult,
        lambda_mult,
    ) in itertools.product(
        ROBUST_FACTORS,
        ROBUST_FACTORS,
        ROBUST_FACTORS,
    ):

        point = analytic_point(
            F_SELECTED
            *
            f_mult,

            H_SELECTED
            *
            h_mult,

            LAMBDA_A_SELECTED
            *
            lambda_mult,
        )

        robust_results.append(
            point
        )

    robust_pass = [
        point
        for point
        in robust_results
        if point.passed
    ]

    print(
        f"ROBUST_TOTAL={len(robust_results)}"
    )

    print(
        f"ROBUST_PASS={len(robust_pass)}"
    )

    if robust_pass:
        print(
            "ROBUST_MIN_PHASE_EIG="
            f"{min(p.phase_eigenvalue_fixed_phi for p in robust_pass):.15e}"
        )

        print(
            "ROBUST_MIN_R_OVER_DELTA="
            f"{min(p.radius_over_delta_char for p in robust_pass):.12f}"
        )

        print(
            "ROBUST_MIN_R_OVER_WIDTH90="
            f"{min(p.radius_over_width_90 for p in robust_pass):.12f}"
        )

        print(
            "ROBUST_MIN_R_OVER_CORE="
            f"{min(p.radius_over_core for p in robust_pass):.12f}"
        )

    robustness_pass = (
        len(
            robust_pass
        )
        ==
        len(
            robust_results
        )
    )

    print(
        "REAL_WALL_SELECTED_ROBUSTNESS="
        f"{'PASS' if robustness_pass else 'FAIL'}"
    )

    print(
        "\n=== BLIND WILDCARD h MULTIPLIERS ==="
    )

    for raw in WILDCARD_VALUES:

        point = analytic_point(
            F_SELECTED,
            H_SELECTED
            *
            raw,
            LAMBDA_A_SELECTED,
        )

        print_analytic_point(
            f"WILDCARD[RAW={raw:.9f}]",
            point,
        )

        print(
            "WILDCARD_INTERPRETATION="
            "BLIND_AUXILIARY_CHECK_NOT_PHYSICS_PRIOR"
        )

    print(
        "\n=== 018A-5 DECISION ==="
    )

    transverse_pass = (
        numeric_phase_eig
        >
        MIN_PHASE_EIGENVALUE
    )

    overall_green = (
        domain_pass
        and
        active_pass
        and
        virial_pass
        and
        transverse_pass
        and
        scale_pass
        and
        robustness_pass
        and
        len(
            coarse_pass
        )
        >
        0
    )

    print(
        "RELAXED_REAL_SECTION_WALL_BVP="
        f"{'PASS' if domain_pass else 'FAIL'}"
    )

    print(
        "CANONICAL_NEGATIVE_ACTIVE_WALL_SOURCE="
        f"{'PASS' if active_pass else 'FAIL'}"
    )

    print(
        "TRANSVERSE_A_IMAGINARY_MODE_PREFLIGHT="
        f"{'PASS' if transverse_pass else 'FAIL'}"
    )

    print(
        "RELAXED_MICROSCOPIC_SCALE_CLOSURE="
        f"{'PASS' if scale_pass else 'FAIL'}"
    )

    print(
        "REAL_WALL_SELECTED_ROBUSTNESS="
        f"{'PASS' if robustness_pass else 'FAIL'}"
    )

    print(
        "018A5_RELAXED_KLS_PLANAR_WALL_GATE="
        f"{'GREEN' if overall_green else 'RED'}"
    )

    print(
        "FULL_RELAXED_REAL_SECTION_MICROSCOPIC_WALL_TENSION="
        +
        (
            "SOLVED_IN_1D_PLANAR_SECTOR"
            if overall_green
            else
            "NOT_ESTABLISHED"
        )
    )

    print(
        "GLOBAL_COMPLEX_WALL_MINIMUM="
        "NOT_YET_PROVEN"
    )

    print(
        "TRUE_2D_STRING_WALL_JUNCTION="
        "NOT_YET_SOLVED"
    )

    print(
        "PERTURBED_017P_EOS_WITH_CHARGE1_FIELD="
        "NOT_YET_SOLVED"
    )

    print(
        "COMPLETE_JUNCTION_STRESS_ENERGY="
        "NOT_YET_SOLVED"
    )

    print(
        "FINITE_PAYLOAD_GRAVITY_WITH_NEW_SECTOR="
        "NOT_YET_TESTED"
    )

    print(
        "FULL_018A_GATE="
        "NOT_YET_GREEN"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018A_RELAXED_KLS_PLANAR_WALL_GATE"
    )

    if overall_green:
        print(
            "NEXT="
            "018A6_MINIMAL_TRUE_2D_KLS_STRING_WALL_JUNCTION_DIAGNOSTIC"
        )
    else:
        print(
            "NEXT="
            "AUDIT_OR_DEMOTE_SAME_GAUGE_WALL_BEFORE_TRUE_2D_ESCALATION"
        )


if __name__ == "__main__":
    main()
