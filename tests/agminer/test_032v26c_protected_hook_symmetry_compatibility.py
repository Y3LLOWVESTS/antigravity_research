"""Scientific regressions for 032V26C protected-hook symmetry gate."""

from __future__ import annotations

import numpy as np

from antigravity_research.agminer.protected_hook_symmetry_compatibility import (
    bms_torsionlike_same_action_gate,
    fully_symmetric_rank3,
    hook_projection_diagnostics,
    marzo_nonlinear_same_action_gate,
    massless_hook_shift_source_ward_gate,
    percacci_sezgin_massive_gate,
    percacci_sezgin_massless_same_action_gate,
    quadratic_metric_hook_shift_gate,
    v26c_action_compatibility_atlas,
    v26c_gate,
)
from antigravity_research.agminer.nonlinear_hook_metric_bridge import (
    rest_pair_hook,
)


def test_actual_v24_hook_has_zero_fully_symmetric_part():
    hook = (
        rest_pair_hook()
    )

    symmetric = (
        fully_symmetric_rank3(
            hook
        )
    )

    assert (
        np.linalg.norm(
            symmetric
        )
        <
        1.0e-12
    )


def test_actual_v24_hook_is_nonzero_pure_hook():
    result = (
        hook_projection_diagnostics(
            rest_pair_hook()
        )
    )

    assert (
        result[
            "hook_nonzero"
        ]
        is True
    )

    assert (
        result[
            "pure_hook_within_tolerance"
        ]
        is True
    )


def test_actual_hook_direct_source_violates_hook_shift_ward_identity():
    result = (
        massless_hook_shift_source_ward_gate()
    )

    assert (
        result[
            "source_shift_variation_nonzero"
        ]
        is True
    )

    assert (
        result[
            "direct_hook_source_respects_published_massless_hook_shift"
        ]
        is False
    )


def test_hook_shift_source_witness_uses_allowed_pure_hook_parameter():
    result = (
        massless_hook_shift_source_ward_gate()
    )

    assert (
        result[
            "actual_v24_source_pure_hook_within_tolerance"
        ]
        is True
    )

    assert (
        result[
            "chosen_ward_parameter"
        ]
        ==
        "xi=J_hook"
    )


def test_quadratic_metric_retains_offstate_first_variation_null():
    result = (
        quadratic_metric_hook_shift_gate()
    )

    assert (
        result[
            "offstate_first_variation_zero"
        ]
        is True
    )


def test_quadratic_metric_breaks_hook_shift_on_active_background():
    result = (
        quadratic_metric_hook_shift_gate()
    )

    assert (
        result[
            "quadratic_metric_g00_nonzero"
        ]
        is True
    )

    assert (
        result[
            "active_first_variation_nonzero"
        ]
        is True
    )

    assert (
        result[
            "quadratic_metric_respects_hook_shift_on_all_backgrounds"
        ]
        is False
    )


def test_quadratic_metric_active_shift_obeys_degree_two_identity():
    result = (
        quadratic_metric_hook_shift_gate()
    )

    assert (
        result[
            "degree_two_identity_pass"
        ]
        is True
    )

    assert (
        result[
            "degree_two_identity_relative_error"
        ]
        <
        1.0e-12
    )


def test_massless_extended_fronsdal_current_h2_same_action_closes():
    result = (
        percacci_sezgin_massless_same_action_gate()
    )

    assert (
        result[
            "current_same_action_hook_source_plus_h2_metric"
        ]
        is False
    )

    assert (
        result[
            "current_h2_scaffold_closed_for_this_published_massless_sector"
        ]
        is True
    )

    assert (
        result[
            "all_metric_affine_gravity_closed"
        ]
        is False
    )


def test_massive_spin3_sector_is_not_falsely_promoted_or_globally_closed():
    result = (
        percacci_sezgin_massive_gate()
    )

    assert (
        result[
            "healthy_massive_spin3_region_reported"
        ]
        is True
    )

    assert (
        result[
            "current_same_action_survivor"
        ]
        is False
    )

    assert (
        result[
            "sector_globally_closed"
        ]
        is False
    )


def test_bms_representation_survives_but_clean_trace_channel_remains_closed():
    result = (
        bms_torsionlike_same_action_gate()
    )

    assert (
        result[
            "actual_hook_to_torsionlike_representation_map"
        ]
        is True
    )

    assert (
        result[
            "clean_pair_source_addition_survives_map"
        ]
        is True
    )

    assert (
        result[
            "clean_rest_pair_direct_protected_trace_vector_source_closed"
        ]
        is True
    )

    assert (
        result[
            "other_protected_vector_channels_closed"
        ]
        is False
    )


def test_marzo_nonlinear_branch_remains_open_without_same_action_source_match():
    result = (
        marzo_nonlinear_same_action_gate()
    )

    assert (
        result[
            "consistent_cubic_deformation_found"
        ]
        is True
    )

    assert (
        result[
            "v24d_linear_route_closed"
        ]
        is True
    )

    assert (
        result[
            "nonlinear_completion_globally_closed"
        ]
        is False
    )

    assert (
        result[
            "current_same_action_survivor"
        ]
        is False
    )


def test_current_mag_action_atlas_contains_no_same_action_survivor():
    rows = (
        v26c_action_compatibility_atlas()
    )

    assert rows

    assert not any(
        row[
            "same_action_survivor"
        ]
        for row
        in rows
    )


def test_v26c_parks_mag_and_promotes_dhost_action_gate_without_overclaim():
    gate = (
        v26c_gate()
    )

    assert (
        gate[
            "v24_intrinsic_dirac_hook_source_preserved"
        ]
        is True
    )

    assert (
        gate[
            "v26b1_quadratic_algebraic_numerator_preserved"
        ]
        is True
    )

    assert (
        gate[
            "protected_massless_hook_h2_same_action_survives"
        ]
        is False
    )

    assert (
        gate[
            "all_metric_affine_gravity_closed"
        ]
        is False
    )

    assert (
        gate[
            "intrinsic_dirac_hypermomentum_closed"
        ]
        is False
    )

    assert (
        gate[
            "expensive_mag_noether_completion_authorized"
        ]
        is False
    )

    assert (
        gate[
            "mag_energy_optimization_authorized"
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
            "agminer_database_mutation_authorized"
        ]
        is False
    )

    assert (
        gate[
            "protected_ct1_dhost_kmm_explicit_action_gate_authorized"
        ]
        is True
    )
