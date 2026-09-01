#!/usr/bin/env python3
"""
023C2AQS — continuous-field active-source finite-payload force integration.

PURPOSE
=======
Resolve the source-representation ambiguity exposed by 023C2AQR before any
further N=73 stationarity work or full tangent-space Hessian calculation.

023C2AQR analytically integrated the finite-payload Newton kernel for the
piecewise-constant (P0) reconstruction of the sampled active source.  That
removed kernel quadrature as the dominant uncertainty, but the previously
weakest N=65 payload direction remained sign-unstable under source-grid
transfer.  The exact P0 N=65 result was slightly inward and had a cancellation
factor of roughly 3e4.  Therefore the next scientific question is not another
optimizer iteration: it is whether a higher-order continuous reconstruction of
the *field* produces a numerically certified finite-payload force sign.

SCIENTIFIC QUESTION
===================
For the strict-stationary N=65 unrestricted B=7 field, what is the radial
finite-payload acceleration along the historically weakest orientation when:

1. the SU(2) field is reconstructed continuously from the Cartesian samples;
2. the continuous field is differentiated analytically;
3. the S^3 unit constraint is restored with its derivative projection included;
4. the full nonlinear active source S=2(e4-V) is rebuilt at quadrature points;
5. the regular finite-payload kernel is integrated by converged composite
   cubature;
6. independent cubic and quintic tensor-product spline reconstructions agree?

This is the cheapest decisive operational-observable gate now available.

PHYSICAL MODEL
==============
The static Skyrme field is

    phi = (sigma, pi1, pi2, pi3),   phi.phi = 1,

with

    e4 = sum_(i<j) [|d_i phi|^2 |d_j phi|^2
                    - (d_i phi . d_j phi)^2],

    V = m^2 (1-sigma) (1+eta sigma),

    S = rho + p1 + p2 + p3 = 2(e4 - V).

The selected branch remains

    B = 7,
    eta = 0.4,
    m = 8.

No stabilizer, symmetry restriction, new interaction, or altered field
parameter is introduced.

CONTINUOUS FIELD RECONSTRUCTION
===============================
For each spline representation, let u(x) be the tensor-product spline through
the four Cartesian field components.  Because component interpolation does not
preserve |u|=1 between nodes, define

    phi(x) = u(x) / |u(x)|.

If u_i = d_i u, the exact derivative of the normalized interpolant is

    d_i phi
      = [u_i - phi (phi.u_i)] / |u|.

The implementation obtains u and u_i directly from SciPy's tensor-product
regular-grid spline and then evaluates e4, V, and S from those projected
physical derivatives.  This is stronger than interpolating the already sampled
scalar source table.

PRIMARY OBSERVABLE
==================
For a uniform spherical passive payload of radius R centered at c, the exact
payload-averaged linearized-GR kernel is

    K(q) = q / max(|q|^3, R^3),

where q=x-c.  Along unit radial direction n,

    A_n = integral S(x) [n.K(x-c)] d^3x.

Positive A_n is outward in the inherited project convention.

NUMERICAL INTEGRATION
=====================
The finite-payload kernel is bounded and continuous at q=0.  Its radial first
derivative changes at |q|=R, so the small neighborhood of the payload is
integrated more aggressively than the smooth far field.

The original N=65 field cells exactly partition the finite computational box.
The run uses:

* global composite Gauss-Legendre orders 2 and 3 on far cells;
* a high-resolution composite Gauss rule on cells near the payload;
* an even finer near-payload rule for an independent local convergence check;
* optional global order 4 automatically when the cheaper estimates do not
  certify a sign;
* independent cubic and quintic field splines.

No result is promoted from a sign alone.  The sign is certified only when the
quadrature-order error, near-payload refinement error, and cubic-vs-quintic
representation spread are all small compared with the final force magnitude.

VALIDATION
==========
The run is fail-closed and requires:

1. exact 023C2AQR source hash audit;
2. 023C2AQR analytic prism/cap validation rerun;
3. strict-stationary N=65 artifact audit;
4. spline nodal reproduction at deterministic lattice nodes;
5. analytic derivative of the normalized spline checked against an independent
   fourth-order finite difference at deterministic off-grid points;
6. the composite finite-payload cubature checked on a constant-density box
   against the independent closed-form rectangular-prism field;
7. cubic/quintic and quadrature convergence of the actual N=65 force.

OPERATIONAL SIGN CERTIFICATE
============================
Define an empirical conservative error scale from:

    quadrature difference,
    near-payload refinement difference,
    cubic/quintic reconstruction difference.

The sign is called CERTIFIED only if both continuous reconstructions have the
same nonzero sign and

    min(|A_cubic|, |A_quintic|)
      > SIGN_SAFETY_FACTOR * ERROR_BOUND.

The default safety factor is 5.  This is deliberately stricter than merely
observing the same sign twice.

FALSIFIERS / STOP RULES
=======================
* Any failed upstream/hash/analytic validation blocks interpretation.
* Failed normalized-spline derivative validation blocks interpretation.
* Failed constant-source cubature validation blocks interpretation.
* If the N=65 continuous-source sign is unresolved, do not run the Hessian.
* If the N=65 sign is robustly inward, the old N=65 all-outward Cartesian
  payload claim is demoted; do not spend compute on N=73/Hessian until a
  corrected bounded payload-position/radius operating-volume gate is justified.
* If the N=65 sign is robustly outward, resume N=73 strict stationarity and use
  this continuous operator for the N=65/N=73 320-direction force-convergence
  gate before the Hessian.

INPUTS
======
simulations/023c2aqr_analytic_prism_exact_cap_payload_operator.py
results/data/023cr4r_strict_stationary_b7_n65.npz

OUTPUTS
=======
Text diagnostics and one run log.  No field artifact is modified.

UNITS / NORMALIZATION
=====================
Inherited dimensionless Skyrme normalization.  The omitted overall positive
linearized-GR factor cannot change force sign.  No SI/device-energy conversion
is performed here.

BOUNDARY CONDITIONS
===================
The continuous spline is constructed on the complete N=65 finite box including
the fixed true-vacuum outer boundary.  Cubature is confined to that same box.
The run reports outer-shell source diagnostics so boundary interpolation cannot
silently dominate the force.

CONSERVATION / STABILITY
========================
The field is not changed.  N=65 stationarity/topology/DEC remain upstream
properties.  This run neither establishes nor tests the full physical Hessian.

LIMITATIONS
===========
* Only the historically weakest payload orientation is tested.
* The continuum field is reconstructed from a finite N=65 sample; true
  field-equation resolution still requires the independently stationary N=73
  solution later.
* Cubic/quintic agreement is a strong numerical reconstruction check, not a
  mathematical proof of the continuum limit.
* Dense payload positions/orientations, fission, nonlinear Einstein-Skyrme
  backreaction, practical energy scaling, materials, experiments, and a device
  remain outside this run.

RELATED FILES
=============
simulations/023cr4r_rlbfgs_stationarity_closure_gradient_audit_repair.py
simulations/023c2a_n73_resolution_and_full_tangent_hessian.py
simulations/023c2ar_n73_persistent_rlbfgs_stationarity_sentinel.py
simulations/023c2aq_payload_voxel_quadrature_resolution_audit.py
simulations/023c2aqr_analytic_prism_exact_cap_payload_operator.py

CLAIM CLASSIFICATION
====================
PROJECT_DERIVED_023C2AQS_CONTINUOUS_FIELD_ACTIVE_SOURCE_FORCE_INTEGRATION

A green result resolves only the N=65 operational force sign for the declared
continuous reconstruction and authorizes the next resolution/stability gate.
It is not a practical antigravity device and not a new-physics discovery.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib.util
import math
import os
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import RegularGridInterpolator
from scipy.sparse.linalg import gcrotmk


ROOT = Path(__file__).resolve().parents[1]
AQR_SOURCE = ROOT / "simulations/023c2aqr_analytic_prism_exact_cap_payload_operator.py"
EXPECTED_AQR_SHA256 = "99ffe598cfa40b03d5af29cf9ec0c5d8753b549e6ed9f140e7d5393b4efb706b"
N65_ARTIFACT = ROOT / "results/data/023cr4r_strict_stationary_b7_n65.npz"

B = 7
ETA = 0.40
MASS = 8.0

FAR_CELL_BATCH_POINTS = int(os.environ.get("AG_SOURCE_FAR_BATCH_POINTS", "120000"))
NEAR_RADIUS_DX = float(os.environ.get("AG_SOURCE_NEAR_RADIUS_DX", "2.0"))
NEAR_GAUSS_ORDER = int(os.environ.get("AG_SOURCE_NEAR_GAUSS_ORDER", "4"))
NEAR_COARSE_SUBDIV = int(os.environ.get("AG_SOURCE_NEAR_COARSE_SUBDIV", "6"))
NEAR_FINE_SUBDIV = int(os.environ.get("AG_SOURCE_NEAR_FINE_SUBDIV", "10"))
SIGN_SAFETY_FACTOR = float(os.environ.get("AG_SOURCE_SIGN_SAFETY", "5.0"))
FORCE_CONST_VALIDATION_REL_TOL = float(os.environ.get("AG_SOURCE_CONST_REL_TOL", "1e-4"))
DERIVATIVE_REL_TOL = float(os.environ.get("AG_SOURCE_DERIV_REL_TOL", "3e-6"))
NODAL_REPRO_ABS_TOL = float(os.environ.get("AG_SOURCE_NODAL_ABS_TOL", "2e-8"))
HEAVY_Q4 = os.environ.get("AG_SOURCE_HEAVY_Q4", "AUTO").strip().upper()


@dataclass
class IntegralResult:
    force: float
    positive: float
    negative: float
    l1: float
    active_mass: float
    source_min: float
    source_max: float
    raw_norm_min: float
    raw_norm_max: float


@dataclass
class MethodResult:
    method: str
    far2: IntegralResult
    far3: IntegralResult
    near_coarse: IntegralResult
    near_fine: IntegralResult
    far4: IntegralResult | None
    best: IntegralResult
    quadrature_error: float
    near_error: float
    internal_error: float


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
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_n65() -> tuple[np.ndarray, np.ndarray, float]:
    require(N65_ARTIFACT)
    with np.load(N65_ARTIFACT, allow_pickle=False) as d:
        phi = np.asarray(d["phi"], dtype=float)
        axis = np.asarray(d["axis"], dtype=float)
        dx = float(d["dx"])
        b = int(round(float(d["B"]))) if "B" in d.files else B
        eta = float(d["eta"]) if "eta" in d.files else ETA
        mass = float(d["mass"]) if "mass" in d.files else MASS
    if phi.shape != (65, 65, 65, 4) or axis.shape != (65,):
        raise RuntimeError(f"Unexpected N65 artifact shape: phi={phi.shape}, axis={axis.shape}")
    if b != B or abs(eta-ETA) > 1e-14 or abs(mass-MASS) > 1e-14:
        raise RuntimeError("N65 artifact physical metadata mismatch")
    norm_err = float(np.max(np.abs(np.sum(phi*phi, axis=-1)-1.0)))
    print(f"N65_ARTIFACT_NORM_MAXERR={norm_err:.15e}", flush=True)
    if norm_err > 5e-10:
        raise RuntimeError("N65 artifact violates S3 norm")
    return phi, axis, dx


def build_interpolator(axis: np.ndarray, phi: np.ndarray, method: str) -> RegularGridInterpolator:
    """Return a strict tensor-product spline for all four field components."""
    return RegularGridInterpolator(
        (axis, axis, axis),
        phi,
        method=method,
        bounds_error=True,
        solver=gcrotmk,
        solver_args={"rtol": 2.0e-12, "atol": 0.0, "maxiter": 1000},
    )


def normalized_field(interp: RegularGridInterpolator, points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Evaluate normalized physical field and raw interpolation norm."""
    u = np.asarray(interp(points), dtype=float)
    norm = np.linalg.norm(u, axis=1)
    if np.min(norm) < 0.25:
        raise RuntimeError(f"Spline raw field approaches zero norm: min={np.min(norm)}")
    return u/norm[:, None], norm


def source_from_continuous_field(
    interp: RegularGridInterpolator,
    points: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Evaluate S=2(e4-V) from exact derivatives of the normalized spline field."""
    u = np.asarray(interp(points), dtype=float)
    ux = np.asarray(interp(points, nu=(1, 0, 0)), dtype=float)
    uy = np.asarray(interp(points, nu=(0, 1, 0)), dtype=float)
    uz = np.asarray(interp(points, nu=(0, 0, 1)), dtype=float)

    norm = np.linalg.norm(u, axis=1)
    if np.min(norm) < 0.25:
        raise RuntimeError(f"Spline raw field approaches zero norm: min={np.min(norm)}")
    phi = u/norm[:, None]

    def project(du: np.ndarray) -> np.ndarray:
        return (du - phi*np.sum(phi*du, axis=1)[:, None])/norm[:, None]

    qx = project(ux)
    qy = project(uy)
    qz = project(uz)

    gxx = np.sum(qx*qx, axis=1)
    gyy = np.sum(qy*qy, axis=1)
    gzz = np.sum(qz*qz, axis=1)
    gxy = np.sum(qx*qy, axis=1)
    gxz = np.sum(qx*qz, axis=1)
    gyz = np.sum(qy*qz, axis=1)
    e4 = (
        gxx*gyy - gxy*gxy
        + gxx*gzz - gxz*gxz
        + gyy*gzz - gyz*gyz
    )
    sigma = phi[:, 0]
    V = MASS*MASS*(1.0-sigma)*(1.0+ETA*sigma)
    active = 2.0*(e4 - V)
    return active, norm


def kernel_radial(points: np.ndarray, center: np.ndarray, direction: np.ndarray, radius: float) -> np.ndarray:
    q = points-center[None, :]
    r2 = np.sum(q*q, axis=1)
    r = np.sqrt(np.maximum(r2, 0.0))
    denom = np.where(r < radius, radius**3, np.maximum(r2*r, 1.0e-300))
    return (q@direction)/denom


def cell_lowers(axis: np.ndarray) -> np.ndarray:
    x = axis[:-1]
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    return np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])


def min_distance_to_cells(lowers: np.ndarray, dx: float, point: np.ndarray) -> np.ndarray:
    hi = lowers+dx
    below = np.maximum(lowers-point[None, :], 0.0)
    above = np.maximum(point[None, :]-hi, 0.0)
    d = below+above
    return np.sqrt(np.sum(d*d, axis=1))


def composite_gauss_offsets(dx: float, order: int, subdiv: int = 1) -> tuple[np.ndarray, np.ndarray]:
    if order < 1 or subdiv < 1:
        raise ValueError("order and subdiv must be positive")
    x, w = leggauss(order)
    subdx = dx/subdiv
    nodes_1d = []
    weights_1d = []
    for s in range(subdiv):
        lo = s*subdx
        nodes_1d.append(lo + 0.5*subdx*(x+1.0))
        weights_1d.append(0.5*subdx*w)
    a = np.concatenate(nodes_1d)
    wa = np.concatenate(weights_1d)
    X, Y, Z = np.meshgrid(a, a, a, indexing="ij")
    WX, WY, WZ = np.meshgrid(wa, wa, wa, indexing="ij")
    offsets = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    weights = (WX*WY*WZ).ravel()
    return offsets, weights


def zero_result() -> IntegralResult:
    return IntegralResult(0.0, 0.0, 0.0, 0.0, 0.0, math.inf, -math.inf, math.inf, -math.inf)


def add_results(a: IntegralResult, b: IntegralResult) -> IntegralResult:
    return IntegralResult(
        force=a.force+b.force,
        positive=a.positive+b.positive,
        negative=a.negative+b.negative,
        l1=a.l1+b.l1,
        active_mass=a.active_mass+b.active_mass,
        source_min=min(a.source_min, b.source_min),
        source_max=max(a.source_max, b.source_max),
        raw_norm_min=min(a.raw_norm_min, b.raw_norm_min),
        raw_norm_max=max(a.raw_norm_max, b.raw_norm_max),
    )


def integrate_cells_field(
    interp: RegularGridInterpolator,
    lowers: np.ndarray,
    offsets: np.ndarray,
    weights: np.ndarray,
    center: np.ndarray,
    direction: np.ndarray,
    radius: float,
    label: str,
) -> IntegralResult:
    """Integrate continuous active source times finite-payload kernel over cells."""
    if lowers.size == 0:
        return zero_result()
    n_q = offsets.shape[0]
    cells_per_batch = max(1, FAR_CELL_BATCH_POINTS//max(n_q, 1))
    total = zero_result()
    n_cells = lowers.shape[0]
    last_report = -1

    for start in range(0, n_cells, cells_per_batch):
        stop = min(start+cells_per_batch, n_cells)
        lo = lowers[start:stop]
        pts = (lo[:, None, :]+offsets[None, :, :]).reshape(-1, 3)
        w = np.broadcast_to(weights[None, :], (len(lo), n_q)).reshape(-1)
        active, raw_norm = source_from_continuous_field(interp, pts)
        k = kernel_radial(pts, center, direction, radius)
        contrib = active*k*w
        mass_contrib = active*w
        block = IntegralResult(
            force=float(np.sum(contrib)),
            positive=float(np.sum(contrib[contrib > 0.0])),
            negative=float(np.sum(contrib[contrib < 0.0])),
            l1=float(np.sum(np.abs(contrib))),
            active_mass=float(np.sum(mass_contrib)),
            source_min=float(np.min(active)),
            source_max=float(np.max(active)),
            raw_norm_min=float(np.min(raw_norm)),
            raw_norm_max=float(np.max(raw_norm)),
        )
        total = add_results(total, block)
        pct = int(100*stop/n_cells)
        if pct//20 != last_report//20:
            print(f"{label}_PROGRESS_CELLS={stop}/{n_cells} PERCENT={pct}", flush=True)
            last_report = pct
    return total


def integrate_cells_constant(
    lowers: np.ndarray,
    offsets: np.ndarray,
    weights: np.ndarray,
    center: np.ndarray,
    direction: np.ndarray,
    radius: float,
) -> float:
    if lowers.size == 0:
        return 0.0
    n_q = offsets.shape[0]
    cells_per_batch = max(1, FAR_CELL_BATCH_POINTS//max(n_q, 1))
    total = 0.0
    for start in range(0, len(lowers), cells_per_batch):
        lo = lowers[start:min(start+cells_per_batch, len(lowers))]
        pts = (lo[:, None, :]+offsets[None, :, :]).reshape(-1, 3)
        w = np.broadcast_to(weights[None, :], (len(lo), n_q)).reshape(-1)
        total += float(np.sum(kernel_radial(pts, center, direction, radius)*w))
    return total


def combine_far_near(far: IntegralResult, near: IntegralResult) -> IntegralResult:
    return add_results(far, near)


def print_integral(label: str, r: IntegralResult) -> None:
    cancellation = r.l1/max(abs(r.force), 1.0e-300)
    print(f"{label}_FORCE={r.force:.15e}", flush=True)
    print(f"{label}_OUTWARD={r.positive:.15e}", flush=True)
    print(f"{label}_INWARD={r.negative:.15e}", flush=True)
    print(f"{label}_L1={r.l1:.15e}", flush=True)
    print(f"{label}_CANCELLATION_FACTOR={cancellation:.15e}", flush=True)
    print(f"{label}_ACTIVE_MASS={r.active_mass:.15e}", flush=True)
    print(f"{label}_SOURCE_MIN={r.source_min:.15e}", flush=True)
    print(f"{label}_SOURCE_MAX={r.source_max:.15e}", flush=True)
    print(f"{label}_RAW_NORM_MIN={r.raw_norm_min:.15e}", flush=True)
    print(f"{label}_RAW_NORM_MAX={r.raw_norm_max:.15e}", flush=True)


def finite_difference_derivative_check(
    interp: RegularGridInterpolator,
    axis: np.ndarray,
    dx: float,
    method: str,
) -> float:
    rng = np.random.default_rng(20260831)
    pts = rng.uniform(float(axis[6]), float(axis[-7]), size=(7, 3))
    u = np.asarray(interp(pts), float)
    raw_norm = np.linalg.norm(u, axis=1)
    phi = u/raw_norm[:, None]

    errs = []
    for deriv_axis, nu in enumerate(((1, 0, 0), (0, 1, 0), (0, 0, 1))):
        du = np.asarray(interp(pts, nu=nu), float)
        analytic = (du-phi*np.sum(phi*du, axis=1)[:, None])/raw_norm[:, None]
        best = math.inf
        for scale in (2.0e-3, 1.0e-3, 5.0e-4):
            h = scale*dx
            e = np.zeros(3)
            e[deriv_axis] = h
            fpp, _ = normalized_field(interp, pts+2.0*e)
            fp, _ = normalized_field(interp, pts+e)
            fm, _ = normalized_field(interp, pts-e)
            fmm, _ = normalized_field(interp, pts-2.0*e)
            numeric = (-fpp+8.0*fp-8.0*fm+fmm)/(12.0*h)
            rel = float(np.linalg.norm(numeric-analytic)/max(np.linalg.norm(analytic), 1e-15))
            best = min(best, rel)
        errs.append(best)
        print(f"{method.upper()}_NORMALIZED_DERIV_AXIS_{deriv_axis}_BEST_RELERR={best:.15e}", flush=True)
    out = max(errs)
    print(f"{method.upper()}_NORMALIZED_DERIVATIVE_MAX_RELERR={out:.15e}", flush=True)
    print(f"{method.upper()}_NORMALIZED_DERIVATIVE_CHECK=" + ("PASS" if out <= DERIVATIVE_REL_TOL else "FAIL"), flush=True)
    return out


def nodal_reproduction_check(
    interp: RegularGridInterpolator,
    phi: np.ndarray,
    axis: np.ndarray,
    method: str,
) -> float:
    rng = np.random.default_rng(7319)
    ids = rng.integers(0, len(axis), size=(256, 3))
    pts = np.column_stack([axis[ids[:, 0]], axis[ids[:, 1]], axis[ids[:, 2]]])
    ref = phi[ids[:, 0], ids[:, 1], ids[:, 2]]
    got = np.asarray(interp(pts), float)
    err = float(np.max(np.abs(got-ref)))
    print(f"{method.upper()}_NODAL_REPRO_MAX_ABSERR={err:.15e}", flush=True)
    print(f"{method.upper()}_NODAL_REPRODUCTION=" + ("PASS" if err <= NODAL_REPRO_ABS_TOL else "FAIL"), flush=True)
    return err


def central_source_diagnostic(cr3, phi: np.ndarray, axis: np.ndarray, dx: float, interp, method: str) -> None:
    qx, qy, qz = cr3.central4_derivatives(phi, dx)
    _, _, _, _, _, _, _, e4 = cr3.metric_terms(qx, qy, qz)
    center_field = phi[2:-2, 2:-2, 2:-2]
    central = 2.0*(e4-cr3.potential_sigma(center_field[..., 0]))
    coords = axis[2:-2]
    X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")
    pts = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    spline_source, raw_norm = source_from_continuous_field(interp, pts)
    ref = central.ravel()
    l2rel = float(np.linalg.norm(spline_source-ref)/max(np.linalg.norm(ref), 1e-15))
    maxabs = float(np.max(np.abs(spline_source-ref)))
    native_mass = float(np.sum(ref)*dx**3)
    spline_node_mass = float(np.sum(spline_source)*dx**3)
    shell = central.copy()
    shell[3:-3, 3:-3, 3:-3] = 0.0
    shell_l1 = float(np.sum(np.abs(shell))*dx**3)
    total_l1 = float(np.sum(np.abs(central))*dx**3)
    print(f"{method.upper()}_SOURCE_NODE_L2_RELCHANGE={l2rel:.15e}", flush=True)
    print(f"{method.upper()}_SOURCE_NODE_MAX_ABSCHANGE={maxabs:.15e}", flush=True)
    print(f"CENTRAL4_NATIVE_ACTIVE_MASS={native_mass:.15e}", flush=True)
    print(f"{method.upper()}_SPLINE_NODE_ACTIVE_MASS={spline_node_mass:.15e}", flush=True)
    print(f"{method.upper()}_SPLINE_NODE_RAW_NORM_MIN={np.min(raw_norm):.15e}", flush=True)
    print(f"CENTRAL4_OUTER_3_SOURCE_L1_FRACTION={shell_l1/max(total_l1, 1e-300):.15e}", flush=True)


def constant_source_validation(
    aqr,
    axis: np.ndarray,
    dx: float,
    far_lowers: np.ndarray,
    near_lowers: np.ndarray,
    center: np.ndarray,
    direction: np.ndarray,
    radius: float,
    far3_offsets: np.ndarray,
    far3_weights: np.ndarray,
    near_fine_offsets: np.ndarray,
    near_fine_weights: np.ndarray,
) -> float:
    # The payload sphere is wholly inside the total box.  For constant source,
    # the finite-payload compact correction integrates to zero by odd symmetry,
    # so the exact result is the ordinary homogeneous-prism field.
    lo = np.array([axis[0], axis[0], axis[0]], float)-center
    hi = np.array([axis[-1], axis[-1], axis[-1]], float)-center
    exact_vec = aqr.prism_field_many(lo, hi)[0]
    exact = float(exact_vec@direction)
    numeric = (
        integrate_cells_constant(far_lowers, far3_offsets, far3_weights, center, direction, radius)
        + integrate_cells_constant(near_lowers, near_fine_offsets, near_fine_weights, center, direction, radius)
    )
    rel = abs(numeric-exact)/max(abs(exact), 1.0)
    print(f"CONSTANT_SOURCE_ANALYTIC_PRISM_RADIAL={exact:.15e}", flush=True)
    print(f"CONSTANT_SOURCE_CONTINUOUS_CUBATURE_RADIAL={numeric:.15e}", flush=True)
    print(f"CONSTANT_SOURCE_CUBATURE_RELERR={rel:.15e}", flush=True)
    print("CONSTANT_SOURCE_CUBATURE_VALIDATION=" + ("PASS" if rel <= FORCE_CONST_VALIDATION_REL_TOL else "FAIL"), flush=True)
    return rel


def run_method(
    method: str,
    interp: RegularGridInterpolator,
    far_lowers: np.ndarray,
    near_lowers: np.ndarray,
    offsets: dict[str, tuple[np.ndarray, np.ndarray]],
    center: np.ndarray,
    direction: np.ndarray,
    radius: float,
    use_q4: bool,
) -> MethodResult:
    tag = method.upper()
    print(f"\n=== {tag} CONTINUOUS FIELD FORCE ===", flush=True)

    far2 = integrate_cells_field(interp, far_lowers, *offsets["far2"], center, direction, radius, f"{tag}_FAR_Q2")
    far3 = integrate_cells_field(interp, far_lowers, *offsets["far3"], center, direction, radius, f"{tag}_FAR_Q3")
    near_coarse = integrate_cells_field(interp, near_lowers, *offsets["near_coarse"], center, direction, radius, f"{tag}_NEAR_COARSE")
    near_fine = integrate_cells_field(interp, near_lowers, *offsets["near_fine"], center, direction, radius, f"{tag}_NEAR_FINE")

    a2 = combine_far_near(far2, near_fine)
    a3 = combine_far_near(far3, near_fine)
    print_integral(f"{tag}_Q2_NEAR_FINE", a2)
    print_integral(f"{tag}_Q3_NEAR_FINE", a3)

    quadrature_error = abs(a3.force-a2.force)
    near_error = abs(near_fine.force-near_coarse.force)
    far4 = None
    best = a3

    if use_q4:
        far4 = integrate_cells_field(interp, far_lowers, *offsets["far4"], center, direction, radius, f"{tag}_FAR_Q4")
        a4 = combine_far_near(far4, near_fine)
        print_integral(f"{tag}_Q4_NEAR_FINE", a4)
        quadrature_error = abs(a4.force-a3.force)
        best = a4

    internal_error = quadrature_error+near_error
    print(f"{tag}_QUADRATURE_ERROR_ESTIMATE={quadrature_error:.15e}", flush=True)
    print(f"{tag}_NEAR_REFINEMENT_ERROR_ESTIMATE={near_error:.15e}", flush=True)
    print(f"{tag}_INTERNAL_ERROR_ESTIMATE={internal_error:.15e}", flush=True)
    print(f"{tag}_BEST_FORCE={best.force:.15e}", flush=True)
    return MethodResult(method, far2, far3, near_coarse, near_fine, far4, best, quadrature_error, near_error, internal_error)


def upgrade_method_q4(
    existing: MethodResult,
    interp: RegularGridInterpolator,
    far_lowers: np.ndarray,
    offsets: dict[str, tuple[np.ndarray, np.ndarray]],
    center: np.ndarray,
    direction: np.ndarray,
    radius: float,
) -> MethodResult:
    """Add only the expensive global Q4 far-field pass without repeating Q2/Q3/near work."""
    tag = existing.method.upper()
    far4 = integrate_cells_field(
        interp, far_lowers, *offsets["far4"], center, direction, radius, f"{tag}_FAR_Q4"
    )
    a4 = combine_far_near(far4, existing.near_fine)
    print_integral(f"{tag}_Q4_NEAR_FINE", a4)
    quadrature_error = abs(a4.force-existing.best.force)
    near_error = existing.near_error
    internal_error = quadrature_error+near_error
    print(f"{tag}_Q4_QUADRATURE_ERROR_ESTIMATE={quadrature_error:.15e}", flush=True)
    print(f"{tag}_Q4_INTERNAL_ERROR_ESTIMATE={internal_error:.15e}", flush=True)
    print(f"{tag}_Q4_BEST_FORCE={a4.force:.15e}", flush=True)
    return MethodResult(
        existing.method, existing.far2, existing.far3, existing.near_coarse, existing.near_fine,
        far4, a4, quadrature_error, near_error, internal_error
    )


def main() -> None:
    print("=== 023C2AQS — CONTINUOUS-FIELD ACTIVE-SOURCE FORCE INTEGRATION ===", flush=True)

    print("\n=== A — UPSTREAM AUDIT ===", flush=True)
    require(AQR_SOURCE)
    actual = sha256(AQR_SOURCE)
    print(f"023C2AQR_SOURCE_SHA256={actual}", flush=True)
    if actual != EXPECTED_AQR_SHA256:
        raise RuntimeError("023C2AQR source hash mismatch")
    print("UPSTREAM_023C2AQR_AUDIT=PASS", flush=True)
    aqr = load_module("c2aqr_for_023c2aqs", AQR_SOURCE)
    aqr.validate_analytic_formulae()
    print("UPSTREAM_ANALYTIC_KERNEL_VALIDATION=PASS", flush=True)

    c2aq = aqr.load_module("c2aq_for_023c2aqs", aqr.C2AQ_SOURCE)
    cr3 = c2aq.load_module("cr3_for_023c2aqs", c2aq.CR3_SOURCE)

    global B, ETA, MASS
    B = int(c2aq.B)
    ETA = float(c2aq.ETA)
    MASS = float(c2aq.MASS)
    payload_center = float(c2aq.PAYLOAD_CENTER)
    payload_radius = float(c2aq.PAYLOAD_RADIUS)
    direction = np.asarray(c2aq.KNOWN_WORST_DIRECTION, float)
    direction /= np.linalg.norm(direction)
    center = payload_center*direction

    print("\n=== B — LOAD STRICT-STATIONARY N65 FIELD ===", flush=True)
    phi, axis, dx = load_n65()
    if abs(dx-float(axis[1]-axis[0])) > 1e-12:
        raise RuntimeError("N65 axis/dx mismatch")
    print(f"N65_DX={dx:.15e}", flush=True)
    print(f"PAYLOAD_CENTER_RADIUS={payload_center:.15e}", flush=True)
    print(f"PAYLOAD_RADIUS={payload_radius:.15e}", flush=True)
    print(f"PAYLOAD_RADIUS_OVER_DX={payload_radius/dx:.15e}", flush=True)
    print("KNOWN_WORST_DIRECTION="+",".join(f"{x:.15e}" for x in direction), flush=True)

    print("\n=== C — CELL PARTITION / QUADRATURE PRECOMPUTE ===", flush=True)
    lowers = cell_lowers(axis)
    dmin = min_distance_to_cells(lowers, dx, center)
    near_radius = NEAR_RADIUS_DX*dx
    near_mask = dmin < near_radius
    near_lowers = lowers[near_mask]
    far_lowers = lowers[~near_mask]
    print(f"TOTAL_FIELD_CELLS={len(lowers)}", flush=True)
    print(f"NEAR_FIELD_CELLS={len(near_lowers)}", flush=True)
    print(f"FAR_FIELD_CELLS={len(far_lowers)}", flush=True)
    print(f"NEAR_RADIUS_DX={NEAR_RADIUS_DX:.8f}", flush=True)
    print(f"NEAR_COARSE_SUBDIV={NEAR_COARSE_SUBDIV}", flush=True)
    print(f"NEAR_FINE_SUBDIV={NEAR_FINE_SUBDIV}", flush=True)
    print(f"NEAR_GAUSS_ORDER={NEAR_GAUSS_ORDER}", flush=True)

    offsets = {
        "far2": composite_gauss_offsets(dx, 2, 1),
        "far3": composite_gauss_offsets(dx, 3, 1),
        "far4": composite_gauss_offsets(dx, 4, 1),
        "near_coarse": composite_gauss_offsets(dx, NEAR_GAUSS_ORDER, NEAR_COARSE_SUBDIV),
        "near_fine": composite_gauss_offsets(dx, NEAR_GAUSS_ORDER, NEAR_FINE_SUBDIV),
    }

    print("\n=== D — INDEPENDENT CONSTANT-SOURCE KERNEL/CUBATURE VALIDATION ===", flush=True)
    const_err = constant_source_validation(
        aqr, axis, dx, far_lowers, near_lowers, center, direction, payload_radius,
        *offsets["far3"], *offsets["near_fine"]
    )
    if const_err > FORCE_CONST_VALIDATION_REL_TOL:
        raise RuntimeError("Continuous force cubature failed constant-source analytic validation")

    print("\n=== E — BUILD / VALIDATE CONTINUOUS FIELD SPLINES ===", flush=True)
    interps: dict[str, RegularGridInterpolator] = {}
    for method in ("cubic", "quintic"):
        print(f"BUILDING_{method.upper()}_TENSOR_SPLINE=START", flush=True)
        interp = build_interpolator(axis, phi, method)
        interps[method] = interp
        print(f"BUILDING_{method.upper()}_TENSOR_SPLINE=DONE", flush=True)
        nodal_err = nodal_reproduction_check(interp, phi, axis, method)
        deriv_err = finite_difference_derivative_check(interp, axis, dx, method)
        if nodal_err > NODAL_REPRO_ABS_TOL or deriv_err > DERIVATIVE_REL_TOL:
            raise RuntimeError(f"{method} continuous field validation failed")
        central_source_diagnostic(cr3, phi, axis, dx, interp, method)

    print("\n=== F — CHEAP CONTINUOUS FORCE PASS ===", flush=True)
    cubic0 = run_method("cubic", interps["cubic"], far_lowers, near_lowers, offsets, center, direction, payload_radius, use_q4=False)
    quintic0 = run_method("quintic", interps["quintic"], far_lowers, near_lowers, offsets, center, direction, payload_radius, use_q4=False)

    prelim_spread = abs(cubic0.best.force-quintic0.best.force)
    prelim_bound = max(cubic0.internal_error, quintic0.internal_error, prelim_spread)
    prelim_margin = min(abs(cubic0.best.force), abs(quintic0.best.force))
    prelim_same_sign = np.sign(cubic0.best.force) == np.sign(quintic0.best.force) and cubic0.best.force != 0.0
    prelim_certified = bool(prelim_same_sign and prelim_margin > SIGN_SAFETY_FACTOR*prelim_bound)
    print(f"PRELIM_CUBIC_QUINTIC_SPREAD={prelim_spread:.15e}", flush=True)
    print(f"PRELIM_ERROR_BOUND={prelim_bound:.15e}", flush=True)
    print(f"PRELIM_SIGN_MARGIN={prelim_margin:.15e}", flush=True)
    print("PRELIM_SIGN_CERTIFIED="+("YES" if prelim_certified else "NO"), flush=True)

    if HEAVY_Q4 == "YES":
        do_q4 = True
    elif HEAVY_Q4 == "NO":
        do_q4 = False
    else:
        do_q4 = not prelim_certified
    print("GLOBAL_Q4_TRIGGERED="+("YES" if do_q4 else "NO"), flush=True)

    if do_q4:
        print("\n=== G — HEAVY GLOBAL Q4 RESOLUTION PASS ===", flush=True)
        cubic = upgrade_method_q4(cubic0, interps["cubic"], far_lowers, offsets, center, direction, payload_radius)
        quintic = upgrade_method_q4(quintic0, interps["quintic"], far_lowers, offsets, center, direction, payload_radius)
    else:
        cubic, quintic = cubic0, quintic0

    print("\n=== H — CONTINUOUS-SOURCE SIGN CERTIFICATE ===", flush=True)
    representation_spread = abs(cubic.best.force-quintic.best.force)
    error_bound = max(cubic.internal_error, quintic.internal_error, representation_spread)
    margin = min(abs(cubic.best.force), abs(quintic.best.force))
    same_sign = np.sign(cubic.best.force) == np.sign(quintic.best.force) and cubic.best.force != 0.0
    certified = bool(same_sign and margin > SIGN_SAFETY_FACTOR*error_bound)
    sign = "OUTWARD" if (certified and cubic.best.force > 0.0) else ("INWARD" if (certified and cubic.best.force < 0.0) else "UNRESOLVED")

    print(f"CUBIC_CONTINUOUS_BEST_FORCE={cubic.best.force:.15e}", flush=True)
    print(f"QUINTIC_CONTINUOUS_BEST_FORCE={quintic.best.force:.15e}", flush=True)
    print(f"CONTINUOUS_REPRESENTATION_SPREAD={representation_spread:.15e}", flush=True)
    print(f"CONTINUOUS_FORCE_ERROR_BOUND={error_bound:.15e}", flush=True)
    print(f"CONTINUOUS_FORCE_SIGN_MARGIN={margin:.15e}", flush=True)
    print(f"CONTINUOUS_FORCE_SIGN_SAFETY_FACTOR={SIGN_SAFETY_FACTOR:.8f}", flush=True)
    print("CUBIC_QUINTIC_SAME_SIGN="+("YES" if same_sign else "NO"), flush=True)
    print("N65_CONTINUOUS_FORCE_SIGN_CERTIFIED="+("YES" if certified else "NO"), flush=True)
    print(f"N65_CONTINUOUS_FORCE_SIGN={sign}", flush=True)
    best_l1 = max(cubic.best.l1, quintic.best.l1)
    best_mag = 0.5*(abs(cubic.best.force)+abs(quintic.best.force))
    print(f"N65_CONTINUOUS_FORCE_CANCELLATION_FACTOR={best_l1/max(best_mag,1e-300):.15e}", flush=True)

    print("\n=== I — 023C2AQS DECISION ===", flush=True)
    if not certified:
        decision = "INCOMPLETE_CONTINUOUS_SOURCE_SIGN_NOT_CERTIFIED"
        next_step = "023C2AQS2_ACTUAL_FINE_FIELD_RESOLUTION_OR_STRONGER_ADAPTIVE_CUBATURE"
        hessian = "DEFERRED_OPERATIONAL_FORCE_UNRESOLVED"
    elif sign == "OUTWARD":
        decision = "GREEN_N65_CONTINUOUS_SOURCE_OUTWARD_SENTINEL"
        next_step = "RESUME_N73_STRICT_STATIONARITY_THEN_320_DIRECTION_CONTINUOUS_FORCE_CONVERGENCE"
        hessian = "AUTHORIZED_ONLY_AFTER_STATIONARY_N73_FORCE_CONVERGENCE"
    else:
        decision = "RED_N65_CONTINUOUS_SOURCE_SENTINEL_INWARD"
        next_step = "023C2AQT_BOUNDED_CORRECTED_PAYLOAD_OPERATING_VOLUME_SCAN_OR_BRANCH_RERANK"
        hessian = "DEFERRED_BY_OPERATIONAL_FORCE_FALSIFIER_AT_DECLARED_PAYLOAD_GEOMETRY"

    print(f"023C2AQS_CONTINUOUS_FIELD_ACTIVE_SOURCE_FORCE_INTEGRATION={decision}", flush=True)
    print(f"FULL_PHYSICAL_HESSIAN={hessian}", flush=True)
    print("N65_STRICT_STATIONARY_FIELD=RETAINED", flush=True)
    print("N65_TOPOLOGY_AND_MATTER_DIAGNOSTICS=RETAINED", flush=True)
    print("OLD_MIDPOINT_PAYLOAD_SIGN=PROMOTION_STATUS_WITHDRAWN_PENDING_OR_SUPERSEDED_BY_CONTINUOUS_OPERATOR", flush=True)
    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR_NOT_A_PROBABILITY", flush=True)
    print(f"NEXT={next_step}", flush=True)
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED_UNTIL_023C_COMPLETE", flush=True)
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
    print("NEW_PHYSICS_DISCOVERY=NO", flush=True)
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023C2AQS_CONTINUOUS_FIELD_ACTIVE_SOURCE_FORCE_INTEGRATION", flush=True)


if __name__ == "__main__":
    main()
