#!/usr/bin/env python3
"""INT-14D — capped thousand-fold final refinement and verification gate.

PURPOSE
-------
Perform the final, predeclared refinement test of the promising finite-density
same-support source class found by INT-14C.

This run does NOT:
- revisit the UV-concentrated unrestricted optimum;
- tune the density cap;
- add smoothing, rigidity, or gradient penalties;
- scan model parameters;
- change support geometry.

It asks one decisive question:

    Does the finite-density R99 matched-core conserved-DEC source remain
    numerically regular and below the >=1000x energy threshold when the
    previously under-resolved force-participation width is refined past the
    unchanged 3-cell resolution gate?

AUTHORIZATION / PRIOR RESULT
----------------------------
INT-14C found:

    current exact-map B=7 coefficient
        C_current ~= 422.222

    fixed density cap
        rho_cap = max(rho) of the unrestricted N12 source
                ~= 1.6698553

    capped N20
        C ~= 0.0596281

    capped N24
        C ~= 0.0599316

so the N20/N24 coefficient changed by only ~0.51%, corresponding to raw
same-support source-class headroom of ~7045x.

The capped branch also passed:
- DEC postchecks;
- exact discrete local conservation;
- Laue balance / active-total identity;
- fixed negative-enclosed-active-core constraint;
- fixed density-cap postcheck;
- independent high-order finite-payload force reconstruction;
- SCS versus CLARABEL cross-check.

The ONLY predeclared INT-14C promotion failure was:

    min(L_E/dx, L_F/dx) >= 3

because at N24

    L_F/dx ~= 1.607.

The physical force participation length itself was already finite:

    L_F ~= 0.2245 h

which is about 5.2 payload radii.

Therefore one final direct refinement is justified.

FROZEN PHYSICS / NUMERICS
-------------------------
The density cap is loaded from the completed INT-14C summary and is never
changed:

    rho <= rho_cap_N12.

This density cap is diagnostic, not a claimed fundamental constant.

Support remains the same source-centered R99 spherical support proxy used in
INT-14B/C.

Payload geometry, matched negative-core fraction, reflection symmetry, DEC,
local conservation, traction-free compact boundary, Laue balance, and target
finite-payload acceleration remain unchanged.

REFINEMENT LADDER
-----------------
Solve only the capped branch at:

    N32 = 32 x 64
    N40 = 40 x 80
    N48 = 48 x 96.

N32 is a bridge diagnostic.

The FINAL convergence pair is N40/N48.

Each completed case is checkpointed to disk so an interrupted run can resume
without repeating successful expensive solves.

UNCHANGED PROMOTION GATES
-------------------------
The final >=1000x finite-density source-class certificate requires:

1. N40 and N48 are green.

2. Conservative coefficient

       C_cons = max(C40, C48)

   satisfies

       C_cons <= C_current / 1000.

3. Coefficient convergence:

       relerr(C40, C48) <= 0.15.

4. Physical energy participation-length convergence:

       relerr(L_E40, L_E48) <= 0.25.

5. Physical outward-force participation-length convergence:

       relerr(L_F40, L_F48) <= 0.25.

6. The unchanged resolution criterion:

       min(L_E48/dx48, L_F48/dx48) >= 3.

7. Peak density respects the fixed N12 cap.

8. Direct postchecks remain green:
   DEC, local conservation, Laue balance, positive total active mass,
   matched negative-enclosed-active-core fraction, target acceleration.

9. Independent high-order N48 payload-force reconstruction agrees with the
   optimization force to <=1e-4 relative error.

10. Independent solver check:
    re-solve the capped N24 problem with SCS and require a green postcheck plus
    <=5% objective disagreement with the prior CLARABEL N24 result.

The thresholds above are inherited unchanged from INT-14C. They are not
relaxed after seeing the answer.

CLAIM IF PASS
-------------
Permitted source-level claim:

    A finite-density, same-R99-support, static conserved-DEC source class
    contains a numerically resolved source with at least 1000x lower
    standardized energy than the present promotion-grade B=7 Skyrmion
    realization under the tested weak-field source constraints.

Even if the numerical coefficient corresponds to several-thousand-fold
headroom, the promotion wording remains conservatively "at least 1000x".

INT Level 3 may then be marked PASS through the simple-source-morphology /
actionable-source-headroom route.

This does NOT establish:
- a microscopic field realization;
- a continuous Skyrmion deformation;
- topology or stability of the efficient source;
- nonlinear Einstein-Skyrme consistency;
- a practical antigravity device.

STOP RULE
---------
If PASS:
    stop source-coefficient polishing immediately;
    proceed to mandatory scaffolding / field-space accessibility.

If FAIL:
    do not continue brute-force global refinement;
    retain INT-14A's robust 12.8-17.9x constructive conserved-DEC headroom;
    retain the capped thousand-fold sequence only as unresolved diagnostics;
    return to field-space accessibility / 023C-023D global reranking.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_INT14D_CAPPED_THOUSANDFOLD_FINAL_REFINEMENT
"""

from __future__ import annotations

import csv
import hashlib
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

INT14B_SUMMARY = DATA / "int14b_support_constrained_structural_overhead_summary.json"
INT14C_SUMMARY = DATA / "int14c_thousandfold_uv_regular_source_summary.json"
INT14C_SOURCE = SIM / "int14c_thousandfold_uv_regular_source_verification.py"

OUT_JSON = DATA / "int14d_capped_thousandfold_final_refinement_summary.json"
OUT_CSV = DATA / "int14d_capped_thousandfold_final_refinement_cases.csv"
OUT_NPZ = DATA / "int14d_capped_thousandfold_final_refinement_N48.npz"
CHECKPOINT_DIR = DATA / "int14d_capped_refinement_checkpoints"

REFINEMENTS = (32, 40, 48)

C_CONVERGENCE_TOL = 0.15
WIDTH_CONVERGENCE_TOL = 0.25
MIN_WIDTH_CELLS = 3.0
INDEPENDENT_FORCE_REL_TOL = 1.0e-4
INDEPENDENT_SOLVER_C_REL_TOL = 0.05
RHO_CAP_REL_TOL = 2.0e-5

DEC_TOL = 3.0e-6
CONS_TOL = 3.0e-6
TRACE_TOL = 3.0e-6
ACTIVE_TOTAL_REL_TOL = 3.0e-6


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


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_case(
    int14c,
    name: str,
    n: int,
    r99: float,
    q_payload: float,
    core_radius: float,
    core_fraction: float,
):
    return int14c.make_case(
        int14c.load_module(
            f"int14d_int14b_case_{n}_{name}",
            int14c.INT14B_SOURCE,
        ),
        name,
        n,
        r99,
        q_payload,
        core_radius,
        core_fraction,
    )


def checkpoint_paths(n: int) -> tuple[Path, Path]:
    return (
        CHECKPOINT_DIR / f"N{n}_metrics.json",
        CHECKPOINT_DIR / f"N{n}_arrays.npz",
    )


def checkpoint_signature(
    *,
    n: int,
    current_C: float,
    rho_cap: float,
    r99: float,
    q_payload: float,
    core_radius: float,
    core_fraction: float,
    int14c_sha: str,
) -> dict[str, Any]:
    return {
        "n": int(n),
        "current_C": float(current_C),
        "rho_cap": float(rho_cap),
        "r99": float(r99),
        "q_payload": float(q_payload),
        "core_radius": float(core_radius),
        "core_fraction": float(core_fraction),
        "int14c_sha256": str(int14c_sha),
    }


def signatures_match(a: dict[str, Any], b: dict[str, Any]) -> bool:
    if str(a.get("int14c_sha256")) != str(b.get("int14c_sha256")):
        return False
    if int(a.get("n", -1)) != int(b.get("n", -2)):
        return False

    for key in (
        "current_C",
        "rho_cap",
        "r99",
        "q_payload",
        "core_radius",
        "core_fraction",
    ):
        av = float(a.get(key, float("nan")))
        bv = float(b.get(key, float("nan")))
        if not (
            math.isfinite(av)
            and math.isfinite(bv)
            and relative_error(av, bv) <= 1.0e-12
        ):
            return False

    return True


def save_checkpoint(
    n: int,
    row: dict[str, Any],
    signature: dict[str, Any],
) -> None:
    CHECKPOINT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    metrics_path, arrays_path = checkpoint_paths(n)

    public = {
        k: v
        for k, v in row.items()
        if k != "_arrays"
    }

    payload = {
        "signature": signature,
        "metrics": public,
    }

    metrics_path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            allow_nan=True,
        )
        + "\n"
    )

    arrays = row.get("_arrays")
    if arrays is not None:
        np.savez_compressed(
            arrays_path,
            **arrays,
        )


def load_checkpoint(
    n: int,
    expected_signature: dict[str, Any],
) -> dict[str, Any] | None:
    metrics_path, arrays_path = checkpoint_paths(n)

    if not (
        metrics_path.is_file()
        and arrays_path.is_file()
    ):
        return None

    payload = json.loads(
        metrics_path.read_text()
    )

    if not signatures_match(
        payload.get("signature", {}),
        expected_signature,
    ):
        return None

    metrics = dict(
        payload["metrics"]
    )

    with np.load(
        arrays_path,
        allow_pickle=False,
    ) as data:
        arrays = {
            key: np.array(
                data[key],
                copy=True,
            )
            for key in data.files
        }

    metrics["_arrays"] = arrays

    return metrics


def public_row(
    int14c,
    row: dict[str, Any],
    current_C: float,
) -> dict[str, Any]:
    return int14c.public_row(
        row,
        current_C,
    )


def print_case(
    int14c,
    label: str,
    row: dict[str, Any],
    current_C: float,
) -> None:
    int14c.print_row(
        label,
        row,
        current_C,
    )

    p = public_row(
        int14c,
        row,
        current_C,
    )

    print(
        f"INT14D_EXTRA={label} "
        f"CORE_FRAC={float(p.get('core_active_fraction', float('nan'))):+.9e} "
        f"ACCEL={float(p.get('acceleration', float('nan'))):.15e} "
        f"ACTIVE_RELERR={float(p.get('active_total_relerr', float('nan'))):.3e} "
        f"DEC={float(p.get('max_dec_violation', float('nan'))):.3e} "
        f"CONS={float(p.get('max_conservation_residual', float('nan'))):.3e} "
        f"TRACE={float(p.get('trace_integral', float('nan'))):.3e} "
        f"CAP_ACTIVE={'YES' if bool(p.get('density_cap_active', False)) else 'NO'}",
        flush=True,
    )


def postcheck_green(
    row: dict[str, Any],
    *,
    rho_cap: float,
    core_fraction_target: float,
) -> bool:
    if not bool(row.get("green", False)):
        return False

    rho = float(
        row.get(
            "max_energy_density",
            float("nan"),
        )
    )
    accel = float(
        row.get(
            "acceleration",
            float("nan"),
        )
    )
    dec = float(
        row.get(
            "max_dec_violation",
            float("inf"),
        )
    )
    cons = float(
        row.get(
            "max_conservation_residual",
            float("inf"),
        )
    )
    trace = float(
        row.get(
            "trace_integral",
            float("inf"),
        )
    )
    active_rel = float(
        row.get(
            "active_total_relerr",
            float("inf"),
        )
    )
    core = float(
        row.get(
            "core_active_fraction",
            float("nan"),
        )
    )

    return bool(
        math.isfinite(rho)
        and rho <= rho_cap * (1.0 + RHO_CAP_REL_TOL)
        and math.isfinite(accel)
        and accel >= 1.0 - 2.0e-5
        and dec < DEC_TOL
        and cons < CONS_TOL
        and abs(trace) < TRACE_TOL
        and active_rel < ACTIVE_TOTAL_REL_TOL
        and math.isfinite(core)
        and core
        <= core_fraction_target
        + 5.0e-7
    )


def main() -> None:
    print(
        "=== INT-14D — CAPPED THOUSAND-FOLD FINAL REFINEMENT ===",
        flush=True,
    )

    for path in (
        INT14B_SUMMARY,
        INT14C_SUMMARY,
        INT14C_SOURCE,
    ):
        require(path)

    b = json.loads(
        INT14B_SUMMARY.read_text()
    )
    c = json.loads(
        INT14C_SUMMARY.read_text()
    )

    current_C = float(
        c["current_C"]
    )
    C1000 = float(
        c["targets"]["C1000"]
    )

    rho_cap = float(
        c["rho_cap"]["value"]
    )

    anatomy = b[
        "exact_support_anatomy"
    ]

    r99 = float(
        anatomy["R99_over_h"]
    )
    q_payload = float(
        anatomy["payload_radius_over_h"]
    )
    core_radius = float(
        anatomy["core_radius_over_h"]
    )
    core_fraction = float(
        anatomy["core_active_fraction"]
    )

    int14c_sha = file_sha256(
        INT14C_SOURCE
    )

    # Prior capped N24 CLARABEL result for the independent SCS recheck.
    prior_capped_cases = (
        c["finite_density"]["cases"]
    )

    prior_n24 = next(
        row
        for row in prior_capped_cases
        if int(row["nr"]) == 24
    )
    prior_n24_C = float(
        prior_n24["coefficient"]
    )

    inherited_scs_pass = bool(
        c["finite_density"].get(
            "SCS_pass",
            False,
        )
    )
    inherited_force_pass = bool(
        c["finite_density"]
        .get(
            "independent_force",
            {},
        )
        .get(
            "pass",
            False,
        )
    )

    print("\n=== A — FROZEN TARGET / AUTHORIZATION ===")
    print(f"CURRENT_C={current_C:.15e}")
    print(f"C_1000_TARGET={C1000:.15e}")
    print(f"FIXED_RHO_CAP_N12={rho_cap:.15e}")
    print(f"R99_OVER_H={r99:.15e}")
    print(f"PAYLOAD_RADIUS_OVER_H={q_payload:.15e}")
    print(f"CORE_RADIUS_OVER_H={core_radius:.15e}")
    print(f"CORE_ACTIVE_FRACTION_TARGET={core_fraction:+.15e}")
    print(f"PRIOR_CAPPED_N24_C={prior_n24_C:.15e}")
    print(
        "INT14C_INHERITED_SCS_CHECK="
        + ("PASS" if inherited_scs_pass else "FAIL")
    )
    print(
        "INT14C_INHERITED_FORCE_CHECK="
        + ("PASS" if inherited_force_pass else "FAIL")
    )
    print(f"INT14C_LOCAL_SOURCE_SHA256={int14c_sha}")
    print("DENSITY_CAP_TUNED_IN_INT14D=NO")
    print("SUPPORT_GEOMETRY_CHANGED_IN_INT14D=NO")
    print("ARBITRARY_SMOOTHING_OR_RIGIDITY_ADDED=NO")

    if not (
        inherited_scs_pass
        and inherited_force_pass
    ):
        raise RuntimeError(
            "INT-14C independent verification prerequisites are not green"
        )

    int14c = load_module(
        "int14d_int14c",
        INT14C_SOURCE,
    )

    rows: dict[int, dict[str, Any]] = {}
    cases: dict[int, Any] = {}

    print(
        "\n=== B — FINAL CAPPED REFINEMENT LADDER ===",
        flush=True,
    )

    for n in REFINEMENTS:
        case = make_case(
            int14c,
            f"INT14D_CAPPED_N{n}",
            n,
            r99,
            q_payload,
            core_radius,
            core_fraction,
        )
        cases[n] = case

        signature = checkpoint_signature(
            n=n,
            current_C=current_C,
            rho_cap=rho_cap,
            r99=r99,
            q_payload=q_payload,
            core_radius=core_radius,
            core_fraction=core_fraction,
            int14c_sha=int14c_sha,
        )

        row = load_checkpoint(
            n,
            signature,
        )

        if row is not None:
            print(
                f"INT14D_CHECKPOINT_REUSED=N{n}",
                flush=True,
            )
        else:
            print(
                f"INT14D_SOLVE_BEGIN=CAPPED_N{n} "
                f"GRID={n}x{2*n}",
                flush=True,
            )

            row = int14c.solve_diagnostic_case(
                int14c.load_module(
                    f"int14d_int14b_solve_{n}",
                    int14c.INT14B_SOURCE,
                ),
                case,
                density_cap=rho_cap,
            )

            save_checkpoint(
                n,
                row,
                signature,
            )

        print_case(
            int14c,
            f"CAPPED_N{n}",
            row,
            current_C,
        )

        rows[n] = row

        if not postcheck_green(
            row,
            rho_cap=rho_cap,
            core_fraction_target=core_fraction,
        ):
            print(
                f"INT14D_EARLY_STOP=N{n}_POSTCHECK_NOT_GREEN"
            )
            break

    n40 = rows.get(40)
    n48 = rows.get(48)

    if n40 is not None and n48 is not None:
        C40 = float(
            n40["coefficient"]
        )
        C48 = float(
            n48["coefficient"]
        )
        LE40 = float(
            n40["energy_effective_length"]
        )
        LE48 = float(
            n48["energy_effective_length"]
        )
        LF40 = float(
            n40["force_effective_length"]
        )
        LF48 = float(
            n48["force_effective_length"]
        )

        C_cons = max(
            C40,
            C48,
        )
        H_cons = (
            current_C
            / C_cons
        )

        C_rel = relative_error(
            C40,
            C48,
        )
        LE_rel = relative_error(
            LE40,
            LE48,
        )
        LF_rel = relative_error(
            LF40,
            LF48,
        )

        width48 = min(
            float(
                n48["energy_width_cells"]
            ),
            float(
                n48["force_width_cells"]
            ),
        )

        rho48 = float(
            n48["max_energy_density"]
        )

        main_numerical_gate = bool(
            postcheck_green(
                n40,
                rho_cap=rho_cap,
                core_fraction_target=core_fraction,
            )
            and postcheck_green(
                n48,
                rho_cap=rho_cap,
                core_fraction_target=core_fraction,
            )
            and C_cons <= C1000
            and C_rel <= C_CONVERGENCE_TOL
            and LE_rel
            <= WIDTH_CONVERGENCE_TOL
            and LF_rel
            <= WIDTH_CONVERGENCE_TOL
            and width48
            >= MIN_WIDTH_CELLS
            and rho48
            <= rho_cap
            * (1.0 + RHO_CAP_REL_TOL)
        )
    else:
        C40 = C48 = float("nan")
        C_cons = H_cons = float("nan")
        C_rel = LE_rel = LF_rel = float("nan")
        width48 = float("nan")
        main_numerical_gate = False

    print("\n=== C — FROZEN N40/N48 GATES ===")
    print(f"C40={C40:.15e}")
    print(f"C48={C48:.15e}")
    print(f"CONSERVATIVE_C40_C48={C_cons:.15e}")
    print(f"CONSERVATIVE_HEADROOM={H_cons:.15e}")
    print(f"C40_C48_REL_DIFF={C_rel:.15e}")
    print(f"ENERGY_LENGTH40_48_REL_DIFF={LE_rel:.15e}")
    print(f"FORCE_LENGTH40_48_REL_DIFF={LF_rel:.15e}")
    print(f"N48_MIN_WIDTH_CELLS={width48:.15e}")
    print(
        "N40_N48_FROZEN_NUMERICAL_GATE="
        + ("PASS" if main_numerical_gate else "FAIL")
    )

    # Independent N48 force reconstruction only if the numerical gate survives.
    force_check: dict[str, Any] = {
        "pass": False,
        "reason": "NUMERICAL_GATE_NOT_PASSED",
    }

    if main_numerical_gate:
        print(
            "\n=== D — INDEPENDENT N48 HIGH-ORDER FORCE RECONSTRUCTION ===",
            flush=True,
        )

        force_check = (
            int14c.independent_force_reconstruction(
                cases[48],
                rows[48],
            )
        )

        print(
            f"INDEPENDENT_N48_FORCE_BASE="
            f"{float(force_check['acceleration_base']):.15e}"
        )
        print(
            f"INDEPENDENT_N48_FORCE_HI="
            f"{float(force_check['acceleration_independent']):.15e}"
        )
        print(
            f"INDEPENDENT_N48_FORCE_RELERR="
            f"{float(force_check['relative_error']):.15e}"
        )
        print(
            "INDEPENDENT_N48_FORCE="
            + (
                "PASS"
                if bool(force_check["pass"])
                else "FAIL"
            )
        )

    # Independent solver recheck at N24. Run only if the main N40/N48
    # refinement and independent N48 force have survived.
    scs_pass = False
    scs_rel = float("nan")
    scs_row: dict[str, Any] | None = None

    if (
        main_numerical_gate
        and bool(force_check.get("pass", False))
    ):
        print(
            "\n=== E — INDEPENDENT SCS N24 SOLVER RECHECK ===",
            flush=True,
        )

        if "SCS" in cp.installed_solvers():
            scs_case = make_case(
                int14c,
                "INT14D_CAPPED_N24_SCS",
                24,
                r99,
                q_payload,
                core_radius,
                core_fraction,
            )

            scs_row = int14c.solve_diagnostic_case(
                int14c.load_module(
                    "int14d_int14b_scs",
                    int14c.INT14B_SOURCE,
                ),
                scs_case,
                density_cap=rho_cap,
                solver_override="SCS",
            )

            print_case(
                int14c,
                "CAPPED_N24_SCS",
                scs_row,
                current_C,
            )

            scs_C = float(
                scs_row.get(
                    "coefficient",
                    float("nan"),
                )
            )

            if math.isfinite(scs_C):
                scs_rel = relative_error(
                    scs_C,
                    prior_n24_C,
                )

            scs_pass = bool(
                postcheck_green(
                    scs_row,
                    rho_cap=rho_cap,
                    core_fraction_target=core_fraction,
                )
                and scs_rel
                <= INDEPENDENT_SOLVER_C_REL_TOL
            )

            print(
                f"SCS_N24_CLARABEL_N24_C_REL_DIFF="
                f"{scs_rel:.15e}"
            )
            print(
                "INDEPENDENT_SCS_N24_RECHECK="
                + ("PASS" if scs_pass else "FAIL")
            )
        else:
            print(
                "INDEPENDENT_SCS_N24_RECHECK=UNAVAILABLE"
            )

    final_pass = bool(
        main_numerical_gate
        and bool(
            force_check.get(
                "pass",
                False,
            )
        )
        and scs_pass
    )

    print(
        "\n=== F — FINAL THOUSAND-FOLD DECISION ==="
    )
    print(
        "THOUSANDFOLD_FINITE_DENSITY_FINAL_VERIFICATION="
        + ("PASS" if final_pass else "FAIL")
    )

    if final_pass:
        decision = (
            "VERIFIED_GE1000X_FINITE_DENSITY_SAME_SUPPORT_"
            "CONSERVED_DEC_SOURCE_CLASS"
        )
        level3 = True
        next_action = (
            "INT09_MANDATORY_SCAFFOLDING_AND_FIELD_SPACE_ACCESSIBILITY"
        )
    else:
        decision = (
            "GE1000X_FINITE_DENSITY_FINAL_REFINEMENT_NOT_VERIFIED"
        )
        level3 = False
        next_action = (
            "STOP_SOURCE_COEFFICIENT_POLISHING_RETAIN_INT14A_"
            "AND_RETURN_TO_FIELD_SPACE_ACCESSIBILITY_OR_023C_023D_RERANK"
        )

    print(
        "INT_LEVEL_3_FORMAL="
        + ("PASS" if level3 else "NOT_YET")
    )
    print(f"INT14D_DECISION={decision}")
    print(
        "PROMOTED_HEADROOM_WORDING="
        + (
            "AT_LEAST_1000X"
            if final_pass
            else "NONE"
        )
    )
    print(
        "RAW_NUMERICAL_HEADROOM_FOR_CONTEXT="
        f"{H_cons:.15e}"
    )
    print("DENSITY_CAP_IS_FUNDAMENTAL_PHYSICS=NO")
    print("MICROSCOPIC_FIELD_REALIZATION=NOT_ESTABLISHED")
    print("FULL_HESSIAN_STABILITY=NOT_ESTABLISHED")
    print("NONLINEAR_EINSTEIN_SKYRME=NOT_ESTABLISHED")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print(f"NEXT={next_action}")
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_INT14D_CAPPED_THOUSANDFOLD_FINAL_REFINEMENT"
    )

    public_rows = [
        public_row(
            int14c,
            row,
            current_C,
        )
        for _, row in sorted(
            rows.items()
        )
    ]

    if scs_row is not None:
        public_rows.append(
            public_row(
                int14c,
                scs_row,
                current_C,
            )
        )

    if public_rows:
        fields = sorted({
            key
            for row in public_rows
            for key in row.keys()
        })

        with OUT_CSV.open(
            "w",
            newline="",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=fields,
            )
            writer.writeheader()
            writer.writerows(
                public_rows
            )

    if 48 in rows:
        arrays48 = rows[48].get(
            "_arrays",
            {},
        )

        extra = {}
        if "kernels_hi" in force_check:
            extra[
                "independent_kernels_hi"
            ] = force_check[
                "kernels_hi"
            ]

        np.savez_compressed(
            OUT_NPZ,
            **arrays48,
            **extra,
        )

    summary = {
        "claim_classification": (
            "PROJECT_DERIVED_INT14D_CAPPED_THOUSANDFOLD_FINAL_REFINEMENT"
        ),
        "decision": decision,
        "next": next_action,
        "current_C": current_C,
        "C1000": C1000,
        "rho_cap": {
            "value": rho_cap,
            "source": (
                "INT14C_UNRESTRICTED_N12_MAX_ENERGY_DENSITY"
            ),
            "fundamental_physics": False,
            "tuned_in_int14d": False,
        },
        "support": {
            "R99_over_h": r99,
            "payload_radius_over_h": q_payload,
            "core_radius_over_h": core_radius,
            "core_active_fraction_target": core_fraction,
            "changed_in_int14d": False,
        },
        "thresholds": {
            "C_convergence": C_CONVERGENCE_TOL,
            "energy_length_convergence": WIDTH_CONVERGENCE_TOL,
            "force_length_convergence": WIDTH_CONVERGENCE_TOL,
            "minimum_width_cells": MIN_WIDTH_CELLS,
            "independent_force_relerr": INDEPENDENT_FORCE_REL_TOL,
            "independent_solver_C_relerr": INDEPENDENT_SOLVER_C_REL_TOL,
        },
        "cases": public_rows,
        "final_pair": {
            "C40": C40,
            "C48": C48,
            "conservative_C": C_cons,
            "conservative_headroom": H_cons,
            "C_rel_diff": C_rel,
            "energy_length_rel_diff": LE_rel,
            "force_length_rel_diff": LF_rel,
            "N48_min_width_cells": width48,
            "numerical_gate_pass": main_numerical_gate,
        },
        "independent_force": {
            key: value
            for key, value
            in force_check.items()
            if key != "kernels_hi"
        },
        "independent_solver": {
            "SCS_N24_pass": scs_pass,
            "SCS_N24_vs_CLARABEL_N24_C_rel_diff": scs_rel,
        },
        "gates": {
            "thousandfold_finite_density_final_verification": final_pass,
            "int_level_3_formal": level3,
        },
        "claim_limits": {
            "density_cap_fundamental": False,
            "microscopic_field_realization": False,
            "continuous_skyrmion_deformation": False,
            "full_hessian_stability": False,
            "strict_N73": False,
            "nonlinear_einstein_skyrme": False,
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

    print(f"INT14D_SUMMARY_JSON={OUT_JSON}")
    print(f"INT14D_CASES_CSV={OUT_CSV}")
    print(f"INT14D_N48_NPZ={OUT_NPZ}")
    print(f"INT14D_CHECKPOINT_DIR={CHECKPOINT_DIR}")
    print("INT14D_RUN_COMPLETE=YES")


if __name__ == "__main__":
    main()
