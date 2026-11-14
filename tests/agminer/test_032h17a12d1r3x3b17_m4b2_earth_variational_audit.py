"""B17-M4B2 reduced-action audits and strict claim boundaries."""

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_m4b2_earth_variational_audit import (
    evaluate,
    _weights,
    _on_shell_action,
    _full_reduced_action,
    _beta,
    _source_at_scale,
)
from antigravity_research.agminer.hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
)
from antigravity_research.agminer.hook17_r3b_m4b_sparse_earth_loading import (
    MaterialGeometry,
    _solve_fixed_sources,
)


@pytest.fixture(scope="module")
def source():
    return assemble_original_aligned_source(0.25)


@pytest.fixture(scope="module")
def control_low():
    return evaluate(0.25, 1000.0, True)


@pytest.fixture(scope="module")
def control_high():
    return evaluate(0.25, 21147.0, True)


def test_source_preserved_but_not_exact(source):
    assert source["electric_relative_net_charge"] < 1e-12
    assert source["electric_outside_source_count"] == 0
    assert source["magnetic_outside_source_count"] == 0
    assert source["synthesized_source_exact_b7_shell"] is False


def test_action_reduction_low(control_low):
    assert control_low["stationary_action_identity_error_j"] < 1e-8
    assert control_low["central_solver_residual"] < 1e-8


def test_action_reduction_high(control_high):
    assert control_high["stationary_action_identity_error_j"] < 1e-5
    assert control_high["central_solver_residual"] < 1e-8


def test_source_fixed_envelope_theorem_low(control_low):
    last = control_low["translation_scan"][-1]
    assert last["relative_derivative_identity_error"] < 0.03


def test_source_fixed_envelope_theorem_high(control_high):
    last = control_high["translation_scan"][-1]
    assert last["relative_derivative_identity_error"] < 1e-4


def test_legacy_tracer_not_variational_translation(
    control_low, control_high,
):
    for result in (control_low, control_high):
        tracer = result["central_legacy_ground_tracer_n"]
        slope = result["translation_scan"][-1][
            "on_shell_action_slope_j_per_m"
        ]
        assert abs(tracer - slope) > 0.2


def test_weighted_reciprocity_and_diagonal_symmetry(control_high):
    symmetry = control_high["weighted_symmetry"]

    assert symmetry["phi_weighted_antisymmetry_max"] < 1e-10
    assert symmetry["a_weighted_antisymmetry_max"] < 1e-10
    assert (
        symmetry["relative_weighted_cross_antisymmetry"]
        < 1e-12
    )


def test_original_b7_source_layer_not_resolved(control_low):
    assert control_low["original_b7_10cm_layer_cells"] < 1
    assert not control_low["b7_layer_resolved"]
    assert not control_low["approximate_source_is_exact_r3b"]


def test_common_source_sign_redefinition(source):
    beta, _, _ = _beta(
        source, MaterialGeometry(), 21147.0, True
    )
    base = _source_at_scale(source, 21147.0)

    original = _solve_fixed_sources(base, beta, 1.0)

    flipped = {
        **base,
        "j_phi": -base["j_phi"],
        "j_a": -base["j_a"],
    }
    reversed_state = _solve_fixed_sources(
        flipped, beta, 1.0
    )

    weights = _weights(source)

    assert _on_shell_action(
        original, base, weights
    ) == pytest.approx(
        _on_shell_action(
            reversed_state, flipped, weights
        ),
        rel=1e-9,
    )


def test_off_state_zero_action(source):
    beta, _, _ = _beta(
        source, MaterialGeometry(), 1000.0, True
    )
    empty = {
        **source,
        "j_phi": np.zeros_like(source["j_phi"]),
        "j_a": np.zeros_like(source["j_a"]),
    }

    state = _solve_fixed_sources(empty, beta, 1.0)
    weights = _weights(source)

    assert _on_shell_action(state, empty, weights) == 0
    assert _full_reduced_action(
        state, empty, beta, weights
    ) == 0


def test_invalid_translation_rejected():
    with pytest.raises(ValueError):
        evaluate(
            0.25, 1000.0, True, steps=(0.2,)
        )

    with pytest.raises(ValueError):
        evaluate(
            0.25, 1000.0, True,
            interface_width_m=-0.1,
        )


def test_three_grids_do_not_certify_thrust():
    for h in (0.3, 0.25, 0.2):
        result = evaluate(
            h, 21147.0, True, steps=(1e-7,)
        )

        assert result["whole_craft_force_n"] is None
        assert result["source_hardware_reaction_n"] is None
        assert not result[
            "earth_gravity_metric_momentum_ledger_closed"
        ]
        assert (
            result["translation_scan"][-1][
                "relative_derivative_identity_error"
            ] < 0.001
        )
