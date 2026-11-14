"""B17-M4A: radial interface footprint; not a full Earth-loaded BVP."""

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_exterior_transmission import (
    normalized_r3b_fit,
)
from antigravity_research.agminer.hook17_r3b_m4a_finite_footprint_gate import (
    finite_footprint,
)

BRANCH = "032H17A12D1R3X3B17-M4A"


def run(grid=0.05, order=64):
    fit = normalized_r3b_fit(grid)
    rows = []

    for clearance in (0.0, 1.0, 5.0):
        for radius in (0.25, 1.0, 2.0, 4.0):
            rows.append({
                "case": "1keV",
                **finite_footprint(
                    fit,
                    radius,
                    clearance,
                    1000.0,
                    order=order,
                ),
            })

            rows.append({
                "case": "21p147keV_matched_unloaded_sigma",
                **finite_footprint(
                    fit,
                    radius,
                    clearance,
                    21147.0,
                    order=order,
                    matched_sigma=True,
                ),
            })

    def choose(case):
        return next(
            row for row in rows
            if row["case"] == case
            and row["radius_m"] == 2.0
            and row["clearance_m"] == 0.0
        )

    return {
        "branch": BRANCH,
        "classification":
            "FINITE_RADIAL_1D_FLUX_COLUMN_CONDITIONAL_ONLY",
        "r3b_grid_m": grid,
        "preloaded_r3b_j": fit["preloaded_energy_j"],
        "rows": rows,
        "reference_1kev": choose("1keV"),
        "reference_21p147kev":
            choose("21p147keV_matched_unloaded_sigma"),
        "source_all_onboard": True,
        "earth_external_below": True,
        "physical_source_reaction_derived": False,
        "reciprocal_3d_matter_loading_solved": False,
        "full_action_source_support_solved": False,
        "complete_energy_lt_10mj_certified": False,
        "whole_craft_force_n": None,
        "gravity_cancellation": None,
        "pure_field_lift": None,
        "006d_replaced": False,
        "warning":
            "Not a full Earth-loaded BVP. "
            "Energy applies only to fixed normal-flux column class.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--grid",
        type=float,
        choices=(0.075, 0.05, 0.04),
        default=0.05,
    )
    parser.add_argument(
        "--order", type=int, default=64
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "results/data/"
            "032h17a12d1r3x3b17_m4a_summary.json"
        ),
    )

    args = parser.parse_args()
    result = run(args.grid, args.order)

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    args.output.write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "branch": BRANCH,
        "grid": args.grid,
        "r3b_j": result["preloaded_r3b_j"],
        "conditional_1kev_2m_footprint_carrier_j":
            result["reference_1kev"]
            ["optimized_conditional_carrier_j"],
        "conditional_21p147kev_2m_footprint_carrier_j":
            result["reference_21p147kev"]
            ["optimized_conditional_carrier_j"],
        "optimized_air_sigma_ratio":
            result["reference_1kev"]
            ["optimized_loaded_sigma_over_unloaded_r3b_air"],
        "optimized_ground_sigma_ratio":
            result["reference_1kev"]
            ["optimized_loaded_sigma_over_unloaded_r3b_ground"],
        "real_lift": result["pure_field_lift"],
        "warning": result["warning"],
    }, indent=2))


if __name__ == "__main__":
    main()
