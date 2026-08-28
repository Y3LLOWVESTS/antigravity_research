"""Effective domain-wall plus current-carrying boundary model.

PURPOSE
-------
Test the cheapest field-theory-motivated stabilization mechanism for a finite
relativistic domain wall before constructing a full nonlinear field simulation.

SCIENTIFIC QUESTION
-------------------
Can a current/charge-supported string loop stabilize a finite circular
domain-wall source while preserving its locally repulsive gravitational near
field, and can it improve the energy coefficient obtained in Simulation 006D?

PHYSICAL MOTIVATION
-------------------
A canonical relativistic domain wall has positive surface energy density
sigma and equal tangential tension:

    p_r = p_phi = -sigma
    p_z = 0.

This is the same qualitative stress pattern as the repulsive inner region of
the project's optimized finite source.

An ordinary wall disk bounded by an ordinary positive-tension string collapses.
A current-carrying string loop can instead acquire an energy contribution that
increases as its radius decreases.  The simplest conserved-current effective
model is

    E(R)
    =
    pi sigma R^2
    +
    2 pi mu R
    +
    J / R

where:

    sigma:
        wall surface energy density, J/m^2;

    mu:
        nonnegative bare string energy per length, J/m;

    J:
        positive conserved current/charge parameter, J m.

This is an effective thin-defect model, not an exact Witten-model vorton.

MECHANICAL EQUILIBRIUM
----------------------
The radial derivative is

    dE/dR
    =
    2 pi sigma R
    +
    2 pi mu
    -
    J/R^2.

A stationary radius therefore requires

    J
    =
    2 pi R^2 (sigma R + mu).

At this radius,

    d^2E/dR^2
    =
    2 pi sigma
    +
    2J/R^3
    >
    0,

so the single radial degree of freedom is locally stable.

This does NOT establish full field-theory stability or stability against
nonaxisymmetric modes.

BOUNDARY STRESS
---------------
The boundary energy per length is

    U_b
    =
    mu + J/(2 pi R^2).

At fixed conserved J, its effective tensile stress is

    T_b
    =
    dE_b/dL
    =
    mu - J/(2 pi R^2).

At equilibrium,

    T_b = -sigma R.

The negative tensile stress is therefore a positive hoop compression, exactly
the mechanical role required by the finite wall.

The active gravitational line source is

    A_b
    =
    U_b - T_b
    =
    2 (sigma R + mu).

ENERGY CONDITIONS
-----------------
At equilibrium,

    U_b = sigma R + 2 mu
    |T_b| = sigma R.

For mu >= 0,

    |T_b| <= U_b.

Thus the effective one-dimensional boundary satisfies the corresponding DEC.
The mu = 0 limit saturates it.

LINEARIZED GRAVITATIONAL FIELD
------------------------------
Let

    x = R/h

and

    m = mu/(sigma R).

The wall's outward axial field factor is

    F_wall
    =
    1 - 1/sqrt(1+x^2).

The equilibrium boundary contributes attraction

    F_boundary
    =
    -2(1+m)x^2/(1+x^2)^(3/2).

Hence

    H(x,m)
    =
    F_wall + F_boundary.

The physical outward acceleration is

    a
    =
    2 pi G sigma H / c^2.

At equilibrium the total positive energy is

    E
    =
    pi sigma R^2 (3 + 4m).

Therefore

    M
    =
    C a h^2/G

with

    C(x,m)
    =
    x^2(3+4m)/(2H).

KEY ANALYTICAL OBSERVATION
--------------------------
For m = 0 this model is exactly the q=1 domain-wall disk plus minimum-energy
DEC-compatible compressive rim studied in Simulation 005B.

Positive m increases the source energy and the boundary's attractive active
stress simultaneously.  It therefore cannot improve the m=0 optimum.

APPROXIMATION LEVEL
-------------------
- effective thin-defect theory;
- static radial energy model;
- static linearized general relativity;
- axisymmetry;
- target on symmetry axis;
- no nonlinear gravitational backreaction.

LIMITATIONS
-----------
This model does not establish:

- an explicit microscopic superconducting-string solution attached to a wall;
- nonlinear field equations for the combined defect;
- nonaxisymmetric stability;
- quantum stability;
- finite thickness;
- a realization of the more efficient 006D distributed support collar;
- experimental accessibility;
- a practical antigravity device.

CLAIM CLASSIFICATION
--------------------
ANALYTICAL_EFFECTIVE_FIELD_THEORY_GATE
"""

from __future__ import annotations

import math

from scipy.optimize import minimize_scalar


def _positive(name: str, value: float) -> None:
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _nonnegative(name: str, value: float) -> None:
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def equilibrium_current_parameter_j_m(
    sigma_j_m2: float,
    mu_j_m: float,
    radius_m: float,
) -> float:
    """Return J required for radial equilibrium, in J m."""

    _positive("sigma_j_m2", sigma_j_m2)
    _nonnegative("mu_j_m", mu_j_m)
    _positive("radius_m", radius_m)

    return (
        2.0
        * math.pi
        * radius_m**2
        * (
            sigma_j_m2 * radius_m
            + mu_j_m
        )
    )


def total_energy_derivative_j_m(
    sigma_j_m2: float,
    mu_j_m: float,
    current_parameter_j_m: float,
    radius_m: float,
) -> float:
    """Return dE/dR for the effective wall-loop energy."""

    _positive("sigma_j_m2", sigma_j_m2)
    _nonnegative("mu_j_m", mu_j_m)
    _positive("current_parameter_j_m", current_parameter_j_m)
    _positive("radius_m", radius_m)

    return (
        2.0 * math.pi * sigma_j_m2 * radius_m
        + 2.0 * math.pi * mu_j_m
        - current_parameter_j_m / radius_m**2
    )


def total_energy_second_derivative_j_m2(
    sigma_j_m2: float,
    current_parameter_j_m: float,
    radius_m: float,
) -> float:
    """Return d^2E/dR^2 for radial stability."""

    _positive("sigma_j_m2", sigma_j_m2)
    _positive("current_parameter_j_m", current_parameter_j_m)
    _positive("radius_m", radius_m)

    return (
        2.0 * math.pi * sigma_j_m2
        + 2.0 * current_parameter_j_m / radius_m**3
    )


def equilibrium_boundary_state_j_m(
    sigma_j_m2: float,
    mu_j_m: float,
    radius_m: float,
) -> tuple[float, float, float]:
    """Return equilibrium boundary energy, tension, and active line source.

    Returns
    -------
    tuple
        ``(U_b, T_b, A_b)`` in J/m.

        ``T_b`` is positive for tension and negative for compression.

        ``A_b = U_b - T_b`` is the static active gravitational line source.
    """

    j = equilibrium_current_parameter_j_m(
        sigma_j_m2,
        mu_j_m,
        radius_m,
    )

    current_energy_per_length = (
        j
        / (
            2.0
            * math.pi
            * radius_m**2
        )
    )

    energy_per_length = (
        mu_j_m
        + current_energy_per_length
    )

    tension = (
        mu_j_m
        - current_energy_per_length
    )

    active_line = (
        energy_per_length
        - tension
    )

    return (
        energy_per_length,
        tension,
        active_line,
    )


def field_factor(
    radius_over_h: float,
    bare_string_ratio: float = 0.0,
) -> float:
    """Return the equilibrium wall-plus-boundary axial field factor.

    Positive values correspond to an outward gravitational field.
    """

    x = radius_over_h
    m = bare_string_ratio

    _positive("radius_over_h", x)
    _nonnegative("bare_string_ratio", m)

    root = math.sqrt(1.0 + x * x)

    wall = 1.0 - 1.0 / root

    boundary = (
        -2.0
        * (1.0 + m)
        * x * x
        / (1.0 + x * x) ** 1.5
    )

    return wall + boundary


def mass_coefficient(
    radius_over_h: float,
    bare_string_ratio: float = 0.0,
) -> float:
    """Return C in M = C a h^2/G for the equilibrium architecture."""

    x = radius_over_h
    m = bare_string_ratio

    factor = field_factor(x, m)

    if factor <= 0.0:
        return math.inf

    return (
        x * x
        * (3.0 + 4.0 * m)
        / (
            2.0 * factor
        )
    )


def optimize_mass_coefficient(
    bare_string_ratio: float = 0.0,
) -> tuple[float, float]:
    """Return the optimal R/h and C for a fixed nonnegative m."""

    _nonnegative(
        "bare_string_ratio",
        bare_string_ratio,
    )

    result = minimize_scalar(
        lambda x: mass_coefficient(
            x,
            bare_string_ratio,
        ),
        bounds=(1.0, 30.0),
        method="bounded",
        options={
            "xatol": 1.0e-13,
        },
    )

    if not result.success:
        raise RuntimeError(result.message)

    return float(result.x), float(result.fun)
