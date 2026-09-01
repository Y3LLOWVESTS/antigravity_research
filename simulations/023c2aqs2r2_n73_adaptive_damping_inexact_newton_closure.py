#!/usr/bin/env python3
"""023C2AQS2R2 — adaptive-damping N=73 inexact Newton-Krylov closure.

PURPOSE
-------
Accelerate the remaining N=73 Euler-Lagrange stationarity solve after
023C2AQS2R established that matrix-free Riemannian Newton-Krylov corrections
are numerically valid and residual-reducing, but also exposed an overly
conservative damping scale.

SCIENTIFIC QUESTION
-------------------
Can the same unrestricted B=7 N=73 field be driven to the unchanged strict
stationarity thresholds efficiently by using the *measured local Hessian
curvature* to choose Levenberg-style regularization, rather than scaling the
regularization from the much larger L-BFGS secant-curvature estimate?

WHY THIS REPAIR IS NEEDED
-------------------------
023C2AQS2R found, at the actual N=73 field,

    HVP step convergence                     PASS
    Hessian bilinear self-adjointness         PASS
    random smooth Rayleigh curvature          ~ 2.9e2
    L-BFGS secant curvature scale              ~ 6.2e5
    first regularization mu                    ~ 1.24e4

and accepted all three attempted Newton corrections.  However, the accepted
pointwise rotations were only O(1e-5), far below the O(1e-3--1e-2) trust
radius.  Thus the previous regularization was dominated by a stiffness scale
that is useful for preconditioning but is not an appropriate universal shift
for the Newton equation.

This file separates those two roles:

1. the positive-curvature 20-pair L-BFGS history remains an SPD inverse-Hessian
   PRECONDITIONER;
2. the Newton regularization scale is inferred independently from current
   matrix-free Hessian-vector products;
3. the unshifted Newton equation is tried first;
4. progressively stronger local-curvature shifts are used only if required by
   descent, topology/smoothness, energy, or nonlinear-residual acceptance.

MODEL / EQUATIONS
-----------------
The physical model, field, boundary conditions, topology sector, action,
stationarity criteria, and operational-force definition are unchanged:

    phi = (sigma, pi1, pi2, pi3),      phi . phi = 1

    E = integral (e2 + e4 + V) d^3x

    V = m^2 (1-sigma)(1+eta sigma),    B=7, eta=0.4, m=8.

The projected stationarity equation is

    g(phi) = 0,

and one inexact Newton correction solves

    (H + mu I) delta ~= -g,

where H is the covariant Riemannian Hessian on the complete three-component
interior tangent space after exact projection of the three global
pion-isorotation zero modes.

The Hessian-vector product is unchanged from 023C2AQS2R and is computed from
centered finite differences of the exact Riemannian gradient along sitewise
S^3 geodesics, with exact parallel transport back to the base tangent space.


OPERATIONAL OBSERVABLE
----------------------
The primary observable of this repair is the norm of the exact discrete
Euler-Lagrange residual on the N=73 field:

    GRAD_RMS
    GRAD_MAX.

Only after both unchanged stationarity thresholds pass is the project's
continuous finite-payload radial force sentinel evaluated.  Positive radial
force is outward in the repository convention.

UNITS / SIGN CONVENTIONS
------------------------
The Skyrme field, coordinates, action, gradients, and Hessian quantities use
the dimensionless normalization inherited from the 023 branch.  Positive
finite-payload radial force means outward acceleration; negative means inward.
The Newton correction delta is tangent to S^3 at every lattice site.

ASSUMPTIONS / APPROXIMATION LEVEL
---------------------------------
This is a flat-spacetime classical Skyrme-matter NUMERICAL_APPROXIMATION.
Gravity is not solved dynamically here; if stationarity is reached, the
existing static LINEARIZED_GENERAL_RELATIVITY operational readout is evaluated.
The outer vacuum boundary, B=7 topological sector, and checkerboard-free
fourth-order discrete action are unchanged.

CONSERVATION / ENERGY CONDITIONS / STABILITY
---------------------------------------------
No new stress-energy or constitutive sector is introduced by this solver
repair.  Complete stress-energy, DEC, positive total active mass, negative
active region, and active-trace diagnostics are reconstructed only after strict
stationarity using the already-audited upstream implementation.  Stationarity
is not stability: a positive full physical Hessian and explicit fission tests
remain mandatory later 023C gates.

ADAPTIVE DAMPING
----------------
At every outer Newton iteration evaluate

    lambda_g = <g,Hg>/<g,g>

and one deterministic smooth-vector Rayleigh quotient lambda_s.  Define a
local curvature scale

    lambda_loc = max(|lambda_g|, 0.1 |lambda_s|, 1).

The predeclared damping ladder is

    mu/lambda_loc = 0, 0.02, 0.10, 0.50, 2.0.

Thus an unshifted Newton solve is always attempted first.  The older L-BFGS
secant curvature scale is printed only as a diagnostic and is NOT used to set
mu.  This is a numerical solver repair, not a change to the field equations.

INEXACT NEWTON / TRUST LOGIC
----------------------------
MINRES is used because the projected Hessian is symmetric and may be singular
or indefinite before the later stability gate.  The inner tolerance tightens
as the nonlinear residual falls.  This follows the standard inexact-Newton
principle that the linear system need not be oversolved far from the root.

Every candidate must satisfy all of:

- a descent direction for the discrete energy;
- Armijo energy decrease;
- unchanged B=7 geometric-topology guard;
- unchanged derivative-topology and link-smoothness guards;
- explicit nonlinear RMS-gradient reduction;
- controlled maximum-residual behavior.

No stationarity, topology, force, or physics threshold is weakened.

INPUTS
------
Preferred resume state:
    results/data/023c2aqs2r2_n73_adaptive_newton_checkpoint.npz

Otherwise:
    results/data/023c2aqs2r_n73_newton_krylov_checkpoint.npz

OUTPUTS
-------
Checkpoint:
    results/data/023c2aqs2r2_n73_adaptive_newton_checkpoint.npz

Strict stationary artifact, if reached:
    results/data/023c2aqs2r2_strict_stationary_b7_n73.npz

If strict stationarity is reached, the already validated cubic/quintic
continuous-field finite-payload force certificate is run exactly once.

PROMOTION CONDITION
-------------------
Strict stationarity thresholds remain exactly

    GRAD_RMS <= 1.5e-3
    GRAD_MAX <= 5.0e-2.

This file may establish only an N=73 strict stationary field and the declared
continuous-force sentinel.  It does NOT establish unrestricted stability or
complete 023C.

FALSIFIERS / STOP RULES
-----------------------
- HVP step convergence or self-adjointness failure: numerical failure; stop.
- Loss of B=7 or smoothness: reject the step; persistent loss blocks this
  numerical route.
- No admissible residual-reducing Newton correction in a bounded slice: stop
  for mode/preconditioner diagnosis; do not return to hundreds of blind
  R-LBFGS steps.
- Certified inward continuous force at strict stationarity is an operational
  falsifier for the declared payload point, subject to companion-resolution
  confirmation.
- The full physical Hessian remains unauthorized until companion-resolution
  continuous-force convergence is established.

VALIDATION
----------
- fail-closed source hash for 023C2AQS2R;
- 94 known-solution regression suite is run externally by the shell block;
- HVP finite-difference step convergence at the actual field;
- Hessian bilinear self-adjointness;
- exact zero-mode projection;
- current-gradient and smooth-vector Rayleigh diagnostics;
- explicit linear-model residual diagnostics;
- exact topology/smoothness guards after accepted corrections;
- checkpoint after every accepted Newton correction.

CLAIM BOUNDARIES
----------------
No new physics discovery is claimed.  This is a numerical stationarity repair.
It does not establish a positive full Hessian, binary-fission stability,
nonlinear Einstein-Skyrme consistency, practical scaling, a material, an
experiment, or a device.


RELATED FILES
-------------
simulations/023c2aqs2r_n73_riemannian_newton_krylov_stationarity_closure.py
simulations/023c2aqs2_n73_stationarity_and_continuous_force_resolution.py
simulations/023c2a_n73_resolution_and_full_tangent_hessian.py
simulations/023c2aqs_continuous_field_active_source_force_integration.py
results/data/023c2aqs2r_n73_newton_krylov_checkpoint.npz

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023C2AQS2R2_ADAPTIVE_DAMPING_INEXACT_NEWTON_REPAIR
"""

from __future__ import annotations

import hashlib
import importlib.util
import math
import os
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import LinearOperator, minres


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

R_SOURCE = SIM / "023c2aqs2r_n73_riemannian_newton_krylov_stationarity_closure.py"
EXPECTED_R_SHA256 = "46fce3c29bb030ab6d4dbb890f1605f0ee95971fd5d5d28cc1c246110ff5dd14"

UPSTREAM_CHECKPOINT = DATA / "023c2aqs2r_n73_newton_krylov_checkpoint.npz"
CHECKPOINT = DATA / "023c2aqs2r2_n73_adaptive_newton_checkpoint.npz"
FINAL = DATA / "023c2aqs2r2_strict_stationary_b7_n73.npz"

B = 7
ETA = 0.4
MASS = 8.0
N = 73
GRAD_RMS_TOL = 1.5e-3
GRAD_MAX_TOL = 5.0e-2
MAX_NEIGHBOR_ANGLE = 0.70

MAX_OUTER = max(1, int(os.environ.get("AG_NK2_MAX_OUTER", "6")))
MINRES_MAXITER = max(6, int(os.environ.get("AG_NK2_MINRES_MAXITER", "28")))
HVP_POINT_ANGLE = float(os.environ.get("AG_NK2_HVP_POINT_ANGLE", "2e-4"))
MAX_LINESEARCH = max(4, int(os.environ.get("AG_NK2_MAX_LINESEARCH", "8")))
ARMIJO_C1 = float(os.environ.get("AG_NK2_ARMIJO_C1", "1e-4"))
RESIDUAL_FACTOR = float(os.environ.get("AG_NK2_RESIDUAL_FACTOR", "0.97"))
GMAX_GROWTH = float(os.environ.get("AG_NK2_GMAX_GROWTH", "1.35"))
DAMPING_MULTIPLIERS = tuple(
    float(x) for x in os.environ.get("AG_NK2_DAMPING_MULTIPLIERS", "0,0.02,0.10,0.50,2.0").split(",")
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def minres_compat(A, b, M, rtol, maxiter, callback):
    try:
        return minres(A, b, M=M, rtol=rtol, maxiter=maxiter, callback=callback, show=False, check=False)
    except TypeError:
        return minres(A, b, M=M, tol=rtol, maxiter=maxiter, callback=callback, show=False, check=False)


def load_state(r, qs2, cr3, cr4r):
    """Resume this repair first, otherwise the successful 023C2AQS2R state."""
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
    if b != B or abs(eta-ETA) > 1e-14 or abs(mass-MASS) > 1e-14:
        raise RuntimeError("N73 physical metadata mismatch")
    norm_err = float(np.max(np.abs(np.linalg.norm(phi, axis=-1) - 1.0)))
    if norm_err > 5e-10:
        raise RuntimeError(f"N73 S3 norm violation {norm_err}")
    history, discarded = qs2.history_from_arrays(cr3, s_hist, y_hist, dx)
    state = cr4r.State(phi=phi, axis=axis, dx=dx, accepted_total=accepted_total)
    return state, history, source, discarded, norm_err, nk_total


def save_checkpoint(state, history, E, rms, gmax, nk_total):
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    if history:
        s_hist = np.stack([item[0] for item in history], axis=0)
        y_hist = np.stack([item[1] for item in history], axis=0)
    else:
        s_hist = np.empty((0, N, N, N, 4), dtype=float)
        y_hist = np.empty((0, N, N, N, 4), dtype=float)
    np.savez(
        CHECKPOINT,
        phi=state.phi, axis=state.axis, dx=np.array(state.dx),
        B=np.array(B), eta=np.array(ETA), mass=np.array(MASS),
        accepted_total=np.array(state.accepted_total),
        newton_accepted_total=np.array(nk_total),
        energy=np.array(E), grad_rms=np.array(rms), grad_max=np.array(gmax),
        source=np.array("023C2AQS2R2_ADAPTIVE_DAMPING_INEXACT_NEWTON"),
        s_hist=s_hist, y_hist=y_hist,
    )
    print(
        f"NK2_CHECKPOINT_WRITTEN={CHECKPOINT.relative_to(ROOT)} "
        f"NEWTON_ACCEPTED_TOTAL={nk_total} HISTORY_LENGTH={len(history)}",
        flush=True,
    )


def save_final(state, E, rms, gmax, diag, nk_total):
    FINAL.parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        FINAL,
        phi=state.phi, axis=state.axis, dx=np.array(state.dx),
        B=np.array(B), eta=np.array(ETA), mass=np.array(MASS),
        accepted_total=np.array(state.accepted_total),
        newton_accepted_total=np.array(nk_total),
        energy=np.array(E), grad_rms=np.array(rms), grad_max=np.array(gmax),
        topology4=np.array(diag.topology4),
        active_total=np.array(diag.active_total),
        min_active_fraction=np.array(diag.min_active_fraction),
        min_dec_scaled_margin=np.array(diag.min_dec_scaled_margin),
        max_active_trace_scaled=np.array(diag.max_active_trace_scaled),
        source=np.array("023C2AQS2R2_N73_STRICT_STATIONARY"),
    )
    print(f"NK2_STRICT_STATIONARY_FIELD_ARTIFACT={FINAL.relative_to(ROOT)}", flush=True)


def inner_rtol_from_rms(rms: float) -> float:
    """Eisenstat-Walker-inspired bounded forcing schedule."""
    return min(0.08, max(0.008, 0.25*math.sqrt(max(rms, 1e-16))))


def adaptive_newton_slice(r, qs2, c2a, cr2, cr3, cr4r, state, history, nk_total):
    E, _E2, _E4, _E0, g, rms, gmax, station = r.strict_stationarity(cr3, state.phi, state.dx)
    stats = {
        "outer_attempted": 0,
        "outer_accepted": 0,
        "hvp_calls": 0,
        "minres_iterations": 0,
        "damping_trials": 0,
        "line_rejects": 0,
    }

    for outer in range(1, MAX_OUTER+1):
        if station:
            break
        stats["outer_attempted"] += 1
        phi = state.phi
        dx = state.dx
        basis = c2a.tangent_basis_householder(phi)
        Z = c2a.orthonormal_columns(c2a.isorotation_modes(phi, basis))
        ndof = basis.shape[0]*3
        gvec = c2a.project_subspace(c2a.field_to_components(g, basis), Z)
        gnorm = float(np.linalg.norm(gvec))

        spatial = c2a.spatial_symmetry_candidates(cr3, phi, state.axis, basis)
        if spatial.size:
            overlaps = np.abs(spatial.T@gvec) / max(gnorm, 1e-300)
            combined = float(np.linalg.norm(spatial.T@gvec) / max(gnorm, 1e-300))
        else:
            overlaps = np.zeros(0)
            combined = 0.0
        print(f"NK2_OUTER={outer} NDOF={ndof} GRAD_RMS={rms:.15e} GRAD_MAX={gmax:.15e}", flush=True)
        print(f"NK2_EXACT_ISOROTATION_ZERO_MODE_COUNT={Z.shape[1]}", flush=True)
        print("NK2_SPATIAL_SYMMETRY_GRAD_OVERLAPS=" + ",".join(f"{x:.9e}" for x in overlaps), flush=True)
        print(f"NK2_SPATIAL_SYMMETRY_COMBINED_GRAD_FRACTION={combined:.15e}", flush=True)

        if outer == 1:
            if not r.audit_hessian_operator(c2a, cr3, phi, state.axis, dx, basis, Z):
                raise RuntimeError("Adaptive Newton local HVP validation failed")

        hvp, calls = c2a.make_hvp(cr3, phi, dx, basis, Z, HVP_POINT_ANGLE)
        pairs = r.component_history(c2a, history, basis, Z)
        secant_scale = r.curvature_scale_from_pairs(pairs)
        print(f"NK2_PRECONDITIONER_USABLE_PAIRS={len(pairs)}", flush=True)
        print(f"NK2_SECANT_CURVATURE_SCALE={secant_scale:.15e}", flush=True)

        Hg = hvp(gvec)
        grad_rq = float(np.dot(gvec, Hg) / max(np.dot(gvec, gvec), 1e-300))
        smooth = c2a.smooth_random_vector(cr3, phi, basis, Z, 2026083121 + outer)
        Hs = hvp(smooth)
        smooth_rq = float(np.dot(smooth, Hs) / max(np.dot(smooth, smooth), 1e-300))
        local_scale = max(abs(grad_rq), 0.1*abs(smooth_rq), 1.0)
        mismatch = secant_scale/max(local_scale, 1e-300)
        print(f"NK2_GRADIENT_RAYLEIGH={grad_rq:.15e}", flush=True)
        print(f"NK2_SMOOTH_RAYLEIGH={smooth_rq:.15e}", flush=True)
        print(f"NK2_LOCAL_DAMPING_SCALE={local_scale:.15e}", flush=True)
        print(f"NK2_SECANT_TO_LOCAL_SCALE_RATIO={mismatch:.15e}", flush=True)

        def mvec(x):
            return r.lbfgs_inverse_vector(x, pairs, Z, c2a)

        M = LinearOperator((ndof, ndof), matvec=mvec, dtype=float) if pairs else None
        rhs = -gvec
        inner_rtol = inner_rtol_from_rms(rms)
        accepted_pack = None

        for mult in DAMPING_MULTIPLIERS:
            stats["damping_trials"] += 1
            mu = max(0.0, mult*local_scale)
            iter_count = {"n": 0}

            def avec(x):
                return hvp(x) + mu*c2a.project_subspace(np.asarray(x, dtype=float), Z)

            A = LinearOperator((ndof, ndof), matvec=avec, dtype=float)

            def cb(_xk):
                iter_count["n"] += 1

            delta, info = minres_compat(A, rhs, M, inner_rtol, MINRES_MAXITER, cb)
            stats["minres_iterations"] += iter_count["n"]
            delta = c2a.project_subspace(np.asarray(delta, dtype=float), Z)
            Hdelta = hvp(delta)
            linear_rel = float(np.linalg.norm(gvec + Hdelta) / max(gnorm, 1e-300))
            shifted_rel = float(np.linalg.norm(gvec + Hdelta + mu*delta) / max(gnorm, 1e-300))
            direction = c2a.components_to_field(delta, basis, phi.shape)
            direction = cr3.project_tangent(phi, direction)
            gd = cr3.tangent_inner(g, direction, dx)
            dd = cr3.tangent_inner(direction, direction, dx)
            max_point = float(np.max(np.linalg.norm(direction[1:-1,1:-1,1:-1], axis=-1)))
            trust_angle = min(2.0e-2, max(2.0e-3, 0.25*rms))
            alpha0 = min(1.0, trust_angle/max(max_point, 1e-300))
            print(
                f"NK2_LINEAR_SOLVE_OUTER={outer} DAMP_MULT={mult:.6e} MU={mu:.15e} "
                f"MINRES_INFO={info} MINRES_ITERS={iter_count['n']} RTOL={inner_rtol:.9e} "
                f"LINEAR_MODEL_RELRES={linear_rel:.15e} SHIFTED_RELRES={shifted_rel:.15e} "
                f"G_DOT_DELTA={gd:.15e} DELTA_NORM2={dd:.15e} MAX_POINT={max_point:.15e} "
                f"TRUST_ANGLE={trust_angle:.15e} ALPHA0={alpha0:.15e}",
                flush=True,
            )
            if info < 0:
                print("NK2_LINEAR_DIRECTION=MINRES_BREAKDOWN_TRY_MORE_DAMPING", flush=True)
                continue
            if (not math.isfinite(gd)) or gd >= -1e-12*max(cr3.tangent_inner(g,g,dx), 1e-300):
                print("NK2_LINEAR_DIRECTION_DESCENT=NO_TRY_MORE_DAMPING", flush=True)
                continue
            print("NK2_LINEAR_DIRECTION_DESCENT=YES", flush=True)

            alpha = alpha0
            for ls in range(MAX_LINESEARCH):
                cand = cr3.exp_map_update(phi, direction, alpha)
                Etrial = cr3.high_order_energy_gradient(cand, dx, False)[0]
                if (not math.isfinite(Etrial)) or Etrial > E + ARMIJO_C1*alpha*gd:
                    stats["line_rejects"] += 1
                    alpha *= 0.5
                    continue
                ok, reason, _ = qs2.candidate_admissible(cr3, cr2, cand, dx, state.accepted_total+1)
                if not ok:
                    stats["line_rejects"] += 1
                    print(f"NK2_LINESEARCH_REJECT_REASON={reason}", flush=True)
                    alpha *= 0.5
                    continue
                pack = r.strict_stationarity(cr3, cand, dx)
                Enew, _e2n, _e4n, _e0n, gnew, rmsnew, gmaxnew, stationnew = pack
                residual_ok = bool(
                    rmsnew <= RESIDUAL_FACTOR*rms
                    and gmaxnew <= max(GMAX_GROWTH*gmax, 10.0*GRAD_MAX_TOL)
                )
                print(
                    f"NK2_LINESEARCH_TRIAL_OUTER={outer} DAMP_MULT={mult:.6e} LS={ls} "
                    f"ALPHA={alpha:.15e} ENERGY={Enew:.15e} GRAD_RMS={rmsnew:.15e} "
                    f"GRAD_MAX={gmaxnew:.15e} RESIDUAL_ACCEPT={'YES' if residual_ok else 'NO'}",
                    flush=True,
                )
                if not residual_ok:
                    stats["line_rejects"] += 1
                    alpha *= 0.5
                    continue
                accepted_pack = (cand, Enew, gnew, rmsnew, gmaxnew, stationnew, direction, alpha, mult, mu, linear_rel)
                break
            if accepted_pack is not None:
                break

        stats["hvp_calls"] += calls["count"]
        if accepted_pack is None:
            print("NK2_NEWTON_STEP_ACCEPTED=NO", flush=True)
            break

        cand, Enew, gnew, rmsnew, gmaxnew, stationnew, direction, alpha, mult_used, mu_used, linear_rel_used = accepted_pack
        old_phi = phi
        old_g = g
        old_rms = rms
        old_gmax = gmax
        history = r.transport_history_after_step(cr3, cr4r, old_phi, cand, direction, alpha, old_g, gnew, history)
        state.phi = cand
        state.accepted_total += 1
        nk_total += 1
        stats["outer_accepted"] += 1
        E, g, rms, gmax, station = Enew, gnew, rmsnew, gmaxnew, stationnew
        t4 = cr3.topology4(state.phi, state.dx)
        deg_ok, degrees = cr3.geometric_guard(state.phi, cr2, True)
        angle = cr3.max_neighbor_angle(state.phi)
        print(
            f"NK2_NEWTON_STEP_ACCEPTED=YES OUTER={outer} DAMP_MULT={mult_used:.6e} "
            f"MU={mu_used:.15e} ALPHA={alpha:.15e} LINEAR_MODEL_RELRES={linear_rel_used:.15e} "
            f"RMS_REDUCTION_FACTOR={old_rms/max(rms,1e-300):.15e} "
            f"GMAX_REDUCTION_FACTOR={old_gmax/max(gmax,1e-300):.15e} ENERGY={E:.15e} "
            f"GRAD_RMS={rms:.15e} GRAD_MAX={gmax:.15e} TOPOLOGY4={t4:.15e} "
            f"GEOMETRIC_DEGREES={','.join(str(x) for x in degrees)} MAX_NEIGHBOR_ANGLE={angle:.15e}",
            flush=True,
        )
        if not deg_ok:
            raise RuntimeError("Accepted adaptive Newton step lost geometric B=7")
        save_checkpoint(state, history, E, rms, gmax, nk_total)

    return state, history, E, g, rms, gmax, station, nk_total, stats


def main():
    print("=== 023C2AQS2R2 — N73 ADAPTIVE-DAMPING INEXACT NEWTON CLOSURE ===", flush=True)

    print("\n=== A — FAIL-CLOSED UPSTREAM AUDIT ===", flush=True)
    require(R_SOURCE)
    actual = sha256(R_SOURCE)
    print(f"023C2AQS2R_SOURCE_SHA256={actual}", flush=True)
    if actual != EXPECTED_R_SHA256:
        raise RuntimeError("023C2AQS2R source hash mismatch")
    print("UPSTREAM_023C2AQS2R_AUDIT=PASS", flush=True)

    r = load_module("c2aqs2r2_r", R_SOURCE)
    qs2 = load_module("c2aqs2r2_qs2", r.QS2_SOURCE)
    c2a = load_module("c2aqs2r2_c2a", r.C2A_SOURCE)
    c2ar = qs2.load_module("c2aqs2r2_c2ar", qs2.C2AR_SOURCE)
    c2aqs = qs2.load_module("c2aqs2r2_c2aqs", qs2.C2AQS_SOURCE)
    cr2 = c2ar.load_module("c2aqs2r2_cr2", c2ar.CR2_SOURCE)
    cr3 = c2ar.load_module("c2aqs2r2_cr3", c2ar.CR3_SOURCE)
    cr4r = c2ar.load_module("c2aqs2r2_cr4r", c2ar.CR4R_SOURCE)

    print("\n=== B — LOAD N73 NEWTON CHECKPOINT ===", flush=True)
    state, history, source, discarded, norm_err, nk_total = load_state(r, qs2, cr3, cr4r)
    E0, _a, _b, _c, g0, rms0, gmax0, station0 = r.strict_stationarity(cr3, state.phi, state.dx)
    deg_ok0, deg0 = cr3.geometric_guard(state.phi, cr2, True)
    print(f"NK2_START_SOURCE={source.relative_to(ROOT)}", flush=True)
    print(f"NK2_START_ACCEPTED_TOTAL={state.accepted_total}", flush=True)
    print(f"NK2_START_NEWTON_ACCEPTED_TOTAL={nk_total}", flush=True)
    print(f"NK2_START_HISTORY_LENGTH={len(history)}", flush=True)
    print(f"NK2_START_HISTORY_DISCARDED={discarded}", flush=True)
    print(f"NK2_START_NORM_MAXERR={norm_err:.15e}", flush=True)
    print(f"NK2_START_ENERGY={E0:.15e}", flush=True)
    print(f"NK2_START_GRAD_RMS={rms0:.15e}", flush=True)
    print(f"NK2_START_GRAD_MAX={gmax0:.15e}", flush=True)
    print("NK2_START_STRICT_STATIONARITY=" + ("PASS" if station0 else "FAIL"), flush=True)
    print(f"NK2_START_TOPOLOGY4={cr3.topology4(state.phi,state.dx):.15e}", flush=True)
    print("NK2_START_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in deg0), flush=True)
    if not deg_ok0:
        raise RuntimeError("Starting N73 field failed geometric B=7")

    if station0:
        E, g, rms, gmax, station = E0, g0, rms0, gmax0, station0
        stats = {"outer_attempted":0,"outer_accepted":0,"hvp_calls":0,"minres_iterations":0,"damping_trials":0,"line_rejects":0}
    else:
        print("\n=== C — ADAPTIVE-DAMPING MATRIX-FREE NEWTON-KRYLOV ===", flush=True)
        state, history, E, g, rms, gmax, station, nk_total, stats = adaptive_newton_slice(
            r, qs2, c2a, cr2, cr3, cr4r, state, history, nk_total
        )

    print("\n=== D — END-OF-SLICE AUDIT ===", flush=True)
    t4 = cr3.topology4(state.phi, state.dx)
    deg_ok, degrees = cr3.geometric_guard(state.phi, cr2, True)
    angle = cr3.max_neighbor_angle(state.phi)
    print(f"NK2_OUTER_ATTEMPTED={stats['outer_attempted']}", flush=True)
    print(f"NK2_OUTER_ACCEPTED={stats['outer_accepted']}", flush=True)
    print(f"NK2_HVP_MATVEC_CALLS={stats['hvp_calls']}", flush=True)
    print(f"NK2_MINRES_TOTAL_ITERATIONS={stats['minres_iterations']}", flush=True)
    print(f"NK2_DAMPING_TRIALS={stats['damping_trials']}", flush=True)
    print(f"NK2_LINESEARCH_REJECTS={stats['line_rejects']}", flush=True)
    print(f"NK2_FINAL_ENERGY={E:.15e}", flush=True)
    print(f"NK2_FINAL_GRAD_RMS={rms:.15e}", flush=True)
    print(f"NK2_FINAL_GRAD_MAX={gmax:.15e}", flush=True)
    print("NK2_FINAL_STRICT_STATIONARITY=" + ("PASS" if station else "FAIL"), flush=True)
    print(f"NK2_FINAL_TOPOLOGY4={t4:.15e}", flush=True)
    print("NK2_FINAL_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in degrees), flush=True)
    print(f"NK2_FINAL_MAX_NEIGHBOR_ANGLE={angle:.15e}", flush=True)

    if not station:
        save_checkpoint(state, history, E, rms, gmax, nk_total)
        print("\n=== E — BOUNDED INCOMPLETE DECISION ===", flush=True)
        print("023C2AQS2R2_N73_ADAPTIVE_NEWTON=INCOMPLETE_SHORT_ADAPTIVE_NEWTON_SLICE", flush=True)
        print("N73_ACTUAL_FINE_STRICT_STATIONARITY=NOT_YET", flush=True)
        if stats["outer_accepted"] > 0:
            print("ADAPTIVE_NEWTON_LOCAL_ACCELERATION=SUPPORTED", flush=True)
            print("NEXT=RERUN_SAME_023C2AQS2R2_FROM_ADAPTIVE_NEWTON_CHECKPOINT", flush=True)
        else:
            print("ADAPTIVE_NEWTON_LOCAL_ACCELERATION=NOT_ESTABLISHED", flush=True)
            print("NEXT=RESIDUAL_SPECTRAL_MODE_DIAGNOSTIC_BEFORE_ANY_MORE_LONG_SOLVES", flush=True)
        print("N73_CONTINUOUS_FORCE=NOT_RUN_BEFORE_STATIONARITY", flush=True)
        print("FULL_PHYSICAL_HESSIAN=DEFERRED_OPERATIONAL_FORCE_AND_FINE_FIELD_UNRESOLVED", flush=True)
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR_NOT_A_PROBABILITY", flush=True)
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED", flush=True)
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
        return

    print("\n=== E — STRICT N73 PHYSICAL FIELD AUDIT ===", flush=True)
    diag = cr3.continuum_local_diagnostics(state.phi, state.axis, state.dx, cr2)
    print(f"NK2_N73_STATIONARY_CONTINUUM_ENERGY={diag.energy_continuum:.15e}", flush=True)
    print(f"NK2_N73_STATIONARY_ACTIVE_TOTAL={diag.active_total:.15e}", flush=True)
    print(f"NK2_N73_STATIONARY_ACTIVE_TO_ENERGY={diag.active_to_energy:.15e}", flush=True)
    print(f"NK2_N73_STATIONARY_MIN_ACTIVE_FRACTION={diag.min_active_fraction:.15e}", flush=True)
    print(f"NK2_N73_STATIONARY_MIN_DEC_SCALED_MARGIN={diag.min_dec_scaled_margin:.15e}", flush=True)
    print(f"NK2_N73_STATIONARY_MAX_ACTIVE_TRACE_SCALED={diag.max_active_trace_scaled:.15e}", flush=True)
    print(f"NK2_N73_STATIONARY_ENERGY_CENTROID_NORM={diag.energy_centroid_norm:.15e}", flush=True)
    physical_gate = bool(
        deg_ok and diag.active_total > 0.0 and diag.min_active_fraction <= -1.0e-2
        and diag.min_dec_scaled_margin >= -1.0e-9
        and diag.max_active_trace_scaled <= 1.0e-10
        and angle <= MAX_NEIGHBOR_ANGLE
    )
    print("NK2_N73_STATIONARY_PHYSICAL_FIELD_GATE=" + ("PASS" if physical_gate else "FAIL"), flush=True)
    save_final(state, E, rms, gmax, diag, nk_total)

    if not physical_gate:
        print("023C2AQS2R2_N73_ADAPTIVE_NEWTON=RED_STRICT_N73_PHYSICAL_FIELD_GATE", flush=True)
        print("FULL_PHYSICAL_HESSIAN=DEFERRED_BY_FINE_FIELD_PHYSICAL_FALSIFIER", flush=True)
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_PENDING_RERANK", flush=True)
        print("NEXT=PRESERVE_NEGATIVE_RESULT_AND_RERANK_023_BRANCH", flush=True)
        return

    print("\n=== F — CONDITIONAL CONTINUOUS-FORCE CERTIFICATE ===", flush=True)
    n65ref = qs2.load_n65_force_reference()
    aqr = c2aqs.load_module("c2aqs2r2_aqr", c2aqs.AQR_SOURCE)
    aqr.validate_analytic_formulae()
    print("NK2_N73_ANALYTIC_KERNEL_VALIDATION=PASS", flush=True)
    force = qs2.continuous_force_gate(c2aqs, aqr, cr3, state.phi, state.axis, state.dx, n65ref)

    print("\n=== G — 023C2AQS2R2 DECISION ===", flush=True)
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

    print(f"023C2AQS2R2_N73_ADAPTIVE_NEWTON={decision}", flush=True)
    print("N73_ACTUAL_FINE_STRICT_STATIONARITY=PASS", flush=True)
    print(f"FULL_PHYSICAL_HESSIAN={hessian}", flush=True)
    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR_NOT_A_PROBABILITY", flush=True)
    print(f"NEXT={next_step}", flush=True)
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED_UNTIL_023C_COMPLETE", flush=True)
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
    print("NEW_PHYSICS_DISCOVERY=NO", flush=True)
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023C2AQS2R2_ADAPTIVE_DAMPING_INEXACT_NEWTON_REPAIR", flush=True)


if __name__ == "__main__":
    main()
