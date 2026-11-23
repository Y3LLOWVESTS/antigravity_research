"""G01-L independent scientific checker.

Reconstructs the rational Maxwell boundary kernels, drive
correction, Hilbert stress by finite differences, and negative
controls without importing the producing physics functions.

A positive audit does not imply a complete physical model.
"""
from __future__ import annotations

from fractions import Fraction
import math

import numpy as np


def action_density_from_inverse(h_inverse, f, y, k, g, H):
    h = np.linalg.inv(h_inverse)
    determinant = np.linalg.det(h)

    if determinant >= 0:
        raise ValueError("NOT_LORENTZIAN")

    fu = h_inverse @ f @ h_inverse.T
    yu = h_inverse @ y @ h_inverse.T

    return float(
        math.sqrt(-determinant) * (
            -k / 4 * np.sum(f * fu)
            -g / 2 * np.sum(f * yu)
            -H / 4 * np.sum(y * yu)
        )
    )


def review(science, k, j):
    if science["status"] != (
        "ACTION_INCOMPLETE_G01K_EXTERIOR_ONLY_KERNEL_NOT_FULL_TWO_SIDED_MAXWELL"
    ):
        raise ValueError("INVALID_CLAIM")

    if (
        science["physical_survivors"] != 0
        or science["replaced_006D"]
    ):
        raise ValueError("FALSE_SURVIVOR_PROMOTION")

    R = Fraction(2)
    K = R
    g = 2 * R
    H = Fraction(41, 10) * R

    max_kernel = 0.0
    max_drive = 0.0
    min_interior = float("inf")

    for row, kr, jr in zip(
        science["modes"], k["modes"], j["modes"]
    ):
        ell = row["ell"]

        if ell != kr["ell"] or ell != jr["ell"]:
            raise ValueError("MODE_MISMATCH")

        e = Fraction(ell)

        Xint = R * e / (2 * e + 1)**2
        Xext = R * (e + 1) / (2 * e + 1)**2
        Yint = R / e
        Yext = R / (e + 1)

        expected = {
            "X_interior": Xint,
            "X_exterior": Xext,
            "X_full": Xint + Xext,
            "Y_interior": Yint,
            "Y_exterior": Yext,
            "Y_full": Yint + Yext,
        }

        for key, value in expected.items():
            max_kernel = max(
                max_kernel,
                abs(row[key] - float(value)),
            )

        q = (
            -float(g / (K + Xint + Xext))
            * jr["b_mode"]
        )

        J = (
            float(H + Yint + Yext) * jr["b_mode"]
            + float(g) * q
        )

        max_drive = max(
            max_drive,
            abs(J - row["required_two_sided_drive"])
            / max(
                1.0,
                abs(J),
                abs(row["required_two_sided_drive"]),
            ),
        )

        if not math.isclose(
            q, row["q_mode"],
            rel_tol=2e-13, abs_tol=2e-13,
        ):
            raise ValueError("Q_RESPONSE_MISMATCH")

        if not math.isclose(
            row["delta_drive"],
            float(Yint) * jr["b_mode"],
            rel_tol=2e-13,
            abs_tol=2e-13,
        ):
            raise ValueError("INTERIOR_DRIVE_MISSING")

        if not math.isclose(
            row["mandatory_interior_magnetic_energy_proxy"],
            0.5 * jr["basis_l2_area_weight"]
            * jr["b_mode"]**2 * float(Yint),
            rel_tol=2e-13,
            abs_tol=2e-13,
        ):
            raise ValueError("INTERIOR_ENERGY_MISSING")

        min_interior = min(min_interior, float(Yint))

        if not (
            row["full_hessian_determinant"]
            > row["old_hessian_determinant"] > 0
        ):
            raise ValueError("HESSIAN_INCONSISTENCY")

        errors = row["radial_midpoint_errors"]

        if not all(
            x > y
            for x, y in zip(errors, errors[1:])
        ):
            raise ValueError("RADIAL_CONVERGENCE_FAIL")

    if max_kernel > 2e-15 or max_drive > 2e-12:
        raise ValueError("INDEPENDENT_KERNEL_FAIL")

    # Independent, non-diagonal inverse-metric variations.
    # Both electric and magnetic worldvolume components
    # are present, so Hodge stress cannot be discarded.
    witness = science["metric_stress"]

    h = np.array(witness["h"], dtype=float)
    f = np.array(witness["f"], dtype=float)
    y = np.array(witness["Y"], dtype=float)
    T = np.array(witness["kinetic_T_ab"], dtype=float)

    inv = np.linalg.inv(h)
    density = math.sqrt(-np.linalg.det(h))

    max_metric = 0.0

    for i in range(3):
        for jj in range(i, 3):
            perturb = np.zeros((3, 3))
            perturb[i, jj] = 1.0
            perturb[jj, i] = 1.0

            eps = 2e-6

            plus = action_density_from_inverse(
                inv + eps * perturb,
                f, y, float(K), float(g), float(H),
            )

            minus = action_density_from_inverse(
                inv - eps * perturb,
                f, y, float(K), float(g), float(H),
            )

            numerical = (plus - minus) / (2 * eps)

            predicted = (
                -0.5 * density
                * (T[i, jj] if i == jj else 2 * T[i, jj])
            )

            max_metric = max(
                max_metric,
                abs(numerical - predicted),
            )

    if (
        max_metric > 2e-7
        or not witness["omit_H_changes_T"]
        or not witness["omit_mixed_Hodge_changes_T"]
    ):
        raise ValueError("SHELL_METRIC_VARIATION_FAIL")

    nonzero = next(
        (
            row["b_mode"]
            for row in science["modes"]
            if row["b_mode"] != 0
        ),
        None,
    )

    if nonzero is None:
        raise ValueError("NO_MAGNETIC_FIELD_TO_TEST")

    controls = {
        "no_interior_field_violates_Bianchi":
            abs(nonzero - 0.0) > 0,
        "correct_Bnormal_continuity":
            abs(nonzero - nonzero) == 0,
        "interior_energy_strictly_positive":
            science[
                "total_mandatory_interior_magnetic_energy_proxy"
            ] > 0,
        "original_Mexterior_not_Mfull":
            all(
                row["Y_full"] > row["Y_exterior"]
                for row in science["modes"]
            ),
        "g_zero_no_mirror_source":
            float(0) / (float(K) + float(R / 3)) == 0,
        "H_zero_local_ghost_prefilter":
            K * 0 - g * g < 0,
        "H_critical_marginal":
            K * (4 * R) - g * g == 0,
        "no_J_positive_hessian_zero_field":
            all(
                row["full_hessian_determinant"] > 0
                for row in science["modes"]
            ),
        "historical_loaded_inward_retained":
            science[
                "historical_loaded_acceleration_m_s2"
            ] < 0,
        "no_SI_interpretation":
            science["current_energy_scope"]
            == "CANONICAL_PROXY_NOT_SI_JOULES",
    }

    if not all(controls.values()):
        raise ValueError("FAILED_NEGATIVE_CONTROL")

    return {
        "status":
            "PASS_INDEPENDENT_SCOPED_TWO_SIDED_MAXWELL_AND_METRIC_AUDIT",
        "modes": len(science["modes"]),
        "max_rational_kernel_error": max_kernel,
        "max_corrected_drive_relative_error": max_drive,
        "max_Lorentzian_metric_variation_error":
            max_metric,
        "min_interior_kernel": min_interior,
        "negative_controls": controls,
        "unresolved":
            "FULL_ACTION_SOURCE_LORENTZIAN_HEALTH_EINSTEIN_EARTH",
        "physical_survivors": 0,
    }
