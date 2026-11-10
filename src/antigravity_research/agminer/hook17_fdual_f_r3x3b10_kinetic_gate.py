"""R3X3B10 — exact positive kinetic-stiffness interface gate.

Scientific question
-------------------
Can a positive, common Maxwell kinetic rescaling Z inside a
spherical topological medium restore unsuppressed E/B transmission
at the large coupling found in the R3B reference?

Assumptions
-----------
- Static spherical interface with uniform interior theta and Z
- Exterior canonical Maxwell theory, Z=1, theta=0
- No free interface charge or current
- Every spherical harmonic ell>=1
- Common positive interior electric/magnetic kinetic coefficient

This is NOT a proof about the smooth toroidal R3B payload.
Matter dynamics, microscopic sources, the universal physical metric,
and complete operating energy are not certified.
"""
from __future__ import annotations

import math

import numpy as np


def matching_matrix(ell: int, theta: float, z: float):
    if type(ell) is not int or ell < 1:
        raise ValueError("ell must be an integer >= 1")

    if (
        not math.isfinite(theta)
        or not math.isfinite(z)
        or z < 0
    ):
        raise ValueError("theta finite and Z nonnegative required")

    return np.array([
        [ell + 1 + ell*z, ell*theta],
        [-(ell + 1)*theta, ell + (ell + 1)*z],
    ], dtype=float)


def transmission(ell: int, theta: float, z: float):
    a = matching_matrix(ell, theta, z)

    return (2*ell + 1) * np.linalg.inv(a)


def universal_bound(theta: float):
    if not math.isfinite(theta):
        raise ValueError("theta must be finite")

    if theta == 0:
        return None

    q = abs(theta)

    return 4.5 * (
        1.0/q**2 + math.sqrt(2.0)/q
    )


def boundary_residual(
    ell, theta, z, incident, interior, radius=1.0
):
    """Independent four-condition spherical boundary check."""
    if not math.isfinite(radius) or radius <= 0:
        raise ValueError("Invalid radius")

    e0, b0 = np.asarray(incident, dtype=float)
    e1, b1 = np.asarray(interior, dtype=float)

    power = radius ** (2*ell + 1)

    electric_scattered = (e1 - e0)*power

    magnetic_scattered = (
        -ell/(ell + 1)*(b1 - b0)*power
    )

    return {
        "tangential_E":
            e0 + electric_scattered/power - e1,

        "normal_B":
            -ell*b0
            + (ell + 1)*magnetic_scattered/power
            + ell*b1,

        "normal_D":
            -ell*e0
            + (ell + 1)*electric_scattered/power
            + ell*(z*e1 + theta*b1),

        "tangential_H":
            b0 + magnetic_scattered/power
            - (z*b1 - theta*e1),
    }


def symbolic_certificate():
    import sympy as sp

    ell, theta, z = sp.symbols(
        "ell theta Z", real=True, positive=True
    )

    a = ell + 1 + ell*z
    b = ell + (ell + 1)*z

    matrix = sp.Matrix([
        [a, ell*theta],
        [-(ell + 1)*theta, b],
    ])

    determinant = sp.factor(matrix.det())

    assert sp.simplify(
        determinant
        - a*b
        - ell*(ell + 1)*theta**2
    ) == 0

    # Positive remainder after removing the terms needed
    # for the uniform denominator bound.
    remainder = sp.simplify(
        determinant
        - ell*(ell + 1)*(z**2 + theta**2)
    )

    expected = (
        ell*(ell + 1)
        + (ell**2 + (ell + 1)**2)*z
    )

    assert sp.simplify(remainder - expected) == 0

    return {
        "determinant": str(determinant),
        "positive_remainder": str(remainder),
        "uniform_bound_proved": True,
        "proof":
            "norm2(adjA)<=sum_abs(adjA)"
            "=(2ell+1)*(1+Z+abs(theta));"
            " detA>=ell*(ell+1)*(Z**2+theta**2);"
            " (2ell+1)**2/(ell*(ell+1))<=9/2;"
            " Z+abs(theta)<=sqrt(2)*sqrt(Z**2+theta**2)",
        "physical_dynamic_stability_certified": False,
    }


def evaluate(theta_reference: float):
    bound = universal_bound(theta_reference)

    rows = []

    for ell in (1, 2, 10, 50):
        for z in (
            1e-6, 1.0, 100.0,
            10000.0, theta_reference, 1e6
        ):
            t = transmission(ell, theta_reference, z)

            norm = float(np.linalg.norm(t, 2))

            incident = np.ones(2)
            interior = t @ incident

            residuals = boundary_residual(
                ell, theta_reference, z,
                incident, interior
            )

            scale = max(
                1.0, abs(theta_reference), z
            )

            error = (
                max(abs(v) for v in residuals.values())
                / scale
            )

            assert norm <= bound*(1.0 + 1e-12)
            assert error < 1e-10

            rows.append({
                "ell": ell,
                "interior_Z": z,
                "transmission_norm": norm,
                "boundary_relative_error": error,
            })

    return {
        "branch": "032H17A12D1R3X3B10",
        "scope":
            "POSITIVE_COMMON_KINETIC_STIFFNESS_SPHERICAL_INTERFACE",
        "theta_reference": theta_reference,
        "all_positive_Z_all_ell_bound": bound,
        "symbolic": symbolic_certificate(),
        "modes": rows,
        "conclusion":
            "COMMON_POSITIVE_KINETIC_STIFFNESS_DOES_NOT_RESTORE_ORDER_ONE_TRANSMISSION_AT_LARGE_THETA",
        "anisotropic_kinetic_operators_excluded": False,
        "dynamical_compensators_excluded": False,
        "toroidal_payload_force_excluded": False,
        "full_same_action_certified": False,
        "complete_energy_certified": False,
        "physical_antigravity_model_found": False,
        "r3b_1p542916j_preloaded_preserved": True,
        "006d_replaced": False,
    }
