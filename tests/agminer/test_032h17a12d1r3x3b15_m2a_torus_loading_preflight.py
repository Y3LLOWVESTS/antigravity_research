"""B15-M2A finite-torus density and 3D inverse-loading tests."""

import importlib.util
import sys
from pathlib import Path

import numpy as np


MODULE = (
    Path(__file__).resolve().parents[2]
    / "simulations"
    / "032h17a12d1r3x3b15_m2a_torus_loading_preflight.py"
)

spec = importlib.util.spec_from_file_location(
    "b15_m2a_test",
    MODULE,
)

m2a = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m2a
spec.loader.exec_module(m2a)


def test_torus_mass_and_compact_support():
    coords = m2a.grid(0.075)
    density, theta = m2a.torus_theta(coords)

    assert abs(
        np.sum(density) * 0.075**3 - 1.0
    ) < 0.004

    assert theta.max() > 1000.0

    for axis in range(3):
        assert np.all(
            theta.take([0, -1], axis=axis) == 0.0
        )

    # Entire sampled box is outside the first 2 m source ball.
    assert coords[..., 2].min() > 2.0


def test_discrete_magnetic_current_conservation():
    rng = np.random.default_rng(152)

    vector = rng.normal(
        size=(9, 7, 5, 3)
    )

    residual = m2a.div(
        m2a.curl(vector, 1.0),
        1.0,
    )

    assert np.max(np.abs(residual)) < 1e-12


def test_no_matter_gives_no_induced_source():
    rng = np.random.default_rng(151)

    electric = rng.normal(
        size=(7, 9, 5, 3)
    )

    magnetic = rng.normal(
        size=(7, 9, 5, 3)
    )

    charge, current = m2a.current_demand(
        np.zeros((7, 9, 5)),
        electric,
        magnetic,
        1.0,
    )

    assert np.max(np.abs(charge)) == 0.0
    assert np.max(np.abs(current)) == 0.0


def test_joint_polarity_flip_preserves_current_norm():
    rng = np.random.default_rng(154)

    electric = rng.normal(
        size=(7, 9, 5, 3)
    )

    magnetic = rng.normal(
        size=(7, 9, 5, 3)
    )

    theta = rng.normal(
        size=(7, 9, 5)
    )

    charge1, current1 = m2a.current_demand(
        theta,
        electric,
        magnetic,
        1.0,
    )

    charge2, current2 = m2a.current_demand(
        theta,
        -electric,
        -magnetic,
        1.0,
    )

    np.testing.assert_allclose(
        charge2,
        -charge1,
        atol=1e-14,
    )

    np.testing.assert_allclose(
        current2,
        -current1,
        atol=1e-14,
    )


def test_orientation_scope_and_exact_current_identities():
    result = m2a.evaluate(
        0.1,
        np.array([1.0, 0.25, -0.1]),
        {"kind": "synthetic_test"},
    )

    assert result["exterior_source_gap_ge_1m"]
    assert result["theta_boundary_zero"]

    assert not result["loaded_3d_solved"]
    assert not result["complete_energy_certified"]
    assert not result["006d_replaced"]

    tilted = result["modes"][
        "relative_tilt_60deg"
    ]

    assert (
        tilted["induced_rhs_ratio_to_aligned_at_equal_1g"]
        > 0.0
    )

    for row in result["modes"].values():
        assert (
            row["incremental_net_charge_relative"]
            < 1e-11
        )

        assert (
            row[
                "incremental_magnetic_current_divergence_relative"
            ]
            < 1e-11
        )
