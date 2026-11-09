"""032H17A12D1R3X2 — Lorentzian independent-source PSD cone gate.

The corrected R3X1 loaded equations are linear in source amplitudes
when beta is frozen to the finite-payload density profile.

Finite-payload acceleration and canonical Maxwell field energy are
quadratic forms in those amplitudes.

Two independent gauge-pair lanes produce a sum of two rank-one PSD
source matrices. Relaxing rank <= 2 gives a necessary convex feasibility
screen in the declared finite source basis.

Any promising source must reconstruct into at most two actual lanes,
survive both grids with one physical source profile, and agree with an
independent full sparse solve.

The ideal spherical shell sources are mathematical source models.
This does not establish microscopic sources, interacting stability,
complete operating energy, or replacement of 006D.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.linalg import lu_factor, lu_solve
from scipy.special import eval_legendre

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    EV_J,
    HBAR_C_EV_M,
    REFERENCE_PORTAL_SCALE_EV,
    SOURCE_RADIUS_M,
    TARGET_ACCELERATION_M_S2,
)
from .hook17_fdual_f_loaded_payload_homotopy import (
    _fields_from_potentials,
)
from .hook17_fdual_f_r3c1_validation import (
    _build_baseline_and_prep,
)
from .hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    _solve_loaded,
    _state,
    _direct_compare,
    provenance_gate as _r3x1_prior_provenance,
    constitutive_action_gate,
)


BRANCH = "032H17A12D1R3X2"
GRIDS_M = (0.075, 0.050)
SHELL_ORDERS = (1, 2, 3)

TARGET_G = TARGET_ACCELERATION_M_S2
LOW_FIELD_SCREEN_J = 100.0
STRICT_COMPLETE_CEILING_J = 10_000_000.0

SOURCE_RESIDUAL_TOL = 1.0e-7
CONTROL_ACCEL_ABS_TOL = 1.0e-5
CONTROL_FIELD_ENERGY_ABS_TOL = 1.0e-7


def provenance_gate() -> dict[str, Any]:
    prior = _r3x1_prior_provenance()

    path = (
        Path(__file__).resolve().parents[3]
        / "results"
        / "data"
        / "032h17a12d1r3x1_lorentzian_sign_audit_summary.json"
    )

    data = json.loads(path.read_text(encoding="utf-8"))

    passed = bool(
        prior["pass"]
        and data.get(
            "lorentzian_sign_and_direct_solver_pass"
        ) is True
        and data.get(
            "reference_portal_sign_full_loading_meets_one_g"
        ) is False
        and data.get("006d_replaced") is False
    )

    return {
        "pass": passed,
        "r3x1_lorentzian_direct_verification_pass":
            data.get("lorentzian_sign_and_direct_solver_pass"),
        "r3x1_full_load_one_g":
            data.get("reference_portal_sign_full_loading_meets_one_g"),
    }


def shell_multipole(
    field: dict[str, Any],
    ell: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Continuous, nonmonopolar electric and magnetic shell modes.

    Outside the original source sphere, these are exact source-free
    harmonic multipoles. Interior regular continuations are joined
    continuously at the shell; jumps in derivatives provide idealized
    shell charges and azimuthal surface currents.
    """
    rho = np.asarray(field["rho_grid"], dtype=float)
    z = np.asarray(field["z_grid"], dtype=float)

    r = np.hypot(rho, z)
    r_safe = np.maximum(r, 1.0e-300)

    x = np.clip(z / r_safe, -1.0, 1.0)
    sin_theta = rho / r_safe

    radius = float(SOURCE_RADIUS_M)
    inside = r <= radius
    exterior_radius = np.maximum(r, radius)

    envelope = np.where(
        inside,
        (r / radius) ** ell,
        (radius / exterior_radius) ** (ell + 1),
    )

    p = eval_legendre(ell, x)
    dp = np.polynomial.legendre.Legendre.basis(
        ell
    ).deriv()(x)

    phi = envelope * p
    a_phi = envelope * sin_theta * dp / ell

    return phi, a_phi


def source_ward_gate() -> dict[str, Any]:
    """Idealized shell continuity and neutrality, not microscopic UV."""
    nodes, weights = np.polynomial.legendre.leggauss(64)

    net_flux = {
        str(ell): abs(float(np.dot(
            weights,
            eval_legendre(ell, nodes),
        )))
        for ell in SHELL_ORDERS
    }

    return {
        "shell_orders": list(SHELL_ORDERS),
        "shell_support_radius_m": float(SOURCE_RADIUS_M),
        "net_electric_charge_multipole_flux_residuals": net_flux,
        "net_charge_zero_pass":
            max(net_flux.values()) < 1.0e-12,
        "azimuthal_surface_current_divergence_zero_by_axisymmetry":
            True,
        "zero_electric_and_magnetic_monopole_source": True,
        "shell_surface_source_microphysicalized": False,
        "independent_axial_gauge_source_and_anomaly_canceled":
            False,
        "full_matter_metric_noether_ward_proven": False,
    }


def _inventory_j(
    field: dict[str, Any],
    e_r: np.ndarray,
    e_z: np.ndarray,
    b_r: np.ndarray,
    b_z: np.ndarray,
) -> float:
    volume = (
        2.0
        * math.pi
        * field["rho_grid"]
        * float(field["h"]) ** 2
    )

    integrand = e_r**2 + e_z**2 + b_r**2 + b_z**2

    return (
        0.5
        * float(np.sum(volume * integrand))
        * EV_J
        / HBAR_C_EV_M
    )


def source_modes(
    setup: dict[str, Any],
) -> list[dict[str, Any]]:
    """Build separate unit-J source amplitudes.

    The R3B control modes cannot promote a new-shell-source result.
    Shell electric and magnetic amplitudes remain independently sourced.
    """
    field = setup["field"]
    zero = np.zeros_like(setup["phi0"])

    raw = [
        ("control_R3B_e", setup["phi0"], zero, False),
        ("control_R3B_b", zero, setup["a0"], False),
    ]

    for ell in SHELL_ORDERS:
        phi, a_phi = shell_multipole(field, ell)

        raw.extend([
            (f"shell_l{ell}_e", phi, zero, True),
            (f"shell_l{ell}_b", zero, a_phi, True),
        ])

    modes = []

    for name, phi, a_phi, shell_only in raw:
        fields = _fields_from_potentials(
            phi,
            a_phi,
            field["rho_grid"],
            float(field["h"]),
        )

        energy = _inventory_j(
            field,
            fields["e_rho"],
            fields["e_z"],
            fields["b_rho"],
            fields["b_z"],
        )

        if not (
            math.isfinite(energy)
            and energy > 0.0
        ):
            raise RuntimeError(
                f"invalid source-mode inventory: {name}"
            )

        norm = math.sqrt(energy)

        modes.append({
            "name": name,
            "shell_source": shell_only,
            "phi": phi / norm,
            "a_phi": a_phi / norm,
            "unscaled_source_vacuum_j": energy,
        })

    return modes


def loaded_response_basis(
    setup: dict[str, Any],
    modes: list[dict[str, Any]],
    lam: float,
) -> dict[str, Any]:
    """One corrected Lorentzian factorization for all source modes."""
    field = setup["field"]
    prep = setup["prep"]

    rp = len(prep["coupling"]["active_phi"])
    ra = len(prep["coupling"]["active_a"])

    reduced = np.eye(rp + ra)
    reduced[:rp, rp:] = lam * prep["c_green_a"]
    reduced[rp:, :rp] = -lam * prep["d_green_phi"]

    phi_vec = np.column_stack([
        mode["phi"][1:-1, :-1].reshape(-1)
        for mode in modes
    ])

    a_vec = np.column_stack([
        mode["a_phi"][1:-1, 1:-1].reshape(-1)
        for mode in modes
    ])

    rhs = lam * np.vstack([
        -(prep["c_active"] @ a_vec),
        prep["d_active"] @ phi_vec,
    ])

    coefficients = lu_solve(
        lu_factor(reduced),
        rhs,
    )

    delta_phi = (
        prep["green_phi"]
        @ coefficients[:rp, :]
    )

    delta_a = (
        prep["green_a"]
        @ coefficients[rp:, :]
    )

    lhs_phi = (
        prep["operators"]["k_phi"] @ delta_phi
        + lam
        * prep["coupling"]["c"] @ (a_vec + delta_a)
    )

    lhs_a = (
        prep["operators"]["k_a"] @ delta_a
        - lam
        * prep["coupling"]["d"] @ (phi_vec + delta_phi)
    )

    residual = max(
        float(np.linalg.norm(lhs_phi)),
        float(np.linalg.norm(lhs_a)),
    ) / max(float(np.linalg.norm(rhs)), 1.0)

    if not math.isfinite(residual) or residual > SOURCE_RESIDUAL_TOL:
        raise RuntimeError(
            f"loaded source response residual too large: {residual}"
        )

    e_r = []
    e_z = []
    b_r = []
    b_z = []

    for j, mode in enumerate(modes):
        phi = mode["phi"].copy()
        a_phi = mode["a_phi"].copy()

        phi[1:-1, :-1] += delta_phi[:, j].reshape(
            prep["operators"]["nz_inner"],
            prep["nr_phi"],
        )

        a_phi[1:-1, 1:-1] += delta_a[:, j].reshape(
            prep["operators"]["nz_inner"],
            prep["nr_a"],
        )

        em = _fields_from_potentials(
            phi,
            a_phi,
            field["rho_grid"],
            float(field["h"]),
        )

        e_r.append(em["e_rho"])
        e_z.append(em["e_z"])
        b_r.append(em["b_rho"])
        b_z.append(em["b_z"])

    return {
        "lambda": lam,
        "relative_source_residual": residual,
        "e_r": np.asarray(e_r),
        "e_z": np.asarray(e_z),
        "b_r": np.asarray(b_r),
        "b_z": np.asarray(b_z),
    }


def quadratic_payload_matrices(
    setup: dict[str, Any],
    response: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray]:
    """Return acceleration A[p,i,j] and canonical energy H[i,j]."""
    field = setup["field"]
    e_r = response["e_r"]
    e_z = response["e_z"]
    b_r = response["b_r"]
    b_z = response["b_z"]

    n = len(e_r)
    payload = field["payload"]
    h = float(field["h"])

    volume = (
        2.0
        * math.pi
        * field["rho_grid"]
        * h**2
    )

    coefficient = (
        2.0
        * C_LIGHT_M_S**2
        * HBAR_C_EV_M**2
        / REFERENCE_PORTAL_SCALE_EV**4
    )

    acceleration_matrix = np.zeros((
        int(np.count_nonzero(payload)),
        n,
        n,
    ))

    energy_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(i, n):
            dot = 0.5 * (
                e_r[i] * b_r[j]
                + e_z[i] * b_z[j]
                + e_r[j] * b_r[i]
                + e_z[j] * b_z[i]
            )

            derivative_z = np.gradient(
                dot,
                h,
                axis=0,
                edge_order=2,
            )

            acceleration = (
                coefficient * derivative_z[payload]
            )

            acceleration_matrix[:, i, j] = acceleration
            acceleration_matrix[:, j, i] = acceleration

            eij = (
                e_r[i] * e_r[j]
                + e_z[i] * e_z[j]
                + b_r[i] * b_r[j]
                + b_z[i] * b_z[j]
            )

            value = (
                0.5
                * float(np.sum(volume * eij))
                * EV_J
                / HBAR_C_EV_M
            )

            energy_matrix[i, j] = value
            energy_matrix[j, i] = value

    return acceleration_matrix, energy_matrix


def direct_quadratic_check(
    setup: dict[str, Any],
    response: dict[str, Any],
    a: np.ndarray,
    hmat: np.ndarray,
    coeff: np.ndarray,
) -> dict[str, float | bool]:
    """Rebuild actual fields rather than trusting matrix contractions."""
    er = np.tensordot(
        coeff, response["e_r"], axes=(0, 0)
    )
    ez = np.tensordot(
        coeff, response["e_z"], axes=(0, 0)
    )
    br = np.tensordot(
        coeff, response["b_r"], axes=(0, 0)
    )
    bz = np.tensordot(
        coeff, response["b_z"], axes=(0, 0)
    )

    field = setup["field"]

    sigma = (
        -2.0
        * HBAR_C_EV_M**2
        * (er * br + ez * bz)
        / REFERENCE_PORTAL_SCALE_EV**4
    )

    measured = (
        -C_LIGHT_M_S**2
        * np.gradient(
            sigma,
            float(field["h"]),
            axis=0,
            edge_order=2,
        )[field["payload"]]
    )

    predicted = np.einsum(
        "i,pij,j->p",
        coeff,
        a,
        coeff,
    )

    physical_energy = _inventory_j(
        field, er, ez, br, bz
    )

    predicted_energy = float(
        coeff @ hmat @ coeff
    )

    a_error = float(
        np.max(np.abs(predicted - measured))
    )

    e_error = abs(
        physical_energy - predicted_energy
    )

    return {
        "acceleration_absolute_error_m_s2": a_error,
        "canonical_energy_absolute_error_j": e_error,
        "pass": bool(
            a_error <= 1.0e-6
            and e_error <= 1.0e-7
        ),
    }


def solve_relaxed_source_cone(
    a: np.ndarray,
    hmat: np.ndarray,
) -> dict[str, Any]:
    """Convex necessary-condition test of the two-lane source family.

    Two real source lanes require Z=u*u^T+v*v^T, positive semidefinite
    with rank <=2. Relaxing the rank is an optimistic screening step.

    No SDP result becomes physical without rank-two reconstruction.
    """
    import cvxpy as cp

    n = hmat.shape[0]
    variable = cp.Variable((n, n), PSD=True)

    requirements = [
        cp.sum(cp.multiply(a[i], variable)) >= TARGET_G
        for i in range(a.shape[0])
    ]

    objective = cp.Minimize(
        cp.sum(cp.multiply(hmat, variable))
    )

    problem = cp.Problem(
        objective,
        requirements,
    )

    try:
        problem.solve(
            solver=cp.CLARABEL,
            max_iter=400,
            tol_feas=1.0e-8,
            tol_gap_abs=1.0e-8,
            tol_gap_rel=1.0e-8,
        )
    except Exception as error:
        return {
            "status": "SOLVER_EXCEPTION",
            "error": str(error),
            "verified_relaxed_feasible": False,
            "two_lane_constructive_pass": False,
        }

    result: dict[str, Any] = {
        "status": str(problem.status),
        "reported_optimal_field_j": (
            float(problem.value)
            if problem.value is not None
            and math.isfinite(float(problem.value))
            else None
        ),
        "verified_relaxed_feasible": False,
        "two_lane_constructive_pass": False,
    }

    if variable.value is None:
        return result

    z = 0.5 * (
        variable.value + variable.value.T
    )

    eigen, vectors = np.linalg.eigh(z)

    accel = np.einsum(
        "pij,ji->p", a, z
    )

    energy = float(
        np.sum(hmat * z)
    )

    relaxed_feasible = bool(
        problem.status == "optimal"
        and float(np.min(eigen)) >= -1.0e-7
        and float(np.min(accel)) >= TARGET_G * (1.0 - 1.0e-5)
        and energy >= -1.0e-7
    )

    result.update({
        "verified_relaxed_feasible": relaxed_feasible,
        "relaxed_minimum_acceleration_m_s2":
            float(np.min(accel)),
        "relaxed_energy_j": energy,
        "minimum_z_eigenvalue":
            float(np.min(eigen)),
        "source_cone_rank_threshold_1e-7":
            int(np.count_nonzero(
                eigen
                > max(float(np.max(eigen)), 1.0) * 1.0e-7
            )),
    })

    if not relaxed_feasible:
        return result

    # A physical two-lane candidate can use only two eigenvectors.
    order = np.argsort(eigen)[::-1][:2]

    pairs = [
        np.sqrt(max(float(eigen[k]), 0.0))
        * vectors[:, k]
        for k in order
    ]

    z2 = sum(
        (np.outer(v, v) for v in pairs),
        np.zeros_like(z),
    )

    projected = np.einsum(
        "pij,ji->p", a, z2
    )

    min_proj = float(
        np.min(projected)
    )

    result[
        "projected_two_lane_minimum_before_rescale_m_s2"
    ] = min_proj

    if min_proj <= 0.0:
        return result

    rescale = math.sqrt(
        TARGET_G / min_proj
    )

    pairs = [v * rescale for v in pairs]
    z2 *= rescale**2

    accel2 = np.einsum(
        "pij,ji->p", a, z2
    )

    energy2 = float(
        np.sum(hmat * z2)
    )

    result.update({
        "two_lane_constructive_pass": bool(
            np.min(accel2) >= TARGET_G * (1.0 - 1.0e-10)
            and energy2 < STRICT_COMPLETE_CEILING_J
        ),
        "two_lane_minimum_acceleration_m_s2":
            float(np.min(accel2)),
        "two_lane_canonical_field_energy_j":
            energy2,
        "two_lane_sub100j_partial_field":
            energy2 < LOW_FIELD_SCREEN_J,
        "two_lane_coefficients":
            [v.tolist() for v in pairs],
    })

    return result


def run_grid(h: float) -> dict[str, Any]:
    """Build the full-loading source response cone and validate R3X1."""
    setup = _build_baseline_and_prep(float(h))
    modes = source_modes(setup)

    response = loaded_response_basis(
        setup,
        modes,
        lam=1.0,
    )

    a_full, h_full = quadratic_payload_matrices(
        setup,
        response,
    )

    # Reproduce the original R3X1 failing mirror as an exact control.
    control = np.zeros(len(modes))

    control[0] = math.sqrt(
        modes[0]["unscaled_source_vacuum_j"]
    )

    control[1] = math.sqrt(
        modes[1]["unscaled_source_vacuum_j"]
    )

    control_check = direct_quadratic_check(
        setup, response, a_full, h_full, control
    )

    control_min = float(np.min(
        np.einsum(
            "i,pij,j->p",
            control,
            a_full,
            control,
        )
    ))

    control_energy = float(
        control @ h_full @ control
    )

    reference = _state(
        setup,
        _solve_loaded(setup["prep"], 1.0, 1.0),
    )

    control_match = bool(
        abs(
            control_min
            - reference["minimum_payload_acceleration_m_s2"]
        ) < CONTROL_ACCEL_ABS_TOL
        and abs(
            control_energy
            - reference["canonical_field_energy_j"]
        ) < CONTROL_FIELD_ENERGY_ABS_TOL
        and control_check["pass"]
    )

    if not control_match:
        raise RuntimeError(
            "R3X2 source basis fails the R3X1 mirror control"
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
        a = a_full[:, indices][:, :, indices]
        hmat = h_full[np.ix_(indices, indices)]

        result = solve_relaxed_source_cone(
            a,
            hmat,
        )

        if result.get("two_lane_constructive_pass"):
            reconstructed = []

            for coeff in result["two_lane_coefficients"]:
                coeff_full = np.zeros(len(modes))
                coeff_full[indices] = coeff

                reconstructed.append(
                    direct_quadratic_check(
                        setup,
                        response,
                        a_full,
                        h_full,
                        coeff_full,
                    )
                )

            result[
                "independent_two_lane_field_reconstruction"
            ] = reconstructed

            result["two_lane_constructive_pass"] = bool(
                all(x["pass"] for x in reconstructed)
            )

        result["source_names"] = [
            modes[i]["name"]
            for i in indices
        ]

        result["source_realization_complete"] = False
        catalogs[name] = result

    return {
        "grid_h_m": float(h),
        "payload_grid_points": int(a_full.shape[0]),
        "source_modes": [
            {
                k: v
                for k, v in mode.items()
                if k not in ("phi", "a_phi")
            }
            for mode in modes
        ],
        "physical_sign_loaded_residual":
            response["relative_source_residual"],
        "baseline_control_min_a_m_s2": control_min,
        "baseline_control_energy_j": control_energy,
        "baseline_matches_r3x1": control_match,
        "catalogs": catalogs,

        # Local-only matrices; never serialized into the JSON summary.
        "_private": {
            "a_full": a_full,
            "h_full": h_full,
            "response": response,
            "setup": setup,
            "modes": modes,
        },
    }


def _independent_full_sparse_lane_checks(
    grid: dict[str, Any],
    raw_lanes: list[dict[str, float]],
    amplitude_rescale: float,
) -> list[dict[str, Any]]:
    """Independently solve the full sparse loaded BVP for each lane."""
    internal = grid["_private"]
    setup = internal["setup"]
    base_prep = setup["prep"]

    modes = {
        mode["name"]: mode
        for mode in internal["modes"]
    }

    checks = []

    for lane in raw_lanes:
        phi0 = np.zeros_like(setup["phi0"])
        a0 = np.zeros_like(setup["a0"])

        for name, raw_weight in lane.items():
            mode = modes[name]

            coefficient = (
                raw_weight
                * amplitude_rescale
                * math.sqrt(
                    mode["unscaled_source_vacuum_j"]
                )
            )

            phi0 += coefficient * mode["phi"]
            a0 += coefficient * mode["a_phi"]

        phi_vec = phi0[1:-1, :-1].reshape(-1)
        a_vec = a0[1:-1, 1:-1].reshape(-1)

        prep = dict(base_prep)
        prep["phi0_vec"] = phi_vec
        prep["a0_vec"] = a_vec

        prep["c_a0"] = np.asarray(
            prep["c_active"] @ a_vec
        ).reshape(-1)

        prep["d_phi0"] = np.asarray(
            prep["d_active"] @ phi_vec
        ).reshape(-1)

        local_setup = dict(setup)

        local_setup.update({
            "prep": prep,
            "phi0": phi0,
            "a0": a0,
        })

        woodbury = _solve_loaded(
            prep,
            1.0,
            1.0,
        )

        if not woodbury["success"]:
            checks.append({
                "pass": False,
                "reason": "woodbury_solve_failed",
            })
            continue

        checks.append(
            _direct_compare(
                local_setup,
                woodbury,
                1.0,
                1.0,
            )
        )

    return checks


def cross_grid_common_source(
    grids: list[dict[str, Any]],
) -> dict[str, Any]:
    """Transfer one fine-grid physical shell source to both grids.

    A single set of raw shell multipole coefficients must work at both
    resolutions. Each grid's unit-J normalization is removed before
    comparing source amplitudes.

    A common rescale is permitted, but source geometry cannot change.
    """
    fine = min(
        grids,
        key=lambda row: row["grid_h_m"],
    )

    catalog = fine["catalogs"]["shell_only"]

    if not catalog.get("two_lane_constructive_pass"):
        return {
            "pass": False,
            "reason": "no_two_lane_fine_grid_source",
        }

    source_names = catalog["source_names"]

    fine_modes = {
        item["name"]:
            item["unscaled_source_vacuum_j"]
        for item in fine["source_modes"]
    }

    raw_lanes = []

    for lane in catalog["two_lane_coefficients"]:
        raw_lanes.append({
            name: float(value) / math.sqrt(fine_modes[name])
            for name, value in zip(source_names, lane)
        })

    grid_records = []

    for grid in grids:
        internal = grid["_private"]
        modes = internal["modes"]

        names = {
            mode["name"]: j
            for j, mode in enumerate(modes)
        }

        coefficients = []

        for lane in raw_lanes:
            vector = np.zeros(len(modes))

            for name, raw_value in lane.items():
                vector[names[name]] = (
                    raw_value
                    * math.sqrt(
                        modes[names[name]][
                            "unscaled_source_vacuum_j"
                        ]
                    )
                )

            coefficients.append(vector)

        a = internal["a_full"]
        hmat = internal["h_full"]

        acceleration = sum(
            np.einsum(
                "i,pij,j->p",
                lane,
                a,
                lane,
            )
            for lane in coefficients
        )

        energy = sum(
            float(lane @ hmat @ lane)
            for lane in coefficients
        )

        checks = [
            direct_quadratic_check(
                internal["setup"],
                internal["response"],
                a,
                hmat,
                lane,
            )
            for lane in coefficients
        ]

        # Mixed invariant is the sum of the two cross-lane products.
        # There is no artificial cross term between the two lanes.
        response = internal["response"]

        combined_eb = np.zeros_like(
            internal["setup"]["field"]["rho_grid"]
        )

        for lane in coefficients:
            er = np.tensordot(
                lane, response["e_r"], axes=(0, 0)
            )
            ez = np.tensordot(
                lane, response["e_z"], axes=(0, 0)
            )
            br = np.tensordot(
                lane, response["b_r"], axes=(0, 0)
            )
            bz = np.tensordot(
                lane, response["b_z"], axes=(0, 0)
            )

            combined_eb += er * br + ez * bz

        sigma = (
            -2.0
            * HBAR_C_EV_M**2
            * combined_eb
            / REFERENCE_PORTAL_SCALE_EV**4
        )

        payload_sigma_max = float(
            np.max(
                np.abs(
                    sigma[
                        internal["setup"]["field"]["payload"]
                    ]
                )
            )
        )

        grid_records.append({
            "grid_h_m": grid["grid_h_m"],
            "minimum_acceleration_before_shared_rescale_m_s2":
                float(np.min(acceleration)),
            "canonical_energy_before_shared_rescale_j":
                energy,
            "max_abs_payload_sigma_before_rescale":
                payload_sigma_max,
            "individual_lane_direct_field_checks":
                checks,
        })

    common_min = min(
        row[
            "minimum_acceleration_before_shared_rescale_m_s2"
        ]
        for row in grid_records
    )

    if common_min <= 0.0:
        return {
            "pass": False,
            "reason":
                "transferred_source_loses_whole_payload_outward_sign",
            "grids": grid_records,
        }

    factor = TARGET_G / common_min

    for row in grid_records:
        row["minimum_acceleration_after_rescale_m_s2"] = (
            row[
                "minimum_acceleration_before_shared_rescale_m_s2"
            ]
            * factor
        )

        row["canonical_energy_after_rescale_j"] = (
            row[
                "canonical_energy_before_shared_rescale_j"
            ]
            * factor
        )

        beta_argument = (
            4.0
            * row["max_abs_payload_sigma_before_rescale"]
            * factor
        )

        row["max_beta_nonlinear_fraction_after_rescale"] = (
            abs(math.expm1(beta_argument))
            if beta_argument < 100.0
            else math.inf
        )

    inexpensive_pass = bool(
        all(
            row[
                "minimum_acceleration_after_rescale_m_s2"
            ] >= TARGET_G * (1.0 - 1.0e-10)
            and row[
                "canonical_energy_after_rescale_j"
            ] < LOW_FIELD_SCREEN_J
            and row[
                "max_beta_nonlinear_fraction_after_rescale"
            ] < 1.0e-8
            and all(
                x["pass"]
                for x in row[
                    "individual_lane_direct_field_checks"
                ]
            )
            for row in grid_records
        )
    )

    if inexpensive_pass:
        for grid, row in zip(grids, grid_records):
            row["independent_full_sparse_lane_checks"] = (
                _independent_full_sparse_lane_checks(
                    grid,
                    raw_lanes,
                    math.sqrt(factor),
                )
            )

    full_pass = bool(
        inexpensive_pass
        and all(
            all(
                check["pass"]
                for check in row[
                    "independent_full_sparse_lane_checks"
                ]
            )
            for row in grid_records
        )
    )

    return {
        "pass": full_pass,
        "common_physical_source_rescale_factor_in_energy":
            factor,
        "grids": grid_records,
    }


def final_decision(
    provenance: dict[str, Any],
    ward: dict[str, Any],
    grids: list[dict[str, Any]],
) -> dict[str, Any]:
    valid = bool(
        provenance["pass"]
        and ward["net_charge_zero_pass"]
        and ward[
            "azimuthal_surface_current_divergence_zero_by_axisymmetry"
        ]
        and all(
            x["baseline_matches_r3x1"]
            for x in grids
        )
        and all(
            x["physical_sign_loaded_residual"]
            < SOURCE_RESIDUAL_TOL
            for x in grids
        )
    )

    common = (
        cross_grid_common_source(grids)
        if valid
        else {"pass": False}
    )

    shell_success = bool(
        valid
        and common["pass"]
        and all(
            x["catalogs"]["shell_only"].get(
                "two_lane_constructive_pass"
            )
            for x in grids
        )
    )

    if not valid:
        decision = (
            "RED_HOLD_R3X2_SOURCE_WARD_OR_"
            "CONTROL_RECONSTRUCTION_FAILED"
        )

        next_run = (
            "REPAIR_R3X2_BEFORE_SCIENTIFIC_PROMOTION"
        )

    elif shell_success:
        decision = (
            "GREEN_SCOPED_R3X2_SHELL_SOURCE_TWO_LANE_"
            "FULL_FROZEN_BETA_ONE_G_AND_LOW_FIELD_CAPACITY"
        )

        next_run = (
            "032H17A12D1R3X3_"
            "CONTINUUM_AND_PHYSICAL_SOURCE_GATE"
        )

    else:
        decision = (
            "YELLOW_SCOPED_R3X2_NO_VERIFIED_LOW_FIELD_"
            "TWO_LANE_SHELL_SOURCE_SURVIVOR_IN_DECLARED_CONE"
        )

        next_run = (
            "032H17A12D1R3X3_"
            "SOURCE_CONE_DUAL_AND_PARITY_GATE"
        )

    return {
        "decision": decision,
        "next": next_run,
        "source_support_ward_pass": valid,
        "shell_two_lane_low_field_candidate_both_grids":
            shell_success,
        "cross_grid_common_physical_source":
            common,
        "psd_relaxation_not_physical_two_lane_certificate":
            True,
        "source_shell_microphysicalized": False,
        "cross_u1_parity_anomaly_completed": False,
        "nonlinear_full_metric_noether_completed": False,
        "interacting_stability_certified": False,
        "continuum_convergence_certified": False,
        "complete_energy_established": False,
        "certified_sub10mj_model_found": False,
        "physical_antigravity_model_found": False,
        "006d_replaced": False,
    }
