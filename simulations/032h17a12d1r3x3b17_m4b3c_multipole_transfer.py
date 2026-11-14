"""B17-M4B3C multipole transfer-matrix simulation."""

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_m4b3c_multipole_transfer import (
    evaluate,
)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input", required=True, type=Path
    )
    parser.add_argument(
        "--output", required=True, type=Path
    )
    parser.add_argument(
        "--align-source-axis", action="store_true"
    )

    args = parser.parse_args()

    result = evaluate(
        args.input,
        align_source_axis=args.align_source_axis,
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

    print(json.dumps({
        "branch": result["branch"],
        "grid_m": result["grid_m"],
        "axis_aligned": result["axis_aligned"],
        "grid_shift_m":
            result["applied_grid_shift_m"],
        "max_normalized_mixed_multipole_error":
            result["normalized_mixed_max_mode_error"],
        "odd_to_even_leakage":
            result[
                "normalized_odd_input_to_even_output_leakage"
            ],
        "multipole_linear_superposition_error":
            result["linear_superposition_relative_error"],
        "original_run_reproduction_error":
            result[
                "unshifted_original_json_reproduction_error"
            ],
        "whole_craft_force_n": None,
        "warning": result["warning"],
    }, indent=2))


if __name__ == "__main__":
    main()
