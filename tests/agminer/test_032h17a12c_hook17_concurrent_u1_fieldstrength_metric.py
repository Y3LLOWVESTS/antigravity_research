"""Regressions for 032H17A12C exact-massless U(1) F^2 metric gate."""

from __future__ import annotations

import math

from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    a12c_provenance_gate,
    canonical_ordinary_source_cost_gate,
    exact_massless_u1_rotation_gate,
    fda_mri_empirical_sanity_gate,
    gauge_invariant_metric_gate,
    h17a12c_summary,
    massless_f2_bvp_gate,
)


def test_a12b_and_a11a_provenance_is_exact():
    result = (
        a12c_provenance_gate()
    )

    assert result[
        "pass"
    ] is True

    assert result[
        "ordinary_stable_payload_silent_current"
    ] == "EM_LIKE_ONLY"

    theorem = result[
        "neutral_atom_direct_silence_theorem"
    ]

    assert theorem[
        "q_n_zero"
    ] is True

    assert theorem[
        "q_p_equals_minus_q_e"
    ] is True


def test_exact_massless_proportional_current_is_basis_rotation():
    result = (
        exact_massless_u1_rotation_gate()
    )

    assert result[
        "ordinary_source_excites_sterile_field"
    ] is False

    assert result[
        "metric_portal_turns_rotation_into_physical_em_field_portal"
    ] is True

    # Correct the old massive-vector interpretation rather than
    # accidentally double-counting the photon-like massless direction.
    assert result[
        "a11a_massive_vector_gminus2_bound_reused"
    ] is False


def test_exact_a12b_symmetry_forbids_old_q_squared_metric():
    result = (
        gauge_invariant_metric_gate()
    )

    assert result[
        "a10e_q_mu_q_nu_portal_transferable_to_exact_massless_a12b"
    ] is False

    assert result[
        "gauge_invariant"
    ] is True

    assert result[
        "off_state_first_variation_zero"
    ] is True

    assert result[
        "active_state_response_nonzero"
    ] is True


def test_massless_f2_bvp_has_strict_whole_payload_1g_and_one_meter_gap():
    result = (
        massless_f2_bvp_gate()[
            "production"
        ]
    )

    assert math.isclose(
        result[
            "geometric_external_standoff_m"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert result[
        "strict_whole_payload_1g_pass"
    ] is True

    assert (
        result[
            "payload_local_acceleration_max_m_s2"
        ]
        >
        9.80665
    )

    assert result[
        "invariant_tidal_response_nonzero"
    ] is True


def test_massless_f2_kill_gate_numerics_are_sufficiently_converged():
    result = (
        massless_f2_bvp_gate()
    )

    assert result[
        "preflight_convergence_pass"
    ] is True

    assert (
        result[
            "grid_energy_relative_difference"
        ]
        <
        0.06
    )

    assert (
        result[
            "domain_energy_relative_difference"
        ]
        <
        0.03
    )

    assert (
        result[
            "production"
        ][
            "source_work_relative_error"
        ]
        <
        1.0e-3
    )


def test_reference_one_kev_field_term_is_only_a_partial_capacity():
    result = (
        massless_f2_bvp_gate()[
            "production"
        ]
    )

    assert (
        2.0
        <
        result[
            "field_energy_j"
        ]
        <
        4.0
    )

    assert result[
        "complete_energy_established"
    ] is False


def test_canonical_ordinary_source_cost_does_not_itself_kill_preflight():
    result = (
        canonical_ordinary_source_cost_gate()
    )

    assert (
        4.0e4
        <
        result[
            "field_only_strict_10mj_portal_scale_ev"
        ]
        <
        5.0e4
    )

    assert (
        4.0e4
        <
        result[
            "field_plus_kinematic_source_strict_10mj_portal_scale_ev"
        ]
        <
        5.0e4
    )

    assert (
        result[
            "partial_total_j"
        ]
        <=
        1.0e7
        *
        (
            1.0
            +
            1.0e-12
        )
    )

    assert result[
        "canonical_source_cost_itself_kills_sub10mj_preflight"
    ] is False


def test_fda_mri_field_gradient_is_orders_beyond_candidate_one_g_gradient():
    result = (
        fda_mri_empirical_sanity_gate()
    )

    assert math.isclose(
        result[
            "fda_b_tesla"
        ],
        1.7,
    )

    assert math.isclose(
        result[
            "fda_spatial_gradient_t_per_m"
        ],
        4.7,
    )

    assert (
        result[
            "fda_grad_b2_over_candidate_1g_gradient"
        ]
        >
        1000.0
    )

    assert result[
        "empirical_sanity_inconsistent_by_more_than_100x"
    ] is True


def test_a12c_closeout_is_scoped_and_preserves_a12b_carrier():
    result = (
        h17a12c_summary()
    )

    assert result[
        "ordinary_em_like_minimal_f2_a12b_realization_closed"
    ] is True

    assert result[
        "a12b_exact_massless_carrier_closed"
    ] is False

    assert result[
        "nonordinary_source_a12b_completion_closed"
    ] is False

    assert result[
        "all_field_strength_metric_portals_closed"
    ] is False

    assert result[
        "hook17_closed"
    ] is False


def test_a12c_does_not_promote_a_device_or_energy_optimization():
    result = (
        h17a12c_summary()
    )

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False

    assert result[
        "complete_energy_optimization_authorized"
    ] is False

    assert result[
        "next"
    ].startswith(
        "032H17A12D_"
    )
