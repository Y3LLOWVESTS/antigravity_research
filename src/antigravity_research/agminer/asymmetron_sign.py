"""
Published-asymmetron sign and thin-wall stability diagnostics.

The declared 2026 asymmetron keeps the symmetron Weyl factor

    A(phi) = 1 + phi^2/(2 M^2) + ...

and places explicit Z2 breaking in the bare scalar potential.

For nonrelativistic neutral matter,

    a_5 = -c^2 grad ln A.

This module tests the resulting wall/bubble sign before any expensive
field solve.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


C_LIGHT = 299792458.0


@dataclass(frozen=True)
class VacuumPair:
    phi_plus: float
    phi_minus: float
    delta: float


def asymmetron_vacua(
    phi0: float,
    kappa_over_lambda: float,
) -> VacuumPair:
    p0 = float(phi0)
    r = float(kappa_over_lambda)

    if p0 <= 0.0:
        raise ValueError("phi0 must be positive")
    if r < 0.0:
        raise ValueError("this gate uses kappa/lambda >= 0")

    delta = math.sqrt(1.0 + 0.25*r*r)

    return VacuumPair(
        phi_plus=p0*(0.5*r + delta),
        phi_minus=p0*(0.5*r - delta),
        delta=delta,
    )


def leading_weyl_factor(phi: float, m_scale: float) -> float:
    p = float(phi)
    m = float(m_scale)

    if m <= 0.0:
        raise ValueError("M must be positive")

    return 1.0 + p*p/(2.0*m*m)


def radial_fifth_acceleration(
    phi: float,
    dphi_dr: float,
    m_scale: float,
) -> float:
    p = float(phi)
    dp = float(dphi_dr)
    m = float(m_scale)
    a = leading_weyl_factor(p, m)

    return -C_LIGHT*C_LIGHT*p*dp/(m*m*a)


def true_inside_outer_side_sign() -> str:
    # true interior: phi>0 -> false exterior: phi<0
    # monotonic wall therefore has phi_prime<0.
    phi = -1.0
    dphi = -1.0
    accel = radial_fifth_acceleration(phi, dphi, 1.0)
    return "INWARD" if accel < 0.0 else "OUTWARD"


def false_inside_outer_side_sign() -> str:
    # false interior: phi<0 -> true exterior: phi>0
    # monotonic wall therefore has phi_prime>0.
    phi = 1.0
    dphi = 1.0
    accel = radial_fifth_acceleration(phi, dphi, 1.0)
    return "INWARD" if accel < 0.0 else "OUTWARD"


def static_bubble_critical_radius(
    sigma: float,
    epsilon: float,
) -> float:
    s = float(sigma)
    e = float(epsilon)

    if s <= 0.0 or e <= 0.0:
        raise ValueError("sigma and epsilon must be positive")

    return 2.0*s/e


def euclidean_bounce_radius(
    sigma: float,
    epsilon: float,
) -> float:
    s = float(sigma)
    e = float(epsilon)

    if s <= 0.0 or e <= 0.0:
        raise ValueError("sigma and epsilon must be positive")

    return 3.0*s/e


def static_bubble_second_derivative_at_critical(
    sigma: float,
) -> float:
    s = float(sigma)
    if s <= 0.0:
        raise ValueError("sigma must be positive")

    return -8.0*math.pi*s


def static_bubble_energy(
    radius: float,
    sigma: float,
    epsilon: float,
) -> float:
    r = float(radius)
    s = float(sigma)
    e = float(epsilon)

    return (
        4.0*math.pi*s*r*r
        - (4.0*math.pi/3.0)*e*r*r*r
    )
