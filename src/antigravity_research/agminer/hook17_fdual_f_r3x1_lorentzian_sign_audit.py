"""R3X1: Lorentzian two-U(1) topological-action sign audit.

The positive-K equations for the standard Lorentzian static Maxwell action
have opposite weighted cross-block signs. This run audits that structure
against the R3C1 positive-K symmetric calculation.

It uses the frozen-density-beta approximation from R3C1. The result is
diagnostic, not a full nonlinear or microscopic antigravity model.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.linalg import lu_factor, lu_solve
from scipy.sparse import bmat, diags
from scipy.sparse.linalg import spsolve

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    EV_J,
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
)

from .hook17_fdual_f_r3x0_cross_topological_gate import (
    algebra_ward_gate,
)


BRANCH = "032H17A12D1R3X1"

GRIDS_M = (
    0.075,
    0.050,
)

LAMBDA_VALUES = (
    0.0,
    1.0e-6,
    1.0e-5,
    3.0e-5,
    1.0e-4,
    1.0,
)

THETA_SIGNS = (
    1.0,
    -1.0,
)

ACTION_REL_TOL = 1.0e-12
DIRECT_VECTOR_REL_TOL = 1.0e-7
DIRECT_ACCEL_ABS_TOL = 1.0e-5
DIRECT_FIELD_ENERGY_REL_TOL = 1.0e-7
FULL_BETA_WEAK_SIGMA_LIMIT = 1.0e-8


def provenance_gate() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[3]
    data = root / "results" / "data"

    r3c1 = json.loads(
        (
            data
            / "032h17a12d1r3c1_hook17_fdual_f_exact_reciprocity_ultrasmall_summary.json"
        ).read_text(encoding="utf-8")
    )

    r3x0 = json.loads(
        (
            data
            / "032h17a12d1r3x0_cross_topological_equivalence_summary.json"
        ).read_text(encoding="utf-8")
    )

    passed = bool(
        r3c1.get(
            "full_variational_certificate_pass_all_grids"
        ) is True
        and r3x0.get(
            "algebra_ward_pass"
        ) is True
        and r3x0.get(
            "two_field_loaded_relabeling_pass"
        ) is True
        and r3x0.get(
            "006d_replaced"
        ) is False
    )

    return {
        "pass": passed,
        "earlier_discrete_symmetric_action_verified": True,
        "earlier_lorentzian_static_sign_certified": False,
    }


def constitutive_action_gate() -> dict[str, Any]:
    """Declare the Lorentzian action and exact constitutive sign.

    L = (E_X^2 + E_Y^2 - B_X^2 - B_Y^2)/2
        + theta (E_X.B_Y + E_Y.B_X)

    D_X = E_X + theta B_Y
    H_Y = B_Y - theta E_X

    For theta = -beta and R3C C = -grad(beta).B,
    positive-K Gauss has +C and positive-K Ampere has -D.
    """

    ward = algebra_ward_gate()

    return {
        "independent_u1_gauge_bianchi_pass":
            ward["independent_u1_ward_pass"],

        "field_redefinition_invariant":
            ward["full_redefinition_pass"],

        "polar_x_axial_y_parity_algebra_pass":
            ward["vector_axial_parity_algebra_pass"],

        "canonical_kinetic_eigenvalues":
            [1.0, 1.0],

        "static_lorentzian_lagrangian":
            (
                "0.5*(E_X2+E_Y2-B_X2-B_Y2)"
                "+theta*(E_X.B_Y+E_Y.B_X)"
            ),

        "constitutive_D_X":
            "E_X + theta B_Y",

        "constitutive_H_Y":
            "B_Y - theta E_X",

        "positive_K_gauss_offdiagonal_sign":
            1,

        "positive_K_ampere_offdiagonal_sign":
            -1,

        "static_lorentzian_hessian_diagonal_signs":
            [1, -1],

        "physicalized_parity_odd_source_current":
            False,

        "anomaly_cancellation_proven":
            False,

        "nonlinear_metric_action_rederived":
            False,
    }


def weighted_sign_certificate(
    field: dict[str, Any],
    prep: dict[str, Any],
) -> dict[str, Any]:
    """Verify the weighted Lorentzian static Hessian.

    Before multiplying the Ampere equation by minus one, the static
    action Hessian is symmetric:

        [ Wphi Kphi       Wphi C ]
        [ C^T Wphi      -Wa Ka  ]

    After rewriting both diagonals as positive K, the cross terms
    are skew-adjoint, not symmetric.
    """

    h = float(field["h"])
    nz = int(prep["operators"]["nz_inner"])

    w_phi_r = np.asarray(
        field["rhos"][:-1],
        dtype=float,
    ).copy()

    w_phi_r[0] = h / 8.0

    w_a_r = np.asarray(
        field["rhos"][1:-1],
        dtype=float,
    )

    wp = diags(
        np.tile(w_phi_r, nz),
        format="csr",
    )

    wa = diags(
        np.tile(w_a_r, nz),
        format="csr",
    )

    c = prep["coupling"]["c"]
    d = prep["coupling"]["d"]
    kp = prep["operators"]["k_phi"]
    ka = prep["operators"]["k_a"]

    skew_residual = (
        wa @ (-d) + c.T @ wp
    ).tocsr()

    old_symmetric_residual = (
        wa @ d - c.T @ wp
    ).tocsr()

    electric_residual = (
        wp @ kp - kp.T @ wp
    ).tocsr()

    magnetic_residual = (
        wa @ ka - ka.T @ wa
    ).tocsr()

    cross = wp @ c
    weighted_kp = wp @ kp
    weighted_ka = wa @ ka

    scale = max(
        (
            float(np.max(np.abs(cross.data)))
            if cross.nnz
            else 0.0
        ),
        float(np.max(np.abs(weighted_kp.data))),
        float(np.max(np.abs(weighted_ka.data))),
        1.0,
    )

    def maxabs(matrix):
        return (
            float(np.max(np.abs(matrix.data)))
            if matrix.nnz
            else 0.0
        )

    residuals = {
        "lorentzian_cross_antisymmetry":
            maxabs(skew_residual) / scale,

        "r3c1_positive_K_symmetry":
            maxabs(old_symmetric_residual) / scale,

        "electric_weighted_K":
            maxabs(electric_residual) / scale,

        "magnetic_weighted_K":
            maxabs(magnetic_residual) / scale,
    }

    return {
        "relative_residuals": residuals,

        "lorentzian_static_action_pass":
            bool(
                max(residuals.values())
                < ACTION_REL_TOL
            ),

        "corrected_positive_K_coupling_signs":
            [1, -1],

        "r3c1_positive_K_coupling_signs":
            [1, 1],

        "axis_scalar_radial_weight_h_over":
            8,

        "physical_source_action_fully_realized":
            False,
    }


def _solve_loaded(
    prep: dict[str, Any],
    lam: float,
    theta_sign: float,
) -> dict[str, Any]:
    """Woodbury solution of the physically signed static equations."""

    rp = len(
        prep["coupling"]["active_phi"]
    )

    ra = len(
        prep["coupling"]["active_a"]
    )

    reduced = np.eye(
        rp + ra,
        dtype=float,
    )

    reduced[:rp, rp:] = (
        lam
        * theta_sign
        * prep["c_green_a"]
    )

    reduced[rp:, :rp] = (
        -lam
        * theta_sign
        * prep["d_green_phi"]
    )

    condition = (
        float(np.linalg.cond(reduced))
        if lam != 0.0
        else 1.0
    )

    if (
        not math.isfinite(condition)
        or condition > 1.0e13
    ):
        return {
            "success": False,
            "condition_number": condition,
        }

    rhs = (
        -lam
        * theta_sign
        * np.concatenate(
            (
                prep["c_a0"],
                -prep["d_phi0"],
            )
        )
    )

    try:
        reduced_solution = lu_solve(
            lu_factor(reduced),
            rhs,
        )
    except (
        ValueError,
        np.linalg.LinAlgError,
    ):
        return {
            "success": False,
            "condition_number": condition,
        }

    delta_phi = (
        prep["green_phi"]
        @ reduced_solution[:rp]
    )

    delta_a = (
        prep["green_a"]
        @ reduced_solution[rp:]
    )

    residual_phi = (
        prep["operators"]["k_phi"] @ delta_phi
        + lam
        * theta_sign
        * (
            prep["coupling"]["c"]
            @ (prep["a0_vec"] + delta_a)
        )
    )

    residual_a = (
        prep["operators"]["k_a"] @ delta_a
        - lam
        * theta_sign
        * (
            prep["coupling"]["d"]
            @ (prep["phi0_vec"] + delta_phi)
        )
    )

    denominator = max(
        float(np.linalg.norm(prep["c_a0"])) * lam,
        float(np.linalg.norm(prep["d_phi0"])) * lam,
        1.0,
    )

    residual = max(
        float(np.linalg.norm(residual_phi)),
        float(np.linalg.norm(residual_a)),
    ) / denominator

    return {
        "success": True,
        "condition_number": condition,
        "delta_phi_vec": delta_phi,
        "delta_a_vec": delta_a,
        "relative_residual": residual,
    }


def _state(
    setup: dict[str, Any],
    solution: dict[str, Any],
) -> dict[str, Any]:
    field = setup["field"]

    phi, a_phi = _vectors_to_full_potentials(
        setup["prep"],
        field,
        setup["phi0"],
        setup["a0"],
        solution,
    )

    em = _fields_from_potentials(
        phi,
        a_phi,
        field["rho_grid"],
        float(field["h"]),
    )

    dot_eb = (
        em["e_rho"] * em["b_rho"]
        + em["e_z"] * em["b_z"]
    )

    sigma = (
        -2.0
        * HBAR_C_EV_M**2
        * dot_eb
        / REFERENCE_PORTAL_SCALE_EV**4
    )

    acceleration = (
        -C_LIGHT_M_S**2
        * np.gradient(
            sigma,
            float(field["h"]),
            axis=0,
            edge_order=2,
        )
    )

    payload = field["payload"]

    payload_indices = np.argwhere(payload)

    worst_j, worst_i = payload_indices[
        int(np.argmin(acceleration[payload]))
    ]

    volume = (
        2.0
        * math.pi
        * field["rho_grid"]
        * float(field["h"])**2
    )

    energy_density_twice = sum(
        em[key]**2
        for key in (
            "e_rho",
            "e_z",
            "b_rho",
            "b_z",
        )
    )

    energy_j = (
        0.5
        * float(np.sum(volume * energy_density_twice))
        / HBAR_C_EV_M
        * EV_J
    )

    sigma_max = float(
        np.max(np.abs(sigma[payload]))
    )

    nonlinear_beta_fraction = (
        abs(math.expm1(4.0 * sigma_max))
        if sigma_max < 100.0
        else math.inf
    )

    minimum_acceleration = float(
        np.min(acceleration[payload])
    )

    return {
        "minimum_payload_acceleration_m_s2":
            minimum_acceleration,

        "maximum_payload_acceleration_m_s2":
            float(np.max(acceleration[payload])),

        "worst_payload_rho_m":
            float(field["rho_grid"][worst_j, worst_i]),

        "worst_payload_z_m":
            float(field["z_grid"][worst_j, worst_i]),

        "canonical_field_energy_j":
            energy_j,

        "max_abs_sigma_on_payload":
            sigma_max,

        "max_beta_relative_nonlinear_correction":
            nonlinear_beta_fraction,

        "weak_sigma_self_consistency":
            bool(
                nonlinear_beta_fraction
                < FULL_BETA_WEAK_SIGMA_LIMIT
            ),

        "whole_payload_meets_one_g_floor":
            bool(
                minimum_acceleration
                >= TARGET_ACCELERATION_M_S2 - 1.0e-6
            ),

        "whole_payload_outward":
            bool(minimum_acceleration > 0.0),
    }


def _direct_compare(
    setup: dict[str, Any],
    woodbury: dict[str, Any],
    lam: float,
    theta_sign: float,
) -> dict[str, Any]:
    """Independently reconstruct the full sparse physical-sign system."""

    prep = setup["prep"]

    kp = prep["operators"]["k_phi"]
    ka = prep["operators"]["k_a"]

    c = prep["coupling"]["c"]
    d = prep["coupling"]["d"]

    full = bmat(
        [
            [kp, lam * theta_sign * c],
            [-lam * theta_sign * d, ka],
        ],
        format="csr",
    )

    rhs = (
        -lam
        * theta_sign
        * np.concatenate(
            (
                np.asarray(
                    c @ prep["a0_vec"]
                ).reshape(-1),
                -np.asarray(
                    d @ prep["phi0_vec"]
                ).reshape(-1),
            )
        )
    )

    direct = np.asarray(
        spsolve(full, rhs)
    ).reshape(-1)

    reference = np.concatenate(
        (
            woodbury["delta_phi_vec"],
            woodbury["delta_a_vec"],
        )
    )

    vector_error = float(
        np.linalg.norm(direct - reference)
        / max(np.linalg.norm(direct), 1.0)
    )

    direct_residual = float(
        np.linalg.norm(full @ direct - rhs)
        / max(np.linalg.norm(rhs), 1.0)
    )

    nphi = len(prep["phi0_vec"])

    direct_solution = {
        "success": True,
        "delta_phi_vec": direct[:nphi],
        "delta_a_vec": direct[nphi:],
    }

    state_direct = _state(
        setup,
        direct_solution,
    )

    state_woodbury = _state(
        setup,
        woodbury,
    )

    acceleration_error = abs(
        state_direct["minimum_payload_acceleration_m_s2"]
        - state_woodbury["minimum_payload_acceleration_m_s2"]
    )

    energy_error = (
        abs(
            state_direct["canonical_field_energy_j"]
            - state_woodbury["canonical_field_energy_j"]
        )
        / max(
            abs(state_direct["canonical_field_energy_j"]),
            1.0,
        )
    )

    return {
        "lambda": lam,
        "theta_sign": theta_sign,

        "vector_relative_difference":
            vector_error,

        "direct_relative_residual":
            direct_residual,

        "minimum_acceleration_absolute_difference_m_s2":
            acceleration_error,

        "field_energy_relative_difference":
            energy_error,

        "pass":
            bool(
                vector_error < DIRECT_VECTOR_REL_TOL
                and direct_residual < 1.0e-7
                and acceleration_error < DIRECT_ACCEL_ABS_TOL
                and energy_error < DIRECT_FIELD_ENERGY_REL_TOL
            ),
    }


def run_grid(h: float) -> dict[str, Any]:
    setup = _build_baseline_and_prep(float(h))

    certificate = weighted_sign_certificate(
        setup["field"],
        setup["prep"],
    )

    rows = []
    direct_checks = []

    for sign in THETA_SIGNS:
        for lam in LAMBDA_VALUES:
            solution = _solve_loaded(
                setup["prep"],
                lam,
                sign,
            )

            row = {
                "lambda": lam,
                "theta_sign": sign,
                "solve_success": solution["success"],
                "condition_number":
                    solution["condition_number"],
            }

            if solution["success"]:
                row.update(
                    _state(setup, solution)
                )

                row["relative_solve_residual"] = (
                    solution["relative_residual"]
                )

                if lam == 1.0:
                    direct_checks.append(
                        _direct_compare(
                            setup,
                            solution,
                            lam,
                            sign,
                        )
                    )

            rows.append(row)

    return {
        "h_m": float(h),
        "sign_certificate": certificate,
        "rows": rows,
        "direct_checks": direct_checks,
    }


def final_decision(
    provenance: dict[str, Any],
    action: dict[str, Any],
    grids: list[dict[str, Any]],
) -> dict[str, Any]:

    ward_pass = bool(
        action["independent_u1_gauge_bianchi_pass"]
        and action["field_redefinition_invariant"]
        and action["polar_x_axial_y_parity_algebra_pass"]
    )

    certificate_pass = all(
        grid["sign_certificate"][
            "lorentzian_static_action_pass"
        ]
        for grid in grids
    )

    direct_pass = all(
        check["pass"]
        for grid in grids
        for check in grid["direct_checks"]
    )

    solves_pass = all(
        row["solve_success"]
        and row.get(
            "relative_solve_residual",
            math.inf,
        ) < 1.0e-7
        for grid in grids
        for row in grid["rows"]
    )

    # The + sign corresponds to the declared theta=-beta convention.
    # The - sign is an independent convention/sensitivity audit.
    reference_full_rows = [
        row
        for grid in grids
        for row in grid["rows"]
        if row["lambda"] == 1.0
        and row["theta_sign"] == 1.0
    ]

    numerical_pass = bool(
        provenance["pass"]
        and ward_pass
        and certificate_pass
        and direct_pass
        and solves_pass
    )

    if not numerical_pass:
        result = (
            "RED_HOLD_R3X1_LORENTZIAN_SIGN_"
            "OR_SOLVER_CERTIFICATE_FAILED"
        )

        next_branch = (
            "REPAIR_R3X1_SIGN_AUDIT_"
            "BEFORE_INDEPENDENT_SOURCES"
        )

    elif all(
        row.get("whole_payload_meets_one_g_floor")
        and row.get("weak_sigma_self_consistency")
        and row.get(
            "canonical_field_energy_j",
            math.inf,
        ) < 100.0
        for row in reference_full_rows
    ):
        result = (
            "GREEN_SCOPED_R3X1_CORRECTED_LORENTZIAN_"
            "MIRROR_FULL_LOAD_SURVIVES"
        )

        next_branch = (
            "032H17A12D1R3X2_"
            "SOURCE_PARITY_AND_COMPLETE_ACTION_GATE"
        )

    else:
        result = (
            "GREEN_THEOREM_YELLOW_R3X1_LORENTZIAN_"
            "SIGN_RECONSTRUCTED_BUT_FULL_LOAD_NOT_CERTIFIED"
        )

        next_branch = (
            "032H17A12D1R3X2_"
            "INDEPENDENT_SOURCE_CONE_WITH_PHYSICAL_SIGN"
        )

    return {
        "decision": result,
        "next": next_branch,

        "lorentzian_sign_and_direct_solver_pass":
            numerical_pass,

        "reference_portal_sign_full_loading_meets_one_g":
            all(
                row.get("whole_payload_meets_one_g_floor")
                for row in reference_full_rows
            ),

        "reference_portal_sign_full_loading_weak_sigma":
            all(
                row.get("weak_sigma_self_consistency")
                for row in reference_full_rows
            ),

        "reinterprets_r3c1_positive_K_symmetric_hessian_as_lorentzian_static_action":
            False,

        "independent_microscopic_source_realized":
            False,

        "full_metric_noether_completed":
            False,

        "interacting_stability_certified":
            False,

        "complete_energy_established":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "006d_replaced":
            False,
    }
