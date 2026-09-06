#!/usr/bin/env python3
"""
031D3C-R5 — saturation-safe relative-translation Schur closeout.

R4 exposed two precision failures rather than a physical instability:

1. f(a_shift)-f(a0) was formed after
       f(a)=1-exp(-a^2/2)
   had rounded to 1 in the saturated a~9.5 core.

2. A dense float64 matrix was asked to preserve a ~1.3e-20
   Rayleigh quotient after cancelling translation-curvature errors
   many orders larger.

R5 avoids both subtractions.

Exact common translation gives

    H(tS+tA)=0.

For normalized relative translation r, H r can therefore be
reconstructed entirely from the microscopic X/phi <-> Y cross-Hessian.

In the basis

    common translation,
    relative translation,
    orthogonal l=1 modes,

the Hessian has

        [ 0   0    0  ]
    H = [ 0   a   b^T ]
        [ 0   b    C  ].

If

    C >= gamma I,

then

    lambda_relative_relaxed
        >=
    a - ||b||^2/gamma.

Only the exact common translation is a zero mode.
Relative translation remains physical.

GREEN is only coupled-linear stability in the declared flat-space
effective X/phi/Y theory.

It is not nonlinear, Einstein, EFT, empirical, reservoir,
switching-radiation, or practical-device closure.
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


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

DATA.mkdir(
    parents=True,
    exist_ok=True,
)

R4_SOURCE = (
    SIM
    / "031d3cr4_relative_translation_ward_closeout.py"
)

R4_SUMMARY = (
    DATA
    / "031d3cr4_relative_translation_ward_summary.json"
)

R3_SUMMARY = (
    DATA
    / "031d3cr3_weighted_variational_l1_summary.json"
)

R2_SUMMARY = (
    DATA
    / "031d3cr2_chebyshev_dense_summary.json"
)

D3C_SUMMARY = (
    DATA
    / "031d3c_activation_stability_switching_summary.json"
)

OUT_JSON = (
    DATA
    / "031d3cr5_saturation_safe_schur_summary.json"
)

OUT_CSV = (
    DATA
    / "031d3cr5_saturation_safe_schur_scan.csv"
)

QUAD_ORDERS = (
    32,
    48,
    64,
    80,
)

DOMAIN_RADII = (
    250.0,
    350.0,
    450.0,
    500.0,
)

FD_DISPLACEMENTS = (
    0.125,
    0.25,
    0.375,
    0.50,
)

FD_RMAX = 500.0
FD_RADIAL_ORDER = 80
FD_ANGULAR_ORDER = 96

# Observed orthogonal l=1 gap is ~1.3e-4.
# We certify against a floor over an order of magnitude smaller.
CERTIFIED_ORTHOGONAL_GAP = 1.0e-5

OBSERVED_OVER_CERTIFIED_MIN = 10.0

FD_REL_TOL = 2.0e-4

CROSS_RQ_REL_TOL = 2.0e-9

COMMON_COUPLING_ABS_TOL = 1.0e-28

SCHUR_MARGIN_FACTOR = 8.0

MAX_NON_L1_GROWTH = 1.0e-9


def require(
    path: Path,
) -> None:

    if not path.is_file():

        raise RuntimeError(
            f"Missing required artifact: {path}"
        )


def load_module(
    name: str,
    path: Path,
):

    spec = (
        importlib.util.spec_from_file_location(
            name,
            path,
        )
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            f"Cannot import {path}"
        )

    module = (
        importlib.util.module_from_spec(
            spec
        )
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


def load_json(
    path: Path,
) -> dict[str, Any]:

    return json.loads(
        path.read_text()
    )


def relerr(
    a: float,
    b: float,
    floor: float = 1.0e-300,
) -> float:

    return (
        abs(
            a - b
        )
        / max(
            abs(
                a
            ),
            abs(
                b
            ),
            floor,
        )
    )


def builtin(
    value: Any,
) -> Any:

    if isinstance(
        value,
        dict,
    ):

        return {
            str(
                key
            ):
            builtin(
                item
            )
            for key, item
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
            builtin(
                item
            )
            for item
            in value
        ]

    if isinstance(
        value,
        np.ndarray,
    ):

        return [
            builtin(
                item
            )
            for item
            in value.tolist()
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


def stable_tail(
    a,
):

    a = np.asarray(
        a,
        dtype=float,
    )

    return np.exp(
        -0.5
        * a
        * a
    )


def saturation_oracle() -> dict[str, Any]:

    a0 = 9.5
    a1 = 9.4

    s0 = math.exp(
        -0.5
        * a0
        * a0
    )

    s1 = math.exp(
        -0.5
        * a1
        * a1
    )

    f0 = (
        1.0
        - s0
    )

    f1 = (
        1.0
        - s1
    )

    naive = (
        f1
        - f0
    )

    stable = (
        s0
        - s1
    )

    passed = bool(
        naive
        == 0.0
        and
        stable
        != 0.0
    )

    return {
        "a0":
            a0,

        "a1":
            a1,

        "tail0":
            s0,

        "tail1":
            s1,

        "naive_f_difference":
            naive,

        "stable_f_difference":
            stable,

        "pass":
            passed,
    }


def corrected_fd(
    r4,
    evaluate: Callable,
) -> dict[str, Any]:

    r, wr = (
        r4.segmented_gauss(
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

    Wy = (
        r4.W(
            y
        )
    )

    s0 = (
        stable_tail(
            a0
        )
    )

    A0 = (
        np.exp(
            -0.5
            * u
            * u
        )
        * np.exp(
            0.5
            * s0
            * u
            * u
        )
    )

    rows = []

    for d in (
        FD_DISPLACEMENTS
    ):

        total = 0.0

        for sign in (
            +1.0,
            -1.0,
        ):

            shifted_radius = np.sqrt(
                r[
                    :,
                    None,
                ] ** 2
                + d
                * d
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
                ashift,
                _aps,
            ) = evaluate(
                shifted_radius
            )

            s_shift = (
                stable_tail(
                    ashift
                )
            )

            # Exact saturation-safe identity:
            #
            # f_shift - f0
            #
            # =
            #
            # (1-s_shift) - (1-s0)
            #
            # =
            #
            # s0 - s_shift.
            #
            # Never evaluate the two near-unity f values first.

            delta_f = (
                s0[
                    :,
                    None,
                ]
                - s_shift
            )

            delta_log_A = (
                -0.5
                * u[
                    :,
                    None,
                ] ** 2
                * delta_f
            )

            delta_V = (
                Wy[
                    :,
                    None,
                ]
                * A0[
                    :,
                    None,
                ]
                * np.expm1(
                    delta_log_A
                )
            )

            total += (
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
                        * delta_V,
                        dtype=np.longdouble,
                    )
                )
            )

        delta_even = (
            0.5
            * total
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

    x = np.asarray(
        [
            row[
                "d"
            ] ** 2
            for row
            in rows
        ],
        dtype=float,
    )

    yk = np.asarray(
        [
            row[
                "k_fd"
            ]
            for row
            in rows
        ],
        dtype=float,
    )

    design = np.column_stack(
        (
            np.ones_like(
                x
            ),
            x,
            x
            * x,
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

    coeff3 = np.linalg.solve(
        design[
            :3
        ],
        yk[
            :3
        ],
    )

    k0_three = float(
        coeff3[
            0
        ]
    )

    uncertainty = max(
        fit_rms,
        abs(
            k0
            - k0_three
        ),
        1.0e-30,
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


def cross_schur(
    r4,
    evaluate: Callable,
    *,
    rmax: float,
    order: int,
    chi: float,
    rho_y: float,
) -> dict[str, float]:

    r, wr = (
        r4.segmented_gauss(
            rmax,
            order,
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
        r
    )

    s = (
        stable_tail(
            a
        )
    )

    fp = (
        a
        * s
    )

    A_sat = np.exp(
        -0.5
        * u
        * u
    )

    A_full = (
        A_sat
        * np.exp(
            0.5
            * s
            * u
            * u
        )
    )

    Wy = (
        r4.W(
            y
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
        * A_full
        * y
        / (
            1.0
            + y
            * y
        )
    )

    one_minus_half_fu2 = (
        1.0
        - 0.5
        * u
        * u
        + 0.5
        * s
        * u
        * u
    )

    c_ua = (
        -chi
        / sqrt_rho
        * u
        * A_full
        * Wy
        * fp
        * one_minus_half_fu2
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

    S = float(
        np.sum(
            wr
            * (
                qx
                * qx
                + qu
                * qu
            ),
            dtype=np.longdouble,
        )
    )

    A_mass = float(
        np.sum(
            wr
            * qa
            * qa,
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

    sqrtM = math.sqrt(
        M_eff
    )

    common = np.zeros(
        (
            r.size,
            5,
        ),
        dtype=float,
    )

    relative = np.zeros_like(
        common
    )

    common[
        :,
        0,
    ] = qx

    common[
        :,
        2,
    ] = qu

    common[
        :,
        3,
    ] = qa

    common /= math.sqrt(
        S
        + A_mass
    )

    relative[
        :,
        0,
    ] = (
        sqrtM
        * qx
        / S
    )

    relative[
        :,
        2,
    ] = (
        sqrtM
        * qu
        / S
    )

    relative[
        :,
        3,
    ] = (
        -sqrtM
        * qa
        / A_mass
    )

    # Exact common translation:
    #
    # H(tS+tA)=0.
    #
    # Therefore H tS is obtained entirely from
    # the microscopic source/activation cross block.

    h_tS = np.zeros_like(
        common
    )

    h_tS[
        :,
        0,
    ] = (
        -c_xa
        * qa
    )

    h_tS[
        :,
        2,
    ] = (
        -c_ua
        * qa
    )

    h_tS[
        :,
        3,
    ] = (
        c_xa
        * qx
        + c_ua
        * qu
    )

    h_relative = (
        h_tS
        / sqrtM
    )

    def inner(
        left,
        right,
    ) -> float:

        return float(
            np.sum(
                wr
                * np.sum(
                    left
                    * right,
                    axis=1,
                ),
                dtype=np.longdouble,
            )
        )

    common_coupling = (
        inner(
            common,
            h_relative,
        )
    )

    relative_rq = (
        inner(
            relative,
            h_relative,
        )
    )

    residual = (
        h_relative
        - relative_rq
        * relative
        - common_coupling
        * common
    )

    b_norm = math.sqrt(
        max(
            inner(
                residual,
                residual,
            ),
            0.0,
        )
    )

    cross_integral = float(
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

    k_cross = (
        -cross_integral
    )

    lambda_cross = (
        k_cross
        / M_eff
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

        "common_norm":
            inner(
                common,
                common,
            ),

        "relative_norm":
            inner(
                relative,
                relative,
            ),

        "common_relative_inner":
            inner(
                common,
                relative,
            ),

        "common_coupling":
            common_coupling,

        "relative_rayleigh":
            relative_rq,

        "k_from_cross":
            k_cross,

        "lambda_from_cross":
            lambda_cross,

        "rayleigh_cross_relerr":
            relerr(
                relative_rq,
                lambda_cross,
            ),

        "b_norm":
            b_norm,

        "h_relative_norm":
            math.sqrt(
                max(
                    inner(
                        h_relative,
                        h_relative,
                    ),
                    0.0,
                )
            ),

        "schur_correction_at_certified_gap":
            (
                b_norm
                * b_norm
                / CERTIFIED_ORTHOGONAL_GAP
            ),

        "max_abs_c_xa":
            float(
                np.max(
                    np.abs(
                        c_xa
                    )
                )
            ),

        "max_abs_c_ua":
            float(
                np.max(
                    np.abs(
                        c_ua
                    )
                )
            ),
    }


def main() -> None:

    print(
        "=== 031D3C-R5 SATURATION-SAFE RELATIVE-TRANSLATION SCHUR CLOSEOUT ==="
    )

    print(
        "CLAIM_CLASS=COUPLED_LINEAR_L1_CANCELLATION_FREE_SCHUR_GATE"
    )

    print(
        "R4_NAIVE_SATURATED_FINITE_DIFFERENCE_REUSED=NO"
    )

    print(
        "R4_TINY_DENSE_EIGENVALUE_USED_FOR_SIGN=NO"
    )

    print(
        "ONLY_EXACT_COMMON_TRANSLATION_ZERO_MODE=YES"
    )

    print(
        "RELATIVE_TRANSLATION_PROJECTED=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        R4_SOURCE,
        R4_SUMMARY,
        R3_SUMMARY,
        R2_SUMMARY,
        D3C_SUMMARY,
    ):

        require(
            path
        )

    r4s = load_json(
        R4_SUMMARY
    )

    r3s = load_json(
        R3_SUMMARY
    )

    r2s = load_json(
        R2_SUMMARY
    )

    d3cs = load_json(
        D3C_SUMMARY
    )

    if not str(
        r4s.get(
            "classification",
            "",
        )
    ).startswith(
        "YELLOW_D3CR4"
    ):

        raise RuntimeError(
            "R5 expects the R4 precision-limited YELLOW state"
        )

    if not bool(
        r3s[
            "decision_metrics"
        ][
            "weighted_self_adjointness_pass"
        ]
    ):

        raise RuntimeError(
            "R3 weighted self-adjointness prerequisite failed"
        )

    print(
        "\n=== STAGE A: SATURATION SUBTRACTION ORACLE ==="
    )

    oracle = (
        saturation_oracle()
    )

    for key, value in (
        oracle.items()
    ):

        print(
            f"SAT_ORACLE_{key.upper()}={value}"
        )

    if not oracle[
        "pass"
    ]:

        raise RuntimeError(
            "Saturation subtraction oracle failed"
        )

    r4 = load_module(
        "d3cr4_parent_for_r5",
        R4_SOURCE,
    )

    model = (
        r4s[
            "model"
        ]
    )

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
        model[
            "target_I_QX"
        ]
    )

    target_qy = float(
        model[
            "target_I_QY"
        ]
    )

    print(
        "\n=== STAGE B: OPERATING PROVENANCE ==="
    )

    for key, value in (
        (
            "OMEGA_X",
            omega_x,
        ),
        (
            "OMEGA_Y",
            omega_y,
        ),
        (
            "EPSILON",
            epsilon,
        ),
        (
            "CHI",
            chi,
        ),
        (
            "MU",
            mu,
        ),
        (
            "RHO_Y",
            rho_y,
        ),
        (
            "TARGET_I_QX",
            target_qx,
        ),
        (
            "TARGET_I_QY",
            target_qy,
        ),
    ):

        print(
            f"{key}={value:.15e}"
        )

    d3b = (
        r4.load_module(
            "d3b031d3cr5",
            r4.D3B_SOURCE,
        )
    )

    qmod = (
        r4.load_module(
            "qball031d3cr5",
            r4.QBALL_SOURCE,
        )
    )

    d3a = (
        r4.load_module(
            "d3a031d3cr5",
            r4.D3A_SOURCE,
        )
    )

    print(
        "\n=== STAGE C: FULL D3B BACKGROUND RECONSTRUCTION ===",
        flush=True,
    )

    (
        product80,
        source80,
        activation80,
    ) = (
        r4.build_product_background(
            qmod,
            d3a,
            omega_x,
            omega_y,
            epsilon,
            chi,
            mu,
            r4.X_SOURCE_MATCH,
        )
    )

    (
        coarse,
        fine,
        tight,
        homotopy,
        diag_c,
        diag_f,
        diag_t,
    ) = (
        r4.reconstruct_full_background(
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
    )

    del (
        product80,
        source80,
        activation80,
    )

    background_pass = bool(
        diag_t[
            "qx_relerr"
        ]
        <= r4.MAX_BVP_CHARGE_RELERR

        and
        diag_t[
            "qy_relerr"
        ]
        <= r4.MAX_BVP_CHARGE_RELERR

        and
        diag_t[
            "max_rms_residual"
        ]
        <= r4.MAX_BVP_RMS
    )

    print(
        f"BVP_TIGHT_OMEGA_X={diag_t['omega_x']:.15e}"
    )

    print(
        f"BVP_TIGHT_OMEGA_Y={diag_t['omega_y']:.15e}"
    )

    print(
        f"BVP_TIGHT_QX_RELERR={diag_t['qx_relerr']:.15e}"
    )

    print(
        f"BVP_TIGHT_QY_RELERR={diag_t['qy_relerr']:.15e}"
    )

    print(
        f"BVP_TIGHT_RMS={diag_t['max_rms_residual']:.15e}"
    )

    print(
        f"FULL_BACKGROUND_RECONSTRUCTION_PASS={background_pass}"
    )

    eval_tight = (
        r4.full_solution_evaluator(
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

    print(
        "\n=== STAGE D: DERIVATIVE CURVATURE ===",
        flush=True,
    )

    derivative_rows = []

    for order in (
        QUAD_ORDERS
    ):

        row = (
            r4.curvature_integrals(
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
        )

        row[
            "scan"
        ] = "DERIVATIVE_QUADRATURE"

        derivative_rows.append(
            row
        )

        print(
            f"DERIVATIVE ORDER={order} "
            f"K={row['k_mixed']:+.15e} "
            f"K_DIRECT={row['k_direct_corrected']:+.15e} "
            f"LAMBDA={row['lambda_relative_collective']:+.15e}",
            flush=True,
        )

    for rmax in (
        DOMAIN_RADII
    ):

        row = (
            r4.curvature_integrals(
                eval_tight,
                rmax=rmax,
                order=80,
                epsilon=epsilon,
                chi=chi,
                mu=mu,
                rho_y=rho_y,
                omega_y=omega_y_tight,
                full_coupled=True,
            )
        )

        row[
            "scan"
        ] = "DERIVATIVE_DOMAIN"

        derivative_rows.append(
            row
        )

        print(
            f"DERIVATIVE_DOMAIN RMAX={rmax:.1f} "
            f"K={row['k_mixed']:+.15e} "
            f"LAMBDA={row['lambda_relative_collective']:+.15e}",
            flush=True,
        )

    d80 = next(
        row
        for row
        in derivative_rows
        if (
            row[
                "scan"
            ]
            == "DERIVATIVE_QUADRATURE"
            and
            row[
                "order"
            ]
            == 80
        )
    )

    print(
        "\n=== STAGE E: SATURATION-SAFE FINITE DISPLACEMENT ===",
        flush=True,
    )

    fd = (
        corrected_fd(
            r4,
            eval_tight,
        )
    )

    for row in (
        fd[
            "rows"
        ]
    ):

        print(
            f"FD_SAFE d={row['d']:.6f} "
            f"DELTA_E={row['delta_E_interaction']:+.15e} "
            f"K_FD={row['k_fd']:+.15e}",
            flush=True,
        )

    k_derivative = float(
        d80[
            "k_mixed"
        ]
    )

    k_fd = float(
        fd[
            "k_extrapolated"
        ]
    )

    fd_rel = (
        relerr(
            k_fd,
            k_derivative,
        )
    )

    fd_pass = bool(
        fd_rel
        <= FD_REL_TOL
        and
        k_fd
        > 0.0
        and
        k_derivative
        > 0.0
    )

    old_fd = float(
        r4s[
            "curvature"
        ][
            "finite_displacement"
        ][
            "k_extrapolated"
        ]
    )

    print(
        f"OLD_R4_FD_K={old_fd:+.15e}"
    )

    print(
        f"R5_SAFE_FD_K={k_fd:+.15e}"
    )

    print(
        f"DERIVATIVE_K={k_derivative:+.15e}"
    )

    print(
        f"SAFE_FD_DERIVATIVE_RELERR={fd_rel:.15e}"
    )

    print(
        f"SATURATION_SAFE_FD_PASS={fd_pass}"
    )

    print(
        "\n=== STAGE F: CANCELLATION-FREE CROSS-HESSIAN ACTION ===",
        flush=True,
    )

    schur_rows = []

    for order in (
        QUAD_ORDERS
    ):

        row = (
            cross_schur(
                r4,
                eval_tight,
                rmax=500.0,
                order=order,
                chi=chi,
                rho_y=rho_y,
            )
        )

        row[
            "scan"
        ] = "SCHUR_QUADRATURE"

        schur_rows.append(
            row
        )

        print(
            f"SCHUR ORDER={order} "
            f"A={row['relative_rayleigh']:+.15e} "
            f"K={row['k_from_cross']:+.15e} "
            f"B_NORM={row['b_norm']:.15e} "
            f"CORR={row['schur_correction_at_certified_gap']:.15e} "
            f"COMMON={row['common_coupling']:+.3e}",
            flush=True,
        )

    for rmax in (
        DOMAIN_RADII
    ):

        row = (
            cross_schur(
                r4,
                eval_tight,
                rmax=rmax,
                order=80,
                chi=chi,
                rho_y=rho_y,
            )
        )

        row[
            "scan"
        ] = "SCHUR_DOMAIN"

        schur_rows.append(
            row
        )

        print(
            f"SCHUR_DOMAIN RMAX={rmax:.1f} "
            f"A={row['relative_rayleigh']:+.15e} "
            f"B_NORM={row['b_norm']:.15e} "
            f"CORR={row['schur_correction_at_certified_gap']:.15e}",
            flush=True,
        )

    s80 = next(
        row
        for row
        in schur_rows
        if (
            row[
                "scan"
            ]
            == "SCHUR_QUADRATURE"
            and
            row[
                "order"
            ]
            == 80
        )
    )

    s64 = next(
        row
        for row
        in schur_rows
        if (
            row[
                "scan"
            ]
            == "SCHUR_QUADRATURE"
            and
            row[
                "order"
            ]
            == 64
        )
    )

    s450 = next(
        row
        for row
        in schur_rows
        if (
            row[
                "scan"
            ]
            == "SCHUR_DOMAIN"
            and
            row[
                "rmax"
            ]
            == 450.0
        )
    )

    cross_identity_pass = bool(
        s80[
            "rayleigh_cross_relerr"
        ]
        <= CROSS_RQ_REL_TOL
    )

    common_pass = bool(
        abs(
            s80[
                "common_coupling"
            ]
        )
        <= COMMON_COUPLING_ABS_TOL
    )

    print(
        "CROSS_ACTION_IDENTITY_RELERR="
        f"{s80['rayleigh_cross_relerr']:.15e}"
    )

    print(
        f"CROSS_ACTION_IDENTITY_PASS={cross_identity_pass}"
    )

    print(
        f"COMMON_COUPLING={s80['common_coupling']:+.15e}"
    )

    print(
        f"COMMON_TRANSLATION_DECOUPLING_PASS={common_pass}"
    )

    print(
        "\n=== STAGE G: ORTHOGONAL GAP + SCHUR LOWER BOUND ==="
    )

    r3_gap = min(
        float(
            row[
                "projected_lambda1"
            ]
        )
        for row
        in r3s[
            "rows"
        ]
    )

    r4_gap = float(
        r4s[
            "decision_metrics"
        ][
            "min_next_gap"
        ]
    )

    observed_gap = min(
        r3_gap,
        r4_gap,
    )

    gap_pass = bool(
        observed_gap
        >=
        OBSERVED_OVER_CERTIFIED_MIN
        * CERTIFIED_ORTHOGONAL_GAP
    )

    r2_l0_pass = bool(
        r2s[
            "chebyshev_decisions"
        ][
            "0"
        ][
            "pass"
        ]
    )

    r2_l2_pass = bool(
        r2s[
            "chebyshev_decisions"
        ][
            "2"
        ][
            "pass"
        ]
    )

    inherited_l3_l8_pass = bool(
        r2s[
            "inherited"
        ][
            "l3_to_l8_pass"
        ]
        and
        r2s[
            "inherited"
        ][
            "l3_to_l8_rightmost_complete"
        ]
    )

    non_l1_growth = max(
        float(
            row[
                "max_physical_growth"
            ]
        )
        for row
        in d3cs[
            "spectrum_rows"
        ]
        if int(
            row[
                "ell"
            ]
        )
        != 1
    )

    non_l1_pass = bool(
        r2_l0_pass
        and
        r2_l2_pass
        and
        inherited_l3_l8_pass
        and
        non_l1_growth
        <= MAX_NON_L1_GROWTH
    )

    inherited_direct_l1 = bool(
        r3s[
            "decision_metrics"
        ][
            "inherited_direct_l1_continuum_pass"
        ]
    )

    a_value = float(
        s80[
            "relative_rayleigh"
        ]
    )

    schur_correction = float(
        s80[
            "schur_correction_at_certified_gap"
        ]
    )

    quad_unc = abs(
        a_value
        - float(
            s64[
                "relative_rayleigh"
            ]
        )
    )

    domain_unc = abs(
        a_value
        - float(
            s450[
                "relative_rayleigh"
            ]
        )
    )

    identity_unc = abs(
        a_value
        - float(
            d80[
                "lambda_relative_collective"
            ]
        )
    )

    fd_unc = (
        abs(
            k_fd
            - k_derivative
        )
        + float(
            fd[
                "uncertainty_proxy"
            ]
        )
    ) / float(
        d80[
            "M_eff"
        ]
    )

    numeric_unc = (
        quad_unc
        + domain_unc
        + identity_unc
        + fd_unc
    )

    lower_bound = (
        a_value
        - SCHUR_MARGIN_FACTOR
        * numeric_unc
        - schur_correction
    )

    positive_schur = bool(
        lower_bound
        > 0.0
        and
        a_value
        > 0.0
        and
        schur_correction
        < a_value
    )

    print(
        f"R3_OBSERVED_NEXT_GAP={r3_gap:+.15e}"
    )

    print(
        f"R4_OBSERVED_NEXT_GAP={r4_gap:+.15e}"
    )

    print(
        f"OBSERVED_ORTHOGONAL_GAP={observed_gap:+.15e}"
    )

    print(
        f"CERTIFIED_ORTHOGONAL_GAP={CERTIFIED_ORTHOGONAL_GAP:+.15e}"
    )

    print(
        f"ORTHOGONAL_GAP_PASS={gap_pass}"
    )

    print(
        f"RELATIVE_RAYLEIGH_A={a_value:+.15e}"
    )

    print(
        "ORTHOGONAL_COUPLING_B_NORM="
        f"{s80['b_norm']:.15e}"
    )

    print(
        "SCHUR_RELAXATION_CORRECTION_MAX="
        f"{schur_correction:.15e}"
    )

    print(
        f"RELATIVE_NUMERIC_UNCERTAINTY={numeric_unc:.15e}"
    )

    print(
        f"SCHUR_MARGIN_FACTOR={SCHUR_MARGIN_FACTOR:.1f}"
    )

    print(
        f"RELAXED_RELATIVE_LOWER_BOUND={lower_bound:+.15e}"
    )

    print(
        f"POSITIVE_SCHUR_LOWER_BOUND={positive_schur}"
    )

    print(
        f"R2_L0_PASS={r2_l0_pass}"
    )

    print(
        f"R2_L2_PASS={r2_l2_pass}"
    )

    print(
        f"INHERITED_L3_TO_L8_PASS={inherited_l3_l8_pass}"
    )

    print(
        f"MAX_NON_L1_GROWTH={non_l1_growth:.15e}"
    )

    print(
        f"NON_L1_SECTORS_PASS={non_l1_pass}"
    )

    prerequisites = bool(
        oracle[
            "pass"
        ]
        and
        background_pass
        and
        fd_pass
        and
        cross_identity_pass
        and
        common_pass
        and
        gap_pass
        and
        inherited_direct_l1
        and
        non_l1_pass
    )

    if (
        prerequisites
        and
        positive_schur
    ):

        classification = (
            "GREEN_D3CR5_COUPLED_LINEAR_L1_RELATIVE_TRANSLATION_"
            "POSITIVE_BY_CANCELLATION_FREE_SCHUR_BOUND"
        )

        l1_status = (
            "GREEN"
        )

        promotion = True

        next_action = (
            "031D3D_EXPLICIT_QY_RESERVOIR_TRANSFER_RESET_SWITCHING_RADIATION"
        )

    else:

        classification = (
            "YELLOW_D3CR5_RELATIVE_TRANSLATION_SCHUR_CLOSEOUT_UNRESOLVED"
        )

        l1_status = (
            "UNRESOLVED"
        )

        promotion = False

        next_action = (
            "REFINE_ONLY_FAILED_R5_SATURATION_FD_CROSS_ACTION_OR_GAP_SUBGATE"
        )

    print(
        "\n=== STAGE H: DECISION ==="
    )

    print(
        f"031D3_L1_COUPLED_LINEAR_STABILITY={l1_status}"
    )

    print(
        "TRUE_EXPONENTIAL_INSTABILITY_ESTABLISHED=False"
    )

    print(
        f"031D3CR5_CLASSIFICATION={classification}"
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

    all_rows = []

    for row in (
        derivative_rows
    ):

        item = dict(
            row
        )

        item[
            "family"
        ] = "DERIVATIVE"

        all_rows.append(
            item
        )

    for row in (
        schur_rows
    ):

        item = dict(
            row
        )

        item[
            "family"
        ] = "SCHUR"

        all_rows.append(
            item
        )

    for row in (
        fd[
            "rows"
        ]
    ):

        item = dict(
            row
        )

        item[
            "family"
        ] = "FINITE_DISPLACEMENT_SAFE"

        all_rows.append(
            item
        )

    fields = sorted(
        {
            key
            for row
            in all_rows
            for key
            in row.keys()
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

        for row in (
            all_rows
        ):

            writer.writerow(
                {
                    key:
                        row.get(
                            key,
                            "",
                        )
                    for key
                    in fields
                }
            )

    summary = {
        "classification":
            classification,

        "next":
            next_action,

        "claim_class":
            "COUPLED_LINEAR_L1_CANCELLATION_FREE_SCHUR_GATE",

        "saturation_oracle":
            oracle,

        "model": {
            "omega_x":
                float(
                    tight.p[
                        0
                    ]
                ),

            "omega_y":
                float(
                    tight.p[
                        1
                    ]
                ),

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

        "background": {
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

        "corrected_finite_displacement": {
            **fd,

            "old_r4_k":
                old_fd,

            "derivative_k":
                k_derivative,

            "relative_error":
                fd_rel,

            "pass":
                fd_pass,
        },

        "schur": {
            "tight":
                s80,

            "observed_gap":
                observed_gap,

            "certified_gap":
                CERTIFIED_ORTHOGONAL_GAP,

            "gap_pass":
                gap_pass,

            "numeric_uncertainty":
                numeric_unc,

            "margin_factor":
                SCHUR_MARGIN_FACTOR,

            "relaxed_relative_lower_bound":
                lower_bound,

            "positive_lower_bound":
                positive_schur,
        },

        "inherited": {
            "r2_l0_pass":
                r2_l0_pass,

            "r2_l2_pass":
                r2_l2_pass,

            "l3_to_l8_pass":
                inherited_l3_l8_pass,

            "max_non_l1_growth":
                non_l1_growth,

            "non_l1_pass":
                non_l1_pass,

            "direct_l1_continuum_pass":
                inherited_direct_l1,
        },

        "decision": {
            "prerequisites":
                prerequisites,

            "l1_coupled_linear_stability":
                l1_status,

            "promotion_authorized":
                promotion,
        },

        "claim_limits": [
            (
                "GREEN is only coupled-linear stability "
                "in the declared flat-space effective "
                "X/phi/Y theory."
            ),
            (
                "Only exact common translation is a zero "
                "mode; relative translation remains physical."
            ),
            (
                "The R4 ~1e-32 finite-displacement result "
                "is rejected as a saturated-subtraction artifact."
            ),
            (
                "The sign decision does not use the R4 tiny "
                "dense eigenvalue because the physical curvature "
                "is ~1e-20."
            ),
            (
                "Explicit QY reservoir/transfer/reset and "
                "switching radiation remain open."
            ),
            (
                "Nonlinear stability, Einstein backreaction, "
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

    print(
        f"SUMMARY_JSON={OUT_JSON}"
    )

    print(
        f"SCAN_CSV={OUT_CSV}"
    )


if __name__ == "__main__":
    main()
