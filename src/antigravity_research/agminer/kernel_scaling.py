"""
Kernel-aware collective scaling diagnostics for AGMINER.

Global source charge scaling is not finite-payload response scaling.

A collective mechanism can only be promoted when the actual physical
payload response and complete energy scaling have both been derived.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class CollectivePromotionAssessment:
    promotable: bool
    reasons: tuple[str, ...]


def source_gain(
    charge_scale: float,
    source_efficiency_exponent: float,
) -> float:
    q = float(charge_scale)
    delta = float(source_efficiency_exponent)

    if q <= 1.0:
        raise ValueError("charge_scale must exceed one")

    return q ** delta


def maximum_combined_tax(
    source_efficiency_gain: float,
    required_gain: float,
) -> float:
    gs = float(source_efficiency_gain)
    gr = float(required_gain)

    if gs <= 0.0 or gr <= 0.0:
        raise ValueError("gains must be positive")

    return gs / gr


def minimum_retention_fraction(
    source_efficiency_gain: float,
    required_gain: float,
) -> float:
    return 1.0 / maximum_combined_tax(
        source_efficiency_gain,
        required_gain,
    )


def required_kernel_exponent(
    source_efficiency_exponent: float,
    required_gain: float,
    charge_scale: float,
) -> float:
    delta = float(source_efficiency_exponent)
    gain = float(required_gain)
    q = float(charge_scale)

    if gain <= 0.0:
        raise ValueError("required_gain must be positive")
    if q <= 1.0:
        raise ValueError("charge_scale must exceed one")

    return math.log(gain) / math.log(q) - delta


def net_efficiency_exponent(
    source_efficiency_exponent: float,
    kernel_participation_exponent: float,
    portal_efficiency_exponent: float = 0.0,
) -> float:
    return (
        float(source_efficiency_exponent)
        + float(kernel_participation_exponent)
        + float(portal_efficiency_exponent)
    )


def assess_collective_promotion(
    *,
    local_covariant_charge: bool,
    physical_vacuum_portal: bool,
    finite_payload_response_derived: bool,
    complete_portal_energy_scaling_derived: bool,
    normalization_invariant: bool,
    naturalness_screened: bool,
) -> CollectivePromotionAssessment:
    reasons = []

    if not local_covariant_charge:
        reasons.append("NO_LOCAL_COVARIANT_CHARGE")
    if not physical_vacuum_portal:
        reasons.append("NO_PHYSICAL_VACUUM_PORTAL")
    if not finite_payload_response_derived:
        reasons.append("FINITE_PAYLOAD_RESPONSE_SCALING_NOT_DERIVED")
    if not complete_portal_energy_scaling_derived:
        reasons.append("COMPLETE_PORTAL_ENERGY_SCALING_NOT_DERIVED")
    if not normalization_invariant:
        reasons.append("NORMALIZATION_INVARIANCE_NOT_ESTABLISHED")
    if not naturalness_screened:
        reasons.append("NATURALNESS_NOT_SCREENED")

    return CollectivePromotionAssessment(
        promotable=len(reasons) == 0,
        reasons=tuple(reasons),
    )
