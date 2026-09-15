"""032H17A12D1R1 — strongly loaded low-capacity F2 rescue run."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

from antigravity_research.agminer.hook17_f2_strong_payload_loading_rescue import (
    BROAD_PORTAL_SCALES_EV,
    BROAD_SCAN_GRID_M,
    INTERMEDIATE_GRID_M,
    LARGER_RHO_MAX_M,
    LARGER_Z_MAX_M,
    LARGER_Z_MIN_M,
    LOADED_DOMAIN_CAPACITY_RELERR_MAX,
    LOADED_GRID_CAPACITY_RELERR_MAX,
    LOADED_GRID_SOURCE_RELERR_MAX,
    LOW_CAPACITY_J,
    LOW_KJ_CAPACITY_J,
    PRIMARY_DENSITY_MODEL,
    PRODUCTION_GRID_M,
    PRODUCTION_RHO_MAX_M,
    PRODUCTION_Z_MAX_M,
    PRODUCTION_Z_MIN_M,
    REFERENCE_PORTAL_SCALE_EV,
    ROBUSTNESS_DENSITY_MODEL,
    STRICT_COMPLETE_OPERATING_TARGET_J,
    SUB_MJ_CAPACITY_J,
    a12c_artifact,
    claim_policy_gate,
    payload_density_model_gate,
    primary_peak_loading_gate,
    provenance_gate,
    solve_strong_payload_loading,
    unloaded_reconstruction_gate,
)


def _finite_capacity(
    row: dict[str, Any],
) -> bool:
    return bool(
        row.get(
            "normalizable_to_whole_payload_1g",
            False,
        )
        and
        row.get(
            "strict_whole_payload_1g_pass",
            False,
        )
        and
        row.get(
            "loaded_quadratic_capacity_j"
        )
        is not None
        and
        math.isfinite(
            float(
                row[
                    "loaded_quadratic_capacity_j"
                ]
            )
        )
    )


def _best(
    rows: list[dict[str, Any]],
) -> dict[str, Any] | None:
    survivors = [
        row
        for row in rows
        if _finite_capacity(
            row
        )
    ]

    if not survivors:
        return None

    return min(
        survivors,
        key=lambda row:
            float(
                row[
                    "loaded_quadratic_capacity_j"
                ]
            ),
    )


def _scan_row(
    stage: str,
    result: dict[str, Any],
) -> dict[str, Any]:
    return {
        "stage":
            stage,

        "grid_spacing_m":
            result[
                "grid_spacing_m"
            ],

        "portal_scale_ev":
            result[
                "portal_scale_ev"
            ],

        "portal_scale_kev":
            (
                result[
                    "portal_scale_ev"
                ]
                /
                1000.0
            ),

        "density_model":
            result[
                "density_model"
            ],

        "z_max":
            result[
                "z_max"
            ],

        "unit_source_payload_acceleration_min_m_s2":
            result[
                "unit_source_payload_acceleration_min_m_s2"
            ],

        "unit_source_payload_acceleration_max_m_s2":
            result[
                "unit_source_payload_acceleration_max_m_s2"
            ],

        "whole_payload_outward_sign":
            result[
                "unit_source_whole_payload_outward_sign"
            ],

        "normalizable_to_whole_payload_1g":
            result[
                "normalizable_to_whole_payload_1g"
            ],

        "canonical_field_energy_j":
            result.get(
                "canonical_field_energy_j"
            ),

        "payload_interaction_energy_j":
            result.get(
                "payload_interaction_energy_j"
            ),

        "loaded_quadratic_capacity_j":
            result.get(
                "loaded_quadratic_capacity_j"
            ),

        "source_work_j":
            result.get(
                "source_work_j"
            ),

        "source_work_relative_error":
            result.get(
                "source_work_relative_error"
            ),

        "integrated_canonical_source_ev_m":
            result.get(
                "integrated_canonical_source_ev_m"
            ),

        "integrated_source_ratio_vs_a12c":
            result.get(
                "integrated_source_ratio_vs_a12c"
            ),

        "payload_sigma_max":
            result.get(
                "payload_sigma_max"
            ),

        "exact_payload_conformal_shift_j":
            result.get(
                "exact_payload_conformal_shift_j"
            ),

        "strict_whole_payload_1g_pass":
            result.get(
                "strict_whole_payload_1g_pass",
                False,
            ),

        "loaded_capacity_below_100j":
            result.get(
                "loaded_capacity_below_100j",
                False,
            ),

        "loaded_capacity_below_10kj":
            result.get(
                "loaded_capacity_below_10kj",
                False,
            ),

        "loaded_capacity_below_1mj":
            result.get(
                "loaded_capacity_below_1mj",
                False,
            ),

        "loaded_capacity_strictly_below_10mj":
            result.get(
                "loaded_capacity_strictly_below_10mj",
                False,
            ),

        "complete_energy_established":
            False,
    }


def main() -> None:
    """Run independent reconstruction, strong-loading scan, and refinement."""

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
        "032h17a12d1r1_hook17_f2_strong_payload_loading_rescue_summary.json"
    )

    scan_path = (
        data_dir
        /
        "032h17a12d1r1_hook17_f2_strong_payload_loading_rescue_scan.csv"
    )

    provenance = (
        provenance_gate()
    )

    assert provenance[
        "pass"
    ] is True

    unloaded = (
        unloaded_reconstruction_gate()
    )

    assert unloaded[
        "pass"
    ] is True

    print(
        "UNLOADED_NEW_SOLVER_RECONSTRUCTION_PASS="
        +
        str(
            unloaded[
                "pass"
            ]
        )
    )

    print(
        "UNLOADED_RECONSTRUCTED_FIELD_ENERGY_J="
        +
        str(
            unloaded[
                "new_solver_result"
            ][
                "canonical_field_energy_j"
            ]
        )
    )

    print(
        "A12C_REFERENCE_FIELD_ENERGY_J="
        +
        str(
            unloaded[
                "a12c_reference_field_energy_j"
            ]
        )
    )

    print(
        "UNLOADED_FIELD_ENERGY_RELERR="
        +
        str(
            unloaded[
                "field_energy_relative_error"
            ]
        )
    )

    print(
        "UNLOADED_SOURCE_RELERR="
        +
        str(
            unloaded[
                "integrated_source_relative_error"
            ]
        )
    )

    scan_rows = []
    raw_results = []

    print(
        "BROAD_STRONG_LOADING_SCAN_BEGIN=True"
    )

    for scale_ev in BROAD_PORTAL_SCALES_EV:
        result = (
            solve_strong_payload_loading(
                h=BROAD_SCAN_GRID_M,
                portal_scale_ev=scale_ev,
                density_model=PRIMARY_DENSITY_MODEL,
                include_payload_loading=True,
            )
        )

        raw_results.append(
            result
        )

        scan_rows.append(
            _scan_row(
                "BROAD_H0P100",
                result,
            )
        )

        print(
            "BROAD_SCALE_EV="
            +
            str(
                scale_ev
            )
            +
            " OUTWARD="
            +
            str(
                result[
                    "unit_source_whole_payload_outward_sign"
                ]
            )
            +
            " CAPACITY_J="
            +
            str(
                result.get(
                    "loaded_quadratic_capacity_j"
                )
            )
        )

    broad_best = (
        _best(
            raw_results
        )
    )

    if broad_best is None:
        broad_best_scale_ev = None
        intermediate_best = None
        production_best = None

    else:
        broad_best_scale_ev = float(
            broad_best[
                "portal_scale_ev"
            ]
        )

        intermediate_scales = sorted(
            set(
                max(
                    100.0,
                    broad_best_scale_ev
                    +
                    offset_ev,
                )
                for offset_ev in (
                    -2000.0,
                    -1000.0,
                    0.0,
                    1000.0,
                    2000.0,
                    3000.0,
                    4000.0,
                )
            )
        )

        intermediate_results = []

        for scale_ev in intermediate_scales:
            result = (
                solve_strong_payload_loading(
                    h=INTERMEDIATE_GRID_M,
                    portal_scale_ev=scale_ev,
                    density_model=PRIMARY_DENSITY_MODEL,
                    include_payload_loading=True,
                )
            )

            intermediate_results.append(
                result
            )

            scan_rows.append(
                _scan_row(
                    "INTERMEDIATE_H0P075",
                    result,
                )
            )

            print(
                "INTERMEDIATE_SCALE_EV="
                +
                str(
                    scale_ev
                )
                +
                " OUTWARD="
                +
                str(
                    result[
                        "unit_source_whole_payload_outward_sign"
                    ]
                )
                +
                " CAPACITY_J="
                +
                str(
                    result.get(
                        "loaded_quadratic_capacity_j"
                    )
                )
            )

        intermediate_best = (
            _best(
                intermediate_results
            )
        )

        if intermediate_best is None:
            production_best = None

        else:
            intermediate_best_scale_ev = float(
                intermediate_best[
                    "portal_scale_ev"
                ]
            )

            production_scales = sorted(
                set(
                    max(
                        100.0,
                        intermediate_best_scale_ev
                        +
                        offset_ev,
                    )
                    for offset_ev in (
                        -1000.0,
                        0.0,
                        1000.0,
                        2000.0,
                        3000.0,
                    )
                )
            )

            production_results = []

            for scale_ev in production_scales:
                result = (
                    solve_strong_payload_loading(
                        h=PRODUCTION_GRID_M,
                        portal_scale_ev=scale_ev,
                        density_model=PRIMARY_DENSITY_MODEL,
                        include_payload_loading=True,
                    )
                )

                production_results.append(
                    result
                )

                scan_rows.append(
                    _scan_row(
                        "PRODUCTION_H0P050",
                        result,
                    )
                )

                print(
                    "PRODUCTION_SCALE_EV="
                    +
                    str(
                        scale_ev
                    )
                    +
                    " OUTWARD="
                    +
                    str(
                        result[
                            "unit_source_whole_payload_outward_sign"
                        ]
                    )
                    +
                    " CAPACITY_J="
                    +
                    str(
                        result.get(
                            "loaded_quadratic_capacity_j"
                        )
                    )
                )

            production_best = (
                _best(
                    production_results
                )
            )

    # Explicitly attack the exact 1-keV outlier at three resolutions.
    one_kev_results = []

    for h in (
        BROAD_SCAN_GRID_M,
        INTERMEDIATE_GRID_M,
        PRODUCTION_GRID_M,
    ):
        result = (
            solve_strong_payload_loading(
                h=h,
                portal_scale_ev=REFERENCE_PORTAL_SCALE_EV,
                density_model=PRIMARY_DENSITY_MODEL,
                include_payload_loading=True,
            )
        )

        one_kev_results.append(
            result
        )

        scan_rows.append(
            _scan_row(
                "ONE_KEV_RESOLUTION_AUDIT",
                result,
            )
        )

        print(
            "ONE_KEV_GRID_M="
            +
            str(
                h
            )
            +
            " OUTWARD="
            +
            str(
                result[
                    "unit_source_whole_payload_outward_sign"
                ]
            )
            +
            " UNIT_MIN_ACCEL="
            +
            str(
                result[
                    "unit_source_payload_acceleration_min_m_s2"
                ]
            )
        )

    one_kev_outward_all_grids = bool(
        all(
            result[
                "unit_source_whole_payload_outward_sign"
            ]
            for result in one_kev_results
        )
    )

    one_kev_sign_fail_all_grids = bool(
        all(
            not result[
                "unit_source_whole_payload_outward_sign"
            ]
            for result in one_kev_results
        )
    )

    convergence = None
    robustness = None

    if production_best is not None:
        best_scale_ev = float(
            production_best[
                "portal_scale_ev"
            ]
        )

        coarse_same_scale = (
            solve_strong_payload_loading(
                h=INTERMEDIATE_GRID_M,
                portal_scale_ev=best_scale_ev,
                density_model=PRIMARY_DENSITY_MODEL,
                include_payload_loading=True,
            )
        )

        larger_domain_same_scale = (
            solve_strong_payload_loading(
                h=INTERMEDIATE_GRID_M,
                portal_scale_ev=best_scale_ev,
                rho_max_m=LARGER_RHO_MAX_M,
                z_min_m=LARGER_Z_MIN_M,
                z_max_m=LARGER_Z_MAX_M,
                density_model=PRIMARY_DENSITY_MODEL,
                include_payload_loading=True,
            )
        )

        robustness = (
            solve_strong_payload_loading(
                h=INTERMEDIATE_GRID_M,
                portal_scale_ev=best_scale_ev,
                density_model=ROBUSTNESS_DENSITY_MODEL,
                include_payload_loading=True,
            )
        )

        scan_rows.append(
            _scan_row(
                "CONVERGENCE_COARSE_SAME_SCALE",
                coarse_same_scale,
            )
        )

        scan_rows.append(
            _scan_row(
                "CONVERGENCE_LARGER_DOMAIN",
                larger_domain_same_scale,
            )
        )

        scan_rows.append(
            _scan_row(
                "ROBUSTNESS_POLYNOMIAL_C1",
                robustness,
            )
        )

        if (
            _finite_capacity(
                coarse_same_scale
            )
            and
            _finite_capacity(
                larger_domain_same_scale
            )
        ):
            grid_capacity_relerr = (
                abs(
                    float(
                        production_best[
                            "loaded_quadratic_capacity_j"
                        ]
                    )
                    -
                    float(
                        coarse_same_scale[
                            "loaded_quadratic_capacity_j"
                        ]
                    )
                )
                /
                float(
                    production_best[
                        "loaded_quadratic_capacity_j"
                    ]
                )
            )

            grid_source_relerr = (
                abs(
                    float(
                        production_best[
                            "integrated_canonical_source_ev_m"
                        ]
                    )
                    -
                    float(
                        coarse_same_scale[
                            "integrated_canonical_source_ev_m"
                        ]
                    )
                )
                /
                float(
                    production_best[
                        "integrated_canonical_source_ev_m"
                    ]
                )
            )

            domain_capacity_relerr = (
                abs(
                    float(
                        coarse_same_scale[
                            "loaded_quadratic_capacity_j"
                        ]
                    )
                    -
                    float(
                        larger_domain_same_scale[
                            "loaded_quadratic_capacity_j"
                        ]
                    )
                )
                /
                float(
                    coarse_same_scale[
                        "loaded_quadratic_capacity_j"
                    ]
                )
            )

            numerical_preflight_pass = bool(
                grid_capacity_relerr
                <
                LOADED_GRID_CAPACITY_RELERR_MAX

                and

                grid_source_relerr
                <
                LOADED_GRID_SOURCE_RELERR_MAX

                and

                domain_capacity_relerr
                <
                LOADED_DOMAIN_CAPACITY_RELERR_MAX
            )

            convergence = {
                "production_grid_m":
                    PRODUCTION_GRID_M,

                "coarse_grid_m":
                    INTERMEDIATE_GRID_M,

                "best_scale_ev":
                    best_scale_ev,

                "grid_capacity_relative_difference":
                    grid_capacity_relerr,

                "grid_source_relative_difference":
                    grid_source_relerr,

                "domain_capacity_relative_difference":
                    domain_capacity_relerr,

                "numerical_preflight_pass":
                    numerical_preflight_pass,

                "promotion_quality_precision":
                    False,
            }

        else:
            convergence = {
                "best_scale_ev":
                    best_scale_ev,

                "numerical_preflight_pass":
                    False,

                "reason":
                    "SAME_SCALE_COARSE_OR_DOMAIN_SOLVE_LOST_WHOLE_PAYLOAD_SIGN",

                "promotion_quality_precision":
                    False,
            }

    if production_best is None:
        best_capacity_j = None
        best_scale_ev = None
        loaded_sub10mj_survivor = False
        loaded_sub1mj_survivor = False
        loaded_sub10kj_survivor = False
        loaded_sub100j_survivor = False

    else:
        best_capacity_j = float(
            production_best[
                "loaded_quadratic_capacity_j"
            ]
        )

        best_scale_ev = float(
            production_best[
                "portal_scale_ev"
            ]
        )

        loaded_sub10mj_survivor = bool(
            best_capacity_j
            <
            STRICT_COMPLETE_OPERATING_TARGET_J
        )

        loaded_sub1mj_survivor = bool(
            best_capacity_j
            <
            SUB_MJ_CAPACITY_J
        )

        loaded_sub10kj_survivor = bool(
            best_capacity_j
            <
            LOW_KJ_CAPACITY_J
        )

        loaded_sub100j_survivor = bool(
            best_capacity_j
            <
            LOW_CAPACITY_J
        )

    numerical_preflight_pass = bool(
        convergence is not None
        and
        convergence.get(
            "numerical_preflight_pass",
            False,
        )
    )

    robustness_outward = bool(
        robustness is not None
        and
        robustness[
            "unit_source_whole_payload_outward_sign"
        ]
    )

    if (
        loaded_sub100j_survivor
        and
        numerical_preflight_pass
        and
        robustness_outward
    ):
        decision = (
            "GREEN_SCOPED_A12D1R1_STRONGLY_LOADED_F2_"
            "SUB100J_CAPACITY_SURVIVES_PAYLOAD_BACKREACTION_PREFLIGHT__"
            "PRESERVE_LOW_CAPACITY_BACKBONE_AND_RETURN_TO_SOURCE_PHYSICALIZATION"
        )

        next_branch = (
            "A12_SOURCE_PHYSICALIZATION_ON_STRONGLY_LOADED_KERNEL"
        )

    elif (
        loaded_sub10mj_survivor
        and
        one_kev_sign_fail_all_grids
    ):
        decision = (
            "YELLOW_SCOPED_A12D1R1_EXACT_1KEV_FEW_JOULE_"
            "DESCENDANT_LOSES_WHOLE_PAYLOAD_OUTWARD_SIGN_UNDER_"
            "SAME_ACTION_PAYLOAD_LOADING__BUT_A_NEARBY_STRONGLY_"
            "LOADED_SUB10MJ_CAPACITY_BRANCH_SURVIVES__PROMOTE_"
            "LOADING_AWARE_SOURCE_SHAPE_RESCUE_BEFORE_ABANDONING_F2"
        )

        next_branch = (
            "032H17A12D1R2_LOADING_AWARE_1KEV_AND_LOW_KEV_"
            "SOURCE_SHAPE_RESCUE"
        )

    elif loaded_sub10mj_survivor:
        decision = (
            "YELLOW_SCOPED_A12D1R1_STRONGLY_LOADED_F2_"
            "SUB10MJ_CAPACITY_SURVIVES_BUT_NUMERICAL_OR_"
            "ONE_KEV_STATUS_REQUIRES_REFINEMENT"
        )

        next_branch = (
            "032H17A12D1R1R_NUMERICAL_REFINEMENT"
        )

    else:
        decision = (
            "RED_SCOPED_A12D1R1_TESTED_STRONGLY_LOADED_"
            "MAGNETOSTATIC_F2_RESCUE_HAS_NO_SUB10MJ_WHOLE_PAYLOAD_"
            "SURVIVOR__PROMOTE_STRUCTURALLY_DIFFERENT_TOPOLOGICAL_PORTAL"
        )

        next_branch = (
            "032H17A12D1R3_MIXED_EB_TOPOLOGICAL_F_DUAL_F_RESCUE"
        )

    a12c = (
        a12c_artifact()
    )

    a12c_production = (
        a12c[
            "massless_f2_finite_payload_bvp"
        ][
            "production"
        ]
    )

    summary = {
        "branch":
            "032H17A12D1R1",

        "decision":
            decision,

        "provenance":
            provenance,

        "claim_policy":
            claim_policy_gate(),

        "payload_density_model":
            payload_density_model_gate(),

        "primary_1kev_peak_loading":
            primary_peak_loading_gate(
                REFERENCE_PORTAL_SCALE_EV
            ),

        "unloaded_independent_reconstruction":
            unloaded,

        "a12c_reference":
            {
                "portal_scale_ev":
                    float(
                        a12c_production[
                            "reference_portal_scale_ev"
                        ]
                    ),

                "field_energy_j":
                    float(
                        a12c_production[
                            "field_energy_j"
                        ]
                    ),

                "integrated_canonical_source_ev_m":
                    float(
                        a12c_production[
                            "integrated_canonical_source_ev_m"
                        ]
                    ),

                "payload_sigma_max":
                    float(
                        a12c_production[
                            "payload_sigma_max"
                        ]
                    ),

                "loaded_matter_backreaction_included":
                    bool(
                        a12c_production[
                            "loaded_matter_backreaction_included"
                        ]
                    ),
            },

        "one_kev_resolution_audit":
            {
                "results":
                    one_kev_results,

                "whole_payload_outward_at_all_tested_grids":
                    one_kev_outward_all_grids,

                "whole_payload_sign_fail_at_all_tested_grids":
                    one_kev_sign_fail_all_grids,
            },

        "broad_best":
            broad_best,

        "intermediate_best":
            intermediate_best,

        "production_best":
            production_best,

        "convergence":
            convergence,

        "robustness_polynomial_c1":
            robustness,

        "strongly_loaded_whole_payload_sub10mj_capacity_survivor":
            loaded_sub10mj_survivor,

        "strongly_loaded_whole_payload_sub1mj_capacity_survivor":
            loaded_sub1mj_survivor,

        "strongly_loaded_whole_payload_sub10kj_capacity_survivor":
            loaded_sub10kj_survivor,

        "strongly_loaded_whole_payload_sub100j_capacity_survivor":
            loaded_sub100j_survivor,

        "numerical_preflight_pass":
            numerical_preflight_pass,

        "exact_1kev_loaded_descendant_closed_globally":
            False,

        "exact_1kev_loaded_descendant_sign_failed_in_declared_payload_model":
            one_kev_sign_fail_all_grids,

        "a12b_exact_massless_carrier_closed":
            False,

        "a12c_f2_metric_mechanism_closed":
            False,

        "all_loading_aware_source_shapes_closed":
            False,

        "mixed_eb_topological_portal_closed":
            False,

        "complete_source_loaded_same_action_solution":
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

    fieldnames = list(
        scan_rows[
            0
        ].keys()
    )

    with scan_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(
            scan_rows
        )

    print()
    print(
        "BRANCH="
        +
        summary[
            "branch"
        ]
    )

    print(
        "DECISION="
        +
        summary[
            "decision"
        ]
    )

    print(
        "PRIMARY_1KEV_PEAK_Z="
        +
        str(
            summary[
                "primary_1kev_peak_loading"
            ][
                "peak_z"
            ]
        )
    )

    print(
        "ONE_KEV_OUTWARD_ALL_GRIDS="
        +
        str(
            one_kev_outward_all_grids
        )
    )

    print(
        "ONE_KEV_SIGN_FAIL_ALL_GRIDS="
        +
        str(
            one_kev_sign_fail_all_grids
        )
    )

    if production_best is not None:
        print(
            "BEST_LOADED_PORTAL_SCALE_EV="
            +
            str(
                production_best[
                    "portal_scale_ev"
                ]
            )
        )

        print(
            "BEST_LOADED_PORTAL_SCALE_KEV="
            +
            str(
                float(
                    production_best[
                        "portal_scale_ev"
                    ]
                )
                /
                1000.0
            )
        )

        print(
            "BEST_CANONICAL_FIELD_ENERGY_J="
            +
            str(
                production_best[
                    "canonical_field_energy_j"
                ]
            )
        )

        print(
            "BEST_PAYLOAD_INTERACTION_ENERGY_J="
            +
            str(
                production_best[
                    "payload_interaction_energy_j"
                ]
            )
        )

        print(
            "BEST_EXACT_PAYLOAD_CONFORMAL_SHIFT_J="
            +
            str(
                production_best[
                    "exact_payload_conformal_shift_j"
                ]
            )
        )

        print(
            "BEST_LOADED_QUADRATIC_CAPACITY_J="
            +
            str(
                production_best[
                    "loaded_quadratic_capacity_j"
                ]
            )
        )

        print(
            "BEST_SOURCE_WORK_J="
            +
            str(
                production_best[
                    "source_work_j"
                ]
            )
        )

        print(
            "BEST_SOURCE_WORK_RELERR="
            +
            str(
                production_best[
                    "source_work_relative_error"
                ]
            )
        )

        print(
            "BEST_INTEGRATED_SOURCE_EV_M="
            +
            str(
                production_best[
                    "integrated_canonical_source_ev_m"
                ]
            )
        )

        print(
            "BEST_SOURCE_RATIO_VS_A12C="
            +
            str(
                production_best[
                    "integrated_source_ratio_vs_a12c"
                ]
            )
        )

        print(
            "BEST_PAYLOAD_SIGMA_MAX="
            +
            str(
                production_best[
                    "payload_sigma_max"
                ]
            )
        )

        print(
            "BEST_SMALL_SIGMA_SELF_CONSISTENT="
            +
            str(
                production_best[
                    "small_sigma_expansion_self_consistent"
                ]
            )
        )

        print(
            "BEST_PAYLOAD_MIN_ACCEL_M_S2="
            +
            str(
                production_best[
                    "payload_local_acceleration_min_m_s2"
                ]
            )
        )

        print(
            "BEST_PAYLOAD_MAX_ACCEL_M_S2="
            +
            str(
                production_best[
                    "payload_local_acceleration_max_m_s2"
                ]
            )
        )

        print(
            "BEST_PAYLOAD_COM_ACCEL_M_S2="
            +
            str(
                production_best[
                    "payload_com_acceleration_m_s2"
                ]
            )
        )

    else:
        print(
            "BEST_LOADED_PORTAL_SCALE_EV=None"
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
                convergence.get(
                    "grid_capacity_relative_difference"
                )
            )
        )

        print(
            "GRID_SOURCE_RELERR="
            +
            str(
                convergence.get(
                    "grid_source_relative_difference"
                )
            )
        )

        print(
            "DOMAIN_CAPACITY_RELERR="
            +
            str(
                convergence.get(
                    "domain_capacity_relative_difference"
                )
            )
        )

    print(
        "ROBUSTNESS_POLYNOMIAL_C1_OUTWARD="
        +
        str(
            robustness_outward
        )
    )

    if (
        robustness is not None
        and
        robustness.get(
            "loaded_quadratic_capacity_j"
        )
        is not None
    ):
        print(
            "ROBUSTNESS_POLYNOMIAL_C1_CAPACITY_J="
            +
            str(
                robustness[
                    "loaded_quadratic_capacity_j"
                ]
            )
        )

    print(
        "STRONGLY_LOADED_SUB100J_CAPACITY_SURVIVOR="
        +
        str(
            loaded_sub100j_survivor
        )
    )

    print(
        "STRONGLY_LOADED_SUB10KJ_CAPACITY_SURVIVOR="
        +
        str(
            loaded_sub10kj_survivor
        )
    )

    print(
        "STRONGLY_LOADED_SUB1MJ_CAPACITY_SURVIVOR="
        +
        str(
            loaded_sub1mj_survivor
        )
    )

    print(
        "STRONGLY_LOADED_SUB10MJ_CAPACITY_SURVIVOR="
        +
        str(
            loaded_sub10mj_survivor
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
        summary[
            "next"
        ]
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
