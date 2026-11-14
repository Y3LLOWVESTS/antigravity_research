"""ALPHA-1R6/M5K matched-current coupled response.

The reduced Lorentzian carrier is solved with a single M5I source
defined independently of the grid. Source normalization remains
artificial and physical spacecraft lift is not certified.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
)
from antigravity_research.agminer.hook17_r3b_m5i_continuum_source import (
    SourceSpec,
)
from antigravity_research.agminer.hook17_r3b_m5k_matched_coupling import (
    BRANCH,
    build_matched_source,
    solve_loaded_controls,
)


def evaluate(h, reverse, m5i_path, m5j_path):
    m5i = json.loads(Path(m5i_path).read_text())
    m5j = json.loads(Path(m5j_path).read_text())

    if (
        m5i.get("branch")
        != "032H17A12D1R3X3B17-ALPHA1R4-M5I"
        or not all(m5i["diagnostic_gates"].values())
    ):
        raise ValueError("M5I source reference invalid")

    if (
        m5j.get("branch")
        != "032H17A12D1R3X3B17-ALPHA1R5-M5J"
        or any(
            row["M5D_reproduction_max_error_j"] > 1e-6
            for row in m5j["historical_reproduction"].values()
        )
    ):
        raise ValueError("M5J solver baseline invalid")

    spec = SourceSpec(
        azimuthal_current_amplitude=(
            -1.0 if reverse else 1.0
        )
    )

    base = assemble_original_aligned_source(h)

    matched, audit = build_matched_source(
        base, spec=spec, order=6
    )

    if (
        np.array_equal(
            base["j_phi"], matched["j_phi"]
        )
        or np.array_equal(
            base["j_a"], matched["j_a"]
        )
    ):
        raise ArithmeticError(
            "Historical inverse source was not replaced"
        )

    coupled = solve_loaded_controls(matched)

    solutions = coupled["solves"]
    residuals = [
        row["relative_solver_residual"]
        for row in solutions.values()
    ]

    reciprocity = [
        row["weighted_operator_reciprocity_defect"]
        for row in solutions.values()
    ]

    source_gates = {
        "M5I_reference_passed": True,
        "M5J_historical_actions_preserved": True,
        "same_continuum_source_spec_on_both_grids": True,
        "electric_RHS_weighted_net_neutral":
            audit["relative_net_charge_residual"] < 1e-10,
        "electric_moment_within_1e_minus_4":
            audit[
                "electric_dipole_reference_relative_error"
            ] < 1e-4,
        "magnetic_moment_within_1e_minus_4":
            audit[
                "magnetic_dipole_reference_relative_error"
            ] < 1e-4,
        "all_coupled_solver_residuals_below_1e_minus_8":
            max(residuals) < 1e-8,
        "weighted_operator_reciprocity_below_1e_minus_8":
            max(reciprocity) < 1e-8,
        "zero_RHS_gives_zero_field_energy":
            solutions["zero_source"][
                "carrier_field_energy_j"
            ] < 1e-12,
        "doubling_RHS_quadruples_unloaded_energy":
            abs(
                coupled["double_RHS_unloaded_energy_ratio"]
                - 4.0
            ) < 1e-8,
    }

    return {
        "branch": BRANCH,
        "grid_m": h,
        "reversed_magnetic": reverse,
        "scope":
            "MATCHED_CONTINUUM_RHS_COUPLED_CARRIER_PREFLIGHT",
        "source_audit": audit,
        "coupled_response": coupled,
        "diagnostic_gates": source_gates,
        "scientific_certification": {
            "new_source_coupled_to_unchanged_R3B_operator":
                True,
            "source_continuum_moments_matched":
                source_gates[
                    "electric_moment_within_1e_minus_4"
                ] and source_gates[
                    "magnetic_moment_within_1e_minus_4"
                ],
            "native_RHS_has_physical_charge_current_units":
                False,
            "full_source_matter_Ward_identity":
                False,
            "complete_same_action_with_gravity":
                False,
            "whole_craft_external_force":
                False,
            "Earth_environment_reaction":
                False,
            "finite_box_artifact_excluded":
                False,
            "exterior_metric_transmission":
                False,
            "complete_energy_below_10MJ":
                False,
            "006d_replaced":
                False,
        },
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--grid", type=float, required=True,
        choices=(0.25, 0.2),
    )
    parser.add_argument(
        "--reverse-magnetic",
        action="store_true",
    )
    parser.add_argument(
        "--m5i", type=Path, required=True
    )
    parser.add_argument(
        "--m5j", type=Path, required=True
    )
    parser.add_argument(
        "--output", type=Path, required=True
    )

    args = parser.parse_args()

    result = evaluate(
        args.grid,
        args.reverse_magnetic,
        args.m5i,
        args.m5j,
    )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        json.dumps(
            result, indent=2, allow_nan=False
        ) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "branch": result["branch"],
        "grid_m": result["grid_m"],
        "reversed_magnetic":
            result["reversed_magnetic"],
        "source_audit": result["source_audit"],
        "coupled_response": result["coupled_response"],
        "diagnostic_gates": result["diagnostic_gates"],
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
    }, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
