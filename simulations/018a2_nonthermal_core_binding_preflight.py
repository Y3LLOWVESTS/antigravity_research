"""Simulation 018A-2 — nonthermal composite-rim core-binding preflight.

PURPOSE
-------
Test the next cheapest decisive prerequisite in the 018A nonthermal
string-wall realization program.

Simulation 018A-1 established, at preflight level, that:

1. the exact 017P field content does not itself provide the required wall;
2. a naive same-U(1) relative-phase wall has a finite-energy winding
   obstruction in the tested minimal class;
3. a separate zero-temperature N_DW=1 pseudo-Goldstone wall/string sector
   survives the topology and microscopic wall-profile tests;
4. its wall tension and thickness close to finite Q, N, and R scales;
5. the scale-matching result is robust over the tested +/-10 percent lattice.

However, 018A-1 did NOT prove that the separate wall's boundary string binds
to the literature-backed 017P gauged superconducting string.

This file attacks that missing junction prerequisite before a full 2D
string-wall or drum PDE is attempted.

SCIENTIFIC QUESTION
-------------------
Can a minimal local, gauge-invariant, zero-temperature interaction make the
N_DW=1 wall's boundary-string core energetically prefer overlap with the 017P
gauged superconducting-string core while:

- keeping the vacuum potential bounded;
- preserving the reconstructed 017P straight-string solution;
- retaining physical characteristic speeds;
- retaining the published thin-string extrinsic stability criterion in a
  non-marginal neighborhood;
- avoiding any thermal support sector?

MODEL
-----
The 017P rim is reconstructed from the set-G gauged superconducting-string
model used in the project journal.

The straight-string fields are

    phi = f(r) exp(i theta)

    sigma = s(r) exp[i(omega t + k z)]

with azimuthal gauge potential A_theta(r).

The 017P radial equations are

    f'' + f'/r
      - [
          lambda_phi/2 (f^2 - eta_phi^2)
          + beta s^2
          + (1 - g A_theta)^2/r^2
        ] f
      = 0

    s'' + s'/r
      - [
          lambda_sigma/2 (s^2 - eta_sigma^2)
          + beta f^2
          - chi
        ] s
      = 0

    A_theta'' - A_theta'/r
      + 2 g f^2 (1 - g A_theta)
      = 0

where

    chi = omega^2 - k^2.

The additional nonthermal wall sector from 018A-1 is locally represented near
its boundary-string core by

    A = rho(r) exp(i theta) / sqrt(2).

The complete explicit-breaking term that produces the wall is NOT included in
this radial core calculation because the actual wall makes the junction
two-dimensional and nonaxisymmetric.

This is deliberate.

The radial calculation is only a prerequisite test of whether the two string
cores can bind in the inner region before paying for the true 2D junction.

The 018A-1 hierarchy is

    m_A / m_r = 0.1

so there is a scale interval in which the string core can be examined before
the full wall geometry dominates.

CORE POTENTIAL
--------------
Use

    V_A
      =
      lambda_A/4 (rho^2 - F^2)^2

inside the radial core approximation.

The local gauge-invariant overlap interaction is defined explicitly as

    V_J
      =
      -kappa/4
      (f^2 - eta_phi^2)
      (rho^2 - F^2).

This sign lowers the local potential when both order parameters are suppressed
in the same core.

Because the quartic part is

    V_4
      =
      1/4 [
          lambda_phi f^4
          + lambda_A rho^4
          - kappa f^2 rho^2
      ],

boundedness requires

    kappa^2
      <
      4 lambda_phi lambda_A.

Define

    kappa_fraction
      =
      kappa /
      (2 sqrt(lambda_phi lambda_A)).

The healthy open interval is therefore

    0 <= kappa_fraction < 1.

The same inequality also makes the radial vacuum Hessian positive definite.

COUPLED CORE EQUATIONS
----------------------
With the normalization above, the f equation becomes

    f'' + f'/r
      - [
          lambda_phi/2 (f^2 - 1)
          + beta s^2
          + (1 - g A_theta)^2/r^2
          - kappa/4 (rho^2 - F^2)
        ] f
      = 0

and the new rho equation is

    rho'' + rho'/r
      - rho/r^2
      - [
          lambda_A (rho^2 - F^2)
          - kappa/2 (f^2 - 1)
        ] rho
      = 0.

The s and gauge equations retain their 017P form but respond indirectly
through the changed f profile.

BOUNDARY CONDITIONS
-------------------
Near r=0:

    f = 0
    A_theta = 0
    rho = 0
    s' = 0

At the numerical outer boundary:

    f -> 1
    s -> 0
    A_theta -> 1/g
    rho -> F.

BINDING OBSERVABLES
-------------------
The primary local binding quantity is the difference in the transverse
worldsheet action A(chi) between:

1. the interacting co-centered composite;
2. the separated-string reference.

At kappa=0 the two sectors decouple, so their co-centered numerical solution
is energetically equivalent to placing them infinitely far apart within this
local transverse approximation.

Thus

    Delta A_bind
      =
      A_composite(kappa)
      - A_separated.

A negative value means overlap is energetically preferred at fixed chi.

A second diagnostic uses the same fixed-charge thin-string energy relation
already used by 017P:

    E_string / Q
      =
      A ell
      +
      2 / (Sigma_2 ell).

At the journaled 017P ell, define

    Delta(E/Q)_bind

relative to the kappa=0 reference.

A negative value is a stronger fixed-charge thin-string binding preflight.

Neither quantity is a complete proof of a stable curved wall-loaded vorton.

GLOBAL-STRING INFRARED TAIL
---------------------------
The separate N_DW=1 wall sector has a global-string-like phase gradient close
to its core.

The true explicit breaking cuts the logarithmic tail off at approximately

    r_IR ~ 1/m_A.

For total-EOS health diagnostics this file adds the leading unresolved tail

    Delta A_tail
      =
      pi F^2 ln(r_IR / r_max)

when r_max < r_IR.

This tail cancels from the local binding-energy subtraction to leading order.

017P RECONSTRUCTION REQUIREMENT
-------------------------------
Before interpreting the new coupling, the kappa=0 calculation must reproduce
the journaled 017P selected-point values

    chi       = 0.00475
    Sigma_2   = 1.054410621125
    A_string  = 10.02499735504.

Failure of that reconstruction invalidates the extension run.

EOS HEALTH
----------
The coupled effective action remains a function of chi.

Because the added A sector has no explicit chi dependence, the envelope
identity should remain

    dA/dchi
      =
      -Sigma_2.

The thin-string characteristic speeds are evaluated as

    c_T^2
      =
      1 /
      (1 + 2 chi Sigma_2/A)

and

    c_L^2
      =
      1 /
      (1 + 2 chi Sigma_2'/Sigma_2).

Physical preflight requires

    0 < c_T^2 <= 1
    0 < c_L^2 <= 1.

EXTRINSIC STABILITY CHECK
-------------------------
For m = 2,...,40 use the published cubic coefficients

    a0 =
      2 (c_L^2 - c_T^2) (m^2 - 1) m

    a1 =
      4 c_T^2 (1 - c_L^2) (m^2 - 1)
      - (1 + c_T^2)(c_L^2 - c_T^2)(m^2 + 1)

    a2 =
      2 c_T^2 [
          c_L^2 - c_T^2
          - 2(1 - c_L^2 c_T^2)
      ] m

    a3 =
      c_T^2 (1 + c_T^2)(1 - c_L^2 c_T^2).

The cubic discriminant is evaluated directly and its roots are independently
checked.

A tested point is classified stable only when all tested derivative steps give
positive discriminants and real roots.

This deliberately avoids promoting a coupling sitting on a numerical
stability boundary.

BLIND WILDCARD NUMBERS
----------------------
The user supplied the numbers

    1.6
    1.875
    3.125
    0.625
    5

as a blind wildcard family.

They have NO privileged physical status.

They are tested only after the main physically motivated scan.

If interpreted directly as kappa_fraction, values >=1 violate the proven
quartic boundedness condition and are recorded as rejected controls.

For a bounded wildcard variant, values x>1 are mapped to 1/x while values
already in [0,1) are retained.

This creates extra blind checks without allowing numerology to determine the
main parameter search.

UNITS
-----
Natural units and the dimensionless field normalization of the 017P
straight-string model are used.

No SI device claim is inferred.

NUMERICAL METHOD
----------------
- scipy.solve_bvp for the coupled radial Euler-Lagrange equations;
- continuation in kappa;
- direct quadrature of A, Sigma_2, and energy terms;
- baseline reconstruction against the journaled 017P solution;
- domain-size convergence for the selected interior coupling;
- multiple backward-difference scales for c_L and the variational identity;
- independent cubic discriminant and polynomial-root stability checks.

PRIMARY PROMOTION CONDITION
---------------------------
This subgate is green only if there exists a non-marginal kappa interval with:

    BOUNDED_VACUUM=YES
    COUPLED_BVP=PASS
    DELTA_A_BIND<0
    DELTA_FIXED_CHARGE_ENERGY_PROXY<0
    CT2_PHYSICAL=YES
    CL2_PHYSICAL=YES
    EXTRINSIC_M2_TO_M40=PASS

and the selected interior point preserves the signs under domain and
finite-difference variation.

FALSIFIER
---------
Reject this particular core-binding interaction if:

- every allowed kappa gives nonbinding or unbound cores;
- binding requires kappa at or beyond the quartic boundedness limit;
- the superconducting condensate or EOS becomes unhealthy before binding;
- the known thin-string stability criterion is lost throughout the binding
  region;
- domain refinement reverses the binding sign.

LIMITATIONS
-----------
Even a green result does NOT establish:

- the actual 2D string-wall junction;
- the explicit-breaking wall inside this radial core BVP;
- complete wall/junction stress-energy;
- full finite-payload gravity after the junction;
- full nonaxisymmetric field stability;
- the complete finite-thickness drum-vorton solution;
- nonlinear Einstein-matter consistency;
- practical energy scaling;
- a practical antigravity device.

A green result only justifies the next calculation:

    TRUE_2D_STRING_WALL_JUNCTION_WITH_EXPLICIT_BREAKING

followed by complete thin-composite gravitational bookkeeping.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018A_CORE_BINDING_PREFLIGHT
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from scipy.integrate import simpson
from scipy.integrate import solve_bvp


# ============================================================================
# 017P set-G field parameters.
# ============================================================================

LAMBDA_PHI = 1.0
LAMBDA_SIGMA = 900.0
ETA_PHI = 1.0
ETA_SIGMA = 0.1825
BETA = 20.0

# Published/project set-G gauge ratio:
#
#     G = g / g_BPS = 0.2
#
# with
#
#     g_BPS^2 = lambda_phi / 2
#
G_RATIO = 0.2
GAUGE_G = (
    G_RATIO
    *
    math.sqrt(
        LAMBDA_PHI / 2.0
    )
)

VORTEX_WINDING = 1


# ============================================================================
# Journaled 017P selected point.
# ============================================================================

CHI_SELECTED = 0.004750000000

SIGMA2_JOURNAL = 1.054410621125
A_STRING_JOURNAL = 10.02499735504

Q_OVER_N_JOURNAL = 6.628230560688
ELL_JOURNAL = 0.4257542346286

OMEGA_JOURNAL = 2.227569443362
K_JOURNAL = 2.226503003591

CT2_JOURNAL = 0.9990018050154
CL2_JOURNAL = 0.9930155006037


# ============================================================================
# 018A-1 nonthermal wall/string parameters.
# ============================================================================

F_PHASE = 0.075
MASS_HIERARCHY = 10.0

M_A = (
    F_PHASE
    /
    MASS_HIERARCHY
)

M_R = F_PHASE

# This is inherited from the full 018A-1 wall potential.
#
# The explicit-breaking term shifts the exact radial mass slightly.
# In the U(1)-symmetric inner-core approximation used here:
#
#     m_r^2 ~ 2 lambda_A F^2
#
# The error induced by dropping the explicit breaking in the core BVP is
# controlled by (m_A/m_r)^2 = 0.01 at the selected point.
LAMBDA_A = (
    M_R * M_R
    -
    M_A * M_A
) / (
    2.0
    *
    F_PHASE
    *
    F_PHASE
)

IR_CUTOFF_RADIUS = (
    1.0
    /
    M_A
)


# ============================================================================
# Junction-coupling normalization.
# ============================================================================

# For
#
#   V4 =
#   1/4 [
#       lambda_phi f^4
#       + lambda_A rho^4
#       - kappa f^2 rho^2
#   ]
#
# positivity requires
#
#   kappa^2 < 4 lambda_phi lambda_A.
#
KAPPA_MAX = (
    2.0
    *
    math.sqrt(
        LAMBDA_PHI
        *
        LAMBDA_A
    )
)


# ============================================================================
# Numerics.
# ============================================================================

R0 = 1.0e-4
MAIN_RMAX = 60.0

BVP_TOL = 2.0e-6
BVP_MAX_NODES = 30000

BASE_GRID_POINTS = 850
INTEGRATION_POINTS = 16000

ROOT_IMAG_TOL = 1.0e-8

BASELINE_REL_TOL = 2.0e-5
VARIATIONAL_REL_TOL = 5.0e-4

SELECTED_KAPPA_FRACTION = 0.625


MAIN_BINDING_SCAN = (
    0.00,
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.625,
    0.65,
    0.70,
    0.725,
    0.75,
    0.80,
    0.90,
    0.975,
)

HEALTH_SCAN = (
    0.40,
    0.50,
    0.60,
    0.625,
    0.65,
    0.70,
    0.75,
    0.80,
)

DERIVATIVE_STEPS = (
    0.00025,
    0.00050,
    0.00075,
)

DOMAIN_SCAN = (
    45.0,
    60.0,
    80.0,
)

BLIND_WILDCARD_VALUES = (
    1.6,
    1.875,
    3.125,
    0.625,
    5.0,
)


@dataclass
class SolutionDiagnostics:
    """Integrated diagnostics for one coupled straight-string solution."""

    chi: float
    kappa_fraction: float
    kappa: float
    rmax: float

    sigma2: float
    sigma4: float

    a_original: float
    a_global_core: float
    a_cross: float
    a_total_radial: float
    a_tail: float
    a_total_ir: float

    fixed_charge_energy_per_q: float

    f_center_slope_proxy: float
    s_center: float
    rho_half_radius: float
    f_half_radius: float

    rms_residual_max: float


def kappa_from_fraction(
    fraction: float,
) -> float:
    """Convert normalized boundedness fraction to kappa."""

    return (
        fraction
        *
        KAPPA_MAX
    )


def quartic_margin(
    fraction: float,
) -> float:
    """Return normalized positive-definiteness margin 1-fraction^2."""

    return (
        1.0
        -
        fraction * fraction
    )


def initial_guess(
    r: np.ndarray,
) -> np.ndarray:
    """Build a smooth initial guess for all four field sectors."""

    f = np.tanh(r)
    fp = 1.0 / np.cosh(r) ** 2

    s = (
        0.32
        *
        np.exp(
            -0.15 * r
        )
    )

    sp = (
        -0.15
        *
        s
    )

    gauge = (
        1.0
        /
        GAUGE_G
        *
        (
            1.0
            -
            np.exp(
                -0.2
                *
                r
                *
                r
            )
        )
    )

    gauge_p = (
        1.0
        /
        GAUGE_G
        *
        (
            0.4
            *
            r
            *
            np.exp(
                -0.2
                *
                r
                *
                r
            )
        )
    )

    rho = (
        F_PHASE
        *
        np.tanh(
            M_R * r
        )
    )

    rho_p = (
        F_PHASE
        *
        M_R
        /
        np.cosh(
            M_R * r
        ) ** 2
    )

    return np.vstack(
        [
            f,
            fp,
            s,
            sp,
            gauge,
            gauge_p,
            rho,
            rho_p,
        ]
    )


def solve_composite(
    *,
    chi: float,
    kappa_fraction: float,
    rmax: float,
    previous=None,
):
    """Solve the coupled radial core BVP."""

    if not (
        0.0
        <=
        kappa_fraction
        <
        1.0
    ):
        raise ValueError(
            "kappa_fraction must satisfy 0 <= fraction < 1"
        )

    kappa = kappa_from_fraction(
        kappa_fraction
    )

    r = np.geomspace(
        R0,
        rmax,
        BASE_GRID_POINTS,
    )

    if previous is None:
        y_guess = initial_guess(
            r
        )
    else:
        y_guess = previous.sol(
            r
        )

    def ode(
        rr: np.ndarray,
        y: np.ndarray,
    ) -> np.ndarray:
        (
            f,
            fp,
            s,
            sp,
            gauge,
            gauge_p,
            rho,
            rho_p,
        ) = y

        rr_safe = np.maximum(
            rr,
            1.0e-12,
        )

        angular = (
            (
                VORTEX_WINDING
                -
                GAUGE_G
                *
                gauge
            )
            /
            rr_safe
        ) ** 2

        f_pp = (
            -fp
            /
            rr_safe
            +
            (
                0.5
                *
                LAMBDA_PHI
                *
                (
                    f * f
                    -
                    ETA_PHI
                    *
                    ETA_PHI
                )
                +
                BETA
                *
                s
                *
                s
                +
                angular
                -
                0.25
                *
                kappa
                *
                (
                    rho * rho
                    -
                    F_PHASE
                    *
                    F_PHASE
                )
            )
            *
            f
        )

        s_pp = (
            -sp
            /
            rr_safe
            +
            (
                0.5
                *
                LAMBDA_SIGMA
                *
                (
                    s * s
                    -
                    ETA_SIGMA
                    *
                    ETA_SIGMA
                )
                +
                BETA
                *
                f
                *
                f
                -
                chi
            )
            *
            s
        )

        gauge_pp = (
            gauge_p
            /
            rr_safe
            -
            2.0
            *
            GAUGE_G
            *
            f
            *
            f
            *
            (
                VORTEX_WINDING
                -
                GAUGE_G
                *
                gauge
            )
        )

        rho_pp = (
            -rho_p
            /
            rr_safe
            +
            rho
            /
            (
                rr_safe
                *
                rr_safe
            )
            +
            (
                LAMBDA_A
                *
                (
                    rho * rho
                    -
                    F_PHASE
                    *
                    F_PHASE
                )
                -
                0.5
                *
                kappa
                *
                (
                    f * f
                    -
                    ETA_PHI
                    *
                    ETA_PHI
                )
            )
            *
            rho
        )

        return np.vstack(
            [
                fp,
                f_pp,
                sp,
                s_pp,
                gauge_p,
                gauge_pp,
                rho_p,
                rho_pp,
            ]
        )

    def bc(
        ya: np.ndarray,
        yb: np.ndarray,
    ) -> np.ndarray:
        return np.array(
            [
                ya[0],
                ya[3],
                ya[4],
                ya[6],
                yb[0] - ETA_PHI,
                yb[2],
                yb[4]
                -
                VORTEX_WINDING
                /
                GAUGE_G,
                yb[6] - F_PHASE,
            ]
        )

    solution = solve_bvp(
        ode,
        bc,
        r,
        y_guess,
        tol=BVP_TOL,
        max_nodes=BVP_MAX_NODES,
    )

    if solution.status != 0:
        raise RuntimeError(
            "BVP failed: "
            f"{solution.message}"
        )

    return solution


def first_radius_at_fraction(
    r: np.ndarray,
    field: np.ndarray,
    target: float,
) -> float:
    """Estimate the first radius at which a monotone profile reaches target."""

    indices = np.where(
        field
        >=
        target
    )[0]

    if len(indices) == 0:
        return math.nan

    i = int(
        indices[0]
    )

    if i == 0:
        return float(
            r[0]
        )

    x0 = r[i - 1]
    x1 = r[i]

    y0 = field[i - 1]
    y1 = field[i]

    if y1 == y0:
        return float(
            x1
        )

    weight = (
        target - y0
    ) / (
        y1 - y0
    )

    return float(
        x0
        +
        weight
        *
        (
            x1 - x0
        )
    )


def diagnose(
    solution,
    *,
    chi: float,
    kappa_fraction: float,
    rmax: float,
) -> SolutionDiagnostics:
    """Integrate worldsheet quantities and binding-relevant contributions."""

    kappa = kappa_from_fraction(
        kappa_fraction
    )

    r = np.linspace(
        R0,
        rmax,
        INTEGRATION_POINTS,
    )

    (
        f,
        fp,
        s,
        sp,
        gauge,
        gauge_p,
        rho,
        rho_p,
    ) = solution.sol(
        r
    )

    sigma2 = float(
        2.0
        *
        math.pi
        *
        simpson(
            r
            *
            s
            *
            s,
            x=r,
        )
    )

    sigma4 = float(
        2.0
        *
        math.pi
        *
        simpson(
            r
            *
            s**4,
            x=r,
        )
    )

    e_phi = (
        fp * fp
        +
        (
            (
                VORTEX_WINDING
                -
                GAUGE_G
                *
                gauge
            )
            /
            r
        ) ** 2
        *
        f
        *
        f
        +
        0.5
        *
        (
            gauge_p
            /
            r
        ) ** 2
        +
        0.25
        *
        LAMBDA_PHI
        *
        (
            f * f
            -
            ETA_PHI
            *
            ETA_PHI
        ) ** 2
    )

    e_sigma_transverse = (
        sp * sp
        +
        0.25
        *
        LAMBDA_SIGMA
        *
        (
            s * s
            -
            ETA_SIGMA
            *
            ETA_SIGMA
        ) ** 2
        +
        BETA
        *
        f
        *
        f
        *
        s
        *
        s
        -
        0.25
        *
        LAMBDA_SIGMA
        *
        ETA_SIGMA**4
        -
        chi
        *
        s
        *
        s
    )

    e_global = (
        0.5
        *
        rho_p
        *
        rho_p
        +
        0.5
        *
        rho
        *
        rho
        /
        (
            r * r
        )
        +
        0.25
        *
        LAMBDA_A
        *
        (
            rho * rho
            -
            F_PHASE
            *
            F_PHASE
        ) ** 2
    )

    e_cross = (
        -0.25
        *
        kappa
        *
        (
            f * f
            -
            ETA_PHI
            *
            ETA_PHI
        )
        *
        (
            rho * rho
            -
            F_PHASE
            *
            F_PHASE
        )
    )

    factor = (
        2.0
        *
        math.pi
        *
        r
    )

    a_original = float(
        simpson(
            factor
            *
            (
                e_phi
                +
                e_sigma_transverse
            ),
            x=r,
        )
    )

    a_global_core = float(
        simpson(
            factor
            *
            e_global,
            x=r,
        )
    )

    a_cross = float(
        simpson(
            factor
            *
            e_cross,
            x=r,
        )
    )

    a_total_radial = (
        a_original
        +
        a_global_core
        +
        a_cross
    )

    if (
        rmax
        <
        IR_CUTOFF_RADIUS
    ):
        a_tail = (
            math.pi
            *
            F_PHASE
            *
            F_PHASE
            *
            math.log(
                IR_CUTOFF_RADIUS
                /
                rmax
            )
        )
    else:
        a_tail = 0.0

    a_total_ir = (
        a_total_radial
        +
        a_tail
    )

    fixed_charge_energy_per_q = (
        a_total_ir
        *
        ELL_JOURNAL
        +
        2.0
        /
        (
            sigma2
            *
            ELL_JOURNAL
        )
    )

    f_half_radius = (
        first_radius_at_fraction(
            r,
            f,
            0.5
            *
            ETA_PHI,
        )
    )

    rho_half_radius = (
        first_radius_at_fraction(
            r,
            rho,
            0.5
            *
            F_PHASE,
        )
    )

    f_center_slope_proxy = float(
        fp[0]
    )

    s_center = float(
        s[0]
    )

    return SolutionDiagnostics(
        chi=chi,
        kappa_fraction=kappa_fraction,
        kappa=kappa,
        rmax=rmax,
        sigma2=sigma2,
        sigma4=sigma4,
        a_original=a_original,
        a_global_core=a_global_core,
        a_cross=a_cross,
        a_total_radial=a_total_radial,
        a_tail=a_tail,
        a_total_ir=a_total_ir,
        fixed_charge_energy_per_q=fixed_charge_energy_per_q,
        f_center_slope_proxy=f_center_slope_proxy,
        s_center=s_center,
        rho_half_radius=rho_half_radius,
        f_half_radius=f_half_radius,
        rms_residual_max=float(
            np.max(
                solution.rms_residuals
            )
        ),
    )


def cubic_stability(
    c_t2: float,
    c_l2: float,
) -> dict[str, float | bool]:
    """Evaluate m=2...40 discriminants and direct polynomial roots."""

    min_discriminant = math.inf
    max_root_imag = 0.0
    worst_mode = -1

    for m in range(
        2,
        41,
    ):
        m2 = float(
            m * m
        )

        a0 = (
            2.0
            *
            (
                c_l2
                -
                c_t2
            )
            *
            (
                m2
                -
                1.0
            )
            *
            m
        )

        a1 = (
            4.0
            *
            c_t2
            *
            (
                1.0
                -
                c_l2
            )
            *
            (
                m2
                -
                1.0
            )
            -
            (
                1.0
                +
                c_t2
            )
            *
            (
                c_l2
                -
                c_t2
            )
            *
            (
                m2
                +
                1.0
            )
        )

        a2 = (
            2.0
            *
            c_t2
            *
            (
                c_l2
                -
                c_t2
                -
                2.0
                *
                (
                    1.0
                    -
                    c_l2
                    *
                    c_t2
                )
            )
            *
            m
        )

        a3 = (
            c_t2
            *
            (
                1.0
                +
                c_t2
            )
            *
            (
                1.0
                -
                c_l2
                *
                c_t2
            )
        )

        discriminant = (
            a1 * a1 * a2 * a2
            -
            4.0
            *
            a1**3
            *
            a3
            -
            4.0
            *
            a0
            *
            a2**3
            -
            27.0
            *
            a0
            *
            a0
            *
            a3
            *
            a3
            +
            18.0
            *
            a0
            *
            a1
            *
            a2
            *
            a3
        )

        if (
            discriminant
            <
            min_discriminant
        ):
            min_discriminant = float(
                discriminant
            )
            worst_mode = m

        roots = np.roots(
            [
                a3,
                a2,
                a1,
                a0,
            ]
        )

        root_imag = float(
            np.max(
                np.abs(
                    np.imag(
                        roots
                    )
                )
            )
        )

        max_root_imag = max(
            max_root_imag,
            root_imag,
        )

    passed = (
        min_discriminant
        >
        0.0
        and
        max_root_imag
        <=
        ROOT_IMAG_TOL
    )

    return {
        "pass": passed,
        "min_discriminant": (
            min_discriminant
        ),
        "max_root_imag": (
            max_root_imag
        ),
        "worst_mode": float(
            worst_mode
        ),
    }


def health_at_step(
    *,
    fraction: float,
    h: float,
    diag0: SolutionDiagnostics,
    diag1: SolutionDiagnostics,
    diag2: SolutionDiagnostics,
) -> dict[str, float | bool]:
    """Compute EOS derivatives and stability from one backward-difference step."""

    sigma2_prime = (
        3.0
        *
        diag0.sigma2
        -
        4.0
        *
        diag1.sigma2
        +
        diag2.sigma2
    ) / (
        2.0
        *
        h
    )

    a_prime = (
        3.0
        *
        diag0.a_total_ir
        -
        4.0
        *
        diag1.a_total_ir
        +
        diag2.a_total_ir
    ) / (
        2.0
        *
        h
    )

    variational_relerr = (
        abs(
            a_prime
            +
            diag0.sigma2
        )
        /
        max(
            abs(
                diag0.sigma2
            ),
            1.0e-30,
        )
    )

    c_t2 = (
        1.0
        /
        (
            1.0
            +
            2.0
            *
            CHI_SELECTED
            *
            diag0.sigma2
            /
            diag0.a_total_ir
        )
    )

    c_l2 = (
        1.0
        /
        (
            1.0
            +
            2.0
            *
            CHI_SELECTED
            *
            sigma2_prime
            /
            diag0.sigma2
        )
    )

    physical_speeds = (
        0.0
        <
        c_t2
        <=
        1.0
        and
        0.0
        <
        c_l2
        <=
        1.0
    )

    stability = cubic_stability(
        c_t2,
        c_l2,
    )

    passed = (
        physical_speeds
        and
        variational_relerr
        <
        VARIATIONAL_REL_TOL
        and
        bool(
            stability[
                "pass"
            ]
        )
    )

    return {
        "pass": passed,
        "fraction": fraction,
        "h": h,
        "sigma2_prime": (
            sigma2_prime
        ),
        "a_prime": (
            a_prime
        ),
        "variational_relerr": (
            variational_relerr
        ),
        "c_t2": c_t2,
        "c_l2": c_l2,
        "min_discriminant": (
            float(
                stability[
                    "min_discriminant"
                ]
            )
        ),
        "max_root_imag": (
            float(
                stability[
                    "max_root_imag"
                ]
            )
        ),
        "worst_mode": (
            float(
                stability[
                    "worst_mode"
                ]
            )
        ),
    }


def solve_and_diagnose(
    *,
    chi: float,
    fraction: float,
    rmax: float,
    previous=None,
) -> tuple[object, SolutionDiagnostics]:
    """Convenience wrapper for BVP solve plus integration."""

    solution = solve_composite(
        chi=chi,
        kappa_fraction=fraction,
        rmax=rmax,
        previous=previous,
    )

    diagnostics = diagnose(
        solution,
        chi=chi,
        kappa_fraction=fraction,
        rmax=rmax,
    )

    return (
        solution,
        diagnostics,
    )


def print_binding_row(
    *,
    label: str,
    diag: SolutionDiagnostics,
    baseline: SolutionDiagnostics,
) -> dict[str, float | bool]:
    """Print and return binding diagnostics versus separated reference."""

    delta_a = (
        diag.a_total_ir
        -
        baseline.a_total_ir
    )

    delta_fixed_charge = (
        diag.fixed_charge_energy_per_q
        -
        baseline.fixed_charge_energy_per_q
    )

    sigma2_shift = (
        diag.sigma2
        /
        baseline.sigma2
        -
        1.0
    )

    bound = (
        diag.kappa_fraction
        >=
        0.0
        and
        diag.kappa_fraction
        <
        1.0
    )

    binding = (
        delta_a
        <
        0.0
        and
        delta_fixed_charge
        <
        0.0
    )

    print(
        f"{label} "
        f"KF={diag.kappa_fraction:.9f} "
        f"KAPPA={diag.kappa:.12e} "
        f"QUARTIC_MARGIN={quartic_margin(diag.kappa_fraction):.9e} "
        f"DELTA_A_BIND={delta_a:+.12e} "
        f"DELTA_FIXEDQ_EQ={delta_fixed_charge:+.12e} "
        f"SIGMA2_SHIFT={sigma2_shift:+.9e} "
        f"A_CROSS={diag.a_cross:+.12e} "
        f"F_HALF_R={diag.f_half_radius:.9f} "
        f"RHO_HALF_R={diag.rho_half_radius:.9f} "
        f"BOUND={'YES' if bound else 'NO'} "
        f"BINDING={'YES' if binding else 'NO'}"
    )

    return {
        "bound": bound,
        "binding": binding,
        "delta_a": delta_a,
        "delta_fixed_charge": (
            delta_fixed_charge
        ),
        "sigma2_shift": (
            sigma2_shift
        ),
    }


def main() -> None:
    """Execute the complete 018A-2 core-binding preflight."""

    print(
        "=== ANTIGRAVITY_RESEARCH 018A-2 ==="
    )

    print(
        "QUESTION="
        "CAN_THE_SEPARATE_NDW1_BOUNDARY_STRING_BIND_TO_THE_017P_GAUGED_STRING_CORE"
    )

    print(
        "THIS_IS_TRUE_2D_JUNCTION_SOLUTION=NO"
    )

    print(
        "THIS_IS_RADIAL_CORE_BINDING_PREFLIGHT=YES"
    )

    print(
        "EXPLICIT_WALL_BREAKING_IN_RADIAL_CORE_BVP="
        "OMITTED_BY_CONTROLLED_INNER_CORE_APPROXIMATION"
    )

    print(
        "FULL_018A_GATE=NOT_YET_GREEN"
    )

    print(
        "\n=== MODEL PARAMETERS ==="
    )

    print(
        f"GAUGE_G={GAUGE_G:.15e}"
    )

    print(
        f"F_PHASE={F_PHASE:.15e}"
    )

    print(
        f"M_A={M_A:.15e}"
    )

    print(
        f"M_R={M_R:.15e}"
    )

    print(
        f"M_A_OVER_M_R={M_A / M_R:.15e}"
    )

    print(
        f"LAMBDA_A={LAMBDA_A:.15e}"
    )

    print(
        f"KAPPA_MAX_OPEN_BOUND={KAPPA_MAX:.15e}"
    )

    print(
        f"IR_CUTOFF_RADIUS={IR_CUTOFF_RADIUS:.15e}"
    )

    assert (
        LAMBDA_A
        >
        0.0
    )

    assert (
        abs(
            OMEGA_JOURNAL
            *
            OMEGA_JOURNAL
            -
            K_JOURNAL
            *
            K_JOURNAL
            -
            CHI_SELECTED
        )
        <
        1.0e-10
    )

    print(
        "\n=== 017P + DECOUPLED GLOBAL STRING BASELINE ==="
    )

    base_solution, baseline = (
        solve_and_diagnose(
            chi=CHI_SELECTED,
            fraction=0.0,
            rmax=MAIN_RMAX,
        )
    )

    a_relerr = (
        abs(
            baseline.a_original
            -
            A_STRING_JOURNAL
        )
        /
        A_STRING_JOURNAL
    )

    sigma2_relerr = (
        abs(
            baseline.sigma2
            -
            SIGMA2_JOURNAL
        )
        /
        SIGMA2_JOURNAL
    )

    print(
        f"RECONSTRUCTED_A_STRING={baseline.a_original:.15e}"
    )

    print(
        f"JOURNAL_A_STRING={A_STRING_JOURNAL:.15e}"
    )

    print(
        f"A_STRING_RELERR={a_relerr:.15e}"
    )

    print(
        f"RECONSTRUCTED_SIGMA2={baseline.sigma2:.15e}"
    )

    print(
        f"JOURNAL_SIGMA2={SIGMA2_JOURNAL:.15e}"
    )

    print(
        f"SIGMA2_RELERR={sigma2_relerr:.15e}"
    )

    print(
        f"GLOBAL_CORE_A_RMAX60={baseline.a_global_core:.15e}"
    )

    print(
        f"GLOBAL_TAIL_TO_1_OVER_MA={baseline.a_tail:.15e}"
    )

    print(
        f"SEPARATED_TOTAL_A_WITH_IR_TAIL={baseline.a_total_ir:.15e}"
    )

    baseline_reconstruction_pass = (
        a_relerr
        <
        BASELINE_REL_TOL
        and
        sigma2_relerr
        <
        BASELINE_REL_TOL
    )

    print(
        "017P_BASELINE_RECONSTRUCTION="
        f"{'PASS' if baseline_reconstruction_pass else 'FAIL'}"
    )

    print(
        "\n=== MAIN PHYSICALLY MOTIVATED BINDING SCAN ==="
    )

    main_records: dict[
        float,
        tuple[
            object,
            SolutionDiagnostics,
            dict[str, float | bool],
        ],
    ] = {}

    previous = base_solution

    for fraction in MAIN_BINDING_SCAN:
        if fraction == 0.0:
            solution = base_solution
            diag = baseline
        else:
            solution, diag = (
                solve_and_diagnose(
                    chi=CHI_SELECTED,
                    fraction=fraction,
                    rmax=MAIN_RMAX,
                    previous=previous,
                )
            )

        record = print_binding_row(
            label="MAIN",
            diag=diag,
            baseline=baseline,
        )

        main_records[
            float(
                fraction
            )
        ] = (
            solution,
            diag,
            record,
        )

        previous = solution

    binding_fractions = [
        fraction
        for fraction, (
            _,
            _,
            record,
        )
        in main_records.items()
        if fraction > 0.0
        and bool(
            record["binding"]
        )
    ]

    print(
        "MAIN_BINDING_PASS_COUNT="
        f"{len(binding_fractions)}"
    )

    print(
        "MAIN_BINDING_TEST_COUNT="
        f"{len(MAIN_BINDING_SCAN) - 1}"
    )

    if binding_fractions:
        print(
            "MAIN_BINDING_MIN_KF="
            f"{min(binding_fractions):.9f}"
        )

        print(
            "MAIN_BINDING_MAX_TESTED_KF="
            f"{max(binding_fractions):.9f}"
        )

    print(
        "\n=== EOS HEALTH + EXTRINSIC STABILITY SCAN ==="
    )

    health_summary: dict[
        float,
        bool,
    ] = {}

    health_details: dict[
        float,
        list[
            dict[str, float | bool]
        ],
    ] = {}

    for fraction in HEALTH_SCAN:
        solution0, diag0, _ = (
            main_records[
                float(
                    fraction
                )
            ]
        )

        needed_chi = set()

        for h in DERIVATIVE_STEPS:
            needed_chi.add(
                CHI_SELECTED
                -
                h
            )

            needed_chi.add(
                CHI_SELECTED
                -
                2.0
                *
                h
            )

        solved: dict[
            float,
            tuple[
                object,
                SolutionDiagnostics,
            ],
        ] = {
            CHI_SELECTED: (
                solution0,
                diag0,
            )
        }

        previous_chi_solution = (
            solution0
        )

        for chi in sorted(
            needed_chi,
            reverse=True,
        ):
            sol, diag = (
                solve_and_diagnose(
                    chi=chi,
                    fraction=fraction,
                    rmax=MAIN_RMAX,
                    previous=previous_chi_solution,
                )
            )

            solved[
                chi
            ] = (
                sol,
                diag,
            )

            previous_chi_solution = (
                sol
            )

        step_results = []

        for h in DERIVATIVE_STEPS:
            diag1 = solved[
                CHI_SELECTED
                -
                h
            ][1]

            diag2 = solved[
                CHI_SELECTED
                -
                2.0
                *
                h
            ][1]

            result = health_at_step(
                fraction=fraction,
                h=h,
                diag0=diag0,
                diag1=diag1,
                diag2=diag2,
            )

            step_results.append(
                result
            )

            print(
                "HEALTH "
                f"KF={fraction:.9f} "
                f"H={h:.9e} "
                f"CT2={float(result['c_t2']):.12f} "
                f"CL2={float(result['c_l2']):.12f} "
                f"VAR_RELERR={float(result['variational_relerr']):.6e} "
                f"MIN_DISC={float(result['min_discriminant']):+.12e} "
                f"WORST_M={int(float(result['worst_mode']))} "
                f"MAX_ROOT_IMAG={float(result['max_root_imag']):.6e} "
                f"PASS={'YES' if bool(result['pass']) else 'NO'}"
            )

        robust = all(
            bool(
                result[
                    "pass"
                ]
            )
            for result
            in step_results
        )

        health_summary[
            float(
                fraction
            )
        ] = robust

        health_details[
            float(
                fraction
            )
        ] = step_results

        print(
            "HEALTH_ROBUST "
            f"KF={fraction:.9f} "
            f"PASS={'YES' if robust else 'NO'}"
        )

    robust_health_fractions = [
        fraction
        for fraction, passed
        in health_summary.items()
        if passed
    ]

    if robust_health_fractions:
        print(
            "MAX_TESTED_ROBUST_HEALTH_KF="
            f"{max(robust_health_fractions):.9f}"
        )
    else:
        print(
            "MAX_TESTED_ROBUST_HEALTH_KF=NONE"
        )

    print(
        "\n=== SELECTED 0.625 DOMAIN CONVERGENCE ==="
    )

    selected_domain_records = []

    for rmax in DOMAIN_SCAN:
        base_sol_domain, base_diag_domain = (
            solve_and_diagnose(
                chi=CHI_SELECTED,
                fraction=0.0,
                rmax=rmax,
            )
        )

        sel_sol_domain, sel_diag_domain = (
            solve_and_diagnose(
                chi=CHI_SELECTED,
                fraction=SELECTED_KAPPA_FRACTION,
                rmax=rmax,
                previous=base_sol_domain,
            )
        )

        delta_a = (
            sel_diag_domain.a_total_ir
            -
            base_diag_domain.a_total_ir
        )

        delta_eq = (
            sel_diag_domain.fixed_charge_energy_per_q
            -
            base_diag_domain.fixed_charge_energy_per_q
        )

        selected_domain_records.append(
            (
                rmax,
                delta_a,
                delta_eq,
            )
        )

        print(
            "DOMAIN "
            f"RMAX={rmax:.1f} "
            f"DELTA_A_BIND={delta_a:+.15e} "
            f"DELTA_FIXEDQ_EQ={delta_eq:+.15e} "
            f"BINDING={'YES' if delta_a < 0.0 and delta_eq < 0.0 else 'NO'}"
        )

    domain_delta_eq = np.array(
        [
            row[2]
            for row
            in selected_domain_records
        ],
        dtype=float,
    )

    reference_abs = max(
        abs(
            domain_delta_eq[
                1
            ]
        ),
        1.0e-30,
    )

    domain_spread = (
        float(
            np.max(
                domain_delta_eq
            )
            -
            np.min(
                domain_delta_eq
            )
        )
        /
        reference_abs
    )

    selected_domain_pass = (
        np.all(
            domain_delta_eq
            <
            0.0
        )
        and
        domain_spread
        <
        0.02
    )

    print(
        f"SELECTED_DOMAIN_REL_SPREAD={domain_spread:.15e}"
    )

    print(
        "SELECTED_DOMAIN_BINDING="
        f"{'PASS' if selected_domain_pass else 'FAIL'}"
    )

    print(
        "\n=== BLIND USER WILDCARD CONTROLS ==="
    )

    for value in BLIND_WILDCARD_VALUES:
        raw_valid = (
            0.0
            <=
            value
            <
            1.0
        )

        print(
            "WILDCARD_RAW "
            f"VALUE={value:.9f} "
            f"AS_KAPPA_FRACTION="
            f"{'ALLOWED' if raw_valid else 'REJECTED_BY_QUARTIC_BOUNDEDNESS'}"
        )

        if value > 1.0:
            safe_fraction = (
                1.0
                /
                value
            )
            transform = "INVERSE"
        else:
            safe_fraction = value
            transform = "IDENTITY"

        if not (
            0.0
            <=
            safe_fraction
            <
            1.0
        ):
            print(
                "WILDCARD_SAFE "
                f"VALUE={value:.9f} "
                "SKIPPED=YES"
            )
            continue

        key = float(
            safe_fraction
        )

        if key in main_records:
            _, wildcard_diag, _ = (
                main_records[
                    key
                ]
            )
        else:
            wildcard_solution, wildcard_diag = (
                solve_and_diagnose(
                    chi=CHI_SELECTED,
                    fraction=safe_fraction,
                    rmax=MAIN_RMAX,
                    previous=base_solution,
                )
            )

        wildcard_record = (
            print_binding_row(
                label=(
                    "WILDCARD_SAFE"
                    f"[SOURCE={value:.9f},TRANSFORM={transform}]"
                ),
                diag=wildcard_diag,
                baseline=baseline,
            )
        )

        print(
            "WILDCARD_INTERPRETATION="
            "BLIND_CONTROL_ONLY_NOT_PHYSICS_PRIOR"
        )

    print(
        "\n=== 018A-2 DECISION ==="
    )

    selected_binding_record = (
        main_records[
            SELECTED_KAPPA_FRACTION
        ][2]
    )

    selected_health_pass = bool(
        health_summary.get(
            SELECTED_KAPPA_FRACTION,
            False,
        )
    )

    selected_quartic_pass = (
        quartic_margin(
            SELECTED_KAPPA_FRACTION
        )
        >
        0.0
    )

    selected_binding_pass = bool(
        selected_binding_record[
            "binding"
        ]
    )

    overall_pass = (
        baseline_reconstruction_pass
        and
        selected_quartic_pass
        and
        selected_binding_pass
        and
        selected_health_pass
        and
        selected_domain_pass
    )

    print(
        "017P_BASELINE_RECONSTRUCTION="
        f"{'PASS' if baseline_reconstruction_pass else 'FAIL'}"
    )

    print(
        "SELECTED_KAPPA_FRACTION="
        f"{SELECTED_KAPPA_FRACTION:.9f}"
    )

    print(
        "SELECTED_QUARTIC_BOUNDEDNESS="
        f"{'PASS' if selected_quartic_pass else 'FAIL'}"
    )

    print(
        "SELECTED_CORE_BINDING="
        f"{'PASS' if selected_binding_pass else 'FAIL'}"
    )

    print(
        "SELECTED_EOS_AND_EXTRINSIC_HEALTH="
        f"{'PASS' if selected_health_pass else 'FAIL'}"
    )

    print(
        "SELECTED_DOMAIN_CONVERGENCE="
        f"{'PASS' if selected_domain_pass else 'FAIL'}"
    )

    print(
        "018A2_CORE_BINDING_PREFLIGHT="
        f"{'GREEN' if overall_pass else 'RED'}"
    )

    print(
        "TRUE_2D_STRING_WALL_JUNCTION="
        "NOT_YET_SOLVED"
    )

    print(
        "COMPLETE_JUNCTION_STRESS_ENERGY="
        "NOT_YET_SOLVED"
    )

    print(
        "FINITE_PAYLOAD_GRAVITY_AFTER_TRUE_JUNCTION="
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
        "PROJECT_DERIVED_018A_CORE_BINDING_PREFLIGHT"
    )

    if overall_pass:
        print(
            "NEXT="
            "018A3_TRUE_2D_STRING_WALL_JUNCTION_WITH_EXPLICIT_BREAKING_AND_COMPLETE_LINE_STRESS"
        )
    else:
        print(
            "NEXT="
            "AUDIT_OR_REJECT_THIS_JUNCTION_INTERACTION_BEFORE_ANY_2D_ESCALATION"
        )


if __name__ == "__main__":
    main()
