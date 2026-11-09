"""032H17A12D1R3C1 — execute exact reciprocity + ultra-small loading validation."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_r3c1_validation import (
    BRANCH,
    GRID_SPACINGS_M,
    final_decision,
    provenance_gate,
    run_grid_validation,
)


def _write_csv(
    path: Path,
    rows: list[dict],
) -> None:
    if not rows:
        return

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(
                rows[
                    0
                ].keys()
            ),
        )

        writer.writeheader()
        writer.writerows(
            rows
        )


def main() -> None:
    root = (
        Path(__file__)
        .resolve()
        .parents[
            1
        ]
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
        "032h17a12d1r3c1_hook17_fdual_f_exact_reciprocity_ultrasmall_summary.json"
    )

    scan_path = (
        data_dir
        /
        "032h17a12d1r3c1_hook17_fdual_f_ultrasmall_scan.csv"
    )

    direct_path = (
        data_dir
        /
        "032h17a12d1r3c1_hook17_fdual_f_direct_vs_woodbury.csv"
    )

    spectrum_path = (
        data_dir
        /
        "032h17a12d1r3c1_hook17_fdual_f_interface_spectrum.csv"
    )

    provenance = (
        provenance_gate()
    )

    assert provenance[
        "pass"
    ] is True

    print(
        "BRANCH="
        +
        BRANCH
    )

    print(
        "OBJECTIVE="
        "FULL_VARIATIONAL_SAME_ACTION_CERTIFICATE_"
        "PLUS_ULTRASMALL_LOADING_VALIDATION"
    )

    print(
        "R3D_STARTED=NO"
    )

    grid_results = {}
    scan_rows = []
    direct_rows = []
    spectrum_rows = []

    for h in GRID_SPACINGS_M:
        print()
        print(
            "================================================================"
        )

        print(
            "R3C1_GRID_M="
            +
            str(
                h
            )
        )

        print(
            "================================================================"
        )

        result = (
            run_grid_validation(
                h
            )
        )

        grid_results[
            str(
                h
            )
        ] = result

        cert = (
            result[
                "variational_certificate"
            ]
        )

        susceptibility = (
            result[
                "linear_susceptibility"
            ]
        )

        print(
            "INTERFACE_CELLS="
            +
            str(
                result[
                    "cells_across_interface_taper"
                ]
            )
        )

        print(
            "ACTION_AXIS_WEIGHT_H_OVER="
            +
            str(
                cert[
                    "axis_weight_required_h_over"
                ]
            )
        )

        print(
            "OLD_AXIS_WEIGHT_H_OVER="
            +
            str(
                cert[
                    "r3c_diagnostic_axis_weight_h_over"
                ]
            )
        )

        print(
            "AXIS_COUPLING_ROWS_NNZ="
            +
            str(
                cert[
                    "axis_coupling_rows_nnz"
                ]
            )
        )

        print(
            "OLD_KPHI_WEIGHTED_SYMM_REL="
            +
            str(
                cert[
                    "r3c_old_kphi_weighted_symmetry"
                ][
                    "relative_max_abs"
                ]
            )
        )

        print(
            "ACTION_KPHI_WEIGHTED_SYMM_REL="
            +
            str(
                cert[
                    "action_kphi_weighted_symmetry"
                ][
                    "relative_max_abs"
                ]
            )
        )

        print(
            "ACTION_KA_WEIGHTED_SYMM_REL="
            +
            str(
                cert[
                    "action_ka_weighted_symmetry"
                ][
                    "relative_max_abs"
                ]
            )
        )

        print(
            "ACTION_CROSS_RECIPROCITY_REL="
            +
            str(
                cert[
                    "action_cross_reciprocity"
                ][
                    "relative_max_abs"
                ]
            )
        )

        print(
            "ACTION_D_VS_EXISTING_D_REL="
            +
            str(
                cert[
                    "action_derived_d_vs_existing_d"
                ][
                    "relative_max_abs"
                ]
            )
        )

        print(
            "FULL_VARIATIONAL_SAME_ACTION_PASS="
            +
            str(
                cert[
                    "complete_variational_same_action_pass"
                ]
            )
        )

        print(
            "LINEAR_FIRST_LOSS_LAMBDA="
            +
            str(
                susceptibility[
                    "first_order_first_sign_loss_lambda"
                ]
            )
        )

        print(
            "LINEAR_FIRST_LOSS_RHO_M="
            +
            str(
                susceptibility[
                    "first_order_crossing_rho_m"
                ]
            )
        )

        print(
            "LINEAR_FIRST_LOSS_Z_M="
            +
            str(
                susceptibility[
                    "first_order_crossing_z_m"
                ]
            )
        )

        print(
            "ULTRASMALL_SCAN_BEGIN"
        )

        for row in result[
            "ultrasmall_scan"
        ]:
            scan_rows.append(
                {
                    "grid_spacing_m":
                        h,

                    **row,
                }
            )

            print(
                f"LAMBDA={row['loading_fraction']} "
                f"SOLVE={row['solve_success']} "
                f"COND={row['reduced_condition_number']} "
                f"RESID={row['relative_solve_residual']} "
                f"MIN_A={row['minimum_payload_acceleration_m_s2']} "
                f"RHO={row['worst_payload_rho_m']} "
                f"Z={row['worst_payload_z_m']} "
                f"MIG={row['worst_point_migration_m']} "
                f"ET2={row.get('interface_weighted_Etangent2_fraction')} "
                f"BN2={row.get('interface_weighted_Bnormal2_fraction')} "
                f"GBDOTB={row.get('interface_gradbeta_dot_B_rms')} "
                f"GBXE={row.get('interface_gradbeta_cross_E_rms')} "
                f"FIELD_J={row['canonical_field_energy_j']}"
            )

        print(
            "ULTRASMALL_SCAN_END"
        )

        print(
            "DIRECTLY_SAMPLED_SIGN_BRACKETS="
            +
            str(
                result[
                    "sign_change_brackets"
                ]
            )
        )

        print(
            "REFINED_SIGN_BRACKETS="
            +
            str(
                result[
                    "refined_sign_change_brackets"
                ]
            )
        )

        for row in result[
            "direct_vs_woodbury"
        ]:
            direct_rows.append(
                {
                    "grid_spacing_m":
                        h,

                    **row,
                }
            )

            print(
                "DIRECT_CHECK "
                +
                "LAMBDA="
                +
                str(
                    row[
                        "loading_fraction"
                    ]
                )
                +
                " PASS="
                +
                str(
                    row[
                        "pass"
                    ]
                )
                +
                " VECTOR_REL="
                +
                str(
                    row.get(
                        "field_vector_relative_difference"
                    )
                )
                +
                " ACCEL_ABS="
                +
                str(
                    row.get(
                        "minimum_acceleration_absolute_difference_m_s2"
                    )
                )
                +
                " ENERGY_REL="
                +
                str(
                    row.get(
                        "canonical_energy_relative_difference"
                    )
                )
            )

        spectrum = (
            result[
                "interface_spectrum"
            ]
        )

        if spectrum is not None:
            singular = (
                spectrum[
                    "reference_singular_diagnostic"
                ]
                or
                {}
            )

            spectrum_rows.append(
                {
                    "grid_spacing_m":
                        h,

                    "reduced_dimension":
                        spectrum[
                            "reduced_dimension"
                        ],

                    "spectral_radius":
                        spectrum[
                            "spectral_radius"
                        ],

                    "max_abs_imag_eigenvalue":
                        spectrum[
                            "maximum_absolute_imaginary_eigenvalue"
                        ],

                    "nearly_real_eigenvalue_fraction":
                        spectrum[
                            "nearly_real_eigenvalue_fraction"
                        ],

                    "smallest_positive_resonance_lambda":
                        spectrum[
                            "smallest_positive_resonance_lambda"
                        ],

                    "reference_lambda":
                        singular.get(
                            "reference_lambda"
                        ),

                    "reference_smallest_singular_value":
                        singular.get(
                            "smallest_singular_value"
                        ),

                    "reference_condition_number":
                        singular.get(
                            "condition_number_from_svd"
                        ),

                    "forcing_overlap":
                        singular.get(
                            "forcing_overlap_with_most_amplified_left_singular_mode"
                        ),
                }
            )

            print(
                "INTERFACE_SPECTRUM="
                +
                str(
                    spectrum
                )
            )

    decision = (
        final_decision(
            grid_results
        )
    )

    summary = {
        "branch":
            BRANCH,

        "provenance":
            provenance,

        "grid_results":
            grid_results,

        **decision,
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

    _write_csv(
        scan_path,
        scan_rows,
    )

    _write_csv(
        direct_path,
        direct_rows,
    )

    _write_csv(
        spectrum_path,
        spectrum_rows,
    )

    print()
    print(
        "================================================================"
    )

    print(
        "R3C1_FINAL_DECISION"
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
        "NEXT="
        +
        decision[
            "next"
        ]
    )

    print(
        "AUTHORIZE_R3D0="
        +
        str(
            decision[
                "authorize_r3d0_node_integrability_prefight"
            ]
        )
    )

    print(
        "VARIATIONAL_PASS_ALL="
        +
        str(
            decision[
                "full_variational_certificate_pass_all_grids"
            ]
        )
    )

    print(
        "DIRECT_WOODBURY_PASS="
        +
        str(
            decision[
                "direct_vs_woodbury_pass_original_grids"
            ]
        )
    )

    print(
        "DIRECT_BRACKET_ORIGINAL_GRIDS="
        +
        str(
            decision[
                "outward_to_inward_bracket_directly_sampled_original_grids"
            ]
        )
    )

    print(
        "INWARD_BY_1E4_ALL_GRIDS="
        +
        str(
            decision[
                "inward_by_1e4_all_three_grids"
            ]
        )
    )

    print(
        "REFINED_FIRST_LOSS_LAMBDAS="
        +
        str(
            decision[
                "refined_first_loss_lambdas"
            ]
        )
    )

    print(
        "THRESHOLD_CONTINUUM_CERTIFIED=False"
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
        "SUMMARY="
        +
        str(
            summary_path
        )
    )

    print(
        "SCAN_CSV="
        +
        str(
            scan_path
        )
    )

    print(
        "DIRECT_CSV="
        +
        str(
            direct_path
        )
    )

    print(
        "SPECTRUM_CSV="
        +
        str(
            spectrum_path
        )
    )


if __name__ == "__main__":
    main()
