"""
031B2-D96
=========

Combined coupled-linear stability certification for the 96.141-GJ operating
candidate's intrinsic spherical global-U(1) Q-ball source.

This run deliberately separates two facts:

1. The rigid payload-adjacent translation and ordinary-matter alpha_m used to
   reach the 96.141-GJ operating ledger do not change the isolated spherical
   source's intrinsic dimensionless amplitude/phase/scalar stability operator.
2. The operating-point leakage/backreaction margins remain a separate gate.

The run therefore certifies the exact C83 best source theory parameters
(epsilon, omega, chi), with:

- independent short/long-domain background reconstruction;
- complete dense coupled spectrum for l=0..8 on two grids at R=60;
- exact treatment of l=1 as the translational Goldstone sector;
- finite-volume Yukawa/Robin tails;
- four-point h->0 translation-mode convergence at epsilon*R=3;
- independent epsilon*R=5 domain cross-check;
- exact translation-orthogonal projected-stiffness cross-check;
- low-overlap near-zero dynamic-mode search.

A GREEN result closes only coupled-linear source stability for l=0..8 within
this model. It does not close finite-amplitude fragmentation, activation,
physical-metric backreaction, radiative naturalness, empirical constraints,
or practical engineering.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

from scipy.linalg import eigvals
from scipy.sparse import bmat, csr_matrix, diags, identity
from scipy.sparse.linalg import (
    ArpackNoConvergence,
    LinearOperator,
    eigs,
    eigsh,
)
from scipy.special import spherical_kn


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

QBALL_SOURCE = SIM / "031b2a_global_qball_activated_scalar_control.py"
BASE_SUMMARY = DATA / "031b2a_global_qball_activated_scalar_control_summary.json"
C83_SUMMARY = DATA / "031c83_compact_qball_epsilon_continuation_summary.json"
D273_GREEN = DATA / "031b2d273tzh_continuum_extrapolation_summary.json"

OUT_JSON = DATA / "031b2d96_combined_coupled_linear_goldstone_summary.json"
OUT_BROAD_CSV = DATA / "031b2d96_broad_spectrum_scan.csv"
OUT_L1_CSV = DATA / "031b2d96_l1_continuum_scan.csv"

# Preserve the successful D273 thresholds rather than tuning gates to D96.
BROAD_RMAX = 60.0
BROAD_H_TARGETS = (0.5, 0.375)
LMAX = 8

L1_PRIMARY_MU_R = 3.0
L1_PRIMARY_H_TARGETS = (0.5, 0.375, 0.25, 0.1875)
L1_CHECK_MU_R = 5.0
L1_CHECK_H_TARGETS = (0.5, 0.25)
LONG_MU_R = 5.0

NONTRANSLATION_GROWTH_TOL = 1.0e-8
NONTRANSLATION_GRID_DIFF_TOL = 1.0e-7
LOW_OVERLAP_GROWTH_TOL = 1.0e-8
TRANSLATION_OVERLAP_MIN = 0.995
PROJECTED_K_MIN_TOL = -1.0e-10
PROJECTED_EIG_RESIDUAL_TOL = 1.0e-8

GROWTH_POWER_MIN = 0.85
GROWTH_POWER_MAX = 1.15
RESIDUAL_POWER_MIN = 2.2
S_OVER_H_CV_MAX = 0.02
ZERO_INTERCEPT_RATIO_MAX = 0.10
DOMAIN_SPREAD_MAX = 0.01
BACKGROUND_CORE_REL_TOL = 1.0e-4

NEARZERO_K = 16
NEARZERO_OVERLAP_CUT = 0.90
EIGS_TOL = 1.0e-10
EIGS_MAXITER = 30000


# -----------------------------------------------------------------------------
# Generic helpers
# -----------------------------------------------------------------------------

def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"Missing required file: {path}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def to_builtin(value: Any):
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, complex):
        return {"real": float(value.real), "imag": float(value.imag)}
    if isinstance(value, dict):
        return {str(k): to_builtin(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_builtin(v) for v in value]
    return value


def rel_l2(a: np.ndarray, b: np.ndarray) -> float:
    return float(
        np.linalg.norm(a - b)
        / max(np.linalg.norm(a), np.linalg.norm(b), 1.0e-300)
    )


def rel_scalar(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0e-300)


# -----------------------------------------------------------------------------
# Background reconstruction
# -----------------------------------------------------------------------------

def solve_background(qmod, omega: float, epsilon: float, chi: float, x_match: float):
    qmod.X_MATCH = float(x_match)
    seed = qmod.solve_uncoupled_qball(omega)
    if seed is None:
        raise RuntimeError(
            f"Uncoupled Q-ball solve failed at X_MATCH={x_match}"
        )
    solution = qmod.solve_coupled(
        seed,
        omega,
        epsilon,
        chi,
        previous=None,
    )
    if solution is None:
        raise RuntimeError(
            f"Coupled Q-ball solve failed at X_MATCH={x_match}"
        )
    return solution


# -----------------------------------------------------------------------------
# Canonical reduced-radial finite-volume operator
# -----------------------------------------------------------------------------

def robin_beta(mu: float, ell: int, radius: float) -> float:
    """Return beta for q' + beta q = 0, q=r*k_l(mu r)."""
    x = mu * radius
    kval = float(spherical_kn(ell, x))
    kprime = float(spherical_kn(ell, x, derivative=True))
    if not math.isfinite(kval) or not math.isfinite(kprime) or kval == 0.0:
        # Large-x asymptotic fallback. The correction is already tiny there.
        return float(mu + 1.0 / max(radius, 1.0e-300))
    beta = -(1.0 / radius + mu * kprime / kval)
    if not math.isfinite(beta) or beta <= 0.0:
        raise RuntimeError(
            f"Invalid Robin beta: mu={mu} ell={ell} R={radius} beta={beta}"
        )
    return float(beta)


def fv_minus_second_derivative(n: int, h: float, beta: float):
    """Symmetric cell-centered -d2/dr2 with q(0)=0 and Robin at R."""
    diagonal = np.full(n, 2.0 / h**2, dtype=float)
    off = np.full(n - 1, -1.0 / h**2, dtype=float)

    # q=0 at the r=0 face via odd ghost continuation.
    diagonal[0] = 3.0 / h**2

    # Robin at the outer face using centered face value and normal derivative.
    gamma = (1.0 - 0.5 * beta * h) / (1.0 + 0.5 * beta * h)
    diagonal[-1] = (2.0 - gamma) / h**2

    return diags((off, diagonal, off), (-1, 0, 1), format="csr")


def build_fv_bundle(
    qmod,
    solution,
    omega: float,
    epsilon: float,
    chi: float,
    ell: int,
    rmax: float,
    h_target: float,
):
    cells = max(16, int(round(rmax / h_target)))
    h = rmax / cells
    r = (np.arange(cells, dtype=float) + 0.5) * h

    state = solution.sol(np.maximum(r, 1.0e-8))
    y = np.asarray(state[0], dtype=float)
    yp = np.asarray(state[1], dtype=float)
    u = np.asarray(state[2], dtype=float)
    up = np.asarray(state[3], dtype=float)

    A = np.exp(np.clip(-0.5 * u**2, -700.0, 0.0))
    denominator = 1.0 + y**2

    Va = A * (1.0 - y**2) / denominator**2 - omega**2
    Vb = A / denominator - omega**2
    Vv = (
        epsilon**2
        + chi**2 * A * qmod.W(y) * (u**2 - 1.0)
    )

    # Original a-v coupling C and D=chi^2*C become the symmetric chi*C
    # after the canonical scalar perturbation rescaling v -> v/chi.
    coupling = chi * (-u * A * y / denominator)

    angular = ell * (ell + 1.0) / r**2

    mu_x = math.sqrt(max(1.0 - omega**2, 1.0e-15))
    beta_x = robin_beta(mu_x, ell, rmax)
    beta_u = robin_beta(epsilon, ell, rmax)

    Tx = fv_minus_second_derivative(cells, h, beta_x)
    Tu = fv_minus_second_derivative(cells, h, beta_u)

    La = Tx + diags(angular + Va, 0, format="csr")
    Lb = Tx + diags(angular + Vb, 0, format="csr")
    Lv = Tu + diags(angular + Vv, 0, format="csr")

    Z = csr_matrix((cells, cells))
    I = identity(cells, format="csr")
    C = diags(coupling, 0, format="csr")

    K = bmat(
        [[La, Z, C], [Z, Lb, Z], [C, Z, Lv]],
        format="csr",
    )

    G = bmat(
        [
            [Z, 2.0 * omega * I, Z],
            [-2.0 * omega * I, Z, Z],
            [Z, Z, Z],
        ],
        format="csr",
    )

    dimension = 3 * cells
    Z3 = csr_matrix((dimension, dimension))
    I3 = identity(dimension, format="csr")

    first_order = bmat(
        [[Z3, I3], [-K, -G]],
        format="csr",
    )

    # Exact infinitesimal spatial translation in the same canonical reduced
    # radial variables used by K.
    translation = np.concatenate(
        [
            r * yp,
            np.zeros(cells, dtype=float),
            r * up / chi,
        ]
    )
    norm_t = float(np.linalg.norm(translation))
    if not math.isfinite(norm_t) or norm_t <= 0.0:
        raise RuntimeError("Degenerate analytic translation vector")
    translation /= norm_t

    k_asym = K - K.T
    g_asym = G + G.T
    k_symmetry_max = (
        float(np.max(np.abs(k_asym.data))) if k_asym.nnz else 0.0
    )
    g_skew_max = (
        float(np.max(np.abs(g_asym.data))) if g_asym.nnz else 0.0
    )

    if k_symmetry_max > 1.0e-12 or g_skew_max > 1.0e-12:
        raise RuntimeError(
            "Canonical structure failure: "
            f"K_SYM_MAX={k_symmetry_max} G_SKEW_MAX={g_skew_max}"
        )

    return {
        "r": r,
        "h": float(h),
        "cells": int(cells),
        "K": K,
        "G": G,
        "operator": first_order,
        "translation": translation,
        "beta_x": beta_x,
        "beta_u": beta_u,
        "k_symmetry_max": k_symmetry_max,
        "g_skew_max": g_skew_max,
    }


# -----------------------------------------------------------------------------
# Spectral diagnostics
# -----------------------------------------------------------------------------

def dense_growth(operator):
    values = eigvals(
        operator.toarray(),
        overwrite_a=True,
        check_finite=False,
    )
    values = np.asarray(values, dtype=complex)
    return float(np.max(values.real)), values


def translation_residual(bundle) -> dict[str, float]:
    K = bundle["K"]
    t = bundle["translation"]
    residual = K @ t
    fro = math.sqrt(float(np.dot(K.data, K.data)))
    absolute = float(np.linalg.norm(residual))
    relative = absolute / max(fro, 1.0e-300)
    rayleigh = float(t @ (K @ t))
    return {
        "absolute": absolute,
        "relative_frobenius": relative,
        "rayleigh": rayleigh,
    }


def nearzero_dynamic(bundle) -> dict[str, Any]:
    operator = bundle["operator"]
    t = bundle["translation"]
    config_dimension = len(t)

    try:
        values, vectors = eigs(
            operator,
            k=NEARZERO_K,
            sigma=0.0,
            which="LM",
            tol=EIGS_TOL,
            maxiter=EIGS_MAXITER,
        )
        arpack_partial = False
    except ArpackNoConvergence as exc:
        values = exc.eigenvalues
        vectors = exc.eigenvectors
        arpack_partial = True
        if values is None or vectors is None or len(values) < 8:
            raise RuntimeError(
                "Near-zero ARPACK did not return enough converged modes"
            ) from exc

    values = np.asarray(values, dtype=complex)
    vectors = np.asarray(vectors, dtype=complex)

    order = np.argsort(np.abs(values))
    values = values[order]
    vectors = vectors[:, order]

    overlaps = []
    for j in range(len(values)):
        config = vectors[:config_dimension, j]
        norm = float(np.linalg.norm(config))
        if norm <= 1.0e-300:
            overlaps.append(0.0)
        else:
            overlaps.append(float(abs(np.vdot(t, config / norm))))

    translation_candidates = [
        j for j, overlap in enumerate(overlaps) if overlap >= 0.95
    ]
    if not translation_candidates:
        raise RuntimeError(
            "No near-zero eigenmode has sufficient translation overlap"
        )

    # The split Goldstone mode appears as +/- real partners. Select the
    # positive member for the finite-grid growth diagnostic.
    translation_index = max(
        translation_candidates,
        key=lambda j: float(values[j].real),
    )

    translation_eigenvalue = values[translation_index]
    translation_overlap = overlaps[translation_index]
    translation_growth = max(0.0, float(translation_eigenvalue.real))

    low_overlap_reals = [
        float(values[j].real)
        for j in range(len(values))
        if overlaps[j] < NEARZERO_OVERLAP_CUT
    ]
    low_overlap_max_real = max(low_overlap_reals) if low_overlap_reals else 0.0

    return {
        "arpack_partial": arpack_partial,
        "translation_growth": translation_growth,
        "translation_overlap": translation_overlap,
        "translation_eigenvalue": translation_eigenvalue,
        "low_overlap_nearzero_max_real": low_overlap_max_real,
        "eigenvalues_by_abs": values,
        "overlaps_by_abs": overlaps,
    }


def projected_stiffness(bundle) -> dict[str, Any]:
    """Lowest exact Ritz values on t-perpendicular space via P K P."""
    K = bundle["K"]
    t = bundle["translation"]
    dimension = K.shape[0]
    penalty = 1.0

    def matvec(x):
        tx = float(np.dot(t, x))
        px = x - t * tx
        y = K @ px
        y = y - t * float(np.dot(t, y))
        return y + penalty * t * tx

    projected = LinearOperator(
        (dimension, dimension),
        matvec=matvec,
        dtype=float,
    )

    values, vectors = eigsh(
        projected,
        k=4,
        which="SA",
        tol=1.0e-10,
        maxiter=30000,
    )

    order = np.argsort(values)
    values = np.asarray(values[order], dtype=float)
    vectors = np.asarray(vectors[:, order], dtype=float)

    residuals = []
    overlaps = []
    for j in range(len(values)):
        vector = vectors[:, j]
        residuals.append(
            float(np.linalg.norm(projected @ vector - values[j] * vector))
        )
        overlaps.append(float(abs(np.dot(t, vector))))

    return {
        "eigenvalues": values,
        "lowest": float(values[0]),
        "residuals": residuals,
        "max_residual": max(residuals),
        "translation_overlaps": overlaps,
    }


def fit_continuum(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda row: float(row["h"]), reverse=True)
    h = np.asarray([float(row["h"]) for row in ordered], dtype=float)
    growth = np.asarray(
        [float(row["translation_growth"]) for row in ordered],
        dtype=float,
    )
    residual = np.asarray(
        [float(row["translation_residual_rel"]) for row in ordered],
        dtype=float,
    )

    if np.any(growth <= 0.0) or np.any(residual <= 0.0):
        raise RuntimeError("Continuum fit requires positive finite diagnostics")

    growth_power = float(np.polyfit(np.log(h), np.log(growth), 1)[0])
    residual_power = float(np.polyfit(np.log(h), np.log(residual), 1)[0])

    linear = np.polyfit(h, growth, 1)
    quadratic = np.polyfit(h, growth, 2)

    linear_intercept = float(linear[1])
    quadratic_intercept = float(quadratic[2])
    finest_growth = float(growth[-1])

    s_over_h = growth / h
    s_over_h_cv = float(np.std(s_over_h) / np.mean(s_over_h))

    return {
        "h": h,
        "growth": growth,
        "translation_residual": residual,
        "growth_power": growth_power,
        "residual_power": residual_power,
        "linear_intercept": linear_intercept,
        "linear_intercept_over_finest_growth": (
            abs(linear_intercept) / finest_growth
        ),
        "quadratic_intercept": quadratic_intercept,
        "quadratic_intercept_over_finest_growth": (
            abs(quadratic_intercept) / finest_growth
        ),
        "s_over_h": s_over_h,
        "s_over_h_cv": s_over_h_cv,
        "growth_monotone": bool(np.all(np.diff(growth) < 0.0)),
        "residual_monotone": bool(np.all(np.diff(residual) < 0.0)),
    }


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    print("=== 031B2-D96 COMBINED COUPLED-LINEAR + GOLDSTONE GATE ===")
    print(
        "CLAIM_CLASS="
        "96GJ_OPERATING_CANDIDATE_INTRINSIC_SPHERICAL_SOURCE_"
        "COUPLED_LINEAR_STABILITY_CERTIFICATION"
    )
    print("RIGID_TRANSLATION_CHANGES_INTRINSIC_SOURCE_SPECTRUM=NO")
    print("ALPHA_M_CHANGES_INTRINSIC_SOURCE_SPECTRUM=NO")
    print("OPERATING_MARGIN_CERTIFIED_BY_THIS_RUN=NO")
    print("NONLINEAR_FRAGMENTATION_PROOF=NO")
    print("FULL_METRIC_BACKREACTION_CLOSED=NO")
    print("PRACTICAL_DEVICE=NO")

    for path in (QBALL_SOURCE, BASE_SUMMARY, C83_SUMMARY, D273_GREEN):
        require(path)

    d273 = json.loads(D273_GREEN.read_text())
    if not bool(d273.get("translation_zero_mode_artifact_established", False)):
        raise RuntimeError("D273 translation-Goldstone methodology is not GREEN")
    if bool(d273.get("true_physical_instability_established", True)):
        raise RuntimeError("D273 predecessor records a physical instability")

    base_summary = json.loads(BASE_SUMMARY.read_text())
    c83_summary = json.loads(C83_SUMMARY.read_text())
    best = c83_summary["best"]

    omega = float(best["omega"])
    epsilon = float(best["epsilon"])
    chi = float(best["chi"])
    short_x_match = float(best["X_MATCH"])

    # Same mediator range as the inherited 031B2-A theory means mX scales as
    # 1/epsilon. This value is only used for provenance/optional time units.
    base_best = base_summary["best"]
    m_x_gev = (
        float(base_best["m_x_gev"])
        * float(base_best["epsilon"])
        / epsilon
    )

    long_x_match = LONG_MU_R / epsilon

    print(f"OMEGA={omega:.15e}")
    print(f"EPSILON={epsilon:.15e}")
    print(f"CHI={chi:.15e}")
    print(f"SHORT_X_MATCH={short_x_match:.15e}")
    print(f"LONG_X_MATCH={long_x_match:.15e}")
    print(f"M_X_GEV_DERIVED={m_x_gev:.15e}")
    print(f"OPERATING_ENERGY_J={float(best['ceiling_E_J']):.15e}")
    print(f"CENTERED_REFERENCE_ENERGY_J={float(best['centered_E_J']):.15e}")
    print(f"OPERATING_SHIFT_M={float(best['max_shift_m']):.15e}")
    print(f"OPERATING_ALPHA_M={float(best['ceiling_alpha_m']):.15e}")
    print(f"OPERATING_SOURCE_LEAK={float(best['source_leak']):.15e}")
    print(f"OPERATING_BACKREACTION={float(best['ceiling_backreaction']):.15e}")
    print(f"E_OVER_QMX={float(best['E_over_QmX']):.15e}")
    print(f"SCALAR_HESSIAN_STORED={float(best['scalar_hessian']):.15e}")

    print("\n=== STAGE A: SHORT/LONG BACKGROUND RECONSTRUCTION ===")

    qmod = load_module("d96_qball", QBALL_SOURCE)

    short_solution = solve_background(
        qmod,
        omega,
        epsilon,
        chi,
        short_x_match,
    )

    long_solution = solve_background(
        qmod,
        omega,
        epsilon,
        chi,
        long_x_match,
    )

    core_x = np.linspace(0.0, BROAD_RMAX, 2001)
    short_state = short_solution.sol(core_x)
    long_state = long_solution.sol(core_x)

    y_rel_l2 = rel_l2(short_state[0], long_state[0])
    u_rel_l2 = rel_l2(short_state[2], long_state[2])
    y_center_rel = rel_scalar(float(short_state[0, 0]), float(long_state[0, 0]))
    u_center_rel = rel_scalar(float(short_state[2, 0]), float(long_state[2, 0]))

    background_pass = bool(
        max(y_rel_l2, u_rel_l2, y_center_rel, u_center_rel)
        <= BACKGROUND_CORE_REL_TOL
    )

    print(
        f"BACKGROUND Y_REL_L2={y_rel_l2:.15e} "
        f"U_REL_L2={u_rel_l2:.15e} "
        f"Y_CENTER_REL={y_center_rel:.15e} "
        f"U_CENTER_REL={u_center_rel:.15e} "
        f"PASS={background_pass}"
    )

    print("\n=== STAGE B: COMPLETE DENSE l=0..8 BROAD SPECTRUM ===")

    broad_rows: list[dict[str, Any]] = []
    broad_by_h: dict[str, dict[str, float]] = {}

    for h_target in BROAD_H_TARGETS:
        grid_key = f"{h_target:.9f}"
        broad_by_h[grid_key] = {}

        for ell in range(LMAX + 1):
            bundle = build_fv_bundle(
                qmod,
                long_solution,
                omega,
                epsilon,
                chi,
                ell,
                BROAD_RMAX,
                h_target,
            )
            growth, values = dense_growth(bundle["operator"])
            broad_by_h[grid_key][str(ell)] = growth

            row = {
                "h_target": h_target,
                "h": bundle["h"],
                "cells": bundle["cells"],
                "rmax": BROAD_RMAX,
                "epsilon_rmax": epsilon * BROAD_RMAX,
                "ell": ell,
                "max_real_growth": growth,
                "translation_sector": ell == 1,
                "beta_x": bundle["beta_x"],
                "beta_u": bundle["beta_u"],
            }
            broad_rows.append(row)

            print(
                f"BROAD H={bundle['h']:.9f} N={bundle['cells']} "
                f"L={ell} MAX_RE_S={growth:.15e} "
                f"TRANSLATION_SECTOR={ell == 1}"
            )

    nontranslation_broad_max = max(
        row["max_real_growth"]
        for row in broad_rows
        if not row["translation_sector"]
    )

    h0_key = f"{BROAD_H_TARGETS[0]:.9f}"
    h1_key = f"{BROAD_H_TARGETS[1]:.9f}"
    nontranslation_grid_diff = max(
        abs(
            broad_by_h[h0_key][str(ell)]
            - broad_by_h[h1_key][str(ell)]
        )
        for ell in range(LMAX + 1)
        if ell != 1
    )

    broad_pass = bool(
        nontranslation_broad_max <= NONTRANSLATION_GROWTH_TOL
        and nontranslation_grid_diff <= NONTRANSLATION_GRID_DIFF_TOL
    )

    print(f"NONTRANSLATION_BROAD_MAX_RE={nontranslation_broad_max:.15e}")
    print(f"NONTRANSLATION_GRID_DIFF={nontranslation_grid_diff:.15e}")
    print(f"BROAD_L0_L2_TO_L8_PASS={broad_pass}")

    print("\n=== STAGE C: l=1 GOLDSTONE h->0 + DOMAIN AUDIT ===")

    l1_rows: list[dict[str, Any]] = []

    cases = [
        (L1_PRIMARY_MU_R, h)
        for h in L1_PRIMARY_H_TARGETS
    ] + [
        (L1_CHECK_MU_R, h)
        for h in L1_CHECK_H_TARGETS
    ]

    for mu_r, h_target in cases:
        rmax = mu_r / epsilon
        bundle = build_fv_bundle(
            qmod,
            long_solution,
            omega,
            epsilon,
            chi,
            1,
            rmax,
            h_target,
        )

        residual = translation_residual(bundle)
        dynamic = nearzero_dynamic(bundle)
        projected = projected_stiffness(bundle)

        row = {
            "epsilon_rmax": mu_r,
            "rmax": rmax,
            "h_target": h_target,
            "h": bundle["h"],
            "cells": bundle["cells"],
            "translation_growth": dynamic["translation_growth"],
            "translation_overlap": dynamic["translation_overlap"],
            "translation_eig_real": float(dynamic["translation_eigenvalue"].real),
            "translation_eig_imag": float(dynamic["translation_eigenvalue"].imag),
            "low_overlap_nearzero_max_real": dynamic["low_overlap_nearzero_max_real"],
            "translation_residual_abs": residual["absolute"],
            "translation_residual_rel": residual["relative_frobenius"],
            "translation_rayleigh": residual["rayleigh"],
            "projected_k0": projected["lowest"],
            "projected_k_max_residual": projected["max_residual"],
            "beta_x": bundle["beta_x"],
            "beta_u": bundle["beta_u"],
            "arpack_partial": dynamic["arpack_partial"],
        }
        l1_rows.append(row)

        print(
            f"L1 EPS_R={mu_r:.3f} RMAX={rmax:.6f} "
            f"H={bundle['h']:.9f} N={bundle['cells']} "
            f"GROWTH={dynamic['translation_growth']:.15e} "
            f"OVERLAP={dynamic['translation_overlap']:.9f} "
            f"RELRES={residual['relative_frobenius']:.15e} "
            f"LOWOV_MAXRE={dynamic['low_overlap_nearzero_max_real']:.15e} "
            f"KPROJ0={projected['lowest']:.15e} "
            f"KPROJ_RES={projected['max_residual']:.15e}"
        )

    primary_rows = [
        row for row in l1_rows
        if math.isclose(
            float(row["epsilon_rmax"]),
            L1_PRIMARY_MU_R,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        )
    ]
    fit = fit_continuum(primary_rows)

    domain_spreads = {}
    for h_target in L1_CHECK_H_TARGETS:
        primary = min(
            primary_rows,
            key=lambda row: abs(float(row["h_target"]) - h_target),
        )
        check_candidates = [
            row for row in l1_rows
            if math.isclose(
                float(row["epsilon_rmax"]),
                L1_CHECK_MU_R,
                rel_tol=0.0,
                abs_tol=1.0e-12,
            )
        ]
        check = min(
            check_candidates,
            key=lambda row: abs(float(row["h_target"]) - h_target),
        )
        spread = abs(
            float(primary["translation_growth"])
            - float(check["translation_growth"])
        ) / max(
            abs(float(primary["translation_growth"])),
            abs(float(check["translation_growth"])),
            1.0e-300,
        )
        domain_spreads[f"{h_target:.6f}"] = spread

    max_domain_spread = max(domain_spreads.values())
    min_overlap = min(float(row["translation_overlap"]) for row in l1_rows)
    max_low_overlap_real = max(
        float(row["low_overlap_nearzero_max_real"]) for row in l1_rows
    )
    min_projected_k = min(float(row["projected_k0"]) for row in l1_rows)
    max_projected_residual = max(
        float(row["projected_k_max_residual"]) for row in l1_rows
    )

    l1_pass = bool(
        GROWTH_POWER_MIN <= fit["growth_power"] <= GROWTH_POWER_MAX
        and fit["residual_power"] >= RESIDUAL_POWER_MIN
        and fit["s_over_h_cv"] <= S_OVER_H_CV_MAX
        and fit["linear_intercept_over_finest_growth"] <= ZERO_INTERCEPT_RATIO_MAX
        and fit["quadratic_intercept_over_finest_growth"] <= ZERO_INTERCEPT_RATIO_MAX
        and fit["growth_monotone"]
        and fit["residual_monotone"]
        and max_domain_spread <= DOMAIN_SPREAD_MAX
        and min_overlap >= TRANSLATION_OVERLAP_MIN
        and max_low_overlap_real <= LOW_OVERLAP_GROWTH_TOL
        and min_projected_k >= PROJECTED_K_MIN_TOL
        and max_projected_residual <= PROJECTED_EIG_RESIDUAL_TOL
    )

    print("\n=== STAGE D: CONTINUUM LEDGER ===")
    print(f"L1_GROWTH_POWER={fit['growth_power']:.15e}")
    print(f"L1_RESIDUAL_POWER={fit['residual_power']:.15e}")
    print(f"L1_S_OVER_H_CV={fit['s_over_h_cv']:.15e}")
    print(f"L1_LINEAR_INTERCEPT={fit['linear_intercept']:.15e}")
    print(
        "L1_LINEAR_INTERCEPT_RATIO="
        f"{fit['linear_intercept_over_finest_growth']:.15e}"
    )
    print(f"L1_QUADRATIC_INTERCEPT={fit['quadratic_intercept']:.15e}")
    print(
        "L1_QUADRATIC_INTERCEPT_RATIO="
        f"{fit['quadratic_intercept_over_finest_growth']:.15e}"
    )
    print(f"L1_MIN_TRANSLATION_OVERLAP={min_overlap:.15e}")
    print(f"L1_MAX_LOW_OVERLAP_REAL={max_low_overlap_real:.15e}")
    print(f"L1_MIN_PROJECTED_K={min_projected_k:.15e}")
    print(f"L1_MAX_PROJECTED_EIG_RESIDUAL={max_projected_residual:.15e}")
    print(f"L1_DOMAIN_SPREADS={json.dumps(domain_spreads, sort_keys=True)}")
    print(f"L1_TRANSLATION_GOLDSTONE_PASS={l1_pass}")

    # ------------------------------------------------------------------
    # Decision: RED only for a distinct reproducible physical instability.
    # Otherwise a numerical subgate failure remains YELLOW.
    # ------------------------------------------------------------------
    distinct_l1_instability = bool(
        max_low_overlap_real > 1.0e-6
    )

    negative_projected_direction = bool(
        min_projected_k < -1.0e-6
    )

    reproducible_nontranslation_instability = False
    for ell in range(LMAX + 1):
        if ell == 1:
            continue
        g0 = broad_by_h[h0_key][str(ell)]
        g1 = broad_by_h[h1_key][str(ell)]
        if g0 > 1.0e-6 and g1 > 1.0e-6:
            relative_difference = abs(g0 - g1) / max(abs(g0), abs(g1), 1.0e-300)
            if relative_difference < 0.25:
                reproducible_nontranslation_instability = True

    true_instability = bool(
        distinct_l1_instability
        or negative_projected_direction
        or reproducible_nontranslation_instability
    )

    all_green = bool(background_pass and broad_pass and l1_pass and not true_instability)

    if true_instability:
        classification = (
            "RED_96GJ_INTRINSIC_QBALL_COUPLED_LINEAR_INSTABILITY_ESTABLISHED"
        )
        next_step = (
            "DEMOTE_96GJ_OPERATING_CANDIDATE_AND_RETAIN_273GJ_STABLE_ANCHOR"
        )
    elif all_green:
        classification = (
            "GREEN_96GJ_INTRINSIC_QBALL_COUPLED_LINEAR_L0_TO_L8_"
            "WITH_L1_TRANSLATIONAL_GOLDSTONE_REMOVED"
        )
        next_step = (
            "031C96_OPERATING_MARGIN_ROBUSTNESS_FIXED_THEORY_AND_THRESHOLD_"
            "SENSITIVITY_GATE"
        )
    else:
        classification = (
            "YELLOW_96GJ_COUPLED_LINEAR_CERTIFICATION_NUMERICALLY_UNRESOLVED"
        )
        next_step = "REFINE_ONLY_FAILED_96GJ_STABILITY_SUBGATE"

    print("\n=== FINAL D96 DECISION ===")
    print(f"BACKGROUND_RECONSTRUCTION_PASS={background_pass}")
    print(f"BROAD_L0_L2_TO_L8_PASS={broad_pass}")
    print(f"L1_TRANSLATION_GOLDSTONE_PASS={l1_pass}")
    print(f"DISTINCT_L1_INSTABILITY={distinct_l1_instability}")
    print(f"NEGATIVE_TRANSLATION_PROJECTED_STIFFNESS={negative_projected_direction}")
    print(
        "REPRODUCIBLE_NONTRANSLATION_INSTABILITY="
        f"{reproducible_nontranslation_instability}"
    )
    print(f"TRUE_PHYSICAL_INSTABILITY_ESTABLISHED={true_instability}")
    print(f"031B2D96_CLASSIFICATION={classification}")
    print(f"NEXT={next_step}")
    print("NONLINEAR_FRAGMENTATION_CLOSED=NO")
    print("OPERATING_MARGIN_ROBUSTNESS_CLOSED=NO")
    print("ACTIVATION_OFFSTATE_CLOSED=NO")
    print("FULL_METRIC_BACKREACTION_CLOSED=NO")
    print("RADIATIVE_NATURALNESS_CLOSED=NO")
    print("EMPIRICAL_FIFTH_FORCE_CLOSURE=NO")
    print("PRACTICAL_DEVICE=NO")

    with OUT_BROAD_CSV.open("w", newline="") as handle:
        fieldnames = list(broad_rows[0].keys())
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(broad_rows)

    with OUT_L1_CSV.open("w", newline="") as handle:
        fieldnames = list(l1_rows[0].keys())
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(l1_rows)

    output = {
        "claim_class": (
            "96GJ_OPERATING_CANDIDATE_INTRINSIC_SPHERICAL_SOURCE_"
            "COUPLED_LINEAR_STABILITY_CERTIFICATION"
        ),
        "candidate": {
            "omega": omega,
            "epsilon": epsilon,
            "chi": chi,
            "chi_factor": float(best["chi_factor"]),
            "m_x_gev_derived": m_x_gev,
            "operating_energy_J": float(best["ceiling_E_J"]),
            "centered_reference_energy_J": float(best["centered_E_J"]),
            "operating_shift_m": float(best["max_shift_m"]),
            "operating_alpha_m": float(best["ceiling_alpha_m"]),
            "operating_source_leak": float(best["source_leak"]),
            "operating_backreaction": float(best["ceiling_backreaction"]),
            "payload_overlap": float(best["payload_overlap"]),
            "E_over_QmX": float(best["E_over_QmX"]),
            "stored_scalar_hessian": float(best["scalar_hessian"]),
            "stored_conservation_rel": float(best["conservation_rel"]),
        },
        "provenance": {
            "qball_source": str(QBALL_SOURCE.relative_to(ROOT)),
            "qball_source_sha256": sha256(QBALL_SOURCE),
            "base_summary": str(BASE_SUMMARY.relative_to(ROOT)),
            "base_summary_sha256": sha256(BASE_SUMMARY),
            "c83_summary": str(C83_SUMMARY.relative_to(ROOT)),
            "c83_summary_sha256": sha256(C83_SUMMARY),
            "d273_green_summary": str(D273_GREEN.relative_to(ROOT)),
            "d273_green_summary_sha256": sha256(D273_GREEN),
        },
        "background": {
            "short_x_match": short_x_match,
            "long_x_match": long_x_match,
            "y_rel_l2": y_rel_l2,
            "u_rel_l2": u_rel_l2,
            "y_center_rel": y_center_rel,
            "u_center_rel": u_center_rel,
            "pass": background_pass,
        },
        "broad_spectrum": {
            "rmax": BROAD_RMAX,
            "h_targets": BROAD_H_TARGETS,
            "rows": broad_rows,
            "nontranslation_max_real": nontranslation_broad_max,
            "nontranslation_grid_difference": nontranslation_grid_diff,
            "pass": broad_pass,
        },
        "l1_goldstone": {
            "rows": l1_rows,
            "primary_fit": fit,
            "domain_spreads": domain_spreads,
            "minimum_translation_overlap": min_overlap,
            "maximum_low_overlap_real": max_low_overlap_real,
            "minimum_projected_stiffness": min_projected_k,
            "maximum_projected_eigen_residual": max_projected_residual,
            "pass": l1_pass,
        },
        "true_physical_instability_established": true_instability,
        "classification": classification,
        "next": next_step,
        "claim_limits": [
            "This certifies only intrinsic coupled-linear spherical-source stability through l=8 within the declared effective model.",
            "The l=1 translational Goldstone mode is treated by analytic-mode overlap, h-to-zero convergence, domain checks, and translation-orthogonal stiffness.",
            "Rigid source translation and payload alpha_m do not enter the isolated intrinsic source spectrum.",
            "The 96.141-GJ operating point remains near declared source-leak and payload-backreaction limits and requires a separate robustness gate.",
            "Finite-amplitude fragmentation and fission remain open.",
            "Activation/off-state remains open.",
            "Full physical-metric backreaction remains open.",
            "Radiative naturalness and empirical fifth-force/EP/PPN closure remain open.",
            "No practical device or experimental new force is established.",
        ],
    }

    OUT_JSON.write_text(
        json.dumps(to_builtin(output), indent=2, sort_keys=True) + "\n"
    )

    print(f"SUMMARY_JSON={OUT_JSON.resolve()}")
    print(f"BROAD_CSV={OUT_BROAD_CSV.resolve()}")
    print(f"L1_CSV={OUT_L1_CSV.resolve()}")


if __name__ == "__main__":
    main()
