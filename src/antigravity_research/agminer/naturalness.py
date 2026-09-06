"""
Cheap AGMINER naturalness/protection gate.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NaturalnessDecision:
    passed: bool
    failure_code: str | None
    state: str | None


def naturalness_gate(
    *,
    protection_specified: bool,
    margin: float | None,
    threshold: float = 1.0,
) -> NaturalnessDecision:
    if not protection_specified:
        return NaturalnessDecision(
            passed=False,
            failure_code="N003",
            state="REJECTED_NATURALNESS",
        )

    if margin is None or margin < threshold:
        return NaturalnessDecision(
            passed=False,
            failure_code="N001",
            state="REJECTED_NATURALNESS",
        )

    return NaturalnessDecision(
        passed=True,
        failure_code=None,
        state=None,
    )
