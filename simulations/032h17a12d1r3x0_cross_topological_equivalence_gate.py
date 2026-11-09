"""032H17A12D1R3X0 — same-action, parity and payload gate."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_r3x0_cross_topological_gate import (
    BRANCH,
    GRIDS_M,
    LOADING_FRACTIONS,
    SOURCE_SPLITS,
    algebra_ward_gate,
    canonical_kinetic_gate,
    decision,
    field_capacity_inequality_gate,
    loaded_block_rotation_gate,
    provenance_gate,
    run_grid,
)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output = root / "results" / "data"
    output.mkdir(parents=True, exist_ok=True)

    summary_file = (
        output
        / "032h17a12d1r3x0_cross_topological_equivalence_summary.json"
    )
    csv_file = (
        output
        / "032h17a12d1r3x0_cross_topological_split_loading.csv"
    )

    provenance = provenance_gate()

    if provenance["pass"] is not True:
        raise RuntimeError(
            "R3C1/R3D0 provenance gates not satisfied"
        )

    algebra = algebra_ward_gate()
    kinetic = canonical_kinetic_gate()
    capacity = field_capacity_inequality_gate()
    block = loaded_block_rotation_gate()

    print(f"BRANCH={BRANCH}")
    print(
        "OBJECTIVE="
        "CROSS_TOPOLOGICAL_TWO_U1_WARD_REDEFINITION_LOADED_EQUIVALENCE"
    )
    print(f"PROVENANCE_PASS={provenance['pass']}")

    for key, value in algebra.items():
        print(f"WARD_{key.upper()}={value}")

    print(
        "KINETIC_POSITIVE_WITH_OPPOSITE_PORTAL_EIGENVALUES="
        f"{kinetic['passes']}"
    )
    print(
        "CANONICAL_INVARIANT_PER_ENERGY_BOUND_PASS="
        f"{capacity['inequality_pass']}"
    )
    print(
        "CANONICAL_BOUND_SATURATED="
        f"{capacity['bound_saturation_pass']}"
    )
    print(
        "LOADED_FOUR_FIELD_BLOCK_ROTATION_PASS="
        f"{block['two_equal_cross_blocks_to_opposite_self_blocks_pass']}"
    )

    grids = []
    rows = []

    for h in GRIDS_M:
        print(f"R3X0_GRID_BEGIN={h}")

        result = run_grid(h)
        grids.append(result)

        print(
            f"R3X0_ACTION_PASS_H={h} "
            f"{result['full_weighted_action_certificate']}"
        )
        print(
            f"R3X0_ACTION_REL_H={h} "
            f"{result['action_hessian_relative_residual']}"
        )

        for row in result["rows"]:
            rows.append({
                "h_m": h,
                **row,
            })

            print(
                f"R3X0_POINT H={h} "
                f"LAMBDA={row['lambda']:.9g} "
                f"SPLIT={row['split_fraction']:.3g} "
                f"MIN_A={row.get('cross_min_acceleration_m_s2')} "
                f"FIELD_J={row.get('original_field_energy_j')} "
                f"PORTAL_REL={row.get('mixed_invariant_relative_difference')} "
                f"ENERGY_REL={row.get('maxwell_energy_density_relative_difference')} "
                f"ACCEL_REL={row.get('payload_acceleration_relative_difference')} "
                f"BLOCK_1_RES={row.get('source_lane_1_relative_residual')} "
                f"BLOCK_2_RES={row.get('source_lane_2_relative_residual')} "
                f"PASS={row.get('mathematical_relabeling_identity_pass')}"
            )

    outcome = decision(
        grids,
        algebra,
        kinetic,
        capacity,
        block,
    )

    summary = {
        "branch": BRANCH,
        "provenance": provenance,
        "algebra_and_ward": algebra,
        "kinetic_normalization": kinetic,
        "canonical_capacity_inequality": capacity,
        "four_field_loaded_block_rotation": block,
        "grid_results": grids,
        "loading_fractions": list(LOADING_FRACTIONS),
        "source_splits": list(SOURCE_SPLITS),
        **outcome,
    }

    summary_file.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    if rows:
        fields = sorted(
            set().union(
                *(row.keys() for row in rows)
            )
        )

        with csv_file.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=fields,
            )
            writer.writeheader()
            writer.writerows(rows)

    print()
    print("================ R3X0 FINAL DECISION ================")

    for key in (
        "decision",
        "next",
        "algebra_ward_pass",
        "weighted_same_action_pass",
        "two_field_loaded_relabeling_pass",
        "simple_cross_mirror_sign_loss_both_grids",
        "naive_cross_portal_is_new_field_capacity",
        "all_independent_two_field_sources_closed",
        "complete_energy_established",
        "parity_completed_microscopic_model_found",
        "source_ward_realization_proven",
        "physical_antigravity_model_found",
        "certified_sub10mj_model_found",
        "006d_replaced",
    ):
        print(f"{key.upper()}={outcome[key]}")

    print(f"SUMMARY={summary_file}")
    print(f"SPLIT_CSV={csv_file}")


if __name__ == "__main__":
    main()
