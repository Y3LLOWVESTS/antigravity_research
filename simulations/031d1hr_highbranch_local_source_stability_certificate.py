"""
031D1H-R — local high-Omega same-Q off-state source certificate

The global scaled continuation in 031D1H already established:

    * one continuous nodeless ground-state Q-ball family;
    * exactly two crossings of the target conserved charge;
    * exactly one Q(Omega) turning point;
    * a high-Omega crossing near Omega ~= 0.9999959.

The previous run failed only while attempting unnecessary ultra-tight
BVP root refinement.

This repair does NOT repeat the global scan.

It locally resolves the high-Omega bracket using ordinary continuation
and tests:

    1. node topology;
    2. sign of dQ/dOmega throughout the crossing neighborhood;
    3. E/(Q m_X) relative to the free-particle threshold;
    4. quadrature convergence of that small energy excess.

If the high branch has robust dQ/dOmega > 0, it fails the Q-ball
source-stability criterion.

Combined with the independently certified low-branch scalar tachyon,
that closes the current gate-free, nodeless, same-Noether-charge
u=0 off-state route.

It does NOT close auxiliary gate architectures.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import re
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"
LOGS = ROOT / "results" / "logs"

H_SOURCE = (
    SIM
    / "031d1h_highomega_scaled_branch_topology_gate.py"
)

LOW_SUMMARY = (
    DATA
    / "031d1r2_lowbranch_offstate_hessian_summary.json"
)

ROBUST_SUMMARY = (
    DATA
    / "031c96_operating_margin_robustness_summary.json"
)

OUT_JSON = (
    DATA
    / "031d1hr_highbranch_certificate_summary.json"
)

OUT_CSV = (
    DATA
    / "031d1hr_highbranch_local_scan.csv"
)


TARGET_Q = 6594.219892350219

MU_MIN = 0.00250
MU_MAX = 0.00315

N_LOCAL = 41

QUAD_POINTS = (
    20_000,
    40_000,
    80_000,
)

SLOPE_SIGN_MARGIN = 1.0e6

ENERGY_EXCESS_ABS_FLOOR = 1.0e-7
ENERGY_NUMERICAL_MARGIN_FACTOR = 20.0


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

    if (
        spec is None
        or spec.loader is None
    ):
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


def latest_global_log() -> Path:
    candidates = sorted(
        LOGS.glob(
            "031d1h_highomega_branch_*.log"
        ),
        key=lambda p:
            p.stat().st_mtime,
    )

    if not candidates:
        raise RuntimeError(
            "No completed 031D1H global log found"
        )

    return candidates[-1]


def parse_global_topology(path: Path):
    text = path.read_text()

    crossing_match = re.search(
        r"GLOBAL_TARGET_CROSSING_COUNT=(\d+)",
        text,
    )

    reversal_match = re.search(
        r"GLOBAL_Q_TREND_REVERSAL_COUNT=(\d+)",
        text,
    )

    qmin_match = re.search(
        r"GLOBAL_Q_MIN=([0-9.eE+-]+)",
        text,
    )

    qmin_omega_match = re.search(
        r"GLOBAL_Q_MIN_OMEGA=([0-9.eE+-]+)",
        text,
    )

    if not all(
        (
            crossing_match,
            reversal_match,
            qmin_match,
            qmin_omega_match,
        )
    ):
        raise RuntimeError(
            "Global 031D1H topology ledger incomplete"
        )

    return {
        "crossing_count":
            int(
                crossing_match.group(1)
            ),
        "reversal_count":
            int(
                reversal_match.group(1)
            ),
        "Q_min":
            float(
                qmin_match.group(1)
            ),
        "Q_min_omega":
            float(
                qmin_omega_match.group(1)
            ),
    }


def main() -> None:
    print(
        "=== 031D1H-R HIGH-OMEGA LOCAL SOURCE CERTIFICATE ==="
    )

    print(
        "GLOBAL_SCAN_REPEATED=NO"
    )

    print(
        "EXACT_ROOT_BVP_REQUIRED=NO"
    )

    print(
        "HIGH_BRANCH_TEST="
        "LOCAL_MONOTONE_BRACKET_PLUS_SOURCE_STABILITY"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        H_SOURCE,
        LOW_SUMMARY,
        ROBUST_SUMMARY,
    ):
        require(path)

    low = json.loads(
        LOW_SUMMARY.read_text()
    )

    robust = json.loads(
        ROBUST_SUMMARY.read_text()
    )

    if not bool(
        low.get(
            "low_branch_robust_tachyon",
            False,
        )
    ):
        raise RuntimeError(
            "Low off branch is not certified tachyonic"
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

    global_log = latest_global_log()

    topology = parse_global_topology(
        global_log
    )

    topology_pass = bool(
        topology[
            "crossing_count"
        ] == 2
        and
        topology[
            "reversal_count"
        ] == 1
    )

    print(
        f"GLOBAL_LOG={global_log}"
    )

    print(
        f"GLOBAL_TARGET_CROSSING_COUNT="
        f"{topology['crossing_count']}"
    )

    print(
        f"GLOBAL_Q_TREND_REVERSAL_COUNT="
        f"{topology['reversal_count']}"
    )

    print(
        f"GLOBAL_Q_MIN="
        f"{topology['Q_min']:.15e}"
    )

    print(
        f"GLOBAL_Q_MIN_OMEGA="
        f"{topology['Q_min_omega']:.15e}"
    )

    print(
        f"GLOBAL_TOPOLOGY_PASS="
        f"{topology_pass}"
    )

    h = load_module(
        "d1h_helpers_repair",
        H_SOURCE,
    )

    print(
        "\n=== STAGE A: THICK-WALL SEED ==="
    )

    solution = (
        h.solve_thick_wall_limit()
    )

    print(
        f"LIMIT_F0="
        f"{float(solution.sol(h.RHO0)[0]):.15e}"
    )

    print(
        "\n=== STAGE B: LOCAL HIGH-BRANCH CONTINUATION ==="
    )

    mu_values = np.linspace(
        MU_MIN,
        MU_MAX,
        N_LOCAL,
    )

    rows = []
    solutions = []

    previous = solution

    # First move from the exact thick-wall limit to MU_MIN
    # in sufficiently small continuation steps.
    approach = np.geomspace(
        1.0e-4,
        MU_MIN,
        35,
    )

    for mu in approach:
        candidate = h.solve_scaled(
            float(mu),
            previous,
            tolerance=8.0e-7,
        )

        if candidate is None:
            raise RuntimeError(
                f"Approach continuation failed at mu={mu}"
            )

        previous = candidate

    for mu in mu_values:
        candidate = h.solve_scaled(
            float(mu),
            previous,
            tolerance=8.0e-7,
        )

        if candidate is None:
            raise RuntimeError(
                f"Local continuation failed at mu={mu}"
            )

        metrics = h.branch_metrics(
            candidate,
            float(mu),
            points=20_000,
        )

        if metrics[
            "nodes"
        ] != 0:
            raise RuntimeError(
                f"Nodeful state encountered at mu={mu}"
            )

        rows.append(
            {
                **metrics,
                "Q_residual":
                    float(
                        metrics["I_Q"]
                        -TARGET_Q
                    ),
            }
        )

        solutions.append(
            candidate
        )

        previous = candidate

        print(
            f"LOCAL "
            f"MU={mu:.12e} "
            f"OMEGA={metrics['omega']:.15e} "
            f"I_Q={metrics['I_Q']:.12e} "
            f"Q_RES="
            f"{metrics['I_Q']-TARGET_Q:+.12e} "
            f"E_OVER_Q="
            f"{metrics['E_over_QmX']:.12e} "
            f"NODES={metrics['nodes']}"
        )

    crossing_indices = []

    for index in range(
        len(rows) - 1
    ):
        left = rows[index][
            "Q_residual"
        ]

        right = rows[
            index + 1
        ][
            "Q_residual"
        ]

        if left * right < 0.0:
            crossing_indices.append(
                index
            )

    print(
        f"LOCAL_CROSSING_COUNT="
        f"{len(crossing_indices)}"
    )

    if len(
        crossing_indices
    ) != 1:
        raise RuntimeError(
            "Expected exactly one local high-branch crossing"
        )

    crossing_index = (
        crossing_indices[0]
    )

    left = rows[
        crossing_index
    ]

    right = rows[
        crossing_index + 1
    ]

    mu_left = float(
        left["mu"]
    )

    mu_right = float(
        right["mu"]
    )

    q_left = float(
        left["I_Q"]
    )

    q_right = float(
        right["I_Q"]
    )

    mu_interp = (
        mu_left
        +(
            TARGET_Q
            -q_left
        )
        *(
            mu_right
            -mu_left
        )
        /(
            q_right
            -q_left
        )
    )

    omega_interp = math.sqrt(
        1.0
        -mu_interp
        *mu_interp
    )

    omega_left = float(
        left["omega"]
    )

    omega_right = float(
        right["omega"]
    )

    secant_dq_domega = (
        q_right
        -q_left
    ) / (
        omega_right
        -omega_left
    )

    print(
        "\n=== STAGE C: HIGH-ROOT BRACKET ==="
    )

    print(
        f"HIGH_ROOT_MU_BRACKET="
        f"[{mu_left:.15e},{mu_right:.15e}]"
    )

    print(
        f"HIGH_ROOT_OMEGA_BRACKET="
        f"[{min(omega_left,omega_right):.15e},"
        f"{max(omega_left,omega_right):.15e}]"
    )

    print(
        f"HIGH_ROOT_MU_INTERPOLATED="
        f"{mu_interp:.15e}"
    )

    print(
        f"HIGH_ROOT_OMEGA_INTERPOLATED="
        f"{omega_interp:.15e}"
    )

    print(
        f"HIGH_ROOT_SECANT_DQ_DOMEGA="
        f"{secant_dq_domega:+.15e}"
    )

    print(
        "\n=== STAGE D: LOCAL SLOPE SIGN AUDIT ==="
    )

    slope_rows = []

    guard_lo = max(
        crossing_index - 3,
        0,
    )

    guard_hi = min(
        crossing_index + 4,
        len(rows) - 1,
    )

    for index in range(
        guard_lo,
        guard_hi
    ):
        a = rows[index]
        b = rows[index + 1]

        slope = (
            float(
                b["I_Q"]
            )
            -float(
                a["I_Q"]
            )
        ) / (
            float(
                b["omega"]
            )
            -float(
                a["omega"]
            )
        )

        slope_rows.append(
            slope
        )

        print(
            f"LOCAL_SLOPE "
            f"I={index} "
            f"DQ_DOMEGA="
            f"{slope:+.15e}"
        )

    minimum_local_slope = min(
        slope_rows
    )

    slope_fatal = bool(
        minimum_local_slope
        > SLOPE_SIGN_MARGIN
    )

    print(
        f"MIN_LOCAL_DQ_DOMEGA="
        f"{minimum_local_slope:+.15e}"
    )

    print(
        f"HIGH_BRANCH_VK_SOURCE_UNSTABLE="
        f"{slope_fatal}"
    )

    print(
        "\n=== STAGE E: E/(Q mX) NUMERICAL MARGIN ==="
    )

    energetic_rows = []

    for index in (
        crossing_index,
        crossing_index + 1,
    ):
        mu = float(
            rows[index]["mu"]
        )

        solution = solutions[
            index
        ]

        values = []

        for points in QUAD_POINTS:
            metrics = h.branch_metrics(
                solution,
                mu,
                points=points,
            )

            values.append(
                float(
                    metrics[
                        "E_over_QmX"
                    ]
                )
            )

            print(
                f"ENERGY_QUAD "
                f"MU={mu:.15e} "
                f"N={points} "
                f"E_OVER_Q="
                f"{metrics['E_over_QmX']:.15e}"
            )

        spread = (
            max(values)
            -min(values)
        )

        excess = (
            min(values)
            -1.0
        )

        energetic_rows.append(
            {
                "mu":
                    mu,
                "values":
                    values,
                "spread":
                    spread,
                "minimum_excess":
                    excess,
            }
        )

        print(
            f"ENERGY_MARGIN "
            f"MU={mu:.15e} "
            f"MIN_EXCESS="
            f"{excess:+.15e} "
            f"QUAD_SPREAD="
            f"{spread:.15e}"
        )

    minimum_energy_excess = min(
        row[
            "minimum_excess"
        ]
        for row in energetic_rows
    )

    maximum_quad_spread = max(
        row["spread"]
        for row in energetic_rows
    )

    energetic_unbound = bool(
        minimum_energy_excess
        > ENERGY_EXCESS_ABS_FLOOR
        and
        minimum_energy_excess
        >
        ENERGY_NUMERICAL_MARGIN_FACTOR
        *maximum_quad_spread
    )

    print(
        f"MIN_HIGH_BRANCH_E_OVER_Q_EXCESS="
        f"{minimum_energy_excess:+.15e}"
    )

    print(
        f"MAX_E_OVER_Q_QUADRATURE_SPREAD="
        f"{maximum_quad_spread:.15e}"
    )

    print(
        f"HIGH_BRANCH_ENERGETICALLY_UNBOUND="
        f"{energetic_unbound}"
    )

    print(
        "\n=== STAGE F: FINAL 031D1 DECISION ==="
    )

    low_tachyon = bool(
        low[
            "low_branch_robust_tachyon"
        ]
    )

    high_source_fatal = bool(
        slope_fatal
    )

    gate_free_closed = bool(
        topology_pass
        and
        low_tachyon
        and
        high_source_fatal
    )

    if gate_free_closed:
        classification = (
            "RED_D1HR_GATE_FREE_SAME_Q_OFFSTATE_ROUTE_CLOSED_"
            "LOW_BRANCH_SCALAR_TACHYON_"
            "HIGH_BRANCH_QBALL_SOURCE_UNSTABLE"
        )

        next_action = (
            "031D2_MINIMUM_AUXILIARY_GATE_MASS_SHIFT_"
            "CONTROL_ENERGY_RECIPROCITY_AND_SWITCHING_COST"
        )

    elif not topology_pass:
        classification = (
            "YELLOW_D1HR_GLOBAL_TOPOLOGY_NOT_CERTIFIED"
        )

        next_action = (
            "REPAIR_ONLY_GLOBAL_TOPOLOGY_PROVENANCE"
        )

    elif not slope_fatal:
        classification = (
            "YELLOW_D1HR_HIGH_BRANCH_SOURCE_STABILITY_UNRESOLVED"
        )

        next_action = (
            "REFINE_ONLY_HIGH_BRANCH_LOCAL_SLOPE"
        )

    else:
        classification = (
            "YELLOW_D1HR_OFFSTATE_CLOSURE_INCOMPLETE"
        )

        next_action = (
            "INSPECT_D1HR_LEDGER"
        )

    print(
        f"LOW_BRANCH_ROBUST_SCALAR_TACHYON="
        f"{low_tachyon}"
    )

    print(
        f"HIGH_BRANCH_SOURCE_FATAL="
        f"{high_source_fatal}"
    )

    print(
        f"GATE_FREE_SAME_Q_OFFSTATE_ROUTE_CLOSED="
        f"{gate_free_closed}"
    )

    print(
        f"AUXILIARY_GATE_REQUIRED="
        f"{gate_free_closed}"
    )

    print(
        f"031D1HR_CLASSIFICATION="
        f"{classification}"
    )

    print(
        f"NEXT={next_action}"
    )

    print(
        "GATE_CONTROL_ENERGY_CLOSED=NO"
    )

    print(
        "RECIPROCITY_CLOSED=NO"
    )

    print(
        "SWITCHING_RESET_COST_CLOSED=NO"
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
        "global_log":
            str(global_log),
        "global_topology":
            topology,
        "global_topology_pass":
            topology_pass,
        "target_I_Q":
            TARGET_Q,
        "high_root": {
            "mu_bracket":
                [
                    mu_left,
                    mu_right,
                ],
            "omega_bracket":
                sorted(
                    [
                        omega_left,
                        omega_right,
                    ]
                ),
            "mu_interpolated":
                mu_interp,
            "omega_interpolated":
                omega_interp,
            "secant_dQ_domega":
                secant_dq_domega,
            "minimum_local_dQ_domega":
                minimum_local_slope,
            "source_slope_unstable":
                slope_fatal,
            "minimum_E_over_Q_excess":
                minimum_energy_excess,
            "maximum_quadrature_spread":
                maximum_quad_spread,
            "energetically_unbound":
                energetic_unbound,
        },
        "low_branch": {
            "omega":
                low["omega_off"],
            "lambda0":
                low["finest_lambda0"],
            "robust_scalar_tachyon":
                low_tachyon,
            "uncontrolled_e_fold_time_s":
                low[
                    "uncontrolled_e_fold_time_s"
                ],
            "critical_delta_m2_over_mphi2":
                low[
                    "critical_delta_m2_over_mphi2"
                ],
        },
        "gate_free_same_Q_offstate_route_closed":
            gate_free_closed,
        "auxiliary_gate_required":
            gate_free_closed,
        "claim_limits": [
            (
                "Closure applies to the current nodeless "
                "same-Noether-charge u=0 Q-ball ground-state family."
            ),
            (
                "The high branch is rejected by source stability; "
                "the tiny E/(QmX)>1 excess is recorded as an "
                "independent energetic diagnostic."
            ),
            (
                "Auxiliary gate architectures remain open."
            ),
            (
                "Gate/control stress-energy, reciprocity and "
                "switching/reset costs remain unpriced."
            ),
            (
                "The GREEN scalarized antigravity on-state is not "
                "falsified by this off-state result."
            ),
            (
                "Full metric backreaction, nonlinear stability, "
                "EFT/naturalness and empirical closure remain open."
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
        f"LOCAL_CSV={OUT_CSV}"
    )


if __name__ == "__main__":
    main()
