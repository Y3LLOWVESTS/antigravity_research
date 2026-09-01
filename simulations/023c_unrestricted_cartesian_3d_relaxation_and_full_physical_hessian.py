#!/usr/bin/env python3
"""023C — unrestricted Cartesian 3D relaxation and full physical Hessian gate.

PURPOSE
-------
Test the strongest surviving false-core Skyrmion candidate outside the
rational-map ansatz that produced it.

023BR promoted the existing B=7, eta=0.4, m=8 candidate to a robust exact-map
field preflight.  It repaired the active-trace numerical diagnostic, selected
by worst-case maximin robustness, and demonstrated outward finite-payload
linearized gravity in a dense 320-direction orientation sphere.

That result remains restricted to the rational-map field class.  The next
qualitative accomplishment is therefore not another parameter scan.  It is a
Cartesian-field stability test in which every interior lattice site can move
independently on SU(2) ~= S^3.

SCIENTIFIC QUESTION
-------------------
Does the 023BR B=7 false-core Skyrmion remain a stationary, topologically
resolved, finite-payload-repulsive local minimum when released into the full
three-dimensional Cartesian field space?

FIELD REPRESENTATION
--------------------
Write

    U = sigma I + i pi_a tau_a,

with the pointwise constraint

    sigma^2 + pi_1^2 + pi_2^2 + pi_3^2 = 1.

The field is represented by the unit four-vector

    phi = (sigma, pi_1, pi_2, pi_3).

The boundary is fixed to the true vacuum

    phi_boundary = (1,0,0,0).

MODEL
-----
The continuum static energy density in the project normalization is

    e_2 = sum_i d_i phi . d_i phi,

    e_4 = sum_(i<j) [
              |d_i phi|^2 |d_j phi|^2
              - (d_i phi . d_j phi)^2
          ],

    V = m^2 (1-sigma) (1+eta sigma),

    rho = e_2 + e_4 + V.

For the rational-map orthonormal derivative eigenvalues (a,b,b), these reduce
exactly to the 023B expressions

    e_2 = a + 2b,
    e_4 = 2ab + b^2.

The general Cartesian stress tensor is reconstructed as

    T_ij =
        2 g_ij - e_2 delta_ij
        + 2[(tr g) g_ij - (g^2)_ij]
        - e_4 delta_ij
        - V delta_ij,

where

    g_ij = d_i phi . d_j phi.

Therefore the unrestricted active trace is again

    S = rho + tr(T) = 2(e_4 - V).

This identity is checked numerically after relaxation.

DISCRETIZATION
--------------
Use a symmetric second-order central-difference Cartesian lattice with fixed
Dirichlet vacuum boundary values.  The discrete energy is evaluated at all
interior sites.  Its gradient is implemented by the exact adjoint of those
central-difference operators, then projected onto the tangent space of S^3.

Before any physics result is accepted, the code checks the analytic discrete
gradient against a centered finite-difference directional derivative on a
small synthetic field.

UNRESTRICTED RELAXATION
-----------------------
The exact B=7 rational-map field is sampled onto the Cartesian lattice only as
an initial condition.  Thereafter every interior site is free to move in all
three physical tangent directions.

Relaxation uses Riemannian nonlinear conjugate gradient with:

- pointwise S^3 exponential-map updates;
- Armijo backtracking;
- fixed vacuum boundary;
- no rational-map constraint;
- no imposed icosahedral symmetry;
- no fixed radial profile.

A smooth deterministic off-ansatz perturbation is separately relaxed on the
lower-resolution grid to test whether the same basin is recovered.

TOPOLOGY
--------
The Cartesian baryon number is independently reconstructed from

    B = -(1/(2 pi^2)) integral det(phi,d_x phi,d_y phi,d_z phi) d^3x,

with the sign convention calibrated by the initial B=7 field.

The run also reports the maximum nearest-neighbor field-space angle.  A
configuration whose topology appears favorable only on an under-resolved
lattice is not promoted.

FULL PHYSICAL HESSIAN
---------------------
At the relaxed Cartesian state, construct an orthonormal three-vector tangent
basis at every interior lattice site.  This spans the COMPLETE physical
lattice tangent space; no rational-map or symmetry restriction remains.

The covariant Hessian is applied matrix-free by centered finite differences of
the projected Riemannian gradient along S^3 geodesics.  scipy.sparse.linalg.eigsh
then targets the lowest algebraic eigenvalues of this full operator.

The code also performs:

- a Hessian bilinear self-adjointness check;
- direct second-energy-difference reconstruction along the lowest mode;
- identification of overlaps with the three exact global isorotation zero
  modes when numerically relevant.

A significant negative eigenvalue is a direct falsifier.

FINITE-PAYLOAD GRAVITY
----------------------
After unrestricted relaxation, reconstruct

    S(x) = 2(e_4 - V)

on the Cartesian lattice and re-evaluate the same uniform spherical payload
geometry inherited from the 023BR selected candidate.

The payload-volume average uses the exact Newton shell-theorem kernel from
023BR.  A 320-direction deterministic Fibonacci sphere is tested.

PROMOTION CONDITION
-------------------
023C is GREEN only if all of the following survive together:

    UPSTREAM_023BR_AUDIT=PASS
    DISCRETE_GRADIENT_SELFCHECK=PASS
    CARTESIAN_GRID_RESOLUTION=PASS
    INITIAL_CARTESIAN_ENERGY_RECONSTRUCTION=PASS
    INITIAL_CARTESIAN_TOPOLOGY=PASS
    UNRESTRICTED_PRIMARY_RELAXATION=PASS
    OFF_ANSATZ_BASIN_RETURN=PASS
    RELAXED_CARTESIAN_TOPOLOGY=PASS
    RELAXED_POINTWISE_DEC=PASS
    RELAXED_ACTIVE_TRACE_IDENTITY=PASS
    RELAXED_NEGATIVE_ENCLOSED_ACTIVE_MASS=PASS
    RELAXED_POSITIVE_TOTAL_ACTIVE_MASS=PASS
    RELAXED_DENSE_FINITE_PAYLOAD_OUTWARD=PASS
    RELAXED_LOW_PRIMARY_CONVERGENCE=PASS
    FULL_TANGENT_HESSIAN_SELF_ADJOINTNESS=PASS
    FULL_PHYSICAL_HESSIAN=PASS_NO_SIGNIFICANT_NEGATIVE_MODE
    LOWEST_MODE_DIRECT_CURVATURE=PASS

A GREEN result supports only

    UNRESTRICTED_CARTESIAN_3D_STABLE_TOPOLOGICAL_REPULSIVE_FIELD.

It would authorize 023D weak-gravity/self-consistent Einstein-Skyrme
continuation.  It does not establish nonlinear gravity or practical energy.

FALSIFIERS
----------
Any of the following blocks 023D:

- relaxation unwinds or changes B materially;
- an off-ansatz perturbation runs to a distinct lower-energy/fission basin;
- a significant negative full-tangent Hessian eigenvalue appears;
- DEC or the active-trace reconstruction fails;
- negative enclosed active mass disappears;
- any dense payload orientation becomes inward;
- the result is not resolved or does not converge with lattice refinement.

STOP RULE
---------
If a robust negative Cartesian mode is found, preserve it as a stability
falsification and do not rescue the branch with arbitrary rigidity or added
stabilizer sectors.

If the only blocker is lattice resolution or Hessian numerical convergence,
perform one targeted 023CR numerical repair before interpreting it as a
physical failure.

If GREEN, proceed directly to

    023D_VALIDATED_WEAK_GRAVITY_EINSTEIN_SKYRME_CONTINUATION.

APPROXIMATION LEVEL
-------------------
Flat-spacetime Skyrme matter fields plus static linearized-GR gravity for the
payload observable.  The matter field itself is unrestricted Cartesian 3D.
Einstein backreaction is not included in this run.

CLAIM BOUNDARIES
----------------
This file does NOT establish:

- a nonlinear Einstein-Skyrme solution;
- practical energy scaling;
- a laboratory material;
- an experimental antigravity signal;
- a practical antigravity device;
- discovery of new physics.

RELATED FILES
-------------
    simulations/023a_topological_false_core_multiskyrmion_gr_repulsion_gate.py
    simulations/023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.py
    simulations/023br_promotion_grade_exact_map_robustness_repair.py

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023C_UNRESTRICTED_CARTESIAN_3D_RELAXATION_AND_FULL_PHYSICAL_HESSIAN
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib.util
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.sparse.linalg import LinearOperator, ArpackNoConvergence, eigsh


ROOT = Path(__file__).resolve().parents[1]

A23_SOURCE = ROOT / "simulations/023a_topological_false_core_multiskyrmion_gr_repulsion_gate.py"
B23_SOURCE = ROOT / "simulations/023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.py"
BR23_SOURCE = ROOT / "simulations/023br_promotion_grade_exact_map_robustness_repair.py"
BR23_LOG = ROOT / "results/logs/023br_promotion_grade_exact_map_robustness_repair.log"

EXPECTED_023A_SHA256 = "0087a5d2b4f93667308cabf4c3c498200ed29381e9493acf21714df7d8e11c9b"
EXPECTED_023B_SHA256 = "6bf99785e67cfe1b2dfcb460bc3145a24115e25949e112f8480a89c880a2803c"
EXPECTED_023BR_SHA256 = "e72d56767ae9a0ec8accdbfc95034425ecd30f81013d2cb4682f7555dd61a7c1"

EXPECTED_023BR_MARKERS = (
    "023BR_PROMOTION_GRADE_EXACT_MAP_ROBUSTNESS_REPAIR=GREEN",
    "MAXIMIN_SELECTED_B=7",
    "MAXIMIN_SELECTED_ETA=4.000000000000000e-01",
    "MAXIMIN_SELECTED_M=8.000000000000000e+00",
    "POINTWISE_ACTIVE_TRACE=PASS_SCALED_AND_HIGH_PRECISION",
    "DENSE_ORIENTATION_FINITE_PAYLOAD_OUTWARD=PASS",
    "RATIONAL_MAP_SHAPE_CURVATURE=PASS",
)

B = 7
ETA = 0.40
MASS = 8.0
DENSE_ORIENTATION_N = 320

# Cartesian resolution policy.
MIN_GRID_N = 31
MAX_PRIMARY_N = 53
MAX_HESSIAN_N = 43
TARGET_POINTS_PER_WALL = 4.5
MIN_PRIMARY_POINTS_PER_WALL = 3.5
MIN_HESSIAN_POINTS_PER_WALL = 2.8

# Lattice reconstruction / topology tolerances.
MAX_INITIAL_ENERGY_RELERR = 8.0e-2
MAX_TOPOLOGY_RELERR = 6.0e-2
MAX_NEIGHBOR_ANGLE = 1.20
MIN_NEGATIVE_ACTIVE_FRACTION = 1.0e-2
MIN_POSITIVE_ACTIVE_RATIO = 0.65
MAX_POSITIVE_ACTIVE_RATIO = 1.35
MIN_DEC_MARGIN = -2.0e-8
MAX_ACTIVE_TRACE_SCALED = 2.0e-10

# Relaxation gates.
RELAX_MAX_ITER_LOW = 180
RELAX_MAX_ITER_PRIMARY = 260
RELAX_GRAD_RMS_TOL = 3.0e-3
RELAX_GRAD_MAX_TOL = 5.0e-2
RELAX_MAX_POINT_ROTATION = 0.12
MAX_RELAX_ENERGY_INCREASE = 2.0e-8
MAX_BASIN_ENERGY_RELERR = 8.0e-3
PERTURB_AMPLITUDE_RAD = 0.045

# Low/primary convergence.
MAX_RELAXED_ENERGY_LOW_PRIMARY_RELERR = 7.5e-2
MAX_ACTIVE_FRACTION_LOW_PRIMARY_ABS = 8.0e-3

# Hessian gates.
HESSIAN_K = 14
HESSIAN_NCV = 30
HESSIAN_TOL = 3.0e-3
HESSIAN_MAXITER = 220
HESSIAN_POINT_ANGLE = 1.5e-4
MAX_HESSIAN_BILINEAR_ASYMMETRY = 5.0e-3
HESSIAN_SIGNIFICANT_NEGATIVE_REL = 2.5e-3
DIRECT_CURVATURE_NEGATIVE_REL = 4.0e-3

# Dense payload convergence / sign.
MIN_DENSE_RADIAL_OUTWARD = 0.0

# Blind wildcard values are diagnostics only and are never selection inputs.
BLIND_WILDCARDS = (1.6, 1.875, 3.125, 0.625, 5.0)


@dataclass
class LatticeDiagnostics:
    """Diagnostics for one Cartesian field."""

    energy: float
    e2: float
    e4: float
    e0: float
    active_total: float
    active_ratio: float
    min_active_fraction: float
    topology_signed: float
    topology_abs: float
    topology_relerr: float
    max_neighbor_angle: float
    min_dec_margin: float
    max_active_trace_scaled: float
    stress_divergence_scaled: float


@dataclass
class RelaxResult:
    """One unrestricted Riemannian relaxation result."""

    field: np.ndarray
    initial_energy: float
    final_energy: float
    initial_grad_rms: float
    final_grad_rms: float
    final_grad_max: float
    iterations: int
    accepted_steps: int
    converged: bool
    line_search_failed: bool


@dataclass
class PayloadAudit:
    """Dense finite-payload result from a Cartesian source."""

    min_radial: float
    max_radial: float
    mean_radial: float
    max_transverse: float
    max_transverse_over_radial: float
    worst_orientation: np.ndarray
    all_outward: bool


def sha256(path: Path) -> str:
    """Return SHA-256 of one file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_file(path: Path) -> None:
    """Fail closed if one required file is missing."""

    if not path.exists():
        raise RuntimeError(f"Missing required file: {path}")


def require_markers(path: Path, markers: tuple[str, ...]) -> None:
    """Fail closed unless all required markers are present."""

    require_file(path)
    text = path.read_text(errors="replace")
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise RuntimeError("Missing required upstream marker(s): " + ", ".join(missing))


def load_module(name: str, path: Path):
    """Import one repository simulation without invoking main()."""

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


def normalize_field(phi: np.ndarray) -> np.ndarray:
    """Normalize a four-vector field pointwise."""

    norm = np.linalg.norm(phi, axis=-1, keepdims=True)
    return phi / np.maximum(norm, 1.0e-300)


def enforce_vacuum_boundary(phi: np.ndarray) -> None:
    """Set all six boundary faces to the true vacuum."""

    vacuum = np.array([1.0, 0.0, 0.0, 0.0])
    phi[0, :, :, :] = vacuum
    phi[-1, :, :, :] = vacuum
    phi[:, 0, :, :] = vacuum
    phi[:, -1, :, :] = vacuum
    phi[:, :, 0, :] = vacuum
    phi[:, :, -1, :] = vacuum


def project_tangent(phi: np.ndarray, vec: np.ndarray) -> np.ndarray:
    """Project ambient four-vectors onto the S^3 tangent bundle."""

    dot = np.sum(phi * vec, axis=-1, keepdims=True)
    return vec - dot * phi


def exp_map_update(phi: np.ndarray, tangent: np.ndarray, alpha: float) -> np.ndarray:
    """Apply a pointwise S^3 exponential-map update to interior sites."""

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
    """False-core potential written directly in sigma=cos(F)."""

    return mass * mass * (1.0 - sigma) * (1.0 + eta * sigma)


def dpotential_dsigma(sigma: np.ndarray, eta: float, mass: float) -> np.ndarray:
    """Derivative of the false-core potential with respect to sigma."""

    return mass * mass * ((eta - 1.0) - 2.0 * eta * sigma)


def central_derivatives(phi: np.ndarray, dx: float):
    """Return central Cartesian derivatives on interior sites."""

    inv = 1.0 / (2.0 * dx)
    qx = (phi[2:, 1:-1, 1:-1] - phi[:-2, 1:-1, 1:-1]) * inv
    qy = (phi[1:-1, 2:, 1:-1] - phi[1:-1, :-2, 1:-1]) * inv
    qz = (phi[1:-1, 1:-1, 2:] - phi[1:-1, 1:-1, :-2]) * inv
    return qx, qy, qz


def metric_terms(qx: np.ndarray, qy: np.ndarray, qz: np.ndarray):
    """Return derivative Gram components and e2/e4."""

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


def energy_and_euclidean_gradient(
    phi: np.ndarray,
    dx: float,
    eta: float,
    mass: float,
    need_gradient: bool = True,
):
    """Return discrete energy, components, and exact Euclidean gradient.

    The energy is defined on central-difference interior sites.  When a
    gradient is requested, derivative contributions are accumulated using the
    exact adjoint of those central-difference operators.
    """

    qx, qy, qz = central_derivatives(phi, dx)
    gxx, gyy, gzz, gxy, gxz, gyz, e2, e4 = metric_terms(qx, qy, qz)

    sigma = phi[1:-1, 1:-1, 1:-1, 0]
    V = potential_sigma(sigma, eta, mass)
    dV = dpotential_dsigma(sigma, eta, mass)

    volume = dx**3
    E2 = float(np.sum(e2) * volume)
    E4 = float(np.sum(e4) * volume)
    E0 = float(np.sum(V) * volume)
    E = E2 + E4 + E0

    if not need_gradient:
        return E, E2, E4, E0, None

    # P_i = d(e2+e4)/d(q_i).
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
    coeff = 1.0 / (2.0 * dx)

    grad[2:, 1:-1, 1:-1] += coeff * px
    grad[:-2, 1:-1, 1:-1] -= coeff * px

    grad[1:-1, 2:, 1:-1] += coeff * py
    grad[1:-1, :-2, 1:-1] -= coeff * py

    grad[1:-1, 1:-1, 2:] += coeff * pz
    grad[1:-1, 1:-1, :-2] -= coeff * pz

    grad[1:-1, 1:-1, 1:-1, 0] += dV
    grad *= volume

    # Boundary values are fixed and are not physical variables.
    grad[0, :, :, :] = 0.0
    grad[-1, :, :, :] = 0.0
    grad[:, 0, :, :] = 0.0
    grad[:, -1, :, :] = 0.0
    grad[:, :, 0, :] = 0.0
    grad[:, :, -1, :] = 0.0

    return E, E2, E4, E0, grad


def riemannian_gradient_density(phi: np.ndarray, dx: float, eta: float, mass: float):
    """Return energy, components, and tangent gradient per coordinate volume."""

    E, E2, E4, E0, grad = energy_and_euclidean_gradient(phi, dx, eta, mass, True)
    assert grad is not None
    gd = grad / (dx**3)
    gd = project_tangent(phi, gd)
    gd[0, :, :, :] = 0.0
    gd[-1, :, :, :] = 0.0
    gd[:, 0, :, :] = 0.0
    gd[:, -1, :, :] = 0.0
    gd[:, :, 0, :] = 0.0
    gd[:, :, -1, :] = 0.0
    return E, E2, E4, E0, gd


def gradient_selfcheck() -> tuple[float, bool]:
    """Compare the analytic discrete gradient with an energy finite difference."""

    n = 7
    L = 1.4
    dx = 2.0 * L / (n - 1)
    axis = np.linspace(-L, L, n)
    X, Y, Z = np.meshgrid(axis, axis, axis, indexing="ij")

    pion = np.zeros((n, n, n, 3))
    envelope = (1.0 - (X / L) ** 2) * (1.0 - (Y / L) ** 2) * (1.0 - (Z / L) ** 2)
    envelope = np.maximum(envelope, 0.0)
    pion[..., 0] = 0.16 * envelope * np.sin(math.pi * X / L)
    pion[..., 1] = 0.12 * envelope * np.sin(math.pi * Y / L)
    pion[..., 2] = 0.10 * envelope * np.sin(math.pi * Z / L)

    pion2 = np.sum(pion * pion, axis=-1)
    phi = np.zeros((n, n, n, 4))
    phi[..., 0] = np.sqrt(np.maximum(1.0 - pion2, 1.0e-14))
    phi[..., 1:] = pion
    enforce_vacuum_boundary(phi)
    phi = normalize_field(phi)

    _, _, _, _, grad = energy_and_euclidean_gradient(phi, dx, ETA, MASS, True)
    assert grad is not None

    rng = np.random.default_rng(23031)
    v = np.zeros_like(phi)
    v[1:-1, 1:-1, 1:-1] = rng.normal(size=v[1:-1, 1:-1, 1:-1].shape)
    v = project_tangent(phi, v)
    norm = math.sqrt(float(np.sum(v * v)))
    v /= max(norm, 1.0e-300)

    eps = 2.0e-6
    plus = exp_map_update(phi, v, eps)
    minus = exp_map_update(phi, v, -eps)
    Eplus = energy_and_euclidean_gradient(plus, dx, ETA, MASS, False)[0]
    Eminus = energy_and_euclidean_gradient(minus, dx, ETA, MASS, False)[0]
    finite = (Eplus - Eminus) / (2.0 * eps)
    analytic = float(np.sum(grad * v))
    rel = abs(finite - analytic) / max(abs(finite), abs(analytic), 1.0e-12)
    return rel, rel <= 2.0e-6


def profile_crossing_radius(profile, fraction_pi: float) -> float:
    """Interpolate radius where monotone F crosses fraction*pi."""

    target = float(fraction_pi * math.pi)
    F = np.asarray(profile.F, dtype=float)
    r = np.asarray(profile.r, dtype=float)
    return float(np.interp(target, F[::-1], r[::-1]))


def choose_cartesian_domain(profile, payload_center: float, payload_radius: float):
    """Choose domain and adaptive lattice sizes from the actual wall thickness."""

    r90 = profile_crossing_radius(profile, 0.90)
    r10 = profile_crossing_radius(profile, 0.10)
    wall_width = max(r10 - r90, 1.0e-3)

    F = np.asarray(profile.F)
    r = np.asarray(profile.r)
    tail_mask = np.where(F <= 1.0e-5)[0]
    r_tail = float(r[tail_mask[0]]) if len(tail_mask) else float(r[-1])

    shell = float(profile.shell_radius)
    half_domain = max(
        1.18 * r_tail,
        shell + 5.0 * wall_width,
        1.08 * (float(payload_center) + float(payload_radius)),
    )
    half_domain = min(half_domain, 0.92 * float(r[-1]))

    target_dx = wall_width / TARGET_POINTS_PER_WALL
    n_req = int(math.ceil(2.0 * half_domain / max(target_dx, 1.0e-6))) + 1
    if n_req % 2 == 0:
        n_req += 1

    primary_n = min(max(n_req, MIN_GRID_N), MAX_PRIMARY_N)
    if primary_n % 2 == 0:
        primary_n -= 1

    low_n = max(MIN_GRID_N, primary_n - 10)
    if low_n % 2 == 0:
        low_n -= 1

    hessian_n = min(primary_n, MAX_HESSIAN_N)
    if hessian_n % 2 == 0:
        hessian_n -= 1

    def ppw(n: int) -> float:
        return wall_width / (2.0 * half_domain / (n - 1))

    return {
        "r90": r90,
        "r10": r10,
        "wall_width": wall_width,
        "r_tail": r_tail,
        "half_domain": half_domain,
        "low_n": low_n,
        "primary_n": primary_n,
        "hessian_n": hessian_n,
        "low_ppw": ppw(low_n),
        "primary_ppw": ppw(primary_n),
        "hessian_ppw": ppw(hessian_n),
    }


def b7_unit_vector_from_xyz(X: np.ndarray, Y: np.ndarray, Z: np.ndarray, b: float):
    """Return n_R for the published B=7 rational map on Cartesian points."""

    r = np.sqrt(X * X + Y * Y + Z * Z)
    denom_stereo = r + Z
    w = np.zeros_like(X, dtype=np.complex128)

    regular = np.abs(denom_stereo) > 1.0e-14 * np.maximum(r, 1.0)
    w[regular] = (X[regular] + 1j * Y[regular]) / denom_stereo[regular]

    p = b * w**6 - 7.0 * w**4 - b * w**2 - 1.0
    q = w * (w**6 + b * w**4 + 7.0 * w**2 - b)

    den = np.abs(p) ** 2 + np.abs(q) ** 2
    den = np.maximum(den, 1.0e-300)
    pqc = p * np.conjugate(q)

    nx = 2.0 * np.real(pqc) / den
    ny = 2.0 * np.imag(pqc) / den
    nz = (np.abs(q) ** 2 - np.abs(p) ** 2) / den

    # South stereographic pole: R -> 0 for this map, so n_R -> +z.
    south = (~regular) & (Z < 0.0)
    nx[south] = 0.0
    ny[south] = 0.0
    nz[south] = 1.0

    # At the spatial origin angular direction is irrelevant because sin(F)=0.
    origin = r <= 1.0e-14
    nx[origin] = 0.0
    ny[origin] = 0.0
    nz[origin] = 1.0

    norm = np.sqrt(nx * nx + ny * ny + nz * nz)
    nx /= np.maximum(norm, 1.0e-300)
    ny /= np.maximum(norm, 1.0e-300)
    nz /= np.maximum(norm, 1.0e-300)
    return nx, ny, nz


def sample_rational_map_field(profile, b_parameter: float, n: int, half_domain: float):
    """Sample the exact-map profile as an initial Cartesian SU(2) field."""

    axis = np.linspace(-half_domain, half_domain, n)
    dx = float(axis[1] - axis[0])
    X, Y, Z = np.meshgrid(axis, axis, axis, indexing="ij")
    r = np.sqrt(X * X + Y * Y + Z * Z)

    F = np.interp(
        r.ravel(),
        np.asarray(profile.r, dtype=float),
        np.asarray(profile.F, dtype=float),
        left=math.pi,
        right=0.0,
    ).reshape(r.shape)

    nx, ny, nz = b7_unit_vector_from_xyz(X, Y, Z, b_parameter)
    s = np.sin(F)

    phi = np.empty((n, n, n, 4), dtype=float)
    phi[..., 0] = np.cos(F)
    phi[..., 1] = s * nx
    phi[..., 2] = s * ny
    phi[..., 3] = s * nz
    phi = normalize_field(phi)
    enforce_vacuum_boundary(phi)
    return phi, axis, dx


def max_neighbor_angle(phi: np.ndarray) -> float:
    """Return maximum geodesic angle between nearest-neighbor field values."""

    maxima = []
    for a, b in (
        (phi[1:], phi[:-1]),
        (phi[:, 1:], phi[:, :-1]),
        (phi[:, :, 1:], phi[:, :, :-1]),
    ):
        dot = np.sum(a * b, axis=-1)
        maxima.append(float(np.max(np.arccos(np.clip(dot, -1.0, 1.0)))))
    return max(maxima)


def topology_charge(phi: np.ndarray, dx: float) -> float:
    """Reconstruct Cartesian baryon number from the four-vector Jacobian."""

    qx, qy, qz = central_derivatives(phi, dx)
    center = phi[1:-1, 1:-1, 1:-1]
    mat = np.stack([center, qx, qy, qz], axis=-1)
    det = np.linalg.det(mat)
    raw = -float(np.sum(det) * dx**3 / (2.0 * math.pi**2))
    return raw


def stress_and_local_diagnostics(phi: np.ndarray, dx: float, eta: float, mass: float):
    """Return energy/source/stress arrays on interior sites."""

    qx, qy, qz = central_derivatives(phi, dx)
    gxx, gyy, gzz, gxy, gxz, gyz, e2, e4 = metric_terms(qx, qy, qz)
    sigma = phi[1:-1, 1:-1, 1:-1, 0]
    V = potential_sigma(sigma, eta, mass)
    rho = e2 + e4 + V

    g = np.empty(e2.shape + (3, 3), dtype=float)
    g[..., 0, 0] = gxx
    g[..., 1, 1] = gyy
    g[..., 2, 2] = gzz
    g[..., 0, 1] = g[..., 1, 0] = gxy
    g[..., 0, 2] = g[..., 2, 0] = gxz
    g[..., 1, 2] = g[..., 2, 1] = gyz

    tr = e2
    g2 = np.einsum("...ik,...kj->...ij", g, g)
    eye = np.eye(3)
    stress = (
        2.0 * g
        - e2[..., None, None] * eye
        + 2.0 * (tr[..., None, None] * g - g2)
        - e4[..., None, None] * eye
        - V[..., None, None] * eye
    )

    active_from_stress = rho + np.trace(stress, axis1=-2, axis2=-1)
    active = 2.0 * (e4 - V)
    scale = (
        rho
        + np.sum(np.abs(np.linalg.eigvalsh(stress)), axis=-1)
        + 2.0 * e4
        + 2.0 * V
        + 1.0e-14
    )
    trace_scaled = np.abs(active_from_stress - active) / scale

    eig = np.linalg.eigvalsh(stress)
    dec_margin = rho - np.max(np.abs(eig), axis=-1)

    return {
        "e2": e2,
        "e4": e4,
        "V": V,
        "rho": rho,
        "stress": stress,
        "active": active,
        "dec_margin": dec_margin,
        "trace_scaled": trace_scaled,
    }


def stress_divergence_scaled(stress: np.ndarray, dx: float) -> float:
    """Return a dimensionless interior stress-divergence diagnostic."""

    if min(stress.shape[:3]) < 5:
        return math.inf

    inv = 1.0 / (2.0 * dx)
    # stress[..., i, j] with divergence_j = d_i T_ij.
    dxt = (stress[2:, 1:-1, 1:-1, 0, :] - stress[:-2, 1:-1, 1:-1, 0, :]) * inv
    dyt = (stress[1:-1, 2:, 1:-1, 1, :] - stress[1:-1, :-2, 1:-1, 1, :]) * inv
    dzt = (stress[1:-1, 1:-1, 2:, 2, :] - stress[1:-1, 1:-1, :-2, 2, :]) * inv
    div = dxt + dyt + dzt
    div_rms = math.sqrt(float(np.mean(np.sum(div * div, axis=-1))))
    stress_rms = math.sqrt(float(np.mean(np.sum(stress * stress, axis=(-2, -1)))))
    return div_rms / max(stress_rms / dx, 1.0e-300)


def lattice_diagnostics(phi: np.ndarray, axis: np.ndarray, dx: float, eta: float, mass: float):
    """Compute complete source/topology/DEC diagnostics for one field."""

    local = stress_and_local_diagnostics(phi, dx, eta, mass)
    volume = dx**3
    E2 = float(np.sum(local["e2"]) * volume)
    E4 = float(np.sum(local["e4"]) * volume)
    E0 = float(np.sum(local["V"]) * volume)
    E = E2 + E4 + E0
    active_weights = local["active"].ravel() * volume
    active_total = float(np.sum(active_weights))

    coords = axis[1:-1]
    X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")
    radii = np.sqrt(X * X + Y * Y + Z * Z).ravel()
    order = np.argsort(radii)
    cumulative = np.cumsum(active_weights[order])
    min_active_fraction = float(np.min(cumulative) / max(E, 1.0e-300))

    topo = topology_charge(phi, dx)
    topo_abs = abs(topo)
    topo_relerr = abs(topo_abs - B) / B

    return LatticeDiagnostics(
        energy=E,
        e2=E2,
        e4=E4,
        e0=E0,
        active_total=active_total,
        active_ratio=active_total / max(E, 1.0e-300),
        min_active_fraction=min_active_fraction,
        topology_signed=topo,
        topology_abs=topo_abs,
        topology_relerr=topo_relerr,
        max_neighbor_angle=max_neighbor_angle(phi),
        min_dec_margin=float(np.min(local["dec_margin"])),
        max_active_trace_scaled=float(np.max(local["trace_scaled"])),
        stress_divergence_scaled=stress_divergence_scaled(local["stress"], dx),
    )


def tangent_inner(a: np.ndarray, b: np.ndarray, dx: float) -> float:
    """L2 tangent inner product with coordinate-volume weight."""

    return float(np.sum(a[1:-1, 1:-1, 1:-1] * b[1:-1, 1:-1, 1:-1]) * dx**3)


def gradient_norms(g: np.ndarray) -> tuple[float, float]:
    """Return pointwise RMS and maximum tangent gradient norms."""

    gi = g[1:-1, 1:-1, 1:-1]
    n = np.linalg.norm(gi, axis=-1)
    return math.sqrt(float(np.mean(n * n))), float(np.max(n))


def relax_field(
    phi0: np.ndarray,
    dx: float,
    eta: float,
    mass: float,
    max_iter: int,
) -> RelaxResult:
    """Unrestricted Riemannian nonlinear-conjugate-gradient relaxation."""

    phi = phi0.copy()
    E, _, _, _, g = riemannian_gradient_density(phi, dx, eta, mass)
    g_rms0, _ = gradient_norms(g)
    direction = -g
    step = 0.08
    accepted = 0
    line_fail = False

    final_rms = g_rms0
    final_max = math.inf

    for iteration in range(1, max_iter + 1):
        final_rms, final_max = gradient_norms(g)
        if final_rms <= RELAX_GRAD_RMS_TOL and final_max <= RELAX_GRAD_MAX_TOL:
            return RelaxResult(
                field=phi,
                initial_energy=energy_and_euclidean_gradient(phi0, dx, eta, mass, False)[0],
                final_energy=E,
                initial_grad_rms=g_rms0,
                final_grad_rms=final_rms,
                final_grad_max=final_max,
                iterations=iteration - 1,
                accepted_steps=accepted,
                converged=True,
                line_search_failed=False,
            )

        # Ensure a descent direction.
        gd = tangent_inner(g, direction, dx)
        if not math.isfinite(gd) or gd >= 0.0:
            direction = -g
            gd = -tangent_inner(g, g, dx)

        max_dir = float(np.max(np.linalg.norm(direction[1:-1, 1:-1, 1:-1], axis=-1)))
        alpha = min(step, RELAX_MAX_POINT_ROTATION / max(max_dir, 1.0e-300))

        accepted_here = False
        trial = None
        Etrial = math.inf

        for _ in range(18):
            trial = exp_map_update(phi, direction, alpha)
            Etrial = energy_and_euclidean_gradient(trial, dx, eta, mass, False)[0]
            if Etrial <= E + 1.0e-4 * alpha * gd + MAX_RELAX_ENERGY_INCREASE:
                accepted_here = True
                break
            alpha *= 0.5

        if not accepted_here or trial is None:
            line_fail = True
            break

        old_phi = phi
        old_g = g
        old_direction = direction
        old_gg = tangent_inner(old_g, old_g, dx)

        phi = trial
        E, _, _, _, g = riemannian_gradient_density(phi, dx, eta, mass)
        accepted += 1

        transported_g = project_tangent(phi, old_g)
        transported_d = project_tangent(phi, old_direction)
        y = g - transported_g
        beta = max(0.0, tangent_inner(g, y, dx) / max(old_gg, 1.0e-300))
        beta = min(beta, 5.0)
        direction = -g + beta * transported_d

        if tangent_inner(g, direction, dx) >= -1.0e-6 * tangent_inner(g, g, dx):
            direction = -g

        step = min(max(alpha * 1.35, 1.0e-7), 2.0)

        # Free references to large old arrays promptly.
        del old_phi

    final_rms, final_max = gradient_norms(g)
    return RelaxResult(
        field=phi,
        initial_energy=energy_and_euclidean_gradient(phi0, dx, eta, mass, False)[0],
        final_energy=E,
        initial_grad_rms=g_rms0,
        final_grad_rms=final_rms,
        final_grad_max=final_max,
        iterations=max_iter if not line_fail else accepted,
        accepted_steps=accepted,
        converged=(final_rms <= RELAX_GRAD_RMS_TOL and final_max <= RELAX_GRAD_MAX_TOL),
        line_search_failed=line_fail,
    )


def smooth_off_ansatz_perturbation(phi: np.ndarray, amplitude: float, seed: int = 23032):
    """Apply a deterministic smooth unrestricted tangent perturbation."""

    rng = np.random.default_rng(seed)
    noise = rng.normal(size=phi.shape)
    for component in range(4):
        noise[..., component] = gaussian_filter(noise[..., component], sigma=1.6, mode="nearest")
    noise = project_tangent(phi, noise)
    interior = noise[1:-1, 1:-1, 1:-1]
    rms = math.sqrt(float(np.mean(np.sum(interior * interior, axis=-1))))
    noise /= max(rms, 1.0e-300)
    return exp_map_update(phi, noise, amplitude)


def fibonacci_sphere(n: int) -> np.ndarray:
    """Return deterministic approximately uniform unit vectors."""

    k = np.arange(n, dtype=float)
    golden = math.pi * (3.0 - math.sqrt(5.0))
    z = 1.0 - 2.0 * (k + 0.5) / n
    rxy = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    phi = golden * k
    vec = np.column_stack([rxy * np.cos(phi), rxy * np.sin(phi), z])
    return vec / np.linalg.norm(vec, axis=1)[:, None]


def analytic_uniform_sphere_payload_average(
    source_xyz: np.ndarray,
    source_weight: np.ndarray,
    centers: np.ndarray,
    payload_radius: float,
    batch_size: int = 16,
) -> np.ndarray:
    """Exact continuum payload-volume average of the Newton kernel."""

    result = np.zeros((len(centers), 3), dtype=float)
    r3 = float(payload_radius**3)
    for start in range(0, len(centers), batch_size):
        stop = min(start + batch_size, len(centers))
        q = source_xyz[None, :, :] - centers[start:stop, None, :]
        d2 = np.sum(q * q, axis=-1)
        d = np.sqrt(np.maximum(d2, 0.0))
        denom = np.where(d < payload_radius, r3, np.maximum(d2 * d, 1.0e-300))
        result[start:stop] = np.sum(
            source_weight[None, :, None] * q / denom[:, :, None], axis=1
        )
    return result


def payload_audit(phi: np.ndarray, axis: np.ndarray, dx: float, center_radius: float, payload_radius: float):
    """Dense finite-payload gravity audit from the unrestricted Cartesian source."""

    local = stress_and_local_diagnostics(phi, dx, ETA, MASS)
    active = local["active"]
    coords = axis[1:-1]
    X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")
    xyz = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    weight = active.ravel() * dx**3

    vectors = fibonacci_sphere(DENSE_ORIENTATION_N)
    centers = float(center_radius) * vectors
    avg = analytic_uniform_sphere_payload_average(xyz, weight, centers, float(payload_radius))
    radial = np.sum(avg * vectors, axis=1)
    transverse_vec = avg - radial[:, None] * vectors
    transverse = np.linalg.norm(transverse_vec, axis=1)
    worst = int(np.argmin(radial))
    ratio = transverse / np.maximum(radial, 1.0e-300)

    return PayloadAudit(
        min_radial=float(np.min(radial)),
        max_radial=float(np.max(radial)),
        mean_radial=float(np.mean(radial)),
        max_transverse=float(np.max(transverse)),
        max_transverse_over_radial=float(np.max(ratio)),
        worst_orientation=vectors[worst],
        all_outward=bool(np.all(radial > MIN_DENSE_RADIAL_OUTWARD)),
    )


def tangent_basis_householder(phi: np.ndarray) -> np.ndarray:
    """Return orthonormal 4x3 tangent bases at all interior sites."""

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

    # Numerical cleanup and diagnostic-quality normalization.
    for j in range(3):
        norm = np.linalg.norm(basis[:, :, j], axis=1)
        basis[:, :, j] /= np.maximum(norm[:, None], 1.0e-300)
    return basis


def tangent_components_to_field(u: np.ndarray, basis: np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
    """Expand packed 3-component tangent coordinates to an ambient field."""

    nsite = basis.shape[0]
    coeff = u.reshape(nsite, 3)
    vint = np.einsum("naj,nj->na", basis, coeff)
    full = np.zeros(shape, dtype=float)
    full[1:-1, 1:-1, 1:-1] = vint.reshape(shape[0] - 2, shape[1] - 2, shape[2] - 2, 4)
    return full


def tangent_field_to_components(v: np.ndarray, basis: np.ndarray) -> np.ndarray:
    """Project an ambient tangent field into packed local tangent coordinates."""

    vint = v[1:-1, 1:-1, 1:-1].reshape(-1, 4)
    coeff = np.einsum("naj,na->nj", basis, vint)
    return coeff.ravel()


def global_isorotation_modes(phi: np.ndarray, basis: np.ndarray) -> list[np.ndarray]:
    """Return packed infinitesimal global SO(3) pion-isorotation zero modes."""

    p = phi[1:-1, 1:-1, 1:-1].reshape(-1, 4)
    pi = p[:, 1:]
    modes = []
    axes = np.eye(3)
    for axis in axes:
        dpi = np.cross(np.broadcast_to(axis, pi.shape), pi)
        ambient = np.zeros_like(p)
        ambient[:, 1:] = dpi
        coeff = np.einsum("naj,na->nj", basis, ambient).ravel()
        norm = np.linalg.norm(coeff)
        if norm > 1.0e-12:
            modes.append(coeff / norm)
    return modes


def hessian_analysis(phi: np.ndarray, dx: float):
    """Compute the lowest full-tangent Cartesian Hessian spectrum matrix-free."""

    basis = tangent_basis_householder(phi)
    nsite = basis.shape[0]
    ndof = 3 * nsite
    shape = phi.shape

    def grad_components(field: np.ndarray) -> np.ndarray:
        _, _, _, _, g = riemannian_gradient_density(field, dx, ETA, MASS)
        # Project to the BASE tangent space for a covariant finite-difference
        # Hessian at a nearly stationary point.
        return tangent_field_to_components(g, basis)

    def matvec(u: np.ndarray) -> np.ndarray:
        u = np.asarray(u, dtype=float)
        v = tangent_components_to_field(u, basis, shape)
        max_point = float(np.max(np.linalg.norm(v[1:-1, 1:-1, 1:-1], axis=-1)))
        scale = HESSIAN_POINT_ANGLE / max(max_point, 1.0e-12)
        plus = exp_map_update(phi, v, scale)
        minus = exp_map_update(phi, v, -scale)
        gp = grad_components(plus)
        gm = grad_components(minus)
        return (gp - gm) / (2.0 * scale)

    op = LinearOperator((ndof, ndof), matvec=matvec, dtype=float)

    rng = np.random.default_rng(23033)
    asymmetries = []
    for _ in range(3):
        u = rng.normal(size=ndof)
        v = rng.normal(size=ndof)
        u /= np.linalg.norm(u)
        v /= np.linalg.norm(v)
        Hu = matvec(u)
        Hv = matvec(v)
        lhs = float(np.dot(u, Hv))
        rhs = float(np.dot(v, Hu))
        asymmetries.append(abs(lhs - rhs) / max(abs(lhs), abs(rhs), 1.0e-12))
    bilinear_asym = max(asymmetries)

    try:
        vals, vecs = eigsh(
            op,
            k=min(HESSIAN_K, ndof - 2),
            which="SA",
            tol=HESSIAN_TOL,
            maxiter=HESSIAN_MAXITER,
            ncv=min(HESSIAN_NCV, ndof - 1),
        )
        converged = True
    except ArpackNoConvergence as exc:
        vals = np.asarray(exc.eigenvalues if exc.eigenvalues is not None else [])
        vecs = np.asarray(exc.eigenvectors if exc.eigenvectors is not None else np.empty((ndof, 0)))
        converged = len(vals) >= 6

    if len(vals) == 0:
        return {
            "converged": False,
            "bilinear_asym": bilinear_asym,
            "eigenvalues": np.array([]),
            "lambda_min": math.nan,
            "spectral_scale": math.nan,
            "negative_significant": True,
            "zero_overlaps": [],
            "direct_rayleigh": [],
            "direct_curvature_pass": False,
        }

    order = np.argsort(vals)
    vals = vals[order]
    vecs = vecs[:, order]
    spectral_scale = max(float(np.max(np.abs(vals))), 1.0)
    lambda_min = float(vals[0])
    negative_significant = lambda_min < -HESSIAN_SIGNIFICANT_NEGATIVE_REL * spectral_scale

    zero_modes = global_isorotation_modes(phi, basis)
    zero_overlaps = []
    for col in range(min(vecs.shape[1], 6)):
        overlaps = [abs(float(np.dot(vecs[:, col], z))) for z in zero_modes]
        zero_overlaps.append(max(overlaps) if overlaps else 0.0)

    # Independent direct energy curvature along the numerically lowest mode.
    lowest = vecs[:, 0]
    vfield = tangent_components_to_field(lowest, basis, shape)
    max_point = float(np.max(np.linalg.norm(vfield[1:-1, 1:-1, 1:-1], axis=-1)))
    E0 = energy_and_euclidean_gradient(phi, dx, ETA, MASS, False)[0]
    direct = []
    for point_angle in (7.5e-4, 1.5e-3, 3.0e-3):
        t = point_angle / max(max_point, 1.0e-12)
        plus = exp_map_update(phi, vfield, t)
        minus = exp_map_update(phi, vfield, -t)
        Ep = energy_and_euclidean_gradient(plus, dx, ETA, MASS, False)[0]
        Em = energy_and_euclidean_gradient(minus, dx, ETA, MASS, False)[0]
        # H_density eigenvalue uses the unweighted coordinate inner product;
        # the energy second variation contains an overall dx^3.
        rayleigh = (Ep + Em - 2.0 * E0) / (t * t * dx**3)
        direct.append(float(rayleigh))

    direct_pass = min(direct) >= -DIRECT_CURVATURE_NEGATIVE_REL * spectral_scale

    return {
        "converged": converged,
        "bilinear_asym": bilinear_asym,
        "eigenvalues": vals,
        "lambda_min": lambda_min,
        "spectral_scale": spectral_scale,
        "negative_significant": negative_significant,
        "zero_overlaps": zero_overlaps,
        "direct_rayleigh": direct,
        "direct_curvature_pass": direct_pass,
    }


def print_diag(prefix: str, diag: LatticeDiagnostics) -> None:
    """Print one compact lattice diagnostic block."""

    print(f"{prefix}_ENERGY={diag.energy:.15e}")
    print(f"{prefix}_E2={diag.e2:.15e}")
    print(f"{prefix}_E4={diag.e4:.15e}")
    print(f"{prefix}_E0={diag.e0:.15e}")
    print(f"{prefix}_ACTIVE_TOTAL={diag.active_total:.15e}")
    print(f"{prefix}_ACTIVE_TO_ENERGY={diag.active_ratio:.15e}")
    print(f"{prefix}_MIN_ACTIVE_FRACTION={diag.min_active_fraction:.15e}")
    print(f"{prefix}_TOPOLOGY_SIGNED={diag.topology_signed:.15e}")
    print(f"{prefix}_TOPOLOGY_ABS={diag.topology_abs:.15e}")
    print(f"{prefix}_TOPOLOGY_RELERR={diag.topology_relerr:.15e}")
    print(f"{prefix}_MAX_NEIGHBOR_ANGLE={diag.max_neighbor_angle:.15e}")
    print(f"{prefix}_MIN_DEC_MARGIN={diag.min_dec_margin:.15e}")
    print(f"{prefix}_MAX_ACTIVE_TRACE_SCALED={diag.max_active_trace_scaled:.15e}")
    print(f"{prefix}_STRESS_DIVERGENCE_SCALED={diag.stress_divergence_scaled:.15e}")


def main() -> None:
    """Execute the complete 023C unrestricted Cartesian stability gate."""

    print("=== 023C — UNRESTRICTED CARTESIAN 3D RELAXATION + FULL PHYSICAL HESSIAN ===")

    # ------------------------------------------------------------------
    # A. Upstream audit.
    # ------------------------------------------------------------------
    print("\n=== A — UPSTREAM 023BR AUDIT ===")
    for path in (A23_SOURCE, B23_SOURCE, BR23_SOURCE, BR23_LOG):
        require_file(path)

    a_sha = sha256(A23_SOURCE)
    b_sha = sha256(B23_SOURCE)
    br_sha = sha256(BR23_SOURCE)
    print(f"023A_SOURCE_SHA256={a_sha}")
    print(f"023B_SOURCE_SHA256={b_sha}")
    print(f"023BR_SOURCE_SHA256={br_sha}")

    source_audit = (
        a_sha == EXPECTED_023A_SHA256
        and b_sha == EXPECTED_023B_SHA256
        and br_sha == EXPECTED_023BR_SHA256
    )
    require_markers(BR23_LOG, EXPECTED_023BR_MARKERS)
    print("UPSTREAM_023BR_AUDIT=" + ("PASS" if source_audit else "FAIL"))
    if not source_audit:
        raise RuntimeError("Upstream source hash audit failed")

    a23 = load_module("a23_for_023c", A23_SOURCE)
    b23 = load_module("b23_for_023c", B23_SOURCE)

    # ------------------------------------------------------------------
    # B. Reconstruct selected continuum candidate and payload geometry.
    # ------------------------------------------------------------------
    print("\n=== B — CONTINUUM SELECTED-CANDIDATE RECONSTRUCTION ===")
    degree, I_direct = b23.angular_integrals_b7(b23.B7_B0)
    profile = b23.solve_profile_with_custom_I(a23, B, ETA, MASS, I_direct)

    sector_profiles, sector_energies = b23.solve_exact_sector(a23, ETA, MASS)
    selected = b23.candidate_from_sector(a23, sector_profiles, sector_energies, B)

    continuum_energy = 4.0 * math.pi * float(profile.E)
    print(f"SELECTED_B={B}")
    print(f"SELECTED_ETA={ETA:.15e}")
    print(f"SELECTED_M={MASS:.15e}")
    print(f"DIRECT_MAP_DEGREE={degree:.15e}")
    print(f"DIRECT_MAP_I={I_direct:.15e}")
    print(f"CONTINUUM_PROFILE_ENERGY_4PI={continuum_energy:.15e}")
    print(f"PAYLOAD_CENTER={selected.payload.payload_center:.15e}")
    print(f"PAYLOAD_RADIUS={selected.payload.payload_radius:.15e}")

    domain = choose_cartesian_domain(
        profile,
        selected.payload.payload_center,
        selected.payload.payload_radius,
    )
    for key, value in domain.items():
        if isinstance(value, int):
            print(f"CARTESIAN_{key.upper()}={value}")
        else:
            print(f"CARTESIAN_{key.upper()}={value:.15e}")

    grid_resolution_pass = (
        domain["primary_ppw"] >= MIN_PRIMARY_POINTS_PER_WALL
        and domain["hessian_ppw"] >= MIN_HESSIAN_POINTS_PER_WALL
    )
    print("CARTESIAN_GRID_RESOLUTION=" + ("PASS" if grid_resolution_pass else "FAIL"))

    # ------------------------------------------------------------------
    # C. Exact discrete-gradient validation.
    # ------------------------------------------------------------------
    print("\n=== C — DISCRETE GRADIENT SELFCHECK ===")
    grad_rel, grad_pass = gradient_selfcheck()
    print(f"DISCRETE_GRADIENT_DIRECTIONAL_RELERR={grad_rel:.15e}")
    print("DISCRETE_GRADIENT_SELFCHECK=" + ("PASS" if grad_pass else "FAIL"))

    # ------------------------------------------------------------------
    # D. Low-resolution unrestricted relaxation + off-ansatz basin test.
    # ------------------------------------------------------------------
    print("\n=== D — LOW CARTESIAN RELAXATION + OFF-ANSATZ BASIN TEST ===")
    low_phi0, low_axis, low_dx = sample_rational_map_field(
        profile, b23.B7_B0, domain["low_n"], domain["half_domain"]
    )
    low_initial = lattice_diagnostics(low_phi0, low_axis, low_dx, ETA, MASS)
    print_diag("LOW_INITIAL", low_initial)

    low_energy_relerr = abs(low_initial.energy - continuum_energy) / continuum_energy
    print(f"LOW_INITIAL_ENERGY_RELERR={low_energy_relerr:.15e}")

    low_relax = relax_field(low_phi0, low_dx, ETA, MASS, RELAX_MAX_ITER_LOW)
    low_final = lattice_diagnostics(low_relax.field, low_axis, low_dx, ETA, MASS)
    print(f"LOW_RELAX_INITIAL_GRAD_RMS={low_relax.initial_grad_rms:.15e}")
    print(f"LOW_RELAX_FINAL_GRAD_RMS={low_relax.final_grad_rms:.15e}")
    print(f"LOW_RELAX_FINAL_GRAD_MAX={low_relax.final_grad_max:.15e}")
    print(f"LOW_RELAX_ITERATIONS={low_relax.iterations}")
    print(f"LOW_RELAX_ACCEPTED_STEPS={low_relax.accepted_steps}")
    print("LOW_RELAX_CONVERGED=" + ("YES" if low_relax.converged else "NO"))
    print("LOW_RELAX_LINE_SEARCH_FAILED=" + ("YES" if low_relax.line_search_failed else "NO"))
    print_diag("LOW_RELAXED", low_final)

    perturbed = smooth_off_ansatz_perturbation(low_phi0, PERTURB_AMPLITUDE_RAD)
    perturb_relax = relax_field(perturbed, low_dx, ETA, MASS, RELAX_MAX_ITER_LOW)
    perturb_final = lattice_diagnostics(perturb_relax.field, low_axis, low_dx, ETA, MASS)
    basin_energy_relerr = abs(perturb_final.energy - low_final.energy) / max(low_final.energy, 1.0e-300)
    print(f"OFF_ANSATZ_PERTURB_AMPLITUDE_RAD={PERTURB_AMPLITUDE_RAD:.15e}")
    print(f"OFF_ANSATZ_FINAL_ENERGY={perturb_final.energy:.15e}")
    print(f"OFF_ANSATZ_BASIN_ENERGY_RELERR={basin_energy_relerr:.15e}")
    print(f"OFF_ANSATZ_FINAL_TOPOLOGY_ABS={perturb_final.topology_abs:.15e}")
    print(f"OFF_ANSATZ_FINAL_GRAD_RMS={perturb_relax.final_grad_rms:.15e}")

    off_ansatz_pass = (
        perturb_relax.converged
        and perturb_final.topology_relerr <= MAX_TOPOLOGY_RELERR
        and basin_energy_relerr <= MAX_BASIN_ENERGY_RELERR
    )
    print("OFF_ANSATZ_BASIN_RETURN=" + ("PASS" if off_ansatz_pass else "FAIL"))

    # ------------------------------------------------------------------
    # E. Primary unrestricted relaxation.
    # ------------------------------------------------------------------
    print("\n=== E — PRIMARY UNRESTRICTED CARTESIAN RELAXATION ===")
    primary_phi0, primary_axis, primary_dx = sample_rational_map_field(
        profile, b23.B7_B0, domain["primary_n"], domain["half_domain"]
    )
    primary_initial = lattice_diagnostics(primary_phi0, primary_axis, primary_dx, ETA, MASS)
    print_diag("PRIMARY_INITIAL", primary_initial)

    primary_energy_relerr = abs(primary_initial.energy - continuum_energy) / continuum_energy
    print(f"PRIMARY_INITIAL_ENERGY_RELERR={primary_energy_relerr:.15e}")

    initial_energy_pass = (
        primary_energy_relerr <= MAX_INITIAL_ENERGY_RELERR
        and primary_initial.max_neighbor_angle <= MAX_NEIGHBOR_ANGLE
    )
    initial_topology_pass = primary_initial.topology_relerr <= MAX_TOPOLOGY_RELERR
    print("INITIAL_CARTESIAN_ENERGY_RECONSTRUCTION=" + ("PASS" if initial_energy_pass else "FAIL"))
    print("INITIAL_CARTESIAN_TOPOLOGY=" + ("PASS" if initial_topology_pass else "FAIL"))

    primary_relax = relax_field(primary_phi0, primary_dx, ETA, MASS, RELAX_MAX_ITER_PRIMARY)
    primary_final = lattice_diagnostics(primary_relax.field, primary_axis, primary_dx, ETA, MASS)
    print(f"PRIMARY_RELAX_INITIAL_GRAD_RMS={primary_relax.initial_grad_rms:.15e}")
    print(f"PRIMARY_RELAX_FINAL_GRAD_RMS={primary_relax.final_grad_rms:.15e}")
    print(f"PRIMARY_RELAX_FINAL_GRAD_MAX={primary_relax.final_grad_max:.15e}")
    print(f"PRIMARY_RELAX_ITERATIONS={primary_relax.iterations}")
    print(f"PRIMARY_RELAX_ACCEPTED_STEPS={primary_relax.accepted_steps}")
    print("PRIMARY_RELAX_CONVERGED=" + ("YES" if primary_relax.converged else "NO"))
    print("PRIMARY_RELAX_LINE_SEARCH_FAILED=" + ("YES" if primary_relax.line_search_failed else "NO"))
    print_diag("PRIMARY_RELAXED", primary_final)

    primary_relax_pass = (
        primary_relax.converged
        and primary_relax.final_energy <= primary_relax.initial_energy * (1.0 + 1.0e-8)
    )
    relaxed_topology_pass = (
        primary_final.topology_relerr <= MAX_TOPOLOGY_RELERR
        and primary_final.max_neighbor_angle <= MAX_NEIGHBOR_ANGLE
    )
    relaxed_dec_pass = primary_final.min_dec_margin >= MIN_DEC_MARGIN
    relaxed_trace_pass = primary_final.max_active_trace_scaled <= MAX_ACTIVE_TRACE_SCALED
    negative_active_pass = primary_final.min_active_fraction <= -MIN_NEGATIVE_ACTIVE_FRACTION
    positive_active_pass = (
        primary_final.active_total > 0.0
        and MIN_POSITIVE_ACTIVE_RATIO <= primary_final.active_ratio <= MAX_POSITIVE_ACTIVE_RATIO
    )

    print("UNRESTRICTED_PRIMARY_RELAXATION=" + ("PASS" if primary_relax_pass else "FAIL"))
    print("RELAXED_CARTESIAN_TOPOLOGY=" + ("PASS" if relaxed_topology_pass else "FAIL"))
    print("RELAXED_POINTWISE_DEC=" + ("PASS" if relaxed_dec_pass else "FAIL"))
    print("RELAXED_ACTIVE_TRACE_IDENTITY=" + ("PASS" if relaxed_trace_pass else "FAIL"))
    print("RELAXED_NEGATIVE_ENCLOSED_ACTIVE_MASS=" + ("PASS" if negative_active_pass else "FAIL"))
    print("RELAXED_POSITIVE_TOTAL_ACTIVE_MASS=" + ("PASS" if positive_active_pass else "FAIL"))

    # ------------------------------------------------------------------
    # F. Dense payload gravity from the unrestricted relaxed source.
    # ------------------------------------------------------------------
    print("\n=== F — RELAXED DENSE FINITE-PAYLOAD GRAVITY ===")
    payload = payload_audit(
        primary_relax.field,
        primary_axis,
        primary_dx,
        selected.payload.payload_center,
        selected.payload.payload_radius,
    )
    print(f"RELAXED_DENSE_ORIENTATION_COUNT={DENSE_ORIENTATION_N}")
    print(f"RELAXED_MIN_RADIAL_OUTWARD={payload.min_radial:.15e}")
    print(f"RELAXED_MAX_RADIAL_OUTWARD={payload.max_radial:.15e}")
    print(f"RELAXED_MEAN_RADIAL_OUTWARD={payload.mean_radial:.15e}")
    print(f"RELAXED_MAX_TRANSVERSE={payload.max_transverse:.15e}")
    print(f"RELAXED_MAX_TRANSVERSE_OVER_RADIAL={payload.max_transverse_over_radial:.15e}")
    print(
        "RELAXED_WORST_RADIAL_ORIENTATION=("
        + ",".join(f"{x:.12e}" for x in payload.worst_orientation)
        + ")"
    )
    print("RELAXED_DENSE_FINITE_PAYLOAD_OUTWARD=" + ("PASS" if payload.all_outward else "FAIL"))

    # ------------------------------------------------------------------
    # G. Low/primary continuum trend.
    # ------------------------------------------------------------------
    print("\n=== G — LOW/PRIMARY CARTESIAN CONVERGENCE ===")
    energy_lp = abs(primary_final.energy - low_final.energy) / max(primary_final.energy, 1.0e-300)
    active_lp = abs(primary_final.min_active_fraction - low_final.min_active_fraction)
    low_primary_pass = (
        energy_lp <= MAX_RELAXED_ENERGY_LOW_PRIMARY_RELERR
        and active_lp <= MAX_ACTIVE_FRACTION_LOW_PRIMARY_ABS
        and low_final.topology_relerr <= MAX_TOPOLOGY_RELERR
        and primary_final.topology_relerr <= MAX_TOPOLOGY_RELERR
    )
    print(f"RELAXED_ENERGY_LOW_PRIMARY_RELERR={energy_lp:.15e}")
    print(f"RELAXED_ACTIVE_FRACTION_LOW_PRIMARY_ABS={active_lp:.15e}")
    print("RELAXED_LOW_PRIMARY_CONVERGENCE=" + ("PASS" if low_primary_pass else "FAIL"))

    # ------------------------------------------------------------------
    # H. Full physical tangent Hessian.
    # ------------------------------------------------------------------
    print("\n=== H — FULL PHYSICAL CARTESIAN HESSIAN ===")
    if domain["hessian_n"] == domain["primary_n"]:
        h_phi = primary_relax.field
        h_axis = primary_axis
        h_dx = primary_dx
        h_relax = primary_relax
        h_diag = primary_final
    else:
        h_phi0, h_axis, h_dx = sample_rational_map_field(
            profile, b23.B7_B0, domain["hessian_n"], domain["half_domain"]
        )
        h_relax = relax_field(h_phi0, h_dx, ETA, MASS, RELAX_MAX_ITER_PRIMARY)
        h_phi = h_relax.field
        h_diag = lattice_diagnostics(h_phi, h_axis, h_dx, ETA, MASS)
        print(f"HESSIAN_GRID_RELAX_FINAL_GRAD_RMS={h_relax.final_grad_rms:.15e}")
        print(f"HESSIAN_GRID_RELAX_FINAL_GRAD_MAX={h_relax.final_grad_max:.15e}")
        print(f"HESSIAN_GRID_TOPOLOGY_RELERR={h_diag.topology_relerr:.15e}")
        print(f"HESSIAN_GRID_MAX_NEIGHBOR_ANGLE={h_diag.max_neighbor_angle:.15e}")

    hessian_resolution_pass = (
        domain["hessian_ppw"] >= MIN_HESSIAN_POINTS_PER_WALL
        and h_diag.topology_relerr <= MAX_TOPOLOGY_RELERR
        and h_diag.max_neighbor_angle <= MAX_NEIGHBOR_ANGLE
        and h_relax.converged
    )
    print("HESSIAN_GRID_RESOLUTION=" + ("PASS" if hessian_resolution_pass else "FAIL"))

    hess = hessian_analysis(h_phi, h_dx) if hessian_resolution_pass else {
        "converged": False,
        "bilinear_asym": math.inf,
        "eigenvalues": np.array([]),
        "lambda_min": math.nan,
        "spectral_scale": math.nan,
        "negative_significant": True,
        "zero_overlaps": [],
        "direct_rayleigh": [],
        "direct_curvature_pass": False,
    }

    print(f"FULL_TANGENT_HESSIAN_DOF={3 * (domain['hessian_n'] - 2) ** 3}")
    print("HESSIAN_EIGENSOLVER_CONVERGED=" + ("YES" if hess["converged"] else "NO"))
    print(f"HESSIAN_BILINEAR_ASYMMETRY={hess['bilinear_asym']:.15e}")
    print("HESSIAN_LOWEST_EIGENVALUES=" + ",".join(f"{x:.15e}" for x in hess["eigenvalues"]))
    print(f"HESSIAN_LAMBDA_MIN={hess['lambda_min']:.15e}")
    print(f"HESSIAN_SPECTRAL_SCALE={hess['spectral_scale']:.15e}")
    print("HESSIAN_LOW_MODE_ISOROTATION_OVERLAPS=" + ",".join(f"{x:.9e}" for x in hess["zero_overlaps"]))
    print("LOWEST_MODE_DIRECT_RAYLEIGH=" + ",".join(f"{x:.15e}" for x in hess["direct_rayleigh"]))

    hessian_selfadj_pass = (
        hess["converged"]
        and hess["bilinear_asym"] <= MAX_HESSIAN_BILINEAR_ASYMMETRY
    )
    hessian_pass = (
        hessian_selfadj_pass
        and not hess["negative_significant"]
    )
    direct_curvature_pass = bool(hess["direct_curvature_pass"])

    print("FULL_TANGENT_HESSIAN_SELF_ADJOINTNESS=" + ("PASS" if hessian_selfadj_pass else "FAIL"))
    print(
        "FULL_PHYSICAL_HESSIAN="
        + ("PASS_NO_SIGNIFICANT_NEGATIVE_MODE" if hessian_pass else "FAIL_OR_UNRESOLVED")
    )
    print("LOWEST_MODE_DIRECT_CURVATURE=" + ("PASS" if direct_curvature_pass else "FAIL"))

    # ------------------------------------------------------------------
    # I. Blind wildcard diagnostics — never evidence.
    # ------------------------------------------------------------------
    print("\n=== I — BLIND WILDCARD DIAGNOSTICS — NOT EVIDENCE ===")
    # Use harmless perturbation-amplitude rescalings only; do not feed these
    # values back into candidate selection or promotion.
    for factor in BLIND_WILDCARDS:
        amp = min(0.08, PERTURB_AMPLITUDE_RAD * float(factor))
        probe = smooth_off_ansatz_perturbation(low_relax.field, amp, seed=23040 + int(1000 * factor))
        Eprobe = energy_and_euclidean_gradient(probe, low_dx, ETA, MASS, False)[0]
        print(f"WILDCARD_FACTOR={factor:.6f} PERTURB_RAD={amp:.9e} ENERGY_RATIO={Eprobe/low_final.energy:.9e}")
    print("BLIND_WILDCARD_VALUES_USED_AS_EVIDENCE=NO")

    # ------------------------------------------------------------------
    # J. Decision.
    # ------------------------------------------------------------------
    print("\n=== J — 023C DECISION ===")
    green = all(
        [
            source_audit,
            grad_pass,
            grid_resolution_pass,
            initial_energy_pass,
            initial_topology_pass,
            primary_relax_pass,
            off_ansatz_pass,
            relaxed_topology_pass,
            relaxed_dec_pass,
            relaxed_trace_pass,
            negative_active_pass,
            positive_active_pass,
            payload.all_outward,
            low_primary_pass,
            hessian_resolution_pass,
            hessian_selfadj_pass,
            hessian_pass,
            direct_curvature_pass,
        ]
    )

    if green:
        print("023C_UNRESTRICTED_CARTESIAN_3D_RELAXATION_AND_FULL_PHYSICAL_HESSIAN=GREEN")
        print("UNRESTRICTED_CARTESIAN_3D_STABLE_TOPOLOGICAL_REPULSIVE_FIELD=SUPPORTED")
        print("HEURISTIC_PROMOTION_ELIGIBILITY=APPROXIMATELY_72_PERCENT_AFTER_CLAIM_AUDIT")
        print("NEXT=023D_VALIDATED_WEAK_GRAVITY_EINSTEIN_SKYRME_CONTINUATION")
    else:
        numerical_only = (
            not hessian_resolution_pass
            or not hess["converged"]
            or not hessian_selfadj_pass
            or not grid_resolution_pass
            or not primary_relax.converged
        ) and not hess["negative_significant"] and relaxed_topology_pass

        if hess["negative_significant"] and hess["converged"] and hessian_selfadj_pass:
            print("023C_UNRESTRICTED_CARTESIAN_3D_RELAXATION_AND_FULL_PHYSICAL_HESSIAN=GREEN_NEGATIVE_RESULT")
            print("UNRESTRICTED_CARTESIAN_3D_STABILITY=FAIL_NEGATIVE_MODE")
            print("NEXT=PRESERVE_FALSIFICATION_AND_GLOBAL_RERANK")
        elif numerical_only:
            print("023C_UNRESTRICTED_CARTESIAN_3D_RELAXATION_AND_FULL_PHYSICAL_HESSIAN=INCOMPLETE_NUMERICAL_GATE")
            print("UNRESTRICTED_CARTESIAN_3D_STABILITY=NOT_YET_RESOLVED")
            print("NEXT=023CR_TARGETED_CARTESIAN_NUMERICAL_REPAIR")
        else:
            print("023C_UNRESTRICTED_CARTESIAN_3D_RELAXATION_AND_FULL_PHYSICAL_HESSIAN=GREEN_NEGATIVE_OR_INCOMPLETE_RESULT")
            print("UNRESTRICTED_CARTESIAN_3D_STABILITY=NOT_PROMOTED")
            print("NEXT=INSPECT_FAILED_PHYSICAL_GATE_BEFORE_ANY_ESCALATION")

    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_ESTABLISHED")
    print("PRACTICAL_ENERGY_SCALING=STILL_CATASTROPHIC_IN_PURE_GR")
    print("REAL_MATERIAL=NO")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print("006D_CONSTRUCTIVE_LINEARIZED_GR_RESULT=RETAINED")
    print("018B_FIELD_EXISTENCE_RESULT=RETAINED")
    print("018C_KLS_M2_STABILITY_FAILURE=RETAINED")
    print("023BR_PROMOTION_GRADE_EXACT_MAP_PREFLIGHT=RETAINED")
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023C_UNRESTRICTED_CARTESIAN_3D_RELAXATION_AND_FULL_PHYSICAL_HESSIAN")

    # Preserve the primary relaxed field for independent post-run inspection.
    data_dir = ROOT / "results/data"
    data_dir.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        data_dir / "023c_unrestricted_cartesian_relaxed_b7.npz",
        phi=primary_relax.field,
        axis=primary_axis,
        dx=np.array(primary_dx),
        eta=np.array(ETA),
        m=np.array(MASS),
        B=np.array(B),
        payload_center=np.array(selected.payload.payload_center),
        payload_radius=np.array(selected.payload.payload_radius),
    )
    print("RELAXED_FIELD_ARTIFACT=results/data/023c_unrestricted_cartesian_relaxed_b7.npz")


if __name__ == "__main__":
    main()
