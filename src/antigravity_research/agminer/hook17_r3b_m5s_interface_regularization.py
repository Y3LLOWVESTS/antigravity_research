"""B17-M5S: C1/C2 interface derivative regularity and continuum blockers.

This is a diagnostic, not a replacement material operator.
The exact cell-integrated cubic/quintic smoothstep is a controlled
reference for a future same-functional carrier assembly; existing
M5R carrier equations remain unchanged.

Step extrapolation cannot certify spatial convergence.
Sources, enclosure and Earth backgrounds remain prescribed.
No physical Earth momentum reaction, Noether identity, spacecraft
lift or complete device energy is inferred here.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import traceback

BRANCH = "032H17A12D1R3X3B17-ALPHA1R14-M5S-INTERFACE"

PARENT_SHA256 = {
    "m5o": "e75e0b11b05b04a1561d4e1e628e6c6b62c2a7f2c36912b85041bec95b8969d3",
    "m5p": "e49f7eb2ac7f700d0f2608bd556e3729cf0941932704761f9b9118d9607c2243",
    "m5q": "93ed171e95cd4344efd3ca6f36661b977d18383a70c9a319e73c1d79ea12abf0",
    "m5r": "fb6604fbbf054843bce1354b61b8c29285092e766fb6fc2c553a62490af7a66a",
}


def smooth_below(x, edge, width, profile):
    """Independent reference for a C1 or C2 transition."""
    if (
        not math.isfinite(width)
        or width <= 0
        or profile not in ("c1", "c2")
    ):
        raise ValueError("Invalid profile/width")

    u = (x-edge+width)/(2.0*width)

    if u <= 0:
        return 1.0
    if u >= 1:
        return 0.0

    if profile == "c1":
        return 1.0 - 3.0*u*u + 2.0*u*u*u

    return 1.0 - 10.0*u**3 + 15.0*u**4 - 6.0*u**5


def primitive_below(x, edge, width, profile):
    """Continuous exact antiderivative, zero at the left edge."""
    left = edge-width
    right = edge+width

    if x <= left:
        return x-left
    if x >= right:
        return width

    u = (x-left)/(2.0*width)

    if profile == "c1":
        return 2.0*width*(
            u-u**3+0.5*u**4
        )

    if profile == "c2":
        return 2.0*width*(
            u-2.5*u**4+3.0*u**5-u**6
        )

    raise ValueError("Invalid profile")


def cell_average(center, edge, width, h, profile):
    """Exact one-dimensional cell mean, not nodal M5O beta."""
    if not math.isfinite(h) or h <= 0:
        raise ValueError("Invalid mesh spacing")

    a = center-h/2.0
    b = center+h/2.0

    return (
        primitive_below(b, edge, width, profile)
        -primitive_below(a, edge, width, profile)
    )/h


def cell_derivative_edge(center, edge, width, h, profile):
    """Derivative of the same integrated cell functional.

    For f(x-edge):
      d/de (1/h integral[a,b] f(x-edge) dx)
      = (f(a-edge)-f(b-edge))/h.
    """
    a = center-h/2.0
    b = center+h/2.0

    return (
        smooth_below(a, edge, width, profile)
        -smooth_below(b, edge, width, profile)
    )/h


def analytic_cell_audit():
    """Audit cell differentiation and translated boundary flux."""
    rows = []

    for profile in ("c1", "c2"):
        for width in (.25, .5):
            for h in (.25, .125, .1, .0625, .05):
                for phase in (-.5, -.25, 0., .25, .5):
                    n = int(
                        math.ceil((4.0*width+4.0)/h)
                    )

                    centers = [
                        (k-n//2+phase)*h
                        for k in range(n)
                    ]

                    delta = 1.e-4*min(width, h)
                    defects = []
                    collocation = []

                    for x in centers:
                        exact = cell_derivative_edge(
                            x, 0., width, h, profile
                        )

                        finite_difference = (
                            cell_average(
                                x, delta, width, h, profile
                            )
                            -cell_average(
                                x, -delta, width, h, profile
                            )
                        )/(2.0*delta)

                        defects.append(
                            abs(exact-finite_difference)
                        )

                        collocation.append(abs(
                            cell_average(
                                x, 0., width, h, profile
                            )
                            -smooth_below(
                                x, 0., width, profile
                            )
                        ))

                    left = centers[0]-h/2.0
                    right = centers[-1]+h/2.0

                    telescoping = h*sum(
                        cell_derivative_edge(
                            x, 0., width, h, profile
                        )
                        for x in centers
                    )

                    endpoint_flux = (
                        smooth_below(
                            left, 0., width, profile
                        )
                        -smooth_below(
                            right, 0., width, profile
                        )
                    )

                    rows.append({
                        "profile": profile,
                        "width_m": width,
                        "h_m": h,
                        "phase_cells": phase,
                        "max_cell_derivative_fd_defect":
                            max(defects),
                        "integrated_translation_flux_defect":
                            abs(telescoping-endpoint_flux),
                        "max_point_sample_vs_cell_average":
                            max(collocation),
                    })

    return {
        "scope":
            "EXACT_ONE_DIMENSIONAL_CELL_REFERENCE_NOT_COUPLED_TO_CARRIER",
        "rows": rows,
        "max_derivative_defect": max(
            r["max_cell_derivative_fd_defect"]
            for r in rows
        ),
        "max_flux_defect": max(
            r["integrated_translation_flux_defect"]
            for r in rows
        ),
        "point_sampling_differs_from_integrated_profile":
            any(
                r["max_point_sample_vs_cell_average"] > 1.e-5
                for r in rows
            ),
    }


def manifest(mode):
    """Controlled displacement and grid-phase experiment."""
    if mode not in ("quick", "full"):
        raise ValueError(mode)

    out = []

    def add(
        name, *, h, domain, profile, width, step,
        phase=0., resolve=False
    ):
        if any(r["name"] == name for r in out):
            raise ValueError("Duplicate case " + name)

        out.append({
            "name": name,
            "parameters": {
                "h": h,
                "domain": domain,
                "profile": profile,
                "width": width,
                "step": step,
                "phase": phase,
                "resolve": resolve,
            },
        })

    for profile in ("c1", "c2"):
        for step in (.001, .0001):
            add(
                f"{profile}_compact_h125_step{step}",
                h=.125,
                domain="compact",
                profile=profile,
                width=.25,
                step=step,
                resolve=True,
            )

    if mode == "full":
        for profile in ("c1", "c2"):
            for step in (.002, .0005, .00001):
                add(
                    f"{profile}_compact_h125_step{step}",
                    h=.125,
                    domain="compact",
                    profile=profile,
                    width=.25,
                    step=step,
                    resolve=True,
                )

        for profile, width in (
            ("c1", .25),
            ("c2", .5),
        ):
            for h, domain in (
                (.0625, "original"),
                (.05, "original"),
            ):
                for step in (.001, .0001, .00001):
                    add(
                        f"{profile}_{domain}_h{h}_step{step}",
                        h=h,
                        domain=domain,
                        profile=profile,
                        width=width,
                        step=step,
                        resolve=(step != .00001),
                    )

        for profile in ("c1", "c2"):
            for phase in (-.25, .25):
                for step in (.0001, .00001):
                    add(
                        f"{profile}_compact_h0625_phase{phase}_step{step}",
                        h=.0625,
                        domain="compact",
                        profile=profile,
                        width=.25,
                        phase=phase,
                        step=step,
                    )

        # Do not mistake a favorable centered grid phase
        # for a continuum certificate.
        for h in (.0625, .05):
            for phase in (-.25, .25):
                add(
                    f"c2_extended_h{h}_phase{phase}",
                    h=h,
                    domain="extended",
                    profile="c2",
                    width=.5,
                    phase=phase,
                    step=.0001,
                )

    return out


def load_parent(path):
    from antigravity_research.agminer import (
        hook17_r3b_m5r_interaction_closure as m5r,
    )

    parent_path = Path(path).resolve()
    raw = parent_path.read_bytes()
    parent = json.loads(raw)

    valid = (
        parent.get("mode") == "full"
        and parent.get("status")
            == "COMPLETE_NUMERICAL_DIAGNOSTIC_ONLY"
        and parent.get("registered") == 55
        and parent.get("processed") == 55
        and len(parent.get("results", {})) == 55
        and not parent.get("errors")
        and parent.get("source_sha256") == PARENT_SHA256
    )

    if not valid:
        raise ValueError(
            "Not the complete immutable M5R reference bundle"
        )

    if m5r.provenance() != PARENT_SHA256:
        raise ValueError(
            "M5O/M5P/M5Q/M5R provenance drift; fail closed"
        )

    return (
        parent,
        hashlib.sha256(raw).hexdigest(),
        m5r,
    )


def run_case(parameters, m5r):
    row = m5r.run_case(**parameters)

    interaction = row["interaction_only"]
    solved = row["resolved_interaction_derivative"]

    result = {
        "parameters": parameters,
        "earth_analytic_j_m":
            interaction["earth_derivative_j_m"],
        "craft_inferred_j_m":
            interaction["craft_derivative_j_m"],
        "common_j_m":
            interaction["common_derivative_j_m"],
        "earth_difference_fd_minus_analytic_j_m":
            interaction[
                "material_derivative_fd_minus_analytic_j_m"
            ],
        "matched_self_translation_j_m":
            interaction["matched_self_translation_j_m"],
        "max_stationarity_residual":
            row["maximum_stationarity_residual"],
        "max_source_fd_relative_defect":
            row["maximum_analytic_source_fd_relative_defect"],
        "resolved_minus_envelope":
            None if solved is None else {
                "earth_j_m":
                    solved["earth_minus_analytic_j_m"],
                "craft_j_m":
                    solved["craft_minus_inferred_j_m"],
                "common_j_m":
                    solved["common_minus_analytic_j_m"],
            },
    }

    values = [
        value
        for key, value in result.items()
        if key.endswith("_j_m")
        and isinstance(value, (int, float))
    ]

    if not all(math.isfinite(v) for v in values):
        raise ArithmeticError("Nonfinite derivative")

    return result


def summarize(rows, plan, cell_audit, parent):
    by_family = {}

    for name, result in rows.items():
        parameters = result["parameters"]

        key = str((
            parameters["profile"],
            parameters["domain"],
            parameters["h"],
            parameters["width"],
            parameters["phase"],
        ))

        by_family.setdefault(key, []).append({
            "name": name,
            "step_m": parameters["step"],
            "earth_fd_disagreement_j_m": abs(
                result[
                    "earth_difference_fd_minus_analytic_j_m"
                ]
            ),
            "common_j_m": result["common_j_m"],
            "earth_j_m": result["earth_analytic_j_m"],
        })

    families = {}

    for key, sequence in by_family.items():
        sequence.sort(
            key=lambda row: row["step_m"],
            reverse=True,
        )

        coarse = sequence[0]
        fine = sequence[-1]

        families[key] = {
            "series": sequence,
            "coarse_to_fine_step_disagreement_ratio":
                coarse["earth_fd_disagreement_j_m"]
                /max(
                    fine["earth_fd_disagreement_j_m"],
                    1.e-30,
                ),
            "earth_derivative_range_j_m":
                max(x["earth_j_m"] for x in sequence)
                -min(x["earth_j_m"] for x in sequence),
            "common_derivative_range_j_m":
                max(x["common_j_m"] for x in sequence)
                -min(x["common_j_m"] for x in sequence),
        }

    complete = len(rows) == len(plan)

    c1_parent = parent["results"][
        "c1_original_h0.05"
    ]["interaction_only"]

    c2_parent = parent["results"][
        "c2_extended_h0.05"
    ]["interaction_only"]

    cell_ok = (
        cell_audit["max_derivative_defect"] < 2.e-5
        and cell_audit["max_flux_defect"] < 2.e-12
        and cell_audit[
            "point_sampling_differs_from_integrated_profile"
        ]
    )

    resolved = [
        row
        for row in rows.values()
        if row["resolved_minus_envelope"] is not None
    ]

    stationary = bool(rows) and all(
        r["max_stationarity_residual"] < 1.e-7
        and r["max_source_fd_relative_defect"] < 1.e-4
        for r in rows.values()
    )

    resolved_ok = (
        bool(resolved)
        and all(
            abs(r["resolved_minus_envelope"]["common_j_m"])
            < .005
            for r in resolved
        )
    )

    extended = [
        r for r in rows.values()
        if (
            r["parameters"]["profile"] == "c2"
            and r["parameters"]["width"] == .5
            and r["parameters"]["domain"] == "extended"
            and r["parameters"]["h"] == .05
            and r["parameters"]["phase"] in (-.25, .25)
        )
    ]

    # A three-phase screen only: the parent supplies phase zero.
    center = c2_parent

    common_values = [
        center["common_derivative_j_m"]
    ] + [
        r["common_j_m"]
        for r in extended
    ]

    earth_values = [
        center["earth_derivative_j_m"]
    ] + [
        r["earth_analytic_j_m"]
        for r in extended
    ]

    phase_screen = (
        len(extended) == 2
        and max(abs(x) for x in common_values) < .02
        and max(common_values)-min(common_values) < .02
        and max(earth_values)-min(earth_values) < .02
    )

    return {
        "registered": len(plan),
        "completed": len(rows),
        "step_families": families,
        "interface_cell_audit": {
            k: v
            for k, v in cell_audit.items()
            if k != "rows"
        },
        "extended_c2_fine_phase_screen": {
            "count_including_parent_center":
                len(common_values),
            "common_spread_j_m":
                max(common_values)-min(common_values),
            "earth_spread_j_m":
                max(earth_values)-min(earth_values),
            "max_abs_common_j_m":
                max(abs(x) for x in common_values),
        },
        "prior_c1_original_h005_common_j_m":
            c1_parent["common_derivative_j_m"],
        "prior_c2_extended_h005_common_j_m":
            c2_parent["common_derivative_j_m"],
        "gates": {
            "S0_exact_cell_integral_identity":
                "PASS" if cell_ok else "FAIL",
            "S1_original_reduced_action_stationarity":
                "PASS" if complete and stationary
                else "FAIL_OR_PARTIAL",
            "S2_re_solved_action_derivative_self_consistency":
                "PASS" if complete and resolved_ok
                else "FAIL_OR_PARTIAL",
            "S3_C1_non_smooth_step_limit":
                "DIAGNOSTIC_ONLY_NOT_SPATIAL_CERTIFICATE",
            "S4_C1_discrete_operator_subcell_reassembly":
                "NOT_IMPLEMENTED",
            "S5_C2_extended_fine_phase_screen":
                "PASS_SCREEN_ONLY" if phase_screen
                else "BLOCKED_OR_PARTIAL",
            "S5B_C2_continuum_phase_domain_uniqueness":
                "NOT_CERTIFIED",
            "S6_explicit_artificial_assembly_action":
                "NOT_DERIVED",
            "S7_physical_Noether_metric_energy_lift":
                "NOT_ESTABLISHED",
        },
        "artificial_model_100_percent_complete": False,
        "whole_spacecraft_lift_certified": False,
        "006d_replaced": False,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)

    ap.add_argument(
        "--mode",
        choices=("quick", "full"),
        default="quick",
    )
    ap.add_argument(
        "--parent-bundle",
        required=True,
    )
    ap.add_argument(
        "--results-dir",
        default="results/data",
    )
    ap.add_argument("--resume")
    ap.add_argument(
        "--max-new-cases",
        type=int,
    )

    args = ap.parse_args(argv)

    if (
        args.max_new_cases is not None
        and args.max_new_cases < 1
    ):
        ap.error("max-new-cases must be positive")

    try:
        parent, parent_hash, m5r = load_parent(
            args.parent_bundle
        )

        plan = manifest(args.mode)
        cells = analytic_cell_audit()

        current_hash = hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest()

        hashes = {
            **PARENT_SHA256,
            "m5s": current_hash,
        }

    except (ValueError, OSError) as exc:
        ap.error(str(exc))

    if args.resume:
        destination = Path(args.resume).resolve()
        record = json.loads(
            destination.read_text()
        )

        if (
            record.get("branch") != BRANCH
            or record.get("mode") != args.mode
            or record.get("manifest") != plan
            or record.get("source_sha256") != hashes
            or record.get("parent_bundle_sha256")
                != parent_hash
        ):
            ap.error(
                "Resume mismatch: source, manifest or parent changed"
            )

    else:
        folder = Path(args.results_dir)
        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        stamp = datetime.now(
            timezone.utc
        ).strftime("%Y%m%dT%H%M%S%fZ")

        destination = folder / (
            f"b17_m5s_interface_{stamp}_"
            f"{args.mode}_bundle.json"
        )

        record = {
            "branch": BRANCH,
            "mode": args.mode,
            "status": "RUNNING",
            "parent_bundle_sha256": parent_hash,
            "parent_bundle_path": str(
                Path(args.parent_bundle).resolve()
            ),
            "source_sha256": hashes,
            "manifest": plan,
            "registered": len(plan),
            "processed": 0,
            "results": {},
            "errors": {},
            "summary": None,
            "scope":
                "C1_C2_EXACT_CELL_REFERENCE_AND_ORIGINAL_CARRIER_STEP_AUDIT",
            "claims": {
                "physical_antigravity": False,
                "whole_spacecraft_lift": False,
                "complete_energy": False,
            },
        }

    def checkpoint():
        temporary = destination.with_suffix(
            destination.suffix + ".tmp"
        )

        with temporary.open("w") as stream:
            json.dump(
                record,
                stream,
                indent=2,
                sort_keys=True,
                allow_nan=False,
            )
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())

        os.replace(
            temporary,
            destination,
        )

    if not args.resume:
        checkpoint()

    number_new = 0

    try:
        for index, entry in enumerate(plan, 1):
            name = entry["name"]

            if name in record["results"]:
                print(
                    f"[{index}/{len(plan)}] REUSED {name}",
                    flush=True,
                )
                continue

            if (
                args.max_new_cases is not None
                and number_new >= args.max_new_cases
            ):
                record["status"] = "PARTIAL_NOT_CERTIFIED"
                checkpoint()

                print(
                    "RESUME_BUNDLE:",
                    destination,
                    flush=True,
                )
                return 2

            print(
                f"[{index}/{len(plan)}] {name}",
                flush=True,
            )

            try:
                row = run_case(
                    entry["parameters"],
                    m5r,
                )

                record["results"][name] = row
                record["errors"].pop(
                    name,
                    None,
                )

                print(
                    "  Earth / common / derivative defect [J/m]:",
                    f"{row['earth_analytic_j_m']:.9g}",
                    f"{row['common_j_m']:.9g}",
                    f"{row['earth_difference_fd_minus_analytic_j_m']:.9g}",
                    flush=True,
                )

            except Exception:
                record["errors"][name] = traceback.format_exc()

                print(
                    "  CASE ERROR:",
                    record["errors"][name],
                    flush=True,
                )

            record["processed"] = (
                len(record["results"])
                +len(record["errors"])
            )

            number_new += 1
            checkpoint()

        record["summary"] = summarize(
            record["results"],
            plan,
            cells,
            parent,
        )

        gates = record["summary"]["gates"]

        numerical_pass = (
            not record["errors"]
            and gates["S0_exact_cell_integral_identity"]
                == "PASS"
            and gates["S1_original_reduced_action_stationarity"]
                == "PASS"
            and gates[
                "S2_re_solved_action_derivative_self_consistency"
            ] == "PASS"
        )

        record["status"] = (
            "COMPLETE_NUMERICAL_DIAGNOSTIC_ONLY"
            if numerical_pass
            else "FAILED_OR_PARTIAL_NUMERICAL_CONTROLS"
        )

        checkpoint()

        print(
            "UPLOAD_ONLY:",
            destination,
            flush=True,
        )
        print(
            "GATES:",
            json.dumps(
                gates,
                indent=2,
            ),
            flush=True,
        )

        return 0 if numerical_pass else 1

    except KeyboardInterrupt:
        record["status"] = "INTERRUPTED"
        checkpoint()

        print(
            "RESUME_BUNDLE:",
            destination,
            flush=True,
        )
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
