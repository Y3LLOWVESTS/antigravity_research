"""AGMINER core infrastructure.

AGMINER performs cheap candidate discovery, rejection-memory bookkeeping,
multi-fidelity screening, and shortlist preparation.

It does not itself certify an antigravity theory.
"""

from .candidate import Candidate
from .config import ENERGY_LIMIT_J
from .fingerprint import candidate_fingerprint
from .mechanism import MechanismMetrics
from .oracle import ActionOracle, CollectiveScalingAssessment
from .storage import Storage

__all__ = [
    "ActionOracle",
    "Candidate",
    "CollectiveScalingAssessment",
    "ENERGY_LIMIT_J",
    "MechanismMetrics",
    "Storage",
    "candidate_fingerprint",
]
