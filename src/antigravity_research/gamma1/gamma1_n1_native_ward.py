"""GAMMA1-N1: authentic PH16 stationarity / topological Ward induction audit.

Question: does native PH16 R5 matter multiplier yield a Y source
not explainable by finite-grid leakage of continuum-null lambda=f(A0)?

Stationary lattice mathematics only. No covariant gravitational stress,
full Lorentzian health, Earth reaction, SI energy or craft lift.
"""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy import sparse

PARENTS = {
    "PH16": (
        "src/antigravity_research/ph16/ph16_04_joint_stationary.py",
        "b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0",
    ),
    "R3": (
        "results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz",
        "94d3763a8d7705ab3dc8774310cf3b8bba96557a0b80d2c34aa110d00b840d54",
    ),
    "R5": (
        "results/data/gamma1_00r5_20261119T024922295970Z_lattice_multiplier_12_L12.npz",
        "2b9217ef9b36758ef675eeb47796198adf1be2ff6b5764b316a2e312bc82c883",
    ),
    "R11": (
        "results/data/gamma1_00r11_20261119T074039011670Z.json",
        "ac7050c648959ee0daa21bed994d8cdc34abb261d08433f302d4362af163acef",
    ),
    "R12": (
        "results/data/gamma1_00r12_20261119T201141220587Z.json",
        "7ebddf22bd718dc9729b1d63cb72943d75e379c12ce68420399edaafcf99bad6",
    ),
    "D0": (
        "results/data/gamma1_d0_20261119T205007375929Z.json",
        "a89998f3a3ab7721295ecbf568795d417e2ec9769fd059caf7e0b6446e380a80",
    ),
    "C1": (
        "results/data/gamma1_c1_20261119T212606521420Z.json",
        "ebd7ebef9cd26d70388c7d0d49ee85b7018654b29043678dbdf307ede3ed4111",
    ),
    "C1_verify": (
        "results/data/gamma1_c1_verification_20261119T213930352220Z.json",
        "373335f857f8f720d4915917ebacf0a22255014bdbb375c19938ad2d3748dd1a",
    ),
}


def sha(path):
    p = Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "MISSING"


def lock(root):
    result = {}
    for name, (relative, expected) in PARENTS.items():
        p = Path(root) / relative
        actual = sha(p)
        if actual != expected:
            raise RuntimeError(f"{name}_SHA_DRIFT:{actual}")
        if p.suffix in (".npz", ".json"):
            side = p.with_name(p.name + ".sha256")
            if not side.is_file() or side.read_text().strip() != expected + "  " + p.name:
                raise RuntimeError(f"{name}_SIDECAR_DRIFT")
        result[name] = {"path": relative, "sha256": actual}

    previous = json.loads((Path(root) / PARENTS["C1"][0]).read_text())
    if (
        previous["GAMMA1_01_authorized"] is not False
        or previous["qualified_gravity_bridge_survivors"] != []
    ):
        raise RuntimeError("C1_AUTHORIZATION_DRIFT")
    return result


def operators(rho, Dr, Dz):
    """Exact PH16 cylindrical magnetic field representation."""
    Br = -Dz
    Bz = sparse.diags(1 / rho) @ Dr @ sparse.diags(rho)
    return Br.tocsr(), Bz.tocsr()


def field_operators(A, Y, rho, Dr, Dz, Br, Bz):
    Er = -Dr @ A
    Ez = -Dz @ A
    Byr = Br @ Y
    Byz = Bz @ Y
    CA = (
        -sparse.diags(Byr) @ Dr
        - sparse.diags(Byz) @ Dz
    ).tocsr()
    CY = (
        sparse.diags(Er) @ Br
        + sparse.diags(Ez) @ Bz
    ).tocsr()
    return CA, CY, Er, Ez, Byr, Byz


def core_mask(nr):
    mask = np.zeros((nr, 2 * nr), dtype=bool)
    mask[3:-3, 3:-3] = True
    return mask.ravel()


def normalized_projection(A, lam, w, CY):
    """Descriptive polynomial lambda=f(A), not an on-shell claim."""
    mean = np.average(A, weights=w)
    std = np.sqrt(np.average((A - mean)**2, weights=w))
    if std < 1e-12:
        raise RuntimeError("NATIVE_X_TOO_CONSTANT_FOR_INTEGRABILITY_TEST")

    x = (A - mean) / std
    columns = np.stack(
        (np.ones(len(A)), x, x*x, x*x*x),
        axis=1,
    )
    sw = np.sqrt(w)
    coefficients = np.linalg.lstsq(
        columns * sw[:, None], lam * sw, rcond=None
    )[0]
    fitted = columns @ coefficients
    residual = lam - fitted

    native = CY.T @ (-w * lam)
    fitted_signal = CY.T @ (-w * fitted)
    remaining = CY.T @ (-w * residual)

    error = np.linalg.norm(
        native - fitted_signal - remaining
    )
    if error > 1e-9:
        raise RuntimeError("POLYNOMIAL_SOURCE_DECOMPOSITION_FAIL")

    denominator = np.linalg.norm(native)
    mean_lam = np.average(lam, weights=w)
    variance = np.dot(w, (lam - mean_lam)**2)

    fit_r2 = (
        1 - np.dot(w, residual**2) / variance
        if variance > 1e-24 else None
    )

    return {
        "lambda_f_of_A_polynomial_degree": 3,
        "lambda_f_of_A_fit_weighted_r2":
            float(fit_r2) if fit_r2 is not None else None,
        "fitted_polynomial_coefficients": coefficients.tolist(),
        "Y_total_source_l2": float(denominator),
        "Y_continuum_null_f_of_A_artifact_l2":
            float(np.linalg.norm(fitted_signal)),
        "Y_nonintegrable_residual_source_l2":
            float(np.linalg.norm(remaining)),
        "Y_aligned_artifact_over_total":
            float(np.linalg.norm(fitted_signal) / denominator)
            if denominator > 1e-30 else None,
        "Y_nonintegrable_over_total":
            float(np.linalg.norm(remaining) / denominator)
            if denominator > 1e-30 else None,
        "exact_linear_decomposition_error": float(error),
        "fitted_lambda_rms": float(
            np.sqrt(np.dot(w, fitted*fitted) / np.sum(w))
        ),
        "residual_lambda_rms": float(
            np.sqrt(np.dot(w, residual*residual) / np.sum(w))
        ),
    }


@lru_cache(maxsize=2)
def native(root):
    """Use actual immutable 12/L12 PH16/R3/R5 data."""
    from antigravity_research.ph16.ph16_04_joint_stationary import (
        CoulombSource, Spec, JointAction, Settings
    )

    root = Path(root)
    with np.load(root / PARENTS["R3"][0], allow_pickle=False) as src:
        A = src["A_X"].copy()
        Y = src["A_Y"].copy()
        F = np.stack((src["F_plus"], src["F_minus"]))
        original_P = src["P"].copy()

    with np.load(root / PARENTS["R5"][0], allow_pickle=False) as saved:
        lam = saved["lambda_Routhian"].copy()
        portal_x = saved["portal_X_gradient"].copy()
        portal_y = saved["portal_Y_gradient"].copy()

    m = CoulombSource(Spec(nr=12, L=12.), self_order=8)
    j = JointAction(m, Settings(nr=12, L=12.))

    if len(A) != 288 or len(lam) != 288:
        raise RuntimeError("NATIVE_SHAPE_DRIFT")

    R, gradient, details = j.evaluate(
        j.pack(F, A, Y), details=True
    )
    if np.linalg.norm(gradient) >= 1e-6:
        raise RuntimeError("NATIVE_ORIGINAL_STATIONARITY_FAIL")

    Br, Bz = operators(m.rho, j.Dr, j.Dz)
    CA, CY, Er, Ez, Byr, Byz = field_operators(
        A, Y, m.rho, j.Dr, j.Dz, Br, Bz
    )

    P = Er*Byr + Ez*Byz
    if np.max(abs(P - original_P)) > 2e-12:
        raise RuntimeError("NATIVE_P_REPLAY_FAIL")

    predicted_x = CA.T @ (-j.w * lam)
    predicted_y = CY.T @ (-j.w * lam)

    if max(
        np.max(abs(predicted_x - portal_x)),
        np.max(abs(predicted_y - portal_y)),
    ) > 1e-10:
        raise RuntimeError("ORIGINAL_R5_SOURCE_VARIATION_DRIFT")

    y_eom = j.Ky @ Y + predicted_y
    if np.linalg.norm(y_eom) > 1e-6:
        raise RuntimeError("NATIVE_Y_STATIONARITY_DRIFT")

    mask = core_mask(12)
    constant_x = CA.T @ j.w
    constant_y = CY.T @ j.w

    null_error = max(
        np.max(abs(constant_x[mask])),
        np.max(abs(constant_y[mask])),
    )
    if null_error > 1e-9:
        raise RuntimeError(
            "NATIVE_CONSTANT_LAMBDA_BULK_TOPOLOGICAL_WARD_FAIL"
        )

    dAr = j.Dr @ A
    dAz = j.Dz @ A
    dLr = j.Dr @ lam
    dLz = j.Dz @ lam

    # Bulk continuum product-rule expectation under fixed orientation.
    density = j.w * (dAr*dLz - dAz*dLr)
    relative_error = float(
        np.linalg.norm((predicted_y - density)[mask])
        / max(np.linalg.norm(predicted_y[mask]), 1e-30)
    )
    aligned_linear = CY.T @ (-j.w * A)
    fit = normalized_projection(A, lam, j.w, CY)

    return {
        "native_grid_cells": 288,
        "Routhian_NOT_J": float(R),
        "joint_gradient_l2": float(np.linalg.norm(gradient)),
        "Noether_plus_minus": [float(v) for v in details["N"]],
        "native_Y_EOM_l2": float(np.linalg.norm(y_eom)),
        "R5_portal_Y_replication_inf":
            float(np.max(abs(predicted_y - portal_y))),
        "native_Y_source_l2": float(np.linalg.norm(predicted_y)),
        "native_Y_source_bulk_l2":
            float(np.linalg.norm(predicted_y[mask])),
        "constant_lambda_X_bulk_inf":
            float(np.max(abs(constant_x[mask]))),
        "constant_lambda_Y_bulk_inf":
            float(np.max(abs(constant_y[mask]))),
        "constant_lambda_X_full_l2_boundary_included":
            float(np.linalg.norm(constant_x)),
        "constant_lambda_Y_full_l2_boundary_included":
            float(np.linalg.norm(constant_y)),
        "linear_lambda_equals_A_bulk_spurious_l2":
            float(np.linalg.norm(aligned_linear[mask])),
        "native_differential_jacobian_bulk_l2":
            float(np.linalg.norm(density[mask])),
        "native_discrete_vs_differential_bulk_relative_error":
            relative_error,
        "lambda_range": [
            float(np.min(lam)), float(np.max(lam))
        ],
        "cross_gradient_rms": float(np.sqrt(
            np.mean((dAr*dLz - dAz*dLr)[mask]**2)
        )),
        "continuum_on_shell_status": "NOT_ESTABLISHED",
        "integrability_projection": fit,
    }


def derivative(n, h):
    D = sparse.diags(
        [-np.ones(n-1)*.5/h, np.ones(n-1)*.5/h],
        [-1, 1], shape=(n, n), format="lil"
    )
    D[0, 0] = -1/h
    D[0, 1] = 1/h
    D[-1, -2] = -1/h
    D[-1, -1] = 1/h
    return D.tocsr()


def manufactured_grid(n, L=12.):
    """Same cylindrical stencil, without the costly Green kernels."""
    h = L/n
    nz = 2*n
    radial = (np.arange(n)+.5)*h
    axial = (np.arange(nz)+.5)*h-L

    r, z = np.meshgrid(radial, axial, indexing="ij")
    r = r.ravel()
    z = z.ravel()
    w = 2*np.pi*r*h*h

    Dr = sparse.kron(
        derivative(n, h), sparse.eye(nz), format="csr"
    )
    Dz = sparse.kron(
        sparse.eye(n), derivative(nz, h), format="csr"
    )

    Br, Bz = operators(r, Dr, Dz)
    return r, z, w, Dr, Dz, Br, Bz


def bump(x, width):
    a = abs(x)/width
    result = np.zeros_like(a)
    inside = a < 1
    result[inside] = np.exp(
        -1/(1-a[inside]**2)
    )
    return result


def smooth_control(n):
    r, z, w, Dr, Dz, Br, Bz = manufactured_grid(n)

    A = (
        bump(r-4, 2.1)*bump(z, 2.2)
        *(1+.2*(r-4)+.1*z)
    )
    Y = (
        bump(r-4.2, 2.1)*bump(z+.3, 2.2)
        *(.5+.15*(r-4)+.1*z)
    )
    lam = (
        .1+.5*bump(r-4.1, 1.5)*bump(z-.1, 1.7)
    )

    CA, CY, Er, Ez, Byr, Byz = field_operators(
        A, Y, r, Dr, Dz, Br, Bz
    )

    constant_error = float(max(
        np.max(abs(CA.T @ w)),
        np.max(abs(CY.T @ w)),
    ))

    aligned = CY.T @ (w*A)
    aligned_l2 = float(
        np.sqrt(np.sum(aligned**2/w))
    )

    source = CY.T @ (-w*lam)
    predicted = w*(
        (Dr @ A)*(Dz @ lam)
        -(Dz @ A)*(Dr @ lam)
    )
    relative = float(
        np.linalg.norm(source-predicted)
        / np.linalg.norm(source)
    )

    return {
        "nr": n,
        "cells": 2*n*n,
        "constant_topological_abs_max": constant_error,
        "aligned_function_of_A_spurious_weighted_l2": aligned_l2,
        "weak_vs_continuum_jacobian_relative_error": relative,
        "nonconstant_source_l2": float(np.linalg.norm(source)),
    }


def convergence():
    probes = [smooth_control(n) for n in (24, 36, 48, 72)]

    if max(
        p["constant_topological_abs_max"] for p in probes
    ) > 1e-10:
        raise AssertionError(
            "SMOOTH_COMPACT_CONSTANT_TOPOLOGY_FAIL"
        )

    aligned = [
        p["aligned_function_of_A_spurious_weighted_l2"]
        for p in probes
    ]
    errors = [
        p["weak_vs_continuum_jacobian_relative_error"]
        for p in probes
    ]

    if not (
        all(x > y for x, y in zip(aligned, aligned[1:]))
        and all(x > y for x, y in zip(errors, errors[1:]))
    ):
        raise AssertionError(
            "SMOOTH_CONTINUUM_NULL_NONCONVERGENCE"
        )

    return {
        "controls": probes,
        "aligned_null_artifact_decreases": True,
        "weak_jacobian_error_decreases": True,
        "limitations":
            "SYNTHETIC_SMOOTH_FIELDS_NOT_NATIVE_ONSHELL_CONVERGENCE",
    }


def science(root):
    parents = lock(root)
    smooth = convergence()
    actual = native(root)

    projected = actual["integrability_projection"]
    ratio = projected["Y_aligned_artifact_over_total"]

    if actual["native_Y_source_l2"] < 1e-13:
        decision = "NATIVE_Y_NULL_AT_REPLAY_PRECISION"
    elif ratio is None:
        decision = "NATIVE_Y_RATIO_UNDEFINED"
    elif ratio >= .5:
        decision = "NATIVE_Y_SUBSTANTIAL_INTEGRABLE_ARTIFACT_RISK"
    else:
        decision = "NATIVE_Y_INTEGRABLE_ARTIFACT_UNDER_HALF_SCOPED"

    return {
        "parents": parents,
        "native": actual,
        "synthetic_smooth_controls": smooth,
        "native_integrability_decision": decision,
        "classification":
            "SCOPED_NATIVE_WARD_AND_INDUCTION_AUDIT_NO_PHYSICAL_PROMOTION",
        "gates": {
            "R3_NATIVE_SOURCE_STATIONARY": "PASS_SCOPED",
            "R5_SAME_ROUTHIAN_MULTIPLIER": "PASS_SCOPED",
            "CONSTANT_MIXED_COEFFICIENT_BULK_TOPOLOGICAL_WARD":
                "PASS_SCOPED",
            "NATIVE_INDUCED_Y_VERSUS_INTEGRABLE_ARTIFACT":
                "MEASURED_NOT_CERTIFIED",
            "SYNTHETIC_REFINEMENT_NULL": "PASS_SCOPED",
            "NATIVE_CONTINUUM_AND_EXTERIOR_MATCH": "NOT_ESTABLISHED",
            "PH16_COVARIANT_LORENTZIAN_ACTION": "NOT_DERIVED",
            "EINSTEIN_EARTH_SUPPORT_FLUID": "NOT_DERIVED",
            "FULL_CONSTRAINED_HEALTH": "NOT_CERTIFIED",
            "SI_EFT_EMPIRICAL_UV": "NOT_CERTIFIED",
        },
        "GAMMA1_01_authorized": False,
        "PH16_05_authorized": False,
        "PH17_authorized": False,
        "006D_replaced": False,
        "qualified_gravity_bridge_survivors": [],
        "Earth_down": "NOT_DERIVED",
        "whole_craft_up": "NOT_DERIVED",
        "complete_operating_energy_lt_10MJ": "NOT_CERTIFIED",
        "GAMMA_heuristic_percent": "UNCHANGED_34",
    }
