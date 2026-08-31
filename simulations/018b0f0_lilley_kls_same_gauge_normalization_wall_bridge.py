#!/usr/bin/env python3
"""Simulation 018B-0F0 — Lilley/KLS same-gauge normalization and wall bridge.

PURPOSE
-------
Build the minimum explicit bridge between the literature-backed two-current
string selected by 018B-0D and the nonthermal KLS wall architecture used by
018A before any stationary loop/wall/gravity search is attempted.

SCIENTIFIC QUESTION
-------------------
Can the charged Higgs field H of the Lilley-Martin-Peter two-current string be
reinterpreted as charge two under a fundamental local U(1)_X, with a new
charge-one KLS wall field A, while preserving:

- the published two-current local string equations;
- U(1) -> Z2 -> 1 topology;
- one branch wall per unit vortex;
- the intended homogeneous vacuum;
- a finite relaxed microscopic wall;
- stable current-carrier fluctuations on that wall?

WHY THIS GATE IS REQUIRED
-------------------------
018B-0D and the older 017P string use different Higgs/gauge normalizations.
Therefore the old 018A junction energy and stress cannot simply be inserted
into the two-current model.

This gate reconstructs the topology and planar wall in one normalization.
The two-dimensional string-wall junction remains a later explicit calculation.

LITERATURE MODEL
----------------
The two-current model contains one locally charged complex Higgs H, gauge
field C_mu, and two neutral current carriers Phi and Sigma.

Use the canonical representative lambda_H = eta_H = 1. This fixes units only;
it is not an additional physical assertion.

The 018B-0D log reconstructs

    qtilde^2 = q^2/lambda_H

    alpha_i = m_i^2/(lambda_i eta_H^2)

    beta_i =
        f_i m_i^2
        /(lambda_H lambda_i eta_H^2)

    gamma_i =
        m_i^4
        /(lambda_H lambda_i eta_H^4).

SAME-GAUGE TOPOLOGY
-------------------
Assign

    Q_H = 2
    Q_A = 1
    g_X = q/Q_H.

Then

    Q_H g_X = q,

so the already reproduced local H/gauge equations are unchanged.

For a unit H vortex,

    g_X integral C.dl = pi.

The charge-one A field therefore sees Wilson phase

    exp(i pi) = -1.

Use the gauge-invariant phase-lock interaction

    -h (H^* A^2 + H A^{*2}).

The vacuum then retains a Z2 branch structure and one wall can terminate on
one unit H string.

COMBINED HOMOGENEOUS POTENTIAL
------------------------------
After minimizing the relative phase,

    V_H =
        lambda_H/8 (H^2-1)^2

and

    V_curr =
        1/2 m_phi^2 Phi^2
        + 1/2 m_sigma^2 Sigma^2
        + 1/2 (H^2-1)
          (f_phi Phi^2 + f_sigma Sigma^2)
        + lambda_phi/4 Phi^4
        + lambda_sigma/4 Sigma^4
        + g/2 Phi^2 Sigma^2.

The KLS extension is

    V_A =
        lambda_A/4 (A^2-F^2)^2
        - 2 h H A^2
        + c_H (H^2-1)
        + c_A (A^2-F^2)
        + V_0,

with

    c_H = h F^2
    c_A = 2 h
    V_0 = 2 h F^2.

Hence

    H=1,
    A=F,
    Phi=Sigma=0

is an exact stationary zero-energy vacuum.

GLOBAL VACUUM TEST
------------------
At fixed H, minimize analytically over

    x = Phi^2 >= 0
    y = Sigma^2 >= 0.

Because

    lambda_phi lambda_sigma > g^2,

the carrier quartic form is positive definite.

At fixed H the potential is also convex in A^2, so A^2 is minimized
analytically.

The complete four-amplitude homogeneous vacuum problem is therefore reduced
to one numerical dimension H.

PLANAR WALL
-----------
Solve the relaxed H-A wall between

    (H,A)=(1,-F)

and

    (H,A)=(1,+F).

Energy per area:

    sigma_W =
        integral [
            1/2 H'^2
            + A'^2
            + V
        ] dz.

Validation uses:

- domain convergence;
- first-integral / virial residual;
- planar active-source identity;
- positive Phi and Sigma fluctuation masses everywhere;
- a +/-10 percent 3^3 wall-corner test.

No old 018A junction quantity is inherited.

STOP RULE
---------
If this gate is GREEN, proceed to a stationary integer-winding/wall-balance/
gravity scout using the NEW wall.

Only after a promising scout should the new two-current 2D junction be solved.

If RED, classify the bridge failure before modifying the field content.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018B0F0_LILLEY_KLS_SAME_GAUGE_NORMALIZATION_WALL_BRIDGE

This simulation does not establish a global toroidal field solution,
full composite stability, nonlinear Einstein-matter consistency,
practical scaling, or a practical antigravity device.
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path
import re

import numpy as np
from scipy.integrate import simpson, solve_bvp
from scipy.optimize import brentq, minimize_scalar


ROOT = Path(__file__).resolve().parents[1]

D_LOG = (
    ROOT
    / "results/logs"
    / "018b0d_literature_two_current_counterflow_gate.log"
)

A8_LOG = (
    ROOT
    / "results/logs"
    / "018a8_finite_thickness_payload_kernel_closeout.log"
)

LAMBDA_H = 1.0
ETA_H = 1.0

Q_H = 2
Q_A = 1

F_SELECTED = 0.075
H_LOCK_SELECTED = 0.010
LAMBDA_A_SELECTED = 1.0

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

LAMBDA_A_SCAN = (
    0.5,
    1.0,
    2.0,
)

ROBUST_LEVELS = (
    0.90,
    0.95,
    1.00,
    1.05,
    1.10,
)

WALL_CORNER_LEVELS = (
    0.90,
    1.00,
    1.10,
)

# Blind wildcard diagnostic only.
# These values are not optimization targets or physics evidence.
WILDCARD_LAMBDA_A = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)

VACUUM_TOL = 1.0e-9
VACUUM_LOCATION_TOL = 2.0e-5
MIN_HESSIAN = 1.0e-8

VIRIAL_REL_TOL = 2.0e-5
ACTIVE_IDENTITY_REL_TOL = 2.0e-5
BVP_RESIDUAL_TOL = 1.0e-5

MIN_SCALE_SEPARATION = 10.0


def read_scalar(
    path: Path,
    label: str,
) -> float:
    """Read one finite scalar immediately following an exact label."""

    text = path.read_text(
        errors="replace"
    )

    number = (
        r"([+-]?"
        r"(?:\d+(?:\.\d*)?|\.\d+)"
        r"(?:[eE][+-]?\d+)?)"
    )

    match = re.search(
        re.escape(
            label
        )
        +
        number,
        text,
    )

    if match is None:
        raise RuntimeError(
            f"Could not find {label!r} in {path}"
        )

    value = float(
        match.group(
            1
        )
    )

    if not math.isfinite(
        value
    ):
        raise RuntimeError(
            f"Nonfinite {label!r} in {path}"
        )

    return value


def reconstruct_parameters():
    """Reconstruct the canonical representative from 018B-0D."""

    alpha_phi = read_scalar(
        D_LOG,
        "ALPHA_PHI_RECONSTRUCTED=",
    )

    alpha_sigma = read_scalar(
        D_LOG,
        "ALPHA_SIGMA_RECONSTRUCTED=",
    )

    beta_phi = read_scalar(
        D_LOG,
        "BETA_PHI_RECONSTRUCTED=",
    )

    beta_sigma = read_scalar(
        D_LOG,
        "BETA_SIGMA_RECONSTRUCTED=",
    )

    gamma_phi = read_scalar(
        D_LOG,
        "GAMMA_PHI_RECONSTRUCTED=",
    )

    gamma_sigma = read_scalar(
        D_LOG,
        "GAMMA_SIGMA_RECONSTRUCTED=",
    )

    qtilde_sq = read_scalar(
        D_LOG,
        "Q_TILDE_SQ_RECONSTRUCTED=",
    )

    g_coupling = read_scalar(
        D_LOG,
        "G_COUPLING=",
    )

    lambda_phi = (
        gamma_phi
        /
        alpha_phi**2
    )

    lambda_sigma = (
        gamma_sigma
        /
        alpha_sigma**2
    )

    m_phi_sq = (
        alpha_phi
        *
        lambda_phi
    )

    m_sigma_sq = (
        alpha_sigma
        *
        lambda_sigma
    )

    f_phi = (
        beta_phi
        /
        alpha_phi
    )

    f_sigma = (
        beta_sigma
        /
        alpha_sigma
    )

    return {
        "alpha_phi":
            alpha_phi,

        "alpha_sigma":
            alpha_sigma,

        "beta_phi":
            beta_phi,

        "beta_sigma":
            beta_sigma,

        "gamma_phi":
            gamma_phi,

        "gamma_sigma":
            gamma_sigma,

        "qtilde_sq":
            qtilde_sq,

        "qtilde":
            math.sqrt(
                qtilde_sq
            ),

        "g":
            g_coupling,

        "lambda_phi":
            lambda_phi,

        "lambda_sigma":
            lambda_sigma,

        "m_phi_sq":
            m_phi_sq,

        "m_sigma_sq":
            m_sigma_sq,

        "f_phi":
            f_phi,

        "f_sigma":
            f_sigma,
    }


def carrier_minimum(
    H,
    p,
):
    """Exactly minimize the carrier sector over Phi^2,Sigma^2 >= 0."""

    a_phi = (
        p[
            "m_phi_sq"
        ]
        +
        p[
            "f_phi"
        ]
        *
        (
            H
            *
            H
            -
            1.0
        )
    )

    a_sigma = (
        p[
            "m_sigma_sq"
        ]
        +
        p[
            "f_sigma"
        ]
        *
        (
            H
            *
            H
            -
            1.0
        )
    )

    candidates = [
        (
            0.0,
            0.0,
        )
    ]

    if a_phi < 0.0:
        candidates.append(
            (
                -a_phi
                /
                p[
                    "lambda_phi"
                ],
                0.0,
            )
        )

    if a_sigma < 0.0:
        candidates.append(
            (
                0.0,
                -a_sigma
                /
                p[
                    "lambda_sigma"
                ],
            )
        )

    matrix = np.array(
        [
            [
                p[
                    "lambda_phi"
                ],
                p[
                    "g"
                ],
            ],
            [
                p[
                    "g"
                ],
                p[
                    "lambda_sigma"
                ],
            ],
        ],
        dtype=float,
    )

    rhs = np.array(
        [
            -a_phi,
            -a_sigma,
        ],
        dtype=float,
    )

    xy = np.linalg.solve(
        matrix,
        rhs,
    )

    if np.all(
        xy >= 0.0
    ):
        candidates.append(
            (
                float(
                    xy[
                        0
                    ]
                ),
                float(
                    xy[
                        1
                    ]
                ),
            )
        )

    def value(
        x,
        y,
    ):
        return float(
            0.5
            *
            a_phi
            *
            x

            +

            0.5
            *
            a_sigma
            *
            y

            +

            0.25
            *
            p[
                "lambda_phi"
            ]
            *
            x
            *
            x

            +

            0.25
            *
            p[
                "lambda_sigma"
            ]
            *
            y
            *
            y

            +

            0.5
            *
            p[
                "g"
            ]
            *
            x
            *
            y
        )

    best_x, best_y = min(
        candidates,
        key=lambda pair:
            value(
                pair[
                    0
                ],
                pair[
                    1
                ],
            ),
    )

    return (
        value(
            best_x,
            best_y,
        ),
        best_x,
        best_y,
    )


def minimized_a_sq(
    H,
    F,
    h_lock,
    lambda_a,
):
    """Analytically minimize homogeneous KLS potential over A^2."""

    return max(
        0.0,
        F
        *
        F

        +

        4.0
        *
        h_lock
        *
        (
            H
            -
            1.0
        )
        /
        lambda_a,
    )


def reduced_homogeneous_potential(
    H,
    F,
    h_lock,
    lambda_a,
    p,
):
    """Return exact carrier/A-minimized homogeneous potential at H."""

    a_sq = minimized_a_sq(
        H,
        F,
        h_lock,
        lambda_a,
    )

    (
        carrier_v,
        phi_sq,
        sigma_sq,
    ) = carrier_minimum(
        H,
        p,
    )

    c_h = (
        h_lock
        *
        F
        *
        F
    )

    c_a = (
        2.0
        *
        h_lock
    )

    constant = (
        2.0
        *
        h_lock
        *
        F
        *
        F
    )

    v_h = (
        LAMBDA_H
        /
        8.0
        *
        (
            H
            *
            H
            -
            1.0
        ) ** 2
    )

    v_a = (
        lambda_a
        /
        4.0
        *
        (
            a_sq
            -
            F
            *
            F
        ) ** 2

        -

        2.0
        *
        h_lock
        *
        H
        *
        a_sq

        +

        c_h
        *
        (
            H
            *
            H
            -
            1.0
        )

        +

        c_a
        *
        (
            a_sq
            -
            F
            *
            F
        )

        +

        constant
    )

    return (
        float(
            v_h
            +
            carrier_v
            +
            v_a
        ),
        a_sq,
        phi_sq,
        sigma_sq,
    )


def homogeneous_global_minimum(
    F,
    h_lock,
    lambda_a,
    p,
):
    """Dense plus local one-dimensional global-vacuum reconstruction."""

    grid = np.linspace(
        0.0,
        2.5,
        2501,
    )

    values = np.array(
        [
            reduced_homogeneous_potential(
                H,
                F,
                h_lock,
                lambda_a,
                p,
            )[
                0
            ]
            for H
            in grid
        ],
        dtype=float,
    )

    candidate_indices = np.argsort(
        values
    )[
        :8
    ]

    best_v = float(
        values[
            candidate_indices[
                0
            ]
        ]
    )

    best_h = float(
        grid[
            candidate_indices[
                0
            ]
        ]
    )

    for index in candidate_indices:

        lo = float(
            grid[
                max(
                    0,
                    int(
                        index
                    )
                    -
                    2,
                )
            ]
        )

        hi = float(
            grid[
                min(
                    grid.size
                    -
                    1,
                    int(
                        index
                    )
                    +
                    2,
                )
            ]
        )

        if hi <= lo:
            continue

        result = minimize_scalar(
            lambda H:
                reduced_homogeneous_potential(
                    H,
                    F,
                    h_lock,
                    lambda_a,
                    p,
                )[
                    0
                ],
            bounds=(
                lo,
                hi,
            ),
            method="bounded",
            options={
                "xatol":
                    1.0e-13,
            },
        )

        if (
            result.success
            and
            float(
                result.fun
            )
            <
            best_v
        ):
            best_v = float(
                result.fun
            )
            best_h = float(
                result.x
            )

    exact_target = (
        reduced_homogeneous_potential(
            1.0,
            F,
            h_lock,
            lambda_a,
            p,
        )
    )

    if (
        exact_target[
            0
        ]
        <=
        best_v
        +
        5.0e-14
    ):
        best_v = float(
            exact_target[
                0
            ]
        )
        best_h = 1.0

    (
        value,
        a_sq,
        phi_sq,
        sigma_sq,
    ) = reduced_homogeneous_potential(
        best_h,
        F,
        h_lock,
        lambda_a,
        p,
    )

    return {
        "v":
            float(
                value
            ),

        "H":
            float(
                best_h
            ),

        "A":
            math.sqrt(
                max(
                    a_sq,
                    0.0,
                )
            ),

        "Phi":
            math.sqrt(
                max(
                    phi_sq,
                    0.0,
                )
            ),

        "Sigma":
            math.sqrt(
                max(
                    sigma_sq,
                    0.0,
                )
            ),
    }


def vacuum_hessian_minimum(
    F,
    h_lock,
    lambda_a,
    p,
):
    """Return smallest amplitude Hessian eigenvalue at target vacuum."""

    h_a_block = np.array(
        [
            [
                LAMBDA_H
                +
                2.0
                *
                h_lock
                *
                F
                *
                F,

                -4.0
                *
                h_lock
                *
                F,
            ],
            [
                -4.0
                *
                h_lock
                *
                F,

                2.0
                *
                lambda_a
                *
                F
                *
                F,
            ],
        ],
        dtype=float,
    )

    eigenvalues = list(
        np.linalg.eigvalsh(
            h_a_block
        )
    )

    eigenvalues.extend(
        [
            p[
                "m_phi_sq"
            ],
            p[
                "m_sigma_sq"
            ],
        ]
    )

    return float(
        min(
            eigenvalues
        )
    )


def evaluate_vacuum_point(
    F,
    h_lock,
    lambda_a,
    p,
):
    """Evaluate one complete homogeneous-vacuum point."""

    result = (
        homogeneous_global_minimum(
            F,
            h_lock,
            lambda_a,
            p,
        )
    )

    hessian_min = (
        vacuum_hessian_minimum(
            F,
            h_lock,
            lambda_a,
            p,
        )
    )

    distance = math.sqrt(
        (
            result[
                "H"
            ]
            -
            1.0
        ) ** 2

        +

        (
            result[
                "A"
            ]
            -
            F
        ) ** 2

        +

        result[
            "Phi"
        ] ** 2

        +

        result[
            "Sigma"
        ] ** 2
    )

    passed = (
        result[
            "v"
        ]
        >=
        -VACUUM_TOL

        and
        distance
        <=
        VACUUM_LOCATION_TOL

        and
        hessian_min
        >=
        MIN_HESSIAN
    )

    return {
        **result,

        "hessian_min":
            hessian_min,

        "distance":
            distance,

        "passed":
            passed,
    }


def wall_potential(
    H,
    A,
    F,
    h_lock,
    lambda_a,
):
    """Return H-A potential on zero-carrier planar-wall branch."""

    c_h = (
        h_lock
        *
        F
        *
        F
    )

    c_a = (
        2.0
        *
        h_lock
    )

    constant = (
        2.0
        *
        h_lock
        *
        F
        *
        F
    )

    return (
        LAMBDA_H
        /
        8.0
        *
        (
            H
            *
            H
            -
            1.0
        ) ** 2

        +

        lambda_a
        /
        4.0
        *
        (
            A
            *
            A
            -
            F
            *
            F
        ) ** 2

        -

        2.0
        *
        h_lock
        *
        H
        *
        A
        *
        A

        +

        c_h
        *
        (
            H
            *
            H
            -
            1.0
        )

        +

        c_a
        *
        (
            A
            *
            A
            -
            F
            *
            F
        )

        +

        constant
    )


def solve_wall(
    F,
    h_lock,
    lambda_a,
    p,
    *,
    extent=8.0,
    tol=3.0e-7,
):
    """Solve symmetric half-wall BVP and reconstruct physical diagnostics."""

    k_trial = (
        F
        *
        math.sqrt(
            lambda_a
        )
        /
        2.0
    )

    half_domain = (
        extent
        /
        k_trial
    )

    z = np.linspace(
        0.0,
        half_domain,
        360,
    )

    c_h = (
        h_lock
        *
        F
        *
        F
    )

    c_a = (
        2.0
        *
        h_lock
    )

    def ode(
        _z,
        y,
    ):
        H, Hp, A, Ap = y

        Hpp = (
            0.5
            *
            LAMBDA_H
            *
            H
            *
            (
                H
                *
                H
                -
                1.0
            )

            -

            2.0
            *
            h_lock
            *
            A
            *
            A

            +

            2.0
            *
            c_h
            *
            H
        )

        # A has |dA|^2 normalization:
        # 2 A'' = dV/dA.
        App = (
            0.5
            *
            lambda_a
            *
            A
            *
            (
                A
                *
                A
                -
                F
                *
                F
            )

            -

            2.0
            *
            h_lock
            *
            H
            *
            A

            +

            c_a
            *
            A
        )

        return np.vstack(
            (
                Hp,
                Hpp,
                Ap,
                App,
            )
        )

    def bc(
        ya,
        yb,
    ):
        return np.array(
            [
                ya[
                    1
                ],
                ya[
                    2
                ],
                yb[
                    0
                ]
                -
                1.0,
                yb[
                    2
                ]
                -
                F,
            ],
            dtype=float,
        )

    A0 = (
        F
        *
        np.tanh(
            k_trial
            *
            z
        )
    )

    y0 = np.vstack(
        (
            np.ones_like(
                z
            ),

            np.zeros_like(
                z
            ),

            A0,

            F
            *
            k_trial
            /
            np.cosh(
                k_trial
                *
                z
            ) ** 2,
        )
    )

    solution = solve_bvp(
        ode,
        bc,
        z,
        y0,
        tol=tol,
        max_nodes=20000,
    )

    if solution.status != 0:
        return {
            "passed":
                False,

            "status":
                float(
                    solution.status
                ),
        }

    dense_z = np.linspace(
        0.0,
        half_domain,
        6001,
    )

    H, Hp, A, Ap = (
        solution.sol(
            dense_z
        )
    )

    potential = wall_potential(
        H,
        A,
        F,
        h_lock,
        lambda_a,
    )

    kinetic = (
        0.5
        *
        Hp
        *
        Hp

        +

        Ap
        *
        Ap
    )

    tension = (
        2.0
        *
        float(
            simpson(
                kinetic
                +
                potential,
                x=dense_z,
            )
        )
    )

    virial = (
        2.0
        *
        float(
            simpson(
                kinetic
                -
                potential,
                x=dense_z,
            )
        )
    )

    active = (
        2.0
        *
        float(
            simpson(
                -2.0
                *
                potential,
                x=dense_z,
            )
        )
    )

    virial_rel = (
        abs(
            virial
        )
        /
        max(
            abs(
                tension
            ),
            1.0e-30,
        )
    )

    active_relerr = (
        abs(
            active
            +
            tension
        )
        /
        max(
            abs(
                tension
            ),
            1.0e-30,
        )
    )

    min_phi_mass_sq = float(
        np.min(
            p[
                "m_phi_sq"
            ]
            +
            p[
                "f_phi"
            ]
            *
            (
                H
                *
                H
                -
                1.0
            )
        )
    )

    min_sigma_mass_sq = float(
        np.min(
            p[
                "m_sigma_sq"
            ]
            +
            p[
                "f_sigma"
            ]
            *
            (
                H
                *
                H
                -
                1.0
            )
        )
    )

    try:
        z90 = brentq(
            lambda zz:
                float(
                    solution.sol(
                        zz
                    )[
                        2
                    ]
                    -
                    0.9
                    *
                    F
                ),
            0.0,
            half_domain,
        )

        width90 = (
            2.0
            *
            z90
        )

    except ValueError:
        width90 = math.inf

    max_rms = float(
        np.max(
            solution.rms_residuals
        )
    )

    passed = (
        tension > 0.0

        and
        virial_rel
        <=
        VIRIAL_REL_TOL

        and
        active_relerr
        <=
        ACTIVE_IDENTITY_REL_TOL

        and
        min_phi_mass_sq > 0.0

        and
        min_sigma_mass_sq > 0.0

        and
        max_rms
        <=
        BVP_RESIDUAL_TOL

        and
        math.isfinite(
            width90
        )
    )

    return {
        "passed":
            passed,

        "tension":
            tension,

        "virial":
            virial,

        "virial_rel":
            virial_rel,

        "active":
            active,

        "active_relerr":
            active_relerr,

        "min_H":
            float(
                np.min(
                    H
                )
            ),

        "min_phi_mass_sq":
            min_phi_mass_sq,

        "min_sigma_mass_sq":
            min_sigma_mass_sq,

        "width90":
            width90,

        "trial_length":
            1.0
            /
            k_trial,

        "max_rms":
            max_rms,

        "status":
            float(
                solution.status
            ),
    }


def main():
    """Execute topology, vacuum, and planar-wall bridge."""

    print(
        "=== 018B-0F0 — LILLEY/KLS SAME-GAUGE "
        "NORMALIZATION + WALL BRIDGE ==="
    )

    if not D_LOG.exists():
        raise RuntimeError(
            f"Missing required 018B-0D log: {D_LOG}"
        )

    p = reconstruct_parameters()

    print(
        "\n=== PUBLISHED TWO-CURRENT PARAMETER RECONSTRUCTION ==="
    )

    for key in (
        "alpha_phi",
        "alpha_sigma",
        "beta_phi",
        "beta_sigma",
        "gamma_phi",
        "gamma_sigma",
        "qtilde_sq",
        "g",
        "lambda_phi",
        "lambda_sigma",
        "m_phi_sq",
        "m_sigma_sq",
        "f_phi",
        "f_sigma",
    ):
        print(
            f"{key.upper()}="
            f"{p[key]:.15e}"
        )

    quartic_margin = (
        p[
            "lambda_phi"
        ]
        *
        p[
            "lambda_sigma"
        ]

        -

        p[
            "g"
        ] ** 2
    )

    parameter_pass = (
        p[
            "beta_phi"
        ]
        >
        p[
            "gamma_phi"
        ]

        and

        p[
            "beta_sigma"
        ]
        >
        p[
            "gamma_sigma"
        ]

        and

        quartic_margin > 0.0

        and

        p[
            "qtilde_sq"
        ]
        >
        0.0
    )

    print(
        "CARRIER_QUARTIC_POSITIVE_DEFINITE_MARGIN="
        f"{quartic_margin:+.15e}"
    )

    print(
        "PUBLISHED_TWO_CURRENT_PARAMETER_HEALTH="
        f"{'PASS' if parameter_pass else 'FAIL'}"
    )

    print(
        "\n=== SAME-GAUGE CHARGE / TOPOLOGY BRIDGE ==="
    )

    g_x = (
        p[
            "qtilde"
        ]
        /
        Q_H
    )

    effective_h_coupling = (
        Q_H
        *
        g_x
    )

    local_match_relerr = (
        abs(
            effective_h_coupling
            -
            p[
                "qtilde"
            ]
        )
        /
        p[
            "qtilde"
        ]
    )

    reduced_flux = (
        1.0
        /
        Q_H
    )

    a_required_winding = (
        Q_A
        *
        reduced_flux
    )

    wilson_phase = (
        2.0
        *
        math.pi
        *
        a_required_winding
    )

    branch_jump = (
        wilson_phase
        %
        (
            2.0
            *
            math.pi
        )
    )

    topology_pass = (
        local_match_relerr
        <
        1.0e-15

        and

        math.isclose(
            a_required_winding,
            0.5,
            rel_tol=0.0,
            abs_tol=1.0e-15,
        )

        and

        math.isclose(
            branch_jump,
            math.pi,
            rel_tol=0.0,
            abs_tol=1.0e-15,
        )
    )

    print(
        "PUBLISHED_Q_TILDE="
        f"{p['qtilde']:.15e}"
    )

    print(
        "FUNDAMENTAL_GX_TILDE="
        f"{g_x:.15e}"
    )

    print(
        f"Q_H={Q_H}"
    )

    print(
        f"Q_A={Q_A}"
    )

    print(
        "QH_GX_OVER_PUBLISHED_Q="
        f"{effective_h_coupling / p['qtilde']:.15e}"
    )

    print(
        "LOCAL_TWO_CURRENT_STRING_EQUATIONS_PRESERVED="
        f"{'YES' if local_match_relerr < 1e-15 else 'NO'}"
    )

    print(
        "A_REQUIRED_WINDING_AROUND_UNIT_H_STRING="
        f"{a_required_winding:.15e}"
    )

    print(
        "A_WILSON_PHASE="
        f"{wilson_phase:.15e}"
    )

    print(
        "ONE_Z2_BRANCH_WALL_PER_UNIT_STRING="
        f"{'YES' if topology_pass else 'NO'}"
    )

    print(
        "SAME_GAUGE_TOPOLOGY_BRIDGE="
        f"{'PASS' if topology_pass else 'FAIL'}"
    )

    print(
        "\n=== HOMOGENEOUS VACUUM — SELECTED POINT ==="
    )

    selected_vac = evaluate_vacuum_point(
        F_SELECTED,
        H_LOCK_SELECTED,
        LAMBDA_A_SELECTED,
        p,
    )

    print(
        "SELECTED_VACUUM_ENERGY="
        f"{float(selected_vac['v']):+.15e}"
    )

    print(
        "SELECTED_VACUUM_DISTANCE="
        f"{float(selected_vac['distance']):.15e}"
    )

    print(
        "SELECTED_VACUUM_HESSIAN_MIN="
        f"{float(selected_vac['hessian_min']):+.15e}"
    )

    print(
        "SELECTED_VACUUM_H="
        f"{float(selected_vac['H']):.15e}"
    )

    print(
        "SELECTED_VACUUM_A="
        f"{float(selected_vac['A']):.15e}"
    )

    print(
        "SELECTED_VACUUM_PHI="
        f"{float(selected_vac['Phi']):.15e}"
    )

    print(
        "SELECTED_VACUUM_SIGMA="
        f"{float(selected_vac['Sigma']):.15e}"
    )

    print(
        "SELECTED_FULL_HOMOGENEOUS_VACUUM="
        f"{'PASS' if selected_vac['passed'] else 'FAIL'}"
    )

    print(
        "\n=== BROAD MODEL-SELECTION VACUUM SCAN ==="
    )

    coarse_total = 0
    coarse_pass = 0
    coarse_min_hessian = math.inf
    coarse_min_energy = math.inf
    coarse_max_distance = 0.0

    for (
        F,
        h_lock,
        lambda_a,
    ) in itertools.product(
        F_SCAN,
        H_SCAN,
        LAMBDA_A_SCAN,
    ):
        result = evaluate_vacuum_point(
            F,
            h_lock,
            lambda_a,
            p,
        )

        coarse_total += 1
        coarse_pass += int(
            bool(
                result[
                    "passed"
                ]
            )
        )

        coarse_min_hessian = min(
            coarse_min_hessian,
            float(
                result[
                    "hessian_min"
                ]
            ),
        )

        coarse_min_energy = min(
            coarse_min_energy,
            float(
                result[
                    "v"
                ]
            ),
        )

        coarse_max_distance = max(
            coarse_max_distance,
            float(
                result[
                    "distance"
                ]
            ),
        )

    print(
        "BROAD_VACUUM_SCAN_PASS="
        f"{coarse_pass}/{coarse_total}"
    )

    print(
        "BROAD_VACUUM_SCAN_MIN_HESSIAN="
        f"{coarse_min_hessian:+.15e}"
    )

    print(
        "BROAD_VACUUM_SCAN_MIN_ENERGY="
        f"{coarse_min_energy:+.15e}"
    )

    print(
        "BROAD_VACUUM_SCAN_MAX_TARGET_DISTANCE="
        f"{coarse_max_distance:.15e}"
    )

    print(
        "\n=== LOCAL +/-10 PERCENT 5^3 VACUUM ROBUSTNESS ==="
    )

    robust_total = 0
    robust_pass = 0
    robust_min_hessian = math.inf

    for (
        f_factor,
        h_factor,
        l_factor,
    ) in itertools.product(
        ROBUST_LEVELS,
        repeat=3,
    ):

        result = evaluate_vacuum_point(
            F_SELECTED
            *
            f_factor,

            H_LOCK_SELECTED
            *
            h_factor,

            LAMBDA_A_SELECTED
            *
            l_factor,

            p,
        )

        robust_total += 1

        robust_pass += int(
            bool(
                result[
                    "passed"
                ]
            )
        )

        robust_min_hessian = min(
            robust_min_hessian,
            float(
                result[
                    "hessian_min"
                ]
            ),
        )

    print(
        "LOCAL_VACUUM_ROBUSTNESS_PASS="
        f"{robust_pass}/{robust_total}"
    )

    print(
        "LOCAL_VACUUM_ROBUSTNESS_MIN_HESSIAN="
        f"{robust_min_hessian:+.15e}"
    )

    print(
        "\n=== BLIND WILDCARD LAMBDA_A DIAGNOSTIC "
        "— NOT PROMOTION EVIDENCE ==="
    )

    wildcard_pass = 0

    for value in WILDCARD_LAMBDA_A:

        result = evaluate_vacuum_point(
            F_SELECTED,
            H_LOCK_SELECTED,
            value,
            p,
        )

        wildcard_pass += int(
            bool(
                result[
                    "passed"
                ]
            )
        )

        print(
            f"WILDCARD_LAMBDA_A={value:.6f} "
            f"PASS={'YES' if result['passed'] else 'NO'} "
            f"HESSIAN_MIN="
            f"{float(result['hessian_min']):+.9e}"
        )

    print(
        "WILDCARD_VACUUM_PASS="
        f"{wildcard_pass}/"
        f"{len(WILDCARD_LAMBDA_A)}"
    )

    print(
        "\n=== SELECTED PLANAR WALL DOMAIN CONVERGENCE ==="
    )

    domain_results = {}

    for extent in (
        6.0,
        8.0,
        10.0,
    ):

        result = solve_wall(
            F_SELECTED,
            H_LOCK_SELECTED,
            LAMBDA_A_SELECTED,
            p,
            extent=extent,
        )

        domain_results[
            extent
        ] = result

        print(
            f"WALL_EXTENT={extent:.1f} "
            f"PASS="
            f"{'YES' if result.get('passed', False) else 'NO'} "
            f"SIGMA="
            f"{float(result.get('tension', math.nan)):.15e} "
            f"VIRIAL_REL="
            f"{float(result.get('virial_rel', math.inf)):.3e} "
            f"ACTIVE_RELERR="
            f"{float(result.get('active_relerr', math.inf)):.3e} "
            f"MAX_RMS="
            f"{float(result.get('max_rms', math.inf)):.3e}"
        )

    wall8 = domain_results[
        8.0
    ]

    wall10 = domain_results[
        10.0
    ]

    if (
        wall8.get(
            "passed",
            False,
        )
        and
        wall10.get(
            "passed",
            False,
        )
    ):

        wall_domain_rel = (
            abs(
                float(
                    wall10[
                        "tension"
                    ]
                )
                -
                float(
                    wall8[
                        "tension"
                    ]
                )
            )
            /
            float(
                wall10[
                    "tension"
                ]
            )
        )

    else:
        wall_domain_rel = (
            math.inf
        )

    selected_wall_pass = (
        all(
            bool(
                domain_results[
                    extent
                ].get(
                    "passed",
                    False,
                )
            )
            for extent
            in (
                6.0,
                8.0,
                10.0,
            )
        )

        and

        wall_domain_rel
        <
        2.0e-5
    )

    print(
        "WALL_8_TO_10_TENSION_REL_CHANGE="
        f"{wall_domain_rel:.15e}"
    )

    print(
        "PLANAR_WALL_DOMAIN_CONVERGENCE="
        f"{'PASS' if selected_wall_pass else 'FAIL'}"
    )

    print(
        "\n=== PLANAR WALL +/-10 PERCENT "
        "3^3 CORNER ROBUSTNESS ==="
    )

    wall_total = 0
    wall_pass = 0

    min_phi_mass_sq = (
        math.inf
    )

    min_sigma_mass_sq = (
        math.inf
    )

    min_tension = (
        math.inf
    )

    max_virial_rel = (
        0.0
    )

    max_active_relerr = (
        0.0
    )

    max_width90 = (
        0.0
    )

    for (
        f_factor,
        h_factor,
        l_factor,
    ) in itertools.product(
        WALL_CORNER_LEVELS,
        repeat=3,
    ):

        result = solve_wall(
            F_SELECTED
            *
            f_factor,

            H_LOCK_SELECTED
            *
            h_factor,

            LAMBDA_A_SELECTED
            *
            l_factor,

            p,
            extent=8.0,
            tol=8.0e-7,
        )

        wall_total += 1

        wall_pass += int(
            bool(
                result.get(
                    "passed",
                    False,
                )
            )
        )

        if result.get(
            "passed",
            False,
        ):

            min_phi_mass_sq = min(
                min_phi_mass_sq,
                float(
                    result[
                        "min_phi_mass_sq"
                    ]
                ),
            )

            min_sigma_mass_sq = min(
                min_sigma_mass_sq,
                float(
                    result[
                        "min_sigma_mass_sq"
                    ]
                ),
            )

            min_tension = min(
                min_tension,
                float(
                    result[
                        "tension"
                    ]
                ),
            )

            max_virial_rel = max(
                max_virial_rel,
                float(
                    result[
                        "virial_rel"
                    ]
                ),
            )

            max_active_relerr = max(
                max_active_relerr,
                float(
                    result[
                        "active_relerr"
                    ]
                ),
            )

            max_width90 = max(
                max_width90,
                float(
                    result[
                        "width90"
                    ]
                ),
            )

    print(
        "WALL_CORNER_ROBUSTNESS_PASS="
        f"{wall_pass}/{wall_total}"
    )

    print(
        "WALL_CORNER_MIN_PHI_MASS_SQ="
        f"{min_phi_mass_sq:+.15e}"
    )

    print(
        "WALL_CORNER_MIN_SIGMA_MASS_SQ="
        f"{min_sigma_mass_sq:+.15e}"
    )

    print(
        "WALL_CORNER_MIN_TENSION="
        f"{min_tension:.15e}"
    )

    print(
        "WALL_CORNER_MAX_VIRIAL_REL="
        f"{max_virial_rel:.15e}"
    )

    print(
        "WALL_CORNER_MAX_ACTIVE_IDENTITY_RELERR="
        f"{max_active_relerr:.15e}"
    )

    print(
        "WALL_CORNER_MAX_WIDTH90="
        f"{max_width90:.15e}"
    )

    selected = (
        wall10
    )

    sigma_wall = float(
        selected[
            "tension"
        ]
    )

    width90 = float(
        selected[
            "width90"
        ]
    )

    min_radius_10x = (
        MIN_SCALE_SEPARATION
        *
        width90
    )

    min_load_10x = (
        sigma_wall
        *
        min_radius_10x
    )

    gauge_core_inverse_mass = (
        1.0
        /
        p[
            "qtilde"
        ]
    )

    print(
        "\n=== NEW EMBEDDED WALL OUTPUTS ==="
    )

    print(
        "NEW_WALL_TENSION="
        f"{sigma_wall:.15e}"
    )

    print(
        "NEW_WALL_ACTIVE_SOURCE="
        f"{float(selected['active']):+.15e}"
    )

    print(
        "NEW_WALL_WIDTH90="
        f"{width90:.15e}"
    )

    print(
        "NEW_WALL_TRIAL_LENGTH="
        f"{float(selected['trial_length']):.15e}"
    )

    print(
        "NEW_STRING_GAUGE_CORE_INVERSE_MASS_PROXY="
        f"{gauge_core_inverse_mass:.15e}"
    )

    print(
        "NEW_WALL_MIN_PHI_FLUCTUATION_MASS_SQ="
        f"{float(selected['min_phi_mass_sq']):+.15e}"
    )

    print(
        "NEW_WALL_MIN_SIGMA_FLUCTUATION_MASS_SQ="
        f"{float(selected['min_sigma_mass_sq']):+.15e}"
    )

    print(
        "MIN_RADIUS_FOR_10X_WALL90="
        f"{min_radius_10x:.15e}"
    )

    print(
        "MIN_POSITIVE_RIM_COMPRESSION_FOR_10X_WALL90="
        f"{min_load_10x:.15e}"
    )

    if A8_LOG.exists():

        old_sigma = read_scalar(
            A8_LOG,
            "WALL_TENSION=",
        )

        rel = (
            abs(
                sigma_wall
                -
                old_sigma
            )
            /
            old_sigma
        )

        print(
            "OLD_018A8_WALL_TENSION_DIAGNOSTIC="
            f"{old_sigma:.15e}"
        )

        print(
            "NEW_VS_OLD_WALL_TENSION_REL_DIFFERENCE="
            f"{rel:.15e}"
        )

    else:

        print(
            "OLD_018A8_WALL_TENSION_DIAGNOSTIC="
            "LOG_NOT_PRESENT"
        )

    print(
        "OLD_018A_JUNCTION_ENERGY_REUSE="
        "PROHIBITED"
    )

    print(
        "OLD_018A_JUNCTION_ACTIVE_STRESS_REUSE="
        "PROHIBITED"
    )

    print(
        "NEW_TWO_CURRENT_2D_JUNCTION_STATUS="
        "NOT_YET_REDERIVED"
    )

    broad_pass = (
        coarse_pass
        ==
        coarse_total
    )

    robust_vac_pass = (
        robust_pass
        ==
        robust_total
    )

    robust_wall_pass = (
        wall_pass
        ==
        wall_total
    )

    green = (
        parameter_pass

        and
        topology_pass

        and
        bool(
            selected_vac[
                "passed"
            ]
        )

        and
        broad_pass

        and
        robust_vac_pass

        and
        selected_wall_pass

        and
        robust_wall_pass
    )

    print(
        "\n=== DECISION ==="
    )

    if green:

        print(
            "018B0F0_LILLEY_KLS_NORMALIZATION_WALL_BRIDGE="
            "GREEN"
        )

        print(
            "TWO_CURRENT_STRING_PLUS_KLS_WALL_COMMON_GAUGE_MODEL="
            "SUPPORTED_AT_PREFLIGHT_LEVEL"
        )

        print(
            "HOMOGENEOUS_VACUUM_ROBUST=YES"
        )

        print(
            "PLANAR_MICROSCOPIC_WALL_ROBUST=YES"
        )

        print(
            "CURRENT_CARRIERS_TACHYONIC_ON_PLANAR_WALL=NO"
        )

        print(
            "NEXT="
            "018B0F_STATIONARY_INTEGER_WALL_BALANCE_"
            "AND_GRAVITY_SCOUT_WITH_NEW_WALL"
        )

        print(
            "NEXT_AFTER_POSITIVE_SCOUT="
            "018B0G_NEW_TWO_CURRENT_2D_JUNCTION_REVALIDATION"
        )

    else:

        print(
            "018B0F0_LILLEY_KLS_NORMALIZATION_WALL_BRIDGE="
            "RED"
        )

        print(
            "TWO_CURRENT_STRING_PLUS_KLS_WALL_COMMON_GAUGE_MODEL="
            "NOT_PROMOTED"
        )

        print(
            "NEXT="
            "CLASSIFY_BRIDGE_FAILURE_BEFORE_ANY_STATIONARY_SEARCH"
        )

    print(
        "CURRENT_HEURISTIC="
        "APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY"
    )

    print(
        "HEURISTIC_INCREASE_FROM_THIS_GATE="
        "NO_MICROSCOPIC_BRIDGE_ONLY"
    )

    print(
        "TRUE_018B_GLOBAL_FIELD_SOLUTION="
        "NOT_YET_RUN"
    )

    print(
        "FULL_COMPOSITE_STABILITY="
        "NOT_ESTABLISHED"
    )

    print(
        "NONLINEAR_EINSTEIN_MATTER="
        "NOT_ESTABLISHED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018B0F0_LILLEY_KLS_"
        "SAME_GAUGE_NORMALIZATION_WALL_BRIDGE"
    )


if __name__ == "__main__":
    main()
