#!/usr/bin/env python3
"""
031D3C-R4 — translational Ward identity + cancellation-free relative-mode closeout.

Purpose
-------
Resolve the only remaining coupled-linear l=1 ambiguity left by 031D3C-R3.
R3 established a self-adjoint weighted variational Hessian, but its lowest
non-Goldstone eigenvalue alternated around zero and its eigenvector converged
almost exactly onto the physical relative translation of the X/phi source
against the Y activation Q-ball.

This run attacks that one coordinate directly in two complementary ways:

1. reconstruct the FULL fixed-QX,QY D3B coupled background;
2. compute the relative-translation curvature from a cancellation-free mixed
   Hessian / integration-by-parts identity, with direct and finite-displacement
   reconstructions;
3. rebuild the weighted Chebyshev l=1 Hessian;
4. enforce the exact common-translation Ward identity with the minimum
   symmetric rank correction;
5. insert the independently reconstructed exact relative collective Rayleigh
   quotient while leaving all couplings to orthogonal physical modes intact;
6. test the resulting lowest non-Goldstone eigenvalue on a grid/domain ladder.

Scientific question
-------------------
Is the apparent R3 l=1 mode a real negative relative-displacement curvature,
or a discretization violation of the exact common translational Goldstone
identity around an exceptionally soft but nonnegative physical mode?

Promotion condition
-------------------
GREEN requires the full coupled fixed-QX,QY background, a robust positive
cancellation-free relative curvature, a converged positive Ward/collective-
matched lowest l=1 eigenvalue, and a positive separated next mode.

Falsifier / stop rule
---------------------
A converged negative full-background relative second variation demotes D3.
If the sign remains below the absolute numerical uncertainty, do not optimize
anything else: refine only this soft l=1 structure.

Only the exact common translation is removed. Relative X/phi-versus-Y
translation remains physical. A robust negative result is a variational
stability failure, but R4 alone does not assert an exponential growth rate.

Outputs
-------
results/data/031d3cr4_relative_translation_ward_summary.json
results/data/031d3cr4_relative_translation_curvature_scan.csv
results/data/031d3cr4_ward_hessian_scan.csv

No practical device, nonlinear stability, Einstein backreaction, explicit QY
reservoir, switching-radiation closure, EFT/naturalness closure, or empirical
closure is claimed here.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path
import sys
from typing import Any, Callable

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import cumulative_trapezoid, solve_bvp
from scipy.linalg import eigh


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"
DATA.mkdir(parents=True, exist_ok=True)

D3B_SOURCE = SIM / "031d3b_full_fixedqx_qy_coupled_activation.py"
QBALL_SOURCE = SIM / "031b2a_global_qball_activated_scalar_control.py"
D3A_SOURCE = SIM / "031d3a_u1_metric_activation_capacity.py"

D3B_SUMMARY = DATA / "031d3b_full_coupled_activation_summary.json"
R3_SUMMARY = DATA / "031d3cr3_weighted_variational_l1_summary.json"

OUT_JSON = DATA / "031d3cr4_relative_translation_ward_summary.json"
OUT_CURVATURE_CSV = DATA / "031d3cr4_relative_translation_curvature_scan.csv"
OUT_HESSIAN_CSV = DATA / "031d3cr4_ward_hessian_scan.csv"

X0 = 1.0e-5
X_SOURCE_MATCH = 80.0
FULL_BVP_XMAX = 500.0
HOMOTOPY_VALUES = (0.0, 0.25, 0.50, 0.75, 1.0)
BVP_TOL_HOMOTOPY = 2.0e-5
BVP_TOL_FINAL = 6.0e-6
BVP_TOL_TIGHT = 2.0e-6
MAX_NODES = 90_000

RADIAL_PARTITIONS = (
    0.0,
    0.5,
    1.0,
    2.0,
    4.0,
    8.0,
    12.0,
    20.0,
    30.0,
    45.0,
    65.0,
    90.0,
    130.0,
    180.0,
    250.0,
    350.0,
    450.0,
    500.0,
)

QUAD_ORDERS = (32, 48, 64, 80)
DOMAIN_RADII = (180.0, 250.0, 350.0, 450.0, 500.0)

FD_DISPLACEMENTS = (0.25, 0.50, 0.75, 1.00)
FD_RADIAL_ORDER = 64
FD_ANGULAR_ORDER = 80
FD_RMAX = 450.0

HESSIAN_CASES = (
    (176, 600.0),
    (208, 600.0),
    (240, 600.0),
    (320, 800.0),
)

ELL = 1
COMMON_LIFT = 0.10
LOW_EIGEN_COUNT = 6

SIGN_SIGMA = 8.0
MIN_NEXT_GAP = 1.0e-6
MAX_ORACLE_RELERR = 2.0e-9
MAX_WARD_RESIDUAL = 2.0e-10
MAX_COLLECTIVE_RQ_RELERR = 5.0e-9
MAX_NORM_R3_RELERR = 2.0e-3
MAX_BVP_CHARGE_RELERR = 1.0e-5
MAX_BVP_RMS = 3.0e-5


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"Missing required artifact: {path}")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)

    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module

    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise

    return module


def relerr(
    a: float,
    b: float,
    floor: float = 1.0e-300,
) -> float:
    return abs(a - b) / max(
        abs(a),
        abs(b),
        floor,
    )


def builtin(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(k): builtin(v)
            for k, v in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            builtin(v)
            for v in value
        ]

    if isinstance(value, np.ndarray):
        return [
            builtin(v)
            for v in value.tolist()
        ]

    if isinstance(
        value,
        (
            np.floating,
            np.integer,
            np.bool_,
        ),
    ):
        return value.item()

    return value


def W(field):
    field = np.asarray(
        field,
        dtype=float,
    )

    return 0.5 * np.log1p(
        field * field
    )


def activation_fraction(a):
    a = np.asarray(
        a,
        dtype=float,
    )

    return 1.0 - np.exp(
        -0.5 * a * a
    )


def activation_fraction_prime(a):
    a = np.asarray(
        a,
        dtype=float,
    )

    return (
        a
        * np.exp(
            -0.5 * a * a
        )
    )


def activation_fraction_second(a):
    a = np.asarray(
        a,
        dtype=float,
    )

    return (
        (1.0 - a * a)
        * np.exp(
            -0.5 * a * a
        )
    )


def segmented_gauss(
    rmax: float,
    order: int,
) -> tuple[np.ndarray, np.ndarray]:
    edges = [
        x
        for x in RADIAL_PARTITIONS
        if x < rmax
    ]

    if (
        not edges
        or edges[0] != 0.0
    ):
        edges.insert(
            0,
            0.0,
        )

    if not math.isclose(
        edges[-1],
        rmax,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    ):
        edges.append(
            float(rmax)
        )

    z, wz = leggauss(
        order
    )

    nodes = []
    weights = []

    for left, right in zip(
        edges[:-1],
        edges[1:],
        strict=True,
    ):
        if right <= left:
            continue

        nodes.append(
            0.5
            * (right - left)
            * z
            + 0.5
            * (right + left)
        )

        weights.append(
            0.5
            * (right - left)
            * wz
        )

    return (
        np.concatenate(nodes),
        np.concatenate(weights),
    )


def chebyshev_lobatto(
    N: int,
) -> tuple[np.ndarray, np.ndarray]:
    if N < 2:
        raise ValueError(
            "N must be >=2"
        )

    j = np.arange(
        N + 1
    )

    x = np.cos(
        np.pi * j / N
    )

    c = np.ones(
        N + 1
    )

    c[0] = 2.0
    c[-1] = 2.0

    c *= (
        (-1.0) ** j
    )

    X = np.tile(
        x,
        (N + 1, 1),
    ).T

    dX = X - X.T

    D = (
        np.outer(
            c,
            1.0 / c,
        )
        / (
            dX
            + np.eye(
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

    return (
        x,
        D,
    )


def clenshaw_curtis_weights(
    N: int,
) -> np.ndarray:
    if N == 1:
        return np.array(
            [
                1.0,
                1.0,
            ]
        )

    theta = (
        np.pi
        * np.arange(
            N + 1
        )
        / N
    )

    w = np.zeros(
        N + 1
    )

    ii = np.arange(
        1,
        N,
    )

    v = np.ones(
        N - 1
    )

    if N % 2 == 0:
        w[0] = (
            1.0
            / (
                N * N
                - 1.0
            )
        )

        w[-1] = w[0]

        for k in range(
            1,
            N // 2,
        ):
            v -= (
                2.0
                * np.cos(
                    2.0
                    * k
                    * theta[ii]
                )
                / (
                    4.0
                    * k
                    * k
                    - 1.0
                )
            )

        v -= (
            np.cos(
                N
                * theta[ii]
            )
            / (
                N * N
                - 1.0
            )
        )

    else:
        w[0] = (
            1.0
            / (
                N * N
            )
        )

        w[-1] = w[0]

        for k in range(
            1,
            (N + 1) // 2,
        ):
            v -= (
                2.0
                * np.cos(
                    2.0
                    * k
                    * theta[ii]
                )
                / (
                    4.0
                    * k
                    * k
                    - 1.0
                )
            )

    w[ii] = (
        2.0
        * v
        / N
    )

    return w


def stage_a_oracles() -> dict[str, float | bool]:
    """
    Validate quadrature, mixed-curvature identity,
    and Ward-repair algebra.
    """

    N = 80
    R = 1.0

    x, Dx = (
        chebyshev_lobatto(
            N
        )
    )

    r = (
        0.5
        * R
        * (
            1.0 - x
        )
    )

    Dr = (
        -2.0
        * Dx
        / R
    )

    w = (
        0.5
        * R
        * clenshaw_curtis_weights(
            N
        )
    )

    E = np.zeros(
        (
            N + 1,
            N - 1,
        )
    )

    E[
        1:N,
        :,
    ] = np.eye(
        N - 1
    )

    B = (
        Dr
        @ E
    )

    Hgrad = (
        B.T
        @ (
            w[
                :,
                None,
            ]
            * B
        )
    )

    ri = r[
        1:N
    ]

    wi = w[
        1:N
    ]

    invsqrt = (
        1.0
        / np.sqrt(
            wi
        )
    )

    Akin = (
        invsqrt[
            :,
            None,
        ]
        * Hgrad
        * invsqrt[
            None,
            :,
        ]
    )

    free0 = float(
        eigh(
            Akin,
            subset_by_index=[
                0,
                0,
            ],
            eigvals_only=True,
        )[0]
    )

    A1 = (
        Akin
        + np.diag(
            2.0
            / (
                ri
                * ri
            )
        )
    )

    free1 = float(
        eigh(
            A1,
            subset_by_index=[
                0,
                0,
            ],
            eigvals_only=True,
        )[0]
    )

    expected0 = (
        math.pi**2
    )

    expected1 = (
        4.493409457909064**2
    )

    alpha = 0.7
    beta = 1.1

    rg, wg = (
        segmented_gauss(
            8.0,
            80,
        )
    )

    P = np.exp(
        -alpha
        * rg
        * rg
    )

    Pp = (
        -2.0
        * alpha
        * rg
        * P
    )

    a = np.exp(
        -beta
        * rg
        * rg
    )

    ap = (
        -2.0
        * beta
        * rg
        * a
    )

    lap_a = (
        (
            -6.0
            * beta
            + 4.0
            * beta
            * beta
            * rg
            * rg
        )
        * a
    )

    k_direct = float(
        np.sum(
            wg
            * rg
            * rg
            * P
            * lap_a
        )
    )

    k_parts = float(
        -np.sum(
            wg
            * rg
            * rg
            * Pp
            * ap
        )
    )

    overlap0 = (
        math.pi
        / (
            alpha
            + beta
        )
    ) ** 1.5

    epp_exact = (
        -2.0
        * alpha
        * beta
        / (
            alpha
            + beta
        )
        * overlap0
    )

    k_exact = (
        3.0
        * epp_exact
        / (
            4.0
            * math.pi
        )
    )

    d = 0.20

    um, wm = (
        leggauss(
            100
        )
    )

    s = np.sqrt(
        rg[
            :,
            None,
        ] ** 2
        + d * d
        - 2.0
        * rg[
            :,
            None,
        ]
        * d
        * um[
            None,
            :,
        ]
    )

    delta = (
        P[
            :,
            None,
        ]
        * (
            np.exp(
                -beta
                * s
                * s
            )
            - a[
                :,
                None,
            ]
        )
    )

    delta_e = (
        2.0
        * math.pi
        * float(
            np.sum(
                wg[
                    :,
                    None,
                ]
                * rg[
                    :,
                    None,
                ] ** 2
                * wm[
                    None,
                    :,
                ]
                * delta
            )
        )
    )

    exact_delta_e = (
        overlap0
        * (
            math.exp(
                -alpha
                * beta
                / (
                    alpha
                    + beta
                )
                * d
                * d
            )
            - 1.0
        )
    )

    S = 4.0
    A_mass = 1.5
    k = 0.002

    lambda_rel = (
        k
        * (
            1.0 / S
            + 1.0 / A_mass
        )
    )

    zS = np.array(
        [
            math.sqrt(S),
            0.0,
            0.0,
        ]
    )

    zA = np.array(
        [
            0.0,
            math.sqrt(A_mass),
            0.0,
        ]
    )

    uc = (
        zS
        + zA
    )

    uc /= (
        np.linalg.norm(
            uc
        )
    )

    ur = (
        zS / S
        - zA / A_mass
    )

    ur -= (
        uc
        * float(
            np.dot(
                uc,
                ur,
            )
        )
    )

    ur /= (
        np.linalg.norm(
            ur
        )
    )

    orth = np.cross(
        uc,
        ur,
    )

    exact = (
        lambda_rel
        * np.outer(
            ur,
            ur,
        )
        + 0.04
        * np.outer(
            orth,
            orth,
        )
    )

    contamination = np.array(
        [
            [
                2.0e-4,
                -1.0e-4,
                5.0e-5,
            ],
            [
                -1.0e-4,
                -1.0e-4,
                -2.0e-5,
            ],
            [
                5.0e-5,
                -2.0e-5,
                0.0,
            ],
        ],
        dtype=float,
    )

    raw = (
        exact
        + contamination
    )

    residual = (
        raw
        @ uc
    )

    rq = float(
        np.dot(
            uc,
            residual,
        )
    )

    ward = (
        raw
        - np.outer(
            residual,
            uc,
        )
        - np.outer(
            uc,
            residual,
        )
        + rq
        * np.outer(
            uc,
            uc,
        )
    )

    ward_res = float(
        np.linalg.norm(
            ward
            @ uc
        )
    )

    ur_rq = float(
        ur
        @ ward
        @ ur
    )

    matched = (
        ward
        + (
            lambda_rel
            - ur_rq
        )
        * np.outer(
            ur,
            ur,
        )
    )

    collective_relerr = relerr(
        float(
            ur
            @ matched
            @ ur
        ),
        lambda_rel,
    )

    errors = (
        relerr(
            float(
                np.sum(
                    w
                )
            ),
            R,
        ),
        relerr(
            free0,
            expected0,
        ),
        relerr(
            free1,
            expected1,
        ),
        relerr(
            k_direct,
            k_exact,
        ),
        relerr(
            k_parts,
            k_exact,
        ),
        relerr(
            delta_e,
            exact_delta_e,
        ),
        collective_relerr,
    )

    passed = bool(
        max(errors)
        <= MAX_ORACLE_RELERR
        and ward_res
        <= 1.0e-13
    )

    return {
        "quadrature_sum":
            float(
                np.sum(
                    w
                )
            ),

        "free_l0":
            free0,

        "free_l0_expected":
            expected0,

        "free_l0_relerr":
            relerr(
                free0,
                expected0,
            ),

        "free_l1":
            free1,

        "free_l1_expected":
            expected1,

        "free_l1_relerr":
            relerr(
                free1,
                expected1,
            ),

        "gaussian_k_direct":
            k_direct,

        "gaussian_k_parts":
            k_parts,

        "gaussian_k_exact":
            k_exact,

        "gaussian_direct_relerr":
            relerr(
                k_direct,
                k_exact,
            ),

        "gaussian_parts_relerr":
            relerr(
                k_parts,
                k_exact,
            ),

        "gaussian_delta_e_numeric":
            delta_e,

        "gaussian_delta_e_exact":
            exact_delta_e,

        "gaussian_delta_e_relerr":
            relerr(
                delta_e,
                exact_delta_e,
            ),

        "ward_residual":
            ward_res,

        "ward_collective_rq_relerr":
            collective_relerr,

        "pass":
            passed,
    }


def source_tail_fields(
    r: np.ndarray,
    match: float,
    boundary: np.ndarray,
    omega_x: float,
    epsilon: float,
    source,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
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
        r <= match
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

        kx = math.sqrt(
            max(
                1.0
                - omega_x
                * omega_x,
                1.0e-14,
            )
        )

        yb = float(
            boundary[
                0
            ]
        )

        ub = float(
            boundary[
                2
            ]
        )

        yo = (
            yb
            * match
            / ro
            * np.exp(
                -kx
                * (
                    ro
                    - match
                )
            )
        )

        uo = (
            ub
            * match
            / ro
            * np.exp(
                -epsilon
                * (
                    ro
                    - match
                )
            )
        )

        y[
            outside
        ] = yo

        yp[
            outside
        ] = (
            -kx
            - 1.0 / ro
        ) * yo

        u[
            outside
        ] = uo

        up[
            outside
        ] = (
            -epsilon
            - 1.0 / ro
        ) * uo

    return (
        y,
        yp,
        u,
        up,
    )


def build_product_background(
    qmod,
    d3a,
    omega_x: float,
    omega_y: float,
    epsilon: float,
    chi: float,
    mu: float,
    match: float,
):
    old_match = float(
        qmod.X_MATCH
    )

    qmod.X_MATCH = float(
        match
    )

    try:
        seed = (
            qmod.solve_uncoupled_qball(
                omega_x
            )
        )

        if seed is None:
            raise RuntimeError(
                "Failed uncoupled source Q-ball reconstruction"
            )

        source = (
            qmod.solve_coupled(
                seed,
                omega_x,
                epsilon,
                chi,
                previous=None,
            )
        )

        if source is None:
            raise RuntimeError(
                "Failed scalarized source reconstruction"
            )

        activation = (
            qmod.solve_uncoupled_qball(
                omega_y
            )
        )

        if activation is None:
            raise RuntimeError(
                "Failed activation Q-ball reconstruction"
            )

    finally:
        qmod.X_MATCH = (
            old_match
        )

    source_boundary = (
        source.sol(
            match
        )
    )

    def evaluate(r):
        rr = np.asarray(
            r,
            dtype=float,
        )

        y, yp, u, up = (
            source_tail_fields(
                rr,
                match,
                source_boundary,
                omega_x,
                epsilon,
                source,
            )
        )

        rho = (
            mu
            * rr
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
                y,
                dtype=float,
            ),
            np.asarray(
                yp,
                dtype=float,
            ),
            np.asarray(
                u,
                dtype=float,
            ),
            np.asarray(
                up,
                dtype=float,
            ),
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

    return (
        evaluate,
        source,
        activation,
    )


def reconstruct_full_background(
    d3b,
    qmod,
    d3a,
    product80: Callable,
    source80,
    activation80,
    *,
    omega_x_seed: float,
    omega_y_seed: float,
    epsilon: float,
    chi: float,
    mu: float,
    rho_y: float,
    target_qx: float,
    target_qy: float,
):
    """
    Reconstruct the D3B fixed-QX,QY t=1 BVP
    and return coarse/fine/tight solutions.
    """

    del product80

    source_boundary = (
        source80.sol(
            X_SOURCE_MATCH
        )
    )

    def independent_source_fields(
        x,
    ):
        return source_tail_fields(
            np.asarray(
                x,
                dtype=float,
            ),
            X_SOURCE_MATCH,
            source_boundary,
            omega_x_seed,
            epsilon,
            source80,
        )

    def independent_activation_fields(
        x,
    ):
        rho = (
            mu
            * np.asarray(
                x,
                dtype=float,
            )
        )

        a, ap_rho = (
            d3a.extended_profile(
                activation80,
                omega_y_seed,
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

    def equations_factory(
        t_value: float,
    ):
        def equations(
            x,
            state,
            parameters,
        ):
            omega_x = float(
                parameters[
                    0
                ]
            )

            omega_y = float(
                parameters[
                    1
                ]
            )

            y = state[
                0
            ]

            u = state[
                2
            ]

            a = state[
                4
            ]

            f = (
                activation_fraction(
                    a
                )
            )

            fp = (
                activation_fraction_prime(
                    a
                )
            )

            f_t = (
                1.0
                - t_value
                * (
                    1.0
                    - f
                )
            )

            A_x = np.exp(
                -0.5
                * f_t
                * u
                * u
            )

            W_x = W(
                y
            )

            reciprocal = (
                -t_value
                * 0.5
                / rho_y
                * u
                * u
                * A_x
                * W_x
                * fp
            )

            return np.vstack(
                (
                    state[
                        1
                    ],

                    A_x
                    * y
                    / (
                        1.0
                        + y * y
                    )
                    - omega_x
                    * omega_x
                    * y
                    - 2.0
                    * state[
                        1
                    ]
                    / x,

                    state[
                        3
                    ],

                    epsilon
                    * epsilon
                    * u
                    - chi
                    * chi
                    * f_t
                    * A_x
                    * W_x
                    * u
                    - 2.0
                    * state[
                        3
                    ]
                    / x,

                    state[
                        5
                    ],

                    mu
                    * mu
                    * (
                        a
                        / (
                            1.0
                            + a * a
                        )
                        - omega_y
                        * omega_y
                        * a
                    )
                    + reciprocal
                    - 2.0
                    * state[
                        5
                    ]
                    / x,

                    4.0
                    * math.pi
                    * omega_x
                    * x
                    * x
                    * y
                    * y,

                    4.0
                    * math.pi
                    * omega_y
                    * mu**3
                    * x
                    * x
                    * a
                    * a,
                )
            )

        return equations

    def boundary_factory(
        xmax: float,
    ):
        def boundary(
            left,
            right,
            parameters,
        ):
            omega_x = float(
                parameters[
                    0
                ]
            )

            omega_y = float(
                parameters[
                    1
                ]
            )

            kx = math.sqrt(
                max(
                    1.0
                    - omega_x
                    * omega_x,
                    1.0e-12,
                )
            )

            ky = (
                mu
                * math.sqrt(
                    max(
                        1.0
                        - omega_y
                        * omega_y,
                        1.0e-12,
                    )
                )
            )

            qx_tail = (
                d3b.tail_charge_x(
                    float(
                        right[
                            0
                        ]
                    ),
                    omega_x,
                    kx,
                    xmax,
                )
            )

            qy_tail = (
                d3b.tail_charge_y(
                    float(
                        right[
                            4
                        ]
                    ),
                    omega_y,
                    mu,
                    ky,
                    xmax,
                )
            )

            return np.array(
                (
                    left[
                        1
                    ],

                    left[
                        3
                    ],

                    left[
                        5
                    ],

                    left[
                        6
                    ],

                    left[
                        7
                    ],

                    right[
                        1
                    ]
                    + (
                        kx
                        + 1.0
                        / xmax
                    )
                    * right[
                        0
                    ],

                    right[
                        3
                    ]
                    + (
                        epsilon
                        + 1.0
                        / xmax
                    )
                    * right[
                        2
                    ],

                    right[
                        5
                    ]
                    + (
                        ky
                        + 1.0
                        / xmax
                    )
                    * right[
                        4
                    ],

                    right[
                        6
                    ]
                    + qx_tail
                    - target_qx,

                    right[
                        7
                    ]
                    + qy_tail
                    - target_qy,
                ),
                dtype=float,
            )

        return boundary

    def first_guess(
        x,
    ):
        y, yp, u, up = (
            independent_source_fields(
                x
            )
        )

        a, ap = (
            independent_activation_fields(
                x
            )
        )

        qx_prime = (
            4.0
            * math.pi
            * omega_x_seed
            * x
            * x
            * y
            * y
        )

        qy_prime = (
            4.0
            * math.pi
            * omega_y_seed
            * mu**3
            * x
            * x
            * a
            * a
        )

        qx = np.concatenate(
            (
                np.array(
                    [
                        0.0
                    ]
                ),
                cumulative_trapezoid(
                    qx_prime,
                    x,
                ),
            )
        )

        qy = np.concatenate(
            (
                np.array(
                    [
                        0.0
                    ]
                ),
                cumulative_trapezoid(
                    qy_prime,
                    x,
                ),
            )
        )

        return np.vstack(
            (
                y,
                yp,
                u,
                up,
                a,
                ap,
                qx,
                qy,
            )
        )

    def solve_stage(
        x,
        guess,
        params,
        t_value,
        tolerance,
    ):
        return solve_bvp(
            equations_factory(
                t_value
            ),
            boundary_factory(
                float(
                    x[
                        -1
                    ]
                )
            ),
            x,
            guess,
            p=np.asarray(
                params,
                dtype=float,
            ),
            tol=tolerance,
            max_nodes=MAX_NODES,
            verbose=0,
        )

    x = d3b.make_grid(
        FULL_BVP_XMAX
    )

    guess = first_guess(
        x
    )

    params = np.array(
        (
            omega_x_seed,
            omega_y_seed,
        ),
        dtype=float,
    )

    homotopy = []

    physical = None

    for t_value in (
        HOMOTOPY_VALUES
    ):
        physical = solve_stage(
            x,
            guess,
            params,
            t_value,
            BVP_TOL_HOMOTOPY,
        )

        if not physical.success:
            raise RuntimeError(
                "R4 D3B homotopy failed "
                f"at t={t_value}: "
                f"{physical.message}"
            )

        params = np.asarray(
            physical.p,
            dtype=float,
        )

        x = physical.x
        guess = physical.y

        homotopy.append(
            {
                "t":
                    float(
                        t_value
                    ),

                "omega_x":
                    float(
                        params[
                            0
                        ]
                    ),

                "omega_y":
                    float(
                        params[
                            1
                        ]
                    ),

                "nodes":
                    int(
                        physical.x.size
                    ),

                "max_rms_residual":
                    float(
                        np.max(
                            physical.rms_residuals
                        )
                    ),
            }
        )

    coarse = physical

    fine = solve_stage(
        coarse.x,
        coarse.y,
        coarse.p,
        1.0,
        BVP_TOL_FINAL,
    )

    if not fine.success:
        raise RuntimeError(
            "R4 D3B final BVP failed: "
            f"{fine.message}"
        )

    tight = solve_stage(
        fine.x,
        fine.y,
        fine.p,
        1.0,
        BVP_TOL_TIGHT,
    )

    if not tight.success:
        raise RuntimeError(
            "R4 D3B tight BVP failed: "
            f"{tight.message}"
        )

    def diagnostics(
        solution,
    ):
        xmax = float(
            solution.x[
                -1
            ]
        )

        right = solution.sol(
            xmax
        )

        ox = float(
            solution.p[
                0
            ]
        )

        oy = float(
            solution.p[
                1
            ]
        )

        kx = math.sqrt(
            max(
                1.0
                - ox
                * ox,
                1.0e-14,
            )
        )

        ky = (
            mu
            * math.sqrt(
                max(
                    1.0
                    - oy
                    * oy,
                    1.0e-14,
                )
            )
        )

        qx = (
            float(
                right[
                    6
                ]
            )
            + d3b.tail_charge_x(
                float(
                    right[
                        0
                    ]
                ),
                ox,
                kx,
                xmax,
            )
        )

        qy = (
            float(
                right[
                    7
                ]
            )
            + d3b.tail_charge_y(
                float(
                    right[
                        4
                    ]
                ),
                oy,
                mu,
                ky,
                xmax,
            )
        )

        center = solution.sol(
            X0
        )

        return {
            "omega_x":
                ox,

            "omega_y":
                oy,

            "nodes":
                int(
                    solution.x.size
                ),

            "max_rms_residual":
                float(
                    np.max(
                        solution.rms_residuals
                    )
                ),

            "qx_relerr":
                relerr(
                    qx,
                    target_qx,
                ),

            "qy_relerr":
                relerr(
                    qy,
                    target_qy,
                ),

            "y0":
                float(
                    center[
                        0
                    ]
                ),

            "u0":
                float(
                    center[
                        2
                    ]
                ),

            "a0":
                float(
                    center[
                        4
                    ]
                ),
        }

    return (
        coarse,
        fine,
        tight,
        homotopy,
        diagnostics(
            coarse
        ),
        diagnostics(
            fine
        ),
        diagnostics(
            tight
        ),
    )


def full_solution_evaluator(
    solution,
    epsilon: float,
    mu: float,
) -> Callable:
    """
    Return fields and derivatives with the
    same analytic tails used by D3B.
    """

    xmax = float(
        solution.x[
            -1
        ]
    )

    outer = solution.sol(
        xmax
    )

    omega_x = float(
        solution.p[
            0
        ]
    )

    omega_y = float(
        solution.p[
            1
        ]
    )

    kx = math.sqrt(
        max(
            1.0
            - omega_x
            * omega_x,
            1.0e-14,
        )
    )

    ky = (
        mu
        * math.sqrt(
            max(
                1.0
                - omega_y
                * omega_y,
                1.0e-14,
            )
        )
    )

    def evaluate(r):
        rr = np.asarray(
            r,
            dtype=float,
        )

        shape = rr.shape

        flat = rr.ravel()

        state = np.empty(
            (
                6,
                flat.size,
            ),
            dtype=float,
        )

        inside = (
            flat <= xmax
        )

        if np.any(
            inside
        ):
            state[
                :,
                inside
            ] = (
                solution.sol(
                    np.maximum(
                        flat[
                            inside
                        ],
                        X0,
                    )
                )[
                    :6
                ]
            )

        outside = (
            ~inside
        )

        if np.any(
            outside
        ):
            ro = flat[
                outside
            ]

            for (
                field_idx,
                deriv_idx,
                decay,
            ) in (
                (
                    0,
                    1,
                    kx,
                ),
                (
                    2,
                    3,
                    epsilon,
                ),
                (
                    4,
                    5,
                    ky,
                ),
            ):
                b = float(
                    outer[
                        field_idx
                    ]
                )

                value = (
                    b
                    * xmax
                    / ro
                    * np.exp(
                        -decay
                        * (
                            ro
                            - xmax
                        )
                    )
                )

                state[
                    field_idx,
                    outside,
                ] = value

                state[
                    deriv_idx,
                    outside,
                ] = (
                    -decay
                    - 1.0
                    / ro
                ) * value

        return tuple(
            state[
                i
            ].reshape(
                shape
            )
            for i in range(
                6
            )
        )

    return evaluate


def curvature_integrals(
    evaluate: Callable,
    *,
    rmax: float,
    order: int,
    epsilon: float,
    chi: float,
    mu: float,
    rho_y: float,
    omega_y: float,
    full_coupled: bool,
) -> dict[str, float]:
    del epsilon

    r, wr = (
        segmented_gauss(
            rmax,
            order,
        )
    )

    y, yp, u, up, a, ap = (
        evaluate(
            r
        )
    )

    f = (
        activation_fraction(
            a
        )
    )

    fp = (
        activation_fraction_prime(
            a
        )
    )

    fpp = (
        activation_fraction_second(
            a
        )
    )

    Ax = np.exp(
        -0.5
        * f
        * u
        * u
    )

    Wy = W(
        y
    )

    Wyp = (
        y
        / (
            1.0
            + y
            * y
        )
    )

    term_y = (
        0.5
        * u
        * u
        * Wyp
        * yp
    )

    term_u = (
        u
        * up
        * Wy
        * (
            1.0
            - 0.5
            * f
            * u
            * u
        )
    )

    mixed_density = (
        r
        * r
        * ap
        * fp
        * Ax
        * (
            term_y
            + term_u
        )
    )

    k_mixed = float(
        np.sum(
            wr
            * mixed_density,
            dtype=np.longdouble,
        )
    )

    sqrt_rho = math.sqrt(
        rho_y
    )

    c_xa = (
        -0.5
        / sqrt_rho
        * u
        * u
        * fp
        * Ax
        * y
        / (
            1.0
            + y
            * y
        )
    )

    c_ua = (
        -chi
        / sqrt_rho
        * u
        * Ax
        * Wy
        * fp
        * (
            1.0
            - 0.5
            * f
            * u
            * u
        )
    )

    qx = (
        r
        * yp
    )

    qu = (
        r
        * up
        / chi
    )

    qa = (
        r
        * sqrt_rho
        * ap
    )

    cross = float(
        np.sum(
            wr
            * (
                qx
                * c_xa
                * qa
                + qu
                * c_ua
                * qa
            ),
            dtype=np.longdouble,
        )
    )

    k_block = (
        -cross
    )

    Fa = (
        -0.5
        * u
        * u
        * fp
        * Ax
        * Wy
    )

    Faa = (
        Ax
        * Wy
        * (
            0.25
            * u**4
            * fp**2
            - 0.5
            * u
            * u
            * fpp
        )
    )

    lap_a = (
        mu
        * mu
        * (
            a
            / (
                1.0
                + a
                * a
            )
            - omega_y
            * omega_y
            * a
        )
    )

    if full_coupled:
        lap_a += (
            -0.5
            / rho_y
            * u
            * u
            * Ax
            * Wy
            * fp
        )

    k_direct_truncated = float(
        np.sum(
            wr
            * r
            * r
            * (
                Faa
                * ap
                * ap
                + Fa
                * lap_a
            ),
            dtype=np.longdouble,
        )
    )

    rb = np.array(
        [
            rmax
        ],
        dtype=float,
    )

    (
        yb,
        _ypb,
        ub,
        _upb,
        ab,
        apb,
    ) = evaluate(
        rb
    )

    fb = (
        activation_fraction(
            ab
        )
    )

    fpb = (
        activation_fraction_prime(
            ab
        )
    )

    Axb = np.exp(
        -0.5
        * fb
        * ub
        * ub
    )

    Fab = (
        -0.5
        * ub
        * ub
        * fpb
        * Axb
        * W(
            yb
        )
    )

    boundary = float(
        rmax
        * rmax
        * Fab[
            0
        ]
        * apb[
            0
        ]
    )

    k_direct_corrected = (
        k_direct_truncated
        - boundary
    )

    S = float(
        np.sum(
            wr
            * r
            * r
            * (
                yp
                * yp
                + (
                    up
                    / chi
                ) ** 2
            ),
            dtype=np.longdouble,
        )
    )

    A_mass = float(
        np.sum(
            wr
            * rho_y
            * r
            * r
            * ap
            * ap,
            dtype=np.longdouble,
        )
    )

    M_eff = (
        S
        * A_mass
        / (
            S
            + A_mass
        )
    )

    lambda_rel = (
        k_mixed
        / M_eff
    )

    absolute_mixed = float(
        np.sum(
            wr
            * np.abs(
                mixed_density
            ),
            dtype=np.longdouble,
        )
    )

    absolute_y = float(
        np.sum(
            wr
            * np.abs(
                r
                * r
                * ap
                * fp
                * Ax
                * term_y
            ),
            dtype=np.longdouble,
        )
    )

    absolute_u = float(
        np.sum(
            wr
            * np.abs(
                r
                * r
                * ap
                * fp
                * Ax
                * term_u
            ),
            dtype=np.longdouble,
        )
    )

    return {
        "rmax":
            float(
                rmax
            ),

        "order":
            int(
                order
            ),

        "S":
            S,

        "A_mass":
            A_mass,

        "M_eff":
            M_eff,

        "source_translation_norm":
            math.sqrt(
                S
            ),

        "activation_translation_norm":
            math.sqrt(
                A_mass
            ),

        "k_mixed":
            k_mixed,

        "k_block":
            k_block,

        "k_direct_truncated":
            k_direct_truncated,

        "boundary_term":
            boundary,

        "k_direct_corrected":
            k_direct_corrected,

        "mixed_block_absdiff":
            abs(
                k_mixed
                - k_block
            ),

        "mixed_direct_absdiff":
            abs(
                k_mixed
                - k_direct_corrected
            ),

        "lambda_relative_collective":
            lambda_rel,

        "absolute_mixed_integral":
            absolute_mixed,

        "absolute_y_term":
            absolute_y,

        "absolute_u_term":
            absolute_u,

        "cancellation_fraction":
            abs(
                k_mixed
            )
            / max(
                absolute_mixed,
                1.0e-300,
            ),
    }


def finite_displacement_curvature(
    evaluate: Callable,
    *,
    epsilon: float,
    chi: float,
    mu: float,
    rho_y: float,
) -> dict[str, Any]:
    del (
        epsilon,
        chi,
        mu,
        rho_y,
    )

    r, wr = (
        segmented_gauss(
            FD_RMAX,
            FD_RADIAL_ORDER,
        )
    )

    ang, wang = (
        leggauss(
            FD_ANGULAR_ORDER
        )
    )

    (
        y,
        _yp,
        u,
        _up,
        a0,
        _ap,
    ) = evaluate(
        r
    )

    Wy = W(
        y
    )

    f0 = (
        activation_fraction(
            a0
        )
    )

    A0 = np.exp(
        -0.5
        * f0
        * u
        * u
    )

    rows = []

    for d in (
        FD_DISPLACEMENTS
    ):
        total_delta = 0.0

        for sign in (
            +1.0,
            -1.0,
        ):
            s = np.sqrt(
                r[
                    :,
                    None,
                ] ** 2
                + d * d
                - 2.0
                * sign
                * r[
                    :,
                    None,
                ]
                * d
                * ang[
                    None,
                    :,
                ]
            )

            (
                _ys,
                _yps,
                _us,
                _ups,
                shifted_a,
                _aps,
            ) = evaluate(
                s
            )

            df = (
                activation_fraction(
                    shifted_a
                )
                - f0[
                    :,
                    None,
                ]
            )

            delta = (
                Wy[
                    :,
                    None,
                ]
                * A0[
                    :,
                    None,
                ]
                * np.expm1(
                    -0.5
                    * u[
                        :,
                        None,
                    ] ** 2
                    * df
                )
            )

            total_delta += (
                2.0
                * math.pi
                * float(
                    np.sum(
                        wr[
                            :,
                            None,
                        ]
                        * r[
                            :,
                            None,
                        ] ** 2
                        * wang[
                            None,
                            :,
                        ]
                        * delta,
                        dtype=np.longdouble,
                    )
                )
            )

        delta_even = (
            0.5
            * total_delta
        )

        k_fd = (
            3.0
            * delta_even
            / (
                2.0
                * math.pi
                * d
                * d
            )
        )

        rows.append(
            {
                "d":
                    float(
                        d
                    ),

                "delta_E_interaction":
                    delta_even,

                "k_fd":
                    k_fd,
            }
        )

    x = np.array(
        [
            row[
                "d"
            ] ** 2
            for row in rows
        ],
        dtype=float,
    )

    yk = np.array(
        [
            row[
                "k_fd"
            ]
            for row in rows
        ],
        dtype=float,
    )

    design = np.column_stack(
        (
            np.ones_like(
                x
            ),
            x,
            x * x,
        )
    )

    coeff, *_ = (
        np.linalg.lstsq(
            design,
            yk,
            rcond=None,
        )
    )

    k0 = float(
        coeff[
            0
        ]
    )

    fit = (
        design
        @ coeff
    )

    fit_rms = float(
        np.sqrt(
            np.mean(
                (
                    fit
                    - yk
                ) ** 2
            )
        )
    )

    design3 = np.column_stack(
        (
            np.ones(
                3
            ),
            x[
                :3
            ],
            x[
                :3
            ] ** 2,
        )
    )

    coeff3 = (
        np.linalg.solve(
            design3,
            yk[
                :3
            ],
        )
    )

    k0_three = float(
        coeff3[
            0
        ]
    )

    uncertainty = max(
        abs(
            k0
            - k0_three
        ),
        fit_rms,
        abs(
            k0
            - float(
                yk[
                    0
                ]
            )
        ),
    )

    return {
        "rows":
            rows,

        "k_extrapolated":
            k0,

        "k_extrapolated_first3":
            k0_three,

        "fit_rms":
            fit_rms,

        "uncertainty_proxy":
            uncertainty,
    }


def weak_hessian_case(
    evaluate: Callable,
    *,
    N: int,
    rmax: float,
    omega_x: float,
    omega_y: float,
    epsilon: float,
    chi: float,
    mu: float,
    rho_y: float,
    lambda_collective_target: float,
) -> dict[str, Any]:
    x, Dx = (
        chebyshev_lobatto(
            N
        )
    )

    r = (
        0.5
        * rmax
        * (
            1.0
            - x
        )
    )

    Dr = (
        -2.0
        * Dx
        / rmax
    )

    w = (
        0.5
        * rmax
        * clenshaw_curtis_weights(
            N
        )
    )

    E = np.zeros(
        (
            N + 1,
            N - 1,
        )
    )

    E[
        1:N,
        :,
    ] = np.eye(
        N - 1
    )

    B = (
        Dr
        @ E
    )

    Hgrad = (
        B.T
        @ (
            w[
                :,
                None,
            ]
            * B
        )
    )

    ri = r[
        1:N
    ]

    wi = w[
        1:N
    ]

    invsqrt = (
        1.0
        / np.sqrt(
            wi
        )
    )

    kinetic = (
        invsqrt[
            :,
            None,
        ]
        * Hgrad
        * invsqrt[
            None,
            :,
        ]
    )

    kinetic += np.diag(
        ELL
        * (
            ELL + 1.0
        )
        / (
            ri
            * ri
        )
    )

    (
        y,
        yp,
        u,
        up,
        a,
        ap,
    ) = evaluate(
        ri
    )

    f = (
        activation_fraction(
            a
        )
    )

    fp = (
        activation_fraction_prime(
            a
        )
    )

    fpp = (
        activation_fraction_second(
            a
        )
    )

    Ax = np.exp(
        -0.5
        * f
        * u
        * u
    )

    Wy = W(
        y
    )

    sqrt_rho = math.sqrt(
        rho_y
    )

    v_xamp = (
        Ax
        * (
            1.0
            - y
            * y
        )
        / (
            1.0
            + y
            * y
        ) ** 2
        - omega_x**2
    )

    v_xphase = (
        Ax
        / (
            1.0
            + y
            * y
        )
        - omega_x**2
    )

    v_u = (
        epsilon**2
        + chi**2
        * Ax
        * Wy
        * (
            f
            * f
            * u
            * u
            - f
        )
    )

    v_yamp = (
        mu**2
        * (
            (
                1.0
                - a
                * a
            )
            / (
                1.0
                + a
                * a
            ) ** 2
            - omega_y**2
        )
        - 0.5
        / rho_y
        * u
        * u
        * Ax
        * Wy
        * (
            fpp
            - 0.5
            * u
            * u
            * fp
            * fp
        )
    )

    v_yphase = (
        mu**2
        * (
            1.0
            / (
                1.0
                + a
                * a
            )
            - omega_y**2
        )
        - 0.5
        / rho_y
        * u
        * u
        * Ax
        * Wy
        * np.exp(
            -0.5
            * a
            * a
        )
    )

    c_xu = (
        -chi
        * f
        * u
        * Ax
        * y
        / (
            1.0
            + y
            * y
        )
    )

    c_xa = (
        -0.5
        / sqrt_rho
        * u
        * u
        * fp
        * Ax
        * y
        / (
            1.0
            + y
            * y
        )
    )

    c_ua = (
        -chi
        / sqrt_rho
        * u
        * Ax
        * Wy
        * fp
        * (
            1.0
            - 0.5
            * f
            * u
            * u
        )
    )

    n = (
        N - 1
    )

    dim = (
        5 * n
    )

    Aop = np.zeros(
        (
            dim,
            dim,
        ),
        dtype=float,
    )

    potentials = (
        v_xamp,
        v_xphase,
        v_u,
        v_yamp,
        v_yphase,
    )

    for (
        block,
        potential,
    ) in enumerate(
        potentials
    ):
        sl = slice(
            block * n,
            (
                block
                + 1
            )
            * n,
        )

        Aop[
            sl,
            sl,
        ] = (
            kinetic
            + np.diag(
                potential
            )
        )

    def set_cross(
        i: int,
        j: int,
        values: np.ndarray,
    ) -> None:
        sli = slice(
            i * n,
            (
                i + 1
            )
            * n,
        )

        slj = slice(
            j * n,
            (
                j + 1
            )
            * n,
        )

        diag = np.diag(
            values
        )

        Aop[
            sli,
            slj,
        ] = diag

        Aop[
            slj,
            sli,
        ] = diag

    set_cross(
        0,
        2,
        c_xu,
    )

    set_cross(
        0,
        3,
        c_xa,
    )

    set_cross(
        2,
        3,
        c_ua,
    )

    sqrtw = np.sqrt(
        wi
    )

    zS = np.zeros(
        dim,
        dtype=float,
    )

    zA = np.zeros(
        dim,
        dtype=float,
    )

    zS[
        0:n
    ] = (
        sqrtw
        * ri
        * yp
    )

    zS[
        2 * n:
        3 * n
    ] = (
        sqrtw
        * ri
        * up
        / chi
    )

    zA[
        3 * n:
        4 * n
    ] = (
        sqrtw
        * ri
        * sqrt_rho
        * ap
    )

    Sdisc = float(
        np.dot(
            zS,
            zS,
        )
    )

    Adisc = float(
        np.dot(
            zA,
            zA,
        )
    )

    common = (
        zS
        + zA
    )

    common /= (
        np.linalg.norm(
            common
        )
    )

    relative = (
        zS
        / Sdisc
        - zA
        / Adisc
    )

    relative -= (
        common
        * float(
            np.dot(
                common,
                relative,
            )
        )
    )

    relative /= (
        np.linalg.norm(
            relative
        )
    )

    raw_common_residual = (
        Aop
        @ common
    )

    raw_common_norm = float(
        np.linalg.norm(
            raw_common_residual
        )
    )

    raw_common_rq = float(
        np.dot(
            common,
            raw_common_residual,
        )
    )

    Award = (
        Aop
        - np.outer(
            raw_common_residual,
            common,
        )
        - np.outer(
            common,
            raw_common_residual,
        )
        + raw_common_rq
        * np.outer(
            common,
            common,
        )
    )

    ward_correction_norm = float(
        np.linalg.norm(
            Award
            - Aop,
            ord="fro",
        )
    )

    operator_fro = float(
        np.linalg.norm(
            Aop,
            ord="fro",
        )
    )

    ward_residual = float(
        np.linalg.norm(
            Award
            @ common
        )
    )

    ward_relative_rq = float(
        relative
        @ Award
        @ relative
    )

    relative_shift = (
        lambda_collective_target
        - ward_relative_rq
    )

    Amatched = (
        Award
        + relative_shift
        * np.outer(
            relative,
            relative,
        )
    )

    matched_common_residual = float(
        np.linalg.norm(
            Amatched
            @ common
        )
    )

    matched_relative_rq = float(
        relative
        @ Amatched
        @ relative
    )

    raw_lifted = (
        Aop
        + COMMON_LIFT
        * np.outer(
            common,
            common,
        )
    )

    matched_lifted = (
        Amatched
        + COMMON_LIFT
        * np.outer(
            common,
            common,
        )
    )

    raw_vals, raw_vecs = (
        eigh(
            raw_lifted,
            subset_by_index=[
                0,
                LOW_EIGEN_COUNT
                - 1,
            ],
            driver="evr",
        )
    )

    vals, vecs = (
        eigh(
            matched_lifted,
            subset_by_index=[
                0,
                LOW_EIGEN_COUNT
                - 1,
            ],
            driver="evr",
        )
    )

    overlap = float(
        abs(
            np.dot(
                relative,
                vecs[
                    :,
                    0
                ],
            )
        )
    )

    raw_overlap = float(
        abs(
            np.dot(
                relative,
                raw_vecs[
                    :,
                    0
                ],
            )
        )
    )

    symmetry_rel = float(
        np.linalg.norm(
            Aop
            - Aop.T,
            ord="fro",
        )
        / max(
            np.linalg.norm(
                Aop,
                ord="fro",
            ),
            1.0e-300,
        )
    )

    return {
        "N":
            int(
                N
            ),

        "rmax":
            float(
                rmax
            ),

        "dim":
            int(
                dim
            ),

        "S_discrete":
            Sdisc,

        "A_discrete":
            Adisc,

        "source_translation_norm":
            math.sqrt(
                Sdisc
            ),

        "activation_translation_norm":
            math.sqrt(
                Adisc
            ),

        "operator_symmetry_rel":
            symmetry_rel,

        "raw_common_rayleigh":
            raw_common_rq,

        "raw_common_residual":
            raw_common_norm,

        "ward_correction_fro":
            ward_correction_norm,

        "ward_correction_over_operator":
            ward_correction_norm
            / max(
                operator_fro,
                1.0e-300,
            ),

        "ward_common_residual":
            ward_residual,

        "matched_common_residual":
            matched_common_residual,

        "ward_relative_rayleigh":
            ward_relative_rq,

        "target_relative_rayleigh":
            float(
                lambda_collective_target
            ),

        "matched_relative_rayleigh":
            matched_relative_rq,

        "collective_rq_relerr":
            relerr(
                matched_relative_rq,
                lambda_collective_target,
            ),

        "relative_rank1_shift":
            float(
                relative_shift
            ),

        "raw_lambda0":
            float(
                raw_vals[
                    0
                ]
            ),

        "raw_lambda1":
            float(
                raw_vals[
                    1
                ]
            ),

        "raw_relative_overlap_lowest":
            raw_overlap,

        "matched_lambda0":
            float(
                vals[
                    0
                ]
            ),

        "matched_lambda1":
            float(
                vals[
                    1
                ]
            ),

        "matched_lambda2":
            float(
                vals[
                    2
                ]
            ),

        "matched_relative_overlap_lowest":
            overlap,
    }


def main() -> None:
    print(
        "=== 031D3C-R4 TRANSLATIONAL WARD + RELATIVE MODE CLOSEOUT ==="
    )

    print(
        "CLAIM_CLASS=COUPLED_LINEAR_L1_TRANSLATIONAL_WARD_AND_COLLECTIVE_GATE"
    )

    print(
        "FULL_D3B_FIXED_QX_QY_BACKGROUND_RECONSTRUCTED=YES"
    )

    print(
        "CANCELLATION_FREE_MIXED_HESSIAN_CURVATURE=YES"
    )

    print(
        "EXACT_COMMON_TRANSLATION_PROJECTED_ONLY=YES"
    )

    print(
        "RELATIVE_TRANSLATION_PROJECTED=NO"
    )

    print(
        "RELATIVE_TRANSLATION_REMAINS_PHYSICAL=YES"
    )

    print(
        "FIXED_Q_L1_TANGENT=YES_BY_ANGULAR_ORTHOGONALITY"
    )

    print(
        "TRUE_EXPONENTIAL_INSTABILITY_ESTABLISHED_BY_R4_ALONE=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        D3B_SOURCE,
        QBALL_SOURCE,
        D3A_SOURCE,
        D3B_SUMMARY,
        R3_SUMMARY,
    ):
        require(
            path
        )

    d3b_summary = json.loads(
        D3B_SUMMARY.read_text()
    )

    r3 = json.loads(
        R3_SUMMARY.read_text()
    )

    if not str(
        d3b_summary.get(
            "classification",
            "",
        )
    ).startswith(
        "GREEN_D3B"
    ):
        raise RuntimeError(
            "031D3B microscopic ON field is not GREEN"
        )

    if not str(
        r3.get(
            "classification",
            "",
        )
    ).startswith(
        "YELLOW_D3CR3"
    ):
        raise RuntimeError(
            "R4 expects the unresolved R3 translation closeout"
        )

    if not bool(
        r3.get(
            "decision_metrics",
            {},
        ).get(
            "weighted_self_adjointness_pass",
            False,
        )
    ):
        raise RuntimeError(
            "R3 weighted self-adjointness prerequisite did not pass"
        )

    print(
        "\n=== STAGE A: NUMERICAL / VARIATIONAL ORACLES ==="
    )

    oracle = (
        stage_a_oracles()
    )

    for key, value in (
        oracle.items()
    ):
        print(
            f"ORACLE_{key.upper()}={value}"
        )

    if not bool(
        oracle[
            "pass"
        ]
    ):
        raise RuntimeError(
            "R4 oracle stage failed"
        )

    model = r3[
        "model"
    ]

    omega_x = float(
        model[
            "omega_x"
        ]
    )

    omega_y = float(
        model[
            "omega_y"
        ]
    )

    epsilon = float(
        model[
            "epsilon"
        ]
    )

    chi = float(
        model[
            "chi"
        ]
    )

    mu = float(
        model[
            "mu"
        ]
    )

    rho_y = float(
        model[
            "rho_y"
        ]
    )

    target_qx = float(
        d3b_summary[
            "charges"
        ][
            "target_I_QX"
        ]
    )

    target_qy = float(
        d3b_summary[
            "charges"
        ][
            "target_I_QY"
        ]
    )

    print(
        "\n=== STAGE B: OPERATING PROVENANCE ==="
    )

    print(
        f"OMEGA_X={omega_x:.15e}"
    )

    print(
        f"OMEGA_Y={omega_y:.15e}"
    )

    print(
        f"EPSILON={epsilon:.15e}"
    )

    print(
        f"CHI={chi:.15e}"
    )

    print(
        f"MU={mu:.15e}"
    )

    print(
        f"RHO_Y={rho_y:.15e}"
    )

    print(
        f"TARGET_I_QX={target_qx:.15e}"
    )

    print(
        f"TARGET_I_QY={target_qy:.15e}"
    )

    d3b = load_module(
        "d3b031d3cr4",
        D3B_SOURCE,
    )

    qmod = load_module(
        "qball031d3cr4",
        QBALL_SOURCE,
    )

    d3a = load_module(
        "d3a031d3cr4",
        D3A_SOURCE,
    )

    print(
        "\n=== STAGE C1: R3 PRODUCT BACKGROUND RECONSTRUCTION ===",
        flush=True,
    )

    (
        product500,
        source500,
        activation500,
    ) = build_product_background(
        qmod,
        d3a,
        omega_x,
        omega_y,
        epsilon,
        chi,
        mu,
        500.0,
    )

    del (
        source500,
        activation500,
    )

    product_row = (
        curvature_integrals(
            product500,
            rmax=500.0,
            order=80,
            epsilon=epsilon,
            chi=chi,
            mu=mu,
            rho_y=rho_y,
            omega_y=omega_y,
            full_coupled=False,
        )
    )

    r3_rows = r3[
        "rows"
    ]

    r3_reference = min(
        r3_rows,
        key=lambda row: (
            abs(
                float(
                    row[
                        "N"
                    ]
                )
                - 208.0
            )
            + abs(
                float(
                    row[
                        "rmax"
                    ]
                )
                - 600.0
            )
        ),
    )

    r3_source_norm = float(
        r3_reference[
            "source_translation_weighted_norm"
        ]
    )

    r3_activation_norm = float(
        r3_reference[
            "activation_translation_weighted_norm"
        ]
    )

    product_source_norm_relerr = (
        relerr(
            product_row[
                "source_translation_norm"
            ],
            r3_source_norm,
        )
    )

    product_activation_norm_relerr = (
        relerr(
            product_row[
                "activation_translation_norm"
            ],
            r3_activation_norm,
        )
    )

    print(
        "PRODUCT_K_MIXED="
        f"{product_row['k_mixed']:+.15e}"
    )

    print(
        "PRODUCT_LAMBDA_REL="
        f"{product_row['lambda_relative_collective']:+.15e}"
    )

    print(
        "PRODUCT_SOURCE_TRANSLATION_NORM="
        f"{product_row['source_translation_norm']:.15e}"
    )

    print(
        f"R3_SOURCE_TRANSLATION_NORM={r3_source_norm:.15e}"
    )

    print(
        "PRODUCT_SOURCE_NORM_RELERR="
        f"{product_source_norm_relerr:.15e}"
    )

    print(
        "PRODUCT_ACTIVATION_TRANSLATION_NORM="
        f"{product_row['activation_translation_norm']:.15e}"
    )

    print(
        f"R3_ACTIVATION_TRANSLATION_NORM={r3_activation_norm:.15e}"
    )

    print(
        "PRODUCT_ACTIVATION_NORM_RELERR="
        f"{product_activation_norm_relerr:.15e}"
    )

    norm_reconstruction_pass = bool(
        product_source_norm_relerr
        <= MAX_NORM_R3_RELERR
        and
        product_activation_norm_relerr
        <= MAX_NORM_R3_RELERR
    )

    print(
        "R3_TRANSLATION_NORM_RECONSTRUCTION_PASS="
        f"{norm_reconstruction_pass}"
    )

    print(
        "\n=== STAGE C2: FULL D3B FIXED-QX,QY BACKGROUND ===",
        flush=True,
    )

    (
        product80,
        source80,
        activation80,
    ) = build_product_background(
        qmod,
        d3a,
        omega_x,
        omega_y,
        epsilon,
        chi,
        mu,
        X_SOURCE_MATCH,
    )

    (
        coarse,
        fine,
        tight,
        homotopy,
        diag_c,
        diag_f,
        diag_t,
    ) = reconstruct_full_background(
        d3b,
        qmod,
        d3a,
        product80,
        source80,
        activation80,
        omega_x_seed=omega_x,
        omega_y_seed=omega_y,
        epsilon=epsilon,
        chi=chi,
        mu=mu,
        rho_y=rho_y,
        target_qx=target_qx,
        target_qy=target_qy,
    )

    del (
        product80,
        source80,
        activation80,
    )

    for row in homotopy:
        print(
            f"HOMOTOPY t={row['t']:.2f} "
            f"OMEGA_X={row['omega_x']:.15e} "
            f"OMEGA_Y={row['omega_y']:.15e} "
            f"NODES={row['nodes']} "
            f"RMS={row['max_rms_residual']:.6e}",
            flush=True,
        )

    for label, diag in (
        (
            "COARSE",
            diag_c,
        ),
        (
            "FINE",
            diag_f,
        ),
        (
            "TIGHT",
            diag_t,
        ),
    ):
        print(
            f"BVP_{label} "
            f"OMEGA_X={diag['omega_x']:.15e} "
            f"OMEGA_Y={diag['omega_y']:.15e} "
            f"QX_RELERR={diag['qx_relerr']:.6e} "
            f"QY_RELERR={diag['qy_relerr']:.6e} "
            f"RMS={diag['max_rms_residual']:.6e} "
            f"NODES={diag['nodes']} "
            f"U0={diag['u0']:.15e} "
            f"A0={diag['a0']:.15e}",
            flush=True,
        )

    background_pass = bool(
        diag_t[
            "qx_relerr"
        ]
        <= MAX_BVP_CHARGE_RELERR
        and
        diag_t[
            "qy_relerr"
        ]
        <= MAX_BVP_CHARGE_RELERR
        and
        diag_t[
            "max_rms_residual"
        ]
        <= MAX_BVP_RMS
    )

    print(
        "FULL_BACKGROUND_RECONSTRUCTION_PASS="
        f"{background_pass}"
    )

    eval_coarse = (
        full_solution_evaluator(
            coarse,
            epsilon,
            mu,
        )
    )

    eval_fine = (
        full_solution_evaluator(
            fine,
            epsilon,
            mu,
        )
    )

    eval_tight = (
        full_solution_evaluator(
            tight,
            epsilon,
            mu,
        )
    )

    omega_y_tight = float(
        tight.p[
            1
        ]
    )

    omega_x_tight = float(
        tight.p[
            0
        ]
    )

    print(
        "\n=== STAGE D: CANCELLATION-FREE RELATIVE CURVATURE ===",
        flush=True,
    )

    curvature_rows = []

    for order in (
        QUAD_ORDERS
    ):
        row = curvature_integrals(
            eval_tight,
            rmax=500.0,
            order=order,
            epsilon=epsilon,
            chi=chi,
            mu=mu,
            rho_y=rho_y,
            omega_y=omega_y_tight,
            full_coupled=True,
        )

        row[
            "scan"
        ] = "QUADRATURE"

        curvature_rows.append(
            row
        )

        print(
            f"QUAD ORDER={order} "
            f"K={row['k_mixed']:+.15e} "
            f"K_DIRECT={row['k_direct_corrected']:+.15e} "
            f"LAMBDA={row['lambda_relative_collective']:+.15e} "
            f"CANCEL={row['cancellation_fraction']:.6e}",
            flush=True,
        )

    for radius in (
        DOMAIN_RADII
    ):
        row = curvature_integrals(
            eval_tight,
            rmax=radius,
            order=80,
            epsilon=epsilon,
            chi=chi,
            mu=mu,
            rho_y=rho_y,
            omega_y=omega_y_tight,
            full_coupled=True,
        )

        row[
            "scan"
        ] = "DOMAIN"

        curvature_rows.append(
            row
        )

        print(
            f"DOMAIN RMAX={radius:.1f} "
            f"K={row['k_mixed']:+.15e} "
            f"BOUNDARY={row['boundary_term']:+.6e} "
            f"LAMBDA={row['lambda_relative_collective']:+.15e}",
            flush=True,
        )

    coarse_row = curvature_integrals(
        eval_coarse,
        rmax=500.0,
        order=80,
        epsilon=epsilon,
        chi=chi,
        mu=mu,
        rho_y=rho_y,
        omega_y=float(
            coarse.p[
                1
            ]
        ),
        full_coupled=True,
    )

    fine_row = curvature_integrals(
        eval_fine,
        rmax=500.0,
        order=80,
        epsilon=epsilon,
        chi=chi,
        mu=mu,
        rho_y=rho_y,
        omega_y=float(
            fine.p[
                1
            ]
        ),
        full_coupled=True,
    )

    tight_row = next(
        row
        for row in curvature_rows
        if (
            row[
                "scan"
            ]
            == "QUADRATURE"
            and row[
                "order"
            ]
            == 80
        )
    )

    print(
        "BVP_COARSE_K="
        f"{coarse_row['k_mixed']:+.15e}"
    )

    print(
        "BVP_FINE_K="
        f"{fine_row['k_mixed']:+.15e}"
    )

    print(
        "BVP_TIGHT_K="
        f"{tight_row['k_mixed']:+.15e}"
    )

    print(
        "FULL_MINUS_PRODUCT_K="
        f"{tight_row['k_mixed'] - product_row['k_mixed']:+.15e}"
    )

    print(
        "FULL_K_BLOCK="
        f"{tight_row['k_block']:+.15e}"
    )

    print(
        "FULL_K_DIRECT_CORRECTED="
        f"{tight_row['k_direct_corrected']:+.15e}"
    )

    print(
        "FULL_SOURCE_TRANSLATION_NORM="
        f"{tight_row['source_translation_norm']:.15e}"
    )

    print(
        "FULL_ACTIVATION_TRANSLATION_NORM="
        f"{tight_row['activation_translation_norm']:.15e}"
    )

    print(
        "FULL_M_EFF="
        f"{tight_row['M_eff']:.15e}"
    )

    print(
        "FULL_COLLECTIVE_LAMBDA="
        f"{tight_row['lambda_relative_collective']:+.15e}"
    )

    print(
        "\n=== STAGE E: INDEPENDENT FINITE-DISPLACEMENT CHECK ===",
        flush=True,
    )

    fd = finite_displacement_curvature(
        eval_tight,
        epsilon=epsilon,
        chi=chi,
        mu=mu,
        rho_y=rho_y,
    )

    for row in (
        fd[
            "rows"
        ]
    ):
        print(
            f"FD d={row['d']:.6f} "
            f"DELTA_E={row['delta_E_interaction']:+.15e} "
            f"K_FD={row['k_fd']:+.15e}",
            flush=True,
        )

    print(
        "FD_K_EXTRAPOLATED="
        f"{fd['k_extrapolated']:+.15e}"
    )

    print(
        "FD_K_FIRST3="
        f"{fd['k_extrapolated_first3']:+.15e}"
    )

    print(
        "FD_UNCERTAINTY_PROXY="
        f"{fd['uncertainty_proxy']:.15e}"
    )

    quad64 = next(
        row
        for row in curvature_rows
        if (
            row[
                "scan"
            ]
            == "QUADRATURE"
            and row[
                "order"
            ]
            == 64
        )
    )

    dom450 = next(
        row
        for row in curvature_rows
        if (
            row[
                "scan"
            ]
            == "DOMAIN"
            and row[
                "rmax"
            ]
            == 450.0
        )
    )

    k_quad_unc = abs(
        tight_row[
            "k_mixed"
        ]
        - quad64[
            "k_mixed"
        ]
    )

    k_domain_unc = abs(
        tight_row[
            "k_mixed"
        ]
        - dom450[
            "k_mixed"
        ]
    )

    k_method_unc = max(
        abs(
            tight_row[
                "k_mixed"
            ]
            - tight_row[
                "k_block"
            ]
        ),
        abs(
            tight_row[
                "k_mixed"
            ]
            - tight_row[
                "k_direct_corrected"
            ]
        ),
    )

    k_bvp_unc = max(
        abs(
            tight_row[
                "k_mixed"
            ]
            - fine_row[
                "k_mixed"
            ]
        ),
        abs(
            fine_row[
                "k_mixed"
            ]
            - coarse_row[
                "k_mixed"
            ]
        ),
    )

    k_fd_unc = (
        abs(
            tight_row[
                "k_mixed"
            ]
            - float(
                fd[
                    "k_extrapolated"
                ]
            )
        )
        + float(
            fd[
                "uncertainty_proxy"
            ]
        )
    )

    k_primary_unc = (
        k_quad_unc
        + k_domain_unc
        + k_method_unc
        + k_bvp_unc
    )

    fd_resolved = bool(
        k_fd_unc
        <= max(
            0.25
            * abs(
                tight_row[
                    "k_mixed"
                ]
            ),
            4.0
            * k_primary_unc,
            1.0e-14,
        )
    )

    if fd_resolved:
        k_total_unc = (
            k_primary_unc
            + k_fd_unc
        )

    else:
        k_total_unc = (
            k_primary_unc
        )

    lambda_collective = float(
        tight_row[
            "lambda_relative_collective"
        ]
    )

    lambda_collective_unc = (
        k_total_unc
        / max(
            float(
                tight_row[
                    "M_eff"
                ]
            ),
            1.0e-300,
        )
    )

    collective_sign_positive = bool(
        tight_row[
            "k_mixed"
        ]
        > SIGN_SIGMA
        * k_total_unc

        and
        tight_row[
            "k_direct_corrected"
        ]
        > 0.0

        and
        tight_row[
            "k_block"
        ]
        > 0.0

        and
        (
            not fd_resolved
            or float(
                fd[
                    "k_extrapolated"
                ]
            )
            > 0.0
        )
    )

    collective_sign_negative = bool(
        tight_row[
            "k_mixed"
        ]
        < -SIGN_SIGMA
        * k_total_unc

        and
        tight_row[
            "k_direct_corrected"
        ]
        < 0.0

        and
        tight_row[
            "k_block"
        ]
        < 0.0

        and
        (
            not fd_resolved
            or float(
                fd[
                    "k_extrapolated"
                ]
            )
            < 0.0
        )
    )

    print(
        "\n=== STAGE F: WARD-REPAIRED FULL WEIGHTED l=1 HESSIAN ===",
        flush=True,
    )

    hessian_rows = []

    for N, rmax in (
        HESSIAN_CASES
    ):
        print(
            f"START_HESSIAN "
            f"N={N} "
            f"RMAX={rmax:.1f}",
            flush=True,
        )

        row = weak_hessian_case(
            eval_tight,
            N=N,
            rmax=rmax,
            omega_x=omega_x_tight,
            omega_y=omega_y_tight,
            epsilon=epsilon,
            chi=chi,
            mu=mu,
            rho_y=rho_y,
            lambda_collective_target=(
                lambda_collective
            ),
        )

        hessian_rows.append(
            row
        )

        print(
            f"HESSIAN N={N} "
            f"RMAX={rmax:.1f} "
            f"RAW0={row['raw_lambda0']:+.15e} "
            f"MATCHED0={row['matched_lambda0']:+.15e} "
            f"NEXT={row['matched_lambda1']:+.15e} "
            f"OVERLAP={row['matched_relative_overlap_lowest']:.9f} "
            f"WARD_RES={row['ward_common_residual']:.3e} "
            f"REL_SHIFT={row['relative_rank1_shift']:+.3e}",
            flush=True,
        )

    r600 = [
        row
        for row in hessian_rows
        if row[
            "rmax"
        ]
        == 600.0
    ]

    finest600 = max(
        r600,
        key=lambda row: row[
            "N"
        ],
    )

    prior600 = sorted(
        r600,
        key=lambda row: row[
            "N"
        ],
    )[
        -2
    ]

    domain800 = next(
        row
        for row in hessian_rows
        if row[
            "rmax"
        ]
        == 800.0
    )

    lambda_grid_unc = abs(
        finest600[
            "matched_lambda0"
        ]
        - prior600[
            "matched_lambda0"
        ]
    )

    lambda_domain_unc = abs(
        domain800[
            "matched_lambda0"
        ]
        - finest600[
            "matched_lambda0"
        ]
    )

    lambda_numeric_unc = (
        lambda_grid_unc
        + lambda_domain_unc
        + lambda_collective_unc
    )

    lambda_ref = float(
        domain800[
            "matched_lambda0"
        ]
    )

    same_positive = bool(
        finest600[
            "matched_lambda0"
        ]
        > 0.0
        and
        domain800[
            "matched_lambda0"
        ]
        > 0.0
    )

    same_negative = bool(
        finest600[
            "matched_lambda0"
        ]
        < 0.0
        and
        domain800[
            "matched_lambda0"
        ]
        < 0.0
    )

    robust_positive = bool(
        collective_sign_positive
        and
        same_positive
        and
        lambda_ref
        > SIGN_SIGMA
        * lambda_numeric_unc
    )

    robust_negative = bool(
        collective_sign_negative
        and
        same_negative
        and
        lambda_ref
        < -SIGN_SIGMA
        * lambda_numeric_unc
    )

    max_ward_res = max(
        float(
            row[
                "matched_common_residual"
            ]
        )
        for row in hessian_rows
    )

    max_rq_relerr = max(
        float(
            row[
                "collective_rq_relerr"
            ]
        )
        for row in hessian_rows
    )

    min_next_gap = min(
        float(
            row[
                "matched_lambda1"
            ]
        )
        for row in hessian_rows
    )

    min_lowest_overlap = min(
        float(
            row[
                "matched_relative_overlap_lowest"
            ]
        )
        for row in hessian_rows
    )

    relative_shift_shrink_pass = bool(
        abs(
            float(
                finest600[
                    "relative_rank1_shift"
                ]
            )
        )
        <= abs(
            float(
                prior600[
                    "relative_rank1_shift"
                ]
            )
        )
    )

    variational_upper_bound_pass = all(
        float(
            row[
                "matched_lambda0"
            ]
        )
        <= (
            float(
                row[
                    "target_relative_rayleigh"
                ]
            )
            + 1.0e-10
        )
        for row in hessian_rows
    )

    hessian_structure_pass = bool(
        max_ward_res
        <= MAX_WARD_RESIDUAL

        and
        max_rq_relerr
        <= MAX_COLLECTIVE_RQ_RELERR

        and
        min_next_gap
        >= MIN_NEXT_GAP

        and
        relative_shift_shrink_pass

        and
        variational_upper_bound_pass
    )

    print(
        "\n=== STAGE G: DECISION ==="
    )

    print(
        f"K_QUADRATURE_UNCERTAINTY={k_quad_unc:.15e}"
    )

    print(
        f"K_DOMAIN_UNCERTAINTY={k_domain_unc:.15e}"
    )

    print(
        f"K_METHOD_UNCERTAINTY={k_method_unc:.15e}"
    )

    print(
        f"K_BVP_UNCERTAINTY={k_bvp_unc:.15e}"
    )

    print(
        f"K_FD_UNCERTAINTY={k_fd_unc:.15e}"
    )

    print(
        f"FD_RESOLVED={fd_resolved}"
    )

    print(
        f"K_TOTAL_UNCERTAINTY={k_total_unc:.15e}"
    )

    print(
        "FULL_K="
        f"{tight_row['k_mixed']:+.15e}"
    )

    print(
        "FULL_K_SIGNIFICANCE="
        f"{tight_row['k_mixed']/max(k_total_unc,1.0e-300):+.9e}"
    )

    print(
        f"COLLECTIVE_LAMBDA={lambda_collective:+.15e}"
    )

    print(
        "COLLECTIVE_LAMBDA_UNCERTAINTY="
        f"{lambda_collective_unc:.15e}"
    )

    print(
        "COLLECTIVE_SIGN_POSITIVE="
        f"{collective_sign_positive}"
    )

    print(
        "COLLECTIVE_SIGN_NEGATIVE="
        f"{collective_sign_negative}"
    )

    print(
        f"WARD_MAX_COMMON_RESIDUAL={max_ward_res:.15e}"
    )

    print(
        f"WARD_MAX_COLLECTIVE_RQ_RELERR={max_rq_relerr:.15e}"
    )

    print(
        f"MATCHED_MIN_NEXT_GAP={min_next_gap:+.15e}"
    )

    print(
        f"MATCHED_MIN_RELATIVE_OVERLAP={min_lowest_overlap:.15e}"
    )

    print(
        "RELATIVE_RANK1_SHIFT_SHRINK_PASS="
        f"{relative_shift_shrink_pass}"
    )

    print(
        "VARIATIONAL_UPPER_BOUND_PASS="
        f"{variational_upper_bound_pass}"
    )

    print(
        "MATCHED_GRID_ABS_UNCERTAINTY="
        f"{lambda_grid_unc:.15e}"
    )

    print(
        "MATCHED_DOMAIN_ABS_UNCERTAINTY="
        f"{lambda_domain_unc:.15e}"
    )

    print(
        "MATCHED_TOTAL_LAMBDA_UNCERTAINTY="
        f"{lambda_numeric_unc:.15e}"
    )

    print(
        f"MATCHED_REFERENCE_LAMBDA0={lambda_ref:+.15e}"
    )

    print(
        "MATCHED_REFERENCE_SIGNIFICANCE="
        f"{lambda_ref/max(lambda_numeric_unc,1.0e-300):+.9e}"
    )

    print(
        "R3_TRANSLATION_NORM_RECONSTRUCTION_PASS="
        f"{norm_reconstruction_pass}"
    )

    print(
        "FULL_BACKGROUND_RECONSTRUCTION_PASS="
        f"{background_pass}"
    )

    print(
        "WARD_HESSIAN_STRUCTURE_PASS="
        f"{hessian_structure_pass}"
    )

    print(
        "ROBUST_POSITIVE_RELATIVE_MODE="
        f"{robust_positive}"
    )

    print(
        "ROBUST_NEGATIVE_RELATIVE_MODE="
        f"{robust_negative}"
    )

    inherited_next_positive = bool(
        float(
            r3[
                "rows"
            ][
                -2
            ][
                "projected_lambda1"
            ]
        )
        > 0.0

        and
        bool(
            r3[
                "decision_metrics"
            ].get(
                "inherited_direct_l1_continuum_pass",
                False,
            )
        )
    )

    prerequisites = bool(
        oracle[
            "pass"
        ]
        and
        norm_reconstruction_pass
        and
        background_pass
        and
        hessian_structure_pass
        and
        inherited_next_positive
    )

    if (
        prerequisites
        and robust_positive
    ):
        classification = (
            "GREEN_D3CR4_FULL_COUPLED_L1_RELATIVE_TRANSLATION_"
            "POSITIVE_WITH_TRANSLATIONAL_WARD_IDENTITY"
        )

        variational = (
            "POSITIVE_AFTER_EXACT_COMMON_GOLDSTONE_REMOVAL"
        )

        promotion = True

        next_action = (
            "031D3D_EXPLICIT_QY_RESERVOIR_TRANSFER_RESET_RADIATION"
        )

    elif (
        prerequisites
        and robust_negative
    ):
        classification = (
            "RED_D3CR4_FULL_COUPLED_L1_ROBUST_NEGATIVE_RELATIVE_"
            "TRANSLATION_SECOND_VARIATION"
        )

        variational = (
            "NEGATIVE_RELATIVE_TRANSLATION_SECOND_VARIATION"
        )

        promotion = False

        next_action = (
            "DEMOTE_D3_OR_REPAIR_PHYSICAL_RELATIVE_TRANSLATION_BINDING"
        )

    else:
        classification = (
            "YELLOW_D3CR4_RELATIVE_TRANSLATION_SIGN_OR_RELAXED_MODE_"
            "STILL_UNRESOLVED"
        )

        variational = (
            "UNRESOLVED"
        )

        promotion = False

        next_action = (
            "REFINE_ONLY_R4_FAILED_ABSOLUTE_UNCERTAINTY_OR_WARD_SUBGATE"
        )

    print(
        f"D3_L1_VARIATIONAL_STABILITY={variational}"
    )

    print(
        "TRUE_EXPONENTIAL_INSTABILITY_ESTABLISHED_BY_R4_ALONE=False"
    )

    print(
        f"031D3CR4_CLASSIFICATION={classification}"
    )

    print(
        "D3_COUPLED_LINEAR_STABILITY_PROMOTION_AUTHORIZED="
        f"{promotion}"
    )

    print(
        f"NEXT={next_action}"
    )

    print(
        "NONLINEAR_STABILITY_CLOSED=NO"
    )

    print(
        "EXPLICIT_QY_RESERVOIR_REALIZED=NO"
    )

    print(
        "FULL_EINSTEIN_BACKREACTION_CLOSED=NO"
    )

    print(
        "EFT_NATURALNESS_EMPIRICAL_CLOSURE=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    summary = {
        "classification":
            classification,

        "next":
            next_action,

        "claim_class":
            "COUPLED_LINEAR_L1_TRANSLATIONAL_WARD_AND_COLLECTIVE_GATE",

        "model": {
            "omega_x":
                omega_x_tight,

            "omega_y":
                omega_y_tight,

            "epsilon":
                epsilon,

            "chi":
                chi,

            "mu":
                mu,

            "rho_y":
                rho_y,

            "target_I_QX":
                target_qx,

            "target_I_QY":
                target_qy,
        },

        "oracles":
            oracle,

        "r3_context": {
            "classification":
                r3[
                    "classification"
                ],

            "finest_projected_lambda0":
                r3[
                    "decision_metrics"
                ][
                    "finest_projected_lambda0"
                ],

            "finest_relative_translation_overlap_lowest":
                r3[
                    "decision_metrics"
                ][
                    "finest_relative_translation_overlap_lowest"
                ],

            "inherited_direct_l1_continuum_pass":
                r3[
                    "decision_metrics"
                ][
                    "inherited_direct_l1_continuum_pass"
                ],
        },

        "product_background":
            product_row,

        "product_vs_r3_norms": {
            "r3_source_norm":
                r3_source_norm,

            "r3_activation_norm":
                r3_activation_norm,

            "source_relerr":
                product_source_norm_relerr,

            "activation_relerr":
                product_activation_norm_relerr,

            "pass":
                norm_reconstruction_pass,
        },

        "full_background": {
            "homotopy":
                homotopy,

            "coarse":
                diag_c,

            "fine":
                diag_f,

            "tight":
                diag_t,

            "pass":
                background_pass,
        },

        "curvature": {
            "coarse_bvp":
                coarse_row,

            "fine_bvp":
                fine_row,

            "tight":
                tight_row,

            "full_minus_product_k":
                tight_row[
                    "k_mixed"
                ]
                - product_row[
                    "k_mixed"
                ],

            "finite_displacement":
                fd,

            "uncertainty": {
                "quadrature":
                    k_quad_unc,

                "domain":
                    k_domain_unc,

                "method":
                    k_method_unc,

                "bvp":
                    k_bvp_unc,

                "finite_displacement":
                    k_fd_unc,

                "finite_displacement_resolved":
                    fd_resolved,

                "total":
                    k_total_unc,
            },

            "collective_lambda":
                lambda_collective,

            "collective_lambda_uncertainty":
                lambda_collective_unc,

            "positive":
                collective_sign_positive,

            "negative":
                collective_sign_negative,
        },

        "hessian_rows":
            hessian_rows,

        "decision_metrics": {
            "max_ward_common_residual":
                max_ward_res,

            "max_collective_rq_relerr":
                max_rq_relerr,

            "min_next_gap":
                min_next_gap,

            "min_relative_overlap":
                min_lowest_overlap,

            "relative_rank1_shift_shrink_pass":
                relative_shift_shrink_pass,

            "variational_upper_bound_pass":
                variational_upper_bound_pass,

            "grid_abs_uncertainty":
                lambda_grid_unc,

            "domain_abs_uncertainty":
                lambda_domain_unc,

            "total_lambda_uncertainty":
                lambda_numeric_unc,

            "reference_lambda0":
                lambda_ref,

            "robust_positive_relative_mode":
                robust_positive,

            "robust_negative_relative_mode":
                robust_negative,

            "ward_hessian_structure_pass":
                hessian_structure_pass,

            "background_pass":
                background_pass,

            "norm_reconstruction_pass":
                norm_reconstruction_pass,

            "d3_coupled_linear_stability_promotion_authorized":
                promotion,
        },

        "claim_limits": [
            (
                "GREEN is only a coupled-linear/energetic l=1 "
                "result in the declared flat-space effective "
                "X/phi/Y theory."
            ),
            (
                "Only the exact common translation is removed; "
                "relative source-versus-activation displacement "
                "remains physical."
            ),
            (
                "A negative weighted second variation fails the "
                "variational stability gate but R4 alone does not "
                "assert an exponential growth rate."
            ),
            (
                "Explicit QY reservoir/transfer/reset and "
                "switching radiation remain open."
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
        + "\n"
    )

    with OUT_CURVATURE_CSV.open(
        "w",
        newline="",
    ) as handle:
        fields = sorted(
            {
                key
                for row in curvature_rows
                for key in row.keys()
            }
        )

        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )

        writer.writeheader()

        for row in (
            curvature_rows
        ):
            writer.writerow(
                {
                    key:
                        row.get(
                            key,
                            "",
                        )
                    for key in fields
                }
            )

    with OUT_HESSIAN_CSV.open(
        "w",
        newline="",
    ) as handle:
        fields = sorted(
            {
                key
                for row in hessian_rows
                for key in row.keys()
            }
        )

        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )

        writer.writeheader()

        for row in (
            hessian_rows
        ):
            writer.writerow(
                {
                    key:
                        row.get(
                            key,
                            "",
                        )
                    for key in fields
                }
            )

    print(
        f"SUMMARY_JSON={OUT_JSON}"
    )

    print(
        f"CURVATURE_CSV={OUT_CURVATURE_CSV}"
    )

    print(
        f"HESSIAN_CSV={OUT_HESSIAN_CSV}"
    )


if __name__ == "__main__":
    main()
