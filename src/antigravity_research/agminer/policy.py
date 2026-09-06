"""AGMINER configurable operating-energy policy."""

from __future__ import annotations

import hashlib
import json
import os
from decimal import Decimal
from pathlib import Path


UNIT_TO_J = {
    "J": Decimal("1"),
    "kJ": Decimal("1e3"),
    "MJ": Decimal("1e6"),
    "GJ": Decimal("1e9"),
    "TJ": Decimal("1e12"),
}

VALID_COMPARISONS = {"LT", "LE"}

DEFAULT_VALUE = Decimal("10")
DEFAULT_UNIT = "MJ"
DEFAULT_COMPARISON = "LT"
DEFAULT_LEDGER = "CONSERVATIVE_COMPLETE_OPERATING"
DEFAULT_LEDGER_VERSION = "CONSERVATIVE_COMPLETE_V1"


def config_path() -> Path:
    return (
        Path(__file__).resolve().parents[3]
        / "config"
        / "agminer_032a.json"
    )


def current_energy_policy() -> dict[str, object]:
    value = DEFAULT_VALUE
    unit = DEFAULT_UNIT
    comparison = DEFAULT_COMPARISON
    ledger = DEFAULT_LEDGER
    ledger_version = DEFAULT_LEDGER_VERSION

    path = config_path()

    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        target = data.get("energy_target", {})

        value = Decimal(str(target.get("value", value)))
        unit = str(target.get("unit", unit))
        comparison = str(target.get("comparison", comparison)).upper()
        ledger = str(data.get("energy_ledger", ledger))
        ledger_version = str(data.get("energy_ledger_version", ledger_version))

    env_value = os.environ.get("AGMINER_ENERGY_TARGET_VALUE")
    env_unit = os.environ.get("AGMINER_ENERGY_TARGET_UNIT")
    env_comparison = os.environ.get("AGMINER_ENERGY_TARGET_COMPARISON")

    if env_value is not None:
        value = Decimal(env_value)

    if env_unit is not None:
        unit = env_unit

    if env_comparison is not None:
        comparison = env_comparison.upper()

    if value <= 0:
        raise ValueError("Energy target must be positive")

    if unit not in UNIT_TO_J:
        raise ValueError("Unsupported energy unit: " + unit)

    if comparison not in VALID_COMPARISONS:
        raise ValueError("Energy comparison must be LT or LE")

    target_j = value * UNIT_TO_J[unit]
    target_j_text = format(target_j, "f")

    payload = {
        "target_j": target_j_text,
        "comparison": comparison,
        "ledger": ledger,
        "ledger_version": ledger_version,
    }

    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    policy_id = "ENERGY_" + hashlib.sha256(encoded).hexdigest()[:16]

    return {
        "value": value,
        "unit": unit,
        "comparison": comparison,
        "limit_j": float(target_j),
        "limit_j_text": target_j_text,
        "inclusive": comparison == "LE",
        "ledger": ledger,
        "ledger_version": ledger_version,
        "policy_id": policy_id,
    }
