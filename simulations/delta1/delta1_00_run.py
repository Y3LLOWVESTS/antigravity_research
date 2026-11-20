"""Immutable DELTA1-00 action-first operator/source-energy audit."""
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
from antigravity_research.delta1.delta1_00_scalar_energy_gate import science, digest
SOURCES = (
    "src/antigravity_research/delta1/delta1_00_scalar_energy_gate.py",
    "simulations/delta1/delta1_00_run.py",
    "tests/delta1/test_delta1_00.py",
    "tests/delta1/verify_delta1_00.py",
    "theory/delta1/DELTA1_00_ACTION_FIRST_SCALAR_TRANSDUCER_LEDGER.md",
)


def main():
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    data, logs = ROOT/"results/data", ROOT/"results/logs"
    data.mkdir(parents=True,exist_ok=True)
    logs.mkdir(parents=True,exist_ok=True)
    output = data/("delta1_00_"+stamp+".json")
    doc = {
        "branch":"DELTA1-00_ACTION_FIRST_SCALAR_GATE",
        "timestamp_utc":stamp,
        "classification":"FAILED_OR_UNDETERMINED_NO_PROMOTION",
        "producers":{s:digest(ROOT/s) for s in SOURCES},
        "006D_replaced":False,
        "GAMMA1_01_authorized":False,
        "qualified_gravity_bridge_survivors":[],
    }
    code=2
    try:
        if "MISSING" in doc["producers"].values():
            raise RuntimeError("MISSING_PRODUCER")
        doc.update(science(ROOT))
        code=0
    except Exception as exc:
        doc["error"]=repr(exc)
        doc["traceback"]=traceback.format_exc()
    raw=(json.dumps(doc,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()
    with output.open("xb") as f:
        f.write(raw);f.flush();os.fsync(f.fileno())
    digest_hex=hashlib.sha256(raw).hexdigest()
    with output.with_name(output.name+".sha256").open("x") as f:
        f.write(digest_hex+"  "+output.name+"\n");f.flush();os.fsync(f.fileno())
    lines = [
        "RESULT_JSON="+str(output),
        "RESULT_SHA256="+digest_hex,
        "CLASSIFICATION="+doc["classification"],
        "FULL_EARTH_CRAFT_FORCE=NOT_DERIVED",
        "COMPLETE_LT10MJ=NOT_CERTIFIED",
        "GAMMA1_01_AUTHORIZED=NO",
        "RETURN_CODE="+str(code),
    ]
    logfile=logs/(output.stem+".log")
    with logfile.open("x") as f:
        f.write("\n".join(lines)+"\n");f.flush();os.fsync(f.fileno())
    print("\n".join(lines),flush=True)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
