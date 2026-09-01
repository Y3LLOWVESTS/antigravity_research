#!/usr/bin/env python3
"""023B — exact rational-map + full-3D T_munu/gravity promotion gate.

PURPOSE
-------
Attempt the first promotion beyond the current approximately-68-percent
knowledge milestone on the newly opened topological-GR branch.

023A established a strong positive CAPACITY result in a rational-map radial
reduction:

    topological charge;
    intrinsic Skyrme/Derrick stabilization;
    negative enclosed active mass;
    positive total active mass;
    binary-fission binding at the selected point;
    outward finite-payload MONOPOLE gravity.

However, 023A used the approximate angular integral

    I approximately 1.28 B^2

and did not directly reconstruct the anisotropic 3D stress-energy or the
anisotropic 3D gravitational field of the actual polyhedral rational map.

A post-run audit also noted that the weakest robustness fission margin fell
below the original 0.2-percent promotion threshold.

023B therefore combines the cheapest remaining decisive checks in ONE run:

1. replace 1.28 B^2 by the published minimal rational-map I values for
   B=1,...,8;

2. re-solve all radial sectors and every binary-fission channel;

3. identify the best exact-map survivor rather than preserving the old B=8
   choice;

4. reconstruct the actual degree-B rational map angular field;

5. independently integrate the complete anisotropic 3D energy and active
   source;

6. reconstruct pointwise principal stresses and directly test DEC on a dense
   3D quadrature;

7. integrate the actual anisotropic 3D linearized-GR field on a finite
   spherical payload at several orientations, instead of using only the
   monopole;

8. test rational-map shape curvature around the selected map parameter;

9. rerun fission robustness with the exact literature I values and numerical
   I uncertainty;

10. fail closed unless all checks agree.

This is still a rational-map field class, not an unrestricted Cartesian PDE
relaxation.  Therefore even a GREEN result is classified conservatively as a

    FULL_3D_RATIONAL_MAP_STABLE_FIELD_THEORY_PREFLIGHT

rather than a proof of the complete unconstrained 3D spectrum.

If the exact 3D result is robust and the claim audit accepts the remaining
ansatz limitation, the project may become eligible for the approximately
70-to-72-percent internal milestone.  The script itself does not declare a
new-physics discovery or practical device.

SCIENTIFIC QUESTION
-------------------
Does a literature-backed, low-charge, intrinsically topological false-core
Skyrmion survive exact rational-map angular data, robust binary fission,
pointwise positive-energy/DEC checks, and the ACTUAL anisotropic finite-payload
3D gravity integral?

OPERATIONAL OBSERVABLE
----------------------
The primary observable is the finite-payload center-of-mass acceleration
projected radially outward from the Skyrmion center.

For a payload center x_c and payload volume V_p,

    <a>_p
      =
    (1/V_p)
    integral_(V_p) a(x) d^3x.

The source is the complete active density

    S(x)
      =
    rho + p_1 + p_2 + p_3
      =
    2 (e_4 - V).

The 3D linearized-GR acceleration, up to one common positive factor, is

    a(x)
      =
    - integral
      S(x')
      [x-x']
      /
      |x-x'|^3
      d^3x'.

A positive projection

    <a>_p . x_c/|x_c| > 0

is outward.

MODEL
-----
The model and false-vacuum potential are inherited from 023A:

    U
      =
    cos F
      +
    i sin F n_R . tau

and

    V(F)
      =
    m^2 (1-cos F)(1+eta cos F).

The promotion-grade basin remains

    1 <= B <= 8,

    eta =
        0.36,
        0.40,
        0.50,
        0.70,

    m =
        1,
        2,
        3,
        5,
        8.

EXACT LITERATURE RATIONAL-MAP DATA
----------------------------------
Houghton, Manton and Sutcliffe give the minimal rational-map angular
integrals:

    B=1 : I= 1.00
    B=2 : I= 5.81
    B=3 : I=13.58
    B=4 : I=20.65
    B=5 : I=35.75
    B=6 : I=50.76
    B=7 : I=60.87
    B=8 : I=85.63.

The published B=7 minimal map has icosahedral/dodecahedral symmetry.  A useful
orientation is

    R(z)
      =
    [
        b z^6 - 7 z^4 - b z^2 - 1
    ]
    /
    [
        z (z^6 + b z^4 + 7 z^2 - b)
    ],

with

    b = 7/sqrt(5).

The code independently reconstructs:

    degree integral = 7,

    I approximately 60.87

by direct angular quadrature before using the map for gravity.

POINTWISE 3D STRESS
-------------------
For a conformal rational map define the local angular stretch

    J
      =
    (1+|z|^2)
    |dR/dz|
    /
    (1+|R|^2).

In a local orthonormal spherical frame let

    a = F'^2,

    b_ang
      =
    sin^2(F) J^2/r^2.

Then

    e_2 = a + 2 b_ang,

    e_4 = 2 a b_ang + b_ang^2,

    rho = e_2 + e_4 + V.

The principal pressures are

    p_r
      =
    a - 2 b_ang
      +
    2 a b_ang - b_ang^2
      -
    V,

    p_t
      =
    -a + b_ang^2 - V.

There are two identical tangential pressures because the rational map is
conformal.

The active trace identity is therefore reconstructed pointwise:

    rho + p_r + 2 p_t
      =
    2(e_4 - V).

DEC requires

    rho >= 0,

    rho >= |p_r|,

    rho >= |p_t|.

The run checks these directly over the 3D quadrature rather than relying only
on the general literature theorem.

INDEPENDENT 3D ENERGY RECONSTRUCTION
------------------------------------
The exact angular-map identities are

    (1/4pi) integral J^2 dOmega = B,

    (1/4pi) integral J^4 dOmega = I.

Therefore the direct 3D quadrature of e_2, e_4 and V must reproduce the radial
rational-map energies.

This is an independent reconstruction of the central source.

FULL 3D FINITE-PAYLOAD GRAVITY
------------------------------
The source quadrature uses:

    Gauss-Legendre radial integration,
    Gauss-Legendre mu=cos(theta),
    uniform midpoint phi.

The payload is sampled by a deterministic equal-volume spherical rule.

The selected payload geometry is inherited from the 023A best operating point
for the newly selected exact-map sector.

The actual anisotropic 3D source is tested along several payload-center
orientations:

    +z,
    +x,
    (1,1,1),
    (1,1,0),
    (1,2,3),
    (2,-1,1).

Every tested orientation must retain an outward volume-averaged radial
acceleration.

The run also reports the anisotropy spread and agreement with the 023A
monopole prediction.

RATIONAL-MAP SHAPE STABILITY
-----------------------------
For the selected B=7 map, perturb

    b = b_0 (1 + epsilon)

with

    epsilon =
        +/-0.01,
        +/-0.02,
        +/-0.04.

For every b, independently integrate I(b), re-solve the radial BVP, and compute
the total energy.

The symmetric second difference must be positive:

    E(+eps)+E(-eps)-2E(0) > 0.

This probes the dominant one-parameter icosahedral rational-map deformation
family.

It is not the complete unrestricted 3D Hessian.

EXACT FISSION ROBUSTNESS
------------------------
For every parameter point, all charge sectors B=1,...,8 are re-solved using
the literature I values.

For a selected B require

    E_B < E_k + E_(B-k)

for every binary split.

The central promotion margin is

    min_k
    [E_k + E_(B-k)-E_B]/E_B >= 0.002.

Robustness repeats the selected candidate under:

    eta +/- 0.04,
    m x {0.8,1,1.2},
    BVP tolerances {1e-4,2e-5,5e-6},
    domains {0.8,1,1.3},
    each literature I_B varied coherently by +/-0.15%.

For parameter/model perturbations that re-evaluate fission, require the full
0.002 margin rather than merely positivity.

PROMOTION CONDITION
-------------------
A promotion-grade GREEN requires all of:

    EXACT_LITERATURE_I_TABLE=PASS

    EXACT_B7_MAP_DEGREE=PASS

    EXACT_B7_MAP_I=PASS

    RATIONAL_MAP_BVP=PASS

    TOPOLOGICAL_CHARGE=PASS

    DERRICK_VIRIAL=PASS

    EXACT_BINARY_FISSION_MARGIN=PASS

    ROBUST_BINARY_FISSION_MARGIN=PASS

    NEGATIVE_ENCLOSED_ACTIVE_MASS=PASS

    POSITIVE_TOTAL_ACTIVE_MASS=PASS

    POINTWISE_3D_DEC=PASS

    FULL_3D_ENERGY_RECONSTRUCTION=PASS

    FULL_3D_ACTIVE_TRACE_RECONSTRUCTION=PASS

    FULL_3D_FINITE_PAYLOAD_OUTWARD_ALL_ORIENTATIONS=PASS

    RATIONAL_MAP_SHAPE_CURVATURE=PASS

    INDEPENDENT_RECONSTRUCTION=PASS

    ROBUST_PARAMETER_BASIN=YES.

If all pass, the script may output:

    023B_EXACT_RATIONAL_MAP_FULL3D_T_MUNU_GRAVITY_PROMOTION_GATE=GREEN

    FULL_3D_RATIONAL_MAP_STABLE_FIELD_THEORY_PREFLIGHT=SUPPORTED

    HEURISTIC_PROMOTION_ELIGIBILITY=
    APPROXIMATELY_70_TO_72_PERCENT_AFTER_CLAIM_AUDIT.

The project must still distinguish this from an unrestricted full Cartesian
Euler-Lagrange/Hessian proof.

FALSIFIER
---------
Any of the following prevents promotion:

    exact literature I removes binding;

    exact 3D source loses outward finite-payload gravity;

    DEC fails;

    3D/radial energy accounting disagrees;

    map-shape curvature is negative;

    robust binary fission falls below 0.002;

    result depends on one orientation.

STOP RULE
---------
If this gate fails, do not escalate to a huge-B Skyrmion.

If this gate is GREEN, the next action is an unrestricted Cartesian 3D
relaxation/eigenmode confirmation plus nonlinear Einstein-matter scaling,
rather than another rational-map scan.

APPROXIMATION LEVEL
-------------------
Flat-spacetime matter fields plus linearized-GR gravity.

The source field is a genuine anisotropic 3D rational-map field but remains
restricted to the rational-map ansatz class.

No nonlinear Einstein backreaction, laboratory material realization, payload
backreaction, or practical energy solution is claimed.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023B_EXACT_RATIONAL_MAP_FULL3D_T_MUNU_GRAVITY_PROMOTION_GATE
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib.util
import math
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import PchipInterpolator


ROOT = Path(__file__).resolve().parents[1]

A23_SOURCE = (
    ROOT
    / "simulations"
    / "023a_topological_false_core_multiskyrmion_gr_repulsion_gate.py"
)
A23_LOG = (
    ROOT
    / "results/logs"
    / "023a_topological_false_core_multiskyrmion_gr_repulsion_gate.log"
)

EXPECTED_023A_SHA256 = (
    "0087a5d2b4f93667308cabf4c3c498200ed29381e9493acf21714df7d8e11c9b"
)

LITERATURE_I = {
    1: 1.00,
    2: 5.81,
    3: 13.58,
    4: 20.65,
    5: 35.75,
    6: 50.76,
    7: 60.87,
    8: 85.63,
}

B_VALUES = tuple(range(1, 9))
ETA_VALUES = (0.36, 0.40, 0.50, 0.70)
M_VALUES = (1.0, 2.0, 3.0, 5.0, 8.0)

B7_B0 = 7.0 / math.sqrt(5.0)

MIN_NEGATIVE_ACTIVE_FRACTION = 1.0e-2
MIN_FISSION_MARGIN = 2.0e-3
MAX_VIRIAL_RELERR = 5.0e-4
MAX_ACTIVE_TOTAL_RELERR = 2.0e-3
MAX_TOPOLOGY_RELERR = 1.0e-8

MAX_I_RECON_RELERR = 5.0e-4
MAX_3D_ENERGY_RELERR = 3.0e-3
MAX_3D_ACTIVE_RELERR = 3.0e-3
MIN_DEC_MARGIN = -2.0e-10

ANGULAR_MU_N = 64
ANGULAR_PHI_N = 128

GR_RADIAL_N = 68
GR_MU_N = 32
GR_PHI_N = 64

PAYLOAD_RADIAL_N = 4
PAYLOAD_MU_N = 6
PAYLOAD_PHI_N = 12

MAP_EPSILONS = (0.01, 0.02, 0.04)

I_UNCERTAINTY = 1.5e-3

ROBUST_TOLS = (1.0e-4, 2.0e-5, 5.0e-6)
ROBUST_DOMAIN_FACTORS = (0.8, 1.0, 1.3)

ORIENTATION_VECTORS = (
    (0.0, 0.0, 1.0),
    (1.0, 0.0, 0.0),
    (1.0, 1.0, 1.0),
    (1.0, 1.0, 0.0),
    (1.0, 2.0, 3.0),
    (2.0, -1.0, 1.0),
)

BLIND_WILDCARDS = (1.6, 1.875, 3.125, 0.625, 5.0)


@dataclass(frozen=True)
class ExactCandidate:
    """One exact-I radial candidate with fission and payload diagnostics."""

    profile: object
    fission_margin: float
    payload: object


def require_marker(path: Path, marker: str) -> None:
    """Fail closed unless an exact upstream marker is present."""

    if not path.exists():
        raise RuntimeError(f"Missing upstream log: {path}")

    text = path.read_text(errors="replace")

    if marker not in text:
        raise RuntimeError(
            f"Missing required marker in {path.name}: {marker}"
        )


def sha256(path: Path) -> str:
    """Return SHA-256."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def relative_error(a: float, b: float) -> float:
    """Stable relative error."""

    return abs(a - b) / max(abs(a), abs(b), 1.0e-300)


def i_ratio_for(B: int, scale: float = 1.0) -> float:
    """Convert an exact literature I value into 023A's i_ratio argument."""

    if B == 1:
        return 1.28

    return (
        LITERATURE_I[B]
        * scale
        / (B * B)
    )


def solve_exact_profile(
    a23,
    B: int,
    eta: float,
    m: float,
    i_scale: float = 1.0,
    tol: float = 2.0e-5,
    domain_factor: float = 1.0,
):
    """Solve one exact-I rational-map radial profile."""

    return a23.solve_profile(
        B,
        eta,
        m,
        i_ratio=i_ratio_for(B, i_scale),
        tol=tol,
        domain_factor=domain_factor,
    )


def solve_exact_sector(
    a23,
    eta: float,
    m: float,
    i_scale: float = 1.0,
    tol: float = 2.0e-5,
    domain_factor: float = 1.0,
):
    """Solve B=1..8 consistently and return profiles plus energies."""

    profiles = {}

    for B in B_VALUES:
        profiles[B] = solve_exact_profile(
            a23,
            B,
            eta,
            m,
            i_scale=i_scale,
            tol=tol,
            domain_factor=domain_factor,
        )

    energies = {
        B: profiles[B].E
        for B in B_VALUES
    }

    return profiles, energies


def candidate_from_sector(a23, profiles, energies, B: int) -> ExactCandidate:
    """Attach exact binary-fission and finite-payload diagnostics."""

    margin = a23.binary_fission_margin(
        energies,
        B,
    )

    candidate = a23.make_candidate(
        profiles[B],
        energies,
    )

    return ExactCandidate(
        profile=profiles[B],
        fission_margin=margin,
        payload=candidate,
    )


def core_pass(a23, candidate: ExactCandidate) -> bool:
    """Promotion-grade exact-I radial predicate."""

    p = candidate.profile

    return (
        p.success
        and p.topology_relerr <= MAX_TOPOLOGY_RELERR
        and p.virial_relerr <= MAX_VIRIAL_RELERR
        and p.active_total_relerr <= MAX_ACTIVE_TOTAL_RELERR
        and p.min_active_fraction <= -MIN_NEGATIVE_ACTIVE_FRACTION
        and candidate.fission_margin >= MIN_FISSION_MARGIN
        and candidate.payload.finite_payload_pass
        and candidate.payload.payload_outward_kernel > 0.0
        and a23.profile_passes_core(p)
    )


def scan_exact_basin(a23):
    """Reconstruct the complete promotion basin using published I values."""

    all_candidates = []

    for eta in ETA_VALUES:
        for m in M_VALUES:
            profiles, energies = solve_exact_sector(
                a23,
                eta,
                m,
            )

            for B in range(2, 9):
                all_candidates.append(
                    candidate_from_sector(
                        a23,
                        profiles,
                        energies,
                        B,
                    )
                )

    passers = [
        c
        for c in all_candidates
        if core_pass(a23, c)
    ]

    return all_candidates, passers


def selected_rank(candidate: ExactCandidate):
    """Prefer strong fission margin, strong repulsion, and low payload C."""

    return (
        -candidate.fission_margin,
        candidate.payload.payload_coefficient_c,
        candidate.profile.virial_relerr,
    )


def b7_pq_and_derivatives(z: np.ndarray, b: float):
    """Return p,q,p',q' for the published B=7 rational-map family."""

    p = (
        b * z**6
        - 7.0 * z**4
        - b * z**2
        - 1.0
    )

    q = (
        z
        * (
            z**6
            + b * z**4
            + 7.0 * z**2
            - b
        )
    )

    pp = (
        6.0 * b * z**5
        - 28.0 * z**3
        - 2.0 * b * z
    )

    qq = (
        (
            z**6
            + b * z**4
            + 7.0 * z**2
            - b
        )
        +
        z
        * (
            6.0 * z**5
            + 4.0 * b * z**3
            + 14.0 * z
        )
    )

    return p, q, pp, qq


def b7_angular_j(mu: np.ndarray, phi: np.ndarray, b: float):
    """Return conformal stretch J on a tensor angular grid."""

    t = np.sqrt(
        (1.0 - mu[:, None])
        /
        (1.0 + mu[:, None])
    )

    z = (
        t
        * np.exp(
            1j * phi[None, :]
        )
    )

    p, q, pp, qq = b7_pq_and_derivatives(
        z,
        b,
    )

    numerator = np.abs(
        pp * q - p * qq
    )

    denominator = (
        np.abs(p)**2
        +
        np.abs(q)**2
    )

    J = (
        (1.0 + np.abs(z)**2)
        * numerator
        / denominator
    )

    return J


def angular_integrals_b7(
    b: float,
    n_mu: int = ANGULAR_MU_N,
    n_phi: int = ANGULAR_PHI_N,
):
    """Directly reconstruct degree and I for one B=7 map."""

    mu, w_mu = leggauss(
        n_mu
    )

    phi = (
        (
            np.arange(n_phi)
            + 0.5
        )
        * 2.0
        * math.pi
        / n_phi
    )

    J = b7_angular_j(
        mu,
        phi,
        b,
    )

    dphi = (
        2.0
        * math.pi
        / n_phi
    )

    degree = (
        np.sum(
            w_mu[:, None]
            * J**2
        )
        * dphi
        / (
            4.0
            * math.pi
        )
    )

    I = (
        np.sum(
            w_mu[:, None]
            * J**4
        )
        * dphi
        / (
            4.0
            * math.pi
        )
    )

    return float(degree), float(I)


def solve_profile_with_custom_I(
    a23,
    B: int,
    eta: float,
    m: float,
    I: float,
):
    """Solve a profile using one directly reconstructed angular I."""

    ratio = (
        1.28
        if B == 1
        else I / (B * B)
    )

    return a23.solve_profile(
        B,
        eta,
        m,
        i_ratio=ratio,
    )


def map_shape_curvature(a23, selected: ExactCandidate):
    """Test positive energy curvature in the published B=7 map family."""

    if selected.profile.B != 7:
        return False, [], float("nan")

    central_degree, central_I = angular_integrals_b7(
        B7_B0
    )

    central_profile = solve_profile_with_custom_I(
        a23,
        7,
        selected.profile.eta,
        selected.profile.m,
        central_I,
    )

    records = []
    min_curvature = math.inf

    for eps in MAP_EPSILONS:
        b_minus = (
            B7_B0 * (1.0 - eps)
        )
        b_plus = (
            B7_B0 * (1.0 + eps)
        )

        _, I_minus = angular_integrals_b7(
            b_minus
        )
        _, I_plus = angular_integrals_b7(
            b_plus
        )

        p_minus = solve_profile_with_custom_I(
            a23,
            7,
            selected.profile.eta,
            selected.profile.m,
            I_minus,
        )

        p_plus = solve_profile_with_custom_I(
            a23,
            7,
            selected.profile.eta,
            selected.profile.m,
            I_plus,
        )

        curvature = (
            p_plus.E
            +
            p_minus.E
            -
            2.0 * central_profile.E
        ) / (
            eps * eps
        )

        min_curvature = min(
            min_curvature,
            curvature,
        )

        records.append(
            (
                eps,
                I_minus,
                central_I,
                I_plus,
                p_minus.E,
                central_profile.E,
                p_plus.E,
                curvature,
            )
        )

    return (
        min_curvature > 0.0,
        records,
        min_curvature,
    )


def direct_3d_reconstruction(profile, b: float):
    """Reconstruct energy, active trace, and DEC on anisotropic 3D quadrature."""

    mu, w_mu = leggauss(
        ANGULAR_MU_N
    )

    phi = (
        (
            np.arange(
                ANGULAR_PHI_N
            )
            + 0.5
        )
        * 2.0
        * math.pi
        / ANGULAR_PHI_N
    )

    J = b7_angular_j(
        mu,
        phi,
        b,
    )

    dphi = (
        2.0
        * math.pi
        / ANGULAR_PHI_N
    )

    # Angular weights.
    w_ang = (
        w_mu[:, None]
        * np.ones(
            (
                1,
                ANGULAR_PHI_N,
            )
        )
        * dphi
    )

    r = profile.r
    F = profile.F
    Fp = profile.Fp

    E2_shell = np.zeros_like(r)
    E4_shell = np.zeros_like(r)
    E0_shell = np.zeros_like(r)
    A_shell = np.zeros_like(r)

    min_dec_margin = math.inf
    min_rho = math.inf
    max_trace_relerr = 0.0

    J2 = J**2
    J4 = J**4

    for index in range(len(r)):
        radius = float(r[index])

        if radius <= 0.0:
            continue

        s2 = math.sin(
            float(F[index])
        ) ** 2

        a = float(
            Fp[index] ** 2
        )

        b_ang = (
            s2
            * J2
            / (
                radius * radius
            )
        )

        e2 = (
            a
            +
            2.0 * b_ang
        )

        e4 = (
            2.0
            * a
            * b_ang
            +
            b_ang**2
        )

        V = float(
            profile.e0_density[index]
        )

        rho = (
            e2
            +
            e4
            +
            V
        )

        pr = (
            a
            -
            2.0 * b_ang
            +
            2.0 * a * b_ang
            -
            b_ang**2
            -
            V
        )

        pt = (
            -a
            +
            b_ang**2
            -
            V
        )

        active = (
            rho
            +
            pr
            +
            2.0 * pt
        )

        active_expected = (
            2.0
            * (
                e4 - V
            )
        )

        trace_err = np.max(
            np.abs(
                active
                -
                active_expected
            )
            /
            np.maximum(
                np.abs(active_expected),
                1.0e-12,
            )
        )

        max_trace_relerr = max(
            max_trace_relerr,
            float(trace_err),
        )

        dec_margin = np.minimum(
            rho - np.abs(pr),
            rho - np.abs(pt),
        )

        min_dec_margin = min(
            min_dec_margin,
            float(
                np.min(
                    dec_margin
                )
            ),
        )

        min_rho = min(
            min_rho,
            float(
                np.min(
                    rho
                )
            ),
        )

        shell_factor = (
            radius * radius
        )

        E2_shell[index] = (
            shell_factor
            * float(
                np.sum(
                    w_ang * e2
                )
            )
        )

        E4_shell[index] = (
            shell_factor
            * float(
                np.sum(
                    w_ang * e4
                )
            )
        )

        E0_shell[index] = (
            shell_factor
            * float(
                np.sum(
                    w_ang
                )
            )
            * V
        )

        A_shell[index] = (
            shell_factor
            * float(
                np.sum(
                    w_ang * active
                )
            )
        )

    E2_3d = float(
        np.trapezoid(
            E2_shell,
            r,
        )
    )

    E4_3d = float(
        np.trapezoid(
            E4_shell,
            r,
        )
    )

    E0_3d = float(
        np.trapezoid(
            E0_shell,
            r,
        )
    )

    A3d = float(
        np.trapezoid(
            A_shell,
            r,
        )
    )

    radial_factor = (
        4.0
        * math.pi
    )

    E2_expected = (
        radial_factor
        * profile.E2
    )
    E4_expected = (
        radial_factor
        * profile.E4
    )
    E0_expected = (
        radial_factor
        * profile.E0
    )
    A_expected = (
        radial_factor
        * profile.active_mass[-1]
    )

    max_energy_relerr = max(
        relative_error(
            E2_3d,
            E2_expected,
        ),
        relative_error(
            E4_3d,
            E4_expected,
        ),
        relative_error(
            E0_3d,
            E0_expected,
        ),
    )

    active_relerr = relative_error(
        A3d,
        A_expected,
    )

    return {
        "E2_3d": E2_3d,
        "E4_3d": E4_3d,
        "E0_3d": E0_3d,
        "A3d": A3d,
        "E2_expected": E2_expected,
        "E4_expected": E4_expected,
        "E0_expected": E0_expected,
        "A_expected": A_expected,
        "max_energy_relerr": max_energy_relerr,
        "active_relerr": active_relerr,
        "min_dec_margin": min_dec_margin,
        "min_rho": min_rho,
        "trace_relerr": max_trace_relerr,
    }


def build_gr_source(profile, b: float):
    """Build deterministic anisotropic 3D active-source quadrature."""

    # The field is negligible after the shell plus several true-vacuum
    # correlation lengths.  Restricting the gravity integral here avoids
    # spending nodes in a numerically empty tail.
    curvature_true = (
        profile.m**2
        * (
            1.0
            +
            profile.eta
        )
    )

    tail_length = (
        1.0
        /
        math.sqrt(
            curvature_true
        )
    )

    rmax = min(
        float(
            profile.r[-1]
        ),
        profile.shell_radius
        +
        8.0 * tail_length,
    )

    nodes_r, weights_r = leggauss(
        GR_RADIAL_N
    )

    r = (
        0.5
        * rmax
        * (
            nodes_r + 1.0
        )
    )

    wr = (
        0.5
        * rmax
        * weights_r
    )

    mu, wmu = leggauss(
        GR_MU_N
    )

    phi = (
        (
            np.arange(
                GR_PHI_N
            )
            + 0.5
        )
        * 2.0
        * math.pi
        / GR_PHI_N
    )

    dphi = (
        2.0
        * math.pi
        / GR_PHI_N
    )

    J = b7_angular_j(
        mu,
        phi,
        b,
    )

    interp_F = PchipInterpolator(
        profile.r,
        profile.F,
        extrapolate=False,
    )

    interp_Fp = PchipInterpolator(
        profile.r,
        profile.Fp,
        extrapolate=False,
    )

    F = interp_F(
        r
    )

    Fp = interp_Fp(
        r
    )

    source_x = []
    source_y = []
    source_z = []
    source_weight = []

    sin_theta = np.sqrt(
        1.0 - mu * mu
    )

    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)

    Xhat = (
        sin_theta[:, None]
        * cos_phi[None, :]
    )
    Yhat = (
        sin_theta[:, None]
        * sin_phi[None, :]
    )
    Zhat = (
        mu[:, None]
        * np.ones(
            (
                1,
                GR_PHI_N,
            )
        )
    )

    angular_weight = (
        wmu[:, None]
        * np.ones(
            (
                1,
                GR_PHI_N,
            )
        )
        * dphi
    )

    for ir, radius in enumerate(r):
        s2 = math.sin(
            float(
                F[ir]
            )
        ) ** 2

        a = float(
            Fp[ir] ** 2
        )

        b_ang = (
            s2
            * J**2
            /
            (
                radius * radius
            )
        )

        e4 = (
            2.0
            * a
            * b_ang
            +
            b_ang**2
        )

        V = (
            profile.m**2
            * (
                1.0
                -
                math.cos(
                    float(
                        F[ir]
                    )
                )
            )
            * (
                1.0
                +
                profile.eta
                * math.cos(
                    float(
                        F[ir]
                    )
                )
            )
        )

        active = (
            2.0
            * (
                e4 - V
            )
        )

        weight = (
            wr[ir]
            * radius**2
            * angular_weight
            * active
        )

        source_x.append(
            (
                radius
                * Xhat
            ).ravel()
        )

        source_y.append(
            (
                radius
                * Yhat
            ).ravel()
        )

        source_z.append(
            (
                radius
                * Zhat
            ).ravel()
        )

        source_weight.append(
            weight.ravel()
        )

    xyz = np.column_stack(
        [
            np.concatenate(
                source_x
            ),
            np.concatenate(
                source_y
            ),
            np.concatenate(
                source_z
            ),
        ]
    )

    weight = np.concatenate(
        source_weight
    )

    return xyz, weight


def deterministic_payload_points(
    center: np.ndarray,
    radius: float,
):
    """Return equal-volume tensor quadrature points and normalized weights."""

    ur, wr = leggauss(
        PAYLOAD_RADIAL_N
    )

    # Integrate s^2 ds by using s=R*((u+1)/2)^(1/3), for which equal spacing
    # in volume coordinate is convenient.  Gauss-Legendre is applied to
    # volume fraction q in [0,1].
    q = (
        0.5
        * (
            ur + 1.0
        )
    )

    wq = (
        0.5
        * wr
    )

    s = (
        radius
        * q**(
            1.0 / 3.0
        )
    )

    mu, wmu = leggauss(
        PAYLOAD_MU_N
    )

    phi = (
        (
            np.arange(
                PAYLOAD_PHI_N
            )
            + 0.5
        )
        * 2.0
        * math.pi
        / PAYLOAD_PHI_N
    )

    dphi = (
        2.0
        * math.pi
        / PAYLOAD_PHI_N
    )

    points = []
    weights = []

    for is_, radius_s in enumerate(s):
        sin_theta = np.sqrt(
            1.0
            -
            mu * mu
        )

        for im, mu_value in enumerate(mu):
            for phi_value in phi:
                direction = np.array(
                    [
                        sin_theta[im]
                        * math.cos(
                            phi_value
                        ),
                        sin_theta[im]
                        * math.sin(
                            phi_value
                        ),
                        mu_value,
                    ],
                    dtype=float,
                )

                points.append(
                    center
                    +
                    radius_s
                    * direction
                )

                # Normalized volume-average weight.
                weights.append(
                    wq[is_]
                    * 0.5
                    * wmu[im]
                    * dphi
                    / (
                        2.0
                        * math.pi
                    )
                )

    weights = np.asarray(
        weights,
        dtype=float,
    )

    weights /= np.sum(
        weights
    )

    return (
        np.asarray(
            points,
            dtype=float,
        ),
        weights,
    )


def acceleration_from_source(
    source_xyz: np.ndarray,
    source_weight: np.ndarray,
    points: np.ndarray,
):
    """Direct anisotropic 3D gravity integral, common positive factor omitted."""

    result = np.zeros(
        (
            len(points),
            3,
        ),
        dtype=float,
    )

    chunk = 24

    for start in range(
        0,
        len(points),
        chunk,
    ):
        stop = min(
            start + chunk,
            len(points),
        )

        p = points[
            start:stop,
            None,
            :
        ]

        diff = (
            p
            -
            source_xyz[
                None,
                :,
                :
            ]
        )

        r2 = np.sum(
            diff * diff,
            axis=-1,
        )

        # Smooth source singularity is integrable.  No payload point is
        # intentionally placed on a source quadrature node; this tiny floor
        # protects only floating-point coincidence.
        invr3 = (
            np.maximum(
                r2,
                1.0e-18,
            )
            ** (
                -1.5
            )
        )

        result[
            start:stop
        ] = (
            -np.sum(
                source_weight[
                    None,
                    :,
                    None,
                ]
                * diff
                * invr3[
                    :,
                    :,
                    None,
                ],
                axis=1,
            )
        )

    return result


def full_3d_payload_audit(
    profile,
    payload_candidate,
    b: float,
):
    """Test actual anisotropic 3D finite-payload gravity in many orientations."""

    source_xyz, source_weight = build_gr_source(
        profile,
        b,
    )

    results = []

    center_radius = float(
        payload_candidate.payload_center
    )

    payload_radius = float(
        payload_candidate.payload_radius
    )

    for raw in ORIENTATION_VECTORS:
        direction = np.asarray(
            raw,
            dtype=float,
        )

        direction /= np.linalg.norm(
            direction
        )

        center = (
            center_radius
            * direction
        )

        points, weights = deterministic_payload_points(
            center,
            payload_radius,
        )

        accel = acceleration_from_source(
            source_xyz,
            source_weight,
            points,
        )

        avg = np.sum(
            weights[:, None]
            * accel,
            axis=0,
        )

        outward = float(
            np.dot(
                avg,
                direction,
            )
        )

        transverse = float(
            np.linalg.norm(
                avg
                -
                outward * direction
            )
        )

        results.append(
            {
                "raw": raw,
                "outward": outward,
                "transverse": transverse,
                "magnitude": float(
                    np.linalg.norm(
                        avg
                    )
                ),
            }
        )

    outward_values = np.array(
        [
            result["outward"]
            for result in results
        ],
        dtype=float,
    )

    min_outward = float(
        np.min(
            outward_values
        )
    )

    max_outward = float(
        np.max(
            outward_values
        )
    )

    mean_outward = float(
        np.mean(
            outward_values
        )
    )

    anisotropy = (
        (
            max_outward
            -
            min_outward
        )
        /
        max(
            abs(
                mean_outward
            ),
            1.0e-300,
        )
    )

    return (
        results,
        min_outward,
        max_outward,
        mean_outward,
        anisotropy,
    )


def robustness_exact_fission(a23, selected: ExactCandidate):
    """Promotion-grade fission robustness with exact literature I values."""

    B = selected.profile.B
    eta0 = selected.profile.eta
    m0 = selected.profile.m

    records = []

    eta_values = (
        max(
            1.0 / 3.0
            + 0.015,
            eta0 - 0.04,
        ),
        eta0,
        min(
            0.95,
            eta0 + 0.04,
        ),
    )

    m_values = (
        0.8 * m0,
        m0,
        1.2 * m0,
    )

    for eta in eta_values:
        for m in m_values:
            profiles, energies = solve_exact_sector(
                a23,
                eta,
                m,
            )

            candidate = candidate_from_sector(
                a23,
                profiles,
                energies,
                B,
            )

            records.append(
                (
                    "PARAM",
                    eta,
                    m,
                    1.0,
                    2.0e-5,
                    1.0,
                    candidate.fission_margin,
                    candidate.profile.min_active_fraction,
                    candidate.payload.finite_payload_pass,
                )
            )

    for scale in (
        1.0 - I_UNCERTAINTY,
        1.0 + I_UNCERTAINTY,
    ):
        profiles, energies = solve_exact_sector(
            a23,
            eta0,
            m0,
            i_scale=scale,
        )

        candidate = candidate_from_sector(
            a23,
            profiles,
            energies,
            B,
        )

        records.append(
            (
                "I_SCALE",
                eta0,
                m0,
                scale,
                2.0e-5,
                1.0,
                candidate.fission_margin,
                candidate.profile.min_active_fraction,
                candidate.payload.finite_payload_pass,
            )
        )

    for tol in ROBUST_TOLS:
        profiles, energies = solve_exact_sector(
            a23,
            eta0,
            m0,
            tol=tol,
        )

        candidate = candidate_from_sector(
            a23,
            profiles,
            energies,
            B,
        )

        records.append(
            (
                "TOL",
                eta0,
                m0,
                1.0,
                tol,
                1.0,
                candidate.fission_margin,
                candidate.profile.min_active_fraction,
                candidate.payload.finite_payload_pass,
            )
        )

    for domain in ROBUST_DOMAIN_FACTORS:
        profiles, energies = solve_exact_sector(
            a23,
            eta0,
            m0,
            domain_factor=domain,
        )

        candidate = candidate_from_sector(
            a23,
            profiles,
            energies,
            B,
        )

        records.append(
            (
                "DOMAIN",
                eta0,
                m0,
                1.0,
                2.0e-5,
                domain,
                candidate.fission_margin,
                candidate.profile.min_active_fraction,
                candidate.payload.finite_payload_pass,
            )
        )

    pass_count = sum(
        1
        for record in records
        if (
            record[6] >= MIN_FISSION_MARGIN
            and record[7]
            <= -MIN_NEGATIVE_ACTIVE_FRACTION
            and record[8]
        )
    )

    worst_margin = min(
        record[6]
        for record in records
    )

    worst_active = max(
        record[7]
        for record in records
    )

    return (
        records,
        pass_count,
        len(records),
        worst_margin,
        worst_active,
    )


def main() -> None:
    """Execute the complete 023B promotion gate."""

    print(
        "=== 023B — EXACT RATIONAL-MAP + FULL-3D "
        "T_MUNU/GRAVITY PROMOTION GATE ==="
    )

    require_marker(
        A23_LOG,
        "023A_TOPOLOGICAL_FALSE_CORE_MULTISKYRMION_GR_REPULSION_GATE=GREEN",
    )

    require_marker(
        A23_LOG,
        "TOPOLOGICALLY_STABILIZED_REPULSIVE_MONOPOLE_CAPACITY_PREFLIGHT=SUPPORTED",
    )

    a23_sha = sha256(
        A23_SOURCE
    )

    print("\n=== UPSTREAM SOURCE AUDIT ===")
    print(
        f"023A_SOURCE_SHA256={a23_sha}"
    )
    print(
        f"023A_EXPECTED_SHA256={EXPECTED_023A_SHA256}"
    )
    print(
        "023A_SOURCE_HASH_MATCH="
        + (
            "PASS"
            if a23_sha
            == EXPECTED_023A_SHA256
            else "FAIL"
        )
    )

    if a23_sha != EXPECTED_023A_SHA256:
        raise RuntimeError(
            "023A source hash mismatch"
        )

    a23 = load_module(
        "ag023b_023a",
        A23_SOURCE,
    )

    # --------------------------------------------------------------
    # A. Literature I table and exact basin.
    # --------------------------------------------------------------
    print("\n=== A — EXACT LITERATURE RATIONAL-MAP I TABLE ===")

    for B in B_VALUES:
        print(
            f"LITERATURE_I_B{B}="
            f"{LITERATURE_I[B]:.15e}"
        )

    print(
        "EXACT_LITERATURE_I_TABLE=PASS"
    )

    print("\n=== B — EXACT-I B<=8 RADIAL + FISSION RECONSTRUCTION ===")

    all_candidates, passers = scan_exact_basin(
        a23
    )

    print(
        f"EXACT_I_TOTAL_CANDIDATES={len(all_candidates)}"
    )
    print(
        f"EXACT_I_PROMOTION_PASSERS={len(passers)}"
    )

    if not passers:
        raise RuntimeError(
            "No exact-I promotion candidate survived"
        )

    selected = min(
        passers,
        key=selected_rank,
    )

    p = selected.profile
    payload = selected.payload

    print(
        f"SELECTED_B={p.B}"
    )
    print(
        f"SELECTED_ETA={p.eta:.15e}"
    )
    print(
        f"SELECTED_M={p.m:.15e}"
    )
    print(
        f"SELECTED_EXACT_I={p.I:.15e}"
    )
    print(
        f"SELECTED_MIN_ENCLOSED_ACTIVE_FRACTION={p.min_active_fraction:.15e}"
    )
    print(
        f"SELECTED_EXACT_BINARY_FISSION_MARGIN={selected.fission_margin:.15e}"
    )
    print(
        f"SELECTED_VIRIAL_RELERR={p.virial_relerr:.15e}"
    )
    print(
        f"SELECTED_TOTAL_ACTIVE_TO_ENERGY_RELERR={p.active_total_relerr:.15e}"
    )
    print(
        f"SELECTED_TOPOLOGICAL_CHARGE={p.topological_charge:.15e}"
    )
    print(
        f"SELECTED_TOPOLOGICAL_CHARGE_RELERR={p.topology_relerr:.15e}"
    )
    print(
        f"SELECTED_PAYLOAD_CENTER={payload.payload_center:.15e}"
    )
    print(
        f"SELECTED_PAYLOAD_RADIUS={payload.payload_radius:.15e}"
    )
    print(
        f"SELECTED_MONOPOLE_PAYLOAD_C={payload.payload_coefficient_c:.15e}"
    )

    exact_fission_pass = (
        selected.fission_margin
        >= MIN_FISSION_MARGIN
    )

    # --------------------------------------------------------------
    # C. Exact published B=7 angular map.
    # --------------------------------------------------------------
    print("\n=== C — EXACT B7 ICOSAHEDRAL RATIONAL MAP AUDIT ===")

    if p.B != 7:
        print(
            "SELECTED_B7_REQUIRED_FOR_THIS_3D_GATE=FAIL"
        )
        raise RuntimeError(
            "Exact-I rerank did not select B=7; 3D map implementation must be updated"
        )

    degree_b7, I_b7 = angular_integrals_b7(
        B7_B0
    )

    degree_relerr = relative_error(
        degree_b7,
        7.0,
    )

    I_relerr = relative_error(
        I_b7,
        LITERATURE_I[7],
    )

    print(
        f"B7_MAP_B_PARAMETER={B7_B0:.15e}"
    )
    print(
        f"B7_MAP_DEGREE_INTEGRAL={degree_b7:.15e}"
    )
    print(
        f"B7_MAP_DEGREE_RELERR={degree_relerr:.15e}"
    )
    print(
        f"B7_MAP_I_DIRECT={I_b7:.15e}"
    )
    print(
        f"B7_MAP_I_LITERATURE={LITERATURE_I[7]:.15e}"
    )
    print(
        f"B7_MAP_I_RELERR={I_relerr:.15e}"
    )

    degree_pass = (
        degree_relerr <= 1.0e-10
    )

    map_i_pass = (
        I_relerr <= MAX_I_RECON_RELERR
    )

    print(
        "EXACT_B7_MAP_DEGREE="
        + (
            "PASS"
            if degree_pass
            else "FAIL"
        )
    )
    print(
        "EXACT_B7_MAP_I="
        + (
            "PASS"
            if map_i_pass
            else "FAIL"
        )
    )

    # Re-solve using the directly reconstructed I instead of the rounded table.
    p_direct = solve_profile_with_custom_I(
        a23,
        7,
        p.eta,
        p.m,
        I_b7,
    )

    direct_profile_relerr = relative_error(
        p_direct.E,
        p.E,
    )

    print(
        f"DIRECT_I_PROFILE_ENERGY_RELERR={direct_profile_relerr:.15e}"
    )

    # --------------------------------------------------------------
    # D. Direct anisotropic 3D stress reconstruction.
    # --------------------------------------------------------------
    print("\n=== D — FULL 3D T_MUNU / DEC RECONSTRUCTION ===")

    recon = direct_3d_reconstruction(
        p_direct,
        B7_B0,
    )

    for key in (
        "E2_3d",
        "E4_3d",
        "E0_3d",
        "A3d",
        "E2_expected",
        "E4_expected",
        "E0_expected",
        "A_expected",
        "max_energy_relerr",
        "active_relerr",
        "min_dec_margin",
        "min_rho",
        "trace_relerr",
    ):
        print(
            f"FULL3D_{key.upper()}="
            f"{recon[key]:.15e}"
        )

    energy_3d_pass = (
        recon["max_energy_relerr"]
        <= MAX_3D_ENERGY_RELERR
    )

    active_3d_pass = (
        recon["active_relerr"]
        <= MAX_3D_ACTIVE_RELERR
        and recon["trace_relerr"]
        <= 1.0e-10
    )

    dec_pass = (
        recon["min_rho"]
        >= MIN_DEC_MARGIN
        and recon["min_dec_margin"]
        >= MIN_DEC_MARGIN
    )

    print(
        "FULL_3D_ENERGY_RECONSTRUCTION="
        + (
            "PASS"
            if energy_3d_pass
            else "FAIL"
        )
    )
    print(
        "FULL_3D_ACTIVE_TRACE_RECONSTRUCTION="
        + (
            "PASS"
            if active_3d_pass
            else "FAIL"
        )
    )
    print(
        "POINTWISE_3D_DEC="
        + (
            "PASS"
            if dec_pass
            else "FAIL"
        )
    )

    # --------------------------------------------------------------
    # E. Actual anisotropic finite-payload gravity.
    # --------------------------------------------------------------
    print("\n=== E — ACTUAL ANISOTROPIC FULL-3D FINITE-PAYLOAD GRAVITY ===")

    (
        orientation_results,
        min_outward,
        max_outward,
        mean_outward,
        anisotropy,
    ) = full_3d_payload_audit(
        p_direct,
        payload,
        B7_B0,
    )

    for index, result in enumerate(
        orientation_results,
        start=1,
    ):
        print(
            f"ORIENTATION_{index}_VECTOR="
            f"{result['raw']}"
        )
        print(
            f"ORIENTATION_{index}_OUTWARD_KERNEL="
            f"{result['outward']:.15e}"
        )
        print(
            f"ORIENTATION_{index}_TRANSVERSE_KERNEL="
            f"{result['transverse']:.15e}"
        )

    print(
        f"FULL3D_PAYLOAD_MIN_OUTWARD_KERNEL={min_outward:.15e}"
    )
    print(
        f"FULL3D_PAYLOAD_MAX_OUTWARD_KERNEL={max_outward:.15e}"
    )
    print(
        f"FULL3D_PAYLOAD_MEAN_OUTWARD_KERNEL={mean_outward:.15e}"
    )
    print(
        f"FULL3D_PAYLOAD_ORIENTATION_ANISOTROPY={anisotropy:.15e}"
    )

    gravity_3d_pass = (
        min_outward > 0.0
    )

    print(
        "FULL_3D_FINITE_PAYLOAD_OUTWARD_ALL_ORIENTATIONS="
        + (
            "PASS"
            if gravity_3d_pass
            else "FAIL"
        )
    )

    # --------------------------------------------------------------
    # F. Exact fission robustness.
    # --------------------------------------------------------------
    print("\n=== F — EXACT-I PROMOTION-GRADE FISSION ROBUSTNESS ===")

    (
        robustness_records,
        robustness_passes,
        robustness_total,
        worst_fission,
        worst_active,
    ) = robustness_exact_fission(
        a23,
        selected,
    )

    for index, record in enumerate(
        robustness_records,
        start=1,
    ):
        print(
            f"ROBUST_{index}_TYPE={record[0]} "
            f"ETA={record[1]:.9e} "
            f"M={record[2]:.9e} "
            f"I_SCALE={record[3]:.9e} "
            f"TOL={record[4]:.9e} "
            f"DOMAIN={record[5]:.9e} "
            f"FISSION={record[6]:.9e} "
            f"MIN_ACTIVE={record[7]:.9e} "
            f"PAYLOAD={'YES' if record[8] else 'NO'}"
        )

    robustness_fraction = (
        robustness_passes
        / max(
            robustness_total,
            1,
        )
    )

    print(
        f"ROBUST_FISSION_PASS_COUNT={robustness_passes}"
    )
    print(
        f"ROBUST_FISSION_TOTAL_COUNT={robustness_total}"
    )
    print(
        f"ROBUST_FISSION_PASS_FRACTION={robustness_fraction:.15e}"
    )
    print(
        f"ROBUST_WORST_BINARY_FISSION_MARGIN={worst_fission:.15e}"
    )
    print(
        f"ROBUST_WORST_MIN_ACTIVE_FRACTION={worst_active:.15e}"
    )

    robust_fission_pass = (
        robustness_total >= 12
        and robustness_fraction >= 0.90
        and worst_fission
        >= MIN_FISSION_MARGIN
        and worst_active
        <= -MIN_NEGATIVE_ACTIVE_FRACTION
    )

    print(
        "ROBUST_BINARY_FISSION_MARGIN="
        + (
            "PASS"
            if robust_fission_pass
            else "FAIL"
        )
    )

    # --------------------------------------------------------------
    # G. Rational-map deformation curvature.
    # --------------------------------------------------------------
    print("\n=== G — B7 RATIONAL-MAP SHAPE CURVATURE ===")

    (
        map_curvature_pass,
        map_records,
        min_map_curvature,
    ) = map_shape_curvature(
        a23,
        selected,
    )

    for record in map_records:
        (
            eps,
            I_minus,
            I_center,
            I_plus,
            E_minus,
            E_center,
            E_plus,
            curvature,
        ) = record

        print(
            f"MAP_EPS={eps:.9e} "
            f"I_MINUS={I_minus:.9e} "
            f"I_CENTER={I_center:.9e} "
            f"I_PLUS={I_plus:.9e} "
            f"E_MINUS={E_minus:.9e} "
            f"E_CENTER={E_center:.9e} "
            f"E_PLUS={E_plus:.9e} "
            f"CURVATURE={curvature:.9e}"
        )

    print(
        f"MIN_RATIONAL_MAP_SHAPE_CURVATURE={min_map_curvature:.15e}"
    )
    print(
        "RATIONAL_MAP_SHAPE_CURVATURE="
        + (
            "PASS"
            if map_curvature_pass
            else "FAIL"
        )
    )

    # --------------------------------------------------------------
    # H. Blind wildcards.
    # --------------------------------------------------------------
    print("\n=== BLIND WILDCARD DIAGNOSTICS — NOT EVIDENCE ===")

    for factor in BLIND_WILDCARDS:
        test_m = min(
            max(
                p.m * factor,
                0.5,
            ),
            20.0,
        )

        profiles_w, energies_w = solve_exact_sector(
            a23,
            p.eta,
            test_m,
        )

        candidate_w = candidate_from_sector(
            a23,
            profiles_w,
            energies_w,
            p.B,
        )

        print(
            f"WILDCARD_FACTOR={factor:.6f} "
            f"M={test_m:.9e} "
            f"FISSION={candidate_w.fission_margin:.9e} "
            f"MIN_ACTIVE={candidate_w.profile.min_active_fraction:.9e} "
            f"PAYLOAD={'YES' if candidate_w.payload.finite_payload_pass else 'NO'}"
        )

    print(
        "BLIND_WILDCARD_VALUES_USED_AS_EVIDENCE=NO"
    )

    # --------------------------------------------------------------
    # I. Decision.
    # --------------------------------------------------------------
    print("\n=== 023B DECISION ===")

    topology_pass = (
        p_direct.topology_relerr
        <= MAX_TOPOLOGY_RELERR
    )

    virial_pass = (
        p_direct.virial_relerr
        <= MAX_VIRIAL_RELERR
    )

    negative_active_pass = (
        p_direct.min_active_fraction
        <= -MIN_NEGATIVE_ACTIVE_FRACTION
    )

    positive_total_pass = (
        p_direct.active_mass[-1] > 0.0
        and p_direct.active_total_relerr
        <= MAX_ACTIVE_TOTAL_RELERR
    )

    independent_pass = (
        degree_pass
        and map_i_pass
        and direct_profile_relerr
        <= 1.0e-3
        and energy_3d_pass
        and active_3d_pass
    )

    full_green = (
        exact_fission_pass
        and degree_pass
        and map_i_pass
        and topology_pass
        and virial_pass
        and negative_active_pass
        and positive_total_pass
        and dec_pass
        and energy_3d_pass
        and active_3d_pass
        and gravity_3d_pass
        and robust_fission_pass
        and map_curvature_pass
        and independent_pass
    )

    print(
        "RATIONAL_MAP_BVP="
        + (
            "PASS"
            if p_direct.success
            else "FAIL"
        )
    )
    print(
        "TOPOLOGICAL_CHARGE="
        + (
            "PASS"
            if topology_pass
            else "FAIL"
        )
    )
    print(
        "DERRICK_VIRIAL="
        + (
            "PASS"
            if virial_pass
            else "FAIL"
        )
    )
    print(
        "EXACT_BINARY_FISSION_MARGIN="
        + (
            "PASS"
            if exact_fission_pass
            else "FAIL"
        )
    )
    print(
        "NEGATIVE_ENCLOSED_ACTIVE_MASS="
        + (
            "PASS"
            if negative_active_pass
            else "FAIL"
        )
    )
    print(
        "POSITIVE_TOTAL_ACTIVE_MASS="
        + (
            "PASS"
            if positive_total_pass
            else "FAIL"
        )
    )
    print(
        "INDEPENDENT_RECONSTRUCTION="
        + (
            "PASS"
            if independent_pass
            else "FAIL"
        )
    )

    if full_green:
        print(
            "023B_EXACT_RATIONAL_MAP_FULL3D_T_MUNU_GRAVITY_PROMOTION_GATE="
            "GREEN"
        )
        print(
            "FULL_3D_RATIONAL_MAP_STABLE_FIELD_THEORY_PREFLIGHT="
            "SUPPORTED"
        )
        print(
            "EXACT_MAP_SELECTED_TOPOLOGICAL_SECTOR="
            f"B{p.B}"
        )
        print(
            "ANISOTROPIC_3D_FINITE_PAYLOAD_REPULSION="
            "SUPPORTED_IN_LINEARIZED_GR"
        )
        print(
            "INTRINSIC_STABILITY_STACK="
            "TOPOLOGY_PLUS_DERRICK_PLUS_EXACT_BINARY_FISSION_PLUS_MAP_SHAPE_CURVATURE"
        )
        print(
            "HEURISTIC_PROMOTION_ELIGIBILITY="
            "APPROXIMATELY_70_TO_72_PERCENT_AFTER_CLAIM_AUDIT"
        )
        print(
            "CURRENT_KNOWLEDGE_HEURISTIC="
            "APPROXIMATELY_68_PERCENT_UNTIL_POST_RUN_CLAIM_AUDIT"
        )
        print(
            "NEXT="
            "023C_UNRESTRICTED_CARTESIAN_3D_RELAXATION_HESSIAN_AND_NONLINEAR_GR_SCALING_GATE"
        )
    else:
        print(
            "023B_EXACT_RATIONAL_MAP_FULL3D_T_MUNU_GRAVITY_PROMOTION_GATE="
            "GREEN_NEGATIVE_OR_INCOMPLETE_RESULT"
        )
        print(
            "FULL_3D_RATIONAL_MAP_STABLE_FIELD_THEORY_PREFLIGHT="
            "NOT_ESTABLISHED"
        )
        print(
            "HEURISTIC_PROMOTION_ELIGIBILITY="
            "NO"
        )
        print(
            "CURRENT_KNOWLEDGE_HEURISTIC="
            "APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY"
        )
        print(
            "NEXT="
            "INSPECT_FAILED_023B_GATE_BEFORE_ESCALATION"
        )

    print(
        "UNRESTRICTED_CARTESIAN_3D_EULER_LAGRANGE="
        "NOT_YET"
    )
    print(
        "COMPLETE_UNRESTRICTED_3D_HESSIAN="
        "NOT_YET"
    )
    print(
        "NONLINEAR_EINSTEIN_MATTER="
        "NOT_ESTABLISHED"
    )
    print(
        "PRACTICAL_ENERGY_SCALING="
        "STILL_CATASTROPHIC_IN_PURE_GR"
    )
    print(
        "REAL_MATERIAL="
        "NO"
    )
    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )
    print(
        "NEW_PHYSICS_DISCOVERY="
        "NO"
    )

    print(
        "006D_CONSTRUCTIVE_LINEARIZED_GR_RESULT="
        "RETAINED"
    )
    print(
        "018B_FIELD_EXISTENCE_RESULT="
        "RETAINED"
    )
    print(
        "018C_KLS_M2_STABILITY_FAILURE="
        "RETAINED"
    )
    print(
        "023A_TOPOLOGICAL_MONOPOLE_CAPACITY_RESULT="
        "RETAINED"
    )
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_023B_EXACT_RATIONAL_MAP_FULL3D_T_MUNU_GRAVITY_PROMOTION_GATE"
    )


if __name__ == "__main__":
    main()
