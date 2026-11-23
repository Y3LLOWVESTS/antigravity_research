"""G01-T0/T1: Original R3B Lorentzian loaded-source response.

SCIENTIFIC QUESTION
-------------------
Can finite ideal-shell electric X and magnetic Y source
multipoles change the original R3X1 loaded response toward
outward acceleration throughout the finite neutral torus?

MODEL
-----
Original R3X1 signed static equations, with the original
matter-loading beta frozen.

The source variations are regular interior and decaying
exterior spherical multipoles generated at an ideal shell.

The sources are conserved in the analytic Maxwell sense:
electric modes have no monopole; magnetic modes use
axisymmetric azimuthal surface currents with zero divergence.

LIMITS
------
There is no identified microscopic hidden-charge material,
no varied neutral matter equilibrium, no new common
source/material action, no Einstein metric and no
whole-craft gravitational force.

This is an optimistic source-control diagnostic, not
a device or a physical antigravity survivor.

The old R3B capacity is retained as historical evidence.
Control normalization uses canonical loaded field energy,
not source preparation or complete operating energy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import legval, legder, leggauss
from scipy.linalg import lu_factor, lu_solve
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from antigravity_research.agminer.hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    _solve_loaded,
    _state,
    _direct_compare,
)
from antigravity_research.agminer.hook17_fdual_f_r3c1_validation import (
    _build_baseline_and_prep,
)
from antigravity_research.agminer.hook17_fdual_f_loaded_payload_homotopy import (
    _fields_from_potentials,
    _vectors_to_full_potentials,
)
from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    HBAR_C_EV_M,
    EV_J,
    REFERENCE_PORTAL_SCALE_EV,
)

PINS = {
    "src/antigravity_research/agminer/hook17_fdual_f_global_mirror_prefight.py":
        "aa8f196fcae6a63405181ca62674e22ac67e5da88303759bdd99d25716fa2263",
    "src/antigravity_research/agminer/hook17_fdual_f_r3x1_lorentzian_sign_audit.py":
        "6f1bf0922712a81e860075a71201af49c7870fa18fe2c21e7f576bb46da97531",
    "src/antigravity_research/agminer/hook17_f2_strong_payload_loading_rescue.py":
        "e1296794c25a4d0e4d5634c7e7d543a0b488b8d2a1963afcf7878bea1c1b99e7",
    "results/data/032h17a12d1r3b_hook17_fdual_f_global_mirror_prefight_summary.json":
        "9474b6782104abb5bd8dd5e893137621b30ad96109e3e52c5a01268794810b11",
}

BASELINE = {
    0.075: -46.4060741,
    0.050: -129.67185782242464,
}

TARGET = 9.80665
R_SHELL = 2.0
FIELDS = ("e_rho", "e_z", "b_rho", "b_z")
ELLS = (1, 2, 4, 8, 12)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_parents():
    for name, expected in PINS.items():
        path = ROOT / name
        if (
            not path.is_file()
            or path.is_symlink()
            or sha(path) != expected
        ):
            raise RuntimeError("PARENT_SHA_HOLD: " + name)
    return dict(PINS)


def multipole(field, ell, kind):
    """Regular-inside, decaying-outside ideal shell multipole."""
    rho = np.asarray(field["rho_grid"])
    z = np.asarray(field["z_grid"])
    r = np.hypot(rho, z)
    safe = np.maximum(r, 1e-14)
    mu = np.clip(z / safe, -1.0, 1.0)

    c = np.zeros(ell + 1)
    c[-1] = 1.0

    p = legval(mu, c)

    radial = np.where(
        r <= R_SHELL,
        (r / R_SHELL) ** ell,
        (R_SHELL / safe) ** (ell + 1),
    )

    phi = np.zeros_like(r)
    a = np.zeros_like(r)

    if kind == "X_electric":
        phi = radial * p
    elif kind == "Y_magnetic":
        dp = legval(mu, legder(c))
        a = (
            R_SHELL / (ell * (ell + 1))
            * radial
            * (rho / safe)
            * dp
        )
    else:
        raise ValueError("UNKNOWN_CONTROL")

    return phi, a


def energy_j(field, maps):
    h = float(field["h"])
    rho = np.asarray(field["rho_grid"])
    volume = 2.0 * math.pi * rho * h * h
    f2 = sum(np.square(maps[k]) for k in FIELDS)
    return float(
        0.5 * np.sum(volume * f2) / HBAR_C_EV_M * EV_J
    )


def dot_eb(x, y):
    return (
        x["e_rho"] * y["b_rho"]
        + x["e_z"] * y["b_z"]
    )


def acceleration(field, dot):
    sigma = (
        -2.0
        * HBAR_C_EV_M**2
        * dot
        / REFERENCE_PORTAL_SCALE_EV**4
    )
    return (
        -C_LIGHT_M_S**2
        * np.gradient(
            sigma,
            float(field["h"]),
            axis=0,
            edge_order=2,
        )
    )


def run_grid(h, levels):
    setup = _build_baseline_and_prep(h)
    field = setup["field"]
    prep = setup["prep"]

    payload = np.asarray(field["payload"], dtype=bool)

    if not payload.any():
        raise RuntimeError("EMPTY_PAYLOAD")

    clearance = float(
        np.min(
            np.hypot(
                field["rho_grid"][payload],
                field["z_grid"][payload],
            )
            - R_SHELL
        )
    )

    if clearance < 1.0 - 2.0 * h:
        raise RuntimeError("SHELL_CLEARANCE_GATE")

    original_solution = _solve_loaded(prep, 1.0, 1.0)

    if (
        not original_solution["success"]
        or original_solution["relative_residual"] > 1e-7
    ):
        raise RuntimeError("SIGNED_PARENT_SOLVE_GATE")

    original = _state(setup, original_solution)
    old_acc = float(
        original["minimum_payload_acceleration_m_s2"]
    )

    if not np.isclose(
        old_acc, BASELINE[h], atol=0.15, rtol=0.0
    ):
        raise RuntimeError(
            "R3X1_BASELINE_DRIFT: " + str(old_acc)
        )

    op, oa = _vectors_to_full_potentials(
        prep,
        field,
        setup["phi0"],
        setup["a0"],
        original_solution,
    )

    base_maps = _fields_from_potentials(
        op, oa, field["rho_grid"], h
    )

    base_acc = acceleration(
        field, dot_eb(base_maps, base_maps)
    )[payload]

    if not np.isclose(
        base_acc.min(), old_acc, atol=1e-8, rtol=1e-10
    ):
        raise RuntimeError("BASELINE_RECONSTRUCTION_GATE")

    rp = len(prep["coupling"]["active_phi"])
    ra = len(prep["coupling"]["active_a"])

    reduced = np.eye(rp + ra)
    reduced[:rp, rp:] = prep["c_green_a"]
    reduced[rp:, :rp] = -prep["d_green_phi"]

    # These are the corrected R3X1 Lorentzian signs.
    factorized = lu_factor(reduced)

    def loaded_response(phi, a):
        pv = phi[1:-1, :-1].reshape(-1)
        av = a[1:-1, 1:-1].reshape(-1)

        rhs = np.r_[
            -np.asarray(
                prep["c_active"] @ av
            ).reshape(-1),
            +np.asarray(
                prep["d_active"] @ pv
            ).reshape(-1),
        ]

        y = lu_solve(factorized, rhs)

        dp = np.asarray(
            prep["green_phi"] @ y[:rp]
        ).reshape(-1)

        da = np.asarray(
            prep["green_a"] @ y[rp:]
        ).reshape(-1)

        res_p = (
            prep["operators"]["k_phi"] @ dp
            + prep["coupling"]["c"] @ (av + da)
        )
        res_a = (
            prep["operators"]["k_a"] @ da
            - prep["coupling"]["d"] @ (pv + dp)
        )

        err = max(
            float(np.linalg.norm(res_p)),
            float(np.linalg.norm(res_a)),
        ) / max(1.0, float(np.linalg.norm(rhs)))

        if not np.isfinite(err) or err > 2e-6:
            raise RuntimeError(
                "SIGNED_RESPONSE_RESIDUAL: " + str(err)
            )

        solution = {
            "delta_phi_vec": dp,
            "delta_a_vec": da,
        }

        total_phi, total_a = _vectors_to_full_potentials(
            prep, field, phi, a, solution
        )

        maps = _fields_from_potentials(
            total_phi,
            total_a,
            field["rho_grid"],
            h,
        )

        return maps, err

    direct = (
        _direct_compare(
            setup, original_solution, 1.0, 1.0
        )
        if h == 0.075
        else None
    )

    if direct is not None and not direct["pass"]:
        raise RuntimeError("DIRECT_SPARSE_PARENT_GATE")

    basis = []
    metadata = []

    for ell in ELLS:
        for kind in ("X_electric", "Y_magnetic"):
            phi, a = multipole(field, ell, kind)
            maps, err = loaded_response(phi, a)

            e = energy_j(field, maps)

            if not np.isfinite(e) or e <= 0.0:
                raise RuntimeError("MODE_ENERGY_GATE")

            normalization = 1.0 / math.sqrt(e)

            maps = {
                k: v * normalization
                for k, v in maps.items()
            }

            basis.append(maps)

            metadata.append({
                "ell": ell,
                "kind": kind,
                "raw_loaded_energy_j": e,
                "normalization_to_one_loaded_field_j":
                    normalization,
                "signed_static_residual": err,
                "physical_Y_source_identified": False,
            })

    # Derivative of acceleration with respect to each
    # ideal shell control at the full-loaded baseline.
    A = np.column_stack([
        acceleration(
            field,
            dot_eb(base_maps, b)
            + dot_eb(b, base_maps),
        )[payload]
        for b in basis
    ])

    singular = np.linalg.svd(A, compute_uv=False)
    rank = int(np.sum(
        singular
        > 1e-8 * max(float(singular[0]), 1e-300)
    ))

    def evaluate(u):
        # Exact bilinear acceleration within this
        # frozen-beta linear field-response model.
        combined = {
            k: (
                base_maps[k]
                + sum(
                    float(u[j]) * basis[j][k]
                    for j in range(len(basis))
                )
            )
            for k in FIELDS
        }

        minimum = float(
            np.min(
                acceleration(
                    field,
                    dot_eb(combined, combined),
                )[payload]
            )
        )

        return minimum, energy_j(field, combined)

    rows = []

    for bound in levels:
        # Optimistic linearized maximin:
        # maximize t, subject to a0 + A*u >= t.
        inequalities = np.column_stack((
            -A,
            np.ones(len(base_acc)),
        ))

        objective = np.r_[
            np.zeros(len(basis)),
            -1.0,
        ]

        bounds = (
            [(-bound, bound)] * len(basis)
            + [(None, None)]
        )

        opt = linprog(
            objective,
            A_ub=inequalities,
            b_ub=base_acc,
            bounds=bounds,
            method="highs",
            options={"time_limit": 90.0},
        )

        if not opt.success:
            rows.append({
                "mode_bound": bound,
                "success": False,
                "linear_program_status": str(opt.message),
            })
            continue

        u = opt.x[:-1]
        minimum, e = evaluate(u)
        reversed_minimum, reversed_e = evaluate(-u)

        delta = 1e-4
        plus, _ = evaluate(delta * u)
        minus, _ = evaluate(-delta * u)

        rows.append({
            "mode_bound": bound,
            "success": True,
            "controls": u.tolist(),
            "linearized_min_m_s2": float(opt.x[-1]),
            "full_bilinear_min_m_s2": minimum,
            "full_bilinear_field_energy_j": e,
            "reverse_direction_min_m_s2":
                reversed_minimum,
            "reverse_direction_field_energy_j":
                reversed_e,
            "directional_min_finite_difference_slope":
                (plus - minus) / (2.0 * delta),
            "meets_1g_full_bilinear":
                bool(minimum >= TARGET),
            "source_cost_j": None,
            "physical_source_gate":
                "HOLD_UNIDENTIFIED_XY_SHELL_MATTER",
            "physical_gravity_gate": "NOT_EVALUATED",
        })

    nodes, weights = leggauss(80)
    flux_errors = []

    for ell in ELLS:
        c = np.zeros(ell + 1)
        c[-1] = 1.0
        flux_errors.append(
            abs(float(
                np.dot(weights, legval(nodes, c))
            ))
        )

    return {
        "h_m": h,
        "payload_count": int(payload.sum()),
        "source_shell_radius_m": R_SHELL,
        "sampled_min_shell_clearance_m": clearance,
        "original_loaded_min_m_s2": old_acc,
        "original_loaded_energy_j":
            float(original["canonical_field_energy_j"]),
        "original_relative_residual":
            float(original_solution["relative_residual"]),
        "lorentzian_coupling_signs": [1, -1],
        "direct_sparse_parent_validation": direct,
        "no_electric_monopole_quadrature_max_error":
            max(flux_errors),
        "magnetic_monopole":
            "ANALYTICALLY_ABSENT_ELL_GE_1",
        "shell_current_divergence":
            "ZERO_FOR_AXISYMMETRIC_AZIMUTHAL_CURRENT",
        "source_microphysics": "NOT_IDENTIFIED",
        "control_modes": metadata,
        "loaded_response_singular_values_m_s2_per_sqrt_j":
            singular.tolist(),
        "loaded_response_rank_at_rel_1e_8": rank,
        "worst_point_base_sensitivity_m_s2_per_sqrt_j":
            A[int(np.argmin(base_acc))].tolist(),
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--fine", action="store_true")
    args = parser.parse_args()

    parents = check_parents()
    levels = (0.0, 0.25, 0.5, 1.0, 2.0)

    grids = [run_grid(0.075, levels)]

    if args.fine:
        grids.append(run_grid(0.050, levels))

    document = {
        "experiment": "G01-T0T1",
        "model":
            "ORIGINAL_R3X1_SIGNED_FROZEN_BETA_IDEAL_SHELL_CONTROLS",
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "parents": parents,
        "source_sha256": sha(Path(__file__)),
        "grids": grids,
        "energy_cap_j": 1.0e7,
        "target_acceleration_m_s2": TARGET,
        "physical_qualified_survivors": 0,
        "physical_research_maturity_percent_not_updated": 37,
        "source_action_identified": False,
        "neutral_matter_equilibrium_varied": False,
        "earth_craft_Einstein_force_derived": False,
        "full_Lorentzian_health": False,
        "operating_energy_certified": False,
        "loaded_response":
            "LINEARIZED_FROZEN_BETA_SOURCE_INPUT_WITH_EXACT_BILINEAR_ACC",
        "statement":
            "Ideal shell-source response, not physical gravitational lift",
        "decision": "SOURCE_MICROPHYSICS_AND_SI_COST_HOLD",
    }

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)

    data = (
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        + "\n"
    ).encode()

    (out / "science.json").write_bytes(data)
    science_sha = hashlib.sha256(data).hexdigest()

    (out / "science.json.sha256").write_text(
        science_sha + "  science.json\n"
    )

    for g in grids:
        print(
            "GRID",
            g["h_m"],
            "BASELINE",
            g["original_loaded_min_m_s2"],
            "CLEARANCE",
            g["sampled_min_shell_clearance_m"],
            flush=True,
        )

        print(
            "RESPONSE_RANK",
            g["loaded_response_rank_at_rel_1e_8"],
            flush=True,
        )

        for row in g["rows"]:
            print(
                "BOUND", row["mode_bound"],
                "LINEAR", row.get("linearized_min_m_s2"),
                "BILINEAR", row.get("full_bilinear_min_m_s2"),
                "FIELD_J",
                row.get("full_bilinear_field_energy_j"),
                flush=True,
            )

    print(
        "G01_T_STATUS=IDEAL_SHELL_RESPONSE_ONLY_SOURCE_NOT_IDENTIFIED"
    )
    print("OUTPUT", out)
    print("SCIENCE_SHA256", science_sha)


if __name__ == "__main__":
    main()
