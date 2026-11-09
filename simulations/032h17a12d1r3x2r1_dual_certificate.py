"""Execute R3X2R1 bounded maximin and independent dual certificate."""

from __future__ import annotations

import json
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_r3x2r1_dual_certificate import (
    BRANCH,
    GRIDS_M,
    prior_artifact,
    run_grid,
    decide,
)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output = root / "results" / "data"
    output.mkdir(parents=True, exist_ok=True)

    prior = prior_artifact()

    print(f"BRANCH={BRANCH}", flush=True)
    print(
        "OBJECTIVE=INDEPENDENT_BOUNDED_"
        "PRIMAL_DUAL_SOURCE_CONE_CERTIFICATE",
        flush=True,
    )

    for diagnostic in prior["prior_solver_diagnostics"]:
        print(
            f"R3X2_PRIOR_SOLVER={diagnostic}",
            flush=True,
        )

    grids = []

    for h in GRIDS_M:
        print(
            f"R3X2R1_GRID_BEGIN={h}",
            flush=True,
        )

        result = run_grid(h)
        grids.append(result)

        print(
            f"R3X2R1_SOURCE_RESIDUAL "
            f"H={h} "
            f"RESID={result['loaded_source_residual']}",
            flush=True,
        )

        for name, catalog in result["catalogs"].items():
            print(
                "R3X2R1_CATALOG "
                f"H={h} "
                f"NAME={name} "
                f"ENERGY_RANK="
                f"{catalog['energy_rank']}/"
                f"{catalog['original_source_rank']} "
                f"ENERGY_COND="
                f"{catalog['retained_condition_number']} "
                f"CERTIFIED_OUTWARD_IMPOSSIBLE="
                f"{catalog['finite_grid_declared_cone_outward_impossibility_certificate']}",
                flush=True,
            )

            for solve in catalog["primal_solves"]:
                print(
                    "R3X2R1_PRIMAL "
                    f"H={h} "
                    f"NAME={name} "
                    f"SOLVER={solve['solver']} "
                    f"STATUS={solve['status']} "
                    f"MARGIN="
                    f"{solve.get('reported_maximin_margin_scaled_per_j')} "
                    f"ERROR={solve.get('error')}",
                    flush=True,
                )

            for solve in catalog["independent_dual_solves"]:
                print(
                    "R3X2R1_DUAL "
                    f"H={h} "
                    f"NAME={name} "
                    f"SOLVER={solve['solver']} "
                    f"STATUS={solve['status']} "
                    f"BOUND="
                    f"{solve.get('reported_dual_upper_scaled_per_j')} "
                    f"ERROR={solve.get('error')}",
                    flush=True,
                )

            witness = catalog.get(
                "best_verified_dual"
            )

            if witness is not None:
                print(
                    "R3X2R1_VERIFIED_WITNESS "
                    f"H={h} "
                    f"NAME={name} "
                    f"SIMPLEX={witness['valid_simplex']} "
                    f"MAX_EIGEN="
                    f"{witness['verified_dual_upper_scaled_per_j']} "
                    f"STRICT_NEGATIVE="
                    f"{witness['strict_negative_dual_witness']} "
                    f"PAYLOAD_POINTS="
                    f"{witness['largest_weights']}",
                    flush=True,
                )

    outcome = decide(grids)

    summary = {
        "branch": BRANCH,
        "prior": prior,
        "grids": grids,
        **outcome,
    }

    summary_path = (
        output
        / "032h17a12d1r3x2r1_dual_certificate_summary.json"
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
        "================ R3X2R1 FINAL DECISION ================",
        flush=True,
    )

    for key, value in outcome.items():
        print(
            f"{key.upper()}={value}",
            flush=True,
        )

    print(
        f"SUMMARY={summary_path}",
        flush=True,
    )


if __name__ == "__main__":
    main()
