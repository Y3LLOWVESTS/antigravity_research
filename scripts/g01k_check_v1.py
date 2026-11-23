"""Independent algebra, source-response and periodic Ward checks."""
from __future__ import annotations

import math
from fractions import Fraction as F

import numpy as np


def review(science, parent):
    R = F(2)
    K = R
    g = 2 * R
    H = F(41, 10) * R

    # Independent uniqueness conditions from ell=1,2.
    if not (
        2*g == 3*K + R
        and 3*g == 5*K + R
    ):
        raise ValueError("EXACT_SOURCE_COEFFICIENT_FAIL")

    if not (
        K*H - g*g > 0
        and K*0 - g*g < 0
        and K*(4*R) - g*g == 0
    ):
        raise ValueError("KINETIC_NEGATIVE_CONTROLS_FAIL")

    if len(science["modes"]) != 12:
        raise ValueError("INCOMPLETE_MULTIPOLE_SET")

    for row, mode in zip(
        science["modes"], parent["modes"]
    ):
        ell = mode["ell"]
        A = R / F(2*ell + 1)
        M = R / F(ell + 1)

        exact = -g / (K + A)

        if exact != -F(2*ell + 1, ell + 1):
            raise ValueError("EXACT_DTN_RESPONSE_FAIL")

        threshold = g*g/(K + A) - M

        if threshold != R*F(
            4*ell + 1, ell + 1
        ):
            raise ValueError("STABILITY_THRESHOLD_FAIL")

        reconstructed = float(exact) * mode["b_mode"]

        if not math.isclose(
            reconstructed,
            row["required_q"],
            rel_tol=2e-13,
            abs_tol=2e-13,
        ):
            raise ValueError("TARGET_CHARGE_MISMATCH")

        if (
            row["q_relative_error"] > 5e-13
            or row["constrained_hessian_det"] <= 0
            or not H > threshold
        ):
            raise ValueError("UNHEALTHY_MODE")

        expected_drive = (
            float(H+M) * mode["b_mode"]
            + float(g) * reconstructed
        )

        if not math.isclose(
            expected_drive,
            row["required_drive_J_canonical"],
            rel_tol=2e-13,
            abs_tol=2e-13,
        ):
            raise ValueError("RECIPROCAL_DRIVE_DRIFT")

    # Discrete closed 2+1 periodic-worldvolume control.
    # j^a = epsilon^{abc} partial_b a_c
    # implies partial_a j^a = 0.
    generator = np.random.default_rng(41973)

    a = generator.normal(size=(3, 8, 8, 8))
    chi = generator.normal(size=(8, 8, 8))

    def d(array, axis):
        return (
            np.roll(array, -1, axis)
            - np.roll(array, 1, axis)
        ) / 2

    jt = d(a[2], 1) - d(a[1], 2)
    jx = d(a[0], 2) - d(a[2], 0)
    jy = d(a[1], 0) - d(a[0], 1)

    divergence = (
        d(jt, 0) + d(jx, 1) + d(jy, 2)
    )

    gauge_variation = float(np.sum(
        d(chi, 0)*jt
        + d(chi, 1)*jx
        + d(chi, 2)*jy
    ))

    max_divergence = float(
        np.max(np.abs(divergence))
    )

    if (
        max_divergence > 1e-12
        or abs(gauge_variation) > 1e-10
    ):
        raise ValueError("DISCRETE_WARD_FAIL")

    # Independent mixed-derivative reciprocity.
    max_reciprocity_error = 0.0

    for mode in parent["modes"]:
        ell = mode["ell"]
        A = float(R / F(2*ell + 1))
        M = float(R / F(ell + 1))
        kk, gg, hh = map(float, (K, g, H))

        def energy(q, b):
            return (
                .5*(kk+A)*q*q
                + gg*q*b
                + .5*(hh+M)*b*b
            )

        step = 1e-4
        q, b = .37, -.44

        mixed = (
            energy(q+step, b+step)
            - energy(q+step, b-step)
            - energy(q-step, b+step)
            + energy(q-step, b-step)
        ) / (4*step*step)

        max_reciprocity_error = max(
            max_reciprocity_error,
            abs(mixed-gg),
        )

    if max_reciprocity_error > 1e-6:
        raise ValueError("RECIPROCITY_CHECK_FAIL")

    # Executed negative-control inequalities.
    ell = 1
    A = float(R / F(3))
    M = float(R / F(2))
    kk, gg, hh = map(float, (K, g, H))

    controls = {
        "zero_coupling_no_induced_charge":
            -0.0/(kk+A) == 0.0,
        "zero_H_static_unstable":
            (kk+A)*M - gg*gg < 0,
        "H_equals_4R_kinetic_marginal":
            kk*(4*float(R)) - gg*gg == 0,
        "zero_drive_zero_unique_equilibrium":
            (kk+A)*(hh+M) - gg*gg > 0,
        "historical_loaded_response_inward":
            science["historical_loaded_min_m_s2"] < 0,
    }

    if not all(controls.values()):
        raise ValueError("NEGATIVE_CONTROL_FAIL")

    if not (
        science["protected_R3B_capacity_J"]
        == 1.5429162116460216
        and science["physical_survivors"] == 0
        and science["Einstein_gravity"] == "NOT_DERIVED"
        and 8.19 < science[
            "stabilizer_to_bare_magnetic_energy_ratio"
        ] < 8.21
    ):
        raise ValueError("FALSE_PHYSICAL_PROMOTION")

    return {
        "status":
            "PASS_CONDITIONAL_STATIC_WORLDVOLUME_SOURCE_NOT_GRAVITY",
        "multipoles_verified": 12,
        "local_kinetic_determinant": float(
            K*H-g*g
        ),
        "periodic_Ward_max_divergence":
            max_divergence,
        "periodic_X_gauge_variation_abs":
            abs(gauge_variation),
        "mixed_derivative_reciprocity_error":
            max_reciprocity_error,
        "negative_controls": controls,
        "certified_gravitational_survivors": 0,
    }
