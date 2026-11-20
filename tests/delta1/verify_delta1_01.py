"""Independent DELTA1-01 verifier: numerical nonlinear BVP and energy.

Does not import the scientific producer. Re-solves the nonlinear
boundary-value equation and separately integrates the two energies.
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
from scipy.integrate import quad,solve_bvp

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def independent(result):
    z = result["exact_radial_nonperturbative_solution"]
    t = float(z["t"])
    R = .5
    C = 299792458.
    G = 6.67430e-11
    eps0 = 8.8541878128e-12

    eta = z["eta"]
    Q = z["Q_C_conventional_X_normalization"]
    alpha = z["alpha"]

    coeff = 2*t*t/math.cos(t)**2
    s = np.linspace(0,1,70)
    yedge = -2*math.log(math.cos(t))

    guess = np.vstack([
        yedge*s*(2-s),
        2*yedge*(1-s),
    ])

    ans = solve_bvp(
        lambda s,y: np.vstack((
            y[1],
            -coeff*np.exp(-y[0]),
        )),
        lambda ya,yb: np.array([
            ya[0],yb[1]
        ]),
        s,guess,
        tol=1e-8,
        max_nodes=16000,
    )

    if ans.status != 0:
        raise AssertionError(
            "INDEPENDENT_BVP_NONCONVERGED"
        )

    electric = Q**2/(8*math.pi*eps0*R)*quad(
        lambda x: math.exp(
            -float(ans.sol(x)[0])
        ),
        0,1,epsrel=1e-10
    )[0]

    scalar = C**4*R/(2*G*eta**2)*quad(
        lambda x: float(
            ans.sol(x)[1]
        )**2,
        0,1,epsrel=1e-10
    )[0]

    radii = np.linspace(1.5,1.7,201)
    accel = np.array([
        alpha*C*C*R/(eta*r*r)
        *float(ans.sol(R/r)[1])
        for r in radii
    ])

    errE = max(
        abs(electric-z["E_X_exterior_J"])
            /z["E_X_exterior_J"],
        abs(scalar-z["E_scalar_exterior_J"])
            /z["E_scalar_exterior_J"],
    )

    if (
        errE > 2e-7
        or accel.min() < 9.80665*(1-2e-7)
    ):
        raise AssertionError(
            "INDEPENDENT_BVP_ENERGY_FORCE_FAIL"
        )

    crit = math.sqrt(
        (electric+scalar)/1e7
    )

    if abs(
        crit
        -result["strict_10MJ_exterior_only_alpha_threshold"]
    ) > 1e-4:
        raise AssertionError(
            "INDEPENDENT_CRITICAL_ALPHA_MISMATCH"
        )

    return {
        "solver_status": int(ans.status),
        "solver_nodes": int(len(ans.x)),
        "independent_EM_J": float(electric),
        "independent_scalar_J": float(scalar),
        "energy_relative_error": float(errE),
        "minimum_radial_acceleration_m_s2":
            float(accel.min()),
        "independent_alpha_threshold": float(crit),
    }


def verify(path):
    p = Path(path).resolve()

    assert p.parent == ROOT/"results/data"
    assert re.fullmatch(
        r"delta1_01_\d{8}T\d{12}Z\.json",
        p.name,
    )

    assert (
        p.with_name(p.name+".sha256").read_text().strip()
        == sha(p)+"  "+p.name
    )

    d = json.loads(p.read_text())

    assert d["classification"] == (
        "SCOPED_EXACT_NONLINEAR_SHELL_FAMILY_ENERGY_GATE"
    )
    assert d["branch"] == (
        "DELTA1-01_EXACT_NONLINEAR_SHELL"
    )
    assert d["gates"][
        "SAME_STATIC_GAUSS_SCALAR_VARIATIONAL_ENERGY"
    ] == "PASS_EXACT_RADIAL"
    assert d["gates"][
        "FULL_EINSTEIN_EARTH_CRAFT_ACTION"
    ] == "NOT_DERIVED"
    assert d["gates"][
        "EMPIRICAL_UV_AND_COMPLETE_OPERATING_ENERGY"
    ] == "NOT_CERTIFIED"

    assert d["qualified_gravity_bridge_survivors"] == []
    assert d["whole_craft_up"] == "NOT_DERIVED"

    for key in (
        "006D_replaced",
        "DELTA1_02_authorized",
        "PH16_05_authorized",
        "PH17_authorized",
        "GAMMA1_01_authorized",
    ):
        assert d[key] is False

    for rel,h in d["producers"].items():
        assert sha(ROOT/rel) == h

    for item in d["parents"].values():
        assert sha(ROOT/item["path"]) == item["sha256"]

    evidence = independent(d)

    print("DELTA1_01_INDEPENDENT_VERIFICATION=PASS")
    print(
        "BVP_ENERGY_REL_ERROR="
        +str(evidence["energy_relative_error"])
    )
    print(
        "BVP_MIN_RADIAL_ACCELERATION="
        +str(evidence["minimum_radial_acceleration_m_s2"])
    )
    print(
        "EXTERIOR_ONLY_ALPHA_THRESHOLD="
        +str(evidence["independent_alpha_threshold"])
    )
    print(
        "SCIENTIFIC_JSON_SHA256="+sha(p)
    )

    return evidence


def record(result,focused,full,independent_log):
    checked = verify(result)

    logs = [
        Path(x).resolve()
        for x in (
            focused,full,independent_log
        )
    ]

    assert all(
        x.parent == ROOT/"results/logs"
        for x in logs
    )

    texts = [p.read_text() for p in logs]

    assert re.search(
        r"\b14 passed\b",
        texts[0],
    )

    totals = re.findall(
        r"(?m)^\s*(\d+) passed(?:,|\s|$)",
        texts[1],
    )
    assert totals and int(totals[-1]) >= 3294

    assert (
        "DELTA1_01_INDEPENDENT_VERIFICATION=PASS"
        in texts[2]
    )

    stamp = dt.datetime.now(
        dt.timezone.utc
    ).strftime("%Y%m%dT%H%M%S%fZ")

    path = ROOT/"results/data"/(
        "delta1_01_verification_"+stamp+".json"
    )

    d = {
        "branch":
            "DELTA1-01_EXACT_NONLINEAR_SHELL",
        "classification":
            "SCOPED_INDEPENDENT_NONLINEAR_SHELL_VERIFIED_NO_PHYSICAL_PROMOTION",
        "science_sha256":
            sha(result),
        "focused_tests_passed":14,
        "full_regression_passed":
            int(totals[-1]),
        "independent_bvp":checked,
        "logs":{
            str(x.relative_to(ROOT)):sha(x)
            for x in logs
        },
        "qualified_gravity_bridge_survivors":[],
        "whole_craft_up":"NOT_DERIVED",
        "006D_replaced":False,
        "complete_operating_energy_lt10MJ":
            "NOT_CERTIFIED",
    }

    raw = (
        json.dumps(
            d,sort_keys=True,
            indent=2,allow_nan=False
        )+"\n"
    ).encode()

    with path.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())

    digest = hashlib.sha256(raw).hexdigest()

    with path.with_name(
        path.name+".sha256"
    ).open("x") as f:
        f.write(digest+"  "+path.name+"\n")
        f.flush()
        os.fsync(f.fileno())

    print("VERIFICATION_JSON="+str(path))
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
