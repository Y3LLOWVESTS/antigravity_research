"""B17-M5P: exterior-boundary closure for the artificial Earth response.

M5O's finite-box zero-Dirichlet problem showed significant boundary
dependence. M5P compares three fixed-box boundary treatments:
zero Dirichlet, first-order local dipole Robin, and exact leading-
dipole neighbor-to-boundary trace extrapolation.

The stationary M5L quadratic functional, artificial M5I continuum
source, M5O material response, and source normalization are unchanged.

At large radius the leading source-free modes are approximated by
    phi   ~ z   / (rho**2+z**2)**(3/2)
    A_phi ~ rho / (rho**2+z**2)**(3/2)

The boundary conditions are approximate: neither one is a complete
nonlocal exterior Dirichlet-to-Neumann operator. Exact dipole trace
means exact for these analytic dipole functions, not for arbitrary
solutions containing higher multipoles.

Numerical results are artificial reduced-action derivatives in J/m.
They are not physical gravitational force, spacecraft lift, source
work, full-system Noether momentum transfer, or complete energy.
006D remains the strongest conservative GR anchor.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

from . import hook17_r3b_m5o_fixed_box as m5o
from .hook17_fdual_f_loaded_payload_homotopy import (
    _build_elliptic_operators,
)
from .hook17_r3b_m5m_translation_consistency import (
    carrier_action_conversion_j_per_native,
)

BRANCH = "032H17A12D1R3X3B17-ALPHA1R11-M5P-EXTERIOR"

BOUNDS = {
    "compact": (7.0, -6.0, 8.0),
    "original": (12.0, -10.0, 13.0),
    "extended": (15.0, -12.0, 15.0),
    "outer21": (21.0, -16.0, 19.0),
    "outer24": (24.0, -18.0, 21.0),
    "outer30": (30.0, -22.0, 25.0),
}


def dipole_robin_alpha(rho, z, side, sector):
    """Return minus the outward logarithmic derivative of a dipole."""
    if sector not in ("phi", "a"):
        raise ValueError("Unknown carrier sector")
    if side not in ("r", "z"):
        raise ValueError("Unknown boundary side")

    radius2 = rho * rho + z * z
    if radius2 <= 0:
        raise ValueError("Dipole closure at origin")

    if side == "r":
        if rho <= 0:
            raise ValueError("Invalid radial boundary")
        alpha = 3.0 * rho / radius2
        if sector == "a":
            alpha -= 1.0 / rho
    else:
        if abs(z) <= 0:
            raise ValueError("Invalid axial boundary")
        alpha = 3.0 * abs(z) / radius2
        if sector == "phi":
            alpha -= 1.0 / abs(z)

    return alpha


def dipole_trace_scale(
    r_inner, z_inner, r_boundary, z_boundary, sector
):
    """Exact boundary/inner ratio for the specified l=1 dipole mode."""
    ri2 = r_inner * r_inner + z_inner * z_inner
    rb2 = r_boundary * r_boundary + z_boundary * z_boundary

    if ri2 <= 0 or rb2 <= 0:
        raise ValueError("Invalid dipole trace radius")

    scale = (ri2 / rb2) ** 1.5

    if sector == "phi":
        if z_boundary != z_inner:
            if z_inner == 0:
                raise ValueError("Scalar dipole trace crosses equator")
            scale *= z_boundary / z_inner
    elif sector == "a":
        if r_inner == 0:
            raise ValueError("Vector trace at axis")
        scale *= r_boundary / r_inner
    else:
        raise ValueError("Unknown carrier sector")

    return scale


def robin_operators(field, closure):
    """Change only boundary-adjacent elliptic diagonal entries.

    The local Robin elimination is
        u_boundary = u_inner / (1 + h*alpha)

    The dipole-trace elimination substitutes the exact dipole
    boundary/inner ratio instead. Both retain the weighted Hessian's
    symmetry because the elimination changes only diagonal entries.

    The Robin elimination is first order and not a transparent
    boundary condition for general higher-multipole fields.
    """
    if closure not in (
        "dirichlet", "dipole_robin", "dipole_trace"
    ):
        raise ValueError("Unknown outer boundary treatment")

    rhos = field["rhos"]
    zs = field["zs"]
    h = field["h"]

    ops = _build_elliptic_operators(rhos, zs, h)

    audit = {
        "outer_closure": closure,
        "accuracy": (
            "FIRST_ORDER_LOCAL_ROBIN"
            if closure == "dipole_robin"
            else "EXACT_LOCAL_DIPOLE_TRACE"
        ),
        "alpha_min": None,
        "alpha_max": None,
        "elimination_min_denominator": None,
        "changes_only_diagonal": True,
    }

    if closure == "dirichlet":
        audit["accuracy"] = "ZERO_DIRICHLET"
        return ops, audit

    nz = ops["nz_inner"]
    rmax = float(rhos[-1])
    zbottom = float(zs[0])
    ztop = float(zs[-1])
    alpha_values = []
    denominators = []

    for sector, nr, key in (
        ("phi", ops["nr_phi"], "k_phi"),
        ("a", ops["nr_a"], "k_a"),
    ):
        indexes = []
        values = []

        last = nr - 1
        r_inner = float(
            rhos[last if sector == "phi" else last + 1]
        )

        radial_coefficient = (
            -1.0 / h**2 - 1.0 / (2.0 * r_inner * h)
        )

        for j in range(nz):
            z = float(zs[j + 1])
            alpha = dipole_robin_alpha(
                rmax, z, "r", sector
            )
            denominator = 1.0 + h * alpha

            if denominator <= 0.1:
                raise ArithmeticError(
                    "Unsafe radial boundary elimination"
                )

            if closure == "dipole_robin":
                scale = 1.0 / denominator
            else:
                scale = dipole_trace_scale(
                    r_inner, z, rmax, z, sector
                )

            indexes.append(j * nr + last)
            values.append(radial_coefficient * scale)
            alpha_values.append(alpha)
            denominators.append(denominator)

        for i in range(nr):
            rho = float(
                rhos[i if sector == "phi" else i + 1]
            )

            for j, zface in (
                (0, zbottom),
                (nz - 1, ztop),
            ):
                alpha = dipole_robin_alpha(
                    rho, zface, "z", sector
                )
                denominator = 1.0 + h * alpha

                if denominator <= 0.1:
                    raise ArithmeticError(
                        "Unsafe axial boundary elimination"
                    )

                z_inner = float(
                    zs[1 if j == 0 else -2]
                )

                if closure == "dipole_robin":
                    scale = 1.0 / denominator
                else:
                    scale = dipole_trace_scale(
                        rho,
                        z_inner,
                        rho,
                        zface,
                        sector,
                    )

                indexes.append(j * nr + i)
                values.append(-scale / h**2)
                alpha_values.append(alpha)
                denominators.append(denominator)

        diagonal = np.bincount(
            indexes,
            weights=values,
            minlength=nr * nz,
        )

        ops[key] = (
            ops[key] + diags(diagonal, format="csr")
        ).tocsr()

    audit["alpha_min"] = float(min(alpha_values))
    audit["alpha_max"] = float(max(alpha_values))
    audit["elimination_min_denominator"] = float(
        min(denominators)
    )

    return ops, audit


def exterior_trace_probe(field, ops, u, targets):
    """Audit the smaller-box trace against a larger-domain solution.

    The relative L2 norm uses cylindrical surface weights. It is a
    boundary-value diagnostic, not physical stress or radiated energy.
    """
    h = float(field["h"])
    zs = field["zs"]
    nrp = ops["nr_phi"]
    nra = ops["nr_a"]
    nz = ops["nz_inner"]

    phi = u[:nrp * nz].reshape(nz, nrp)
    vector = u[nrp * nz:].reshape(nz, nra)

    errors = {}

    for target in targets:
        if target not in BOUNDS:
            raise ValueError("Unknown trace-probe box")

        rmax, zmin, zmax = BOUNDS[target]

        if (
            rmax >= field["rhos"][-1]
            or zmin <= zs[0]
            or zmax >= zs[-1]
        ):
            raise ValueError(
                "Reference domain does not contain probe box"
            )

        ir = round(rmax / h)
        jlo = round((zmin - zs[0]) / h)
        jhi = round((zmax - zs[0]) / h)

        if max(
            abs(ir * h - rmax),
            abs(zs[jlo] - zmin),
            abs(zs[jhi] - zmax),
        ) > 1e-8:
            raise ValueError(
                "Trace-probe surfaces are not grid-aligned"
            )

        section = {}

        for sector, F in (
            ("phi", phi),
            ("a", vector),
        ):
            for kind in (
                "dipole_trace",
                "dipole_robin",
            ):
                numerator = 0.0
                denominator = 0.0

                # Radial cylindrical surface.
                for j in range(jlo + 1, jhi):
                    z = float(zs[j])

                    idx_boundary = (
                        ir if sector == "phi" else ir - 1
                    )
                    idx_inner = (
                        ir - 1 if sector == "phi" else ir - 2
                    )

                    actual = float(F[j - 1, idx_boundary])
                    alpha = dipole_robin_alpha(
                        rmax, z, "r", sector
                    )

                    if kind == "dipole_trace":
                        scale = dipole_trace_scale(
                            rmax - h, z, rmax, z, sector
                        )
                    else:
                        scale = 1.0 / (1.0 + h * alpha)

                    predicted = (
                        scale * float(F[j - 1, idx_inner])
                    )
                    weight = rmax * h

                    numerator += (
                        weight * (actual - predicted)**2
                    )
                    denominator += weight * actual**2

                # Upper and lower planar surfaces.
                for j, zface in (
                    (jlo, zmin),
                    (jhi, zmax),
                ):
                    jinner = (
                        j + 1 if j == jlo else j - 1
                    )

                    first_i = (
                        0 if sector == "phi" else 1
                    )

                    for i in range(first_i, ir):
                        rho = float(i * h)
                        idx = (
                            i if sector == "phi" else i - 1
                        )

                        actual = float(F[j - 1, idx])
                        alpha = dipole_robin_alpha(
                            rho, zface, "z", sector
                        )

                        if kind == "dipole_trace":
                            scale = dipole_trace_scale(
                                rho,
                                float(zs[jinner]),
                                rho,
                                zface,
                                sector,
                            )
                        else:
                            scale = 1.0 / (
                                1.0 + h * alpha
                            )

                        predicted = (
                            scale * float(F[jinner - 1, idx])
                        )
                        weight = max(rho, h / 8.0) * h

                        numerator += (
                            weight * (actual - predicted)**2
                        )
                        denominator += weight * actual**2

                key = (
                    sector + "_" + kind
                    + "_weighted_relative_l2"
                )

                section[key] = (
                    float(math.sqrt(
                        numerator / denominator
                    ))
                    if denominator > 0
                    else None
                )

        errors[target] = section

    return errors


def evaluate(
    h=0.2,
    domain=BOUNDS["compact"],
    closure="dipole_robin",
    width=0.5,
    profile="c2",
    step=0.0001,
    earth_present=True,
    zero_source=False,
    order=6,
    do_resolve=False,
    trace_targets=(),
):
    """Evaluate one unchanged-source stationary Earth response."""
    field = m5o.mesh(h, domain)
    ops, boundary = robin_operators(field, closure)

    source, source_audit = m5o.source_rhs(
        field, ops, 0.0, order=order
    )

    if zero_source:
        source = np.zeros_like(source)

    beta, dbeta, material_audit = m5o.material(
        field,
        0.0,
        0.0,
        width,
        profile,
        earth_present,
    )

    A, H, W, asymmetry = m5o.weighted(
        field, ops, beta
    )

    u = spsolve(A, source)
    rhs = W * source

    trace_audit = (
        exterior_trace_probe(
            field, ops, u, trace_targets
        )
        if trace_targets
        else None
    )

    residual = float(
        np.linalg.norm(A @ u - source)
        / max(np.linalg.norm(source), 1.0)
    )

    stationary = float(
        np.linalg.norm(H @ u - rhs)
        / max(np.linalg.norm(rhs), 1.0)
    )

    conversion = carrier_action_conversion_j_per_native(h)

    Hzero = m5o.weighted(
        field, ops, np.zeros_like(beta)
    )[1]

    Hprime = (
        m5o.weighted(field, ops, dbeta)[1]
        - Hzero
    )

    derivative = float(
        0.5 * conversion * u @ (Hprime @ u)
    )

    beta_plus = m5o.material(
        field, 0.0, step, width, profile, earth_present
    )[0]

    beta_minus = m5o.material(
        field, 0.0, -step, width, profile, earth_present
    )[0]

    Aplus, Hplus, Wplus, _ = m5o.weighted(
        field, ops, beta_plus
    )
    Aminus, Hminus, Wminus, _ = m5o.weighted(
        field, ops, beta_minus
    )

    if not (
        np.array_equal(W, Wplus)
        and np.array_equal(W, Wminus)
    ):
        raise ArithmeticError(
            "Material-dependent source pairing"
        )

    hfinite = float(
        0.5 * conversion
        * u @ ((Hplus - Hminus) @ u)
        / (2.0 * step)
    )

    resolved = None

    if do_resolve:
        uplus = spsolve(Aplus, source)
        uminus = spsolve(Aminus, source)

        qplus = -0.5 * conversion * (
            uplus @ rhs
        )
        qminus = -0.5 * conversion * (
            uminus @ rhs
        )
        resolved = float(
            (qplus - qminus) / (2.0 * step)
        )

    return {
        "branch": BRANCH,
        "h_m": h,
        "domain_m": list(domain),
        "closure": closure,
        "interface_profile": profile,
        "interface_width_m": width,
        "earth_step_m": step,
        "source": source_audit,
        "material": material_audit,
        "boundary": boundary,
        "external_trace_probe": trace_audit,
        "derivative_analytic_j_m": derivative,
        "derivative_H_finite_difference_j_m": hfinite,
        "derivative_resolved_j_m": resolved,
        "derivative_H_difference_error_j_m": (
            hfinite - derivative
        ),
        "derivative_resolve_difference_error_j_m": (
            None if resolved is None
            else resolved - derivative
        ),
        "on_shell_q_j": float(
            -0.5 * conversion * u @ rhs
        ),
        "operator_residual": residual,
        "stationarity_residual": stationary,
        "weighted_operator_asymmetry": float(asymmetry),
        "zero_source": zero_source,
        "earth_present": earth_present,
        "artificial_source_amplitude": m5o.AMPLITUDE,
        "physical_force_certified": False,
        "whole_spacecraft_lift_certified": False,
        "complete_operating_energy_certified": False,
        "006d_replaced": False,
    }


def _jobs(mode):
    """Pre-register the controlled, targeted experiment matrix."""
    if mode not in ("quick", "full"):
        raise ValueError("Invalid M5P run mode")

    jobs = []
    names = set()

    def add(name, **kwargs):
        if name in names:
            raise AssertionError("Duplicate case: " + name)
        names.add(name)
        jobs.append((name, kwargs))

    add(
        "dirichlet_reference_compact_0.2",
        h=0.2,
        domain=BOUNDS["compact"],
        closure="dirichlet",
        do_resolve=True,
    )
    add(
        "dirichlet_reference_original_0.1",
        h=0.1,
        domain=BOUNDS["original"],
        closure="dirichlet",
        do_resolve=True,
    )

    for label in ("compact", "original", "extended"):
        meshes = (
            (0.2, 0.1)
            if mode == "quick"
            else (0.2, 0.1, 0.0625)
        )

        for h in meshes:
            for closure in (
                "dirichlet",
                "dipole_robin",
                "dipole_trace",
            ):
                add(
                    f"{label}_{h}_{closure}",
                    h=h,
                    domain=BOUNDS[label],
                    closure=closure,
                )

    for h in (0.2, 0.1):
        for closure in (
            "dirichlet",
            "dipole_robin",
            "dipole_trace",
        ):
            add(
                f"outer21_{h}_{closure}",
                h=h,
                domain=BOUNDS["outer21"],
                closure=closure,
            )

    if mode == "full":
        for label in ("outer24", "outer30"):
            for h in (0.2, 0.1):
                add(
                    f"{label}_{h}_dipole_trace",
                    h=h,
                    domain=BOUNDS[label],
                    closure="dipole_trace",
                )

        for h in (0.2, 0.1):
            add(
                f"outer30_{h}_dirichlet",
                h=h,
                domain=BOUNDS["outer30"],
                closure="dirichlet",
                trace_targets=("compact", "original"),
            )

        for label in (
            "compact",
            "original",
            "extended",
        ):
            add(
                f"{label}_0.05_dipole_trace",
                h=0.05,
                domain=BOUNDS[label],
                closure="dipole_trace",
            )
    else:
        add(
            "outer30_0.2_dirichlet",
            h=0.2,
            domain=BOUNDS["outer30"],
            closure="dirichlet",
            trace_targets=("compact", "original"),
        )

    for profile, width in (
        ("c1", 0.25),
        ("c2", 0.5),
    ):
        add(
            f"model_{profile}_{width}",
            h=0.125,
            domain=BOUNDS["compact"],
            width=width,
            profile=profile,
            closure="dipole_robin",
        )

    add(
        "no_earth",
        h=0.25,
        domain=BOUNDS["compact"],
        closure="dipole_robin",
        earth_present=False,
    )
    add(
        "zero_source",
        h=0.25,
        domain=BOUNDS["compact"],
        closure="dipole_robin",
        zero_source=True,
    )

    return jobs


def _diagnose(jobs, results):
    """Fail-closed numerical gates, without physical promotion."""
    summary = {
        "branch": BRANCH,
        "registered": len(jobs),
        "completed": len(results),
        "reproducibility": {},
        "comparison": {},
        "gates": {},
    }
    gates = summary["gates"]

    references = {
        "dirichlet_reference_compact_0.2":
            -11.712738348790097,
        "dirichlet_reference_original_0.1":
            -11.586961767542604,
    }

    reproduction_ok = True

    for name, reference in references.items():
        actual = results.get(
            name, {}
        ).get("derivative_analytic_j_m")

        difference = (
            None if actual is None
            else actual - reference
        )

        summary["reproducibility"][name] = {
            "measured": actual,
            "difference_j_m": difference,
        }

        reproduction_ok &= (
            difference is not None
            and abs(difference) < 1e-8
        )

    complete = len(results) == len(jobs)

    gates["P0_m5o_dirichlet_reproduction"] = (
        "PASS"
        if complete and reproduction_ok
        else "FAIL_OR_INCOMPLETE"
    )

    action_ok = complete
    source_ok = complete

    for result in results.values():
        d = result["derivative_analytic_j_m"]
        tolerance = max(
            0.02, 0.005 * abs(d)
        )

        action_ok &= (
            result["operator_residual"] < 1e-8
            and result["stationarity_residual"] < 1e-8
            and result["weighted_operator_asymmetry"] < 1e-10
            and abs(
                result["derivative_H_difference_error_j_m"]
            ) < tolerance
            and (
                result["derivative_resolve_difference_error_j_m"]
                is None
                or abs(
                    result[
                        "derivative_resolve_difference_error_j_m"
                    ]
                ) < tolerance
            )
        )

        src = result["source"]
        moments = src["reference_moments"]

        e_error = abs(
            src["electric_dipole_moment"]
            - moments["electric_dipole_z_integral"]
        ) / max(
            abs(moments["electric_dipole_z_integral"]),
            1e-30,
        )

        m_error = abs(
            src["magnetic_dipole_moment"]
            - moments["magnetic_dipole_z_integral"]
        ) / max(
            abs(moments["magnetic_dipole_z_integral"]),
            1e-30,
        )

        source_ok &= max(
            e_error,
            m_error,
            src["net_charge_after_projection_rel"],
            src["charge_projection_fraction"],
        ) < 1e-3

    gates["P1_stationarity_and_derivative"] = (
        "PASS" if action_ok else "FAIL_OR_INCOMPLETE"
    )
    gates["P1a_source_moments"] = (
        "PASS" if source_ok else "FAIL_OR_INCOMPLETE"
    )

    zero_earth = results.get(
        "no_earth", {}
    ).get("derivative_analytic_j_m")

    zero_source = results.get(
        "zero_source", {}
    ).get("derivative_analytic_j_m")

    gates["P2_negative_controls"] = (
        "PASS"
        if (
            zero_earth is not None
            and zero_source is not None
            and abs(zero_earth) < 1e-10
            and abs(zero_source) < 1e-10
        )
        else "FAIL_OR_INCOMPLETE"
    )

    spreads = {}
    ratios = {}

    for h in (0.2, 0.1, 0.0625, 0.05):
        for closure in (
            "dirichlet",
            "dipole_robin",
            "dipole_trace",
        ):
            values = []

            for label in (
                "compact",
                "original",
                "extended",
            ):
                name = f"{label}_{h}_{closure}"

                if name in results:
                    values.append(
                        results[name]["derivative_analytic_j_m"]
                    )

            if len(values) == 3:
                spreads[f"{h}_{closure}"] = float(
                    max(values) - min(values)
                )

        before = spreads.get(
            f"{h}_dirichlet"
        )
        after = spreads.get(
            f"{h}_dipole_trace"
        )

        if (
            before is not None
            and after is not None
            and after > 0
        ):
            ratios[str(h)] = float(
                before / after
            )

    summary["cross_box_spreads_j_m"] = spreads
    summary["dirichlet_to_trace_spread_reduction"] = ratios

    gates["P3_domain_sensitivity_reduced"] = (
        "PASS_NUMERICAL_DIAGNOSTIC_ONLY"
        if all(
            ratios.get(str(h), 0.0) > 50.0
            for h in (0.2, 0.1)
        )
        else "FAIL_OR_INCOMPLETE"
    )

    fits = {}

    for label in (
        "compact",
        "original",
        "extended",
    ):
        names = [
            f"{label}_0.1_dipole_trace",
            f"{label}_0.0625_dipole_trace",
            f"{label}_0.05_dipole_trace",
        ]

        if all(name in results for name in names):
            hs = np.array(
                [0.1, 0.0625, 0.05]
            )
            ys = np.array([
                results[name]["derivative_analytic_j_m"]
                for name in names
            ])

            coeff = np.polyfit(
                hs**2, ys, 1
            )

            fits[label] = {
                "assumed_order": 2,
                "candidate_extrapolation_j_m": float(
                    coeff[1]
                ),
                "max_fit_residual_j_m": float(
                    np.max(
                        np.abs(
                            ys - np.polyval(coeff, hs**2)
                        )
                    )
                ),
                "certified": False,
                "physical_force": False,
            }

    summary["conditional_h_squared_extrapolations"] = fits

    if len(fits) == 3:
        candidates = [
            value["candidate_extrapolation_j_m"]
            for value in fits.values()
        ]

        summary[
            "conditional_cross_box_extrapolation_spread_j_m"
        ] = max(candidates) - min(candidates)
    else:
        summary[
            "conditional_cross_box_extrapolation_spread_j_m"
        ] = None

    gates["P3_mesh_domain_joint"] = (
        "YELLOW_NOT_PROVEN"
    )

    probes = {
        name: result["external_trace_probe"]
        for name, result in results.items()
        if result["external_trace_probe"] is not None
    }

    summary["reference_trace_probes"] = probes

    trace_errors = [
        value
        for probe in probes.values()
        for target in probe.values()
        for key, value in target.items()
        if "dipole_trace" in key
        and value is not None
    ]

    max_trace = (
        max(trace_errors)
        if trace_errors
        else None
    )

    summary["reference_trace_max_relative_l2"] = max_trace

    gates["P4a_exterior_trace_reference"] = (
        "PASS_NUMERICAL_DIAGNOSTIC_ONLY"
        if max_trace is not None and max_trace < 0.03
        else "FAIL_OR_INCOMPLETE"
    )

    gates["P4_exterior_boundary"] = (
        "YELLOW_LOCAL_ASYMPTOTIC_ONLY"
    )
    gates["P5_material_profile"] = (
        "YELLOW_PRESCRIBED_MODEL"
    )
    gates["P6_physical_action"] = (
        "NOT_ESTABLISHED"
    )

    for h in (0.2, 0.1, 0.0625, 0.05):
        values = {}

        for label in BOUNDS:
            for closure in (
                "dirichlet",
                "dipole_robin",
                "dipole_trace",
            ):
                name = f"{label}_{h}_{closure}"

                if name in results:
                    values[f"{label}:{closure}"] = (
                        results[name][
                            "derivative_analytic_j_m"
                        ]
                    )

        if values:
            summary["comparison"][str(h)] = values

    summary["complete_device_energy_j"] = None
    summary["continuum_force_certified"] = False
    summary["physical_lift_certified"] = False
    summary["006d_replaced"] = False

    return summary


def main():
    """Write one checkpointed JSON, with provenance-checked resume."""
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
    parser.add_argument(
        "--resume",
        default=None,
    )
    parser.add_argument(
        "--max-new-cases",
        type=int,
        default=None,
    )

    args = parser.parse_args()

    if (
        args.max_new_cases is not None
        and args.max_new_cases < 1
    ):
        parser.error(
            "--max-new-cases must be a positive integer"
        )

    jobs = _jobs(args.mode)
    manifest = [
        {
            "name": name,
            "parameters": kwargs,
        }
        for name, kwargs in jobs
    ]

    own_hash = hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()

    upstream_hash = hashlib.sha256(
        Path(m5o.__file__).read_bytes()
    ).hexdigest()

    if args.resume:
        filename = Path(args.resume).resolve()

        if not filename.is_file():
            parser.error("Resume bundle not found")

        record = json.loads(
            filename.read_text(encoding="utf-8")
        )

        if (
            record.get("branch") != BRANCH
            or record.get("mode") != args.mode
            or record.get("source_code_sha256") != own_hash
            or record.get("m5o_source_sha256") != upstream_hash
            or record.get("manifest") != json.loads(
                json.dumps(manifest)
            )
        ):
            parser.error(
                "Resume rejected: code, mode, or manifest changed"
            )
    else:
        folder = Path(args.results_dir)
        folder.mkdir(parents=True, exist_ok=True)

        stamp = datetime.now(timezone.utc).strftime(
            "%Y%m%dT%H%M%S%fZ"
        )

        filename = folder / (
            f"b17_m5p_exterior_{stamp}_{args.mode}_bundle.json"
        )

        record = {
            "schema": "antigravity.single_run.v1",
            "branch": BRANCH,
            "status": "RUNNING",
            "mode": args.mode,
            "manifest": manifest,
            "registered": len(jobs),
            "processed": 0,
            "results": {},
            "errors": {},
            "summary": None,
            "source_code_sha256": own_hash,
            "m5o_source_sha256": upstream_hash,
            "physical_claims": {
                "force": False,
                "lift": False,
                "complete_energy": False,
            },
        }

    def checkpoint():
        temporary = filename.with_name(
            filename.name + ".tmp"
        )

        with temporary.open(
            "w", encoding="utf-8"
        ) as stream:
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

        os.replace(temporary, filename)

    if not args.resume:
        checkpoint()

    record["status"] = "RUNNING"
    new_count = 0

    try:
        for number, (name, kwargs) in enumerate(jobs, 1):
            if name in record["results"]:
                print(
                    f"[{number}/{len(jobs)}] REUSED {name}",
                    flush=True,
                )
                continue

            if (
                args.max_new_cases is not None
                and new_count >= args.max_new_cases
            ):
                record["status"] = (
                    "PARTIAL_CHECKPOINT_NOT_CERTIFIED"
                )
                checkpoint()

                print(
                    "PARTIAL_BUNDLE_RESUME_WITH:",
                    filename,
                    flush=True,
                )
                return 2

            print(
                f"[{number}/{len(jobs)}] {name}",
                flush=True,
            )

            try:
                value = evaluate(**kwargs)
                record["results"][name] = value
                record["errors"].pop(name, None)

                print(
                    "  Artificial derivative [J/m]:",
                    value["derivative_analytic_j_m"],
                    flush=True,
                )

            except Exception:
                import traceback

                record["errors"][name] = (
                    traceback.format_exc()
                )
                print(
                    "FAILED:",
                    record["errors"][name],
                    flush=True,
                )

            record["processed"] = (
                len(record["results"])
                + len(record["errors"])
            )
            new_count += 1
            checkpoint()

        record["summary"] = _diagnose(
            jobs, record["results"]
        )

        required = (
            "P0_m5o_dirichlet_reproduction",
            "P1_stationarity_and_derivative",
            "P1a_source_moments",
            "P2_negative_controls",
            "P3_domain_sensitivity_reduced",
            "P4a_exterior_trace_reference",
        )

        numerical_pass = all(
            str(
                record["summary"]["gates"].get(
                    gate, ""
                )
            ).startswith("PASS")
            for gate in required
        )

        record["status"] = (
            "COMPLETE_NUMERICAL_ONLY"
            if not record["errors"] and numerical_pass
            else "FAILED_NUMERICAL_CONTROLS"
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

        return int(
            record["status"] != "COMPLETE_NUMERICAL_ONLY"
        )

    except KeyboardInterrupt:
        record["status"] = "INTERRUPTED"
        checkpoint()

        print(
            "INTERRUPTED_BUNDLE_RESUME_WITH:",
            filename,
            flush=True,
        )
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
