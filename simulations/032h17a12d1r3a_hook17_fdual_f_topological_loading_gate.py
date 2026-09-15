"""032H17A12D1R3A — execute topological F·Fdual same-action rescue gate."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_topological_loading_gate import (
    BRANCH,
    r3a_summary,
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
        "032h17a12d1r3a_hook17_fdual_f_topological_loading_summary.json"
    )

    atlas_path = (
        data_dir
        /
        "032h17a12d1r3a_hook17_fdual_f_rescue_portal_atlas.csv"
    )

    summary = (
        r3a_summary()
    )

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

    atlas = (
        summary[
            "rescue_portal_atlas"
        ]
    )

    with atlas_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(
                atlas[
                    0
                ].keys()
            ),
        )

        writer.writeheader()

        writer.writerows(
            atlas
        )

    variation = (
        summary[
            "same_action_variation"
        ]
    )

    theorem = (
        summary[
            "affine_bulk_cancellation_theorem"
        ]
    )

    capacity = (
        summary[
            "ideal_a12c_capacity_equivalence"
        ]
    )

    loading = (
        summary[
            "loading_structure"
        ]
    )

    interface = (
        summary[
            "interface_prefight"
        ]
    )

    parity = (
        summary[
            "parity_cp"
        ]
    )

    health = (
        summary[
            "health_and_ward"
        ]
    )

    print(
        "BRANCH="
        +
        BRANCH
    )

    print()
    print(
        "================================================================"
    )
    print(
        "SAME-ACTION TOPOLOGICAL VARIATION"
    )
    print(
        "================================================================"
    )

    print(
        "PORTAL_INVARIANT="
        +
        variation[
            "portal_invariant"
        ]
    )

    print(
        "SIGMA="
        +
        variation[
            "sigma"
        ]
    )

    print(
        "DELTA_P="
        +
        variation[
            "delta_P"
        ]
    )

    print(
        "DELTA_SIGMA="
        +
        variation[
            "delta_sigma"
        ]
    )

    print(
        "SAME_ACTION_EQUATION="
        +
        variation[
            "schematic_same_action_equation"
        ]
    )

    print(
        "LEADING_CONSTANT_TRACE_BULK_LOADING_ZERO="
        +
        str(
            variation[
                "leading_constant_trace_bulk_loading_zero"
            ]
        )
    )

    print(
        "EXACT_CONSTANT_TRACE_BULK_LOADING_ZERO="
        +
        str(
            variation[
                "exact_constant_trace_bulk_loading_zero"
            ]
        )
    )

    print()
    print(
        "================================================================"
    )
    print(
        "AFFINE PORTAL UNIQUENESS"
    )
    print(
        "================================================================"
    )

    print(
        "LINEAR_P_UNIQUE_NONTRIVIAL_LOCAL_fP_BULK_CANCELLATION="
        +
        str(
            theorem[
                "linear_P_unique_nontrivial_local_fP_bulk_cancellation"
            ]
        )
    )

    print(
        "PARITY_EVEN_NONTRIVIAL_ANALYTIC_fP_CAN_BE_AFFINE="
        +
        str(
            theorem[
                "nontrivial_analytic_parity_even_fP_can_be_affine"
            ]
        )
    )

    print(
        "P_SQUARED_PRESERVES_BULK_CANCELLATION="
        +
        str(
            theorem[
                "P_squared_preserves_bulk_cancellation"
            ]
        )
    )

    print()
    print(
        "================================================================"
    )
    print(
        "IDEAL A12C CAPACITY PRESERVATION"
    )
    print(
        "================================================================"
    )

    print(
        "A12C_REFERENCE_FIELD_ENERGY_J="
        +
        str(
            capacity[
                "a12c_reference_field_energy_j"
            ]
        )
    )

    print(
        "MIRROR_E_OVER_BA="
        +
        str(
            capacity[
                "mirror_E_over_BA"
            ]
        )
    )

    print(
        "MIRROR_B_OVER_BA="
        +
        str(
            capacity[
                "mirror_B_over_BA"
            ]
        )
    )

    print(
        "MIRROR_SIGMA_OVER_A12C_SIGMA="
        +
        str(
            capacity[
                "mirror_sigma_over_a12c_sigma"
            ]
        )
    )

    print(
        "MIRROR_CANONICAL_ENERGY_OVER_A12C_ENERGY="
        +
        str(
            capacity[
                "mirror_canonical_energy_over_a12c_energy"
            ]
        )
    )

    print(
        "IDEAL_MIXED_EB_FIELD_ENERGY_J="
        +
        str(
            capacity[
                "ideal_mixed_EB_field_energy_j"
            ]
        )
    )

    print(
        "IDEAL_CAPACITY_EXACTLY_EQUAL_TO_A12C="
        +
        str(
            capacity[
                "ideal_capacity_exactly_equal_to_a12c"
            ]
        )
    )

    print(
        "PAYLOAD_CONFORMAL_REST_SHIFT_UPPER_J="
        +
        str(
            capacity[
                "payload_rest_energy_conformal_shift_upper_j"
            ]
        )
    )

    print(
        "LOCAL_ELECTROSTATIC_MIRROR_INTEGRABLE_IN_PAYLOAD="
        +
        str(
            capacity[
                "local_electrostatic_mirror_integrable_in_payload_region"
            ]
        )
    )

    print(
        "GLOBAL_MIRROR_FIELD_SOLUTION_ESTABLISHED="
        +
        str(
            capacity[
                "global_mirror_field_solution_established"
            ]
        )
    )

    print()
    print(
        "================================================================"
    )
    print(
        "BULK LOADING COMPARISON"
    )
    print(
        "================================================================"
    )

    print(
        "F2_AVERAGE_BULK_LOADING_EPSILON="
        +
        str(
            loading[
                "f2_average_bulk_loading_epsilon"
            ]
        )
    )

    print(
        "F2_PEAK_BULK_LOADING_EPSILON="
        +
        str(
            loading[
                "f2_peak_bulk_loading_epsilon"
            ]
        )
    )

    print(
        "FDUALF_BETA_AVERAGE_MAGNITUDE="
        +
        str(
            loading[
                "topological_beta_average_magnitude"
            ]
        )
    )

    print(
        "FDUALF_BETA_PEAK_MAGNITUDE="
        +
        str(
            loading[
                "topological_beta_peak_magnitude"
            ]
        )
    )

    print(
        "FDUALF_LEADING_UNIFORM_BULK_LOADING_ZERO="
        +
        str(
            loading[
                "leading_uniform_bulk_loading_exactly_zero"
            ]
        )
    )

    print(
        "FDUALF_EXACT_NONLINEAR_BULK_PRINCIPAL_PROXY_PEAK="
        +
        str(
            loading[
                "exact_uniform_bulk_nonlinear_principal_proxy_peak"
            ]
        )
    )

    print(
        "FDUALF_NONLINEAR_BULK_PROXY_PASS="
        +
        str(
            loading[
                "nonlinear_bulk_proxy_pass"
            ]
        )
    )

    print(
        "F2_TO_FDUALF_RESIDUAL_BULK_SUPPRESSION_FACTOR="
        +
        str(
            loading[
                "f2_bulk_vs_topological_residual_suppression_factor"
            ]
        )
    )

    print()
    print(
        "================================================================"
    )
    print(
        "FINITE DENSITY-GRADIENT / INTERFACE PREFLIGHT"
    )
    print(
        "================================================================"
    )

    print(
        "INTERFACE_BETA_AVERAGE_MAGNITUDE="
        +
        str(
            interface[
                "average_beta_magnitude"
            ]
        )
    )

    print(
        "INTERFACE_BETA_PEAK_MAGNITUDE="
        +
        str(
            interface[
                "peak_beta_magnitude"
            ]
        )
    )

    print(
        "POSITIVE_SIGMA_SELECTS_FAVORABLE_INTERFACE_SIGN="
        +
        str(
            interface[
                "positive_sigma_and_nonrelativistic_T_select_favorable_sign"
            ]
        )
    )

    print(
        "PLANAR_INTERFACE_FAVORABLE_FACTOR_AVERAGE="
        +
        str(
            interface[
                "average_favorable_local_energy_density_factor"
            ]
        )
    )

    print(
        "PLANAR_INTERFACE_FAVORABLE_FACTOR_PEAK="
        +
        str(
            interface[
                "peak_favorable_local_energy_density_factor"
            ]
        )
    )

    print(
        "PLANAR_INTERFACE_UNFAVORABLE_FACTOR_PEAK="
        +
        str(
            interface[
                "peak_unfavorable_local_energy_density_factor"
            ]
        )
    )

    print(
        "NAIVE_A12C_TIMES_FAVORABLE_AVERAGE_INTERFACE_FACTOR_J="
        +
        str(
            interface[
                "naive_if_favorable_factor_applied_to_entire_a12c_field_average_j"
            ]
        )
    )

    print(
        "NAIVE_A12C_TIMES_FAVORABLE_PEAK_INTERFACE_FACTOR_J="
        +
        str(
            interface[
                "naive_if_favorable_factor_applied_to_entire_a12c_field_peak_j"
            ]
        )
    )

    print(
        "INTERFACE_HEURISTIC_IS_RIGOROUS_GLOBAL_BOUND="
        +
        str(
            interface[
                "heuristic_global_energy_is_rigorous_bound"
            ]
        )
    )

    print(
        "P_NODE_OR_POLARIZATION_ROTATION_IN_DENSITY_GRADIENT_LAYER_OPEN="
        +
        str(
            interface[
                "P_node_or_polarization_rotation_in_density_gradient_layer_is_open"
            ]
        )
    )

    print()
    print(
        "================================================================"
    )
    print(
        "PARITY / HEALTH"
    )
    print(
        "================================================================"
    )

    print(
        "BARE_LINEAR_P_PRESERVES_PARITY="
        +
        str(
            parity[
                "bare_linear_P_metric_preserves_parity"
            ]
        )
    )

    print(
        "BARE_LINEAR_P_PRESERVES_CP="
        +
        str(
            parity[
                "bare_linear_P_metric_preserves_CP"
            ]
        )
    )

    print(
        "PARITY_REPAIR_REQUIRES_EXTRA_ODD_STRUCTURE="
        +
        str(
            parity[
                "repair_requires_additional_parity_odd_structure"
            ]
        )
    )

    print(
        "GAUGE_INVARIANT="
        +
        str(
            health[
                "portal_is_gauge_invariant"
            ]
        )
    )

    print(
        "MATTER_INDUCED_CURRENT_IDENTICALLY_CONSERVED="
        +
        str(
            health[
                "matter_induced_current_identically_conserved"
            ]
        )
    )

    print(
        "FIELD_EQUATIONS_SECOND_ORDER="
        +
        str(
            health[
                "field_equations_second_order"
            ]
        )
    )

    print(
        "FULL_INTERACTING_HYPERBOLICITY_CERTIFIED="
        +
        str(
            health[
                "full_interacting_hyperbolicity_certified"
            ]
        )
    )

    print()
    print(
        "================================================================"
    )
    print(
        "R3A FINAL SCIENTIFIC RESULT"
    )
    print(
        "================================================================"
    )

    print(
        "DECISION="
        +
        summary[
            "decision"
        ]
    )

    print(
        "STRUCTURAL_RESCUE_SURVIVES_CHEAP_GATE="
        +
        str(
            summary[
                "structural_rescue_survives_cheap_gate"
            ]
        )
    )

    print(
        "DOMINANT_REMAINING_GATE="
        +
        summary[
            "dominant_remaining_gate"
        ]
    )

    print(
        "R3B_AUTHORIZED="
        +
        str(
            summary[
                "r3b_authorized"
            ]
        )
    )

    print(
        "FULL_LOADED_EB_BVP_AUTHORIZED_IMMEDIATELY="
        +
        str(
            summary[
                "full_loaded_EB_BVP_authorized_immediately"
            ]
        )
    )

    print(
        "A12B_CARRIER_CLOSED=False"
    )

    print(
        "A12C_LOW_CAPACITY_CLUE_DISCARDED=False"
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
        "ATLAS_PATH="
        +
        str(
            atlas_path
        )
    )


if __name__ == "__main__":
    main()
