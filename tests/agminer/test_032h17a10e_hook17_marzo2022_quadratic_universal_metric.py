"""Regressions for 032H17A10E protected quadratic universal metric."""

from __future__ import annotations

import math

from antigravity_research.agminer.hook17_marzo2022_quadratic_universal_metric import (
    a10d_anchor_provenance,
    anchor_vector_factorization_gate,
    h17a10e_summary,
    linear_metric_operator_protection_gate,
    quadratic_metric_tensor_gate,
    static_external_g00_gate,
    stueckelberg_invariant_action_scaffold_gate,
)


def test_a10d_exact_healthy_pole_is_required():
    result = a10d_anchor_provenance()

    assert result[
        "pass"
    ] is True


def test_healthy_pole_factorizes_exactly_into_one_vector():
    result = (
        anchor_vector_factorization_gate()
    )

    assert result[
        "factorization_pass"
    ] is True

    assert result[
        "normalized_vector_exact"
    ] == [
        "0",
        "1",
        "0",
        "0",
    ]

    assert result[
        "vector_squared_mostly_minus_exact"
    ] == "-1"


def test_quadratic_conformal_metric_tensor_is_exact():
    result = quadratic_metric_tensor_gate()

    assert result[
        "conformal_identity_exact"
    ] is True

    assert result[
        "quadratic_g00_numerator_nonzero"
    ] is True

    assert result[
        "quadratic_metric_requires_principal_margin_collapse"
    ] is False


def test_second_quadratic_tensor_is_vector_disformal_structure():
    result = quadratic_metric_tensor_gate()

    assert result[
        "vector_identity_exact"
    ] is True


def test_zero_derivative_linear_rank2_is_forbidden_by_rank_parity():
    result = (
        linear_metric_operator_protection_gate()
    )

    assert result[
        "zero_derivative_linear_rank2_from_one_rank3_exists"
    ] is False

    assert result[
        "epsilon_zero_derivative_linear_rank2_exists"
    ] is False


def test_sourcefree_linear_vector_metric_response_is_redundant():
    result = (
        linear_metric_operator_protection_gate()
    )

    assert abs(
        result[
            "transverse_test_q_dot_v"
        ]
    ) < 1.0e-12

    assert result[
        "remaining_linear_term_is_field_redefinition"
    ] is True

    assert result[
        "remaining_linear_term_has_zero_linearized_riemann"
    ] is True

    assert result[
        "nonredundant_sourcefree_linear_physical_metric_response"
    ] is False

    assert result[
        "linear_external_operator_protection_pass"
    ] is True


def test_same_action_scaffold_preserves_marzo_abelian_symmetry():
    result = (
        stueckelberg_invariant_action_scaffold_gate()
    )

    assert result[
        "marzo_protected_family"
    ] is True

    assert result[
        "stueckelberg_invariant_distortion_exact"
    ] is True

    assert result[
        "abelian_symmetry_preserved_by_source_connection"
    ] is True

    assert result[
        "abelian_symmetry_preserved_by_quadratic_metric"
    ] is True

    assert result[
        "action_level_scaffold_established"
    ] is True

    assert result[
        "ordinary_payload_one_universal_metric"
    ] is True


def test_quadratic_portal_has_exact_offstate_silence():
    result = h17a10e_summary()

    assert result[
        "zero_derivative_linear_metric_response"
    ] is False

    assert result[
        "quadratic_offstate_first_variation_zero"
    ] is True

    assert result[
        "quadratic_active_state_response_nonzero"
    ] is True


def test_static_profile_is_sourcefree_transverse_proca_solution():
    result = static_external_g00_gate()

    assert result[
        "source_free_static_proca_pass"
    ] is True

    assert result[
        "transverse_constraint_pass"
    ] is True

    assert math.isclose(
        result[
            "range_m"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )


def test_static_metric_reproduces_exact_1g_outward_at_1m_probe():
    result = static_external_g00_gate()

    assert result[
        "stand_off_probe_m"
    ] == 1.0

    assert result[
        "target_acceleration_reproduced"
    ] is True

    assert result[
        "outward_sign"
    ] is True

    assert result[
        "weak_field"
    ] is True

    assert result[
        "sigma_at_payload"
    ] < 1.0e-15


def test_quadratic_metric_has_nonzero_invariant_tidal_curvature():
    result = static_external_g00_gate()

    assert result[
        "invariant_tidal_response_nonzero"
    ] is True

    assert result[
        "quadratic_metric_response_is_pure_coordinate_effect"
    ] is False

    assert result[
        "metric_exactly_invertible_for_finite_sigma"
    ] is True


def test_a10e_promotes_only_final_finite_payload_energy_gate():
    result = h17a10e_summary()

    assert result[
        "partial_green"
    ] is True

    assert result[
        "technical_naturalness_external_operator_preflight"
    ] is True

    assert result[
        "full_quantum_rg_uv_certified"
    ] is False

    assert result[
        "ultralight_mass_quantitative_naturalness_certified"
    ] is False

    assert result[
        "physical_g00_response_nonzero"
    ] is True

    assert result[
        "physical_g00_outward_sign"
    ] is True

    assert result[
        "finite_payload_established"
    ] is False

    assert result[
        "energy_optimization_authorized"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False

    assert result[
        "next"
    ] == (
        "032H17A10F_FINITE_SOURCE_FINITE_PAYLOAD_1G_1M_"
        "SOURCE_ENERGY_EMPIRICAL_UV_COMPLETE_LEDGER_PREFLIGHT"
    )
