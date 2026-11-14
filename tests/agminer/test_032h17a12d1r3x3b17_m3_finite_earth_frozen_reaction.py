"""B17-M3 finite-Earth frozen-field tests; NOT a physical lift test."""

import importlib.util
import math
from pathlib import Path
import sys

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_exterior_transmission import (
    normalized_r3b_fit,
    fitted_b_field,
)
from antigravity_research.agminer.hook17_r3b_earth_frozen_reaction import (
    FiniteEarthCylinder,
    sigma_from_fit,
    interaction_energy_j,
    conditional_force_pair,
)
from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    HBAR_C_EV_M,
    REFERENCE_PORTAL_SCALE_EV,
)


@pytest.fixture(scope="module")
def fit():
    return normalized_r3b_fit(0.05)


def test_vectorized_multipoles_match_original_m0(fit):
    scale = fit["amplitude_squared_scale"]

    for rho in (0.0, 0.5, 1.0, 3.0):
        br, bz = fitted_b_field(
            fit["coefficients"], rho, -3.0
        )
        reference = (
            HBAR_C_EV_M**2
            / REFERENCE_PORTAL_SCALE_EV**4
            * scale * (br**2 + bz**2)
        )
        assert math.isclose(
            float(sigma_from_fit(fit, rho, -3)),
            reference,
            rel_tol=1e-13,
        )


def test_sigma_positive_and_field_sign_invariant(fit):
    values = sigma_from_fit(
        fit,
        [0.0, 1.0, 2.0],
        [-3.0, -4.0, -5.0],
    )
    flipped = {
        **fit,
        "coefficients": -fit["coefficients"],
    }
    assert np.all(values >= 0)
    np.testing.assert_allclose(
        values,
        sigma_from_fit(
            flipped, [0, 1, 2], [-3, -4, -5]
        ),
        rtol=1e-14,
    )


def test_finite_patch_and_source_clearance(fit):
    patch = FiniteEarthCylinder(2, 1, 2000)
    assert math.isclose(
        patch.mass_kg, 8000*math.pi
    )
    with pytest.raises(ValueError):
        FiniteEarthCylinder(-1, 1, 2000)
    with pytest.raises(ValueError):
        interaction_energy_j(fit, patch, 2.01)
    with pytest.raises(ValueError):
        sigma_from_fit(fit, 0, -1)


def test_joint_translation_invariance(fit):
    patch = FiniteEarthCylinder(1, 0.5, 2000)

    a = interaction_energy_j(
        fit, patch, 3, 20, 0
    )
    b = interaction_energy_j(
        fit, patch, 3.125, 20, 0.125
    )

    assert math.isclose(a, b, rel_tol=1e-13)


def test_frozen_pair_reciprocity_not_true_recoil(fit):
    result = conditional_force_pair(
        fit, FiniteEarthCylinder(2, 1, 2000),
        3.0, order=20
    )

    assert result["earth_frozen_force_z_n"] < 0
    assert result["source_anchor_frozen_force_z_n"] > 0
    assert result["pair_force_relative_residual"] < 1e-8
    assert (
        result["volume_vs_energy_derivative_relative_residual"]
        < 1e-8
    )
    assert result["source_current_reaction_derived"] is False
    assert result["whole_craft_field_force_n"] is None


def test_quadrature_and_derivative_refinement(fit):
    patch = FiniteEarthCylinder(2, 1, 2000)

    coarse = conditional_force_pair(
        fit, patch, 3, 20, 0.01
    )
    medium = conditional_force_pair(
        fit, patch, 3, 28, 0.005
    )
    fine = conditional_force_pair(
        fit, patch, 3, 36, 0.0025
    )

    def relative(a, b):
        return abs(a-b)/max(1.0, abs(b))

    assert relative(
        medium["earth_frozen_force_z_n"],
        fine["earth_frozen_force_z_n"],
    ) < 5e-5

    assert relative(
        coarse["earth_frozen_force_z_n"],
        fine["earth_frozen_force_z_n"],
    ) < 2e-4


def test_density_linearity_reveals_frozen_approximation(fit):
    a = conditional_force_pair(
        fit, FiniteEarthCylinder(2, 1, 1000),
        3, 20
    )
    b = conditional_force_pair(
        fit, FiniteEarthCylinder(2, 1, 2000),
        3, 20
    )

    assert math.isclose(
        b["earth_frozen_force_z_n"],
        2*a["earth_frozen_force_z_n"],
        rel_tol=1e-12,
    )

    assert not a["complete_action_reaction_certified"]


def test_preloaded_interaction_decreases_with_altitude(fit):
    patch = FiniteEarthCylinder(2, 1, 2000)

    low = conditional_force_pair(
        fit, patch, 3, 20
    )
    high = conditional_force_pair(
        fit, patch, 8, 20
    )

    assert (
        abs(low["earth_frozen_force_z_n"])
        > abs(high["earth_frozen_force_z_n"])
    )


def test_source_off_zero_conditional_force(fit):
    off = {
        **fit,
        "coefficients": np.zeros_like(fit["coefficients"]),
    }

    result = conditional_force_pair(
        off,
        FiniteEarthCylinder(1, 0.25, 2000),
        3,
        order=16,
    )

    assert result["interaction_energy_j"] == 0
    assert result["earth_frozen_force_z_n"] == 0
    assert result["source_anchor_frozen_force_z_n"] == 0
    assert result["earth_force_direct_volume_integral_n"] == 0


def test_full_lift_and_energy_claims_fail_closed():
    path = (
        Path(__file__).resolve().parents[2]
        / "simulations"
        / "032h17a12d1r3x3b17_m3_finite_earth_frozen_reaction.py"
    )

    spec = importlib.util.spec_from_file_location(
        "b17_m3_test_sim", path
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    result = module.run(
        0.05,
        craft_mass_kg=100,
        order=16,
    )

    assert result["r3b_preloaded_field_energy_j"] == pytest.approx(
        1.5429162116460216,
        abs=5e-8,
    )
    assert result["whole_craft_external_force_n"] is None
    assert result["effective_weight_cancellation"] is None
    assert result["field_only_lift"] is None
    assert result["earth_reaction_certified"] is False
    assert result["complete_energy_below_10mj_certified"] is False
    assert result["006d_replaced"] is False
