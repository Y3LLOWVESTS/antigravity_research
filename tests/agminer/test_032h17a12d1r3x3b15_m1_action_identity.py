"""Focused B15-M1 two-U(1) Lorentzian action identity tests."""

import importlib.util
from pathlib import Path

import numpy as np
import pytest


MODULE = (
    Path(__file__).resolve().parents[2]
    / "simulations"
    / "032h17a12d1r3x3b15_m1_action_identity.py"
)

spec = importlib.util.spec_from_file_location(
    "b15_m1",
    MODULE,
)

b15 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b15)


@pytest.mark.parametrize("n", [5, 7, 9])
def test_frozen_action_and_both_gauge_identities(n):
    result = b15.run(n=n)

    assert result[
        "exact_gauge_reciprocity_gate_pass"
    ]

    assert (
        result["max_relative_identity_residual"]
        < 1e-10
    )

    assert result[
        "nonconstant_theta_mixed_coupling_present"
    ]

    assert (
        result["numerical_residuals"][
            "independent_action_derivative_relative"
        ]
        < 1e-8
    )

    assert result["loaded_3d_solution"] is False
    assert result["loaded_1g"] is False
    assert result["source_support_1m_certified"] is False


def test_even_grid_is_excluded():
    with pytest.raises(ValueError):
        b15.periodic_derivative(6, 1.0)


def test_bad_theta_shape_is_rejected():
    grad, curl = b15.complex_3d(5, 1.0)

    with pytest.raises(ValueError):
        b15.hessians(
            grad,
            curl,
            np.ones(4),
            1.0,
        )
