"""
031D1-R2 — decisive low-branch fixed-charge off-state Hessian gate

The previous branch-tracked run established a smooth, nodeless,
same-charge crossing near Omega ~= 0.49396.

This run deliberately ignores the unresolved high-Omega anomaly and asks
the cheapest decisive question first:

    Is the clean low-Omega same-Q off state scalar-linearly stable?

A robust negative Dirichlet finite-box eigenvalue is sufficient to prove
a negative direction in the infinite-domain quadratic form.

A nonnegative converged result would preserve the gate-free off-state route.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

QBALL_SOURCE = (
    SIM / "031b2a_global_qball_activated_scalar_control.py"
)

D1_SOURCE = (
    SIM / "031d1_qball_self_activation_offstate_fixed_charge_gate.py"
)

R1_SOURCE = (
    SIM / "031d1r_branch_tracked_offstate_fixed_charge_gate.py"
)

ROBUST_SUMMARY = (
    DATA / "031c96_operating_margin_robustness_summary.json"
)

D96_SUMMARY = (
    DATA / "031b2d96_combined_coupled_linear_goldstone_summary.json"
)

OUT_JSON = (
    DATA / "031d1r2_lowbranch_offstate_hessian_summary.json"
)

OUT_BRANCH_CSV = (
    DATA / "031d1r2_lowbranch_tracking.csv"
)

OUT_HESSIAN_CSV = (
    DATA / "031d1r2_lowbranch_hessian_scan.csv"
)


X_MATCH = 80.0

OMEGA_ON = 0.34

LOW_SEED = 0.495897436

LOW_MIN = 0.4910
LOW_MAX = 0.4990

CONTINUATION_STEP = 0.001

ROOT_Q_REL_TOL = 2.0e-8

EPS_R_VALUES = (
    1.2,
    3.0,
    5.0,
    8.0,
)

H_VALUES = (
    0.50,
    0.25,
    0.125,
)

NEGATIVE_TOL = 1.0e-6

GRID_CONVERGENCE_TOL = 0.02
DOMAIN_CONVERGENCE_TOL = 0.02

HBAR_GEV_S = 6.582119569e-25


def require(path: Path):
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
            str(k): builtin(v)
            for k, v in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            builtin(v)
            for v in value
        ]

    return value


def find_row(rows, eps_r, h_target):
    matches = [
        row
        for row in rows
        if abs(
            float(row["epsilon_rmax"])
            -eps_r
        ) < 1.0e-12
        and abs(
            float(row["h_target"])
            -h_target
        ) < 1.0e-12
    ]

    if len(matches) != 1:
        raise RuntimeError(
            f"Missing Hessian row epsR={eps_r}, h={h_target}"
        )

    return matches[0]


def main():
    print(
        "=== 031D1-R2 LOW-BRANCH DECISIVE OFF-STATE HESSIAN ==="
    )

    print(
        "QUESTION="
        "IS_CLEAN_SAME_Q_LOW_OMEGA_OFF_STATE_SCALAR_LINEarly_STABLE"
    )

    print(
        "HIGH_OMEGA_BRANCH_REQUIRED_FOR_THIS_GATE=NO"
    )

    print(
        "AUXILIARY_GATE_FIELD_INCLUDED=NO"
    )

    print(
        "CONTROL_ENERGY_INCLUDED=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        QBALL_SOURCE,
        D1_SOURCE,
        R1_SOURCE,
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
            "D96 intrinsic source stability is not GREEN"
        )

    qmod = load_module(
        "qball031d1r2",
        QBALL_SOURCE,
    )

    d1 = load_module(
        "d1helpers031d1r2",
        D1_SOURCE,
    )

    r1 = load_module(
        "r1helpers031d1r2",
        R1_SOURCE,
    )

    candidate = robust["candidate"]

    epsilon = float(
        candidate["epsilon"]
    )

    chi = float(
        candidate["chi"]
    )

    m_x_gev = float(
        candidate["m_x_gev_derived"]
    )

    original_q_xmatch = float(
        qmod.X_MATCH
    )

    original_d1_xmatch = float(
        d1.X_MATCH_SOURCE
    )

    original_r1_xmatch = float(
        r1.X_MATCH
    )

    original_step = float(
        r1.CONTINUATION_STEP
    )

    qmod.X_MATCH = X_MATCH
    d1.X_MATCH_SOURCE = X_MATCH
    r1.X_MATCH = X_MATCH
    r1.CONTINUATION_STEP = CONTINUATION_STEP

    try:
        print(
            "\n=== STAGE A: ON-STATE TARGET CHARGE ==="
        )

        seed_on = qmod.solve_uncoupled_qball(
            OMEGA_ON
        )

        if seed_on is None:
            raise RuntimeError(
                "Failed to reconstruct on-state seed"
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
                "Failed to reconstruct scalarized on state"
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

        print(
            f"TARGET_I_Q={target_q:.15e}"
        )

        print(
            f"ON_E_OVER_QMX="
            f"{on_metrics['E_over_QmX']:.15e}"
        )

        print(
            "\n=== STAGE B: CLEAN LOW-BRANCH CONTINUATION ==="
        )

        branch_records = r1.walk_branch(
            qmod,
            d1,
            "low_decisive",
            LOW_SEED,
            LOW_MIN,
            LOW_MAX,
            target_q,
        )

        brackets = r1.locate_bracket(
            branch_records
        )

        print(
            f"LOW_BRANCH_BRACKET_COUNT="
            f"{len(brackets)}"
        )

        if len(brackets) != 1:
            raise RuntimeError(
                "Expected exactly one low-branch same-Q crossing"
            )

        omega_off, off_solution, root_record = (
            r1.refine_charge_root(
                qmod,
                d1,
                "low_decisive",
                brackets[0][0],
                brackets[0][1],
                target_q,
            )
        )

        if r1.count_nodes(
            off_solution
        ) != 0:
            raise RuntimeError(
                "Refined low branch is not nodeless"
            )

        print(
            "\n=== STAGE C: SAME-Q ROOT SOURCE DIAGNOSTICS ==="
        )

        off_metrics = d1.uncoupled_integrals(
            off_solution,
            omega_off,
        )

        dq_domega = r1.branch_slope(
            qmod,
            d1,
            omega_off,
            off_solution,
        )

        q_match_rel = float(
            root_record[
                "Q_rel_residual"
            ]
        )

        e_over_q = float(
            off_metrics[
                "E_over_QmX"
            ]
        )

        source_slope_stable = bool(
            math.isfinite(dq_domega)
            and dq_domega < 0.0
        )

        qball_bound = bool(
            e_over_q < 1.0
        )

        source_viable = bool(
            q_match_rel
            <= ROOT_Q_REL_TOL
            and
            source_slope_stable
            and
            qball_bound
        )

        chi_critical = (
            qmod.scalarization_critical_chi(
                off_solution,
                epsilon,
            )
        )

        if (
            chi_critical is not None
            and
            chi_critical > 0.0
        ):
            chi_over_critical = (
                chi
                / chi_critical
            )
        else:
            chi_over_critical = math.nan

        print(
            f"OMEGA_OFF={omega_off:.15e}"
        )

        print(
            f"Q_MATCH_RELERR={q_match_rel:.15e}"
        )

        print(
            f"OFF_E_OVER_QMX={e_over_q:.15e}"
        )

        print(
            f"DQ_DOMEGA={dq_domega:+.15e}"
        )

        print(
            f"SOURCE_SLOPE_STABLE="
            f"{source_slope_stable}"
        )

        print(
            f"QBALL_BOUND_PASS={qball_bound}"
        )

        print(
            f"SOURCE_VIABLE={source_viable}"
        )

        print(
            f"CHI_CRITICAL="
            f"{chi_critical if chi_critical is not None else math.nan:.15e}"
        )

        print(
            f"CHI_OVER_CRITICAL="
            f"{chi_over_critical:.15e}"
        )

        print(
            "\n=== STAGE D: OFF-STATE HESSIAN DOMAIN/GRID CONVERGENCE ==="
        )

        hessian_rows = []

        for eps_r in EPS_R_VALUES:
            for h_target in H_VALUES:
                row = d1.off_hessian_row(
                    off_solution,
                    omega_off,
                    epsilon,
                    chi,
                    eps_r,
                    h_target,
                )

                hessian_rows.append(
                    row
                )

                print(
                    f"HESSIAN "
                    f"EPS_R={eps_r:.3f} "
                    f"RMAX={row['rmax']:.6f} "
                    f"H={row['h']:.9f} "
                    f"LAMBDA0="
                    f"{row['lambda0']:+.15e} "
                    f"LAMBDA1="
                    f"{row['lambda1']:+.15e} "
                    f"GROWTH="
                    f"{row['growth_dimensionless']:.15e}"
                )

        finest = find_row(
            hessian_rows,
            8.0,
            0.125,
        )

        grid_compare = find_row(
            hessian_rows,
            8.0,
            0.25,
        )

        domain_compare = find_row(
            hessian_rows,
            5.0,
            0.125,
        )

        box5_fine = find_row(
            hessian_rows,
            5.0,
            0.125,
        )

        box8_fine = finest

        lambda0 = float(
            finest["lambda0"]
        )

        grid_rel = d1.relerr(
            lambda0,
            float(
                grid_compare[
                    "lambda0"
                ]
            ),
        )

        domain_rel = d1.relerr(
            lambda0,
            float(
                domain_compare[
                    "lambda0"
                ]
            ),
        )

        finite_box_negative_proof = bool(
            float(
                box5_fine[
                    "lambda0"
                ]
            )
            < -NEGATIVE_TOL
            and
            float(
                box8_fine[
                    "lambda0"
                ]
            )
            < -NEGATIVE_TOL
        )

        quantitative_convergence = bool(
            grid_rel
            <= GRID_CONVERGENCE_TOL
            and
            domain_rel
            <= DOMAIN_CONVERGENCE_TOL
        )

        robust_tachyon = bool(
            finite_box_negative_proof
            and
            quantitative_convergence
        )

        nonnegative_survivor = bool(
            lambda0
            >= -NEGATIVE_TOL
            and
            quantitative_convergence
        )

        growth_dimensionless = (
            math.sqrt(-lambda0)
            if lambda0 < 0.0
            else 0.0
        )

        growth_rate_s = (
            growth_dimensionless
            * m_x_gev
            / HBAR_GEV_S
        )

        e_fold_s = (
            1.0 / growth_rate_s
            if growth_rate_s > 0.0
            else math.inf
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

        critical_m_eff_over_mphi = (
            math.sqrt(
                1.0
                +delta_m2_over_mphi2
            )
        )

        print(
            "\n=== STAGE E: DECISION ==="
        )

        print(
            f"FINEST_LAMBDA0="
            f"{lambda0:+.15e}"
        )

        print(
            f"HESSIAN_GRID_REL_DIFF="
            f"{grid_rel:.15e}"
        )

        print(
            f"HESSIAN_DOMAIN_REL_DIFF="
            f"{domain_rel:.15e}"
        )

        print(
            f"FINITE_BOX_NEGATIVE_DIRECTION_PROOF="
            f"{finite_box_negative_proof}"
        )

        print(
            f"QUANTITATIVE_HESSIAN_CONVERGENCE="
            f"{quantitative_convergence}"
        )

        print(
            f"LOW_BRANCH_ROBUST_TACHYON="
            f"{robust_tachyon}"
        )

        print(
            f"LOW_BRANCH_NONNEGATIVE_SURVIVOR="
            f"{nonnegative_survivor}"
        )

        print(
            f"UNCONTROLLED_GROWTH_EFOLD_S="
            f"{e_fold_s:.15e}"
        )

        print(
            f"CRITICAL_POSITIVE_DELTA_M2_HAT="
            f"{delta_m2_hat:.15e}"
        )

        print(
            f"CRITICAL_DELTA_M2_OVER_MPHI2="
            f"{delta_m2_over_mphi2:.15e}"
        )

        print(
            f"CRITICAL_M_EFF_OVER_MPHI="
            f"{critical_m_eff_over_mphi:.15e}"
        )

        if not source_viable:
            classification = (
                "YELLOW_D1R2_LOW_BRANCH_"
                "SOURCE_DIAGNOSTIC_FAILED"
            )

            next_action = (
                "REFINE_LOW_BRANCH_SOURCE_STABILITY_ONLY"
            )

        elif robust_tachyon:
            classification = (
                "RED_D1R2_LOW_OMEGA_SAME_Q_"
                "OFF_BRANCH_TACHYONIC"
            )

            next_action = (
                "031D1H_HIGH_OMEGA_BRANCH_IDENTITY_"
                "AND_NODE_TOPOLOGY_AUDIT_BEFORE_"
                "CLOSING_ALL_GATE_FREE_OFF_STATES"
            )

        elif nonnegative_survivor:
            classification = (
                "GREEN_D1R2_LOW_OMEGA_SAME_Q_"
                "OFF_BRANCH_SCALAR_LINEARLY_STABLE"
            )

            next_action = (
                "031D_SWITCHING_BARRIER_CONTROL_PATH_"
                "AND_RECIPROCITY"
            )

        else:
            classification = (
                "YELLOW_D1R2_LOW_BRANCH_"
                "HESSIAN_NOT_YET_CONVERGED"
            )

            next_action = (
                "REFINE_ONLY_HESSIAN_GRID_DOMAIN"
            )

        print(
            f"031D1R2_CLASSIFICATION="
            f"{classification}"
        )

        print(
            f"NEXT={next_action}"
        )

        print(
            "GATE_FREE_OFFSTATE_ROUTE_CLOSED=NO"
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

        summary = {
            "classification":
                classification,
            "next":
                next_action,
            "target_I_Q":
                target_q,
            "omega_off":
                omega_off,
            "Q_match_relerr":
                q_match_rel,
            "E_over_QmX":
                e_over_q,
            "dq_domega":
                dq_domega,
            "source_slope_stable":
                source_slope_stable,
            "qball_bound_pass":
                qball_bound,
            "source_viable":
                source_viable,
            "chi":
                chi,
            "chi_critical":
                chi_critical,
            "chi_over_critical":
                chi_over_critical,
            "finest_lambda0":
                lambda0,
            "hessian_grid_rel_difference":
                grid_rel,
            "hessian_domain_rel_difference":
                domain_rel,
            "finite_box_negative_direction_proof":
                finite_box_negative_proof,
            "quantitative_hessian_convergence":
                quantitative_convergence,
            "low_branch_robust_tachyon":
                robust_tachyon,
            "low_branch_nonnegative_survivor":
                nonnegative_survivor,
            "growth_dimensionless":
                growth_dimensionless,
            "uncontrolled_e_fold_time_s":
                e_fold_s,
            "critical_positive_delta_m2_hat":
                delta_m2_hat,
            "critical_delta_m2_over_mphi2":
                delta_m2_over_mphi2,
            "critical_m_eff_over_mphi":
                critical_m_eff_over_mphi,
            "high_omega_branch_status":
                "UNRESOLVED_NOT_REQUIRED_UNLESS_LOW_BRANCH_TACHYONIC",
            "claim_limits": [
                (
                    "This run decides only the clean low-Omega "
                    "same-charge unscalarized branch."
                ),
                (
                    "A negative low-branch result does not by itself "
                    "close all possible gate-free off branches."
                ),
                (
                    "A finite-box negative Dirichlet eigenvalue "
                    "provides a negative variational direction for "
                    "the infinite-domain operator."
                ),
                (
                    "Auxiliary gate/control energy and reciprocity "
                    "remain open."
                ),
                (
                    "Full physical-metric backreaction, nonlinear "
                    "stability, EFT naturalness, and empirical "
                    "closure remain open."
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

        branch_rows = [
            item[2]
            for item in branch_records
        ]

        branch_fields = sorted(
            {
                key
                for row in branch_rows
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
                branch_rows
            )

        hessian_fields = sorted(
            {
                key
                for row in hessian_rows
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
                hessian_rows
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}"
        )

        print(
            f"BRANCH_CSV={OUT_BRANCH_CSV}"
        )

        print(
            f"HESSIAN_CSV={OUT_HESSIAN_CSV}"
        )

    finally:
        qmod.X_MATCH = (
            original_q_xmatch
        )

        d1.X_MATCH_SOURCE = (
            original_d1_xmatch
        )

        r1.X_MATCH = (
            original_r1_xmatch
        )

        r1.CONTINUATION_STEP = (
            original_step
        )


if __name__ == "__main__":
    main()
