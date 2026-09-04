"""
031D2C — full fixed-Noether-charge X + phi + auxiliary-gate solve

This run stops using the exterior fixed-u approximation.

It solves the microscopic Q-ball source y, scalar-metric field u,
and reciprocal gate field z=s/v_s simultaneously.

Model
-----

A(u) = exp(-u^2/2)

W(y) = 1/2 log(1+y^2)

y'' + 2y'/x
    = A(u) y/(1+y^2) - Omega^2 y

u'' + 2u'/x
    = [epsilon^2 + delta2 z^2] u
      - chi^2 A(u) W(y) u

z'' + 2z'/x
    = [a2(z^2-1) + b2 u^2] z

Noether accumulator:

Qhat' = 4 pi Omega x^2 y^2.

Omega is solved as a BVP parameter so that Qhat at infinity equals
the certified scalarized on-state charge.

Gate candidate
--------------

We deliberately do NOT use the D2B minimum-energy portal.
That candidate created an extreme multiscale problem.

Instead use a conditioning-balanced portal

    g_s = 3e-16

while preserving the same required product g_s v_s and the same
gate vacuum mass m_s.

This is an existence/coupling run, not an optimization run.

Claims this run can establish
-----------------------------
- self-consistent fixed-Q microscopic y/u/z ON solution;
- exact same-Q OFF solution exists with u=0, z=1;
- OFF scalar tachyon is removed by the gate mass shift;
- gate/source reciprocity is included in the equations;
- gate positive energy is counted;
- payload-region scalar gradient is compared with the previous
  certified antigravity source;
- domain convergence is checked.

Still open
----------
- full coupled perturbative stability of y/u/z;
- nonlinear switching/nucleation and reset;
- radiation;
- full physical metric / Einstein backreaction;
- EFT/naturalness and empirical closure;
- practical device.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

from scipy.integrate import quad, solve_bvp


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

QBALL_SOURCE = (
    SIM
    / "031b2a_global_qball_activated_scalar_control.py"
)

ROBUST_SUMMARY = (
    DATA
    / "031c96_operating_margin_robustness_summary.json"
)

LOW_SUMMARY = (
    DATA
    / "031d1r2_lowbranch_offstate_hessian_summary.json"
)

D1HR_SUMMARY = (
    DATA
    / "031d1hr_highbranch_certificate_summary.json"
)

OUT_JSON = (
    DATA
    / "031d2c_full_fixedq_gate_summary.json"
)

OUT_CSV = (
    DATA
    / "031d2c_full_fixedq_domain_scan.csv"
)


X0 = 1.0e-5
X_MATCH = 80.0

RMAX_VALUES = (
    320.0,
    450.0,
    600.0,
)

INITIAL_POINTS = 3200

BVP_TOL = 3.0e-5
FINAL_TOL = 8.0e-6

MAX_NODES = 100_000

# Conditioning-balanced gate candidate.
G_S = 3.0e-16

# Preserve the D2B gate vacuum mass.
M_S_EV = 2.0719332942e-7

STABILIZATION_MARGIN = 1.20

Q_REL_TOL = 3.0e-6

DOMAIN_OMEGA_REL_TOL = 5.0e-4
DOMAIN_U0_REL_TOL = 5.0e-3
DOMAIN_ENERGY_REL_TOL = 2.0e-2

ON_U0_MIN = 0.20
ON_Z0_MAX = 5.0e-2

OFF_STABILITY_MARGIN_MIN = 1.0e-4

PAYLOAD_GRADIENT_RATIO_MIN = 0.90

HBARC_EV_M = 1.973269804e-7
J_PER_EV = 1.602176634e-19
J_PER_GEV = 1.602176634e-10


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(
            f"Missing required file: {path}"
        )


def load_module(name: str, path: Path):
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

    sys.modules[name] = module
    spec.loader.exec_module(module)

    return module


def builtin(value: Any):
    if isinstance(value, np.generic):
        return value.item()

    if isinstance(value, np.ndarray):
        return value.tolist()

    if isinstance(value, dict):
        return {
            str(key): builtin(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            builtin(item)
            for item in value
        ]

    return value


def relerr(a: float, b: float) -> float:
    return abs(a - b) / max(
        abs(a),
        abs(b),
        1.0e-300,
    )


def cumulative_trapezoid(
    x: np.ndarray,
    f: np.ndarray,
):
    out = np.zeros_like(
        x,
        dtype=float,
    )

    out[1:] = np.cumsum(
        0.5
        * (
            f[1:]
            + f[:-1]
        )
        * np.diff(x)
    )

    return out


def main() -> None:
    print(
        "=== 031D2C FULL FIXED-Q X+PHI+GATE ON/OFF BVP ==="
    )

    print(
        "EXTERIOR_FIXED_U_APPROXIMATION=REMOVED"
    )

    print(
        "SOURCE_REACTION_INCLUDED=YES"
    )

    print(
        "FIXED_NOETHER_CHARGE=YES"
    )

    print(
        "RECIPROCAL_GATE_COUPLING_INCLUDED=YES"
    )

    print(
        "PRESCRIBED_SPATIAL_MPHI=NO"
    )

    print(
        "GATE_PARAMETER_OPTIMIZATION=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        QBALL_SOURCE,
        ROBUST_SUMMARY,
        LOW_SUMMARY,
        D1HR_SUMMARY,
    ):
        require(path)

    robust = json.loads(
        ROBUST_SUMMARY.read_text()
    )

    low = json.loads(
        LOW_SUMMARY.read_text()
    )

    d1hr = json.loads(
        D1HR_SUMMARY.read_text()
    )

    if not bool(
        robust.get(
            "family_operating_robustness_green",
            False,
        )
    ):
        raise RuntimeError(
            "031C96 operating family is not GREEN"
        )

    if not bool(
        d1hr.get(
            "gate_free_same_Q_offstate_route_closed",
            False,
        )
    ):
        raise RuntimeError(
            "031D1 gate-free off-state closure missing"
        )

    candidate = robust[
        "candidate"
    ]

    operating = robust[
        "interior_20pct_margin_point"
    ]

    quadrature = robust[
        "quadrature"
    ][
        "high_order_result"
    ]

    nominal_geometry = next(
        row
        for row in robust[
            "geometry_scan"
        ]
        if row[
            "label"
        ] == "nominal"
    )

    omega_seed = float(
        candidate["omega"]
    )

    epsilon = float(
        candidate["epsilon"]
    )

    chi = float(
        candidate["chi"]
    )

    m_x_gev = float(
        candidate[
            "m_x_gev_derived"
        ]
    )

    m_x_ev = (
        m_x_gev
        * 1.0e9
    )

    F_gev = float(
        quadrature[
            "F_gev"
        ]
    )

    M_c_gev = (
        F_gev
        / chi
    )

    M_c_ev = (
        M_c_gev
        * 1.0e9
    )

    operating_energy_j = float(
        operating[
            "energy_J"
        ]
    )

    target_q = float(
        low[
            "target_I_Q"
        ]
    )

    critical_hat = float(
        low[
            "critical_positive_delta_m2_hat"
        ]
    )

    delta2 = (
        STABILIZATION_MARGIN
        * critical_hat
    )

    required_gv_ev = (
        m_x_ev
        * math.sqrt(
            delta2
        )
    )

    v_s_ev = (
        required_gv_ev
        / G_S
    )

    lambda_s = (
        M_S_EV**2
        /
        (
            2.0
            * v_s_ev**2
        )
    )

    a2 = (
        lambda_s
        * v_s_ev**2
        / m_x_ev**2
    )

    b2 = (
        G_S**2
        * M_c_ev**2
        / m_x_ev**2
    )

    epsilon_off = math.sqrt(
        epsilon**2
        + delta2
    )

    gate_vacuum_k = math.sqrt(
        2.0
        * a2
    )

    off_lambda0 = (
        float(
            low[
                "finest_lambda0"
            ]
        )
        + delta2
    )

    print(
        f"TARGET_I_Q={target_q:.15e}"
    )

    print(
        f"G_S={G_S:.15e}"
    )

    print(
        f"V_S_EV={v_s_ev:.15e}"
    )

    print(
        f"LAMBDA_S={lambda_s:.15e}"
    )

    print(
        f"M_S_EV={M_S_EV:.15e}"
    )

    print(
        f"A2_GATE={a2:.15e}"
    )

    print(
        f"B2_GATE={b2:.15e}"
    )

    print(
        f"DELTA2_GATE={delta2:.15e}"
    )

    print(
        f"EPSILON_OFF={epsilon_off:.15e}"
    )

    print(
        f"OFF_FIXEDQ_SCALAR_LAMBDA0="
        f"{off_lambda0:+.15e}"
    )

    print(
        f"OFF_GATE_RADIAL_MASS2_HAT="
        f"{2.0 * a2:.15e}"
    )

    qmod = load_module(
        "qball031d2c",
        QBALL_SOURCE,
    )

    old_x_match = float(
        qmod.X_MATCH
    )

    qmod.X_MATCH = X_MATCH

    try:
        print(
            "\n=== STAGE A: BASELINE SCALARIZED SOURCE FOR INITIAL DATA ==="
        )

        seed = qmod.solve_uncoupled_qball(
            omega_seed
        )

        if seed is None:
            raise RuntimeError(
                "Could not reconstruct Q-ball seed"
            )

        baseline = qmod.solve_coupled(
            seed,
            omega_seed,
            epsilon,
            chi,
            previous=None,
        )

        if baseline is None:
            raise RuntimeError(
                "Could not reconstruct scalarized baseline"
            )

        y80 = float(
            baseline.sol(
                X_MATCH
            )[0]
        )

        yp80 = float(
            baseline.sol(
                X_MATCH
            )[1]
        )

        u80 = float(
            baseline.sol(
                X_MATCH
            )[2]
        )

        up80 = float(
            baseline.sol(
                X_MATCH
            )[3]
        )

        k_y_seed = math.sqrt(
            1.0
            - omega_seed**2
        )

        def y_baseline_extended(x):
            xx = np.asarray(
                x,
                dtype=float,
            )

            result = np.empty_like(
                xx,
                dtype=float,
            )

            inside = (
                xx <= X_MATCH
            )

            if np.any(
                inside
            ):
                result[
                    inside
                ] = baseline.sol(
                    np.maximum(
                        xx[
                            inside
                        ],
                        X0,
                    )
                )[0]

            if np.any(
                ~inside
            ):
                xo = xx[
                    ~inside
                ]

                result[
                    ~inside
                ] = (
                    y80
                    * X_MATCH
                    / xo
                    * np.exp(
                        -k_y_seed
                        * (
                            xo
                            - X_MATCH
                        )
                    )
                )

            return result

        def yp_baseline_extended(x):
            xx = np.asarray(
                x,
                dtype=float,
            )

            result = np.empty_like(
                xx,
                dtype=float,
            )

            inside = (
                xx <= X_MATCH
            )

            if np.any(
                inside
            ):
                result[
                    inside
                ] = baseline.sol(
                    np.maximum(
                        xx[
                            inside
                        ],
                        X0,
                    )
                )[1]

            if np.any(
                ~inside
            ):
                xo = xx[
                    ~inside
                ]

                yo = (
                    y80
                    * X_MATCH
                    / xo
                    * np.exp(
                        -k_y_seed
                        * (
                            xo
                            - X_MATCH
                        )
                    )
                )

                result[
                    ~inside
                ] = (
                    -k_y_seed
                    -1.0 / xo
                ) * yo

            return result

        def u_light_extended(x):
            xx = np.asarray(
                x,
                dtype=float,
            )

            result = np.empty_like(
                xx,
                dtype=float,
            )

            inside = (
                xx <= X_MATCH
            )

            if np.any(
                inside
            ):
                result[
                    inside
                ] = baseline.sol(
                    np.maximum(
                        xx[
                            inside
                        ],
                        X0,
                    )
                )[2]

            if np.any(
                ~inside
            ):
                xo = xx[
                    ~inside
                ]

                result[
                    ~inside
                ] = (
                    u80
                    * X_MATCH
                    / xo
                    * np.exp(
                        -epsilon
                        * (
                            xo
                            - X_MATCH
                        )
                    )
                )

            return result

        u_transition = math.sqrt(
            a2 / b2
        )

        x_hi = 200.0

        while (
            float(
                u_light_extended(
                    np.array(
                        [x_hi]
                    )
                )[0]
            )
            > u_transition
        ):
            x_hi *= 1.5

            if x_hi > 1.0e6:
                raise RuntimeError(
                    "Could not bracket initial gate transition"
                )

        from scipy.optimize import brentq

        x_transition_guess = brentq(
            lambda x:
                float(
                    u_light_extended(
                        np.array(
                            [x]
                        )
                    )[0]
                )
                - u_transition,
            X_MATCH,
            x_hi,
        )

        x_length_m = (
            HBARC_EV_M
            / m_x_ev
        )

        print(
            f"INITIAL_TRANSITION_X="
            f"{x_transition_guess:.15e}"
        )

        print(
            f"INITIAL_TRANSITION_M="
            f"{x_transition_guess * x_length_m:.15e}"
        )

        previous = None
        domain_rows = []

        print(
            "\n=== STAGE B: FULL FIXED-Q DOMAIN CONTINUATION ==="
        )

        def make_initial_guess(
            x,
            rmax,
            previous_solution=None,
        ):
            if previous_solution is None:
                y = y_baseline_extended(
                    x
                )

                yp = yp_baseline_extended(
                    x
                )

                u_light = u_light_extended(
                    x
                )

                u_at_transition = float(
                    u_light_extended(
                        np.array(
                            [
                                x_transition_guess
                            ]
                        )
                    )[0]
                )

                u_heavy = (
                    u_at_transition
                    * x_transition_guess
                    / x
                    * np.exp(
                        -epsilon_off
                        * (
                            x
                            - x_transition_guess
                        )
                    )
                )

                u = np.where(
                    x <= x_transition_guess,
                    u_light,
                    u_heavy,
                )

                up = np.gradient(
                    u,
                    x,
                )

                gate_width_x = (
                    1.0
                    / max(
                        gate_vacuum_k,
                        1.0e-6,
                    )
                )

                arg = np.clip(
                    (
                        x
                        - x_transition_guess
                    )
                    / gate_width_x,
                    -50.0,
                    50.0,
                )

                z = (
                    0.5
                    * (
                        1.0
                        + np.tanh(
                            arg
                        )
                    )
                )

                zp = np.gradient(
                    z,
                    x,
                )

                qprime = (
                    4.0
                    * math.pi
                    * omega_seed
                    * x**2
                    * y**2
                )

                qacc = cumulative_trapezoid(
                    x,
                    qprime,
                )

                if qacc[-1] > 0.0:
                    qacc *= (
                        target_q
                        / qacc[-1]
                    )

                state = np.vstack(
                    (
                        y,
                        yp,
                        u,
                        up,
                        z,
                        zp,
                        qacc,
                    )
                )

                return (
                    state,
                    omega_seed,
                )

            previous_rmax = (
                previous_solution.x[-1]
            )

            inside = (
                x <= previous_rmax
            )

            state = np.zeros(
                (
                    7,
                    len(x),
                ),
                dtype=float,
            )

            if np.any(
                inside
            ):
                state[
                    :,
                    inside,
                ] = previous_solution.sol(
                    x[
                        inside
                    ]
                )

            if np.any(
                ~inside
            ):
                xo = x[
                    ~inside
                ]

                omega_prev = float(
                    previous_solution.p[
                        0
                    ]
                )

                k_y = math.sqrt(
                    max(
                        1.0
                        - omega_prev**2,
                        1.0e-10,
                    )
                )

                boundary = previous_solution.sol(
                    previous_rmax
                )

                yb = float(
                    boundary[0]
                )

                ub = float(
                    boundary[2]
                )

                zb = float(
                    boundary[4]
                )

                qb = float(
                    boundary[6]
                )

                yout = (
                    yb
                    * previous_rmax
                    / xo
                    * np.exp(
                        -k_y
                        * (
                            xo
                            - previous_rmax
                        )
                    )
                )

                uout = (
                    ub
                    * previous_rmax
                    / xo
                    * np.exp(
                        -epsilon_off
                        * (
                            xo
                            - previous_rmax
                        )
                    )
                )

                eta_b = (
                    1.0
                    - zb
                )

                eta = (
                    eta_b
                    * previous_rmax
                    / xo
                    * np.exp(
                        -gate_vacuum_k
                        * (
                            xo
                            - previous_rmax
                        )
                    )
                )

                zout = (
                    1.0
                    - eta
                )

                state[
                    0,
                    ~inside,
                ] = yout

                state[
                    1,
                    ~inside,
                ] = (
                    -k_y
                    -1.0 / xo
                ) * yout

                state[
                    2,
                    ~inside,
                ] = uout

                state[
                    3,
                    ~inside,
                ] = (
                    -epsilon_off
                    -1.0 / xo
                ) * uout

                state[
                    4,
                    ~inside,
                ] = zout

                state[
                    5,
                    ~inside,
                ] = (
                    gate_vacuum_k
                    +1.0 / xo
                ) * eta

                state[
                    6,
                    ~inside,
                ] = qb

            return (
                state,
                float(
                    previous_solution.p[
                        0
                    ]
                ),
            )

        def solve_domain(
            rmax,
            previous_solution,
            tolerance,
        ):
            x = np.linspace(
                X0,
                rmax,
                INITIAL_POINTS,
            )

            guess, omega_guess = (
                make_initial_guess(
                    x,
                    rmax,
                    previous_solution,
                )
            )

            def equations(
                xx,
                state,
                parameters,
            ):
                omega = float(
                    parameters[0]
                )

                y = state[0]
                u = state[2]
                z = state[4]

                A = np.exp(
                    -0.5
                    * u**2
                )

                W = 0.5 * np.log1p(
                    y**2
                )

                return np.vstack(
                    (
                        state[1],

                        A
                        * y
                        / (
                            1.0
                            + y**2
                        )
                        - omega**2
                        * y
                        - 2.0
                        * state[1]
                        / xx,

                        state[3],

                        (
                            epsilon**2
                            + delta2
                            * z**2
                        )
                        * u
                        - chi**2
                        * A
                        * W
                        * u
                        - 2.0
                        * state[3]
                        / xx,

                        state[5],

                        (
                            a2
                            * (
                                z**2
                                - 1.0
                            )
                            + b2
                            * u**2
                        )
                        * z
                        - 2.0
                        * state[5]
                        / xx,

                        4.0
                        * math.pi
                        * omega
                        * xx**2
                        * y**2,
                    )
                )

            def boundary(
                left,
                right,
                parameters,
            ):
                omega = float(
                    parameters[0]
                )

                if not (
                    0.0
                    < omega
                    < 1.0
                ):
                    k_y = 1.0e-6
                else:
                    k_y = math.sqrt(
                        1.0
                        - omega**2
                    )

                return np.array(
                    (
                        left[1],
                        left[3],
                        left[5],
                        left[6],

                        right[1]
                        + (
                            k_y
                            +1.0 / rmax
                        )
                        * right[0],

                        right[3]
                        + (
                            epsilon_off
                            +1.0 / rmax
                        )
                        * right[2],

                        right[5]
                        - (
                            gate_vacuum_k
                            +1.0 / rmax
                        )
                        * (
                            1.0
                            - right[4]
                        ),

                        right[6]
                        - target_q,
                    ),
                    dtype=float,
                )

            result = solve_bvp(
                equations,
                boundary,
                x,
                guess,
                p=np.array(
                    [
                        omega_guess
                    ],
                    dtype=float,
                ),
                tol=tolerance,
                max_nodes=MAX_NODES,
                verbose=0,
            )

            return result

        for index, rmax in enumerate(
            RMAX_VALUES
        ):
            tolerance = (
                FINAL_TOL
                if index
                == len(
                    RMAX_VALUES
                ) - 1
                else BVP_TOL
            )

            result = solve_domain(
                rmax,
                previous,
                tolerance,
            )

            if not result.success:
                print(
                    f"DOMAIN RMAX={rmax:.1f} "
                    "SUCCESS=False "
                    f"MESSAGE={result.message}"
                )

                raise RuntimeError(
                    "Full fixed-Q y/u/z BVP failed at "
                    f"RMAX={rmax}: {result.message}"
                )

            omega = float(
                result.p[0]
            )

            center = result.sol(
                X0
            )

            outer = result.sol(
                rmax
            )

            q_end = float(
                outer[6]
            )

            q_rel = relerr(
                q_end,
                target_q,
            )

            max_rms = float(
                np.max(
                    result.rms_residuals
                )
            )

            row = {
                "rmax":
                    rmax,

                "omega":
                    omega,

                "u0":
                    float(
                        center[2]
                    ),

                "z0":
                    float(
                        center[4]
                    ),

                "z_outer":
                    float(
                        outer[4]
                    ),

                "u_outer":
                    float(
                        outer[2]
                    ),

                "Q_end":
                    q_end,

                "Q_relerr":
                    q_rel,

                "nodes":
                    int(
                        result.x.size
                    ),

                "max_rms_residual":
                    max_rms,
            }

            domain_rows.append(
                row
            )

            print(
                f"DOMAIN "
                f"RMAX={rmax:.1f} "
                f"OMEGA={omega:.12e} "
                f"U0={row['u0']:.12e} "
                f"Z0={row['z0']:.12e} "
                f"ZOUT={row['z_outer']:.12e} "
                f"Q_RELERR={q_rel:.6e} "
                f"NODES={row['nodes']} "
                f"RMS={max_rms:.6e}"
            )

            previous = result

        final = previous
        final_rmax = float(
            final.x[-1]
        )

        omega_final = float(
            final.p[0]
        )

        print(
            "\n=== STAGE C: FULL POSITIVE ENERGY LEDGER ==="
        )

        sample = np.linspace(
            X0,
            final_rmax,
            80_000,
        )

        state = final.sol(
            sample
        )

        y = np.asarray(
            state[0],
            dtype=float,
        )

        yp = np.asarray(
            state[1],
            dtype=float,
        )

        u = np.asarray(
            state[2],
            dtype=float,
        )

        up = np.asarray(
            state[3],
            dtype=float,
        )

        z = np.asarray(
            state[4],
            dtype=float,
        )

        zp = np.asarray(
            state[5],
            dtype=float,
        )

        W = 0.5 * np.log1p(
            y**2
        )

        source_inventory_density = (
            0.5
            * yp**2
            + 0.5
            * omega_final**2
            * y**2
            + W
        )

        phi_density = (
            (
                0.5
                * up**2
                + 0.5
                * epsilon**2
                * u**2
            )
            / chi**2
        )

        I_inventory_inside = (
            4.0
            * math.pi
            * np.trapezoid(
                sample**2
                * (
                    source_inventory_density
                    + phi_density
                ),
                sample,
            )
        )

        u_r = float(
            state[2, -1]
        )

        def scalar_outer_integrand(x):
            uo = (
                u_r
                * final_rmax
                / x
                * math.exp(
                    -epsilon_off
                    * (
                        x
                        - final_rmax
                    )
                )
            )

            upo = (
                -epsilon_off
                -1.0 / x
            ) * uo

            return (
                4.0
                * math.pi
                * x**2
                * (
                    0.5
                    * upo**2
                    +0.5
                    * epsilon**2
                    * uo**2
                )
                / chi**2
            )

        I_phi_outer = quad(
            scalar_outer_integrand,
            final_rmax,
            np.inf,
            epsabs=1.0e-14,
            epsrel=1.0e-9,
            limit=300,
        )[0]

        I_inventory = (
            I_inventory_inside
            + I_phi_outer
        )

        source_scalar_inventory_j = (
            I_inventory
            / m_x_gev
            * F_gev**2
            * J_PER_GEV
        )

        gate_prefactor_j = (
            4.0
            * math.pi
            * v_s_ev**2
            / m_x_ev
            * J_PER_EV
        )

        gate_density = (
            0.5
            * zp**2
            + a2
            / 4.0
            * (
                z**2
                -1.0
            )**2
            + 0.5
            * b2
            * u**2
            * z**2
        )

        gate_inside_j = (
            gate_prefactor_j
            * np.trapezoid(
                sample**2
                * gate_density,
                sample,
            )
        )

        z_r = float(
            z[-1]
        )

        eta_r = (
            1.0
            - z_r
        )

        def gate_outer_integrand(x):
            uo = (
                u_r
                * final_rmax
                / x
                * math.exp(
                    -epsilon_off
                    * (
                        x
                        - final_rmax
                    )
                )
            )

            eta = (
                eta_r
                * final_rmax
                / x
                * math.exp(
                    -gate_vacuum_k
                    * (
                        x
                        - final_rmax
                    )
                )
            )

            etaprime = (
                -gate_vacuum_k
                -1.0 / x
            ) * eta

            zo = (
                1.0
                - eta
            )

            return (
                x**2
                * (
                    0.5
                    * etaprime**2
                    + a2
                    / 4.0
                    * (
                        zo**2
                        -1.0
                    )**2
                    + 0.5
                    * b2
                    * uo**2
                    * zo**2
                )
            )

        gate_outer_j = (
            gate_prefactor_j
            * quad(
                gate_outer_integrand,
                final_rmax,
                np.inf,
                epsabs=1.0e-14,
                epsrel=1.0e-9,
                limit=300,
            )[0]
        )

        gate_total_j = (
            gate_inside_j
            + gate_outer_j
        )

        total_inventory_j = (
            source_scalar_inventory_j
            + gate_total_j
        )

        print(
            f"SOURCE_SCALAR_INVENTORY_GJ="
            f"{source_scalar_inventory_j / 1.0e9:.12f}"
        )

        print(
            f"GATE_POSITIVE_ENERGY_GJ="
            f"{gate_total_j / 1.0e9:.12f}"
        )

        print(
            f"TOTAL_GATED_INVENTORY_GJ="
            f"{total_inventory_j / 1.0e9:.12f}"
        )

        print(
            f"TOTAL_OVER_PREVIOUS_ROBUST="
            f"{total_inventory_j / operating_energy_j:.15e}"
        )

        print(
            "\n=== STAGE D: PAYLOAD-REGION RESPONSE PRESERVATION ==="
        )

        source_shift_m = float(
            operating[
                "shift_m"
            ]
        )

        payload_center_m = float(
            nominal_geometry[
                "payload_center_m"
            ]
        )

        payload_radius_m = float(
            nominal_geometry[
                "payload_radius_m"
            ]
        )

        payload_center_from_source_m = abs(
            payload_center_m
            - source_shift_m
        )

        payload_near_m = (
            payload_center_from_source_m
            - payload_radius_m
        )

        payload_far_m = (
            payload_center_from_source_m
            + payload_radius_m
        )

        x_length_m = (
            HBARC_EV_M
            / m_x_ev
        )

        x_payload_near = (
            payload_near_m
            / x_length_m
        )

        x_payload_center = (
            payload_center_from_source_m
            / x_length_m
        )

        x_payload_far = (
            payload_far_m
            / x_length_m
        )

        payload_points = (
            (
                "near",
                x_payload_near,
            ),
            (
                "center",
                x_payload_center,
            ),
            (
                "far",
                x_payload_far,
            ),
        )

        payload_ratios = []

        for label, xp in payload_points:
            gated_up = float(
                final.sol(
                    xp
                )[3]
            )

            baseline_up = float(
                baseline.sol(
                    xp
                )[3]
            )

            ratio = (
                abs(
                    gated_up
                )
                / max(
                    abs(
                        baseline_up
                    ),
                    1.0e-300,
                )
            )

            same_sign = bool(
                gated_up
                * baseline_up
                > 0.0
            )

            payload_ratios.append(
                ratio
            )

            print(
                f"PAYLOAD_{label.upper()} "
                f"X={xp:.9f} "
                f"BASE_UP={baseline_up:+.12e} "
                f"GATED_UP={gated_up:+.12e} "
                f"ABS_RATIO={ratio:.12e} "
                f"SAME_SIGN={same_sign}"
            )

        payload_preserved = bool(
            min(
                payload_ratios
            )
            >= PAYLOAD_GRADIENT_RATIO_MIN
        )

        print(
            f"PAYLOAD_GRADIENT_PRESERVED="
            f"{payload_preserved}"
        )

        print(
            "\n=== STAGE E: OFF-STATE EXACT BRANCH ==="
        )

        off_source_stable = bool(
            low[
                "source_slope_stable"
            ]
        )

        off_qball_bound = bool(
            low[
                "qball_bound_pass"
            ]
        )

        off_scalar_stable = bool(
            off_lambda0
            > OFF_STABILITY_MARGIN_MIN
        )

        off_gate_stable = bool(
            2.0
            * a2
            > 0.0
        )

        off_exact_branch_pass = bool(
            off_source_stable
            and
            off_qball_bound
            and
            off_scalar_stable
            and
            off_gate_stable
        )

        print(
            f"OFF_SOURCE_SLOPE_STABLE="
            f"{off_source_stable}"
        )

        print(
            f"OFF_QBALL_BOUND_PASS="
            f"{off_qball_bound}"
        )

        print(
            f"OFF_SCALAR_LAMBDA0_WITH_GATE="
            f"{off_lambda0:+.15e}"
        )

        print(
            f"OFF_SCALAR_STABLE="
            f"{off_scalar_stable}"
        )

        print(
            f"OFF_GATE_MASS2_HAT="
            f"{2.0 * a2:.15e}"
        )

        print(
            f"OFF_EXACT_FIXEDQ_BRANCH_PASS="
            f"{off_exact_branch_pass}"
        )

        print(
            "\n=== STAGE F: DOMAIN CONVERGENCE / DECISION ==="
        )

        last_three = domain_rows

        omega_values = [
            row[
                "omega"
            ]
            for row in last_three
        ]

        u0_values = [
            row[
                "u0"
            ]
            for row in last_three
        ]

        omega_spread = (
            max(
                omega_values
            )
            -min(
                omega_values
            )
        ) / max(
            abs(
                np.mean(
                    omega_values
                )
            ),
            1.0e-300,
        )

        u0_spread = (
            max(
                u0_values
            )
            -min(
                u0_values
            )
        ) / max(
            abs(
                np.mean(
                    u0_values
                )
            ),
            1.0e-300,
        )

        q_pass = bool(
            domain_rows[-1][
                "Q_relerr"
            ]
            <= Q_REL_TOL
        )

        on_branch_pass = bool(
            abs(
                domain_rows[-1][
                    "u0"
                ]
            )
            >= ON_U0_MIN
            and
            abs(
                domain_rows[-1][
                    "z0"
                ]
            )
            <= ON_Z0_MAX
            and
            0.0
            < omega_final
            < 1.0
        )

        domain_pass = bool(
            omega_spread
            <= DOMAIN_OMEGA_REL_TOL
            and
            u0_spread
            <= DOMAIN_U0_REL_TOL
        )

        positive_finite_energy = bool(
            math.isfinite(
                total_inventory_j
            )
            and
            total_inventory_j
            > 0.0
            and
            gate_total_j
            >= 0.0
        )

        print(
            f"OMEGA_DOMAIN_REL_SPREAD="
            f"{omega_spread:.15e}"
        )

        print(
            f"U0_DOMAIN_REL_SPREAD="
            f"{u0_spread:.15e}"
        )

        print(
            f"FIXED_Q_PASS="
            f"{q_pass}"
        )

        print(
            f"ON_BRANCH_NONTRIVIAL_PASS="
            f"{on_branch_pass}"
        )

        print(
            f"DOMAIN_CONVERGENCE_PASS="
            f"{domain_pass}"
        )

        print(
            f"POSITIVE_FINITE_TOTAL_ENERGY_PASS="
            f"{positive_finite_energy}"
        )

        green = bool(
            q_pass
            and
            on_branch_pass
            and
            domain_pass
            and
            positive_finite_energy
            and
            payload_preserved
            and
            off_exact_branch_pass
        )

        if green:
            classification = (
                "GREEN_D2C_FULL_FIXEDQ_MICROSCOPIC_"
                "X_PHI_GATE_ON_OFF_EXISTENCE_AND_RECIPROCITY"
            )

            next_action = (
                "031D2D_COUPLED_Y_U_Z_STABILITY_"
                "AND_SWITCHING_BARRIER_RESET_ENERGY"
            )

        else:
            classification = (
                "YELLOW_D2C_FULL_FIXEDQ_GATE_"
                "HAS_UNCLOSED_EXISTENCE_OR_CONVERGENCE_SUBGATE"
            )

            next_action = (
                "REFINE_ONLY_FAILED_D2C_SUBGATE"
            )

        print(
            f"031D2C_CLASSIFICATION="
            f"{classification}"
        )

        print(
            f"NEXT={next_action}"
        )

        print(
            "FULL_COUPLED_Y_U_Z_LINEAR_STABILITY_CLOSED=NO"
        )

        print(
            "SWITCHING_BARRIER_CLOSED=NO"
        )

        print(
            "FORMATION_RESET_ENERGY_CLOSED=NO"
        )

        print(
            "RADIATION_CLOSED=NO"
        )

        print(
            "FULL_PHYSICAL_METRIC_BACKREACTION_CLOSED=NO"
        )

        print(
            "EFT_NATURALNESS_CLOSED=NO"
        )

        print(
            "EMPIRICAL_FIFTH_FORCE_EPPPN_CLOSED=NO"
        )

        print(
            "PRACTICAL_DEVICE=NO"
        )

        summary = {
            "classification":
                classification,

            "next":
                next_action,

            "gate_candidate": {
                "g_s":
                    G_S,

                "v_s_eV":
                    v_s_ev,

                "lambda_s":
                    lambda_s,

                "m_s_eV":
                    M_S_EV,

                "a2":
                    a2,

                "b2":
                    b2,

                "delta2":
                    delta2,
            },

            "fixed_Q": {
                "target":
                    target_q,

                "omega_final":
                    omega_final,

                "Q_relerr":
                    domain_rows[-1][
                        "Q_relerr"
                    ],
            },

            "domain_rows":
                domain_rows,

            "energy": {
                "previous_robust_J":
                    operating_energy_j,

                "source_scalar_inventory_J":
                    source_scalar_inventory_j,

                "gate_positive_energy_J":
                    gate_total_j,

                "total_gated_inventory_J":
                    total_inventory_j,

                "total_over_previous":
                    total_inventory_j
                    / operating_energy_j,
            },

            "payload": {
                "gradient_ratios":
                    payload_ratios,

                "preserved":
                    payload_preserved,
            },

            "off_state": {
                "exact_branch":
                    True,

                "source_slope_stable":
                    off_source_stable,

                "qball_bound":
                    off_qball_bound,

                "scalar_lambda0_with_gate":
                    off_lambda0,

                "scalar_stable":
                    off_scalar_stable,

                "gate_mass2_hat":
                    2.0
                    * a2,

                "pass":
                    off_exact_branch_pass,
            },

            "claim_limits": [
                (
                    "This run permits the microscopic Q-ball source "
                    "to react self-consistently to the auxiliary gate."
                ),
                (
                    "The solved parameter Omega enforces the same "
                    "Noether charge as the certified source."
                ),
                (
                    "Positive canonical gate energy and reciprocal "
                    "phi-s interaction are included."
                ),
                (
                    "The OFF state is the exact u=0,z=1 fixed-Q branch."
                ),
                (
                    "Coupled y/u/z perturbative stability remains open."
                ),
                (
                    "Switching/nucleation, reset energy and radiation "
                    "remain open."
                ),
                (
                    "Full Einstein/physical-metric backreaction, "
                    "EFT naturalness and empirical closure remain open."
                ),
                (
                    "No practical device is established."
                ),
            ],
        }

        OUT_JSON.write_text(
            json.dumps(
                builtin(summary),
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )

        fields = sorted(
            {
                key
                for row in domain_rows
                for key in row.keys()
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
                domain_rows
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}"
        )

        print(
            f"DOMAIN_CSV={OUT_CSV}"
        )

    finally:
        qmod.X_MATCH = old_x_match


if __name__ == "__main__":
    main()
