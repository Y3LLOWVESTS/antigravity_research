"""Action-specific relaxed-oracle and collective-scaling contracts.

The oracle layer separates intrinsic action limits from microscopic
realization costs. It is deliberately explicit about energy semantics so an
optimistic relaxed source cannot be confused with a complete realized field.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

from .learning import assess_energy
from .policy import current_energy_policy


LEDGER_COMPLETE_RELAXED = "CONSERVATIVE_COMPLETE_RELAXED"
LEDGER_PARTIAL_OPTIMISTIC = "PARTIAL_OPTIMISTIC"


@dataclass(frozen=True)
class ActionOracle:
    canonical_invariant_id: str
    proof_reference: str
    proven_lower_bound_j: float | None = None
    relaxed_complete_energy_j: float | None = None
    realized_complete_energy_j: float | None = None
    ledger_scope: str = LEDGER_PARTIAL_OPTIMISTIC
    normalization_invariant: bool = False
    naturalness_screened: bool = False
    universal_metric_screened: bool = False

    def __post_init__(self) -> None:
        if not self.canonical_invariant_id:
            raise ValueError("canonical_invariant_id is required")
        if not self.proof_reference:
            raise ValueError("proof_reference is required")

        values = [
            self.proven_lower_bound_j,
            self.relaxed_complete_energy_j,
            self.realized_complete_energy_j,
        ]

        for value in values:
            if value is None:
                continue
            numeric = float(value)
            if not math.isfinite(numeric) or numeric < 0.0:
                raise ValueError("oracle energies must be finite and nonnegative")

        lower = self.proven_lower_bound_j
        relaxed = self.relaxed_complete_energy_j
        realized = self.realized_complete_energy_j

        if lower is not None and relaxed is not None and lower > relaxed:
            raise ValueError("proven lower bound cannot exceed relaxed energy")
        if relaxed is not None and realized is not None and relaxed > realized:
            raise ValueError("relaxed energy cannot exceed realized energy")

    @property
    def trusted_for_reachability(self) -> bool:
        return (
            self.ledger_scope == LEDGER_COMPLETE_RELAXED
            and self.normalization_invariant
            and self.naturalness_screened
            and self.universal_metric_screened
        )


@dataclass(frozen=True)
class OracleAssessment:
    target_j: float
    lower_bound_excludes_target: bool | None
    relaxed_band: str | None
    realized_band: str | None
    realization_gap: float | None
    trusted_for_reachability: bool
    priority: str


def assess_oracle(
    oracle: ActionOracle,
    *,
    target_j: float | None = None,
) -> OracleAssessment:
    if target_j is None:
        target_j = float(current_energy_policy()["limit_j"])

    target = float(target_j)
    if target <= 0.0:
        raise ValueError("target_j must be positive")

    lower = oracle.proven_lower_bound_j
    relaxed = oracle.relaxed_complete_energy_j
    realized = oracle.realized_complete_energy_j

    excludes = None if lower is None else lower >= target
    relaxed_band = None if relaxed is None else assess_energy(relaxed).band
    realized_band = None if realized is None else assess_energy(realized).band

    gap = None
    if relaxed is not None and realized is not None:
        if relaxed == 0.0:
            gap = math.inf
        else:
            gap = realized / relaxed

    if realized is not None and realized < target:
        priority = "TARGET_ENERGY_CROSSED_NOT_CERTIFIED"
    elif (
        oracle.trusted_for_reachability
        and relaxed is not None
        and relaxed < target
    ):
        priority = "REALIZATION_LIMITED_HIGH_PRIORITY"
    elif oracle.trusted_for_reachability and relaxed is not None:
        band = assess_energy(relaxed).band
        if band == "NEAR_MISS_10_TO_100MJ":
            priority = "ACTION_ORACLE_NEAR_MISS"
        elif band == "MECHANISM_100MJ_TO_1GJ":
            priority = "ACTION_ORACLE_MECHANISM_LEARNING"
        else:
            priority = "ACTION_ORACLE_ARCHIVE"
    elif excludes is True:
        priority = "PROVEN_INTRINSIC_FLOOR_ABOVE_TARGET"
    else:
        priority = "ORACLE_PROVENANCE_INCOMPLETE"

    return OracleAssessment(
        target_j=target,
        lower_bound_excludes_target=excludes,
        relaxed_band=relaxed_band,
        realized_band=realized_band,
        realization_gap=gap,
        trusted_for_reachability=oracle.trusted_for_reachability,
        priority=priority,
    )


@dataclass(frozen=True)
class CollectiveScalingAssessment:
    sample_count: int
    response_exponent: float
    energy_exponent: float
    efficiency_exponent: float
    scaffold_exponent: float | None
    beneficial_collective_scaling: bool


def _log_slope(x_values: list[float], y_values: list[float]) -> float:
    lx = [math.log(value) for value in x_values]
    ly = [math.log(value) for value in y_values]
    mean_x = sum(lx) / len(lx)
    mean_y = sum(ly) / len(ly)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(lx, ly))
    denominator = sum((x - mean_x) ** 2 for x in lx)
    if denominator == 0.0:
        raise ValueError("collective scale values must not all be identical")
    return numerator / denominator


def assess_collective_scaling(
    n_values: Iterable[float],
    useful_response_values: Iterable[float],
    complete_energy_values: Iterable[float],
    *,
    scaffold_energy_values: Iterable[float] | None = None,
) -> CollectiveScalingAssessment:
    n = [float(value) for value in n_values]
    response = [float(value) for value in useful_response_values]
    energy = [float(value) for value in complete_energy_values]

    if len(n) < 3 or len(n) != len(response) or len(n) != len(energy):
        raise ValueError("collective scaling requires >=3 matched samples")

    if any(value <= 0.0 or not math.isfinite(value) for value in n + response + energy):
        raise ValueError("collective scaling inputs must be finite and positive")

    response_exponent = _log_slope(n, response)
    energy_exponent = _log_slope(n, energy)
    efficiency_exponent = response_exponent - energy_exponent

    scaffold_exponent = None
    if scaffold_energy_values is not None:
        scaffold = [float(value) for value in scaffold_energy_values]
        if len(scaffold) != len(n):
            raise ValueError("scaffold_energy_values length mismatch")
        if any(value <= 0.0 or not math.isfinite(value) for value in scaffold):
            raise ValueError("scaffold energies must be finite and positive")
        scaffold_exponent = _log_slope(n, scaffold)

    return CollectiveScalingAssessment(
        sample_count=len(n),
        response_exponent=response_exponent,
        energy_exponent=energy_exponent,
        efficiency_exponent=efficiency_exponent,
        scaffold_exponent=scaffold_exponent,
        beneficial_collective_scaling=efficiency_exponent > 0.0,
    )
