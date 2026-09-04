#!/usr/bin/env python3
"""
031B2-D273-TZ — translational Goldstone-mode audit and l=1 certification gate.

PURPOSE
-------
Resolve the only anomalous angular sector in the dense 273-GJ coupled spectrum
without changing the microscopic theory or optimizing the source.

SCIENTIFIC QUESTION
-------------------
Is the positive l=1 growth seen by 031B2-D273-R a genuine coupled instability,
or is it finite-domain/discretization splitting of the exact translational
Goldstone zero mode of the isolated spherical Q-ball + scalar solution?


PHYSICAL MODEL / FIELD CONTENT
------------------------------
The frozen 273-GJ global U(1) Q-ball background is

    X = y(r) exp(-i omega t),    phi = M u(r),

with the same even-Z2 scalar coupling and fixed theory used by 031B2-A/C273/D273-R.
Perturbations are the coupled co-rotating Q-ball amplitude a, phase b, and
canonically normalized scalar variable w. No new interaction is introduced.

EQUATIONS / REPRESENTATION
--------------------------
For l=1 the D273-R quadratic problem is

    (s^2 I + s G + K) q = 0,

with symmetric K and skew G. The radial operator acts on reduced variables
r times the physical spherical-harmonic amplitudes. The analytic translation
configuration is therefore q_T=(r y', 0, r u'/chi).

SIGN CONVENTIONS / UNITS
------------------------
Dimensionless Q-ball coordinates and natural-unit spectral growth s are used.
Positive Re(s) denotes exponential growth. The reported physical growth rate
uses the same GeV-to-s conversion as D273-R.

INPUTS
------
simulations/031b2a_global_qball_activated_scalar_control.py
results/data/031b2a_global_qball_activated_scalar_control_summary.json

OUTPUTS
-------
results/data/031b2d273tz_translation_zero_mode_summary.json
results/data/031b2d273tz_domain_grid_scan.csv
results/data/031b2d273tz_translation_mode_vectors.npz

ASSUMPTIONS / APPROXIMATION LEVEL
---------------------------------
Flat-background microscopic matter plus scalar, linear perturbations, spherical
background, l=1 only in this diagnostic. Payload and physical metric are not
dynamical perturbation degrees of freedom here.

BOUNDARY CONDITIONS
-------------------
The historical hard-wall problem is reproduced first. The independent audit
then uses regular reduced-variable behavior q(0)=0 and l=1 Yukawa/Robin tails.

CONSERVATION / STABILITY OR NATURALNESS
---------------------------------------
The background inherits the previously audited stationary/conservation state.
This file tests coupled linear l=1 stability only; nonlinear stability and
radiative naturalness remain open.

NUMERICAL METHOD / VALIDATION STRATEGY
--------------------------------------
Reproduce D273-R exactly at N=120/160, compare against its historical growth,
measure analytic-mode overlap/residual, project translation only after that
audit, then independently rebuild the operator with symmetric finite volume,
enlarged domains, Robin tails, grid refinement, constrained LOBPCG, and sparse
shift-invert dynamic checks.

FALSIFICATION STRATEGY
----------------------
Require convergence behavior rather than one favorable grid. A distinct
low-overlap positive dynamic mode must persist on the two largest domains to
count as a physical-instability candidate.

LIMITATIONS / RELATED FILES
---------------------------
Related: 031b2d273r_dense_coupled_linear_mode_gate.py and
031b2c273_qball_fixed_theory_certification_preflight.py. This run does not
replace nonlinear fragmentation, activation/off-state, full metric, EFT, or
empirical gates.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_031B2_D273_TRANSLATIONAL_ZERO_MODE_AND_L1_CERTIFICATION_GATE

This file deliberately combines the next several cheapest decisive checks:

1. Reproduce the historical D273-R N=120/N=160 Dirichlet l=1 growth.
2. Construct the analytic translation vector in the SAME reduced/canonical
   variables used by D273-R:

       a_trans = r y'(r)
       b_trans = 0
       w_trans = r u'(r) / chi

   because D273-R uses v = chi*w and its radial Schrodinger-form operator acts
   on r times the physical l=1 perturbation.
3. Measure the discrete zero-mode residual and overlap of the apparent growing
   eigenvector with the analytic translation vector.
4. Explicitly project the analytic translation direction out of the legacy
   N=120/N=160 dense problem and recompute the full remaining l=1 spectrum.
5. Independently rebuild l=1 with a symmetric cell-centered finite-volume
   radial operator and physical asymptotic Robin/Yukawa conditions.
6. Repeat that independent operator at epsilon*Rmax ~= 1.2, 3, 5, 8 and at two
   grid spacings, while keeping the background on one large Robin domain.
7. Use a translation-constrained symmetric stiffness solve to test the lowest
   nontranslation l=1 directions on the enlarged domains.
8. Use sparse shift-invert first-order solves near s=0 to track the
   translation-associated dynamic eigenvalue and its overlap.

For a physical l=1 Yukawa tail f ~ k_1(mu r), the reduced variable q=r f obeys
asymptotically

    q' + beta_1 q = 0,

with

    beta_1 = mu + 1 / [R (mu R + 1)].

This is the l=1 refinement of the generic Yukawa Robin condition in the
carry-forward notes. It tends to q' + mu q = 0 at large radius.

PROMOTION CONDITION
-------------------
A translation-artifact interpretation is supported only if the historical
positive mode is strongly aligned with the analytic translation vector, its
zero-mode residual/growth decrease with refinement/domain improvement, and the
translation-constrained l=1 stiffness has no negative direction. The legacy
translation-projected dense dynamic spectrum must also show no significant
remaining positive growth.

FALSIFIER / STOP RULE
---------------------
A distinct low-overlap l=1 mode that converges to finite positive Re(s), or a
converged negative translation-constrained stiffness mode, blocks promotion.
Do not tune around such a result.

CLAIM LIMITS
------------
This is a coupled LINEAR l=1 stability gate only. It does not establish
finite-amplitude fragmentation stability, radiative naturalness, activation,
empirical fifth-force closure, full physical-metric backreaction, or a device.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
import warnings
from pathlib import Path
from typing import Any

import numpy as np

from scipy.linalg import eig, eigvals, eigh, null_space
from scipy.sparse import bmat, csr_matrix, diags, identity
from scipy.sparse.linalg import ArpackNoConvergence, eigs, lobpcg


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

UPSTREAM = SIM / "031b2a_global_qball_activated_scalar_control.py"
SUMMARY = DATA / "031b2a_global_qball_activated_scalar_control_summary.json"

OUT_JSON = DATA / "031b2d273tz_translation_zero_mode_summary.json"
OUT_CSV = DATA / "031b2d273tz_domain_grid_scan.csv"
OUT_NPZ = DATA / "031b2d273tz_translation_mode_vectors.npz"

LEGACY_RMAX = 60.0
LEGACY_N = (120, 160)
HISTORICAL_GROWTH = {
    120: 1.04047816e-2,
    160: 7.52246363e-3,
}

# Physical scalar Compton-length domain tests for epsilon=0.02 become
# Rmax = 60, 150, 250, 400. Values are generated from epsilon at runtime.
MU_R_VALUES = (3.0, 5.0)
H_TARGETS = (0.25, 0.1875)

GROWTH_TOL = 1.0e-4
OVERLAP_STRONG = 0.90
LEGACY_REPRO_REL_TOL = 3.0e-4
PROJECTED_K_MARGIN = 1.0e-6
LOBPCG_RESIDUAL_TOL = 2.0e-5
BACKGROUND_CORE_REL_TOL = 2.0e-3

HBAR_GEV_S = 6.582119569e-25


def require(path: Path) -> None:
    """Fail closed when a required source/result artifact is missing."""

    if not path.is_file():
        raise RuntimeError(f"Missing required file: {path}")


def sha256(path: Path) -> str:
    """Return SHA-256 for one provenance input."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head() -> str:
    """Return current git HEAD when available without making it a run blocker."""

    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return "UNKNOWN"


def load_module(name: str, path: Path):
    """Import a repository simulation without invoking its main function."""

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def to_builtin(value: Any):
    """Recursively convert NumPy/complex values to JSON-safe builtins."""

    # Complex must be handled BEFORE generic NumPy scalars. This explicitly
    # repairs the D273-R serialization pathology recorded in the last session.
    if isinstance(value, (complex, np.complexfloating)):
        return {
            "real": float(np.real(value)),
            "imag": float(np.imag(value)),
        }
    if isinstance(value, np.generic):
        return to_builtin(value.item())
    if isinstance(value, np.ndarray):
        return [to_builtin(v) for v in value.tolist()]
    if isinstance(value, dict):
        return {str(k): to_builtin(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_builtin(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        if math.isnan(value):
            return "nan"
        return "inf" if value > 0.0 else "-inf"
    return value


def safe_rel(a: float, b: float) -> float:
    """Symmetric relative difference."""

    return abs(a - b) / max(abs(a), abs(b), 1.0e-300)


def overlap(a: np.ndarray, b: np.ndarray) -> float:
    """Absolute normalized complex inner-product overlap."""

    den = np.linalg.norm(a) * np.linalg.norm(b)
    if den <= 1.0e-300:
        return 0.0
    return float(abs(np.vdot(a, b)) / den)


def reconstruct(qmod, best, match: float):
    """Reconstruct the fixed-theory background on a requested Robin domain."""

    omega = float(best["omega"])
    epsilon = float(best["epsilon"])
    chi = float(best["chi"])

    old_match = float(qmod.X_MATCH)
    qmod.X_MATCH = float(match)

    try:
        seed = qmod.solve_uncoupled_qball(omega)
        if seed is None:
            raise RuntimeError(
                f"Uncoupled Q-ball reconstruction failed at X_MATCH={match}"
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
                f"Coupled Q-ball reconstruction failed at X_MATCH={match}"
            )
    finally:
        qmod.X_MATCH = old_match

    return omega, epsilon, chi, solution


def potentials(qmod, solution, omega, epsilon, chi, r):
    """Return D273-R canonical l-independent potential/coupling arrays."""

    state = solution.sol(np.maximum(r, 1.0e-5))
    y = state[0]
    yp = state[1]
    u = state[2]
    up = state[3]

    A = np.exp(np.clip(-0.5 * u**2, -700.0, 0.0))
    denominator = 1.0 + y**2

    Va = A * (1.0 - y**2) / denominator**2 - omega**2
    Vb = A / denominator - omega**2
    Vv = (
        epsilon**2
        + chi**2 * A * qmod.W(y) * (u**2 - 1.0)
    )
    coupling = -chi * u * A * y / denominator

    return y, yp, u, up, Va, Vb, Vv, coupling


def assemble_first_order(K: csr_matrix, G: csr_matrix) -> csr_matrix:
    """Linearize (s^2 I + s G + K)X=0 into first-order form."""

    dim = K.shape[0]
    Z = csr_matrix((dim, dim))
    I = identity(dim, format="csr")
    return bmat(((Z, I), (-K, -G)), format="csr")


def gyroscopic_matrix(count: int, omega: float) -> csr_matrix:
    """Return the canonical amplitude/phase gyroscopic matrix."""

    Z = csr_matrix((count, count))
    I = identity(count, format="csr")
    return bmat(
        (
            (Z, 2.0 * omega * I, Z),
            (-2.0 * omega * I, Z, Z),
            (Z, Z, Z),
        ),
        format="csr",
    )


def build_legacy_node_dirichlet(
    qmod,
    solution,
    omega: float,
    epsilon: float,
    chi: float,
    n: int,
    rmax: float = LEGACY_RMAX,
):
    """Exactly rebuild the active D273-R canonical node/Dirichlet l=1 operator."""

    r = np.linspace(0.0, rmax, n)
    h = float(r[1] - r[0])
    ri = r[1:-1]
    count = len(ri)

    y, yp, u, up, Va, Vb, Vv, coupling = potentials(
        qmod, solution, omega, epsilon, chi, ri
    )

    angular = 2.0 / ri**2
    diag = np.full(count, 2.0 / h**2)
    off = np.full(count - 1, -1.0 / h**2)
    T = diags((off, diag, off), (-1, 0, 1), format="csr")

    La = T + diags(angular + Va, 0, format="csr")
    Lb = T + diags(angular + Vb, 0, format="csr")
    Lv = T + diags(angular + Vv, 0, format="csr")

    Z = csr_matrix((count, count))
    B = diags(coupling, 0, format="csr")
    K = bmat(((La, Z, B), (Z, Lb, Z), (B, Z, Lv)), format="csr")
    G = gyroscopic_matrix(count, omega)
    A = assemble_first_order(K, G)

    # D273-R uses reduced radial variables and v=chi*w.
    t = np.concatenate(
        (
            ri * yp,
            np.zeros_like(ri),
            ri * up / chi,
        )
    )

    return {
        "r": ri,
        "h": h,
        "K": K,
        "G": G,
        "A": A,
        "translation": t,
        "background": (y, u),
    }


def operator_residual(K: csr_matrix, t: np.ndarray, count: int) -> dict[str, float]:
    """Measure absolute/relative translation zero-mode residual and localization."""

    kt = np.asarray(K @ t)
    tnorm = max(float(np.linalg.norm(t)), 1.0e-300)
    abs_res = float(np.linalg.norm(kt) / tnorm)

    fro = math.sqrt(float(np.sum(np.abs(K.data) ** 2)))
    rel_res = float(np.linalg.norm(kt) / max(fro * tnorm, 1.0e-300))

    rayleigh = float(np.real(np.vdot(t, kt)) / max(np.vdot(t, t).real, 1.0e-300))

    # Residual energy localization by radial deciles, summed over all 3 fields.
    block = kt.reshape(3, count)
    sq = np.sum(np.abs(block) ** 2, axis=0)
    total = max(float(np.sum(sq)), 1.0e-300)
    cut = max(1, count // 10)

    return {
        "absolute_residual": abs_res,
        "relative_frobenius_residual": rel_res,
        "rayleigh": rayleigh,
        "inner_10pct_residual_fraction": float(np.sum(sq[:cut]) / total),
        "outer_10pct_residual_fraction": float(np.sum(sq[-cut:]) / total),
    }


def dense_legacy_spectrum(bundle: dict, n: int) -> dict:
    """Compute the complete legacy l=1 spectrum and translation overlap."""

    A = bundle["A"].toarray()
    K = bundle["K"].toarray()
    G = bundle["G"].toarray()
    t = np.asarray(bundle["translation"], dtype=float)
    m = len(t)

    values, vectors = eig(
        A,
        left=False,
        right=True,
        overwrite_a=True,
        check_finite=False,
    )
    order = np.argsort(values.real)[::-1]
    values = values[order]
    vectors = vectors[:, order]

    config_overlaps = np.array(
        [overlap(t, vectors[:m, j]) for j in range(vectors.shape[1])],
        dtype=float,
    )

    max_growth_idx = int(np.argmax(values.real))
    max_overlap_idx = int(np.argmax(config_overlaps))

    # Prefer the positive-real member of the translation-associated +/- pair
    # when several vectors have essentially the same translation overlap.
    max_ov = float(config_overlaps[max_overlap_idx])
    near_translation = np.where(config_overlaps >= max(0.95 * max_ov, 0.5))[0]
    if len(near_translation):
        trans_idx = int(
            near_translation[np.argmax(values[near_translation].real)]
        )
    else:
        trans_idx = max_overlap_idx

    residual = operator_residual(bundle["K"], t, len(bundle["r"]))

    # Exact Euclidean translation projection for the small legacy dense cases.
    tn = t / max(np.linalg.norm(t), 1.0e-300)
    Q = null_space(tn.reshape(1, -1), rcond=1.0e-12)
    Kp = Q.T @ K @ Q
    Gp = Q.T @ G @ Q
    d = Kp.shape[0]
    Ap = np.block(
        [
            [np.zeros((d, d)), np.eye(d)],
            [-Kp, -Gp],
        ]
    )
    projected_values = eigvals(
        Ap,
        overwrite_a=True,
        check_finite=False,
    )
    projected_growth = float(np.max(projected_values.real))
    projected_k_low = eigh(
        Kp,
        eigvals_only=True,
        subset_by_index=(0, min(4, d - 1)),
        check_finite=False,
    )

    growth = float(values[max_growth_idx].real)
    expected = HISTORICAL_GROWTH[n]
    repro_rel = abs(growth - expected) / max(abs(expected), 1.0e-300)

    return {
        "n": n,
        "h": float(bundle["h"]),
        "growth": growth,
        "historical_growth": expected,
        "historical_reproduction_relerr": repro_rel,
        "historical_reproduction_pass": bool(repro_rel <= LEGACY_REPRO_REL_TOL),
        "growing_mode_eigenvalue": values[max_growth_idx],
        "growing_mode_translation_overlap": float(config_overlaps[max_growth_idx]),
        "translation_associated_eigenvalue": values[trans_idx],
        "translation_associated_overlap": float(config_overlaps[trans_idx]),
        "max_translation_overlap": max_ov,
        "translation_residual": residual,
        "projected_dynamic_max_growth": projected_growth,
        "projected_dynamic_pass": bool(projected_growth <= GROWTH_TOL),
        "projected_lowest_stiffness": projected_k_low,
        "leading_eigenvalues": values[:12],
        "translation_mode_config_vector": vectors[:m, trans_idx],
    }


def beta_reduced_l1(mu: float, radius: float) -> float:
    """Exact asymptotic l=1 reduced-variable Robin logarithmic decay rate."""

    z = max(mu * radius, 1.0e-12)
    return float(mu + 1.0 / (radius * (z + 1.0)))


def fv_minus_d2(count: int, h: float, beta_outer: float) -> csr_matrix:
    """Symmetric cell-centered -d^2/dr^2 with q(0)=0 and outer Robin flux."""

    if count < 8:
        raise ValueError("Too few finite-volume cells")

    diag = np.full(count, 2.0 / h**2)
    off = np.full(count - 1, -1.0 / h**2)

    # Inner Dirichlet face q(0)=0 at half a cell from the first center.
    diag[0] = 3.0 / h**2

    # Outer Robin face q' + beta*q = 0. Eliminating the face value from the
    # finite-volume flux keeps the matrix symmetric and second-order in the
    # interior while avoiding a hard Dirichlet wall.
    diag[-1] = (
        1.0 / h**2
        + beta_outer / (h * (1.0 + 0.5 * beta_outer * h))
    )

    return diags((off, diag, off), (-1, 0, 1), format="csr")


def build_fv_robin_l1(
    qmod,
    solution,
    omega: float,
    epsilon: float,
    chi: float,
    radius: float,
    h_target: float,
):
    """Independent symmetric finite-volume l=1 canonical operator."""

    count = max(16, int(round(radius / h_target)))
    h = float(radius / count)
    r = (np.arange(count, dtype=float) + 0.5) * h

    y, yp, u, up, Va, Vb, Vv, coupling = potentials(
        qmod, solution, omega, epsilon, chi, r
    )

    kappa_x = math.sqrt(max(1.0 - omega**2, 1.0e-12))
    beta_x = beta_reduced_l1(kappa_x, radius)
    beta_u = beta_reduced_l1(epsilon, radius)

    Tx = fv_minus_d2(count, h, beta_x)
    Tu = fv_minus_d2(count, h, beta_u)
    angular = 2.0 / r**2

    La = Tx + diags(angular + Va, 0, format="csr")
    Lb = Tx + diags(angular + Vb, 0, format="csr")
    Lv = Tu + diags(angular + Vv, 0, format="csr")

    Z = csr_matrix((count, count))
    B = diags(coupling, 0, format="csr")
    K = bmat(((La, Z, B), (Z, Lb, Z), (B, Z, Lv)), format="csr")
    G = gyroscopic_matrix(count, omega)
    A = assemble_first_order(K, G)

    t = np.concatenate(
        (
            r * yp,
            np.zeros_like(r),
            r * up / chi,
        )
    )

    k_sym = float(
        np.linalg.norm((K - K.T).data)
        / max(math.sqrt(float(np.sum(np.abs(K.data) ** 2))), 1.0e-300)
    )
    g_skew = float(
        np.linalg.norm((G + G.T).data)
        / max(math.sqrt(float(np.sum(np.abs(G.data) ** 2))), 1.0e-300)
    )

    if k_sym > 1.0e-12 or g_skew > 1.0e-12:
        raise RuntimeError(
            f"FV canonical structure failed: K_SYM={k_sym}, G_SKEW={g_skew}"
        )

    return {
        "r": r,
        "h": h,
        "count": count,
        "K": K,
        "G": G,
        "A": A,
        "translation": t,
        "beta_x": beta_x,
        "beta_u": beta_u,
        "background": (y, u),
    }


def constrained_stiffness(K: csr_matrix, t: np.ndarray, modes: int = 4) -> dict:
    """Compute the lowest K eigenvalues subject to exact t-orthogonality."""

    m = K.shape[0]
    k = min(modes, max(1, m - 2))
    tn = np.asarray(t, dtype=float)
    tn /= max(np.linalg.norm(tn), 1.0e-300)

    rng = np.random.default_rng(273031)
    X = rng.standard_normal((m, k))
    X -= tn[:, None] * (tn @ X)[None, :]
    X, _ = np.linalg.qr(X)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        values, vectors, residual_history = lobpcg(
            K,
            X,
            Y=tn[:, None],
            largest=False,
            tol=2.0e-8,
            maxiter=500,
            retResidualNormsHistory=True,
        )

    order = np.argsort(values)
    values = np.asarray(values)[order]
    vectors = np.asarray(vectors)[:, order]

    direct_residuals = np.array(
        [
            np.linalg.norm(K @ vectors[:, j] - values[j] * vectors[:, j])
            for j in range(vectors.shape[1])
        ],
        dtype=float,
    )
    constraint_overlaps = np.array(
        [overlap(tn, vectors[:, j]) for j in range(vectors.shape[1])],
        dtype=float,
    )

    return {
        "eigenvalues": values,
        "direct_residuals": direct_residuals,
        "constraint_overlaps": constraint_overlaps,
        "lowest": float(values[0]),
        "lowest_residual": float(direct_residuals[0]),
        "positive_margin_pass": bool(
            values[0] > PROJECTED_K_MARGIN
            and direct_residuals[0] <= LOBPCG_RESIDUAL_TOL
        ),
        "warnings": [str(w.message) for w in caught],
        "residual_history_tail": np.asarray(residual_history)[-5:],
    }


def near_zero_dynamic(A: csr_matrix, t: np.ndarray) -> dict:
    """Track the low-frequency first-order modes with sparse shift-invert."""

    m = len(t)
    last_error = None
    values = None
    vectors = None
    used_sigma = None

    for sigma in (0.0, 1.0e-10, 1.0e-8, 1.0e-6):
        try:
            values, vectors = eigs(
                A,
                k=min(16, A.shape[0] - 2),
                sigma=sigma,
                which="LM",
                tol=2.0e-9,
                maxiter=30_000,
                return_eigenvectors=True,
            )
            used_sigma = sigma
            break
        except (ArpackNoConvergence, RuntimeError, ValueError) as exc:
            last_error = repr(exc)

    if values is None or vectors is None:
        return {
            "success": False,
            "error": last_error,
        }

    values = np.asarray(values, dtype=complex)
    vectors = np.asarray(vectors, dtype=complex)
    overlaps = np.array(
        [overlap(t, vectors[:m, j]) for j in range(vectors.shape[1])],
        dtype=float,
    )

    max_ov = float(np.max(overlaps))
    high = np.where(overlaps >= max(0.95 * max_ov, 0.5))[0]
    if len(high):
        trans_idx = int(high[np.argmax(values[high].real)])
    else:
        trans_idx = int(np.argmax(overlaps))

    low_overlap = np.where(overlaps < 0.5)[0]
    if len(low_overlap):
        nontrans_max_real = float(np.max(values[low_overlap].real))
    else:
        nontrans_max_real = math.nan

    order = np.argsort(np.abs(values))

    return {
        "success": True,
        "sigma": used_sigma,
        "translation_eigenvalue": values[trans_idx],
        "translation_overlap": float(overlaps[trans_idx]),
        "translation_growth": float(max(values[trans_idx].real, 0.0)),
        "max_overlap": max_ov,
        "low_overlap_nearzero_max_real": nontrans_max_real,
        "eigenvalues_by_abs": values[order],
        "overlaps_by_abs": overlaps[order],
        "translation_mode_config_vector": vectors[:m, trans_idx],
    }


def background_core_difference(sol_a, sol_b, radius: float = 60.0) -> dict[str, float]:
    """Compare two reconstructed backgrounds over the physical core/near tail."""

    r = np.linspace(1.0e-5, radius, 2000)
    a = sol_a.sol(r)
    b = sol_b.sol(r)

    def rel_l2(x, y):
        num = float(np.trapezoid((x - y) ** 2, r))
        den = max(float(np.trapezoid(y**2, r)), 1.0e-300)
        return math.sqrt(num / den)

    return {
        "y_rel_l2": rel_l2(a[0], b[0]),
        "u_rel_l2": rel_l2(a[2], b[2]),
        "y_center_rel": safe_rel(float(a[0, 0]), float(b[0, 0])),
        "u_center_rel": safe_rel(float(a[2, 0]), float(b[2, 0])),
    }


def main() -> None:
    """Execute the combined D273 translation-mode audit."""

    print("=== 031B2-D273-TZ TRANSLATIONAL ZERO-MODE AUDIT ===")
    print(
        "CLAIM_CLASS="
        "D273_L1_TRANSLATIONAL_GOLDSTONE_NUMERICAL_DIAGNOSTIC_AND_"
        "COUPLED_LINEAR_STABILITY_GATE"
    )
    print("NONLINEAR_FRAGMENTATION_PROOF=NO")

    require(UPSTREAM)
    require(SUMMARY)

    summary = json.loads(SUMMARY.read_text())
    best = summary["best"]
    qmod = load_module("d273tz_qball", UPSTREAM)

    original_match = float(qmod.X_MATCH)
    omega, epsilon, chi, legacy_solution = reconstruct(
        qmod,
        best,
        original_match,
    )
    mx_gev = float(best["m_x_gev"])

    print(f"OMEGA={omega:.15e}")
    print(f"EPSILON={epsilon:.15e}")
    print(f"CHI={chi:.15e}")
    print(f"UPSTREAM_X_MATCH={original_match:.9f}")

    # ------------------------------------------------------------------
    # Stage A: exact reconstruction of the historical D273-R l=1 issue.
    # ------------------------------------------------------------------
    legacy_results = {}
    legacy_vectors = {}

    print("\n=== STAGE A: LEGACY D273-R REPRODUCTION + OVERLAP ===")

    for n in LEGACY_N:
        bundle = build_legacy_node_dirichlet(
            qmod,
            legacy_solution,
            omega,
            epsilon,
            chi,
            n,
        )
        result = dense_legacy_spectrum(bundle, n)
        legacy_results[str(n)] = result
        legacy_vectors[f"legacy_r_n{n}"] = bundle["r"]
        legacy_vectors[f"legacy_translation_n{n}"] = bundle["translation"]
        legacy_vectors[f"legacy_mode_n{n}"] = result["translation_mode_config_vector"]

        eigv = result["translation_associated_eigenvalue"]
        tres = result["translation_residual"]
        print(
            "LEGACY "
            f"N={n} "
            f"GROWTH={result['growth']:.15e} "
            f"HIST_RELERR={result['historical_reproduction_relerr']:.6e} "
            f"GROW_OV={result['growing_mode_translation_overlap']:.9f} "
            f"TRANS_EIG=({eigv.real:.9e},{eigv.imag:.9e}) "
            f"TRANS_OV={result['translation_associated_overlap']:.9f} "
            f"TRANS_RELRES={tres['relative_frobenius_residual']:.9e} "
            f"PROJECTED_GROWTH={result['projected_dynamic_max_growth']:.9e} "
            f"PROJECTED_K0={float(result['projected_lowest_stiffness'][0]):.9e}"
        )

    # ------------------------------------------------------------------
    # Stage B: one large-domain background with the upstream physical Robin
    # background boundary. This prevents extrapolating a solution beyond its
    # BVP domain during the Rmax=150/250/400 perturbation tests.
    # ------------------------------------------------------------------
    max_mu_r = max(MU_R_VALUES)
    long_match = float(max_mu_r / epsilon)

    print("\n=== STAGE B: LARGE-DOMAIN BACKGROUND RECONSTRUCTION ===")
    print(f"LONG_BACKGROUND_X_MATCH={long_match:.9f}")

    _, _, _, long_solution = reconstruct(
        qmod,
        best,
        long_match,
    )

    bg_difference = background_core_difference(
        legacy_solution,
        long_solution,
        radius=LEGACY_RMAX,
    )

    print(
        "BACKGROUND_CORE_COMPARISON "
        f"Y_REL_L2={bg_difference['y_rel_l2']:.9e} "
        f"U_REL_L2={bg_difference['u_rel_l2']:.9e} "
        f"Y_CENTER_REL={bg_difference['y_center_rel']:.9e} "
        f"U_CENTER_REL={bg_difference['u_center_rel']:.9e}"
    )

    # ------------------------------------------------------------------
    # Stage C: independent FV/Robin domain + grid stack.
    # ------------------------------------------------------------------
    print("\n=== STAGE C: FV/ROBIN DOMAIN + GRID CONVERGENCE ===")

    scan_rows = []
    fv_results = {}
    final_vectors = {}

    for mu_r in MU_R_VALUES:
        radius = float(mu_r / epsilon)
        domain_key = f"{mu_r:g}"
        fv_results[domain_key] = {}

        for h_target in H_TARGETS:
            bundle = build_fv_robin_l1(
                qmod,
                long_solution,
                omega,
                epsilon,
                chi,
                radius,
                h_target,
            )
            count = bundle["count"]
            residual = operator_residual(bundle["K"], bundle["translation"], count)
            constrained = constrained_stiffness(
                bundle["K"],
                bundle["translation"],
                modes=4,
            )
            dynamic = near_zero_dynamic(
                bundle["A"],
                bundle["translation"],
            )

            result = {
                "epsilon_rmax": mu_r,
                "rmax": radius,
                "h_target": h_target,
                "h": bundle["h"],
                "cells": count,
                "beta_x": bundle["beta_x"],
                "beta_u": bundle["beta_u"],
                "translation_residual": residual,
                "constrained_stiffness": constrained,
                "near_zero_dynamic": dynamic,
            }
            fv_results[domain_key][f"{h_target:.6f}"] = result

            if dynamic.get("success", False):
                deig = dynamic["translation_eigenvalue"]
                dov = dynamic["translation_overlap"]
                dgrowth = dynamic["translation_growth"]
                nontrans = dynamic["low_overlap_nearzero_max_real"]
            else:
                deig = complex(math.nan, math.nan)
                dov = math.nan
                dgrowth = math.nan
                nontrans = math.nan

            print(
                "FV_ROBIN "
                f"EPS_R={mu_r:.3f} "
                f"RMAX={radius:.6f} "
                f"H={bundle['h']:.9f} "
                f"CELLS={count} "
                f"RELRES={residual['relative_frobenius_residual']:.9e} "
                f"OUTER_RES_FRAC={residual['outer_10pct_residual_fraction']:.6f} "
                f"KPROJ0={constrained['lowest']:.9e} "
                f"KPROJ_RES={constrained['lowest_residual']:.9e} "
                f"TRANS_EIG=({deig.real:.9e},{deig.imag:.9e}) "
                f"TRANS_OV={dov:.9f} "
                f"TRANS_GROWTH={dgrowth:.9e} "
                f"LOWOV_NEARZERO_MAXRE={nontrans:.9e}"
            )

            scan_rows.append(
                {
                    "epsilon_rmax": mu_r,
                    "rmax": radius,
                    "h_target": h_target,
                    "h": bundle["h"],
                    "cells": count,
                    "translation_abs_residual": residual["absolute_residual"],
                    "translation_rel_residual": residual["relative_frobenius_residual"],
                    "translation_rayleigh": residual["rayleigh"],
                    "outer_residual_fraction": residual["outer_10pct_residual_fraction"],
                    "projected_k0": constrained["lowest"],
                    "projected_k0_residual": constrained["lowest_residual"],
                    "projected_k_pass": constrained["positive_margin_pass"],
                    "dynamic_success": dynamic.get("success", False),
                    "translation_growth": dgrowth,
                    "translation_overlap": dov,
                    "translation_eig_real": deig.real,
                    "translation_eig_imag": deig.imag,
                    "low_overlap_nearzero_max_real": nontrans,
                }
            )

            if mu_r == max(MU_R_VALUES) and h_target == min(H_TARGETS):
                final_vectors["fv_final_r"] = bundle["r"]
                final_vectors["fv_final_translation"] = bundle["translation"]
                if dynamic.get("success", False):
                    final_vectors["fv_final_translation_mode"] = dynamic[
                        "translation_mode_config_vector"
                    ]

    # ------------------------------------------------------------------
    # Stage D: fail-closed decision ledger.
    # ------------------------------------------------------------------
    print("\n=== STAGE D: DECISION LEDGER ===")

    legacy_repro_pass = all(
        legacy_results[str(n)]["historical_reproduction_pass"]
        for n in LEGACY_N
    )
    legacy_overlap_pass = all(
        legacy_results[str(n)]["growing_mode_translation_overlap"] >= OVERLAP_STRONG
        for n in LEGACY_N
    )
    legacy_projected_pass = all(
        legacy_results[str(n)]["projected_dynamic_pass"]
        for n in LEGACY_N
    )

    bg_pass = bool(
        bg_difference["y_rel_l2"] <= BACKGROUND_CORE_REL_TOL
        and bg_difference["u_rel_l2"] <= BACKGROUND_CORE_REL_TOL
    )

    # Fine grid means the smaller target h = 0.375.
    fine_h = min(H_TARGETS)
    coarse_h = max(H_TARGETS)
    fine_key = f"{fine_h:.6f}"
    coarse_key = f"{coarse_h:.6f}"

    fine_results = [
        fv_results[f"{mu_r:g}"][fine_key]
        for mu_r in MU_R_VALUES
    ]
    coarse_final = fv_results[f"{max(MU_R_VALUES):g}"][coarse_key]
    fine_final = fv_results[f"{max(MU_R_VALUES):g}"][fine_key]

    projected_k_pass = all(
        row["constrained_stiffness"]["positive_margin_pass"]
        for row in fine_results
    )

    dynamic_available = all(
        row["near_zero_dynamic"].get("success", False)
        for row in fine_results
    )

    if dynamic_available:
        fine_growth = [
            row["near_zero_dynamic"]["translation_growth"]
            for row in fine_results
        ]
        fine_overlap = [
            row["near_zero_dynamic"]["translation_overlap"]
            for row in fine_results
        ]
        if fine_growth[0] <= GROWTH_TOL:
            domain_growth_pass = bool(max(fine_growth) <= GROWTH_TOL)
        else:
            domain_growth_pass = bool(
                fine_growth[-1] <= GROWTH_TOL
                and fine_growth[-1] <= 0.35 * fine_growth[0]
            )
        robin_overlap_pass = bool(min(fine_overlap) >= OVERLAP_STRONG)
    else:
        fine_growth = []
        fine_overlap = []
        domain_growth_pass = False
        robin_overlap_pass = False

    fine_residuals = [
        row["translation_residual"]["absolute_residual"]
        for row in fine_results
    ]
    domain_residual_pass = bool(
        fine_residuals[-1] <= 0.50 * max(fine_residuals[0], 1.0e-300)
    )

    final_grid_residual_pass = bool(
        fine_final["translation_residual"]["absolute_residual"]
        <= 0.90
        * coarse_final["translation_residual"]["absolute_residual"]
    )

    final_dynamic = fine_final["near_zero_dynamic"]
    if final_dynamic.get("success", False):
        final_nontrans_nearzero = final_dynamic["low_overlap_nearzero_max_real"]
        final_nontrans_dynamic_pass = bool(
            math.isnan(final_nontrans_nearzero)
            or final_nontrans_nearzero <= GROWTH_TOL
        )
    else:
        final_nontrans_nearzero = math.nan
        final_nontrans_dynamic_pass = False

    artifact_supported = bool(
        legacy_repro_pass
        and legacy_overlap_pass
        and legacy_projected_pass
        and bg_pass
        and projected_k_pass
        and domain_growth_pass
        and robin_overlap_pass
        and domain_residual_pass
        and final_grid_residual_pass
        and final_nontrans_dynamic_pass
    )

    # A direct physical falsifier is stronger than failure of an artifact
    # promotion criterion. We distinguish RED from unresolved/YELLOW.
    distinct_dynamic_instability = False
    converged_distinct_mode = []
    for row in fine_results[-2:]:
        dyn = row["near_zero_dynamic"]
        if not dyn.get("success", False):
            converged_distinct_mode = []
            break
        val = dyn["low_overlap_nearzero_max_real"]
        if not (math.isfinite(val) and val > 5.0 * GROWTH_TOL):
            converged_distinct_mode = []
            break
        converged_distinct_mode.append(float(val))
    if len(converged_distinct_mode) == 2:
        spread = abs(converged_distinct_mode[1] - converged_distinct_mode[0]) / max(
            abs(converged_distinct_mode[1]),
            abs(converged_distinct_mode[0]),
            1.0e-30,
        )
        distinct_dynamic_instability = bool(spread <= 0.35)

    negative_projected_stiffness = any(
        row["constrained_stiffness"]["lowest"] < -5.0 * PROJECTED_K_MARGIN
        and row["constrained_stiffness"]["lowest_residual"] <= LOBPCG_RESIDUAL_TOL
        for row in fine_results[-2:]
    )

    if distinct_dynamic_instability:
        classification = (
            "RED_273GJ_DISTINCT_LOW_OVERLAP_L1_DYNAMIC_MODE_FOUND_"
            "DO_NOT_PROMOTE"
        )
        next_step = (
            "DEMODE_273GJ_GLOBAL_QBALL_AND_TEST_QSHELL_OR_MULTICOMPONENT_"
            "REALIZATION"
        )
    elif negative_projected_stiffness:
        classification = (
            "RED_OR_STRONG_YELLOW_273GJ_TRANSLATION_PROJECTED_L1_"
            "NEGATIVE_STIFFNESS_FOUND_REQUIRES_DIRECT_DYNAMIC_CONFIRMATION"
        )
        next_step = (
            "CONFIRM_PROJECTED_NEGATIVE_DIRECTION_WITH_INDEPENDENT_DYNAMIC_"
            "SOLVER_BEFORE_ANY_PROMOTION"
        )
    elif artifact_supported:
        classification = (
            "GREEN_D273_L1_TRANSLATIONAL_GOLDSTONE_SPLITTING_SUPPORTED_"
            "273GJ_COUPLED_LINEAR_L0_TO_L8_GREEN_WITHIN_TESTED_MODEL"
        )
        next_step = (
            "APPLY_IDENTICAL_COUPLED_STABILITY_CERTIFICATION_STACK_TO_"
            "96P141GJ_CANDIDATE_BEFORE_031D"
        )
    else:
        classification = (
            "YELLOW_D273_L1_TRANSLATION_ARTIFACT_NOT_YET_CERTIFIED_AND_"
            "TRUE_INSTABILITY_NOT_ESTABLISHED"
        )
        next_step = (
            "INSPECT_FAILED_TZ_SUBGATE_AND_REFINE_ONLY_THE_DECISIVE_"
            "GRID_DOMAIN_OR_PROJECTED_SOLVER_DIAGNOSTIC"
        )

    decisions = {
        "legacy_reproduction_pass": legacy_repro_pass,
        "legacy_growing_mode_translation_overlap_pass": legacy_overlap_pass,
        "legacy_translation_projected_dynamic_pass": legacy_projected_pass,
        "large_domain_background_core_match_pass": bg_pass,
        "fine_domain_projected_stiffness_pass": projected_k_pass,
        "translation_growth_domain_convergence_pass": domain_growth_pass,
        "robin_translation_overlap_pass": robin_overlap_pass,
        "translation_residual_domain_convergence_pass": domain_residual_pass,
        "final_grid_residual_convergence_pass": final_grid_residual_pass,
        "final_low_overlap_nearzero_dynamic_pass": final_nontrans_dynamic_pass,
        "distinct_low_overlap_dynamic_instability": distinct_dynamic_instability,
        "negative_translation_projected_stiffness": negative_projected_stiffness,
        "translation_artifact_supported": artifact_supported,
    }

    for key, value in decisions.items():
        print(f"{key.upper()}={value}")

    print(f"031B2D273TZ_CLASSIFICATION={classification}")
    print(f"NEXT={next_step}")
    print("TRUE_PHYSICAL_INSTABILITY_ESTABLISHED=" + str(distinct_dynamic_instability))
    print("TRANSLATION_ZERO_MODE_ARTIFACT_ESTABLISHED=" + str(artifact_supported))
    print("NONLINEAR_FRAGMENTATION_CLOSED=NO")
    print("RADIATIVE_NATURALNESS_CLOSED=NO")
    print("FULL_METRIC_BACKREACTION_CLOSED=NO")

    output = {
        "provenance": {
            "git_head": git_head(),
            "upstream": str(UPSTREAM.relative_to(ROOT)),
            "upstream_sha256": sha256(UPSTREAM),
            "summary": str(SUMMARY.relative_to(ROOT)),
            "summary_sha256": sha256(SUMMARY),
        },
        "theory": {
            "omega": omega,
            "epsilon": epsilon,
            "chi": chi,
            "m_x_gev": mx_gev,
            "legacy_background_x_match": original_match,
            "long_background_x_match": long_match,
            "mu_r_values": MU_R_VALUES,
            "h_targets": H_TARGETS,
        },
        "background_core_difference": bg_difference,
        "legacy": legacy_results,
        "fv_robin": fv_results,
        "decisions": decisions,
        "classification": classification,
        "next": next_step,
        "claim_limits": [
            "Only the coupled linear l=1 translation question is newly certified here.",
            "The prior D273-R l=0 and l=2..8 dense results remain the companion evidence.",
            "Finite-amplitude fragmentation and fission remain open.",
            "The physical metric and payload are not dynamical degrees of freedom in this spectrum.",
            "Radiative naturalness, activation/off-state, and empirical closure remain open.",
            "A green translation audit is not a practical-device claim.",
        ],
    }

    OUT_JSON.write_text(json.dumps(to_builtin(output), indent=2, sort_keys=True) + "\n")

    fieldnames = sorted({key for row in scan_rows for key in row})
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scan_rows)

    np.savez_compressed(
        OUT_NPZ,
        **legacy_vectors,
        **final_vectors,
    )

    print(f"SUMMARY_JSON={OUT_JSON.resolve()}")
    print(f"SCAN_CSV={OUT_CSV.resolve()}")
    print(f"MODE_VECTORS_NPZ={OUT_NPZ.resolve()}")


if __name__ == "__main__":
    main()
