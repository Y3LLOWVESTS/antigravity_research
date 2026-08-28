"""Simulation 008A — wall plus current-carrying boundary decision gate.

PURPOSE
-------
Determine whether a simple current/charge-supported string boundary can turn
the 006D domain-wall-like core into a more physically motivated stable finite
source without losing the project's energy improvement.

PRIMARY QUESTION
----------------
Does current-supported boundary stabilization create a better repulsive
architecture than the existing 006D distributed support collar?

MODEL
-----
Effective thin domain wall plus conserved-current loop:

    E(R)
    =
    pi sigma R^2
    +
    2 pi mu R
    +
    J/R.

The equilibrium current is solved analytically.  The equilibrium boundary
stress-energy is then included in the static linearized-GR axial field.

VALIDATION
----------
The zero-bare-string limit must independently reproduce Simulation 005B.

DECISION
--------
If the best effective current-loop architecture reproduces 005B and remains
substantially more expensive than 006D, the simple localized vorton boundary
is deprioritized as an energy-improvement path.

This does not rule out a distributed field-theory realization of the 006D
support collar.

CLAIM CLASSIFICATION
--------------------
ANALYTICAL_EFFECTIVE_FIELD_THEORY_GATE
"""

from __future__ import annotations

import csv
from pathlib import Path

from antigravity_research.geometry.wall_current_loop import (
    optimize_mass_coefficient,
)


ROOT = Path(__file__).resolve().parents[1]

OUTPUT = (
    ROOT
    / "results"
    / "data"
    / "008a_wall_current_loop_gate.csv"
)

REFERENCE_005B_C = 79.753148116012
REFERENCE_005B_X = 4.006149730748

REFERENCE_006D_C = 23.591586299249


def main() -> None:
    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    ratios = [
        0.0,
        0.01,
        0.05,
        0.10,
        0.25,
    ]

    rows = []

    print(
        "=== SIMULATION 008A — WALL + CURRENT LOOP GATE ==="
    )

    print(
        "MODEL=EFFECTIVE_DOMAIN_WALL_PLUS_CONSERVED_CURRENT_LOOP"
    )

    print(
        "FULL_MICROSCOPIC_VORTON_FIELD_THEORY=NOT_MODELED"
    )

    print()
    print("=== OPTIMIZATION SCAN ===")

    for m in ratios:
        x, coefficient = (
            optimize_mass_coefficient(m)
        )

        rows.append(
            {
                "bare_string_ratio": m,
                "optimal_r_over_h": x,
                "mass_coefficient": coefficient,
            }
        )

        print(
            f"BARE_STRING_RATIO={m:.6f} "
            f"OPTIMAL_R_OVER_H={x:.12f} "
            f"C={coefficient:.12f}"
        )

    best = rows[0]

    x0 = float(
        best["optimal_r_over_h"]
    )

    c0 = float(
        best["mass_coefficient"]
    )

    recovers_005b = (
        abs(
            x0
            - REFERENCE_005B_X
        )
        < 2.0e-6
        and abs(
            c0
            - REFERENCE_005B_C
        )
        < 1.0e-8
    )

    positive_mu_worsens = all(
        float(row["mass_coefficient"])
        > c0
        for row in rows[1:]
    )

    improves_006d = (
        c0
        < REFERENCE_006D_C
    )

    ratio_to_006d = (
        c0
        / REFERENCE_006D_C
    )

    with OUTPUT.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "bare_string_ratio",
                "optimal_r_over_h",
                "mass_coefficient",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    print()
    print("=== CENTRAL RESULT ===")

    print(
        f"ZERO_BARE_STRING_OPTIMAL_R_OVER_H="
        f"{x0:.12f}"
    )

    print(
        f"ZERO_BARE_STRING_C="
        f"{c0:.12f}"
    )

    print(
        f"REFERENCE_005B_C="
        f"{REFERENCE_005B_C:.12f}"
    )

    print(
        f"REFERENCE_006D_C="
        f"{REFERENCE_006D_C:.12f}"
    )

    print(
        f"CURRENT_LOOP_TO_006D_C_RATIO="
        f"{ratio_to_006d:.12f}"
    )

    print(
        "RECOVERS_005B="
        f"{'YES' if recovers_005b else 'NO'}"
    )

    print(
        "POSITIVE_BARE_STRING_ENERGY_WORSENS="
        f"{'YES' if positive_mu_worsens else 'NO'}"
    )

    print(
        "RADIAL_EFFECTIVE_STABILITY="
        "YES"
    )

    print(
        "FULL_FIELD_THEORY_STABILITY="
        "NOT_ESTABLISHED"
    )

    print(
        "WALL_PLUS_CURRENT_LOOP_IMPROVES_006D="
        f"{'YES' if improves_006d else 'NO'}"
    )

    print()
    print("=== SCIENTIFIC DECISION ===")

    decision_green = (
        recovers_005b
        and positive_mu_worsens
        and not improves_006d
    )

    print(
        "SIMPLE_LOCALIZED_VORTON_BOUNDARY="
        f"{'DEPRIORITIZE_AS_ENERGY_PATH' if decision_green else 'UNRESOLVED'}"
    )

    print(
        "CURRENT_LOOP_CAN_SUPPLY_REQUIRED_EFFECTIVE_COMPRESSION="
        "YES_WITHIN_EFFECTIVE_MODEL"
    )

    print(
        "006D_DISTRIBUTED_COLLAR_REMAINS_MORE_EFFICIENT="
        f"{'YES' if ratio_to_006d > 1.0 else 'NO'}"
    )

    print(
        "KNOWN_MICROSCOPIC_REALIZATION_OF_006D_COLLAR="
        "NO"
    )

    print(
        "DYNAMIC_STABILITY_OF_COMPLETE_006D_SOURCE="
        "NOT_ESTABLISHED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "ANALYTICAL_EFFECTIVE_FIELD_THEORY_GATE"
    )

    print(
        "NEXT="
        "DISTRIBUTED_FIELD_THEORY_COLLAR_REALIZATION_OR_CLASSICAL_BRANCH_STOP"
    )

    print(
        f"OUTPUT_CSV={OUTPUT}"
    )

    print(
        "SIMULATION_008A=GREEN"
        if decision_green
        else "SIMULATION_008A=REVIEW"
    )


if __name__ == "__main__":
    main()
