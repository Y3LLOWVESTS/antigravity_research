"""Regressions for 032H17A12D1R2 loaded source-shape rescue."""

from __future__ import annotations

import numpy as np

from antigravity_research.agminer.hook17_f2_loaded_source_shape_rescue import (
    BRANCH,
    ENERGY_EIGEN_RELATIVE_FLOOR,
    PORTAL_LADDER_EV,
    SOURCE_BASIS_COUNT,
    _capacity_from_margin,
    _normalize_coefficients,
    claim_policy_gate,
    original_a12c_source_profile,
    provenance_gate,
    source_basis_gate,
    source_basis_labels,
    source_basis_profiles,
)


def test_branch_name_is_frozen():
    assert BRANCH == "032H17A12D1R2"


def test_r1_provenance_preserves_exact_failure_scope():
    result = provenance_gate()

    assert result[
        "pass"
    ] is True

    assert result[
        "r1_exact_1kev_original_shape_failed_loaded_sign"
    ] is True

    assert result[
        "a12b_carrier_preserved"
    ] is True

    assert result[
        "a12c_f2_mechanism_preserved"
    ] is True


def test_source_basis_has_declared_dimension():
    assert (
        SOURCE_BASIS_COUNT
        ==
        len(
            source_basis_labels()
        )
    )

    assert SOURCE_BASIS_COUNT == 15


def test_basis_zero_is_exact_original_a12c_source():
    rho = np.linspace(
        0.0,
        2.5,
        17,
    )

    z = np.linspace(
        -2.5,
        2.5,
        19,
    )

    rho_grid, z_grid = np.meshgrid(
        rho,
        z,
    )

    basis = source_basis_profiles(
        rho_grid,
        z_grid,
    )

    original = original_a12c_source_profile(
        rho_grid,
        z_grid,
    )

    assert np.allclose(
        basis[
            0
        ],
        original,
        rtol=0.0,
        atol=0.0,
    )


def test_each_raw_basis_member_is_nonnegative():
    rho = np.linspace(
        0.0,
        2.5,
        23,
    )

    z = np.linspace(
        -2.5,
        2.5,
        25,
    )

    rho_grid, z_grid = np.meshgrid(
        rho,
        z,
    )

    basis = source_basis_profiles(
        rho_grid,
        z_grid,
    )

    assert np.all(
        basis
        >=
        0.0
    )


def test_basis_is_compact_outside_original_source_radius():
    rho = np.asarray(
        [
            [
                2.1,
                0.0,
            ]
        ]
    )

    z = np.asarray(
        [
            [
                0.0,
                2.1,
            ]
        ]
    )

    basis = source_basis_profiles(
        rho,
        z,
    )

    assert np.all(
        basis
        ==
        0.0
    )


def test_basis_gate_preserves_exact_current_conservation():
    result = source_basis_gate()

    assert result[
        "basis_zero_exactly_original_a12c"
    ] is True

    assert result[
        "divergence_zero_by_axisymmetry"
    ] is True

    assert result[
        "all_basis_members_compact_inside_original_source_radius"
    ] is True

    assert result[
        "geometry_modified"
    ] is False


def test_portal_ladder_keeps_one_kev_primary_and_samples_below_above():
    assert 1000.0 in PORTAL_LADDER_EV

    assert min(
        PORTAL_LADDER_EV
    ) < 1000.0

    assert max(
        PORTAL_LADDER_EV
    ) > 1000.0


def test_near_null_response_floor_is_nonzero():
    assert (
        ENERGY_EIGEN_RELATIVE_FLOOR
        >
        0.0
    )

    assert (
        ENERGY_EIGEN_RELATIVE_FLOOR
        >=
        1.0e-10
    )


def test_coefficient_normalization_preserves_direction():
    c = np.asarray(
        [
            2.0,
            -1.0,
            0.5,
        ]
    )

    normalized = (
        _normalize_coefficients(
            c
        )
    )

    assert np.max(
        np.abs(
            normalized
        )
    ) == 1.0

    assert np.allclose(
        normalized,
        c
        /
        2.0,
    )


def test_capacity_from_margin_obeys_homogeneous_scaling():
    capacity = (
        _capacity_from_margin(
            9.80665
            /
            100.0
        )
    )

    assert capacity is not None

    assert abs(
        capacity
        -
        100.0
    ) < 1.0e-10

    assert (
        _capacity_from_margin(
            -1.0
        )
        is None
    )


def test_claim_policy_keeps_few_joule_priority_without_overclaiming():
    result = claim_policy_gate()

    assert result[
        "primary_target_is_exact_1kev_rescue"
    ] is True

    assert result[
        "few_joule_branch_given_special_priority"
    ] is True

    assert result[
        "carrier_modified"
    ] is False

    assert result[
        "metric_function_modified"
    ] is False

    assert result[
        "source_current_conservation_preserved"
    ] is True

    assert result[
        "near_null_response_gain_allowed"
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
