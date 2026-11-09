"""Execute R3X1 Lorentzian topological loaded-action audit."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    BRANCH,
    GRIDS_M,
    constitutive_action_gate,
    final_decision,
    provenance_gate,
    run_grid,
)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output = root / "results" / "data"
    output.mkdir(parents=True, exist_ok=True)

    provenance = provenance_gate()

    if not provenance["pass"]:
        raise RuntimeError(
            "R3C1/R3X0 provenance gate failed"
        )

    action = constitutive_action_gate()

    print(f"BRANCH={BRANCH}")
    print(
        "OBJECTIVE="
        "LORENTZIAN_MAXWELL_CONSTITUTIVE_SIGN_"
        "AND_FULL_LOADED_SOURCE_AUDIT"
    )

    print(
        "R3X0_GAUGE_WARD_PASS="
        f"{action['independent_u1_gauge_bianchi_pass']}"
    )

    print(
        "R3X0_FIELD_REDEFINITION_PASS="
        f"{action['field_redefinition_invariant']}"
    )

    print(
        "PHYSICAL_GAUSS_AMPERE_CROSS_SIGNS="
        f"{action['positive_K_gauss_offdiagonal_sign']},"
        f"{action['positive_K_ampere_offdiagonal_sign']}"
    )

    print("REFERENCE_R3C1_CROSS_SIGNS=1,1")

    grids = []

    for h in GRIDS_M:
        print(f"R3X1_GRID_BEGIN={h}", flush=True)

        grid = run_grid(h)
        grids.append(grid)

        certificate = grid["sign_certificate"]

        print(
            f"LORENTZIAN_HESSIAN_PASS_H_{h}="
            f"{certificate['lorentzian_static_action_pass']}",
            flush=True,
        )

        print(
            f"LORENTZIAN_HESSIAN_RESIDUALS_H_{h}="
            f"{certificate['relative_residuals']}",
            flush=True,
        )

        for row in grid["rows"]:
            print(
                "R3X1_POINT "
                f"H={h} "
                f"LAMBDA={row['lambda']} "
                f"THETA_SIGN={row['theta_sign']:+g} "
                f"SUCCESS={row['solve_success']} "
                f"COND={row['condition_number']} "
                f"RESIDUAL={row.get('relative_solve_residual')} "
                f"MIN_A={row.get('minimum_payload_acceleration_m_s2')} "
                f"ENERGY_J={row.get('canonical_field_energy_j')} "
                f"WEAK_SIGMA={row.get('weak_sigma_self_consistency')} "
                f"OUTWARD={row.get('whole_payload_outward')} "
                f"ONE_G={row.get('whole_payload_meets_one_g_floor')}",
                flush=True,
            )

        for check in grid["direct_checks"]:
            print(
                "R3X1_DIRECT "
                f"H={h} "
                f"LAMBDA={check['lambda']} "
                f"THETA_SIGN={check['theta_sign']:+g} "
                f"PASS={check['pass']} "
                f"VECTOR_REL={check['vector_relative_difference']} "
                f"ACCEL_ABS={check['minimum_acceleration_absolute_difference_m_s2']} "
                f"FIELD_REL={check['field_energy_relative_difference']}",
                flush=True,
            )

    decision = final_decision(
        provenance,
        action,
        grids,
    )

    summary = {
        "branch": BRANCH,
        "provenance": provenance,
        "lorentzian_action": action,
        "grids": grids,
        **decision,
    }

    summary_path = (
        output
        / "032h17a12d1r3x1_lorentzian_sign_audit_summary.json"
    )

    summary_path.write_text(
        json.dumps(
            summary,
            sort_keys=True,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    rows = [
        {
            "grid_h_m": grid["h_m"],
            **row,
        }
        for grid in grids
        for row in grid["rows"]
    ]

    csv_path = (
        output
        / "032h17a12d1r3x1_lorentzian_sign_audit_scan.csv"
    )

    with csv_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=sorted(rows[0]),
        )

        writer.writeheader()
        writer.writerows(rows)

    print()
    print("================ R3X1 FINAL DECISION ================")

    for key, value in decision.items():
        print(f"{key.upper()}={value}")

    print(f"SUMMARY={summary_path}")
    print(f"CSV={csv_path}")


if __name__ == "__main__":
    main()
