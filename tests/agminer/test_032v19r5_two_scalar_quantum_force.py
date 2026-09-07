"""Scientific regressions for 032V19R5 two-scalar empirical gate."""

import math

from antigravity_research.agminer.two_scalar_quantum_force import (
    DBI_REFERENCE_COEFFICIENT,
    TRACE_PAIR_COEFFICIENT,
    born_halfspace_pressure_pa,
    dbi_reference_force_coefficient,
    empirical_pressure_gate,
    integrated_pairwise_pressure_coefficient,
    laboratory_momentum_scout,
    matter_loading_from_c1,
    metric_scale_from_c1_ev,
    scalar_casimir_pressure_pa,
    soft_mass_range_scout,
    trace_pair_force_coefficient,
)


C1 = 1.5142715050689224e-18

HARD_EV = 56.92491792612398
METRIC_EV = 23971.29870009097

AU_DENSITY_KG_M3 = 19300.0

SEPARATION_M = 200.0e-9

SPHERE_AU_M = 180.0e-9
PLATE_AU_M = 210.0e-9

MEASURED_PA = 0.51050
THEORY_PA = 0.51126
XI95_PA = 0.00840

SPHERE_RADIUS_M = 151.3e-6


def test_trace_pair_force_coefficient():
    assert math.isclose(
        trace_pair_force_coefficient(),
        15.0
        / (
            8.0
            * math.pi**3
        ),
        rel_tol=0.0,
        abs_tol=0.0,
    )


def test_dbi_reference_normalization_ratio_is_eighty():
    assert math.isclose(
        dbi_reference_force_coefficient(),
        3.0
        / (
            128.0
            * math.pi**3
        ),
        rel_tol=0.0,
        abs_tol=0.0,
    )

    assert math.isclose(
        TRACE_PAIR_COEFFICIENT
        / DBI_REFERENCE_COEFFICIENT,
        80.0,
        rel_tol=2.0e-15,
    )


def test_integrated_pairwise_pressure_identity():
    assert math.isclose(
        integrated_pairwise_pressure_coefficient(),
        3.0
        / (
            16.0
            * math.pi**2
        ),
        rel_tol=2.0e-15,
    )


def test_metric_scale_reconstructs_r4_target():
    assert math.isclose(
        metric_scale_from_c1_ev(
            C1
        ),
        METRIC_EV,
        rel_tol=2.0e-14,
    )


def test_gold_matter_loading_is_nonperturbative():
    result = (
        matter_loading_from_c1(
            c1_ev_m4=
                C1,

            density_kg_m3=
                AU_DENSITY_KG_M3,
        )
    )

    assert math.isclose(
        result[
            "epsilon"
        ],
        251.93092268688164,
        rel_tol=3.0e-13,
    )

    assert (
        result[
            "born_material_limit"
        ]
        is False
    )


def test_gold_interface_reflection_is_near_unity():
    result = (
        matter_loading_from_c1(
            c1_ev_m4=
                C1,

            density_kg_m3=
                AU_DENSITY_KG_M3,
        )
    )

    assert math.isclose(
        result[
            "interface_reflection"
        ],
        0.9921238422684496,
        rel_tol=3.0e-13,
    )


def test_exact_resummation_recovers_born_limit_at_low_density():
    dilute_density = 0.01

    exact = (
        scalar_casimir_pressure_pa(
            c1_ev_m4=
                C1,

            density1_kg_m3=
                dilute_density,

            density2_kg_m3=
                dilute_density,

            separation_m=
                SEPARATION_M,
        )[
            "pressure_magnitude_pa"
        ]
    )

    born = (
        born_halfspace_pressure_pa(
            c1_ev_m4=
                C1,

            density1_kg_m3=
                dilute_density,

            density2_kg_m3=
                dilute_density,

            separation_m=
                SEPARATION_M,
        )
    )

    assert (
        abs(
            exact
            / born
            - 1.0
        )
        <
        2.0e-4
    )


def test_exact_gold_halfspace_pressure():
    result = (
        scalar_casimir_pressure_pa(
            c1_ev_m4=
                C1,

            density1_kg_m3=
                AU_DENSITY_KG_M3,

            density2_kg_m3=
                AU_DENSITY_KG_M3,

            separation_m=
                SEPARATION_M,
        )
    )

    assert math.isclose(
        result[
            "pressure_magnitude_pa"
        ],
        0.39922889493702024,
        rel_tol=3.0e-9,
    )


def test_actual_gold_film_only_pressure():
    result = (
        scalar_casimir_pressure_pa(
            c1_ev_m4=
                C1,

            density1_kg_m3=
                AU_DENSITY_KG_M3,

            density2_kg_m3=
                AU_DENSITY_KG_M3,

            separation_m=
                SEPARATION_M,

            thickness1_m=
                SPHERE_AU_M,

            thickness2_m=
                PLATE_AU_M,
        )
    )

    assert math.isclose(
        result[
            "pressure_magnitude_pa"
        ],
        0.397023655115379,
        rel_tol=3.0e-9,
    )

    assert (
        result[
            "substrate_scalar_reflection_included"
        ]
        is False
    )


def test_even_one_nm_gold_films_are_empirically_large():
    result = (
        scalar_casimir_pressure_pa(
            c1_ev_m4=
                C1,

            density1_kg_m3=
                AU_DENSITY_KG_M3,

            density2_kg_m3=
                AU_DENSITY_KG_M3,

            separation_m=
                SEPARATION_M,

            thickness1_m=
                1.0e-9,

            thickness2_m=
                1.0e-9,
        )
    )

    assert (
        result[
            "pressure_magnitude_pa"
        ]
        >
        0.110
    )

    assert (
        result[
            "pressure_magnitude_pa"
        ]
        / XI95_PA
        >
        13.0
    )


def test_actual_film_pressure_exceeds_95pct_residual_by_gt47():
    extra = (
        scalar_casimir_pressure_pa(
            c1_ev_m4=
                C1,

            density1_kg_m3=
                AU_DENSITY_KG_M3,

            density2_kg_m3=
                AU_DENSITY_KG_M3,

            separation_m=
                SEPARATION_M,

            thickness1_m=
                SPHERE_AU_M,

            thickness2_m=
                PLATE_AU_M,
        )[
            "pressure_magnitude_pa"
        ]
    )

    assert (
        extra
        / XI95_PA
        >
        47.0
    )


def test_standard_theory_plus_scalar_is_excluded():
    extra = (
        scalar_casimir_pressure_pa(
            c1_ev_m4=
                C1,

            density1_kg_m3=
                AU_DENSITY_KG_M3,

            density2_kg_m3=
                AU_DENSITY_KG_M3,

            separation_m=
                SEPARATION_M,

            thickness1_m=
                SPHERE_AU_M,

            thickness2_m=
                PLATE_AU_M,
        )[
            "pressure_magnitude_pa"
        ]
    )

    gate = (
        empirical_pressure_gate(
            extra_pressure_pa=
                extra,

            measured_pressure_pa=
                MEASURED_PA,

            standard_theory_pressure_pa=
                THEORY_PA,

            confidence_halfwidth_pa=
                XI95_PA,
        )
    )

    assert (
        gate[
            "excluded_at_declared_95pct_interval"
        ]
        is True
    )

    assert (
        gate[
            "mismatch_over_95pct_halfwidth"
        ]
        >
        47.0
    )


def test_pfa_geometry_parameter_is_small():
    assert (
        SEPARATION_M
        / SPHERE_RADIUS_M
        <
        0.0014
    )


def test_device_range_soft_mass_does_not_suppress_200nm_gate():
    result = (
        soft_mass_range_scout(
            required_range_m=
                0.20,

            laboratory_separation_m=
                SEPARATION_M,
        )
    )

    assert (
        result[
            "maximum_mass_ev_for_required_range"
        ]
        <
        1.0e-6
    )

    assert (
        result[
            "m_times_d_over_hbarc"
        ]
        <=
        1.0e-6
        * (
            1.0
            + 1.0e-12
        )
    )

    assert (
        result[
            "massless_laboratory_limit"
        ]
        is True
    )


def test_casimir_momentum_is_inside_current_low_energy_domain():
    result = (
        laboratory_momentum_scout(
            separation_m=
                SEPARATION_M,

            source_hard_scale_ev=
                HARD_EV,

            metric_scale_ev=
                METRIC_EV,
        )
    )

    assert math.isclose(
        result[
            "q_ev"
        ],
        0.986634902,
        rel_tol=2.0e-14,
    )

    assert (
        result[
            "q_over_source_hard"
        ]
        <
        0.018
    )

    assert (
        result[
            "q_over_metric_scale"
        ]
        <
        5.0e-5
    )

    assert (
        result[
            "below_source_hard_scale"
        ]
        is True
    )
