"""Scientific regressions for 032V25A active-state KGB action existence."""

from __future__ import annotations

import math

from antigravity_research.agminer.active_state_kgb_action import (
    action_specification,
    active_offstate_cross_response_demo,
    off_state_tree_gate,
    persist_v25a_metadata,
    protection_gate,
    quadratic_cross_response_invariance,
    required_state_for_canonical_gain,
    source_and_conservation_gate,
    static_spacelike_state,
    v25a_action_existence_gate,
)
from antigravity_research.agminer.storage import (
    Storage,
)


def test_action_has_single_universal_matter_metric():
    result = action_specification()

    assert result[
        "ordinary_matter_minimally_coupled"
    ] is True

    assert result[
        "one_universal_physical_metric"
    ] is True

    assert result[
        "physical_metric"
    ] == "g_munu"


def test_action_preserves_exact_constant_shift_symmetry():
    result = action_specification()

    assert result[
        "exact_constant_shift_symmetry"
    ] is True

    assert result[
        "horndeski_second_order_structure"
    ] is True


def test_hidden_axial_source_operator_is_same_shift_symmetric_form():
    result = source_and_conservation_gate()

    assert result[
        "hidden_axial_derivative_source_operator_exists"
    ] is True

    assert result[
        "exact_scalar_constant_shift_preserved"
    ] is True

    assert result[
        "zero_net_derivative_source_topology_available"
    ] is True


def test_offstate_tree_portal_vanishes():
    result = off_state_tree_gate()

    assert result[
        "cubic_braiding_active"
    ] is False

    assert result[
        "debraided_scalar_matter_coupling_active"
    ] is False

    assert result[
        "tree_level_active_offstate_separation"
    ] is True


def test_offstate_does_not_claim_quantum_empirical_closure():
    result = off_state_tree_gate()

    assert result[
        "quantum_gravitational_descendants_certified"
    ] is False

    assert result[
        "offstate_empirical_closure"
    ] is False


def test_active_spacelike_state_has_nonzero_debraided_matter_coupling():
    result = static_spacelike_state(
        0.10
    )

    assert result[
        "hyperbolic_principal_part"
    ] is True

    assert result[
        "active_debraided_matter_coupling_nonzero"
    ] is True


def test_static_healthy_state_coefficients_match_exact_relations():
    result = static_spacelike_state(
        0.25
    )

    assert math.isclose(
        result[
            "z_time"
        ],
        0.75,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )

    assert math.isclose(
        result[
            "z_transverse"
        ],
        0.75,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )

    assert math.isclose(
        result[
            "z_parallel"
        ],
        1.75,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )


def test_hyperbolicity_closes_at_y_one():
    result = static_spacelike_state(
        1.0
    )

    assert result[
        "hyperbolic_principal_part"
    ] is False

    assert result[
        "kinetic_degenerate"
    ] is True

    assert result[
        "canonical_matter_coupling_times_mpl"
    ] is None


def test_canonical_coupling_at_y_two_thirds_is_one_planck():
    result = static_spacelike_state(
        2.0
        /
        3.0
    )

    assert math.isclose(
        result[
            "canonical_matter_coupling_times_mpl"
        ],
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )


def test_required_margin_for_10x_gain():
    result = required_state_for_canonical_gain(
        10.0
    )

    assert math.isclose(
        result[
            "required_z_time_margin"
        ],
        1.0
        /
        201.0,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )

    assert math.isclose(
        result[
            "reconstructed_canonical_gain_times_planck"
        ],
        10.0,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )


def test_required_margin_for_1000x_gain_is_near_degenerate():
    result = required_state_for_canonical_gain(
        1000.0
    )

    assert result[
        "required_z_time_margin"
    ] < 5.1e-7

    assert result[
        "near_kinetic_degeneracy"
    ] is True

    assert result[
        "strong_coupling_scale_certified"
    ] is False


def test_cross_amplitude_survives_kinetic_diagonalization():
    result = quadratic_cross_response_invariance(
        metric_kinetic=
            2.0,

        scalar_kinetic=
            3.0,

        mixing=
            0.5,
    )

    assert result[
        "healthy_quadratic_channel"
    ] is True

    assert result[
        "response_invariant_under_declared_field_redefinition"
    ] is True

    assert result[
        "relative_error"
    ] < 1.0e-12


def test_cross_amplitude_offstate_zero_active_nonzero():
    result = active_offstate_cross_response_demo()

    assert result[
        "offstate_zero"
    ] is True

    assert result[
        "active_nonzero"
    ] is True

    assert result[
        "active_response_field_redefinition_invariant"
    ] is True


def test_bulk_wbg_context_is_not_full_source_naturalness_certificate():
    result = protection_gate()

    assert result[
        "exact_constant_shift_symmetry"
    ] is True

    assert result[
        "weakly_broken_galileon_gravity_context"
    ] is True

    assert result[
        "hidden_source_preserves_full_galileon_symmetry"
    ] is False

    assert result[
        "full_source_coupled_naturalness_certified"
    ] is False


def test_action_existence_gate_is_green_partial_not_oracle():
    result = v25a_action_existence_gate()

    assert result[
        "explicit_covariant_action_exists"
    ] is True

    assert result[
        "one_universal_physical_metric"
    ] is True

    assert result[
        "tree_level_active_offstate_separation"
    ] is True

    assert result[
        "action_oracle_authorized"
    ] is False


def test_no_sign_payload_or_energy_claims():
    result = v25a_action_existence_gate()

    assert result[
        "outward_sign_established"
    ] is False

    assert result[
        "finite_payload_response_established"
    ] is False

    assert result[
        "source_charge_per_joule_established"
    ] is False

    assert result[
        "complete_operating_energy_established"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False


def test_metadata_idempotent_and_mutates_no_science_tables(
    tmp_path,
):
    storage = Storage(
        tmp_path
        /
        "agminer.sqlite3"
    )

    tables = (
        "models",
        "rejections",
        "survivors",
        "region_rules",
        "action_oracles",
        "collective_scaling",
        "mechanism_metrics",
    )

    try:
        before = {
            table:
                int(
                    storage.connection.execute(
                        f"SELECT COUNT(*) AS count FROM {table}"
                    ).fetchone()[
                        "count"
                    ]
                )
            for table
            in tables
        }

        persist_v25a_metadata(
            storage
        )

        persist_v25a_metadata(
            storage
        )

        after = {
            table:
                int(
                    storage.connection.execute(
                        f"SELECT COUNT(*) AS count FROM {table}"
                    ).fetchone()[
                        "count"
                    ]
                )
            for table
            in tables
        }

        assert before == after

        assert (
            storage.get_metadata(
                "032v25a_explicit_covariant_action_exists"
            )
            ==
            "1"
        )

        assert (
            storage.get_metadata(
                "032v25a_action_oracle_authorized"
            )
            ==
            "0"
        )

    finally:
        storage.close()


def test_v25a_next_gate_is_generalized_kgb_gain_and_rg():
    result = v25a_action_existence_gate()

    assert result[
        "next"
    ] == (
        "032V25B_GENERALIZED_KGB_CANONICAL_GAIN_STRONG_COUPLING_"
        "RG_UV_AND_HIDDEN_SOURCE_SELFCONSISTENCY_GATE"
    )

    assert result[
        "blind_parameter_scan_authorized"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False
