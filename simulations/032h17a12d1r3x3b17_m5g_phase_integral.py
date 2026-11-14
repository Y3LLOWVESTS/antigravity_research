"""ALPHA-1R2/M5G exact phase-integral audit."""

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_m5g_phase_integral import (
    evaluate,
)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--grid",
        type=float,
        choices=(0.25, 0.2),
        required=True,
    )

    parser.add_argument(
        "--reverse-magnetic",
        action="store_true",
    )

    parser.add_argument(
        "--m5d",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--m5f",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
    )

    args = parser.parse_args()

    row = evaluate(
        args.grid,
        0.0,
        args.reverse_magnetic,
        args.m5d,
        args.m5f,
    )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        json.dumps(
            row,
            indent=2,
            allow_nan=False,
        ) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "branch": row["branch"],
        "grid_m": row["grid_m"],
        "reverse_magnetic":
            row["reverse_magnetic"],

        "exact_integral_j_per_m":
            row[
                "exact_one_cell_mean_common_derivative_j_per_m"
            ],

        "phase_quadrature":
            row["quadratures"],

        "errors_against_exact_integral":
            row[
                "quadrature_errors_against_exact_identity"
            ],

        "relative_32phase_reciprocity_defect":
            row[
                "relative_32phase_reciprocity_defect"
            ],

        "diagnostic_gates":
            row["diagnostic_gates"],

        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
    }, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
