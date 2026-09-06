"""
Finite-payload AGMINER gate helpers.

These are generic infrastructure checks only.
Theory-specific metric/force calculations belong in family modules.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PayloadDecision:
    passed: bool
    failure_code: str | None
    state: str | None


def payload_gate(
    *,
    cm_accel_mps2: float,
    surface_min_accel_mps2: float,
    target_cm_accel_mps2: float,
    target_surface_accel_mps2: float,
) -> PayloadDecision:
    if cm_accel_mps2 <= 0.0:
        return PayloadDecision(
            passed=False,
            failure_code="P001",
            state="REJECTED_PAYLOAD",
        )

    if cm_accel_mps2 < target_cm_accel_mps2:
        return PayloadDecision(
            passed=False,
            failure_code="P001",
            state="REJECTED_PAYLOAD",
        )

    if surface_min_accel_mps2 < target_surface_accel_mps2:
        return PayloadDecision(
            passed=False,
            failure_code="P002",
            state="REJECTED_PAYLOAD",
        )

    return PayloadDecision(
        passed=True,
        failure_code=None,
        state=None,
    )
