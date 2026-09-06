"""Config-driven conservative-complete AGMINER energy gate."""

from __future__ import annotations

from dataclasses import dataclass

from .policy import current_energy_policy


@dataclass(frozen=True)
class EnergyDecision:
    passed: bool
    failure_code: str | None
    state: str | None
    borderline: bool
    policy_id: str


def _fails(value_j: float, limit_j: float, inclusive: bool) -> bool:
    if inclusive:
        return value_j > limit_j

    return value_j >= limit_j


def hard_energy_gate(
    energy_j: float,
    *,
    lower_j: float | None = None,
    upper_j: float | None = None,
    reliable_estimate: bool = True,
    limit_j: float | None = None,
    inclusive: bool | None = None,
    policy_id: str | None = None,
) -> EnergyDecision:
    policy = current_energy_policy()

    if limit_j is None:
        limit_j = float(policy["limit_j"])

    if inclusive is None:
        inclusive = bool(policy["inclusive"])

    if policy_id is None:
        policy_id = str(policy["policy_id"])

    state = "REJECTED_ENERGY_OBJECTIVE:" + policy_id

    if lower_j is not None and _fails(float(lower_j), limit_j, inclusive):
        return EnergyDecision(False, "E001", state, False, policy_id)

    if reliable_estimate and _fails(float(energy_j), limit_j, inclusive):
        return EnergyDecision(False, "E002", state, False, policy_id)

    borderline = (
        upper_j is not None
        and _fails(float(upper_j), limit_j, inclusive)
    )

    return EnergyDecision(True, None, None, borderline, policy_id)


def refined_energy_gate(
    energy_j: float,
    *,
    limit_j: float | None = None,
    inclusive: bool | None = None,
    policy_id: str | None = None,
) -> EnergyDecision:
    result = hard_energy_gate(
        energy_j,
        limit_j=limit_j,
        inclusive=inclusive,
        policy_id=policy_id,
    )

    if result.passed:
        return result

    return EnergyDecision(
        False,
        "E003",
        result.state,
        False,
        result.policy_id,
    )
