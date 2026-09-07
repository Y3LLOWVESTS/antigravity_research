"""Regressions for 032V22 localized disformal / provenance repair."""

import math

from antigravity_research.agminer.localized_disformal_activation import (
    constant_disformal_empirical_b_cap,
    maximum_cutoff_ratio_for_strict_target,
    minimum_gradient_taper_scout,
    optimistic_localized_partial_floor,
    persist_v22_rules,
    provenance_repair_status,
    quartic_disformal_hard_cutoff_descent,
    single_scale_minimum_metric_scale_ev,
    source_scale_comparison,
)
from antigravity_research.agminer.storage import (
    Storage,
)


AU_DENSITY = 19300.0

SEPARATION_M = 200.0e-9
SPHERE_AU_M = 180.0e-9
PLATE_AU_M = 210.0e-9
ALLOWED_PA = 0.00764

TARGET_J = 1.0e7
TARGET_A = 9.80665

PAYLOAD_RADIUS = 0.10
SOURCE_RADIUS = 0.10
H = 0.10

EXPECTED_B_CAP = 2.5691838555e-20
EXPECTED_SINGLE_M = 18736.513184

V21_K_CAP = 4.63719171872628e-21
V21_Q2_MIN_INVERTIBLE = 2.0539670618763077e-13

R2_B = 6.123454611098919
R2_F = 22.70625323988203

V21_HALF_CAP_S2 = 18824.099298090347


def bcap():
    return (
        constant_disformal_empirical_b_cap(
            gold_density_kg_m3=
                AU_DENSITY,

            separation_m=
                SEPARATION_M,

            sphere_gold_thickness_m=
                SPHERE_AU_M,

            plate_gold_thickness_m=
                PLATE_AU_M,

            allowed_extra_pressure_pa=
                ALLOWED_PA,
        )
    )


def single_m():
    return (
        single_scale_minimum_metric_scale_ev(
            empirical_b_cap_ev_m4=
                bcap()[
                    "b_cap_ev_m4"
                ]
        )
    )


def single_floor():
    return (
        optimistic_localized_partial_floor(
            metric_scale_ev=
                single_m(),

            target_acceleration_m_s2=
                TARGET_A,

            gradient_scale_m=
                H,

            payload_radius_m=
                PAYLOAD_RADIUS,

            source_radius_m=
                SOURCE_RADIUS,
        )
    )


def threshold():
    return (
        maximum_cutoff_ratio_for_strict_target(
            empirical_single_scale_m_ev=
                single_m(),

            target_energy_j=
                TARGET_J,

            target_acceleration_m_s2=
                TARGET_A,

            gradient_scale_m=
                H,

            payload_radius_m=
                PAYLOAD_RADIUS,

            source_radius_m=
                SOURCE_RADIUS,
        )
    )


def test_constant_disformal_b_cap():
    result = bcap()

    assert math.isclose(
        result[
            "b_cap_ev_m4"
        ],
        EXPECTED_B_CAP,
        rel_tol=5.0e-9,
    )


def test_single_scale_metric_minimum():
    assert math.isclose(
        single_m(),
        EXPECTED_SINGLE_M,
        rel_tol=5.0e-9,
    )


def test_hard_cutoff_descent_hits_b_cap():
    result = (
        quartic_disformal_hard_cutoff_descent(
            metric_scale_ev=
                single_m(),

            cutoff_ratio=
                1.0,
        )
    )

    assert math.isclose(
        result[
            "induced_constant_disformal_b_ev_m4"
        ],
        bcap()[
            "b_cap_ev_m4"
        ],
        rel_tol=8.0e-9,
    )

    assert (
        result[
            "scheme_independent_physical_prediction"
        ]
        is False
    )


def test_descent_scales_as_cutoff_ratio_fourth_power():
    full = (
        quartic_disformal_hard_cutoff_descent(
            metric_scale_ev=
                single_m(),

            cutoff_ratio=
                1.0,
        )[
            "induced_constant_disformal_b_ev_m4"
        ]
    )

    half = (
        quartic_disformal_hard_cutoff_descent(
            metric_scale_ev=
                single_m(),

            cutoff_ratio=
                0.5,
        )[
            "induced_constant_disformal_b_ev_m4"
        ]
    )

    assert math.isclose(
        half
        / full,
        0.5**4,
        rel_tol=2.0e-14,
    )


def test_single_scale_optimistic_floor_is_about_275mj():
    state = single_floor()

    assert (
        2.74e8
        <
        state[
            "partial_floor_j"
        ]
        <
        2.77e8
    )


def test_single_scale_optimum_balances_q_and_psi_energy():
    state = single_floor()

    ratio = (
        state[
            "q_payload_volume_energy_j"
        ]
        /
        state[
            "psi_gradient_energy_j"
        ]
    )

    assert (
        0.999
        <
        ratio
        <
        1.001
    )


def test_single_scale_source_hard_margin_is_large():
    state = single_floor()

    assert (
        state[
            "metric_scale_over_hard_derivative_scale"
        ]
        >
        150.0
    )


def test_cutoff_ratio_threshold_is_about_0p4365():
    result = threshold()

    assert (
        0.435
        <
        result[
            "maximum_cutoff_over_metric_scale_for_lt_target"
        ]
        <
        0.438
    )


def test_cutoff_ratio_boundary_is_10mj():
    result = threshold()

    assert math.isclose(
        result[
            "floor_at_boundary_j"
        ],
        TARGET_J,
        rel_tol=2.0e-7,
    )

    assert (
        result[
            "strict_pass_requires_smaller_ratio"
        ]
        is True
    )


def test_localized_wall_hold_time_is_tens_of_ms():
    q2 = (
        1.1
        * V21_Q2_MIN_INVERTIBLE
    )

    lambda_ev = (
        q2
        / V21_K_CAP
    )**0.125

    result = (
        minimum_gradient_taper_scout(
            q2_ev4=
                q2,

            lambda_ev=
                lambda_ev,

            active_radius_m=
                0.31,

            wall_thickness_m=
                0.10,

            chi=
                1.0,
        )
    )

    assert (
        0.044
        <
        result[
            "hold_time_s"
        ]
        <
        0.045
    )


def test_localized_wall_inventory_is_kj_not_mj():
    q2 = (
        1.1
        * V21_Q2_MIN_INVERTIBLE
    )

    lambda_ev = (
        q2
        / V21_K_CAP
    )**0.125

    result = (
        minimum_gradient_taper_scout(
            q2_ev4=
                q2,

            lambda_ev=
                lambda_ev,

            active_radius_m=
                0.31,

            wall_thickness_m=
                0.10,
        )
    )

    assert (
        6.5e3
        <
        result[
            "wall_gradient_field_inventory_j"
        ]
        <
        6.8e3
    )


def test_field_swing_rate_is_not_declared_dissipated_power():
    q2 = (
        1.1
        * V21_Q2_MIN_INVERTIBLE
    )

    lambda_ev = (
        q2
        / V21_K_CAP
    )**0.125

    result = (
        minimum_gradient_taper_scout(
            q2_ev4=
                q2,

            lambda_ev=
                lambda_ev,

            active_radius_m=
                0.31,

            wall_thickness_m=
                0.10,
        )
    )

    assert (
        1.4e5
        <
        result[
            "field_energy_swing_rate_w"
        ]
        <
        1.6e5
    )

    assert (
        result[
            "field_energy_swing_rate_is_dissipated_power"
        ]
        is False
    )


def test_axial_scale_proximity_is_not_source_match():
    result = (
        source_scale_comparison(
            axial_b_ev=
                R2_B,

            axial_fpsi_ev=
                R2_F,

            required_s2_ev4=
                V21_HALF_CAP_S2,
        )
    )

    assert (
        result[
            "relative_difference"
        ]
        <
        0.02
    )

    assert (
        result[
            "microscopic_source_match"
        ]
        is False
    )

    assert (
        result[
            "same_profile_proved"
        ]
        is False
    )


def test_v20_a2_provenance_is_repaired():
    result = (
        provenance_repair_status()
    )

    assert (
        result[
            "v20_a2_was_new_untested_family"
        ]
        is False
    )

    assert (
        result[
            "minimal_branch_closed_by_032t"
        ]
        is True
    )

    assert (
        result[
            "linear_t_only_rank3_monopole_closed_by_032u"
        ]
        is True
    )

    assert (
        result[
            "derivative_multipole_frontier_open"
        ]
        is True
    )


def test_v22_region_rules_are_idempotent(tmp_path):
    storage = Storage(
        tmp_path
        / "agminer.sqlite3"
    )

    try:
        first = (
            persist_v22_rules(
                storage,

                single_scale_floor_j=
                    single_floor()[
                        "partial_floor_j"
                    ],

                single_scale_metric_ev=
                    single_m(),

                b_cap_ev_m4=
                    bcap()[
                        "b_cap_ev_m4"
                    ],

                cutoff_ratio_threshold=
                    threshold()[
                        "maximum_cutoff_over_metric_scale_for_lt_target"
                    ],
            )
        )

        second = (
            persist_v22_rules(
                storage,

                single_scale_floor_j=
                    single_floor()[
                        "partial_floor_j"
                    ],

                single_scale_metric_ev=
                    single_m(),

                b_cap_ev_m4=
                    bcap()[
                        "b_cap_ev_m4"
                    ],

                cutoff_ratio_threshold=
                    threshold()[
                        "maximum_cutoff_over_metric_scale_for_lt_target"
                    ],
            )
        )

        assert first == 2
        assert second == 0

    finally:
        storage.close()


def test_v22_rules_do_not_create_models_or_rejections(tmp_path):
    storage = Storage(
        tmp_path
        / "agminer.sqlite3"
    )

    try:
        persist_v22_rules(
            storage,

            single_scale_floor_j=
                single_floor()[
                    "partial_floor_j"
                ],

            single_scale_metric_ev=
                single_m(),

            b_cap_ev_m4=
                bcap()[
                    "b_cap_ev_m4"
                ],

            cutoff_ratio_threshold=
                threshold()[
                    "maximum_cutoff_over_metric_scale_for_lt_target"
                ],
        )

        models = int(
            storage.connection.execute(
                "SELECT COUNT(*) AS count FROM models"
            ).fetchone()[
                "count"
            ]
        )

        rejections = int(
            storage.connection.execute(
                "SELECT COUNT(*) AS count FROM rejections"
            ).fetchone()[
                "count"
            ]
        )

        assert models == 0
        assert rejections == 0

    finally:
        storage.close()
