"""Regressions for 032V19R6 companion positivity / empirical coefficient gate."""

import math

from antigravity_research.agminer.companion_operator_empirical import (
    allowed_extra_attractive_pressure_pa,
    finite_gold_film_static_c_cap,
    fixed_static_j0_j2_coefficients,
    material_j0_j2_kinetic_factors,
    normalized_finite_slab_reflection,
    normalized_planar_reflection,
    positivity_companion_cancellation_gate,
)
from antigravity_research.agminer.two_scalar_quantum_force import (
    matter_loading_from_c1,
)


CURRENT_C = 1.5142715050689224e-18

AU_DENSITY = 19300.0

SEPARATION_M = 200.0e-9
SPHERE_AU_M = 180.0e-9
PLATE_AU_M = 210.0e-9

MEASURED_PA = 0.51050
THEORY_PA = 0.51126
XI95_PA = 0.00840


def gold_rho_ev4():
    return float(
        matter_loading_from_c1(
            c1_ev_m4=
                CURRENT_C,

            density_kg_m3=
                AU_DENSITY,
        )[
            "rho_ev4"
        ]
    )


def empirical_cap():
    return (
        finite_gold_film_static_c_cap(
            current_c_ev_m4=
                CURRENT_C,

            gold_density_kg_m3=
                AU_DENSITY,

            separation_m=
                SEPARATION_M,

            sphere_gold_thickness_m=
                SPHERE_AU_M,

            plate_gold_thickness_m=
                PLATE_AU_M,

            measured_pressure_pa=
                MEASURED_PA,

            standard_theory_pressure_pa=
                THEORY_PA,

            confidence_halfwidth_pa=
                XI95_PA,
        )
    )


def test_fixed_static_decomposition():
    result = (
        fixed_static_j0_j2_coefficients(
            static_spatial_c_ev_m4=
                CURRENT_C,

            j2_c_ev_m4=
                0.5
                * CURRENT_C,
        )
    )

    assert math.isclose(
        result[
            "c_s_ev_m4"
        ],
        CURRENT_C,
        rel_tol=0.0,
        abs_tol=0.0,
    )

    assert math.isclose(
        result[
            "c_t_ev_m4"
        ],
        1.5
        * CURRENT_C,
        rel_tol=2.0e-15,
    )


def test_positive_j2_is_forward_positivity_compatible():
    result = (
        fixed_static_j0_j2_coefficients(
            static_spatial_c_ev_m4=
                CURRENT_C,

            j2_c_ev_m4=
                CURRENT_C,
        )
    )

    assert (
        result[
            "jiang_forward_positivity_compatible"
        ]
        is True
    )


def test_positive_j2_has_zt_ge_zs():
    result = (
        material_j0_j2_kinetic_factors(
            rho_ev4=
                gold_rho_ev4(),

            static_spatial_c_ev_m4=
                CURRENT_C,

            j2_c_ev_m4=
                CURRENT_C,
        )
    )

    assert (
        result[
            "z_t_ge_z_s"
        ]
        is True
    )

    assert (
        result[
            "z_t"
        ]
        >
        result[
            "z_s"
        ]
    )


def test_zero_j2_reproduces_pure_j0_reflection():
    factors = (
        material_j0_j2_kinetic_factors(
            rho_ev4=
                gold_rho_ev4(),

            static_spatial_c_ev_m4=
                CURRENT_C,

            j2_c_ev_m4=
                0.0,
        )
    )

    result = (
        normalized_planar_reflection(
            z_t=
                factors[
                    "z_t"
                ],

            z_s=
                factors[
                    "z_s"
                ],

            xi_over_kappa0=
                0.7,
        )
    )

    assert (
        abs(
            result[
                "reflection_minus_pure_j0"
            ]
        )
        <
        1.0e-14
    )


def test_positive_j2_increases_nonzero_frequency_reflection():
    result = (
        positivity_companion_cancellation_gate(
            rho_ev4=
                gold_rho_ev4(),

            static_spatial_c_ev_m4=
                CURRENT_C,

            j2_c_ev_m4=
                CURRENT_C,

            xi_over_kappa0=
                0.7,
        )
    )

    assert (
        result[
            "reflection_minus_pure_j0"
        ]
        >
        0.0
    )

    assert (
        result[
            "positivity_compatible_cancellation"
        ]
        is False
    )


def test_negative_j2_can_reduce_but_violates_positivity():
    result = (
        positivity_companion_cancellation_gate(
            rho_ev4=
                gold_rho_ev4(),

            static_spatial_c_ev_m4=
                CURRENT_C,

            j2_c_ev_m4=
                -0.5
                * CURRENT_C,

            xi_over_kappa0=
                0.7,
        )
    )

    assert (
        result[
            "reflection_reduced"
        ]
        is True
    )

    assert (
        result[
            "jiang_forward_positivity_compatible"
        ]
        is False
    )


def test_positive_j2_increases_finite_slab_reflection():
    pure_factors = (
        material_j0_j2_kinetic_factors(
            rho_ev4=
                gold_rho_ev4(),

            static_spatial_c_ev_m4=
                CURRENT_C,

            j2_c_ev_m4=
                0.0,
        )
    )

    positive_factors = (
        material_j0_j2_kinetic_factors(
            rho_ev4=
                gold_rho_ev4(),

            static_spatial_c_ev_m4=
                CURRENT_C,

            j2_c_ev_m4=
                CURRENT_C,
        )
    )

    pure = (
        normalized_finite_slab_reflection(
            z_t=
                pure_factors[
                    "z_t"
                ],

            z_s=
                pure_factors[
                    "z_s"
                ],

            xi_over_kappa0=
                0.7,

            kappa0_times_thickness=
                1.0,
        )
    )

    positive = (
        normalized_finite_slab_reflection(
            z_t=
                positive_factors[
                    "z_t"
                ],

            z_s=
                positive_factors[
                    "z_s"
                ],

            xi_over_kappa0=
                0.7,

            kappa0_times_thickness=
                1.0,
        )
    )

    assert (
        positive[
            "finite_slab_reflection"
        ]
        >
        pure[
            "finite_slab_reflection"
        ]
    )


def test_allowed_extra_pressure_is_7p64_mpa():
    allowed = (
        allowed_extra_attractive_pressure_pa(
            measured_pressure_pa=
                MEASURED_PA,

            standard_theory_pressure_pa=
                THEORY_PA,

            confidence_halfwidth_pa=
                XI95_PA,
        )
    )

    assert math.isclose(
        allowed,
        0.00764,
        rel_tol=2.0e-14,
    )


def test_empirical_static_c_cap():
    result = empirical_cap()

    assert (
        2.14e-21
        <
        result[
            "static_c_cap_ev_m4"
        ]
        <
        2.17e-21
    )


def test_empirical_metric_scale_is_about_123kev():
    result = empirical_cap()

    assert (
        123.0e3
        <
        result[
            "metric_scale_min_ev"
        ]
        <
        124.0e3
    )


def test_current_coefficient_requires_gt700_suppression():
    result = empirical_cap()

    assert (
        result[
            "current_over_cap"
        ]
        >
        700.0
    )


def test_gold_loading_at_empirical_cap_is_moderate():
    result = empirical_cap()

    assert (
        0.3
        <
        result[
            "cap_gold_epsilon"
        ]
        <
        0.4
    )


def test_current_coefficient_is_not_empirically_allowed():
    result = empirical_cap()

    assert (
        result[
            "current_coefficient_already_allowed"
        ]
        is False
    )

    assert (
        result[
            "current_extra_pressure_pa"
        ]
        >
        0.39
    )


def test_empirical_cap_metric_is_above_v17_100kev_reference():
    result = empirical_cap()

    assert (
        result[
            "metric_scale_min_ev"
        ]
        >
        1.0e5
    )
