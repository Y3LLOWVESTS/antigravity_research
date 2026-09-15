"""Regressions for 032H17A12D Pauli/magnetization source reopening."""

from __future__ import annotations

from antigravity_research.agminer.hook17_pauli_f2_source_reopen import (
    h17a12d_summary,
    pauli_geometry_gate,
    pauli_source_reference_floor,
    provenance_gate,
    source_energy_at_portal_scale,
    source_selectivity_and_empirical_scope_gate,
    stellar_electron_pauli_bound_gate,
    strict_partial_energy_boundary,
)


def test_a12c_and_a11a_provenance_is_preserved():
    result = provenance_gate()

    assert result[
        "pass"
    ] is True

    assert result[
        "a12c_reduced_f2_1g_1m"
    ] is True

    assert result[
        "a12b_carrier_preserved"
    ] is True

    assert result[
        "a11a_simple_pauli_was_closed_under_old_energy_requirement"
    ] is True


def test_pauli_source_is_exact_curl_of_a12c_source_shape():
    result = pauli_geometry_gate()

    assert result[
        "source_shape_identity_pass"
    ] is True

    assert result[
        "derivative_current_identically_conserved"
    ] is True

    assert result[
        "q_identity_pass"
    ] is True

    assert (
        9.8e-8
        <
        result[
            "q_from_source_radius_ev"
        ]
        <
        1.0e-7
    )


def test_stellar_bound_translates_to_extremely_large_pauli_scale():
    result = (
        stellar_electron_pauli_bound_gate()
    )

    assert (
        1.4e19
        <
        result[
            "minimum_effective_pauli_scale_ev"
        ]
        <
        1.6e19
    )

    assert (
        1.0e-26
        <
        result[
            "maximum_effective_constituent_coupling"
        ]
        <
        2.0e-26
    )


def test_one_kev_reference_source_is_impossible_under_stellar_bound():
    result = (
        pauli_source_reference_floor()
    )

    assert (
        result[
            "optimistic_electron_rest_floor_j"
        ]
        >
        1.0e26
    )

    assert result[
        "complete_energy_established"
    ] is False


def test_lowering_metric_portal_scale_to_q_reopens_partial_energy_overlap():
    geometry = pauli_geometry_gate()

    result = (
        source_energy_at_portal_scale(
            geometry[
                "q_from_source_radius_ev"
            ]
        )
    )

    assert (
        6.0e6
        <
        result[
            "optimistic_electron_rest_floor_j"
        ]
        <
        6.3e6
    )

    assert (
        result[
            "partial_total_j"
        ]
        <
        1.0e7
    )


def test_two_q_margin_already_exceeds_strict_energy_policy():
    geometry = pauli_geometry_gate()

    result = (
        source_energy_at_portal_scale(
            2.0
            *
            geometry[
                "q_from_source_radius_ev"
            ]
        )
    )

    assert (
        result[
            "partial_total_j"
        ]
        >
        2.4e7
    )


def test_exact_strict_boundary_is_only_about_1p28_q():
    result = (
        strict_partial_energy_boundary()
    )

    assert result[
        "partial_overlap_exists_at_portal_scale_equal_q"
    ] is True

    assert (
        1.27
        <
        result[
            "portal_boundary_over_characteristic_q"
        ]
        <
        1.29
    )

    assert (
        0.77
        <
        result[
            "minimum_q_over_portal_scale_inside_sub10mj_corridor"
        ]
        <
        0.80
    )

    assert result[
        "exactly_10mj_passes"
    ] is False


def test_no_two_x_or_ten_x_scale_headroom_survives():
    result = (
        strict_partial_energy_boundary()
    )

    assert result[
        "two_q_scale_margin_sub10mj"
    ] is False

    assert result[
        "ten_q_scale_margin_sub10mj"
    ] is False

    assert result[
        "narrow_eft_edge_overlap_only"
    ] is True

    assert result[
        "parametric_q_over_M_small"
    ] is False


def test_a12c_mri_kill_does_not_automatically_transfer_to_pauli_source():
    result = (
        source_selectivity_and_empirical_scope_gate()
    )

    assert result[
        "source_is_derivative_current"
    ] is True

    assert result[
        "source_is_identically_conserved"
    ] is True

    assert result[
        "source_is_spin_dependent"
    ] is True

    assert result[
        "a12c_em_like_photon_alignment_applies"
    ] is False

    assert result[
        "a12c_mri_photon_field_kill_directly_reused"
    ] is False

    assert result[
        "radiative_kinetic_mixing_certified_zero"
    ] is False


def test_a12d_reopens_only_scoped_edge_corridor_and_promotes_uv_gate():
    result = h17a12d_summary()

    assert result[
        "minimal_electron_pauli_source_partial_corridor_reopened"
    ] is True

    assert result[
        "controlled_local_f2_eft_completion_promoted"
    ] is False

    assert result[
        "explicit_low_scale_uv_completion_closed"
    ] is False

    assert result[
        "a12b_exact_massless_carrier_closed"
    ] is False

    assert result[
        "a12c_gauge_invariant_f2_metric_mechanism_closed"
    ] is False

    assert result[
        "ordinary_em_like_route_remains_closed"
    ] is True

    assert result[
        "metric_bvp_rerun_authorized"
    ] is False

    assert result[
        "complete_energy_optimization_authorized"
    ] is False

    assert result[
        "hook17_closed"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False

    assert result[
        "decision"
    ].startswith(
        "YELLOW_SCOPED_A12D_"
    )

    assert result[
        "next"
    ] == (
        "032H17A12E_PAULI_UV_RADIATIVE_KINETIC_MIXING_"
        "SPIN_SOURCE_EMPIRICAL_AND_SUPPORT_GATE"
    )
