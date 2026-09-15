"""Regressions for 032H17A12D1R2B exact-1-keV source upper-bound gate."""

from __future__ import annotations

import math

import numpy as np

from antigravity_research.agminer.hook17_f2_1kev_source_upper_bound import (
    A12C_REFERENCE_CAPACITY_J,
    BRANCH,
    CAPACITY_TARGETS_J,
    FULL_BASIS_COUNT,
    NESTED_BASIS_COUNTS,
    _project_simplex,
    candidate_patch_centers,
    claim_policy_gate,
    expanded_source_basis_profiles,
    ordered_patch_centers,
    provenance_gate,
    source_basis_labels,
    source_space_gate,
    target_efficiency_m_s2_per_j,
)


def test_branch_name_is_frozen():
    assert BRANCH == "032H17A12D1R2B"


def test_r2_provenance_keeps_continuous_space_open():
    result = provenance_gate()

    assert result[
        "pass"
    ] is True

    assert result[
        "r2_exact_1kev_rescued"
    ] is False

    assert result[
        "continuous_source_space_exhausted"
    ] is False

    assert result[
        "a12b_carrier_preserved"
    ] is True

    assert result[
        "a12c_f2_mechanism_preserved"
    ] is True


def test_candidate_center_count_is_exact():
    assert len(
        candidate_patch_centers()
    ) == 75


def test_farthest_ordering_preserves_all_centers():
    candidates = set(
        candidate_patch_centers()
    )

    ordered = (
        ordered_patch_centers()
    )

    assert len(
        ordered
    ) == 75

    assert len(
        set(
            ordered
        )
    ) == 75

    assert set(
        ordered
    ) == candidates


def test_full_basis_dimension_is_76():
    assert FULL_BASIS_COUNT == 76

    assert len(
        source_basis_labels()
    ) == 76


def test_nested_basis_counts_end_at_full_space():
    assert (
        NESTED_BASIS_COUNTS[
            -1
        ]
        ==
        FULL_BASIS_COUNT
    )

    assert list(
        NESTED_BASIS_COUNTS
    ) == [
        16,
        32,
        52,
        76,
    ]


def test_basis_zero_is_exact_original_source_shape():
    rho = np.linspace(
        0.0,
        2.3,
        15,
    )

    z = np.linspace(
        -2.3,
        2.3,
        17,
    )

    rho_grid, z_grid = np.meshgrid(
        rho,
        z,
    )

    basis = (
        expanded_source_basis_profiles(
            rho_grid,
            z_grid,
        )
    )

    from antigravity_research.agminer.hook17_f2_loaded_source_shape_rescue import (
        original_a12c_source_profile,
    )

    original = (
        original_a12c_source_profile(
            rho_grid,
            z_grid,
        )
    )

    assert np.allclose(
        basis[
            0
        ],
        original,
        rtol=0.0,
        atol=0.0,
    )


def test_all_raw_patch_basis_functions_are_compact():
    rho = np.asarray(
        [
            [
                2.05,
                0.0,
            ]
        ]
    )

    z = np.asarray(
        [
            [
                0.0,
                2.05,
            ]
        ]
    )

    basis = (
        expanded_source_basis_profiles(
            rho,
            z,
        )
    )

    assert np.all(
        basis
        ==
        0.0
    )


def test_simplex_projection_is_valid():
    values = np.asarray(
        [
            -1.0,
            0.2,
            2.0,
            0.4,
        ]
    )

    projected = (
        _project_simplex(
            values
        )
    )

    assert np.all(
        projected
        >=
        0.0
    )

    assert math.isclose(
        float(
            np.sum(
                projected
            )
        ),
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_original_energy_target_requires_about_3p69_response_per_joule():
    required = (
        target_efficiency_m_s2_per_j(
            A12C_REFERENCE_CAPACITY_J
        )
    )

    assert (
        3.68
        <
        required
        <
        3.70
    )


def test_capacity_targets_include_few_joule_and_higher_diagnostics():
    assert A12C_REFERENCE_CAPACITY_J in CAPACITY_TARGETS_J
    assert 10.0 in CAPACITY_TARGETS_J
    assert 100.0 in CAPACITY_TARGETS_J
    assert 1000.0 in CAPACITY_TARGETS_J
    assert 10000.0 in CAPACITY_TARGETS_J


def test_claim_policy_preserves_scope():
    result = claim_policy_gate()

    assert result[
        "few_joule_branch_priority"
    ] is True

    assert result[
        "exact_1kev_primary"
    ] is True

    assert result[
        "continuous_source_space_exhausted"
    ] is False

    assert result[
        "all_possible_source_shapes_closed"
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
