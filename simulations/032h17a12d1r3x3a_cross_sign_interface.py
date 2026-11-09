"""Execute physical cross-topological opposite-sign interface source gate."""
from __future__ import annotations

import json
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_r3x3a_cross_sign_interface import (
    run_all,
)


def main():
    root = Path(__file__).resolve().parents[1]
    path = (
        root
        / "results/data/032h17a12d1r3x3a_cross_sign_interface_summary.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)

    result = run_all()

    print("BRANCH=" + result["branch"])
    print("ACTION_WARD_PASS=" + str(result["action_gate"]["pass"]))
    print(
        "SHELL_NET_NEUTRAL="
        + str(result["source_ward_gate"]["net_charge_zero_pass"])
    )

    for grid in result["grids"]:
        h = grid["h_m"]
        dual = grid["dual"]
        primal = grid["primal"]
        witness = dual.get("witness")

        print(
            f"GRID={h} "
            f"STANDOFF_M={grid['analytic_geometric_standoff_m']} "
            f"PLUS_RESID={grid['plus_loaded_residual']} "
            f"MINUS_RESID={grid['minus_loaded_residual']}"
        )

        print(
            f"OLD_DUAL_LIFT H={h} "
            f"PLUS_EIGEN={grid['old_witness_largest_plus_eigenvalue']} "
            f"OPPOSITE_EIGEN="
            f"{grid['old_witness_largest_opposite_sector_eigenvalue']} "
            f"BOTH_EXCLUDED="
            f"{grid['old_witness_excludes_both_opposite_sectors']}"
        )

        print(
            f"NEW_CROSS_DUAL H={h} STATUS={dual['status']} "
            f"GAMMA={witness.get('gamma_max') if witness else None} "
            f"PLUS={witness.get('gamma_plus') if witness else None} "
            f"MINUS={witness.get('gamma_minus') if witness else None}"
        )

        if witness:
            for budget in witness["energy_bound"]:
                print(
                    f"CROSS_BUDGET H={h} "
                    f"PERTURB={budget['normalized_matrix_perturbation']} "
                    f"MAX_MIN_A_10MJ="
                    f"{budget['maximum_min_acceleration_at_10mj_m_s2']} "
                    f"EXCLUDES={budget['one_g_excluded_below_10mj']} "
                    f"FIELD_LOWER_J="
                    f"{budget['minimum_canonical_field_energy_j_if_positive']}"
                )

        print(
            f"CROSS_PRIMAL H={h} "
            f"STATUS={primal['status']} "
            f"MIN_PER_J={primal.get('independent_min_scaled_margin')} "
            f"RANK1_MIN_A="
            f"{primal.get('rank_one_min_acceleration_per_unit_source_m_s2')} "
            f"RANK1_FIELD_REQUIRED_J="
            f"{primal.get('rank_one_required_field_j_fine_grid')}"
        )

    print(
        "CROSS_GRID="
        + json.dumps(result["cross_grid"], sort_keys=True)
    )

    path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    for key in (
        "decision",
        "next",
        "physical_antigravity_model_found",
        "certified_sub10mj_model_found",
        "continuum_certified",
        "006d_replaced",
    ):
        print(f"{key.upper()}={result[key]}")

    print("SUMMARY=" + str(path))


if __name__ == "__main__":
    main()
