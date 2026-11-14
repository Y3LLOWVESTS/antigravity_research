"""B17-M4B4: source/Earth translation and action-envelope checks."""

import math
import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_m4b4_paired_translation import (
    evaluate,
    shifted_material,
    shifted_source,
    source_support_check,
)

from antigravity_research.agminer.hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
)


def test_independent_small_quadratic_envelope_identity():
    """Exact two-variable Lorentzian action derivative control."""
    theta, jp, ja = 0.7, 2.1, -0.8

    def state(t, p, a):
        phi, va = np.linalg.solve(
            [[2.0, t], [-t, 3.0]],
            [p, a],
        )
        on_shell = -0.5 * phi * p + 0.5 * va * a
        return phi, va, on_shell

    phi, av, _ = state(theta, jp, ja)
    eps = 1e-5

    dt = (
        state(theta + eps, jp, ja)[2]
        - state(theta - eps, jp, ja)[2]
    ) / (2 * eps)

    dp = (
        state(theta, jp + eps, ja)[2]
        - state(theta, jp - eps, ja)[2]
    ) / (2 * eps)

    da = (
        state(theta, jp, ja + eps)[2]
        - state(theta, jp, ja - eps)[2]
    ) / (2 * eps)

    assert dt == pytest.approx(phi * av, rel=1e-8)
    assert dp == pytest.approx(-phi, rel=1e-8)
    assert da == pytest.approx(av, rel=1e-8)


@pytest.fixture(scope="module")
def source():
    return assemble_original_aligned_source(0.25)


def test_material_reference_and_enclosure_move(source):
    beta_off, density_off, ground_off = shifted_material(
        source, 0.0, 0.0, 1000.0,
        earth_present=False,
    )

    beta_on, density_on, ground_on = shifted_material(
        source, 0.0, 0.0, 1000.0,
        earth_present=True,
    )

    assert np.min(density_off) >= 0
    assert np.min(density_on) >= 0
    assert np.count_nonzero(ground_off) == 0
    assert np.max(ground_on) > 0.5
    assert np.max(abs(beta_on - beta_off)) > 1

    # Zero-shift material must reproduce the established M4B0 model.
    from antigravity_research.agminer.hook17_r3b_m4b_sparse_earth_loading import (
        material_density,
        MaterialGeometry,
    )

    historical_density, _ = material_density(
        source["field"],
        MaterialGeometry(),
        True,
        True,
    )

    np.testing.assert_allclose(
        density_on,
        historical_density,
        rtol=0,
        atol=1e-10,
    )

    beta_moved, _, _ = shifted_material(
        source, 0.0, 0.01, 1000.0,
        earth_present=True,
    )

    assert np.max(abs(beta_moved - beta_on)) > 0


def test_virtual_shift_does_not_claim_physical_current(source):
    row = source_support_check(source, 2e-4)

    assert row["max_nodal_source_radius_m"] > 0
    assert row["translated_source_is_exact_physical_current"] is False

    moved = shifted_source(source, 1000.0, 2e-4)

    assert np.isfinite(moved["j_phi"]).all()
    assert np.isfinite(moved["j_a"]).all()


def test_common_source_sign_flip(source):
    from antigravity_research.agminer.hook17_r3b_m4b_sparse_earth_loading import (
        _solve_fixed_sources,
    )
    from antigravity_research.agminer.hook17_r3b_m4b2_earth_variational_audit import (
        _on_shell_action,
        _weights,
    )

    beta, _, _ = shifted_material(
        source, 0.0, 0.0, 21147.0,
        earth_present=True,
    )

    base = shifted_source(source, 21147.0, 0.0)
    original = _solve_fixed_sources(base, beta, 1.0)

    flipped = {
        **base,
        "j_phi": -base["j_phi"],
        "j_a": -base["j_a"],
    }

    reversed_state = _solve_fixed_sources(
        flipped,
        beta,
        1.0,
    )

    weights = _weights(source)

    assert _on_shell_action(
        original, base, weights
    ) == pytest.approx(
        _on_shell_action(
            reversed_state,
            flipped,
            weights,
        ),
        rel=1e-10,
    )


def test_high_scale_derivative_identity_and_claim_limits():
    result = evaluate(0.25, 21147.0, 2e-4)

    for key in (
        "earth_action_slope_j_m",
        "craft_action_slope_j_m",
        "paired_translation_defect_fraction",
        "common_shift_finite_difference_j_m",
    ):
        assert math.isfinite(result[key])

    assert result["earth_envelope_relative_error"] < 0.05
    assert result["craft_envelope_relative_error"] < 0.05

    assert result["whole_craft_force_n"] is None
    assert not result["finite_box_artifact_excluded"]
    assert not result["force_as_physical_thrust_certified"]
    assert not result["complete_craft_earth_matter_metric_action"]
    assert not result["source_translation_is_physically_sourced_motion"]
    assert not result["same_action_full_noether_identity_certified"]
    assert result["complete_operating_energy_j"] is None
    assert not result["006d_replaced"]


def test_invalid_parameters():
    for args in (
        (0.25, 0.0, 2e-4),
        (0.25, -5.0, 2e-4),
        (0.25, 1000.0, 0.0),
        (0.15, 1000.0, 0.1),
    ):
        with pytest.raises(ValueError):
            evaluate(*args)
