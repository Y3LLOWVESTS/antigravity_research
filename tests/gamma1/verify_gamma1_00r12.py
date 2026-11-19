"""Independent R12 verifier: second metric experiment and evidence checks.

No import of R12 producer. The original R11 independent verifier must also
pass separately. A PASS here proves only scoped L0 consistency, not lift.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def independent_metric_fd():
    """Diagonal-metric variation with unrelated fields and scalar gradient."""
    g = np.diag([-1.7, 1.1, 1.2, .8])
    dg = np.diag([.03, -.02, .04, -.01])
    grad = np.array([.1, .2, -.15, .05])
    h, F01, G23 = 1e-5, .04, -.06

    def core(metric):
        p = F01*G23/np.sqrt(-np.linalg.det(metric))
        sig = .05*p - 40*p*p
        gt = np.exp(2*sig)*metric
        inv = np.linalg.inv(gt)
        return -np.sqrt(-np.linalg.det(gt))*(.5*grad@inv@grad+.5*.6**2)

    p = F01*G23/np.sqrt(-np.linalg.det(g))
    sig = .05*p - 40*p*p
    gt = np.exp(2*sig)*g
    inv = np.linalg.inv(gt)
    L = .5*grad@inv@grad+.5*.6**2
    Tt = np.outer(inv@grad, inv@grad)-inv*L
    trace = np.sum(gt*Tt)
    Tg = (np.exp(6*sig)*Tt
          -np.exp(4*sig)*(.05-80*p)*p*trace*np.linalg.inv(g))
    exact = .5*np.sqrt(-np.linalg.det(g))*np.sum(Tg*dg)
    finite = (core(g+h*dg)-core(g-h*dg))/(2*h)
    error = float(abs(exact-finite))
    if error>=1e-8:
        raise AssertionError("INDEPENDENT_METRIC_FD_FAIL: "+str(error))
    return error


def verify(result):
    p = Path(result).resolve()
    if p.parent != ROOT/"results/data" or not re.fullmatch(
        r"gamma1_00r12_\d{8}T\d{12}Z\.json", p.name
    ):
        raise AssertionError("INVALID_SCIENTIFIC_PATH")
    if p.with_name(p.name+".sha256").read_text().strip() != sha(p)+"  "+p.name:
        raise AssertionError("R12_SIDECAR_SHA_DRIFT")
    d = json.loads(p.read_text())
    assert d["classification"]=="INSUFFICIENT_UNIQUE_COVARIANT_ACTION"
    assert d["branch"]=="GAMMA1-00R12"
    assert d["gates"]["METRIC_HODGE_DERIVED"]=="PASS_SCOPED"
    assert d["gates"]["FULL_WARD_NOETHER_BIANCHI"]=="NOT_DERIVED"
    assert d["gates"]["HEALTHY_CONSTRAINED_LORENTZIAN"]=="NOT_CERTIFIED"
    assert d["whole_craft_up"]=="NOT_DERIVED"
    assert d["complete_energy"]=="ENERGY_UNDETERMINED"
    assert d["qualified_gravity_bridge_survivors"]==[]
    for key in ("GAMMA1_01_authorized","PH16_05_authorized",
                "PH17_authorized","006D_replaced"):
        assert d[key] is False
    assert d["scalar_U1_offshell_jet"] is True
    assert d["r11_fixed_N"]["rank"]==2
    assert max(d["hodge_metric_errors"].values())<1e-8
    assert len(d["negative_controls"])==5
    assert all(v is True for v in d["negative_controls"].values())
    for rel, digest in d["producing_sources"].items():
        assert sha(ROOT/rel)==digest
    for item in d["parents"].values():
        assert sha(ROOT/item["path"])==item["sha256"]
    error = independent_metric_fd()
    print("R12_INDEPENDENT_VERIFICATION=PASS")
    print("INDEPENDENT_METRIC_FD_MAX_ABS="+str(error))
    print("SCIENTIFIC_JSON_SHA256="+sha(p))
    return error


def record(result, focused, full, independent, r11_log):
    error = verify(result)
    logs = [Path(x).resolve() for x in (focused, full, independent, r11_log)]
    assert all(x.parent==ROOT/"results/logs" for x in logs)
    texts = [x.read_text() for x in logs]
    assert re.search(r"\b8 passed\b", texts[0])
    counts = re.findall(r"(?m)^\s*(\d+) passed(?:,|\s|$)", texts[1])
    assert counts and int(counts[-1])>=3233
    assert "R12_INDEPENDENT_VERIFICATION=PASS" in texts[2]
    assert "R11_INDEPENDENT_VERIFICATION=PASS" in texts[3] or (
        "R11" in texts[3] and "PASS" in texts[3]
    ), "Expected original R11 independent verifier PASS output"
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    p = ROOT/"results/data"/("gamma1_00r12_verification_"+stamp+".json")
    doc = {
        "branch": "GAMMA1-00R12",
        "classification": "SCOPED_L0_VERIFIED_NO_PHYSICAL_PROMOTION",
        "scientific_result_sha256": sha(result),
        "focused_tests_passed": 8,
        "full_regression_passed": int(counts[-1]),
        "independent_metric_fd_error": error,
        "logs": {str(x.relative_to(ROOT)): sha(x) for x in logs},
        "GAMMA1_01_authorized": False,
        "PH16_05_authorized": False,
        "PH17_authorized": False,
        "006D_replaced": False,
        "whole_craft_up": "NOT_DERIVED",
        "complete_energy_lt10MJ": "NOT_CERTIFIED",
    }
    raw = (json.dumps(doc, indent=2, sort_keys=True, allow_nan=False)+"\n").encode()
    with p.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    with p.with_name(p.name+".sha256").open("x") as stream:
        stream.write(hashlib.sha256(raw).hexdigest()+"  "+p.name+"\n")
        stream.flush()
        os.fsync(stream.fileno())
    print("VERIFICATION_JSON="+str(p))
    print("VERIFICATION_SHA256="+sha(p))


if __name__ == "__main__":
    if len(sys.argv)==2:
        verify(sys.argv[1])
    elif len(sys.argv)==7 and sys.argv[1]=="--record":
        record(*sys.argv[2:])
    else:
        raise SystemExit("usage: RESULT.json | --record RESULT.json focused.log full.log independent.log r11.log")
