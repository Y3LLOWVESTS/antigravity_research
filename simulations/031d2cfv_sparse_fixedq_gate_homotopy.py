"""
031D2C-FV
=========

Sparse finite-volume / finite-difference fixed-Q realization gate for
the canonical reciprocal mediator-mass gate.

Why this run exists
-------------------
Previous collocation formulations failed numerically.

031D2C-V then used constrained energy minimization, but all declared
seeds exhausted the optimizer iteration budget with very large raw
discrete gradients. They remained ON-like rather than collapsing OFF.

Therefore the D2C-V printed RED classification is not a physics result.

This run solves the stationary Euler-Lagrange equations directly using:

    scipy.optimize.least_squares
    sparse Jacobian structure
    trust-region reflective method
    radial finite-volume Laplacian
    explicit fixed-Noether-charge equation
    continuation in gate backreaction t

This is independent of solve_bvp and independent of the previous
energy-gradient stopping metric.

Physical theory at t=1
----------------------
A(u) = exp(-u^2/2)
W(y) = 1/2 log(1+y^2)

lap y =
    A(u) y/(1+y^2)
    - Omega^2 y

lap u =
    (epsilon^2 + delta2 z^2) u
    - chi^2 A(u) W(y) u

lap z =
    [a2(z^2-1) + b2 u^2] z

Q =
    4 pi Omega integral r^2 y^2 dr
    = Q_target.

Intermediate t only multiplies the reciprocal gate contribution in
the u equation:

    delta2 z^2 -> t delta2 z^2.

Only t=1 is physical.

Promotion
---------
GREEN requires:
- continuation reaches t=1;
- locally normalized residuals converge;
- fixed Q converges;
- ON branch remains nontrivial;
- domain/grid reconstruction agrees;
- positive gate energy is finite;
- payload scalar-gradient sign/magnitude survives;
- exact OFF branch remains linearly stabilized.

A failure is not automatically proof of nonexistence, but reproducible
failure of this method plus the previous independent methods would
strongly demote the tested canonical gate.

No practical device claim.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

from scipy.optimize import least_squares
from scipy.sparse import lil_matrix


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

QBALL_SOURCE = (
    SIM / "031b2a_global_qball_activated_scalar_control.py"
)

ROBUST_SUMMARY = (
    DATA / "031c96_operating_margin_robustness_summary.json"
)

LOW_SUMMARY = (
    DATA / "031d1r2_lowbranch_offstate_hessian_summary.json"
)

D1HR_SUMMARY = (
    DATA / "031d1hr_highbranch_certificate_summary.json"
)

OUT_JSON = (
    DATA / "031d2cfv_sparse_fixedq_summary.json"
)

OUT_HOMOTOPY = (
    DATA / "031d2cfv_homotopy_scan.csv"
)

OUT_DOMAIN = (
    DATA / "031d2cfv_domain_scan.csv"
)


# ----------------------------------------------------------------------
# Theory / candidate
# ----------------------------------------------------------------------

X_MATCH = 80.0

G_S = 3.0e-16
M_S_EV = 2.0719332942e-7

STABILIZATION_MARGIN = 1.20

# Coarse existence grid followed by independent domain/grid checks.
GRID_SPECS = (
    (300.0, 0.75),
    (400.0, 0.60),
    (500.0, 0.50),
)

INITIAL_T_STEP = 0.10
MIN_T_STEP = 0.0125

MAX_NFEV = 1000

RESIDUAL_RMS_MAX = 3.0e-5
RESIDUAL_MAX_MAX = 5.0e-4

Q_REL_MAX = 2.0e-6

ON_U0_MIN = 0.20
ON_Z0_MAX = 5.0e-2

PAYLOAD_GRADIENT_RATIO_MIN = 0.85

DOMAIN_OMEGA_REL_MAX = 2.0e-3
DOMAIN_U0_REL_MAX = 2.0e-2

HBARC_EV_M = 1.973269804e-7
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


def relerr(a: float, b: float) -> float:
    return abs(a - b) / max(
        abs(a),
        abs(b),
        1.0e-300,
    )


def builtin(value):
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


def make_grid(rmax: float, h_target: float):
    n = int(
        math.ceil(
            rmax / h_target
        )
    )

    h = rmax / n

    r = np.linspace(
        0.0,
        rmax,
        n + 1,
    )

    return r, h


def radial_laplacian(
    field: np.ndarray,
    r: np.ndarray,
    h: float,
):
    n = len(r) - 1

    lap = np.empty_like(
        field
    )

    # Regular spherical origin:
    #
    # f(r)=f0 + a r^2 + ...
    # lap f(0)=6a ~= 6(f1-f0)/h^2
    lap[0] = (
        6.0
        * (
            field[1]
            - field[0]
        )
        / h**2
    )

    ri = r[
        1:n
    ]

    rp = (
        ri
        + 0.5 * h
    )

    rm = (
        ri
        - 0.5 * h
    )

    lap[
        1:n
    ] = (
        rp**2
        * (
            field[
                2:n + 1
            ]
            - field[
                1:n
            ]
        )
        -
        rm**2
        * (
            field[
                1:n
            ]
            - field[
                0:n - 1
            ]
        )
    ) / (
        ri**2
        * h**2
    )

    lap[n] = math.nan

    return lap


def charge_integral(
    y: np.ndarray,
    omega: float,
    r: np.ndarray,
):
    return float(
        4.0
        * math.pi
        * omega
        * np.trapezoid(
            r**2
            * y**2,
            r,
        )
    )


def unpack(
    values: np.ndarray,
    n_nodes: int,
):
    y = values[
        0:n_nodes
    ]

    u = values[
        n_nodes:
        2 * n_nodes
    ]

    z = values[
        2 * n_nodes:
        3 * n_nodes
    ]

    omega = float(
        values[-1]
    )

    return (
        y,
        u,
        z,
        omega,
    )


def pack(
    y,
    u,
    z,
    omega,
):
    return np.concatenate(
        (
            y,
            u,
            z,
            np.array(
                [omega]
            ),
        )
    )


def jacobian_sparsity(
    n_nodes: int,
):
    total = (
        3 * n_nodes
        + 1
    )

    J = lil_matrix(
        (
            total,
            total,
        ),
        dtype=int,
    )

    # Residual blocks:
    #
    # y rows      0 .. N-1
    # u rows      N .. 2N-1
    # z rows      2N .. 3N-1
    # charge row  3N
    #
    # Each PDE row depends on nearest neighbors in its own field,
    # local cross-fields and Omega where appropriate.

    for i in range(
        n_nodes
    ):
        # y equation / BC
        row = i

        for j in (
            i - 1,
            i,
            i + 1,
        ):
            if 0 <= j < n_nodes:
                J[
                    row,
                    j,
                ] = 1

        J[
            row,
            n_nodes + i,
        ] = 1

        J[
            row,
            total - 1,
        ] = 1

        # u equation / BC
        row = (
            n_nodes
            + i
        )

        for j in (
            i - 1,
            i,
            i + 1,
        ):
            if 0 <= j < n_nodes:
                J[
                    row,
                    n_nodes + j,
                ] = 1

        J[
            row,
            i,
        ] = 1

        J[
            row,
            2 * n_nodes + i,
        ] = 1

        # z equation / BC
        row = (
            2 * n_nodes
            + i
        )

        for j in (
            i - 1,
            i,
            i + 1,
        ):
            if 0 <= j < n_nodes:
                J[
                    row,
                    2 * n_nodes + j,
                ] = 1

        J[
            row,
            n_nodes + i,
        ] = 1

    # Charge equation depends on all y nodes and Omega.
    qrow = (
        3 * n_nodes
    )

    for j in range(
        n_nodes
    ):
        J[
            qrow,
            j,
        ] = 1

    J[
        qrow,
        total - 1,
    ] = 1

    return J.tocsr()


def main() -> None:
    print(
        "=== 031D2C-FV SPARSE FIXED-Q GATE HOMOTOPY ==="
    )

    print(
        "SOLVE_BVP_USED=NO"
    )

    print(
        "ENERGY_MINIMIZER_USED=NO"
    )

    print(
        "FINITE_VOLUME_RADIAL_RESIDUAL=YES"
    )

    print(
        "SPARSE_TRUST_REGION_LEAST_SQUARES=YES"
    )

    print(
        "FIXED_NOETHER_CHARGE=YES"
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
            "031D1 gate-free closure missing"
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

    omega0 = float(
        candidate[
            "omega"
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

    F_ev = (
        F_gev
        * 1.0e9
    )

    M_c_gev = (
        F_gev
        / chi
    )

    M_c_ev = (
        M_c_gev
        * 1.0e9
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

    rho_gate = (
        v_s_ev
        / F_ev
    )**2

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

    print(
        f"TARGET_I_Q={target_q:.15e}"
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
        f"RHO_GATE={rho_gate:.15e}"
    )

    print(
        f"OFF_SCALAR_LAMBDA0_WITH_GATE="
        f"{off_lambda0:+.15e}"
    )

    qmod = load_module(
        "qball031d2cfv",
        QBALL_SOURCE,
    )

    old_xmatch = float(
        qmod.X_MATCH
    )

    qmod.X_MATCH = X_MATCH

    try:
        print(
            "\n=== STAGE A: BASELINE ON STATE ==="
        )

        seed = qmod.solve_uncoupled_qball(
            omega0
        )

        if seed is None:
            raise RuntimeError(
                "Failed baseline Q-ball"
            )

        baseline = qmod.solve_coupled(
            seed,
            omega0,
            epsilon,
            chi,
            previous=None,
        )

        if baseline is None:
            raise RuntimeError(
                "Failed baseline scalarized source"
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

        ky0 = math.sqrt(
            1.0
            - omega0**2
        )

        def baseline_arrays(
            r,
        ):
            y = np.zeros_like(
                r
            )

            u = np.zeros_like(
                r
            )

            inside = (
                r <= X_MATCH
            )

            rs = np.maximum(
                r[
                    inside
                ],
                1.0e-5,
            )

            state = baseline.sol(
                rs
            )

            y[
                inside
            ] = state[
                0
            ]

            u[
                inside
            ] = state[
                2
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

                y[
                    outside
                ] = (
                    y80
                    * X_MATCH
                    / ro
                    * np.exp(
                        -ky0
                        * (
                            ro
                            - X_MATCH
                        )
                    )
                )

                u[
                    outside
                ] = (
                    u80
                    * X_MATCH
                    / ro
                    * np.exp(
                        -epsilon
                        * (
                            ro
                            - X_MATCH
                        )
                    )
                )

            u_transition = math.sqrt(
                a2 / b2
            )

            z_alg = np.sqrt(
                np.clip(
                    1.0
                    - (
                        b2
                        * u**2
                        / a2
                    ),
                    0.0,
                    1.0,
                )
            )

            # Smooth the algebraic transition modestly.
            z = np.array(
                z_alg,
                copy=True,
            )

            for _ in range(
                8
            ):
                z[
                    1:-1
                ] = (
                    0.25
                    * z[
                        :-2
                    ]
                    + 0.50
                    * z[
                        1:-1
                    ]
                    + 0.25
                    * z[
                        2:
                    ]
                )

            z = np.clip(
                z,
                0.0,
                1.0,
            )

            z[-1] = 1.0

            return (
                y,
                u,
                z,
                u_transition,
            )

        # ----------------------------------------------------------
        # Residual factory
        # ----------------------------------------------------------

        def residual_function(
            values,
            r,
            h,
            t_value,
        ):
            n_nodes = len(
                r
            )

            y, u, z, omega = unpack(
                values,
                n_nodes,
            )

            lap_y = radial_laplacian(
                y,
                r,
                h,
            )

            lap_u = radial_laplacian(
                u,
                r,
                h,
            )

            lap_z = radial_laplacian(
                z,
                r,
                h,
            )

            A = np.exp(
                -0.5
                * u**2
            )

            W = (
                0.5
                * np.log1p(
                    y**2
                )
            )

            n = (
                n_nodes
                - 1
            )

            ry = np.empty(
                n_nodes
            )

            ru = np.empty(
                n_nodes
            )

            rz = np.empty(
                n_nodes
            )

            # Local EOM scales keep residuals dimensionless and
            # independent of radial volume weighting.
            y_scale = (
                0.05
                + np.abs(
                    A
                    * y
                    / (
                        1.0
                        + y**2
                    )
                )
                + omega**2
                * np.abs(
                    y
                )
            )

            u_scale = (
                1.0e-3
                + (
                    epsilon**2
                    + t_value
                    * delta2
                    * z**2
                )
                * np.abs(
                    u
                )
                + chi**2
                * A
                * W
                * np.abs(
                    u
                )
            )

            z_scale = (
                1.0e-5
                + (
                    a2
                    * (
                        1.0
                        + z**2
                    )
                    + b2
                    * u**2
                )
                * np.maximum(
                    np.abs(
                        z
                    ),
                    1.0e-3,
                )
            )

            ry[
                :n
            ] = (
                lap_y[
                    :n
                ]
                - A[
                    :n
                ]
                * y[
                    :n
                ]
                / (
                    1.0
                    + y[
                        :n
                    ]**2
                )
                + omega**2
                * y[
                    :n
                ]
            ) / y_scale[
                :n
            ]

            ru[
                :n
            ] = (
                lap_u[
                    :n
                ]
                - (
                    epsilon**2
                    + t_value
                    * delta2
                    * z[
                        :n
                    ]**2
                )
                * u[
                    :n
                ]
                + chi**2
                * A[
                    :n
                ]
                * W[
                    :n
                ]
                * u[
                    :n
                ]
            ) / u_scale[
                :n
            ]

            rz[
                :n
            ] = (
                lap_z[
                    :n
                ]
                - (
                    a2
                    * (
                        z[
                            :n
                        ]**2
                        - 1.0
                    )
                    + b2
                    * u[
                        :n
                    ]**2
                )
                * z[
                    :n
                ]
            ) / z_scale[
                :n
            ]

            # Outer Robin conditions.
            ky = math.sqrt(
                max(
                    1.0
                    - omega**2,
                    1.0e-10,
                )
            )

            eps_outer = math.sqrt(
                epsilon**2
                + t_value
                * delta2
            )

            yp_outer = (
                y[-1]
                - y[-2]
            ) / h

            up_outer = (
                u[-1]
                - u[-2]
            ) / h

            zp_outer = (
                z[-1]
                - z[-2]
            ) / h

            ry[-1] = (
                yp_outer
                + (
                    ky
                    + 1.0
                    / r[-1]
                )
                * y[-1]
            ) / max(
                abs(
                    y[-2]
                )
                / h,
                1.0e-6,
            )

            ru[-1] = (
                up_outer
                + (
                    eps_outer
                    + 1.0
                    / r[-1]
                )
                * u[-1]
            ) / max(
                abs(
                    u[-2]
                )
                / h,
                1.0e-7,
            )

            rz[-1] = (
                zp_outer
                - (
                    gate_k
                    + 1.0
                    / r[-1]
                )
                * (
                    1.0
                    - z[-1]
                )
            ) / max(
                (
                    abs(
                        1.0
                        - z[-2]
                    )
                    / h
                ),
                1.0e-6,
            )

            q_value = charge_integral(
                y,
                omega,
                r,
            )

            rq = (
                q_value
                - target_q
            ) / target_q

            return np.concatenate(
                (
                    ry,
                    ru,
                    rz,
                    np.array(
                        [
                            10.0
                            * rq
                        ]
                    ),
                )
            )

        def solve_grid(
            r,
            h,
            initial_values,
            t_value,
        ):
            n_nodes = len(
                r
            )

            lower = np.concatenate(
                (
                    np.zeros(
                        n_nodes
                    ),
                    np.zeros(
                        n_nodes
                    ),
                    np.zeros(
                        n_nodes
                    ),
                    np.array(
                        [
                            0.15
                        ]
                    ),
                )
            )

            upper = np.concatenate(
                (
                    np.full(
                        n_nodes,
                        20.0,
                    ),
                    np.full(
                        n_nodes,
                        5.0,
                    ),
                    np.full(
                        n_nodes,
                        1.20,
                    ),
                    np.array(
                        [
                            0.95
                        ]
                    ),
                )
            )

            sparsity = jacobian_sparsity(
                n_nodes
            )

            return least_squares(
                residual_function,
                initial_values,
                bounds=(
                    lower,
                    upper,
                ),
                args=(
                    r,
                    h,
                    t_value,
                ),
                method="trf",
                jac="2-point",
                jac_sparsity=sparsity,
                x_scale="jac",
                loss="linear",
                ftol=1.0e-10,
                xtol=1.0e-10,
                gtol=1.0e-9,
                max_nfev=MAX_NFEV,
                tr_solver="lsmr",
                verbose=0,
            )

        # ----------------------------------------------------------
        # STAGE B: t homotopy on first grid
        # ----------------------------------------------------------

        print(
            "\n=== STAGE B: FIXED-Q FINITE-VOLUME HOMOTOPY ==="
        )

        r0, h0 = make_grid(
            *GRID_SPECS[
                0
            ]
        )

        y0, u0, z0, u_transition = baseline_arrays(
            r0
        )

        current_values = pack(
            y0,
            u0,
            z0,
            omega0,
        )

        # First solve t=0 so the spectator gate itself is stationary.
        current = solve_grid(
            r0,
            h0,
            current_values,
            0.0,
        )

        if not current.success:
            raise RuntimeError(
                "Finite-volume t=0 solve failed: "
                f"{current.message}"
            )

        current_values = current.x

        homotopy_rows = []

        t_current = 0.0
        t_step = INITIAL_T_STEP

        while (
            t_current
            < 1.0
            - 1.0e-12
        ):
            t_trial = min(
                1.0,
                t_current
                + t_step,
            )

            trial = solve_grid(
                r0,
                h0,
                current_values,
                t_trial,
            )

            trial_residual = residual_function(
                trial.x,
                r0,
                h0,
                t_trial,
            )

            rms = float(
                math.sqrt(
                    np.mean(
                        trial_residual**2
                    )
                )
            )

            rmax_abs = float(
                np.max(
                    np.abs(
                        trial_residual
                    )
                )
            )

            if (
                not trial.success
                or
                rms
                > 5.0e-4
            ):
                t_step *= 0.5

                print(
                    f"HOMOTOPY_RETRY "
                    f"T_CURRENT={t_current:.6f} "
                    f"T_TRIAL={t_trial:.6f} "
                    f"STEP={t_step:.6f} "
                    f"SUCCESS={trial.success} "
                    f"RMS={rms:.6e}"
                )

                if (
                    t_step
                    < MIN_T_STEP
                ):
                    raise RuntimeError(
                        "Finite-volume homotopy could not "
                        "continue toward t=1"
                    )

                continue

            current = trial
            current_values = trial.x
            t_current = t_trial

            y, u, z, omega = unpack(
                current_values,
                len(
                    r0
                ),
            )

            q_rel = relerr(
                charge_integral(
                    y,
                    omega,
                    r0,
                ),
                target_q,
            )

            row = {
                "t":
                    t_current,

                "omega":
                    omega,

                "u0":
                    float(
                        u[0]
                    ),

                "z0":
                    float(
                        z[0]
                    ),

                "zmax":
                    float(
                        np.max(
                            z
                        )
                    ),

                "Q_relerr":
                    q_rel,

                "rms_residual":
                    rms,

                "max_residual":
                    rmax_abs,

                "nfev":
                    int(
                        trial.nfev
                    ),

                "cost":
                    float(
                        trial.cost
                    ),
            }

            homotopy_rows.append(
                row
            )

            print(
                f"HOMOTOPY "
                f"T={t_current:.6f} "
                f"OMEGA={omega:.12e} "
                f"U0={u[0]:.12e} "
                f"Z0={z[0]:.12e} "
                f"Q_REL={q_rel:.6e} "
                f"RMS={rms:.6e} "
                f"MAXR={rmax_abs:.6e} "
                f"NFEV={trial.nfev}"
            )

            t_step = min(
                INITIAL_T_STEP,
                1.35
                * t_step,
            )

        if abs(
            t_current
            - 1.0
        ) > 1.0e-12:
            raise RuntimeError(
                "Did not reach t=1"
            )

        print(
            "\n=== STAGE C: DOMAIN / GRID RECONSTRUCTION ==="
        )

        domain_rows = []

        previous_r = r0
        previous_values = current_values

        for (
            rmax,
            h_target,
        ) in GRID_SPECS:
            r, h = make_grid(
                rmax,
                h_target,
            )

            if (
                len(r) == len(previous_r)
                and
                np.allclose(
                    r,
                    previous_r,
                )
            ):
                guess = previous_values

            else:
                py, pu, pz, pomega = unpack(
                    previous_values,
                    len(
                        previous_r
                    ),
                )

                y_guess = np.interp(
                    r,
                    previous_r,
                    py,
                    left=py[0],
                    right=0.0,
                )

                u_guess = np.interp(
                    r,
                    previous_r,
                    pu,
                    left=pu[0],
                    right=0.0,
                )

                z_guess = np.interp(
                    r,
                    previous_r,
                    pz,
                    left=pz[0],
                    right=1.0,
                )

                guess = pack(
                    y_guess,
                    u_guess,
                    z_guess,
                    pomega,
                )

            solved = solve_grid(
                r,
                h,
                guess,
                1.0,
            )

            residual = residual_function(
                solved.x,
                r,
                h,
                1.0,
            )

            rms = float(
                math.sqrt(
                    np.mean(
                        residual**2
                    )
                )
            )

            max_residual = float(
                np.max(
                    np.abs(
                        residual
                    )
                )
            )

            y, u, z, omega = unpack(
                solved.x,
                len(r),
            )

            q_rel = relerr(
                charge_integral(
                    y,
                    omega,
                    r,
                ),
                target_q,
            )

            # z=0.5 transition.
            zmono = np.maximum.accumulate(
                np.clip(
                    z,
                    0.0,
                    1.0,
                )
            )

            transition_x = float(
                np.interp(
                    0.5,
                    zmono,
                    r,
                )
            )

            row = {
                "rmax":
                    rmax,

                "h":
                    h,

                "omega":
                    omega,

                "u0":
                    float(
                        u[0]
                    ),

                "z0":
                    float(
                        z[0]
                    ),

                "transition_x":
                    transition_x,

                "Q_relerr":
                    q_rel,

                "rms_residual":
                    rms,

                "max_residual":
                    max_residual,

                "nfev":
                    int(
                        solved.nfev
                    ),

                "success":
                    bool(
                        solved.success
                    ),
            }

            domain_rows.append(
                row
            )

            print(
                f"DOMAIN "
                f"RMAX={rmax:.1f} "
                f"H={h:.6f} "
                f"OMEGA={omega:.12e} "
                f"U0={u[0]:.12e} "
                f"Z0={z[0]:.12e} "
                f"Z50={transition_x:.6f} "
                f"Q_REL={q_rel:.6e} "
                f"RMS={rms:.6e} "
                f"MAXR={max_residual:.6e}"
            )

            previous_r = r
            previous_values = solved.x

        final_r = previous_r
        final_values = previous_values

        fy, fu, fz, fomega = unpack(
            final_values,
            len(
                final_r
            ),
        )

        final_h = (
            final_r[-1]
            / (
                len(
                    final_r
                )
                - 1
            )
        )

        final_residual = residual_function(
            final_values,
            final_r,
            final_h,
            1.0,
        )

        final_rms = float(
            math.sqrt(
                np.mean(
                    final_residual**2
                )
            )
        )

        final_max = float(
            np.max(
                np.abs(
                    final_residual
                )
            )
        )

        final_q_rel = relerr(
            charge_integral(
                fy,
                fomega,
                final_r,
            ),
            target_q,
        )

        # ----------------------------------------------------------
        # STAGE D: positive energy ledger
        # ----------------------------------------------------------

        print(
            "\n=== STAGE D: POSITIVE ENERGY LEDGER ==="
        )

        r = final_r
        h = final_h

        dy = np.gradient(
            fy,
            h,
        )

        du = np.gradient(
            fu,
            h,
        )

        dz = np.gradient(
            fz,
            h,
        )

        W = (
            0.5
            * np.log1p(
                fy**2
            )
        )

        A = np.exp(
            -0.5
            * fu**2
        )

        source_inventory_density = (
            0.5
            * dy**2
            + 0.5
            * fomega**2
            * fy**2
            + W
        )

        scalar_density = (
            (
                0.5
                * du**2
                + 0.5
                * epsilon**2
                * fu**2
            )
            / chi**2
        )

        gate_density_dimensionless = (
            rho_gate
            * (
                0.5
                * dz**2
                + a2
                / 4.0
                * (
                    fz**2
                    - 1.0
                )**2
                + 0.5
                * b2
                * fu**2
                * fz**2
            )
        )

        I_source_scalar = float(
            4.0
            * math.pi
            * np.trapezoid(
                r**2
                * (
                    source_inventory_density
                    + scalar_density
                ),
                r,
            )
        )

        I_gate = float(
            4.0
            * math.pi
            * np.trapezoid(
                r**2
                * gate_density_dimensionless,
                r,
            )
        )

        energy_scale_j = (
            F_gev**2
            / m_x_gev
            * J_PER_GEV
        )

        source_scalar_j = (
            I_source_scalar
            * energy_scale_j
        )

        gate_j = (
            I_gate
            * energy_scale_j
        )

        total_j = (
            source_scalar_j
            + gate_j
        )

        print(
            f"SOURCE_SCALAR_INVENTORY_GJ="
            f"{source_scalar_j/1.0e9:.12f}"
        )

        print(
            f"GATE_POSITIVE_ENERGY_GJ="
            f"{gate_j/1.0e9:.12f}"
        )

        print(
            f"TOTAL_GATED_INVENTORY_GJ="
            f"{total_j/1.0e9:.12f}"
        )

        # ----------------------------------------------------------
        # STAGE E: payload response
        # ----------------------------------------------------------

        print(
            "\n=== STAGE E: PAYLOAD RESPONSE ==="
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

        center_from_source = abs(
            payload_center_m
            - source_shift_m
        )

        x_length_m = (
            HBARC_EV_M
            / m_x_ev
        )

        payload_radii = (
            (
                "near",
                center_from_source
                - payload_radius_m,
            ),
            (
                "center",
                center_from_source,
            ),
            (
                "far",
                center_from_source
                + payload_radius_m,
            ),
        )

        final_up = np.gradient(
            fu,
            final_h,
        )

        payload_ratios = []
        payload_signs = []

        for label, radius_m in payload_radii:
            xp = (
                radius_m
                / x_length_m
            )

            gated_up = float(
                np.interp(
                    xp,
                    final_r,
                    final_up,
                )
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

            payload_signs.append(
                same_sign
            )

            print(
                f"PAYLOAD_{label.upper()} "
                f"R_M={radius_m:.9f} "
                f"BASE_UP={baseline_up:+.12e} "
                f"GATED_UP={gated_up:+.12e} "
                f"ABS_RATIO={ratio:.12e} "
                f"SAME_SIGN={same_sign}"
            )

        payload_pass = bool(
            min(
                payload_ratios
            )
            >= PAYLOAD_GRADIENT_RATIO_MIN
            and all(
                payload_signs
            )
        )

        # ----------------------------------------------------------
        # Final decision
        # ----------------------------------------------------------

        omega_values = np.array(
            [
                row[
                    "omega"
                ]
                for row in domain_rows
            ]
        )

        u0_values = np.array(
            [
                row[
                    "u0"
                ]
                for row in domain_rows
            ]
        )

        omega_spread = (
            np.max(
                omega_values
            )
            - np.min(
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
            - np.min(
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

        domain_pass = bool(
            omega_spread
            <= DOMAIN_OMEGA_REL_MAX
            and
            u0_spread
            <= DOMAIN_U0_REL_MAX
        )

        residual_pass = bool(
            final_rms
            <= RESIDUAL_RMS_MAX
            and
            final_max
            <= RESIDUAL_MAX_MAX
        )

        q_pass = bool(
            final_q_rel
            <= Q_REL_MAX
        )

        on_pass = bool(
            fu[0]
            >= ON_U0_MIN
            and
            fz[0]
            <= ON_Z0_MAX
            and
            0.0
            < fomega
            < 1.0
        )

        off_pass = bool(
            low[
                "source_slope_stable"
            ]
            and
            low[
                "qball_bound_pass"
            ]
            and
            off_lambda0
            > 0.0
            and
            2.0 * a2
            > 0.0
        )

        positive_energy_pass = bool(
            math.isfinite(
                total_j
            )
            and
            total_j
            > 0.0
            and
            gate_j
            >= 0.0
        )

        print(
            "\n=== STAGE F: DECISION ==="
        )

        print(
            f"FINAL_RMS_RESIDUAL="
            f"{final_rms:.15e}"
        )

        print(
            f"FINAL_MAX_RESIDUAL="
            f"{final_max:.15e}"
        )

        print(
            f"FINAL_Q_RELERR="
            f"{final_q_rel:.15e}"
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
            f"FINITE_VOLUME_RESIDUAL_PASS="
            f"{residual_pass}"
        )

        print(
            f"FIXED_Q_PASS="
            f"{q_pass}"
        )

        print(
            f"ON_BRANCH_PASS="
            f"{on_pass}"
        )

        print(
            f"DOMAIN_RECONSTRUCTION_PASS="
            f"{domain_pass}"
        )

        print(
            f"PAYLOAD_GRADIENT_PRESERVED="
            f"{payload_pass}"
        )

        print(
            f"OFF_EXACT_FIXEDQ_BRANCH_PASS="
            f"{off_pass}"
        )

        print(
            f"POSITIVE_FINITE_ENERGY_PASS="
            f"{positive_energy_pass}"
        )

        green = bool(
            residual_pass
            and
            q_pass
            and
            on_pass
            and
            domain_pass
            and
            payload_pass
            and
            off_pass
            and
            positive_energy_pass
        )

        if green:
            classification = (
                "GREEN_D2CFV_FIXEDQ_RECIPROCAL_"
                "MICROSCOPIC_ON_OFF_EXISTENCE"
            )

            next_action = (
                "031D2D_COUPLED_GATE_STABILITY_"
                "SWITCHING_RESET_AND_RADIATION"
            )

        else:
            classification = (
                "YELLOW_D2CFV_CANONICAL_GATE_"
                "NOT_CERTIFIED_BY_INDEPENDENT_RESIDUAL_SOLVE"
            )

            next_action = (
                "RERANK_031D_AND_COMPARE_D3_"
                "AUXILIARY_METRIC_ACTIVATION"
            )

        print(
            f"031D2CFV_CLASSIFICATION="
            f"{classification}"
        )

        print(
            f"NEXT={next_action}"
        )

        print(
            "CANONICAL_D2_S2PHI2_GATE_CLOSED="
            f"{False if green else 'STRONGLY_DEMOTED_NOT_FORMALLY_PROVEN_IMPOSSIBLE'}"
        )

        print(
            "SWITCHING_RESET_CLOSED=NO"
        )

        print(
            "FULL_METRIC_BACKREACTION_CLOSED=NO"
        )

        print(
            "EFT_NATURALNESS_CLOSED=NO"
        )

        print(
            "PRACTICAL_DEVICE=NO"
        )

        summary = {
            "classification":
                classification,

            "next":
                next_action,

            "scientific_correction": (
                "031D2C-V printed RED is not promoted because all "
                "three optimizers failed to converge and remained "
                "ON-like."
            ),

            "gate": {
                "g_s":
                    G_S,

                "v_s_eV":
                    v_s_ev,

                "lambda_s":
                    lambda_s,

                "a2":
                    a2,

                "b2":
                    b2,

                "delta2":
                    delta2,

                "rho_gate":
                    rho_gate,
            },

            "homotopy_rows":
                homotopy_rows,

            "domain_rows":
                domain_rows,

            "final": {
                "omega":
                    fomega,

                "u0":
                    float(
                        fu[0]
                    ),

                "z0":
                    float(
                        fz[0]
                    ),

                "Q_relerr":
                    final_q_rel,

                "rms_residual":
                    final_rms,

                "max_residual":
                    final_max,

                "source_scalar_inventory_J":
                    source_scalar_j,

                "gate_positive_energy_J":
                    gate_j,

                "total_inventory_J":
                    total_j,

                "payload_gradient_ratios":
                    payload_ratios,
            },

            "claim_limits": [
                (
                    "Failure of a numerical solver is not a theorem "
                    "of nonexistence."
                ),
                (
                    "GREEN would establish static fixed-Q existence "
                    "only, not coupled spectral stability."
                ),
                (
                    "Switching/reset/radiation remain open."
                ),
                (
                    "Full physical metric/Einstein backreaction "
                    "remains open."
                ),
                (
                    "EFT/naturalness and empirical closure remain open."
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
            + "\n"
        )

        homotopy_fields = sorted(
            {
                key
                for row in homotopy_rows
                for key in row
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
                for row in domain_rows
                for key in row
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
        qmod.X_MATCH = old_xmatch


if __name__ == "__main__":
    main()
