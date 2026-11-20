"""Immutable DELTA1-02 R3B action-reciprocity and geometric-rank runner."""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"src"))

from antigravity_research.delta1.delta1_02_r3b_portal_rank import science,sha

SOURCES=(
    "src/antigravity_research/delta1/delta1_02_r3b_portal_rank.py",
    "simulations/delta1/delta1_02_run.py",
    "tests/delta1/test_delta1_02.py",
    "tests/delta1/verify_delta1_02.py",
    "theory/delta1/DELTA1_02_R3B_PORTAL_RECIPROCITY_LEDGER.md",
)


def main():
    stamp=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    (ROOT/"results/data").mkdir(parents=True,exist_ok=True)
    (ROOT/"results/logs").mkdir(parents=True,exist_ok=True)
    path=ROOT/"results/data"/("delta1_02_"+stamp+".json")

    doc={
        "branch":"DELTA1-02_R3B_PORTAL_PHYSICALIZATION_FORK",
        "timestamp_utc":stamp,
        "classification":"FAILED_OR_INCOMPLETE_NO_PROMOTION",
        "producers":{x:sha(ROOT/x) for x in SOURCES},
        "006D_replaced":False,
        "DELTA1_03_authorized":False,
        "qualified_gravity_bridge_survivors":[],
    }

    status=2
    try:
        if "MISSING" in doc["producers"].values():
            raise RuntimeError("MISSING_SCIENTIFIC_SOURCE")
        doc.update(science(ROOT))
        status=0
    except Exception as exc:
        doc["error"]=repr(exc)
        doc["traceback"]=traceback.format_exc()

    raw=(json.dumps(doc,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()
    with path.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())

    digest=hashlib.sha256(raw).hexdigest()
    with path.with_name(path.name+".sha256").open("x") as f:
        f.write(digest+"  "+path.name+"\n")
        f.flush()
        os.fsync(f.fileno())

    lines=[
        "RESULT_JSON="+str(path),
        "RESULT_SHA256="+digest,
        "CLASSIFICATION="+doc["classification"],
        "R3B_CAPACITY_J="+str(doc.get(
            "original_R3B_prescribed_field_capacity_J","NOT_VALIDATED"
        )),
        "RANK_DECISION="+doc.get(
            "one_extra_even_invariant_rank_decision","INCONCLUSIVE"
        ),
        "DELTA1_03_AUTHORIZED=NO",
        "RETURN_CODE="+str(status),
    ]
    log=ROOT/"results/logs"/(path.stem+".log")
    with log.open("x") as f:
        f.write("\n".join(lines)+"\n")
        f.flush()
        os.fsync(f.fileno())

    print("\n".join(lines),flush=True)
    return status


if __name__=="__main__":
    raise SystemExit(main())
