"""Regressions for 032H17A10F1."""

from __future__ import annotations

import math

from antigravity_research.agminer.hook17_marzo_finite_transverse_payload_bvp import (
    h17a10f1_summary,
    on_axis_sphere_comparator_gate,
    primary_bvp_convergence_gate,
    primary_geometric_standoff_m,
    primary_lambda_ev_m2,
    primary_torus_bvp_gate,
    source_rest_energy_gate,
    wheeler_bare_current_normalization_gate,
)
from antigravity_research.agminer.hook17_marzo_physical_scale_payload_loading import (
    empirical_quadratic_metric_gate,
)


def test_wheeler_eq28_scaling_is_exact():
    result = wheeler_bare_current_normalization_gate()

    assert result[
        "eq28_alpha_over_kappa_scaling_verified"
    ] is True

    assert result[
        "maximum_alpha_over_kappa_scaling_error"
    ] < 1.0e-12

    assert result[
        "eq28_response_is_bare_connection_current"
    ] is False


def test_canonical_symmetric_connection_current_is_half_response_magnitude():
    result = wheeler_bare_current_normalization_gate()

    assert math.isclose(
        result[
            "canonical_symmetric_connection_current_relative_to_unit_eq28_response_magnitude"
        ],
        0.5,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    assert result[
        "alpha_cancels_from_canonical_bare_current"
    ] is True


def test_normalization_repair_preserves_pole_but_corrects_residue():
    result = wheeler_bare_current_normalization_gate()

    assert result[
        "corrected_absolute_source_normalization_preflight"
    ] is True

    assert result[
        "a10d_nonzero_pole_overlap_survives_normalization_repair"
    ] is True

    assert result[
        "response_normalized_a10d_residue_16_is_absolute_source_residue"
    ] is False

    assert math.isclose(
        result[
            "corrected_connection_current_residue"
        ],
        4.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "corrected_canonical_pair_pole_coupling_magnitude"
        ],
        2.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_primary_geometry_has_exact_one_metre_external_gap():
    assert math.isclose(
        primary_geometric_standoff_m(),
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_primary_source_and_field_are_exactly_transverse_by_symmetry():
    result = primary_torus_bvp_gate()

    assert result[
        "source_support_compact"
    ] is True

    assert result[
        "source_profile_c1_at_boundary"
    ] is True

    assert result[
        "source_divergence_exactly_zero_by_axisymmetry"
    ] is True

    assert result[
        "field_divergence_exactly_zero_by_axisymmetry"
    ] is True


def test_primary_payload_lambda_has_large_empirical_headroom():
    selected = primary_lambda_ev_m2()

    empirical = empirical_quadratic_metric_gate()[
        "lambda_empirical_max_ev_m2"
    ]

    assert (
        8.0e-30
        <
        selected
        <
        1.3e-29
    )

    assert (
        empirical
        /
        selected
        >
        2.0e4
    )


def test_finite_torus_payload_has_one_g_center_of_mass_response():
    result = primary_torus_bvp_gate()

    assert result[
        "finite_payload_bvp"
    ] is True

    assert result[
        "payload_neutral"
    ] is True

    assert math.isclose(
        result[
            "payload_mass_kg"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    assert result[
        "payload_com_at_least_1g"
    ] is True

    assert math.isclose(
        result[
            "payload_com_outward_acceleration_m_s2"
        ],
        9.80665,
        rel_tol=2.0e-12,
        abs_tol=1.0e-10,
    )


def test_finite_torus_field_energy_and_source_work_agree():
    result = primary_torus_bvp_gate()

    assert (
        1.5e5
        <
        result[
            "field_loading_energy_j"
        ]
        <
        3.0e5
    )

    assert result[
        "source_work_relative_error"
    ] < 1.0e-3

    assert result[
        "field_loading_energy_j"
    ] < 1.0e7


def test_primary_bvp_has_grid_and_domain_convergence():
    result = primary_bvp_convergence_gate()

    assert result[
        "convergence_pass"
    ] is True

    assert result[
        "grid_energy_relative_change"
    ] < 0.03

    assert result[
        "grid_source_count_relative_change"
    ] < 0.03

    assert result[
        "domain_energy_relative_change"
    ] < 0.002


def test_corrected_source_count_has_sub10mj_rest_mass_corridors():
    result = source_rest_energy_gate()

    assert (
        1.0e16
        <
        result[
            "source_pair_count"
        ]
        <
        3.0e16
    )

    assert result[
        "electron_variant_partial_floor_below_10mj"
    ] is True

    assert result[
        "proton_mass_comparator_partial_floor_below_10mj"
    ] is True

    assert (
        result[
            "maximum_particle_mass_gev_before_field_plus_rest_hits_10mj"
        ]
        >
        1.0
    )

    assert result[
        "complete_energy"
    ] is False


def test_compact_on_axis_sphere_exposes_geometry_specific_energy_failure():
    result = on_axis_sphere_comparator_gate()

    assert result[
        "payload_kind"
    ] == "SPHERE"

    assert result[
        "payload_com_at_least_1g"
    ] is True

    assert result[
        "field_loading_energy_j"
    ] > 1.0e9

    assert result[
        "field_loading_energy_j"
    ] > 1.0e7


def test_a10f1_is_finite_reduced_eft_witness_not_complete_model():
    result = h17a10f1_summary()

    assert result[
        "partial_green"
    ] is True

    assert result[
        "finite_neutral_payload_reduced_eft_bvp_established"
    ] is True

    assert math.isclose(
        result[
            "reduced_eft_geometric_external_standoff_m"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert result[
        "on_axis_spherical_payload_current_geometry_rejected_by_energy"
    ] is True

    assert result[
        "payload_shape_independent_performance_established"
    ] is False

    assert result[
        "microscopic_dirac_source_solution_established"
    ] is False

    assert result[
        "full_quantum_rg_uv_certified"
    ] is False

    assert result[
        "complete_energy_established"
    ] is False

    assert result[
        "partial_energy_may_promote_model"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False

    assert result[
        "hook17_closed"
    ] is False

    assert result[
        "next"
    ] == (
        "032H17A10F2_MICROSCOPIC_SOURCE_STATE_REALIZATION_"
        "ULTRALIGHT_NATURALNESS_SUPPORT_REACTION_NONLINEAR_"
        "AND_COMPLETE_ENERGY_CLOSEOUT"
    )
