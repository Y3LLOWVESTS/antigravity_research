"""B15-M0 mathematical source-orientation and support regression tests.

These tests do not certify a loaded 3D solution.
"""

import importlib.util
import sys
from pathlib import Path

import numpy as np

MODULE = (
    Path(__file__).resolve().parents[2]
    / "simulations"
    / "032h17a12d1r3x3b15_orientation_preflight.py"
)

spec = importlib.util.spec_from_file_location(
    "b15_m0_orientation",
    MODULE,
)

b15 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = b15
spec.loader.exec_module(b15)

AMPS = np.array([1.0, 0.3, -0.1])


def test_exact_covariance_under_so3():
    assert b15.covariance_check(AMPS)["pass"]


def test_torus_gap_is_exact_and_all_sources_exterior():
    assert abs(
        b15.exact_support_gap((0, 0, 0)) - 1.0
    ) < 1e-12

    points = b15.torus_points().reshape(-1, 3)

    for sources in b15.configurations().values():
        for source in sources:
            assert (
                b15.exact_support_gap(source.center)
                >= 1.0 - 1e-12
            )

            distance = np.linalg.norm(
                points - np.asarray(source.center),
                axis=-1,
            )

            assert np.min(distance) > 2.0


def test_joint_sign_flip_and_one_sector_pseudoscalar_sign():
    points = np.array([
        [0.7, 0.2, 3.3],
        [1.1, -0.4, 3.0],
    ])

    source = b15.make_source()

    dual = b15.Source(
        source.center,
        source.e_axis,
        source.b_axis,
        -1,
        -1,
    )

    electric = b15.Source(
        source.center,
        source.e_axis,
        source.b_axis,
        -1,
        1,
    )

    reference = b15.sigma(
        points,
        [source],
        AMPS,
    )

    np.testing.assert_allclose(
        b15.sigma(points, [dual], AMPS),
        reference,
        rtol=1e-13,
    )

    np.testing.assert_allclose(
        b15.sigma(points, [electric], AMPS),
        -reference,
        rtol=1e-13,
    )


def test_axisymmetry_and_tilt_nonaxisymmetry_are_distinct():
    points = b15.torus_points()

    original = b15.sigma(
        points,
        [b15.make_source()],
        AMPS,
    )

    tilted = b15.sigma(
        points,
        b15.configurations()["relative_tilt_60deg"],
        AMPS,
    )

    assert (
        np.max(np.std(original, axis=-1))
        < 1e-10 * np.max(np.abs(original))
    )

    assert (
        np.max(np.std(tilted, axis=-1))
        > 1e-4 * np.max(np.abs(tilted))
    )


def test_e_and_b_are_maxwell_harmonic_exterior_gradient():
    points = np.array([
        [0.6, 0.4, 3.9],
        [1.2, 0.5, 3.5],
    ])

    source = b15.make_source(
        axis=(0.4, 0.1, 0.8),
    )

    electric, magnetic = b15.fields(
        points,
        [source],
        AMPS,
    )

    np.testing.assert_allclose(
        electric,
        -magnetic,
        rtol=1e-13,
    )

    step = 1e-4
    jacobian = np.zeros((2, 3, 3))

    for direction in range(3):
        shift = np.eye(3)[direction] * step

        jacobian[:, :, direction] = (
            b15.exterior_b(
                points + shift,
                source.center,
                source.b_axis,
                AMPS,
            )
            - b15.exterior_b(
                points - shift,
                source.center,
                source.b_axis,
                AMPS,
            )
        ) / (2 * step)

    divergence = np.trace(
        jacobian,
        axis1=1,
        axis2=2,
    )

    curl_matrix = (
        jacobian
        - np.swapaxes(jacobian, 1, 2)
    )

    assert np.max(np.abs(divergence)) < 1e-5
    assert np.max(np.abs(curl_matrix)) < 1e-5


def test_synthetic_gate_never_claims_loaded_success():
    summary = b15.analyze(
        AMPS,
        {"kind": "synthetic_test"},
    )

    assert summary[
        "proper_rotation_covariance"
    ]["pass"]

    assert not summary["loaded_1g_established"]
    assert not summary["certified_sub10mj_device"]

    assert summary["entries"][
        "relative_tilt_60deg"
    ]["nonaxisymmetric_source_relative_to_torus"]

    assert not summary["entries"][
        "aligned_original"
    ]["nonaxisymmetric_source_relative_to_torus"]
