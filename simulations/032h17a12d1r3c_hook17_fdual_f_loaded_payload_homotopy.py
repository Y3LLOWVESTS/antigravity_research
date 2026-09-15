"""032H17A12D1R3C — execute loaded topological homotopy."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_loaded_payload_homotopy import (
    BRANCH,
    GRID_SPACINGS_M,
    claim_policy_gate,
    final_decision,
    node_geometry_burden,
    provenance_gate,
    _run_grid,
)


def main() -> None:
    root = (
        Path(__file__)
        .resolve()
        .parents[1]
    )

    data_dir = (
        root
        /
        "results"
        /
        "data"
    )

    data_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary_path = (
        data_dir
        /
        "032h17a12d1r3c_hook17_fdual_f_loaded_payload_homotopy_summary.json"
    )

    homotopy_path = (
        data_dir
        /
        "032h17a12d1r3c_hook17_fdual_f_loaded_payload_homotopy.csv"
    )

    provenance = (
        provenance_gate()
    )

    assert provenance[
        "pass"
    ] is True

    node = (
        node_geometry_burden()
    )

    print(
        "BRANCH="
        +
        BRANCH
    )

    print(
        "FINAL_EXPLORATORY_RUN_BEFORE_SESSION_NOTES=True"
    )

    print()
    print(
        "================================================================"
    )

    print(
        "CORRECTED POLARIZATION-NODE INTERPRETATION"
    )

    print(
        "================================================================"
    )

    print(
        "R3B_BNORMAL2_FRACTION="
        +
        str(
            node[
                "r3b_gradient_weighted_Bnormal2_fraction"
            ]
        )
    )

    print(
        "R3B_BTANGENT2_FRACTION="
        +
        str(
            node[
                "r3b_gradient_weighted_Btangent2_fraction"
            ]
        )
    )

    print(
        "R3B_RMS_B_ANGLE_TO_NORMAL_DEG="
        +
        str(
            node[
                "r3b_rms_B_angle_to_interface_normal_deg"
            ]
        )
    )

    print(
        "GROSS_REORIENTATION_TO_ESTABLISH_NODE_DEG="
        +
        str(
            node[
                "approx_gross_reorientation_to_establish_node_deg"
            ]
        )
    )

    print(
        "ADDITIONAL_NODE_CENTERED_ROTATION_ACROSS_TAPER_DEG="
        +
        str(
            node[
                "node_centered_additional_rotation_across_taper_deg"
            ]
        )
    )

    print(
        "NODE_INTERPRETATION="
        +
        node[
            "important_interpretation"
        ]
    )

    grid_results = {}
    csv_rows = []

    for h in GRID_SPACINGS_M:
        print()
        print(
            "================================================================"
        )

        print(
            "BUILDING_LOADED_INTERFACE_SYSTEM_GRID_M="
            +
            str(
                h
            )
        )

        print(
            "================================================================"
        )

        result = (
            _run_grid(
                h
            )
        )

        grid_results[
            str(
                h
            )
        ] = result

        print(
            "PAYLOAD_MASS_NUMERICAL_KG="
            +
            str(
                result[
                    "payload_mass_numerical_kg"
                ]
            )
        )

        print(
            "PEAK_BETA_MAGNITUDE="
            +
            str(
                result[
                    "payload_peak_beta_magnitude"
                ]
            )
        )

        print(
            "ACTIVE_ELECTRIC_INTERFACE_ROWS="
            +
            str(
                result[
                    "active_phi_interface_rows"
                ]
            )
        )

        print(
            "ACTIVE_MAGNETIC_INTERFACE_ROWS="
            +
            str(
                result[
                    "active_a_interface_rows"
                ]
            )
        )

        print(
            "SAME_ACTION_RECIPROCITY_MAX_ABS="
            +
            str(
                result[
                    "same_action_reciprocity_max_abs"
                ]
            )
        )

        print(
            "SAME_ACTION_DISCRETE_RECIPROCITY_EXACT="
            +
            str(
                result[
                    "same_action_discrete_reciprocity_exact"
                ]
            )
        )

        print()
        print(
            "UNLOADED_BASELINE_MIN_ACCEL_M_S2="
            +
            str(
                result[
                    "baseline"
                ][
                    "minimum_payload_acceleration_m_s2"
                ]
            )
        )

        print(
            "UNLOADED_BASELINE_FIELD_ENERGY_J="
            +
            str(
                result[
                    "baseline"
                ][
                    "canonical_field_energy_j"
                ]
            )
        )

        print(
            "UNLOADED_BASELINE_MATTER_ABS_INTERACTION_J="
            +
            str(
                result[
                    "baseline"
                ][
                    "matter_interaction_absolute_j"
                ]
            )
        )

        print()
        print(
            "LOADING_HOMOTOPY_TABLE_BEGIN"
        )

        for row in result[
            "homotopy"
        ]:
            csv_rows.append(
                {
                    "grid_spacing_m":
                        h,

                    **row,
                }
            )

            print(
                "LAMBDA="
                +
                str(
                    row[
                        "loading_fraction"
                    ]
                )
                +
                " SOLVE="
                +
                str(
                    row[
                        "solve_success"
                    ]
                )
                +
                " COND="
                +
                str(
                    row[
                        "reduced_condition_number"
                    ]
                )
                +
                " RESID="
                +
                str(
                    row[
                        "relative_solve_residual"
                    ]
                )
                +
                " MIN_A="
                +
                str(
                    row[
                        "minimum_payload_acceleration_m_s2"
                    ]
                )
                +
                " OUTWARD="
                +
                str(
                    row[
                        "whole_payload_outward"
                    ]
                )
                +
                " FIELD_1G_J="
                +
                str(
                    row[
                        "normalized_field_energy_j"
                    ]
                )
                +
                " MATTER_ABS_1G_J="
                +
                str(
                    row[
                        "normalized_matter_interaction_absolute_j"
                    ]
                )
                +
                " PARTIAL_1G_J="
                +
                str(
                    row[
                        "normalized_field_plus_abs_matter_j"
                    ]
                )
            )

        print(
            "LOADING_HOMOTOPY_TABLE_END"
        )

        critical = (
            result[
                "critical_loading"
            ]
        )

        suppression = (
            result[
                "polarization_node_suppression_target"
            ]
        )

        print()
        print(
            "FULL_LOADING_OUTWARD="
            +
            str(
                critical[
                    "full_loading_outward"
                ]
            )
        )

        print(
            "CRITICAL_LOADING_FRACTION="
            +
            str(
                critical[
                    "critical_loading_fraction"
                ]
            )
        )

        print(
            "SIGN_CROSSING_FOUND="
            +
            str(
                critical[
                    "sign_crossing_found"
                ]
            )
        )

        print(
            "REQUIRED_EFFECTIVE_INTERFACE_FRACTION="
            +
            str(
                suppression[
                    "effective_interface_fraction_target"
                ]
            )
        )

        print(
            "REQUIRED_INTERFACE_CANCELLATION_FRACTION="
            +
            str(
                suppression[
                    "minimum_interface_cancellation_fraction"
                ]
            )
        )

        print(
            "HEURISTIC_NODE_ANGULAR_TOLERANCE_DEG="
            +
            str(
                suppression[
                    "heuristic_node_angular_tolerance_deg"
                ]
            )
        )

        print()
        print(
            "OPPOSITE_SIGN_AUDIT_SOLVE="
            +
            str(
                result[
                    "opposite_sign_full_loading_audit"
                ][
                    "solve_success"
                ]
            )
        )

        print(
            "OPPOSITE_SIGN_AUDIT_MIN_ACCEL_M_S2="
            +
            str(
                result[
                    "opposite_sign_full_loading_audit"
                ][
                    "minimum_payload_acceleration_m_s2"
                ]
            )
        )

        print(
            "OPPOSITE_SIGN_AUDIT_OUTWARD="
            +
            str(
                result[
                    "opposite_sign_full_loading_audit"
                ][
                    "whole_payload_outward"
                ]
            )
        )

        print(
            "OPPOSITE_SIGN_AUDIT_PARTIAL_1G_J="
            +
            str(
                result[
                    "opposite_sign_full_loading_audit"
                ][
                    "normalized_field_plus_abs_matter_j"
                ]
            )
        )

    decision = (
        final_decision(
            grid_results
        )
    )

    print()
    print(
        "================================================================"
    )

    print(
        "R3C FINAL SCIENTIFIC RESULT"
    )

    print(
        "================================================================"
    )

    print(
        "DECISION="
        +
        decision[
            "decision"
        ]
    )

    print(
        "BOTH_GRIDS_FULL_LOADING_SOLVED="
        +
        str(
            decision[
                "both_grids_full_loading_solved"
            ]
        )
    )

    print(
        "BOTH_GRIDS_FULL_LOADING_WHOLE_PAYLOAD_OUTWARD="
        +
        str(
            decision[
                "both_grids_full_loading_whole_payload_outward"
            ]
        )
    )

    print(
        "FINE_FULL_LOADING_PARTIAL_CAPACITY_J="
        +
        str(
            decision[
                "fine_full_loading_partial_capacity_j"
            ]
        )
    )

    print(
        "SIMPLE_PARALLEL_LOADED_CORRIDOR_SURVIVES="
        +
        str(
            decision[
                "simple_parallel_loaded_corridor_survives"
            ]
        )
    )

    print(
        "FINE_CRITICAL_LOADING_FRACTION="
        +
        str(
            decision[
                "fine_critical_loading_fraction"
            ]
        )
    )

    print(
        "FINE_INTERFACE_SUPPRESSION_TARGET="
        +
        str(
            decision[
                "fine_interface_suppression_target"
            ]
        )
    )

    print(
        "PHYSICAL_ANTIGRAVITY_MODEL_FOUND=False"
    )

    print(
        "CERTIFIED_SUB10MJ_MODEL_FOUND=False"
    )

    print(
        "006D_REPLACED=False"
    )

    print(
        "SESSION_CLOSEOUT_READY="
        +
        str(
            decision[
                "session_closeout_ready"
            ]
        )
    )

    print(
        "NEXT="
        +
        decision[
            "next"
        ]
    )

    summary = {
        "branch":
            BRANCH,

        "decision":
            decision[
                "decision"
            ],

        "provenance":
            provenance,

        "node_geometry_burden":
            node,

        "claim_policy":
            claim_policy_gate(),

        "grid_results":
            grid_results,

        "final":
            decision,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "complete_operating_energy_established":
            False,

        "surface_charge_physicalized":
            False,

        "parity_cp_completed":
            False,

        "full_interacting_hyperbolicity_certified":
            False,

        "quantum_naturalness_certified":
            False,

        "empirical_consistency_certified":
            False,

        "006d_replaced":
            False,

        "hook17_closed":
            False,

        "session_closeout_ready":
            True,

        "next":
            decision[
                "next"
            ],
    }

    summary_path.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
        +
        "\n",
        encoding="utf-8",
    )

    with homotopy_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(
                csv_rows[
                    0
                ].keys()
            ),
        )

        writer.writeheader()

        writer.writerows(
            csv_rows
        )

    print(
        "SUMMARY_PATH="
        +
        str(
            summary_path
        )
    )

    print(
        "HOMOTOPY_PATH="
        +
        str(
            homotopy_path
        )
    )


if __name__ == "__main__":
    main()
