#!/usr/bin/env python3
"""023C2AQS2R5 — two-level V-cycle N=73 stationarity closure.

PURPOSE
-------
Close the remaining unrestricted N=73 B=7 Skyrmion Euler-Lagrange residual
after 023C2AQS2R4 demonstrated that a residual-informed coarse Galerkin space
can capture and reduce the smooth error very cheaply, but consecutive coarse
steps regenerate a high-frequency complement and can push GRAD_MAX back above
its strict threshold.

ACTIVE SCIENTIFIC QUESTION
--------------------------
Can an explicit two-level nonlinear V-cycle, alternating

    (fine smoothing) -> (coarse Galerkin correction),

drive the SAME full N=73 field to the unchanged strict stationarity gates while
preserving B=7 topology, the exact discrete action, and all physical audit
conditions?

LATEST EVIDENCE MOTIVATING THIS RUN
-----------------------------------
At the 023C2AQS2R4 input field:

    GRAD_RMS  ~= 2.713e-3
    GRAD_MAX  ~= 1.350e-2
    merit     ~= 1.809

and the residual was overwhelmingly smooth:

    low-frequency fraction  ~= 0.826
    high-frequency fraction ~= 0.022
    roughness                ~= 0.220.

The first R4 coarse basis captured ~99.90% of the full gradient, validating the
coarse-space diagnosis.  Three accepted coarse corrections used only 39 HVPs
and reduced the full-field stationarity merit to ~1.623.  However the final
residual had flipped character:

    low-frequency fraction  ~= 0.233
    high-frequency fraction ~= 0.578
    roughness                ~= 2.925
    GRAD_MAX                 ~= 5.95e-2.

Thus the coarse solver is useful but incomplete by itself.  Repeating it
without a fine-grid smoother would violate the information-gain stop rule.

PHYSICAL MODEL / EQUATIONS
--------------------------
No physical model change is introduced.  This run uses the same unrestricted
static SU(2) Skyrme field

    phi = (sigma, pi1, pi2, pi3),       phi.phi = 1,

with

    E = integral (e2 + e4 + V) d^3x,
    V = m^2 (1-sigma)(1+eta sigma),

at

    B = 7,
    eta = 0.4,
    m = 8.

The exact projected stationarity equation remains

    g(phi) = 0

for the checkerboard-free fourth-order lattice action inherited from the
audited 023CR/023C2 chain.

STRICT OPERATIONAL NUMERICAL OBSERVABLE
----------------------------------------
The unchanged stationarity merit is

    M = max(
        GRAD_RMS / 1.5e-3,
        GRAD_MAX / 5.0e-2
    ).

Strict N=73 stationarity requires exactly

    GRAD_RMS <= 1.5e-3,
    GRAD_MAX <= 5.0e-2.

No threshold is weakened.

TWO-LEVEL V-CYCLE
-----------------
Each bounded nonlinear cycle has two possible phases.

A. FINE SMOOTHER

When the residual is high-frequency/rough or GRAD_MAX is above threshold, try
cheap full-space smoothers before building another coarse Hessian.

Primary smoother:
    delta_f = - B_LBFGS g,

where B_LBFGS is the existing positive-curvature limited-memory inverse
Hessian approximation from the transported 20-pair history.

Fallback smoother:
    delta_h = - (g - G_sigma=1 g),

the high-pass tangent residual itself.

These are numerical directions only.  They change no equation or physical
constraint.  Every candidate is accepted only after recomputing the complete
exact million-DOF gradient, energy, topology and smoothness.

B. COARSE GALERKIN CORRECTION

When smooth residual remains, construct the audited R4 residual-informed
coarse basis U and full covariant HVP, then form

    A_c = U^T H U.

For each small predeclared damping candidate solve

    (A_c + mu I)c = -U^T g,
    delta_c = U c.

Unlike R4, this run does not automatically accept the first damping value with
a marginal full-field improvement.  It evaluates the bounded damping ladder
and retains the best full-field admissible candidate.

A frequency guard prevents a coarse half-cycle from recreating a dominant
lattice-scale residual:

    high_fraction_new <= max(0.35, 1.5 high_fraction_old)
    roughness_new      <= max(1.50, 1.5 roughness_old)

unless the candidate already reaches strict stationarity.

These are solver guards only.  They never enter the physical field equations,
stress tensor, force observable or final stationarity test.

WHY THIS IS A TRUE TWO-LEVEL TEST
---------------------------------
The coarse basis is not a physical ansatz.  The fine field remains unrestricted.
Every accepted half-step is judged using:

- the complete exact N=73 gradient;
- the unchanged full energy;
- the geometric and derivative topology guards;
- the original link-smoothness guard;
- the original stationarity merit.

Therefore the V-cycle cannot manufacture stationarity by projecting away a
physical mode.

HESSIAN / ZERO MODES
--------------------
The covariant matrix-free Hessian-vector product is inherited unchanged from
023C2A and is re-audited at the actual starting field for finite-difference
step convergence and bilinear self-adjointness.

Only the exact three global pion-isorotation zero modes are projected out.
Approximate translations and spatial rotations are retained.

EFFICIENCY DESIGN
-----------------
- Fine L-BFGS/high-pass smoothing needs no HVPs.
- A coarse half-cycle uses only the coarse basis dimension (~13 HVPs).
- Default maximum is four V-cycles.
- The expensive continuous finite-payload calculation is still run only after
  strict stationarity and the full physical-field audit.

INPUTS
------
Required upstream source:
    simulations/023c2aqs2r4_residual_informed_coarse_galerkin_stationarity.py

Preferred field:
    results/data/023c2aqs2r5_n73_two_level_vcycle_checkpoint.npz

Fallback:
    results/data/023c2aqs2r4_n73_coarse_galerkin_checkpoint.npz

OUTPUTS
-------
Checkpoint:
    results/data/023c2aqs2r5_n73_two_level_vcycle_checkpoint.npz

Strict stationary artifact:
    results/data/023c2aqs2r5_strict_stationary_b7_n73.npz

VALIDATION / FALSIFICATION
--------------------------
- fail-closed R4 source hash;
- external 94-test known-solution regression;
- exact inherited action/gradient;
- HVP step convergence and self-adjointness;
- exact isorotation projection only;
- positive-curvature L-BFGS history only;
- coarse basis orthonormality and Galerkin symmetry;
- complete full-field merit, topology, smoothness and energy after every trial;
- before/after frequency and localization diagnostics;
- full stress-energy/DEC/trace audit only after strict stationarity;
- continuous-force certificate only after the physical field gate.

PROMOTION CONDITION
-------------------
This run may establish only:

    STRICT_STATIONARY_N73
    plus the declared N73 continuous-force sentinel.

It does NOT establish complete unrestricted 023C stability.

FALSIFIERS / STOP RULE
----------------------
- Failed upstream/HVP audit: numerical failure.
- Loss of B=7 or smoothness: reject candidate.
- No merit-reducing fine or coarse correction in a complete V-cycle: stop for
  an explicitly augmented/deflated full MINRES gate; do not tune indefinitely.
- If four cycles produce <10% total merit improvement and remain nonstationary,
  stop for the augmented Krylov gate.
- Certified inward continuous force at strict N=73 is an operational blocker
  for the declared payload point, subject to companion-resolution confirmation.
- Never weaken stationarity, topology, DEC, trace or force criteria.

CLAIM BOUNDARIES
----------------
This is a numerical stationarity solver repair.  It does not establish a
positive full physical Hessian, fission stability, N73/N81 continuum force
convergence, nonlinear Einstein-Skyrme consistency, practical energy scaling,
a material realization, an experiment, a device, or discovery of new physics.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023C2AQS2R5_TWO_LEVEL_VCYCLE_STATIONARITY_REPAIR
"""

from __future__ import annotations

import hashlib
import importlib.util
import math
import os
from pathlib import Path
import sys

import numpy as np
from scipy.ndimage import gaussian_filter


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

R4_SOURCE = SIM / "023c2aqs2r4_residual_informed_coarse_galerkin_stationarity.py"
EXPECTED_R4_SHA256 = "bc6673be817b838febdd786834f3ab63222f002fe8cd122121afce4017646002"

UPSTREAM_CHECKPOINT = DATA / "023c2aqs2r4_n73_coarse_galerkin_checkpoint.npz"
CHECKPOINT = DATA / "023c2aqs2r5_n73_two_level_vcycle_checkpoint.npz"
FINAL = DATA / "023c2aqs2r5_strict_stationary_b7_n73.npz"

B = 7
ETA = 0.4
MASS = 8.0
N = 73

GRAD_RMS_TOL = 1.5e-3
GRAD_MAX_TOL = 5.0e-2
MAX_NEIGHBOR_ANGLE = 0.70

MAX_CYCLES = max(1, int(os.environ.get("AG_V5_MAX_CYCLES", "4")))
MAX_FINE_STEPS = max(1, int(os.environ.get("AG_V5_MAX_FINE_STEPS", "2")))
MAX_LINESEARCH = max(4, int(os.environ.get("AG_V5_MAX_LINESEARCH", "8")))
HVP_POINT_ANGLE = float(os.environ.get("AG_V5_HVP_POINT_ANGLE", "2e-4"))

FINE_HIGH_TRIGGER = float(os.environ.get("AG_V5_FINE_HIGH_TRIGGER", "0.20"))
FINE_ROUGH_TRIGGER = float(os.environ.get("AG_V5_FINE_ROUGH_TRIGGER", "1.00"))
COARSE_LOW_TRIGGER = float(os.environ.get("AG_V5_COARSE_LOW_TRIGGER", "0.25"))

HALFSTEP_MERIT_FACTOR = float(os.environ.get("AG_V5_HALFSTEP_MERIT_FACTOR", "0.995"))
ARMIJO_C1 = float(os.environ.get("AG_V5_ARMIJO_C1", "1e-4"))
MIN_COARSE_CAPTURE = float(os.environ.get("AG_V5_MIN_COARSE_CAPTURE", "0.35"))
MAX_COARSE_BASIS = max(6, int(os.environ.get("AG_V5_MAX_COARSE_BASIS", "14")))

DAMPING_MULTIPLIERS = tuple(
    float(x)
    for x in os.environ.get("AG_V5_DAMPING_MULTIPLIERS", "0,0.25,1,4").split(",")
)


def sha256(path: Path) -> str:
    """Return SHA-256 for one required scientific source."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def require(path: Path) -> None:
    """Fail closed if a required source or checkpoint is absent."""
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def load_module(name: str, path: Path):
    """Import one repository simulation by explicit path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def stationarity_merit(rms: float, gmax: float) -> float:
    """Return unchanged normalized distance from strict stationarity."""
    return max(rms / GRAD_RMS_TOL, gmax / GRAD_MAX_TOL)


def load_state(r4, qs2, cr3, cr4r):
    """Load the R5 checkpoint or the latest R4 field plus transported history."""
    source = CHECKPOINT if CHECKPOINT.is_file() else UPSTREAM_CHECKPOINT
    require(source)
    with np.load(source, allow_pickle=False) as d:
        phi = np.array(d["phi"], dtype=float, copy=True)
        axis = np.array(d["axis"], dtype=float, copy=True)
        dx = float(d["dx"])
        accepted_total = int(d["accepted_total"]) if "accepted_total" in d.files else 0
        nk_total = int(d["newton_accepted_total"]) if "newton_accepted_total" in d.files else 0
        coarse_total = int(d["coarse_accepted_total"]) if "coarse_accepted_total" in d.files else 0
        vcycle_total = int(d["vcycle_accepted_total"]) if "vcycle_accepted_total" in d.files else 0
        fine_total = int(d["fine_accepted_total"]) if "fine_accepted_total" in d.files else 0
        b = int(d["B"]) if "B" in d.files else B
        eta = float(d["eta"]) if "eta" in d.files else ETA
        mass = float(d["mass"]) if "mass" in d.files else MASS
        s_hist = (
            np.asarray(d["s_hist"], dtype=float)
            if "s_hist" in d.files else np.empty((0, N, N, N, 4), dtype=float)
        )
        y_hist = (
            np.asarray(d["y_hist"], dtype=float)
            if "y_hist" in d.files else np.empty((0, N, N, N, 4), dtype=float)
        )

    if phi.shape != (N, N, N, 4) or axis.shape != (N,):
        raise RuntimeError(f"Unexpected N73 state shape phi={phi.shape} axis={axis.shape}")
    if b != B or abs(eta - ETA) > 1e-14 or abs(mass - MASS) > 1e-14:
        raise RuntimeError("N73 metadata mismatch")

    norm_err = float(np.max(np.abs(np.linalg.norm(phi, axis=-1) - 1.0)))
    if norm_err > 5e-10:
        raise RuntimeError(f"N73 S3 norm violation {norm_err}")

    history, discarded = qs2.history_from_arrays(cr3, s_hist, y_hist, dx)
    state = cr4r.State(phi=phi, axis=axis, dx=dx, accepted_total=accepted_total)
    return (
        state, history, source, discarded, norm_err,
        nk_total, coarse_total, vcycle_total, fine_total,
    )


def save_checkpoint(
    state, history, E, rms, gmax,
    nk_total, coarse_total, vcycle_total, fine_total,
):
    """Persist the unrestricted field and transported curvature history."""
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
        B=np.array(B),
        eta=np.array(ETA),
        mass=np.array(MASS),
        accepted_total=np.array(state.accepted_total),
        newton_accepted_total=np.array(nk_total),
        coarse_accepted_total=np.array(coarse_total),
        vcycle_accepted_total=np.array(vcycle_total),
        fine_accepted_total=np.array(fine_total),
        energy=np.array(E),
        grad_rms=np.array(rms),
        grad_max=np.array(gmax),
        source=np.array("023C2AQS2R5_TWO_LEVEL_VCYCLE"),
        s_hist=s_hist,
        y_hist=y_hist,
    )

    print(
        f"V5_CHECKPOINT_WRITTEN={CHECKPOINT.relative_to(ROOT)} "
        f"VCYCLE_ACCEPTED_TOTAL={vcycle_total} "
        f"FINE_ACCEPTED_TOTAL={fine_total} "
        f"COARSE_ACCEPTED_TOTAL={coarse_total} "
        f"HISTORY_LENGTH={len(history)}",
        flush=True,
    )


def save_final(state, E, rms, gmax, diag, nk_total, coarse_total, vcycle_total, fine_total):
    """Persist a strict stationary field only after the original gates pass."""
    FINAL.parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        FINAL,
        phi=state.phi,
        axis=state.axis,
        dx=np.array(state.dx),
        B=np.array(B),
        eta=np.array(ETA),
        mass=np.array(MASS),
        accepted_total=np.array(state.accepted_total),
        newton_accepted_total=np.array(nk_total),
        coarse_accepted_total=np.array(coarse_total),
        vcycle_accepted_total=np.array(vcycle_total),
        fine_accepted_total=np.array(fine_total),
        energy=np.array(E),
        grad_rms=np.array(rms),
        grad_max=np.array(gmax),
        topology4=np.array(diag.topology4),
        active_total=np.array(diag.active_total),
        min_active_fraction=np.array(diag.min_active_fraction),
        min_dec_scaled_margin=np.array(diag.min_dec_scaled_margin),
        max_active_trace_scaled=np.array(diag.max_active_trace_scaled),
        source=np.array("023C2AQS2R5_N73_STRICT_STATIONARY"),
    )
    print(f"V5_STRICT_STATIONARY_FIELD_ARTIFACT={FINAL.relative_to(ROOT)}", flush=True)


def residual_metrics(c2a, phi, g):
    """Return low/high residual fractions and nearest-neighbor roughness."""
    basis = c2a.tangent_basis_householder(phi)
    comp = c2a.field_to_components(g, basis).reshape(N - 2, N - 2, N - 2, 3)

    low = np.empty_like(comp)
    for a in range(3):
        low[..., a] = gaussian_filter(comp[..., a], sigma=1.0, mode="nearest")
    high = comp - low

    total = float(np.sum(comp * comp))
    low2 = float(np.sum(low * low))
    high2 = float(np.sum(high * high))

    rough_num = 0.0
    for axis in range(3):
        d = np.diff(comp, axis=axis)
        rough_num += float(np.sum(d * d))

    return {
        "basis": basis,
        "comp": comp,
        "low": low,
        "high": high,
        "low_frac": low2 / max(total, 1e-300),
        "high_frac": high2 / max(total, 1e-300),
        "rough": rough_num / max(total, 1e-300),
    }


def print_metrics(label: str, metrics: dict) -> None:
    """Print residual spectrum in the same convention as R3/R4."""
    print(f"{label}_RESIDUAL_GAUSSIAN_LOW_L2_FRACTION={metrics['low_frac']:.15e}", flush=True)
    print(f"{label}_RESIDUAL_GAUSSIAN_HIGH_L2_FRACTION={metrics['high_frac']:.15e}", flush=True)
    print(f"{label}_RESIDUAL_NEIGHBOR_ROUGHNESS_RATIO={metrics['rough']:.15e}", flush=True)


def full_candidate(
    r4, r, qs2, c2a, cr2, cr3,
    state, g, E, rms, gmax,
    direction, label: str,
    frequency_guard: bool,
    old_metrics: dict,
):
    """Line-search one unrestricted tangent direction with full exact gates."""
    phi = state.phi
    dx = state.dx
    merit0 = stationarity_merit(rms, gmax)

    direction = cr3.project_tangent(phi, direction)
    gd = cr3.tangent_inner(g, direction, dx)
    g2 = max(cr3.tangent_inner(g, g, dx), 1e-300)

    print(f"{label}_G_DOT_DELTA={gd:.15e}", flush=True)
    if (not math.isfinite(gd)) or gd >= -1e-12 * g2:
        print(f"{label}_DESCENT=NO", flush=True)
        return None
    print(f"{label}_DESCENT=YES", flush=True)

    max_point = float(np.max(np.linalg.norm(direction[1:-1, 1:-1, 1:-1], axis=-1)))
    trust_angle = min(1.5e-3, max(2.5e-4, 0.30 * rms))
    alpha = min(1.0, trust_angle / max(max_point, 1e-300))

    print(
        f"{label}_MAX_POINT={max_point:.15e} TRUST_ANGLE={trust_angle:.15e} "
        f"ALPHA0={alpha:.15e}",
        flush=True,
    )

    for ls in range(MAX_LINESEARCH):
        cand = cr3.exp_map_update(phi, direction, alpha)
        Etrial = cr3.high_order_energy_gradient(cand, dx, False)[0]

        if (not math.isfinite(Etrial)) or Etrial > E + ARMIJO_C1 * alpha * gd:
            print(f"{label}_LS={ls} ENERGY_ACCEPT=NO ALPHA={alpha:.15e}", flush=True)
            alpha *= 0.5
            continue

        ok, reason, _ = qs2.candidate_admissible(
            cr3, cr2, cand, dx, state.accepted_total + 1
        )
        if not ok:
            print(f"{label}_LS={ls} ADMISSIBLE=NO REASON={reason}", flush=True)
            alpha *= 0.5
            continue

        pack = r.strict_stationarity(cr3, cand, dx)
        Enew, _a, _b, _c, gnew, rmsnew, gmaxnew, stationnew = pack
        merit_new = stationarity_merit(rmsnew, gmaxnew)
        merit_ok = bool(stationnew or merit_new <= HALFSTEP_MERIT_FACTOR * merit0)

        new_metrics = residual_metrics(c2a, cand, gnew)
        freq_ok = True
        if frequency_guard and not stationnew:
            high_cap = max(0.35, 1.5 * old_metrics["high_frac"])
            rough_cap = max(1.50, 1.5 * old_metrics["rough"])
            freq_ok = bool(
                new_metrics["high_frac"] <= high_cap
                and new_metrics["rough"] <= rough_cap
            )

        print(
            f"{label}_LS={ls} ALPHA={alpha:.15e} ENERGY={Enew:.15e} "
            f"GRAD_RMS={rmsnew:.15e} GRAD_MAX={gmaxnew:.15e} "
            f"STATIONARITY_MERIT={merit_new:.15e} "
            f"HIGH_FRACTION={new_metrics['high_frac']:.15e} "
            f"ROUGHNESS={new_metrics['rough']:.15e} "
            f"MERIT_ACCEPT={'YES' if merit_ok else 'NO'} "
            f"FREQUENCY_ACCEPT={'YES' if freq_ok else 'NO'}",
            flush=True,
        )

        if merit_ok and freq_ok:
            return {
                "cand": cand,
                "E": Enew,
                "g": gnew,
                "rms": rmsnew,
                "gmax": gmaxnew,
                "station": stationnew,
                "merit": merit_new,
                "metrics": new_metrics,
                "direction": direction,
                "alpha": alpha,
            }

        alpha *= 0.5

    return None


def accept_pack(
    r, cr3, cr4r,
    state, history, old_g, pack,
    kind: str,
):
    """Transport history and install one fully admissible unrestricted update."""
    old_phi = state.phi
    old_merit = None
    direction = pack["direction"]
    alpha = pack["alpha"]

    r.transport_history_after_step(
        cr3, cr4r,
        old_phi, pack["cand"],
        direction, alpha,
        old_g, pack["g"],
        history,
    )
    state.phi = pack["cand"]
    state.accepted_total += 1

    t4 = cr3.topology4(state.phi, state.dx)
    deg_ok, degrees = cr3.geometric_guard(state.phi, cr4r.load_module if False else None, True) if False else (True, ())

    # The actual geometric audit is performed by the caller with cr2 because
    # this helper intentionally has no hidden model dependencies.
    print(f"V5_ACCEPTED_KIND={kind}", flush=True)
    print(f"V5_ACCEPTED_TOPOLOGY4={t4:.15e}", flush=True)
    return state


def try_fine_smoother(
    r4, r, qs2, c2a, cr2, cr3, cr4r,
    state, history, E, g, rms, gmax,
):
    """Try L-BFGS inverse smoothing, then an explicit high-pass fallback."""
    phi = state.phi
    basis = c2a.tangent_basis_householder(phi)
    Z = c2a.orthonormal_columns(c2a.isorotation_modes(phi, basis))
    gvec = c2a.project_subspace(c2a.field_to_components(g, basis), Z)
    pairs = r.component_history(c2a, history, basis, Z)

    old_metrics = residual_metrics(c2a, phi, g)
    print(f"V5_FINE_PRECONDITIONER_USABLE_PAIRS={len(pairs)}", flush=True)

    candidates = []

    if pairs:
        delta_lbfgs = -r.lbfgs_inverse_vector(gvec, pairs, Z, c2a)
        delta_lbfgs = c2a.project_subspace(delta_lbfgs, Z)
        dir_lbfgs = c2a.components_to_field(delta_lbfgs, basis, phi.shape)
        candidates.append(("V5_FINE_LBFGS", dir_lbfgs))

    highvec = c2a.project_subspace(old_metrics["high"].reshape(-1), Z)
    if np.linalg.norm(highvec) > 1e-14 * max(np.linalg.norm(gvec), 1e-300):
        dir_high = c2a.components_to_field(-highvec, basis, phi.shape)
        candidates.append(("V5_FINE_HIGHPASS", dir_high))

    best = None
    for label, direction in candidates:
        pack = full_candidate(
            r4, r, qs2, c2a, cr2, cr3,
            state, g, E, rms, gmax,
            direction, label,
            frequency_guard=False,
            old_metrics=old_metrics,
        )
        if pack is not None and (best is None or pack["merit"] < best["merit"]):
            best = pack
            best["label"] = label

    return best


def build_coarse(r4, c2a, cr3, state, g):
    """Build the R4 residual-informed coarse basis and full Galerkin Hessian."""
    phi = state.phi
    basis = c2a.tangent_basis_householder(phi)
    Z = c2a.orthonormal_columns(c2a.isorotation_modes(phi, basis))
    gvec = c2a.project_subspace(c2a.field_to_components(g, basis), Z)
    gnorm = float(np.linalg.norm(gvec))
    gcomp = gvec.reshape(N - 2, N - 2, N - 2, 3)

    # Respect the R5 basis cap without mutating the imported module globally.
    candidates = r4.candidate_vectors(gcomp, state.axis)[:MAX_COARSE_BASIS]
    U = r4.orthonormal_coarse_basis(c2a, candidates, Z, gnorm)

    proj = U @ (U.T @ gvec)
    capture = float(np.linalg.norm(proj) / max(gnorm, 1e-300))
    orth = float(np.linalg.norm(gvec - proj) / max(gnorm, 1e-300))

    print(f"V5_COARSE_BASIS_DIM={U.shape[1]}", flush=True)
    print(f"V5_COARSE_GRADIENT_CAPTURE_FRACTION={capture:.15e}", flush=True)
    print(f"V5_COARSE_ORTHOGONAL_RESIDUAL_FRACTION={orth:.15e}", flush=True)

    if capture < MIN_COARSE_CAPTURE:
        print("V5_COARSE_CAPTURE_GATE=FAIL", flush=True)
        return None
    print("V5_COARSE_CAPTURE_GATE=PASS", flush=True)

    hvp, calls = c2a.make_hvp(cr3, phi, state.dx, basis, Z, HVP_POINT_ANGLE)
    HU = np.empty_like(U)
    for j in range(U.shape[1]):
        HU[:, j] = hvp(U[:, j])
        print(f"V5_COARSE_HVP_PROGRESS={j+1}/{U.shape[1]}", flush=True)

    Ac_raw = U.T @ HU
    asym = float(
        np.linalg.norm(Ac_raw - Ac_raw.T)
        / max(np.linalg.norm(Ac_raw), 1e-300)
    )
    print(f"V5_COARSE_GALERKIN_RELASYM={asym:.15e}", flush=True)
    if asym > 5e-6:
        raise RuntimeError("V5 coarse Galerkin symmetry audit failed")

    Ac = 0.5 * (Ac_raw + Ac_raw.T)
    evals = np.linalg.eigvalsh(Ac)
    emin = float(evals[0])
    emax = float(evals[-1])
    abs_nonzero = np.abs(
        evals[np.abs(evals) > 1e-12 * max(float(np.max(np.abs(evals))), 1.0)]
    )
    escale = float(np.median(abs_nonzero)) if abs_nonzero.size else max(abs(emax), 1.0)
    shift_floor = max(0.0, -emin + 0.05 * escale)

    print("V5_COARSE_EIGENVALUES=" + ",".join(f"{x:.9e}" for x in evals), flush=True)
    print(f"V5_COARSE_EIG_MIN={emin:.15e}", flush=True)
    print(f"V5_COARSE_EIG_MAX={emax:.15e}", flush=True)
    print(f"V5_COARSE_EIG_SCALE={escale:.15e}", flush=True)
    print(f"V5_COARSE_POSITIVITY_SHIFT_FLOOR={shift_floor:.15e}", flush=True)

    return {
        "basis": basis,
        "Z": Z,
        "gvec": gvec,
        "U": U,
        "Ac": Ac,
        "b": U.T @ gvec,
        "escale": escale,
        "shift_floor": shift_floor,
        "hvp_calls": calls["count"],
    }


def try_best_coarse(
    r4, r, qs2, c2a, cr2, cr3,
    state, E, g, rms, gmax,
):
    """Evaluate bounded coarse damping candidates and return the best full-field step."""
    old_metrics = residual_metrics(c2a, state.phi, g)
    coarse = build_coarse(r4, c2a, cr3, state, g)
    if coarse is None:
        return None, 0

    U = coarse["U"]
    Ac = coarse["Ac"]
    b = coarse["b"]
    Z = coarse["Z"]
    basis = coarse["basis"]
    escale = coarse["escale"]
    shift_floor = coarse["shift_floor"]

    best = None

    for mult in DAMPING_MULTIPLIERS:
        mu = shift_floor + max(0.0, mult) * escale
        mat = Ac + mu * np.eye(Ac.shape[0])

        try:
            coeff = np.linalg.solve(mat, -b)
        except np.linalg.LinAlgError:
            print(f"V5_COARSE_SOLVE_DAMP={mult:.6e} SINGULAR=YES", flush=True)
            continue

        coarse_rel = float(
            np.linalg.norm(b + mat @ coeff)
            / max(np.linalg.norm(b), 1e-300)
        )
        delta = c2a.project_subspace(U @ coeff, Z)
        direction = c2a.components_to_field(delta, basis, state.phi.shape)

        print(
            f"V5_COARSE_SOLVE_DAMP={mult:.6e} MU={mu:.15e} "
            f"COARSE_LINEAR_RELRES={coarse_rel:.15e}",
            flush=True,
        )

        pack = full_candidate(
            r4, r, qs2, c2a, cr2, cr3,
            state, g, E, rms, gmax,
            direction,
            f"V5_COARSE_DAMP_{mult:.6e}",
            frequency_guard=True,
            old_metrics=old_metrics,
        )

        if pack is not None and (best is None or pack["merit"] < best["merit"]):
            best = pack
            best["damp_mult"] = mult
            best["mu"] = mu

    return best, coarse["hvp_calls"]


def install_update(
    r, qs2, c2a, cr2, cr3, cr4r,
    state, history, old_g, old_merit, pack, kind,
):
    """Install one accepted full-field update and transport curvature history."""
    old_phi = state.phi
    r.transport_history_after_step(
        cr3, cr4r,
        old_phi, pack["cand"],
        pack["direction"], pack["alpha"],
        old_g, pack["g"],
        history,
    )

    state.phi = pack["cand"]
    state.accepted_total += 1

    t4 = cr3.topology4(state.phi, state.dx)
    deg_ok, degrees = cr3.geometric_guard(state.phi, cr2, True)
    angle = cr3.max_neighbor_angle(state.phi)

    if not deg_ok:
        raise RuntimeError("Installed V5 step lost geometric B=7")

    print(
        f"V5_STEP_ACCEPTED=YES KIND={kind} "
        f"ALPHA={pack['alpha']:.15e} "
        f"MERIT_REDUCTION_FACTOR={old_merit/max(pack['merit'],1e-300):.15e} "
        f"ENERGY={pack['E']:.15e} GRAD_RMS={pack['rms']:.15e} "
        f"GRAD_MAX={pack['gmax']:.15e} STATIONARITY_MERIT={pack['merit']:.15e} "
        f"TOPOLOGY4={t4:.15e} "
        f"GEOMETRIC_DEGREES={','.join(str(x) for x in degrees)} "
        f"MAX_NEIGHBOR_ANGLE={angle:.15e} "
        f"LOW_FRACTION={pack['metrics']['low_frac']:.15e} "
        f"HIGH_FRACTION={pack['metrics']['high_frac']:.15e} "
        f"ROUGHNESS={pack['metrics']['rough']:.15e}",
        flush=True,
    )

    return state


def vcycle_slice(
    r4, r3, r, qs2, c2a, cr2, cr3, cr4r,
    state, history,
    nk_total, coarse_total, vcycle_total, fine_total,
):
    """Run bounded nonlinear fine/coarse V-cycles."""
    E, _a, _b, _c, g, rms, gmax, station = r.strict_stationarity(
        cr3, state.phi, state.dx
    )

    stats = {
        "cycles_attempted": 0,
        "cycles_with_progress": 0,
        "fine_accepted": 0,
        "coarse_accepted": 0,
        "hvp_calls": 0,
    }

    initial_merit = stationarity_merit(rms, gmax)

    for cycle in range(1, MAX_CYCLES + 1):
        if station:
            break

        stats["cycles_attempted"] += 1
        cycle_start_merit = stationarity_merit(rms, gmax)
        cycle_progress = False

        print(
            f"\n=== V5 CYCLE {cycle} START ===\n"
            f"V5_CYCLE_START={cycle} GRAD_RMS={rms:.15e} GRAD_MAX={gmax:.15e} "
            f"STATIONARITY_MERIT={cycle_start_merit:.15e}",
            flush=True,
        )

        metrics = residual_metrics(c2a, state.phi, g)
        print_metrics(f"V5_CYCLE_{cycle}_START", metrics)

        # Re-audit the actual Hessian only once, before the first coarse use.
        if cycle == 1:
            basis_audit = c2a.tangent_basis_householder(state.phi)
            Z_audit = c2a.orthonormal_columns(c2a.isorotation_modes(state.phi, basis_audit))
            if not r.audit_hessian_operator(
                c2a, cr3, state.phi, state.axis, state.dx, basis_audit, Z_audit
            ):
                raise RuntimeError("V5 HVP validation failed")

        # Fine smoothing is indicated by rough/high residual or a failing max.
        fine_needed = bool(
            metrics["high_frac"] >= FINE_HIGH_TRIGGER
            or metrics["rough"] >= FINE_ROUGH_TRIGGER
            or gmax > GRAD_MAX_TOL
        )

        if fine_needed:
            print("V5_FINE_SMOOTHER_TRIGGER=YES", flush=True)
            for fine_step in range(1, MAX_FINE_STEPS + 1):
                if station:
                    break
                old_merit = stationarity_merit(rms, gmax)
                old_g = g

                pack = try_fine_smoother(
                    r4, r, qs2, c2a, cr2, cr3, cr4r,
                    state, history, E, g, rms, gmax,
                )
                if pack is None:
                    print(f"V5_FINE_STEP={fine_step} ACCEPTED=NO", flush=True)
                    break

                install_update(
                    r, qs2, c2a, cr2, cr3, cr4r,
                    state, history, old_g, old_merit, pack,
                    f"FINE_{pack['label']}",
                )
                fine_total += 1
                vcycle_total += 1
                stats["fine_accepted"] += 1
                cycle_progress = True

                E = pack["E"]
                g = pack["g"]
                rms = pack["rms"]
                gmax = pack["gmax"]
                station = pack["station"]

                save_checkpoint(
                    state, history, E, rms, gmax,
                    nk_total, coarse_total, vcycle_total, fine_total,
                )

                metrics = pack["metrics"]
                if (
                    metrics["high_frac"] < FINE_HIGH_TRIGGER
                    and metrics["rough"] < FINE_ROUGH_TRIGGER
                    and gmax <= GRAD_MAX_TOL
                ):
                    break
        else:
            print("V5_FINE_SMOOTHER_TRIGGER=NO", flush=True)

        if station:
            break

        # One coarse correction per V-cycle.  Consecutive coarse-only steps
        # are deliberately avoided because R4 showed they regenerate fine error.
        metrics = residual_metrics(c2a, state.phi, g)
        print_metrics(f"V5_CYCLE_{cycle}_PRECOARSE", metrics)

        if metrics["low_frac"] >= COARSE_LOW_TRIGGER:
            print("V5_COARSE_TRIGGER=YES", flush=True)
            old_merit = stationarity_merit(rms, gmax)
            old_g = g

            pack, hvp_calls = try_best_coarse(
                r4, r, qs2, c2a, cr2, cr3,
                state, E, g, rms, gmax,
            )
            stats["hvp_calls"] += hvp_calls

            if pack is not None:
                install_update(
                    r, qs2, c2a, cr2, cr3, cr4r,
                    state, history, old_g, old_merit, pack,
                    f"COARSE_DAMP_{pack['damp_mult']:.6e}",
                )
                coarse_total += 1
                vcycle_total += 1
                stats["coarse_accepted"] += 1
                cycle_progress = True

                E = pack["E"]
                g = pack["g"]
                rms = pack["rms"]
                gmax = pack["gmax"]
                station = pack["station"]

                save_checkpoint(
                    state, history, E, rms, gmax,
                    nk_total, coarse_total, vcycle_total, fine_total,
                )
            else:
                print("V5_COARSE_STEP_ACCEPTED=NO", flush=True)
        else:
            print("V5_COARSE_TRIGGER=NO", flush=True)

        cycle_end_merit = stationarity_merit(rms, gmax)
        reduction = cycle_start_merit / max(cycle_end_merit, 1e-300)
        if cycle_progress:
            stats["cycles_with_progress"] += 1

        print(
            f"V5_CYCLE_END={cycle} GRAD_RMS={rms:.15e} GRAD_MAX={gmax:.15e} "
            f"STATIONARITY_MERIT={cycle_end_merit:.15e} "
            f"CYCLE_MERIT_REDUCTION_FACTOR={reduction:.15e}",
            flush=True,
        )

        # Complete-cycle stagnation is a decisive stop for an augmented full
        # Krylov method rather than endless alternating microsteps.
        if not cycle_progress or reduction < 1.002:
            print("V5_CYCLE_STAGNATION_STOP=YES", flush=True)
            break

    total_reduction = initial_merit / max(stationarity_merit(rms, gmax), 1e-300)
    stats["total_merit_reduction"] = total_reduction
    return (
        state, history, E, g, rms, gmax, station,
        nk_total, coarse_total, vcycle_total, fine_total, stats,
    )


def main():
    print("=== 023C2AQS2R5 — TWO-LEVEL V-CYCLE N73 STATIONARITY CLOSURE ===", flush=True)

    print("\n=== A — FAIL-CLOSED UPSTREAM AUDIT ===", flush=True)
    require(R4_SOURCE)
    actual = sha256(R4_SOURCE)
    print(f"023C2AQS2R4_SOURCE_SHA256={actual}", flush=True)
    if actual != EXPECTED_R4_SHA256:
        raise RuntimeError("023C2AQS2R4 source hash mismatch")
    print("UPSTREAM_023C2AQS2R4_AUDIT=PASS", flush=True)

    r4 = load_module("c2aqs2r5_r4", R4_SOURCE)
    r3 = r4.load_module("c2aqs2r5_r3", r4.R3_SOURCE)
    r2 = r3.load_module("c2aqs2r5_r2", r3.R2_SOURCE)
    r = r3.load_module("c2aqs2r5_r", r2.R_SOURCE)
    qs2 = r3.load_module("c2aqs2r5_qs2", r.QS2_SOURCE)
    c2a = r3.load_module("c2aqs2r5_c2a", r.C2A_SOURCE)
    c2ar = qs2.load_module("c2aqs2r5_c2ar", qs2.C2AR_SOURCE)
    c2aqs = qs2.load_module("c2aqs2r5_c2aqs", qs2.C2AQS_SOURCE)
    cr2 = c2ar.load_module("c2aqs2r5_cr2", c2ar.CR2_SOURCE)
    cr3 = c2ar.load_module("c2aqs2r5_cr3", c2ar.CR3_SOURCE)
    cr4r = c2ar.load_module("c2aqs2r5_cr4r", c2ar.CR4R_SOURCE)

    print("\n=== B — LOAD LATEST N73 FIELD ===", flush=True)
    (
        state, history, source, discarded, norm_err,
        nk_total, coarse_total, vcycle_total, fine_total,
    ) = load_state(r4, qs2, cr3, cr4r)

    E0, _a, _b, _c, g0, rms0, gmax0, station0 = r.strict_stationarity(
        cr3, state.phi, state.dx
    )
    deg_ok0, degrees0 = cr3.geometric_guard(state.phi, cr2, True)

    print(f"V5_START_SOURCE={source.relative_to(ROOT)}", flush=True)
    print(f"V5_START_ACCEPTED_TOTAL={state.accepted_total}", flush=True)
    print(f"V5_START_NEWTON_ACCEPTED_TOTAL={nk_total}", flush=True)
    print(f"V5_START_COARSE_ACCEPTED_TOTAL={coarse_total}", flush=True)
    print(f"V5_START_VCYCLE_ACCEPTED_TOTAL={vcycle_total}", flush=True)
    print(f"V5_START_FINE_ACCEPTED_TOTAL={fine_total}", flush=True)
    print(f"V5_START_HISTORY_LENGTH={len(history)}", flush=True)
    print(f"V5_START_HISTORY_DISCARDED={discarded}", flush=True)
    print(f"V5_START_NORM_MAXERR={norm_err:.15e}", flush=True)
    print(f"V5_START_ENERGY={E0:.15e}", flush=True)
    print(f"V5_START_GRAD_RMS={rms0:.15e}", flush=True)
    print(f"V5_START_GRAD_MAX={gmax0:.15e}", flush=True)
    print(f"V5_START_STATIONARITY_MERIT={stationarity_merit(rms0,gmax0):.15e}", flush=True)
    print("V5_START_STRICT_STATIONARITY=" + ("PASS" if station0 else "FAIL"), flush=True)
    print(f"V5_START_TOPOLOGY4={cr3.topology4(state.phi,state.dx):.15e}", flush=True)
    print("V5_START_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in degrees0), flush=True)

    if not deg_ok0:
        raise RuntimeError("Starting R4 field failed geometric B=7")

    print("\n=== C — START RESIDUAL AUDIT ===", flush=True)
    cr4r.residual_localization(cr3, state, g0)
    print_metrics("V5_START", residual_metrics(c2a, state.phi, g0))

    if station0:
        E, g, rms, gmax, station = E0, g0, rms0, gmax0, station0
        stats = {
            "cycles_attempted": 0, "cycles_with_progress": 0,
            "fine_accepted": 0, "coarse_accepted": 0,
            "hvp_calls": 0, "total_merit_reduction": 1.0,
        }
    else:
        print("\n=== D — TWO-LEVEL V-CYCLE SLICE ===", flush=True)
        (
            state, history, E, g, rms, gmax, station,
            nk_total, coarse_total, vcycle_total, fine_total, stats,
        ) = vcycle_slice(
            r4, r3, r, qs2, c2a, cr2, cr3, cr4r,
            state, history,
            nk_total, coarse_total, vcycle_total, fine_total,
        )

    print("\n=== E — END-OF-SLICE AUDIT ===", flush=True)
    t4 = cr3.topology4(state.phi, state.dx)
    deg_ok, degrees = cr3.geometric_guard(state.phi, cr2, True)
    angle = cr3.max_neighbor_angle(state.phi)

    print(f"V5_CYCLES_ATTEMPTED={stats['cycles_attempted']}", flush=True)
    print(f"V5_CYCLES_WITH_PROGRESS={stats['cycles_with_progress']}", flush=True)
    print(f"V5_FINE_ACCEPTED={stats['fine_accepted']}", flush=True)
    print(f"V5_COARSE_ACCEPTED={stats['coarse_accepted']}", flush=True)
    print(f"V5_HVP_MATVEC_CALLS={stats['hvp_calls']}", flush=True)
    print(f"V5_TOTAL_MERIT_REDUCTION_FACTOR={stats['total_merit_reduction']:.15e}", flush=True)
    print(f"V5_FINAL_ENERGY={E:.15e}", flush=True)
    print(f"V5_FINAL_GRAD_RMS={rms:.15e}", flush=True)
    print(f"V5_FINAL_GRAD_MAX={gmax:.15e}", flush=True)
    print(f"V5_FINAL_STATIONARITY_MERIT={stationarity_merit(rms,gmax):.15e}", flush=True)
    print("V5_FINAL_STRICT_STATIONARITY=" + ("PASS" if station else "FAIL"), flush=True)
    print(f"V5_FINAL_TOPOLOGY4={t4:.15e}", flush=True)
    print("V5_FINAL_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in degrees), flush=True)
    print(f"V5_FINAL_MAX_NEIGHBOR_ANGLE={angle:.15e}", flush=True)

    print("\n=== F — FINAL RESIDUAL AUDIT ===", flush=True)
    cr4r.residual_localization(cr3, state, g)
    print_metrics("V5_FINAL", residual_metrics(c2a, state.phi, g))

    if not station:
        save_checkpoint(
            state, history, E, rms, gmax,
            nk_total, coarse_total, vcycle_total, fine_total,
        )

        print("\n=== G — BOUNDED INCOMPLETE DECISION ===", flush=True)
        print("023C2AQS2R5_TWO_LEVEL_VCYCLE=INCOMPLETE_N73_STATIONARITY", flush=True)
        print("N73_ACTUAL_FINE_STRICT_STATIONARITY=NOT_YET", flush=True)

        if stats["total_merit_reduction"] >= 1.10 and stats["cycles_with_progress"] > 0:
            print("TWO_LEVEL_VCYCLE_LOCAL_ACCELERATION=SUPPORTED", flush=True)
            print("NEXT=RERUN_SAME_023C2AQS2R5_FROM_VCYCLE_CHECKPOINT", flush=True)
        else:
            print("TWO_LEVEL_VCYCLE_LOCAL_ACCELERATION=NOT_ESTABLISHED", flush=True)
            print("NEXT=023C2AQS2R6_AUGMENTED_DEFLATED_FULL_MINRES_GATE", flush=True)

        print("N73_CONTINUOUS_FORCE=NOT_RUN_BEFORE_STATIONARITY", flush=True)
        print("FULL_PHYSICAL_HESSIAN=DEFERRED_OPERATIONAL_FORCE_AND_FINE_FIELD_UNRESOLVED", flush=True)
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR_NOT_A_PROBABILITY", flush=True)
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED", flush=True)
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
        return

    print("\n=== G — STRICT N73 PHYSICAL FIELD AUDIT ===", flush=True)
    diag = cr3.continuum_local_diagnostics(state.phi, state.axis, state.dx, cr2)

    print(f"V5_N73_STATIONARY_CONTINUUM_ENERGY={diag.energy_continuum:.15e}", flush=True)
    print(f"V5_N73_STATIONARY_ACTIVE_TOTAL={diag.active_total:.15e}", flush=True)
    print(f"V5_N73_STATIONARY_MIN_ACTIVE_FRACTION={diag.min_active_fraction:.15e}", flush=True)
    print(f"V5_N73_STATIONARY_MIN_DEC_SCALED_MARGIN={diag.min_dec_scaled_margin:.15e}", flush=True)
    print(f"V5_N73_STATIONARY_MAX_ACTIVE_TRACE_SCALED={diag.max_active_trace_scaled:.15e}", flush=True)

    physical_gate = bool(
        deg_ok
        and diag.active_total > 0.0
        and diag.min_active_fraction <= -1.0e-2
        and diag.min_dec_scaled_margin >= -1.0e-9
        and diag.max_active_trace_scaled <= 1.0e-10
        and angle <= MAX_NEIGHBOR_ANGLE
    )

    print("V5_N73_STATIONARY_PHYSICAL_FIELD_GATE=" + ("PASS" if physical_gate else "FAIL"), flush=True)
    save_final(
        state, E, rms, gmax, diag,
        nk_total, coarse_total, vcycle_total, fine_total,
    )

    if not physical_gate:
        print("023C2AQS2R5_TWO_LEVEL_VCYCLE=RED_STRICT_N73_PHYSICAL_FIELD_GATE", flush=True)
        print("FULL_PHYSICAL_HESSIAN=DEFERRED_BY_FINE_FIELD_PHYSICAL_FALSIFIER", flush=True)
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_PENDING_RERANK", flush=True)
        print("NEXT=PRESERVE_NEGATIVE_RESULT_AND_RERANK_023_BRANCH", flush=True)
        return

    print("\n=== H — CONDITIONAL CONTINUOUS-FORCE CERTIFICATE ===", flush=True)
    n65ref = qs2.load_n65_force_reference()
    aqr = c2aqs.load_module("c2aqs2r5_aqr", c2aqs.AQR_SOURCE)
    aqr.validate_analytic_formulae()
    print("V5_N73_ANALYTIC_KERNEL_VALIDATION=PASS", flush=True)

    force = qs2.continuous_force_gate(
        c2aqs, aqr, cr3, state.phi, state.axis, state.dx, n65ref
    )

    print("\n=== I — 023C2AQS2R5 DECISION ===", flush=True)

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

    print(f"023C2AQS2R5_TWO_LEVEL_VCYCLE={decision}", flush=True)
    print("N73_ACTUAL_FINE_STRICT_STATIONARITY=PASS", flush=True)
    print(f"FULL_PHYSICAL_HESSIAN={hessian}", flush=True)
    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR_NOT_A_PROBABILITY", flush=True)
    print(f"NEXT={next_step}", flush=True)
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED_UNTIL_023C_COMPLETE", flush=True)
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
    print("NEW_PHYSICS_DISCOVERY=NO", flush=True)
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023C2AQS2R5_TWO_LEVEL_VCYCLE_STATIONARITY_REPAIR", flush=True)


if __name__ == "__main__":
    main()
