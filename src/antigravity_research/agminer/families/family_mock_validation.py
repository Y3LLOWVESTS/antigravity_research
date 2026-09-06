"""
Synthetic nonphysical validation candidates for AGMINER infrastructure tests.

These are software controls only.
"""

from __future__ import annotations

from ..candidate import Candidate


def unprotected_sub10_control() -> Candidate:
    return Candidate(
        family_id="MOCK_031_LIKE_UNPROTECTED",
        family_version="1",
        params={
            "energy_estimate_j": 8.0e6,
            "energy_lower_j": 7.9e6,
            "energy_upper_j": 8.1e6,
            "protection_specified": False,
            "naturalness_margin": 0.0,
        },
        physical_model_version="SYNTHETIC_VALIDATION_ONLY",
        energy_ledger_version="CONSERVATIVE_COMPLETE_V1",
    )


def protected_sub10_control() -> Candidate:
    return Candidate(
        family_id="MOCK_PROTECTED_SUB10",
        family_version="1",
        params={
            "energy_estimate_j": 8.0e6,
            "energy_lower_j": 7.9e6,
            "energy_upper_j": 8.1e6,
            "protection_specified": True,
            "naturalness_margin": 100.0,
        },
        physical_model_version="SYNTHETIC_VALIDATION_ONLY",
        energy_ledger_version="CONSERVATIVE_COMPLETE_V1",
    )
