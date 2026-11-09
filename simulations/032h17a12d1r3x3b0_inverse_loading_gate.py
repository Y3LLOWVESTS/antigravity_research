"""Execute R3X3B0 inverse-loading and source-support audit."""

from __future__ import annotations

import json
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_r3x3b0_inverse_loading import (
    BRANCH,
    GRIDS_M,
    provenance,
    constitutive_action_gate,
    run_grid,
    decide,
    action_augmentation_triage,
)


def main() -> None:
    root = Path(__file__).resolve().parents[1]

    output = (
        root
        / "results/data/"
        "032h17a12d1r3x3b0_inverse_loading_summary.json"
    )

    output.parent.mkdir(parents=True, exist_ok=True)

    prior = provenance()
    action = constitutive_action_gate()

    action_pass = bool(
        action["independent_u1_gauge_bianchi_pass"]
        and action["field_redefinition_invariant"]
        and action["positive_K_ampere_offdiagonal_sign"] == -1
    )

    if not prior["pass"] or not action_pass:
        raise RuntimeError(
            "R3X3B0_PROVENANCE_OR_ACTION_GATE_FAILED"
        )

    print(f"BRANCH={BRANCH}", flush=True)
    print(
        "OBJECTIVE=EXACT_INVERSE_LOADING_AND_SOURCE_SUPPORT",
        flush=True,
    )
    print("FULL_ACTION_COMPLETED=False", flush=True)

    grids = []

    for h in GRIDS_M:
        print(f"GRID_BEGIN={h}", flush=True)

        grid = run_grid(h)
        grids.append(grid)

        symmetry = grid["signed_sector_action_conjugacy"]
        source = grid["inverse_counter_source"]

        critical = grid[
            "scalar_beta_suppression_diagnostic"
        ]["first_failing_interval"]

        print(
            f"SIGN_CONJUGACY H={h} "
            f"PASS={symmetry['sign_conjugacy_pass']} "
            f"RELATIVE={symmetry['conjugacy_relative']}",
            flush=True,
        )

        print(
            f"FIELD H={h} "
            f"PRELOAD_J={grid['preloaded_canonical_field_j']} "
            f"PRELOAD_MIN_A={grid['preloaded_min_a_m_s2']} "
            f"FULL_LOAD_J={grid['fully_loaded_canonical_field_j']} "
            f"FULL_LOAD_MIN_A={grid['fully_loaded_min_a_m_s2']}",
            flush=True,
        )

        for channel in source["channels"]:
            print(
                f"INVERSE_SOURCE H={h} "
                f"CHANNEL={channel['channel']} "
                f"L2_OUTSIDE_2M="
                f"{channel['residual_l2_fraction_outside_strict_2m_support']} "
                f"L2_OUTSIDE_BUFFER="
                f"{channel['residual_l2_fraction_outside_buffered_support']} "
                f"L2_INSIDE_PAYLOAD="
                f"{channel['residual_l2_fraction_on_payload_nodes']} "
                f"L2_NEAR_PAYLOAD="
                f"{channel['residual_l2_fraction_payload_plus_two_cell_interface']} "
                f"BASELINE_OUTSIDE_BUFFER="
                f"{channel['baseline_current_l2_fraction_outside_buffered_source']} "
                f"PEAK_RHO={channel['required_rhs_peak_rho_m']} "
                f"PEAK_Z={channel['required_rhs_peak_z_m']} "
                f"NEEDS_OUT_OF_SUPPORT_SOURCE="
                f"{channel['any_required_rhs_outside_buffer_at_rel_1e_minus_9']}",
                flush=True,
            )

        print(
            f"EXACT_GLOBAL_MIRROR_EXTERNAL_ONLY_RULED_OUT "
            f"H={h} "
            f"VALUE="
            f"{source['exact_global_preloaded_potentials_with_external_only_old_action_ruled_out_on_grid']}",
            flush=True,
        )

        print(
            f"LOADING_FIRST_ONE_G_LOSS H={h} "
            f"BRACKET={critical}",
            flush=True,
        )

    decision = decide(
        grids,
        prior["pass"],
        action_pass,
    )

    atlas = action_augmentation_triage(
        grids[-1]["inverse_counter_source"]
    )

    summary = {
        "branch": BRANCH,
        "provenance": prior,
        "action": action,
        "grids": grids,
        "augmentation_atlas": atlas,
        **decision,
    }

    output.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    print()
    print(
        "================ R3X3B0 FINAL DECISION ================",
        flush=True,
    )

    for key, value in decision.items():
        print(f"{key.upper()}={value}", flush=True)

    print(
        "ACTION_AUGMENTATION_PREFLIGHT_ONLY="
        + json.dumps(atlas),
        flush=True,
    )

    print(f"SUMMARY={output}", flush=True)


if __name__ == "__main__":
    main()
