"""R3X3A: physical-sign cross U(1) source-cone interface falsification.

For the normalized linear portal, F_X*F_Y = (F_+*F_+ - F_-*F_-)/2.
The two canonical +/- sectors therefore have opposite beta-loading signs,
and their portal acceleration contributes with opposite signs while their
Maxwell energy contributions add. The R3X2R2 same-sign cone is not this cone.

Finite grids and frozen density beta only. A feasible convex PSD relaxation
is not a two-field physical realization or a complete-energy certificate.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from .hook17_concurrent_u1_fieldstrength_metric import (
    HBAR_C_EV_M, REFERENCE_PORTAL_SCALE_EV, TARGET_ACCELERATION_M_S2,
    geometric_standoff_m,
)
from .hook17_fdual_f_r3x2_source_cone import (
    _build_baseline_and_prep, source_modes, loaded_response_basis,
    quadratic_payload_matrices, source_ward_gate,
)
from .hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    _solve_loaded, _direct_compare, constitutive_action_gate,
)

BRANCH = "032H17A12D1R3X3A"
GRIDS = (0.075, 0.05)
BUDGET_J = 10_000_000.0
TARGET_G = float(TARGET_ACCELERATION_M_S2)
SENSITIVITY = (0.0, 1e-10, 1e-9, 1e-8)


def algebra_gate() -> dict[str, Any]:
    rng = np.random.default_rng(31730)
    f = rng.normal(size=(4, 3))  # E+, B+, E-, B-
    ep, bp, em, bm = f
    ex, ey = (ep + em) / np.sqrt(2), (ep - em) / np.sqrt(2)
    bx, by = (bp + bm) / np.sqrt(2), (bp - bm) / np.sqrt(2)
    cross = float(ex @ by + ey @ bx)
    diagonal = float(ep @ bp - em @ bm)
    energy_original = float(np.sum(ex**2 + ey**2 + bx**2 + by**2))
    energy_diagonal = float(np.sum(ep**2 + em**2 + bp**2 + bm**2))
    action = constitutive_action_gate()
    return {
        "cross_identity_residual": abs(cross - diagonal),
        "canonical_energy_residual": abs(energy_original - energy_diagonal),
        "independent_u1_ward": action["independent_u1_gauge_bianchi_pass"],
        "parity_algebra_only": action["polar_x_axial_y_parity_algebra_pass"],
        "microscopic_parity_anomaly_complete": False,
        "same_action_signs": [1, -1],
        "pass": bool(abs(cross-diagonal)<1e-12 and
                     abs(energy_original-energy_diagonal)<1e-12 and
                     action["independent_u1_gauge_bianchi_pass"]),
    }


def old_witness(h: float) -> list[dict[str, Any]]:
    root = Path(__file__).resolve().parents[3]
    path = root / "results/data/032h17a12d1r3x2r2_energy_budget_dual_summary.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["branch"] == "032H17A12D1R3X2R2"
    grid = next(g for g in data["grids"] if abs(g["h_m"]-h)<1e-12)
    return grid["catalogs"]["shell_only"]["new_dual_solve"]["witness"]["largest_weights"]


def whiten(a: np.ndarray, h: np.ndarray):
    h = (h+h.T)/2
    e, v = np.linalg.eigh(h)
    if e[0] <= 0 or e[0] < 1e-12 * e[-1]:
        raise ValueError("energy Gram nonpositive or energy rank unresolved")
    w = v / np.sqrt(e)[None, :]
    residual = float(np.max(np.abs(w.T @ h @ w - np.eye(len(e)))))
    b = np.einsum("ir,pij,js->prs", w, a, w, optimize=True)
    b = (b + np.swapaxes(b,1,2))/2
    return b, w, residual, float(e[-1]/e[0])


def source_grid(h: float):
    setup = _build_baseline_and_prep(float(h))
    modes = source_modes(setup)
    indices = [i for i, m in enumerate(modes) if m["shell_source"]]
    assert len(indices) == 6
    blocks = {}
    for sign in (1, -1):
        resp = loaded_response_basis(setup, modes, lam=float(sign))
        if resp["relative_source_residual"] >= 1e-7:
            raise RuntimeError("signed source Ward/loading residual failed")
        a, hmat = quadratic_payload_matrices(setup, resp)
        a = a[:, indices][:, :, indices]
        hmat = hmat[np.ix_(indices, indices)]
        b, w, err, cond = whiten(a, hmat)
        if err > 1e-7:
            raise RuntimeError("noncanonical energy whitening")
        blocks[sign] = {
            "a": a, "h": hmat, "b": b, "w": w,
            "whiten_error": err, "energy_condition": cond,
            "residual": resp["relative_source_residual"], "response": resp
        }

    scale = max(float(np.max(np.abs(blocks[1]["b"]))),
                float(np.max(np.abs(blocks[-1]["b"]))))
    if scale <= 0 or not math.isfinite(scale):
        raise RuntimeError("zero or nonfinite cross-source response")

    bp = blocks[1]["b"] / scale
    bm = -blocks[-1]["b"] / scale
    points = np.argwhere(setup["field"]["payload"])

    weight_record = old_witness(h)
    mu_old = np.zeros(len(points))
    for item in weight_record:
        mu_old[int(item["payload_index"])] = float(item["weight"])
    mu_old /= np.sum(mu_old)

    witness_old_plus = float(
        np.linalg.eigvalsh(np.einsum("p,pij->ij", mu_old, bp))[-1]
    )
    witness_old_minus = float(
        np.linalg.eigvalsh(np.einsum("p,pij->ij", mu_old, bm))[-1]
    )

    info = {
        "h_m": float(h),
        "payload_points": len(points),
        "source_names": [modes[i]["name"] for i in indices],
        "source_radius_m": 2.0,
        "analytic_geometric_standoff_m": float(geometric_standoff_m()),
        "acceleration_per_joule_scale": scale,
        "plus_whiten_error": blocks[1]["whiten_error"],
        "minus_whiten_error": blocks[-1]["whiten_error"],
        "plus_loaded_residual": blocks[1]["residual"],
        "minus_loaded_residual": blocks[-1]["residual"],
        "old_witness_largest_plus_eigenvalue": witness_old_plus,
        "old_witness_largest_opposite_sector_eigenvalue": witness_old_minus,
        "old_witness_excludes_both_opposite_sectors": bool(
            max(witness_old_plus, witness_old_minus) < -1e-8
        ),
    }

    private = {
        "setup": setup, "modes": modes, "indices": indices,
        "blocks": blocks, "bp": bp, "bm": bm, "scale": scale
    }
    return info, private


def verify_dual(bp, bm, mu, scale):
    weights = np.maximum(np.asarray(mu, dtype=float).reshape(-1), 0.0)
    if not np.isfinite(weights).all() or np.sum(weights) <= 0:
        return None
    weights /= np.sum(weights)

    gamma_plus = float(np.linalg.eigvalsh(
        np.einsum("p,pij->ij", weights, bp)
    )[-1])
    gamma_minus = float(np.linalg.eigvalsh(
        np.einsum("p,pij->ij", weights, bm)
    )[-1])
    gamma = max(gamma_plus, gamma_minus)

    stress = []
    for eps in SENSITIVITY:
        upper = max(0.0, gamma + eps) * scale * BUDGET_J
        stress.append({
            "normalized_matrix_perturbation": eps,
            "one_g_excluded_below_10mj": bool(upper < 0.95 * TARGET_G),
            "maximum_min_acceleration_at_10mj_m_s2": upper,
            "minimum_canonical_field_energy_j_if_positive": (
                TARGET_G / ((gamma + eps) * scale)
                if gamma + eps > 0 else None
            ),
        })

    order = np.argsort(weights)[-8:][::-1]
    return {
        "gamma_plus": gamma_plus,
        "gamma_minus": gamma_minus,
        "gamma_max": gamma,
        "energy_bound": stress,
        "weights_top_indices": [int(i) for i in order],
        "weights_top_values": [float(weights[i]) for i in order],
    }


def dual_solve(bp, bm, scale):
    import cvxpy as cp

    count, n, _ = bp.shape
    mu = cp.Variable(count, nonneg=True)
    tau = cp.Variable()

    weighted_plus = cp.reshape(
        np.transpose(bp, (1, 2, 0)).reshape(n*n, count) @ mu,
        (n, n), order="C"
    )
    weighted_minus = cp.reshape(
        np.transpose(bm, (1, 2, 0)).reshape(n*n, count) @ mu,
        (n, n), order="C"
    )

    problem = cp.Problem(
        cp.Minimize(tau),
        [
            cp.sum(mu) == 1,
            weighted_plus << tau * np.eye(n),
            weighted_minus << tau * np.eye(n),
        ],
    )

    try:
        problem.solve(
            solver="CLARABEL",
            max_iter=500,
            tol_feas=1e-10,
            tol_gap_abs=1e-10,
            tol_gap_rel=1e-10,
        )
    except Exception as exc:
        return {
            "status": "exception",
            "error": str(exc),
            "witness": None,
        }

    witness = (
        verify_dual(bp, bm, mu.value, scale)
        if mu.value is not None else None
    )
    return {
        "status": str(problem.status),
        "reported_scaled_bound": (
            float(problem.value) if problem.value is not None else None
        ),
        "witness": witness,
    }


def primal_solve(bp, bm, scale, blocks):
    import cvxpy as cp

    count, n, _ = bp.shape
    zp = cp.Variable((n, n), PSD=True)
    zm = cp.Variable((n, n), PSD=True)
    t = cp.Variable()

    constraints = [cp.trace(zp) + cp.trace(zm) == 1]
    constraints.extend(
        cp.sum(cp.multiply(bp[i], zp))
        + cp.sum(cp.multiply(bm[i], zm)) >= t
        for i in range(count)
    )

    problem = cp.Problem(cp.Maximize(t), constraints)

    try:
        problem.solve(
            solver="CLARABEL",
            max_iter=500,
            tol_feas=1e-10,
            tol_gap_abs=1e-10,
            tol_gap_rel=1e-10,
        )
    except Exception as exc:
        return {"status": "exception", "error": str(exc)}, None

    row = {
        "status": str(problem.status),
        "reported_scaled_margin": (
            float(problem.value) if problem.value is not None else None
        ),
    }

    if zp.value is None or zm.value is None:
        return row, None

    vplus = (np.asarray(zp.value) + np.asarray(zp.value).T) / 2
    vminus = (np.asarray(zm.value) + np.asarray(zm.value).T) / 2
    values = (
        np.einsum("pij,ji->p", bp, vplus)
        + np.einsum("pij,ji->p", bm, vminus)
    )

    eigp, qp = np.linalg.eigh(vplus)
    eigm, qm = np.linalg.eigh(vminus)

    row.update({
        "independent_min_scaled_margin": float(np.min(values)),
        "z_plus_min_eigenvalue": float(eigp[0]),
        "z_minus_min_eigenvalue": float(eigm[0]),
        "trace_sum": float(np.trace(vplus) + np.trace(vminus)),
    })

    # Only one real source vector per physical canonical sector.
    up = np.sqrt(max(float(eigp[-1]), 0)) * qp[:, -1]
    um = np.sqrt(max(float(eigm[-1]), 0)) * qm[:, -1]

    coeff_plus = blocks[1]["w"] @ up
    coeff_minus = blocks[-1]["w"] @ um

    rank_one = (
        np.einsum(
            "i,pij,j->p",
            coeff_plus, blocks[1]["a"], coeff_plus
        )
        -
        np.einsum(
            "i,pij,j->p",
            coeff_minus, blocks[-1]["a"], coeff_minus
        )
    )

    rank_one_energy = (
        float(coeff_plus @ blocks[1]["h"] @ coeff_plus)
        + float(coeff_minus @ blocks[-1]["h"] @ coeff_minus)
    )
    minimum = float(np.min(rank_one))

    row.update({
        "rank_one_min_acceleration_per_unit_source_m_s2": minimum,
        "rank_one_canonical_energy_j": rank_one_energy,
        "rank_one_required_field_j_fine_grid": (
            TARGET_G * rank_one_energy / minimum
            if minimum > 0 else None
        ),
        "rank_one_positive": minimum > 0,
    })

    return (
        row,
        (coeff_plus, coeff_minus) if minimum > 0 else None,
    )


def cross_grid_transfer(grids, private_by_h, coeffs):
    """One shell source profile: same raw amplitudes on every grid."""
    h0 = min(private_by_h)
    fine = private_by_h[h0]
    modes = fine["modes"]
    ids = fine["indices"]

    raw = []
    for lane in coeffs:
        raw.append(np.array([
            lane[j] / math.sqrt(
                modes[i]["unscaled_source_vacuum_j"]
            )
            for j, i in enumerate(ids)
        ]))

    records = []

    for info in grids:
        h = info["h_m"]
        p = private_by_h[h]

        raw_coef = []
        for lane in raw:
            raw_coef.append(np.array([
                lane[j] * math.sqrt(
                    p["modes"][i]["unscaled_source_vacuum_j"]
                )
                for j, i in enumerate(p["indices"])
            ]))

        x, y = raw_coef
        a1 = p["blocks"][1]["a"]
        a2 = p["blocks"][-1]["a"]
        h1 = p["blocks"][1]["h"]
        h2 = p["blocks"][-1]["h"]

        acceleration = (
            np.einsum("i,pij,j->p", x, a1, x)
            -
            np.einsum("i,pij,j->p", y, a2, y)
        )
        energy = float(x @ h1 @ x + y @ h2 @ y)

        density = None
        for sign, coef in ((1, x), (-1, y)):
            resp = p["blocks"][sign]["response"]
            selected = p["indices"]

            er = np.tensordot(
                coef, resp["e_r"][selected], axes=(0, 0)
            )
            ez = np.tensordot(
                coef, resp["e_z"][selected], axes=(0, 0)
            )
            br = np.tensordot(
                coef, resp["b_r"][selected], axes=(0, 0)
            )
            bz = np.tensordot(
                coef, resp["b_z"][selected], axes=(0, 0)
            )

            term = sign * (er*br + ez*bz)
            density = term if density is None else density + term

        sigma = (
            -2 * HBAR_C_EV_M**2
            / REFERENCE_PORTAL_SCALE_EV**4
        ) * density

        max_sigma = float(np.max(np.abs(
            sigma[p["setup"]["field"]["payload"]]
        )))

        records.append({
            "grid_h_m": h,
            "unscaled_min_acceleration_m_s2": float(
                np.min(acceleration)
            ),
            "unscaled_field_energy_j": energy,
            "unscaled_sigma_max": max_sigma,
            "coeff_plus": x,
            "coeff_minus": y,
        })

    min_acc = min(
        r["unscaled_min_acceleration_m_s2"]
        for r in records
    )

    if min_acc <= 0:
        return {
            "common_source_outward": False,
            "grid_summary": [
                {
                    "grid_h_m": r["grid_h_m"],
                    "min_a_m_s2":
                        r["unscaled_min_acceleration_m_s2"],
                }
                for r in records
            ],
        }

    factor = TARGET_G / min_acc

    eligible = all(
        r["unscaled_field_energy_j"] * factor < BUDGET_J
        and 4 * r["unscaled_sigma_max"] * factor < 1e-8
        for r in records
    )

    checks = []

    if eligible:
        for record in records:
            p = private_by_h[record["grid_h_m"]]

            for sign, source_coeff in (
                (1, record["coeff_plus"]),
                (-1, record["coeff_minus"]),
            ):
                checks.append({
                    "grid_h_m": record["grid_h_m"],
                    "sector": sign,
                    **direct_full_sparse_check(
                        p,
                        source_coeff * math.sqrt(factor),
                        sign,
                    ),
                })

    return {
        "common_source_outward": True,
        "rescale_energy_factor": factor,
        "grid_summary": [
            {
                "grid_h_m": r["grid_h_m"],
                "min_a_m_s2": (
                    r["unscaled_min_acceleration_m_s2"] * factor
                ),
                "canonical_field_energy_j": (
                    r["unscaled_field_energy_j"] * factor
                ),
                "max_relative_nonlinear_beta_change_upper": (
                    float(math.expm1(
                        4 * r["unscaled_sigma_max"] * factor
                    ))
                    if 4 * r["unscaled_sigma_max"] * factor < 50
                    else math.inf
                ),
            }
            for r in records
        ],
        "field_budget_screen_both_grids": eligible,
        "independent_full_sparse_checks": checks,
        "constructive_numerical_pass": bool(
            eligible and checks and all(c["pass"] for c in checks)
        ),
    }


def direct_full_sparse_check(private, coeff, sign):
    base = private["setup"]
    modes = private["modes"]
    ids = private["indices"]

    phi = np.zeros_like(base["phi0"])
    av = np.zeros_like(base["a0"])

    for amplitude, index in zip(coeff, ids):
        phi += amplitude * modes[index]["phi"]
        av += amplitude * modes[index]["a_phi"]

    phi_vec = phi[1:-1, :-1].reshape(-1)
    a_vec = av[1:-1, 1:-1].reshape(-1)

    prep = dict(base["prep"])
    prep["phi0_vec"] = phi_vec
    prep["a0_vec"] = a_vec

    prep["c_a0"] = np.asarray(
        prep["c_active"] @ a_vec
    ).reshape(-1)

    prep["d_phi0"] = np.asarray(
        prep["d_active"] @ phi_vec
    ).reshape(-1)

    local = {
        **base,
        "prep": prep,
        "phi0": phi,
        "a0": av,
    }

    woodbury = _solve_loaded(prep, 1.0, float(sign))

    if not woodbury["success"]:
        return {
            "pass": False,
            "reason": "woodbury_failed",
        }

    comparison = _direct_compare(
        local, woodbury, 1.0, float(sign)
    )

    return {
        "pass": bool(comparison["pass"]),
        "vector_relative_difference":
            comparison["vector_relative_difference"],
        "acceleration_absolute_difference_m_s2":
            comparison[
                "minimum_acceleration_absolute_difference_m_s2"
            ],
        "field_energy_relative_difference":
            comparison["field_energy_relative_difference"],
    }


def run_all():
    gate = algebra_gate()
    ward = source_ward_gate()

    if not ward["net_charge_zero_pass"]:
        raise RuntimeError(
            "shell source charge conservation check failed"
        )

    if not gate["pass"]:
        raise RuntimeError(
            "cross-field action normalization failed"
        )

    grids = []
    private_by_h = {}

    for h in GRIDS:
        info, private = source_grid(h)

        dual = dual_solve(
            private["bp"],
            private["bm"],
            private["scale"],
        )

        primal, candidate = primal_solve(
            private["bp"],
            private["bm"],
            private["scale"],
            private["blocks"],
        )

        info["dual"] = dual
        info["primal"] = primal
        private["candidate"] = candidate

        grids.append(info)
        private_by_h[h] = private

    fine = private_by_h[min(GRIDS)]["candidate"]

    transfer = (
        cross_grid_transfer(grids, private_by_h, fine)
        if fine is not None
        else {
            "common_source_outward": False,
            "reason": "no_rank_one_fine_grid_candidate",
        }
    )

    dual_excluded = all(
        g["dual"]["witness"] is not None
        and g["dual"]["witness"]["energy_bound"][2][
            "one_g_excluded_below_10mj"
        ]
        for g in grids
    )

    if transfer.get("constructive_numerical_pass"):
        decision = (
            "YELLOW_CONSTRUCTIVE_CROSS_SIGN_TWO_LANE_"
            "FROZEN_BETA_PREMODEL"
        )
        nxt = (
            "R3X3B_MICROSCOPIC_SOURCE_PARITY_"
            "NOETHER_AND_CONTINUUM"
        )
    elif dual_excluded:
        decision = (
            "GREEN_SCOPED_NEW_CROSS_SIGN_SHELL_CONE_"
            "ENERGY_EXCLUDED_BOTH_GRIDS"
        )
        nxt = (
            "R3X3B_NEW_INTERFACE_OPERATOR_"
            "PROVENANCE_PREFLIGHT"
        )
    else:
        decision = (
            "YELLOW_CROSS_SIGN_CONE_UNRESOLVED__"
            "NO_FALSE_PROMOTION"
        )
        nxt = (
            "R3X3B_TARGETED_INTERFACE_MODE_"
            "OR_SOURCE_ACTION_GATE"
        )

    return {
        "branch": BRANCH,
        "action_gate": gate,
        "source_ward_gate": ward,
        "grids": grids,
        "cross_grid": transfer,
        "decision": decision,
        "next": nxt,
        "source_family":
            "ideal_shell_ell_1_2_3_two_canonical_opposite_sign_lanes",
        "physical_U1_XY_cross_topological_diagonalization": True,
        "same_action_nonlinear_metric_noether_proven": False,
        "microscopic_axial_source_anomaly_canceled": False,
        "full_interacting_stability_proven": False,
        "continuum_certified": False,
        "complete_energy_established": False,
        "certified_sub10mj_model_found": False,
        "physical_antigravity_model_found": False,
        "006d_replaced": False,
    }
