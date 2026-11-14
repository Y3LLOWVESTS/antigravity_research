"""Independent synthetic regressions for B17-M5L.

These tests establish algebraic correctness of the signed
quadratic construction. They do not certify R3B physics.
"""

import numpy as np
import pytest

from scipy.sparse import csr_matrix, diags

from antigravity_research.agminer.hook17_r3b_m5l_variational_audit import (
    assemble_variational_matrix,
    on_shell_quadratic,
)


def example():
    """Construct an exactly weighted-self-adjoint toy system."""
    ops = {
        "k_phi": csr_matrix(
            np.diag([2.0, 3.0])
        ),
        "k_a": csr_matrix([[7.0]]),
        "nz_inner": 1,
    }

    c = csr_matrix([
        [0.2],
        [0.4],
    ])

    d = csr_matrix([
        [0.2 / 3.0, 0.4]
    ])

    rhos = np.array([
        0.0, 3.0, 5.0
    ])

    return ops, c, d, rhos


def test_signed_weight_makes_action_symmetric():
    ops, c, d, rhos = example()

    A, H, weights, defect = (
        assemble_variational_matrix(
            ops,
            {"c": c, "d": d},
            rhos,
            8.0,
        )
    )

    assert defect < 1e-14

    assert np.array_equal(
        weights,
        [1.0, 3.0, -3.0],
    )

    incorrectly_signed = (
        diags(np.abs(weights)) @ A
    )

    asymmetry = (
        incorrectly_signed
        - incorrectly_signed.T
    )

    assert np.max(
        np.abs(asymmetry.data)
    ) > 1e-2


def test_wrong_cross_coupling_is_detected():
    ops, c, d, rhos = example()

    _, _, _, defect = (
        assemble_variational_matrix(
            ops,
            {
                "c": c,
                "d": 1.5 * d,
            },
            rhos,
            8.0,
        )
    )

    assert defect > 1e-3


def test_on_shell_variation_and_scaling():
    ops, c, d, rhos = example()

    A, H, weights, _ = (
        assemble_variational_matrix(
            ops,
            {"c": c, "d": d},
            rhos,
            8.0,
        )
    )

    j = np.array([1.0, 2.0, 3.0])

    u = np.linalg.solve(
        A.toarray(), j
    )

    first = on_shell_quadratic(
        u, j, H, weights
    )

    doubled = on_shell_quadratic(
        2 * u,
        2 * j,
        H,
        weights,
    )

    assert first[
        "relative_action_variation_residual"
    ] < 1e-14

    assert first[
        "relative_on_shell_identity_defect"
    ] < 1e-14

    assert doubled[
        "native_quadratic_functional"
    ] == pytest.approx(
        4 * first[
            "native_quadratic_functional"
        ]
    )

    displaced = on_shell_quadratic(
        u + np.array([1.0, 0.0, 0.0]),
        j,
        H,
        weights,
    )

    assert displaced[
        "relative_action_variation_residual"
    ] > 0.1


def test_invalid_source_pairing_is_rejected():
    ops, c, d, rhos = example()

    _, H, weights, _ = (
        assemble_variational_matrix(
            ops,
            {"c": c, "d": d},
            rhos,
            8.0,
        )
    )

    with pytest.raises(ValueError):
        on_shell_quadratic(
            np.array([1.0]),
            np.array([2.0, 3.0]),
            H,
            weights,
        )
