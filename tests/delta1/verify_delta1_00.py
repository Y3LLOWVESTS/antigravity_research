"""Independent result verifier for DELTA1-00; never imports producer."""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def independent():
    # Independent normalization: define psi=alpha*varphi; the kinetic
    # energy density for psi is c^4 |grad psi|^2/(8 pi G alpha^2).
    gravity=9.80665
    newton=6.67430e-11
    allowed_gamma=0.0001
    beta2=allowed_gamma/(2-allowed_gamma)
    rho=8000.0
    V=1.0/rho
    independent_E=V*(gravity**2)/(8*math.pi*newton*beta2)
    independent_alpha=math.sqrt(beta2)
    # Contradiction at any coupling this small: energy alone > ceiling.
    assert independent_E>1e11
    # Full exterior monopole check: integrate r^-4 energy exactly.
    R=1.0
    outside=gravity**2*R**3/(2*newton*beta2)
    assert outside>1e15
    return {"alpha_illustrative":independent_alpha,
            "dense_target_gradient_energy_J":independent_E,
            "spherical_exterior_energy_J":outside,
            "PPN_tolerance_NOT_experimental_CI":allowed_gamma}


def verify(result):
    p=Path(result).resolve()
    assert p.parent==ROOT/"results/data"
    assert re.fullmatch(r"delta1_00_\d{8}T\d{12}Z\.json",p.name)
    assert p.with_name(p.name+".sha256").read_text().strip()==sha(p)+"  "+p.name
    d=json.loads(p.read_text())
    assert d["branch"]=="DELTA1-00_ACTION_FIRST_SCALAR_GATE"
    assert d["classification"]=="SCOPED_RED_LONG_RANGE_UNSCREENED_SCALAR_F2"
    assert d["candidate_nonminimal_coupling_count"]==1
    assert d["short_range_screened_branch"].startswith("OPEN_UNTESTED")
    assert d["gates"]["FULL_LORENTZIAN_CONSTRAINED_HEALTH"]=="NOT_CERTIFIED"
    assert d["gates"]["EARTH_DOWN_WHOLE_CRAFT_UP"]=="NOT_DERIVED_REAL_SOURCE"
    assert all(d["negative_controls"].values())
    for key in ("006D_replaced","GAMMA1_01_authorized","PH16_05_authorized","PH17_authorized"):
        assert d[key] is False
    assert d["qualified_gravity_bridge_survivors"]==[]
    for rel,h in d["producers"].items():assert sha(ROOT/rel)==h
    for item in d["parent_sha_lock"].values():assert sha(ROOT/item["path"])==item["sha256"]
    independent_result=independent()
    sample=[x for x in d["target_energy"] if x["density_kg_m3_ASSUMED"]==8000.0][0]
    err=abs(sample["scalar_field_energy_in_target_J_LOWER_BOUND"]-independent_result["dense_target_gradient_energy_J"])
    assert err/independent_result["dense_target_gradient_energy_J"]<1e-14
    print("DELTA1_00_INDEPENDENT_VERIFICATION=PASS")
    print("DENSE_TARGET_FIELD_FLOOR_J="+str(independent_result["dense_target_gradient_energy_J"]))
    print("SCIENTIFIC_SHA256="+sha(p))
    return independent_result


def record(result,focused,full,independent_log):
    v=verify(result)
    logs=[Path(x).resolve() for x in (focused,full,independent_log)]
    assert all(x.parent==ROOT/"results/logs" for x in logs)
    txt=[p.read_text() for p in logs]
    assert re.search(r"\b14 passed\b",txt[0])
    counts=re.findall(r"(?m)^\s*(\d+) passed(?:,|\s|$)",txt[1])
    assert counts and int(counts[-1])>=3280
    assert "DELTA1_00_INDEPENDENT_VERIFICATION=PASS" in txt[2]
    stamp=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    path=ROOT/"results/data"/("delta1_00_verification_"+stamp+".json")
    doc={"branch":"DELTA1-00_ACTION_FIRST_SCALAR_GATE",
         "classification":"SCOPED_INDEPENDENT_RED_NO_PHYSICAL_PROMOTION",
         "scientific_sha256":sha(result),"focused_passed":14,
         "full_regression_passed":int(counts[-1]),
         "independent_analytic_checks":v,
         "logs":{str(x.relative_to(ROOT)):sha(x) for x in logs},
         "whole_craft_up":"NOT_DERIVED","006D_replaced":False,
         "GAMMA1_01_authorized":False,"complete_energy_lt10MJ":"NOT_CERTIFIED"}
    raw=(json.dumps(doc,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()
    with path.open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
    h=hashlib.sha256(raw).hexdigest()
    with path.with_name(path.name+".sha256").open("x") as f:
        f.write(h+"  "+path.name+"\n");f.flush();os.fsync(f.fileno())
    print("VERIFICATION_JSON="+str(path))
    print("VERIFICATION_SHA256="+h)

if __name__=="__main__":
    if len(sys.argv)==2:verify(sys.argv[1])
    elif len(sys.argv)==6 and sys.argv[1]=="--record":record(*sys.argv[2:])
    else:raise SystemExit("usage RESULT.json | --record RESULT focused full independent")
