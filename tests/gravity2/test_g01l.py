"""Focused tests for G01-L exact Maxwell and metric gates."""
from fractions import Fraction
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from antigravity_research.gravity2 import g01l_core as source
import g01l_check_v1 as verifier


def test_maxwell_kernel_exact_fraction():
    for ell in range(1, 31):
        v = source.full_mode(ell, 2.0)

        assert math.isclose(
            v["X_full"], 2 / (2 * ell + 1)
        )

        assert math.isclose(
            v["Y_full"],
            2 / ell + 2 / (ell + 1),
        )

        assert v["Y_interior"] > 0


def test_interior_normal_continuity_required():
    for ell in range(1, 13):
        v = source.full_mode(ell, 2.0)

        assert v["Y_full"] > v["Y_exterior"]

        assert math.isclose(
            v["Y_full"] - v["Y_exterior"],
            v["Y_interior"],
        )


def test_radial_grid_convergence():
    for ell in (1, 2, 4, 8, 12):
        errors = [
            source.radial_midpoint_error(ell, n)
            for n in (128, 256, 512, 1024)
        ]

        assert all(
            x > y
            for x, y in zip(errors, errors[1:])
        )

        assert errors[-1] < 2e-4


def test_closed_form_induced_q_preserved():
    R = Fraction(2)

    for ell in range(1, 13):
        A = R / Fraction(2 * ell + 1)
        q_over_b = -2 * R / (R + A)

        assert q_over_b == -Fraction(
            2 * ell + 1, ell + 1
        )


def test_metric_stress_offdiagonal():
    witness = source.metric_witness()

    T = np.array(witness["kinetic_T_ab"])
    h = np.array(witness["h"])
    f = np.array(witness["f"])
    y = np.array(witness["Y"])

    assert np.max(np.abs(T - T.T)) < 1e-12

    assert witness["omit_H_changes_T"]
    assert witness["omit_mixed_Hodge_changes_T"]

    inv = np.linalg.inv(h)
    eps = 2e-6

    for a, b in (
        (0, 0),
        (0, 1),
        (1, 2),
        (2, 2),
    ):
        perturb = np.zeros((3, 3))
        perturb[a, b] = 1.0
        perturb[b, a] = 1.0

        up = verifier.action_density_from_inverse(
            inv + eps * perturb,
            f, y, 2.0, 4.0, 8.2,
        )

        dn = verifier.action_density_from_inverse(
            inv - eps * perturb,
            f, y, 2.0, 4.0, 8.2,
        )

        predicted = (
            -0.5
            * math.sqrt(-np.linalg.det(h))
            * T[a, b]
            * (1 if a == b else 2)
        )

        assert abs(
            (up - dn) / (2 * eps) - predicted
        ) < 2e-7
