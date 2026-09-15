"""032H17A12D1R2B — exact-1-keV primal/dual source-space certificate."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.hook17_f2_1kev_source_upper_bound import (
    A12C_REFERENCE_CAPACITY_J,
    BRANCH,
    CAPACITY_TARGETS_J,
    FULL_BASIS_COUNT,
    NESTED_BASIS_COUNTS,
    PRIMARY_GRID_M,
    PRIMARY_PORTAL_SCALE_EV,
    TARGET_ACCELERATION_M_S2,
    VALIDATION_GRID_M,
    analyze_subspace,
    build_expanded_response,
    claim_policy_gate,
    provenance_gate,
    solve_expanded_source_coefficients,
    source_basis_labels,
    source_space_gate,
    target_efficiency_m_s2_per_j,
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
        "032h17a12d1r2b_hook17_f2_1kev_source_upper_bound_summary.json"
    )

    scan_path = (
        data_dir
        /
        "032h17a12d1r2b_hook17_f2_1kev_source_upper_bound_scan.csv"
    )

    coefficient_path = (
        data_dir
        /
        "032h17a12d1r2b_hook17_f2_1kev_source_upper_bound_coefficients.csv"
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
        "PORTAL_SCALE_EV="
        +
        str(
            PRIMARY_PORTAL_SCALE_EV
        )
    )

    print(
        "PRIMARY_GRID_M="
        +
        str(
            PRIMARY_GRID_M
        )
    )

    print(
        "FULL_EXPANDED_BASIS_COUNT="
        +
        str(
            FULL_BASIS_COUNT
        )
    )

    print(
        "REQUIRED_RESPONSE_FOR_2P656859J_M_S2_PER_J="
        +
        str(
            target_efficiency_m_s2_per_j(
                A12C_REFERENCE_CAPACITY_J
            )
        )
    )

    print(
        "BUILDING_EXPANDED_LOADED_RESPONSE=True"
    )

    full_response = (
        build_expanded_response(
            portal_scale_ev=
                PRIMARY_PORTAL_SCALE_EV,

            h=
                PRIMARY_GRID_M,
        )
    )

    print(
        "EXPANDED_RESPONSE_Z_MAX="
        +
        str(
            full_response[
                "z_max"
            ]
        )
    )

    analyses = {}
    scan_rows = []

    for basis_count in NESTED_BASIS_COUNTS:
        print()
        print(
            "ANALYZING_BASIS_COUNT="
            +
            str(
                basis_count
            )
        )

        analysis = (
            analyze_subspace(
                full_response,
                basis_count,
            )
        )

        analyses[
            str(
                basis_count
            )
        ] = analysis

        if not analysis[
            "certificate_valid"
        ]:
            print(
                "CERTIFICATE_VALID=False"
            )

            print(
                "CERTIFICATE_FAILURE_REASON="
                +
                str(
                    analysis[
                        "whitening"
                    ][
                        "reason"
                    ]
                )
            )

            scan_rows.append(
                {
                    "basis_count":
                        basis_count,

                    "certificate_valid":
                        False,

                    "energy_condition_number":
                        None,

                    "constructive_lower_bound_m_s2_per_j":
                        None,

                    "constructive_predicted_capacity_j":
                        None,

                    "pointwise_upper_bound_m_s2_per_j":
                        None,

                    "dual_upper_bound_m_s2_per_j":
                        None,

                    "certified_capacity_lower_bound_j":
                        None,

                    "a12c_2p656859j_ruled_out":
                        None,

                    "sub10j_ruled_out":
                        None,

                    "sub100j_ruled_out":
                        None,

                    "sub1kj_ruled_out":
                        None,

                    "sub10kj_ruled_out":
                        None,
                }
            )

            continue

        dual = (
            analysis[
                "dual"
            ]
        )

        primal = (
            analysis[
                "primal"
            ]
        )

        targets = (
            analysis[
                "capacity_targets"
            ]
        )

        original_target = (
            targets[
                str(
                    A12C_REFERENCE_CAPACITY_J
                )
            ]
        )

        target_10j = (
            targets[
                "10.0"
            ]
        )

        target_100j = (
            targets[
                "100.0"
            ]
        )

        target_1kj = (
            targets[
                "1000.0"
            ]
        )

        target_10kj = (
            targets[
                "10000.0"
            ]
        )

        print(
            "ENERGY_CONDITION_NUMBER="
            +
            str(
                analysis[
                    "energy_condition_number"
                ]
            )
        )

        print(
            "CONSTRUCTIVE_LOWER_BOUND_M_S2_PER_J="
            +
            str(
                primal[
                    "constructive_lower_bound_m_s2_per_j"
                ]
            )
        )

        print(
            "CONSTRUCTIVE_PREDICTED_CAPACITY_J="
            +
            str(
                primal[
                    "constructive_predicted_capacity_j"
                ]
            )
        )

        print(
            "POINTWISE_UPPER_BOUND_M_S2_PER_J="
            +
            str(
                dual[
                    "pointwise_upper_bound_m_s2_per_j"
                ]
            )
        )

        print(
            "WEIGHTED_DUAL_UPPER_BOUND_M_S2_PER_J="
            +
            str(
                dual[
                    "weighted_dual_upper_bound_m_s2_per_j"
                ]
            )
        )

        print(
            "BEST_VALID_UPPER_BOUND_M_S2_PER_J="
            +
            str(
                dual[
                    "best_valid_upper_bound_m_s2_per_j"
                ]
            )
        )

        print(
            "CERTIFIED_CAPACITY_LOWER_BOUND_J="
            +
            str(
                analysis[
                    "certified_capacity_lower_bound_j"
                ]
            )
        )

        print(
            "A12C_2P656859J_RUled_OUT="
            +
            str(
                original_target[
                    "ruled_out_by_upper_bound"
                ]
            )
        )

        print(
            "SUB10J_RUled_OUT="
            +
            str(
                target_10j[
                    "ruled_out_by_upper_bound"
                ]
            )
        )

        print(
            "SUB100J_RUled_OUT="
            +
            str(
                target_100j[
                    "ruled_out_by_upper_bound"
                ]
            )
        )

        print(
            "SUB1KJ_RUled_OUT="
            +
            str(
                target_1kj[
                    "ruled_out_by_upper_bound"
                ]
            )
        )

        print(
            "SUB10KJ_RUled_OUT="
            +
            str(
                target_10kj[
                    "ruled_out_by_upper_bound"
                ]
            )
        )

        print(
            "BOTTLENECK_RHO_M="
            +
            str(
                dual[
                    "bottleneck_payload_rho_m"
                ]
            )
        )

        print(
            "BOTTLENECK_Z_M="
            +
            str(
                dual[
                    "bottleneck_payload_z_m"
                ]
            )
        )

        scan_rows.append(
            {
                "basis_count":
                    basis_count,

                "certificate_valid":
                    True,

                "energy_condition_number":
                    analysis[
                        "energy_condition_number"
                    ],

                "constructive_lower_bound_m_s2_per_j":
                    primal[
                        "constructive_lower_bound_m_s2_per_j"
                    ],

                "constructive_predicted_capacity_j":
                    primal[
                        "constructive_predicted_capacity_j"
                    ],

                "pointwise_upper_bound_m_s2_per_j":
                    dual[
                        "pointwise_upper_bound_m_s2_per_j"
                    ],

                "dual_upper_bound_m_s2_per_j":
                    dual[
                        "best_valid_upper_bound_m_s2_per_j"
                    ],

                "certified_capacity_lower_bound_j":
                    analysis[
                        "certified_capacity_lower_bound_j"
                    ],

                "a12c_2p656859j_ruled_out":
                    original_target[
                        "ruled_out_by_upper_bound"
                    ],

                "sub10j_ruled_out":
                    target_10j[
                        "ruled_out_by_upper_bound"
                    ],

                "sub100j_ruled_out":
                    target_100j[
                        "ruled_out_by_upper_bound"
                    ],

                "sub1kj_ruled_out":
                    target_1kj[
                        "ruled_out_by_upper_bound"
                    ],

                "sub10kj_ruled_out":
                    target_10kj[
                        "ruled_out_by_upper_bound"
                    ],
            }
        )

    full_analysis = (
        analyses[
            str(
                FULL_BASIS_COUNT
            )
        ]
    )

    certificate_valid = bool(
        full_analysis[
            "certificate_valid"
        ]
    )

    validations = []

    if certificate_valid:
        full_primal = (
            full_analysis[
                "primal"
            ]
        )

        constructive_positive = bool(
            full_primal[
                "constructive_lower_bound_m_s2_per_j"
            ]
            >
            0.0
        )

        if constructive_positive:
            coefficients = np.asarray(
                full_primal[
                    "source_coefficients"
                ],
                dtype=float,
            )

            for h in VALIDATION_GRID_M:
                validation = (
                    solve_expanded_source_coefficients(
                        coefficients,
                        h,
                    )
                )

                validations.append(
                    validation
                )

                print()
                print(
                    "DIRECT_VALIDATION_GRID_M="
                    +
                    str(
                        h
                    )
                )

                print(
                    "DIRECT_VALIDATION_OUTWARD="
                    +
                    str(
                        validation[
                            "whole_payload_outward_sign"
                        ]
                    )
                )

                print(
                    "DIRECT_VALIDATION_CAPACITY_J="
                    +
                    str(
                        validation.get(
                            "loaded_quadratic_capacity_j"
                        )
                    )
                )

    direct_validation_pass = bool(
        validations
        and
        all(
            row[
                "whole_payload_outward_sign"
            ]
            and
            row.get(
                "strict_whole_payload_1g_pass",
                False,
            )
            for row in validations
        )
    )

    if direct_validation_pass:
        finest_validation = min(
            validations,
            key=lambda row:
                float(
                    row[
                        "grid_spacing_m"
                    ]
                ),
        )

        finest_capacity_j = float(
            finest_validation[
                "loaded_quadratic_capacity_j"
            ]
        )

    else:
        finest_validation = None
        finest_capacity_j = None

    if certificate_valid:
        targets = (
            full_analysis[
                "capacity_targets"
            ]
        )

        exact_target_ruled_out = bool(
            targets[
                str(
                    A12C_REFERENCE_CAPACITY_J
                )
            ][
                "ruled_out_by_upper_bound"
            ]
        )

        sub10j_ruled_out = bool(
            targets[
                "10.0"
            ][
                "ruled_out_by_upper_bound"
            ]
        )

        sub100j_ruled_out = bool(
            targets[
                "100.0"
            ][
                "ruled_out_by_upper_bound"
            ]
        )

        sub1kj_ruled_out = bool(
            targets[
                "1000.0"
            ][
                "ruled_out_by_upper_bound"
            ]
        )

        sub10kj_ruled_out = bool(
            targets[
                "10000.0"
            ][
                "ruled_out_by_upper_bound"
            ]
        )

        certified_capacity_lower_bound_j = float(
            full_analysis[
                "certified_capacity_lower_bound_j"
            ]
        )

    else:
        exact_target_ruled_out = False
        sub10j_ruled_out = False
        sub100j_ruled_out = False
        sub1kj_ruled_out = False
        sub10kj_ruled_out = False
        certified_capacity_lower_bound_j = None

    previous_count = (
        NESTED_BASIS_COUNTS[
            -2
        ]
    )

    previous_analysis = (
        analyses[
            str(
                previous_count
            )
        ]
    )

    basis_upper_bound_stable = False

    if (
        certificate_valid
        and
        previous_analysis[
            "certificate_valid"
        ]
    ):
        current_upper = float(
            full_analysis[
                "dual"
            ][
                "best_valid_upper_bound_m_s2_per_j"
            ]
        )

        previous_upper = float(
            previous_analysis[
                "dual"
            ][
                "best_valid_upper_bound_m_s2_per_j"
            ]
        )

        denominator = max(
            abs(
                current_upper
            ),
            abs(
                previous_upper
            ),
            1.0e-30,
        )

        basis_upper_bound_stable = bool(
            abs(
                current_upper
                -
                previous_upper
            )
            /
            denominator
            <
            0.25
        )

    if (
        direct_validation_pass
        and
        finest_capacity_j
        is not None
        and
        finest_capacity_j
        <=
        A12C_REFERENCE_CAPACITY_J
        *
        1.25
    ):
        decision = (
            "GREEN_SCOPED_A12D1R2B_EXACT_1KEV_FEW_JOULE_"
            "LOADED_SOURCE_RESCUE_CONSTRUCTIVELY_FOUND__"
            "PROMOTE_INDEPENDENT_HIGH_RESOLUTION_AND_SOURCE_PHYSICALIZATION"
        )

        next_branch = (
            "032H17A12D1R2C_FEW_JOULE_INDEPENDENT_RECONSTRUCTION"
        )

    elif (
        direct_validation_pass
        and
        finest_capacity_j
        is not None
        and
        finest_capacity_j
        <
        100.0
    ):
        decision = (
            "GREEN_SCOPED_A12D1R2B_EXACT_1KEV_SUB100J_"
            "LOADED_SOURCE_RESCUE_FOUND__FEW_JOULE_CLASS_REMAINS_PRIORITY"
        )

        next_branch = (
            "032H17A12D1R2C_HIGH_RESOLUTION_LOW_JOULE_REFINEMENT"
        )

    elif (
        certificate_valid
        and
        sub100j_ruled_out
        and
        basis_upper_bound_stable
    ):
        decision = (
            "RED_SCOPED_A12D1R2B_EXPANDED_76D_COMPACT_CURRENT_"
            "DUAL_CERTIFICATE_RULES_OUT_SUB100J_AT_1KEV_IN_TESTED_SPACE__"
            "THIS_IS_NOT_A_CONTINUUM_NO_GO__PROMOTE_STRUCTURAL_PORTAL_RESCUE"
        )

        next_branch = (
            "032H17A12D1R3_MIXED_EB_F_DUAL_F_LOW_CAPACITY_RESCUE"
        )

    elif (
        certificate_valid
        and
        exact_target_ruled_out
        and
        not sub100j_ruled_out
    ):
        decision = (
            "YELLOW_SCOPED_A12D1R2B_EXACT_2P656859J_TARGET_"
            "RULED_OUT_IN_EXPANDED_DISCRETE_SOURCE_SPACE_BUT_"
            "LOW_TENS_OR_HUNDREDS_OF_JOULES_NOT_CERTIFIED_CLOSED__"
            "CONTINUE_ONE_MORE_SOURCE_SPACE_REFINEMENT_OR_STRUCTURAL_RESCUE"
        )

        next_branch = (
            "032H17A12D1R2C_OR_R3_BASED_ON_CERTIFICATE_GAP"
        )

    elif certificate_valid:
        decision = (
            "YELLOW_A12D1R2B_DUAL_UPPER_BOUND_STILL_LEAVES_"
            "FEW_JOULE_MATHEMATICAL_HEADROOM_IN_EXPANDED_SOURCE_SPACE__"
            "DO_NOT_PIVOT__IMPROVE_CONSTRUCTIVE_SOLVER_AND_SOURCE_BASIS"
        )

        next_branch = (
            "032H17A12D1R2C_FEW_JOULE_PRIMAL_GAP_CLOSURE"
        )

    else:
        decision = (
            "YELLOW_A12D1R2B_CERTIFICATE_NUMERICALLY_UNRELIABLE__"
            "NO_PHYSICS_CLOSURE__REBUILD_BASIS_OR_ORTHOGONALIZATION"
        )

        next_branch = (
            "032H17A12D1R2B1_NUMERICAL_CERTIFICATE_REPAIR"
        )

    coefficient_rows = []

    if certificate_valid:
        coefficients = (
            full_analysis[
                "primal"
            ][
                "source_coefficients"
            ]
        )

        labels = (
            source_basis_labels()
        )

        for index, (
            label,
            coefficient,
        ) in enumerate(
            zip(
                labels,
                coefficients,
            )
        ):
            coefficient_rows.append(
                {
                    "basis_index":
                        index,

                    "basis_label":
                        label,

                    "coefficient":
                        coefficient,
                }
            )

    summary = {
        "branch":
            BRANCH,

        "decision":
            decision,

        "provenance":
            provenance,

        "claim_policy":
            claim_policy_gate(),

        "source_space":
            source_space_gate(),

        "portal_scale_ev":
            PRIMARY_PORTAL_SCALE_EV,

        "grid_spacing_m":
            PRIMARY_GRID_M,

        "required_efficiency_for_a12c_reference_m_s2_per_j":
            target_efficiency_m_s2_per_j(
                A12C_REFERENCE_CAPACITY_J
            ),

        "nested_analyses":
            analyses,

        "full_basis_certificate_valid":
            certificate_valid,

        "full_basis_certified_capacity_lower_bound_j":
            certified_capacity_lower_bound_j,

        "a12c_2p656859j_ruled_out_in_tested_space":
            exact_target_ruled_out,

        "sub10j_ruled_out_in_tested_space":
            sub10j_ruled_out,

        "sub100j_ruled_out_in_tested_space":
            sub100j_ruled_out,

        "sub1kj_ruled_out_in_tested_space":
            sub1kj_ruled_out,

        "sub10kj_ruled_out_in_tested_space":
            sub10kj_ruled_out,

        "basis_upper_bound_stable_52_to_76":
            basis_upper_bound_stable,

        "direct_validations":
            validations,

        "direct_validation_pass":
            direct_validation_pass,

        "direct_finest_capacity_j":
            finest_capacity_j,

        "continuous_source_space_exhausted":
            False,

        "all_possible_1kev_source_shapes_closed":
            False,

        "a12b_exact_massless_carrier_closed":
            False,

        "a12c_f2_metric_mechanism_closed":
            False,

        "mixed_eb_topological_portal_closed":
            False,

        "complete_energy_established":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "006d_replaced":
            False,

        "practical_device_found":
            False,

        "hook17_closed":
            False,

        "next":
            next_branch,
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

    with scan_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(
                scan_rows[
                    0
                ].keys()
            ),
        )

        writer.writeheader()

        writer.writerows(
            scan_rows
        )

    if coefficient_rows:
        with coefficient_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=list(
                    coefficient_rows[
                        0
                    ].keys()
                ),
            )

            writer.writeheader()

            writer.writerows(
                coefficient_rows
            )

    print()
    print(
        "================================================================"
    )

    print(
        "R2B FINAL SCIENTIFIC RESULT"
    )

    print(
        "================================================================"
    )

    print(
        "DECISION="
        +
        decision
    )

    print(
        "FULL_BASIS_CERTIFICATE_VALID="
        +
        str(
            certificate_valid
        )
    )

    if certificate_valid:
        print(
            "FULL_BASIS_CONSTRUCTIVE_LOWER_BOUND_M_S2_PER_J="
            +
            str(
                full_analysis[
                    "primal"
                ][
                    "constructive_lower_bound_m_s2_per_j"
                ]
            )
        )

        print(
            "FULL_BASIS_CONSTRUCTIVE_PREDICTED_CAPACITY_J="
            +
            str(
                full_analysis[
                    "primal"
                ][
                    "constructive_predicted_capacity_j"
                ]
            )
        )

        print(
            "FULL_BASIS_POINTWISE_UPPER_BOUND_M_S2_PER_J="
            +
            str(
                full_analysis[
                    "dual"
                ][
                    "pointwise_upper_bound_m_s2_per_j"
                ]
            )
        )

        print(
            "FULL_BASIS_WEIGHTED_DUAL_UPPER_BOUND_M_S2_PER_J="
            +
            str(
                full_analysis[
                    "dual"
                ][
                    "weighted_dual_upper_bound_m_s2_per_j"
                ]
            )
        )

        print(
            "FULL_BASIS_CERTIFIED_CAPACITY_LOWER_BOUND_J="
            +
            str(
                certified_capacity_lower_bound_j
            )
        )

        print(
            "BOTTLENECK_PAYLOAD_RHO_M="
            +
            str(
                full_analysis[
                    "dual"
                ][
                    "bottleneck_payload_rho_m"
                ]
            )
        )

        print(
            "BOTTLENECK_PAYLOAD_Z_M="
            +
            str(
                full_analysis[
                    "dual"
                ][
                    "bottleneck_payload_z_m"
                ]
            )
        )

    print(
        "A12C_2P656859J_RULED_OUT_IN_TESTED_SPACE="
        +
        str(
            exact_target_ruled_out
        )
    )

    print(
        "SUB10J_RULED_OUT_IN_TESTED_SPACE="
        +
        str(
            sub10j_ruled_out
        )
    )

    print(
        "SUB100J_RULED_OUT_IN_TESTED_SPACE="
        +
        str(
            sub100j_ruled_out
        )
    )

    print(
        "SUB1KJ_RULED_OUT_IN_TESTED_SPACE="
        +
        str(
            sub1kj_ruled_out
        )
    )

    print(
        "SUB10KJ_RULED_OUT_IN_TESTED_SPACE="
        +
        str(
            sub10kj_ruled_out
        )
    )

    print(
        "BASIS_UPPER_BOUND_STABLE_52_TO_76="
        +
        str(
            basis_upper_bound_stable
        )
    )

    print(
        "DIRECT_VALIDATION_PASS="
        +
        str(
            direct_validation_pass
        )
    )

    print(
        "DIRECT_FINEST_CAPACITY_J="
        +
        str(
            finest_capacity_j
        )
    )

    print(
        "CONTINUOUS_SOURCE_SPACE_EXHAUSTED=False"
    )

    print(
        "A12B_CARRIER_CLOSED=False"
    )

    print(
        "A12C_F2_MECHANISM_CLOSED=False"
    )

    print(
        "PHYSICAL_ANTIGRAVITY_MODEL_FOUND=False"
    )

    print(
        "CERTIFIED_SUB10MJ_MODEL_FOUND=False"
    )

    print(
        "HOOK17_CLOSED=False"
    )

    print(
        "NEXT="
        +
        next_branch
    )

    print(
        "SUMMARY_PATH="
        +
        str(
            summary_path
        )
    )

    print(
        "SCAN_PATH="
        +
        str(
            scan_path
        )
    )

    print(
        "COEFFICIENT_PATH="
        +
        str(
            coefficient_path
        )
    )


if __name__ == "__main__":
    main()
