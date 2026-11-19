"""R12 L0 immutable theorem runner: no expensive PDE or gravity claim."""
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
from antigravity_research.gamma1.gamma1_00r12_offshell_fork import science, sha

SOURCES = (
    "src/antigravity_research/gamma1/gamma1_00r12_offshell_fork.py",
    "simulations/gamma1/gamma1_00r12_run.py",
    "tests/gamma1/test_gamma1_00r12.py",
    "tests/gamma1/verify_gamma1_00r12.py",
    "theory/gamma1/GAMMA1_00R12_OFFSHELL_COVARIANT_ACTION_LEDGER.md",
)


def main():
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    stem = "gamma1_00r12_"+timestamp
    data = ROOT/"results/data"
    logs = ROOT/"results/logs"
    data.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    path = data/(stem+".json")
    log = logs/(stem+".log")
    doc = {
        "branch": "GAMMA1-00R12",
        "timestamp_utc": timestamp,
        "classification": "R12_EVIDENCE_FAILURE_NO_PROMOTION",
        "GAMMA1_01_authorized": False,
        "PH16_05_authorized": False,
        "PH17_authorized": False,
        "006D_replaced": False,
        "qualified_gravity_bridge_survivors": [],
        "producing_sources": {rel: sha(ROOT/rel) for rel in SOURCES},
    }
    status = 2
    try:
        if "MISSING" in doc["producing_sources"].values():
            raise RuntimeError("R12_PRODUCER_MISSING")
        doc.update(science(ROOT))
        status = 0
    except Exception as exc:
        doc["classification"] = "R12_EVIDENCE_FAILURE_NO_PROMOTION"
        doc["error"] = str(exc)
        doc["traceback"] = traceback.format_exc()
    raw = (json.dumps(doc, sort_keys=True, indent=2, allow_nan=False)+"\n").encode()
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    digest = hashlib.sha256(raw).hexdigest()
    with path.with_name(path.name+".sha256").open("x") as stream:
        stream.write(digest+"  "+path.name+"\n")
        stream.flush()
        os.fsync(stream.fileno())
    lines = ["RESULT_JSON="+str(path), "RESULT_SHA256="+digest,
             "CLASSIFICATION="+doc["classification"],
             "WHOLE_CRAFT_UP=NOT_DERIVED", "FULL_LORENTZIAN_HEALTH=NOT_CERTIFIED",
             "COMPLETE_ENERGY_LT10MJ=NOT_CERTIFIED", "GAMMA1_01_AUTHORIZED=NO",
             "RETURN_CODE="+str(status)]
    with log.open("x") as stream:
        stream.write("\n".join(lines)+"\n")
        stream.flush()
        os.fsync(stream.fileno())
    print("\n".join(lines), flush=True)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
