"""B17-M2: finite local Earth-interface variational energy preflight.

The two 1cm layers represent a hypothetical local slab adjacent
to Earth's surface. They do NOT model the entire atmosphere,
ground half-space, or finite spacecraft.

Source-side D is allowed to adjust. This is a relaxed mathematical
minimum, without paying for the real onboard generator.

The higher portal-scale comparator rescales B proportional to M^2
to preserve the prescribed sigma strength, not a physical source.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_layer_variational_gate import (
    Layer,
    axial_slab_variational,
    physical_r3b_axial_b,
    stationary_nosource_planar_localization_gate,
)

BRANCH = "032H17A12D1R3X3B17-M2"


def run(grid_m: float = 0.05) -> dict:
    fit = physical_r3b_axial_b(grid_m)
    b = fit["fitted_normal_b_r3b_units"]

    air_ground = (
        Layer("air", 0.01, 1.2),
        Layer("ground", 0.01, 2000.0),
    )

    vacuum_ground = (
        Layer("vacuum", 0.01, 0.0),
        Layer("ground", 0.01, 2000.0),
    )

    reference = axial_slab_variational(
        air_ground,
        b,
        1000.0,
        fixed_source_e_normal=b,
    )

    vacuum = axial_slab_variational(
        vacuum_ground,
        b,
        1000.0,
        fixed_source_e_normal=b,
    )

    # Conditional B1-scale comparator:
    # fixed metric sigma requires B proportional to M^2.
    factor = 21.147

    higher_scale = axial_slab_variational(
        air_ground,
        b*factor**2,
        1000.0*factor,
        fixed_source_e_normal=b*factor**2,
    )

    return {
        "branch": BRANCH,
        "classification":
            "ONE_DIMENSIONAL_FROZEN_THETA_CONDITIONAL_ENERGY_FLOOR",
        "preloaded_fit": fit,
        "air_ground_1cm_each_1kev": reference,
        "vacuum_ground_1cm_each_1kev": vacuum,
        "air_ground_1cm_each_21p147kev_matched_sigma":
            higher_scale,
        "planar_source_free_zero_theorem":
            stationary_nosource_planar_localization_gate(
                True, True
            ),
        "assumptions": [
            "Local 1D fixed axial B, not full 3D geometry",
            "No free interface or bulk sheets",
            "Two 1cm test layers, not full Earth",
            "Source D may adjust; source cost excluded",
            "Theta follows idealized frozen-density law",
            "Carrier Hamiltonian only; not total matter energy",
            "Higher-scale comparator uses prescribed sigma",
        ],
        "whole_craft_force_n": None,
        "earth_down_force_n": None,
        "source_support_and_hull_solved": False,
        "recoil_and_total_stress_derived": False,
        "gravity_cancellation": None,
        "pure_field_lift": None,
        "complete_energy_under_10mj_certified": False,
        "006d_replaced": False,
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
        "--output",
        type=Path,
        default=Path(
            "results/data/"
            "032h17a12d1r3x3b17_m2_variational_earth_layer_summary.json"
        ),
    )

    args = parser.parse_args()

    result = run(args.grid)

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
        "grid_m": args.grid,
        "preloaded_r3b_j":
            result["preloaded_fit"]["r3b_preloaded_energy_j"],
        "b_on_axis":
            result["preloaded_fit"]["fitted_normal_b_r3b_units"],
        "air_ground_fixed_j_per_m2":
            result["air_ground_1cm_each_1kev"]
            ["fixed_source"]["carrier_energy_j_per_m2"],
        "air_ground_optimized_j_per_m2":
            result["air_ground_1cm_each_1kev"]
            ["optimal"]["carrier_energy_j_per_m2"],
        "vacuum_ground_optimized_j_per_m2":
            result["vacuum_ground_1cm_each_1kev"]
            ["optimal"]["carrier_energy_j_per_m2"],
        "higher_portal_optimized_j_per_m2":
            result["air_ground_1cm_each_21p147kev_matched_sigma"]
            ["optimal"]["carrier_energy_j_per_m2"],
        "lift": result["pure_field_lift"],
        "warning":
            "CONDITIONAL LOCAL PER-AREA ENERGY, NOT CRAFT FORCE",
    }, indent=2))


if __name__ == "__main__":
    main()
