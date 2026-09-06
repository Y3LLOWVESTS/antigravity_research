"""
Feasibility-first learning bands for AGMINER.

This module does NOT alter the strict physical energy objective.

Strict project target:
    E_complete < 10 MJ.

Additional bands exist only to retain useful scientific near misses:

    TARGET          E < 10 MJ
    NEAR_MISS       10 MJ <= E < 100 MJ
    MECHANISM       100 MJ <= E <= 1 GJ
    ARCHIVE         E > 1 GJ

Only TARGET can ever be certification-eligible.

A higher-energy learning case is not a successful antigravity model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


STRICT_TARGET_J = 10_000_000.0
NEAR_MISS_CEILING_J = 100_000_000.0
MECHANISM_CEILING_J = 1_000_000_000.0


BAND_TARGET = "TARGET_LT_10MJ"
BAND_NEAR = "NEAR_MISS_10_TO_100MJ"
BAND_MECHANISM = "MECHANISM_100MJ_TO_1GJ"
BAND_ARCHIVE = "ARCHIVE_GT_1GJ"


@dataclass(frozen=True)
class LearningAssessment:
    energy_j: float
    band: str
    target_factor: float
    strict_energy_success: bool
    certification_energy_eligible: bool
    learning_priority: str
    proof_backed_floor_j: Optional[float]
    same_declared_branch_can_reach_target: Optional[bool]
    removable_energy_above_floor_j: Optional[float]
    maximum_proven_reduction_factor: Optional[float]


def classify_energy(energy_j: float) -> str:
    energy = float(energy_j)

    if energy < 0.0:
        raise ValueError("energy_j must be nonnegative")

    if energy < STRICT_TARGET_J:
        return BAND_TARGET

    if energy < NEAR_MISS_CEILING_J:
        return BAND_NEAR

    if energy <= MECHANISM_CEILING_J:
        return BAND_MECHANISM

    return BAND_ARCHIVE


def learning_priority_for_band(band: str) -> str:
    if band == BAND_TARGET:
        return "CERTIFICATION_PRECHECK_PRIORITY"
    if band == BAND_NEAR:
        return "HIGH_LEARNING_PRIORITY"
    if band == BAND_MECHANISM:
        return "CONDITIONAL_MECHANISM_PRIORITY"
    return "ARCHIVE_UNLESS_NOVEL_MECHANISM"


def assess_energy(
    energy_j: float,
    *,
    proof_backed_floor_j: float | None = None,
) -> LearningAssessment:
    energy = float(energy_j)
    band = classify_energy(energy)

    strict = energy < STRICT_TARGET_J

    floor = None
    same_branch = None
    removable = None
    max_reduction = None

    if proof_backed_floor_j is not None:
        floor = float(proof_backed_floor_j)

        if floor < 0.0:
            raise ValueError("proof_backed_floor_j must be nonnegative")

        if floor > energy:
            raise ValueError("proof-backed floor cannot exceed total energy")

        same_branch = floor < STRICT_TARGET_J
        removable = energy - floor

        if floor == 0.0:
            max_reduction = float("inf")
        else:
            max_reduction = energy / floor

    return LearningAssessment(
        energy_j=energy,
        band=band,
        target_factor=energy / STRICT_TARGET_J,
        strict_energy_success=strict,
        certification_energy_eligible=strict,
        learning_priority=learning_priority_for_band(band),
        proof_backed_floor_j=floor,
        same_declared_branch_can_reach_target=same_branch,
        removable_energy_above_floor_j=removable,
        maximum_proven_reduction_factor=max_reduction,
    )
