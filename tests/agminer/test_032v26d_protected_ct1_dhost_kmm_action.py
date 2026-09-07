"""Scientific regressions for 032V26D protected cT=1 DHOST/KMM action."""

from __future__ import annotations

import math

import pytest

from antigravity_research.agminer.protected_ct1_dhost_kmm_action import (
    action_specification,
    active_background_gate,
    cosmological_eft_parameters,
    dhost_degeneracy_coefficients,
    identity_scan,
    inherited_failure_separation,
    normalized_linear_f_model,
    offstate_gate,
    v26d_gate,
)


def test_a3_zero_degeneracy_gives_six_fx_squared_over_f():
    result = (
        dhost_degeneracy_coefficients(
            F=
                2.0,

            F_X=
                0.25,

            X=
                0.30,

            A3=
                0.0,
        )
    )

    expected = (
        6.0
        *
        0.25**2
        /
        2.0
    )

    assert math.isclose(
        result[
            "A4"
        ],
        expected,
        rel_tol=1.0e-15,
    )


def test_a3_zero_degeneracy_gives_a5_zero():
    result = (
        dhost_degeneracy_coefficients(
            F=
                2.0,

            F_X=
                0.25,

            X=
                0.30,

            A3=
                0.0,
        )
    )

    assert (
        result[
            "A5"
        ]
        ==
        0.0
    )


def test_a3_zero_exactly_cancels_no_decay_combination():
    result = (
        cosmological_eft_parameters(
            F=
                2.0,

            F_X=
                0.25,

            X=
                0.30,

            A3=
                0.0,
        )
    )

    assert math.isclose(
        result[
            "alpha_H"
        ]
        +
        2.0
        *
        result[
            "beta_1"
        ],
        0.0,
        abs_tol=1.0e-15,
    )


def test_a3_zero_does_not_force_beta1_to_zero_in_active_state():
    result = (
        cosmological_eft_parameters(
            F=
                2.0,

            F_X=
                0.25,

            X=
                0.30,

            A3=
                0.0,
        )
    )

    assert (
        abs(
            result[
                "beta_1"
            ]
        )
        >
        0.0
    )


def test_normalized_linear_f_model_has_exact_active_relation():
    result = (
        normalized_linear_f_model(
            x=
                0.20,

            eta=
                0.50,
        )
    )

    expected_beta = (
        0.50
        *
        0.20
        /
        (
            1.0
            +
            0.50
            *
            0.20
        )
    )

    assert math.isclose(
        result[
            "beta_1"
        ],
        expected_beta,
        rel_tol=1.0e-15,
    )

    assert math.isclose(
        result[
            "alpha_H"
        ],
        -2.0
        *
        expected_beta,
        rel_tol=1.0e-15,
    )


def test_offstate_has_zero_classical_kmm_even_if_fx_nonzero():
    result = (
        offstate_gate()
    )

    assert (
        result[
            "alpha_H"
        ]
        ==
        0.0
    )

    assert (
        result[
            "beta_1"
        ]
        ==
        0.0
    )

    assert (
        result[
            "classical_kmm_zero"
        ]
        is True
    )


def test_offstate_does_not_claim_quantum_silence():
    result = (
        offstate_gate()
    )

    assert (
        result[
            "offstate_quantum_material_descendants_audited"
        ]
        is False
    )

    assert (
        result[
            "offstate_radiative_matching_audited"
        ]
        is False
    )


def test_one_universal_matter_metric_is_declared():
    result = (
        action_specification()
    )

    assert (
        result[
            "physical_metric"
        ]
        ==
        "g_mu_nu"
    )

    assert (
        result[
            "ordinary_matter_minimal_to_physical_metric"
        ]
        is True
    )

    assert (
        result[
            "second_physical_metric_required"
        ]
        is False
    )


def test_same_action_source_vertex_is_explicit_but_solution_not_promoted():
    result = (
        action_specification()
    )

    assert (
        result[
            "same_action_source_vertex_explicit"
        ]
        is True
    )

    assert (
        result[
            "same_action_microscopic_source_solution_established"
        ]
        is False
    )


def test_active_background_is_static_spacelike_not_v21_q_reservoir():
    result = (
        active_background_gate()
    )

    assert (
        result[
            "background_type"
        ]
        ==
        "STATIC_SPACELIKE"
    )

    assert (
        result[
            "partial_t_phi"
        ]
        ==
        0.0
    )

    assert (
        result[
            "spatial_gradient_nonzero"
        ]
        is True
    )


def test_inherited_failure_gate_does_not_reopen_v21_or_v22():
    result = (
        inherited_failure_separation()
    )

    assert (
        result[
            "v21_stationary_time_gradient_q_reopened"
        ]
        is False
    )

    assert (
        result[
            "v22_explicit_disformal_physical_metric_reopened"
        ]
        is False
    )

    assert (
        result[
            "v22_offstate_lesson_still_applies"
        ]
        is True
    )


def test_identity_scan_is_not_energy_or_principal_margin_optimization():
    rows = (
        identity_scan()
    )

    assert rows

    assert all(
        row[
            "energy_point"
        ]
        is False
        for row
        in rows
    )

    assert all(
        row[
            "principal_eigenvalue_tuned"
        ]
        is False
        for row
        in rows
    )


def test_identity_scan_passes_no_decay_relation_everywhere():
    rows = (
        identity_scan()
    )

    assert all(
        row[
            "no_decay_identity_pass"
        ]
        is True
        for row
        in rows
    )


def test_normalized_f_positive_guard_rejects_bad_domain():
    with pytest.raises(
        ValueError
    ):
        normalized_linear_f_model(
            x=
                -2.0,

            eta=
                1.0,
        )


def test_v26d_promotes_only_v26e_not_action_or_energy_oracle():
    gate = (
        v26d_gate()
    )

    assert (
        gate[
            "explicit_same_action_scaffold"
        ]
        is True
    )

    assert (
        gate[
            "one_universal_physical_metric"
        ]
        is True
    )

    assert (
        gate[
            "a3_zero_no_decay_identity"
        ]
        is True
    )

    assert (
        gate[
            "active_offstate_separation_at_eft_identity_level"
        ]
        is True
    )

    assert (
        gate[
            "static_spacelike_source_to_metric_cross_response_established"
        ]
        is False
    )

    assert (
        gate[
            "canonical_health_on_static_spacelike_background_established"
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

    assert (
        gate[
            "v26e_principal_symbol_crossprop_gate_authorized"
        ]
        is True
    )
