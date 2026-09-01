#!/usr/bin/env python3
"""
023C2AQR — analytic rectangular-prism + exact spherical-cap payload operator.

PURPOSE
=======
Resolve the finite-payload force-integration failure exposed by 023C2AQ with a
closed-form voxel kernel wherever the current project geometry permits it.

023C2AQ showed that the inherited midpoint source integration is not
promotion-grade when the spherical payload radius is much smaller than a
source-grid cell.  Fixed tensor Gauss orders also oscillated in sign because a
few cells straddle the payload-sphere kernel transition.

This repair removes that quadrature problem rather than increasing Gauss order.

SCIENTIFIC QUESTION
===================
For the strict-stationary N=65 field and the current N=73 continuation state,
what is the radial finite-payload acceleration along the previously weakest
orientation when the inherited piecewise-constant source voxels are integrated
analytically?

The result is a numerical-observable audit only.  It does not continue N=73,
compute the physical Hessian, establish continuum source-grid convergence, or
change the physical model.

PHYSICAL MODEL
==============
The active linearized-GR source remains

    S = rho + p_x + p_y + p_z = 2 (e4 - V).

For a uniform spherical passive payload centered at c with radius R, the exact
payload-averaged Newton kernel is

    K(q) = q / max(|q|^3, R^3),

where q = x' - c is source minus payload-center displacement.

The tested radial observable is

    A_n = integral S(x') [n . K(x'-c)] d^3x',

with positive A_n meaning outward acceleration in the existing project sign
convention.

UNITS AND NORMALIZATION
=======================
All field coordinates, payload geometry, energies, active-source values, and
acceleration coefficients in this gate are the inherited dimensionless Skyrme
normalization.  The omitted common factor multiplying the reported force is
positive, so it cannot change the outward/inward sign.  No SI conversion or
practical-energy claim is made here.

SIGN CONVENTION
===============
q = x' - c points from the payload center toward a source element.  The
project's inherited radial coefficient is positive for outward payload
acceleration.  This file reproduces the historical midpoint coefficient before
using the repaired operator, which protects against an unnoticed sign flip.

ASSUMPTIONS / APPROXIMATION LEVEL
=================================
* static flat-spacetime Skyrme matter field;
* linearized-GR active-source diagnostic only;
* passive uniform spherical payload;
* no payload backreaction;
* P0 node-dual-voxel reconstruction of the already sampled active source;
* fixed-vacuum finite Cartesian field box inherited from 023CR/023CR4R;
* exact kernel integration is distinguished from continuum source convergence.

CONSERVATION / TOPOLOGY
=======================
This observable-only file does not alter the field and therefore cannot repair
or spoil matter conservation, topology, or stationarity.  Those properties
remain whatever the audited upstream field artifacts established.  The N=73
checkpoint remains nonstationary and is diagnostic only.

PIECEWISE-CONSTANT SOURCE REPRESENTATION
========================================
As in 023C2AQ, each sampled active-source value S_j is associated with a cubic
node-dual voxel of side dx centered on its grid node.  This file exactly
integrates the payload kernel for that P0 reconstruction.  It does NOT claim
that the P0 source itself is continuum-converged.

ANALYTIC VOXEL REDUCTION
========================
First compute the ordinary point-payload field of every uniform source voxel at
c using the standard closed-form rectangular-prism gravity formula:

    P_j(c) = integral_{V_j} q/|q|^3 d^3q.

For a payload sphere wholly contained in one P0 source voxel, or wholly outside
a voxel, the payload-average correction vanishes by symmetry / harmonic mean
value.  A correction is needed only where a source-voxel face actually cuts the
payload sphere.

Write the exact finite-payload kernel as point kernel plus a compact correction:

    q/max(r^3,R^3)
      = q/r^3
        + 1_{r<R} q (1/R^3 - 1/r^3).

Therefore

    A_n
      = sum_j S_j [n.P_j(c)]
        + integral_{r<R} S_P0(c+q)
            (n.q) (1/R^3 - 1/r^3) d^3q.

For the actual N=65/N=73/N=81 grids used here, R < dx/2 and geometry auditing
shows that the payload sphere is cut by at most one grid face.  The correction
is then an EXACT spherical-cap integral.

For a plane q_a=d with |d|<R, define the upper-cap vector integral

    I_cap(d)
      = integral_{r<R, q_a>=d}
          q_a (1/R^3 - 1/r^3) d^3q.

By direct spherical integration,

    I_cap(d)
      = 2*pi * [
          -3R/8
          + |d|
          - 3 d^2/(4R)
          + d^4/(8 R^3)
        ],

for the upper cap at positive |d|.  This scalar is non-positive.  A lower cap
has the opposite vector sign.  Multiplying by the source jump across the face
and by the radial-direction component n_a gives the complete P0 payload
correction.

Thus, for the current grids, there is no numerical kernel quadrature at all:

    CLOSED_FORM_PRISM_SUM
    +
    CLOSED_FORM_SPHERICAL_CAP_CORRECTION.

LITERATURE / MATHEMATICAL ANCHORS
=================================
The homogeneous rectangular-prism gravity formula is the standard
Nagy-type closed form used in gravimetry.  The finite spherical-payload kernel
is the ordinary Newton-shell-theorem average already validated earlier in the
project.  The cap correction above is derived explicitly from that same kernel
and independently checked numerically in this run.

VALIDATION
==========
1. Audit the exact 023C2AQ source hash.
2. Reproduce its historical N65 and N73 midpoint sentinel values.
3. Validate the analytic rectangular-prism vector against independent
   high-order direct 3D Gauss quadrature on deterministic exterior boxes.
4. Validate the spherical-cap formula against independent 1D Gauss integration
   of the derived cap integral for several d/R values.
5. Audit how many grid faces cut the payload sphere.  The closed-form cap path
   is permitted only for zero or one cut face.
6. Evaluate native N65 and N73 exact-P0 forces.
7. Repeat the exact-P0 operator after diagnostic field transfers to N65/N73/N81
   grids to determine whether the enormous old midpoint sign swings collapse.

BOUNDARY CONDITIONS
===================
The source grid uses the inherited finite Cartesian domain and central-fourth
derivative interior.  Each interior active-source sample is assigned a cubic
dual voxel of side dx.  The payload lies well inside that active-source grid;
the script aborts if the payload sphere reaches its outer dual-grid boundary.

LIMITATIONS
===========
* Exactness is only with respect to the P0 voxel source representation.
* Cross-grid interpolation cannot create missing continuum information and is
  therefore diagnostic only.
* Only the previously worst payload orientation is tested in this gate.
* Dense orientations/positions, Hessian stability, fission channels, nonlinear
  Einstein backreaction, real materials, energy scaling, and a device remain
  outside this calculation.

RELATED FILES
=============
    simulations/023cr4r_rlbfgs_stationarity_closure_gradient_audit_repair.py
    simulations/023c2a_n73_resolution_and_full_tangent_hessian.py
    simulations/023c2ar_n73_persistent_rlbfgs_stationarity_sentinel.py
    simulations/023c2aq_payload_voxel_quadrature_resolution_audit.py

CLAIM BOUNDARY
==============
Even a perfectly converged P0 kernel does NOT establish continuum source-grid
convergence.  If the analytic P0 force remains sign-sensitive under source-grid
reconstruction, the next gate must integrate a higher-order continuous active
source before any Hessian or Einstein-Skyrme promotion.

The current N=73 state is not stationary and is never used here as a physical
falsification.

STOP RULE
=========
* Any failed analytic-prism or cap validation blocks interpretation.
* More than one payload-sphere-cutting grid face blocks the simple exact-cap
  formula and requires the general multi-plane correction integrator.
* If the repaired P0 force is sign-unstable under source reconstruction, stop
  spending compute on N73 stationarity/Hessian and repair source integration.
* Only after the operational force is resolved should the project return to
  N73 strict stationarity and full 3D stability.

CLAIM CLASSIFICATION
====================
PROJECT_DERIVED_023C2AQR_ANALYTIC_PRISM_EXACT_CAP_PAYLOAD_OPERATOR
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib.util
import math
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss


ROOT = Path(__file__).resolve().parents[1]
C2AQ_SOURCE = ROOT / "simulations/023c2aq_payload_voxel_quadrature_resolution_audit.py"
EXPECTED_C2AQ_SHA256 = "48d1bb68246726ba0a12bce09d08a194eb686f2ed607670a210db3411cd88002"

N65_ARTIFACT = ROOT / "results/data/023cr4r_strict_stationary_b7_n65.npz"
N73_CHECKPOINT = ROOT / "results/data/023c2ar_n73_persistent_rlbfgs_checkpoint.npz"

SYNTHETIC_GAUSS_ORDER = 22
PRISM_VALIDATION_REL_TOL = 2.0e-9
CAP_VALIDATION_ABS_TOL = 5.0e-11
MIDPOINT_REFERENCE_REL_TOL = 2.0e-9

# The project geometry is assigned from the audited upstream script in main().
PAYLOAD_CENTER = math.nan
PAYLOAD_RADIUS = math.nan
KNOWN_WORST_DIRECTION = np.array([1.0, 0.0, 0.0], dtype=float)


@dataclass
class P0Result:
    label: str
    midpoint: float
    prism_point: float
    cap_correction: float
    exact_payload: float
    positive: float
    negative: float
    l1: float
    cancellation: float
    cut_face_count: int
    cut_axis: str
    cut_distance: float


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


def atan_ratio(num: np.ndarray, den: np.ndarray) -> np.ndarray:
    """Principal arctan(num/den) used by the classical prism formula."""
    num_b, den_b = np.broadcast_arrays(np.asarray(num, float), np.asarray(den, float))
    out = np.empty_like(num_b)
    ordinary = np.abs(den_b) > 1.0e-300
    out[ordinary] = np.arctan(num_b[ordinary] / den_b[ordinary])
    singular = ~ordinary
    out[singular] = np.sign(num_b[singular]) * (0.5*np.pi)
    out[singular & (np.abs(num_b) <= 1.0e-300)] = 0.0
    return out


def coeff_log(coeff: np.ndarray, arg: np.ndarray) -> np.ndarray:
    return np.asarray(coeff, float) * np.log(np.maximum(np.asarray(arg, float), np.finfo(float).tiny))


def prism_field_many(lo: np.ndarray, hi: np.ndarray) -> np.ndarray:
    """Exact unit-density integral int_box q/|q|^3 dV for many boxes."""
    lo = np.asarray(lo, dtype=float)
    hi = np.asarray(hi, dtype=float)
    if lo.ndim == 1:
        lo = lo[None, :]
        hi = hi[None, :]
    out = np.zeros_like(lo)

    for ix in (0, 1):
        x = lo[:, 0] if ix == 0 else hi[:, 0]
        for iy in (0, 1):
            y = lo[:, 1] if iy == 0 else hi[:, 1]
            for iz in (0, 1):
                z = lo[:, 2] if iz == 0 else hi[:, 2]
                s = -1.0 if ((ix + iy + iz) & 1) else 1.0
                r = np.sqrt(x*x + y*y + z*z)

                fx = (
                    coeff_log(y, z+r)
                    + coeff_log(z, y+r)
                    - x*atan_ratio(y*z, x*r)
                )
                fy = (
                    coeff_log(z, x+r)
                    + coeff_log(x, z+r)
                    - y*atan_ratio(z*x, y*r)
                )
                fz = (
                    coeff_log(x, y+r)
                    + coeff_log(y, x+r)
                    - z*atan_ratio(x*y, z*r)
                )
                out += s*np.column_stack([fx, fy, fz])
    return out


def direct_gauss_box(lo: np.ndarray, hi: np.ndarray, order: int) -> np.ndarray:
    """Independent volume quadrature for exterior-box prism validation."""
    nodes, weights = leggauss(order)
    xyz = []
    www = []
    for a, b in zip(lo, hi):
        xyz.append(0.5*(a+b) + 0.5*(b-a)*nodes)
        www.append(0.5*(b-a)*weights)
    X, Y, Z = np.meshgrid(*xyz, indexing="ij")
    WX, WY, WZ = np.meshgrid(*www, indexing="ij")
    pts = np.stack([X, Y, Z], axis=-1)
    r = np.sqrt(np.sum(pts*pts, axis=-1))
    vals = pts / np.maximum(r[..., None]**3, 1.0e-300)
    return np.sum(vals*(WX*WY*WZ)[..., None], axis=(0, 1, 2))


def cap_integral_scalar(radius: float, abs_d: float) -> float:
    """Exact axis component of the regularization correction over an upper cap."""
    if abs_d >= radius:
        return 0.0
    d = abs(float(abs_d))
    R = float(radius)
    return 2.0*np.pi * (
        -3.0*R/8.0
        + d
        - 3.0*d*d/(4.0*R)
        + d**4/(8.0*R**3)
    )


def cap_integral_numeric(radius: float, abs_d: float, order: int = 160) -> float:
    """Independent 1D Gauss check of the analytically integrated cap formula."""
    R = float(radius)
    d = abs(float(abs_d))
    if d >= R:
        return 0.0
    mu0 = d/R
    x, w = leggauss(order)
    mu = 0.5*(1.0-mu0)*x + 0.5*(1.0+mu0)
    ww = 0.5*(1.0-mu0)*w

    # Radial antiderivative of (r^3/R^3 - 1) is r^4/(4R^3)-r.
    F_R = -3.0*R/4.0
    r0 = d/mu
    F_r0 = r0**4/(4.0*R**3) - r0
    integrand = mu*(F_R - F_r0)
    return float(2.0*np.pi*np.sum(ww*integrand))


def validate_analytic_formulae() -> None:
    print("\n=== B — ANALYTIC FORMULA VALIDATION ===", flush=True)
    boxes = (
        (np.array([0.82, -0.21, 0.31]), np.array([1.04, 0.07, 0.52])),
        (np.array([-1.31, 0.42, -0.73]), np.array([-1.08, 0.61, -0.49])),
        (np.array([0.27, 0.66, 0.91]), np.array([0.49, 0.93, 1.13])),
        (np.array([-0.74, -1.19, 0.36]), np.array([-0.51, -0.94, 0.61])),
        (np.array([1.42, -0.82, -0.31]), np.array([1.67, -0.57, -0.09])),
        (np.array([-0.48, 0.39, 1.24]), np.array([-0.23, 0.62, 1.47])),
    )
    errs = []
    for i, (lo, hi) in enumerate(boxes):
        ana = prism_field_many(lo, hi)[0]
        num = direct_gauss_box(lo, hi, SYNTHETIC_GAUSS_ORDER)
        rel = float(np.linalg.norm(ana-num) / max(np.linalg.norm(ana), np.linalg.norm(num), 1.0e-15))
        errs.append(rel)
        print(f"PRISM_VALIDATION_CASE_{i}_RELERR={rel:.15e}", flush=True)
    max_err = max(errs)
    print(f"PRISM_VALIDATION_MAX_RELERR={max_err:.15e}", flush=True)
    prism_pass = max_err <= PRISM_VALIDATION_REL_TOL
    print("ANALYTIC_PRISM_VALIDATION=" + ("PASS" if prism_pass else "FAIL"), flush=True)
    if not prism_pass:
        raise RuntimeError("Analytic prism formula failed independent quadrature validation")

    R = 0.01675735743205162
    cap_errs = []
    for frac in (0.0, 0.17, 0.41, 0.73, 0.93):
        d = frac*R
        ana = cap_integral_scalar(R, d)
        num = cap_integral_numeric(R, d, order=180)
        err = abs(ana-num)
        cap_errs.append(err)
        print(
            f"CAP_VALIDATION_D_OVER_R={frac:.6f} ANALYTIC={ana:.15e} "
            f"NUMERIC={num:.15e} ABSERR={err:.15e}",
            flush=True,
        )
    max_cap = max(cap_errs)
    print(f"CAP_VALIDATION_MAX_ABSERR={max_cap:.15e}", flush=True)
    cap_pass = max_cap <= CAP_VALIDATION_ABS_TOL
    print("ANALYTIC_CAP_VALIDATION=" + ("PASS" if cap_pass else "FAIL"), flush=True)
    if not cap_pass:
        raise RuntimeError("Analytic spherical-cap correction failed independent validation")


def nearest_dual_cell(coords: np.ndarray, x: float) -> int:
    idx = int(np.rint((x - coords[0]) / (coords[1]-coords[0])))
    return int(np.clip(idx, 0, len(coords)-1))


def payload_cut_faces(grid, center: np.ndarray) -> list[tuple[int, float, int, int]]:
    """Return (axis, signed face offset d, base_index, adjacent_index)."""
    coords = np.asarray(grid.axis[2:-2], dtype=float)
    cuts: list[tuple[int, float, int, int]] = []
    for axis in range(3):
        i0 = nearest_dual_cell(coords, float(center[axis]))
        c0 = float(coords[i0])
        lower = c0 - 0.5*grid.dx
        upper = c0 + 0.5*grid.dx
        dl = lower - center[axis]   # negative if center is inside base voxel
        du = upper - center[axis]   # positive if center is inside base voxel
        # At R<dx/2, at most one of these can cut the sphere.
        candidates = []
        if abs(dl) < PAYLOAD_RADIUS:
            candidates.append((dl, i0-1))
        if abs(du) < PAYLOAD_RADIUS:
            candidates.append((du, i0+1))
        for d, iadj in candidates:
            if iadj < 0 or iadj >= len(coords):
                raise RuntimeError("Payload sphere reaches edge of active-source dual grid")
            cuts.append((axis, float(d), i0, int(iadj)))
    return cuts


def prism_point_kernel(grid, center: np.ndarray, direction: np.ndarray, batch: int = 32768) -> np.ndarray:
    """Exact point-center prism kernel for every P0 source voxel."""
    half = 0.5*grid.dx
    out = np.empty(grid.xyz.shape[0], dtype=float)
    for start in range(0, grid.xyz.shape[0], batch):
        stop = min(start+batch, grid.xyz.shape[0])
        xyz = grid.xyz[start:stop]
        lo = xyz - half - center[None, :]
        hi = xyz + half - center[None, :]
        field = prism_field_many(lo, hi)
        out[start:stop] = field @ direction
    return out


def one_face_cap_correction(grid, center: np.ndarray, direction: np.ndarray, cut) -> tuple[np.ndarray, float, str, float]:
    """Exact per-cell radial correction for a single sphere-cutting grid face."""
    n = len(grid.axis[2:-2])
    active3 = grid.active.reshape((n, n, n))
    coords = np.asarray(grid.axis[2:-2], dtype=float)
    base = [nearest_dual_cell(coords, float(center[a])) for a in range(3)]
    corr = np.zeros_like(grid.active)

    if cut is None:
        return corr, 0.0, "NONE", math.nan

    axis, d, i0, iadj = cut
    idx_base = list(base)
    idx_adj = list(base)
    idx_base[axis] = i0
    idx_adj[axis] = iadj
    S_base = float(active3[tuple(idx_base)])
    S_adj = float(active3[tuple(idx_adj)])
    deltaS = S_adj - S_base

    # cap_integral_scalar is the +axis component for an upper cap.  A lower cap
    # has the opposite vector sign, encoded by sign(d).
    J_axis = math.copysign(1.0, d) * cap_integral_scalar(PAYLOAD_RADIUS, abs(d))
    radial_corr_total = deltaS * direction[axis] * J_axis

    # Allocate the correction to the adjacent cell for an auditable per-cell
    # contribution decomposition.  Relative to a baseline where S_base fills
    # the entire sphere, only the cap carrying S_adj-S_base contributes.
    flat_adj = np.ravel_multi_index(tuple(idx_adj), active3.shape)
    corr[flat_adj] = radial_corr_total

    axis_name = "XYZ"[axis]
    print(f"CAP_CUT_AXIS={axis_name}", flush=True)
    print(f"CAP_CUT_SIGNED_DISTANCE={d:.15e}", flush=True)
    print(f"CAP_CUT_DISTANCE_OVER_R={abs(d)/PAYLOAD_RADIUS:.15e}", flush=True)
    print(f"CAP_BASE_SOURCE={S_base:.15e}", flush=True)
    print(f"CAP_ADJACENT_SOURCE={S_adj:.15e}", flush=True)
    print(f"CAP_SOURCE_JUMP={deltaS:.15e}", flush=True)
    print(f"CAP_AXIS_KERNEL_INTEGRAL={J_axis:.15e}", flush=True)
    print(f"CAP_RADIAL_CORRECTION={radial_corr_total:.15e}", flush=True)
    return corr, radial_corr_total, axis_name, float(d)


def exact_p0_payload(grid, c2aq, label: str) -> P0Result:
    center = PAYLOAD_CENTER*KNOWN_WORST_DIRECTION
    direction = KNOWN_WORST_DIRECTION
    print(f"\n=== {label} — CLOSED-FORM P0 PAYLOAD OPERATOR ===", flush=True)
    print(f"{label}_DX={grid.dx:.15e}", flush=True)
    print(f"{label}_PAYLOAD_RADIUS_OVER_DX={PAYLOAD_RADIUS/grid.dx:.15e}", flush=True)

    _idx, q1 = c2aq.cell_integrals(grid, 1)
    midpoint_contrib = grid.active*q1
    midpoint = float(np.sum(midpoint_contrib))
    print(f"{label}_MIDPOINT_RADIAL={midpoint:.15e}", flush=True)

    point_kernel = prism_point_kernel(grid, center, direction)
    point_contrib = grid.active*point_kernel
    prism_point = float(np.sum(point_contrib))
    print(f"{label}_ANALYTIC_PRISM_POINT_RADIAL={prism_point:.15e}", flush=True)

    cuts = payload_cut_faces(grid, center)
    print(f"{label}_PAYLOAD_CUT_FACE_COUNT={len(cuts)}", flush=True)
    for k, cut in enumerate(cuts):
        print(
            f"{label}_CUT_{k}_AXIS={'XYZ'[cut[0]]} SIGNED_DISTANCE={cut[1]:.15e} "
            f"DISTANCE_OVER_R={abs(cut[1])/PAYLOAD_RADIUS:.15e}",
            flush=True,
        )
    if len(cuts) > 1:
        raise RuntimeError(
            f"{label}: payload sphere is cut by {len(cuts)} grid faces; "
            "simple exact single-cap formula is not applicable"
        )

    corr_contrib, cap_total, axis_name, cut_distance = one_face_cap_correction(
        grid, center, direction, cuts[0] if cuts else None
    )
    final_contrib = point_contrib + corr_contrib
    exact = float(np.sum(final_contrib))
    positive = float(np.sum(final_contrib[final_contrib > 0.0]))
    negative = float(np.sum(final_contrib[final_contrib < 0.0]))
    l1 = float(np.sum(np.abs(final_contrib)))
    cancellation = l1/max(abs(exact), 1.0e-300)

    print(f"{label}_EXACT_CAP_CORRECTION={cap_total:.15e}", flush=True)
    print(f"{label}_EXACT_P0_PAYLOAD_RADIAL={exact:.15e}", flush=True)
    print(f"{label}_EXACT_P0_OUTWARD_CONTRIB={positive:.15e}", flush=True)
    print(f"{label}_EXACT_P0_INWARD_CONTRIB={negative:.15e}", flush=True)
    print(f"{label}_EXACT_P0_CONTRIB_L1={l1:.15e}", flush=True)
    print(f"{label}_EXACT_P0_CANCELLATION_FACTOR={cancellation:.15e}", flush=True)
    print(f"{label}_MIDPOINT_MINUS_EXACT={midpoint-exact:.15e}", flush=True)
    print(f"{label}_MIDPOINT_SIGN_CHANGED=" + ("YES" if ((midpoint > 0.0) != (exact > 0.0)) else "NO"), flush=True)

    return P0Result(
        label=label,
        midpoint=midpoint,
        prism_point=prism_point,
        cap_correction=cap_total,
        exact_payload=exact,
        positive=positive,
        negative=negative,
        l1=l1,
        cancellation=cancellation,
        cut_face_count=len(cuts),
        cut_axis=axis_name,
        cut_distance=cut_distance,
    )


def transfer(c2aq, cr3, cr3r, phi, axis, n_new: int, label: str) -> P0Result:
    out, axis_new, dx_new = cr3r.interpolate_field(phi, axis, n_new, cr3)
    grid = c2aq.make_source_grid(cr3, label, out, axis_new, dx_new)
    return exact_p0_payload(grid, c2aq, label)


def sign_text(x: float) -> str:
    if x > 0.0:
        return "OUTWARD"
    if x < 0.0:
        return "INWARD"
    return "ZERO"


def sign_stable(values: list[float]) -> bool:
    s = [int(np.sign(x)) for x in values]
    return len(set(s)) == 1 and s[0] != 0


def main() -> None:
    print("=== 023C2AQR — ANALYTIC PRISM + EXACT CAP PAYLOAD OPERATOR ===", flush=True)

    print("\n=== A — UPSTREAM AUDIT ===", flush=True)
    require(C2AQ_SOURCE)
    actual = sha256(C2AQ_SOURCE)
    print(f"023C2AQ_SOURCE_SHA256={actual}", flush=True)
    if actual != EXPECTED_C2AQ_SHA256:
        raise RuntimeError("023C2AQ source hash mismatch")
    print("UPSTREAM_023C2AQ_AUDIT=PASS", flush=True)

    c2aq = load_module("c2aq_for_023c2aqr", C2AQ_SOURCE)
    global PAYLOAD_CENTER, PAYLOAD_RADIUS, KNOWN_WORST_DIRECTION
    PAYLOAD_CENTER = float(c2aq.PAYLOAD_CENTER)
    PAYLOAD_RADIUS = float(c2aq.PAYLOAD_RADIUS)
    KNOWN_WORST_DIRECTION = np.asarray(c2aq.KNOWN_WORST_DIRECTION, dtype=float)
    KNOWN_WORST_DIRECTION /= np.linalg.norm(KNOWN_WORST_DIRECTION)

    validate_analytic_formulae()

    cr3 = c2aq.load_module("cr3_for_023c2aqr", c2aq.CR3_SOURCE)
    cr3r = c2aq.load_module("cr3r_for_023c2aqr", c2aq.CR3R_SOURCE)

    print("\n=== C — LOAD PROJECT STATES ===", flush=True)
    phi65, axis65, dx65, meta65 = c2aq.load_field(N65_ARTIFACT, 65)
    phi73, axis73, dx73, meta73 = c2aq.load_field(N73_CHECKPOINT, 73)
    print(f"N65_SOURCE={N65_ARTIFACT.relative_to(ROOT)}", flush=True)
    print(f"N73_SOURCE={N73_CHECKPOINT.relative_to(ROOT)}", flush=True)
    print(f"N73_ACCEPTED_TOTAL={meta73['accepted_total']:.0f}", flush=True)
    print(f"PAYLOAD_CENTER_RADIUS={PAYLOAD_CENTER:.15e}", flush=True)
    print(f"PAYLOAD_RADIUS={PAYLOAD_RADIUS:.15e}", flush=True)
    print("KNOWN_WORST_DIRECTION=" + ",".join(f"{x:.15e}" for x in KNOWN_WORST_DIRECTION), flush=True)

    grid65 = c2aq.make_source_grid(cr3, "N65_NATIVE", phi65, axis65, dx65)
    grid73 = c2aq.make_source_grid(cr3, "N73_NATIVE", phi73, axis73, dx73)

    print("\n=== D — NATIVE CLOSED-FORM P0 FORCE ===", flush=True)
    n65 = exact_p0_payload(grid65, c2aq, "N65_NATIVE")
    n73 = exact_p0_payload(grid73, c2aq, "N73_NATIVE")

    e65 = abs(n65.midpoint-float(c2aq.MIDPOINT_N65_REFERENCE))/max(abs(float(c2aq.MIDPOINT_N65_REFERENCE)), 1.0)
    e73 = abs(n73.midpoint-float(c2aq.MIDPOINT_N73_REFERENCE))/max(abs(float(c2aq.MIDPOINT_N73_REFERENCE)), 1.0)
    print(f"N65_MIDPOINT_REFERENCE_RELERR={e65:.15e}", flush=True)
    print(f"N73_MIDPOINT_REFERENCE_RELERR={e73:.15e}", flush=True)
    midpoint_ok = max(e65, e73) <= MIDPOINT_REFERENCE_REL_TOL
    print("MIDPOINT_REFERENCE_REPRODUCTION=" + ("PASS" if midpoint_ok else "FAIL"), flush=True)
    if not midpoint_ok:
        raise RuntimeError("Historical midpoint sentinel reproduction failed")

    print("\n=== E — CROSS-GRID CLOSED-FORM P0 DIAGNOSTICS ===", flush=True)
    n65_on73 = transfer(c2aq, cr3, cr3r, phi65, axis65, 73, "N65_FIELD_ON_N73")
    n65_on81 = transfer(c2aq, cr3, cr3r, phi65, axis65, 81, "N65_FIELD_ON_N81")
    n73_on65 = transfer(c2aq, cr3, cr3r, phi73, axis73, 65, "N73_FIELD_ON_N65")
    n73_on81 = transfer(c2aq, cr3, cr3r, phi73, axis73, 81, "N73_FIELD_ON_N81")
    print("CROSS_GRID_TRANSFERS_USED_AS_PROMOTION_EVIDENCE=NO", flush=True)

    print("\n=== F — DECISION ===", flush=True)
    vals65 = [n65.exact_payload, n65_on73.exact_payload, n65_on81.exact_payload]
    vals73 = [n73_on65.exact_payload, n73.exact_payload, n73_on81.exact_payload]
    stable65 = sign_stable(vals65)
    stable73 = sign_stable(vals73)

    print(f"N65_EXACT_P0_SENTINEL={n65.exact_payload:.15e}", flush=True)
    print(f"N65_EXACT_P0_SENTINEL_SIGN={sign_text(n65.exact_payload)}", flush=True)
    print(f"N73_EXACT_P0_SENTINEL={n73.exact_payload:.15e}", flush=True)
    print(f"N73_EXACT_P0_SENTINEL_SIGN={sign_text(n73.exact_payload)}", flush=True)
    print("N65_EXACT_P0_TRANSFER_VALUES=" + ",".join(f"{x:.15e}" for x in vals65), flush=True)
    print("N73_EXACT_P0_TRANSFER_VALUES=" + ",".join(f"{x:.15e}" for x in vals73), flush=True)
    print("N65_TRANSFER_SIGN_STABLE_DIAGNOSTIC=" + ("YES" if stable65 else "NO"), flush=True)
    print("N73_TRANSFER_SIGN_STABLE_DIAGNOSTIC=" + ("YES" if stable73 else "NO"), flush=True)

    # The analytic kernel itself is exact at the P0 representation level once
    # all formula validation and <=1-face geometry checks pass.  The remaining
    # uncertainty is source reconstruction / continuum resolution.
    if not stable65 or not stable73:
        status = "ANALYTIC_P0_KERNEL_REPAIRED_BUT_SOURCE_GRID_SIGN_UNSTABLE"
        next_action = "023C2AQS_HIGHER_ORDER_CONTINUOUS_ACTIVE_SOURCE_FORCE_INTEGRATION"
    elif n65.exact_payload <= 0.0:
        status = "N65_MIDPOINT_OUTWARD_SIGN_NOT_PRESERVED_BY_EXACT_P0_KERNEL"
        next_action = "023C2AQS_HIGHER_ORDER_CONTINUOUS_ACTIVE_SOURCE_FORCE_INTEGRATION"
    else:
        status = "ANALYTIC_P0_KERNEL_GREEN_WITH_N65_OUTWARD_SIGN"
        next_action = "RESUME_N73_STATIONARITY_WITH_EXACT_OPERATOR_THEN_FULL_FORCE_CONVERGENCE"

    print(f"023C2AQR_ANALYTIC_PRISM_EXACT_CAP_PAYLOAD_OPERATOR={status}", flush=True)
    print("P0_KERNEL_INTEGRATION=ANALYTICALLY_RESOLVED_FOR_TESTED_GEOMETRY", flush=True)
    print("CONTINUUM_SOURCE_RESOLUTION_ESTABLISHED=NO", flush=True)
    print("N73_INTERMEDIATE_STATE_USED_AS_PHYSICAL_FALSIFICATION=NO", flush=True)
    print("FULL_PHYSICAL_HESSIAN=DEFERRED_UNTIL_OPERATIONAL_FORCE_IS_RESOLVED", flush=True)
    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT", flush=True)
    print(f"NEXT={next_action}", flush=True)
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED", flush=True)
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
    print("NEW_PHYSICS_DISCOVERY=NO", flush=True)
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023C2AQR_ANALYTIC_PRISM_EXACT_CAP_PAYLOAD_OPERATOR", flush=True)


if __name__ == "__main__":
    main()
