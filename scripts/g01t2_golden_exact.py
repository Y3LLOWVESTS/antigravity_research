"""G01-T2: exact two-grid R3B source-controllability experiment.

The original R3X1 signed frozen-beta operator is retained.
Ten finite-shell X-electric/Y-magnetic multipoles are used
as idealized source controls, not physical source materials.

The exact acceleration is a quadratic function of the
source controls. A nonconvex multistart optimizer evaluates
its worst-point response on both historical grids.

An independent energy-ellipsoid dual supplies optimistic
pointwise upper bounds and assumption-scoped exclusions.

No Einstein metric, microscopic Y source, complete energy,
neutral-matter relaxation, or spacecraft force is certified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import legval, legder
from scipy.linalg import lu_factor, lu_solve, solve_triangular
from scipy.optimize import minimize, minimize_scalar, brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from antigravity_research.agminer.hook17_fdual_f_r3c1_validation import (
    _build_baseline_and_prep,
)
from antigravity_research.agminer.hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    _solve_loaded, _state, _direct_compare,
)
from antigravity_research.agminer.hook17_fdual_f_loaded_payload_homotopy import (
    _fields_from_potentials,
    _vectors_to_full_potentials,
)
from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    HBAR_C_EV_M,
    EV_J,
    REFERENCE_PORTAL_SCALE_EV,
)

T1_SHA = (
    "e7a265f3963131e2f0a06e2d0f04c688658bad68"
    "cb00bfb49b5ec91a90cc4e39"
)
T1_SOURCE_SHA = (
    "57efe5406cd8dde4a9a040a102e9781c2fbb225"
    "08fe323d5465ea0928921a3b0"
)

PARENT_ACCEL = {
    0.075: -46.40607408464625,
    0.050: -129.67185782242464,
}

TARGET = 9.80665
SHELL = 2.0
ELLS = (1, 2, 4, 8, 12)
MODES = tuple(
    (ell, kind)
    for ell in ELLS
    for kind in ("X_electric", "Y_magnetic")
)
COMP = ("e_rho", "e_z", "b_rho", "b_z")
N = len(MODES)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def get_t1(path):
    raw = Path(path).read_bytes()

    if hashlib.sha256(raw).hexdigest() != T1_SHA:
        raise RuntimeError("T1_SCIENCE_SHA_MISMATCH")

    d = json.loads(raw)

    if d["experiment"] != "G01-T0T1":
        raise RuntimeError("WRONG_T1_PARENT")

    if len(d["grids"]) != 2:
        raise RuntimeError("T1_MISSING_GRID")

    if d["source_sha256"] != T1_SOURCE_SHA:
        raise RuntimeError("T1_PRODUCER_SHA_MISMATCH")

    if sha(ROOT / "scripts/g01t_t0t1.py") != T1_SOURCE_SHA:
        raise RuntimeError("LOCAL_T1_SOURCE_SHA_MISMATCH")

    for filename, expected in d["parents"].items():
        if sha(ROOT / filename) != expected:
            raise RuntimeError("PARENT_SHA_MISMATCH: " + filename)

    return d


def shell_potentials(field, ell, kind):
    rho = np.asarray(field["rho_grid"])
    z = np.asarray(field["z_grid"])

    r = np.hypot(rho, z)
    safe = np.maximum(r, 1e-14)
    mu = np.clip(z / safe, -1.0, 1.0)

    coeff = np.zeros(ell + 1)
    coeff[-1] = 1.0

    radial = np.where(
        r <= SHELL,
        (r / SHELL) ** ell,
        (SHELL / safe) ** (ell + 1),
    )

    if kind == "X_electric":
        return radial * legval(mu, coeff), np.zeros_like(r)

    if kind == "Y_magnetic":
        a = (
            SHELL / (ell * (ell + 1))
            * radial
            * (rho / safe)
            * legval(mu, legder(coeff))
        )
        return np.zeros_like(r), a

    raise ValueError(kind)


def eb_dot(x, y):
    return (
        x["e_rho"] * y["b_rho"]
        + x["e_z"] * y["b_z"]
    )


def acc(field, dot):
    sigma = (
        -2.0 * HBAR_C_EV_M**2
        / REFERENCE_PORTAL_SCALE_EV**4
        * dot
    )

    return (
        -C_LIGHT_M_S**2
        * np.gradient(
            sigma,
            float(field["h"]),
            axis=0,
            edge_order=2,
        )
    )


def energy(field, maps):
    h = float(field["h"])
    vol = 2 * math.pi * field["rho_grid"] * h * h

    squared = sum(maps[k] ** 2 for k in COMP)

    return float(
        0.5 * np.sum(vol * squared)
        / HBAR_C_EV_M * EV_J
    )


def grid_build(h, norm_coarse=None):
    setup = _build_baseline_and_prep(h)
    field = setup["field"]
    p = setup["prep"]
    mask = np.asarray(field["payload"], bool)

    if not mask.any():
        raise RuntimeError("EMPTY_PAYLOAD")

    stand = float(np.min(
        np.hypot(
            field["rho_grid"][mask],
            field["z_grid"][mask],
        ) - SHELL
    ))

    if stand < 1.0 - 1e-9:
        raise RuntimeError("STANDOFF_BELOW_ONE_METER")

    sol = _solve_loaded(p, 1.0, 1.0)
    state = _state(setup, sol)

    if not sol["success"]:
        raise RuntimeError("PARENT_SOLVER_FAILED")

    if sol["relative_residual"] > 1e-7:
        raise RuntimeError("PARENT_RESIDUAL_FAILED")

    original = state["minimum_payload_acceleration_m_s2"]

    if abs(original - PARENT_ACCEL[h]) > 1e-5:
        raise RuntimeError("PARENT_LOADED_ACCELERATION_DRIFT")

    base_phi, base_a = _vectors_to_full_potentials(
        p, field, setup["phi0"], setup["a0"], sol
    )

    baseline = _fields_from_potentials(
        base_phi, base_a, field["rho_grid"], h
    )

    a0 = acc(
        field, eb_dot(baseline, baseline)
    )[mask]

    if abs(float(a0.min()) - PARENT_ACCEL[h]) > 1e-5:
        raise RuntimeError("BASELINE_RECONSTRUCTION_FAILED")

    rp = len(p["coupling"]["active_phi"])
    ra = len(p["coupling"]["active_a"])

    matrix = np.eye(rp + ra)
    matrix[:rp, rp:] = p["c_green_a"]
    matrix[rp:, :rp] = -p["d_green_phi"]

    lu = lu_factor(matrix)

    def response(phi, a):
        pv = phi[1:-1, :-1].reshape(-1)
        av = a[1:-1, 1:-1].reshape(-1)

        rhs = np.r_[
            -np.asarray(p["c_active"] @ av).reshape(-1),
            np.asarray(p["d_active"] @ pv).reshape(-1),
        ]

        y = lu_solve(lu, rhs)

        dp = np.asarray(
            p["green_phi"] @ y[:rp]
        ).reshape(-1)

        da = np.asarray(
            p["green_a"] @ y[rp:]
        ).reshape(-1)

        res1 = (
            p["operators"]["k_phi"] @ dp
            + p["coupling"]["c"] @ (av + da)
        )

        res2 = (
            p["operators"]["k_a"] @ da
            - p["coupling"]["d"] @ (pv + dp)
        )

        rel = max(
            float(np.linalg.norm(res1)),
            float(np.linalg.norm(res2)),
        ) / max(1.0, float(np.linalg.norm(rhs)))

        if not np.isfinite(rel) or rel > 2e-6:
            raise RuntimeError("SIGNED_RESPONSE_FAILED")

        total_phi, total_a = _vectors_to_full_potentials(
            p, field, phi, a,
            {"delta_phi_vec": dp, "delta_a_vec": da},
        )

        maps = _fields_from_potentials(
            total_phi,
            total_a,
            field["rho_grid"],
            h,
        )

        return maps, rel

    raw = []
    raw_energy = []
    residuals = []

    for ell, kind in MODES:
        maps, rel = response(
            *shell_potentials(field, ell, kind)
        )

        e = energy(field, maps)

        if not 0 < e < math.inf:
            raise RuntimeError("INVALID_MODE_ENERGY")

        raw.append(maps)
        raw_energy.append(e)
        residuals.append(rel)

    if norm_coarse is None:
        norm_coarse = np.sqrt(raw_energy)

    norm_coarse = np.asarray(norm_coarse, float)

    maps = [
        {
            k: x[k] / norm_coarse[i]
            for k in COMP
        }
        for i, x in enumerate(raw)
    ]

    g = np.stack([
        acc(
            field,
            eb_dot(baseline, x) + eb_dot(x, baseline),
        )[mask]
        for x in maps
    ], axis=1)

    # Exact quadratic acceleration coefficients.
    q = np.zeros((len(a0), N, N))

    for i in range(N):
        for j in range(i, N):
            v = 0.5 * acc(
                field,
                eb_dot(maps[i], maps[j])
                + eb_dot(maps[j], maps[i]),
            )[mask]

            q[:, i, j] = v
            q[:, j, i] = v

    vol = (
        2 * math.pi * field["rho_grid"] * h * h
        / HBAR_C_EV_M * EV_J
    )

    e0 = energy(field, baseline)

    linear = np.array([
        float(np.sum(
            vol * sum(
                baseline[k] * m[k] for k in COMP
            )
        ))
        for m in maps
    ])

    K = np.empty((N, N))

    for i in range(N):
        for j in range(i, N):
            val = 0.5 * float(np.sum(
                vol * sum(
                    maps[i][f] * maps[j][f]
                    for f in COMP
                )
            ))

            K[i, j] = val
            K[j, i] = val

    K = (K + K.T) * 0.5

    if np.linalg.eigvalsh(K)[0] < 1e-9:
        raise RuntimeError("FIELD_ENERGY_GRAM_NOT_POSITIVE")

    # Independently compare exact quadratic and reconstructed fields.
    rng = np.random.default_rng(
        20261122 + int(h * 1000)
    )

    errors = []

    for trial in range(5):
        u = rng.normal(size=N) * (
            0.18 if trial < 3 else 0.8
        )

        combined = {
            f: baseline[f] + sum(
                u[j] * maps[j][f]
                for j in range(N)
            )
            for f in COMP
        }

        direct_a = acc(
            field, eb_dot(combined, combined)
        )[mask]

        quadratic_a = (
            a0 + g @ u
            + np.einsum(
                "i,nij,j->n", u, q, u, optimize=True
            )
        )

        quadratic_e = (
            e0 + linear @ u + u @ K @ u
        )

        errors.append((
            float(np.max(np.abs(direct_a - quadratic_a))),
            abs(energy(field, combined) - quadratic_e),
        ))

    if max(x[0] for x in errors) > 1e-7:
        raise RuntimeError("ACCELERATION_QUADRATIC_FAILED")

    if max(x[1] for x in errors) > 1e-8:
        raise RuntimeError("ENERGY_QUADRATIC_FAILED")

    direct = None

    if h == 0.075:
        direct = _direct_compare(setup, sol, 1.0, 1.0)

        if not direct["pass"]:
            raise RuntimeError("DIRECT_SPARSE_PARENT_FAILED")

    return {
        "h": h,
        "a0": a0,
        "g": g,
        "q": q,
        "e0": e0,
        "l": linear,
        "k": K,
        "raw_energy": raw_energy,
        "normalization": norm_coarse,
        "rel": residuals,
        "stand": stand,
        "mask_count": int(mask.sum()),
        "original": original,
        "direct": direct,
        "errors": errors,
    }


def a_values(G, u):
    return (
        G["a0"] + G["g"] @ u
        + np.einsum(
            "i,nij,j->n", u, G["q"], u, optimize=True
        )
    )


def a_jac(G, u):
    return (
        G["g"] + 2 * np.einsum(
            "nij,j->ni", G["q"], u, optimize=True
        )
    )


def E(G, u):
    return float(
        G["e0"] + G["l"] @ u + u @ G["k"] @ u
    )


def upper_bound_single_point(G, i, cap, return_lambda=False):
    """Optimistic energy-ball upper bound.

    This ignores the source-control box and all other payload
    points. Its result is therefore an upper bound on what
    the entire sampled torus could achieve for that cap.
    """

    K = G["k"]
    L = np.linalg.cholesky(K)
    U = L.T

    uc = -0.5 * np.linalg.solve(K, G["l"])
    emin = E(G, uc)

    if cap < emin - 1e-10:
        if return_lambda:
            return float("-inf"), None
        return float("-inf")

    radius2 = max(0.0, cap - emin)

    Q = G["q"][i]
    grad = G["g"][i]

    invU = solve_triangular(
        U, np.eye(N), lower=False
    )

    H = invU.T @ Q @ invU
    H = (H + H.T) / 2

    new_grad = invU.T @ (grad + 2 * Q @ uc)

    constant = float(
        G["a0"][i]
        + grad @ uc
        + uc @ Q @ uc
    )

    eig, V = np.linalg.eigh(H)
    squared = (V.T @ new_grad) ** 2

    lam0 = max(0.0, float(eig[-1]))
    scale = max(
        1.0, abs(lam0), float(np.max(np.abs(eig)))
    )

    def dual(logstep):
        lam = lam0 + scale * math.exp(float(logstep))
        den = lam - eig

        if np.any(den <= 0):
            return math.inf

        return float(
            constant
            + lam * radius2
            + 0.25 * np.sum(squared / den)
        )

    res = minimize_scalar(
        dual,
        bounds=(-27.0, 27.0),
        method="bounded",
        options={"xatol": 1e-8},
    )

    options = [-27.0, 27.0, float(res.x)]
    winner = min(options, key=dual)

    value = dual(winner)
    lam = lam0 + scale * math.exp(winner)

    if return_lambda:
        return value, lam

    return value


def t1_reproduction(G, old_grid, coarse_norm):
    # Convert the historical per-grid normalization into
    # the same shell amplitudes on both new grids.
    factors = (
        np.asarray(coarse_norm)
        / np.sqrt(np.asarray(G["raw_energy"]))
    )

    differences = []

    for row in old_grid["rows"]:
        if not row["success"]:
            continue

        u = np.asarray(row["controls"]) * factors

        actual = float(np.min(a_values(G, u)))
        actual_energy = E(G, u)

        da = actual - row["full_bilinear_min_m_s2"]
        de = actual_energy - row["full_bilinear_field_energy_j"]

        differences.append({
            "bound": row["mode_bound"],
            "acc_diff": da,
            "energy_diff_j": de,
        })

        if abs(da) > 1e-6 or abs(de) > 1e-7:
            raise RuntimeError("T1_EXACT_REPRODUCTION_FAILED")

    return differences


def optimize(grids, cap, bound, seeds, maxiter):
    count = sum(len(g["a0"]) for g in grids)

    def fields(u):
        aa = np.concatenate([
            a_values(g, u) for g in grids
        ])
        jac = np.concatenate([
            a_jac(g, u) for g in grids
        ], axis=0)

        return aa, jac

    def constraints(z):
        u = z[:N]
        threshold = z[N]
        aa, _ = fields(u)

        return np.r_[
            aa - threshold,
            [cap - E(g, u) for g in grids],
        ]

    def jacobian(z):
        u = z[:N]
        _, jac = fields(u)

        left = np.column_stack((
            jac, -np.ones(count)
        ))

        right = np.stack([
            np.r_[
                -(g["l"] + 2 * g["k"] @ u),
                0,
            ]
            for g in grids
        ])

        return np.concatenate([left, right], axis=0)

    best = None
    trials = []

    for number, seed in enumerate(seeds):
        u = np.clip(
            np.asarray(seed, float), -bound, bound
        )

        while (
            max(E(g, u) for g in grids) > cap
            and np.linalg.norm(u) > 1e-13
        ):
            u *= 0.5

        threshold = float(min(
            np.min(a_values(g, u)) for g in grids
        ))

        start = np.r_[u, threshold]

        result = minimize(
            lambda z: -z[N],
            start,
            jac=lambda z: np.r_[
                np.zeros(N), -1.0
            ],
            method="SLSQP",
            bounds=(
                [(-bound, bound)] * N
                + [(None, None)]
            ),
            constraints=[{
                "type": "ineq",
                "fun": constraints,
                "jac": jacobian,
            }],
            options={
                "ftol": 1e-9,
                "maxiter": maxiter,
                "disp": False,
            },
        )

        u = np.asarray(result.x[:N])

        actual = float(min(
            np.min(a_values(g, u)) for g in grids
        ))

        energies = [E(g, u) for g in grids]

        feasible = bool(
            np.all(np.isfinite(u))
            and np.max(np.abs(u)) <= bound + 2e-7
            and max(energies) <= cap + 2e-6
            and actual >= float(result.x[N]) - 2e-5
        )

        trials.append({
            "seed": number,
            "success": bool(result.success),
            "feasible": feasible,
            "iterations": int(result.nit),
            "actual_min_m_s2": actual,
            "max_field_energy_j": float(max(energies)),
            "message": str(result.message)[:140],
        })

        if feasible and (
            best is None or actual > best["min_m_s2"]
        ):
            best = {
                "min_m_s2": actual,
                "u": u.tolist(),
                "field_energy_j_by_grid": energies,
                "acceleration_m_s2_by_grid": [
                    float(np.min(a_values(g, u)))
                    for g in grids
                ],
                "solver_reported_success":
                    bool(result.success),
                "iteration_count": int(result.nit),
            }

    return best, trials


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--t1", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-iter", type=int, default=240)
    parser.add_argument("--random-starts", type=int, default=5)
    args = parser.parse_args()

    started = time.monotonic()

    t1 = get_t1(args.t1)

    coarse = grid_build(0.075)
    fine = grid_build(
        0.050, norm_coarse=coarse["normalization"]
    )

    grids = [coarse, fine]

    t1_audits = [
        t1_reproduction(g, old, coarse["normalization"])
        for g, old in zip(grids, t1["grids"])
    ]

    print(
        "T1_PARENTS=PASS TWO_GRIDS=REPRODUCED",
        flush=True,
    )
    print(
        "EXACT_QUADRATIC=PASS SHARED_SOURCE=YES",
        flush=True,
    )

    seeds = [np.zeros(N)]

    for G, old in zip(grids, t1["grids"]):
        factors = (
            np.asarray(coarse["normalization"])
            / np.sqrt(np.asarray(G["raw_energy"]))
        )

        for row in old["rows"]:
            if (
                row["success"]
                and row["mode_bound"] in (0.25, 0.5)
            ):
                seeds.append(
                    np.asarray(row["controls"]) * factors
                )

    A = np.concatenate([g["g"] for g in grids])
    desired = np.concatenate([
        np.full(len(g["a0"]), TARGET) - g["a0"]
        for g in grids
    ])

    seeds.append(
        np.linalg.lstsq(A, desired, rcond=1e-9)[0]
    )

    rng = np.random.default_rng(20261122)

    seeds.extend(
        rng.normal(0.0, 0.7, N)
        for _ in range(max(0, args.random_starts))
    )

    settings = [
        (2.0, 0.5),
        (2.0, 2.0),
        (10.0, 2.0),
        (10.0, 5.0),
        (100.0, 8.0),
    ]

    results = []

    for cap, bound in settings:
        print(
            "EXACT_QCQP",
            "CAP_J", cap,
            "MODE_BOUND", bound,
            flush=True,
        )

        best, trials = optimize(
            grids,
            cap,
            bound,
            seeds,
            args.max_iter,
        )

        if best is None:
            status = "OPTIMIZER_FAILED_NO_CERTIFICATE"
        elif best["min_m_s2"] >= TARGET:
            status = "ARTIFICIAL_SIGN_REVERSAL"
        else:
            status = "NO_1G_CANDIDATE_FOUND"

        print(
            "STATUS", status,
            "MIN", None if best is None else best["min_m_s2"],
            flush=True,
        )

        upper = [
            upper_bound_single_point(g, i, cap)
            for g in grids
            for i in range(len(g["a0"]))
        ]

        min_upper = float(min(upper))

        if min_upper < TARGET - 1e-5:
            certificate = (
                "ENERGY_BALL_POINTWISE_IMPOSSIBILITY_"
                "FOR_FROZEN_BETA_SAMPLES"
            )
        else:
            certificate = "UPPER_BOUND_INCONCLUSIVE"

        results.append({
            "cap_canonical_field_j": cap,
            "bound_per_coarse_normalized_mode": bound,
            "status": status,
            "best": best,
            "solver_trials": trials,
            "relaxed_upper_bound_on_global_min_m_s2":
                min_upper,
            "upper_bound_status": certificate,
        })

    diagnostics = []

    for cap in (2.0, 10.0, 100.0, 10000.0, 1e7):
        choices = []

        for G in grids:
            bounds = [
                upper_bound_single_point(G, i, cap, True)
                for i in range(len(G["a0"]))
            ]

            idx = min(
                range(len(bounds)),
                key=lambda i: bounds[i][0],
            )

            choices.append({
                "h_m": G["h"],
                "payload_index": int(idx),
                "energy_ellipsoid_dual_upper_m_s2":
                    float(bounds[idx][0]),
                "certifying_dual_lambda":
                    float(bounds[idx][1]),
            })

        joint_upper = min(
            x["energy_ellipsoid_dual_upper_m_s2"]
            for x in choices
        )

        diagnostics.append({
            "field_energy_cap_j": cap,
            "per_grid": choices,
            "joint_optimistic_upper_m_s2": joint_upper,
            "one_point_1g_exclusion":
                bool(joint_upper < TARGET - 1e-5),
        })

    def min_upper(cap):
        return min(
            upper_bound_single_point(G, i, cap)
            for G in grids
            for i in range(len(G["a0"]))
        )

    necessary_cap = float(
        brentq(
            lambda c: min_upper(c) - TARGET,
            100.0,
            1e7,
            xtol=0.1,
        )
    )

    winner = max(
        (
            r for r in results
            if r["best"] is not None
        ),
        key=lambda r: r["best"]["min_m_s2"],
        default=None,
    )

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)

    np.savez_compressed(
        out / "quadratic_coefficients.npz",
        **{
            f"{key}_{tag}": value
            for tag, G in (
                ("075", coarse),
                ("050", fine),
            )
            for key, value in [
                ("a0", G["a0"]),
                ("g", G["g"]),
                ("Q", G["q"]),
                ("E0", np.array(G["e0"])),
                ("l", G["l"]),
                ("K", G["k"]),
            ]
        },
    )

    report = {
        "experiment":
            "G01-T2-EXACT-QUADRATIC-SHARED-SOURCE-GOLDEN",
        "created_utc":
            datetime.now(timezone.utc).isoformat(),
        "source_sha256": sha(__file__),
        "t1_source_sha256": T1_SOURCE_SHA,
        "t1_science_sha256": T1_SHA,
        "parent_files_sha256": t1["parents"],
        "model":
            "ORIGINAL_R3X1_LORENTZIAN_FROZEN_BETA_"
            "IDEAL_SHELL_CONTROLS",
        "source_shell_radius_m": SHELL,
        "source_control_modes": [
            {"ell": ell, "kind": kind}
            for ell, kind in MODES
        ],
        "same_shell_amplitudes_on_both_grids": True,
        "grids": [
            {
                "h_m": G["h"],
                "payload_count": G["mask_count"],
                "minimum_sampled_clearance_m": G["stand"],
                "baseline_min_m_s2": G["original"],
                "baseline_field_energy_j": G["e0"],
                "raw_loaded_mode_energy_j": G["raw_energy"],
                "signed_response_residual_max":
                    max(G["rel"]),
                "quadratic_reconstruction_acc_max_abs_error":
                    max(v[0] for v in G["errors"]),
                "quadratic_reconstruction_energy_max_abs_error":
                    max(v[1] for v in G["errors"]),
                "energy_quadratic_eigen_min":
                    float(np.linalg.eigvalsh(G["k"])[0]),
                "t1_exact_reproduction": audit,
            }
            for G, audit in zip(grids, t1_audits)
        ],
        "results": results,
        "rigorous_relaxed_energy_ball_bounds": diagnostics,
        "optimistic_necessary_field_energy_j_for_sampled_1g":
            necessary_cap,
        "quadratic_coefficients_file":
            "quadratic_coefficients.npz",
        "quadratic_coefficients_sha256":
            sha(out / "quadratic_coefficients.npz"),
        "best_evaluated_setting":
            None if winner is None else {
                "cap_j": winner["cap_canonical_field_j"],
                "mode_bound":
                    winner["bound_per_coarse_normalized_mode"],
                "minimum_m_s2":
                    winner["best"]["min_m_s2"],
            },
        "target_m_s2": TARGET,
        "full_regression": "NOT_RUN_BY_USER_POLICY",
        "independent_second_field_solver": "NOT_RUN",
        "physical_source_action": "NOT_DERIVED",
        "microscopic_Y_current": "NOT_IDENTIFIED",
        "source_support_energy_j": None,
        "universal_Einstein_metric": "NOT_SOLVED",
        "earth_down_whole_craft_up": "NOT_DERIVED",
        "neutral_body_equilibrium": "FROZEN_BETA",
        "continuum_exterior": "NOT_CERTIFIED",
        "physical_survivors": 0,
        "physical_research_maturity_percent": 37,
        "claim": "ARTIFICIAL_SOURCE_CONTROL_FEASIBILITY_ONLY",
        "wall_seconds": time.monotonic() - started,
    }

    data = (
        json.dumps(
            report,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        ) + "\n"
    ).encode()

    (out / "science.json").write_bytes(data)

    science_sha = hashlib.sha256(data).hexdigest()

    (out / "science.json.sha256").write_text(
        science_sha + "  science.json\n"
    )

    print(
        "OPTIMISTIC_NECESSARY_FIELD_ENERGY_J",
        necessary_cap,
        flush=True,
    )
    print("RESULT_DIR", out, flush=True)
    print("SCIENCE_SHA256", science_sha, flush=True)
    print(
        "PHYSICAL_SOURCE_AND_GRAVITY=HOLD_NOT_CERTIFIED",
        flush=True,
    )


if __name__ == "__main__":
    main()
