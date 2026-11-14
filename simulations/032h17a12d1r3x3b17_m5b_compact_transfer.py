"""B17-M5B compact-source cross-grid inverse-design audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_m5b_compact_transfer import (
    evaluate,
    cross_grid_transfer,
)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--bias",
        type=float,
        choices=(-0.5, 0.0, 0.5),
        required=True,
    )

    parser.add_argument(
        "--step",
        type=float,
        default=0.0002,
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
    )

    args = parser.parse_args()

    a = evaluate(
        0.25,
        step_m=args.step,
        bias=args.bias,
    )

    b = evaluate(
        0.2,
        step_m=args.step,
        bias=args.bias,
    )

    transfer = cross_grid_transfer(a, b)

    result = {
        "branch": a["branch"],
        "scope":
            "COMPACT_SOURCE_TRANSFER_NOT_PHYSICAL_LIFT",
        "shape_bias": args.bias,
        "step_m": args.step,
        "grids": {
            "0.25": a,
            "0.2": b,
        },
        "cross_grid": transfer,
        "physical_success": False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
    }

    args.output.parent.mkdir(
        parents=True, exist_ok=True
    )

    args.output.write_text(
        json.dumps(
            result, indent=2, allow_nan=False
        ) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "branch": a["branch"],
        "bias": args.bias,
        "step_m": args.step,
        "source_max_radius_m": {
            "0.25":
                a["source_audit"][
                    "max_nonzero_source_radius_m"
                ],
            "0.2":
                b["source_audit"][
                    "max_nonzero_source_radius_m"
                ],
        },
        "original_sign_earth_slope_j_per_m": {
            "0.25":
                a["controls"]["original_signs"][
                    "earth_slope_j_per_m"
                ],
            "0.2":
                b["controls"]["original_signs"][
                    "earth_slope_j_per_m"
                ],
        },
        "reversed_magnetic_earth_slope_j_per_m": {
            "0.25":
                a["controls"]["reverse_magnetic"][
                    "earth_slope_j_per_m"
                ],
            "0.2":
                b["controls"]["reverse_magnetic"][
                    "earth_slope_j_per_m"
                ],
        },
        "cross_grid_reciprocity_errors": [
            round(
                row["held_out_relative_defect"], 6
            )
            for row in transfer["cross_grid_rows"]
        ],
        "all_modes_stable_under_5pct":
            transfer["all_modes_stable_under_5pct"],
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
    }, indent=2))


if __name__ == "__main__":
    main()
