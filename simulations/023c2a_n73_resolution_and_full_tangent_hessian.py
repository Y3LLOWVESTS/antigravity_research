#!/usr/bin/env python3
"""023C2A — N=73 resolution closure + full-tangent N=65 Hessian gate.

PURPOSE
-------
Advance the strongest surviving false-core B=7 Skyrmion branch from the
single-resolution stationary result of 023CR4R toward the complete 023C
unrestricted-stability milestone.

023CR4R established, at N=65 on the checkerboard-free fourth-order Cartesian
action, a strictly stationary unrestricted field with:

    |B_geometric| = 7,
    positive total active mass,
    a negative enclosed active-mass region,
    pointwise DEC,
    the active-trace identity,
    and outward finite-payload linearized-GR response in 320 directions.

The weakest outward payload direction at that stationary state is positive but
small relative to the mean field.  Therefore the highest-information next
experiment is resolution-first: before spending heavily on the Hessian, verify
that a finer stationary N=73 companion preserves the operational sign and that
the complete 320-direction force field converges.

Only if that gate is green does this file launch the full-tangent N=65 Hessian
calculation.  This ordering is a computational stop rule, not a change in the
physics or promotion criteria.

SCIENTIFIC QUESTIONS
--------------------
1. Does the strictly stationary unrestricted B=7 state persist on a finer N=73
   Cartesian lattice with the same action, topology, stress-energy properties,
   and outward finite-payload response?
2. Does the N=65 stationary point have a significant negative mode in the
   COMPLETE three-component tangent space at every interior lattice site?

OPERATIONAL OBSERVABLE
----------------------
For the full unrestricted active source

    S(x) = rho + p1 + p2 + p3 = 2(e4 - V),

the uniform spherical payload average uses the exact shell-theorem kernel

    <a>(c) = integral S(x') (x'-c) / max(|x'-c|^3, Rp^3) d^3x'.

The radial projection must remain positive for all 320 deterministic
Fibonacci-sphere orientations at BOTH N=65 and N=73.  In addition to sign, the
full 320-value radial vector must converge under refinement.

PHYSICAL MODEL
--------------
The static SU(2) Skyrme field is

    phi = (sigma, pi1, pi2, pi3),
    phi . phi = 1,

with fixed true-vacuum boundary phi=(1,0,0,0) and

    E = integral (e2 + e4 + V) d^3x,

    e2 = sum_i |d_i phi|^2,

    e4 = sum_(i<j) [|d_i phi|^2 |d_j phi|^2
                    - (d_i phi . d_j phi)^2],

    V = m^2 (1-sigma)(1+eta sigma),

at the selected parameters

    B=7, eta=0.4, m=8.

No new stabilizer, rigidity term, symmetry restriction, or rational-map
constraint is introduced.

DISCRETE ACTION
---------------
Use exactly the 023CR3/023CR4R checkerboard-free parity-symmetrized fourth-order
one-sided action and its exact analytic gradient.  N=73 is obtained only by
interpolating the already stationary N=65 field, renormalizing onto S^3,
fixing the vacuum boundary, and re-solving the SAME discrete Euler-Lagrange
problem with R-LBFGS.

N=73 STATIONARITY / CHECKPOINTING
---------------------------------
The N=73 R-LBFGS continuation uses the unchanged strict thresholds

    gradient RMS <= 1.5e-3,
    gradient max <= 5e-2.

It writes

    results/data/023c2a_n73_rlbfgs_checkpoint.npz

and may be rerun.  The per-invocation accepted-step budget is controlled by

    AG_N73_RLBFGS_MAX_ACCEPTED

(default 40).  If N=73 is not stationary after one invocation, the script
exits INCOMPLETE before any Hessian work.  Thus no long Hessian run is wasted
on a still-moving companion field.

RESOLUTION PROMOTION GATE
-------------------------
Both N=65 and N=73 must independently satisfy the physical gate.  The pair
must also satisfy predeclared companion-grid tolerances:

    continuum-energy relative change <= 1.5e-2,
    min-active-fraction absolute change <= 3.0e-3,
    |topology4_N73 - topology4_N65| <= 1.0e-2,
    320-direction radial L_inf difference / mean_N73 <= 1.0e-1,
    320-direction radial RMS difference / mean_N73 <= 4.0e-2,
    every radial payload direction positive at both resolutions.

These tolerances are not a substitute for later domain-size convergence.

FULL PHYSICAL HESSIAN
---------------------
At the stationary N=65 field, form an orthonormal three-vector tangent basis at
every interior site.  This gives

    3 (N-2)^3

physical lattice degrees of freedom and contains arbitrary local, angular,
radial, shear, twist, clustering, and fission-like infinitesimal directions.
No rational-map or point-group restriction remains.

The covariant Hessian-vector product is evaluated matrix-free by:

1. moving along the product-S^3 exponential map in +/-v directions;
2. evaluating the exact Riemannian gradient at both endpoints;
3. exactly parallel-transporting those gradients back to the base tangent
   space site by site;
4. taking the centered difference.

This avoids the connection error that can arise from comparing tangent vectors
living at different S^3 points.

EXACT AND APPROXIMATE ZERO MODES
--------------------------------
The potential depends on sigma only, so global SO(3) rotations of the pion
triplet are exact internal symmetries of the DISCRETE action.  Their three
infinitesimal modes are explicitly projected out of the eigensolver.

Continuum translations and spatial rotations are also reported as candidate
zero-mode subspaces, but they are NOT projected out automatically because the
finite Cartesian box and lattice break those symmetries slightly.  An
individual numerical mode may be classified as symmetry-like only if it is
near zero and has strong overlap with that candidate subspace.  This prevents
an arbitrary projection from hiding a real negative mode.

HESSIAN VALIDATION
------------------
Before the eigensolve:
- perform a bilinear self-adjointness check;
- repeat one Hessian-vector product at three finite-difference point angles to
  verify step-size convergence;
- perform deterministic smooth random Rayleigh probes as a cheap negative-mode
  falsifier.

The lowest eigenmodes are then computed with scipy.sparse.linalg.eigsh over the
FULL tangent operator after exact-isorotation projection.  The numerically
lowest physical mode is independently checked by direct symmetric energy
curvature at several finite amplitudes.

A negative full-space mode confirmed by direct energy curvature is a physical
stability falsifier.  A nonconverged eigensolver is numerical incompleteness,
not stability evidence.

PROMOTION / STOP RULE
---------------------
This file can establish only:

    N73_STATIONARY_COMPANION_AND_FORCE_CONVERGENCE
    N65_FULL_TANGENT_HESSIAN_SINGLE_RESOLUTION

It does NOT by itself complete 023C because the project still requires an
explicit finite-amplitude binary fission/deformation challenge and Hessian
resolution confirmation before 023D.

If the N=73 stationary payload develops any inward orientation, stop before the
Hessian and inspect refinement/domain behavior.  If a robust negative Hessian
mode is found and independently confirmed, preserve it as a stability
falsification and do not rescue the branch with arbitrary stabilizers.

If both stages are green, the next action is a short 023C2B gate containing:
- N=73 confirmation of the lowest N=65 physical Hessian mode / spectral gap;
- explicit B1+B6, B2+B5, B3+B4 finite-amplitude fission/deformation challenges;
- domain-size spot convergence.
A green 023C2B would complete the approximately-72-percent unrestricted-field
milestone and authorize 023D validated weak-gravity Einstein-Skyrme
continuation.

APPROXIMATION LEVEL / CLAIM BOUNDARIES
--------------------------------------
Flat-spacetime classical Skyrme matter; gravity is a static linearized-GR
operational readout.  This file does not establish a nonlinear Einstein-Skyrme
solution, practical energy scaling, a real material, an experiment, a device,
or discovery of new physics.

RELATED FILES
-------------
simulations/023cr2_high_order_geometric_topology_preflight.py
simulations/023cr3_geometric_degree_guarded_unrestricted_relaxation.py
simulations/023cr3r_stationarity_continuation_and_optimizer_crosscheck.py
simulations/023cr4r_rlbfgs_stationarity_closure_gradient_audit_repair.py
results/data/023cr4r_strict_stationary_b7_n65.npz

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023C2A_N73_RESOLUTION_AND_FULL_TANGENT_HESSIAN
"""

from __future__ import annotations

import hashlib
import importlib.util
from concurrent.futures import ThreadPoolExecutor
import math
import os
from pathlib import Path
import sys
from typing import Iterable

import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.sparse.linalg import ArpackNoConvergence, LinearOperator, eigsh


ROOT = Path(__file__).resolve().parents[1]
CR2_SOURCE = ROOT / "simulations/023cr2_high_order_geometric_topology_preflight.py"
CR3_SOURCE = ROOT / "simulations/023cr3_geometric_degree_guarded_unrestricted_relaxation.py"
CR3R_SOURCE = ROOT / "simulations/023cr3r_stationarity_continuation_and_optimizer_crosscheck.py"
CR4R_SOURCE = ROOT / "simulations/023cr4r_rlbfgs_stationarity_closure_gradient_audit_repair.py"
CR4R_LOG = ROOT / "results/logs/023cr4r_rlbfgs_stationarity_closure_gradient_audit_repair.log"
N65_ARTIFACT = ROOT / "results/data/023cr4r_strict_stationary_b7_n65.npz"

EXPECTED_CR2_SHA256 = "6affc28547b7849140f1eacf6992c9541ea9ba9a7c306e69121ca60ef76ad1db"
EXPECTED_CR3_SHA256 = "350868726af644d1a8bb2970b559c92e1febc4ea261f409ab38c1dca64ac97da"
EXPECTED_CR3R_SHA256 = "545770186fca2b319e37e3882a4f280eb40093a11fe59f95f40ab6eaefab9306"
EXPECTED_CR4R_SHA256 = "eda4d558c258a45e986b7fe6f9fe47e5a371349380f8df509612c66bde515cb3"
EXPECTED_CR4R_MARKERS = (
    "023CR4R_GRADIENT_AUDIT_AND_RLBFGS_STATIONARITY_CLOSURE=GREEN_STRICT_STATIONARY_N65",
    "FINAL_STRICT_STATIONARITY=PASS",
    "FINAL_GEOMETRIC_DEGREES=-7,-7,-7",
    "STATIONARY_PHYSICAL_GATE=PASS",
    "STATIONARY_DENSE_FINITE_PAYLOAD_OUTWARD=PASS",
    "FULL_PHYSICAL_HESSIAN=AUTHORIZED_NOT_YET_ESTABLISHED",
)

B = 7
ETA = 0.40
MASS = 8.0
N65 = 65
N73 = 73
PAYLOAD_CENTER = 3.870161274564900e-01
PAYLOAD_RADIUS = 1.675735743205162e-02
DENSE_ORIENTATION_N = 320

GRAD_RMS_TOL = 1.5e-3
GRAD_MAX_TOL = 5.0e-2
MAX_NEIGHBOR_ANGLE = 0.70
MAX_TOPOLOGY_RELERR = 3.0e-2
MIN_NEGATIVE_ACTIVE_FRACTION = 1.0e-2
MIN_DEC_SCALED_MARGIN = -2.0e-8
MAX_ACTIVE_TRACE_SCALED = 2.0e-12

MAX_PAIR_ENERGY_RELCHANGE = 1.5e-2
MAX_PAIR_ACTIVE_FRACTION_ABSCHANGE = 3.0e-3
MAX_PAIR_TOPOLOGY_ABSCHANGE = 1.0e-2
MAX_PAIR_PAYLOAD_LINF_OVER_MEAN = 1.0e-1
MAX_PAIR_PAYLOAD_RMS_OVER_MEAN = 4.0e-2

N73_CHECKPOINT = ROOT / "results/data/023c2a_n73_rlbfgs_checkpoint.npz"
N73_FINAL_ARTIFACT = ROOT / "results/data/023c2a_strict_stationary_b7_n73.npz"
N73_MAX_ACCEPTED = max(1, int(os.environ.get("AG_N73_RLBFGS_MAX_ACCEPTED", "40")))

HESSIAN_K = max(8, int(os.environ.get("AG_HESSIAN_K", "12")))
HESSIAN_NCV = max(HESSIAN_K + 4, int(os.environ.get("AG_HESSIAN_NCV", "28")))
HESSIAN_TOL = float(os.environ.get("AG_HESSIAN_TOL", "3e-3"))
HESSIAN_MAXITER = max(20, int(os.environ.get("AG_HESSIAN_MAXITER", "100")))
HESSIAN_POINT_ANGLE = float(os.environ.get("AG_HESSIAN_POINT_ANGLE", "2e-4"))
MAX_HESSIAN_BILINEAR_ASYMMETRY = 5.0e-3
MAX_HVP_STEP_RELCHANGE = 1.5e-2
HESSIAN_SIGNIFICANT_NEGATIVE_REL = 2.5e-3
HESSIAN_POSITIVE_GAP_REL = 2.5e-3
SYMMETRY_ZERO_REL = 5.0e-3
SYMMETRY_OVERLAP_MIN = 0.70
DIRECT_CURVATURE_NEGATIVE_REL = 2.5e-3

RNG = np.random.default_rng(23032026)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def require(path: Path) -> None:
    if not path.exists():
        raise RuntimeError(f"Required file missing: {path}")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def relerr(a: float, b: float) -> float:
    return abs(float(a) - float(b)) / max(abs(float(a)), abs(float(b)), 1.0e-300)


def strict_stationarity(cr3, phi: np.ndarray, dx: float):
    E, _, _, _, g = cr3.riemannian_gradient_density(phi, dx)
    rms, gmax = cr3.gradient_norms(g)
    return float(E), g, float(rms), float(gmax), bool(rms <= GRAD_RMS_TOL and gmax <= GRAD_MAX_TOL)


def load_n65(cr3, cr2):
    require(N65_ARTIFACT)
    with np.load(N65_ARTIFACT, allow_pickle=False) as d:
        phi = np.asarray(d["phi"], dtype=float)
        axis = np.asarray(d["axis"], dtype=float)
        dx = float(d["dx"])
        b = int(d["B"])
        eta = float(d["eta"])
        mass = float(d["mass"])
        source = str(d["source"])
    if phi.shape != (N65, N65, N65, 4):
        raise RuntimeError(f"Unexpected N65 artifact shape {phi.shape}")
    if b != B or abs(eta - ETA) > 1e-14 or abs(mass - MASS) > 1e-14:
        raise RuntimeError("N65 artifact physical parameters do not match selected candidate")
    if source != "023CR4R_N65":
        raise RuntimeError(f"Unexpected N65 source tag: {source}")
    if abs(float(np.max(np.abs(np.linalg.norm(phi, axis=-1) - 1.0)))) > 5e-10:
        raise RuntimeError("N65 artifact violates S3 norm")
    diag = cr3.continuum_local_diagnostics(phi, axis, dx, cr2)
    E, _g, rms, gmax, station = strict_stationarity(cr3, phi, dx)
    return phi, axis, dx, diag, E, rms, gmax, station


def load_or_interpolate_n73(cr3, cr3r, cr4r, phi65, axis65):
    if N73_CHECKPOINT.exists():
        with np.load(N73_CHECKPOINT, allow_pickle=False) as d:
            phi = np.asarray(d["phi"], dtype=float)
            axis = np.asarray(d["axis"], dtype=float)
            dx = float(d["dx"])
            accepted = int(d["accepted_total"])
        source = "023C2A_N73_CHECKPOINT"
    else:
        phi, axis, dx = cr3r.interpolate_field(phi65, axis65, N73, cr3)
        accepted = 0
        source = "INTERPOLATED_FROM_023CR4R_N65"
    if phi.shape != (N73, N73, N73, 4):
        raise RuntimeError(f"Unexpected N73 shape {phi.shape}")
    state = cr4r.State(phi=phi, axis=axis, dx=dx, accepted_total=accepted)
    return state, source


def payload_raw(cr3, phi: np.ndarray, axis: np.ndarray, dx: float):
    """Return the full 320-direction payload array and its audited summary.

    This deliberately evaluates the expensive source/payload convolution only
    once per field.  The returned `PayloadDiagnostics` object is built from the
    same raw array and is passed directly into the inherited physical gate, so
    the resolution test and the promotion summary cannot silently disagree.
    """
    qx, qy, qz = cr3.central4_derivatives(phi, dx)
    _, _, _, _, _, _, _, e4 = cr3.metric_terms(qx, qy, qz)
    center_field = phi[2:-2, 2:-2, 2:-2]
    V = cr3.potential_sigma(center_field[..., 0])
    active = 2.0 * (e4 - V)
    coords = axis[2:-2]
    X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")
    xyz = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    weight = active.ravel() * dx**3
    vectors = cr3.fibonacci_sphere(DENSE_ORIENTATION_N)
    centers = PAYLOAD_CENTER * vectors
    avg = cr3.analytic_uniform_sphere_payload_average(xyz, weight, centers, PAYLOAD_RADIUS)
    radial = np.sum(avg * vectors, axis=1)
    transverse = np.linalg.norm(avg - radial[:, None] * vectors, axis=1)
    worst = int(np.argmin(radial))
    positive = radial > 0.0
    ratio = np.divide(
        transverse,
        np.maximum(radial, 1.0e-300),
        out=np.full_like(transverse, np.inf),
        where=positive,
    )
    payload = cr3.PayloadDiagnostics(
        min_radial=float(np.min(radial)),
        max_radial=float(np.max(radial)),
        mean_radial=float(np.mean(radial)),
        max_transverse=float(np.max(transverse)),
        max_transverse_over_radial=float(np.max(ratio)),
        worst_orientation=np.asarray(vectors[worst], dtype=float),
        all_outward=bool(np.all(positive)),
    )
    return vectors, radial, transverse, payload


def physical_checks(cr3r, cr3, diag, payload, radial: np.ndarray):
    """Apply the inherited physical gate to the already-computed payload data."""
    physical, checks = cr3r.physical_gate(cr3, diag, payload)
    return bool(physical and np.all(radial > 0.0)), checks


def tangent_basis_householder(phi: np.ndarray) -> np.ndarray:
    p = phi[1:-1, 1:-1, 1:-1].reshape(-1, 4)
    n = len(p)
    basis = np.zeros((n, 4, 3), dtype=float)
    e0 = np.zeros((n, 4), dtype=float)
    e0[:, 0] = 1.0
    v = e0 - p
    v2 = np.sum(v * v, axis=1)
    regular = v2 > 1.0e-14
    for j in range(3):
        ej = np.zeros((n, 4), dtype=float)
        ej[:, j + 1] = 1.0
        col = ej.copy()
        if np.any(regular):
            coeff = 2.0 * v[regular, j + 1] / v2[regular]
            col[regular] -= coeff[:, None] * v[regular]
        basis[:, :, j] = col
    for j in range(3):
        norm = np.linalg.norm(basis[:, :, j], axis=1)
        basis[:, :, j] /= np.maximum(norm[:, None], 1.0e-300)
    return basis


def components_to_field(u: np.ndarray, basis: np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
    coeff = u.reshape(basis.shape[0], 3)
    vint = np.einsum("naj,nj->na", basis, coeff)
    out = np.zeros(shape, dtype=float)
    out[1:-1, 1:-1, 1:-1] = vint.reshape(shape[0]-2, shape[1]-2, shape[2]-2, 4)
    return out


def field_to_components(v: np.ndarray, basis: np.ndarray) -> np.ndarray:
    vint = v[1:-1, 1:-1, 1:-1].reshape(-1, 4)
    return np.einsum("naj,na->nj", basis, vint).ravel()


def orthonormal_columns(vectors: Iterable[np.ndarray], tol: float = 1e-11) -> np.ndarray:
    cols = []
    for vec in vectors:
        q = np.asarray(vec, dtype=float).copy()
        for z in cols:
            q -= z * float(np.dot(z, q))
        n = float(np.linalg.norm(q))
        if n > tol:
            q /= n
            # second MGS pass for large vectors
            for z in cols:
                q -= z * float(np.dot(z, q))
            n2 = float(np.linalg.norm(q))
            if n2 > tol:
                cols.append(q / n2)
    if not cols:
        return np.empty((len(next(iter(vectors), np.zeros(0))), 0))
    return np.column_stack(cols)


def isorotation_modes(phi: np.ndarray, basis: np.ndarray) -> list[np.ndarray]:
    p = phi[1:-1, 1:-1, 1:-1].reshape(-1, 4)
    pi = p[:, 1:]
    modes = []
    for axis in np.eye(3):
        ambient = np.zeros_like(p)
        ambient[:, 1:] = np.cross(np.broadcast_to(axis, pi.shape), pi)
        coeff = np.einsum("naj,na->nj", basis, ambient).ravel()
        if np.linalg.norm(coeff) > 1e-12:
            modes.append(coeff)
    return modes


def spatial_symmetry_candidates(cr3, phi: np.ndarray, axis: np.ndarray, basis: np.ndarray) -> np.ndarray:
    # These are diagnostic continuum symmetry candidates only.  They are not
    # removed from the Hessian because the finite lattice/box breaks them.
    grads = []
    for component in range(4):
        gx, gy, gz = np.gradient(phi[..., component], axis, axis, axis, edge_order=2)
        grads.append((gx, gy, gz))
    dphi = []
    for spatial in range(3):
        arr = np.stack([grads[a][spatial] for a in range(4)], axis=-1)
        arr = cr3.project_tangent(phi, arr)
        arr[0]=0; arr[-1]=0; arr[:,0]=0; arr[:,-1]=0; arr[:,:,0]=0; arr[:,:,-1]=0
        dphi.append(arr)

    candidates = []
    candidates.extend(field_to_components(v, basis) for v in dphi)
    X, Y, Z = np.meshgrid(axis, axis, axis, indexing="ij")
    coords = (X, Y, Z)
    # infinitesimal spatial rotation: delta phi = -(omega x x).grad phi
    for k in range(3):
        eps = np.zeros((3,3))
        if k == 0:
            xi = (np.zeros_like(X), -Z, Y)
        elif k == 1:
            xi = (Z, np.zeros_like(X), -X)
        else:
            xi = (-Y, X, np.zeros_like(X))
        ambient = -(xi[0][...,None]*dphi[0] + xi[1][...,None]*dphi[1] + xi[2][...,None]*dphi[2])
        ambient = cr3.project_tangent(phi, ambient)
        candidates.append(field_to_components(ambient, basis))
    return orthonormal_columns(candidates)


def project_subspace(u: np.ndarray, Z: np.ndarray) -> np.ndarray:
    if Z.size == 0:
        return np.asarray(u, dtype=float)
    return np.asarray(u, dtype=float) - Z @ (Z.T @ np.asarray(u, dtype=float))


def exp_endpoint_and_tangent(cr3, phi: np.ndarray, v: np.ndarray, alpha: float):
    endpoint = cr3.exp_map_update(phi, v, alpha)
    n = np.linalg.norm(v, axis=-1)
    mask = n > 1e-14
    u = np.zeros_like(v)
    u[mask] = v[mask] / n[mask,None]
    theta = alpha * n
    c = np.cos(theta)
    s = np.sin(theta)
    tangent = -s[...,None]*phi + c[...,None]*u
    tangent[~mask] = 0.0
    return endpoint, u, tangent


def reverse_parallel_transport(cr3, base: np.ndarray, endpoint: np.ndarray, u: np.ndarray, tangent: np.ndarray, w: np.ndarray):
    b = np.sum(w * tangent, axis=-1)
    out = w + b[...,None] * (u - tangent)
    out = cr3.project_tangent(base, out)
    out[0]=0; out[-1]=0; out[:,0]=0; out[:,-1]=0; out[:,:,0]=0; out[:,:,-1]=0
    return out


def make_hvp(cr3, phi: np.ndarray, dx: float, basis: np.ndarray, Z: np.ndarray, point_angle: float):
    shape = phi.shape
    calls = {"count": 0}

    def hvp(uvec: np.ndarray) -> np.ndarray:
        uvec = project_subspace(np.asarray(uvec, dtype=float), Z)
        v = components_to_field(uvec, basis, shape)
        maxp = float(np.max(np.linalg.norm(v[1:-1,1:-1,1:-1], axis=-1)))
        if maxp <= 1e-300:
            return np.zeros_like(uvec)
        alpha = point_angle / maxp
        plus, up, tp = exp_endpoint_and_tangent(cr3, phi, v, alpha)
        minus, um, tm = exp_endpoint_and_tangent(cr3, phi, v, -alpha)
        # The +/- endpoint gradients are independent.  Evaluating them on two
        # worker threads lets NumPy's compiled kernels use two CPU cores without
        # changing the operator or floating-point algebra of either endpoint.
        with ThreadPoolExecutor(max_workers=2) as pool:
            fp = pool.submit(cr3.riemannian_gradient_density, plus, dx)
            fm = pool.submit(cr3.riemannian_gradient_density, minus, dx)
            gp = fp.result()[4]
            gm = fm.result()[4]
        gp0 = reverse_parallel_transport(cr3, phi, plus, up, tp, gp)
        gm0 = reverse_parallel_transport(cr3, phi, minus, um, tm, gm)
        hfield = (gp0 - gm0) / (2.0 * alpha)
        out = field_to_components(hfield, basis)
        calls["count"] += 1
        return project_subspace(out, Z)

    return hvp, calls


def smooth_random_vector(cr3, phi: np.ndarray, basis: np.ndarray, Z: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    ambient = rng.normal(size=phi.shape)
    for a in range(4):
        ambient[...,a] = gaussian_filter(ambient[...,a], sigma=2.0, mode="nearest")
    ambient = cr3.project_tangent(phi, ambient)
    ambient[0]=0; ambient[-1]=0; ambient[:,0]=0; ambient[:,-1]=0; ambient[:,:,0]=0; ambient[:,:,-1]=0
    q = project_subspace(field_to_components(ambient, basis), Z)
    n = np.linalg.norm(q)
    return q / max(n, 1e-300)


def direct_curvatures(cr3, phi: np.ndarray, dx: float, basis: np.ndarray, mode: np.ndarray):
    v = components_to_field(mode, basis, phi.shape)
    maxp = float(np.max(np.linalg.norm(v[1:-1,1:-1,1:-1], axis=-1)))
    E0 = cr3.high_order_energy_gradient(phi, dx, False)[0]
    values = []
    for point_angle in (5e-4, 1e-3, 2e-3):
        alpha = point_angle / max(maxp, 1e-300)
        pp = cr3.exp_map_update(phi, v, alpha)
        pm = cr3.exp_map_update(phi, v, -alpha)
        Ep = cr3.high_order_energy_gradient(pp, dx, False)[0]
        Em = cr3.high_order_energy_gradient(pm, dx, False)[0]
        ray = (Ep + Em - 2.0*E0) / (alpha*alpha*dx**3)
        values.append(float(ray))
    return values


def hessian_gate(cr3, phi: np.ndarray, axis: np.ndarray, dx: float):
    print("\n=== H — FULL-TANGENT N=65 HESSIAN ===", flush=True)
    basis = tangent_basis_householder(phi)
    ndof = 3 * (phi.shape[0]-2)**3
    Z = orthonormal_columns(isorotation_modes(phi, basis))
    spatial_Z = spatial_symmetry_candidates(cr3, phi, axis, basis)
    print(f"FULL_TANGENT_HESSIAN_DOF={ndof}", flush=True)
    print(f"EXACT_ISOROTATION_ZERO_MODE_COUNT={Z.shape[1]}", flush=True)
    print(f"SPATIAL_SYMMETRY_CANDIDATE_COUNT={spatial_Z.shape[1]}", flush=True)

    # Step-size convergence on one fixed full-space smooth probe.
    probe = smooth_random_vector(cr3, phi, basis, Z, 230321)
    hvals = []
    for pa in (1e-4, HESSIAN_POINT_ANGLE, 4e-4):
        hvp_i, _ = make_hvp(cr3, phi, dx, basis, Z, pa)
        hv = hvp_i(probe)
        hvals.append(hv)
        rq = float(np.dot(probe, hv))
        print(f"HVP_STEP_POINT_ANGLE={pa:.15e} RAYLEIGH={rq:.15e}", flush=True)
    step_rel_01 = np.linalg.norm(hvals[0]-hvals[1]) / max(np.linalg.norm(hvals[1]),1e-300)
    step_rel_12 = np.linalg.norm(hvals[1]-hvals[2]) / max(np.linalg.norm(hvals[1]),1e-300)
    step_pass = min(step_rel_01, step_rel_12) <= MAX_HVP_STEP_RELCHANGE
    print(f"HVP_STEP_RELCHANGE_SMALL_PRIMARY={step_rel_01:.15e}", flush=True)
    print(f"HVP_STEP_RELCHANGE_PRIMARY_LARGE={step_rel_12:.15e}", flush=True)
    print("HESSIAN_FINITE_DIFFERENCE_STEP_CONVERGENCE=" + ("PASS" if step_pass else "FAIL"), flush=True)

    hvp, calls = make_hvp(cr3, phi, dx, basis, Z, HESSIAN_POINT_ANGLE)

    # Bilinear symmetry checks.
    asym = []
    for pair in range(2):
        u = smooth_random_vector(cr3, phi, basis, Z, 9100+2*pair)
        v = smooth_random_vector(cr3, phi, basis, Z, 9101+2*pair)
        Hu = hvp(u)
        Hv = hvp(v)
        a = float(np.dot(u, Hv))
        b = float(np.dot(Hu, v))
        err = abs(a-b)/max(abs(a),abs(b),1e-12)
        asym.append(err)
        print(f"HESSIAN_BILINEAR_PAIR={pair+1} UV={a:.15e} VU={b:.15e} RELASYM={err:.15e}", flush=True)
    max_asym = max(asym)
    selfadj = max_asym <= MAX_HESSIAN_BILINEAR_ASYMMETRY
    print(f"HESSIAN_MAX_BILINEAR_ASYMMETRY={max_asym:.15e}", flush=True)
    print("FULL_TANGENT_HESSIAN_SELF_ADJOINTNESS=" + ("PASS" if selfadj else "FAIL"), flush=True)

    # Cheap deterministic full-space Rayleigh probes before ARPACK.
    probe_rq = []
    for i in range(6):
        q = smooth_random_vector(cr3, phi, basis, Z, 12000+i)
        Hq = hvp(q)
        rq = float(np.dot(q,Hq))
        probe_rq.append(rq)
        print(f"HESSIAN_RANDOM_RAYLEIGH_{i+1}={rq:.15e}", flush=True)
    print(f"HESSIAN_RANDOM_RAYLEIGH_MIN={min(probe_rq):.15e}", flush=True)

    op = LinearOperator((ndof, ndof), matvec=hvp, dtype=float)
    v0 = smooth_random_vector(cr3, phi, basis, Z, 230322)
    print(
        f"HESSIAN_EIGENSOLVE_START=YES K={HESSIAN_K} NCV={HESSIAN_NCV} "
        f"TOL={HESSIAN_TOL:.3e} MAXITER={HESSIAN_MAXITER}",
        flush=True,
    )
    converged = True
    try:
        vals, vecs = eigsh(
            op,
            k=min(HESSIAN_K, ndof-2),
            which="SA",
            v0=v0,
            ncv=min(HESSIAN_NCV, ndof-1),
            tol=HESSIAN_TOL,
            maxiter=HESSIAN_MAXITER,
        )
    except ArpackNoConvergence as exc:
        converged = False
        vals = np.asarray(exc.eigenvalues if exc.eigenvalues is not None else [], dtype=float)
        vecs = np.asarray(exc.eigenvectors if exc.eigenvectors is not None else np.empty((ndof,0)), dtype=float)
    if vals.size:
        order = np.argsort(vals)
        vals = vals[order]
        vecs = vecs[:,order]
    print("HESSIAN_EIGENSOLVER_CONVERGED=" + ("YES" if converged else "NO"), flush=True)
    print(f"HESSIAN_MATVEC_CALLS={calls['count']}", flush=True)
    print("HESSIAN_LOWEST_EIGENVALUES=" + ",".join(f"{x:.15e}" for x in vals), flush=True)

    if vals.size < 4:
        return {
            "complete": False, "negative": False, "positive": False,
            "converged": converged, "selfadj": selfadj, "step": step_pass,
            "vals": vals, "direct": [], "physical_min": math.nan,
        }

    spectral_scale = max(float(np.percentile(np.abs(vals), 75)), 1.0e-12)
    symmetry_like = []
    overlaps = []
    for j in range(vals.size):
        ov = float(np.linalg.norm(spatial_Z.T @ vecs[:,j])) if spatial_Z.size else 0.0
        overlaps.append(ov)
        sym = bool(abs(vals[j]) <= SYMMETRY_ZERO_REL*spectral_scale and ov >= SYMMETRY_OVERLAP_MIN)
        symmetry_like.append(sym)
        print(
            f"HESSIAN_MODE_{j+1}_LAMBDA={vals[j]:.15e} "
            f"SPATIAL_SYMMETRY_SUBSPACE_OVERLAP={ov:.9e} "
            f"CLASS={'SYMMETRY_LIKE_ZERO' if sym else 'PHYSICAL_CANDIDATE'}",
            flush=True,
        )

    physical_indices = [i for i,s in enumerate(symmetry_like) if not s]
    if not physical_indices:
        return {
            "complete": False, "negative": False, "positive": False,
            "converged": converged, "selfadj": selfadj, "step": step_pass,
            "vals": vals, "direct": [], "physical_min": math.nan,
        }
    ip = min(physical_indices, key=lambda i: vals[i])
    physical_min = float(vals[ip])
    lowest_mode = vecs[:,ip]
    direct = direct_curvatures(cr3, phi, dx, basis, lowest_mode)
    print(f"HESSIAN_SPECTRAL_SCALE={spectral_scale:.15e}", flush=True)
    print(f"HESSIAN_LOWEST_PHYSICAL_MODE_INDEX={ip+1}", flush=True)
    print(f"HESSIAN_LOWEST_PHYSICAL_EIGENVALUE={physical_min:.15e}", flush=True)
    print("LOWEST_PHYSICAL_MODE_DIRECT_CURVATURE=" + ",".join(f"{x:.15e}" for x in direct), flush=True)

    significant_negative = physical_min < -HESSIAN_SIGNIFICANT_NEGATIVE_REL*spectral_scale
    direct_negative = max(direct) < -DIRECT_CURVATURE_NEGATIVE_REL*spectral_scale
    robust_negative = bool(significant_negative and direct_negative)
    positive_gap = bool(physical_min > HESSIAN_POSITIVE_GAP_REL*spectral_scale and min(direct) > 0.0)
    complete = bool(converged and selfadj and step_pass)
    print("FULL_PHYSICAL_HESSIAN_NEGATIVE_MODE=" + ("CONFIRMED" if robust_negative else "NO_CONFIRMED_SIGNIFICANT_NEGATIVE_MODE"), flush=True)
    print("LOWEST_MODE_DIRECT_CURVATURE=" + ("PASS_POSITIVE" if min(direct)>0 else ("FAIL_NEGATIVE" if max(direct)<0 else "MIXED_UNRESOLVED")), flush=True)
    if complete and positive_gap:
        hstatus = "PASS_POSITIVE_GAP_SINGLE_RESOLUTION"
    elif complete and robust_negative:
        hstatus = "FAIL_CONFIRMED_NEGATIVE_MODE"
    else:
        hstatus = "INCOMPLETE_OR_NEAR_ZERO"
    print(f"N65_FULL_PHYSICAL_HESSIAN={hstatus}", flush=True)
    return {
        "complete": complete,
        "negative": robust_negative,
        "positive": bool(complete and positive_gap),
        "converged": converged,
        "selfadj": selfadj,
        "step": step_pass,
        "vals": vals,
        "direct": direct,
        "physical_min": physical_min,
        "spectral_scale": spectral_scale,
    }


def main() -> None:
    print("=== 023C2A — N73 RESOLUTION + FULL-TANGENT N65 HESSIAN ===", flush=True)

    print("\n=== A — UPSTREAM STRICT-STATIONARY AUDIT ===", flush=True)
    for p in (CR2_SOURCE, CR3_SOURCE, CR3R_SOURCE, CR4R_SOURCE, CR4R_LOG, N65_ARTIFACT):
        require(p)
    hashes = {
        "023CR2": sha256(CR2_SOURCE),
        "023CR3": sha256(CR3_SOURCE),
        "023CR3R": sha256(CR3R_SOURCE),
        "023CR4R": sha256(CR4R_SOURCE),
    }
    expected = {
        "023CR2": EXPECTED_CR2_SHA256,
        "023CR3": EXPECTED_CR3_SHA256,
        "023CR3R": EXPECTED_CR3R_SHA256,
        "023CR4R": EXPECTED_CR4R_SHA256,
    }
    for k,v in hashes.items():
        print(f"{k}_SOURCE_SHA256={v}", flush=True)
        if v != expected[k]:
            raise RuntimeError(f"{k} source hash mismatch")
    logtext = CR4R_LOG.read_text(errors="replace")
    for marker in EXPECTED_CR4R_MARKERS:
        if marker not in logtext:
            raise RuntimeError(f"Missing upstream marker: {marker}")
    print("UPSTREAM_023CR4R_AUDIT=PASS", flush=True)

    cr2 = load_module("ag023c2a_cr2", CR2_SOURCE)
    cr3 = load_module("ag023c2a_cr3", CR3_SOURCE)
    cr3r = load_module("ag023c2a_cr3r", CR3R_SOURCE)
    cr4r = load_module("ag023c2a_cr4r", CR4R_SOURCE)

    print("\n=== B — LOAD STRICT-STATIONARY N65 FIELD ===", flush=True)
    phi65, axis65, dx65, diag65, E65d, rms65, gmax65, station65 = load_n65(cr3, cr2)
    print(f"N65_DISCRETE_ENERGY={E65d:.15e}", flush=True)
    print(f"N65_GRAD_RMS={rms65:.15e}", flush=True)
    print(f"N65_GRAD_MAX={gmax65:.15e}", flush=True)
    print("N65_STRICT_STATIONARITY=" + ("PASS" if station65 else "FAIL"), flush=True)
    print(f"N65_CONTINUUM_ENERGY={diag65.energy_continuum:.15e}", flush=True)
    print(f"N65_MIN_ACTIVE_FRACTION={diag65.min_active_fraction:.15e}", flush=True)
    print(f"N65_TOPOLOGY4={diag65.topology4:.15e}", flush=True)
    print("N65_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in diag65.geometric_degrees), flush=True)
    if not station65:
        raise RuntimeError("Upstream N65 artifact is not strictly stationary")

    print("\n=== C — N73 COMPANION INTERPOLATION / R-LBFGS ===", flush=True)
    state73, source73 = load_or_interpolate_n73(cr3, cr3r, cr4r, phi65, axis65)
    E73i, g73i, rms73i, gmax73i, station73i = strict_stationarity(cr3, state73.phi, state73.dx)
    print(f"N73_START_SOURCE={source73}", flush=True)
    print(f"N73_START_DX={state73.dx:.15e}", flush=True)
    print(f"N73_START_ENERGY={E73i:.15e}", flush=True)
    print(f"N73_START_GRAD_RMS={rms73i:.15e}", flush=True)
    print(f"N73_START_GRAD_MAX={gmax73i:.15e}", flush=True)
    print("N73_START_STRICT_STATIONARITY=" + ("PASS" if station73i else "FAIL"), flush=True)
    print(f"N73_START_TOPOLOGY4={cr3.topology4(state73.phi,state73.dx):.15e}", flush=True)
    deg73i = tuple(int(x) for x in cr2.geometric_degrees(state73.phi))
    print("N73_START_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in deg73i), flush=True)

    # Reuse the audited R-LBFGS implementation but redirect its checkpoint and
    # per-invocation work budget.  Physics/tolerances remain unchanged.
    old_checkpoint = cr4r.CHECKPOINT
    old_budget = cr4r.MAX_ACCEPTED_THIS_RUN
    old_known = np.array(cr4r.KNOWN_WORST_DIRECTION, copy=True)
    try:
        cr4r.CHECKPOINT = N73_CHECKPOINT
        cr4r.MAX_ACCEPTED_THIS_RUN = N73_MAX_ACCEPTED
        state73, E73d, g73, rms73, gmax73, station73 = cr4r.rlbfgs(cr3, cr2, state73)
    finally:
        cr4r.CHECKPOINT = old_checkpoint
        cr4r.MAX_ACCEPTED_THIS_RUN = old_budget
        cr4r.KNOWN_WORST_DIRECTION = old_known

    print(f"N73_FINAL_DISCRETE_ENERGY={E73d:.15e}", flush=True)
    print(f"N73_FINAL_GRAD_RMS={rms73:.15e}", flush=True)
    print(f"N73_FINAL_GRAD_MAX={gmax73:.15e}", flush=True)
    print("N73_FINAL_STRICT_STATIONARITY=" + ("PASS" if station73 else "FAIL"), flush=True)
    print(f"N73_CHECKPOINT={N73_CHECKPOINT.relative_to(ROOT)}", flush=True)

    if not station73:
        print("\n=== 023C2A EARLY DECISION ===", flush=True)
        print("023C2A_N73_RESOLUTION_AND_FULL_TANGENT_HESSIAN=INCOMPLETE_CONTINUE_N73_CHECKPOINT", flush=True)
        print("N73_STATIONARY_COMPANION=NOT_YET", flush=True)
        print("FULL_PHYSICAL_HESSIAN=DEFERRED_UNTIL_N73_STATIONARY", flush=True)
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR", flush=True)
        print("NEXT=RERUN_SAME_023C2A_FROM_N73_CHECKPOINT", flush=True)
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_YET_AUTHORIZED", flush=True)
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
        return

    print("\n=== D — N65/N73 PHYSICAL + PAYLOAD RESOLUTION ===", flush=True)
    diag73 = cr3.continuum_local_diagnostics(state73.phi, state73.axis, state73.dx, cr2)
    vec65, rad65, tr65, pay65 = payload_raw(cr3, phi65, axis65, dx65)
    vec73, rad73, tr73, pay73 = payload_raw(cr3, state73.phi, state73.axis, state73.dx)
    if np.max(np.abs(vec65-vec73)) > 1e-14:
        raise RuntimeError("Payload orientation sets differ")

    phys65, checks65 = physical_checks(cr3r, cr3, diag65, pay65, rad65)
    phys73, checks73 = physical_checks(cr3r, cr3, diag73, pay73, rad73)

    for label,diag,rad,pay,phys in (
        ("N65",diag65,rad65,pay65,phys65),
        ("N73",diag73,rad73,pay73,phys73),
    ):
        print(f"{label}_CONTINUUM_ENERGY={diag.energy_continuum:.15e}", flush=True)
        print(f"{label}_ACTIVE_TOTAL={diag.active_total:.15e}", flush=True)
        print(f"{label}_MIN_ACTIVE_FRACTION={diag.min_active_fraction:.15e}", flush=True)
        print(f"{label}_TOPOLOGY4={diag.topology4:.15e}", flush=True)
        print("%s_GEOMETRIC_DEGREES=%s" % (label, ",".join(str(x) for x in diag.geometric_degrees)), flush=True)
        print(f"{label}_MIN_DEC_SCALED_MARGIN={diag.min_dec_scaled_margin:.15e}", flush=True)
        print(f"{label}_MAX_ACTIVE_TRACE_SCALED={diag.max_active_trace_scaled:.15e}", flush=True)
        print(f"{label}_PAYLOAD_MIN_RADIAL={np.min(rad):.15e}", flush=True)
        print(f"{label}_PAYLOAD_MAX_RADIAL={np.max(rad):.15e}", flush=True)
        print(f"{label}_PAYLOAD_MEAN_RADIAL={np.mean(rad):.15e}", flush=True)
        print(f"{label}_DENSE_FINITE_PAYLOAD_OUTWARD=" + ("PASS" if np.all(rad>0) else "FAIL"), flush=True)
        print(f"{label}_PHYSICAL_GATE=" + ("PASS" if phys else "FAIL"), flush=True)

    diff = rad73-rad65
    mean73 = max(float(np.mean(np.abs(rad73))),1e-300)
    energy_pair = relerr(diag65.energy_continuum,diag73.energy_continuum)
    active_pair = abs(diag65.min_active_fraction-diag73.min_active_fraction)
    topology_pair = abs(abs(diag65.topology4)-abs(diag73.topology4))
    payload_linf = float(np.max(np.abs(diff))/mean73)
    payload_rms = float(np.sqrt(np.mean(diff*diff))/mean73)
    pair_pass = bool(
        phys65 and phys73
        and energy_pair <= MAX_PAIR_ENERGY_RELCHANGE
        and active_pair <= MAX_PAIR_ACTIVE_FRACTION_ABSCHANGE
        and topology_pair <= MAX_PAIR_TOPOLOGY_ABSCHANGE
        and payload_linf <= MAX_PAIR_PAYLOAD_LINF_OVER_MEAN
        and payload_rms <= MAX_PAIR_PAYLOAD_RMS_OVER_MEAN
        and np.all(rad65>0) and np.all(rad73>0)
    )
    print(f"N65_N73_ENERGY_RELCHANGE={energy_pair:.15e}", flush=True)
    print(f"N65_N73_ACTIVE_FRACTION_ABSCHANGE={active_pair:.15e}", flush=True)
    print(f"N65_N73_TOPOLOGY_ABSCHANGE={topology_pair:.15e}", flush=True)
    print(f"N65_N73_PAYLOAD_RADIAL_LINF_OVER_N73_MEAN={payload_linf:.15e}", flush=True)
    print(f"N65_N73_PAYLOAD_RADIAL_RMS_OVER_N73_MEAN={payload_rms:.15e}", flush=True)
    print("N65_N73_STATIONARY_PHYSICAL_FORCE_CONVERGENCE=" + ("PASS" if pair_pass else "FAIL"), flush=True)

    cr3r.save_artifact(N73_FINAL_ARTIFACT, state73.phi, state73.axis, state73.dx, diag73, pay73, "023C2A_N73")
    print(f"N73_STATIONARY_FIELD_ARTIFACT={N73_FINAL_ARTIFACT.relative_to(ROOT)}", flush=True)

    if not pair_pass:
        print("\n=== 023C2A EARLY DECISION ===", flush=True)
        print("023C2A_N73_RESOLUTION_AND_FULL_TANGENT_HESSIAN=GREEN_NEGATIVE_OR_INCOMPLETE_RESOLUTION_RESULT", flush=True)
        print("N73_STATIONARY_COMPANION=SUPPORTED", flush=True)
        print("N65_N73_OPERATIONAL_FORCE_CONVERGENCE=FAIL", flush=True)
        print("FULL_PHYSICAL_HESSIAN=DEFERRED_BY_CHEAPEST_FALSIFIER", flush=True)
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR", flush=True)
        print("NEXT=INSPECT_N65_N73_FORCE_DIFFERENCE_AND_DOMAIN_BEFORE_HESSIAN", flush=True)
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED", flush=True)
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
        return

    hess = hessian_gate(cr3, phi65, axis65, dx65)

    print("\n=== I — 023C2A DECISION ===", flush=True)
    if hess["negative"]:
        print("023C2A_N73_RESOLUTION_AND_FULL_TANGENT_HESSIAN=GREEN_NEGATIVE_STABILITY_RESULT", flush=True)
        print("UNRESTRICTED_CARTESIAN_3D_STABILITY=FAIL_CONFIRMED_NEGATIVE_MODE", flush=True)
        print("PHYSICAL_FALSIFICATION=YES_FULL_TANGENT_NEGATIVE_MODE", flush=True)
        print("NEXT=PRESERVE_NEGATIVE_RESULT_AND_RERANK_DO_NOT_ADD_ARBITRARY_STABILIZERS", flush=True)
    elif hess["positive"]:
        print("023C2A_N73_RESOLUTION_AND_FULL_TANGENT_HESSIAN=GREEN_POSITIVE_SINGLE_RESOLUTION_HESSIAN", flush=True)
        print("N73_STATIONARY_COMPANION_AND_FORCE_CONVERGENCE=SUPPORTED", flush=True)
        print("N65_FULL_TANGENT_HESSIAN=PASS_POSITIVE_GAP_SINGLE_RESOLUTION", flush=True)
        print("UNRESTRICTED_CARTESIAN_3D_STABILITY=NOT_YET_COMPLETE_PENDING_HESSIAN_RESOLUTION_AND_EXPLICIT_FISSION", flush=True)
        print("NEXT=023C2B_N73_HESSIAN_MODE_CONFIRMATION_BINARY_FISSION_AND_DOMAIN_CHALLENGE", flush=True)
    else:
        print("023C2A_N73_RESOLUTION_AND_FULL_TANGENT_HESSIAN=INCOMPLETE_HESSIAN_NUMERICAL_GATE", flush=True)
        print("UNRESTRICTED_CARTESIAN_3D_STABILITY=NOT_YET_RESOLVED", flush=True)
        print("NEXT=TARGETED_HESSIAN_CONVERGENCE_REPAIR_NO_PHYSICS_PROMOTION", flush=True)

    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR", flush=True)
    print("HEURISTIC_PROMOTION_FROM_023C2A=NO_HOLD_FOR_COMPLETE_023C_BUNDLE", flush=True)
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_YET_AUTHORIZED_UNTIL_023C2B_GREEN", flush=True)
    print("PRACTICAL_ENERGY_SCALING=STILL_CATASTROPHIC_IN_PURE_GR", flush=True)
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
    print("NEW_PHYSICS_DISCOVERY=NO", flush=True)
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023C2A_N73_RESOLUTION_AND_FULL_TANGENT_HESSIAN", flush=True)


if __name__ == "__main__":
    main()
