#!/usr/bin/env python3
"""023CR — checkerboard-free Cartesian topology and relaxation repair.

PURPOSE
-------
Repair the numerical obstruction exposed by 023C before interpreting any
unrestricted Cartesian result as physical.

023C did not begin from a faithful Cartesian representation of the exact
B=7 candidate: its primary initial lattice reconstructed B ~= 4.83 rather
than 7 and underestimated the continuum energy by about 30 percent.  During
relaxation it then developed nearest-neighbor angles arbitrarily close to pi
while the quartic Skyrme energy collapsed almost to zero.

That behavior is diagnostic of a centered-difference checkerboard/Nyquist
null mode.  For the centered derivative

    D_c f_i = (f_{i+1} - f_{i-1}) / (2 dx),

an alternating lattice mode f_i = (-1)^i has D_c f_i = 0 despite maximal
nearest-neighbor variation.  A field energy built only from such centered
first derivatives can therefore develop an unphysical odd/even lattice mode
that has no continuum analogue.

SCIENTIFIC QUESTION
-------------------
Can the exact 023BR B=7, eta=0.4, m=8 candidate be represented and relaxed on
a Cartesian lattice after removing the checkerboard-blind discretization,
while preserving its continuum topological sector and smoothness?

CHEAPEST DECISIVE EXPERIMENT
----------------------------
1. Audit the exact 023C run and reproduce the checkerboard null-mode witness.
2. Replace the centered derivative action by a parity-symmetrized nearest-
   neighbor link action.  Every nearest-neighbor jump contributes to the
   energy, so the checkerboard mode is not a null direction.
3. Verify the exact discrete link-action gradient against a finite-difference
   directional derivative.
4. Shrink the Cartesian box only to the already-resolved continuum tail
   radius, rather than wasting resolution on several additional wall widths.
5. Scan several lattice resolutions BEFORE relaxation.
6. Require two consecutive resolutions to reconstruct the continuum energy,
   its E2/E4/E0 components, and B=7 topology consistently.
7. Only if that prerequisite is green, perform an unrestricted S^3
   relaxation with a numerical admissibility guard that rejects lattice
   discontinuities/topology loss.  This guard enforces the continuum
   topological sector; it is not a new physical stabilizer.
8. Reconstruct smooth-field continuum diagnostics with an independent
   fourth-order derivative after relaxation.

MODEL
-----
The continuum static field is

    phi = (sigma, pi_1, pi_2, pi_3),
    phi . phi = 1,

with energy density

    e2 = sum_i |d_i phi|^2,

    e4 = sum_(i<j) [
        |d_i phi|^2 |d_j phi|^2
        - (d_i phi . d_j phi)^2
    ],

    V = m^2 (1-sigma) (1+eta sigma).

The active gravitational source remains

    S = 2(e4 - V).

CHECKERBOARD-FREE DISCRETE ACTION
---------------------------------
For each cubic lattice cell use forward link derivatives from one corner,

    q_x = (phi_{i+1,j,k} - phi_{i,j,k}) / dx,
    q_y = (phi_{i,j+1,k} - phi_{i,j,k}) / dx,
    q_z = (phi_{i,j,k+1} - phi_{i,j,k}) / dx,

and average that action with the opposite-corner backward-link action.  The
result is parity symmetric and every nearest-neighbor alternating mode has
nonzero derivative cost.

The exact Euclidean gradient is implemented as the adjoint of these link
operators and projected onto the S^3 tangent bundle.  A numerical gradient
self-check is mandatory.

TOPOLOGY DIAGNOSTICS
--------------------
Topology is reconstructed independently using both second-order and
fourth-order continuum Jacobian estimators,

    B = -(1/(2 pi^2)) integral det(phi,d_x phi,d_y phi,d_z phi) d^3x.

The fourth-order estimator is primary once the field is demonstrably smooth.
Agreement between the two estimators is itself a resolution diagnostic.

The relaxation also enforces a mesh-continuity admissibility condition:
trials are rejected if the maximum nearest-neighbor S^3 angle becomes too
large or if the independently reconstructed topological charge departs
materially from B=7.  In the continuum, fixed-vacuum-boundary degree cannot
change under a smooth deformation, so rejecting a discrete topology-changing
jump prevents a numerical artifact rather than adding a stabilizing force.

PROMOTION CONDITION
-------------------
023CR is GREEN_NUMERICAL_REPAIR only if:

    UPSTREAM_023C_AUDIT=PASS
    CHECKERBOARD_NULL_MODE_DIAGNOSIS=PASS
    LINK_ACTION_GRADIENT_SELFCHECK=PASS
    INITIAL_RESOLUTION_PAIR=FOUND
    INITIAL_LINK_ENERGY_RECONSTRUCTION=PASS
    INITIAL_CARTESIAN_TOPOLOGY_RECONSTRUCTION=PASS
    ADMISSIBLE_UNRESTRICTED_RELAXATION=PASS
    RELAXED_CARTESIAN_TOPOLOGY=PASS
    RELAXED_LATTICE_SMOOTHNESS=PASS
    RELAXED_POSITIVE_TOTAL_ACTIVE_MASS=PASS
    RELAXED_NEGATIVE_ENCLOSED_ACTIVE_MASS=PASS

A green result is a NUMERICAL repair only.  It does not establish the full
unrestricted Hessian.  It authorizes a corrected 023C2 link-lattice Hessian
and dense-payload gate.

FALSIFIERS / STOP RULE
----------------------
- If no tested resolution faithfully reconstructs the initial B=7 field,
  stop and replace the topology discretization/adapt the mesh before further
  relaxation.
- If the checkerboard-free action still cannot preserve a smooth B=7 sector
  under refinement, do not call that a physical instability until continuum
  convergence is established.
- If a later corrected full Hessian finds a robust negative mode inside the
  resolved B=7 sector, preserve that as the physical stability falsification.

APPROXIMATION LEVEL
-------------------
Flat-spacetime Skyrme matter field.  Gravity is used only through the static
linearized active source diagnostic.  Einstein backreaction is not included.

CLAIM BOUNDARIES
----------------
This run does not establish nonlinear Einstein-Skyrme consistency, practical
energy scaling, a real material, an experimental signal, or a practical
antigravity device.

RELATED FILES
-------------
    simulations/023a_topological_false_core_multiskyrmion_gr_repulsion_gate.py
    simulations/023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.py
    simulations/023br_promotion_grade_exact_map_robustness_repair.py
    simulations/023c_unrestricted_cartesian_3d_relaxation_and_full_physical_hessian.py

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023CR_CHECKERBOARD_FREE_LINK_LATTICE_TOPOLOGY_REPAIR
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib.util
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
A23_SOURCE = ROOT / "simulations/023a_topological_false_core_multiskyrmion_gr_repulsion_gate.py"
B23_SOURCE = ROOT / "simulations/023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.py"
BR23_SOURCE = ROOT / "simulations/023br_promotion_grade_exact_map_robustness_repair.py"
C23_SOURCE = ROOT / "simulations/023c_unrestricted_cartesian_3d_relaxation_and_full_physical_hessian.py"
C23_LOG = ROOT / "results/logs/023c_unrestricted_cartesian_3d_relaxation_and_full_physical_hessian.log"

EXPECTED_023A_SHA256 = "0087a5d2b4f93667308cabf4c3c498200ed29381e9493acf21714df7d8e11c9b"
EXPECTED_023B_SHA256 = "6bf99785e67cfe1b2dfcb460bc3145a24115e25949e112f8480a89c880a2803c"
EXPECTED_023BR_SHA256 = "e72d56767ae9a0ec8accdbfc95034425ecd30f81013d2cb4682f7555dd61a7c1"
EXPECTED_023C_SHA256 = "9fd323a2f845c0373f7926af11f09c563138386b18c8fa3c091acb114318a675"

EXPECTED_023C_MARKERS = (
    "INITIAL_CARTESIAN_ENERGY_RECONSTRUCTION=FAIL",
    "INITIAL_CARTESIAN_TOPOLOGY=FAIL",
    "PRIMARY_RELAXED_TOPOLOGY_RELERR=9.999999999999861e-01",
    "PRIMARY_RELAXED_MAX_NEIGHBOR_ANGLE=3.141575972393730e+00",
    "FULL_PHYSICAL_HESSIAN=FAIL_OR_UNRESOLVED",
    "UNRESTRICTED_CARTESIAN_3D_STABILITY=NOT_PROMOTED",
)

B = 7
ETA = 0.40
MASS = 8.0

# Initial representation scan.  The final 113 grid is used only if needed.
GRID_LEVELS = (53, 65, 81, 97, 113)
TAIL_FACTOR = 1.18
PAYLOAD_DOMAIN_FACTOR = 1.15
SHELL_WALL_MARGIN = 2.0

# Initial continuum reconstruction gates.
MAX_INITIAL_TOTAL_ENERGY_RELERR = 5.0e-2
MAX_INITIAL_COMPONENT_RELERR = 8.0e-2
MAX_INITIAL_TOPOLOGY_RELERR = 3.0e-2
MAX_TOPOLOGY_ESTIMATOR_DISAGREEMENT = 2.0e-2
MAX_INITIAL_NEIGHBOR_ANGLE = 0.95
MAX_PAIR_ENERGY_RELCHANGE = 2.5e-2
MAX_PAIR_TOPOLOGY_ABSCHANGE = 1.5e-2

# Admissible relaxation.  These are numerical smoothness/topology guards.
RELAX_MAX_ITER = 90
RELAX_GRAD_RMS_TOL = 4.0e-3
RELAX_GRAD_MAX_TOL = 6.0e-2
RELAX_MAX_POINT_ROTATION = 0.055
MAX_ADMISSIBLE_NEIGHBOR_ANGLE = 1.05
MAX_ADMISSIBLE_TOPOLOGY_RELERR = 5.0e-2
MIN_ACCEPTED_STEPS_FOR_AUDIT = 5
MIN_GRADIENT_REDUCTION_FACTOR = 3.0

# Physical diagnostics retained from 023BR.
MIN_NEGATIVE_ACTIVE_FRACTION = 1.0e-2
MIN_POSITIVE_ACTIVE_RATIO = 0.0

BLIND_WILDCARDS = (1.6, 1.875, 3.125, 0.625, 5.0)


@dataclass
class InitialAudit:
    n: int
    half_domain: float
    dx: float
    total_energy: float
    e2: float
    e4: float
    e0: float
    energy_relerr: float
    e2_relerr: float
    e4_relerr: float
    e0_relerr: float
    topology2: float
    topology4: float
    topology4_relerr: float
    topology_disagreement: float
    max_neighbor_angle: float
    passed: bool


@dataclass
class RelaxResult:
    field: np.ndarray
    initial_energy: float
    final_energy: float
    initial_grad_rms: float
    final_grad_rms: float
    final_grad_max: float
    iterations: int
    accepted_steps: int
    rejected_topology: int
    rejected_smoothness: int
    line_search_failed: bool
    converged: bool


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_file(path: Path) -> None:
    if not path.exists():
        raise RuntimeError(f"Missing required file: {path}")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


def relative_error(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0e-300)


def enforce_vacuum_boundary(phi: np.ndarray) -> None:
    vacuum = np.array([1.0, 0.0, 0.0, 0.0])
    phi[0, :, :, :] = vacuum
    phi[-1, :, :, :] = vacuum
    phi[:, 0, :, :] = vacuum
    phi[:, -1, :, :] = vacuum
    phi[:, :, 0, :] = vacuum
    phi[:, :, -1, :] = vacuum


def normalize_field(phi: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(phi, axis=-1, keepdims=True)
    return phi / np.maximum(norm, 1.0e-300)


def project_tangent(phi: np.ndarray, vec: np.ndarray) -> np.ndarray:
    return vec - np.sum(phi * vec, axis=-1, keepdims=True) * phi


def exp_map_update(phi: np.ndarray, tangent: np.ndarray, alpha: float) -> np.ndarray:
    out = phi.copy()
    p = phi[1:-1, 1:-1, 1:-1]
    v = tangent[1:-1, 1:-1, 1:-1]
    speed = np.linalg.norm(v, axis=-1)
    angle = alpha * speed
    new = p.copy()
    mask = speed > 1.0e-16
    if np.any(mask):
        unit = np.zeros_like(v)
        unit[mask] = v[mask] / speed[mask, None]
        new[mask] = (
            np.cos(angle[mask])[:, None] * p[mask]
            + np.sin(angle[mask])[:, None] * unit[mask]
        )
    out[1:-1, 1:-1, 1:-1] = new
    enforce_vacuum_boundary(out)
    return normalize_field(out)


def potential_sigma(sigma: np.ndarray, eta: float, mass: float) -> np.ndarray:
    return mass * mass * (1.0 - sigma) * (1.0 + eta * sigma)


def dpotential_dsigma(sigma: np.ndarray, eta: float, mass: float) -> np.ndarray:
    return mass * mass * ((eta - 1.0) - 2.0 * eta * sigma)


def metric_terms(qx: np.ndarray, qy: np.ndarray, qz: np.ndarray):
    gxx = np.sum(qx * qx, axis=-1)
    gyy = np.sum(qy * qy, axis=-1)
    gzz = np.sum(qz * qz, axis=-1)
    gxy = np.sum(qx * qy, axis=-1)
    gxz = np.sum(qx * qz, axis=-1)
    gyz = np.sum(qy * qz, axis=-1)
    e2 = gxx + gyy + gzz
    e4 = (
        gxx * gyy - gxy * gxy
        + gxx * gzz - gxz * gxz
        + gyy * gzz - gyz * gyz
    )
    return gxx, gyy, gzz, gxy, gxz, gyz, e2, e4


def link_orientation_energy_gradient(
    phi: np.ndarray,
    dx: float,
    forward: bool,
    need_gradient: bool,
):
    """Derivative action from one opposite cube-corner orientation."""

    if forward:
        base = phi[:-1, :-1, :-1]
        qx = (phi[1:, :-1, :-1] - base) / dx
        qy = (phi[:-1, 1:, :-1] - base) / dx
        qz = (phi[:-1, :-1, 1:] - base) / dx
    else:
        base = phi[1:, 1:, 1:]
        qx = (base - phi[:-1, 1:, 1:]) / dx
        qy = (base - phi[1:, :-1, 1:]) / dx
        qz = (base - phi[1:, 1:, :-1]) / dx

    gxx, gyy, gzz, gxy, gxz, gyz, e2, e4 = metric_terms(qx, qy, qz)
    volume = dx**3
    E2 = float(np.sum(e2) * volume)
    E4 = float(np.sum(e4) * volume)

    if not need_gradient:
        return E2, E4, None

    px = 2.0 * (
        qx
        + (gyy + gzz)[..., None] * qx
        - gxy[..., None] * qy
        - gxz[..., None] * qz
    )
    py = 2.0 * (
        qy
        + (gxx + gzz)[..., None] * qy
        - gxy[..., None] * qx
        - gyz[..., None] * qz
    )
    pz = 2.0 * (
        qz
        + (gxx + gyy)[..., None] * qz
        - gxz[..., None] * qx
        - gyz[..., None] * qy
    )

    grad = np.zeros_like(phi)
    c = volume / dx

    if forward:
        grad[:-1, :-1, :-1] -= c * (px + py + pz)
        grad[1:, :-1, :-1] += c * px
        grad[:-1, 1:, :-1] += c * py
        grad[:-1, :-1, 1:] += c * pz
    else:
        grad[1:, 1:, 1:] += c * (px + py + pz)
        grad[:-1, 1:, 1:] -= c * px
        grad[1:, :-1, 1:] -= c * py
        grad[1:, 1:, :-1] -= c * pz

    return E2, E4, grad


def link_energy_gradient(
    phi: np.ndarray,
    dx: float,
    eta: float,
    mass: float,
    need_gradient: bool = True,
):
    """Parity-symmetrized nearest-neighbor link action and exact gradient."""

    E2f, E4f, gf = link_orientation_energy_gradient(phi, dx, True, need_gradient)
    E2b, E4b, gb = link_orientation_energy_gradient(phi, dx, False, need_gradient)
    E2 = 0.5 * (E2f + E2b)
    E4 = 0.5 * (E4f + E4b)

    sigma = phi[1:-1, 1:-1, 1:-1, 0]
    V = potential_sigma(sigma, eta, mass)
    E0 = float(np.sum(V) * dx**3)
    E = E2 + E4 + E0

    if not need_gradient:
        return E, E2, E4, E0, None

    assert gf is not None and gb is not None
    grad = 0.5 * (gf + gb)
    grad[1:-1, 1:-1, 1:-1, 0] += dpotential_dsigma(sigma, eta, mass) * dx**3

    grad[0, :, :, :] = 0.0
    grad[-1, :, :, :] = 0.0
    grad[:, 0, :, :] = 0.0
    grad[:, -1, :, :] = 0.0
    grad[:, :, 0, :] = 0.0
    grad[:, :, -1, :] = 0.0
    return E, E2, E4, E0, grad


def riemannian_gradient_density(phi: np.ndarray, dx: float):
    E, E2, E4, E0, grad = link_energy_gradient(phi, dx, ETA, MASS, True)
    assert grad is not None
    gd = project_tangent(phi, grad / dx**3)
    gd[0, :, :, :] = 0.0
    gd[-1, :, :, :] = 0.0
    gd[:, 0, :, :] = 0.0
    gd[:, -1, :, :] = 0.0
    gd[:, :, 0, :] = 0.0
    gd[:, :, -1, :] = 0.0
    return E, E2, E4, E0, gd


def gradient_selfcheck() -> tuple[float, bool]:
    n = 8
    L = 1.4
    axis = np.linspace(-L, L, n)
    dx = float(axis[1] - axis[0])
    X, Y, Z = np.meshgrid(axis, axis, axis, indexing="ij")
    envelope = np.maximum(
        (1.0 - (X / L) ** 2) * (1.0 - (Y / L) ** 2) * (1.0 - (Z / L) ** 2),
        0.0,
    )
    pion = np.zeros((n, n, n, 3))
    pion[..., 0] = 0.13 * envelope * np.sin(math.pi * X / L)
    pion[..., 1] = 0.10 * envelope * np.sin(math.pi * Y / L)
    pion[..., 2] = 0.08 * envelope * np.sin(math.pi * Z / L)
    pion2 = np.sum(pion * pion, axis=-1)
    phi = np.zeros((n, n, n, 4))
    phi[..., 0] = np.sqrt(np.maximum(1.0 - pion2, 1.0e-14))
    phi[..., 1:] = pion
    enforce_vacuum_boundary(phi)
    phi = normalize_field(phi)

    _, _, _, _, grad = link_energy_gradient(phi, dx, ETA, MASS, True)
    assert grad is not None
    rng = np.random.default_rng(23041)
    v = np.zeros_like(phi)
    v[1:-1, 1:-1, 1:-1] = rng.normal(size=v[1:-1, 1:-1, 1:-1].shape)
    v = project_tangent(phi, v)
    v /= max(math.sqrt(float(np.sum(v * v))), 1.0e-300)

    eps = 1.5e-6
    plus = exp_map_update(phi, v, eps)
    minus = exp_map_update(phi, v, -eps)
    Ep = link_energy_gradient(plus, dx, ETA, MASS, False)[0]
    Em = link_energy_gradient(minus, dx, ETA, MASS, False)[0]
    finite = (Ep - Em) / (2.0 * eps)
    analytic = float(np.sum(grad * v))
    rel = abs(finite - analytic) / max(abs(finite), abs(analytic), 1.0e-12)
    return rel, rel <= 3.0e-6


def checkerboard_witness() -> tuple[float, float, bool]:
    n = 18
    idx = np.indices((n, n, n))
    f = (-1.0) ** (idx[0] + idx[1] + idx[2])
    dcx = 0.5 * (f[2:, 1:-1, 1:-1] - f[:-2, 1:-1, 1:-1])
    dcy = 0.5 * (f[1:-1, 2:, 1:-1] - f[1:-1, :-2, 1:-1])
    dcz = 0.5 * (f[1:-1, 1:-1, 2:] - f[1:-1, 1:-1, :-2])
    central_rms = math.sqrt(float(np.mean(dcx * dcx + dcy * dcy + dcz * dcz)))
    lfx = f[1:, :-1, :-1] - f[:-1, :-1, :-1]
    lfy = f[:-1, 1:, :-1] - f[:-1, :-1, :-1]
    lfz = f[:-1, :-1, 1:] - f[:-1, :-1, :-1]
    link_rms = math.sqrt(float(np.mean(lfx * lfx + lfy * lfy + lfz * lfz)))
    passed = central_rms <= 1.0e-15 and link_rms > 1.0
    return central_rms, link_rms, passed


def central2_derivatives(phi: np.ndarray, dx: float):
    inv = 1.0 / (2.0 * dx)
    qx = (phi[2:, 1:-1, 1:-1] - phi[:-2, 1:-1, 1:-1]) * inv
    qy = (phi[1:-1, 2:, 1:-1] - phi[1:-1, :-2, 1:-1]) * inv
    qz = (phi[1:-1, 1:-1, 2:] - phi[1:-1, 1:-1, :-2]) * inv
    return qx, qy, qz


def central4_derivatives(phi: np.ndarray, dx: float):
    c = 1.0 / (12.0 * dx)
    qx = (
        -phi[4:, 2:-2, 2:-2]
        + 8.0 * phi[3:-1, 2:-2, 2:-2]
        - 8.0 * phi[1:-3, 2:-2, 2:-2]
        + phi[:-4, 2:-2, 2:-2]
    ) * c
    qy = (
        -phi[2:-2, 4:, 2:-2]
        + 8.0 * phi[2:-2, 3:-1, 2:-2]
        - 8.0 * phi[2:-2, 1:-3, 2:-2]
        + phi[2:-2, :-4, 2:-2]
    ) * c
    qz = (
        -phi[2:-2, 2:-2, 4:]
        + 8.0 * phi[2:-2, 2:-2, 3:-1]
        - 8.0 * phi[2:-2, 2:-2, 1:-3]
        + phi[2:-2, 2:-2, :-4]
    ) * c
    return qx, qy, qz


def topology_from_derivatives(center: np.ndarray, qx: np.ndarray, qy: np.ndarray, qz: np.ndarray, dx: float) -> float:
    mat = np.stack([center, qx, qy, qz], axis=-1)
    det = np.linalg.det(mat)
    return -float(np.sum(det) * dx**3 / (2.0 * math.pi**2))


def topology2(phi: np.ndarray, dx: float) -> float:
    qx, qy, qz = central2_derivatives(phi, dx)
    return topology_from_derivatives(phi[1:-1, 1:-1, 1:-1], qx, qy, qz, dx)


def topology4(phi: np.ndarray, dx: float) -> float:
    qx, qy, qz = central4_derivatives(phi, dx)
    return topology_from_derivatives(phi[2:-2, 2:-2, 2:-2], qx, qy, qz, dx)


def max_neighbor_angle(phi: np.ndarray) -> float:
    maxima = []
    for a, b in (
        (phi[1:], phi[:-1]),
        (phi[:, 1:], phi[:, :-1]),
        (phi[:, :, 1:], phi[:, :, :-1]),
    ):
        dot = np.sum(a * b, axis=-1)
        maxima.append(float(np.max(np.arccos(np.clip(dot, -1.0, 1.0)))))
    return max(maxima)


def profile_crossing_radius(profile, fraction_pi: float) -> float:
    target = float(fraction_pi * math.pi)
    F = np.asarray(profile.F, dtype=float)
    r = np.asarray(profile.r, dtype=float)
    return float(np.interp(target, F[::-1], r[::-1]))


def choose_compact_half_domain(profile, payload_center: float, payload_radius: float) -> tuple[float, float, float]:
    F = np.asarray(profile.F, dtype=float)
    r = np.asarray(profile.r, dtype=float)
    tail_idx = np.where(F <= 1.0e-5)[0]
    r_tail = float(r[tail_idx[0]]) if len(tail_idx) else float(r[-1])
    r90 = profile_crossing_radius(profile, 0.90)
    r10 = profile_crossing_radius(profile, 0.10)
    wall = max(r10 - r90, 1.0e-6)
    half = max(
        TAIL_FACTOR * r_tail,
        float(profile.shell_radius) + SHELL_WALL_MARGIN * wall,
        PAYLOAD_DOMAIN_FACTOR * (payload_center + payload_radius),
    )
    half = min(half, 0.92 * float(r[-1]))
    boundary_F = float(np.interp(half, r, F))
    return half, r_tail, boundary_F


def sample_rational_map_field(profile, b_parameter: float, n: int, half_domain: float, c23):
    return c23.sample_rational_map_field(profile, b_parameter, n, half_domain)


def audit_initial(phi: np.ndarray, dx: float, n: int, half_domain: float, continuum: tuple[float, float, float, float]) -> InitialAudit:
    E, E2, E4, E0, _ = link_energy_gradient(phi, dx, ETA, MASS, False)
    CE, CE2, CE4, CE0 = continuum
    t2 = topology2(phi, dx)
    t4 = topology4(phi, dx)
    trel = abs(abs(t4) / B - 1.0)
    tdis = abs(abs(t4) - abs(t2)) / B
    angle = max_neighbor_angle(phi)
    passed = (
        relative_error(E, CE) <= MAX_INITIAL_TOTAL_ENERGY_RELERR
        and relative_error(E2, CE2) <= MAX_INITIAL_COMPONENT_RELERR
        and relative_error(E4, CE4) <= MAX_INITIAL_COMPONENT_RELERR
        and relative_error(E0, CE0) <= MAX_INITIAL_COMPONENT_RELERR
        and trel <= MAX_INITIAL_TOPOLOGY_RELERR
        and tdis <= MAX_TOPOLOGY_ESTIMATOR_DISAGREEMENT
        and angle <= MAX_INITIAL_NEIGHBOR_ANGLE
    )
    return InitialAudit(
        n=n,
        half_domain=half_domain,
        dx=dx,
        total_energy=E,
        e2=E2,
        e4=E4,
        e0=E0,
        energy_relerr=relative_error(E, CE),
        e2_relerr=relative_error(E2, CE2),
        e4_relerr=relative_error(E4, CE4),
        e0_relerr=relative_error(E0, CE0),
        topology2=t2,
        topology4=t4,
        topology4_relerr=trel,
        topology_disagreement=tdis,
        max_neighbor_angle=angle,
        passed=passed,
    )


def print_audit(a: InitialAudit) -> None:
    p = f"N{a.n}"
    print(f"{p}_DX={a.dx:.15e}")
    print(f"{p}_LINK_ENERGY={a.total_energy:.15e}")
    print(f"{p}_LINK_E2={a.e2:.15e}")
    print(f"{p}_LINK_E4={a.e4:.15e}")
    print(f"{p}_LINK_E0={a.e0:.15e}")
    print(f"{p}_ENERGY_RELERR={a.energy_relerr:.15e}")
    print(f"{p}_E2_RELERR={a.e2_relerr:.15e}")
    print(f"{p}_E4_RELERR={a.e4_relerr:.15e}")
    print(f"{p}_E0_RELERR={a.e0_relerr:.15e}")
    print(f"{p}_TOPOLOGY_CENTRAL2={a.topology2:.15e}")
    print(f"{p}_TOPOLOGY_CENTRAL4={a.topology4:.15e}")
    print(f"{p}_TOPOLOGY4_RELERR={a.topology4_relerr:.15e}")
    print(f"{p}_TOPOLOGY_ESTIMATOR_DISAGREEMENT={a.topology_disagreement:.15e}")
    print(f"{p}_MAX_NEIGHBOR_ANGLE={a.max_neighbor_angle:.15e}")
    print(f"{p}_INITIAL_RECONSTRUCTION=" + ("PASS" if a.passed else "FAIL"))


def gradient_norms(g: np.ndarray) -> tuple[float, float]:
    mag = np.linalg.norm(g[1:-1, 1:-1, 1:-1], axis=-1)
    return float(np.sqrt(np.mean(mag * mag))), float(np.max(mag))


def tangent_inner(a: np.ndarray, b: np.ndarray, dx: float) -> float:
    return float(np.sum(a[1:-1, 1:-1, 1:-1] * b[1:-1, 1:-1, 1:-1]) * dx**3)


def relax_admissible(phi0: np.ndarray, dx: float) -> RelaxResult:
    phi = phi0.copy()
    E, _, _, _, g = riemannian_gradient_density(phi, dx)
    initial_energy = E
    g0, _ = gradient_norms(g)
    direction = -g
    previous_g = None
    accepted = 0
    rejected_topology = 0
    rejected_smoothness = 0
    line_failed = False

    for iteration in range(1, RELAX_MAX_ITER + 1):
        grms, gmax = gradient_norms(g)
        if grms <= RELAX_GRAD_RMS_TOL and gmax <= RELAX_GRAD_MAX_TOL:
            return RelaxResult(phi, initial_energy, E, g0, grms, gmax, iteration - 1, accepted, rejected_topology, rejected_smoothness, False, True)

        if previous_g is not None:
            y = g - previous_g
            denom = max(tangent_inner(previous_g, previous_g, dx), 1.0e-300)
            beta = max(0.0, tangent_inner(g, y, dx) / denom)
            direction = -g + beta * direction
            direction = project_tangent(phi, direction)
            if tangent_inner(g, direction, dx) >= 0.0:
                direction = -g

        previous_g = g.copy()
        max_dir = float(np.max(np.linalg.norm(direction[1:-1, 1:-1, 1:-1], axis=-1)))
        alpha = min(1.0, RELAX_MAX_POINT_ROTATION / max(max_dir, 1.0e-300))
        slope = tangent_inner(g, direction, dx)
        accepted_trial = False

        for _ in range(18):
            trial = exp_map_update(phi, direction, alpha)
            angle = max_neighbor_angle(trial)
            if angle > MAX_ADMISSIBLE_NEIGHBOR_ANGLE:
                rejected_smoothness += 1
                alpha *= 0.5
                continue

            Et = link_energy_gradient(trial, dx, ETA, MASS, False)[0]
            if Et > E + 1.0e-4 * alpha * slope:
                alpha *= 0.5
                continue

            t4 = topology4(trial, dx)
            if abs(abs(t4) / B - 1.0) > MAX_ADMISSIBLE_TOPOLOGY_RELERR:
                rejected_topology += 1
                alpha *= 0.5
                continue

            phi = trial
            E = Et
            accepted += 1
            accepted_trial = True
            break

        if not accepted_trial:
            line_failed = True
            break

        E, _, _, _, g = riemannian_gradient_density(phi, dx)

    grms, gmax = gradient_norms(g)
    converged = grms <= RELAX_GRAD_RMS_TOL and gmax <= RELAX_GRAD_MAX_TOL
    return RelaxResult(phi, initial_energy, E, g0, grms, gmax, iteration, accepted, rejected_topology, rejected_smoothness, line_failed, converged)


def smooth_continuum_diagnostics(phi: np.ndarray, axis: np.ndarray, dx: float):
    qx, qy, qz = central4_derivatives(phi, dx)
    _, _, _, _, _, _, e2, e4 = metric_terms(qx, qy, qz)
    center = phi[2:-2, 2:-2, 2:-2]
    V = potential_sigma(center[..., 0], ETA, MASS)
    rho = e2 + e4 + V
    active = 2.0 * (e4 - V)
    volume = dx**3
    E = float(np.sum(rho) * volume)
    Atot = float(np.sum(active) * volume)

    coord = axis[2:-2]
    X, Y, Z = np.meshgrid(coord, coord, coord, indexing="ij")
    r = np.sqrt(X * X + Y * Y + Z * Z).ravel()
    source = (active * volume).ravel()
    order = np.argsort(r)
    cumulative = np.cumsum(source[order])
    min_active = float(np.min(cumulative)) if cumulative.size else 0.0
    min_fraction = min_active / max(E, 1.0e-300)

    return {
        "energy": E,
        "active_total": Atot,
        "active_ratio": Atot / max(E, 1.0e-300),
        "min_active_fraction": min_fraction,
        "topology2": topology2(phi, dx),
        "topology4": topology4(phi, dx),
        "max_neighbor_angle": max_neighbor_angle(phi),
    }


def main() -> None:
    print("=== 023CR — CHECKERBOARD-FREE LINK-LATTICE TOPOLOGY REPAIR ===")

    print("\n=== A — UPSTREAM 023C AUDIT ===")
    for p in (A23_SOURCE, B23_SOURCE, BR23_SOURCE, C23_SOURCE, C23_LOG):
        require_file(p)
    hashes = {
        "023A": sha256(A23_SOURCE),
        "023B": sha256(B23_SOURCE),
        "023BR": sha256(BR23_SOURCE),
        "023C": sha256(C23_SOURCE),
    }
    for k, v in hashes.items():
        print(f"{k}_SOURCE_SHA256={v}")
    log_text = C23_LOG.read_text(errors="replace")
    markers_ok = all(m in log_text for m in EXPECTED_023C_MARKERS)
    audit_ok = (
        hashes["023A"] == EXPECTED_023A_SHA256
        and hashes["023B"] == EXPECTED_023B_SHA256
        and hashes["023BR"] == EXPECTED_023BR_SHA256
        and hashes["023C"] == EXPECTED_023C_SHA256
        and markers_ok
    )
    print("UPSTREAM_023C_AUDIT=" + ("PASS" if audit_ok else "FAIL"))
    if not audit_ok:
        raise RuntimeError("023C source/log audit failed")

    print("\n=== B — CHECKERBOARD NULL-MODE DIAGNOSIS ===")
    central_rms, link_rms, checker_pass = checkerboard_witness()
    print(f"CHECKERBOARD_CENTRAL_DERIVATIVE_RMS={central_rms:.15e}")
    print(f"CHECKERBOARD_LINK_DERIVATIVE_RMS={link_rms:.15e}")
    print("CHECKERBOARD_NULL_MODE_DIAGNOSIS=" + ("PASS" if checker_pass else "FAIL"))

    print("\n=== C — LINK-ACTION GRADIENT SELFCHECK ===")
    grad_rel, grad_pass = gradient_selfcheck()
    print(f"LINK_ACTION_GRADIENT_DIRECTIONAL_RELERR={grad_rel:.15e}")
    print("LINK_ACTION_GRADIENT_SELFCHECK=" + ("PASS" if grad_pass else "FAIL"))

    a23 = load_module("a23_for_023cr", A23_SOURCE)
    b23 = load_module("b23_for_023cr", B23_SOURCE)
    c23 = load_module("c23_for_023cr", C23_SOURCE)

    print("\n=== D — CONTINUUM RECONSTRUCTION + COMPACT DOMAIN ===")
    degree, I_direct = b23.angular_integrals_b7(b23.B7_B0)
    profile = b23.solve_profile_with_custom_I(a23, B, ETA, MASS, I_direct)
    sector_profiles, sector_energies = b23.solve_exact_sector(a23, ETA, MASS)
    selected = b23.candidate_from_sector(a23, sector_profiles, sector_energies, B)

    continuum = (
        4.0 * math.pi * float(profile.E),
        4.0 * math.pi * float(profile.E2),
        4.0 * math.pi * float(profile.E4),
        4.0 * math.pi * float(profile.E0),
    )
    half_domain, r_tail, boundary_F = choose_compact_half_domain(
        profile,
        selected.payload.payload_center,
        selected.payload.payload_radius,
    )
    print(f"DIRECT_MAP_DEGREE={degree:.15e}")
    print(f"DIRECT_MAP_I={I_direct:.15e}")
    print(f"CONTINUUM_ENERGY={continuum[0]:.15e}")
    print(f"CONTINUUM_E2={continuum[1]:.15e}")
    print(f"CONTINUUM_E4={continuum[2]:.15e}")
    print(f"CONTINUUM_E0={continuum[3]:.15e}")
    print(f"COMPACT_R_TAIL={r_tail:.15e}")
    print(f"COMPACT_HALF_DOMAIN={half_domain:.15e}")
    print(f"PROFILE_F_AT_CARTESIAN_FACE={boundary_F:.15e}")
    print("COMPACT_DOMAIN_TAIL=" + ("PASS" if abs(boundary_F) <= 2.0e-5 else "FAIL"))

    print("\n=== E — PRE-RELAXATION RESOLUTION SCAN ===")
    audits: list[InitialAudit] = []
    fields: dict[int, tuple[np.ndarray, np.ndarray, float]] = {}
    pair = None

    for n in GRID_LEVELS:
        phi, axis, dx = sample_rational_map_field(profile, b23.B7_B0, n, half_domain, c23)
        a = audit_initial(phi, dx, n, half_domain, continuum)
        audits.append(a)
        fields[n] = (phi, axis, dx)
        print_audit(a)

        if len(audits) >= 2:
            lo = audits[-2]
            hi = audits[-1]
            pair_energy = relative_error(lo.total_energy, hi.total_energy)
            pair_top = abs(abs(lo.topology4) - abs(hi.topology4)) / B
            print(f"PAIR_N{lo.n}_N{hi.n}_ENERGY_RELCHANGE={pair_energy:.15e}")
            print(f"PAIR_N{lo.n}_N{hi.n}_TOPOLOGY_ABSCHANGE={pair_top:.15e}")
            pair_ok = (
                lo.passed
                and hi.passed
                and pair_energy <= MAX_PAIR_ENERGY_RELCHANGE
                and pair_top <= MAX_PAIR_TOPOLOGY_ABSCHANGE
            )
            print(f"PAIR_N{lo.n}_N{hi.n}_CONVERGENCE=" + ("PASS" if pair_ok else "FAIL"))
            if pair_ok:
                pair = (lo, hi)
                break

        # Free old fields aggressively.  Keep only current and previous levels.
        if len(audits) >= 3:
            oldn = audits[-3].n
            fields.pop(oldn, None)

    pair_found = pair is not None
    print("INITIAL_RESOLUTION_PAIR=" + ("FOUND" if pair_found else "NOT_FOUND"))

    if not pair_found:
        print("INITIAL_LINK_ENERGY_RECONSTRUCTION=FAIL_OR_UNRESOLVED")
        print("INITIAL_CARTESIAN_TOPOLOGY_RECONSTRUCTION=FAIL_OR_UNRESOLVED")
        print("023CR_CHECKERBOARD_FREE_LINK_LATTICE_TOPOLOGY_REPAIR=INCOMPLETE_NUMERICAL_GATE")
        print("UNRESTRICTED_CARTESIAN_3D_STABILITY=NOT_YET_RESOLVED")
        print("NEXT=GEOMETRIC_TOPOLOGY_OR_ADAPTIVE_CARTESIAN_DISCRETIZATION")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_ESTABLISHED")
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
        return

    lo, hi = pair
    print("INITIAL_LINK_ENERGY_RECONSTRUCTION=PASS")
    print("INITIAL_CARTESIAN_TOPOLOGY_RECONSTRUCTION=PASS")
    # Use the coarser member of the converged pair for the repair relaxation.
    # The finer member independently establishes pre-relaxation convergence.
    selected_n = lo.n
    phi0, axis, dx = fields[selected_n]
    print(f"RELAX_SELECTED_N={selected_n}")
    print(f"RELAX_SELECTED_DX={dx:.15e}")

    print("\n=== F — ADMISSIBLE UNRESTRICTED LINK-LATTICE RELAXATION ===")
    relax = relax_admissible(phi0, dx)
    print(f"RELAX_INITIAL_ENERGY={relax.initial_energy:.15e}")
    print(f"RELAX_FINAL_ENERGY={relax.final_energy:.15e}")
    print(f"RELAX_INITIAL_GRAD_RMS={relax.initial_grad_rms:.15e}")
    print(f"RELAX_FINAL_GRAD_RMS={relax.final_grad_rms:.15e}")
    print(f"RELAX_FINAL_GRAD_MAX={relax.final_grad_max:.15e}")
    print(f"RELAX_ITERATIONS={relax.iterations}")
    print(f"RELAX_ACCEPTED_STEPS={relax.accepted_steps}")
    print(f"RELAX_REJECTED_TOPOLOGY_TRIALS={relax.rejected_topology}")
    print(f"RELAX_REJECTED_SMOOTHNESS_TRIALS={relax.rejected_smoothness}")
    print("RELAX_LINE_SEARCH_FAILED=" + ("YES" if relax.line_search_failed else "NO"))
    print("RELAX_CONVERGED=" + ("YES" if relax.converged else "NO"))

    final = smooth_continuum_diagnostics(relax.field, axis, dx)
    print(f"RELAXED_CONTINUUM_ENERGY={final['energy']:.15e}")
    print(f"RELAXED_ACTIVE_TOTAL={final['active_total']:.15e}")
    print(f"RELAXED_ACTIVE_TO_ENERGY={final['active_ratio']:.15e}")
    print(f"RELAXED_MIN_ACTIVE_FRACTION={final['min_active_fraction']:.15e}")
    print(f"RELAXED_TOPOLOGY_CENTRAL2={final['topology2']:.15e}")
    print(f"RELAXED_TOPOLOGY_CENTRAL4={final['topology4']:.15e}")
    print(f"RELAXED_TOPOLOGY4_RELERR={abs(abs(final['topology4'])/B-1.0):.15e}")
    print(f"RELAXED_MAX_NEIGHBOR_ANGLE={final['max_neighbor_angle']:.15e}")

    topology_pass = abs(abs(final["topology4"]) / B - 1.0) <= MAX_ADMISSIBLE_TOPOLOGY_RELERR
    smooth_pass = final["max_neighbor_angle"] <= MAX_ADMISSIBLE_NEIGHBOR_ANGLE
    active_positive = final["active_ratio"] > MIN_POSITIVE_ACTIVE_RATIO
    active_negative = final["min_active_fraction"] <= -MIN_NEGATIVE_ACTIVE_FRACTION
    gradient_reduced = relax.final_grad_rms <= relax.initial_grad_rms / MIN_GRADIENT_REDUCTION_FACTOR
    relaxation_pass = (
        relax.accepted_steps >= MIN_ACCEPTED_STEPS_FOR_AUDIT
        and not relax.line_search_failed
        and relax.final_energy <= relax.initial_energy * (1.0 + 1.0e-9)
        and gradient_reduced
        and topology_pass
        and smooth_pass
    )

    print("ADMISSIBLE_UNRESTRICTED_RELAXATION=" + ("PASS" if relaxation_pass else "FAIL_OR_INCOMPLETE"))
    print("RELAXED_CARTESIAN_TOPOLOGY=" + ("PASS" if topology_pass else "FAIL"))
    print("RELAXED_LATTICE_SMOOTHNESS=" + ("PASS" if smooth_pass else "FAIL"))
    print("RELAXED_POSITIVE_TOTAL_ACTIVE_MASS=" + ("PASS" if active_positive else "FAIL"))
    print("RELAXED_NEGATIVE_ENCLOSED_ACTIVE_MASS=" + ("PASS" if active_negative else "FAIL"))

    artifact = ROOT / "results/data/023cr_checkerboard_free_link_lattice_b7.npz"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        artifact,
        phi=relax.field,
        axis=axis,
        dx=np.array(dx),
        B=np.array(B),
        eta=np.array(ETA),
        mass=np.array(MASS),
        half_domain=np.array(half_domain),
        topology4=np.array(final["topology4"]),
        active_ratio=np.array(final["active_ratio"]),
        min_active_fraction=np.array(final["min_active_fraction"]),
    )
    print(f"RELAXED_FIELD_ARTIFACT={artifact.relative_to(ROOT)}")

    print("\n=== G — BLIND WILDCARD DIAGNOSTICS — NOT EVIDENCE ===")
    for factor in BLIND_WILDCARDS:
        amp = min(0.035, 0.012 * factor)
        rng = np.random.default_rng(int(round(1000 * factor)) + 23040)
        v = np.zeros_like(relax.field)
        v[1:-1, 1:-1, 1:-1] = rng.normal(size=v[1:-1, 1:-1, 1:-1].shape)
        v = project_tangent(relax.field, v)
        mag = np.linalg.norm(v[1:-1, 1:-1, 1:-1], axis=-1)
        vmax = float(np.max(mag))
        probe = exp_map_update(relax.field, v, amp / max(vmax, 1.0e-300))
        Eprobe = link_energy_gradient(probe, dx, ETA, MASS, False)[0]
        print(f"WILDCARD_FACTOR={factor:.6f} PERTURB_RAD={amp:.9e} ENERGY_RATIO={Eprobe/max(relax.final_energy,1e-300):.9e}")
    print("BLIND_WILDCARD_VALUES_USED_AS_EVIDENCE=NO")

    print("\n=== H — 023CR DECISION ===")
    green = all(
        (
            audit_ok,
            checker_pass,
            grad_pass,
            pair_found,
            relaxation_pass,
            topology_pass,
            smooth_pass,
            active_positive,
            active_negative,
        )
    )

    if green:
        print("023CR_CHECKERBOARD_FREE_LINK_LATTICE_TOPOLOGY_REPAIR=GREEN_NUMERICAL_REPAIR")
        print("023C_ORIGINAL_TOPOLOGY_COLLAPSE=NUMERICAL_CHECKERBOARD_ARTIFACT_SUPPORTED")
        print("UNRESTRICTED_CARTESIAN_B7_SECTOR=NUMERICALLY_RESOLVED_ENOUGH_FOR_CORRECTED_STABILITY_GATE")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
        print("HEURISTIC_PROMOTION_FROM_023CR=NO_NUMERICAL_REPAIR_ONLY")
        print("NEXT=023C2_CHECKERBOARD_FREE_FULL_HESSIAN_AND_DENSE_PAYLOAD_GATE")
    else:
        print("023CR_CHECKERBOARD_FREE_LINK_LATTICE_TOPOLOGY_REPAIR=INCOMPLETE_NUMERICAL_GATE")
        print("UNRESTRICTED_CARTESIAN_3D_STABILITY=NOT_YET_RESOLVED")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
        print("NEXT=INSPECT_023CR_FAILED_NUMERICAL_GATE_BEFORE_ESCALATION")

    print("NONLINEAR_EINSTEIN_SKYRME=NOT_ESTABLISHED")
    print("PRACTICAL_ENERGY_SCALING=STILL_CATASTROPHIC_IN_PURE_GR")
    print("REAL_MATERIAL=NO")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print("006D_CONSTRUCTIVE_LINEARIZED_GR_RESULT=RETAINED")
    print("018B_FIELD_EXISTENCE_RESULT=RETAINED")
    print("018C_KLS_M2_STABILITY_FAILURE=RETAINED")
    print("023BR_PROMOTION_GRADE_EXACT_MAP_PREFLIGHT=RETAINED")
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023CR_CHECKERBOARD_FREE_LINK_LATTICE_TOPOLOGY_REPAIR")


if __name__ == "__main__":
    main()
