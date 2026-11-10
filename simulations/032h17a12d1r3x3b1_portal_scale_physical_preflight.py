"""R3X3B1 — physically linked portal-scale and payload-loading gate.

MODEL
-----
Universal metric: g_phys = exp(2 sigma) g
Topological portal: sigma = (F *Fdual)/(2 M_X^4)

For t = (M0/M_X)^4, increase the external source amplitude
by 1/sqrt(t). The preloaded metric response stays fixed, while
the reciprocal finite-matter loading operator scales by t.
Canonical Maxwell energy scales by 1/t.

Uses corrected R3X1 frozen-density Lorentzian loading equations.

LIMITATIONS
-----------
Field-only numerical preflight; not an independently physicalized
source, parity/CP completion, continuum limit, nonlinear action,
complete operating-energy certification, or demonstrated device.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    REFERENCE_PORTAL_SCALE_EV,
    TARGET_ACCELERATION_M_S2,
)
from antigravity_research.agminer.hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    _build_baseline_and_prep,
    _solve_loaded,
    _state,
    _direct_compare,
)

ENERGY_LIMIT_J = 10_000_000.0


def linked_scale(t: float) -> dict:
    if not math.isfinite(t) or not (0 < t <= 1):
        raise ValueError("t must satisfy 0 < t <= 1")

    m = REFERENCE_PORTAL_SCALE_EV * t**(-0.25)

    return {
        "M_X_eV": float(m),
        "relative_matter_loading": t,
        "source_amplitude_factor": t**(-0.5),
        "field_energy_factor": t**(-1),
        "preloaded_metric_invariant_ratio":
            t**(-1) * (REFERENCE_PORTAL_SCALE_EV / m)**4,
    }


def parity_bulk_gate() -> dict:
    # d[T*sigma'(P)] =
    # sigma'(P)*dT + T*sigma''(P)*dP
    #
    # Generic constant-T bulk silence requires sigma'' = 0.
    # Therefore sigma = a + b*P.
    #
    # P/CP symmetry with only one pseudoscalar P requires b = 0.

    return {
        "affine_sigma_generic_bulk_silent": True,
        "nonconstant_affine_single_P_is_parity_odd": True,
        "nonlinear_even_sigma_restores_bulk_loading": True,
        "scope": "ONE_P_NO_INDEPENDENT_ODD_SPURION",
        "new_compensator_certified": False,
    }


def run(grids, ratios):
    records = []

    for h in grids:
        setup = _build_baseline_and_prep(h)
        rows = []

        for t in ratios:
            identity = linked_scale(t)

            assert math.isclose(
                identity["preloaded_metric_invariant_ratio"],
                1.0,
                rel_tol=1e-12,
            )

            solution = _solve_loaded(setup["prep"], t, 1.0)

            if not solution.get("success"):
                raise RuntimeError(
                    f"LOADED_SOLVER_FAILED: h={h}, t={t}"
                )

            state = _state(setup, solution)
            a_min = float(
                state["minimum_payload_acceleration_m_s2"]
            )

            row = {
                "t": t,
                "M_X_keV": identity["M_X_eV"] / 1000,
                "loaded_min_acceleration_before_adjustment":
                    a_min,
                "outward_everywhere_sampled": a_min > 0,
            }

            if a_min > 0:
                adjustment = TARGET_ACCELERATION_M_S2 / a_min

                energy = (
                    state["canonical_field_energy_j"]
                    * adjustment / t
                )

                row.update({
                    "canonical_field_energy_1g_j": float(energy),
                    "field_only_under_10MJ":
                        energy < ENERGY_LIMIT_J,
                    "required_source_amplitude_vs_1keV":
                        math.sqrt(adjustment / t),
                    "static_condition_number":
                        solution["condition_number"],
                    "static_relative_residual":
                        solution["relative_residual"],
                })

            if h == 0.05 and math.isclose(
                t, 5e-6, rel_tol=0, abs_tol=1e-15
            ):
                direct = _direct_compare(
                    setup, solution, t, 1.0
                )
                row["direct_solver_validation"] = direct
                assert direct["pass"]

            rows.append(row)

            print(
                f"h={h:.3f}m "
                f"M={identity['M_X_eV']/1000:.3f}keV "
                f"t={t:.1e} "
                f"a_min={a_min:.6f} "
                f"E_1g={row.get('canonical_field_energy_1g_j')}",
                flush=True,
            )

        records.append({
            "h_m": h,
            "payload_grid_points":
                int(setup["field"]["payload"].sum()),
            "rows": rows,
        })

    result = {
        "branch":
            "032H17A12D1R3X3B1_LINKED_PORTAL_SCALE_PREFLIGHT",
        "theory_scope":
            "CORRECTED_LORENTZIAN_FROZEN_BETA_ONLY",
        "parity_bulk_gate": parity_bulk_gate(),
        "grids": records,
        "microscopic_source_realized": False,
        "parity_CP_completed": False,
        "continuum_certified": False,
        "complete_operating_energy_certified": False,
        "physical_antigravity_model_found": False,
        "006d_replaced": False,
    }

    output = Path(
        "results/data/"
        "032h17a12d1r3x3b1_portal_scale_physical_preflight.json"
    )

    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )

    print("RESULT_PATH=", output)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--grids",
        nargs="+",
        type=float,
        default=[0.075, 0.05, 0.04],
    )

    parser.add_argument(
        "--ratios",
        nargs="+",
        type=float,
        default=[1e-6, 5e-6],
    )

    args = parser.parse_args()
    run(tuple(args.grids), tuple(args.ratios))
