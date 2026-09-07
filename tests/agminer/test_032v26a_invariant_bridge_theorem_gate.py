"""Scientific regressions for 032V26A invariant-bridge theorem gate."""

from __future__ import annotations

import math

from antigravity_research.agminer.invariant_bridge_theorem_gate import (
    SCALAR_TWO_MEDIATOR_KERNEL,
    STANDARD_GRAVITY_MPS2,
    V17_PAYLOAD_RADIUS_M,
    einstein_payload_dirichlet_response_norm_j,
    field_strength_medium_health,
    field_strength_two_mediator_kernel,
    normalized_field_strength_portal_bound,
    required_cross_mixing_margin_for_transfer,
    static_first_derivative_metric_response,
    two_mode_cross_mixing,
    v17_einstein_metric_response_norms,
    v26a_gate,
)


def test_pure_static_disformal_has_zero_g00_response():
    result = (
        static_first_derivative_metric_response(
            conformal_coefficient=
                0.0,

            disformal_coefficient=
                3.0,

            gradient_magnitude=
                2.0,
        )
    )

    assert (
        result[
            "delta_g00"
        ]
        ==
        0.0
    )

    assert (
        result[
            "pure_disformal_delta_g00"
        ]
        ==
        0.0
    )

    assert (
        result[
            "pure_static_disformal_has_leading_rest_mass_numerator"
        ]
        is False
    )


def test_static_rest_response_depends_on_conformal_piece():
    result = (
        static_first_derivative_metric_response(
            conformal_coefficient=
                0.25,

            disformal_coefficient=
                100.0,

            gradient_magnitude=
                2.0,
        )
    )

    assert math.isclose(
        result[
            "delta_g00"
        ],
        -1.0,
        abs_tol=1.0e-14,
    )

    assert math.isclose(
        result[
            "rest_interaction_per_density"
        ],
        -0.5,
        abs_tol=1.0e-14,
    )


def test_field_strength_kernel_is_positive_definite():
    for e_value, b_value in (
        (1.0, 0.0),
        (0.0, 1.0),
        (1.0, 1.0),
        (-1.0, 1.0),
    ):
        result = (
            field_strength_two_mediator_kernel(
                electric_coefficient=
                    e_value,

                magnetic_coefficient=
                    b_value,
            )
        )

        assert (
            result[
                "kernel_coefficient"
            ]
            >
            0.0
        )


def test_unconstrained_field_strength_optimum_matches_16_over_23_scalar():
    result = (
        normalized_field_strength_portal_bound()
    )

    assert math.isclose(
        result[
            "unconstrained_optimal_electric_coefficient"
        ],
        7.0
        /
        23.0,
        rel_tol=1.0e-14,
    )

    assert math.isclose(
        result[
            "unconstrained_ratio_to_scalar_reference"
        ],
        16.0
        /
        23.0,
        rel_tol=1.0e-14,
    )


def test_causal_medium_constraint_for_outward_magnetic_branch():
    healthy = (
        field_strength_medium_health(
            electric_coefficient=
                -1.0,

            magnetic_coefficient=
                1.0,

            density_normalization=
                0.1,
        )
    )

    unhealthy = (
        field_strength_medium_health(
            electric_coefficient=
                7.0
                /
                23.0,

            magnetic_coefficient=
                1.0,

            density_normalization=
                0.1,
        )
    )

    assert (
        healthy[
            "healthy_declared_medium"
        ]
        is True
    )

    assert (
        unhealthy[
            "healthy_declared_medium"
        ]
        is False
    )


def test_healthy_field_strength_minimum_is_twice_scalar_reference():
    result = (
        normalized_field_strength_portal_bound()
    )

    assert math.isclose(
        result[
            "healthy_minimum_ratio_to_scalar_reference"
        ],
        2.0,
        rel_tol=1.0e-14,
    )

    assert (
        result[
            "healthy_leading_portal_beats_scalar_reference"
        ]
        is False
    )


def test_scalar_reference_kernel_normalization():
    assert math.isclose(
        SCALAR_TWO_MEDIATOR_KERNEL,
        15.0
        /
        (
            8.0
            *
            math.pi**3
        ),
        rel_tol=1.0e-15,
    )


def test_two_mode_cross_mixing_inverse_identity():
    result = (
        two_mode_cross_mixing(
            0.5
        )
    )

    assert (
        result[
            "healthy"
        ]
        is True
    )

    assert math.isclose(
        result[
            "minimum_eigenvalue"
        ],
        0.5,
        abs_tol=1.0e-14,
    )

    assert math.isclose(
        result[
            "inverse_cross"
        ],
        -2.0
        /
        3.0,
        rel_tol=1.0e-14,
    )


def test_large_cross_transfer_requires_small_principal_margin():
    result = (
        required_cross_mixing_margin_for_transfer(
            1000.0
        )
    )

    assert (
        result[
            "minimum_abs_mu_required"
        ]
        >
        0.999
    )

    assert (
        result[
            "maximum_minimum_eigenvalue"
        ]
        <
        5.1e-4
    )

    assert (
        result[
            "condition_number_at_threshold"
        ]
        >
        3900.0
    )


def test_unhealthy_cross_mixing_detected():
    result = (
        two_mode_cross_mixing(
            1.01
        )
    )

    assert (
        result[
            "healthy"
        ]
        is False
    )

    assert (
        result[
            "minimum_eigenvalue"
        ]
        <
        0.0
    )


def test_one_g_payload_dirichlet_response_norm_is_about_240_mj():
    result = (
        einstein_payload_dirichlet_response_norm_j(
            payload_radius_m=
                V17_PAYLOAD_RADIUS_M,

            volume_average_acceleration_mps2=
                STANDARD_GRAVITY_MPS2,
        )
    )

    assert math.isclose(
        result[
            "dirichlet_response_norm_mj"
        ],
        240.1509876753618,
        rel_tol=1.0e-12,
    )

    assert (
        result[
            "norm_below_strict_10mj_target"
        ]
        is False
    )


def test_v17_average_response_norm_is_gigajoule_scale():
    result = (
        v17_einstein_metric_response_norms()
    )

    v17 = (
        result[
            "v17_reported_volume_average"
        ]
    )

    assert (
        v17[
            "dirichlet_response_norm_j"
        ]
        >
        4.5e9
    )

    assert (
        result[
            "v17_average_norm_over_10mj"
        ]
        >
        450.0
    )


def test_dirichlet_norm_is_not_mislabeled_as_gr_energy_theorem():
    result = (
        einstein_payload_dirichlet_response_norm_j(
            payload_radius_m=
                0.1,

            volume_average_acceleration_mps2=
                9.80665,
        )
    )

    assert (
        result[
            "is_gauge_invariant_local_gr_energy_theorem"
        ]
        is False
    )

    assert (
        result[
            "is_complete_operating_energy"
        ]
        is False
    )


def test_v26a_preserves_scoped_open_families_and_blocks_blind_scan():
    gate = (
        v26a_gate()
    )

    assert (
        gate[
            "all_dhost_closed"
        ]
        is False
    )

    assert (
        gate[
            "all_vector_portals_closed"
        ]
        is False
    )

    assert (
        gate[
            "all_metric_affine_closed"
        ]
        is False
    )

    assert (
        gate[
            "intrinsic_dirac_hypermomentum_preserved"
        ]
        is True
    )

    assert (
        gate[
            "riemannian_offstate_exact_nonlinear_mag_target_preserved"
        ]
        is True
    )

    assert (
        gate[
            "blind_parameter_scan_authorized"
        ]
        is False
    )

    assert (
        gate[
            "generic_energy_optimization_authorized"
        ]
        is False
    )

    assert (
        gate[
            "next_action_specific_construction_authorized"
        ]
        is True
    )
