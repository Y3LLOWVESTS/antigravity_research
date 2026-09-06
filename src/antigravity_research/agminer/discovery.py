"""Non-opaque AGMINER discovery diagnosis.

This module deliberately returns interpretable bottleneck labels instead of a
single optimization score. Hard physical gates remain separate.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from .mechanism import MechanismMetrics
from .oracle import ActionOracle, assess_oracle
from .policy import current_energy_policy


@dataclass(frozen=True)
class DiscoveryDiagnosis:
    target_j: float
    energy_factor_to_target: float
    organization_headroom: float | None
    residual_gain_after_ideal_organization: float | None
    realization_gap: float | None
    bottleneck: str
    next_action: str


def diagnose_candidate(
    *,
    current_complete_energy_j: float,
    oracle: ActionOracle | None = None,
    mechanism: MechanismMetrics | None = None,
    target_j: float | None = None,
) -> DiscoveryDiagnosis:
    if target_j is None:
        target_j = float(current_energy_policy()["limit_j"])

    target = float(target_j)
    current = float(current_complete_energy_j)

    if not math.isfinite(current) or current <= 0.0:
        raise ValueError("current_complete_energy_j must be finite and positive")
    if target <= 0.0:
        raise ValueError("target_j must be positive")

    factor = current / target
    organization = None
    residual = None

    if mechanism is not None:
        organization = mechanism.organization_headroom
        if organization is not None:
            residual = max(1.0, factor / organization)

    oracle_assessment = None if oracle is None else assess_oracle(
        oracle,
        target_j=target,
    )

    realization_gap = None
    if oracle_assessment is not None:
        realization_gap = oracle_assessment.realization_gap

    if current < target:
        bottleneck = "TARGET_ENERGY_CROSSED_NOT_CERTIFIED"
        next_action = "RUN_PHYSICAL_GATES_NOT_MORE_ENERGY_OPTIMIZATION"
    elif (
        oracle_assessment is not None
        and oracle_assessment.lower_bound_excludes_target is True
    ):
        bottleneck = "INTRINSIC_ACTION_FLOOR"
        next_action = "CHANGE_ACTION_KEEP_TRANSFERABLE_LESSONS"
    elif (
        oracle is not None
        and oracle.trusted_for_reachability
        and oracle.relaxed_complete_energy_j is not None
        and oracle.relaxed_complete_energy_j < target
    ):
        bottleneck = "MICROSCOPIC_REALIZATION_GAP"
        next_action = "OPTIMIZE_SOURCE_SCAFFOLD_AND_MORPHOLOGY"
    elif organization is not None and organization >= factor:
        bottleneck = "ORGANIZATION_LIMITED_OPTIMISTIC"
        next_action = "BUILD_ACTION_SPECIFIC_TEACHER_AND_REALIZATION"
    elif residual is not None and residual > 1.0:
        bottleneck = "INTRINSIC_CHARGE_PER_JOULE_LIMITED"
        next_action = "SEARCH_NONREDUNDANT_PROTECTED_CHARGE_MECHANISM"
    elif oracle is None:
        bottleneck = "ACTION_ORACLE_MISSING"
        next_action = "DERIVE_ACTION_SPECIFIC_ORACLE_BEFORE_DEEP_PDE"
    else:
        bottleneck = "UNRESOLVED"
        next_action = "IMPROVE_PROVENANCE_AND_DECOMPOSITION"

    return DiscoveryDiagnosis(
        target_j=target,
        energy_factor_to_target=factor,
        organization_headroom=organization,
        residual_gain_after_ideal_organization=residual,
        realization_gap=realization_gap,
        bottleneck=bottleneck,
        next_action=next_action,
    )
