"""Scientific regressions for 032H17A3 same-action/protection gate."""

import math

import numpy as np

from antigravity_research.agminer.hook17_same_action_naturalness import (
    field_redefinition_invariance_gate,
    h17a3_summary,
    hook_1plus_constraint_residuals,
    hook_1plus_health,
    hook_2plus_constraint_residuals,
    hook_2plus_health,
    mp_hook_1plus_coefficients,
    mp_hook_2plus_coefficients,
    protection_and_provenance_gate,
    rg_protection_gate,
    same_action_scaffold,
    universal_metric_active_offstate_gate,
)


def test_2plus_representative_point_satisfies_exact_branch_relations():
    point = (
        mp_hook_2plus_coefficients()
    )

    residual = (
        hook_2plus_constraint_residuals(
            point
        )
    )

    assert (
        np.linalg.norm(
            residual
        )
        <
        1.0e-10
    )


def test_2plus_representative_point_is_free_healthy():
    point = (
        mp_hook_2plus_coefficients()
    )

    health = (
        hook_2plus_health(
            point
        )
    )

    assert health[
        "m1_lt_zero"
    ]

    assert health[
        "b6_lt_zero"
    ]

    assert health[
        "mass2_positive"
    ]

    assert health[
        "healthy"
    ]


def test_1plus_representative_point_satisfies_exact_branch_relations():
    point = (
        mp_hook_1plus_coefficients()
    )

    residual = (
        hook_1plus_constraint_residuals(
            point
        )
    )

    assert (
        np.linalg.norm(
            residual
        )
        <
        1.0e-10
    )


def test_1plus_representative_point_is_free_healthy():
    point = (
        mp_hook_1plus_coefficients()
    )

    health = (
        hook_1plus_health(
            point
        )
    )

    assert health[
        "m1_lt_zero"
    ]

    assert health[
        "b7_lt_zero"
    ]

    assert health[
        "mass2_positive"
    ]

    assert health[
        "healthy"
    ]


def test_2plus_scaffold_preserves_exact_v24_source_overlap():
    result = (
        same_action_scaffold(
            "HOOK_2_PLUS"
        )
    )

    assert (
        result[
            "h17a2_exact_source_projector_nonzero"
        ]
        is True
    )

    assert (
        result[
            "free_healthy_mode"
        ]
        is True
    )


def test_1plus_scaffold_preserves_exact_v24_source_overlap():
    result = (
        same_action_scaffold(
            "HOOK_1_PLUS"
        )
    )

    assert (
        result[
            "h17a2_exact_source_projector_nonzero"
        ]
        is True
    )

    assert (
        result[
            "free_healthy_mode"
        ]
        is True
    )


def test_quadratic_universal_metric_preserves_active_offstate_separation():
    result = (
        universal_metric_active_offstate_gate()
    )

    assert (
        result[
            "offstate_linear_metric_response_zero"
        ]
        is True
    )

    assert (
        result[
            "active_linear_metric_response_nonzero"
        ]
        is True
    )

    assert (
        result[
            "quadratic_homogeneity_identity_pass"
        ]
        is True
    )


def test_universal_metric_adds_no_linear_offstate_metric_source_feedback():
    result = (
        universal_metric_active_offstate_gate()
    )

    assert (
        result[
            "offstate_metric_feedback_source_zero"
        ]
        is True
    )


def test_universal_metric_does_add_active_state_source_feedback():
    result = (
        universal_metric_active_offstate_gate()
    )

    assert (
        result[
            "active_metric_feedback_source_nonzero"
        ]
        is True
    )

    assert (
        abs(
            result[
                "unit_t00_active_directional_source_feedback"
            ]
        )
        >
        1.0e-10
    )


def test_active_response_survives_invertible_field_redefinition():
    result = (
        field_redefinition_invariance_gate()
    )

    assert (
        result[
            "field_transform_invertible"
        ]
        is True
    )

    assert (
        result[
            "explicit_portal_removed_in_redefined_metric_projection"
        ]
        is True
    )

    assert (
        result[
            "physical_response_field_redefinition_invariant"
        ]
        is True
    )

    assert (
        result[
            "response_relative_error"
        ]
        <
        1.0e-10
    )


def test_field_redefinition_does_not_obtain_gain_from_principal_collapse():
    result = (
        field_redefinition_invariance_gate()
    )

    assert (
        result[
            "original_principal_margin_positive"
        ]
        is True
    )

    assert (
        result[
            "redefined_principal_margin_positive"
        ]
        is True
    )


def test_2plus_healthy_surface_has_high_local_codimension():
    result = (
        rg_protection_gate(
            "HOOK_2_PLUS"
        )
    )

    assert (
        result[
            "constraint_surface_jacobian_rank"
        ]
        ==
        7
    )

    assert (
        result[
            "constraint_surface_local_codimension"
        ]
        ==
        7
    )

    assert (
        result[
            "constraint_surface_tangent_nullity"
        ]
        ==
        3
    )


def test_1plus_healthy_surface_has_high_local_codimension():
    result = (
        rg_protection_gate(
            "HOOK_1_PLUS"
        )
    )

    assert (
        result[
            "constraint_surface_jacobian_rank"
        ]
        ==
        7
    )

    assert (
        result[
            "constraint_surface_local_codimension"
        ]
        ==
        7
    )

    assert (
        result[
            "constraint_surface_tangent_nullity"
        ]
        ==
        3
    )


def test_generic_rg_direction_is_not_automatically_tangent_for_2plus():
    result = (
        rg_protection_gate(
            "HOOK_2_PLUS"
        )
    )

    assert (
        result[
            "generic_beta_automatically_tangent"
        ]
        is False
    )

    assert (
        result[
            "generic_beta_normal_drift_norm"
        ]
        >
        1.0e-8
    )

    assert (
        result[
            "actual_beta_functions_calculated"
        ]
        is False
    )


def test_generic_rg_direction_is_not_automatically_tangent_for_1plus():
    result = (
        rg_protection_gate(
            "HOOK_1_PLUS"
        )
    )

    assert (
        result[
            "generic_beta_automatically_tangent"
        ]
        is False
    )

    assert (
        result[
            "generic_beta_normal_drift_norm"
        ]
        >
        1.0e-8
    )

    assert (
        result[
            "actual_beta_functions_calculated"
        ]
        is False
    )


def test_unprotected_branches_fail_closed_on_protection_not_on_tree_health():
    two = (
        protection_and_provenance_gate(
            "HOOK_2_PLUS"
        )
    )

    one = (
        protection_and_provenance_gate(
            "HOOK_1_PLUS"
        )
    )

    assert two[
        "tree_level_action_scaffold_exists"
    ]

    assert one[
        "tree_level_action_scaffold_exists"
    ]

    assert (
        two[
            "naturalness_protection_gate_pass"
        ]
        is False
    )

    assert (
        one[
            "naturalness_protection_gate_pass"
        ]
        is False
    )

    assert (
        two[
            "technical_naturalness_established"
        ]
        is False
    )

    assert (
        one[
            "technical_naturalness_established"
        ]
        is False
    )


def test_tree_level_manifest_is_not_mislabeled_same_action_complete():
    two = (
        same_action_scaffold(
            "HOOK_2_PLUS"
        )
    )

    one = (
        same_action_scaffold(
            "HOOK_1_PLUS"
        )
    )

    for result in (
        two,
        one,
    ):
        assert (
            result[
                "single_action_manifest_written"
            ]
            is True
        )

        assert (
            result[
                "tree_level_action_scaffold_only"
            ]
            is True
        )

        assert (
            result[
                "same_action_provenance_complete"
            ]
            is False
        )

        assert (
            result[
                "full_combined_dirac_variation_rederived"
            ]
            is False
        )

        assert (
            result[
                "full_hypermomentum_noether_identity_rederived"
            ]
            is False
        )


def test_h17a3_blocks_h17b_and_energy_until_protected_completion():
    result = (
        h17a3_summary()
    )

    assert (
        result[
            "decision"
        ].startswith(
            "YELLOW_H17A3_"
        )
    )

    assert (
        result[
            "next"
        ].startswith(
            "032H17A4_PROTECTED_MAG_STUECKELBERG_"
        )
    )

    assert (
        result[
            "tier1_hook17_mechanism_certified"
        ]
        is False
    )

    assert (
        result[
            "h17b_authorized"
        ]
        is False
    )

    assert (
        result[
            "energy_optimization_authorized"
        ]
        is False
    )

    assert (
        result[
            "agminer_database_mutation_authorized"
        ]
        is False
    )

    assert math.isclose(
        result[
            "hook17_reference_capacity_rp1e12_j"
        ],
        17.0676442196,
    )

    assert (
        result[
            "hook17_complete_energy_j"
        ]
        is None
    )

    assert (
        result[
            "physical_antigravity_model_found"
        ]
        is False
    )
