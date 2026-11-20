"""Immutable GAMMA1-N1 native-field/topological-Ward decision runner."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/"src"))

from antigravity_research.gamma1.gamma1_n1_native_ward import (
    science, sha
)

SOURCES = (
    "src/antigravity_research/gamma1/gamma1_n1_native_ward.py",
    "simulations/gamma1/gamma1_n1_run.py",
    "tests/gamma1/test_gamma1_n1.py",
    "tests/gamma1/verify_gamma1_n1.py",
    "theory/gamma1/GAMMA1_N1_NATIVE_TOPOLOGICAL_WARD_LEDGER.md",
)


def main():
    stamp = dt.datetime.now(dt.timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )
    data = ROOT/"results/data"
    logs = ROOT/"results/logs"
    data.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)

    path = data/("gamma1_n1_"+stamp+".json")
    doc = {
        "branch": "GAMMA1-N1_NATIVE_WARD_INDUCTION",
        "utc": stamp,
        "classification": "EVIDENCE_FAILED_NO_PROMOTION",
        "producer_sources": {
            rel: sha(ROOT/rel) for rel in SOURCES
        },
        "GAMMA1_01_authorized": False,
        "PH16_05_authorized": False,
        "PH17_authorized": False,
        "006D_replaced": False,
        "qualified_gravity_bridge_survivors": [],
    }

    status = 2
    try:
        if "MISSING" in doc["producer_sources"].values():
            raise RuntimeError("MISSING_PRODUCING_SOURCE")
        doc.update(science(ROOT))
        status = 0
    except Exception as exc:
        doc["error"] = repr(exc)
        doc["traceback"] = traceback.format_exc()

    raw = (
        json.dumps(doc, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode()

    with path.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())

    digest = hashlib.sha256(raw).hexdigest()
    with path.with_name(path.name+".sha256").open("x") as f:
        f.write(digest+"  "+path.name+"\n")
        f.flush()
        os.fsync(f.fileno())

    lines = [
        "RESULT_JSON="+str(path),
        "RESULT_SHA256="+digest,
        "CLASSIFICATION="+doc["classification"],
        "NATIVE_INTEGRABILITY_DECISION="+doc.get(
            "native_integrability_decision", "INCONCLUSIVE"
        ),
        "NATIVE_CONTINUUM=NOT_CERTIFIED",
        "EARTH_DOWN_CRAFT_UP=NOT_DERIVED",
        "GAMMA1_01_AUTHORIZED=NO",
        "RETURN_CODE="+str(status),
    ]

    with (logs/(path.stem+".log")).open("x") as f:
        f.write("\n".join(lines)+"\n")
        f.flush()
        os.fsync(f.fileno())

    print("\n".join(lines), flush=True)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
