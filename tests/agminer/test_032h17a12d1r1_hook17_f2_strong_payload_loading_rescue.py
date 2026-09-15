"""Regressions for 032H17A12D1R1 strongly loaded F2 rescue."""

from __future__ import annotations

import math

import numpy as np

from antigravity_research.agminer.hook17_f2_strong_payload_loading_rescue import (
    FLAT_C1_CROSS_SECTION_MEAN,
    PRIMARY_DENSITY_MODEL,
    REFERENCE_PORTAL_SCALE_EV,
    ROBUSTNESS_DENSITY_MODEL,
    _flat_c1_profile,
    claim_policy_gate,
    geometric_standoff_m,
    loading_coefficient_z,
    one_ev4_j_m3,
    operator_structure_gate,
    payload_density_model_gate,
    payload_density_profile_kg_m3,
    primary_peak_loading_gate,
    provenance_gate,
)


def test_a12c_a12d1_provenance_is_exact():
    result = (
        provenance_gate()
    )

    assert result[
        "pass"
    ] is True

    assert result[
        "a12c_low_capacity_mechanism_preserved"
    ] is True

    assert result[
        "a12d1_closed_only_perturbative_pauli_kernel_reuse"
    ] is True

    assert result[
        "strongly_loaded_solution_was_closed_by_a12d1"
    ] is False


def test_geometric_standoff_remains_exactly_one_meter():
    assert math.isclose(
        geometric_standoff_m(),
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_flat_c1_profile_has_correct_endpoint_behavior():
    s = np.asarray(
        [
            0.0,
            0.25,
            0.5,
            0.75,
            1.0,
            1.25,
        ]
    )

    profile = (
        _flat_c1_profile(
            s
        )
    )

    assert profile[
        0
    ] == 1.0

    assert profile[
        2
    ] == 1.0

    assert (
        0.0
        <
        profile[
            3
        ]
        <
        1.0
    )

    assert profile[
        4
    ] == 0.0

    assert profile[
        5
    ] == 0.0


def test_primary_profile_is_only_mildly_peaked():
    result = (
        payload_density_model_gate()
    )

    assert math.isclose(
        FLAT_C1_CROSS_SECTION_MEAN,
        23.0
        /
        40.0,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    assert (
        1.7
        <
        result[
            "primary_peak_over_average"
        ]
        <
        1.8
    )

    assert result[
        "primary_profile_is_deliberately_optimistic"
    ] is True


def test_robustness_profile_is_more_peaked_than_primary():
    result = (
        payload_density_model_gate()
    )

    assert result[
        "robustness_peak_over_average"
    ] == 3.0

    assert (
        result[
            "robustness_peak_density_kg_m3"
        ]
        >
        result[
            "primary_peak_density_kg_m3"
        ]
    )


def test_payload_density_profiles_are_nonnegative_and_compact():
    rho = np.asarray(
        [
            [
                1.0,
                1.0,
                1.0,
            ]
        ]
    )

    z0 = 3.039736830714133

    z = np.asarray(
        [
            [
                z0,
                z0
                +
                0.1,
                z0
                +
                0.3,
            ]
        ]
    )

    primary = (
        payload_density_profile_kg_m3(
            rho,
            z,
            PRIMARY_DENSITY_MODEL,
        )
    )

    robustness = (
        payload_density_profile_kg_m3(
            rho,
            z,
            ROBUSTNESS_DENSITY_MODEL,
        )
    )

    assert np.all(
        primary
        >=
        0.0
    )

    assert np.all(
        robustness
        >=
        0.0
    )

    assert primary[
        0,
        -1
    ] == 0.0

    assert robustness[
        0,
        -1
    ] == 0.0


def test_one_ev4_conversion_is_in_expected_range():
    value = (
        one_ev4_j_m3()
    )

    assert (
        20.0
        <
        value
        <
        21.0
    )


def test_primary_one_kev_peak_loading_is_strong_and_positive():
    result = (
        primary_peak_loading_gate(
            REFERENCE_PORTAL_SCALE_EV
        )
    )

    assert result[
        "peak_z"
    ] > 1.0

    assert result[
        "peak_epsilon_load"
    ] > 1.0e4


def test_weighted_variational_operator_is_symmetric_positive():
    result = (
        operator_structure_gate()
    )

    assert result[
        "symmetric"
    ] is True

    assert result[
        "all_diagonal_positive"
    ] is True

    assert result[
        "rhs_finite"
    ] is True

    assert result[
        "z_positive"
    ] is True


def test_claim_policy_never_promotes_device_from_r1():
    result = (
        claim_policy_gate()
    )

    assert result[
        "payload_backreaction_added"
    ] is True

    assert result[
        "microscopic_source_backreaction_added"
    ] is False

    assert result[
        "complete_energy_established"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False

    assert result[
        "006d_replaced"
    ] is False
