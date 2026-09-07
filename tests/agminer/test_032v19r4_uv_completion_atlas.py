"""Regressions for the 032V19R4 UV-completion atlas."""

import math

from antigravity_research.agminer.uv_completion_atlas import (
    atlas_records,
    gev_m2_to_ev_m2,
    linear_scalar_tower_coefficients,
    narrow_band_linear_scalar_bound,
    same_vertex_screening_scout,
    z2_loop_generated_xt_scale,
)


C1 = 1.5142715050689224e-18
HARD_EV = 56.92491792612398

STATIC_J = 3681919.075350863
TARGET_J = 1.0e7

R3_DECLARED_DX = 1.1911552455145487e-08
R3_DECLARED_X_ENERGY_J = 0.38884442498637145

SOURCE_X_INVENTORY = (
    R3_DECLARED_X_ENERGY_J
    / R3_DECLARED_DX
)

UPDATED_LOOSE_GRAPHICAL_G2 = 1.0e-14

R3_WEAKEST_SINGLE_G2 = 4.94085661597683e-10


def bound():
    return (
        narrow_band_linear_scalar_bound(
            target_c1_ev_m4=
                C1,

            minimum_mediator_mass_ev=
                HARD_EV,

            total_yukawa_g2_limit_gev_m2=
                UPDATED_LOOSE_GRAPHICAL_G2,

            source_x_inventory_j_per_ev_m4=
                SOURCE_X_INVENTORY,

            base_static_energy_j=
                STATIC_J,

            energy_limit_j=
                TARGET_J,
        )
    )


def test_single_scalar_saturates_cauchy():
    result = (
        linear_scalar_tower_coefficients(
            masses_ev=[
                100.0,
            ],

            matter_couplings_ev_m1=[
                2.0e-6,
            ],

            x_couplings_ev_m1=[
                3.0e-3,
            ],
        )
    )

    assert (
        result[
            "cauchy_satisfied"
        ]
        is True
    )

    assert math.isclose(
        result[
            "cauchy_saturation_ratio"
        ],
        1.0,
        rel_tol=1.0e-14,
    )


def test_generic_scalar_tower_obeys_cauchy():
    result = (
        linear_scalar_tower_coefficients(
            masses_ev=[
                60.0,
                80.0,
                120.0,
            ],

            matter_couplings_ev_m1=[
                2.0e-7,
                -3.0e-7,
                1.5e-7,
            ],

            x_couplings_ev_m1=[
                4.0e-4,
                2.0e-4,
                -1.0e-4,
            ],
        )
    )

    assert (
        result[
            "cauchy_satisfied"
        ]
        is True
    )

    assert (
        result[
            "cauchy_saturation_ratio"
        ]
        <
        1.0
    )


def test_gev_to_ev_inverse_square_conversion():
    assert math.isclose(
        gev_m2_to_ev_m2(
            1.0e-14
        ),
        1.0e-32,
        rel_tol=0.0,
        abs_tol=0.0,
    )


def test_r3_source_x_inventory_reconstructed():
    assert math.isclose(
        SOURCE_X_INVENTORY,
        32644311.180311393,
        rel_tol=2.0e-14,
    )


def test_narrow_band_dx_floor():
    result = bound()

    assert math.isclose(
        result[
            "d_x_min_ev_m4"
        ],
        0.3715201134629564,
        rel_tol=2.0e-14,
    )


def test_narrow_band_x_companion_exceeds_12_mj():
    result = bound()

    assert (
        result[
            "x_companion_energy_min_j"
        ]
        >
        1.21e7
    )


def test_narrow_band_current_source_fails_strict_10mj():
    result = bound()

    assert (
        result[
            "base_plus_x_floor_j"
        ]
        >
        1.58e7
    )

    assert (
        result[
            "passes_strict_energy_limit"
        ]
        is False
    )


def test_x_companion_exceeds_remaining_budget():
    result = bound()

    assert (
        result[
            "x_energy_over_remaining_budget"
        ]
        >
        1.9
    )


def test_same_vertex_screening_requires_subpercent_amplitude():
    result = (
        same_vertex_screening_scout(
            unscreened_g2_gev_m2=
                R3_WEAKEST_SINGLE_G2,

            empirical_g2_limit_gev_m2=
                UPDATED_LOOSE_GRAPHICAL_G2,
        )
    )

    assert (
        result[
            "required_matter_amplitude_retention_max"
        ]
        <
        0.0046
    )

    assert (
        result[
            "active_x_dependent_descreening_required_for_rescue"
        ]
        is True
    )


def test_same_vertex_screening_does_not_preserve_c1_target():
    result = (
        same_vertex_screening_scout(
            unscreened_g2_gev_m2=
                R3_WEAKEST_SINGLE_G2,

            empirical_g2_limit_gev_m2=
                UPDATED_LOOSE_GRAPHICAL_G2,
        )
    )

    assert (
        result[
            "same_vertex_target_preserved_without_descreening"
        ]
        is False
    )


def test_z2_loop_scaffold_scale_is_kev():
    result = (
        z2_loop_generated_xt_scale(
            target_c1_ev_m4=
                C1
        )
    )

    assert (
        6.7e3
        <
        result[
            "equal_portal_scale_ev"
        ]
        <
        6.9e3
    )

    assert (
        result[
            "equal_portal_scale_ev"
        ]
        / HARD_EV
        >
        100.0
    )


def test_z2_loop_scaffold_is_not_uv_completion():
    result = (
        z2_loop_generated_xt_scale(
            target_c1_ev_m4=
                C1
        )
    )

    assert (
        result[
            "linear_offstate_single_mediator_yukawa"
        ]
        is False
    )

    assert (
        result[
            "xt_counterterm_symmetry_allowed"
        ]
        is True
    )

    assert (
        result[
            "finite_c1_sign_predicted_without_uv_boundary_condition"
        ]
        is False
    )

    assert (
        result[
            "complete_uv_origin"
        ]
        is False
    )


def test_atlas_keeps_goldstone_and_loop_routes_open():
    records = {
        row[
            "family"
        ]:
        row
        for row in atlas_records()
    }

    assert (
        records[
            "DIRECT_SHIFT_PROTECTED_GOLDSTONE_KINETIC_METRIC"
        ][
            "status"
        ]
        ==
        "YELLOW_HIGHEST_PRIORITY"
    )

    assert (
        records[
            "Z2_LOOP_GENERATED_J0_PORTAL"
        ][
            "status"
        ]
        ==
        "YELLOW_SECOND_PRIORITY"
    )

    assert (
        records[
            "TREE_SPIN2_POSITIVE_C1"
        ][
            "status"
        ]
        ==
        "CLOSED"
    )
