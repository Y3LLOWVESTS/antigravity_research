"""M5E source-vs-material phase attribution; not a craft force."""

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_m5e_ablation import (
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
        choices=(0.0, 0.5),
        default=0.0,
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

    row = evaluate(
        args.grid,
        args.bias,
        args.reverse_magnetic,
        reference=args.reference,
    )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        json.dumps(
            row, indent=2, allow_nan=False
        ) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "branch": row["branch"],
        "grid_m": row["h_m"],
        "bias": row["bias"],
        "reversed_magnetic":
            row["magnetic_reversed"],
        "decomposition":
            row["decomposition"],
        "source_quadratic_midpoint":
            row[
                "frozen_material_quadratic_midpoint_identity"
            ],
        "m5d_reproduction_max_abs_error_j":
            row[
                "saved_m5d_full_path_reproduction_max_abs_error_j"
            ],
        "max_solver_residual":
            row["max_coupled_solver_residual"],
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
    }, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
