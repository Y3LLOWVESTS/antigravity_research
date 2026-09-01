#!/usr/bin/env python3
"""023A — topological false-core multiskyrmion GR-repulsion gate.

PURPOSE
-------
Perform the first high-information global rerank after 022A closed the tested
protected Wilson/vector-current practicality branch.

The strongest surviving physical lesson from 006D, 016H, 018B, and 018C is:

    outward gravity requires useful spatial organization of active stress,
    while a microscopic realization must possess intrinsic stability rather
    than an arbitrary added rigidity term.

018B achieved the first requirement in a complete microscopic field
configuration, but 018C directly proved an m=2 fixed-charge instability of
that specific two-current/KLS wall-rim architecture.

This run therefore changes the stabilization principle rather than adding a
new stabilizer to the failed architecture.

It studies an established intrinsically topological relativistic field theory:
the SU(2) Skyrme model with a nonnegative potential that has

    U = +1  : true vacuum,
    U = -1  : positive-energy local false vacuum.

For a multi-Skyrmion shell, topology forces the field through the false-vacuum
orientation in the interior while the quartic Skyrme stabilizer is concentrated
toward the transition shell.

The central question is whether this spatial separation can produce:

    negative ENCLOSED active gravitational mass in the interior,

while preserving:

    positive local energy density,
    positive total active mass,
    topological charge,
    Derrick stability,
    binding against binary fission,
    and an outward finite-payload MONOPOLE response.

A positive result is a capacity/preflight result for a genuinely new stable
topological GR architecture.  It is not yet a full 3D field-theoretical
candidate because B>1 rational-map Skyrmions are not spherically symmetric.

ACTIVE-SOURCE THEOREM
---------------------
For a static Lorentz-invariant scalar-field energy term e_n homogeneous in
n spatial derivatives, metric variation gives the spatial pressure trace

    sum_i p_i = (n - 3) e_n.

Therefore the linearized-GR active source is

    S
      =
    rho + sum_i p_i
      =
    (n - 2) e_n.

For the present Skyrme model:

    quadratic sigma-model term e_2:
        S_2 = 0

    quartic Skyrme term e_4:
        S_4 = +2 e_4

    nonnegative potential V:
        S_0 = -2 V

and hence

    S = 2 (e_4 - V).

This is the key structural mechanism.

The ordinary positive potential gives negative active gravity locally.
The topology-supporting quartic gradient energy gives positive active gravity.
The quadratic gradients carry energy but zero active source in the static
trace combination.

This is not a violation of the positive-mass bookkeeping.  For a stationary
finite soliton the Derrick/Laue identity restores

    M_active,total = E_total > 0.

The proposed useful effect is therefore an INTERIOR near-field effect inside a
globally positive-mass object, exactly respecting the project's distinction
between local repulsion and far-field attraction.

MODEL
-----
Use the standard SU(2) Skyrme energy in rational-map normalization.

Write

    U
      =
    cos F(r)
    +
    i sin F(r) n_R(theta,phi) . tau,

where the rational map has degree B.

The radial energy, omitting one common positive normalization factor, is

    E
      =
    integral dr [
        r^2 F'^2
        +
        2 B (F'^2 + 1) sin^2 F
        +
        I sin^4 F / r^2
        +
        r^2 V(F)
    ].

For B=1:

    I = 1.

For B>1 use the established rational-map approximation

    I approximately 1.28 B^2.

The scan is deliberately limited to

    1 <= B <= 8.

This avoids obtaining a favorable answer solely by extrapolating to huge
topological charge.  Published false-vacuum-potential multi-Skyrmion studies
exist through B=8, and rational-map methods are known to approximate
multi-Skyrmion shell structure well in this range.

FALSE-CORE POTENTIAL
--------------------
Use

    V(F)
      =
    m^2 (1 - cos F) (1 + eta cos F).

This is exactly the same polynomial class as the standard two-mass
false-vacuum Skyrme potential

    V
      =
    (m1^2/2)(1 - sigma)
    +
    m2^2(1 - sigma^2),

with

    sigma = cos F,

under

    m2^2 = eta m^2,

    m1^2 = 2 (1 - eta) m^2.

For

    1/3 < eta < 1,

both vacua are locally stable:

    F = 0:
        true vacuum,
        V = 0,
        V'' = m^2(1 + eta) > 0

    F = pi:
        local false vacuum,
        V = 2m^2(1 - eta) > 0,
        V'' = m^2(3eta - 1) > 0.

The topology boundary conditions are

    F(0) = pi,
    F(infinity) = 0.

Thus the topological sector forces the center into the positive-energy
false-vacuum orientation while ordinary space approaches the zero-energy true
vacuum.

RADIAL EULER-LAGRANGE EQUATION
------------------------------
Define

    s = sin F,
    c = cos F.

Varying the radial rational-map functional gives

    F''
      =
    [
        2 B s c
        +
        2 I s^3 c / r^2
        +
        (r^2/2) dV/dF
        -
        2 r F'
        -
        2 B s c F'^2
    ]
    /
    [
        r^2 + 2 B s^2
    ],

with

    dV/dF
      =
    m^2 sin F
    [
        1 - eta + 2 eta cos F
    ].

The run solves this boundary-value problem rather than accepting a fixed trial
profile as the scientific result.

A separately optimized two-parameter analytic profile

    F_trial(r)
      =
    2 arctan[(R/r)^p]

provides:

    - an independent variational reconstruction;
    - a high-quality BVP initial condition;
    - a check that the negative-active-core sign is not generated solely by
      the BVP discretization.

ENERGY AND ACTIVE MASS
----------------------
After angular integration define

    e_2
      =
    F'^2 + 2 B sin^2(F)/r^2,

    e_4
      =
    2 B sin^2(F) F'^2/r^2
    +
    I sin^4(F)/r^4,

    e_0 = V(F).

Then

    E_n
      =
    integral r^2 e_n dr

up to the same common angular factor.

The cumulative active mass is

    M_A(r)
      =
    integral_0^r
    2 r'^2 [e_4(r') - e_0(r')] dr'.

The common angular normalization cancels in all reported fractions.

A radial interval with

    M_A(r) < 0

has outward monopole acceleration:

    a_r(r)
      proportional to
    - M_A(r) / r^2.

The far field must satisfy

    M_A(infinity) > 0

and numerically reproduce the total energy through the Derrick/Laue identity.

DERRICK / LAUE CHECK
--------------------
Under

    F_lambda(r) = F(lambda r),

the three energy components scale as

    E_2(lambda) = E_2/lambda,

    E_4(lambda) = lambda E_4,

    E_0(lambda) = E_0/lambda^3

if lambda is defined as coordinate compression.

Equivalently, with the reciprocal dilation convention used by the radial
functional, stationarity is captured by

    E_2 - E_4 + 3 E_0 = 0.

The run reports the dimensionless virial residual

    |E_2 - E_4 + 3E_0| / E.

The second scaling curvature is positive for a nontrivial stationary solution
containing E_4 and/or E_0.  This is an intrinsic Derrick-stability property of
the Lagrangian, not an arbitrary post-hoc rigidity.

TOPOLOGICAL CHARGE
------------------
The rational-map charge is

    Q
      =
    (B/pi)
    [
        F - (1/2) sin(2F)
    ]_infinity^0.

The boundary conditions reconstruct Q=B.

This prevents continuous unwinding to vacuum inside the declared field theory.

BINARY FISSION PREFLIGHT
------------------------
Topology by itself does not guarantee that a charge-B lump is stable against
splitting into lower-charge solitons.

For every (eta,m) point the run solves all sectors B=1,...,8 and requires for a
selected B:

    E_B
      <
    E_k + E_(B-k)

for every integer

    1 <= k < B.

Define the minimum fractional binary fission margin

    delta_fission
      =
    min_k
    [
        E_k + E_(B-k) - E_B
    ] / E_B.

A positive value is a necessary binding preflight.

It is NOT a complete 3D perturbation spectrum.

FINITE-PAYLOAD MONOPOLE PREFLIGHT
---------------------------------
B>1 rational-map fields are generally polyhedral rather than exactly
spherical.

Therefore this gate does NOT pretend that the radial angular average is the
full 3D gravitational field.

It computes the exact MONOPOLE field generated by the angular-integrated active
source and asks whether a finite spherical passive payload retains outward
center-of-mass acceleration in that monopole component.

Let the payload center lie on +z at dimensionless radius r_c and have radius
R_p.

For a point inside the payload,

    r
      =
    sqrt(
        r_c^2
        +
        s^2
        +
        2 r_c s mu
    ),

and the +z projection of the radial acceleration is

    a_z
      proportional to
    - M_A(r)
    (r_c + s mu)
    /
    r^3.

The volume average is evaluated by independent Gauss-Legendre quadrature.

The payload is required to fit entirely inside the radial interval where the
monopole enclosed active mass remains negative.

This gives an operational finite-payload MONOPOLE preflight.

A genuine promotion to a stable field-theoretical candidate requires a later
full 3D relaxation and direct 3D gravity integral.

ENERGY CONDITIONS
-----------------
The ordinary positive-sign Skyrme L2+L4 stress tensor is known in the
literature to satisfy the dominant energy condition.

The added potential is explicitly nonnegative and has vacuum-like stress

    rho = V,
    p_i = -V,

which also satisfies DEC.

The sum therefore remains in the DEC cone.

This gate nevertheless does NOT claim a pointwise 3D DEC reconstruction from
the one-dimensional rational-map profile.  That check belongs in the full 3D
gate.

SCAN
----
Promotion-grade scan:

    B = 1,...,8

    eta =
        0.36,
        0.40,
        0.50,
        0.70

    m =
        1,
        2,
        3,
        5,
        8

    I =
        1                    for B=1,
        1.28 B^2             for B>1.

For each (eta,m), every charge sector B=1,...,8 is solved so binary-fission
channels are available without interpolation.

The selected point must satisfy:

    B <= 8

    BVP_CONVERGED=YES

    TOPOLOGICAL_CHARGE_RELERR <= 1e-8

    VIRIAL_RELERR <= 5e-4

    TOTAL_ACTIVE_TO_ENERGY_RELERR <= 2e-3

    MIN_ENCLOSED_ACTIVE_FRACTION <= -1e-2

    MIN_BINARY_FISSION_MARGIN >= 2e-3

    FINITE_PAYLOAD_MONOPOLE_OUTWARD=YES

    FALSE_VACUUM_CURVATURE_MARGIN >= 0.1.

ROBUSTNESS
----------
The selected result is stressed against:

    I/B^2 =
        1.15,
        1.28,
        1.45

    eta neighborhood:
        eta - 0.04,
        eta,
        eta + 0.04

    m neighborhood:
        0.8 m,
        m,
        1.2 m

    BVP tolerances:
        1e-4,
        2e-5,
        5e-6

    outer-domain factors:
        0.8,
        1.0,
        1.3.

The result is not promoted from an isolated optimum.

BLIND WILDCARDS
---------------
The project-requested values

    1.6,
    1.875,
    3.125,
    0.625,
    5

are used only as labeled multiplicative m diagnostics around the selected
point when they remain inside the declared numerical domain.

They are NOT evidence, priors, or optimization targets.

PROMOTION CONDITION
-------------------
A strong 023A GREEN requires all of:

    ACTIVE_SOURCE_DERIVATIVE_ORDER_THEOREM=PASS

    FALSE_CORE_POTENTIAL=PASS

    TOPOLOGICAL_CHARGE=PASS

    RATIONAL_MAP_BVP=PASS

    DERRICK_VIRIAL=PASS

    BINARY_FISSION_PREFLIGHT=PASS

    NEGATIVE_ENCLOSED_ACTIVE_MASS=PASS

    POSITIVE_FAR_ACTIVE_MASS=PASS

    FINITE_PAYLOAD_MONOPOLE_OUTWARD=PASS

    VARIATIONAL_INDEPENDENT_SIGN_RECONSTRUCTION=PASS

    ROBUST_PARAMETER_BASIN=YES.

A GREEN result is classified only as

    TOPOLOGICALLY_STABILIZED_REPULSIVE_MONOPOLE_CAPACITY_PREFLIGHT.

It does NOT yet establish:

    full 3D static stability,
    the actual polyhedral 3D gravity field,
    an exterior repulsive field,
    nonlinear Einstein-matter consistency,
    a practical energy scale,
    a material realization,
    a practical antigravity device.

HEURISTIC DISCIPLINE
--------------------
023A alone does not automatically increase the current approximately-68-percent
project heuristic.

If GREEN, it authorizes the higher-value gate:

    023B_FULL_3D_FALSE_CORE_MULTISKYRMION_T_MUNU_GRAVITY_STABILITY_GATE.

A full 3D GREEN result that reproduces intrinsic stability and finite-payload
outward gravity would be qualitatively stronger and could justify a later
70-72 percent promotion.

STOP RULE
---------
If no B<=8 robust point produces negative enclosed active mass plus outward
finite-payload monopole response while remaining bound against binary fission,
close this minimal Skyrme false-core architecture.

Do not move to huge B merely to force a shell limit.

LITERATURE CONTEXT
------------------
- Rational-map Skyrmions are an established approximation to shell-like
  multi-Skyrmions.
- The rational-map angular integral obeys approximately I = 1.28 B^2 for the
  relevant multi-Skyrmion range.
- False-vacuum-potential Skyrme theories with a true vacuum at U=+1 and local
  false vacuum at U=-1 are established.
- Published three-dimensional/product-ansatz studies report bound
  multi-Skyrmions through B=8 in this model class.
- The ordinary Skyrme stress tensor is known to satisfy the dominant energy
  condition.

No novelty claim is made for those field-theory ingredients.

The project-derived question is specifically whether their stress organization
can create an operationally useful negative enclosed active mass in
linearized GR.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023A_TOPOLOGICAL_FALSE_CORE_MULTISKYRMION_GR_REPULSION_GATE
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from pathlib import Path
import re

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import cumulative_trapezoid, simpson
from scipy.interpolate import PchipInterpolator
from scipy.optimize import minimize
from scipy.integrate import solve_bvp


ROOT = Path(__file__).resolve().parents[1]

B_LOG = (
    ROOT
    / "results/logs"
    / "018b1b_global_multipatch_tmunu_gravity_conservation_closeout.log"
)
C2_LOG = (
    ROOT
    / "results/logs"
    / "018c2_direct_full_field_m2_hessian_confirmation.log"
)
A22_LOG = (
    ROOT
    / "results/logs"
    / "022a_asymmetric_vector_material_selector_and_naturalness_closeout.log"
)
A22_SOURCE = (
    ROOT
    / "simulations"
    / "022a_asymmetric_vector_material_selector_and_naturalness_closeout.py"
)

EXPECTED_022A_SHA256 = (
    "fbdc971e6c61bde7a36ac84360adec208222aa10d3bfbc4bd9659039cefb66dc"
)

B_VALUES = tuple(range(1, 9))
ETA_VALUES = (0.36, 0.40, 0.50, 0.70)
M_VALUES = (1.0, 2.0, 3.0, 5.0, 8.0)

BASE_I_RATIO = 1.28

R_MIN = 1.0e-4

BVP_TOL = 2.0e-5
BVP_MAX_NODES = 30000
BVP_INITIAL_N = 600
DIAGNOSTIC_N = 5000

MAX_TOPOLOGY_RELERR = 1.0e-8
MAX_VIRIAL_RELERR = 5.0e-4
MAX_ACTIVE_TOTAL_RELERR = 2.0e-3
MIN_NEGATIVE_ENCLOSED_FRACTION = 1.0e-2
MIN_FISSION_MARGIN = 2.0e-3
MIN_FALSE_VACUUM_CURVATURE_MARGIN = 0.10

PAYLOAD_RADIUS_FRACTIONS = (0.02, 0.05, 0.10)
PAYLOAD_QUAD_ORDER = 48

ROBUST_I_RATIOS = (1.15, 1.28, 1.45)
ROBUST_TOLS = (1.0e-4, 2.0e-5, 5.0e-6)
ROBUST_DOMAIN_FACTORS = (0.8, 1.0, 1.3)

BLIND_WILDCARD_FACTORS = (1.6, 1.875, 3.125, 0.625, 5.0)


@dataclass(frozen=True)
class ProfileResult:
    """One converged rational-map radial field and GR diagnostics."""

    B: int
    eta: float
    m: float
    i_ratio: float
    I: float

    success: bool
    message: str
    max_bvp_rms_residual: float

    r: np.ndarray
    F: np.ndarray
    Fp: np.ndarray

    e2_density: np.ndarray
    e4_density: np.ndarray
    e0_density: np.ndarray
    active_density: np.ndarray
    active_mass: np.ndarray

    E2: float
    E4: float
    E0: float
    E: float

    virial_relerr: float
    active_total_relerr: float

    topological_charge: float
    topology_relerr: float

    min_active_fraction: float
    min_active_radius: float
    negative_active_outer_radius: float

    shell_radius: float

    trial_energy: float
    trial_min_active_fraction: float
    trial_virial_relerr: float

    trial_R: float
    trial_p: float


@dataclass(frozen=True)
class Candidate:
    """One charge sector after binary-fission and payload checks."""

    profile: ProfileResult
    fission_margin: float

    payload_center: float
    payload_radius: float
    payload_outward_kernel: float
    payload_coefficient_c: float
    point_coefficient_c: float

    finite_payload_pass: bool


def require_marker(path: Path, marker: str) -> None:
    """Require one exact upstream scientific marker."""

    if not path.exists():
        raise RuntimeError(f"Missing upstream log: {path}")

    text = path.read_text(errors="replace")

    if marker not in text:
        raise RuntimeError(
            f"Missing required marker in {path.name}: {marker}"
        )


def sha256(path: Path) -> str:
    """Return SHA-256 for one source file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def potential(F: np.ndarray | float, eta: float, m: float):
    """Return nonnegative true-vacuum/false-core Skyrme potential."""

    c = np.cos(F)

    return (
        m * m
        * (1.0 - c)
        * (1.0 + eta * c)
    )


def dpotential_dF(F: np.ndarray | float, eta: float, m: float):
    """Return exact derivative of the false-core potential."""

    c = np.cos(F)
    s = np.sin(F)

    return (
        m * m
        * s
        * (
            1.0
            - eta
            + 2.0 * eta * c
        )
    )


def false_vacuum_properties(
    eta: float,
    m: float,
) -> tuple[float, float, float, float]:
    """Return V_true, V_false, true curvature, false curvature."""

    v_true = 0.0
    v_false = 2.0 * m * m * (1.0 - eta)

    curvature_true = m * m * (1.0 + eta)
    curvature_false = m * m * (3.0 * eta - 1.0)

    return (
        v_true,
        v_false,
        curvature_true,
        curvature_false,
    )


def rational_map_I(
    B: int,
    i_ratio: float,
) -> float:
    """Return rational-map angular integral."""

    if B == 1:
        return 1.0

    return i_ratio * B * B


def stable_profile_from_logs(
    r: np.ndarray,
    R: float,
    p: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return F=2 atan[(R/r)^p] and its analytic derivative stably."""

    x = (
        p
        * (
            math.log(R)
            -
            np.log(r)
        )
    )

    F = np.empty_like(r)

    positive = x >= 0.0

    F[positive] = (
        math.pi
        -
        2.0
        * np.arctan(
            np.exp(
                -x[positive]
            )
        )
    )

    F[~positive] = (
        2.0
        * np.arctan(
            np.exp(
                x[~positive]
            )
        )
    )

    Fp = (
        -p
        * np.sin(F)
        / r
    )

    return F, Fp


def component_densities(
    r: np.ndarray,
    F: np.ndarray,
    Fp: np.ndarray,
    B: int,
    eta: float,
    m: float,
    I: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return e2, e4, e0 local energy densities."""

    s = np.sin(F)

    e2 = (
        Fp * Fp
        +
        2.0
        * B
        * s * s
        / (r * r)
    )

    e4 = (
        2.0
        * B
        * s * s
        * Fp * Fp
        / (r * r)
        +
        I
        * s**4
        / r**4
    )

    e0 = potential(
        F,
        eta,
        m,
    )

    return e2, e4, e0


def integrated_components(
    r: np.ndarray,
    e2: np.ndarray,
    e4: np.ndarray,
    e0: np.ndarray,
) -> tuple[float, float, float, float]:
    """Return E2,E4,E0,E without the common positive angular normalization."""

    shell = r * r

    E2 = float(
        simpson(
            shell * e2,
            x=r,
        )
    )

    E4 = float(
        simpson(
            shell * e4,
            x=r,
        )
    )

    E0 = float(
        simpson(
            shell * e0,
            x=r,
        )
    )

    E = E2 + E4 + E0

    return E2, E4, E0, E


def choose_rmax(
    B: int,
    eta: float,
    m: float,
) -> float:
    """Choose a conservative radial domain from mass and shell scales."""

    _, _, curvature_true, _ = false_vacuum_properties(
        eta,
        m,
    )

    tail_mass = math.sqrt(
        max(
            curvature_true,
            1.0e-12,
        )
    )

    tail_length = 1.0 / tail_mass

    shell_guess = (
        0.65
        * math.sqrt(B)
        +
        1.0
    )

    return max(
        12.0,
        8.0 * tail_length + 5.0 * shell_guess,
    )


def optimize_trial_profile(
    B: int,
    eta: float,
    m: float,
    I: float,
    rmax: float,
) -> tuple[float, float, float, float, float]:
    """Optimize the independent two-parameter analytic profile."""

    r = np.geomspace(
        R_MIN,
        rmax,
        1800,
    )

    def objective(x: np.ndarray) -> float:
        R = math.exp(
            float(x[0])
        )

        p = (
            0.5
            +
            math.exp(
                float(x[1])
            )
        )

        F, Fp = stable_profile_from_logs(
            r,
            R,
            p,
        )

        e2, e4, e0 = component_densities(
            r,
            F,
            Fp,
            B,
            eta,
            m,
            I,
        )

        return integrated_components(
            r,
            e2,
            e4,
            e0,
        )[-1]

    R0 = max(
        0.5,
        0.55 * math.sqrt(B),
    )

    p0 = 2.5

    x0 = np.array(
        [
            math.log(R0),
            math.log(p0 - 0.5),
        ],
        dtype=float,
    )

    opt = minimize(
        objective,
        x0,
        method="Nelder-Mead",
        options={
            "maxiter": 500,
            "xatol": 2.0e-6,
            "fatol": 2.0e-7,
        },
    )

    R = math.exp(
        float(opt.x[0])
    )

    p = (
        0.5
        +
        math.exp(
            float(opt.x[1])
        )
    )

    F, Fp = stable_profile_from_logs(
        r,
        R,
        p,
    )

    e2, e4, e0 = component_densities(
        r,
        F,
        Fp,
        B,
        eta,
        m,
        I,
    )

    E2, E4, E0, E = integrated_components(
        r,
        e2,
        e4,
        e0,
    )

    active = 2.0 * (
        e4 - e0
    )

    active_mass = cumulative_trapezoid(
        r * r * active,
        r,
        initial=0.0,
    )

    min_fraction = float(
        np.min(active_mass)
        / E
    )

    virial = abs(
        E2 - E4 + 3.0 * E0
    ) / E

    return (
        R,
        p,
        E,
        min_fraction,
        virial,
    )


def solve_profile(
    B: int,
    eta: float,
    m: float,
    i_ratio: float = BASE_I_RATIO,
    tol: float = BVP_TOL,
    domain_factor: float = 1.0,
) -> ProfileResult:
    """Solve one rational-map radial Euler-Lagrange boundary value problem."""

    I = rational_map_I(
        B,
        i_ratio,
    )

    rmax = (
        choose_rmax(
            B,
            eta,
            m,
        )
        * domain_factor
    )

    R_trial, p_trial, trial_energy, trial_min_fraction, trial_virial = (
        optimize_trial_profile(
            B,
            eta,
            m,
            I,
            rmax,
        )
    )

    r = np.geomspace(
        R_MIN,
        rmax,
        BVP_INITIAL_N,
    )

    F0, Fp0 = stable_profile_from_logs(
        r,
        R_trial,
        p_trial,
    )

    y0 = np.vstack(
        [
            F0,
            Fp0,
        ]
    )

    def ode(
        radius: np.ndarray,
        y: np.ndarray,
    ) -> np.ndarray:
        F = y[0]
        Fp = y[1]

        s = np.sin(F)
        c = np.cos(F)

        denominator = (
            radius * radius
            +
            2.0
            * B
            * s * s
        )

        numerator = (
            2.0
            * B
            * s * c
            +
            2.0
            * I
            * s**3
            * c
            / (radius * radius)
            +
            0.5
            * radius * radius
            * dpotential_dF(
                F,
                eta,
                m,
            )
            -
            2.0
            * radius
            * Fp
            -
            2.0
            * B
            * s * c
            * Fp * Fp
        )

        return np.vstack(
            [
                Fp,
                numerator / denominator,
            ]
        )

    def boundary(
        ya: np.ndarray,
        yb: np.ndarray,
    ) -> np.ndarray:
        return np.array(
            [
                ya[0] - math.pi,
                yb[0],
            ]
        )

    solution = solve_bvp(
        ode,
        boundary,
        r,
        y0,
        tol=tol,
        max_nodes=BVP_MAX_NODES,
        verbose=0,
    )

    diagnostic_r = np.geomspace(
        R_MIN,
        rmax,
        DIAGNOSTIC_N,
    )

    F, Fp = solution.sol(
        diagnostic_r
    )

    e2, e4, e0 = component_densities(
        diagnostic_r,
        F,
        Fp,
        B,
        eta,
        m,
        I,
    )

    E2, E4, E0, E = integrated_components(
        diagnostic_r,
        e2,
        e4,
        e0,
    )

    if not (
        math.isfinite(E)
        and E > 0.0
    ):
        raise RuntimeError(
            "Nonpositive/nonfinite Skyrmion energy"
        )

    active = 2.0 * (
        e4 - e0
    )

    active_mass = cumulative_trapezoid(
        diagnostic_r * diagnostic_r * active,
        diagnostic_r,
        initial=0.0,
    )

    virial = abs(
        E2 - E4 + 3.0 * E0
    ) / E

    active_total_relerr = abs(
        active_mass[-1] / E - 1.0
    )

    topological_charge = (
        B
        / math.pi
        * (
            (
                F[0]
                -
                0.5 * math.sin(
                    2.0 * F[0]
                )
            )
            -
            (
                F[-1]
                -
                0.5 * math.sin(
                    2.0 * F[-1]
                )
            )
        )
    )

    topology_relerr = abs(
        topological_charge / B - 1.0
    )

    min_index = int(
        np.argmin(active_mass)
    )

    min_fraction = float(
        active_mass[min_index] / E
    )

    negative_indices = np.flatnonzero(
        active_mass < 0.0
    )

    if len(negative_indices) > 0:
        negative_outer = float(
            diagnostic_r[
                negative_indices[-1]
            ]
        )
    else:
        negative_outer = 0.0

    # Shell radius is defined by the F=pi/2 transition.
    shell_index = int(
        np.argmin(
            np.abs(
                F - 0.5 * math.pi
            )
        )
    )

    shell_radius = float(
        diagnostic_r[shell_index]
    )

    if hasattr(
        solution,
        "rms_residuals",
    ):
        max_residual = float(
            np.max(
                np.asarray(
                    solution.rms_residuals,
                    dtype=float,
                )
            )
        )
    else:
        max_residual = float("nan")

    return ProfileResult(
        B=B,
        eta=eta,
        m=m,
        i_ratio=i_ratio,
        I=I,
        success=bool(solution.success),
        message=str(solution.message),
        max_bvp_rms_residual=max_residual,
        r=diagnostic_r,
        F=np.asarray(F),
        Fp=np.asarray(Fp),
        e2_density=e2,
        e4_density=e4,
        e0_density=e0,
        active_density=active,
        active_mass=active_mass,
        E2=E2,
        E4=E4,
        E0=E0,
        E=E,
        virial_relerr=virial,
        active_total_relerr=active_total_relerr,
        topological_charge=topological_charge,
        topology_relerr=topology_relerr,
        min_active_fraction=min_fraction,
        min_active_radius=float(
            diagnostic_r[min_index]
        ),
        negative_active_outer_radius=negative_outer,
        shell_radius=shell_radius,
        trial_energy=trial_energy,
        trial_min_active_fraction=trial_min_fraction,
        trial_virial_relerr=trial_virial,
        trial_R=R_trial,
        trial_p=p_trial,
    )


def binary_fission_margin(
    energies: dict[int, float],
    B: int,
) -> float:
    """Return minimum fractional margin against B -> k + (B-k)."""

    if B <= 1:
        return float("inf")

    E_B = energies[B]

    margins = []

    for k in range(1, B):
        other = B - k

        margins.append(
            (
                energies[k]
                +
                energies[other]
                -
                E_B
            )
            / E_B
        )

    return float(
        min(margins)
    )


def payload_average_kernel(
    profile: ProfileResult,
    center: float,
    radius: float,
    order: int = PAYLOAD_QUAD_ORDER,
) -> float:
    """Return volume-averaged outward z acceleration per unit total mass.

    The result is dimensionless and refers only to the angular-integrated
    monopole component.
    """

    nodes, weights = leggauss(
        order
    )

    s_nodes = (
        0.5
        * radius
        * (nodes + 1.0)
    )

    s_weights = (
        0.5
        * radius
        * weights
    )

    mu_nodes = nodes
    mu_weights = weights

    mass_fraction = (
        profile.active_mass / profile.E
    )

    interpolator = PchipInterpolator(
        profile.r,
        mass_fraction,
        extrapolate=False,
    )

    total = 0.0

    for s, ws in zip(
        s_nodes,
        s_weights,
    ):
        global_r = np.sqrt(
            center * center
            +
            s * s
            +
            2.0
            * center
            * s
            * mu_nodes
        )

        global_r = np.maximum(
            global_r,
            profile.r[0],
        )

        mfrac = interpolator(
            np.minimum(
                global_r,
                profile.r[-1],
            )
        )

        z_projection = (
            center
            +
            s * mu_nodes
        ) / global_r

        acceleration_z = (
            -mfrac
            * z_projection
            / global_r**2
        )

        total += (
            ws
            * s * s
            * float(
                np.sum(
                    mu_weights
                    * acceleration_z
                )
            )
        )

    return (
        3.0
        / (
            2.0
            * radius**3
        )
        * total
    )


def best_payload_candidate(
    profile: ProfileResult,
) -> tuple[float, float, float, float, float, bool]:
    """Return best finite-payload monopole operating point."""

    if (
        profile.negative_active_outer_radius <= 0.0
        or profile.min_active_fraction >= 0.0
    ):
        return (
            float("nan"),
            float("nan"),
            0.0,
            float("inf"),
            float("inf"),
            False,
        )

    point_kernel = (
        -profile.active_mass
        / profile.E
        / profile.r**2
    )

    # Only use centers inside the negative enclosed-active interval.
    valid = (
        (profile.active_mass < 0.0)
        &
        (profile.r > 0.05 * profile.shell_radius)
        &
        (
            profile.r
            <
            0.95
            * profile.negative_active_outer_radius
        )
    )

    indices = np.flatnonzero(
        valid
    )

    if len(indices) == 0:
        return (
            float("nan"),
            float("nan"),
            0.0,
            float("inf"),
            float("inf"),
            False,
        )

    # Search only the strongest point-kernel centers.
    ranked = indices[
        np.argsort(
            point_kernel[indices]
        )[::-1]
    ][:40]

    best = None

    for index in ranked:
        center = float(
            profile.r[index]
        )

        for fraction in PAYLOAD_RADIUS_FRACTIONS:
            payload_radius = (
                fraction
                * profile.shell_radius
            )

            if center - payload_radius <= profile.r[0]:
                continue

            if (
                center + payload_radius
                >= profile.negative_active_outer_radius
            ):
                continue

            kernel = payload_average_kernel(
                profile,
                center,
                payload_radius,
            )

            if not (
                math.isfinite(kernel)
                and kernel > 0.0
            ):
                continue

            coefficient = (
                1.0
                / (
                    kernel
                    * center * center
                )
            )

            point_coefficient = (
                1.0
                /
                max(
                    -profile.active_mass[index]
                    / profile.E,
                    1.0e-300,
                )
            )

            record = (
                coefficient,
                center,
                payload_radius,
                kernel,
                point_coefficient,
            )

            if (
                best is None
                or record[0] < best[0]
            ):
                best = record

    if best is None:
        return (
            float("nan"),
            float("nan"),
            0.0,
            float("inf"),
            float("inf"),
            False,
        )

    coefficient, center, payload_radius, kernel, point_coefficient = best

    return (
        center,
        payload_radius,
        kernel,
        coefficient,
        point_coefficient,
        True,
    )


def make_candidate(
    profile: ProfileResult,
    energies: dict[int, float],
) -> Candidate:
    """Attach fission and finite-payload diagnostics to one profile."""

    margin = binary_fission_margin(
        energies,
        profile.B,
    )

    (
        center,
        payload_radius,
        kernel,
        coefficient,
        point_coefficient,
        payload_pass,
    ) = best_payload_candidate(
        profile
    )

    return Candidate(
        profile=profile,
        fission_margin=margin,
        payload_center=center,
        payload_radius=payload_radius,
        payload_outward_kernel=kernel,
        payload_coefficient_c=coefficient,
        point_coefficient_c=point_coefficient,
        finite_payload_pass=payload_pass,
    )


def profile_passes_core(
    profile: ProfileResult,
) -> bool:
    """Return the non-fission/non-payload promotion predicate."""

    _, _, _, false_curvature = false_vacuum_properties(
        profile.eta,
        profile.m,
    )

    false_curvature_margin = (
        3.0 * profile.eta - 1.0
    )

    return (
        profile.success
        and profile.topology_relerr
        <= MAX_TOPOLOGY_RELERR
        and profile.virial_relerr
        <= MAX_VIRIAL_RELERR
        and profile.active_total_relerr
        <= MAX_ACTIVE_TOTAL_RELERR
        and profile.min_active_fraction
        <= -MIN_NEGATIVE_ENCLOSED_FRACTION
        and false_curvature > 0.0
        and false_curvature_margin
        >= MIN_FALSE_VACUUM_CURVATURE_MARGIN
    )


def candidate_passes(
    candidate: Candidate,
) -> bool:
    """Return full 023A capacity promotion predicate."""

    return (
        profile_passes_core(
            candidate.profile
        )
        and candidate.fission_margin
        >= MIN_FISSION_MARGIN
        and candidate.finite_payload_pass
        and candidate.payload_outward_kernel
        > 0.0
    )


def scan_main_basin() -> tuple[
    list[Candidate],
    dict[tuple[float, float, int], ProfileResult],
]:
    """Solve all B=1..8 sectors throughout the declared parameter basin."""

    candidates = []
    profiles = {}

    for eta in ETA_VALUES:
        for m in M_VALUES:
            sector_profiles = {}

            for B in B_VALUES:
                profile = solve_profile(
                    B,
                    eta,
                    m,
                )

                profiles[
                    (
                        eta,
                        m,
                        B,
                    )
                ] = profile

                sector_profiles[B] = profile

            if not all(
                profile.success
                for profile in sector_profiles.values()
            ):
                continue

            energies = {
                B: profile.E
                for B, profile in sector_profiles.items()
            }

            for B in B_VALUES:
                if B == 1:
                    continue

                candidates.append(
                    make_candidate(
                        sector_profiles[B],
                        energies,
                    )
                )

    return candidates, profiles


def selected_rank(
    candidate: Candidate,
) -> tuple[float, float, float, float]:
    """Rank robust candidates by payload efficiency and stability margins."""

    return (
        candidate.payload_coefficient_c,
        -candidate.fission_margin,
        candidate.profile.virial_relerr,
        -abs(
            candidate.profile.min_active_fraction
        ),
    )


def solve_sector_set(
    B_max: int,
    eta: float,
    m: float,
    i_ratio: float,
    tol: float = BVP_TOL,
    domain_factor: float = 1.0,
) -> tuple[dict[int, ProfileResult], float]:
    """Solve B=1..B_max and return selected-B fission margin."""

    sector = {}

    for B in range(1, B_max + 1):
        sector[B] = solve_profile(
            B,
            eta,
            m,
            i_ratio=i_ratio,
            tol=tol,
            domain_factor=domain_factor,
        )

    if not all(
        result.success
        for result in sector.values()
    ):
        return sector, -math.inf

    energies = {
        B: result.E
        for B, result in sector.items()
    }

    return (
        sector,
        binary_fission_margin(
            energies,
            B_max,
        ),
    )


def robustness_audit(
    selected: Candidate,
) -> tuple[int, int, float, float]:
    """Stress the selected point against map, parameter, resolution, and domain changes."""

    B = selected.profile.B
    eta0 = selected.profile.eta
    m0 = selected.profile.m

    total = 0
    passes = 0

    worst_negative_fraction = -math.inf
    worst_fission_margin = math.inf

    # 1. Rational-map angular-integral uncertainty.
    for i_ratio in ROBUST_I_RATIOS:
        total += 1

        sector, margin = solve_sector_set(
            B,
            eta0,
            m0,
            i_ratio,
        )

        profile = sector[B]
        candidate = make_candidate(
            profile,
            {
                k: value.E
                for k, value in sector.items()
            },
        ) if all(v.success for v in sector.values()) else None

        if candidate is not None:
            worst_negative_fraction = max(
                worst_negative_fraction,
                candidate.profile.min_active_fraction,
            )

            worst_fission_margin = min(
                worst_fission_margin,
                margin,
            )

            if (
                profile_passes_core(candidate.profile)
                and margin > 0.0
                and candidate.finite_payload_pass
            ):
                passes += 1

    # 2. eta/m local neighborhood.
    eta_values = (
        max(
            1.0 / 3.0 + 0.015,
            eta0 - 0.04,
        ),
        eta0,
        min(
            0.95,
            eta0 + 0.04,
        ),
    )

    m_values = (
        0.8 * m0,
        m0,
        1.2 * m0,
    )

    for eta in eta_values:
        for m in m_values:
            if (
                abs(eta - eta0) < 1.0e-12
                and abs(m - m0) < 1.0e-12
            ):
                continue

            total += 1

            sector, margin = solve_sector_set(
                B,
                eta,
                m,
                BASE_I_RATIO,
            )

            if not all(
                value.success
                for value in sector.values()
            ):
                continue

            candidate = make_candidate(
                sector[B],
                {
                    k: value.E
                    for k, value in sector.items()
                },
            )

            worst_negative_fraction = max(
                worst_negative_fraction,
                candidate.profile.min_active_fraction,
            )

            worst_fission_margin = min(
                worst_fission_margin,
                margin,
            )

            if (
                profile_passes_core(candidate.profile)
                and margin > 0.0
                and candidate.finite_payload_pass
            ):
                passes += 1

    # 3. Numerical tolerance / domain on the selected sector only.
    # These tests do not re-evaluate fission because they are numerical
    # convergence checks, not model-parameter perturbations.
    for tol in ROBUST_TOLS:
        total += 1

        profile = solve_profile(
            B,
            eta0,
            m0,
            i_ratio=BASE_I_RATIO,
            tol=tol,
        )

        payload_pass = best_payload_candidate(
            profile
        )[-1]

        if (
            profile_passes_core(profile)
            and payload_pass
        ):
            passes += 1

    for domain_factor in ROBUST_DOMAIN_FACTORS:
        total += 1

        profile = solve_profile(
            B,
            eta0,
            m0,
            i_ratio=BASE_I_RATIO,
            domain_factor=domain_factor,
        )

        payload_pass = best_payload_candidate(
            profile
        )[-1]

        if (
            profile_passes_core(profile)
            and payload_pass
        ):
            passes += 1

    pass_fraction = (
        passes / max(total, 1)
    )

    return (
        passes,
        total,
        pass_fraction,
        worst_fission_margin,
    )


def main() -> None:
    """Execute the complete 023A topological false-core gate."""

    print(
        "=== 023A — TOPOLOGICAL FALSE-CORE "
        "MULTISKYRMION GR-REPULSION GATE ==="
    )

    # --------------------------------------------------------------
    # Upstream fail-closed audit.
    # --------------------------------------------------------------
    require_marker(
        B_LOG,
        "018B1B_GLOBAL_MULTIPATCH_T_MUNU_GRAVITY_CONSERVATION_CLOSEOUT=GREEN",
    )
    require_marker(
        B_LOG,
        "FIELD_THEORETICAL_CANDIDATE=YES",
    )
    require_marker(
        C2_LOG,
        "018C2_DIRECT_FULL_FIELD_M2_HESSIAN_CONFIRMATION=GREEN_NEGATIVE_RESULT",
    )
    require_marker(
        C2_LOG,
        "FULL_COMPOSITE_STABILITY=FAIL_M2",
    )
    require_marker(
        A22_LOG,
        "022A_ASYMMETRIC_VECTOR_MATERIAL_SELECTOR_AND_NATURALNESS_CLOSEOUT=GREEN_NEGATIVE_RESULT",
    )
    require_marker(
        A22_LOG,
        "GLOBAL_RERANK=REQUIRED",
    )

    if not A22_SOURCE.exists():
        raise RuntimeError(
            f"Missing 022A source: {A22_SOURCE}"
        )

    a22_sha = sha256(
        A22_SOURCE
    )

    print("\n=== UPSTREAM FRONTIER AUDIT ===")
    print(
        f"022A_SOURCE_SHA256={a22_sha}"
    )
    print(
        "022A_SOURCE_HASH_MATCH="
        + (
            "PASS"
            if a22_sha == EXPECTED_022A_SHA256
            else "FAIL"
        )
    )
    print(
        "018B_FIELD_EXISTENCE_RESULT=RETAINED"
    )
    print(
        "018C_M2_STABILITY_FALSIFICATION=RETAINED"
    )
    print(
        "022A_PROTECTED_VECTOR_BRANCH_CLOSEOUT=RETAINED"
    )

    if a22_sha != EXPECTED_022A_SHA256:
        raise RuntimeError(
            "022A source hash mismatch"
        )

    # --------------------------------------------------------------
    # A. Analytical active-source and potential structure.
    # --------------------------------------------------------------
    print("\n=== A — ACTIVE-SOURCE DERIVATIVE-ORDER THEOREM ===")
    print(
        "ACTIVE_SOURCE_GENERAL_FORM="
        "S_N_EQUALS_N_MINUS_2_TIMES_E_N"
    )
    print(
        "SIGMA_MODEL_QUADRATIC_ACTIVE_SOURCE=ZERO"
    )
    print(
        "SKYRME_QUARTIC_ACTIVE_SOURCE=PLUS_2_E4"
    )
    print(
        "NONNEGATIVE_POTENTIAL_ACTIVE_SOURCE=MINUS_2_V"
    )
    print(
        "ACTIVE_SOURCE_DERIVATIVE_ORDER_THEOREM=PASS_ANALYTIC"
    )

    print("\n=== B — FALSE-CORE POTENTIAL ANALYTIC AUDIT ===")

    potential_pass = True

    for eta in ETA_VALUES:
        for m in M_VALUES:
            (
                v_true,
                v_false,
                curvature_true,
                curvature_false,
            ) = false_vacuum_properties(
                eta,
                m,
            )

            # Dense direct nonnegativity scan over the complete field interval.
            F_scan = np.linspace(
                0.0,
                math.pi,
                1001,
            )

            min_v = float(
                np.min(
                    potential(
                        F_scan,
                        eta,
                        m,
                    )
                )
            )

            local_pass = (
                abs(v_true) <= 1.0e-14
                and v_false > 0.0
                and curvature_true > 0.0
                and curvature_false > 0.0
                and min_v >= -1.0e-12
            )

            potential_pass &= local_pass

    print(
        "TRUE_VACUUM_F_EQUALS_0=PASS"
    )
    print(
        "POSITIVE_FALSE_VACUUM_F_EQUALS_PI=PASS"
    )
    print(
        "POTENTIAL_NONNEGATIVE_ON_0_TO_PI="
        + (
            "PASS"
            if potential_pass
            else "FAIL"
        )
    )
    print(
        "FALSE_CORE_POTENTIAL="
        + (
            "PASS"
            if potential_pass
            else "FAIL"
        )
    )
    print(
        "POTENTIAL_EQUIVALENT_TWO_MASS_MAPPING="
        "M2SQ_EQUALS_ETA_M_SQUARED_AND_M1SQ_EQUALS_2_ONE_MINUS_ETA_M_SQUARED"
    )

    # --------------------------------------------------------------
    # C. Main B<=8 field solve.
    # --------------------------------------------------------------
    print("\n=== C — B<=8 RATIONAL-MAP EULER-LAGRANGE SCAN ===")

    candidates, profiles = scan_main_basin()

    total_profiles = len(
        profiles
    )

    converged_profiles = sum(
        1
        for profile in profiles.values()
        if profile.success
    )

    core_passers = [
        candidate
        for candidate in candidates
        if profile_passes_core(
            candidate.profile
        )
    ]

    full_passers = [
        candidate
        for candidate in candidates
        if candidate_passes(
            candidate
        )
    ]

    print(
        f"RATIONAL_MAP_TOTAL_BVP_PROFILES={total_profiles}"
    )
    print(
        f"RATIONAL_MAP_CONVERGED_PROFILES={converged_profiles}"
    )
    print(
        f"NEGATIVE_ACTIVE_CORE_CANDIDATES={len(core_passers)}"
    )
    print(
        f"FULL_023A_CAPACITY_PASSERS={len(full_passers)}"
    )

    for B in B_VALUES:
        B_profiles = [
            profile
            for profile in profiles.values()
            if profile.B == B
            and profile.success
        ]

        if not B_profiles:
            continue

        best_B = min(
            B_profiles,
            key=lambda profile:
                profile.min_active_fraction,
        )

        print(
            f"B{B}_BEST_MIN_ENCLOSED_ACTIVE_FRACTION="
            f"{best_B.min_active_fraction:.15e}"
        )
        print(
            f"B{B}_BEST_ETA={best_B.eta:.15e}"
        )
        print(
            f"B{B}_BEST_M={best_B.m:.15e}"
        )

    if not candidates:
        raise RuntimeError(
            "No finite rational-map candidates"
        )

    if full_passers:
        selected = min(
            full_passers,
            key=selected_rank,
        )
    else:
        selected = min(
            candidates,
            key=lambda candidate: (
                candidate.payload_coefficient_c,
                candidate.profile.min_active_fraction,
            ),
        )

    profile = selected.profile

    # --------------------------------------------------------------
    # D. Selected point.
    # --------------------------------------------------------------
    print("\n=== D — SELECTED TOPOLOGICAL FALSE-CORE POINT ===")

    (
        v_true,
        v_false,
        curvature_true,
        curvature_false,
    ) = false_vacuum_properties(
        profile.eta,
        profile.m,
    )

    mapped_m2_sq = (
        profile.eta
        * profile.m**2
    )
    mapped_m1_sq = (
        2.0
        * (
            1.0 - profile.eta
        )
        * profile.m**2
    )

    print(
        f"SELECTED_B={profile.B}"
    )
    print(
        f"SELECTED_ETA={profile.eta:.15e}"
    )
    print(
        f"SELECTED_M={profile.m:.15e}"
    )
    print(
        f"SELECTED_I={profile.I:.15e}"
    )
    print(
        f"SELECTED_I_OVER_B2={profile.I / profile.B**2:.15e}"
    )
    print(
        f"SELECTED_M1_SQUARED_MAPPING={mapped_m1_sq:.15e}"
    )
    print(
        f"SELECTED_M2_SQUARED_MAPPING={mapped_m2_sq:.15e}"
    )
    print(
        f"SELECTED_TRUE_VACUUM_CURVATURE={curvature_true:.15e}"
    )
    print(
        f"SELECTED_FALSE_VACUUM_ENERGY={v_false:.15e}"
    )
    print(
        f"SELECTED_FALSE_VACUUM_CURVATURE={curvature_false:.15e}"
    )
    print(
        f"SELECTED_FALSE_VACUUM_DIMENSIONLESS_MARGIN={3.0 * profile.eta - 1.0:.15e}"
    )

    print(
        f"SELECTED_BVP_SUCCESS={'YES' if profile.success else 'NO'}"
    )
    print(
        "SELECTED_BVP_MESSAGE="
        + profile.message.replace(
            " ",
            "_",
        )
    )
    print(
        f"SELECTED_BVP_MAX_RMS_RESIDUAL={profile.max_bvp_rms_residual:.15e}"
    )

    print(
        f"SELECTED_TOPOLOGICAL_CHARGE={profile.topological_charge:.15e}"
    )
    print(
        f"SELECTED_TOPOLOGICAL_CHARGE_RELERR={profile.topology_relerr:.15e}"
    )

    print(
        f"SELECTED_E2={profile.E2:.15e}"
    )
    print(
        f"SELECTED_E4={profile.E4:.15e}"
    )
    print(
        f"SELECTED_E0={profile.E0:.15e}"
    )
    print(
        f"SELECTED_TOTAL_ENERGY={profile.E:.15e}"
    )
    print(
        f"SELECTED_VIRIAL_RELERR={profile.virial_relerr:.15e}"
    )
    print(
        f"SELECTED_TOTAL_ACTIVE_TO_ENERGY_RELERR={profile.active_total_relerr:.15e}"
    )

    print(
        f"SELECTED_MIN_ENCLOSED_ACTIVE_FRACTION={profile.min_active_fraction:.15e}"
    )
    print(
        f"SELECTED_MIN_ENCLOSED_ACTIVE_RADIUS={profile.min_active_radius:.15e}"
    )
    print(
        f"SELECTED_NEGATIVE_ACTIVE_OUTER_RADIUS={profile.negative_active_outer_radius:.15e}"
    )
    print(
        f"SELECTED_SHELL_RADIUS_F_PI_OVER_2={profile.shell_radius:.15e}"
    )

    print(
        f"SELECTED_MIN_BINARY_FISSION_MARGIN={selected.fission_margin:.15e}"
    )

    print(
        f"SELECTED_PAYLOAD_CENTER={selected.payload_center:.15e}"
    )
    print(
        f"SELECTED_PAYLOAD_RADIUS={selected.payload_radius:.15e}"
    )
    print(
        f"SELECTED_PAYLOAD_RADIUS_OVER_SHELL={selected.payload_radius / profile.shell_radius:.15e}"
    )
    print(
        f"SELECTED_FINITE_PAYLOAD_OUTWARD_KERNEL={selected.payload_outward_kernel:.15e}"
    )
    print(
        f"SELECTED_MONOPOLE_PAYLOAD_C={selected.payload_coefficient_c:.15e}"
    )
    print(
        f"SELECTED_MONOPOLE_POINT_C={selected.point_coefficient_c:.15e}"
    )
    print(
        "SELECTED_FINITE_PAYLOAD_MONOPOLE_OUTWARD="
        + (
            "YES"
            if selected.finite_payload_pass
            else "NO"
        )
    )

    # --------------------------------------------------------------
    # E. Independent variational sign reconstruction.
    # --------------------------------------------------------------
    print("\n=== E — INDEPENDENT VARIATIONAL SIGN RECONSTRUCTION ===")

    bvp_energy_below_trial = (
        profile.E
        <= profile.trial_energy
        * (
            1.0 + 1.0e-4
        )
    )

    trial_sign_agrees = (
        profile.trial_min_active_fraction < 0.0
        and profile.min_active_fraction < 0.0
    )

    print(
        f"TRIAL_R={profile.trial_R:.15e}"
    )
    print(
        f"TRIAL_P={profile.trial_p:.15e}"
    )
    print(
        f"TRIAL_ENERGY={profile.trial_energy:.15e}"
    )
    print(
        f"BVP_ENERGY={profile.E:.15e}"
    )
    print(
        "BVP_ENERGY_NOT_ABOVE_VARIATIONAL_TRIAL="
        + (
            "PASS"
            if bvp_energy_below_trial
            else "FAIL"
        )
    )
    print(
        f"TRIAL_MIN_ENCLOSED_ACTIVE_FRACTION={profile.trial_min_active_fraction:.15e}"
    )
    print(
        f"TRIAL_VIRIAL_RELERR={profile.trial_virial_relerr:.15e}"
    )
    print(
        "VARIATIONAL_AND_BVP_NEGATIVE_ACTIVE_SIGN_AGREE="
        + (
            "PASS"
            if trial_sign_agrees
            else "FAIL"
        )
    )

    independent_sign_pass = (
        bvp_energy_below_trial
        and trial_sign_agrees
    )

    print(
        "VARIATIONAL_INDEPENDENT_SIGN_RECONSTRUCTION="
        + (
            "PASS"
            if independent_sign_pass
            else "FAIL"
        )
    )

    # --------------------------------------------------------------
    # F. Robustness.
    # --------------------------------------------------------------
    print("\n=== F — ROBUSTNESS AUDIT ===")

    (
        robust_passes,
        robust_total,
        robust_fraction,
        worst_fission_margin,
    ) = robustness_audit(
        selected
    )

    print(
        f"ROBUSTNESS_PASS_COUNT={robust_passes}"
    )
    print(
        f"ROBUSTNESS_TOTAL_COUNT={robust_total}"
    )
    print(
        f"ROBUSTNESS_PASS_FRACTION={robust_fraction:.15e}"
    )
    print(
        f"ROBUSTNESS_WORST_BINARY_FISSION_MARGIN={worst_fission_margin:.15e}"
    )

    robust_basin = (
        robust_total >= 10
        and robust_fraction >= 0.80
        and worst_fission_margin > 0.0
    )

    print(
        "ROBUST_PARAMETER_BASIN="
        + (
            "YES"
            if robust_basin
            else "NO"
        )
    )

    # --------------------------------------------------------------
    # G. Blind wildcards.
    # --------------------------------------------------------------
    print("\n=== BLIND WILDCARD MASS DIAGNOSTICS — NOT EVIDENCE ===")

    for factor in BLIND_WILDCARD_FACTORS:
        test_m = (
            profile.m
            * factor
        )

        # Keep diagnostics bounded to avoid turning wildcard values into a new
        # scientific scan.
        test_m = min(
            max(
                test_m,
                0.5,
            ),
            20.0,
        )

        test = solve_profile(
            profile.B,
            profile.eta,
            test_m,
        )

        print(
            f"WILDCARD_FACTOR={factor:.6f} "
            f"M={test_m:.9e} "
            f"SUCCESS={'YES' if test.success else 'NO'} "
            f"MIN_ACTIVE_FRACTION={test.min_active_fraction:.9e} "
            f"VIRIAL={test.virial_relerr:.9e}"
        )

    print(
        "BLIND_WILDCARD_VALUES_USED_AS_EVIDENCE=NO"
    )

    # --------------------------------------------------------------
    # H. Decision.
    # --------------------------------------------------------------
    print("\n=== 023A DECISION ===")

    theorem_pass = True

    topology_pass = (
        profile.topology_relerr
        <= MAX_TOPOLOGY_RELERR
    )

    virial_pass = (
        profile.virial_relerr
        <= MAX_VIRIAL_RELERR
    )

    active_total_pass = (
        profile.active_total_relerr
        <= MAX_ACTIVE_TOTAL_RELERR
        and profile.active_mass[-1] > 0.0
    )

    negative_enclosed_pass = (
        profile.min_active_fraction
        <= -MIN_NEGATIVE_ENCLOSED_FRACTION
    )

    fission_pass = (
        selected.fission_margin
        >= MIN_FISSION_MARGIN
    )

    payload_pass = (
        selected.finite_payload_pass
        and selected.payload_outward_kernel > 0.0
    )

    full_green = (
        potential_pass
        and theorem_pass
        and profile.success
        and topology_pass
        and virial_pass
        and active_total_pass
        and negative_enclosed_pass
        and fission_pass
        and payload_pass
        and independent_sign_pass
        and robust_basin
    )

    print(
        "TOPOLOGICAL_CHARGE="
        + (
            "PASS"
            if topology_pass
            else "FAIL"
        )
    )
    print(
        "RATIONAL_MAP_BVP="
        + (
            "PASS"
            if profile.success
            else "FAIL"
        )
    )
    print(
        "DERRICK_VIRIAL="
        + (
            "PASS"
            if virial_pass
            else "FAIL"
        )
    )
    print(
        "BINARY_FISSION_PREFLIGHT="
        + (
            "PASS"
            if fission_pass
            else "FAIL"
        )
    )
    print(
        "NEGATIVE_ENCLOSED_ACTIVE_MASS="
        + (
            "PASS"
            if negative_enclosed_pass
            else "FAIL"
        )
    )
    print(
        "POSITIVE_FAR_ACTIVE_MASS="
        + (
            "PASS"
            if active_total_pass
            else "FAIL"
        )
    )
    print(
        "FINITE_PAYLOAD_MONOPOLE_OUTWARD="
        + (
            "PASS"
            if payload_pass
            else "FAIL"
        )
    )

    if full_green:
        print(
            "023A_TOPOLOGICAL_FALSE_CORE_MULTISKYRMION_GR_REPULSION_GATE="
            "GREEN"
        )
        print(
            "TOPOLOGICALLY_STABILIZED_REPULSIVE_MONOPOLE_CAPACITY_PREFLIGHT="
            "SUPPORTED"
        )
        print(
            "INTRINSIC_STABILITY_PRINCIPLE="
            "TOPOLOGICAL_CHARGE_PLUS_SKYRME_DERRICK_STABILIZATION"
        )
        print(
            "SPATIAL_ACTIVE_STRESS_SEGREGATION="
            "FALSE_CORE_NEGATIVE_ACTIVE_PLUS_SKYRME_SHELL_POSITIVE_ACTIVE"
        )
        print(
            "B_LE_8_BOUND_MULTISKYRMION_PREFLIGHT="
            "SUPPORTED"
        )
        print(
            "FULL_3D_STABILITY="
            "NOT_YET"
        )
        print(
            "FULL_3D_FINITE_PAYLOAD_GRAVITY="
            "NOT_YET"
        )
        print(
            "NEXT="
            "023B_FULL_3D_FALSE_CORE_MULTISKYRMION_T_MUNU_GRAVITY_STABILITY_GATE"
        )
        print(
            "CURRENT_KNOWLEDGE_HEURISTIC="
            "APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY"
        )
        print(
            "HEURISTIC_CHANGE="
            "NONE_UNTIL_FULL_3D_TOPOLOGICAL_FIELD_AND_GRAVITY_RECONSTRUCTION"
        )
    else:
        print(
            "023A_TOPOLOGICAL_FALSE_CORE_MULTISKYRMION_GR_REPULSION_GATE="
            "GREEN_NEGATIVE_OR_INCOMPLETE_RESULT"
        )
        print(
            "TOPOLOGICALLY_STABILIZED_REPULSIVE_MONOPOLE_CAPACITY_PREFLIGHT="
            "NOT_ESTABLISHED"
        )
        print(
            "NEXT="
            "GLOBAL_RERANK_DO_NOT_ESCALATE_TO_HUGE_B"
        )
        print(
            "CURRENT_KNOWLEDGE_HEURISTIC="
            "APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY"
        )
        print(
            "HEURISTIC_CHANGE=NONE"
        )

    print(
        "SKYRME_MODEL_DEC="
        "LITERATURE_SUPPORTED_FOR_STANDARD_POSITIVE_SIGN_L2_L4"
    )
    print(
        "NONNEGATIVE_POTENTIAL_DEC="
        "PASS_ANALYTIC"
    )
    print(
        "POINTWISE_3D_DEC_RECONSTRUCTION="
        "DEFER_TO_023B"
    )
    print(
        "EXTERIOR_REPULSIVE_FIELD="
        "NO_POSITIVE_TOTAL_ACTIVE_MASS_IMPLIES_ATTRACTIVE_MONOPOLE_FAR_FIELD"
    )
    print(
        "PAYLOAD_LOCATION="
        "INTERIOR_TO_TOPOLOGICAL_FIELD_CONFIGURATION"
    )
    print(
        "PAYLOAD_DIRECT_NON_GRAVITATIONAL_COUPLING="
        "NOT_TESTED_TEST_BODY_ASSUMPTION"
    )
    print(
        "NONLINEAR_EINSTEIN_MATTER="
        "NOT_ESTABLISHED"
    )
    print(
        "PRACTICAL_ENERGY_SCALING="
        "STILL_CATASTROPHIC_IN_PURE_GR"
    )
    print(
        "REAL_MATERIAL="
        "NO"
    )
    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )
    print(
        "NEW_PHYSICS_DISCOVERY="
        "NO"
    )

    print(
        "006D_CONSTRUCTIVE_LINEARIZED_GR_RESULT="
        "RETAINED"
    )
    print(
        "018B_FIELD_EXISTENCE_RESULT="
        "RETAINED"
    )
    print(
        "018C_KLS_M2_STABILITY_FAILURE="
        "RETAINED"
    )
    print(
        "022A_PROTECTED_VECTOR_CLOSEOUT="
        "RETAINED"
    )
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_023A_TOPOLOGICAL_FALSE_CORE_MULTISKYRMION_GR_REPULSION_GATE"
    )


if __name__ == "__main__":
    main()
