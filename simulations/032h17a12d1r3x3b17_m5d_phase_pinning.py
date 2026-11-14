"""B17-M5D finite-step action audit, not lift certification."""

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_m5d_phase_pinning import (
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
        choices=(-0.5, 0.0, 0.5),
    )
    parser.add_argument(
        "--small-step",
        type=float,
        default=0.0002,
    )
    parser.add_argument(
        "--reverse-magnetic",
        action="store_true",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
    )

    args = parser.parse_args()

    result = evaluate(
        args.grid,
        args.bias,
        21147.0,
        args.small_step,
        args.reverse_magnetic,
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

    paired = result[
        "matched_earth_and_craft_slopes"
    ]

    print(json.dumps({
        "branch": result["branch"],
        "h_m": args.grid,
        "bias": args.bias,
        "magnetic_reversed":
            args.reverse_magnetic,

        "subcell_paired_slope_j_per_m":
            paired["subcell"][
                "interaction_action_j"
            ]["paired_sum_slope_j_per_m"],

        "subcell_common_slope_j_per_m":
            paired["subcell"][
                "interaction_action_j"
            ]["common_shift_slope_j_per_m"],

        "one_cell_paired_slope_j_per_m":
            paired["one_cell"][
                "interaction_action_j"
            ]["paired_sum_slope_j_per_m"],

        "one_cell_common_slope_j_per_m":
            paired["one_cell"][
                "interaction_action_j"
            ]["common_shift_slope_j_per_m"],

        "phase_diagnostics":
            result["grid_phase_diagnostics"],

        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
    }, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
