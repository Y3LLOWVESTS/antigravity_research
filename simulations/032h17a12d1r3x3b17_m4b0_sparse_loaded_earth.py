"""B17-M4B0 finite-Earth loaded carrier control.

All force figures are tracer integrals, not certified whole-craft force.
The source is a new finite, net-neutral control, not exact R3B.
"""
import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_m4b_sparse_earth_loading import (
    run_case,
)

BRANCH = "032H17A12D1R3X3B17-M4B0"


def run(grid=0.25):
    cases = {}

    for scale in (1000.0, 21147.0):
        for air in (False, True):
            label = (
                f"{int(scale)}eV_"
                + ("ground_air" if air else "ground_vacuum")
            )

            cases[label] = run_case(
                grid,
                portal_scale_ev=scale,
                include_air=air,
            )

    comparison = {}

    for label, case in cases.items():
        before = case["states"]["0.0"]
        after = case["states"]["1.0"]

        f0 = before["ground_frozen_tracer_force_n"]
        f1 = after["ground_frozen_tracer_force_n"]

        comparison[label] = {
            "ground_frozen_tracer_before_n": f0,
            "ground_frozen_tracer_after_n": f1,
            "signed_loaded_to_unloaded_tracer_ratio":
                f1 / f0 if f0 else None,
            "unloaded_carrier_energy_j":
                before["carrier_energy_j"],
            "loaded_carrier_energy_j":
                after["carrier_energy_j"],
            "loaded_source_fixed_solver_relative_residual":
                after["loaded_solve_residual"],
            "weighted_lorentzian_reciprocity_relative_residual":
                after["same_action_weighted_relative_residual"],
        }

    return {
        "branch": BRANCH,
        "classification":
            "SOURCE_FIXED_FINITE_BOX_TWO_U1_FROZEN_DENSITY_CONTROL",
        "grid_m": grid,
        "reference_original_r3b_field_only_energy_j":
            cases["1000eV_ground_air"]["reference_r3b_preloaded_j"],
        "new_control_source_is_exact_r3b": False,
        "source_all_onboard_phenomenological": True,
        "source_electric_net_charge_relative_residual":
            cases["1000eV_ground_air"]["electric_relative_net_charge"],
        "finite_earth_radius_m": 2.0,
        "finite_earth_depth_m": 1.0,
        "vacuum_source_enclosure_radius_m": 2.25,
        "loaded_force_grid_convergence_certified": False,
        "full_earth_halfspace": False,
        "complete_hull_support": False,
        "microscopic_source_power": None,
        "total_gravity_stress_and_earth_craft_recoil_derived": False,
        "whole_craft_force_n": None,
        "gravity_cancellation": None,
        "pure_field_lift": None,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
        "cases": cases,
        "comparison": comparison,
        "claim_limit":
            "Finite-box, fixed-source carrier BVP; not spacecraft lift",
    }


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
            "results/data/032h17a12d1r3x3b17_m4b0_summary.json"
        ),
    )

    args = parser.parse_args()
    result = run(args.grid)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )

    low = result["comparison"]["1000eV_ground_air"]
    high = result["comparison"]["21147eV_ground_air"]

    print(json.dumps({
        "branch": BRANCH,
        "grid": args.grid,
        "reference_r3b_unloaded_j":
            result["reference_original_r3b_field_only_energy_j"],
        "source_is_original_r3b": False,
        "control_1kev_air_ground_force_ratio":
            low["signed_loaded_to_unloaded_tracer_ratio"],
        "control_1kev_air_ground_loaded_force_n":
            low["ground_frozen_tracer_after_n"],
        "control_21kev_air_ground_force_ratio":
            high["signed_loaded_to_unloaded_tracer_ratio"],
        "control_21kev_air_ground_loaded_carrier_j":
            high["loaded_carrier_energy_j"],
        "maximum_weighted_reciprocity_residual": max(
            row["weighted_lorentzian_reciprocity_relative_residual"]
            for row in result["comparison"].values()
        ),
        "whole_craft_force_n": None,
        "claim_limit": result["claim_limit"],
    }, indent=2))


if __name__ == "__main__":
    main()
