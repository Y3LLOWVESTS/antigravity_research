"""Scientific regressions for 032H17A2 exact healthy hook-MAG projectors."""

import math

import numpy as np

from antigravity_research.agminer.hook17_healthy_mag_projector import (
    clean_v24_source_components,
    h17a2_summary,
    healthy_branch_identity_scan,
    healthy_hook_1plus_branch,
    healthy_hook_2plus_branch,
    mp_hook_1plus_source_numerator,
    mp_hook_2plus_source_numerator,
    same_action_provenance_gate,
    static_fourier_source_gate,
    timelike_rest_pole_projector_gate,
)
from antigravity_research.agminer.nonlinear_hook_metric_bridge import (
    rest_pair_hook,
)


def test_actual_v24_source_is_sparse_nonzero_and_inherited_pure_hook():
    result = (
        clean_v24_source_components()
    )

    assert (
        result[
            "nonzero_component_count"
        ]
        ==
        6
    )

    assert math.isclose(
        result[
            "euclidean_component_norm2"
        ],
        256.0 / 3.0,
        rel_tol=1.0e-12,
    )

    assert (
        result[
            "pure_hook_source_inherited_from_v24_v26c"
        ]
        is True
    )


def test_exact_2plus_source_map_is_nonzero_symmetric_traceless_at_rest():
    result = (
        timelike_rest_pole_projector_gate()
    )

    assert (
        result[
            "hook_2plus_symmetric"
        ]
        is True
    )

    assert (
        result[
            "hook_2plus_traceless"
        ]
        is True
    )

    assert (
        result[
            "hook_2plus_exact_pole_source_nonzero"
        ]
        is True
    )

    assert (
        result[
            "hook_2plus_expected_identity_pass"
        ]
        is True
    )

    assert math.isclose(
        result[
            "hook_2plus_raw_spatial_norm2"
        ],
        32.0,
        rel_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "hook_2plus_projected_spatial_norm2"
        ],
        32.0,
        rel_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "hook_2plus_projector_retention_fraction"
        ],
        1.0,
        rel_tol=1.0e-12,
    )


def test_exact_1plus_source_map_is_nonzero_antisymmetric_at_rest():
    result = (
        timelike_rest_pole_projector_gate()
    )

    assert (
        result[
            "hook_1plus_antisymmetric"
        ]
        is True
    )

    assert (
        result[
            "hook_1plus_exact_pole_source_nonzero"
        ]
        is True
    )

    assert (
        result[
            "hook_1plus_expected_identity_pass"
        ]
        is True
    )

    assert math.isclose(
        result[
            "hook_1plus_raw_spatial_norm2"
        ],
        128.0,
        rel_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "hook_1plus_projected_spatial_norm2"
        ],
        128.0,
        rel_tol=1.0e-12,
    )

    assert math.isclose(
        result[
            "hook_1plus_projector_retention_fraction"
        ],
        1.0,
        rel_tol=1.0e-12,
    )


def test_source_maps_are_linear_in_fourier_momentum():
    tau = (
        rest_pair_hook()
    )

    q = np.array(
        [
            0.7,
            0.2,
            -0.3,
            0.9,
        ]
    )

    n2 = (
        mp_hook_2plus_source_numerator(
            tau,
            q,
        )
    )

    n1 = (
        mp_hook_1plus_source_numerator(
            tau,
            q,
        )
    )

    assert np.allclose(
        mp_hook_2plus_source_numerator(
            tau,
            3.0 * q,
        ),
        3.0 * n2,
    )

    assert np.allclose(
        mp_hook_1plus_source_numerator(
            tau,
            3.0 * q,
        ),
        3.0 * n1,
    )


def test_healthy_2plus_branch_has_positive_canonical_source_strength_identity():
    result = (
        healthy_hook_2plus_branch(
            -1.0,
            -0.25,
        )
    )

    assert (
        result[
            "healthy"
        ]
        is True
    )

    assert (
        result[
            "mass2"
        ]
        >
        0.0
    )

    assert (
        result[
            "positive_residue_source_strength"
        ]
        is True
    )

    assert (
        result[
            "canonical_identity_pass"
        ]
        is True
    )

    assert math.isclose(
        result[
            "canonical_source_norm2"
        ],
        128.0,
        rel_tol=1.0e-12,
    )


def test_healthy_1plus_branch_has_positive_canonical_source_strength_identity():
    result = (
        healthy_hook_1plus_branch(
            -1.0,
            -0.5,
        )
    )

    assert (
        result[
            "healthy"
        ]
        is True
    )

    assert (
        result[
            "mass2"
        ]
        >
        0.0
    )

    assert (
        result[
            "positive_residue_source_strength"
        ]
        is True
    )

    assert (
        result[
            "canonical_identity_pass"
        ]
        is True
    )

    assert math.isclose(
        result[
            "canonical_source_norm2"
        ],
        256.0,
        rel_tol=1.0e-12,
    )


def test_unhealthy_sign_choices_fail_closed():
    assert (
        healthy_hook_2plus_branch(
            +1.0,
            -1.0,
        )[
            "healthy"
        ]
        is False
    )

    assert (
        healthy_hook_2plus_branch(
            -1.0,
            +1.0,
        )[
            "healthy"
        ]
        is False
    )

    assert (
        healthy_hook_1plus_branch(
            +1.0,
            -1.0,
        )[
            "healthy"
        ]
        is False
    )

    assert (
        healthy_hook_1plus_branch(
            -1.0,
            +1.0,
        )[
            "healthy"
        ]
        is False
    )


def test_canonical_identities_survive_widely_separated_healthy_points():
    result = (
        healthy_branch_identity_scan()
    )

    assert (
        result[
            "hook_2plus_all_healthy"
        ]
        is True
    )

    assert (
        result[
            "hook_1plus_all_healthy"
        ]
        is True
    )

    assert (
        result[
            "hook_2plus_identity_all_pass"
        ]
        is True
    )

    assert (
        result[
            "hook_1plus_identity_all_pass"
        ]
        is True
    )

    assert (
        result[
            "hook_2plus_positive_source_strength_all"
        ]
        is True
    )

    assert (
        result[
            "hook_1plus_positive_source_strength_all"
        ]
        is True
    )


def test_static_2plus_source_has_exact_anisotropic_quadratic_form():
    result = (
        static_fourier_source_gate()
    )

    assert (
        result[
            "hook_2plus_exact_anisotropy_identity_pass"
        ]
        is True
    )

    assert (
        result[
            "hook_2plus_quadratic_coefficients_kx_ky_kz"
        ]
        ==
        [
            0.0,
            128.0,
            32.0,
        ]
    )

    assert math.isclose(
        result[
            "hook_2plus_unit_sphere_angular_average_norm2"
        ],
        160.0 / 3.0,
    )

    assert (
        result[
            "hook_2plus_generic_static_gradient_support_nonzero"
        ]
        is True
    )


def test_static_1plus_source_has_exact_anisotropic_quadratic_form():
    result = (
        static_fourier_source_gate()
    )

    assert (
        result[
            "hook_1plus_exact_anisotropy_identity_pass"
        ]
        is True
    )

    assert (
        result[
            "hook_1plus_quadratic_coefficients_kx_ky_kz"
        ]
        ==
        [
            0.0,
            0.0,
            128.0,
        ]
    )

    assert math.isclose(
        result[
            "hook_1plus_unit_sphere_angular_average_norm2"
        ],
        128.0 / 3.0,
    )

    assert (
        result[
            "hook_1plus_generic_static_gradient_support_nonzero"
        ]
        is True
    )


def test_static_gate_does_not_overclaim_green_function_or_payload():
    result = (
        static_fourier_source_gate()
    )

    assert (
        result[
            "static_green_function_evaluated"
        ]
        is False
    )

    assert (
        result[
            "finite_payload_evaluated"
        ]
        is False
    )


def test_same_action_provenance_fail_closed_despite_nonzero_poles():
    result = (
        same_action_provenance_gate()
    )

    assert (
        result[
            "hook_2plus_exact_source_to_pole_nonzero"
        ]
        is True
    )

    assert (
        result[
            "hook_1plus_exact_source_to_pole_nonzero"
        ]
        is True
    )

    assert (
        result[
            "mikura_percacci_reference_matter_interactions_included"
        ]
        is False
    )

    assert (
        result[
            "single_reference_contains_dirac_source_plus_healthy_hook_kinetic"
        ]
        is False
    )

    assert (
        result[
            "hook17_q2_universal_metric_in_same_action"
        ]
        is False
    )

    assert (
        result[
            "same_action_complete"
        ]
        is False
    )

    assert (
        result[
            "literature_stitching_counts_as_same_action"
        ]
        is False
    )


def test_nonzero_exact_projectors_authorize_only_explicit_same_action_construction():
    result = (
        same_action_provenance_gate()
    )

    assert (
        result[
            "explicit_same_action_construction_attempt_authorized"
        ]
        is True
    )


def test_h17a2_green_necessary_condition_but_h17b_stays_closed():
    result = (
        h17a2_summary()
    )

    assert (
        result[
            "decision"
        ].startswith(
            "GREEN_H17A2_"
        )
    )

    assert (
        result[
            "explicit_same_action_construction_attempt_authorized"
        ]
        is True
    )

    assert (
        result[
            "same_action_complete"
        ]
        is False
    )

    assert (
        result[
            "h17b_authorized"
        ]
        is False
    )

    assert (
        result[
            "energy_optimization_authorized"
        ]
        is False
    )

    assert (
        result[
            "mass_candidate_campaign_authorized"
        ]
        is False
    )

    assert (
        result[
            "action_oracle_authorized"
        ]
        is False
    )

    assert (
        result[
            "agminer_database_mutation_authorized"
        ]
        is False
    )


def test_hook17_capacity_claim_boundary_remains_unchanged():
    result = (
        h17a2_summary()
    )

    assert math.isclose(
        result[
            "hook17_reference_capacity_rp1e12_j"
        ],
        17.0676442196,
    )

    assert (
        result[
            "hook17_complete_energy_j"
        ]
        is None
    )

    assert (
        result[
            "strict_complete_operating_target_j"
        ]
        ==
        1.0e7
    )

    assert (
        result[
            "exactly_target_passes"
        ]
        is False
    )


def test_next_is_explicit_single_action_not_energy_optimization():
    result = (
        h17a2_summary()
    )

    assert (
        result[
            "next"
        ].startswith(
            "032H17A3_EXPLICIT_SINGLE_ACTION_"
        )
    )

    assert (
        result[
            "physical_antigravity_model_found"
        ]
        is False
    )

    assert (
        result[
            "certified_sub10mj_model_found"
        ]
        is False
    )

    assert (
        result[
            "practical_device_found"
        ]
        is False
    )

    assert (
        result[
            "v26d_fallback_status"
        ]
        ==
        "PRESERVED_PAUSED_V26E_NOT_ACTIVATED"
    )
