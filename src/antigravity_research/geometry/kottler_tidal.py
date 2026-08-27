"""Tidal/geodesic-deviation quantities for Kottler spacetime.

For radial free fall in an orthonormal frame:

    radial eigenvalue:
        2GM/r^3 + Lambda*c^2/3

    transverse eigenvalues:
        -GM/r^3 + Lambda*c^2/3

Positive eigenvalue:
    neighboring freely falling particles accelerate apart.

Negative eigenvalue:
    neighboring freely falling particles accelerate together.

Units: s^-2
"""

from antigravity_research.geometry.kottler import C, G


def radial_tidal_eigenvalue_s2(
    radius_m: float,
    mass_kg: float,
    cosmological_constant_m2: float,
) -> float:
    if radius_m <= 0.0:
        raise ValueError("radius_m must be positive")

    return (
        2.0 * G * mass_kg / radius_m**3
        + cosmological_constant_m2 * C**2 / 3.0
    )


def transverse_tidal_eigenvalue_s2(
    radius_m: float,
    mass_kg: float,
    cosmological_constant_m2: float,
) -> float:
    if radius_m <= 0.0:
        raise ValueError("radius_m must be positive")

    return (
        -G * mass_kg / radius_m**3
        + cosmological_constant_m2 * C**2 / 3.0
    )


def tidal_trace_s2(
    radius_m: float,
    mass_kg: float,
    cosmological_constant_m2: float,
) -> float:
    radial = radial_tidal_eigenvalue_s2(
        radius_m,
        mass_kg,
        cosmological_constant_m2,
    )

    transverse = transverse_tidal_eigenvalue_s2(
        radius_m,
        mass_kg,
        cosmological_constant_m2,
    )

    return radial + 2.0 * transverse
