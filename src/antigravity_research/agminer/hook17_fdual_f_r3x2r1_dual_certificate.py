"""032H17A12D1R3X2R1: bounded primal-dual source-cone audit.

Replace the fragile homogeneous minimum-energy SDP with a bounded
energy-normalized maximin SDP. Independently optimize a dual payload
weighting and verify each witness using NumPy eigenvalues.

All closure claims are limited to the declared R3X2 shell source space,
grids, linear frozen-beta Lorentzian loading and retained energy subspace.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from .hook17_fdual_f_r3x2_source_cone import (
    GRIDS_M,
    SHELL_ORDERS,
    _build_baseline_and_prep,
    loaded_response_basis,
    quadratic_payload_matrices,
    source_modes,
)


BRANCH = "032H17A12D1R3X2R1"

EIGEN_REL_CUTOFF = 1.0e-12
DUAL_NEGATIVE_MARGIN = 1.0e-6
SIMPLEX_TOL = 1.0e-5
SOURCE_CONE_TOL = 1.0e-6


def prior_artifact() -> dict[str, Any]:
    path = (
        Path(__file__).resolve().parents[3]
        / "results"
        / "data"
        / "032h17a12d1r3x2_independent_source_cone_summary.json"
    )

    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    if not (
        data.get("source_support_ward_pass") is True
        and data.get("006d_replaced") is False
    ):
        raise RuntimeError(
            "R3X2 provenance gate failed"
        )

    return {
        "branch": data.get("branch"),
        "source_support_ward_pass": True,
        "prior_solver_diagnostics": [
            {
                "grid_h_m": grid.get("grid_h_m"),
                "catalogs": {
                    k: {
                        "status": v.get("status"),
                        "error": v.get("error"),
                    }
                    for k, v in grid.get(
                        "catalogs", {}
                    ).items()
                },
            }
            for grid in data.get("grids", [])
        ],
    }


def whiten_source_cone(
    a: np.ndarray,
    hmat: np.ndarray,
) -> dict[str, Any]:
    """Normalize actual Maxwell energy to Euclidean source norm."""

    if a.ndim != 3 or a.shape[1] != a.shape[2]:
        raise ValueError(
            "A must have shape (payload,n,n)"
        )

    if hmat.shape != (a.shape[1], a.shape[2]):
        raise ValueError(
            "energy matrix dimension mismatch"
        )

    hmat = 0.5 * (hmat + hmat.T)
    eig, vec = np.linalg.eigh(hmat)

    maximum = float(np.max(eig))
    minimum = float(np.min(eig))

    if not math.isfinite(maximum) or maximum <= 0:
        raise ValueError(
            "invalid energy Gram matrix"
        )

    if minimum < -1.0e-8 * maximum:
        raise ValueError(
            "Maxwell energy Gram has significantly "
            "negative eigenvalue"
        )

    retained = (
        eig > EIGEN_REL_CUTOFF * maximum
    )

    if not np.any(retained):
        raise ValueError(
            "empty positive Maxwell-energy subspace"
        )

    w = (
        vec[:, retained]
        /
        np.sqrt(eig[retained])[None, :]
    )

    transformed = np.einsum(
        "ir,pij,js->prs",
        w,
        a,
        w,
        optimize=True,
    )

    transformed = 0.5 * (
        transformed
        + np.swapaxes(transformed, 1, 2)
    )

    scale = float(
        np.max(np.abs(transformed))
    )

    if scale <= 0 or not math.isfinite(scale):
        raise ValueError(
            "all acceleration forms vanish "
            "or are nonfinite"
        )

    return {
        "normalized_forms": transformed / scale,
        "acceleration_per_joule_scale": scale,
        "energy_rank": int(np.count_nonzero(retained)),
        "original_source_rank": int(len(eig)),
        "full_energy_rank_retained": bool(
            np.all(retained)
        ),
        "minimum_energy_eigenvalue": minimum,
        "maximum_energy_eigenvalue": maximum,
        "retained_condition_number": float(
            np.max(eig[retained])
            / np.min(eig[retained])
        ),
    }


def verify_primal(
    b: np.ndarray,
    z: np.ndarray,
) -> dict[str, Any]:
    z = 0.5 * (z + z.T)
    values = np.linalg.eigvalsh(z)

    trace = float(np.trace(z))

    acceleration = np.einsum(
        "pij,ji->p",
        b,
        z,
        optimize=True,
    )

    return {
        "minimum_acceleration_scaled_per_j":
            float(np.min(acceleration)),
        "minimum_z_eigenvalue":
            float(np.min(values)),
        "trace_z": trace,
        "primal_psd_trace_check": bool(
            np.min(values) >= -SOURCE_CONE_TOL
            and abs(trace - 1.0) <= SOURCE_CONE_TOL
        ),
    }


def verify_dual(
    b: np.ndarray,
    weights: np.ndarray,
) -> dict[str, Any]:
    weights = np.asarray(
        weights,
        dtype=float,
    ).reshape(-1)

    if (
        len(weights) != len(b)
        or not np.all(np.isfinite(weights))
    ):
        return {"valid_simplex": False}

    raw_sum = float(np.sum(weights))
    minimum_raw = float(np.min(weights))

    if raw_sum <= 0:
        return {"valid_simplex": False}

    weights_clipped = np.maximum(
        weights,
        0.0,
    )

    weights_clipped /= np.sum(weights_clipped)

    weighted_form = np.tensordot(
        weights_clipped,
        b,
        axes=(0, 0),
    )

    eigen = np.linalg.eigvalsh(
        0.5 * (
            weighted_form
            + weighted_form.T
        )
    )

    largest = float(np.max(eigen))

    valid = bool(
        abs(raw_sum - 1.0) < SIMPLEX_TOL
        and minimum_raw > -SIMPLEX_TOL
    )

    order = np.argsort(
        weights_clipped
    )[::-1][:12]

    return {
        "valid_simplex": valid,
        "raw_weight_sum": raw_sum,
        "minimum_raw_weight": minimum_raw,
        "verified_dual_upper_scaled_per_j": largest,
        "strict_negative_dual_witness": bool(
            valid
            and largest < -DUAL_NEGATIVE_MARGIN
        ),
        "largest_weights": [
            {
                "payload_index": int(i),
                "weight": float(weights_clipped[i]),
            }
            for i in order
            if weights_clipped[i] > 1.0e-8
        ],
    }


def solve_bounded_maximin(
    b: np.ndarray,
    solver: str,
) -> dict[str, Any]:
    """Primal: max t, B_p:Z >= t, Z >= 0, trace Z=1."""

    import cvxpy as cp

    rank = b.shape[1]

    z = cp.Variable(
        (rank, rank),
        PSD=True,
    )

    t = cp.Variable()

    constraints = [
        cp.trace(z) == 1
    ]

    cone = [
        cp.sum(cp.multiply(b[i], z)) >= t
        for i in range(len(b))
    ]

    prob = cp.Problem(
        cp.Maximize(t),
        constraints + cone,
    )

    opts = (
        {
            "max_iter": 450,
            "tol_feas": 1.0e-9,
            "tol_gap_abs": 1.0e-9,
            "tol_gap_rel": 1.0e-9,
        }
        if solver == "CLARABEL"
        else {
            "eps": 1.0e-7,
            "max_iters": 50000,
        }
    )

    try:
        prob.solve(
            solver=solver,
            **opts,
        )
    except Exception as error:
        return {
            "solver": solver,
            "status": "EXCEPTION",
            "error": repr(error),
        }

    result: dict[str, Any] = {
        "solver": solver,
        "status": str(prob.status),
        "reported_maximin_margin_scaled_per_j": (
            float(prob.value)
            if prob.value is not None
            else None
        ),
    }

    if z.value is not None:
        result["primal"] = verify_primal(
            b,
            np.asarray(z.value),
        )

    if all(
        c.dual_value is not None
        for c in cone
    ):
        result["dual_from_primal"] = verify_dual(
            b,
            np.array([
                float(c.dual_value)
                for c in cone
            ]),
        )

    return result


def solve_independent_dual(
    b: np.ndarray,
    solver: str,
) -> dict[str, Any]:
    """Dual: min tau, sum(mu_p B_p) <= tau I, mu simplex."""

    import cvxpy as cp

    n_payload, rank, _ = b.shape

    mu = cp.Variable(
        n_payload,
        nonneg=True,
    )

    tau = cp.Variable()

    flat = np.transpose(
        b,
        (1, 2, 0),
    ).reshape(
        rank * rank,
        n_payload,
    )

    weighted = cp.reshape(
        flat @ mu,
        (rank, rank),
        order="C",
    )

    constraints = [
        cp.sum(mu) == 1,
        weighted << tau * np.eye(rank),
    ]

    prob = cp.Problem(
        cp.Minimize(tau),
        constraints,
    )

    opts = (
        {
            "max_iter": 450,
            "tol_feas": 1.0e-9,
            "tol_gap_abs": 1.0e-9,
            "tol_gap_rel": 1.0e-9,
        }
        if solver == "CLARABEL"
        else {
            "eps": 1.0e-7,
            "max_iters": 50000,
        }
    )

    try:
        prob.solve(
            solver=solver,
            **opts,
        )
    except Exception as error:
        return {
            "solver": solver,
            "status": "EXCEPTION",
            "error": repr(error),
        }

    result: dict[str, Any] = {
        "solver": solver,
        "status": str(prob.status),
        "reported_dual_upper_scaled_per_j": (
            float(prob.value)
            if prob.value is not None
            else None
        ),
    }

    if mu.value is not None:
        result["independently_verified_dual"] = verify_dual(
            b,
            np.asarray(mu.value),
        )

    return result


def audit_catalog(
    a: np.ndarray,
    hmat: np.ndarray,
) -> dict[str, Any]:
    white = whiten_source_cone(
        a,
        hmat,
    )

    b = white.pop(
        "normalized_forms"
    )

    primal = [
        solve_bounded_maximin(b, solver)
        for solver in ("CLARABEL", "SCS")
    ]

    dual = [
        solve_independent_dual(b, solver)
        for solver in ("CLARABEL", "SCS")
    ]

    candidates = [
        row["dual_from_primal"]
        for row in primal
        if "dual_from_primal" in row
    ] + [
        row["independently_verified_dual"]
        for row in dual
        if "independently_verified_dual" in row
    ]

    valid = [
        c
        for c in candidates
        if c.get("valid_simplex")
    ]

    best = min(
        valid,
        key=lambda x:
            x["verified_dual_upper_scaled_per_j"],
        default=None,
    )

    negative = bool(
        best
        and best["strict_negative_dual_witness"]
    )

    certified_scope = bool(
        negative
        and white["full_energy_rank_retained"]
    )

    return {
        **white,
        "primal_solves": primal,
        "independent_dual_solves": dual,
        "best_verified_dual": best,
        "finite_grid_declared_cone_outward_impossibility_certificate":
            certified_scope,
        "projected_cone_only_certificate":
            negative and not certified_scope,
        "numerical_tolerance_not_formal_interval_proof": True,
    }


def run_grid(
    h: float,
) -> dict[str, Any]:
    setup = _build_baseline_and_prep(
        float(h)
    )

    modes = source_modes(setup)

    response = loaded_response_basis(
        setup,
        modes,
        lam=1.0,
    )

    a, energy = quadratic_payload_matrices(
        setup,
        response,
    )

    catalogs = {}

    for name, indices in (
        (
            "shell_only",
            [
                i
                for i, mode in enumerate(modes)
                if mode["shell_source"]
            ],
        ),
        (
            "baseline_augmented_diagnostic",
            list(range(len(modes))),
        ),
    ):
        result = audit_catalog(
            a[:, indices][:, :, indices],
            energy[np.ix_(indices, indices)],
        )

        witness = result.get(
            "best_verified_dual"
        )

        if witness is not None:
            points = np.argwhere(
                setup["field"]["payload"]
            )

            for item in witness["largest_weights"]:
                j, i = points[
                    item["payload_index"]
                ]

                item["rho_m"] = float(
                    setup["field"]["rho_grid"][j, i]
                )

                item["z_m"] = float(
                    setup["field"]["z_grid"][j, i]
                )

        result["source_names"] = [
            modes[i]["name"]
            for i in indices
        ]

        catalogs[name] = result

    return {
        "h_m": float(h),
        "loaded_source_residual":
            response["relative_source_residual"],
        "payload_points": int(a.shape[0]),
        "catalogs": catalogs,
    }


def decide(
    grids: list[dict[str, Any]],
) -> dict[str, Any]:
    required = [
        grid["catalogs"]["shell_only"]
        for grid in grids
    ]

    fine = min(
        grids,
        key=lambda row: row["h_m"],
    )["catalogs"]["shell_only"]

    both = all(
        row[
            "finite_grid_declared_cone_outward_impossibility_certificate"
        ]
        for row in required
    )

    if both:
        label = (
            "GREEN_SCOPED_DUAL_NO_OUTWARD_SOURCE_"
            "IN_R3X2_SHELL_CONE_BOTH_GRIDS"
        )

        next_branch = (
            "032H17A12D1R3X3_"
            "SOURCE_PARITY_AND_FAMILY_EXTENSION_GATE"
        )

    elif fine[
        "finite_grid_declared_cone_outward_impossibility_certificate"
    ]:
        label = (
            "YELLOW_FINE_GRID_NUMERICAL_DUAL_EXCLUSION_ONLY__"
            "NO_CONTINUUM_CLAIM"
        )

        next_branch = (
            "032H17A12D1R3X3_"
            "SOURCE_PARITY_AND_FAMILY_EXTENSION_GATE"
        )

    else:
        label = (
            "YELLOW_R3X2R1_NO_STRICT_DUAL_CERTIFICATE__"
            "DO_NOT_CLOSE_SOURCE_CONE"
        )

        next_branch = (
            "AUDIT_R3X2R1_CONDITIONING_"
            "OR_FIND_CONSTRUCTIVE_SOURCE"
        )

    return {
        "decision": label,
        "next": next_branch,
        "declared_shell_cone_dual_excluded_both_grids": both,
        "genuinely_independent_source_families_all_closed": False,
        "parity_anomaly_completed": False,
        "microscopic_source_realized": False,
        "continuum_certified": False,
        "full_metric_noether_completed": False,
        "complete_energy_established": False,
        "physical_antigravity_model_found": False,
        "certified_sub10mj_model_found": False,
        "006d_replaced": False,
    }
