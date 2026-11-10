"""R3X3B8 exact spherical-interface tests."""
import importlib.util
from pathlib import Path

import numpy as np
import pytest


PATH = (
    Path(__file__).resolve().parents[2]
    / "simulations"
    / "032h17a12d1r3x3b8_spherical_interface_screening.py"
)

SPEC = importlib.util.spec_from_file_location(
    "r3x3b8", PATH
)

MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def test_zero_theta_identity():
    for ell in (1, 3, 20):
        assert np.allclose(
            MOD.exact_transfer_matrix(ell, 0),
            np.eye(2),
        )


@pytest.mark.parametrize("ell", [1, 2, 7, 50])
@pytest.mark.parametrize(
    "theta", [0.0, 1.0, -3.0, 100.0, 1e4]
)
def test_exact_boundary_continuity(ell, theta):
    incident = np.array([1.25, -0.7])

    interior = (
        MOD.exact_transfer_matrix(ell, theta)
        @ incident
    )

    residuals = MOD.boundary_residual(
        ell, theta, incident, interior
    )

    assert max(
        abs(value) for value in residuals.values()
    ) < 2e-10


@pytest.mark.parametrize("ell", [1, 2, 10, 50, 1000])
def test_uniform_high_theta_bound(ell):
    for theta in (-1e4, -100.0, 100.0, 1e4):
        norm = np.linalg.norm(
            MOD.exact_transfer_matrix(ell, theta), 2
        )

        bound = MOD.universal_high_theta_bound(theta)

        assert norm <= bound * (1 + 1e-12)


def test_parallel_incident_sign_reversal():
    for ell in (1, 2, 8):
        row = MOD.screening_row(ell, 1e4)

        assert row["interior_EB_to_incident_EB"] < 0

        assert abs(
            row["interior_EB_to_incident_EB"]
        ) < 1e-6


def test_symbolic_matrix_identity():
    result = MOD.symbolic_certificate()

    assert result[
        "det_positive_for_real_theta_ell_gt0"
    ]


def test_conservative_claims():
    row = MOD.screening_row(1, 1e4)

    assert row["torus_no_go_proved"] is False
    assert MOD.universal_high_theta_bound(3.0) is None

    with pytest.raises(ValueError):
        MOD.exact_transfer_matrix(0, 1)
