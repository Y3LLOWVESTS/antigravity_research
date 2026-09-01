#!/usr/bin/env python3
"""INT-02/05R — signed-kernel, orientation, covariance, and representation robustness.

PURPOSE
-------
Follow the positive INT-01 N=65 influence-tomography result with one
high-information fixed-field run that asks whether the apparent productive
skeleton and extreme cancellation are robust enough to justify deeper
Introspective work.

SCIENTIFIC QUESTION
-------------------
Is the INT-01 concentration/cancellation pattern a robust mechanism-level
feature across:

1. payload orientation;
2. modest payload geometry changes;
3. cubic versus quintic continuous reconstruction; and
4. the promotion-grade exact B=7 rational-map representation?

And, more specifically, which of the four signed source/kernel channels

    S+ K+
    S+ K-
    S- K+
    S- K-

produce the gross outward and opposing finite-payload influence?

MODEL
-----
Static B=7, eta=0.4, m=8 false-core Skyrme field.

    E = integral (e2 + e4 + V) d^3x

    rho = e2 + e4 + V

    S = 2(e4 - V)

The finite spherical payload kernel is

    K_P(x') =
        [(x' - c) . n]
        / max(|x' - c|^3, R_P^3)

with positive total integral S K_P defined as outward.

SIGNED SOURCE/KERNEL DECOMPOSITION
----------------------------------
Define

    S+ = max(S, 0)
    S- = max(-S, 0)

    K+ = max(K, 0)
    K- = max(-K, 0)

Then

    A =
        integral S+ K+ dV
      + integral S- K- dV
      - integral S+ K- dV
      - integral S- K+ dV

The first two channels contribute outward.
The latter two oppose the desired outward response.

This decomposition prevents the incorrect shortcut

    negative active density = outward gravity.

ANGULAR COVARIANCE DIAGNOSTIC
-----------------------------
Within radial shell b,

    integral_b S K dV
      =
    V_b <S>_b <K>_b
      +
    V_b Cov_b(S,K)

so the difference between the true force and the radialized diagnostic is the
integrated angular source-kernel covariance.

A strongly negative covariance means the current angular arrangement is
operationally unfavorable for that payload.  Radialization remains a
counterfactual attribution diagnostic and is NOT a physical field solution.

VIRIAL AUDIT
------------
For exact continuum static equilibrium,

    E2 - E4 + 3 E0 = 0

and therefore the integrated active source equals the total energy.

The unrestricted N=65 field is a strict stationary solution of the repository
DISCRETE action.  This run separately reports the virial residual reconstructed
from the continuous spline field.  A non-small residual is a continuum /
finite-domain / representation warning; it does not erase discrete stationarity.

ORIENTATION ROBUSTNESS
----------------------
The primary N=65 test uses:

- the inherited previously worst payload direction;
- eight deterministic Fibonacci-sphere directions.

The same concentration and signed-kernel metrics are reconstructed for cubic
and quintic continuous fields.

GEOMETRY ROBUSTNESS
-------------------
At the inherited worst direction, also test:

- center distance x0.8 and x1.2;
- payload radius x0.5 and x2.0.

Two user-requested blind wildcard radius multipliers are included only as
clearly labeled non-promotion diagnostics:

    0.625
    1.6

They are NOT optimization targets or privileged physics values.

EXACT-MAP COMPARATOR
--------------------
The promotion-grade B=7 rational map is independently reconstructed from the
023A/023B field equations and direct angular map.

A separate Gauss-Legendre x Gauss-Legendre x midpoint-phi quadrature builds:

    energy weights
    active-source weights
    e4 weights
    V weights

and evaluates the exact uniform-sphere payload kernel directly.

This comparator is an independent representation, not an unrestricted
Cartesian solution.

HOTSPOT OVERLAP
---------------
For each N=65 orientation, the cubic and quintic cell sets responsible for
50 percent of gross outward influence are compared using:

- ordinary Jaccard overlap;
- energy-weighted Jaccard overlap.

Very similar F50 values are not sufficient by themselves; the spatial sets
should also agree.

NUMERICAL METHOD
----------------
N=65 continuous source:

- global fourth-order tensor Gauss cubature per source cell;
- payload-near cells replaced by the established highly subdivided near-field
  cubature used by 023C2AQS/INT-01;
- cubic and quintic normalized S^3 tensor splines;
- analytic normalized-field derivatives.

The field is never altered or re-relaxed.

PROMOTION / FALSIFICATION
-------------------------
Strong continuation evidence requires, diagnostically:

- all nominal orientations have F50 <= 0.10 in cubic and quintic;
- cubic/quintic top-50-percent hotspot energy-weighted Jaccard is >= 0.50
  on every nominal orientation;
- the dominant signed source/kernel mechanism agrees qualitatively between
  cubic and quintic;
- exact-map comparator also shows concentrated useful influence.

These thresholds are diagnostic, not fundamental constants.

This run cannot establish INT Level 2 by itself because strict N=73 or another
equivalent fine-resolution unrestricted stationary field is not yet available.

OUTPUTS
-------
results/data/int02_signed_kernel_orientation_robustness_summary.json
results/data/int02_orientation_metrics.csv
results/data/int02_baseline_shell_covariance_cubic.csv
results/data/int02_baseline_shell_covariance_quintic.csv

CLAIM LIMITS
------------
This run does NOT establish:

- removable source structure;
- a new stationary source;
- a >=10x physically achievable efficiency improvement;
- continuum-converged N=65 force sign;
- full physical Hessian stability;
- nonlinear Einstein-Skyrme consistency;
- practical energy scaling;
- a real material or device;
- new physics.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_INT02_05R_SIGNED_KERNEL_ORIENTATION_ROBUSTNESS
"""

from __future__ import annotations

from dataclasses import dataclass
import csv
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
from typing import Any

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import PchipInterpolator


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"
LOGS = ROOT / "results/logs"

INT01_SOURCE = SIM / "int01_certified_fixed_field_influence_tomography.py"
INT01_SUMMARY = DATA / "int01_certified_fixed_field_influence_tomography_summary.json"

OUT_JSON = DATA / "int02_signed_kernel_orientation_robustness_summary.json"
OUT_CSV = DATA / "int02_orientation_metrics.csv"

B = 7
ETA = 0.40
MASS = 8.0

N_EXTRA_ORIENTATIONS = max(
    4,
    int(os.environ.get("AG_INT02_EXTRA_ORIENTATIONS", "8")),
)

RADIAL_BINS = max(
    24,
    int(os.environ.get("AG_INT02_RADIAL_BINS", "80")),
)

MAX_BATCH_POINTS = max(
    20000,
    int(os.environ.get("AG_INT02_BATCH_POINTS", "120000")),
)

TOP50_WEIGHTED_JACCARD_MIN = 0.50
STRONG_F50_MAX = 0.10
VIRIAL_WARNING_REL = 1.0e-2

# Diagnostic only.  These are never used to select or promote a model.
BLIND_WILDCARD_RADIUS_MULTIPLIERS = (0.625, 1.6)


@dataclass(frozen=True)
class PayloadCase:
    label: str
    category: str
    direction: np.ndarray
    center_radius: float
    payload_radius: float
    promotion_relevant: bool


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


def unit(v: np.ndarray) -> np.ndarray:
    out = np.asarray(v, dtype=float)
    n = float(np.linalg.norm(out))
    if not math.isfinite(n) or n <= 0.0:
        raise RuntimeError("Invalid direction")
    return out / n


def fibonacci_sphere(n: int) -> np.ndarray:
    """Return deterministic approximately equal-area unit directions."""
    k = np.arange(n, dtype=float)
    z = 1.0 - 2.0 * (k + 0.5) / n
    rxy = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    golden = math.pi * (3.0 - math.sqrt(5.0))
    phi = golden * k
    out = np.column_stack(
        [
            rxy * np.cos(phi),
            rxy * np.sin(phi),
            z,
        ]
    )
    out /= np.linalg.norm(out, axis=1)[:, None]
    return out


def build_cases(
    base_direction: np.ndarray,
    center_radius: float,
    payload_radius: float,
) -> list[PayloadCase]:
    cases: list[PayloadCase] = [
        PayloadCase(
            "O00_BASE",
            "ORIENTATION",
            unit(base_direction),
            center_radius,
            payload_radius,
            True,
        )
    ]

    for i, direction in enumerate(
        fibonacci_sphere(N_EXTRA_ORIENTATIONS),
        start=1,
    ):
        cases.append(
            PayloadCase(
                f"O{i:02d}_FIB",
                "ORIENTATION",
                unit(direction),
                center_radius,
                payload_radius,
                True,
            )
        )

    for mult in (0.8, 1.2):
        cases.append(
            PayloadCase(
                f"DIST_X{mult:.2f}",
                "GEOMETRY_DISTANCE",
                unit(base_direction),
                center_radius * mult,
                payload_radius,
                True,
            )
        )

    for mult in (0.5, 2.0):
        cases.append(
            PayloadCase(
                f"RADIUS_X{mult:.2f}",
                "GEOMETRY_RADIUS",
                unit(base_direction),
                center_radius,
                payload_radius * mult,
                True,
            )
        )

    for mult in BLIND_WILDCARD_RADIUS_MULTIPLIERS:
        cases.append(
            PayloadCase(
                f"WILDCARD_RADIUS_X{mult:.3f}",
                "BLIND_WILDCARD_DIAGNOSTIC",
                unit(base_direction),
                center_radius,
                payload_radius * mult,
                False,
            )
        )

    return cases


def concentration_metrics(
    energy: np.ndarray,
    outward: np.ndarray,
) -> dict[str, Any]:
    energy = np.maximum(np.asarray(energy, dtype=float), 0.0)
    outward = np.maximum(np.asarray(outward, dtype=float), 0.0)

    E = float(np.sum(energy))
    Aplus = float(np.sum(outward))

    leverage = np.zeros_like(energy)
    good = energy > max(float(np.max(energy)), 1.0) * 1.0e-15
    leverage[good] = outward[good] / energy[good]

    order = np.argsort(leverage)[::-1]

    cum_e = np.cumsum(energy[order]) / max(E, 1.0e-300)
    cum_o = np.cumsum(outward[order]) / max(Aplus, 1.0e-300)

    def fq(q: float) -> float:
        idx = int(np.searchsorted(cum_o, q, side="left"))
        idx = min(idx, len(order) - 1)
        return float(cum_e[idx])

    mean1 = float(
        np.sum(energy * leverage)
        / max(E, 1.0e-300)
    )
    mean2 = float(
        np.sum(energy * leverage * leverage)
        / max(E, 1.0e-300)
    )
    fpart = (
        mean1 * mean1 / mean2
        if mean2 > 0.0
        else float("nan")
    )

    idx50 = int(np.searchsorted(cum_o, 0.50, side="left"))
    idx50 = min(idx50, len(order) - 1)
    top50 = np.zeros(len(energy), dtype=bool)
    top50[order[: idx50 + 1]] = True

    return {
        "F25": fq(0.25),
        "F50": fq(0.50),
        "F75": fq(0.75),
        "F90": fq(0.90),
        "F99": fq(0.99),
        "f_part": float(fpart),
        "top50_mask": top50,
        "leverage": leverage,
    }


def weighted_jaccard(
    a: np.ndarray,
    b: np.ndarray,
    weights: np.ndarray,
) -> tuple[float, float]:
    inter = a & b
    union = a | b

    plain = (
        float(np.count_nonzero(inter))
        / max(float(np.count_nonzero(union)), 1.0)
    )

    w = np.maximum(np.asarray(weights, dtype=float), 0.0)
    weighted = (
        float(np.sum(w[inter]))
        / max(float(np.sum(w[union])), 1.0e-300)
    )

    return plain, weighted


def evaluate_points(
    int01,
    interp,
    points: np.ndarray,
):
    (
        _phi,
        _qx,
        _qy,
        _qz,
        e2,
        e4,
        potential,
        rho,
        active,
    ) = int01.independent_terms(
        interp,
        points,
    )
    return e2, e4, potential, rho, active


def integrate_block_for_case(
    int01,
    interp,
    lowers: np.ndarray,
    offsets: np.ndarray,
    weights: np.ndarray,
    case: PayloadCase,
):
    """Return per-cell force ledgers plus signed-sector totals."""
    nq = len(weights)
    ncell = len(lowers)

    net = np.zeros(ncell, dtype=float)
    outward = np.zeros(ncell, dtype=float)
    kernel_volume = np.zeros(ncell, dtype=float)

    sectors = np.zeros(4, dtype=float)
    # [S+K+, S+K-, S-K+, S-K-], all stored as positive magnitudes.
    e4_force = 0.0
    v_force = 0.0

    cells_per_batch = max(
        1,
        MAX_BATCH_POINTS // max(nq, 1),
    )

    center = case.center_radius * case.direction

    for start in range(0, ncell, cells_per_batch):
        stop = min(start + cells_per_batch, ncell)
        lo = lowers[start:stop]
        pts = (
            lo[:, None, :]
            + offsets[None, :, :]
        ).reshape(-1, 3)

        _e2, e4, potential, _rho, active = evaluate_points(
            int01,
            interp,
            pts,
        )

        kernel = int01.independent_kernel(
            pts,
            center,
            case.direction,
            case.payload_radius,
        )

        nc = len(lo)
        w = np.broadcast_to(
            weights[None, :],
            (nc, nq),
        )

        e4 = e4.reshape(nc, nq)
        potential = potential.reshape(nc, nq)
        active = active.reshape(nc, nq)
        kernel = kernel.reshape(nc, nq)

        influence = active * kernel

        net[start:stop] = np.sum(influence * w, axis=1)
        outward[start:stop] = np.sum(
            np.maximum(influence, 0.0) * w,
            axis=1,
        )
        kernel_volume[start:stop] = np.sum(kernel * w, axis=1)

        sp = np.maximum(active, 0.0)
        sn = np.maximum(-active, 0.0)
        kp = np.maximum(kernel, 0.0)
        kn = np.maximum(-kernel, 0.0)

        sectors[0] += float(np.sum(sp * kp * w))
        sectors[1] += float(np.sum(sp * kn * w))
        sectors[2] += float(np.sum(sn * kp * w))
        sectors[3] += float(np.sum(sn * kn * w))

        e4_force += float(np.sum(2.0 * e4 * kernel * w))
        v_force += float(np.sum(-2.0 * potential * kernel * w))

    return net, outward, kernel_volume, sectors, e4_force, v_force


def integrate_representation(
    tag: str,
    int01,
    c2aqs,
    interp,
    axis: np.ndarray,
    dx: float,
    cases: list[PayloadCase],
):
    """Integrate one continuous representation over all declared payload cases."""
    print(f"\n=== {tag.upper()} — GLOBAL Q4 FIELD / FORCE LEDGER ===", flush=True)

    all_lowers = c2aqs.cell_lowers(axis)
    ncell = len(all_lowers)
    all_indices = np.arange(ncell, dtype=int)

    q4_offsets, q4_weights = c2aqs.composite_gauss_offsets(
        dx,
        4,
        1,
    )

    nq = len(q4_weights)
    cells_per_batch = max(
        1,
        MAX_BATCH_POINTS // max(nq, 1),
    )

    e2_cell = np.zeros(ncell, dtype=float)
    e4_cell = np.zeros(ncell, dtype=float)
    v_cell = np.zeros(ncell, dtype=float)
    energy_cell = np.zeros(ncell, dtype=float)
    active_cell = np.zeros(ncell, dtype=float)

    ncase = len(cases)
    net_cell = np.zeros((ncase, ncell), dtype=float)
    outward_cell = np.zeros((ncase, ncell), dtype=float)

    sectors = np.zeros((ncase, 4), dtype=float)
    e4_force = np.zeros(ncase, dtype=float)
    v_force = np.zeros(ncase, dtype=float)

    # Only baseline needs a per-cell kernel ledger for shell covariance.
    baseline_kernel_cell = np.zeros(ncell, dtype=float)

    active_pos_budget = 0.0
    active_neg_budget = 0.0

    last_bucket = -1

    for start in range(0, ncell, cells_per_batch):
        stop = min(start + cells_per_batch, ncell)
        lo = all_lowers[start:stop]
        pts = (
            lo[:, None, :]
            + q4_offsets[None, :, :]
        ).reshape(-1, 3)

        e2, e4, potential, rho, active = evaluate_points(
            int01,
            interp,
            pts,
        )

        nc = len(lo)
        w = np.broadcast_to(
            q4_weights[None, :],
            (nc, nq),
        )

        e2r = e2.reshape(nc, nq)
        e4r = e4.reshape(nc, nq)
        vr = potential.reshape(nc, nq)
        rhor = rho.reshape(nc, nq)
        sr = active.reshape(nc, nq)

        e2_cell[start:stop] = np.sum(e2r * w, axis=1)
        e4_cell[start:stop] = np.sum(e4r * w, axis=1)
        v_cell[start:stop] = np.sum(vr * w, axis=1)
        energy_cell[start:stop] = np.sum(rhor * w, axis=1)
        active_cell[start:stop] = np.sum(sr * w, axis=1)

        active_pos_budget += float(np.sum(np.maximum(sr, 0.0) * w))
        active_neg_budget += float(np.sum(np.maximum(-sr, 0.0) * w))

        for icase, case in enumerate(cases):
            center = case.center_radius * case.direction

            kernel = int01.independent_kernel(
                pts,
                center,
                case.direction,
                case.payload_radius,
            ).reshape(nc, nq)

            influence = sr * kernel

            net_cell[icase, start:stop] = np.sum(
                influence * w,
                axis=1,
            )

            outward_cell[icase, start:stop] = np.sum(
                np.maximum(influence, 0.0) * w,
                axis=1,
            )

            sp = np.maximum(sr, 0.0)
            sn = np.maximum(-sr, 0.0)
            kp = np.maximum(kernel, 0.0)
            kn = np.maximum(-kernel, 0.0)

            sectors[icase, 0] += float(np.sum(sp * kp * w))
            sectors[icase, 1] += float(np.sum(sp * kn * w))
            sectors[icase, 2] += float(np.sum(sn * kp * w))
            sectors[icase, 3] += float(np.sum(sn * kn * w))

            e4_force[icase] += float(
                np.sum(2.0 * e4r * kernel * w)
            )
            v_force[icase] += float(
                np.sum(-2.0 * vr * kernel * w)
            )

            if icase == 0:
                baseline_kernel_cell[start:stop] = np.sum(
                    kernel * w,
                    axis=1,
                )

        pct = int(100 * stop / max(ncell, 1))
        bucket = pct // 10
        if bucket != last_bucket:
            print(
                f"{tag.upper()}_GLOBAL_Q4_PROGRESS="
                f"{stop}/{ncell} PERCENT={pct}",
                flush=True,
            )
            last_bucket = bucket

    # Replace near-field Q4 force contributions with the established fine
    # near cubature, separately for each payload case.
    near_offsets, near_weights = c2aqs.composite_gauss_offsets(
        dx,
        c2aqs.NEAR_GAUSS_ORDER,
        c2aqs.NEAR_FINE_SUBDIV,
    )

    print(f"\n=== {tag.upper()} — CASE-SPECIFIC NEAR-FIELD REPLACEMENT ===")

    for icase, case in enumerate(cases):
        center = case.center_radius * case.direction
        dmin = c2aqs.min_distance_to_cells(
            all_lowers,
            dx,
            center,
        )
        near_mask = dmin < c2aqs.NEAR_RADIUS_DX * dx
        ids = all_indices[near_mask]
        lowers = all_lowers[near_mask]

        old = integrate_block_for_case(
            int01,
            interp,
            lowers,
            q4_offsets,
            q4_weights,
            case,
        )
        new = integrate_block_for_case(
            int01,
            interp,
            lowers,
            near_offsets,
            near_weights,
            case,
        )

        old_net, old_out, old_k, old_sec, old_e4f, old_vf = old
        new_net, new_out, new_k, new_sec, new_e4f, new_vf = new

        net_cell[icase, ids] = new_net
        outward_cell[icase, ids] = new_out

        sectors[icase] += new_sec - old_sec
        e4_force[icase] += new_e4f - old_e4f
        v_force[icase] += new_vf - old_vf

        if icase == 0:
            baseline_kernel_cell[ids] = new_k

        print(
            f"{tag.upper()}_{case.label}_NEAR_CELLS={len(ids)}",
            flush=True,
        )

    E2 = float(np.sum(e2_cell))
    E4 = float(np.sum(e4_cell))
    V = float(np.sum(v_cell))
    E = float(np.sum(energy_cell))
    active_total = float(np.sum(active_cell))

    virial = E2 - E4 + 3.0 * V
    virial_rel = virial / max(E, 1.0e-300)
    active_over_energy = active_total / max(E, 1.0e-300)

    print(f"\n=== {tag.upper()} — CONTINUUM ENERGY / VIRIAL ===")
    print(f"{tag.upper()}_E={E:.15e}")
    print(f"{tag.upper()}_E2={E2:.15e}")
    print(f"{tag.upper()}_E4={E4:.15e}")
    print(f"{tag.upper()}_V={V:.15e}")
    print(f"{tag.upper()}_VIRIAL_RESIDUAL={virial:.15e}")
    print(f"{tag.upper()}_VIRIAL_RESIDUAL_OVER_E={virial_rel:.15e}")
    print(f"{tag.upper()}_ACTIVE_TOTAL={active_total:.15e}")
    print(f"{tag.upper()}_ACTIVE_TOTAL_OVER_E={active_over_energy:.15e}")
    print(f"{tag.upper()}_ACTIVE_POSITIVE_BUDGET_QPLUS={active_pos_budget:.15e}")
    print(f"{tag.upper()}_ACTIVE_NEGATIVE_BUDGET_QMINUS={active_neg_budget:.15e}")

    results: dict[str, Any] = {}
    top50_masks: dict[str, np.ndarray] = {}
    leverage_baseline = None

    for icase, case in enumerate(cases):
        net = float(np.sum(net_cell[icase]))
        outward = float(np.sum(outward_cell[icase]))
        opposing = float(np.sum(outward_cell[icase] - net_cell[icase]))
        l1 = outward + opposing
        cancellation = l1 / max(abs(net), 1.0e-300)

        conc = concentration_metrics(
            energy_cell,
            outward_cell[icase],
        )

        top50_masks[case.label] = conc["top50_mask"]
        if icase == 0:
            leverage_baseline = conc["leverage"]

        spkp, spkn, snkp, snkn = sectors[icase]
        sector_net = spkp + snkn - spkn - snkp
        sector_error = abs(sector_net - net)

        positive_active_force = spkp - spkn
        negative_active_force = snkn - snkp

        mean_k_splus = positive_active_force / max(
            active_pos_budget,
            1.0e-300,
        )
        # This is the actual force per unit magnitude of negative active source.
        mean_force_per_sminus = negative_active_force / max(
            active_neg_budget,
            1.0e-300,
        )

        term_cancel = (
            abs(e4_force[icase]) + abs(v_force[icase])
        ) / max(abs(net), 1.0e-300)

        eta_op = (
            case.center_radius**2
            * net
            / max(E, 1.0e-300)
        )

        result = {
            "label": case.label,
            "category": case.category,
            "promotion_relevant": case.promotion_relevant,
            "direction": [float(x) for x in case.direction],
            "center_radius": float(case.center_radius),
            "payload_radius": float(case.payload_radius),
            "net": net,
            "outward": outward,
            "opposing": opposing,
            "cancellation": cancellation,
            "F25": conc["F25"],
            "F50": conc["F50"],
            "F75": conc["F75"],
            "F90": conc["F90"],
            "F99": conc["F99"],
            "f_part": conc["f_part"],
            "eta_op": eta_op,
            "Splus_Kplus": float(spkp),
            "Splus_Kminus": float(spkn),
            "Sminus_Kplus": float(snkp),
            "Sminus_Kminus": float(snkn),
            "signed_sector_reconstruction_error": sector_error,
            "positive_active_net_force": float(positive_active_force),
            "negative_active_net_force": float(negative_active_force),
            "mean_force_per_Qplus": float(mean_k_splus),
            "mean_force_per_Qminus": float(mean_force_per_sminus),
            "e4_force": float(e4_force[icase]),
            "V_force": float(v_force[icase]),
            "e4_V_cancellation": float(term_cancel),
        }
        results[case.label] = result

        print(
            f"{tag.upper()}_CASE={case.label} "
            f"NET={net:.9e} "
            f"F50={conc['F50']:.9e} "
            f"F90={conc['F90']:.9e} "
            f"FPART={conc['f_part']:.9e} "
            f"CANCEL={cancellation:.9e} "
            f"SPKP={spkp:.9e} "
            f"SPKN={spkn:.9e} "
            f"SNKP={snkp:.9e} "
            f"SNKN={snkn:.9e}",
            flush=True,
        )

    # Baseline radial shell covariance:
    centers = all_lowers + 0.5 * dx
    radius = np.linalg.norm(centers, axis=1)
    edges = np.linspace(
        0.0,
        float(np.max(radius)) * (1.0 + 1.0e-12),
        RADIAL_BINS + 1,
    )
    bins = np.searchsorted(edges, radius, side="right") - 1
    bins = np.clip(bins, 0, RADIAL_BINS - 1)

    cell_volume = dx**3
    shell_rows = []
    radialized_force = 0.0
    covariance_force = 0.0

    for ib in range(RADIAL_BINS):
        ids = np.flatnonzero(bins == ib)
        if len(ids) == 0:
            shell_rows.append(
                [
                    ib,
                    0.5 * (edges[ib] + edges[ib + 1]),
                    0.0, 0.0, 0.0, 0.0, 0.0,
                ]
            )
            continue

        vol = len(ids) * cell_volume
        intS = float(np.sum(active_cell[ids]))
        intK = float(np.sum(baseline_kernel_cell[ids]))
        intSK = float(np.sum(net_cell[0, ids]))

        radial_part = intS * intK / max(vol, 1.0e-300)
        cov_part = intSK - radial_part

        radialized_force += radial_part
        covariance_force += cov_part

        shell_rows.append(
            [
                ib,
                0.5 * (edges[ib] + edges[ib + 1]),
                intS,
                intK,
                intSK,
                radial_part,
                cov_part,
            ]
        )

    cov_path = DATA / f"int02_baseline_shell_covariance_{tag}.csv"
    with cov_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "bin",
                "radius_mid",
                "int_S",
                "int_K",
                "int_SK",
                "radialized_force",
                "covariance_force",
            ]
        )
        writer.writerows(shell_rows)

    baseline_net = results["O00_BASE"]["net"]

    print(f"{tag.upper()}_BASELINE_RADIALIZED_FORCE={radialized_force:.15e}")
    print(f"{tag.upper()}_BASELINE_ANGULAR_COVARIANCE_FORCE={covariance_force:.15e}")
    print(
        f"{tag.upper()}_BASELINE_RADIALIZED_PLUS_COV_MINUS_DIRECT="
        f"{radialized_force + covariance_force - baseline_net:.15e}"
    )

    return {
        "tag": tag,
        "E": E,
        "E2": E2,
        "E4": E4,
        "V": V,
        "virial": virial,
        "virial_rel": virial_rel,
        "active_total": active_total,
        "active_over_energy": active_over_energy,
        "Qplus": active_pos_budget,
        "Qminus": active_neg_budget,
        "energy_cell": energy_cell,
        "top50_masks": top50_masks,
        "leverage_baseline": leverage_baseline,
        "cases": results,
        "radialized_force": radialized_force,
        "covariance_force": covariance_force,
    }


def exact_map_weighted_source(
    b23,
    profile,
    b_parameter: float,
    n_r: int = 68,
    n_mu: int = 32,
    n_phi: int = 64,
):
    """Build independent exact-map energy/active quadrature weights."""
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
    phi = (
        (np.arange(n_phi) + 0.5)
        * 2.0 * math.pi
        / n_phi
    )
    dphi = 2.0 * math.pi / n_phi

    J = b23.b7_angular_j(mu, phi, b_parameter)

    F_interp = PchipInterpolator(
        profile.r,
        profile.F,
        extrapolate=False,
    )
    Fp_interp = PchipInterpolator(
        profile.r,
        profile.Fp,
        extrapolate=False,
    )

    F = F_interp(r)
    Fp = Fp_interp(r)

    sin_theta = np.sqrt(1.0 - mu * mu)
    Xhat = sin_theta[:, None] * np.cos(phi)[None, :]
    Yhat = sin_theta[:, None] * np.sin(phi)[None, :]
    Zhat = mu[:, None] * np.ones((1, n_phi))

    w_ang = (
        wmu[:, None]
        * np.ones((1, n_phi))
        * dphi
    )

    xyz_parts = []
    energy_parts = []
    active_parts = []
    e4_parts = []
    v_parts = []

    for ir, radius in enumerate(r):
        s2 = math.sin(float(F[ir])) ** 2
        a = float(Fp[ir] ** 2)

        bang = s2 * J**2 / (radius * radius)

        e2 = a + 2.0 * bang
        e4 = 2.0 * a * bang + bang**2

        V = (
            profile.m**2
            * (1.0 - math.cos(float(F[ir])))
            * (1.0 + profile.eta * math.cos(float(F[ir])))
        )

        rho = e2 + e4 + V
        active = 2.0 * (e4 - V)

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
        e4_parts.append((volume_w * 2.0 * e4).ravel())
        v_parts.append((volume_w * -2.0 * V).ravel())

    return (
        np.concatenate(xyz_parts, axis=0),
        np.concatenate(energy_parts),
        np.concatenate(active_parts),
        np.concatenate(e4_parts),
        np.concatenate(v_parts),
    )


def exact_map_case_metrics(
    xyz: np.ndarray,
    energy_w: np.ndarray,
    active_w: np.ndarray,
    e4_w: np.ndarray,
    v_w: np.ndarray,
    direction: np.ndarray,
    center_radius: float,
    payload_radius: float,
):
    center = center_radius * direction
    q = xyz - center[None, :]
    d2 = np.sum(q * q, axis=1)
    d = np.sqrt(np.maximum(d2, 0.0))
    denom = np.where(
        d < payload_radius,
        payload_radius**3,
        np.maximum(d2 * d, 1.0e-300),
    )
    kernel = (q @ direction) / denom

    influence = active_w * kernel
    outward = np.maximum(influence, 0.0)
    opposing = np.maximum(-influence, 0.0)

    net = float(np.sum(influence))
    Aplus = float(np.sum(outward))
    Aminus = float(np.sum(opposing))
    cancellation = (
        Aplus + Aminus
    ) / max(abs(net), 1.0e-300)

    conc = concentration_metrics(
        energy_w,
        outward,
    )

    sp = np.maximum(active_w, 0.0)
    sn = np.maximum(-active_w, 0.0)
    kp = np.maximum(kernel, 0.0)
    kn = np.maximum(-kernel, 0.0)

    # active_w already includes positive quadrature volume, so these are
    # correctly integrated source/kernel channel contributions.
    spkp = float(np.sum(sp * kp))
    spkn = float(np.sum(sp * kn))
    snkp = float(np.sum(sn * kp))
    snkn = float(np.sum(sn * kn))

    e4_force = float(np.sum(e4_w * kernel))
    v_force = float(np.sum(v_w * kernel))

    return {
        "net": net,
        "outward": Aplus,
        "opposing": Aminus,
        "cancellation": cancellation,
        "F25": conc["F25"],
        "F50": conc["F50"],
        "F75": conc["F75"],
        "F90": conc["F90"],
        "F99": conc["F99"],
        "f_part": conc["f_part"],
        "Splus_Kplus": spkp,
        "Splus_Kminus": spkn,
        "Sminus_Kplus": snkp,
        "Sminus_Kminus": snkn,
        "e4_force": e4_force,
        "V_force": v_force,
        "e4_V_cancellation": (
            abs(e4_force) + abs(v_force)
        ) / max(abs(net), 1.0e-300),
    }


def summarize_range(values: list[float]) -> dict[str, float]:
    x = np.asarray(values, dtype=float)
    return {
        "min": float(np.min(x)),
        "median": float(np.median(x)),
        "max": float(np.max(x)),
    }


def main() -> None:
    print(
        "=== INT-02/05R — SIGNED KERNEL + ORIENTATION ROBUSTNESS ===",
        flush=True,
    )

    require(INT01_SOURCE)
    require(INT01_SUMMARY)

    int01_summary = json.loads(
        INT01_SUMMARY.read_text()
    )
    if not bool(int01_summary.get("attribution_both")):
        raise RuntimeError(
            "INT-01 attribution did not close; INT-02/05R is not authorized"
        )

    int01 = load_module(
        "int02_int01",
        INT01_SOURCE,
    )

    require(int01.C2AQS_SOURCE)
    if int01.sha256(int01.C2AQS_SOURCE) != int01.EXPECTED_C2AQS_SHA256:
        raise RuntimeError("023C2AQS hash audit failed through INT-01")

    c2aqs = load_module(
        "int02_c2aqs",
        int01.C2AQS_SOURCE,
    )
    aqr = load_module(
        "int02_aqr",
        c2aqs.AQR_SOURCE,
    )

    if int01.sha256(c2aqs.AQR_SOURCE) != c2aqs.EXPECTED_AQR_SHA256:
        raise RuntimeError("023C2AQR hash audit failed")

    aqr.validate_analytic_formulae()

    c2aq = aqr.load_module(
        "int02_c2aq",
        aqr.C2AQ_SOURCE,
    )
    cr3 = c2aq.load_module(
        "int02_cr3",
        c2aq.CR3_SOURCE,
    )

    phi, axis, dx = c2aqs.load_n65()

    Edisc, E2disc, E4disc, Vdisc, grad = cr3.riemannian_gradient_density(
        phi,
        dx,
    )
    grad_rms, grad_max = cr3.gradient_norms(grad)
    topology4 = cr3.topology4(phi, dx)

    print("\n=== A — STRICT N65 AUDIT ===")
    print(f"N65_GRAD_RMS={grad_rms:.15e}")
    print(f"N65_GRAD_MAX={grad_max:.15e}")
    print(f"N65_TOPOLOGY4={topology4:.15e}")
    print(f"N65_DISCRETE_E={Edisc:.15e}")
    print(f"N65_DISCRETE_E2={E2disc:.15e}")
    print(f"N65_DISCRETE_E4={E4disc:.15e}")
    print(f"N65_DISCRETE_V={Vdisc:.15e}")

    discrete_virial = E2disc - E4disc + 3.0 * Vdisc
    print(f"N65_DISCRETE_VIRIAL_RESIDUAL={discrete_virial:.15e}")
    print(
        f"N65_DISCRETE_VIRIAL_RESIDUAL_OVER_E="
        f"{discrete_virial/max(Edisc,1.0e-300):.15e}"
    )

    if grad_rms > int01.GRAD_RMS_TOL or grad_max > int01.GRAD_MAX_TOL:
        raise RuntimeError("N65 strict stationarity no longer passes")

    if abs(abs(topology4) / B - 1.0) > 3.0e-2:
        raise RuntimeError("N65 topology audit failed")

    base_direction = unit(
        np.asarray(c2aq.KNOWN_WORST_DIRECTION, dtype=float)
    )
    center_radius = float(c2aq.PAYLOAD_CENTER)
    payload_radius = float(c2aq.PAYLOAD_RADIUS)

    cases = build_cases(
        base_direction,
        center_radius,
        payload_radius,
    )

    print("\n=== B — PAYLOAD CASES ===")
    print(f"PAYLOAD_CASE_COUNT={len(cases)}")
    print(f"NOMINAL_ORIENTATION_COUNT={1 + N_EXTRA_ORIENTATIONS}")
    for case in cases:
        print(
            f"CASE={case.label} CATEGORY={case.category} "
            f"CENTER={case.center_radius:.9e} "
            f"RADIUS={case.payload_radius:.9e} "
            f"PROMOTION_RELEVANT={'YES' if case.promotion_relevant else 'NO'}"
        )

    print("\n=== C — BUILD CONTINUOUS REPRESENTATIONS ===")
    cubic = c2aqs.build_interpolator(axis, phi, "cubic")
    print("CUBIC_INTERPOLATOR=READY", flush=True)
    quintic = c2aqs.build_interpolator(axis, phi, "quintic")
    print("QUINTIC_INTERPOLATOR=READY", flush=True)

    cubic_result = integrate_representation(
        "cubic",
        int01,
        c2aqs,
        cubic,
        axis,
        dx,
        cases,
    )

    quintic_result = integrate_representation(
        "quintic",
        int01,
        c2aqs,
        quintic,
        axis,
        dx,
        cases,
    )

    print("\n=== D — CUBIC / QUINTIC HOTSPOT OVERLAP ===")

    avg_energy = 0.5 * (
        cubic_result["energy_cell"]
        + quintic_result["energy_cell"]
    )

    overlap: dict[str, dict[str, float]] = {}

    for case in cases:
        cm = cubic_result["top50_masks"][case.label]
        qm = quintic_result["top50_masks"][case.label]

        plain, weighted = weighted_jaccard(
            cm,
            qm,
            avg_energy,
        )

        overlap[case.label] = {
            "jaccard": plain,
            "energy_weighted_jaccard": weighted,
        }

        print(
            f"HOTSPOT_OVERLAP_CASE={case.label} "
            f"JACCARD={plain:.9e} "
            f"ENERGY_WEIGHTED_JACCARD={weighted:.9e}"
        )

    cbase = cubic_result["leverage_baseline"]
    qbase = quintic_result["leverage_baseline"]

    nonvac = avg_energy > max(float(np.max(avg_energy)), 1.0) * 1.0e-14
    if int(np.count_nonzero(nonvac)) >= 10:
        ranks_c = np.argsort(np.argsort(cbase[nonvac]))
        ranks_q = np.argsort(np.argsort(qbase[nonvac]))
        baseline_rank_corr = float(
            np.corrcoef(ranks_c, ranks_q)[0, 1]
        )
    else:
        baseline_rank_corr = float("nan")

    print(
        f"BASELINE_CUBIC_QUINTIC_LEVERAGE_RANK_CORRELATION="
        f"{baseline_rank_corr:.15e}"
    )

    print("\n=== E — EXACT B7 RATIONAL-MAP COMPARATOR ===")

    require(aqr.C2AQ_SOURCE)
    # Load canonical 023A/023B directly from the audited chain.
    b23_path = ROOT / "simulations/023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.py"
    a23_path = ROOT / "simulations/023a_topological_false_core_multiskyrmion_gr_repulsion_gate.py"
    require(a23_path)
    require(b23_path)

    a23 = load_module("int02_a23", a23_path)
    b23 = load_module("int02_b23", b23_path)

    degree, I_direct = b23.angular_integrals_b7(b23.B7_B0)
    profile = b23.solve_profile_with_custom_I(
        a23,
        B,
        ETA,
        MASS,
        I_direct,
    )

    sector_profiles, sector_energies = b23.solve_exact_sector(
        a23,
        ETA,
        MASS,
    )
    selected = b23.candidate_from_sector(
        a23,
        sector_profiles,
        sector_energies,
        B,
    )

    exact_center = float(selected.payload.payload_center)
    exact_radius = float(selected.payload.payload_radius)

    xyz, energy_w, active_w, e4_w, v_w = exact_map_weighted_source(
        b23,
        profile,
        b23.B7_B0,
        68,
        32,
        64,
    )

    exact_E = float(np.sum(energy_w))
    exact_active = float(np.sum(active_w))
    exact_virial = (
        4.0 * math.pi
        * (
            float(profile.E2)
            - float(profile.E4)
            + 3.0 * float(profile.E0)
        )
    )
    exact_virial_rel = exact_virial / max(
        4.0 * math.pi * float(profile.E),
        1.0e-300,
    )

    print(f"EXACT_MAP_DEGREE={degree:.15e}")
    print(f"EXACT_MAP_I={I_direct:.15e}")
    print(f"EXACT_MAP_SOURCE_NODES={len(xyz)}")
    print(f"EXACT_MAP_E={exact_E:.15e}")
    print(f"EXACT_MAP_ACTIVE_TOTAL={exact_active:.15e}")
    print(f"EXACT_MAP_ACTIVE_OVER_E={exact_active/max(exact_E,1e-300):.15e}")
    print(f"EXACT_MAP_VIRIAL_RESIDUAL_OVER_E={exact_virial_rel:.15e}")
    print(f"EXACT_MAP_PAYLOAD_CENTER={exact_center:.15e}")
    print(f"EXACT_MAP_PAYLOAD_RADIUS={exact_radius:.15e}")

    exact_cases: dict[str, Any] = {}
    nominal_orientation_cases = [
        case
        for case in cases
        if case.category == "ORIENTATION"
    ]

    for case in nominal_orientation_cases:
        m = exact_map_case_metrics(
            xyz,
            energy_w,
            active_w,
            e4_w,
            v_w,
            case.direction,
            exact_center,
            exact_radius,
        )
        exact_cases[case.label] = m
        print(
            f"EXACT_MAP_CASE={case.label} "
            f"NET={m['net']:.9e} "
            f"F50={m['F50']:.9e} "
            f"F90={m['F90']:.9e} "
            f"FPART={m['f_part']:.9e} "
            f"CANCEL={m['cancellation']:.9e}"
        )

    print("\n=== F — ROBUSTNESS SUMMARY ===")

    orient_labels = [
        case.label
        for case in nominal_orientation_cases
    ]

    def vals(rep, key):
        return [
            float(rep["cases"][label][key])
            for label in orient_labels
        ]

    summaries = {
        "cubic_F50": summarize_range(vals(cubic_result, "F50")),
        "quintic_F50": summarize_range(vals(quintic_result, "F50")),
        "exact_F50": summarize_range(
            [float(exact_cases[label]["F50"]) for label in orient_labels]
        ),
        "cubic_F90": summarize_range(vals(cubic_result, "F90")),
        "quintic_F90": summarize_range(vals(quintic_result, "F90")),
        "exact_F90": summarize_range(
            [float(exact_cases[label]["F90"]) for label in orient_labels]
        ),
        "cubic_cancellation": summarize_range(
            vals(cubic_result, "cancellation")
        ),
        "quintic_cancellation": summarize_range(
            vals(quintic_result, "cancellation")
        ),
        "exact_cancellation": summarize_range(
            [float(exact_cases[label]["cancellation"]) for label in orient_labels]
        ),
        "hotspot_weighted_jaccard": summarize_range(
            [
                float(overlap[label]["energy_weighted_jaccard"])
                for label in orient_labels
            ]
        ),
    }

    for name, value in summaries.items():
        print(
            f"{name.upper()}_MIN={value['min']:.15e} "
            f"MEDIAN={value['median']:.15e} "
            f"MAX={value['max']:.15e}"
        )

    cubic_all_strong = (
        summaries["cubic_F50"]["max"]
        <= STRONG_F50_MAX
    )
    quintic_all_strong = (
        summaries["quintic_F50"]["max"]
        <= STRONG_F50_MAX
    )
    exact_all_strong = (
        summaries["exact_F50"]["max"]
        <= STRONG_F50_MAX
    )

    overlap_pass = (
        summaries["hotspot_weighted_jaccard"]["min"]
        >= TOP50_WEIGHTED_JACCARD_MIN
    )

    virial_warning = (
        abs(cubic_result["virial_rel"]) > VIRIAL_WARNING_REL
        or abs(quintic_result["virial_rel"]) > VIRIAL_WARNING_REL
    )

    # Check the qualitative signed-source mechanism: which of the two outward
    # channels dominates each nominal orientation?
    def dominant_outward_channel(rep, label):
        m = rep["cases"][label]
        if m["Splus_Kplus"] >= m["Sminus_Kminus"]:
            return "SPLUS_KPLUS"
        return "SMINUS_KMINUS"

    signed_agreement = True
    for label in orient_labels:
        if dominant_outward_channel(cubic_result, label) != dominant_outward_channel(
            quintic_result,
            label,
        ):
            signed_agreement = False
            break

    if (
        cubic_all_strong
        and quintic_all_strong
        and exact_all_strong
        and overlap_pass
        and signed_agreement
    ):
        if virial_warning:
            decision = (
                "ROBUST_MECHANISM_SIGNAL_WITH_CONTINUUM_VIRIAL_WARNING"
            )
            next_action = (
                "INT03_04_GEOMETRY_ZERO_SURFACE_AND_CONSERVATION_AWARE_"
                "HEADROOM_BOUND_BEFORE_SOURCE_REDESIGN"
            )
        else:
            decision = (
                "ROBUST_MECHANISM_SIGNAL_ACROSS_ORIENTATION_AND_REPRESENTATION"
            )
            next_action = (
                "INT03_04_GEOMETRY_ZERO_SURFACE_THEN_INT11_FIELD_SPACE_"
                "SENSITIVITY_WHEN_HESSIAN_INFRASTRUCTURE_IS_READY"
            )
    elif not (cubic_all_strong and quintic_all_strong):
        decision = (
            "PRODUCTIVE_SKELETON_NOT_ORIENTATION_ROBUST_ON_N65"
        )
        next_action = (
            "STOP_HOTSPOT_PROMOTION_AND_CHARACTERIZE_ORIENTATION_FAILURE"
        )
    elif not overlap_pass:
        decision = (
            "SCALAR_CONCENTRATION_SURVIVES_BUT_HOTSPOT_GEOMETRY_IS_"
            "REPRESENTATION_SENSITIVE"
        )
        next_action = (
            "REQUIRE_FINE_GRID_OR_EXACT_MAP_GEOMETRY_BEFORE_INTERPRETATION"
        )
    elif not exact_all_strong:
        decision = (
            "N65_CONCENTRATION_NOT_REPRODUCED_BY_EXACT_MAP_COMPARATOR"
        )
        next_action = (
            "LOCATE_RELAXATION_INDUCED_MECHANISM_CHANGE_BEFORE_HEADROOM_CLAIM"
        )
    else:
        decision = "SIGNED_SOURCE_KERNEL_MECHANISM_REPRESENTATION_SENSITIVE"
        next_action = "INT05_SIGNED_SOURCE_KERNEL_ANATOMY_REPAIR"

    print(f"ORIENTATION_CUBIC_ALL_F50_LE_0P10={'PASS' if cubic_all_strong else 'FAIL'}")
    print(f"ORIENTATION_QUINTIC_ALL_F50_LE_0P10={'PASS' if quintic_all_strong else 'FAIL'}")
    print(f"EXACT_MAP_ALL_F50_LE_0P10={'PASS' if exact_all_strong else 'FAIL'}")
    print(f"TOP50_HOTSPOT_WEIGHTED_JACCARD_MIN_GE_0P50={'PASS' if overlap_pass else 'FAIL'}")
    print(f"SIGNED_SOURCE_KERNEL_DOMINANT_CHANNEL_AGREEMENT={'PASS' if signed_agreement else 'FAIL'}")
    print(f"N65_CONTINUUM_VIRIAL_WARNING={'YES' if virial_warning else 'NO'}")

    print("\n=== G — INTROSPECTIVE DECISION ===")
    print(f"INT02_05R_DECISION={decision}")
    print(
        "INT_LEVEL_1="
        "N65_ACCOUNTING_AND_MECHANISM_DECOMPOSITION_CLOSED_"
        "BUT_FULLY_INDEPENDENT_N65_FORCE_SOLVER_STILL_PARTIAL"
    )
    print(
        "INT_LEVEL_2="
        "NOT_YET_REQUIRES_STRICT_FINE_RESOLUTION_OR_EQUIVALENT_"
        "UNRESTRICTED_SUPPORT"
    )
    print(
        "INT_LEVEL_3="
        "NOT_YET_NO_PHYSICALLY_ACCESSIBLE_10X_BOUND_OR_CONTINUABLE_DIRECTION"
    )
    print(
        "COUNTERFACTUAL_RADIALIZATION_PHYSICAL_CONFIGURATION="
        "NO_DIAGNOSTIC_ONLY"
    )
    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )
    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "APPROXIMATELY_70_TO_71_PERCENT_NOT_A_PROBABILITY"
    )
    print(f"NEXT={next_action}")
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_INT02_05R_SIGNED_KERNEL_ORIENTATION_ROBUSTNESS"
    )

    # Save compact machine-readable outputs.
    rows = []
    for rep_name, rep in (
        ("cubic", cubic_result),
        ("quintic", quintic_result),
    ):
        for case in cases:
            m = rep["cases"][case.label]
            rows.append(
                {
                    "representation": rep_name,
                    **m,
                    "hotspot_jaccard": overlap[case.label]["jaccard"],
                    "hotspot_energy_weighted_jaccard": (
                        overlap[case.label]["energy_weighted_jaccard"]
                    ),
                }
            )

    with OUT_CSV.open("w", newline="") as f:
        fieldnames = [
            "representation",
            "label",
            "category",
            "promotion_relevant",
            "direction",
            "center_radius",
            "payload_radius",
            "net",
            "outward",
            "opposing",
            "cancellation",
            "F25",
            "F50",
            "F75",
            "F90",
            "F99",
            "f_part",
            "eta_op",
            "Splus_Kplus",
            "Splus_Kminus",
            "Sminus_Kplus",
            "Sminus_Kminus",
            "signed_sector_reconstruction_error",
            "positive_active_net_force",
            "negative_active_net_force",
            "mean_force_per_Qplus",
            "mean_force_per_Qminus",
            "e4_force",
            "V_force",
            "e4_V_cancellation",
            "hotspot_jaccard",
            "hotspot_energy_weighted_jaccard",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    def strip_rep(rep):
        return {
            "E": rep["E"],
            "E2": rep["E2"],
            "E4": rep["E4"],
            "V": rep["V"],
            "virial": rep["virial"],
            "virial_rel": rep["virial_rel"],
            "active_total": rep["active_total"],
            "active_over_energy": rep["active_over_energy"],
            "Qplus": rep["Qplus"],
            "Qminus": rep["Qminus"],
            "radialized_force": rep["radialized_force"],
            "covariance_force": rep["covariance_force"],
            "cases": rep["cases"],
        }

    summary = {
        "claim_classification": (
            "PROJECT_DERIVED_INT02_05R_SIGNED_KERNEL_ORIENTATION_ROBUSTNESS"
        ),
        "decision": decision,
        "next": next_action,
        "thresholds": {
            "strong_F50_max": STRONG_F50_MAX,
            "top50_weighted_jaccard_min": TOP50_WEIGHTED_JACCARD_MIN,
            "virial_warning_abs_rel": VIRIAL_WARNING_REL,
        },
        "cubic": strip_rep(cubic_result),
        "quintic": strip_rep(quintic_result),
        "hotspot_overlap": overlap,
        "baseline_leverage_rank_correlation": baseline_rank_corr,
        "exact_map": {
            "degree": degree,
            "I": I_direct,
            "E": exact_E,
            "active_total": exact_active,
            "virial_rel": exact_virial_rel,
            "payload_center": exact_center,
            "payload_radius": exact_radius,
            "cases": exact_cases,
        },
        "orientation_summaries": summaries,
        "gates": {
            "cubic_all_strong": cubic_all_strong,
            "quintic_all_strong": quintic_all_strong,
            "exact_all_strong": exact_all_strong,
            "hotspot_overlap_pass": overlap_pass,
            "signed_mechanism_agreement": signed_agreement,
            "continuum_virial_warning": virial_warning,
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

    print(f"INT02_05R_SUMMARY_JSON={OUT_JSON}")
    print(f"INT02_05R_ORIENTATION_CSV={OUT_CSV}")
    print("INT02_05R_RUN_COMPLETE=YES")


if __name__ == "__main__":
    main()
