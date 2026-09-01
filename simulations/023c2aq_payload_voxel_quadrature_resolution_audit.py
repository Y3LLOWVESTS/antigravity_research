#!/usr/bin/env python3
"""
023C2AQ — payload-voxel quadrature and cross-grid force-sign audit.

PURPOSE
=======
Diagnose the unexpectedly large change in the previously weakest finite-payload
radial acceleration between the strict stationary N=65 field and the relaxing
N=73 companion BEFORE spending more computation on stationarity or a full
million-DOF Hessian.

SCIENTIFIC QUESTION
===================
Is the observed sign change

    N65 strict stationary sentinel  > 0,
    current N73 sentinel            < 0,

primarily caused by genuine field-state/resolution evolution, or by the source
quadrature used to integrate the sharply varying finite-payload Newton kernel?

The payload radius is much smaller than one field-grid cell.  The inherited
observable evaluates

    a_r = integral S(x) K_r(x; x_P, R_P) d^3x

with node-centered midpoint weights S_i dx^3.  Although the uniform spherical
payload kernel itself is analytically regularized, midpoint source quadrature
can still be inaccurate when R_P << dx and the payload lies inside the source
region.  This file therefore cell-integrates the SAME analytic payload kernel
over each source voxel using deterministic Gauss-Legendre quadrature.

PHYSICAL MODEL
==============
No field theory, source definition, payload geometry, sign convention, or
promotion threshold is changed.  The active source remains

    S = 2 (e4 - V),

with e4 reconstructed from the inherited fourth-order continuum derivative and

    V = m^2 (1-sigma) (1+eta sigma).

Positive radial result means outward acceleration in the existing project
convention.

NUMERICAL METHOD
================
For each central4 source node x_i, associate a cubic voxel of side dx centered
on x_i and hold S_i constant inside that voxel.  The radial kernel integral of
that voxel is evaluated by tensor-product Gauss-Legendre quadrature.

The q=1 result is exactly the inherited midpoint rule.  We then compute q=2,
q=3, and q=4 globally.  To resolve the sub-cell payload scale efficiently, the
q=3 result is repaired in a small near-payload region by replacing the q=3
voxel integrals with q=6, q=10, and q=14 integrals.  Only source cells whose
centers lie within a configurable number of grid spacings of the payload are
refined, so high-order quadrature is spent only where the kernel changes most
rapidly.

The calculation is performed independently for:

1. the strict stationary N=65 field from 023CR4R;
2. the latest N=73 field from 023C2AR (stationarity is NOT assumed);
3. N65 interpolated to N=73, using midpoint only;
4. current N73 interpolated to N=65, using midpoint only.

The transfer cases separate field-state evolution from grid/readout effects.

VALIDATION
==========
* Audit all upstream source hashes.
* Reproduce the previously printed midpoint sentinel for N=65.
* Reproduce the latest N=73 midpoint sentinel from its checkpoint metadata to
  tight floating-point tolerance.
* Report total active source, signed outward/inward force contributions,
  absolute-contribution cancellation factor, and near-payload contribution.
* Require no claim from an unconverged Gauss-order sequence.

INTERPRETATION / CLAIM BOUNDARY
===============================
This is a NUMERICAL OBSERVABLE audit, not a new physics result.

If high-order voxel integration reverses the sign of the midpoint result, the
old midpoint force sign is not promotion-grade and the payload observable must
be repaired before any Hessian or Einstein-Skyrme promotion.

If N65 and N73 retain opposite signs under converged voxel integration, the
force difference is much more likely to reflect the field/resolution branch
rather than the payload quadrature alone.  N73 must still reach strict
stationarity before that difference is a physical resolution falsification.

This file does not establish stability, nonlinear Einstein-Skyrme gravity,
practical energy scaling, a material, an experiment, or a device.

INPUTS
======
results/data/023cr4r_strict_stationary_b7_n65.npz
results/data/023c2ar_n73_persistent_rlbfgs_checkpoint.npz

OUTPUTS
=======
Text diagnostics only.  No field state is modified.

RUN CONTROL
===========
AG_PAYLOAD_QUAD_BATCH        source-voxel batch size (default 4096)
AG_PAYLOAD_NEAR_DX           near-region radius in grid spacings (default 2.5)

CLAIM CLASSIFICATION
====================
PROJECT_DERIVED_023C2AQ_PAYLOAD_VOXEL_QUADRATURE_RESOLUTION_AUDIT
"""

from __future__ import annotations

import hashlib
import importlib.util
import math
import os
from pathlib import Path
import sys
from dataclasses import dataclass

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CR3_SOURCE = ROOT / "simulations/023cr3_geometric_degree_guarded_unrestricted_relaxation.py"
CR3R_SOURCE = ROOT / "simulations/023cr3r_stationarity_continuation_and_optimizer_crosscheck.py"
CR4R_SOURCE = ROOT / "simulations/023cr4r_rlbfgs_stationarity_closure_gradient_audit_repair.py"
C2A_SOURCE = ROOT / "simulations/023c2a_n73_resolution_and_full_tangent_hessian.py"
C2AR_SOURCE = ROOT / "simulations/023c2ar_n73_persistent_rlbfgs_stationarity_sentinel.py"

EXPECTED_CR3_SHA256 = "350868726af644d1a8bb2970b559c92e1febc4ea261f409ab38c1dca64ac97da"
EXPECTED_CR3R_SHA256 = "545770186fca2b319e37e3882a4f280eb40093a11fe59f95f40ab6eaefab9306"
EXPECTED_CR4R_SHA256 = "eda4d558c258a45e986b7fe6f9fe47e5a371349380f8df509612c66bde515cb3"
EXPECTED_C2A_SHA256 = "0862560521ef4088744879435c193824f75a032a2040ee3475e005ad54147a51"
EXPECTED_C2AR_SHA256 = "50ce682704f0786b49c8460a9a588f8245460db5b34a9118d85aef0a5412267a"

N65_ARTIFACT = ROOT / "results/data/023cr4r_strict_stationary_b7_n65.npz"
N73_CHECKPOINT = ROOT / "results/data/023c2ar_n73_persistent_rlbfgs_checkpoint.npz"

B = 7
ETA = 0.40
MASS = 8.0
PAYLOAD_CENTER = 3.870161274564900e-01
PAYLOAD_RADIUS = 1.675735743205162e-02
KNOWN_WORST_DIRECTION = np.array(
    [-4.543501844638e-01, 1.878880658051e-02, 8.906250000000e-01],
    dtype=float,
)
KNOWN_WORST_DIRECTION /= np.linalg.norm(KNOWN_WORST_DIRECTION)

BATCH = max(256, int(os.environ.get("AG_PAYLOAD_QUAD_BATCH", "4096")))
NEAR_DX = max(1.0, float(os.environ.get("AG_PAYLOAD_NEAR_DX", "2.5")))
GLOBAL_ORDERS = (1, 2, 3, 4)
NEAR_ORDERS = (6, 10, 14)

MIDPOINT_N65_REFERENCE = 5.601853299475295e00
MIDPOINT_N73_REFERENCE = -2.296974284514114e02
MIDPOINT_REFERENCE_REL_TOL = 2.0e-9


@dataclass
class SourceGrid:
    label: str
    phi: np.ndarray
    axis: np.ndarray
    dx: float
    xyz: np.ndarray
    active: np.ndarray
    topology4: float


@dataclass
class QuadResult:
    total: float
    positive: float
    negative: float
    l1: float
    cancellation: float
    near: float
    max_abs_cell: float


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


def load_field(path: Path, expected_n: int) -> tuple[np.ndarray, np.ndarray, float, dict[str, float]]:
    require(path)
    with np.load(path, allow_pickle=False) as d:
        phi = np.asarray(d["phi"], dtype=float)
        axis = np.asarray(d["axis"], dtype=float)
        dx = float(d["dx"])
        metadata = {
            "B": float(d["B"]) if "B" in d.files else float(B),
            "eta": float(d["eta"]) if "eta" in d.files else float(ETA),
            "mass": float(d["mass"]) if "mass" in d.files else float(MASS),
            "accepted_total": float(d["accepted_total"]) if "accepted_total" in d.files else math.nan,
        }
    if phi.shape != (expected_n, expected_n, expected_n, 4):
        raise RuntimeError(f"Unexpected field shape {phi.shape} in {path}")
    if axis.shape != (expected_n,):
        raise RuntimeError(f"Unexpected axis shape {axis.shape} in {path}")
    if int(round(metadata["B"])) != B or abs(metadata["eta"] - ETA) > 1e-14 or abs(metadata["mass"] - MASS) > 1e-14:
        raise RuntimeError(f"Field metadata mismatch in {path}: {metadata}")
    return phi, axis, dx, metadata


def make_source_grid(cr3, label: str, phi: np.ndarray, axis: np.ndarray, dx: float) -> SourceGrid:
    norm_err = float(np.max(np.abs(np.sum(phi * phi, axis=-1) - 1.0)))
    if norm_err > 5e-10:
        raise RuntimeError(f"{label} S3 norm violation {norm_err}")
    qx, qy, qz = cr3.central4_derivatives(phi, dx)
    _, _, _, _, _, _, _, e4 = cr3.metric_terms(qx, qy, qz)
    center_field = phi[2:-2, 2:-2, 2:-2]
    V = cr3.potential_sigma(center_field[..., 0])
    active3 = 2.0 * (e4 - V)
    coords = axis[2:-2]
    X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")
    xyz = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    return SourceGrid(
        label=label,
        phi=phi,
        axis=axis,
        dx=float(dx),
        xyz=xyz,
        active=active3.ravel(),
        topology4=float(cr3.topology4(phi, dx)),
    )


def radial_kernel(points: np.ndarray, center: np.ndarray, direction: np.ndarray) -> np.ndarray:
    q = points - center[None, :]
    d2 = np.sum(q * q, axis=1)
    d = np.sqrt(np.maximum(d2, 0.0))
    denom = np.where(
        d < PAYLOAD_RADIUS,
        PAYLOAD_RADIUS ** 3,
        np.maximum(d2 * d, 1.0e-300),
    )
    return (q @ direction) / denom


def gauss_rule(order: int, dx: float) -> tuple[np.ndarray, np.ndarray]:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    nodes = 0.5 * dx * nodes
    weights = 0.5 * dx * weights
    X, Y, Z = np.meshgrid(nodes, nodes, nodes, indexing="ij")
    WX, WY, WZ = np.meshgrid(weights, weights, weights, indexing="ij")
    offsets = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    w3 = (WX * WY * WZ).ravel()
    return offsets, w3


def cell_integrals(
    grid: SourceGrid,
    order: int,
    indices: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Integrate the radial payload kernel over selected source-centered voxels."""
    if indices is None:
        indices = np.arange(grid.xyz.shape[0], dtype=np.int64)
    offsets, weights = gauss_rule(order, grid.dx)
    center = PAYLOAD_CENTER * KNOWN_WORST_DIRECTION
    out = np.empty(indices.size, dtype=float)
    for start in range(0, indices.size, BATCH):
        stop = min(start + BATCH, indices.size)
        idx = indices[start:stop]
        pts = grid.xyz[idx, None, :] + offsets[None, :, :]
        flat = pts.reshape(-1, 3)
        kval = radial_kernel(flat, center, KNOWN_WORST_DIRECTION).reshape(len(idx), -1)
        out[start:stop] = kval @ weights
    return indices, out


def summarize(grid: SourceGrid, cell_kernel: np.ndarray) -> QuadResult:
    contrib = grid.active * cell_kernel
    positive = float(np.sum(contrib[contrib > 0.0]))
    negative = float(np.sum(contrib[contrib < 0.0]))
    total = float(np.sum(contrib))
    l1 = float(np.sum(np.abs(contrib)))
    cancellation = l1 / max(abs(total), 1.0e-300)
    center = PAYLOAD_CENTER * KNOWN_WORST_DIRECTION
    r = np.linalg.norm(grid.xyz - center[None, :], axis=1)
    near = float(np.sum(contrib[r <= NEAR_DX * grid.dx]))
    max_abs_cell = float(np.max(np.abs(contrib)))
    return QuadResult(total, positive, negative, l1, cancellation, near, max_abs_cell)


def print_result(label: str, scheme: str, q: QuadResult) -> None:
    print(
        f"{label}_{scheme}_RADIAL={q.total:.15e} "
        f"OUTWARD_CONTRIB={q.positive:.15e} INWARD_CONTRIB={q.negative:.15e} "
        f"CONTRIB_L1={q.l1:.15e} CANCELLATION_FACTOR={q.cancellation:.15e} "
        f"NEAR_{NEAR_DX:.2f}DX_CONTRIB={q.near:.15e} MAX_ABS_CELL={q.max_abs_cell:.15e}",
        flush=True,
    )


def audit_native(grid: SourceGrid) -> dict[str, QuadResult]:
    print(f"\n=== {grid.label} — NATIVE VOXEL QUADRATURE ===", flush=True)
    print(f"{grid.label}_DX={grid.dx:.15e}", flush=True)
    print(f"{grid.label}_PAYLOAD_RADIUS_OVER_DX={PAYLOAD_RADIUS/grid.dx:.15e}", flush=True)
    print(f"{grid.label}_TOPOLOGY4={grid.topology4:.15e}", flush=True)
    print(f"{grid.label}_ACTIVE_TOTAL_MIDPOINT={np.sum(grid.active)*grid.dx**3:.15e}", flush=True)

    results: dict[str, QuadResult] = {}
    kernels: dict[int, np.ndarray] = {}
    for order in GLOBAL_ORDERS:
        _idx, kernel = cell_integrals(grid, order)
        kernels[order] = kernel
        q = summarize(grid, kernel)
        results[f"Q{order}"] = q
        print_result(grid.label, f"Q{order}", q)

    center = PAYLOAD_CENTER * KNOWN_WORST_DIRECTION
    r = np.linalg.norm(grid.xyz - center[None, :], axis=1)
    near_idx = np.flatnonzero(r <= NEAR_DX * grid.dx)
    print(f"{grid.label}_NEAR_CELL_COUNT={near_idx.size}", flush=True)
    base = np.array(kernels[3], copy=True)
    for order in NEAR_ORDERS:
        idx, refined = cell_integrals(grid, order, near_idx)
        hybrid = np.array(base, copy=True)
        hybrid[idx] = refined
        q = summarize(grid, hybrid)
        results[f"Q3_NEAR_Q{order}"] = q
        print_result(grid.label, f"Q3_NEAR_Q{order}", q)

    q10 = results["Q3_NEAR_Q10"].total
    q14 = results["Q3_NEAR_Q14"].total
    abs_change = abs(q14 - q10)
    rel_change = abs_change / max(abs(q14), abs(q10), 1.0)
    same_sign = (q10 > 0.0) == (q14 > 0.0)
    converged = bool(same_sign and rel_change <= 1.0e-2)
    midpoint_same_sign = (results["Q1"].total > 0.0) == (q14 > 0.0)
    print(f"{grid.label}_NEAR_Q10_Q14_ABSCHANGE={abs_change:.15e}", flush=True)
    print(f"{grid.label}_NEAR_Q10_Q14_RELCHANGE={rel_change:.15e}", flush=True)
    print(f"{grid.label}_VOXEL_QUADRATURE_CONVERGED=" + ("PASS" if converged else "FAIL"), flush=True)
    print(f"{grid.label}_MIDPOINT_AND_REFINED_SIGN_AGREE=" + ("YES" if midpoint_same_sign else "NO"), flush=True)
    return results


def midpoint_transfer(cr3, cr3r, label: str, phi: np.ndarray, axis: np.ndarray, n_new: int) -> tuple[float, float]:
    out, axis_new, dx_new = cr3r.interpolate_field(phi, axis, n_new, cr3)
    grid = make_source_grid(cr3, label, out, axis_new, dx_new)
    _idx, kernel = cell_integrals(grid, 1)
    q = summarize(grid, kernel)
    print_result(label, "Q1", q)
    print(f"{label}_TOPOLOGY4={grid.topology4:.15e}", flush=True)
    return q.total, grid.topology4


def relative_match(value: float, reference: float) -> float:
    return abs(value-reference) / max(abs(value), abs(reference), 1.0)


def main() -> None:
    print("=== 023C2AQ — PAYLOAD VOXEL-QUADRATURE RESOLUTION AUDIT ===", flush=True)

    print("\n=== A — UPSTREAM AUDIT ===", flush=True)
    expected = {
        CR3_SOURCE: EXPECTED_CR3_SHA256,
        CR3R_SOURCE: EXPECTED_CR3R_SHA256,
        CR4R_SOURCE: EXPECTED_CR4R_SHA256,
        C2A_SOURCE: EXPECTED_C2A_SHA256,
        C2AR_SOURCE: EXPECTED_C2AR_SHA256,
    }
    for path, exp in expected.items():
        require(path)
        actual = sha256(path)
        print(f"{path.name}_SHA256={actual}", flush=True)
        if actual != exp:
            raise RuntimeError(f"Upstream source hash mismatch for {path.name}")
    print("UPSTREAM_023C2AR_AUDIT=PASS", flush=True)

    cr3 = load_module("cr3_for_023c2aq", CR3_SOURCE)
    cr3r = load_module("cr3r_for_023c2aq", CR3R_SOURCE)

    print("\n=== B — LOAD FIELDS ===", flush=True)
    phi65, axis65, dx65, meta65 = load_field(N65_ARTIFACT, 65)
    phi73, axis73, dx73, meta73 = load_field(N73_CHECKPOINT, 73)
    print(f"N65_SOURCE={N65_ARTIFACT.relative_to(ROOT)}", flush=True)
    print(f"N73_SOURCE={N73_CHECKPOINT.relative_to(ROOT)}", flush=True)
    print(f"N73_ACCEPTED_TOTAL={meta73['accepted_total']:.0f}", flush=True)
    print(f"PAYLOAD_CENTER={PAYLOAD_CENTER:.15e}", flush=True)
    print(f"PAYLOAD_RADIUS={PAYLOAD_RADIUS:.15e}", flush=True)
    print("KNOWN_WORST_DIRECTION=" + ",".join(f"{x:.15e}" for x in KNOWN_WORST_DIRECTION), flush=True)

    grid65 = make_source_grid(cr3, "N65_NATIVE", phi65, axis65, dx65)
    grid73 = make_source_grid(cr3, "N73_NATIVE", phi73, axis73, dx73)

    r65 = audit_native(grid65)
    r73 = audit_native(grid73)

    print("\n=== C — MIDPOINT REPRODUCTION CHECK ===", flush=True)
    e65 = relative_match(r65["Q1"].total, MIDPOINT_N65_REFERENCE)
    e73 = relative_match(r73["Q1"].total, MIDPOINT_N73_REFERENCE)
    print(f"N65_MIDPOINT_REFERENCE_RELERR={e65:.15e}", flush=True)
    print(f"N73_MIDPOINT_REFERENCE_RELERR={e73:.15e}", flush=True)
    print("MIDPOINT_REFERENCE_REPRODUCTION=" + ("PASS" if max(e65,e73) <= MIDPOINT_REFERENCE_REL_TOL else "FAIL"), flush=True)
    if max(e65, e73) > MIDPOINT_REFERENCE_REL_TOL:
        raise RuntimeError("Midpoint payload reproduction failed; do not interpret quadrature audit")

    print("\n=== D — CROSS-GRID FIELD TRANSFER MIDPOINT MATRIX ===", flush=True)
    n65_to_73, _ = midpoint_transfer(cr3, cr3r, "N65_FIELD_ON_N73_GRID", phi65, axis65, 73)
    n73_to_65, _ = midpoint_transfer(cr3, cr3r, "N73_FIELD_ON_N65_GRID", phi73, axis73, 65)
    n65_to_81, _ = midpoint_transfer(cr3, cr3r, "N65_FIELD_ON_N81_GRID", phi65, axis65, 81)
    n73_to_81, _ = midpoint_transfer(cr3, cr3r, "N73_FIELD_ON_N81_GRID", phi73, axis73, 81)

    print("\n=== E — DECISION ===", flush=True)
    n65_ref = r65["Q3_NEAR_Q14"]
    n73_ref = r73["Q3_NEAR_Q14"]
    n65_conv = abs(r65["Q3_NEAR_Q14"].total-r65["Q3_NEAR_Q10"].total) / max(abs(r65["Q3_NEAR_Q14"].total),abs(r65["Q3_NEAR_Q10"].total),1.0) <= 1e-2
    n73_conv = abs(r73["Q3_NEAR_Q14"].total-r73["Q3_NEAR_Q10"].total) / max(abs(r73["Q3_NEAR_Q14"].total),abs(r73["Q3_NEAR_Q10"].total),1.0) <= 1e-2
    n65_mid_sign = r65["Q1"].total > 0.0
    n73_mid_sign = r73["Q1"].total > 0.0
    n65_ref_sign = n65_ref.total > 0.0
    n73_ref_sign = n73_ref.total > 0.0

    print(f"N65_REFINED_SENTINEL={n65_ref.total:.15e}", flush=True)
    print(f"N73_REFINED_SENTINEL={n73_ref.total:.15e}", flush=True)
    print("N65_REFINED_SENTINEL_OUTWARD=" + ("YES" if n65_ref_sign else "NO"), flush=True)
    print("N73_REFINED_SENTINEL_OUTWARD=" + ("YES" if n73_ref_sign else "NO"), flush=True)
    print("N65_POINT_QUADRATURE_SIGN_CHANGED=" + ("YES" if n65_mid_sign != n65_ref_sign else "NO"), flush=True)
    print("N73_POINT_QUADRATURE_SIGN_CHANGED=" + ("YES" if n73_mid_sign != n73_ref_sign else "NO"), flush=True)
    print(f"N65_FIELD_ON_N73_GRID_MIDPOINT={n65_to_73:.15e}", flush=True)
    print(f"N73_FIELD_ON_N65_GRID_MIDPOINT={n73_to_65:.15e}", flush=True)
    print(f"N65_FIELD_ON_N81_GRID_MIDPOINT={n65_to_81:.15e}", flush=True)
    print(f"N73_FIELD_ON_N81_GRID_MIDPOINT={n73_to_81:.15e}", flush=True)

    if not (n65_conv and n73_conv):
        status = "INCOMPLETE_KERNEL_QUADRATURE_NOT_CONVERGED"
        next_action = "ADAPTIVE_CELL_KERNEL_INTEGRATION_OR_ANALYTIC_VOXEL_KERNEL"
    elif n65_mid_sign != n65_ref_sign:
        status = "MIDPOINT_N65_FORCE_SIGN_FALSIFIED_BY_VOXEL_QUADRATURE"
        next_action = "REPAIR_FULL_320_DIRECTION_PAYLOAD_OPERATOR_BEFORE_MORE_STATIONARITY_OR_HESSIAN"
    elif n73_mid_sign != n73_ref_sign:
        status = "MIDPOINT_N73_FORCE_SIGN_CHANGED_BY_VOXEL_QUADRATURE"
        next_action = "REPAIR_PAYLOAD_OPERATOR_THEN_REASSESS_N65_N73_FORCE_CONVERGENCE"
    elif n65_ref_sign != n73_ref_sign:
        status = "REFINED_QUADRATURE_PRESERVES_N65_N73_OPPOSITE_SIGNS"
        next_action = "FINISH_N73_STRICT_STATIONARITY_THEN_APPLY_REFINED_FORCE_OPERATOR"
    else:
        status = "REFINED_QUADRATURE_GIVES_COMMON_FORCE_SIGN"
        next_action = "USE_REFINED_OPERATOR_FOR_FULL_FORCE_CONVERGENCE_AND_DECIDE_023C2"

    print(f"023C2AQ_PAYLOAD_VOXEL_QUADRATURE_RESOLUTION_AUDIT={status}", flush=True)
    print("N73_INTERMEDIATE_STATE_USED_AS_PHYSICAL_FALSIFICATION=NO", flush=True)
    print("FULL_PHYSICAL_HESSIAN=DEFERRED_UNTIL_PAYLOAD_OPERATOR_AND_N73_STATIONARITY_ARE_RESOLVED", flush=True)
    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT", flush=True)
    print(f"NEXT={next_action}", flush=True)
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED", flush=True)
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
    print("NEW_PHYSICS_DISCOVERY=NO", flush=True)
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023C2AQ_PAYLOAD_VOXEL_QUADRATURE_RESOLUTION_AUDIT", flush=True)


if __name__ == "__main__":
    main()
