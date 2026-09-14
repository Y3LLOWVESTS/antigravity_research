"""Regressions for 032H17A10D exact protected 1- pole overlap."""

from __future__ import annotations

import math

import numpy as np

from antigravity_research.agminer.hook17_marzo2022_exact_1minus_pole import (
    _benchmark_gate,
    _basis_orthonormality_error,
    _source_coordinates,
    h17a10d_summary,
)


def test_a10c_provenance_is_required_and_preserved():
    result = h17a10d_summary()

    assert result[
        "a10c_source_noether_completion_preserved"
    ] is True

    assert result[
        "published_protected_unique_massive_1minus_family"
    ] is True


def test_rest_frame_1minus_basis_is_orthonormal():
    assert (
        _basis_orthonormality_error()
        <
        1.0e-12
    )


def test_anchor_action_hits_exact_published_pole():
    result = _benchmark_gate(
        "D2_ZERO_ANCHOR"
    )

    assert result[
        "published_health_branch_I_pass"
    ] is True

    assert result[
        "published_mass_squared_exact"
    ] == "1"

    assert result[
        "published_residue_exact"
    ] == "4"

    assert result[
        "action_determinant_zero_at_published_mass"
    ] is True

    assert result[
        "action_determinant_has_simple_pole"
    ] is True

    assert result[
        "action_pole_matrix_rank"
    ] == 3

    assert result[
        "action_pole_nullity"
    ] == 1


def test_anchor_exact_null_vector_and_positive_derivative():
    result = _benchmark_gate(
        "D2_ZERO_ANCHOR"
    )

    expected = np.array(
        [
            math.sqrt(10.0) / 2.0,
            -math.sqrt(2.0),
            -math.sqrt(2.0) / 2.0,
            1.0,
        ]
    )

    assert np.allclose(
        np.asarray(
            result[
                "pole_vector"
            ]
        ),
        expected,
        atol=1.0e-12,
        rtol=0.0,
    )

    assert math.isclose(
        result[
            "pole_derivative_norm"
        ],
        1.5,
        abs_tol=1.0e-12,
        rel_tol=0.0,
    )

    assert result[
        "pole_derivative_positive"
    ] is True


def test_engineered_source_coordinates_are_exact_equal_opposites():
    minus = _source_coordinates(
        "U1_V1",
        1,
    )

    plus = _source_coordinates(
        "U2_V2",
        1,
    )

    expected = np.array(
        [
            -8.0 / math.sqrt(15.0),
            2.0 / math.sqrt(3.0),
            0.0,
            0.0,
        ]
    )

    assert np.allclose(
        minus,
        expected,
        atol=1.0e-12,
        rtol=0.0,
    )

    assert np.allclose(
        plus,
        -expected,
        atol=1.0e-12,
        rtol=0.0,
    )


def test_anchor_source_has_exact_positive_pole_residue_16():
    result = _benchmark_gate(
        "D2_ZERO_ANCHOR"
    )

    for row in result[
        "source_rows"
    ]:
        assert row[
            "pole_overlap_nonzero"
        ] is True

        assert row[
            "source_saturated_residue_positive"
        ] is True

        assert math.isclose(
            row[
                "pole_amplitude_abs"
            ],
            2.0 * math.sqrt(6.0),
            abs_tol=1.0e-10,
            rel_tol=0.0,
        )

        assert math.isclose(
            row[
                "source_saturated_pole_residue"
            ],
            16.0,
            abs_tol=1.0e-9,
            rel_tol=0.0,
        )

        assert math.isclose(
            row[
                "canonical_pole_coupling_magnitude"
            ],
            4.0,
            abs_tol=1.0e-9,
            rel_tol=0.0,
        )

        assert math.isclose(
            row[
                "equivalent_published_constrained_source_norm"
            ],
            2.0,
            abs_tol=1.0e-9,
            rel_tol=0.0,
        )


def test_stueckelberg_scalar_source_zero_at_pole_rest_frame():
    result = _benchmark_gate(
        "D2_ZERO_ANCHOR"
    )

    for row in result[
        "source_rows"
    ]:
        assert row[
            "pole_rest_stueckelberg_scalar_source_zero"
        ] is True


def test_d2_one_tenth_robustness_remains_healthy_and_nonzero():
    result = _benchmark_gate(
        "D2_ONE_TENTH_ROBUSTNESS"
    )

    assert result[
        "published_health_branch_I_pass"
    ] is True

    assert result[
        "published_mass_squared_exact"
    ] == "175/94"

    assert result[
        "published_residue_exact"
    ] == "44986/2209"

    assert result[
        "action_determinant_zero_at_published_mass"
    ] is True

    assert result[
        "unique_pole_direction"
    ] is True

    assert result[
        "pole_derivative_positive"
    ] is True

    assert result[
        "both_engineered_sources_have_nonzero_positive_pole_residue"
    ] is True

    for row in result[
        "source_rows"
    ]:
        assert row[
            "source_saturated_pole_residue"
        ] > 60.0


def test_a10d_green_is_exact_pole_not_physical_model():
    result = h17a10d_summary()

    assert result[
        "partial_green"
    ] is True

    assert result[
        "exact_linearized_healthy_1minus_pole_overlap_established"
    ] is True

    assert result[
        "anchor_exact_residue_16_reproduced"
    ] is True

    assert result[
        "robustness_nonzero_overlap_reproduced"
    ] is True

    assert result[
        "full_covariant_dirac_matter_action_established"
    ] is False

    assert result[
        "universal_physical_metric_established"
    ] is False

    assert result[
        "physical_g00_response_established"
    ] is False


def test_a10d_does_not_authorize_energy():
    result = h17a10d_summary()

    assert result[
        "energy_optimization_authorized"
    ] is False

    assert result[
        "geometry_optimization_authorized"
    ] is False

    assert result[
        "source_charge_per_joule_established"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False


def test_a10d_promotes_compound_matter_metric_gate():
    result = h17a10d_summary()

    assert result[
        "hook17_closed"
    ] is False

    assert result[
        "next"
    ] == (
        "032H17A10E_MARZO_PROTECTED_1MINUS_FULL_COVARIANT_MATTER_"
        "AND_QUADRATIC_UNIVERSAL_METRIC_G00_NATURALNESS_GATE"
    )
