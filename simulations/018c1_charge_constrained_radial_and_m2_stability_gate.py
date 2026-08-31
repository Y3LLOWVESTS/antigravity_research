#!/usr/bin/env python3
"""018C-1 — charge-constrained radial stability and microscopic m=2 shape gate.

PURPOSE
-------
This simulation begins the full-composite stability program for the promoted
018B-1B field-theoretical candidate.  It attacks the two cheapest and most
scientifically decisive stability questions before a much larger Fourier-mode
Hessian calculation:

1. Is the negative radial curvature reported by 018B-1B a genuine physical
   instability, or is it an artifact of differentiating the grand potential
   at fixed carrier frequencies instead of fixed conserved Noether charges?

2. Does the *actual microscopic curved field solution* provide enough bending
   rigidity to stabilize the positive-tension wall against the universal
   nonaxisymmetric m=2 drum deformation already identified in 017O?

SCIENTIFIC QUESTION
-------------------
The promoted 018B candidate has two separately conserved global U(1) charges,
Q_phi and Q_sigma.  Stability must therefore be assessed on the fixed-charge
constraint surface.  The 018B-1B radius scan held omega_phi and omega_sigma
fixed and found negative curvature of the grand potential F.  That sign alone
is not the physical fixed-charge radial Hessian.

For a stationary constrained solution

    F(R, omega) = E(R,Q) - omega_i Q_i,

with

    Q_i = - dF/domega_i,

the fixed-charge radial curvature is the Schur complement

    d2E/dR2 |_Q
      = F_RR
        - F_Romega F_omegaomega^{-1} F_omegaR

and, because

    F_Romega = -Q_R,
    F_omegaomega = -Q_omega,

this becomes

    d2E/dR2 |_Q
      = F_RR + Q_R^T Q_omega^{-1} Q_R.

The correction is positive when the charge-susceptibility matrix Q_omega is
positive definite.  This file reconstructs every term by re-solving the full
curved microscopic fields at two spatial resolutions.

The nonaxisymmetric question is different.  For a positive-tension membrane
bounded by a local line theory, a small shape perturbation

    r(varphi) = R [1 + epsilon cos(m varphi)]

has the quadratic energy

    Delta E_m
      = (pi sigma R^2 / 2) (m^2 - 1)
        [ b (m^2 - 1) - 1 ] epsilon^2,

where

    b = B / (sigma R^3)

and B is the line bending rigidity.  Thus m=2 requires

    B > B_crit = sigma R^3 / 3.

Rather than assume a thin-core estimate for B, this file reconstructs B from
018B's *actual fully coupled curved microscopic fields*.  The normalized local
stationary action used in 018B-1A is the full ring action divided by 2*pi*R.
For a local derivative expansion

    f(kappa)
      = f_0 + c_1 kappa + (B/2) kappa^2 + O(kappa^3),

where kappa=1/R.  The c_1 term integrates to a topological total-curvature
constant on a closed loop and does not stabilize shape modes.  Therefore the
quadratic coefficient of f(kappa) directly determines B.

The field-derived rigidity is reconstructed in two independent ways:

- the existing N=41 018B-1A continuation log;
- a fresh N=33 curvature continuation re-solved by this file.

Polynomial fits of degree 2, 3, and 4 are compared.  A deliberately favorable
upper bound on B is then used in the m=2..12 stability test.  If even that
upper bound fails by a large margin, omitted higher-curvature terms cannot be
invoked casually as a rescue.

PHYSICAL MODEL
--------------
The matter model is exactly the promoted 018B two-current/KLS configuration:

- charge-two vortex-forming Higgs field H;
- transverse Higgsed gauge field;
- two neutral current-carrying condensates Phi and Sigma;
- charge-one KLS wall field A;
- the same junction couplings, integer windings, frequencies, wall profile,
  and boundary conditions already promoted by 018B-1B.

No new stabilizer is introduced in this gate.

INPUTS
------
Required repository artifacts:

    simulations/018b0g2_fully_coupled_two_current_matched_2d_junction.py
    simulations/018b1a_global_toroidal_curvature_continuation.py
    simulations/018b1b_global_multipatch_tmunu_gravity_conservation_closeout.py
    results/logs/018b0h_complete_source_gravity_revalidation.log
    results/logs/018b1a_global_toroidal_curvature_continuation.log
    results/logs/018b1b_global_multipatch_tmunu_gravity_conservation_closeout.log
    results/data/018b1b_global_field_theoretical_candidate.npz

UNITS
-----
Dimensionless natural/model units inherited from 018B.  Only dimensionless
ratios are used for the stability decisions.

SIGN CONVENTIONS
----------------
Positive Hessian curvature means restoring/stable in the tested direction.
Negative quadratic shape energy means an unstable deformation.
Positive wall tension sigma is the physical KLS membrane tension.

APPROXIMATION LEVEL
-------------------
This is a flat-spacetime matter-field stability preflight around the promoted
018B stationary solution.  It does not include metric backreaction or frame
dragging.  The radial Schur-complement test uses the full curved microscopic
field solves.  The m>=2 gate uses the local derivative expansion of the same
microscopic field theory and extracts its bending coefficient directly from
curved field solutions.

This is deliberately cheaper than the final full 2D Fourier-sector Hessian.
A GREEN positive result would authorize that full spectrum calculation.  A
large-margin RED result is a high-information falsifier and must not be hidden
by adding arbitrary rigidity sectors.

BOUNDARY CONDITIONS
-------------------
Inherited exactly from 018B-1A/1B.  The fresh N=33 curvature reconstruction
uses the same fixed outer microscopic profiles and continuation path.

CONSERVATION REQUIREMENTS
-------------------------
The radial mode is evaluated at fixed integer windings and fixed separately
conserved Q_phi and Q_sigma through the exact Schur complement.  The charge
susceptibility matrix must be positive definite and numerically well
conditioned enough for the correction to be meaningful.

VALIDATION / FALSIFICATION
--------------------------
Radial validation:

- repeat at N=25 and N=33;
- reconstruct F_RR, Q_R, and Q_omega independently;
- require positive-definite Q_omega;
- require positive fixed-charge radial curvature at both resolutions;
- require the two curvatures to agree in sign and reasonable scale.

Rigidity validation:

- reconstruct N=41 curvature data from the executed 018B-1A log;
- independently re-solve N=33 curvature stages;
- fit degree 2/3/4 curvature expansions;
- require all extracted B estimates to have a controlled spread;
- use a conservative upper bound on B in the shape test;
- numerically integrate finite-amplitude polar deformations as an independent
  check of the analytic quadratic formula.

STOP RULE
---------
If the conservative upper bound on microscopic B is still below B_crit for
m=2 by orders of magnitude and the direct finite-amplitude shape calculation
is negative, do not proceed as if 018C were healthy.  Classify a robust m=2
instability and run at most one direct full-field m=2 eigenmode confirmation
before demoting/reranking the present local wall+r​​im architecture.

PERMITTED CLAIMS
----------------
This gate may establish or falsify:

- fixed-charge axisymmetric radial stability;
- adequacy of the microscopic bending rigidity for nonaxisymmetric wall-rim
  shape stability in the local derivative expansion;
- whether a direct m=2 full-field confirmation is warranted.

It may NOT establish:

- full composite stability by itself;
- nonlinear Einstein-matter stability;
- practical antigravity;
- a new-physics discovery.

RELATED FILES
-------------
RESEARCH_BUILDPLAN.md section 018C
journal/2026-08-29_017a_017s_drum_vorton_realization_and_thermal_obstruction.md
018B-1A and 018B-1B source/log/artifacts
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import importlib.util
import math
from pathlib import Path
import re
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

G2_SOURCE = ROOT / "simulations/018b0g2_fully_coupled_two_current_matched_2d_junction.py"
A_SOURCE = ROOT / "simulations/018b1a_global_toroidal_curvature_continuation.py"
B_SOURCE = ROOT / "simulations/018b1b_global_multipatch_tmunu_gravity_conservation_closeout.py"

H_LOG = ROOT / "results/logs/018b0h_complete_source_gravity_revalidation.log"
A_LOG = ROOT / "results/logs/018b1a_global_toroidal_curvature_continuation.log"
B_LOG = ROOT / "results/logs/018b1b_global_multipatch_tmunu_gravity_conservation_closeout.log"

B_ARTIFACT = ROOT / "results/data/018b1b_global_field_theoretical_candidate.npz"

RADIAL_RESOLUTIONS = (25, 33)
RADIAL_BOX_HALF = 12.0
RADIAL_DR_FRACTION = 1.0e-3
OMEGA_STEPS = (5.0e-5, 1.0e-4)

RIGIDITY_RECOMPUTE_N = 33
RIGIDITY_BOX_HALF = 12.0
RIGIDITY_RATIOS = (
    Fraction(4, 1),
    Fraction(2, 1),
    Fraction(3, 2),
    Fraction(5, 4),
    Fraction(1, 1),
)

M_MODES = tuple(range(2, 13))
FINITE_EPSILONS = (1.0e-4, 3.0e-4, 1.0e-3)

# Numerical acceptance thresholds.  These are intentionally not tuned to the
# preview values; they simply reject ill-conditioned Schur complements or a
# rigidity inference dominated by fit/resolution ambiguity.
MAX_SUSCEPTIBILITY_CONDITION = 1.0e2
MAX_SUSCEPTIBILITY_ASYMMETRY = 0.10
MIN_POSITIVE_RADIAL_CURVATURE = 1.0e-4
MAX_RADIAL_CURVATURE_REL_SPREAD = 0.50
MAX_BENDING_ESTIMATE_REL_SPREAD = 0.50
MIN_SHAPE_NUMERIC_ANALYTIC_AGREEMENT = 0.97


@dataclass
class RadialRecord:
    """One resolution's fixed-charge radial Schur-complement reconstruction."""

    n: int
    f_rr_fixed_omega: float
    correction: float
    e_rr_fixed_charge: float
    susceptibility_condition: float
    susceptibility_asymmetry: float
    qomega_min_eigenvalue: float
    q_r_phi: float
    q_r_sigma: float
    gradient_rms: float


@dataclass
class RigidityRecord:
    """One bending-rigidity fit."""

    source: str
    degree: int
    B: float
    max_fit_residual: float


def load_module(name: str, path: Path):
    """Import one repository simulation without invoking its main()."""

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def require_marker(path: Path, marker: str) -> None:
    """Require an exact upstream GREEN marker."""

    if not path.exists():
        raise RuntimeError(f"Missing upstream log: {path}")

    text = path.read_text(errors="replace")
    if marker not in text:
        raise RuntimeError(f"Missing marker {marker!r} in {path}")


def scalar(path: Path, label: str) -> float:
    """Read one finite floating-point scalar from an exact whole-line label."""

    text = path.read_text(errors="replace")
    number = r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
    match = re.search(r"(?m)^" + re.escape(label) + number + r"\s*$", text)
    if match is None:
        raise RuntimeError(f"Missing exact scalar line {label!r} in {path}")

    value = float(match.group(1))
    if not math.isfinite(value):
        raise RuntimeError(f"Nonfinite {label!r} in {path}")
    return value


def sha256(path: Path) -> str:
    """Return SHA-256 for one artifact."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_artifact(path: Path) -> dict[str, np.ndarray]:
    """Load the promoted 018B-1B field state into independent arrays."""

    if not path.exists():
        raise RuntimeError(f"Missing promoted field artifact: {path}")

    with np.load(path) as payload:
        return {key: np.array(payload[key]) for key in payload.files}


def evaluate_global(
    one,
    g2,
    b1b,
    p,
    data,
    wall_per_area,
    artifact,
    *,
    R: float,
    n_phi: int,
    n_sigma: int,
    omega_phi: float,
    omega_sigma: float,
    n: int,
    h_over_r: float,
):
    """Re-solve one curved field state and reconstruct its global ledger."""

    result = b1b.build_and_solve(
        one,
        g2,
        p,
        data,
        R=R,
        n_phi=n_phi,
        n_sigma=n_sigma,
        omega_phi=omega_phi,
        omega_sigma=omega_sigma,
        n=n,
        box_half=RADIAL_BOX_HALF,
        artifact=artifact,
    )

    evaluation = b1b.global_from_result(
        one,
        g2,
        p,
        data,
        wall_per_area,
        result,
        h_over_r=h_over_r,
        tail_case=b1b.TAIL_CASES[0],
    )

    return result, evaluation


def charge_vector(evaluation) -> np.ndarray:
    """Return the two separately conserved Noether charges."""

    return np.array(
        [
            evaluation.ledger.q_phi_charge,
            evaluation.ledger.q_sigma_charge,
        ],
        dtype=float,
    )


def radial_schur_record(
    one,
    g2,
    b1b,
    p,
    data,
    wall_per_area,
    artifact,
    *,
    n: int,
    R: float,
    n_phi: int,
    n_sigma: int,
    omega: np.ndarray,
    h_over_r: float,
) -> RadialRecord:
    """Reconstruct the fixed-charge radial Hessian by a Schur complement.

    The calculation independently measures:

        F_RR,
        Q_R,
        Q_omega.

    It then evaluates

        E_RR|Q = F_RR + Q_R^T Q_omega^{-1} Q_R.
    """

    center_result, center_eval = evaluate_global(
        one,
        g2,
        b1b,
        p,
        data,
        wall_per_area,
        artifact,
        R=R,
        n_phi=n_phi,
        n_sigma=n_sigma,
        omega_phi=float(omega[0]),
        omega_sigma=float(omega[1]),
        n=n,
        h_over_r=h_over_r,
    )

    dR = RADIAL_DR_FRACTION * R

    _plus_result, plus_eval = evaluate_global(
        one,
        g2,
        b1b,
        p,
        data,
        wall_per_area,
        artifact,
        R=R + dR,
        n_phi=n_phi,
        n_sigma=n_sigma,
        omega_phi=float(omega[0]),
        omega_sigma=float(omega[1]),
        n=n,
        h_over_r=h_over_r,
    )

    _minus_result, minus_eval = evaluate_global(
        one,
        g2,
        b1b,
        p,
        data,
        wall_per_area,
        artifact,
        R=R - dR,
        n_phi=n_phi,
        n_sigma=n_sigma,
        omega_phi=float(omega[0]),
        omega_sigma=float(omega[1]),
        n=n,
        h_over_r=h_over_r,
    )

    f_rr = (
        plus_eval.grand_potential
        - 2.0 * center_eval.grand_potential
        + minus_eval.grand_potential
    ) / (dR * dR)

    q_r = (
        charge_vector(plus_eval)
        - charge_vector(minus_eval)
    ) / (2.0 * dR)

    q_omega = np.zeros((2, 2), dtype=float)

    for j, step in enumerate(OMEGA_STEPS):
        omega_plus = omega.copy()
        omega_minus = omega.copy()
        omega_plus[j] += step
        omega_minus[j] -= step

        _rp, ep = evaluate_global(
            one,
            g2,
            b1b,
            p,
            data,
            wall_per_area,
            artifact,
            R=R,
            n_phi=n_phi,
            n_sigma=n_sigma,
            omega_phi=float(omega_plus[0]),
            omega_sigma=float(omega_plus[1]),
            n=n,
            h_over_r=h_over_r,
        )

        _rm, em = evaluate_global(
            one,
            g2,
            b1b,
            p,
            data,
            wall_per_area,
            artifact,
            R=R,
            n_phi=n_phi,
            n_sigma=n_sigma,
            omega_phi=float(omega_minus[0]),
            omega_sigma=float(omega_minus[1]),
            n=n,
            h_over_r=h_over_r,
        )

        q_omega[:, j] = (
            charge_vector(ep)
            - charge_vector(em)
        ) / (2.0 * step)

    # Q_omega must be symmetric in the converged continuum problem because it
    # is minus the omega-Hessian of the scalar grand potential.  Symmetrize the
    # small finite-grid mismatch but report it explicitly as a validation metric.
    scale = max(float(np.linalg.norm(q_omega)), 1.0e-30)
    asymmetry = float(np.linalg.norm(q_omega - q_omega.T) / scale)
    symmetric = 0.5 * (q_omega + q_omega.T)

    eigenvalues = np.linalg.eigvalsh(symmetric)
    condition = float(np.linalg.cond(symmetric))

    if eigenvalues[0] <= 0.0:
        correction = math.nan
        fixed_charge = math.nan
    else:
        correction = float(q_r @ np.linalg.solve(symmetric, q_r))
        fixed_charge = float(f_rr + correction)

    return RadialRecord(
        n=n,
        f_rr_fixed_omega=float(f_rr),
        correction=correction,
        e_rr_fixed_charge=fixed_charge,
        susceptibility_condition=condition,
        susceptibility_asymmetry=asymmetry,
        qomega_min_eigenvalue=float(eigenvalues[0]),
        q_r_phi=float(q_r[0]),
        q_r_sigma=float(q_r[1]),
        gradient_rms=float(center_result.gradient_rms),
    )


def curvature_actions_from_log(path: Path) -> list[tuple[float, float]]:
    """Read the five unique N=41 curvature stages from the executed 018B-1A log."""

    text = path.read_text(errors="replace")
    pattern = re.compile(
        r"CURVATURE_STAGE=(\d+)/(\d+)\s+"
        r"R=([0-9eE+\-.]+).*?"
        r"ACTION=([0-9eE+\-.]+)"
    )

    by_ratio: dict[tuple[int, int], tuple[float, float]] = {}
    for numerator, denominator, R_text, action_text in pattern.findall(text):
        key = (int(numerator), int(denominator))
        if key not in by_ratio:
            by_ratio[key] = (float(R_text), float(action_text))

    required = [(r.numerator, r.denominator) for r in RIGIDITY_RATIOS]
    missing = [key for key in required if key not in by_ratio]
    if missing:
        raise RuntimeError(f"Missing 018B-1A curvature stages: {missing}")

    return [by_ratio[key] for key in required]


def recompute_curvature_actions(
    one,
    g2,
    b1b,
    p,
    data,
    artifact,
    *,
    R0: float,
    n_phi: int,
    n_sigma: int,
    omega_phi: float,
    omega_sigma: float,
) -> list[tuple[float, float]]:
    """Independently re-solve the curvature continuation on an N=33 grid."""

    records: list[tuple[float, float]] = []
    previous = None

    for ratio in RIGIDITY_RATIOS:
        R = R0 * float(ratio)
        stage_n_phi = one.scaled_integer(n_phi, ratio)
        stage_n_sigma = one.scaled_integer(n_sigma, ratio)

        reference = one.build_problem(
            g2,
            p,
            data,
            R=R,
            n_phi=stage_n_phi,
            n_sigma=stage_n_sigma,
            omega_phi=omega_phi,
            omega_sigma=omega_sigma,
            n=RIGIDITY_RECOMPUTE_N,
            box_half=RIGIDITY_BOX_HALF,
            blend_factor=one.PRIMARY_BLEND_FACTOR,
        )

        problem = one.build_problem(
            g2,
            p,
            data,
            R=R,
            n_phi=stage_n_phi,
            n_sigma=stage_n_sigma,
            omega_phi=omega_phi,
            omega_sigma=omega_sigma,
            n=RIGIDITY_RECOMPUTE_N,
            box_half=RIGIDITY_BOX_HALF,
            blend_factor=one.PRIMARY_BLEND_FACTOR,
        )

        if previous is None:
            b1b.inject_artifact(problem, artifact)
        else:
            one.set_initial_from_result(problem, previous)

        result = one.solve_problem(g2, p, problem, reference)

        if not result.optimizer_success:
            raise RuntimeError(
                f"Fresh rigidity continuation failed at ratio {ratio}: optimizer did not converge"
            )

        print(
            "RIGIDITY_RECOMPUTE_STAGE="
            f"{ratio.numerator}/{ratio.denominator} "
            f"N={RIGIDITY_RECOMPUTE_N} "
            f"R={R:.15e} "
            f"ACTION={result.normalized_action:+.15e} "
            f"GRAD_RMS={result.gradient_rms:.3e} "
            f"GRAD_MAX={result.gradient_max:.3e}"
        )

        records.append((R, float(result.normalized_action)))
        previous = result

    return records


def rigidity_fits(source: str, records: list[tuple[float, float]]) -> list[RigidityRecord]:
    """Fit f(kappa) and extract B=2*c2 for several polynomial orders."""

    R = np.array([row[0] for row in records], dtype=float)
    action = np.array([row[1] for row in records], dtype=float)
    kappa = 1.0 / R

    fits: list[RigidityRecord] = []

    for degree in (2, 3, 4):
        coefficients = np.polyfit(kappa, action, degree)
        # np.polyfit returns descending powers.  The kappa^2 coefficient is
        # always the third coefficient from the end for degree >= 2.
        c2 = float(coefficients[-3])
        B = 2.0 * c2
        residual = float(np.max(np.abs(np.polyval(coefficients, kappa) - action)))

        fits.append(
            RigidityRecord(
                source=source,
                degree=degree,
                B=B,
                max_fit_residual=residual,
            )
        )

    return fits


def polar_shape_geometry(R: float, m: int, epsilon: float, samples: int = 200000):
    """Numerically integrate area, perimeter, and integral(kappa^2 ds).

    The high-resolution one-dimensional quadrature is independent of the
    analytic quadratic shape expansion and is cheap compared with the field
    solves.
    """

    theta = np.linspace(0.0, 2.0 * math.pi, samples, endpoint=False)
    dtheta = 2.0 * math.pi / samples

    cos = np.cos(m * theta)
    sin = np.sin(m * theta)

    r = R * (1.0 + epsilon * cos)
    rp = -R * epsilon * m * sin
    rpp = -R * epsilon * m * m * cos

    ds_dtheta = np.sqrt(r * r + rp * rp)
    curvature = (
        r * r + 2.0 * rp * rp - r * rpp
    ) / np.maximum((r * r + rp * rp) ** 1.5, 1.0e-300)

    area = 0.5 * float(np.sum(r * r) * dtheta)
    perimeter = float(np.sum(ds_dtheta) * dtheta)
    kappa2 = float(np.sum(curvature * curvature * ds_dtheta) * dtheta)

    return area, perimeter, kappa2


def numeric_shape_delta(R: float, sigma: float, B: float, m: int, epsilon: float) -> float:
    """Evaluate the finite-amplitude local wall+line+bending shape energy.

    The local line first derivative tau is chosen so the circular configuration
    is stationary after including the bending term:

        tau = -sigma R + B/(2 R^2).
    """

    area0 = math.pi * R * R
    length0 = 2.0 * math.pi * R
    kappa20 = 2.0 * math.pi / R

    tau = -sigma * R + B / (2.0 * R * R)

    area, length, kappa2 = polar_shape_geometry(R, m, epsilon)

    return (
        sigma * (area - area0)
        + tau * (length - length0)
        + 0.5 * B * (kappa2 - kappa20)
    )


def analytic_shape_coefficient(R: float, sigma: float, B: float, m: int) -> float:
    """Return Delta E / epsilon^2 at quadratic order for one azimuthal mode."""

    b = B / (sigma * R**3)
    mm = float(m * m - 1)
    return 0.5 * math.pi * sigma * R * R * mm * (b * mm - 1.0)


def relative_spread(values: list[float]) -> float:
    """Return max-min divided by a robust magnitude scale."""

    array = np.asarray(values, dtype=float)
    scale = max(float(np.max(np.abs(array))), 1.0e-30)
    return float((np.max(array) - np.min(array)) / scale)


def main() -> None:
    """Run the first promotion-grade 018C stability gate."""

    print("=== 018C-1 — FIXED-CHARGE RADIAL + MICROSCOPIC M2 STABILITY GATE ===")

    require_marker(B_LOG, "018B1B_GLOBAL_MULTIPATCH_T_MUNU_GRAVITY_CONSERVATION_CLOSEOUT=GREEN")
    require_marker(B_LOG, "FIELD_THEORETICAL_CANDIDATE=YES")
    require_marker(A_LOG, "018B1A_GLOBAL_TOROIDAL_CURVATURE_CONTINUATION=GREEN")

    print("\n=== UPSTREAM ARTIFACT AUDIT ===")
    print(f"018B1A_SOURCE_SHA256={sha256(A_SOURCE)}")
    print(f"018B1B_SOURCE_SHA256={sha256(B_SOURCE)}")
    print(f"018B1B_FIELD_ARTIFACT_SHA256={sha256(B_ARTIFACT)}")

    one = load_module("ag018c1_one", A_SOURCE)
    g2 = load_module("ag018c1_g2", G2_SOURCE)
    b1b = load_module("ag018c1_b1b", B_SOURCE)

    p = g2.load_parameters()
    data = g2.reconstruct_continuum(p)
    wall_per_area = b1b.wall_integrated_per_area(g2, data)
    artifact = load_artifact(B_ARTIFACT)

    R = float(artifact["R"])
    n_phi = int(artifact["n_phi"])
    n_sigma = int(artifact["n_sigma"])
    omega = np.array(
        [
            float(artifact["omega_phi"]),
            float(artifact["omega_sigma"]),
        ],
        dtype=float,
    )
    h_over_r = scalar(H_LOG, "SELECTED_H_OVER_R=")
    wall_tension = scalar(H_LOG, "WALL_PROFILE_TENSION=")

    print("\n=== PROMOTED 018B STATE ===")
    print(f"R_EQ={R:.15e}")
    print(f"N_PHI={n_phi}")
    print(f"N_SIGMA={n_sigma}")
    print(f"OMEGA_PHI={omega[0]:+.15e}")
    print(f"OMEGA_SIGMA={omega[1]:+.15e}")
    print(f"Q_PHI_PROMOTED={float(artifact['noether_q_phi']):+.15e}")
    print(f"Q_SIGMA_PROMOTED={float(artifact['noether_q_sigma']):+.15e}")
    print(f"WALL_TENSION={wall_tension:+.15e}")

    # ------------------------------------------------------------------
    # Part I: fixed-charge radial Schur-complement stability.
    # ------------------------------------------------------------------
    print("\n=== FIXED-CHARGE RADIAL SCHUR-COMPLEMENT STABILITY ===")

    radial_records: list[RadialRecord] = []

    for n in RADIAL_RESOLUTIONS:
        record = radial_schur_record(
            one,
            g2,
            b1b,
            p,
            data,
            wall_per_area,
            artifact,
            n=n,
            R=R,
            n_phi=n_phi,
            n_sigma=n_sigma,
            omega=omega,
            h_over_r=h_over_r,
        )
        radial_records.append(record)

        print(
            f"RADIAL_RESOLUTION_N={record.n} "
            f"FIELD_GRAD_RMS={record.gradient_rms:.3e} "
            f"F_RR_FIXED_OMEGA={record.f_rr_fixed_omega:+.15e} "
            f"CHARGE_CONSTRAINT_CORRECTION={record.correction:+.15e} "
            f"E_RR_FIXED_Q={record.e_rr_fixed_charge:+.15e} "
            f"Q_R_PHI={record.q_r_phi:+.15e} "
            f"Q_R_SIGMA={record.q_r_sigma:+.15e} "
            f"QOMEGA_MIN_EIG={record.qomega_min_eigenvalue:+.15e} "
            f"QOMEGA_CONDITION={record.susceptibility_condition:.6e} "
            f"QOMEGA_ASYMMETRY={record.susceptibility_asymmetry:.6e}"
        )

    radial_curvatures = [r.e_rr_fixed_charge for r in radial_records]
    radial_spread = relative_spread(radial_curvatures)

    susceptibility_pass = all(
        r.qomega_min_eigenvalue > 0.0
        and r.susceptibility_condition <= MAX_SUSCEPTIBILITY_CONDITION
        and r.susceptibility_asymmetry <= MAX_SUSCEPTIBILITY_ASYMMETRY
        for r in radial_records
    )

    radial_pass = bool(
        susceptibility_pass
        and all(value >= MIN_POSITIVE_RADIAL_CURVATURE for value in radial_curvatures)
        and radial_spread <= MAX_RADIAL_CURVATURE_REL_SPREAD
    )

    print(f"FIXED_CHARGE_RADIAL_CURVATURE_REL_SPREAD={radial_spread:.15e}")
    print("CHARGE_SUSCEPTIBILITY_HEALTH=" + ("PASS" if susceptibility_pass else "FAIL"))
    print("FIXED_OMEGA_NEGATIVE_CURVATURE_INTERPRETATION=ENSEMBLE_DEPENDENT")
    print("FIXED_CHARGE_RADIAL_STABILITY=" + ("PASS" if radial_pass else "FAIL"))

    # ------------------------------------------------------------------
    # Part II: field-derived microscopic bending rigidity.
    # ------------------------------------------------------------------
    print("\n=== MICROSCOPIC CURVATURE-RIGIDITY RECONSTRUCTION ===")

    log_records = curvature_actions_from_log(A_LOG)
    fresh_records = recompute_curvature_actions(
        one,
        g2,
        b1b,
        p,
        data,
        artifact,
        R0=R,
        n_phi=n_phi,
        n_sigma=n_sigma,
        omega_phi=float(omega[0]),
        omega_sigma=float(omega[1]),
    )

    fits = rigidity_fits("N41_EXECUTED_018B1A", log_records)
    fits.extend(rigidity_fits("N33_FRESH_018C1", fresh_records))

    for record in fits:
        print(
            f"BENDING_FIT_SOURCE={record.source} "
            f"DEGREE={record.degree} "
            f"B_EFF={record.B:+.15e} "
            f"MAX_ACTION_FIT_RESIDUAL={record.max_fit_residual:.3e}"
        )

    B_values = [record.B for record in fits]
    B_spread = relative_spread(B_values)

    B_min = min(B_values)
    B_max = max(B_values)
    B_range = B_max - B_min

    # Favor stability aggressively: take the largest inferred B and add twice
    # the entire cross-resolution/model-fit range.  If this still fails, the
    # conclusion does not depend on picking the most negative fit.
    B_upper = B_max + 2.0 * B_range

    B_crit_m2 = wall_tension * R**3 / 3.0
    b_upper = B_upper / (wall_tension * R**3)
    required_ratio = B_crit_m2 / max(abs(B_upper), 1.0e-30)

    rigidity_fit_pass = B_spread <= MAX_BENDING_ESTIMATE_REL_SPREAD

    print(f"BENDING_ESTIMATE_REL_SPREAD={B_spread:.15e}")
    print(f"B_EFF_MIN={B_min:+.15e}")
    print(f"B_EFF_MAX={B_max:+.15e}")
    print(f"B_EFF_CONSERVATIVE_UPPER={B_upper:+.15e}")
    print(f"B_CRIT_M2={B_crit_m2:+.15e}")
    print(f"B_UPPER_OVER_SIGMA_R3={b_upper:+.15e}")
    print(f"B_CRIT_OVER_ABS_B_UPPER={required_ratio:.15e}")
    print("MICROSCOPIC_BENDING_FIT_CONVERGENCE=" + ("PASS" if rigidity_fit_pass else "FAIL"))

    # ------------------------------------------------------------------
    # Part III: analytic and independent finite-amplitude shape tests.
    # ------------------------------------------------------------------
    print("\n=== NONAXISYMMETRIC SHAPE SPECTRUM M=2..12 ===")

    mode_coefficients: dict[int, float] = {}
    all_modes_stable = True

    for m in M_MODES:
        coefficient = analytic_shape_coefficient(R, wall_tension, B_upper, m)
        mode_coefficients[m] = coefficient
        stable = coefficient > 0.0
        all_modes_stable = all_modes_stable and stable

        print(
            f"SHAPE_MODE_M={m} "
            f"DELTA_E_OVER_EPS2={coefficient:+.15e} "
            f"STABLE={'YES' if stable else 'NO'}"
        )

    print("\n=== DIRECT FINITE-AMPLITUDE M2 GEOMETRY CHECK ===")

    m2_analytic = mode_coefficients[2]
    agreement_values = []
    finite_all_positive = True

    for epsilon in FINITE_EPSILONS:
        delta = numeric_shape_delta(R, wall_tension, B_upper, 2, epsilon)
        normalized = delta / (epsilon * epsilon)
        ratio = normalized / m2_analytic if abs(m2_analytic) > 0.0 else math.nan
        agreement = 1.0 - abs(ratio - 1.0) if math.isfinite(ratio) else -math.inf
        agreement_values.append(agreement)
        finite_all_positive = finite_all_positive and delta > 0.0

        print(
            f"M2_FINITE_EPSILON={epsilon:.6e} "
            f"DELTA_E={delta:+.15e} "
            f"DELTA_E_OVER_EPS2={normalized:+.15e} "
            f"RATIO_TO_ANALYTIC={ratio:+.15e}"
        )

    shape_quadrature_pass = min(agreement_values) >= MIN_SHAPE_NUMERIC_ANALYTIC_AGREEMENT
    m2_pass = bool(
        rigidity_fit_pass
        and all_modes_stable
        and finite_all_positive
        and shape_quadrature_pass
    )

    print("SHAPE_NUMERIC_ANALYTIC_CROSSCHECK=" + ("PASS" if shape_quadrature_pass else "FAIL"))
    print("M2_ELLIPTIC_MODE=" + ("STABLE" if m2_pass else "UNSTABLE"))
    print("HIGHER_M_LOCAL_SHAPE_MODES=" + ("STABLE" if all_modes_stable else "UNSTABLE_PRESENT"))

    # A large gap is scientifically meaningful even before the direct full m=2
    # Fourier-field eigenproblem.  Report rather than hide it.
    if B_upper <= 0.0:
        margin_class = "WRONG_SIGN"
    elif B_upper < 0.01 * B_crit_m2:
        margin_class = "MORE_THAN_100X_SHORT"
    elif B_upper < B_crit_m2:
        margin_class = "INSUFFICIENT"
    else:
        margin_class = "SUFFICIENT"

    print(f"M2_RIGIDITY_MARGIN_CLASS={margin_class}")

    # ------------------------------------------------------------------
    # Decision logic.
    # ------------------------------------------------------------------
    print("\n=== 018C-1 DECISION ===")

    if radial_pass and m2_pass:
        print("018C1_CHARGE_CONSTRAINED_RADIAL_AND_M2_STABILITY_GATE=GREEN")
        print("AXISYMMETRIC_RADIAL_MODE=STABLE_AT_FIXED_CHARGES")
        print("FIELD_DERIVED_M2_SHAPE_MODE=STABLE")
        print("LOW_M_STABILITY_ESCALATION=AUTHORIZED")
        print("NEXT=018C2_FULL_FOURIER_M0_M1_M2_AND_HIGHER_FIELD_HESSIAN")
        print("CURRENT_HEURISTIC=APPROXIMATELY_69_PERCENT_NOT_A_PROBABILITY")
        print("HEURISTIC_CHANGE=APPROXIMATELY_68_TO_69_PERCENT_PENDING_FULL_018C")
    elif radial_pass and not m2_pass:
        print("018C1_CHARGE_CONSTRAINED_RADIAL_AND_M2_STABILITY_GATE=GREEN_NEGATIVE_RESULT")
        print("AXISYMMETRIC_RADIAL_MODE=STABLE_AT_FIXED_CHARGES")
        print("FIXED_OMEGA_RADIAL_WARNING=RESOLVED_AS_ENSEMBLE_ARTIFACT")
        print("FIELD_DERIVED_M2_SHAPE_MODE=UNSTABLE")
        print("FULL_COMPOSITE_STABILITY=NOT_ESTABLISHED_M2_OBSTRUCTION")
        print("STABLE_FIELD_THEORETICAL_CANDIDATE=NO")
        print("NEXT=018C2_DIRECT_FULL_FIELD_M2_EIGENMODE_CONFIRMATION_BEFORE_BRANCH_DEMOTION")
        print("CURRENT_HEURISTIC=APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY")
        print("HEURISTIC_INCREASE=NO_M2_STABILITY_FALSIFIER")
    else:
        print("018C1_CHARGE_CONSTRAINED_RADIAL_AND_M2_STABILITY_GATE=RED")
        print("AXISYMMETRIC_RADIAL_MODE=UNSTABLE_OR_NUMERICALLY_UNRESOLVED")
        print("FIELD_DERIVED_M2_SHAPE_MODE=" + ("STABLE" if m2_pass else "UNSTABLE"))
        print("FULL_COMPOSITE_STABILITY=NOT_ESTABLISHED")
        print("NEXT=CLASSIFY_018C1_RADIAL_FAILURE_BEFORE_ANY_ESCALATION")
        print("CURRENT_HEURISTIC=APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY")
        print("HEURISTIC_INCREASE=NO")

    print("FIELD_THEORETICAL_CANDIDATE_FROM_018B=RETAINED")
    print("FRAME_DRAGGING=NOT_INCLUDED")
    print("NONLINEAR_EINSTEIN_MATTER=NOT_ESTABLISHED")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018C1_FIXED_CHARGE_RADIAL_AND_MICROSCOPIC_M2_STABILITY_GATE"
    )


if __name__ == "__main__":
    main()
