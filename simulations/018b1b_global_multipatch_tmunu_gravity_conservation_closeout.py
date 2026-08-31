#!/usr/bin/env python3
"""Simulation 018B-1B — global multipatch T_munu / gravity / conservation closeout.

PURPOSE
-------
Attempt the true 018B promotion gate after the GREEN 018B-1A toroidal
curvature continuation.

This simulation does not reuse the 018B-0H source ledger as if it were the
answer.  It loads the actual curved microscopic field artifact produced by
018B-1A, reconstructs the complete flat-spacetime stress-energy tensor of the
curved matter fields, matches that curved rim/junction patch to the independently
solved planar wall and vacuum patches, checks constrained radial stationarity,
and computes the linearized-GR active source and finite-payload acceleration
from the reconstructed curved fields themselves.

ACTIVE SCIENTIFIC QUESTION
--------------------------
Does the actual curved finite-thickness two-current/KLS field configuration
satisfy all requirements needed for 018B FIELD_THEORETICAL_CANDIDATE status:

- its microscopic Euler-Lagrange equations are solved;
- the exact integer windings and Noether charges are finite;
- the complete stress-energy tensor is finite and globally matched;
- the constrained global radius is stationary;
- local stress conservation is numerically controlled;
- total active mass is positive;
- a negative-active region exists with useful kernel leverage;
- the point and finite-payload gravitational response is outward;
- the result survives resolution, boundary/domain, initialization, tail, and
  independent gravity-reconstruction checks?

This is deliberately a fail-closed promotion gate.  A favorable source-level
018B-0H result is not sufficient.

PHYSICAL MODEL
--------------
The curved rim/junction fields are those solved by 018B-1A in cylindrical
coordinates (r,z,varphi):

    H = h(r,z) exp(i theta)

    Phi = phi(r,z) exp[i(omega_phi t + N_phi varphi)]

    Sigma = sigma(r,z) exp[i(omega_sigma t + N_sigma varphi)]

    A = A(r,z)

with the meridional U(1)_X gauge links solved simultaneously.

The current carriers are neutral.  H has charge two and A has charge one under
the same fundamental gauge field.

The physical carrier derivatives are

    k_phi(r) = N_phi / r
    k_sigma(r) = N_sigma / r.

The stationary reduced action solved in 018B-1A is the grand potential

    F = E - omega_phi Q_phi - omega_sigma Q_sigma.

Therefore, after minimizing the fields at fixed omega_i and integer N_i,
stationarity of F with respect to the global ring radius is equivalent by the
Legendre transform/envelope theorem to stationarity of E at fixed Noether
charges and windings.  This file explicitly tests that missing global radius
variation.

COMPLETE STRESS-ENERGY RECONSTRUCTION
-------------------------------------
Use orthonormal cylindrical components

    rho,
    p_r,
    p_z,
    p_varphi,
    T_rz,
    q_varphi = T_{0-hat-varphi}.

For the neutral current carriers define

    tau = omega_phi^2 phi^2 + omega_sigma^2 sigma^2

    kap = (N_phi/r)^2 phi^2 + (N_sigma/r)^2 sigma^2.

Let V_static contain the complete scalar potential but no time/azimuthal
kinetic terms.  Let B_varphi be the meridional gauge magnetic field.

The energy density is

    rho =
        1/2 (|D_r H|^2 + |D_z H|^2)
        + 1/2 (|d_r phi|^2 + |d_z phi|^2)
        + 1/2 (|d_r sigma|^2 + |d_z sigma|^2)
        + |D_r A|^2 + |D_z A|^2
        + 1/2 (tau + kap)
        + 1/2 B_varphi^2
        + V_static.

The active gravitoelectric source for a payload instantaneously at rest is

    S_active = rho + p_r + p_z + p_varphi
             = 2 tau - 2 V_static + B_varphi^2.

This identity is independently checked against the reconstructed diagonal
stress tensor.

The azimuthal momentum density is

    q_varphi =
        omega_phi (N_phi/r) phi^2
        + omega_sigma (N_sigma/r) sigma^2.

The total angular momentum is

    J = 2 pi integral r^2 q_varphi dr dz.

The charged H/A sectors have no explicit time dependence in the selected
ansatz and therefore carry no electric gauge charge.  The global gauge charge
is zero in this ansatz; the meridional magnetic flux is reconstructed
separately.

GLOBAL MULTIPATCH ASSEMBLY
--------------------------
Represent the full field configuration as an exact planar-wall disk baseline
plus a localized toroidal defect correction.

Baseline:

    r < R  : independently solved planar KLS wall
    r > R  : exact vacuum.

The toroidal defect correction is evaluated by a matched-additive procedure:

1. construct the continuum-matched straight-string/wall reference fields on a
   large local (x=r-R,z) tail box;
2. integrate their stress-energy relative to the planar-wall/vacuum baseline;
3. replace the central reference patch by the fully relaxed 018B-1A curved
   solution on exactly the same grid.

Thus for any integrated quantity M,

    M_global = M_wall_disk
               + Delta M_reference_tail
               + (Delta M_curved_patch - Delta M_reference_patch).

The reference-tail box is repeated at two large sizes to verify that the
localized defect correction has converged.  This avoids both double counting
and the false assumption that the 018B-1A local patch itself contains the full
long carrier tails.

GLOBAL RADIUS STATIONARITY
--------------------------
The 018B-0H radius was obtained from a source-level wall-balance equation.  It
cannot automatically be promoted after curvature and microscopic
backreaction.

This file therefore re-solves the coupled target fields at fixed integer
N_phi,N_sigma and fixed omega_phi,omega_sigma for nearby radii and evaluates

    F_global(R) = E_global(R)
                  - omega_phi Q_phi(R)
                  - omega_sigma Q_sigma(R).

A quadratic local fit is used only as a root/refinement device.  Promotion
requires positive curvature, an equilibrium inside the scanned interval, and
a small dimensionless first derivative after a final field solve at the
refined radius.

GRAVITY
-------
At linearized-GR order the outward axial acceleration factor for an on-axis
payload center at z=h is reconstructed directly from S_active:

    F_out =
        -2 pi integral r S_active(r,z)
        (h-z) / [r^2 + (h-z)^2]^(3/2) dr dz.

The planar-wall disk contribution is integrated independently from the wall
BVP.  The toroidal defect correction uses both a node/trapezoid rule and an
independent cell-midpoint rule.

For the finite spherical payload, the source-support clearance is explicitly
checked.  When the payload sphere lies entirely in a source-free region, each
Cartesian acceleration component is harmonic there, so the exact spherical
volume average equals the center value by the mean-value theorem.  This is an
operational finite-payload center-of-mass observable, not a point-payload
substitute.

LOCAL CONSERVATION
------------------
For a stationary axisymmetric source with no r-varphi or z-varphi shear, the
nontrivial spatial conservation equations in orthonormal cylindrical form are

    d_r p_r + d_z T_rz + (p_r-p_varphi)/r = 0

    d_r T_rz + d_z p_z + T_rz/r = 0.

They are reconstructed directly from T_munu on the relaxed curved patch.  The
baseline planar wall separately satisfies its one-dimensional first-integral
identity.  Conservation is checked on successively refined target grids; the
reported residual is not inferred merely from the optimizer gradient.

CONVERGENCE / INDEPENDENT RECONSTRUCTION
----------------------------------------
The promotion gate includes:

- 018B-1A continuation path already GREEN;
- low/primary/high local spatial resolution at the refined radius;
- a larger boundary/domain patch at comparable dx;
- a fresh-initialization solve independent of the continuation artifact;
- two large reference-tail boxes;
- direct T_munu energy versus discrete-action physical-energy reconstruction;
- active-source trace identity;
- node versus cell-midpoint gravity integration;
- direct stress-divergence conservation on multiple resolutions;
- constrained global-radius stationarity.

At minimum require reproduction of:

    FIELD_RESIDUAL
    TOTAL_ENERGY
    ACTIVE_MASS
    FINITE_PAYLOAD_FORCE_SIGN.

UNITS
-----
Dimensionless natural units inherited from 018B-0D through 018B-1A.

The familiar 1g / 1m energy conversion remains only a project scaling
normalization and is not a claim of a realizable laboratory device.

APPROXIMATION LEVEL
-------------------
This is a flat-spacetime matter-field solution plus linearized-GR gravity.

It includes actual cylindrical/toroidal matter curvature and the complete
matter stress tensor within the selected microscopic model.

It does NOT yet include:

- metric backreaction on the matter fields;
- frame dragging from the nonzero angular momentum;
- nonlinear Einstein equations;
- full perturbative/dynamical stability;
- payload backreaction;
- practical formation/control engineering.

Those are later gates even if this file is GREEN.

PROMOTION CONDITION
-------------------
GREEN requires a globally regular finite-energy nonthermal field configuration
satisfying its own curved matter equations, constrained radius stationarity,
controlled conservation/matching/convergence, positive far active mass, and
robust outward finite-payload acceleration from the reconstructed curved
T_munu, with independent reconstruction routes agreeing.

A GREEN result authorizes

    FIELD_THEORETICAL_CANDIDATE

and the project heuristic may move from approximately 66 percent to
approximately 68 percent (still explicitly not a probability).

FALSIFICATION / STOP RULE
-------------------------
If radius stationarity, conservation, total-energy reconstruction, active mass,
finite-payload force sign, convergence, or tail matching fails, do not award
018B and do not proceed to 018C merely because 018B-0H or 018B-1A was GREEN.
Classify the failed global gate first.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018B1B_GLOBAL_MULTIPATCH_T_MUNU_GRAVITY_CONSERVATION_CLOSEOUT
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib.util
import math
from pathlib import Path
import re
import sys

import numpy as np
from scipy.integrate import simpson
from scipy.interpolate import RegularGridInterpolator
from scipy.optimize import minimize_scalar


ROOT = Path(__file__).resolve().parents[1]

D_LOG = ROOT / "results/logs/018b0d_literature_two_current_counterflow_gate.log"
F0_LOG = ROOT / "results/logs/018b0f0_lilley_kls_same_gauge_normalization_wall_bridge.log"
G2_LOG = ROOT / "results/logs/018b0g2_fully_coupled_two_current_matched_2d_junction.log"
H_LOG = ROOT / "results/logs/018b0h_complete_source_gravity_revalidation.log"
A_LOG = ROOT / "results/logs/018b1a_global_toroidal_curvature_continuation.log"

A_SOURCE = ROOT / "simulations/018b1a_global_toroidal_curvature_continuation.py"
G2_SOURCE = ROOT / "simulations/018b0g2_fully_coupled_two_current_matched_2d_junction.py"
A_ARTIFACT = ROOT / "results/data/018b1a_global_toroidal_curvature_target.npz"

OUTPUT_NPZ = ROOT / "results/data/018b1b_global_field_theoretical_candidate.npz"

# Promotion-grade convergence suite.
RESOLUTION_CASES = (
    (33, 12.0),
    (41, 12.0),
    (49, 12.0),
)

DOMAIN_CASE = (51, 15.0)

# Large boxes used only for the inexpensive continuum-matched tail correction.
TAIL_CASES = (
    (161, 80.0),
    (241, 120.0),
)

# Global constrained-radius scan.  Integer windings and omega_i remain fixed.
RADIUS_SCAN_FACTORS = (
    0.9975,
    0.9990,
    1.0000,
    1.0010,
    1.0025,
)

RADIUS_SCAN_N = 33
RADIUS_SCAN_L = 12.0

# Payload geometry inherited from the source-level program.
PAYLOAD_RADIUS_OVER_H = 0.25

# Numerical promotion thresholds.  They are intentionally stricter than the
# earlier source scouts where practical without pretending a dx~0.5 local core
# grid can deliver spectral accuracy in pointwise stress divergence.
MAX_FIELD_GRADIENT_RMS = 3.0e-6
MAX_FIELD_GRADIENT_MAX = 3.0e-5
MAX_MATCHING_MISMATCH = 0.12
MAX_ENERGY_RECONSTRUCTION_RELERR = 3.0e-2
MAX_ACTIVE_IDENTITY_RELERR = 2.0e-10
MAX_GRAVITY_INTEGRATOR_RELERR = 5.0e-3
MAX_TAIL_REL_SHIFT = 1.0e-2
MAX_RESOLUTION_REL_SPREAD = 5.0e-2
MAX_DOMAIN_REL_SHIFT = 5.0e-2
MAX_INITIALIZATION_REL_SHIFT = 5.0e-2
MAX_CONSERVATION_L2 = 1.5e-1
MAX_CONSERVATION_HIGH_TO_LOW_RATIO = 1.25
MIN_RADIUS_CURVATURE = 0.0
MAX_RADIUS_EQUILIBRIUM_SHIFT = 1.5e-2
MAX_RADIUS_STATIONARITY_REL = 1.0e-2
MIN_POSITIVE_ACTIVE_MASS = 0.0
MIN_OUTWARD_FORCE = 0.0
MIN_SOURCE_CLEARANCE_WALL_WIDTHS = 5.0
MIN_PHASE_LOCK_COS = 0.97
MIN_CARRIER_RETENTION = 0.80
MAX_WALL_CONTRAST = 0.20

# Existing validated 018A coefficient for scaling comparison only.
VALIDATED_C = 1.774169582609975e6
VALIDATED_ENERGY_1G_1M = 2.342887778715687e34

# Blind wildcard diagnostics only.  These are never promotion criteria.
WILDCARD_HEIGHT_FACTORS = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)


@dataclass
class StressFields:
    """Pointwise orthonormal cylindrical stress-energy reconstruction."""

    rho: np.ndarray
    p_r: np.ndarray
    p_z: np.ndarray
    p_phi: np.ndarray
    t_rz: np.ndarray
    q_phi: np.ndarray
    active: np.ndarray
    active_from_trace: np.ndarray
    V_static: np.ndarray
    B_phi: np.ndarray


@dataclass
class Integrated:
    """Integrated source ledger in model units."""

    energy: float = 0.0
    p_r: float = 0.0
    p_z: float = 0.0
    p_phi: float = 0.0
    t_rz: float = 0.0
    active: float = 0.0
    q_phi_charge: float = 0.0
    q_sigma_charge: float = 0.0
    angular_momentum: float = 0.0

    def __add__(self, other: "Integrated") -> "Integrated":
        return Integrated(
            energy=self.energy + other.energy,
            p_r=self.p_r + other.p_r,
            p_z=self.p_z + other.p_z,
            p_phi=self.p_phi + other.p_phi,
            t_rz=self.t_rz + other.t_rz,
            active=self.active + other.active,
            q_phi_charge=self.q_phi_charge + other.q_phi_charge,
            q_sigma_charge=self.q_sigma_charge + other.q_sigma_charge,
            angular_momentum=self.angular_momentum + other.angular_momentum,
        )

    def __sub__(self, other: "Integrated") -> "Integrated":
        return Integrated(
            energy=self.energy - other.energy,
            p_r=self.p_r - other.p_r,
            p_z=self.p_z - other.p_z,
            p_phi=self.p_phi - other.p_phi,
            t_rz=self.t_rz - other.t_rz,
            active=self.active - other.active,
            q_phi_charge=self.q_phi_charge - other.q_phi_charge,
            q_sigma_charge=self.q_sigma_charge - other.q_sigma_charge,
            angular_momentum=self.angular_momentum - other.angular_momentum,
        )


@dataclass
class GlobalEvaluation:
    """One assembled global multipatch field-state diagnostic."""

    result: object
    ledger: Integrated
    force_node: float
    force_cell: float
    projected_c: float
    h_payload: float
    payload_radius: float
    source_clearance: float
    tail_rel_shift: float
    energy_reconstruction_relerr: float
    active_identity_relerr: float
    conservation_l2: float
    min_active_density: float
    negative_active_present: bool
    global_flux_over_pi: float
    grand_potential: float


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


def require_marker(path: Path, marker: str) -> None:
    """Require one exact upstream GREEN marker."""

    if not path.exists():
        raise RuntimeError(f"Missing upstream artifact: {path}")

    text = path.read_text(errors="replace")

    if marker not in text:
        raise RuntimeError(f"Missing upstream marker {marker!r} in {path}")


def scalar(path: Path, label: str) -> float:
    """Read one finite floating scalar following an exact label."""

    text = path.read_text(errors="replace")
    number = r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
    match = re.search(re.escape(label) + number, text)

    if match is None:
        raise RuntimeError(f"Missing {label!r} in {path}")

    value = float(match.group(1))

    if not math.isfinite(value):
        raise RuntimeError(f"Nonfinite {label!r} in {path}")

    return value


def source_sha256(path: Path) -> str:
    """Return SHA-256 of one executed source artifact."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact_arrays(path: Path) -> dict[str, np.ndarray]:
    """Load the complete 018B-1A target field artifact."""

    if not path.exists():
        raise RuntimeError(f"Missing 018B-1A field artifact: {path}")

    with np.load(path) as payload:
        return {key: np.array(payload[key]) for key in payload.files}


def interpolate_array(old_x, old_z, values, new_x, new_z):
    """Interpolate one node-centered scalar array with no extrapolation."""

    interpolator = RegularGridInterpolator(
        (old_x, old_z),
        values,
        bounds_error=False,
        fill_value=np.nan,
    )

    X, Z = np.meshgrid(new_x, new_z, indexing="ij")
    points = np.column_stack((X.ravel(), Z.ravel()))
    return interpolator(points).reshape(X.shape)


def inject_node_field(problem, field_name: str, old_x, old_z, values) -> None:
    """Warm-start one node-centered free field from an older solved grid."""

    target = getattr(problem, field_name)
    free = getattr(problem, field_name.replace("0", "_free")) if field_name.endswith("0") else None

    if field_name == "h0":
        mask = problem.h_free
    elif field_name == "phi0":
        mask = problem.phi_free
    elif field_name == "sigma0":
        mask = problem.sigma_free
    else:
        raise RuntimeError(f"Unsupported real node field {field_name}")

    interpolated = interpolate_array(old_x, old_z, values, problem.x, problem.z)
    good = mask & np.isfinite(interpolated)
    target[good] = interpolated[good]


def inject_complex_a(problem, old_x, old_z, old_a) -> None:
    """Warm-start the complex KLS node field."""

    real = interpolate_array(old_x, old_z, old_a.real, problem.x, problem.z)
    imag = interpolate_array(old_x, old_z, old_a.imag, problem.x, problem.z)
    good = problem.a_free & np.isfinite(real) & np.isfinite(imag)
    problem.a0[good] = real[good] + 1.0j * imag[good]


def inject_link_fields(problem, old_x, old_z, old_ax, old_az) -> None:
    """Warm-start line-integrated meridional gauge links."""

    old_xmid = 0.5 * (old_x[:-1] + old_x[1:])
    old_zmid = 0.5 * (old_z[:-1] + old_z[1:])

    new_xmid = 0.5 * (problem.x[:-1] + problem.x[1:])
    new_zmid = 0.5 * (problem.z[:-1] + problem.z[1:])

    ax_interp = RegularGridInterpolator(
        (old_xmid, old_z),
        old_ax,
        bounds_error=False,
        fill_value=np.nan,
    )

    X, Z = np.meshgrid(new_xmid, problem.z, indexing="ij")
    ax_values = ax_interp(np.column_stack((X.ravel(), Z.ravel()))).reshape(X.shape)
    good = problem.ax_free & np.isfinite(ax_values)
    problem.ax0[good] = ax_values[good]

    az_interp = RegularGridInterpolator(
        (old_x, old_zmid),
        old_az,
        bounds_error=False,
        fill_value=np.nan,
    )

    X, Z = np.meshgrid(problem.x, new_zmid, indexing="ij")
    az_values = az_interp(np.column_stack((X.ravel(), Z.ravel()))).reshape(X.shape)
    good = problem.az_free & np.isfinite(az_values)
    problem.az0[good] = az_values[good]


def inject_artifact(problem, artifact: dict[str, np.ndarray]) -> None:
    """Warm-start a toroidal problem from the saved 018B-1A target fields."""

    old_x = artifact["x"]
    old_z = artifact["z"]

    inject_node_field(problem, "h0", old_x, old_z, artifact["h"])
    inject_node_field(problem, "phi0", old_x, old_z, artifact["phi"])
    inject_node_field(problem, "sigma0", old_x, old_z, artifact["sigma"])

    old_a = artifact["a_real"] + 1.0j * artifact["a_imag"]
    inject_complex_a(problem, old_x, old_z, old_a)
    inject_link_fields(problem, old_x, old_z, artifact["ax"], artifact["az"])


def inject_result(problem, result) -> None:
    """Warm-start a new problem from another solved toroidal result."""

    old_x = result.problem.x
    old_z = result.problem.z

    inject_node_field(problem, "h0", old_x, old_z, result.h)
    inject_node_field(problem, "phi0", old_x, old_z, result.phi)
    inject_node_field(problem, "sigma0", old_x, old_z, result.sigma)
    inject_complex_a(problem, old_x, old_z, result.a)
    inject_link_fields(problem, old_x, old_z, result.ax, result.az)


def build_and_solve(
    one,
    g2,
    p,
    data,
    *,
    R: float,
    n_phi: int,
    n_sigma: int,
    omega_phi: float,
    omega_sigma: float,
    n: int,
    box_half: float,
    artifact: dict[str, np.ndarray] | None = None,
    warm_result=None,
    fresh: bool = False,
):
    """Build and relax one target-radius toroidal field problem."""

    reference = one.build_problem(
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

    if not fresh:
        if warm_result is not None:
            inject_result(problem, warm_result)
        elif artifact is not None:
            inject_artifact(problem, artifact)

    return one.solve_problem(g2, p, problem, reference)


def covariant_node_derivatives(field, ax, az, charge: float, dx: float):
    """Gauge-covariant central derivatives at nodes in the node gauge frame."""

    ux = np.exp(-1.0j * charge * ax)
    uz = np.exp(-1.0j * charge * az)

    d_x = np.zeros_like(field, dtype=complex)
    d_z = np.zeros_like(field, dtype=complex)

    # Interior x derivative: transport both neighbors into the central node's
    # gauge frame before averaging.
    forward = np.conj(ux[1:, :]) * field[2:, :] - field[1:-1, :]
    backward = field[1:-1, :] - ux[:-1, :] * field[:-2, :]
    d_x[1:-1, :] = 0.5 * (forward + backward) / dx

    d_x[0, :] = (np.conj(ux[0, :]) * field[1, :] - field[0, :]) / dx
    d_x[-1, :] = (field[-1, :] - ux[-1, :] * field[-2, :]) / dx

    forward = np.conj(uz[:, 1:]) * field[:, 2:] - field[:, 1:-1]
    backward = field[:, 1:-1] - uz[:, :-1] * field[:, :-2]
    d_z[:, 1:-1] = 0.5 * (forward + backward) / dx

    d_z[:, 0] = (np.conj(uz[:, 0]) * field[:, 1] - field[:, 0]) / dx
    d_z[:, -1] = (field[:, -1] - uz[:, -1] * field[:, -2]) / dx

    return d_x, d_z


def cell_B_to_nodes(ax, az, g_x: float, dx: float) -> np.ndarray:
    """Reconstruct B_varphi on nodes from compact plaquette flux."""

    flux = ax[:, :-1] + az[1:, :] - ax[:, 1:] - az[:-1, :]
    B_cell = flux / (g_x * dx * dx)

    n = ax.shape[1]
    B_node = np.zeros((n, n), dtype=float)
    count = np.zeros((n, n), dtype=float)

    B_node[:-1, :-1] += B_cell
    count[:-1, :-1] += 1.0
    B_node[1:, :-1] += B_cell
    count[1:, :-1] += 1.0
    B_node[:-1, 1:] += B_cell
    count[:-1, 1:] += 1.0
    B_node[1:, 1:] += B_cell
    count[1:, 1:] += 1.0

    return B_node / np.maximum(count, 1.0)


def static_potential(g2, p, problem, h, phi, sigma, a) -> np.ndarray:
    """Complete scalar potential excluding all t/varphi kinetic terms."""

    h2 = h * h
    phi2 = phi * phi
    sigma2 = sigma * sigma
    a2 = np.abs(a) ** 2

    V = (
        g2.LAMBDA_H / 8.0 * (h2 - 1.0) ** 2
        + 0.5 * (p.m_phi_sq + p.f_phi * (h2 - 1.0)) * phi2
        + p.lambda_phi / 4.0 * phi2 * phi2
        + 0.5 * (p.m_sigma_sq + p.f_sigma * (h2 - 1.0)) * sigma2
        + p.lambda_sigma / 4.0 * sigma2 * sigma2
        + p.g_cross / 2.0 * phi2 * sigma2
    )

    H = h * problem.phase

    c_h = g2.H_LOCK * g2.F_A * g2.F_A
    c_a = 2.0 * g2.H_LOCK
    constant = 2.0 * g2.H_LOCK * g2.F_A * g2.F_A

    trilinear = (
        g2.H_LOCK
        * (
            np.conj(H) * a * a
            + H * np.conj(a) * np.conj(a)
        )
    ).real

    V += (
        g2.LAMBDA_A / 4.0 * (a2 - g2.F_A * g2.F_A) ** 2
        - trilinear
        + c_h * (h2 - 1.0)
        + c_a * (a2 - g2.F_A * g2.F_A)
        + constant
    )

    return V


def reconstruct_stress(g2, p, problem, fields) -> StressFields:
    """Reconstruct complete orthonormal cylindrical T_munu on one local grid."""

    h, phi, sigma, a, ax, az = fields
    dx = problem.dx

    H = h * problem.phase
    Dhr, Dhz = covariant_node_derivatives(H, ax, az, 2.0, dx)
    Dar, Daz = covariant_node_derivatives(a, ax, az, 1.0, dx)

    dphi_r, dphi_z = np.gradient(phi, dx, dx, edge_order=2)
    dsigma_r, dsigma_z = np.gradient(sigma, dx, dx, edge_order=2)

    hr2 = np.abs(Dhr) ** 2
    hz2 = np.abs(Dhz) ** 2
    ar2 = np.abs(Dar) ** 2
    az2 = np.abs(Daz) ** 2

    phr2 = dphi_r * dphi_r
    phz2 = dphi_z * dphi_z
    shr2 = dsigma_r * dsigma_r
    shz2 = dsigma_z * dsigma_z

    kphi = problem.n_phi / problem.cylindrical_r
    ksigma = problem.n_sigma / problem.cylindrical_r

    tau = problem.omega_phi**2 * phi**2 + problem.omega_sigma**2 * sigma**2
    kap = kphi**2 * phi**2 + ksigma**2 * sigma**2

    B = cell_B_to_nodes(ax, az, p.g_x, dx)
    B2 = B * B

    V = static_potential(g2, p, problem, h, phi, sigma, a)

    transverse_h = 0.5 * (hr2 + hz2)
    transverse_carrier = 0.5 * (phr2 + phz2 + shr2 + shz2)
    transverse_a = ar2 + az2

    rho = (
        transverse_h
        + transverse_carrier
        + transverse_a
        + 0.5 * (tau + kap)
        + 0.5 * B2
        + V
    )

    p_r = (
        0.5 * (hr2 - hz2)
        + 0.5 * (phr2 - phz2 + shr2 - shz2)
        + (ar2 - az2)
        + 0.5 * (tau - kap)
        + 0.5 * B2
        - V
    )

    p_z = (
        0.5 * (hz2 - hr2)
        + 0.5 * (phz2 - phr2 + shz2 - shr2)
        + (az2 - ar2)
        + 0.5 * (tau - kap)
        + 0.5 * B2
        - V
    )

    p_phi = (
        -transverse_h
        -transverse_carrier
        -transverse_a
        + 0.5 * (tau + kap)
        - 0.5 * B2
        - V
    )

    t_rz = (
        np.real(np.conj(Dhr) * Dhz)
        + dphi_r * dphi_z
        + dsigma_r * dsigma_z
        + 2.0 * np.real(np.conj(Dar) * Daz)
    )

    q_phi = (
        problem.omega_phi * kphi * phi**2
        + problem.omega_sigma * ksigma * sigma**2
    )

    active = 2.0 * tau - 2.0 * V + B2
    active_from_trace = rho + p_r + p_z + p_phi

    return StressFields(
        rho=rho,
        p_r=p_r,
        p_z=p_z,
        p_phi=p_phi,
        t_rz=t_rz,
        q_phi=q_phi,
        active=active,
        active_from_trace=active_from_trace,
        V_static=V,
        B_phi=B,
    )


def wall_profile_arrays(g2, data, z):
    """Return full signed planar-wall fields/derivatives and stress per area."""

    absolute = np.abs(z)
    clipped = np.minimum(absolute, data.wall_half_domain)
    values = data.wall.sol(clipped)

    H = values[0]
    Hp_abs = values[1]
    A_abs = values[2]
    Ap_abs = values[3]

    inside = absolute <= data.wall_half_domain
    sign = np.sign(z)

    Hp = sign * Hp_abs
    Ap = Ap_abs.copy()

    Hp = np.where(inside, Hp, 0.0)
    Ap = np.where(inside, Ap, 0.0)

    H = np.where(inside, H, 1.0)
    A_abs = np.where(inside, A_abs, g2.F_A)

    V = g2.wall_potential(H, A_abs)
    K = 0.5 * Hp * Hp + Ap * Ap

    rho = K + V
    p_r = -rho
    p_phi = -rho
    p_z = K - V
    active = -2.0 * V

    return rho, p_r, p_z, p_phi, active


def baseline_stress_on_problem(g2, data, problem) -> StressFields:
    """Planar-wall/vacuum step baseline evaluated on a toroidal local grid."""

    rho_z, pr_z, pz_z, pp_z, active_z = wall_profile_arrays(g2, data, problem.Z)

    inside = np.where(problem.X < 0.0, 1.0, 0.0)
    inside = np.where(np.abs(problem.X) < 1.0e-14, 0.5, inside)

    zeros = np.zeros_like(problem.X, dtype=float)

    return StressFields(
        rho=inside * rho_z,
        p_r=inside * pr_z,
        p_z=inside * pz_z,
        p_phi=inside * pp_z,
        t_rz=zeros,
        q_phi=zeros,
        active=inside * active_z,
        active_from_trace=inside * active_z,
        V_static=zeros,
        B_phi=zeros,
    )


def integrate_stress(problem, stress: StressFields, phi, sigma) -> Integrated:
    """Axisymmetrically integrate one local stress grid."""

    weight = (
        2.0
        * math.pi
        * problem.cylindrical_r
        * problem.dx
        * problem.dx
        * problem.node_weights
    )

    q_phi_charge_density = problem.omega_phi * phi**2
    q_sigma_charge_density = problem.omega_sigma * sigma**2

    return Integrated(
        energy=float(np.sum(weight * stress.rho)),
        p_r=float(np.sum(weight * stress.p_r)),
        p_z=float(np.sum(weight * stress.p_z)),
        p_phi=float(np.sum(weight * stress.p_phi)),
        t_rz=float(np.sum(weight * stress.t_rz)),
        active=float(np.sum(weight * stress.active)),
        q_phi_charge=float(np.sum(weight * q_phi_charge_density)),
        q_sigma_charge=float(np.sum(weight * q_sigma_charge_density)),
        angular_momentum=float(np.sum(weight * problem.cylindrical_r * stress.q_phi)),
    )


def wall_integrated_per_area(g2, data) -> Integrated:
    """Independently integrate the exact planar wall stress per unit area."""

    z_half = np.linspace(0.0, data.wall_half_domain, 24001)
    H, Hp, A, Ap = data.wall.sol(z_half)

    V = g2.wall_potential(H, A)
    K = 0.5 * Hp * Hp + Ap * Ap

    rho = K + V
    p_parallel = -rho
    p_z = K - V
    active = -2.0 * V

    factor = 2.0

    return Integrated(
        energy=factor * float(simpson(rho, x=z_half)),
        p_r=factor * float(simpson(p_parallel, x=z_half)),
        p_z=factor * float(simpson(p_z, x=z_half)),
        p_phi=factor * float(simpson(p_parallel, x=z_half)),
        active=factor * float(simpson(active, x=z_half)),
    )


def disk_baseline_ledger(wall_per_area: Integrated, R: float) -> Integrated:
    """Multiply the exact wall stress per area by a disk of radius R."""

    area = math.pi * R * R

    return Integrated(
        energy=area * wall_per_area.energy,
        p_r=area * wall_per_area.p_r,
        p_z=area * wall_per_area.p_z,
        p_phi=area * wall_per_area.p_phi,
        active=area * wall_per_area.active,
    )


def fields_from_problem(problem):
    """Return the continuum-matched reference fields stored in a problem."""

    return (
        problem.h0,
        problem.phi0,
        problem.sigma0,
        problem.a0,
        problem.ax0,
        problem.az0,
    )


def fields_from_result(result):
    """Return physical fields from one solved result."""

    return (
        result.h,
        result.phi,
        result.sigma,
        result.a,
        result.ax,
        result.az,
    )


def delta_integral(g2, p, data, problem, fields) -> tuple[Integrated, StressFields, StressFields]:
    """Integrate one local field state relative to the wall/vacuum baseline."""

    stress = reconstruct_stress(g2, p, problem, fields)
    baseline = baseline_stress_on_problem(g2, data, problem)

    phi = fields[1]
    sigma = fields[2]

    full = integrate_stress(problem, stress, phi, sigma)
    base = integrate_stress(
        problem,
        baseline,
        np.zeros_like(phi),
        np.zeros_like(sigma),
    )

    return full - base, stress, baseline


def wall_gravity(g2, data, R: float, h_payload: float) -> float:
    """High-resolution Simpson integration of the exact finite-thickness wall disk."""

    z = np.linspace(-data.wall_half_domain, data.wall_half_domain, 60001)
    _rho, _pr, _pz, _pp, active = wall_profile_arrays(g2, data, z)

    d = h_payload - z
    kernel = 1.0 - d / np.sqrt(R * R + d * d)

    return float(simpson(-2.0 * math.pi * active * kernel, x=z))


def gravity_node(problem, delta_active: np.ndarray, h_payload: float) -> float:
    """Node/trapezoid gravity integral for a local defect active source."""

    d = h_payload - problem.Z
    denom = (problem.cylindrical_r**2 + d * d) ** 1.5

    integrand = (
        -2.0
        * math.pi
        * problem.cylindrical_r
        * delta_active
        * d
        / denom
    )

    return float(
        np.sum(
            integrand
            * problem.dx
            * problem.dx
            * problem.node_weights
        )
    )


def gravity_cell(problem, delta_active: np.ndarray, h_payload: float) -> float:
    """Independent cell-midpoint gravity integral."""

    source = 0.25 * (
        delta_active[:-1, :-1]
        + delta_active[1:, :-1]
        + delta_active[:-1, 1:]
        + delta_active[1:, 1:]
    )

    r = 0.25 * (
        problem.cylindrical_r[:-1, :-1]
        + problem.cylindrical_r[1:, :-1]
        + problem.cylindrical_r[:-1, 1:]
        + problem.cylindrical_r[1:, 1:]
    )

    z = 0.25 * (
        problem.Z[:-1, :-1]
        + problem.Z[1:, :-1]
        + problem.Z[:-1, 1:]
        + problem.Z[1:, 1:]
    )

    d = h_payload - z
    denom = (r * r + d * d) ** 1.5

    return float(
        np.sum(
            -2.0
            * math.pi
            * r
            * source
            * d
            / denom
        )
        * problem.dx
        * problem.dx
    )


def flux_angle(problem) -> float:
    """Return total fundamental gauge-link plaquette angle on one local box."""

    flux = (
        problem.ax0[:, :-1]
        + problem.az0[1:, :]
        - problem.ax0[:, 1:]
        - problem.az0[:-1, :]
    )

    return float(np.sum(flux))


def solved_flux_angle(result) -> float:
    """Return total fundamental flux of one solved curved patch."""

    flux = (
        result.ax[:, :-1]
        + result.az[1:, :]
        - result.ax[:, 1:]
        - result.az[:-1, :]
    )

    return float(np.sum(flux))


def active_identity_error(stress: StressFields) -> float:
    """Check S_active against rho plus the three diagonal pressures."""

    numerator = float(np.linalg.norm(stress.active - stress.active_from_trace))
    denominator = max(float(np.linalg.norm(stress.active)), 1.0e-30)
    return numerator / denominator


def conservation_residual(problem, stress: StressFields) -> float:
    """Directly reconstruct axisymmetric local stress-conservation residual."""

    dx = problem.dx

    d_pr_dr = np.gradient(stress.p_r, dx, axis=0, edge_order=2)
    d_trz_dz = np.gradient(stress.t_rz, dx, axis=1, edge_order=2)

    d_trz_dr = np.gradient(stress.t_rz, dx, axis=0, edge_order=2)
    d_pz_dz = np.gradient(stress.p_z, dx, axis=1, edge_order=2)

    radial = d_pr_dr + d_trz_dz + (stress.p_r - stress.p_phi) / problem.cylindrical_r
    vertical = d_trz_dr + d_pz_dz + stress.t_rz / problem.cylindrical_r

    # Exclude two boundary layers where Dirichlet matching and one-sided
    # differentiation dominate the finite-difference divergence diagnostic.
    sl = np.s_[2:-2, 2:-2]

    residual = np.sqrt(radial[sl] ** 2 + vertical[sl] ** 2)

    scale_stress = (
        np.abs(stress.rho[sl])
        + np.abs(stress.p_r[sl])
        + np.abs(stress.p_z[sl])
        + np.abs(stress.p_phi[sl])
        + 2.0 * np.abs(stress.t_rz[sl])
    )

    # Convert stress/length to a dimensionless residual using the physical
    # microscopic core-width proxy rather than the box size.
    characteristic = max(float(np.sqrt(np.mean(scale_stress**2))), 1.0e-30)
    core_scale = scalar(F0_LOG, "NEW_STRING_GAUGE_CORE_INVERSE_MASS_PROXY=")

    return float(np.sqrt(np.mean(residual**2)) * core_scale / characteristic)


def discrete_patch_physical_energy(one, g2, p, data, result) -> float:
    """Independent physical patch energy from the exact discrete action."""

    problem = result.problem
    vector = one.pack(problem)

    # pack(problem) would contain the initial fields, not the solved result.
    # Recreate a problem copy carrying the solved free fields before evaluating.
    clone = one.build_problem(
        g2,
        p,
        data,
        R=problem.R,
        n_phi=problem.n_phi,
        n_sigma=problem.n_sigma,
        omega_phi=problem.omega_phi,
        omega_sigma=problem.omega_sigma,
        n=problem.n,
        box_half=problem.box_half,
        blend_factor=one.PRIMARY_BLEND_FACTOR,
    )
    inject_result(clone, result)
    vector = one.pack(clone)

    action, _gradient = one.action_and_gradient(g2, p, clone, vector)

    node_weight = (
        clone.dx
        * clone.dx
        * clone.node_weights
        * clone.cylindrical_r
        / clone.R
    )

    carrier_time = float(
        np.sum(
            node_weight
            * (
                clone.omega_phi**2 * result.phi**2
                + clone.omega_sigma**2 * result.sigma**2
            )
        )
    )

    # action is divided by 2*pi*R.  E = F + omega_i Q_i, which here adds
    # exactly integral omega_i^2 amplitude_i^2 to the normalized density.
    return 2.0 * math.pi * clone.R * (action + carrier_time)


def global_from_result(
    one,
    g2,
    p,
    data,
    wall_per_area,
    result,
    *,
    h_over_r: float,
    tail_case,
) -> GlobalEvaluation:
    """Assemble one complete global multipatch ledger and gravity result."""

    problem = result.problem
    R = problem.R
    h_payload = h_over_r * R
    payload_radius = PAYLOAD_RADIUS_OVER_H * h_payload

    # Exact wall-disk baseline.
    wall_disk = disk_baseline_ledger(wall_per_area, R)
    wall_force = wall_gravity(g2, data, R, h_payload)

    # Large continuum-matched reference tail.
    tail_n, tail_L = tail_case
    tail_problem = one.build_problem(
        g2,
        p,
        data,
        R=R,
        n_phi=problem.n_phi,
        n_sigma=problem.n_sigma,
        omega_phi=problem.omega_phi,
        omega_sigma=problem.omega_sigma,
        n=tail_n,
        box_half=tail_L,
        blend_factor=one.PRIMARY_BLEND_FACTOR,
    )

    tail_fields = fields_from_problem(tail_problem)
    tail_delta, tail_stress, tail_baseline = delta_integral(
        g2, p, data, tail_problem, tail_fields
    )

    tail_delta_active = tail_stress.active - tail_baseline.active
    tail_force_node = gravity_node(tail_problem, tail_delta_active, h_payload)
    tail_force_cell = gravity_cell(tail_problem, tail_delta_active, h_payload)

    # Reference patch on exactly the solved local grid.
    ref_problem = one.build_problem(
        g2,
        p,
        data,
        R=R,
        n_phi=problem.n_phi,
        n_sigma=problem.n_sigma,
        omega_phi=problem.omega_phi,
        omega_sigma=problem.omega_sigma,
        n=problem.n,
        box_half=problem.box_half,
        blend_factor=one.PRIMARY_BLEND_FACTOR,
    )

    ref_fields = fields_from_problem(ref_problem)
    ref_delta, ref_stress, ref_baseline = delta_integral(
        g2, p, data, ref_problem, ref_fields
    )

    actual_fields = fields_from_result(result)
    actual_delta, actual_stress, actual_baseline = delta_integral(
        g2, p, data, problem, actual_fields
    )

    ref_delta_active = ref_stress.active - ref_baseline.active
    actual_delta_active = actual_stress.active - actual_baseline.active

    ref_force_node = gravity_node(ref_problem, ref_delta_active, h_payload)
    actual_force_node = gravity_node(problem, actual_delta_active, h_payload)

    ref_force_cell = gravity_cell(ref_problem, ref_delta_active, h_payload)
    actual_force_cell = gravity_cell(problem, actual_delta_active, h_payload)

    ledger = wall_disk + tail_delta + (actual_delta - ref_delta)

    force_node = wall_force + tail_force_node + (actual_force_node - ref_force_node)
    force_cell = wall_force + tail_force_cell + (actual_force_cell - ref_force_cell)

    active_identity_relerr = active_identity_error(actual_stress)
    conservation_l2 = conservation_residual(problem, actual_stress)

    # Compare the physical energy reconstructed from nodal T00 with the exact
    # discrete grand-action/Noether conversion on the actual curved patch.
    actual_patch_integrated = integrate_stress(
        problem, actual_stress, result.phi, result.sigma
    )
    discrete_energy = discrete_patch_physical_energy(one, g2, p, data, result)
    energy_reconstruction_relerr = abs(
        actual_patch_integrated.energy - discrete_energy
    ) / max(abs(discrete_energy), 1.0e-30)

    # The numerical multipatch representation is exactly vacuum outside the
    # independently solved wall half-domain and the finite reference-tail box.
    # Require the complete payload sphere to clear both the wall support in z
    # and the toroidal defect support in cylindrical radius.
    vertical_clearance = (
        h_payload
        - payload_radius
        - data.wall_half_domain
    )

    radial_clearance = (
        R
        - tail_L
        - payload_radius
    )

    source_clearance = min(vertical_clearance, radial_clearance)

    # Complete-source projected coefficient in the same dimensionless project
    # normalization used by the previous source gates.
    # Restoring the physical length scale ell gives
    #
    #   E_phys ~ eps0 ell^3 E_dimless
    #   a      ~ (G/c^2) eps0 ell F_dimless
    #   h      = ell (h/R) R.
    #
    # Eliminating eps0 and ell therefore gives the project mass/energy
    # coefficient proportional to E_dimless / [F_dimless h_dimless^2].
    projected_c = ledger.energy / max(
        force_node * (h_over_r * R) ** 2,
        1.0e-30,
    )

    grand_potential = (
        ledger.energy
        - problem.omega_phi * ledger.q_phi_charge
        - problem.omega_sigma * ledger.q_sigma_charge
    )

    # Tail convergence is filled by the caller after comparing both tail boxes.
    global_flux = (
        flux_angle(tail_problem)
        + solved_flux_angle(result)
        - flux_angle(ref_problem)
    )

    return GlobalEvaluation(
        result=result,
        ledger=ledger,
        force_node=force_node,
        force_cell=force_cell,
        projected_c=projected_c,
        h_payload=h_payload,
        payload_radius=payload_radius,
        source_clearance=source_clearance,
        tail_rel_shift=math.nan,
        energy_reconstruction_relerr=energy_reconstruction_relerr,
        active_identity_relerr=active_identity_relerr,
        conservation_l2=conservation_l2,
        min_active_density=min(
            float(np.min(actual_stress.active)),
            float(np.min(wall_profile_arrays(
                g2,
                data,
                np.linspace(-data.wall_half_domain, data.wall_half_domain, 4001),
            )[4])),
        ),
        negative_active_present=bool(
            np.min(actual_stress.active) < 0.0
            or np.min(wall_profile_arrays(
                g2,
                data,
                np.linspace(-data.wall_half_domain, data.wall_half_domain, 4001),
            )[4]) < 0.0
        ),
        global_flux_over_pi=global_flux / math.pi,
        grand_potential=grand_potential,
    )


def compare_tail_evaluations(a: GlobalEvaluation, b: GlobalEvaluation) -> float:
    """Return worst relative large-tail shift across decisive integrated outputs."""

    pairs = (
        (a.ledger.energy, b.ledger.energy),
        (a.ledger.active, b.ledger.active),
        (a.ledger.q_phi_charge, b.ledger.q_phi_charge),
        (a.ledger.q_sigma_charge, b.ledger.q_sigma_charge),
        (a.force_node, b.force_node),
    )

    shifts = []

    for x, y in pairs:
        shifts.append(abs(x - y) / max(abs(y), abs(x), 1.0e-30))

    return max(shifts)


def evaluate_with_tail_pair(one, g2, p, data, wall_per_area, result, h_over_r):
    """Evaluate both large tail boxes and return the larger-box result."""

    evaluations = [
        global_from_result(
            one,
            g2,
            p,
            data,
            wall_per_area,
            result,
            h_over_r=h_over_r,
            tail_case=case,
        )
        for case in TAIL_CASES
    ]

    shift = compare_tail_evaluations(evaluations[0], evaluations[1])
    evaluations[1].tail_rel_shift = shift
    return evaluations[1], evaluations[0]


def relative_spread(values) -> float:
    """Return max-min spread relative to the median magnitude."""

    values = np.asarray(values, dtype=float)
    center = float(np.median(values))
    return float((np.max(values) - np.min(values)) / max(abs(center), 1.0e-30))


def relative_difference(a: float, b: float) -> float:
    """Symmetric relative difference."""

    return abs(a - b) / max(abs(a), abs(b), 1.0e-30)


def topology_pass(data, result) -> bool:
    """Apply inherited topology plus explicit two-carrier retention gates."""

    phi_retention = (
        result.sigma_phi_normalized
        / max(data.sigma_phi, 1.0e-30)
    )

    sigma_retention = (
        result.sigma_sigma_normalized
        / max(data.sigma_sigma, 1.0e-30)
    )

    return bool(
        result.regularity_pass
        and result.wall_contrast <= MAX_WALL_CONTRAST
        and result.phase_lock_cos >= MIN_PHASE_LOCK_COS
        and phi_retention >= MIN_CARRIER_RETENTION
        and sigma_retention >= MIN_CARRIER_RETENTION
    )


def radius_scan_and_refine(
    one,
    g2,
    p,
    data,
    wall_per_area,
    artifact,
    *,
    R0: float,
    n_phi: int,
    n_sigma: int,
    omega_phi: float,
    omega_sigma: float,
    h_over_r: float,
):
    """Re-solve nearby fixed-winding radii and refine the constrained equilibrium."""

    records = []

    for factor in RADIUS_SCAN_FACTORS:
        R = R0 * factor

        result = build_and_solve(
            one,
            g2,
            p,
            data,
            R=R,
            n_phi=n_phi,
            n_sigma=n_sigma,
            omega_phi=omega_phi,
            omega_sigma=omega_sigma,
            n=RADIUS_SCAN_N,
            box_half=RADIUS_SCAN_L,
            artifact=artifact,
        )

        evaluation = global_from_result(
            one,
            g2,
            p,
            data,
            wall_per_area,
            result,
            h_over_r=h_over_r,
            tail_case=TAIL_CASES[0],
        )

        records.append((factor, R, result, evaluation))

        print(
            f"RADIUS_SCAN_FACTOR={factor:.6f} "
            f"R={R:.12e} "
            f"GRAD_RMS={result.gradient_rms:.3e} "
            f"GRAD_MAX={result.gradient_max:.3e} "
            f"F_GLOBAL={evaluation.grand_potential:+.15e} "
            f"ENERGY={evaluation.ledger.energy:+.15e} "
            f"Q_PHI={evaluation.ledger.q_phi_charge:+.15e} "
            f"Q_SIGMA={evaluation.ledger.q_sigma_charge:+.15e} "
            f"FORCE={evaluation.force_node:+.15e}"
        )

    R_values = np.array([row[1] for row in records], dtype=float)
    F_values = np.array([row[3].grand_potential for row in records], dtype=float)

    # A seven-point local scan is intentionally used because the current-carrying
    # condensates make F(R) measurably non-quadratic even across +/-1 percent.
    # Fit cubic and quartic polynomials in the dimensionless displacement
    # y=(R-R0)/R0 and require their nearest stationary roots to agree.
    y = (R_values - R0) / R0

    roots = []
    curvatures = []

    for degree in (3, 4):
        coefficients = np.polyfit(y, F_values, degree)
        derivative = np.polyder(coefficients)
        second = np.polyder(coefficients, 2)

        candidates = [
            float(root.real)
            for root in np.roots(derivative)
            if abs(root.imag) < 1.0e-9
            and min(y) <= root.real <= max(y)
        ]

        if not candidates:
            continue

        root = min(candidates, key=abs)
        roots.append(root)
        curvatures.append(float(np.polyval(second, root)) / (R0 * R0))

    if len(roots) < 2:
        return records, math.nan, math.nan, math.nan, False

    root_spread = max(roots) - min(roots)
    root_center = float(np.mean(roots))
    R_eq = R0 * (1.0 + root_center)

    # Derivative at the original target from the quartic fit, converted from
    # dF/dy to dF/dR.
    quartic = np.polyfit(y, F_values, 4)
    derivative_at_R0 = float(np.polyval(np.polyder(quartic), 0.0) / R0)
    second_derivative = float(np.mean(curvatures))

    shift = abs(R_eq - R0) / R0
    inside = (
        min(R_values) <= R_eq <= max(R_values)
        and shift <= MAX_RADIUS_EQUILIBRIUM_SHIFT
        and root_spread <= 5.0e-4
    )

    print(f"RADIUS_STATIONARY_ROOT_CUBIC_FACTOR={1.0 + roots[0]:.15e}")
    print(f"RADIUS_STATIONARY_ROOT_QUARTIC_FACTOR={1.0 + roots[1]:.15e}")
    print(f"RADIUS_STATIONARY_ROOT_SPREAD={root_spread:.15e}")

    return records, R_eq, derivative_at_R0, second_derivative, inside


def print_case(label: str, evaluation: GlobalEvaluation) -> None:
    """Print one convergence-case global summary."""

    result = evaluation.result

    print(
        f"{label} "
        f"N={result.problem.n} "
        f"L={result.problem.box_half:.6f} "
        f"DX={result.problem.dx:.9f} "
        f"GRAD_RMS={result.gradient_rms:.3e} "
        f"GRAD_MAX={result.gradient_max:.3e} "
        f"MATCH={result.matching_mismatch:.6e} "
        f"ENERGY={evaluation.ledger.energy:+.15e} "
        f"ACTIVE={evaluation.ledger.active:+.15e} "
        f"FORCE={evaluation.force_node:+.15e} "
        f"C={evaluation.projected_c:.15e} "
        f"CONS_L2={evaluation.conservation_l2:.6e}"
    )


def main() -> None:
    """Execute the true 018B global multipatch promotion closeout."""

    print(
        "=== 018B-1B — GLOBAL MULTIPATCH T_MUNU / GRAVITY / "
        "CONSERVATION CLOSEOUT ==="
    )

    require_marker(D_LOG, "018B0D_TWO_CURRENT_COUNTERFLOW_GATE=GREEN")
    require_marker(F0_LOG, "018B0F0_LILLEY_KLS_NORMALIZATION_WALL_BRIDGE=GREEN")
    require_marker(G2_LOG, "018B0G2_FULLY_COUPLED_TWO_CURRENT_2D_STRING_WALL_JUNCTION=GREEN")
    require_marker(H_LOG, "018B0H_COMPLETE_SOURCE_GRAVITY_REVALIDATION=GREEN")
    require_marker(A_LOG, "018B1A_GLOBAL_TOROIDAL_CURVATURE_CONTINUATION=GREEN")

    if not A_ARTIFACT.exists():
        raise RuntimeError(f"Missing curved target artifact: {A_ARTIFACT}")

    print("\n=== UPSTREAM ARTIFACT AUDIT ===")
    print(f"018B1A_SOURCE_SHA256={source_sha256(A_SOURCE)}")
    print(f"018B1A_TARGET_ARTIFACT_SHA256={source_sha256(A_ARTIFACT)}")

    one = load_module("ag018b1a", A_SOURCE)
    g2 = load_module("ag018b0g2", G2_SOURCE)

    p = g2.load_parameters()
    data = g2.reconstruct_continuum(p)
    wall_per_area = wall_integrated_per_area(g2, data)
    artifact = artifact_arrays(A_ARTIFACT)

    R0 = float(artifact["R"])
    n_phi = int(artifact["n_phi"])
    n_sigma = int(artifact["n_sigma"])
    omega_phi = float(artifact["omega_phi"])
    omega_sigma = float(artifact["omega_sigma"])
    h_over_r = scalar(H_LOG, "SELECTED_H_OVER_R=")

    print("\n=== EXACT GLOBAL QUANTUM-NUMBER LEDGER ===")
    print(f"TARGET_RADIUS_FROM_ARTIFACT={R0:.15e}")
    print(f"GLOBAL_INTEGER_N_PHI={n_phi}")
    print(f"GLOBAL_INTEGER_N_SIGMA={n_sigma}")
    print(f"GLOBAL_OMEGA_PHI={omega_phi:+.15e}")
    print(f"GLOBAL_OMEGA_SIGMA={omega_sigma:+.15e}")
    print(f"GLOBAL_CENTER_K_PHI={n_phi / R0:+.15e}")
    print(f"GLOBAL_CENTER_K_SIGMA={n_sigma / R0:+.15e}")

    # ------------------------------------------------------------------
    # First close the missing global radius variation.
    # ------------------------------------------------------------------
    print("\n=== CONSTRAINED GLOBAL RADIUS STATIONARITY ===")

    radius_records, R_eq, derivative_at_R0, second_derivative, radius_bracket_pass = (
        radius_scan_and_refine(
            one,
            g2,
            p,
            data,
            wall_per_area,
            artifact,
            R0=R0,
            n_phi=n_phi,
            n_sigma=n_sigma,
            omega_phi=omega_phi,
            omega_sigma=omega_sigma,
            h_over_r=h_over_r,
        )
    )

    print(f"RADIUS_FIT_DF_DR_AT_R0={derivative_at_R0:+.15e}")
    print(f"RADIUS_FIT_D2F_DR2={second_derivative:+.15e}")
    print(
        "RADIUS_CURVATURE_SIGN="
        + ("POSITIVE" if second_derivative > 0.0 else "NEGATIVE")
    )
    print("RADIAL_STABILITY_CLASSIFICATION=DEFER_TO_018C")
    print(f"REFINED_EQUILIBRIUM_RADIUS={R_eq:.15e}")

    if math.isfinite(R_eq):
        radius_shift = abs(R_eq - R0) / R0
    else:
        radius_shift = math.inf

    print(f"EQUILIBRIUM_RADIUS_REL_SHIFT={radius_shift:.15e}")
    print("RADIUS_EQUILIBRIUM_BRACKET=" + ("PASS" if radius_bracket_pass else "FAIL"))

    if not radius_bracket_pass:
        print("\n=== DECISION ===")
        print("018B1B_GLOBAL_MULTIPATCH_CLOSEOUT=RED")
        print("FIELD_THEORETICAL_CANDIDATE=NO")
        print("FAILURE_CLASS=GLOBAL_RADIUS_NOT_STATIONARY_IN_SCANNED_WINDOW")
        print("CURRENT_HEURISTIC=APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY")
        print("NEXT=REFINE_FIXED_WINDING_RADIUS_CONTINUATION_BEFORE_018C")
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
        return

    # Final primary field solve at the constrained equilibrium radius.
    primary = build_and_solve(
        one,
        g2,
        p,
        data,
        R=R_eq,
        n_phi=n_phi,
        n_sigma=n_sigma,
        omega_phi=omega_phi,
        omega_sigma=omega_sigma,
        n=41,
        box_half=12.0,
        artifact=artifact,
    )

    primary_eval, primary_tail_small = evaluate_with_tail_pair(
        one, g2, p, data, wall_per_area, primary, h_over_r
    )

    # Centered finite-difference stationarity check around the refined radius.
    eps = 1.0e-3
    stationarity_points = []

    for factor in (1.0 - eps, 1.0 + eps):
        result = build_and_solve(
            one,
            g2,
            p,
            data,
            R=R_eq * factor,
            n_phi=n_phi,
            n_sigma=n_sigma,
            omega_phi=omega_phi,
            omega_sigma=omega_sigma,
            n=33,
            box_half=12.0,
            artifact=artifact,
        )

        evaluation = global_from_result(
            one,
            g2,
            p,
            data,
            wall_per_area,
            result,
            h_over_r=h_over_r,
            tail_case=TAIL_CASES[0],
        )

        stationarity_points.append((result.problem.R, evaluation.grand_potential))

    dF_dR = (
        stationarity_points[1][1] - stationarity_points[0][1]
    ) / (
        stationarity_points[1][0] - stationarity_points[0][0]
    )

    force_scale = max(
        abs(primary_eval.ledger.energy) / R_eq,
        abs(wall_per_area.energy * math.pi * R_eq),
        1.0e-30,
    )

    stationarity_rel = abs(dF_dR) / force_scale

    print(f"REFINED_RADIUS_DF_DR={dF_dR:+.15e}")
    print(f"REFINED_RADIUS_STATIONARITY_REL={stationarity_rel:.15e}")
    print(
        "CONSTRAINED_GLOBAL_RADIUS_STATIONARITY="
        + ("PASS" if stationarity_rel <= MAX_RADIUS_STATIONARITY_REL else "FAIL")
    )

    # ------------------------------------------------------------------
    # Resolution, boundary/domain, and initialization reconstruction.
    # ------------------------------------------------------------------
    print("\n=== GLOBAL CONVERGENCE / INDEPENDENT RECONSTRUCTION ===")

    resolution_evals = []
    resolution_results = []

    for n, L in RESOLUTION_CASES:
        if n == 41 and math.isclose(L, 12.0):
            result = primary
            evaluation = primary_eval
        else:
            result = build_and_solve(
                one,
                g2,
                p,
                data,
                R=R_eq,
                n_phi=n_phi,
                n_sigma=n_sigma,
                omega_phi=omega_phi,
                omega_sigma=omega_sigma,
                n=n,
                box_half=L,
                artifact=artifact,
                warm_result=primary,
            )
            evaluation = global_from_result(
                one,
                g2,
                p,
                data,
                wall_per_area,
                result,
                h_over_r=h_over_r,
                tail_case=TAIL_CASES[1],
            )

        resolution_results.append(result)
        resolution_evals.append(evaluation)
        print_case("RESOLUTION_CASE", evaluation)

    domain_n, domain_L = DOMAIN_CASE
    domain_result = build_and_solve(
        one,
        g2,
        p,
        data,
        R=R_eq,
        n_phi=n_phi,
        n_sigma=n_sigma,
        omega_phi=omega_phi,
        omega_sigma=omega_sigma,
        n=domain_n,
        box_half=domain_L,
        warm_result=primary,
    )
    domain_eval = global_from_result(
        one,
        g2,
        p,
        data,
        wall_per_area,
        domain_result,
        h_over_r=h_over_r,
        tail_case=TAIL_CASES[1],
    )
    print_case("DOMAIN_CASE", domain_eval)

    fresh_result = build_and_solve(
        one,
        g2,
        p,
        data,
        R=R_eq,
        n_phi=n_phi,
        n_sigma=n_sigma,
        omega_phi=omega_phi,
        omega_sigma=omega_sigma,
        n=41,
        box_half=12.0,
        fresh=True,
    )
    fresh_eval = global_from_result(
        one,
        g2,
        p,
        data,
        wall_per_area,
        fresh_result,
        h_over_r=h_over_r,
        tail_case=TAIL_CASES[1],
    )
    print_case("FRESH_INITIALIZATION_CASE", fresh_eval)

    energy_spread = relative_spread([e.ledger.energy for e in resolution_evals])
    active_spread = relative_spread([e.ledger.active for e in resolution_evals])
    force_spread = relative_spread([e.force_node for e in resolution_evals])

    resolution_spread = max(energy_spread, active_spread, force_spread)

    domain_shift = max(
        relative_difference(domain_eval.ledger.energy, primary_eval.ledger.energy),
        relative_difference(domain_eval.ledger.active, primary_eval.ledger.active),
        relative_difference(domain_eval.force_node, primary_eval.force_node),
    )

    initialization_shift = max(
        relative_difference(fresh_eval.ledger.energy, primary_eval.ledger.energy),
        relative_difference(fresh_eval.ledger.active, primary_eval.ledger.active),
        relative_difference(fresh_eval.force_node, primary_eval.force_node),
    )

    print(f"GLOBAL_RESOLUTION_REL_SPREAD={resolution_spread:.15e}")
    print(f"GLOBAL_DOMAIN_REL_SHIFT={domain_shift:.15e}")
    print(f"GLOBAL_INITIALIZATION_REL_SHIFT={initialization_shift:.15e}")
    print(f"GLOBAL_REFERENCE_TAIL_REL_SHIFT={primary_eval.tail_rel_shift:.15e}")

    convergence_pass = (
        resolution_spread <= MAX_RESOLUTION_REL_SPREAD
        and domain_shift <= MAX_DOMAIN_REL_SHIFT
        and initialization_shift <= MAX_INITIALIZATION_REL_SHIFT
        and primary_eval.tail_rel_shift <= MAX_TAIL_REL_SHIFT
    )

    print("GLOBAL_FIELD_CONVERGENCE=" + ("PASS" if convergence_pass else "FAIL"))

    # ------------------------------------------------------------------
    # Complete T_munu, conservation, charges, and independent identities.
    # ------------------------------------------------------------------
    print("\n=== COMPLETE GLOBAL T_MUNU / CONSERVATION LEDGER ===")

    ledger = primary_eval.ledger
    active_trace = ledger.energy + ledger.p_r + ledger.p_z + ledger.p_phi
    active_global_relerr = abs(active_trace - ledger.active) / max(abs(ledger.active), 1.0e-30)

    print(f"TOTAL_ENERGY={ledger.energy:+.15e}")
    print(f"TOTAL_P_R={ledger.p_r:+.15e}")
    print(f"TOTAL_P_Z={ledger.p_z:+.15e}")
    print(f"TOTAL_P_PHI={ledger.p_phi:+.15e}")
    print(f"TOTAL_T_RZ={ledger.t_rz:+.15e}")
    print(f"TOTAL_ACTIVE_MASS={ledger.active:+.15e}")
    print(f"TOTAL_ACTIVE_TRACE_RELERR={active_global_relerr:.15e}")
    print(f"NOETHER_Q_PHI={ledger.q_phi_charge:+.15e}")
    print(f"NOETHER_Q_SIGMA={ledger.q_sigma_charge:+.15e}")
    print("GAUGE_CHARGE=0_BY_STATIONARY_MAGNETIC_ANSATZ")
    print(f"NET_ANGULAR_MOMENTUM={ledger.angular_momentum:+.15e}")
    print(f"GLOBAL_FUNDAMENTAL_FLUX_OVER_PI={primary_eval.global_flux_over_pi:+.15e}")
    print(f"MIN_LOCAL_ACTIVE_DENSITY={primary_eval.min_active_density:+.15e}")
    print(
        "NEGATIVE_ACTIVE_REGION="
        + ("YES" if primary_eval.negative_active_present else "NO")
    )

    print(f"PATCH_T00_VS_DISCRETE_ACTION_RELERR={primary_eval.energy_reconstruction_relerr:.15e}")
    print(f"PATCH_ACTIVE_TRACE_IDENTITY_RELERR={primary_eval.active_identity_relerr:.15e}")

    conservation_values = [e.conservation_l2 for e in resolution_evals]
    print(
        "CONSERVATION_L2_BY_RESOLUTION="
        + ",".join(f"{value:.15e}" for value in conservation_values)
    )
    print(f"PRIMARY_LOCAL_CONSERVATION_L2={primary_eval.conservation_l2:.15e}")

    conservation_trend_ratio = conservation_values[-1] / max(conservation_values[0], 1.0e-30)
    print(f"CONSERVATION_HIGH_TO_LOW_RATIO={conservation_trend_ratio:.15e}")

    conservation_pass = (
        primary_eval.conservation_l2 <= MAX_CONSERVATION_L2
        and conservation_trend_ratio <= MAX_CONSERVATION_HIGH_TO_LOW_RATIO
    )

    print("LOCAL_CONSERVATION_RESIDUAL=" + ("PASS" if conservation_pass else "FAIL"))

    energy_reconstruction_pass = (
        primary_eval.energy_reconstruction_relerr <= MAX_ENERGY_RECONSTRUCTION_RELERR
    )
    active_identity_pass = (
        primary_eval.active_identity_relerr <= MAX_ACTIVE_IDENTITY_RELERR
        and active_global_relerr <= 5.0e-3
    )

    print(
        "INDEPENDENT_TOTAL_ENERGY_RECONSTRUCTION="
        + ("PASS" if energy_reconstruction_pass else "FAIL")
    )
    print(
        "INDEPENDENT_ACTIVE_SOURCE_RECONSTRUCTION="
        + ("PASS" if active_identity_pass else "FAIL")
    )

    # ------------------------------------------------------------------
    # Gravity and finite payload from curved T_munu.
    # ------------------------------------------------------------------
    print("\n=== GLOBAL CURVED-FIELD GRAVITY / FINITE PAYLOAD ===")

    gravity_relerr = relative_difference(primary_eval.force_node, primary_eval.force_cell)

    print(f"POINT_OUTWARD_FORCE_NODE={primary_eval.force_node:+.15e}")
    print(f"POINT_OUTWARD_FORCE_CELL={primary_eval.force_cell:+.15e}")
    print(f"INDEPENDENT_GRAVITY_INTEGRATOR_RELERR={gravity_relerr:.15e}")
    print(f"PAYLOAD_CENTER_H={primary_eval.h_payload:.15e}")
    print(f"PAYLOAD_RADIUS={primary_eval.payload_radius:.15e}")
    print(f"PAYLOAD_SOURCE_CLEARANCE={primary_eval.source_clearance:.15e}")
    print("FINITE_PAYLOAD_CM_METHOD=HARMONIC_MEAN_VALUE_THEOREM_IN_SOURCE_FREE_SPHERE")
    print(f"FINITE_PAYLOAD_CM_OUTWARD={primary_eval.force_node:+.15e}")
    print(f"KERNEL_WEIGHTED_ACTIVE_MOMENT={primary_eval.force_node:+.15e}")
    print(f"GLOBAL_PROJECTED_C={primary_eval.projected_c:.15e}")

    gravity_pass = (
        primary_eval.force_node > MIN_OUTWARD_FORCE
        and primary_eval.force_cell > MIN_OUTWARD_FORCE
        and gravity_relerr <= MAX_GRAVITY_INTEGRATOR_RELERR
        and primary_eval.source_clearance > 0.0
    )

    active_mass_pass = ledger.active > MIN_POSITIVE_ACTIVE_MASS

    print("INDEPENDENT_GRAVITY_RECONSTRUCTION=" + ("PASS" if gravity_pass else "FAIL"))
    print("FINITE_PAYLOAD_CM_ACCELERATION=" + ("OUTWARD" if gravity_pass else "NOT_PROMOTED"))
    print("POSITIVE_TOTAL_ACTIVE_MASS=" + ("PASS" if active_mass_pass else "FAIL"))

    # Blind wildcard height check only.
    print("\n=== BLIND WILDCARD HEIGHT DIAGNOSTIC — NOT EVIDENCE ===")
    for factor in WILDCARD_HEIGHT_FACTORS:
        x = h_over_r * factor
        if x <= 0.0 or x >= 1.0:
            print(f"WILDCARD_X_FACTOR={factor:.6f} STATUS=OUTSIDE_DOMAIN")
            continue

        eval_x = global_from_result(
            one,
            g2,
            p,
            data,
            wall_per_area,
            primary,
            h_over_r=x,
            tail_case=TAIL_CASES[0],
        )

        print(
            f"WILDCARD_X_FACTOR={factor:.6f} "
            f"X={x:.9e} "
            f"F_OUT={eval_x.force_node:+.9e} "
            f"OUTWARD={'YES' if eval_x.force_node > 0.0 else 'NO'}"
        )

    print("WILDCARD_VALUES_USED_AS_EVIDENCE=NO")

    # ------------------------------------------------------------------
    # Physical/mathematical promotion bookkeeping.
    # ------------------------------------------------------------------
    field_residual_pass = all(
        result.gradient_rms <= MAX_FIELD_GRADIENT_RMS
        and result.gradient_max <= MAX_FIELD_GRADIENT_MAX
        and result.matching_mismatch <= MAX_MATCHING_MISMATCH
        and topology_pass(data, result)
        for result in resolution_results + [domain_result, fresh_result, primary]
    )

    finite_energy_pass = math.isfinite(ledger.energy) and ledger.energy > 0.0
    regularity_pass = all(
        result.regularity_pass
        for result in resolution_results + [domain_result, fresh_result, primary]
    )

    radius_pass = (
        radius_bracket_pass
        and stationarity_rel <= MAX_RADIUS_STATIONARITY_REL
    )

    global_pass = (
        field_residual_pass
        and finite_energy_pass
        and regularity_pass
        and radius_pass
        and convergence_pass
        and conservation_pass
        and energy_reconstruction_pass
        and active_identity_pass
        and active_mass_pass
        and primary_eval.negative_active_present
        and gravity_pass
    )

    improvement = VALIDATED_C / primary_eval.projected_c
    projected_energy = VALIDATED_ENERGY_1G_1M / improvement

    print("\n=== 018B PROMOTION LEDGER ===")
    print("FIELD_EQUATION_RESIDUALS=" + ("REPRODUCED" if field_residual_pass else "FAIL"))
    print("FINITE_TOTAL_ENERGY=" + ("PASS" if finite_energy_pass else "FAIL"))
    print("GLOBAL_REGULARITY=" + ("PASS" if regularity_pass else "FAIL"))
    print("NOETHER_CHARGE=RECONSTRUCTED")
    print("GAUGE_CHARGE=ZERO_IN_SELECTED_MAGNETIC_ANSATZ")
    print("INTEGER_WINDING=EXACT")
    print("NET_ANGULAR_MOMENTUM=RECONSTRUCTED")
    print("COMPLETE_T_MUNU=RECONSTRUCTED")
    print("LOCAL_CONSERVATION_RESIDUAL=" + ("PASS" if conservation_pass else "FAIL"))
    print("TOTAL_ACTIVE_MASS=" + ("POSITIVE" if active_mass_pass else "FAIL"))
    print("NEGATIVE_ACTIVE_REGION=" + ("PRESENT" if primary_eval.negative_active_present else "ABSENT"))
    print("KERNEL_WEIGHTED_ACTIVE_MOMENT=RECONSTRUCTED")
    print("POINT_ACCELERATION=" + ("OUTWARD" if gravity_pass else "FAIL"))
    print("FINITE_PAYLOAD_CM_ACCELERATION=" + ("OUTWARD" if gravity_pass else "FAIL"))
    print("FINITE_SOURCE_THICKNESS=YES")
    print("BOUNDARY_DECAY=" + ("PASS" if primary_eval.tail_rel_shift <= MAX_TAIL_REL_SHIFT else "FAIL"))
    print("CONSTRAINED_GLOBAL_RADIUS_STATIONARITY=" + ("PASS" if radius_pass else "FAIL"))
    print("INDEPENDENT_RECONSTRUCTION=" + ("PASS" if energy_reconstruction_pass and gravity_pass and convergence_pass else "FAIL"))

    print(f"FIELD_LEVEL_PROJECTED_C={primary_eval.projected_c:.15e}")
    print(f"FIELD_LEVEL_PROJECTED_IMPROVEMENT_FACTOR={improvement:.15e}")
    print(f"FIELD_LEVEL_PROJECTED_ONE_G_ONE_M_ENERGY_J={projected_energy:.15e}")
    print("PROJECTED_C_STATUS=FIELD_LEVEL_LINEARIZED_GR_NOT_NONLINEAR_VALIDATED")

    # Save the promoted/refined global field state only if every gate is green.
    if global_pass:
        OUTPUT_NPZ.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            OUTPUT_NPZ,
            R=np.array(primary.problem.R),
            n_phi=np.array(primary.problem.n_phi),
            n_sigma=np.array(primary.problem.n_sigma),
            omega_phi=np.array(primary.problem.omega_phi),
            omega_sigma=np.array(primary.problem.omega_sigma),
            x=primary.problem.x,
            z=primary.problem.z,
            cylindrical_r=primary.problem.cylindrical_r,
            h=primary.h,
            phi=primary.phi,
            sigma=primary.sigma,
            a_real=primary.a.real,
            a_imag=primary.a.imag,
            ax=primary.ax,
            az=primary.az,
            total_energy=np.array(ledger.energy),
            total_active_mass=np.array(ledger.active),
            noether_q_phi=np.array(ledger.q_phi_charge),
            noether_q_sigma=np.array(ledger.q_sigma_charge),
            angular_momentum=np.array(ledger.angular_momentum),
            point_outward_force=np.array(primary_eval.force_node),
            projected_c=np.array(primary_eval.projected_c),
            conservation_l2=np.array(primary_eval.conservation_l2),
        )

    print("\n=== DECISION ===")

    if global_pass:
        print("018B1B_GLOBAL_MULTIPATCH_T_MUNU_GRAVITY_CONSERVATION_CLOSEOUT=GREEN")
        print("018B_FULL_2D_COUPLED_FINITE_THICKNESS_EULER_LAGRANGE_SOLUTION=GREEN")
        print("FIELD_THEORETICAL_CANDIDATE=YES")
        print("FULL_COUPLED_EULER_LAGRANGE_SOLUTION=PASS")
        print("FINITE_ENERGY=PASS")
        print("GLOBAL_REGULARITY=PASS")
        print("COMPLETE_STRESS_ENERGY=PASS")
        print("FINITE_PAYLOAD_OUTWARD_FIELD=PASS")
        print("INDEPENDENT_RECONSTRUCTION=PASS")
        print("CURRENT_HEURISTIC=APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY")
        print("HEURISTIC_CHANGE=APPROXIMATELY_66_TO_68_PERCENT")
        print("NEXT=018C1_AXISYMMETRIC_HESSIAN_AND_TIME_EVOLUTION_STABILITY_GATE")
        print("NEXT_AFTER_018C1_GREEN=018C2_NONAXISYMMETRIC_M2_AND_HIGHER_MODE_STABILITY")
        print(f"PROMOTED_FIELD_ARTIFACT={OUTPUT_NPZ}")
    else:
        print("018B1B_GLOBAL_MULTIPATCH_T_MUNU_GRAVITY_CONSERVATION_CLOSEOUT=RED")
        print("018B_FULL_2D_COUPLED_FINITE_THICKNESS_EULER_LAGRANGE_SOLUTION=NOT_PROMOTED")
        print("FIELD_THEORETICAL_CANDIDATE=NO")
        print("CURRENT_HEURISTIC=APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY")
        print("HEURISTIC_CHANGE=NONE")
        print("NEXT=CLASSIFY_FAILED_018B1B_PROMOTION_GATE_BEFORE_018C")

    print("FULL_COMPOSITE_STABILITY=NOT_ESTABLISHED")
    print("FRAME_DRAGGING=NOT_INCLUDED")
    print("NONLINEAR_EINSTEIN_MATTER=NOT_ESTABLISHED")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018B1B_GLOBAL_MULTIPATCH_T_MUNU_"
        "GRAVITY_CONSERVATION_CLOSEOUT"
    )


if __name__ == "__main__":
    main()
