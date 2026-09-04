"""
031D2C-R — logarithmic-gate fixed-Q homotopy solve

Repairs repeated direct-z BVP failures.

Problem
-------
The physical ON solution requires

    z = s/v_s

to be exponentially suppressed in the Q-ball core and approach one
outside. Direct collocation in z therefore spans an extreme dynamic
range even when the portal coefficient itself is modest.

Use

    q = log(z)

instead.

Then

    z = exp(q)

and the exact gate equation is

    q'' + 2q'/x + q'^2
      = a2 (exp(2q)-1) + b2 u^2.

The full physical final equations are

    y'' + 2y'/x
      = A(u) y/(1+y^2) - Omega^2 y

    u'' + 2u'/x
      = [epsilon^2 + delta2 exp(2q)] u
        - chi^2 A(u) W(y) u

    q'' + 2q'/x + q'^2
      = a2(exp(2q)-1) + b2 u^2.

Noether charge is fixed by solving Omega as a BVP parameter.

Numerical homotopy
------------------
At continuation parameter t=0, the gate feels the scalar background
but does not backreact on u:

    u equation gate term -> t * delta2 exp(2q) u.

The known Q-ball + scalar state is therefore an exact starting branch.
t is then continued to 1.

Intermediate t values are numerical continuation devices only.
Only t=1 represents the reciprocal target theory.

If the t=1 branch exists, this run prices the complete positive
canonical gate energy, checks finite payload response and domain
convergence, and verifies the exact fixed-Q OFF branch stabilization.

Open afterward:
- coupled perturbative y/u/q stability;
- switching/nucleation/reset/radiation;
- full physical metric / Einstein backreaction;
- EFT/naturalness and empirical constraints;
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
    / "031d2cr_loggate_homotopy_summary.json"
)

OUT_HOMOTOPY = (
    DATA
    / "031d2cr_homotopy_scan.csv"
)

OUT_DOMAIN = (
    DATA
    / "031d2cr_domain_scan.csv"
)


X0 = 1.0e-5
X_MATCH = 80.0

RMAX_INITIAL = 320.0

RMAX_FINAL_VALUES = (
    320.0,
    450.0,
    600.0,
)

# Conditioning-balanced D2C candidate.
G_S = 3.0e-16
M_S_EV = 2.0719332942e-7

STABILIZATION_MARGIN = 1.20

BVP_TOL_HOMOTOPY = 2.0e-5
BVP_TOL_FINAL = 7.0e-6

MAX_NODES = 120_000

INITIAL_HOMOTOPY_STEP = 0.10
MIN_HOMOTOPY_STEP = 0.005

Q_REL_TOL = 3.0e-6

DOMAIN_OMEGA_REL_TOL = 5.0e-4
DOMAIN_U0_REL_TOL = 5.0e-3
DOMAIN_ENERGY_REL_TOL = 2.0e-2

PAYLOAD_GRADIENT_RATIO_MIN = 0.90

ON_U0_MIN = 0.20
ON_Z0_MAX = 1.0e-3

OFF_STABILITY_MARGIN_MIN = 1.0e-4

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
            str(k): builtin(v)
            for k, v in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            builtin(v)
            for v in value
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


def safe_exp2q(q):
    return np.exp(
        2.0
        * np.clip(
            q,
            -400.0,
            10.0,
        )
    )


def safe_z(q):
    return np.exp(
        np.clip(
            q,
            -745.0,
            10.0,
        )
    )


def make_grid(
    rmax: float,
    transition_x: float,
):
    pieces = []

    pieces.append(
        np.linspace(
            X0,
            min(
                X_MATCH,
                rmax,
            ),
            1800,
        )
    )

    if rmax > X_MATCH:
        left_wall = max(
            X_MATCH,
            transition_x - 100.0,
        )

        if left_wall > X_MATCH:
            pieces.append(
                np.linspace(
                    X_MATCH,
                    left_wall,
                    700,
                )
            )

        right_wall = min(
            rmax,
            transition_x + 120.0,
        )

        if right_wall > left_wall:
            pieces.append(
                np.linspace(
                    left_wall,
                    right_wall,
                    2200,
                )
            )

        if rmax > right_wall:
            pieces.append(
                np.linspace(
                    right_wall,
                    rmax,
                    900,
                )
            )

    return np.unique(
        np.concatenate(
            pieces
        )
    )


def main():
    print(
        "=== 031D2C-R LOG-GATE FIXED-Q HOMOTOPY ==="
    )

    print(
        "DIRECT_Z_COLLOCATION=REMOVED"
    )

    print(
        "GATE_VARIABLE=q=LOG_Z"
    )

    print(
        "FIXED_NOETHER_CHARGE=YES"
    )

    print(
        "SOURCE_REACTION_AT_FINAL_T1=YES"
    )

    print(
        "RECIPROCAL_TARGET_THEORY_AT_T1=YES"
    )

    print(
        "INTERMEDIATE_HOMOTOPY_PHYSICAL=NO"
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
            "031D1 gate-free closure is missing"
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

    gate_k = math.sqrt(
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

    u_transition = math.sqrt(
        a2 / b2
    )

    x_length_m = (
        HBARC_EV_M
        / m_x_ev
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
        f"A2_GATE={a2:.15e}"
    )

    print(
        f"B2_GATE={b2:.15e}"
    )

    print(
        f"DELTA2_GATE={delta2:.15e}"
    )

    print(
        f"U_TRANSITION={u_transition:.15e}"
    )

    print(
        f"OFF_FIXEDQ_SCALAR_LAMBDA0="
        f"{off_lambda0:+.15e}"
    )

    qmod = load_module(
        "qball031d2cr",
        QBALL_SOURCE,
    )

    old_x_match = float(
        qmod.X_MATCH
    )

    qmod.X_MATCH = X_MATCH

    try:
        print(
            "\n=== STAGE A: RECONSTRUCT UNGATED FIXED-Q ON STATE ==="
        )

        seed = qmod.solve_uncoupled_qball(
            omega_seed
        )

        if seed is None:
            raise RuntimeError(
                "Failed Q-ball seed"
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
                "Failed baseline coupled source"
            )

        y80 = float(
            baseline.sol(
                X_MATCH
            )[0]
        )

        u80 = float(
            baseline.sol(
                X_MATCH
            )[2]
        )

        k_y_seed = math.sqrt(
            1.0
            - omega_seed**2
        )

        def baseline_y(x):
            xx = np.asarray(
                x,
                dtype=float,
            )

            result = np.empty_like(
                xx
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

        def baseline_yp(x):
            xx = np.asarray(
                x,
                dtype=float,
            )

            result = np.empty_like(
                xx
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

        def baseline_u(x):
            xx = np.asarray(
                x,
                dtype=float,
            )

            result = np.empty_like(
                xx
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

        def baseline_up(x):
            xx = np.asarray(
                x,
                dtype=float,
            )

            result = np.empty_like(
                xx
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
                )[3]

            if np.any(
                ~inside
            ):
                xo = xx[
                    ~inside
                ]

                uo = (
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

                result[
                    ~inside
                ] = (
                    -epsilon
                    -1.0 / xo
                ) * uo

            return result

        x_hi = 200.0

        while (
            float(
                baseline_u(
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
                    "Could not bracket gate transition"
                )

        from scipy.optimize import brentq

        x_transition = brentq(
            lambda x:
                float(
                    baseline_u(
                        np.array(
                            [x]
                        )
                    )[0]
                )
                -u_transition,
            X_MATCH,
            x_hi,
        )

        print(
            f"INITIAL_TRANSITION_X="
            f"{x_transition:.15e}"
        )

        print(
            f"INITIAL_TRANSITION_M="
            f"{x_transition*x_length_m:.15e}"
        )

        print(
            "\n=== STAGE B: SPECTATOR LOG-GATE SOLVE ==="
        )

        grid = make_grid(
            RMAX_INITIAL,
            x_transition,
        )

        u_bg = baseline_u(
            grid
        )

        coefficient = (
            b2
            * u_bg**2
            -a2
        )

        k_inner = np.sqrt(
            np.maximum(
                coefficient,
                0.0,
            )
        )

        transition_index = int(
            np.argmin(
                np.abs(
                    grid
                    -x_transition
                )
            )
        )

        q_guess = np.empty_like(
            grid
        )

        q_at_transition = -1.0

        # WKB-like inner logarithmic suppression.
        q_guess[
            transition_index
        ] = q_at_transition

        for i in range(
            transition_index - 1,
            -1,
            -1,
        ):
            dx = (
                grid[
                    i + 1
                ]
                -grid[i]
            )

            q_guess[i] = (
                q_guess[
                    i + 1
                ]
                -0.5
                * (
                    k_inner[i]
                    +k_inner[
                        i + 1
                    ]
                )
                * dx
            )

        # Smooth approach to q=0 outside.
        outer_width = (
            1.0
            / max(
                gate_k,
                1.0e-8,
            )
        )

        for i in range(
            transition_index + 1,
            len(grid),
        ):
            dx = (
                grid[i]
                -x_transition
            )

            q_guess[i] = (
                q_at_transition
                * math.exp(
                    -dx
                    / outer_width
                )
            )

        qp_guess = np.gradient(
            q_guess,
            grid,
        )

        def spectator_equations(
            x,
            state,
        ):
            q = state[0]

            u = baseline_u(
                x
            )

            z2 = safe_exp2q(
                q
            )

            return np.vstack(
                (
                    state[1],

                    a2
                    * (
                        z2
                        -1.0
                    )
                    +b2
                    * u**2
                    -state[1]**2
                    -2.0
                    * state[1]
                    / x,
                )
            )

        def spectator_boundary(
            left,
            right,
        ):
            q_right = float(
                right[0]
            )

            robin_ratio = np.expm1(
                np.clip(
                    -q_right,
                    -50.0,
                    50.0,
                )
            )

            return np.array(
                (
                    left[1],

                    right[1]
                    -(
                        gate_k
                        +1.0
                        /RMAX_INITIAL
                    )
                    * robin_ratio,
                ),
                dtype=float,
            )

        spectator = solve_bvp(
            spectator_equations,
            spectator_boundary,
            grid,
            np.vstack(
                (
                    q_guess,
                    qp_guess,
                )
            ),
            tol=1.0e-5,
            max_nodes=80_000,
            verbose=0,
        )

        if not spectator.success:
            raise RuntimeError(
                "Spectator log-gate BVP failed: "
                f"{spectator.message}"
            )

        q0_spectator = float(
            spectator.sol(
                X0
            )[0]
        )

        z0_spectator = float(
            safe_z(
                q0_spectator
            )
        )

        print(
            f"SPECTATOR_Q0="
            f"{q0_spectator:.15e}"
        )

        print(
            f"SPECTATOR_Z0="
            f"{z0_spectator:.15e}"
        )

        print(
            f"SPECTATOR_NODES="
            f"{spectator.x.size}"
        )

        print(
            f"SPECTATOR_MAX_RMS="
            f"{float(np.max(spectator.rms_residuals)):.15e}"
        )

        print(
            "\n=== STAGE C: FIXED-Q HOMOTOPY TO FULL RECIPROCITY ==="
        )

        qacc_prime = (
            4.0
            * math.pi
            * omega_seed
            * grid**2
            * baseline_y(
                grid
            )**2
        )

        qacc = cumulative_trapezoid(
            grid,
            qacc_prime,
        )

        if qacc[-1] <= 0.0:
            raise RuntimeError(
                "Invalid baseline Noether accumulator"
            )

        qacc *= (
            target_q
            / qacc[-1]
        )

        initial_state = np.vstack(
            (
                baseline_y(
                    grid
                ),
                baseline_yp(
                    grid
                ),
                baseline_u(
                    grid
                ),
                baseline_up(
                    grid
                ),
                spectator.sol(
                    grid
                )[0],
                spectator.sol(
                    grid
                )[1],
                qacc,
            )
        )

        def solve_at_t(
            t_value: float,
            previous_solution,
            first_guess=None,
            tolerance=BVP_TOL_HOMOTOPY,
        ):
            rmax = RMAX_INITIAL

            if previous_solution is None:
                x = grid
                guess = first_guess

                omega_guess = (
                    omega_seed
                )

            else:
                x = previous_solution.x
                guess = previous_solution.y

                omega_guess = float(
                    previous_solution.p[
                        0
                    ]
                )

            epsilon_outer = math.sqrt(
                epsilon**2
                +t_value
                *delta2
            )

            def equations(
                x,
                state,
                parameters,
            ):
                omega = float(
                    parameters[0]
                )

                y = state[0]
                u = state[2]
                q = state[4]
                qp = state[5]

                A = np.exp(
                    -0.5
                    * u**2
                )

                W = 0.5 * np.log1p(
                    y**2
                )

                z2 = safe_exp2q(
                    q
                )

                return np.vstack(
                    (
                        state[1],

                        A
                        * y
                        /(
                            1.0
                            +y**2
                        )
                        -omega**2
                        * y
                        -2.0
                        * state[1]
                        /x,

                        state[3],

                        (
                            epsilon**2
                            +t_value
                            *delta2
                            *z2
                        )
                        *u
                        -chi**2
                        *A
                        *W
                        *u
                        -2.0
                        *state[3]
                        /x,

                        qp,

                        a2
                        *(
                            z2
                            -1.0
                        )
                        +b2
                        *u**2
                        -qp**2
                        -2.0
                        *qp
                        /x,

                        4.0
                        *math.pi
                        *omega
                        *x**2
                        *y**2,
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

                k_y = math.sqrt(
                    max(
                        1.0
                        -omega**2,
                        1.0e-10,
                    )
                )

                q_right = float(
                    right[4]
                )

                gate_robin_ratio = np.expm1(
                    np.clip(
                        -q_right,
                        -50.0,
                        50.0,
                    )
                )

                return np.array(
                    (
                        left[1],
                        left[3],
                        left[5],
                        left[6],

                        right[1]
                        +(
                            k_y
                            +1.0
                            /rmax
                        )
                        *right[0],

                        right[3]
                        +(
                            epsilon_outer
                            +1.0
                            /rmax
                        )
                        *right[2],

                        right[5]
                        -(
                            gate_k
                            +1.0
                            /rmax
                        )
                        *gate_robin_ratio,

                        right[6]
                        -target_q,
                    ),
                    dtype=float,
                )

            return solve_bvp(
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

        homotopy_rows = []

        current = solve_at_t(
            0.0,
            None,
            first_guess=initial_state,
        )

        if not current.success:
            raise RuntimeError(
                "t=0 log-gate branch solve failed: "
                f"{current.message}"
            )

        t_current = 0.0
        step = INITIAL_HOMOTOPY_STEP

        while t_current < 1.0 - 1.0e-12:
            t_trial = min(
                1.0,
                t_current + step,
            )

            trial = solve_at_t(
                t_trial,
                current,
            )

            if not trial.success:
                step *= 0.5

                print(
                    f"HOMOTOPY_RETRY "
                    f"T_CURRENT={t_current:.6f} "
                    f"T_TRIAL={t_trial:.6f} "
                    f"NEW_STEP={step:.6f} "
                    f"MESSAGE={trial.message}"
                )

                if step < MIN_HOMOTOPY_STEP:
                    raise RuntimeError(
                        "Physical t=1 branch could not be "
                        "continued: homotopy step fell below "
                        f"{MIN_HOMOTOPY_STEP}"
                    )

                continue

            t_current = t_trial
            current = trial

            center = current.sol(
                X0
            )

            outer = current.sol(
                RMAX_INITIAL
            )

            q0 = float(
                center[4]
            )

            z0 = float(
                safe_z(
                    q0
                )
            )

            z_outer = float(
                safe_z(
                    outer[4]
                )
            )

            q_rel = relerr(
                float(
                    outer[6]
                ),
                target_q,
            )

            row = {
                "t":
                    t_current,

                "omega":
                    float(
                        current.p[0]
                    ),

                "u0":
                    float(
                        center[2]
                    ),

                "q0":
                    q0,

                "z0":
                    z0,

                "z_outer":
                    z_outer,

                "Q_relerr":
                    q_rel,

                "nodes":
                    int(
                        current.x.size
                    ),

                "max_rms_residual":
                    float(
                        np.max(
                            current.rms_residuals
                        )
                    ),
            }

            homotopy_rows.append(
                row
            )

            print(
                f"HOMOTOPY "
                f"T={t_current:.6f} "
                f"OMEGA={row['omega']:.12e} "
                f"U0={row['u0']:.12e} "
                f"Q0={row['q0']:.12e} "
                f"Z0={row['z0']:.12e} "
                f"ZOUT={row['z_outer']:.12e} "
                f"Q_RELERR={q_rel:.6e} "
                f"NODES={row['nodes']} "
                f"RMS={row['max_rms_residual']:.6e}"
            )

            step = min(
                INITIAL_HOMOTOPY_STEP,
                step * 1.4,
            )

        if abs(
            t_current
            -1.0
        ) > 1.0e-12:
            raise RuntimeError(
                "Homotopy did not reach physical t=1"
            )

        print(
            "\n=== STAGE D: PHYSICAL T=1 DOMAIN CONVERGENCE ==="
        )

        physical = current
        domain_rows = []

        def extend_guess(
            previous,
            rmax,
        ):
            x_old_max = float(
                previous.x[-1]
            )

            transition_estimate = (
                x_transition
            )

            x = make_grid(
                rmax,
                transition_estimate,
            )

            state = np.zeros(
                (
                    7,
                    len(x),
                ),
                dtype=float,
            )

            inside = (
                x <= x_old_max
            )

            state[
                :,
                inside,
            ] = previous.sol(
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

                boundary = previous.sol(
                    x_old_max
                )

                omega = float(
                    previous.p[0]
                )

                k_y = math.sqrt(
                    max(
                        1.0
                        -omega**2,
                        1.0e-10,
                    )
                )

                yb = float(
                    boundary[0]
                )

                ub = float(
                    boundary[2]
                )

                qb = float(
                    boundary[4]
                )

                qacc_b = float(
                    boundary[6]
                )

                yout = (
                    yb
                    *x_old_max
                    /xo
                    *np.exp(
                        -k_y
                        *(
                            xo
                            -x_old_max
                        )
                    )
                )

                uout = (
                    ub
                    *x_old_max
                    /xo
                    *np.exp(
                        -epsilon_off
                        *(
                            xo
                            -x_old_max
                        )
                    )
                )

                z_b = float(
                    safe_z(
                        qb
                    )
                )

                eta_b = max(
                    1.0
                    -z_b,
                    0.0,
                )

                eta = (
                    eta_b
                    *x_old_max
                    /xo
                    *np.exp(
                        -gate_k
                        *(
                            xo
                            -x_old_max
                        )
                    )
                )

                zout = np.clip(
                    1.0
                    -eta,
                    1.0e-300,
                    1.0,
                )

                qout = np.log(
                    zout
                )

                qpout = (
                    (
                        gate_k
                        +1.0
                        /xo
                    )
                    *eta
                    /zout
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
                    -1.0
                    /xo
                ) *yout

                state[
                    2,
                    ~inside,
                ] = uout

                state[
                    3,
                    ~inside,
                ] = (
                    -epsilon_off
                    -1.0
                    /xo
                ) *uout

                state[
                    4,
                    ~inside,
                ] = qout

                state[
                    5,
                    ~inside,
                ] = qpout

                state[
                    6,
                    ~inside,
                ] = qacc_b

            return x, state

        def solve_physical_domain(
            previous,
            rmax,
            tolerance,
        ):
            if abs(
                previous.x[-1]
                -rmax
            ) < 1.0e-12:
                x = previous.x
                guess = previous.y
            else:
                x, guess = extend_guess(
                    previous,
                    rmax,
                )

            omega_guess = float(
                previous.p[0]
            )

            def equations(
                x,
                state,
                parameters,
            ):
                omega = float(
                    parameters[0]
                )

                y = state[0]
                u = state[2]
                q = state[4]
                qp = state[5]

                A = np.exp(
                    -0.5
                    *u**2
                )

                W = 0.5 * np.log1p(
                    y**2
                )

                z2 = safe_exp2q(
                    q
                )

                return np.vstack(
                    (
                        state[1],

                        A
                        *y
                        /(
                            1.0
                            +y**2
                        )
                        -omega**2
                        *y
                        -2.0
                        *state[1]
                        /x,

                        state[3],

                        (
                            epsilon**2
                            +delta2
                            *z2
                        )
                        *u
                        -chi**2
                        *A
                        *W
                        *u
                        -2.0
                        *state[3]
                        /x,

                        qp,

                        a2
                        *(
                            z2
                            -1.0
                        )
                        +b2
                        *u**2
                        -qp**2
                        -2.0
                        *qp
                        /x,

                        4.0
                        *math.pi
                        *omega
                        *x**2
                        *y**2,
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

                k_y = math.sqrt(
                    max(
                        1.0
                        -omega**2,
                        1.0e-10,
                    )
                )

                q_right = float(
                    right[4]
                )

                gate_ratio = np.expm1(
                    np.clip(
                        -q_right,
                        -50.0,
                        50.0,
                    )
                )

                return np.array(
                    (
                        left[1],
                        left[3],
                        left[5],
                        left[6],

                        right[1]
                        +(
                            k_y
                            +1.0
                            /rmax
                        )
                        *right[0],

                        right[3]
                        +(
                            epsilon_off
                            +1.0
                            /rmax
                        )
                        *right[2],

                        right[5]
                        -(
                            gate_k
                            +1.0
                            /rmax
                        )
                        *gate_ratio,

                        right[6]
                        -target_q,
                    ),
                    dtype=float,
                )

            return solve_bvp(
                equations,
                boundary,
                x,
                guess,
                p=np.array(
                    [
                        omega_guess
                    ]
                ),
                tol=tolerance,
                max_nodes=MAX_NODES,
                verbose=0,
            )

        for rmax in RMAX_FINAL_VALUES:
            if abs(
                physical.x[-1]
                -rmax
            ) < 1.0e-12:
                result = solve_physical_domain(
                    physical,
                    rmax,
                    BVP_TOL_FINAL,
                )
            else:
                result = solve_physical_domain(
                    physical,
                    rmax,
                    BVP_TOL_FINAL,
                )

            if not result.success:
                raise RuntimeError(
                    f"t=1 domain solve failed at "
                    f"RMAX={rmax}: {result.message}"
                )

            center = result.sol(
                X0
            )

            outer = result.sol(
                rmax
            )

            q0 = float(
                center[4]
            )

            row = {
                "rmax":
                    rmax,

                "omega":
                    float(
                        result.p[0]
                    ),

                "u0":
                    float(
                        center[2]
                    ),

                "q0":
                    q0,

                "z0":
                    float(
                        safe_z(
                            q0
                        )
                    ),

                "z_outer":
                    float(
                        safe_z(
                            outer[4]
                        )
                    ),

                "Q_relerr":
                    relerr(
                        float(
                            outer[6]
                        ),
                        target_q,
                    ),

                "nodes":
                    int(
                        result.x.size
                    ),

                "max_rms_residual":
                    float(
                        np.max(
                            result.rms_residuals
                        )
                    ),
            }

            domain_rows.append(
                row
            )

            print(
                f"DOMAIN "
                f"RMAX={rmax:.1f} "
                f"OMEGA={row['omega']:.12e} "
                f"U0={row['u0']:.12e} "
                f"Q0={row['q0']:.12e} "
                f"Z0={row['z0']:.12e} "
                f"ZOUT={row['z_outer']:.12e} "
                f"Q_RELERR={row['Q_relerr']:.6e} "
                f"NODES={row['nodes']} "
                f"RMS={row['max_rms_residual']:.6e}"
            )

            physical = result

        print(
            "\n=== STAGE E: COMPLETE POSITIVE ENERGY LEDGER ==="
        )

        rmax = float(
            physical.x[-1]
        )

        omega_final = float(
            physical.p[0]
        )

        sample = np.linspace(
            X0,
            rmax,
            100_000,
        )

        state = physical.sol(
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

        q = np.asarray(
            state[4],
            dtype=float,
        )

        qp = np.asarray(
            state[5],
            dtype=float,
        )

        z = safe_z(
            q
        )

        zp = (
            qp
            *z
        )

        W = 0.5 * np.log1p(
            y**2
        )

        source_inventory_density = (
            0.5
            *yp**2
            +0.5
            *omega_final**2
            *y**2
            +W
        )

        scalar_density = (
            (
                0.5
                *up**2
                +0.5
                *epsilon**2
                *u**2
            )
            /chi**2
        )

        I_source_scalar_inside = (
            4.0
            *math.pi
            *np.trapezoid(
                sample**2
                *(
                    source_inventory_density
                    +scalar_density
                ),
                sample,
            )
        )

        u_r = float(
            u[-1]
        )

        def scalar_outer_integrand(x):
            uo = (
                u_r
                *rmax
                /x
                *math.exp(
                    -epsilon_off
                    *(
                        x
                        -rmax
                    )
                )
            )

            upo = (
                -epsilon_off
                -1.0
                /x
            ) *uo

            return (
                4.0
                *math.pi
                *x**2
                *(
                    0.5
                    *upo**2
                    +0.5
                    *epsilon**2
                    *uo**2
                )
                /chi**2
            )

        I_scalar_outer = quad(
            scalar_outer_integrand,
            rmax,
            np.inf,
            epsabs=1.0e-14,
            epsrel=1.0e-9,
            limit=300,
        )[0]

        I_inventory = (
            I_source_scalar_inside
            +I_scalar_outer
        )

        source_scalar_inventory_j = (
            I_inventory
            /m_x_gev
            *F_gev**2
            *J_PER_GEV
        )

        gate_prefactor_j = (
            4.0
            *math.pi
            *v_s_ev**2
            /m_x_ev
            *J_PER_EV
        )

        gate_density = (
            0.5
            *zp**2
            +a2
            /4.0
            *(
                z**2
                -1.0
            )**2
            +0.5
            *b2
            *u**2
            *z**2
        )

        gate_inside_j = (
            gate_prefactor_j
            *np.trapezoid(
                sample**2
                *gate_density,
                sample,
            )
        )

        q_r = float(
            q[-1]
        )

        z_r = float(
            z[-1]
        )

        eta_r = max(
            1.0
            -z_r,
            0.0,
        )

        def gate_outer_integrand(x):
            uo = (
                u_r
                *rmax
                /x
                *math.exp(
                    -epsilon_off
                    *(
                        x
                        -rmax
                    )
                )
            )

            eta = (
                eta_r
                *rmax
                /x
                *math.exp(
                    -gate_k
                    *(
                        x
                        -rmax
                    )
                )
            )

            etap = (
                -gate_k
                -1.0
                /x
            ) *eta

            zo = (
                1.0
                -eta
            )

            return (
                x**2
                *(
                    0.5
                    *etap**2
                    +a2
                    /4.0
                    *(
                        zo**2
                        -1.0
                    )**2
                    +0.5
                    *b2
                    *uo**2
                    *zo**2
                )
            )

        gate_outer_j = (
            gate_prefactor_j
            *quad(
                gate_outer_integrand,
                rmax,
                np.inf,
                epsabs=1.0e-14,
                epsrel=1.0e-9,
                limit=300,
            )[0]
        )

        gate_total_j = (
            gate_inside_j
            +gate_outer_j
        )

        total_inventory_j = (
            source_scalar_inventory_j
            +gate_total_j
        )

        print(
            f"SOURCE_SCALAR_INVENTORY_GJ="
            f"{source_scalar_inventory_j/1.0e9:.12f}"
        )

        print(
            f"GATE_POSITIVE_ENERGY_GJ="
            f"{gate_total_j/1.0e9:.12f}"
        )

        print(
            f"TOTAL_GATED_INVENTORY_GJ="
            f"{total_inventory_j/1.0e9:.12f}"
        )

        print(
            f"TOTAL_OVER_PREVIOUS_ROBUST="
            f"{total_inventory_j/operating_energy_j:.15e}"
        )

        print(
            "\n=== STAGE F: PAYLOAD RESPONSE ==="
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
            -source_shift_m
        )

        payload_points_m = (
            (
                "near",
                payload_center_from_source_m
                -payload_radius_m,
            ),
            (
                "center",
                payload_center_from_source_m,
            ),
            (
                "far",
                payload_center_from_source_m
                +payload_radius_m,
            ),
        )

        payload_ratios = []
        payload_signs = []

        for label, radius_m in payload_points_m:
            xp = (
                radius_m
                /x_length_m
            )

            gated_up = float(
                physical.sol(
                    xp
                )[3]
            )

            baseline_up_value = float(
                baseline.sol(
                    xp
                )[3]
            )

            ratio = (
                abs(
                    gated_up
                )
                /max(
                    abs(
                        baseline_up_value
                    ),
                    1.0e-300,
                )
            )

            same_sign = bool(
                gated_up
                *baseline_up_value
                >0.0
            )

            payload_ratios.append(
                ratio
            )

            payload_signs.append(
                same_sign
            )

            print(
                f"PAYLOAD_{label.upper()} "
                f"R_M={radius_m:.9f} "
                f"BASE_UP={baseline_up_value:+.12e} "
                f"GATED_UP={gated_up:+.12e} "
                f"ABS_RATIO={ratio:.12e} "
                f"SAME_SIGN={same_sign}"
            )

        payload_pass = bool(
            min(
                payload_ratios
            )
            >=PAYLOAD_GRADIENT_RATIO_MIN
            and
            all(
                payload_signs
            )
        )

        print(
            f"PAYLOAD_GRADIENT_PRESERVED="
            f"{payload_pass}"
        )

        print(
            "\n=== STAGE G: OFF STATE AND FINAL DECISION ==="
        )

        off_source_pass = bool(
            low[
                "source_slope_stable"
            ]
            and
            low[
                "qball_bound_pass"
            ]
        )

        off_scalar_pass = bool(
            off_lambda0
            >OFF_STABILITY_MARGIN_MIN
        )

        off_gate_pass = bool(
            2.0
            *a2
            >0.0
        )

        off_pass = bool(
            off_source_pass
            and
            off_scalar_pass
            and
            off_gate_pass
        )

        omega_values = np.array(
            [
                row[
                    "omega"
                ]
                for row
                in domain_rows
            ],
            dtype=float,
        )

        u0_values = np.array(
            [
                row[
                    "u0"
                ]
                for row
                in domain_rows
            ],
            dtype=float,
        )

        omega_spread = (
            np.max(
                omega_values
            )
            -np.min(
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
            np.max(
                u0_values
            )
            -np.min(
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

        final_center = physical.sol(
            X0
        )

        final_outer = physical.sol(
            rmax
        )

        final_z0 = float(
            safe_z(
                final_center[4]
            )
        )

        fixed_q_pass = bool(
            relerr(
                float(
                    final_outer[6]
                ),
                target_q,
            )
            <=Q_REL_TOL
        )

        on_branch_pass = bool(
            abs(
                float(
                    final_center[2]
                )
            )
            >=ON_U0_MIN
            and
            final_z0
            <=ON_Z0_MAX
            and
            0.0
            <omega_final
            <1.0
        )

        domain_pass = bool(
            omega_spread
            <=DOMAIN_OMEGA_REL_TOL
            and
            u0_spread
            <=DOMAIN_U0_REL_TOL
        )

        positive_energy_pass = bool(
            math.isfinite(
                total_inventory_j
            )
            and
            total_inventory_j
            >0.0
            and
            gate_total_j
            >=0.0
        )

        print(
            f"OFF_SOURCE_PASS="
            f"{off_source_pass}"
        )

        print(
            f"OFF_SCALAR_LAMBDA0_WITH_GATE="
            f"{off_lambda0:+.15e}"
        )

        print(
            f"OFF_SCALAR_STABLE="
            f"{off_scalar_pass}"
        )

        print(
            f"OFF_EXACT_FIXEDQ_BRANCH_PASS="
            f"{off_pass}"
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
            f"{fixed_q_pass}"
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
            f"{positive_energy_pass}"
        )

        green = bool(
            fixed_q_pass
            and
            on_branch_pass
            and
            domain_pass
            and
            positive_energy_pass
            and
            payload_pass
            and
            off_pass
        )

        if green:
            classification = (
                "GREEN_D2CR_FULL_FIXEDQ_LOGGATE_"
                "MICROSCOPIC_ON_OFF_EXISTENCE"
            )

            next_action = (
                "031D2D_COUPLED_Y_U_GATE_STABILITY_"
                "SWITCHING_BARRIER_RESET_AND_RADIATION"
            )

        else:
            classification = (
                "YELLOW_D2CR_TARGET_BRANCH_REACHED_"
                "BUT_CERTIFICATION_SUBGATE_FAILED"
            )

            next_action = (
                "REFINE_ONLY_FAILED_D2CR_SUBGATE"
            )

        print(
            f"031D2CR_CLASSIFICATION="
            f"{classification}"
        )

        print(
            f"NEXT={next_action}"
        )

        print(
            "COUPLED_Y_U_GATE_LINEAR_STABILITY_CLOSED=NO"
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
            "FULL_METRIC_BACKREACTION_CLOSED=NO"
        )

        print(
            "EFT_NATURALNESS_CLOSED=NO"
        )

        print(
            "EMPIRICAL_CLOSURE=NO"
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

                "u_transition":
                    u_transition,
            },

            "spectator_gate": {
                "q0":
                    q0_spectator,

                "z0":
                    z0_spectator,

                "nodes":
                    int(
                        spectator.x.size
                    ),
            },

            "homotopy_rows":
                homotopy_rows,

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
                    /operating_energy_j,
            },

            "payload": {
                "gradient_ratios":
                    payload_ratios,

                "pass":
                    payload_pass,
            },

            "off_state": {
                "scalar_lambda0_with_gate":
                    off_lambda0,

                "pass":
                    off_pass,
            },

            "claim_limits": [
                (
                    "q=log(s/v_s) is an exact field reparameterization."
                ),
                (
                    "Intermediate homotopy t values are numerical "
                    "continuation devices and are not physical theories."
                ),
                (
                    "Only the final t=1 solution represents the "
                    "reciprocal target Lagrangian."
                ),
                (
                    "The microscopic Q-ball source reacts "
                    "self-consistently at t=1."
                ),
                (
                    "Positive canonical gate energy and interaction "
                    "energy are included."
                ),
                (
                    "Coupled perturbative gate stability remains open."
                ),
                (
                    "Switching, reset, radiation, full metric "
                    "backreaction, EFT/naturalness and empirical "
                    "closure remain open."
                ),
                (
                    "No practical device is established."
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
            +"\n"
        )

        homotopy_fields = sorted(
            {
                key
                for row
                in homotopy_rows
                for key
                in row.keys()
            }
        )

        with OUT_HOMOTOPY.open(
            "w",
            newline="",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=homotopy_fields,
            )

            writer.writeheader()
            writer.writerows(
                homotopy_rows
            )

        domain_fields = sorted(
            {
                key
                for row
                in domain_rows
                for key
                in row.keys()
            }
        )

        with OUT_DOMAIN.open(
            "w",
            newline="",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=domain_fields,
            )

            writer.writeheader()
            writer.writerows(
                domain_rows
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}"
        )

        print(
            f"HOMOTOPY_CSV={OUT_HOMOTOPY}"
        )

        print(
            f"DOMAIN_CSV={OUT_DOMAIN}"
        )

    finally:
        qmod.X_MATCH = old_x_match


if __name__ == "__main__":
    main()
