"""Run 032H17A12D1R3X2R2 conditional 10MJ spectral dual certificate."""

from __future__ import annotations

import json
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_r3x2r2_budget_dual import (
    BRANCH,
    GRID_SPACINGS_M,
    provenance_gate,
    run_grid,
    decide,
)


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    output = repo / "results" / "data"
    output.mkdir(parents=True, exist_ok=True)

    provenance = provenance_gate()

    if not provenance["pass"]:
        raise RuntimeError(
            "R3X2R1 source-cone provenance invalid"
        )

    results = []

    print(f"BRANCH={BRANCH}", flush=True)

    print(
        "OBJECTIVE="
        "RECONSTRUCT_DUAL_AND_TEST_STRICT_10MJ_FIELD_BOUND",
        flush=True,
    )

    print(
        "CLAIM_SCOPE="
        "FROZEN_BETA_TWO_U1_AXISYMMETRIC_FINITE_GRIDS",
        flush=True,
    )

    for h in GRID_SPACINGS_M:
        print(f"GRID_BEGIN={h}", flush=True)

        grid = run_grid(h)
        results.append(grid)

        print(
            f"GRID_RESIDUAL H={h} "
            f"VALUE={grid['loaded_source_residual']}",
            flush=True,
        )

        for name, catalog in grid["catalogs"].items():
            solve = catalog["new_dual_solve"]
            witness = solve["witness"]

            print(
                f"CATALOG H={h} NAME={name} "
                f"SOLVER={solve['status']} "
                f"RANK={catalog['energy_rank']}/"
                f"{catalog['original_source_rank']} "
                f"ENERGY_WHITEN_ERR="
                f"{catalog['whiten_identity']['relative_error']} "
                f"BASIS_PASS={catalog['whiten_identity']['pass']}",
                flush=True,
            )

            if witness is not None:
                print(
                    f"DUAL H={h} NAME={name} "
                    f"LAMBDA_NUMPY={witness['eigenvalue_float64']} "
                    f"LAMBDA_MP70="
                    f"{witness['eigenvalue_mpmath_70dps']} "
                    f"LAMBDA_GERSHGORIN="
                    f"{witness['gershgorin_rotated_upper']} "
                    f"CONSERVATIVE="
                    f"{witness['conservative_upper_scaled_per_j']}",
                    flush=True,
                )

                for budget in catalog["budget_sensitivity"]:
                    print(
                        f"BUDGET H={h} NAME={name} "
                        f"PERTURB="
                        f"{budget['assumed_uniform_norm_perturbation']} "
                        f"ACCEL_UPPER_10MJ="
                        f"{budget['max_min_acceleration_with_budget_m_s2']} "
                        f"ENERGY_LOWER_J="
                        f"{budget['minimum_field_energy_lower_bound_j']} "
                        f"NO_OUTWARD="
                        f"{budget['unlimited_energy_outward_excluded']} "
                        f"EXCLUDES_1G="
                        f"{budget['field_budget_excludes_one_g_with_5pct_margin']}",
                        flush=True,
                    )

                print(
                    f"WITNESS_POINTS H={h} NAME={name} "
                    f"POINTS={witness['largest_weights']}",
                    flush=True,
                )

            else:
                print(
                    f"DUAL_HOLD H={h} NAME={name} "
                    f"ERROR={solve.get('error')}",
                    flush=True,
                )

    decision = decide(results)

    summary = {
        "branch": BRANCH,
        "provenance": provenance,
        "grids": results,
        **decision,
    }

    summary_path = (
        output
        / "032h17a12d1r3x2r2_energy_budget_dual_summary.json"
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
        "================ R3X2R2 FINAL DECISION ================",
        flush=True,
    )

    for key, value in decision.items():
        print(f"{key.upper()}={value}", flush=True)

    print(f"SUMMARY={summary_path}", flush=True)


if __name__ == "__main__":
    main()
