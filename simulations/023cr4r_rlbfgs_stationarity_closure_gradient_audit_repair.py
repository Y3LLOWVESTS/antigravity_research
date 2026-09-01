#!/usr/bin/env python3
"""023CR4 — Riemannian L-BFGS stationarity closure for the unrestricted B=7 field.

PURPOSE
-------
Close the only surviving 023CR3R primary-field blocker as efficiently and
conservatively as possible: strict stationarity of the topology-preserving
unrestricted Cartesian B=7 false-core Skyrmion.

023CR3R already drove the N=65 field from gradient RMS 4.625 to 0.01025 while
preserving geometric degree |B|=7, derivative topology, lattice smoothness,
positive total active mass, a negative enclosed active region, pointwise DEC,
the active-trace identity, and outward finite-payload gravity in all 320 tested
orientations.  It did not satisfy the predeclared strict stationarity tolerance
RMS <= 1.5e-3 (although its max residual 0.0656 was already close to the 0.05
pointwise threshold).

SCIENTIFIC QUESTION
-------------------
Is the remaining Euler-Lagrange residual merely slow first-order optimizer
convergence, or does it reveal a localized numerical/physical obstruction?

CHEAPEST DECISIVE EXPERIMENT
----------------------------
1. Audit the saved 023CR3R N=65 field and exact discrete gradient.
2. Localize the residual before changing the field.
3. Continue the SAME discrete action on the SAME S^3 product manifold with a
   limited-memory Riemannian quasi-Newton method (R-LBFGS), using exact
   sitewise parallel transport along the exponential-map update.
4. Preserve the original topology, smoothness, and strict stationarity gates.
5. Avoid the expensive 320-direction payload calculation during optimization.
   A single previously worst-direction payload sentinel is cheap and diagnostic
   only.  The complete 320-direction audit is performed once, only after strict
   stationarity is achieved.

PHYSICAL MODEL / ACTION
-----------------------
No physics is changed relative to 023CR3/023CR3R.  The high-order
checkerboard-free Cartesian action is imported verbatim from 023CR3:

    E = integral (e2 + e4 + V) d^3x,

    e2 = sum_i d_i phi . d_i phi,

    e4 = sum_{i<j} [|d_i phi|^2 |d_j phi|^2
                    - (d_i phi . d_j phi)^2],

    V = m^2 (1-sigma)(1+eta sigma),

with phi=(sigma,pi_1,pi_2,pi_3) constrained pointwise to S^3 and fixed vacuum
boundary phi=(1,0,0,0).

The operational linearized-GR active source remains

    S = rho + tr(T) = 2(e4 - V).

INPUTS
------
- `results/data/023cr3r_stationary_b7_n65.npz`, or this file's own later
  checkpoint if present;
- audited 023CR2/023CR3/023CR3R source files and the 023CR3R log;
- optional `AG_RLBFGS_MAX_ACCEPTED` environment variable controlling the
  maximum accepted quasi-Newton steps in one invocation.

OUTPUTS
-------
- printed residual-localization, convergence, topology, and physical gates;
- `results/data/023cr4r_n65_rlbfgs_checkpoint.npz`;
- on strict stationary success,
  `results/data/023cr4r_strict_stationary_b7_n65.npz`.

UNITS / NORMALIZATION
---------------------
Dimensionless Skyrme units, identical to 023BR--023CR3R.  B=7, eta=0.4,
m=8.  No rescaling or threshold changes are introduced here.

SIGN / COORDINATE CONVENTIONS
-----------------------------
The inherited baryon-number orientation is negative on the sampled B=7 map,
so the geometric witnesses are expected to report -7 while promotion uses
|B|=7.  Positive payload radial kernel means outward acceleration in the
project's linearized-GR convention.  Cartesian coordinates are centered on the
energy centroid with a fixed true-vacuum outer boundary.

ASSUMPTIONS / PHYSICAL CONSTRAINTS
----------------------------------
Flat-spacetime static Skyrme matter is used for this gate.  Gravity is only an
operational linearized-GR readout after stationarity.  Pointwise S^3 unit norm,
fixed vacuum boundary, geometric topological degree, derivative topology, DEC,
positive total active mass, and the negative-active-core threshold are all
retained from the upstream gates.

OPTIMIZER
---------
R-LBFGS is used because the current state is already close to stationarity and
first-order NCG/BB convergence has become slow.  At each accepted exponential
map step, all stored secant vectors are exactly parallel transported along the
sitewise S^3 geodesic.  A cautious positive-curvature update is required before
adding a secant pair.  If the quasi-Newton direction ceases to be descent, the
history is discarded and a steepest-descent direction is used.

Armijo backtracking, the 023CR3 topology-4 bound, the exact geometric degree
guard, maximum-neighbor-angle smoothness guard, and fixed vacuum boundary are
retained.  No symmetry, rational-map, radial-profile, or stabilizer constraint
is added.

RESIDUAL LOCALIZATION
---------------------
Before optimization the code reports:
- gradient RMS and max;
- coordinate/radius and boundary distance of the maximum residual;
- fractions of squared residual in boundary/tail/core/wall-like regions;
- a directional finite-difference check at the saved field.

This separates a genuine interior Euler-Lagrange residual from a boundary or
stencil artifact before interpreting stationarity.

CHECKPOINTING / RUN LENGTH
--------------------------
The R-LBFGS field is checkpointed every 10 accepted steps and at exit.  A later
invocation automatically resumes from that checkpoint.  The maximum accepted
steps per invocation is controlled by environment variable

    AG_RLBFGS_MAX_ACCEPTED

(default 80).  Thus this gate can be run in short pieces without losing work.

PROMOTION CONDITION
-------------------
This gate is GREEN_STRICT_STATIONARY_N65 only if all of the following hold:

    SAVED_FIELD_AUDIT=PASS
    SAVED_FIELD_DIRECTIONAL_GRADIENT_CHECK=PASS_EPSILON_PLATEAU
    FINAL_GRAD_RMS <= 1.5e-3
    FINAL_GRAD_MAX <= 5.0e-2
    |B_geometric| = 7 for all three independent targets
    topology4 relative error <= 3e-2
    max neighbor angle <= 0.70
    positive total active mass
    min enclosed active fraction <= -1e-2
    pointwise DEC pass
    active-trace identity pass
    all 320 finite-payload orientations outward

A GREEN result establishes an unrestricted stationary N=65 field only.  It
DOES NOT establish stability.  The next mandatory gate remains a full physical
tangent-space Hessian plus the explicit fission/deformation challenge before
023D Einstein-Skyrme continuation is authorized.

FALSIFIERS / STOP RULE
----------------------
- Loss of B=7 under smooth admissible updates blocks promotion.
- Loss of positive total active mass, negative active core, DEC, or stationary
  320-direction outward payload response is a physical blocker to this branch.
- Failure to reach strict stationarity with continued substantial residual
  decrease is numerical incompleteness; rerun from checkpoint.
- Genuine R-LBFGS stagnation with localized residual authorizes a targeted
  Newton-Krylov/preconditioner gate, not a physics claim.
- Do not weaken the stationarity thresholds.

KNOWN LIMITATIONS / INTERPRETATION
----------------------------------
N=65 stationarity alone is not a stability proof and is not a continuum-limit
proof.  R-LBFGS can establish a stationary point but cannot determine whether
its physical Hessian has a negative mode.  The complete 023C promotion still
requires companion-resolution convergence, full tangent-space Hessian checks,
and explicit fission/deformation challenges.  Einstein backreaction, practical
energy scaling, real materials, and a device remain outside this file.

VALIDATION
----------
- Upstream source hashes and 023CR3R artifact metadata are fail-closed.
- The 023CR3 synthetic exact-gradient selfcheck is rerun.
- A saved-field epsilon sweep with independent second- and fourth-order
  directional derivatives is performed to distinguish truncation error from
  cancellation near stationarity.
- R-LBFGS energy must be monotone under Armijo acceptance.
- Geometric topology is checked periodically and at the end.
- The complete physical and 320-direction payload audit is deferred until
  strict stationarity, avoiding repeated expensive work.

RELATED FILES / TESTS
---------------------
- `simulations/023cr2_high_order_geometric_topology_preflight.py`
- `simulations/023cr3_geometric_degree_guarded_unrestricted_relaxation.py`
- `simulations/023cr3r_stationarity_continuation_and_optimizer_crosscheck.py`
- `tests/known_solutions/` regression baseline (94 tests at current checkpoint)

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023CR4R_GRADIENT_AUDIT_AND_RLBFGS_STATIONARITY_CLOSURE
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


ROOT = Path(__file__).resolve().parents[1]
CR2_SOURCE = ROOT / "simulations/023cr2_high_order_geometric_topology_preflight.py"
CR3_SOURCE = ROOT / "simulations/023cr3_geometric_degree_guarded_unrestricted_relaxation.py"
CR3R_SOURCE = ROOT / "simulations/023cr3r_stationarity_continuation_and_optimizer_crosscheck.py"
CR3R_LOG = ROOT / "results/logs/023cr3r_stationarity_continuation_and_optimizer_crosscheck.log"
CR3R_ARTIFACT = ROOT / "results/data/023cr3r_stationary_b7_n65.npz"

EXPECTED_CR2_SHA256 = "6affc28547b7849140f1eacf6992c9541ea9ba9a7c306e69121ca60ef76ad1db"
EXPECTED_CR3_SHA256 = "350868726af644d1a8bb2970b559c92e1febc4ea261f409ab38c1dca64ac97da"
EXPECTED_CR3R_SHA256 = "545770186fca2b319e37e3882a4f280eb40093a11fe59f95f40ab6eaefab9306"

B = 7
ETA = 0.40
MASS = 8.0
GRAD_RMS_TOL = 1.5e-3
GRAD_MAX_TOL = 5.0e-2
MAX_NEIGHBOR_ANGLE = 0.70
MAX_TOPOLOGY_RELERR = 3.0e-2
MIN_NEGATIVE_ACTIVE_FRACTION = 1.0e-2
MIN_DEC_SCALED_MARGIN = -2.0e-8
MAX_ACTIVE_TRACE_SCALED = 2.0e-12
PAYLOAD_CENTER = 3.870161274564900e-01
PAYLOAD_RADIUS = 1.675735743205162e-02
KNOWN_WORST_DIRECTION = np.array(
    [-4.543501844638e-01, 1.878880658051e-02, 8.906250000000e-01], dtype=float
)
KNOWN_WORST_DIRECTION /= np.linalg.norm(KNOWN_WORST_DIRECTION)

HISTORY_SIZE = 7
ARMIJO_C1 = 1.0e-4
MAX_POINT_ROTATION = 0.045
MIN_ALPHA = 1.0e-12
MAX_LINESEARCH = 24
GEOMETRIC_GUARD_EVERY = 10
FULL_GEOMETRIC_GUARD_EVERY = 30
PROGRESS_EVERY = 5
CHECKPOINT_EVERY = 10
CAUTIOUS_CURVATURE = 1.0e-7
MAX_ACCEPTED_THIS_RUN = max(1, int(os.environ.get("AG_RLBFGS_MAX_ACCEPTED", "80")))

CHECKPOINT = ROOT / "results/data/023cr4r_n65_rlbfgs_checkpoint.npz"
FINAL_ARTIFACT = ROOT / "results/data/023cr4r_strict_stationary_b7_n65.npz"


@dataclass
class State:
    phi: np.ndarray
    axis: np.ndarray
    dx: float
    accepted_total: int


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def strict_stationarity(cr3, phi: np.ndarray, dx: float):
    E, E2, E4, E0, g = cr3.riemannian_gradient_density(phi, dx)
    rms, gmax = cr3.gradient_norms(g)
    ok = bool(rms <= GRAD_RMS_TOL and gmax <= GRAD_MAX_TOL)
    return float(E), float(E2), float(E4), float(E0), g, float(rms), float(gmax), ok


def load_start(cr3, cr2) -> tuple[State, str]:
    source = CHECKPOINT if CHECKPOINT.is_file() else CR3R_ARTIFACT
    with np.load(source, allow_pickle=False) as data:
        phi = np.array(data["phi"], dtype=float, copy=True)
        axis = np.array(data["axis"], dtype=float, copy=True)
        dx = float(data["dx"])
        b = int(data["B"]) if "B" in data.files else B
        eta = float(data["eta"]) if "eta" in data.files else ETA
        mass = float(data["mass"]) if "mass" in data.files else MASS
        accepted = int(data["accepted_total"]) if "accepted_total" in data.files else 0
        source_tag = str(data["source"]) if "source" in data.files else "UNKNOWN"
    cr3.enforce_vacuum_boundary(phi)
    phi = cr3.normalize_field(phi)
    if phi.shape != (65, 65, 65, 4):
        raise RuntimeError(f"Unexpected N65 field shape: {phi.shape}")
    if b != B or abs(eta - ETA) > 1e-14 or abs(mass - MASS) > 1e-14:
        raise RuntimeError("Saved-field parameter audit failed")
    allowed_source = source_tag in {"023CR3R_N65", "023CR4R_RLBFGS", "023CR4R_RLBFGS_EXIT"}
    if not allowed_source:
        raise RuntimeError(f"Unexpected saved-field source tag: {source_tag}")
    t4 = cr3.topology4(phi, dx)
    gok, degrees = cr3.geometric_guard(phi, cr2, True)
    angle = cr3.max_neighbor_angle(phi)
    ok = bool(
        gok
        and abs(abs(t4) / B - 1.0) <= MAX_TOPOLOGY_RELERR
        and angle <= MAX_NEIGHBOR_ANGLE
    )
    print(f"START_FIELD={source.relative_to(ROOT)}")
    print(f"START_FIELD_SHAPE={phi.shape}")
    print(f"START_DX={dx:.15e}")
    print(f"START_ACCEPTED_TOTAL={accepted}")
    print(f"START_SOURCE_TAG={source_tag}")
    print(f"START_TOPOLOGY4={t4:.15e}")
    print("START_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in degrees))
    print(f"START_MAX_NEIGHBOR_ANGLE={angle:.15e}")
    print("SAVED_FIELD_AUDIT=" + ("PASS" if ok else "FAIL"))
    if not ok:
        raise RuntimeError("Saved field failed topology/smoothness audit")
    return State(phi=phi, axis=axis, dx=dx, accepted_total=accepted), source.name


def residual_localization(cr3, state: State, g: np.ndarray) -> None:
    phi, axis = state.phi, state.axis
    nrm = np.linalg.norm(g, axis=-1)
    nrm2 = nrm * nrm
    interior = np.zeros(phi.shape[:3], dtype=bool)
    interior[1:-1, 1:-1, 1:-1] = True
    total = float(np.sum(nrm2[interior]))
    idx = np.unravel_index(int(np.argmax(nrm)), nrm.shape)
    x = np.array([axis[idx[0]], axis[idx[1]], axis[idx[2]]], dtype=float)
    radius = float(np.linalg.norm(x))
    boundary_cells = int(min(idx[0], idx[1], idx[2], phi.shape[0]-1-idx[0], phi.shape[1]-1-idx[1], phi.shape[2]-1-idx[2]))

    I, J, K = np.indices(phi.shape[:3])
    bd = np.minimum.reduce([I, J, K, phi.shape[0]-1-I, phi.shape[1]-1-J, phi.shape[2]-1-K])
    X, Y, Z = np.meshgrid(axis, axis, axis, indexing="ij")
    R = np.sqrt(X*X + Y*Y + Z*Z)

    def frac(mask):
        return float(np.sum(nrm2[mask & interior]) / max(total, 1e-300))

    print(f"RESIDUAL_MAX_INDEX={idx}")
    print(f"RESIDUAL_MAX_COORD=({x[0]:.12e},{x[1]:.12e},{x[2]:.12e})")
    print(f"RESIDUAL_MAX_RADIUS={radius:.15e}")
    print(f"RESIDUAL_MAX_BOUNDARY_DISTANCE_CELLS={boundary_cells}")
    print(f"RESIDUAL_L2_FRACTION_BOUNDARY_4={frac(bd <= 4):.15e}")
    print(f"RESIDUAL_L2_FRACTION_CORE_R_LT_0P30={frac(R < 0.30):.15e}")
    print(f"RESIDUAL_L2_FRACTION_WALL_R_0P30_TO_1P60={frac((R >= 0.30) & (R < 1.60)):.15e}")
    print(f"RESIDUAL_L2_FRACTION_TAIL_R_GE_1P60={frac(R >= 1.60):.15e}")


def saved_field_directional_check(cr3, state: State, g: np.ndarray):
    """Validate the saved-field analytic gradient without cancellation bias.

    The original 023CR4 check used one very small step, ``eps=2e-7``.  At the
    nearly stationary N=65 field the directional derivative is only O(1e-5)
    while the total discrete energy is O(1e3), so a single tiny central
    difference is vulnerable to subtraction roundoff.  This repair does not
    weaken the gradient requirement.  Instead it performs a deterministic
    epsilon sweep and uses two independent even-order finite-difference
    estimators:

    - second-order centered derivative ``D2(h)``;
    - fourth-order five-point derivative ``D4(h)``.

    A validation plateau is accepted only when two adjacent moderate step
    sizes simultaneously satisfy all of the following predeclared conditions:

    1. ``D4`` agrees with the analytic derivative to <= 5e-4 relative error;
    2. adjacent ``D4`` estimates agree to <= 5e-4 relative error;
    3. ``D2`` and ``D4`` at the finer step agree to <= 2e-3 relative error;
    4. the maximum sitewise geodesic perturbation is <= 5e-3 rad.

    The old ``eps=2e-7`` value remains printed as a diagnostic but is not used
    as the sole oracle.  Failure of the plateau blocks R-LBFGS exactly as a
    genuine gradient inconsistency should.
    """
    rng = np.random.default_rng(23064)
    v = np.zeros_like(state.phi)
    raw = rng.normal(size=v[3:-3, 3:-3, 3:-3].shape)
    v[3:-3, 3:-3, 3:-3] = raw
    v = cr3.project_tangent(state.phi, v)
    norm = math.sqrt(max(cr3.tangent_inner(v, v, state.dx), 1e-300))
    v /= norm

    analytic = cr3.tangent_inner(g, v, state.dx)
    local_vmax = float(np.max(np.linalg.norm(v, axis=-1)))
    Ecenter = cr3.high_order_energy_gradient(state.phi, state.dx, False)[0]

    # Moderate-to-small steps expose the expected truncation-to-roundoff
    # transition.  Values are fixed in advance and are not selected by an
    # optimizer or by the desired answer.
    eps_values = np.array(
        [2e-3, 1e-3, 5e-4, 2e-4, 1e-4, 5e-5, 2e-5, 1e-5,
         5e-6, 2e-6, 1e-6, 5e-7, 2e-7],
        dtype=float,
    )

    def energy_at(alpha: float) -> float:
        trial = cr3.exp_map_update(state.phi, v, alpha)
        return float(cr3.high_order_energy_gradient(trial, state.dx, False)[0])

    records = []
    for h in eps_values:
        Ep = energy_at(float(h))
        Em = energy_at(float(-h))
        Epp = energy_at(float(2.0*h))
        Emm = energy_at(float(-2.0*h))
        d2 = (Ep - Em) / (2.0*h)
        d4 = (-Epp + 8.0*Ep - 8.0*Em + Emm) / (12.0*h)
        denom = max(abs(analytic), abs(d4), 1e-12)
        rel_analytic = abs(d4 - analytic) / denom
        rel_d2_d4 = abs(d2 - d4) / max(abs(d2), abs(d4), 1e-12)
        roundoff_scale = (
            32.0 * np.finfo(float).eps
            * max(abs(Ecenter), abs(Ep), abs(Em), abs(Epp), abs(Emm), 1.0)
            / h
        )
        max_angle = h * local_vmax
        records.append((h, d2, d4, rel_analytic, rel_d2_d4, roundoff_scale, max_angle))
        print(
            f"SAVED_FIELD_EPS_SWEEP_H={h:.15e} "
            f"D2={d2:.15e} D4={d4:.15e} "
            f"D4_ANALYTIC_RELERR={rel_analytic:.15e} "
            f"D2_D4_RELERR={rel_d2_d4:.15e} "
            f"ROUND_OFF_DERIVATIVE_SCALE={roundoff_scale:.15e} "
            f"MAX_SITE_GEODESIC_STEP={max_angle:.15e}"
        )

    plateau_pairs = []
    for i in range(len(records)-1):
        h0, _, d40, rel0, _, _, ang0 = records[i]
        h1, d21, d41, rel1, d2d41, _, ang1 = records[i+1]
        adjacent = abs(d40 - d41) / max(abs(d40), abs(d41), 1e-12)
        pair_ok = bool(
            rel0 <= 5e-4
            and rel1 <= 5e-4
            and adjacent <= 5e-4
            and d2d41 <= 2e-3
            and max(ang0, ang1) <= 5e-3
        )
        print(
            f"SAVED_FIELD_EPS_PLATEAU_PAIR_H0={h0:.15e} H1={h1:.15e} "
            f"D4_ADJACENT_RELCHANGE={adjacent:.15e} "
            f"FINER_D2_D4_RELERR={d2d41:.15e} "
            f"PAIR_PASS={'YES' if pair_ok else 'NO'}"
        )
        if pair_ok:
            plateau_pairs.append((i, adjacent))

    # Preserve the exact old diagnostic for continuity with 023CR4.
    old = next(r for r in records if abs(r[0] - 2e-7) < 1e-20)
    old_h, old_d2, old_d4, old_rel, old_d2d4, _, _ = old
    print(f"SAVED_FIELD_DIRECTIONAL_OLD_EPS={old_h:.15e}")
    print(f"SAVED_FIELD_DIRECTIONAL_OLD_D2={old_d2:.15e}")
    print(f"SAVED_FIELD_DIRECTIONAL_OLD_D4={old_d4:.15e}")
    print(f"SAVED_FIELD_DIRECTIONAL_ANALYTIC={analytic:.15e}")
    print(f"SAVED_FIELD_DIRECTIONAL_OLD_D4_RELERR={old_rel:.15e}")
    print(f"SAVED_FIELD_DIRECTIONAL_OLD_D2_D4_RELERR={old_d2d4:.15e}")

    ok = len(plateau_pairs) >= 1
    if ok:
        i, adjacent = min(plateau_pairs, key=lambda p: p[1])
        h0, _, d40, rel0, _, _, _ = records[i]
        h1, _, d41, rel1, _, _, _ = records[i+1]
        print(f"SAVED_FIELD_DIRECTIONAL_VALIDATION_H_COARSE={h0:.15e}")
        print(f"SAVED_FIELD_DIRECTIONAL_VALIDATION_H_FINE={h1:.15e}")
        print(f"SAVED_FIELD_DIRECTIONAL_VALIDATION_D4_COARSE={d40:.15e}")
        print(f"SAVED_FIELD_DIRECTIONAL_VALIDATION_D4_FINE={d41:.15e}")
        print(f"SAVED_FIELD_DIRECTIONAL_VALIDATION_RELERR_COARSE={rel0:.15e}")
        print(f"SAVED_FIELD_DIRECTIONAL_VALIDATION_RELERR_FINE={rel1:.15e}")
        print(f"SAVED_FIELD_DIRECTIONAL_VALIDATION_ADJACENT_RELCHANGE={adjacent:.15e}")
    else:
        best = min(records, key=lambda r: r[3])
        print(f"SAVED_FIELD_DIRECTIONAL_BEST_H={best[0]:.15e}")
        print(f"SAVED_FIELD_DIRECTIONAL_BEST_D4={best[2]:.15e}")
        print(f"SAVED_FIELD_DIRECTIONAL_BEST_RELERR={best[3]:.15e}")

    print("SAVED_FIELD_DIRECTIONAL_GRADIENT_CHECK=" + ("PASS_EPSILON_PLATEAU" if ok else "FAIL_NO_VALIDATION_PLATEAU"))
    return ok


def transport_geometry(phi: np.ndarray, direction: np.ndarray, alpha: float, endpoint: np.ndarray):
    """Precompute geometry for exact product-S^3 parallel transport."""
    dnorm = np.linalg.norm(direction, axis=-1)
    mask = dnorm > 1e-14
    u = np.zeros_like(direction)
    u[mask] = direction[mask] / dnorm[mask, None]
    theta = alpha * dnorm
    return u, np.cos(theta), np.sin(theta), endpoint


def exact_parallel_transport(phi: np.ndarray, geom, v: np.ndarray, cr3) -> np.ndarray:
    """Exact sitewise S^3 parallel transport using precomputed geometry."""
    u, ctheta, stheta, endpoint = geom
    a = np.sum(v * u, axis=-1)
    out = np.array(v, copy=True)
    out += (a * (ctheta - 1.0))[..., None] * u - (a * stheta)[..., None] * phi
    # Numerical projection cleans roundoff at the endpoint.
    out = cr3.project_tangent(endpoint, out)
    out[0] = 0.0; out[-1] = 0.0
    out[:, 0] = 0.0; out[:, -1] = 0.0
    out[:, :, 0] = 0.0; out[:, :, -1] = 0.0
    return out


def two_loop_direction(cr3, g, history, dx):
    if not history:
        return -g, False
    q = np.array(g, copy=True)
    alphas = []
    for s, y, rho in reversed(history):
        a = rho * cr3.tangent_inner(s, q, dx)
        alphas.append(a)
        q -= a * y
    s_last, y_last, _ = history[-1]
    yy = cr3.tangent_inner(y_last, y_last, dx)
    sy = cr3.tangent_inner(s_last, y_last, dx)
    gamma = sy / max(yy, 1e-300)
    gamma = min(max(gamma, 1e-8), 1e8)
    r = gamma * q
    for (s, y, rho), a in zip(history, reversed(alphas)):
        beta = rho * cr3.tangent_inner(y, r, dx)
        r += s * (a - beta)
    return -r, True


def save_checkpoint(state: State, E: float, rms: float, gmax: float, source: str) -> None:
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        CHECKPOINT,
        phi=state.phi,
        axis=state.axis,
        dx=np.array(state.dx),
        B=np.array(B), eta=np.array(ETA), mass=np.array(MASS),
        accepted_total=np.array(state.accepted_total),
        energy=np.array(E), grad_rms=np.array(rms), grad_max=np.array(gmax),
        source=np.array(source),
    )
    print(f"CHECKPOINT_WRITTEN={CHECKPOINT.relative_to(ROOT)}")


def one_direction_payload(cr3, phi, axis, dx, direction):
    qx, qy, qz = cr3.central4_derivatives(phi, dx)
    _, _, _, _, _, _, _, e4 = cr3.metric_terms(qx, qy, qz)
    center_field = phi[2:-2, 2:-2, 2:-2]
    V = cr3.potential_sigma(center_field[..., 0])
    active = 2.0 * (e4 - V)
    coords = axis[2:-2]
    X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")
    xyz = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    weight = active.ravel() * dx**3
    center = PAYLOAD_CENTER * direction
    q = xyz - center[None, :]
    d2 = np.sum(q*q, axis=1)
    d = np.sqrt(np.maximum(d2, 0.0))
    denom = np.where(d < PAYLOAD_RADIUS, PAYLOAD_RADIUS**3, np.maximum(d2*d, 1e-300))
    avg = np.sum(weight[:, None] * q / denom[:, None], axis=0)
    return float(np.dot(avg, direction))


def rlbfgs(cr3, cr2, state: State):
    phi = state.phi
    dx = state.dx
    E, _, _, _, g, rms, gmax, station = strict_stationarity(cr3, phi, dx)
    history = []
    accepted_this = 0
    rejected_energy = 0
    rejected_topology = 0
    rejected_smooth = 0
    history_resets = 0
    secant_rejects = 0

    print(f"RLBFGS_INITIAL_ENERGY={E:.15e}")
    print(f"RLBFGS_INITIAL_GRAD_RMS={rms:.15e}")
    print(f"RLBFGS_INITIAL_GRAD_MAX={gmax:.15e}")
    print("RLBFGS_INITIAL_STRICT_STATIONARITY=" + ("PASS" if station else "FAIL"))

    while accepted_this < MAX_ACCEPTED_THIS_RUN and not station:
        direction, used_history = two_loop_direction(cr3, g, history, dx)
        direction = cr3.project_tangent(phi, direction)
        gd = cr3.tangent_inner(g, direction, dx)
        gg = cr3.tangent_inner(g, g, dx)
        if (not math.isfinite(gd)) or gd >= -1e-10 * max(gg, 1e-300):
            history.clear()
            history_resets += 1
            direction = -g
            gd = -gg
            used_history = False

        max_dir = float(np.max(np.linalg.norm(direction[1:-1,1:-1,1:-1], axis=-1)))
        alpha = min(1.0, MAX_POINT_ROTATION / max(max_dir, 1e-300))
        trial = None
        Etrial = math.inf
        accepted_next = state.accepted_total + 1
        full_guard = accepted_next % FULL_GEOMETRIC_GUARD_EVERY == 0
        do_guard = accepted_next % GEOMETRIC_GUARD_EVERY == 0

        for _ in range(MAX_LINESEARCH):
            if alpha < MIN_ALPHA:
                break
            cand = cr3.exp_map_update(phi, direction, alpha)
            Etrial = cr3.high_order_energy_gradient(cand, dx, False)[0]
            if (not math.isfinite(Etrial)) or Etrial > E + ARMIJO_C1 * alpha * gd:
                rejected_energy += 1
                alpha *= 0.5
                continue
            angle = cr3.max_neighbor_angle(cand)
            if angle > MAX_NEIGHBOR_ANGLE:
                rejected_smooth += 1
                alpha *= 0.5
                continue
            t4 = cr3.topology4(cand, dx)
            if abs(abs(t4)/B - 1.0) > MAX_TOPOLOGY_RELERR:
                rejected_topology += 1
                alpha *= 0.5
                continue
            if do_guard:
                gok, _ = cr3.geometric_guard(cand, cr2, full_guard)
                if not gok:
                    rejected_topology += 1
                    alpha *= 0.5
                    continue
            trial = cand
            break

        if trial is None and used_history:
            # One fail-safe retry with steepest descent before declaring a
            # numerical stall; no physical threshold is changed.
            history.clear()
            history_resets += 1
            direction = -g
            gd = -gg
            max_dir = float(np.max(np.linalg.norm(direction[1:-1,1:-1,1:-1], axis=-1)))
            alpha = min(0.25, MAX_POINT_ROTATION / max(max_dir, 1e-300))
            for _ in range(MAX_LINESEARCH):
                if alpha < MIN_ALPHA:
                    break
                cand = cr3.exp_map_update(phi, direction, alpha)
                Etrial = cr3.high_order_energy_gradient(cand, dx, False)[0]
                if (not math.isfinite(Etrial)) or Etrial > E + ARMIJO_C1 * alpha * gd:
                    rejected_energy += 1; alpha *= 0.5; continue
                if cr3.max_neighbor_angle(cand) > MAX_NEIGHBOR_ANGLE:
                    rejected_smooth += 1; alpha *= 0.5; continue
                t4 = cr3.topology4(cand, dx)
                if abs(abs(t4)/B - 1.0) > MAX_TOPOLOGY_RELERR:
                    rejected_topology += 1; alpha *= 0.5; continue
                trial = cand
                break

        if trial is None:
            print("RLBFGS_LINE_SEARCH_FAILED=YES")
            break

        old_phi = phi
        old_g = g
        old_direction = direction
        old_history = history

        phi = trial
        E, _, _, _, g, rms, gmax, station = strict_stationarity(cr3, phi, dx)
        state.phi = phi
        state.accepted_total += 1
        accepted_this += 1

        # Transport existing memory and form the new secant pair.  The
        # geodesic trigonometry is computed once per accepted step, not once
        # per history vector.
        geom = transport_geometry(old_phi, old_direction, alpha, phi)
        transported = []
        for s_old, y_old, _rho_old in old_history:
            st = exact_parallel_transport(old_phi, geom, s_old, cr3)
            yt = exact_parallel_transport(old_phi, geom, y_old, cr3)
            sy_t = cr3.tangent_inner(st, yt, dx)
            if sy_t > 1e-300:
                transported.append((st, yt, 1.0/sy_t))

        g_old_t = exact_parallel_transport(old_phi, geom, old_g, cr3)
        step_old = alpha * old_direction
        s_new = exact_parallel_transport(old_phi, geom, step_old, cr3)
        y_new = g - g_old_t
        ss = cr3.tangent_inner(s_new, s_new, dx)
        yy = cr3.tangent_inner(y_new, y_new, dx)
        sy = cr3.tangent_inner(s_new, y_new, dx)
        cautious = CAUTIOUS_CURVATURE * math.sqrt(max(ss*yy, 0.0))
        if math.isfinite(sy) and sy > max(cautious, 1e-300):
            transported.append((s_new, y_new, 1.0/sy))
        else:
            secant_rejects += 1
        history = transported[-HISTORY_SIZE:]

        if accepted_this % PROGRESS_EVERY == 0 or station:
            t4 = cr3.topology4(phi, dx)
            sentinel_text = "NOT_EVALUATED_THIS_STEP"
            if accepted_this % (2 * PROGRESS_EVERY) == 0 or station:
                sentinel = one_direction_payload(cr3, phi, state.axis, dx, KNOWN_WORST_DIRECTION)
                sentinel_text = f"{sentinel:.15e}"
            print(
                f"RLBFGS_PROGRESS_ACCEPTED_THIS_RUN={accepted_this} "
                f"ACCEPTED_TOTAL={state.accepted_total} ENERGY={E:.15e} "
                f"GRAD_RMS={rms:.15e} GRAD_MAX={gmax:.15e} "
                f"TOPOLOGY4={t4:.15e} WORST_DIRECTION_SENTINEL={sentinel_text} "
                f"HISTORY={len(history)} ALPHA={alpha:.15e}"
            )
        if state.accepted_total % CHECKPOINT_EVERY == 0 or station:
            save_checkpoint(state, E, rms, gmax, "023CR4R_RLBFGS")

    print(f"RLBFGS_ACCEPTED_THIS_RUN={accepted_this}")
    print(f"RLBFGS_ACCEPTED_TOTAL={state.accepted_total}")
    print(f"RLBFGS_REJECTED_ENERGY_TRIALS={rejected_energy}")
    print(f"RLBFGS_REJECTED_TOPOLOGY_TRIALS={rejected_topology}")
    print(f"RLBFGS_REJECTED_SMOOTHNESS_TRIALS={rejected_smooth}")
    print(f"RLBFGS_HISTORY_RESETS={history_resets}")
    print(f"RLBFGS_SECANT_REJECTS={secant_rejects}")
    return state, E, g, rms, gmax, station


def main() -> None:
    print("=== 023CR4R — GRADIENT-AUDIT REPAIR + RLBFGS STATIONARITY CLOSURE ===", flush=True)

    print("\n=== A — UPSTREAM AUDIT ===", flush=True)
    for p in (CR2_SOURCE, CR3_SOURCE, CR3R_SOURCE, CR3R_LOG, CR3R_ARTIFACT):
        require(p)
    hashes = {
        "023CR2": sha256(CR2_SOURCE),
        "023CR3": sha256(CR3_SOURCE),
        "023CR3R": sha256(CR3R_SOURCE),
    }
    expected = {
        "023CR2": EXPECTED_CR2_SHA256,
        "023CR3": EXPECTED_CR3_SHA256,
        "023CR3R": EXPECTED_CR3R_SHA256,
    }
    for k, v in hashes.items():
        print(f"{k}_SOURCE_SHA256={v}")
    log_text = CR3R_LOG.read_text(errors="replace")
    markers = (
        "N65_FINAL_GEOMETRIC_DEGREES=-7,-7,-7",
        "N65_FINAL_DENSE_FINITE_PAYLOAD_OUTWARD=PASS",
        "N65_PHYSICAL_GATE=PASS",
        "N65_FINAL_STRICT_STATIONARITY=FAIL",
        "023CR3R_STATIONARITY_CONTINUATION_AND_OPTIMIZER_CROSSCHECK=INCOMPLETE_PRIMARY_STATIONARITY_GATE",
    )
    upstream_ok = all(hashes[k] == expected[k] for k in expected) and all(m in log_text for m in markers)
    print("UPSTREAM_023CR3R_AUDIT=" + ("PASS" if upstream_ok else "FAIL"))
    if not upstream_ok:
        raise RuntimeError("023CR3R upstream audit failed")

    cr2 = load_module("cr2_for_023cr4", CR2_SOURCE)
    cr3 = load_module("cr3_for_023cr4", CR3_SOURCE)
    cr3r = load_module("cr3r_for_023cr4", CR3R_SOURCE)

    print("\n=== B — EXACT DISCRETE GRADIENT RECHECK ===", flush=True)
    rel, ok = cr3.gradient_selfcheck()
    print(f"HIGH_ORDER_ACTION_GRADIENT_DIRECTIONAL_RELERR={rel:.15e}")
    print("HIGH_ORDER_ACTION_GRADIENT_SELFCHECK=" + ("PASS" if ok else "FAIL"))
    if not ok:
        raise RuntimeError("Imported high-order gradient selfcheck failed")

    print("\n=== C — LOAD / LOCALIZE SAVED RESIDUAL ===", flush=True)
    state, start_name = load_start(cr3, cr2)
    E, E2, E4, E0, g, rms, gmax, station = strict_stationarity(cr3, state.phi, state.dx)
    print(f"START_ENERGY={E:.15e}")
    print(f"START_GRAD_RMS={rms:.15e}")
    print(f"START_GRAD_MAX={gmax:.15e}")
    print("START_STRICT_STATIONARITY=" + ("PASS" if station else "FAIL"))
    residual_localization(cr3, state, g)
    if not saved_field_directional_check(cr3, state, g):
        raise RuntimeError("Directional gradient check failed at saved N65 field")
    print("GRADIENT_VALIDATION_THRESHOLDS_WEAKENED=NO")
    start_sentinel = one_direction_payload(cr3, state.phi, state.axis, state.dx, KNOWN_WORST_DIRECTION)
    print(f"START_WORST_DIRECTION_PAYLOAD_SENTINEL={start_sentinel:.15e}")
    print("PAYLOAD_SENTINEL_USED_AS_PROMOTION_EVIDENCE=NO")

    print("\n=== D — R-LBFGS STATIONARITY CLOSURE ===", flush=True)
    print(f"RLBFGS_MAX_ACCEPTED_THIS_RUN={MAX_ACCEPTED_THIS_RUN}")
    state, E, g, rms, gmax, station = rlbfgs(cr3, cr2, state)
    save_checkpoint(state, E, rms, gmax, "023CR4R_RLBFGS_EXIT")

    print("\n=== E — FINAL STATIONARITY / TOPOLOGY ===", flush=True)
    t4 = cr3.topology4(state.phi, state.dx)
    gok, degrees = cr3.geometric_guard(state.phi, cr2, True)
    angle = cr3.max_neighbor_angle(state.phi)
    final_sentinel = one_direction_payload(cr3, state.phi, state.axis, state.dx, KNOWN_WORST_DIRECTION)
    print(f"FINAL_ENERGY={E:.15e}")
    print(f"FINAL_GRAD_RMS={rms:.15e}")
    print(f"FINAL_GRAD_MAX={gmax:.15e}")
    print("FINAL_STRICT_STATIONARITY=" + ("PASS" if station else "FAIL"))
    print(f"FINAL_TOPOLOGY4={t4:.15e}")
    print("FINAL_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in degrees))
    print(f"FINAL_MAX_NEIGHBOR_ANGLE={angle:.15e}")
    print(f"FINAL_WORST_DIRECTION_PAYLOAD_SENTINEL={final_sentinel:.15e}")

    if not station:
        ratio = rms / max(GRAD_RMS_TOL, 1e-300)
        print("\n=== F — 023CR4 DECISION ===")
        print("023CR4R_GRADIENT_AUDIT_AND_RLBFGS_STATIONARITY_CLOSURE=INCOMPLETE_CONTINUE_FROM_CHECKPOINT")
        print("UNRESTRICTED_CARTESIAN_STATIONARY_B7_FIELD=NOT_YET_ESTABLISHED")
        print(f"REMAINING_RMS_TO_THRESHOLD_RATIO={ratio:.15e}")
        print("PHYSICAL_FALSIFICATION=NO_NONSTATIONARY_FIELD")
        print("HEURISTIC_PROMOTION_FROM_023CR4=NO")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
        print("NEXT=RERUN_023CR4_FROM_CHECKPOINT_OR_NEWTON_KRYLOV_IF_RLBFGS_STAGNATES")
        print("FULL_PHYSICAL_HESSIAN=NOT_AUTHORIZED")
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_ESTABLISHED")
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
        return

    print("\n=== F — ONE-TIME STATIONARY PHYSICAL + 320-DIRECTION AUDIT ===", flush=True)
    diag = cr3.continuum_local_diagnostics(state.phi, state.axis, state.dx, cr2)
    payload = cr3.payload_diagnostics(state.phi, state.axis, state.dx, PAYLOAD_CENTER, PAYLOAD_RADIUS)
    physical, checks = cr3r.physical_gate(cr3, diag, payload)
    print(f"STATIONARY_CONTINUUM_ENERGY={diag.energy_continuum:.15e}")
    print(f"STATIONARY_ACTIVE_TOTAL={diag.active_total:.15e}")
    print(f"STATIONARY_ACTIVE_TO_ENERGY={diag.active_to_energy:.15e}")
    print(f"STATIONARY_MIN_ACTIVE_FRACTION={diag.min_active_fraction:.15e}")
    print(f"STATIONARY_TOPOLOGY4={diag.topology4:.15e}")
    print("STATIONARY_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in diag.geometric_degrees))
    print(f"STATIONARY_MAX_NEIGHBOR_ANGLE={diag.max_neighbor_angle:.15e}")
    print(f"STATIONARY_MIN_DEC_SCALED_MARGIN={diag.min_dec_scaled_margin:.15e}")
    print(f"STATIONARY_MAX_ACTIVE_TRACE_SCALED={diag.max_active_trace_scaled:.15e}")
    print(f"STATIONARY_PAYLOAD_MIN_RADIAL={payload.min_radial:.15e}")
    print(f"STATIONARY_PAYLOAD_MAX_RADIAL={payload.max_radial:.15e}")
    print(f"STATIONARY_PAYLOAD_MEAN_RADIAL={payload.mean_radial:.15e}")
    print(f"STATIONARY_PAYLOAD_MAX_TRANSVERSE_OVER_RADIAL={payload.max_transverse_over_radial:.15e}")
    print("STATIONARY_DENSE_FINITE_PAYLOAD_OUTWARD=" + ("PASS" if payload.all_outward else "FAIL"))
    for key, val in checks.items():
        print(f"STATIONARY_{key}=" + ("PASS" if val else "FAIL"))
    print("STATIONARY_PHYSICAL_GATE=" + ("PASS" if physical else "FAIL"))

    cr3r.save_artifact(FINAL_ARTIFACT, state.phi, state.axis, state.dx, diag, payload, "023CR4R_N65")
    print(f"STRICT_STATIONARY_FIELD_ARTIFACT={FINAL_ARTIFACT.relative_to(ROOT)}")

    print("\n=== G — 023CR4 DECISION ===")
    if physical:
        print("023CR4R_GRADIENT_AUDIT_AND_RLBFGS_STATIONARITY_CLOSURE=GREEN_STRICT_STATIONARY_N65")
        print("UNRESTRICTED_CARTESIAN_STATIONARY_B7_FIELD=SUPPORTED_AT_N65")
        print("FINITE_PAYLOAD_REPULSION_AT_STRICT_STATIONARITY=SUPPORTED_AT_N65")
        print("HEURISTIC_PROMOTION_FROM_023CR4=NO_HOLD_FOR_FULL_HESSIAN_AND_RESOLUTION")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
        print("NEXT=023C2_FULL_TANGENT_HESSIAN_RESOLUTION_AND_FISSION_CHALLENGE")
        print("FULL_PHYSICAL_HESSIAN=AUTHORIZED_NOT_YET_ESTABLISHED")
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_YET_AUTHORIZED_UNTIL_023C2_GREEN")
    else:
        print("023CR4R_GRADIENT_AUDIT_AND_RLBFGS_STATIONARITY_CLOSURE=GREEN_STATIONARY_BUT_PHYSICAL_GATE_FAILED")
        print("UNRESTRICTED_CARTESIAN_STATIONARY_B7_FIELD=SUPPORTED_AT_N65")
        print("FINITE_PAYLOAD_REPULSION_AT_STRICT_STATIONARITY=" + ("SUPPORTED" if payload.all_outward else "FAILED"))
        print("HEURISTIC_PROMOTION_FROM_023CR4=NO")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
        print("NEXT=REPRODUCE_PHYSICAL_GATE_FAILURE_AT_COMPANION_RESOLUTION_BEFORE_RERANK")
        print("FULL_PHYSICAL_HESSIAN=NOT_AUTHORIZED")
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_ESTABLISHED")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023CR4R_GRADIENT_AUDIT_AND_RLBFGS_STATIONARITY_CLOSURE")


if __name__ == "__main__":
    main()
