"""Positive-energy gravitational repulsion from relativistic tension.

Consider an ideal planar surface source with:

    U   = surface energy density [J/m^2]
    tau = positive tangential tension [N/m = J/m^2]

The corresponding surface pressures are

    p_y = p_z = -tau.

For a reflection-symmetric planar wall, the weak-field/exact-wall
acceleration sign is governed by

    U - 2*tau.

We define outward acceleration as positive:

    a_out = 2*pi*G*(2*tau - U)/c^2.

Therefore:

    tau/U < 1/2  -> attraction
    tau/U = 1/2  -> zero active planar gravity
    tau/U > 1/2  -> repulsion

For positive U and nonnegative tension, the shell energy conditions are:

    NEC: U - tau >= 0
    WEC: U >= 0 and NEC
    DEC: U >= |tau|

Thus

    1/2 < tau/U <= 1

is a positive-energy, NEC/WEC/DEC-compatible repulsive window.

The endpoint tau=U is the ideal relativistic domain wall and maximizes
repulsion per unit positive surface energy.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from antigravity_research.geometry.kottler import C, G


GEV_J = 1.602176634e-10
GEV_INV_M = 1.973269804e-16

# 1 GeV^3 in SI wall tension J/m^2:
GEV3_TO_J_M2 = (
    GEV_J
    / GEV_INV_M**2
)


@dataclass(frozen=True)
class WallEnergyConditions:
    nec: bool
    wec: bool
    dec: bool


def outward_planar_acceleration_m_s2(
    surface_energy_j_m2: float,
    tension_n_m: float,
) -> float:
    """Outward gravitational acceleration on either side."""

    return (
        2.0
        * math.pi
        * G
        * (
            2.0 * tension_n_m
            - surface_energy_j_m2
        )
        / C**2
    )


def active_surface_mass_density_kg_m2(
    surface_energy_j_m2: float,
    tension_n_m: float,
) -> float:
    """Active surface mass density U - 2 tau divided by c^2."""

    return (
        surface_energy_j_m2
        - 2.0 * tension_n_m
    ) / C**2


def evaluate_wall_energy_conditions(
    surface_energy_j_m2: float,
    tension_n_m: float,
) -> WallEnergyConditions:

    scale = max(
        abs(surface_energy_j_m2),
        abs(tension_n_m),
        1.0,
    )

    tol = (
        scale
        * 1.0e-12
    )

    nec = (
        surface_energy_j_m2
        - tension_n_m
        >= -tol
    )

    wec = (
        surface_energy_j_m2
        >= -tol
        and nec
    )

    dec = (
        surface_energy_j_m2
        >= -tol
        and (
            surface_energy_j_m2
            - abs(tension_n_m)
        )
        >= -tol
    )

    return WallEnergyConditions(
        nec=nec,
        wec=wec,
        dec=dec,
    )


def required_surface_energy_j_m2(
    target_outward_acceleration_m_s2: float,
    tension_fraction_q: float,
) -> float:
    """Required positive surface energy for given tau/U=q."""

    if target_outward_acceleration_m_s2 <= 0.0:
        raise ValueError(
            "target acceleration must be positive"
        )

    if tension_fraction_q <= 0.5:
        raise ValueError(
            "q must exceed 1/2 for repulsion"
        )

    return (
        target_outward_acceleration_m_s2
        * C**2
        / (
            2.0
            * math.pi
            * G
            * (
                2.0 * tension_fraction_q
                - 1.0
            )
        )
    )


def domain_wall_minimum_surface_energy_j_m2(
    target_outward_acceleration_m_s2: float,
) -> float:
    """Minimum U within the DEC-compatible 0.5 < q <= 1 family."""

    return required_surface_energy_j_m2(
        target_outward_acceleration_m_s2,
        1.0,
    )


def surface_mass_equivalent_kg_m2(
    surface_energy_j_m2: float,
) -> float:

    return (
        surface_energy_j_m2
        / C**2
    )


# ============================================================
# phi^4 scalar kink
#
# V(phi) = lambda/4 * (phi^2 - v^2)^2
#
# Natural units:
#
# sigma = (2 sqrt(2)/3) sqrt(lambda) v^3
#
# thickness scale:
#
# delta = sqrt(2)/(v sqrt(lambda))
# ============================================================

def wall_tension_gev3_from_si(
    surface_energy_j_m2: float,
) -> float:

    return (
        surface_energy_j_m2
        / GEV3_TO_J_M2
    )


def phi4_v_gev_for_tension(
    surface_energy_j_m2: float,
    lambda_dimensionless: float,
) -> float:

    if surface_energy_j_m2 <= 0.0:
        raise ValueError(
            "surface energy must be positive"
        )

    if lambda_dimensionless <= 0.0:
        raise ValueError(
            "lambda must be positive"
        )

    sigma_gev3 = (
        wall_tension_gev3_from_si(
            surface_energy_j_m2
        )
    )

    coefficient = (
        2.0
        * math.sqrt(2.0)
        / 3.0
        * math.sqrt(
            lambda_dimensionless
        )
    )

    return (
        sigma_gev3
        / coefficient
    ) ** (
        1.0 / 3.0
    )


def phi4_wall_thickness_m(
    v_gev: float,
    lambda_dimensionless: float,
) -> float:

    if v_gev <= 0.0:
        raise ValueError(
            "v must be positive"
        )

    if lambda_dimensionless <= 0.0:
        raise ValueError(
            "lambda must be positive"
        )

    thickness_gev_inverse = (
        math.sqrt(2.0)
        / (
            v_gev
            * math.sqrt(
                lambda_dimensionless
            )
        )
    )

    return (
        thickness_gev_inverse
        * GEV_INV_M
    )


def circular_patch_energy_mass_kg(
    radius_m: float,
    surface_energy_j_m2: float,
) -> float:
    """Energy-equivalent mass of a circular patch.

    This is only an accounting quantity.

    It does NOT claim a free finite domain-wall disk is dynamically stable.
    """

    if radius_m <= 0.0:
        raise ValueError(
            "radius must be positive"
        )

    return (
        math.pi
        * radius_m**2
        * surface_energy_j_m2
        / C**2
    )
