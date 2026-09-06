"""
AGMINER learning-corridor provenance rules.

Purpose:
  Prevent obsolete or superseded quantitative energy estimates from
  being promoted as present-day near-miss candidates.

Important distinction:

  SUPERSEDED_QUANTITATIVE_RESULT
      means the stored number must not drive current candidate ranking.

  It does NOT necessarily mean every theory in that broad family has
  been physically closed.

Historical lessons are retained.
Closed branches are not reopened.
"""

from __future__ import annotations

from dataclasses import dataclass


PROVENANCE_CURRENT = "CURRENT_QUANTITATIVE_PROVENANCE"
PROVENANCE_SUPERSEDED = "SUPERSEDED_QUANTITATIVE_PROVENANCE"
PROVENANCE_HISTORICAL = "HISTORICAL_VERIFIED_CONTROL"


SUPERSEDED_ENERGY_FAMILIES = {
    "032C_TWIN_PNGB_DBI_METRIC": {
        "reason": "PRELIMINARY_SOURCE_LEDGER_SUPERSEDED_BY_SOURCE_AWARE_RECONSTRUCTION",
        "replacement_program": "032G_032H_SOURCE_AWARE_SHARED_SOURCE_VECTOR_CHARGE",
        "broad_family_closed": False,
    },
    "032E_COLLECTIVE_MULTISCALAR_TWIN_PNGB": {
        "reason": "PRELIMINARY_COLLECTIVE_SOURCE_LEDGER_SUPERSEDED_BY_SOURCE_AWARE_RECONSTRUCTION",
        "replacement_program": "032G_032H_SOURCE_AWARE_SHARED_SOURCE_VECTOR_CHARGE",
        "broad_family_closed": False,
    },
}


@dataclass(frozen=True)
class ProvenanceAssessment:
    family: str
    status: str
    usable_for_active_energy_ranking: bool
    historical_lesson_preserved: bool
    reason: str
    replacement_program: str | None



def assess_family_provenance(family: str) -> ProvenanceAssessment:
    family = str(family)

    if family in SUPERSEDED_ENERGY_FAMILIES:
        info = SUPERSEDED_ENERGY_FAMILIES[family]
        return ProvenanceAssessment(
            family=family,
            status=PROVENANCE_SUPERSEDED,
            usable_for_active_energy_ranking=False,
            historical_lesson_preserved=True,
            reason=str(info["reason"]),
            replacement_program=str(info["replacement_program"]),
        )

    return ProvenanceAssessment(
        family=family,
        status=PROVENANCE_CURRENT,
        usable_for_active_energy_ranking=True,
        historical_lesson_preserved=True,
        reason="NO_SUPERSESSION_RULE_REGISTERED",
        replacement_program=None,
    )
