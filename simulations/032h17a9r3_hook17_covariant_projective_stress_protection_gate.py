"""032H17A9R3 — covariant projector / same-action stress / protection audit."""

from __future__ import annotations

import json
from pathlib import Path

from antigravity_research.agminer.hook17_covariant_projective_stress_protection import (
    case_i_protection_audit,
    clean_covariant_source_gate,
    clean_same_action_diffeomorphism_ward_gate,
    covariant_projector_geometry_gate,
    covariant_projector_gl_equivariance_gate,
    flat_covariant_projector_regression_gate,
    h17a9r3_summary,
    same_action_clean_metric_stress_gate,
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

    data_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    a9r2_path = (
        data_dir
        /
        "032h17a9r2_hook17_projective_dirac_completion_summary.json"
    )

    if not a9r2_path.exists():
        raise FileNotFoundError(
            str(
                a9r2_path
            )
        )

    a9r2 = json.loads(
        a9r2_path.read_text(
            encoding="utf-8"
        )
    )[
        "summary"
    ]

    assert a9r2[
        "partial_green"
    ] is True

    assert a9r2[
        "clean_a9_1plus_pole_numerator_preserved"
    ] is True

    geometry = covariant_projector_geometry_gate()
    equivariance = covariant_projector_gl_equivariance_gate()
    flat = flat_covariant_projector_regression_gate()
    clean = clean_covariant_source_gate()
    stress = same_action_clean_metric_stress_gate()
    ward = clean_same_action_diffeomorphism_ward_gate()
    protection = case_i_protection_audit()
    summary = h17a9r3_summary()

    payload = {
        "covariant_projector_geometry":
            geometry,

        "gl4_equivariance":
            equivariance,

        "flat_regression":
            flat,

        "clean_source":
            clean,

        "same_action_clean_metric_stress":
            stress,

        "clean_same_action_diffeomorphism_ward":
            ward,

        "case_i_protection":
            protection,

        "summary":
            summary,
    }

    summary_path = (
        data_dir
        /
        "032h17a9r3_hook17_covariant_projective_stress_protection_summary.json"
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
        "COVARIANT_GEOMETRIC_PROJECTOR_ESTABLISHED="
        +
        str(
            summary[
                "covariant_geometric_projector_established"
            ]
        )
    )

    print(
        "PROJECTOR_GL4_EQUIVARIANCE_PASS="
        +
        str(
            summary[
                "projector_gl4_equivariance_pass"
            ]
        )
    )

    print(
        "PROJECTOR_FLAT_LIMIT_MATCHES_A9R2="
        +
        str(
            summary[
                "projector_flat_limit_matches_a9r2"
            ]
        )
    )

    print(
        "CLEAN_A9_SOURCE_SURVIVES_COVARIANT_PROJECTOR="
        +
        str(
            summary[
                "clean_a9_source_survives_covariant_projector"
            ]
        )
    )

    print(
        "CLEAN_A9_EXACT_1PLUS_POLE_NUMERATOR="
        +
        str(
            summary[
                "clean_a9_exact_1plus_pole_numerator"
            ]
        )
    )

    print(
        "SAME_ACTION_LINEARIZED_CLEAN_METRIC_STRESS_DERIVED="
        +
        str(
            summary[
                "same_action_linearized_clean_metric_stress_derived"
            ]
        )
    )

    print(
        "SAME_ACTION_LINEARIZED_S032="
        +
        str(
            summary[
                "same_action_linearized_s032"
            ]
        )
    )

    print(
        "SAME_ACTION_LINEARIZED_SIGMA_MATCHES_UNIQUE_A9R1_SOLUTION="
        +
        str(
            summary[
                "same_action_linearized_sigma_matches_unique_a9r1_solution"
            ]
        )
    )

    print(
        "SAME_ACTION_CLEAN_LINEARIZED_DIFFEO_WARD_PASS="
        +
        str(
            summary[
                "same_action_clean_linearized_diffeomorphism_ward_pass"
            ]
        )
    )

    print(
        "GEOMETRIC_AND_CLEAN_LINEARIZED_NOETHER_PARTIAL_GREEN="
        +
        str(
            summary[
                "geometric_and_clean_linearized_noether_partial_green"
            ]
        )
    )

    print(
        "FULL_GLOBAL_WORLD_SPINOR_COVARIANCE_ESTABLISHED="
        +
        str(
            summary[
                "full_global_world_spinor_covariance_established"
            ]
        )
    )

    print(
        "CASE_I_HEALTH_SURFACE_CODIMENSION="
        +
        str(
            summary[
                "case_i_health_surface_codimension"
            ]
        )
    )

    print(
        "PROJECTIVE_SYMMETRY_ALONE_ENFORCES_CASE_I_HEALTH_RELATIONS="
        +
        str(
            summary[
                "projective_symmetry_alone_enforces_case_i_health_relations"
            ]
        )
    )

    print(
        "CASE_I_MODE_REMOVAL_IS_NEW_GAUGE_NULL="
        +
        str(
            summary[
                "case_i_mode_removal_is_new_gauge_null"
            ]
        )
    )

    print(
        "ADDITIONAL_CASE_I_PROTECTING_SYMMETRY_ESTABLISHED="
        +
        str(
            summary[
                "additional_case_i_protecting_symmetry_established"
            ]
        )
    )

    print(
        "CASE_I_ACTUAL_BETA_FUNCTIONS_COMPUTED="
        +
        str(
            summary[
                "case_i_actual_beta_functions_computed"
            ]
        )
    )

    print(
        "CASE_I_RADIATIVE_STABILITY_ESTABLISHED="
        +
        str(
            summary[
                "case_i_radiative_stability_established"
            ]
        )
    )

    print(
        "CASE_I_TECHNICAL_NATURALNESS_GATE_PASS="
        +
        str(
            summary[
                "case_i_technical_naturalness_gate_pass"
            ]
        )
    )

    print(
        "CURRENT_PS_CASE_I_CANDIDATE_PROMOTION_AUTHORIZED="
        +
        str(
            summary[
                "current_ps_case_i_candidate_promotion_authorized"
            ]
        )
    )

    print(
        "CURRENT_PS_CASE_I_BRANCH_STATUS="
        +
        summary[
            "current_ps_case_i_branch_status"
        ]
    )

    print(
        "UNKNOWN_PROTECTED_CASE_I_COMPLETION_GLOBALLY_CLOSED="
        +
        str(
            summary[
                "unknown_protected_case_i_completion_globally_closed"
            ]
        )
    )

    print(
        "SAME_ACTION_HOOK17_COMPLETE="
        +
        str(
            summary[
                "same_action_hook17_complete"
            ]
        )
    )

    print(
        "HOOK17_CLOSED="
        +
        str(
            summary[
                "hook17_closed"
            ]
        )
    )

    print(
        "HOOK17_REFERENCE_CAPACITY_RP1E12_J="
        +
        str(
            summary[
                "hook17_reference_capacity_rp1e12_j"
            ]
        )
    )

    print(
        "HOOK17_COMPLETE_ENERGY_J="
        +
        str(
            summary[
                "hook17_complete_energy_j"
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
        "V26D_RESUME_AUTHORIZED="
        +
        str(
            summary[
                "v26d_resume_authorized"
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
