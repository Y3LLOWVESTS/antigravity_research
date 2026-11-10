"""R3X3B10 — independent matching, bounds and claim checks."""
import numpy as np
import pytest

from antigravity_research.agminer.hook17_fdual_f_r3x3b10_kinetic_gate import (
    matching_matrix,
    transmission,
    universal_bound,
    boundary_residual,
    symbolic_certificate,
    evaluate,
)


@pytest.mark.parametrize("ell", [1, 2, 10, 50])
@pytest.mark.parametrize("z", [0.001, 1.0, 1e4])
def test_independent_boundary_conditions(ell, z):
    incident = np.array([0.7, -0.2])

    for theta in (0.0, 1.0, -100.0, 18987.283771593688):
        t = transmission(ell, theta, z)
        interior = t @ incident

        algebra = (
            matching_matrix(ell, theta, z) @ interior
            - (2*ell + 1)*incident
        )

        assert np.linalg.norm(algebra) < 1e-8

        residuals = boundary_residual(
            ell, theta, z, incident, interior
        )

        assert max(
            abs(x) for x in residuals.values()
        ) < 1e-8


@pytest.mark.parametrize("ell", [1, 2, 10, 50, 500])
def test_all_positive_stiffness_bound(ell):
    for z in (0.001, 1.0, 100.0, 1e4, 1e7):
        for theta in (10.0, 100.0, 1e4):
            norm = np.linalg.norm(
                transmission(ell, theta, z), 2
            )

            assert norm <= (
                universal_bound(theta) * (1 + 1e-12)
            )


def test_matches_r3x3b8_at_z_one():
    ell = 1
    theta = 100.0

    determinant = (
        (2*ell+1)**2
        + ell*(ell+1)*theta**2
    )

    original = (
        (2*ell+1)/determinant
        * np.array([
            [2*ell+1, -ell*theta],
            [(ell+1)*theta, 2*ell+1],
        ])
    )

    assert np.allclose(
        transmission(ell, theta, 1.0),
        original,
    )


def test_invalid_parameters_rejected():
    for ell, z in ((0, 1), (-1, 1), (1, -1)):
        with pytest.raises(ValueError):
            transmission(ell, 1.0, z)

    assert universal_bound(0.0) is None

    with pytest.raises(ValueError):
        universal_bound(float("nan"))


def test_exact_symbolic_proof():
    assert symbolic_certificate()[
        "uniform_bound_proved"
    ]


def test_result_claims_remain_scoped():
    result = evaluate(18987.283771593688)

    assert (
        result["all_positive_Z_all_ell_bound"]
        < 0.00034
    )

    assert not result[
        "toroidal_payload_force_excluded"
    ]

    assert not result[
        "physical_antigravity_model_found"
    ]
