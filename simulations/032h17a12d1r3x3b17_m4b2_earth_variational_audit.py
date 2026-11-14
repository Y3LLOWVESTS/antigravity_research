"""B17-M4B2 reduced-action Earth-translation diagnostic."""

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_m4b2_earth_variational_audit import (
    evaluate,
)

BRANCH = "032H17A12D1R3X3B17-M4B2"


def run(grid=0.25, sweep_widths=False):
    cases = {}

    for scale in (1000.0, 21147.0):
        cases[str(int(scale))] = evaluate(
            grid, scale
        )

    width_controls = {}

    if sweep_widths:
        for scale in (1000.0, 21147.0):
            for width in (0.20, 0.30, 0.40):
                row = evaluate(
                    grid,
                    scale,
                    True,
                    steps=(1e-7,),
                    interface_width_m=width,
                )

                width_controls[
                    f"{int(scale)}eV_width_{width}m"
                ] = {
                    "legacy_tracer_n":
                        row["central_legacy_ground_tracer_n"],
                    "on_shell_action_slope_j_per_m":
                        row["translation_scan"][-1][
                            "on_shell_action_slope_j_per_m"
                        ],
                    "derivative_identity_error":
                        row["translation_scan"][-1][
                            "relative_derivative_identity_error"
                        ],
                }

    return {
        "branch": BRANCH,
        "grid_m": grid,
        "cases": cases,
        "interface_width_controls": width_controls,
        "complete_spacecraft_force_n": None,
        "006d_replaced": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--grid",
        type=float,
        choices=(0.3, 0.25, 0.2),
        default=0.25,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "results/data/b17_m4b2_variational.json"
        ),
    )
    parser.add_argument(
        "--sweep-widths",
        action="store_true",
    )

    args = parser.parse_args()
    result = run(args.grid, args.sweep_widths)

    args.output.parent.mkdir(
        parents=True, exist_ok=True
    )
    args.output.write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )

    for scale, case in result["cases"].items():
        entry = case["translation_scan"][-1]

        print(json.dumps({
            "grid_m": args.grid,
            "scale_ev": int(scale),
            "legacy_ground_tracer_n":
                case["central_legacy_ground_tracer_n"],
            "carrier_action_slope_j_per_m":
                entry["on_shell_action_slope_j_per_m"],
            "envelope_slope_j_per_m":
                entry["frozen_field_envelope_slope_j_per_m"],
            "derivative_identity_error":
                entry["relative_derivative_identity_error"],
            "source_b7_layer_cells":
                case["original_b7_10cm_layer_cells"],
            "whole_craft_force_n": None,
        }, indent=2))

    if args.sweep_widths:
        print(json.dumps({
            "interface_width_controls":
                result["interface_width_controls"],
        }, indent=2))


if __name__ == "__main__":
    main()
