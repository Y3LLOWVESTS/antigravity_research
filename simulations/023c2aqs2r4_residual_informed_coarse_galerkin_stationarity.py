#!/usr/bin/env python3
"""023C2AQS2R4 — residual-informed coarse-Galerkin N=73 stationarity closure.

PURPOSE
-------
Close the remaining smooth low-frequency Euler-Lagrange residual of the
unrestricted N=73 B=7 Skyrmion field after 023C2AQS2R3 reached a regime where
ordinary true-residual MINRES/Newton iterations no longer produced a certified
direction efficiently.

SCIENTIFIC QUESTION
-------------------
Can the remaining N=73 stationarity error be removed by a small, explicitly
validated coarse/low-frequency Newton correction while preserving the SAME
full discrete field equations, B=7 topology, fixed-vacuum boundary, physical
stress-energy diagnostics, and strict stationarity thresholds?

WHY THIS RUN / ACTIVE NUMERICAL FRONTIER
-----------------------------------------
The latest 023C2AQS2R3 checkpoint has approximately

    GRAD_RMS = 2.713e-3,
    GRAD_MAX = 1.350e-2,

with unchanged promotion thresholds

    GRAD_RMS <= 1.5e-3,
    GRAD_MAX <= 5.0e-2.

The pointwise maximum already passes.  The remaining residual is strongly
smooth/extended:

    Gaussian low-frequency L2 fraction  ~ 0.826,
    Gaussian high-frequency L2 fraction ~ 0.022,
    nearest-neighbor roughness           ~ 0.220,

with negligible core and boundary contribution and dominant wall/tail power.

The final bounded 023C2AQS2R3 Newton attempt spent hundreds of HVP/MINRES
iterations without finding a true-residual-certified direction.  Its explicit
stop rule therefore authorizes a targeted preconditioner/coarse-space gate
instead of further damping scans or blind R-LBFGS continuation.

PHYSICAL MODEL / EQUATIONS
--------------------------
No physics is changed.  The same unrestricted static SU(2) Skyrme field is
used:

    phi = (sigma, pi1, pi2, pi3),       phi . phi = 1,

    E = integral (e2 + e4 + V) d^3x,

    V = m^2 (1-sigma)(1+eta sigma),

at

    B = 7,
    eta = 0.4,
    m = 8.

The discrete Euler-Lagrange residual is the exact projected Riemannian gradient

    g(phi) = 0

of the same checkerboard-free fourth-order lattice action used throughout the
023CR3/023CR4R/023C2 sequence.

COARSE-GALERKIN METHOD
----------------------
The coarse space is a NUMERICAL ACCELERATOR ONLY.  It does not constrain the
final field and is never used as a stationarity or physics diagnostic.

At each outer coarse correction:

1. Build the complete local three-component tangent representation of the FULL
   N=73 residual, with the exact three global pion-isorotation zero modes
   projected out exactly as in the audited Hessian code.

2. Construct a small deterministic residual-informed smooth candidate set from:
   - Gaussian low-pass residuals at several lattice scales;
   - independent tangent-component low-pass residuals;
   - low-order x/y/z modulations of a smooth residual;
   - smooth wall-region and tail-region windows motivated by the already
     reported residual localization.

3. Project every candidate out of the exact isorotation zero modes and
   orthonormalize the surviving vectors.  No spatial rotation or translation
   candidate is projected out.

4. Apply the already validated matrix-free covariant Hessian H to every coarse
   basis vector U_j and form the Galerkin matrix

       A_c = U^T H U.

   The independently measured symmetry defect of A_c is reported before
   numerical symmetrization.

5. Solve the small shifted coarse Newton system

       (A_c + mu I)c = -U^T g,

   and prolong the correction

       delta = U c

   to the FULL tangent field.

6. Accept a candidate ONLY if the complete million-DOF field satisfies:
   - energy Armijo decrease;
   - unchanged B=7 geometric/topology guards;
   - unchanged link-smoothness guard;
   - reduction of the strict normalized stationarity merit computed from the
     FULL exact gradient.

Thus a favorable coarse solve cannot manufacture stationarity: after every
candidate correction the complete exact N=73 residual is recomputed.

COARSE BASIS
------------
The default deterministic basis uses at most fourteen vectors:

- full three-component residual low-pass at sigma = 1, 2, 4, 8 cells;
- each tangent component separately at sigma = 2 cells;
- x, y, z multiplied by the sigma=4 smooth residual;
- wall-window times sigma=2 and sigma=4 smooth residual;
- tail-window times sigma=2 and sigma=4 smooth residual.

The smooth wall/tail windows are used only to improve numerical approximation
of the measured extended residual.  They are NOT physical constraints and do
not appear in the energy, equations, stationarity gate, or final claim.

The code reports

    COARSE_GRADIENT_CAPTURE_FRACTION =
        ||U U^T g|| / ||g||.

A low capture fraction is a direct falsifier of this particular coarse-space
choice and triggers a different two-level/augmented Krylov design rather than
blind repetition.

HESSIAN / ZERO-MODE HANDLING
----------------------------
The full covariant Hessian-vector product is imported from the audited 023C2A
implementation and first rechecked at the actual field for finite-difference
step convergence and bilinear self-adjointness.

Only the three exact global pion-isorotation zero modes are projected out.
Approximate finite-box translation/rotation modes are not removed, so the
coarse gate cannot hide a real physical residual in those directions.

DAMPING / COARSE SPECTRUM
-------------------------
The small Galerkin matrix is diagonalized explicitly.  If its lowest
eigenvalue is non-positive or nearly singular, a minimum positive shift is
added before trying the predeclared coarse damping ladder.

This shift is only a nonlinear-solver regularization.  It does not change the
field energy or equations.  Every accepted correction is still judged by the
unshifted exact full-field gradient.

OPERATIONAL OBSERVABLE
----------------------
Primary stationarity merit:

    M = max(
        GRAD_RMS / 1.5e-3,
        GRAD_MAX / 5.0e-2
    ).

Strict N=73 stationarity requires exactly

    GRAD_RMS <= 1.5e-3
    GRAD_MAX <= 5.0e-2.

Only after strict stationarity passes does this file run the existing complete
stress-energy audit and the validated continuous finite-payload force
certificate.  Positive radial force is outward in the repository convention.

INPUTS
------
Required source:
    simulations/023c2aqs2r3_true_residual_newton_and_localized_stationarity.py

Preferred state:
    results/data/023c2aqs2r4_n73_coarse_galerkin_checkpoint.npz

Fallback:
    results/data/023c2aqs2r3_n73_true_residual_newton_checkpoint.npz

OUTPUTS
-------
Checkpoint:
    results/data/023c2aqs2r4_n73_coarse_galerkin_checkpoint.npz

Strict stationary artifact:
    results/data/023c2aqs2r4_strict_stationary_b7_n73.npz

UNITS / SIGN CONVENTIONS
------------------------
Dimensionless Skyrme units inherited from the 023 branch.  Positive radial
finite-payload response means outward acceleration after the common positive
linearized-GR factor.

ASSUMPTIONS / APPROXIMATION LEVEL
---------------------------------
Flat-spacetime classical Skyrme matter on the same finite N=73 Cartesian
lattice with fixed true-vacuum boundary.  Gravity is evaluated only as the
existing static linearized-GR operational readout after strict stationarity.

VALIDATION / FALSIFICATION
--------------------------
- fail-closed exact 023C2AQS2R3 source hash;
- external 94-test known-solution suite;
- inherited exact discrete action and gradient;
- HVP step convergence at the actual field;
- full-Hessian bilinear self-adjointness at the actual field;
- coarse Galerkin symmetry audit;
- exact-zero-mode projection;
- complete field gradient after every coarse correction;
- topology/link-smoothness and Armijo guards;
- residual localization before and after;
- existing physical stress-energy and continuous-force audit only after strict
  stationarity.

PROMOTION CONDITION
-------------------
This file may establish only:

    STRICT_STATIONARY_N73
    plus the declared N73 continuous-force sentinel.

It does NOT establish complete 023C stability.

FALSIFIERS / STOP RULES
-----------------------
- Failed upstream audit or HVP validation: numerical failure; stop.
- Coarse gradient capture fraction below the declared minimum: stop for a
  richer two-level/augmented Krylov coarse space.
- Loss of |B|=7 or link smoothness: reject the candidate.
- No full-field merit-reducing coarse correction in the bounded outer slice:
  stop; do not tune damping indefinitely.
- Certified inward continuous force after strict stationarity: operational
  blocker for the declared payload point, subject to companion-resolution
  confirmation.
- Do not weaken stationarity, topology, force, DEC, or trace thresholds.

LIMITATIONS / CLAIM BOUNDARIES
-----------------------------
This run does not establish:
- a positive full physical Hessian;
- binary-fission stability;
- N=73/N=81 continuum force convergence;
- nonlinear Einstein-Skyrme consistency;
- practical energy scaling;
- a material realization;
- an experiment;
- a practical antigravity device;
- discovery of new physics.

RELATED FILES
-------------
simulations/023c2aqs2r3_true_residual_newton_and_localized_stationarity.py
simulations/023c2aqs2r2_n73_adaptive_damping_inexact_newton_closure.py
simulations/023c2a_n73_resolution_and_full_tangent_hessian.py
simulations/023c2aqs2_n73_stationarity_and_continuous_force_resolution.py
simulations/023c2aqs_continuous_field_active_source_force_integration.py

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023C2AQS2R4_RESIDUAL_INFORMED_COARSE_GALERKIN_STATIONARITY_REPAIR
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

R3_SOURCE = SIM / "023c2aqs2r3_true_residual_newton_and_localized_stationarity.py"
EXPECTED_R3_SHA256 = "8d2419c5a3fe4fa52788b636bb7081fa6efde51e79e248d2cad0d29fe321d8f4"

UPSTREAM_CHECKPOINT = DATA / "023c2aqs2r3_n73_true_residual_newton_checkpoint.npz"
CHECKPOINT = DATA / "023c2aqs2r4_n73_coarse_galerkin_checkpoint.npz"
FINAL = DATA / "023c2aqs2r4_strict_stationary_b7_n73.npz"

B = 7
ETA = 0.4
MASS = 8.0
N = 73

GRAD_RMS_TOL = 1.5e-3
GRAD_MAX_TOL = 5.0e-2
MAX_NEIGHBOR_ANGLE = 0.70

MAX_OUTER = max(1, int(os.environ.get("AG_CG4_MAX_OUTER", "3")))
MAX_LINESEARCH = max(4, int(os.environ.get("AG_CG4_MAX_LINESEARCH", "8")))
HVP_POINT_ANGLE = float(os.environ.get("AG_CG4_HVP_POINT_ANGLE", "2e-4"))
MIN_CAPTURE_FRACTION = float(os.environ.get("AG_CG4_MIN_CAPTURE", "0.45"))
MERIT_FACTOR = float(os.environ.get("AG_CG4_MERIT_FACTOR", "0.99"))
ARMIJO_C1 = float(os.environ.get("AG_CG4_ARMIJO_C1", "1e-4"))
MAX_COARSE_BASIS = max(6, int(os.environ.get("AG_CG4_MAX_BASIS", "14")))
DAMPING_MULTIPLIERS = tuple(
    float(x)
    for x in os.environ.get("AG_CG4_DAMPING_MULTIPLIERS", "0,0.25,1,4").split(",")
)


def sha256(path: Path) -> str:
    """Return SHA-256 for one scientific source file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def require(path: Path) -> None:
    """Fail closed when a required file is absent."""
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def load_module(name: str, path: Path):
    """Import one repository simulation without invoking its main routine."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def stationarity_merit(rms: float, gmax: float) -> float:
    """Return the unchanged normalized distance from strict stationarity."""
    return max(rms / GRAD_RMS_TOL, gmax / GRAD_MAX_TOL)


def load_state(r3, qs2, cr3, cr4r):
    """Load this gate's checkpoint or fall back to the latest R3 checkpoint."""
    source = CHECKPOINT if CHECKPOINT.is_file() else UPSTREAM_CHECKPOINT
    require(source)
    with np.load(source, allow_pickle=False) as d:
        phi = np.array(d["phi"], dtype=float, copy=True)
        axis = np.array(d["axis"], dtype=float, copy=True)
        dx = float(d["dx"])
        accepted_total = int(d["accepted_total"]) if "accepted_total" in d.files else 0
        nk_total = int(d["newton_accepted_total"]) if "newton_accepted_total" in d.files else 0
        b = int(d["B"]) if "B" in d.files else B
        eta = float(d["eta"]) if "eta" in d.files else ETA
        mass = float(d["mass"]) if "mass" in d.files else MASS
        s_hist = np.asarray(d["s_hist"], dtype=float) if "s_hist" in d.files else np.empty((0, N, N, N, 4))
        y_hist = np.asarray(d["y_hist"], dtype=float) if "y_hist" in d.files else np.empty((0, N, N, N, 4))
        coarse_total = int(d["coarse_accepted_total"]) if "coarse_accepted_total" in d.files else 0

    if phi.shape != (N, N, N, 4) or axis.shape != (N,):
        raise RuntimeError(f"Unexpected N73 state shape phi={phi.shape} axis={axis.shape}")
    if b != B or abs(eta - ETA) > 1e-14 or abs(mass - MASS) > 1e-14:
        raise RuntimeError("N73 metadata mismatch")
    norm_err = float(np.max(np.abs(np.linalg.norm(phi, axis=-1) - 1.0)))
    if norm_err > 5e-10:
        raise RuntimeError(f"N73 S3 norm violation {norm_err}")

    history, discarded = qs2.history_from_arrays(cr3, s_hist, y_hist, dx)
    state = cr4r.State(phi=phi, axis=axis, dx=dx, accepted_total=accepted_total)
    return state, history, source, discarded, norm_err, nk_total, coarse_total


def save_checkpoint(state, history, E, rms, gmax, nk_total, coarse_total):
    """Persist the full field and transported L-BFGS history."""
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
        energy=np.array(E),
        grad_rms=np.array(rms),
        grad_max=np.array(gmax),
        source=np.array("023C2AQS2R4_COARSE_GALERKIN"),
        s_hist=s_hist,
        y_hist=y_hist,
    )
    print(
        f"CG4_CHECKPOINT_WRITTEN={CHECKPOINT.relative_to(ROOT)} "
        f"COARSE_ACCEPTED_TOTAL={coarse_total} HISTORY_LENGTH={len(history)}",
        flush=True,
    )


def save_final(state, E, rms, gmax, diag, nk_total, coarse_total):
    """Persist the strict N=73 field only after the original gates pass."""
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
        energy=np.array(E),
        grad_rms=np.array(rms),
        grad_max=np.array(gmax),
        topology4=np.array(diag.topology4),
        active_total=np.array(diag.active_total),
        min_active_fraction=np.array(diag.min_active_fraction),
        min_dec_scaled_margin=np.array(diag.min_dec_scaled_margin),
        max_active_trace_scaled=np.array(diag.max_active_trace_scaled),
        source=np.array("023C2AQS2R4_N73_STRICT_STATIONARY"),
    )
    print(f"CG4_STRICT_STATIONARY_FIELD_ARTIFACT={FINAL.relative_to(ROOT)}", flush=True)


def smooth_windows(axis: np.ndarray):
    """Return smooth wall/tail numerical windows on the interior lattice."""
    coords = np.asarray(axis[1:-1], dtype=float)
    X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")
    R = np.sqrt(X * X + Y * Y + Z * Z)

    # Smooth numerical partitions around the already-used diagnostic radii.
    width = 0.18
    sigmoid = lambda q: 0.5 * (1.0 + np.tanh(q / width))
    wall = sigmoid(R - 0.30) * sigmoid(1.60 - R)
    tail = sigmoid(R - 1.45)

    scale = max(float(np.max(np.abs(coords))), 1e-300)
    return X / scale, Y / scale, Z / scale, wall, tail


def candidate_vectors(gcomp: np.ndarray, axis: np.ndarray):
    """Construct deterministic smooth residual-informed coarse candidates."""
    candidates = []

    lows = {}
    for sigma in (1.0, 2.0, 4.0, 8.0):
        low = np.empty_like(gcomp)
        for a in range(3):
            low[..., a] = gaussian_filter(gcomp[..., a], sigma=sigma, mode="nearest")
        lows[sigma] = low
        candidates.append((f"FULL_SIGMA_{sigma:g}", low))

    # Independent tangent-component freedom at the scale where the measured
    # residual is already very smooth.
    for a in range(3):
        v = np.zeros_like(gcomp)
        v[..., a] = lows[2.0][..., a]
        candidates.append((f"COMP_{a}_SIGMA_2", v))

    X, Y, Z, wall, tail = smooth_windows(axis)
    base4 = lows[4.0]
    candidates.extend(
        [
            ("X_MOD_SIGMA_4", X[..., None] * base4),
            ("Y_MOD_SIGMA_4", Y[..., None] * base4),
            ("Z_MOD_SIGMA_4", Z[..., None] * base4),
            ("WALL_SIGMA_2", wall[..., None] * lows[2.0]),
            ("WALL_SIGMA_4", wall[..., None] * base4),
            ("TAIL_SIGMA_2", tail[..., None] * lows[2.0]),
            ("TAIL_SIGMA_4", tail[..., None] * base4),
        ]
    )

    return candidates[:MAX_COARSE_BASIS]


def orthonormal_coarse_basis(c2a, candidates, Z, gnorm: float):
    """Project exact zero modes and modified-Gram-Schmidt the coarse vectors."""
    basis_vectors = []
    names = []

    for name, arr in candidates:
        v = np.asarray(arr, dtype=float).reshape(-1)
        v = c2a.project_subspace(v, Z)

        for q in basis_vectors:
            v = v - q * float(np.dot(q, v))
        # Reorthogonalize once because low-pass residual candidates can be very
        # nearly linearly dependent.
        for q in basis_vectors:
            v = v - q * float(np.dot(q, v))

        nrm = float(np.linalg.norm(v))
        if nrm <= max(1e-12 * gnorm, 1e-14):
            print(f"CG4_COARSE_CANDIDATE_DROPPED={name} NORM={nrm:.15e}", flush=True)
            continue
        basis_vectors.append(v / nrm)
        names.append(name)

    if not basis_vectors:
        raise RuntimeError("No independent coarse basis vectors survived")

    U = np.column_stack(basis_vectors)
    gram_err = float(np.max(np.abs(U.T @ U - np.eye(U.shape[1]))))
    print(f"CG4_COARSE_BASIS_DIM={U.shape[1]}", flush=True)
    print("CG4_COARSE_BASIS_NAMES=" + ",".join(names), flush=True)
    print(f"CG4_COARSE_ORTHONORMALITY_MAXERR={gram_err:.15e}", flush=True)
    if gram_err > 2e-10:
        raise RuntimeError("Coarse basis orthonormality audit failed")
    return U


def coarse_galerkin_slice(r3, r2, r, qs2, c2a, cr2, cr3, cr4r, state, history, nk_total, coarse_total):
    """Run bounded residual-informed coarse Galerkin corrections."""
    E, _e2, _e4, _e0, g, rms, gmax, station = r.strict_stationarity(cr3, state.phi, state.dx)

    stats = {
        "outer_attempted": 0,
        "outer_accepted": 0,
        "hvp_calls": 0,
        "line_rejects": 0,
        "capture_failures": 0,
    }

    for outer in range(1, MAX_OUTER + 1):
        if station:
            break

        stats["outer_attempted"] += 1
        phi = state.phi
        dx = state.dx
        merit0 = stationarity_merit(rms, gmax)

        basis = c2a.tangent_basis_householder(phi)
        Z = c2a.orthonormal_columns(c2a.isorotation_modes(phi, basis))
        gvec = c2a.project_subspace(c2a.field_to_components(g, basis), Z)
        gnorm = float(np.linalg.norm(gvec))
        ndof = gvec.size

        print(
            f"CG4_OUTER={outer} NDOF={ndof} GRAD_RMS={rms:.15e} "
            f"GRAD_MAX={gmax:.15e} STATIONARITY_MERIT={merit0:.15e}",
            flush=True,
        )

        if outer == 1:
            if not r.audit_hessian_operator(c2a, cr3, phi, state.axis, dx, basis, Z):
                raise RuntimeError("CG4 HVP validation failed")

        gcomp = gvec.reshape(N - 2, N - 2, N - 2, 3)
        U = orthonormal_coarse_basis(
            c2a,
            candidate_vectors(gcomp, state.axis),
            Z,
            gnorm,
        )

        proj = U @ (U.T @ gvec)
        capture = float(np.linalg.norm(proj) / max(gnorm, 1e-300))
        residual_after_projection = float(np.linalg.norm(gvec - proj) / max(gnorm, 1e-300))
        print(f"CG4_COARSE_GRADIENT_CAPTURE_FRACTION={capture:.15e}", flush=True)
        print(f"CG4_COARSE_ORTHOGONAL_RESIDUAL_FRACTION={residual_after_projection:.15e}", flush=True)

        if capture < MIN_CAPTURE_FRACTION:
            stats["capture_failures"] += 1
            print("CG4_COARSE_CAPTURE_GATE=FAIL", flush=True)
            break
        print("CG4_COARSE_CAPTURE_GATE=PASS", flush=True)

        hvp, calls = c2a.make_hvp(cr3, phi, dx, basis, Z, HVP_POINT_ANGLE)
        HU = np.empty_like(U)
        for j in range(U.shape[1]):
            HU[:, j] = hvp(U[:, j])
            print(
                f"CG4_COARSE_HVP_PROGRESS={j+1}/{U.shape[1]}",
                flush=True,
            )
        stats["hvp_calls"] += calls["count"]

        Ac_raw = U.T @ HU
        asym = float(
            np.linalg.norm(Ac_raw - Ac_raw.T)
            / max(np.linalg.norm(Ac_raw), 1e-300)
        )
        print(f"CG4_COARSE_GALERKIN_RELASYM={asym:.15e}", flush=True)
        if asym > 5e-6:
            raise RuntimeError("Coarse Galerkin Hessian symmetry audit failed")

        Ac = 0.5 * (Ac_raw + Ac_raw.T)
        evals = np.linalg.eigvalsh(Ac)
        emin = float(evals[0])
        emax = float(evals[-1])
        abs_nonzero = np.abs(evals[np.abs(evals) > 1e-12 * max(np.max(np.abs(evals)), 1.0)])
        escale = float(np.median(abs_nonzero)) if abs_nonzero.size else max(abs(emax), 1.0)
        shift_floor = max(0.0, -emin + 0.05 * escale)

        print("CG4_COARSE_EIGENVALUES=" + ",".join(f"{x:.9e}" for x in evals), flush=True)
        print(f"CG4_COARSE_EIG_MIN={emin:.15e}", flush=True)
        print(f"CG4_COARSE_EIG_MAX={emax:.15e}", flush=True)
        print(f"CG4_COARSE_EIG_SCALE={escale:.15e}", flush=True)
        print(f"CG4_COARSE_POSITIVITY_SHIFT_FLOOR={shift_floor:.15e}", flush=True)

        b = U.T @ gvec
        accepted_pack = None

        for mult in DAMPING_MULTIPLIERS:
            mu = shift_floor + max(0.0, mult) * escale
            mat = Ac + mu * np.eye(Ac.shape[0])
            try:
                coeff = np.linalg.solve(mat, -b)
            except np.linalg.LinAlgError:
                print(f"CG4_COARSE_SOLVE_DAMP={mult:.6e} SINGULAR=YES", flush=True)
                continue

            delta = U @ coeff
            delta = c2a.project_subspace(delta, Z)

            # Coarse shifted linear residual in the Galerkin system.
            coarse_rel = float(
                np.linalg.norm(b + (Ac + mu * np.eye(Ac.shape[0])) @ coeff)
                / max(np.linalg.norm(b), 1e-300)
            )

            direction = c2a.components_to_field(delta, basis, phi.shape)
            direction = cr3.project_tangent(phi, direction)
            gd = cr3.tangent_inner(g, direction, dx)
            g2 = max(cr3.tangent_inner(g, g, dx), 1e-300)

            print(
                f"CG4_COARSE_SOLVE_DAMP={mult:.6e} MU={mu:.15e} "
                f"COARSE_LINEAR_RELRES={coarse_rel:.15e} G_DOT_DELTA={gd:.15e}",
                flush=True,
            )

            if (not math.isfinite(gd)) or gd >= -1e-12 * g2:
                print("CG4_COARSE_DIRECTION_DESCENT=NO_TRY_MORE_DAMPING", flush=True)
                continue
            print("CG4_COARSE_DIRECTION_DESCENT=YES", flush=True)

            max_point = float(
                np.max(np.linalg.norm(direction[1:-1, 1:-1, 1:-1], axis=-1))
            )
            trust_angle = min(2.0e-2, max(7.5e-4, 0.40 * rms))
            alpha = min(1.0, trust_angle / max(max_point, 1e-300))

            print(
                f"CG4_DIRECTION_OUTER={outer} DAMP_MULT={mult:.6e} "
                f"MAX_POINT={max_point:.15e} TRUST_ANGLE={trust_angle:.15e} "
                f"ALPHA0={alpha:.15e}",
                flush=True,
            )

            for ls in range(MAX_LINESEARCH):
                cand = cr3.exp_map_update(phi, direction, alpha)
                Etrial = cr3.high_order_energy_gradient(cand, dx, False)[0]

                if (not math.isfinite(Etrial)) or Etrial > E + ARMIJO_C1 * alpha * gd:
                    stats["line_rejects"] += 1
                    alpha *= 0.5
                    continue

                ok, reason, _ = qs2.candidate_admissible(
                    cr3, cr2, cand, dx, state.accepted_total + 1
                )
                if not ok:
                    stats["line_rejects"] += 1
                    print(f"CG4_LINESEARCH_REJECT_REASON={reason}", flush=True)
                    alpha *= 0.5
                    continue

                pack = r.strict_stationarity(cr3, cand, dx)
                Enew, _a, _b2, _c, gnew, rmsnew, gmaxnew, stationnew = pack
                merit_new = stationarity_merit(rmsnew, gmaxnew)
                merit_ok = bool(stationnew or merit_new <= MERIT_FACTOR * merit0)

                print(
                    f"CG4_LINESEARCH_TRIAL_OUTER={outer} DAMP_MULT={mult:.6e} "
                    f"LS={ls} ALPHA={alpha:.15e} ENERGY={Enew:.15e} "
                    f"GRAD_RMS={rmsnew:.15e} GRAD_MAX={gmaxnew:.15e} "
                    f"STATIONARITY_MERIT={merit_new:.15e} "
                    f"MERIT_ACCEPT={'YES' if merit_ok else 'NO'}",
                    flush=True,
                )

                if not merit_ok:
                    stats["line_rejects"] += 1
                    alpha *= 0.5
                    continue

                accepted_pack = (
                    cand, Enew, gnew, rmsnew, gmaxnew, stationnew,
                    direction, alpha, mult, mu, merit_new,
                )
                break

            if accepted_pack is not None:
                break

        if accepted_pack is None:
            print("CG4_COARSE_STEP_ACCEPTED=NO", flush=True)
            break

        (
            cand, Enew, gnew, rmsnew, gmaxnew, stationnew,
            direction, alpha, mult_used, mu_used, merit_new,
        ) = accepted_pack

        old_phi = phi
        old_g = g
        old_merit = merit0

        r.transport_history_after_step(
            cr3, cr4r, old_phi, cand, direction, alpha, old_g, gnew, history
        )

        state.phi = cand
        state.accepted_total += 1
        coarse_total += 1
        stats["outer_accepted"] += 1

        E, g, rms, gmax, station = Enew, gnew, rmsnew, gmaxnew, stationnew

        t4 = cr3.topology4(state.phi, state.dx)
        deg_ok, degrees = cr3.geometric_guard(state.phi, cr2, True)
        angle = cr3.max_neighbor_angle(state.phi)

        print(
            f"CG4_COARSE_STEP_ACCEPTED=YES OUTER={outer} "
            f"DAMP_MULT={mult_used:.6e} MU={mu_used:.15e} ALPHA={alpha:.15e} "
            f"MERIT_REDUCTION_FACTOR={old_merit/max(merit_new,1e-300):.15e} "
            f"ENERGY={E:.15e} GRAD_RMS={rms:.15e} GRAD_MAX={gmax:.15e} "
            f"STATIONARITY_MERIT={merit_new:.15e} TOPOLOGY4={t4:.15e} "
            f"GEOMETRIC_DEGREES={','.join(str(x) for x in degrees)} "
            f"MAX_NEIGHBOR_ANGLE={angle:.15e}",
            flush=True,
        )

        if not deg_ok:
            raise RuntimeError("Accepted coarse correction lost geometric B=7")

        save_checkpoint(state, history, E, rms, gmax, nk_total, coarse_total)

    return state, history, E, g, rms, gmax, station, nk_total, coarse_total, stats


def main():
    print("=== 023C2AQS2R4 — RESIDUAL-INFORMED COARSE-GALERKIN N73 CLOSURE ===", flush=True)

    print("\n=== A — FAIL-CLOSED UPSTREAM AUDIT ===", flush=True)
    require(R3_SOURCE)
    actual = sha256(R3_SOURCE)
    print(f"023C2AQS2R3_SOURCE_SHA256={actual}", flush=True)
    if actual != EXPECTED_R3_SHA256:
        raise RuntimeError("023C2AQS2R3 source hash mismatch")
    print("UPSTREAM_023C2AQS2R3_AUDIT=PASS", flush=True)

    r3 = load_module("c2aqs2r4_r3", R3_SOURCE)
    r2 = r3.load_module("c2aqs2r4_r2", r3.R2_SOURCE)
    r = r3.load_module("c2aqs2r4_r", r2.R_SOURCE)
    qs2 = r3.load_module("c2aqs2r4_qs2", r.QS2_SOURCE)
    c2a = r3.load_module("c2aqs2r4_c2a", r.C2A_SOURCE)
    c2ar = qs2.load_module("c2aqs2r4_c2ar", qs2.C2AR_SOURCE)
    c2aqs = qs2.load_module("c2aqs2r4_c2aqs", qs2.C2AQS_SOURCE)
    cr2 = c2ar.load_module("c2aqs2r4_cr2", c2ar.CR2_SOURCE)
    cr3 = c2ar.load_module("c2aqs2r4_cr3", c2ar.CR3_SOURCE)
    cr4r = c2ar.load_module("c2aqs2r4_cr4r", c2ar.CR4R_SOURCE)

    print("\n=== B — LOAD LATEST N73 FIELD ===", flush=True)
    state, history, source, discarded, norm_err, nk_total, coarse_total = load_state(
        r3, qs2, cr3, cr4r
    )

    E0, _a, _b, _c, g0, rms0, gmax0, station0 = r.strict_stationarity(
        cr3, state.phi, state.dx
    )
    deg_ok0, degrees0 = cr3.geometric_guard(state.phi, cr2, True)

    print(f"CG4_START_SOURCE={source.relative_to(ROOT)}", flush=True)
    print(f"CG4_START_ACCEPTED_TOTAL={state.accepted_total}", flush=True)
    print(f"CG4_START_NEWTON_ACCEPTED_TOTAL={nk_total}", flush=True)
    print(f"CG4_START_COARSE_ACCEPTED_TOTAL={coarse_total}", flush=True)
    print(f"CG4_START_HISTORY_LENGTH={len(history)}", flush=True)
    print(f"CG4_START_HISTORY_DISCARDED={discarded}", flush=True)
    print(f"CG4_START_NORM_MAXERR={norm_err:.15e}", flush=True)
    print(f"CG4_START_ENERGY={E0:.15e}", flush=True)
    print(f"CG4_START_GRAD_RMS={rms0:.15e}", flush=True)
    print(f"CG4_START_GRAD_MAX={gmax0:.15e}", flush=True)
    print(f"CG4_START_STATIONARITY_MERIT={stationarity_merit(rms0,gmax0):.15e}", flush=True)
    print("CG4_START_STRICT_STATIONARITY=" + ("PASS" if station0 else "FAIL"), flush=True)
    print(f"CG4_START_TOPOLOGY4={cr3.topology4(state.phi,state.dx):.15e}", flush=True)
    print("CG4_START_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in degrees0), flush=True)

    if not deg_ok0:
        raise RuntimeError("Starting N73 field failed geometric B=7")

    print("\n=== C — START RESIDUAL LOCALIZATION ===", flush=True)
    cr4r.residual_localization(cr3, state, g0)
    r3.residual_frequency_diagnostic(c2a, cr3, state, g0, "CG4_START")

    if station0:
        state2, history2 = state, history
        E, g, rms, gmax, station = E0, g0, rms0, gmax0, station0
        stats = {
            "outer_attempted": 0, "outer_accepted": 0,
            "hvp_calls": 0, "line_rejects": 0, "capture_failures": 0,
        }
    else:
        print("\n=== D — COARSE-GALERKIN STATIONARITY SLICE ===", flush=True)
        (
            state2, history2, E, g, rms, gmax, station,
            nk_total, coarse_total, stats,
        ) = coarse_galerkin_slice(
            r3, r2, r, qs2, c2a, cr2, cr3, cr4r,
            state, history, nk_total, coarse_total,
        )

    print("\n=== E — END-OF-SLICE AUDIT ===", flush=True)
    t4 = cr3.topology4(state2.phi, state2.dx)
    deg_ok, degrees = cr3.geometric_guard(state2.phi, cr2, True)
    angle = cr3.max_neighbor_angle(state2.phi)

    print(f"CG4_OUTER_ATTEMPTED={stats['outer_attempted']}", flush=True)
    print(f"CG4_OUTER_ACCEPTED={stats['outer_accepted']}", flush=True)
    print(f"CG4_HVP_MATVEC_CALLS={stats['hvp_calls']}", flush=True)
    print(f"CG4_LINESEARCH_REJECTS={stats['line_rejects']}", flush=True)
    print(f"CG4_CAPTURE_FAILURES={stats['capture_failures']}", flush=True)
    print(f"CG4_FINAL_ENERGY={E:.15e}", flush=True)
    print(f"CG4_FINAL_GRAD_RMS={rms:.15e}", flush=True)
    print(f"CG4_FINAL_GRAD_MAX={gmax:.15e}", flush=True)
    print(f"CG4_FINAL_STATIONARITY_MERIT={stationarity_merit(rms,gmax):.15e}", flush=True)
    print("CG4_FINAL_STRICT_STATIONARITY=" + ("PASS" if station else "FAIL"), flush=True)
    print(f"CG4_FINAL_TOPOLOGY4={t4:.15e}", flush=True)
    print("CG4_FINAL_GEOMETRIC_DEGREES=" + ",".join(str(x) for x in degrees), flush=True)
    print(f"CG4_FINAL_MAX_NEIGHBOR_ANGLE={angle:.15e}", flush=True)

    print("\n=== F — FINAL RESIDUAL LOCALIZATION ===", flush=True)
    cr4r.residual_localization(cr3, state2, g)
    r3.residual_frequency_diagnostic(c2a, cr3, state2, g, "CG4_FINAL")

    if not station:
        save_checkpoint(state2, history2, E, rms, gmax, nk_total, coarse_total)
        merit0 = stationarity_merit(rms0, gmax0)
        merit1 = stationarity_merit(rms, gmax)
        improvement = merit0 / max(merit1, 1e-300)

        print("\n=== G — BOUNDED INCOMPLETE DECISION ===", flush=True)
        print("023C2AQS2R4_COARSE_GALERKIN=INCOMPLETE_N73_STATIONARITY", flush=True)
        print("N73_ACTUAL_FINE_STRICT_STATIONARITY=NOT_YET", flush=True)
        print(f"CG4_SLICE_MERIT_REDUCTION_FACTOR={improvement:.15e}", flush=True)

        if stats["capture_failures"] > 0:
            print("COARSE_GALERKIN_LOCAL_ACCELERATION=COARSE_SPACE_INSUFFICIENT", flush=True)
            print("NEXT=023C2AQS2R5_RICHER_TWO_LEVEL_AUGMENTED_MINRES_PRECONDITIONER", flush=True)
        elif stats["outer_accepted"] > 0 and improvement >= 1.10:
            print("COARSE_GALERKIN_LOCAL_ACCELERATION=SUPPORTED", flush=True)
            print("NEXT=RERUN_SAME_023C2AQS2R4_FROM_COARSE_CHECKPOINT", flush=True)
        else:
            print("COARSE_GALERKIN_LOCAL_ACCELERATION=NOT_ESTABLISHED", flush=True)
            print("NEXT=023C2AQS2R5_AUGMENTED_MINRES_WITH_EXPLICIT_COARSE_CORRECTION", flush=True)

        print("N73_CONTINUOUS_FORCE=NOT_RUN_BEFORE_STATIONARITY", flush=True)
        print("FULL_PHYSICAL_HESSIAN=DEFERRED_OPERATIONAL_FORCE_AND_FINE_FIELD_UNRESOLVED", flush=True)
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR_NOT_A_PROBABILITY", flush=True)
        print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED", flush=True)
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
        return

    print("\n=== G — STRICT N73 PHYSICAL FIELD AUDIT ===", flush=True)
    diag = cr3.continuum_local_diagnostics(state2.phi, state2.axis, state2.dx, cr2)

    print(f"CG4_N73_STATIONARY_CONTINUUM_ENERGY={diag.energy_continuum:.15e}", flush=True)
    print(f"CG4_N73_STATIONARY_ACTIVE_TOTAL={diag.active_total:.15e}", flush=True)
    print(f"CG4_N73_STATIONARY_MIN_ACTIVE_FRACTION={diag.min_active_fraction:.15e}", flush=True)
    print(f"CG4_N73_STATIONARY_MIN_DEC_SCALED_MARGIN={diag.min_dec_scaled_margin:.15e}", flush=True)
    print(f"CG4_N73_STATIONARY_MAX_ACTIVE_TRACE_SCALED={diag.max_active_trace_scaled:.15e}", flush=True)

    physical_gate = bool(
        deg_ok
        and diag.active_total > 0.0
        and diag.min_active_fraction <= -1.0e-2
        and diag.min_dec_scaled_margin >= -1.0e-9
        and diag.max_active_trace_scaled <= 1.0e-10
        and angle <= MAX_NEIGHBOR_ANGLE
    )

    print("CG4_N73_STATIONARY_PHYSICAL_FIELD_GATE=" + ("PASS" if physical_gate else "FAIL"), flush=True)
    save_final(state2, E, rms, gmax, diag, nk_total, coarse_total)

    if not physical_gate:
        print("023C2AQS2R4_COARSE_GALERKIN=RED_STRICT_N73_PHYSICAL_FIELD_GATE", flush=True)
        print("FULL_PHYSICAL_HESSIAN=DEFERRED_BY_FINE_FIELD_PHYSICAL_FALSIFIER", flush=True)
        print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_PENDING_RERANK", flush=True)
        print("NEXT=PRESERVE_NEGATIVE_RESULT_AND_RERANK_023_BRANCH", flush=True)
        return

    print("\n=== H — CONDITIONAL CONTINUOUS-FORCE CERTIFICATE ===", flush=True)
    n65ref = qs2.load_n65_force_reference()
    aqr = c2aqs.load_module("c2aqs2r4_aqr", c2aqs.AQR_SOURCE)
    aqr.validate_analytic_formulae()
    print("CG4_N73_ANALYTIC_KERNEL_VALIDATION=PASS", flush=True)

    force = qs2.continuous_force_gate(
        c2aqs,
        aqr,
        cr3,
        state2.phi,
        state2.axis,
        state2.dx,
        n65ref,
    )

    print("\n=== I — 023C2AQS2R4 DECISION ===", flush=True)

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

    print(f"023C2AQS2R4_COARSE_GALERKIN={decision}", flush=True)
    print("N73_ACTUAL_FINE_STRICT_STATIONARITY=PASS", flush=True)
    print(f"FULL_PHYSICAL_HESSIAN={hessian}", flush=True)
    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_FROM_023BR_NOT_A_PROBABILITY", flush=True)
    print(f"NEXT={next_step}", flush=True)
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED_UNTIL_023C_COMPLETE", flush=True)
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO", flush=True)
    print("NEW_PHYSICS_DISCOVERY=NO", flush=True)
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_023C2AQS2R4_RESIDUAL_INFORMED_COARSE_GALERKIN_STATIONARITY_REPAIR", flush=True)


if __name__ == "__main__":
    main()
