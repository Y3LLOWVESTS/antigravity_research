#!/usr/bin/env python3
"""023C2AQS2 — actual N=73 stationary-field and continuous-force resolution gate.

PURPOSE
-------
Resolve the dominant uncertainty left by 023C2AQS: the finite-payload kernel and
continuous cubature are now validated, but the strict-stationary N=65 field is
not fine enough to certify the historically weakest payload-force sign because
cubic and quintic continuous-field reconstructions differ by more than the
small net force.

This file therefore advances the *actual field resolution* rather than further
refining quadrature on the same N=65 samples.  It resumes the already-computed
N=73 unrestricted B=7 field, drives that SAME discrete field equation toward
the unchanged strict-stationarity thresholds, and only after stationarity
rebuilds the continuous active source S=2(e4-V) from independent cubic and
quintic field splines and recomputes the finite-payload force.

SCIENTIFIC QUESTION
-------------------
Does a genuinely finer, strictly stationary unrestricted N=73 B=7 field retain
an operationally outward finite-payload response along the historically weakest
orientation when the force is reconstructed from the continuous field rather
than a point/midpoint source table?

A second question is numerical: does going from N=65 to an actual stationary
N=73 field shrink the cubic-vs-quintic representation spread that prevented the
N=65 force sign from being certified?

PHYSICAL MODEL
--------------
The static SU(2) Skyrme field is

    phi = (sigma, pi1, pi2, pi3),    phi.phi = 1,

with

    E = integral (e2 + e4 + V) d^3x,

    V = m^2 (1-sigma)(1+eta sigma),

    S = rho + p1 + p2 + p3 = 2(e4 - V),

at the already selected parameters

    B=7, eta=0.4, m=8.

No stabilizer, symmetry restriction, rational-map constraint, altered payload,
or new interaction is introduced.

DISCRETE FIELD EQUATION
-----------------------
The N=73 solve uses exactly the checkerboard-free parity-symmetrized fourth-
order one-sided action and exact analytic gradient already validated in
023CR3/023CR4R.  The true-vacuum outer boundary, topology-4 guard, exact
geometric B=7 witnesses, and link-smoothness guard are unchanged.

STATIONARITY SOLVER
-------------------
The current N=73 state already contains a valid Riemannian L-BFGS history.  This
run preserves that history and permits it to grow from 7 to a modest larger
window.  Near stationarity, ordinary Armijo energy decrease can accept steps
that lower E while strongly increasing the Euler-Lagrange residual.  Therefore
this continuation adds a *numerical optimizer safeguard only*: after an Armijo-
admissible step, the exact candidate gradient is evaluated and very large
residual-growth steps are backtracked.  No physical configuration is excluded;
a steepest-descent fallback remains available and all original physical guards
are retained.

The stationarity thresholds are NOT weakened:

    grad_RMS <= 1.5e-3,
    grad_max <= 5.0e-2.

This is consistent with the project rule that a numerical repair may improve
how the same equations are solved but may not make the scientific gate easier.

CONTINUOUS ACTIVE SOURCE
------------------------
After strict N=73 stationarity only, the four field components are independently
reconstructed with cubic and quintic tensor-product splines.  For raw spline
field u(x), the physical field is

    phi = u/|u|,

and the exact derivative of the normalized interpolant is

    d_i phi = [d_i u - phi (phi.d_i u)] / |u|.

The code rebuilds e4, V, and S=2(e4-V) at integration points.  It does not
interpolate the scalar source table.

FINITE-PAYLOAD OBSERVABLE
-------------------------
For a uniform spherical passive payload of radius R centered at c, along unit
radial direction n,

    A_n = integral S(x)
                 n.(x-c) / max(|x-c|^3, R^3)
                 d^3x.

Positive A_n is outward in the inherited project convention.  This file tests
only the historically weakest orientation.  A complete 320-direction audit is
not authorized until this cheapest direction is numerically resolved.

NUMERICAL FORCE CERTIFICATE
---------------------------
The validated 023C2AQS continuous operator is reused:

- far-field Gauss-Legendre orders 2, 3, and 4;
- aggressively subdivided near-payload cells;
- independent cubic and quintic field reconstructions;
- analytic rectangular-prism constant-source validation;
- normalized-spline derivative finite-difference validation.

The sign is certified only if cubic and quintic agree in sign and

    min(|A_cubic|, |A_quintic|)
      > 5 * max(internal_errors, representation_spread).

The factor 5 is unchanged from 023C2AQS.

N=65 REFERENCE
--------------
The successful 023C2AQS log is parsed fail-closed for the N=65 q=4 continuous
forces and representation spread.  These values are used only as a resolution-
trend diagnostic.  They are NOT re-promoted as a certified N=65 sign.

PROMOTION / STOP RULES
----------------------
1. If N=73 does not reach strict stationarity during the bounded work slice,
   save field + full L-BFGS history and exit INCOMPLETE.  Re-run this file.
2. If B=7, smoothness, positive total active mass, negative active core, DEC,
   or active-trace consistency fail at strict stationarity, stop and preserve
   the negative result.
3. If the N=73 continuous force is robustly inward, the declared payload
   orientation blocks the all-outward 023C claim; do not run the Hessian.
4. If the force is unresolved, the next field-resolution gate is N=81; do not
   spend compute on the full Hessian yet.
5. If the N=73 force is robustly outward and representation uncertainty shrinks,
   authorize an N=81 stationary companion / dense continuous-force resolution
   gate.  Full Hessian remains deferred until operational force convergence.

INPUTS
------
simulations/023c2ar_n73_persistent_rlbfgs_stationarity_sentinel.py
simulations/023c2aqs_continuous_field_active_source_force_integration.py
results/data/023c2ar_n73_persistent_rlbfgs_checkpoint.npz
results/logs/023c2aqs_continuous_field_active_source_force_integration.log

On later invocations this file prefers its own checkpoint.

OUTPUTS
-------
results/data/023c2aqs2_n73_stationarity_checkpoint.npz
results/data/023c2aqs2_strict_stationary_b7_n73.npz
plus text diagnostics captured by the caller's run log.

UNITS / SIGN CONVENTIONS
------------------------
Dimensionless Skyrme normalization.  Positive radial payload value means
outward acceleration after the omitted common positive linearized-GR factor.
Geometric degree is expected to be -7 because of the inherited orientation;
promotion uses |B|=7.

VALIDATION / FALSIFICATION
--------------------------
- fail-closed upstream source hashes;
- 94 known-solutions tests are expected to be run by the shell wrapper;
- unchanged exact action/gradient from audited upstream code;
- exact geometric degree + derivative topology + smoothness during relaxation;
- N=73 continuum stress/DEC/trace audit at stationarity;
- independent cubic/quintic continuous-field reconstructions;
- analytic normalized-spline derivative checks;
- constant-source cubature vs analytic prism field;
- q=2/3/4 and near-payload integration convergence;
- conservative sign certificate.

LIMITATIONS
-----------
This file does not establish the full physical Hessian, fission stability,
nonlinear Einstein-Skyrme consistency, practical energy scaling, a material
realization, an experiment, or a practical antigravity device.

RELATED FILES
-------------
simulations/023cr4r_rlbfgs_stationarity_closure_gradient_audit_repair.py
simulations/023c2a_n73_resolution_and_full_tangent_hessian.py
simulations/023c2ar_n73_persistent_rlbfgs_stationarity_sentinel.py
simulations/023c2aqr_analytic_prism_exact_cap_payload_operator.py
simulations/023c2aqs_continuous_field_active_source_force_integration.py

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023C2AQS2_ACTUAL_N73_FIELD_RESOLUTION

A green result is a field-resolution/operational-observable accomplishment only.
It does not by itself establish unrestricted stability or practical antigravity.
"""

from __future__ import annotations

import hashlib
import importlib.util
import math
import os
from pathlib import Path
import re
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

C2AR_SOURCE = ROOT / "simulations/023c2ar_n73_persistent_rlbfgs_stationarity_sentinel.py"
C2AQS_SOURCE = ROOT / "simulations/023c2aqs_continuous_field_active_source_force_integration.py"
EXPECTED_C2AR_SHA256 = "50ce682704f0786b49c8460a9a588f8245460db5b34a9118d85aef0a5412267a"
EXPECTED_C2AQS_SHA256 = "e6d6131d7b26c1a140f1b214cec8f73d129d4288be4960cace124fc3a8250434"

UPSTREAM_CHECKPOINT = ROOT / "results/data/023c2ar_n73_persistent_rlbfgs_checkpoint.npz"
CHECKPOINT = ROOT / "results/data/023c2aqs2_n73_stationarity_checkpoint.npz"
FINAL = ROOT / "results/data/023c2aqs2_strict_stationary_b7_n73.npz"
N65_FORCE_LOG = ROOT / "results/logs/023c2aqs_continuous_field_active_source_force_integration.log"

B = 7
ETA = 0.40
MASS = 8.0
N = 73

GRAD_RMS_TOL = 1.5e-3
GRAD_MAX_TOL = 5.0e-2
MAX_TOPOLOGY_RELERR = 3.0e-2
MAX_NEIGHBOR_ANGLE = 0.70

MAX_ACCEPTED = int(os.environ.get("AG_N73_FINE_MAX_ACCEPTED", "160"))
CHECKPOINT_EVERY = int(os.environ.get("AG_N73_FINE_CHECKPOINT_EVERY", "20"))
PROGRESS_EVERY = int(os.environ.get("AG_N73_FINE_PROGRESS_EVERY", "10"))
HISTORY_SIZE = int(os.environ.get("AG_N73_FINE_HISTORY", "20"))
GRAD_GROWTH_RMS = float(os.environ.get("AG_N73_FINE_GRAD_GROWTH_RMS", "1.6"))
GRAD_GROWTH_MAX = float(os.environ.get("AG_N73_FINE_GRAD_GROWTH_MAX", "2.5"))
GRAD_SAFEGUARD_ACTIVATE = float(os.environ.get("AG_N73_FINE_GRAD_SAFEGUARD_ACTIVATE", "1.0"))
MAX_LINESEARCH = int(os.environ.get("AG_N73_FINE_MAX_LINESEARCH", "14"))
MIN_ALPHA = 2.0 ** -24
ARMIJO_C1 = 1.0e-4
CAUTIOUS_CURVATURE = 1.0e-7


def sha256(path: Path) -> str:
    """Return SHA-256 of one source file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def require(path: Path) -> None:
    """Fail closed when a required project artifact is absent."""
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def load_module(name: str, path: Path):
    """Load a project simulation as an auditable Python module."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def strict_stationarity(cr3, phi: np.ndarray, dx: float):
    """Return exact discrete energy, Riemannian gradient, and strict gate."""
    E, E2, E4, E0, g = cr3.riemannian_gradient_density(phi, dx)
    rms, gmax = cr3.gradient_norms(g)
    station = bool(rms <= GRAD_RMS_TOL and gmax <= GRAD_MAX_TOL)
    return float(E), float(E2), float(E4), float(E0), g, float(rms), float(gmax), station


def history_from_arrays(cr3, s_hist: np.ndarray, y_hist: np.ndarray, dx: float):
    """Rebuild positive-curvature R-LBFGS correction pairs."""
    history = []
    discarded = 0
    if s_hist.size == 0 or y_hist.size == 0:
        return history, discarded
    if s_hist.shape != y_hist.shape or s_hist.ndim != 5 or s_hist.shape[1:] != (N, N, N, 4):
        raise RuntimeError(f"Invalid persisted history shapes: {s_hist.shape}, {y_hist.shape}")
    for s, y in zip(s_hist, y_hist):
        sy = cr3.tangent_inner(s, y, dx)
        if math.isfinite(sy) and sy > 1e-300:
            history.append((np.array(s, copy=True), np.array(y, copy=True), 1.0 / sy))
        else:
            discarded += 1
    return history[-HISTORY_SIZE:], discarded


def load_state(cr3, cr4r):
    """Load this gate's checkpoint, else the latest 023C2AR N=73 state."""
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
    if phi.shape != (N, N, N, 4) or axis.shape != (N,):
        raise RuntimeError(f"Unexpected N73 state shape phi={phi.shape} axis={axis.shape}")
    if b != B or abs(eta - ETA) > 1e-14 or abs(mass - MASS) > 1e-14:
        raise RuntimeError("N73 physical metadata mismatch")
    norm_err = float(np.max(np.abs(np.linalg.norm(phi, axis=-1) - 1.0)))
    if norm_err > 5e-10:
        raise RuntimeError(f"N73 S3 norm violation {norm_err}")
    history, discarded = history_from_arrays(cr3, s_hist, y_hist, dx)
    state = cr4r.State(phi=phi, axis=axis, dx=dx, accepted_total=accepted_total)
    return state, history, source, discarded, norm_err


def save_checkpoint(state, history, E: float, rms: float, gmax: float) -> None:
    """Persist field plus full current curvature history without compression."""
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
        energy=np.array(E), grad_rms=np.array(rms), grad_max=np.array(gmax),
        source=np.array("023C2AQS2_STABILIZED_RLBFGS"),
        s_hist=s_hist, y_hist=y_hist,
    )
    print(
        f"N73_FINE_CHECKPOINT_WRITTEN={CHECKPOINT.relative_to(ROOT)} "
        f"HISTORY_LENGTH={len(history)}",
        flush=True,
    )


def save_final(state, E: float, rms: float, gmax: float, diag) -> None:
    """Persist the strict-stationary N=73 field for later resolution gates."""
    FINAL.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        FINAL,
        phi=state.phi,
        axis=state.axis,
        dx=np.array(state.dx),
        B=np.array(B), eta=np.array(ETA), mass=np.array(MASS),
        accepted_total=np.array(state.accepted_total),
        energy=np.array(E), grad_rms=np.array(rms), grad_max=np.array(gmax),
        topology4=np.array(diag.topology4),
        active_total=np.array(diag.active_total),
        min_active_fraction=np.array(diag.min_active_fraction),
        min_dec_scaled_margin=np.array(diag.min_dec_scaled_margin),
        max_active_trace_scaled=np.array(diag.max_active_trace_scaled),
        energy_centroid_norm=np.array(diag.energy_centroid_norm),
        source=np.array("023C2AQS2_N73_STRICT_STATIONARY"),
    )
    print(f"STRICT_N73_FINE_FIELD_ARTIFACT={FINAL.relative_to(ROOT)}", flush=True)


def trust_rotation(rms: float) -> float:
    """Return a shrinking numerical trust radius near the stationary point."""
    if rms <= 1.0e-2:
        return 0.005
    if rms <= 1.0e-1:
        return 0.010
    return 0.020


def two_loop_direction(cr3, g, history, dx):
    """Apply R-LBFGS inverse-Hessian recursion for arbitrary history length."""
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


def candidate_admissible(cr3, cr2, cand, dx: float, accepted_next: int):
    """Apply unchanged topology/smoothness guards to one candidate field."""
    angle = cr3.max_neighbor_angle(cand)
    if angle > MAX_NEIGHBOR_ANGLE:
        return False, "SMOOTHNESS", None
    t4 = cr3.topology4(cand, dx)
    if abs(abs(t4) / B - 1.0) > MAX_TOPOLOGY_RELERR:
        return False, "TOPOLOGY4", None
    full_guard = accepted_next % 30 == 0
    do_guard = accepted_next % 10 == 0
    if do_guard:
        gok, degrees = cr3.geometric_guard(cand, cr2, full_guard)
        if not gok:
            return False, "GEOMETRIC", degrees
    return True, "PASS", None


def stabilized_rlbfgs(cr2, cr3, cr4r, state, history):
    """Continue N=73 stationarity with persistent history and residual safeguard."""
    E, _E2, _E4, _E0, g, rms, gmax, station = strict_stationarity(cr3, state.phi, state.dx)
    accepted_this = 0
    rejected_energy = 0
    rejected_gradient = 0
    rejected_topology = 0
    rejected_smoothness = 0
    history_resets = 0
    secant_rejects = 0
    fallback_steps = 0

    while accepted_this < MAX_ACCEPTED and not station:
        phi = state.phi
        dx = state.dx
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

        max_dir = float(np.max(np.linalg.norm(direction[1:-1, 1:-1, 1:-1], axis=-1)))
        alpha = min(1.0, trust_rotation(rms) / max(max_dir, 1e-300))
        accepted_next = state.accepted_total + 1
        trial_pack = None

        for _ in range(MAX_LINESEARCH):
            if alpha < MIN_ALPHA:
                break
            cand = cr3.exp_map_update(phi, direction, alpha)
            Etrial = cr3.high_order_energy_gradient(cand, dx, False)[0]
            if (not math.isfinite(Etrial)) or Etrial > E + ARMIJO_C1 * alpha * gd:
                rejected_energy += 1
                alpha *= 0.5
                continue
            ok, reason, _ = candidate_admissible(cr3, cr2, cand, dx, accepted_next)
            if not ok:
                if reason == "SMOOTHNESS":
                    rejected_smoothness += 1
                else:
                    rejected_topology += 1
                alpha *= 0.5
                continue

            # Near the solution evaluate the exact residual before accepting.
            pack = strict_stationarity(cr3, cand, dx)
            Eexact, E2t, E4t, E0t, gtrial, rmst, gmaxt, stationt = pack
            if rms <= GRAD_SAFEGUARD_ACTIVATE:
                rms_cap = max(GRAD_GROWTH_RMS * rms, 10.0 * GRAD_RMS_TOL)
                gmax_cap = max(GRAD_GROWTH_MAX * gmax, 10.0 * GRAD_MAX_TOL)
                if rmst > rms_cap or gmaxt > gmax_cap:
                    rejected_gradient += 1
                    alpha *= 0.5
                    continue
            trial_pack = (cand, Eexact, E2t, E4t, E0t, gtrial, rmst, gmaxt, stationt)
            break

        if trial_pack is None:
            # Conservative fallback: discard quasi-Newton history and take a
            # small steepest-descent step.  Physical guards remain unchanged.
            history.clear()
            history_resets += 1
            fallback_steps += 1
            direction = -g
            gd = -gg
            max_dir = float(np.max(np.linalg.norm(direction[1:-1, 1:-1, 1:-1], axis=-1)))
            alpha = min(0.125, 0.005 / max(max_dir, 1e-300))
            for _ in range(MAX_LINESEARCH):
                if alpha < MIN_ALPHA:
                    break
                cand = cr3.exp_map_update(phi, direction, alpha)
                Etrial = cr3.high_order_energy_gradient(cand, dx, False)[0]
                if (not math.isfinite(Etrial)) or Etrial > E + ARMIJO_C1 * alpha * gd:
                    rejected_energy += 1
                    alpha *= 0.5
                    continue
                ok, reason, _ = candidate_admissible(cr3, cr2, cand, dx, accepted_next)
                if not ok:
                    if reason == "SMOOTHNESS":
                        rejected_smoothness += 1
                    else:
                        rejected_topology += 1
                    alpha *= 0.5
                    continue
                pack = strict_stationarity(cr3, cand, dx)
                trial_pack = (cand,) + pack
                break

        if trial_pack is None:
            print("N73_FINE_LINE_SEARCH_FAILED=YES", flush=True)
            break

        old_phi = phi
        old_g = g
        old_direction = direction
        old_history = history

        cand, E, _E2, _E4, _E0, g, rms, gmax, station = trial_pack
        state.phi = cand
        state.accepted_total += 1
        accepted_this += 1

        geom = cr4r.transport_geometry(old_phi, old_direction, alpha, state.phi)
        transported = []
        for s_old, y_old, _rho_old in old_history:
            st = cr4r.exact_parallel_transport(old_phi, geom, s_old, cr3)
            yt = cr4r.exact_parallel_transport(old_phi, geom, y_old, cr3)
            sy_t = cr3.tangent_inner(st, yt, state.dx)
            if sy_t > 1e-300:
                transported.append((st, yt, 1.0 / sy_t))

        g_old_t = cr4r.exact_parallel_transport(old_phi, geom, old_g, cr3)
        step_old = alpha * old_direction
        s_new = cr4r.exact_parallel_transport(old_phi, geom, step_old, cr3)
        y_new = g - g_old_t
        ss = cr3.tangent_inner(s_new, s_new, state.dx)
        yy = cr3.tangent_inner(y_new, y_new, state.dx)
        sy = cr3.tangent_inner(s_new, y_new, state.dx)
        cautious = CAUTIOUS_CURVATURE * math.sqrt(max(ss * yy, 0.0))
        if math.isfinite(sy) and sy > max(cautious, 1e-300):
            transported.append((s_new, y_new, 1.0 / sy))
        else:
            secant_rejects += 1
        history = transported[-HISTORY_SIZE:]

        if accepted_this % PROGRESS_EVERY == 0 or station:
            print(
                f"N73_FINE_PROGRESS_THIS_RUN={accepted_this} "
                f"ACCEPTED_TOTAL={state.accepted_total} ENERGY={E:.15e} "
                f"GRAD_RMS={rms:.15e} GRAD_MAX={gmax:.15e} "
                f"TOPOLOGY4={cr3.topology4(state.phi, state.dx):.15e} "
                f"HISTORY={len(history)} TRUST_ROTATION={trust_rotation(rms):.9e} "
                f"ALPHA={alpha:.15e}",
                flush=True,
            )

        if accepted_this % CHECKPOINT_EVERY == 0 or station:
            save_checkpoint(state, history, E, rms, gmax)

    save_checkpoint(state, history, E, rms, gmax)
    stats = {
        "accepted_this": accepted_this,
        "rejected_energy": rejected_energy,
        "rejected_gradient": rejected_gradient,
        "rejected_topology": rejected_topology,
        "rejected_smoothness": rejected_smoothness,
        "history_resets": history_resets,
        "secant_rejects": secant_rejects,
        "fallback_steps": fallback_steps,
    }
    return state, history, E, g, rms, gmax, station, stats


def log_value(text: str, key: str) -> float:
    """Extract one scientific floating-point marker from an upstream log."""
    m = re.search(rf"^{re.escape(key)}=([-+0-9.eE]+)$", text, flags=re.MULTILINE)
    if not m:
        raise RuntimeError(f"Missing upstream N65 marker {key}")
    return float(m.group(1))


def load_n65_force_reference():
    """Read the N=65 q=4 continuous-force result without re-running it."""
    require(N65_FORCE_LOG)
    text = N65_FORCE_LOG.read_text(errors="replace")
    marker = "023C2AQS_CONTINUOUS_FIELD_ACTIVE_SOURCE_FORCE_INTEGRATION=INCOMPLETE_CONTINUOUS_SOURCE_SIGN_NOT_CERTIFIED"
    if marker not in text:
        raise RuntimeError("N65 continuous-force log does not contain expected decision marker")
    return {
        "cubic": log_value(text, "CUBIC_CONTINUOUS_BEST_FORCE"),
        "quintic": log_value(text, "QUINTIC_CONTINUOUS_BEST_FORCE"),
        "spread": log_value(text, "CONTINUOUS_REPRESENTATION_SPREAD"),
        "error": log_value(text, "CONTINUOUS_FORCE_ERROR_BOUND"),
    }


def continuous_force_gate(c2aqs, aqr, cr3, phi, axis, dx, n65ref):
    """Run the validated continuous-field force certificate on strict N=73."""
    payload_center = float(c2aqs.load_module("c2aqs2_c2aq", aqr.C2AQ_SOURCE).PAYLOAD_CENTER)
    c2aq = sys.modules["c2aqs2_c2aq"]
    payload_radius = float(c2aq.PAYLOAD_RADIUS)
    direction = np.asarray(c2aq.KNOWN_WORST_DIRECTION, dtype=float)
    direction /= np.linalg.norm(direction)
    center = payload_center * direction

    print("\n=== F — N73 CONTINUOUS-FIELD FORCE PRECOMPUTE ===", flush=True)
    print(f"N73_FORCE_DX={dx:.15e}", flush=True)
    print(f"N73_PAYLOAD_RADIUS_OVER_DX={payload_radius/dx:.15e}", flush=True)
    print("N73_FORCE_DIRECTION=" + ",".join(f"{x:.15e}" for x in direction), flush=True)

    lowers = c2aqs.cell_lowers(axis)
    dmin = c2aqs.min_distance_to_cells(lowers, dx, center)
    near_radius = c2aqs.NEAR_RADIUS_DX * dx
    near_mask = dmin < near_radius
    near_lowers = lowers[near_mask]
    far_lowers = lowers[~near_mask]
    print(f"N73_TOTAL_FIELD_CELLS={len(lowers)}", flush=True)
    print(f"N73_NEAR_FIELD_CELLS={len(near_lowers)}", flush=True)

    offsets = {
        "far2": c2aqs.composite_gauss_offsets(dx, 2, 1),
        "far3": c2aqs.composite_gauss_offsets(dx, 3, 1),
        "far4": c2aqs.composite_gauss_offsets(dx, 4, 1),
        "near_coarse": c2aqs.composite_gauss_offsets(dx, c2aqs.NEAR_GAUSS_ORDER, c2aqs.NEAR_COARSE_SUBDIV),
        "near_fine": c2aqs.composite_gauss_offsets(dx, c2aqs.NEAR_GAUSS_ORDER, c2aqs.NEAR_FINE_SUBDIV),
    }

    const_err = c2aqs.constant_source_validation(
        aqr, axis, dx, far_lowers, near_lowers, center, direction, payload_radius,
        *offsets["far3"], *offsets["near_fine"]
    )
    if const_err > c2aqs.FORCE_CONST_VALIDATION_REL_TOL:
        raise RuntimeError("N73 continuous cubature failed constant-source validation")

    print("\n=== G — N73 CUBIC / QUINTIC CONTINUOUS FIELDS ===", flush=True)
    interps = {}
    for method in ("cubic", "quintic"):
        print(f"N73_BUILDING_{method.upper()}_TENSOR_SPLINE=START", flush=True)
        interp = c2aqs.build_interpolator(axis, phi, method)
        interps[method] = interp
        print(f"N73_BUILDING_{method.upper()}_TENSOR_SPLINE=DONE", flush=True)
        nodal = c2aqs.nodal_reproduction_check(interp, phi, axis, method)
        deriv = c2aqs.finite_difference_derivative_check(interp, axis, dx, method)
        if nodal > c2aqs.NODAL_REPRO_ABS_TOL or deriv > c2aqs.DERIVATIVE_REL_TOL:
            raise RuntimeError(f"N73 {method} continuous-field validation failed")
        c2aqs.central_source_diagnostic(cr3, phi, axis, dx, interp, method)

    print("\n=== H — N73 HEAVY q=2/3/4 CONTINUOUS FORCE ===", flush=True)
    cubic = c2aqs.run_method(
        "cubic", interps["cubic"], far_lowers, near_lowers, offsets,
        center, direction, payload_radius, use_q4=True,
    )
    quintic = c2aqs.run_method(
        "quintic", interps["quintic"], far_lowers, near_lowers, offsets,
        center, direction, payload_radius, use_q4=True,
    )

    spread = abs(cubic.best.force - quintic.best.force)
    error_bound = max(cubic.internal_error, quintic.internal_error, spread)
    margin = min(abs(cubic.best.force), abs(quintic.best.force))
    same_sign = bool(np.sign(cubic.best.force) == np.sign(quintic.best.force) and cubic.best.force != 0.0)
    certified = bool(same_sign and margin > c2aqs.SIGN_SAFETY_FACTOR * error_bound)
    sign = "OUTWARD" if (certified and cubic.best.force > 0.0) else (
        "INWARD" if (certified and cubic.best.force < 0.0) else "UNRESOLVED"
    )
    l1 = max(cubic.best.l1, quintic.best.l1)
    avgmag = 0.5 * (abs(cubic.best.force) + abs(quintic.best.force))
    cancellation = l1 / max(avgmag, 1e-300)

    n65mean = 0.5 * (n65ref["cubic"] + n65ref["quintic"])
    n73mean = 0.5 * (cubic.best.force + quintic.best.force)
    mean_relchange = abs(n73mean - n65mean) / max(abs(n65mean), abs(n73mean), 1e-12)
    spread_ratio = spread / max(n65ref["spread"], 1e-300)

    print("\n=== I — N73 CONTINUOUS FORCE CERTIFICATE ===", flush=True)
    print(f"N65_REFERENCE_CUBIC_FORCE={n65ref['cubic']:.15e}", flush=True)
    print(f"N65_REFERENCE_QUINTIC_FORCE={n65ref['quintic']:.15e}", flush=True)
    print(f"N65_REFERENCE_REPRESENTATION_SPREAD={n65ref['spread']:.15e}", flush=True)
    print(f"N73_CUBIC_CONTINUOUS_BEST_FORCE={cubic.best.force:.15e}", flush=True)
    print(f"N73_QUINTIC_CONTINUOUS_BEST_FORCE={quintic.best.force:.15e}", flush=True)
    print(f"N73_CONTINUOUS_REPRESENTATION_SPREAD={spread:.15e}", flush=True)
    print(f"N73_CONTINUOUS_FORCE_ERROR_BOUND={error_bound:.15e}", flush=True)
    print(f"N73_CONTINUOUS_FORCE_SIGN_MARGIN={margin:.15e}", flush=True)
    print(f"N73_CONTINUOUS_FORCE_SIGN_SAFETY_FACTOR={c2aqs.SIGN_SAFETY_FACTOR:.8f}", flush=True)
    print("N73_CUBIC_QUINTIC_SAME_SIGN=" + ("YES" if same_sign else "NO"), flush=True)
    print("N73_CONTINUOUS_FORCE_SIGN_CERTIFIED=" + ("YES" if certified else "NO"), flush=True)
    print(f"N73_CONTINUOUS_FORCE_SIGN={sign}", flush=True)
    print(f"N73_CONTINUOUS_FORCE_CANCELLATION_FACTOR={cancellation:.15e}", flush=True)
    print(f"N65_N73_CONTINUOUS_FORCE_MEAN_RELCHANGE={mean_relchange:.15e}", flush=True)
    print(f"N65_TO_N73_REPRESENTATION_SPREAD_RATIO={spread_ratio:.15e}", flush=True)
    print("N65_TO_N73_REPRESENTATION_UNCERTAINTY_SHRANK=" + ("YES" if spread_ratio < 1.0 else "NO"), flush=True)

    return {
        "cubic": cubic.best.force,
        "quintic": quintic.best.force,
        "spread": spread,
        "error": error_bound,
        "certified": certified,
        "sign": sign,
        "mean_relchange": mean_relchange,
        "spread_ratio": spread_ratio,
    }


def main() -> None:
    """Execute N=73 actual-field resolution and conditional force certificate."""
    print("=== 023C2AQS2 — N73 STATIONARITY + CONTINUOUS FORCE RESOLUTION ===", flush=True)

    print("\n=== A — FAIL-CLOSED UPSTREAM AUDIT ===", flush=True)
    for path, expected in (
        (C2AR_SOURCE, EXPECTED_C2AR_SHA256),
        (C2AQS_SOURCE, EXPECTED_C2AQS_SHA256),
    ):
        require(path)
        actual = sha256(path)
        print(f"{path.name}_SHA256={actual}", flush=True)
        if actual != expected:
            raise RuntimeError(f"Upstream source hash mismatch: {path.name}")
    print("UPSTREAM_023C2AR_023C2AQS_AUDIT=PASS", flush=True)

    c2ar = load_module("c2aqs2_c2ar", C2AR_SOURCE)
    c2aqs = load_module("c2aqs2_c2aqs", C2AQS_SOURCE)
    cr2 = c2ar.load_module("c2aqs2_cr2", c2ar.CR2_SOURCE)
    cr3 = c2ar.load_module("c2aqs2_cr3", c2ar.CR3_SOURCE)
    cr4r = c2ar.load_module("c2aqs2_cr4r", c2ar.CR4R_SOURCE)

    print("\n=== B — LOAD ACTUAL N73 FIELD + CURVATURE HISTORY ===", flush=True)
    state, history, source, discarded, norm_err = load_state(cr3, cr4r)
    E0, _a, _b, _c, _g0, rms0, gmax0, station0 = strict_stationarity(cr3, state.phi, state.dx)
    deg_ok0, degrees0 = cr3.geometric_guard(state.phi, cr2, True)
    print(f"N73_FINE_START_SOURCE={source.relative_to(ROOT)}", flush=True)
    print(f"N73_FINE_START_ACCEPTED_TOTAL={state.accepted_total}", flush=True)
    print(f"N73_FINE_START_HISTORY_LENGTH={len(history)}", flush=True)
    print(f"N73_FINE_START_HISTORY_DISCARDED={discarded}", flush=True)
    print(f"N73_FINE_START_NORM_MAXERR={norm_err:.15e}", flush=True)
    print(f"N73_FINE_START_ENERGY={E0:.15e}", flush=True)
    print(f"N73_FINE_START_GRAD_RMS={rms0:.15e}", flush=True)
    print(f"N73_FINE_START_GRAD_MAX={gmax0:.15e}", flush=True)
    print("N73_FINE_START_STRICT_STATIONARITY=" + ("PASS" if station0 else "FAIL"), flush=True)
    print(f"N73_FINE_START_TOPOLOGY4={cr3.topology4(state.phi, state.dx):.15e}", flush=True)
    print("N73_FINE_START_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in degrees0), flush=True)
    if not deg_ok0:
        raise RuntimeError("Starting N73 field failed geometric B=7 guard")

    print("\n=== C — STABILIZED PERSISTENT R-LBFGS ===", flush=True)
    state, history, E, g, rms, gmax, station, stats = stabilized_rlbfgs(cr2, cr3, cr4r, state, history)

    print("\n=== D — END-OF-STATIONARITY-SLICE AUDIT ===", flush=True)
    deg_ok, degrees = cr3.geometric_guard(state.phi, cr2, True)
    t4 = cr3.topology4(state.phi, state.dx)
    angle = cr3.max_neighbor_angle(state.phi)
    print(f"N73_FINE_FINAL_ACCEPTED_THIS_RUN={stats['accepted_this']}", flush=True)
    print(f"N73_FINE_FINAL_ACCEPTED_TOTAL={state.accepted_total}", flush=True)
    print(f"N73_FINE_FINAL_HISTORY_LENGTH={len(history)}", flush=True)
    print(f"N73_FINE_REJECTED_ENERGY_TRIALS={stats['rejected_energy']}", flush=True)
    print(f"N73_FINE_REJECTED_GRADIENT_GROWTH_TRIALS={stats['rejected_gradient']}", flush=True)
    print(f"N73_FINE_REJECTED_TOPOLOGY_TRIALS={stats['rejected_topology']}", flush=True)
    print(f"N73_FINE_REJECTED_SMOOTHNESS_TRIALS={stats['rejected_smoothness']}", flush=True)
    print(f"N73_FINE_HISTORY_RESETS={stats['history_resets']}", flush=True)
    print(f"N73_FINE_SECANT_REJECTS={stats['secant_rejects']}", flush=True)
    print(f"N73_FINE_FALLBACK_STEPS={stats['fallback_steps']}", flush=True)
    print(f"N73_FINE_FINAL_ENERGY={E:.15e}", flush=True)
    print(f"N73_FINE_FINAL_GRAD_RMS={rms:.15e}", flush=True)
    print(f"N73_FINE_FINAL_GRAD_MAX={gmax:.15e}", flush=True)
    print("N73_FINE_FINAL_STRICT_STATIONARITY=" + ("PASS" if station else "FAIL"), flush=True)
    print(f"N73_FINE_FINAL_TOPOLOGY4={t4:.15e}", flush=True)
    print("N73_FINE_FINAL_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in degrees), flush=True)
    print(f"N73_FINE_FINAL_MAX_NEIGHBOR_ANGLE={angle:.15e}", flush=True)

    if not station:
        print("\n=== E — BOUNDED INCOMPLETE DECISION ===", flush=True)
        print("023C2AQS2_N73_STATIONARITY_AND_CONTINUOUS_FORCE=INCOMPLETE_CONTINUE_N73_CHECKPOINT", flush=True)
        print("N73_ACTUAL_FINE_STRICT_STATIONARITY=NOT_YET", flush=True)
        print("N73_CONTINUOUS_FORCE=NOT_RUN_BEFORE_STATIONARITY", flush=True)
        print("FULL_PHYSICAL_HESSIAN=DEFERRED_OPERATIONAL_FORCE_AND_FINE_FIELD_UNRESOLVED", flush=True)
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR_NOT_A_PROBABILITY", flush=True)
        print("NEXT=RERUN_SAME_023C2AQS2_FROM_PERSISTENT_HISTORY", flush=True)
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED", flush=True)
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
        return

    print("\n=== E — STRICT N73 PHYSICAL FIELD AUDIT ===", flush=True)
    diag = cr3.continuum_local_diagnostics(state.phi, state.axis, state.dx, cr2)
    print(f"N73_STATIONARY_CONTINUUM_ENERGY={diag.energy_continuum:.15e}", flush=True)
    print(f"N73_STATIONARY_ACTIVE_TOTAL={diag.active_total:.15e}", flush=True)
    print(f"N73_STATIONARY_ACTIVE_TO_ENERGY={diag.active_to_energy:.15e}", flush=True)
    print(f"N73_STATIONARY_MIN_ACTIVE_FRACTION={diag.min_active_fraction:.15e}", flush=True)
    print(f"N73_STATIONARY_TOPOLOGY4={diag.topology4:.15e}", flush=True)
    print("N73_STATIONARY_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in diag.geometric_degrees), flush=True)
    print(f"N73_STATIONARY_MIN_DEC_SCALED_MARGIN={diag.min_dec_scaled_margin:.15e}", flush=True)
    print(f"N73_STATIONARY_MAX_ACTIVE_TRACE_SCALED={diag.max_active_trace_scaled:.15e}", flush=True)
    print(f"N73_STATIONARY_ENERGY_CENTROID_NORM={diag.energy_centroid_norm:.15e}", flush=True)
    physical_gate = bool(
        deg_ok
        and diag.active_total > 0.0
        and diag.min_active_fraction <= -1.0e-2
        and diag.min_dec_scaled_margin >= -1.0e-9
        and diag.max_active_trace_scaled <= 1.0e-10
        and angle <= MAX_NEIGHBOR_ANGLE
    )
    print("N73_STATIONARY_PHYSICAL_FIELD_GATE=" + ("PASS" if physical_gate else "FAIL"), flush=True)
    save_final(state, E, rms, gmax, diag)

    if not physical_gate:
        print("023C2AQS2_N73_STATIONARITY_AND_CONTINUOUS_FORCE=RED_N73_STATIONARY_FIELD_PHYSICAL_GATE", flush=True)
        print("FULL_PHYSICAL_HESSIAN=DEFERRED_BY_FINE_FIELD_PHYSICAL_FALSIFIER", flush=True)
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_PENDING_RERANK", flush=True)
        print("NEXT=PRESERVE_NEGATIVE_RESULT_AND_RERANK_023_BRANCH", flush=True)
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED", flush=True)
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
        return

    print("\n=== F0 — LOAD N65 CONTINUOUS-FORCE REFERENCE ===", flush=True)
    n65ref = load_n65_force_reference()
    print(f"N65_REFERENCE_CUBIC_FORCE={n65ref['cubic']:.15e}", flush=True)
    print(f"N65_REFERENCE_QUINTIC_FORCE={n65ref['quintic']:.15e}", flush=True)
    print(f"N65_REFERENCE_REPRESENTATION_SPREAD={n65ref['spread']:.15e}", flush=True)
    print(f"N65_REFERENCE_ERROR_BOUND={n65ref['error']:.15e}", flush=True)

    # Re-run the upstream analytic kernel validation, then use the continuous
    # operator on the actual strict N=73 field.
    aqr = c2aqs.load_module("c2aqs2_aqr", c2aqs.AQR_SOURCE)
    aqr.validate_analytic_formulae()
    print("N73_UPSTREAM_ANALYTIC_KERNEL_VALIDATION=PASS", flush=True)
    force = continuous_force_gate(c2aqs, aqr, cr3, state.phi, state.axis, state.dx, n65ref)

    print("\n=== J — 023C2AQS2 DECISION ===", flush=True)
    if force["certified"] and force["sign"] == "OUTWARD":
        decision = "GREEN_N73_STRICT_STATIONARY_CONTINUOUS_OUTWARD_SENTINEL"
        if force["spread_ratio"] < 1.0:
            next_step = "023C2AQS3_N81_STATIONARY_COMPANION_AND_CONTINUOUS_FORCE_RESOLUTION_THEN_320_DIRECTION_GATE"
        else:
            next_step = "023C2AQS3_N81_STATIONARY_COMPANION_REQUIRED_REPRESENTATION_SPREAD_NOT_SHRINKING"
        hessian = "DEFERRED_UNTIL_N73_N81_OPERATIONAL_FORCE_CONVERGENCE"
    elif force["certified"] and force["sign"] == "INWARD":
        decision = "RED_N73_STRICT_STATIONARY_CONTINUOUS_SENTINEL_INWARD"
        next_step = "023C2AQS3_N81_CONFIRMATION_OR_BOUNDED_PAYLOAD_OPERATING_VOLUME_RERANK"
        hessian = "DEFERRED_BY_FINE_FIELD_OPERATIONAL_FORCE_FALSIFIER"
    else:
        decision = "INCOMPLETE_N73_CONTINUOUS_FORCE_SIGN_NOT_CERTIFIED"
        next_step = "023C2AQS3_N81_ACTUAL_FIELD_RESOLUTION_FROM_STRICT_N73"
        hessian = "DEFERRED_OPERATIONAL_FORCE_CONTINUUM_NOT_RESOLVED"

    print(f"023C2AQS2_N73_STATIONARITY_AND_CONTINUOUS_FORCE={decision}", flush=True)
    print("N73_ACTUAL_FINE_STRICT_STATIONARITY=PASS", flush=True)
    print(f"FULL_PHYSICAL_HESSIAN={hessian}", flush=True)
    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR_NOT_A_PROBABILITY", flush=True)
    print(f"NEXT={next_step}", flush=True)
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED_UNTIL_023C_COMPLETE", flush=True)
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
    print("NEW_PHYSICS_DISCOVERY=NO", flush=True)
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023C2AQS2_ACTUAL_N73_FIELD_RESOLUTION", flush=True)


if __name__ == "__main__":
    main()
