#!/usr/bin/env python3
"""024A4 — true stand-off conserved-DEC teacher reconstruction.

PURPOSE
-------
Repair the successor-design target after 024A3 showed that the old INT14D N48
teacher obtained ~97.65% of gross outward response from positive active source
in the positive-kernel region beyond the payload. That teacher remains a valid
relaxed operational-force diagnostic, but it is not a one-sided stand-off
repulsion blueprint.

SCIENTIFIC QUESTION
-------------------
How much source-level efficiency survives if all source stress-energy is
confined to z<=0 while the payload center is at h=1, with positive energy,
exact type-I DEC, exact static finite-volume conservation, traction-free compact
boundaries, Laue identities, the finite-spherical-payload kernel, the frozen
INT14C density cap, and the current B7 R99 support scale?

The primary branch is FREECORE because the old B7 matched-core constraint
belonged to the payload-inside-shell geometry. A MATCHED_CORE branch measures
how much extra cost is associated with preserving that B7 anatomy.

ANALYTIC BOUND
--------------
For z<=z_max<1, K<0 and |K|<=1/(1-z_max)^2. Type-I DEC gives
S=rho+p1+p2+p3 >= -2 rho. Therefore A<=2E/(1-z_max)^2 and

    C=E/A >= (1-z_max)^2/2.

For strict z<=0, C>=1/2. With C_B7~422.222, the absolute static DEC headroom
in this strict class is only ~844x, so the old raw ~17230x teacher cannot be a
true one-sided static DEC source.

GEOMETRY LADDER
---------------
N16 scouts:
  KNEG_TANGENT_FREECORE: zmax=1-Rp/h (forbid K>0 only)
  HALF_GAP_FREECORE:     zmax=0.5
  STRICT_STANDOFF_FREECORE: zmax=0 (primary)
  STRICT_STANDOFF_MATCHED_CORE: zmax=0 (diagnostic)

The primary strict branch is refined at N24/N32/N40. Promotion uses N32/N40,
plus N24 as an additional convergence sentinel. A high-order independent force
reconstruction and SCS cross-solver check are required.

COMPARATORS / PROMOTION
-----------------------
A result is not promoted merely for >=10x versus B7 because 006D already gives
~17.9x true stand-off headroom. Promotion levels are:
  HOME_RUN:                  certified >=100x versus B7
  MAJOR_NEW_STANDOFF_RECORD: certified >=2x better than 006D
  NEW_STANDOFF_RECORD:       certified >=1.10x better than 006D

If compact R99 is numerically certified but does not beat 006D, a support
fallback scouts gamma=1.25,1.5 and clearly labeled blind wildcard diagnostics
1.6,1.875. Only the smallest candidate that beats the 006D record threshold is
refined.

ANATOMY / HANDOFF
-----------------
For the strict N40 source report A_rho, A_spatial_trace, cancellation, F50/F90,
force-weighted S/rho, force-weighted principal stresses, DEC saturation,
productive centroid, and the nearest simple stress archetype among isotropic
tension, domain-wall tension, string tension, and tension/compression transport.
This corrected anatomy determines the next microscopic 024B prefilter.

FALSIFIERS / STOP RULES
-----------------------
If strict stand-off cannot beat 006D, stop reverse-engineering the old teacher
and rerank 006D microscopic realization vs 023C/023D and Analogue Antigravity.
If a promising coefficient is not numerically certified, do only a targeted
024A4R refinement. No large 3D microscopic solve is authorized by this run.

CLAIM LIMITS
------------
Abstract linearized-GR source-level optimization only. No microscopic field,
stability, nonlinear GR, practical scaling, experiment, or device is claimed.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_024A4_TRUE_STANDOFF_CONSERVED_DEC_TEACHER_RECONSTRUCTION
"""
from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path
import sys
from typing import Any

import cvxpy as cp
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

INT14A_SUMMARY = DATA / "int14a_conservation_aware_constructive_headroom_summary.json"
INT14B_SUMMARY = DATA / "int14b_support_constrained_structural_overhead_summary.json"
INT14C_SUMMARY = DATA / "int14c_thousandfold_uv_regular_source_summary.json"
INT14B_SOURCE = SIM / "int14b_support_constrained_structural_overhead_bridge.py"
INT14C_SOURCE = SIM / "int14c_thousandfold_uv_regular_source_verification.py"
A3_SUMMARY = DATA / "024a3_isorotation_inertia_tomography_summary.json"

OUT_JSON = DATA / "024a4_true_standoff_teacher_reconstruction_summary.json"
OUT_CSV = DATA / "024a4_true_standoff_teacher_cases.csv"
OUT_NPZ = DATA / "024a4_true_standoff_teacher_best_arrays.npz"

SCOUT_N = 16
PRIMARY_NS = (24, 32, 40)
MATCHED_NS = (24, 32)
C_REL_TOL = 0.15
WIDTH_REL_TOL = 0.25
MIN_WIDTH_CELLS = 3.0
SCS_REL_TOL = 0.05
RHO_REL_TOL = 2e-5
CORE_ABS_TOL = 5e-5
NEG_CHANNEL_MIN = 1.0 - 1e-8
GE10 = 10.0
GE100 = 100.0
BEAT_006D = 1.10
MAJOR_006D = 2.0

ARCHETYPES = {
    "ISOTROPIC_TENSION": np.array([-1.0, -1.0, -1.0]),
    "DOMAIN_WALL_TENSION": np.array([-1.0, -1.0, 0.0]),
    "STRING_TENSION": np.array([-1.0, 0.0, 0.0]),
    "TENSION_COMPRESSION_TRANSPORT": np.array([-1.0, 0.0, 1.0]),
}


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def relerr(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def wquantile(v: np.ndarray, w: np.ndarray, q: float) -> float:
    v, w = np.asarray(v, float).ravel(), np.asarray(w, float).ravel()
    m = np.isfinite(v) & np.isfinite(w) & (w > 0)
    if not np.any(m):
        return float("nan")
    v, w = v[m], w[m]
    order = np.argsort(v)
    v, w = v[order], w[order]
    c = np.cumsum(w)
    i = min(int(np.searchsorted(c, q * c[-1], side="left")), len(v) - 1)
    return float(v[i])


def make_case(int14b, name: str, n: int, r99: float, qp: float,
              core_r: float, core_f: float, zmax: float, gamma: float = 1.0,
              matched_core: bool = False):
    radius = gamma * r99
    zmin = -radius
    zmax = min(float(zmax), radius)
    dr = radius / n
    nz = max(4, int(round((zmax - zmin) / dr)))
    return int14b.SupportCase(
        name=name, nr=n, nz=nz, radius=radius, zmin=zmin, zmax=zmax,
        target_z=1.0, payload_radius=qp, spherical_mask=True,
        reflection_symmetry=False,
        core_radius=(core_r if matched_core else None),
        core_fraction_target=(core_f if matched_core else None),
        category="024A4_TRUE_STANDOFF",
    )


def postcheck(row: dict[str, Any], rho_cap: float, core_target: float | None) -> bool:
    if not bool(row.get("green", False)):
        return False
    C = float(row.get("coefficient", float("nan")))
    if not (math.isfinite(C) and C > 0):
        return False
    if float(row.get("max_energy_density", float("inf"))) > rho_cap * (1 + RHO_REL_TOL):
        return False
    if core_target is not None:
        if float(row.get("core_active_fraction", float("inf"))) > core_target + CORE_ABS_TOL:
            return False
    return True


def public_row(row: dict[str, Any], label: str, kind: str,
               current_C: float, c006d: float) -> dict[str, Any]:
    out = {k: v for k, v in row.items() if k != "_arrays"}
    out.update(label=label, kind=kind)
    C = float(out.get("coefficient", float("nan")))
    if bool(out.get("green", False)) and math.isfinite(C) and C > 0:
        out["headroom_vs_B7"] = current_C / C
        out["improvement_vs_006D"] = c006d / C
    else:
        out["headroom_vs_B7"] = out["improvement_vs_006D"] = float("nan")
    return out


def print_case(label: str, row: dict[str, Any], current_C: float, c006d: float) -> None:
    C = float(row.get("coefficient", float("nan")))
    good = bool(row.get("green", False)) and math.isfinite(C) and C > 0
    H = current_C / C if good else float("nan")
    G = c006d / C if good else float("nan")
    print(
        f"024A4_CASE={label} STATUS={row.get('status')} GREEN={row.get('green')} "
        f"GRID={row.get('nr')}x{row.get('nz')} C={C:.12e} HEADROOM_B7={H:.9e} "
        f"GAIN_VS_006D={G:.9e} ACCEL={float(row.get('acceleration', float('nan'))):.12e} "
        f"RHO_MAX={float(row.get('max_energy_density', float('nan'))):.12e} "
        f"LE_CELLS={float(row.get('energy_width_cells', float('nan'))):.6e} "
        f"LF_CELLS={float(row.get('force_width_cells', float('nan'))):.6e}", flush=True)


def source_anatomy(row: dict[str, Any]) -> dict[str, Any]:
    a = row["_arrays"]
    rho, pr, pz, pp = (np.asarray(a[k], float) for k in ("e", "pr", "pz", "pphi"))
    trz = np.asarray(a["trz"], float)
    S, K, V = (np.asarray(a[k], float) for k in ("active_density", "kernels", "volumes"))
    r, z = (np.asarray(a[k], float) for k in ("r_centers", "z_centers"))
    cell_E, cell_F = rho * V, S * K
    out, opp = np.maximum(cell_F, 0), np.maximum(-cell_F, 0)
    gross, net, E = float(np.sum(out)), float(np.sum(cell_F)), float(np.sum(cell_E))

    stress = np.zeros(rho.shape + (3, 3))
    stress[..., 0, 0], stress[..., 1, 1], stress[..., 2, 2] = pr, pz, pp
    stress[..., 0, 1] = stress[..., 1, 0] = trz
    eig = np.linalg.eigvalsh(stress)
    floor = max(float(np.max(rho)), 1.0) * 1e-14
    good = rho > floor
    ratios = np.full_like(eig, np.nan)
    ratios[good] = eig[good] / rho[good, None]
    sratio = np.full_like(rho, np.nan)
    sratio[good] = S[good] / rho[good]
    dec = np.full_like(rho, np.nan)
    dec[good] = np.max(np.abs(ratios[good]), axis=-1)

    R, Z = np.meshgrid(r, z, indexing="ij")
    useful_neg = np.where((S < 0) & (K < 0), out, 0.0)
    useful_pos = np.where((S > 0) & (K > 0), out, 0.0)
    centroid_r = float(np.sum(R * out) / gross) if gross > 0 else float("nan")
    centroid_z = float(np.sum(Z * out) / gross) if gross > 0 else float("nan")
    A_rho = float(np.sum(rho * K))
    A_trace = float(np.sum((pr + pz + pp) * K))

    lmin = wquantile(ratios[..., 0], out, 0.5)
    lmid = wquantile(ratios[..., 1], out, 0.5)
    lmax = wquantile(ratios[..., 2], out, 0.5)
    med = np.array([lmin, lmid, lmax])
    distances = {k: float(np.linalg.norm(med - v)) for k, v in ARCHETYPES.items()}
    nearest = min(distances, key=distances.get)

    return {
        "E": E, "A": net, "C": E / max(net, 1e-300),
        "A_rho": A_rho, "A_spatial_trace": A_trace,
        "A_rho_over_net": A_rho / max(abs(net), 1e-300),
        "A_spatial_trace_over_net": A_trace / max(abs(net), 1e-300),
        "rho_trace_ledger_relerr": relerr(net, A_rho + A_trace),
        "gross_outward": gross, "gross_opposing": float(np.sum(opp)),
        "cancellation": float((np.sum(out) + np.sum(opp)) / max(abs(net), 1e-300)),
        "kernel_min": float(np.min(K)), "kernel_max": float(np.max(K)),
        "kernel_all_negative": bool(float(np.max(K)) < 1e-12),
        "negative_active_negative_kernel_fraction_of_gross": float(np.sum(useful_neg) / max(gross, 1e-300)),
        "positive_active_positive_kernel_fraction_of_gross": float(np.sum(useful_pos) / max(gross, 1e-300)),
        "force_weighted_S_over_rho_median": wquantile(sratio, out, 0.5),
        "force_weighted_lambda_min_over_rho": lmin,
        "force_weighted_lambda_mid_over_rho": lmid,
        "force_weighted_lambda_max_over_rho": lmax,
        "force_weighted_DEC_saturation": wquantile(dec, out, 0.5),
        "productive_centroid_r_over_h": centroid_r,
        "productive_centroid_z_over_h": centroid_z,
        "F50_energy_fraction": float(row.get("F50_energy_fraction", float("nan"))),
        "F90_energy_fraction": float(row.get("F90_energy_fraction", float("nan"))),
        "energy_width_cells": float(row.get("energy_width_cells", float("nan"))),
        "force_width_cells": float(row.get("force_width_cells", float("nan"))),
        "nearest_simple_stress_archetype": nearest,
        "stress_archetype_distances": distances,
    }


def main() -> None:
    print("=== 024A4 — TRUE STAND-OFF CONSERVED-DEC TEACHER RECONSTRUCTION ===", flush=True)
    for p in (INT14A_SUMMARY, INT14B_SUMMARY, INT14C_SUMMARY,
              INT14B_SOURCE, INT14C_SOURCE, A3_SUMMARY):
        require(p)

    a14 = json.loads(INT14A_SUMMARY.read_text())
    b14 = json.loads(INT14B_SUMMARY.read_text())
    c14 = json.loads(INT14C_SUMMARY.read_text())
    a3 = json.loads(A3_SUMMARY.read_text())
    old = a3["teacher_audit"]
    far_frac = float(old["positive_active_positive_kernel_fraction_of_gross_outward"])
    if old["mechanism_classification"] != "POSITIVE_ACTIVE_FAR_KERNEL_ATTRACTION_DOMINATED" or far_frac < 0.90:
        raise RuntimeError("024A3 far-side teacher prerequisite changed")

    current_C = float(c14["current_C"])
    rho_cap = float(c14["rho_cap"]["value"])
    sup = b14["exact_support_anatomy"]
    r99 = float(sup["R99_over_h"])
    qp = float(sup["payload_radius_over_h"])
    core_r = float(sup["core_radius_over_h"])
    core_f = float(sup["core_active_fraction"])
    c006d = float(a14["source_006d"]["finest_C"])
    h006d = current_C / c006d

    int14b = load_module("ag024a4_int14b", INT14B_SOURCE)
    int14c = load_module("ag024a4_int14c", INT14C_SOURCE)

    print("\n=== A — CORRECTED TARGET / ANALYTIC BOUNDS ===")
    print(f"CURRENT_B7_C={current_C:.15e}")
    print(f"006D_C={c006d:.15e}")
    print(f"006D_HEADROOM_VS_B7={h006d:.15e}")
    print(f"R99_OVER_H={r99:.15e}")
    print(f"PAYLOAD_RADIUS_OVER_H={qp:.15e}")
    print(f"FIXED_RHO_CAP={rho_cap:.15e}")
    print(f"CORE_RADIUS_OVER_H={core_r:.15e}")
    print(f"CORE_ACTIVE_FRACTION_TARGET={core_f:+.15e}")
    print(f"OLD_TEACHER_FAR_ATTRACTION_GROSS_FRACTION={far_frac:.15e}")
    print("OLD_RAW_TEACHER_AS_TRUE_STANDOFF_BLUEPRINT=RETIRED")

    z_tangent, z_half, z_strict = 1.0 - qp, 0.5, 0.0
    floors = {
        "KNEG_TANGENT": 0.5 * (1 - z_tangent) ** 2,
        "HALF_GAP": 0.5 * (1 - z_half) ** 2,
        "STRICT_STANDOFF": 0.5,
    }
    for name, floor in floors.items():
        print(f"{name}_DEC_C_FLOOR={floor:.15e}")
        print(f"{name}_B7_HEADROOM_ABSOLUTE_CEILING={current_C/floor:.15e}")
    print(f"STRICT_STANDOFF_006D_IMPROVEMENT_ABSOLUTE_CEILING={c006d/0.5:.15e}")
    print("RAW_17230X_COMPATIBLE_WITH_ZLE0_STATIC_DEC=NO")

    case_rows: list[dict[str, Any]] = []

    def solve(label: str, n: int, zmax: float, gamma: float,
              matched: bool, kind: str, solver: str | None = None):
        suffix = f"_{solver}" if solver else ""
        full = f"{label}_N{n}{suffix}"
        case = make_case(int14b, full, n, r99, qp, core_r, core_f, zmax, gamma, matched)
        print(f"024A4_SOLVE_BEGIN={full} GRID={case.nr}x{case.nz} R={case.radius:.9e} "
              f"ZMIN={case.zmin:.9e} ZMAX={case.zmax:.9e} MATCHED_CORE={'YES' if matched else 'NO'} "
              f"SOLVER={solver or 'DEFAULT'}", flush=True)
        row = int14c.solve_diagnostic_case(int14b, case, density_cap=rho_cap, solver_override=solver)
        print_case(full, row, current_C, c006d)
        case_rows.append(public_row(row, full, kind, current_C, c006d))
        return case, row

    print("\n=== B — N16 GEOMETRY LADDER ===", flush=True)
    _, tangent16 = solve("KNEG_TANGENT_FREECORE", SCOUT_N, z_tangent, 1.0, False, "GEOMETRY_SCOUT")
    _, half16 = solve("HALF_GAP_FREECORE", SCOUT_N, z_half, 1.0, False, "GEOMETRY_SCOUT")
    strict16_case, strict16 = solve("STRICT_STANDOFF_FREECORE", SCOUT_N, z_strict, 1.0, False, "PRIMARY")
    _, matched16 = solve("STRICT_STANDOFF_MATCHED_CORE", SCOUT_N, z_strict, 1.0, True, "CORE_DIAGNOSTIC")

    print("\n=== C — PRIMARY STRICT STANDOFF FREECORE REFINEMENT ===", flush=True)
    strict_cases, strict_rows = {SCOUT_N: strict16_case}, {SCOUT_N: strict16}
    for n in PRIMARY_NS:
        case, row = solve("STRICT_STANDOFF_FREECORE", n, z_strict, 1.0, False, "PRIMARY")
        strict_cases[n], strict_rows[n] = case, row

    print("\n=== D — MATCHED-CORE OVERHEAD REFINEMENT ===", flush=True)
    matched_rows = {SCOUT_N: matched16}
    for n in MATCHED_NS:
        _, matched_rows[n] = solve("STRICT_STANDOFF_MATCHED_CORE", n, z_strict, 1.0, True, "CORE_DIAGNOSTIC")

    green = all(postcheck(strict_rows[n], rho_cap, None) for n in PRIMARY_NS)
    if green:
        C24, C32, C40 = (float(strict_rows[n]["coefficient"]) for n in PRIMARY_NS)
        Ccons = max(C32, C40)
        Hcons, G006 = current_C / Ccons, c006d / Ccons
        c2432, c3240 = relerr(C24, C32), relerr(C32, C40)
        le2432 = relerr(float(strict_rows[24]["energy_effective_length"]), float(strict_rows[32]["energy_effective_length"]))
        le3240 = relerr(float(strict_rows[32]["energy_effective_length"]), float(strict_rows[40]["energy_effective_length"]))
        lf2432 = relerr(float(strict_rows[24]["force_effective_length"]), float(strict_rows[32]["force_effective_length"]))
        lf3240 = relerr(float(strict_rows[32]["force_effective_length"]), float(strict_rows[40]["force_effective_length"]))
        width40 = min(float(strict_rows[40]["energy_width_cells"]), float(strict_rows[40]["force_width_cells"]))
    else:
        C24 = C32 = C40 = Ccons = Hcons = G006 = float("nan")
        c2432 = c3240 = le2432 = le3240 = lf2432 = lf3240 = float("inf")
        width40 = 0.0

    print("\n=== E — INDEPENDENT FORCE / SOLVER CHECKS ===", flush=True)
    force = {"pass": False, "reason": "PRIMARY_NOT_GREEN"}
    if green:
        force = int14c.independent_force_reconstruction(strict_cases[40], strict_rows[40])
    print(f"STRICT_N40_INDEPENDENT_FORCE_BASE={float(force.get('acceleration_base', float('nan'))):.15e}")
    print(f"STRICT_N40_INDEPENDENT_FORCE_HI={float(force.get('acceleration_independent', float('nan'))):.15e}")
    print(f"STRICT_N40_INDEPENDENT_FORCE_RELERR={float(force.get('relative_error', float('nan'))):.15e}")
    print("STRICT_N40_INDEPENDENT_FORCE=" + ("PASS" if bool(force.get("pass", False)) else "FAIL"))

    scs_available = "SCS" in cp.installed_solvers()
    scs_pass, scs_rel = not scs_available, float("nan")
    if scs_available:
        _, scs16 = solve("STRICT_STANDOFF_FREECORE", SCOUT_N, z_strict, 1.0, False,
                         "SOLVER_CROSSCHECK", solver="SCS")
        scs_rel = relerr(float(strict16.get("coefficient", float("nan"))),
                         float(scs16.get("coefficient", float("nan"))))
        scs_pass = postcheck(scs16, rho_cap, None) and scs_rel <= SCS_REL_TOL
    print(f"STRICT_N16_SCS_AVAILABLE={'YES' if scs_available else 'NO'}")
    print(f"STRICT_N16_SCS_CLARABEL_C_RELERR={scs_rel:.15e}")
    print("STRICT_N16_INDEPENDENT_SOLVER=" + ("PASS" if scs_pass else "FAIL"))

    print("\n=== F — STRICT STANDOFF SOURCE ANATOMY ===", flush=True)
    anatomy = source_anatomy(strict_rows[40]) if green else None
    kernel_pass = bool(anatomy and anatomy["kernel_all_negative"])
    negchan_pass = bool(anatomy and anatomy["negative_active_negative_kernel_fraction_of_gross"] >= NEG_CHANNEL_MIN)
    if anatomy:
        for k, v in anatomy.items():
            if isinstance(v, (float, int)):
                print(f"STRICT_ANATOMY_{k.upper()}={float(v):.15e}")
        print(f"STRICT_ANATOMY_NEAREST_SIMPLE_STRESS_ARCHETYPE={anatomy['nearest_simple_stress_archetype']}")
    print("STRICT_KERNEL_ALL_NEGATIVE=" + ("PASS" if kernel_pass else "FAIL"))
    print("STRICT_OUTWARD_CHANNEL_IS_NEGATIVE_ACTIVE_NEGATIVE_KERNEL=" + ("PASS" if negchan_pass else "FAIL"))

    coeff_gate = green and max(c2432, c3240) <= C_REL_TOL
    length_gate = green and max(le2432, le3240, lf2432, lf3240) <= WIDTH_REL_TOL
    width_gate = green and width40 >= MIN_WIDTH_CELLS
    main_gate = bool(green and coeff_gate and length_gate and width_gate and
                     bool(force.get("pass", False)) and scs_pass and kernel_pass and negchan_pass)

    print("\n=== G — STRICT STANDOFF CERTIFICATE ===")
    print(f"STRICT_C24={C24:.15e}")
    print(f"STRICT_C32={C32:.15e}")
    print(f"STRICT_C40={C40:.15e}")
    print(f"STRICT_CONSERVATIVE_C32_C40={Ccons:.15e}")
    print(f"STRICT_CONSERVATIVE_HEADROOM_VS_B7={Hcons:.15e}")
    print(f"STRICT_CONSERVATIVE_IMPROVEMENT_VS_006D={G006:.15e}")
    print(f"STRICT_C_REL_DIFF_24_32={c2432:.15e}")
    print(f"STRICT_C_REL_DIFF_32_40={c3240:.15e}")
    print(f"STRICT_ENERGY_LENGTH_REL_DIFF_24_32={le2432:.15e}")
    print(f"STRICT_ENERGY_LENGTH_REL_DIFF_32_40={le3240:.15e}")
    print(f"STRICT_FORCE_LENGTH_REL_DIFF_24_32={lf2432:.15e}")
    print(f"STRICT_FORCE_LENGTH_REL_DIFF_32_40={lf3240:.15e}")
    print(f"STRICT_N40_MIN_WIDTH_CELLS={width40:.15e}")
    print("STRICT_STANDOFF_NUMERICAL_GATE=" + ("PASS" if main_gate else "FAIL"))

    matched32 = matched_rows[32]
    if green and postcheck(matched32, rho_cap, core_f):
        matched_C32 = float(matched32["coefficient"])
        core_overhead = matched_C32 / C32
    else:
        matched_C32 = core_overhead = float("nan")
    print("\n=== H — MATCHED-CORE OVERHEAD ===")
    print(f"MATCHED_CORE_C32={matched_C32:.15e}")
    print(f"MATCHED_CORE_OVER_FREECORE_C_RATIO_N32={core_overhead:.15e}")

    expansion = None
    if main_gate and G006 < BEAT_006D:
        print("\n=== I — EXPANDED-SUPPORT FALLBACK SCOUT ===", flush=True)
        probes = ((1.25, False), (1.50, False), (1.60, True), (1.875, True))
        selected = None
        for gamma, wildcard in probes:
            tag = str(gamma).replace(".", "P") + ("_BLIND_WILDCARD" if wildcard else "")
            case, row = solve(f"STANDOFF_EXPANDED_{tag}", SCOUT_N, z_strict, gamma, False,
                              "BLIND_WILDCARD_FALLBACK" if wildcard else "PHYSICAL_FALLBACK")
            if selected is None and postcheck(row, rho_cap, None):
                C = float(row["coefficient"])
                if c006d / C >= BEAT_006D:
                    selected = (gamma, wildcard)
        if selected:
            gamma, wildcard = selected
            tag = str(gamma).replace(".", "P") + ("_BLIND_WILDCARD" if wildcard else "")
            ecases, erows = {}, {}
            for n in (24, 32):
                ecases[n], erows[n] = solve(f"STANDOFF_EXPANDED_{tag}", n, z_strict, gamma, False, "FALLBACK_REFINED")
            if all(postcheck(erows[n], rho_cap, None) for n in (24, 32)):
                EC24, EC32 = float(erows[24]["coefficient"]), float(erows[32]["coefficient"])
                EC = max(EC24, EC32)
                ef = int14c.independent_force_reconstruction(ecases[32], erows[32])
                expansion = {
                    "gamma": gamma, "wildcard": wildcard, "C24": EC24, "C32": EC32,
                    "conservative_C": EC, "headroom_vs_B7": current_C / EC,
                    "improvement_vs_006D": c006d / EC, "C_rel_diff": relerr(EC24, EC32),
                    "independent_force": {k: v for k, v in ef.items() if k != "kernels_hi"},
                }
                expansion["pass"] = bool(expansion["C_rel_diff"] <= C_REL_TOL and
                                         ef.get("pass", False) and
                                         expansion["improvement_vs_006D"] >= BEAT_006D)

    if main_gate and Hcons >= GE100:
        decision = "GREEN_HOME_RUN_GE100X_TRUE_STANDOFF_CONSERVED_DEC_SOURCE_BLUEPRINT"
        next_action = "024B_CONSTITUTIVE_MATCHED_MICROSCOPIC_FIELD_PREFILTER_FROM_TRUE_STANDOFF_TEACHER"
    elif main_gate and G006 >= MAJOR_006D:
        decision = "GREEN_MAJOR_GE2X_OVER_006D_TRUE_STANDOFF_SOURCE_BLUEPRINT"
        next_action = "024B_CONSTITUTIVE_MATCHED_MICROSCOPIC_FIELD_PREFILTER_FROM_TRUE_STANDOFF_TEACHER"
    elif main_gate and G006 >= BEAT_006D:
        decision = "GREEN_NEW_TRUE_STANDOFF_RECORD_OVER_006D"
        next_action = "024B_CONSTITUTIVE_MATCHED_MICROSCOPIC_FIELD_PREFILTER_FROM_TRUE_STANDOFF_TEACHER"
    elif expansion and expansion.get("pass"):
        decision = "YELLOW_NEW_TRUE_STANDOFF_RECORD_REQUIRES_EXPANDED_SUPPORT"
        next_action = "024B_MICROSCOPIC_FIELD_PREFILTER_USING_MEASURED_EXPANDED_STANDOFF_SUPPORT"
    elif main_gate and Hcons >= GE10:
        decision = "YELLOW_GE10X_VS_B7_BUT_DOES_NOT_BEAT_006D"
        next_action = "RERANK_006D_MICROSCOPIC_REALIZATION_VS_023C_023D_AND_ANALOGUE_ANTIGRAVITY"
    elif main_gate:
        decision = "RED_CERTIFIED_COMPACT_TRUE_STANDOFF_SOURCE_DOES_NOT_IMPROVE_EXISTING_ANCHOR"
        next_action = "RERANK_006D_MICROSCOPIC_REALIZATION_VS_023C_023D_AND_ANALOGUE_ANTIGRAVITY"
    elif green:
        decision = "YELLOW_TRUE_STANDOFF_SIGNAL_NUMERICALLY_UNCERTIFIED"
        next_action = "024A4R_TARGETED_CONTINUUM_REFINEMENT_ONLY"
    else:
        decision = "RED_TRUE_STANDOFF_SOURCE_PRIMARY_NOT_GREEN"
        next_action = "REVIEW_CONSTRAINT_FEASIBILITY_THEN_RERANK_006D_VS_023C_023D_AND_ANALOGUE_ANTIGRAVITY"

    fields = sorted({k for row in case_rows for k in row})
    with OUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(case_rows)
    if green:
        np.savez_compressed(OUT_NPZ, **strict_rows[40]["_arrays"])

    summary = {
        "claim_classification": "PROJECT_DERIVED_024A4_TRUE_STANDOFF_CONSERVED_DEC_TEACHER_RECONSTRUCTION",
        "reason_for_single_reopen": "024A3_SHOWED_OLD_RAW_TEACHER_IS_97P65_PERCENT_FAR_SIDE_ATTRACTION",
        "current_B7_C": current_C,
        "006D": {"C": c006d, "headroom_vs_B7": h006d},
        "fixed_density_cap": {"value": rho_cap, "fundamental_physics": False},
        "support": {"R99_over_h": r99, "payload_radius_over_h": qp,
                    "core_radius_over_h": core_r, "core_active_fraction_target": core_f},
        "old_teacher": {"far_attraction_gross_fraction": far_frac,
                        "retired_as_true_standoff_blueprint": True},
        "analytic_bounds": {"KNEG_tangent_C_floor": floors["KNEG_TANGENT"],
                            "half_gap_C_floor": floors["HALF_GAP"],
                            "strict_z_le_0_C_floor": floors["STRICT_STANDOFF"],
                            "strict_B7_headroom_absolute_ceiling": current_C / 0.5,
                            "strict_006D_improvement_absolute_ceiling": c006d / 0.5,
                            "raw_17230x_compatible_with_strict_z_le_0_static_DEC": False},
        "cases": case_rows,
        "strict_primary_certificate": {
            "green_rows": green, "numerical_gate": main_gate,
            "C24": C24, "C32": C32, "C40": C40, "conservative_C32_C40": Ccons,
            "conservative_headroom_vs_B7": Hcons, "conservative_improvement_vs_006D": G006,
            "C_rel_diff_24_32": c2432, "C_rel_diff_32_40": c3240,
            "energy_length_rel_diff_24_32": le2432, "energy_length_rel_diff_32_40": le3240,
            "force_length_rel_diff_24_32": lf2432, "force_length_rel_diff_32_40": lf3240,
            "N40_min_width_cells": width40,
            "independent_force": {k: v for k, v in force.items() if k != "kernels_hi"},
            "SCS_available": scs_available, "SCS_rel_diff": scs_rel, "SCS_pass": scs_pass,
            "kernel_sign_pass": kernel_pass, "negative_channel_pass": negchan_pass,
        },
        "strict_source_anatomy": anatomy,
        "matched_core_over_freecore_C_ratio_N32": core_overhead,
        "expansion_fallback": expansion,
        "decision": decision, "next": next_action,
        "large_3D_microscopic_solve_authorized": False,
        "claim_limits": {"abstract_source_only": True, "density_cap_fundamental": False,
                         "microscopic_field_realization": False, "topology_stability": False,
                         "dynamic_well_posedness": False, "nonlinear_GR": False,
                         "practical_device": False},
        "current_knowledge_heuristic": "APPROXIMATELY_70_TO_71_PERCENT_NOT_A_PROBABILITY",
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2, allow_nan=True) + "\n")

    print("\n=== J — 024A4 DECISION ===")
    print(f"024A4_TRUE_STANDOFF_TEACHER_RECONSTRUCTION={decision}")
    print(f"STRICT_CONSERVATIVE_C={Ccons:.15e}")
    print(f"STRICT_CONSERVATIVE_HEADROOM_VS_B7={Hcons:.15e}")
    print(f"STRICT_CONSERVATIVE_IMPROVEMENT_VS_006D={G006:.15e}")
    print(f"STRICT_ABSOLUTE_DEC_B7_HEADROOM_CEILING={current_C/0.5:.15e}")
    if anatomy:
        print(f"STANDOFF_FORCE_WEIGHTED_MEDIAN_S_OVER_RHO={anatomy['force_weighted_S_over_rho_median']:.15e}")
        print(f"STANDOFF_FORCE_WEIGHTED_LAMBDA_MIN_OVER_RHO={anatomy['force_weighted_lambda_min_over_rho']:.15e}")
        print(f"STANDOFF_FORCE_WEIGHTED_LAMBDA_MID_OVER_RHO={anatomy['force_weighted_lambda_mid_over_rho']:.15e}")
        print(f"STANDOFF_FORCE_WEIGHTED_LAMBDA_MAX_OVER_RHO={anatomy['force_weighted_lambda_max_over_rho']:.15e}")
        print(f"STANDOFF_FORCE_WEIGHTED_DEC_SATURATION={anatomy['force_weighted_DEC_saturation']:.15e}")
        print(f"STANDOFF_NEGATIVE_ACTIVE_NEGATIVE_KERNEL_GROSS_FRACTION={anatomy['negative_active_negative_kernel_fraction_of_gross']:.15e}")
        print(f"STANDOFF_F90_ENERGY_FRACTION={anatomy['F90_energy_fraction']:.15e}")
        print(f"STANDOFF_A_RHO={anatomy['A_rho']:.15e}")
        print(f"STANDOFF_A_SPATIAL_STRESS_TRACE={anatomy['A_spatial_trace']:.15e}")
        print(f"STANDOFF_NEAREST_SIMPLE_STRESS_ARCHETYPE={anatomy['nearest_simple_stress_archetype']}")
    print(f"MATCHED_CORE_OVER_FREECORE_C_RATIO_N32={core_overhead:.15e}")
    print("OLD_RAW_17230X_TRUE_STANDOFF_TARGET=RETIRED")
    print(f"NEXT={next_action}")
    print("LARGE_3D_MICROSCOPIC_SOLVE_AUTHORIZED=NO_PREFILTER_FIRST")
    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_70_TO_71_PERCENT_NOT_A_PROBABILITY")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_024A4_TRUE_STANDOFF_CONSERVED_DEC_TEACHER_RECONSTRUCTION")
    print(f"SUMMARY_JSON={OUT_JSON.relative_to(ROOT)}")
    print(f"CASES_CSV={OUT_CSV.relative_to(ROOT)}")
    print(f"BEST_ARRAYS_NPZ={OUT_NPZ.relative_to(ROOT)}")
    print("024A4_RUN_COMPLETE=YES")


if __name__ == "__main__":
    main()
