#!/usr/bin/env python3
"""025B0 — Hyperelastic compatibility + full acoustic-cone falsification.

PURPOSE
-------
Attempt to falsify the 025A Saturating Relativistic Hencky Solid before
authorizing an expensive finite-thickness nonlinear material BVP.

025A established a strong LOCAL constitutive preflight:

    positive energy;
    finite-strain DEC/NEC;
    exact local principal stress-state realization;
    principal longitudinal characteristic speeds in [0,1];
    reference transverse speed below light;
    outward finite-payload weak-field response.

It did NOT establish:

    one globally compatible deformation field;
    one Euler-Lagrange material solution;
    a finite-thickness collar;
    the complete finite-strain acoustic characteristic cone;
    dynamic stability.

025B0 attacks the two cheapest dangerous gaps:

    1. compatibility of the material-coordinate deformation;
    2. arbitrary-direction acoustic characteristics.

This is intended as a falsification gate.

SCIENTIFIC QUESTION
-------------------
Can the 025A hyperelastic constitutive law be embedded into one continuous,
orientation-preserving axisymmetric material deformation while retaining
useful outward gravitational response, and does its full local relativistic
acoustic cone remain real, positive and subluminal at the extreme stress
states selected by 025A?

PART I — EXACT RADIAL COMPATIBILITY
-----------------------------------
For an ordinary Euclidean-reference axisymmetric radial material map

    X = X(r)

define the material linear particle densities

    n_r   = dX/dr

    n_phi = X/r

with unstrained reference values normalized to one.

Therefore

    y_r
      =
    ln(dX/dr)

and

    y_phi
      =
    ln(X/r).

Define

    g(r)
      =
    ln(X/r).

Then

    X
      =
    r exp(g)

and therefore

    dX/dr
      =
    exp(g) [1 + r g'(r)].

Hence the exact compatibility identity is

    y_phi
      =
    g

    y_r
      =
    g + ln[1+r g'].

Orientation preservation requires

    1+r g' > 0.

The 025A idealized source asks locally for:

Core:

    y_r   = -Y_core
    y_phi = -Y_core.

Transfer annulus:

    y_r   = -Y_ann
    y_phi = +Y_ann.

The selected 025A solution has both magnitudes approximately four.

A sharp interface would require

    X/r = exp(-Y_core)

on one side and

    X/r = exp(+Y_ann)

on the other side.

Since X/r must be continuous for a continuous deformation at r>0, the
piecewise target is incompatible with an ordinary Euclidean-reference
radial map.

SMOOTHING THE INTERFACE
-----------------------
Suppose g crosses continuously from negative to positive.

At an upward zero crossing:

    g = 0

and generically:

    g' > 0.

Then:

    y_r
      =
    ln(1+r g')
      >
    0.

Thus the transition necessarily develops radial compression even though the
006B/025A transfer architecture wants radial tension.

This does not prove that every possible 2-D elastic configuration fails.

It proves that the direct diagonal plane-strain radial realization of the
piecewise 025A target is impossible without transition states that depart
from that target.

PART II — COMPATIBLE RADIAL-MAP SCOUT
-------------------------------------
Do not stop at the theorem.

Search for the best gravitational source that the SAME constitutive law can
produce when compatibility is imposed from the beginning.

Parameterize:

    g(x)
      =
    g0
    + c2 x^2
    + c4 x^4
    + c6 x^6
    + c8 x^8,

where:

    x = r/R in [0,1].

Then:

    y_phi = g

and:

    y_r
      =
    g + ln[1+x dg/dx].

This family is regular at the center because:

    y_r(0)=y_phi(0)=g0.

PRIMARY COMPATIBLE SUBCLASS
---------------------------
The primary scout requires radial tension everywhere:

    p_r < 0.

This avoids a singular inversion of the static equilibrium equation at
p_r=0 and directly tests the simplest globally compatible continuation of
the repulsive core.

This is a declared subclass.

Failure of this subclass is NOT a universal theorem against arbitrary
two-dimensional deformations, shear, non-Euclidean reference metrics, or
prestressed media.

EXACT STATIC CONSERVATION
-------------------------
For a thin axisymmetric membrane:

    dp_r/dr
    +
    (p_r-p_phi)/r
      =
    0.

Let:

    w_r
      =
    p_r/rho
      =
    tanh(k y_r),

    w_phi
      =
    p_phi/rho
      =
    tanh(k y_phi).

For sign-definite p_r, write:

    p_r = -P

with P>0.

Then:

    d ln P / d ln r
      =
    -1 + w_phi/w_r.

Therefore the compatible stress profile is NOT independently assigned.

For every deformation profile g(r), the radial stress and energy-density
profile are reconstructed by integrating this exact equilibrium identity.

Then:

    rho = p_r/w_r > 0

and:

    p_phi = w_phi rho.

The required material grading is reconstructed from the 025A constitutive
energy:

    rho
      =
    rho_star
    exp[
        y_r+y_phi+y_z
        +
        (1/k)
        sum_i ln cosh(k y_i)
    ],

with:

    y_z=0.

Thus:

    rho_star(r)

is an OUTPUT.

No density profile is inserted by hand.

OUTER SUPPORT
-------------
If p_r(R)<0, terminate the radial tension with a thin outer support ring.

Let:

    s
      =
    p_support/rho_support
      =
    tanh(k y_support)
      >
    0.

The minimum line energy required by radial force balance is:

    lambda
      =
    -R p_r(R)/s.

Its active line source is:

    lambda + p_phi,line
      =
    (1+s) lambda.

This is the same support bookkeeping principle used by the established
006B/006D architecture.

GRAVITATIONAL OBSERVABLE
------------------------
For h=1, define the thin surface active source:

    S(r)
      =
    rho+p_r+p_phi.

The outward on-axis field factor is:

    F_surface
      =
    - integral_0^R
        r S(r)
        /
        (1+r^2)^(3/2)
        dr.

The support contribution is:

    F_line
      =
    - R (1+s) lambda
      /
      (1+R^2)^(3/2).

Then:

    F = F_surface + F_line.

The dimensionless total energy is:

    m
      =
    2 integral_0^R r rho(r) dr
    +
    2 R lambda.

For F>0:

    C = m/(2F).

Compare with:

    C_006D = 23.591586299249

    C_006B = 23.426710175391

    C_005B = 79.753148116012.

FINITE-PAYLOAD RESPONSE
-----------------------
The best compatible strain-cap-four candidate receives an independent
finite spherical-payload integration.

Payload radius:

    R_P/h
      =
    0.043298860805059215.

Promotion requires every sampled payload point to remain outward.

PART III — FULL RELATIVISTIC ACOUSTIC CONE
------------------------------------------
Use the standard relativistic Hadamard characteristic equation:

    [v^2 (rho h^{ac}+p^{ac}) - Q^{ac}] iota_c = 0

with:

    Q^{ac}
      =
    A^{abcd} nu_b nu_d

and:

    A^{abcd}
      =
    E^{abcd}
    -
    h^{ac} p^{bd},

    E^{abcd}
      =
    -2 partial p^{ab}/partial g_cd
    -
    p^{ab} h^{cd}.

The 025A spectral energy is extended off the principal axes as an isotropic
spectral function.

Let:

    B
      =
    F_material h^{-1} F_material^T.

Its eigenvalues are:

    n_i^2.

Then:

    y_i
      =
    1/2 ln eigenvalue_i(B).

The stored energy is:

    rho
      =
    exp[
        sum_i y_i
        +
        (1/k) sum_i ln cosh(k y_i)
    ]

with an irrelevant positive rho_star factor set to one for local wave-speed
calculations.

The spatial pressure tensor is reconstructed from metric variation:

    p^{ab}
      =
    -rho h^{ab}
    -
    2 partial rho/partial h_ab.

The elasticity and Hadamard tensors are then obtained independently by
finite metric differentiation.

VALIDATION OF THE ACOUSTIC IMPLEMENTATION
-----------------------------------------
At zero strain the numerical characteristic cone must reproduce:

    c_L^2 = k

    c_T^2 = k/2

for all principal axes.

At each selected 025A principal state, the numerically reconstructed
longitudinal principal characteristic must reproduce the analytic identity:

    c_L,i^2
      =
    k
    +
    (1-k) p_i/rho.

Only after these checks pass is the arbitrary-direction cone trusted.

025A LOCAL STATES TESTED
------------------------
Selected 025A parameters are loaded directly from its summary JSON.

Core:

    (-Y_core, -Y_core, 0)

Annulus:

    (-Y_ann, +Y_ann, 0)

Support:

    (0, +Y_support, 0).

For each state scan a deterministic approximately uniform sphere of
propagation directions.

For every direction calculate all three generalized characteristic
eigenvalues v^2.

Primary full-cone criteria:

    minimum v^2 >= -1e-3

    maximum v^2 <= 1.001

with independent finite-difference step comparison.

A numerical result near a boundary is not promoted without step convergence.

COMPATIBLE SEARCH
-----------------
For each maximum logarithmic strain:

    2
    3
    4
    5
    6

perform several independent differential-evolution searches.

Search variables:

    k
    R/h
    g0
    c2
    c4
    c6
    c8
    y_support.

The polynomial family is deliberately small.

This is an information-gain gate, not a claim of global optimization over
all elastic deformations.

BLIND WILDCARDS
---------------
Report compatible strain-cap diagnostics for:

    0.625
    1.6
    1.875
    3.125
    5

only as:

    BLIND_WILDCARD_NOT_PHYSICS_PRIOR.

They do not select the model.

PROMOTION
---------
A strong minimal-compatibility promotion requires:

    acoustic implementation validation PASS;

    full selected-state acoustic cone PASS;

    compatible orientation-preserving radial deformation;

    exact reconstructed static radial conservation;

    positive rho;

    finite material grading;

    finite-payload all outward;

    C < 30 at max |y| <= 4.

A stronger result would retain:

    C < C_006D.

FALSIFIERS
----------
If the full acoustic cone contains a robust:

    v^2 < 0

or:

    v^2 > 1,

demote the 025A constitutive law before any BVP.

If the local cone is healthy but the exact piecewise architecture is
incompatible and the best compatible radial deformation regresses toward
the old supported-tension-disk scale C~80, then:

    the local 025A matter law survives;

    the direct 006B/006D material-realization interpretation is demoted;

    spatial compatibility is identified as the dominant obstruction.

STOP RULE
---------
Do not launch the expensive finite-thickness axisymmetric hyperelastic BVP
unless this gate establishes enough compatible-source headroom to justify it.

If the simple compatible radial subclass fails badly but the local acoustic
cone survives, the next action must be an analytical decision between:

    a genuinely 2-D axisymmetric material map with shear

and:

    an explicit non-Euclidean/prestrained reference metric.

Do not silently add a reference metric merely to recover the desired stress
tensor.

CLAIM CLASS
-----------
PROJECT_DERIVED_HYPERELASTIC_COMPATIBILITY_AND_FULL_ACOUSTIC_CONE_GATE

DOES NOT ESTABLISH
------------------
- a complete 2-D material solution;
- finite collars;
- full nonlinear Einstein-matter equilibrium;
- microscopic material synthesis;
- laboratory realizability;
- favorable 1/G scaling;
- a practical antigravity device.
"""

from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import differential_evolution
from scipy.stats import qmc


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results/data"

PREV = DATA / "025a_saturating_relativistic_hencky_summary.json"

OUTJ = DATA / "025b0_hyperelastic_compatibility_acoustic_cone_summary.json"
OUTF = DATA / "025b0_compatible_radial_map_frontier.csv"
OUTC = DATA / "025b0_full_acoustic_cone.csv"
OUTN = DATA / "025b0_best_compatible_radial_profile.npz"


C006B = 23.426710175391
C006D = 23.591586299249
C005B = 79.753148116012

PAYLOAD_RADIUS = 0.043298860805059215

SMOKE = (
    os.environ.get(
        "AG_SMOKE",
        "0",
    )
    ==
    "1"
)

PROFILE_N = (
    192
    if SMOKE
    else 768
)

PROFILE_HIGH_N = (
    512
    if SMOKE
    else 4096
)

CONE_DIRECTIONS = (
    128
    if SMOKE
    else 2048
)

PAYLOAD_SAMPLES = (
    16
    if SMOKE
    else 128
)

PAYLOAD_PHI = (
    64
    if SMOKE
    else 160
)

SEARCH_MAXITER = (
    20
    if SMOKE
    else 110
)

SEARCH_POPSIZE = (
    6
    if SMOKE
    else 12
)

SEARCH_SEEDS = (
    1
    if SMOKE
    else 3
)

PRIMARY_CAPS = (
    2.0,
    3.0,
    4.0,
    5.0,
    6.0,
)

WILDCARD_CAPS = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)

METRIC_STEPS = (
    2.0e-4,
    1.0e-4,
)


def logcosh(
    x: np.ndarray,
) -> np.ndarray:
    """Return log(cosh(x)) without large-exponential overflow."""

    return (
        np.logaddexp(
            x,
            -x,
        )
        -
        math.log(2.0)
    )


def fibonacci_sphere(
    n: int,
) -> np.ndarray:
    """Return deterministic approximately uniform unit directions."""

    i = np.arange(
        n,
        dtype=float,
    )

    z = (
        1.0
        -
        2.0
        * (
            i
            +
            0.5
        )
        /
        n
    )

    golden = (
        math.pi
        * (
            3.0
            -
            math.sqrt(5.0)
        )
    )

    phi = (
        golden
        * i
    )

    r = np.sqrt(
        np.maximum(
            0.0,
            1.0
            -
            z * z,
        )
    )

    return np.column_stack(
        (
            r
            * np.cos(phi),

            r
            * np.sin(phi),

            z,
        )
    )


# ----------------------------------------------------------------------
# Relativistic acoustic tensor.
# ----------------------------------------------------------------------

_METRIC_PAIRS = (
    (0, 0),
    (1, 1),
    (2, 2),
    (0, 1),
    (0, 2),
    (1, 2),
)


def perturb_metric(
    h: np.ndarray,
    i: int,
    j: int,
    delta: float,
) -> np.ndarray:
    """Return symmetric metric perturbation."""

    out = np.array(
        h,
        dtype=float,
        copy=True,
    )

    out[
        i,
        j
    ] += delta

    if i != j:

        out[
            j,
            i
        ] += delta

    return out


def rho_from_metric(
    h_cov: np.ndarray,
    material_gradient: np.ndarray,
    k: float,
) -> float:
    """Return local rest energy at fixed material-coordinate gradient.

    Parameters
    ----------
    h_cov:
        Positive-definite spatial covariant metric.

    material_gradient:
        Matrix whose singular/eigenvalue content defines the material
        linear particle densities in the local rest frame.

    k:
        Saturation/stiffness parameter of the 025A constitutive law.

    Returns
    -------
    float
        Positive energy density with rho_star normalized to one.

    Notes
    -----
    The material metric pullback is

        B = F h^{-1} F^T.

    Its eigenvalues are n_i^2.

    No gravity is included in this local characteristic calculation.
    """

    h_inv = np.linalg.inv(
        h_cov
    )

    B = (
        material_gradient
        @ h_inv
        @ material_gradient.T
    )

    eig = np.linalg.eigvalsh(
        B
    )

    if np.min(
        eig
    ) <= 0.0:

        raise ValueError(
            "Non-positive material metric eigenvalue"
        )

    y = (
        0.5
        * np.log(
            eig
        )
    )

    log_rho = (
        np.sum(y)
        +
        np.sum(
            logcosh(
                k
                * y
            )
        )
        /
        k
    )

    return float(
        np.exp(
            log_rho
        )
    )


def pressure_from_metric(
    h_cov: np.ndarray,
    material_gradient: np.ndarray,
    k: float,
    gradient_step: float,
) -> tuple[float, np.ndarray]:
    """Reconstruct p^{ab} by independent metric differentiation.

    Uses:

        p^{ab}
          =
        -rho h^{ab}
        -
        2 partial rho / partial h_ab.

    Off-diagonal symmetric coordinate perturbations change h_ij and h_ji
    together and are therefore divided by two when converting the scalar
    parameter derivative to a tensor-component derivative.
    """

    rho = rho_from_metric(
        h_cov,
        material_gradient,
        k,
    )

    h_inv = np.linalg.inv(
        h_cov
    )

    p = (
        -rho
        * h_inv
    )

    p = np.array(
        p,
        dtype=float,
        copy=True,
    )

    for i, j in _METRIC_PAIRS:

        rp = rho_from_metric(
            perturb_metric(
                h_cov,
                i,
                j,
                +gradient_step,
            ),
            material_gradient,
            k,
        )

        rm = rho_from_metric(
            perturb_metric(
                h_cov,
                i,
                j,
                -gradient_step,
            ),
            material_gradient,
            k,
        )

        parameter_derivative = (
            rp
            -
            rm
        ) / (
            2.0
            * gradient_step
        )

        if i == j:

            tensor_derivative = (
                parameter_derivative
            )

        else:

            tensor_derivative = (
                0.5
                * parameter_derivative
            )

        value = (
            -rho
            * h_inv[
                i,
                j
            ]
            -
            2.0
            * tensor_derivative
        )

        p[
            i,
            j
        ] = value

        p[
            j,
            i
        ] = value

    return (
        rho,
        p,
    )


def hadamard_tensor(
    y: np.ndarray,
    k: float,
    metric_step: float,
) -> tuple[
    float,
    np.ndarray,
    np.ndarray,
]:
    """Return rho, pressure and relativistic Hadamard elasticity tensor."""

    h = np.eye(
        3,
        dtype=float,
    )

    material_gradient = np.diag(
        np.exp(
            np.asarray(
                y,
                dtype=float,
            )
        )
    )

    pressure_step = (
        metric_step
        /
        10.0
    )

    rho, p0 = pressure_from_metric(
        h,
        material_gradient,
        k,
        pressure_step,
    )

    h_inv = np.eye(
        3,
        dtype=float,
    )

    E = np.zeros(
        (
            3,
            3,
            3,
            3,
        ),
        dtype=float,
    )

    for c, d in _METRIC_PAIRS:

        _, pp = pressure_from_metric(
            perturb_metric(
                h,
                c,
                d,
                +metric_step,
            ),
            material_gradient,
            k,
            pressure_step,
        )

        _, pm = pressure_from_metric(
            perturb_metric(
                h,
                c,
                d,
                -metric_step,
            ),
            material_gradient,
            k,
            pressure_step,
        )

        parameter_derivative = (
            pp
            -
            pm
        ) / (
            2.0
            * metric_step
        )

        if c == d:

            tensor_derivative = (
                parameter_derivative
            )

        else:

            tensor_derivative = (
                0.5
                * parameter_derivative
            )

        value = (
            -2.0
            * tensor_derivative
            -
            p0
            * h_inv[
                c,
                d
            ]
        )

        E[
            :,
            :,
            c,
            d
        ] = value

        E[
            :,
            :,
            d,
            c
        ] = value

    A = np.empty_like(
        E
    )

    for a in range(3):

        for b in range(3):

            for c in range(3):

                for d in range(3):

                    A[
                        a,
                        b,
                        c,
                        d
                    ] = (
                        E[
                            a,
                            b,
                            c,
                            d
                        ]
                        -
                        h_inv[
                            a,
                            c
                        ]
                        * p0[
                            b,
                            d
                        ]
                    )

    return (
        rho,
        p0,
        A,
    )


def wave_speeds(
    rho: float,
    p: np.ndarray,
    A: np.ndarray,
    direction: np.ndarray,
) -> np.ndarray:
    """Return the three generalized relativistic characteristic v^2."""

    n = np.asarray(
        direction,
        dtype=float,
    )

    n = (
        n
        /
        np.linalg.norm(
            n
        )
    )

    Q = np.einsum(
        "abcd,b,d->ac",
        A,
        n,
        n,
    )

    Q = (
        0.5
        * (
            Q
            +
            Q.T
        )
    )

    inertia = (
        rho
        * np.eye(3)
        +
        p
    )

    eval_m, vec_m = np.linalg.eigh(
        0.5
        * (
            inertia
            +
            inertia.T
        )
    )

    if np.min(
        eval_m
    ) <= 0.0:

        return np.asarray(
            [
                -math.inf,
                -math.inf,
                -math.inf,
            ]
        )

    invsqrt = (
        vec_m
        @ np.diag(
            1.0
            /
            np.sqrt(
                eval_m
            )
        )
        @ vec_m.T
    )

    reduced = (
        invsqrt
        @ Q
        @ invsqrt
    )

    reduced = (
        0.5
        * (
            reduced
            +
            reduced.T
        )
    )

    return np.linalg.eigvalsh(
        reduced
    )


def acoustic_validation(
    selected: dict,
) -> dict:
    """Validate and scan the full selected-state acoustic cone."""

    k = float(
        selected[
            "k"
        ]
    )

    t = float(
        selected[
            "t"
        ]
    )

    q = float(
        selected[
            "q"
        ]
    )

    support = float(
        selected[
            "support"
        ]
    )

    yc = (
        math.atanh(t)
        /
        k
    )

    ya = (
        math.atanh(q)
        /
        k
    )

    ys = (
        math.atanh(
            support
        )
        /
        k
    )

    states = {
        "CORE":
            np.asarray(
                [
                    -yc,
                    -yc,
                    0.0,
                ]
            ),

        "ANNULUS":
            np.asarray(
                [
                    -ya,
                    +ya,
                    0.0,
                ]
            ),

        "SUPPORT":
            np.asarray(
                [
                    0.0,
                    +ys,
                    0.0,
                ]
            ),
    }

    # ----------------------------------------------------------
    # Zero-strain benchmark.
    # ----------------------------------------------------------

    zero_rows = []

    zero_max_error = 0.0

    for step in METRIC_STEPS:

        rho0, p0, A0 = hadamard_tensor(
            np.zeros(3),
            k,
            step,
        )

        for axis in range(3):

            n = np.eye(3)[
                axis
            ]

            values = np.sort(
                wave_speeds(
                    rho0,
                    p0,
                    A0,
                    n,
                )
            )

            expected = np.asarray(
                [
                    0.5 * k,
                    0.5 * k,
                    k,
                ]
            )

            error = float(
                np.max(
                    np.abs(
                        values
                        -
                        expected
                    )
                )
            )

            zero_max_error = max(
                zero_max_error,
                error,
            )

            zero_rows.append({
                "step":
                    step,

                "axis":
                    axis,

                "v2_min":
                    float(
                        values[0]
                    ),

                "v2_mid":
                    float(
                        values[1]
                    ),

                "v2_max":
                    float(
                        values[2]
                    ),

                "expected_transverse":
                    0.5 * k,

                "expected_longitudinal":
                    k,

                "max_abs_error":
                    error,
            })

    zero_pass = bool(
        zero_max_error
        <=
        2.0e-3
    )

    # ----------------------------------------------------------
    # Principal longitudinal benchmark.
    # ----------------------------------------------------------

    principal_max_error = 0.0
    principal_rows = []

    for name, y in states.items():

        expected_w = np.tanh(
            k
            * y
        )

        expected_longitudinal = (
            k
            +
            (
                1.0
                -
                k
            )
            * expected_w
        )

        for step in METRIC_STEPS:

            rho, p, A = hadamard_tensor(
                y,
                k,
                step,
            )

            for axis in range(3):

                n = np.eye(3)[
                    axis
                ]

                Q = np.einsum(
                    "abcd,b,d->ac",
                    A,
                    n,
                    n,
                )

                numeric = float(
                    Q[
                        axis,
                        axis
                    ]
                    /
                    (
                        rho
                        +
                        p[
                            axis,
                            axis
                        ]
                    )
                )

                expected = float(
                    expected_longitudinal[
                        axis
                    ]
                )

                error = abs(
                    numeric
                    -
                    expected
                )

                principal_max_error = max(
                    principal_max_error,
                    error,
                )

                principal_rows.append({
                    "state":
                        name,

                    "step":
                        step,

                    "axis":
                        axis,

                    "numeric_longitudinal_v2":
                        numeric,

                    "expected_longitudinal_v2":
                        expected,

                    "absolute_error":
                        error,
                })

    principal_pass = bool(
        principal_max_error
        <=
        3.0e-3
    )

    # ----------------------------------------------------------
    # Full-direction scan.
    # ----------------------------------------------------------

    directions = fibonacci_sphere(
        CONE_DIRECTIONS
    )

    cone_rows = []

    state_summary = {}

    for name, y in states.items():

        by_step = {}

        for step in METRIC_STEPS:

            rho, p, A = hadamard_tensor(
                y,
                k,
                step,
            )

            global_min = math.inf
            global_max = -math.inf

            min_direction = None
            max_direction = None

            negative_count = 0
            superluminal_count = 0

            for direction in directions:

                values = wave_speeds(
                    rho,
                    p,
                    A,
                    direction,
                )

                local_min = float(
                    np.min(
                        values
                    )
                )

                local_max = float(
                    np.max(
                        values
                    )
                )

                if local_min < global_min:

                    global_min = (
                        local_min
                    )

                    min_direction = (
                        direction.copy()
                    )

                if local_max > global_max:

                    global_max = (
                        local_max
                    )

                    max_direction = (
                        direction.copy()
                    )

                if local_min < -1.0e-3:

                    negative_count += 1

                if local_max > 1.001:

                    superluminal_count += 1

            by_step[
                str(step)
            ] = {
                "min_v2":
                    global_min,

                "max_v2":
                    global_max,

                "negative_direction_count":
                    negative_count,

                "superluminal_direction_count":
                    superluminal_count,

                "min_direction":
                    [
                        float(x)
                        for x
                        in min_direction
                    ],

                "max_direction":
                    [
                        float(x)
                        for x
                        in max_direction
                    ],
            }

            cone_rows.append({
                "state":
                    name,

                "metric_step":
                    step,

                "min_v2":
                    global_min,

                "max_v2":
                    global_max,

                "negative_direction_count":
                    negative_count,

                "superluminal_direction_count":
                    superluminal_count,

                "min_nx":
                    float(
                        min_direction[0]
                    ),

                "min_ny":
                    float(
                        min_direction[1]
                    ),

                "min_nz":
                    float(
                        min_direction[2]
                    ),

                "max_nx":
                    float(
                        max_direction[0]
                    ),

                "max_ny":
                    float(
                        max_direction[1]
                    ),

                "max_nz":
                    float(
                        max_direction[2]
                    ),
            })

        first = by_step[
            str(
                METRIC_STEPS[0]
            )
        ]

        second = by_step[
            str(
                METRIC_STEPS[1]
            )
        ]

        min_step_difference = abs(
            first[
                "min_v2"
            ]
            -
            second[
                "min_v2"
            ]
        )

        max_step_difference = abs(
            first[
                "max_v2"
            ]
            -
            second[
                "max_v2"
            ]
        )

        state_pass = bool(
            second[
                "min_v2"
            ]
            >=
            -1.0e-3
            and
            second[
                "max_v2"
            ]
            <=
            1.001
            and
            second[
                "negative_direction_count"
            ]
            ==
            0
            and
            second[
                "superluminal_direction_count"
            ]
            ==
            0
            and
            min_step_difference
            <=
            5.0e-3
            and
            max_step_difference
            <=
            5.0e-3
        )

        state_summary[
            name
        ] = {
            "y":
                [
                    float(v)
                    for v in y
                ],

            "by_step":
                by_step,

            "min_step_difference":
                min_step_difference,

            "max_step_difference":
                max_step_difference,

            "pass":
                state_pass,
        }

    full_cone_pass = bool(
        zero_pass
        and
        principal_pass
        and
        all(
            item[
                "pass"
            ]
            for item in
            state_summary.values()
        )
    )

    return {
        "k":
            k,

        "Y_core":
            yc,

        "Y_annulus":
            ya,

        "Y_support":
            ys,

        "zero_strain_max_error":
            zero_max_error,

        "zero_strain_pass":
            zero_pass,

        "principal_longitudinal_max_error":
            principal_max_error,

        "principal_longitudinal_pass":
            principal_pass,

        "state_summary":
            state_summary,

        "full_cone_pass":
            full_cone_pass,

        "zero_rows":
            zero_rows,

        "principal_rows":
            principal_rows,

        "cone_rows":
            cone_rows,
    }


# ----------------------------------------------------------------------
# Compatible radial material maps.
# ----------------------------------------------------------------------

def profile_metrics(
    vector: np.ndarray,
    strain_cap: float,
    n: int,
    return_profile: bool = False,
) -> dict | None:
    """Evaluate a compatible sign-definite radial-tension material map."""

    (
        k,
        R,
        g0,
        c2,
        c4,
        c6,
        c8,
        y_support,
    ) = [
        float(v)
        for v in vector
    ]

    if not (
        0.5
        <=
        k
        <=
        0.95
    ):

        return None

    if not (
        R
        >
        0.0
    ):

        return None

    if not (
        y_support
        >
        0.0
    ):

        return None

    x = np.linspace(
        0.0,
        1.0,
        n,
    )

    g = (
        g0
        +
        c2
        * x ** 2
        +
        c4
        * x ** 4
        +
        c6
        * x ** 6
        +
        c8
        * x ** 8
    )

    dg = (
        2.0
        * c2
        * x
        +
        4.0
        * c4
        * x ** 3
        +
        6.0
        * c6
        * x ** 5
        +
        8.0
        * c8
        * x ** 7
    )

    jacobian = (
        1.0
        +
        x
        * dg
    )

    if np.min(
        jacobian
    ) <= 0.0:

        return None

    y_phi = g

    y_r = (
        g
        +
        np.log(
            jacobian
        )
    )

    max_strain = float(
        max(
            np.max(
                np.abs(
                    y_r
                )
            ),
            np.max(
                np.abs(
                    y_phi
                )
            ),
            abs(
                y_support
            ),
        )
    )

    if max_strain > (
        strain_cap
        +
        1.0e-10
    ):

        return None

    w_r = np.tanh(
        k
        * y_r
    )

    w_phi = np.tanh(
        k
        * y_phi
    )

    s = math.tanh(
        k
        * y_support
    )

    # Declared primary subclass:
    # radial tension remains sign-definite.
    if np.max(
        w_r
    ) >= -1.0e-3:

        return None

    if s <= 1.0e-4:

        return None

    integrand = np.zeros_like(
        x
    )

    integrand[
        1:
    ] = (
        -(
            1.0
            -
            w_phi[
                1:
            ]
            /
            w_r[
                1:
            ]
        )
        /
        x[
            1:
        ]
    )

    # Regular center: y_r=y_phi, so the limit is zero.
    integrand[
        0
    ] = 0.0

    ln_abs_pr = np.concatenate(
        (
            np.asarray(
                [
                    0.0
                ]
            ),
            cumulative_trapezoid(
                integrand,
                x,
            ),
        )
    )

    if (
        np.max(
            ln_abs_pr
        )
        -
        np.min(
            ln_abs_pr
        )
        >
        40.0
    ):

        return None

    p_r = (
        -np.exp(
            ln_abs_pr
            -
            ln_abs_pr[0]
        )
    )

    rho = (
        p_r
        /
        w_r
    )

    if (
        np.min(
            rho
        )
        <=
        0.0
        or
        not np.all(
            np.isfinite(
                rho
            )
        )
    ):

        return None

    p_phi = (
        w_phi
        * rho
    )

    r = (
        R
        * x
    )

    active = (
        rho
        +
        p_r
        +
        p_phi
    )

    lambda_line = (
        -R
        * p_r[
            -1
        ]
        /
        s
    )

    if lambda_line <= 0.0:

        return None

    mass_surface = (
        2.0
        * np.trapezoid(
            r
            * rho,
            r,
        )
    )

    mass_line = (
        2.0
        * R
        * lambda_line
    )

    mass = (
        mass_surface
        +
        mass_line
    )

    field_surface = (
        -np.trapezoid(
            r
            * active
            /
            (
                1.0
                +
                r * r
            ) ** 1.5,
            r,
        )
    )

    field_line = (
        -R
        * (
            1.0
            +
            s
        )
        * lambda_line
        /
        (
            1.0
            +
            R * R
        ) ** 1.5
    )

    F = (
        field_surface
        +
        field_line
    )

    if (
        not math.isfinite(
            F
        )
        or
        F
        <=
        0.0
    ):

        return None

    C = (
        mass
        /
        (
            2.0
            * F
        )
    )

    log_H = (
        y_r
        +
        y_phi
        +
        (
            logcosh(
                k
                * y_r
            )
            +
            logcosh(
                k
                * y_phi
            )
        )
        /
        k
    )

    rho_star = (
        rho
        /
        np.exp(
            log_H
        )
    )

    grading_contrast = (
        float(
            np.max(
                rho_star
            )
        )
        /
        float(
            np.min(
                rho_star
            )
        )
    )

    # Direct discrete equilibrium residual.
    dp_dr = np.gradient(
        p_r,
        r,
        edge_order=2,
    )

    residual = (
        dp_dr
        +
        (
            p_r
            -
            p_phi
        )
        /
        np.where(
            r > 0.0,
            r,
            1.0,
        )
    )

    residual[
        0
    ] = residual[
        1
    ]

    residual_scale = max(
        float(
            np.max(
                np.abs(
                    dp_dr
                )
            )
        ),
        float(
            np.max(
                np.abs(
                    p_r
                    -
                    p_phi
                )
                /
                np.maximum(
                    r,
                    R
                    /
                    max(
                        n - 1,
                        1,
                    )
                )
            )
        ),
        1.0e-12,
    )

    residual_rel = float(
        np.max(
            np.abs(
                residual
            )
        )
        /
        residual_scale
    )

    out = {
        "k":
            k,

        "R":
            R,

        "g0":
            g0,

        "c2":
            c2,

        "c4":
            c4,

        "c6":
            c6,

        "c8":
            c8,

        "y_support":
            y_support,

        "support_ratio":
            s,

        "C":
            C,

        "F":
            F,

        "mass":
            mass,

        "mass_surface":
            mass_surface,

        "mass_line":
            mass_line,

        "lambda_line":
            lambda_line,

        "max_log_strain":
            max_strain,

        "min_y_r":
            float(
                np.min(
                    y_r
                )
            ),

        "max_y_r":
            float(
                np.max(
                    y_r
                )
            ),

        "min_y_phi":
            float(
                np.min(
                    y_phi
                )
            ),

        "max_y_phi":
            float(
                np.max(
                    y_phi
                )
            ),

        "min_w_r":
            float(
                np.min(
                    w_r
                )
            ),

        "max_w_r":
            float(
                np.max(
                    w_r
                )
            ),

        "min_w_phi":
            float(
                np.min(
                    w_phi
                )
            ),

        "max_w_phi":
            float(
                np.max(
                    w_phi
                )
            ),

        "min_orientation_jacobian":
            float(
                np.min(
                    jacobian
                )
            ),

        "rho_star_grading_contrast":
            grading_contrast,

        "rho_star_min":
            float(
                np.min(
                    rho_star
                )
            ),

        "rho_star_max":
            float(
                np.max(
                    rho_star
                )
            ),

        "equilibrium_residual_relative":
            residual_rel,
    }

    if return_profile:

        out[
            "profile"
        ] = {
            "x":
                x,

            "r":
                r,

            "g":
                g,

            "y_r":
                y_r,

            "y_phi":
                y_phi,

            "w_r":
                w_r,

            "w_phi":
                w_phi,

            "rho":
                rho,

            "p_r":
                p_r,

            "p_phi":
                p_phi,

            "active":
                active,

            "rho_star":
                rho_star,
        }

    return out


def objective(
    vector: np.ndarray,
    strain_cap: float,
) -> float:
    """Optimization objective for compatible radial maps."""

    row = profile_metrics(
        vector,
        strain_cap,
        PROFILE_N,
        return_profile=False,
    )

    if row is None:

        return 1.0e6

    # Conservation is constructed analytically.
    # Add only a tiny numerical tie-break against poorly resolved profiles.
    return (
        row[
            "C"
        ]
        +
        1.0e-3
        * row[
            "equilibrium_residual_relative"
        ]
    )


def optimize_compatible(
    strain_cap: float,
    seed: int,
) -> dict | None:
    """Independent differential-evolution compatible-map search."""

    cap = float(
        strain_cap
    )

    lower_g = (
        -max(
            cap,
            0.30,
        )
    )

    upper_g = (
        -0.15
    )

    support_hi = max(
        0.20,
        cap,
    )

    bounds = (
        (
            0.50,
            0.95,
        ),
        (
            1.5,
            7.0,
        ),
        (
            lower_g,
            upper_g,
        ),
        (
            -1.0,
            +1.0,
        ),
        (
            -1.0,
            +1.0,
        ),
        (
            -1.0,
            +1.0,
        ),
        (
            -1.0,
            +1.0,
        ),
        (
            0.15,
            support_hi,
        ),
    )

    initial_strain = min(
        0.95
        * cap,
        3.8,
    )

    x0 = np.asarray(
        [
            min(
                0.949,
                0.50
                +
                0.45
            ),
            4.0,
            -initial_strain,
            0.0,
            0.0,
            0.0,
            0.0,
            max(
                0.20,
                initial_strain,
            ),
        ]
    )

    result = differential_evolution(
        lambda x:
            objective(
                x,
                cap,
            ),
        bounds,
        seed=seed,
        maxiter=SEARCH_MAXITER,
        popsize=SEARCH_POPSIZE,
        tol=1.0e-9,
        atol=1.0e-9,
        polish=True,
        workers=1,
        updating="immediate",
        x0=x0,
    )

    row = profile_metrics(
        result.x,
        cap,
        PROFILE_HIGH_N,
        return_profile=False,
    )

    if row is None:

        return None

    row[
        "optimizer_fun"
    ] = float(
        result.fun
    )

    row[
        "optimizer_success"
    ] = bool(
        result.success
    )

    row[
        "optimizer_nfev"
    ] = int(
        result.nfev
    )

    row[
        "seed"
    ] = int(
        seed
    )

    row[
        "strain_cap"
    ] = cap

    return row


def best_over_seeds(
    strain_cap: float,
) -> tuple[
    dict | None,
    list[dict],
]:
    """Run independent seeds and return the best high-resolution result."""

    rows = []

    base = (
        250000
        +
        int(
            100
            * strain_cap
        )
    )

    for j in range(
        SEARCH_SEEDS
    ):

        row = optimize_compatible(
            strain_cap,
            base + j,
        )

        if row is not None:

            rows.append(
                row
            )

    if not rows:

        return (
            None,
            [],
        )

    rows.sort(
        key=lambda item:
            item[
                "C"
            ]
    )

    return (
        rows[0],
        rows,
    )


# ----------------------------------------------------------------------
# Finite payload for an arbitrary compatible radial source.
# ----------------------------------------------------------------------

def field_at_payload_points(
    profile: dict,
    support_ratio: float,
    lambda_line: float,
    R: float,
    rho_p: np.ndarray,
    z_p: np.ndarray,
) -> np.ndarray:
    """Direct Green-function axial field of arbitrary thin radial profile."""

    r = profile[
        "r"
    ]

    active = profile[
        "active"
    ]

    phi = np.linspace(
        0.0,
        2.0
        * math.pi,
        PAYLOAD_PHI,
        endpoint=False,
    )

    cos_phi = np.cos(
        phi
    )

    result = np.zeros(
        len(
            rho_p
        ),
        dtype=float,
    )

    for j in range(
        len(
            rho_p
        )
    ):

        rp = float(
            rho_p[
                j
            ]
        )

        zp = float(
            z_p[
                j
            ]
        )

        d2 = (
            rp * rp
            +
            r[:, None]
            * r[:, None]
            -
            2.0
            * rp
            * r[:, None]
            * cos_phi[
                None,
                :
            ]
            +
            zp * zp
        )

        kernel = (
            zp
            /
            d2 ** 1.5
        )

        angular = np.mean(
            kernel,
            axis=1,
        )

        surface = (
            -np.trapezoid(
                r
                * active
                * angular,
                r,
            )
        )

        d2_line = (
            rp * rp
            +
            R * R
            -
            2.0
            * rp
            * R
            * cos_phi
            +
            zp * zp
        )

        line_kernel = float(
            np.mean(
                zp
                /
                d2_line ** 1.5
            )
        )

        line = (
            -R
            * (
                1.0
                +
                support_ratio
            )
            * lambda_line
            * line_kernel
        )

        result[
            j
        ] = (
            surface
            +
            line
        )

    return result


def payload_audit(
    best: dict,
) -> dict:
    """Independent finite spherical-payload audit."""

    vector = np.asarray(
        [
            best["k"],
            best["R"],
            best["g0"],
            best["c2"],
            best["c4"],
            best["c6"],
            best["c8"],
            best["y_support"],
        ]
    )

    row = profile_metrics(
        vector,
        best[
            "strain_cap"
        ],
        PROFILE_HIGH_N,
        return_profile=True,
    )

    if row is None:

        raise RuntimeError(
            "Selected compatible profile could not be rebuilt"
        )

    profile = row[
        "profile"
    ]

    center = field_at_payload_points(
        profile,
        row[
            "support_ratio"
        ],
        row[
            "lambda_line"
        ],
        row[
            "R"
        ],
        np.asarray(
            [
                0.0
            ]
        ),
        np.asarray(
            [
                1.0
            ]
        ),
    )[
        0
    ]

    center_relerr = (
        abs(
            center
            -
            row[
                "F"
            ]
        )
        /
        max(
            abs(
                row[
                    "F"
                ]
            ),
            1.0e-300,
        )
    )

    power = int(
        math.ceil(
            math.log2(
                PAYLOAD_SAMPLES
            )
        )
    )

    raw = qmc.Sobol(
        d=3,
        scramble=True,
        seed=250299,
    ).random_base2(
        power
    )[
        :PAYLOAD_SAMPLES
    ]

    radius = (
        PAYLOAD_RADIUS
        * raw[
            :,
            0
        ] ** (
            1.0
            /
            3.0
        )
    )

    cos_theta = (
        2.0
        * raw[
            :,
            1
        ]
        -
        1.0
    )

    sin_theta = np.sqrt(
        np.maximum(
            0.0,
            1.0
            -
            cos_theta
            * cos_theta,
        )
    )

    az = (
        2.0
        * math.pi
        * raw[
            :,
            2
        ]
    )

    x = (
        radius
        * sin_theta
        * np.cos(
            az
        )
    )

    y = (
        radius
        * sin_theta
        * np.sin(
            az
        )
    )

    z = (
        1.0
        +
        radius
        * cos_theta
    )

    rho_p = np.sqrt(
        x * x
        +
        y * y
    )

    fields = field_at_payload_points(
        profile,
        row[
            "support_ratio"
        ],
        row[
            "lambda_line"
        ],
        row[
            "R"
        ],
        rho_p,
        z,
    )

    mean_field = float(
        np.mean(
            fields
        )
    )

    finite_C = (
        row[
            "mass"
        ]
        /
        (
            2.0
            * mean_field
        )
        if mean_field > 0.0
        else math.inf
    )

    return {
        "sample_count":
            PAYLOAD_SAMPLES,

        "radius_over_h":
            PAYLOAD_RADIUS,

        "analytic_center_F":
            row[
                "F"
            ],

        "numeric_center_F":
            float(
                center
            ),

        "center_relative_error":
            center_relerr,

        "mean_F":
            mean_field,

        "min_F":
            float(
                np.min(
                    fields
                )
            ),

        "max_F":
            float(
                np.max(
                    fields
                )
            ),

        "all_outward":
            bool(
                np.all(
                    fields
                    >
                    0.0
                )
            ),

        "finite_payload_C":
            finite_C,
    }


def print_candidate(
    prefix: str,
    row: dict | None,
) -> None:
    """Print compatible candidate summary."""

    if row is None:

        print(
            f"{prefix}_SURVIVOR=NO"
        )

        return

    print(
        f"{prefix}_SURVIVOR=YES"
    )

    for key in (
        "C",
        "F",
        "mass",
        "k",
        "R",
        "g0",
        "c2",
        "c4",
        "c6",
        "c8",
        "y_support",
        "support_ratio",
        "max_log_strain",
        "min_y_r",
        "max_y_r",
        "min_y_phi",
        "max_y_phi",
        "min_w_r",
        "max_w_r",
        "min_w_phi",
        "max_w_phi",
        "min_orientation_jacobian",
        "rho_star_grading_contrast",
        "equilibrium_residual_relative",
        "lambda_line",
    ):

        print(
            f"{prefix}_{key.upper()}="
            f"{float(row[key]):.15e}"
        )


def main() -> None:
    """Execute 025B0."""

    print(
        "=== 025B0 HYPERELASTIC COMPATIBILITY + FULL ACOUSTIC CONE ==="
    )

    previous = json.loads(
        PREV.read_text(
            encoding="utf-8"
        )
    )

    selected = previous[
        "selected"
    ]

    if selected is None:

        raise RuntimeError(
            "025A selected state unavailable"
        )

    print(
        "\n=== A — PREDECESSOR ANCHORS ==="
    )

    print(
        f"C_006B="
        f"{C006B:.15e}"
    )

    print(
        f"C_006D="
        f"{C006D:.15e}"
    )

    print(
        f"C_005B="
        f"{C005B:.15e}"
    )

    print(
        f"C_025A_SELECTED="
        f"{float(selected['C']):.15e}"
    )

    print(
        f"K_025A_SELECTED="
        f"{float(selected['k']):.15e}"
    )

    print(
        f"T_025A_SELECTED="
        f"{float(selected['t']):.15e}"
    )

    print(
        f"Q_025A_SELECTED="
        f"{float(selected['q']):.15e}"
    )

    print(
        f"SUPPORT_025A_SELECTED="
        f"{float(selected['support']):.15e}"
    )

    # --------------------------------------------------------------
    # B. Exact compatibility theorem.
    # --------------------------------------------------------------

    print(
        "\n=== B — EXACT RADIAL COMPATIBILITY AUDIT ==="
    )

    k = float(
        selected[
            "k"
        ]
    )

    Y_core = (
        math.atanh(
            float(
                selected[
                    "t"
                ]
            )
        )
        /
        k
    )

    Y_ann = (
        math.atanh(
            float(
                selected[
                    "q"
                ]
            )
        )
        /
        k
    )

    core_X_over_r = math.exp(
        -Y_core
    )

    ann_X_over_r = math.exp(
        +Y_ann
    )

    discontinuity_ratio = (
        ann_X_over_r
        /
        core_X_over_r
    )

    print(
        f"TARGET_Y_CORE_MAGNITUDE="
        f"{Y_core:.15e}"
    )

    print(
        f"TARGET_Y_ANNULUS_MAGNITUDE="
        f"{Y_ann:.15e}"
    )

    print(
        f"TARGET_CORE_X_OVER_R="
        f"{core_X_over_r:.15e}"
    )

    print(
        f"TARGET_ANNULUS_X_OVER_R="
        f"{ann_X_over_r:.15e}"
    )

    print(
        f"TARGET_INTERFACE_X_OVER_R_JUMP_RATIO="
        f"{discontinuity_ratio:.15e}"
    )

    print(
        "EXACT_PIECEWISE_025A_TARGET_CONTINUOUS_RADIAL_MAP=NO"
    )

    print(
        "SMOOTH_NEGATIVE_TO_POSITIVE_Y_PHI_CROSSING_"
        "PRESERVES_RADIAL_TENSION_EVERYWHERE=NO"
    )

    print(
        "COMPATIBILITY_REASON="
        "Y_R_EQUALS_G_PLUS_LOG_ONE_PLUS_R_GPRIME"
    )

    print(
        "DIRECT_DIAGONAL_006B_STRESS_STATE_REALIZATION="
        "INCOMPATIBLE_WITH_ORDINARY_EUCLIDEAN_REFERENCE_RADIAL_MAP"
    )

    # --------------------------------------------------------------
    # C. Acoustic cone.
    # --------------------------------------------------------------

    print(
        "\n=== C — FULL RELATIVISTIC ACOUSTIC CONE ===",
        flush=True,
    )

    acoustic = acoustic_validation(
        selected
    )

    print(
        f"ACOUSTIC_ZERO_STRAIN_MAX_ERROR="
        f"{acoustic['zero_strain_max_error']:.15e}"
    )

    print(
        "ACOUSTIC_ZERO_STRAIN_VALIDATION="
        +
        (
            "PASS"
            if acoustic[
                "zero_strain_pass"
            ]
            else "FAIL"
        )
    )

    print(
        f"ACOUSTIC_PRINCIPAL_LONGITUDINAL_MAX_ERROR="
        f"{acoustic['principal_longitudinal_max_error']:.15e}"
    )

    print(
        "ACOUSTIC_PRINCIPAL_LONGITUDINAL_VALIDATION="
        +
        (
            "PASS"
            if acoustic[
                "principal_longitudinal_pass"
            ]
            else "FAIL"
        )
    )

    for name, item in acoustic[
        "state_summary"
    ].items():

        preferred = item[
            "by_step"
        ][
            str(
                METRIC_STEPS[
                    1
                ]
            )
        ]

        print(
            f"ACOUSTIC_{name}_MIN_V2="
            f"{preferred['min_v2']:.15e}"
        )

        print(
            f"ACOUSTIC_{name}_MAX_V2="
            f"{preferred['max_v2']:.15e}"
        )

        print(
            f"ACOUSTIC_{name}_MIN_STEP_DIFFERENCE="
            f"{item['min_step_difference']:.15e}"
        )

        print(
            f"ACOUSTIC_{name}_MAX_STEP_DIFFERENCE="
            f"{item['max_step_difference']:.15e}"
        )

        print(
            f"ACOUSTIC_{name}_NEGATIVE_DIRECTION_COUNT="
            f"{preferred['negative_direction_count']}"
        )

        print(
            f"ACOUSTIC_{name}_SUPERLUMINAL_DIRECTION_COUNT="
            f"{preferred['superluminal_direction_count']}"
        )

        print(
            f"ACOUSTIC_{name}_FULL_DIRECTION_GATE="
            +
            (
                "PASS"
                if item[
                    "pass"
                ]
                else "FAIL"
            )
        )

    print(
        "FULL_SELECTED_STATE_ACOUSTIC_CONE="
        +
        (
            "PASS"
            if acoustic[
                "full_cone_pass"
            ]
            else "FAIL"
        )
    )

    # --------------------------------------------------------------
    # D. Compatible deformation scout.
    # --------------------------------------------------------------

    print(
        "\n=== D — COMPATIBLE RADIAL-MAP SEARCH ===",
        flush=True,
    )

    frontier_rows = []
    best_by_cap = {}

    for cap in PRIMARY_CAPS:

        print(
            f"COMPATIBLE_SEARCH_BEGIN_STRAIN_CAP="
            f"{cap:.6f}",
            flush=True,
        )

        best, rows = best_over_seeds(
            cap
        )

        best_by_cap[
            str(cap)
        ] = best

        for row in rows:

            frontier_rows.append(
                row
            )

        print_candidate(
            "COMPATIBLE_CAP_"
            +
            str(cap).replace(
                ".",
                "P",
            ),
            best,
        )

    # --------------------------------------------------------------
    # E. Wildcard diagnostics.
    # --------------------------------------------------------------

    print(
        "\n=== E — BLIND WILDCARD COMPATIBILITY DIAGNOSTICS ==="
    )

    wildcard_rows = []

    for cap in WILDCARD_CAPS:

        best, _ = best_over_seeds(
            cap
        )

        wildcard_rows.append({
            "cap":
                cap,

            "best":
                best,
        })

        if best is None:

            print(
                f"WILDCARD_COMPATIBLE_STRAIN_CAP={cap:.6f} "
                "BEST_C=inf "
                "ROLE=BLIND_WILDCARD_NOT_PHYSICS_PRIOR"
            )

        else:

            print(
                f"WILDCARD_COMPATIBLE_STRAIN_CAP={cap:.6f} "
                f"BEST_C={best['C']:.12e} "
                "ROLE=BLIND_WILDCARD_NOT_PHYSICS_PRIOR"
            )

    print(
        "WILDCARDS_USED_FOR_SELECTION=NO"
    )

    # --------------------------------------------------------------
    # F. High-resolution convergence for cap 4.
    # --------------------------------------------------------------

    print(
        "\n=== F — CAP-4 HIGH-RESOLUTION RECONSTRUCTION ==="
    )

    best4 = best_by_cap.get(
        "4.0"
    )

    best4_high = None

    if best4 is not None:

        vector = np.asarray(
            [
                best4["k"],
                best4["R"],
                best4["g0"],
                best4["c2"],
                best4["c4"],
                best4["c6"],
                best4["c8"],
                best4["y_support"],
            ]
        )

        low = profile_metrics(
            vector,
            4.0,
            PROFILE_N,
            return_profile=False,
        )

        high = profile_metrics(
            vector,
            4.0,
            PROFILE_HIGH_N,
            return_profile=True,
        )

        if (
            low is None
            or
            high is None
        ):

            raise RuntimeError(
                "Cap-4 compatible candidate failed reconstruction"
            )

        C_rel = (
            abs(
                low[
                    "C"
                ]
                -
                high[
                    "C"
                ]
            )
            /
            max(
                abs(
                    high[
                        "C"
                    ]
                ),
                1.0e-300,
            )
        )

        F_rel = (
            abs(
                low[
                    "F"
                ]
                -
                high[
                    "F"
                ]
            )
            /
            max(
                abs(
                    high[
                        "F"
                    ]
                ),
                1.0e-300,
            )
        )

        best4_high = high

        print(
            f"CAP4_LOW_C="
            f"{low['C']:.15e}"
        )

        print(
            f"CAP4_HIGH_C="
            f"{high['C']:.15e}"
        )

        print(
            f"CAP4_C_RELATIVE_DIFFERENCE="
            f"{C_rel:.15e}"
        )

        print(
            f"CAP4_F_RELATIVE_DIFFERENCE="
            f"{F_rel:.15e}"
        )

        convergence_pass = bool(
            C_rel
            <=
            5.0e-3
            and
            F_rel
            <=
            5.0e-3
        )

        print(
            "CAP4_PROFILE_CONVERGENCE="
            +
            (
                "PASS"
                if convergence_pass
                else "FAIL"
            )
        )

    else:

        convergence_pass = False

        print(
            "CAP4_PROFILE_CONVERGENCE="
            "NOT_RUN_NO_SURVIVOR"
        )

    # --------------------------------------------------------------
    # G. Finite payload.
    # --------------------------------------------------------------

    print(
        "\n=== G — FINITE PAYLOAD AUDIT OF BEST COMPATIBLE CAP-4 MAP ==="
    )

    payload = None

    if best4 is not None:

        payload = payload_audit(
            best4
        )

        for key, value in payload.items():

            if isinstance(
                value,
                bool,
            ):

                print(
                    f"COMPATIBLE_PAYLOAD_{key.upper()}="
                    +
                    (
                        "YES"
                        if value
                        else "NO"
                    )
                )

            elif isinstance(
                value,
                int,
            ):

                print(
                    f"COMPATIBLE_PAYLOAD_{key.upper()}="
                    f"{value}"
                )

            else:

                print(
                    f"COMPATIBLE_PAYLOAD_{key.upper()}="
                    f"{float(value):.15e}"
                )

        payload_pass = bool(
            payload[
                "all_outward"
            ]
            and
            payload[
                "mean_F"
            ]
            >
            0.0
            and
            payload[
                "center_relative_error"
            ]
            <=
            5.0e-3
        )

        print(
            "COMPATIBLE_FINITE_PAYLOAD_AUDIT="
            +
            (
                "PASS"
                if payload_pass
                else "FAIL"
            )
        )

    else:

        payload_pass = False

        print(
            "COMPATIBLE_FINITE_PAYLOAD_AUDIT="
            "NOT_RUN_NO_SURVIVOR"
        )

    # --------------------------------------------------------------
    # H. Decision.
    # --------------------------------------------------------------

    print(
        "\n=== H — 025B0 DECISION ==="
    )

    exact_target_compatible = False

    cap4_C = (
        float(
            best4_high[
                "C"
            ]
        )
        if best4_high is not None
        else math.inf
    )

    compatible_lt30 = bool(
        math.isfinite(
            cap4_C
        )
        and
        cap4_C
        <
        30.0
        and
        convergence_pass
        and
        payload_pass
    )

    compatible_beats_006d = bool(
        compatible_lt30
        and
        cap4_C
        <
        C006D
    )

    compatible_near_005b = bool(
        math.isfinite(
            cap4_C
        )
        and
        (
            cap4_C
            /
            C005B
        )
        >=
        0.75
    )

    local_law_survives = bool(
        acoustic[
            "full_cone_pass"
        ]
    )

    print(
        "EXACT_025A_PIECEWISE_RADIAL_MAP_COMPATIBLE="
        +
        (
            "YES"
            if exact_target_compatible
            else "NO"
        )
    )

    print(
        "LOCAL_025A_FULL_ACOUSTIC_CONE_SURVIVES="
        +
        (
            "YES"
            if local_law_survives
            else "NO"
        )
    )

    print(
        "COMPATIBLE_CAP4_C_LT_30="
        +
        (
            "YES"
            if compatible_lt30
            else "NO"
        )
    )

    print(
        "COMPATIBLE_CAP4_BEATS_006D="
        +
        (
            "YES"
            if compatible_beats_006d
            else "NO"
        )
    )

    print(
        "COMPATIBLE_CAP4_REGRESSES_TOWARD_005B_SCALE="
        +
        (
            "YES"
            if compatible_near_005b
            else "NO"
        )
    )

    if not local_law_survives:

        decision = (
            "RED_025A_HYPERELASTIC_CONSTITUTIVE_LAW_"
            "FAILS_FULL_ACOUSTIC_CONE"
        )

        interpretation = (
            "LOCAL_PRINCIPAL_CAUSALITY_WAS_INSUFFICIENT_"
            "ARBITRARY_DIRECTION_CHARACTERISTICS_KILL_MODEL"
        )

        next_action = (
            "CLOSE_025A_025B0_AND_GLOBAL_RERANK"
        )

    elif compatible_beats_006d:

        decision = (
            "YELLOW_STRONG_GLOBALLY_COMPATIBLE_RADIAL_"
            "HYPERELASTIC_PREFLIGHT"
        )

        interpretation = (
            "SAME_CONSTITUTIVE_LAW_SURVIVES_COMPATIBILITY_"
            "WITH_006D_LEVEL_SOURCE_EFFICIENCY"
        )

        next_action = (
            "025B1_FINITE_THICKNESS_AXISYMMETRIC_"
            "HYPERELASTIC_BVP_WITH_SMOOTH_COLLARS"
        )

    elif compatible_lt30:

        decision = (
            "YELLOW_COMPATIBLE_HYPERELASTIC_SOURCE_SURVIVES_"
            "WITH_MODERATE_EFFICIENCY_PENALTY"
        )

        interpretation = (
            "EXACT_006B_TARGET_IS_INCOMPATIBLE_BUT_A_NEW_"
            "COMPATIBLE_STRESS_PROFILE_RETAINS_USEFUL_HEADROOM"
        )

        next_action = (
            "025B1_FINITE_THICKNESS_COMPATIBLE_MATERIAL_BVP"
        )

    else:

        decision = (
            "YELLOW_LOCAL_LAW_SURVIVES_BUT_DIRECT_006B_"
            "MATERIAL_REALIZATION_DEMOTED_BY_COMPATIBILITY"
        )

        interpretation = (
            "COMPATIBILITY_ERASES_THE_006B_STRESS_TRANSFER_"
            "ADVANTAGE_IN_TESTED_RADIAL_MAP_SUBCLASS"
        )

        next_action = (
            "025B1_ANALYTIC_FULL_2D_AXISYMMETRIC_MAP_VS_"
            "NON_EUCLIDEAN_REFERENCE_METRIC_DECISION_GATE"
        )

    print(
        f"025B0_INTERPRETATION="
        f"{interpretation}"
    )

    print(
        f"025B0_DECISION="
        f"{decision}"
    )

    print(
        f"NEXT="
        f"{next_action}"
    )

    print(
        "ORDINARY_EUCLIDEAN_REFERENCE_RADIAL_MAP_TESTED=YES"
    )

    print(
        "GENERAL_2D_AXISYMMETRIC_MAP_TESTED=NO"
    )

    print(
        "NON_EUCLIDEAN_REFERENCE_METRIC_TESTED=NO"
    )

    print(
        "FINITE_THICKNESS_COLLAR_BVP=NO"
    )

    print(
        "NONLINEAR_GR=NO"
    )

    print(
        "REMOVES_1_OVER_G_SCALING=NO"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "70_TO_71_PERCENT_RETAIN_UNLESS_GLOBAL_MATERIAL_PROMOTION_IS_EARNED"
    )

    # --------------------------------------------------------------
    # Persist outputs.
    # --------------------------------------------------------------

    if frontier_rows:

        fields = sorted({
            key
            for row in frontier_rows
            for key in row.keys()
            if not isinstance(
                row[
                    key
                ],
                dict,
            )
        })

        with OUTF.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=fields,
                extrasaction="ignore",
            )

            writer.writeheader()

            writer.writerows(
                frontier_rows
            )

    cone_rows = acoustic[
        "cone_rows"
    ]

    if cone_rows:

        fields = list(
            cone_rows[
                0
            ].keys()
        )

        with OUTC.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=fields,
            )

            writer.writeheader()

            writer.writerows(
                cone_rows
            )

    if best4_high is not None:

        p = best4_high[
            "profile"
        ]

        np.savez_compressed(
            OUTN,
            x=p["x"],
            r=p["r"],
            g=p["g"],
            y_r=p["y_r"],
            y_phi=p["y_phi"],
            w_r=p["w_r"],
            w_phi=p["w_phi"],
            rho=p["rho"],
            p_r=p["p_r"],
            p_phi=p["p_phi"],
            active=p["active"],
            rho_star=p["rho_star"],
            parameters=np.asarray(
                [
                    best4_high["k"],
                    best4_high["R"],
                    best4_high["g0"],
                    best4_high["c2"],
                    best4_high["c4"],
                    best4_high["c6"],
                    best4_high["c8"],
                    best4_high["y_support"],
                    best4_high["C"],
                ]
            ),
        )

    serial_best = {}

    for cap, row in best_by_cap.items():

        serial_best[
            cap
        ] = row

    summary = {
        "claim_classification":
            (
                "PROJECT_DERIVED_HYPERELASTIC_COMPATIBILITY_"
                "AND_FULL_ACOUSTIC_CONE_GATE"
            ),

        "anchors": {
            "C006B":
                C006B,

            "C006D":
                C006D,

            "C005B":
                C005B,

            "C025A_selected":
                float(
                    selected[
                        "C"
                    ]
                ),
        },

        "compatibility": {
            "Y_core":
                Y_core,

            "Y_annulus":
                Y_ann,

            "core_X_over_r":
                core_X_over_r,

            "annulus_X_over_r":
                ann_X_over_r,

            "required_jump_ratio":
                discontinuity_ratio,

            "exact_piecewise_target_compatible":
                False,

            "identity":
                (
                    "y_r=g+ln(1+r*gprime), y_phi=g"
                ),

            "scope":
                (
                    "ordinary Euclidean-reference diagonal radial map"
                ),
        },

        "acoustic": {
            key: value
            for key, value in acoustic.items()
            if key not in (
                "zero_rows",
                "principal_rows",
                "cone_rows",
            )
        },

        "compatible_best_by_cap":
            serial_best,

        "best_cap4_high":
            (
                {
                    key: value
                    for key, value
                    in best4_high.items()
                    if key != "profile"
                }
                if best4_high is not None
                else None
            ),

        "payload":
            payload,

        "decision": {
            "local_full_acoustic_cone_survives":
                local_law_survives,

            "exact_025A_piecewise_radial_compatible":
                exact_target_compatible,

            "compatible_cap4_C_lt_30":
                compatible_lt30,

            "compatible_cap4_beats_006D":
                compatible_beats_006d,

            "compatible_cap4_regresses_toward_005B":
                compatible_near_005b,

            "interpretation":
                interpretation,

            "result":
                decision,

            "next":
                next_action,

            "practical_device":
                False,
        },

        "limits": [
            "RADIAL_SIGN_DEFINITE_TENSION_SUBCLASS_FOR_COMPATIBLE_SCOUT",
            "NO_GENERAL_2D_AXISYMMETRIC_MAP",
            "NO_NON_EUCLIDEAN_REFERENCE_METRIC",
            "NO_FINITE_THICKNESS_COLLAR_BVP",
            "NO_NONLINEAR_GR",
            "NO_1_OVER_G_ESCAPE",
            "NO_DEVICE",
        ],
    }

    OUTJ.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
            allow_nan=True,
        )
        +
        "\n",
        encoding="utf-8",
    )

    print(
        f"SUMMARY_JSON="
        f"{OUTJ.relative_to(ROOT)}"
    )

    print(
        f"FRONTIER_CSV="
        f"{OUTF.relative_to(ROOT)}"
    )

    print(
        f"ACOUSTIC_CONE_CSV="
        f"{OUTC.relative_to(ROOT)}"
    )

    if OUTN.is_file():

        print(
            f"BEST_PROFILE_NPZ="
            f"{OUTN.relative_to(ROOT)}"
        )

    print(
        "025B0_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
