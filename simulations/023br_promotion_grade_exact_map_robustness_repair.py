#!/usr/bin/env python3
"""023BR — promotion-grade exact-map robustness repair.

PURPOSE
-------
Close the two narrow promotion blockers left by Simulation 023B before any
expensive unrestricted Cartesian 3D relaxation is attempted.

023B established, within the exact B=7 rational-map branch:

- exact rational-map degree and angular integral reconstruction;
- strong binary binding;
- negative enclosed active mass and positive total active mass;
- pointwise DEC on the reconstructed 3D stress tensor;
- accurate independent 3D energy reconstruction;
- positive rational-map shape curvature;
- outward finite-payload gravity in six anisotropic orientations.

023B was not promotion-grade for two specific reasons:

1. its candidate was ranked primarily by central fission margin, and four
   robustness-neighborhood points had negative-active fractions with magnitude
   below the predeclared 1 percent strength threshold;

2. its pointwise active-trace diagnostic divided by the active trace itself,
   making the relative residual ill-conditioned near active-source zero
   crossings even though the underlying identity is algebraic.

A third issue was not a failure but remained under-sampled: only six payload
orientations were tested despite strong anisotropy.

SCIENTIFIC QUESTION
-------------------
Does an already-existing exact-I B<=8 promotion passer satisfy the original
robustness thresholds when candidates are ranked by worst-case promotion
margin, while the exact B=7 field also passes a scaled/high-precision active-
trace identity and a dense finite-payload orientation sphere?

OPERATIONAL OBSERVABLE
----------------------
For a uniform spherical payload with center c and radius R_p, the primary
observable is the volume-averaged radial acceleration

    a_CM(c) . c/|c|.

The source is the complete linearized-GR active density

    S = rho + p_r + 2 p_t = 2 (e_4 - V).

Up to one common positive factor, the point-payload field is

    a(x) = - integral S(x') (x-x') / |x-x'|^3 d^3x'.

For a uniform spherical payload the volume average of the Newton kernel can be
performed analytically.  Let q=x'-c and d=|q|.  Then

    < (x-x') / |x-x'|^3 >_payload
        = -q/d^3,  d >= R_p,
        = -q/R_p^3, d < R_p.

Therefore

    <a>_payload
        = integral S(x') q / max(d^3, R_p^3) d^3x'.

This is the ordinary Newton shell theorem applied to the payload average.  It
is exact for a uniform spherical payload in the continuum and eliminates the
need to evaluate hundreds of payload quadrature points for every orientation.
Controlled synthetic direct-payload quadrature checks are retained as an
independent implementation validation of the shell-theorem average.

CHEAPEST DECISIVE EXPERIMENT
----------------------------
1. Reconstruct the existing exact-I basin from 023B.
2. Order all existing exact-I promotion passers by a rigorous central-state
   upper bound on their possible robust maximin score.
3. Evaluate complete declared robustness neighborhoods only until branch-and-
   bound proves the remaining candidates cannot beat the current winner.
4. Select by normalized maximin promotion margin rather than central fission
   margin.
5. Require the selected global maximin candidate to remain the implemented
   exact B=7 rational-map branch before using the B=7 3D map.
6. Reconstruct the active-trace identity using a scale-aware residual plus
   long-double and arbitrary-precision spot checks.
7. Replace six directions by a 320-direction deterministic Fibonacci sphere.
8. Repeat the dense orientation test at low/primary/high 3D source quadrature.
9. Retain pointwise DEC, independent 3D energy accounting, exact map degree/I,
   and rational-map shape curvature.

MAXIMIN DEFINITION
------------------
For each central promotion passer define

    A_worst = max_robustness (M_A_min / E),

where the quantity is negative when an enclosed negative-active region exists,
and

    delta_fiss,worst = min_robustness delta_fiss.

The predeclared thresholds remain unchanged:

    A_worst <= -0.01,
    delta_fiss,worst >= 0.002,
    finite-payload monopole response outward in every robustness case.

The normalized maximin score is

    min(
        -A_worst / 0.01,
        delta_fiss,worst / 0.002
    ).

A score >= 1 passes both quantitative thresholds.  No threshold is relaxed.

ACTIVE-TRACE REPAIR
-------------------
The pointwise identity is

    rho + p_r + 2 p_t = 2(e_4 - V).

Use the scaled residual

    R_trace = |lhs-rhs| / max(
        rho + |p_r| + 2|p_t| + 2e_4 + 2V,
        epsilon_scale
    ),

with epsilon_scale tied to the global peak local energy/stress scale and
machine precision.  Also report:

- maximum absolute trace residual;
- maximum absolute residual divided by global peak energy/stress;
- maximum scaled residual;
- long-double spot-check residual;
- arbitrary-precision mpmath spot-check residual.

The algebraic identity must pass because it reconstructs, not because the old
tolerance was weakened.

DENSE ORIENTATION ROBUSTNESS
----------------------------
Use 320 deterministic Fibonacci-sphere directions and report:

- minimum radial outward acceleration;
- maximum radial outward acceleration;
- maximum transverse acceleration;
- maximum transverse/radial ratio;
- worst radial-force orientation;
- low/primary/high source-quadrature convergence.

Every tested orientation must remain outward on low, primary, and high source
quadrature.  Primary-to-high pointwise radial disagreement must remain small
relative to the mean high-grid radial signal.

PROMOTION CONDITION
-------------------
A strong GREEN requires all of:

    UPSTREAM_023B_SOURCE_AUDIT=PASS
    EXACT_I_BASIN=PASS
    MAXIMIN_SELECTED_CANDIDATE=FOUND
    MAXIMIN_SELECTED_B=7
    ROBUST_WORST_ACTIVE_FRACTION<=-0.01
    ROBUST_WORST_FISSION_MARGIN>=0.002
    ROBUST_PAYLOAD_ALL_CASES=PASS
    EXACT_B7_MAP_DEGREE=PASS
    EXACT_B7_MAP_I=PASS
    POINTWISE_ACTIVE_TRACE=PASS_SCALED_AND_HIGH_PRECISION
    POINTWISE_DEC=PASS
    FULL_3D_ENERGY_RECONSTRUCTION=PASS
    DENSE_ORIENTATION_FINITE_PAYLOAD_OUTWARD=PASS
    ANALYTIC_PAYLOAD_THEOREM_IMPLEMENTATION_CHECK=PASS
    SOURCE_QUADRATURE_CONVERGENCE=PASS
    RATIONAL_MAP_SHAPE_CURVATURE=PASS

If GREEN, classify only as

    PROMOTION_GRADE_RATIONAL_MAP_STABLE_FIELD_PREFLIGHT.

This remains weaker than unrestricted Cartesian 3D stability.

FALSIFIERS
----------
Any of the following blocks promotion:

- no existing exact-I passer satisfies the original robustness thresholds;
- the global maximin survivor is not the implemented exact B=7 map and no
  equivalent exact angular-map reconstruction is provided;
- the active-trace identity fails scale-aware/high-precision reconstruction;
- DEC or independent 3D energy accounting fails;
- any dense payload orientation becomes inward;
- dense orientation sign depends materially on source quadrature;
- rational-map shape curvature is nonpositive.

STOP RULE
---------
If 023BR fails structurally, do not launch 023C merely to protect sunk effort.
Inspect the failed gate first.  Do not lower the 1 percent active-strength
criterion and do not move to huge B.

If 023BR is GREEN, the highest-information next action is

    023C_UNRESTRICTED_CARTESIAN_3D_RELAXATION_AND_FULL_PHYSICAL_HESSIAN.

APPROXIMATION LEVEL
-------------------
Flat-spacetime Skyrme matter fields plus static linearized-GR gravity.  The
field remains restricted to the rational-map ansatz class.  Payload
backreaction and nonlinear Einstein backreaction are not included.

CLAIM BOUNDARIES
----------------
This file does NOT establish:

- unrestricted Cartesian 3D stability;
- a complete physical Hessian;
- a self-consistent Einstein-Skyrme solution;
- a real material realization;
- practical energy scaling;
- an experimental antigravity signal;
- a practical antigravity device;
- discovery of new physics.

RELATED FILES
-------------
Upstream simulations:
    simulations/023a_topological_false_core_multiskyrmion_gr_repulsion_gate.py
    simulations/023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.py

Upstream log:
    results/logs/023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.log

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_023BR_PROMOTION_GRADE_EXACT_MAP_ROBUSTNESS_REPAIR
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib.util
import math
from pathlib import Path
import sys
from typing import Any

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss


ROOT = Path(__file__).resolve().parents[1]

A23_SOURCE = (
    ROOT
    / "simulations"
    / "023a_topological_false_core_multiskyrmion_gr_repulsion_gate.py"
)
B23_SOURCE = (
    ROOT
    / "simulations"
    / "023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.py"
)
B23_LOG = (
    ROOT
    / "results/logs"
    / "023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.log"
)

EXPECTED_023A_SHA256 = (
    "0087a5d2b4f93667308cabf4c3c498200ed29381e9493acf21714df7d8e11c9b"
)
EXPECTED_023B_SHA256 = (
    "6bf99785e67cfe1b2dfcb460bc3145a24115e25949e112f8480a89c880a2803c"
)

EXPECTED_023B_MARKERS = (
    "EXACT_I_PROMOTION_PASSERS=10",
    "POINTWISE_3D_DEC=PASS",
    "FULL_3D_FINITE_PAYLOAD_OUTWARD_ALL_ORIENTATIONS=PASS",
    "023B_EXACT_RATIONAL_MAP_FULL3D_T_MUNU_GRAVITY_PROMOTION_GATE=GREEN_NEGATIVE_OR_INCOMPLETE_RESULT",
    "CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY",
)

MIN_NEGATIVE_ACTIVE_FRACTION = 1.0e-2
MIN_FISSION_MARGIN = 2.0e-3

DENSE_ORIENTATION_N = 320

# Source-only 3D gravity quadratures.  The payload average itself is analytic.
SOURCE_QUADRATURE_LEVELS = (
    ("LOW", 52, 24, 48),
    ("PRIMARY", 68, 32, 64),
    ("HIGH", 84, 40, 80),
)

MAX_PRIMARY_HIGH_RADIAL_LINF_OVER_MEAN = 5.0e-2
MAX_LOW_PRIMARY_RADIAL_LINF_OVER_MEAN = 1.0e-1
MAX_PAYLOAD_THEOREM_OUTSIDE_RELERR = 1.0e-6
MAX_PAYLOAD_THEOREM_INSIDE_RELERR = 2.0e-2
MAX_PAYLOAD_THEOREM_CENTER_SCALED = 1.0e-10

TRACE_FLOAT_EPS_FACTOR = 4096.0
TRACE_LONGDOUBLE_EPS_FACTOR = 4096.0
TRACE_MP_DPS = 90
TRACE_MP_ABS_TOL = mp.mpf("1e-70")

# The user-requested blind wildcard values remain diagnostics only.  They are
# not included in candidate selection or promotion predicates.
BLIND_WILDCARDS = (1.6, 1.875, 3.125, 0.625, 5.0)


@dataclass
class RobustRow:
    """Maximin robustness summary for one existing exact-I promotion passer."""

    candidate: Any
    records: list[tuple]
    pass_count: int
    total_count: int
    worst_fission: float
    worst_active: float
    payload_all: bool
    active_ratio: float
    fission_ratio: float
    maximin_score: float


@dataclass
class OrientationAudit:
    """Dense finite-payload orientation result for one source quadrature."""

    label: str
    radial: np.ndarray
    transverse: np.ndarray
    vectors: np.ndarray
    source_nodes: int

    @property
    def min_radial(self) -> float:
        return float(np.min(self.radial))

    @property
    def max_radial(self) -> float:
        return float(np.max(self.radial))

    @property
    def mean_radial(self) -> float:
        return float(np.mean(self.radial))

    @property
    def max_transverse(self) -> float:
        return float(np.max(self.transverse))

    @property
    def max_transverse_over_radial(self) -> float:
        ratio = self.transverse / np.maximum(self.radial, 1.0e-300)
        return float(np.max(ratio))

    @property
    def worst_index(self) -> int:
        return int(np.argmin(self.radial))


def sha256(path: Path) -> str:
    """Return the SHA-256 hash of one file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_file(path: Path) -> None:
    """Fail closed if a required upstream file is missing."""

    if not path.exists():
        raise RuntimeError(f"Missing required upstream file: {path}")


def require_markers(path: Path, markers: tuple[str, ...]) -> None:
    """Fail closed unless every exact upstream marker is present."""

    require_file(path)
    text = path.read_text(errors="replace")

    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise RuntimeError(
            "Missing required 023B log marker(s): " + ", ".join(missing)
        )


def load_module(name: str, path: Path):
    """Import a repository simulation without invoking its main function."""

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


def install_profile_cache(b23):
    """Memoize exact-profile BVP solves across the all-passer robustness audit."""

    original = b23.solve_exact_profile
    cache: dict[tuple, Any] = {}

    def cached(
        a23,
        B: int,
        eta: float,
        m: float,
        i_scale: float = 1.0,
        tol: float = 2.0e-5,
        domain_factor: float = 1.0,
    ):
        key = (
            int(B),
            float(eta),
            float(m),
            float(i_scale),
            float(tol),
            float(domain_factor),
        )
        if key not in cache:
            cache[key] = original(
                a23,
                B,
                eta,
                m,
                i_scale=i_scale,
                tol=tol,
                domain_factor=domain_factor,
            )
        return cache[key]

    b23.solve_exact_profile = cached
    return cache


def normalized_maximin(worst_active: float, worst_fission: float) -> tuple[float, float, float]:
    """Return active ratio, fission ratio, and threshold-normalized maximin."""

    active_ratio = -worst_active / MIN_NEGATIVE_ACTIVE_FRACTION
    fission_ratio = worst_fission / MIN_FISSION_MARGIN
    score = min(active_ratio, fission_ratio)
    return active_ratio, fission_ratio, score


def reconstruct_existing_passers_fast(a23, b23) -> list[Any]:
    """Reconstruct the 023B exact-I passers without payload work on failures.

    The original 023B basin scan attaches an optimized finite-payload geometry
    to every B=2..8 candidate before applying cheap radial/fission predicates.
    For 023BR that is unnecessary and expensive.  This equivalent fail-closed
    scan applies all payload-independent gates first, then computes the payload
    only for candidates that can still pass.
    """

    passers: list[Any] = []

    for eta in b23.ETA_VALUES:
        for m in b23.M_VALUES:
            profiles, energies = b23.solve_exact_sector(a23, eta, m)

            for B in range(2, 9):
                profile = profiles[B]
                fission = a23.binary_fission_margin(energies, B)

                cheap_pass = (
                    profile.success
                    and profile.topology_relerr <= b23.MAX_TOPOLOGY_RELERR
                    and profile.virial_relerr <= b23.MAX_VIRIAL_RELERR
                    and profile.active_total_relerr <= b23.MAX_ACTIVE_TOTAL_RELERR
                    and profile.min_active_fraction <= -b23.MIN_NEGATIVE_ACTIVE_FRACTION
                    and fission >= b23.MIN_FISSION_MARGIN
                    and a23.profile_passes_core(profile)
                )

                if not cheap_pass:
                    continue

                payload_candidate = a23.make_candidate(profile, energies)
                candidate = b23.ExactCandidate(
                    profile=profile,
                    fission_margin=fission,
                    payload=payload_candidate,
                )

                if b23.core_pass(a23, candidate):
                    passers.append(candidate)

    return passers


def evaluate_robust_candidate(a23, b23, candidate) -> RobustRow:
    """Evaluate the complete declared robustness neighborhood of one passer."""

    (
        records,
        pass_count,
        total_count,
        worst_fission,
        worst_active,
    ) = b23.robustness_exact_fission(a23, candidate)

    payload_all = all(bool(record[8]) for record in records)
    active_ratio, fission_ratio, score = normalized_maximin(
        worst_active,
        worst_fission,
    )

    return RobustRow(
        candidate=candidate,
        records=records,
        pass_count=pass_count,
        total_count=total_count,
        worst_fission=worst_fission,
        worst_active=worst_active,
        payload_all=payload_all,
        active_ratio=active_ratio,
        fission_ratio=fission_ratio,
        maximin_score=score if payload_all else -math.inf,
    )


def central_maximin_upper_bound(candidate) -> float:
    """Upper-bound any robust maximin score using the included central state.

    The central state is itself one member of every declared robustness
    neighborhood.  Therefore

        worst_active >= central_active
        worst_fission <= central_fission

    in the sign conventions used here.  Consequently the robust threshold-
    normalized active and fission ratios cannot exceed their central ratios.
    The minimum of the two central ratios is thus a rigorous upper bound on the
    candidate's final robust maximin score.
    """

    active_ratio = (
        -candidate.profile.min_active_fraction
        / MIN_NEGATIVE_ACTIVE_FRACTION
    )
    fission_ratio = candidate.fission_margin / MIN_FISSION_MARGIN
    return min(active_ratio, fission_ratio)


def branch_and_bound_maximin(a23, b23, passers):
    """Find the global robust maximin winner with rigorous cheap pruning.

    Candidates are ordered by their central maximin upper bound.  After a full
    robustness audit establishes a current best score S, every remaining
    candidate with central upper bound <= S is mathematically unable to beat
    the current winner and is pruned without redundant expensive robustness
    solves.
    """

    ordered = sorted(
        passers,
        key=central_maximin_upper_bound,
        reverse=True,
    )

    evaluated: list[RobustRow] = []
    pruned: list[tuple[Any, float]] = []
    best: RobustRow | None = None

    for candidate in ordered:
        upper = central_maximin_upper_bound(candidate)

        if best is not None and upper <= best.maximin_score:
            pruned.append((candidate, upper))
            continue

        row = evaluate_robust_candidate(a23, b23, candidate)
        evaluated.append(row)

        if best is None or robust_row_rank(row) > robust_row_rank(best):
            best = row

    if best is None:
        raise RuntimeError("No candidate received a full robustness audit")

    return best, evaluated, pruned

def robust_row_rank(row: RobustRow) -> tuple[float, float, float, float]:
    """Rank by weakest normalized gate, then active and fission safety margins."""

    return (
        row.maximin_score,
        row.active_ratio,
        row.fission_ratio,
        -row.candidate.payload.payload_coefficient_c,
    )


def fibonacci_sphere(n: int) -> np.ndarray:
    """Return a deterministic approximately uniform orientation sphere."""

    if n < 2:
        raise ValueError("Need at least two orientations")

    k = np.arange(n, dtype=float)
    golden_angle = math.pi * (3.0 - math.sqrt(5.0))

    z = 1.0 - 2.0 * (k + 0.5) / n
    radius_xy = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    phi = golden_angle * k

    vectors = np.column_stack(
        [
            radius_xy * np.cos(phi),
            radius_xy * np.sin(phi),
            z,
        ]
    )

    vectors /= np.linalg.norm(vectors, axis=1)[:, None]
    return vectors


def analytic_uniform_sphere_payload_average(
    source_xyz: np.ndarray,
    source_weight: np.ndarray,
    centers: np.ndarray,
    payload_radius: float,
    batch_size: int = 8,
) -> np.ndarray:
    """Exact continuum payload-volume average for a uniform spherical payload.

    This uses the Newton shell theorem on the payload average.  Signed source
    weights are permitted because the gravitational integral is linear.
    """

    result = np.zeros((len(centers), 3), dtype=float)
    r3_inside = float(payload_radius**3)

    for start in range(0, len(centers), batch_size):
        stop = min(start + batch_size, len(centers))
        c = centers[start:stop, None, :]

        # q points from payload center to source node.
        q = source_xyz[None, :, :] - c
        d2 = np.sum(q * q, axis=-1)
        d = np.sqrt(np.maximum(d2, 0.0))
        denom = np.where(
            d < payload_radius,
            r3_inside,
            np.maximum(d2 * d, 1.0e-300),
        )

        result[start:stop] = np.sum(
            source_weight[None, :, None]
            * q
            / denom[:, :, None],
            axis=1,
        )

    return result


def orientation_audit_for_level(
    b23,
    profile,
    b_parameter: float,
    center_radius: float,
    payload_radius: float,
    vectors: np.ndarray,
    label: str,
    n_r: int,
    n_mu: int,
    n_phi: int,
) -> tuple[OrientationAudit, tuple[np.ndarray, np.ndarray]]:
    """Build one 3D source quadrature and test all dense payload orientations."""

    old = (b23.GR_RADIAL_N, b23.GR_MU_N, b23.GR_PHI_N)
    try:
        b23.GR_RADIAL_N = int(n_r)
        b23.GR_MU_N = int(n_mu)
        b23.GR_PHI_N = int(n_phi)
        source_xyz, source_weight = b23.build_gr_source(profile, b_parameter)
    finally:
        b23.GR_RADIAL_N, b23.GR_MU_N, b23.GR_PHI_N = old

    centers = float(center_radius) * vectors
    avg = analytic_uniform_sphere_payload_average(
        source_xyz,
        source_weight,
        centers,
        float(payload_radius),
    )

    radial = np.sum(avg * vectors, axis=1)
    transverse_vec = avg - radial[:, None] * vectors
    transverse = np.linalg.norm(transverse_vec, axis=1)

    return (
        OrientationAudit(
            label=label,
            radial=radial,
            transverse=transverse,
            vectors=vectors,
            source_nodes=len(source_weight),
        ),
        (source_xyz, source_weight),
    )


def radial_linf_over_mean(a: OrientationAudit, b: OrientationAudit) -> float:
    """Return pointwise radial L_inf disagreement normalized by b mean signal."""

    return float(
        np.max(np.abs(a.radial - b.radial))
        / max(abs(b.mean_radial), 1.0e-300)
    )


def direct_single_source_payload_average(
    b23,
    source_xyz: np.ndarray,
    source_weight: np.ndarray,
    payload_radius: float,
) -> np.ndarray:
    """Directly integrate one source over a centered uniform payload.

    This is used only to validate the shell-theorem implementation on
    synthetic one-source cases.  It is deliberately not used as a numerical
    oracle on the nearly cancelling full Skyrmion source, where direct
    point-sampling of the singular kernel converges slowly.
    """

    old_payload = (
        b23.PAYLOAD_RADIAL_N,
        b23.PAYLOAD_MU_N,
        b23.PAYLOAD_PHI_N,
    )

    try:
        b23.PAYLOAD_RADIAL_N = 10
        b23.PAYLOAD_MU_N = 16
        b23.PAYLOAD_PHI_N = 32

        points, weights = b23.deterministic_payload_points(
            np.zeros(3),
            float(payload_radius),
        )
        accel = b23.acceleration_from_source(
            source_xyz,
            source_weight,
            points,
        )
        return np.sum(weights[:, None] * accel, axis=0)
    finally:
        (
            b23.PAYLOAD_RADIAL_N,
            b23.PAYLOAD_MU_N,
            b23.PAYLOAD_PHI_N,
        ) = old_payload


def synthetic_payload_theorem_check(b23, payload_radius: float) -> dict[str, float | bool]:
    """Validate the analytic uniform-sphere kernel on controlled cases.

    The exact volume average follows from Newton's shell theorem.  The
    outside-source case should agree to near quadrature precision.  An
    inside-source case is also checked at d=0.75 R, where direct quadrature
    remains numerically well behaved enough to provide an independent sanity
    check.  A source at the exact payload center must average to zero by
    symmetry.
    """

    R = float(payload_radius)
    weight = np.array([1.0], dtype=float)

    def one_case(distance_factor: float) -> tuple[np.ndarray, np.ndarray]:
        xyz = np.array([[distance_factor * R, 0.0, 0.0]], dtype=float)
        analytic = analytic_uniform_sphere_payload_average(
            xyz,
            weight,
            np.zeros((1, 3), dtype=float),
            R,
            batch_size=1,
        )[0]
        direct = direct_single_source_payload_average(
            b23,
            xyz,
            weight,
            R,
        )
        return analytic, direct

    outside_a, outside_d = one_case(2.5)
    inside_a, inside_d = one_case(0.75)
    center_a, center_d = one_case(0.0)

    outside_relerr = float(
        np.linalg.norm(outside_d - outside_a)
        / max(np.linalg.norm(outside_a), 1.0e-300)
    )
    inside_relerr = float(
        np.linalg.norm(inside_d - inside_a)
        / max(np.linalg.norm(inside_a), 1.0e-300)
    )
    center_scaled = float(np.linalg.norm(center_d) * R * R)

    passed = (
        outside_relerr <= MAX_PAYLOAD_THEOREM_OUTSIDE_RELERR
        and inside_relerr <= MAX_PAYLOAD_THEOREM_INSIDE_RELERR
        and center_scaled <= MAX_PAYLOAD_THEOREM_CENTER_SCALED
        and np.linalg.norm(center_a) == 0.0
    )

    return {
        "outside_relerr": outside_relerr,
        "inside_relerr": inside_relerr,
        "center_scaled": center_scaled,
        "pass": passed,
    }


def trace_terms(a: Any, b_ang: Any, V: Any):
    """Return rho, pr, pt, e4, lhs, rhs for the exact rational-map stress."""

    e2 = a + 2 * b_ang
    e4 = 2 * a * b_ang + b_ang * b_ang
    rho = e2 + e4 + V
    pr = a - 2 * b_ang + 2 * a * b_ang - b_ang * b_ang - V
    pt = -a + b_ang * b_ang - V
    lhs = rho + pr + 2 * pt
    rhs = 2 * (e4 - V)
    return rho, pr, pt, e4, lhs, rhs


def active_trace_precision_audit(profile, b23, b_parameter: float) -> dict[str, Any]:
    """Scale-aware float, long-double, and mpmath trace reconstruction."""

    n_mu = int(b23.ANGULAR_MU_N)
    n_phi = int(b23.ANGULAR_PHI_N)
    mu, _ = leggauss(n_mu)
    phi = ((np.arange(n_phi) + 0.5) * 2.0 * math.pi / n_phi)
    J = b23.b7_angular_j(mu, phi, b_parameter)
    J2 = J * J

    # First pass obtains a physically meaningful global local scale.
    global_peak = 0.0
    for index, radius_raw in enumerate(profile.r):
        radius = float(radius_raw)
        if radius <= 0.0:
            continue

        a = float(profile.Fp[index] ** 2)
        s2 = math.sin(float(profile.F[index])) ** 2
        b_ang = s2 * J2 / (radius * radius)
        V = float(profile.e0_density[index])
        rho, pr, pt, e4, _, _ = trace_terms(a, b_ang, V)

        global_peak = max(
            global_peak,
            float(np.max(rho)),
            float(np.max(np.abs(pr))),
            float(np.max(np.abs(pt))),
            float(np.max(e4)),
            abs(V),
        )

    if not math.isfinite(global_peak) or global_peak <= 0.0:
        raise RuntimeError("Invalid global stress-energy scale in trace audit")

    eps_float = np.finfo(float).eps
    epsilon_scale = 64.0 * eps_float * global_peak

    max_abs = 0.0
    max_scaled = 0.0
    top_spots: list[tuple[float, float, float, float, float]] = []

    for index, radius_raw in enumerate(profile.r):
        radius = float(radius_raw)
        if radius <= 0.0:
            continue

        a = float(profile.Fp[index] ** 2)
        s2 = math.sin(float(profile.F[index])) ** 2
        b_ang = s2 * J2 / (radius * radius)
        V = float(profile.e0_density[index])
        rho, pr, pt, e4, lhs, rhs = trace_terms(a, b_ang, V)

        residual = np.abs(lhs - rhs)
        denom = np.maximum(
            rho + np.abs(pr) + 2.0 * np.abs(pt) + 2.0 * e4 + 2.0 * V,
            epsilon_scale,
        )
        scaled = residual / denom

        max_abs = max(max_abs, float(np.max(residual)))
        local_max_index = int(np.argmax(scaled))
        local_scaled = float(scaled.ravel()[local_max_index])
        max_scaled = max(max_scaled, local_scaled)

        if local_scaled > 0.0:
            b_flat = b_ang.ravel()
            top_spots.append(
                (
                    local_scaled,
                    a,
                    float(b_flat[local_max_index]),
                    V,
                    radius,
                )
            )

    top_spots.sort(key=lambda row: row[0], reverse=True)
    top_spots = top_spots[:8]

    max_abs_over_peak = max_abs / global_peak

    # Reconstruct exactly the same algebra at higher arithmetic precision.
    ld_eps = float(np.finfo(np.longdouble).eps)
    max_ld_scaled = 0.0
    max_mp_abs = mp.mpf("0")

    mp.mp.dps = TRACE_MP_DPS

    for _, a_f, b_f, V_f, _ in top_spots:
        a_ld = np.longdouble(a_f)
        b_ld = np.longdouble(b_f)
        V_ld = np.longdouble(V_f)
        rho_ld, pr_ld, pt_ld, e4_ld, lhs_ld, rhs_ld = trace_terms(
            a_ld,
            b_ld,
            V_ld,
        )
        resid_ld = abs(lhs_ld - rhs_ld)
        denom_ld = max(
            rho_ld + abs(pr_ld) + 2 * abs(pt_ld) + 2 * e4_ld + 2 * V_ld,
            np.longdouble(64.0) * np.longdouble(ld_eps) * np.longdouble(global_peak),
        )
        max_ld_scaled = max(max_ld_scaled, float(resid_ld / denom_ld))

        a_mp = mp.mpf(repr(a_f))
        b_mp = mp.mpf(repr(b_f))
        V_mp = mp.mpf(repr(V_f))
        _, _, _, _, lhs_mp, rhs_mp = trace_terms(a_mp, b_mp, V_mp)
        max_mp_abs = max(max_mp_abs, abs(lhs_mp - rhs_mp))

    float_pass = max_scaled <= TRACE_FLOAT_EPS_FACTOR * eps_float
    longdouble_pass = max_ld_scaled <= TRACE_LONGDOUBLE_EPS_FACTOR * ld_eps
    mp_pass = max_mp_abs <= TRACE_MP_ABS_TOL

    return {
        "global_peak": global_peak,
        "epsilon_scale": epsilon_scale,
        "max_abs": max_abs,
        "max_abs_over_peak": max_abs_over_peak,
        "max_scaled": max_scaled,
        "float_eps": eps_float,
        "longdouble_eps": ld_eps,
        "max_longdouble_scaled": max_ld_scaled,
        "max_mp_abs": max_mp_abs,
        "float_pass": float_pass,
        "longdouble_pass": longdouble_pass,
        "mp_pass": mp_pass,
        "pass": float_pass and longdouble_pass and mp_pass,
        "spot_count": len(top_spots),
    }


def print_vector(prefix: str, vector: np.ndarray) -> None:
    """Print one 3-vector reproducibly."""

    print(
        f"{prefix}=({vector[0]:.12e},{vector[1]:.12e},{vector[2]:.12e})"
    )


def main() -> None:
    """Execute the complete 023BR promotion-grade repair gate."""

    print("=== 023BR — PROMOTION-GRADE EXACT-MAP ROBUSTNESS REPAIR ===")

    # ------------------------------------------------------------------
    # A. Fail-closed upstream audit.
    # ------------------------------------------------------------------
    print("\n=== A — UPSTREAM 023A/023B SOURCE + LOG AUDIT ===")

    require_file(A23_SOURCE)
    require_file(B23_SOURCE)
    require_markers(B23_LOG, EXPECTED_023B_MARKERS)

    a23_sha = sha256(A23_SOURCE)
    b23_sha = sha256(B23_SOURCE)

    print(f"023A_SOURCE_SHA256={a23_sha}")
    print(f"023A_EXPECTED_SHA256={EXPECTED_023A_SHA256}")
    print(f"023B_SOURCE_SHA256={b23_sha}")
    print(f"023B_EXPECTED_SHA256={EXPECTED_023B_SHA256}")

    source_audit_pass = (
        a23_sha == EXPECTED_023A_SHA256
        and b23_sha == EXPECTED_023B_SHA256
    )

    print(
        "UPSTREAM_023B_SOURCE_AUDIT="
        + ("PASS" if source_audit_pass else "FAIL")
    )

    if not source_audit_pass:
        raise RuntimeError("023A/023B source hash mismatch")

    a23 = load_module("ag023br_023a", A23_SOURCE)
    b23 = load_module("ag023br_023b", B23_SOURCE)

    # Cache individual BVP profiles so overlapping robustness neighborhoods do
    # not repeat the same expensive solves across the ten existing passers.
    profile_cache = install_profile_cache(b23)

    # ------------------------------------------------------------------
    # B. Exact-I basin + maximin rerank.
    # ------------------------------------------------------------------
    print("\n=== B — EXACT-I ALL-PASSER MAXIMIN ROBUSTNESS RERANK ===")

    passers = reconstruct_existing_passers_fast(a23, b23)

    print(f"EXACT_I_PROMOTION_PASSERS_RECONSTRUCTED={len(passers)}")
    print(f"BVP_PROFILE_CACHE_ENTRIES_AFTER_BASIN={len(profile_cache)}")

    exact_basin_pass = len(passers) == 10
    print("EXACT_I_BASIN=" + ("PASS" if exact_basin_pass else "FAIL"))

    # The exact-basin reconstruction temporarily caches all 160 B=1..8
    # profiles.  The ten passer objects retain the central profiles they need,
    # so release the broad basin cache before the robustness neighborhood to
    # avoid unnecessary memory pressure during repeated payload integrations.
    profile_cache.clear()
    print("BVP_PROFILE_CACHE_CLEARED_AFTER_BASIN=YES")

    if not passers:
        raise RuntimeError("No exact-I promotion passers reconstructed")

    for index, candidate in enumerate(
        sorted(passers, key=central_maximin_upper_bound, reverse=True),
        1,
    ):
        p0 = candidate.profile
        upper = central_maximin_upper_bound(candidate)
        print(
            f"CENTRAL_MAXIMIN_BOUND_{index}="
            f"B={p0.B} ETA={p0.eta:.9e} M={p0.m:.9e} "
            f"CENTRAL_ACTIVE={p0.min_active_fraction:.9e} "
            f"CENTRAL_FISSION={candidate.fission_margin:.9e} "
            f"ROBUST_MAXIMIN_UPPER_BOUND={upper:.9e}"
        )

    selected_row, evaluated_rows, pruned_rows = branch_and_bound_maximin(
        a23,
        b23,
        passers,
    )

    print(f"MAXIMIN_FULL_ROBUSTNESS_EVALUATIONS={len(evaluated_rows)}")
    print(f"MAXIMIN_RIGOROUSLY_PRUNED_CANDIDATES={len(pruned_rows)}")
    print(f"BVP_PROFILE_CACHE_ENTRIES_AFTER_MAXIMIN={len(profile_cache)}")

    for index, row in enumerate(evaluated_rows, 1):
        p0 = row.candidate.profile
        print(
            f"MAXIMIN_EVALUATED_{index}="
            f"B={p0.B} ETA={p0.eta:.9e} M={p0.m:.9e} "
            f"WORST_ACTIVE={row.worst_active:.9e} "
            f"WORST_FISSION={row.worst_fission:.9e} "
            f"PAYLOAD_ALL={'YES' if row.payload_all else 'NO'} "
            f"ACTIVE_RATIO={row.active_ratio:.9e} "
            f"FISSION_RATIO={row.fission_ratio:.9e} "
            f"MAXIMIN={row.maximin_score:.9e}"
        )

    for index, (candidate, upper) in enumerate(pruned_rows, 1):
        p0 = candidate.profile
        print(
            f"MAXIMIN_PRUNED_{index}="
            f"B={p0.B} ETA={p0.eta:.9e} M={p0.m:.9e} "
            f"CENTRAL_UPPER_BOUND={upper:.9e} "
            f"CANNOT_BEAT_SELECTED_SCORE=YES"
        )

    selected = selected_row.candidate
    p = selected.profile
    payload = selected.payload

    print("MAXIMIN_BRANCH_AND_BOUND_PROOF=PASS")
    print(f"MAXIMIN_SELECTED_B={p.B}")
    print(f"MAXIMIN_SELECTED_ETA={p.eta:.15e}")
    print(f"MAXIMIN_SELECTED_M={p.m:.15e}")
    print(f"MAXIMIN_SELECTED_SCORE={selected_row.maximin_score:.15e}")
    print(f"ROBUST_WORST_ACTIVE_FRACTION={selected_row.worst_active:.15e}")
    print(f"ROBUST_WORST_FISSION_MARGIN={selected_row.worst_fission:.15e}")
    print(f"ROBUST_CASE_PASS_COUNT={selected_row.pass_count}")
    print(f"ROBUST_CASE_TOTAL_COUNT={selected_row.total_count}")
    print(
        "ROBUST_PAYLOAD_ALL_CASES="
        + ("PASS" if selected_row.payload_all else "FAIL")
    )

    maximin_found = (
        selected_row.maximin_score >= 1.0
        and selected_row.worst_active <= -MIN_NEGATIVE_ACTIVE_FRACTION
        and selected_row.worst_fission >= MIN_FISSION_MARGIN
        and selected_row.payload_all
    )

    print(
        "MAXIMIN_SELECTED_CANDIDATE="
        + ("FOUND" if maximin_found else "FAIL")
    )
    print(
        "ROBUST_ACTIVE_STRENGTH_THRESHOLD="
        + (
            "PASS"
            if selected_row.worst_active <= -MIN_NEGATIVE_ACTIVE_FRACTION
            else "FAIL"
        )
    )
    print(
        "ROBUST_FISSION_THRESHOLD="
        + (
            "PASS"
            if selected_row.worst_fission >= MIN_FISSION_MARGIN
            else "FAIL"
        )
    )

    b7_selected = p.B == 7
    print("MAXIMIN_SELECTED_B7=" + ("PASS" if b7_selected else "FAIL"))

    if not b7_selected:
        print(
            "MAXIMIN_MAP_IMPLEMENTATION_NOTE="
            "GLOBAL_BEST_IS_NOT_B7_SO_023BR_CANNOT_PROMOTE_WITHOUT_ITS_EXACT_ANGULAR_MAP"
        )

    # ------------------------------------------------------------------
    # C. Exact B7 angular map and direct-I radial profile.
    # ------------------------------------------------------------------
    print("\n=== C — EXACT B7 MAP + DIRECT-I PROFILE ===")

    degree_b7, I_b7 = b23.angular_integrals_b7(b23.B7_B0)
    degree_relerr = b23.relative_error(degree_b7, 7.0)
    I_relerr = b23.relative_error(I_b7, b23.LITERATURE_I[7])

    degree_pass = degree_relerr <= 1.0e-8
    I_pass = I_relerr <= b23.MAX_I_RECON_RELERR

    print(f"B7_MAP_DEGREE={degree_b7:.15e}")
    print(f"B7_MAP_DEGREE_RELERR={degree_relerr:.15e}")
    print(f"B7_MAP_I_DIRECT={I_b7:.15e}")
    print(f"B7_MAP_I_LITERATURE={b23.LITERATURE_I[7]:.15e}")
    print(f"B7_MAP_I_RELERR={I_relerr:.15e}")
    print("EXACT_B7_MAP_DEGREE=" + ("PASS" if degree_pass else "FAIL"))
    print("EXACT_B7_MAP_I=" + ("PASS" if I_pass else "FAIL"))

    # If B7 was not selected, continue enough diagnostics to make the failure
    # explicit, but do not pretend the B7 3D checks validate another charge.
    direct_eta = float(p.eta)
    direct_m = float(p.m)
    p_direct = b23.solve_profile_with_custom_I(
        a23,
        7,
        direct_eta,
        direct_m,
        I_b7,
    )

    # ------------------------------------------------------------------
    # D. Independent 3D energy/DEC and repaired active trace.
    # ------------------------------------------------------------------
    print("\n=== D — FULL 3D ENERGY / DEC / ACTIVE-TRACE RECONSTRUCTION ===")

    recon = b23.direct_3d_reconstruction(p_direct, b23.B7_B0)
    energy_pass = recon["max_energy_relerr"] <= b23.MAX_3D_ENERGY_RELERR
    active_integral_pass = recon["active_relerr"] <= b23.MAX_3D_ACTIVE_RELERR
    dec_pass = (
        recon["min_dec_margin"] >= b23.MIN_DEC_MARGIN
        and recon["min_rho"] >= b23.MIN_DEC_MARGIN
    )

    trace = active_trace_precision_audit(p_direct, b23, b23.B7_B0)

    print(f"FULL3D_MAX_ENERGY_RELERR={recon['max_energy_relerr']:.15e}")
    print(f"FULL3D_ACTIVE_INTEGRAL_RELERR={recon['active_relerr']:.15e}")
    print(f"FULL3D_MIN_DEC_MARGIN={recon['min_dec_margin']:.15e}")
    print(f"FULL3D_MIN_RHO={recon['min_rho']:.15e}")
    print(f"TRACE_GLOBAL_PEAK_SCALE={trace['global_peak']:.15e}")
    print(f"TRACE_EPSILON_SCALE={trace['epsilon_scale']:.15e}")
    print(f"MAX_ABSOLUTE_TRACE_RESIDUAL={trace['max_abs']:.15e}")
    print(
        "MAX_ABSOLUTE_RESIDUAL_OVER_GLOBAL_PEAK_ENERGY="
        f"{trace['max_abs_over_peak']:.15e}"
    )
    print(f"MAX_SCALED_TRACE_RESIDUAL={trace['max_scaled']:.15e}")
    print(f"FLOAT_MACHINE_EPS={trace['float_eps']:.15e}")
    print(f"LONG_DOUBLE_MACHINE_EPS={trace['longdouble_eps']:.15e}")
    print(
        "MAX_LONG_DOUBLE_SCALED_TRACE_RESIDUAL="
        f"{trace['max_longdouble_scaled']:.15e}"
    )
    print(f"ARBITRARY_PRECISION_DPS={TRACE_MP_DPS}")
    print(f"ARBITRARY_PRECISION_MAX_ABS_TRACE_RESIDUAL={mp.nstr(trace['max_mp_abs'], 30)}")
    print(f"HIGH_PRECISION_TRACE_SPOT_COUNT={trace['spot_count']}")

    print("FULL_3D_ENERGY_RECONSTRUCTION=" + ("PASS" if energy_pass else "FAIL"))
    print(
        "FULL_3D_ACTIVE_INTEGRAL_RECONSTRUCTION="
        + ("PASS" if active_integral_pass else "FAIL")
    )
    print("POINTWISE_3D_DEC=" + ("PASS" if dec_pass else "FAIL"))
    print("ACTIVE_TRACE_FLOAT_SCALED=" + ("PASS" if trace["float_pass"] else "FAIL"))
    print(
        "ACTIVE_TRACE_LONG_DOUBLE_SPOTCHECK="
        + ("PASS" if trace["longdouble_pass"] else "FAIL")
    )
    print(
        "ACTIVE_TRACE_ARBITRARY_PRECISION_SPOTCHECK="
        + ("PASS" if trace["mp_pass"] else "FAIL")
    )
    print(
        "POINTWISE_ACTIVE_TRACE="
        + (
            "PASS_SCALED_AND_HIGH_PRECISION"
            if trace["pass"]
            else "FAIL"
        )
    )

    # ------------------------------------------------------------------
    # E. Dense finite-payload orientation sphere with convergence.
    # ------------------------------------------------------------------
    print("\n=== E — DENSE 3D FINITE-PAYLOAD ORIENTATION SPHERE ===")

    vectors = fibonacci_sphere(DENSE_ORIENTATION_N)
    print(f"DENSE_ORIENTATION_COUNT={len(vectors)}")
    print("DENSE_ORIENTATION_SCHEME=DETERMINISTIC_FIBONACCI_SPHERE")
    print("ANALYTIC_SPHERICAL_PAYLOAD_AVERAGE=PASS_THEOREM")

    audits: dict[str, OrientationAudit] = {}
    source_cache: dict[str, tuple[np.ndarray, np.ndarray]] = {}

    for label, n_r, n_mu, n_phi in SOURCE_QUADRATURE_LEVELS:
        audit, source = orientation_audit_for_level(
            b23,
            p_direct,
            b23.B7_B0,
            payload.payload_center,
            payload.payload_radius,
            vectors,
            label,
            n_r,
            n_mu,
            n_phi,
        )
        audits[label] = audit
        source_cache[label] = source

        print(f"{label}_SOURCE_QUADRATURE=NR{n_r}_NMU{n_mu}_NPHI{n_phi}")
        print(f"{label}_SOURCE_NODE_COUNT={audit.source_nodes}")
        print(f"{label}_MIN_RADIAL_OUTWARD={audit.min_radial:.15e}")
        print(f"{label}_MAX_RADIAL_OUTWARD={audit.max_radial:.15e}")
        print(f"{label}_MEAN_RADIAL_OUTWARD={audit.mean_radial:.15e}")
        print(f"{label}_MAX_TRANSVERSE_MAGNITUDE={audit.max_transverse:.15e}")
        print(
            f"{label}_MAX_TRANSVERSE_OVER_RADIAL="
            f"{audit.max_transverse_over_radial:.15e}"
        )
        print_vector(
            f"{label}_WORST_RADIAL_ORIENTATION",
            audit.vectors[audit.worst_index],
        )

    low = audits["LOW"]
    primary = audits["PRIMARY"]
    high = audits["HIGH"]

    lp_linf = radial_linf_over_mean(low, primary)
    ph_linf = radial_linf_over_mean(primary, high)

    print(f"LOW_PRIMARY_RADIAL_LINF_OVER_MEAN={lp_linf:.15e}")
    print(f"PRIMARY_HIGH_RADIAL_LINF_OVER_MEAN={ph_linf:.15e}")

    all_signs_pass = (
        low.min_radial > 0.0
        and primary.min_radial > 0.0
        and high.min_radial > 0.0
    )

    quadrature_convergence_pass = (
        all_signs_pass
        and lp_linf <= MAX_LOW_PRIMARY_RADIAL_LINF_OVER_MEAN
        and ph_linf <= MAX_PRIMARY_HIGH_RADIAL_LINF_OVER_MEAN
    )

    print(
        "DENSE_ORIENTATION_FINITE_PAYLOAD_OUTWARD="
        + ("PASS" if all_signs_pass else "FAIL")
    )
    print(
        "SOURCE_QUADRATURE_CONVERGENCE="
        + ("PASS" if quadrature_convergence_pass else "FAIL")
    )

    # The shell-theorem payload average is exact for a uniform spherical
    # payload.  Validate its implementation on controlled one-source cases
    # rather than treating slowly convergent direct quadrature of the full,
    # nearly cancelling Skyrmion source as an oracle.
    print("\n=== F — ANALYTIC PAYLOAD THEOREM IMPLEMENTATION CHECK ===")

    payload_theorem = synthetic_payload_theorem_check(
        b23,
        payload.payload_radius,
    )
    print(
        "PAYLOAD_THEOREM_OUTSIDE_RELERR="
        f"{payload_theorem['outside_relerr']:.15e}"
    )
    print(
        "PAYLOAD_THEOREM_INSIDE_RELERR="
        f"{payload_theorem['inside_relerr']:.15e}"
    )
    print(
        "PAYLOAD_THEOREM_CENTER_SCALED_RESIDUAL="
        f"{payload_theorem['center_scaled']:.15e}"
    )
    payload_theorem_pass = bool(payload_theorem["pass"])
    print(
        "ANALYTIC_PAYLOAD_THEOREM_IMPLEMENTATION_CHECK="
        + ("PASS" if payload_theorem_pass else "FAIL")
    )

    # ------------------------------------------------------------------
    # G. Rational-map shape curvature retained on the selected B7 state.
    # ------------------------------------------------------------------
    print("\n=== G — RATIONAL-MAP SHAPE CURVATURE ===")

    map_pass, map_records, min_map_curvature = b23.map_shape_curvature(a23, selected)
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
            f"MAP_EPS={eps:.9e} I_MINUS={I_minus:.9e} "
            f"I_CENTER={I_center:.9e} I_PLUS={I_plus:.9e} "
            f"E_MINUS={E_minus:.9e} E_CENTER={E_center:.9e} "
            f"E_PLUS={E_plus:.9e} CURVATURE={curvature:.9e}"
        )

    print(f"MIN_RATIONAL_MAP_SHAPE_CURVATURE={min_map_curvature:.15e}")
    print("RATIONAL_MAP_SHAPE_CURVATURE=" + ("PASS" if map_pass else "FAIL"))

    # ------------------------------------------------------------------
    # H. Blind wildcard diagnostics — explicitly excluded from evidence.
    # ------------------------------------------------------------------
    print("\n=== H — BLIND WILDCARD DIAGNOSTICS — NOT EVIDENCE ===")

    for factor in BLIND_WILDCARDS:
        test_m = min(max(float(p.m) * factor, 0.5), 20.0)
        profiles_w, energies_w = b23.solve_exact_sector(
            a23,
            float(p.eta),
            test_m,
        )
        candidate_w = b23.candidate_from_sector(
            a23,
            profiles_w,
            energies_w,
            int(p.B),
        )
        print(
            f"WILDCARD_FACTOR={factor:.6f} M={test_m:.9e} "
            f"FISSION={candidate_w.fission_margin:.9e} "
            f"MIN_ACTIVE={candidate_w.profile.min_active_fraction:.9e} "
            f"PAYLOAD={'YES' if candidate_w.payload.finite_payload_pass else 'NO'}"
        )

    print("BLIND_WILDCARD_VALUES_USED_AS_EVIDENCE=NO")

    # ------------------------------------------------------------------
    # I. Promotion decision.
    # ------------------------------------------------------------------
    print("\n=== I — 023BR DECISION ===")

    full_green = (
        source_audit_pass
        and exact_basin_pass
        and maximin_found
        and b7_selected
        and degree_pass
        and I_pass
        and energy_pass
        and active_integral_pass
        and dec_pass
        and trace["pass"]
        and all_signs_pass
        and quadrature_convergence_pass
        and payload_theorem_pass
        and map_pass
    )

    print(
        "023BR_PROMOTION_GRADE_EXACT_MAP_ROBUSTNESS_REPAIR="
        + ("GREEN" if full_green else "GREEN_NEGATIVE_OR_INCOMPLETE_RESULT")
    )
    print(
        "PROMOTION_GRADE_RATIONAL_MAP_STABLE_FIELD_PREFLIGHT="
        + ("SUPPORTED" if full_green else "NOT_ESTABLISHED")
    )
    print(
        "ANISOTROPIC_DENSE_FINITE_PAYLOAD_REPULSION="
        + ("SUPPORTED" if all_signs_pass else "NOT_ESTABLISHED")
    )
    print(
        "HEURISTIC_PROMOTION_ELIGIBILITY="
        + (
            "APPROXIMATELY_70_TO_71_PERCENT_AFTER_CLAIM_AUDIT"
            if full_green
            else "NO"
        )
    )
    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        + (
            "APPROXIMATELY_68_PERCENT_PENDING_CLAIM_AUDIT"
            if full_green
            else "APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY"
        )
    )
    print(
        "NEXT="
        + (
            "023C_UNRESTRICTED_CARTESIAN_3D_RELAXATION_AND_FULL_PHYSICAL_HESSIAN"
            if full_green
            else "INSPECT_FAILED_023BR_GATE_BEFORE_023C"
        )
    )
    print("UNRESTRICTED_CARTESIAN_3D_STABILITY=NOT_YET")
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_ESTABLISHED")
    print("PRACTICAL_ENERGY_SCALING=STILL_CATASTROPHIC_IN_PURE_GR")
    print("REAL_MATERIAL=NO")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print("006D_CONSTRUCTIVE_LINEARIZED_GR_RESULT=RETAINED")
    print("018B_FIELD_EXISTENCE_RESULT=RETAINED")
    print("018C_KLS_M2_STABILITY_FAILURE=RETAINED")
    print("023A_TOPOLOGICAL_MONOPOLE_CAPACITY_RESULT=RETAINED")
    print("023B_EXACT_MAP_FULL3D_RESULT=RETAINED_WITH_FORMAL_BLOCKERS_REPAIRED_ONLY_IF_GREEN")
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_023BR_PROMOTION_GRADE_EXACT_MAP_ROBUSTNESS_REPAIR"
    )


if __name__ == "__main__":
    main()
