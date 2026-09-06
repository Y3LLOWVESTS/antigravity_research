"""
Deterministic AGMINER candidate fingerprints.

Candidate identity contains:

FAMILY_ID
FAMILY_VERSION
CANONICAL_PARAMETER_VECTOR
PHYSICAL_MODEL_VERSION
ENERGY_LEDGER_VERSION

Changing numerical resolution alone must not silently create a different
physical candidate identity.
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any


def _canonicalize(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value

    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("Candidate parameters must be finite")

        if value == 0.0:
            value = 0.0

        return {
            "__float__": format(value, ".17g"),
        }

    if isinstance(value, dict):
        return {
            str(key): _canonicalize(value[key])
            for key in sorted(value, key=str)
        }

    if isinstance(value, (list, tuple)):
        return [_canonicalize(item) for item in value]

    raise TypeError(
        f"Unsupported candidate parameter type: {type(value).__name__}"
    )


def canonical_candidate_payload(
    *,
    family_id: str,
    family_version: str,
    params: dict[str, Any],
    physical_model_version: str,
    energy_ledger_version: str,
) -> dict[str, Any]:
    return {
        "family_id": family_id,
        "family_version": family_version,
        "params": _canonicalize(params),
        "physical_model_version": physical_model_version,
        "energy_ledger_version": energy_ledger_version,
    }


def canonical_candidate_bytes(**kwargs: Any) -> bytes:
    payload = canonical_candidate_payload(**kwargs)

    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )

    return encoded.encode("utf-8")


def candidate_fingerprint(**kwargs: Any) -> str:
    """
    Return the 24-hex-character AGMINER candidate identifier.
    """

    payload = canonical_candidate_bytes(**kwargs)
    return hashlib.sha256(payload).hexdigest()[:24]
