"""B17-M5C finite-domain common-translation audit."""

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_m5c_common_translation import (
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
        "--bias",
        type=float,
        choices=(-0.5, 0.0, 0.5),
        default=0.0,
    )

    parser.add_argument(
        "--reference", type=Path
    )

    parser.add_argument(
        "--output", type=Path, required=True
    )

    args = parser.parse_args()

    result = evaluate(
        args.grid,
        args.bias,
        reference=args.reference,
    )

    args.output.parent.mkdir(
        parents=True, exist_ok=True
    )

    args.output.write_text(
        json.dumps(
            result,
            indent=2,
            allow_nan=False,
        ) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "branch": result["branch"],
        "grid_m": args.grid,
        "shape_bias": args.bias,
        "source_max_radius_m":
            result["source_audit"][
                "max_nonzero_source_radius_m"
            ],
        "source_transport": {
            name: row[
                "current_shift_relative_l2_errors"
            ]
            for name, row in result[
                "current_transport"
            ].items()
        },
        "earth_present_material_transport":
            result[
                "earth_present_material_transport"
            ],
        "earth_absent_material_transport":
            result[
                "earth_absent_material_transport"
            ],
        "common_mode_controls":
            result["common_mode_controls"],
        "m5b_reference_comparison":
            result["reference_comparison"],
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
    }, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
