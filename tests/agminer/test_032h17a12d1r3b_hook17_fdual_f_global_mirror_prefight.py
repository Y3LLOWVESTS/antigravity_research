"""Regressions for 032H17A12D1R3B global mirror/interface preflight."""

from __future__ import annotations

import math

from antigravity_research.agminer.hook17_fdual_f_global_mirror_prefight import (
    A12C_REFERENCE_SIGMA_MAX,
    BRANCH,
    FIT_LMAX_VALUES,
    FIT_RADII_M,
    GRID_SPACINGS_M,
    PRIMARY_FIT_RADIUS_M,
    PRIMARY_LMAX,
    TAPER_THICKNESS_M,
    analytic_mode_energy_ratio,
    claim_policy_gate,
    field_energy_ratio_for_repartition,
    fit_configuration_gate,
    interface_null_geometry_gate,
    polarization_node_corridor,
    provenance_gate,
    required_sigma_gradient_for_one_g_per_m,
)


def test_branch_name_is_frozen():
    assert BRANCH == "032H17A12D1R3B"


def test_provenance_requires_green_r3a_structural_corridor():
    result = provenance_gate()

    assert result[
        "pass"
    ] is True

    assert result[
        "r3a_structural_rescue_survives"
    ] is True

    assert result[
        "r3a_r3b_authorized"
    ] is True


def test_dipole_electric_completion_cost_is_three_quarters_of_original_exterior_B():
    result = analytic_mode_energy_ratio(
        1
    )

    assert math.isclose(
        result[
            "electric_total_over_original_magnetic_exterior"
        ],
        0.75,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )


def test_high_multipole_electric_completion_ratio_approaches_one():
    low = analytic_mode_energy_ratio(
        1
    )

    high = analytic_mode_energy_ratio(
        100
    )

    assert (
        low[
            "electric_total_over_original_magnetic_exterior"
        ]
        <
        high[
            "electric_total_over_original_magnetic_exterior"
        ]
        <
        1.0
    )


def test_equal_E_B_split_is_minimum_field_energy_at_fixed_product():
    assert math.isclose(
        field_energy_ratio_for_repartition(
            1.0
        ),
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    assert (
        field_energy_ratio_for_repartition(
            2.0
        )
        >
        1.0
    )


def test_repartition_energy_is_reciprocal_symmetric():
    assert math.isclose(
        field_energy_ratio_for_repartition(
            4.0
        ),
        field_energy_ratio_for_repartition(
            0.25
        ),
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )


def test_interface_null_geometry_removes_both_large_beta_components():
    result = interface_null_geometry_gate()

    assert result[
        "E_tangential"
    ] == 0.0

    assert result[
        "B_normal"
    ] == 0.0

    assert result[
        "large_beta_Dn_mixing"
    ] == 0.0

    assert result[
        "large_beta_Ht_mixing"
    ] == 0.0

    assert result[
        "exact_interface_mix_null"
    ] is True


def test_interface_null_is_also_a_P_node_not_a_force_solution_by_itself():
    result = interface_null_geometry_gate()

    assert result[
        "E_dot_B"
    ] == 0.0

    assert result[
        "P"
    ] == 0.0

    assert result[
        "metric_force_zero_if_configuration_constant"
    ] is True

    assert result[
        "usable_as_P_node_with_nonzero_gradient"
    ] is True


def test_one_g_sigma_gradient_has_expected_1e16_scale():
    gradient = (
        required_sigma_gradient_for_one_g_per_m()
    )

    assert (
        1.0e-16
        <
        gradient
        <
        1.2e-16
    )


def test_P_node_rotation_across_payload_taper_is_sub_radian():
    result = polarization_node_corridor()

    assert math.isclose(
        result[
            "a12c_sigma_amplitude"
        ],
        A12C_REFERENCE_SIGMA_MAX,
        rel_tol=0.0,
        abs_tol=1.0e-30,
    )

    assert math.isclose(
        result[
            "payload_c1_taper_thickness_m"
        ],
        TAPER_THICKNESS_M,
    )

    assert (
        result[
            "rotation_angle_across_taper_rad"
        ]
        <
        0.2
    )

    assert result[
        "finite_width_taper_still_requires_loaded_solution"
    ] is True


def test_fit_configuration_is_multigrid_multiradius_and_not_cherry_picked():
    result = fit_configuration_gate()

    assert tuple(
        result[
            "grid_spacings_m"
        ]
    ) == GRID_SPACINGS_M

    assert tuple(
        result[
            "fit_radii_m"
        ]
    ) == FIT_RADII_M

    assert tuple(
        result[
            "fit_lmax_values"
        ]
    ) == FIT_LMAX_VALUES

    assert result[
        "primary_fit_radius_m"
    ] == PRIMARY_FIT_RADIUS_M

    assert result[
        "primary_lmax"
    ] == PRIMARY_LMAX


def test_claim_policy_does_not_promote_model_or_device():
    result = claim_policy_gate()

    assert result[
        "primary_goal_preserve_2p656859j_mechanism"
    ] is True

    assert result[
        "surface_charge_physicalized"
    ] is False

    assert result[
        "parity_cp_completed"
    ] is False

    assert result[
        "full_loaded_BVP_completed"
    ] is False

    assert result[
        "complete_energy_established"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "006d_replaced"
    ] is False
