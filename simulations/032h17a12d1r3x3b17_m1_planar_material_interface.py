"""B17-M1: exact local interface test using actual R3B multipoles.

Scans the original source's Earth-facing field from the craft-mounted
B17-M0 geometry. Vacuum -> air -> ground interface matching is compared
with direct vacuum -> ground matching.

The result is a *local planar* necessary-condition diagnostic. It is
not a global field or Earth-loaded spacecraft solution.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.hook17_r3b_exterior_transmission import (
    OnboardGeometry,
    fitted_b_field,
    normalized_r3b_fit,
)
from antigravity_research.agminer.hook17_r3b_earth_interface import (
    classify_lift,
    field_only_energy_density,
    jump_residuals,
    match_no_free_interface,
    original_mirror_state,
    source_sheet_needed_to_preserve_fields,
    theta_for_density,
)

BRANCH = "032H17A12D1R3X3B17-M1"


def _components(state):
    return (state.e_x, state.b_x, state.e_y, state.b_y)


def run(grid_m=0.05, craft_mass_kg=100.0):
    fit = normalized_r3b_fit(grid_m)

    theta_vac = theta_for_density(0.0)
    theta_air = theta_for_density(1.2)
    theta_ground = theta_for_density(2000.0)

    rows = []

    for clearance in (0.0, 1.0, 5.0):
        geometry = OnboardGeometry(
            hull_bottom_above_ground_m=clearance
        )

        for rho in (0.0, 0.5, 1.0, 2.0, 3.0):
            br, bz = fitted_b_field(
                fit["coefficients"],
                rho,
                -geometry.source_center_z_m,
            )

            vacuum = original_mirror_state(br, bz)

            air = match_no_free_interface(
                vacuum, theta_vac, theta_air
            )

            ground = match_no_free_interface(
                air, theta_air, theta_ground
            )

            direct = match_no_free_interface(
                vacuum, theta_vac, theta_ground
            )

            error = max(
                float(np.max(np.abs(a - b)))
                for a, b in zip(
                    _components(ground),
                    _components(direct),
                )
            )

            scale = max(
                1.0,
                *(
                    float(np.max(np.abs(vector)))
                    for vector in _components(direct)
                ),
            )

            reference_energy = field_only_energy_density(vacuum)

            air_residual = jump_residuals(
                vacuum, air, theta_vac, theta_air
            )

            ground_residual = jump_residuals(
                air, ground, theta_air, theta_ground
            )

            rows.append({
                "hull_bottom_clearance_m": clearance,
                "source_to_ground_gap_m":
                    geometry.source_support_to_earth_gap_m,
                "radial_m": rho,
                "preloaded_field_norm": math.hypot(br, bz),
                "vacuum_to_air_field_only_density_ratio":
                    field_only_energy_density(air) / reference_energy,
                "vacuum_to_ground_field_only_density_ratio":
                    field_only_energy_density(ground) / reference_energy,
                "relative_composition_error": error / scale,
                "max_scaled_jump_residual": max(
                    *air_residual.values(),
                    *ground_residual.values(),
                ) / scale,
                "canonical_sheet_required_if_ground_field_unchanged":
                    source_sheet_needed_to_preserve_fields(
                        vacuum, theta_vac, theta_ground
                    ),
            })

    return {
        "branch": BRANCH,
        "classification":
            "EXACT_LOCAL_PLANAR_FROZEN_THETA_JUMP_NECESSITY_ONLY",
        "r3b_grid_m": grid_m,
        "r3b_preloaded_energy_j": fit["preloaded_energy_j"],
        "r3b_fit_relative_rms": fit["fitted_exterior_rms"],
        "theta_vacuum": theta_vac,
        "theta_air_1p2_kg_m3": theta_air,
        "theta_ground_2000_kg_m3": theta_ground,
        "rows": rows,
        "craft_lift_gate": classify_lift(craft_mass_kg, None),
        "whole_craft_force_derived": False,
        "earth_3d_loading_solved": False,
        "hull_interface_solved": False,
        "physical_source_realized": False,
        "earth_reaction_derived": False,
        "full_energy_balance_derived": False,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
        "claim_limit":
            "Local planar Maxwell matching, not Earth force or craft lift",
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
        "--craft-mass-kg", type=float, default=100.0
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "results/data/"
            "032h17a12d1r3x3b17_m1_planar_material_interface_summary.json"
        ),
    )

    args = parser.parse_args()
    result = run(args.grid, args.craft_mass_kg)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "branch": BRANCH,
        "grid_m": args.grid,
        "theta_air": result["theta_air_1p2_kg_m3"],
        "theta_ground": result["theta_ground_2000_kg_m3"],
        "axis_contact_air_field_density_ratio":
            result["rows"][0][
                "vacuum_to_air_field_only_density_ratio"
            ],
        "axis_contact_ground_field_density_ratio":
            result["rows"][0][
                "vacuum_to_ground_field_only_density_ratio"
            ],
        "max_composition_relative_error": max(
            row["relative_composition_error"]
            for row in result["rows"]
        ),
        "gravity_cancellation":
            result["craft_lift_gate"]["gravity_cancellation"],
        "pure_field_lift":
            result["craft_lift_gate"]["pure_field_lift"],
        "whole_craft_force_derived":
            result["whole_craft_force_derived"],
        "claim_limit": result["claim_limit"],
    }, indent=2))


if __name__ == "__main__":
    main()
