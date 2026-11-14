"""B17-M5U-X: final artificial-model numerical decision audit.

Reuses M5R/M5S/M5T evidence with SHA-256 provenance and adds
predeclared exterior-boundary, mesh, grid-phase, source-quadrature,
displacement-step, cell-integration, and negative-control experiments.

M5R and M5T remain DIFFERENT discretized boundary-value problems.
This run does not silently merge their actions or claim the port exists.

Artificial action completeness, physical Earth reaction, onboard hull
lift, and complete physical operating energy are NOT established.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import traceback
from datetime import datetime, timezone

BRANCH = (
    "032H17A12D1R3X3B17-ALPHA1R16-M5U-DECISION"
)

PARENT_SPECS = {
    "m5r": (
        "b17_m5r_interaction_*_full_bundle.json", 55
    ),
    "m5s": (
        "b17_m5s_interface_*_full_bundle.json", 34
    ),
    "m5t": (
        "b17_m5t_material_*_full_bundle.json", 21
    ),
}

MODULE_NAMES = {
    "m5o": "hook17_r3b_m5o_fixed_box",
    "m5p": "hook17_r3b_m5p_exterior_boundary",
    "m5q": "hook17_r3b_m5q_translation_balance",
    "m5r": "hook17_r3b_m5r_interaction_closure",
    "m5s": "hook17_r3b_m5s_interface_regularization",
    "m5t": "hook17_r3b_m5t_variational_cell_material",
}


def digest(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def choose_parent(folder, pattern, count):
    candidates = sorted(
        folder.glob(pattern),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    for path in candidates:
        try:
            record = json.loads(path.read_text())
        except (ValueError, OSError):
            continue

        if (
            record.get("mode") == "full"
            and record.get("status")
                == "COMPLETE_NUMERICAL_DIAGNOSTIC_ONLY"
            and not record.get("errors")
            and len(record.get("results", {})) == count
            and record.get("manifest")
        ):
            return path.resolve(), record

    raise RuntimeError(
        "No complete full parent matches " + pattern
    )


def parents_and_code(folder):
    data = {}

    for name, (pattern, count) in PARENT_SPECS.items():
        path, record = choose_parent(
            folder, pattern, count
        )

        data[name] = {
            "path": str(path),
            "sha256": digest(path),
            "data": record,
        }

    if (
        data["m5s"]["data"].get("parent_bundle_sha256")
        != data["m5r"]["sha256"]
    ):
        raise RuntimeError(
            "M5S does not reference selected M5R bundle"
        )

    if set(
        data["m5r"]["data"].get(
            "source_sha256", {}
        )
    ) != {"m5o", "m5p", "m5q", "m5r"}:
        raise RuntimeError(
            "Malformed M5R source provenance"
        )

    modules = {}
    hashes = {}

    prefix = "antigravity_research.agminer."

    for name, shortname in MODULE_NAMES.items():
        module = importlib.import_module(
            prefix + shortname
        )

        modules[name] = module
        hashes[name] = digest(module.__file__)

    for name in ("m5o", "m5p", "m5q", "m5r"):
        expected = data["m5r"]["data"][
            "source_sha256"
        ][name]

        if hashes[name] != expected:
            raise RuntimeError(
                "M5R parent/source drift: " + name
            )

    if (
        hashes["m5s"]
        != data["m5s"]["data"][
            "source_sha256"
        ]["m5s"]
    ):
        raise RuntimeError("M5S source drift")

    if (
        hashes["m5t"]
        != data["m5t"]["data"]["module_sha256"]
    ):
        raise RuntimeError("M5T source drift")

    if (
        modules["m5r"].provenance()
        != data["m5r"]["data"]["source_sha256"]
    ):
        raise RuntimeError(
            "M5R self-provenance disagreement"
        )

    modules["m5t"].validate_legacy_provenance()

    public = {
        name: {
            "path": entry["path"],
            "sha256": entry["sha256"],
            "cases": len(entry["data"]["results"]),
        }
        for name, entry in data.items()
    }

    return data, modules, hashes, public


def make_manifest(mode="quick"):
    if mode not in ("quick", "full"):
        raise ValueError(mode)

    jobs = []

    def add(name, backend, **parameters):
        if any(
            job["name"] == name for job in jobs
        ):
            raise AssertionError(
                "Duplicate job name: " + name
            )

        # Never recompute a parameter tuple merely
        # because it was assigned another label.
        if any(
            job["backend"] == backend
            and job["parameters"] == parameters
            for job in jobs
        ):
            return

        jobs.append({
            "name": name,
            "backend": backend,
            "parameters": parameters,
        })

    # Five-case preflight, retained in the full manifest.
    add(
        "c2_ext_h005_phneg05",
        "m5r",
        h=.05,
        domain="extended",
        phase=-.5,
    )

    add(
        "c2_orig_h005_phpos05",
        "m5r",
        h=.05,
        domain="original",
        phase=.5,
    )

    add(
        "c2_compact_h004_center",
        "m5r",
        h=.04,
        domain="compact",
        resolve=True,
    )

    add(
        "c2_ext_h005_zero_source",
        "m5r",
        h=.05,
        domain="extended",
        zero_source=True,
    )

    add(
        "cell_c2_h02_q16",
        "m5t",
        h=.2,
        profile="c2",
        width=.5,
        order=16,
        step=1.e-4,
    )

    if mode == "quick":
        return jobs

    # New spatial resolution, fixed physical domains,
    # and source/grid phase controls.
    for domain in (
        "compact", "original", "extended"
    ):
        if domain != "compact":
            add(
                f"c2_{domain}_h004_center",
                "m5r",
                h=.04,
                domain=domain,
                resolve=(domain == "original"),
            )

        for phase in (-.25, .25):
            add(
                f"c2_{domain}_h004_phase{phase:+g}",
                "m5r",
                h=.04,
                domain=domain,
                phase=phase,
            )

    for domain in (
        "compact", "original", "extended"
    ):
        for phase in (-.5, .5):
            name = (
                f"c2_{domain}_h005_phase{phase:+g}"
            )

            if any(
                item["name"] == name
                for item in jobs
            ):
                continue

            add(
                name,
                "m5r",
                h=.05,
                domain=domain,
                phase=phase,
            )

    # The three boundary closures are NOT presumed
    # interchangeable at a finite exterior boundary.
    for domain in ("original", "extended"):
        for h in (.0625, .05):
            for closure in (
                "dipole_robin", "dirichlet"
            ):
                add(
                    f"c2_{domain}_h{h}_b{closure}",
                    "m5r",
                    h=h,
                    domain=domain,
                    closure=closure,
                )

    # Source-deposition quadrature, distinct from
    # M5T material-cell quadrature.
    for order in (4, 8, 12):
        add(
            f"c2_original_h005_source_q{order}",
            "m5r",
            h=.05,
            domain="original",
            order=order,
        )

    # Earth/craft/common derivatives must be
    # independently re-solved at multiple steps.
    for domain in ("original", "extended"):
        for step in (1.e-3, 1.e-5):
            add(
                f"c2_{domain}_h005_step{step}",
                "m5r",
                h=.05,
                domain=domain,
                step=step,
                resolve=True,
            )

    add(
        "c2_original_h004_no_source",
        "m5r",
        h=.04,
        domain="original",
        zero_source=True,
    )

    # Historical alternate interface: falsification.
    add(
        "c1_original_h004_step1e5",
        "m5r",
        h=.04,
        domain="original",
        profile="c1",
        width=.25,
        step=1.e-5,
        resolve=True,
    )

    # A distinct material-width experiment, not
    # a convergence comparison with width 0.5 m.
    add(
        "c2_width025_orig_h004",
        "m5r",
        h=.04,
        domain="original",
        profile="c2",
        width=.25,
    )

    # Independently integrated material response:
    # unchanged old Dirichlet carrier and source.
    for h in (.25, .2):
        add(
            f"cell_c1_h{h}_q16",
            "m5t",
            h=h,
            profile="c1",
            width=.25,
            order=16,
            step=1.e-4,
        )

        if h == .25:
            add(
                "cell_c2_h025_q16",
                "m5t",
                h=h,
                profile="c2",
                width=.5,
                order=16,
                step=1.e-4,
            )

        add(
            f"cell_c2_h{h}_step1e6",
            "m5t",
            h=h,
            profile="c2",
            width=.5,
            order=8,
            step=1.e-6,
        )

        add(
            f"cell_zero_h{h}",
            "m5t",
            h=h,
            profile="c2",
            width=.5,
            order=8,
            step=1.e-4,
            zero_source=True,
        )

    return jobs


def run_one(job, modules):
    if job["backend"] == "m5r":
        return modules["m5r"].run_case(
            **job["parameters"]
        )

    if job["backend"] == "m5t":
        return modules["m5t"].evaluate(
            **job["parameters"]
        )

    raise ValueError("Unknown backend")


def picked(
    rows,
    *,
    profile="c2",
    width=.5,
    closure="dipole_trace",
    domain=None,
    phase=None,
    h=None,
    zero_source=False,
):
    matches = []

    for row in rows:
        if (
            row["profile"] != profile
            or row["width_m"] != width
        ):
            continue

        if (
            row["closure"] != closure
            or row["zero_source"] != zero_source
        ):
            continue

        if (
            domain is not None
            and row["domain"] != domain
        ):
            continue

        if (
            phase is not None
            and abs(row["phase_cells"] - phase) > 1.e-10
        ):
            continue

        if (
            h is not None
            and abs(row["mesh_h_m"] - h) > 1.e-10
        ):
            continue

        matches.append(row)

    return matches


def analyze(record, parents):
    old = list(
        parents["m5r"]["data"]["results"].values()
    )

    new = [
        result
        for name, result in record["results"].items()
        if next(
            job["backend"]
            for job in record["manifest"]
            if job["name"] == name
        ) == "m5r"
    ]

    rows = old + new

    def best(
        domain,
        h,
        phase=0.,
        closure="dipole_trace",
        profile="c2",
        width=.5,
    ):
        possible = picked(
            rows,
            domain=domain,
            h=h,
            phase=phase,
            closure=closure,
            profile=profile,
            width=width,
        )

        if not possible:
            return None

        canonical = sorted(
            possible,
            key=lambda r: abs(
                r["derivative_step_m"] - 1.e-4
            ),
        )

        return canonical[0]["interaction_only"]

    def scalar(result, key):
        return (
            None if result is None
            else float(result[key])
        )

    domains = (
        "compact", "original", "extended"
    )

    hs = (.1, .0625, .05, .04)

    mesh = {}

    for domain in domains:
        mesh[domain] = [
            {
                "h_m": h,
                "earth_j_m": scalar(
                    best(domain, h),
                    "earth_derivative_j_m",
                ),
                "common_j_m": scalar(
                    best(domain, h),
                    "common_derivative_j_m",
                ),
            }
            for h in hs
        ]

    phases = {}

    for domain in domains:
        for h in (.0625, .05, .04):
            sampled = []

            for phase in (
                -.5, -.25, 0., .25, .5
            ):
                result = best(
                    domain, h, phase=phase
                )

                if result is not None:
                    sampled.append({
                        "phase": phase,
                        "earth_j_m": scalar(
                            result,
                            "earth_derivative_j_m",
                        ),
                        "common_j_m": scalar(
                            result,
                            "common_derivative_j_m",
                        ),
                    })

            if len(sampled) >= 3:
                earth = [
                    r["earth_j_m"] for r in sampled
                ]

                common = [
                    r["common_j_m"] for r in sampled
                ]

                phases[f"{domain}:h={h}"] = {
                    "values": sampled,
                    "earth_spread_j_m":
                        max(earth)-min(earth),
                    "common_spread_j_m":
                        max(common)-min(common),
                    "max_abs_common_j_m":
                        max(map(abs, common)),
                }

    boundary = {}

    for domain in domains:
        for h in (.1, .0625, .05):
            reference = best(domain, h)

            if reference is None:
                continue

            variants = {}

            for closure in (
                "dipole_robin", "dirichlet"
            ):
                alternate = best(
                    domain, h, closure=closure
                )

                if alternate is not None:
                    variants[closure] = {
                        "earth_difference_from_trace_j_m":
                            alternate[
                                "earth_derivative_j_m"
                            ] - reference[
                                "earth_derivative_j_m"
                            ],
                        "common_difference_from_trace_j_m":
                            alternate[
                                "common_derivative_j_m"
                            ] - reference[
                                "common_derivative_j_m"
                            ],
                    }

            if variants:
                boundary[f"{domain}:h={h}"] = variants

    # Paired h^2 extrapolations are diagnostics.
    # Agreement is not a theorem of continuum convergence.
    extrapolation = {}

    for domain in domains:
        def intercept(a, b):
            xa = best(domain, a)
            xb = best(domain, b)

            if xa is None or xb is None:
                return None

            fa = xa["earth_derivative_j_m"]
            fb = xb["earth_derivative_j_m"]

            return (
                a*a*fb - b*b*fa
            ) / (a*a - b*b)

        estimate1 = intercept(.0625, .05)
        estimate2 = intercept(.05, .04)

        extrapolation[domain] = {
            "quadratic_h2_intercept_0625_05_j_m":
                estimate1,
            "quadratic_h2_intercept_05_04_j_m":
                estimate2,
            "intercept_disagreement_j_m": (
                None
                if estimate1 is None
                or estimate2 is None
                else estimate2-estimate1
            ),
            "not_a_continuum_certificate": True,
        }

    def value(domain, h, key):
        result = best(domain, h)

        return (
            None if result is None
            else result[key]
        )

    strong_terms = [
        value(
            "extended", .04,
            "earth_derivative_j_m",
        ),
        value(
            "original", .04,
            "earth_derivative_j_m",
        ),
        value(
            "extended", .05,
            "earth_derivative_j_m",
        ),
        value(
            "extended", .04,
            "common_derivative_j_m",
        ),
    ]

    fine_available = all(
        item is not None for item in strong_terms
    )

    fine_domain_difference = (
        abs(strong_terms[0]-strong_terms[1])
        if fine_available else None
    )

    fine_mesh_difference = (
        abs(strong_terms[0]-strong_terms[2])
        if fine_available else None
    )

    fine_max_common = (
        abs(strong_terms[3])
        if fine_available else None
    )

    phase04 = phases.get("extended:h=0.04")

    phase_screen = (
        phase04 is not None
        and len(phase04["values"]) >= 3
        and phase04["earth_spread_j_m"] < .01
        and phase04["max_abs_common_j_m"] < .01
    )

    # Exploratory tolerances only. They are NOT
    # empirical constraints or physical force certificates.
    finite_screen = (
        fine_available
        and fine_domain_difference < .005
        and fine_mesh_difference < .08
        and fine_max_common < .01
        and phase_screen
    )

    controls = []

    for row in new:
        if row["zero_source"]:
            interaction = row["interaction_only"]

            controls.append({
                "domain": row["domain"],
                "h": row["mesh_h_m"],
                "max_abs": max(
                    abs(row[
                        "interaction_action_difference_j"
                    ]),
                    abs(interaction[
                        "earth_derivative_j_m"
                    ]),
                    abs(interaction[
                        "craft_derivative_j_m"
                    ]),
                    abs(interaction[
                        "common_derivative_j_m"
                    ]),
                ),
            })

    negative_pass = (
        bool(controls)
        and all(
            item["max_abs"] < 1.e-10
            for item in controls
        )
    )

    # Require EACH independent derivative; never
    # accept cancellation in the common sum alone.
    resolved_checks = []

    for row in new:
        resolved = row.get(
            "resolved_interaction_derivative"
        )

        if resolved is None:
            continue

        resolved_checks.append({
            "domain": row["domain"],
            "h": row["mesh_h_m"],
            "profile": row["profile"],
            "max_abs_j_m": max(
                abs(resolved[key])
                for key in (
                    "earth_minus_analytic_j_m",
                    "craft_minus_inferred_j_m",
                    "common_minus_analytic_j_m",
                )
            ),
        })

    c2_resolved = [
        item for item in resolved_checks
        if item["profile"] == "c2"
    ]

    resolved_pass = (
        bool(c2_resolved)
        and all(
            item["max_abs_j_m"] < .005
            for item in c2_resolved
        )
    )

    historical_cell = list(
        parents["m5t"]["data"]["results"].values()
    )

    fresh_cell = [
        result
        for name, result in record["results"].items()
        if next(
            job["backend"]
            for job in record["manifest"]
            if job["name"] == name
        ) == "m5t"
    ]

    def cell_earth(h, profile, order):
        candidates = [
            r
            for r in historical_cell+fresh_cell
            if (
                r["h"] == h
                and r["profile"] == profile
                and r["order"] == order
                and not r["zero_source"]
                and r["step"] == 1.e-4
            )
        ]

        return (
            None
            if not candidates
            else candidates[-1][
                "same_functional_analytic_j_m"
            ]["earth"]
        )

    high_q = {}

    for profile in ("c1", "c2"):
        for h in (.25, .2):
            q12 = cell_earth(h, profile, 12)
            q16 = cell_earth(h, profile, 16)

            high_q[f"{profile}:h={h}"] = {
                "q12_earth_j_m": q12,
                "q16_earth_j_m": q16,
                "q12_minus_q16_j_m": (
                    None
                    if q12 is None or q16 is None
                    else q12-q16
                ),
            }

    cell_c2_ok = all(
        high_q[
            f"c2:h={h}"
        ]["q12_minus_q16_j_m"] is not None
        and abs(
            high_q[
                f"c2:h={h}"
            ]["q12_minus_q16_j_m"]
        ) < .001
        for h in (.25, .2)
    )

    errors = record["errors"]

    complete = (
        len(record["results"])
        == len(record["manifest"])
        and not errors
    )

    intriguing = bool(
        complete
        and finite_screen
        and negative_pass
        and resolved_pass
    )

    gates = {
        "X0_all_predeclared_cases": (
            "PASS" if complete
            else "FAIL_OR_INCOMPLETE"
        ),
        "X1_provenance_and_parent_integrity":
            "PASS",
        "X2_source_free_controls": (
            "PASS" if negative_pass
            else "FAIL_OR_INCOMPLETE"
        ),
        "X3_individual_independent_derivatives": (
            "PASS_SCREEN_ONLY" if resolved_pass
            else "FAIL_OR_INCOMPLETE"
        ),
        "X4_smooth_C2_finer_mesh_domain_phase": (
            "PASS_SCREEN_ONLY" if finite_screen
            else "BLOCKED_OR_INCOMPLETE"
        ),
        "X4B_old_Dirichlet_cell_C2_q12_to_q16": (
            "PASS_SCREEN_ONLY" if cell_c2_ok
            else "BLOCKED_OR_INCOMPLETE"
        ),
        "X5_M5T_integrated_material_with_M5P_exterior_in_one_action":
            "NOT_IMPLEMENTED",
        "X6_C2_continuum_uniqueness":
            "NOT_CERTIFIED",
        "X7_artificial_source_enclosure_support_hull_action":
            "NOT_DERIVED",
        "X8_independent_whole_craft_upward_external_force":
            "NOT_DERIVED",
        "X9_physical_Noether_modes_metric_complete_energy":
            "NOT_ESTABLISHED",
    }

    return {
        "past_runs_count": sum(
            len(entry["data"]["results"])
            for entry in parents.values()
        ),
        "new_case_count": len(
            record["results"]
        ),
        "historical_m5t_gate_T5":
            parents["m5t"]["data"][
                "summary"
            ]["gates"].get(
                "T5_C2_quadrature_screen"
            ),
        "historical_m5s_gate_S5":
            parents["m5s"]["data"][
                "summary"
            ]["gates"].get(
                "S5_C2_extended_fine_phase_screen"
            ),
        "c2_mesh_table": mesh,
        "c2_quadratic_h2_extrapolation_diagnostics":
            extrapolation,
        "c2_phase_tables": phases,
        "c2_boundary_comparisons": boundary,
        "resolved_derivative_audit":
            resolved_checks,
        "old_Dirichlet_cell_higher_quadrature":
            high_q,
        "zero_source_controls": controls,
        "finest_mesh_gate_metrics": {
            "extended_vs_original_earth_j_m":
                fine_domain_difference,
            "extended_h004_vs_h005_earth_j_m":
                fine_mesh_difference,
            "extended_h004_abs_common_j_m":
                fine_max_common,
            "extended_h004_three_phase_screen":
                bool(phase_screen),
            "criteria_are_exploratory_not_certification":
                True,
        },
        "gates": gates,
        "intriguing_numerical_signal_worth_true_port":
            intriguing,
        "decision": (
            "RUN_INCOMPLETE_NO_RESEARCH_VERDICT"
            if not complete
            else (
                "OPTIONAL_ONE_TARGETED_INTEGRATION_IF_NEW_INFORMATION"
                if intriguing
                else "RETURN_PRIMARY_EFFORT_TO_PHYSICAL_ACTION_AND_M6"
            )
        ),
        "unverified_physical_and_assembly_claims": {
            "artificial_model_complete": False,
            "physical_antigravity": False,
            "whole_craft_lift": False,
            "complete_operating_energy_less_than_10_MJ":
                False,
            "006d_replaced": False,
        },
    }


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__
    )

    ap.add_argument(
        "--mode",
        choices=("quick", "full"),
        default="quick",
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
    ap.add_argument(
        "--regression",
        action="store_true",
    )

    args = ap.parse_args(argv)

    if (
        args.max_new_cases is not None
        and args.max_new_cases < 1
    ):
        ap.error(
            "max-new-cases must be positive"
        )

    folder = Path(
        args.results_dir
    ).resolve()

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    parents, modules, source_hashes, parent_info = (
        parents_and_code(folder)
    )

    jobs = make_manifest(args.mode)

    hashes = {
        **source_hashes,
        "m5u": digest(__file__),
    }

    fingerprint = {
        "manifest": jobs,
        "parent_evidence": parent_info,
        "source_sha256": hashes,
    }

    if args.resume:
        destination = Path(
            args.resume
        ).resolve()

        record = json.loads(
            destination.read_text()
        )

        if any(
            record.get(key) != value
            for key, value in fingerprint.items()
        ):
            ap.error(
                "Resume refused: manifest, parent "
                "or source changed"
            )

    else:
        stamp = datetime.now(
            timezone.utc
        ).strftime(
            "%Y%m%dT%H%M%S%fZ"
        )

        destination = folder / (
            f"b17_m5u_decision_{stamp}_"
            f"{args.mode}_bundle.json"
        )

        # Preserve the exact newer code and all 110
        # previous numerical cases in the SAME JSON.
        source_snapshot = {
            name: {
                "sha256": source_hashes[name],
                "code": Path(
                    module.__file__
                ).read_text(),
            }
            for name, module in modules.items()
        }

        record = {
            "branch": BRANCH,
            "mode": args.mode,
            "status": "RUNNING",
            **fingerprint,
            "results": {},
            "errors": {},
            "summary": None,
            "parent_evidence_full": {
                name: entry["data"]
                for name, entry in parents.items()
            },
            "source_snapshot":
                source_snapshot,
            "regression": None,
            "environment": {
                "python":
                    sys.version.split()[0],
                "platform":
                    platform.platform(),
            },
            "claims": {
                "physical_lift": False,
                "complete_artificial_model": False,
            },
        }

    def checkpoint():
        temporary = destination.with_name(
            destination.name + ".tmp"
        )

        with temporary.open("w") as stream:
            json.dump(
                record,
                stream,
                sort_keys=True,
                indent=2,
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
        for index, job in enumerate(jobs, 1):
            name = job["name"]

            if name in record["results"]:
                print(
                    f"[{index}/{len(jobs)}] "
                    f"REUSED {name}",
                    flush=True,
                )
                continue

            if (
                args.max_new_cases is not None
                and number_new >= args.max_new_cases
            ):
                record["status"] = (
                    "PARTIAL_NOT_CERTIFIED"
                )
                checkpoint()

                print(
                    "RESUME_BUNDLE:",
                    destination,
                    flush=True,
                )
                return 2

            print(
                f"[{index}/{len(jobs)}] {name}",
                flush=True,
            )

            try:
                result = run_one(
                    job, modules
                )

                record["results"][name] = result
                record["errors"].pop(
                    name, None
                )

                if job["backend"] == "m5r":
                    interaction = result[
                        "interaction_only"
                    ]

                    print(
                        "  Earth / craft / common [J/m]:",
                        *[
                            f"{interaction[key]:.10g}"
                            for key in (
                                "earth_derivative_j_m",
                                "craft_derivative_j_m",
                                "common_derivative_j_m",
                            )
                        ],
                        flush=True,
                    )

                else:
                    print(
                        "  Cell Earth / max independent defect [J/m]:",
                        f"{result['same_functional_analytic_j_m']['earth']:.10g}",
                        f"{result['maximum_abs_disagreement_j_m']:.4g}",
                        flush=True,
                    )

            except Exception:
                record["errors"][name] = (
                    traceback.format_exc()
                )

                print(
                    "  CASE ERROR",
                    record["errors"][name],
                    flush=True,
                )

            number_new += 1
            checkpoint()

        record["summary"] = analyze(
            record, parents
        )

        if (
            args.regression
            and record["regression"] is None
        ):
            print(
                "FULL REGRESSION",
                flush=True,
            )

            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "-q",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env={
                    **os.environ,
                    "PYTHONPATH": str(
                        Path.cwd() / "src"
                    ),
                },
                check=False,
            )

            record["regression"] = {
                "exit_code": process.returncode,
                "log_tail": process.stdout[-8000:],
            }

            checkpoint()

            print(
                process.stdout[-2000:],
                flush=True,
            )

        numerical_pass = (
            not record["errors"]
            and len(record["results"]) == len(jobs)
            and (
                record["regression"] is None
                or record["regression"][
                    "exit_code"
                ] == 0
            )
        )

        record["status"] = (
            "COMPLETE_NUMERICAL_DECISION_ONLY"
            if numerical_pass
            else "FAILED_OR_INCOMPLETE"
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
                record["summary"]["gates"],
                indent=2,
            ),
            flush=True,
        )

        print(
            "DECISION:",
            record["summary"]["decision"],
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
