"""Canonical-invariant fingerprints for normalization/provenance audits."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_invariant_fingerprint(
    *,
    family_id: str,
    family_version: str,
    invariants: dict[str, Any],
) -> str:
    if not invariants:
        raise ValueError("canonical invariants must not be empty")

    payload = {
        "family_id": str(family_id),
        "family_version": str(family_version),
        "invariants": invariants,
    }

    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")

    return "CANON_" + hashlib.sha256(encoded).hexdigest()[:24]


def normalization_equivalent(
    *,
    family_id: str,
    family_version: str,
    first_invariants: dict[str, Any],
    second_invariants: dict[str, Any],
) -> bool:
    return canonical_invariant_fingerprint(
        family_id=family_id,
        family_version=family_version,
        invariants=first_invariants,
    ) == canonical_invariant_fingerprint(
        family_id=family_id,
        family_version=family_version,
        invariants=second_invariants,
    )
