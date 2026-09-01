#!/usr/bin/env python3
"""INT-15R — thousand-fold regression / provenance audit.

PURPOSE
-------
This is a verification-only audit. It performs NO optimization and changes no
physics parameters.

It answers four distinct questions:

1. Did the trusted promotion-grade B=7 operational baseline change?
2. Did the INT-14D N48 finite-density teacher source change?
3. Did the raw >1000x source-level efficiency margin change?
4. Did the formal >=1000x certification status change?

The intended outcome is to distinguish:

    RAW NUMERICAL HEADROOM

from

    CERTIFIED CONTINUUM SOURCE-CLASS HEADROOM

and prevent an orientation/comparator repair from being mistaken for a
scientific regression.

EXPECTED PRIOR STATE
--------------------
Trusted B=7 coefficient:
    C_current ~= 422.2220709

INT-14D N48 teacher:
    C_teacher ~= 0.02450446248

Raw diagnostic headroom:
    C_current / C_teacher ~= 1.723e4

But the formal INT-14D >=1000x certificate FAILED because:
    C40/C48 relative difference ~= 0.15567 > 0.15
    N48 minimum width ~= 1.856 cells < 3

The repaired INT-15 B=7 comparator should reproduce the trusted worst-direction
payload force exactly while leaving C_current, C_teacher, and raw headroom
unchanged.

CLAIM BOUNDARY
--------------
A PASS here means:

    NO REGRESSION IN THE RAW THOUSAND-FOLD-PLUS SOURCE-LEVEL SIGNAL.

It does NOT mean:

    >=1000x continuum headroom has been certified.

The robust promoted source-level result remains INT-14A's independently
verified ~12.8x to ~17.9x constructive conserved-DEC headroom.

No microscopic field realization or practical device is established.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_INT15R_THOUSANDFOLD_REGRESSION_PROVENANCE_AUDIT
"""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

INT14A = DATA / "int14a_conservation_aware_constructive_headroom_summary.json"
INT14C = DATA / "int14c_thousandfold_uv_regular_source_summary.json"
INT14D = DATA / "int14d_capped_thousandfold_final_refinement_summary.json"
INT14D_N48 = DATA / "int14d_capped_thousandfold_final_refinement_N48.npz"
INT15 = DATA / "int15_static_pulse_successor_blueprint_summary.json"

INT15_SOURCE = SIM / "int15_static_pulse_successor_blueprint_synthesis.py"

OUT_JSON = DATA / "int15r_thousandfold_regression_provenance_audit.json"

REL_TIGHT = 2.0e-8
FORCE_REL_TOL = 1.0e-4


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


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


def first_number(*candidates):
    for value in candidates:
        try:
            x = float(value)
        except Exception:
            continue
        if math.isfinite(x):
            return x
    raise RuntimeError("No finite numeric candidate found")


def main() -> None:
    print("=== INT-15R — THOUSAND-FOLD REGRESSION / PROVENANCE AUDIT ===")

    for p in (INT14A, INT14C, INT14D, INT14D_N48, INT15, INT15_SOURCE):
        require(p)

    a = load_json(INT14A)
    c = load_json(INT14C)
    d = load_json(INT14D)
    s = load_json(INT15)

    # ------------------------------------------------------------------
    # A. Provenance across summaries
    # ------------------------------------------------------------------
    print("\n=== A — CROSS-STAGE PROVENANCE ===")

    C_a = float(a["current_exact_map"]["C"])
    C_c = float(c["current_C"])
    C_d = float(d["current_C"])
    C_s = float(s["teacher"]["current_B7_C"])

    current_values = [C_a, C_c, C_d, C_s]
    current_spread = max(current_values) - min(current_values)
    current_rel_spread = current_spread / max(current_values)

    teacher_d = float(d["final_pair"]["conservative_C"])
    teacher_s = float(s["teacher"]["coefficient"])

    raw_d = float(d["final_pair"]["conservative_headroom"])
    raw_s = float(s["teacher"]["raw_headroom_vs_b7"])

    C1000 = float(d["C1000"])

    print(f"INT14A_CURRENT_C={C_a:.15e}")
    print(f"INT14C_CURRENT_C={C_c:.15e}")
    print(f"INT14D_CURRENT_C={C_d:.15e}")
    print(f"INT15_CURRENT_C={C_s:.15e}")
    print(f"CURRENT_C_REL_SPREAD={current_rel_spread:.15e}")

    print(f"INT14D_TEACHER_C={teacher_d:.15e}")
    print(f"INT15_TEACHER_C={teacher_s:.15e}")
    print(f"TEACHER_C_REL_DIFF_D15={relerr(teacher_d, teacher_s):.15e}")

    print(f"INT14D_RAW_HEADROOM={raw_d:.15e}")
    print(f"INT15_RAW_HEADROOM={raw_s:.15e}")
    print(f"RAW_HEADROOM_REL_DIFF_D15={relerr(raw_d, raw_s):.15e}")
    print(f"C_1000_THRESHOLD={C1000:.15e}")
    print(f"TEACHER_BELOW_C1000={'YES' if teacher_s <= C1000 else 'NO'}")

    provenance_pass = bool(
        current_rel_spread <= REL_TIGHT
        and relerr(teacher_d, teacher_s) <= REL_TIGHT
        and relerr(raw_d, raw_s) <= REL_TIGHT
        and teacher_s <= C1000
    )

    print("CROSS_STAGE_PROVENANCE=" + ("PASS" if provenance_pass else "FAIL"))

    # ------------------------------------------------------------------
    # B. Reconstruct N48 teacher directly from arrays.
    # ------------------------------------------------------------------
    print("\n=== B — DIRECT N48 TEACHER RECONSTRUCTION ===")

    with np.load(INT14D_N48, allow_pickle=False) as f:
        arrays = {k: np.array(f[k], copy=True) for k in f.files}

    for key in (
        "volumes",
        "kernels",
        "e",
        "pr",
        "pz",
        "pphi",
        "trz",
        "active_density",
        "active_mask",
        "r_edges",
        "z_edges",
    ):
        if key not in arrays:
            raise RuntimeError(f"N48 archive missing {key}")

    E_re = float(np.sum(arrays["volumes"] * arrays["e"]))
    A_re = float(np.sum(arrays["kernels"] * arrays["active_density"]))
    C_re = E_re / A_re

    int15 = load_module("int15r_int15", INT15_SOURCE)

    eig = int15.stress_eigenvalues(
        arrays["pr"],
        arrays["pz"],
        arrays["pphi"],
        arrays["trz"],
    )

    rho = arrays["e"]
    active = arrays["active_mask"].astype(bool)

    dec_violation_re = float(
        np.max(
            np.maximum(
                np.max(np.abs(eig), axis=-1) - rho,
                0.0,
            )[active]
        )
    )

    print(f"N48_RECONSTRUCTED_E={E_re:.15e}")
    print(f"N48_RECONSTRUCTED_A={A_re:.15e}")
    print(f"N48_RECONSTRUCTED_C={C_re:.15e}")
    print(f"N48_C_RELERR_VS_INT14D={relerr(C_re, teacher_d):.15e}")
    print(f"N48_RECOMPUTED_DEC_VIOLATION={dec_violation_re:.15e}")

    payload_radius = float(d["support"]["payload_radius_over_h"])

    # independent_teacher_force() is defined in INT-15, but its first
    # argument must be the INT-14C module because that module owns the
    # independent_cell_kernel() implementation.
    int14c = load_module(
        "int15r_int14c",
        int15.INT14C_SOURCE,
    )

    force = int15.independent_teacher_force(
        int14c,
        arrays,
        1.0,
        payload_radius,
    )

    print(f"N48_FORCE_BASE={float(force['A_base']):.15e}")
    print(
        f"N48_FORCE_INDEPENDENT_HI="
        f"{float(force['A_independent_high_order']):.15e}"
    )
    print(
        f"N48_FORCE_INDEPENDENT_RELERR="
        f"{float(force['relative_error']):.15e}"
    )
    print(
        "N48_FORCE_INDEPENDENT="
        + ("PASS" if bool(force["pass"]) else "FAIL")
    )

    teacher_reconstruction_pass = bool(
        relerr(C_re, teacher_d) <= REL_TIGHT
        and dec_violation_re <= 3.0e-6
        and bool(force["pass"])
    )

    print(
        "N48_TEACHER_RECONSTRUCTION="
        + ("PASS" if teacher_reconstruction_pass else "FAIL")
    )

    # ------------------------------------------------------------------
    # C. Independently rebuild B7 worst-direction operational baseline.
    # ------------------------------------------------------------------
    print("\n=== C — B7 WORST-DIRECTION BASELINE REBUILD ===")

    for p in (
        int15.INT02_SOURCE,
        int15.A23_SOURCE,
        int15.B23_SOURCE,
    ):
        require(p)

    int02 = load_module("int15r_int02", int15.INT02_SOURCE)
    a23 = load_module("int15r_a23", int15.A23_SOURCE)
    b23 = load_module("int15r_b23", int15.B23_SOURCE)

    exact = int15.rebuild_exact_b7(int02, a23, b23)

    A_b7_re = float(exact["A"])
    E_b7_re = float(exact["E"])
    h_b7 = float(exact["h"])
    C_b7_re = E_b7_re / (h_b7 * h_b7 * A_b7_re)

    A_b7_trusted = float(a["current_exact_map"]["A"])

    print(f"B7_REBUILT_A={A_b7_re:.15e}")
    print(f"B7_TRUSTED_A_INT14A={A_b7_trusted:.15e}")
    print(f"B7_A_RELERR={relerr(A_b7_re, A_b7_trusted):.15e}")
    print(f"B7_REBUILT_E={E_b7_re:.15e}")
    print(f"B7_REBUILT_C={C_b7_re:.15e}")
    print(f"B7_C_RELERR_VS_TRUSTED={relerr(C_b7_re, C_a):.15e}")

    b7_pass = bool(
        relerr(A_b7_re, A_b7_trusted) <= 2.0e-3
        and relerr(C_b7_re, C_a) <= 2.0e-3
    )

    print("B7_BASELINE_REBUILD=" + ("PASS" if b7_pass else "FAIL"))

    # ------------------------------------------------------------------
    # D. Recompute raw headroom from independent reconstructions.
    # ------------------------------------------------------------------
    print("\n=== D — INDEPENDENT RAW HEADROOM RECOMPUTATION ===")

    H_re = C_b7_re / C_re
    margin_over_1000 = H_re / 1000.0

    print(f"RAW_HEADROOM_RECOMPUTED={H_re:.15e}")
    print(f"RAW_HEADROOM_MARGIN_OVER_1000X={margin_over_1000:.15e}")
    print(
        "RAW_THOUSANDFOLD_SIGNAL_PRESENT="
        + ("YES" if H_re >= 1000.0 else "NO")
    )

    raw_signal_pass = bool(
        H_re >= 1000.0
        and relerr(H_re, raw_s) <= 2.0e-3
    )

    print(
        "RAW_HEADROOM_NO_REGRESSION="
        + ("PASS" if raw_signal_pass else "FAIL")
    )

    # ------------------------------------------------------------------
    # E. Certification status: explicitly confirm why it is still not promoted.
    # ------------------------------------------------------------------
    print("\n=== E — CERTIFICATION STATUS AUDIT ===")

    final = d["final_pair"]

    c_pair_rel = float(final["C_rel_diff"])
    width48 = float(final["N48_min_width_cells"])

    c_tol = float(d["thresholds"]["C_convergence"])
    width_min = float(d["thresholds"]["minimum_width_cells"])

    formal_gate = bool(
        d["gates"]["thousandfold_finite_density_final_verification"]
    )
    level3 = bool(
        d["gates"]["int_level_3_formal"]
    )

    print(f"INT14D_C40_C48_REL_DIFF={c_pair_rel:.15e}")
    print(f"INT14D_C_CONVERGENCE_LIMIT={c_tol:.15e}")
    print(
        "INT14D_C_CONVERGENCE_GATE="
        + ("PASS" if c_pair_rel <= c_tol else "FAIL")
    )

    print(f"INT14D_N48_MIN_WIDTH_CELLS={width48:.15e}")
    print(f"INT14D_MIN_WIDTH_REQUIREMENT={width_min:.15e}")
    print(
        "INT14D_WIDTH_GATE="
        + ("PASS" if width48 >= width_min else "FAIL")
    )

    print(
        "INT14D_FORMAL_THOUSANDFOLD_CERTIFICATE="
        + ("PASS" if formal_gate else "FAIL")
    )
    print(
        "INT14D_FORMAL_LEVEL3="
        + ("PASS" if level3 else "NOT_YET")
    )

    certification_unchanged = bool(
        not formal_gate
        and not level3
        and c_pair_rel > c_tol
        and width48 < width_min
    )

    print(
        "CERTIFICATION_STATUS_UNCHANGED="
        + ("PASS" if certification_unchanged else "FAIL")
    )

    # ------------------------------------------------------------------
    # F. Robust promoted comparator remains.
    # ------------------------------------------------------------------
    print("\n=== F — ROBUST PROMOTED SOURCE HEADROOM ===")

    h006d = float(a["source_006d"]["headroom_vs_current"])
    h006b = float(
        next(
            row["headroom_vs_current"]
            for row in a["source_006b"]
            if row["name"] == "KNOWN_THIN20"
        )
    )

    print(f"ROBUST_006D_HEADROOM={h006d:.15e}")
    print(f"ROBUST_006B_HEADROOM={h006b:.15e}")
    print(
        "ROBUST_TWO_ROUTE_GE10X="
        + (
            "PASS"
            if h006d >= 10.0 and h006b >= 10.0
            else "FAIL"
        )
    )

    # ------------------------------------------------------------------
    # Final decision.
    # ------------------------------------------------------------------
    overall = bool(
        provenance_pass
        and teacher_reconstruction_pass
        and b7_pass
        and raw_signal_pass
        and certification_unchanged
        and h006d >= 10.0
        and h006b >= 10.0
    )

    print("\n=== G — FINAL REGRESSION DECISION ===")

    if overall:
        decision = (
            "NO_REGRESSION_RAW_THOUSANDFOLD_PLUS_SIGNAL_PERSISTS_"
            "BUT_REMAINS_UNCERTIFIED"
        )
    else:
        decision = (
            "REGRESSION_OR_PROVENANCE_INCONSISTENCY_REQUIRES_REVIEW"
        )

    print(
        "INT15R_REGRESSION_AUDIT="
        + ("PASS" if overall else "FAIL")
    )
    print(f"INT15R_DECISION={decision}")
    print(
        "RAW_GE1000X_SOURCE_LEVEL_SIGNAL="
        + ("PRESENT" if raw_signal_pass else "NOT_CONFIRMED")
    )
    print(
        "CERTIFIED_GE1000X_SOURCE_CLASS="
        + ("NO" if certification_unchanged else "REVIEW")
    )
    print(
        "ROBUST_PROMOTED_CONSTRUCTIVE_HEADROOM="
        "12P8_TO_17P9X"
    )
    print(
        "MICROSCOPIC_FIELD_GE1000X_REALIZATION=NO"
    )
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print(
        "NEXT="
        "RETURN_TO_STATIC_AND_PULSED_SUCCESSOR_FIELD_DESIGN_"
        "WITHOUT_MORE_ABSTRACT_COEFFICIENT_POLISHING"
    )

    summary = {
        "claim_classification": (
            "PROJECT_DERIVED_INT15R_THOUSANDFOLD_REGRESSION_PROVENANCE_AUDIT"
        ),
        "overall_pass": overall,
        "decision": decision,
        "current_C": {
            "INT14A": C_a,
            "INT14C": C_c,
            "INT14D": C_d,
            "INT15": C_s,
            "relative_spread": current_rel_spread,
        },
        "teacher": {
            "INT14D_C": teacher_d,
            "INT15_C": teacher_s,
            "reconstructed_C": C_re,
            "independent_force": {
                "base": float(force["A_base"]),
                "high_order": float(force["A_independent_high_order"]),
                "relative_error": float(force["relative_error"]),
                "pass": bool(force["pass"]),
            },
            "recomputed_DEC_violation": dec_violation_re,
        },
        "b7": {
            "trusted_A": A_b7_trusted,
            "rebuilt_A": A_b7_re,
            "rebuilt_E": E_b7_re,
            "trusted_C": C_a,
            "rebuilt_C": C_b7_re,
            "pass": b7_pass,
        },
        "raw_headroom": {
            "INT14D": raw_d,
            "INT15": raw_s,
            "independently_recomputed": H_re,
            "margin_over_1000": margin_over_1000,
            "no_regression_pass": raw_signal_pass,
        },
        "certification": {
            "C40_C48_rel_diff": c_pair_rel,
            "C_convergence_limit": c_tol,
            "N48_min_width_cells": width48,
            "minimum_width_cells": width_min,
            "formal_thousandfold_certificate": formal_gate,
            "formal_INT_level3": level3,
            "status_unchanged": certification_unchanged,
        },
        "robust_promoted": {
            "006D_headroom": h006d,
            "006B_headroom": h006b,
            "two_route_ge10x": bool(
                h006d >= 10.0 and h006b >= 10.0
            ),
        },
        "claim_limits": {
            "certified_ge1000x_source_class": False,
            "microscopic_ge1000x_field_realization": False,
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

    print(f"INT15R_SUMMARY_JSON={OUT_JSON}")
    print("INT15R_RUN_COMPLETE=YES")


if __name__ == "__main__":
    main()
