"""032H17A12D1R3X0 — canonical two-U(1) cross-topological theorem gate.

Goal
----
Decide whether replacing the single-U(1) portal with

    sigma = (F_X . dual(F_Y))/M**4

actually supplies a new healthy, backreaction-compatible low-energy mechanism.

Kinetic action: -1/4 (F_X**2 + F_Y**2). The mixed invariant is

    F_X . dual(F_Y) = -2 (E_X.B_Y + E_Y.B_X).

Using A_+/-=(A_X +/- A_Y)/sqrt(2), the mixed invariant is exactly

    (F_+ . dual(F_+) - F_- . dual(F_-))/2.

Consequently sigma is a positive and a negative copy of the original
R3A linear topological portal; both Maxwell kinetic terms remain healthy.

For the parity completion in which X is polar and Y axial, parity exchanges
the +/- channels while preserving the total cross portal.

A single populated cross pair (Phi_X,A_Y) has precisely the R3C/R3C1 loaded
block. Splitting that mirror between (Phi_X,A_Y) and (Phi_Y,A_X) retains the
same field energy, metric observable, and bad interface morphology.

Genuinely independent source profiles or new same-action physics remain open.

This run does not prove anomaly cancellation, physical microscopic sources,
complete energy, or a physical antigravity model.
"""

from __future__ import annotations

import json
import math
from itertools import permutations
from pathlib import Path
from typing import Any

import numpy as np

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    HBAR_C_EV_M,
    REFERENCE_PORTAL_SCALE_EV,
    TARGET_ACCELERATION_M_S2,
)
from .hook17_fdual_f_loaded_payload_homotopy import (
    _fields_from_potentials,
    _vectors_to_full_potentials,
)
from .hook17_fdual_f_r3c1_validation import (
    _build_baseline_and_prep,
    _state_for_loading,
    full_variational_certificate,
)


BRANCH = "032H17A12D1R3X0"

GRIDS_M = (0.075, 0.050)
LOADING_FRACTIONS = (0.0, 1.0e-6, 1.0e-5, 3.0e-5, 1.0)
SOURCE_SPLITS = (0.0, 0.25, 0.5, 1.0)

IDENTITY_TOL = 5.0e-13
SOLVER_REL_TOL = 1.0e-8
SPLIT_OBSERVABLE_REL_TOL = 1.0e-10


def provenance_gate() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[3]
    data = root / "results" / "data"

    r3c1 = json.loads(
        (
            data
            / "032h17a12d1r3c1_hook17_fdual_f_exact_reciprocity_ultrasmall_summary.json"
        ).read_text(encoding="utf-8")
    )

    r3d0 = json.loads(
        (
            data
            / "032h17a12d1r3d0_hook17_node_integrability_summary.json"
        ).read_text(encoding="utf-8")
    )

    passed = bool(
        r3c1.get("full_variational_certificate_pass_all_grids") is True
        and r3c1.get("direct_vs_woodbury_pass_original_grids") is True
        and r3d0.get("authorize_cross_topological_r3x0") is True
        and r3d0.get("authorize_single_field_loaded_r3d1") is False
        and r3d0.get("006d_replaced") is False
    )

    return {
        "pass": passed,
        "r3d0_decision": r3d0.get("decision"),
        "r3c1_threshold_continuum_certified":
            r3c1.get("threshold_is_continuum_certified"),
    }


def dual_euclidean(f: np.ndarray) -> np.ndarray:
    """Algebraic 4-form dual for gauge and field-redefinition checks.

    Uses the Euclidean epsilon symbol. Physical E.B signs are checked
    separately, so no Lorentzian-energy claim is inferred from this helper.
    """
    if f.shape != (4, 4):
        raise ValueError("expected 4x4 field-strength tensor")

    result = np.zeros((4, 4), dtype=float)

    for indices in permutations(range(4)):
        inversions = sum(
            indices[i] > indices[j]
            for i in range(4)
            for j in range(i + 1, 4)
        )
        a, b, c, d = indices
        sign = -1.0 if inversions % 2 else 1.0
        result[a, b] += 0.5 * sign * f[c, d]

    return result


def f_of_potential(k: np.ndarray, a: np.ndarray) -> np.ndarray:
    """Fourier field strength invariant under A -> A + k alpha."""
    return np.outer(k, a) - np.outer(a, k)


def algebra_ward_gate() -> dict[str, Any]:
    """Independent U(1) gauge/Bianchi and parity/invariant identities."""
    kx = np.array([1.2, -0.7, 2.1, 0.3])
    ky = np.array([-0.4, 0.6, 1.3, 1.7])
    ax = np.array([0.2, 0.9, -1.1, 0.4])
    ay = np.array([-0.6, 0.1, 0.8, 1.5])

    fx = f_of_potential(kx, ax)
    fy = f_of_potential(ky, ay)

    gauge_x = f_of_potential(kx, ax + 2.3 * kx)
    gauge_y = f_of_potential(ky, ay - 0.7 * ky)

    bianchi_x = float(
        np.max(np.abs(kx @ dual_euclidean(fx)))
    )
    bianchi_y = float(
        np.max(np.abs(ky @ dual_euclidean(fy)))
    )

    gauge_error = max(
        float(np.max(np.abs(fx - gauge_x))),
        float(np.max(np.abs(fy - gauge_y))),
    )

    fp = (fx + fy) / math.sqrt(2.0)
    fm = (fx - fy) / math.sqrt(2.0)

    p_cross = float(np.sum(fx * dual_euclidean(fy)))
    p_rotated = 0.5 * float(
        np.sum(fp * dual_euclidean(fp))
        - np.sum(fm * dual_euclidean(fm))
    )

    invariant_rel = abs(p_cross - p_rotated) / max(
        abs(p_cross), abs(p_rotated), 1.0
    )

    energy_xy = float(np.sum(fx**2 + fy**2))
    energy_pm = float(np.sum(fp**2 + fm**2))

    energy_rel = abs(energy_xy - energy_pm) / max(
        energy_xy, 1.0
    )

    # X polar, Y axial:
    # E_X -> -E_X, B_X -> B_X,
    # E_Y -> E_Y,  B_Y -> -B_Y.
    ex = np.array([0.2, -0.7, 1.1])
    bx = np.array([1.3, 0.1, -0.3])
    ey = np.array([-0.4, 0.8, 0.9])
    by = np.array([0.5, -1.2, 0.6])

    before = float(ex @ by + ey @ bx)
    after = float((-ex) @ (-by) + ey @ bx)

    parity_rel = abs(before - after) / max(abs(before), 1.0)

    return {
        "gauge_x_residual": gauge_error,
        "bianchi_x_residual": bianchi_x,
        "bianchi_y_residual": bianchi_y,
        "mixed_self_duality_identity_relative": invariant_rel,
        "canonical_energy_rotation_relative": energy_rel,
        "assigned_vector_axial_parity_relative": parity_rel,
        "independent_u1_ward_pass": bool(
            max(gauge_error, bianchi_x, bianchi_y) < IDENTITY_TOL
        ),
        "full_redefinition_pass": bool(
            max(invariant_rel, energy_rel) < IDENTITY_TOL
        ),
        "vector_axial_parity_algebra_pass": bool(
            parity_rel < IDENTITY_TOL
        ),
        "axial_gauge_anomaly_canceled": False,
        "source_ward_realization_proven": False,
    }


def canonical_kinetic_gate() -> dict[str, Any]:
    """Canonical normalization with positive-definite kinetic mixing.

    Nonzero mixing is an algebraic diagnostic, not parity-allowed for
    an exact polar-X/axial-Y assignment.
    """
    rows = []

    for epsilon in (0.0, 0.2, 0.6, 0.9):
        kinetic = np.array([
            [1.0, epsilon],
            [epsilon, 1.0],
        ])

        eigen_k, basis_k = np.linalg.eigh(kinetic)

        if float(np.min(eigen_k)) <= 0.0:
            raise RuntimeError("unhealthy Maxwell kinetic matrix")

        inv_sqrt = (
            basis_k
            @ np.diag(1.0 / np.sqrt(eigen_k))
            @ basis_k.T
        )

        q = np.array([
            [0.0, 0.5],
            [0.5, 0.0],
        ])

        canonical_q = inv_sqrt @ q @ inv_sqrt
        eigen_q = np.linalg.eigvalsh(canonical_q)

        rows.append({
            "kinetic_mixing": epsilon,
            "minimum_kinetic_eigenvalue": float(eigen_k[0]),
            "canonical_portal_eigenvalues": [
                float(eigen_q[0]),
                float(eigen_q[1]),
            ],
            "one_positive_one_negative": bool(
                eigen_q[0] < 0.0 < eigen_q[1]
            ),
            "healthy_kinetic": True,
            "parity_allowed_when_x_polar_y_axial":
                bool(epsilon == 0.0),
        })

    return {
        "rows": rows,
        "passes": all(
            row["one_positive_one_negative"]
            for row in rows
        ),
        "negative_portal_eigenvalue_is_a_ghost": False,
    }


def loaded_block_rotation_gate() -> dict[str, Any]:
    """Exact four-field quadratic-action block rotation.

    Old order: Phi_X, A_Y, Phi_Y, A_X.
    New order: Phi_+, A_+, Phi_-, A_-.

    Two identical cross-coupled blocks transform into two self-topological
    blocks with opposite coupling signs.
    """
    ke = 2.0
    kb = 3.0
    c = 0.4
    lam = 0.73

    h = np.array([
        [ke, lam * c],
        [lam * c, kb],
    ])

    original = np.zeros((4, 4))
    original[:2, :2] = h
    original[2:, 2:] = h

    transform = np.array([
        [1.0, 0.0, 1.0, 0.0],
        [0.0, 1.0, 0.0, -1.0],
        [1.0, 0.0, -1.0, 0.0],
        [0.0, 1.0, 0.0, 1.0],
    ]) / math.sqrt(2.0)

    rotated = transform.T @ original @ transform

    expected = np.zeros((4, 4))
    expected[:2, :2] = h
    expected[2:, 2:] = [
        [ke, -lam * c],
        [-lam * c, kb],
    ]

    error = float(np.max(np.abs(rotated - expected)))
    orthogonality = float(
        np.max(np.abs(transform.T @ transform - np.eye(4)))
    )

    return {
        "relative_hessian_rotation_error":
            error / max(float(np.max(np.abs(expected))), 1.0),
        "orthogonality_error": orthogonality,
        "unloaded_kinetic_positive": bool(ke > 0.0 and kb > 0.0),
        "two_equal_cross_blocks_to_opposite_self_blocks_pass": bool(
            max(error, orthogonality) < IDENTITY_TOL
        ),
    }


def field_capacity_inequality_gate() -> dict[str, Any]:
    """Check |F_X dual F_Y| <= 2 u_Maxwell in the declared convention."""
    ex = np.array([1.2, -0.4, 2.1])
    ey = np.array([0.5, -1.4, 0.3])
    bx = np.array([-0.7, 0.9, -1.8])
    by = np.array([0.4, -0.2, 1.7])

    invariant = abs(-2.0 * float(ex @ by + ey @ bx))
    energy = 0.5 * sum(
        float(v @ v) for v in (ex, ey, bx, by)
    )

    e = np.array([1.0, 0.0, 0.0])
    saturated_invariant = abs(-2.0 * float(e @ e))
    saturated_energy = float(e @ e)

    ratio = saturated_invariant / (2.0 * saturated_energy)

    return {
        "test_invariant_magnitude": invariant,
        "test_twice_canonical_energy_density": 2.0 * energy,
        "saturating_ratio": ratio,
        "inequality_pass": bool(
            invariant <= 2.0 * energy + 1.0e-13
        ),
        "bound_saturation_pass": bool(
            abs(ratio - 1.0) < 1.0e-15
        ),
        "capacity_improvement_from_relabeling": False,
    }


def _split_operator_relative_residual(
    prep: dict[str, Any],
    solution: dict[str, Any],
    loading: float,
    fraction: float,
) -> float:
    """Check both separately sourced cross pairs satisfy the loaded BVP."""
    k_phi = prep["operators"]["k_phi"]
    k_a = prep["operators"]["k_a"]
    c = prep["coupling"]["c"]
    d = prep["coupling"]["d"]

    dphi = np.asarray(solution["delta_phi_vec"])
    da = np.asarray(solution["delta_a_vec"])

    phi0 = np.asarray(prep["phi0_vec"])
    a0 = np.asarray(prep["a0_vec"])

    scale = math.sqrt(float(fraction))

    rphi = (
        k_phi @ (scale * dphi)
        + loading * c @ (scale * (a0 + da))
    )
    ra = (
        k_a @ (scale * da)
        + loading * d @ (scale * (phi0 + dphi))
    )

    denominator = max(
        float(np.linalg.norm(k_phi @ (scale * dphi))),
        float(np.linalg.norm(k_a @ (scale * da))),
        float(np.linalg.norm(
            loading * c @ (scale * (a0 + da))
        )),
        float(np.linalg.norm(
            loading * d @ (scale * (phi0 + dphi))
        )),
        1.0,
    )

    return max(
        float(np.linalg.norm(rphi)),
        float(np.linalg.norm(ra)),
    ) / denominator


def split_mirror_identity(
    setup: dict[str, Any],
    loading: float,
    fraction: float,
    solved: tuple[dict[str, Any], dict[str, Any] | None] | None = None,
) -> dict[str, Any]:
    """Reconstruct X/Y potentials, cross invariant, energy and loading.

    Pair 1: (Phi_X, A_Y) = sqrt(f)*(Phi,A).
    Pair 2: (Phi_Y, A_X) = sqrt(1-f)*(Phi,A).

    The fields satisfy the two independent loaded same-action cross blocks.
    """
    solution, state = (
        solved
        if solved is not None
        else _state_for_loading(setup, loading)
    )

    if state is None or not solution["success"]:
        return {
            "lambda": loading,
            "split_fraction": fraction,
            "solve_success": False,
        }

    field = setup["field"]

    phi, a_phi = _vectors_to_full_potentials(
        setup["prep"],
        field,
        setup["phi0"],
        setup["a0"],
        solution,
    )

    normal = _fields_from_potentials(
        phi,
        a_phi,
        field["rho_grid"],
        field["h"],
    )

    s = math.sqrt(fraction)
    t = math.sqrt(1.0 - fraction)

    ex_r = s * normal["e_rho"]
    ex_z = s * normal["e_z"]
    ey_r = t * normal["e_rho"]
    ey_z = t * normal["e_z"]

    bx_r = t * normal["b_rho"]
    bx_z = t * normal["b_z"]
    by_r = s * normal["b_rho"]
    by_z = s * normal["b_z"]

    mixed = (
        ex_r * by_r
        + ex_z * by_z
        + ey_r * bx_r
        + ey_z * bx_z
    )

    single = (
        normal["e_rho"] * normal["b_rho"]
        + normal["e_z"] * normal["b_z"]
    )

    relative_p = (
        float(np.max(np.abs(mixed - single)))
        / max(float(np.max(np.abs(single))), 1.0e-50)
    )

    u_cross = 0.5 * sum(
        v**2
        for v in (
            ex_r, ex_z, ey_r, ey_z,
            bx_r, bx_z, by_r, by_z,
        )
    )

    u_single = 0.5 * sum(
        normal[key]**2
        for key in (
            "e_rho", "e_z", "b_rho", "b_z"
        )
    )

    relative_u = (
        float(np.max(np.abs(u_cross - u_single)))
        / max(float(np.max(np.abs(u_single))), 1.0e-50)
    )

    coefficient = (
        -2.0 * HBAR_C_EV_M**2
        / REFERENCE_PORTAL_SCALE_EV**4
    )

    sigma_cross = coefficient * mixed
    sigma_single = coefficient * single

    accel_cross = (
        -C_LIGHT_M_S**2
        * np.gradient(
            sigma_cross,
            field["h"],
            axis=0,
            edge_order=2,
        )
    )

    accel_single = (
        -C_LIGHT_M_S**2
        * np.gradient(
            sigma_single,
            field["h"],
            axis=0,
            edge_order=2,
        )
    )

    payload = field["payload"]

    relative_accel = (
        float(np.max(
            np.abs(accel_cross[payload] - accel_single[payload])
        ))
        / max(
            float(np.max(np.abs(accel_single[payload]))),
            1.0,
        )
    )

    residual_1 = _split_operator_relative_residual(
        setup["prep"], solution, loading, fraction
    )

    residual_2 = _split_operator_relative_residual(
        setup["prep"], solution, loading, 1.0 - fraction
    )

    return {
        "lambda": float(loading),
        "split_fraction": float(fraction),
        "solve_success": True,
        "original_min_acceleration_m_s2": float(
            state["minimum_payload_acceleration_m_s2"]
        ),
        "cross_min_acceleration_m_s2": float(
            np.min(accel_cross[payload])
        ),
        "original_field_energy_j": float(
            state["canonical_field_energy_j"]
        ),
        "mixed_invariant_relative_difference": relative_p,
        "maxwell_energy_density_relative_difference": relative_u,
        "payload_acceleration_relative_difference": relative_accel,
        "source_lane_1_relative_residual": residual_1,
        "source_lane_2_relative_residual": residual_2,
        "loaded_meets_one_g_floor": bool(
            np.min(accel_cross[payload])
            >= TARGET_ACCELERATION_M_S2 - 1.0e-7
        ),
        "mathematical_relabeling_identity_pass": bool(
            max(relative_p, relative_u, relative_accel)
            <= SPLIT_OBSERVABLE_REL_TOL
            and max(residual_1, residual_2) <= SOLVER_REL_TOL
        ),
    }


def run_grid(h: float) -> dict[str, Any]:
    setup = _build_baseline_and_prep(float(h))

    certificate = full_variational_certificate(
        setup["field"],
        setup["prep"],
    )

    rows = []

    for loading in LOADING_FRACTIONS:
        solved = _state_for_loading(setup, loading)

        for fraction in SOURCE_SPLITS:
            rows.append(
                split_mirror_identity(
                    setup, loading, fraction, solved
                )
            )

    return {
        "h_m": float(h),
        "full_weighted_action_certificate":
            certificate["complete_variational_same_action_pass"],
        "action_hessian_relative_residual":
            certificate["complete_hessian_relative_max_abs"],
        "rows": rows,
    }


def decision(
    results: list[dict[str, Any]],
    algebra: dict[str, Any],
    kinetic: dict[str, Any],
    capacity: dict[str, Any],
    block: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if block is None:
        block = loaded_block_rotation_gate()

    algebra_pass = bool(
        algebra["independent_u1_ward_pass"]
        and algebra["full_redefinition_pass"]
        and algebra["vector_axial_parity_algebra_pass"]
        and kinetic["passes"]
        and capacity["inequality_pass"]
        and capacity["bound_saturation_pass"]
        and block["two_equal_cross_blocks_to_opposite_self_blocks_pass"]
    )

    action_pass = all(
        item["full_weighted_action_certificate"]
        for item in results
    )

    split_rows = [
        row
        for grid in results
        for row in grid["rows"]
    ]

    split_pass = bool(split_rows) and all(
        row.get("mathematical_relabeling_identity_pass")
        for row in split_rows
    )

    sign_loss = all(
        any(
            math.isclose(
                row["lambda"],
                3.0e-5,
                rel_tol=0.0,
                abs_tol=1.0e-16,
            )
            and math.isclose(
                row["split_fraction"],
                0.5,
                rel_tol=0.0,
                abs_tol=1.0e-15,
            )
            and row.get(
                "cross_min_acceleration_m_s2",
                math.inf,
            ) < 0.0
            for row in grid["rows"]
        )
        for grid in results
    )

    if not algebra_pass or not action_pass or not split_pass:
        outcome = (
            "RED_HOLD_R3X0_IDENTITY_OR_SAME_ACTION_RECONSTRUCTION_FAILED"
        )
        next_branch = "REPAIR_R3X0_BEFORE_PHYSICAL_CLAIMS"

    elif sign_loss:
        outcome = (
            "GREEN_THEOREM_RED_NAIVE_CROSS_RELABELING__"
            "NO_CAPACITY_OR_LOADING_RESCUE"
        )
        next_branch = (
            "032H17A12D1R3X1_"
            "INDEPENDENT_SOURCE_AND_PARITY_WARD_FEASIBILITY"
        )

    else:
        outcome = (
            "YELLOW_R3X0_SIMPLE_MIRROR_COMPARISON_"
            "DID_NOT_REPLICATE_R3C1"
        )
        next_branch = (
            "AUDIT_R3X0_NORMALIZATION_AND_R3C1_BASELINE"
        )

    return {
        "decision": outcome,
        "next": next_branch,
        "algebra_ward_pass": algebra_pass,
        "weighted_same_action_pass": action_pass,
        "two_field_loaded_relabeling_pass": split_pass,
        "simple_cross_mirror_sign_loss_both_grids": sign_loss,
        "naive_cross_portal_is_new_field_capacity": False,
        "all_independent_two_field_sources_closed": False,
        "complete_energy_established": False,
        "parity_completed_microscopic_model_found": False,
        "source_ward_realization_proven": False,
        "physical_antigravity_model_found": False,
        "certified_sub10mj_model_found": False,
        "006d_replaced": False,
    }
