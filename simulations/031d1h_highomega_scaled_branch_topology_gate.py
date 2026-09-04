"""
031D1H — high-Omega same-charge Q-ball branch identity/topology audit

PURPOSE
-------
031D1-R2 established that the clean low-Omega same-Noether-charge
unscalarized Q-ball branch is source-viable but has a robust scalar
tachyon.

Before declaring an auxiliary off-state gate mandatory, we must close
the only remaining nodeless same-charge loophole: the high-Omega
(thick-wall) Q-ball branch.

The numerically appropriate variables near Omega -> 1 are

    mu  = sqrt(1 - Omega^2)
    rho = mu x
    y   = mu f

which transform

    y'' + 2 y'/x = y/(1+y^2) - Omega^2 y

into

    f'' + 2 f'/rho
        = f - f^3/(1 + mu^2 f^2).

The asymptotic decay mass in rho is exactly unity, so one fixed rho
domain works even arbitrarily close to Omega=1.

SCIENTIFIC QUESTION
-------------------
How many nodeless ground-state u=0 Q-ball configurations carry the
same conserved charge as the GREEN scalarized on-state, and is the
high-Omega member a viable stable off-state source?

PROMOTION / FALSIFICATION
-------------------------
If the entire nodeless ground-state family has exactly two same-Q
crossings,
    * low branch = the already-certified scalar tachyon, and
    * high branch has dQ/dOmega > 0,
then the current gate-free same-charge off-state route is closed:
one branch fails scalar stability and the other fails source stability.

This does not close auxiliary gate architectures.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

QBALL_SOURCE = (
    SIM / "031b2a_global_qball_activated_scalar_control.py"
)

D1_SOURCE = (
    SIM / "031d1_qball_self_activation_offstate_fixed_charge_gate.py"
)

ROBUST_SUMMARY = (
    DATA / "031c96_operating_margin_robustness_summary.json"
)

LOW_SUMMARY = (
    DATA / "031d1r2_lowbranch_offstate_hessian_summary.json"
)

D96_SUMMARY = (
    DATA / "031b2d96_combined_coupled_linear_goldstone_summary.json"
)

OUT_JSON = (
    DATA / "031d1h_highomega_branch_summary.json"
)

OUT_CSV = (
    DATA / "031d1h_scaled_groundstate_branch.csv"
)


RHO_MAX = 30.0
RHO0 = 1.0e-6

TARGET_ROOT_REL_TOL = 2.0e-8

OMEGA_ON = 0.34

# Global nodeless branch grid.
MU_GRID = np.unique(
    np.concatenate(
        (
            np.geomspace(
                1.0e-4,
                2.0e-2,
                32,
            ),
            np.linspace(
                0.025,
                0.80,
                80,
            ),
            np.linspace(
                0.805,
                0.90,
                49,
            ),
        )
    )
)

HBARC_EV_M = 1.973269804e-7


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


def builtin(value):
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


def W(y):
    return 0.5 * np.log1p(
        y * y
    )


def count_nodes(solution) -> int:
    rho = np.linspace(
        RHO0,
        RHO_MAX,
        5000,
    )

    f = np.asarray(
        solution.sol(rho)[0],
        dtype=float,
    )

    scale = max(
        float(
            np.max(
                np.abs(f)
            )
        ),
        1.0e-300,
    )

    significant = f[
        np.abs(f)
        > 1.0e-6 * scale
    ]

    if len(significant) < 2:
        return 0

    signs = np.sign(
        significant
    )

    return int(
        np.sum(
            signs[1:]
            * signs[:-1]
            < 0.0
        )
    )


def scaled_equations(
    rho,
    state,
    mu,
):
    f = state[0]

    rhs = (
        f
        -f * f * f
        / (
            1.0
            +mu * mu * f * f
        )
    )

    return np.vstack(
        (
            state[1],
            rhs
            -2.0
            * state[1]
            / rho,
        )
    )


def boundary_conditions(
    left,
    right,
):
    return np.array(
        (
            left[1],
            right[1]
            +(
                1.0
                +1.0 / RHO_MAX
            )
            *right[0],
        ),
        dtype=float,
    )


def solve_thick_wall_limit():
    """
    Solve the mu=0 limiting cubic ground state.

        f'' + 2f'/rho = f - f^3.
    """

    rho = np.linspace(
        RHO0,
        RHO_MAX,
        2000,
    )

    amplitude = 4.0

    f = (
        amplitude
        *np.exp(-rho)
        / (
            1.0
            +0.2 * rho
        )
    )

    fp = (
        f
        *(
            -1.0
            -0.2
            / (
                1.0
                +0.2 * rho
            )
        )
    )

    guess = np.vstack(
        (
            f,
            fp,
        )
    )

    solution = solve_bvp(
        lambda r, s:
            scaled_equations(
                r,
                s,
                0.0,
            ),
        boundary_conditions,
        rho,
        guess,
        tol=5.0e-7,
        max_nodes=60_000,
        verbose=0,
    )

    if not solution.success:
        raise RuntimeError(
            "Failed to solve thick-wall limiting ground state"
        )

    if count_nodes(
        solution
    ) != 0:
        raise RuntimeError(
            "Thick-wall limiting solution is nodeful"
        )

    if abs(
        float(
            solution.sol(
                RHO0
            )[0]
        )
    ) < 1.0:
        raise RuntimeError(
            "Thick-wall solver collapsed toward trivial branch"
        )

    return solution


def solve_scaled(
    mu: float,
    previous,
    tolerance: float = 8.0e-7,
):
    rho = np.linspace(
        RHO0,
        RHO_MAX,
        1400,
    )

    guess = np.asarray(
        previous.sol(rho),
        dtype=float,
    )

    solution = solve_bvp(
        lambda r, s:
            scaled_equations(
                r,
                s,
                mu,
            ),
        boundary_conditions,
        rho,
        guess,
        tol=tolerance,
        max_nodes=70_000,
        verbose=0,
    )

    if not solution.success:
        return None

    if count_nodes(
        solution
    ) != 0:
        return None

    if abs(
        float(
            solution.sol(
                RHO0
            )[0]
        )
    ) < 1.0e-3:
        return None

    return solution


def branch_metrics(
    solution,
    mu: float,
    points: int = 30_000,
):
    omega = math.sqrt(
        max(
            1.0 - mu * mu,
            0.0,
        )
    )

    rho = np.linspace(
        RHO0,
        RHO_MAX,
        points,
    )

    state = solution.sol(
        rho
    )

    f = np.asarray(
        state[0],
        dtype=float,
    )

    fp = np.asarray(
        state[1],
        dtype=float,
    )

    j2 = float(
        4.0
        *math.pi
        *np.trapezoid(
            rho * rho * f * f,
            rho,
        )
    )

    I_Q = (
        omega
        / mu
        *j2
    )

    grad_density = (
        0.5
        *mu
        *fp * fp
    )

    kinetic_density = (
        0.5
        *omega * omega
        / mu
        *f * f
    )

    potential_density = (
        0.5
        / (
            mu * mu * mu
        )
        *np.log1p(
            mu * mu
            *f * f
        )
    )

    I_E = float(
        4.0
        *math.pi
        *np.trapezoid(
            rho * rho
            *(
                grad_density
                +kinetic_density
                +potential_density
            ),
            rho,
        )
    )

    return {
        "mu":
            float(mu),
        "omega":
            float(omega),
        "I_Q":
            float(I_Q),
        "I_E":
            float(I_E),
        "E_over_QmX":
            float(
                I_E / I_Q
            ),
        "f0":
            float(
                solution.sol(
                    RHO0
                )[0]
            ),
        "y0":
            float(
                mu
                *solution.sol(
                    RHO0
                )[0]
            ),
        "nodes":
            count_nodes(
                solution
            ),
        "J2":
            j2,
    }


def refine_root(
    target_q: float,
    left,
    right,
):
    mu_lo, sol_lo, met_lo = left
    mu_hi, sol_hi, met_hi = right

    f_lo = (
        met_lo["I_Q"]
        -target_q
    )

    f_hi = (
        met_hi["I_Q"]
        -target_q
    )

    if f_lo * f_hi > 0.0:
        raise RuntimeError(
            "Invalid same-Q root bracket"
        )

    best = (
        left
        if abs(f_lo) < abs(f_hi)
        else right
    )

    for iteration in range(60):
        mu_mid = (
            0.5
            *(
                mu_lo
                +mu_hi
            )
        )

        seed = (
            sol_lo
            if abs(
                mu_mid
                -mu_lo
            )
            <=
            abs(
                mu_hi
                -mu_mid
            )
            else sol_hi
        )

        sol_mid = solve_scaled(
            mu_mid,
            seed,
            tolerance=2.0e-8,
        )

        if sol_mid is None:
            other = (
                sol_hi
                if seed is sol_lo
                else sol_lo
            )

            sol_mid = solve_scaled(
                mu_mid,
                other,
                tolerance=2.0e-8,
            )

        if sol_mid is None:
            raise RuntimeError(
                f"Root continuation failed at mu={mu_mid}"
            )

        met_mid = branch_metrics(
            sol_mid,
            mu_mid,
            points=50_000,
        )

        f_mid = (
            met_mid["I_Q"]
            -target_q
        )

        q_rel = (
            abs(f_mid)
            / target_q
        )

        print(
            f"ROOT_REFINE "
            f"ITER={iteration} "
            f"MU={mu_mid:.15e} "
            f"OMEGA={met_mid['omega']:.15e} "
            f"Q_RELERR={q_rel:.6e}"
        )

        if (
            abs(f_mid)
            <
            abs(
                best[2]["I_Q"]
                -target_q
            )
        ):
            best = (
                mu_mid,
                sol_mid,
                met_mid,
            )

        if q_rel <= TARGET_ROOT_REL_TOL:
            return (
                mu_mid,
                sol_mid,
                met_mid,
            )

        if f_lo * f_mid <= 0.0:
            mu_hi = mu_mid
            sol_hi = sol_mid
            met_hi = met_mid
            f_hi = f_mid
        else:
            mu_lo = mu_mid
            sol_lo = sol_mid
            met_lo = met_mid
            f_lo = f_mid

    return best


def dq_domega(
    root_mu,
    root_solution,
    target_q,
):
    delta_mu = min(
        5.0e-5,
        0.02 * root_mu,
    )

    delta_mu = max(
        delta_mu,
        2.0e-6,
    )

    mu_minus = (
        root_mu
        -delta_mu
    )

    mu_plus = (
        root_mu
        +delta_mu
    )

    minus = solve_scaled(
        mu_minus,
        root_solution,
        tolerance=2.0e-8,
    )

    plus = solve_scaled(
        mu_plus,
        root_solution,
        tolerance=2.0e-8,
    )

    if (
        minus is None
        or plus is None
    ):
        raise RuntimeError(
            "Failed derivative continuation around high root"
        )

    m_minus = branch_metrics(
        minus,
        mu_minus,
        points=40_000,
    )

    m_plus = branch_metrics(
        plus,
        mu_plus,
        points=40_000,
    )

    return (
        m_plus["I_Q"]
        -m_minus["I_Q"]
    ) / (
        m_plus["omega"]
        -m_minus["omega"]
    )


def charge_radii(
    solution,
    mu,
    m_x_gev,
):
    rho = np.linspace(
        RHO0,
        RHO_MAX,
        80_000,
    )

    f = np.asarray(
        solution.sol(
            rho
        )[0],
        dtype=float,
    )

    density = (
        rho * rho
        *f * f
    )

    increments = (
        0.5
        *(
            density[1:]
            +density[:-1]
        )
        *np.diff(rho)
    )

    cumulative = np.concatenate(
        (
            [0.0],
            np.cumsum(
                increments
            ),
        )
    )

    cumulative /= cumulative[-1]

    m_x_ev = (
        m_x_gev
        *1.0e9
    )

    compton_m = (
        HBARC_EV_M
        /m_x_ev
    )

    result = {}

    for fraction in (
        0.50,
        0.90,
        0.99,
    ):
        rho_f = float(
            np.interp(
                fraction,
                cumulative,
                rho,
            )
        )

        x_f = (
            rho_f
            /mu
        )

        result[
            f"rho_{int(100*fraction)}"
        ] = rho_f

        result[
            f"x_{int(100*fraction)}"
        ] = x_f

        result[
            f"radius_{int(100*fraction)}_m"
        ] = (
            x_f
            *compton_m
        )

    return result


def main():
    print(
        "=== 031D1H SCALED HIGH-OMEGA BRANCH TOPOLOGY GATE ==="
    )

    print(
        "BRANCH_VARIABLES="
        "MU_SQRT_1_MINUS_OMEGA2_RHO_MU_X_Y_MU_F"
    )

    print(
        "NODEFUL_EXCITED_STATES_ACCEPTED=NO"
    )

    print(
        "AUXILIARY_GATE_INCLUDED=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        QBALL_SOURCE,
        D1_SOURCE,
        ROBUST_SUMMARY,
        LOW_SUMMARY,
        D96_SUMMARY,
    ):
        require(path)

    robust = json.loads(
        ROBUST_SUMMARY.read_text()
    )

    low = json.loads(
        LOW_SUMMARY.read_text()
    )

    d96 = json.loads(
        D96_SUMMARY.read_text()
    )

    if not bool(
        low.get(
            "low_branch_robust_tachyon",
            False,
        )
    ):
        raise RuntimeError(
            "031D1-R2 low branch is not certified tachyonic"
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

    if not str(
        d96.get(
            "classification",
            "",
        )
    ).startswith(
        "GREEN_96GJ_INTRINSIC_QBALL"
    ):
        raise RuntimeError(
            "D96 intrinsic source stability is not GREEN"
        )

    qmod = load_module(
        "qball031d1h",
        QBALL_SOURCE,
    )

    d1 = load_module(
        "d1helpers031d1h",
        D1_SOURCE,
    )

    candidate = robust[
        "candidate"
    ]

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

    print(
        "\n=== STAGE A: INDEPENDENT ON-STATE CHARGE ==="
    )

    original_xmatch = float(
        qmod.X_MATCH
    )

    original_d1_xmatch = float(
        d1.X_MATCH_SOURCE
    )

    qmod.X_MATCH = 80.0
    d1.X_MATCH_SOURCE = 80.0

    try:
        seed_on = (
            qmod.solve_uncoupled_qball(
                OMEGA_ON
            )
        )

        if seed_on is None:
            raise RuntimeError(
                "Failed on-state seed"
            )

        on_solution = qmod.solve_coupled(
            seed_on,
            OMEGA_ON,
            epsilon,
            chi,
            previous=None,
        )

        if on_solution is None:
            raise RuntimeError(
                "Failed on-state reconstruction"
            )

        on_metrics = d1.coupled_integrals(
            on_solution,
            OMEGA_ON,
            epsilon,
            chi,
        )

        target_q = float(
            on_metrics["I_Q"]
        )

    finally:
        qmod.X_MATCH = (
            original_xmatch
        )

        d1.X_MATCH_SOURCE = (
            original_d1_xmatch
        )

    print(
        f"TARGET_I_Q={target_q:.15e}"
    )

    print(
        "\n=== STAGE B: THICK-WALL LIMIT ==="
    )

    limit_solution = (
        solve_thick_wall_limit()
    )

    rho = np.linspace(
        RHO0,
        RHO_MAX,
        50_000,
    )

    f_limit = np.asarray(
        limit_solution.sol(
            rho
        )[0],
        dtype=float,
    )

    K_Q = float(
        4.0
        *math.pi
        *np.trapezoid(
            rho * rho
            *f_limit * f_limit,
            rho,
        )
    )

    mu_prediction = (
        K_Q
        /target_q
    )

    omega_prediction = math.sqrt(
        1.0
        -mu_prediction
        *mu_prediction
    )

    print(
        f"THICK_WALL_F0="
        f"{float(limit_solution.sol(RHO0)[0]):.15e}"
    )

    print(
        f"THICK_WALL_KQ="
        f"{K_Q:.15e}"
    )

    print(
        f"HIGH_ROOT_ASYMPTOTIC_MU="
        f"{mu_prediction:.15e}"
    )

    print(
        f"HIGH_ROOT_ASYMPTOTIC_OMEGA="
        f"{omega_prediction:.15e}"
    )

    print(
        "\n=== STAGE C: GLOBAL NODELESS GROUND-STATE CONTINUATION ==="
    )

    previous = (
        limit_solution
    )

    branch = []

    for mu in MU_GRID:
        solution = solve_scaled(
            float(mu),
            previous,
        )

        if solution is None:
            raise RuntimeError(
                f"Ground-state continuation failed at mu={mu}"
            )

        metrics = branch_metrics(
            solution,
            float(mu),
            points=12_000,
        )

        branch.append(
            (
                float(mu),
                solution,
                metrics,
            )
        )

        previous = solution

        print(
            f"BRANCH "
            f"MU={mu:.9e} "
            f"OMEGA={metrics['omega']:.12e} "
            f"I_Q={metrics['I_Q']:.9e} "
            f"E_OVER_Q={metrics['E_over_QmX']:.9e} "
            f"F0={metrics['f0']:.9e} "
            f"Y0={metrics['y0']:.9e} "
            f"NODES={metrics['nodes']}"
        )

    crossings = []

    for left, right in zip(
        branch[:-1],
        branch[1:],
        strict=True,
    ):
        f_left = (
            left[2]["I_Q"]
            -target_q
        )

        f_right = (
            right[2]["I_Q"]
            -target_q
        )

        if (
            f_left
            *f_right
            < 0.0
        ):
            crossings.append(
                (
                    left,
                    right,
                )
            )

    q_values = np.array(
        [
            item[2]["I_Q"]
            for item in branch
        ],
        dtype=float,
    )

    q_differences = np.diff(
        q_values
    )

    trend_signs = np.sign(
        q_differences
    )

    trend_reversals = int(
        np.sum(
            trend_signs[1:]
            *trend_signs[:-1]
            < 0.0
        )
    )

    minimum_index = int(
        np.argmin(
            q_values
        )
    )

    minimum_row = (
        branch[
            minimum_index
        ][2]
    )

    print(
        f"GLOBAL_TARGET_CROSSING_COUNT="
        f"{len(crossings)}"
    )

    print(
        f"GLOBAL_Q_TREND_REVERSAL_COUNT="
        f"{trend_reversals}"
    )

    print(
        f"GLOBAL_Q_MIN="
        f"{minimum_row['I_Q']:.15e}"
    )

    print(
        f"GLOBAL_Q_MIN_OMEGA="
        f"{minimum_row['omega']:.15e}"
    )

    if len(crossings) != 2:
        raise RuntimeError(
            "Expected exactly two same-Q nodeless crossings"
        )

    print(
        "\n=== STAGE D: REFINE BOTH SAME-Q ROOTS ==="
    )

    roots = []

    for crossing_id, bracket in enumerate(
        crossings
    ):
        root = refine_root(
            target_q,
            bracket[0],
            bracket[1],
        )

        roots.append(
            root
        )

        print(
            f"ROOT={crossing_id} "
            f"MU={root[0]:.15e} "
            f"OMEGA={root[2]['omega']:.15e} "
            f"I_Q={root[2]['I_Q']:.15e} "
            f"E_OVER_Q="
            f"{root[2]['E_over_QmX']:.15e}"
        )

    roots.sort(
        key=lambda item:
            item[2]["omega"]
    )

    low_root = roots[0]
    high_root = roots[1]

    low_omega_reference = float(
        low["omega_off"]
    )

    low_omega_relerr = (
        abs(
            low_root[2]["omega"]
            -low_omega_reference
        )
        /
        abs(
            low_omega_reference
        )
    )

    print(
        f"LOW_ROOT_OMEGA="
        f"{low_root[2]['omega']:.15e}"
    )

    print(
        f"LOW_ROOT_REFERENCE_OMEGA="
        f"{low_omega_reference:.15e}"
    )

    print(
        f"LOW_ROOT_OMEGA_RELERR="
        f"{low_omega_relerr:.15e}"
    )

    print(
        "\n=== STAGE E: HIGH-OMEGA SOURCE-STABILITY AUDIT ==="
    )

    high_mu = float(
        high_root[0]
    )

    high_solution = (
        high_root[1]
    )

    # Re-solve the final high root at tighter BVP tolerance.
    tight_high = solve_scaled(
        high_mu,
        high_solution,
        tolerance=5.0e-9,
    )

    if tight_high is None:
        raise RuntimeError(
            "Tight high-root reconstruction failed"
        )

    high_20k = branch_metrics(
        tight_high,
        high_mu,
        points=20_000,
    )

    high_40k = branch_metrics(
        tight_high,
        high_mu,
        points=40_000,
    )

    high_80k = branch_metrics(
        tight_high,
        high_mu,
        points=80_000,
    )

    eq_quadrature_relspread = (
        max(
            high_20k[
                "E_over_QmX"
            ],
            high_40k[
                "E_over_QmX"
            ],
            high_80k[
                "E_over_QmX"
            ],
        )
        -
        min(
            high_20k[
                "E_over_QmX"
            ],
            high_40k[
                "E_over_QmX"
            ],
            high_80k[
                "E_over_QmX"
            ],
        )
    ) / max(
        abs(
            high_80k[
                "E_over_QmX"
            ]
        ),
        1.0e-300,
    )

    slope = dq_domega(
        high_mu,
        tight_high,
        target_q,
    )

    high_source_slope_stable = bool(
        slope < 0.0
    )

    high_qball_bound_pass = bool(
        high_80k[
            "E_over_QmX"
        ] < 1.0
    )

    high_source_viable = bool(
        high_source_slope_stable
        and
        high_qball_bound_pass
    )

    print(
        f"HIGH_ROOT_MU="
        f"{high_mu:.15e}"
    )

    print(
        f"HIGH_ROOT_OMEGA="
        f"{high_80k['omega']:.15e}"
    )

    print(
        f"HIGH_ROOT_E_OVER_QMX_20K="
        f"{high_20k['E_over_QmX']:.15e}"
    )

    print(
        f"HIGH_ROOT_E_OVER_QMX_40K="
        f"{high_40k['E_over_QmX']:.15e}"
    )

    print(
        f"HIGH_ROOT_E_OVER_QMX_80K="
        f"{high_80k['E_over_QmX']:.15e}"
    )

    print(
        f"HIGH_ROOT_EQ_QUADRATURE_RELSPREAD="
        f"{eq_quadrature_relspread:.15e}"
    )

    print(
        f"HIGH_ROOT_DQ_DOMEGA="
        f"{slope:+.15e}"
    )

    print(
        f"HIGH_ROOT_SOURCE_SLOPE_STABLE="
        f"{high_source_slope_stable}"
    )

    print(
        f"HIGH_ROOT_QBALL_BOUND_PASS="
        f"{high_qball_bound_pass}"
    )

    print(
        f"HIGH_ROOT_SOURCE_VIABLE="
        f"{high_source_viable}"
    )

    print(
        "\n=== STAGE F: HIGH-ROOT SCALAR AND SIZE DIAGNOSTICS ==="
    )

    probe_rho = np.linspace(
        RHO0,
        RHO_MAX,
        80_000,
    )

    high_f = np.asarray(
        tight_high.sol(
            probe_rho
        )[0],
        dtype=float,
    )

    high_y = (
        high_mu
        *high_f
    )

    y_max = float(
        np.max(
            np.abs(
                high_y
            )
        )
    )

    scalar_potential_min = (
        epsilon * epsilon
        -chi * chi
        *float(
            W(
                y_max
            )
        )
    )

    scalar_pointwise_positive = bool(
        scalar_potential_min > 0.0
    )

    radii = charge_radii(
        tight_high,
        high_mu,
        m_x_gev,
    )

    print(
        f"HIGH_ROOT_Y_MAX="
        f"{y_max:.15e}"
    )

    print(
        f"HIGH_ROOT_SCALAR_OPERATOR_VMIN="
        f"{scalar_potential_min:+.15e}"
    )

    print(
        f"HIGH_ROOT_SCALAR_POINTWISE_POSITIVE="
        f"{scalar_pointwise_positive}"
    )

    print(
        f"HIGH_ROOT_R50_M="
        f"{radii['radius_50_m']:.15e}"
    )

    print(
        f"HIGH_ROOT_R90_M="
        f"{radii['radius_90_m']:.15e}"
    )

    print(
        f"HIGH_ROOT_R99_M="
        f"{radii['radius_99_m']:.15e}"
    )

    print(
        "\n=== STAGE G: FINAL GATE-FREE OFF-STATE DECISION ==="
    )

    topology_pass = bool(
        len(crossings) == 2
        and
        trend_reversals == 1
        and
        low_omega_relerr
        < 2.0e-4
    )

    low_branch_tachyonic = bool(
        low[
            "low_branch_robust_tachyon"
        ]
    )

    high_branch_fatal = bool(
        not high_source_slope_stable
    )

    gate_free_route_closed = bool(
        topology_pass
        and
        low_branch_tachyonic
        and
        high_branch_fatal
    )

    if gate_free_route_closed:
        classification = (
            "RED_D1H_GATE_FREE_SAME_Q_OFFSTATE_ROUTE_CLOSED_"
            "LOW_BRANCH_SCALAR_TACHYON_"
            "HIGH_BRANCH_QBALL_SOURCE_UNSTABLE"
        )

        next_action = (
            "031D2_MINIMUM_AUXILIARY_GATE_MASS_SHIFT_"
            "CONTROL_ENERGY_AND_RECIPROCITY"
        )

    elif not topology_pass:
        classification = (
            "YELLOW_D1H_NODELESS_BRANCH_TOPOLOGY_UNRESOLVED"
        )

        next_action = (
            "REFINE_ONLY_GLOBAL_GROUNDSTATE_CONTINUATION"
        )

    elif high_source_viable:
        classification = (
            "YELLOW_D1H_HIGH_OMEGA_SAME_Q_OFF_BRANCH_SURVIVES"
        )

        next_action = (
            "031D1H2_HIGH_BRANCH_FULL_STABILITY_AND_"
            "OPERATING_GEOMETRY_GATE"
        )

    else:
        classification = (
            "YELLOW_D1H_HIGH_BRANCH_FAILURE_NOT_YET_"
            "SUFFICIENTLY_CLASSIFIED"
        )

        next_action = (
            "REFINE_ONLY_HIGH_BRANCH_SOURCE_STABILITY"
        )

    print(
        f"NODELESS_BRANCH_TOPOLOGY_PASS="
        f"{topology_pass}"
    )

    print(
        f"LOW_BRANCH_ROBUST_TACHYON="
        f"{low_branch_tachyonic}"
    )

    print(
        f"HIGH_BRANCH_SOURCE_FATAL="
        f"{high_branch_fatal}"
    )

    print(
        f"GATE_FREE_SAME_Q_OFFSTATE_ROUTE_CLOSED="
        f"{gate_free_route_closed}"
    )

    print(
        f"AUXILIARY_GATE_REQUIRED="
        f"{gate_free_route_closed}"
    )

    print(
        f"031D1H_CLASSIFICATION="
        f"{classification}"
    )

    print(
        f"NEXT={next_action}"
    )

    print(
        "AUXILIARY_GATE_CONTROL_ENERGY_CLOSED=NO"
    )

    print(
        "RECIPROCITY_CLOSED=NO"
    )

    print(
        "FULL_METRIC_BACKREACTION_CLOSED=NO"
    )

    print(
        "NONLINEAR_FRAGMENTATION_CLOSED=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    rows = [
        item[2]
        for item in branch
    ]

    fields = sorted(
        {
            key
            for row in rows
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
            rows
        )

    summary = {
        "classification":
            classification,
        "next":
            next_action,
        "target_I_Q":
            target_q,
        "thick_wall": {
            "f0":
                float(
                    limit_solution.sol(
                        RHO0
                    )[0]
                ),
            "K_Q":
                K_Q,
            "predicted_high_mu":
                mu_prediction,
            "predicted_high_omega":
                omega_prediction,
        },
        "global_branch": {
            "same_Q_crossing_count":
                len(crossings),
            "Q_trend_reversal_count":
                trend_reversals,
            "Q_min":
                minimum_row["I_Q"],
            "Q_min_omega":
                minimum_row["omega"],
            "topology_pass":
                topology_pass,
        },
        "low_root": {
            "mu":
                low_root[0],
            **low_root[2],
            "omega_reference":
                low_omega_reference,
            "omega_relerr":
                low_omega_relerr,
            "robust_scalar_tachyon":
                low_branch_tachyonic,
            "lambda0_reference":
                low["finest_lambda0"],
            "critical_delta_m2_over_mphi2":
                low[
                    "critical_delta_m2_over_mphi2"
                ],
        },
        "high_root": {
            "mu":
                high_mu,
            **high_80k,
            "dq_domega":
                slope,
            "source_slope_stable":
                high_source_slope_stable,
            "qball_bound_pass":
                high_qball_bound_pass,
            "source_viable":
                high_source_viable,
            "E_over_Q_quadrature_relspread":
                eq_quadrature_relspread,
            "scalar_operator_Vmin":
                scalar_potential_min,
            "scalar_pointwise_positive":
                scalar_pointwise_positive,
            **radii,
        },
        "gate_free_same_Q_offstate_route_closed":
            gate_free_route_closed,
        "auxiliary_gate_required":
            gate_free_route_closed,
        "claim_limits": [
            (
                "Closure applies to the current nodeless "
                "same-Noether-charge u=0 Q-ball ground-state family."
            ),
            (
                "Nodeful excited Q-ball states are not accepted as "
                "stable device off states."
            ),
            (
                "The low branch is independently inherited as a "
                "converged scalar tachyon from 031D1-R2."
            ),
            (
                "An auxiliary-gate requirement does not yet establish "
                "that a viable or affordable gate exists."
            ),
            (
                "Gate/control stress-energy, switching energy and "
                "reciprocity remain open."
            ),
            (
                "Full physical metric, nonlinear stability, EFT "
                "naturalness and empirical closure remain open."
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

    print(
        f"SUMMARY_JSON={OUT_JSON}"
    )

    print(
        f"BRANCH_CSV={OUT_CSV}"
    )


if __name__ == "__main__":
    main()
