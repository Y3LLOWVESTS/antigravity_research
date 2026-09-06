"""
032V9 — Hopf-to-metric portal locality and mediator-energy preflight.

This module does not invent a new interaction.

It asks whether the source-side Q^(1/4) efficiency discovered in 032V8
can survive the structural requirements of a local physical portal.

Mathematical Hopf structure:

For n:S^3->S^2,

    F = n^*(omega_S2)

is a closed two-form. Because H^2(S^3)=0, introduce beta with

    F = d beta.

The Hopf invariant is proportional to

    integral beta wedge d beta.

Therefore Hopf charge is a secondary invariant. It is not the integral
of a target-space local three-form pulled back from S^2, since
H^3(S^2)=0.

An auxiliary connection, inverse derivative, lift, preferred structure,
or other additional field data is required to expose the Hopf charge as
a local current/source.

Canonical mediator scaling:

If mediator amplitude grows linearly with Q, canonical quadratic field
energy grows as Q^2.

For the V8 source-side energy law E_source~Q^(3/4) and a linear useful
response A~Q, the fixed-response equivalent energy has the normalized
form

    R(Q) = Q^(-1/4) + mu Q.

The first term is the V8 source advantage. The second is the canonical
mediator self-energy tax.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


HOPF_SOURCE_ENERGY_EXPONENT = 3.0 / 4.0
LINEAR_CHARGE_RESPONSE_EXPONENT = 1.0
CANONICAL_LINEAR_MEDIATOR_ENERGY_EXPONENT = 2.0


@dataclass(frozen=True)
class HopfPortalStructure:
    hopf_is_secondary_invariant: bool = True
    h3_s2_zero: bool = True
    local_target_space_three_form_density_exists: bool = False
    auxiliary_connection_required_for_cs_density: bool = True
    direct_minimal_einstein_hopf_charge_portal: bool = False
    derivative_scalar_current_static_bulk_source: bool = False


def fixed_response_ratio_linear_portal(
    charge_scale: float,
    mediator_coefficient: float,
) -> float:
    q = float(charge_scale)
    mu = float(mediator_coefficient)

    if q <= 0.0:
        raise ValueError("charge_scale must be positive")
    if mu < 0.0:
        raise ValueError("mediator_coefficient must be nonnegative")

    return q ** (-0.25) + mu * q


def optimum_charge_scale_linear_portal(
    mediator_coefficient: float,
) -> float:
    mu = float(mediator_coefficient)
    if mu <= 0.0:
        raise ValueError("mediator_coefficient must be positive")

    return (1.0 / (4.0 * mu)) ** (4.0 / 5.0)


def minimum_ratio_linear_portal(
    mediator_coefficient: float,
) -> float:
    mu = float(mediator_coefficient)
    if mu <= 0.0:
        raise ValueError("mediator_coefficient must be positive")

    return (5.0 / 4.0) * (4.0 * mu) ** (1.0 / 5.0)


def maximum_mediator_coefficient_for_ratio(
    target_ratio: float,
) -> float:
    r = float(target_ratio)
    if r <= 0.0:
        raise ValueError("target_ratio must be positive")

    return ((4.0 * r / 5.0) ** 5) / 4.0


def asymptotic_efficiency_exponent(
    response_exponent: float,
    source_energy_exponent: float,
    mediator_energy_exponent: float,
) -> float:
    return float(response_exponent) - max(
        float(source_energy_exponent),
        float(mediator_energy_exponent),
    )


def linear_portal_asymptotic_exponent() -> float:
    return asymptotic_efficiency_exponent(
        LINEAR_CHARGE_RESPONSE_EXPONENT,
        HOPF_SOURCE_ENERGY_EXPONENT,
        CANONICAL_LINEAR_MEDIATOR_ENERGY_EXPONENT,
    )


def quadratic_metric_portal_asymptotic_exponent() -> float:
    return asymptotic_efficiency_exponent(
        2.0,
        HOPF_SOURCE_ENERGY_EXPONENT,
        CANONICAL_LINEAR_MEDIATOR_ENERGY_EXPONENT,
    )
