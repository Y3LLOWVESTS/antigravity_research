"""GAMMA1-C1 immutable analytic decision atlas: no PDE or new survivor."""
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

from antigravity_research.gamma1.gamma1_c1_decision_atlas import science, sha

SOURCES = (
    "src/antigravity_research/gamma1/gamma1_c1_decision_atlas.py",
    "simulations/gamma1/gamma1_c1_run.py",
    "tests/gamma1/test_gamma1_c1.py",
    "tests/gamma1/verify_gamma1_c1.py",
    "theory/gamma1/GAMMA1_C1_GRAVITY_BRIDGE_DECISION_LEDGER.md",
)


def main():
    stamp = dt.datetime.now(dt.timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )
    data = ROOT/"results/data"
    logs = ROOT/"results/logs"
    data.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)

    result = data/("gamma1_c1_"+stamp+".json")
    d = {
        "program":"ANTIGRAVITY_RESEARCH",
        "branch":"GAMMA1-C1_POSTR12_DECISION_ATLAS",
        "timestamp_utc":stamp,
        "classification":"FAILED_OR_INCOMPLETE",
        "producer_sources":{
            str(x):sha(ROOT/x) for x in SOURCES
        },
        "GAMMA1_01_authorized":False,
        "PH16_05_authorized":False,
        "PH17_authorized":False,
        "006D_replaced":False,
        "qualified_gravity_bridge_survivors":[],
        "complete_operating_energy_SI_lt10MJ":"NOT_CERTIFIED",
    }

    status = 2
    try:
        if "MISSING" in d["producer_sources"].values():
            raise RuntimeError("SCIENTIFIC_PRODUCER_MISSING")
        d.update(science(ROOT))
        status = 0
    except Exception as exc:
        d["classification"] = "FAILED_OR_INCOMPLETE"
        d["failure"] = repr(exc)
        d["traceback"] = traceback.format_exc()

    raw = (
        json.dumps(d, indent=2, sort_keys=True, allow_nan=False)
        + "\n"
    ).encode()
    with result.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())

    digest = hashlib.sha256(raw).hexdigest()
    with result.with_name(result.name+".sha256").open("x") as f:
        f.write(digest+"  "+result.name+"\n")
        f.flush()
        os.fsync(f.fileno())

    lines = [
        "RESULT_JSON="+str(result),
        "RESULT_SHA256="+digest,
        "CLASSIFICATION="+d["classification"],
        "M0_SOURCE_ONSHELL=NOT_DERIVED",
        "M1_LINEAR_GR_DEC_SCOPE=ENERGY_BOUND",
        "M2_MINIMAL_UNIVERSAL_SCALAR=LINEAR_ATTRACTION",
        "EARTH_DOWN_CRAFT_UP=NOT_DERIVED",
        "GAMMA1_01_AUTHORIZED=NO",
        "RETURN_CODE="+str(status),
    ]
    log = logs/(result.stem+".log")
    with log.open("x") as f:
        f.write("\n".join(lines)+"\n")
        f.flush()
        os.fsync(f.fileno())
    print("\n".join(lines), flush=True)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
