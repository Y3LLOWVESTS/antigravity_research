"""Finite positive vacuum-energy core diagnostics.

We investigate an idealized spherical region with

    p = -epsilon

and compare a de Sitter interior to a Schwarzschild exterior.

This module does NOT assume that a smooth boundary exists.

In fact, one purpose of the calculation is to test that assumption.

Definitions
-----------

epsilon:
    energy density [J/m^3]

p:
    pressure [Pa = J/m^3]

For p = -epsilon, the isotropic geodesic-deviation rate is

    k = 8*pi*G*epsilon / (3*c^2)

so

    epsilon = 3*c^2*k / (8*pi*G)

The equivalent cosmological constant is

    Lambda_eff = 8*pi*G*epsilon / c^4
               = 3*k / c^2

and the static de Sitter metric function is

    f_in(r) = 1 - Lambda_eff*r^2/3
            = 1 - k*r^2/c^2.

If we assign the ordinary volume energy inside radius R the mass

    M = (4*pi/3) R^3 epsilon / c^2,

then the corresponding Schwarzschild exterior has

    f_out(r) = 1 - 2GM/(c^2 r).

At r = R, f_in and f_out agree.

Their radial derivatives do not.

This is a boundary-layer diagnostic, not yet a complete Israel-junction
calculation.
"""

from __future__ import annotations

import math

from antigravity_research.geometry.kottler import C, G


def vacuum_energy_density_for_rate(
    rate_s2: float,
) -> float:
    """Required w=-1 energy density [J/m^3] for isotropic rate k."""

    if rate_s2 < 0.0:
        raise ValueError("rate_s2 must not be negative")

    return (
        3.0
        * C**2
        * rate_s2
        / (
            8.0
            * math.pi
            * G
        )
    )


def effective_lambda_m2(
    energy_density_j_m3: float,
) -> float:
    """Equivalent Lambda for positive vacuum energy."""

    return (
        8.0
        * math.pi
        * G
        * energy_density_j_m3
        / C**4
    )


def enclosed_energy_mass_kg(
    radius_m: float,
    energy_density_j_m3: float,
) -> float:
    """Energy-equivalent mass inside a uniform spherical core."""

    if radius_m <= 0.0:
        raise ValueError("radius_m must be positive")

    volume = (
        4.0
        * math.pi
        * radius_m**3
        / 3.0
    )

    return (
        energy_density_j_m3
        * volume
        / C**2
    )


def de_sitter_metric_f(
    radius_m: float,
    energy_density_j_m3: float,
) -> float:
    """Static-patch de Sitter metric function."""

    lam = effective_lambda_m2(
        energy_density_j_m3
    )

    return (
        1.0
        - lam
        * radius_m**2
        / 3.0
    )


def schwarzschild_metric_f(
    radius_m: float,
    mass_kg: float,
) -> float:
    """Schwarzschild metric function."""

    if radius_m <= 0.0:
        raise ValueError("radius_m must be positive")

    return (
        1.0
        - 2.0
        * G
        * mass_kg
        / (
            C**2
            * radius_m
        )
    )


def de_sitter_metric_derivative_per_m(
    radius_m: float,
    energy_density_j_m3: float,
) -> float:
    """df_in/dr at radius r."""

    lam = effective_lambda_m2(
        energy_density_j_m3
    )

    return (
        -2.0
        * lam
        * radius_m
        / 3.0
    )


def schwarzschild_metric_derivative_per_m(
    radius_m: float,
    mass_kg: float,
) -> float:
    """df_out/dr at radius r."""

    return (
        2.0
        * G
        * mass_kg
        / (
            C**2
            * radius_m**2
        )
    )


def compactness(
    radius_m: float,
    mass_kg: float,
) -> float:
    """Dimensionless 2GM/(c^2 R)."""

    return (
        2.0
        * G
        * mass_kg
        / (
            C**2
            * radius_m
        )
    )


def de_sitter_horizon_radius_m(
    rate_s2: float,
) -> float:
    """Static-patch horizon radius for k > 0.

    Since f = 1 - k r^2/c^2,

        r_h = c / sqrt(k)
    """

    if rate_s2 <= 0.0:
        return math.inf

    return (
        C
        / math.sqrt(rate_s2)
    )


def tov_pressure_gradient_pa_per_m(
    radius_m: float,
    enclosed_mass_kg: float,
    energy_density_j_m3: float,
    pressure_pa: float,
) -> float:
    """SI TOV pressure gradient.

    dp/dr =
      -G * (epsilon + p)/c^2
      * (m + 4*pi*r^3*p/c^2)
      / [r^2 * (1 - 2Gm/(r c^2))]
    """

    if radius_m <= 0.0:
        raise ValueError("radius_m must be positive")

    f = (
        1.0
        - 2.0
        * G
        * enclosed_mass_kg
        / (
            radius_m
            * C**2
        )
    )

    if f <= 0.0:
        raise ValueError(
            "TOV evaluation point is at or inside a horizon"
        )

    inertial_density = (
        energy_density_j_m3
        + pressure_pa
    ) / C**2

    gravitational_mass_term = (
        enclosed_mass_kg
        + 4.0
        * math.pi
        * radius_m**3
        * pressure_pa
        / C**2
    )

    return (
        -G
        * inertial_density
        * gravitational_mass_term
        / (
            radius_m**2
            * f
        )
    )


def weak_field_exterior_acceleration_m_s2(
    radius_m: float,
    mass_kg: float,
) -> float:
    """Weak-field Schwarzschild radial acceleration diagnostic."""

    if radius_m <= 0.0:
        raise ValueError("radius_m must be positive")

    return (
        -G
        * mass_kg
        / radius_m**2
    )
