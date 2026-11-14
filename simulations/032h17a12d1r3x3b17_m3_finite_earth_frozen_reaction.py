"""B17-M3 finite Earth patch: frozen interaction and conditional recoil.

The actual coupled Earth-loaded fields, source current and whole
spacecraft momentum are not computed. Never promote a finite patch
conditional force to a physical spacecraft lift claim.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_exterior_transmission import (
    normalized_r3b_fit,
)

from antigravity_research.agminer.hook17_r3b_earth_frozen_reaction import (
    FiniteEarthCylinder,
    conditional_force_pair,
)

BRANCH = "032H17A12D1R3X3B17-M3"


def run(grid_m=0.05, craft_mass_kg=100.0, order=32):
    if not math.isfinite(craft_mass_kg) or craft_mass_kg <= 0:
        raise ValueError("Positive finite craft mass required")

    fit = normalized_r3b_fit(grid_m)
    rows = []

    for clearance in (0.0, 1.0, 5.0):
        # Original 2m sphere, with 1m gap from hull bottom.
        source_center = clearance + 3.0

        for radius, depth in (
            (1.0, 0.25),
            (2.0, 0.5),
            (2.0, 1.0),
            (4.0, 1.0),
            (4.0, 2.0),
        ):
            patch = FiniteEarthCylinder(
                radius_m=radius,
                depth_m=depth,
                density_kg_m3=2000.0,
            )

            result = conditional_force_pair(
                fit,
                patch,
                source_center,
                order=order,
            )

            rows.append({
                "hull_clearance_m": clearance,
                "source_center_above_surface_m": source_center,
                "earth_patch_radius_m": radius,
                "earth_patch_depth_m": depth,
                **result,
            })

    return {
        "branch": BRANCH,
        "classification":
            "FROZEN_EXTERNAL_FIELD_FINITE_EARTH_ACTION_REACTION_CONTROL",
        "r3b_grid_m": grid_m,
        "r3b_preloaded_field_energy_j": fit["preloaded_energy_j"],
        "r3b_exterior_fit_relative_rms":
            fit["fitted_exterior_rms"],
        "craft_reference_mass_kg": craft_mass_kg,
        "craft_reference_weight_n": craft_mass_kg*9.80665,
        "finite_earth_region_results": rows,
        "field_is_held_prescribed": True,
        "dense_earth_loading_included": False,
        "atmosphere_and_hull_loading_included": False,
        "microscopic_onboard_source_derived": False,
        "source_hardware_recoil_derived": False,
        "field_and_gravity_momentum_complete": False,
        "earth_full_halfspace_integrated": False,
        "earth_reaction_certified": False,
        "whole_craft_external_force_n": None,
        "effective_weight_cancellation": None,
        "field_only_lift": None,
        "auxiliary_thrust_reduction_n": None,
        "total_operating_energy_j": None,
        "complete_energy_below_10mj_certified": False,
        "006d_replaced": False,
        "warning":
            "Frozen reduced interaction potential only; no actual lift",
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
        "--mass", type=float, default=100.0
    )
    parser.add_argument(
        "--order", type=int, default=32
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "results/data/"
            "032h17a12d1r3x3b17_m3_finite_earth_frozen_reaction_summary.json"
        ),
    )

    args = parser.parse_args()
    result = run(args.grid, args.mass, args.order)

    args.output.parent.mkdir(
        parents=True, exist_ok=True
    )

    args.output.write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )

    selected = next(
        row
        for row in result["finite_earth_region_results"]
        if (
            row["hull_clearance_m"] == 0
            and row["earth_patch_radius_m"] == 2
            and row["earth_patch_depth_m"] == 1
        )
    )

    print(json.dumps({
        "branch": BRANCH,
        "grid_m": args.grid,
        "preloaded_r3b_j":
            result["r3b_preloaded_field_energy_j"],
        "conditional_frozen_earth_down_n":
            selected["earth_frozen_force_z_n"],
        "conditional_frozen_source_anchor_up_n":
            selected["source_anchor_frozen_force_z_n"],
        "reduced_action_force_residual":
            selected["pair_force_relative_residual"],
        "independent_force_residual":
            selected["volume_vs_energy_derivative_relative_residual"],
        "whole_craft_force_n":
            result["whole_craft_external_force_n"],
        "gravity_cancellation":
            result["effective_weight_cancellation"],
        "field_only_lift": result["field_only_lift"],
        "warning": result["warning"],
    }, indent=2))


if __name__ == "__main__":
    main()
