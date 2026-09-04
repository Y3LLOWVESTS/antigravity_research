"""
031D1-R — branch-tracked fixed-charge Q-ball off-state repair

Repairs the failed 031D1 root search.

The previous run established:
- the scalarized on-state reconstructs cleanly;
- target dimensionless Noether charge I_Q ~ 6594.22;
- a low-omega unscalarized crossing exists near omega ~ 0.494;
- a second apparent high-omega crossing exists near omega ~ 0.93;
- cold-start solves can jump between branches and fail inside brentq.

This run explicitly CONTINUES each candidate branch and never asks a
cold-start black-box solver to define a root function.

No gate field is introduced here.
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

from scipy.integrate import solve_bvp


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

QBALL_SOURCE = (
    SIM
    / "031b2a_global_qball_activated_scalar_control.py"
)

D1_SOURCE = (
    SIM
    / "031d1_qball_self_activation_offstate_fixed_charge_gate.py"
)

ROBUST_SUMMARY = (
    DATA
    / "031c96_operating_margin_robustness_summary.json"
)

D96_SUMMARY = (
    DATA
    / "031b2d96_combined_coupled_linear_goldstone_summary.json"
)

OUT_JSON = (
    DATA
    / "031d1r_branch_tracked_offstate_summary.json"
)

OUT_BRANCH_CSV = (
    DATA
    / "031d1r_branch_tracking_scan.csv"
)

OUT_HESSIAN_CSV = (
    DATA
    / "031d1r_offstate_hessian_scan.csv"
)


X_MATCH = 80.0

LOW_SEED_OMEGA = 0.495897436
LOW_SEARCH_MIN = 0.485
LOW_SEARCH_MAX = 0.502

HIGH_SEED_OMEGA = 0.930256410
HIGH_SEARCH_MIN = 0.910
HIGH_SEARCH_MAX = 0.940

CONTINUATION_STEP = 0.002

ROOT_Q_REL_TOL = 2.0e-8
ROOT_OMEGA_TOL = 2.0e-9

DQ_STEP = 7.5e-4

DOMAIN_EPS_R_VALUES = (
    1.2,
    3.0,
    5.0,
)

H_TARGETS = (
    0.50,
    0.25,
)

NEGATIVE_EIGENVALUE_TOL = 1.0e-6

GRID_REL_TOL = 5.0e-2
DOMAIN_REL_TOL = 5.0e-2

HBAR_GEV_S = 6.582119569e-25


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


def to_builtin(value: Any):
    if isinstance(value, np.generic):
        return value.item()

    if isinstance(value, np.ndarray):
        return value.tolist()

    if isinstance(value, dict):
        return {
            str(k): to_builtin(v)
            for k, v in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            to_builtin(v)
            for v in value
        ]

    return value


def count_nodes(solution) -> int:
    x = np.linspace(
        1.0e-5,
        X_MATCH,
        6000,
    )

    y = np.asarray(
        solution.sol(x)[0],
        dtype=float,
    )

    scale = max(
        float(np.max(np.abs(y))),
        1.0e-300,
    )

    mask = (
        np.abs(y)
        > 1.0e-5 * scale
    )

    significant = y[mask]

    if len(significant) < 2:
        return 0

    signs = np.sign(significant)

    return int(
        np.sum(
            signs[1:]
            * signs[:-1]
            < 0.0
        )
    )


def central_amplitude(solution) -> float:
    return abs(
        float(
            solution.sol(
                1.0e-5
            )[0]
        )
    )


def profile_distance(
    a,
    b,
) -> float:
    x = np.linspace(
        1.0e-5,
        X_MATCH,
        1200,
    )

    ya = np.asarray(
        a.sol(x)[0],
        dtype=float,
    )

    yb = np.asarray(
        b.sol(x)[0],
        dtype=float,
    )

    return float(
        np.linalg.norm(
            ya - yb
        )
        / max(
            np.linalg.norm(yb),
            1.0e-300,
        )
    )


def continuation_solve(
    qmod,
    omega: float,
    previous,
):
    """
    Solve at a new omega using the previous solution itself as the BVP
    initial profile. This preserves branch identity far better than the
    upstream cold-start helper.
    """

    r = np.linspace(
        1.0e-5,
        X_MATCH,
        1400,
    )

    guess = np.asarray(
        previous.sol(r),
        dtype=float,
    )

    decay = math.sqrt(
        max(
            1.0 - omega * omega,
            1.0e-10,
        )
    )

    def equations(
        x,
        state,
    ):
        y = state[0]

        return np.vstack(
            (
                state[1],
                qmod.dW(y)
                -omega * omega * y
                -2.0 * state[1] / x,
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
                    decay
                    +1.0 / X_MATCH
                )
                * right[0],
            ),
            dtype=float,
        )

    for tolerance in (
        1.0e-6,
        3.0e-6,
        1.0e-5,
    ):
        solution = solve_bvp(
            equations,
            boundary_conditions,
            r,
            guess,
            tol=tolerance,
            max_nodes=60_000,
            verbose=0,
        )

        if not solution.success:
            continue

        if central_amplitude(
            solution
        ) <= 1.0e-3:
            continue

        if count_nodes(
            solution
        ) != 0:
            continue

        return solution

    return None


def cold_nodeless_seed(
    qmod,
    omega: float,
):
    solution = qmod.solve_uncoupled_qball(
        omega
    )

    if solution is None:
        return None

    if count_nodes(
        solution
    ) != 0:
        return None

    return solution


def metric_record(
    d1,
    solution,
    omega: float,
    target_q: float,
    branch: str,
):
    metrics = d1.uncoupled_integrals(
        solution,
        omega,
    )

    return {
        "branch":
            branch,
        "omega":
            float(omega),
        "I_Q":
            float(metrics["I_Q"]),
        "I_E":
            float(metrics["I_E"]),
        "E_over_QmX":
            float(metrics["E_over_QmX"]),
        "Q_residual":
            float(
                metrics["I_Q"]
                -target_q
            ),
        "Q_rel_residual":
            abs(
                float(
                    metrics["I_Q"]
                    -target_q
                )
            )
            / max(
                abs(target_q),
                1.0e-300,
            ),
        "y0":
            central_amplitude(
                solution
            ),
        "nodes":
            count_nodes(
                solution
            ),
    }


def walk_branch(
    qmod,
    d1,
    branch: str,
    seed_omega: float,
    search_min: float,
    search_max: float,
    target_q: float,
):
    """
    Start from a deterministic nodeless cold seed, then walk in both
    omega directions with continuation.
    """

    seed = cold_nodeless_seed(
        qmod,
        seed_omega,
    )

    if seed is None:
        raise RuntimeError(
            f"{branch}: nodeless seed failed at "
            f"omega={seed_omega}"
        )

    records = [
        (
            seed_omega,
            seed,
            metric_record(
                d1,
                seed,
                seed_omega,
                target_q,
                branch,
            ),
        )
    ]

    for direction in (
        -1.0,
        +1.0,
    ):
        omega = seed_omega
        previous = seed

        while True:
            next_omega = (
                omega
                +direction
                * CONTINUATION_STEP
            )

            if (
                next_omega
                < search_min - 1.0e-12
                or
                next_omega
                > search_max + 1.0e-12
            ):
                break

            solution = continuation_solve(
                qmod,
                next_omega,
                previous,
            )

            if solution is None:
                print(
                    f"CONTINUATION branch={branch} "
                    f"omega={next_omega:.9f} "
                    "SUCCESS=False"
                )
                break

            distance = profile_distance(
                solution,
                previous,
            )

            record = metric_record(
                d1,
                solution,
                next_omega,
                target_q,
                branch,
            )

            record[
                "profile_distance_from_previous"
            ] = distance

            print(
                f"CONTINUATION branch={branch} "
                f"omega={next_omega:.9f} "
                f"I_Q={record['I_Q']:.9e} "
                f"Q_RES={record['Q_residual']:+.9e} "
                f"Y0={record['y0']:.9e} "
                f"DIST={distance:.6e} "
                f"NODES={record['nodes']}"
            )

            records.append(
                (
                    next_omega,
                    solution,
                    record,
                )
            )

            omega = next_omega
            previous = solution

    records.sort(
        key=lambda item:
        item[0]
    )

    return records


def locate_bracket(
    records,
):
    brackets = []

    for left, right in zip(
        records[:-1],
        records[1:],
        strict=True,
    ):
        f_left = float(
            left[2][
                "Q_residual"
            ]
        )

        f_right = float(
            right[2][
                "Q_residual"
            ]
        )

        if f_left == 0.0:
            brackets.append(
                (left, left)
            )

        elif (
            f_left * f_right
            < 0.0
        ):
            brackets.append(
                (left, right)
            )

    return brackets


def refine_charge_root(
    qmod,
    d1,
    branch: str,
    left,
    right,
    target_q: float,
):
    if left[0] == right[0]:
        return left

    lo_omega, lo_solution, lo_record = left
    hi_omega, hi_solution, hi_record = right

    lo_f = float(
        lo_record[
            "Q_residual"
        ]
    )

    hi_f = float(
        hi_record[
            "Q_residual"
        ]
    )

    if lo_f * hi_f > 0.0:
        raise RuntimeError(
            f"{branch}: invalid root bracket"
        )

    best = (
        left
        if abs(lo_f) < abs(hi_f)
        else right
    )

    for iteration in range(60):
        mid_omega = (
            0.5
            * (
                lo_omega
                +hi_omega
            )
        )

        if (
            abs(
                mid_omega
                -lo_omega
            )
            <=
            abs(
                hi_omega
                -mid_omega
            )
        ):
            first_seed = lo_solution
            second_seed = hi_solution
        else:
            first_seed = hi_solution
            second_seed = lo_solution

        mid_solution = continuation_solve(
            qmod,
            mid_omega,
            first_seed,
        )

        if mid_solution is None:
            mid_solution = continuation_solve(
                qmod,
                mid_omega,
                second_seed,
            )

        if mid_solution is None:
            raise RuntimeError(
                f"{branch}: continuation failed "
                f"inside root refinement at "
                f"omega={mid_omega}"
            )

        mid_record = metric_record(
            d1,
            mid_solution,
            mid_omega,
            target_q,
            branch,
        )

        mid_f = float(
            mid_record[
                "Q_residual"
            ]
        )

        if (
            abs(mid_f)
            <
            abs(
                float(
                    best[2][
                        "Q_residual"
                    ]
                )
            )
        ):
            best = (
                mid_omega,
                mid_solution,
                mid_record,
            )

        print(
            f"ROOT_REFINE branch={branch} "
            f"iter={iteration} "
            f"omega={mid_omega:.12f} "
            f"Q_RELERR="
            f"{mid_record['Q_rel_residual']:.6e}"
        )

        if (
            mid_record[
                "Q_rel_residual"
            ]
            <= ROOT_Q_REL_TOL
        ):
            return (
                mid_omega,
                mid_solution,
                mid_record,
            )

        if (
            hi_omega
            -lo_omega
            <= ROOT_OMEGA_TOL
        ):
            return best

        if lo_f * mid_f <= 0.0:
            hi_omega = mid_omega
            hi_solution = mid_solution
            hi_record = mid_record
            hi_f = mid_f
        else:
            lo_omega = mid_omega
            lo_solution = mid_solution
            lo_record = mid_record
            lo_f = mid_f

    return best


def branch_slope(
    qmod,
    d1,
    omega_root: float,
    root_solution,
):
    minus = continuation_solve(
        qmod,
        omega_root - DQ_STEP,
        root_solution,
    )

    plus = continuation_solve(
        qmod,
        omega_root + DQ_STEP,
        root_solution,
    )

    if (
        minus is None
        or
        plus is None
    ):
        return math.nan

    q_minus = float(
        d1.uncoupled_integrals(
            minus,
            omega_root - DQ_STEP,
        )["I_Q"]
    )

    q_plus = float(
        d1.uncoupled_integrals(
            plus,
            omega_root + DQ_STEP,
        )["I_Q"]
    )

    return (
        q_plus
        -q_minus
    ) / (
        2.0
        * DQ_STEP
    )


def hessian_audit(
    qmod,
    d1,
    branch: str,
    omega: float,
    solution,
    epsilon: float,
    chi: float,
):
    rows = []

    for epsilon_rmax in (
        DOMAIN_EPS_R_VALUES
    ):
        for h_target in H_TARGETS:
            row = d1.off_hessian_row(
                solution,
                omega,
                epsilon,
                chi,
                epsilon_rmax,
                h_target,
            )

            row[
                "branch"
            ] = branch

            row[
                "omega"
            ] = omega

            rows.append(row)

            print(
                f"HESSIAN branch={branch} "
                f"EPS_R={epsilon_rmax:.3f} "
                f"H={row['h']:.9f} "
                f"LAMBDA0="
                f"{row['lambda0']:+.12e} "
                f"GROWTH="
                f"{row['growth_dimensionless']:.12e}"
            )

    def select(
        eps_r,
        h_target,
    ):
        matches = [
            row
            for row in rows
            if abs(
                row["epsilon_rmax"]
                -eps_r
            ) < 1.0e-12
            and
            abs(
                row["h_target"]
                -h_target
            ) < 1.0e-12
        ]

        if len(matches) != 1:
            raise RuntimeError(
                "Missing Hessian convergence point"
            )

        return matches[0]

    fine5 = select(
        5.0,
        0.25,
    )

    coarse5 = select(
        5.0,
        0.50,
    )

    fine3 = select(
        3.0,
        0.25,
    )

    lambda0 = float(
        fine5["lambda0"]
    )

    grid_rel = d1.relerr(
        lambda0,
        float(
            coarse5[
                "lambda0"
            ]
        ),
    )

    domain_rel = d1.relerr(
        lambda0,
        float(
            fine3[
                "lambda0"
            ]
        ),
    )

    negative_all = all(
        float(
            row[
                "lambda0"
            ]
        )
        < -NEGATIVE_EIGENVALUE_TOL
        for row in rows
    )

    robust_tachyon = bool(
        negative_all
        and
        grid_rel
        <= GRID_REL_TOL
        and
        domain_rel
        <= DOMAIN_REL_TOL
    )

    growth_dimless = (
        math.sqrt(
            -lambda0
        )
        if lambda0 < 0.0
        else 0.0
    )

    return {
        "rows":
            rows,
        "lambda0_fine":
            lambda0,
        "grid_rel_difference":
            grid_rel,
        "domain_rel_difference":
            domain_rel,
        "robust_tachyon":
            robust_tachyon,
        "growth_dimensionless":
            growth_dimless,
    }


def main():
    print(
        "=== 031D1-R BRANCH-TRACKED FIXED-CHARGE OFF-STATE GATE ==="
    )

    print(
        "COLD_START_ROOT_FINDING=REMOVED"
    )

    print(
        "BRANCH_TRACKING=EXPLICIT_BVP_CONTINUATION"
    )

    print(
        "NODEFUL_BRANCHES_ACCEPTED=NO"
    )

    print(
        "AUXILIARY_GATE_FIELD_INCLUDED=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        QBALL_SOURCE,
        D1_SOURCE,
        ROBUST_SUMMARY,
        D96_SUMMARY,
    ):
        require(path)

    robust = json.loads(
        ROBUST_SUMMARY.read_text()
    )

    d96 = json.loads(
        D96_SUMMARY.read_text()
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
            "D96 intrinsic stability is not GREEN"
        )

    qmod = load_module(
        "qball031d1r",
        QBALL_SOURCE,
    )

    d1 = load_module(
        "d1helpers031d1r",
        D1_SOURCE,
    )

    candidate = robust[
        "candidate"
    ]

    quadrature = robust[
        "quadrature"
    ][
        "high_order_result"
    ]

    omega_on = float(
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

    original_x_match_q = float(
        qmod.X_MATCH
    )

    original_x_match_d1 = float(
        d1.X_MATCH_SOURCE
    )

    qmod.X_MATCH = X_MATCH
    d1.X_MATCH_SOURCE = X_MATCH

    try:
        print(
            "\n=== STAGE A: ON-STATE CHARGE RECONSTRUCTION ==="
        )

        seed_on = (
            qmod.solve_uncoupled_qball(
                omega_on
            )
        )

        if seed_on is None:
            raise RuntimeError(
                "On-state seed reconstruction failed"
            )

        on_solution = qmod.solve_coupled(
            seed_on,
            omega_on,
            epsilon,
            chi,
            previous=None,
        )

        if on_solution is None:
            raise RuntimeError(
                "On-state coupled reconstruction failed"
            )

        on = d1.coupled_integrals(
            on_solution,
            omega_on,
            epsilon,
            chi,
        )

        target_q = float(
            on["I_Q"]
        )

        print(
            f"TARGET_I_Q="
            f"{target_q:.15e}"
        )

        print(
            f"ON_E_OVER_QMX="
            f"{on['E_over_QmX']:.15e}"
        )

        print(
            "\n=== STAGE B: LOW-OMEGA BRANCH CONTINUATION ==="
        )

        low_records = walk_branch(
            qmod,
            d1,
            "low",
            LOW_SEED_OMEGA,
            LOW_SEARCH_MIN,
            LOW_SEARCH_MAX,
            target_q,
        )

        low_brackets = locate_bracket(
            low_records
        )

        print(
            f"LOW_BRANCH_BRACKETS="
            f"{len(low_brackets)}"
        )

        print(
            "\n=== STAGE C: HIGH-OMEGA BRANCH CONTINUATION ==="
        )

        high_records = walk_branch(
            qmod,
            d1,
            "high",
            HIGH_SEED_OMEGA,
            HIGH_SEARCH_MIN,
            HIGH_SEARCH_MAX,
            target_q,
        )

        high_brackets = locate_bracket(
            high_records
        )

        print(
            f"HIGH_BRANCH_BRACKETS="
            f"{len(high_brackets)}"
        )

        all_branch_rows = [
            item[2]
            for item
            in (
                low_records
                +high_records
            )
        ]

        root_inputs = []

        if len(
            low_brackets
        ) == 1:
            root_inputs.append(
                (
                    "low",
                    low_brackets[0],
                )
            )

        if len(
            high_brackets
        ) == 1:
            root_inputs.append(
                (
                    "high",
                    high_brackets[0],
                )
            )

        roots = []
        all_hessian_rows = []

        print(
            "\n=== STAGE D: SAME-Q ROOT REFINEMENT + STABILITY ==="
        )

        for branch, bracket in root_inputs:
            omega_root, solution, record = (
                refine_charge_root(
                    qmod,
                    d1,
                    branch,
                    bracket[0],
                    bracket[1],
                    target_q,
                )
            )

            slope = branch_slope(
                qmod,
                d1,
                omega_root,
                solution,
            )

            source_slope_stable = bool(
                math.isfinite(
                    slope
                )
                and
                slope < 0.0
            )

            q_bound = bool(
                float(
                    record[
                        "E_over_QmX"
                    ]
                )
                < 1.0
            )

            nodeless = bool(
                count_nodes(
                    solution
                )
                == 0
            )

            source_viable = bool(
                source_slope_stable
                and
                q_bound
                and
                nodeless
                and
                float(
                    record[
                        "Q_rel_residual"
                    ]
                )
                <= ROOT_Q_REL_TOL
            )

            chi_critical = (
                qmod.scalarization_critical_chi(
                    solution,
                    epsilon,
                )
            )

            chi_over_critical = (
                chi / chi_critical
                if (
                    chi_critical is not None
                    and
                    chi_critical > 0.0
                )
                else math.nan
            )

            audit = hessian_audit(
                qmod,
                d1,
                branch,
                omega_root,
                solution,
                epsilon,
                chi,
            )

            all_hessian_rows.extend(
                audit["rows"]
            )

            lambda0 = float(
                audit[
                    "lambda0_fine"
                ]
            )

            delta_m2_hat = max(
                0.0,
                -lambda0,
            )

            delta_m2_over_mphi2 = (
                delta_m2_hat
                / (
                    epsilon
                    * epsilon
                )
            )

            m_eff_over_mphi = math.sqrt(
                1.0
                +delta_m2_over_mphi2
            )

            growth_rate_s = (
                float(
                    audit[
                        "growth_dimensionless"
                    ]
                )
                *m_x_gev
                / HBAR_GEV_S
            )

            e_fold_s = (
                1.0
                / growth_rate_s
                if growth_rate_s > 0.0
                else math.inf
            )

            root = {
                **record,
                "dq_domega":
                    slope,
                "source_slope_stable":
                    source_slope_stable,
                "qball_bound":
                    q_bound,
                "nodeless":
                    nodeless,
                "source_viable":
                    source_viable,
                "chi_critical":
                    chi_critical,
                "chi_over_critical":
                    chi_over_critical,
                "lambda0_fine":
                    lambda0,
                "hessian_grid_rel_difference":
                    audit[
                        "grid_rel_difference"
                    ],
                "hessian_domain_rel_difference":
                    audit[
                        "domain_rel_difference"
                    ],
                "robust_tachyon":
                    audit[
                        "robust_tachyon"
                    ],
                "growth_dimensionless":
                    audit[
                        "growth_dimensionless"
                    ],
                "e_fold_time_s":
                    e_fold_s,
                "critical_positive_delta_m2_hat":
                    delta_m2_hat,
                "critical_delta_m2_over_mphi2":
                    delta_m2_over_mphi2,
                "critical_m_eff_over_mphi":
                    m_eff_over_mphi,
            }

            roots.append(root)

            print(
                f"ROOT branch={branch} "
                f"OMEGA={omega_root:.12e} "
                f"Q_RELERR="
                f"{record['Q_rel_residual']:.6e} "
                f"E_OVER_QMX="
                f"{record['E_over_QmX']:.9e} "
                f"DQ_DOMEGA="
                f"{slope:+.9e} "
                f"SOURCE_VIABLE="
                f"{source_viable} "
                f"CHI_CRIT="
                f"{chi_critical if chi_critical is not None else math.nan:.9e} "
                f"CHI_OVER_CRIT="
                f"{chi_over_critical:.9e} "
                f"LAMBDA0="
                f"{lambda0:+.12e} "
                f"TACHYON="
                f"{audit['robust_tachyon']}"
            )

            print(
                f"ROOT_GATE_REQUIREMENT branch={branch} "
                f"DELTA_M2_OVER_MPHI2="
                f"{delta_m2_over_mphi2:.12e} "
                f"M_EFF_OVER_MPHI="
                f"{m_eff_over_mphi:.12e} "
                f"EFOLD_TIME_S="
                f"{e_fold_s:.12e}"
            )

        print(
            "\n=== STAGE E: DECISION ==="
        )

        low_root = next(
            (
                row
                for row in roots
                if row[
                    "branch"
                ] == "low"
            ),
            None,
        )

        high_root = next(
            (
                row
                for row in roots
                if row[
                    "branch"
                ] == "high"
            ),
            None,
        )

        branch_reconstruction_pass = bool(
            low_root is not None
            and
            high_root is not None
        )

        stable_roots = [
            row
            for row in roots
            if bool(
                row[
                    "source_viable"
                ]
            )
        ]

        stable_non_tachyonic = [
            row
            for row in stable_roots
            if not bool(
                row[
                    "robust_tachyon"
                ]
            )
        ]

        stable_tachyonic = [
            row
            for row in stable_roots
            if bool(
                row[
                    "robust_tachyon"
                ]
            )
        ]

        high_branch_unstable = bool(
            high_root is not None
            and
            not bool(
                high_root[
                    "source_slope_stable"
                ]
            )
        )

        if not branch_reconstruction_pass:
            classification = (
                "YELLOW_D1R_TWO_BRANCH_"
                "RECONSTRUCTION_INCOMPLETE"
            )

            next_action = (
                "REFINE_ONLY_FAILED_BRANCH_"
                "CONTINUATION"
            )

        elif stable_non_tachyonic:
            classification = (
                "YELLOW_D1R_STABLE_SAME_Q_"
                "OFF_BRANCH_SURVIVES_SCALAR_HESSIAN"
            )

            next_action = (
                "031D1S_SWITCHING_BARRIER_"
                "AND_CONTROL_PATH"
            )

        elif (
            len(stable_roots) >= 1
            and
            len(stable_tachyonic)
            == len(stable_roots)
        ):
            classification = (
                "RED_D1R_GATE_FREE_OFFSTATE_"
                "TACHYONIC_ON_ALL_SOURCE_STABLE_"
                "SAME_Q_BRANCHES"
            )

            next_action = (
                "031D2_MINIMUM_AUXILIARY_GATE_"
                "MASS_SHIFT_AND_CONTROL_ENERGY"
            )

        else:
            classification = (
                "YELLOW_D1R_OFFSTATE_"
                "SOURCE_STABILITY_UNRESOLVED"
            )

            next_action = (
                "REFINE_SOURCE_BRANCH_STABILITY_ONLY"
            )

        gate_required = bool(
            classification.startswith(
                "RED_D1R"
            )
        )

        if stable_tachyonic:
            best_gate_target = min(
                stable_tachyonic,
                key=lambda row:
                    float(
                        row[
                            "critical_delta_m2_over_mphi2"
                        ]
                    ),
            )
        else:
            best_gate_target = None

        print(
            f"TWO_BRANCH_RECONSTRUCTION_PASS="
            f"{branch_reconstruction_pass}"
        )

        print(
            f"SAME_Q_ROOT_COUNT="
            f"{len(roots)}"
        )

        print(
            f"SOURCE_STABLE_ROOT_COUNT="
            f"{len(stable_roots)}"
        )

        print(
            f"SOURCE_STABLE_NON_TACHYONIC_COUNT="
            f"{len(stable_non_tachyonic)}"
        )

        print(
            f"HIGH_OMEGA_BRANCH_SOURCE_UNSTABLE="
            f"{high_branch_unstable}"
        )

        print(
            f"AUXILIARY_GATE_REQUIRED="
            f"{gate_required}"
        )

        if best_gate_target is not None:
            print(
                "MINIMUM_STABLE_BRANCH_"
                "DELTA_M2_OVER_MPHI2="
                f"{best_gate_target['critical_delta_m2_over_mphi2']:.15e}"
            )

            print(
                "MINIMUM_STABLE_BRANCH_"
                "M_EFF_OVER_MPHI="
                f"{best_gate_target['critical_m_eff_over_mphi']:.15e}"
            )

            print(
                "UNCONTROLLED_OFFSTATE_"
                "EFOLD_TIME_S="
                f"{best_gate_target['e_fold_time_s']:.15e}"
            )

        print(
            "031D1R_CLASSIFICATION="
            f"{classification}"
        )

        print(
            "NEXT="
            f"{next_action}"
        )

        print(
            "GATE_CONTROL_ENERGY_CLOSED=NO"
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

        summary = {
            "classification":
                classification,
            "next":
                next_action,
            "target_I_Q":
                target_q,
            "omega_on":
                omega_on,
            "epsilon":
                epsilon,
            "chi":
                chi,
            "two_branch_reconstruction_pass":
                branch_reconstruction_pass,
            "high_omega_branch_source_unstable":
                high_branch_unstable,
            "roots":
                roots,
            "source_stable_root_count":
                len(stable_roots),
            "source_stable_non_tachyonic_count":
                len(
                    stable_non_tachyonic
                ),
            "auxiliary_gate_required":
                gate_required,
            "best_gate_target":
                best_gate_target,
            "claim_limits": [
                (
                    "This run repairs numerical branch "
                    "tracking in the gate-free u=0 off-state test."
                ),
                (
                    "Only nodeless unscalarized Q-ball "
                    "branches are accepted as candidate source states."
                ),
                (
                    "A RED result closes only the gate-free "
                    "off state of this current single-field Z2 model."
                ),
                (
                    "Auxiliary gate/control energy is not "
                    "included and remains the next gate."
                ),
                (
                    "Full physical-metric backreaction, "
                    "nonlinear stability, EFT naturalness, "
                    "and empirical closure remain open."
                ),
            ],
        }

        OUT_JSON.write_text(
            json.dumps(
                to_builtin(summary),
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )

        branch_fields = sorted(
            {
                key
                for row in all_branch_rows
                for key in row.keys()
            }
        )

        with OUT_BRANCH_CSV.open(
            "w",
            newline="",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=branch_fields,
            )

            writer.writeheader()
            writer.writerows(
                all_branch_rows
            )

        if all_hessian_rows:
            hessian_fields = sorted(
                {
                    key
                    for row in all_hessian_rows
                    for key in row.keys()
                }
            )

            with OUT_HESSIAN_CSV.open(
                "w",
                newline="",
            ) as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=hessian_fields,
                )

                writer.writeheader()
                writer.writerows(
                    all_hessian_rows
                )

        else:
            OUT_HESSIAN_CSV.write_text(
                "branch,omega\n"
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}"
        )

        print(
            f"BRANCH_SCAN_CSV={OUT_BRANCH_CSV}"
        )

        print(
            f"HESSIAN_SCAN_CSV={OUT_HESSIAN_CSV}"
        )

    finally:
        qmod.X_MATCH = original_x_match_q
        d1.X_MATCH_SOURCE = (
            original_x_match_d1
        )


if __name__ == "__main__":
    main()
