#!/usr/bin/env python3
"""023C2AQS2R — N=73 Riemannian Newton-Krylov stationarity closure.

PURPOSE
-------
Close the remaining N=73 Euler-Lagrange residual of the strongest surviving
B=7 false-core Skyrmion branch more efficiently than continued long R-LBFGS
slices, then conditionally evaluate the already-validated continuous finite-
payload force observable exactly once if strict stationarity is reached.

SCIENTIFIC QUESTION
-------------------
The actual N=73 field has preserved |B|=7 and monotonically lowered the same
checkerboard-free fourth-order discrete action through 400 accepted R-LBFGS
steps, but the residual has entered a slowly convergent, ill-conditioned local
regime.  Is this merely first-order/quasi-Newton conditioning, so that a
matrix-free second-order correction can close the same stationary equations
without changing the model, topology guards, or stationarity thresholds?

WHY THIS RUN EXISTS / INFORMATION-GAIN STOP RULE
------------------------------------------------
023C2AQS2 reduced the N=73 RMS gradient from approximately 0.613 to 0.0995 in
160 accepted steps while retaining 20 positive-curvature L-BFGS secant pairs.
A continuation at the same empirical rate would require hundreds more accepted
steps to reach the unchanged strict threshold 1.5e-3.  The earlier 023CR4R
stop rule explicitly authorizes a targeted Newton-Krylov/preconditioner gate
when R-LBFGS becomes slow near stationarity.

This file therefore does NOT launch another long first-order block.  It uses
matrix-free Riemannian Hessian-vector products and a truncated, regularized
Newton solve.  The existing L-BFGS inverse approximation is reused only as an
SPD Krylov preconditioner.  If a short Newton-Krylov slice does not materially
reduce the residual, the run stops and reports numerical incompleteness rather
than consuming an unbounded number of iterations.

MODEL / EQUATIONS
-----------------
The field and discrete action are unchanged from 023CR3/023CR4R/023C2AQS2:

    phi = (sigma, pi1, pi2, pi3),      phi . phi = 1

    E = integral (e2 + e4 + V) d^3x

    V = m^2 (1-sigma)(1+eta sigma)

with B=7, eta=0.4, m=8 and the parity-symmetrized checkerboard-free
fourth-order one-sided derivative action.

At a base field phi, let g be the projected Riemannian gradient density and H
its covariant derivative.  Each Newton correction approximately solves

    (H + mu I) delta = -g

in the complete three-component tangent space of every non-boundary lattice
site.  The three exact global pion-isorotation zero modes are projected out.
Translations and spatial rotations are measured diagnostically but are NOT
projected out because the finite Cartesian lattice/box breaks them.

The Hessian-vector product is matrix-free:

    H v ~= PT_{+ -> 0} g(exp_phi(+eps v))
           - PT_{- -> 0} g(exp_phi(-eps v))
           ---------------------------------
                         2 eps

where PT is exact parallel transport on S^3 along the sitewise geodesic.

NUMERICAL METHOD
----------------
1. Load the latest 023C2AQS2 N=73 field and its 20-pair transported L-BFGS
   history.
2. Recompute the exact analytic discrete gradient and unchanged strict
   stationarity thresholds.
3. Build a complete 3-DOF/site tangent basis and project the exact global
   isorotation zero modes.
4. Audit one Hessian-vector product at three finite-difference point angles and
   audit bilinear self-adjointness before using second-order information.
5. Convert the positive-curvature L-BFGS history into a symmetric positive
   inverse-Hessian preconditioner on the projected tangent subspace.
6. Approximately solve a mildly regularized Newton equation with MINRES.  The
   inner solve is deliberately inexact/truncated; high precision is unnecessary
   far from the root.
7. Accept a Newton correction only after Armijo energy decrease, exact
   topology/smoothness guards, and an explicit residual-decrease test.
8. Checkpoint after every accepted Newton correction.
9. If strict stationarity is reached, run the same physical-field audit and
   cubic/quintic continuous-force certificate already validated by 023C2AQS2.

The approach follows standard large-scale truncated-Newton practice: use only
Hessian-vector products, solve the Newton equation inexactly, and precondition
using available curvature information.  The manifold constraint is respected
with S^3 exponential maps and parallel transport throughout.

INPUTS
------
Primary checkpoint:
    results/data/023c2aqs2_n73_stationarity_checkpoint.npz

If this repair has already accepted a Newton step, it resumes instead from:
    results/data/023c2aqs2r_n73_newton_krylov_checkpoint.npz

Upstream source files are hash-audited before use.

OUTPUTS
-------
Checkpoint:
    results/data/023c2aqs2r_n73_newton_krylov_checkpoint.npz

Strict-stationary artifact, if reached:
    results/data/023c2aqs2r_strict_stationary_b7_n73.npz

The terminal log reports:
- residual and symmetry-overlap diagnostics;
- Hessian-vector step-size convergence;
- Hessian bilinear self-adjointness;
- usable L-BFGS preconditioner pairs and curvature scale;
- MINRES iteration/matvec counts and regularization;
- accepted Newton residual reduction;
- unchanged topology/smoothness diagnostics;
- conditional continuous-force certificate.

UNITS / SIGN CONVENTIONS
------------------------
All quantities use the dimensionless Skyrme normalization inherited from the
023 branch.  Positive radial finite-payload force means outward acceleration in
the project's linearized-GR convention.

PROMOTION CONDITION
-------------------
This repair may establish only strict N=73 stationarity and, conditionally, the
single declared continuous-force sentinel.  The stationarity thresholds are
UNCHANGED:

    GRAD_RMS <= 1.5e-3
    GRAD_MAX <= 5.0e-2

A positive continuous-force result is certified only by the unchanged
023C2AQS2 cubic/quintic error rule.  No threshold is weakened.

FALSIFIERS / STOP RULES
-----------------------
- Loss of |B|=7, smoothness, DEC, positive total active mass, or the negative
  active region is a physical blocker to this branch.
- Failure of Hessian-vector step convergence or self-adjointness is numerical
  incompleteness; do not trust the Newton correction.
- A short Newton-Krylov slice that cannot produce a residual-reducing admissible
  step stops for residual-mode/preconditioner diagnosis rather than returning
  to hundreds of blind R-LBFGS iterations.
- A certified inward continuous-force sentinel at strict N=73 stationarity is
  a finite-payload falsifier for the declared operating point, subject to the
  planned companion-resolution confirmation.
- Do not launch the full physical Hessian until operational force resolution is
  established at companion resolutions.

VALIDATION
----------
- Fail-closed upstream source hashes.
- Existing 94 known-solution regression suite is run externally by the shell
  block supplied with this file.
- Exact discrete gradient comes unchanged from 023CR3 and its established
  directional self-check.
- Hessian-vector finite-difference step convergence is checked at the actual
  N=73 field.
- Hessian bilinear self-adjointness is checked on independent smooth vectors.
- Exact topology and link-smoothness guards are retained for every accepted
  Newton correction.
- Existing continuous-force machinery is reused rather than reimplemented.

LIMITATIONS / CLAIM BOUNDARIES
-----------------------------
This file does NOT establish:
- a positive physical Hessian or unrestricted stability;
- N=73/N=81 continuum force convergence;
- binary fission stability;
- a nonlinear Einstein-Skyrme solution;
- practical energy scaling;
- a real material or device;
- discovery of new physics.

RELATED FILES
-------------
simulations/023cr3_geometric_degree_guarded_unrestricted_relaxation.py
simulations/023cr4r_rlbfgs_stationarity_closure_gradient_audit_repair.py
simulations/023c2a_n73_resolution_and_full_tangent_hessian.py
simulations/023c2aqs_continuous_field_active_source_force_integration.py
simulations/023c2aqs2_n73_stationarity_and_continuous_force_resolution.py

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023C2AQS2R_RIEMANNIAN_NEWTON_KRYLOV_STATIONARITY_REPAIR

NOVEL PHYSICS CLAIM
-------------------
NO
"""

from __future__ import annotations

import hashlib
import importlib.util
import math
import os
import sys
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import LinearOperator, minres


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

QS2_SOURCE = SIM / "023c2aqs2_n73_stationarity_and_continuous_force_resolution.py"
C2A_SOURCE = SIM / "023c2a_n73_resolution_and_full_tangent_hessian.py"

EXPECTED_QS2_SHA256 = "99e716b4af2c00aca5aa32874bbbb772013d849419683b2ee75200e5c5c7ab1d"
EXPECTED_C2A_SHA256 = "0862560521ef4088744879435c193824f75a032a2040ee3475e005ad54147a51"

UPSTREAM_CHECKPOINT = DATA / "023c2aqs2_n73_stationarity_checkpoint.npz"
CHECKPOINT = DATA / "023c2aqs2r_n73_newton_krylov_checkpoint.npz"
FINAL = DATA / "023c2aqs2r_strict_stationary_b7_n73.npz"

B = 7
ETA = 0.4
MASS = 8.0
N = 73
GRAD_RMS_TOL = 1.5e-3
GRAD_MAX_TOL = 5.0e-2
MAX_NEIGHBOR_ANGLE = 0.70

MAX_NEWTON_OUTER = max(1, int(os.environ.get("AG_NK_MAX_OUTER", "3")))
MINRES_MAXITER = max(4, int(os.environ.get("AG_NK_MINRES_MAXITER", "18")))
MINRES_RTOL_MAX = float(os.environ.get("AG_NK_MINRES_RTOL_MAX", "0.15"))
MINRES_RTOL_MIN = float(os.environ.get("AG_NK_MINRES_RTOL_MIN", "0.03"))
HVP_POINT_ANGLE = float(os.environ.get("AG_NK_HVP_POINT_ANGLE", "2e-4"))
HVP_STEP_REL_TOL = float(os.environ.get("AG_NK_HVP_STEP_REL_TOL", "1.5e-2"))
HVP_SELFADJ_REL_TOL = float(os.environ.get("AG_NK_HVP_SELFADJ_REL_TOL", "5.0e-3"))
NEWTON_RESIDUAL_FACTOR = float(os.environ.get("AG_NK_RESIDUAL_ACCEPT_FACTOR", "0.90"))
NEWTON_GMAX_GROWTH = float(os.environ.get("AG_NK_GMAX_GROWTH", "1.25"))
ARMIJO_C1 = 1.0e-4
MAX_LINESEARCH = max(6, int(os.environ.get("AG_NK_MAX_LINESEARCH", "10")))
CAUTIOUS_CURVATURE = 1.0e-10


def sha256(path: Path) -> str:
    """Return SHA-256 for a source artifact."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def require(path: Path) -> None:
    """Fail closed when a required upstream artifact is absent."""
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def load_module(name: str, path: Path):
    """Import a Python source file by absolute path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def strict_stationarity(cr3, phi: np.ndarray, dx: float):
    """Recompute exact discrete energy, Riemannian gradient, and thresholds."""
    E, E2, E4, E0, g = cr3.riemannian_gradient_density(phi, dx)
    rms, gmax = cr3.gradient_norms(g)
    return E, E2, E4, E0, g, rms, gmax, bool(rms <= GRAD_RMS_TOL and gmax <= GRAD_MAX_TOL)


def load_state(qs2, cr3, cr4r):
    """Load this repair checkpoint first, else the latest 023C2AQS2 state."""
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
        if "s_hist" in d.files and "y_hist" in d.files:
            s_hist = np.asarray(d["s_hist"], dtype=float)
            y_hist = np.asarray(d["y_hist"], dtype=float)
        else:
            s_hist = np.empty((0, N, N, N, 4), dtype=float)
            y_hist = np.empty((0, N, N, N, 4), dtype=float)
        nk_total = int(d["newton_accepted_total"]) if "newton_accepted_total" in d.files else 0
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


def save_checkpoint(state, history, E: float, rms: float, gmax: float, nk_total: int) -> None:
    """Persist field and transported L-BFGS history after a Newton correction."""
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
        B=np.array(B), eta=np.array(ETA), mass=np.array(MASS),
        accepted_total=np.array(state.accepted_total),
        newton_accepted_total=np.array(nk_total),
        energy=np.array(E), grad_rms=np.array(rms), grad_max=np.array(gmax),
        source=np.array("023C2AQS2R_RIEMANNIAN_NEWTON_KRYLOV"),
        s_hist=s_hist, y_hist=y_hist,
    )
    print(
        f"NK_CHECKPOINT_WRITTEN={CHECKPOINT.relative_to(ROOT)} "
        f"NEWTON_ACCEPTED_TOTAL={nk_total} HISTORY_LENGTH={len(history)}",
        flush=True,
    )


def save_final(state, E: float, rms: float, gmax: float, diag, nk_total: int) -> None:
    """Persist the strict-stationary N=73 field with physical diagnostics."""
    FINAL.parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        FINAL,
        phi=state.phi,
        axis=state.axis,
        dx=np.array(state.dx),
        B=np.array(B), eta=np.array(ETA), mass=np.array(MASS),
        accepted_total=np.array(state.accepted_total),
        newton_accepted_total=np.array(nk_total),
        energy=np.array(E), grad_rms=np.array(rms), grad_max=np.array(gmax),
        topology4=np.array(diag.topology4),
        active_total=np.array(diag.active_total),
        min_active_fraction=np.array(diag.min_active_fraction),
        min_dec_scaled_margin=np.array(diag.min_dec_scaled_margin),
        max_active_trace_scaled=np.array(diag.max_active_trace_scaled),
        source=np.array("023C2AQS2R_N73_STRICT_STATIONARY"),
    )
    print(f"NK_STRICT_STATIONARY_FIELD_ARTIFACT={FINAL.relative_to(ROOT)}", flush=True)


def component_history(c2a, history, basis, Z):
    """Convert transported field-space secant pairs to projected coordinates."""
    pairs = []
    for s, y, _rho in history:
        sv = c2a.project_subspace(c2a.field_to_components(s, basis), Z)
        yv = c2a.project_subspace(c2a.field_to_components(y, basis), Z)
        sy = float(np.dot(sv, yv))
        ss = float(np.dot(sv, sv))
        yy = float(np.dot(yv, yv))
        if (
            math.isfinite(sy) and sy > 1e-14 * math.sqrt(max(ss*yy, 0.0))
            and ss > 0.0 and yy > 0.0
        ):
            pairs.append((sv, yv, 1.0/sy))
    return pairs


def lbfgs_inverse_vector(v: np.ndarray, pairs, Z, c2a) -> np.ndarray:
    """Apply the positive-curvature limited-memory inverse Hessian approximation."""
    q = c2a.project_subspace(np.asarray(v, dtype=float), Z).copy()
    if not pairs:
        return q
    alphas = []
    for s, y, rho in reversed(pairs):
        a = rho * float(np.dot(s, q))
        alphas.append(a)
        q -= a*y
    s_last, y_last, _ = pairs[-1]
    sy = float(np.dot(s_last, y_last))
    yy = float(np.dot(y_last, y_last))
    gamma = sy / max(yy, 1e-300)
    gamma = min(max(gamma, 1e-8), 1e8)
    r = gamma*q
    for (s, y, rho), a in zip(pairs, reversed(alphas)):
        beta = rho * float(np.dot(y, r))
        r += s*(a-beta)
    return c2a.project_subspace(r, Z)


def curvature_scale_from_pairs(pairs) -> float:
    """Return a robust positive local Hessian scale inferred from secant pairs."""
    vals = []
    for s, y, _rho in pairs:
        sy = float(np.dot(s, y))
        yy = float(np.dot(y, y))
        if sy > 0.0 and math.isfinite(sy) and math.isfinite(yy):
            vals.append(yy/sy)
    if not vals:
        return 1.0
    return float(np.median(np.asarray(vals, dtype=float)))


def relative_vector_difference(a: np.ndarray, b: np.ndarray) -> float:
    """Scale-aware Euclidean relative difference."""
    return float(np.linalg.norm(a-b) / max(np.linalg.norm(a), np.linalg.norm(b), 1e-300))


def audit_hessian_operator(c2a, cr3, phi, axis, dx, basis, Z):
    """Validate local HVP step convergence and bilinear self-adjointness."""
    v = c2a.smooth_random_vector(cr3, phi, basis, Z, 2026083101)
    hvals = []
    for pa in (0.5*HVP_POINT_ANGLE, HVP_POINT_ANGLE, 2.0*HVP_POINT_ANGLE):
        hvp, calls = c2a.make_hvp(cr3, phi, dx, basis, Z, pa)
        hv = hvp(v)
        hvals.append(hv)
        rq = float(np.dot(v, hv) / max(np.dot(v, v), 1e-300))
        print(
            f"NK_HVP_STEP_POINT_ANGLE={pa:.15e} RAYLEIGH={rq:.15e} "
            f"MATVECS={calls['count']}", flush=True,
        )
    d01 = relative_vector_difference(hvals[0], hvals[1])
    d12 = relative_vector_difference(hvals[1], hvals[2])
    step_ok = bool(min(d01, d12) <= HVP_STEP_REL_TOL)
    print(f"NK_HVP_STEP_RELCHANGE_FINE_PRIMARY={d01:.15e}", flush=True)
    print(f"NK_HVP_STEP_RELCHANGE_PRIMARY_COARSE={d12:.15e}", flush=True)
    print("NK_HVP_STEP_CONVERGENCE=" + ("PASS" if step_ok else "FAIL"), flush=True)

    hvp, calls = c2a.make_hvp(cr3, phi, dx, basis, Z, HVP_POINT_ANGLE)
    u = c2a.smooth_random_vector(cr3, phi, basis, Z, 2026083102)
    w = c2a.smooth_random_vector(cr3, phi, basis, Z, 2026083103)
    Hu = hvp(u)
    Hw = hvp(w)
    a = float(np.dot(u, Hw))
    b = float(np.dot(Hu, w))
    asym = abs(a-b) / max(abs(a), abs(b), 1e-300)
    selfadj = bool(asym <= HVP_SELFADJ_REL_TOL)
    print(f"NK_HESSIAN_BILINEAR_UHV={a:.15e}", flush=True)
    print(f"NK_HESSIAN_BILINEAR_HUW={b:.15e}", flush=True)
    print(f"NK_HESSIAN_BILINEAR_RELASYM={asym:.15e}", flush=True)
    print("NK_HESSIAN_SELF_ADJOINTNESS=" + ("PASS" if selfadj else "FAIL"), flush=True)
    return step_ok and selfadj


def minres_compat(A, b, M, rtol, maxiter, callback):
    """Call SciPy MINRES across rtol/tol API generations."""
    try:
        return minres(A, b, M=M, rtol=rtol, maxiter=maxiter, callback=callback, show=False, check=False)
    except TypeError:
        return minres(A, b, M=M, tol=rtol, maxiter=maxiter, callback=callback, show=False, check=False)


def transport_history_after_step(cr3, cr4r, old_phi, new_phi, direction, alpha, old_g, new_g, history):
    """Transport existing secant memory and add the accepted Newton secant pair."""
    geom = cr4r.transport_geometry(old_phi, direction, alpha, new_phi)
    transported = []
    for s_old, y_old, _rho_old in history:
        st = cr4r.exact_parallel_transport(old_phi, geom, s_old, cr3)
        yt = cr4r.exact_parallel_transport(old_phi, geom, y_old, cr3)
        sy = cr3.tangent_inner(st, yt, 1.0)  # dx^3 is a common positive factor.
        if math.isfinite(sy) and sy > 1e-300:
            transported.append((st, yt, 1.0/sy))

    g_old_t = cr4r.exact_parallel_transport(old_phi, geom, old_g, cr3)
    step_old = alpha*direction
    s_new = cr4r.exact_parallel_transport(old_phi, geom, step_old, cr3)
    y_new = new_g - g_old_t
    ss = cr3.tangent_inner(s_new, s_new, 1.0)
    yy = cr3.tangent_inner(y_new, y_new, 1.0)
    sy = cr3.tangent_inner(s_new, y_new, 1.0)
    cautious = CAUTIOUS_CURVATURE*math.sqrt(max(ss*yy, 0.0))
    if math.isfinite(sy) and sy > max(cautious, 1e-300):
        transported.append((s_new, y_new, 1.0/sy))
    return transported[-20:]


def newton_krylov_slice(qs2, c2a, cr2, cr3, cr4r, state, history, nk_total):
    """Perform a short sequence of regularized, preconditioned Newton corrections."""
    E, _E2, _E4, _E0, g, rms, gmax, station = strict_stationarity(cr3, state.phi, state.dx)
    stats = {
        "outer_attempted": 0,
        "outer_accepted": 0,
        "hvp_calls": 0,
        "minres_iterations": 0,
        "damping_retries": 0,
        "line_rejects": 0,
    }

    for outer in range(1, MAX_NEWTON_OUTER+1):
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
        print(f"NK_OUTER={outer} NDOF={ndof} GRAD_RMS={rms:.15e} GRAD_MAX={gmax:.15e}", flush=True)
        print(f"NK_EXACT_ISOROTATION_ZERO_MODE_COUNT={Z.shape[1]}", flush=True)
        print("NK_SPATIAL_SYMMETRY_GRAD_OVERLAPS=" + ",".join(f"{x:.9e}" for x in overlaps), flush=True)
        print(f"NK_SPATIAL_SYMMETRY_COMBINED_GRAD_FRACTION={combined:.15e}", flush=True)

        if outer == 1:
            if not audit_hessian_operator(c2a, cr3, phi, state.axis, dx, basis, Z):
                raise RuntimeError("Local Hessian-vector operator validation failed")

        hvp, calls = c2a.make_hvp(cr3, phi, dx, basis, Z, HVP_POINT_ANGLE)
        pairs = component_history(c2a, history, basis, Z)
        curv_scale = curvature_scale_from_pairs(pairs)
        print(f"NK_PRECONDITIONER_USABLE_PAIRS={len(pairs)}", flush=True)
        print(f"NK_SECANT_CURVATURE_SCALE={curv_scale:.15e}", flush=True)

        def mvec(x):
            return lbfgs_inverse_vector(x, pairs, Z, c2a)

        M = LinearOperator((ndof, ndof), matvec=mvec, dtype=float) if pairs else None
        rhs = -gvec
        inner_rtol = min(MINRES_RTOL_MAX, max(MINRES_RTOL_MIN, 0.5*math.sqrt(max(rms, 1e-16))))

        accepted_pack = None
        # Mild regularization first.  If the Newton direction is not descent or
        # the nonlinear residual rejects it, increase damping rather than spend
        # hundreds of first-order steps.
        damping_candidates = [0.02, 0.10, 0.50, 2.00]
        for damp_index, damp_factor in enumerate(damping_candidates):
            mu = max(1e-10, damp_factor*max(curv_scale, 1e-8))
            iter_count = {"n": 0}

            def avec(x):
                return hvp(x) + mu*c2a.project_subspace(np.asarray(x, dtype=float), Z)

            A = LinearOperator((ndof, ndof), matvec=avec, dtype=float)
            def cb(_xk):
                iter_count["n"] += 1
            delta, info = minres_compat(A, rhs, M, inner_rtol, MINRES_MAXITER, cb)
            stats["minres_iterations"] += iter_count["n"]
            if damp_index:
                stats["damping_retries"] += 1
            delta = c2a.project_subspace(np.asarray(delta, dtype=float), Z)
            direction = c2a.components_to_field(delta, basis, phi.shape)
            direction = cr3.project_tangent(phi, direction)
            gd = cr3.tangent_inner(g, direction, dx)
            dd = cr3.tangent_inner(direction, direction, dx)
            max_point = float(np.max(np.linalg.norm(direction[1:-1,1:-1,1:-1], axis=-1)))
            trust_angle = min(1.0e-2, max(2.0e-3, 0.10*rms))
            alpha0 = min(1.0, trust_angle/max(max_point, 1e-300))
            print(
                f"NK_LINEAR_SOLVE_OUTER={outer} DAMP_FACTOR={damp_factor:.6e} MU={mu:.15e} "
                f"MINRES_INFO={info} MINRES_ITERS={iter_count['n']} RTOL={inner_rtol:.9e} "
                f"G_DOT_DELTA={gd:.15e} DELTA_NORM2={dd:.15e} MAX_POINT={max_point:.15e} "
                f"TRUST_ANGLE={trust_angle:.15e} ALPHA0={alpha0:.15e}", flush=True,
            )
            if (not math.isfinite(gd)) or gd >= -1e-12*max(cr3.tangent_inner(g,g,dx), 1e-300):
                print("NK_LINEAR_DIRECTION_DESCENT=NO_RETRY_WITH_MORE_DAMPING", flush=True)
                continue
            print("NK_LINEAR_DIRECTION_DESCENT=YES", flush=True)

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
                    print(f"NK_LINESEARCH_REJECT_REASON={reason}", flush=True)
                    alpha *= 0.5
                    continue
                pack = strict_stationarity(cr3, cand, dx)
                Enew, E2n, E4n, E0n, gnew, rmsnew, gmaxnew, stationnew = pack
                # Newton is being used specifically to reduce the Euler-Lagrange
                # residual.  Do not accept a merely energy-lowering step that
                # reproduces the R-LBFGS residual spikes we are trying to avoid.
                residual_ok = bool(
                    rmsnew <= NEWTON_RESIDUAL_FACTOR*rms
                    and gmaxnew <= max(NEWTON_GMAX_GROWTH*gmax, 10.0*GRAD_MAX_TOL)
                )
                print(
                    f"NK_LINESEARCH_TRIAL_OUTER={outer} LS={ls} ALPHA={alpha:.15e} "
                    f"ENERGY={Enew:.15e} GRAD_RMS={rmsnew:.15e} GRAD_MAX={gmaxnew:.15e} "
                    f"RESIDUAL_ACCEPT={'YES' if residual_ok else 'NO'}",
                    flush=True,
                )
                if not residual_ok:
                    stats["line_rejects"] += 1
                    alpha *= 0.5
                    continue
                accepted_pack = (cand, Enew, gnew, rmsnew, gmaxnew, stationnew, direction, alpha)
                break
            if accepted_pack is not None:
                break

        stats["hvp_calls"] += calls["count"]
        if accepted_pack is None:
            print("NK_NEWTON_STEP_ACCEPTED=NO", flush=True)
            break

        cand, Enew, gnew, rmsnew, gmaxnew, stationnew, direction, alpha = accepted_pack
        old_phi = phi
        old_g = g
        old_rms = rms
        history = transport_history_after_step(cr3, cr4r, old_phi, cand, direction, alpha, old_g, gnew, history)
        state.phi = cand
        state.accepted_total += 1
        nk_total += 1
        stats["outer_accepted"] += 1
        E, g, rms, gmax, station = Enew, gnew, rmsnew, gmaxnew, stationnew
        reduction = old_rms/max(rms, 1e-300)
        t4 = cr3.topology4(state.phi, state.dx)
        deg_ok, degrees = cr3.geometric_guard(state.phi, cr2, True)
        angle = cr3.max_neighbor_angle(state.phi)
        print(
            f"NK_NEWTON_STEP_ACCEPTED=YES OUTER={outer} ALPHA={alpha:.15e} "
            f"RMS_REDUCTION_FACTOR={reduction:.15e} ENERGY={E:.15e} "
            f"GRAD_RMS={rms:.15e} GRAD_MAX={gmax:.15e} TOPOLOGY4={t4:.15e} "
            f"GEOMETRIC_DEGREES={','.join(str(x) for x in degrees)} "
            f"MAX_NEIGHBOR_ANGLE={angle:.15e}", flush=True,
        )
        if not deg_ok:
            raise RuntimeError("Accepted Newton step lost geometric B=7")
        save_checkpoint(state, history, E, rms, gmax, nk_total)

    return state, history, E, g, rms, gmax, station, nk_total, stats


def main() -> None:
    """Execute the targeted N=73 Newton-Krylov stationarity repair."""
    print("=== 023C2AQS2R — N73 RIEMANNIAN NEWTON-KRYLOV STATIONARITY CLOSURE ===", flush=True)

    print("\n=== A — FAIL-CLOSED UPSTREAM AUDIT ===", flush=True)
    for path, expected in ((QS2_SOURCE, EXPECTED_QS2_SHA256), (C2A_SOURCE, EXPECTED_C2A_SHA256)):
        require(path)
        actual = sha256(path)
        print(f"{path.name}_SHA256={actual}", flush=True)
        if actual != expected:
            raise RuntimeError(f"Upstream source hash mismatch: {path.name}")
    print("UPSTREAM_023C2AQS2_C2A_AUDIT=PASS", flush=True)

    qs2 = load_module("c2aqs2r_qs2", QS2_SOURCE)
    c2a = load_module("c2aqs2r_c2a", C2A_SOURCE)
    c2ar = qs2.load_module("c2aqs2r_c2ar", qs2.C2AR_SOURCE)
    c2aqs = qs2.load_module("c2aqs2r_c2aqs", qs2.C2AQS_SOURCE)
    cr2 = c2ar.load_module("c2aqs2r_cr2", c2ar.CR2_SOURCE)
    cr3 = c2ar.load_module("c2aqs2r_cr3", c2ar.CR3_SOURCE)
    cr4r = c2ar.load_module("c2aqs2r_cr4r", c2ar.CR4R_SOURCE)

    print("\n=== B — LOAD N73 STATE ===", flush=True)
    state, history, source, discarded, norm_err, nk_total = load_state(qs2, cr3, cr4r)
    E0, _a, _b, _c, g0, rms0, gmax0, station0 = strict_stationarity(cr3, state.phi, state.dx)
    deg_ok0, deg0 = cr3.geometric_guard(state.phi, cr2, True)
    print(f"NK_START_SOURCE={source.relative_to(ROOT)}", flush=True)
    print(f"NK_START_ACCEPTED_TOTAL={state.accepted_total}", flush=True)
    print(f"NK_START_NEWTON_ACCEPTED_TOTAL={nk_total}", flush=True)
    print(f"NK_START_HISTORY_LENGTH={len(history)}", flush=True)
    print(f"NK_START_HISTORY_DISCARDED={discarded}", flush=True)
    print(f"NK_START_NORM_MAXERR={norm_err:.15e}", flush=True)
    print(f"NK_START_ENERGY={E0:.15e}", flush=True)
    print(f"NK_START_GRAD_RMS={rms0:.15e}", flush=True)
    print(f"NK_START_GRAD_MAX={gmax0:.15e}", flush=True)
    print("NK_START_STRICT_STATIONARITY=" + ("PASS" if station0 else "FAIL"), flush=True)
    print(f"NK_START_TOPOLOGY4={cr3.topology4(state.phi,state.dx):.15e}", flush=True)
    print("NK_START_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in deg0), flush=True)
    if not deg_ok0:
        raise RuntimeError("Starting N73 field failed geometric B=7")

    if station0:
        E, g, rms, gmax, station = E0, g0, rms0, gmax0, station0
        stats = {"outer_attempted":0,"outer_accepted":0,"hvp_calls":0,"minres_iterations":0,"damping_retries":0,"line_rejects":0}
    else:
        print("\n=== C — MATRIX-FREE RIEMANNIAN NEWTON-KRYLOV ===", flush=True)
        state, history, E, g, rms, gmax, station, nk_total, stats = newton_krylov_slice(
            qs2, c2a, cr2, cr3, cr4r, state, history, nk_total
        )

    print("\n=== D — END-OF-SLICE AUDIT ===", flush=True)
    t4 = cr3.topology4(state.phi, state.dx)
    deg_ok, degrees = cr3.geometric_guard(state.phi, cr2, True)
    angle = cr3.max_neighbor_angle(state.phi)
    print(f"NK_OUTER_ATTEMPTED={stats['outer_attempted']}", flush=True)
    print(f"NK_OUTER_ACCEPTED={stats['outer_accepted']}", flush=True)
    print(f"NK_HVP_MATVEC_CALLS={stats['hvp_calls']}", flush=True)
    print(f"NK_MINRES_TOTAL_ITERATIONS={stats['minres_iterations']}", flush=True)
    print(f"NK_DAMPING_RETRIES={stats['damping_retries']}", flush=True)
    print(f"NK_LINESEARCH_REJECTS={stats['line_rejects']}", flush=True)
    print(f"NK_FINAL_ENERGY={E:.15e}", flush=True)
    print(f"NK_FINAL_GRAD_RMS={rms:.15e}", flush=True)
    print(f"NK_FINAL_GRAD_MAX={gmax:.15e}", flush=True)
    print("NK_FINAL_STRICT_STATIONARITY=" + ("PASS" if station else "FAIL"), flush=True)
    print(f"NK_FINAL_TOPOLOGY4={t4:.15e}", flush=True)
    print("NK_FINAL_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in degrees), flush=True)
    print(f"NK_FINAL_MAX_NEIGHBOR_ANGLE={angle:.15e}", flush=True)

    if not station:
        save_checkpoint(state, history, E, rms, gmax, nk_total)
        print("\n=== E — BOUNDED INCOMPLETE DECISION ===", flush=True)
        print("023C2AQS2R_N73_NEWTON_KRYLOV_STATIONARITY=INCOMPLETE_SHORT_SECOND_ORDER_SLICE", flush=True)
        print("N73_ACTUAL_FINE_STRICT_STATIONARITY=NOT_YET", flush=True)
        if stats["outer_accepted"] > 0:
            print("NEWTON_KRYLOV_LOCAL_ACCELERATION=SUPPORTED", flush=True)
            print("NEXT=RERUN_SAME_023C2AQS2R_FROM_NEWTON_KRYLOV_CHECKPOINT", flush=True)
        else:
            print("NEWTON_KRYLOV_LOCAL_ACCELERATION=NOT_ESTABLISHED", flush=True)
            print("NEXT=RESIDUAL_MODE_AND_PRECONDITIONER_DIAGNOSTIC_DO_NOT_RETURN_TO_LONG_BLIND_RLBFGS", flush=True)
        print("N73_CONTINUOUS_FORCE=NOT_RUN_BEFORE_STATIONARITY", flush=True)
        print("FULL_PHYSICAL_HESSIAN=DEFERRED_OPERATIONAL_FORCE_AND_FINE_FIELD_UNRESOLVED", flush=True)
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR_NOT_A_PROBABILITY", flush=True)
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED", flush=True)
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
        return

    print("\n=== E — STRICT N73 PHYSICAL FIELD AUDIT ===", flush=True)
    diag = cr3.continuum_local_diagnostics(state.phi, state.axis, state.dx, cr2)
    print(f"NK_N73_STATIONARY_CONTINUUM_ENERGY={diag.energy_continuum:.15e}", flush=True)
    print(f"NK_N73_STATIONARY_ACTIVE_TOTAL={diag.active_total:.15e}", flush=True)
    print(f"NK_N73_STATIONARY_ACTIVE_TO_ENERGY={diag.active_to_energy:.15e}", flush=True)
    print(f"NK_N73_STATIONARY_MIN_ACTIVE_FRACTION={diag.min_active_fraction:.15e}", flush=True)
    print(f"NK_N73_STATIONARY_MIN_DEC_SCALED_MARGIN={diag.min_dec_scaled_margin:.15e}", flush=True)
    print(f"NK_N73_STATIONARY_MAX_ACTIVE_TRACE_SCALED={diag.max_active_trace_scaled:.15e}", flush=True)
    print(f"NK_N73_STATIONARY_ENERGY_CENTROID_NORM={diag.energy_centroid_norm:.15e}", flush=True)
    physical_gate = bool(
        deg_ok and diag.active_total > 0.0 and diag.min_active_fraction <= -1.0e-2
        and diag.min_dec_scaled_margin >= -1.0e-9
        and diag.max_active_trace_scaled <= 1.0e-10
        and angle <= MAX_NEIGHBOR_ANGLE
    )
    print("NK_N73_STATIONARY_PHYSICAL_FIELD_GATE=" + ("PASS" if physical_gate else "FAIL"), flush=True)
    save_final(state, E, rms, gmax, diag, nk_total)

    if not physical_gate:
        print("023C2AQS2R_N73_NEWTON_KRYLOV_STATIONARITY=RED_STRICT_N73_PHYSICAL_FIELD_GATE", flush=True)
        print("FULL_PHYSICAL_HESSIAN=DEFERRED_BY_FINE_FIELD_PHYSICAL_FALSIFIER", flush=True)
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_PENDING_RERANK", flush=True)
        print("NEXT=PRESERVE_NEGATIVE_RESULT_AND_RERANK_023_BRANCH", flush=True)
        return

    print("\n=== F — CONDITIONAL CONTINUOUS-FORCE CERTIFICATE ===", flush=True)
    n65ref = qs2.load_n65_force_reference()
    aqr = c2aqs.load_module("c2aqs2r_aqr", c2aqs.AQR_SOURCE)
    aqr.validate_analytic_formulae()
    print("NK_N73_ANALYTIC_KERNEL_VALIDATION=PASS", flush=True)
    force = qs2.continuous_force_gate(c2aqs, aqr, cr3, state.phi, state.axis, state.dx, n65ref)

    print("\n=== G — 023C2AQS2R DECISION ===", flush=True)
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

    print(f"023C2AQS2R_N73_NEWTON_KRYLOV_STATIONARITY={decision}", flush=True)
    print("N73_ACTUAL_FINE_STRICT_STATIONARITY=PASS", flush=True)
    print(f"FULL_PHYSICAL_HESSIAN={hessian}", flush=True)
    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR_NOT_A_PROBABILITY", flush=True)
    print(f"NEXT={next_step}", flush=True)
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED_UNTIL_023C_COMPLETE", flush=True)
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
    print("NEW_PHYSICS_DISCOVERY=NO", flush=True)
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023C2AQS2R_RIEMANNIAN_NEWTON_KRYLOV_STATIONARITY_REPAIR", flush=True)


if __name__ == "__main__":
    main()
