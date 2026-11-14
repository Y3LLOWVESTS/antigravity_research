"""B17-M5A: oracle-guided, theorem-first inverse design.

The artificial target is algebraically guaranteed, not physically
realized. No spacecraft thrust or complete energy is certified.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_m5a_inverse_design import (
    evaluate,
    field_retention_oracle,
)


def run(h, scale, shape, step, mass, reference=None):
    result = evaluate(
        h, scale, step, mass, shape
    )

    if reference is not None:
        previous = json.loads(
            Path(reference).read_text(encoding="utf-8")
        )

        if (
            previous.get("branch")
            != "032H17A12D1R3X3B17-M4B1"
            or abs(float(previous["h_m"]) - h) > 1e-12
        ):
            raise ValueError(
                "M4B1 reference must match this grid"
            )

        result["artificial_scalar_field_retention_control"] = (
            field_retention_oracle(
                previous,
                9.80665 * mass,
            )
        )

    return result


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--grid",
        type=float,
        choices=(0.2, 0.25, 0.3),
        default=0.25,
    )
    parser.add_argument(
        "--portal-ev",
        type=float,
        choices=(1000.0, 21147.0),
        default=21147.0,
    )
    parser.add_argument(
        "--shape",
        choices=("original", "earth_facing", "sky_facing"),
        default="original",
    )
    parser.add_argument(
        "--step", type=float, default=0.0002
    )
    parser.add_argument(
        "--craft-mass", type=float, default=1000.0
    )
    parser.add_argument(
        "--m4b1-reference", type=Path
    )
    parser.add_argument(
        "--output", required=True, type=Path
    )

    args = parser.parse_args()

    bias = {
        "original": 0.0,
        "earth_facing": 0.5,
        "sky_facing": -0.5,
    }[args.shape]

    result = run(
        args.grid,
        args.portal_ev,
        bias,
        args.step,
        args.craft_mass,
        args.m4b1_reference,
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

    original = result["polarity_controls"]["both_positive"]
    reversed_m = result["polarity_controls"]["magnetic_reversed"]

    print(json.dumps({
        "branch": result["branch"],
        "grid_m": result["grid_m"],
        "portal_ev": result["portal_scale_ev"],
        "shape": args.shape,
        "calculation_class":
            "REDUCED_ACTION_PROXY_NOT_PHYSICAL_LIFT",
        "original_earth_action_slope_j_per_m":
            original["earth_action_slope_j_per_m"],
        "original_craft_action_slope_j_per_m":
            original["craft_action_slope_j_per_m"],
        "magnetic_flip_earth_action_slope_j_per_m":
            reversed_m["earth_action_slope_j_per_m"],
        "magnetic_flip_craft_action_slope_j_per_m":
            reversed_m["craft_action_slope_j_per_m"],
        "original_reciprocity_defect_j_per_m":
            original["reciprocity_defect_j_per_m"],
        "quadratic_norm_positive": (
            min(result["basis_norm_positive_eigenvalues"]) > 0
        ),
        "exact_reciprocal_null_directions": len(
            result["inverse_source_space"][
                "exact_reciprocal_null_directions"
            ]
        ),
        "oracle_goal_guaranteed_algebraically": True,
        "oracle_physical_success": False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "field_retention_oracle":
            result.get("artificial_scalar_field_retention_control"),
    }, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
