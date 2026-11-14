"""B17-M0: onboard source, exterior transmission and Earth-side sign test.

Physical question: does the frozen R3B exterior have the required sign on
Earth below a craft-carried source, and is a fully carrier-confined local
portal necessarily zero outside the enclosure? This is an inexpensive gate,
NOT a fully loaded Earth/craft reaction or physical propulsion calculation.

Run after standard tests, with no guessed source strength. Outputs a
persisted results/data JSON (never overwrites journal or historical outputs).
Units are SI, +z up. Source is entirely on craft; Earth below the craft.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_exterior_transmission import (
    OnboardGeometry, local_confined_portal_gate, normalized_r3b_fit,
    frozen_earth_tracer_accel,
)

BRANCH = "032H17A12D1R3X3B17-M0"


def run(h: float = 0.05) -> dict:
    fit = normalized_r3b_fit(h)
    confined = local_confined_portal_gate(
        exterior_fx_zero=True, exterior_fy_zero=True
    )
    not_confined = local_confined_portal_gate(
        exterior_fx_zero=False, exterior_fy_zero=False
    )
    rows = []
    for clearance in (0.0, 0.1, 1.0, 5.0, 10.0, 30.0, 100.0):
        geometry = OnboardGeometry(hull_bottom_above_ground_m=clearance)
        for rho in (0.0, 0.5, 1.0, 2.0, 3.0):
            a1 = frozen_earth_tracer_accel(
                fit["coefficients"], geometry, rho, 0.0,
                fit["amplitude_squared_scale"], 0.0025
            )
            a2 = frozen_earth_tracer_accel(
                fit["coefficients"], geometry, rho, 0.0,
                fit["amplitude_squared_scale"], 0.00125
            )
            rows.append({
                "hull_bottom_clearance_m": clearance,
                "source_to_earth_gap_m": geometry.source_support_to_earth_gap_m,
                "source_center_to_earth_m": geometry.source_center_z_m,
                "earth_radial_m": rho,
                "earth_surface_preloaded_az_m_s2": a2,
                "direction": "EARTH_DOWN" if a2 < 0 else ("EARTH_UP" if a2 > 0 else "ZERO"),
                "finite_difference_relative_change": abs(a1-a2)/max(abs(a2), 1e-100),
            })
    return {
        "branch": BRANCH,
        "classification": "CONDITIONAL_PRELOADED_EARTH_SIDE_AND_LOCAL_PORTAL_NO_GO",
        "r3b_grid_m": fit["grid_m"],
        "r3b_reconstructed_preloaded_energy_j": fit["preloaded_energy_j"],
        "r3b_fitted_exterior_rms": fit["fitted_exterior_rms"],
        "fully_confined_local_portal": confined,
        "exterior_carriers_allowed": not_confined,
        "tracer_rows": rows,
        "source_location": "ALL_ONBOARD_CRAFT",
        "earth_location": "EXTERNAL_GROUND_BELOW_SOURCE",
        "matter_backreaction_solved": False,
        "hull_interface_solved": False,
        "physical_microscopic_source_solved": False,
        "whole_craft_force_n": None,
        "earth_reaction_impulse_ns": None,
        "auxiliary_thrust_reduction_n": None,
        "field_only_hover_established": False,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
        "claim_limit": "Preloaded tracer sign, NOT a sourced/loaded craft-Earth force or device",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", type=float, choices=(0.075, 0.05, 0.04), default=0.05)
    parser.add_argument("--output", type=Path, default=Path(
        "results/data/032h17a12d1r3x3b17_m0_exterior_earth_facing_summary.json"
    ))
    opts = parser.parse_args()
    result = run(opts.grid)
    opts.output.parent.mkdir(parents=True, exist_ok=True)
    opts.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({
        "branch": result["branch"],
        "preloaded_energy_j": result["r3b_reconstructed_preloaded_energy_j"],
        "confined_portal_transmits": result["fully_confined_local_portal"]["direct_local_portal_transmits"],
        "surface_axis_at_contact_m_s2": result["tracer_rows"][0]["earth_surface_preloaded_az_m_s2"],
        "earth_surface_points_down": sum(x["direction"] == "EARTH_DOWN" for x in result["tracer_rows"]),
        "earth_surface_points_total": len(result["tracer_rows"]),
        "max_derivative_relative_change": max(x["finite_difference_relative_change"] for x in result["tracer_rows"]),
        "whole_craft_force_n": result["whole_craft_force_n"],
        "claim_limit": result["claim_limit"],
    }, indent=2))
    print("RESULT_JSON=" + str(opts.output))


if __name__ == "__main__":
    main()
