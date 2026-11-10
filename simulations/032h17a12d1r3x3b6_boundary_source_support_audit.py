"""R3X3B6: independently audited baseline source support."""
import json
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_r3x3b6_boundary_support import (
    audit_grid,
)


def run():
    grids = []

    for h in (0.075, 0.05, 0.04):
        result = audit_grid(h)
        grids.append(result)

        print(
            "h=", h,
            "RAW_OUT=",
            result["old_baseline_outside_l2_fraction"],
            "CORRECTED_OUT=",
            result["boundary_corrected_outside_l2_fraction"],
            "INDEPENDENT_ERROR=",
            result["independent_stencil_relative_error"],
            "INTERFACE_E_OUT=",
            result[
                "required_electric_interface_rhs_outside_fraction"
            ],
            flush=True,
        )

    summary = {
        "branch": "032H17A12D1R3X3B6",
        "scope": "BOUNDARY_CORRECTED_BASELINE_SOURCE_AUDIT",
        "original_r3b_1p542916_j_preserved": True,
        "old_baseline_boundary_artifact_identified": True,
        "interface_compensation_obstruction_unchanged": True,
        "grids": grids,
        "microscopic_source_certified": False,
        "continuum_certified": False,
        "new_compensator_certified": False,
        "complete_energy_certified": False,
        "physical_antigravity_model_found": False,
        "006d_replaced": False,
    }

    path = Path(
        "results/data/"
        "032h17a12d1r3x3b6_boundary_source_support_summary.json"
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2) + "\n")

    print("R3X3B6_RESULT_PATH=", path)

    return summary


if __name__ == "__main__":
    run()
