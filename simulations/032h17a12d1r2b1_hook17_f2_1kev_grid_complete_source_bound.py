"""032H17A12D1R2B1 — grid-complete 1-keV pointwise source certificate."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from antigravity_research.agminer.hook17_f2_1kev_grid_complete_source_bound import (
    A12C_REFERENCE_CAPACITY_J,
    BRANCH,
    CERTIFICATE_GRID_SPACINGS_M,
    GRID_BOUND_STABILITY_RELATIVE_TOL,
    PORTAL_SCALE_EV,
    TARGET_ACCELERATION_M_S2,
    claim_policy_gate,
    grid_complete_pointwise_certificate,
    provenance_gate,
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
        "032h17a12d1r2b1_hook17_f2_1kev_grid_complete_source_bound_summary.json"
    )

    scan_path = (
        data_dir
        /
        "032h17a12d1r2b1_hook17_f2_1kev_grid_complete_source_bound_scan.csv"
    )

    provenance = provenance_gate()

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
            PORTAL_SCALE_EV
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
        "PRIOR_R2B_DECISION_STRING_LOGIC_INCONSISTENT="
        +
        str(
            provenance[
                "r2b_decision_string_logic_inconsistent"
            ]
        )
    )

    results = []

    for h in CERTIFICATE_GRID_SPACINGS_M:
        print()
        print(
            "BUILDING_GRID_COMPLETE_SOURCE_SPACE_H_M="
            +
            str(
                h
            )
        )

        result = (
            grid_complete_pointwise_certificate(
                h
            )
        )

        results.append(
            result
        )

        print(
            "GRID_M="
            +
            str(
                h
            )
        )

        print(
            "CERTIFICATE_VALID="
            +
            str(
                result[
                    "certificate_valid"
                ]
            )
        )

        print(
            "SOURCE_DOF_COUNT="
            +
            str(
                result[
                    "source_dof_count"
                ]
            )
        )

        print(
            "PAYLOAD_CERTIFICATE_POINT_COUNT="
            +
            str(
                result[
                    "payload_certificate_point_count"
                ]
            )
        )

        if not result[
            "certificate_valid"
        ]:
            print(
                "CERTIFICATE_FAILURE_REASON="
                +
                str(
                    result[
                        "reason"
                    ]
                )
            )

            continue

        print(
            "ENERGY_CONDITION_NUMBER="
            +
            str(
                result[
                    "energy_condition_number"
                ]
            )
        )

        print(
            "WHOLE_PAYLOAD_POINTWISE_UPPER_BOUND_M_S2_PER_J="
            +
            str(
                result[
                    "whole_payload_pointwise_upper_bound_m_s2_per_j"
                ]
            )
        )

        print(
            "CERTIFIED_LOADED_CAPACITY_FLOOR_J="
            +
            str(
                result[
                    "certified_loaded_capacity_floor_j"
                ]
            )
        )

        print(
            "BOTTLENECK_RHO_M="
            +
            str(
                result[
                    "bottleneck_payload_rho_m"
                ]
            )
        )

        print(
            "BOTTLENECK_Z_M="
            +
            str(
                result[
                    "bottleneck_payload_z_m"
                ]
            )
        )

        print(
            "PRIOR_R2B_BOTTLENECK_LOCAL_UPPER_BOUND_M_S2_PER_J="
            +
            str(
                result[
                    "prior_r2b_bottleneck_local_upper_bound_m_s2_per_j"
                ]
            )
        )

        print(
            "GRID_COMPLETE_BOUND_OVER_R2B_76D_BOUND="
            +
            str(
                result[
                    "grid_complete_upper_bound_over_r2b_76d_bound"
                ]
            )
        )

        targets = (
            result[
                "capacity_targets"
            ]
        )

        for label, capacity in (
            (
                "A12C_2P656859J",
                A12C_REFERENCE_CAPACITY_J,
            ),
            (
                "SUB10J",
                10.0,
            ),
            (
                "SUB100J",
                100.0,
            ),
            (
                "SUB1KJ",
                1000.0,
            ),
            (
                "SUB10KJ",
                10000.0,
            ),
            (
                "SUB100KJ",
                100000.0,
            ),
            (
                "SUB1MJ",
                1000000.0,
            ),
            (
                "SUB10MJ",
                10000000.0,
            ),
        ):
            print(
                label
                +
                "_RULED_OUT="
                +
                str(
                    targets[
                        str(
                            capacity
                        )
                    ][
                        "ruled_out_by_pointwise_upper_bound"
                    ]
                )
            )

    valid_results = [
        result
        for result in results
        if result[
            "certificate_valid"
        ]
    ]

    all_valid = bool(
        len(
            valid_results
        )
        ==
        len(
            CERTIFICATE_GRID_SPACINGS_M
        )
    )

    if all_valid:
        coarse = valid_results[
            0
        ]

        fine = valid_results[
            1
        ]

        coarse_upper = float(
            coarse[
                "whole_payload_pointwise_upper_bound_m_s2_per_j"
            ]
        )

        fine_upper = float(
            fine[
                "whole_payload_pointwise_upper_bound_m_s2_per_j"
            ]
        )

        denominator = max(
            abs(
                coarse_upper
            ),
            abs(
                fine_upper
            ),
            1.0e-300,
        )

        grid_bound_relative_difference = (
            abs(
                fine_upper
                -
                coarse_upper
            )
            /
            denominator
        )

        grid_bound_preflight_stable = bool(
            grid_bound_relative_difference
            <
            GRID_BOUND_STABILITY_RELATIVE_TOL
        )

        fine_targets = (
            fine[
                "capacity_targets"
            ]
        )

        coarse_targets = (
            coarse[
                "capacity_targets"
            ]
        )

        exact_target_ruled_out_both = bool(
            fine_targets[
                str(
                    A12C_REFERENCE_CAPACITY_J
                )
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]

            and

            coarse_targets[
                str(
                    A12C_REFERENCE_CAPACITY_J
                )
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]
        )

        sub10j_ruled_out_both = bool(
            fine_targets[
                "10.0"
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]

            and

            coarse_targets[
                "10.0"
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]
        )

        sub100j_ruled_out_both = bool(
            fine_targets[
                "100.0"
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]

            and

            coarse_targets[
                "100.0"
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]
        )

        sub1kj_ruled_out_both = bool(
            fine_targets[
                "1000.0"
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]

            and

            coarse_targets[
                "1000.0"
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]
        )

        sub10kj_ruled_out_both = bool(
            fine_targets[
                "10000.0"
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]

            and

            coarse_targets[
                "10000.0"
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]
        )

        sub100kj_ruled_out_both = bool(
            fine_targets[
                "100000.0"
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]

            and

            coarse_targets[
                "100000.0"
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]
        )

        sub1mj_ruled_out_both = bool(
            fine_targets[
                "1000000.0"
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]

            and

            coarse_targets[
                "1000000.0"
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]
        )

        sub10mj_ruled_out_both = bool(
            fine_targets[
                "10000000.0"
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]

            and

            coarse_targets[
                "10000000.0"
            ][
                "ruled_out_by_pointwise_upper_bound"
            ]
        )

        required_for_original = (
            target_efficiency_m_s2_per_j(
                A12C_REFERENCE_CAPACITY_J
            )
        )

        original_response_gap_factor = (
            required_for_original
            /
            max(
                fine_upper,
                1.0e-300,
            )
        )

        fine_capacity_floor_j = float(
            fine[
                "certified_loaded_capacity_floor_j"
            ]
        )

    else:
        grid_bound_relative_difference = None
        grid_bound_preflight_stable = False
        exact_target_ruled_out_both = False
        sub10j_ruled_out_both = False
        sub100j_ruled_out_both = False
        sub1kj_ruled_out_both = False
        sub10kj_ruled_out_both = False
        sub100kj_ruled_out_both = False
        sub1mj_ruled_out_both = False
        sub10mj_ruled_out_both = False
        original_response_gap_factor = None
        fine_capacity_floor_j = None

    if (
        all_valid
        and
        exact_target_ruled_out_both
        and
        sub100j_ruled_out_both
        and
        grid_bound_preflight_stable
    ):
        decision = (
            "RED_SCOPED_A12D1R2B1_GRID_COMPLETE_AXISYMMETRIC_"
            "SOURCE_CELL_POINTWISE_CERTIFICATE_RULES_OUT_THE_"
            "FEW_JOULE_AND_SUB100J_1KEV_SOURCE_SHAPING_ROUTE_ON_"
            "BOTH_TESTED_GRIDS__THIS_IS_NOT_A_CONTINUUM_OR_PORTAL_NO_GO__"
            "PIVOT_LOW_CAPACITY_RESCUE_TO_BACKREACTION_STRUCTURE"
        )

        next_branch = (
            "032H17A12D1R3_MIXED_EB_F_DUAL_F_LOW_CAPACITY_RESCUE"
        )

    elif (
        all_valid
        and
        exact_target_ruled_out_both
        and
        original_response_gap_factor
        is not None
        and
        original_response_gap_factor
        >
        1000.0
    ):
        decision = (
            "RED_YELLOW_SCOPED_A12D1R2B1_EXACT_2P656859J_"
            "GRID_COMPLETE_SOURCE_SHAPING_REMAINS_EXCLUDED_BY_"
            "MORE_THAN_THREE_ORDERS_OF_MAGNITUDE_ON_THE_FINE_GRID__"
            "GRID_BOUND_NOT_YET_STABLE_ENOUGH_FOR_STRONGER_CAPACITY_TIERS__"
            "STRUCTURAL_PORTAL_RESCUE_NOW_HIGHER_VALUE_THAN_MORE_SOURCE_SHAPING"
        )

        next_branch = (
            "032H17A12D1R3_MIXED_EB_F_DUAL_F_LOW_CAPACITY_RESCUE"
        )

    elif (
        all_valid
        and
        not exact_target_ruled_out_both
    ):
        decision = (
            "YELLOW_POSITIVE_A12D1R2B1_GRID_COMPLETE_SOURCE_SPACE_"
            "REOPENS_MATHEMATICAL_HEADROOM_FOR_THE_2P656859J_1KEV_TARGET__"
            "DO_NOT_PIVOT__CONSTRUCT_THE_EXTREMAL_SOURCE_AND_TEST_WHOLE_PAYLOAD"
        )

        next_branch = (
            "032H17A12D1R2C_GRID_COMPLETE_EXTREMAL_SOURCE_CONSTRUCTION"
        )

    else:
        decision = (
            "YELLOW_A12D1R2B1_GRID_COMPLETE_CERTIFICATE_NUMERICALLY_"
            "INCONCLUSIVE__NO_PHYSICS_CLOSURE__REFINE_THE_DISCRETIZATION"
        )

        next_branch = (
            "032H17A12D1R2B2_GRID_CERTIFICATE_REFINEMENT"
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

        "portal_scale_ev":
            PORTAL_SCALE_EV,

        "grid_results":
            results,

        "all_grid_certificates_valid":
            all_valid,

        "grid_bound_relative_difference":
            grid_bound_relative_difference,

        "grid_bound_preflight_stable":
            grid_bound_preflight_stable,

        "a12c_2p656859j_ruled_out_on_both_grids":
            exact_target_ruled_out_both,

        "sub10j_ruled_out_on_both_grids":
            sub10j_ruled_out_both,

        "sub100j_ruled_out_on_both_grids":
            sub100j_ruled_out_both,

        "sub1kj_ruled_out_on_both_grids":
            sub1kj_ruled_out_both,

        "sub10kj_ruled_out_on_both_grids":
            sub10kj_ruled_out_both,

        "sub100kj_ruled_out_on_both_grids":
            sub100kj_ruled_out_both,

        "sub1mj_ruled_out_on_both_grids":
            sub1mj_ruled_out_both,

        "sub10mj_ruled_out_on_both_grids":
            sub10mj_ruled_out_both,

        "fine_grid_certified_loaded_capacity_floor_j":
            fine_capacity_floor_j,

        "a12c_reference_response_gap_factor_on_fine_grid":
            original_response_gap_factor,

        "continuous_source_space_exhausted":
            False,

        "nonaxisymmetric_source_space_exhausted":
            False,

        "all_source_supports_exhausted":
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

    scan_rows = []

    for result in results:
        row = {
            "grid_spacing_m":
                result[
                    "grid_spacing_m"
                ],

            "certificate_valid":
                result[
                    "certificate_valid"
                ],

            "source_dof_count":
                result[
                    "source_dof_count"
                ],

            "payload_certificate_point_count":
                result[
                    "payload_certificate_point_count"
                ],

            "energy_condition_number":
                result.get(
                    "energy_condition_number"
                ),

            "whole_payload_pointwise_upper_bound_m_s2_per_j":
                result.get(
                    "whole_payload_pointwise_upper_bound_m_s2_per_j"
                ),

            "certified_loaded_capacity_floor_j":
                result.get(
                    "certified_loaded_capacity_floor_j"
                ),

            "bottleneck_payload_rho_m":
                result.get(
                    "bottleneck_payload_rho_m"
                ),

            "bottleneck_payload_z_m":
                result.get(
                    "bottleneck_payload_z_m"
                ),

            "prior_r2b_bottleneck_local_upper_bound_m_s2_per_j":
                result.get(
                    "prior_r2b_bottleneck_local_upper_bound_m_s2_per_j"
                ),

            "grid_complete_upper_bound_over_r2b_76d_bound":
                result.get(
                    "grid_complete_upper_bound_over_r2b_76d_bound"
                ),
        }

        scan_rows.append(
            row
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

    print()
    print(
        "================================================================"
    )

    print(
        "R2B1 FINAL SCIENTIFIC RESULT"
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
        "ALL_GRID_CERTIFICATES_VALID="
        +
        str(
            all_valid
        )
    )

    print(
        "GRID_BOUND_RELATIVE_DIFFERENCE="
        +
        str(
            grid_bound_relative_difference
        )
    )

    print(
        "GRID_BOUND_PREFLIGHT_STABLE="
        +
        str(
            grid_bound_preflight_stable
        )
    )

    print(
        "A12C_2P656859J_RULED_OUT_ON_BOTH_GRIDS="
        +
        str(
            exact_target_ruled_out_both
        )
    )

    print(
        "SUB10J_RULED_OUT_ON_BOTH_GRIDS="
        +
        str(
            sub10j_ruled_out_both
        )
    )

    print(
        "SUB100J_RULED_OUT_ON_BOTH_GRIDS="
        +
        str(
            sub100j_ruled_out_both
        )
    )

    print(
        "SUB1KJ_RULED_OUT_ON_BOTH_GRIDS="
        +
        str(
            sub1kj_ruled_out_both
        )
    )

    print(
        "SUB10KJ_RULED_OUT_ON_BOTH_GRIDS="
        +
        str(
            sub10kj_ruled_out_both
        )
    )

    print(
        "SUB100KJ_RULED_OUT_ON_BOTH_GRIDS="
        +
        str(
            sub100kj_ruled_out_both
        )
    )

    print(
        "SUB1MJ_RULED_OUT_ON_BOTH_GRIDS="
        +
        str(
            sub1mj_ruled_out_both
        )
    )

    print(
        "SUB10MJ_RULED_OUT_ON_BOTH_GRIDS="
        +
        str(
            sub10mj_ruled_out_both
        )
    )

    print(
        "FINE_GRID_CERTIFIED_LOADED_CAPACITY_FLOOR_J="
        +
        str(
            fine_capacity_floor_j
        )
    )

    print(
        "A12C_REFERENCE_RESPONSE_GAP_FACTOR_FINE_GRID="
        +
        str(
            original_response_gap_factor
        )
    )

    print(
        "CONTINUOUS_SOURCE_SPACE_EXHAUSTED=False"
    )

    print(
        "NONAXISYMMETRIC_SOURCE_SPACE_EXHAUSTED=False"
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


if __name__ == "__main__":
    main()
