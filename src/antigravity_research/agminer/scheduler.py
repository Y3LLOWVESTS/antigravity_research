"""
Minimal 032A scheduler primitives.

The real physics campaign is deliberately not authorized yet.
"""

from __future__ import annotations

from dataclasses import dataclass

from .candidate import Candidate
from .gates import tier0_prefilter
from .storage import Storage


@dataclass(frozen=True)
class DispatchResult:
    candidate_id: str
    action: str
    state: str


def evaluate_mock_tier0(
    storage: Storage,
    candidate: Candidate,
    *,
    run_id: str,
    naturalness_threshold: float = 1.0,
) -> DispatchResult:
    if storage.is_terminal(candidate.candidate_id):
        return DispatchResult(
            candidate_id=candidate.candidate_id,
            action="SKIP_KNOWN",
            state=str(
                storage.candidate_state(candidate.candidate_id)
            ),
        )

    storage.record_candidate(
        candidate,
        state="TIER0_RUNNING",
        tier=0,
        run_id=run_id,
    )

    params = candidate.params

    result = tier0_prefilter(
        protection_specified=bool(
            params.get("protection_specified", False)
        ),
        naturalness_margin=params.get(
            "naturalness_margin"
        ),
        naturalness_threshold=naturalness_threshold,
        energy_estimate_j=float(
            params["energy_estimate_j"]
        ),
        energy_lower_j=params.get(
            "energy_lower_j"
        ),
        energy_upper_j=params.get(
            "energy_upper_j"
        ),
    )

    if not result.passed:
        storage.reject(
            candidate.candidate_id,
            state=result.state,
            failure_code=str(result.failure_code),
            gate=result.gate,
            energy_j=float(
                params["energy_estimate_j"]
            ),
            run_id=run_id,
        )

        return DispatchResult(
            candidate_id=candidate.candidate_id,
            action="REJECT",
            state=result.state,
        )

    storage.set_state(
        candidate.candidate_id,
        "TIER1_RUNNING",
        tier=1,
    )

    return DispatchResult(
        candidate_id=candidate.candidate_id,
        action="ADVANCE",
        state="TIER1_RUNNING",
    )
