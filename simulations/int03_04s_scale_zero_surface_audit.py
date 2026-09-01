#!/usr/bin/env python3
"""INT-03/04S — scale, zero-surface, and re-equilibrated size audit.

PURPOSE
-------
Test whether the productive gravitational anatomy isolated by INT-01/INT-02
persists under controlled changes of source size.

This run deliberately separates:

1. HOMOTHETIC DILATION of the strict unrestricted N=65 field.
   This is a diagnostic deformation. Except at the reference point it is NOT
   a new stationary field-equation solution.

2. RE-EQUILIBRATED exact-rational-map changes of m at 0.8, 1.0, and 1.2 of
   the selected value. These re-solve the field equations and therefore are
   genuinely different equilibrium profiles within the same model class.

REFERENCE MODEL
---------------
B = 7
eta = 0.4
m = 8

Static energy:

    E = E2 + E4 + V

Static active source:

    S = 2(e4 - V)

Under phi_lambda(x) = phi(x/lambda):

    E2(lambda) = lambda E2
    E4(lambda) = E4 / lambda
    V(lambda) = lambda^3 V

and

    dE/dlambda = E2 - E4/lambda^2 + 3 lambda^2 V.

If payload center and radius scale by the same lambda, then

    K(lambda) = K(1) / lambda^2

so

    A_e4(lambda) = A_e4(1) / lambda^3
    A_V(lambda)  = lambda A_V(1)

and

    A(lambda) = A_e4(1)/lambda^3 + lambda A_V(1).

The active-source zero surface obeys

    Sigma_0(lambda): e4/lambda^4 = V.

OUTPUTS
-------
results/data/int03_04s_scale_zero_surface_summary.json
results/data/int03_04s_n65_scale_scan.csv
results/data/int03_04s_exactmap_m_scan.csv

CLAIM LIMITS
------------
This is a static scale-mode audit, not a radiation/emission calculation.
Homothetic dilation away from lambda=1 is diagnostic only.
No practical-device claim is authorized.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_INT03_04S_SCALE_ZERO_SURFACE_AUDIT
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
from typing import Any

import numpy as np
from scipy.ndimage import distance_transform_edt, generate_binary_structure, label
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

INT02_SOURCE = SIM / "int02_signed_kernel_orientation_robustness.py"
INT02_SUMMARY = DATA / "int02_signed_kernel_orientation_robustness_summary.json"

OUT_JSON = DATA / "int03_04s_scale_zero_surface_summary.json"
OUT_SCALE_CSV = DATA / "int03_04s_n65_scale_scan.csv"
OUT_M_CSV = DATA / "int03_04s_exactmap_m_scan.csv"

B = 7
ETA = 0.40
M0 = 8.0

MAX_BATCH_POINTS = max(20000, int(os.environ.get("AG_INT03S_BATCH_POINTS", "120000")))

MAIN_LAMBDAS = (0.75, 0.875, 0.95, 0.975, 1.0, 1.025, 1.05, 1.125, 1.25)
WILDCARD_LAMBDAS = (0.625, 1.6)
M_MULTIPLIERS = (0.8, 1.0, 1.2)

STRONG_F50_MAX = 0.10
FORCE_SCALING_REL_TOL = 5.0e-10


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


def concentration_metrics(energy: np.ndarray, outward: np.ndarray) -> dict[str, Any]:
    energy = np.maximum(np.asarray(energy, dtype=float), 0.0)
    outward = np.maximum(np.asarray(outward, dtype=float), 0.0)

    E = float(np.sum(energy))
    Aplus = float(np.sum(outward))

    leverage = np.zeros_like(energy)
    floor = max(float(np.max(energy)), 1.0) * 1.0e-15
    good = energy > floor
    leverage[good] = outward[good] / energy[good]

    order = np.argsort(leverage)[::-1]
    cum_e = np.cumsum(energy[order]) / max(E, 1.0e-300)
    cum_o = np.cumsum(outward[order]) / max(Aplus, 1.0e-300)

    def fq(q: float) -> float:
        idx = int(np.searchsorted(cum_o, q, side="left"))
        idx = min(idx, len(order) - 1)
        return float(cum_e[idx])

    mean1 = float(np.sum(energy * leverage) / max(E, 1.0e-300))
    mean2 = float(np.sum(energy * leverage * leverage) / max(E, 1.0e-300))
    fpart = mean1 * mean1 / mean2 if mean2 > 0.0 else float("nan")

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
    }


def block_scaled_ledgers(
    int01,
    interp,
    lowers: np.ndarray,
    offsets: np.ndarray,
    weights: np.ndarray,
    center0: np.ndarray,
    direction: np.ndarray,
    radius0: float,
    lambdas: np.ndarray,
):
    nq = len(weights)
    ncell = len(lowers)
    nl = len(lambdas)

    E2_cell = np.zeros(ncell)
    E4_cell = np.zeros(ncell)
    V_cell = np.zeros(ncell)

    net = np.zeros((nl, ncell))
    outward = np.zeros((nl, ncell))

    qplus = np.zeros(nl)
    qminus = np.zeros(nl)
    neg_volume = np.zeros(nl)
    total_volume = np.zeros(nl)

    sectors = np.zeros((nl, 4))
    e4_force = np.zeros(nl)
    v_force = np.zeros(nl)

    cells_per_batch = max(1, MAX_BATCH_POINTS // max(nq, 1))

    for start in range(0, ncell, cells_per_batch):
        stop = min(start + cells_per_batch, ncell)
        lo = lowers[start:stop]
        pts = (lo[:, None, :] + offsets[None, :, :]).reshape(-1, 3)

        (
            _phi,
            _qx,
            _qy,
            _qz,
            e2,
            e4,
            potential,
            _rho,
            _active,
        ) = int01.independent_terms(interp, pts)

        kernel0 = int01.independent_kernel(
            pts,
            center0,
            direction,
            radius0,
        )

        nc = len(lo)
        w = np.broadcast_to(weights[None, :], (nc, nq))

        e2r = e2.reshape(nc, nq)
        e4r = e4.reshape(nc, nq)
        vr = potential.reshape(nc, nq)
        kr = kernel0.reshape(nc, nq)

        E2_cell[start:stop] = np.sum(e2r * w, axis=1)
        E4_cell[start:stop] = np.sum(e4r * w, axis=1)
        V_cell[start:stop] = np.sum(vr * w, axis=1)

        for il, lam in enumerate(lambdas):
            active_density = 2.0 * (e4r / lam**4 - vr)
            transformed_weight = lam**3 * w
            kernel_lam = kr / lam**2
            influence = active_density * kernel_lam

            net[il, start:stop] = np.sum(influence * transformed_weight, axis=1)
            outward[il, start:stop] = np.sum(
                np.maximum(influence, 0.0) * transformed_weight,
                axis=1,
            )

            qplus[il] += float(
                np.sum(np.maximum(active_density, 0.0) * transformed_weight)
            )
            qminus[il] += float(
                np.sum(np.maximum(-active_density, 0.0) * transformed_weight)
            )
            neg_volume[il] += float(
                np.sum((active_density < 0.0) * transformed_weight)
            )
            total_volume[il] += float(np.sum(transformed_weight))

            sp = np.maximum(active_density, 0.0)
            sn = np.maximum(-active_density, 0.0)
            kp = np.maximum(kernel_lam, 0.0)
            kn = np.maximum(-kernel_lam, 0.0)

            sectors[il, 0] += float(np.sum(sp * kp * transformed_weight))
            sectors[il, 1] += float(np.sum(sp * kn * transformed_weight))
            sectors[il, 2] += float(np.sum(sn * kp * transformed_weight))
            sectors[il, 3] += float(np.sum(sn * kn * transformed_weight))

            e4_force[il] += float(
                np.sum(
                    2.0 * (e4r / lam**4)
                    * kernel_lam
                    * transformed_weight
                )
            )
            v_force[il] += float(
                np.sum(-2.0 * vr * kernel_lam * transformed_weight)
            )

    return {
        "E2_cell": E2_cell,
        "E4_cell": E4_cell,
        "V_cell": V_cell,
        "net": net,
        "outward": outward,
        "qplus": qplus,
        "qminus": qminus,
        "neg_volume": neg_volume,
        "total_volume": total_volume,
        "sectors": sectors,
        "e4_force": e4_force,
        "v_force": v_force,
    }


def zero_surface_cell_metrics(
    e4_center: np.ndarray,
    v_center: np.ndarray,
    energy_cell: np.ndarray,
    top50: np.ndarray,
    lam: float,
    dx: float,
    nside: int,
):
    sgn = (e4_center / lam**4 - v_center) >= 0.0
    cube = sgn.reshape((nside, nside, nside))

    interface = np.zeros_like(cube, dtype=bool)

    for ax in range(3):
        sl0 = [slice(None)] * 3
        sl1 = [slice(None)] * 3
        sl0[ax] = slice(0, nside - 1)
        sl1[ax] = slice(1, nside)

        a = cube[tuple(sl0)]
        b = cube[tuple(sl1)]
        change = a != b

        interface[tuple(sl0)] |= change
        interface[tuple(sl1)] |= change

    if np.any(interface):
        dist = distance_transform_edt(~interface, sampling=dx * lam).ravel()
    else:
        dist = np.full(nside**3, np.nan)

    top = top50.astype(bool)
    top_energy = np.maximum(energy_cell[top], 0.0)
    top_dist = dist[top]

    if len(top_dist) and np.all(np.isfinite(top_dist)):
        mean_dist = float(
            np.sum(top_energy * top_dist)
            / max(float(np.sum(top_energy)), 1.0e-300)
        )
        median_dist = float(np.median(top_dist))
    else:
        mean_dist = float("nan")
        median_dist = float("nan")

    top_cube = top.reshape((nside, nside, nside))
    structure = generate_binary_structure(3, 1)
    labels, ncomp = label(top_cube, structure=structure)

    component_energy = []
    flat_labels = labels.ravel()

    for ic in range(1, ncomp + 1):
        mask = flat_labels == ic
        component_energy.append(float(np.sum(energy_cell[mask])))

    if component_energy:
        largest_fraction = max(component_energy) / max(
            float(np.sum(energy_cell[top])),
            1.0e-300,
        )
    else:
        largest_fraction = float("nan")

    return {
        "sigma0_interface_cells": int(np.count_nonzero(interface)),
        "top50_mean_distance_to_sigma0": mean_dist,
        "top50_median_distance_to_sigma0": median_dist,
        "top50_connected_components": int(ncomp),
        "top50_largest_component_energy_fraction": float(largest_fraction),
    }


def solve_homothetic_energy_minimum(E2: float, E4: float, V: float) -> float:
    def derivative(lam):
        return E2 - E4 / lam**2 + 3.0 * lam**2 * V

    grid = np.geomspace(0.2, 5.0, 200)
    values = [derivative(x) for x in grid]

    for a, b, fa, fb in zip(grid[:-1], grid[1:], values[:-1], values[1:]):
        if fa == 0.0:
            return float(a)
        if fa * fb < 0.0:
            return float(brentq(derivative, a, b))

    return float("nan")


def run_exact_m_scan(int02, a23, b23, direction: np.ndarray):
    rows = []

    for mult in M_MULTIPLIERS:
        m = M0 * mult

        print(
            f"\nEXACT_M_SCAN_BEGIN MULT={mult:.6f} M={m:.9e}",
            flush=True,
        )

        profiles, energies = b23.solve_exact_sector(a23, ETA, m)

        if not all(p.success for p in profiles.values()):
            rows.append({
                "m_multiplier": float(mult),
                "m": float(m),
                "success": False,
            })
            print(f"EXACT_M_SCAN_SUCCESS_M{mult:.3f}=NO")
            continue

        candidate = b23.candidate_from_sector(a23, profiles, energies, B)
        profile = candidate.profile
        payload = candidate.payload

        xyz, energy_w, active_w, e4_w, v_w = int02.exact_map_weighted_source(
            b23,
            profile,
            b23.B7_B0,
            68,
            32,
            64,
        )

        metrics = int02.exact_map_case_metrics(
            xyz,
            energy_w,
            active_w,
            e4_w,
            v_w,
            direction,
            float(payload.payload_center),
            float(payload.payload_radius),
        )

        eta_op = (
            float(payload.payload_center) ** 2
            * float(metrics["net"])
            / max(float(np.sum(energy_w)), 1.0e-300)
        )

        tail_length = 1.0 / (m * math.sqrt(1.0 + ETA))

        row = {
            "m_multiplier": float(mult),
            "m": float(m),
            "success": True,
            "shell_radius": float(profile.shell_radius),
            "negative_active_outer_radius": float(profile.negative_active_outer_radius),
            "tail_length": float(tail_length),
            "profile_energy_4pi": float(4.0 * math.pi * profile.E),
            "quadrature_energy": float(np.sum(energy_w)),
            "virial_relerr": float(profile.virial_relerr),
            "active_total_relerr": float(profile.active_total_relerr),
            "min_active_fraction": float(profile.min_active_fraction),
            "fission_margin": float(candidate.fission_margin),
            "payload_center": float(payload.payload_center),
            "payload_radius": float(payload.payload_radius),
            "payload_coefficient_c": float(payload.payload_coefficient_c),
            "net_force": float(metrics["net"]),
            "F50": float(metrics["F50"]),
            "F90": float(metrics["F90"]),
            "f_part": float(metrics["f_part"]),
            "cancellation": float(metrics["cancellation"]),
            "e4_force": float(metrics["e4_force"]),
            "V_force": float(metrics["V_force"]),
            "eta_op": float(eta_op),
        }
        rows.append(row)

        print(
            f"EXACT_M_CASE MULT={mult:.3f} "
            f"SHELL_R={row['shell_radius']:.9e} "
            f"NEG_OUTER_R={row['negative_active_outer_radius']:.9e} "
            f"PAYLOAD_C={row['payload_center']:.9e} "
            f"FORCE={row['net_force']:.9e} "
            f"F50={row['F50']:.9e} "
            f"ETA_OP={row['eta_op']:.9e} "
            f"VIRIAL={row['virial_relerr']:.9e} "
            f"FISSION={row['fission_margin']:.9e}",
            flush=True,
        )

    return rows


def main() -> None:
    print("=== INT-03/04S — SCALE + ZERO-SURFACE AUDIT ===", flush=True)

    require(INT02_SOURCE)
    require(INT02_SUMMARY)

    int02_summary = json.loads(INT02_SUMMARY.read_text())

    if int02_summary.get("decision") != (
        "ROBUST_MECHANISM_SIGNAL_WITH_CONTINUUM_VIRIAL_WARNING"
    ):
        raise RuntimeError(
            "INT-02 result does not authorize this scale/anatomy follow-up"
        )

    int02 = load_module("int03s_int02", INT02_SOURCE)
    int01 = load_module("int03s_int01", int02.INT01_SOURCE)
    c2aqs = load_module("int03s_c2aqs", int01.C2AQS_SOURCE)
    aqr = load_module("int03s_aqr", c2aqs.AQR_SOURCE)
    c2aq = aqr.load_module("int03s_c2aq", aqr.C2AQ_SOURCE)
    cr3 = c2aq.load_module("int03s_cr3", c2aq.CR3_SOURCE)

    a23_path = SIM / "023a_topological_false_core_multiskyrmion_gr_repulsion_gate.py"
    b23_path = SIM / "023b_exact_rational_map_full3d_tmunu_gravity_promotion_gate.py"

    require(a23_path)
    require(b23_path)

    a23 = load_module("int03s_a23", a23_path)
    b23 = load_module("int03s_b23", b23_path)

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
    print(
        "N65_DISCRETE_VIRIAL_OVER_E="
        f"{(E2disc-E4disc+3.0*Vdisc)/Edisc:.15e}"
    )

    if grad_rms > int01.GRAD_RMS_TOL or grad_max > int01.GRAD_MAX_TOL:
        raise RuntimeError("Strict N65 stationarity audit failed")

    direction = np.asarray(c2aq.KNOWN_WORST_DIRECTION, dtype=float)
    direction /= np.linalg.norm(direction)

    h0 = float(c2aq.PAYLOAD_CENTER)
    rp0 = float(c2aq.PAYLOAD_RADIUS)
    center0 = h0 * direction

    lambdas = np.asarray(
        tuple(sorted(set(MAIN_LAMBDAS + WILDCARD_LAMBDAS))),
        dtype=float,
    )
    wildcard_set = set(WILDCARD_LAMBDAS)

    print("\n=== B — HOMOTHETIC SCALE GRID ===")
    for lam in lambdas:
        print(
            f"LAMBDA={lam:.9f} "
            f"CATEGORY={'BLIND_WILDCARD' if lam in wildcard_set else 'MAIN'}"
        )

    quintic = c2aqs.build_interpolator(axis, phi, "quintic")
    print("QUINTIC_INTERPOLATOR=READY")

    all_lowers = c2aqs.cell_lowers(axis)
    nside = len(axis) - 1

    q4_offsets, q4_weights = c2aqs.composite_gauss_offsets(dx, 4, 1)

    print("\n=== C — GLOBAL SCALE LEDGER ===", flush=True)
    global_result = block_scaled_ledgers(
        int01,
        quintic,
        all_lowers,
        q4_offsets,
        q4_weights,
        center0,
        direction,
        rp0,
        lambdas,
    )

    dmin = c2aqs.min_distance_to_cells(all_lowers, dx, center0)
    near_mask = dmin < c2aqs.NEAR_RADIUS_DX * dx
    near_ids = np.flatnonzero(near_mask)
    near_lowers = all_lowers[near_mask]

    near_offsets, near_weights = c2aqs.composite_gauss_offsets(
        dx,
        c2aqs.NEAR_GAUSS_ORDER,
        c2aqs.NEAR_FINE_SUBDIV,
    )

    old_near = block_scaled_ledgers(
        int01,
        quintic,
        near_lowers,
        q4_offsets,
        q4_weights,
        center0,
        direction,
        rp0,
        lambdas,
    )
    new_near = block_scaled_ledgers(
        int01,
        quintic,
        near_lowers,
        near_offsets,
        near_weights,
        center0,
        direction,
        rp0,
        lambdas,
    )

    for key in ("net", "outward"):
        global_result[key][:, near_ids] = new_near[key]

    for key in (
        "qplus",
        "qminus",
        "neg_volume",
        "total_volume",
        "sectors",
        "e4_force",
        "v_force",
    ):
        global_result[key] += new_near[key] - old_near[key]

    E2_0 = float(np.sum(global_result["E2_cell"]))
    E4_0 = float(np.sum(global_result["E4_cell"]))
    V_0 = float(np.sum(global_result["V_cell"]))

    lambda_energy_min = solve_homothetic_energy_minimum(E2_0, E4_0, V_0)

    centers_ref = all_lowers + 0.5 * dx
    (
        _p,
        _qx,
        _qy,
        _qz,
        _e2_center,
        e4_center,
        v_center,
        _rho_center,
        _s_center,
    ) = int01.independent_terms(quintic, centers_ref)

    print("\n=== D — SCALE RESULTS ===")

    scale_rows = []
    max_force_scaling_relerr = 0.0

    i1 = int(np.where(np.isclose(lambdas, 1.0))[0][0])
    Ae4_1 = float(global_result["e4_force"][i1])
    AV_1 = float(global_result["v_force"][i1])

    if Ae4_1 < 0.0 and AV_1 > 0.0:
        lambda_force_zero = float((-Ae4_1 / AV_1) ** 0.25)
    else:
        lambda_force_zero = float("nan")

    for il, lam in enumerate(lambdas):
        energy_cell = (
            lam * global_result["E2_cell"]
            + global_result["E4_cell"] / lam
            + lam**3 * global_result["V_cell"]
        )
        E = float(np.sum(energy_cell))

        net_cell = global_result["net"][il]
        out_cell = global_result["outward"][il]

        net = float(np.sum(net_cell))
        outward = float(np.sum(out_cell))
        opposing = float(np.sum(out_cell - net_cell))
        cancellation = (outward + opposing) / max(abs(net), 1.0e-300)

        conc = concentration_metrics(energy_cell, out_cell)

        analytic_force = Ae4_1 / lam**3 + lam * AV_1
        force_relerr = relative_error(net, analytic_force)
        max_force_scaling_relerr = max(max_force_scaling_relerr, force_relerr)

        derrick = E2_0 - E4_0 / lam**2 + 3.0 * lam**2 * V_0
        curvature = 2.0 * E4_0 / lam**3 + 6.0 * lam * V_0

        active_total = 2.0 * E4_0 / lam - 2.0 * lam**3 * V_0

        eta_op = (lam * h0) ** 2 * net / max(E, 1.0e-300)

        morphology = zero_surface_cell_metrics(
            e4_center,
            v_center,
            energy_cell,
            conc["top50_mask"],
            lam,
            dx,
            nside,
        )

        spkp, spkn, snkp, snkn = global_result["sectors"][il]
        neg_active_force = snkn - snkp
        pos_active_force = spkp - spkn

        row = {
            "lambda": float(lam),
            "category": (
                "BLIND_WILDCARD_DIAGNOSTIC"
                if lam in wildcard_set
                else "MAIN"
            ),
            "scaled_center": float(lam * h0),
            "scaled_payload_radius": float(lam * rp0),
            "E": E,
            "E2": float(lam * E2_0),
            "E4": float(E4_0 / lam),
            "V": float(lam**3 * V_0),
            "derrick_derivative": float(derrick),
            "derrick_derivative_over_E": float(derrick / max(E, 1.0e-300)),
            "dilation_curvature": float(curvature),
            "active_total": float(active_total),
            "active_over_energy": float(active_total / max(E, 1.0e-300)),
            "negative_active_volume_fraction": float(
                global_result["neg_volume"][il]
                / max(global_result["total_volume"][il], 1.0e-300)
            ),
            "Qplus": float(global_result["qplus"][il]),
            "Qminus": float(global_result["qminus"][il]),
            "net_force": net,
            "analytic_force": float(analytic_force),
            "force_scaling_relerr": float(force_relerr),
            "outward": outward,
            "opposing": opposing,
            "cancellation": float(cancellation),
            "F25": float(conc["F25"]),
            "F50": float(conc["F50"]),
            "F75": float(conc["F75"]),
            "F90": float(conc["F90"]),
            "F99": float(conc["F99"]),
            "f_part": float(conc["f_part"]),
            "eta_op": float(eta_op),
            "e4_force": float(global_result["e4_force"][il]),
            "V_force": float(global_result["v_force"][il]),
            "negative_active_net_force": float(neg_active_force),
            "positive_active_net_force": float(pos_active_force),
            **morphology,
        }
        scale_rows.append(row)

        print(
            f"SCALE_CASE LAMBDA={lam:.6f} "
            f"NET={net:.9e} "
            f"ANALYTIC={analytic_force:.9e} "
            f"RELERR={force_relerr:.3e} "
            f"F50={row['F50']:.9e} "
            f"F90={row['F90']:.9e} "
            f"ETA_OP={eta_op:.9e} "
            f"DERRICK_OVER_E={row['derrick_derivative_over_E']:.9e} "
            f"NEG_VOL={row['negative_active_volume_fraction']:.9e} "
            f"DIST_SIGMA0={row['top50_mean_distance_to_sigma0']:.9e} "
            f"COMP={row['top50_connected_components']}",
            flush=True,
        )

    print(
        "HOMOTHETIC_FORCE_SCALING_MAX_RELERR="
        f"{max_force_scaling_relerr:.15e}"
    )
    print(f"HOMOTHETIC_FORCE_ZERO_LAMBDA={lambda_force_zero:.15e}")
    print(f"HOMOTHETIC_ENERGY_MIN_LAMBDA={lambda_energy_min:.15e}")

    if max_force_scaling_relerr > FORCE_SCALING_REL_TOL:
        raise RuntimeError("Homothetic force scaling identity did not close")

    print("\n=== E — RE-EQUILIBRATED EXACT-MAP m CHECK ===")
    m_rows = run_exact_m_scan(int02, a23, b23, direction)

    main_rows = [row for row in scale_rows if row["category"] == "MAIN"]

    scale_concentration_pass = all(
        row["F50"] <= STRONG_F50_MAX
        for row in main_rows
    )

    exact_success = [row for row in m_rows if row.get("success")]

    exact_concentration_pass = (
        len(exact_success) == len(M_MULTIPLIERS)
        and all(row["F50"] <= STRONG_F50_MAX for row in exact_success)
    )

    main_f50 = np.asarray([row["F50"] for row in main_rows])
    f50_spread = float(np.max(main_f50) - np.min(main_f50))

    if exact_success:
        eta_values = np.asarray([row["eta_op"] for row in exact_success])
        positive_eta = eta_values[eta_values > 0.0]
        if len(positive_eta) >= 2:
            exact_eta_ratio = float(
                np.max(positive_eta) / np.min(positive_eta)
            )
        else:
            exact_eta_ratio = float("nan")
    else:
        exact_eta_ratio = float("nan")

    if scale_concentration_pass and exact_concentration_pass:
        decision = (
            "SCALE_ROBUST_PRODUCTIVE_ANATOMY_WITH_NONSTATIONARY_DILATION_"
            "AND_REEQUILIBRATED_EXACT_MAP_SUPPORT"
        )
        next_action = (
            "INT03_04_GEOMETRY_CORRELATIONS_THEN_INT14_"
            "CONSERVATION_AWARE_SOURCE_LOWER_BOUND"
        )
    elif not scale_concentration_pass:
        decision = (
            "PRODUCTIVE_ANATOMY_IS_SCALE_SENSITIVE_IN_HOMOTHETIC_DIAGNOSTIC"
        )
        next_action = "LOCALIZE_SCALE_FAILURE_BEFORE_ANY_HEADROOM_CLAIM"
    else:
        decision = (
            "HOMOTHETIC_ANATOMY_SURVIVES_BUT_REEQUILIBRATED_M_FAMILY_"
            "DOES_NOT_REPRODUCE_IT"
        )
        next_action = (
            "DISTINGUISH_PARAMETER_EFFECT_FROM_GEOMETRIC_DILATION"
        )

    print("\n=== F — INT-03/04S DECISION ===")
    print(
        "MAIN_SCALE_ALL_F50_LE_0P10="
        f"{'PASS' if scale_concentration_pass else 'FAIL'}"
    )
    print(
        "REEQUILIBRATED_EXACT_M_ALL_F50_LE_0P10="
        f"{'PASS' if exact_concentration_pass else 'FAIL'}"
    )
    print(f"MAIN_SCALE_F50_SPREAD={f50_spread:.15e}")
    print(f"REEQUILIBRATED_EXACT_ETA_OP_RATIO={exact_eta_ratio:.15e}")
    print(
        "HOMOTHETIC_DILATION_PHYSICAL_STATIONARY_SOLUTION="
        "NO_EXCEPT_REFERENCE_LAMBDA_1"
    )
    print("STATIC_SCALE_SCAN_IS_EMISSION_CALCULATION=NO")
    print(f"INT03_04S_DECISION={decision}")
    print(
        "INT_LEVEL_2="
        "NOT_YET_REQUIRES_N65_N73_OR_EQUIVALENT_UNRESTRICTED_RESOLUTION_SUPPORT"
    )
    print(
        "INT_LEVEL_3="
        "NOT_YET_REQUIRES_CONSERVATION_OR_FIELD_EQUATION_COMPATIBLE_HEADROOM"
    )
    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "APPROXIMATELY_70_TO_71_PERCENT_NOT_A_PROBABILITY"
    )
    print(f"NEXT={next_action}")
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_INT03_04S_SCALE_ZERO_SURFACE_AUDIT"
    )

    with OUT_SCALE_CSV.open("w", newline="") as f:
        fieldnames = list(scale_rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scale_rows)

    if m_rows:
        fields = []
        for row in m_rows:
            for key in row:
                if key not in fields:
                    fields.append(key)
        with OUT_M_CSV.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(m_rows)

    summary = {
        "claim_classification": (
            "PROJECT_DERIVED_INT03_04S_SCALE_ZERO_SURFACE_AUDIT"
        ),
        "decision": decision,
        "next": next_action,
        "reference": {
            "B": B,
            "eta": ETA,
            "m": M0,
            "payload_center": h0,
            "payload_radius": rp0,
            "direction": [float(x) for x in direction],
            "E2": E2_0,
            "E4": E4_0,
            "V": V_0,
            "Ae4": Ae4_1,
            "AV": AV_1,
        },
        "homothetic": {
            "lambda_force_zero": lambda_force_zero,
            "lambda_energy_min": lambda_energy_min,
            "force_scaling_max_relerr": max_force_scaling_relerr,
            "main_F50_spread": f50_spread,
            "cases": scale_rows,
        },
        "reequilibrated_exact_m": {
            "eta_op_ratio": exact_eta_ratio,
            "cases": m_rows,
        },
        "gates": {
            "main_scale_concentration_pass": scale_concentration_pass,
            "exact_m_concentration_pass": exact_concentration_pass,
        },
        "claim_limits": {
            "homothetic_nonreference_is_stationary": False,
            "emission_calculated": False,
            "int_level_2": False,
            "int_level_3": False,
            "practical_device": False,
        },
    }

    OUT_JSON.write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=True) + "\n"
    )

    print(f"INT03_04S_SUMMARY_JSON={OUT_JSON}")
    print(f"INT03_04S_SCALE_CSV={OUT_SCALE_CSV}")
    print(f"INT03_04S_EXACT_M_CSV={OUT_M_CSV}")
    print("INT03_04S_RUN_COMPLETE=YES")


if __name__ == "__main__":
    main()
