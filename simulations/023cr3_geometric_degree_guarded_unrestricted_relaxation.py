#!/usr/bin/env python3
"""023CR3 — geometric-degree-guarded unrestricted Cartesian relaxation.

PURPOSE
-------
Perform the first trustworthy unrestricted Cartesian relaxation of the selected
false-core B=7 Skyrmion after 023CR2 repaired the lattice representation.

SCIENTIFIC QUESTION
-------------------
Does the exact-map B=7, eta=0.4, m=8 candidate relax to a nearby stationary
configuration in the *full* SU(2) field space while preserving:

1. the exact topological sector |B|=7;
2. lattice smoothness sufficient to exclude discrete topology jumps;
3. positive total active gravitational mass;
4. a finite negative enclosed active-mass region; and
5. outward finite-payload linearized-GR acceleration over a dense orientation
   sphere?

This is a stationarity / unrestricted-relaxation gate.  It is deliberately
separate from the full physical Hessian.  A green result authorizes the
corrected full-tangent Hessian gate; it does not by itself prove dynamical
stability.

UPSTREAM STATE
--------------
023BR selected the existing exact-map candidate

    B = 7,
    eta = 0.4,
    m = 8,

and found promotion-grade rational-map robustness plus dense 320-orientation
finite-payload outward gravity.

023C attempted unrestricted Cartesian relaxation with centered differences.
It was numerically invalid because the centered derivative has an exact
checkerboard/Nyquist null mode; the initial grid also failed to reconstruct
B=7 before relaxation.

023CR diagnosed and removed that null mode with a nearest-neighbor link action.
023CR2 then established a higher-order checkerboard-free representation with:

    N=57 and N=65 both passing continuum reconstruction,
    derivative topology close to B=7,
    three independent geometric degree witnesses equal to -7,
    and a converged N57/N65 representation pair.

CONTINUUM MODEL
---------------
The static SU(2) Skyrme field is represented by

    phi = (sigma, pi_1, pi_2, pi_3),
    phi . phi = 1.

The continuum energy is

    E = integral (e2 + e4 + V) d^3x,

    e2 = sum_i |d_i phi|^2,

    e4 = sum_(i<j) [
        |d_i phi|^2 |d_j phi|^2
        - (d_i phi . d_j phi)^2
    ],

    V = m^2 (1-sigma)(1+eta sigma).

The static active gravitational source is

    S = rho + p_1 + p_2 + p_3 = 2(e4 - V).

HIGH-ORDER CHECKERBOARD-FREE ACTION
-----------------------------------
Use the fourth-order one-sided derivative

    D_+ f_i =
      (-25 f_i + 48 f_{i+1} - 36 f_{i+2}
       +16 f_{i+3} - 3 f_{i+4}) / (12 dx),

and its backward partner.  The action is the average of the forward- and
backward-oriented derivative energies.  023CR2 verified that the corresponding
Fourier symbol has no spurious unit-circle zero and strongly penalizes the
Nyquist/checkerboard mode.

This file implements the exact discrete gradient of that high-order action and
verifies it by a directional finite-difference self-check before relaxation.

TOPOLOGY GUARD
--------------
Continuum degree cannot change under a smooth deformation with the vacuum
boundary held fixed.  Numerical relaxation is therefore constrained only
against *discrete artifacts* that would illegally change topology:

- the outer vacuum boundary is fixed;
- every accepted trial must remain link-smooth;
- the fourth-order derivative topology must remain near |B|=7;
- a geometric preimage degree witness is checked on accepted candidates;
- all three independent geometric targets are rechecked at the final state.

This does not add a physical stabilizer or rigidity term.  It restricts the
numerical evolution to the continuum topological sector being tested.

OPERATIONAL OBSERVABLE
----------------------
After relaxation, reconstruct the continuum stress tensor from fourth-order
central derivatives and compute:

    S = 2(e4 - V).

For a uniform spherical payload the exact volume-averaged Newton kernel is
used, as in 023BR/023C, over a deterministic 320-direction Fibonacci sphere.
Positive radial kernel means outward acceleration in the repository convention.

CHEAPEST DECISIVE EXPERIMENT
----------------------------
1. Audit 023CR2 source + successful log.
2. Verify the exact high-order action gradient on an independent smooth field.
3. Reconstruct the exact B=7 candidate independently at N=57 and N=65.
4. Unrestrictedly relax both lattices in the fixed B=7 sector.
5. Require final stationarity, geometric degree |B|=7, smooth links, positive
   total active mass, a negative enclosed active region, pointwise DEC, active
   trace consistency, and dense finite-payload outward gravity.
6. Require the N57/N65 relaxed observables to agree at useful accuracy.

PROMOTION CONDITION
-------------------
023CR3 is GREEN_UNRESTRICTED_STATIONARY_FIELD only if both N=57 and N=65:

- pass initial reconstruction;
- converge under the unrestricted high-order Riemannian relaxation;
- retain all three geometric degrees at the same sign with |degree|=7;
- retain derivative topology close to 7;
- remain lattice-smooth;
- have positive total active mass;
- retain a negative enclosed active-mass fraction at least 1 percent;
- satisfy pointwise DEC to numerical tolerance;
- satisfy the active-trace identity;
- preserve outward finite-payload acceleration in all 320 tested orientations;
- and pass low/primary relaxed-observable convergence.

A green result authorizes:

    023C2_CORRECTED_FULL_PHYSICAL_HESSIAN

It does NOT by itself establish unrestricted dynamical stability.

FALSIFIER / STOP RULE
---------------------
If the evolution remains numerically admissible and stationary in B=7 but the
relaxed continuum field loses positive total active mass or loses dense
finite-payload outward gravity at both resolutions, preserve that as a physical
negative result for this candidate before considering another candidate.

If degree or link smoothness fails, or the two resolutions do not converge,
classify the run as an incomplete numerical gate rather than a physical
instability.  Do not proceed to the Hessian until the stationary field is
numerically trustworthy.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023CR3_GEOMETRIC_DEGREE_GUARDED_UNRESTRICTED_RELAXATION

WHAT THIS FILE DOES NOT ESTABLISH
---------------------------------
- a positive full physical Hessian;
- nonlinear Einstein-Skyrme consistency;
- practical energy scaling;
- a real material realization;
- an experimental signal;
- a practical antigravity device;
- discovery of new physics.
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
C23_SOURCE = ROOT / "simulations/023c_unrestricted_cartesian_3d_relaxation_and_full_physical_hessian.py"
CR2_SOURCE = ROOT / "simulations/023cr2_high_order_geometric_topology_preflight.py"
CR2_LOG = ROOT / "results/logs/023cr2_high_order_geometric_topology_preflight.log"

EXPECTED_023A_SHA256 = "0087a5d2b4f93667308cabf4c3c498200ed29381e9493acf21714df7d8e11c9b"
EXPECTED_023B_SHA256 = "6bf99785e67cfe1b2dfcb460bc3145a24115e25949e112f8480a89c880a2803c"
EXPECTED_023C_SHA256 = "9fd323a2f845c0373f7926af11f09c563138386b18c8fa3c091acb114318a675"
EXPECTED_023CR2_SHA256 = "6affc28547b7849140f1eacf6992c9541ea9ba9a7c306e69121ca60ef76ad1db"

B = 7
ETA = 0.40
MASS = 8.0
GRID_LEVELS = (57, 65)
PRIMARY_N = 65
DENSE_ORIENTATION_N = 320

FORWARD_COEFF = np.array([-25.0, 48.0, -36.0, 16.0, -3.0]) / 12.0
BACKWARD_COEFF = np.array([25.0, -48.0, 36.0, -16.0, 3.0]) / 12.0

MAX_INITIAL_ENERGY_RELERR = 1.0e-2
MAX_INITIAL_E4_RELERR = 1.5e-2
MAX_INITIAL_TOPOLOGY_RELERR = 1.0e-2
MAX_NEIGHBOR_ANGLE = 0.70
MAX_GUARD_TOPOLOGY_RELERR = 3.0e-2

RELAX_MAX_ITER = 180
RELAX_GRAD_RMS_TOL = 1.5e-3
RELAX_GRAD_MAX_TOL = 5.0e-2
RELAX_MAX_POINT_ROTATION = 0.075
RELAX_ARMIJO = 1.0e-4
RELAX_MIN_STEP = 1.0e-8
GEOMETRIC_GUARD_EVERY = 5

MIN_NEGATIVE_ACTIVE_FRACTION = 1.0e-2
MIN_DENSE_RADIAL_OUTWARD = 0.0
MIN_DEC_SCALED_MARGIN = -2.0e-8
MAX_ACTIVE_TRACE_SCALED = 2.0e-12

MAX_RELAXED_ENERGY_PAIR_RELCHANGE = 2.0e-2
MAX_RELAXED_ACTIVE_PAIR_ABSCHANGE = 4.0e-2
MAX_RELAXED_PAYLOAD_PAIR_RELCHANGE = 8.0e-2
MAX_RELAXED_TOPOLOGY_PAIR_ABSCHANGE = 1.5e-2

ARTIFACT = ROOT / "results/data/023cr3_unrestricted_relaxed_b7_n65.npz"


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
    rejected_energy_trials: int
    rejected_topology_trials: int
    rejected_smoothness_trials: int
    converged: bool
    line_search_failed: bool
    final_geometric_degrees: tuple[int, ...]
    final_topology4: float
    final_max_neighbor_angle: float


@dataclass
class PhysicalDiagnostics:
    energy_continuum: float
    e2: float
    e4: float
    e0: float
    active_total: float
    active_to_energy: float
    min_active_fraction: float
    topology4: float
    topology4_relerr: float
    geometric_degrees: tuple[int, ...]
    max_neighbor_angle: float
    min_dec_scaled_margin: float
    max_active_trace_scaled: float
    energy_centroid_norm: float


@dataclass
class PayloadDiagnostics:
    min_radial: float
    max_radial: float
    mean_radial: float
    max_transverse: float
    max_transverse_over_radial: float
    worst_orientation: np.ndarray
    all_outward: bool


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


def normalize_field(phi: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(phi, axis=-1, keepdims=True)
    return phi / np.maximum(norm, 1.0e-300)


def enforce_vacuum_boundary(phi: np.ndarray) -> None:
    vacuum = np.array([1.0, 0.0, 0.0, 0.0])
    phi[0, :, :, :] = vacuum
    phi[-1, :, :, :] = vacuum
    phi[:, 0, :, :] = vacuum
    phi[:, -1, :, :] = vacuum
    phi[:, :, 0, :] = vacuum
    phi[:, :, -1, :] = vacuum


def project_tangent(phi: np.ndarray, vector: np.ndarray) -> np.ndarray:
    return vector - np.sum(vector * phi, axis=-1, keepdims=True) * phi


def exp_map_update(phi: np.ndarray, tangent: np.ndarray, alpha: float) -> np.ndarray:
    out = phi.copy()
    p = phi[1:-1, 1:-1, 1:-1]
    v = tangent[1:-1, 1:-1, 1:-1]
    speed = np.linalg.norm(v, axis=-1)
    angle = alpha * speed
    mask = speed > 1.0e-16
    new = p.copy()
    if np.any(mask):
        unit = np.zeros_like(v)
        unit[mask] = v[mask] / speed[mask, None]
        new[mask] = (
            np.cos(angle[mask])[..., None] * p[mask]
            + np.sin(angle[mask])[..., None] * unit[mask]
        )
    out[1:-1, 1:-1, 1:-1] = new
    enforce_vacuum_boundary(out)
    return normalize_field(out)


def potential_sigma(sigma: np.ndarray) -> np.ndarray:
    return MASS * MASS * (1.0 - sigma) * (1.0 + ETA * sigma)


def dpotential_dsigma(sigma: np.ndarray) -> np.ndarray:
    return MASS * MASS * ((ETA - 1.0) - 2.0 * ETA * sigma)


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


def oriented_high_order_energy_gradient(
    phi: np.ndarray,
    dx: float,
    forward: bool,
    need_gradient: bool,
):
    """One orientation of the fourth-order one-sided derivative action."""

    n = phi.shape[0]
    m = n - 4
    coeff = FORWARD_COEFF if forward else BACKWARD_COEFF

    if forward:
        qx = sum(coeff[s] * phi[s:s + m, :m, :m] for s in range(5)) / dx
        qy = sum(coeff[s] * phi[:m, s:s + m, :m] for s in range(5)) / dx
        qz = sum(coeff[s] * phi[:m, :m, s:s + m] for s in range(5)) / dx
    else:
        qx = sum(coeff[s] * phi[4 - s:n - s, 4:, 4:] for s in range(5)) / dx
        qy = sum(coeff[s] * phi[4:, 4 - s:n - s, 4:] for s in range(5)) / dx
        qz = sum(coeff[s] * phi[4:, 4:, 4 - s:n - s] for s in range(5)) / dx

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
        for s in range(5):
            cs = c * coeff[s]
            grad[s:s + m, :m, :m] += cs * px
            grad[:m, s:s + m, :m] += cs * py
            grad[:m, :m, s:s + m] += cs * pz
    else:
        for s in range(5):
            cs = c * coeff[s]
            grad[4 - s:n - s, 4:, 4:] += cs * px
            grad[4:, 4 - s:n - s, 4:] += cs * py
            grad[4:, 4:, 4 - s:n - s] += cs * pz

    return E2, E4, grad


def high_order_energy_gradient(phi: np.ndarray, dx: float, need_gradient: bool = True):
    E2f, E4f, gf = oriented_high_order_energy_gradient(phi, dx, True, need_gradient)
    E2b, E4b, gb = oriented_high_order_energy_gradient(phi, dx, False, need_gradient)
    E2 = 0.5 * (E2f + E2b)
    E4 = 0.5 * (E4f + E4b)

    sigma = phi[2:-2, 2:-2, 2:-2, 0]
    V = potential_sigma(sigma)
    E0 = float(np.sum(V) * dx**3)
    E = E2 + E4 + E0

    if not need_gradient:
        return E, E2, E4, E0, None

    assert gf is not None and gb is not None
    grad = 0.5 * (gf + gb)
    grad[2:-2, 2:-2, 2:-2, 0] += dpotential_dsigma(sigma) * dx**3

    grad[0, :, :, :] = 0.0
    grad[-1, :, :, :] = 0.0
    grad[:, 0, :, :] = 0.0
    grad[:, -1, :, :] = 0.0
    grad[:, :, 0, :] = 0.0
    grad[:, :, -1, :] = 0.0
    return E, E2, E4, E0, grad


def riemannian_gradient_density(phi: np.ndarray, dx: float):
    E, E2, E4, E0, grad = high_order_energy_gradient(phi, dx, True)
    assert grad is not None
    gd = project_tangent(phi, grad / dx**3)
    gd[0, :, :, :] = 0.0
    gd[-1, :, :, :] = 0.0
    gd[:, 0, :, :] = 0.0
    gd[:, -1, :, :] = 0.0
    gd[:, :, 0, :] = 0.0
    gd[:, :, -1, :] = 0.0
    return E, E2, E4, E0, gd


def tangent_inner(a: np.ndarray, b: np.ndarray, dx: float) -> float:
    return float(np.sum(a[1:-1, 1:-1, 1:-1] * b[1:-1, 1:-1, 1:-1]) * dx**3)


def gradient_norms(g: np.ndarray) -> tuple[float, float]:
    gi = g[1:-1, 1:-1, 1:-1]
    n = np.linalg.norm(gi, axis=-1)
    return math.sqrt(float(np.mean(n * n))), float(np.max(n))


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


def topology4(phi: np.ndarray, dx: float) -> float:
    qx, qy, qz = central4_derivatives(phi, dx)
    center = phi[2:-2, 2:-2, 2:-2]
    mat = np.stack([center, qx, qy, qz], axis=-1)
    det = np.linalg.det(mat)
    return -float(np.sum(det) * dx**3 / (2.0 * math.pi**2))


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


def gradient_selfcheck() -> tuple[float, bool]:
    n = 10
    L = 1.25
    axis = np.linspace(-L, L, n)
    dx = float(axis[1] - axis[0])
    X, Y, Z = np.meshgrid(axis, axis, axis, indexing="ij")
    envelope = np.maximum(
        (1.0 - (X / L) ** 2)
        * (1.0 - (Y / L) ** 2)
        * (1.0 - (Z / L) ** 2),
        0.0,
    )
    pion = np.zeros((n, n, n, 3))
    pion[..., 0] = 0.11 * envelope * np.sin(math.pi * X / L)
    pion[..., 1] = 0.09 * envelope * np.sin(math.pi * Y / L)
    pion[..., 2] = 0.07 * envelope * np.sin(math.pi * Z / L)
    pion2 = np.sum(pion * pion, axis=-1)
    phi = np.zeros((n, n, n, 4))
    phi[..., 0] = np.sqrt(np.maximum(1.0 - pion2, 1.0e-14))
    phi[..., 1:] = pion
    enforce_vacuum_boundary(phi)
    phi = normalize_field(phi)

    _, _, _, _, grad = high_order_energy_gradient(phi, dx, True)
    assert grad is not None
    rng = np.random.default_rng(23051)
    v = np.zeros_like(phi)
    v[1:-1, 1:-1, 1:-1] = rng.normal(size=v[1:-1, 1:-1, 1:-1].shape)
    v = project_tangent(phi, v)
    v /= max(math.sqrt(float(np.sum(v * v))), 1.0e-300)

    eps = 8.0e-7
    plus = exp_map_update(phi, v, eps)
    minus = exp_map_update(phi, v, -eps)
    Ep = high_order_energy_gradient(plus, dx, False)[0]
    Em = high_order_energy_gradient(minus, dx, False)[0]
    finite = (Ep - Em) / (2.0 * eps)
    analytic = float(np.sum(grad * v))
    rel = abs(finite - analytic) / max(abs(finite), abs(analytic), 1.0e-12)
    return rel, rel <= 5.0e-6


def geometric_guard(phi: np.ndarray, cr2, all_targets: bool) -> tuple[bool, tuple[int, ...]]:
    if all_targets:
        degrees = tuple(int(x) for x in cr2.geometric_degrees(phi))
    else:
        degree = int(cr2.geometric_degree_single(phi, cr2.GEOMETRIC_TARGETS[0], 1.15))
        if abs(degree) != B:
            degree = int(cr2.geometric_degree_single(phi, cr2.GEOMETRIC_TARGETS[0], 1.55))
        degrees = (degree,)
    ok = all(abs(d) == B for d in degrees) and len(set(np.sign(d) for d in degrees)) == 1
    return ok, degrees


def relax_field(phi0: np.ndarray, dx: float, cr2) -> RelaxResult:
    phi = phi0.copy()
    enforce_vacuum_boundary(phi)
    phi = normalize_field(phi)

    E0 = high_order_energy_gradient(phi, dx, False)[0]
    E, _, _, _, g = riemannian_gradient_density(phi, dx)
    initial_rms, _ = gradient_norms(g)
    direction = -g
    step = 0.05
    accepted = 0
    rej_energy = 0
    rej_topology = 0
    rej_smooth = 0
    line_fail = False

    for iteration in range(1, RELAX_MAX_ITER + 1):
        rms, gmax = gradient_norms(g)
        if rms <= RELAX_GRAD_RMS_TOL and gmax <= RELAX_GRAD_MAX_TOL:
            break

        gd = tangent_inner(g, direction, dx)
        gg = tangent_inner(g, g, dx)
        if not math.isfinite(gd) or gd >= -1.0e-8 * gg:
            direction = -g
            gd = -gg

        max_dir = float(np.max(np.linalg.norm(direction[1:-1, 1:-1, 1:-1], axis=-1)))
        alpha = min(step, RELAX_MAX_POINT_ROTATION / max(max_dir, 1.0e-300))
        accepted_here = False
        trial = None
        Etrial = math.inf

        for _ in range(20):
            if alpha < RELAX_MIN_STEP:
                break
            candidate = exp_map_update(phi, direction, alpha)
            Etrial = high_order_energy_gradient(candidate, dx, False)[0]
            if not math.isfinite(Etrial) or Etrial > E + RELAX_ARMIJO * alpha * gd:
                rej_energy += 1
                alpha *= 0.5
                continue

            angle = max_neighbor_angle(candidate)
            if angle > MAX_NEIGHBOR_ANGLE:
                rej_smooth += 1
                alpha *= 0.5
                continue

            t4 = topology4(candidate, dx)
            if abs(abs(t4) / B - 1.0) > MAX_GUARD_TOPOLOGY_RELERR:
                rej_topology += 1
                alpha *= 0.5
                continue

            # Smooth links plus the derivative topology guard prevent a
            # continuum-forbidden degree jump between geometric audits.  To
            # keep the relaxation affordable, use one exact geometric target
            # every GEOMETRIC_GUARD_EVERY accepted steps and all three targets
            # every four such checks.  The final field is always audited with
            # all three independent targets.
            guard_index = accepted + 1
            if guard_index % GEOMETRIC_GUARD_EVERY == 0:
                full_check = (guard_index % (4 * GEOMETRIC_GUARD_EVERY) == 0)
                gok, _ = geometric_guard(candidate, cr2, full_check)
                if not gok:
                    rej_topology += 1
                    alpha *= 0.5
                    continue

            trial = candidate
            accepted_here = True
            break

        if not accepted_here or trial is None:
            line_fail = True
            break

        old_g = g
        old_direction = direction
        old_gg = tangent_inner(old_g, old_g, dx)

        phi = trial
        E, _, _, _, g = riemannian_gradient_density(phi, dx)
        accepted += 1

        transported_g = project_tangent(phi, old_g)
        transported_d = project_tangent(phi, old_direction)
        y = g - transported_g
        beta = max(0.0, tangent_inner(g, y, dx) / max(old_gg, 1.0e-300))
        beta = min(beta, 4.0)
        direction = -g + beta * transported_d
        if tangent_inner(g, direction, dx) >= -1.0e-6 * tangent_inner(g, g, dx):
            direction = -g

        step = min(max(alpha * 1.30, 1.0e-7), 1.0)

    final_rms, final_max = gradient_norms(g)
    final_t4 = topology4(phi, dx)
    final_angle = max_neighbor_angle(phi)
    gok, degrees = geometric_guard(phi, cr2, True)
    converged = (
        final_rms <= RELAX_GRAD_RMS_TOL
        and final_max <= RELAX_GRAD_MAX_TOL
        and gok
        and abs(abs(final_t4) / B - 1.0) <= MAX_GUARD_TOPOLOGY_RELERR
        and final_angle <= MAX_NEIGHBOR_ANGLE
    )

    return RelaxResult(
        field=phi,
        initial_energy=E0,
        final_energy=E,
        initial_grad_rms=initial_rms,
        final_grad_rms=final_rms,
        final_grad_max=final_max,
        iterations=accepted if line_fail else min(RELAX_MAX_ITER, accepted),
        accepted_steps=accepted,
        rejected_energy_trials=rej_energy,
        rejected_topology_trials=rej_topology,
        rejected_smoothness_trials=rej_smooth,
        converged=converged,
        line_search_failed=line_fail,
        final_geometric_degrees=degrees,
        final_topology4=final_t4,
        final_max_neighbor_angle=final_angle,
    )


def continuum_local_diagnostics(phi: np.ndarray, axis: np.ndarray, dx: float, cr2) -> PhysicalDiagnostics:
    qx, qy, qz = central4_derivatives(phi, dx)
    gxx, gyy, gzz, gxy, gxz, gyz, e2, e4 = metric_terms(qx, qy, qz)
    center = phi[2:-2, 2:-2, 2:-2]
    sigma = center[..., 0]
    V = potential_sigma(sigma)
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
    eig = np.linalg.eigvalsh(stress)
    dec_margin = rho - np.max(np.abs(eig), axis=-1)
    local_scale = rho + np.max(np.abs(eig), axis=-1) + 1.0e-14
    min_dec_scaled = float(np.min(dec_margin / local_scale))

    trace_scale = (
        rho
        + np.sum(np.abs(eig), axis=-1)
        + 2.0 * e4
        + 2.0 * np.abs(V)
        + 1.0e-14
    )
    max_trace = float(np.max(np.abs(active_from_stress - active) / trace_scale))

    volume = dx**3
    E2 = float(np.sum(e2) * volume)
    E4 = float(np.sum(e4) * volume)
    E0 = float(np.sum(V) * volume)
    E = E2 + E4 + E0
    active_weights = active.ravel() * volume
    active_total = float(np.sum(active_weights))

    coords = axis[2:-2]
    X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")
    radii = np.sqrt(X * X + Y * Y + Z * Z).ravel()
    order = np.argsort(radii)
    cumulative = np.cumsum(active_weights[order])
    min_active_fraction = float(np.min(cumulative) / max(E, 1.0e-300))

    weights = rho * volume
    wsum = float(np.sum(weights))
    centroid = np.array([
        float(np.sum(weights * X) / max(wsum, 1.0e-300)),
        float(np.sum(weights * Y) / max(wsum, 1.0e-300)),
        float(np.sum(weights * Z) / max(wsum, 1.0e-300)),
    ])

    t4 = topology4(phi, dx)
    degrees = tuple(int(x) for x in cr2.geometric_degrees(phi))

    return PhysicalDiagnostics(
        energy_continuum=E,
        e2=E2,
        e4=E4,
        e0=E0,
        active_total=active_total,
        active_to_energy=active_total / max(E, 1.0e-300),
        min_active_fraction=min_active_fraction,
        topology4=t4,
        topology4_relerr=abs(abs(t4) / B - 1.0),
        geometric_degrees=degrees,
        max_neighbor_angle=max_neighbor_angle(phi),
        min_dec_scaled_margin=min_dec_scaled,
        max_active_trace_scaled=max_trace,
        energy_centroid_norm=float(np.linalg.norm(centroid)),
    )


def fibonacci_sphere(n: int) -> np.ndarray:
    k = np.arange(n, dtype=float)
    golden = math.pi * (3.0 - math.sqrt(5.0))
    z = 1.0 - 2.0 * (k + 0.5) / n
    rxy = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    az = golden * k
    vec = np.column_stack([rxy * np.cos(az), rxy * np.sin(az), z])
    return vec / np.linalg.norm(vec, axis=1)[:, None]


def analytic_uniform_sphere_payload_average(
    source_xyz: np.ndarray,
    source_weight: np.ndarray,
    centers: np.ndarray,
    payload_radius: float,
    batch_size: int = 16,
) -> np.ndarray:
    result = np.zeros((len(centers), 3), dtype=float)
    r3 = float(payload_radius**3)
    for start in range(0, len(centers), batch_size):
        stop = min(start + batch_size, len(centers))
        q = source_xyz[None, :, :] - centers[start:stop, None, :]
        d2 = np.sum(q * q, axis=-1)
        d = np.sqrt(np.maximum(d2, 0.0))
        denom = np.where(d < payload_radius, r3, np.maximum(d2 * d, 1.0e-300))
        result[start:stop] = np.sum(
            source_weight[None, :, None] * q / denom[:, :, None],
            axis=1,
        )
    return result


def payload_diagnostics(
    phi: np.ndarray,
    axis: np.ndarray,
    dx: float,
    center_radius: float,
    payload_radius: float,
) -> PayloadDiagnostics:
    qx, qy, qz = central4_derivatives(phi, dx)
    _, _, _, _, _, _, _, e4 = metric_terms(qx, qy, qz)
    center = phi[2:-2, 2:-2, 2:-2]
    V = potential_sigma(center[..., 0])
    active = 2.0 * (e4 - V)

    coords = axis[2:-2]
    X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")
    xyz = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    weight = active.ravel() * dx**3

    vectors = fibonacci_sphere(DENSE_ORIENTATION_N)
    centers = float(center_radius) * vectors
    avg = analytic_uniform_sphere_payload_average(
        xyz,
        weight,
        centers,
        float(payload_radius),
    )
    radial = np.sum(avg * vectors, axis=1)
    transverse_vec = avg - radial[:, None] * vectors
    transverse = np.linalg.norm(transverse_vec, axis=1)
    worst = int(np.argmin(radial))
    ratio = transverse / np.maximum(radial, 1.0e-300)

    return PayloadDiagnostics(
        min_radial=float(np.min(radial)),
        max_radial=float(np.max(radial)),
        mean_radial=float(np.mean(radial)),
        max_transverse=float(np.max(transverse)),
        max_transverse_over_radial=float(np.max(ratio)),
        worst_orientation=vectors[worst],
        all_outward=bool(np.all(radial > MIN_DENSE_RADIAL_OUTWARD)),
    )


def print_relax(prefix: str, r: RelaxResult) -> None:
    print(f"{prefix}_RELAX_INITIAL_ENERGY={r.initial_energy:.15e}")
    print(f"{prefix}_RELAX_FINAL_ENERGY={r.final_energy:.15e}")
    print(f"{prefix}_RELAX_ENERGY_DROP_FRACTION={(r.initial_energy-r.final_energy)/max(r.initial_energy,1e-300):.15e}")
    print(f"{prefix}_RELAX_INITIAL_GRAD_RMS={r.initial_grad_rms:.15e}")
    print(f"{prefix}_RELAX_FINAL_GRAD_RMS={r.final_grad_rms:.15e}")
    print(f"{prefix}_RELAX_FINAL_GRAD_MAX={r.final_grad_max:.15e}")
    print(f"{prefix}_RELAX_ACCEPTED_STEPS={r.accepted_steps}")
    print(f"{prefix}_RELAX_REJECTED_ENERGY_TRIALS={r.rejected_energy_trials}")
    print(f"{prefix}_RELAX_REJECTED_TOPOLOGY_TRIALS={r.rejected_topology_trials}")
    print(f"{prefix}_RELAX_REJECTED_SMOOTHNESS_TRIALS={r.rejected_smoothness_trials}")
    print(f"{prefix}_RELAX_LINE_SEARCH_FAILED=" + ("YES" if r.line_search_failed else "NO"))
    print(f"{prefix}_RELAX_CONVERGED=" + ("YES" if r.converged else "NO"))
    print(f"{prefix}_RELAX_FINAL_TOPOLOGY4={r.final_topology4:.15e}")
    print(f"{prefix}_RELAX_FINAL_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in r.final_geometric_degrees))
    print(f"{prefix}_RELAX_FINAL_MAX_NEIGHBOR_ANGLE={r.final_max_neighbor_angle:.15e}")


def print_physical(prefix: str, d: PhysicalDiagnostics) -> None:
    print(f"{prefix}_CONTINUUM_ENERGY={d.energy_continuum:.15e}")
    print(f"{prefix}_CONTINUUM_E2={d.e2:.15e}")
    print(f"{prefix}_CONTINUUM_E4={d.e4:.15e}")
    print(f"{prefix}_CONTINUUM_E0={d.e0:.15e}")
    print(f"{prefix}_ACTIVE_TOTAL={d.active_total:.15e}")
    print(f"{prefix}_ACTIVE_TO_ENERGY={d.active_to_energy:.15e}")
    print(f"{prefix}_MIN_ACTIVE_FRACTION={d.min_active_fraction:.15e}")
    print(f"{prefix}_TOPOLOGY4={d.topology4:.15e}")
    print(f"{prefix}_TOPOLOGY4_RELERR={d.topology4_relerr:.15e}")
    print(f"{prefix}_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in d.geometric_degrees))
    print(f"{prefix}_MAX_NEIGHBOR_ANGLE={d.max_neighbor_angle:.15e}")
    print(f"{prefix}_MIN_DEC_SCALED_MARGIN={d.min_dec_scaled_margin:.15e}")
    print(f"{prefix}_MAX_ACTIVE_TRACE_SCALED={d.max_active_trace_scaled:.15e}")
    print(f"{prefix}_ENERGY_CENTROID_NORM={d.energy_centroid_norm:.15e}")


def print_payload(prefix: str, p: PayloadDiagnostics) -> None:
    print(f"{prefix}_DENSE_ORIENTATION_COUNT={DENSE_ORIENTATION_N}")
    print(f"{prefix}_MIN_RADIAL_OUTWARD={p.min_radial:.15e}")
    print(f"{prefix}_MAX_RADIAL_OUTWARD={p.max_radial:.15e}")
    print(f"{prefix}_MEAN_RADIAL_OUTWARD={p.mean_radial:.15e}")
    print(f"{prefix}_MAX_TRANSVERSE={p.max_transverse:.15e}")
    print(f"{prefix}_MAX_TRANSVERSE_OVER_RADIAL={p.max_transverse_over_radial:.15e}")
    print(
        f"{prefix}_WORST_RADIAL_ORIENTATION=("
        f"{p.worst_orientation[0]:.12e},"
        f"{p.worst_orientation[1]:.12e},"
        f"{p.worst_orientation[2]:.12e})"
    )
    print(f"{prefix}_DENSE_FINITE_PAYLOAD_OUTWARD=" + ("PASS" if p.all_outward else "FAIL"))


def initial_pass(phi: np.ndarray, dx: float, continuum_energy: float, cr2) -> tuple[bool, float, tuple[int, ...], float]:
    E, _, E4, _, _ = high_order_energy_gradient(phi, dx, False)
    # Continuum E4 is read separately by caller through relative-error output;
    # here the decisive representation checks are total energy + topology.
    t4 = topology4(phi, dx)
    degrees = tuple(int(x) for x in cr2.geometric_degrees(phi))
    angle = max_neighbor_angle(phi)
    passed = (
        relative_error(E, continuum_energy) <= MAX_INITIAL_ENERGY_RELERR
        and abs(abs(t4) / B - 1.0) <= MAX_INITIAL_TOPOLOGY_RELERR
        and all(abs(d) == B for d in degrees)
        and len(set(np.sign(d) for d in degrees)) == 1
        and angle <= MAX_NEIGHBOR_ANGLE
    )
    return passed, E4, degrees, angle


def main() -> None:
    print("=== 023CR3 — GEOMETRIC-DEGREE-GUARDED UNRESTRICTED RELAXATION ===")

    print("\n=== A — UPSTREAM 023CR2 AUDIT ===")
    for p in (A23_SOURCE, B23_SOURCE, C23_SOURCE, CR2_SOURCE, CR2_LOG):
        require_file(p)
    hashes = {
        "023A": sha256(A23_SOURCE),
        "023B": sha256(B23_SOURCE),
        "023C": sha256(C23_SOURCE),
        "023CR2": sha256(CR2_SOURCE),
    }
    expected = {
        "023A": EXPECTED_023A_SHA256,
        "023B": EXPECTED_023B_SHA256,
        "023C": EXPECTED_023C_SHA256,
        "023CR2": EXPECTED_023CR2_SHA256,
    }
    for k, v in hashes.items():
        print(f"{k}_SOURCE_SHA256={v}")
    log_text = CR2_LOG.read_text(errors="replace")
    markers = (
        "INITIAL_HIGH_ORDER_RESOLUTION_PAIR=N57_N65",
        "INITIAL_GEOMETRIC_B7_DEGREE=PASS",
        "023CR2_HIGH_ORDER_GEOMETRIC_TOPOLOGY_PREFLIGHT=GREEN_NUMERICAL_REPRESENTATION_REPAIR",
        "CARTESIAN_B7_REPRESENTATION=PROMOTION_GRADE_FOR_RELAXATION",
    )
    upstream_ok = all(hashes[k] == expected[k] for k in expected) and all(m in log_text for m in markers)
    print("UPSTREAM_023CR2_AUDIT=" + ("PASS" if upstream_ok else "FAIL"))
    if not upstream_ok:
        raise RuntimeError("023CR2 audit failed")

    print("\n=== B — HIGH-ORDER ACTION GRADIENT SELFCHECK ===")
    grad_rel, grad_ok = gradient_selfcheck()
    print(f"HIGH_ORDER_ACTION_GRADIENT_DIRECTIONAL_RELERR={grad_rel:.15e}")
    print("HIGH_ORDER_ACTION_GRADIENT_SELFCHECK=" + ("PASS" if grad_ok else "FAIL"))
    if not grad_ok:
        raise RuntimeError("High-order action gradient selfcheck failed")

    a23 = load_module("a23_for_023cr3", A23_SOURCE)
    b23 = load_module("b23_for_023cr3", B23_SOURCE)
    c23 = load_module("c23_for_023cr3", C23_SOURCE)
    cr2 = load_module("cr2_for_023cr3", CR2_SOURCE)

    print("\n=== C — CONTINUUM SELECTED-CANDIDATE RECONSTRUCTION ===")
    degree, I_direct = b23.angular_integrals_b7(b23.B7_B0)
    profile = b23.solve_profile_with_custom_I(a23, B, ETA, MASS, I_direct)
    sector_profiles, sector_energies = b23.solve_exact_sector(a23, ETA, MASS)
    selected = b23.candidate_from_sector(a23, sector_profiles, sector_energies, B)
    continuum_energy = 4.0 * math.pi * float(profile.E)
    continuum_e4 = 4.0 * math.pi * float(profile.E4)
    cr_source = load_module("cr_source_for_023cr3", ROOT / "simulations/023cr_checkerboard_free_link_lattice_topology_repair.py")
    half_domain, r_tail, boundary_f = cr_source.choose_compact_half_domain(
        profile,
        selected.payload.payload_center,
        selected.payload.payload_radius,
    )
    print(f"DIRECT_MAP_DEGREE={degree:.15e}")
    print(f"DIRECT_MAP_I={I_direct:.15e}")
    print(f"CONTINUUM_ENERGY={continuum_energy:.15e}")
    print(f"CONTINUUM_E4={continuum_e4:.15e}")
    print(f"PAYLOAD_CENTER={selected.payload.payload_center:.15e}")
    print(f"PAYLOAD_RADIUS={selected.payload.payload_radius:.15e}")
    print(f"HALF_DOMAIN={half_domain:.15e}")
    print(f"R_TAIL={r_tail:.15e}")
    print(f"PROFILE_F_AT_FACE={boundary_f:.15e}")

    results: dict[int, tuple[np.ndarray, np.ndarray, float, RelaxResult, PhysicalDiagnostics, PayloadDiagnostics]] = {}

    for n in GRID_LEVELS:
        print(f"\n=== D{n} — N={n} INITIAL RECONSTRUCTION + UNRESTRICTED RELAXATION ===")
        phi, axis, dx = c23.sample_rational_map_field(profile, b23.B7_B0, n, half_domain)
        enforce_vacuum_boundary(phi)
        phi = normalize_field(phi)

        initial_E, initial_E2, initial_E4, initial_E0, _ = high_order_energy_gradient(phi, dx, False)
        initial_t4 = topology4(phi, dx)
        initial_degrees = tuple(int(x) for x in cr2.geometric_degrees(phi))
        initial_angle = max_neighbor_angle(phi)
        initial_ok = (
            relative_error(initial_E, continuum_energy) <= MAX_INITIAL_ENERGY_RELERR
            and relative_error(initial_E4, continuum_e4) <= MAX_INITIAL_E4_RELERR
            and abs(abs(initial_t4) / B - 1.0) <= MAX_INITIAL_TOPOLOGY_RELERR
            and all(abs(d) == B for d in initial_degrees)
            and len(set(np.sign(d) for d in initial_degrees)) == 1
            and initial_angle <= MAX_NEIGHBOR_ANGLE
        )
        p = f"N{n}"
        print(f"{p}_DX={dx:.15e}")
        print(f"{p}_INITIAL_HIGH_ORDER_ENERGY={initial_E:.15e}")
        print(f"{p}_INITIAL_HIGH_ORDER_E2={initial_E2:.15e}")
        print(f"{p}_INITIAL_HIGH_ORDER_E4={initial_E4:.15e}")
        print(f"{p}_INITIAL_HIGH_ORDER_E0={initial_E0:.15e}")
        print(f"{p}_INITIAL_ENERGY_RELERR={relative_error(initial_E, continuum_energy):.15e}")
        print(f"{p}_INITIAL_E4_RELERR={relative_error(initial_E4, continuum_e4):.15e}")
        print(f"{p}_INITIAL_TOPOLOGY4={initial_t4:.15e}")
        print(f"{p}_INITIAL_TOPOLOGY4_RELERR={abs(abs(initial_t4)/B-1.0):.15e}")
        print(f"{p}_INITIAL_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in initial_degrees))
        print(f"{p}_INITIAL_MAX_NEIGHBOR_ANGLE={initial_angle:.15e}")
        print(f"{p}_INITIAL_RECONSTRUCTION=" + ("PASS" if initial_ok else "FAIL"))
        if not initial_ok:
            print("023CR3_GEOMETRIC_DEGREE_GUARDED_UNRESTRICTED_RELAXATION=INCOMPLETE_NUMERICAL_GATE")
            print("UNRESTRICTED_CARTESIAN_STATIONARY_FIELD=NOT_ESTABLISHED")
            print("NEXT=REPAIR_INITIAL_RECONSTRUCTION_BEFORE_RELAXATION")
            return

        relax = relax_field(phi, dx, cr2)
        print_relax(p, relax)
        physical = continuum_local_diagnostics(relax.field, axis, dx, cr2)
        print_physical(p + "_RELAXED", physical)
        payload = payload_diagnostics(
            relax.field,
            axis,
            dx,
            selected.payload.payload_center,
            selected.payload.payload_radius,
        )
        print_payload(p + "_RELAXED", payload)

        results[n] = (relax.field, axis, dx, relax, physical, payload)

    print("\n=== E — TWO-RESOLUTION RELAXED CONVERGENCE ===")
    _, _, _, r57, d57, p57 = results[57]
    field65, axis65, dx65, r65, d65, p65 = results[65]

    energy_pair = relative_error(d57.energy_continuum, d65.energy_continuum)
    active_pair = abs(d57.min_active_fraction - d65.min_active_fraction)
    payload_pair = relative_error(p57.min_radial, p65.min_radial)
    topo_pair = abs(abs(d57.topology4) - abs(d65.topology4)) / B
    pair_ok = (
        energy_pair <= MAX_RELAXED_ENERGY_PAIR_RELCHANGE
        and active_pair <= MAX_RELAXED_ACTIVE_PAIR_ABSCHANGE
        and payload_pair <= MAX_RELAXED_PAYLOAD_PAIR_RELCHANGE
        and topo_pair <= MAX_RELAXED_TOPOLOGY_PAIR_ABSCHANGE
    )
    print(f"RELAXED_N57_N65_ENERGY_RELCHANGE={energy_pair:.15e}")
    print(f"RELAXED_N57_N65_ACTIVE_FRACTION_ABSCHANGE={active_pair:.15e}")
    print(f"RELAXED_N57_N65_MIN_PAYLOAD_RELCHANGE={payload_pair:.15e}")
    print(f"RELAXED_N57_N65_TOPOLOGY_ABSCHANGE={topo_pair:.15e}")
    print("RELAXED_N57_N65_CONVERGENCE=" + ("PASS" if pair_ok else "FAIL"))

    print("\n=== F — PHYSICAL PROMOTION CHECKS ===")
    per_grid = []
    for n in GRID_LEVELS:
        _, _, _, relax, diag, payload = results[n]
        degree_ok = all(abs(d) == B for d in diag.geometric_degrees) and len(set(np.sign(d) for d in diag.geometric_degrees)) == 1
        topo_ok = diag.topology4_relerr <= MAX_GUARD_TOPOLOGY_RELERR
        smooth_ok = diag.max_neighbor_angle <= MAX_NEIGHBOR_ANGLE
        active_positive = diag.active_total > 0.0
        negative_core = diag.min_active_fraction <= -MIN_NEGATIVE_ACTIVE_FRACTION
        dec_ok = diag.min_dec_scaled_margin >= MIN_DEC_SCALED_MARGIN
        trace_ok = diag.max_active_trace_scaled <= MAX_ACTIVE_TRACE_SCALED
        payload_ok = payload.all_outward
        stationarity_ok = relax.converged and not relax.line_search_failed
        grid_ok = all((
            stationarity_ok,
            degree_ok,
            topo_ok,
            smooth_ok,
            active_positive,
            negative_core,
            dec_ok,
            trace_ok,
            payload_ok,
        ))
        per_grid.append(grid_ok)
        p = f"N{n}"
        print(f"{p}_UNRESTRICTED_STATIONARITY=" + ("PASS" if stationarity_ok else "FAIL"))
        print(f"{p}_GEOMETRIC_B7_DEGREE=" + ("PASS" if degree_ok else "FAIL"))
        print(f"{p}_DERIVATIVE_TOPOLOGY=" + ("PASS" if topo_ok else "FAIL"))
        print(f"{p}_LATTICE_SMOOTHNESS=" + ("PASS" if smooth_ok else "FAIL"))
        print(f"{p}_POSITIVE_TOTAL_ACTIVE_MASS=" + ("PASS" if active_positive else "FAIL"))
        print(f"{p}_NEGATIVE_ENCLOSED_ACTIVE_MASS=" + ("PASS" if negative_core else "FAIL"))
        print(f"{p}_POINTWISE_DEC=" + ("PASS" if dec_ok else "FAIL"))
        print(f"{p}_ACTIVE_TRACE_IDENTITY=" + ("PASS" if trace_ok else "FAIL"))
        print(f"{p}_DENSE_FINITE_PAYLOAD_OUTWARD=" + ("PASS" if payload_ok else "FAIL"))
        print(f"{p}_PHYSICAL_RELAXATION_GATE=" + ("PASS" if grid_ok else "FAIL"))

    green = grad_ok and pair_ok and all(per_grid)

    # Preserve the highest-resolution relaxed field whenever it is a valid B=7
    # smooth field, even if an operational gravity gate fails.  This makes the
    # negative result reproducible and permits an independent audit.
    primary_degree_ok = all(abs(d) == B for d in d65.geometric_degrees)
    if primary_degree_ok and d65.max_neighbor_angle <= MAX_NEIGHBOR_ANGLE:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            ARTIFACT,
            phi=field65,
            axis=axis65,
            dx=np.array(dx65),
            B=np.array(B),
            eta=np.array(ETA),
            mass=np.array(MASS),
            high_order_energy=np.array(r65.final_energy),
            continuum_energy=np.array(d65.energy_continuum),
            active_total=np.array(d65.active_total),
            min_active_fraction=np.array(d65.min_active_fraction),
            topology4=np.array(d65.topology4),
            geometric_degrees=np.array(d65.geometric_degrees, dtype=int),
            payload_min_radial=np.array(p65.min_radial),
        )
        print(f"RELAXED_FIELD_ARTIFACT={ARTIFACT.relative_to(ROOT)}")
    else:
        print("RELAXED_FIELD_ARTIFACT=NOT_WRITTEN_INVALID_TOPOLOGY_OR_SMOOTHNESS")

    print("\n=== G — 023CR3 DECISION ===")
    if green:
        print("023CR3_GEOMETRIC_DEGREE_GUARDED_UNRESTRICTED_RELAXATION=GREEN_UNRESTRICTED_STATIONARY_FIELD")
        print("UNRESTRICTED_CARTESIAN_STATIONARY_B7_FIELD=SUPPORTED")
        print("FINITE_PAYLOAD_REPULSION_AFTER_UNRESTRICTED_RELAXATION=SUPPORTED")
        print("FULL_PHYSICAL_HESSIAN=NOT_YET_TESTED")
        print("HEURISTIC_PROMOTION_FROM_023CR3=NO_WAIT_FOR_FULL_PHYSICAL_HESSIAN")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
        print("NEXT=023C2_CORRECTED_FULL_PHYSICAL_HESSIAN")
    else:
        numerically_admissible = all(
            results[n][3].converged
            and all(abs(d) == B for d in results[n][4].geometric_degrees)
            and results[n][4].max_neighbor_angle <= MAX_NEIGHBOR_ANGLE
            for n in GRID_LEVELS
        )
        physical_loss = numerically_admissible and all(
            (results[n][4].active_total <= 0.0 or not results[n][5].all_outward)
            for n in GRID_LEVELS
        )
        if physical_loss:
            print("023CR3_GEOMETRIC_DEGREE_GUARDED_UNRESTRICTED_RELAXATION=GREEN_NEGATIVE_PHYSICAL_RESULT")
            print("UNRESTRICTED_CARTESIAN_STATIONARY_B7_FIELD=SUPPORTED_BUT_REPULSIVE_OPERATIONAL_GATE_FAILED")
            print("NEXT=PRESERVE_NEGATIVE_RESULT_AND_RERANK_FALSE_CORE_CANDIDATES")
        else:
            print("023CR3_GEOMETRIC_DEGREE_GUARDED_UNRESTRICTED_RELAXATION=INCOMPLETE_NUMERICAL_OR_STATIONARITY_GATE")
            print("UNRESTRICTED_CARTESIAN_STATIONARY_B7_FIELD=NOT_YET_ESTABLISHED")
            print("NEXT=INSPECT_FIRST_FAILED_GATE_BEFORE_HESSIAN")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")

    print("UNRESTRICTED_CARTESIAN_3D_STABILITY=NOT_YET_ESTABLISHED_UNTIL_HESSIAN")
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_ESTABLISHED")
    print("PRACTICAL_ENERGY_SCALING=STILL_CATASTROPHIC_IN_PURE_GR")
    print("REAL_MATERIAL=NO")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023CR3_GEOMETRIC_DEGREE_GUARDED_UNRESTRICTED_RELAXATION")


if __name__ == "__main__":
    main()
