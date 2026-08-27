"""Finite relativistic-tension disk with a minimum-energy DEC rim.

The infinite-wall result is useful but not sufficient for a finite device.

A circular membrane of radius R has

    surface energy U               [J/m^2]
    tangential tension tau = q U   [N/m]

For q > 1/2 the membrane's local active gravitational density is negative:

    sigma_active = (U - 2 tau)/c^2.

A finite membrane cannot remain static without an edge support.

Mechanical equilibrium of a circular membrane requires a rim compression

    C = tau R.

For a one-dimensional rim, the dominant energy condition requires its
energy per unit length Lambda to satisfy

    Lambda >= |C|.

The most energy-efficient DEC-compatible support therefore has

    Lambda = C.

The rim then contributes positive active gravitational mass.

This construction implements the relativistic analogue of the stress
compensation underlying the von Laue / Tolman-pressure argument.

The resulting system:

    * has positive total energy;
    * can satisfy NEC/WEC/DEC component-by-component;
    * has local repulsive gravity close to the membrane;
    * has positive total active mass;
    * becomes attractive in the far field.

All gravitational field expressions here are in linearized GR.
"""

from __future__ import annotations

import math

from antigravity_research.geometry.kottler import C, G


def _validate(
    radius_m: float,
    surface_energy_j_m2: float,
    q: float,
) -> None:

    if radius_m <= 0.0:
        raise ValueError(
            "radius_m must be positive"
        )

    if surface_energy_j_m2 <= 0.0:
        raise ValueError(
            "surface energy must be positive"
        )

    if q < 0.0:
        raise ValueError(
            "q must be nonnegative"
        )


def membrane_active_surface_mass_density_kg_m2(
    surface_energy_j_m2: float,
    q: float,
) -> float:
    """Active gravitational surface mass density."""

    tau = (
        q
        * surface_energy_j_m2
    )

    return (
        surface_energy_j_m2
        - 2.0 * tau
    ) / C**2


def rim_compression_n(
    radius_m: float,
    surface_energy_j_m2: float,
    q: float,
) -> float:
    """Compression required to statically support the membrane."""

    _validate(
        radius_m,
        surface_energy_j_m2,
        q,
    )

    tau = (
        q
        * surface_energy_j_m2
    )

    return (
        tau
        * radius_m
    )


def minimum_dec_rim_energy_per_length_j_m(
    radius_m: float,
    surface_energy_j_m2: float,
    q: float,
) -> float:
    """Minimum rim energy/length allowed by DEC.

    For a line source with compressive pressure C:

        Lambda >= |C|.

    Minimum occurs at equality.
    """

    return rim_compression_n(
        radius_m,
        surface_energy_j_m2,
        q,
    )


def rim_active_line_mass_density_kg_m(
    radius_m: float,
    surface_energy_j_m2: float,
    q: float,
) -> float:
    """Active line mass of minimum-DEC rim.

    Active source = energy + pressure.

    At the DEC minimum:

        Lambda = C

    so active line energy is 2 C.
    """

    compression = rim_compression_n(
        radius_m,
        surface_energy_j_m2,
        q,
    )

    line_energy = (
        minimum_dec_rim_energy_per_length_j_m(
            radius_m,
            surface_energy_j_m2,
            q,
        )
    )

    return (
        line_energy
        + compression
    ) / C**2


def membrane_rest_mass_kg(
    radius_m: float,
    surface_energy_j_m2: float,
) -> float:

    return (
        math.pi
        * radius_m**2
        * surface_energy_j_m2
        / C**2
    )


def rim_rest_mass_kg(
    radius_m: float,
    surface_energy_j_m2: float,
    q: float,
) -> float:

    line_energy = (
        minimum_dec_rim_energy_per_length_j_m(
            radius_m,
            surface_energy_j_m2,
            q,
        )
    )

    circumference = (
        2.0
        * math.pi
        * radius_m
    )

    return (
        circumference
        * line_energy
        / C**2
    )


def total_rest_mass_kg(
    radius_m: float,
    surface_energy_j_m2: float,
    q: float,
) -> float:

    return (
        membrane_rest_mass_kg(
            radius_m,
            surface_energy_j_m2,
        )
        + rim_rest_mass_kg(
            radius_m,
            surface_energy_j_m2,
            q,
        )
    )


def membrane_active_mass_kg(
    radius_m: float,
    surface_energy_j_m2: float,
    q: float,
) -> float:

    sigma = (
        membrane_active_surface_mass_density_kg_m2(
            surface_energy_j_m2,
            q,
        )
    )

    return (
        math.pi
        * radius_m**2
        * sigma
    )


def rim_active_mass_kg(
    radius_m: float,
    surface_energy_j_m2: float,
    q: float,
) -> float:

    line_density = (
        rim_active_line_mass_density_kg_m(
            radius_m,
            surface_energy_j_m2,
            q,
        )
    )

    return (
        2.0
        * math.pi
        * radius_m
        * line_density
    )


def total_active_mass_kg(
    radius_m: float,
    surface_energy_j_m2: float,
    q: float,
) -> float:

    return (
        membrane_active_mass_kg(
            radius_m,
            surface_energy_j_m2,
            q,
        )
        + rim_active_mass_kg(
            radius_m,
            surface_energy_j_m2,
            q,
        )
    )


def integrated_spatial_stress_j(
    radius_m: float,
    surface_energy_j_m2: float,
    q: float,
) -> tuple[float, float, float]:
    """Integrated spatial-stress trace.

    Membrane:
        Tii integral = -2 tau A

    Rim:
        Tii integral = +C * circumference

    For C=tau R they cancel exactly.
    """

    tau = (
        q
        * surface_energy_j_m2
    )

    area = (
        math.pi
        * radius_m**2
    )

    membrane = (
        -2.0
        * tau
        * area
    )

    compression = rim_compression_n(
        radius_m,
        surface_energy_j_m2,
        q,
    )

    rim = (
        compression
        * 2.0
        * math.pi
        * radius_m
    )

    return (
        membrane,
        rim,
        membrane + rim,
    )


def dimensionless_axis_factor(
    q: float,
    x: float,
) -> float:
    """Dimensionless total acceleration factor.

    x = z/R.

    a_z =
        2*pi*G*U/c^2 * F(q,x)

    Positive means outward away from the membrane.
    """

    if x < 0.0:
        raise ValueError(
            "x must be nonnegative"
        )

    root = math.sqrt(
        1.0
        + x**2
    )

    membrane = (
        (2.0 * q - 1.0)
        * (
            1.0
            - x / root
        )
    )

    rim = (
        -2.0
        * q
        * x
        / (
            1.0
            + x**2
        ) ** 1.5
    )

    return (
        membrane
        + rim
    )


def axial_acceleration_m_s2(
    height_m: float,
    radius_m: float,
    surface_energy_j_m2: float,
    q: float,
) -> float:
    """Net axial acceleration in linearized GR.

    Positive = away from the upper face of the membrane.
    """

    _validate(
        radius_m,
        surface_energy_j_m2,
        q,
    )

    if height_m < 0.0:
        raise ValueError(
            "height must be nonnegative"
        )

    x = (
        height_m
        / radius_m
    )

    factor = (
        dimensionless_axis_factor(
            q,
            x,
        )
    )

    return (
        2.0
        * math.pi
        * G
        * surface_energy_j_m2
        / C**2
        * factor
    )


def mass_coefficient_for_target(
    q: float,
    x: float,
) -> float:
    """Dimensionless mass coefficient.

    For a target acceleration a at stand-off h,

        M = coefficient * a*h^2/G.

    This assumes the minimum-DEC support rim.
    """

    factor = (
        dimensionless_axis_factor(
            q,
            x,
        )
    )

    if factor <= 0.0:
        return math.inf

    return (
        1.0
        + 2.0 * q
    ) / (
        2.0
        * x**2
        * factor
    )


def required_surface_energy_for_target_j_m2(
    target_acceleration_m_s2: float,
    q: float,
    x: float,
) -> float:

    factor = (
        dimensionless_axis_factor(
            q,
            x,
        )
    )

    if factor <= 0.0:
        raise ValueError(
            "requested point is outside repulsive region"
        )

    return (
        target_acceleration_m_s2
        * C**2
        / (
            2.0
            * math.pi
            * G
            * factor
        )
    )


def compactness_parameter(
    total_mass_kg: float,
    radius_m: float,
) -> float:
    """GM/(c^2 R), for checking linearized-GR regime."""

    return (
        G
        * total_mass_kg
        / (
            C**2
            * radius_m
        )
    )
