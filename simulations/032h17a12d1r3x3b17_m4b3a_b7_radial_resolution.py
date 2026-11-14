"""B17-M4B3A B7 radial source-resolution simulation."""

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_m4b3a_b7_radial_resolution import (
    evaluate,
)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "results/data/b17_m4b3a_b7_radial_resolution.json"
        ),
    )

    args = parser.parse_args()

    result = evaluate()

    args.output.parent.mkdir(
        parents=True, exist_ok=True
    )

    args.output.write_text(
        json.dumps(
            result, indent=2, allow_nan=False
        ) + "\n",
        encoding="utf-8",
    )

    print("B17-M4B3A: B7 finite source resolution")

    for h in (
        0.30, 0.25, 0.20, 0.10,
        0.05, 0.025, 0.02, 0.01,
    ):
        row = next(
            r for r in result["rows"]
            if r["ell"] == 1
            and abs(r["grid_m"] - h) < 1e-9
        )

        print(
            f"h={h:.3f} m; "
            f"shell_cells={row['shell_width_in_grid_cells']:.2f}; "
            f"midpoint_max_error="
            f"{row['midpoint_max_phase_relative_error']:.6g}; "
            f"split_cell_error="
            f"{row['split_cell_max_phase_relative_error']:.3g}"
        )

    print("SOURCE_LOCAL_PROFILE_CONVERGED=False")
    print("WHOLE_CRAFT_FORCE=None")
    print("B17_M4B3A_PREFLIGHT=COMPLETE")


if __name__ == "__main__":
    main()
