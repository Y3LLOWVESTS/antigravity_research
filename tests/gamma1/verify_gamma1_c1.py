"""Independent C1 theorem and immutable record verification.

The independent verifier deliberately never imports the C1 producer.
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

ROOT = Path(__file__).resolve().parents[2]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def independent_theorems():
    # Independently derive the ordinary-GR DEC bound.
    G = 6.67430e-11
    lightspeed = 299792458
    accel = 9.80665
    distance = 1.0
    E_min = (
        accel*distance*distance/G
        *lightspeed*lightspeed/4
    )
    a_cap = 4*G*1e7/(lightspeed*lightspeed*distance*distance)
    assert 3e27 < E_min < 4e27
    assert a_cap < 3e-20

    # Independent M2 finite-difference derivative of Yukawa potential.
    strength = .2**2/(4*math.pi)
    mu = .35
    radius = 1.3

    def potential(r):
        return -strength*math.exp(-mu*r)/r

    dx = 1e-5
    radial_force = -(
        potential(radius+dx)-potential(radius-dx)
    )/(2*dx)
    assert radial_force < 0

    # Independent exterior electrostatic Y-source test,
    # with DIFFERENT manufactured lambda and spatial point.
    x,y,z = 1.4,.55,1.1
    R2 = x*x+y*y+z*z
    invr3 = R2**(-1.5)
    invr5 = R2**(-2.5)
    gp = [
        -3*z*x*invr5,
        -3*z*y*invr5,
        invr3-3*z*z*invr5,
    ]
    gl = [y,x,0.]
    j = [
        gl[1]*gp[2]-gl[2]*gp[1],
        gl[2]*gp[0]-gl[0]*gp[2],
        gl[0]*gp[1]-gl[1]*gp[0],
    ]

    def phi(xx,yy,zz):
        return zz/(xx*xx+yy*yy+zz*zz)**1.5

    def lam(xx,yy,zz):
        return xx*yy

    h = 1e-4
    q = (x,y,z)
    gf = []
    lf = []
    for axis in range(3):
        qp = list(q)
        qm = list(q)
        qp[axis] += h
        qm[axis] -= h
        gf.append((phi(*qp)-phi(*qm))/(2*h))
        lf.append((lam(*qp)-lam(*qm))/(2*h))

    jf = [
        lf[1]*gf[2]-lf[2]*gf[1],
        lf[2]*gf[0]-lf[0]*gf[2],
        lf[0]*gf[1]-lf[1]*gf[0],
    ]
    yerr = max(abs(u-v) for u,v in zip(j,jf))
    assert yerr < 1e-7
    assert max(abs(v) for v in j) > 1e-3

    return {
        "independent_GR_min_source_energy_J":E_min,
        "independent_GR_max_accel_10MJ":a_cap,
        "independent_M2_yukawa_radial_force":radial_force,
        "independent_M0_manufactured_Y_error":yerr,
    }


def verify(path):
    p = Path(path).resolve()
    assert p.parent == ROOT/"results/data"
    assert re.fullmatch(
        r"gamma1_c1_\d{8}T\d{12}Z\.json",p.name
    )
    assert p.with_name(p.name+".sha256").read_text().strip() == (
        sha(p)+"  "+p.name
    )
    d = json.loads(p.read_text())
    assert d["classification"] == "SCOPED_IMPOSSIBILITY_CERTIFICATE"
    assert d["program"] == "ANTIGRAVITY_RESEARCH"
    assert d["branch"] == "GAMMA1-C1_POSTR12_DECISION_ATLAS"

    assert len(d["hypothesis_matrix"]) == 4
    assert [m["family"] for m in d["hypothesis_matrix"]] == [
        "M0","M1","M2","M3"
    ]
    assert all(
        m["qualified_survivor"] is False
        for m in d["hypothesis_matrix"]
    )
    assert all(v is True for v in d["negative_controls"].values())
    assert d["gates"]["D0_Y_EULER_ERRATUM"] == (
        "DERIVED_DIFFERENTIAL_NECESSARY_CONDITION"
    )
    assert d["gates"]["M0_REAL_ONSHELL_SOURCE"] == "NOT_DERIVED"
    assert d["gates"]["M0_PH16_NATIVE_CONTINUUM_MATCH"] == "NOT_DERIVED"
    assert d["gates"]["FULL_LORENTZIAN_CONSTRAINT_HEALTH"] == "NOT_CERTIFIED"
    assert d["gates"]["SI_EP_UV"] == "NOT_CERTIFIED"

    assert d["qualified_gravity_bridge_survivors"] == []
    assert d["M0_conditional_neutral_geometry"]["prescribed_metric_profile_only"] is True
    assert d["SI_portal_scaling_warning"]["physical_SI_normalization"] == "NOT_SPECIFIED"
    assert d["M1_GR_DEC_energy"]["operating_energy_inference"].startswith("NOT_DIRECT")
    assert d["M2_canonical_scalar_exchange"]["wrong_sign_kinetic_repulsion"] == "GHOST_DISALLOWED"

    for key in (
        "GAMMA1_01_authorized",
        "PH16_05_authorized",
        "PH17_authorized",
        "006D_replaced",
    ):
        assert d[key] is False
    assert d["whole_craft_up"] == "NOT_DERIVED"
    assert d["complete_operating_energy_SI_lt10MJ"] == "NOT_CERTIFIED"
    assert d["research_maturity_heuristic_after_percent"] == 34

    for rel,expected in d["producer_sources"].items():
        assert sha(ROOT/rel) == expected
    for item in d["parents"].values():
        assert sha(ROOT/item["path"]) == item["sha256"]

    t = independent_theorems()
    e = d["M1_GR_DEC_energy"]["min_source_gravitating_energy_J"]
    assert abs(e-t["independent_GR_min_source_energy_J"])/e < 1e-14
    af = d["M1_GR_DEC_energy"]["max_accel_if_source_gravitating_energy_lt_10MJ_m_s2"]
    assert abs(af-t["independent_GR_max_accel_10MJ"])/af < 1e-14

    print("C1_INDEPENDENT_VERIFICATION=PASS")
    print("INDEPENDENT_M0_Y_SOURCE_ERROR="+str(
        t["independent_M0_manufactured_Y_error"]
    ))
    print("INDEPENDENT_M1_GR_MIN_ENERGY_J="+str(e))
    print("SCIENTIFIC_JSON_SHA256="+sha(p))
    return t


def record(result,focused,full,independent):
    t = verify(result)
    logs = [
        Path(x).resolve()
        for x in (focused,full,independent)
    ]
    assert all(x.parent == ROOT/"results/logs" for x in logs)
    lines = [p.read_text() for p in logs]
    assert re.search(r"\b14 passed\b",lines[0])

    counts = re.findall(
        r"(?m)^\s*(\d+) passed(?:,|\s|$)",lines[1]
    )
    assert counts and int(counts[-1]) >= 3255
    assert "C1_INDEPENDENT_VERIFICATION=PASS" in lines[2]

    stamp = dt.datetime.now(dt.timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )
    p = ROOT/"results/data"/(
        "gamma1_c1_verification_"+stamp+".json"
    )

    document = {
        "program":"ANTIGRAVITY_RESEARCH",
        "branch":"GAMMA1-C1_POSTR12_DECISION_ATLAS",
        "classification":
            "SCOPED_INDEPENDENT_VERIFIED_NO_PHYSICAL_PROMOTION",
        "scientific_result_sha256":sha(result),
        "focused_passed":14,
        "full_regression_passed":int(counts[-1]),
        "independent_theorems":t,
        "logs":{
            str(x.relative_to(ROOT)):sha(x)
            for x in logs
        },
        "GAMMA1_01_authorized":False,
        "006D_replaced":False,
        "whole_craft_up":"NOT_DERIVED",
        "complete_energy_SI":"NOT_CERTIFIED",
    }

    raw = (
        json.dumps(
            document,sort_keys=True,indent=2,allow_nan=False
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
    print("VERIFICATION_JSON="+str(p))
    print("VERIFICATION_SHA256="+digest)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        verify(sys.argv[1])
    elif len(sys.argv) == 6 and sys.argv[1] == "--record":
        record(*sys.argv[2:])
    else:
        raise SystemExit(
            "usage: RESULT.json | "
            "--record RESULT.json focused.log full.log independent.log"
        )
