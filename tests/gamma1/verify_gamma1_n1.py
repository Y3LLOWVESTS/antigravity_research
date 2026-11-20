"""Independent N1 native-source verification.

Does not import the producing N1 scientific implementation.
Reconstructs PH16's discrete differential matrices independently.
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
from scipy import sparse

ROOT = Path(__file__).resolve().parents[2]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def derivative(n, h):
    rows, cols, vals = [], [], []
    for i in range(n):
        if i == 0:
            entries = [(0, -1/h), (1, 1/h)]
        elif i == n-1:
            entries = [(n-2, -1/h), (n-1, 1/h)]
        else:
            entries = [(i-1, -.5/h), (i+1, .5/h)]
        for j, value in entries:
            rows.append(i)
            cols.append(j)
            vals.append(value)
    return sparse.coo_matrix(
        (vals, (rows, cols)), shape=(n, n)
    ).tocsr()


def independent_native():
    nr, nz = 12, 24
    data = ROOT/"results/data"

    with np.load(
        data/"gamma1_00r3_20261119T001454764826Z_native_12_L12.npz",
        allow_pickle=False
    ) as z:
        A = z["A_X"].copy()
        Y = z["A_Y"].copy()
        P_saved = z["P"].copy()
        weights = z["weights"].copy()

    with np.load(
        data/"gamma1_00r5_20261119T024922295970Z_lattice_multiplier_12_L12.npz",
        allow_pickle=False
    ) as z:
        lam = z["lambda_Routhian"].copy()

    rho = np.repeat(np.arange(nr)+.5, nz)
    w = 2*np.pi*rho

    if np.max(abs(w-weights)) > 1e-10:
        raise AssertionError("INDEPENDENT_NATIVE_WEIGHT_MISMATCH")

    Dr = sparse.kron(
        derivative(nr, 1.),
        sparse.eye(nz),
        format="csr"
    )
    Dz = sparse.kron(
        sparse.eye(nr),
        derivative(nz, 1.),
        format="csr"
    )

    Er = -Dr@A
    Ez = -Dz@A

    def magnetic(y):
        return -Dz@y, (Dr@(rho*y))/rho

    Br, Bz = magnetic(Y)

    if np.max(abs(P_saved-(Er*Br+Ez*Bz))) > 2e-12:
        raise AssertionError("INDEPENDENT_NATIVE_P_MISMATCH")

    # Independent matrix variation of
    # -sum_cells(w*lambda*(Er*Br+Ez*Bz)).
    Br_matrix = -Dz
    Bz_matrix = (
        sparse.diags(1/rho)
        @ Dr
        @ sparse.diags(rho)
    )

    grad_y = np.asarray(
        Br_matrix.T@(w*lam*Er)
        + Bz_matrix.T@(w*lam*Ez)
    ).ravel()
    source = -grad_y

    core = np.zeros((nr, nz), dtype=bool)
    core[3:-3, 3:-3] = True
    mask = core.ravel()

    constant = -(
        Br_matrix.T@(w*Er)
        + Bz_matrix.T@(w*Ez)
    )
    constant_inf = float(np.max(abs(constant[mask])))

    rng = np.random.default_rng(17)
    direction = rng.normal(size=len(Y))
    direction /= np.linalg.norm(direction)

    def functional(y):
        by, bz = magnetic(y)
        return -float(np.dot(
            w*lam, Er*by+Ez*bz
        ))

    h = 1e-4
    finite = (
        functional(Y+h*direction)
        - functional(Y-h*direction)
    )/(2*h)
    derivative_error = float(
        abs(finite-np.dot(source, direction))
    )

    if derivative_error > 1e-7 or constant_inf > 1e-9:
        raise AssertionError("INDEPENDENT_NATIVE_WARD_FAIL")

    return {
        "Y_source_l2": float(np.linalg.norm(source)),
        "constant_lambda_bulk_inf": constant_inf,
        "independent_Y_variational_fd_error": derivative_error,
    }


def verify(path):
    p = Path(path).resolve()

    assert p.parent == ROOT/"results/data"
    assert re.fullmatch(
        r"gamma1_n1_\d{8}T\d{12}Z\.json", p.name
    )
    assert p.with_name(p.name+".sha256").read_text().strip() == (
        sha(p)+"  "+p.name
    )

    d = json.loads(p.read_text())

    assert d["classification"] == (
        "SCOPED_NATIVE_WARD_AND_INDUCTION_AUDIT_NO_PHYSICAL_PROMOTION"
    )
    assert d["gates"][
        "CONSTANT_MIXED_COEFFICIENT_BULK_TOPOLOGICAL_WARD"
    ] == "PASS_SCOPED"
    assert d["gates"][
        "NATIVE_CONTINUUM_AND_EXTERIOR_MATCH"
    ] == "NOT_ESTABLISHED"

    for key in (
        "GAMMA1_01_authorized",
        "PH16_05_authorized",
        "PH17_authorized",
        "006D_replaced"
    ):
        assert d[key] is False

    assert d["qualified_gravity_bridge_survivors"] == []
    assert d["whole_craft_up"] == "NOT_DERIVED"
    assert d["GAMMA_heuristic_percent"] == "UNCHANGED_34"

    for rel, digest in d["producer_sources"].items():
        assert sha(ROOT/rel) == digest

    for entry in d["parents"].values():
        assert sha(ROOT/entry["path"]) == entry["sha256"]

    independent = independent_native()

    if abs(
        d["native"]["native_Y_source_l2"]
        - independent["Y_source_l2"]
    ) > 1e-9:
        raise AssertionError("INDEPENDENT_SOURCE_MISMATCH")

    assert d["native"]["constant_lambda_Y_bulk_inf"] < 1e-9

    print("N1_INDEPENDENT_VERIFICATION=PASS")
    print(
        "INDEPENDENT_NATIVE_Y_SOURCE_L2="
        + str(independent["Y_source_l2"])
    )
    print(
        "INDEPENDENT_VARIATIONAL_FD_ERROR="
        + str(independent["independent_Y_variational_fd_error"])
    )
    print(
        "N1_NATIVE_FIT_ARTIFACT_OVER_TOTAL="
        + str(d["native"]["integrability_projection"][
            "Y_aligned_artifact_over_total"
        ])
    )
    print("SCIENTIFIC_JSON_SHA256="+sha(p))

    return independent


def record(result, focused, full, independent):
    values = verify(result)

    logs = [
        Path(x).resolve()
        for x in (focused, full, independent)
    ]
    assert all(x.parent == ROOT/"results/logs" for x in logs)
    texts = [x.read_text() for x in logs]

    assert re.search(r"\b11 passed\b", texts[0])

    totals = re.findall(
        r"(?m)^\s*(\d+) passed(?:,|\s|$)", texts[1]
    )
    assert totals and int(totals[-1]) >= 3266
    assert "N1_INDEPENDENT_VERIFICATION=PASS" in texts[2]

    stamp = dt.datetime.now(dt.timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )
    path = ROOT/"results/data"/(
        "gamma1_n1_verification_"+stamp+".json"
    )

    doc = {
        "branch": "GAMMA1-N1",
        "classification":
            "SCOPED_INDEPENDENT_VERIFIED_NO_PHYSICAL_PROMOTION",
        "scientific_result_sha256": sha(result),
        "full_regression_passed": int(totals[-1]),
        "focused_passed": 11,
        "independent_result": values,
        "logs": {
            str(x.relative_to(ROOT)): sha(x)
            for x in logs
        },
        "GAMMA1_01_authorized": False,
        "006D_replaced": False,
        "whole_craft_up": "NOT_DERIVED",
    }

    raw = (
        json.dumps(doc, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode()

    with path.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())

    digest = hashlib.sha256(raw).hexdigest()
    with path.with_name(path.name+".sha256").open("x") as f:
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
