#!/usr/bin/env python3
"""024A1 — fixed-field sextic kernel-placement gate.

PURPOSE
-------
Test the cheapest decisive geometric prerequisite for the generalized
L2+L4+L6+V successor before any expensive generalized-field relaxation.

024A analytical preflight established that a positive sextic baryon-current
squared term can raise the local static active-source ceiling from

    S/rho <= 2

to

    S/rho <= 4,

and can in principle reproduce the teacher trace near S/rho ~= 2.65.
That constitutive fact does not imply that the sextic energy naturally lives
in a useful location for the finite-payload gravitational kernel.

SCIENTIFIC QUESTION
-------------------
On the two strongest current B=7 reference geometries,

1. the promotion-grade exact rational-map field, and
2. the strict stationary unrestricted N=65 field,

does the natural static sextic density

    e6(x) proportional to B0(x)^2

have better finite-payload kernel leverage per unit energy than the current
field as a whole?

OPERATIONAL OBSERVABLE
----------------------
For payload direction n, center c=h n, radius Rp, and source point x,

    K_P(x;n) = ((x-c).n) / max(|x-c|^3, Rp^3)

with positive integral defined as outward.

For the baseline field,

    A0(n) = integral S0 K_P dV
    eta0(n) = A0(n) / E0

(up to the common h^2 factor used in the project coefficient).

Normalize the sextic *shape* by its total raw integral E6_raw and add a
fraction lambda of the baseline energy in that fixed shape:

    E6 = lambda E0
    alpha = lambda E0 / E6_raw

so

    rho_lambda = rho0 + alpha e6_raw
    S_lambda   = S0   + 4 alpha e6_raw.

This parameterization is independent of the arbitrary normalization chosen for
B0 and c6.  It asks only whether the natural B0^2 spatial shape is favorable.

The infinitesimal efficiency condition is exact for the frozen field:

    d/dlambda [A/E] at lambda=0 > 0

iff

    4 L6(n) > A0(n)/E0

where

    L6(n) = [integral e6_raw K_P dV] / E6_raw.

Define the dimensionless gain ratio

    G6(n) = 4 L6(n) / [A0(n)/E0].

Then G6>1 means an infinitesimal sextic addition improves operational
acceleration per total energy in that orientation.  G6<1 means it worsens it.

CHEAPEST DECISIVE TEST
----------------------
- Rebuild the exact B=7 rational-map source at low/primary/high quadrature.
- Verify the trusted INT-15 reference-direction force at primary quadrature.
- Evaluate baseline and sextic leverage over the same 320-direction Fibonacci
  sphere used by 023BR.
- Load the strict stationary N=65 artifact and reconstruct rho, S, B0^2 and
  the same 320 payload directions using the current fourth-order continuum
  derivative diagnostic.
- Scan finite frozen-field sextic energy fractions lambda without re-relaxing
  the field.
- Optionally compare sextic placement with the saved INT-15 teacher F90 mask.

PROMOTION CONDITION
-------------------
The direct BPS-sextic placement hypothesis is promoted to a generalized-field
re-equilibration scout if the strict stationary N=65 field satisfies both:

    WORST_DIRECTION_G6 > 1

and

    some lambda > 0 improves the dense-320 worst-direction coefficient while
    retaining outward force in all 320 tested orientations.

The rational-map result is a secondary independent representation check.

FALSIFIER / STOP RULE
---------------------
If BOTH the exact-map and strict N=65 geometries have worst-direction G6 <= 1
and no positive finite lambda improves the dense-orientation coefficient, do
not launch a large L2+L4+L6+V PDE scan by simply turning on c6.  The constitutive
route remains mathematically open, but it needs a mechanism that reorganizes
topology/geometry or a different well-motivated higher-order operator.

INTERPRETATION LIMITS
---------------------
This is a fixed-field derivative and finite-coupling scout.  It does NOT solve
the generalized Euler-Lagrange equations.  It does not establish stationarity
or stability after c6 is turned on.  A finite-lambda improvement is a
promotion criterion for re-equilibration, not a physical successor field.

The N=65 continuum readout remains a single-grid diagnostic.  It is used here
because that field has already passed strict discrete stationarity; it is not a
continuum force certificate.

RELATED FILES
-------------
    simulations/023a_topological_false_core_multiskyrmion_gr_repulsion_gate.py
    simulations/023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.py
    simulations/023br_promotion_grade_exact_map_robustness_repair.py
    simulations/023cr3_geometric_degree_guarded_unrestricted_relaxation.py
    simulations/023cr4r_rlbfgs_stationarity_closure_gradient_audit_repair.py
    results/data/023cr4r_strict_stationary_b7_n65.npz
    results/data/int15_teacher_b7_comparison_maps.npz

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_024A1_FIXED_FIELD_SEXTIC_KERNEL_PLACEMENT_GATE
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import PchipInterpolator


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

A23_SOURCE = SIM / "023a_topological_false_core_multiskyrmion_gr_repulsion_gate.py"
B23_SOURCE = SIM / "023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.py"
CR3_SOURCE = SIM / "023cr3_geometric_degree_guarded_unrestricted_relaxation.py"
N65_ARTIFACT = DATA / "023cr4r_strict_stationary_b7_n65.npz"
TEACHER_MAPS = DATA / "int15_teacher_b7_comparison_maps.npz"

OUT_JSON = DATA / "024a1_sextic_fixed_field_kernel_placement_summary.json"
OUT_CSV = DATA / "024a1_sextic_fixed_field_lambda_scan.csv"
OUT_NPZ = DATA / "024a1_sextic_fixed_field_orientation_arrays.npz"

B = 7
ETA = 0.40
MASS = 8.0
DENSE_N = 320
TEACHER_TARGET_S_OVER_RHO = 2.649629

# Exact-map source quadratures copied from the 023BR low/primary/high policy.
EXACT_LEVELS = (
    ("LOW", 52, 24, 48),
    ("PRIMARY", 68, 32, 64),
    ("HIGH", 84, 40, 80),
)

# Trusted INT-15 comparator orientation.  This is retained for provenance
# reproduction; the dense 320-direction minimum is reported separately.
TRUSTED_INT15_DIRECTION = np.array(
    [-0.45435018446379805, 0.01878880658050992, 0.8906249999999961],
    dtype=float,
)
TRUSTED_INT15_DIRECTION /= np.linalg.norm(TRUSTED_INT15_DIRECTION)
TRUSTED_INT15_A = 28.81787638114564
MAX_TRUSTED_A_RELERR = 2.0e-3

# Frozen-field finite-coupling diagnostic scan.  lambda is E6/E0, not c6.
LAMBDA_SCAN = np.array(
    [
        0.0,
        1.0e-4,
        3.0e-4,
        1.0e-3,
        3.0e-3,
        1.0e-2,
        3.0e-2,
        1.0e-1,
        3.0e-1,
        1.0,
        3.0,
    ],
    dtype=float,
)

# Fine logarithmic scan used only to locate the best positive frozen-field
# lambda if one exists.  It does not optimize a physical field.
LAMBDA_FINE = np.concatenate(
    [
        np.array([0.0]),
        np.logspace(-6.0, 1.0, 281),
    ]
)

MAX_BATCH_DIRECTIONS = 8


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


def fibonacci_sphere(n: int) -> np.ndarray:
    k = np.arange(n, dtype=float)
    z = 1.0 - 2.0 * (k + 0.5) / n
    rxy = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    golden = math.pi * (3.0 - math.sqrt(5.0))
    az = golden * k
    vec = np.column_stack(
        [
            rxy * np.cos(az),
            rxy * np.sin(az),
            z,
        ]
    )
    return vec / np.linalg.norm(vec, axis=1)[:, None]


def weighted_quantile(values: np.ndarray, weights: np.ndarray, q: float = 0.5) -> float:
    values = np.asarray(values, dtype=float).ravel()
    weights = np.asarray(weights, dtype=float).ravel()
    mask = np.isfinite(values) & np.isfinite(weights) & (weights > 0.0)
    if not np.any(mask):
        return float("nan")
    v = values[mask]
    w = weights[mask]
    order = np.argsort(v)
    v = v[order]
    w = w[order]
    c = np.cumsum(w)
    target = float(q) * float(c[-1])
    return float(v[min(int(np.searchsorted(c, target, side="left")), len(v) - 1)])


def exact_profile(a23, b23):
    degree, angular_I = b23.angular_integrals_b7(b23.B7_B0)
    if abs(degree - B) > 1.0e-8:
        raise RuntimeError(f"Exact B7 map degree changed: {degree}")
    profile = b23.solve_profile_with_custom_I(
        a23,
        B,
        ETA,
        MASS,
        angular_I,
    )
    sector_profiles, sector_energies = b23.solve_exact_sector(a23, ETA, MASS)
    if not all(p.success for p in sector_profiles.values()):
        raise RuntimeError("Exact sector solve failed")
    candidate = b23.candidate_from_sector(
        a23,
        sector_profiles,
        sector_energies,
        B,
    )
    return profile, candidate, float(degree), float(angular_I)


def build_exact_source(
    b23,
    profile,
    n_r: int,
    n_mu: int,
    n_phi: int,
) -> dict[str, np.ndarray | float]:
    """Return exact-map quadrature weights including e6 shape ~ a b^2."""
    curvature_true = profile.m**2 * (1.0 + profile.eta)
    tail_length = 1.0 / math.sqrt(curvature_true)
    rmax = min(
        float(profile.r[-1]),
        profile.shell_radius + 8.0 * tail_length,
    )

    ur, wur = leggauss(n_r)
    r = 0.5 * rmax * (ur + 1.0)
    wr = 0.5 * rmax * wur

    mu, wmu = leggauss(n_mu)
    phi = (np.arange(n_phi) + 0.5) * 2.0 * math.pi / n_phi
    dphi = 2.0 * math.pi / n_phi

    J = b23.b7_angular_j(mu, phi, b23.B7_B0)

    F_interp = PchipInterpolator(profile.r, profile.F, extrapolate=False)
    Fp_interp = PchipInterpolator(profile.r, profile.Fp, extrapolate=False)
    F = F_interp(r)
    Fp = Fp_interp(r)

    sin_theta = np.sqrt(1.0 - mu * mu)
    Xhat = sin_theta[:, None] * np.cos(phi)[None, :]
    Yhat = sin_theta[:, None] * np.sin(phi)[None, :]
    Zhat = mu[:, None] * np.ones((1, n_phi))
    w_ang = wmu[:, None] * np.ones((1, n_phi)) * dphi

    xyz_parts: list[np.ndarray] = []
    energy_parts: list[np.ndarray] = []
    active_parts: list[np.ndarray] = []
    e6_parts: list[np.ndarray] = []

    for ir, radius in enumerate(r):
        s2 = math.sin(float(F[ir])) ** 2
        a = float(Fp[ir] ** 2)
        bang = s2 * J**2 / (radius * radius)

        e2 = a + 2.0 * bang
        e4 = 2.0 * a * bang + bang**2
        potential = (
            profile.m**2
            * (1.0 - math.cos(float(F[ir])))
            * (1.0 + profile.eta * math.cos(float(F[ir])))
        )
        rho = e2 + e4 + potential
        active = 2.0 * (e4 - potential)

        # For rational-map strain eigenvalues (a,b,b), B0^2 is proportional
        # to a*b^2.  The omitted constant is immaterial because lambda is
        # defined by the *total added sextic energy fraction* E6/E0.
        e6_shape = a * bang**2

        volume_w = wr[ir] * radius**2 * w_ang
        xyz_parts.append(
            np.column_stack(
                [
                    (radius * Xhat).ravel(),
                    (radius * Yhat).ravel(),
                    (radius * Zhat).ravel(),
                ]
            )
        )
        energy_parts.append((volume_w * rho).ravel())
        active_parts.append((volume_w * active).ravel())
        e6_parts.append((volume_w * e6_shape).ravel())

    return {
        "xyz": np.concatenate(xyz_parts, axis=0),
        "energy_w": np.concatenate(energy_parts),
        "active_w": np.concatenate(active_parts),
        "e6_w": np.concatenate(e6_parts),
    }


def build_n65_source(cr3) -> tuple[dict[str, np.ndarray | float], dict[str, Any]]:
    require(N65_ARTIFACT)
    with np.load(N65_ARTIFACT, allow_pickle=False) as data:
        phi = np.asarray(data["phi"], dtype=float)
        axis = np.asarray(data["axis"], dtype=float)
        dx = float(np.asarray(data["dx"]).item())
        artifact_meta = {
            "B": int(np.asarray(data["B"]).item()),
            "eta": float(np.asarray(data["eta"]).item()),
            "mass": float(np.asarray(data["mass"]).item()),
            "shape": list(phi.shape),
            "source": str(np.asarray(data["source"]).item()) if "source" in data.files else "UNKNOWN",
        }

    if phi.shape != (65, 65, 65, 4):
        raise RuntimeError(f"Unexpected strict N65 field shape: {phi.shape}")
    if artifact_meta["B"] != B or abs(artifact_meta["eta"] - ETA) > 1.0e-12 or abs(artifact_meta["mass"] - MASS) > 1.0e-12:
        raise RuntimeError(f"Strict N65 metadata mismatch: {artifact_meta}")

    qx, qy, qz = cr3.central4_derivatives(phi, dx)
    _, _, _, _, _, _, e2, e4 = cr3.metric_terms(qx, qy, qz)
    center = phi[2:-2, 2:-2, 2:-2]
    potential = cr3.potential_sigma(center[..., 0])
    rho = e2 + e4 + potential
    active = 2.0 * (e4 - potential)

    # Repository topological density convention:
    # B0 = -det(phi,d_x phi,d_y phi,d_z phi)/(2 pi^2).
    # Squaring removes the orientation sign.
    mat = np.stack([center, qx, qy, qz], axis=-1)
    det = np.linalg.det(mat)
    b0 = -det / (2.0 * math.pi**2)
    e6_shape = b0 * b0

    coords = axis[2:-2]
    X, Y, Z = np.meshgrid(coords, coords, coords, indexing="ij")
    xyz = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    volume = dx**3

    source = {
        "xyz": xyz,
        "energy_w": rho.ravel() * volume,
        "active_w": active.ravel() * volume,
        "e6_w": e6_shape.ravel() * volume,
        "topology4": float(cr3.topology4(phi, dx)),
        "dx": dx,
    }
    return source, artifact_meta


def radial_kernel_matrix(
    xyz: np.ndarray,
    directions: np.ndarray,
    center_radius: float,
    payload_radius: float,
) -> np.ndarray:
    """Return radial payload kernel K for a small direction batch."""
    centers = center_radius * directions
    q = xyz[None, :, :] - centers[:, None, :]
    d2 = np.sum(q * q, axis=-1)
    d = np.sqrt(np.maximum(d2, 0.0))
    denom = np.where(
        d < payload_radius,
        payload_radius**3,
        np.maximum(d2 * d, 1.0e-300),
    )
    return np.einsum("bni,bi->bn", q, directions) / denom


def evaluate_orientations(
    source: dict[str, np.ndarray | float],
    directions: np.ndarray,
    center_radius: float,
    payload_radius: float,
) -> dict[str, Any]:
    xyz = np.asarray(source["xyz"], dtype=float)
    energy_w = np.asarray(source["energy_w"], dtype=float)
    active_w = np.asarray(source["active_w"], dtype=float)
    e6_w = np.asarray(source["e6_w"], dtype=float)

    E = float(np.sum(energy_w))
    E6_raw = float(np.sum(e6_w))
    if not math.isfinite(E) or E <= 0.0:
        raise RuntimeError("Nonpositive baseline energy")
    if not math.isfinite(E6_raw) or E6_raw <= 0.0:
        raise RuntimeError("Nonpositive sextic template integral")

    A0 = np.empty(len(directions), dtype=float)
    L6 = np.empty(len(directions), dtype=float)

    for start in range(0, len(directions), MAX_BATCH_DIRECTIONS):
        stop = min(start + MAX_BATCH_DIRECTIONS, len(directions))
        dirs = directions[start:stop]
        K = radial_kernel_matrix(xyz, dirs, center_radius, payload_radius)
        A0[start:stop] = K @ active_w
        L6[start:stop] = (K @ e6_w) / E6_raw

    eta0 = A0 / E
    gain = np.full_like(A0, np.nan)
    positive = A0 > 0.0
    gain[positive] = 4.0 * L6[positive] / eta0[positive]

    worst = int(np.argmin(A0))
    reversal_candidates = []
    for a0, l6 in zip(A0, L6):
        if a0 > 0.0 and l6 < 0.0:
            reversal_candidates.append(-a0 / (4.0 * E * l6))
    lambda_first_reversal = (
        float(min(reversal_candidates))
        if reversal_candidates
        else float("inf")
    )

    return {
        "E": E,
        "E6_raw": E6_raw,
        "A0": A0,
        "L6": L6,
        "gain_ratio": gain,
        "worst_index": worst,
        "worst_direction": directions[worst],
        "baseline_all_outward": bool(np.all(A0 > 0.0)),
        "lambda_first_reversal": lambda_first_reversal,
    }


def scan_lambdas(
    source_name: str,
    evaluation: dict[str, Any],
    center_radius: float,
    lambdas: np.ndarray,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    E = float(evaluation["E"])
    A0 = np.asarray(evaluation["A0"], dtype=float)
    L6 = np.asarray(evaluation["L6"], dtype=float)

    baseline_min = float(np.min(A0))
    baseline_C = E / (center_radius**2 * baseline_min) if baseline_min > 0.0 else float("inf")

    rows: list[dict[str, Any]] = []
    best = {
        "lambda": 0.0,
        "C_worst": baseline_C,
        "headroom_vs_lambda0": 1.0,
        "min_A": baseline_min,
        "all_outward": bool(np.all(A0 > 0.0)),
        "worst_index": int(np.argmin(A0)),
    }

    for lam in np.asarray(lambdas, dtype=float):
        A = A0 + 4.0 * lam * E * L6
        min_A = float(np.min(A))
        worst = int(np.argmin(A))
        all_outward = bool(np.all(A > 0.0))
        C = (
            E * (1.0 + lam) / (center_radius**2 * min_A)
            if min_A > 0.0
            else float("inf")
        )
        headroom = baseline_C / C if math.isfinite(C) and C > 0.0 else 0.0
        row = {
            "source": source_name,
            "lambda_E6_over_E0": float(lam),
            "min_A": min_A,
            "all_320_outward": all_outward,
            "worst_orientation_index": worst,
            "C_worst_fixed_field": C,
            "headroom_vs_lambda0": headroom,
        }
        rows.append(row)
        if all_outward and C < float(best["C_worst"]):
            best = {
                "lambda": float(lam),
                "C_worst": C,
                "headroom_vs_lambda0": headroom,
                "min_A": min_A,
                "all_outward": True,
                "worst_index": worst,
            }

    return rows, best


def force_weighted_s_over_rho_at_lambda(
    source: dict[str, np.ndarray | float],
    direction: np.ndarray,
    center_radius: float,
    payload_radius: float,
    lam: float,
) -> float:
    xyz = np.asarray(source["xyz"], dtype=float)
    energy_w = np.asarray(source["energy_w"], dtype=float)
    active_w = np.asarray(source["active_w"], dtype=float)
    e6_w = np.asarray(source["e6_w"], dtype=float)
    E = float(np.sum(energy_w))
    E6_raw = float(np.sum(e6_w))
    alpha = float(lam) * E / E6_raw

    rho_new_w = energy_w + alpha * e6_w
    active_new_w = active_w + 4.0 * alpha * e6_w
    K = radial_kernel_matrix(
        xyz,
        direction[None, :],
        center_radius,
        payload_radius,
    )[0]
    influence = active_new_w * K
    outward = np.maximum(influence, 0.0)
    ratio = active_new_w / np.maximum(rho_new_w, 1.0e-300)
    return weighted_quantile(ratio, outward, 0.5)


def teacher_overlap(
    source: dict[str, np.ndarray | float],
    direction: np.ndarray,
    center_radius: float,
    payload_radius: float,
) -> dict[str, Any]:
    if not TEACHER_MAPS.is_file():
        return {"available": False, "reason": "INT15_MAP_FILE_MISSING"}

    with np.load(TEACHER_MAPS, allow_pickle=False) as data:
        needed = {"teacher_F90_mask", "r_edges", "z_edges"}
        if not needed.issubset(data.files):
            return {"available": False, "reason": "INT15_MAP_KEYS_MISSING"}
        mask = np.asarray(data["teacher_F90_mask"], dtype=bool)
        r_edges = np.asarray(data["r_edges"], dtype=float)
        z_edges = np.asarray(data["z_edges"], dtype=float)

    xyz = np.asarray(source["xyz"], dtype=float)
    e6_w = np.asarray(source["e6_w"], dtype=float)
    K = radial_kernel_matrix(
        xyz,
        direction[None, :],
        center_radius,
        payload_radius,
    )[0]
    e6_outward = np.maximum(4.0 * e6_w * K, 0.0)

    z_parallel = xyz @ direction
    radius2 = np.sum(xyz * xyz, axis=1)
    r_perp = np.sqrt(np.maximum(radius2 - z_parallel**2, 0.0))
    r = r_perp / center_radius
    z = z_parallel / center_radius

    ir = np.searchsorted(r_edges, r, side="right") - 1
    iz = np.searchsorted(z_edges, z, side="right") - 1
    valid = (
        (ir >= 0)
        & (ir < len(r_edges) - 1)
        & (iz >= 0)
        & (iz < len(z_edges) - 1)
    )

    e6_bin = np.zeros(mask.shape, dtype=float)
    out_bin = np.zeros(mask.shape, dtype=float)
    np.add.at(e6_bin, (ir[valid], iz[valid]), e6_w[valid])
    np.add.at(out_bin, (ir[valid], iz[valid]), e6_outward[valid])

    total_e6 = float(np.sum(e6_bin))
    total_out = float(np.sum(out_bin))
    return {
        "available": True,
        "e6_energy_in_teacher_F90": float(np.sum(e6_bin[mask]) / max(total_e6, 1.0e-300)),
        "e6_gross_outward_in_teacher_F90": float(np.sum(out_bin[mask]) / max(total_out, 1.0e-300)),
        "fraction_e6_captured_by_teacher_grid": float(total_e6 / max(float(np.sum(e6_w)), 1.0e-300)),
    }


def summarize_reference(
    name: str,
    source: dict[str, np.ndarray | float],
    evaluation: dict[str, Any],
    center_radius: float,
    payload_radius: float,
) -> dict[str, Any]:
    A0 = np.asarray(evaluation["A0"], dtype=float)
    L6 = np.asarray(evaluation["L6"], dtype=float)
    gain = np.asarray(evaluation["gain_ratio"], dtype=float)
    worst = int(evaluation["worst_index"])

    coarse_rows, _ = scan_lambdas(name, evaluation, center_radius, LAMBDA_SCAN)
    _, best_fine = scan_lambdas(name, evaluation, center_radius, LAMBDA_FINE)

    lambda_one_percent = 1.0e-2
    A_1pct = A0 + 4.0 * lambda_one_percent * float(evaluation["E"]) * L6
    C0 = float(evaluation["E"]) / (center_radius**2 * float(np.min(A0)))
    C1 = (
        float(evaluation["E"]) * (1.0 + lambda_one_percent)
        / (center_radius**2 * float(np.min(A_1pct)))
        if np.min(A_1pct) > 0.0
        else float("inf")
    )
    improve_1pct = C0 / C1 if math.isfinite(C1) and C1 > 0.0 else 0.0

    worst_direction = np.asarray(evaluation["worst_direction"], dtype=float)
    teacher_median_baseline = force_weighted_s_over_rho_at_lambda(
        source,
        worst_direction,
        center_radius,
        payload_radius,
        0.0,
    )
    teacher_median_1pct = force_weighted_s_over_rho_at_lambda(
        source,
        worst_direction,
        center_radius,
        payload_radius,
        lambda_one_percent,
    )

    overlap = teacher_overlap(
        source,
        TRUSTED_INT15_DIRECTION,
        center_radius,
        payload_radius,
    )

    infinitesimal_pass = bool(gain[worst] > 1.0)
    finite_pass = bool(
        float(best_fine["lambda"]) > 0.0
        and float(best_fine["headroom_vs_lambda0"]) > 1.0
        and bool(best_fine["all_outward"])
    )

    summary = {
        "name": name,
        "E": float(evaluation["E"]),
        "E6_raw": float(evaluation["E6_raw"]),
        "baseline_all_320_outward": bool(evaluation["baseline_all_outward"]),
        "baseline_min_A": float(np.min(A0)),
        "baseline_max_A": float(np.max(A0)),
        "baseline_C_worst_dense320": C0,
        "worst_orientation_index": worst,
        "worst_orientation": worst_direction.tolist(),
        "worst_direction_L6": float(L6[worst]),
        "worst_direction_gain_ratio_G6": float(gain[worst]),
        "gain_ratio_min": float(np.nanmin(gain)),
        "gain_ratio_median": float(np.nanmedian(gain)),
        "gain_ratio_max": float(np.nanmax(gain)),
        "fraction_orientations_G6_gt_1": float(np.mean(gain > 1.0)),
        "fraction_orientations_L6_positive": float(np.mean(L6 > 0.0)),
        "lambda_first_orientation_reversal": float(evaluation["lambda_first_reversal"]),
        "one_percent_C_headroom": improve_1pct,
        "one_percent_all_320_outward": bool(np.all(A_1pct > 0.0)),
        "best_positive_frozen_lambda": best_fine,
        "force_weighted_median_S_over_rho_at_worst_lambda0": teacher_median_baseline,
        "force_weighted_median_S_over_rho_at_worst_lambda0p01": teacher_median_1pct,
        "teacher_target_S_over_rho": TEACHER_TARGET_S_OVER_RHO,
        "teacher_F90_overlap": overlap,
        "infinitesimal_worst_direction_improvement": infinitesimal_pass,
        "finite_positive_lambda_improvement": finite_pass,
        "direct_sextic_geometry_pass": infinitesimal_pass and finite_pass,
        "coarse_lambda_rows": coarse_rows,
    }
    return summary


def print_summary(prefix: str, s: dict[str, Any]) -> None:
    print(f"{prefix}_E={s['E']:.15e}")
    print(f"{prefix}_E6_RAW={s['E6_raw']:.15e}")
    print(f"{prefix}_BASELINE_MIN_A={s['baseline_min_A']:.15e}")
    print(f"{prefix}_BASELINE_MAX_A={s['baseline_max_A']:.15e}")
    print(f"{prefix}_BASELINE_C_WORST_DENSE320={s['baseline_C_worst_dense320']:.15e}")
    print(f"{prefix}_WORST_ORIENTATION_INDEX={s['worst_orientation_index']}")
    d = s["worst_orientation"]
    print(f"{prefix}_WORST_ORIENTATION=({d[0]:.12e},{d[1]:.12e},{d[2]:.12e})")
    print(f"{prefix}_WORST_DIRECTION_L6={s['worst_direction_L6']:.15e}")
    print(f"{prefix}_WORST_DIRECTION_GAIN_RATIO_G6={s['worst_direction_gain_ratio_G6']:.15e}")
    print(f"{prefix}_GAIN_RATIO_MIN={s['gain_ratio_min']:.15e}")
    print(f"{prefix}_GAIN_RATIO_MEDIAN={s['gain_ratio_median']:.15e}")
    print(f"{prefix}_GAIN_RATIO_MAX={s['gain_ratio_max']:.15e}")
    print(f"{prefix}_FRACTION_ORIENTATIONS_G6_GT_1={s['fraction_orientations_G6_gt_1']:.15e}")
    print(f"{prefix}_FRACTION_ORIENTATIONS_L6_POSITIVE={s['fraction_orientations_L6_positive']:.15e}")
    print(f"{prefix}_LAMBDA_FIRST_ORIENTATION_REVERSAL={s['lambda_first_orientation_reversal']:.15e}")
    print(f"{prefix}_ONE_PERCENT_C_HEADROOM={s['one_percent_C_headroom']:.15e}")
    print(f"{prefix}_ONE_PERCENT_ALL_320_OUTWARD=" + ("YES" if s["one_percent_all_320_outward"] else "NO"))
    best = s["best_positive_frozen_lambda"]
    print(f"{prefix}_BEST_FROZEN_LAMBDA={float(best['lambda']):.15e}")
    print(f"{prefix}_BEST_FROZEN_HEADROOM={float(best['headroom_vs_lambda0']):.15e}")
    print(f"{prefix}_FORCE_WEIGHTED_MEDIAN_S_OVER_RHO_LAMBDA0={s['force_weighted_median_S_over_rho_at_worst_lambda0']:.15e}")
    print(f"{prefix}_FORCE_WEIGHTED_MEDIAN_S_OVER_RHO_LAMBDA0P01={s['force_weighted_median_S_over_rho_at_worst_lambda0p01']:.15e}")
    overlap = s["teacher_F90_overlap"]
    print(f"{prefix}_TEACHER_F90_OVERLAP_AVAILABLE=" + ("YES" if overlap.get("available") else "NO"))
    if overlap.get("available"):
        print(f"{prefix}_E6_ENERGY_IN_TEACHER_F90={overlap['e6_energy_in_teacher_F90']:.15e}")
        print(f"{prefix}_E6_GROSS_OUTWARD_IN_TEACHER_F90={overlap['e6_gross_outward_in_teacher_F90']:.15e}")
    print(f"{prefix}_INFINITESIMAL_WORST_DIRECTION_IMPROVEMENT=" + ("PASS" if s["infinitesimal_worst_direction_improvement"] else "FAIL"))
    print(f"{prefix}_FINITE_POSITIVE_LAMBDA_IMPROVEMENT=" + ("PASS" if s["finite_positive_lambda_improvement"] else "FAIL"))
    print(f"{prefix}_DIRECT_SEXTIC_GEOMETRY=" + ("PASS" if s["direct_sextic_geometry_pass"] else "FAIL"))


def main() -> None:
    print("=== 024A1 — FIXED-FIELD SEXTIC KERNEL-PLACEMENT GATE ===", flush=True)

    for path in (A23_SOURCE, B23_SOURCE, CR3_SOURCE, N65_ARTIFACT):
        require(path)

    a23 = load_module("ag024a1_023a", A23_SOURCE)
    b23 = load_module("ag024a1_023b", B23_SOURCE)
    cr3 = load_module("ag024a1_023cr3", CR3_SOURCE)

    directions = fibonacci_sphere(DENSE_N)
    profile, candidate, degree, angular_I = exact_profile(a23, b23)
    h = float(candidate.payload.payload_center)
    rp = float(candidate.payload.payload_radius)

    print("\n=== A — EXACT B7 LOW/PRIMARY/HIGH SEXTIC LEVERAGE ===", flush=True)
    print(f"EXACT_B7_DEGREE={degree:.15e}")
    print(f"EXACT_B7_I={angular_I:.15e}")
    print(f"PAYLOAD_CENTER_RADIUS={h:.15e}")
    print(f"PAYLOAD_RADIUS={rp:.15e}")

    exact_levels: dict[str, Any] = {}
    exact_sources: dict[str, Any] = {}
    exact_evaluations: dict[str, Any] = {}
    for label, nr, nmu, nphi in EXACT_LEVELS:
        print(f"\n--- EXACT_{label} nr={nr} nmu={nmu} nphi={nphi} ---", flush=True)
        source = build_exact_source(b23, profile, nr, nmu, nphi)
        evaluation = evaluate_orientations(source, directions, h, rp)
        summary = summarize_reference(f"EXACT_{label}", source, evaluation, h, rp)
        exact_levels[label] = summary
        exact_sources[label] = source
        exact_evaluations[label] = evaluation
        print_summary(f"EXACT_{label}", summary)

    # Provenance reproduction at the trusted INT-15 direction uses the primary
    # quadrature exactly, matching INT-15's comparator resolution.
    primary = exact_sources["PRIMARY"]
    K_ref = radial_kernel_matrix(
        np.asarray(primary["xyz"]),
        TRUSTED_INT15_DIRECTION[None, :],
        h,
        rp,
    )[0]
    A_ref = float(np.sum(np.asarray(primary["active_w"]) * K_ref))
    A_ref_relerr = relative_error(A_ref, TRUSTED_INT15_A)
    ref_pass = A_ref_relerr <= MAX_TRUSTED_A_RELERR
    print("\n=== B — TRUSTED INT15 EXACT-MAP PROVENANCE ===", flush=True)
    print(f"TRUSTED_INT15_REFERENCE_A_REBUILT={A_ref:.15e}")
    print(f"TRUSTED_INT15_REFERENCE_A_EXPECTED={TRUSTED_INT15_A:.15e}")
    print(f"TRUSTED_INT15_REFERENCE_A_RELERR={A_ref_relerr:.15e}")
    print("TRUSTED_INT15_REFERENCE_REPRODUCTION=" + ("PASS" if ref_pass else "FAIL"))

    # Convergence of the new sextic leverage at the dense worst direction is
    # assessed by the reported scalar summaries, not by forcing identical
    # worst indices across quadrature levels.
    p = exact_levels["PRIMARY"]
    hi = exact_levels["HIGH"]
    exact_gain_relerr = relative_error(
        float(p["worst_direction_gain_ratio_G6"]),
        float(hi["worst_direction_gain_ratio_G6"]),
    )
    exact_minA_relerr = relative_error(
        float(p["baseline_min_A"]),
        float(hi["baseline_min_A"]),
    )
    exact_convergence = bool(exact_gain_relerr <= 0.10 and exact_minA_relerr <= 0.10)
    print(f"EXACT_PRIMARY_HIGH_WORST_G6_RELERR={exact_gain_relerr:.15e}")
    print(f"EXACT_PRIMARY_HIGH_MIN_A_RELERR={exact_minA_relerr:.15e}")
    print("EXACT_SEXTIC_LEVERAGE_CONVERGENCE=" + ("PASS" if exact_convergence else "FAIL"))

    print("\n=== C — STRICT STATIONARY N65 SEXTIC LEVERAGE ===", flush=True)
    n65_source, n65_meta = build_n65_source(cr3)
    print(f"N65_ARTIFACT_SOURCE={n65_meta['source']}")
    print(f"N65_ARTIFACT_SHAPE={tuple(n65_meta['shape'])}")
    print(f"N65_TOPOLOGY4_REBUILT={float(n65_source['topology4']):.15e}")
    n65_eval = evaluate_orientations(n65_source, directions, h, rp)
    n65_summary = summarize_reference("N65", n65_source, n65_eval, h, rp)
    print_summary("N65", n65_summary)

    print("\n=== D — FROZEN-FIELD LAMBDA SCAN ===", flush=True)
    rows: list[dict[str, Any]] = []
    for s in (exact_levels["HIGH"], n65_summary):
        rows.extend(s["coarse_lambda_rows"])
        for row in s["coarse_lambda_rows"]:
            print(
                f"{row['source']} LAMBDA={row['lambda_E6_over_E0']:.6e} "
                f"MIN_A={row['min_A']:.9e} "
                f"ALL_OUTWARD={'YES' if row['all_320_outward'] else 'NO'} "
                f"C_WORST={row['C_worst_fixed_field']:.9e} "
                f"HEADROOM={row['headroom_vs_lambda0']:.9e}",
                flush=True,
            )

    DATA.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    np.savez_compressed(
        OUT_NPZ,
        directions=directions,
        exact_high_A0=np.asarray(exact_evaluations["HIGH"]["A0"]),
        exact_high_L6=np.asarray(exact_evaluations["HIGH"]["L6"]),
        n65_A0=np.asarray(n65_eval["A0"]),
        n65_L6=np.asarray(n65_eval["L6"]),
        lambda_scan=LAMBDA_SCAN,
    )

    print("\n=== E — 024A1 DECISION ===", flush=True)
    exact_pass = bool(exact_levels["HIGH"]["direct_sextic_geometry_pass"] and exact_convergence and ref_pass)
    n65_pass = bool(n65_summary["direct_sextic_geometry_pass"] and n65_summary["baseline_all_320_outward"])

    if n65_pass and exact_pass:
        decision = "GREEN_BOTH_REFERENCES"
        next_action = "024B_REDUCED_GENERALIZED_L2_L4_L6_V_REEQUILIBRATION_SCOUT"
    elif n65_pass:
        decision = "GREEN_N65_ONLY_GEOMETRIC_REORGANIZATION_ALREADY_HELPFUL"
        next_action = "024B_N65_SEEDED_GENERALIZED_FIELD_REEQUILIBRATION_SCOUT"
    elif exact_pass:
        decision = "YELLOW_EXACT_MAP_ONLY_N65_NOT_YET_SUPPORTIVE"
        next_action = "024B_RATIONAL_MAP_GENERALIZED_PROFILE_REEQUILIBRATION_BEFORE_3D"
    else:
        decision = "RED_NAIVE_B0_SQUARED_SEXTIC_PLACEMENT_ON_CURRENT_GEOMETRIES"
        next_action = "024A2_GEOMETRY_REORGANIZING_HIGHER_ORDER_OR_ALTERNATIVE_TOPOLOGICAL_OPERATOR_PREFILTER"

    print(f"024A1_FIXED_FIELD_SEXTIC_KERNEL_PLACEMENT_GATE={decision}")
    print("EXACT_MAP_DIRECT_SEXTIC_GEOMETRY=" + ("PASS" if exact_pass else "FAIL"))
    print("N65_DIRECT_SEXTIC_GEOMETRY=" + ("PASS" if n65_pass else "FAIL"))
    print(f"NEXT={next_action}")
    print("GENERALIZED_L2_L4_L6_V_CONSTITUTIVE_PREFLIGHT=RETAINED")
    print("PURE_BPS_L6_PLUS_V_STATIC_TEACHER_MATCH=DEMOTED")
    print("LARGE_GENERALIZED_3D_PDE_SCAN_AUTHORIZED=" + ("YES" if n65_pass else "NO"))
    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_NOT_A_PROBABILITY")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_024A1_FIXED_FIELD_SEXTIC_KERNEL_PLACEMENT_GATE")

    summary = {
        "claim_classification": "PROJECT_DERIVED_024A1_FIXED_FIELD_SEXTIC_KERNEL_PLACEMENT_GATE",
        "claim_limits": {
            "generalized_field_equations_solved": False,
            "generalized_field_stationary": False,
            "generalized_field_stable": False,
            "continuum_N65_force_certified": False,
            "nonlinear_einstein_matter": False,
            "practical_device": False,
        },
        "question": "Does the natural B0^2 sextic energy shape improve finite-payload acceleration per total energy on current trusted B7 geometries?",
        "payload": {
            "center_radius": h,
            "payload_radius": rp,
            "orientation_count": DENSE_N,
        },
        "trusted_reference_reproduction": {
            "A_rebuilt": A_ref,
            "A_expected": TRUSTED_INT15_A,
            "relative_error": A_ref_relerr,
            "pass": ref_pass,
        },
        "exact_levels": {k: {kk: vv for kk, vv in v.items() if kk != "coarse_lambda_rows"} for k, v in exact_levels.items()},
        "exact_primary_high_convergence": {
            "worst_G6_relative_error": exact_gain_relerr,
            "min_A_relative_error": exact_minA_relerr,
            "pass": exact_convergence,
        },
        "n65_artifact": n65_meta,
        "n65": {k: v for k, v in n65_summary.items() if k != "coarse_lambda_rows"},
        "decision": decision,
        "next": next_action,
    }

    with OUT_JSON.open("w") as handle:
        json.dump(summary, handle, indent=2, allow_nan=True)
        handle.write("\n")

    print(f"SUMMARY_JSON={OUT_JSON.relative_to(ROOT)}")
    print(f"LAMBDA_SCAN_CSV={OUT_CSV.relative_to(ROOT)}")
    print(f"ORIENTATION_ARRAYS_NPZ={OUT_NPZ.relative_to(ROOT)}")
    print("024A1_RUN_COMPLETE=YES")


if __name__ == "__main__":
    main()

