"""
Configuration helpers for AGMINER 032A.

The 10 GJ limit is applied to conservative complete operating inventory.
Exactly 10 GJ survives. Values above 10 GJ fail.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


ENERGY_LIMIT_J = 1.0e7
ENERGY_LIMIT_GJ = ENERGY_LIMIT_J / 1.0e9

DEFAULT_CONFIG: dict[str, Any] = {
    "energy_limit_j": ENERGY_LIMIT_J,
    "payload_mass_kg": 1.0,
    "payload_radius_m": 0.10,
    "target_surface_accel_mps2": 9.80665,
    "target_cm_accel_mps2": 9.80665,
    "sampler_seed": 3201,
    "worker_count": 1,
    "tier0_budget": 10000,
    "tier1_budget": 1000,
    "tier2_budget": 25,
    "disk_budget_mb": 500,
    "checkpoint_limit": 25,
    "logging_limit_mb": 2,
    "logging_backup_count": 2,
    "naturalness_threshold": 1.0,
    "leak_limit": 1.0e-4,
    "backreaction_limit": 1.0e-2,
    "database_path": "results/agminer/agminer.sqlite3",
    "log_path": "results/agminer/agminer_current.log",
    "physical_model_version": "032A_INFRASTRUCTURE_ONLY",
    "energy_ledger_version": "CONSERVATIVE_COMPLETE_V1",
}


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def config_fingerprint(config: dict[str, Any]) -> str:
    """
    Return a compact deterministic identifier for the effective configuration.
    """

    payload = _canonical_json(config).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """
    Load the effective AGMINER configuration.

    Missing user fields inherit the 032A defaults.
    """

    config = deepcopy(DEFAULT_CONFIG)

    if path is None:
        return config

    source = Path(path)
    if not source.exists():
        return config

    with source.open("r", encoding="utf-8") as handle:
        loaded = json.load(handle)

    if not isinstance(loaded, dict):
        raise ValueError("AGMINER config must be a JSON object")

    config.update(loaded)
    return config
