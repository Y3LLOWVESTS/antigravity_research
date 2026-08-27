"""Schwarzschild-de Sitter (Kottler) baseline calculations.

This module intentionally begins with the weak-field radial acceleration.

The quantity calculated here is a Newtonian-like radial coordinate
acceleration. It is NOT, by itself, an invariant proof of local antigravity.

Later research stages will analyze geodesic deviation and other operationally
meaningful observables.
"""

from __future__ import annotations


G = 6.67430e-11
C = 299_792_458.0

SOLAR_MASS_KG = 1.98847e30
PARSEC_M = 3.085677581491367e16
MEGAPARSEC_M = 1.0e6 * PARSEC_M


def weak_field_attractive_acceleration(
    radius_m: float,
    mass_kg: float,
) -> float:
    """Newtonian central gravitational acceleration in m/s^2."""

    if radius_m <= 0.0:
        raise ValueError("radius_m must be positive")

    if mass_kg < 0.0:
        raise ValueError("mass_kg must not be negative")

    return -(G * mass_kg) / radius_m**2


def cosmological_acceleration(
    radius_m: float,
    cosmological_constant_m2: float,
) -> float:
    """Outward Lambda term in the weak-field Kottler acceleration."""

    if radius_m <= 0.0:
        raise ValueError("radius_m must be positive")

    return (
        cosmological_constant_m2
        * C**2
        * radius_m
        / 3.0
    )


def weak_field_radial_acceleration(
    radius_m: float,
    mass_kg: float,
    cosmological_constant_m2: float,
) -> float:
    """Return total weak-field radial acceleration in m/s^2.

    a(r) = -GM/r^2 + Lambda*c^2*r/3

    Negative = inward.
    Positive = outward.
    """

    return (
        weak_field_attractive_acceleration(radius_m, mass_kg)
        + cosmological_acceleration(
            radius_m,
            cosmological_constant_m2,
        )
    )


def static_radius(
    mass_kg: float,
    cosmological_constant_m2: float,
) -> float:
    """Radius where the two weak-field acceleration terms balance.

    r_static = (3GM / (Lambda*c^2))^(1/3)
    """

    if mass_kg <= 0.0:
        raise ValueError("mass_kg must be positive")

    if cosmological_constant_m2 <= 0.0:
        raise ValueError(
            "cosmological_constant_m2 must be positive"
        )

    return (
        3.0
        * G
        * mass_kg
        / (
            cosmological_constant_m2
            * C**2
        )
    ) ** (1.0 / 3.0)


def cosmological_constant_from_flat_lcdm(
    hubble_constant_s: float,
    omega_lambda: float,
) -> float:
    """Derive Lambda from H0 and Omega_Lambda.

    Lambda = 3 * Omega_Lambda * H0^2 / c^2
    """

    if hubble_constant_s <= 0.0:
        raise ValueError("hubble_constant_s must be positive")

    if not 0.0 <= omega_lambda <= 1.0:
        raise ValueError("omega_lambda must be between 0 and 1")

    return (
        3.0
        * omega_lambda
        * hubble_constant_s**2
        / C**2
    )
