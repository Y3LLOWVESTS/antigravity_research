"""B17-M5Q: reduced-action virtual-work translation closure audit.

For the prescribed stationary functional H(s,e)=W A(s,e),

    Q(u;s,e) = c*(0.5*u.T@H@u - u.T@W@j(s))

the on-shell derivatives are

    dQ*/de = c*0.5*u.T@H_e@u
    dQ*/ds = c*(0.5*u.T@H_s@u - u.T@W@j_s)

The common translation derivative is their sum.

The source derivative includes the analytic derivative of the M5M
dual-cell quadrature and its numerical neutrality projection.

Finite-grid common-shift residuals do not constitute true physical
Earth/craft forces. No complete source matter action, Noether stress,
metric response or complete device energy is implied.

All artificial amplitudes remain explicitly prescribed.
006D is unreplaced.
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
from scipy.sparse.linalg import spsolve

from . import hook17_r3b_m5o_fixed_box as m5o
from . import hook17_r3b_m5p_exterior_boundary as m5p
from .hook17_r3b_m5m_translation_consistency import (
    carrier_action_conversion_j_per_native,
)

BRANCH = (
    "032H17A12D1R3X3B17-"
    "ALPHA1R12-M5Q-TRANSLATION"
)

REFERENCE = {
    ("compact", .2): -12.7882913449623,
    ("compact", .1): -11.790388401910823,
    ("compact", .0625): -11.49124392008987,
    ("compact", .05): -11.423904983849905,
    ("original", .2): -12.791192797359773,
    ("original", .1): -11.792488561807556,
    ("original", .0625): -11.493276097709023,
    ("original", .05): -11.425932326932216,
    ("extended", .1): -11.792846221468729,
    ("extended", .0625): -11.49361437570856,
    ("extended", .05): -11.42626740911225,
}


def analytic_source_translation(field, shift, order=6):
    """Differentiate the M5I/M5M prescribed source deposition exactly.

    Includes the charge-neutrality quadrature projection.
    This is not a physical source Euler-Lagrange equation.
    """
    spec = m5o.SOURCE
    h = field["h"]
    nodes, weights = leggauss(order)

    factor = (
        m5o.AMPLITUDE
        * (m5o.PORTAL_SCALE_EV / 1000.0)**2
        / (2.0 * math.pi * h*h)
    )

    def deposit(radial_nodes):
        rnodes = np.asarray(radial_nodes, dtype=float)
        znodes = field["zs"][1:-1]

        rlow = np.maximum(0.0, rnodes-h/2.0)
        rhigh = rnodes+h/2.0
        rmid = (rlow+rhigh)/2.0
        rhalf = (rhigh-rlow)/2.0

        shape = (len(znodes), len(rnodes))
        charge = np.zeros(shape)
        compensator = np.zeros(shape)
        dcharge = np.zeros(shape)
        dcompensator = np.zeros(shape)
        dcurrent = np.zeros(shape)

        for i, xi in enumerate(nodes):
            rho = (rmid+rhalf*xi)[None, :]
            wr = rhalf[None, :]*weights[i]

            ur = (
                (rho-spec.radial_center_m)
                / spec.radial_halfwidth_m
            )**2

            for k, xk in enumerate(nodes):
                relative_z = (
                    znodes+h*xk/2.0-shift
                )[:, None]

                scaled_z = (
                    relative_z/spec.axial_halfwidth_m
                )

                bumpbase = np.maximum(
                    1.0-ur-scaled_z**2, 0.0
                )

                b4 = bumpbase**4
                b5 = bumpbase**5

                db5_ds = (
                    10.0*relative_z
                    / spec.axial_halfwidth_m**2*b4
                )

                rho_e = (
                    spec.density_amplitude
                    * scaled_z*b5
                )

                d_rho_e = (
                    spec.density_amplitude
                    * (
                        -b5/spec.axial_halfwidth_m
                        + scaled_z*db5_ds
                    )
                )

                dv = (
                    2.0*math.pi*rho*wr
                    * (h*weights[k]/2.0)
                )

                charge += rho_e*dv
                dcharge += d_rho_e*dv
                compensator += b5*dv
                dcompensator += db5_ds*dv

                dcurrent += (
                    spec.azimuthal_current_amplitude
                    * db5_ds*dv
                )

        raw = float(np.sum(charge))
        norm = float(np.sum(compensator))
        draw = float(np.sum(dcharge))
        dnorm = float(np.sum(dcompensator))

        if norm <= 0.0:
            raise ArithmeticError(
                "Empty neutrality projection"
            )

        coefficient = raw/norm
        dcoefficient = (
            draw*norm-raw*dnorm
        )/norm**2

        dprojected = (
            dcharge
            - dcoefficient*compensator
            - coefficient*dcompensator
        )

        return (
            dprojected,
            dcharge,
            dcurrent,
            {
                "raw_charge": raw,
                "raw_charge_derivative": draw,
                "compensator_integral": norm,
                "projection_coefficient": coefficient,
                "projection_derivative": dcoefficient,
                "projected_charge_derivative_sum":
                    float(np.sum(dprojected)),
            },
        )

    dscalar, draw, _, sa = deposit(
        field["rhos"][:-1]
    )

    _, _, dvector, va = deposit(
        field["rhos"][1:-1]
    )

    wp = field["rhos"][:-1].copy()
    wp[0] = h/8.0
    wa = field["rhos"][1:-1]

    scalar = (
        factor*dscalar/wp[None, :]
    ).ravel()

    scalar_raw = (
        factor*draw/wp[None, :]
    ).ravel()

    vector = (
        factor*dvector/wa[None, :]
    ).ravel()

    return np.r_[scalar, vector], {
        "scalar_unprojected_rhs_derivative": scalar_raw,
        "scalar_projected_rhs_derivative": scalar,
        "electric_projection": sa,
        "vector_deposition": va,
    }


def evaluate(
    h=.2,
    domain=m5p.BOUNDS["compact"],
    closure="dipole_trace",
    profile="c2",
    width=.5,
    phase=0.,
    step=1.e-4,
    order=6,
    earth_present=True,
    zero_source=False,
    resolve=False,
    direct_craft=True,
):
    """Check the complete translation derivative of the reduced action."""
    parameters = (h, width, phase, step)

    if not all(map(math.isfinite, parameters)):
        raise ValueError("Nonfinite M5Q input")

    if not (
        h > 0 and width > 0 and step > 0
        and -.5 <= phase <= .5
        and order in (4, 6)
    ):
        raise ValueError("Invalid M5Q parameter range")

    field = m5o.mesh(h, domain)
    shift = h*phase

    ops, boundary_audit = m5p.robin_operators(
        field, closure
    )

    conv = carrier_action_conversion_j_per_native(h)

    def build(ss, ee, solve=False):
        j, source_audit = m5o.source_rhs(
            field, ops, ss, order=order
        )

        if zero_source:
            j = np.zeros_like(j)

        beta, dbeta, material_audit = m5o.material(
            field,
            ss,
            ee,
            width,
            profile,
            earth_present,
        )

        A, H, W, asym = m5o.weighted(
            field, ops, beta
        )

        u = spsolve(A, j) if solve else None

        return {
            "j": j,
            "source_audit": source_audit,
            "beta": beta,
            "dbeta": dbeta,
            "material_audit": material_audit,
            "A": A,
            "H": H,
            "W": W,
            "asym": asym,
            "u": u,
        }

    base = build(shift, 0., True)

    u = base["u"]
    W = base["W"]
    j = base["j"]
    H = base["H"]

    common_plus = build(shift+step, 0.)
    common_minus = build(shift-step, 0.)

    earth_plus = build(shift, step)
    earth_minus = build(shift, -step)

    dj_fd = (
        common_plus["j"]-common_minus["j"]
    )/(2.*step)

    dj, derivative_audit = analytic_source_translation(
        field, shift, order
    )

    if zero_source:
        dj = np.zeros_like(dj)
        derivative_audit[
            "scalar_unprojected_rhs_derivative"
        ] = np.zeros_like(
            derivative_audit[
                "scalar_unprojected_rhs_derivative"
            ]
        )

    source_derivative_defect = float(
        np.linalg.norm(dj-dj_fd)
        / max(np.linalg.norm(dj), 1.0)
    )

    if (
        not np.isfinite(source_derivative_defect)
        or source_derivative_defect > .005
    ):
        raise ArithmeticError(
            "Analytic source derivative mismatch"
        )

    Hcommon = (
        common_plus["H"]-common_minus["H"]
    )/(2.*step)

    Hearth_finite = (
        earth_plus["H"]-earth_minus["H"]
    )/(2.*step)

    Hzero = m5o.weighted(
        field,
        ops,
        np.zeros_like(base["dbeta"]),
    )[1]

    Hearth = m5o.weighted(
        field,
        ops,
        base["dbeta"],
    )[1]-Hzero

    def operator_term(matrix):
        return float(
            .5*conv*np.dot(u, matrix@u)
        )

    earth = operator_term(Hearth)
    earth_finite = operator_term(Hearth_finite)

    common_operator = operator_term(Hcommon)
    source_total = float(
        -conv*np.dot(u, W*dj)
    )

    nphi = ops["k_phi"].shape[0]

    source_scalar = float(
        -conv*np.dot(
            u[:nphi], W[:nphi]*dj[:nphi]
        )
    )

    source_vector = float(
        -conv*np.dot(
            u[nphi:], W[nphi:]*dj[nphi:]
        )
    )

    source_scalar_raw = float(
        -conv*np.dot(
            u[:nphi],
            W[:nphi] * derivative_audit[
                "scalar_unprojected_rhs_derivative"
            ],
        )
    )

    source_scalar_projection = (
        source_scalar-source_scalar_raw
    )

    enclosure_inferred = common_operator-earth
    common_total = common_operator+source_total

    craft_inferred = (
        enclosure_inferred+source_total
    )

    craft_direct = None
    craft_plus = None
    craft_minus = None

    if direct_craft:
        # Move craft, but hold physical Earth fixed.
        craft_plus = build(shift+step, -step)
        craft_minus = build(shift-step, step)

        craft_direct = (
            operator_term(
                (
                    craft_plus["H"]
                    - craft_minus["H"]
                )/(2.*step)
            )
            + source_total
        )

    def on_shell(sol):
        return float(
            -.5*conv*np.dot(
                sol["u"],
                sol["W"]*sol["j"],
            )
        )

    resolved_checks = None

    if resolve:
        for state in (
            earth_plus,
            earth_minus,
            common_plus,
            common_minus,
        ):
            state["u"] = spsolve(
                state["A"], state["j"]
            )

        resolved_checks = {
            "earth_j_m": (
                on_shell(earth_plus)
                - on_shell(earth_minus)
            )/(2.*step),
            "common_j_m": (
                on_shell(common_plus)
                - on_shell(common_minus)
            )/(2.*step),
        }

        if direct_craft:
            for state in (
                craft_plus,
                craft_minus,
            ):
                state["u"] = spsolve(
                    state["A"], state["j"]
                )

            resolved_checks["craft_j_m"] = (
                on_shell(craft_plus)
                - on_shell(craft_minus)
            )/(2.*step)

    stationary = float(
        np.linalg.norm(H@u-W*j)
        / max(np.linalg.norm(W*j), 1.)
    )

    operator_residual = float(
        np.linalg.norm(base["A"]@u-j)
        / max(np.linalg.norm(j), 1.)
    )

    derivatives = {
        "earth_operator_analytic": earth,
        "earth_operator_finite_difference":
            earth_finite,
        "common_operator_finite_difference":
            common_operator,
        "source_explicit_total": source_total,
        "source_explicit_scalar": source_scalar,
        "source_explicit_vector": source_vector,
        "source_explicit_scalar_raw":
            source_scalar_raw,
        "source_explicit_scalar_projection":
            source_scalar_projection,
        "enclosure_operator_inferred":
            enclosure_inferred,
        "craft_earth_fixed_inferred":
            craft_inferred,
        "craft_earth_fixed_direct":
            craft_direct,
        "common_total": common_total,
        "common_minus_earth_plus_craft": (
            None if craft_direct is None
            else common_total-earth-craft_direct
        ),
    }

    return {
        "branch": BRANCH,
        "scope": "ARTIFICIAL_REDUCED_ACTION_TRANSLATION_ONLY",
        "h_m": h,
        "domain_m": list(domain),
        "closure": closure,
        "profile": profile,
        "width_m": width,
        "phase": phase,
        "translation_step_m": step,
        "order": order,
        "earth_present": earth_present,
        "zero_source": zero_source,
        "source_audit": base["source_audit"],
        "boundary_audit": boundary_audit,
        "derivative_terms_j_m": derivatives,
        "on_shell_derivative_re_solved": resolved_checks,
        "stationarity_residual": stationary,
        "operator_residual": operator_residual,
        "weighted_operator_asymmetry": float(
            base["asym"]
        ),
        "on_shell_action_j": on_shell(base),
        "source_derivative_relative_norm_per_m": float(
            np.linalg.norm(dj)
            / max(np.linalg.norm(j), 1.)
        ),
        "source_derivative_fd_relative_defect":
            source_derivative_defect,
        "source_projection_derivative": {
            "electric_projection":
                derivative_audit["electric_projection"],
        },
        "physical_earth_craft_reciprocity_certified": False,
        "source_matter_action_derived": False,
        "whole_spacecraft_lift_certified": False,
        "complete_device_energy_j": None,
        "006d_replaced": False,
    }


def jobs(mode):
    """Targeted matrix. No amplitude or material fitting."""
    if mode not in ("quick", "full"):
        raise ValueError("Invalid mode")

    tasks = []
    names = set()

    def add(name, **kwargs):
        if name in names:
            raise AssertionError(name)
        names.add(name)
        tasks.append((name, kwargs))

    add("base_compact_0.2", h=.2, resolve=True)
    add("base_compact_0.1", h=.1, resolve=True)
    add(
        "base_original_0.1",
        h=.1,
        domain=m5p.BOUNDS["original"],
    )
    add(
        "control_no_earth",
        h=.25,
        earth_present=False,
        resolve=True,
    )
    add(
        "control_zero_source",
        h=.25,
        zero_source=True,
        resolve=True,
    )
    add(
        "model_c1_0.25",
        h=.125,
        profile="c1",
        width=.25,
        resolve=True,
    )

    if mode == "full":
        for label, meshes in (
            ("compact", (.25, .125, .0625, .05)),
            ("original", (.2, .0625, .05)),
            ("extended", (.1, .0625, .05)),
            ("outer21", (.2, .1)),
        ):
            for h in meshes:
                add(
                    f"mesh_{label}_{h}",
                    h=h,
                    domain=m5p.BOUNDS[label],
                    direct_craft=(h >= .0625),
                    resolve=(
                        h >= .125 and label == "compact"
                    ),
                )

        for h in (.2, .1, .0625):
            for phase in (-.5, -.25, .25, .5):
                add(
                    f"phase_compact_{h}_{phase}",
                    h=h,
                    phase=phase,
                    direct_craft=False,
                )

        for h in (.25, .2, .1, .0625, .05):
            add(
                f"c1_mesh_compact_{h}",
                h=h,
                profile="c1",
                width=.25,
                direct_craft=(h >= .1),
            )

        for h in (.2, .1):
            add(
                f"quad4_compact_{h}",
                h=h,
                order=4,
            )

        for step in (1.e-3, 1.e-5):
            add(
                f"step_compact_0.125_{step}",
                h=.125,
                step=step,
                resolve=True,
            )

        add(
            "dirichlet_control",
            h=.1,
            closure="dirichlet",
        )

        add(
            "robin_control",
            h=.1,
            closure="dipole_robin",
        )

    return tasks


def summarize(tasklist, results):
    """Numerical certificates cannot promote a physical claim."""
    complete = len(results) == len(tasklist)
    match = {}

    reference_ok = True
    action_ok = complete
    split_ok = complete
    derivative_ok = complete
    zero_ok = complete

    for name, kwargs in tasklist:
        if name not in results:
            continue

        row = results[name]
        d = row["derivative_terms_j_m"]

        action_ok &= (
            row["operator_residual"] < 1.e-8
            and row["stationarity_residual"] < 1.e-8
            and row["weighted_operator_asymmetry"] < 1.e-10
        )

        split_ok &= abs(
            d["source_explicit_scalar"]
            + d["source_explicit_vector"]
            - d["source_explicit_total"]
        ) < 1.e-7

        split_ok &= abs(
            d["source_explicit_scalar_raw"]
            + d["source_explicit_scalar_projection"]
            - d["source_explicit_scalar"]
        ) < 1.e-7

        derivative_ok &= (
            row["source_derivative_fd_relative_defect"]
            < .005
        )

        if d["craft_earth_fixed_direct"] is not None:
            split_ok &= abs(
                d["common_minus_earth_plus_craft"]
            ) < max(
                .02,
                .005*abs(d["common_total"]),
            )

        derivative_ok &= abs(
            d["earth_operator_finite_difference"]
            - d["earth_operator_analytic"]
        ) < max(
            .02,
            .005*abs(d["earth_operator_analytic"]),
        )

        resolved = row["on_shell_derivative_re_solved"]

        if resolved:
            comparisons = (
                (
                    "earth_j_m",
                    d["earth_operator_analytic"],
                ),
                (
                    "common_j_m",
                    d["common_total"],
                ),
                (
                    "craft_j_m",
                    d["craft_earth_fixed_direct"],
                ),
            )

            for key, expected in comparisons:
                if key in resolved:
                    derivative_ok &= abs(
                        resolved[key]-expected
                    ) < max(
                        .02,
                        .005*abs(expected),
                    )

        if (
            row["phase"] == 0
            and row["profile"] == "c2"
            and row["width_m"] == .5
            and row["order"] == 6
            and row["closure"] == "dipole_trace"
            and row["earth_present"]
            and not row["zero_source"]
        ):
            for (label, h), expected in REFERENCE.items():
                if (
                    tuple(row["domain_m"])
                    == m5p.BOUNDS[label]
                    and h == row["h_m"]
                ):
                    actual = d["earth_operator_analytic"]

                    match[name] = {
                        "difference_j_m":
                            actual-expected,
                        "reference_j_m": expected,
                    }

                    reference_ok &= (
                        abs(actual-expected) < 1.e-7
                    )

        if name == "control_no_earth":
            zero_ok &= abs(
                d["earth_operator_analytic"]
            ) < 1.e-10

        if name == "control_zero_source":
            zero_ok &= max(
                abs(value)
                for value in d.values()
                if value is not None
            ) < 1.e-10

    translation_balance = []

    for name, row in results.items():
        if (
            row["phase"] == 0
            and row["profile"] == "c2"
            and row["closure"] == "dipole_trace"
            and row["earth_present"]
            and not row["zero_source"]
            and row["order"] == 6
        ):
            d = row["derivative_terms_j_m"]

            translation_balance.append({
                "name": name,
                "h_m": row["h_m"],
                "domain_m": row["domain_m"],
                "earth_j_m":
                    d["earth_operator_analytic"],
                "craft_j_m":
                    d["craft_earth_fixed_inferred"],
                "common_j_m": d["common_total"],
            })

    phase_spreads = {}

    for h in (.2, .1, .0625):
        names = [
            f"phase_compact_{h}_{phase}"
            for phase in (-.5, -.25, .25, .5)
        ]

        center = (
            "base_compact_0.2" if h == .2
            else "base_compact_0.1" if h == .1
            else "mesh_compact_0.0625"
        )

        names.append(center)

        if all(name in results for name in names):
            values = [
                results[name][
                    "derivative_terms_j_m"
                ]["common_total"]
                for name in names
            ]

            phase_spreads[str(h)] = {
                "max_minus_min_j_m":
                    max(values)-min(values),
                "max_absolute_j_m":
                    max(abs(x) for x in values),
                "certified": False,
            }

    fine_names = (
        "mesh_compact_0.05",
        "mesh_original_0.05",
        "mesh_extended_0.05",
    )

    fine = None

    if all(n in results for n in fine_names):
        fine = {
            n: results[n][
                "derivative_terms_j_m"
            ]["common_total"]
            for n in fine_names
        }

    return {
        "branch": BRANCH,
        "registered": len(tasklist),
        "completed": len(results),
        "gates": {
            "Q0_m5p_Earth_derivative_reproduction": (
                "PASS"
                if complete and reference_ok and len(match) >= 2
                else "FAIL_OR_INCOMPLETE"
            ),
            "Q1_stationary_quadratic_action": (
                "PASS"
                if action_ok else "FAIL_OR_INCOMPLETE"
            ),
            "Q2_Hellmann_Feynman_resolved": (
                "PASS"
                if derivative_ok else "FAIL_OR_INCOMPLETE"
            ),
            "Q3_total_source_enclosure_Earth_partition": (
                "PASS"
                if split_ok else "FAIL_OR_INCOMPLETE"
            ),
            "Q4_negative_controls": (
                "PASS"
                if zero_ok else "FAIL_OR_INCOMPLETE"
            ),
            "Q5_infinite_domain_translation_limit":
                "YELLOW_NOT_PROVEN",
            "Q6_material_and_grid_phase":
                "YELLOW_NOT_PROVEN",
            "Q7_physical_Noether_reciprocity":
                "NOT_ESTABLISHED",
            "Q8_complete_operating_energy":
                "NOT_ESTABLISHED",
        },
        "m5p_earth_reproduction": match,
        "translation_balance_matrix":
            translation_balance,
        "common_translation_phase_spreads":
            phase_spreads,
        "fine_mesh_common_translation_by_box":
            fine,
        "max_source_translation_fd_relative_defect":
            max(
                [
                    r["source_derivative_fd_relative_defect"]
                    for r in results.values()
                ],
                default=None,
            ),
        "physical_action_or_force_certified": False,
        "006d_replaced": False,
    }


def main():
    parser = argparse.ArgumentParser(
        description=__doc__
    )

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

    args = parser.parse_args()
    tasks = jobs(args.mode)

    manifest = [
        {
            "name": name,
            "parameters": kwargs,
        }
        for name, kwargs in tasks
    ]

    import sys

    self_path = Path(__file__)

    hashes = {
        "m5q": hashlib.sha256(
            self_path.read_bytes()
        ).hexdigest(),
        "m5p": hashlib.sha256(
            Path(m5p.__file__).read_bytes()
        ).hexdigest(),
        "m5o": hashlib.sha256(
            Path(m5o.__file__).read_bytes()
        ).hexdigest(),
    }

    if args.resume:
        filename = Path(args.resume).resolve()
        record = json.loads(filename.read_text())

        if (
            record.get("branch") != BRANCH
            or record.get("mode") != args.mode
            or record.get("manifest") != json.loads(
                json.dumps(manifest)
            )
            or record.get("code_sha256") != hashes
        ):
            parser.error(
                "Unsafe resume: code or manifest changed"
            )
    else:
        folder = Path(args.results_dir)
        folder.mkdir(parents=True, exist_ok=True)

        stamp = datetime.now(
            timezone.utc
        ).strftime("%Y%m%dT%H%M%S%fZ")

        filename = folder / (
            f"b17_m5q_translation_{stamp}_"
            f"{args.mode}_bundle.json"
        )

        record = {
            "branch": BRANCH,
            "status": "RUNNING",
            "schema": "antigravity.single_run.v1",
            "mode": args.mode,
            "manifest": manifest,
            "registered": len(tasks),
            "processed": 0,
            "results": {},
            "errors": {},
            "summary": None,
            "code_sha256": hashes,
            "claims": {
                "physical_lift": False,
                "physical_action": False,
                "complete_energy": False,
            },
        }

    def checkpoint():
        tmp = filename.with_name(
            filename.name+".tmp"
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

        os.replace(tmp, filename)

    if not args.resume:
        checkpoint()

    count = 0
    record["status"] = "RUNNING"

    try:
        for number, (name, kw) in enumerate(tasks, 1):
            if name in record["results"]:
                print(
                    f"[{number}/{len(tasks)}] REUSED {name}",
                    flush=True,
                )
                continue

            if (
                args.max_new_cases is not None
                and count >= args.max_new_cases
            ):
                record["status"] = "PARTIAL_NOT_CERTIFIED"
                checkpoint()

                print(
                    "RESUME_BUNDLE:",
                    filename,
                    flush=True,
                )
                return 2

            print(
                f"[{number}/{len(tasks)}] {name}",
                flush=True,
            )

            try:
                value = evaluate(**kw)
                record["results"][name] = value
                record["errors"].pop(name, None)

                terms = value["derivative_terms_j_m"]

                print(
                    "  Earth / craft / common [J/m]:",
                    *[
                        round(terms[k], 9)
                        for k in (
                            "earth_operator_analytic",
                            "craft_earth_fixed_inferred",
                            "common_total",
                        )
                    ],
                    flush=True,
                )
            except Exception:
                record["errors"][name] = (
                    traceback.format_exc()
                )
                print(
                    "FAILED",
                    name,
                    record["errors"][name],
                    flush=True,
                )

            count += 1

            record["processed"] = (
                len(record["results"])
                + len(record["errors"])
            )

            checkpoint()

        record["summary"] = summarize(
            tasks, record["results"]
        )

        required = (
            "Q0_m5p_Earth_derivative_reproduction",
            "Q1_stationary_quadratic_action",
            "Q2_Hellmann_Feynman_resolved",
            "Q3_total_source_enclosure_Earth_partition",
            "Q4_negative_controls",
        )

        passed = (
            not record["errors"]
            and all(
                record["summary"]["gates"][key] == "PASS"
                for key in required
            )
        )

        record["status"] = (
            "COMPLETE_NUMERICAL_ONLY"
            if passed else
            "FAILED_NUMERICAL_CONTROLS"
        )

        checkpoint()

        print(
            "UPLOAD_ONLY:",
            filename,
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

        return 0 if passed else 1

    except KeyboardInterrupt:
        record["status"] = "INTERRUPTED"
        checkpoint()
        print(
            "RESUME_BUNDLE:",
            filename,
            flush=True,
        )
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
