"""B17-M5R: matched Earth-present/absent interaction-only derivative audit.

The stationary reduced action is evaluated twice on identical grids:

    Delta Q_*(s, e) = Q_*[Earth profile enabled](s, e)
                    - Q_*[Earth profile disabled](s)

where Q_*= -1/2*c*(u.T @ W @ j) for H u = W j, H = W A.

M5Q derivatives are recomputed with the analytic translated M5M source
including neutrality-projection derivative. All Earth-on and Earth-off
source coordinates, finite boxes, mesh phases, closure rules, source amplitude,
and material profile shape are matched before subtraction.

The interaction derivative is NOT a physical Earth/craft force: neither
source matter, enclosure, metric stress nor gravity is dynamically sourced.
The artificial background is prescribed and its Earth-on/off subtraction
is not a derivation of a gravitational Earth action. No whole-craft lift,
sub-10-MJ complete energy, physical reciprocity or 006D replacement is claimed.
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

from . import hook17_r3b_m5q_translation_balance as m5q
from . import hook17_r3b_m5p_exterior_boundary as m5p
from . import hook17_r3b_m5o_fixed_box as m5o

BRANCH = "032H17A12D1R3X3B17-ALPHA1R13-M5R-INTERACTION"
EXPECTED_PARENT_SHA256 = {
    "m5o": "e75e0b11b05b04a1561d4e1e628e6c6b62c2a7f2c36912b85041bec95b8969d3",
    "m5p": "e49f7eb2ac7f700d0f2608bd556e3729cf0941932704761f9b9118d9607c2243",
    "m5q": "93ed171e95cd4344efd3ca6f36661b977d18383a70c9a319e73c1d79ea12abf0",
}


def provenance():
    files = {
        "m5o": m5o.__file__,
        "m5p": m5p.__file__,
        "m5q": m5q.__file__,
        "m5r": __file__,
    }
    return {
        k: hashlib.sha256(Path(p).read_bytes()).hexdigest()
        for k, p in files.items()
    }


def tasks(mode):
    if mode not in ("quick", "full"):
        raise ValueError("Invalid mode")
    out = []
    names = set()

    def add(name, **kw):
        if name in names:
            raise AssertionError(name)
        names.add(name)
        out.append((name, kw))

    add("c2_compact_h0p2", h=.2, domain="compact", resolve=True)
    add("c2_compact_h0p125", h=.125, domain="compact", resolve=True)
    add("c2_original_h0p1", h=.1, domain="original", resolve=True)
    add(
        "c1_compact_h0p125",
        h=.125, domain="compact", profile="c1",
        width=.25, resolve=True,
    )
    add(
        "c2_compact_phase_negative",
        h=.2, domain="compact", phase=-.25,
    )
    add(
        "c2_compact_phase_positive",
        h=.2, domain="compact", phase=.25,
    )
    add(
        "zero_source_control",
        h=.25, domain="compact",
        zero_source=True, resolve=True,
    )

    if mode == "full":
        for label, hs in (
            ("compact", (.25, .1, .0625, .05)),
            ("original", (.2, .0625, .05)),
            ("extended", (.1, .0625, .05)),
            ("outer21", (.2, .1)),
        ):
            for h in hs:
                add(
                    f"c2_{label}_h{h}",
                    h=h, domain=label,
                )

        for h in (.1, .0625):
            for phase in (-.5, -.25, .25, .5):
                add(
                    f"c2_compact_phase_h{h}_p{phase}",
                    h=h,
                    domain="compact",
                    phase=phase,
                )

        for h in (.1, .0625):
            for phase in (-.25, .25):
                add(
                    f"c2_original_phase_h{h}_p{phase}",
                    h=h,
                    domain="original",
                    phase=phase,
                )

        for h in (.25, .2, .1, .0625, .05):
            add(
                f"c1_compact_h{h}",
                h=h,
                domain="compact",
                profile="c1",
                width=.25,
            )

        for h in (.1, .0625, .05):
            add(
                f"c1_original_h{h}",
                h=h,
                domain="original",
                profile="c1",
                width=.25,
            )

        for h in (.1, .0625):
            for phase in (-.25, .25):
                add(
                    f"c1_compact_phase_h{h}_p{phase}",
                    h=h,
                    domain="compact",
                    profile="c1",
                    width=.25,
                    phase=phase,
                )

        for h in (.125, .1, .0625, .05):
            add(
                f"c2_samewidth_compact_h{h}",
                h=h,
                domain="compact",
                profile="c2",
                width=.25,
            )

        for h in (.1, .0625):
            for phase in (-.25, .25):
                add(
                    f"c2_samewidth_phase_h{h}_p{phase}",
                    h=h,
                    domain="compact",
                    profile="c2",
                    width=.25,
                    phase=phase,
                )

        add(
            "source_quad_order_control",
            h=.1, domain="compact", order=4,
        )
        add(
            "source_step_control",
            h=.125, domain="compact",
            step=1.e-5, resolve=True,
        )
        add(
            "source_boundary_dirichlet",
            h=.1, domain="compact",
            closure="dirichlet",
        )
        add(
            "source_boundary_robin",
            h=.1, domain="compact",
            closure="dipole_robin",
        )

    return out


def run_case(
    h,
    domain="compact",
    profile="c2",
    width=.5,
    phase=0.,
    order=6,
    step=1.e-4,
    closure="dipole_trace",
    zero_source=False,
    resolve=False,
):
    """Evaluate both states and subtract only matched quantities."""
    if domain not in m5p.BOUNDS:
        raise ValueError("Unrecognized domain")

    if h <= 0 or not math.isfinite(h) or not -.5 <= phase <= .5:
        raise ValueError("Bad spacing or phase")

    kw = dict(
        h=h,
        domain=m5p.BOUNDS[domain],
        profile=profile,
        width=width,
        phase=phase,
        order=order,
        step=step,
        closure=closure,
        zero_source=zero_source,
        resolve=resolve,
        direct_craft=resolve,
    )

    earth_on = m5q.evaluate(**kw, earth_present=True)
    earth_off = m5q.evaluate(**kw, earth_present=False)

    on = earth_on["derivative_terms_j_m"]
    off = earth_off["derivative_terms_j_m"]

    def difference(key):
        return float(on[key] - off[key])

    e = difference("earth_operator_analytic")
    c = difference("craft_earth_fixed_inferred")
    t = difference("common_total")

    analytic_earth_error = (
        difference("earth_operator_finite_difference") - e
    )

    self_background = float(off["common_total"])
    noearth_earth = float(off["earth_operator_analytic"])

    direct = None
    if resolve:
        if (
            on["craft_earth_fixed_direct"] is None
            or off["craft_earth_fixed_direct"] is None
        ):
            raise ArithmeticError(
                "Requested independent craft derivative absent"
            )

        direct = {
            "craft_direct_j_m": difference(
                "craft_earth_fixed_direct"
            ),
            "craft_inferred_j_m": c,
            "craft_direct_minus_inferred_j_m": (
                difference("craft_earth_fixed_direct") - c
            ),
        }

    res = None
    if resolve:
        a = earth_on["on_shell_derivative_re_solved"]
        b = earth_off["on_shell_derivative_re_solved"]

        if a is None or b is None:
            raise ArithmeticError(
                "Requested re-solved variation absent"
            )

        res = {
            "earth_j_m": a["earth_j_m"] - b["earth_j_m"],
            "craft_j_m": a["craft_j_m"] - b["craft_j_m"],
            "common_j_m": a["common_j_m"] - b["common_j_m"],
        }
        res["earth_minus_analytic_j_m"] = (
            res["earth_j_m"] - e
        )
        res["craft_minus_inferred_j_m"] = (
            res["craft_j_m"] - c
        )
        res["common_minus_analytic_j_m"] = (
            res["common_j_m"] - t
        )

    return {
        "branch": BRANCH,
        "scope": "PRESCRIBED_ON_OFF_REDUCED_ACTION_ONLY",
        "mesh_h_m": h,
        "domain": domain,
        "bounds_m": list(m5p.BOUNDS[domain]),
        "profile": profile,
        "width_m": width,
        "phase_cells": phase,
        "closure": closure,
        "quadrature_order": order,
        "derivative_step_m": step,
        "zero_source": zero_source,
        "on_shell_action_enabled_j": earth_on[
            "on_shell_action_j"
        ],
        "on_shell_action_disabled_j": earth_off[
            "on_shell_action_j"
        ],
        "interaction_action_difference_j": (
            earth_on["on_shell_action_j"]
            - earth_off["on_shell_action_j"]
        ),
        "earth_on": {
            "earth_j_m": on["earth_operator_analytic"],
            "craft_j_m": on["craft_earth_fixed_inferred"],
            "common_j_m": on["common_total"],
        },
        "earth_off": {
            "earth_j_m": off["earth_operator_analytic"],
            "craft_j_m": off["craft_earth_fixed_inferred"],
            "common_j_m": self_background,
        },
        "interaction_only": {
            "earth_derivative_j_m": e,
            "craft_derivative_j_m": c,
            "common_derivative_j_m": t,
            "translation_partition_error_j_m": t - e - c,
            "common_relative_to_earth": (
                abs(t) / max(abs(e), 1.)
            ),
            "matched_self_translation_j_m": self_background,
            "noearth_earth_derivative_j_m": noearth_earth,
            "material_derivative_fd_minus_analytic_j_m": (
                analytic_earth_error
            ),
            "source_explicit_difference_j_m": difference(
                "source_explicit_total"
            ),
            "enclosure_operator_difference_j_m": difference(
                "enclosure_operator_inferred"
            ),
            "vector_source_difference_j_m": difference(
                "source_explicit_vector"
            ),
            "scalar_source_difference_j_m": difference(
                "source_explicit_scalar"
            ),
        },
        "independent_craft_check": direct,
        "resolved_interaction_derivative": res,
        "maximum_stationarity_residual": max(
            earth_on["stationarity_residual"],
            earth_off["stationarity_residual"],
        ),
        "maximum_operator_residual": max(
            earth_on["operator_residual"],
            earth_off["operator_residual"],
        ),
        "maximum_operator_asymmetry": max(
            earth_on["weighted_operator_asymmetry"],
            earth_off["weighted_operator_asymmetry"],
        ),
        "maximum_analytic_source_fd_relative_defect": max(
            earth_on["source_derivative_fd_relative_defect"],
            earth_off["source_derivative_fd_relative_defect"],
        ),
        "modeled_energy_not_complete_device_energy": True,
        "physical_reciprocity_certified": False,
        "whole_spacecraft_lift_certified": False,
        "006d_replaced": False,
    }


def analyze(jobs, results):
    """Issue scoped gates; do not promote artificial numerics to physics."""
    eps = 1.e-12
    complete = len(results) == len(jobs)
    all_rows = list(results.values())

    def close_checks(r):
        x = r["interaction_only"]

        if any(
            not math.isfinite(float(v))
            for v in x.values()
        ):
            return False

        if abs(x["noearth_earth_derivative_j_m"]) > eps:
            return False

        if abs(x["translation_partition_error_j_m"]) > .004:
            return False

        if any(
            r[name] > 1.e-7
            for name in (
                "maximum_operator_residual",
                "maximum_stationarity_residual",
                "maximum_operator_asymmetry",
            )
        ):
            return False

        if (
            r["maximum_analytic_source_fd_relative_defect"]
            > .005
        ):
            return False

        if r["zero_source"]:
            if abs(r["interaction_action_difference_j"]) > eps:
                return False

            if max(
                abs(x[k])
                for k in (
                    "earth_derivative_j_m",
                    "craft_derivative_j_m",
                    "common_derivative_j_m",
                )
            ) > eps:
                return False

        return True

    parent_reference = {
        "c2_compact_h0p2": (
            -12.7882913449623,
            .41078212848375095,
        ),
        "c2_original_h0p1": (
            -11.792488561807552,
            -.007886958674649946,
        ),
    }

    matches = {}

    for name, (
        expected_earth,
        expected_common,
    ) in parent_reference.items():
        if name in results:
            on = results[name]["earth_on"]

            matches[name] = {
                "earth_difference_j_m": (
                    on["earth_j_m"] - expected_earth
                ),
                "common_difference_j_m": (
                    on["common_j_m"] - expected_common
                ),
            }

    parent_ok = (
        len(matches) == 2
        and all(
            abs(value) < 1.e-7
            for item in matches.values()
            for value in item.values()
        )
    )

    resolved = [
        r for r in all_rows
        if r["resolved_interaction_derivative"] is not None
    ]

    resolved_ok = (
        bool(resolved)
        and all(
            max(
                abs(value)
                for key, value in r[
                    "resolved_interaction_derivative"
                ].items()
                if (
                    key.endswith("minus_analytic_j_m")
                    or key.endswith("minus_inferred_j_m")
                )
            ) < .01
            for r in resolved
        )
    )

    identity_ok = (
        bool(all_rows)
        and all(close_checks(r) for r in all_rows)
    )

    def gather(profile, width, label, hs, phases=(0.,)):
        return [
            r for r in all_rows
            if (
                r["profile"] == profile
                and r["width_m"] == width
                and r["domain"] == label
                and r["mesh_h_m"] in hs
                and r["phase_cells"] in phases
                and r["closure"] == "dipole_trace"
                and not r["zero_source"]
                and r["quadrature_order"] == 6
                and r["derivative_step_m"] == 1.e-4
            )
        ]

    fine_c2 = gather(
        "c2", .5, "original", (.05,)
    )
    fine_c2 += gather(
        "c2", .5, "extended", (.05,)
    )

    fine_c1 = gather(
        "c1", .25, "compact", (.1, .0625, .05)
    )
    fine_c1 += gather(
        "c1", .25, "original", (.1, .0625, .05)
    )

    # Predeclared screening tolerances, not physical certificates.
    c2_box_probe = (
        len(fine_c2) == 2
        and max(
            abs(
                r["interaction_only"][
                    "common_derivative_j_m"
                ]
            )
            for r in fine_c2
        ) < .01
        and abs(
            fine_c2[0]["interaction_only"][
                "earth_derivative_j_m"
            ]
            - fine_c2[1]["interaction_only"][
                "earth_derivative_j_m"
            ]
        ) < .01
    )

    c1_probe = (
        len(fine_c1) == 6
        and max(
            abs(
                r["interaction_only"][
                    "common_derivative_j_m"
                ]
            )
            for r in fine_c1
        ) < .01
        and max(
            abs(
                r["interaction_only"][
                    "material_derivative_fd_minus_analytic_j_m"
                ]
            )
            for r in fine_c1
        ) < 1.e-4
    )

    phase = {}

    for profile, width in (
        ("c2", .5),
        ("c1", .25),
        ("c2", .25),
    ):
        for h in (.2, .1, .0625):
            entries = gather(
                profile, width, "compact", (h,),
                (-.5, -.25, 0., .25, .5),
            )

            if len(entries) < 3:
                continue

            vals = [
                r["interaction_only"][
                    "common_derivative_j_m"
                ]
                for r in entries
            ]

            phase[
                f"{profile}_width{width}_h{h}"
            ] = {
                "count": len(vals),
                "spread_j_m": max(vals) - min(vals),
                "max_abs_j_m": max(
                    abs(v) for v in vals
                ),
                "certified": False,
            }

    return {
        "branch": BRANCH,
        "registered": len(jobs),
        "completed": len(results),
        "parent_reproduction": matches,
        "fine_c2_interaction": {
            f"{r['domain']}:{r['mesh_h_m']}":
                r["interaction_only"]
            for r in fine_c2
        },
        "fine_c1_interaction": {
            f"{r['domain']}:{r['mesh_h_m']}":
                r["interaction_only"]
            for r in fine_c1
        },
        "interaction_phase_spreads": phase,
        "gates": {
            "R0_M5Q_reference_preserved": (
                "PASS"
                if parent_ok
                else "FAIL_OR_INCOMPLETE"
            ),
            "R1_matched_background_and_stationary_checks": (
                "PASS"
                if complete and identity_ok
                else "FAIL_OR_INCOMPLETE"
            ),
            "R2_independently_resolved_interaction_derivatives": (
                "PASS"
                if complete and resolved_ok
                else "FAIL_OR_INCOMPLETE"
            ),
            "R3_c2_fine_domain_screen": (
                "PASS_SCREEN_ONLY"
                if c2_box_probe
                else "YELLOW_OR_INCOMPLETE"
            ),
            "R4_c1_interface_screen": (
                "PASS_SCREEN_ONLY"
                if c1_probe
                else "BLOCKED_OR_INCOMPLETE"
            ),
            "R5_phase_mesh_continuum_uniqueness":
                "NOT_CERTIFIED",
            "R6_independent_enclosure_support_action":
                "NOT_DERIVED",
            "R7_physical_Noether_momentum_and_metric":
                "NOT_DERIVED",
            "R8_complete_operating_energy_and_lift":
                "NOT_ESTABLISHED",
        },
        "stationary_artificial_model_complete": False,
        "physical_antigravity_certified": False,
        "whole_craft_lift_certified": False,
        "complete_energy_certified": False,
        "006d_replaced": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--mode",
        choices=("quick", "full"),
        default="quick",
    )
    parser.add_argument(
        "--results-dir",
        default="results/data",
    )
    parser.add_argument("--resume")
    parser.add_argument(
        "--max-new-cases",
        type=int,
    )

    args = parser.parse_args(argv)
    entries = tasks(args.mode)

    manifest = [
        {"name": name, "parameters": kw}
        for name, kw in entries
    ]

    hashes = provenance()

    mismatched = {
        key: (
            EXPECTED_PARENT_SHA256[key],
            hashes[key],
        )
        for key in EXPECTED_PARENT_SHA256
        if hashes[key] != EXPECTED_PARENT_SHA256[key]
    }

    if mismatched:
        parser.error(
            "M5O/M5P/M5Q code changed since the supplied "
            "M5Q bundle: " + json.dumps(mismatched)
        )

    if args.resume:
        destination = Path(args.resume).resolve()
        record = json.loads(destination.read_text())

        if (
            record.get("branch") != BRANCH
            or record.get("mode") != args.mode
            or record.get("manifest") != manifest
            or record.get("source_sha256") != hashes
        ):
            parser.error(
                "Resume refused: manifest or code hashes have changed"
            )
    else:
        folder = Path(args.results_dir)
        folder.mkdir(parents=True, exist_ok=True)

        stamp = datetime.now(
            timezone.utc
        ).strftime("%Y%m%dT%H%M%S%fZ")

        destination = folder / (
            f"b17_m5r_interaction_{stamp}_"
            f"{args.mode}_bundle.json"
        )

        record = {
            "branch": BRANCH,
            "schema": "antigravity.single_run.v1",
            "mode": args.mode,
            "manifest": manifest,
            "source_sha256": hashes,
            "status": "RUNNING",
            "registered": len(entries),
            "processed": 0,
            "results": {},
            "errors": {},
            "summary": None,
            "claims": {
                "physical_antigravity": False,
                "whole_spacecraft_lift": False,
                "complete_device_energy": False,
            },
        }

    def save():
        tmp = destination.with_name(
            destination.name + ".tmp"
        )

        with tmp.open("w") as stream:
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

        os.replace(tmp, destination)

    if not args.resume:
        save()

    number_new = 0

    try:
        for number, (name, kwargs) in enumerate(
            entries, 1
        ):
            if name in record["results"]:
                print(
                    f"[{number}/{len(entries)}] REUSED {name}",
                    flush=True,
                )
                continue

            if (
                args.max_new_cases is not None
                and number_new >= args.max_new_cases
            ):
                record["status"] = "PARTIAL_NOT_CERTIFIED"
                save()
                print(
                    "RESUME_BUNDLE:",
                    destination,
                    flush=True,
                )
                return 2

            print(
                f"[{number}/{len(entries)}] {name}",
                flush=True,
            )

            try:
                row = run_case(**kwargs)
                record["results"][name] = row
                record["errors"].pop(name, None)

                values = row["interaction_only"]

                print(
                    "  Delta Earth / craft / common [J/m]:",
                    *[
                        f"{values[key]:.9g}"
                        for key in (
                            "earth_derivative_j_m",
                            "craft_derivative_j_m",
                            "common_derivative_j_m",
                        )
                    ],
                    "background:",
                    f"{values['matched_self_translation_j_m']:.9g}",
                    flush=True,
                )
            except Exception:
                record["errors"][name] = (
                    traceback.format_exc()
                )
                print(
                    "  ERROR:",
                    record["errors"][name],
                    flush=True,
                )

            record["processed"] = (
                len(record["results"])
                + len(record["errors"])
            )

            number_new += 1
            save()

        record["summary"] = analyze(
            entries, record["results"]
        )

        required = (
            "R0_M5Q_reference_preserved",
            "R1_matched_background_and_stationary_checks",
            "R2_independently_resolved_interaction_derivatives",
        )

        numerical_pass = (
            not record["errors"]
            and all(
                record["summary"]["gates"][key] == "PASS"
                for key in required
            )
        )

        record["status"] = (
            "COMPLETE_NUMERICAL_DIAGNOSTIC_ONLY"
            if numerical_pass
            else "FAILED_NUMERICAL_CONTROLS"
        )
        save()

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

        return 0 if numerical_pass else 1

    except KeyboardInterrupt:
        record["status"] = "INTERRUPTED"
        save()

        print(
            "RESUME_BUNDLE:",
            destination,
            flush=True,
        )
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
