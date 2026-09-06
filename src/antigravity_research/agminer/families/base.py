"""Base AGMINER family protocols.

Legacy families only need ``CandidateFamily``. New discovery families may opt
into the Introspective-factorized contract without breaking older plugins.
"""

from __future__ import annotations

from typing import Any, Protocol

from ..candidate import Candidate
from ..mechanism import MechanismMetrics
from ..oracle import ActionOracle, CollectiveScalingAssessment


class CandidateFamily(Protocol):
    family_id: str
    family_version: str

    def candidates(self) -> list[Candidate]:
        ...


class IntrospectiveDiscoveryFamily(Protocol):
    """Optional high-information contract for new physical families.

    Implementations must derive these quantities from the explicit family
    action. AGMINER must not fabricate them from generic tuning knobs.
    """

    family_id: str
    family_version: str

    def canonical_invariants(
        self,
        params: dict[str, Any],
        config: dict[str, Any],
    ) -> dict[str, Any]:
        ...

    def action_oracle(
        self,
        params: dict[str, Any],
        config: dict[str, Any],
    ) -> ActionOracle:
        ...

    def mechanism_metrics(
        self,
        solution: Any,
        params: dict[str, Any],
        config: dict[str, Any],
    ) -> MechanismMetrics:
        ...

    def collective_scaling_probe(
        self,
        params: dict[str, Any],
        config: dict[str, Any],
    ) -> CollectiveScalingAssessment | None:
        ...
