"""DELTA1-01 immutable exact nonlinear source-and-energy experiment.

Falsifies a low-energy claim within a specified flat, spherical,
massless-scalar, fixed-charge and zero-bare-source-matter sector.
It does not test all modified-gravity theories.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"src"))

from antigravity_research.delta1.delta1_01_exact_shell import science,sha

FILES = (
    "src/antigravity_research/delta1/delta1_01_exact_shell.py",
    "simulations/delta1/delta1_01_run.py",
    "tests/delta1/test_delta1_01.py",
    "tests/delta1/verify_delta1_01.py",
    "theory/delta1/DELTA1_01_NONLINEAR_SHELL_ENERGY_LEDGER.md",
)


def main():
    stamp = dt.datetime.now(
        dt.timezone.utc
    ).strftime("%Y%m%dT%H%M%S%fZ")

    (ROOT/"results/data").mkdir(parents=True,exist_ok=True)
    (ROOT/"results/logs").mkdir(parents=True,exist_ok=True)

    p = ROOT/"results/data"/(
        "delta1_01_"+stamp+".json"
    )

    d = {
        "branch":"DELTA1-01_EXACT_NONLINEAR_SHELL",
        "timestamp_utc":stamp,
        "classification":"EVIDENCE_FAILED_NO_PROMOTION",
        "producers":{
            x:sha(ROOT/x) for x in FILES
        },
        "006D_replaced":False,
        "DELTA1_02_authorized":False,
        "qualified_gravity_bridge_survivors":[],
    }

    status = 2
    try:
        if "MISSING" in d["producers"].values():
            raise RuntimeError("MISSING_PRODUCING_FILE")
        d.update(science(ROOT))
        status = 0
    except Exception as exc:
        d["failure"] = repr(exc)
        d["traceback"] = traceback.format_exc()

    raw = (
        json.dumps(
            d,sort_keys=True,indent=2,allow_nan=False
        )+"\n"
    ).encode()

    with p.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())

    digest = hashlib.sha256(raw).hexdigest()
    with p.with_name(p.name+".sha256").open("x") as f:
        f.write(digest+"  "+p.name+"\n")
        f.flush()
        os.fsync(f.fileno())

    lines = [
        "RESULT_JSON="+str(p),
        "RESULT_SHA256="+digest,
        "CLASSIFICATION="+d["classification"],
        "ALPHA_CRIT_EXTERIOR_ONLY="+str(
            d.get(
                "strict_10MJ_exterior_only_alpha_threshold",
                "UNDEFINED",
            )
        ),
        "EARTH_DOWN_CRAFT_UP=NOT_DERIVED",
        "FULL_DEVICE_LT10MJ=NOT_CERTIFIED",
        "RETURN_CODE="+str(status),
    ]

    with (ROOT/"results/logs"/(p.stem+".log")).open("x") as f:
        f.write("\n".join(lines)+"\n")
        f.flush()
        os.fsync(f.fileno())

    print("\n".join(lines),flush=True)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
