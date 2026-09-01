#!/usr/bin/env python3
"""INT-14B — support-constrained source bound and structural-overhead bridge.

PURPOSE
-------
Test whether the >=10x conservation-aware source-level headroom established by
INT-14A survives when the source is forced into a compact, source-centered,
reflection-symmetric support envelope derived directly from the promotion-grade
B=7 exact-map field.

This is a stricter and more geometry-faithful test than the one-sided 006B
stand-off comparator used in INT-14A.

SCIENTIFIC QUESTION
-------------------
Can a static positive-energy, DEC-satisfying, locally conserved stress tensor
produce the matched finite-spherical-payload outward response with >=10x lower
standardized energy than the current B=7 field while remaining inside a
source-centered support envelope comparable to the current field's actual
energy support and while retaining its negative-enclosed-active core anatomy?

WHY THIS RUN IS NEEDED
----------------------
INT-14A established two independent constructive comparisons:

    current exact-map B=7:
        C ~= 422.22

    006D:
        C ~= 23.59
        headroom ~= 17.90x

    independent 006B KNOWN_THIN20:
        C ~= 32.95
        headroom ~= 12.81x

Both conserved-DEC routes exceeded the project's >=10x headroom threshold.

However, the one-sided 006B sources live below a payload that is outside their
support.  The B=7 payload instead lies inside the shell-like field source.
Therefore INT-14A correctly left

    STRICT_INT14_SAME_SUPPORT_GLOBAL_LOWER_BOUND=NOT_YET.

INT-14B removes that mismatch as far as possible without yet constructing a
new microscopic field theory.

CURRENT-FIELD SUPPORT DEFINITION
--------------------------------
Rebuild the exact B=7, eta=0.4, m=8 rational-map source using the same
independently validated 3D source quadrature used by INT-02/INT-14A.

From its positive energy weights define spherical energy quantile radii

    R90, R95, R99

by

    integral_{|x| <= Rq} rho d^3x = q E.

Normalize all lengths by the current payload-center distance h, so h=1 in the
optimization.

The primary support envelope is the R99 sphere.

R95 and R90 are declared tighter sensitivity probes.

SUPPORT MODEL
-------------
Use an axisymmetric staggered finite-volume stress tensor in cylindrical
coordinates (r,z), centered on the source origin.

The finite box is

    0 <= r <= R_support
    -R_support <= z <= +R_support.

Only cells whose centers satisfy

    r^2 + z^2 <= R_support^2

are active.

The resulting stair-step sphere is refined with the grid.  Tractions crossing
from an active cell into an inactive/vacuum cell are set to zero explicitly.
Thus the finite-volume source has a traction-free compact boundary.

This is still an axisymmetric support proxy, not the exact polyhedral B=7
support.

SOURCE-CENTERED REFLECTION SYMMETRY
-----------------------------------
To prevent a trivial optimizer from translating ordinary positive mass to the
far side of the payload and calling the attraction "outward", impose source
reflection symmetry z -> -z:

    e, p_r, p_z, p_phi are even,
    T_rz is odd.

This preserves a source centered at the B=7 origin.

NEGATIVE-ENCLOSED-ACTIVE CORE MATCH
-----------------------------------
The exact B=7 source has a payload lying inside a negative-enclosed-active
region.

Using the exact-map 3D source reconstruction, evaluate at the outer payload
radius

    r_core = h + R_P

the fraction

    f_core_exact =
        M_A(r_core) / E.

For the primary MATCHED_CORE optimization require

    M_A_proxy(r_core)
        <=
    f_core_exact * E_proxy.

Because f_core_exact < 0, the proxy must retain at least the same normalized
negative-enclosed-active core strength through the complete payload.

A secondary SIGN_ONLY diagnostic requires only

    M_A_proxy(r_core) <= 0.

The SIGN_ONLY result is never sufficient for promotion if MATCHED_CORE fails.

FINITE-PAYLOAD KERNEL
---------------------
The payload center is on +z at h=1 and the uniform spherical payload has
radius

    q_P = R_P / h.

For an axisymmetric source point (r,z), the exact payload-averaged radial
kernel is

    K_P(r,z)
      =
    (z-h) / max([r^2+(z-h)^2]^(3/2), q_P^3).

After azimuthal integration the annular integrand is

    2 pi r K_P(r,z).

Each finite-volume cell kernel is evaluated by high-order Gauss-Legendre
cubature, with composite refinement near the payload cap.

VALIDATION
----------
Before any support-bound result is used, the generalized finite-payload
kernel/solver must recover the repository 006B KNOWN_THIN20 stand-off case.

For that validation source the payload ball is source-free, so the mean-value
theorem says the finite spherical payload acceleration equals the point-target
acceleration exactly.

The numerical cell kernels are also compared directly against the repository's
analytic 006B cell kernel.

STRESS / CONSERVATION MODEL
---------------------------
Variables:

    e          cell-centered positive energy density
    p_phi      cell-centered azimuthal stress
    p_r        radial-face normal stress
    p_z        z-face normal stress
    T_rz       vertex shear stress

Cell-centered spatial stress:

    [[p_r, T_rz, 0],
     [T_rz, p_z, 0],
     [0, 0, p_phi]].

Exact type-I DEC is imposed by second-order-cone constraints

    |lambda_i| <= e.

Discrete local conservation is the same exact integrated staggered
finite-volume force balance already audited in 006B:

    (1/r) d(r p_r)/dr + d(T_rz)/dz - p_phi/r = 0

    (1/r) d(r T_rz)/dr + d(p_z)/dz = 0.

Global Laue identities are retained as independent necessary static checks:

    integral (p_r+p_phi) dV = 0
    integral p_z dV = 0.

Therefore, for a green localized static solution,

    integral S dV = integral e dV > 0,

giving positive total far-field active mass.

OBJECTIVE / NORMALIZATION
-------------------------
Set

    h = 1
    A_P >= 1.

Minimize

    C_proxy = integral e dV.

This is directly comparable with

    C_current = 1 / eta_op

from INT-14A.

Headroom:

    H = C_current / C_proxy.

Structural-overhead fraction relative to the tested proxy:

    f_overhead = 1 - C_proxy / C_current.

This is SOURCE-LEVEL structural overhead only.

It does not mean that the corresponding Skyrmion energy can be removed while
preserving topology, stationarity, or stability.

PRIMARY RESOLUTION SEQUENCE
---------------------------
For the R99 MATCHED_CORE spherical support proxy use:

    low:      nr=8,  nz=16
    primary:  nr=12, nz=24
    high:     nr=16, nz=32.

Predeclared finite-grid convergence criterion:

    primary-to-high C relative difference <= 0.15.

The tolerance is deliberately much tighter than the order-of-magnitude
promotion threshold but recognizes the historical convergence cost of the
staggered finite-volume source solver.

SENSITIVITY
-----------
At primary resolution also evaluate:

    R95 MATCHED_CORE
    R90 MATCHED_CORE
    R99 SIGN_ONLY.

These diagnose whether the answer is controlled by tail support or by the
negative-core-strength matching constraint.

EXPANSION-COMPATIBILITY FALLBACK
--------------------------------
Only if the R99 MATCHED_CORE result does not establish >=10x converged headroom,
probe larger homothetic support envelopes.

Primary physical probes:

    gamma = 1.125
    gamma = 1.25
    gamma = 1.50.

The gamma=1.25 probe directly tests whether a modest support enlargement in the
same direction highlighted by the earlier nonstationary dilation diagnostic
can restore conserved-DEC efficiency.

Blind wildcard diagnostics, only in this fallback:

    gamma = 1.6
    gamma = 1.875.

They are not evidence, priors, or optimization targets.

PROMOTION
---------
INT-14B promotes formal INT Level 3 through the SIMPLE SOURCE MORPHOLOGY route
if all of the following hold:

    INT14A_TWO_ROUTE_GE10X=PASS

    GENERALIZED_006B_RECOVERY=PASS

    R99_MATCHED_CORE_PRIMARY=GREEN

    R99_MATCHED_CORE_HIGH=GREEN

    R99_PRIMARY_HIGH_C_REL_DIFF <= 0.15

    conservative R99 headroom >= 10x

where conservative headroom uses the larger (less favorable) of the primary
and high coefficients.

Permitted claim:

    A source-centered compact conserved-DEC morphology inside the tested R99
    energy-support proxy reproduces the matched finite-payload outward
    response with >=10x lower standardized energy than the present B=7 field.

This establishes actionable SOURCE-ORGANIZATION headroom in the tested class.

It does NOT establish a new field realization.

FALSIFIERS / NEGATIVE OUTCOMES
------------------------------
Important negative results include:

- R99 MATCHED_CORE infeasible under refinement;
- R99 converges but headroom <10x;
- only SIGN_ONLY passes;
- only substantially expanded support passes;
- generalized solver fails 006B recovery;
- DEC/conservation/Laue/active-total checks fail.

If only gamma>1 support envelopes pass, record the minimum tested support
expansion needed.  Do not call that same-support headroom.

STOP RULE
---------
If formal R99 >=10x headroom passes, stop source-coefficient polishing.

Proceed to mandatory-scaffolding / field-space accessibility:

    Which parts of the current Skyrmion energy are required by topology,
    stationarity, and stability, and is there a continuable low-energy field
    direction toward the efficient source anatomy?

If R99 fails and no modest expanded support retains >=10x, close the
source-organization efficiency path and return to 023C/023D/global reranking.

CLAIM LIMITS
------------
No source mask is a microscopic field solution.
No axisymmetric proxy is the exact B=7 polyhedral field.
No Hessian stability is established.
No strict N=73 result is established.
No nonlinear Einstein-Skyrme continuation is established.
No practical antigravity device is established.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_INT14B_SUPPORT_CONSTRAINED_STRUCTURAL_OVERHEAD_BRIDGE
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
import importlib.util
import json
import math
from pathlib import Path
import sys
from typing import Any

import cvxpy as cp
import numpy as np
from numpy.polynomial.legendre import leggauss


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

INT14A_SUMMARY = DATA / "int14a_conservation_aware_constructive_headroom_summary.json"
INT03S_SUMMARY = DATA / "int03_04s_scale_zero_surface_summary.json"

INT02_SOURCE = SIM / "int02_signed_kernel_orientation_robustness.py"
A23_SOURCE = SIM / "023a_topological_false_core_multiskyrmion_gr_repulsion_gate.py"
B23_SOURCE = SIM / "023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.py"
S006B = SIM / "006b_full_rz_decision.py"

OUT_JSON = DATA / "int14b_support_constrained_structural_overhead_summary.json"
OUT_CSV = DATA / "int14b_support_constrained_cases.csv"

B = 7
ETA = 0.4
MASS = 8.0

EXACT_NR = 68
EXACT_NMU = 32
EXACT_NPHI = 64

HEADROOM_MAJOR = 10.0

DEC_TOL = 3.0e-6
CONS_TOL = 3.0e-6
TRACE_TOL = 3.0e-6
ACTIVE_TOTAL_REL_TOL = 3.0e-6

RECOVERY_C_REL_TOL = 3.0e-3
KERNEL_RECOVERY_REL_TOL = 2.0e-9

PRIMARY_HIGH_C_REL_TOL = 0.15

BASE_GAUSS_ORDER = 8
NEAR_GAUSS_ORDER = 8
NEAR_SUBDIV = 6

BLIND_WILDCARD_GAMMAS = (1.6, 1.875)


@dataclass(frozen=True)
class SupportCase:
    """One generalized axisymmetric finite-volume source problem."""

    name: str
    nr: int
    nz: int
    radius: float
    zmin: float
    zmax: float
    target_z: float
    payload_radius: float

    spherical_mask: bool = False
    reflection_symmetry: bool = False

    core_radius: float | None = None
    core_fraction_target: float | None = None

    category: str = "PRIMARY"


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)

    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def relative_error(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0e-300)


def energy_quantile_radius(
    radius: np.ndarray,
    energy: np.ndarray,
    fraction: float,
) -> float:
    order = np.argsort(radius)
    r = radius[order]
    e = np.maximum(energy[order], 0.0)

    cumulative = np.cumsum(e)
    target = fraction * float(cumulative[-1])

    index = int(np.searchsorted(cumulative, target, side="left"))
    index = min(index, len(r) - 1)

    return float(r[index])


def exact_map_support_anatomy(int02, a23, b23) -> dict[str, float]:
    degree, I = b23.angular_integrals_b7(b23.B7_B0)

    profile = b23.solve_profile_with_custom_I(
        a23,
        B,
        ETA,
        MASS,
        I,
    )

    sector_profiles, sector_energies = b23.solve_exact_sector(
        a23,
        ETA,
        MASS,
    )

    if not all(p.success for p in sector_profiles.values()):
        raise RuntimeError("Exact sector solve failed")

    candidate = b23.candidate_from_sector(
        a23,
        sector_profiles,
        sector_energies,
        B,
    )

    payload = candidate.payload

    xyz, energy_w, active_w, _e4_w, _v_w = int02.exact_map_weighted_source(
        b23,
        profile,
        b23.B7_B0,
        EXACT_NR,
        EXACT_NMU,
        EXACT_NPHI,
    )

    radii = np.linalg.norm(xyz, axis=1)

    E = float(np.sum(energy_w))
    active_total = float(np.sum(active_w))

    if E <= 0.0:
        raise RuntimeError("Exact-map source has nonpositive energy")

    h = float(payload.payload_center)
    rp = float(payload.payload_radius)
    r_core = h + rp

    core_active = float(
        np.sum(
            active_w[
                radii <= r_core
            ]
        )
    )

    result = {
        "degree": float(degree),
        "I": float(I),
        "E": E,
        "h": h,
        "payload_radius": rp,
        "payload_radius_over_h": rp / h,
        "shell_radius": float(profile.shell_radius),
        "shell_radius_over_h": float(profile.shell_radius / h),
        "negative_active_outer_radius": float(
            profile.negative_active_outer_radius
        ),
        "negative_active_outer_over_h": float(
            profile.negative_active_outer_radius / h
        ),
        "R90": energy_quantile_radius(radii, energy_w, 0.90),
        "R95": energy_quantile_radius(radii, energy_w, 0.95),
        "R99": energy_quantile_radius(radii, energy_w, 0.99),
        "active_total_over_E": active_total / E,
        "core_radius": r_core,
        "core_radius_over_h": r_core / h,
        "core_active_fraction": core_active / E,
    }

    for q in ("R90", "R95", "R99"):
        result[q + "_over_h"] = result[q] / h

    return result


def gauss_interval(
    a: float,
    b: float,
    order: int,
) -> tuple[np.ndarray, np.ndarray]:
    nodes, weights = leggauss(order)

    x = 0.5 * (a + b) + 0.5 * (b - a) * nodes
    w = 0.5 * (b - a) * weights

    return x, w


def finite_payload_cell_kernel(
    r0: float,
    r1: float,
    z0: float,
    z1: float,
    target_z: float,
    payload_radius: float,
) -> float:
    """Return annular-cell finite-spherical-payload axial kernel integral."""

    dr = r1 - r0
    dz = z1 - z0

    r_closest = max(r0, 0.0)

    if z0 <= target_z <= z1:
        z_distance = 0.0
    else:
        z_distance = min(
            abs(z0 - target_z),
            abs(z1 - target_z),
        )

    dmin = math.hypot(r_closest, z_distance)

    near_scale = max(
        payload_radius,
        dr,
        dz,
    )

    subdiv = NEAR_SUBDIV if dmin < 2.5 * near_scale else 1
    order = NEAR_GAUSS_ORDER if subdiv > 1 else BASE_GAUSS_ORDER

    total = 0.0

    r_breaks = np.linspace(r0, r1, subdiv + 1)
    z_breaks = np.linspace(z0, z1, subdiv + 1)

    rp3 = payload_radius**3

    for ir in range(subdiv):
        ra, rb = r_breaks[ir], r_breaks[ir + 1]
        rr, rw = gauss_interval(ra, rb, order)

        for iz in range(subdiv):
            za, zb = z_breaks[iz], z_breaks[iz + 1]
            zz, zw = gauss_interval(za, zb, order)

            R, Z = np.meshgrid(
                rr,
                zz,
                indexing="ij",
            )
            WR, WZ = np.meshgrid(
                rw,
                zw,
                indexing="ij",
            )

            dzp = Z - target_z
            d2 = R * R + dzp * dzp
            d = np.sqrt(d2)

            denominator = np.maximum(
                d2 * d,
                rp3,
            )

            integrand = (
                2.0
                * math.pi
                * R
                * dzp
                / denominator
            )

            total += float(
                np.sum(
                    WR
                    * WZ
                    * integrand
                )
            )

    return total


def build_geometry(case: SupportCase):
    r_edges = np.linspace(
        0.0,
        case.radius,
        case.nr + 1,
    )
    z_edges = np.linspace(
        case.zmin,
        case.zmax,
        case.nz + 1,
    )

    r_centers = 0.5 * (
        r_edges[:-1] + r_edges[1:]
    )
    z_centers = 0.5 * (
        z_edges[:-1] + z_edges[1:]
    )

    volumes = np.zeros(
        (case.nr, case.nz),
        dtype=float,
    )
    kernels = np.zeros_like(volumes)

    for i in range(case.nr):
        r0, r1 = r_edges[i], r_edges[i + 1]
        annulus_area = math.pi * (
            r1 * r1 - r0 * r0
        )

        for j in range(case.nz):
            z0, z1 = z_edges[j], z_edges[j + 1]

            volumes[i, j] = (
                annulus_area
                * (z1 - z0)
            )

            kernels[i, j] = finite_payload_cell_kernel(
                r0,
                r1,
                z0,
                z1,
                case.target_z,
                case.payload_radius,
            )

    R, Z = np.meshgrid(
        r_centers,
        z_centers,
        indexing="ij",
    )

    if case.spherical_mask:
        active_mask = (
            R * R + Z * Z
            <= case.radius * case.radius
        )
    else:
        active_mask = np.ones(
            (case.nr, case.nz),
            dtype=bool,
        )

    return (
        r_edges,
        z_edges,
        r_centers,
        z_centers,
        volumes,
        kernels,
        active_mask,
    )


def add_mask_boundary_constraints(
    constraints,
    case: SupportCase,
    active_mask: np.ndarray,
    e,
    pphi,
    pr_face,
    pz_face,
    trz_vertex,
):
    nr, nz = case.nr, case.nz

    # Inactive cells are literal vacuum in the proxy.
    for i in range(nr):
        for j in range(nz):
            if not active_mask[i, j]:
                constraints.extend([
                    e[i, j] == 0.0,
                    pphi[i, j] == 0.0,
                ])

    # Radial normal traction.  r=0 is an axis, not a vacuum boundary.
    constraints.append(pr_face[nr, :] == 0.0)

    for i in range(1, nr):
        for j in range(nz):
            left_active = bool(active_mask[i - 1, j])
            right_active = bool(active_mask[i, j])

            if not (left_active and right_active):
                constraints.append(
                    pr_face[i, j] == 0.0
                )

    # z normal traction.
    constraints.extend([
        pz_face[:, 0] == 0.0,
        pz_face[:, nz] == 0.0,
    ])

    for i in range(nr):
        for j in range(1, nz):
            lower_active = bool(active_mask[i, j - 1])
            upper_active = bool(active_mask[i, j])

            if not (lower_active and upper_active):
                constraints.append(
                    pz_face[i, j] == 0.0
                )

    # Shear traction: keep a vertex free only when every adjacent
    # in-domain cell is active.  This is a conservative stair-step
    # traction-free spherical boundary.
    constraints.extend([
        trz_vertex[0, :] == 0.0,
        trz_vertex[nr, :] == 0.0,
        trz_vertex[:, 0] == 0.0,
        trz_vertex[:, nz] == 0.0,
    ])

    for i in range(1, nr):
        for j in range(1, nz):
            neighbors = (
                active_mask[i - 1, j - 1],
                active_mask[i, j - 1],
                active_mask[i - 1, j],
                active_mask[i, j],
            )

            if not all(bool(x) for x in neighbors):
                constraints.append(
                    trz_vertex[i, j] == 0.0
                )

    # Axis regularity.
    for j in range(nz):
        if active_mask[0, j]:
            constraints.append(
                pr_face[0, j] == pphi[0, j]
            )
        else:
            constraints.extend([
                pr_face[0, j] == 0.0,
                pphi[0, j] == 0.0,
            ])


def add_reflection_symmetry(
    constraints,
    case: SupportCase,
    e,
    pphi,
    pr_face,
    pz_face,
    trz_vertex,
):
    if not case.reflection_symmetry:
        return

    nr, nz = case.nr, case.nz

    if not math.isclose(
        case.zmin,
        -case.zmax,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    ):
        raise RuntimeError(
            "Reflection-symmetric case requires zmin=-zmax"
        )

    # Cell-centered even quantities.
    for j in range(nz // 2):
        jm = nz - 1 - j

        constraints.extend([
            e[:, j] == e[:, jm],
            pphi[:, j] == pphi[:, jm],
            pr_face[:, j] == pr_face[:, jm],
        ])

    # z-face p_z is even; shear is odd.
    for k in range((nz + 1) // 2):
        km = nz - k

        constraints.append(
            pz_face[:, k] == pz_face[:, km]
        )

        constraints.append(
            trz_vertex[:, k] == -trz_vertex[:, km]
        )

    if nz % 2 == 0:
        constraints.append(
            trz_vertex[:, nz // 2] == 0.0
        )


def solve_support_case(case: SupportCase) -> dict[str, Any]:
    (
        r_edges,
        z_edges,
        r_centers,
        z_centers,
        volumes,
        kernels,
        active_mask,
    ) = build_geometry(case)

    nr, nz = case.nr, case.nz

    e = cp.Variable(
        (nr, nz),
        nonneg=True,
        name="e",
    )
    pphi = cp.Variable(
        (nr, nz),
        name="pphi",
    )
    pr_face = cp.Variable(
        (nr + 1, nz),
        name="pr_face",
    )
    pz_face = cp.Variable(
        (nr, nz + 1),
        name="pz_face",
    )
    trz_vertex = cp.Variable(
        (nr + 1, nz + 1),
        name="trz_vertex",
    )

    constraints: list[cp.Constraint] = []

    add_mask_boundary_constraints(
        constraints,
        case,
        active_mask,
        e,
        pphi,
        pr_face,
        pz_face,
        trz_vertex,
    )

    add_reflection_symmetry(
        constraints,
        case,
        e,
        pphi,
        pr_face,
        pz_face,
        trz_vertex,
    )

    pr_cell: list[list[cp.Expression]] = [
        [None for _ in range(nz)]
        for _ in range(nr)
    ]  # type: ignore[list-item]

    pz_cell: list[list[cp.Expression]] = [
        [None for _ in range(nz)]
        for _ in range(nr)
    ]  # type: ignore[list-item]

    trz_cell: list[list[cp.Expression]] = [
        [None for _ in range(nz)]
        for _ in range(nr)
    ]  # type: ignore[list-item]

    # Cell stresses + exact type-I DEC.
    for i in range(nr):
        for j in range(nz):
            prc = 0.5 * (
                pr_face[i, j]
                + pr_face[i + 1, j]
            )
            pzc = 0.5 * (
                pz_face[i, j]
                + pz_face[i, j + 1]
            )
            trzc = 0.25 * (
                trz_vertex[i, j]
                + trz_vertex[i + 1, j]
                + trz_vertex[i, j + 1]
                + trz_vertex[i + 1, j + 1]
            )

            pr_cell[i][j] = prc
            pz_cell[i][j] = pzc
            trz_cell[i][j] = trzc

            mean = 0.5 * (prc + pzc)
            half_difference = 0.5 * (
                prc - pzc
            )
            spectral_radius = cp.norm(
                cp.hstack([
                    half_difference,
                    trzc,
                ]),
                2,
            )

            constraints.extend([
                spectral_radius
                <= e[i, j] - mean,
                spectral_radius
                <= e[i, j] + mean,
                pphi[i, j] <= e[i, j],
                -pphi[i, j] <= e[i, j],
            ])

    # Exact integrated finite-volume conservation.
    for i in range(nr):
        r0, r1 = (
            r_edges[i],
            r_edges[i + 1],
        )
        dr = r1 - r0
        annular_radial_factor = 0.5 * (
            r1 * r1 - r0 * r0
        )

        for j in range(nz):
            z0, z1 = (
                z_edges[j],
                z_edges[j + 1],
            )
            dz = z1 - z0

            trz_south = 0.5 * (
                trz_vertex[i, j]
                + trz_vertex[i + 1, j]
            )
            trz_north = 0.5 * (
                trz_vertex[i, j + 1]
                + trz_vertex[i + 1, j + 1]
            )

            trz_west = 0.5 * (
                trz_vertex[i, j]
                + trz_vertex[i, j + 1]
            )
            trz_east = 0.5 * (
                trz_vertex[i + 1, j]
                + trz_vertex[i + 1, j + 1]
            )

            radial_balance = (
                dz
                * (
                    r1 * pr_face[i + 1, j]
                    - r0 * pr_face[i, j]
                )
                + annular_radial_factor
                * (
                    trz_north
                    - trz_south
                )
                - dr
                * dz
                * pphi[i, j]
            )

            vertical_balance = (
                2.0
                * dz
                * (
                    r1 * trz_east
                    - r0 * trz_west
                )
                + (
                    r1 * r1
                    - r0 * r0
                )
                * (
                    pz_face[i, j + 1]
                    - pz_face[i, j]
                )
            )

            constraints.extend([
                radial_balance == 0.0,
                vertical_balance == 0.0,
            ])

    pr_matrix = cp.vstack([
        cp.hstack([
            pr_cell[i][j]
            for j in range(nz)
        ])
        for i in range(nr)
    ])

    pz_matrix = cp.vstack([
        cp.hstack([
            pz_cell[i][j]
            for j in range(nz)
        ])
        for i in range(nr)
    ])

    volume_constant = cp.Constant(volumes)

    # Necessary global static Laue identities.
    constraints.extend([
        cp.sum(
            cp.multiply(
                volume_constant,
                pr_matrix + pphi,
            )
        ) == 0.0,
        cp.sum(
            cp.multiply(
                volume_constant,
                pz_matrix,
            )
        ) == 0.0,
    ])

    active_density = (
        e
        + pr_matrix
        + pz_matrix
        + pphi
    )

    total_mass = cp.sum(
        cp.multiply(
            volume_constant,
            e,
        )
    )

    target_acceleration = cp.sum(
        cp.multiply(
            cp.Constant(kernels),
            active_density,
        )
    )

    constraints.append(
        target_acceleration >= 1.0
    )

    # Preserve the normalized negative-enclosed-active core anatomy.
    if (
        case.core_radius is not None
        and case.core_fraction_target is not None
    ):
        R, Z = np.meshgrid(
            r_centers,
            z_centers,
            indexing="ij",
        )

        core_mask = (
            R * R + Z * Z
            <= case.core_radius**2
        ).astype(float)

        core_active = cp.sum(
            cp.multiply(
                cp.Constant(
                    volumes * core_mask
                ),
                active_density,
            )
        )

        constraints.append(
            core_active
            <= case.core_fraction_target
            * total_mass
        )

    problem = cp.Problem(
        cp.Minimize(total_mass),
        constraints,
    )

    installed = cp.installed_solvers()
    solver = (
        "CLARABEL"
        if "CLARABEL" in installed
        else "SCS"
    )

    try:
        problem.solve(
            solver=solver,
            verbose=False,
        )
    except Exception:
        if (
            solver != "SCS"
            and "SCS" in installed
        ):
            solver = "SCS"
            problem.solve(
                solver=solver,
                verbose=False,
                eps=2.0e-5,
                max_iters=150000,
            )
        else:
            raise

    base = {
        "name": case.name,
        "category": case.category,
        "nr": nr,
        "nz": nz,
        "support_radius": case.radius,
        "zmin": case.zmin,
        "zmax": case.zmax,
        "target_z": case.target_z,
        "payload_radius": case.payload_radius,
        "spherical_mask": case.spherical_mask,
        "reflection_symmetry": (
            case.reflection_symmetry
        ),
        "core_radius": case.core_radius,
        "core_fraction_target": (
            case.core_fraction_target
        ),
        "active_cell_fraction": float(
            np.mean(active_mask)
        ),
        "status": str(problem.status),
        "solver": solver,
    }

    if problem.status not in (
        cp.OPTIMAL,
        cp.OPTIMAL_INACCURATE,
    ):
        return {
            **base,
            "coefficient": float("nan"),
            "green": False,
        }

    e_v = np.asarray(
        e.value,
        dtype=float,
    )
    pphi_v = np.asarray(
        pphi.value,
        dtype=float,
    )
    prf_v = np.asarray(
        pr_face.value,
        dtype=float,
    )
    pzf_v = np.asarray(
        pz_face.value,
        dtype=float,
    )
    trzv_v = np.asarray(
        trz_vertex.value,
        dtype=float,
    )

    pr_v = 0.5 * (
        prf_v[:-1, :]
        + prf_v[1:, :]
    )
    pz_v = 0.5 * (
        pzf_v[:, :-1]
        + pzf_v[:, 1:]
    )
    trz_v = 0.25 * (
        trzv_v[:-1, :-1]
        + trzv_v[1:, :-1]
        + trzv_v[:-1, 1:]
        + trzv_v[1:, 1:]
    )

    active_v = (
        e_v
        + pr_v
        + pz_v
        + pphi_v
    )

    mass_v = float(
        np.sum(
            volumes * e_v
        )
    )
    acceleration_v = float(
        np.sum(
            kernels * active_v
        )
    )

    max_dec_violation = 0.0

    for i in range(nr):
        for j in range(nz):
            stress = np.array([
                [
                    pr_v[i, j],
                    trz_v[i, j],
                    0.0,
                ],
                [
                    trz_v[i, j],
                    pz_v[i, j],
                    0.0,
                ],
                [
                    0.0,
                    0.0,
                    pphi_v[i, j],
                ],
            ])

            largest = float(
                np.max(
                    np.abs(
                        np.linalg.eigvalsh(
                            stress
                        )
                    )
                )
            )

            max_dec_violation = max(
                max_dec_violation,
                largest - e_v[i, j],
            )

    max_conservation_residual = 0.0

    for i in range(nr):
        r0, r1 = (
            r_edges[i],
            r_edges[i + 1],
        )
        dr = r1 - r0
        annular_radial_factor = 0.5 * (
            r1 * r1 - r0 * r0
        )

        for j in range(nz):
            dz = (
                z_edges[j + 1]
                - z_edges[j]
            )

            trz_south = 0.5 * (
                trzv_v[i, j]
                + trzv_v[i + 1, j]
            )
            trz_north = 0.5 * (
                trzv_v[i, j + 1]
                + trzv_v[i + 1, j + 1]
            )
            trz_west = 0.5 * (
                trzv_v[i, j]
                + trzv_v[i, j + 1]
            )
            trz_east = 0.5 * (
                trzv_v[i + 1, j]
                + trzv_v[i + 1, j + 1]
            )

            rr = (
                dz
                * (
                    r1 * prf_v[i + 1, j]
                    - r0 * prf_v[i, j]
                )
                + annular_radial_factor
                * (
                    trz_north
                    - trz_south
                )
                - dr
                * dz
                * pphi_v[i, j]
            )

            zz = (
                2.0
                * dz
                * (
                    r1 * trz_east
                    - r0 * trz_west
                )
                + (
                    r1 * r1
                    - r0 * r0
                )
                * (
                    pzf_v[i, j + 1]
                    - pzf_v[i, j]
                )
            )

            max_conservation_residual = max(
                max_conservation_residual,
                abs(float(rr)),
                abs(float(zz)),
            )

    radial_laue = float(
        np.sum(
            volumes
            * (
                pr_v
                + pphi_v
            )
        )
    )
    vertical_laue = float(
        np.sum(
            volumes
            * pz_v
        )
    )
    trace_integral = (
        radial_laue
        + vertical_laue
    )

    active_total = float(
        np.sum(
            volumes
            * active_v
        )
    )
    active_total_relerr = (
        abs(
            active_total - mass_v
        )
        / max(
            abs(mass_v),
            1.0e-300,
        )
    )

    R, Z = np.meshgrid(
        r_centers,
        z_centers,
        indexing="ij",
    )

    energy_cell = (
        volumes
        * e_v
    )

    if case.core_radius is not None:
        core_mask_numeric = (
            R * R + Z * Z
            <= case.core_radius**2
        )
        core_active_numeric = float(
            np.sum(
                volumes[
                    core_mask_numeric
                ]
                * active_v[
                    core_mask_numeric
                ]
            )
        )
        core_active_fraction = (
            core_active_numeric
            / max(
                mass_v,
                1.0e-300,
            )
        )
    else:
        core_active_numeric = float("nan")
        core_active_fraction = float("nan")

    cell_force = (
        kernels
        * active_v
    )
    gross_outward = float(
        np.sum(
            np.maximum(
                cell_force,
                0.0,
            )
        )
    )
    gross_opposing = float(
        np.sum(
            np.maximum(
                -cell_force,
                0.0,
            )
        )
    )
    cancellation = (
        (
            gross_outward
            + gross_opposing
        )
        / max(
            abs(acceleration_v),
            1.0e-300,
        )
    )

    radius_center = np.sqrt(
        R * R + Z * Z
    )

    outer_energy_fraction = float(
        np.sum(
            energy_cell[
                radius_center
                >= 0.90 * case.radius
            ]
        )
        / max(
            mass_v,
            1.0e-300,
        )
    )

    occupied = (
        e_v
        > 1.0e-7
        * max(
            float(np.max(e_v)),
            1.0e-30,
        )
    )

    green = bool(
        math.isfinite(mass_v)
        and mass_v > 0.0
        and acceleration_v >= 1.0 - 2.0e-5
        and max_dec_violation < DEC_TOL
        and max_conservation_residual < CONS_TOL
        and abs(trace_integral) < TRACE_TOL
        and active_total_relerr < ACTIVE_TOTAL_REL_TOL
    )

    return {
        **base,
        "coefficient": mass_v,
        "acceleration": acceleration_v,
        "max_dec_violation": max_dec_violation,
        "max_conservation_residual": (
            max_conservation_residual
        ),
        "radial_laue": radial_laue,
        "vertical_laue": vertical_laue,
        "trace_integral": trace_integral,
        "active_total": active_total,
        "active_total_relerr": active_total_relerr,
        "core_active": core_active_numeric,
        "core_active_fraction": core_active_fraction,
        "gross_outward": gross_outward,
        "gross_opposing": gross_opposing,
        "cancellation": cancellation,
        "outer_10pct_energy_fraction": outer_energy_fraction,
        "occupied_fraction": float(
            np.mean(
                occupied[
                    active_mask
                ]
            )
        ) if np.any(active_mask) else 0.0,
        "max_energy_density": float(
            np.max(e_v)
        ),
        "green": green,
    }


def direct_006b_kernel_recovery(
    s006b,
    payload_radius: float,
) -> float:
    """Return maximum relative cell-kernel disagreement with exact 006B."""

    nr = 20
    nz = 2
    radius = 5.0
    zmin = -0.125
    zmax = 0.0
    target = 1.0

    r_edges = np.linspace(
        0.0,
        radius,
        nr + 1,
    )
    z_edges = np.linspace(
        zmin,
        zmax,
        nz + 1,
    )

    errors = []

    for i in range(nr):
        for j in range(nz):
            r0, r1 = (
                r_edges[i],
                r_edges[i + 1],
            )
            z0, z1 = (
                z_edges[j],
                z_edges[j + 1],
            )

            numeric = finite_payload_cell_kernel(
                r0,
                r1,
                z0,
                z1,
                target,
                payload_radius,
            )

            exact = s006b.exact_cell_axial_kernel(
                r0,
                r1,
                z0,
                z1,
                target_z=target,
            )

            errors.append(
                relative_error(
                    numeric,
                    exact,
                )
            )

    return float(max(errors))


def print_case(row: dict[str, Any], current_C: float):
    c = float(row.get("coefficient", float("nan")))
    green = bool(row.get("green", False))

    headroom = (
        current_C / c
        if green and math.isfinite(c) and c > 0.0
        else float("nan")
    )

    row["headroom_vs_current"] = headroom

    if math.isfinite(headroom) and headroom > 0.0:
        row["source_level_overhead_fraction"] = (
            1.0 - 1.0 / headroom
        )
    else:
        row["source_level_overhead_fraction"] = float("nan")

    print(
        f"INT14B_CASE={row['name']} "
        f"C={c:.15e} "
        f"HEADROOM={headroom:.15e} "
        f"STATUS={row['status']} "
        f"SOLVER={row['solver']} "
        f"GREEN={'YES' if green else 'NO'} "
        f"CORE_FRAC={float(row.get('core_active_fraction', float('nan'))):+.9e} "
        f"ACTIVE_TOTAL_RELERR={float(row.get('active_total_relerr', float('nan'))):.3e} "
        f"DEC={float(row.get('max_dec_violation', float('nan'))):.3e} "
        f"CONS={float(row.get('max_conservation_residual', float('nan'))):.3e} "
        f"BOUNDARY_E_FRAC={float(row.get('outer_10pct_energy_fraction', float('nan'))):.3e}",
        flush=True,
    )


def main() -> None:
    print(
        "=== INT-14B — SUPPORT-CONSTRAINED STRUCTURAL-OVERHEAD BRIDGE ===",
        flush=True,
    )

    for path in (
        INT14A_SUMMARY,
        INT02_SOURCE,
        A23_SOURCE,
        B23_SOURCE,
        S006B,
    ):
        require(path)

    prior = json.loads(
        INT14A_SUMMARY.read_text()
    )

    if not bool(
        prior.get(
            "gates",
            {},
        ).get(
            "two_route_ge10x",
            False,
        )
    ):
        raise RuntimeError(
            "INT-14A two-route >=10x gate did not pass"
        )

    current_C = float(
        prior["current_exact_map"]["C"]
    )
    prior_006b_C = float(
        next(
            row["coefficient"]
            for row
            in prior["source_006b"]
            if row["name"] == "KNOWN_THIN20"
        )
    )

    print("\n=== A — INT-14A AUTHORIZATION ===")
    print(f"CURRENT_C={current_C:.15e}")
    print(f"INT14A_006D_HEADROOM={float(prior['source_006d']['headroom_vs_current']):.15e}")
    print(f"INT14A_006B_HEADROOM={float(next(row['headroom_vs_current'] for row in prior['source_006b'] if row['name']=='KNOWN_THIN20')):.15e}")
    print("INT14A_TWO_ROUTE_GE10X=PASS")
    print(
        "EXPANSION_HUNDREDS_FOLD_HEADROOM_STATUS="
        "PRESERVED_AS_NONSTATIONARY_MECHANISM_CLUE"
    )

    int02 = load_module(
        "int14b_int02",
        INT02_SOURCE,
    )
    a23 = load_module(
        "int14b_a23",
        A23_SOURCE,
    )
    b23 = load_module(
        "int14b_b23",
        B23_SOURCE,
    )
    s006b = load_module(
        "int14b_006b",
        S006B,
    )

    print("\n=== B — EXACT B=7 SUPPORT ANATOMY ===", flush=True)

    anatomy = exact_map_support_anatomy(
        int02,
        a23,
        b23,
    )

    h = anatomy["h"]
    q_payload = anatomy["payload_radius_over_h"]

    r90 = anatomy["R90_over_h"]
    r95 = anatomy["R95_over_h"]
    r99 = anatomy["R99_over_h"]

    core_radius = anatomy["core_radius_over_h"]
    core_fraction = anatomy["core_active_fraction"]

    print(f"EXACT_R90_OVER_H={r90:.15e}")
    print(f"EXACT_R95_OVER_H={r95:.15e}")
    print(f"EXACT_R99_OVER_H={r99:.15e}")
    print(f"EXACT_SHELL_RADIUS_OVER_H={anatomy['shell_radius_over_h']:.15e}")
    print(f"EXACT_NEGATIVE_ACTIVE_OUTER_OVER_H={anatomy['negative_active_outer_over_h']:.15e}")
    print(f"PAYLOAD_RADIUS_OVER_H={q_payload:.15e}")
    print(f"PAYLOAD_OUTER_CORE_RADIUS_OVER_H={core_radius:.15e}")
    print(f"EXACT_CORE_ACTIVE_FRACTION={core_fraction:+.15e}")
    print(f"EXACT_ACTIVE_TOTAL_OVER_E={anatomy['active_total_over_E']:.15e}")

    if not (
        core_fraction < 0.0
        and core_radius
        < anatomy["negative_active_outer_over_h"]
    ):
        raise RuntimeError(
            "Exact payload is not safely inside negative-enclosed-active region"
        )

    print("\n=== C — GENERALIZED KERNEL / 006B RECOVERY ===", flush=True)

    kernel_relerr = direct_006b_kernel_recovery(
        s006b,
        q_payload,
    )

    recovery_case = SupportCase(
        name="RECOVERY_006B_KNOWN_THIN20",
        nr=20,
        nz=2,
        radius=5.0,
        zmin=-0.125,
        zmax=0.0,
        target_z=1.0,
        payload_radius=q_payload,
        spherical_mask=False,
        reflection_symmetry=False,
        category="VALIDATION",
    )

    recovery = solve_support_case(
        recovery_case
    )

    recovery_C = float(
        recovery.get(
            "coefficient",
            float("nan"),
        )
    )

    recovery_relerr = relative_error(
        recovery_C,
        prior_006b_C,
    )

    recovery_pass = bool(
        recovery.get("green", False)
        and kernel_relerr
        <= KERNEL_RECOVERY_REL_TOL
        and recovery_relerr
        <= RECOVERY_C_REL_TOL
    )

    print(f"KERNEL_006B_MAX_RELERR={kernel_relerr:.15e}")
    print(f"RECOVERY_006B_C={recovery_C:.15e}")
    print(f"RECOVERY_006B_PRIOR_C={prior_006b_C:.15e}")
    print(f"RECOVERY_006B_C_RELERR={recovery_relerr:.15e}")
    print(
        "GENERALIZED_006B_RECOVERY="
        + ("PASS" if recovery_pass else "FAIL")
    )

    if not recovery_pass:
        raise RuntimeError(
            "Generalized solver failed 006B recovery"
        )

    rows: list[dict[str, Any]] = []

    print("\n=== D — R99 MATCHED-CORE RESOLUTION SEQUENCE ===", flush=True)

    resolution_cases = [
        SupportCase(
            "R99_MATCHED_CORE_N8",
            8,
            16,
            r99,
            -r99,
            +r99,
            1.0,
            q_payload,
            spherical_mask=True,
            reflection_symmetry=True,
            core_radius=core_radius,
            core_fraction_target=core_fraction,
            category="R99_MATCHED_CORE_RESOLUTION",
        ),
        SupportCase(
            "R99_MATCHED_CORE_N12",
            12,
            24,
            r99,
            -r99,
            +r99,
            1.0,
            q_payload,
            spherical_mask=True,
            reflection_symmetry=True,
            core_radius=core_radius,
            core_fraction_target=core_fraction,
            category="R99_MATCHED_CORE_RESOLUTION",
        ),
        SupportCase(
            "R99_MATCHED_CORE_N16",
            16,
            32,
            r99,
            -r99,
            +r99,
            1.0,
            q_payload,
            spherical_mask=True,
            reflection_symmetry=True,
            core_radius=core_radius,
            core_fraction_target=core_fraction,
            category="R99_MATCHED_CORE_RESOLUTION",
        ),
    ]

    for case in resolution_cases:
        print(
            f"INT14B_SOLVE_BEGIN={case.name} "
            f"GRID={case.nr}x{case.nz} "
            f"R_SUPPORT={case.radius:.9e}",
            flush=True,
        )

        row = solve_support_case(case)
        print_case(row, current_C)
        rows.append(row)

    r99_primary = rows[1]
    r99_high = rows[2]

    primary_green = bool(
        r99_primary.get("green", False)
    )
    high_green = bool(
        r99_high.get("green", False)
    )

    if primary_green and high_green:
        c_primary = float(
            r99_primary["coefficient"]
        )
        c_high = float(
            r99_high["coefficient"]
        )

        c_rel_diff = relative_error(
            c_primary,
            c_high,
        )

        conservative_C = max(
            c_primary,
            c_high,
        )
        conservative_headroom = (
            current_C
            / conservative_C
        )
    else:
        c_rel_diff = float("nan")
        conservative_C = float("nan")
        conservative_headroom = float("nan")

    print(f"R99_PRIMARY_HIGH_C_REL_DIFF={c_rel_diff:.15e}")
    print(f"R99_CONSERVATIVE_C={conservative_C:.15e}")
    print(f"R99_CONSERVATIVE_HEADROOM={conservative_headroom:.15e}")

    r99_formal_pass = bool(
        primary_green
        and high_green
        and c_rel_diff
        <= PRIMARY_HIGH_C_REL_TOL
        and conservative_headroom
        >= HEADROOM_MAJOR
    )

    print(
        "R99_MATCHED_CORE_GE10X_CONVERGED="
        + ("PASS" if r99_formal_pass else "FAIL")
    )

    print("\n=== E — SUPPORT / CORE SENSITIVITY ===", flush=True)

    sensitivity_cases = [
        SupportCase(
            "R95_MATCHED_CORE_N12",
            12,
            24,
            r95,
            -r95,
            +r95,
            1.0,
            q_payload,
            spherical_mask=True,
            reflection_symmetry=True,
            core_radius=core_radius,
            core_fraction_target=core_fraction,
            category="SUPPORT_SENSITIVITY",
        ),
        SupportCase(
            "R90_MATCHED_CORE_N12",
            12,
            24,
            r90,
            -r90,
            +r90,
            1.0,
            q_payload,
            spherical_mask=True,
            reflection_symmetry=True,
            core_radius=core_radius,
            core_fraction_target=core_fraction,
            category="SUPPORT_SENSITIVITY",
        ),
        SupportCase(
            "R99_SIGN_ONLY_N12",
            12,
            24,
            r99,
            -r99,
            +r99,
            1.0,
            q_payload,
            spherical_mask=True,
            reflection_symmetry=True,
            core_radius=core_radius,
            core_fraction_target=0.0,
            category="CORE_SENSITIVITY",
        ),
    ]

    for case in sensitivity_cases:
        print(
            f"INT14B_SOLVE_BEGIN={case.name}",
            flush=True,
        )

        row = solve_support_case(case)
        print_case(row, current_C)
        rows.append(row)

    fallback_rows: list[dict[str, Any]] = []

    if not r99_formal_pass:
        print(
            "\n=== F — EXPANSION-COMPATIBILITY FALLBACK ===",
            flush=True,
        )

        gamma_specs = [
            (1.125, "PHYSICAL_SUPPORT_PROBE"),
            (1.25, "EXPANSION_LINKED_SUPPORT_PROBE"),
            (1.50, "PHYSICAL_SUPPORT_PROBE"),
            (1.6, "BLIND_WILDCARD_DIAGNOSTIC"),
            (1.875, "BLIND_WILDCARD_DIAGNOSTIC"),
        ]

        for gamma, category in gamma_specs:
            support_r = gamma * r99

            case = SupportCase(
                name=(
                    "R99_EXPANDED_GAMMA_"
                    + str(gamma).replace(".", "P")
                    + "_N10"
                ),
                nr=10,
                nz=20,
                radius=support_r,
                zmin=-support_r,
                zmax=+support_r,
                target_z=1.0,
                payload_radius=q_payload,
                spherical_mask=True,
                reflection_symmetry=True,
                core_radius=core_radius,
                core_fraction_target=core_fraction,
                category=category,
            )

            print(
                f"INT14B_FALLBACK_BEGIN GAMMA={gamma:.6f} "
                f"CATEGORY={category}",
                flush=True,
            )

            row = solve_support_case(case)
            row["support_gamma_vs_R99"] = gamma
            print_case(row, current_C)

            fallback_rows.append(row)
            rows.append(row)

    physical_fallback_passers = [
        row
        for row in fallback_rows
        if (
            row.get("category")
            != "BLIND_WILDCARD_DIAGNOSTIC"
            and bool(row.get("green", False))
            and float(row.get(
                "headroom_vs_current",
                float("nan"),
            )) >= HEADROOM_MAJOR
        )
    ]

    if physical_fallback_passers:
        first_support_pass = min(
            physical_fallback_passers,
            key=lambda row: float(
                row["support_gamma_vs_R99"]
            ),
        )
        minimum_support_gamma = float(
            first_support_pass[
                "support_gamma_vs_R99"
            ]
        )
    else:
        minimum_support_gamma = float("nan")

    print("\n=== G — STRUCTURAL-OVERHEAD DECISION ===")

    if r99_formal_pass:
        formal_level3 = True
        decision = (
            "FORMAL_INT_LEVEL_3_ACTIONABLE_SOURCE_ORGANIZATION_HEADROOM_"
            "R99_MATCHED_CORE_GE10X"
        )
        next_action = (
            "INT09_MANDATORY_SCAFFOLDING_AND_FIELD_SPACE_ACCESSIBILITY"
        )
    elif math.isfinite(minimum_support_gamma):
        formal_level3 = False
        decision = (
            "GE10X_HEADROOM_REQUIRES_SUPPORT_EXPANSION_"
            "SAME_SUPPORT_ACCESSIBILITY_NOT_ESTABLISHED"
        )
        next_action = (
            "INT14C_REFINE_MINIMUM_SUPPORT_EXPANSION_AND_COMPARE_"
            "WITH_DILATION_SOFT_MODE"
        )
    else:
        formal_level3 = False
        decision = (
            "COMPACT_MATCHED_CORE_GE10X_HEADROOM_NOT_ESTABLISHED"
        )
        next_action = (
            "RETURN_TO_023C_023D_GLOBAL_RERANK_OR_HESSIAN_ONLY_IF_ALREADY_REQUIRED"
        )

    print(
        "INT_LEVEL_3_FORMAL="
        + ("PASS" if formal_level3 else "NOT_YET")
    )
    print(f"INT14B_DECISION={decision}")
    print(f"MINIMUM_TESTED_PHYSICAL_SUPPORT_GAMMA_GE10X={minimum_support_gamma:.15e}")
    print(
        "EXPANSION_HUNDREDS_FOLD_HEADROOM_STATUS="
        "PRESERVED_AS_NONSTATIONARY_MECHANISM_CLUE"
    )
    print(
        "SOURCE_LEVEL_STRUCTURAL_OVERHEAD_IS_REMOVABLE_FIELD_ENERGY="
        "NO"
    )
    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )
    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "APPROXIMATELY_70_TO_71_PERCENT_PENDING_THIS_GATE_INTERPRETATION"
    )
    print(f"NEXT={next_action}")
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_INT14B_SUPPORT_CONSTRAINED_STRUCTURAL_OVERHEAD_BRIDGE"
    )

    fieldnames = sorted({
        key
        for row in rows
        for key in row.keys()
    })

    with OUT_CSV.open(
        "w",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "claim_classification": (
            "PROJECT_DERIVED_INT14B_SUPPORT_CONSTRAINED_STRUCTURAL_OVERHEAD_BRIDGE"
        ),
        "decision": decision,
        "next": next_action,
        "current_C": current_C,
        "int14a_two_route_ge10x": True,
        "exact_support_anatomy": anatomy,
        "validation": {
            "kernel_006b_max_relerr": kernel_relerr,
            "recovery_006b_C": recovery_C,
            "prior_006b_C": prior_006b_C,
            "recovery_C_relerr": recovery_relerr,
            "pass": recovery_pass,
        },
        "r99_resolution": {
            "primary_high_C_rel_diff": c_rel_diff,
            "conservative_C": conservative_C,
            "conservative_headroom": conservative_headroom,
            "formal_pass": r99_formal_pass,
        },
        "minimum_tested_physical_support_gamma_ge10x": (
            minimum_support_gamma
        ),
        "cases": rows,
        "gates": {
            "generalized_006b_recovery": recovery_pass,
            "r99_matched_core_ge10x_converged": r99_formal_pass,
            "int_level_3_formal": formal_level3,
        },
        "claim_limits": {
            "axisymmetric_proxy_is_exact_b7": False,
            "source_proxy_is_microscopic_field": False,
            "structural_overhead_is_removable_field_energy": False,
            "strict_n73": False,
            "full_hessian_stability": False,
            "nonlinear_einstein_skyrme": False,
            "practical_device": False,
        },
    }

    OUT_JSON.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
            allow_nan=True,
        )
        + "\n"
    )

    print(f"INT14B_SUMMARY_JSON={OUT_JSON}")
    print(f"INT14B_CASES_CSV={OUT_CSV}")
    print("INT14B_RUN_COMPLETE=YES")


if __name__ == "__main__":
    main()
