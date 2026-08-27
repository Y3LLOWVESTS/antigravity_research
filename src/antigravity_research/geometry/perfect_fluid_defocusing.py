"""Perfect-fluid geodesic-defocusing benchmark.

This module investigates a deliberately idealized locally homogeneous and
isotropic perfect-fluid source.

For energy density epsilon [J/m^3] and isotropic pressure p [Pa]:

    k = xi_ddot / xi
      = -(4*pi*G / (3*c^2)) * (epsilon + 3*p)
        + Lambda*c^2/3

where k has units s^-2.

For a separation L:

    relative acceleration = k * L

Positive k means neighboring freely falling observers accelerate apart.

IMPORTANT
---------

This is NOT a complete model of a localized antigravity device.

A real finite source would also require:
- a self-consistent spacetime metric;
- boundary/matching conditions;
- stress-energy conservation;
- source stability;
- treatment of anisotropic boundary stresses;
- causal dynamics.

The purpose here is to calculate the local curvature/stress-energy scale
required before attempting a full spacetime solution.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from antigravity_research.geometry.kottler import C, G


@dataclass(frozen=True)
class EnergyConditions:
    nec: bool
    wec: bool
    sec: bool
    dec: bool


def isotropic_defocusing_rate_s2(
    energy_density_j_m3: float,
    pressure_pa: float,
    cosmological_constant_m2: float = 0.0,
) -> float:
    """Return local isotropic relative-acceleration rate k in s^-2."""

    matter_term = (
        -4.0
        * math.pi
        * G
        / (3.0 * C**2)
        * (
            energy_density_j_m3
            + 3.0 * pressure_pa
        )
    )

    lambda_term = (
        cosmological_constant_m2
        * C**2
        / 3.0
    )

    return matter_term + lambda_term


def active_mass_density_kg_m3(
    energy_density_j_m3: float,
    pressure_pa: float,
) -> float:
    """Return (epsilon + 3p)/c^2 in kg/m^3."""

    return (
        energy_density_j_m3
        + 3.0 * pressure_pa
    ) / C**2


def required_active_mass_density_kg_m3(
    target_relative_acceleration_m_s2: float,
    separation_m: float,
    cosmological_constant_m2: float = 0.0,
) -> float:
    """Solve for active gravitational density needed for a target effect.

    target acceleration = k * separation

    rho_active =
        -3/(4*pi*G) * (k - Lambda*c^2/3)
    """

    if separation_m <= 0.0:
        raise ValueError("separation_m must be positive")

    k_target = (
        target_relative_acceleration_m_s2
        / separation_m
    )

    lambda_rate = (
        cosmological_constant_m2
        * C**2
        / 3.0
    )

    return (
        -3.0
        / (4.0 * math.pi * G)
        * (
            k_target
            - lambda_rate
        )
    )


def required_energy_density_for_w(
    target_relative_acceleration_m_s2: float,
    separation_m: float,
    w: float,
    cosmological_constant_m2: float = 0.0,
) -> float:
    """Return required epsilon [J/m^3] for p = w*epsilon.

    Because:

        epsilon + 3p = epsilon * (1 + 3w)

    w = -1/3 cannot generate isotropic acceleration through this term
    at any finite epsilon.
    """

    denominator = 1.0 + 3.0 * w

    if math.isclose(
        denominator,
        0.0,
        abs_tol=1e-14,
    ):
        raise ValueError(
            "w = -1/3 gives zero active gravitational density "
            "for any finite energy density"
        )

    rho_active = required_active_mass_density_kg_m3(
        target_relative_acceleration_m_s2,
        separation_m,
        cosmological_constant_m2,
    )

    return (
        rho_active
        * C**2
        / denominator
    )


def evaluate_energy_conditions(
    energy_density_j_m3: float,
    pressure_pa: float,
) -> EnergyConditions:
    """Evaluate perfect-fluid energy conditions.

    For a perfect fluid:

    NEC:
        epsilon + p >= 0

    WEC:
        epsilon >= 0
        epsilon + p >= 0

    SEC:
        epsilon + p >= 0
        epsilon + 3p >= 0

    DEC:
        epsilon >= 0
        epsilon >= |p|
    """

    scale = max(
        abs(energy_density_j_m3),
        abs(pressure_pa),
        1.0,
    )

    tolerance = scale * 1e-12

    nec_term = (
        energy_density_j_m3
        + pressure_pa
    )

    sec_term = (
        energy_density_j_m3
        + 3.0 * pressure_pa
    )

    nec = (
        nec_term
        >= -tolerance
    )

    wec = (
        energy_density_j_m3
        >= -tolerance
        and nec
    )

    sec = (
        nec
        and sec_term
        >= -tolerance
    )

    dec = (
        energy_density_j_m3
        >= -tolerance
        and (
            energy_density_j_m3
            - abs(pressure_pa)
        )
        >= -tolerance
    )

    return EnergyConditions(
        nec=nec,
        wec=wec,
        sec=sec,
        dec=dec,
    )
