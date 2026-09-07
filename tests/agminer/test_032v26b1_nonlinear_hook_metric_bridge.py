"""Scientific regressions for 032V26B1 nonlinear hook-metric preflight."""

from __future__ import annotations

import math

import numpy as np

from antigravity_research.agminer.nonlinear_hook_metric_bridge import (
    STANDARD_GRAVITY_M_S2,
    active_offstate_numerator_gate,
    hook_quadratic_metric_basis,
    normalized_metric_signature,
    quadratic_active_background_derivative,
    quadratic_metric_descendant,
    rest_pair_hook,
    rest_pair_hook_metric_atlas,
    same_action_compatibility_atlas,
    v26b1_gate,
    weak_field_lapse_variation,
    zero_derivative_linear_metric_descendant_gate,
)


def test_rank_parity_closes_zero_derivative_linear_hook_metric_map():
    result = (
        zero_derivative_linear_metric_descendant_gate()
    )

    assert (
        result[
            "zero_derivative_linear_rank2_descendant_exists"
        ]
        is False
    )


def test_rank_parity_does_not_close_derivative_linear_operators():
    result = (
        zero_derivative_linear_metric_descendant_gate()
    )

    assert (
        result[
            "derivative_linear_rank2_descendants_closed"
        ]
        is False
    )

    assert (
        "nabla"
        in result[
            "example_derivative_linear_operator"
        ]
    )


def test_actual_v24_rest_pair_hook_is_nonzero():
    hook = (
        rest_pair_hook()
    )

    assert (
        np.linalg.norm(
            hook
        )
        >
        1.0e-14
    )


def test_quadratic_metric_basis_is_symmetric():
    result = (
        hook_quadratic_metric_basis(
            rest_pair_hook()
        )
    )

    assert (
        result[
            "all_rank2_descendants_symmetric"
        ]
        is True
    )


def test_actual_hook_has_nonzero_quadratic_g00_numerator():
    result = (
        rest_pair_hook_metric_atlas()
    )

    assert (
        result[
            "at_least_one_quadratic_g00_numerator_nonzero"
        ]
        is True
    )

    assert (
        result[
            "basis"
        ][
            "A"
        ][
            "g00_numerator_nonzero"
        ]
        is True
    )

    assert (
        result[
            "basis"
        ][
            "B"
        ][
            "g00_numerator_nonzero"
        ]
        is True
    )


def test_quadratic_active_derivative_obeys_degree_two_identity():
    hook = (
        rest_pair_hook()
    )

    q = (
        quadratic_metric_descendant(
            hook
        )
    )

    derivative = (
        quadratic_active_background_derivative(
            hook,
            hook,
        )
    )

    assert np.allclose(
        derivative,
        2.0
        *
        q,
        atol=1.0e-11,
        rtol=1.0e-12,
    )


def test_offstate_linear_response_is_exactly_zero():
    hook = (
        rest_pair_hook()
    )

    derivative = (
        quadratic_active_background_derivative(
            np.zeros_like(
                hook
            ),
            hook,
        )
    )

    assert np.allclose(
        derivative,
        0.0,
        atol=1.0e-12,
        rtol=0.0,
    )


def test_active_offstate_gate_finds_numerator_not_denominator_gain():
    result = (
        active_offstate_numerator_gate()
    )

    assert (
        result[
            "offstate_linear_metric_response_zero"
        ]
        is True
    )

    assert (
        result[
            "active_linear_metric_response_nonzero"
        ]
        is True
    )

    assert (
        result[
            "active_background_numerator_present"
        ]
        is True
    )

    assert (
        result[
            "small_principal_eigenvalue_required_by_this_algebra"
        ]
        is False
    )


def test_one_g_over_ten_cm_requires_tiny_lapse_variation():
    result = (
        weak_field_lapse_variation(
            acceleration_m_s2=
                STANDARD_GRAVITY_M_S2,

            length_m=
                0.10,
        )
    )

    assert math.isclose(
        result[
            "absolute_delta_g00"
        ],
        2.1822739344396436e-17,
        rel_tol=1.0e-12,
    )


def test_actual_required_lapse_load_is_far_from_metric_singularity():
    hook = (
        rest_pair_hook()
    )

    tensor = (
        quadratic_metric_descendant(
            hook
        )
    )

    lapse = (
        weak_field_lapse_variation()
    )[
        "absolute_delta_g00"
    ]

    result = (
        normalized_metric_signature(
            tensor,
            delta_g00=
                -lapse,
        )
    )

    assert (
        result[
            "lorentzian_signature"
        ]
        is True
    )

    assert (
        result[
            "invertible"
        ]
        is True
    )


def test_representative_large_normalized_load_still_has_lorentz_signature():
    tensor = (
        quadratic_metric_descendant(
            rest_pair_hook()
        )
    )

    result = (
        normalized_metric_signature(
            tensor,
            delta_g00=
                -0.9,
        )
    )

    assert (
        result[
            "lorentzian_signature"
        ]
        is True
    )

    assert (
        result[
            "invertible"
        ]
        is True
    )


def test_published_action_atlas_has_no_current_same_action_survivor():
    rows = (
        same_action_compatibility_atlas()
    )

    assert rows

    assert not any(
        row[
            "current_same_action_survivor"
        ]
        for row
        in rows
    )


def test_wheeler_source_and_marzo_nonlinear_bridge_are_not_silently_stitched():
    rows = {
        row[
            "family"
        ]:
            row
        for row
        in same_action_compatibility_atlas()
    }

    wheeler = rows[
        "WHEELER_2026_GL4_DIRAC_SOURCE"
    ]

    marzo = rows[
        "MARZO_2026_VECTOR_GRAVITON"
    ]

    assert (
        wheeler[
            "explicit_dirac_affine_source"
        ]
        ==
        "YES"
    )

    assert (
        wheeler[
            "current_same_action_survivor"
        ]
        is False
    )

    assert (
        marzo[
            "nonlinear_active_background_bridge_same_action"
        ]
        ==
        "OPEN_NOT_ESTABLISHED"
    )

    assert (
        marzo[
            "current_same_action_survivor"
        ]
        is False
    )


def test_v26b1_promotes_only_design_witness_not_action_oracle():
    gate = (
        v26b1_gate()
    )

    assert (
        gate[
            "intrinsic_dirac_hook_source_preserved"
        ]
        is True
    )

    assert (
        gate[
            "hook_quadratic_rank2_metric_descendant_exists"
        ]
        is True
    )

    assert (
        gate[
            "hook_quadratic_active_background_g00_numerator"
        ]
        is True
    )

    assert (
        gate[
            "published_same_action_v26b1_survivor"
        ]
        is False
    )

    assert (
        gate[
            "full_symmetry_protected_action_established"
        ]
        is False
    )

    assert (
        gate[
            "healthy_mode_projection_authorized"
        ]
        is False
    )

    assert (
        gate[
            "action_oracle_authorized"
        ]
        is False
    )

    assert (
        gate[
            "energy_optimization_authorized"
        ]
        is False
    )

    assert (
        gate[
            "agminer_database_mutation_authorized"
        ]
        is False
    )
