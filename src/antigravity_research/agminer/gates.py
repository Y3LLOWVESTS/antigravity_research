"""
Generic fail-fast AGMINER gate orchestration.

Theory-specific equations are intentionally absent from this module.
"""

from __future__ import annotations

from dataclasses import dataclass

from .energy import hard_energy_gate
from .naturalness import naturalness_gate


@dataclass(frozen=True)
class Tier0Result:
    passed: bool
    state: str
    failure_code: str | None
    gate: str


def tier0_prefilter(
    *,
    protection_specified: bool,
    naturalness_margin: float | None,
    naturalness_threshold: float,
    energy_estimate_j: float,
    energy_lower_j: float | None = None,
    energy_upper_j: float | None = None,
) -> Tier0Result:
    naturalness = naturalness_gate(
        protection_specified=protection_specified,
        margin=naturalness_margin,
        threshold=naturalness_threshold,
    )

    if not naturalness.passed:
        return Tier0Result(
            passed=False,
            state=str(naturalness.state),
            failure_code=naturalness.failure_code,
            gate="naturalness",
        )

    energy = hard_energy_gate(
        energy_estimate_j,
        lower_j=energy_lower_j,
        upper_j=energy_upper_j,
    )

    if not energy.passed:
        return Tier0Result(
            passed=False,
            state=str(energy.state),
            failure_code=energy.failure_code,
            gate="energy",
        )

    return Tier0Result(
        passed=True,
        state="TIER0_PASS",
        failure_code=None,
        gate="tier0",
    )
