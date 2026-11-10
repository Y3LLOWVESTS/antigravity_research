"""R3X3B6: analytical boundary tests and real R3B audit."""
import numpy as np
import pytest

from antigravity_research.agminer.hook17_fdual_f_loaded_payload_homotopy import (
    _build_elliptic_operators,
)
from antigravity_research.agminer.hook17_fdual_f_r3x3b6_boundary_support import (
    correct_baseline_source,
    independent_cylindrical_laplacian,
    norm_fraction,
    audit_grid,
)


@pytest.mark.parametrize("h", [0.125, 0.25])
def test_constant_potential(h):
    rhos = np.arange(0, 2.0 + h / 2, h)
    zs = np.arange(-2, 2 + h / 2, h)

    k = _build_elliptic_operators(
        rhos, zs, h
    )["k_phi"]

    phi = np.ones((len(zs), len(rhos)))

    raw, corrected = correct_baseline_source(
        k, phi, rhos, h
    )

    assert np.linalg.norm(raw) > 0
    assert np.max(np.abs(corrected)) < 1e-10

    independent = independent_cylindrical_laplacian(
        phi, rhos, h
    )

    assert np.max(np.abs(independent)) < 1e-10


@pytest.mark.parametrize("h", [0.125, 0.25])
def test_quadratic_potential(h):
    rhos = np.arange(0, 2.0 + h / 2, h)
    zs = np.arange(-2, 2 + h / 2, h)

    phi = zs[:, None]**2 + rhos[None, :]**2

    k = _build_elliptic_operators(
        rhos, zs, h
    )["k_phi"]

    _, corrected = correct_baseline_source(
        k, phi, rhos, h
    )

    independent = independent_cylindrical_laplacian(
        phi, rhos, h
    )

    assert np.max(np.abs(corrected + 6.0)) < 1e-10
    assert np.max(np.abs(independent + 6.0)) < 1e-10


def test_invalid_potential():
    with pytest.raises(ValueError):
        independent_cylindrical_laplacian(
            np.array([1.0, 2.0]),
            np.array([0.0, 1.0]),
            1.0,
        )


def test_norm_is_not_signed_charge():
    values = np.array([[1., 2.], [3., 4.]])
    mask = np.array([
        [True, False],
        [False, False],
    ])

    assert norm_fraction(values, mask) == pytest.approx(
        1.0 / np.sqrt(30.0)
    )


def test_original_r3b_boundary_correction():
    result = audit_grid(0.075)

    assert result["old_baseline_outside_l2_fraction"] > 0.5

    assert (
        result["boundary_corrected_outside_l2_fraction"]
        < 0.001
    )

    assert result["independent_stencil_relative_error"] < 1e-11

    assert result[
        "required_electric_interface_rhs_outside_fraction"
    ] == pytest.approx(1.0)

    assert result[
        "required_magnetic_interface_rhs_outside_fraction"
    ] == pytest.approx(1.0)

    assert not result["microscopic_source_certified"]
    assert not result["continuum_certified"]
