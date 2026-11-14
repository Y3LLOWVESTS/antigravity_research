"""B17-M5O: fixed-boundary artificial continuum convergence falsifier.

SCIENTIFIC QUESTION
-------------------
Does the Earth-only derivative of the M5L stationary carrier action
converge when M5I's same prescribed source and material profiles
are resolved on successively finer meshes?

Common fractional-cell translations move the source, enclosure,
and Earth together inside an UNCHANGED outer computational box.
Because their distance to the boundary changes, this is a
translation-equivalence diagnostic, not a pure mesh-origin shift.
Domain enlargement must independently bound that confound.

ACTION
------
    H(x) = W A(x)
    H u = W j
    Q = 0.5 u^T H u - u^T W j
    dQ*/dx = 0.5 u^T H'(x) u

The derivative is taken with respect to Earth displacement while
the prescribed source and enclosure are held fixed.

The derivative operator is constructed analytically from the
material law and independently checked by finite differences
and re-solved stationary actions.

SOURCE
------
Reuse the M5I compact, stationary, neutral continuum trial source,
M5M physical dual-cell quadrature, original artificial amplitude
1e6, and portal input 21147 eV. No grid-dependent refitting.

CLAIM LIMITATIONS
-----------------
This is a prescribed, artificial, reduced carrier-action problem.
A signed derivative in J/m is NOT a certified physical force.

NOT ESTABLISHED:
- microscopic source action
- dynamical Ward/Noether closure
- healthy propagating modes
- physical exterior gravitational metric
- Earth/craft momentum exchange
- whole-spacecraft upward force
- complete operating energy below 10 MJ

Original M5I-M5N and 006D artifacts are never overwritten.
"""

from __future__ import annotations

from dataclasses import asdict, replace
import math
from unittest.mock import patch

import numpy as np
from scipy.sparse.linalg import spsolve

from . import hook17_fdual_f_loaded_payload_homotopy as carrier
from .hook17_fdual_f_loaded_payload_homotopy import (
    _build_elliptic_operators,
    _build_same_action_coupling,
)
from .hook17_r3b_m5i_continuum_source import (
    SourceSpec,
    reference_moments,
)
from .hook17_r3b_m5m_translation_consistency import (
    _dual_redeposit,
    carrier_action_conversion_j_per_native,
    PORTAL_SCALE_EV,
)
from .hook17_r3b_m5l_variational_audit import (
    assemble_variational_matrix,
)
from .hook17_r3b_m4b_sparse_earth_loading import (
    MaterialGeometry,
)
from .hook17_f2_strong_payload_loading_rescue import (
    loading_coefficient_z,
)

BRANCH = "032H17A12D1R3X3B17-ALPHA1R10-M5O-FIXEDBOX"

SOURCE = SourceSpec()
GEOMETRY = MaterialGeometry()

AMPLITUDE = 1.0e6

DOMAINS = {
    "compact": (7.0, -6.0, 8.0),
    "original": (12.0, -10.0, 13.0),
    "extended": (15.0, -12.0, 15.0),
}


def mesh(h, domain):
    """Construct a uniform grid with fixed physical box endpoints."""
    h = float(h)
    rmax, zmin, zmax = map(float, domain)

    if h <= 0 or not all(map(
        math.isfinite, (h, rmax, zmin, zmax)
    )):
        raise ValueError("Invalid physical box")

    nr = round(rmax / h)
    nz = round((zmax - zmin) / h)

    if (
        nr < 12
        or nz < 24
        or abs(nr * h - rmax) > 1e-8
        or abs(nz * h - (zmax - zmin)) > 1e-8
    ):
        raise ValueError("Box must be mesh-aligned")

    r = np.arange(nr + 1) * h
    z = zmin + np.arange(nz + 1) * h
    rr, zz = np.meshgrid(r, z)

    return {
        "h": h,
        "rhos": r,
        "zs": z,
        "rho_grid": rr,
        "z_grid": zz,
    }


def source_rhs(
    field, ops, shift, reversed_current=False, order=6
):
    """Deposit the same translated M5I continuum source."""
    if order not in (4, 6):
        raise ValueError("Quadrature order must be 4 or 6")

    spec = replace(
        SOURCE,
        azimuthal_current_amplitude=(
            -1.0 if reversed_current else 1.0
        ),
    )

    h = field["h"]
    r = field["rhos"]
    z = field["zs"][1:-1]

    e = _dual_redeposit(
        spec, r[:-1], z, h, shift, order
    )
    m = _dual_redeposit(
        spec, r[1:-1], z, h, shift, order
    )

    wp = r[:-1].copy()
    wp[0] = h / 8.0
    wa = r[1:-1]

    factor = (
        AMPLITUDE
        * (PORTAL_SCALE_EV / 1000.0)**2
        / (2.0 * math.pi * h * h)
    )

    jphi = factor * e["corrected_charge_cells"] / wp[None, :]
    ja = factor * m["current_cells"] / wa[None, :]
    j = np.r_[jphi.ravel(), ja.ravel()]

    expected = (
        ops["k_phi"].shape[0] + ops["k_a"].shape[0]
    )
    if j.size != expected:
        raise ValueError("Source/operator dimensions disagree")

    return j, {
        "continuum_source": asdict(spec),
        "shift_m": float(shift),
        "artificial_amplitude": AMPLITUDE,
        "portal_scale_ev": PORTAL_SCALE_EV,
        "order": order,
        "net_charge_before_projection_rel":
            e["raw_relative_net_charge"],
        "net_charge_after_projection_rel":
            e["projected_relative_net_charge"],
        "charge_projection_fraction":
            e["quadrature_correction_relative"],
        "electric_dipole_moment":
            e["electric_dipole_before_projection"],
        "magnetic_dipole_moment":
            m["magnetic_dipole"],
        "reference_moments":
            reference_moments(spec, order=80),
    }


def below(x, edge, w, profile):
    """Compact C1 or C2 material transition."""
    v = np.clip(
        (np.asarray(x) - edge + w) / (2 * w),
        0.0, 1.0,
    )

    if profile == "c1":
        return 1.0 - 3*v*v + 2*v*v*v
    if profile == "c2":
        return 1.0 - 10*v**3 + 15*v**4 - 6*v**5

    raise ValueError("Unknown interface profile")


def below_dedge(x, edge, w, profile):
    """Exact derivative of the transition with respect to edge."""
    v = (np.asarray(x) - edge + w) / (2*w)

    if profile == "c1":
        k = 3*v*(1-v)/w
    elif profile == "c2":
        k = 15*v*v*(1-v)**2/w
    else:
        raise ValueError("Unknown interface profile")

    return np.where((v > 0) & (v < 1), k, 0.0)


def material(
    field, shift, earth_offset, width, profile,
    earth_present=True,
):
    """Translate complete geometry; differentiate Earth only."""
    geo = GEOMETRY

    r = field["rho_grid"]
    z = field["z_grid"]

    rdist = np.hypot(r, z - shift)

    air = geo.air_density_kg_m3 * (
        1.0 - below(
            rdist, geo.enclosure_radius_m, width, profile
        )
    )

    disk = below(
        r, geo.ground_radius_m, width, profile
    )

    top = (
        shift + earth_offset
        + geo.ground_top_relative_z_m
    )
    bottom = top - geo.ground_depth_m

    bt = below(z, top, width, profile)
    ab = 1.0 - below(z, bottom, width, profile)

    fraction = (
        disk * bt * ab
        if earth_present
        else np.zeros_like(z)
    )

    density = (
        air
        + (geo.ground_density_kg_m3 - air) * fraction
    )

    beta = 1.0 - loading_coefficient_z(
        density, PORTAL_SCALE_EV
    )

    if earth_present:
        dt = disk * (
            below_dedge(z, top, width, profile) * ab
            - bt * below_dedge(z, bottom, width, profile)
        )
    else:
        dt = np.zeros_like(z)

    ddensity = (
        geo.ground_density_kg_m3 - air
    ) * dt

    coefficient = float(
        loading_coefficient_z(
            np.array([1.0]), PORTAL_SCALE_EV
        )[0]
        - loading_coefficient_z(
            np.array([0.0]), PORTAL_SCALE_EV
        )[0]
    )

    dbeta = -coefficient * ddensity

    return beta, dbeta, {
        "earth_top_m": top,
        "earth_bottom_m": bottom,
        "ground_radius_m": geo.ground_radius_m,
        "interface_width_m": width,
        "density_max_kg_m3": float(np.max(density)),
        "max_beta_derivative":
            float(np.max(np.abs(dbeta))),
    }


def weighted(field, ops, beta):
    """Assemble the same-action weighted operator without pruning."""
    with patch.object(
        carrier,
        "COUPLING_GRADIENT_RELATIVE_THRESHOLD",
        0.0,
    ):
        coupling = _build_same_action_coupling(
            field["rhos"],
            field["zs"],
            field["h"],
            beta,
            ops,
        )

    return assemble_variational_matrix(
        ops, coupling, field["rhos"], field["h"]
    )


def evaluate(
    h=0.2,
    domain=DOMAINS["compact"],
    width=0.5,
    profile="c2",
    phase=0.0,
    step=0.001,
    order=6,
    reversed_current=False,
    earth_present=True,
    zero_source=False,
    do_resolve=True,
    center_action_audit=False,
):
    """Evaluate one specified artificial reduced-action problem."""
    if (
        not all(map(math.isfinite, (h, width, phase, step)))
        or width <= 0
        or step <= 0
    ):
        raise ValueError("Invalid numerical experiment")

    if not -0.5 <= phase <= 0.5:
        raise ValueError("Invalid fractional translation")

    f = mesh(h, domain)
    shift = h * phase

    ops = _build_elliptic_operators(
        f["rhos"], f["zs"], h
    )

    j, source_audit = source_rhs(
        f, ops, shift, reversed_current, order
    )

    if zero_source:
        j = np.zeros_like(j)

    beta, dbeta, material_audit = material(
        f, shift, 0.0, width, profile, earth_present
    )

    A, H, W, asymmetry = weighted(f, ops, beta)
    u = spsolve(A, j)
    rhs = W*j

    residual = float(
        np.linalg.norm(A @ u - j)
        / max(np.linalg.norm(j), 1.0)
    )

    stationary = float(
        np.linalg.norm(H @ u - rhs)
        / max(np.linalg.norm(rhs), 1.0)
    )

    conversion = carrier_action_conversion_j_per_native(h)
    on_shell = -0.5 * conversion * float(u @ rhs)

    interaction_j = None

    if center_action_audit:
        air_beta = material(
            f, shift, 0.0, width, profile, False
        )[0]

        Aair, _, Wair, _ = weighted(
            f, ops, air_beta
        )

        if not np.array_equal(Wair, W):
            raise AssertionError("Air pairing weights changed")

        uair = spsolve(Aair, j)
        qair = -0.5 * conversion * float(
            uair @ rhs
        )

        interaction_j = on_shell - qair

    # Differentiate the discrete stationary matrix analytically.
    # The diagonal elliptic operators are beta-independent.
    H0 = weighted(
        f, ops, np.zeros_like(dbeta)
    )[1]

    Hprime = weighted(f, ops, dbeta)[1] - H0

    rows = 0.5 * conversion * u * (Hprime @ u)
    derivative = float(rows.sum())

    # Independent finite difference of the weighted operator.
    bp = material(
        f, shift, step, width, profile, earth_present
    )[0]
    bm = material(
        f, shift, -step, width, profile, earth_present
    )[0]

    Ap, Hp, Wp, _ = weighted(f, ops, bp)
    Am, Hm, Wm, _ = weighted(f, ops, bm)

    if not (
        np.array_equal(W, Wp)
        and np.array_equal(W, Wm)
    ):
        raise AssertionError("Material-dependent source weights")

    hfinite = (
        0.5 * conversion
        * float(u @ ((Hp - Hm) @ u))
        / (2 * step)
    )

    resolved = None

    if do_resolve:
        up = spsolve(Ap, j)
        um = spsolve(Am, j)

        resolved = (
            -0.5 * conversion
            * (float(up @ rhs) - float(um @ rhs))
            / (2 * step)
        )

    return {
        "branch": BRANCH,
        "claim": "ARTIFICIAL_STATIONARY_REDUCED_ACTION_ONLY",
        "h_m": h,
        "domain_m": list(domain),
        "actual_box_m": [
            float(f["rhos"][-1]),
            float(f["zs"][0]),
            float(f["zs"][-1]),
        ],
        "physical_config_common_shift_m": shift,
        "fractional_shift": phase,
        "interface_profile": profile,
        "interface_width_m": width,
        "source": source_audit,
        "material": material_audit,
        "earth_present": earth_present,
        "zero_source": zero_source,
        "reversed_current": reversed_current,
        "derivative_analytic_j_m": derivative,
        "derivative_H_finite_difference_j_m": hfinite,
        "derivative_resolved_j_m": resolved,
        "earth_step_m": step,
        "derivative_H_difference_error_j_m":
            hfinite - derivative,
        "derivative_resolve_difference_error_j_m":
            None if resolved is None else resolved - derivative,
        "on_shell_q_earth_j": on_shell,
        "earth_minus_air_reduced_action_j": interaction_j,
        "operator_residual": residual,
        "stationarity_residual": stationary,
        "weighted_operator_asymmetry": float(asymmetry),
        "signed_rows_j_m": {
            "sum": derivative,
            "absolute_sum": float(np.abs(rows).sum()),
            "cancellation_ratio":
                float(np.abs(rows).sum())
                / max(abs(derivative), 1e-300),
        },
        "source_physically_derived": False,
        "physical_force_certified": False,
        "earth_craft_momentum_exchange_certified": False,
        "whole_craft_lift_certified": False,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
    }


def _registered_jobs(mode):
    """Register all controls before inspecting results."""
    jobs = []

    def add(name, **kwargs):
        if any(x[0] == name for x in jobs):
            raise AssertionError("Duplicate case: " + name)
        jobs.append((name, kwargs))

    # Original M5K/M5N action and derivative controls.
    for h in (0.25, 0.2):
        add(
            "historical_" + str(h),
            h=h,
            domain=DOMAINS["original"],
            width=0.25,
            profile="c1",
            step=0.001,
            center_action_audit=True,
        )

    # Fixed physical interface and source across resolutions.
    for domain in ("compact", "original", "extended"):
        hs = (
            (0.25, 0.2, 0.125, 0.1, 0.0625)
            if domain == "compact"
            else (0.2, 0.1, 0.0625)
        )

        if mode == "full":
            hs = (*hs, 0.05)

        for h in hs:
            add(
                "mesh_" + domain + "_" + str(h),
                h=h,
                domain=DOMAINS[domain],
                do_resolve=False,
            )

    # Translate physical source, enclosure and Earth together.
    # Keep the outer box fixed in physical coordinates.
    for h in (
        (0.2, 0.1, 0.0625, 0.05)
        if mode == "full"
        else (0.2, 0.1, 0.0625)
    ):
        for domain in ("compact", "original"):
            for phase in (-0.5, -0.25, 0.25, 0.5):
                if mode == "quick" and phase in (-0.25, 0.25):
                    continue

                add(
                    "phase_" + domain
                    + "_" + str(h)
                    + "_" + str(phase),
                    h=h,
                    domain=DOMAINS[domain],
                    phase=phase,
                    do_resolve=False,
                )

    add("zero_earth", h=0.25, earth_present=False,
        do_resolve=False)
    add("zero_source", h=0.25, zero_source=True,
        do_resolve=False)
    add("source_order4", h=0.2, order=4)
    add("magnetic_reversed", h=0.2, reversed_current=True)

    if mode == "full":
        # Independent outer-box enlargement.
        for size, dom in (
            (21, (21., -16., 19.)),
            (24, (24., -18., 21.)),
            (30, (30., -22., 25.)),
        ):
            for h in (
                (0.1, 0.0625, 0.05)
                if size != 30
                else (0.1, 0.0625)
            ):
                add(
                    "domain_" + str(size) + "_" + str(h),
                    h=h, domain=dom, do_resolve=False,
                )

        # Different interface profiles are separate artificial models.
        for width, profile in (
            (0.25, "c1"),
            (0.25, "c2"),
            (0.5, "c1"),
        ):
            for h in (0.2, 0.1, 0.0625):
                add(
                    f"width_{profile}_{width}_{h}",
                    h=h,
                    width=width,
                    profile=profile,
                    do_resolve=False,
                )

        # Explicitly isolate the historical C1 endpoint step bias.
        for step in (0.002, 0.0001, 0.00001):
            add(
                "step_C1_" + str(step),
                h=0.25,
                domain=DOMAINS["original"],
                width=0.25,
                profile="c1",
                step=step,
            )

    return jobs


def _summary(joblist, results, mode):
    """Fail-closed scientific classification."""
    historical_d = {
        0.25: -1.8335603471034372,
        0.2: -9.888729681527348,
    }
    historical_q = {
        0.25: -7.743566757,
        0.2: -7.121916830,
    }

    historical = {}

    for h in historical_d:
        r = results.get("historical_" + str(h))
        if r:
            historical[str(h)] = {
                "m5n_difference_j_m":
                    r["derivative_H_finite_difference_j_m"]
                    - historical_d[h],
                "m5k_interaction_difference_j":
                    r["earth_minus_air_reduced_action_j"]
                    - historical_q[h],
                "exact_derivative_j_m":
                    r["derivative_analytic_j_m"],
                "historical_one_mm_derivative_j_m":
                    r["derivative_H_finite_difference_j_m"],
            }

    source_ok = True
    operator_ok = True
    derivative_ok = True

    for name, r in results.items():
        s = r["source"]
        ref = s["reference_moments"]

        es = abs(
            s["electric_dipole_moment"]
            - ref["electric_dipole_z_integral"]
        ) / max(
            1e-30,
            abs(ref["electric_dipole_z_integral"]),
        )

        ms = abs(
            s["magnetic_dipole_moment"]
            - ref["magnetic_dipole_z_integral"]
        ) / max(
            1e-30,
            abs(ref["magnetic_dipole_z_integral"]),
        )

        source_ok &= max(
            es, ms,
            s["net_charge_after_projection_rel"],
            s["charge_projection_fraction"],
        ) < 1e-3

        operator_ok &= (
            r["operator_residual"] < 1e-9
            and r["stationarity_residual"] < 1e-9
            and r["weighted_operator_asymmetry"] < 1e-10
        )

        d = r["derivative_analytic_j_m"]
        tolerance = max(0.05, 0.01 * abs(d))

        derivative_ok &= abs(
            r["derivative_H_difference_error_j_m"]
        ) < tolerance

        if r["derivative_resolved_j_m"] is not None:
            derivative_ok &= abs(
                r["derivative_resolve_difference_error_j_m"]
            ) < tolerance

    historical_ok = (
        len(historical) == 2
        and all(
            abs(x["m5n_difference_j_m"]) < 1e-6
            and abs(x["m5k_interaction_difference_j"]) < 1e-5
            for x in historical.values()
        )
    )

    mesh_table = {}
    extrapolations = {}
    phase_table = {}
    domains = {}

    for label in ("compact", "original", "extended"):
        points = []

        for h in (
            0.25, 0.2, 0.125, 0.1, 0.0625, 0.05
        ):
            name = "mesh_" + label + "_" + str(h)
            if name in results:
                points.append([
                    h, results[name]["derivative_analytic_j_m"]
                ])

        mesh_table[label] = points

        if len(points) >= 3:
            # Hypothetical second-order fit, NOT continuum certification.
            xs = np.array([
                p[0]**2 for p in points[-3:]
            ])
            ys = np.array([
                p[1] for p in points[-3:]
            ])

            c = np.polyfit(xs, ys, 1)

            extrapolations[label] = {
                "last_three_mesh_m":
                    [p[0] for p in points[-3:]],
                "h_squared_continuum_candidate_j_m":
                    float(c[1]),
                "fit_max_residual_j_m":
                    float(np.max(np.abs(
                        ys - np.polyval(c, xs)
                    ))),
                "assumed_order": 2,
                "finite_outer_box": True,
                "certified": False,
            }

    for label in ("compact", "original"):
        for h in (0.2, 0.1, 0.0625, 0.05):
            names = [
                "mesh_" + label + "_" + str(h)
            ] + [
                "phase_" + label
                + "_" + str(h)
                + "_" + str(v)
                for v in (-0.5, -0.25, 0.25, 0.5)
            ]

            values = [
                results[n]["derivative_analytic_j_m"]
                for n in names
                if n in results
            ]

            if len(values) >= 3:
                phase_table[label + "_" + str(h)] = {
                    "spread_j_m":
                        max(values) - min(values),
                    "values_j_m": values,
                    "fixed_outer_box": True,
                    "not_a_pure_grid_origin_shift": True,
                }

    for h in (0.2, 0.1, 0.0625, 0.05):
        vals = {}

        for label in ("compact", "original", "extended"):
            name = "mesh_" + label + "_" + str(h)
            if name in results:
                vals[label] = results[name][
                    "derivative_analytic_j_m"
                ]

        for radius in (21, 24, 30):
            name = "domain_" + str(radius) + "_" + str(h)
            if name in results:
                vals[str(radius)] = results[name][
                    "derivative_analytic_j_m"
                ]

        if len(vals) > 1:
            domains[str(h)] = vals

    noearth = results.get(
        "zero_earth", {}
    ).get("derivative_analytic_j_m")

    nosource = results.get(
        "zero_source", {}
    ).get("derivative_analytic_j_m")

    neg_ok = (
        noearth is not None
        and nosource is not None
        and abs(noearth) < 1e-10
        and abs(nosource) < 1e-10
    )

    complete = len(results) == len(joblist)

    claims_ok = all(
        not r["physical_force_certified"]
        and not r["whole_craft_lift_certified"]
        and r["complete_operating_energy_j"] is None
        for r in results.values()
    )

    return {
        "branch": BRANCH,
        "mode": mode,
        "registered": len(joblist),
        "completed": len(results),
        "gates": {
            "N0_source":
                "PASS" if complete and source_ok
                else "FAIL_OR_INCOMPLETE",
            "N1_action":
                "PASS" if complete and operator_ok and historical_ok
                else "FAIL_OR_INCOMPLETE",
            "N2_derivative":
                "PASS" if complete and derivative_ok
                else "FAIL_OR_INCOMPLETE",
            "N3_phase_and_mesh":
                "YELLOW_FINITE_DOMAIN_CONTINUUM_NOT_CERTIFIED",
            "N4_material_width":
                "YELLOW_MODEL_DEPENDENT_NO_SHARP_LIMIT",
            "N5_domain":
                "YELLOW_OUTER_BOUNDARY_REMAINS_ACTIVE",
            "N6_negative_controls":
                "PASS" if neg_ok
                else "FAIL_OR_INCOMPLETE",
            "N7_claim_scope":
                "PASS" if complete and claims_ok
                else "FAIL_OR_INCOMPLETE",
        },
        "historical_reproduction": historical,
        "mesh_derivatives_j_m": mesh_table,
        "fixed_domain_h2_extrapolations": extrapolations,
        "phase_spreads": phase_table,
        "domain_derivatives_j_m": domains,
        "negative_controls": {
            "zero_earth_j_m": noearth,
            "zero_source_j_m": nosource,
        },
        "source_fit_not_physical": True,
        "derivative_is_not_whole_craft_force": True,
        "external_reaction_not_derived": True,
        "continuum_force_not_certified": True,
        "complete_energy_under_10mj_certified": False,
        "006d_replaced": False,
    }


def main():
    import argparse
    import json
    from datetime import datetime, timezone
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode", choices=("quick", "full"), default="quick"
    )
    parser.add_argument(
        "--results-dir", default="results/data"
    )
    args = parser.parse_args()

    jobs = _registered_jobs(args.mode)
    folder = Path(args.results_dir)
    folder.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"
    )
    prefix = f"b17_m5o_fixed_box_{stamp}_{args.mode}"

    (folder / f"{prefix}_manifest.json").write_text(
        json.dumps({
            "branch": BRANCH,
            "cases": [
                {"name": n, "parameters": kw}
                for n, kw in jobs
            ],
        }, indent=2) + "\n"
    )

    results = {}
    errors = {}

    for i, (name, kw) in enumerate(jobs, 1):
        print(f"[{i}/{len(jobs)}] {name}", flush=True)

        try:
            value = evaluate(**kw)
            results[name] = value

            (folder / f"{prefix}_{name}.json").write_text(
                json.dumps(
                    value, indent=2, sort_keys=True
                ) + "\n"
            )

            print(
                "  Prescribed derivative [J/m]:",
                value["derivative_analytic_j_m"],
                flush=True,
            )

        except Exception as exc:
            errors[name] = repr(exc)
            print("FAILED:", repr(exc), flush=True)

    summary = _summary(jobs, results, args.mode)
    summary["errors"] = errors

    summary_path = folder / f"{prefix}_summary.json"
    summary_path.write_text(
        json.dumps(
            summary, indent=2, sort_keys=True
        ) + "\n"
    )

    print("M5O summary:", summary_path)
    print("GATES:", json.dumps(summary["gates"], indent=2))

    return 1 if errors or any(
        s == "FAIL_OR_INCOMPLETE"
        for s in summary["gates"].values()
    ) else 0


if __name__ == "__main__":
    raise SystemExit(main())
