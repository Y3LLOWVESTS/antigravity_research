#!/usr/bin/env python3
"""018C-2 — direct full-field fixed-charge m=2 Hessian confirmation.

PURPOSE
-------
Perform the single direct full-field nonaxisymmetric confirmation authorized by
018C-1 before the present two-current/KLS wall-rim realization is either
retained or demoted for stability.

018C-1 established that the axisymmetric radius is restoring at fixed Noether
charges, but inferred a very large m=2 instability from a curvature derivative
expansion of the actual 018B microscopic fields.  This file does not reuse the
fitted bending rigidity.  Instead it evaluates the complete microscopic field
energy of a physical m=2 deformation directly.

SCIENTIFIC QUESTION
-------------------
Does the promoted 018B microscopic field configuration possess an admissible
m=2 deformation, tangent to the separately conserved Q_phi and Q_sigma charge
surface, whose second energy variation is negative?

If yes, the Rayleigh-Ritz principle proves that the constrained Hessian has a
negative eigenvalue.  In the selected canonical scalar/gauge matter model the
kinetic metric is positive, so this is the static spectral signature of a
growing mode.  A complete enormous 3D Hessian diagonalization is unnecessary
to prove existence of at least one unstable mode.

If the direct sign is nonnegative or numerically unresolved, 018C-1's local
rigidity reduction is not independently confirmed and the branch must remain
open for a broader Fourier-sector Hessian calculation.

PHYSICAL m=2 DEFORMATION
------------------------
The boundary of the wall disk and its attached vortex ring is deformed as

    r_b(varphi) = R [1 + epsilon cos(2 varphi)].

Crucially, the microscopic string cross-section is transported in the LOCAL
NORMAL direction of this deformed planar curve rather than merely shifted in
the cylindrical-r direction.  This is the low-energy physical shape mode.

Let s be arclength along the deformed rim and x the outward Frenet-normal
coordinate.  For a planar curve with positive outward-normal convention, the
local tubular metric is

    dl^2 = dz^2 + dx^2 + [1 + kappa x]^2 ds^2.

Using the polar angle varphi as parameter, define

    ell(varphi) = ds/dvarphi

and therefore

    sqrt(g) = ell(varphi) [1 + kappa(varphi) x].

For

    r = r_b(varphi),

    r' = dr/dvarphi,

    r'' = d^2r/dvarphi^2,

the exact planar geometry is

    ell = sqrt(r^2 + r'^2),

    kappa = [r^2 + 2 r'^2 - r r''] / [r^2 + r'^2]^(3/2).

At epsilon=0 this reduces to

    ell = R,
    kappa = 1/R,

and the tubular Jacobian becomes R+x, exactly reproducing the cylindrical
measure used by 018B-1B.

MICROSCOPIC FIELD ENERGY
------------------------
The full promoted cross-sectional fields H, Phi, Sigma, A and the meridional
gauge field are pulled back unchanged in local (x,z) coordinates.  This is an
admissible trial configuration; internal relaxation could only lower its
energy further.

The two current carriers retain their exact integer phases

    Phi   = phi(x,z) exp[i(theta_phi(t) + N_phi varphi)],
    Sigma = sigma(x,z) exp[i(theta_sigma(t) + N_sigma varphi)].

Their tangent-gradient energy is therefore evaluated with the exact deformed
metric factor

    N_i^2 / [ell^2 (1 + kappa x)^2].

All transverse scalar and gauge terms use the actual solved microscopic field
arrays.  No thin-string or fitted-rigidity approximation enters the decision.

EXACT FIXED-CHARGE IMPLEMENTATION
---------------------------------
For each shape define the global carrier norms

    I_i(epsilon)
      = integral sqrt(g) |psi_i|^2 dvarphi dx dz.

The code enforces the separately conserved promoted charges exactly through

    omega_i(epsilon) = Q_i / I_i(epsilon).

The azimuthal phases retain theta_i = N_i varphi throughout the trial.  Hence
each carrier also retains its canonical axial angular momentum J_i = N_i Q_i
while preserving the exact integer winding.  The trial therefore does not
obtain a spurious negative direction by borrowing angular momentum from an
external reservoir.

The temporal kinetic contribution is then

    E_time,i = Q_i^2 / [2 I_i(epsilon)].

This is the finite-amplitude fixed-charge Legendre transform, not a
fixed-frequency surrogate.

GLOBAL MULTIPATCH ACCOUNTING
----------------------------
Use exactly the 018B-1B decomposition

    global = exact planar wall disk
             + large continuum reference-tail correction
             + promoted curved-patch correction
             - same-grid reference-patch correction.

For the deformed wall, the exact enclosed planar area is

    A = 1/2 integral r_b(varphi)^2 dvarphi.

Two large tail boxes are compared.  This preserves all mandatory wall, carrier,
gauge and junction energy already present in the promoted field model and
avoids double counting the wall disk.

SECOND VARIATION
----------------
For each epsilon calculate

    C_2(epsilon)
      = [E(+epsilon) + E(-epsilon) - 2E(0)] / [2 epsilon^2].

A controlled negative value proves a negative direction of the fixed-charge
Hessian.  By Rayleigh-Ritz,

    lambda_min(H_Q) < 0.

NUMERICAL INDEPENDENCE
----------------------
The gate requires agreement across:

- independently re-relaxed N=33 and N=41 microscopic fields;
- epsilon = 1e-4, 3e-4, 1e-3;
- periodic trapezoid and Gauss-Legendre integration over varphi;
- both 018B-1B reference-tail boxes;
- exact epsilon=0 reproduction of the axisymmetric global energy and charges;
- explicit frequency shifts required to hold Q_phi,Q_sigma fixed.

STOP RULE
---------
A robust negative result is the one direct confirmation allowed by 018C-1.
If confirmed, demote the present two-current/KLS wall-rim architecture for full
stability and rerank.  Do not invent an arbitrary rigidity term to preserve
sunk effort.

A nonnegative or numerically unresolved result does not prove full stability.
It only falsifies the 018C-1 m=2 obstruction and authorizes a broader explicit
Fourier Hessian.

APPROXIMATION / CLAIM LIMITS
----------------------------
Flat-spacetime matter-field stability only.  No metric perturbations, frame
dragging, nonlinear Einstein equations, payload backreaction, experiment, or
practical engineering are established here.

A stability failure does not erase 018B's existence result or its linearized-GR
outward finite-payload field.  It means this specific realization is not a
stable field-theoretical candidate.

RELATED FILES
-------------
simulations/018c1_charge_constrained_radial_and_m2_stability_gate.py
simulations/018b1b_global_multipatch_tmunu_gravity_conservation_closeout.py
simulations/018b1a_global_toroidal_curvature_continuation.py
results/data/018b1b_global_field_theoretical_candidate.npz
RESEARCH_BUILDPLAN.md section 018C

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018C2_DIRECT_FULL_FIELD_M2_CONSTRAINED_HESSIAN_CONFIRMATION
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

G2_SOURCE = ROOT / "simulations/018b0g2_fully_coupled_two_current_matched_2d_junction.py"
A_SOURCE = ROOT / "simulations/018b1a_global_toroidal_curvature_continuation.py"
B_SOURCE = ROOT / "simulations/018b1b_global_multipatch_tmunu_gravity_conservation_closeout.py"
C1_SOURCE = ROOT / "simulations/018c1_charge_constrained_radial_and_m2_stability_gate.py"

B_LOG = ROOT / "results/logs/018b1b_global_multipatch_tmunu_gravity_conservation_closeout.log"
C1_LOG = ROOT / "results/logs/018c1_charge_constrained_radial_and_m2_stability_gate.log"
B_ARTIFACT = ROOT / "results/data/018b1b_global_field_theoretical_candidate.npz"

MODE = 2
FIELD_RESOLUTIONS = (33, 41)
BOX_HALF = 12.0
EPSILONS = (1.0e-4, 3.0e-4, 1.0e-3)
TRAPEZOID_NPHI = 256
GAUSS_NPHI = 128

MAX_FIELD_GRADIENT_RMS = 3.0e-6
MAX_FIELD_GRADIENT_MAX = 3.0e-5
MAX_BASELINE_ENERGY_RELERR = 5.0e-3
MAX_BASELINE_CHARGE_RELERR = 5.0e-3
MAX_QUADRATURE_REL_DIFFERENCE = 3.0e-3
MAX_EPSILON_REL_SPREAD = 8.0e-2
MAX_RESOLUTION_REL_SPREAD = 3.0e-1
MAX_TAIL_COEFFICIENT_REL_SHIFT = 8.0e-2
MIN_NEGATIVE_COEFFICIENT_MAGNITUDE = 1.0e2
MAX_REQUIRED_OMEGA_REL_SHIFT = 5.0e-2


@dataclass(frozen=True)
class PatchPieces:
    """Microscopic arrays needed for exact Frenet-tube energy integration."""

    x: np.ndarray
    weights_dx2: np.ndarray
    static_delta: np.ndarray
    phi2: np.ndarray
    sigma2: np.ndarray
    phase_numerator: np.ndarray


@dataclass(frozen=True)
class GeometryIntegral:
    """Global shape quantities before the fixed-charge temporal contribution."""

    static_plus_phase: float
    i_phi: float
    i_sigma: float


@dataclass(frozen=True)
class ShapeValue:
    """Fixed-charge energy and adjusted carrier frequencies for one amplitude."""

    energy: float
    omega_phi: float
    omega_sigma: float
    i_phi: float
    i_sigma: float


@dataclass
class ResolutionRecord:
    """One resolution's full-field direct m=2 diagnostics."""

    n: int
    gradient_rms: float
    gradient_max: float
    baseline_energy_relerr: float
    baseline_q_phi_relerr: float
    baseline_q_sigma_relerr: float
    coefficient_trap: list[float]
    coefficient_gauss: list[float]
    quadrature_relerr: list[float]
    omega_phi_shift: list[float]
    omega_sigma_shift: list[float]


def sha256(path: Path) -> str:
    """Return SHA-256 for one source/artifact."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path):
    """Import one repository simulation without invoking main()."""

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def require_marker(path: Path, marker: str) -> None:
    """Require one exact upstream scientific decision marker."""

    if not path.exists():
        raise RuntimeError(f"Missing upstream log: {path}")
    if marker not in path.read_text(errors="replace"):
        raise RuntimeError(f"Missing marker {marker!r} in {path}")


def load_artifact(path: Path) -> dict[str, np.ndarray]:
    """Load the promoted 018B field artifact."""

    if not path.exists():
        raise RuntimeError(f"Missing promoted field artifact: {path}")
    with np.load(path) as payload:
        return {key: np.array(payload[key]) for key in payload.files}


def relative_difference(a: float, b: float) -> float:
    """Symmetric relative difference."""

    return abs(a - b) / max(abs(a), abs(b), 1.0e-30)


def relative_spread(values) -> float:
    """Full spread relative to median absolute magnitude."""

    values = np.asarray(values, dtype=float)
    center = float(np.median(values))
    return float((np.max(values) - np.min(values)) / max(abs(center), 1.0e-30))


def polar_geometry(R: float, epsilon: float, varphi: float):
    """Return boundary radius, ds/dphi and positive circle-limit curvature."""

    c = math.cos(MODE * varphi)
    s = math.sin(MODE * varphi)

    radius = R * (1.0 + epsilon * c)
    first = -R * epsilon * MODE * s
    second = -R * epsilon * MODE * MODE * c

    ell = math.sqrt(radius * radius + first * first)
    curvature = (
        radius * radius
        + 2.0 * first * first
        - radius * second
    ) / (ell**3)

    return radius, ell, curvature


def patch_pieces(b1b, g2, p, data, problem, fields) -> PatchPieces:
    """Separate the full microscopic energy into tubular-geometry pieces."""

    h, phi, sigma, a, ax, az = fields
    dx = float(problem.dx)

    H = h * problem.phase
    Dhr, Dhz = b1b.covariant_node_derivatives(H, ax, az, 2.0, dx)
    Dar, Daz = b1b.covariant_node_derivatives(a, ax, az, 1.0, dx)

    dphi_x, dphi_z = np.gradient(phi, dx, dx, edge_order=2)
    dsigma_x, dsigma_z = np.gradient(sigma, dx, dx, edge_order=2)

    B = b1b.cell_B_to_nodes(ax, az, p.g_x, dx)
    V = b1b.static_potential(g2, p, problem, h, phi, sigma, a)

    # Exclude BOTH temporal and tangential carrier kinetic terms.  They are
    # reinserted globally after imposing exact fixed Q and deformed geometry.
    static_density = (
        0.5 * (np.abs(Dhr) ** 2 + np.abs(Dhz) ** 2)
        + 0.5 * (
            dphi_x**2
            + dphi_z**2
            + dsigma_x**2
            + dsigma_z**2
        )
        + np.abs(Dar) ** 2
        + np.abs(Daz) ** 2
        + 0.5 * B**2
        + V
    )

    baseline = b1b.baseline_stress_on_problem(g2, data, problem)

    return PatchPieces(
        x=np.array(problem.X, dtype=float),
        weights_dx2=np.array(problem.node_weights, dtype=float) * dx * dx,
        static_delta=np.array(static_density - baseline.rho, dtype=float),
        phi2=np.array(phi * phi, dtype=float),
        sigma2=np.array(sigma * sigma, dtype=float),
        phase_numerator=np.array(
            problem.n_phi**2 * phi**2 + problem.n_sigma**2 * sigma**2,
            dtype=float,
        ),
    )


def integrate_patch_geometry(
    pieces: PatchPieces,
    *,
    ell: float,
    curvature: float,
) -> tuple[float, float, float]:
    """Integrate one defect patch at one azimuth in exact tubular geometry."""

    tube = 1.0 + curvature * pieces.x
    if np.min(tube) <= 0.0:
        raise RuntimeError("Frenet tubular coordinate reached a focal singularity")

    jacobian = ell * tube

    static = float(np.sum(pieces.weights_dx2 * jacobian * pieces.static_delta))

    # Tangential phase energy: J * (1/2) N^2 psi^2 / [ell^2 tube^2].
    phase = float(
        np.sum(
            pieces.weights_dx2
            * 0.5
            * pieces.phase_numerator
            / (ell * tube)
        )
    )

    i_phi = float(np.sum(pieces.weights_dx2 * jacobian * pieces.phi2))
    i_sigma = float(np.sum(pieces.weights_dx2 * jacobian * pieces.sigma2))

    return static + phase, i_phi, i_sigma


def azimuthal_rule(kind: str):
    """Return independent trapezoid or Gauss-Legendre azimuthal quadrature."""

    if kind == "trap":
        nodes = 2.0 * math.pi * np.arange(TRAPEZOID_NPHI) / TRAPEZOID_NPHI
        weights = np.full(TRAPEZOID_NPHI, 2.0 * math.pi / TRAPEZOID_NPHI)
        return nodes, weights

    if kind == "gauss":
        nodes, weights = np.polynomial.legendre.leggauss(GAUSS_NPHI)
        return math.pi * (nodes + 1.0), math.pi * weights

    raise ValueError(kind)


def geometry_integral(
    *,
    epsilon: float,
    R: float,
    wall_energy_per_area: float,
    tail: PatchPieces,
    actual: PatchPieces,
    reference_patch: PatchPieces,
    quadrature: str,
) -> GeometryIntegral:
    """Assemble wall + full multipatch spatial/tangential energy and norms."""

    nodes, weights = azimuthal_rule(quadrature)

    energy = 0.0
    i_phi = 0.0
    i_sigma = 0.0
    wall_area = 0.0

    for varphi, weight in zip(nodes, weights):
        radius, ell, curvature = polar_geometry(R, epsilon, float(varphi))
        wall_area += float(weight) * 0.5 * radius * radius

        et, qpt, qst = integrate_patch_geometry(tail, ell=ell, curvature=curvature)
        ea, qpa, qsa = integrate_patch_geometry(actual, ell=ell, curvature=curvature)
        er, qpr, qsr = integrate_patch_geometry(
            reference_patch,
            ell=ell,
            curvature=curvature,
        )

        energy += float(weight) * (et + ea - er)
        i_phi += float(weight) * (qpt + qpa - qpr)
        i_sigma += float(weight) * (qst + qsa - qsr)

    energy += wall_energy_per_area * wall_area

    return GeometryIntegral(
        static_plus_phase=float(energy),
        i_phi=float(i_phi),
        i_sigma=float(i_sigma),
    )


def fixed_charge_value(
    geometry: GeometryIntegral,
    *,
    q_phi: float,
    q_sigma: float,
) -> ShapeValue:
    """Insert the exact two-charge Legendre transform for one deformed shape."""

    if geometry.i_phi <= 0.0 or geometry.i_sigma <= 0.0:
        raise RuntimeError("Nonpositive carrier norm in deformed configuration")

    omega_phi = q_phi / geometry.i_phi
    omega_sigma = q_sigma / geometry.i_sigma

    temporal = (
        0.5 * q_phi * q_phi / geometry.i_phi
        + 0.5 * q_sigma * q_sigma / geometry.i_sigma
    )

    return ShapeValue(
        energy=float(geometry.static_plus_phase + temporal),
        omega_phi=float(omega_phi),
        omega_sigma=float(omega_sigma),
        i_phi=float(geometry.i_phi),
        i_sigma=float(geometry.i_sigma),
    )


def symmetric_coefficient(center: float, plus: float, minus: float, epsilon: float) -> float:
    """Return C in E=E0+C epsilon^2+O(epsilon^4)."""

    return (plus + minus - 2.0 * center) / (2.0 * epsilon * epsilon)


def build_reference_pieces(
    one,
    b1b,
    g2,
    p,
    data,
    *,
    R,
    n_phi,
    n_sigma,
    omega_phi,
    omega_sigma,
    n,
    box_half,
):
    """Build straight-reference fields and their direct geometry pieces."""

    problem = one.build_problem(
        g2,
        p,
        data,
        R=R,
        n_phi=n_phi,
        n_sigma=n_sigma,
        omega_phi=omega_phi,
        omega_sigma=omega_sigma,
        n=n,
        box_half=box_half,
        blend_factor=one.PRIMARY_BLEND_FACTOR,
    )
    fields = b1b.fields_from_problem(problem)
    return patch_pieces(b1b, g2, p, data, problem, fields)


def evaluate_resolution(
    one,
    b1b,
    g2,
    p,
    data,
    wall_per_area,
    artifact,
    *,
    n: int,
    tail_case,
) -> ResolutionRecord:
    """Re-solve one field resolution and directly evaluate the m=2 Hessian path."""

    R = float(artifact["R"])
    n_phi = int(artifact["n_phi"])
    n_sigma = int(artifact["n_sigma"])
    omega_phi0 = float(artifact["omega_phi"])
    omega_sigma0 = float(artifact["omega_sigma"])

    result = b1b.build_and_solve(
        one,
        g2,
        p,
        data,
        R=R,
        n_phi=n_phi,
        n_sigma=n_sigma,
        omega_phi=omega_phi0,
        omega_sigma=omega_sigma0,
        n=n,
        box_half=BOX_HALF,
        artifact=artifact,
    )

    if not result.optimizer_success:
        raise RuntimeError(f"N={n} re-solve did not converge")
    if result.gradient_rms > MAX_FIELD_GRADIENT_RMS or result.gradient_max > MAX_FIELD_GRADIENT_MAX:
        raise RuntimeError(
            f"N={n} field residual too large: rms={result.gradient_rms} max={result.gradient_max}"
        )

    actual = patch_pieces(
        b1b,
        g2,
        p,
        data,
        result.problem,
        b1b.fields_from_result(result),
    )

    reference_patch = build_reference_pieces(
        one,
        b1b,
        g2,
        p,
        data,
        R=R,
        n_phi=n_phi,
        n_sigma=n_sigma,
        omega_phi=omega_phi0,
        omega_sigma=omega_sigma0,
        n=n,
        box_half=BOX_HALF,
    )

    tail_n, tail_L = tail_case
    tail = build_reference_pieces(
        one,
        b1b,
        g2,
        p,
        data,
        R=R,
        n_phi=n_phi,
        n_sigma=n_sigma,
        omega_phi=omega_phi0,
        omega_sigma=omega_sigma0,
        n=tail_n,
        box_half=tail_L,
    )

    direct_global = b1b.global_from_result(
        one,
        g2,
        p,
        data,
        wall_per_area,
        result,
        h_over_r=0.17,
        tail_case=tail_case,
    )

    center_geometry_trap = geometry_integral(
        epsilon=0.0,
        R=R,
        wall_energy_per_area=wall_per_area.energy,
        tail=tail,
        actual=actual,
        reference_patch=reference_patch,
        quadrature="trap",
    )
    center_geometry_gauss = geometry_integral(
        epsilon=0.0,
        R=R,
        wall_energy_per_area=wall_per_area.energy,
        tail=tail,
        actual=actual,
        reference_patch=reference_patch,
        quadrature="gauss",
    )

    # Each discretization is tested at its own exactly reconstructed charges.
    # These converge to the promoted continuum charges and make omega_i at
    # epsilon=0 exactly the solved frequencies.
    q_phi = omega_phi0 * center_geometry_gauss.i_phi
    q_sigma = omega_sigma0 * center_geometry_gauss.i_sigma

    center_trap = fixed_charge_value(
        center_geometry_trap,
        q_phi=q_phi,
        q_sigma=q_sigma,
    )
    center_gauss = fixed_charge_value(
        center_geometry_gauss,
        q_phi=q_phi,
        q_sigma=q_sigma,
    )

    baseline_energy_relerr = max(
        relative_difference(center_trap.energy, direct_global.ledger.energy),
        relative_difference(center_gauss.energy, direct_global.ledger.energy),
    )
    baseline_q_phi_relerr = relative_difference(q_phi, direct_global.ledger.q_phi_charge)
    baseline_q_sigma_relerr = relative_difference(q_sigma, direct_global.ledger.q_sigma_charge)

    coeff_trap: list[float] = []
    coeff_gauss: list[float] = []
    quadrature_relerr: list[float] = []
    omega_phi_shift: list[float] = []
    omega_sigma_shift: list[float] = []

    for epsilon in EPSILONS:
        route = {}

        for quadrature, center in (("trap", center_trap), ("gauss", center_gauss)):
            plus_geometry = geometry_integral(
                epsilon=+epsilon,
                R=R,
                wall_energy_per_area=wall_per_area.energy,
                tail=tail,
                actual=actual,
                reference_patch=reference_patch,
                quadrature=quadrature,
            )
            minus_geometry = geometry_integral(
                epsilon=-epsilon,
                R=R,
                wall_energy_per_area=wall_per_area.energy,
                tail=tail,
                actual=actual,
                reference_patch=reference_patch,
                quadrature=quadrature,
            )

            plus = fixed_charge_value(plus_geometry, q_phi=q_phi, q_sigma=q_sigma)
            minus = fixed_charge_value(minus_geometry, q_phi=q_phi, q_sigma=q_sigma)

            coefficient = symmetric_coefficient(
                center.energy,
                plus.energy,
                minus.energy,
                epsilon,
            )

            op_shift = max(
                relative_difference(plus.omega_phi, omega_phi0),
                relative_difference(minus.omega_phi, omega_phi0),
            )
            os_shift = max(
                relative_difference(plus.omega_sigma, omega_sigma0),
                relative_difference(minus.omega_sigma, omega_sigma0),
            )

            route[quadrature] = (coefficient, op_shift, os_shift)

        ct, opt, ost = route["trap"]
        cg, opg, osg = route["gauss"]

        coeff_trap.append(float(ct))
        coeff_gauss.append(float(cg))
        quadrature_relerr.append(relative_difference(ct, cg))
        omega_phi_shift.append(max(opt, opg))
        omega_sigma_shift.append(max(ost, osg))

        print(
            f"FULL_FIELD_M2_N={n} "
            f"TAIL={tail_n}x{tail_L:.0f} "
            f"EPS={epsilon:.6e} "
            f"C_TRAP={ct:+.15e} "
            f"C_GAUSS={cg:+.15e} "
            f"QUAD_RELERR={quadrature_relerr[-1]:.3e} "
            f"OMEGA_PHI_REL_SHIFT={omega_phi_shift[-1]:.3e} "
            f"OMEGA_SIGMA_REL_SHIFT={omega_sigma_shift[-1]:.3e}"
        )

    print(
        f"FULL_FIELD_BASELINE_N={n} "
        f"TAIL={tail_n}x{tail_L:.0f} "
        f"GRAD_RMS={result.gradient_rms:.3e} "
        f"GRAD_MAX={result.gradient_max:.3e} "
        f"DIRECT_GLOBAL_E={direct_global.ledger.energy:+.15e} "
        f"FIXED_Q_E0={center_gauss.energy:+.15e} "
        f"ENERGY_RELERR={baseline_energy_relerr:.3e} "
        f"QPHI_RELERR={baseline_q_phi_relerr:.3e} "
        f"QSIGMA_RELERR={baseline_q_sigma_relerr:.3e}"
    )

    return ResolutionRecord(
        n=n,
        gradient_rms=float(result.gradient_rms),
        gradient_max=float(result.gradient_max),
        baseline_energy_relerr=float(baseline_energy_relerr),
        baseline_q_phi_relerr=float(baseline_q_phi_relerr),
        baseline_q_sigma_relerr=float(baseline_q_sigma_relerr),
        coefficient_trap=coeff_trap,
        coefficient_gauss=coeff_gauss,
        quadrature_relerr=quadrature_relerr,
        omega_phi_shift=omega_phi_shift,
        omega_sigma_shift=omega_sigma_shift,
    )


def main() -> None:
    """Run the one authorized direct full-field m=2 confirmation."""

    print("=== 018C-2 — DIRECT FULL-FIELD FIXED-CHARGE M2 HESSIAN CONFIRMATION ===")

    require_marker(B_LOG, "018B1B_GLOBAL_MULTIPATCH_T_MUNU_GRAVITY_CONSERVATION_CLOSEOUT=GREEN")
    require_marker(B_LOG, "FIELD_THEORETICAL_CANDIDATE=YES")
    require_marker(C1_LOG, "018C1_CHARGE_CONSTRAINED_RADIAL_AND_M2_STABILITY_GATE=GREEN_NEGATIVE_RESULT")
    require_marker(C1_LOG, "FIELD_DERIVED_M2_SHAPE_MODE=UNSTABLE")

    for path in (G2_SOURCE, A_SOURCE, B_SOURCE, C1_SOURCE, B_ARTIFACT):
        if not path.exists():
            raise RuntimeError(f"Missing required artifact: {path}")

    print("\n=== UPSTREAM ARTIFACT AUDIT ===")
    print(f"018B0G2_SOURCE_SHA256={sha256(G2_SOURCE)}")
    print(f"018B1A_SOURCE_SHA256={sha256(A_SOURCE)}")
    print(f"018B1B_SOURCE_SHA256={sha256(B_SOURCE)}")
    print(f"018C1_SOURCE_SHA256={sha256(C1_SOURCE)}")
    print(f"018B1B_FIELD_ARTIFACT_SHA256={sha256(B_ARTIFACT)}")

    g2 = load_module("ag018c2_g2", G2_SOURCE)
    one = load_module("ag018c2_1a", A_SOURCE)
    b1b = load_module("ag018c2_1b", B_SOURCE)

    p = g2.load_parameters()
    data = g2.reconstruct_continuum(p)
    wall_per_area = b1b.wall_integrated_per_area(g2, data)
    artifact = load_artifact(B_ARTIFACT)

    print("\n=== PROMOTED 018B STATE ===")
    print(f"R_EQ={float(artifact['R']):.15e}")
    print(f"N_PHI={int(artifact['n_phi'])}")
    print(f"N_SIGMA={int(artifact['n_sigma'])}")
    print(f"OMEGA_PHI={float(artifact['omega_phi']):+.15e}")
    print(f"OMEGA_SIGMA={float(artifact['omega_sigma']):+.15e}")
    print(f"Q_PHI_PROMOTED={float(artifact['noether_q_phi']):+.15e}")
    print(f"Q_SIGMA_PROMOTED={float(artifact['noether_q_sigma']):+.15e}")
    print(f"WALL_ENERGY_PER_AREA={wall_per_area.energy:+.15e}")
    print("M2_CROSS_SECTION_TRANSPORT=FRENET_NORMAL_TUBULAR_COORDINATES")
    print("FIXED_CHARGE_IMPLEMENTATION=EXACT_TWO_CHARGE_LEGENDRE_TRANSFORM")
    print("FITTED_BENDING_RIGIDITY_USED_IN_DECISION=NO")

    print("\n=== DIRECT FULL-FIELD M2 — LARGE-TAIL PRIMARY ===")
    primary_tail = b1b.TAIL_CASES[1]
    records = [
        evaluate_resolution(
            one,
            b1b,
            g2,
            p,
            data,
            wall_per_area,
            artifact,
            n=n,
            tail_case=primary_tail,
        )
        for n in FIELD_RESOLUTIONS
    ]

    print("\n=== REFERENCE-TAIL INDEPENDENCE ===")
    small_tail_record = evaluate_resolution(
        one,
        b1b,
        g2,
        p,
        data,
        wall_per_area,
        artifact,
        n=FIELD_RESOLUTIONS[-1],
        tail_case=b1b.TAIL_CASES[0],
    )

    primary_41 = records[-1]
    tail_shifts = [
        relative_difference(a, b)
        for a, b in zip(primary_41.coefficient_gauss, small_tail_record.coefficient_gauss)
    ]
    max_tail_shift = max(tail_shifts)

    print(f"M2_TAIL_COEFFICIENT_MAX_REL_SHIFT={max_tail_shift:.15e}")
    print("M2_REFERENCE_TAIL_CONVERGENCE=" + (
        "PASS" if max_tail_shift <= MAX_TAIL_COEFFICIENT_REL_SHIFT else "FAIL"
    ))

    print("\n=== FULL-FIELD CONSTRAINED HESSIAN AUDIT ===")
    all_coefficients = []
    epsilon_spreads = []
    max_quad_relerr = 0.0
    max_energy_relerr = 0.0
    max_charge_relerr = 0.0
    max_omega_shift = 0.0

    resolution_means = []

    for record in records:
        merged = [
            0.5 * (a + b)
            for a, b in zip(record.coefficient_trap, record.coefficient_gauss)
        ]
        all_coefficients.extend(merged)
        epsilon_spreads.append(relative_spread(merged))
        resolution_means.append(float(np.mean(merged)))
        max_quad_relerr = max(max_quad_relerr, max(record.quadrature_relerr))
        max_energy_relerr = max(max_energy_relerr, record.baseline_energy_relerr)
        max_charge_relerr = max(
            max_charge_relerr,
            record.baseline_q_phi_relerr,
            record.baseline_q_sigma_relerr,
        )
        max_omega_shift = max(
            max_omega_shift,
            max(record.omega_phi_shift),
            max(record.omega_sigma_shift),
        )

    resolution_spread = relative_spread(resolution_means)
    mean_coefficient = float(np.mean(all_coefficients))
    favorable_coefficient = float(max(all_coefficients))
    most_negative = float(min(all_coefficients))

    print(f"M2_FULL_FIELD_MEAN_QUADRATIC_COEFFICIENT={mean_coefficient:+.15e}")
    print(f"M2_FULL_FIELD_MOST_FAVORABLE_COEFFICIENT={favorable_coefficient:+.15e}")
    print(f"M2_FULL_FIELD_MOST_NEGATIVE_COEFFICIENT={most_negative:+.15e}")
    print(f"M2_EPSILON_MAX_REL_SPREAD={max(epsilon_spreads):.15e}")
    print(f"M2_RESOLUTION_REL_SPREAD={resolution_spread:.15e}")
    print(f"M2_QUADRATURE_MAX_RELERR={max_quad_relerr:.15e}")
    print(f"M2_BASELINE_ENERGY_MAX_RELERR={max_energy_relerr:.15e}")
    print(f"M2_BASELINE_CHARGE_MAX_RELERR={max_charge_relerr:.15e}")
    print(f"M2_MAX_REQUIRED_OMEGA_REL_SHIFT={max_omega_shift:.15e}")

    numerical_pass = bool(
        max_energy_relerr <= MAX_BASELINE_ENERGY_RELERR
        and max_charge_relerr <= MAX_BASELINE_CHARGE_RELERR
        and max_quad_relerr <= MAX_QUADRATURE_REL_DIFFERENCE
        and max(epsilon_spreads) <= MAX_EPSILON_REL_SPREAD
        and resolution_spread <= MAX_RESOLUTION_REL_SPREAD
        and max_tail_shift <= MAX_TAIL_COEFFICIENT_REL_SHIFT
        and max_omega_shift <= MAX_REQUIRED_OMEGA_REL_SHIFT
    )

    negative_pass = bool(
        numerical_pass
        and all(value < -MIN_NEGATIVE_COEFFICIENT_MAGNITUDE for value in all_coefficients)
    )
    nonnegative_pass = bool(
        numerical_pass
        and all(value >= 0.0 for value in all_coefficients)
    )

    print("FULL_FIELD_M2_NUMERICAL_CONTROL=" + ("PASS" if numerical_pass else "FAIL"))
    print("FIXED_Q_PHI_Q_SIGMA_ENFORCED=YES_EXACTLY_BY_CONJUGATE_FREQUENCY_ADJUSTMENT")
    print("FIXED_INTEGER_WINDINGS=YES")
    print("FIXED_CARRIER_ANGULAR_MOMENTA=YES_VIA_J_I_EQUALS_N_I_Q_I")

    print("\n=== RAYLEIGH-RITZ DECISION ===")
    if negative_pass:
        print("018C2_DIRECT_FULL_FIELD_M2_HESSIAN_CONFIRMATION=GREEN_NEGATIVE_RESULT")
        print("FULL_FIELD_M2_NEGATIVE_HESSIAN_DIRECTION=CONFIRMED")
        print("CONSTRAINED_HESSIAN_HAS_NEGATIVE_EIGENVALUE=YES_BY_RAYLEIGH_RITZ")
        print("M2_GROWING_MODE_STATIC_SPECTRAL_SIGNATURE=CONFIRMED_WITHIN_SELECTED_MATTER_MODEL")
        print("018C1_EFFECTIVE_RIGIDITY_FALSIFIER=INDEPENDENTLY_CONFIRMED")
        print("AXISYMMETRIC_FIXED_CHARGE_RADIAL_STABILITY=RETAINED_FROM_018C1")
        print("FULL_COMPOSITE_STABILITY=FAIL_M2")
        print("STABLE_FIELD_THEORETICAL_CANDIDATE=NO")
        print("FIELD_THEORETICAL_CANDIDATE_FROM_018B=RETAINED_AS_EXISTENCE_RESULT")
        print("PRESENT_TWO_CURRENT_KLS_WALL_RIM_ARCHITECTURE=DEMOTE_FOR_STABILITY")
        print("ARBITRARY_RIGIDITY_STABILIZER_AUTHORIZED=NO")
        print("NEXT=GLOBAL_RERANK_AFTER_CONFIRMED_018C_M2_INSTABILITY")
        print("CURRENT_HEURISTIC=APPROXIMATELY_68_PERCENT_KNOWLEDGE_MILESTONE_NOT_STABLE_CANDIDATE")
        print("HEURISTIC_CHANGE=NO_FURTHER_PROMOTION_RERANK_REQUIRED")
    elif nonnegative_pass:
        print("018C2_DIRECT_FULL_FIELD_M2_HESSIAN_CONFIRMATION=GREEN_POSITIVE_SURPRISE")
        print("FULL_FIELD_M2_NEGATIVE_HESSIAN_DIRECTION=NOT_FOUND")
        print("018C1_EFFECTIVE_RIGIDITY_FALSIFIER=NOT_CONFIRMED_BY_DIRECT_FULL_FIELD_TEST")
        print("PRESENT_TWO_CURRENT_KLS_WALL_RIM_ARCHITECTURE=RETAIN")
        print("NEXT=018C3_FULL_LOW_M_COUPLED_FOURIER_HESSIAN_SPECTRUM")
        print("CURRENT_HEURISTIC=APPROXIMATELY_69_PERCENT_NOT_A_PROBABILITY")
        print("HEURISTIC_CHANGE=M2_FALSIFIER_CLEARED_NOT_FULL_STABILITY")
    else:
        print("018C2_DIRECT_FULL_FIELD_M2_HESSIAN_CONFIRMATION=RED_NUMERICALLY_UNRESOLVED")
        print("FULL_FIELD_M2_NEGATIVE_HESSIAN_DIRECTION=UNRESOLVED")
        print("PRESENT_TWO_CURRENT_KLS_WALL_RIM_ARCHITECTURE=DO_NOT_DEMOTE_FROM_THIS_RUN_ALONE")
        print("NEXT=REFINE_018C2_NUMERICAL_CONTROL_WITHOUT_CHANGING_PHYSICS")
        print("CURRENT_HEURISTIC=APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY")
        print("HEURISTIC_CHANGE=NONE")

    print("FRAME_DRAGGING=NOT_INCLUDED")
    print("NONLINEAR_EINSTEIN_MATTER=NOT_ESTABLISHED")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018C2_DIRECT_FULL_FIELD_M2_CONSTRAINED_HESSIAN_CONFIRMATION"
    )


if __name__ == "__main__":
    main()
