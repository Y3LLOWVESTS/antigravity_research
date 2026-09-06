"""031D3C-R3 — weighted variational l=1 translation closeout.

PURPOSE
-------
Close the one unresolved 031D3 coupled-linear stability diagnostic left by
031D3C-R2. R2's direct Chebyshev dense spectra were favorable, but its final
translation-projected stiffness used an ordinary Euclidean projection of a
Chebyshev collocation matrix. That matrix had not been shown to represent the
self-adjoint physical second variation in the corresponding inner product.

SCIENTIFIC QUESTION
-------------------
After removing only the exact common spatial translation Goldstone mode, is
the true l=1 quadratic second variation of the activated X + phi + Y field
positive, negative, or numerically unresolved?

PHYSICAL QUADRATIC VARIABLES
----------------------------
Use the same canonical reduced radial perturbations as 031D3C/R2:

    q1 = r * delta y                         X amplitude
    q2 = r * y * delta theta_X               X phase
    q3 = r * delta u / chi                   scalar
    q4 = r * sqrt(rho_Y) * delta a           Y amplitude
    q5 = r * sqrt(rho_Y) * a * delta theta_Y Y phase

For these canonical reduced fields the kinetic norm is

    <q,q> = integral_0^R dr sum_i |q_i|^2.

Hence the correct radial mass/inner-product matrix is the Clenshaw-Curtis
quadrature matrix M, not the identity matrix on nonuniform collocation nodes.

The continuous fixed-frequency second variation in l=1 is

    delta^2 R = integral dr [
        sum_i |q_i'|^2
        + l(l+1)/r^2 sum_i |q_i|^2
        + q^T V(r) q
    ],

where R = E - omega_X Q_X - omega_Y Q_Y is the constrained Routhian and V is
exactly the local canonical Hessian already used by 031D3C/R2.

Because the background is spherical, every l=1 perturbation is tangent to both
fixed-charge manifolds at first order: the angular integral of Y_1m vanishes.
No additional charge projection is therefore applied in this l=1 gate.

NUMERICAL METHOD
----------------
1. Reconstruct the same promoted D3 background used by R2.
2. Use Chebyshev-Lobatto nodes on [0,R].
3. Build Clenshaw-Curtis quadrature weights.
4. Build the derivative part from the integrated weak/variational form

       H_grad = B^T W B,

   where B differentiates an interior Dirichlet vector on the full Lobatto
   grid. This is symmetric by construction.
5. Add angular, local-Hessian and cross-coupling terms under the same weights.
6. Solve the generalized self-adjoint problem

       H v = lambda M v.

7. Transform to canonical Euclidean coordinates z=M^(1/2)v and remove only
   the common analytic translation with the physically correct weighted
   projector.
8. Leave relative source-versus-activation translation fully physical.
9. Repeat over grid and domain ladders.

VALIDATION
----------
The run independently checks:
- Clenshaw-Curtis integral of 1;
- free l=0 Dirichlet eigenvalue pi^2;
- free l=1 radial eigenvalue j_1,1^2;
- H symmetry to numerical precision;
- weighted self-adjointness after M^(1/2) transformation;
- the old raw collocation operator's weighted asymmetry, as a diagnostic only;
- common-translation Rayleigh quotient and residual;
- next translation-projected eigenvalue convergence;
- relative-translation Rayleigh quotient and overlap with the lowest physical
  projected mode.

PROMOTION / FALSIFICATION
-------------------------
GREEN requires a positive next weighted eigenvalue that is converged in grid
and domain and separated from the numerical Goldstone splitting by a declared
margin. A robust negative next eigenvalue fails the physical variational
stability gate. A value comparable to the Goldstone/discretization floor is
YELLOW and must not be promoted.

A negative variational direction is sufficient to fail this stability gate,
but this run does not by itself claim an exponentially growing time-domain
mode if the gyroscopic system were to require a separate dynamical proof.

CLAIM LIMITS
------------
Even GREEN establishes only coupled-linear energetic stability of the l=1
sector in the declared flat-space effective X/phi/Y theory, combined with the
already favorable direct spectra and inherited l=0..8 results. It does not
establish nonlinear fragmentation stability, a Q_Y reservoir, switching
radiation, Einstein backreaction, radiative naturalness, empirical viability,
or a practical antigravity device.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from scipy.linalg import eigh


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

QBALL_SOURCE = SIM / "031b2a_global_qball_activated_scalar_control.py"
D3A_SOURCE = SIM / "031d3a_u1_metric_activation_capacity.py"

D3B_SUMMARY = DATA / "031d3b_full_coupled_activation_summary.json"
D3C_SUMMARY = DATA / "031d3c_activation_stability_switching_summary.json"
D3CR_SUMMARY = DATA / "031d3cr_surgical_closeout_summary.json"
D3CR2_SUMMARY = DATA / "031d3cr2_chebyshev_dense_summary.json"
D3AR_SUMMARY = DATA / "031d3ar_metric_eft_payload_summary.json"
ROBUST_SUMMARY = DATA / "031c96_operating_margin_robustness_summary.json"

OUT_JSON = DATA / "031d3cr3_weighted_variational_l1_summary.json"
OUT_CSV = DATA / "031d3cr3_weighted_variational_l1_scan.csv"

ELL = 1
X_MATCH = 500.0
X0 = 1.0e-5

MAIN_RMAX = 600.0
MAIN_N_VALUES = (112, 144, 176, 208)
DOMAIN_CASES = ((224, 800.0),)

FREE_TEST_N = 80
QUAD_REL_TOL = 2.0e-13
FREE_L0_REL_TOL = 2.0e-8
FREE_L1_REL_TOL = 2.0e-8
H_SYM_REL_TOL = 2.0e-13
A_SYM_REL_TOL = 2.0e-13

# Promotion is deliberately relative to the measured Goldstone splitting.
GOLDSTONE_MARGIN_FACTOR = 20.0
MIN_ABS_POSITIVE_LAMBDA = 1.0e-10
GRID_REL_SPREAD_MAX = 0.08
DOMAIN_REL_DIFF_MAX = 0.10
TRANSLATION_RESIDUAL_MAX = 2.0e-3

# If a robust negative direction is found, fail the variational stability gate.
NEGATIVE_MARGIN_FACTOR = 20.0


def require(path: Path) -> None:
    """Require one upstream source or result artifact."""

    if not path.is_file():
        raise RuntimeError(
            f"Missing required upstream file: {path}"
        )


def load_module(name: str, path: Path):
    """Import one repository simulation without invoking its main function."""

    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"Cannot import {path}"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[
        name
    ] = module

    spec.loader.exec_module(
        module
    )

    return module


def builtin(value: Any):
    """Convert NumPy values recursively into JSON-compatible values."""

    if isinstance(
        value,
        np.generic,
    ):
        return value.item()

    if isinstance(
        value,
        np.ndarray,
    ):
        return value.tolist()

    if isinstance(
        value,
        dict,
    ):
        return {
            str(k):
            builtin(v)
            for k, v
            in value.items()
        }

    if isinstance(
        value,
        (
            list,
            tuple,
        ),
    ):
        return [
            builtin(v)
            for v
            in value
        ]

    return value


def W(q):
    """Logarithmic Q-ball potential function."""

    q = np.asarray(
        q,
        dtype=float,
    )

    return 0.5 * np.log1p(
        q**2
    )


def activation_fraction(a):
    """Return f(a)=1-exp(-a^2/2)."""

    a = np.asarray(
        a,
        dtype=float,
    )

    return (
        1.0
        -
        np.exp(
            -0.5
            * a**2
        )
    )


def activation_fp(a):
    """Return f'(a)."""

    a = np.asarray(
        a,
        dtype=float,
    )

    return (
        a
        *
        np.exp(
            -0.5
            * a**2
        )
    )


def activation_fpp(a):
    """Return f''(a)."""

    a = np.asarray(
        a,
        dtype=float,
    )

    return (
        1.0
        -
        a**2
    ) * np.exp(
        -0.5
        * a**2
    )


def clenshaw_curtis_weights(
    N: int,
) -> np.ndarray:
    """Return weights for integral_-1^1 f(x) dx on Lobatto nodes."""

    if N < 2:
        raise ValueError(
            "N must be >= 2"
        )

    theta = (
        math.pi
        * np.arange(
            N + 1,
            dtype=float,
        )
        / N
    )

    w = np.zeros(
        N + 1,
        dtype=float,
    )

    interior = np.arange(
        1,
        N,
        dtype=int,
    )

    v = np.ones(
        N - 1,
        dtype=float,
    )

    if N % 2 == 0:
        w[
            0
        ] = (
            1.0
            /
            (
                N**2
                -
                1.0
            )
        )

        w[
            -1
        ] = w[
            0
        ]

        for k in range(
            1,
            N // 2,
        ):
            v -= (
                2.0
                *
                np.cos(
                    2.0
                    * k
                    * theta[
                        interior
                    ]
                )
                /
                (
                    4.0
                    * k**2
                    -
                    1.0
                )
            )

        v -= (
            np.cos(
                N
                * theta[
                    interior
                ]
            )
            /
            (
                N**2
                -
                1.0
            )
        )

    else:
        w[
            0
        ] = (
            1.0
            /
            N**2
        )

        w[
            -1
        ] = w[
            0
        ]

        for k in range(
            1,
            (N - 1) // 2 + 1,
        ):
            v -= (
                2.0
                *
                np.cos(
                    2.0
                    * k
                    * theta[
                        interior
                    ]
                )
                /
                (
                    4.0
                    * k**2
                    -
                    1.0
                )
            )

    w[
        interior
    ] = (
        2.0
        * v
        / N
    )

    return w


def chebyshev_variational_grid(
    N: int,
    rmax: float,
) -> dict[str, np.ndarray]:
    """Build Lobatto grid, derivative matrix, and CC weights on [0,R]."""

    j = np.arange(
        N + 1,
        dtype=float,
    )

    x = np.cos(
        math.pi
        * j
        / N
    )

    c = np.ones(
        N + 1,
        dtype=float,
    )

    c[
        0
    ] = 2.0

    c[
        -1
    ] = 2.0

    c *= (
        -1.0
    ) ** np.arange(
        N + 1
    )

    X = np.tile(
        x,
        (
            N + 1,
            1,
        ),
    ).T

    dX = (
        X
        -
        X.T
    )

    D = (
        np.outer(
            c,
            1.0 / c,
        )
        /
        (
            dX
            +
            np.eye(
                N + 1
            )
        )
    )

    D -= np.diag(
        np.sum(
            D,
            axis=1,
        )
    )

    Dr = (
        -2.0
        * D
        / rmax
    )

    D2r = (
        Dr
        @ Dr
    )

    r = (
        0.5
        * rmax
        * (
            1.0
            -
            x
        )
    )

    w = (
        0.5
        * rmax
        * clenshaw_curtis_weights(
            N
        )
    )

    interior = np.arange(
        1,
        N,
        dtype=int,
    )

    return {
        "r_full":
            r,

        "r":
            r[
                interior
            ],

        "w_full":
            w,

        "w":
            w[
                interior
            ],

        "Dr_full":
            Dr,

        "D2_collocation":
            D2r[
                np.ix_(
                    interior,
                    interior,
                )
            ],

        "B":
            Dr[
                :,
                interior,
            ],

        "interior":
            interior,
    }


def relerr(
    a: float,
    b: float,
) -> float:
    """Return symmetric relative difference."""

    return (
        abs(
            a
            -
            b
        )
        /
        max(
            abs(
                a
            ),
            abs(
                b
            ),
            1.0e-300,
        )
    )


def relative_spread(
    values,
) -> float:
    """Return max-min spread relative to mean magnitude."""

    values = np.asarray(
        values,
        dtype=float,
    )

    center = float(
        np.mean(
            values
        )
    )

    return float(
        (
            np.max(
                values
            )
            -
            np.min(
                values
            )
        )
        /
        max(
            abs(
                center
            ),
            1.0e-300,
        )
    )


def validate_variational_discretization() -> dict[str, Any]:
    """Validate the weighted weak-form radial discretization."""

    grid = chebyshev_variational_grid(
        FREE_TEST_N,
        1.0,
    )

    r = grid[
        "r"
    ]

    w = grid[
        "w"
    ]

    B = grid[
        "B"
    ]

    wf = grid[
        "w_full"
    ]

    grad = (
        B.T
        @ (
            wf[
                :,
                None,
            ]
            * B
        )
    )

    mass = np.diag(
        w
    )

    lam0 = float(
        eigh(
            grad,
            mass,
            subset_by_index=(
                0,
                0,
            ),
            eigvals_only=True,
        )[
            0
        ]
    )

    expected0 = (
        math.pi**2
    )

    h1 = (
        grad
        +
        np.diag(
            w
            * 2.0
            / r**2
        )
    )

    lam1 = float(
        eigh(
            h1,
            mass,
            subset_by_index=(
                0,
                0,
            ),
            eigvals_only=True,
        )[
            0
        ]
    )

    j11 = (
        4.4934094579090641753
    )

    expected1 = (
        j11**2
    )

    quad_sum = float(
        np.sum(
            wf
        )
    )

    return {
        "quadrature_sum":
            quad_sum,

        "quadrature_relerr":
            relerr(
                quad_sum,
                1.0,
            ),

        "free_l0_lambda":
            lam0,

        "free_l0_expected":
            expected0,

        "free_l0_relerr":
            relerr(
                lam0,
                expected0,
            ),

        "free_l1_lambda":
            lam1,

        "free_l1_expected":
            expected1,

        "free_l1_relerr":
            relerr(
                lam1,
                expected1,
            ),

        "pass":
            bool(
                relerr(
                    quad_sum,
                    1.0,
                )
                <=
                QUAD_REL_TOL

                and
                relerr(
                    lam0,
                    expected0,
                )
                <=
                FREE_L0_REL_TOL

                and
                relerr(
                    lam1,
                    expected1,
                )
                <=
                FREE_L1_REL_TOL
            ),
    }


def main() -> None:
    """Run the weighted D3 l=1 variational stability closeout."""

    print(
        "=== 031D3C-R3 WEIGHTED VARIATIONAL l=1 CLOSEOUT ===",
        flush=True,
    )

    print(
        "CLAIM_CLASS="
        "WEIGHTED_VARIATIONAL_COUPLED_LINEAR_STABILITY_GATE",
        flush=True,
    )

    print(
        "RAW_EUCLIDEAN_CHEBYSHEV_PROJECTION_USED=NO",
        flush=True,
    )

    print(
        "PHYSICAL_REDUCED_RADIAL_INNER_PRODUCT="
        "INTEGRAL_DR_Q_DAGGER_Q",
        flush=True,
    )

    print(
        "QUADRATURE=CLENSHAW_CURTIS",
        flush=True,
    )

    print(
        "FIXED_Q_L1_TANGENT="
        "YES_BY_Y1M_ANGULAR_ORTHOGONALITY",
        flush=True,
    )

    print(
        "ONLY_EXACT_COMMON_TRANSLATION_PROJECTED=YES",
        flush=True,
    )

    print(
        "RELATIVE_TRANSLATION_PROJECTED=NO",
        flush=True,
    )

    print(
        "PRACTICAL_DEVICE=NO",
        flush=True,
    )

    for path in (
        QBALL_SOURCE,
        D3A_SOURCE,
        D3B_SUMMARY,
        D3C_SUMMARY,
        D3CR_SUMMARY,
        D3CR2_SUMMARY,
        D3AR_SUMMARY,
        ROBUST_SUMMARY,
    ):
        require(
            path
        )

    validation = (
        validate_variational_discretization()
    )

    print(
        "\n=== STAGE A: VARIATIONAL DISCRETIZATION ORACLE ===",
        flush=True,
    )

    for key, value in validation.items():
        print(
            f"{key.upper()}={value}",
            flush=True,
        )

    if not validation[
        "pass"
    ]:
        raise RuntimeError(
            "Variational discretization oracle failed"
        )

    d3b = json.loads(
        D3B_SUMMARY.read_text()
    )

    d3c = json.loads(
        D3C_SUMMARY.read_text()
    )

    d3cr = json.loads(
        D3CR_SUMMARY.read_text()
    )

    d3cr2 = json.loads(
        D3CR2_SUMMARY.read_text()
    )

    d3ar = json.loads(
        D3AR_SUMMARY.read_text()
    )

    robust = json.loads(
        ROBUST_SUMMARY.read_text()
    )

    if not str(
        d3b[
            "classification"
        ]
    ).startswith(
        "GREEN_D3B"
    ):
        raise RuntimeError(
            "D3B is not GREEN"
        )

    if not bool(
        d3c[
            "source_stability"
        ][
            "inherited_green"
        ]
    ):
        raise RuntimeError(
            "Inherited X+phi stability is not GREEN"
        )

    if not bool(
        d3c[
            "activation_branch"
        ][
            "slope_pass"
        ]
    ):
        raise RuntimeError(
            "Activation Q-ball slope gate failed"
        )

    if not bool(
        d3cr[
            "decision"
        ][
            "l1_continuum_pass"
        ]
    ):
        raise RuntimeError(
            "Finite-difference l=1 continuum gate did not pass"
        )

    candidate = robust[
        "candidate"
    ]

    quadrature = robust[
        "quadrature"
    ][
        "high_order_result"
    ]

    primary = d3ar[
        "primary"
    ]

    omega_x = float(
        d3b[
            "domain_rows"
        ][
            -1
        ][
            "omega_x"
        ]
    )

    omega_y = float(
        d3b[
            "domain_rows"
        ][
            -1
        ][
            "omega_y"
        ]
    )

    epsilon = float(
        candidate[
            "epsilon"
        ]
    )

    chi = float(
        candidate[
            "chi"
        ]
    )

    F_gev = float(
        quadrature[
            "F_gev"
        ]
    )

    mu = float(
        primary[
            "mu_mA_over_mX"
        ]
    )

    rho_y = (
        float(
            primary[
                "V_required_eV"
            ]
        )
        /
        (
            F_gev
            * 1.0e9
        )
    )**2

    sqrt_rho = math.sqrt(
        rho_y
    )

    print(
        "\n=== STAGE B: OPERATING PROVENANCE ===",
        flush=True,
    )

    print(
        f"OMEGA_X={omega_x:.15e}",
        flush=True,
    )

    print(
        f"OMEGA_Y={omega_y:.15e}",
        flush=True,
    )

    print(
        f"EPSILON={epsilon:.15e}",
        flush=True,
    )

    print(
        f"CHI={chi:.15e}",
        flush=True,
    )

    print(
        f"MU={mu:.15e}",
        flush=True,
    )

    print(
        f"RHO_Y={rho_y:.15e}",
        flush=True,
    )

    print(
        "R2_CLASSIFICATION="
        f"{d3cr2.get('classification', 'UNKNOWN')}",
        flush=True,
    )

    qmod = load_module(
        "qball031d3cr3",
        QBALL_SOURCE,
    )

    d3a = load_module(
        "d3a031d3cr3",
        D3A_SOURCE,
    )

    old_xmatch = float(
        qmod.X_MATCH
    )

    try:
        print(
            "\n=== STAGE C: BACKGROUND RECONSTRUCTION ===",
            flush=True,
        )

        qmod.X_MATCH = (
            X_MATCH
        )

        source_seed = (
            qmod.solve_uncoupled_qball(
                omega_x
            )
        )

        if source_seed is None:
            raise RuntimeError(
                "Failed X seed"
            )

        source = qmod.solve_coupled(
            source_seed,
            omega_x,
            epsilon,
            chi,
            previous=None,
        )

        if source is None:
            raise RuntimeError(
                "Failed X+phi source"
            )

        boundary = source.sol(
            X_MATCH
        )

        y_boundary = float(
            boundary[
                0
            ]
        )

        u_boundary = float(
            boundary[
                2
            ]
        )

        kx_tail = math.sqrt(
            1.0
            -
            omega_x**2
        )

        def source_fields(r):
            """Evaluate source/scalar fields including declared tails."""

            r = np.asarray(
                r,
                dtype=float,
            )

            y = np.empty_like(
                r
            )

            yp = np.empty_like(
                r
            )

            u = np.empty_like(
                r
            )

            up = np.empty_like(
                r
            )

            inside = (
                r
                <=
                X_MATCH
            )

            if np.any(
                inside
            ):
                state = source.sol(
                    np.maximum(
                        r[
                            inside
                        ],
                        X0,
                    )
                )

                y[
                    inside
                ] = state[
                    0
                ]

                yp[
                    inside
                ] = state[
                    1
                ]

                u[
                    inside
                ] = state[
                    2
                ]

                up[
                    inside
                ] = state[
                    3
                ]

            outside = (
                ~inside
            )

            if np.any(
                outside
            ):
                ro = r[
                    outside
                ]

                yo = (
                    y_boundary
                    * X_MATCH
                    / ro
                    * np.exp(
                        -kx_tail
                        * (
                            ro
                            -
                            X_MATCH
                        )
                    )
                )

                uo = (
                    u_boundary
                    * X_MATCH
                    / ro
                    * np.exp(
                        -epsilon
                        * (
                            ro
                            -
                            X_MATCH
                        )
                    )
                )

                y[
                    outside
                ] = yo

                yp[
                    outside
                ] = (
                    -kx_tail
                    -
                    1.0 / ro
                ) * yo

                u[
                    outside
                ] = uo

                up[
                    outside
                ] = (
                    -epsilon
                    -
                    1.0 / ro
                ) * uo

            return (
                y,
                yp,
                u,
                up,
            )

        qmod.X_MATCH = (
            80.0
        )

        activation = (
            qmod.solve_uncoupled_qball(
                omega_y
            )
        )

        if activation is None:
            raise RuntimeError(
                "Failed activation Q-ball"
            )

        def activation_fields(r):
            """Evaluate activation field and derivative in x coordinates."""

            rho = (
                mu
                * np.asarray(
                    r,
                    dtype=float,
                )
            )

            a, ap_rho = (
                d3a.extended_profile(
                    activation,
                    omega_y,
                    rho,
                )
            )

            return (
                np.asarray(
                    a,
                    dtype=float,
                ),
                mu
                * np.asarray(
                    ap_rho,
                    dtype=float,
                ),
            )

        print(
            f"SOURCE_U0={float(source.sol(X0)[2]):.15e}",
            flush=True,
        )

        print(
            f"ACTIVATION_A0={float(activation.sol(X0)[0]):.15e}",
            flush=True,
        )

        def build_case(
            N: int,
            rmax: float,
        ) -> dict[str, Any]:
            """Build and solve one weighted l=1 variational discretization."""

            grid = (
                chebyshev_variational_grid(
                    N,
                    rmax,
                )
            )

            r = grid[
                "r"
            ]

            w = grid[
                "w"
            ]

            wf = grid[
                "w_full"
            ]

            B = grid[
                "B"
            ]

            D2c = grid[
                "D2_collocation"
            ]

            n = len(
                r
            )

            y, yp, u, up = (
                source_fields(
                    r
                )
            )

            a, ap = (
                activation_fields(
                    r
                )
            )

            f = activation_fraction(
                a
            )

            fp = activation_fp(
                a
            )

            fpp = activation_fpp(
                a
            )

            A = np.exp(
                -0.5
                * f
                * u**2
            )

            wx = W(
                y
            )

            v_xamp = (
                A
                * (
                    1.0
                    -
                    y**2
                )
                /
                (
                    1.0
                    +
                    y**2
                ) ** 2
                -
                omega_x**2
            )

            v_xphase = (
                A
                /
                (
                    1.0
                    +
                    y**2
                )
                -
                omega_x**2
            )

            v_u = (
                epsilon**2
                +
                chi**2
                * A
                * wx
                * (
                    f**2
                    * u**2
                    -
                    f
                )
            )

            v_yamp = (
                mu**2
                * (
                    (
                        1.0
                        -
                        a**2
                    )
                    /
                    (
                        1.0
                        +
                        a**2
                    ) ** 2
                    -
                    omega_y**2
                )
                -
                0.5
                / rho_y
                * u**2
                * A
                * wx
                * (
                    fpp
                    -
                    0.5
                    * u**2
                    * fp**2
                )
            )

            v_yphase = (
                mu**2
                * (
                    1.0
                    /
                    (
                        1.0
                        +
                        a**2
                    )
                    -
                    omega_y**2
                )
                -
                0.5
                / rho_y
                * u**2
                * A
                * wx
                * np.exp(
                    -0.5
                    * a**2
                )
            )

            c_xu = (
                -chi
                * f
                * u
                * A
                * y
                /
                (
                    1.0
                    +
                    y**2
                )
            )

            c_xa = (
                -0.5
                / sqrt_rho
                * u**2
                * fp
                * A
                * y
                /
                (
                    1.0
                    +
                    y**2
                )
            )

            c_ua = (
                -chi
                / sqrt_rho
                * u
                * A
                * wx
                * fp
                * (
                    1.0
                    -
                    0.5
                    * f
                    * u**2
                )
            )

            # ------------------------------------------------------
            # True weak / variational second-derivative form.
            # ------------------------------------------------------

            grad = (
                B.T
                @ (
                    wf[
                        :,
                        None,
                    ]
                    * B
                )
            )

            angular = np.diag(
                w
                * ELL
                * (
                    ELL
                    +
                    1.0
                )
                / r**2
            )

            base = (
                grad
                +
                angular
            )

            def weighted_local(v):
                return np.diag(
                    w
                    * v
                )

            Hxa = (
                base
                +
                weighted_local(
                    v_xamp
                )
            )

            Hxp = (
                base
                +
                weighted_local(
                    v_xphase
                )
            )

            Hu = (
                base
                +
                weighted_local(
                    v_u
                )
            )

            Hya = (
                base
                +
                weighted_local(
                    v_yamp
                )
            )

            Hyp = (
                base
                +
                weighted_local(
                    v_yphase
                )
            )

            HXU = weighted_local(
                c_xu
            )

            HXA = weighted_local(
                c_xa
            )

            HUA = weighted_local(
                c_ua
            )

            Z = np.zeros(
                (
                    n,
                    n,
                ),
                dtype=float,
            )

            H = np.block(
                [
                    [
                        Hxa,
                        Z,
                        HXU,
                        HXA,
                        Z,
                    ],
                    [
                        Z,
                        Hxp,
                        Z,
                        Z,
                        Z,
                    ],
                    [
                        HXU,
                        Z,
                        Hu,
                        HUA,
                        Z,
                    ],
                    [
                        HXA,
                        Z,
                        HUA,
                        Hya,
                        Z,
                    ],
                    [
                        Z,
                        Z,
                        Z,
                        Z,
                        Hyp,
                    ],
                ]
            )

            # ------------------------------------------------------
            # Physical quadrature metric.
            # ------------------------------------------------------

            mdiag = np.tile(
                w,
                5,
            )

            sqrt_m = np.sqrt(
                mdiag
            )

            inv_sqrt_m = (
                1.0
                /
                sqrt_m
            )

            Araw = (
                inv_sqrt_m[
                    :,
                    None,
                ]
                * H
            ) * inv_sqrt_m[
                None,
                :
            ]

            a_sym = float(
                np.linalg.norm(
                    Araw
                    -
                    Araw.T
                )
                /
                max(
                    np.linalg.norm(
                        Araw
                    ),
                    1.0e-300,
                )
            )

            # Only remove roundoff-level antisymmetry after measuring it.
            # If this is not self-adjoint to tolerance, GREEN is impossible.
            Avar = (
                0.5
                * (
                    Araw
                    +
                    Araw.T
                )
            )

            nq = (
                5
                * n
            )

            source_t = np.zeros(
                nq,
                dtype=float,
            )

            activation_t = np.zeros(
                nq,
                dtype=float,
            )

            # Analytic common spatial translation.
            source_t[
                0:n
            ] = (
                r
                * yp
            )

            source_t[
                2 * n:
                3 * n
            ] = (
                r
                * up
                / chi
            )

            activation_t[
                3 * n:
                4 * n
            ] = (
                r
                * sqrt_rho
                * ap
            )

            common_t = (
                source_t
                +
                activation_t
            )

            # Convert physical weighted vectors into Euclidean canonical
            # coordinates z = M^(1/2) v.
            zs = (
                sqrt_m
                * source_t
            )

            za = (
                sqrt_m
                * activation_t
            )

            zc = (
                sqrt_m
                * common_t
            )

            zc_norm = np.linalg.norm(
                zc
            )

            if zc_norm <= 1.0e-300:
                raise RuntimeError(
                    "Degenerate common translation vector"
                )

            zc /= (
                zc_norm
            )

            # A physical relative-displacement direction. It remains in the
            # spectrum and is not projected away.
            zrel = (
                zs
                -
                zc
                * np.dot(
                    zc,
                    zs,
                )
            )

            zrel_norm = np.linalg.norm(
                zrel
            )

            if zrel_norm <= 1.0e-300:
                zrel = (
                    za
                    -
                    zc
                    * np.dot(
                        zc,
                        za,
                    )
                )

                zrel_norm = np.linalg.norm(
                    zrel
                )

            if zrel_norm <= 1.0e-300:
                raise RuntimeError(
                    "Degenerate relative translation direction"
                )

            zrel /= (
                zrel_norm
            )

            common_rayleigh = float(
                zc
                @ Avar
                @ zc
            )

            Azc = (
                Avar
                @ zc
            )

            operator_scale = max(
                float(
                    np.linalg.norm(
                        Avar,
                        ord=np.inf,
                    )
                ),
                1.0,
            )

            common_residual = float(
                np.linalg.norm(
                    Azc
                )
                /
                operator_scale
            )

            relative_rayleigh = float(
                zrel
                @ Avar
                @ zrel
            )

            # ------------------------------------------------------
            # Project ONLY the exact common translation.
            #
            # Rank-one expansion of P A P avoids constructing P and avoids
            # two full dense matrix multiplications.
            # ------------------------------------------------------

            Az = (
                Avar
                @ zc
            )

            zAz = float(
                zc
                @ Az
            )

            Aproj = (
                Avar
                -
                np.outer(
                    zc,
                    Az,
                )
                -
                np.outer(
                    Az,
                    zc,
                )
                +
                zAz
                * np.outer(
                    zc,
                    zc,
                )
            )

            # Lift the removed symmetry direction above the low spectrum.
            lift = max(
                1.0,
                float(
                    np.max(
                        np.abs(
                            np.diag(
                                Avar
                            )
                        )
                    )
                ),
            )

            Aproj += (
                lift
                * np.outer(
                    zc,
                    zc,
                )
            )

            Aproj = (
                0.5
                * (
                    Aproj
                    +
                    Aproj.T
                )
            )

            evals, evecs = eigh(
                Aproj,
                subset_by_index=(
                    0,
                    7,
                ),
                eigvals_only=False,
                check_finite=False,
                driver="evr",
            )

            projected_lambda0 = float(
                evals[
                    0
                ]
            )

            lowest_vec = evecs[
                :,
                0
            ]

            relative_overlap = float(
                abs(
                    np.dot(
                        zrel,
                        lowest_vec,
                    )
                )
            )

            h_sym = float(
                np.linalg.norm(
                    H
                    -
                    H.T
                )
                /
                max(
                    np.linalg.norm(
                        H
                    ),
                    1.0e-300,
                )
            )

            # ------------------------------------------------------
            # Diagnostic reconstruction of old strong collocation K.
            #
            # This is NOT used in the R3 decision. Its weighted asymmetry
            # quantifies why raw collocation + Euclidean projection is not
            # the correct variational object.
            # ------------------------------------------------------

            Tcoll = (
                -D2c
                +
                np.diag(
                    ELL
                    * (
                        ELL
                        +
                        1.0
                    )
                    / r**2
                )
            )

            Lxa = (
                Tcoll
                +
                np.diag(
                    v_xamp
                )
            )

            Lxp = (
                Tcoll
                +
                np.diag(
                    v_xphase
                )
            )

            Lu = (
                Tcoll
                +
                np.diag(
                    v_u
                )
            )

            Lya = (
                Tcoll
                +
                np.diag(
                    v_yamp
                )
            )

            Lyp = (
                Tcoll
                +
                np.diag(
                    v_yphase
                )
            )

            CXU = np.diag(
                c_xu
            )

            CXA = np.diag(
                c_xa
            )

            CUA = np.diag(
                c_ua
            )

            Kcoll = np.block(
                [
                    [
                        Lxa,
                        Z,
                        CXU,
                        CXA,
                        Z,
                    ],
                    [
                        Z,
                        Lxp,
                        Z,
                        Z,
                        Z,
                    ],
                    [
                        CXU,
                        Z,
                        Lu,
                        CUA,
                        Z,
                    ],
                    [
                        CXA,
                        Z,
                        CUA,
                        Lya,
                        Z,
                    ],
                    [
                        Z,
                        Z,
                        Z,
                        Z,
                        Lyp,
                    ],
                ]
            )

            Acoll_w = (
                sqrt_m[
                    :,
                    None,
                ]
                * Kcoll
            ) * inv_sqrt_m[
                None,
                :
            ]

            coll_weighted_asym = float(
                np.linalg.norm(
                    Acoll_w
                    -
                    Acoll_w.T
                )
                /
                max(
                    np.linalg.norm(
                        Acoll_w
                    ),
                    1.0e-300,
                )
            )

            goldstone_floor = max(
                abs(
                    common_rayleigh
                ),
                common_residual
                * operator_scale,
            )

            margin_ratio = (
                projected_lambda0
                /
                max(
                    goldstone_floor,
                    1.0e-300,
                )
            )

            return {
                "N":
                    N,

                "rmax":
                    rmax,

                "n":
                    n,

                "quadrature_sum":
                    float(
                        np.sum(
                            wf
                        )
                    ),

                "H_symmetry_rel":
                    h_sym,

                "A_symmetry_rel":
                    a_sym,

                "raw_collocation_weighted_asymmetry_rel":
                    coll_weighted_asym,

                "common_translation_rayleigh":
                    common_rayleigh,

                "common_translation_residual":
                    common_residual,

                "relative_translation_rayleigh":
                    relative_rayleigh,

                "relative_translation_overlap_lowest":
                    relative_overlap,

                "projected_lambda0":
                    projected_lambda0,

                "projected_lambda1":
                    float(
                        evals[
                            1
                        ]
                    ),

                "projected_lambda2":
                    float(
                        evals[
                            2
                        ]
                    ),

                "projected_lambda3":
                    float(
                        evals[
                            3
                        ]
                    ),

                "projected_lambda4":
                    float(
                        evals[
                            4
                        ]
                    ),

                "projected_lambda5":
                    float(
                        evals[
                            5
                        ]
                    ),

                "goldstone_floor":
                    goldstone_floor,

                "projected_over_goldstone_floor":
                    margin_ratio,

                "source_translation_weighted_norm":
                    float(
                        np.linalg.norm(
                            zs
                        )
                    ),

                "activation_translation_weighted_norm":
                    float(
                        np.linalg.norm(
                            za
                        )
                    ),
            }

        print(
            "\n=== STAGE D: WEIGHTED l=1 GRID / DOMAIN LADDER ===",
            flush=True,
        )

        rows = []

        for N in MAIN_N_VALUES:
            print(
                f"START_WEIGHTED N={N} RMAX={MAIN_RMAX:.1f}",
                flush=True,
            )

            row = build_case(
                N,
                MAIN_RMAX,
            )

            rows.append(
                row
            )

            print(
                "RESULT "
                f"N={N} "
                f"RMAX={MAIN_RMAX:.1f} "
                f"LAMBDA0={row['projected_lambda0']:+.15e} "
                f"GOLD_RQ={row['common_translation_rayleigh']:+.15e} "
                f"GOLD_RES={row['common_translation_residual']:.6e} "
                f"REL_RQ={row['relative_translation_rayleigh']:+.15e} "
                f"REL_OV={row['relative_translation_overlap_lowest']:.9f} "
                f"RAW_ASYM={row['raw_collocation_weighted_asymmetry_rel']:.6e}",
                flush=True,
            )

        for N, rmax in DOMAIN_CASES:
            print(
                f"START_WEIGHTED N={N} RMAX={rmax:.1f}",
                flush=True,
            )

            row = build_case(
                N,
                rmax,
            )

            rows.append(
                row
            )

            print(
                "RESULT "
                f"N={N} "
                f"RMAX={rmax:.1f} "
                f"LAMBDA0={row['projected_lambda0']:+.15e} "
                f"GOLD_RQ={row['common_translation_rayleigh']:+.15e} "
                f"GOLD_RES={row['common_translation_residual']:.6e} "
                f"REL_RQ={row['relative_translation_rayleigh']:+.15e} "
                f"REL_OV={row['relative_translation_overlap_lowest']:.9f}",
                flush=True,
            )

        main_rows = [
            row
            for row
            in rows
            if row[
                "rmax"
            ]
            ==
            MAIN_RMAX
        ]

        finest = main_rows[
            -1
        ]

        domain = rows[
            -1
        ]

        last3 = [
            row[
                "projected_lambda0"
            ]
            for row
            in main_rows[
                -3:
            ]
        ]

        grid_spread = relative_spread(
            last3
        )

        domain_rel_diff = relerr(
            finest[
                "projected_lambda0"
            ],
            domain[
                "projected_lambda0"
            ],
        )

        max_h_sym = max(
            row[
                "H_symmetry_rel"
            ]
            for row
            in rows
        )

        max_a_sym = max(
            row[
                "A_symmetry_rel"
            ]
            for row
            in rows
        )

        max_gold_res = max(
            row[
                "common_translation_residual"
            ]
            for row
            in main_rows[
                -2:
            ]
        )

        finest_floor = max(
            finest[
                "goldstone_floor"
            ],
            1.0e-300,
        )

        finest_lambda = finest[
            "projected_lambda0"
        ]

        positive_separation = (
            finest_lambda
            /
            finest_floor
        )

        negative_separation = (
            -finest_lambda
            /
            finest_floor
        )

        symmetry_pass = bool(
            max_h_sym
            <=
            H_SYM_REL_TOL
            and
            max_a_sym
            <=
            A_SYM_REL_TOL
        )

        grid_pass = bool(
            grid_spread
            <=
            GRID_REL_SPREAD_MAX
        )

        domain_pass = bool(
            domain_rel_diff
            <=
            DOMAIN_REL_DIFF_MAX
        )

        translation_pass = bool(
            max_gold_res
            <=
            TRANSLATION_RESIDUAL_MAX
        )

        robust_positive = bool(
            finest_lambda
            >=
            MIN_ABS_POSITIVE_LAMBDA

            and
            positive_separation
            >=
            GOLDSTONE_MARGIN_FACTOR

            and
            grid_pass

            and
            domain_pass

            and
            translation_pass

            and
            symmetry_pass
        )

        robust_negative = bool(
            finest_lambda
            <
            0.0

            and
            negative_separation
            >=
            NEGATIVE_MARGIN_FACTOR

            and
            grid_pass

            and
            domain_pass

            and
            translation_pass

            and
            symmetry_pass
        )

        if robust_positive:
            classification = (
                "GREEN_D3CR3_WEIGHTED_VARIATIONAL_L1_"
                "COMMON_TRANSLATION_REMOVED_NEXT_MODE_POSITIVE"
            )

            next_action = (
                "031D3D_EXPLICIT_QY_RESERVOIR_TRANSFER_"
                "RESET_RADIATION"
            )

            variational_stability = (
                "PASS"
            )

        elif robust_negative:
            classification = (
                "RED_D3CR3_WEIGHTED_VARIATIONAL_L1_"
                "ROBUST_NEGATIVE_SECOND_VARIATION"
            )

            next_action = (
                "DEMOTE_D3_AND_DIAGNOSE_RELATIVE_TRANSLATION_"
                "OR_OTHER_L1_MODE"
            )

            variational_stability = (
                "FAIL"
            )

        else:
            classification = (
                "YELLOW_D3CR3_WEIGHTED_VARIATIONAL_L1_"
                "NUMERICALLY_OR_PHYSICALLY_UNRESOLVED"
            )

            next_action = (
                "REFINE_ONLY_WEIGHTED_L1_ZERO_OR_SOFT_MODE_STRUCTURE"
            )

            variational_stability = (
                "UNRESOLVED"
            )

        print(
            "\n=== STAGE E: DECISION ===",
            flush=True,
        )

        print(
            f"MAX_H_SYMMETRY_REL={max_h_sym:.15e}",
            flush=True,
        )

        print(
            f"MAX_A_SYMMETRY_REL={max_a_sym:.15e}",
            flush=True,
        )

        print(
            f"GRID_LAST3_REL_SPREAD={grid_spread:.15e}",
            flush=True,
        )

        print(
            f"DOMAIN_REL_DIFF={domain_rel_diff:.15e}",
            flush=True,
        )

        print(
            f"MAX_FINE_TRANSLATION_RESIDUAL={max_gold_res:.15e}",
            flush=True,
        )

        print(
            f"FINEST_PROJECTED_LAMBDA0={finest_lambda:.15e}",
            flush=True,
        )

        print(
            f"FINEST_GOLDSTONE_FLOOR={finest_floor:.15e}",
            flush=True,
        )

        print(
            f"FINEST_POSITIVE_SEPARATION={positive_separation:.15e}",
            flush=True,
        )

        print(
            f"FINEST_NEGATIVE_SEPARATION={negative_separation:.15e}",
            flush=True,
        )

        print(
            "FINEST_RELATIVE_TRANSLATION_RAYLEIGH="
            f"{finest['relative_translation_rayleigh']:.15e}",
            flush=True,
        )

        print(
            "FINEST_RELATIVE_TRANSLATION_OVERLAP_LOWEST="
            f"{finest['relative_translation_overlap_lowest']:.15e}",
            flush=True,
        )

        print(
            f"WEIGHTED_SELF_ADJOINTNESS_PASS={symmetry_pass}",
            flush=True,
        )

        print(
            f"GRID_CONVERGENCE_PASS={grid_pass}",
            flush=True,
        )

        print(
            f"DOMAIN_CONVERGENCE_PASS={domain_pass}",
            flush=True,
        )

        print(
            f"TRANSLATION_RESIDUAL_PASS={translation_pass}",
            flush=True,
        )

        print(
            f"ROBUST_POSITIVE_NEXT_MODE={robust_positive}",
            flush=True,
        )

        print(
            f"ROBUST_NEGATIVE_NEXT_MODE={robust_negative}",
            flush=True,
        )

        print(
            f"D3_L1_VARIATIONAL_STABILITY={variational_stability}",
            flush=True,
        )

        print(
            "TRUE_EXPONENTIAL_INSTABILITY_ESTABLISHED_BY_R3_ALONE=False",
            flush=True,
        )

        print(
            f"031D3CR3_CLASSIFICATION={classification}",
            flush=True,
        )

        print(
            f"NEXT={next_action}",
            flush=True,
        )

        inherited_direct = bool(
            d3cr[
                "decision"
            ][
                "l1_continuum_pass"
            ]
        )

        d3_coupled_linear_promoted = bool(
            robust_positive
            and
            inherited_direct
        )

        print(
            f"INHERITED_DIRECT_L1_CONTINUUM_PASS={inherited_direct}",
            flush=True,
        )

        print(
            "D3_COUPLED_LINEAR_STABILITY_PROMOTION_AUTHORIZED="
            f"{d3_coupled_linear_promoted}",
            flush=True,
        )

        summary = {
            "generated_utc":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "classification":
                classification,

            "next":
                next_action,

            "claim_class":
                "WEIGHTED_VARIATIONAL_COUPLED_LINEAR_STABILITY_GATE",

            "model": {
                "ell":
                    ELL,

                "omega_x":
                    omega_x,

                "omega_y":
                    omega_y,

                "epsilon":
                    epsilon,

                "chi":
                    chi,

                "mu":
                    mu,

                "rho_y":
                    rho_y,
            },

            "variational_derivation": {
                "reduced_inner_product":
                    "integral dr sum_i q_i^2",

                "fixed_q_l1_tangent":
                    True,

                "reason":
                    (
                        "spherical background times Y_1m integrates "
                        "to zero at first order"
                    ),

                "quadrature":
                    "Clenshaw-Curtis on Chebyshev-Lobatto nodes",

                "gradient_form":
                    "B.T @ W @ B",

                "projected_symmetry":
                    "common translation only",

                "relative_translation_projected":
                    False,
            },

            "validation":
                validation,

            "rows":
                rows,

            "decision_metrics": {
                "max_H_symmetry_rel":
                    max_h_sym,

                "max_A_symmetry_rel":
                    max_a_sym,

                "grid_last3_rel_spread":
                    grid_spread,

                "domain_rel_diff":
                    domain_rel_diff,

                "max_fine_translation_residual":
                    max_gold_res,

                "finest_projected_lambda0":
                    finest_lambda,

                "finest_goldstone_floor":
                    finest_floor,

                "finest_positive_separation":
                    positive_separation,

                "finest_negative_separation":
                    negative_separation,

                "finest_relative_translation_rayleigh":
                    finest[
                        "relative_translation_rayleigh"
                    ],

                "finest_relative_translation_overlap_lowest":
                    finest[
                        "relative_translation_overlap_lowest"
                    ],

                "weighted_self_adjointness_pass":
                    symmetry_pass,

                "grid_convergence_pass":
                    grid_pass,

                "domain_convergence_pass":
                    domain_pass,

                "translation_residual_pass":
                    translation_pass,

                "robust_positive_next_mode":
                    robust_positive,

                "robust_negative_next_mode":
                    robust_negative,

                "variational_stability":
                    variational_stability,

                "inherited_direct_l1_continuum_pass":
                    inherited_direct,

                "d3_coupled_linear_stability_promotion_authorized":
                    d3_coupled_linear_promoted,
            },

            "r2_context": {
                "classification":
                    d3cr2.get(
                        "classification",
                        "UNKNOWN",
                    ),

                "old_projected_stiffness_not_used_for_r3_decision":
                    True,
            },

            "claim_limits": [
                (
                    "GREEN is only a coupled-linear/energetic l=1 result "
                    "in the declared flat-space effective X/phi/Y theory."
                ),
                (
                    "Only the exact common translation is removed; "
                    "relative source-versus-activation displacement "
                    "remains physical."
                ),
                (
                    "A negative weighted second variation fails the "
                    "variational stability gate but R3 alone does not "
                    "assert an exponential growth rate."
                ),
                (
                    "Explicit QY reservoir/transfer/reset and switching "
                    "radiation remain open."
                ),
                (
                    "Nonlinear fragmentation, Einstein backreaction, "
                    "EFT/naturalness and empirical closure remain open."
                ),
                (
                    "No practical antigravity device is established."
                ),
            ],
        }

        OUT_JSON.write_text(
            json.dumps(
                builtin(
                    summary
                ),
                indent=2,
                sort_keys=True,
            )
            +
            "\n"
        )

        fields = sorted(
            {
                key
                for row
                in rows
                for key
                in row
            }
        )

        with OUT_CSV.open(
            "w",
            newline="",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=fields,
            )

            writer.writeheader()
            writer.writerows(
                rows
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}",
            flush=True,
        )

        print(
            f"SCAN_CSV={OUT_CSV}",
            flush=True,
        )

    finally:
        qmod.X_MATCH = (
            old_xmatch
        )


if __name__ == "__main__":
    main()
