"""
Persistent candidate representation used by AGMINER.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .fingerprint import candidate_fingerprint


@dataclass(frozen=True)
class Candidate:
    family_id: str
    family_version: str
    params: dict[str, Any]
    physical_model_version: str
    energy_ledger_version: str

    @property
    def candidate_id(self) -> str:
        return candidate_fingerprint(
            family_id=self.family_id,
            family_version=self.family_version,
            params=self.params,
            physical_model_version=self.physical_model_version,
            energy_ledger_version=self.energy_ledger_version,
        )
