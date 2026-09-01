#!/usr/bin/env python3
"""INT-01 — certified fixed-field influence tomography.

PURPOSE
-------
Perform the highest-information first experiment in the ANTIGRAVITY_RESEARCH
INTROSPECTIVE branch.

The run asks whether useful finite-payload outward gravitational influence in
the strict-stationary unrestricted N=65 B=7 false-core Skyrmion is:

1. concentrated in a small fraction of the source energy;
2. broadly distributed;
3. dominated by cancellation between much larger opposing contributions;
4. mainly radial/geometric rather than dependent on detailed angular structure;
5. robust to cubic-vs-quintic continuous-field reconstruction.

SCIENTIFIC QUESTION
-------------------
Does a small subset of the complete positive-energy field perform a
disproportionately large fraction of the useful outward gravitational work?

PRIMARY OBSERVABLE
------------------
For finite payload kernel K_P,

    I_P(x) = S(x) K_P(x)

and

    A_P = integral I_P(x) d^3x.

For the selected static Skyrme model,

    rho = e2 + e4 + V

and

    S = rho + p1 + p2 + p3
      = 2(e4 - V).

Thus e2 contributes no direct static active source, although it may remain
essential for topology, equilibrium, and stability.

INFLUENCE DECOMPOSITION
-----------------------
Define

    I+ = max(I_P, 0)
    I- = max(-I_P, 0)

so

    A+ = integral I+ d^3x
    A- = integral I- d^3x
    A_P = A+ - A-.

The cancellation factor is

    C = (A+ + A-) / |A_P|.

ENERGY-NORMALIZED LEVERAGE
--------------------------
For source energy E and cell leverage ell+,

    ell+ = I+ / E_cell.

The energy-participation fraction is

    f_part =
        <ell+>_E^2
        /
        <ell+^2>_E.

Concentration outputs include F25, F50, F75, F90, and F99, where F50 is the
minimum fraction of total source energy required to produce 50 percent of gross
outward influence.

PREDECLARED INTERPRETATION
--------------------------
Strong concentration:

    F50 <= 0.10

Very strong concentration:

    F50 <= 0.05

Extreme concentration:

    F50 <= 0.01

Strong evidence against a small productive skeleton:

    F50 >= 0.35
    and
    f_part >= 0.50.

These are diagnostic criteria, not fundamental physical constants.

CHEAPEST DECISIVE TEST
----------------------
The field is NEVER modified.

The strict N=65 artifact is reconstructed continuously with independent cubic
and quintic tensor-product splines. The normalized field derivatives are
evaluated analytically.

The finite-payload force is independently reconstructed from those derivatives
and compared against the already validated 023C2AQS continuous-force log before
any hotspot/mechanism interpretation is accepted.

NUMERICAL STRATEGY
------------------
The integration uses the same declared finite-payload geometry and the same
high-accuracy cell partition as 023C2AQS:

- global Gauss-Legendre order 4 away from the payload;
- heavily subdivided order-4 integration close to the payload;
- cubic continuous field;
- quintic continuous field.

However, the local field terms, source decomposition, influence decomposition,
kernel multiplication, concentration statistics, and source-shuffle diagnostics
are independently assembled in this file.

VALIDATION
----------
The run fails closed on:

- known 023C2AQS source hash;
- analytic payload-kernel validation;
- strict N=65 S^3 artifact audit;
- strict N=65 Euler-Lagrange residual thresholds;
- constant-source cubature validation;
- failure of the independent influence sum to reconstruct the corresponding
  previously logged continuous force.

Only after attribution closure may concentration/hotspot diagnostics be
interpreted.

FIXED-FIELD SURROGATES
----------------------
The run additionally performs diagnostic, NONPHYSICAL source rearrangements:

- radialized active source;
- angular shuffle within radial shells;
- sign-preserving angular shuffle within radial shells.

These answer whether radial source placement and source-kernel correlation are
important.

They are NOT new field configurations and must never be promoted as realizable
Skyrmions.

PROMOTION / FALSIFICATION
-------------------------
A promising INT-01 diagnostic result requires:

- attribution closure in cubic and quintic reconstructions;
- qualitatively consistent concentration classifications;
- preferably F50 <= 0.10 in both reconstructions.

A strong negative productive-skeleton result is:

- attribution closes;
- both reconstructions give F50 >= 0.35;
- both give f_part >= 0.50.

If cubic and quintic give qualitatively incompatible anatomy, the correct result
is representation-sensitive and N=73/finer resolution is needed before
mechanistic interpretation.

OUTPUTS
-------
results/data/int01_certified_fixed_field_influence_tomography.npz
results/data/int01_certified_fixed_field_influence_tomography_summary.json
results/data/int01_cubic_concentration_curve.csv
results/data/int01_quintic_concentration_curve.csv
results/data/int01_cubic_radial_bins.csv
results/data/int01_quintic_radial_bins.csv

The caller should preserve stdout in a timestamped run log.

APPROXIMATION LEVEL
-------------------
Static flat-spacetime Skyrme matter with a linearized-GR finite-payload
operational readout.

This run does NOT establish:

- continuum-resolution force convergence;
- full physical Hessian stability;
- fission stability;
- nonlinear Einstein-Skyrme consistency;
- practical energy scaling;
- a real material;
- an experiment;
- a practical antigravity device;
- new physics.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_INT01_CERTIFIED_FIXED_FIELD_INFLUENCE_TOMOGRAPHY
"""

from __future__ import annotations

from dataclasses import dataclass, fields
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import sys

import numpy as np
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"
LOGS = ROOT / "results/logs"

C2AQS_SOURCE = SIM / "023c2aqs_continuous_field_active_source_force_integration.py"
EXPECTED_C2AQS_SHA256 = (
    "e6d6131d7b26c1a140f1b214cec8f73d129d4288be4960cace124fc3a8250434"
)

N65_ARTIFACT = DATA / "023cr4r_strict_stationary_b7_n65.npz"
N65_FORCE_LOG = LOGS / "023c2aqs_continuous_field_active_source_force_integration.log"

OUT_NPZ = DATA / "int01_certified_fixed_field_influence_tomography.npz"
OUT_JSON = DATA / "int01_certified_fixed_field_influence_tomography_summary.json"

B = 7
ETA = 0.40
MASS = 8.0

GRAD_RMS_TOL = 1.5e-3
GRAD_MAX_TOL = 5.0e-2

RADIAL_BINS = max(24, int(os.environ.get("AG_INT01_RADIAL_BINS", "96")))
SHUFFLES = max(4, int(os.environ.get("AG_INT01_SHUFFLES", "32")))
MAX_BATCH_POINTS = max(
    20000,
    int(os.environ.get("AG_INT01_BATCH_POINTS", "120000")),
)

ENERGY_FLOOR_REL = float(os.environ.get("AG_INT01_ENERGY_FLOOR_REL", "1e-12"))
ATTRIBUTION_L1_TOL = float(
    os.environ.get("AG_INT01_ATTRIBUTION_L1_TOL", "1e-9")
)

RNG_SEED = 20260901


@dataclass
class CellLedger:
    e2: np.ndarray
    e4: np.ndarray
    potential: np.ndarray
    energy: np.ndarray
    active: np.ndarray
    influence: np.ndarray
    outward: np.ndarray
    opposing: np.ndarray
    kernel_volume: np.ndarray
    e4_force: np.ndarray
    potential_force: np.ndarray


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


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


def parse_float(path: Path, key: str) -> float:
    text = path.read_text(errors="replace")
    pattern = rf"^{re.escape(key)}=([^\r\n]+)$"
    match = re.search(pattern, text, re.MULTILINE)
    if match is None:
        raise RuntimeError(f"Missing required marker {key} in {path}")
    value = float(match.group(1).strip())
    if not math.isfinite(value):
        raise RuntimeError(f"Nonfinite {key}")
    return value


def independent_terms(interp, points: np.ndarray):
    """Independently reconstruct e2, e4, V, rho, and S."""
    u = np.asarray(interp(points), dtype=float)
    ux = np.asarray(interp(points, nu=(1, 0, 0)), dtype=float)
    uy = np.asarray(interp(points, nu=(0, 1, 0)), dtype=float)
    uz = np.asarray(interp(points, nu=(0, 0, 1)), dtype=float)

    norm = np.linalg.norm(u, axis=1)
    if float(np.min(norm)) < 0.25:
        raise RuntimeError(
            f"Raw spline field approaches zero norm: {float(np.min(norm))}"
        )

    phi = u / norm[:, None]

    def tangent(du: np.ndarray) -> np.ndarray:
        longitudinal = np.sum(phi * du, axis=1)
        return (
            du
            - phi * longitudinal[:, None]
        ) / norm[:, None]

    qx = tangent(ux)
    qy = tangent(uy)
    qz = tangent(uz)

    gxx = np.sum(qx * qx, axis=1)
    gyy = np.sum(qy * qy, axis=1)
    gzz = np.sum(qz * qz, axis=1)

    gxy = np.sum(qx * qy, axis=1)
    gxz = np.sum(qx * qz, axis=1)
    gyz = np.sum(qy * qz, axis=1)

    e2 = gxx + gyy + gzz

    e4 = (
        gxx * gyy - gxy * gxy
        + gxx * gzz - gxz * gxz
        + gyy * gzz - gyz * gyz
    )

    sigma = phi[:, 0]
    potential = MASS * MASS * (1.0 - sigma) * (1.0 + ETA * sigma)

    rho = e2 + e4 + potential
    active = 2.0 * (e4 - potential)

    return phi, qx, qy, qz, e2, e4, potential, rho, active


def independent_kernel(
    points: np.ndarray,
    center: np.ndarray,
    direction: np.ndarray,
    payload_radius: float,
) -> np.ndarray:
    q = points - center[None, :]
    r2 = np.sum(q * q, axis=1)
    r = np.sqrt(np.maximum(r2, 0.0))

    denominator = np.where(
        r < payload_radius,
        payload_radius**3,
        np.maximum(r2 * r, 1.0e-300),
    )

    return (q @ direction) / denominator


def empty_ledger(n: int) -> CellLedger:
    return CellLedger(
        *[np.zeros(n, dtype=float) for _ in range(len(fields(CellLedger)))]
    )


def integrate_subset(
    interp,
    lowers: np.ndarray,
    global_indices: np.ndarray,
    offsets: np.ndarray,
    weights: np.ndarray,
    center: np.ndarray,
    direction: np.ndarray,
    payload_radius: float,
    ledger: CellLedger,
    label: str,
) -> None:
    nq = len(weights)
    cells_per_batch = max(1, MAX_BATCH_POINTS // max(nq, 1))

    total_cells = len(lowers)
    last_bucket = -1

    for start in range(0, total_cells, cells_per_batch):
        stop = min(start + cells_per_batch, total_cells)

        lo = lowers[start:stop]
        ids = global_indices[start:stop]

        pts = (
            lo[:, None, :]
            + offsets[None, :, :]
        ).reshape(-1, 3)

        (
            _,
            _,
            _,
            _,
            e2,
            e4,
            potential,
            rho,
            active,
        ) = independent_terms(interp, pts)

        kernel = independent_kernel(
            pts,
            center,
            direction,
            payload_radius,
        )

        nc = len(lo)

        w2 = np.broadcast_to(
            weights[None, :],
            (nc, nq),
        )

        e2 = e2.reshape(nc, nq)
        e4 = e4.reshape(nc, nq)
        potential = potential.reshape(nc, nq)
        rho = rho.reshape(nc, nq)
        active = active.reshape(nc, nq)
        kernel = kernel.reshape(nc, nq)

        influence = active * kernel

        ledger.e2[ids] = np.sum(e2 * w2, axis=1)
        ledger.e4[ids] = np.sum(e4 * w2, axis=1)
        ledger.potential[ids] = np.sum(potential * w2, axis=1)
        ledger.energy[ids] = np.sum(rho * w2, axis=1)
        ledger.active[ids] = np.sum(active * w2, axis=1)

        weighted_i = influence * w2

        ledger.influence[ids] = np.sum(weighted_i, axis=1)
        ledger.outward[ids] = np.sum(
            np.maximum(influence, 0.0) * w2,
            axis=1,
        )
        ledger.opposing[ids] = np.sum(
            np.maximum(-influence, 0.0) * w2,
            axis=1,
        )

        ledger.kernel_volume[ids] = np.sum(kernel * w2, axis=1)

        ledger.e4_force[ids] = np.sum(
            2.0 * e4 * kernel * w2,
            axis=1,
        )

        ledger.potential_force[ids] = np.sum(
            -2.0 * potential * kernel * w2,
            axis=1,
        )

        pct = int(100 * stop / max(total_cells, 1))
        bucket = pct // 10

        if bucket != last_bucket:
            print(
                f"{label}_PROGRESS={stop}/{total_cells} "
                f"PERCENT={pct}",
                flush=True,
            )
            last_bucket = bucket


def baryon_density_at_centers(interp, points: np.ndarray) -> np.ndarray:
    """Compute signed continuum baryon-density proxy at cell centers."""
    out = np.zeros(len(points), dtype=float)

    for start in range(0, len(points), MAX_BATCH_POINTS):
        stop = min(start + MAX_BATCH_POINTS, len(points))

        (
            phi,
            qx,
            qy,
            qz,
            _,
            _,
            _,
            _,
            _,
        ) = independent_terms(interp, points[start:stop])

        matrix = np.stack(
            [phi, qx, qy, qz],
            axis=-1,
        )

        det = np.linalg.det(matrix)

        out[start:stop] = (
            -det
            /
            (2.0 * math.pi**2)
        )

    return out


def weighted_quantile(
    values: np.ndarray,
    weights: np.ndarray,
    fraction: float,
) -> float:
    total = float(np.sum(weights))

    if total <= 0.0:
        return float("nan")

    order = np.argsort(values)
    v = values[order]
    w = weights[order]

    cumulative = np.cumsum(w) / total
    idx = int(np.searchsorted(cumulative, fraction, side="left"))
    idx = min(idx, len(v) - 1)

    return float(v[idx])


def concentration_class(f50: float, fpart: float) -> str:
    if f50 <= 0.01:
        return "EXTREME_CONCENTRATION"
    if f50 <= 0.05:
        return "VERY_STRONG_CONCENTRATION"
    if f50 <= 0.10:
        return "STRONG_CONCENTRATION"
    if f50 >= 0.35 and fpart >= 0.50:
        return "DIFFUSE_SMALL_SKELETON_DISFAVORED"
    return "INTERMEDIATE"


def safe_spearman(x: np.ndarray, y: np.ndarray) -> float:
    good = (
        np.isfinite(x)
        & np.isfinite(y)
    )

    if int(np.count_nonzero(good)) < 10:
        return float("nan")

    value = spearmanr(
        x[good],
        y[good],
        nan_policy="omit",
    ).statistic

    return float(value)


def radial_and_shuffle_diagnostics(
    ledger: CellLedger,
    centers: np.ndarray,
    dx: float,
    rng: np.random.Generator,
):
    radius = np.linalg.norm(centers, axis=1)
    cell_volume = dx**3

    edges = np.linspace(
        0.0,
        float(np.max(radius)) * (1.0 + 1.0e-12),
        RADIAL_BINS + 1,
    )

    bins = np.searchsorted(
        edges,
        radius,
        side="right",
    ) - 1

    bins = np.clip(bins, 0, RADIAL_BINS - 1)

    source_density = ledger.active / cell_volume

    radial_force = 0.0
    table = []

    members = []

    for b in range(RADIAL_BINS):
        ids = np.flatnonzero(bins == b)
        members.append(ids)

        if len(ids) == 0:
            table.append(
                [
                    0.5 * (edges[b] + edges[b + 1]),
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                ]
            )
            continue

        shell_volume = len(ids) * cell_volume
        shell_active = float(np.sum(ledger.active[ids]))
        shell_energy = float(np.sum(ledger.energy[ids]))
        shell_kernel_volume = float(
            np.sum(ledger.kernel_volume[ids])
        )

        mean_source = shell_active / shell_volume

        shell_force = mean_source * shell_kernel_volume
        radial_force += shell_force

        table.append(
            [
                0.5 * (edges[b] + edges[b + 1]),
                shell_active,
                shell_energy,
                shell_kernel_volume,
                shell_force,
            ]
        )

    unrestricted = []
    sign_preserving = []

    for _ in range(SHUFFLES):
        shuffled = source_density.copy()
        shuffled_sign = source_density.copy()

        for ids in members:
            if len(ids) < 2:
                continue

            shuffled[ids] = source_density[
                rng.permutation(ids)
            ]

            positive_ids = ids[source_density[ids] >= 0.0]
            negative_ids = ids[source_density[ids] < 0.0]

            if len(positive_ids) >= 2:
                shuffled_sign[positive_ids] = source_density[
                    rng.permutation(positive_ids)
                ]

            if len(negative_ids) >= 2:
                shuffled_sign[negative_ids] = source_density[
                    rng.permutation(negative_ids)
                ]

        unrestricted.append(
            float(
                np.sum(
                    shuffled
                    * ledger.kernel_volume
                )
            )
        )

        sign_preserving.append(
            float(
                np.sum(
                    shuffled_sign
                    * ledger.kernel_volume
                )
            )
        )

    return (
        float(radial_force),
        np.asarray(unrestricted, dtype=float),
        np.asarray(sign_preserving, dtype=float),
        np.asarray(table, dtype=float),
    )


def analyze(
    tag: str,
    ledger: CellLedger,
    centers: np.ndarray,
    baryon_density: np.ndarray,
    center: np.ndarray,
    dx: float,
    reference_force: float,
    reference_l1: float,
    rng: np.random.Generator,
):
    cell_volume = dx**3

    total_energy = float(np.sum(ledger.energy))
    e2_total = float(np.sum(ledger.e2))
    e4_total = float(np.sum(ledger.e4))
    v_total = float(np.sum(ledger.potential))

    net = float(np.sum(ledger.influence))
    outward = float(np.sum(ledger.outward))
    opposing = float(np.sum(ledger.opposing))

    l1 = outward + opposing

    cancellation = (
        l1 / max(abs(net), 1.0e-300)
    )

    term_e4 = float(np.sum(ledger.e4_force))
    term_v = float(np.sum(ledger.potential_force))
    term_error = abs(net - (term_e4 + term_v))

    closure_abs = abs(net - reference_force)
    closure_l1 = closure_abs / max(reference_l1, 1.0)

    attribution_closed = bool(
        closure_l1 <= ATTRIBUTION_L1_TOL
    )

    if float(np.min(ledger.energy)) < -1.0e-10 * max(
        float(np.max(ledger.energy)),
        1.0,
    ):
        raise RuntimeError(
            f"{tag}: materially negative reconstructed energy cell"
        )

    energy = np.maximum(ledger.energy, 0.0)

    energy_density = energy / cell_volume
    energy_floor = (
        ENERGY_FLOOR_REL
        * max(float(np.max(energy_density)), 1.0e-300)
    )

    valid = energy_density > energy_floor

    leverage = np.zeros_like(energy)

    leverage[valid] = (
        ledger.outward[valid]
        /
        np.maximum(energy[valid], 1.0e-300)
    )

    mean1 = float(
        np.sum(energy * leverage)
        /
        max(total_energy, 1.0e-300)
    )

    mean2 = float(
        np.sum(energy * leverage * leverage)
        /
        max(total_energy, 1.0e-300)
    )

    fpart = (
        mean1 * mean1 / mean2
        if mean2 > 0.0
        else float("nan")
    )

    order = np.argsort(leverage)[::-1]

    cumulative_energy = (
        np.cumsum(energy[order])
        /
        max(total_energy, 1.0e-300)
    )

    cumulative_outward = (
        np.cumsum(ledger.outward[order])
        /
        max(outward, 1.0e-300)
    )

    def fq(q: float) -> float:
        idx = int(
            np.searchsorted(
                cumulative_outward,
                q,
                side="left",
            )
        )
        idx = min(idx, len(order) - 1)
        return float(cumulative_energy[idx])

    def share_at_energy(fraction: float) -> float:
        return float(
            np.interp(
                fraction,
                cumulative_energy,
                cumulative_outward,
                left=0.0,
                right=1.0,
            )
        )

    F25 = fq(0.25)
    F50 = fq(0.50)
    F75 = fq(0.75)
    F90 = fq(0.90)
    F99 = fq(0.99)

    source_radius = np.linalg.norm(centers, axis=1)
    payload_distance = np.linalg.norm(
        centers - center[None, :],
        axis=1,
    )

    r50 = weighted_quantile(
        source_radius,
        ledger.outward,
        0.50,
    )
    r90 = weighted_quantile(
        source_radius,
        ledger.outward,
        0.90,
    )

    d50 = weighted_quantile(
        payload_distance,
        ledger.outward,
        0.50,
    )
    d90 = weighted_quantile(
        payload_distance,
        ledger.outward,
        0.90,
    )

    if outward > 0.0:
        influence_centroid = (
            np.sum(
                centers
                * ledger.outward[:, None],
                axis=0,
            )
            / outward
        )

        delta = centers - influence_centroid[None, :]

        covariance = (
            np.einsum(
                "ni,nj,n->ij",
                delta,
                delta,
                ledger.outward,
            )
            / outward
        )

        principal_variances = np.linalg.eigvalsh(
            covariance
        )[::-1]

    else:
        influence_centroid = np.full(3, np.nan)
        principal_variances = np.full(3, np.nan)

    fraction_e2 = e2_total / max(total_energy, 1.0e-300)
    fraction_e4 = e4_total / max(total_energy, 1.0e-300)
    fraction_v = v_total / max(total_energy, 1.0e-300)

    potential_dominated = ledger.potential > ledger.e4

    potential_dom_energy = float(
        np.sum(energy[potential_dominated])
        /
        max(total_energy, 1.0e-300)
    )

    potential_dom_outward = float(
        np.sum(ledger.outward[potential_dominated])
        /
        max(outward, 1.0e-300)
    )

    e4_dom_outward = float(
        np.sum(ledger.outward[~potential_dominated])
        /
        max(outward, 1.0e-300)
    )

    energy_fraction_local = np.zeros_like(energy)
    nz = energy > 0.0

    e2_fraction_local = np.zeros_like(energy)
    e4_fraction_local = np.zeros_like(energy)
    v_fraction_local = np.zeros_like(energy)

    e2_fraction_local[nz] = ledger.e2[nz] / energy[nz]
    e4_fraction_local[nz] = ledger.e4[nz] / energy[nz]
    v_fraction_local[nz] = ledger.potential[nz] / energy[nz]

    baryon_abs = np.abs(baryon_density)

    corr = {
        "radius": safe_spearman(leverage[valid], source_radius[valid]),
        "payload_distance": safe_spearman(
            leverage[valid],
            payload_distance[valid],
        ),
        "e2_fraction": safe_spearman(
            leverage[valid],
            e2_fraction_local[valid],
        ),
        "e4_fraction": safe_spearman(
            leverage[valid],
            e4_fraction_local[valid],
        ),
        "V_fraction": safe_spearman(
            leverage[valid],
            v_fraction_local[valid],
        ),
        "abs_baryon_density": safe_spearman(
            leverage[valid],
            baryon_abs[valid],
        ),
        "active_cell": safe_spearman(
            leverage[valid],
            ledger.active[valid],
        ),
    }

    top50_mask = np.zeros(len(order), dtype=bool)
    idx50 = int(
        np.searchsorted(
            cumulative_outward,
            0.50,
            side="left",
        )
    )
    top50_mask[order[: idx50 + 1]] = True

    baryon_weight = baryon_abs * cell_volume

    top50_abs_baryon_share = float(
        np.sum(baryon_weight[top50_mask])
        /
        max(float(np.sum(baryon_weight)), 1.0e-300)
    )

    radial_force, shuffles, sign_shuffles, radial_table = (
        radial_and_shuffle_diagnostics(
            ledger,
            centers,
            dx,
            rng,
        )
    )

    characteristic_h = float(np.linalg.norm(center))

    eta_op = (
        characteristic_h**2
        * net
        /
        max(total_energy, 1.0e-300)
    )

    eta_gross = (
        characteristic_h**2
        * outward
        /
        max(total_energy, 1.0e-300)
    )

    classification = concentration_class(F50, fpart)

    excluded_energy_fraction = float(
        np.sum(energy[~valid])
        /
        max(total_energy, 1.0e-300)
    )

    excluded_outward_fraction = float(
        np.sum(ledger.outward[~valid])
        /
        max(outward, 1.0e-300)
    )

    print(f"\n=== {tag.upper()} INTROSPECTIVE METRICS ===")
    print(f"{tag.upper()}_ATTRIBUTION_FORCE={net:.15e}")
    print(f"{tag.upper()}_REFERENCE_FORCE={reference_force:.15e}")
    print(f"{tag.upper()}_ATTRIBUTION_CLOSURE_ABS={closure_abs:.15e}")
    print(f"{tag.upper()}_ATTRIBUTION_CLOSURE_OVER_L1={closure_l1:.15e}")
    print(
        f"{tag.upper()}_ATTRIBUTION_CLOSED="
        + ("YES" if attribution_closed else "NO")
    )

    print(f"{tag.upper()}_A_PLUS={outward:.15e}")
    print(f"{tag.upper()}_A_MINUS={opposing:.15e}")
    print(f"{tag.upper()}_A_NET={net:.15e}")
    print(f"{tag.upper()}_CANCELLATION_FACTOR={cancellation:.15e}")

    print(f"{tag.upper()}_TOTAL_ENERGY={total_energy:.15e}")
    print(f"{tag.upper()}_E2_FRACTION={fraction_e2:.15e}")
    print(f"{tag.upper()}_E4_FRACTION={fraction_e4:.15e}")
    print(f"{tag.upper()}_V_FRACTION={fraction_v:.15e}")

    print(f"{tag.upper()}_E4_DIRECT_FORCE={term_e4:.15e}")
    print(f"{tag.upper()}_V_DIRECT_FORCE={term_v:.15e}")
    print(f"{tag.upper()}_TERM_RECONSTRUCTION_ERROR={term_error:.15e}")

    print(f"{tag.upper()}_F25={F25:.15e}")
    print(f"{tag.upper()}_F50={F50:.15e}")
    print(f"{tag.upper()}_F75={F75:.15e}")
    print(f"{tag.upper()}_F90={F90:.15e}")
    print(f"{tag.upper()}_F99={F99:.15e}")
    print(f"{tag.upper()}_ENERGY_PARTICIPATION={fpart:.15e}")

    print(
        f"{tag.upper()}_TOP_1PCT_ENERGY_OUTWARD_SHARE="
        f"{share_at_energy(0.01):.15e}"
    )
    print(
        f"{tag.upper()}_TOP_5PCT_ENERGY_OUTWARD_SHARE="
        f"{share_at_energy(0.05):.15e}"
    )
    print(
        f"{tag.upper()}_TOP_10PCT_ENERGY_OUTWARD_SHARE="
        f"{share_at_energy(0.10):.15e}"
    )
    print(
        f"{tag.upper()}_TOP_25PCT_ENERGY_OUTWARD_SHARE="
        f"{share_at_energy(0.25):.15e}"
    )

    print(f"{tag.upper()}_OUTWARD_RADIUS_50={r50:.15e}")
    print(f"{tag.upper()}_OUTWARD_RADIUS_90={r90:.15e}")
    print(f"{tag.upper()}_PAYLOAD_DISTANCE_50={d50:.15e}")
    print(f"{tag.upper()}_PAYLOAD_DISTANCE_90={d90:.15e}")

    print(
        f"{tag.upper()}_INFLUENCE_CENTROID="
        + ",".join(f"{x:.15e}" for x in influence_centroid)
    )
    print(
        f"{tag.upper()}_INFLUENCE_PRINCIPAL_VARIANCES="
        + ",".join(f"{x:.15e}" for x in principal_variances)
    )

    print(
        f"{tag.upper()}_POTENTIAL_DOMINATED_ENERGY_FRACTION="
        f"{potential_dom_energy:.15e}"
    )
    print(
        f"{tag.upper()}_POTENTIAL_DOMINATED_OUTWARD_SHARE="
        f"{potential_dom_outward:.15e}"
    )
    print(
        f"{tag.upper()}_E4_DOMINATED_OUTWARD_SHARE="
        f"{e4_dom_outward:.15e}"
    )

    print(
        f"{tag.upper()}_TOP50_OUTWARD_ABS_BARYON_SHARE="
        f"{top50_abs_baryon_share:.15e}"
    )

    for name, value in corr.items():
        print(
            f"{tag.upper()}_SPEARMAN_LEVERAGE_{name.upper()}="
            f"{value:.15e}"
        )

    print(f"{tag.upper()}_RADIALIZED_FORCE={radial_force:.15e}")
    print(
        f"{tag.upper()}_RADIALIZED_FORCE_MINUS_DIRECT_OVER_L1="
        f"{(radial_force-net)/max(l1,1.0e-300):.15e}"
    )

    print(
        f"{tag.upper()}_ANGULAR_SHUFFLE_FORCE_MEDIAN="
        f"{float(np.median(shuffles)):.15e}"
    )
    print(
        f"{tag.upper()}_ANGULAR_SHUFFLE_FORCE_P05="
        f"{float(np.quantile(shuffles,0.05)):.15e}"
    )
    print(
        f"{tag.upper()}_ANGULAR_SHUFFLE_FORCE_P95="
        f"{float(np.quantile(shuffles,0.95)):.15e}"
    )

    print(
        f"{tag.upper()}_SIGN_PRESERVING_SHUFFLE_FORCE_MEDIAN="
        f"{float(np.median(sign_shuffles)):.15e}"
    )
    print(
        f"{tag.upper()}_SIGN_PRESERVING_SHUFFLE_FORCE_P05="
        f"{float(np.quantile(sign_shuffles,0.05)):.15e}"
    )
    print(
        f"{tag.upper()}_SIGN_PRESERVING_SHUFFLE_FORCE_P95="
        f"{float(np.quantile(sign_shuffles,0.95)):.15e}"
    )

    print(f"{tag.upper()}_ETA_OP={eta_op:.15e}")
    print(f"{tag.upper()}_ETA_GROSS_OUTWARD={eta_gross:.15e}")
    print(f"{tag.upper()}_ENERGY_FLOOR_DENSITY={energy_floor:.15e}")
    print(
        f"{tag.upper()}_FLOOR_EXCLUDED_ENERGY_FRACTION="
        f"{excluded_energy_fraction:.15e}"
    )
    print(
        f"{tag.upper()}_FLOOR_EXCLUDED_OUTWARD_FRACTION="
        f"{excluded_outward_fraction:.15e}"
    )
    print(
        f"{tag.upper()}_CONCENTRATION_CLASS="
        f"{classification}"
    )

    curve_energy = np.linspace(0.0, 1.0, 101)
    curve_outward = np.interp(
        curve_energy,
        cumulative_energy,
        cumulative_outward,
        left=0.0,
        right=1.0,
    )

    curve = np.column_stack(
        [curve_energy, curve_outward]
    )

    return {
        "attribution_closed": attribution_closed,
        "reference_force": reference_force,
        "net": net,
        "outward": outward,
        "opposing": opposing,
        "l1": l1,
        "cancellation": cancellation,
        "energy": total_energy,
        "e2_fraction": fraction_e2,
        "e4_fraction": fraction_e4,
        "V_fraction": fraction_v,
        "e4_force": term_e4,
        "V_force": term_v,
        "F25": F25,
        "F50": F50,
        "F75": F75,
        "F90": F90,
        "F99": F99,
        "f_part": fpart,
        "top1_share": share_at_energy(0.01),
        "top5_share": share_at_energy(0.05),
        "top10_share": share_at_energy(0.10),
        "top25_share": share_at_energy(0.25),
        "r50": r50,
        "r90": r90,
        "d50": d50,
        "d90": d90,
        "eta_op": eta_op,
        "eta_gross": eta_gross,
        "classification": classification,
        "potential_dominated_energy_fraction": potential_dom_energy,
        "potential_dominated_outward_share": potential_dom_outward,
        "top50_abs_baryon_share": top50_abs_baryon_share,
        "radialized_force": radial_force,
        "shuffle_median": float(np.median(shuffles)),
        "shuffle_p05": float(np.quantile(shuffles, 0.05)),
        "shuffle_p95": float(np.quantile(shuffles, 0.95)),
        "sign_shuffle_median": float(np.median(sign_shuffles)),
        "correlations": corr,
        "curve": curve,
        "radial_table": radial_table,
        "leverage": leverage,
    }


def main() -> None:
    print(
        "=== INT-01 — CERTIFIED FIXED-FIELD INFLUENCE TOMOGRAPHY ===",
        flush=True,
    )

    print("\n=== A — FAIL-CLOSED UPSTREAM AUDIT ===")

    require(C2AQS_SOURCE)
    require(N65_ARTIFACT)
    require(N65_FORCE_LOG)

    source_hash = sha256(C2AQS_SOURCE)

    print(f"023C2AQS_SOURCE_SHA256={source_hash}")

    if source_hash != EXPECTED_C2AQS_SHA256:
        raise RuntimeError(
            "023C2AQS source hash mismatch"
        )

    print("UPSTREAM_023C2AQS_SOURCE_AUDIT=PASS")

    c2aqs = load_module(
        "int01_c2aqs",
        C2AQS_SOURCE,
    )

    aqr = load_module(
        "int01_aqr",
        c2aqs.AQR_SOURCE,
    )

    if sha256(c2aqs.AQR_SOURCE) != c2aqs.EXPECTED_AQR_SHA256:
        raise RuntimeError(
            "023C2AQR analytic payload source hash mismatch"
        )

    aqr.validate_analytic_formulae()

    print("ANALYTIC_PAYLOAD_KERNEL_VALIDATION=PASS")

    c2aq = aqr.load_module(
        "int01_c2aq",
        aqr.C2AQ_SOURCE,
    )

    cr3 = c2aq.load_module(
        "int01_cr3",
        c2aq.CR3_SOURCE,
    )

    global B, ETA, MASS

    B = int(c2aq.B)
    ETA = float(c2aq.ETA)
    MASS = float(c2aq.MASS)

    payload_center = float(c2aq.PAYLOAD_CENTER)
    payload_radius = float(c2aq.PAYLOAD_RADIUS)

    direction = np.asarray(
        c2aq.KNOWN_WORST_DIRECTION,
        dtype=float,
    )

    direction /= np.linalg.norm(direction)

    center = payload_center * direction

    print("\n=== B — STRICT N65 FIELD AUDIT ===")

    phi, axis, dx = c2aqs.load_n65()

    Edisc, E2disc, E4disc, E0disc, grad = (
        cr3.riemannian_gradient_density(
            phi,
            dx,
        )
    )

    grad_rms, grad_max = cr3.gradient_norms(grad)
    topology4 = cr3.topology4(phi, dx)

    print(f"N65_DISCRETE_ENERGY={Edisc:.15e}")
    print(f"N65_DISCRETE_E2={E2disc:.15e}")
    print(f"N65_DISCRETE_E4={E4disc:.15e}")
    print(f"N65_DISCRETE_V={E0disc:.15e}")
    print(f"N65_GRAD_RMS={grad_rms:.15e}")
    print(f"N65_GRAD_MAX={grad_max:.15e}")
    print(f"N65_TOPOLOGY4={topology4:.15e}")

    if grad_rms > GRAD_RMS_TOL:
        raise RuntimeError(
            "N65 strict RMS stationarity gate no longer passes"
        )

    if grad_max > GRAD_MAX_TOL:
        raise RuntimeError(
            "N65 strict max stationarity gate no longer passes"
        )

    if abs(abs(topology4) / B - 1.0) > 3.0e-2:
        raise RuntimeError(
            "N65 topology4 audit failed"
        )

    print("N65_STRICT_STATIONARITY_AUDIT=PASS")

    print("\n=== C — PAYLOAD / QUADRATURE PARTITION ===")

    all_lowers = c2aqs.cell_lowers(axis)
    all_indices = np.arange(len(all_lowers), dtype=int)

    dmin = c2aqs.min_distance_to_cells(
        all_lowers,
        dx,
        center,
    )

    near_radius = c2aqs.NEAR_RADIUS_DX * dx
    near_mask = dmin < near_radius

    far_indices = all_indices[~near_mask]
    near_indices = all_indices[near_mask]

    far_lowers = all_lowers[far_indices]
    near_lowers = all_lowers[near_indices]

    far3_offsets, far3_weights = (
        c2aqs.composite_gauss_offsets(
            dx,
            3,
            1,
        )
    )

    far4_offsets, far4_weights = (
        c2aqs.composite_gauss_offsets(
            dx,
            4,
            1,
        )
    )

    near_fine_offsets, near_fine_weights = (
        c2aqs.composite_gauss_offsets(
            dx,
            c2aqs.NEAR_GAUSS_ORDER,
            c2aqs.NEAR_FINE_SUBDIV,
        )
    )

    print(f"TOTAL_SOURCE_CELLS={len(all_lowers)}")
    print(f"FAR_SOURCE_CELLS={len(far_lowers)}")
    print(f"NEAR_SOURCE_CELLS={len(near_lowers)}")
    print(f"PAYLOAD_CENTER={payload_center:.15e}")
    print(f"PAYLOAD_RADIUS={payload_radius:.15e}")
    print(f"PAYLOAD_RADIUS_OVER_DX={payload_radius/dx:.15e}")
    print(
        "PAYLOAD_DIRECTION="
        + ",".join(f"{x:.15e}" for x in direction)
    )

    const_relerr = c2aqs.constant_source_validation(
        aqr,
        axis,
        dx,
        far_lowers,
        near_lowers,
        center,
        direction,
        payload_radius,
        far3_offsets,
        far3_weights,
        near_fine_offsets,
        near_fine_weights,
    )

    if const_relerr > c2aqs.FORCE_CONST_VALIDATION_REL_TOL:
        raise RuntimeError(
            "Constant-source payload cubature validation failed"
        )

    print("\n=== D — BUILD INDEPENDENT CONTINUOUS FIELDS ===")

    cubic = c2aqs.build_interpolator(
        axis,
        phi,
        "cubic",
    )

    print("CUBIC_INTERPOLATOR=READY", flush=True)

    quintic = c2aqs.build_interpolator(
        axis,
        phi,
        "quintic",
    )

    print("QUINTIC_INTERPOLATOR=READY", flush=True)

    centers = all_lowers + 0.5 * dx

    reference = {
        "cubic": {
            "force": parse_float(
                N65_FORCE_LOG,
                "CUBIC_Q4_NEAR_FINE_FORCE",
            ),
            "l1": parse_float(
                N65_FORCE_LOG,
                "CUBIC_Q4_NEAR_FINE_L1",
            ),
        },
        "quintic": {
            "force": parse_float(
                N65_FORCE_LOG,
                "QUINTIC_Q4_NEAR_FINE_FORCE",
            ),
            "l1": parse_float(
                N65_FORCE_LOG,
                "QUINTIC_Q4_NEAR_FINE_L1",
            ),
        },
    }

    rng = np.random.default_rng(RNG_SEED)

    ledgers = {}
    analyses = {}
    baryon = {}

    for tag, interp in (
        ("cubic", cubic),
        ("quintic", quintic),
    ):
        print(
            f"\n=== E — {tag.upper()} INDEPENDENT TOMOGRAPHY ===",
            flush=True,
        )

        ledger = empty_ledger(len(all_lowers))

        integrate_subset(
            interp,
            far_lowers,
            far_indices,
            far4_offsets,
            far4_weights,
            center,
            direction,
            payload_radius,
            ledger,
            f"{tag.upper()}_FAR_Q4",
        )

        integrate_subset(
            interp,
            near_lowers,
            near_indices,
            near_fine_offsets,
            near_fine_weights,
            center,
            direction,
            payload_radius,
            ledger,
            f"{tag.upper()}_NEAR_FINE",
        )

        baryon_density = baryon_density_at_centers(
            interp,
            centers,
        )

        ledgers[tag] = ledger
        baryon[tag] = baryon_density

        analyses[tag] = analyze(
            tag,
            ledger,
            centers,
            baryon_density,
            center,
            dx,
            reference[tag]["force"],
            reference[tag]["l1"],
            rng,
        )

        np.savetxt(
            DATA / f"int01_{tag}_concentration_curve.csv",
            analyses[tag]["curve"],
            delimiter=",",
            header="energy_fraction,gross_outward_share",
            comments="",
        )

        np.savetxt(
            DATA / f"int01_{tag}_radial_bins.csv",
            analyses[tag]["radial_table"],
            delimiter=",",
            header=(
                "radius_mid,"
                "active_integral,"
                "energy_integral,"
                "kernel_volume_integral,"
                "radialized_force"
            ),
            comments="",
        )

    print("\n=== F — REPRESENTATION ROBUSTNESS ===")

    c = analyses["cubic"]
    q = analyses["quintic"]

    force_spread = abs(c["net"] - q["net"])
    f50_spread = abs(c["F50"] - q["F50"])
    f90_spread = abs(c["F90"] - q["F90"])
    fpart_spread = abs(c["f_part"] - q["f_part"])

    print(f"CUBIC_QUINTIC_FORCE_SPREAD={force_spread:.15e}")
    print(f"CUBIC_QUINTIC_F50_SPREAD={f50_spread:.15e}")
    print(f"CUBIC_QUINTIC_F90_SPREAD={f90_spread:.15e}")
    print(f"CUBIC_QUINTIC_FPART_SPREAD={fpart_spread:.15e}")

    print(
        "CUBIC_CONCENTRATION_CLASS="
        + c["classification"]
    )

    print(
        "QUINTIC_CONCENTRATION_CLASS="
        + q["classification"]
    )

    both_attribution = (
        c["attribution_closed"]
        and q["attribution_closed"]
    )

    strong_classes = {
        "STRONG_CONCENTRATION",
        "VERY_STRONG_CONCENTRATION",
        "EXTREME_CONCENTRATION",
    }

    both_strong = (
        c["classification"] in strong_classes
        and q["classification"] in strong_classes
    )

    both_diffuse = (
        c["classification"]
        == "DIFFUSE_SMALL_SKELETON_DISFAVORED"
        and q["classification"]
        == "DIFFUSE_SMALL_SKELETON_DISFAVORED"
    )

    if not both_attribution:
        decision = (
            "BLOCKED_ATTRIBUTION_RECONSTRUCTION_NOT_CLOSED"
        )
        next_action = (
            "REPAIR_INT01_ATTRIBUTION_BEFORE_INTERPRETING_HOTSPOTS"
        )
    elif both_strong:
        decision = (
            "PROMISING_PRODUCTIVE_SKELETON_SIGNAL_AT_N65"
        )
        next_action = (
            "INT02_TERM_GEOMETRY_AND_ORIENTATION_ROBUSTNESS_"
            "THEN_FINE_GRID_CONFIRMATION"
        )
    elif both_diffuse:
        decision = (
            "SMALL_PRODUCTIVE_SKELETON_HYPOTHESIS_DISFAVORED_AT_N65"
        )
        next_action = (
            "QUANTIFY_CANCELLATION_AND_CONSERVATION_BOUND_"
            "BEFORE_MORE_COEFFICIENT_POLISHING"
        )
    else:
        decision = (
            "INTERMEDIATE_OR_REPRESENTATION_SENSITIVE_MECHANISM"
        )
        next_action = (
            "USE_INT01_ANATOMY_TO_TARGET_MINIMAL_NEXT_DIAGNOSTIC_"
            "AND_REQUIRE_N73_IF_REPRESENTATION_SENSITIVE"
        )

    print("\n=== G — INT-01 DECISION ===")
    print(
        "INT01_INDEPENDENT_ATTRIBUTION_BOTH="
        + ("PASS" if both_attribution else "FAIL")
    )
    print(f"INT01_DIRECTION_TEST={decision}")

    print(
        "PRODUCTIVE_SKELETON_PROMOTION_GRADE="
        "NO_N65_FIXED_FIELD_DIAGNOSTIC_ONLY"
    )

    print(
        "SOURCE_MASK_PHYSICAL_CONFIGURATION="
        "NO_DIAGNOSTIC_ONLY"
    )

    print(
        "N65_FORCE_CONTINUUM_PROMOTION="
        "UNCHANGED_STILL_REQUIRES_RESOLUTION_CLOSURE"
    )

    print(
        "FULL_PHYSICAL_HESSIAN="
        "NOT_ESTABLISHED"
    )

    print(
        "NONLINEAR_EINSTEIN_SKYRME="
        "NOT_ESTABLISHED"
    )

    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "APPROXIMATELY_70_TO_71_PERCENT_NOT_A_PROBABILITY"
    )

    print(f"NEXT={next_action}")

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_INT01_CERTIFIED_FIXED_FIELD_INFLUENCE_TOMOGRAPHY"
    )

    print("\n=== H — SAVE COMPLETE TOMOGRAPHY ===")

    payload = {
        "centers": centers,
        "payload_center": center,
        "payload_direction": direction,
        "payload_radius": np.array(payload_radius),
        "dx": np.array(dx),
    }

    for tag, ledger in ledgers.items():
        for field in fields(CellLedger):
            payload[
                f"{tag}_{field.name}"
            ] = getattr(ledger, field.name)

        payload[
            f"{tag}_baryon_density_center"
        ] = baryon[tag]

        payload[
            f"{tag}_leverage"
        ] = analyses[tag]["leverage"]

    np.savez_compressed(
        OUT_NPZ,
        **payload,
    )

    summary = {
        "claim_classification": (
            "PROJECT_DERIVED_INT01_CERTIFIED_FIXED_FIELD_"
            "INFLUENCE_TOMOGRAPHY"
        ),
        "decision": decision,
        "next": next_action,
        "attribution_both": both_attribution,
        "cubic": {
            k: v
            for k, v in c.items()
            if k not in {
                "curve",
                "radial_table",
                "leverage",
            }
        },
        "quintic": {
            k: v
            for k, v in q.items()
            if k not in {
                "curve",
                "radial_table",
                "leverage",
            }
        },
        "representation_spreads": {
            "force": force_spread,
            "F50": f50_spread,
            "F90": f90_spread,
            "f_part": fpart_spread,
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

    print(f"INT01_NPZ={OUT_NPZ}")
    print(f"INT01_SUMMARY_JSON={OUT_JSON}")
    print("INT01_RUN_COMPLETE=YES")


if __name__ == "__main__":
    main()
