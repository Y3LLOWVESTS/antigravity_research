"""B17-M1 exact constitutive and material-interface regression tests."""

import math
import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_earth_interface import (
    TwoCarrierState,
    classify_lift,
    field_only_energy_density,
    jump_residuals,
    match_no_free_interface,
    original_mirror_state,
    theta_for_density,
)


def test_density_and_theta_reference():
    assert theta_for_density(0) == 0
    assert math.isclose(
        theta_for_density(1.2), -10344.313, rel_tol=1e-6
    )
    assert math.isclose(
        theta_for_density(2000), -17240522, rel_tol=1e-6
    )
    with pytest.raises(ValueError):
        theta_for_density(-1)
    with pytest.raises(ValueError):
        theta_for_density(float("nan"))


def test_all_maxwell_jump_conditions_random():
    rng = np.random.default_rng(2039)

    for _ in range(20):
        state = TwoCarrierState(
            *(rng.normal(size=3) for _ in range(4))
        )
        after = match_no_free_interface(
            state, 3.4, -7.2, normal=(1, 2, 3)
        )
        residuals = jump_residuals(
            state, after, 3.4, -7.2, normal=(1, 2, 3)
        )
        assert max(residuals.values()) < 2e-13


def test_composition_and_reversal():
    rng = np.random.default_rng(13)
    original = TwoCarrierState(
        *(rng.normal(size=3) for _ in range(4))
    )

    air = match_no_free_interface(original, 0, -1300)
    via = match_no_free_interface(air, -1300, -300000)
    direct = match_no_free_interface(original, 0, -300000)
    restored = match_no_free_interface(via, -300000, 0)

    for name in ("e_x", "b_x", "e_y", "b_y"):
        np.testing.assert_allclose(
            getattr(via, name),
            getattr(direct, name),
            rtol=1e-12,
            atol=1e-10,
        )
        np.testing.assert_allclose(
            getattr(restored, name),
            getattr(original, name),
            rtol=0,
            atol=1e-9,
        )


def test_normal_mirror_interface():
    theta = theta_for_density(2000)
    original = original_mirror_state(0, 1)

    after = match_no_free_interface(original, 0, theta)

    assert math.isclose(after.e_x[2], 1 - theta, rel_tol=1e-14)
    assert after.b_y[2] == 1

    expected = ((1 - theta)**2 + 1) / 2

    assert math.isclose(
        field_only_energy_density(after)
        / field_only_energy_density(original),
        expected,
        rel_tol=1e-14,
    )
    assert max(
        jump_residuals(original, after, 0, theta).values()
    ) == 0


def test_sign_redefinition():
    original = original_mirror_state(0.25, -0.8)
    negative = original_mirror_state(-0.25, 0.8)

    after = match_no_free_interface(original, 0, -300)
    flipped = match_no_free_interface(negative, 0, -300)

    for name in ("e_x", "b_x", "e_y", "b_y"):
        np.testing.assert_allclose(
            getattr(after, name),
            -getattr(flipped, name),
            rtol=0,
            atol=1e-12,
        )


def test_gravity_cancellation_and_lift_thresholds():
    unknown = classify_lift(100, None)
    assert unknown["status"] == "NOT_DETERMINED"
    assert unknown["gravity_cancellation"] is None
    assert unknown["pure_field_lift"] is None

    # Illustrative arithmetic, not a physically sourced force.
    equal = classify_lift(100, 980.665)
    assert equal["gravity_cancellation"] is True
    assert equal["pure_field_lift"] is False

    greater = classify_lift(100, 981.665)
    assert greater["pure_field_lift"] is True

    assisted = classify_lift(100, 100)
    assert assisted["auxiliary_hover_thrust_n"] > 0


def test_real_r3b_fit_provenance():
    from antigravity_research.agminer.hook17_r3b_exterior_transmission import (
        normalized_r3b_fit,
    )

    fit = normalized_r3b_fit(0.05)

    assert math.isclose(
        fit["preloaded_energy_j"],
        1.5429162116460216,
        abs_tol=5e-8,
    )
    assert fit["fitted_exterior_rms"] < 0.05
