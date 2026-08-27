"""Static spherical Israel shell between de Sitter and Schwarzschild.

Interior:
    f_-(r) = 1 - k*r^2/c^2

Exterior:
    f_+(r) = 1 - 2GM_ext/(c^2*r)

For a static shell at radius R, with the standard outward normal orientation:

    sigma_geom
      = (sqrt(f_-) - sqrt(f_+)) / (4*pi*R)

    P_geom
      = -sigma_geom/2
        + 1/(16*pi) *
          (f_+' / sqrt(f_+) - f_-' / sqrt(f_-))

sigma_geom and P_geom have dimensions 1/m in geometrized units.

SI conversion:

    surface energy density [J/m^2]
        = (c^4/G) * sigma_geom

    surface pressure [N/m = J/m^2]
        = (c^4/G) * P_geom

Positive P means tangential surface pressure.
Negative P means tangential surface tension.

The implementation uses compactness variables to avoid catastrophic
cancellation for the extremely weak-curvature terrestrial cases.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from antigravity_research.geometry.kottler import C, G


@dataclass(frozen=True)
class ShellEnergyConditions:
    nec: bool
    wec: bool
    dec: bool


def interior_compactness(
    rate_s2: float,
    radius_m: float,
) -> float:
    """x = k R^2 / c^2."""

    if rate_s2 < 0.0:
        raise ValueError("rate_s2 must not be negative")

    if radius_m <= 0.0:
        raise ValueError("radius_m must be positive")

    return (
        rate_s2
        * radius_m**2
        / C**2
    )


def exterior_compactness(
    exterior_mass_kg: float,
    radius_m: float,
) -> float:
    """y = 2 G M_ext / (c^2 R)."""

    if radius_m <= 0.0:
        raise ValueError("radius_m must be positive")

    return (
        2.0
        * G
        * exterior_mass_kg
        / (
            C**2
            * radius_m
        )
    )


def interior_volume_mass_kg(
    rate_s2: float,
    radius_m: float,
) -> float:
    """Positive vacuum-energy mass inside the core."""

    # epsilon = 3 c^2 k / (8 pi G)
    # Mv = 4 pi R^3 epsilon / (3 c^2)
    #    = k R^3 / (2G)

    return (
        rate_s2
        * radius_m**3
        / (
            2.0
            * G
        )
    )


def _sqrt_static_factor(
    compactness_value: float,
) -> float:
    if compactness_value >= 1.0:
        raise ValueError(
            "Shell is not in the static region: f <= 0"
        )

    return math.sqrt(
        1.0 - compactness_value
    )


def surface_energy_geom_per_m(
    rate_s2: float,
    radius_m: float,
    exterior_mass_kg: float,
) -> float:
    """Israel surface energy density in geometrized units [1/m].

    Uses the algebraically equivalent stable difference

        sqrt(1-x) - sqrt(1-y)
        = (y-x) / (sqrt(1-x) + sqrt(1-y)).
    """

    x = interior_compactness(
        rate_s2,
        radius_m,
    )

    y = exterior_compactness(
        exterior_mass_kg,
        radius_m,
    )

    sqrt_minus = _sqrt_static_factor(x)
    sqrt_plus = _sqrt_static_factor(y)

    stable_difference = (
        y - x
    ) / (
        sqrt_minus
        + sqrt_plus
    )

    return (
        stable_difference
        / (
            4.0
            * math.pi
            * radius_m
        )
    )


def surface_pressure_geom_per_m(
    rate_s2: float,
    radius_m: float,
    exterior_mass_kg: float,
) -> float:
    """Tangential shell pressure in geometrized units [1/m]."""

    x = interior_compactness(
        rate_s2,
        radius_m,
    )

    y = exterior_compactness(
        exterior_mass_kg,
        radius_m,
    )

    sqrt_minus = _sqrt_static_factor(x)
    sqrt_plus = _sqrt_static_factor(y)

    sigma = surface_energy_geom_per_m(
        rate_s2,
        radius_m,
        exterior_mass_kg,
    )

    derivative_jump_term = (
        y / sqrt_plus
        + 2.0 * x / sqrt_minus
    ) / radius_m

    return (
        -0.5 * sigma
        + derivative_jump_term
        / (
            16.0
            * math.pi
        )
    )


def surface_energy_j_m2(
    rate_s2: float,
    radius_m: float,
    exterior_mass_kg: float,
) -> float:
    """Shell surface energy density [J/m^2]."""

    return (
        C**4
        / G
        * surface_energy_geom_per_m(
            rate_s2,
            radius_m,
            exterior_mass_kg,
        )
    )


def surface_mass_density_kg_m2(
    rate_s2: float,
    radius_m: float,
    exterior_mass_kg: float,
) -> float:
    """Shell energy-equivalent mass density [kg/m^2]."""

    return (
        surface_energy_j_m2(
            rate_s2,
            radius_m,
            exterior_mass_kg,
        )
        / C**2
    )


def surface_pressure_n_m(
    rate_s2: float,
    radius_m: float,
    exterior_mass_kg: float,
) -> float:
    """Tangential shell pressure [N/m]."""

    return (
        C**4
        / G
        * surface_pressure_geom_per_m(
            rate_s2,
            radius_m,
            exterior_mass_kg,
        )
    )


def shell_energy_mass_kg(
    rate_s2: float,
    radius_m: float,
    exterior_mass_kg: float,
) -> float:
    """Surface rest-energy equivalent mass 4*pi*R^2*sigma/c^2."""

    return (
        4.0
        * math.pi
        * radius_m**2
        * surface_mass_density_kg_m2(
            rate_s2,
            radius_m,
            exterior_mass_kg,
        )
    )


def evaluate_shell_energy_conditions(
    surface_energy_density_j_m2: float,
    surface_pressure_n_m: float,
) -> ShellEnergyConditions:
    """Energy conditions for isotropic 2+1-dimensional shell matter.

    NEC:
        U + P >= 0

    WEC:
        U >= 0
        U + P >= 0

    DEC:
        U >= 0
        U >= |P|
    """

    scale = max(
        abs(surface_energy_density_j_m2),
        abs(surface_pressure_n_m),
        1.0,
    )

    tolerance = (
        scale
        * 1.0e-12
    )

    nec = (
        surface_energy_density_j_m2
        + surface_pressure_n_m
        >= -tolerance
    )

    wec = (
        surface_energy_density_j_m2
        >= -tolerance
        and nec
    )

    dec = (
        surface_energy_density_j_m2
        >= -tolerance
        and (
            surface_energy_density_j_m2
            - abs(surface_pressure_n_m)
        )
        >= -tolerance
    )

    return ShellEnergyConditions(
        nec=nec,
        wec=wec,
        dec=dec,
    )


def exterior_weak_field_acceleration_m_s2(
    radius_m: float,
    exterior_mass_kg: float,
) -> float:
    """Weak-field radial acceleration in Schwarzschild exterior."""

    if radius_m <= 0.0:
        raise ValueError("radius_m must be positive")

    return (
        -G
        * exterior_mass_kg
        / radius_m**2
    )


def gravastar_mass_relation_residual_kg(
    rate_s2: float,
    radius_m: float,
    exterior_mass_kg: float,
) -> float:
    """Check the exact thin-shell gravastar mass relation.

    In geometrized units:

        M =
            Mv
            + Ms * sqrt(1 - 2Mv/R)
            + Ms^2/(2R)

    where M, Mv, Ms are geometrized lengths.

    Returns reconstructed M_ext - specified M_ext in kg.
    """

    volume_mass_kg = interior_volume_mass_kg(
        rate_s2,
        radius_m,
    )

    shell_mass_kg = shell_energy_mass_kg(
        rate_s2,
        radius_m,
        exterior_mass_kg,
    )

    m_ext = (
        G
        * exterior_mass_kg
        / C**2
    )

    m_v = (
        G
        * volume_mass_kg
        / C**2
    )

    m_s = (
        G
        * shell_mass_kg
        / C**2
    )

    f_minus = (
        1.0
        - 2.0
        * m_v
        / radius_m
    )

    reconstructed = (
        m_v
        + m_s
        * math.sqrt(f_minus)
        + m_s**2
        / (
            2.0
            * radius_m
        )
    )

    return (
        reconstructed
        - m_ext
    ) * (
        C**2
        / G
    )
