"""032H17A12D1R3X2R2 — independently reconstructed energy-budget dual gate.

Reason for this run
-------------------
R3X2R1 reported an independently reconstructed negative fine-grid shell-only
PSD-cone witness (about -1.49e-8), but its fixed -1e-6 acceptance threshold
rejected that witness. A nonnegative dual bound can also falsify a candidate
under a finite energy ceiling without proving an unlimited-energy no-go.

Let a_p = trace(A_p Z) be acceleration at each finite-payload node, and let
U_box = trace(H Z) be canonical Maxwell energy in the computed domain. For
Z positive semidefinite, and any payload weights mu_p >= 0, sum(mu)=1:

  min_p a_p <= sum_p mu_p a_p
          = trace((sum_p mu_p A_p) Z)
          <= gamma * U_box,

where gamma is the largest eigenvalue of the energy-whitened weighted form.
If gamma < 0, no nonzero PSD source combination yields outward acceleration
at all nodes, at any energy. If gamma >= 0 but gamma * 10MJ < 1g, no
candidate within the 10-MJ complete energy ceiling can satisfy all nodes,
because canonical field energy is a positive component of complete energy.

This test reconstructs the source matrices from R3X2, obtains a new dual
witness with Clarabel, verifies the bound independently by float64 eigensolve,
rotated Gershgorin, and 70-digit mpmath eigsy, and tests sensitivity to a
specified uniform spectral perturbation of all normalized node matrices.

Scoped limits
-------------
Finite sampled grids only; frozen-beta Lorentzian action; static axisymmetry;
original shell support; only ell=1..3 shell sources, with an R3B-augmented
diagnostic catalog. The relaxation allows arbitrary PSD rank, so a valid
exclusion also excludes its rank <= 2 physical two-lane subset. There is no
continuum/input interval error bound, microscopic source, exact nonlinear
metric Noether identity, anomaly cancellation, stability, or complete energy
certification. Numerical witnesses are NOT general antigravity no-go theorems.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np

BRANCH = "032H17A12D1R3X2R2"
GRID_SPACINGS_M = (0.075, 0.050)
BUDGET_J = 10_000_000.0
TARGET_G = 9.80665
PERTURBATION_SPECTRAL_NORM = (0.0, 1e-10, 1e-9, 1e-8)
SAFE_MARGIN_FRACTION = 0.05
SOURCE_RESIDUAL_TOL = 1e-7
WHITEN_IDENTITY_TOL = 3e-6
SIMPLEX_RAW_TOL = 1e-4


def provenance_gate() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[3] / "results" / "data"
    previous = json.loads(
        (
            root
            / "032h17a12d1r3x2r1_dual_certificate_summary.json"
        ).read_text(encoding="utf-8")
    )

    passed = (
        previous.get("branch") == "032H17A12D1R3X2R1"
        and previous.get(
            "declared_shell_cone_dual_excluded_both_grids"
        ) is False
        and previous.get("physical_antigravity_model_found") is False
        and previous.get("006d_replaced") is False
        and len(previous.get("grids", [])) == 2
    )

    return {
        "pass": bool(passed),
        "previous_decision": previous.get("decision"),
    }


def _simplex(
    mu_raw: np.ndarray,
) -> tuple[np.ndarray, dict[str, Any]]:
    raw = np.asarray(mu_raw, dtype=float).reshape(-1)

    if not np.all(np.isfinite(raw)):
        raise ValueError("nonfinite dual weights")

    if raw.size == 0:
        raise ValueError("empty dual weights")

    raw_sum = float(np.sum(raw))
    raw_min = float(np.min(raw))

    if (
        abs(raw_sum - 1.0) > SIMPLEX_RAW_TOL
        or raw_min < -SIMPLEX_RAW_TOL
    ):
        raise ValueError("dual solution too far outside simplex")

    nonnegative = np.maximum(raw, 0.0)
    total = float(np.sum(nonnegative))

    if total <= 0.0:
        raise ValueError("zero normalized dual weight")

    mu = nonnegative / total

    assert np.min(mu) >= 0
    assert abs(float(np.sum(mu)) - 1) < 5e-15

    return mu, {
        "raw_min": raw_min,
        "raw_sum": raw_sum,
        "negative_weight_mass_clipped": float(
            np.sum(np.maximum(-raw, 0.0))
        ),
    }


def independent_spectrum(
    forms: np.ndarray,
    weights: np.ndarray,
) -> dict[str, Any]:
    """Check the represented weighted symmetric form in three ways."""
    a = np.asarray(forms, dtype=float)
    mu, simplex = _simplex(weights)

    if (
        a.ndim != 3
        or a.shape[0] != len(mu)
        or a.shape[1] != a.shape[2]
    ):
        raise ValueError("malformed dual matrices")

    n = a.shape[1]

    matrix = np.einsum(
        "p,pij->ij",
        mu,
        a,
        optimize=True,
    )

    asymmetry = float(
        np.max(np.abs(matrix - matrix.T))
    )

    matrix = 0.5 * (matrix + matrix.T)

    eigs, q = np.linalg.eigh(matrix)

    rotated = q.T @ matrix @ q

    radii = (
        np.sum(np.abs(rotated), axis=1)
        - np.abs(np.diag(rotated))
    )

    gershgorin_upper = float(
        np.max(np.diag(rotated) + radii)
    )

    import mpmath as mp

    with mp.workdps(70):
        exact_stored_matrix = mp.matrix([
            [
                mp.mpf(float(matrix[i, j]))
                for j in range(n)
            ]
            for i in range(n)
        ])

        mp_eigs, _ = mp.eigsy(exact_stored_matrix)
        mp_largest = float(mp_eigs[n - 1])

    float_largest = float(eigs[-1])

    # A transparent arithmetic cushion, NOT a formal interval
    # bound on physical input matrices or continuum discretization.
    arithmetic_cushion = max(
        256
        * np.finfo(float).eps
        * n
        * max(float(np.max(np.abs(matrix))), 1e-12),
        1e-14,
    )

    conservative_upper = (
        max(
            float_largest,
            mp_largest,
            gershgorin_upper,
        )
        + arithmetic_cushion
    )

    return {
        **simplex,
        "valid_reconstructed_simplex": True,
        "max_form_asymmetry": asymmetry,
        "eigenvalue_float64": float_largest,
        "eigenvalue_mpmath_70dps": mp_largest,
        "gershgorin_rotated_upper": gershgorin_upper,
        "arithmetic_cushion_heuristic": arithmetic_cushion,
        "conservative_upper_scaled_per_j": conservative_upper,
        "numerical_interval_proof": False,
        "largest_weights": [
            {
                "payload_index": int(i),
                "weight": float(mu[i]),
            }
            for i in np.argsort(mu)[::-1][:12]
            if mu[i] > 1e-8
        ],
    }


def budget_bound(
    upper_scaled: float,
    acceleration_per_joule_scale: float,
    budget_j: float = BUDGET_J,
    target_g: float = TARGET_G,
    perturb: float = 0.0,
) -> dict[str, Any]:
    """Conditional bound for ||delta B_p||_2 <= perturb at each node."""
    if (
        perturb < 0
        or acceleration_per_joule_scale <= 0
        or budget_j <= 0
    ):
        raise ValueError("invalid budget or perturbation")

    gamma = (
        float(upper_scaled) + perturb
    ) * acceleration_per_joule_scale

    if gamma <= 0:
        # Zero source has zero acceleration, so allowing U <= budget
        # gives maximum attainable minimum acceleration <= zero.
        cap_at_budget = 0.0
        lower_bound_j = None
        sign_impossible = True
    else:
        cap_at_budget = budget_j * gamma
        lower_bound_j = target_g / gamma
        sign_impossible = False

    return {
        "assumed_uniform_norm_perturbation": float(perturb),
        "dual_upper_accel_per_j": float(gamma),
        "max_min_acceleration_with_budget_m_s2": float(
            cap_at_budget
        ),
        "minimum_field_energy_lower_bound_j": lower_bound_j,
        "unlimited_energy_outward_excluded": sign_impossible,
        "field_budget_excludes_one_g_with_5pct_margin": bool(
            cap_at_budget
            < (1.0 - SAFE_MARGIN_FRACTION) * target_g
        ),
    }


def solve_dual_fresh(
    forms: np.ndarray,
) -> dict[str, Any]:
    """Build a new full simplex witness, never truncated JSON weights."""
    import cvxpy as cp

    count, n, _ = forms.shape

    mu = cp.Variable(count, nonneg=True)
    tau = cp.Variable()

    flat = np.transpose(
        forms,
        (1, 2, 0),
    ).reshape(n * n, count)

    weighted = cp.reshape(
        flat @ mu,
        (n, n),
        order="C",
    )

    problem = cp.Problem(
        cp.Minimize(tau),
        [
            cp.sum(mu) == 1,
            weighted << tau * np.eye(n),
        ],
    )

    try:
        problem.solve(
            solver=cp.CLARABEL,
            max_iter=500,
            tol_feas=1e-10,
            tol_gap_abs=1e-10,
            tol_gap_rel=1e-10,
        )
    except Exception as error:
        return {
            "status": "EXCEPTION",
            "error": repr(error),
            "witness": None,
        }

    if mu.value is None:
        return {
            "status": str(problem.status),
            "witness": None,
        }

    try:
        witness = independent_spectrum(
            forms,
            np.asarray(mu.value),
        )
    except (ValueError, np.linalg.LinAlgError) as error:
        return {
            "status": str(problem.status),
            "error": repr(error),
            "witness": None,
        }

    return {
        "status": str(problem.status),
        "solver_reported_upper": (
            float(problem.value)
            if problem.value is not None
            else None
        ),
        "witness": witness,
    }


def _energy_identity_error(
    matrix: np.ndarray,
) -> dict[str, Any]:
    h = 0.5 * (matrix + matrix.T)
    eig, vectors = np.linalg.eigh(h)

    maximum = float(np.max(eig))
    retained = eig > maximum * 1e-12

    if not np.any(retained):
        return {
            "pass": False,
            "relative_error": None,
            "all_modes_retained": False,
        }

    w = (
        vectors[:, retained]
        / np.sqrt(eig[retained])[None, :]
    )

    identity = w.T @ h @ w

    error = float(np.max(
        np.abs(identity - np.eye(identity.shape[0]))
    ))

    return {
        "pass": bool(error < WHITEN_IDENTITY_TOL),
        "relative_error": error,
        "all_modes_retained": bool(np.all(retained)),
        "minimum_eigenvalue": float(eig[0]),
        "condition_number": (
            float(eig[-1] / eig[0])
            if eig[0] > 0
            else None
        ),
    }


def run_grid(
    h: float,
) -> dict[str, Any]:
    from .hook17_fdual_f_r3x2_source_cone import (
        _build_baseline_and_prep,
        loaded_response_basis,
        quadratic_payload_matrices,
        source_modes,
    )
    from .hook17_fdual_f_r3x2r1_dual_certificate import (
        whiten_source_cone,
    )

    setup = _build_baseline_and_prep(float(h))
    modes = source_modes(setup)
    loaded = loaded_response_basis(setup, modes, lam=1.0)

    a, energy = quadratic_payload_matrices(
        setup,
        loaded,
    )

    output: dict[str, Any] = {
        "h_m": float(h),
        "payload_points": int(a.shape[0]),
        "loaded_source_residual": float(
            loaded["relative_source_residual"]
        ),
        "catalogs": {},
    }

    catalogs = (
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
    )

    for name, indices in catalogs:
        aa = a[:, indices][:, :, indices]
        hh = energy[np.ix_(indices, indices)]

        normalized = whiten_source_cone(aa, hh)
        forms = normalized.pop("normalized_forms")

        identity = _energy_identity_error(hh)
        solve = solve_dual_fresh(forms)
        witness = solve.get("witness")

        if witness is not None:
            points = np.argwhere(
                setup["field"]["payload"]
            )

            for item in witness["largest_weights"]:
                j, i = points[item["payload_index"]]

                item["rho_m"] = float(
                    setup["field"]["rho_grid"][j, i]
                )

                item["z_m"] = float(
                    setup["field"]["z_grid"][j, i]
                )

            budgets = [
                budget_bound(
                    witness["conservative_upper_scaled_per_j"],
                    float(
                        normalized["acceleration_per_joule_scale"]
                    ),
                    perturb=epsilon,
                )
                for epsilon in PERTURBATION_SPECTRAL_NORM
            ]
        else:
            budgets = []

        eligible = bool(
            witness is not None
            and identity["pass"]
            and identity["all_modes_retained"]
            and normalized["full_energy_rank_retained"]
            and output["loaded_source_residual"] < SOURCE_RESIDUAL_TOL
            and solve["status"] in (
                "optimal",
                "optimal_inaccurate",
            )
        )

        output["catalogs"][name] = {
            **normalized,
            "source_names": [
                modes[i]["name"]
                for i in indices
            ],
            "whiten_identity": identity,
            "new_dual_solve": solve,
            "budget_sensitivity": budgets,
            "eligible_for_numeric_scoped_certificate": eligible,
            "grid_10mj_exclusion_at_1e_minus_9_perturbation": (
                bool(
                    eligible
                    and budgets[2][
                        "field_budget_excludes_one_g_with_5pct_margin"
                    ]
                )
                if budgets
                else False
            ),
        }

    return output


def decide(
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    def eligible(h: float, name: str) -> bool:
        matches = [
            result
            for result in results
            if abs(result["h_m"] - h) < 1e-12
        ]

        if len(matches) != 1:
            return False

        return matches[0]["catalogs"][name].get(
            "grid_10mj_exclusion_at_1e_minus_9_perturbation",
            False,
        )

    shell_coarse = eligible(0.075, "shell_only")
    shell_fine = eligible(0.05, "shell_only")
    augmented_fine = eligible(
        0.05,
        "baseline_augmented_diagnostic",
    )

    if shell_coarse and shell_fine and augmented_fine:
        label = (
            "GREEN_SCOPED_R3X2R2_FIELD_BUDGET_DUAL_"
            "EXCLUDES_DECLARED_SHELL_CONE_BOTH_GRIDS_"
            "AND_AUGMENTED_FINE_GRID"
        )

        next_branch = (
            "032H17A12D1R3X3_"
            "NEW_SOURCE_PROVENANCE_PARITY_WARD_PREFLIGHT"
        )

    elif shell_fine and augmented_fine:
        label = (
            "YELLOW_SCOPED_R3X2R2_FINE_GRID_ONLY_"
            "BUDGET_EXCLUSION__NO_CONTINUUM_CLOSURE"
        )

        next_branch = (
            "AUDIT_R3X2R2_COARSE_GRID_DUAL_"
            "AND_DISCRETIZATION"
        )

    else:
        label = (
            "YELLOW_HOLD_R3X2R2_"
            "NO_RECONSTRUCTED_ENERGY_DUAL_CLOSURE"
        )

        next_branch = (
            "REPAIR_R3X2R2_DUAL_ACCURACY_"
            "BEFORE_SOURCE_CLAIMS"
        )

    return {
        "decision": label,
        "next": next_branch,
        "shell_only_10mj_excluded_coarse_grid": shell_coarse,
        "shell_only_10mj_excluded_fine_grid": shell_fine,
        "augmented_diagnostic_10mj_excluded_fine_grid":
            augmented_fine,
        "all_source_families_closed": False,
        "numerical_grid_level_only": True,
        "continuum_certified": False,
        "exact_interval_input_certified": False,
        "fully_microscopic_sources": False,
        "parity_anomaly_completed": False,
        "full_noether_metric_completed": False,
        "complete_energy_established": False,
        "physical_antigravity_model_found": False,
        "certified_sub10mj_model_found": False,
        "006d_replaced": False,
    }
