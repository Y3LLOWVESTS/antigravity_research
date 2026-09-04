"""
031C-83
=======

Targeted compact-Q-ball continuation toward the 82.750782-GJ target.

The previous 031B2-B0 result reached 102.988 GJ but the optimum sat at the
smallest tested epsilon:

    epsilon = m_phi / m_X = 0.01.

At fixed mediator range, decreasing epsilon increases m_X and shrinks the
physical X-source while leaving the gravitational scalar range fixed.

This can permit a larger payload-adjacent translation without relaxing either:

    X-source leakage <= 1e-4
    payload backreaction <= 1e-2.

This is a physically motivated boundary continuation of the SAME source
theory. No new operator, no new support sector, no relaxed gate.

If this fails to cross 83 GJ or reaches a clear minimum, the simple compact
global-Q-ball morphology is closed and 031C moves to a genuine anisotropic
Q-shell / multicomponent source.
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


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

QBALL_SOURCE = (
    SIM
    /
    "031b2a_global_qball_activated_scalar_control.py"
)

TRANSLATION_SOURCE = (
    SIM
    /
    "031b2b0_qball_payload_adjacent_translation_gate.py"
)

SUMMARY = (
    DATA
    /
    "031b2a_global_qball_activated_scalar_control_summary.json"
)

OUT_JSON = (
    DATA
    /
    "031c83_compact_qball_epsilon_continuation_summary.json"
)

OUT_CSV = (
    DATA
    /
    "031c83_compact_qball_epsilon_continuation_scan.csv"
)


EPSILONS = (
    0.0040,
    0.0050,
    0.00625,
    0.0075,
    0.00875,
    0.0100,
)

OMEGAS = (
    0.34,
    0.37,
    0.40,
    0.43,
)

CHI_FACTORS = (
    2.0,
    2.5,
    3.125,
    4.0,
    5.0,
)

SCALAR_DOMAIN_MU_R = 0.80

SOURCE_LEAK_LIMIT = 1.0e-4
PAYLOAD_OVERLAP_LIMIT = 1.0e-10
BACKREACTION_LIMIT = 1.0e-2

TARGET_REL_TOL = 2.0e-3


def require(path: Path):

    if not path.is_file():

        raise RuntimeError(
            f"Missing required file: {path}"
        )


def load_module(name, path):

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

    sys.modules[
        spec.name
    ] = module

    spec.loader.exec_module(
        module
    )

    return module


def to_builtin(value: Any):

    if isinstance(value, np.generic):

        return value.item()

    if isinstance(value, np.ndarray):

        return value.tolist()

    if isinstance(value, dict):

        return {
            str(k):
            to_builtin(v)
            for k, v
            in value.items()
        }

    if isinstance(value, (list, tuple)):

        return [
            to_builtin(v)
            for v
            in value
        ]

    return value


def main():

    print(
        "=== 031C-83 COMPACT Q-BALL "
        "EPSILON CONTINUATION ==="
    )

    print(
        "CLAIM_CLASS="
        "SAME_THEORY_PHYSICALLY_MOTIVATED_"
        "SOURCE_COMPACTNESS_CONTINUATION"
    )

    print(
        "NEW_OPERATOR=NO"
    )

    print(
        "SOURCE_LEAK_GATE_RELAXED=NO"
    )

    print(
        "BACKREACTION_GATE_RELAXED=NO"
    )

    require(
        QBALL_SOURCE
    )

    require(
        TRANSLATION_SOURCE
    )

    require(
        SUMMARY
    )

    qmod = load_module(
        "c83_qball",
        QBALL_SOURCE,
    )

    tmod = load_module(
        "c83_translation",
        TRANSLATION_SOURCE,
    )

    summary = json.loads(
        SUMMARY.read_text()
    )

    target = float(
        summary[
            "target_energy_J"
        ]
    )

    alpha_promoted = float(
        summary[
            "alpha_m_on_cap"
        ]
    )

    mediator_range = float(
        summary[
            "mediator_range_m"
        ]
    )

    print(
        f"TARGET_ENERGY_J="
        f"{target:.15e}"
    )

    print(
        f"PROMOTED_ALPHA_M="
        f"{alpha_promoted:.15e}"
    )

    print(
        f"MEDIATOR_RANGE_M="
        f"{mediator_range:.15e}"
    )

    rows = []

    for epsilon in EPSILONS:

        qmod.X_MATCH = (
            SCALAR_DOMAIN_MU_R
            /
            epsilon
        )

        print(
            f"\n=== EPSILON={epsilon:.9e} "
            f"X_MATCH={qmod.X_MATCH:.9e} ==="
        )

        for omega in OMEGAS:

            seed = qmod.solve_uncoupled_qball(
                omega
            )

            if seed is None:

                print(
                    f"SEED_FAIL "
                    f"EPS={epsilon:.9e} "
                    f"OMEGA={omega:.9e}"
                )

                continue

            chi_critical = (
                qmod.scalarization_critical_chi(
                    seed,
                    epsilon,
                )
            )

            if chi_critical is None:

                print(
                    f"THRESHOLD_FAIL "
                    f"EPS={epsilon:.9e} "
                    f"OMEGA={omega:.9e}"
                )

                continue

            for factor in CHI_FACTORS:

                chi = (
                    chi_critical
                    *
                    factor
                )

                source_row = {
                    "omega":
                    omega,

                    "epsilon":
                    epsilon,

                    "chi":
                    chi,

                    "chi_factor":
                    factor,

                    "E_inventory_J":
                    math.nan,
                }

                case = tmod.reconstruct(
                    qmod,
                    source_row,
                    mediator_range,
                )

                if case is None:

                    continue

                centered = qmod.evaluate_case(
                    case[
                        "solution"
                    ],
                    omega,
                    epsilon,
                    chi,
                    target,
                    alpha_promoted,
                    mediator_range,
                )

                if not centered.get(
                    "success",
                    False,
                ):

                    print(
                        f"CASE_FAIL "
                        f"EPS={epsilon:.9e} "
                        f"OMEGA={omega:.9e} "
                        f"FACTOR={factor:.9e} "
                        f"REASON="
                        f"{centered.get('reason', 'UNKNOWN')}"
                    )

                    continue

                if not centered.get(
                    "prefilter_pass",
                    False,
                ):

                    print(
                        f"PREFILTER_FAIL "
                        f"EPS={epsilon:.9e} "
                        f"OMEGA={omega:.9e} "
                        f"FACTOR={factor:.9e}"
                    )

                    continue

                max_shift = tmod.maximum_shift(
                    case,
                    SOURCE_LEAK_LIMIT,
                )

                leak, overlap = tmod.containment(
                    case,
                    max_shift,
                )

                promoted = tmod.force_solution(
                    qmod,
                    case,
                    max_shift,
                    alpha_promoted,
                )

                ceiling = (
                    tmod.alpha_ceiling_solution(
                        qmod,
                        case,
                        max_shift,
                        alpha_promoted,
                    )
                )

                if (
                    promoted is None
                    or
                    ceiling is None
                ):

                    continue

                pass83 = bool(
                    ceiling[
                        "E_inventory_J"
                    ]
                    <=
                    target
                    *
                    (
                        1.0
                        +
                        TARGET_REL_TOL
                    )
                    and
                    ceiling[
                        "backreaction"
                    ]
                    <=
                    BACKREACTION_LIMIT
                    *
                    (
                        1.0
                        +
                        1.0e-6
                    )
                    and
                    leak
                    <=
                    SOURCE_LEAK_LIMIT
                    *
                    (
                        1.0
                        +
                        1.0e-6
                    )
                    and
                    overlap
                    <=
                    PAYLOAD_OVERLAP_LIMIT
                )

                row = {
                    "epsilon":
                    epsilon,

                    "omega":
                    omega,

                    "chi_factor":
                    factor,

                    "chi":
                    chi,

                    "chi_critical":
                    chi_critical,

                    "X_MATCH":
                    qmod.X_MATCH,

                    "centered_E_J":
                    centered[
                        "E_inventory_J"
                    ],

                    "max_shift_m":
                    max_shift,

                    "source_leak":
                    leak,

                    "payload_overlap":
                    overlap,

                    "promoted_E_J":
                    promoted[
                        "E_inventory_J"
                    ],

                    "promoted_backreaction":
                    promoted[
                        "backreaction"
                    ],

                    "ceiling_alpha_m":
                    ceiling[
                        "alpha_m"
                    ],

                    "ceiling_E_J":
                    ceiling[
                        "E_inventory_J"
                    ],

                    "ceiling_backreaction":
                    ceiling[
                        "backreaction"
                    ],

                    "surface_min_mps2":
                    ceiling[
                        "surface_min_mps2"
                    ],

                    "a_cm_mps2":
                    ceiling[
                        "a_cm_mps2"
                    ],

                    "E_over_QmX":
                    centered[
                        "E_over_QmX"
                    ],

                    "scalar_hessian":
                    centered[
                        "scalar_fixed_x_hessian"
                    ],

                    "conservation_rel":
                    centered[
                        "conservation_rel"
                    ],

                    "DEC_pass":
                    centered[
                        "DEC_pass"
                    ],

                    "PASS83":
                    pass83,
                }

                rows.append(
                    row
                )

                print(
                    f"COMPACT_CASE "
                    f"EPS={epsilon:.9e} "
                    f"OMEGA={omega:.9e} "
                    f"FACTOR={factor:.9e} "
                    f"SHIFT={max_shift:.9e} "
                    f"LEAK={leak:.9e} "
                    f"ALPHA="
                    f"{ceiling['alpha_m']:.9e} "
                    f"E_J="
                    f"{ceiling['E_inventory_J']:.9e} "
                    f"BACK="
                    f"{ceiling['backreaction']:.9e} "
                    f"PASS83={pass83}"
                )

    if not rows:

        raise RuntimeError(
            "No valid compact-source continuation cases"
        )

    best = min(
        rows,
        key=lambda row:
        row[
            "ceiling_E_J"
        ],
    )

    survivors = [
        row
        for row
        in rows
        if row[
            "PASS83"
        ]
    ]

    print(
        "\n=== DECISION ==="
    )

    print(
        f"VALID_COMPACT_CASES="
        f"{len(rows)}"
    )

    print(
        f"COMPACT_83GJ_SURVIVORS="
        f"{len(survivors)}"
    )

    print(
        f"BEST_COMPACT_ENERGY_J="
        f"{best['ceiling_E_J']:.15e}"
    )

    print(
        f"BEST_COMPACT_ENERGY_OVER_TARGET="
        f"{best['ceiling_E_J'] / target:.15e}"
    )

    print(
        f"BEST_COMPACT_EPSILON="
        f"{best['epsilon']:.15e}"
    )

    print(
        f"BEST_COMPACT_OMEGA="
        f"{best['omega']:.15e}"
    )

    print(
        f"BEST_COMPACT_CHI_FACTOR="
        f"{best['chi_factor']:.15e}"
    )

    print(
        f"BEST_COMPACT_SHIFT_M="
        f"{best['max_shift_m']:.15e}"
    )

    print(
        f"BEST_COMPACT_ALPHA_M="
        f"{best['ceiling_alpha_m']:.15e}"
    )

    print(
        f"BEST_COMPACT_BACKREACTION="
        f"{best['ceiling_backreaction']:.15e}"
    )

    print(
        f"BEST_COMPACT_SOURCE_LEAK="
        f"{best['source_leak']:.15e}"
    )

    if survivors:

        classification = (
            "GREEN_SAME_THEORY_COMPACT_QBALL_"
            "RECOVERS_83GJ"
        )

        next_step = (
            "031C83_CERTIFY_WINNER_PLUS_"
            "031D_SELF_ACTIVATION_GATE"
        )

    else:

        classification = (
            "RED_COMPACT_QBALL_CONTINUATION_"
            "DOES_NOT_RECOVER_83GJ"
        )

        next_step = (
            "031C_QSHELL_OR_MULTICOMPONENT_"
            "PAYLOAD_ADJACENT_SOURCE"
        )

    print(
        f"031C83_CLASSIFICATION="
        f"{classification}"
    )

    print(
        f"NEXT="
        f"{next_step}"
    )

    OUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUT_CSV.open(
        "w",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=list(
                rows[
                    0
                ].keys()
            ),
        )

        writer.writeheader()

        writer.writerows(
            rows
        )

    output = {
        "target_energy_J":
        target,

        "valid_cases":
        len(
            rows
        ),

        "83gj_survivors":
        len(
            survivors
        ),

        "best":
        best,

        "classification":
        classification,

        "next":
        next_step,

        "claim_limits": [
            "Same global-Q-ball source theory as 031B2-A.",
            "No source leakage or backreaction threshold is relaxed.",
            "The continuation is motivated by the previous optimum lying at the minimum scanned epsilon.",
            "Full coupled nonradial stability remains open.",
            "Radiative naturalness remains open.",
            "Activation/off-state remains open.",
            "No practical device is established.",
        ],
    }

    OUT_JSON.write_text(
        json.dumps(
            to_builtin(
                output
            ),
            indent=2,
            sort_keys=True,
        )
        +
        "\n"
    )

    print(
        f"SUMMARY_JSON="
        f"{OUT_JSON.resolve()}"
    )

    print(
        f"SCAN_CSV="
        f"{OUT_CSV.resolve()}"
    )


if __name__ == "__main__":
    main()
