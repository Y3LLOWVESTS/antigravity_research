"""Independent verification without importing DELTA1-02 producer.

Reconstructs the original R3B multipole mirror and independently tests
the universal metric trace identity using finite differences.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys

import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"src"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def independent_original_coarse():
    from antigravity_research.agminer.hook17_fdual_f_global_mirror_prefight import (
        reconstruct_a12c_field,
        fit_exterior_multipoles,
        evaluate_multipole_field,
    )
    from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
        HBAR_C_EV_M,
        REFERENCE_PORTAL_SCALE_EV,
        C_LIGHT_M_S,
    )

    h=.075
    field=reconstruct_a12c_field(h)
    fit=fit_exterior_multipoles(field,2.40,12)
    br,bz=evaluate_multipole_field(field,fit)

    # Independently write R3B mixed metric from the original E/B mirror.
    factor=HBAR_C_EV_M**2/REFERENCE_PORTAL_SCALE_EV**4
    p=factor*(br*field["b_rho"]+bz*field["b_z"])
    # Q_Y = F_Y^2, purely magnetic in the static R3B ansatz.
    q=factor*(
        field["b_rho"]**2+field["b_z"]**2
    )
    dpz,dpr=np.gradient(p,h,h,edge_order=2)
    minimum=float(np.min(-C_LIGHT_M_S**2*dpz[field["payload"]]))
    if minimum<=0:
        raise AssertionError("INDEPENDENT_R3B_SIGN_FAILURE")

    scale=9.80665/minimum
    dpz*=scale
    dpr*=scale
    dqz,dqr=np.gradient(q*scale,h,h,edge_order=2)

    mask=field["payload"]
    pvec=np.r_[dpz[mask],dpr[mask]]
    qvec=np.r_[dqz[mask],dqr[mask]]
    correlation=float(
        np.dot(pvec,qvec)
        / math.sqrt(float(pvec@pvec)*float(qvec@qvec))
    )
    independence=math.sqrt(max(0.,1-correlation**2))
    return {
        "coarse_normalization":scale,
        "coarse_invariant_gradient_cosine":correlation,
        "coarse_Q_independent_fraction":independence,
    }


def independent_trace_identity():
    # Verify nonlinear sigma(P) without calling producing symbolic code.
    P=.13
    T=-2.6
    Px,Pz=.9,-.4
    Tx,Tz=3.1,1.7

    def sig(p):
        return .08*p-.7*p*p+.16*p**3

    def sigp(p):
        return .08-1.4*p+.48*p*p

    def lam(p,t):
        return math.exp(4*sig(p))*t*sigp(p)

    h=1e-5
    lpx=(lam(P+h*Px,T+h*Tx)-lam(P-h*Px,T-h*Tx))/(2*h)
    lpz=(lam(P+h*Pz,T+h*Tz)-lam(P-h*Pz,T-h*Tz))/(2*h)

    observed=lpx*Pz-lpz*Px
    predicted=math.exp(4*sig(P))*sigp(P)*(Tx*Pz-Tz*Px)
    if abs(observed-predicted)>1e-7:
        raise AssertionError("INDEPENDENT_TRACE_WEDGE_FAIL")

    return {"trace_wedge_abs_error":abs(observed-predicted)}


def verify(path):
    p=Path(path).resolve()
    assert p.parent==ROOT/"results/data"
    assert re.fullmatch(r"delta1_02_\d{8}T\d{12}Z\.json",p.name)
    assert p.with_name(p.name+".sha256").read_text().strip()==sha(p)+"  "+p.name

    d=json.loads(p.read_text())
    assert d["branch"]=="DELTA1-02_R3B_PORTAL_PHYSICALIZATION_FORK"
    assert d["classification"]=="R3B_SCOPED_RECIPROCITY_AND_GEOMETRIC_RANK_AUDIT"
    assert d["original_R3B_prescribed_field_capacity_J"]==1.5429162116460216
    assert len(d["native_meshes"])==2
    assert d["DELTA1_03_authorized"] is False
    assert d["qualified_gravity_bridge_survivors"]==[]
    assert d["whole_craft_up"]=="NOT_DERIVED"
    assert d["complete_operating_energy_lt10MJ"]=="NOT_CERTIFIED"

    for rel,expected in d["producers"].items():
        assert sha(ROOT/rel)==expected
    for item in d["parents"].values():
        assert sha(ROOT/item["path"])==item["sha256"]

    ref=independent_original_coarse()
    old=d["native_meshes"][0]

    assert abs(
        ref["coarse_invariant_gradient_cosine"]
        -old["gradient_cosine_P_Q"]
    )<1e-9
    assert abs(
        ref["coarse_Q_independent_fraction"]
        -old["gradient_independent_fraction_Q"]
    )<1e-7

    ident=independent_trace_identity()
    print("DELTA1_02_INDEPENDENT_VERIFICATION=PASS")
    print("COARSE_Q_INDEPENDENT_FRACTION="+str(
        ref["coarse_Q_independent_fraction"]
    ))
    print("TRACE_WEDGE_ABS_ERROR="+str(
        ident["trace_wedge_abs_error"]
    ))
    print("SCIENTIFIC_SHA256="+sha(p))

    return {"rank":ref,"identity":ident}


def record(result,focused,full,independent_log):
    checked=verify(result)
    logs=[Path(x).resolve() for x in (focused,full,independent_log)]
    assert all(x.parent==ROOT/"results/logs" for x in logs)
    texts=[x.read_text() for x in logs]

    assert re.search(r"\b10 passed\b",texts[0])
    totals=re.findall(r"(?m)^\s*(\d+) passed(?:,|\s|$)",texts[1])
    assert totals and int(totals[-1])>=3304
    assert "DELTA1_02_INDEPENDENT_VERIFICATION=PASS" in texts[2]

    stamp=dt.datetime.now(dt.timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )
    path=ROOT/"results/data"/(
        "delta1_02_verification_"+stamp+".json"
    )
    doc={
        "branch":"DELTA1-02",
        "classification":"SCOPED_INDEPENDENT_R3B_RECIPROCITY_VERIFIED_NO_PROMOTION",
        "science_sha256":sha(result),
        "focused_passed":10,
        "full_regression_passed":int(totals[-1]),
        "independent_checks":checked,
        "logs":{
            str(x.relative_to(ROOT)):sha(x)
            for x in logs
        },
        "006D_replaced":False,
        "DELTA1_03_authorized":False,
        "whole_craft_up":"NOT_DERIVED",
        "complete_energy_lt10MJ":"NOT_CERTIFIED",
    }
    raw=(json.dumps(doc,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()
    with path.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    digest=hashlib.sha256(raw).hexdigest()
    with path.with_name(path.name+".sha256").open("x") as f:
        f.write(digest+"  "+path.name+"\n")
        f.flush()
        os.fsync(f.fileno())

    print("VERIFICATION_JSON="+str(path))
    print("VERIFICATION_SHA256="+digest)


if __name__=="__main__":
    if len(sys.argv)==2:
        verify(sys.argv[1])
    elif len(sys.argv)==6 and sys.argv[1]=="--record":
        record(*sys.argv[2:])
    else:
        raise SystemExit(
            "usage RESULT.json | --record RESULT focused full independent"
        )
