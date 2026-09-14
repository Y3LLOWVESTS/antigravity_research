"""Regressions for 032H17A11B K2 / Wheeler torsion source theorem."""

from __future__ import annotations

import math

import numpy as np

from antigravity_research.agminer.hook17_k2_wheeler_torsion_ward import (
    engineered_k2_ward_gate,
    engineered_torsion_source_gate,
    exact_rest_density_k2_theorem,
    h17a11b_summary,
    k2_published_carrier_gate,
    rest_density_torsion_basis,
    wheeler_eq27_validation_gate,
    wheeler_full_torsion_response,
)


def test_full_wheeler_eq27_reproduces_existing_special_case():
    result = wheeler_eq27_validation_gate()

    assert result[
        "electron_special_case_exact"
    ] is True

    assert result[
        "positron_special_case_exact"
    ] is True

    assert result[
        "existing_special_case_reports_pair_cancellation"
    ] is True


def test_general_wheeler_torsion_is_pair_antisymmetric():
    result = wheeler_eq27_validation_gate()

    assert result[
        "full_eq27_pair_antisymmetry_pass"
    ] is True

    assert result[
        "maximum_pair_antisymmetry_error"
    ] < 1.0e-12


def test_historical_clean_pair_torsion_still_cancels():
    result = engineered_torsion_source_gate()

    assert result[
        "historical_clean_U1_V2_torsion_zero"
    ] is True

    assert math.isclose(
        result[
            "historical_clean_U1_V2_torsion_norm"
        ],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_a10_engineered_pairs_reopen_full_wheeler_torsion():
    result = engineered_torsion_source_gate()

    assert result[
        "engineered_source_state_reopens_full_wheeler_torsion"
    ] is True

    assert math.isclose(
        result[
            "U1_V1_torsion_norm"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "U2_V2_torsion_norm"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_full_rest_density_basis_has_sixteen_real_directions():
    rows = rest_density_torsion_basis()

    assert len(
        rows
    ) == 16

    assert [
        label
        for label, _ in rows
    ] == [
        "D0",
        "D1",
        "D2",
        "D3",
        "R01",
        "I01",
        "R02",
        "I02",
        "R03",
        "I03",
        "R12",
        "I12",
        "R13",
        "I13",
        "R23",
        "I23",
    ]


def test_k2_is_genuinely_massless_protected_vector_carrier():
    result = k2_published_carrier_gate()

    assert result[
        "propagating_particle"
    ] == "MASSLESS_VECTOR"

    assert result[
        "physical_polarizations"
    ] == 2

    assert result[
        "protected_by_symmetry_first_construction"
    ] is True

    assert result[
        "ultralight_mass_parameter_required"
    ] is False

    assert result[
        "a10f2_specific_ultralight_mass_naturalness_obstruction"
    ] is False


def test_engineered_states_fail_generic_exact_k2_ward():
    result = engineered_k2_ward_gate()

    assert result[
        "both_engineered_sources_fail_generic_k2_ward"
    ] is True


def test_single_lightlike_direction_is_accidental_false_green():
    result = engineered_k2_ward_gate()

    assert result[
        "both_engineered_sources_accidentally_pass_lightlike_z"
    ] is True

    assert result[
        "single_lightlike_direction_is_sufficient_source_test"
    ] is False

    assert result[
        "exact_polynomial_ward_test_required"
    ] is True


def test_exact_rest_source_and_ward_maps_have_rank_twelve():
    result = exact_rest_density_k2_theorem()

    assert result[
        "symbolic_exact_arithmetic"
    ] is True

    assert result[
        "wheeler_torsion_source_map_rank"
    ] == 12

    assert result[
        "k2_exact_polynomial_ward_rank"
    ] == 12

    assert result[
        "k2_exact_polynomial_ward_nullity"
    ] == 4


def test_every_k2_ward_null_rest_density_source_is_torsion_silent():
    result = exact_rest_density_k2_theorem()

    assert result[
        "ward_nullspace_source_image_rank"
    ] == 0

    assert result[
        "ward_nullspace_maps_to_exact_zero_torsion_source"
    ] is True

    assert result[
        "nonzero_ward_compatible_wheeler_torsion_source_exists"
    ] is False

    assert result[
        "direct_k2_zero_momentum_rest_density_route_closed"
    ] is True


def test_a11b_closes_only_direct_rest_density_k2_route():
    result = h17a11b_summary()

    assert result[
        "a11a_provenance"
    ] is True

    assert result[
        "new_scientific_fact_engineered_states_source_full_wheeler_torsion"
    ] is True

    assert result[
        "single_lightlike_screen_would_have_false_green"
    ] is True

    assert result[
        "direct_k2_rest_density_wheeler_route_closed"
    ] is True

    assert result[
        "k2_massless_family_globally_closed"
    ] is False

    assert result[
        "k2_nonrest_momentum_textured_dirac_source_closed"
    ] is False

    assert result[
        "k3_historical_clean_route_reopened"
    ] is False

    assert result[
        "metric_gate_authorized"
    ] is False

    assert result[
        "payload_gate_authorized"
    ] is False

    assert result[
        "energy_optimization_authorized"
    ] is False

    assert result[
        "hook17_closed"
    ] is False

    assert result[
        "next"
    ] == (
        "032H17A11C_K2_ONSHELL_NONREST_DIRAC_BILINEAR_"
        "EXACT_WARD_AND_MASSLESS_POLE_GATE"
    )
