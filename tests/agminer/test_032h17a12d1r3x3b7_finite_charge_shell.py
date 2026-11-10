"""Focused R3X3B7 analytical and numerical tests."""
import math

import numpy as np
import pytest

from antigravity_research.agminer.hook17_fdual_f_r3x3b7_finite_charge_shell import (
    radial_profile,
    source_density_proxy,
    shell_energy_penalty,
    evaluate_r3b_grid,
)


@pytest.mark.parametrize("ell", [1, 2, 3, 8])
def test_continuous_potential_and_derivative(ell):
    radius = 2.0
    width = 0.1

    for edge in (radius - width, radius):
        f, fp, _ = radial_profile(
            ell, 1.0, radius, width,
            np.array([edge - 1e-9, edge + 1e-9]),
        )

        assert abs(f[1] - f[0]) < 2e-7
        assert abs(fp[1] - fp[0]) < 2e-6


@pytest.mark.parametrize("ell", [1, 2, 3])
def test_exact_exterior(ell):
    radius = 2.0
    amplitude = 1.4
    r = np.array([2.01, 2.4, 3.6])

    f, fp, _ = radial_profile(
        ell, amplitude, radius, 0.1, r
    )

    expected = (
        -amplitude / math.sqrt(2)
        * (radius / r)**(ell + 1)
    )

    assert np.allclose(f, expected, rtol=1e-14)
    assert np.allclose(
        fp, -(ell + 1) * expected / r,
        rtol=1e-14,
    )


def test_charge_is_inside_shell():
    r = np.array([
        1.0, 1.5, 1.89,
        1.91, 1.95, 1.99,
        2.01, 2.3, 3.0,
    ])

    source = source_density_proxy(
        1, 1.5, 2.0, 0.1, r
    )

    assert max(abs(source[:3])) < 1e-10
    assert max(abs(source[6:])) < 1e-10
    assert max(abs(source[3:6])) > 1e-2


@pytest.mark.parametrize("width", [0.025, 0.05, 0.1, 0.2, 0.4])
def test_positive_energy_penalty(width):
    row = shell_energy_penalty(
        [1.0, 0.25, 0.05],
        2.0,
        width,
    )

    assert (
        row[
            "extra_electric_field_energy_j_before_1g_normalization"
        ] > 0
    )

    assert row["dirichlet_identity_relative_error"] < 1e-8
    assert row["charge_supported_inside_source"]
    assert not row["microscopic_source_realized"]


def test_no_electric_monopole():
    with pytest.raises(ValueError):
        radial_profile(
            0, 1.0, 2.0, 0.1,
            np.array([3.0]),
        )


def test_invalid_shell_width():
    with pytest.raises(ValueError):
        shell_energy_penalty([1.0], 2.0, 0.0)


def test_original_r3b_fine_reference():
    row = evaluate_r3b_grid(0.05, (0.1,))

    assert math.isclose(
        row["original_preloaded_field_energy_j"],
        1.5429162116460216,
        abs_tol=1e-8,
    )

    assert math.isclose(
        row["shells"][0]["mixed_field_energy_j_normalized"],
        1.5473042949759865,
        abs_tol=1e-7,
    )

    assert not row["fully_loaded_payload_certified"]
