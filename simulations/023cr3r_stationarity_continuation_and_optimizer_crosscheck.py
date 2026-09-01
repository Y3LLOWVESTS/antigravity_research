#!/usr/bin/env python3
"""023CR3R — stationarity continuation and optimizer cross-check.

PURPOSE
-------
Resolve the first failed gate from 023CR3: unrestricted Cartesian stationarity
of the promotion-grade false-core B=7 Skyrmion candidate.

SCIENTIFIC QUESTION
-------------------
023CR3 showed that the checkerboard-free, geometric-degree-preserving B=7
field can move substantially in unrestricted SU(2) field space while retaining
its topology, pointwise DEC, negative enclosed active mass, and (at N=65)
outward finite-payload gravity over all 320 tested orientations.  However, the
relaxation stopped after 180 accepted nonlinear-conjugate-gradient steps with a
non-negligible residual gradient.  Therefore the field was not yet stationary
and no full physical Hessian was scientifically authorized.

This run asks:

    Does the same topological B=7 field converge to a numerically trustworthy
    unrestricted stationary point when the relaxation is continued and checked
    with a second optimization strategy?

The run deliberately does NOT compute a Hessian unless stationarity has first
been established.  It is a continuation/optimizer gate, not a stability gate.

UPSTREAM RESULT
---------------
023CR3 retained, at N=65, approximately:

    geometric degree              = (-7,-7,-7)
    derivative topology           = 6.96977
    negative active fraction      = -1.603 percent
    positive total active mass    = yes
    pointwise DEC                 = pass
    active-trace identity         = pass
    320-direction payload minimum = positive

but reported:

    RELAX_CONVERGED = NO

with the gradient tolerance as the first failed physical gate.

MODEL AND ACTION
----------------
The field is the unit four-vector

    phi = (sigma, pi_1, pi_2, pi_3),
    phi . phi = 1,

with continuum energy

    E = integral (e2 + e4 + V) d^3x,

    e2 = sum_i |d_i phi|^2,

    e4 = sum_(i<j) [
        |d_i phi|^2 |d_j phi|^2
        - (d_i phi . d_j phi)^2
    ],

    V = m^2 (1-sigma)(1+eta sigma).

The discrete action and exact discrete gradient are imported byte-for-byte from
023CR3.  They use the fourth-order forward/backward averaged one-sided action
that 023CR2 proved has no checkerboard/Nyquist null mode.

OPTIMIZATION STRATEGY
---------------------
The run uses two stages on the SAME action:

1. Restarted Riemannian nonlinear conjugate gradient (NCG), reusing the audited
   023CR3 implementation but allowing substantially more accepted steps.
2. If needed, an independent Riemannian Barzilai-Borwein (BB) steepest-descent
   continuation with monotone Armijo backtracking.

The BB stage is intentionally simpler than NCG.  Agreement between the two
methods strengthens the stationarity diagnosis and avoids mistaking optimizer
exhaustion for a physical obstruction.

TOPOLOGY / SMOOTHNESS GUARDS
----------------------------
The outer vacuum boundary is fixed.  Every candidate update must satisfy:

- the fourth-order derivative topology remains close to |B|=7;
- nearest-neighbor field angles remain below the established smoothness bound;
- exact geometric preimage degree is periodically checked and must remain
  |degree|=7;
- the final field is checked against all three independent geometric targets.

These are numerical admissibility conditions, not added physical stabilizers.
Continuum degree cannot change under a smooth deformation with fixed vacuum
boundary conditions.

RESOLUTION STRATEGY
-------------------
The saved N=65 field from 023CR3 is continued first.  This is the cheapest
high-information test because it already retained all non-stationarity physical
gates including dense payload repulsion.

Only if N=65 becomes stationary and remains physically admissible is a finer
N=73 companion field constructed by smooth interpolation into the same basin,
re-audited for B=7, and independently relaxed.  This avoids spending a large
second-grid calculation if the primary field cannot converge.

OPERATIONAL OBSERVABLE
----------------------
After stationarity, reconstruct the continuum stress tensor and

    S = rho + p_1 + p_2 + p_3 = 2(e4 - V)

using the audited fourth-order diagnostics.  Test a uniform spherical payload
on the deterministic 320-direction Fibonacci sphere using the exact
sphere-averaged Newton kernel.

PROMOTION CONDITION
-------------------
This gate is GREEN_UNRESTRICTED_STATIONARY_FIELD only if:

- N=65 reaches the original strict gradient tolerances;
- its exact geometric degree remains |B|=7;
- positive total active mass survives;
- negative enclosed active mass remains at least 1 percent in magnitude;
- pointwise DEC and the active-trace identity pass;
- all 320 finite-payload directions remain outward;
- the N=73 companion also reaches stationarity in the same topological sector;
- N=65/N=73 relaxed physical observables converge at declared tolerances.

A green result authorizes the corrected full physical Hessian gate.  It does
NOT itself prove dynamical stability.

FALSIFIER / STOP RULE
---------------------
If a numerically smooth, topologically valid stationary field is reached at
both resolutions but positive total active mass or dense finite-payload
repulsion is lost robustly, preserve that as a physical negative result for
this selected candidate.

If stationarity is not reached, topology is lost, or the two resolutions do
not converge, classify the result as incomplete numerical/stationarity work.
Do not proceed to a Hessian or Einstein-Skyrme continuation.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023CR3R_STATIONARITY_CONTINUATION_AND_OPTIMIZER_CROSSCHECK

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

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CR3_SOURCE = ROOT / "simulations/023cr3_geometric_degree_guarded_unrestricted_relaxation.py"
CR3_LOG = ROOT / "results/logs/023cr3_geometric_degree_guarded_unrestricted_relaxation.log"
CR3_ARTIFACT = ROOT / "results/data/023cr3_unrestricted_relaxed_b7_n65.npz"
CR2_SOURCE = ROOT / "simulations/023cr2_high_order_geometric_topology_preflight.py"

EXPECTED_CR3_SHA256 = "350868726af644d1a8bb2970b559c92e1febc4ea261f409ab38c1dca64ac97da"
EXPECTED_CR2_SHA256 = "6affc28547b7849140f1eacf6992c9541ea9ba9a7c306e69121ca60ef76ad1db"

B = 7
ETA = 0.40
MASS = 8.0
PRIMARY_N = 65
COMPANION_N = 73
DENSE_ORIENTATION_N = 320

# Preserve the strict stationarity tolerances from 023CR3.
GRAD_RMS_TOL = 1.5e-3
GRAD_MAX_TOL = 5.0e-2
MAX_NEIGHBOR_ANGLE = 0.70
MAX_TOPOLOGY_RELERR = 3.0e-2
MIN_NEGATIVE_ACTIVE_FRACTION = 1.0e-2
MIN_DEC_SCALED_MARGIN = -2.0e-8
MAX_ACTIVE_TRACE_SCALED = 2.0e-12

# Continuation controls.  Stage 1 reuses the audited NCG implementation.
NCG_MAX_ITER = 420
NCG_GEOMETRIC_GUARD_EVERY = 20

# Stage 2 is an independent monotone BB steepest-descent continuation.
BB_MAX_ITER = 900
BB_ARMIJO = 1.0e-4
BB_MIN_STEP = 1.0e-10
BB_MAX_STEP = 1.0
BB_MAX_POINT_ROTATION = 0.045
BB_GEOMETRIC_GUARD_EVERY = 20
BB_PROGRESS_EVERY = 100

# Two-resolution stationary-observable convergence requirements.
MAX_PAIR_ENERGY_RELCHANGE = 1.5e-2
MAX_PAIR_ACTIVE_FRACTION_ABSCHANGE = 1.5e-2
MAX_PAIR_PAYLOAD_MIN_RELCHANGE = 2.0e-1
MAX_PAIR_TOPOLOGY_ABSCHANGE = 1.0e-2

PRIMARY_ARTIFACT = ROOT / "results/data/023cr3r_stationary_b7_n65.npz"
COMPANION_ARTIFACT = ROOT / "results/data/023cr3r_stationary_b7_n73.npz"


@dataclass
class BBResult:
    field: np.ndarray
    initial_energy: float
    final_energy: float
    initial_grad_rms: float
    initial_grad_max: float
    final_grad_rms: float
    final_grad_max: float
    accepted_steps: int
    rejected_energy_trials: int
    rejected_topology_trials: int
    rejected_smoothness_trials: int
    converged: bool
    line_search_failed: bool
    final_topology4: float
    final_geometric_degrees: tuple[int, ...]
    final_max_neighbor_angle: float


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_file(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def relative_error(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0e-300)


def strict_stationarity(cr3, field: np.ndarray, dx: float) -> tuple[float, float, bool]:
    _, _, _, _, g = cr3.riemannian_gradient_density(field, dx)
    rms, gmax = cr3.gradient_norms(g)
    return rms, gmax, bool(rms <= GRAD_RMS_TOL and gmax <= GRAD_MAX_TOL)


def physical_gate(cr3, diag, payload) -> tuple[bool, dict[str, bool]]:
    checks = {
        "GEOMETRIC_B7": (
            all(abs(int(d)) == B for d in diag.geometric_degrees)
            and len(set(np.sign(int(d)) for d in diag.geometric_degrees)) == 1
        ),
        "DERIVATIVE_TOPOLOGY": diag.topology4_relerr <= MAX_TOPOLOGY_RELERR,
        "LATTICE_SMOOTHNESS": diag.max_neighbor_angle <= MAX_NEIGHBOR_ANGLE,
        "POSITIVE_TOTAL_ACTIVE_MASS": diag.active_total > 0.0,
        "NEGATIVE_ENCLOSED_ACTIVE_MASS": diag.min_active_fraction <= -MIN_NEGATIVE_ACTIVE_FRACTION,
        "POINTWISE_DEC": diag.min_dec_scaled_margin >= MIN_DEC_SCALED_MARGIN,
        "ACTIVE_TRACE_IDENTITY": diag.max_active_trace_scaled <= MAX_ACTIVE_TRACE_SCALED,
        "DENSE_FINITE_PAYLOAD_OUTWARD": payload.all_outward,
    }
    return all(checks.values()), checks


def periodic_geometric_guard(cr3, cr2, field: np.ndarray, accepted_next: int) -> bool:
    if accepted_next % BB_GEOMETRIC_GUARD_EVERY != 0:
        return True
    full = accepted_next % (4 * BB_GEOMETRIC_GUARD_EVERY) == 0
    ok, _ = cr3.geometric_guard(field, cr2, full)
    return bool(ok)


def bb_relax(cr3, cr2, phi0: np.ndarray, dx: float) -> BBResult:
    """Monotone Riemannian Barzilai-Borwein steepest descent.

    The discrete action and exact gradient are imported from 023CR3.  BB only
    chooses a scalar step length; every physical update remains an exponential
    map along the negative Riemannian gradient.
    """
    phi = np.array(phi0, dtype=float, copy=True)
    cr3.enforce_vacuum_boundary(phi)
    phi = cr3.normalize_field(phi)

    E, _, _, _, g = cr3.riemannian_gradient_density(phi, dx)
    initial_E = float(E)
    initial_rms, initial_gmax = cr3.gradient_norms(g)
    step_guess = min(0.02, BB_MAX_POINT_ROTATION / max(initial_gmax, 1.0e-300))

    accepted = 0
    rej_energy = 0
    rej_topology = 0
    rej_smooth = 0
    line_fail = False

    prev_step = None
    prev_g_at_new = None

    for iteration in range(1, BB_MAX_ITER + 1):
        rms, gmax = cr3.gradient_norms(g)
        if rms <= GRAD_RMS_TOL and gmax <= GRAD_MAX_TOL:
            break

        direction = -g
        gg = cr3.tangent_inner(g, g, dx)
        max_dir = float(np.max(np.linalg.norm(direction[1:-1, 1:-1, 1:-1], axis=-1)))
        alpha = min(
            max(step_guess, BB_MIN_STEP),
            BB_MAX_POINT_ROTATION / max(max_dir, 1.0e-300),
            BB_MAX_STEP,
        )

        trial = None
        Etrial = math.inf
        for _ in range(28):
            if alpha < BB_MIN_STEP:
                break
            candidate = cr3.exp_map_update(phi, direction, alpha)
            Etrial = cr3.high_order_energy_gradient(candidate, dx, False)[0]
            if not math.isfinite(Etrial) or Etrial > E - BB_ARMIJO * alpha * gg:
                rej_energy += 1
                alpha *= 0.5
                continue

            angle = cr3.max_neighbor_angle(candidate)
            if angle > MAX_NEIGHBOR_ANGLE:
                rej_smooth += 1
                alpha *= 0.5
                continue

            t4 = cr3.topology4(candidate, dx)
            if abs(abs(t4) / B - 1.0) > MAX_TOPOLOGY_RELERR:
                rej_topology += 1
                alpha *= 0.5
                continue

            if not periodic_geometric_guard(cr3, cr2, candidate, accepted + 1):
                rej_topology += 1
                alpha *= 0.5
                continue

            trial = candidate
            break

        if trial is None:
            line_fail = True
            break

        old_phi = phi
        old_g = g
        old_direction = direction
        phi = trial
        E, _, _, _, g = cr3.riemannian_gradient_density(phi, dx)
        accepted += 1

        # Approximate the accepted manifold displacement in the new tangent
        # space and transport the old gradient by orthogonal projection.
        s = cr3.project_tangent(phi, alpha * old_direction)
        old_g_transport = cr3.project_tangent(phi, old_g)
        y = g - old_g_transport
        ss = cr3.tangent_inner(s, s, dx)
        sy = cr3.tangent_inner(s, y, dx)
        yy = cr3.tangent_inner(y, y, dx)

        # Alternate BB1 and BB2.  Reject nonpositive curvature estimates and
        # fall back to the accepted Armijo step in that case.
        if sy > 1.0e-300 and yy > 1.0e-300:
            if accepted % 2:
                bb = ss / sy
            else:
                bb = sy / yy
            if math.isfinite(bb) and bb > 0.0:
                step_guess = min(max(bb, BB_MIN_STEP), BB_MAX_STEP)
            else:
                step_guess = min(max(alpha * 1.20, BB_MIN_STEP), BB_MAX_STEP)
        else:
            step_guess = min(max(alpha * 1.20, BB_MIN_STEP), BB_MAX_STEP)

        prev_step = s
        prev_g_at_new = g
        _ = old_phi, prev_step, prev_g_at_new  # retained for audit readability

        if accepted % BB_PROGRESS_EVERY == 0:
            prms, pgmax = cr3.gradient_norms(g)
            print(
                f"BB_PROGRESS_ACCEPTED={accepted} "
                f"ENERGY={E:.15e} GRAD_RMS={prms:.15e} "
                f"GRAD_MAX={pgmax:.15e} STEP_GUESS={step_guess:.15e}"
            )

    final_rms, final_gmax = cr3.gradient_norms(g)
    final_t4 = cr3.topology4(phi, dx)
    final_angle = cr3.max_neighbor_angle(phi)
    gok, degrees = cr3.geometric_guard(phi, cr2, True)
    converged = bool(
        final_rms <= GRAD_RMS_TOL
        and final_gmax <= GRAD_MAX_TOL
        and gok
        and abs(abs(final_t4) / B - 1.0) <= MAX_TOPOLOGY_RELERR
        and final_angle <= MAX_NEIGHBOR_ANGLE
    )

    return BBResult(
        field=phi,
        initial_energy=initial_E,
        final_energy=float(E),
        initial_grad_rms=initial_rms,
        initial_grad_max=initial_gmax,
        final_grad_rms=final_rms,
        final_grad_max=final_gmax,
        accepted_steps=accepted,
        rejected_energy_trials=rej_energy,
        rejected_topology_trials=rej_topology,
        rejected_smoothness_trials=rej_smooth,
        converged=converged,
        line_search_failed=line_fail,
        final_topology4=final_t4,
        final_geometric_degrees=tuple(int(x) for x in degrees),
        final_max_neighbor_angle=final_angle,
    )


def print_bb(prefix: str, r: BBResult) -> None:
    print(f"{prefix}_BB_INITIAL_ENERGY={r.initial_energy:.15e}")
    print(f"{prefix}_BB_FINAL_ENERGY={r.final_energy:.15e}")
    print(f"{prefix}_BB_ENERGY_DROP_FRACTION={(r.initial_energy-r.final_energy)/max(r.initial_energy,1e-300):.15e}")
    print(f"{prefix}_BB_INITIAL_GRAD_RMS={r.initial_grad_rms:.15e}")
    print(f"{prefix}_BB_INITIAL_GRAD_MAX={r.initial_grad_max:.15e}")
    print(f"{prefix}_BB_FINAL_GRAD_RMS={r.final_grad_rms:.15e}")
    print(f"{prefix}_BB_FINAL_GRAD_MAX={r.final_grad_max:.15e}")
    print(f"{prefix}_BB_ACCEPTED_STEPS={r.accepted_steps}")
    print(f"{prefix}_BB_REJECTED_ENERGY_TRIALS={r.rejected_energy_trials}")
    print(f"{prefix}_BB_REJECTED_TOPOLOGY_TRIALS={r.rejected_topology_trials}")
    print(f"{prefix}_BB_REJECTED_SMOOTHNESS_TRIALS={r.rejected_smoothness_trials}")
    print(f"{prefix}_BB_LINE_SEARCH_FAILED=" + ("YES" if r.line_search_failed else "NO"))
    print(f"{prefix}_BB_CONVERGED=" + ("YES" if r.converged else "NO"))
    print(f"{prefix}_BB_FINAL_TOPOLOGY4={r.final_topology4:.15e}")
    print(f"{prefix}_BB_FINAL_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in r.final_geometric_degrees))
    print(f"{prefix}_BB_FINAL_MAX_NEIGHBOR_ANGLE={r.final_max_neighbor_angle:.15e}")


def save_artifact(path: Path, field: np.ndarray, axis: np.ndarray, dx: float, diag, payload, source: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        phi=field,
        axis=axis,
        dx=np.array(dx),
        B=np.array(B),
        eta=np.array(ETA),
        mass=np.array(MASS),
        source=np.array(source),
        continuum_energy=np.array(diag.energy_continuum),
        active_total=np.array(diag.active_total),
        min_active_fraction=np.array(diag.min_active_fraction),
        topology4=np.array(diag.topology4),
        geometric_degrees=np.array(diag.geometric_degrees, dtype=int),
        payload_min_radial=np.array(payload.min_radial),
    )


def interpolate_field(phi: np.ndarray, axis_old: np.ndarray, n_new: int, cr3) -> tuple[np.ndarray, np.ndarray, float]:
    from scipy.interpolate import RegularGridInterpolator

    axis_new = np.linspace(float(axis_old[0]), float(axis_old[-1]), n_new)
    X, Y, Z = np.meshgrid(axis_new, axis_new, axis_new, indexing="ij")
    points = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    out = np.empty((n_new, n_new, n_new, 4), dtype=float)
    for a in range(4):
        interp = RegularGridInterpolator(
            (axis_old, axis_old, axis_old),
            phi[..., a],
            method="linear",
            bounds_error=True,
        )
        out[..., a] = interp(points).reshape((n_new, n_new, n_new))
    out = cr3.normalize_field(out)
    cr3.enforce_vacuum_boundary(out)
    out = cr3.normalize_field(out)
    dx = float(axis_new[1] - axis_new[0])
    return out, axis_new, dx


def run_continuation(label: str, cr3, cr2, phi0: np.ndarray, axis: np.ndarray, dx: float):
    print(f"\n=== {label} — RESTARTED NCG CONTINUATION ===")

    # Temporarily extend only the iteration budget / exact-geometric audit
    # cadence.  Physical action, gradient, tolerances, and guards are unchanged.
    old_max_iter = cr3.RELAX_MAX_ITER
    old_guard_every = cr3.GEOMETRIC_GUARD_EVERY
    old_rotation = cr3.RELAX_MAX_POINT_ROTATION
    try:
        cr3.RELAX_MAX_ITER = NCG_MAX_ITER
        cr3.GEOMETRIC_GUARD_EVERY = NCG_GEOMETRIC_GUARD_EVERY
        cr3.RELAX_MAX_POINT_ROTATION = 0.050
        ncg = cr3.relax_field(phi0, dx, cr2)
    finally:
        cr3.RELAX_MAX_ITER = old_max_iter
        cr3.GEOMETRIC_GUARD_EVERY = old_guard_every
        cr3.RELAX_MAX_POINT_ROTATION = old_rotation

    cr3.print_relax(label + "_NCG", ncg)
    rms, gmax, station = strict_stationarity(cr3, ncg.field, dx)
    print(f"{label}_NCG_STRICT_GRAD_RMS={rms:.15e}")
    print(f"{label}_NCG_STRICT_GRAD_MAX={gmax:.15e}")
    print(f"{label}_NCG_STRICT_STATIONARITY=" + ("PASS" if station else "FAIL"))

    if station and ncg.converged:
        final_field = ncg.field
        method = "RESTARTED_NCG"
        bb = None
    else:
        print(f"\n=== {label} — INDEPENDENT BB CONTINUATION ===")
        bb = bb_relax(cr3, cr2, ncg.field, dx)
        print_bb(label, bb)
        final_field = bb.field
        method = "RESTARTED_NCG_PLUS_BB"

    final_rms, final_gmax, final_station = strict_stationarity(cr3, final_field, dx)
    diag = cr3.continuum_local_diagnostics(final_field, axis, dx, cr2)
    payload = cr3.payload_diagnostics(final_field, axis, dx, float(payload_center), float(payload_radius))
    physical_ok, checks = physical_gate(cr3, diag, payload)

    print(f"\n=== {label} — FINAL STATIONARY/PHYSICAL AUDIT ===")
    print(f"{label}_FINAL_METHOD={method}")
    print(f"{label}_FINAL_GRAD_RMS={final_rms:.15e}")
    print(f"{label}_FINAL_GRAD_MAX={final_gmax:.15e}")
    print(f"{label}_FINAL_STRICT_STATIONARITY=" + ("PASS" if final_station else "FAIL"))
    cr3.print_physical(label + "_FINAL", diag)
    cr3.print_payload(label + "_FINAL", payload)
    for key, ok in checks.items():
        print(f"{label}_{key}=" + ("PASS" if ok else "FAIL"))
    print(f"{label}_PHYSICAL_GATE=" + ("PASS" if physical_ok else "FAIL"))

    return final_field, diag, payload, final_station, physical_ok


def main() -> None:
    print("=== 023CR3R — STATIONARITY CONTINUATION + OPTIMIZER CROSS-CHECK ===")

    print("\n=== A — UPSTREAM 023CR3 AUDIT ===")
    for path in (CR3_SOURCE, CR3_LOG, CR3_ARTIFACT, CR2_SOURCE):
        require_file(path)
    h_cr3 = sha256(CR3_SOURCE)
    h_cr2 = sha256(CR2_SOURCE)
    print(f"023CR3_SOURCE_SHA256={h_cr3}")
    print(f"023CR2_SOURCE_SHA256={h_cr2}")
    log_text = CR3_LOG.read_text(errors="replace")
    markers = (
        "N65_RELAX_FINAL_GEOMETRIC_DEGREES=-7,-7,-7",
        "N65_POSITIVE_TOTAL_ACTIVE_MASS=PASS",
        "N65_NEGATIVE_ENCLOSED_ACTIVE_MASS=PASS",
        "N65_DENSE_FINITE_PAYLOAD_OUTWARD=PASS",
        "N65_UNRESTRICTED_STATIONARITY=FAIL",
        "023CR3_GEOMETRIC_DEGREE_GUARDED_UNRESTRICTED_RELAXATION=INCOMPLETE_NUMERICAL_OR_STATIONARITY_GATE",
    )
    upstream_ok = (
        h_cr3 == EXPECTED_CR3_SHA256
        and h_cr2 == EXPECTED_CR2_SHA256
        and all(marker in log_text for marker in markers)
    )
    print("UPSTREAM_023CR3_AUDIT=" + ("PASS" if upstream_ok else "FAIL"))
    if not upstream_ok:
        raise RuntimeError("023CR3 audit failed")

    cr3 = load_module("cr3_for_023cr3r", CR3_SOURCE)
    cr2 = load_module("cr2_for_023cr3r", CR2_SOURCE)

    print("\n=== B — DISCRETE GRADIENT RECHECK ===")
    grad_rel, grad_ok = cr3.gradient_selfcheck()
    print(f"HIGH_ORDER_ACTION_GRADIENT_DIRECTIONAL_RELERR={grad_rel:.15e}")
    print("HIGH_ORDER_ACTION_GRADIENT_SELFCHECK=" + ("PASS" if grad_ok else "FAIL"))
    if not grad_ok:
        raise RuntimeError("High-order action gradient selfcheck failed")

    print("\n=== C — LOAD SAVED N=65 FIELD ===")
    data = np.load(CR3_ARTIFACT, allow_pickle=False)
    phi65 = np.array(data["phi"], dtype=float)
    axis65 = np.array(data["axis"], dtype=float)
    dx65 = float(np.asarray(data["dx"]))
    b_art = int(np.asarray(data["B"]))
    eta_art = float(np.asarray(data["eta"]))
    mass_art = float(np.asarray(data["mass"]))
    artifact_ok = (
        phi65.shape[:3] == (PRIMARY_N, PRIMARY_N, PRIMARY_N)
        and b_art == B
        and abs(eta_art - ETA) <= 1.0e-14
        and abs(mass_art - MASS) <= 1.0e-14
    )
    print(f"N65_ARTIFACT_SHAPE={phi65.shape}")
    print(f"N65_ARTIFACT_DX={dx65:.15e}")
    print(f"N65_ARTIFACT_B={b_art}")
    print(f"N65_ARTIFACT_ETA={eta_art:.15e}")
    print(f"N65_ARTIFACT_M={mass_art:.15e}")
    print("N65_ARTIFACT_AUDIT=" + ("PASS" if artifact_ok else "FAIL"))
    if not artifact_ok:
        raise RuntimeError("023CR3 N65 artifact audit failed")

    global payload_center, payload_radius
    # Persisted payload data are not needed in the NPZ; audit the exact values
    # recorded by 023CR3's selected-candidate reconstruction.
    payload_center = 3.870161274564900e-01
    payload_radius = 1.675735743205162e-02

    initial_rms, initial_gmax, initial_station = strict_stationarity(cr3, phi65, dx65)
    initial_diag = cr3.continuum_local_diagnostics(phi65, axis65, dx65, cr2)
    initial_payload = cr3.payload_diagnostics(phi65, axis65, dx65, payload_center, payload_radius)
    print(f"N65_RESUME_INITIAL_GRAD_RMS={initial_rms:.15e}")
    print(f"N65_RESUME_INITIAL_GRAD_MAX={initial_gmax:.15e}")
    print("N65_RESUME_INITIAL_STATIONARITY=" + ("PASS" if initial_station else "FAIL"))
    print(f"N65_RESUME_INITIAL_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in initial_diag.geometric_degrees))
    print(f"N65_RESUME_INITIAL_MIN_ACTIVE_FRACTION={initial_diag.min_active_fraction:.15e}")
    print(f"N65_RESUME_INITIAL_ACTIVE_TOTAL={initial_diag.active_total:.15e}")
    print(f"N65_RESUME_INITIAL_PAYLOAD_MIN_RADIAL={initial_payload.min_radial:.15e}")

    field65, diag65, pay65, station65, physical65 = run_continuation(
        "N65", cr3, cr2, phi65, axis65, dx65
    )
    save_artifact(PRIMARY_ARTIFACT, field65, axis65, dx65, diag65, pay65, "023CR3R_N65")
    print(f"N65_STATIONARY_FIELD_ARTIFACT={PRIMARY_ARTIFACT.relative_to(ROOT)}")

    if not station65:
        print("\n=== F — 023CR3R DECISION ===")
        print("023CR3R_STATIONARITY_CONTINUATION_AND_OPTIMIZER_CROSSCHECK=INCOMPLETE_PRIMARY_STATIONARITY_GATE")
        print("UNRESTRICTED_CARTESIAN_STATIONARY_B7_FIELD=NOT_YET_ESTABLISHED")
        print("PHYSICAL_FALSIFICATION=NO_PRIMARY_FIELD_NOT_STATIONARY")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
        print("NEXT=INSPECT_RESIDUAL_GRADIENT_LOCALIZATION_OR_USE_NEWTON_KRYLOV_PRECONDITIONER")
        print("FULL_PHYSICAL_HESSIAN=NOT_AUTHORIZED")
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_ESTABLISHED")
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
        return

    if not physical65:
        print("\n=== F — 023CR3R DECISION ===")
        print("023CR3R_STATIONARITY_CONTINUATION_AND_OPTIMIZER_CROSSCHECK=PRIMARY_STATIONARY_PHYSICAL_GATE_FAILED")
        print("UNRESTRICTED_CARTESIAN_STATIONARY_B7_FIELD=SUPPORTED_AT_N65")
        print("NEXT=REPRODUCE_PHYSICAL_LOSS_AT_COMPANION_RESOLUTION_BEFORE_RERANK")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
        print("FULL_PHYSICAL_HESSIAN=NOT_AUTHORIZED")
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_ESTABLISHED")
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
        return

    print("\n=== D — BUILD N=73 COMPANION IN SAME BASIN ===")
    phi73, axis73, dx73 = interpolate_field(field65, axis65, COMPANION_N, cr3)
    deg73 = tuple(int(x) for x in cr2.geometric_degrees(phi73))
    t73 = cr3.topology4(phi73, dx73)
    angle73 = cr3.max_neighbor_angle(phi73)
    interp_ok = (
        all(abs(d) == B for d in deg73)
        and len(set(np.sign(d) for d in deg73)) == 1
        and abs(abs(t73) / B - 1.0) <= MAX_TOPOLOGY_RELERR
        and angle73 <= MAX_NEIGHBOR_ANGLE
    )
    print(f"N73_INTERPOLATED_DX={dx73:.15e}")
    print(f"N73_INTERPOLATED_TOPOLOGY4={t73:.15e}")
    print(f"N73_INTERPOLATED_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in deg73))
    print(f"N73_INTERPOLATED_MAX_NEIGHBOR_ANGLE={angle73:.15e}")
    print("N73_INTERPOLATED_BASIN_AUDIT=" + ("PASS" if interp_ok else "FAIL"))
    if not interp_ok:
        print("023CR3R_STATIONARITY_CONTINUATION_AND_OPTIMIZER_CROSSCHECK=INCOMPLETE_COMPANION_INTERPOLATION_GATE")
        print("NEXT=RECONSTRUCT_N73_FROM_CONTINUUM_AND_RELAX")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
        return

    field73, diag73, pay73, station73, physical73 = run_continuation(
        "N73", cr3, cr2, phi73, axis73, dx73
    )
    save_artifact(COMPANION_ARTIFACT, field73, axis73, dx73, diag73, pay73, "023CR3R_N73")
    print(f"N73_STATIONARY_FIELD_ARTIFACT={COMPANION_ARTIFACT.relative_to(ROOT)}")

    print("\n=== E — N65/N73 STATIONARY CONVERGENCE ===")
    energy_pair = relative_error(diag65.energy_continuum, diag73.energy_continuum)
    active_pair = abs(diag65.min_active_fraction - diag73.min_active_fraction)
    payload_pair = relative_error(pay65.min_radial, pay73.min_radial)
    topo_pair = abs(abs(diag65.topology4) - abs(diag73.topology4)) / B
    pair_ok = (
        energy_pair <= MAX_PAIR_ENERGY_RELCHANGE
        and active_pair <= MAX_PAIR_ACTIVE_FRACTION_ABSCHANGE
        and payload_pair <= MAX_PAIR_PAYLOAD_MIN_RELCHANGE
        and topo_pair <= MAX_PAIR_TOPOLOGY_ABSCHANGE
    )
    print(f"STATIONARY_N65_N73_ENERGY_RELCHANGE={energy_pair:.15e}")
    print(f"STATIONARY_N65_N73_ACTIVE_FRACTION_ABSCHANGE={active_pair:.15e}")
    print(f"STATIONARY_N65_N73_PAYLOAD_MIN_RELCHANGE={payload_pair:.15e}")
    print(f"STATIONARY_N65_N73_TOPOLOGY_ABSCHANGE={topo_pair:.15e}")
    print("STATIONARY_N65_N73_CONVERGENCE=" + ("PASS" if pair_ok else "FAIL"))

    green = station65 and physical65 and station73 and physical73 and pair_ok

    print("\n=== F — 023CR3R DECISION ===")
    if green:
        print("023CR3R_STATIONARITY_CONTINUATION_AND_OPTIMIZER_CROSSCHECK=GREEN_UNRESTRICTED_STATIONARY_FIELD")
        print("UNRESTRICTED_CARTESIAN_STATIONARY_B7_FIELD=SUPPORTED")
        print("FINITE_PAYLOAD_REPULSION_AFTER_UNRESTRICTED_RELAXATION=SUPPORTED")
        print("OPTIMIZER_CROSSCHECK=PASS_RESTARTED_NCG_AND_BB_AVAILABLE")
        print("HEURISTIC_PROMOTION_FROM_023CR3R=NO_WAIT_FOR_FULL_PHYSICAL_HESSIAN")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
        print("NEXT=023C2_CORRECTED_FULL_PHYSICAL_HESSIAN")
        print("FULL_PHYSICAL_HESSIAN=AUTHORIZED_NOT_YET_TESTED")
    else:
        if station65 and station73 and (not physical65) and (not physical73):
            print("023CR3R_STATIONARITY_CONTINUATION_AND_OPTIMIZER_CROSSCHECK=GREEN_NEGATIVE_PHYSICAL_RESULT")
            print("UNRESTRICTED_CARTESIAN_STATIONARY_B7_FIELD=SUPPORTED_BUT_OPERATIONAL_REPULSION_NOT_ROBUST")
            print("NEXT=PRESERVE_NEGATIVE_RESULT_AND_RERANK_FALSE_CORE_CANDIDATES")
        else:
            print("023CR3R_STATIONARITY_CONTINUATION_AND_OPTIMIZER_CROSSCHECK=INCOMPLETE_TWO_RESOLUTION_GATE")
            print("UNRESTRICTED_CARTESIAN_STATIONARY_B7_FIELD=NOT_PROMOTED")
            print("NEXT=INSPECT_FIRST_FAILED_COMPANION_OR_CONVERGENCE_GATE")
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR")
        print("FULL_PHYSICAL_HESSIAN=NOT_AUTHORIZED")

    print("UNRESTRICTED_CARTESIAN_3D_STABILITY=NOT_YET_ESTABLISHED_UNTIL_HESSIAN")
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_ESTABLISHED")
    print("PRACTICAL_ENERGY_SCALING=STILL_CATASTROPHIC_IN_PURE_GR")
    print("REAL_MATERIAL=NO")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023CR3R_STATIONARITY_CONTINUATION_AND_OPTIMIZER_CROSSCHECK")


if __name__ == "__main__":
    main()
