#!/usr/bin/env python3
"""024A4R — true stand-off feasibility decomposition and 006B positive control.

PURPOSE
-------
Repair the interpretation of 024A4.

024A4 found the strict z<=0, R99/h~=3.354, frozen-density-cap source problem
infeasible from N16 through N40. That cannot be interpreted as a universal
stand-off no-go because 006B and 006D are already constructive positive-energy,
DEC, locally-conserved stand-off sources.

This run determines which additional restriction caused the 024A4
infeasibility:

    1. insufficient radial support,
    2. insufficient density capacity,
    3. vertical thickness / aspect geometry,
    4. some combination of the above.

QUESTION
--------
What is the minimum support/capacity change needed to recover a legitimate
z<=0 conserved-DEC source, and does any numerically resolved corrected source
beat the existing 006D coefficient?

POSITIVE CONTROL
----------------
The run must first reproduce the known independent 006B finite-volume source

    nr=20
    nz=2
    R/h=5
    depth/h=0.125

with

    C ~= 32.9547546669.

The generalized finite-spherical-payload solver must independently reproduce
the same coefficient.

Because the entire payload sphere is source-free, the mean-value theorem makes
the point-target 006B acceleration exactly equal to the uniform spherical
payload center-of-mass acceleration.

KNOWN CLASSICAL ANCHORS
-----------------------
006B thin analytic optimum:

    R/h = 4.701437405300
    C   = 23.426710175391

006D finite-thickness:

    C   = 23.591586299249

024A4 strict compact support:

    R99/h = 3.353681771...
    rho_cap ~= 1.669855319...

The frozen density cap is diagnostic, not fundamental physics.

TRACK A — RADIAL SUPPORT
------------------------
Use the original uncapped 006B solver at fixed thin depth/h=0.125 and scan:

    R/h =
      3.0,
      R99,
      3.75,
      4.0,
      4.25,
      4.5,
      beta_006B,
      5.0,
      5.5,
      6.0.

This directly identifies the approximate finite-volume radial feasibility
threshold without contamination by the INT14 density cap.

TRACK B — DENSITY-CAP CAPACITY
------------------------------
At the validated R/h=5, depth/h=0.125 geometry, use the generalized
finite-payload solver with

    rho_cap multiplier =
      1,
      2,
      4,
      8,
      16,
      uncapped.

If the multiplier-1 case fails but a larger finite multiplier passes, perform
four bisection steps to estimate the cap multiplier required for feasibility.

TRACK C — STRICT CYLINDRICAL GEOMETRY MATRIX
--------------------------------------------
At the original frozen density cap, keep zmax=0 and scan:

    R/h =
      R99,
      4.0,
      beta_006B,
      5.0,
      6.0

    depth/h =
      0.125,
      0.25,
      0.5,
      1.0.

All sources remain fully on the source side of the payload.

This determines whether increased radial support, increased volume/thickness,
or both can recover strict stand-off feasibility without relaxing the frozen
density cap.

TRACK D — REFINEMENT
--------------------
If Track C finds any green source, select the lowest-C source using ONLY those
predeclared physical scans and refine it at radial N16 and N24 with
aspect-ratio-aware vertical resolution.

Require:

    DEC green,
    conservation green,
    Laue green,
    positive target acceleration,
    density cap obeyed,
    C16/C24 relative disagreement <= 15%,
    minimum energy/force participation width >= 3 cells at N24,
    independent high-order finite-payload force <= 1e-4 relative error,
    independent SCS coefficient agreement <= 5% when SCS is available.

PROMOTION
---------
A corrected source is a new stand-off source-level record only if the
conservative N16/N24 coefficient satisfies

    C_conservative < C006D / 1.10.

A major record requires

    C_conservative <= C006D / 2.

No source-level result is a microscopic realization.

FALSIFICATION / STOP RULE
-------------------------
If feasibility is restored but no certified source improves 006D, stop
stand-off coefficient polishing. Preserve 006D as the strongest classical
stand-off architecture and rerank:

    006D microscopic realization,
    023C/023D nonlinear topological path,
    Analogue Antigravity.

If only relaxing the nonfundamental density cap restores feasibility, record
that explicitly and do not promote the cap as a physics obstruction.

If larger radius is required, record the radial support threshold and treat
spatial stress-transfer reach as a mandatory successor-field design feature.

CLAIM LIMITS
------------
Static linearized-GR source optimization only.
No microscopic matter field.
No nonlinear Einstein solution.
No dynamical stability.
No practical energy scale improvement by itself.
No practical antigravity device.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_024A4R_STANDOFF_FEASIBILITY_DECOMPOSITION
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

S006B = SIM / "006b_full_rz_decision.py"
INT14B_SOURCE = SIM / "int14b_support_constrained_structural_overhead_bridge.py"
INT14C_SOURCE = SIM / "int14c_thousandfold_uv_regular_source_verification.py"

INT14A_SUMMARY = DATA / "int14a_conservation_aware_constructive_headroom_summary.json"
A4_SUMMARY = DATA / "024a4_true_standoff_teacher_reconstruction_summary.json"

OUT_JSON = DATA / "024a4r_standoff_feasibility_decomposition_summary.json"
OUT_CSV = DATA / "024a4r_standoff_feasibility_cases.csv"
OUT_NPZ = DATA / "024a4r_best_standoff_source_arrays.npz"

EXPECTED_006B_C = 32.95475466694425
C006B_THIN = 23.426710175391
BETA_006B = 4.701437405300

RECOVERY_REL_TOL = 3.0e-3
DEC_TOL = 3.0e-6
CONS_TOL = 3.0e-6
TRACE_TOL = 3.0e-6

C_CONV_TOL = 0.15
WIDTH_MIN = 3.0
FORCE_REL_TOL = 1.0e-4
SCS_REL_TOL = 0.05

NEW_RECORD_FACTOR = 1.10
MAJOR_RECORD_FACTOR = 2.0


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(
            f"Required file missing: {path}"
        )


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"Cannot import {path}"
        )

    mod = importlib.util.module_from_spec(
        spec
    )

    sys.modules[name] = mod
    spec.loader.exec_module(mod)

    return mod


def relerr(a: float, b: float) -> float:
    return (
        abs(a - b)
        / max(
            abs(a),
            abs(b),
            1.0e-300,
        )
    )


def clean_json(value):
    if isinstance(value, dict):
        return {
            str(k): clean_json(v)
            for k, v in value.items()
            if k != "_arrays"
        }

    if isinstance(value, (list, tuple)):
        return [
            clean_json(v)
            for v in value
        ]

    if isinstance(value, np.ndarray):
        return value.tolist()

    if isinstance(value, np.generic):
        return value.item()

    return value


def direct_green(row: dict[str, Any]) -> bool:
    C = float(
        row.get(
            "coefficient",
            float("nan"),
        )
    )

    if not (
        math.isfinite(C)
        and C > 0.0
    ):
        return False

    return bool(
        abs(
            float(
                row.get(
                    "acceleration",
                    float("nan"),
                )
            )
            - 1.0
        )
        <= 2.0e-5
        and float(
            row.get(
                "max_dec_violation",
                float("inf"),
            )
        )
        <= DEC_TOL
        and float(
            row.get(
                "max_conservation_residual",
                float("inf"),
            )
        )
        <= CONS_TOL
        and abs(
            float(
                row.get(
                    "trace_integral",
                    float("inf"),
                )
            )
        )
        <= TRACE_TOL
    )


def diagnostic_green(
    row: dict[str, Any],
) -> bool:
    return bool(
        row.get(
            "green",
            False,
        )
    )


def nz_for(
    nr: int,
    radius: float,
    depth: float,
) -> int:
    aspect = int(
        math.ceil(
            depth
            * nr
            / max(
                radius,
                1.0e-12,
            )
        )
    )

    if depth <= 0.25:
        floor = 2
    elif depth <= 0.5:
        floor = 3
    else:
        floor = 4

    return max(
        floor,
        aspect,
    )


def support_case(
    int14b,
    name: str,
    nr: int,
    radius: float,
    depth: float,
    q_payload: float,
):
    return int14b.SupportCase(
        name=name,
        nr=nr,
        nz=nz_for(
            nr,
            radius,
            depth,
        ),
        radius=radius,
        zmin=-depth,
        zmax=0.0,
        target_z=1.0,
        payload_radius=q_payload,
        spherical_mask=False,
        reflection_symmetry=False,
        core_radius=None,
        core_fraction_target=None,
        category="024A4R_STRICT_STANDOFF_CYLINDER",
    )


def print_direct(
    label: str,
    row: dict[str, Any],
    current_C: float,
    c006d: float,
) -> None:
    C = float(
        row.get(
            "coefficient",
            float("nan"),
        )
    )

    green = direct_green(row)

    H = (
        current_C / C
        if green
        else float("nan")
    )

    G = (
        c006d / C
        if green
        else float("nan")
    )

    print(
        f"024A4R_DIRECT={label} "
        f"STATUS={row.get('status')} "
        f"GREEN={'YES' if green else 'NO'} "
        f"C={C:.15e} "
        f"HEADROOM_B7={H:.15e} "
        f"GAIN_VS_006D={G:.15e} "
        f"R={float(row.get('radius', float('nan'))):.9e} "
        f"DEPTH={float(row.get('depth', float('nan'))):.9e}",
        flush=True,
    )


def print_diag(
    label: str,
    row: dict[str, Any],
    current_C: float,
    c006d: float,
    cap_multiplier: float | None,
) -> None:
    C = float(
        row.get(
            "coefficient",
            float("nan"),
        )
    )

    green = diagnostic_green(row)

    H = (
        current_C / C
        if green
        else float("nan")
    )

    G = (
        c006d / C
        if green
        else float("nan")
    )

    cap_text = (
        "UNCAPPED"
        if cap_multiplier is None
        else f"{cap_multiplier:.8g}"
    )

    print(
        f"024A4R_DIAG={label} "
        f"STATUS={row.get('status')} "
        f"GREEN={'YES' if green else 'NO'} "
        f"C={C:.15e} "
        f"HEADROOM_B7={H:.15e} "
        f"GAIN_VS_006D={G:.15e} "
        f"RHO_MAX={float(row.get('max_energy_density', float('nan'))):.15e} "
        f"LE_CELLS={float(row.get('energy_width_cells', float('nan'))):.9e} "
        f"LF_CELLS={float(row.get('force_width_cells', float('nan'))):.9e} "
        f"CAP_MULT={cap_text}",
        flush=True,
    )


def direct_record(
    name: str,
    case,
    raw: dict[str, Any],
    current_C: float,
    c006d: float,
) -> dict[str, Any]:
    out = {
        "track": "A_UNCAPPED_RADIAL_SUPPORT",
        "name": name,
        "nr": case.nr,
        "nz": case.nz,
        "radius": case.radius,
        "depth": case.depth,
        **clean_json(raw),
    }

    C = float(
        out.get(
            "coefficient",
            float("nan"),
        )
    )

    out["green_postcheck"] = direct_green(raw)

    out["headroom_vs_B7"] = (
        current_C / C
        if out["green_postcheck"]
        else float("nan")
    )

    out["gain_vs_006D"] = (
        c006d / C
        if out["green_postcheck"]
        else float("nan")
    )

    return out


def diag_record(
    track: str,
    label: str,
    case,
    row: dict[str, Any],
    current_C: float,
    c006d: float,
    cap_multiplier: float | None,
) -> dict[str, Any]:
    out = {
        "track": track,
        "label": label,
        "nr": case.nr,
        "nz": case.nz,
        "radius": case.radius,
        "depth": -case.zmin,
        "cap_multiplier": (
            cap_multiplier
            if cap_multiplier is not None
            else float("nan")
        ),
        "uncapped": (
            cap_multiplier is None
        ),
        **clean_json(row),
    }

    C = float(
        out.get(
            "coefficient",
            float("nan"),
        )
    )

    green = diagnostic_green(row)

    out["green_postcheck"] = green

    out["headroom_vs_B7"] = (
        current_C / C
        if green
        else float("nan")
    )

    out["gain_vs_006D"] = (
        c006d / C
        if green
        else float("nan")
    )

    return out


def solve_capped(
    int14b,
    int14c,
    label: str,
    nr: int,
    radius: float,
    depth: float,
    q_payload: float,
    cap: float | None,
    cap_multiplier: float | None,
    current_C: float,
    c006d: float,
    solver: str | None = None,
):
    case = support_case(
        int14b,
        label,
        nr,
        radius,
        depth,
        q_payload,
    )

    print(
        f"024A4R_SOLVE_BEGIN={label} "
        f"GRID={case.nr}x{case.nz} "
        f"R={radius:.9e} "
        f"DEPTH={depth:.9e} "
        f"CAP={'NONE' if cap is None else f'{cap:.9e}'} "
        f"SOLVER={solver or 'DEFAULT'}",
        flush=True,
    )

    row = int14c.solve_diagnostic_case(
        int14b,
        case,
        density_cap=cap,
        solver_override=solver,
    )

    print_diag(
        label,
        row,
        current_C,
        c006d,
        cap_multiplier,
    )

    return case, row


def main() -> None:
    print(
        "=== 024A4R — STAND-OFF FEASIBILITY DECOMPOSITION ===",
        flush=True,
    )

    for p in (
        S006B,
        INT14B_SOURCE,
        INT14C_SOURCE,
        INT14A_SUMMARY,
        A4_SUMMARY,
    ):
        require(p)

    prior = json.loads(
        INT14A_SUMMARY.read_text()
    )

    a4 = json.loads(
        A4_SUMMARY.read_text()
    )

    current_C = float(
        a4["current_B7_C"]
    )

    c006d = float(
        a4["006D"]["C"]
    )

    rho_cap = float(
        a4[
            "fixed_density_cap"
        ][
            "value"
        ]
    )

    r99 = float(
        a4[
            "support"
        ][
            "R99_over_h"
        ]
    )

    q_payload = float(
        a4[
            "support"
        ][
            "payload_radius_over_h"
        ]
    )

    prior_006b_C = float(
        next(
            x["coefficient"]
            for x
            in prior["source_006b"]
            if x["name"]
            == "KNOWN_THIN20"
        )
    )

    s006b = load_module(
        "ag024a4r_006b",
        S006B,
    )

    int14b = load_module(
        "ag024a4r_int14b",
        INT14B_SOURCE,
    )

    int14c = load_module(
        "ag024a4r_int14c",
        INT14C_SOURCE,
    )

    all_rows: list[
        dict[str, Any]
    ] = []

    print(
        "\n=== A — ANCHORS / POSITIVE CONTROLS ===",
        flush=True,
    )

    print(
        f"CURRENT_B7_C="
        f"{current_C:.15e}"
    )

    print(
        f"006B_THIN_ANALYTIC_C="
        f"{C006B_THIN:.15e}"
    )

    print(
        f"006B_THIN_ANALYTIC_BETA="
        f"{BETA_006B:.15e}"
    )

    print(
        f"006D_FINITE_C="
        f"{c006d:.15e}"
    )

    print(
        f"024A4_R99_OVER_H="
        f"{r99:.15e}"
    )

    print(
        f"024A4_RHO_CAP="
        f"{rho_cap:.15e}"
    )

    direct_case = s006b.Case(
        "POSITIVE_CONTROL_006B_KNOWN_THIN20",
        20,
        2,
        5.0,
        0.125,
    )

    direct = s006b.solve_case(
        direct_case
    )

    print_direct(
        direct_case.name,
        direct,
        current_C,
        c006d,
    )

    direct_rel = relerr(
        float(
            direct.get(
                "coefficient",
                float("nan"),
            )
        ),
        EXPECTED_006B_C,
    )

    direct_pass = bool(
        direct_green(direct)
        and direct_rel
        <= RECOVERY_REL_TOL
    )

    print(
        "DIRECT_006B_POSITIVE_CONTROL_RELERR="
        f"{direct_rel:.15e}"
    )

    print(
        "DIRECT_006B_POSITIVE_CONTROL="
        + (
            "PASS"
            if direct_pass
            else "FAIL"
        )
    )

    if not direct_pass:
        raise RuntimeError(
            "Direct 006B positive control failed"
        )

    recovery_case = int14b.SupportCase(
        name="GENERALIZED_006B_POSITIVE_CONTROL",
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

    recovery = (
        int14c.solve_diagnostic_case(
            int14b,
            recovery_case,
            density_cap=None,
        )
    )

    recovery_C = float(
        recovery.get(
            "coefficient",
            float("nan"),
        )
    )

    recovery_rel = relerr(
        recovery_C,
        prior_006b_C,
    )

    recovery_pass = bool(
        diagnostic_green(recovery)
        and recovery_rel
        <= RECOVERY_REL_TOL
    )

    print_diag(
        "GENERALIZED_006B_POSITIVE_CONTROL",
        recovery,
        current_C,
        c006d,
        None,
    )

    print(
        "GENERALIZED_006B_CONTROL_RELERR="
        f"{recovery_rel:.15e}"
    )

    print(
        "GENERALIZED_006B_POSITIVE_CONTROL="
        + (
            "PASS"
            if recovery_pass
            else "FAIL"
        )
    )

    if not recovery_pass:
        raise RuntimeError(
            "Generalized 006B recovery failed"
        )

    print(
        "\n=== B — TRACK A: "
        "UNCAPPED RADIAL SUPPORT THRESHOLD ===",
        flush=True,
    )

    radius_scan = [
        3.0,
        r99,
        3.75,
        4.0,
        4.25,
        4.5,
        BETA_006B,
        5.0,
        5.5,
        6.0,
    ]

    direct_scan = []

    for radius in radius_scan:
        label = (
            "RADIAL_R"
            + str(
                round(
                    radius,
                    6,
                )
            ).replace(
                ".",
                "P",
            )
        )

        case = s006b.Case(
            label,
            20,
            2,
            float(radius),
            0.125,
        )

        row = s006b.solve_case(
            case
        )

        print_direct(
            label,
            row,
            current_C,
            c006d,
        )

        record = direct_record(
            label,
            case,
            row,
            current_C,
            c006d,
        )

        direct_scan.append(
            record
        )

        all_rows.append(
            record
        )

    feasible_radii = [
        float(r["radius"])
        for r in direct_scan
        if r[
            "green_postcheck"
        ]
    ]

    radial_threshold = (
        min(feasible_radii)
        if feasible_radii
        else float("nan")
    )

    radial_support_obstruction = bool(
        math.isfinite(
            radial_threshold
        )
        and radial_threshold
        > r99
        * 1.01
    )

    print(
        "UNCAPPED_MIN_TESTED_FEASIBLE_R_OVER_H="
        f"{radial_threshold:.15e}"
    )

    print(
        "R99_BELOW_UNCAPPED_FEASIBILITY_THRESHOLD="
        + (
            "YES"
            if radial_support_obstruction
            else "NO"
        )
    )

    print(
        "\n=== C — TRACK B: "
        "DENSITY-CAP CAPACITY AT KNOWN 006B GEOMETRY ===",
        flush=True,
    )

    cap_rows: dict[
        float,
        tuple[Any, dict[str, Any]]
    ] = {}

    for mult in (
        1.0,
        2.0,
        4.0,
        8.0,
        16.0,
    ):
        label = (
            "CAPACITY_R5_D0P125_M"
            + str(mult).replace(
                ".",
                "P",
            )
        )

        case, row = solve_capped(
            int14b,
            int14c,
            label,
            20,
            5.0,
            0.125,
            q_payload,
            rho_cap * mult,
            mult,
            current_C,
            c006d,
        )

        cap_rows[
            mult
        ] = (
            case,
            row,
        )

        all_rows.append(
            diag_record(
                "B_DENSITY_CAPACITY",
                label,
                case,
                row,
                current_C,
                c006d,
                mult,
            )
        )

    uncapped_record = diag_record(
        "B_DENSITY_CAPACITY",
        "CAPACITY_R5_D0P125_UNCAPPED",
        recovery_case,
        recovery,
        current_C,
        c006d,
        None,
    )

    all_rows.append(
        uncapped_record
    )

    passing_mults = [
        m
        for m, (_, row)
        in cap_rows.items()
        if diagnostic_green(row)
    ]

    cap_critical_upper = (
        min(passing_mults)
        if passing_mults
        else float("nan")
    )

    cap_critical_lower = 1.0

    if passing_mults:
        lower_candidates = [
            m
            for m
            in cap_rows
            if (
                m < cap_critical_upper
                and not
                diagnostic_green(
                    cap_rows[m][1]
                )
            )
        ]

        if lower_candidates:
            cap_critical_lower = max(
                lower_candidates
            )
        elif diagnostic_green(
            cap_rows[1.0][1]
        ):
            cap_critical_lower = 1.0
            cap_critical_upper = 1.0

    if (
        passing_mults
        and cap_critical_upper
        > cap_critical_lower
    ):
        lo = cap_critical_lower
        hi = cap_critical_upper

        print(
            "CAPACITY_BISECTION_BRACKET="
            f"{lo:.9e},{hi:.9e}"
        )

        for iteration in range(4):
            mid = 0.5 * (
                lo + hi
            )

            label = (
                f"CAPACITY_BISECT_{iteration}_"
                + str(
                    round(
                        mid,
                        8,
                    )
                ).replace(
                    ".",
                    "P",
                )
            )

            case, row = solve_capped(
                int14b,
                int14c,
                label,
                20,
                5.0,
                0.125,
                q_payload,
                rho_cap * mid,
                mid,
                current_C,
                c006d,
            )

            all_rows.append(
                diag_record(
                    "B_DENSITY_BISECTION",
                    label,
                    case,
                    row,
                    current_C,
                    c006d,
                    mid,
                )
            )

            if diagnostic_green(
                row
            ):
                hi = mid
            else:
                lo = mid

        cap_critical_lower = lo
        cap_critical_upper = hi

    cap_obstruction = bool(
        not diagnostic_green(
            cap_rows[1.0][1]
        )
        and diagnostic_green(
            recovery
        )
    )

    print(
        "BASE_CAP_R5_THIN_FEASIBLE="
        + (
            "YES"
            if diagnostic_green(
                cap_rows[1.0][1]
            )
            else "NO"
        )
    )

    print(
        "DENSITY_CAP_IS_A_FEASIBILITY_OBSTRUCTION="
        + (
            "YES"
            if cap_obstruction
            else "NO"
        )
    )

    print(
        "CRITICAL_CAP_MULTIPLIER_LOWER="
        f"{cap_critical_lower:.15e}"
    )

    print(
        "CRITICAL_CAP_MULTIPLIER_UPPER="
        f"{cap_critical_upper:.15e}"
    )

    print(
        "\n=== D — TRACK C: "
        "BASE-CAP STRICT CYLINDRICAL GEOMETRY MATRIX ===",
        flush=True,
    )

    geometry_radii = [
        r99,
        4.0,
        BETA_006B,
        5.0,
        6.0,
    ]

    geometry_depths = [
        0.125,
        0.25,
        0.5,
        1.0,
    ]

    geometry_green = []

    for radius in geometry_radii:
        for depth in geometry_depths:
            label = (
                "BASECAP_R"
                + str(
                    round(
                        radius,
                        6,
                    )
                ).replace(
                    ".",
                    "P",
                )
                + "_D"
                + str(depth).replace(
                    ".",
                    "P",
                )
            )

            case, row = solve_capped(
                int14b,
                int14c,
                label,
                12,
                float(radius),
                float(depth),
                q_payload,
                rho_cap,
                1.0,
                current_C,
                c006d,
            )

            rec = diag_record(
                "C_BASECAP_GEOMETRY",
                label,
                case,
                row,
                current_C,
                c006d,
                1.0,
            )

            all_rows.append(
                rec
            )

            if diagnostic_green(
                row
            ):
                geometry_green.append(
                    (
                        float(
                            row[
                                "coefficient"
                            ]
                        ),
                        radius,
                        depth,
                        case,
                        row,
                    )
                )

    thickness_rescue = bool(
        any(
            depth > 0.125
            for _, _, depth, _, _
            in geometry_green
        )
    )

    if geometry_green:
        geometry_green.sort(
            key=lambda x: x[0]
        )

        (
            scout_C,
            selected_R,
            selected_D,
            selected_case12,
            selected_row12,
        ) = geometry_green[0]

        print(
            "BASECAP_BEST_SCOUT_FOUND=YES"
        )

        print(
            f"BASECAP_BEST_SCOUT_R="
            f"{selected_R:.15e}"
        )

        print(
            f"BASECAP_BEST_SCOUT_DEPTH="
            f"{selected_D:.15e}"
        )

        print(
            f"BASECAP_BEST_SCOUT_C="
            f"{scout_C:.15e}"
        )
    else:
        selected_R = float(
            "nan"
        )

        selected_D = float(
            "nan"
        )

        selected_case12 = None
        selected_row12 = None

        print(
            "BASECAP_BEST_SCOUT_FOUND=NO"
        )

    print(
        "INCREASED_THICKNESS_RESTORES_BASE_CAP_FEASIBILITY="
        + (
            "YES"
            if thickness_rescue
            else "NO"
        )
    )

    refinement = {
        "attempted": False,
        "certified": False,
    }

    if selected_case12 is not None:
        print(
            "\n=== E — TRACK D: "
            "SELECTED BASE-CAP REFINEMENT ===",
            flush=True,
        )

        refine = {}

        for nr in (
            16,
            24,
        ):
            label = (
                f"REFINE_N{nr}_"
                f"R{selected_R:.6f}_"
                f"D{selected_D:.6f}"
            ).replace(
                ".",
                "P",
            )

            case, row = solve_capped(
                int14b,
                int14c,
                label,
                nr,
                selected_R,
                selected_D,
                q_payload,
                rho_cap,
                1.0,
                current_C,
                c006d,
            )

            refine[
                nr
            ] = (
                case,
                row,
            )

            all_rows.append(
                diag_record(
                    "D_REFINEMENT",
                    label,
                    case,
                    row,
                    current_C,
                    c006d,
                    1.0,
                )
            )

        row16 = refine[16][1]
        row24 = refine[24][1]

        refine_green = bool(
            diagnostic_green(
                row16
            )
            and diagnostic_green(
                row24
            )
        )

        if refine_green:
            C16 = float(
                row16[
                    "coefficient"
                ]
            )

            C24 = float(
                row24[
                    "coefficient"
                ]
            )

            Ccons = max(
                C16,
                C24,
            )

            Crel = relerr(
                C16,
                C24,
            )

            width24 = min(
                float(
                    row24.get(
                        "energy_width_cells",
                        0.0,
                    )
                ),
                float(
                    row24.get(
                        "force_width_cells",
                        0.0,
                    )
                ),
            )

            force = (
                int14c.independent_force_reconstruction(
                    refine[24][0],
                    row24,
                )
            )

            force_pass = bool(
                force.get(
                    "pass",
                    False,
                )
                and float(
                    force.get(
                        "relative_error",
                        float("inf"),
                    )
                )
                <= FORCE_REL_TOL
            )

            scs_available = (
                "SCS"
                in cp.installed_solvers()
            )

            if scs_available:
                scs_case, scs_row = (
                    solve_capped(
                        int14b,
                        int14c,
                        "SELECTED_N12_SCS",
                        12,
                        selected_R,
                        selected_D,
                        q_payload,
                        rho_cap,
                        1.0,
                        current_C,
                        c006d,
                        solver="SCS",
                    )
                )

                all_rows.append(
                    diag_record(
                        "D_SOLVER_CROSSCHECK",
                        "SELECTED_N12_SCS",
                        scs_case,
                        scs_row,
                        current_C,
                        c006d,
                        1.0,
                    )
                )

                scs_rel = relerr(
                    float(
                        selected_row12[
                            "coefficient"
                        ]
                    ),
                    float(
                        scs_row.get(
                            "coefficient",
                            float("nan"),
                        )
                    ),
                )

                scs_pass = bool(
                    diagnostic_green(
                        scs_row
                    )
                    and scs_rel
                    <= SCS_REL_TOL
                )
            else:
                scs_rel = float(
                    "nan"
                )

                scs_pass = True

            certified = bool(
                Crel
                <= C_CONV_TOL
                and width24
                >= WIDTH_MIN
                and force_pass
                and scs_pass
            )

            refinement = {
                "attempted": True,
                "green_both": True,
                "C16": C16,
                "C24": C24,
                "conservative_C": Ccons,
                "C_relerr": Crel,
                "width24_min_cells": width24,
                "independent_force":
                    clean_json(force),
                "SCS_available":
                    scs_available,
                "SCS_relerr":
                    scs_rel,
                "SCS_pass":
                    scs_pass,
                "certified":
                    certified,
                "headroom_vs_B7":
                    current_C / Ccons,
                "gain_vs_006D":
                    c006d / Ccons,
            }

            print(
                f"REFINED_C16="
                f"{C16:.15e}"
            )

            print(
                f"REFINED_C24="
                f"{C24:.15e}"
            )

            print(
                "REFINED_CONSERVATIVE_C="
                f"{Ccons:.15e}"
            )

            print(
                "REFINED_C_RELERR="
                f"{Crel:.15e}"
            )

            print(
                "REFINED_N24_MIN_WIDTH_CELLS="
                f"{width24:.15e}"
            )

            print(
                "REFINED_INDEPENDENT_FORCE_RELERR="
                f"{float(force.get('relative_error', float('nan'))):.15e}"
            )

            print(
                "REFINED_INDEPENDENT_FORCE="
                + (
                    "PASS"
                    if force_pass
                    else "FAIL"
                )
            )

            print(
                "REFINED_SCS_RELERR="
                f"{scs_rel:.15e}"
            )

            print(
                "REFINED_SCS_CROSSCHECK="
                + (
                    "PASS"
                    if scs_pass
                    else "FAIL"
                )
            )

            print(
                "REFINED_NUMERICAL_CERTIFICATE="
                + (
                    "PASS"
                    if certified
                    else "FAIL"
                )
            )

            if (
                certified
                and "_arrays"
                in row24
            ):
                np.savez_compressed(
                    OUT_NPZ,
                    **row24[
                        "_arrays"
                    ],
                )

        else:
            refinement = {
                "attempted": True,
                "green_both": False,
                "certified": False,
            }

            print(
                "REFINED_NUMERICAL_CERTIFICATE=FAIL"
            )

    print(
        "\n=== F — CAUSAL DIAGNOSIS ===",
        flush=True,
    )

    print(
        "RADIAL_SUPPORT_OBSTRUCTION="
        + (
            "YES"
            if radial_support_obstruction
            else "NO"
        )
    )

    print(
        "FROZEN_DENSITY_CAP_OBSTRUCTION="
        + (
            "YES"
            if cap_obstruction
            else "NO"
        )
    )

    print(
        "THICKNESS_VOLUME_RESCUE="
        + (
            "YES"
            if thickness_rescue
            else "NO"
        )
    )

    if (
        radial_support_obstruction
        and cap_obstruction
    ):
        diagnosis = (
            "RADIAL_SUPPORT_PLUS_FROZEN_"
            "DENSITY_CAP_COMBINED"
        )
    elif radial_support_obstruction:
        diagnosis = (
            "RADIAL_SUPPORT_PRIMARY"
        )
    elif cap_obstruction:
        diagnosis = (
            "FROZEN_DENSITY_CAP_PRIMARY"
        )
    elif thickness_rescue:
        diagnosis = (
            "VERTICAL_CAPACITY_OR_ASPECT_PRIMARY"
        )
    else:
        diagnosis = (
            "NO_SINGLE_SCANNED_CONSTRAINT_"
            "FULLY_EXPLAINS_024A4"
        )

    print(
        f"024A4_INFEASIBILITY_DIAGNOSIS="
        f"{diagnosis}"
    )

    if refinement.get(
        "certified",
        False,
    ):
        gain006d = float(
            refinement[
                "gain_vs_006D"
            ]
        )

        if gain006d >= MAJOR_RECORD_FACTOR:
            decision = (
                "GREEN_MAJOR_NEW_TRUE_STANDOFF_"
                "SOURCE_RECORD_GE2X_OVER_006D"
            )

            next_action = (
                "024B_MICROSCOPIC_REALIZATION_"
                "PREFILTER_FROM_CORRECTED_"
                "STANDOFF_STRESS_ANATOMY"
            )

        elif gain006d >= NEW_RECORD_FACTOR:
            decision = (
                "GREEN_NEW_TRUE_STANDOFF_"
                "SOURCE_RECORD_OVER_006D"
            )

            next_action = (
                "024B_MICROSCOPIC_REALIZATION_"
                "PREFILTER_FROM_CORRECTED_"
                "STANDOFF_STRESS_ANATOMY"
            )

        else:
            decision = (
                "GREEN_FEASIBILITY_RESTORED_"
                "BUT_006D_REMAINS_BEST_"
                "CERTIFIED_STANDOFF_ANCHOR"
            )

            next_action = (
                "RERANK_006D_MICROSCOPIC_"
                "REALIZATION_VS_023C_023D_"
                "AND_ANALOGUE_ANTIGRAVITY"
            )

    elif (
        radial_support_obstruction
        or cap_obstruction
        or thickness_rescue
    ):
        decision = (
            "YELLOW_024A4_INFEASIBILITY_"
            "CAUSE_IDENTIFIED_NO_NEW_"
            "CERTIFIED_STANDOFF_RECORD"
        )

        next_action = (
            "RERANK_006D_MICROSCOPIC_"
            "REALIZATION_VS_023C_023D_"
            "AND_ANALOGUE_ANTIGRAVITY"
        )

    else:
        decision = (
            "RED_024A4_INFEASIBILITY_"
            "NOT_EXPLAINED_BY_SCANNED_"
            "CAPACITY_GEOMETRY_CONTROLS"
        )

        next_action = (
            "024A4R2_FORMULATION_LEVEL_"
            "CONSTRAINT_AUDIT_BEFORE_"
            "ANY_NEW_FIELD_MODEL"
        )

    fieldnames = sorted(
        {
            key
            for row in all_rows
            for key in row.keys()
            if not isinstance(
                row.get(key),
                (
                    dict,
                    list,
                    tuple,
                    np.ndarray,
                ),
            )
        }
    )

    with OUT_CSV.open(
        "w",
        newline="",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )

        writer.writeheader()

        for row in all_rows:
            writer.writerow(
                {
                    k: row.get(k)
                    for k
                    in fieldnames
                }
            )

    summary = {
        "claim_classification":
            "PROJECT_DERIVED_024A4R_"
            "STANDOFF_FEASIBILITY_DECOMPOSITION",

        "anchors": {
            "current_B7_C":
                current_C,

            "006B_thin_C":
                C006B_THIN,

            "006B_beta":
                BETA_006B,

            "006D_C":
                c006d,

            "024A4_R99":
                r99,

            "024A4_rho_cap":
                rho_cap,
        },

        "positive_controls": {
            "direct_006B_pass":
                direct_pass,

            "direct_006B_C":
                float(
                    direct[
                        "coefficient"
                    ]
                ),

            "generalized_006B_pass":
                recovery_pass,

            "generalized_006B_C":
                recovery_C,

            "generalized_recovery_relerr":
                recovery_rel,
        },

        "radial_support": {
            "scan":
                direct_scan,

            "minimum_tested_feasible_R":
                radial_threshold,

            "R99_below_threshold":
                radial_support_obstruction,
        },

        "density_capacity": {
            "base_cap_R5_thin_feasible":
                diagnostic_green(
                    cap_rows[1.0][1]
                ),

            "cap_is_obstruction":
                cap_obstruction,

            "critical_multiplier_lower":
                cap_critical_lower,

            "critical_multiplier_upper":
                cap_critical_upper,
        },

        "base_cap_geometry": {
            "green_count":
                len(
                    geometry_green
                ),

            "thickness_rescue":
                thickness_rescue,

            "selected_R":
                selected_R,

            "selected_depth":
                selected_D,
        },

        "refinement":
            refinement,

        "causal_diagnosis":
            diagnosis,

        "decision":
            decision,

        "next":
            next_action,

        "density_cap_fundamental":
            False,

        "large_microscopic_solve_authorized":
            bool(
                decision.startswith(
                    "GREEN_NEW"
                )
                or decision.startswith(
                    "GREEN_MAJOR"
                )
            ),

        "current_knowledge_heuristic":
            "APPROXIMATELY_70_TO_71_PERCENT_"
            "NOT_A_PROBABILITY",

        "claim_limits": {
            "source_level_only":
                True,

            "microscopic_realization":
                False,

            "stability":
                False,

            "nonlinear_GR":
                False,

            "practical_device":
                False,
        },
    }

    OUT_JSON.write_text(
        json.dumps(
            clean_json(
                summary
            ),
            indent=2,
            allow_nan=True,
        )
        + "\n"
    )

    print(
        "\n=== G — 024A4R DECISION ===",
        flush=True,
    )

    print(
        "DIRECT_006B_POSITIVE_CONTROL="
        + (
            "PASS"
            if direct_pass
            else "FAIL"
        )
    )

    print(
        "GENERALIZED_006B_POSITIVE_CONTROL="
        + (
            "PASS"
            if recovery_pass
            else "FAIL"
        )
    )

    print(
        "UNCAPPED_MIN_TESTED_FEASIBLE_R_OVER_H="
        f"{radial_threshold:.15e}"
    )

    print(
        "DENSITY_CAP_IS_A_FEASIBILITY_OBSTRUCTION="
        + (
            "YES"
            if cap_obstruction
            else "NO"
        )
    )

    print(
        "CRITICAL_CAP_MULTIPLIER_BRACKET="
        f"{cap_critical_lower:.15e},"
        f"{cap_critical_upper:.15e}"
    )

    print(
        "INCREASED_THICKNESS_RESTORES_BASE_CAP_FEASIBILITY="
        + (
            "YES"
            if thickness_rescue
            else "NO"
        )
    )

    print(
        f"024A4_INFEASIBILITY_DIAGNOSIS="
        f"{diagnosis}"
    )

    if refinement.get(
        "attempted",
        False,
    ):
        print(
            "REFINED_NUMERICAL_CERTIFICATE="
            + (
                "PASS"
                if refinement.get(
                    "certified",
                    False,
                )
                else "FAIL"
            )
        )

        print(
            "REFINED_CONSERVATIVE_C="
            f"{float(refinement.get('conservative_C', float('nan'))):.15e}"
        )

        print(
            "REFINED_HEADROOM_VS_B7="
            f"{float(refinement.get('headroom_vs_B7', float('nan'))):.15e}"
        )

        print(
            "REFINED_GAIN_VS_006D="
            f"{float(refinement.get('gain_vs_006D', float('nan'))):.15e}"
        )

    print(
        "024A4R_STANDOFF_FEASIBILITY_DECOMPOSITION="
        f"{decision}"
    )

    print(
        f"NEXT={next_action}"
    )

    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "APPROXIMATELY_70_TO_71_PERCENT_"
        "NOT_A_PROBABILITY"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_024A4R_"
        "STANDOFF_FEASIBILITY_DECOMPOSITION"
    )

    print(
        f"SUMMARY_JSON="
        f"{OUT_JSON.relative_to(ROOT)}"
    )

    print(
        f"CASES_CSV="
        f"{OUT_CSV.relative_to(ROOT)}"
    )

    print(
        f"BEST_ARRAYS_NPZ="
        f"{OUT_NPZ.relative_to(ROOT)}"
    )

    print(
        "024A4R_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
