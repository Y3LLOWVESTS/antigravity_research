"""032V26E1B0 — pure-j0 frame provenance / failure-memory gate."""

from __future__ import annotations

import json
from pathlib import Path

from antigravity_research.agminer.v26e1b0_pure_j0_provenance_collision import (
    inherited_v19r6_failure_memory,
    offstate_two_scalar_force_gate,
    pure_j0_operator_gate,
    source_operator_provenance_gate,
    v17_coefficient_match_gate,
    v26e1b0_summary,
)


def main() -> None:
    root = (
        Path(
            __file__
        )
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

    e1a_path = (
        data_dir
        /
        "032v26e1a_exact_einstein_frame_map_summary.json"
    )

    r6_path = (
        data_dir
        /
        "032v19r6_companion_positivity_empirical_energy_summary.json"
    )

    if not e1a_path.exists():
        raise FileNotFoundError(
            str(
                e1a_path
            )
        )

    if not r6_path.exists():
        raise FileNotFoundError(
            str(
                r6_path
            )
        )

    e1a = json.loads(
        e1a_path.read_text(
            encoding="utf-8"
        )
    )[
        "summary"
    ]

    r6 = json.loads(
        r6_path.read_text(
            encoding="utf-8"
        )
    )

    assert e1a[
        "v26e1a_partial_green"
    ] is True

    assert r6[
        "current_032_kinetic_conformal_axial_implementation_closed"
    ] is True

    assert r6[
        "all_possible_kinetic_conformal_theories_closed"
    ] is False

    actual_empirical_min = float(
        r6[
            "v17_exact_reconstruction"
        ][
            "empirical_min_metric_ev"
        ]
    )

    actual_energy_max = float(
        r6[
            "v17_exact_reconstruction"
        ][
            "energy_max_metric_ev"
        ]
    )

    actual_overlap = bool(
        r6[
            "v17_exact_reconstruction"
        ][
            "empirical_energy_overlap_exists"
        ]
    )

    actual_boundary_j = float(
        r6[
            "v17_exact_reconstruction"
        ][
            "empirical_boundary"
        ][
            "partial_energy_j"
        ]
    )

    operator = pure_j0_operator_gate()
    coefficient = v17_coefficient_match_gate()
    source = source_operator_provenance_gate()
    force = offstate_two_scalar_force_gate()
    memory = inherited_v19r6_failure_memory()
    summary = v26e1b0_summary()

    payload = {
        "frame_operator":
            operator,

        "coefficient_mapping":
            coefficient,

        "source_provenance":
            source,

        "offstate_two_scalar_force":
            force,

        "durable_v19r6_memory":
            memory,

        "actual_r6_result_crosscheck":
            {
                "empirical_metric_min_ev":
                    actual_empirical_min,

                "energy_metric_max_ev":
                    actual_energy_max,

                "empirical_energy_overlap_exists":
                    actual_overlap,

                "empirical_boundary_partial_j":
                    actual_boundary_j,
            },

        "summary":
            summary,
    }

    summary_path = (
        data_dir
        /
        "032v26e1b0_pure_j0_provenance_collision_summary.json"
    )

    summary_path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
        +
        "\n",
        encoding="utf-8",
    )

    print(
        "BRANCH="
        +
        summary[
            "branch"
        ]
    )

    print(
        "SUBGATE="
        +
        summary[
            "subgate"
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
        "V26E1A_PROVENANCE_PASS="
        +
        str(
            summary[
                "v26e1a_provenance_pass"
            ]
        )
    )

    print(
        "LEADING_EINSTEIN_FRAME_MATTER_OPERATOR_PURE_J0="
        +
        str(
            summary[
                "leading_einstein_frame_matter_operator_pure_j0"
            ]
        )
    )

    print(
        "LEADING_INDEPENDENT_J2_GENERATED="
        +
        str(
            summary[
                "leading_independent_j2_generated"
            ]
        )
    )

    print(
        "V17_V19_OPERATOR_CLASS_COLLISION="
        +
        str(
            summary[
                "v17_v19_operator_class_collision"
            ]
        )
    )

    print(
        "V17_EQUIVALENT_ABS_C1_OVER_ABS_KAPPA="
        +
        str(
            summary[
                "v17_equivalent_abs_c1_over_abs_kappa"
            ]
        )
    )

    print(
        "SIGN_CONVENTION_TRANSLATION_REQUIRED="
        +
        str(
            summary[
                "sign_convention_translation_required"
            ]
        )
    )

    print(
        "OFFSTATE_FORCE_SIGN_FLIP_ESCAPE="
        +
        str(
            summary[
                "offstate_force_sign_flip_escape"
            ]
        )
    )

    print(
        "SAME_HIDDEN_AXIAL_SOURCE_OPERATOR_CLASS="
        +
        str(
            summary[
                "same_hidden_axial_source_operator_class"
            ]
        )
    )

    print(
        "SAME_HIDDEN_AXIAL_SOURCE_STATE_ESTABLISHED="
        +
        str(
            summary[
                "same_hidden_axial_source_state_established"
            ]
        )
    )

    print(
        "R5_TYPE_TWO_SCALAR_FORCE_PRESENT_FOR_CANONICAL_UNSCREENED_COMPLETION="
        +
        str(
            summary[
                "r5_type_two_scalar_force_present_for_canonical_unscreened_completion"
            ]
        )
    )

    print(
        "C1_F2_CANONICAL_RESCALING_INVARIANT="
        +
        str(
            summary[
                "c1_f2_canonical_rescaling_invariant"
            ]
        )
    )

    print(
        "ACTUAL_V19R6_EMPIRICAL_METRIC_MIN_EV="
        +
        str(
            actual_empirical_min
        )
    )

    print(
        "ACTUAL_V19R6_STRICT_ENERGY_METRIC_MAX_EV="
        +
        str(
            actual_energy_max
        )
    )

    print(
        "ACTUAL_V19R6_METRIC_GAP_EV="
        +
        str(
            actual_empirical_min
            -
            actual_energy_max
        )
    )

    print(
        "ACTUAL_V19R6_EMPIRICAL_BOUNDARY_PARTIAL_J="
        +
        str(
            actual_boundary_j
        )
    )

    print(
        "ACTUAL_V19R6_EMPIRICAL_ENERGY_OVERLAP_EXISTS="
        +
        str(
            actual_overlap
        )
    )

    print(
        "EXACT_V19R6_ENERGY_BOUNDARY_TRANSFERS_TO_ARBITRARY_V26D_SOURCE="
        +
        str(
            summary[
                "exact_v19r6_energy_boundary_transfers_to_arbitrary_v26d_source"
            ]
        )
    )

    print(
        "EXACT_V17_EQUIVALENT_COMPLETION_CLOSED="
        +
        str(
            summary[
                "exact_v17_equivalent_completion_closed"
            ]
        )
    )

    print(
        "ALL_V26D_COMPLETIONS_GLOBALLY_CLOSED="
        +
        str(
            summary[
                "all_v26d_completions_globally_closed"
            ]
        )
    )

    print(
        "PLAIN_CANONICAL_E1B_CROSSPROP_AS_NEW_CANDIDATE_AUTHORIZED="
        +
        str(
            summary[
                "plain_canonical_e1b_crossprop_recomputation_as_new_candidate_authorized"
            ]
        )
    )

    print(
        "GENUINELY_NEW_V26D_COMPLETION_RERANK_AUTHORIZED="
        +
        str(
            summary[
                "genuinely_new_v26d_completion_rerank_authorized"
            ]
        )
    )

    print(
        "PHYSICAL_G00_CROSS_RESPONSE_ESTABLISHED="
        +
        str(
            summary[
                "physical_g00_cross_response_established"
            ]
        )
    )

    print(
        "MIN_OUTWARD_ACCELERATION_M_S2="
        +
        str(
            summary[
                "minimum_required_outward_acceleration_m_s2"
            ]
        )
    )

    print(
        "MIN_TRUE_STANDOFF_M="
        +
        str(
            summary[
                "minimum_required_true_standoff_m"
            ]
        )
    )

    print(
        "PERFORMANCE_ABOVE_FLOOR_IS_FAVORABLE="
        +
        str(
            summary[
                "performance_above_floor_is_favorable"
            ]
        )
    )

    print(
        "V26D_COMPLETE_ENERGY_J="
        +
        str(
            summary[
                "v26d_complete_energy_j"
            ]
        )
    )

    print(
        "ENERGY_OPTIMIZATION_AUTHORIZED="
        +
        str(
            summary[
                "energy_optimization_authorized"
            ]
        )
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


if __name__ == "__main__":
    main()
