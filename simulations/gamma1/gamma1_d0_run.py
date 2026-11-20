"""Immutable GAMMA1 post-R12 D0 local action experiment."""
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

from antigravity_research.gamma1.gamma1_d0_m0_local_action_gate import (
    science, sha
)

SOURCES = (
    "src/antigravity_research/gamma1/gamma1_d0_m0_local_action_gate.py",
    "simulations/gamma1/gamma1_d0_run.py",
    "tests/gamma1/test_gamma1_d0.py",
    "tests/gamma1/verify_gamma1_d0.py",
    "theory/gamma1/GAMMA1_D0_M0_LOCAL_ACTION_LEDGER.md",
)


def main():
    stamp = dt.datetime.now(dt.timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )
    data = ROOT/"results/data"
    logs = ROOT/"results/logs"
    data.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)

    path = data/("gamma1_d0_"+stamp+".json")
    doc = {
        "branch": "GAMMA1-POSTR12-D0",
        "timestamp_utc": stamp,
        "classification": "EVIDENCE_FAILURE_NO_PROMOTION",
        "GAMMA1_01_authorized": False,
        "006D_replaced": False,
        "qualified_survivors": [],
        "producers": {
            rel: sha(ROOT/rel) for rel in SOURCES
        },
    }
    status = 2

    try:
        if "MISSING" in doc["producers"].values():
            raise RuntimeError("D0_PRODUCING_SOURCE_MISSING")
        doc.update(science(ROOT))
        status = 0
    except Exception as exc:
        doc["error"] = str(exc)
        doc["traceback"] = traceback.format_exc()
        doc["classification"] = "EVIDENCE_FAILURE_NO_PROMOTION"

    raw = (
        json.dumps(
            doc, indent=2, sort_keys=True, allow_nan=False
        ) + "\n"
    ).encode()

    with path.open("xb") as output:
        output.write(raw)
        output.flush()
        os.fsync(output.fileno())

    digest = hashlib.sha256(raw).hexdigest()
    sidecar = path.with_name(path.name+".sha256")
    with sidecar.open("x") as output:
        output.write(digest+"  "+path.name+"\n")
        output.flush()
        os.fsync(output.fileno())

    lines = [
        "RESULT_JSON="+str(path),
        "RESULT_SHA256="+digest,
        "CLASSIFICATION="+doc["classification"],
        "PH16_STATIONARY_PARENT_MATCH=NOT_DERIVED",
        "EARTH_DOWN_CRAFT_UP=NOT_DERIVED",
        "LT10MJ=NOT_CERTIFIED",
        "GAMMA1_01_AUTHORIZED=NO",
        "RETURN_CODE="+str(status),
    ]
    with (logs/(path.stem+".log")).open("x") as output:
        output.write("\n".join(lines)+"\n")
        output.flush()
        os.fsync(output.fileno())

    print("\n".join(lines), flush=True)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
