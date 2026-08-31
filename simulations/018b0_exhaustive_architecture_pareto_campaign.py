#!/usr/bin/env python3
"""018B-0 — exhaustive architecture and wall-amplitude Pareto campaign.

PURPOSE
-------
Select the physically simplest and most informative target architecture for
the first true 018B full toroidal finite-thickness Euler-Lagrange solve.

018A-8 is GREEN.

It established, at the complete declared zero-temperature source-preflight
level:

    topology-consistent KLS-like microscopic wall;
    finite wall tension and thickness;
    fully coupled local wall/vortex junction;
    positive total active mass;
    finite-thickness finite-payload outward linearized gravity;
    finite rim-core robustness;
    healthy vorton EOS;
    radial effective stationarity;
    2187/2187 finite-thickness source-level robustness.

Therefore a full field solve is authorized.

However, before committing large computational resources to one global PDE
architecture, one remaining model-definition ambiguity should be removed.

The current effective global construction uses two equal counterrotating
vorton copies so that T_tphi cancels.

A single ordinary vorton is instead naturally stationary and carries angular
momentum.

The project already contains a later stationary-gravity/frame-dragging gate.
Thus exact cancellation of T_tphi is not itself required at this stage.

SCIENTIFIC QUESTION
-------------------
Is the current doubled counterrotating architecture actually the best
microscopic target for 018B, or can the already-demonstrated one-wall /
one-vortex topology be matched directly to one stationary gauged vorton while:

    retaining positive total active mass;
    retaining outward finite-payload gravity;
    retaining robust kernel leverage;
    retaining scale separation;
    satisfying radial stationarity;
    improving or preserving the energy coefficient;
    and avoiding an unnecessary second complete vorton sector?

CHEAPEST DECISIVE TEST
----------------------
Before a global toroidal PDE solve:

1. reconstruct the promoted 018A-8 source;
2. infer the one-copy 017P radial support directly from its stress;
3. independently reconstruct that support from the journaled pair load;
4. scan wall amplitude F;
5. scan vorton multiplicity m=1..4;
6. optimize the operational payload height h/R for each candidate;
7. enforce topology, quantization, active-mass, kernel, and scale gates;
8. identify the thin-wall asymptotic efficiency floor;
9. select Pareto knees instead of blindly driving F to zero;
10. subject all serious single-vorton finalists to a strong deterministic
    stress envelope;
11. apply an independent randomized stress test;
12. reconstruct the winner with the slower high-precision 018A-8 integrators.

THIS IS NOT 018B ITSELF
-----------------------
This calculation does NOT solve a new global matter-field PDE.

A favorable reparameterized single-vorton candidate must still rerun the
microscopic wall and fully coupled local junction at the selected F before it
can replace the already-promoted F=0.075 microscopic point.

Consequently:

    this scan alone cannot raise the project progress percentage;

    it cannot establish a new field-theoretical candidate;

    it cannot establish nonlinear GR;

    it cannot establish practical energy scaling.

Its purpose is to prevent the much more expensive 018B solve from targeting
an unnecessarily complicated or energetically inferior architecture.

PHYSICAL MODEL
--------------
The straight-string 017P integrated stress quantities for one vorton copy are

    U
      =
      2 omega^2 Sigma2
      +
      A_string

    P_parallel
      =
      2 k^2 Sigma2
      -
      A_string

    S_active
      =
      2 Sigma2
      (
        omega^2
        +
        k^2
      ).

The current project doubled these quantities using two counterrotating copies.

For m identical copies, with one local KLS wall/string junction contribution
for each copy, the effective radial support is

    L_radial
      =
      m
      (
        P_parallel
        -
        mu_J
      ).

The wall equilibrium radius is

    sigma_W R
      =
      L_radial.

Equivalently, in the existing Q/N normalization,

    Q_req
      =
      2 pi R / ell

and

    N_req
      =
      Q_req / (Q/N).

The nearest integer N is explicitly checked.

WALL REPARAMETERIZATION
-----------------------
The promoted wall has the far-from-vortex Ising profile

    A_x(z)
      =
      F tanh(k_W z)

with

    k_W
      =
      F sqrt(lambda_A) / 2.

The analytic frozen-Phi tension is

    sigma_W
      =
      4/3
      F^3
      sqrt(lambda_A).

018A-5 numerically reconstructed this relation to approximately 2e-4
relative accuracy.

This campaign therefore uses

    sigma_W(F)
      =
      r_sigma
      4/3
      F^3
      sqrt(lambda_A),

where r_sigma is calibrated from the promoted F=0.075 solution.

This is a controlled source-level continuation model, NOT a substitute for
rerunning the microscopic field equations at the newly selected F.

IMPORTANT SCALING
-----------------
For one vorton:

    R
      proportional to
      F^-3,

while

    delta_W
      proportional to
      F^-1.

Therefore

    R/delta_W
      proportional to
      F^-2.

Reducing F can make the finite wall effectively thinner relative to the
equilibrium drum even though its microscopic absolute width grows.

This is the mechanism being tested.

TOPOLOGY / LOCAL-STABILITY PREFLIGHT
------------------------------------
The same-gauge KLS-like construction uses:

    q_phi = 2;
    q_A   = 1;

with the phase-locking term

    phi^* A^2 + h.c.

The topological wall-number argument is unchanged for any nonzero F.

For every scanned F this file nevertheless checks:

    the vacuum radial Hessian is positive;
    the transverse Ising-wall mode remains positive;
    the gauge-mass shift remains small.

Using the established normalization,

    H_ff =
      2 lambda_phi v^2
      +
      2 h F^2/v

    H_AA =
      2 lambda_A F^2

    H_fA =
      -4 h F.

The transverse frozen-Phi wall eigenvalue is

    lambda_perp
      =
      4 h v
      -
      lambda_A F^2/4.

FINITE-PAYLOAD GRAVITY
----------------------
The exact spherical-payload overlap kernel introduced in 018A-8 is retained.

The wall integral is evaluated in the dimensionless coordinate

    y = k_W z.

Its normalized active-source profile is

    p(y)
      =
      3/4 sech^4(y).

Piecewise Gauss-Legendre integration explicitly splits the integral at:

    payload bottom;
    payload center;
    payload top.

This avoids the quadrature problem discovered in 018A-7.

The dense scout uses an infinitesimally thin positive rim.

This is conservative for the already-tested 018A-8 finite-core family because
the line limit gave the largest inward rim field there.

Every finalist is then reconstructed with the independent high-precision
018A-8 finite-core integration at:

    zero core width;
    one measured core width;
    two measured core widths.

SIGN CONVENTION
---------------
Positive vertical field factor means outward acceleration.

The finite-thickness wall contributes positively.

The ordinary positive-active vorton rim contributes inward.

Required:

    F_payload
      =
      F_wall
      -
      F_rim

      >
      0.

ACTIVE MASS
-----------
Required simultaneously:

    Q_plus
      >
      Q_minus.

Thus the candidate must remain attractive in its far-field monopole while
giving local finite-payload repulsion.

KERNEL LEVERAGE
---------------
Require

    kappa_minus/kappa_plus
      >
      Q_plus/Q_minus.

The reported margin is

    M_kernel
      =
      (kappa_minus/kappa_plus)
      /
      (Q_plus/Q_minus).

Require

    M_kernel > 1.

ENERGY COEFFICIENT
------------------
For each candidate,

    C_eff
      =
      (E_total/R)
      /
      [
        F_payload
        (h/R)^2
      ].

The one-meter / one-g diagnostic remains

    M_1g,1m
      =
      C_eff g/G

and

    E_1g,1m
      =
      M_1g,1m c^2.

The current 018A-8 result is independently reconstructed first.

MULTIPLICITY BRANCHES
---------------------
m=1:

    preferred minimal stationary-vorton architecture;
    nonzero total angular momentum;
    future 018D required.

m=2:

    current effective counterrotating-pair architecture;
    leading T_tphi can cancel;
    retained as the control.

m=3,4:

    diagnostic only;
    used to determine whether apparent gains are simply coming from adding
    more complete positive-energy support sectors.

No m>1 architecture is selected over a healthy m=1 solution merely because
its finite-thickness geometry looks slightly better.

This follows the project rule:

    prefer the minimal physically sufficient field content.

SCAN
----
Wall amplitude:

    0.020 <= F <= 0.085

using 326 points.

Multiplicity:

    m = 1,2,3,4.

Payload height ratio:

    0.003 <= h/R <= 0.040.

For every F,m the code:

    performs a coarse height scan;
    refines the best height continuously;
    checks topology;
    checks scale separation;
    checks integer winding;
    checks positive active mass;
    checks point and finite-payload outward gravity;
    checks kernel leverage;
    computes C_eff.

PARETO SELECTION
----------------
The thin-wall one-vorton efficiency floor is calculated independently.

Do NOT simply choose the smallest F.

Instead find the largest F whose C lies within each of:

    10%
    8%
    6%
    5%
    4%
    3%
    2%

of the asymptotic thin-wall minimum.

These are Pareto knees between:

    minimal departure from the already validated microscopic F;

and

    finite-thickness energy efficiency.

ROBUSTNESS
----------
Every serious single-vorton Pareto finalist is subjected to a deterministic
eight-dimensional stress lattice.

The dimensions are:

    F                  +/-10%
    radial support     +/-10%
    junction energy    x0.5, x1, x2
    base active line   +/-10%
    junction active    x0.5, x1, x2
    Q/N                +/-10%
    h/R                +/-10%
    wall-tension model +/-2%

Total per finalist:

    3^8 = 6561.

The energy coefficient is additionally evaluated pessimistically with:

    base line energy +10%;
    junction physical energy x2.

A deep robust candidate requires:

    all deterministic cases pass;
    minimum payload outward factor > 0.05;
    minimum kernel-leverage margin > 1.02;
    minimum scale separation > 15;
    integer mismatch < 1e-3.

After deterministic selection, run 20,000 continuous random perturbations over
the same uncertainty ranges.

PROMOTION CONDITION
-------------------
This run does not promote 018B.

It selects an 018B target.

If a robust m=1 candidate wins:

    018B_TARGET_ARCHITECTURE =
      SINGLE_STATIONARY_VORTON_PLUS_ONE_KLS_WALL

and the immediate next action is:

    rerun the microscopic wall;
    rerun the fully coupled local KLS junction;
    rerun complete gravity bookkeeping;

at the selected F.

If that revalidation is green, launch the true global 018B PDE.

If no robust m=1 candidate exists, retain the current pair only after explicitly
defining how the second complete vorton sector is realized microscopically.

FALSIFIERS
----------
The single-vorton simplification is rejected if no meaningful F interval can
simultaneously satisfy:

    positive active mass;
    finite-payload outward gravity;
    kernel leverage;
    topology/local wall stability;
    scale separation;
    quantization;
    robust uncertainty margins.

The project must not select a low-C point on a sign boundary.

APPROXIMATION LEVEL
-------------------
Source-level / thin-curvature architecture selection with measured finite wall
thickness.

Not a new global Euler-Lagrange solution.

Not a stability proof.

Not nonlinear GR.

Not a practical device.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018B0_ARCHITECTURE_PARETO_SCOUT
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import itertools
import math
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import minimize_scalar


ROOT = Path(__file__).resolve().parents[1]

SOURCE = (
    ROOT
    / "simulations"
    / "018a8_finite_thickness_payload_kernel_closeout.py"
)


def load_module(
    name: str,
    path: Path,
):
    """Import a verified project simulation without invoking its main()."""

    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            f"Cannot import {path}"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[
        name
    ] = module

    try:
        spec.loader.exec_module(
            module
        )
    except Exception:
        sys.modules.pop(
            name,
            None,
        )
        raise

    return module


g8 = load_module(
    "ag018a8_architecture_campaign",
    SOURCE,
)

b3 = g8.b3
b2 = g8.b2
fc = g8.fc
m = g8.m


# ============================================================================
# Campaign policy.
# ============================================================================

COPY_COUNTS = (
    1,
    2,
    3,
    4,
)

F_GRID = np.linspace(
    0.020,
    0.085,
    326,
)

X_GRID = np.linspace(
    0.003,
    0.040,
    96,
)

PARETO_THRESHOLDS = (
    1.10,
    1.08,
    1.06,
    1.05,
    1.04,
    1.03,
    1.02,
)

PAYLOAD_RADIUS_OVER_H = 0.25

MIN_SCALE_SEPARATION = 10.0
MIN_DEEP_SCALE_SEPARATION = 15.0

MAX_INTEGER_MISMATCH = 1.0e-3

MIN_DEEP_PAYLOAD_MARGIN = 0.05
MIN_DEEP_LEVERAGE_MARGIN = 1.02

SCOUT_GL_ORDER = 24
HIGH_GL_ORDER = 48

RANDOM_STRESS_CASES = 20000
RANDOM_SEED = 180180

CURRENT_EXPECTED_C = (
    1.774169582609975e6
)

CURRENT_EXPECTED_ENERGY_J = (
    2.342887778715687e34
)

G_SI = 6.67430e-11
C_SI = 299792458.0
G0_SI = 9.80665


# ============================================================================
# Established KLS potential constants.
# ============================================================================

V_PHI = 1.0
LAMBDA_PHI = 1.0

H_LOCK = 0.01


@dataclass(
    frozen=True
)
class Anchors:
    """Promoted 018A/017P quantities needed by the architecture campaign."""

    f0: float
    lambda_a: float
    sigma0: float
    tension_calibration: float

    mu_j: float
    delta_sigma2: float
    endpoint_active: float

    sigma2: float
    a_string: float

    omega: float
    k_long: float

    ell: float
    q_over_n: float

    p_parallel_stress: float
    p_parallel_calibrated: float

    base_energy_one: float
    base_active_one: float
    junction_energy_one: float

    rim_core_width: float


def reconstruct_anchors() -> Anchors:
    """Reconstruct all source quantities instead of hard-coding scan inputs."""

    outer, _, outer_pass = (
        b3.global_outer_morphology()
    )

    if not outer_pass:
        raise RuntimeError(
            "Promoted outer wall reconstruction is no longer green."
        )

    selected = (
        b3.matched_pair(
            g8.CHI_SELECTED,
            81,
            20.0,
        )
    )

    if not (
        selected[
            "full"
        ].success
        and
        selected[
            "base"
        ].success
    ):
        raise RuntimeError(
            "Promoted fully coupled local junction no longer reconstructs."
        )

    full = (
        selected[
            "full"
        ]
    )

    _, diag = (
        b2.global_fixed_case(
            g8.CHI_SELECTED
        )
    )

    sigma0 = float(
        m.SIGMA_W_RELAXED_018A5
    )

    f0 = float(
        m.F_A
    )

    lambda_a = float(
        m.LAMBDA_A
    )

    analytic_sigma0 = (
        4.0
        /
        3.0
        *
        f0**3
        *
        math.sqrt(
            lambda_a
        )
    )

    tension_calibration = (
        sigma0
        /
        analytic_sigma0
    )

    mu_j = float(
        outer.junction_excess_energy
        +
        selected[
            "delta_e"
        ]
    )

    delta_sigma2 = float(
        selected[
            "delta_sigma2"
        ]
    )

    endpoint_active = float(
        selected[
            "endpoint_active"
        ]
    )

    sigma2 = float(
        full.sigma2_background
    )

    a_string = float(
        diag.a_string
    )

    omega = float(
        g8.OMEGA
    )

    k_long = float(
        g8.K_LONG
    )

    ell = float(
        fc.ELL
    )

    q_over_n = float(
        fc.Q_OVER_N
    )

    p_parallel_stress = (
        2.0
        *
        k_long**2
        *
        sigma2
        -
        a_string
    )

    # The promoted 017P pair wall-load coefficient supplies an independent
    # reconstruction of the one-copy longitudinal support.
    p_parallel_calibrated = (
        float(
            fc.W_STAT
        )
        *
        ell
        /
        (
            4.0
            *
            math.pi
        )
    )

    base_energy_one = (
        2.0
        *
        omega**2
        *
        sigma2
        +
        a_string
    )

    base_active_one = (
        2.0
        *
        sigma2
        *
        (
            omega**2
            +
            k_long**2
        )
    )

    junction_energy_one = (
        mu_j
        +
        2.0
        *
        omega**2
        *
        delta_sigma2
    )

    return Anchors(
        f0=f0,
        lambda_a=lambda_a,
        sigma0=sigma0,
        tension_calibration=tension_calibration,
        mu_j=mu_j,
        delta_sigma2=delta_sigma2,
        endpoint_active=endpoint_active,
        sigma2=sigma2,
        a_string=a_string,
        omega=omega,
        k_long=k_long,
        ell=ell,
        q_over_n=q_over_n,
        p_parallel_stress=p_parallel_stress,
        p_parallel_calibrated=p_parallel_calibrated,
        base_energy_one=base_energy_one,
        base_active_one=base_active_one,
        junction_energy_one=junction_energy_one,
        rim_core_width=float(
            m.A_CORE_WIDTH
        ),
    )


# ============================================================================
# Wall model and topology.
# ============================================================================


def wall_tension(
    anchors: Anchors,
    f_value: float,
) -> float:
    """Continue the exactly known Ising-wall F^3 tension law."""

    return (
        anchors.tension_calibration
        *
        4.0
        /
        3.0
        *
        f_value**3
        *
        math.sqrt(
            anchors.lambda_a
        )
    )


def wall_k(
    anchors: Anchors,
    f_value: float,
) -> float:
    """Return the inverse Ising-wall profile scale."""

    return (
        f_value
        *
        math.sqrt(
            anchors.lambda_a
        )
        /
        2.0
    )


def wall_width90(
    anchors: Anchors,
    f_value: float,
) -> float:
    """Return the 90-percent amplitude wall width."""

    return (
        2.0
        *
        math.atanh(
            0.9
        )
        /
        wall_k(
            anchors,
            f_value,
        )
    )


def topology_metrics(
    anchors: Anchors,
    f_value: float,
) -> dict[str, float | bool]:
    """Evaluate vacuum and transverse-wall local-stability margins."""

    h_ff = (
        2.0
        *
        LAMBDA_PHI
        *
        V_PHI**2

        +
        2.0
        *
        H_LOCK
        *
        f_value**2
        /
        V_PHI
    )

    h_aa = (
        2.0
        *
        anchors.lambda_a
        *
        f_value**2
    )

    h_fa = (
        -4.0
        *
        H_LOCK
        *
        f_value
    )

    eigvals = np.linalg.eigvalsh(
        np.array(
            [
                [
                    h_ff,
                    h_fa,
                ],
                [
                    h_fa,
                    h_aa,
                ],
            ],
            dtype=float,
        )
    )

    transverse = (
        4.0
        *
        H_LOCK
        *
        V_PHI

        -
        anchors.lambda_a
        *
        f_value**2
        /
        4.0
    )

    gauge_shift = (
        f_value**2
        /
        (
            4.0
            *
            V_PHI**2
        )
    )

    passed = (
        f_value
        >
        0.0

        and
        float(
            eigvals[
                0
            ]
        )
        >
        0.0

        and
        transverse
        >
        0.0

        and
        gauge_shift
        <
        0.01
    )

    return {
        "min_hessian_eigenvalue":
            float(
                eigvals[
                    0
                ]
            ),

        "transverse_eigenvalue":
            float(
                transverse
            ),

        "gauge_mass_shift_fraction":
            float(
                gauge_shift
            ),

        "pass":
            bool(
                passed
            ),
    }


# ============================================================================
# Fast exact-overlap wall integrator.
# ============================================================================


def make_gauss_rule(
    order: int,
):
    """Return the reusable Gauss-Legendre rule."""

    return leggauss(
        order
    )


SCOUT_NODES, SCOUT_WEIGHTS = (
    make_gauss_rule(
        SCOUT_GL_ORDER
    )
)

HIGH_NODES, HIGH_WEIGHTS = (
    make_gauss_rule(
        HIGH_GL_ORDER
    )
)


def integrate_segment(
    left: float,
    right: float,
    function,
    nodes: np.ndarray,
    weights: np.ndarray,
) -> float:
    """Integrate one smooth segment with fixed Gauss-Legendre quadrature."""

    if right <= left:
        return 0.0

    y = (
        0.5
        *
        (
            right
            -
            left
        )
        *
        nodes

        +
        0.5
        *
        (
            right
            +
            left
        )
    )

    w = (
        0.5
        *
        (
            right
            -
            left
        )
        *
        weights
    )

    return float(
        np.sum(
            w
            *
            function(
                y
            )
        )
    )


def normalized_profile_y(
    y: np.ndarray,
) -> np.ndarray:
    """Return p(y)=3/4 sech^4(y)."""

    return (
        0.75
        /
        np.cosh(
            y
        ) ** 4
    )


def point_radial_unit(
    d: np.ndarray,
) -> np.ndarray:
    """Unit-radius radial integral of the point-target vertical kernel."""

    return (
        np.sign(
            d
        )
        -
        d
        /
        np.sqrt(
            1.0
            +
            d
            *
            d
        )
    )


def payload_radial_unit(
    d: np.ndarray,
    payload_radius_over_r: float,
) -> np.ndarray:
    """Unit-radius exact spherical-payload radial kernel integral."""

    a = float(
        payload_radius_over_r
    )

    abs_d = np.abs(
        d
    )

    result = np.empty_like(
        d
    )

    outside = (
        abs_d
        >=
        a
    )

    result[
        outside
    ] = (
        d[
            outside
        ]
        *
        (
            1.0
            /
            abs_d[
                outside
            ]

            -
            1.0
            /
            np.sqrt(
                1.0
                +
                d[
                    outside
                ] ** 2
            )
        )
    )

    inside = ~outside

    di = (
        d[
            inside
        ]
    )

    result[
        inside
    ] = (
        di
        /
        a**3
        *
        (
            a**2
            -
            di**2
        )
        /
        2.0

        +
        di
        *
        (
            1.0
            /
            a

            -
            1.0
            /
            np.sqrt(
                1.0
                +
                di**2
            )
        )
    )

    return result


def wall_kernel_factors(
    sigma_wall: float,
    k_wall: float,
    radius: float,
    x: float,
    *,
    high_precision: bool,
) -> tuple[float, float]:
    """Return finite-thickness wall point and finite-payload factors.

    The integration is split at every payload-kernel branch point.
    """

    beta = (
        k_wall
        *
        radius
    )

    payload_radius = (
        PAYLOAD_RADIUS_OVER_H
        *
        x
    )

    nodes = (
        HIGH_NODES
        if high_precision
        else SCOUT_NODES
    )

    weights = (
        HIGH_WEIGHTS
        if high_precision
        else SCOUT_WEIGHTS
    )

    y_max = 14.0

    raw_cuts = [
        -y_max,

        beta
        *
        (
            x
            -
            payload_radius
        ),

        beta
        *
        x,

        beta
        *
        (
            x
            +
            payload_radius
        ),

        y_max,
    ]

    cuts = sorted(
        set(
            max(
                -y_max,
                min(
                    y_max,
                    float(
                        value
                    ),
                ),
            )
            for value
            in raw_cuts
        )
    )

    def point_integrand(
        y: np.ndarray,
    ) -> np.ndarray:

        d = (
            x
            -
            y
            /
            beta
        )

        return (
            normalized_profile_y(
                y
            )
            *
            point_radial_unit(
                d
            )
        )

    def payload_integrand(
        y: np.ndarray,
    ) -> np.ndarray:

        d = (
            x
            -
            y
            /
            beta
        )

        return (
            normalized_profile_y(
                y
            )
            *
            payload_radial_unit(
                d,
                payload_radius,
            )
        )

    normalization = 0.0
    point_expectation = 0.0
    payload_expectation = 0.0

    for index in range(
        len(
            cuts
        )
        -
        1
    ):

        left = cuts[
            index
        ]

        right = cuts[
            index
            +
            1
        ]

        normalization += integrate_segment(
            left,
            right,
            normalized_profile_y,
            nodes,
            weights,
        )

        point_expectation += integrate_segment(
            left,
            right,
            point_integrand,
            nodes,
            weights,
        )

        payload_expectation += integrate_segment(
            left,
            right,
            payload_integrand,
            nodes,
            weights,
        )

    scale = (
        2.0
        *
        math.pi
        *
        sigma_wall
        *
        radius
        /
        normalization
    )

    return (
        float(
            scale
            *
            point_expectation
        ),

        float(
            scale
            *
            payload_expectation
        ),
    )


# ============================================================================
# Architecture evaluation.
# ============================================================================


def evaluate_case(
    anchors: Anchors,
    f_value: float,
    copies: int,
    x: float,
    *,
    pressure_factor: float = 1.0,
    mu_factor: float = 1.0,
    base_active_factor: float = 1.0,
    endpoint_active_factor: float = 1.0,
    q_factor: float = 1.0,
    tension_factor: float = 1.0,
    base_energy_factor: float = 1.0,
    junction_energy_factor: float = 1.0,
    high_precision: bool = False,
) -> dict[str, float | bool]:
    """Evaluate one stationary thin-curvature architecture candidate."""

    topology = (
        topology_metrics(
            anchors,
            f_value,
        )
    )

    sigma_wall = (
        wall_tension(
            anchors,
            f_value,
        )
        *
        tension_factor
    )

    k_wall = (
        wall_k(
            anchors,
            f_value,
        )
    )

    p_parallel = (
        anchors.p_parallel_calibrated
        *
        pressure_factor
    )

    mu_j = (
        anchors.mu_j
        *
        mu_factor
    )

    support_per_copy = (
        p_parallel
        -
        mu_j
    )

    if support_per_copy <= 0.0:

        return {
            "pass":
                False,

            "c_eff":
                math.inf,

            "payload_outward":
                -math.inf,

            "point_outward":
                -math.inf,

            "leverage_margin":
                -math.inf,

            "min_scale":
                0.0,

            "integer_mismatch":
                math.inf,
        }

    total_support = (
        copies
        *
        support_per_copy
    )

    radius = (
        total_support
        /
        sigma_wall
    )

    q_over_n = (
        anchors.q_over_n
        *
        q_factor
    )

    q_required = (
        2.0
        *
        math.pi
        *
        radius
        /
        anchors.ell
    )

    n_required = (
        q_required
        /
        q_over_n
    )

    n_integer = max(
        1,
        int(
            round(
                n_required
            )
        ),
    )

    w_required = (
        2.0
        *
        math.pi
        *
        total_support
        /
        anchors.ell
    )

    integer_mismatch = (
        abs(
            sigma_wall
            *
            n_integer
            *
            q_over_n
            -
            w_required
        )
        /
        w_required
    )

    active_line = (
        copies
        *
        (
            anchors.base_active_one
            *
            base_active_factor

            +
            anchors.endpoint_active
            *
            endpoint_active_factor
        )
    )

    energy_line = (
        copies
        *
        (
            anchors.base_energy_one
            *
            base_energy_factor

            +
            anchors.junction_energy_one
            *
            junction_energy_factor
        )
    )

    (
        wall_point,
        wall_payload,
    ) = (
        wall_kernel_factors(
            sigma_wall,
            k_wall,
            radius,
            x,
            high_precision=high_precision,
        )
    )

    rim_inward = (
        2.0
        *
        math.pi
        *
        active_line
        *
        x
        /
        (
            1.0
            +
            x
            *
            x
        ) ** 1.5
    )

    point_outward = (
        wall_point
        -
        rim_inward
    )

    payload_outward = (
        wall_payload
        -
        rim_inward
    )

    positive_active_per_r = (
        2.0
        *
        math.pi
        *
        active_line
    )

    negative_active_per_r = (
        math.pi
        *
        sigma_wall
        *
        radius
    )

    active_mass_per_r = (
        positive_active_per_r
        -
        negative_active_per_r
    )

    if (
        positive_active_per_r
        >
        0.0

        and
        negative_active_per_r
        >
        0.0

        and
        rim_inward
        >
        0.0
    ):

        kappa_positive = (
            rim_inward
            /
            positive_active_per_r
        )

        kappa_negative = (
            wall_payload
            /
            negative_active_per_r
        )

        active_ratio = (
            positive_active_per_r
            /
            negative_active_per_r
        )

        leverage_ratio = (
            kappa_negative
            /
            kappa_positive
        )

        leverage_margin = (
            leverage_ratio
            /
            active_ratio
        )

    else:

        leverage_margin = (
            -math.inf
        )

    width90 = (
        wall_width90(
            anchors,
            f_value,
        )
    )

    r_over_wall = (
        radius
        /
        width90
    )

    r_over_core = (
        radius
        /
        anchors.rim_core_width
    )

    min_scale = min(
        r_over_wall,
        r_over_core,
    )

    energy_per_r = (
        2.0
        *
        math.pi
        *
        energy_line

        +
        math.pi
        *
        sigma_wall
        *
        radius
    )

    if payload_outward > 0.0:

        c_eff = (
            energy_per_r
            /
            (
                payload_outward
                *
                x
                *
                x
            )
        )

    else:

        c_eff = (
            math.inf
        )

    passed = (
        bool(
            topology[
                "pass"
            ]
        )

        and
        point_outward
        >
        0.0

        and
        payload_outward
        >
        0.0

        and
        active_mass_per_r
        >
        0.0

        and
        leverage_margin
        >
        1.0

        and
        min_scale
        >=
        MIN_SCALE_SEPARATION

        and
        integer_mismatch
        <=
        MAX_INTEGER_MISMATCH
    )

    return {
        "pass":
            bool(
                passed
            ),

        "f":
            float(
                f_value
            ),

        "copies":
            float(
                copies
            ),

        "x":
            float(
                x
            ),

        "sigma_wall":
            float(
                sigma_wall
            ),

        "k_wall":
            float(
                k_wall
            ),

        "radius":
            float(
                radius
            ),

        "q_required":
            float(
                q_required
            ),

        "n_required":
            float(
                n_required
            ),

        "n_integer":
            float(
                n_integer
            ),

        "integer_mismatch":
            float(
                integer_mismatch
            ),

        "wall_point":
            float(
                wall_point
            ),

        "wall_payload":
            float(
                wall_payload
            ),

        "rim_inward":
            float(
                rim_inward
            ),

        "point_outward":
            float(
                point_outward
            ),

        "payload_outward":
            float(
                payload_outward
            ),

        "active_mass_per_r":
            float(
                active_mass_per_r
            ),

        "leverage_margin":
            float(
                leverage_margin
            ),

        "r_over_wall":
            float(
                r_over_wall
            ),

        "r_over_core":
            float(
                r_over_core
            ),

        "min_scale":
            float(
                min_scale
            ),

        "energy_per_r":
            float(
                energy_per_r
            ),

        "c_eff":
            float(
                c_eff
            ),

        "min_hessian_eigenvalue":
            float(
                topology[
                    "min_hessian_eigenvalue"
                ]
            ),

        "transverse_eigenvalue":
            float(
                topology[
                    "transverse_eigenvalue"
                ]
            ),

        "gauge_mass_shift_fraction":
            float(
                topology[
                    "gauge_mass_shift_fraction"
                ]
            ),
    }


def optimize_x(
    anchors: Anchors,
    f_value: float,
    copies: int,
) -> dict[str, float | bool] | None:
    """Optimize the payload height without hiding failed physical gates."""

    coarse = [
        evaluate_case(
            anchors,
            f_value,
            copies,
            float(
                x
            ),
        )
        for x in X_GRID
    ]

    finite_indices = [
        index
        for (
            index,
            result,
        )
        in enumerate(
            coarse
        )
        if result[
            "pass"
        ]
        and
        math.isfinite(
            float(
                result[
                    "c_eff"
                ]
            )
        )
    ]

    if not finite_indices:
        return None

    best_index = min(
        finite_indices,
        key=lambda index:
            float(
                coarse[
                    index
                ][
                    "c_eff"
                ]
            ),
    )

    lower_index = max(
        0,
        best_index
        -
        1,
    )

    upper_index = min(
        len(
            X_GRID
        )
        -
        1,
        best_index
        +
        1,
    )

    lower = float(
        X_GRID[
            lower_index
        ]
    )

    upper = float(
        X_GRID[
            upper_index
        ]
    )

    if upper <= lower:
        return coarse[
            best_index
        ]

    def objective(
        x: float,
    ) -> float:

        result = evaluate_case(
            anchors,
            f_value,
            copies,
            x,
        )

        if not result[
            "pass"
        ]:

            return 1.0e100

        return float(
            result[
                "c_eff"
            ]
        )

    refined = minimize_scalar(
        objective,
        bounds=(
            lower,
            upper,
        ),
        method="bounded",
        options={
            "xatol":
                1.0e-9,

            "maxiter":
                200,
        },
    )

    result = evaluate_case(
        anchors,
        f_value,
        copies,
        float(
            refined.x
        ),
    )

    if not result[
        "pass"
    ]:
        return coarse[
            best_index
        ]

    return result


# ============================================================================
# Thin-limit control.
# ============================================================================


def thin_limit_case(
    anchors: Anchors,
    copies: int,
    x: float,
) -> dict[str, float]:
    """Evaluate the exact zero-thickness-wall limit."""

    support = (
        copies
        *
        (
            anchors.p_parallel_calibrated
            -
            anchors.mu_j
        )
    )

    wall = (
        2.0
        *
        math.pi
        *
        support
        *
        (
            1.0

            -
            x
            /
            math.sqrt(
                1.0
                +
                x
                *
                x
            )
        )
    )

    active_line = (
        copies
        *
        (
            anchors.base_active_one
            +
            anchors.endpoint_active
        )
    )

    rim = (
        2.0
        *
        math.pi
        *
        active_line
        *
        x
        /
        (
            1.0
            +
            x
            *
            x
        ) ** 1.5
    )

    net = (
        wall
        -
        rim
    )

    energy_line = (
        copies
        *
        (
            anchors.base_energy_one
            +
            anchors.junction_energy_one
        )
    )

    energy_per_r = (
        2.0
        *
        math.pi
        *
        energy_line

        +
        math.pi
        *
        support
    )

    c_eff = (
        energy_per_r
        /
        (
            net
            *
            x
            *
            x
        )
        if net > 0.0
        else math.inf
    )

    return {
        "x":
            float(
                x
            ),

        "net":
            float(
                net
            ),

        "c_eff":
            float(
                c_eff
            ),
    }


def optimize_thin_limit(
    anchors: Anchors,
) -> dict[str, float]:
    """Find the independent single-vorton thin-wall efficiency floor."""

    grid = np.linspace(
        0.003,
        0.040,
        2000,
    )

    values = [
        thin_limit_case(
            anchors,
            1,
            float(
                x
            ),
        )
        for x in grid
    ]

    finite = [
        result
        for result
        in values
        if math.isfinite(
            result[
                "c_eff"
            ]
        )
    ]

    best = min(
        finite,
        key=lambda result:
            result[
                "c_eff"
            ],
    )

    best_index = int(
        np.argmin(
            [
                result[
                    "c_eff"
                ]
                for result
                in values
            ]
        )
    )

    lo = float(
        grid[
            max(
                0,
                best_index
                -
                1,
            )
        ]
    )

    hi = float(
        grid[
            min(
                len(
                    grid
                )
                -
                1,
                best_index
                +
                1,
            )
        ]
    )

    refined = minimize_scalar(
        lambda x:
            thin_limit_case(
                anchors,
                1,
                x,
            )[
                "c_eff"
            ],
        bounds=(
            lo,
            hi,
        ),
        method="bounded",
        options={
            "xatol":
                1.0e-12,
        },
    )

    return thin_limit_case(
        anchors,
        1,
        float(
            refined.x
        ),
    )


# ============================================================================
# Deterministic and randomized robustness.
# ============================================================================


def deterministic_stress(
    anchors: Anchors,
    candidate: dict[str, float | bool],
) -> dict[str, object]:
    """Run the complete 3^8 architecture stress lattice."""

    levels = (
        0.90,
        1.00,
        1.10,
    )

    junction_levels = (
        0.50,
        1.00,
        2.00,
    )

    tension_levels = (
        0.98,
        1.00,
        1.02,
    )

    total = 0
    passed = 0

    min_payload = math.inf
    min_point = math.inf
    min_active = math.inf
    min_leverage = math.inf
    min_scale = math.inf

    max_integer_mismatch = 0.0
    max_c = 0.0

    worst_payload_case = None

    for (
        f_f,
        f_pressure,
        f_mu,
        f_base_active,
        f_endpoint,
        f_q,
        f_x,
        f_tension,
    ) in itertools.product(
        levels,
        levels,
        junction_levels,
        levels,
        junction_levels,
        levels,
        levels,
        tension_levels,
    ):

        total += 1

        result = evaluate_case(
            anchors,
            float(
                candidate[
                    "f"
                ]
            )
            *
            f_f,
            1,
            float(
                candidate[
                    "x"
                ]
            )
            *
            f_x,
            pressure_factor=f_pressure,
            mu_factor=f_mu,
            base_active_factor=f_base_active,
            endpoint_active_factor=f_endpoint,
            q_factor=f_q,
            tension_factor=f_tension,

            # Conservative energy-only stress. These do not influence
            # the force sign or stationarity.
            base_energy_factor=1.10,
            junction_energy_factor=2.00,
        )

        if result[
            "pass"
        ]:
            passed += 1

        payload = float(
            result[
                "payload_outward"
            ]
        )

        if payload < min_payload:

            min_payload = payload

            worst_payload_case = {
                "F_FACTOR":
                    f_f,

                "PRESSURE_FACTOR":
                    f_pressure,

                "MU_FACTOR":
                    f_mu,

                "BASE_ACTIVE_FACTOR":
                    f_base_active,

                "ENDPOINT_ACTIVE_FACTOR":
                    f_endpoint,

                "Q_OVER_N_FACTOR":
                    f_q,

                "X_FACTOR":
                    f_x,

                "TENSION_FACTOR":
                    f_tension,
            }

        min_point = min(
            min_point,
            float(
                result[
                    "point_outward"
                ]
            ),
        )

        min_active = min(
            min_active,
            float(
                result.get(
                    "active_mass_per_r",
                    -math.inf,
                )
            ),
        )

        min_leverage = min(
            min_leverage,
            float(
                result[
                    "leverage_margin"
                ]
            ),
        )

        min_scale = min(
            min_scale,
            float(
                result[
                    "min_scale"
                ]
            ),
        )

        max_integer_mismatch = max(
            max_integer_mismatch,
            float(
                result[
                    "integer_mismatch"
                ]
            ),
        )

        c_eff = float(
            result[
                "c_eff"
            ]
        )

        if math.isfinite(
            c_eff
        ):

            max_c = max(
                max_c,
                c_eff,
            )

        else:

            max_c = math.inf

    all_pass = (
        passed
        ==
        total
    )

    deep_pass = (
        all_pass

        and
        min_payload
        >
        MIN_DEEP_PAYLOAD_MARGIN

        and
        min_leverage
        >
        MIN_DEEP_LEVERAGE_MARGIN

        and
        min_scale
        >
        MIN_DEEP_SCALE_SEPARATION

        and
        max_integer_mismatch
        <
        MAX_INTEGER_MISMATCH
    )

    return {
        "total":
            total,

        "passed":
            passed,

        "all_pass":
            all_pass,

        "deep_pass":
            deep_pass,

        "min_payload":
            min_payload,

        "min_point":
            min_point,

        "min_active":
            min_active,

        "min_leverage":
            min_leverage,

        "min_scale":
            min_scale,

        "max_integer_mismatch":
            max_integer_mismatch,

        "max_c":
            max_c,

        "worst_payload_case":
            worst_payload_case,
    }


def randomized_stress(
    anchors: Anchors,
    candidate: dict[str, float | bool],
) -> dict[str, float | int | bool]:
    """Run a continuous 20k adversarial Monte Carlo around the selected point."""

    rng = np.random.default_rng(
        RANDOM_SEED
    )

    passed = 0

    min_payload = math.inf
    min_leverage = math.inf
    min_scale = math.inf
    max_integer_mismatch = 0.0

    for _ in range(
        RANDOM_STRESS_CASES
    ):

        f_f = rng.uniform(
            0.90,
            1.10,
        )

        f_pressure = rng.uniform(
            0.90,
            1.10,
        )

        # Log-uniform gives equal weight to multiplicative deviations.
        f_mu = math.exp(
            rng.uniform(
                math.log(
                    0.50
                ),
                math.log(
                    2.00
                ),
            )
        )

        f_base_active = rng.uniform(
            0.90,
            1.10,
        )

        f_endpoint = math.exp(
            rng.uniform(
                math.log(
                    0.50
                ),
                math.log(
                    2.00
                ),
            )
        )

        f_q = rng.uniform(
            0.90,
            1.10,
        )

        f_x = rng.uniform(
            0.90,
            1.10,
        )

        f_tension = rng.uniform(
            0.98,
            1.02,
        )

        result = evaluate_case(
            anchors,
            float(
                candidate[
                    "f"
                ]
            )
            *
            f_f,
            1,
            float(
                candidate[
                    "x"
                ]
            )
            *
            f_x,
            pressure_factor=f_pressure,
            mu_factor=f_mu,
            base_active_factor=f_base_active,
            endpoint_active_factor=f_endpoint,
            q_factor=f_q,
            tension_factor=f_tension,
            high_precision=False,
        )

        if result[
            "pass"
        ]:
            passed += 1

        min_payload = min(
            min_payload,
            float(
                result[
                    "payload_outward"
                ]
            ),
        )

        min_leverage = min(
            min_leverage,
            float(
                result[
                    "leverage_margin"
                ]
            ),
        )

        min_scale = min(
            min_scale,
            float(
                result[
                    "min_scale"
                ]
            ),
        )

        max_integer_mismatch = max(
            max_integer_mismatch,
            float(
                result[
                    "integer_mismatch"
                ]
            ),
        )

    all_pass = (
        passed
        ==
        RANDOM_STRESS_CASES
    )

    return {
        "total":
            RANDOM_STRESS_CASES,

        "passed":
            passed,

        "all_pass":
            all_pass,

        "min_payload":
            min_payload,

        "min_leverage":
            min_leverage,

        "min_scale":
            min_scale,

        "max_integer_mismatch":
            max_integer_mismatch,
    }


# ============================================================================
# High precision independent reconstruction.
# ============================================================================


def high_precision_selected(
    anchors: Anchors,
    candidate: dict[str, float | bool],
) -> dict[str, float | bool]:
    """Use the independent 018A-8 adaptive wall and finite-core rim routines."""

    f_value = float(
        candidate[
            "f"
        ]
    )

    x = float(
        candidate[
            "x"
        ]
    )

    nominal = evaluate_case(
        anchors,
        f_value,
        1,
        x,
        high_precision=True,
    )

    sigma_wall = float(
        nominal[
            "sigma_wall"
        ]
    )

    radius = float(
        nominal[
            "radius"
        ]
    )

    k_wall = float(
        nominal[
            "k_wall"
        ]
    )

    h = (
        x
        *
        radius
    )

    payload_radius = (
        PAYLOAD_RADIUS_OVER_H
        *
        h
    )

    adaptive_wall = (
        g8.wall_gravity_factors(
            sigma_wall,
            k_wall,
            radius,
            h,
            payload_radius,
        )
    )

    active_line = (
        anchors.base_active_one
        +
        anchors.endpoint_active
    )

    (
        rim_values,
        rim_worst,
    ) = (
        g8.rim_envelope(
            active_line,
            radius,
            h,
            payload_radius,
            anchors.rim_core_width,
            high_precision=True,
        )
    )

    point = (
        float(
            adaptive_wall[
                "point"
            ]
        )
        -
        rim_worst
    )

    payload = (
        float(
            adaptive_wall[
                "payload"
            ]
        )
        -
        rim_worst
    )

    energy_per_r = (
        float(
            nominal[
                "energy_per_r"
            ]
        )
    )

    c_eff = (
        energy_per_r
        /
        (
            payload
            *
            x
            *
            x
        )
    )

    wall_point_relerr = (
        abs(
            float(
                adaptive_wall[
                    "point"
                ]
            )
            -
            float(
                nominal[
                    "wall_point"
                ]
            )
        )
        /
        abs(
            float(
                adaptive_wall[
                    "point"
                ]
            )
        )
    )

    wall_payload_relerr = (
        abs(
            float(
                adaptive_wall[
                    "payload"
                ]
            )
            -
            float(
                nominal[
                    "wall_payload"
                ]
            )
        )
        /
        abs(
            float(
                adaptive_wall[
                    "payload"
                ]
            )
        )
    )

    return {
        "point":
            float(
                point
            ),

        "payload":
            float(
                payload
            ),

        "c_eff":
            float(
                c_eff
            ),

        "wall_point_relerr":
            float(
                wall_point_relerr
            ),

        "wall_payload_relerr":
            float(
                wall_payload_relerr
            ),

        "rim_values":
            rim_values,

        "rim_worst":
            float(
                rim_worst
            ),

        "pass":
            bool(
                point
                >
                0.0

                and
                payload
                >
                0.0

                and
                wall_point_relerr
                <
                5.0e-6

                and
                wall_payload_relerr
                <
                5.0e-6
            ),
    }


# ============================================================================
# Utilities.
# ============================================================================


def energy_scaling(
    c_eff: float,
) -> tuple[float, float]:
    """Return one-meter / one-g mass and energy equivalents."""

    mass = (
        c_eff
        *
        G0_SI
        /
        G_SI
    )

    energy = (
        mass
        *
        C_SI**2
    )

    return (
        float(
            mass
        ),
        float(
            energy
        ),
    )


def print_candidate(
    prefix: str,
    result: dict[str, float | bool],
) -> None:
    """Print the central candidate quantities in a compact machine-readable row."""

    print(
        f"{prefix} "
        f"F={float(result['f']):.9f} "
        f"COPIES={int(float(result['copies']))} "
        f"X={float(result['x']):.12f} "
        f"C={float(result['c_eff']):.15e} "
        f"R={float(result['radius']):.15e} "
        f"N_REQ={float(result['n_required']):.15e} "
        f"N_INT={int(float(result['n_integer']))} "
        f"INTEGER_MISMATCH={float(result['integer_mismatch']):.15e} "
        f"PAYLOAD_OUTWARD={float(result['payload_outward']):+.15e} "
        f"POINT_OUTWARD={float(result['point_outward']):+.15e} "
        f"LEVERAGE={float(result['leverage_margin']):.15e} "
        f"R_OVER_WALL={float(result['r_over_wall']):.12f} "
        f"R_OVER_CORE={float(result['r_over_core']):.12f}"
    )


# ============================================================================
# Main campaign.
# ============================================================================


def main() -> None:
    """Execute the exhaustive architecture-selection campaign."""

    anchors = (
        reconstruct_anchors()
    )

    print(
        "=== ANTIGRAVITY_RESEARCH 018B-0 ==="
    )

    print(
        "QUESTION="
        "WHAT_IS_THE_MINIMAL_ROBUST_MICROSCOPIC_ARCHITECTURE_TO_TARGET_WITH_THE_FULL_018B_TOROIDAL_FIELD_SOLVER"
    )

    # ========================================================================
    # Anchor audit.
    # ========================================================================

    print(
        "\n=== 017P / 018A ANCHOR AUDIT ==="
    )

    pressure_relerr = (
        abs(
            anchors.p_parallel_stress
            -
            anchors.p_parallel_calibrated
        )
        /
        abs(
            anchors.p_parallel_calibrated
        )
    )

    print(
        "ONE_COPY_P_PARALLEL_FROM_STRESS="
        f"{anchors.p_parallel_stress:.15e}"
    )

    print(
        "ONE_COPY_P_PARALLEL_FROM_PROMOTED_PAIR_LOAD="
        f"{anchors.p_parallel_calibrated:.15e}"
    )

    print(
        "ONE_COPY_P_PARALLEL_RECONSTRUCTION_RELERR="
        f"{pressure_relerr:.15e}"
    )

    print(
        "ONE_COPY_BASE_ENERGY_LINE="
        f"{anchors.base_energy_one:.15e}"
    )

    print(
        "ONE_COPY_BASE_ACTIVE_LINE="
        f"{anchors.base_active_one:.15e}"
    )

    print(
        "ONE_COPY_JUNCTION_REDUCED_ENERGY="
        f"{anchors.mu_j:+.15e}"
    )

    print(
        "ONE_COPY_JUNCTION_PHYSICAL_ENERGY="
        f"{anchors.junction_energy_one:+.15e}"
    )

    print(
        "ONE_COPY_JUNCTION_ACTIVE="
        f"{anchors.endpoint_active:+.15e}"
    )

    print(
        "WALL_TENSION_CALIBRATION_RATIO="
        f"{anchors.tension_calibration:.15e}"
    )

    pressure_pass = (
        pressure_relerr
        <
        5.0e-5
    )

    print(
        "ONE_COPY_RADIAL_SUPPORT_RECONSTRUCTION="
        f"{'PASS' if pressure_pass else 'FAIL'}"
    )

    # ========================================================================
    # Reconstruct current pair control.
    # ========================================================================

    print(
        "\n=== CURRENT TWO-COPY 018A-8 CONTROL ==="
    )

    current = evaluate_case(
        anchors,
        anchors.f0,
        2,
        float(
            g8.X_TARGET
        ),
        high_precision=True,
    )

    print_candidate(
        "CURRENT_PAIR",
        current,
    )

    current_hp_wall = (
        g8.wall_gravity_factors(
            float(
                current[
                    "sigma_wall"
                ]
            ),
            float(
                current[
                    "k_wall"
                ]
            ),
            float(
                current[
                    "radius"
                ]
            ),
            float(
                g8.X_TARGET
            )
            *
            float(
                current[
                    "radius"
                ]
            ),
            PAYLOAD_RADIUS_OVER_H
            *
            float(
                g8.X_TARGET
            )
            *
            float(
                current[
                    "radius"
                ]
            ),
        )
    )

    pair_active_line = (
        2.0
        *
        (
            anchors.base_active_one
            +
            anchors.endpoint_active
        )
    )

    _, current_rim_worst = (
        g8.rim_envelope(
            pair_active_line,
            float(
                current[
                    "radius"
                ]
            ),
            float(
                g8.X_TARGET
            )
            *
            float(
                current[
                    "radius"
                ]
            ),
            PAYLOAD_RADIUS_OVER_H
            *
            float(
                g8.X_TARGET
            )
            *
            float(
                current[
                    "radius"
                ]
            ),
            anchors.rim_core_width,
            high_precision=True,
        )
    )

    current_payload_hp = (
        float(
            current_hp_wall[
                "payload"
            ]
        )
        -
        current_rim_worst
    )

    current_c_hp = (
        float(
            current[
                "energy_per_r"
            ]
        )
        /
        (
            current_payload_hp
            *
            float(
                g8.X_TARGET
            ) ** 2
        )
    )

    current_c_relerr = (
        abs(
            current_c_hp
            -
            CURRENT_EXPECTED_C
        )
        /
        CURRENT_EXPECTED_C
    )

    print(
        "CURRENT_PAIR_HIGH_PRECISION_C="
        f"{current_c_hp:.15e}"
    )

    print(
        "CURRENT_PAIR_C_VS_018A8_RELERR="
        f"{current_c_relerr:.15e}"
    )

    current_control_pass = (
        current[
            "pass"
        ]

        and
        current_c_relerr
        <
        5.0e-6
    )

    print(
        "CURRENT_018A8_RECONSTRUCTION="
        f"{'PASS' if current_control_pass else 'FAIL'}"
    )

    # ========================================================================
    # Thin-wall theoretical floor.
    # ========================================================================

    print(
        "\n=== SINGLE-VORTON THIN-WALL EFFICIENCY FLOOR ==="
    )

    thin = (
        optimize_thin_limit(
            anchors
        )
    )

    print(
        "SINGLE_VORTON_THIN_OPT_X="
        f"{thin['x']:.15e}"
    )

    print(
        "SINGLE_VORTON_THIN_OUTWARD="
        f"{thin['net']:+.15e}"
    )

    print(
        "SINGLE_VORTON_THIN_C_FLOOR="
        f"{thin['c_eff']:.15e}"
    )

    # ========================================================================
    # Full architecture scan.
    # ========================================================================

    print(
        "\n=== MULTIPLICITY x F x HEIGHT ARCHITECTURE SCAN ==="
    )

    scan_by_copy = {}

    for copies in COPY_COUNTS:

        records = []

        for f_value in F_GRID:

            result = optimize_x(
                anchors,
                float(
                    f_value
                ),
                copies,
            )

            if result is not None:
                records.append(
                    result
                )

        scan_by_copy[
            copies
        ] = records

        print(
            "ARCHITECTURE_SCAN "
            f"COPIES={copies} "
            f"TOTAL_F={len(F_GRID)} "
            f"PASSING_F={len(records)}"
        )

        if records:

            best = min(
                records,
                key=lambda result:
                    float(
                        result[
                            "c_eff"
                        ]
                    ),
            )

            max_f = max(
                records,
                key=lambda result:
                    float(
                        result[
                            "f"
                        ]
                    ),
            )

            print_candidate(
                f"COPIES_{copies}_LOWEST_C",
                best,
            )

            print_candidate(
                f"COPIES_{copies}_MAX_F_PASS",
                max_f,
            )

    single_records = (
        scan_by_copy[
            1
        ]
    )

    if not single_records:

        print(
            "SINGLE_VORTON_FEASIBLE_REGION=NO"
        )

        print(
            "018B0_ARCHITECTURE_DECISION="
            "RETAIN_PAIR_PENDING_MICROSCOPIC_PAIR_DEFINITION"
        )

        print(
            "CURRENT_HEURISTIC="
            "APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY"
        )

        print(
            "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
        )

        return

    print(
        "SINGLE_VORTON_FEASIBLE_REGION=YES"
    )

    # ========================================================================
    # Pareto knees.
    # ========================================================================

    print(
        "\n=== SINGLE-VORTON PARETO KNEES ==="
    )

    pareto_candidates = []

    seen_f = set()

    for threshold in PARETO_THRESHOLDS:

        eligible = [
            result
            for result
            in single_records
            if float(
                result[
                    "c_eff"
                ]
            )
            <=
            threshold
            *
            thin[
                "c_eff"
            ]
        ]

        if not eligible:

            print(
                "PARETO_KNEE "
                f"C_OVER_THIN_MAX={threshold:.3f} "
                "FOUND=NO"
            )

            continue

        knee = max(
            eligible,
            key=lambda result:
                float(
                    result[
                        "f"
                    ]
                ),
        )

        print(
            "PARETO_KNEE "
            f"C_OVER_THIN_MAX={threshold:.3f} "
            f"FOUND=YES"
        )

        print_candidate(
            f"PARETO_{threshold:.3f}",
            knee,
        )

        key = round(
            float(
                knee[
                    "f"
                ]
            ),
            8,
        )

        if key not in seen_f:

            pareto_candidates.append(
                (
                    threshold,
                    knee,
                )
            )

            seen_f.add(
                key
            )

    lowest_c_single = min(
        single_records,
        key=lambda result:
            float(
                result[
                    "c_eff"
                ]
            ),
    )

    key = round(
        float(
            lowest_c_single[
                "f"
            ]
        ),
        8,
    )

    if key not in seen_f:

        pareto_candidates.append(
            (
                1.0,
                lowest_c_single,
            )
        )

    # ========================================================================
    # Exhaustive deterministic stress.
    # ========================================================================

    print(
        "\n=== DETERMINISTIC 3^8 STRESS OF SINGLE-VORTON FINALISTS ==="
    )

    stress_records = []

    for (
        threshold,
        candidate,
    ) in pareto_candidates:

        stress = deterministic_stress(
            anchors,
            candidate,
        )

        stress_records.append(
            (
                threshold,
                candidate,
                stress,
            )
        )

        print(
            "FINALIST_STRESS "
            f"F={float(candidate['f']):.9f} "
            f"NOMINAL_C={float(candidate['c_eff']):.15e} "
            f"TOTAL={int(stress['total'])} "
            f"PASSING={int(stress['passed'])} "
            f"ALL_PASS={'YES' if stress['all_pass'] else 'NO'} "
            f"DEEP_PASS={'YES' if stress['deep_pass'] else 'NO'} "
            f"MIN_PAYLOAD={float(stress['min_payload']):+.15e} "
            f"MIN_POINT={float(stress['min_point']):+.15e} "
            f"MIN_ACTIVE={float(stress['min_active']):+.15e} "
            f"MIN_LEVERAGE={float(stress['min_leverage']):.15e} "
            f"MIN_SCALE={float(stress['min_scale']):.15e} "
            f"MAX_INTEGER_MISMATCH={float(stress['max_integer_mismatch']):.15e} "
            f"CONSERVATIVE_MAX_C={float(stress['max_c']):.15e}"
        )

        print(
            "FINALIST_WORST_PAYLOAD_CASE="
            f"{stress['worst_payload_case']}"
        )

    # Robustness first:
    # choose the largest F among deep-robust candidates whose nominal C lies
    # within 10 percent of the thin asymptotic floor.
    deep = [
        (
            threshold,
            candidate,
            stress,
        )
        for (
            threshold,
            candidate,
            stress,
        )
        in stress_records
        if stress[
            "deep_pass"
        ]
        and
        float(
            candidate[
                "c_eff"
            ]
        )
        <=
        1.10
        *
        thin[
            "c_eff"
        ]
    ]

    if deep:

        selected_threshold, selected, selected_stress = max(
            deep,
            key=lambda item:
                float(
                    item[
                        1
                    ][
                        "f"
                    ]
                ),
        )

        selection_class = (
            "DEEP_ROBUST_SINGLE_VORTON_PARETO"
        )

    else:

        all_pass = [
            (
                threshold,
                candidate,
                stress,
            )
            for (
                threshold,
                candidate,
                stress,
            )
            in stress_records
            if stress[
                "all_pass"
            ]
        ]

        if all_pass:

            selected_threshold, selected, selected_stress = max(
                all_pass,
                key=lambda item:
                    float(
                        item[
                            1
                        ][
                            "f"
                        ]
                    ),
            )

            selection_class = (
                "SIGN_ROBUST_SINGLE_VORTON_PARETO_NOT_DEEP"
            )

        else:

            selected_threshold = math.nan
            selected = None
            selected_stress = None

            selection_class = (
                "NO_ROBUST_SINGLE_VORTON_FINALIST"
            )

    print(
        "\n=== SINGLE-VORTON SELECTION ==="
    )

    print(
        "SELECTION_CLASS="
        f"{selection_class}"
    )

    if selected is None:

        print(
            "ROBUST_SINGLE_VORTON_SELECTED=NO"
        )

        print(
            "018B_TARGET_ARCHITECTURE="
            "CURRENT_COUNTERROTATING_PAIR_PENDING_MICROSCOPIC_PAIR_DEFINITION"
        )

        print(
            "NEXT="
            "DEFINE_AND_SOLVE_MICROSCOPIC_TWO_VORTON_BINDING_BEFORE_GLOBAL_018B"
        )

        print(
            "CURRENT_HEURISTIC="
            "APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY"
        )

        print(
            "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
        )

        return

    print(
        "ROBUST_SINGLE_VORTON_SELECTED=YES"
    )

    print(
        "SELECTED_PARETO_THRESHOLD="
        f"{selected_threshold:.6f}"
    )

    print_candidate(
        "SELECTED_SINGLE_VORTON",
        selected,
    )

    # ========================================================================
    # 20,000 continuous random stresses.
    # ========================================================================

    print(
        "\n=== 20,000-CASE RANDOM CONTINUOUS STRESS ==="
    )

    random_result = randomized_stress(
        anchors,
        selected,
    )

    print(
        "RANDOM_STRESS_TOTAL="
        f"{int(random_result['total'])}"
    )

    print(
        "RANDOM_STRESS_PASSING="
        f"{int(random_result['passed'])}"
    )

    print(
        "RANDOM_STRESS_PASS_FRACTION="
        f"{float(random_result['passed']) / float(random_result['total']):.15f}"
    )

    print(
        "RANDOM_STRESS_MIN_PAYLOAD="
        f"{float(random_result['min_payload']):+.15e}"
    )

    print(
        "RANDOM_STRESS_MIN_LEVERAGE="
        f"{float(random_result['min_leverage']):.15e}"
    )

    print(
        "RANDOM_STRESS_MIN_SCALE="
        f"{float(random_result['min_scale']):.15e}"
    )

    print(
        "RANDOM_STRESS_MAX_INTEGER_MISMATCH="
        f"{float(random_result['max_integer_mismatch']):.15e}"
    )

    print(
        "RANDOM_STRESS="
        f"{'PASS' if random_result['all_pass'] else 'FAIL'}"
    )

    # ========================================================================
    # Independent high precision reconstruction.
    # ========================================================================

    print(
        "\n=== HIGH-PRECISION INDEPENDENT RECONSTRUCTION ==="
    )

    high = high_precision_selected(
        anchors,
        selected,
    )

    print(
        "HIGH_PRECISION_POINT_OUTWARD="
        f"{float(high['point']):+.15e}"
    )

    print(
        "HIGH_PRECISION_PAYLOAD_OUTWARD="
        f"{float(high['payload']):+.15e}"
    )

    print(
        "SCOUT_VS_ADAPTIVE_WALL_POINT_RELERR="
        f"{float(high['wall_point_relerr']):.15e}"
    )

    print(
        "SCOUT_VS_ADAPTIVE_WALL_PAYLOAD_RELERR="
        f"{float(high['wall_payload_relerr']):.15e}"
    )

    for (
        width,
        value,
    ) in high[
        "rim_values"
    ]:

        print(
            "SELECTED_RIM_CORE "
            f"WIDTH={float(width):.15e} "
            f"INWARD_FACTOR={float(value):.15e}"
        )

    print(
        "HIGH_PRECISION_FINITE_CORE_WORST_RIM="
        f"{float(high['rim_worst']):.15e}"
    )

    print(
        "HIGH_PRECISION_C="
        f"{float(high['c_eff']):.15e}"
    )

    print(
        "HIGH_PRECISION_RECONSTRUCTION="
        f"{'PASS' if high['pass'] else 'FAIL'}"
    )

    # ========================================================================
    # Topology and stationary-vorton implications.
    # ========================================================================

    print(
        "\n=== SELECTED MICROSCOPIC / STATIONARY INTERPRETATION ==="
    )

    selected_topology = topology_metrics(
        anchors,
        float(
            selected[
                "f"
            ]
        ),
    )

    print(
        "SELECTED_MIN_VACUUM_HESSIAN_EIGENVALUE="
        f"{float(selected_topology['min_hessian_eigenvalue']):.15e}"
    )

    print(
        "SELECTED_TRANSVERSE_WALL_EIGENVALUE="
        f"{float(selected_topology['transverse_eigenvalue']):.15e}"
    )

    print(
        "SELECTED_GAUGE_MASS_SHIFT_FRACTION="
        f"{float(selected_topology['gauge_mass_shift_fraction']):.15e}"
    )

    print(
        "SELECTED_TOPOLOGY_PREFLIGHT="
        f"{'PASS' if selected_topology['pass'] else 'FAIL'}"
    )

    selected_q = float(
        selected[
            "q_required"
        ]
    )

    selected_n = float(
        selected[
            "n_required"
        ]
    )

    angular_momentum_estimate = (
        selected_q
        *
        selected_n
    )

    print(
        "SINGLE_VORTON_NET_ANGULAR_MOMENTUM="
        "NONZERO"
    )

    print(
        "SINGLE_VORTON_J_EQUALS_NQ_ESTIMATE="
        f"{angular_momentum_estimate:.15e}"
    )

    print(
        "STATIC_CLASSIFICATION="
        "NO"
    )

    print(
        "STATIONARY_AXISYMMETRIC_CLASSIFICATION="
        "YES"
    )

    print(
        "018D_FRAME_DRAGGING_GATE_REQUIRED="
        "YES"
    )

    print(
        "COUNTERROTATING_PAIR_REQUIRED_FOR_FIELD_EXISTENCE="
        "NO"
    )

    print(
        "COUNTERROTATING_PAIR_WAS_USED_TO_CANCEL_EFFECTIVE_T_TPHI="
        "YES"
    )

    print(
        "FULL_MICROSCOPIC_COUNTERROTATING_PAIR_BINDING="
        "NOT_ESTABLISHED_BY_THIS_CAMPAIGN"
    )

    # ========================================================================
    # Energy closeout.
    # ========================================================================

    print(
        "\n=== 1g / 1m ENERGY REQUIREMENT ==="
    )

    selected_c = float(
        high[
            "c_eff"
        ]
    )

    (
        selected_mass,
        selected_energy,
    ) = energy_scaling(
        selected_c
    )

    (
        current_mass,
        current_energy,
    ) = energy_scaling(
        current_c_hp
    )

    print(
        "CURRENT_018A8_C="
        f"{current_c_hp:.15e}"
    )

    print(
        "CURRENT_018A8_ONE_G_ONE_M_MASS_KG="
        f"{current_mass:.15e}"
    )

    print(
        "CURRENT_018A8_ONE_G_ONE_M_ENERGY_J="
        f"{current_energy:.15e}"
    )

    print(
        "SELECTED_PROJECTED_C="
        f"{selected_c:.15e}"
    )

    print(
        "SELECTED_PROJECTED_ONE_G_ONE_M_MASS_KG="
        f"{selected_mass:.15e}"
    )

    print(
        "SELECTED_PROJECTED_ONE_G_ONE_M_ENERGY_J="
        f"{selected_energy:.15e}"
    )

    improvement = (
        current_energy
        /
        selected_energy
    )

    energy_fraction = (
        selected_energy
        /
        current_energy
    )

    print(
        "PROJECTED_ENERGY_IMPROVEMENT_FACTOR="
        f"{improvement:.15e}"
    )

    print(
        "PROJECTED_ENERGY_FRACTION_OF_CURRENT="
        f"{energy_fraction:.15e}"
    )

    print(
        "ENERGY_MODEL_STATUS="
        "SOURCE_LEVEL_REPARAMETERIZATION_ONLY_NOT_YET_MICROSCOPICALLY_REVALIDATED"
    )

    print(
        "PRACTICAL_ENERGY_SCALING="
        "STILL_CATASTROPHIC"
    )

    # ========================================================================
    # Final decision.
    # ========================================================================

    final_preflight = (
        pressure_pass
        and
        current_control_pass
        and
        bool(
            selected_topology[
                "pass"
            ]
        )
        and
        bool(
            selected[
                "pass"
            ]
        )
        and
        bool(
            selected_stress[
                "all_pass"
            ]
        )
        and
        bool(
            random_result[
                "all_pass"
            ]
        )
        and
        bool(
            high[
                "pass"
            ]
        )
    )

    print(
        "\n=== 018B-0 DECISION ==="
    )

    print(
        "FULL_018A_GATE=GREEN_INHERITED"
    )

    print(
        "018B_AUTHORIZED=YES_INHERITED"
    )

    print(
        "SINGLE_STATIONARY_VORTON_SOURCE_LEVEL_REGION="
        f"{'SUPPORTED' if final_preflight else 'NOT_ESTABLISHED'}"
    )

    print(
        "018B0_ARCHITECTURE_PARETO_CAMPAIGN="
        f"{'GREEN' if final_preflight else 'RED'}"
    )

    if final_preflight:

        print(
            "018B_TARGET_ARCHITECTURE="
            "SINGLE_STATIONARY_GAUGED_VORTON_PLUS_ONE_KLS_WALL"
        )

        print(
            "SECOND_COMPLETE_VORTON_COPY="
            "NOT_REQUIRED_BY_SELECTED_SOURCE_LEVEL_ARCHITECTURE"
        )

        print(
            "MICROSCOPIC_REPARAMETERIZATION_REQUIRED="
            "YES"
        )

        print(
            "NEXT="
            "018B0B_RERUN_PLANAR_WALL_AND_FULLY_COUPLED_LOCAL_JUNCTION_AT_SELECTED_F_THEN_LAUNCH_GLOBAL_018B"
        )

    else:

        print(
            "018B_TARGET_ARCHITECTURE="
            "CURRENT_PAIR_UNTIL_FAILURE_CHANNEL_IS_RESOLVED"
        )

        print(
            "NEXT="
            "IDENTIFY_FAILED_SINGLE_VORTON_ARCHITECTURE_CHANNEL"
        )

    print(
        "TRUE_018B_GLOBAL_TOROIDAL_FIELD_SOLUTION="
        "NOT_YET_RUN"
    )

    print(
        "018C_FULL_COMPOSITE_STABILITY="
        "NOT_YET_RUN"
    )

    print(
        "018D_STATIONARY_GR_FRAME_DRAGGING="
        "NOT_YET_RUN"
    )

    print(
        "018E_NONLINEAR_EINSTEIN_MATTER="
        "NOT_YET_RUN"
    )

    print(
        "CURRENT_HEURISTIC="
        "APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY"
    )

    print(
        "HEURISTIC_INCREASE_FROM_THIS_SCAN="
        "NO_PARAMETER_SCAN_ALONE_DOES_NOT_EARN_PROMOTION"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018B0_ARCHITECTURE_PARETO_SCOUT"
    )


if __name__ == "__main__":
    main()
