"""ALPHA-1R1/M5F grid-phase reciprocity preflight."""

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_m5f_phase_reciprocity import (
    evaluate,
)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--grid",
        type=float,
        required=True,
        choices=(0.25, 0.2),
    )
    parser.add_argument(
        "--bias",
        type=float,
        default=0.0,
        choices=(0.0, 0.5),
    )
    parser.add_argument(
        "--reverse-magnetic",
        action="store_true",
    )
    parser.add_argument(
        "--reference",
        type=Path,
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
    )

    args = parser.parse_args()

    result = evaluate(
        h=args.grid,
        bias=args.bias,
        reverse_magnetic=args.reverse_magnetic,
        reference=args.reference,
    )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        json.dumps(
            result,
            indent=2,
            allow_nan=False,
        ) + "\n",
        encoding="utf-8",
    )

    averages = result[
        "quadratures"
    ]["midpoint8"][
        "average_slopes"
    ]["interaction_action_j"]

    print(json.dumps({
        "branch": result["branch"],
        "grid_m": args.grid,
        "bias": args.bias,
        "reverse_magnetic":
            args.reverse_magnetic,

        "phase_averaged_earth_action_gradient_j_per_m":
            averages["earth_only_j_per_m"],

        "phase_averaged_craft_action_gradient_j_per_m":
            averages["craft_only_j_per_m"],

        "phase_averaged_reciprocity_defect_j_per_m":
            averages["paired_sum_j_per_m"],

        "phase_averaged_common_shift_gradient_j_per_m":
            averages["common_shift_j_per_m"],

        "4_to_8_phase_bin_convergence":
            result[
                "quadrature_relative_differences_4_to_8"
            ]["interaction_action_j"],

        "phase_span_j":
            result["quadratures"][
                "midpoint8"
            ]["interaction_phase_span_j"],

        "node_midpoint_averaging_disagreement_j":
            result[
                "node4_vs_midpoint4_mean_interaction_difference_j"
            ],

        "historical_reference_abs_errors":
            result[
                "central_historical_reference_abs_errors_j_per_m"
            ],

        "diagnostic_gates":
            result["diagnostic_gates"],

        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
    }, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
