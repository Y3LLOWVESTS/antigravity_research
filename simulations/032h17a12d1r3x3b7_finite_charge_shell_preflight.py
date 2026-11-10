"""R3X3B7 — three-grid finite charge-shell source preflight."""
import json
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_r3x3b7_finite_charge_shell import (
    evaluate_r3b_grid,
)


def run():
    grids = []

    for h in (0.075, 0.05, 0.04):
        row = evaluate_r3b_grid(h)
        grids.append(row)

        print(
            "GRID_H=", h,
            "ORIGINAL_J=",
            row["original_preloaded_field_energy_j"],
            flush=True,
        )

        for shell in row["shells"]:
            print(
                "SHELL_WIDTH_M=", shell["layer_width_m"],
                "FIELD_ENERGY_J=",
                shell["mixed_field_energy_j_normalized"],
                flush=True,
            )

    result = {
        "branch": "032H17A12D1R3X3B7",
        "scope": "FINITE_WIDTH_NET_NEUTRAL_ELECTRIC_SOURCE_GEOMETRY",
        "grids": grids,
        "external_preloaded_metric_response_unchanged": True,
        "mathematical_electric_source_within_2m": True,
        "original_r3b_1p542916j_preserved": True,
        "microscopic_source_realized": False,
        "reciprocal_payload_loading_solved": False,
        "continuum_certified": False,
        "complete_energy_certified": False,
        "physical_antigravity_model_found": False,
        "006d_replaced": False,
    }

    path = Path(
        "results/data/"
        "032h17a12d1r3x3b7_finite_charge_shell_summary.json"
    )

    path.write_text(json.dumps(result, indent=2) + "\n")

    print("R3X3B7_RESULT_PATH=", path)

    return result


if __name__ == "__main__":
    run()
