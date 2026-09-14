"""Regression tests for 032V26E0."""

import math

from antigravity_research.agminer.v26e0_static_spacelike_tensor_symbol import (
    a4_beta_identity_gate,
    background_route_atlas,
    fallback_trigger_gate,
    p_only_scalar_stationary_point_gate,
    representative_tensor_angle_scan,
    representative_tensor_gate,
    representative_v26d_beta_gate,
    tensor_health_bound_gate,
    tensor_symbol_from_beta,
    unsupported_flat_background_gate,
    v26d_provenance_gate,
    v26e0_summary,
)


def test_a9r3_authorizes_v26d_fallback_without_erasing_partial_results():
    result = fallback_trigger_gate()

    assert result[
        "fallback_trigger_pass"
    ] is True

    assert result[
        "a9r3_partial_results_preserved"
    ] is True

    assert result[
        "current_ps_case_i_blocked"
    ] is True

    assert result[
        "v26d_resume_authorized"
    ] is True


def test_v26d_preserved_action_scaffold_is_valid_starting_point():
    result = v26d_provenance_gate()

    assert result[
        "v26d_provenance_pass"
    ] is True

    assert result[
        "explicit_same_action_scaffold"
    ] is True

    assert result[
        "one_universal_physical_metric"
    ] is True

    assert result[
        "a3_zero_no_decay_identity"
    ] is True

    assert result[
        "active_kmm_witness_nonzero"
    ] is True


def test_a4_beta_identity_is_reconstructed_independently():
    result = a4_beta_identity_gate()

    assert result[
        "a4_beta_identity_pass"
    ] is True

    assert result[
        "identity_error"
    ] <= 1.0e-12

    assert math.isclose(
        result[
            "a4_x2_over_2f"
        ],
        result[
            "three_beta1_squared"
        ],
        abs_tol=1.0e-12,
    )


def test_tensor_parallel_to_gradient_is_exactly_unmodified_and_luminal():
    result = tensor_symbol_from_beta(
        beta_1=
            0.40,

        theta_rad=
            0.0,
    )

    assert math.isclose(
        result[
            "affected_tensor_relative_principal_coefficient"
        ],
        1.0,
        abs_tol=1.0e-12,
    )

    assert result[
        "both_tensor_characteristics_luminal"
    ] is True

    assert result[
        "tensor_ghost_free"
    ] is True


def test_representative_v26d_worst_tensor_margin_is_146_over_147():
    beta = representative_v26d_beta_gate()

    assert beta[
        "representative_beta_matches"
    ] is True

    result = representative_tensor_gate()

    assert math.isclose(
        result[
            "beta_1"
        ],
        1.0 / 21.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "worst_direction_relative_margin"
        ],
        146.0 / 147.0,
        abs_tol=1.0e-12,
    )

    assert result[
        "representative_anisotropic_tensor_ct1_pass"
    ] is True


def test_exact_tensor_health_boundary_is_one_over_sqrt_three():
    result = tensor_health_bound_gate()

    assert math.isclose(
        result[
            "critical_abs_beta_1"
        ],
        1.0 / math.sqrt(3.0),
        abs_tol=1.0e-12,
    )

    assert result[
        "beta_0p50_healthy"
    ] is True

    assert result[
        "beta_0p60_healthy"
    ] is False

    assert result[
        "health_boundary_reconstructed"
    ] is True


def test_representative_angle_scan_is_luminal_and_healthy_everywhere():
    rows = representative_tensor_angle_scan()

    assert len(
        rows
    ) == 7

    assert all(
        row[
            "both_tensor_characteristics_luminal"
        ]
        is True
        for row in rows
    )

    assert all(
        row[
            "tensor_ghost_free"
        ]
        is True
        for row in rows
    )

    assert all(
        row[
            "energy_point"
        ]
        is False
        for row in rows
    )


def test_unsupported_flat_constant_gradient_requires_p_and_px_zero():
    result = unsupported_flat_background_gate()

    assert result[
        "unsupported_flat_background_theorem_pass"
    ] is True

    assert result[
        "unsupported_minkowski_requires_P_zero"
    ] is True

    assert result[
        "unsupported_minkowski_requires_P_X_zero"
    ] is True

    assert result[
        "P_zero_and_P_X_zero_suffice_for_P_sector_background_stress"
    ] is True


def test_stationary_p_sector_does_not_supply_standalone_time_kinetic():
    result = p_only_scalar_stationary_point_gate()

    assert result[
        "p_only_standalone_time_kinetic_nonzero"
    ] is False

    assert math.isclose(
        result[
            "p_only_time_kinetic_coefficient"
        ],
        0.0,
        abs_tol=1.0e-12,
    )

    assert result[
        "full_dhost_mixing_may_supply_scalar_kinetic"
    ] is True

    assert result[
        "full_constrained_scalar_metric_symbol_required"
    ] is True

    assert result[
        "full_scalar_instability_established"
    ] is False


def test_support_balanced_and_curved_background_routes_remain_open():
    rows = background_route_atlas()

    by_name = {
        row[
            "route"
        ]:
            row
        for row in rows
    }

    assert by_name[
        "SUPPORT_BALANCED_LOCAL_PATCH"
    ][
        "closed"
    ] is False

    assert by_name[
        "SUPPORT_BALANCED_LOCAL_PATCH"
    ][
        "support_energy_required"
    ] is True

    assert by_name[
        "CURVED_ONSHELL_STATIC_BACKGROUND"
    ][
        "closed"
    ] is False


def test_v26e0_is_tensor_partial_green_not_full_principal_symbol_green():
    result = v26e0_summary()

    assert result[
        "decision"
    ].startswith(
        "GREEN_PARTIAL_V26E0_"
    )

    assert result[
        "tensor_sector_partial_green"
    ] is True

    assert result[
        "anisotropic_tensor_cone_ct1_established_on_constant_gradient_patch"
    ] is True

    assert result[
        "representative_tensor_principal_health_pass"
    ] is True

    assert result[
        "canonical_health_on_full_static_spacelike_background_established"
    ] is False

    assert result[
        "constraint_elimination_completed"
    ] is False

    assert result[
        "static_spacelike_source_to_metric_cross_response_established"
    ] is False

    assert result[
        "v26e1_full_constrained_symbol_crossprop_authorized"
    ] is True


def test_v26e0_does_not_transfer_hook17_capacity_or_authorize_energy_work():
    result = v26e0_summary()

    assert result[
        "hook17_capacity_reference_transfers_to_v26d"
    ] is False

    assert result[
        "v26d_field_capacity_established"
    ] is False

    assert result[
        "v26d_complete_energy_j"
    ] is None

    assert result[
        "energy_optimization_authorized"
    ] is False

    assert result[
        "action_oracle_authorized"
    ] is False

    assert result[
        "agminer_database_mutation_authorized"
    ] is False

    assert result[
        "original_v26e_scope_complete"
    ] is False

    assert result[
        "next"
    ] == (
        "032V26E1_STATIC_SPACELIKE_FULL_CONSTRAINED_"
        "SCALAR_METRIC_SYMBOL_CROSSPROP_GATE"
    )
