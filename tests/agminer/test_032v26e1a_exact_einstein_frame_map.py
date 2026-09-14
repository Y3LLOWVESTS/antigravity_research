"""Regression tests for 032V26E1A."""

import math

from antigravity_research.agminer.v26e1a_exact_einstein_frame_map import (
    explicit_inverse_map_gate,
    forward_reconstruction_gate,
    frame_observable_discipline_gate,
    inverse_normalized_kinetic_map,
    invertibility_identity_scan,
    invertibility_scan_gate,
    normalized_linear_map,
    representative_frame_gate,
    v26e0_provenance_gate,
    v26e1a_summary,
)


def test_v26e0_provenance_authorizes_frame_theorem():
    result = v26e0_provenance_gate()

    assert result[
        "v26e0_provenance_pass"
    ] is True

    assert result[
        "tensor_partial_green"
    ] is True

    assert result[
        "scalar_metric_symbol_still_required"
    ] is True

    assert result[
        "crossprop_still_required"
    ] is True


def test_inverse_class_ia_equation_290_and_bx_zero():
    result = explicit_inverse_map_gate()

    assert result[
        "eq_2_90_pass"
    ] is True

    assert result[
        "B_X_zero"
    ] is True

    assert result[
        "eq_2_90_error"
    ] <= 1.0e-12

    assert abs(
        result[
            "B_X"
        ]
    ) <= 1.0e-12


def test_inverse_map_reduces_curvature_coefficient_to_constant():
    result = explicit_inverse_map_gate()

    assert result[
        "F_tilde_constant_F0"
    ] is True

    assert math.isclose(
        result[
            "F_tilde"
        ],
        result[
            "F0"
        ],
        abs_tol=1.0e-12,
    )

    assert result[
        "map_invertible"
    ] is True


def test_forward_eh_map_reconstructs_all_v26d_quadratic_coefficients():
    result = forward_reconstruction_gate()

    assert result[
        "eh_forward_reconstruction_pass"
    ] is True

    assert result[
        "alpha1"
    ] == 0.0

    assert result[
        "alpha2"
    ] == 0.0

    assert result[
        "alpha3"
    ] == 0.0

    assert result[
        "alpha5"
    ] == 0.0


def test_forward_alpha4_is_exactly_six_fx_squared_over_f():
    result = forward_reconstruction_gate()

    assert result[
        "alpha4_reconstruction_error"
    ] <= 1.0e-12

    assert math.isclose(
        result[
            "alpha4"
        ],
        result[
            "expected_v26d_alpha4"
        ],
        abs_tol=1.0e-12,
    )


def test_representative_v26d_map_has_exact_unit_jacobian_margin():
    result = representative_frame_gate()

    assert result[
        "representative_frame_map_green"
    ] is True

    assert math.isclose(
        result[
            "A"
        ],
        1.05,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "D_map"
        ],
        1.0,
        abs_tol=1.0e-12,
    )

    assert result[
        "transformation_jacobian_margin_collapse"
    ] is False


def test_linear_f_identity_scan_keeps_d_map_exactly_one():
    result = invertibility_scan_gate()

    assert result[
        "scan_point_count"
    ] > 0

    assert result[
        "all_admitted_points_D_exactly_one"
    ] is True

    assert result[
        "all_admitted_points_invertible"
    ] is True

    assert result[
        "near_noninvertible_points_used"
    ] is False

    assert math.isclose(
        result[
            "minimum_abs_D_map"
        ],
        1.0,
        abs_tol=1.0e-12,
    )


def test_kinetic_variable_map_has_positive_derivative():
    row = normalized_linear_map(
        x=0.25,
        eta=0.50,
    )

    assert row[
        "d_x_tilde_d_x"
    ] > 0.0

    expected = (
        1.0
        /
        float(
            row[
                "A"
            ]
        )**2
    )

    assert math.isclose(
        float(
            row[
                "d_x_tilde_d_x"
            ]
        ),
        expected,
        abs_tol=1.0e-12,
    )


def test_kinetic_map_roundtrip_is_exact_on_scan():
    for row in invertibility_identity_scan():
        reconstructed = inverse_normalized_kinetic_map(
            x_tilde=float(
                row[
                    "x_tilde"
                ]
            ),
            eta=float(
                row[
                    "eta"
                ]
            ),
        )

        assert math.isclose(
            reconstructed,
            float(
                row[
                    "x"
                ]
            ),
            abs_tol=1.0e-11,
        )


def test_offstate_map_is_regular():
    row = normalized_linear_map(
        x=0.0,
        eta=0.50,
    )

    assert math.isclose(
        float(
            row[
                "A"
            ]
        ),
        1.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        float(
            row[
                "D_map"
            ]
        ),
        1.0,
        abs_tol=1.0e-12,
    )

    assert row[
        "map_invertible"
    ] is True


def test_frame_change_does_not_allow_metric_observable_to_be_dropped():
    result = frame_observable_discipline_gate()

    assert result[
        "ordinary_matter_minimal_in_jordan_frame"
    ] is True

    assert result[
        "ordinary_matter_minimal_in_einstein_frame"
    ] is False

    assert result[
        "matter_action_must_be_transformed"
    ] is True

    assert result[
        "einstein_metric_response_alone_is_physical_observable"
    ] is False

    assert result[
        "physical_g00_must_be_reconstructed"
    ] is True

    assert result[
        "same_observable_must_match_between_frames"
    ] is True


def test_v26e1a_partial_green_preserves_all_later_physical_gates():
    result = v26e1a_summary()

    assert result[
        "decision"
    ].startswith(
        "GREEN_PARTIAL_V26E1A_"
    )

    assert result[
        "v26e1a_partial_green"
    ] is True

    assert result[
        "quadratic_dhost_gravity_sector_eh_equivalent"
    ] is True

    assert result[
        "linear_F_map_D_identically_one"
    ] is True

    assert result[
        "field_redefinition_near_singular"
    ] is False

    assert result[
        "field_redefinition_margin_collapse_used_for_gain"
    ] is False

    assert result[
        "lower_derivative_scalar_completion_required"
    ] is True

    assert result[
        "full_static_spacelike_scalar_health_established"
    ] is False

    assert result[
        "physical_g00_cross_response_established"
    ] is False

    assert result[
        "finite_payload_established"
    ] is False

    assert result[
        "v26d_complete_energy_j"
    ] is None

    assert result[
        "energy_optimization_authorized"
    ] is False

    assert result[
        "minimum_required_outward_acceleration_m_s2"
    ] == 9.80665

    assert result[
        "minimum_required_true_standoff_m"
    ] == 1.0

    assert result[
        "performance_above_floor_is_favorable"
    ] is True

    assert result[
        "v26e1b_authorized"
    ] is True

    assert result[
        "next"
    ] == (
        "032V26E1B_EINSTEIN_FRAME_HEALTHY_SCALAR_"
        "AND_PHYSICAL_G00_CROSSPROP_GATE"
    )
