#!/usr/bin/env python3
"""023C2AQS2R3 — true-residual Newton closure + residual localization at N=73.

PURPOSE
-------
Close the remaining N=73 Euler-Lagrange residual efficiently after
023C2AQS2R2 demonstrated that adaptive matrix-free Newton-Krylov corrections
are admissible and residual-reducing, but also revealed that several inner
MINRES solves had large *true* Newton-model residuals even when MINRES returned
success.

SCIENTIFIC QUESTION
-------------------
Is the remaining N=73 stationarity blocker primarily an under-solved stiff
linear Newton equation, rather than a physical obstruction or failure of the
B=7 field branch?

ACTIVE FRONTIER / WHY THIS RUN
------------------------------
At the latest accepted N=73 state, 023C2AQS2R2 reported approximately

    GRAD_RMS = 9.79e-3,
    GRAD_MAX = 1.87e-1,

with unchanged strict thresholds

    GRAD_RMS <= 1.5e-3,
    GRAD_MAX <= 5.0e-2.

The matrix-free Hessian had already passed finite-difference step convergence
and bilinear self-adjointness.  However, the reported true linear-model
residual ratios for accepted/tried Newton directions frequently remained
O(1), and in some cases exceeded unity.  A genuine inexact Newton correction
for

    H delta = -g

should instead satisfy

    ||g + H delta|| / ||g|| <= eta_k,

with a forcing term eta_k < 1.  For a shifted/regularized solve this gate uses

    ||g + (H + mu I) delta|| / ||g|| <= eta_k.

This file therefore makes the *true Euclidean Krylov residual* a fail-closed
condition on every candidate Newton direction.  MINRES convergence status by
itself is not considered sufficient.

PHYSICAL MODEL / EQUATIONS
--------------------------
No physics is changed.  The same unrestricted static SU(2) Skyrme field is
used:

    phi = (sigma, pi1, pi2, pi3),       phi . phi = 1,

    E = integral (e2 + e4 + V) d^3x,

    V = m^2 (1-sigma)(1+eta sigma),     B=7, eta=0.4, m=8.

The projected Euler-Lagrange equation is

    g(phi) = 0.

The covariant Hessian-vector product is the already validated centered
finite-difference product-S3 construction inherited from 023C2A/023C2AQS2R.
The exact three global pion-isorotation zero modes are projected out.

OPERATIONAL OBSERVABLE
----------------------
Primary numerical observables:

    GRAD_RMS,
    GRAD_MAX,
    normalized stationarity merit

        M = max(GRAD_RMS / 1.5e-3, GRAD_MAX / 5.0e-2).

Every accepted correction must reduce M.  This prevents a step from appearing
successful by reducing the global RMS while allowing the pointwise maximum to
stall or grow in a way that moves the solve away from the actual promotion
criterion.

Only after strict stationarity passes is the already validated continuous
finite-payload force certificate run.  Positive radial force is outward in the
repository convention.

RESIDUAL LOCALIZATION / SPECTRAL DIAGNOSTIC
-------------------------------------------
Before and after the Newton slice the code reports:

- location/radius/boundary distance of the largest residual;
- fractions of residual L2 power in boundary/core/wall/tail regions;
- a tangent-component Gaussian low/high-frequency split;
- a nearest-neighbor roughness ratio.

These diagnostics are interpretation aids only.  They do not project out,
smooth, or otherwise modify any physical degree of freedom.

TRUE-RESIDUAL INEXACT NEWTON
----------------------------
For each damping candidate solve

    (H + mu I) delta ~= -g.

The L-BFGS history remains an SPD inverse-Hessian preconditioner.  Because
preconditioned MINRES stopping criteria need not imply a sufficiently small
unpreconditioned/Euclidean model residual for this particular scaling, this
file explicitly computes

    r_lin = -g - (H + mu I) delta.

If

    ||r_lin|| / ||g|| > eta_k,

iterative refinement solves the correction equation

    (H + mu I) e ~= r_lin

and updates

    delta <- delta + e.

The direction is not sent to the nonlinear line search unless the true
shifted residual is certified below eta_k.

The bounded forcing schedule is

    eta_k = clip(0.8 sqrt(GRAD_RMS), 0.03, 0.18).

It tightens naturally as the nonlinear root is approached without grossly
oversolving the linear problem far from stationarity.

NUMERICAL METHOD / EFFICIENCY STOP RULE
---------------------------------------
This is intentionally a short production gate:

- at most 4 outer Newton corrections by default;
- at most 26 MINRES iterations per refinement solve;
- at most 3 true-residual refinement rounds;
- damping ladder based on measured current-gradient curvature;
- expensive continuous-force integration only after strict stationarity.

If no true-residual-certified admissible correction is found, stop for
preconditioner/spectral redesign rather than spending hundreds of additional
R-LBFGS steps.

INPUTS
------
Preferred state:
    results/data/023c2aqs2r3_n73_true_residual_newton_checkpoint.npz

Fallback:
    results/data/023c2aqs2r2_n73_adaptive_newton_checkpoint.npz

Required upstream source:
    simulations/023c2aqs2r2_n73_adaptive_damping_inexact_newton_closure.py

OUTPUTS
-------
Checkpoint:
    results/data/023c2aqs2r3_n73_true_residual_newton_checkpoint.npz

Strict stationary artifact, if achieved:
    results/data/023c2aqs2r3_strict_stationary_b7_n73.npz

UNITS / SIGN CONVENTIONS
------------------------
Dimensionless Skyrme units inherited from the 023 branch.  Positive radial
finite-payload force means outward acceleration.

ASSUMPTIONS / APPROXIMATION LEVEL
---------------------------------
Flat-spacetime classical Skyrme matter on the same N=73 checkerboard-free
fourth-order lattice action.  Gravity remains a static linearized-GR
operational readout after stationarity.  The boundary, topological sector,
field equations, and physical thresholds are unchanged.

VALIDATION
----------
- fail-closed 023C2AQS2R2 source hash;
- external 94-test known-solution suite;
- inherited HVP step-convergence and Hessian self-adjointness audit;
- explicit true Euclidean shifted-linear residual after every MINRES/refinement
  solve;
- topology and link-smoothness guards on every nonlinear candidate;
- energy Armijo decrease;
- strict normalized stationarity-merit decrease;
- residual localization before/after the solve.

PROMOTION CONDITION
-------------------
Strict N=73 stationarity still requires exactly

    GRAD_RMS <= 1.5e-3,
    GRAD_MAX <= 5.0e-2.

If stationarity is achieved, the complete stress-energy/DEC/negative-active
region audit and continuous finite-payload sentinel are run.  A positive
sentinel is still not a full 023C stability result.

FALSIFIERS / STOP RULES
-----------------------
- HVP validation failure: numerical failure; stop.
- Loss of |B|=7 or link smoothness: reject; persistent loss blocks route.
- No true-residual-certified Newton direction in the bounded damping/refinement
  ladder: stop for preconditioner/spectral diagnosis.
- Certified inward continuous force at strict N=73: operational blocker for
  the declared payload point, subject to companion-resolution confirmation.
- Do not weaken stationarity or force thresholds.

LIMITATIONS / CLAIM BOUNDARIES
-----------------------------
This run does not establish a positive full physical Hessian, fission
stability, nonlinear Einstein-Skyrme consistency, practical energy scaling,
real-material realization, an experiment, a device, or discovery of new
physics.

RELATED FILES
-------------
simulations/023c2aqs2r2_n73_adaptive_damping_inexact_newton_closure.py
simulations/023c2aqs2r_n73_riemannian_newton_krylov_stationarity_closure.py
simulations/023c2aqs_continuous_field_active_source_force_integration.py
simulations/023c2a_n73_resolution_and_full_tangent_hessian.py

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023C2AQS2R3_TRUE_RESIDUAL_NEWTON_STATIONARITY_REPAIR
"""

from __future__ import annotations

import hashlib
import importlib.util
import math
import os
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.sparse.linalg import LinearOperator, minres


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

R2_SOURCE = SIM / "023c2aqs2r2_n73_adaptive_damping_inexact_newton_closure.py"
EXPECTED_R2_SHA256 = "3f2378f9d7f8a4b77cf2d5a40582b2a00aea4fe1725426a3021167be7d67a773"

UPSTREAM_CHECKPOINT = DATA / "023c2aqs2r2_n73_adaptive_newton_checkpoint.npz"
CHECKPOINT = DATA / "023c2aqs2r3_n73_true_residual_newton_checkpoint.npz"
FINAL = DATA / "023c2aqs2r3_strict_stationary_b7_n73.npz"

B = 7
ETA = 0.4
MASS = 8.0
N = 73
GRAD_RMS_TOL = 1.5e-3
GRAD_MAX_TOL = 5.0e-2
MAX_NEIGHBOR_ANGLE = 0.70

MAX_OUTER = max(1, int(os.environ.get("AG_NK3_MAX_OUTER", "4")))
MINRES_MAXITER = max(8, int(os.environ.get("AG_NK3_MINRES_MAXITER", "26")))
MAX_REFINEMENTS = max(1, int(os.environ.get("AG_NK3_MAX_REFINEMENTS", "3")))
HVP_POINT_ANGLE = float(os.environ.get("AG_NK3_HVP_POINT_ANGLE", "2e-4"))
MAX_LINESEARCH = max(4, int(os.environ.get("AG_NK3_MAX_LINESEARCH", "8")))
ARMIJO_C1 = float(os.environ.get("AG_NK3_ARMIJO_C1", "1e-4"))
MERIT_FACTOR = float(os.environ.get("AG_NK3_MERIT_FACTOR", "0.97"))
DAMPING_MULTIPLIERS = tuple(
    float(x)
    for x in os.environ.get("AG_NK3_DAMPING_MULTIPLIERS", "0,0.005,0.02,0.10").split(",")
)


def sha256(path: Path) -> str:
    """Return SHA-256 for a required upstream scientific source file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def require(path: Path) -> None:
    """Fail closed if a required source/artifact is absent."""
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def load_module(name: str, path: Path):
    """Import one audited repository module by explicit filesystem path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def minres_compat(A, b, M, rtol, maxiter, callback):
    """Call SciPy MINRES across old/new ``tol`` versus ``rtol`` APIs."""
    try:
        return minres(A, b, M=M, rtol=rtol, maxiter=maxiter, callback=callback, show=False, check=False)
    except TypeError:
        return minres(A, b, M=M, tol=rtol, maxiter=maxiter, callback=callback, show=False, check=False)


def load_state(r2, qs2, cr3, cr4r):
    """Load this gate's checkpoint first, otherwise the latest R2 checkpoint."""
    source = CHECKPOINT if CHECKPOINT.is_file() else UPSTREAM_CHECKPOINT
    require(source)
    with np.load(source, allow_pickle=False) as d:
        phi = np.array(d["phi"], dtype=float, copy=True)
        axis = np.array(d["axis"], dtype=float, copy=True)
        dx = float(d["dx"])
        accepted_total = int(d["accepted_total"]) if "accepted_total" in d.files else 0
        b = int(d["B"]) if "B" in d.files else B
        eta = float(d["eta"]) if "eta" in d.files else ETA
        mass = float(d["mass"]) if "mass" in d.files else MASS
        nk_total = int(d["newton_accepted_total"]) if "newton_accepted_total" in d.files else 0
        if "s_hist" in d.files and "y_hist" in d.files:
            s_hist = np.asarray(d["s_hist"], dtype=float)
            y_hist = np.asarray(d["y_hist"], dtype=float)
        else:
            s_hist = np.empty((0, N, N, N, 4), dtype=float)
            y_hist = np.empty((0, N, N, N, 4), dtype=float)
    if phi.shape != (N, N, N, 4) or axis.shape != (N,):
        raise RuntimeError(f"Unexpected N73 state shape phi={phi.shape} axis={axis.shape}")
    if b != B or abs(eta - ETA) > 1e-14 or abs(mass - MASS) > 1e-14:
        raise RuntimeError("N73 physical metadata mismatch")
    norm_err = float(np.max(np.abs(np.linalg.norm(phi, axis=-1) - 1.0)))
    if norm_err > 5e-10:
        raise RuntimeError(f"N73 S3 norm violation {norm_err}")
    history, discarded = qs2.history_from_arrays(cr3, s_hist, y_hist, dx)
    state = cr4r.State(phi=phi, axis=axis, dx=dx, accepted_total=accepted_total)
    return state, history, source, discarded, norm_err, nk_total


def save_checkpoint(state, history, E, rms, gmax, nk_total):
    """Persist field plus transported L-BFGS curvature history."""
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    if history:
        s_hist = np.stack([item[0] for item in history], axis=0)
        y_hist = np.stack([item[1] for item in history], axis=0)
    else:
        s_hist = np.empty((0, N, N, N, 4), dtype=float)
        y_hist = np.empty((0, N, N, N, 4), dtype=float)
    np.savez(
        CHECKPOINT,
        phi=state.phi,
        axis=state.axis,
        dx=np.array(state.dx),
        B=np.array(B),
        eta=np.array(ETA),
        mass=np.array(MASS),
        accepted_total=np.array(state.accepted_total),
        newton_accepted_total=np.array(nk_total),
        energy=np.array(E),
        grad_rms=np.array(rms),
        grad_max=np.array(gmax),
        source=np.array("023C2AQS2R3_TRUE_RESIDUAL_NEWTON"),
        s_hist=s_hist,
        y_hist=y_hist,
    )
    print(
        f"NK3_CHECKPOINT_WRITTEN={CHECKPOINT.relative_to(ROOT)} "
        f"NEWTON_ACCEPTED_TOTAL={nk_total} HISTORY_LENGTH={len(history)}",
        flush=True,
    )


def save_final(state, E, rms, gmax, diag, nk_total):
    """Write strict N=73 field only after unchanged stationarity gates pass."""
    FINAL.parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        FINAL,
        phi=state.phi,
        axis=state.axis,
        dx=np.array(state.dx),
        B=np.array(B),
        eta=np.array(ETA),
        mass=np.array(MASS),
        accepted_total=np.array(state.accepted_total),
        newton_accepted_total=np.array(nk_total),
        energy=np.array(E),
        grad_rms=np.array(rms),
        grad_max=np.array(gmax),
        topology4=np.array(diag.topology4),
        active_total=np.array(diag.active_total),
        min_active_fraction=np.array(diag.min_active_fraction),
        min_dec_scaled_margin=np.array(diag.min_dec_scaled_margin),
        max_active_trace_scaled=np.array(diag.max_active_trace_scaled),
        source=np.array("023C2AQS2R3_N73_STRICT_STATIONARY"),
    )
    print(f"NK3_STRICT_STATIONARY_FIELD_ARTIFACT={FINAL.relative_to(ROOT)}", flush=True)


def stationarity_merit(rms: float, gmax: float) -> float:
    """Return max normalized distance from the two strict stationarity gates."""
    return max(rms / GRAD_RMS_TOL, gmax / GRAD_MAX_TOL)


def forcing_eta(rms: float) -> float:
    """Bounded Eisenstat-Walker-style forcing target for true linear residual."""
    return min(0.18, max(0.03, 0.8 * math.sqrt(max(rms, 1e-16))))


def residual_frequency_diagnostic(c2a, cr3, state, g, label: str):
    """Report whether residual power is smooth/extended or lattice-scale/stiff.

    This function is diagnostic only.  The Gaussian split never enters the
    optimization update and therefore cannot remove or hide a physical mode.
    """
    phi = state.phi
    basis = c2a.tangent_basis_householder(phi)
    comp = c2a.field_to_components(g, basis).reshape(N - 2, N - 2, N - 2, 3)
    low = np.empty_like(comp)
    for a in range(3):
        low[..., a] = gaussian_filter(comp[..., a], sigma=1.0, mode="nearest")
    high = comp - low
    total = float(np.sum(comp * comp))
    low2 = float(np.sum(low * low))
    high2 = float(np.sum(high * high))
    # A normalized nearest-neighbor roughness indicator.  Large values mean
    # that the remaining residual varies strongly at the lattice scale.
    rough_num = 0.0
    for axis in range(3):
        d = np.diff(comp, axis=axis)
        rough_num += float(np.sum(d * d))
    rough = rough_num / max(total, 1e-300)
    print(f"{label}_RESIDUAL_GAUSSIAN_LOW_L2_FRACTION={low2/max(total,1e-300):.15e}", flush=True)
    print(f"{label}_RESIDUAL_GAUSSIAN_HIGH_L2_FRACTION={high2/max(total,1e-300):.15e}", flush=True)
    print(f"{label}_RESIDUAL_NEIGHBOR_ROUGHNESS_RATIO={rough:.15e}", flush=True)


def certified_linear_solve(A, rhs, M, eta_target: float, label: str, stats: dict):
    """Solve a symmetric Newton system with explicit true-residual refinement.

    MINRES status is advisory.  A direction is certified only if the actual
    Euclidean residual of the shifted Newton equation satisfies

        ||rhs - A delta|| / ||rhs|| <= eta_target.

    Returns
    -------
    tuple
        (delta, certified, true_rel, total_iterations)
    """
    delta = np.zeros_like(rhs)
    rhs_norm = float(np.linalg.norm(rhs))
    residual = rhs.copy()
    prev_rel = 1.0
    total_iters = 0

    for ref in range(MAX_REFINEMENTS):
        rel_before = float(np.linalg.norm(residual) / max(rhs_norm, 1e-300))
        if rel_before <= eta_target:
            return delta, True, rel_before, total_iters

        # The internal tolerance is deliberately tighter than the required
        # *true* forcing target because preconditioning changes MINRES's native
        # stopping norm.  The external residual below remains the authority.
        inner_rtol = max(2.0e-5, min(5.0e-3, 0.12 * eta_target * (0.25 ** ref)))
        it = {"n": 0}

        def cb(_xk):
            it["n"] += 1

        corr, info = minres_compat(A, residual, M, inner_rtol, MINRES_MAXITER, cb)
        total_iters += it["n"]
        stats["minres_iterations"] += it["n"]
        if info < 0 or not np.all(np.isfinite(corr)):
            print(f"{label}_REFINE={ref} MINRES_BREAKDOWN=YES INFO={info}", flush=True)
            return delta, False, rel_before, total_iters

        delta = delta + np.asarray(corr, dtype=float)
        residual = rhs - A.matvec(delta)
        true_rel = float(np.linalg.norm(residual) / max(rhs_norm, 1e-300))
        reduction = prev_rel / max(true_rel, 1e-300)
        print(
            f"{label}_REFINE={ref} MINRES_INFO={info} MINRES_ITERS={it['n']} "
            f"INNER_RTOL={inner_rtol:.9e} TRUE_SHIFTED_RELRES={true_rel:.15e} "
            f"TRUE_RELRES_REDUCTION={reduction:.15e} ETA_TARGET={eta_target:.15e}",
            flush=True,
        )
        if true_rel <= eta_target:
            return delta, True, true_rel, total_iters
        # If refinement fails to make even modest progress twice, spend no more
        # HVPs on this damping value; the next damping candidate is more useful.
        if ref >= 1 and true_rel >= 0.97 * prev_rel:
            print(f"{label}_TRUE_RESIDUAL_STAGNATION=YES", flush=True)
            return delta, False, true_rel, total_iters
        prev_rel = true_rel

    true_rel = float(np.linalg.norm(residual) / max(rhs_norm, 1e-300))
    return delta, bool(true_rel <= eta_target), true_rel, total_iters


def newton_slice(r2, r, qs2, c2a, cr2, cr3, cr4r, state, history, nk_total):
    """Run a bounded true-residual-certified Riemannian Newton slice."""
    E, _e2, _e4, _e0, g, rms, gmax, station = r.strict_stationarity(cr3, state.phi, state.dx)
    stats = {
        "outer_attempted": 0,
        "outer_accepted": 0,
        "hvp_calls": 0,
        "minres_iterations": 0,
        "linear_cert_failures": 0,
        "line_rejects": 0,
    }

    for outer in range(1, MAX_OUTER + 1):
        if station:
            break
        stats["outer_attempted"] += 1
        phi = state.phi
        dx = state.dx
        basis = c2a.tangent_basis_householder(phi)
        Z = c2a.orthonormal_columns(c2a.isorotation_modes(phi, basis))
        ndof = basis.shape[0] * 3
        gvec = c2a.project_subspace(c2a.field_to_components(g, basis), Z)
        gnorm = float(np.linalg.norm(gvec))
        merit0 = stationarity_merit(rms, gmax)
        eta_target = forcing_eta(rms)
        print(
            f"NK3_OUTER={outer} NDOF={ndof} GRAD_RMS={rms:.15e} GRAD_MAX={gmax:.15e} "
            f"STATIONARITY_MERIT={merit0:.15e} TRUE_FORCING_ETA={eta_target:.15e}",
            flush=True,
        )

        if outer == 1:
            if not r.audit_hessian_operator(c2a, cr3, phi, state.axis, dx, basis, Z):
                raise RuntimeError("N73 true-residual Newton HVP validation failed")

        hvp, calls = c2a.make_hvp(cr3, phi, dx, basis, Z, HVP_POINT_ANGLE)
        pairs = r.component_history(c2a, history, basis, Z)
        secant_scale = r.curvature_scale_from_pairs(pairs)
        print(f"NK3_PRECONDITIONER_USABLE_PAIRS={len(pairs)}", flush=True)
        print(f"NK3_SECANT_CURVATURE_SCALE={secant_scale:.15e}", flush=True)

        Hg = hvp(gvec)
        grad_rq = float(np.dot(gvec, Hg) / max(np.dot(gvec, gvec), 1e-300))
        smooth = c2a.smooth_random_vector(cr3, phi, basis, Z, 2026090101 + outer)
        Hs = hvp(smooth)
        smooth_rq = float(np.dot(smooth, Hs) / max(np.dot(smooth, smooth), 1e-300))
        local_scale = max(abs(grad_rq), 0.1 * abs(smooth_rq), 1.0)
        stiffness_ratio = abs(grad_rq) / max(abs(smooth_rq), 1e-300)
        print(f"NK3_GRADIENT_RAYLEIGH={grad_rq:.15e}", flush=True)
        print(f"NK3_SMOOTH_RAYLEIGH={smooth_rq:.15e}", flush=True)
        print(f"NK3_GRADIENT_TO_SMOOTH_CURVATURE_RATIO={stiffness_ratio:.15e}", flush=True)
        print(f"NK3_LOCAL_DAMPING_SCALE={local_scale:.15e}", flush=True)

        def mvec(x):
            return r.lbfgs_inverse_vector(x, pairs, Z, c2a)

        M = LinearOperator((ndof, ndof), matvec=mvec, dtype=float) if pairs else None
        rhs = -gvec
        accepted_pack = None

        for mult in DAMPING_MULTIPLIERS:
            mu = max(0.0, mult * local_scale)

            def avec(x):
                q = c2a.project_subspace(np.asarray(x, dtype=float), Z)
                return hvp(q) + mu * q

            A = LinearOperator((ndof, ndof), matvec=avec, dtype=float)
            label = f"NK3_LINEAR_OUTER_{outer}_DAMP_{mult:.6e}"
            delta, certified, true_rel, _iters = certified_linear_solve(
                A, rhs, M, eta_target, label, stats
            )
            delta = c2a.project_subspace(np.asarray(delta, dtype=float), Z)
            print(
                f"NK3_LINEAR_CERTIFICATE_OUTER={outer} DAMP_MULT={mult:.6e} MU={mu:.15e} "
                f"TRUE_SHIFTED_RELRES={true_rel:.15e} ETA_TARGET={eta_target:.15e} "
                f"CERTIFIED={'YES' if certified else 'NO'}",
                flush=True,
            )
            if not certified:
                stats["linear_cert_failures"] += 1
                continue

            direction = c2a.components_to_field(delta, basis, phi.shape)
            direction = cr3.project_tangent(phi, direction)
            gd = cr3.tangent_inner(g, direction, dx)
            if (not math.isfinite(gd)) or gd >= -1e-12 * max(cr3.tangent_inner(g, g, dx), 1e-300):
                print("NK3_LINEAR_DIRECTION_DESCENT=NO_TRY_MORE_DAMPING", flush=True)
                continue
            print("NK3_LINEAR_DIRECTION_DESCENT=YES", flush=True)

            max_point = float(np.max(np.linalg.norm(direction[1:-1, 1:-1, 1:-1], axis=-1)))
            trust_angle = min(2.0e-2, max(1.0e-3, 0.35 * rms))
            alpha = min(1.0, trust_angle / max(max_point, 1e-300))
            print(
                f"NK3_DIRECTION_OUTER={outer} DAMP_MULT={mult:.6e} MAX_POINT={max_point:.15e} "
                f"TRUST_ANGLE={trust_angle:.15e} ALPHA0={alpha:.15e}",
                flush=True,
            )

            for ls in range(MAX_LINESEARCH):
                cand = cr3.exp_map_update(phi, direction, alpha)
                Etrial = cr3.high_order_energy_gradient(cand, dx, False)[0]
                if (not math.isfinite(Etrial)) or Etrial > E + ARMIJO_C1 * alpha * gd:
                    stats["line_rejects"] += 1
                    alpha *= 0.5
                    continue
                ok, reason, _ = qs2.candidate_admissible(cr3, cr2, cand, dx, state.accepted_total + 1)
                if not ok:
                    stats["line_rejects"] += 1
                    print(f"NK3_LINESEARCH_REJECT_REASON={reason}", flush=True)
                    alpha *= 0.5
                    continue
                pack = r.strict_stationarity(cr3, cand, dx)
                Enew, _e2n, _e4n, _e0n, gnew, rmsnew, gmaxnew, stationnew = pack
                merit_new = stationarity_merit(rmsnew, gmaxnew)
                merit_ok = bool(stationnew or merit_new <= MERIT_FACTOR * merit0)
                print(
                    f"NK3_LINESEARCH_TRIAL_OUTER={outer} DAMP_MULT={mult:.6e} LS={ls} "
                    f"ALPHA={alpha:.15e} ENERGY={Enew:.15e} GRAD_RMS={rmsnew:.15e} "
                    f"GRAD_MAX={gmaxnew:.15e} STATIONARITY_MERIT={merit_new:.15e} "
                    f"MERIT_ACCEPT={'YES' if merit_ok else 'NO'}",
                    flush=True,
                )
                if not merit_ok:
                    stats["line_rejects"] += 1
                    alpha *= 0.5
                    continue
                accepted_pack = (
                    cand, Enew, gnew, rmsnew, gmaxnew, stationnew,
                    direction, alpha, mult, mu, true_rel, merit_new,
                )
                break
            if accepted_pack is not None:
                break

        stats["hvp_calls"] += calls["count"]
        if accepted_pack is None:
            print("NK3_NEWTON_STEP_ACCEPTED=NO", flush=True)
            break

        (
            cand, Enew, gnew, rmsnew, gmaxnew, stationnew,
            direction, alpha, mult_used, mu_used, true_rel_used, merit_new,
        ) = accepted_pack
        old_phi = phi
        old_g = g
        old_merit = merit0
        r.transport_history_after_step(
            cr3, cr4r, old_phi, cand, direction, alpha, old_g, gnew, history
        )
        state.phi = cand
        state.accepted_total += 1
        nk_total += 1
        stats["outer_accepted"] += 1
        E, g, rms, gmax, station = Enew, gnew, rmsnew, gmaxnew, stationnew
        t4 = cr3.topology4(state.phi, state.dx)
        deg_ok, degrees = cr3.geometric_guard(state.phi, cr2, True)
        angle = cr3.max_neighbor_angle(state.phi)
        print(
            f"NK3_NEWTON_STEP_ACCEPTED=YES OUTER={outer} DAMP_MULT={mult_used:.6e} "
            f"MU={mu_used:.15e} ALPHA={alpha:.15e} TRUE_SHIFTED_RELRES={true_rel_used:.15e} "
            f"MERIT_REDUCTION_FACTOR={old_merit/max(merit_new,1e-300):.15e} "
            f"ENERGY={E:.15e} GRAD_RMS={rms:.15e} GRAD_MAX={gmax:.15e} "
            f"STATIONARITY_MERIT={merit_new:.15e} TOPOLOGY4={t4:.15e} "
            f"GEOMETRIC_DEGREES={','.join(str(x) for x in degrees)} "
            f"MAX_NEIGHBOR_ANGLE={angle:.15e}",
            flush=True,
        )
        if not deg_ok:
            raise RuntimeError("Accepted true-residual Newton step lost geometric B=7")
        save_checkpoint(state, history, E, rms, gmax, nk_total)

    return state, history, E, g, rms, gmax, station, nk_total, stats


def main():
    print("=== 023C2AQS2R3 — TRUE-RESIDUAL N73 NEWTON + LOCALIZATION ===", flush=True)

    print("\n=== A — FAIL-CLOSED UPSTREAM AUDIT ===", flush=True)
    require(R2_SOURCE)
    actual = sha256(R2_SOURCE)
    print(f"023C2AQS2R2_SOURCE_SHA256={actual}", flush=True)
    if actual != EXPECTED_R2_SHA256:
        raise RuntimeError("023C2AQS2R2 source hash mismatch")
    print("UPSTREAM_023C2AQS2R2_AUDIT=PASS", flush=True)

    r2 = load_module("c2aqs2r3_r2", R2_SOURCE)
    r = load_module("c2aqs2r3_r", r2.R_SOURCE)
    qs2 = load_module("c2aqs2r3_qs2", r.QS2_SOURCE)
    c2a = load_module("c2aqs2r3_c2a", r.C2A_SOURCE)
    c2ar = qs2.load_module("c2aqs2r3_c2ar", qs2.C2AR_SOURCE)
    c2aqs = qs2.load_module("c2aqs2r3_c2aqs", qs2.C2AQS_SOURCE)
    cr2 = c2ar.load_module("c2aqs2r3_cr2", c2ar.CR2_SOURCE)
    cr3 = c2ar.load_module("c2aqs2r3_cr3", c2ar.CR3_SOURCE)
    cr4r = c2ar.load_module("c2aqs2r3_cr4r", c2ar.CR4R_SOURCE)

    print("\n=== B — LOAD LATEST N73 STATE ===", flush=True)
    state, history, source, discarded, norm_err, nk_total = load_state(r2, qs2, cr3, cr4r)
    E0, _a, _b, _c, g0, rms0, gmax0, station0 = r.strict_stationarity(cr3, state.phi, state.dx)
    deg_ok0, deg0 = cr3.geometric_guard(state.phi, cr2, True)
    print(f"NK3_START_SOURCE={source.relative_to(ROOT)}", flush=True)
    print(f"NK3_START_ACCEPTED_TOTAL={state.accepted_total}", flush=True)
    print(f"NK3_START_NEWTON_ACCEPTED_TOTAL={nk_total}", flush=True)
    print(f"NK3_START_HISTORY_LENGTH={len(history)}", flush=True)
    print(f"NK3_START_HISTORY_DISCARDED={discarded}", flush=True)
    print(f"NK3_START_NORM_MAXERR={norm_err:.15e}", flush=True)
    print(f"NK3_START_ENERGY={E0:.15e}", flush=True)
    print(f"NK3_START_GRAD_RMS={rms0:.15e}", flush=True)
    print(f"NK3_START_GRAD_MAX={gmax0:.15e}", flush=True)
    print(f"NK3_START_STATIONARITY_MERIT={stationarity_merit(rms0,gmax0):.15e}", flush=True)
    print("NK3_START_STRICT_STATIONARITY=" + ("PASS" if station0 else "FAIL"), flush=True)
    print(f"NK3_START_TOPOLOGY4={cr3.topology4(state.phi,state.dx):.15e}", flush=True)
    print("NK3_START_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in deg0), flush=True)
    if not deg_ok0:
        raise RuntimeError("Starting N73 field failed geometric B=7")

    print("\n=== C — START RESIDUAL LOCALIZATION ===", flush=True)
    cr4r.residual_localization(cr3, state, g0)
    residual_frequency_diagnostic(c2a, cr3, state, g0, "NK3_START")

    if station0:
        E, g, rms, gmax, station = E0, g0, rms0, gmax0, station0
        stats = {
            "outer_attempted": 0, "outer_accepted": 0, "hvp_calls": 0,
            "minres_iterations": 0, "linear_cert_failures": 0, "line_rejects": 0,
        }
    else:
        print("\n=== D — TRUE-RESIDUAL-CERTIFIED NEWTON SLICE ===", flush=True)
        state, history, E, g, rms, gmax, station, nk_total, stats = newton_slice(
            r2, r, qs2, c2a, cr2, cr3, cr4r, state, history, nk_total
        )

    print("\n=== E — END-OF-SLICE AUDIT ===", flush=True)
    t4 = cr3.topology4(state.phi, state.dx)
    deg_ok, degrees = cr3.geometric_guard(state.phi, cr2, True)
    angle = cr3.max_neighbor_angle(state.phi)
    print(f"NK3_OUTER_ATTEMPTED={stats['outer_attempted']}", flush=True)
    print(f"NK3_OUTER_ACCEPTED={stats['outer_accepted']}", flush=True)
    print(f"NK3_HVP_MATVEC_CALLS={stats['hvp_calls']}", flush=True)
    print(f"NK3_MINRES_TOTAL_ITERATIONS={stats['minres_iterations']}", flush=True)
    print(f"NK3_LINEAR_CERT_FAILURES={stats['linear_cert_failures']}", flush=True)
    print(f"NK3_LINESEARCH_REJECTS={stats['line_rejects']}", flush=True)
    print(f"NK3_FINAL_ENERGY={E:.15e}", flush=True)
    print(f"NK3_FINAL_GRAD_RMS={rms:.15e}", flush=True)
    print(f"NK3_FINAL_GRAD_MAX={gmax:.15e}", flush=True)
    print(f"NK3_FINAL_STATIONARITY_MERIT={stationarity_merit(rms,gmax):.15e}", flush=True)
    print("NK3_FINAL_STRICT_STATIONARITY=" + ("PASS" if station else "FAIL"), flush=True)
    print(f"NK3_FINAL_TOPOLOGY4={t4:.15e}", flush=True)
    print("NK3_FINAL_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in degrees), flush=True)
    print(f"NK3_FINAL_MAX_NEIGHBOR_ANGLE={angle:.15e}", flush=True)

    print("\n=== F — FINAL RESIDUAL LOCALIZATION ===", flush=True)
    cr4r.residual_localization(cr3, state, g)
    residual_frequency_diagnostic(c2a, cr3, state, g, "NK3_FINAL")

    if not station:
        save_checkpoint(state, history, E, rms, gmax, nk_total)
        print("\n=== G — BOUNDED INCOMPLETE DECISION ===", flush=True)
        print("023C2AQS2R3_TRUE_RESIDUAL_NEWTON=INCOMPLETE_SHORT_TRUE_RESIDUAL_SLICE", flush=True)
        print("N73_ACTUAL_FINE_STRICT_STATIONARITY=NOT_YET", flush=True)
        if stats["outer_accepted"] > 0:
            print("TRUE_RESIDUAL_NEWTON_LOCAL_ACCELERATION=SUPPORTED", flush=True)
            print("NEXT=RERUN_SAME_023C2AQS2R3_FROM_TRUE_RESIDUAL_CHECKPOINT", flush=True)
        else:
            print("TRUE_RESIDUAL_NEWTON_LOCAL_ACCELERATION=NOT_ESTABLISHED", flush=True)
            print("NEXT=USE_REPORTED_RESIDUAL_LOCALIZATION_FOR_TARGETED_PRECONDITIONER_OR_MULTIGRID_GATE", flush=True)
        print("N73_CONTINUOUS_FORCE=NOT_RUN_BEFORE_STATIONARITY", flush=True)
        print("FULL_PHYSICAL_HESSIAN=DEFERRED_OPERATIONAL_FORCE_AND_FINE_FIELD_UNRESOLVED", flush=True)
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR_NOT_A_PROBABILITY", flush=True)
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED", flush=True)
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
        return

    print("\n=== G — STRICT N73 PHYSICAL FIELD AUDIT ===", flush=True)
    diag = cr3.continuum_local_diagnostics(state.phi, state.axis, state.dx, cr2)
    print(f"NK3_N73_STATIONARY_CONTINUUM_ENERGY={diag.energy_continuum:.15e}", flush=True)
    print(f"NK3_N73_STATIONARY_ACTIVE_TOTAL={diag.active_total:.15e}", flush=True)
    print(f"NK3_N73_STATIONARY_MIN_ACTIVE_FRACTION={diag.min_active_fraction:.15e}", flush=True)
    print(f"NK3_N73_STATIONARY_MIN_DEC_SCALED_MARGIN={diag.min_dec_scaled_margin:.15e}", flush=True)
    print(f"NK3_N73_STATIONARY_MAX_ACTIVE_TRACE_SCALED={diag.max_active_trace_scaled:.15e}", flush=True)
    physical_gate = bool(
        deg_ok
        and diag.active_total > 0.0
        and diag.min_active_fraction <= -1.0e-2
        and diag.min_dec_scaled_margin >= -1.0e-9
        and diag.max_active_trace_scaled <= 1.0e-10
        and angle <= MAX_NEIGHBOR_ANGLE
    )
    print("NK3_N73_STATIONARY_PHYSICAL_FIELD_GATE=" + ("PASS" if physical_gate else "FAIL"), flush=True)
    save_final(state, E, rms, gmax, diag, nk_total)

    if not physical_gate:
        print("023C2AQS2R3_TRUE_RESIDUAL_NEWTON=RED_STRICT_N73_PHYSICAL_FIELD_GATE", flush=True)
        print("FULL_PHYSICAL_HESSIAN=DEFERRED_BY_FINE_FIELD_PHYSICAL_FALSIFIER", flush=True)
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_PENDING_RERANK", flush=True)
        print("NEXT=PRESERVE_NEGATIVE_RESULT_AND_RERANK_023_BRANCH", flush=True)
        return

    print("\n=== H — CONDITIONAL CONTINUOUS-FORCE CERTIFICATE ===", flush=True)
    n65ref = qs2.load_n65_force_reference()
    aqr = c2aqs.load_module("c2aqs2r3_aqr", c2aqs.AQR_SOURCE)
    aqr.validate_analytic_formulae()
    print("NK3_N73_ANALYTIC_KERNEL_VALIDATION=PASS", flush=True)
    force = qs2.continuous_force_gate(c2aqs, aqr, cr3, state.phi, state.axis, state.dx, n65ref)

    print("\n=== I — 023C2AQS2R3 DECISION ===", flush=True)
    if force["certified"] and force["sign"] == "OUTWARD":
        decision = "GREEN_STRICT_N73_CONTINUOUS_OUTWARD_SENTINEL"
        next_step = "023C2AQS3_N81_STATIONARY_COMPANION_AND_CONTINUOUS_FORCE_RESOLUTION_THEN_320_DIRECTION_GATE"
        hessian = "DEFERRED_UNTIL_N73_N81_OPERATIONAL_FORCE_CONVERGENCE"
    elif force["certified"] and force["sign"] == "INWARD":
        decision = "RED_STRICT_N73_CONTINUOUS_SENTINEL_INWARD"
        next_step = "023C2AQS3_N81_CONFIRMATION_OR_BOUNDED_PAYLOAD_OPERATING_VOLUME_RERANK"
        hessian = "DEFERRED_BY_FINE_FIELD_OPERATIONAL_FORCE_FALSIFIER"
    else:
        decision = "INCOMPLETE_STRICT_N73_CONTINUOUS_FORCE_SIGN_NOT_CERTIFIED"
        next_step = "023C2AQS3_N81_ACTUAL_FIELD_RESOLUTION_FROM_STRICT_N73"
        hessian = "DEFERRED_OPERATIONAL_FORCE_CONTINUUM_NOT_RESOLVED"

    print(f"023C2AQS2R3_TRUE_RESIDUAL_NEWTON={decision}", flush=True)
    print("N73_ACTUAL_FINE_STRICT_STATIONARITY=PASS", flush=True)
    print(f"FULL_PHYSICAL_HESSIAN={hessian}", flush=True)
    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR_NOT_A_PROBABILITY", flush=True)
    print(f"NEXT={next_step}", flush=True)
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED_UNTIL_023C_COMPLETE", flush=True)
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
    print("NEW_PHYSICS_DISCOVERY=NO", flush=True)
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023C2AQS2R3_TRUE_RESIDUAL_NEWTON_STATIONARITY_REPAIR", flush=True)


if __name__ == "__main__":
    main()
