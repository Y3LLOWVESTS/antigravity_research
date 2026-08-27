"""Simulation 006C — independent finite-disk gravitational-field verification.

PURPOSE
-------
Independently verify the gravitational field used in Simulation 005B without
reusing its analytic field formula as the computational implementation.

SCIENTIFIC QUESTION
-------------------
Does direct numerical integration of the linearized-GR Green-function response
to the complete idealized membrane-plus-support-rim stress-energy reproduce
the 005B axial field, repulsive-zone zero, optimized geometry, and mass
coefficient?

WHY THIS TEST MATTERS
---------------------
Simulation 005B established a finite positive-energy source with a locally
repulsive near field, but its production implementation and many regression
tests share the same analytic field expression.

This simulation provides an independent numerical path.  It constructs the
active source from the membrane and rim stress-energy and numerically
integrates the axial gravitational kernel.

The production 005B analytic function is imported only after the independent
integral has been evaluated and is used solely as a comparison reference.

PHYSICAL MODEL
--------------
Linearized general relativity in the static weak-field limit.

The source is:

    1. a circular membrane of radius R and surface energy density U;
    2. isotropic tangential membrane tension tau = q U;
    3. a minimum-energy DEC-compatible compressive support rim.

Positive pressure denotes compression and negative pressure denotes tension.

For the membrane,

    p_r = p_phi = -q U.

Its active surface source is therefore

    U + p_r + p_phi
    =
    U (1 - 2 q).

The support rim carries line energy

    lambda = q U R

and equal-magnitude positive hoop compression at the DEC minimum.  Its active
line source is consequently

    lambda + p_phi,line
    =
    2 q U R.

For a source element at radius r and an axial target at height z, the
linearized axial Green-function kernel is proportional to

    z / (r^2 + z^2)^(3/2).

The sign convention used here is positive acceleration away from the upper
face of the membrane.

DIMENSIONLESS NORMALIZATION
---------------------------
Let

    y = z / R.

The physical acceleration is written

    a_z = 2 pi G U / c^2 * F(q, y).

This simulation computes F(q,y) by adaptive quadrature directly over the
stress-energy source.

INDEPENDENCE
------------
The numerical implementation below does not call:

    dimensionless_axis_factor()
    axial_acceleration_m_s2()
    mass_coefficient_for_target()

to obtain its primary results.

The production function ``dimensionless_axis_factor`` is imported only for
post-computation comparison.

ENERGY CONDITIONS
-----------------
For the principal branch,

    1/2 < q <= 1.

The membrane and minimum-energy support rim satisfy the component DEC in the
idealized 005B model.

ASSUMPTIONS
-----------
- linearized general relativity;
- static source;
- axisymmetry;
- ideal infinitesimally thin membrane;
- ideal line support rim;
- no dynamical-stability analysis;
- no finite-thickness material model;
- no constitutive material law.

NUMERICAL METHOD
----------------
Adaptive SciPy quadrature is used independently for:

    membrane radial integration;
    membrane azimuthal integration;
    support-rim azimuthal integration.

Root finding uses the independently integrated field.

Geometry optimization uses the independently integrated field at every
objective evaluation.

VALIDATION TARGETS
------------------
For q=1, independently reproduce approximately

    z_zero / R = 0.393319893190

and

    R / h = 4.00614967

with

    C_005B = 79.753148...

The direct numerical field should also agree with the production analytic
formula over a grid of q and z/R values.

CLAIM LIMITS
------------
Success verifies the 005B linearized gravitational-field implementation.

It does not establish:

- finite-thickness realizability;
- nonlinear-GR validity outside the weak-field regime;
- dynamical stability;
- a known material implementation;
- a practical antigravity device.

CLAIM CLASSIFICATION
--------------------
INDEPENDENT_NUMERICAL_VERIFICATION if all verification gates pass.

NOVEL PHYSICS CLAIM
-------------------
NO.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar


REFERENCE_ZERO = 0.393319893190329
REFERENCE_R_OVER_H = 4.006149670781
REFERENCE_C = 79.753148116012


def membrane_factor_numeric(
    q: float,
    y: float,
) -> float:
    """Numerically integrate the membrane contribution to F(q,y).

    The direct radial Green-function integrand becomes increasingly localized
    near r=0 when y=z/R is very small.  Direct adaptive quadrature in r can
    therefore become ill-conditioned even though the physical integral is
    finite.

    Use the coordinate transformation

        r = y tan(theta)

    so that

        y r dr / (r^2+y^2)^(3/2) = sin(theta) dtheta

    with

        0 <= theta <= atan(1/y).

    The transformed integral is still evaluated numerically.  No analytic
    antiderivative or 005B production field formula is used.
    """

    active_ratio = 1.0 - 2.0 * q

    theta_max = math.atan2(
        1.0,
        y,
    )

    def transformed_radial_integrand(
        theta: float,
    ) -> float:
        return math.sin(theta)

    radial, radial_error = quad(
        transformed_radial_integrand,
        0.0,
        theta_max,
        epsabs=1.0e-13,
        epsrel=1.0e-13,
        limit=200,
    )

    def angular_integrand(
        theta_phi: float,
    ) -> float:
        del theta_phi
        return radial

    angular, angular_error = quad(
        angular_integrand,
        0.0,
        2.0 * math.pi,
        epsabs=1.0e-13,
        epsrel=1.0e-13,
        limit=100,
    )

    del radial_error, angular_error

    # F is normalized by 2*pi*G*U/c^2.
    #
    # Positive acceleration points away from the membrane.  For q>1/2,
    # active_ratio is negative and the membrane contribution is repulsive.
    return (
        -active_ratio
        * angular
        / (2.0 * math.pi)
    )

def rim_factor_numeric(
    q: float,
    y: float,
) -> float:
    """Numerically integrate the complete active support-rim contribution."""

    # In units U=R=1, minimum DEC line energy is lambda=q.
    # Active line source is energy + hoop compression = 2*q.
    active_line_ratio = 2.0 * q

    def angular_integrand(theta: float) -> float:
        del theta

        return (
            active_line_ratio
            * y
            / (1.0 + y * y) ** 1.5
        )

    angular, angular_error = quad(
        angular_integrand,
        0.0,
        2.0 * math.pi,
        epsabs=1.0e-13,
        epsrel=1.0e-13,
        limit=100,
    )

    del angular_error

    # Positive active rim energy attracts toward the source, so its
    # contribution is negative in the outward-positive convention.
    return (
        -angular
        / (2.0 * math.pi)
    )


def field_factor_numeric(
    q: float,
    y: float,
) -> float:
    """Return the independently integrated total dimensionless field."""

    if not (
        math.isfinite(q)
        and 0.0 < q <= 1.0
    ):
        raise ValueError(
            "q must satisfy 0 < q <= 1"
        )

    if not (
        math.isfinite(y)
        and y > 0.0
    ):
        raise ValueError(
            "y=z/R must be positive"
        )

    return (
        membrane_factor_numeric(q, y)
        +
        rim_factor_numeric(q, y)
    )


def mass_coefficient_numeric(
    q: float,
    y: float,
) -> float:
    """Return C using only the independently integrated field."""

    factor = field_factor_numeric(
        q,
        y,
    )

    if factor <= 0.0:
        return math.inf

    # Total positive energy-equivalent mass:
    #
    # membrane = pi U R^2 / c^2
    # rim      = 2 pi q U R^2 / c^2
    #
    # M = pi U R^2 (1+2q)/c^2.
    #
    # Since h=yR and
    #
    # a = 2*pi*G*U/c^2 * F,
    #
    # C = M G / (a h^2).
    return (
        (1.0 + 2.0 * q)
        /
        (
            2.0
            * y
            * y
            * factor
        )
    )


def independent_repulsive_zero(
    q: float,
) -> float:
    """Find z/R where the independently integrated field changes sign.

    The bracketing interval is discovered numerically rather than supplied
    from the known 005B result.
    """

    scan = np.geomspace(
        1.0e-5,
        10.0,
        300,
    )

    previous_y = float(scan[0])
    previous_f = field_factor_numeric(
        q,
        previous_y,
    )

    for candidate in scan[1:]:
        candidate_y = float(candidate)
        candidate_f = field_factor_numeric(
            q,
            candidate_y,
        )

        if previous_f == 0.0:
            return previous_y

        if candidate_f == 0.0:
            return candidate_y

        if (
            previous_f > 0.0
            and candidate_f < 0.0
        ) or (
            previous_f < 0.0
            and candidate_f > 0.0
        ):
            return float(
                brentq(
                    lambda y:
                        field_factor_numeric(
                            q,
                            y,
                        ),
                    previous_y,
                    candidate_y,
                    xtol=1.0e-13,
                    rtol=1.0e-13,
                )
            )

        previous_y = candidate_y
        previous_f = candidate_f

    raise RuntimeError(
        "Independent field scan found no repulsive-to-attractive sign change."
    )

def independent_optimum(
    q: float,
) -> tuple[float, float, float]:
    """Optimize y=h/R and return y, R/h, C independently."""

    zero = independent_repulsive_zero(
        q
    )

    result = minimize_scalar(
        lambda y:
            mass_coefficient_numeric(
                q,
                y,
            ),
        bounds=(
            1.0e-4,
            zero * (1.0 - 1.0e-8),
        ),
        method="bounded",
        options={
            "xatol": 1.0e-12,
        },
    )

    if not result.success:
        raise RuntimeError(
            result.message
        )

    y = float(result.x)
    coefficient = float(result.fun)

    return (
        y,
        1.0 / y,
        coefficient,
    )


print(
    "=== SIMULATION 006C RESULTS ==="
)

print(
    "IMPLEMENTATION="
    "DIRECT_NUMERICAL_GREEN_FUNCTION_INTEGRATION"
)

print(
    "PRIMARY_FIELD_IMPLEMENTATION_REUSES_005B_ANALYTIC_FORMULA=NO"
)

print()


# ---------------------------------------------------------------------------
# Direct comparison grid.
#
# Compute the independent numerical value first.
# Only then import the production analytic expression for comparison.
# ---------------------------------------------------------------------------

comparison_points = []

for q in (
    0.51,
    0.60,
    0.75,
    0.90,
    1.00,
):
    for y in (
        0.05,
        0.10,
        0.20,
        0.30,
        0.50,
        1.00,
    ):
        independent = field_factor_numeric(
            q,
            y,
        )

        comparison_points.append(
            {
                "q": q,
                "z_over_r": y,
                "independent_factor": independent,
            }
        )


from antigravity_research.geometry.finite_tension_disk import (  # noqa: E402
    dimensionless_axis_factor,
)


max_abs_error = 0.0
max_rel_error = 0.0

for row in comparison_points:
    reference = dimensionless_axis_factor(
        float(row["q"]),
        float(row["z_over_r"]),
    )

    independent = float(
        row["independent_factor"]
    )

    absolute_error = abs(
        independent - reference
    )

    scale = max(
        abs(reference),
        abs(independent),
        1.0e-15,
    )

    relative_error = (
        absolute_error
        / scale
    )

    row[
        "production_factor"
    ] = reference

    row[
        "absolute_error"
    ] = absolute_error

    row[
        "relative_error"
    ] = relative_error

    max_abs_error = max(
        max_abs_error,
        absolute_error,
    )

    max_rel_error = max(
        max_rel_error,
        relative_error,
    )


print(
    "=== FIELD GRID CROSS-CHECK ==="
)

print(
    f"COMPARISON_POINT_COUNT={len(comparison_points)}"
)

print(
    f"MAX_ABSOLUTE_FIELD_ERROR={max_abs_error:.12e}"
)

print(
    f"MAX_RELATIVE_FIELD_ERROR={max_rel_error:.12e}"
)

field_grid_pass = (
    max_abs_error < 1.0e-10
)

print(
    "FIELD_GRID_MATCH="
    + (
        "PASS"
        if field_grid_pass
        else "FAIL"
    )
)

print()


# ---------------------------------------------------------------------------
# Independent q=1 repulsive-zero reconstruction.
# ---------------------------------------------------------------------------

zero = independent_repulsive_zero(
    1.0
)

zero_error = abs(
    zero
    -
    REFERENCE_ZERO
)

print(
    "=== INDEPENDENT REPULSIVE ZERO ==="
)

print(
    f"NUMERIC_Z_ZERO_OVER_R={zero:.15f}"
)

print(
    f"REFERENCE_Z_ZERO_OVER_R={REFERENCE_ZERO:.15f}"
)

print(
    f"ZERO_ABSOLUTE_ERROR={zero_error:.12e}"
)

zero_pass = (
    zero_error < 1.0e-9
)

print(
    "REPULSIVE_ZERO_MATCH="
    + (
        "PASS"
        if zero_pass
        else "FAIL"
    )
)

print()


# ---------------------------------------------------------------------------
# Independent geometry/mass optimization.
# ---------------------------------------------------------------------------

(
    optimal_y,
    optimal_r_over_h,
    optimal_c,
) = independent_optimum(
    1.0
)

r_error = abs(
    optimal_r_over_h
    -
    REFERENCE_R_OVER_H
)

c_error = abs(
    optimal_c
    -
    REFERENCE_C
)

print(
    "=== INDEPENDENT 005B OPTIMUM ==="
)

print(
    f"OPTIMAL_H_OVER_R={optimal_y:.15f}"
)

print(
    f"OPTIMAL_R_OVER_H={optimal_r_over_h:.15f}"
)

print(
    f"REFERENCE_R_OVER_H={REFERENCE_R_OVER_H:.15f}"
)

print(
    f"R_OVER_H_ABSOLUTE_ERROR={r_error:.12e}"
)

print(
    f"NUMERIC_005B_COEFFICIENT={optimal_c:.15f}"
)

print(
    f"REFERENCE_005B_COEFFICIENT={REFERENCE_C:.15f}"
)

print(
    f"COEFFICIENT_ABSOLUTE_ERROR={c_error:.12e}"
)

optimum_pass = (
    r_error < 1.0e-6
    and
    c_error < 1.0e-6
)

print(
    "005B_OPTIMUM_MATCH="
    + (
        "PASS"
        if optimum_pass
        else "FAIL"
    )
)

print()


# ---------------------------------------------------------------------------
# Save independent comparison data.
# ---------------------------------------------------------------------------

data_path = Path(
    "results/data/"
    "006c_independent_finite_disk_field.csv"
)

data_path.parent.mkdir(
    parents=True,
    exist_ok=True,
)

with data_path.open(
    "w",
    newline="",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(
            comparison_points[0].keys()
        ),
    )

    writer.writeheader()
    writer.writerows(
        comparison_points
    )


all_pass = (
    field_grid_pass
    and zero_pass
    and optimum_pass
)


print(
    "=== SIMULATION 006C SUMMARY ==="
)

print(
    "DIRECT_STRESS_ENERGY_GREEN_FUNCTION_INTEGRATION=YES"
)

print(
    "INDEPENDENT_OF_005B_FIELD_IMPLEMENTATION=YES"
)

print(
    "FIELD_GRID_VERIFIED="
    + (
        "YES"
        if field_grid_pass
        else "NO"
    )
)

print(
    "REPULSIVE_ZERO_VERIFIED="
    + (
        "YES"
        if zero_pass
        else "NO"
    )
)

print(
    "005B_OPTIMUM_VERIFIED="
    + (
        "YES"
        if optimum_pass
        else "NO"
    )
)

print(
    "SIMULATION_006C="
    + (
        "GREEN"
        if all_pass
        else "REVIEW"
    )
)

print(
    "CLAIM_CLASSIFICATION="
    + (
        "INDEPENDENT_NUMERICAL_VERIFICATION"
        if all_pass
        else "NUMERICAL_RESULT_REQUIRES_REVIEW"
    )
)

print(
    "FINITE_THICKNESS_REALIZATION=NOT_ESTABLISHED"
)

print(
    "DYNAMIC_STABILITY=NOT_ESTABLISHED"
)

print(
    "KNOWN_MATERIAL_REALIZATION=NO"
)

print(
    "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
)

print(
    f"DATA={data_path}"
)

print(
    "NEXT=006D_FINITE_THICKNESS_REALIZABILITY_GATE"
)
