"""032H17A12D1R2 — loaded low-keV source-shape rescue."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from antigravity_research.agminer.hook17_f2_loaded_source_shape_rescue import (
    BRANCH,
    DOMAIN_CAPACITY_RELERR_PREFLIGHT_MAX,
    FEW_JOULE_TARGET_J,
    GRID_CAPACITY_RELERR_PREFLIGHT_MAX,
    PORTAL_LADDER_EV,
    PRIMARY_DENSITY_MODEL,
    REFINED_RESPONSE_GRID_M,
    ROBUSTNESS_DENSITY_MODEL,
    SOURCE_BASIS_COUNT,
    SUB100J_TARGET_J,
    SUB100KJ_TARGET_J,
    SUB10KJ_TARGET_J,
    SUB1KJ_TARGET_J,
    SUB1MJ_TARGET_J,
    VALIDATION_GRID_M,
    BROAD_RESPONSE_GRID_M,
    LARGER_RHO_MAX_M,
    LARGER_Z_MAX_M,
    LARGER_Z_MIN_M,
    build_response_problem,
    claim_policy_gate,
    optimize_response_problem,
    provenance_gate,
    r1_artifact,
    solve_source_coefficients,
    source_basis_gate,
)


def _candidate_capacity(
    optimization: dict[str, Any],
) -> float:
    result = (
        optimization[
            "best_result"
        ]
    )

    capacity = (
        result[
            "predicted_loaded_capacity_j"
        ]
    )

    if capacity is None:
        return math.inf

    return float(
        capacity
    )


def _validation_passes(
    rows: list[dict[str, Any]],
) -> bool:
    return bool(
        rows
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
            for row in rows
        )
    )


def _fine_capacity(
    rows: list[dict[str, Any]],
) -> float | None:
    if not _validation_passes(
        rows
    ):
        return None

    finest = min(
        rows,
        key=lambda row:
            float(
                row[
                    "grid_spacing_m"
                ]
            ),
    )

    return float(
        finest[
            "loaded_quadratic_capacity_j"
        ]
    )


def _scan_row(
    stage: str,
    portal_scale_ev: float,
    optimization: dict[str, Any],
    response: dict[str, Any],
) -> dict[str, Any]:
    signed = (
        optimization[
            "signed_lane"
        ]
    )

    nonnegative = (
        optimization[
            "nonnegative_lane"
        ]
    )

    best = (
        optimization[
            "best_result"
        ]
    )

    return {
        "stage":
            stage,

        "grid_spacing_m":
            response[
                "grid_spacing_m"
            ],

        "portal_scale_ev":
            portal_scale_ev,

        "portal_scale_kev":
            portal_scale_ev
            /
            1000.0,

        "z_max":
            response[
                "z_max"
            ],

        "retained_energy_rank":
            response[
                "retained_energy_rank"
            ],

        "discarded_near_null_dimension":
            response[
                "discarded_near_null_dimension"
            ],

        "energy_condition_number_retained":
            response[
                "energy_condition_number_retained"
            ],

        "signed_margin_m_s2_per_j":
            signed[
                "minimum_acceleration_per_loaded_joule_m_s2_per_j"
            ],

        "signed_predicted_capacity_j":
            signed[
                "predicted_loaded_capacity_j"
            ],

        "nonnegative_margin_m_s2_per_j":
            nonnegative[
                "minimum_acceleration_per_loaded_joule_m_s2_per_j"
            ],

        "nonnegative_predicted_capacity_j":
            nonnegative[
                "predicted_loaded_capacity_j"
            ],

        "best_lane":
            optimization[
                "best_lane"
            ],

        "best_predicted_capacity_j":
            best[
                "predicted_loaded_capacity_j"
            ],

        "physical_model_found":
            False,

        "complete_energy_established":
            False,
    }


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
        "032h17a12d1r2_hook17_f2_loaded_source_shape_rescue_summary.json"
    )

    scan_path = (
        data_dir
        /
        "032h17a12d1r2_hook17_f2_loaded_source_shape_rescue_scan.csv"
    )

    coefficient_path = (
        data_dir
        /
        "032h17a12d1r2_hook17_f2_loaded_source_shape_coefficients.csv"
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
        "SOURCE_BASIS_COUNT="
        +
        str(
            SOURCE_BASIS_COUNT
        )
    )

    print(
        "PRIMARY_GOAL=RECOVER_EXACT_1KEV_FEW_JOULE_BRANCH"
    )

    print(
        "BROAD_SOURCE_SHAPE_PORTAL_LADDER_BEGIN=True"
    )

    broad_results = {}
    scan_rows = []

    for index, portal_scale_ev in enumerate(
        PORTAL_LADDER_EV
    ):
        response = (
            build_response_problem(
                portal_scale_ev=
                    portal_scale_ev,

                h=
                    BROAD_RESPONSE_GRID_M,

                density_model=
                    PRIMARY_DENSITY_MODEL,
            )
        )

        optimization = (
            optimize_response_problem(
                response,
                effort="BROAD",
                deterministic_seed=
                    17000
                    +
                    index
                    *
                    101,
            )
        )

        broad_results[
            str(
                portal_scale_ev
            )
        ] = {
            "response":
                {
                    "portal_scale_ev":
                        response[
                            "portal_scale_ev"
                        ],

                    "grid_spacing_m":
                        response[
                            "grid_spacing_m"
                        ],

                    "z_max":
                        response[
                            "z_max"
                        ],

                    "retained_energy_rank":
                        response[
                            "retained_energy_rank"
                        ],

                    "discarded_near_null_dimension":
                        response[
                            "discarded_near_null_dimension"
                        ],

                    "energy_condition_number_retained":
                        response[
                            "energy_condition_number_retained"
                        ],
                },

            "optimization":
                optimization,
        }

        scan_rows.append(
            _scan_row(
                "BROAD_H0P125",
                portal_scale_ev,
                optimization,
                response,
            )
        )

        print(
            "BROAD_SCALE_EV="
            +
            str(
                portal_scale_ev
            )
            +
            " BEST_LANE="
            +
            str(
                optimization[
                    "best_lane"
                ]
            )
            +
            " PREDICTED_CAPACITY_J="
            +
            str(
                optimization[
                    "best_result"
                ][
                    "predicted_loaded_capacity_j"
                ]
            )
            +
            " SIGNED_J="
            +
            str(
                optimization[
                    "signed_lane"
                ][
                    "predicted_loaded_capacity_j"
                ]
            )
            +
            " SAME_SIGN_J="
            +
            str(
                optimization[
                    "nonnegative_lane"
                ][
                    "predicted_loaded_capacity_j"
                ]
            )
        )

    ranked_scales = sorted(
        PORTAL_LADDER_EV,
        key=lambda scale:
            _candidate_capacity(
                broad_results[
                    str(
                        scale
                    )
                ][
                    "optimization"
                ]
            ),
    )

    refine_scales = [
        1000.0,
    ]

    for scale in ranked_scales:
        if (
            math.isfinite(
                _candidate_capacity(
                    broad_results[
                        str(
                            scale
                        )
                    ][
                        "optimization"
                    ]
                )
            )
            and
            scale
            not in refine_scales
        ):
            refine_scales.append(
                scale
            )

        if len(
            refine_scales
        ) >= 4:
            break

    refined_results = {}

    print(
        "REFINED_SCALES_EV="
        +
        ",".join(
            str(
                value
            )
            for value in refine_scales
        )
    )

    for index, portal_scale_ev in enumerate(
        refine_scales
    ):
        response = (
            build_response_problem(
                portal_scale_ev=
                    portal_scale_ev,

                h=
                    REFINED_RESPONSE_GRID_M,

                density_model=
                    PRIMARY_DENSITY_MODEL,
            )
        )

        effort = (
            "EXACT_1KEV"
            if math.isclose(
                portal_scale_ev,
                1000.0,
                rel_tol=0.0,
                abs_tol=1.0e-12,
            )
            else
            "REFINED"
        )

        optimization = (
            optimize_response_problem(
                response,
                effort=effort,
                deterministic_seed=
                    27000
                    +
                    index
                    *
                    103,
            )
        )

        refined_results[
            str(
                portal_scale_ev
            )
        ] = {
            "response":
                {
                    "portal_scale_ev":
                        response[
                            "portal_scale_ev"
                        ],

                    "grid_spacing_m":
                        response[
                            "grid_spacing_m"
                        ],

                    "z_max":
                        response[
                            "z_max"
                        ],

                    "retained_energy_rank":
                        response[
                            "retained_energy_rank"
                        ],

                    "discarded_near_null_dimension":
                        response[
                            "discarded_near_null_dimension"
                        ],

                    "energy_condition_number_retained":
                        response[
                            "energy_condition_number_retained"
                        ],
                },

            "optimization":
                optimization,
        }

        scan_rows.append(
            _scan_row(
                "REFINED_H0P100",
                portal_scale_ev,
                optimization,
                response,
            )
        )

        print(
            "REFINED_SCALE_EV="
            +
            str(
                portal_scale_ev
            )
            +
            " EFFORT="
            +
            effort
            +
            " BEST_LANE="
            +
            str(
                optimization[
                    "best_lane"
                ]
            )
            +
            " PREDICTED_CAPACITY_J="
            +
            str(
                optimization[
                    "best_result"
                ][
                    "predicted_loaded_capacity_j"
                ]
            )
        )

    validation_targets = []

    exact_1kev_optimization = (
        refined_results[
            "1000.0"
        ][
            "optimization"
        ]
    )

    exact_1kev_best = (
        exact_1kev_optimization[
            "best_result"
        ]
    )

    if (
        exact_1kev_best[
            "predicted_loaded_capacity_j"
        ]
        is not None
    ):
        validation_targets.append(
            (
                "EXACT_1KEV",
                1000.0,
                exact_1kev_best,
            )
        )

    refined_ranked = sorted(
        (
            float(
                scale
            ),
            value[
                "optimization"
            ][
                "best_result"
            ],
        )
        for scale, value in refined_results.items()
        if value[
            "optimization"
        ][
            "best_result"
        ][
            "predicted_loaded_capacity_j"
        ]
        is not None
    )

    refined_ranked.sort(
        key=lambda item:
            float(
                item[
                    1
                ][
                    "predicted_loaded_capacity_j"
                ]
            )
    )

    for scale, result in refined_ranked:
        duplicate = bool(
            math.isclose(
                scale,
                1000.0,
                rel_tol=0.0,
                abs_tol=1.0e-12,
            )
        )

        if not duplicate:
            validation_targets.append(
                (
                    "BEST_REFINED",
                    scale,
                    result,
                )
            )

            break

    validations = {}

    for label, scale, optimization_result in validation_targets:
        coefficients = np.asarray(
            optimization_result[
                "source_coefficients"
            ],
            dtype=float,
        )

        rows = []

        for h in VALIDATION_GRID_M:
            direct = (
                solve_source_coefficients(
                    portal_scale_ev=
                        scale,

                    coefficients=
                        coefficients,

                    h=
                        h,

                    density_model=
                        PRIMARY_DENSITY_MODEL,
                )
            )

            rows.append(
                direct
            )

            print(
                "VALIDATION="
                +
                label
                +
                " SCALE_EV="
                +
                str(
                    scale
                )
                +
                " GRID_M="
                +
                str(
                    h
                )
                +
                " OUTWARD="
                +
                str(
                    direct[
                        "whole_payload_outward_sign"
                    ]
                )
                +
                " CAPACITY_J="
                +
                str(
                    direct.get(
                        "loaded_quadratic_capacity_j"
                    )
                )
            )

        validations[
            label
        ] = {
            "portal_scale_ev":
                scale,

            "optimization_result":
                optimization_result,

            "direct_grid_results":
                rows,

            "passes_all_three_grids":
                _validation_passes(
                    rows
                ),

            "finest_grid_capacity_j":
                _fine_capacity(
                    rows
                ),
        }

    best_validated_label = None
    best_validated_capacity = math.inf

    for label, result in validations.items():
        capacity = (
            result[
                "finest_grid_capacity_j"
            ]
        )

        if (
            capacity
            is not None
            and
            capacity
            <
            best_validated_capacity
        ):
            best_validated_label = (
                label
            )

            best_validated_capacity = float(
                capacity
            )

    convergence = None
    robustness = None

    if best_validated_label is not None:
        selected = (
            validations[
                best_validated_label
            ]
        )

        scale = float(
            selected[
                "portal_scale_ev"
            ]
        )

        coefficients = np.asarray(
            selected[
                "optimization_result"
            ][
                "source_coefficients"
            ]
        )

        medium = next(
            row
            for row in selected[
                "direct_grid_results"
            ]
            if math.isclose(
                row[
                    "grid_spacing_m"
                ],
                0.075,
                rel_tol=0.0,
                abs_tol=1.0e-12,
            )
        )

        fine = next(
            row
            for row in selected[
                "direct_grid_results"
            ]
            if math.isclose(
                row[
                    "grid_spacing_m"
                ],
                0.050,
                rel_tol=0.0,
                abs_tol=1.0e-12,
            )
        )

        larger_domain = (
            solve_source_coefficients(
                portal_scale_ev=
                    scale,

                coefficients=
                    coefficients,

                h=
                    0.075,

                density_model=
                    PRIMARY_DENSITY_MODEL,

                rho_max_m=
                    LARGER_RHO_MAX_M,

                z_min_m=
                    LARGER_Z_MIN_M,

                z_max_m=
                    LARGER_Z_MAX_M,
            )
        )

        robustness = (
            solve_source_coefficients(
                portal_scale_ev=
                    scale,

                coefficients=
                    coefficients,

                h=
                    0.075,

                density_model=
                    ROBUSTNESS_DENSITY_MODEL,
            )
        )

        if (
            medium[
                "whole_payload_outward_sign"
            ]
            and
            fine[
                "whole_payload_outward_sign"
            ]
            and
            larger_domain[
                "whole_payload_outward_sign"
            ]
        ):
            grid_relerr = (
                abs(
                    float(
                        fine[
                            "loaded_quadratic_capacity_j"
                        ]
                    )
                    -
                    float(
                        medium[
                            "loaded_quadratic_capacity_j"
                        ]
                    )
                )
                /
                float(
                    fine[
                        "loaded_quadratic_capacity_j"
                    ]
                )
            )

            domain_relerr = (
                abs(
                    float(
                        larger_domain[
                            "loaded_quadratic_capacity_j"
                        ]
                    )
                    -
                    float(
                        medium[
                            "loaded_quadratic_capacity_j"
                        ]
                    )
                )
                /
                float(
                    medium[
                        "loaded_quadratic_capacity_j"
                    ]
                )
            )

            numerical_preflight_pass = bool(
                grid_relerr
                <
                GRID_CAPACITY_RELERR_PREFLIGHT_MAX

                and

                domain_relerr
                <
                DOMAIN_CAPACITY_RELERR_PREFLIGHT_MAX
            )

        else:
            grid_relerr = None
            domain_relerr = None
            numerical_preflight_pass = False

        convergence = {
            "selected_label":
                best_validated_label,

            "portal_scale_ev":
                scale,

            "grid_capacity_relative_difference":
                grid_relerr,

            "domain_capacity_relative_difference":
                domain_relerr,

            "larger_domain_result":
                larger_domain,

            "numerical_preflight_pass":
                numerical_preflight_pass,

            "promotion_quality_precision":
                False,
        }

    exact_1kev_validated = bool(
        "EXACT_1KEV"
        in validations
        and
        validations[
            "EXACT_1KEV"
        ][
            "passes_all_three_grids"
        ]
    )

    exact_1kev_capacity = (
        validations.get(
            "EXACT_1KEV",
            {},
        ).get(
            "finest_grid_capacity_j"
        )
    )

    exact_1kev_under_10j = bool(
        exact_1kev_capacity
        is not None
        and
        exact_1kev_capacity
        <
        FEW_JOULE_TARGET_J
    )

    exact_1kev_under_100j = bool(
        exact_1kev_capacity
        is not None
        and
        exact_1kev_capacity
        <
        SUB100J_TARGET_J
    )

    exact_1kev_under_1kj = bool(
        exact_1kev_capacity
        is not None
        and
        exact_1kev_capacity
        <
        SUB1KJ_TARGET_J
    )

    exact_1kev_under_10kj = bool(
        exact_1kev_capacity
        is not None
        and
        exact_1kev_capacity
        <
        SUB10KJ_TARGET_J
    )

    any_validated = (
        best_validated_label
        is not None
    )

    best_under_100j = bool(
        any_validated
        and
        best_validated_capacity
        <
        SUB100J_TARGET_J
    )

    best_under_1kj = bool(
        any_validated
        and
        best_validated_capacity
        <
        SUB1KJ_TARGET_J
    )

    best_under_10kj = bool(
        any_validated
        and
        best_validated_capacity
        <
        SUB10KJ_TARGET_J
    )

    best_under_100kj = bool(
        any_validated
        and
        best_validated_capacity
        <
        SUB100KJ_TARGET_J
    )

    best_under_1mj = bool(
        any_validated
        and
        best_validated_capacity
        <
        SUB1MJ_TARGET_J
    )

    numerical_preflight_pass = bool(
        convergence is not None
        and
        convergence[
            "numerical_preflight_pass"
        ]
    )

    robustness_outward = bool(
        robustness is not None
        and
        robustness[
            "whole_payload_outward_sign"
        ]
    )

    if (
        exact_1kev_under_10j
        and
        numerical_preflight_pass
    ):
        decision = (
            "GREEN_SCOPED_A12D1R2_EXACT_1KEV_FEW_JOULE_"
            "STRONGLY_LOADED_SOURCE_SHAPE_RESCUE_FOUND__"
            "PRESERVE_AND_PROMOTE_INDEPENDENT_CONVERGENCE_AND_"
            "MICROSCOPIC_SOURCE_PHYSICALIZATION"
        )

        next_branch = (
            "032H17A12D1R2C_EXACT_1KEV_INDEPENDENT_SOLVER_"
            "HIGH_RESOLUTION_AND_SOURCE_PHYSICALIZATION"
        )

    elif (
        exact_1kev_under_100j
        and
        numerical_preflight_pass
    ):
        decision = (
            "GREEN_SCOPED_A12D1R2_EXACT_1KEV_SUB100J_"
            "STRONGLY_LOADED_RESCUE_FOUND__ORIGINAL_2P66J_NUMBER_"
            "NOT_PRESERVED_EXACTLY_BUT_FEW_TENS_OF_JOULES_CLASS_"
            "MECHANISM_SURVIVES"
        )

        next_branch = (
            "032H17A12D1R2C_EXACT_1KEV_HIGH_RESOLUTION_"
            "SOURCE_PHYSICALIZATION"
        )

    elif exact_1kev_under_10kj:
        decision = (
            "YELLOW_STRONG_A12D1R2_EXACT_1KEV_WHOLE_PAYLOAD_"
            "LOADED_SIGN_RESCUED_BUT_CAPACITY_REMAINS_ABOVE_100J__"
            "CONTINUE_ADJOINT_SOURCE_SHAPE_REFINEMENT_BEFORE_"
            "ABANDONING_FEW_JOULE_TARGET"
        )

        next_branch = (
            "032H17A12D1R2B_CONTINUOUS_ADJOINT_1KEV_"
            "SOURCE_SHAPE_RESCUE"
        )

    elif best_under_10kj:
        decision = (
            "YELLOW_STRONG_A12D1R2_LOW_KEV_SUB10KJ_"
            "LOADED_DESCENDANT_FOUND__EXACT_1KEV_NOT_YET_RESCUED__"
            "KEEP_FEW_JOULE_PROGRAM_ACTIVE_AND_PROMOTE_CONTINUOUS_"
            "1KEV_SOURCE_SHAPE_OPTIMIZATION"
        )

        next_branch = (
            "032H17A12D1R2B_CONTINUOUS_ADJOINT_1KEV_"
            "SOURCE_SHAPE_RESCUE"
        )

    elif best_under_100kj:
        decision = (
            "YELLOW_A12D1R2_SOURCE_SHAPING_IMPROVES_LOADED_F2_"
            "BUT_DOES_NOT_YET_RECOVER_LOW_JOULE_CLASS__EXPAND_"
            "CONTINUOUS_SOURCE_CONTROL_BEFORE_STRUCTURAL_PORTAL_PIVOT"
        )

        next_branch = (
            "032H17A12D1R2B_CONTINUOUS_ADJOINT_LOW_KEV_RESCUE"
        )

    elif best_under_1mj:
        decision = (
            "YELLOW_WEAK_A12D1R2_FINITE_BASIS_SOURCE_SHAPING_"
            "RETAINS_SUB1MJ_BRANCH_BUT_NOT_THE_FEW_JOULE_OUTLIER__"
            "ONE_CONTINUOUS_CONTROL_ATTEMPT_AUTHORIZED_BEFORE_FDUALF"
        )

        next_branch = (
            "032H17A12D1R2B_FINAL_CONTINUOUS_1KEV_RESCUE_ATTEMPT"
        )

    else:
        decision = (
            "RED_SCOPED_A12D1R2_FINITE_COMPACT_SOURCE_SHAPE_BASIS_"
            "DOES_NOT_RESCUE_LOW_KEV_F2_CAPACITY__DO_NOT_CLOSE_A12B__"
            "PROMOTE_STRUCTURALLY_DIFFERENT_MIXED_EB_TOPOLOGICAL_PORTAL"
        )

        next_branch = (
            "032H17A12D1R3_MIXED_EB_F_DUAL_F_LOW_CAPACITY_RESCUE"
        )

    coefficient_rows = []

    for scale_string, refined in refined_results.items():
        optimization = (
            refined[
                "optimization"
            ]
        )

        for lane_name in (
            "signed_lane",
            "nonnegative_lane",
        ):
            lane = (
                optimization[
                    lane_name
                ]
            )

            coefficients = (
                lane[
                    "source_coefficients"
                ]
            )

            labels = (
                lane[
                    "source_basis_labels"
                ]
            )

            for label, coefficient in zip(
                labels,
                coefficients,
            ):
                coefficient_rows.append(
                    {
                        "portal_scale_ev":
                            float(
                                scale_string
                            ),

                        "lane":
                            lane[
                                "lane"
                            ],

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

        "source_basis":
            source_basis_gate(),

        "portal_ladder_ev":
            list(
                PORTAL_LADDER_EV
            ),

        "broad_results":
            broad_results,

        "refined_results":
            refined_results,

        "validations":
            validations,

        "convergence":
            convergence,

        "robustness_polynomial_c1":
            robustness,

        "exact_1kev_direct_validation_pass":
            exact_1kev_validated,

        "exact_1kev_finest_capacity_j":
            exact_1kev_capacity,

        "exact_1kev_sub10j":
            exact_1kev_under_10j,

        "exact_1kev_sub100j":
            exact_1kev_under_100j,

        "exact_1kev_sub1kj":
            exact_1kev_under_1kj,

        "exact_1kev_sub10kj":
            exact_1kev_under_10kj,

        "best_validated_label":
            best_validated_label,

        "best_validated_capacity_j":
            (
                best_validated_capacity
                if any_validated
                else None
            ),

        "best_validated_sub100j":
            best_under_100j,

        "best_validated_sub1kj":
            best_under_1kj,

        "best_validated_sub10kj":
            best_under_10kj,

        "best_validated_sub100kj":
            best_under_100kj,

        "best_validated_sub1mj":
            best_under_1mj,

        "numerical_preflight_pass":
            numerical_preflight_pass,

        "robustness_polynomial_c1_outward":
            robustness_outward,

        "a12b_exact_massless_carrier_closed":
            False,

        "a12c_f2_metric_mechanism_closed":
            False,

        "all_source_shapes_closed":
            False,

        "continuous_source_shape_space_exhausted":
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
        "DECISION="
        +
        decision
    )

    print(
        "EXACT_1KEV_DIRECT_VALIDATION_PASS="
        +
        str(
            exact_1kev_validated
        )
    )

    print(
        "EXACT_1KEV_FINEST_CAPACITY_J="
        +
        str(
            exact_1kev_capacity
        )
    )

    print(
        "EXACT_1KEV_SUB10J="
        +
        str(
            exact_1kev_under_10j
        )
    )

    print(
        "EXACT_1KEV_SUB100J="
        +
        str(
            exact_1kev_under_100j
        )
    )

    print(
        "EXACT_1KEV_SUB1KJ="
        +
        str(
            exact_1kev_under_1kj
        )
    )

    print(
        "EXACT_1KEV_SUB10KJ="
        +
        str(
            exact_1kev_under_10kj
        )
    )

    if (
        "1000.0"
        in refined_results
    ):
        exact_refined = (
            refined_results[
                "1000.0"
            ][
                "optimization"
            ]
        )

        print(
            "EXACT_1KEV_BEST_LANE="
            +
            str(
                exact_refined[
                    "best_lane"
                ]
            )
        )

        print(
            "EXACT_1KEV_QUADRATIC_PREDICTED_CAPACITY_J="
            +
            str(
                exact_refined[
                    "best_result"
                ][
                    "predicted_loaded_capacity_j"
                ]
            )
        )

        print(
            "EXACT_1KEV_SIGNED_PREDICTED_CAPACITY_J="
            +
            str(
                exact_refined[
                    "signed_lane"
                ][
                    "predicted_loaded_capacity_j"
                ]
            )
        )

        print(
            "EXACT_1KEV_SAME_SIGN_PREDICTED_CAPACITY_J="
            +
            str(
                exact_refined[
                    "nonnegative_lane"
                ][
                    "predicted_loaded_capacity_j"
                ]
            )
        )

    print(
        "BEST_VALIDATED_LABEL="
        +
        str(
            best_validated_label
        )
    )

    print(
        "BEST_VALIDATED_CAPACITY_J="
        +
        str(
            (
                best_validated_capacity
                if any_validated
                else None
            )
        )
    )

    if best_validated_label is not None:
        best_validation = (
            validations[
                best_validated_label
            ]
        )

        fine_result = min(
            best_validation[
                "direct_grid_results"
            ],
            key=lambda row:
                float(
                    row[
                        "grid_spacing_m"
                    ]
                ),
        )

        print(
            "BEST_VALIDATED_PORTAL_SCALE_EV="
            +
            str(
                best_validation[
                    "portal_scale_ev"
                ]
            )
        )

        print(
            "BEST_VALIDATED_LANE="
            +
            str(
                best_validation[
                    "optimization_result"
                ][
                    "lane"
                ]
            )
        )

        print(
            "BEST_CANONICAL_FIELD_ENERGY_J="
            +
            str(
                fine_result[
                    "canonical_field_energy_j"
                ]
            )
        )

        print(
            "BEST_PAYLOAD_INTERACTION_ENERGY_J="
            +
            str(
                fine_result[
                    "payload_interaction_energy_j"
                ]
            )
        )

        print(
            "BEST_SOURCE_WORK_J="
            +
            str(
                fine_result[
                    "source_work_j"
                ]
            )
        )

        print(
            "BEST_SOURCE_WORK_RELERR="
            +
            str(
                fine_result[
                    "source_work_relative_error"
                ]
            )
        )

        print(
            "BEST_ABSOLUTE_SOURCE_RATIO_VS_A12C="
            +
            str(
                fine_result[
                    "absolute_source_ratio_vs_a12c"
                ]
            )
        )

        print(
            "BEST_NEGATIVE_SOURCE_L1_FRACTION="
            +
            str(
                fine_result[
                    "negative_source_l1_fraction"
                ]
            )
        )

        print(
            "BEST_SOURCE_HAS_COUNTER_CIRCULATING_REGIONS="
            +
            str(
                fine_result[
                    "source_has_counter_circulating_regions"
                ]
            )
        )

        print(
            "BEST_PAYLOAD_SIGMA_MAX="
            +
            str(
                fine_result[
                    "payload_sigma_max"
                ]
            )
        )

        print(
            "BEST_EXACT_PAYLOAD_CONFORMAL_SHIFT_J="
            +
            str(
                fine_result[
                    "exact_payload_conformal_shift_j"
                ]
            )
        )

        print(
            "BEST_PAYLOAD_MIN_ACCEL_M_S2="
            +
            str(
                fine_result[
                    "payload_local_acceleration_min_m_s2"
                ]
            )
        )

        print(
            "BEST_PAYLOAD_MAX_ACCEL_M_S2="
            +
            str(
                fine_result[
                    "payload_local_acceleration_max_m_s2"
                ]
            )
        )

    print(
        "NUMERICAL_PREFLIGHT_PASS="
        +
        str(
            numerical_preflight_pass
        )
    )

    if convergence is not None:
        print(
            "GRID_CAPACITY_RELERR="
            +
            str(
                convergence[
                    "grid_capacity_relative_difference"
                ]
            )
        )

        print(
            "DOMAIN_CAPACITY_RELERR="
            +
            str(
                convergence[
                    "domain_capacity_relative_difference"
                ]
            )
        )

    print(
        "ROBUSTNESS_POLYNOMIAL_C1_OUTWARD="
        +
        str(
            robustness_outward
        )
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
