#!/usr/bin/env python3
"""INT-03/04G — geometry causation and expansion-signature audit.

PURPOSE
-------
Identify which local geometric / field features control the productive
finite-payload response of the strict stationary N=65 B=7 field, and identify
which of those features change when the previously observed nonstationary
homothetic expansion unlocks hundreds-fold apparent outward-force headroom.

This run is deliberately diagnostic.  It does not optimize the field.

SCIENTIFIC QUESTIONS
--------------------
1. What reproducible local features distinguish high outward-leverage cells
   from the rest of the stationary N=65 field?

2. Are high-leverage cells close to the active-source zero surface

       Sigma_0 = { e4 = V },

   to energy-density ridges, or to topological-density ridges?

3. What strain-eigenvalue signature does the productive set carry?

4. When the same field is homothetically expanded from lambda=1 to
   lambda=1.25, which reference-coordinate cells account for the large
   increase in outward force?

5. Does the exact B=7 rational-map comparator show a compatible angular
   relationship between leverage and the conformal-stretch quantities

       J, J^2, J^4 ?

EXPANSION CAVEAT
----------------
The lambda=1.25 field is NOT stationary.  It is used only as a mechanism probe.

The previous exact scaling audit established

    A(lambda) = A_e4(1)/lambda^3 + lambda A_V(1)

and showed hundreds-fold apparent outward-force increase relative to the
near-cancelled lambda=1 baseline.

This run keeps that result explicitly in view while asking what spatial /
geometric change is responsible.

MODEL
-----
Static Skyrme field:

    phi = (sigma, pi_1, pi_2, pi_3),
    phi.phi = 1

Energy:

    rho = e2 + e4 + V

Active source:

    S = 2(e4 - V)

Unrestricted-field pullback matrix:

    g_ij = partial_i phi . partial_j phi

with ordered eigenvalues

    lambda_1 <= lambda_2 <= lambda_3.

Topology-density magnitude is reconstructed independently as

    |b| =
    |det(phi, partial_x phi, partial_y phi, partial_z phi)|
    / (2 pi^2).

SUB-CELL SIGMA_0 DIAGNOSTIC
---------------------------
The previous grid-distance transform was visibly quantized at approximately
one lattice spacing.  This run therefore adds the local tangent-plane
distance estimator

    d_plane = |S| / |grad S|

near Sigma_0.

It also reports nearest reconstructed sign-change-interface distance.  Neither
is promoted as exact continuum geometry, but agreement is informative.

ENERGY / TOPOLOGY RIDGES
------------------------
Define reference ridge sets from high local density:

    energy ridge      = top 10% of rho among non-vacuum cells
    topology ridge    = top 10% of |b| among topologically resolved cells.

Nearest spatial distances to those sets are computed for all cells.

PRODUCTIVE SET
--------------
The stationary and lambda=1.25 cellwise gross outward influence ledgers use
the already validated continuous quintic reconstruction and high-order
payload cubature chain.

For each field, the top-F50 set is the minimum-energy set accounting for
50 percent of gross outward influence.

EXPANSION-GAIN LEDGER
---------------------
In common reference coordinates define per-cell signed force gain

    Delta A_cell =
        A_cell(lambda=1.25)
        - A_cell(lambda=1).

The run reports how signed and positive gain partition among cells whose
center active-source sign changes as

    S+ -> S+
    S+ -> S-
    S- -> S+
    S- -> S-.

This is a diagnostic decomposition only.

EXACT-MAP COMPARATOR
--------------------
The promotion-grade exact B=7 rational-map field at eta=0.4, m=8 is rebuilt.

At every exact-map quadrature node compute:

    J
    J^2
    J^4
    W = |p' q - p q'|

and correlate them with gross outward leverage.

This is an independent angular-geometry comparator.  It is not an unrestricted
Cartesian resolution substitute.

PROMOTION / FALSIFICATION
-------------------------
This run establishes a useful INT-03/04 geometry result if:

- stationary cell-force attribution closes;
- lambda=1.25 attribution closes and reproduces the previous scaling result;
- top-F50 geometry metrics are reported without using naive midpoint payload
  force as central evidence;
- at least one geometry relation is reproducible between stationary N=65 and
  the exact-map comparator or the expansion-gain ledger.

It does NOT by itself establish INT Level 2 because strict fine-resolution
unrestricted support remains unresolved.

A simple geometry signature is weakened if:

- high leverage has only weak correlations with all declared field/geometric
  variables;
- productive-set distances are indistinguishable from energy-weighted
  background;
- expansion gain is spatially diffuse and unrelated to source-sign /
  strain / interface structure.

OUTPUTS
-------
results/data/int03_04g_geometry_causation_summary.json
results/data/int03_04g_geometry_correlations.csv
results/data/int03_04g_expansion_gain_sectors.csv
results/data/int03_04g_geometry_arrays.npz

CLAIM LIMITS
------------
No source mask is a physical configuration.
No lambda=1.25 result is a stationary realization.
No radiation/emission calculation is performed.
No >=10x physically accessible efficiency claim is authorized here.
No practical antigravity device is established.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_INT03_04G_GEOMETRY_CAUSATION_EXPANSION_SIGNATURE
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
from scipy.spatial import cKDTree
from scipy.stats import pearsonr, spearmanr


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

INT03S_SOURCE = SIM / "int03_04s_scale_zero_surface_audit.py"
INT03S_SUMMARY = DATA / "int03_04s_scale_zero_surface_summary.json"

OUT_JSON = DATA / "int03_04g_geometry_causation_summary.json"
OUT_CORR = DATA / "int03_04g_geometry_correlations.csv"
OUT_GAIN = DATA / "int03_04g_expansion_gain_sectors.csv"
OUT_NPZ = DATA / "int03_04g_geometry_arrays.npz"

B = 7
ETA = 0.40
MASS = 8.0

LAMBDA_REFERENCE = 1.0
LAMBDA_EXPANDED = 1.25

ENERGY_RIDGE_QUANTILE = 0.90
TOPOLOGY_RIDGE_QUANTILE = 0.90
VACUUM_RHO_REL_FLOOR = 1.0e-8
TOPOLOGY_REL_FLOOR = 1.0e-8

FORCE_CLOSE_REL = 5.0e-10
FORCE_CLOSE_ABS = 1.0e-9


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


def relerr(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0e-300)


def top_fraction_mask(
    energy: np.ndarray,
    positive_quantity: np.ndarray,
    fraction: float,
) -> np.ndarray:
    energy = np.maximum(np.asarray(energy, dtype=float), 0.0)
    q = np.maximum(np.asarray(positive_quantity, dtype=float), 0.0)

    leverage = np.zeros_like(energy)
    floor = max(float(np.max(energy)), 1.0) * 1.0e-15
    good = energy > floor
    leverage[good] = q[good] / energy[good]

    order = np.argsort(leverage)[::-1]
    cumulative = np.cumsum(q[order])
    target = fraction * float(np.sum(q))

    idx = int(np.searchsorted(cumulative, target, side="left"))
    idx = min(idx, len(order) - 1)

    mask = np.zeros(len(energy), dtype=bool)
    mask[order[: idx + 1]] = True
    return mask


def weighted_mean(x: np.ndarray, w: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    w = np.maximum(np.asarray(w, dtype=float), 0.0)
    good = np.isfinite(x) & np.isfinite(w)
    if not np.any(good):
        return float("nan")
    return float(
        np.sum(x[good] * w[good])
        / max(float(np.sum(w[good])), 1.0e-300)
    )


def weighted_jaccard(
    a: np.ndarray,
    b: np.ndarray,
    w: np.ndarray,
) -> float:
    inter = a & b
    union = a | b
    return float(
        np.sum(w[inter])
        / max(float(np.sum(w[union])), 1.0e-300)
    )


def safe_corr(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    good = np.isfinite(x) & np.isfinite(y)

    if int(np.count_nonzero(good)) < 20:
        return float("nan"), float("nan")

    xx = x[good]
    yy = y[good]

    if float(np.std(xx)) <= 1.0e-30 or float(np.std(yy)) <= 1.0e-30:
        return float("nan"), float("nan")

    p = float(pearsonr(xx, yy).statistic)
    s = float(spearmanr(xx, yy).statistic)
    return p, s


def reconstruct_scaled_ledgers(
    int03s,
    int01,
    c2aqs,
    interp,
    axis: np.ndarray,
    dx: float,
    direction: np.ndarray,
    h0: float,
    rp0: float,
):
    lambdas = np.asarray(
        [LAMBDA_REFERENCE, LAMBDA_EXPANDED],
        dtype=float,
    )

    center0 = h0 * direction
    lowers = c2aqs.cell_lowers(axis)

    q4_offsets, q4_weights = c2aqs.composite_gauss_offsets(
        dx,
        4,
        1,
    )

    result = int03s.block_scaled_ledgers(
        int01,
        interp,
        lowers,
        q4_offsets,
        q4_weights,
        center0,
        direction,
        rp0,
        lambdas,
    )

    dmin = c2aqs.min_distance_to_cells(
        lowers,
        dx,
        center0,
    )
    near_mask = dmin < c2aqs.NEAR_RADIUS_DX * dx
    near_ids = np.flatnonzero(near_mask)
    near_lowers = lowers[near_mask]

    near_offsets, near_weights = c2aqs.composite_gauss_offsets(
        dx,
        c2aqs.NEAR_GAUSS_ORDER,
        c2aqs.NEAR_FINE_SUBDIV,
    )

    old = int03s.block_scaled_ledgers(
        int01,
        interp,
        near_lowers,
        q4_offsets,
        q4_weights,
        center0,
        direction,
        rp0,
        lambdas,
    )
    new = int03s.block_scaled_ledgers(
        int01,
        interp,
        near_lowers,
        near_offsets,
        near_weights,
        center0,
        direction,
        rp0,
        lambdas,
    )

    for key in ("net", "outward"):
        result[key][:, near_ids] = new[key]

    for key in (
        "qplus",
        "qminus",
        "neg_volume",
        "total_volume",
        "sectors",
        "e4_force",
        "v_force",
    ):
        result[key] += new[key] - old[key]

    return lowers, result


def cell_center_geometry(
    int01,
    interp,
    lowers: np.ndarray,
    dx: float,
):
    centers = lowers + 0.5 * dx

    (
        phi,
        qx,
        qy,
        qz,
        e2,
        e4,
        potential,
        rho,
        active,
    ) = int01.independent_terms(
        interp,
        centers,
    )

    q = np.stack([qx, qy, qz], axis=1)
    # g_ij = q_i . q_j
    strain = np.einsum("niA,njA->nij", q, q)
    eig = np.linalg.eigvalsh(strain)

    eig1 = eig[:, 0]
    eig2 = eig[:, 1]
    eig3 = eig[:, 2]

    trace = eig1 + eig2 + eig3
    mean_eig = trace / 3.0

    strain_anisotropy = np.sqrt(
        (
            (eig1 - mean_eig) ** 2
            + (eig2 - mean_eig) ** 2
            + (eig3 - mean_eig) ** 2
        )
        / 3.0
    ) / np.maximum(mean_eig, 1.0e-15)

    eig_ratio = eig3 / np.maximum(eig1, 1.0e-15)

    mat = np.stack(
        [phi, qx, qy, qz],
        axis=-1,
    )
    det4 = np.linalg.det(mat)
    baryon_abs = np.abs(det4) / (2.0 * math.pi**2)

    nside = round(len(centers) ** (1.0 / 3.0))
    if nside**3 != len(centers):
        raise RuntimeError("Unexpected non-cubic source-cell lattice")

    Sgrid = active.reshape((nside, nside, nside))
    gx, gy, gz = np.gradient(
        Sgrid,
        dx,
        dx,
        dx,
        edge_order=2,
    )
    gradS = np.sqrt(gx * gx + gy * gy + gz * gz).ravel()

    grad_floor = max(float(np.max(gradS)), 1.0) * 1.0e-12
    sigma_plane_distance = np.abs(active) / np.maximum(gradS, grad_floor)

    sign = Sgrid >= 0.0
    interface = np.zeros_like(sign, dtype=bool)

    for ax in range(3):
        sl0 = [slice(None)] * 3
        sl1 = [slice(None)] * 3
        sl0[ax] = slice(0, nside - 1)
        sl1[ax] = slice(1, nside)

        a = sign[tuple(sl0)]
        b = sign[tuple(sl1)]
        changed = a != b

        interface[tuple(sl0)] |= changed
        interface[tuple(sl1)] |= changed

    interface_ids = np.flatnonzero(interface.ravel())
    if len(interface_ids) == 0:
        sigma_nearest_distance = np.full(len(centers), np.nan)
    else:
        tree = cKDTree(centers[interface_ids])
        sigma_nearest_distance = tree.query(
            centers,
            k=1,
            workers=-1,
        )[0]

    nonvac = rho > max(float(np.max(rho)), 1.0) * VACUUM_RHO_REL_FLOOR

    if int(np.count_nonzero(nonvac)) < 100:
        raise RuntimeError("Non-vacuum mask unexpectedly small")

    energy_threshold = float(
        np.quantile(
            rho[nonvac],
            ENERGY_RIDGE_QUANTILE,
        )
    )
    energy_ridge = nonvac & (rho >= energy_threshold)

    bfloor = max(float(np.max(baryon_abs)), 1.0e-300) * TOPOLOGY_REL_FLOOR
    topo_valid = baryon_abs > bfloor

    if int(np.count_nonzero(topo_valid)) < 100:
        raise RuntimeError("Topology-density support unexpectedly small")

    topo_threshold = float(
        np.quantile(
            baryon_abs[topo_valid],
            TOPOLOGY_RIDGE_QUANTILE,
        )
    )
    topology_ridge = topo_valid & (baryon_abs >= topo_threshold)

    energy_tree = cKDTree(centers[energy_ridge])
    topo_tree = cKDTree(centers[topology_ridge])

    distance_energy_ridge = energy_tree.query(
        centers,
        k=1,
        workers=-1,
    )[0]
    distance_topology_ridge = topo_tree.query(
        centers,
        k=1,
        workers=-1,
    )[0]

    return {
        "centers": centers,
        "phi": phi,
        "e2": e2,
        "e4": e4,
        "V": potential,
        "rho": rho,
        "S": active,
        "gradS": gradS,
        "sigma_plane_distance": sigma_plane_distance,
        "sigma_nearest_distance": sigma_nearest_distance,
        "strain_eig1": eig1,
        "strain_eig2": eig2,
        "strain_eig3": eig3,
        "strain_trace": trace,
        "strain_anisotropy": strain_anisotropy,
        "strain_eig_ratio": eig_ratio,
        "baryon_abs": baryon_abs,
        "distance_energy_ridge": distance_energy_ridge,
        "distance_topology_ridge": distance_topology_ridge,
        "nonvac": nonvac,
        "energy_ridge": energy_ridge,
        "topology_ridge": topology_ridge,
        "sigma_interface": interface.ravel(),
        "energy_ridge_threshold": energy_threshold,
        "topology_ridge_threshold": topo_threshold,
    }


def geometry_metric_table(
    label: str,
    energy_cell: np.ndarray,
    outward_cell: np.ndarray,
    geom: dict[str, np.ndarray],
):
    energy = np.maximum(np.asarray(energy_cell, dtype=float), 0.0)
    outward = np.maximum(np.asarray(outward_cell, dtype=float), 0.0)

    leverage = np.zeros_like(energy)
    good_energy = energy > max(float(np.max(energy)), 1.0) * 1.0e-15
    leverage[good_energy] = outward[good_energy] / energy[good_energy]

    mask50 = top_fraction_mask(
        energy,
        outward,
        0.50,
    )

    nonvac = geom["nonvac"] & good_energy

    metrics = {
        "radius": np.linalg.norm(geom["centers"], axis=1),
        "rho_center": geom["rho"],
        "S_center": geom["S"],
        "abs_S_center": np.abs(geom["S"]),
        "gradS": geom["gradS"],
        "sigma_plane_distance": geom["sigma_plane_distance"],
        "sigma_nearest_distance": geom["sigma_nearest_distance"],
        "distance_energy_ridge": geom["distance_energy_ridge"],
        "distance_topology_ridge": geom["distance_topology_ridge"],
        "baryon_abs": geom["baryon_abs"],
        "strain_eig1": geom["strain_eig1"],
        "strain_eig2": geom["strain_eig2"],
        "strain_eig3": geom["strain_eig3"],
        "strain_trace": geom["strain_trace"],
        "strain_anisotropy": geom["strain_anisotropy"],
        "strain_eig_ratio": geom["strain_eig_ratio"],
        "e4_over_V": geom["e4"] / np.maximum(geom["V"], 1.0e-15),
        "V_fraction_center": geom["V"] / np.maximum(geom["rho"], 1.0e-15),
        "e4_fraction_center": geom["e4"] / np.maximum(geom["rho"], 1.0e-15),
    }

    rows = []

    for name, values in metrics.items():
        x = np.asarray(values, dtype=float)

        p, s = safe_corr(
            np.log1p(np.maximum(leverage[nonvac], 0.0)),
            x[nonvac],
        )

        background_mean = weighted_mean(
            x[nonvac],
            energy[nonvac],
        )
        top_mean = weighted_mean(
            x[mask50],
            energy[mask50],
        )

        if abs(background_mean) > 1.0e-300:
            ratio = top_mean / background_mean
        else:
            ratio = float("nan")

        rows.append({
            "field": label,
            "metric": name,
            "pearson_log_leverage": p,
            "spearman_leverage": s,
            "energy_weighted_background_mean": background_mean,
            "top50_energy_weighted_mean": top_mean,
            "top50_to_background_ratio": ratio,
        })

    return rows, mask50, leverage


def exact_map_geometry(
    int02,
    a23,
    b23,
    direction: np.ndarray,
):
    degree, I = b23.angular_integrals_b7(
        b23.B7_B0
    )
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
    candidate = b23.candidate_from_sector(
        a23,
        sector_profiles,
        sector_energies,
        B,
    )

    xyz, energy_w, active_w, e4_w, v_w = int02.exact_map_weighted_source(
        b23,
        profile,
        b23.B7_B0,
        68,
        32,
        64,
    )

    h = float(candidate.payload.payload_center)
    rp = float(candidate.payload.payload_radius)
    center = h * direction

    q = xyz - center[None, :]
    d2 = np.sum(q * q, axis=1)
    d = np.sqrt(np.maximum(d2, 0.0))
    denom = np.where(
        d < rp,
        rp**3,
        np.maximum(d2 * d, 1.0e-300),
    )
    kernel = (q @ direction) / denom

    influence = active_w * kernel
    outward = np.maximum(influence, 0.0)

    leverage = np.zeros_like(energy_w)
    good = energy_w > max(float(np.max(energy_w)), 1.0) * 1.0e-15
    leverage[good] = outward[good] / energy_w[good]

    r = np.linalg.norm(xyz, axis=1)
    r_safe = np.maximum(r, 1.0e-300)
    mu = np.clip(xyz[:, 2] / r_safe, -1.0 + 1.0e-14, 1.0 - 1.0e-14)
    phi_angle = np.arctan2(xyz[:, 1], xyz[:, 0])

    t = np.sqrt((1.0 - mu) / (1.0 + mu))
    z = t * np.exp(1j * phi_angle)

    p, qq, pp, qprime = b23.b7_pq_and_derivatives(
        z,
        b23.B7_B0,
    )

    wronskian = np.abs(pp * qq - p * qprime)
    denominator = np.abs(p)**2 + np.abs(qq)**2

    J = (
        (1.0 + np.abs(z)**2)
        * wronskian
        / np.maximum(denominator, 1.0e-300)
    )

    mask50 = top_fraction_mask(
        energy_w,
        outward,
        0.50,
    )

    rows = []

    for name, values in {
        "J": J,
        "J2": J**2,
        "J4": J**4,
        "Wronskian_abs": wronskian,
        "radius": r,
    }.items():
        p_corr, s_corr = safe_corr(
            np.log1p(np.maximum(leverage[good], 0.0)),
            values[good],
        )

        bg = weighted_mean(values[good], energy_w[good])
        top = weighted_mean(values[mask50], energy_w[mask50])
        ratio = top / bg if abs(bg) > 1.0e-300 else float("nan")

        rows.append({
            "field": "EXACT_MAP",
            "metric": name,
            "pearson_log_leverage": p_corr,
            "spearman_leverage": s_corr,
            "energy_weighted_background_mean": bg,
            "top50_energy_weighted_mean": top,
            "top50_to_background_ratio": ratio,
        })

    return {
        "degree": float(degree),
        "I": float(I),
        "payload_center": h,
        "payload_radius": rp,
        "net_force": float(np.sum(influence)),
        "F50_energy_fraction": float(np.sum(energy_w[mask50]) / np.sum(energy_w)),
        "rows": rows,
    }


def main() -> None:
    print(
        "=== INT-03/04G — GEOMETRY CAUSATION + EXPANSION SIGNATURE ===",
        flush=True,
    )

    require(INT03S_SOURCE)
    require(INT03S_SUMMARY)

    prior = json.loads(INT03S_SUMMARY.read_text())

    expected = (
        "SCALE_ROBUST_PRODUCTIVE_ANATOMY_WITH_NONSTATIONARY_DILATION_"
        "AND_REEQUILIBRATED_EXACT_MAP_SUPPORT"
    )
    if prior.get("decision") != expected:
        raise RuntimeError(
            "INT-03/04S result does not authorize geometry follow-up"
        )

    int03s = load_module(
        "int04g_int03s",
        INT03S_SOURCE,
    )
    int02 = load_module(
        "int04g_int02",
        int03s.INT02_SOURCE,
    )
    int01 = load_module(
        "int04g_int01",
        int02.INT01_SOURCE,
    )
    c2aqs = load_module(
        "int04g_c2aqs",
        int01.C2AQS_SOURCE,
    )
    aqr = load_module(
        "int04g_aqr",
        c2aqs.AQR_SOURCE,
    )
    c2aq = aqr.load_module(
        "int04g_c2aq",
        aqr.C2AQ_SOURCE,
    )
    cr3 = c2aq.load_module(
        "int04g_cr3",
        c2aq.CR3_SOURCE,
    )

    a23_path = SIM / "023a_topological_false_core_multiskyrmion_gr_repulsion_gate.py"
    b23_path = SIM / "023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.py"

    require(a23_path)
    require(b23_path)

    a23 = load_module("int04g_a23", a23_path)
    b23 = load_module("int04g_b23", b23_path)

    # ---------------------------------------------------------------
    # A. strict N65 state audit
    # ---------------------------------------------------------------
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

    if grad_rms > int01.GRAD_RMS_TOL or grad_max > int01.GRAD_MAX_TOL:
        raise RuntimeError("N65 stationarity audit failed")

    direction = np.asarray(
        c2aq.KNOWN_WORST_DIRECTION,
        dtype=float,
    )
    direction /= np.linalg.norm(direction)

    h0 = float(c2aq.PAYLOAD_CENTER)
    rp0 = float(c2aq.PAYLOAD_RADIUS)

    # ---------------------------------------------------------------
    # B. continuous field + two force ledgers
    # ---------------------------------------------------------------
    print("\n=== B — QUINTIC FIELD + FORCE LEDGERS ===", flush=True)

    quintic = c2aqs.build_interpolator(
        axis,
        phi,
        "quintic",
    )
    print("QUINTIC_INTERPOLATOR=READY", flush=True)

    lowers, ledgers = reconstruct_scaled_ledgers(
        int03s,
        int01,
        c2aqs,
        quintic,
        axis,
        dx,
        direction,
        h0,
        rp0,
    )

    E2_cell = ledgers["E2_cell"]
    E4_cell = ledgers["E4_cell"]
    V_cell = ledgers["V_cell"]

    energy_ref = E2_cell + E4_cell + V_cell
    energy_exp = (
        LAMBDA_EXPANDED * E2_cell
        + E4_cell / LAMBDA_EXPANDED
        + LAMBDA_EXPANDED**3 * V_cell
    )

    net_ref_cell = ledgers["net"][0]
    net_exp_cell = ledgers["net"][1]
    out_ref_cell = ledgers["outward"][0]
    out_exp_cell = ledgers["outward"][1]

    net_ref = float(np.sum(net_ref_cell))
    net_exp = float(np.sum(net_exp_cell))

    Ae4_ref = float(ledgers["e4_force"][0])
    AV_ref = float(ledgers["v_force"][0])

    analytic_exp = (
        Ae4_ref / LAMBDA_EXPANDED**3
        + LAMBDA_EXPANDED * AV_ref
    )

    exp_close_abs = abs(net_exp - analytic_exp)
    exp_close_rel = relerr(net_exp, analytic_exp)

    print(f"REFERENCE_NET_FORCE={net_ref:.15e}")
    print(f"EXPANDED_NET_FORCE={net_exp:.15e}")
    print(f"EXPANDED_ANALYTIC_FORCE={analytic_exp:.15e}")
    print(f"EXPANDED_FORCE_CLOSE_ABS={exp_close_abs:.15e}")
    print(f"EXPANDED_FORCE_CLOSE_REL={exp_close_rel:.15e}")
    print(
        f"EXPANDED_OVER_REFERENCE_FORCE_RATIO="
        f"{net_exp/max(abs(net_ref),1.0e-300):.15e}"
    )

    if (
        exp_close_abs > FORCE_CLOSE_ABS
        and exp_close_rel > FORCE_CLOSE_REL
    ):
        raise RuntimeError(
            "Expansion force failed analytic scaling closure"
        )

    # ---------------------------------------------------------------
    # C. field geometry on source-cell centers
    # ---------------------------------------------------------------
    print("\n=== C — LOCAL GEOMETRY RECONSTRUCTION ===", flush=True)

    geom = cell_center_geometry(
        int01,
        quintic,
        lowers,
        dx,
    )

    print(
        f"ENERGY_RIDGE_THRESHOLD="
        f"{geom['energy_ridge_threshold']:.15e}"
    )
    print(
        f"TOPOLOGY_RIDGE_THRESHOLD="
        f"{geom['topology_ridge_threshold']:.15e}"
    )
    print(
        f"SIGMA0_INTERFACE_CELL_COUNT="
        f"{int(np.count_nonzero(geom['sigma_interface']))}"
    )

    corr_ref, mask50_ref, leverage_ref = geometry_metric_table(
        "N65_STATIONARY",
        energy_ref,
        out_ref_cell,
        geom,
    )

    corr_exp, mask50_exp, leverage_exp = geometry_metric_table(
        "N65_EXPANDED_LAMBDA_1P25_DIAGNOSTIC",
        energy_exp,
        out_exp_cell,
        geom,
    )

    overlap = weighted_jaccard(
        mask50_ref,
        mask50_exp,
        0.5 * (energy_ref + energy_exp),
    )

    print(
        f"STATIONARY_EXPANDED_TOP50_WEIGHTED_JACCARD="
        f"{overlap:.15e}"
    )

    # ---------------------------------------------------------------
    # D. expansion gain sectors
    # ---------------------------------------------------------------
    print("\n=== D — EXPANSION GAIN SOURCE-SIGN SECTORS ===")

    delta = net_exp_cell - net_ref_cell
    positive_gain = np.maximum(delta, 0.0)

    S1 = geom["S"]
    Sexp = 2.0 * (
        geom["e4"] / LAMBDA_EXPANDED**4
        - geom["V"]
    )

    sector_defs = {
        "SPLUS_TO_SPLUS": (S1 >= 0.0) & (Sexp >= 0.0),
        "SPLUS_TO_SMINUS": (S1 >= 0.0) & (Sexp < 0.0),
        "SMINUS_TO_SPLUS": (S1 < 0.0) & (Sexp >= 0.0),
        "SMINUS_TO_SMINUS": (S1 < 0.0) & (Sexp < 0.0),
    }

    total_positive_gain = float(np.sum(positive_gain))
    total_signed_gain = float(np.sum(delta))

    gain_rows = []

    for name, mask in sector_defs.items():
        signed = float(np.sum(delta[mask]))
        pos = float(np.sum(positive_gain[mask]))
        eref = float(np.sum(energy_ref[mask]))

        row = {
            "sector": name,
            "cell_count": int(np.count_nonzero(mask)),
            "reference_energy_fraction": eref / max(float(np.sum(energy_ref)), 1.0e-300),
            "signed_force_gain": signed,
            "signed_force_gain_fraction": signed / max(abs(total_signed_gain), 1.0e-300),
            "positive_force_gain": pos,
            "positive_force_gain_fraction": pos / max(total_positive_gain, 1.0e-300),
        }
        gain_rows.append(row)

        print(
            f"GAIN_SECTOR={name} "
            f"ENERGY_FRAC={row['reference_energy_fraction']:.9e} "
            f"SIGNED_GAIN={signed:.9e} "
            f"POS_GAIN={pos:.9e} "
            f"POS_GAIN_SHARE={row['positive_force_gain_fraction']:.9e}"
        )

    gain50 = top_fraction_mask(
        energy_ref,
        positive_gain,
        0.50,
    )
    gain50_energy_fraction = float(
        np.sum(energy_ref[gain50])
        / max(float(np.sum(energy_ref)), 1.0e-300)
    )

    gain50_overlap_stationary = weighted_jaccard(
        gain50,
        mask50_ref,
        energy_ref,
    )

    print(f"EXPANSION_GAIN_F50={gain50_energy_fraction:.15e}")
    print(
        f"EXPANSION_GAIN50_STATIONARY_TOP50_WEIGHTED_JACCARD="
        f"{gain50_overlap_stationary:.15e}"
    )

    # ---------------------------------------------------------------
    # E. exact map angular geometry comparator
    # ---------------------------------------------------------------
    print("\n=== E — EXACT-MAP ANGULAR GEOMETRY COMPARATOR ===")

    exact = exact_map_geometry(
        int02,
        a23,
        b23,
        direction,
    )

    print(f"EXACT_MAP_DEGREE={exact['degree']:.15e}")
    print(f"EXACT_MAP_I={exact['I']:.15e}")
    print(f"EXACT_MAP_NET_FORCE={exact['net_force']:.15e}")
    print(
        f"EXACT_MAP_F50_ENERGY_FRACTION="
        f"{exact['F50_energy_fraction']:.15e}"
    )

    for row in exact["rows"]:
        print(
            f"EXACT_GEOMETRY_METRIC={row['metric']} "
            f"PEARSON={row['pearson_log_leverage']:.9e} "
            f"SPEARMAN={row['spearman_leverage']:.9e} "
            f"TOP50_RATIO={row['top50_to_background_ratio']:.9e}"
        )

    # ---------------------------------------------------------------
    # F. classify strongest declared signatures
    # ---------------------------------------------------------------
    all_corr_rows = corr_ref + corr_exp + exact["rows"]

    ref_by_metric = {
        row["metric"]: row
        for row in corr_ref
    }
    exp_by_metric = {
        row["metric"]: row
        for row in corr_exp
    }
    exact_by_metric = {
        row["metric"]: row
        for row in exact["rows"]
    }

    # Rank the stationary unrestricted metrics by absolute Spearman magnitude.
    ranked = sorted(
        [
            (
                name,
                abs(float(row["spearman_leverage"]))
                if math.isfinite(float(row["spearman_leverage"]))
                else -1.0,
                float(row["spearman_leverage"]),
                float(row["top50_to_background_ratio"]),
            )
            for name, row in ref_by_metric.items()
        ],
        key=lambda x: x[1],
        reverse=True,
    )

    print("\n=== F — STRONGEST STATIONARY GEOMETRY SIGNATURES ===")
    for rank, item in enumerate(ranked[:8], start=1):
        name, _absr, signedr, ratio = item
        print(
            f"GEOMETRY_RANK={rank} "
            f"METRIC={name} "
            f"SPEARMAN={signedr:.9e} "
            f"TOP50_RATIO={ratio:.9e}"
        )

    # Reproducibility test: at least one unrestricted metric has |rho_s|>=0.25
    # with same sign in stationary and expanded diagnostic.
    reproducible_metrics = []

    for name in ref_by_metric:
        if name not in exp_by_metric:
            continue

        r1 = float(ref_by_metric[name]["spearman_leverage"])
        r2 = float(exp_by_metric[name]["spearman_leverage"])

        if (
            math.isfinite(r1)
            and math.isfinite(r2)
            and abs(r1) >= 0.25
            and abs(r2) >= 0.25
            and r1 * r2 > 0.0
        ):
            reproducible_metrics.append(name)

    # Independent exact-map angular signal is considered nontrivial at |rho_s|>=0.20.
    exact_nontrivial = [
        name
        for name, row in exact_by_metric.items()
        if (
            math.isfinite(float(row["spearman_leverage"]))
            and abs(float(row["spearman_leverage"])) >= 0.20
        )
    ]

    geometry_signal = bool(reproducible_metrics or exact_nontrivial)

    if geometry_signal:
        decision = (
            "GEOMETRY_SIGNATURE_IDENTIFIED_FOR_SOURCE_BOUND_TARGETING"
        )
        next_action = (
            "INT08_SOURCE_LEVEL_CONSERVATION_AWARE_HEADROOM_BOUND_"
            "WITH_GEOMETRY_SIGNATURE_CONSTRAINTS"
        )
    else:
        decision = (
            "NO_SIMPLE_LOCAL_GEOMETRY_SIGNATURE_FOUND"
        )
        next_action = (
            "INT06_MULTIPOLE_SPECTRAL_ANATOMY_BEFORE_SOURCE_BOUND"
        )

    print("\n=== G — INT-03/04G DECISION ===")
    print(
        "REPRODUCIBLE_UNRESTRICTED_GEOMETRY_METRICS="
        + (
            ",".join(reproducible_metrics)
            if reproducible_metrics
            else "NONE"
        )
    )
    print(
        "NONTRIVIAL_EXACT_MAP_GEOMETRY_METRICS="
        + (
            ",".join(exact_nontrivial)
            if exact_nontrivial
            else "NONE"
        )
    )
    print(
        f"INT03_04G_GEOMETRY_SIGNAL="
        f"{'PASS' if geometry_signal else 'FAIL'}"
    )
    print(f"INT03_04G_DECISION={decision}")
    print(
        "EXPANSION_HUNDREDS_FOLD_HEADROOM_STATUS="
        "PRESERVED_AS_NONSTATIONARY_MECHANISM_CLUE"
    )
    print(
        "LAMBDA_1P25_PHYSICAL_STATIONARY_CONFIGURATION=NO"
    )
    print(
        "INT_LEVEL_2="
        "NOT_YET_REQUIRES_FINE_RESOLUTION_UNRESTRICTED_SUPPORT"
    )
    print(
        "INT_LEVEL_3="
        "NOT_YET_REQUIRES_CONSERVATION_AWARE_GE10X_HEADROOM_OR_CONTINUABLE_DIRECTION"
    )
    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "APPROXIMATELY_70_TO_71_PERCENT_NOT_A_PROBABILITY"
    )
    print(f"NEXT={next_action}")
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_INT03_04G_GEOMETRY_CAUSATION_EXPANSION_SIGNATURE"
    )

    # ---------------------------------------------------------------
    # H. save machine-readable results
    # ---------------------------------------------------------------
    with OUT_CORR.open("w", newline="") as f:
        fields = [
            "field",
            "metric",
            "pearson_log_leverage",
            "spearman_leverage",
            "energy_weighted_background_mean",
            "top50_energy_weighted_mean",
            "top50_to_background_ratio",
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_corr_rows)

    with OUT_GAIN.open("w", newline="") as f:
        fields = list(gain_rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(gain_rows)

    np.savez_compressed(
        OUT_NPZ,
        centers=geom["centers"],
        rho=geom["rho"],
        S=geom["S"],
        gradS=geom["gradS"],
        sigma_plane_distance=geom["sigma_plane_distance"],
        sigma_nearest_distance=geom["sigma_nearest_distance"],
        distance_energy_ridge=geom["distance_energy_ridge"],
        distance_topology_ridge=geom["distance_topology_ridge"],
        baryon_abs=geom["baryon_abs"],
        strain_eig1=geom["strain_eig1"],
        strain_eig2=geom["strain_eig2"],
        strain_eig3=geom["strain_eig3"],
        strain_anisotropy=geom["strain_anisotropy"],
        leverage_stationary=leverage_ref,
        leverage_expanded=leverage_exp,
        top50_stationary=mask50_ref,
        top50_expanded=mask50_exp,
        expansion_gain=delta,
        expansion_positive_gain=positive_gain,
        expansion_gain50=gain50,
    )

    summary = {
        "claim_classification": (
            "PROJECT_DERIVED_INT03_04G_GEOMETRY_CAUSATION_EXPANSION_SIGNATURE"
        ),
        "decision": decision,
        "next": next_action,
        "reference": {
            "net_force": net_ref,
            "payload_center": h0,
            "payload_radius": rp0,
            "direction": [float(x) for x in direction],
        },
        "expanded_diagnostic": {
            "lambda": LAMBDA_EXPANDED,
            "net_force": net_exp,
            "analytic_force": analytic_exp,
            "force_close_abs": exp_close_abs,
            "force_close_rel": exp_close_rel,
            "force_ratio_to_reference": net_exp / max(abs(net_ref), 1.0e-300),
            "top50_weighted_jaccard_to_stationary": overlap,
            "gain_F50_energy_fraction": gain50_energy_fraction,
            "gain50_stationary_top50_weighted_jaccard": (
                gain50_overlap_stationary
            ),
            "gain_sectors": gain_rows,
            "stationary": False,
        },
        "stationary_geometry_correlations": corr_ref,
        "expanded_geometry_correlations": corr_exp,
        "exact_map": exact,
        "reproducible_unrestricted_metrics": reproducible_metrics,
        "nontrivial_exact_map_metrics": exact_nontrivial,
        "gates": {
            "geometry_signal": geometry_signal,
            "force_scaling_closure": (
                exp_close_abs <= FORCE_CLOSE_ABS
                or exp_close_rel <= FORCE_CLOSE_REL
            ),
        },
        "claim_limits": {
            "expanded_field_stationary": False,
            "source_mask_physical": False,
            "int_level_2": False,
            "int_level_3": False,
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

    print(f"INT03_04G_SUMMARY_JSON={OUT_JSON}")
    print(f"INT03_04G_CORRELATIONS_CSV={OUT_CORR}")
    print(f"INT03_04G_GAIN_SECTORS_CSV={OUT_GAIN}")
    print(f"INT03_04G_ARRAYS_NPZ={OUT_NPZ}")
    print("INT03_04G_RUN_COMPLETE=YES")


if __name__ == "__main__":
    main()
