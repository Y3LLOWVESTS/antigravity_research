"""Scientific regressions for 032V23 derivative-hypermomentum multipole gate."""

import math

import numpy as np

from antigravity_research.agminer.derivative_hypermomentum_multipole import (
    derivative_gaussian_moments,
    finite_payload_surface_metrics,
    goodkind_shape_only_alpha_scout,
    longitudinal_derivative_oracle,
    persist_v23_failure_rule,
    practical_range_gate,
    required_alpha_for_finite_payload,
    scalarized_portal_scale_ev,
    source_energy_required_at_alpha,
)
from antigravity_research.agminer.storage import (
    Storage,
)


SOURCE_ENERGY_J = 1.0e7
TARGET_A = 9.80665

PAYLOAD_CENTER_Z_M = 0.20
PAYLOAD_RADIUS_M = 0.10

REFERENCE_RANGE_M = 0.20


def reference_gate():
    return (
        practical_range_gate(
            source_energy_j=
                SOURCE_ENERGY_J,

            target_acceleration_m_s2=
                TARGET_A,

            payload_center_z_m=
                PAYLOAD_CENTER_Z_M,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            range_m=
                REFERENCE_RANGE_M,
        )
    )


def test_derivative_source_monopole_is_zero():
    result = (
        derivative_gaussian_moments(
            source_energy_j=
                SOURCE_ENERGY_J
        )
    )

    assert (
        result[
            "zero_monopole"
        ]
        is True
    )

    assert (
        result[
            "monopole_relative_to_source_mass"
        ]
        <
        1.0e-10
    )


def test_derivative_source_first_moment_is_fixed_by_source_mass():
    result = (
        derivative_gaussian_moments(
            source_energy_j=
                SOURCE_ENERGY_J
        )
    )

    assert (
        result[
            "fixed_first_moment"
        ]
        is True
    )

    assert (
        result[
            "first_moment_relative_error"
        ]
        <
        1.0e-10
    )

    assert (
        result[
            "charge_per_joule_free_parameter"
        ]
        is False
    )


def test_generous_longitudinal_oracle_has_repulsive_massive_piece():
    result = (
        longitudinal_derivative_oracle()
    )

    assert (
        result[
            "positive_quadratic_hamiltonian_assumed"
        ]
        is True
    )

    assert (
        result[
            "separated_massive_cross_potential_sign"
        ]
        ==
        "REPULSIVE"
    )


def test_massless_longitudinal_derivative_piece_has_no_exterior_force():
    result = (
        longitudinal_derivative_oracle()
    )

    assert (
        result[
            "massless_separated_long_range_piece"
        ]
        is False
    )

    assert (
        result[
            "full_metric_affine_action_established"
        ]
        is False
    )


def test_finite_payload_surface_is_one_sided_outward():
    result = (
        finite_payload_surface_metrics(
            alpha=
                1.0,

            source_energy_j=
                SOURCE_ENERGY_J,

            payload_center_z_m=
                PAYLOAD_CENTER_Z_M,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            range_m=
                REFERENCE_RANGE_M,
        )
    )

    assert (
        result[
            "all_surface_points_outward"
        ]
        is True
    )


def test_adverse_surface_is_far_payload_pole():
    result = (
        finite_payload_surface_metrics(
            alpha=
                1.0,

            source_energy_j=
                SOURCE_ENERGY_J,

            payload_center_z_m=
                PAYLOAD_CENTER_Z_M,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            range_m=
                REFERENCE_RANGE_M,
        )
    )

    assert math.isclose(
        result[
            "surface_min_mu"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )

    assert math.isclose(
        result[
            "surface_min_source_distance_m"
        ],
        0.30,
        rel_tol=2.0e-14,
    )


def test_reference_finite_payload_alpha_requirement():
    result = (
        required_alpha_for_finite_payload(
            target_acceleration_m_s2=
                TARGET_A,

            source_energy_j=
                SOURCE_ENERGY_J,

            payload_center_z_m=
                PAYLOAD_CENTER_Z_M,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            range_m=
                REFERENCE_RANGE_M,
        )
    )

    assert math.isclose(
        result[
            "alpha_required"
        ],
        2.13059341980305e20,
        rel_tol=5.0e-12,
    )


def test_finite_payload_is_much_harder_than_nearest_point():
    result = (
        required_alpha_for_finite_payload(
            target_acceleration_m_s2=
                TARGET_A,

            source_energy_j=
                SOURCE_ENERGY_J,

            payload_center_z_m=
                PAYLOAD_CENTER_Z_M,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            range_m=
                REFERENCE_RANGE_M,
        )
    )

    assert (
        result[
            "finite_payload_penalty_over_nearest_point"
        ]
        >
        14.0
    )


def test_goodkind_shape_only_scout_reference():
    result = (
        goodkind_shape_only_alpha_scout(
            range_m=
                REFERENCE_RANGE_M
        )
    )

    assert math.isclose(
        result[
            "allowed_endpoint_ratio"
        ],
        1.01
        / 0.99,
        rel_tol=2.0e-15,
    )

    assert math.isclose(
        result[
            "derived_shape_only_alpha_ceiling"
        ],
        0.0506870907684129,
        rel_tol=5.0e-12,
    )


def test_goodkind_scout_is_not_mislabelled_as_published_limit():
    result = (
        goodkind_shape_only_alpha_scout(
            range_m=
                REFERENCE_RANGE_M
        )
    )

    assert (
        result[
            "is_published_95pct_alpha_limit"
        ]
        is False
    )

    assert (
        result[
            "is_digitized_experimental_likelihood"
        ]
        is False
    )

    assert (
        result[
            "is_deliberately_loose_prefight_scout"
        ]
        is True
    )


def test_reference_response_gap_exceeds_4e21():
    result = reference_gate()

    assert (
        result[
            "required_over_shape_scout"
        ]
        >
        4.0e21
    )


def test_reference_empirical_source_energy_floor_exceeds_1e28j():
    result = reference_gate()

    assert (
        result[
            "source_energy_floor_j_at_shape_scout"
        ]
        >
        4.0e28
    )

    assert (
        result[
            "strict_lt10mj_possible_under_shape_scout"
        ]
        is False
    )


def test_reference_empirical_10mj_acceleration_is_tiny():
    result = reference_gate()

    assert (
        result[
            "max_surface_acceleration_for_declared_source_j"
        ]
        <
        3.0e-21
    )


def test_scalarized_portal_target_and_empirical_scales_are_widely_separated():
    result = reference_gate()

    assert (
        result[
            "target_portal_scale_ev_scalarized"
        ]
        <
        1.0e6
    )

    assert (
        result[
            "empirical_portal_scale_min_ev_scalarized"
        ]
        >
        1.0e11
    )

    assert (
        result[
            "portal_scale_ratio_empirical_over_target"
        ]
        >
        2.0e5
    )


def test_entire_goodkind_range_has_gt7e20_gap():
    gaps = []

    for range_m in np.geomspace(
        0.2,
        2.0,
        41,
    ):
        result = (
            practical_range_gate(
                source_energy_j=
                    SOURCE_ENERGY_J,

                target_acceleration_m_s2=
                    TARGET_A,

                payload_center_z_m=
                    PAYLOAD_CENTER_Z_M,

                payload_radius_m=
                    PAYLOAD_RADIUS_M,

                range_m=
                    float(
                        range_m
                    ),
            )
        )

        gaps.append(
            result[
                "required_over_shape_scout"
            ]
        )

    assert (
        min(
            gaps
        )
        >
        7.0e20
    )


def test_v23_failure_memory_is_idempotent(tmp_path):
    storage = Storage(
        tmp_path
        / "agminer.sqlite3"
    )

    try:
        first = (
            persist_v23_failure_rule(
                storage,

                least_bad_gap=
                    7.2e20,

                least_bad_source_energy_floor_j=
                    7.2e27,
            )
        )

        second = (
            persist_v23_failure_rule(
                storage,

                least_bad_gap=
                    7.2e20,

                least_bad_source_energy_floor_j=
                    7.2e27,
            )
        )

        assert first == 1
        assert second == 0

    finally:
        storage.close()


def test_v23_failure_rule_does_not_create_candidates(tmp_path):
    storage = Storage(
        tmp_path
        / "agminer.sqlite3"
    )

    try:
        persist_v23_failure_rule(
            storage,

            least_bad_gap=
                7.2e20,

            least_bad_source_energy_floor_j=
                7.2e27,
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
