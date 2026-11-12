"""B15-M2C exact angular identities and scope tests."""

import importlib.util
import sys
from pathlib import Path

import numpy as np


MODULE = (
    Path(__file__).resolve().parents[2]
    / "simulations"
    / "032h17a12d1r3x3b15_m2c_angular_routing_gate.py"
)

spec = importlib.util.spec_from_file_location(
    "b15_m2c", MODULE
)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def test_equal_field_angle_identity_for_local_rotations():
    rng = np.random.default_rng(422)
    g = rng.normal(size=(7, 5, 3))
    e = rng.normal(size=(7, 5, 3))

    for angle in (0.0, 0.23, 0.88, 1.57, 2.23):
        c, s = np.cos(angle), np.sin(angle)

        rotation = np.array(
            [
                [c, -s, 0.0],
                [s, c, 0.0],
                [0.0, 0.0, 1.0],
            ]
        )

        er = e @ rotation.T

        phi = np.sum(g * er, axis=-1)
        current = np.cross(g, er)

        actual = (
            phi**2
            + np.sum(current**2, axis=-1)
        )

        expected = (
            np.sum(g**2, axis=-1)
            * np.sum(er**2, axis=-1)
        )

        np.testing.assert_allclose(
            actual,
            expected,
            rtol=1e-13,
            atol=1e-13,
        )


def test_zero_interface_demand_forces_zero_topological_overlap():
    g = np.array([0.0, 0.0, 3.0])
    e = np.array([0.0, 0.0, 2.0])
    b = np.array([4.0, 1.0, 0.0])

    assert np.dot(g, b) == 0.0
    assert np.all(np.cross(g, e) == 0.0)
    assert np.dot(e, b) == 0.0


def test_interface_cauchy_lower_bound_random():
    rng = np.random.default_rng(434)

    for _ in range(25):
        g, e, b = rng.normal(size=(3, 3))

        n = g / np.linalg.norm(g)

        e_n = np.dot(e, n)
        b_t2 = (
            np.dot(b, b)
            - np.dot(b, n)**2
        )

        q = np.hypot(
            np.dot(g, b),
            np.linalg.norm(np.cross(g, e)),
        )

        lhs = (
            np.linalg.norm(g)
            * abs(np.dot(e, b))
        )

        rhs = (
            np.sqrt(e_n**2 + b_t2)
            * q
        )

        assert lhs <= rhs + 1e-12


def test_static_cross_sector_not_poynting_flux():
    e_x = np.array([1.0, 0.0, 0.0])
    b_y = np.array([0.0, 1.0, 0.0])
    e_y = np.zeros(3)
    b_x = np.zeros(3)

    poynting = (
        np.cross(e_x, b_x)
        + np.cross(e_y, b_y)
    )

    mixed_vector = np.cross(e_x, b_y)

    np.testing.assert_allclose(
        poynting,
        np.zeros(3),
    )

    assert np.linalg.norm(mixed_vector) == 1.0


def test_3d_payload_normalization_and_box_support():
    h = 0.075
    coords = m.grid(h)

    density, theta = m.material(coords)

    assert abs(
        np.sum(density) * h**3 - 1.0
    ) < 0.004

    assert np.max(theta) > 1000.0

    for axis in range(3):
        assert not np.any(
            theta.take([0, -1], axis=axis)
        )

    assert np.min(coords[..., 2]) > 2.0


def test_multipole_dipole_exact_direction_and_axis_covariance():
    points = np.array(
        [[[[1.3, 0.7, 3.1], [0.4, -0.5, 3.6]]]]
    )

    coeffs = np.array([1.0])
    center = np.zeros(3)
    axis = np.array([0.0, 0.0, 1.0])

    actual = m.multipole_field(
        points, coeffs, center, axis
    )

    r = np.linalg.norm(points, axis=-1)

    expected = 2.0**2 * (
        3.0
        * points[..., 2, None]
        * points
        / r[..., None]**5
        - axis / r[..., None]**3
    )

    np.testing.assert_allclose(
        actual,
        expected,
        rtol=1e-12,
        atol=1e-12,
    )


def test_discrete_curl_conservation():
    rng = np.random.default_rng(415)
    v = rng.normal(size=(7, 9, 5, 3))

    residual = m.divergence(
        m.curl(v, 1.0),
        1.0,
    )

    assert np.max(np.abs(residual)) < 1e-12
