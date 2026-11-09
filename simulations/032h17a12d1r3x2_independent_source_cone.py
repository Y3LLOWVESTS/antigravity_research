"""Execute R3X2 independent-source physically signed two-lane PSD gate."""

from __future__ import annotations

import json
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_r3x2_source_cone import (
    BRANCH,
    GRIDS_M,
    source_ward_gate,
    provenance_gate,
    constitutive_action_gate,
    run_grid,
    final_decision,
)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output = root / "results" / "data"
    output.mkdir(parents=True, exist_ok=True)

    provenance = provenance_gate()
    action = constitutive_action_gate()
    ward = source_ward_gate()

    assert provenance["pass"] is True
    assert action["independent_u1_gauge_bianchi_pass"] is True

    print(f"BRANCH={BRANCH}", flush=True)
    print(
        "OBJECTIVE="
        "INDEPENDENT_SHELL_SOURCE_TWO_LANE_LORENTZIAN_PSD_CONE",
        flush=True,
    )
    print(
        "NET_CHARGE_ZERO_WARD_PASS="
        f"{ward['net_charge_zero_pass']}",
        flush=True,
    )
    print(
        "MICROSCOPIC_AXIAL_CURRENT_COMPLETED=False",
        flush=True,
    )

    grids = []

    for h in GRIDS_M:
        print(f"R3X2_GRID_BEGIN={h}", flush=True)

        grid = run_grid(h)
        grids.append(grid)

        print(
            f"R3X2_CONTROL H={h} "
            f"R3X1_MATCH={grid['baseline_matches_r3x1']} "
            f"MIN_A={grid['baseline_control_min_a_m_s2']} "
            f"FIELD_J={grid['baseline_control_energy_j']} "
            f"RESID={grid['physical_sign_loaded_residual']}",
            flush=True,
        )

        for name, candidate in grid["catalogs"].items():
            print(
                "R3X2_CONE "
                f"H={h} "
                f"CATALOG={name} "
                f"STATUS={candidate['status']} "
                f"RELAXED_FEASIBLE="
                f"{candidate['verified_relaxed_feasible']} "
                f"LOWER_FIELD_J={candidate.get('relaxed_energy_j')} "
                f"RANK={candidate.get('source_cone_rank_threshold_1e-7')} "
                f"TWO_LANE={candidate['two_lane_constructive_pass']} "
                f"TWO_LANE_FIELD_J="
                f"{candidate.get('two_lane_canonical_field_energy_j')} "
                f"TWO_LANE_MIN_A="
                f"{candidate.get('two_lane_minimum_acceleration_m_s2')}",
                flush=True,
            )

    outcome = final_decision(
        provenance,
        ward,
        grids,
    )

    summary = {
        "branch": BRANCH,
        "provenance": provenance,
        "source_ward": ward,
        "constitutive_action": action,
        "grids": [
            {
                k: v
                for k, v in grid.items()
                if k != "_private"
            }
            for grid in grids
        ],
        **outcome,
    }

    summary_path = (
        output
        / "032h17a12d1r3x2_independent_source_cone_summary.json"
    )

    summary_path.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    print()
    print(
        "================ R3X2 FINAL DECISION ================"
    )

    for key, value in outcome.items():
        print(f"{key.upper()}={value}")

    print(f"SUMMARY={summary_path}")


if __name__ == "__main__":
    main()
