"""Independent D0 metric/field variation and evidence verifier.

This verifier deliberately does not import the D0 scientific producer.
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


def independent_derivation():
    """Second variational model: pure potential, different metric/fields."""
    U = .32
    alpha, beta = .05, 40.
    h = 2e-6

    g = np.diag([-1.3, 1.2, 1.05, .9])
    dg = np.diag([.012, -.01, .015, .007])
    ex, by = -.023, .03

    def action_density(metric, magnetic_y):
        volume = np.sqrt(-np.linalg.det(metric))
        p = ex*magnetic_y/volume
        sig = alpha*p-beta*p*p
        return -volume*U*np.exp(4*sig)

    volume = np.sqrt(-np.linalg.det(g))
    p = ex*by/volume
    sig = alpha*p-beta*p*p
    ds = alpha-2*beta*p

    lam = -4*U*np.exp(4*sig)*ds

    numerical_y = (
        action_density(g, by+h)-action_density(g, by-h)
    )/(2*h)
    exact_y = lam*ex
    error_y = float(abs(numerical_y-exact_y))

    Tg = (
        -np.exp(4*sig)*U*(1-4*p*ds)
        * np.linalg.inv(g)
    )
    numerical_metric = (
        action_density(g+h*dg, by)
        - action_density(g-h*dg, by)
    )/(2*h)
    exact_metric = .5*volume*np.sum(Tg*dg)
    error_metric = float(
        abs(numerical_metric-exact_metric)
    )

    assert max(error_y, error_metric) < 1e-8
    return {
        "portal_Y_FD_error": error_y,
        "metric_FD_error": error_metric,
    }


def verify(path):
    p = Path(path).resolve()

    assert p.parent == ROOT/"results/data"
    assert re.fullmatch(
        r"gamma1_d0_\d{8}T\d{12}Z\.json", p.name
    )

    sidecar = p.with_name(p.name+".sha256")
    assert sidecar.read_text().strip() == (
        sha(p)+"  "+p.name
    )

    d = json.loads(p.read_text())
    assert d["branch"] == "GAMMA1-POSTR12-D0"
    assert d["classification"] == (
        "SCOPED_LOCAL_PROXY_ACTION_WARDS_PASS_"
        "PHYSICAL_BRIDGE_NOT_ESTABLISHED"
    )
    assert d["gates"]["TWO_CARRIER_VARIATIONS"] == "PASS_SCOPED"
    assert d["gates"]["CHARGED_CURRENT_AND_GAUGE_WARD"] == "PASS_SCOPED"
    assert d["gates"]["FULL_EARTH_SUPPORT_FLUID_GR_ACTION"] == "NOT_DERIVED"
    assert d["gates"]["PH16_R11_MATCHED_AS_STATIC_REDUCTION"] == "NOT_DERIVED"
    assert d["gates"]["TRUE_EXTERIOR_EINSTEIN_FORCE"] == "NOT_DERIVED"
    assert d["gates"]["FULL_LORENTZIAN_CONSTRAINED_HEALTH"] == "NOT_CERTIFIED"
    assert d["complete_energy"] == "ENERGY_UNDETERMINED"
    assert d["whole_craft_up"] == "NOT_DERIVED"
    assert d["qualified_survivors"] == []

    for key in (
        "GAMMA1_01_authorized",
        "PH16_05_authorized",
        "PH17_authorized",
        "006D_replaced",
    ):
        assert d[key] is False

    assert all(d["negative_controls"].values())
    assert max(d["errors"].values()) < 1e-8

    for rel, digest in d["producers"].items():
        assert sha(ROOT/rel) == digest

    for item in d["parents"].values():
        assert sha(ROOT/item["path"]) == item["sha256"]

    second = independent_derivation()
    print("D0_INDEPENDENT_VERIFICATION=PASS")
    print("SECOND_Y_VARIATION_FD="+str(second["portal_Y_FD_error"]))
    print("SECOND_METRIC_VARIATION_FD="+str(second["metric_FD_error"]))
    print("D0_SCIENCE_SHA256="+sha(p))
    return second


def record(result, focused, full, independent):
    second = verify(result)

    log_paths = [
        Path(p).resolve()
        for p in (focused, full, independent)
    ]
    assert all(
        p.parent == ROOT/"results/logs"
        for p in log_paths
    )

    texts = [p.read_text() for p in log_paths]
    assert re.search(r"\b8 passed\b", texts[0])

    matches = re.findall(
        r"(?m)^\s*(\d+) passed(?:,|\s|$)",
        texts[1]
    )
    assert matches and int(matches[-1]) >= 3241
    assert "D0_INDEPENDENT_VERIFICATION=PASS" in texts[2]

    stamp = dt.datetime.now(dt.timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )
    path = ROOT/"results/data"/(
        "gamma1_d0_verification_"+stamp+".json"
    )
    doc = {
        "branch": "GAMMA1-POSTR12-D0",
        "classification": "SCOPED_PROXY_AUDIT_VERIFIED_NO_PROMOTION",
        "scientific_sha256": sha(result),
        "focused_tests_passed": 8,
        "full_regression_passed": int(matches[-1]),
        "second_derivation": second,
        "logs": {
            str(p.relative_to(ROOT)): sha(p)
            for p in log_paths
        },
        "GAMMA1_01_authorized": False,
        "whole_craft_up": "NOT_DERIVED",
        "complete_energy": "NOT_CERTIFIED",
    }

    raw = (
        json.dumps(doc, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode()

    with path.open("xb") as output:
        output.write(raw)
        output.flush()
        os.fsync(output.fileno())

    with path.with_name(path.name+".sha256").open("x") as output:
        output.write(
            hashlib.sha256(raw).hexdigest()
            + "  " + path.name + "\n"
        )
        output.flush()
        os.fsync(output.fileno())

    print("VERIFICATION_JSON="+str(path))
    print("VERIFICATION_SHA256="+sha(path))


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
