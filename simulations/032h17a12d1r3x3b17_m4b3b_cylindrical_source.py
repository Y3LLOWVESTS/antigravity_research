"""B17-M4B3B: unloaded B7 source deposition into R3B grid."""

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_m4b3b_cylindrical_source import (
    r3b_aligned_source_audit,
)


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
            "results/data/b17_m4b3b_source_audit.json"
        ),
    )

    args = parser.parse_args()
    result = r3b_aligned_source_audit(args.grid)

    args.output.parent.mkdir(
        parents=True, exist_ok=True
    )
    args.output.write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )

    moments = [
        {
            "ell": row["ell"],
            "ratio": row["moment_ratio"],
            "relative_error": row["relative_moment_error"],
        }
        for row in result["source"]["moment_rows"]
    ]

    print(json.dumps({
        "branch": result["branch"],
        "grid_m": args.grid,
        "source_charge_neutrality":
            result["source"]["net_charge_relative_residual"],
        "source_outside_support_count":
            result["source"]["source_outside_support_count"],
        "unloaded_exterior_electric_l2_error":
            result["unloaded_electric_exterior_relative_l2_error"],
        "multipole_moments": moments,
        "loaded_earth_solver_executed": False,
        "whole_craft_force_n": None,
        "006d_replaced": False,
    }, indent=2))


if __name__ == "__main__":
    main()
