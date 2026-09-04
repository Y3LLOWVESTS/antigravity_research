"""
031D2B-R — numerically conditioned reciprocal gate-wall solve

Repairs the D2B solve_bvp failure.

D2B's physical coefficients were

    a2     = 6.0031125e-4
    b2     = 6.4113966e14
    delta2 = 1.501650749e-1

in

    u'' + 2u'/x
        = (epsilon^2 + delta2 z^2) u

    z'' + 2z'/x
        = [a2(z^2-1) + b2 u^2] z.

The huge b2 is a coordinate-conditioning problem.

Define

    u_t = sqrt(a2/b2)
    p   = u/u_t.

Then exactly

    p'' + 2p'/x
        = (epsilon^2 + delta2 z^2) p

    z'' + 2z'/x
        = a2 (z^2 - 1 + p^2) z.

No large coefficient remains.

This run:
- reconstructs the certified on-state scalar tail;
- independently reconstructs the D2B transition radius;
- solves p/z rather than u/z;
- uses asymptotic Robin conditions on both outer fields;
- includes positive gate potential, gradient and interaction energy;
- includes the change in the scalar tail energy;
- checks window/domain convergence;
- checks matching derivative feedback at the inner boundary.

It remains an EXTERIOR phi+s solve.
The microscopic Q-ball y field is not re-solved in this run.
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
from scipy.optimize import brentq


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

D2A_SUMMARY = (
    DATA
    / "031d2a_auxiliary_gate_capacity_summary.json"
)

OUT_JSON = (
    DATA
    / "031d2br_rescaled_gate_wall_summary.json"
)

OUT_CSV = (
    DATA
    / "031d2br_rescaled_gate_wall_convergence.csv"
)


HBARC_EV_M = 1.973269804e-7
J_PER_EV = 1.602176634e-19

X_MATCH = 80.0

# Frozen D2B corrected candidate.
G_S = 2.207692682950422e-9
V_S_EV = 1.049586849219965e3
LAMBDA_S = 1.948429882455258e-20
M_S_EV = 2.071933294200000e-7

EXPECTED_TRANSITION_M = 5.277272028575505e1

STABILIZATION_MARGIN = 1.20

HALF_WINDOWS_X = (
    220.0,
    280.0,
    340.0,
    400.0,
)

BVP_TOL = 2.0e-6
BVP_MAX_NODES = 45_000

WALL_RADIUS_REL_SPREAD_MAX = 0.01
WALL_ENERGY_REL_SPREAD_MAX = 0.03

INNER_DERIVATIVE_REL_MISMATCH_MAX = 0.01

OUTER_Z_DEVIATION_MAX = 5.0e-5

MAX_RMS_RESIDUAL = 2.0e-5

GATE_ENERGY_FRACTION_MAX = 0.01


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


def main() -> None:
    print(
        "=== 031D2B-R RESCALED DYNAMIC RECIPROCAL GATE WALL ==="
    )

    print(
        "OLD_B2_LARGE_COEFFICIENT_REMOVED_BY_EXACT_FIELD_RESCALE=YES"
    )

    print(
        "PRESCRIBED_GATE_RADIUS=NO"
    )

    print(
        "SPATIALLY_PRESCRIBED_MPHI=NO"
    )

    print(
        "POSITIVE_GATE_INTERACTION_ENERGY_INCLUDED=YES"
    )

    print(
        "FULL_Y_U_Z_SOURCE_BVP=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        QBALL_SOURCE,
        ROBUST_SUMMARY,
        LOW_SUMMARY,
        D1HR_SUMMARY,
        D2A_SUMMARY,
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

    d2a = json.loads(
        D2A_SUMMARY.read_text()
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

    if not str(
        d2a.get(
            "classification",
            "",
        )
    ).startswith(
        "GREEN_D2A"
    ):
        raise RuntimeError(
            "031D2A capacity gate is not GREEN"
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

    omega = float(
        candidate["omega"]
    )

    epsilon = float(
        candidate["epsilon"]
    )

    chi = float(
        candidate["chi"]
    )

    m_x_gev = float(
        candidate["m_x_gev_derived"]
    )

    m_x_ev = (
        m_x_gev
        * 1.0e9
    )

    F_gev = float(
        quadrature["F_gev"]
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
        operating["energy_J"]
    )

    critical_hat = float(
        low[
            "critical_positive_delta_m2_hat"
        ]
    )

    required_delta2 = (
        STABILIZATION_MARGIN
        * critical_hat
    )

    stabilized_lambda0 = (
        float(
            low["finest_lambda0"]
        )
        + required_delta2
    )

    a2 = (
        LAMBDA_S
        * V_S_EV**2
        / m_x_ev**2
    )

    b2 = (
        G_S**2
        * M_c_ev**2
        / m_x_ev**2
    )

    delta2 = (
        G_S
        * V_S_EV
        / m_x_ev
    )**2

    u_transition = math.sqrt(
        a2 / b2
    )

    epsilon_off = math.sqrt(
        epsilon**2
        + delta2
    )

    k_gate_out = math.sqrt(
        2.0 * a2
    )

    x_length_m = (
        HBARC_EV_M
        / m_x_ev
    )

    print(
        f"M_X_EV={m_x_ev:.15e}"
    )

    print(
        f"M_C_GEV={M_c_gev:.15e}"
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
        f"EPSILON_OFF={epsilon_off:.15e}"
    )

    print(
        f"OFF_HESSIAN_LAMBDA0="
        f"{stabilized_lambda0:+.15e}"
    )

    identity_error = relerr(
        b2 * u_transition**2,
        a2,
    )

    print(
        f"RESCALE_IDENTITY_RELERR="
        f"{identity_error:.15e}"
    )

    qmod = load_module(
        "qball031d2br",
        QBALL_SOURCE,
    )

    old_x_match = float(
        qmod.X_MATCH
    )

    qmod.X_MATCH = X_MATCH

    try:
        print(
            "\n=== STAGE A: RECONSTRUCT CERTIFIED ON-STATE TAIL ==="
        )

        seed = qmod.solve_uncoupled_qball(
            omega
        )

        if seed is None:
            raise RuntimeError(
                "Failed Q-ball seed reconstruction"
            )

        source = qmod.solve_coupled(
            seed,
            omega,
            epsilon,
            chi,
            previous=None,
        )

        if source is None:
            raise RuntimeError(
                "Failed coupled on-state reconstruction"
            )

        u80 = float(
            source.sol(
                X_MATCH
            )[2]
        )

        up80 = float(
            source.sol(
                X_MATCH
            )[3]
        )

        print(
            f"U_XMATCH={u80:.15e}"
        )

        print(
            f"UP_XMATCH={up80:.15e}"
        )

        def u_light(x):
            xx = np.asarray(
                x,
                dtype=float,
            )

            return (
                u80
                * X_MATCH
                / xx
                * np.exp(
                    -epsilon
                    * (
                        xx
                        - X_MATCH
                    )
                )
            )

        def up_light(x):
            value = u_light(
                x
            )

            return (
                -epsilon
                -1.0
                / np.asarray(
                    x,
                    dtype=float,
                )
            ) * value

        def transition_equation(x):
            return (
                float(
                    u_light(x)
                )
                - u_transition
            )

        x_hi = 200.0

        while (
            transition_equation(
                x_hi
            ) > 0.0
        ):
            x_hi *= 1.5

            if x_hi > 1.0e6:
                raise RuntimeError(
                    "Could not bracket transition"
                )

        x_transition = brentq(
            transition_equation,
            X_MATCH,
            x_hi,
            xtol=1.0e-11,
            rtol=1.0e-12,
        )

        r_transition_m = (
            x_transition
            * x_length_m
        )

        transition_relerr = relerr(
            r_transition_m,
            EXPECTED_TRANSITION_M,
        )

        print(
            f"X_TRANSITION={x_transition:.15e}"
        )

        print(
            f"R_TRANSITION_M={r_transition_m:.15e}"
        )

        print(
            f"R_TRANSITION_VS_D2B_RELERR="
            f"{transition_relerr:.15e}"
        )

        print(
            "\n=== STAGE B: CONDITIONED P/Z WALL SOLVES ==="
        )

        wall_rows = []

        for half_window in HALF_WINDOWS_X:
            x_left = (
                x_transition
                - half_window
            )

            x_right = (
                x_transition
                + half_window
            )

            if x_left <= X_MATCH:
                raise RuntimeError(
                    "Window entered source-matching region"
                )

            p_left = (
                float(
                    u_light(
                        x_left
                    )
                )
                / u_transition
            )

            if p_left <= 1.0:
                raise RuntimeError(
                    "Inner wall boundary is not in restored phase"
                )

            inner_z_mass = math.sqrt(
                max(
                    a2
                    * (
                        p_left**2
                        - 1.0
                    ),
                    1.0e-12,
                )
            )

            grid = np.linspace(
                x_left,
                x_right,
                1800,
            )

            # Light scalar on the inner side.
            p_inner = (
                u_light(grid)
                / u_transition
            )

            # Heavy scalar continuation on the outer side.
            p_outer = (
                x_transition
                / grid
                * np.exp(
                    -epsilon_off
                    * (
                        grid
                        - x_transition
                    )
                )
            )

            p_guess = np.where(
                grid <= x_transition,
                p_inner,
                p_outer,
            )

            p_guess = np.maximum(
                p_guess,
                1.0e-80,
            )

            pp_guess = np.gradient(
                p_guess,
                grid,
            )

            wall_scale_x = (
                1.0
                / max(
                    k_gate_out,
                    1.0e-12,
                )
            )

            argument = np.clip(
                (
                    grid
                    - x_transition
                )
                / wall_scale_x,
                -50.0,
                50.0,
            )

            z_guess = (
                0.5
                * (
                    1.0
                    + np.tanh(
                        argument
                    )
                )
            )

            zp_guess = np.gradient(
                z_guess,
                grid,
            )

            guess = np.vstack(
                (
                    p_guess,
                    pp_guess,
                    z_guess,
                    zp_guess,
                )
            )

            def equations(
                x,
                state,
            ):
                p = state[0]
                z = state[2]

                return np.vstack(
                    (
                        state[1],

                        (
                            epsilon**2
                            + delta2
                            * z**2
                        )
                        * p
                        -2.0
                        * state[1]
                        / x,

                        state[3],

                        a2
                        * (
                            z**2
                            -1.0
                            +p**2
                        )
                        * z
                        -2.0
                        * state[3]
                        / x,
                    )
                )

            def boundary(
                left,
                right,
            ):
                # p amplitude matched to inherited light scalar tail.
                bc_p_left = (
                    left[0]
                    - p_left
                )

                # z decays inward toward zero.
                bc_z_left = (
                    left[3]
                    - (
                        inner_z_mass
                        -1.0 / x_left
                    )
                    * left[2]
                )

                # p decays outward with the heavy off-state mass.
                bc_p_right = (
                    right[1]
                    + (
                        epsilon_off
                        +1.0 / x_right
                    )
                    * right[0]
                )

                # eta=1-z decays with gate vacuum mass.
                bc_z_right = (
                    right[3]
                    - (
                        k_gate_out
                        +1.0 / x_right
                    )
                    * (
                        1.0
                        -right[2]
                    )
                )

                return np.array(
                    (
                        bc_p_left,
                        bc_p_right,
                        bc_z_left,
                        bc_z_right,
                    ),
                    dtype=float,
                )

            result = solve_bvp(
                equations,
                boundary,
                grid,
                guess,
                tol=BVP_TOL,
                max_nodes=BVP_MAX_NODES,
                verbose=0,
            )

            if not result.success:
                raise RuntimeError(
                    "RESCALED wall BVP failed for "
                    f"half_window={half_window}: "
                    f"{result.message}"
                )

            sample = np.linspace(
                x_left,
                x_right,
                40_000,
            )

            state = result.sol(
                sample
            )

            p = np.asarray(
                state[0],
                dtype=float,
            )

            pp = np.asarray(
                state[1],
                dtype=float,
            )

            z = np.asarray(
                state[2],
                dtype=float,
            )

            zp = np.asarray(
                state[3],
                dtype=float,
            )

            if (
                np.min(z) < -2.0e-3
                or
                np.max(z) > 1.002
            ):
                raise RuntimeError(
                    "Gate field left physical wall basin"
                )

            z_monotone = np.maximum.accumulate(
                np.clip(
                    z,
                    0.0,
                    1.0,
                )
            )

            x10 = float(
                np.interp(
                    0.10,
                    z_monotone,
                    sample,
                )
            )

            x50 = float(
                np.interp(
                    0.50,
                    z_monotone,
                    sample,
                )
            )

            x90 = float(
                np.interp(
                    0.90,
                    z_monotone,
                    sample,
                )
            )

            # ----------------------------------------------------------
            # Gate energy
            # ----------------------------------------------------------

            gate_prefactor_j = (
                4.0
                * math.pi
                * V_S_EV**2
                / m_x_ev
                * J_PER_EV
            )

            gate_gradient_density = (
                0.5
                * zp**2
            )

            gate_potential_density = (
                a2
                / 4.0
                * (
                    z**2
                    -1.0
                )**2
            )

            # b2*u^2 = a2*p^2 exactly.
            interaction_density = (
                0.5
                * a2
                * z**2
                * p**2
            )

            def gate_integral(
                density,
            ):
                return (
                    gate_prefactor_j
                    * np.trapezoid(
                        sample**2
                        * density,
                        sample,
                    )
                )

            # Inside x_left, z~0.
            interior_false_j = (
                gate_prefactor_j
                * (
                    a2 / 4.0
                )
                * x_left**3
                / 3.0
            )

            gradient_j = gate_integral(
                gate_gradient_density
            )

            potential_j = gate_integral(
                gate_potential_density
            )

            interaction_j = gate_integral(
                interaction_density
            )

            p_right = float(
                result.sol(
                    x_right
                )[0]
            )

            def p_outer_tail(x):
                return (
                    p_right
                    * x_right
                    / x
                    * math.exp(
                        -epsilon_off
                        * (
                            x
                            - x_right
                        )
                    )
                )

            interaction_outer_j = (
                gate_prefactor_j
                * quad(
                    lambda x:
                        x**2
                        *0.5
                        *a2
                        *p_outer_tail(x)**2,
                    x_right,
                    np.inf,
                    epsabs=1.0e-15,
                    epsrel=1.0e-9,
                    limit=300,
                )[0]
            )

            gate_total_j = (
                interior_false_j
                +gradient_j
                +potential_j
                +interaction_j
                +interaction_outer_j
            )

            # ----------------------------------------------------------
            # Scalar-tail energy change
            # ----------------------------------------------------------

            scalar_prefactor_j = (
                4.0
                * math.pi
                * M_c_ev**2
                / m_x_ev
                * J_PER_EV
            )

            u = (
                u_transition
                * p
            )

            up = (
                u_transition
                * pp
            )

            scalar_new_local_j = (
                scalar_prefactor_j
                * np.trapezoid(
                    sample**2
                    * (
                        0.5
                        * up**2
                        +0.5
                        * epsilon**2
                        * u**2
                    ),
                    sample,
                )
            )

            u_right = (
                u_transition
                * p_right
            )

            def new_scalar_outer(x):
                uo = (
                    u_right
                    * x_right
                    / x
                    * math.exp(
                        -epsilon_off
                        * (
                            x
                            - x_right
                        )
                    )
                )

                upo = (
                    -epsilon_off
                    -1.0 / x
                ) * uo

                return (
                    x**2
                    * (
                        0.5
                        * upo**2
                        +0.5
                        * epsilon**2
                        * uo**2
                    )
                )

            scalar_new_outer_j = (
                scalar_prefactor_j
                * quad(
                    new_scalar_outer,
                    x_right,
                    np.inf,
                    epsabs=1.0e-15,
                    epsrel=1.0e-9,
                    limit=300,
                )[0]
            )

            def old_scalar_tail(x):
                uo = float(
                    u_light(
                        x
                    )
                )

                upo = float(
                    up_light(
                        x
                    )
                )

                return (
                    x**2
                    * (
                        0.5
                        * upo**2
                        +0.5
                        * epsilon**2
                        * uo**2
                    )
                )

            scalar_old_tail_j = (
                scalar_prefactor_j
                * quad(
                    old_scalar_tail,
                    x_left,
                    np.inf,
                    epsabs=1.0e-15,
                    epsrel=1.0e-9,
                    limit=300,
                )[0]
            )

            scalar_new_tail_j = (
                scalar_new_local_j
                +scalar_new_outer_j
            )

            scalar_tail_delta_j = (
                scalar_new_tail_j
                -scalar_old_tail_j
            )

            new_uprime_left = (
                u_transition
                * float(
                    result.sol(
                        x_left
                    )[1]
                )
            )

            old_uprime_left = float(
                up_light(
                    x_left
                )
            )

            derivative_rel_mismatch = relerr(
                new_uprime_left,
                old_uprime_left,
            )

            right_z = float(
                result.sol(
                    x_right
                )[2]
            )

            right_z_deviation = abs(
                1.0
                - right_z
            )

            max_rms = float(
                np.max(
                    result.rms_residuals
                )
            )

            row = {
                "half_window_x":
                    half_window,

                "nodes":
                    int(
                        result.x.size
                    ),

                "max_rms_residual":
                    max_rms,

                "x_left":
                    x_left,

                "x_right":
                    x_right,

                "p_left":
                    p_left,

                "x10":
                    x10,

                "x50":
                    x50,

                "x90":
                    x90,

                "r10_m":
                    x10
                    * x_length_m,

                "r50_m":
                    x50
                    * x_length_m,

                "r90_m":
                    x90
                    * x_length_m,

                "wall_10_90_width_m":
                    (
                        x90
                        -x10
                    )
                    * x_length_m,

                "inner_uprime_rel_mismatch":
                    derivative_rel_mismatch,

                "right_z_deviation":
                    right_z_deviation,

                "interior_false_J":
                    interior_false_j,

                "gradient_J":
                    gradient_j,

                "gate_potential_J":
                    potential_j,

                "interaction_local_J":
                    interaction_j,

                "interaction_outer_J":
                    interaction_outer_j,

                "gate_total_positive_J":
                    gate_total_j,

                "scalar_old_tail_J":
                    scalar_old_tail_j,

                "scalar_new_tail_J":
                    scalar_new_tail_j,

                "scalar_tail_delta_J":
                    scalar_tail_delta_j,

                "conservative_total_J":
                    operating_energy_j
                    +gate_total_j,

                "matched_total_J":
                    operating_energy_j
                    +gate_total_j
                    +scalar_tail_delta_j,
            }

            wall_rows.append(
                row
            )

            print(
                f"WALL "
                f"HALF_X={half_window:.1f} "
                f"NODES={result.x.size} "
                f"R50_M={row['r50_m']:.9f} "
                f"WIDTH10_90_M="
                f"{row['wall_10_90_width_m']:.9f} "
                f"GATE_J="
                f"{gate_total_j:.12e} "
                f"INTERACTION_J="
                f"{interaction_j + interaction_outer_j:.12e} "
                f"SCALAR_DELTA_J="
                f"{scalar_tail_delta_j:+.12e} "
                f"DERIV_MISMATCH="
                f"{derivative_rel_mismatch:.6e} "
                f"RMS={max_rms:.6e}"
            )

        print(
            "\n=== STAGE C: DOMAIN/WINDOW CONVERGENCE ==="
        )

        # Use the largest three windows for convergence.
        convergence_rows = (
            wall_rows[-3:]
        )

        r50_values = np.array(
            [
                row["r50_m"]
                for row
                in convergence_rows
            ],
            dtype=float,
        )

        gate_values = np.array(
            [
                row[
                    "gate_total_positive_J"
                ]
                for row
                in convergence_rows
            ],
            dtype=float,
        )

        r50_spread = (
            np.max(
                r50_values
            )
            -np.min(
                r50_values
            )
        ) / max(
            np.mean(
                r50_values
            ),
            1.0e-300,
        )

        gate_spread = (
            np.max(
                gate_values
            )
            -np.min(
                gate_values
            )
        ) / max(
            np.mean(
                gate_values
            ),
            1.0e-300,
        )

        max_derivative_mismatch = max(
            row[
                "inner_uprime_rel_mismatch"
            ]
            for row
            in convergence_rows
        )

        max_outer_z_deviation = max(
            row[
                "right_z_deviation"
            ]
            for row
            in convergence_rows
        )

        max_rms = max(
            row[
                "max_rms_residual"
            ]
            for row
            in convergence_rows
        )

        reference = (
            convergence_rows[-1]
        )

        gate_fraction = (
            reference[
                "gate_total_positive_J"
            ]
            / operating_energy_j
        )

        wall_convergence_pass = bool(
            r50_spread
            <= WALL_RADIUS_REL_SPREAD_MAX
            and
            gate_spread
            <= WALL_ENERGY_REL_SPREAD_MAX
        )

        matching_pass = bool(
            max_derivative_mismatch
            <= INNER_DERIVATIVE_REL_MISMATCH_MAX
        )

        asymptotic_pass = bool(
            max_outer_z_deviation
            <= OUTER_Z_DEVIATION_MAX
        )

        residual_pass = bool(
            max_rms
            <= MAX_RMS_RESIDUAL
        )

        energy_pass = bool(
            gate_fraction
            <= GATE_ENERGY_FRACTION_MAX
        )

        off_stability_pass = bool(
            stabilized_lambda0
            > 0.0
        )

        print(
            f"WALL_R50_REL_SPREAD="
            f"{r50_spread:.15e}"
        )

        print(
            f"GATE_ENERGY_REL_SPREAD="
            f"{gate_spread:.15e}"
        )

        print(
            f"MAX_INNER_DERIVATIVE_REL_MISMATCH="
            f"{max_derivative_mismatch:.15e}"
        )

        print(
            f"MAX_OUTER_Z_DEVIATION="
            f"{max_outer_z_deviation:.15e}"
        )

        print(
            f"MAX_BVP_RMS_RESIDUAL="
            f"{max_rms:.15e}"
        )

        print(
            f"WALL_CONVERGENCE_PASS="
            f"{wall_convergence_pass}"
        )

        print(
            f"INNER_MATCHING_PASS="
            f"{matching_pass}"
        )

        print(
            f"OUTER_ASYMPTOTIC_PASS="
            f"{asymptotic_pass}"
        )

        print(
            f"BVP_RESIDUAL_PASS="
            f"{residual_pass}"
        )

        print(
            f"OFF_STATE_LINEAR_STABILIZATION_PASS="
            f"{off_stability_pass}"
        )

        print(
            f"REFERENCE_GATE_TOTAL_POSITIVE_J="
            f"{reference['gate_total_positive_J']:.15e}"
        )

        print(
            f"REFERENCE_GATE_ENERGY_FRACTION="
            f"{gate_fraction:.15e}"
        )

        print(
            f"REFERENCE_INTERACTION_ENERGY_J="
            f"{reference['interaction_local_J'] + reference['interaction_outer_J']:.15e}"
        )

        print(
            f"REFERENCE_SCALAR_TAIL_DELTA_J="
            f"{reference['scalar_tail_delta_J']:+.15e}"
        )

        print(
            f"CONSERVATIVE_TOTAL_WITH_GATE_GJ="
            f"{reference['conservative_total_J'] / 1.0e9:.12f}"
        )

        print(
            "\n=== STAGE D: DECISION ==="
        )

        green = bool(
            wall_convergence_pass
            and
            matching_pass
            and
            asymptotic_pass
            and
            residual_pass
            and
            off_stability_pass
            and
            energy_pass
        )

        if green:
            classification = (
                "GREEN_D2BR_RESCALED_RECIPROCAL_"
                "EXTERIOR_GATE_WALL_EXISTS_AND_CONVERGES"
            )

            next_action = (
                "031D2C_FULL_FIXED_Q_COUPLED_Y_U_Z_"
                "ON_OFF_SOURCE_BVP_AND_SWITCHING_BARRIER"
            )

        else:
            classification = (
                "YELLOW_D2BR_RESCALED_GATE_WALL_"
                "HAS_UNCLOSED_NUMERICAL_OR_MATCHING_SUBGATE"
            )

            next_action = (
                "REFINE_ONLY_FAILED_D2BR_SUBGATE"
            )

        print(
            f"031D2BR_CLASSIFICATION="
            f"{classification}"
        )

        print(
            f"NEXT={next_action}"
        )

        print(
            "FULL_Y_U_Z_SOURCE_BVP_CLOSED=NO"
        )

        print(
            "SWITCHING_BARRIER_CLOSED=NO"
        )

        print(
            "FORMATION_RESET_ENERGY_CLOSED=NO"
        )

        print(
            "FULL_METRIC_BACKREACTION_CLOSED=NO"
        )

        print(
            "RADIATIVE_NATURALNESS_CLOSED=NO"
        )

        print(
            "PRACTICAL_DEVICE=NO"
        )

        summary = {
            "classification":
                classification,

            "next":
                next_action,

            "candidate": {
                "g_s":
                    G_S,

                "v_s_eV":
                    V_S_EV,

                "lambda_s":
                    LAMBDA_S,

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

                "transition_radius_m":
                    r_transition_m,
            },

            "rescaling": {
                "definition":
                    "p=u/u_transition",

                "identity_relerr":
                    identity_error,

                "equations":
                    [
                        (
                            "p''+2p'/x="
                            "(epsilon^2+delta2*z^2)*p"
                        ),
                        (
                            "z''+2z'/x="
                            "a2*(z^2-1+p^2)*z"
                        ),
                    ],
            },

            "off_state": {
                "stabilized_lambda0":
                    stabilized_lambda0,

                "pass":
                    off_stability_pass,
            },

            "wall_rows":
                wall_rows,

            "convergence": {
                "r50_rel_spread":
                    r50_spread,

                "gate_energy_rel_spread":
                    gate_spread,

                "max_inner_derivative_rel_mismatch":
                    max_derivative_mismatch,

                "max_outer_z_deviation":
                    max_outer_z_deviation,

                "max_bvp_rms_residual":
                    max_rms,

                "wall_convergence_pass":
                    wall_convergence_pass,

                "matching_pass":
                    matching_pass,

                "asymptotic_pass":
                    asymptotic_pass,

                "residual_pass":
                    residual_pass,
            },

            "reference":
                reference,

            "claim_limits": [
                (
                    "The large D2B coefficient was removed by "
                    "an exact field normalization, not altered physics."
                ),
                (
                    "This remains an exterior phi+s solve."
                ),
                (
                    "The Q-ball y field is inherited rather than "
                    "re-solved with the gate."
                ),
                (
                    "Positive gate interaction energy is included."
                ),
                (
                    "Switching, formation/reset and radiation "
                    "remain open."
                ),
                (
                    "Full metric backreaction, EFT naturalness "
                    "and empirical closure remain open."
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
                for row in wall_rows
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
                wall_rows
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}"
        )

        print(
            f"WALL_CSV={OUT_CSV}"
        )

    finally:
        qmod.X_MATCH = old_x_match


if __name__ == "__main__":
    main()
