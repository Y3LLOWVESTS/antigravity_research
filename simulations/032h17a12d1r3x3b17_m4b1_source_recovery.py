"""B17-M4B1 approximate R3B compact-source loading preflight."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_m4b1_source_recovery import (
    BRANCH,
    run_case,
)


def run(grid=0.25):
    cases = {}

    for scale in (1000.0, 21147.0):
        for air in (False, True):
            label = (
                f"{int(scale)}eV_"
                + ("ground_air" if air else "ground_vacuum")
            )
            cases[label] = run_case(grid, scale, air)

    selected = cases["1000eV_ground_air"]
    comparisons = {}

    for label, case in cases.items():
        loaded = case["states"]["1.0"]

        comparisons[label] = {
            "loaded_to_unloaded_tracer_ratio":
                case["loaded_to_unloaded_tracer_force_ratio"],
            "loaded_ground_tracer_n":
                loaded["earth_ground_tracer_force_n"],
            "loaded_carrier_j":
                loaded["canonical_carrier_energy_j"],
            "loaded_solver_residual":
                loaded["coupled_solver_relative_residual"],
            "weighted_reciprocity_residual":
                loaded["weighted_reciprocity_residual"],
        }

    return {
        "branch": BRANCH,
        "classification":
            "R3B_ALIGNED_COMPACT_SOURCE_BVP_CONTROL_NOT_EXACT_R3B",
        "h_m": grid,
        "original_r3b_1p542916j_unloaded_anchor_preserved": True,
        "source": selected["source"],
        "r3b_target_ground_tracer_n":
            selected["r3b_unloaded_target_ground_tracer_n"],
        "recovered_unloaded_target_tracer_ratio":
            selected["recovered_vs_r3b_frozen_tracer_ratio"],
        "comparisons": comparisons,
        "cases": cases,
        "exact_r3b_source_recovered": False,
        "10cm_b7_shell_resolved": False,
        "full_earth_halfspace_solved": False,
        "field_momentum_source_stress_ledger_derived": False,
        "loaded_force_grid_convergence_certified": False,
        "complete_operating_energy_below_10mj_certified": False,
        "whole_craft_force_n": None,
        "gravity_cancellation": None,
        "propellantless_lift": None,
        "006d_replaced": False,
        "warning":
            "Approximate R3B-aligned compact source only; "
            "no physically certified thrust",
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
            "results/data/"
            "032h17a12d1r3x3b17_m4b1_summary.json"
        ),
    )

    args = parser.parse_args()
    result = run(args.grid)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )

    low = result["comparisons"]["1000eV_ground_air"]
    high = result["comparisons"]["21147eV_ground_air"]
    source = result["source"]

    print(json.dumps({
        "branch": BRANCH,
        "grid_m": args.grid,
        "original_r3b_1p542916j_preserved": True,
        "approximate_source_energy_unloaded_j":
            source["recovered_unloaded_energy_j"],
        "r3b_frozen_earth_tracer_recovery_ratio":
            result["recovered_unloaded_target_tracer_ratio"],
        "electric_exterior_l2_error":
            source["exterior_electric_relative_l2_error"],
        "magnetic_exterior_l2_error":
            source["exterior_magnetic_relative_l2_error"],
        "electric_net_charge_residual":
            source["electric_relative_net_charge"],
        "loaded_1kev_air_ground_tracer_n":
            low["loaded_ground_tracer_n"],
        "loaded_1kev_to_unloaded_ratio":
            low["loaded_to_unloaded_tracer_ratio"],
        "loaded_21kev_air_ground_tracer_n":
            high["loaded_ground_tracer_n"],
        "loaded_21kev_to_unloaded_ratio":
            high["loaded_to_unloaded_tracer_ratio"],
        "loaded_21kev_carrier_energy_j":
            high["loaded_carrier_j"],
        "whole_craft_force_n": None,
        "warning": result["warning"],
    }, indent=2))


if __name__ == "__main__":
    main()
