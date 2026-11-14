"""B17-M5T: variational cell-averaged material reconstruction.

PURPOSE
-------
Replace point-sampled material loading in an independent M5M
coupled-carrier pilot with cylindrical dual-cell integration.

The same quadrature defines beta and its Earth/enclosure position
derivatives. The original R3X1 Lorentzian carrier signs, source
normalization, and weighted stationary action are preserved.

SCOPE
-----
This pilot uses the older M5M native fixed-Dirichlet boundary,
not the M5P dipole-trace exterior closure. It is NOT yet a
complete M5P replacement or a continuum certificate.

The source is prescribed artificial M5I matter, not a derived
microscopic source. No physical Noether identity, Earth reaction,
whole-spacecraft lift, or complete operating energy is established.
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

import numpy as np
from numpy.polynomial.legendre import leggauss

from . import hook17_r3b_m4b_sparse_earth_loading as loading
from .hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
)
from .hook17_r3b_m4b_sparse_earth_loading import MaterialGeometry
from .hook17_f2_strong_payload_loading_rescue import (
    loading_coefficient_z,
)
from .hook17_r3b_m5i_continuum_source import SourceSpec
from .hook17_r3b_m5m_translation_consistency import (
    PORTAL_SCALE_EV,
    carrier_action_conversion_j_per_native,
    redeposit_shifted_source,
)
from .hook17_r3b_m5l_variational_audit import (
    assemble_variational_matrix,
    on_shell_quadratic,
)

BRANCH = (
    "032H17A12D1R3X3B17-"
    "ALPHA1R15-M5T-VARIATIONAL-CELL"
)

AMPLIFIER = (PORTAL_SCALE_EV / 1000.0)**2

EXPECTED_PARENT_SHA256 = {
    "hook17_r3b_m5i_continuum_source":
        "ee3ff31e2068e2f6fc5c8bf46ee951e5b11098d24ba36d73e8f0e1f568f44a54",
    "hook17_r3b_m5m_translation_consistency":
        "f95a33f65c815b129007beea44a75f19feb0efe859817843b69922d9ac84a7ec",
    "hook17_r3b_m5l_variational_audit":
        "aa5571303309c80762d7f8d9fc058d56c458e2b3793e773d37c3bf77573c256b",
    "hook17_r3b_m4b_sparse_earth_loading":
        "446963973cad865bb2a8460ee0e44f0e260c9953c1c0ae2a26b2031fa33a643c",
    "hook17_r3b_m4b1_source_recovery":
        "59be7700953a715562d7676d48959953837145310191398eb5ce167a8a010599",
    "hook17_fdual_f_loaded_payload_homotopy":
        "a0368a7163e1f392745fd47c7c2e79fd54adce5e666362e51dc5c980c87a0fee",
    "hook17_f2_strong_payload_loading_rescue":
        "e1296794c25a4d0e4d5634c7e7d543a0b488b8d2a1963afcf7878bea1c1b99e7",
}


def provenance():
    root = Path(__file__).resolve().parent
    return {
        name: hashlib.sha256(
            (root / (name + ".py")).read_bytes()
        ).hexdigest()
        for name in EXPECTED_PARENT_SHA256
    }


def validate_legacy_provenance():
    actual = provenance()
    mismatches = {
        name: {
            "expected": expected,
            "actual": actual[name],
        }
        for name, expected in EXPECTED_PARENT_SHA256.items()
        if actual[name] != expected
    }

    if mismatches:
        raise RuntimeError(
            "Legacy carrier/source drift: "
            + json.dumps(mismatches)
        )

    return actual


def f_and_dedge(x, edge, width, profile):
    """C1/C2 smoothstep and exact derivative w.r.t. its edge."""
    if profile not in ("c1", "c2") or width <= 0:
        raise ValueError("Invalid smoothstep")

    t = (
        np.asarray(x, dtype=float) - edge + width
    ) / (2.0 * width)

    u = np.clip(t, 0.0, 1.0)

    if profile == "c1":
        fraction = 1.0 - 3.0*u**2 + 2.0*u**3
        derivative = 3.0*u*(1.0-u)/width
    else:
        fraction = (
            1.0 - 10.0*u**3 + 15.0*u**4 - 6.0*u**5
        )
        derivative = (
            15.0*u**2*(1.0-u)**2/width
        )

    derivative *= (t > 0.0) & (t < 1.0)

    return fraction, derivative


def geometry_at(
    r, z, earth, craft, profile, width,
    geometry, earth_present,
):
    """Density and its exact coordinate variations at sample points."""
    distance = np.hypot(r, z-craft)

    enclosure, enclosure_edge = f_and_dedge(
        distance,
        geometry.enclosure_radius_m,
        width,
        profile,
    )

    outside = 1.0 - enclosure

    d_outside_craft = (
        enclosure_edge
        * (craft-z)
        / np.maximum(distance, 1.e-100)
    )

    if earth_present:
        disk = f_and_dedge(
            r,
            geometry.ground_radius_m,
            width,
            profile,
        )[0]

        top = (
            earth
            + geometry.ground_top_relative_z_m
        )

        bottom = top - geometry.ground_depth_m

        below_top, top_edge = f_and_dedge(
            z, top, width, profile
        )

        below_bottom, bottom_edge = f_and_dedge(
            z, bottom, width, profile
        )

        ground = (
            disk * below_top * (1.0-below_bottom)
        )

        d_ground_earth = disk * (
            top_edge*(1.0-below_bottom)
            - below_top*bottom_edge
        )
    else:
        ground = np.zeros_like(distance)
        d_ground_earth = np.zeros_like(distance)

    air_density = geometry.air_density_kg_m3
    ground_density = geometry.ground_density_kg_m3

    density = (
        air_density*outside*(1.0-ground)
        + ground_density*ground
    )

    d_density_earth = (
        ground_density-air_density*outside
    )*d_ground_earth

    d_density_craft = (
        air_density*(1.0-ground)*d_outside_craft
    )

    return (
        density,
        d_density_earth,
        d_density_craft,
    )


def dual_cell_beta(
    base,
    earth=0.0,
    craft=0.0,
    profile="c2",
    width=0.5,
    order=8,
    earth_present=True,
):
    """Cylindrical dual-cell averaged material loading and derivatives.

    Integrates with the r dr dz measure, including the axis half-cell.
    The integral is evaluated by Gaussian quadrature, not claimed
    analytically exact for piecewise profiles at every cell crossing.

    The same quadrature produces beta and beta's position derivatives.
    """

    if order not in (4, 8, 12, 16):
        raise ValueError("Unregistered quadrature order")

    if (
        width <= 0
        or not all(
            math.isfinite(x)
            for x in (earth, craft, width)
        )
    ):
        raise ValueError("Invalid coordinates")

    field = base["field"]
    h = float(field["h"])

    radial = np.asarray(field["rhos"], dtype=float)
    axial = np.asarray(field["zs"], dtype=float)

    rlow = np.maximum(0.0, radial-h/2.0)
    rhigh = radial+h/2.0

    rmid = (rlow+rhigh)/2.0
    rhalf = (rhigh-rlow)/2.0

    radial_norm = 0.5*(rhigh**2-rlow**2)

    if np.any(radial_norm <= 0):
        raise ArithmeticError("Invalid radial cell")

    cell_norm = radial_norm[None, :]*h

    shape = (len(axial), len(radial))

    density_sum = np.zeros(shape)
    earth_sum = np.zeros(shape)
    craft_sum = np.zeros(shape)

    nodes, weights = leggauss(order)
    geometry = MaterialGeometry()

    for xi, wi in zip(nodes, weights):
        r = (rmid+rhalf*xi)[None, :]
        radial_weight = rhalf[None, :]*wi*r

        for xj, wj in zip(nodes, weights):
            z = (axial+h*xj/2.0)[:, None]

            weight = radial_weight*(h*wj/2.0)

            density, de, dc = geometry_at(
                r,
                z,
                earth,
                craft,
                profile,
                width,
                geometry,
                earth_present,
            )

            density_sum += weight*density
            earth_sum += weight*de
            craft_sum += weight*dc

    density_avg = density_sum/cell_norm
    density_earth = earth_sum/cell_norm
    density_craft = craft_sum/cell_norm

    # The native material law is linear in density.
    kappa = float(
        loading_coefficient_z(
            np.array([1.0]),
            PORTAL_SCALE_EV,
        )[0] - 1.0
    )

    beta = -kappa*density_avg
    beta_earth = -kappa*density_earth
    beta_craft = -kappa*density_craft

    for values in (
        beta,
        beta_earth,
        beta_craft,
    ):
        if not np.isfinite(values).all():
            raise ArithmeticError(
                "Nonfinite integrated material"
            )

    return beta, beta_earth, beta_craft


def fields_and_source(base, shift, zero_source=False):
    """M5I physical-coordinate redeposition, not nodal interpolation."""
    shifted, audit = redeposit_shifted_source(
        base,
        SourceSpec(),
        float(shift),
        order=6,
    )

    if zero_source:
        return {
            **shifted,
            "j_phi": 0.0*shifted["j_phi"],
            "j_a": 0.0*shifted["j_a"],
        }, audit

    return {
        **shifted,
        "j_phi": AMPLIFIER*shifted["j_phi"],
        "j_a": AMPLIFIER*shifted["j_a"],
    }, audit


def state(
    base, earth, craft, profile, width,
    order, present, zero_source=False,
):
    """Solve and differentiate the same weighted stationary carrier."""
    active, source_audit = fields_and_source(
        base, craft, zero_source
    )

    beta, beta_earth, beta_craft = dual_cell_beta(
        base,
        earth,
        craft,
        profile,
        width,
        order,
        present,
    )

    solution = loading._solve_fixed_sources(
        active,
        beta,
        fraction=1.0,
    )

    field = active["field"]
    operators = active["operators"]

    u = np.r_[
        solution["phi"][1:-1, :-1].ravel(),
        solution["a"][1:-1, 1:-1].ravel(),
    ]

    j = np.r_[
        active["j_phi"],
        active["j_a"],
    ]

    _, H, weights, asymmetry = (
        assemble_variational_matrix(
            operators,
            solution["coupling"],
            field["rhos"],
            float(field["h"]),
        )
    )

    quadratic = on_shell_quadratic(
        u, j, H, weights
    )

    conversion = carrier_action_conversion_j_per_native(
        float(field["h"])
    )

    action = float(
        quadratic["native_quadratic_functional"]
    )*conversion

    nphi = len(active["j_phi"])
    phi = u[:nphi]
    azimuthal = u[nphi:]

    wphi = weights[:nphi]

    def material_action_derivative(d_beta):
        """Evaluate half-u-Hprime-u from the unchanged signed coupling."""
        varied_coupling = (
            loading._build_same_action_coupling(
                field["rhos"],
                field["zs"],
                float(field["h"]),
                d_beta,
                operators,
            )
        )

        return conversion*float(
            np.dot(
                phi,
                wphi*(varied_coupling["c"] @ azimuthal),
            )
        )

    return {
        "action": action,
        "u": u,
        "j": j,
        "weights": weights,
        "earth_operator": material_action_derivative(
            beta_earth
        ),
        "craft_operator": material_action_derivative(
            beta_craft
        ),
        "stationarity": quadratic[
            "relative_action_variation_residual"
        ],
        "on_shell_identity": quadratic[
            "relative_on_shell_identity_defect"
        ],
        "weighted_asymmetry": asymmetry,
        "solver_residual": solution["residual"],
        "source_audit": source_audit,
    }


def evaluate(
    h=0.25,
    profile="c2",
    width=0.5,
    order=8,
    step=1.e-4,
    zero_source=False,
):
    """Compare analytic same-action derivatives with re-solved differences."""
    if h not in (0.25, 0.2):
        raise ValueError("Unregistered historical M5M grid")

    if not 0.0 < step <= 0.002:
        raise ValueError("Invalid translation step")

    base = assemble_original_aligned_source(h)
    cache = {}

    def get_state(earth, craft, present):
        key = (earth, craft, present)

        if key not in cache:
            cache[key] = state(
                base,
                earth,
                craft,
                profile,
                width,
                order,
                present,
                zero_source,
            )

        return cache[key]

    earth_on = get_state(0.0, 0.0, True)
    earth_off = get_state(0.0, 0.0, False)

    def interaction(earth, craft):
        return (
            get_state(earth, craft, True)["action"]
            - get_state(earth, craft, False)["action"]
        )

    finite = {
        "earth": (
            interaction(step, 0.0)
            - interaction(-step, 0.0)
        )/(2.0*step),
        "craft": (
            interaction(0.0, step)
            - interaction(0.0, -step)
        )/(2.0*step),
        "common": (
            interaction(step, step)
            - interaction(-step, -step)
        )/(2.0*step),
    }

    plus, _ = fields_and_source(
        base, step, zero_source
    )

    minus, _ = fields_and_source(
        base, -step, zero_source
    )

    dj = (
        np.r_[
            plus["j_phi"], plus["j_a"]
        ]
        - np.r_[
            minus["j_phi"], minus["j_a"]
        ]
    )/(2.0*step)

    conversion = carrier_action_conversion_j_per_native(h)

    def analytic_part(x):
        return {
            "earth": x["earth_operator"],
            "craft_operator": x["craft_operator"],
            "craft_source": -conversion*float(
                np.dot(
                    x["u"],
                    x["weights"]*dj,
                )
            ),
        }

    on = analytic_part(earth_on)
    off = analytic_part(earth_off)

    analytic = {
        "earth": on["earth"]-off["earth"],
        "craft_operator": (
            on["craft_operator"]-off["craft_operator"]
        ),
        "craft_source": (
            on["craft_source"]-off["craft_source"]
        ),
    }

    analytic["craft"] = (
        analytic["craft_operator"]
        + analytic["craft_source"]
    )

    analytic["common"] = (
        analytic["earth"]+analytic["craft"]
    )

    defects = {
        key: finite[key]-analytic[key]
        for key in ("earth", "craft", "common")
    }

    numerical_residuals = {
        "stationarity": max(
            x["stationarity"] for x in cache.values()
        ),
        "on_shell_identity": max(
            x["on_shell_identity"] for x in cache.values()
        ),
        "weighted_asymmetry": max(
            x["weighted_asymmetry"] for x in cache.values()
        ),
        "solver": max(
            x["solver_residual"] for x in cache.values()
        ),
    }

    return {
        "branch": BRANCH,
        "scope": "M5M_NATIVE_DIRICHLET_BVP_NEW_CYLINDRICAL_CELL_MATERIAL",
        "h": h,
        "profile": profile,
        "width": width,
        "order": order,
        "step": step,
        "zero_source": zero_source,
        "center_action_on_j": earth_on["action"],
        "center_action_off_j": earth_off["action"],
        "interaction_action_j": (
            earth_on["action"]-earth_off["action"]
        ),
        "finite_difference_j_m": finite,
        "same_functional_analytic_j_m": analytic,
        "finite_minus_analytic_j_m": defects,
        "maximum_abs_disagreement_j_m": max(
            abs(x) for x in defects.values()
        ),
        "numerical_residuals": numerical_residuals,
        "all_sources_onboard_physically_realized": False,
        "M5P_exterior_boundary_reproduced": False,
        "whole_spacecraft_force_derived": False,
        "physical_noether_identity_derived": False,
        "complete_operating_energy_derived": False,
        "006d_replaced": False,
    }


def manifest(mode):
    quick = [
        dict(
            h=.25, profile="c1",
            width=.25, order=8, step=1.e-4,
        ),
        dict(
            h=.25, profile="c2",
            width=.5, order=8, step=1.e-4,
        ),
        dict(
            h=.25, profile="c2",
            width=.5, order=8, step=1.e-4,
            zero_source=True,
        ),
    ]

    if mode == "quick":
        return quick

    if mode != "full":
        raise ValueError(mode)

    full = quick.copy()

    for h in (.25, .2):
        for profile, width in (
            ("c1", .25),
            ("c2", .5),
        ):
            for order in (4, 12):
                full.append(dict(
                    h=h, profile=profile,
                    width=width, order=order,
                    step=1.e-4,
                ))

            for step in (1.e-3, 1.e-5):
                full.append(dict(
                    h=h, profile=profile,
                    width=width, order=8,
                    step=step,
                ))

    full.extend([
        dict(
            h=.2, profile="c1",
            width=.25, order=8, step=1.e-4,
        ),
        dict(
            h=.2, profile="c2",
            width=.5, order=8, step=1.e-4,
        ),
    ])

    return full


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
    parser.add_argument("--max-new-cases", type=int)

    args = parser.parse_args(argv)
    jobs = manifest(args.mode)

    filehash = hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()

    try:
        parent_hashes = validate_legacy_provenance()
    except RuntimeError as exc:
        parser.error(str(exc))

    if args.resume:
        destination = Path(args.resume).resolve()
        record = json.loads(destination.read_text())

        if (
            record.get("manifest") != jobs
            or record.get("module_sha256") != filehash
            or record.get("parent_source_sha256")
                != parent_hashes
        ):
            parser.error(
                "Resume refused: source or manifest changed"
            )
    else:
        folder = Path(args.results_dir)
        folder.mkdir(parents=True, exist_ok=True)

        stamp = datetime.now(
            timezone.utc
        ).strftime("%Y%m%dT%H%M%S%fZ")

        destination = folder / (
            f"b17_m5t_material_{stamp}_"
            f"{args.mode}_bundle.json"
        )

        record = {
            "branch": BRANCH,
            "mode": args.mode,
            "status": "RUNNING",
            "manifest": jobs,
            "module_sha256": filehash,
            "parent_source_sha256": parent_hashes,
            "results": {},
            "errors": {},
            "summary": None,
        }

    def checkpoint():
        temporary = destination.with_name(
            destination.name + ".tmp"
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

        os.replace(temporary, destination)

    if not args.resume:
        checkpoint()

    completed_new = 0

    try:
        for index, kw in enumerate(jobs, 1):
            name = (
                f"{index:02d}_{kw['profile']}_"
                f"{kw['h']}_{kw['order']}_"
                f"{kw['step']}_"
                f"{kw.get('zero_source', False)}"
            )

            if name in record["results"]:
                continue

            if (
                args.max_new_cases is not None
                and completed_new >= args.max_new_cases
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
                f"[{index}/{len(jobs)}] {name}",
                flush=True,
            )

            try:
                result = evaluate(**kw)
                record["results"][name] = result
                record["errors"].pop(name, None)

                print(
                    "  Analytic:",
                    result["same_functional_analytic_j_m"],
                    flush=True,
                )
                print(
                    "  Independent derivative defects:",
                    result["finite_minus_analytic_j_m"],
                    flush=True,
                )

            except Exception:
                record["errors"][name] = (
                    traceback.format_exc()
                )

                print(
                    record["errors"][name],
                    flush=True,
                )

            completed_new += 1
            checkpoint()

        rows = list(record["results"].values())

        complete = (
            not record["errors"]
            and len(rows) == len(jobs)
        )

        zero_control = any(
            row["zero_source"]
            and abs(row["interaction_action_j"]) < 1.e-10
            for row in rows
        )

        stationary = (
            bool(rows)
            and max(
                row["numerical_residuals"]["stationarity"]
                for row in rows
            ) < 1.e-8
        )

        derivative_check = (
            bool(rows)
            and all(
                row["maximum_abs_disagreement_j_m"] < .002
                for row in rows
            )
        )

        quadrature = {}

        for profile in ("c1", "c2"):
            for h in (.25, .2):
                selected = [
                    row for row in rows
                    if (
                        not row["zero_source"]
                        and row["profile"] == profile
                        and row["h"] == h
                        and row["step"] == 1.e-4
                        and row["order"] in (4, 8, 12)
                    )
                ]

                if len(selected) != 3:
                    continue

                values = [
                    row["same_functional_analytic_j_m"]["earth"]
                    for row in selected
                ]

                spread = max(values)-min(values)

                quadrature[f"{profile}_h{h}"] = {
                    "orders": [4, 8, 12],
                    "earth_derivative_spread_j_m": spread,
                    "relative_spread": (
                        spread/max(
                            1.0,
                            abs(next(
                                row["same_functional_analytic_j_m"]["earth"]
                                for row in selected
                                if row["order"] == 8
                            )),
                        )
                    ),
                }

        def quadrature_screen(profile):
            members = {
                key: value
                for key, value in quadrature.items()
                if key.startswith(profile + "_")
            }

            return (
                len(members) == 2
                and all(
                    x["relative_spread"] < 1.e-3
                    for x in members.values()
                )
            )

        gates = {
            "T0_all_predeclared_cases":
                "PASS" if complete else "FAIL_OR_PARTIAL",
            "T1_stationary_weighted_variation":
                "PASS" if complete and stationary
                else "FAIL_OR_PARTIAL",
            "T2_separately_resolved_Earth_craft_common":
                "PASS_SCREEN_ONLY"
                if complete and derivative_check
                else "FAIL_OR_PARTIAL",
            "T3_zero_source_negative_control":
                "PASS" if zero_control else "FAIL_OR_PARTIAL",
            "T4_C1_quadrature_screen":
                "PASS_SCREEN_ONLY"
                if quadrature_screen("c1")
                else "BLOCKED_OR_PARTIAL",
            "T5_C2_quadrature_screen":
                "PASS_SCREEN_ONLY"
                if quadrature_screen("c2")
                else "BLOCKED_OR_PARTIAL",
            "T6_C1_C2_mesh_domain_phase_limit":
                "NOT_CERTIFIED",
            "T7_M5P_exterior_closure_port":
                "NOT_IMPLEMENTED",
            "T8_independent_artificial_hull_assembly_action":
                "NOT_DERIVED",
            "T9_physical_Noether_metric_energy_lift":
                "NOT_ESTABLISHED",
        }

        record["summary"] = {
            "gates": gates,
            "complete_artificial_model": False,
            "quadrature_spreads": quadrature,
            "case_count": len(rows),
            "error_count": len(record["errors"]),
        }

        numerical_ok = (
            complete
            and stationary
            and derivative_check
            and zero_control
        )

        record["status"] = (
            "COMPLETE_NUMERICAL_DIAGNOSTIC_ONLY"
            if numerical_ok
            else "FAILED_OR_PARTIAL"
        )

        checkpoint()

        print(
            "UPLOAD_ONLY:",
            destination,
            flush=True,
        )
        print(
            "GATES:",
            json.dumps(gates, indent=2),
            flush=True,
        )

        return 0 if numerical_ok else 1

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
