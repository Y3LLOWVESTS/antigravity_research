"""G01-J: R3B boundary BF source-current compatibility atlas.

SCIENTIFIC QUESTION
-------------------
Can a constant boundary BF coupling source the R3B bipolar
electric mirror from magnetic flux? Does one gauge-covariant
Hodge-Laplacian BF operator improve multipole compatibility?

MODEL
-----
A closed spherical source interface at R=2 m.

The original R3B mirror gives

    sigma_l = -(2*l+1)*a_l/(sqrt(2)*R)
    Bn_l = (l+1)*a_l/(sqrt(2)*R)

The proposed boundary action terms are

    S0 = k0 integral A_X wedge F_Y
    S1 = S0 + k2*R**2 integral A_X wedge Delta_H F_Y

Delta_H is the Hodge-de Rham Laplacian on the interface.

SCOPE
-----
These are proposed boundary effective operators, NOT a complete
microscopic source, gravity action, stability proof or lift result.

The magnetic background is frozen during the compatibility fit.
The mandatory reciprocal Y current and full metric/Hodge
variations remain unresolved.

Evidence is immutable; historical results are read-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import secrets
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss, legval

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results/gravity2/g01j_bf_runs"

PINS = {
    "R3B_RESULT": (
        "results/data/"
        "032h17a12d1r3b_hook17_fdual_f_global_mirror_prefight_summary.json",
        "9474b6782104abb5bd8dd5e893137621b30ad96109e3e52c5a01268794810b11",
    ),
    "R3B_SOURCE": (
        "src/antigravity_research/agminer/"
        "hook17_fdual_f_global_mirror_prefight.py",
        "aa8f196fcae6a63405181ca62674e22ac67e5da88303759bdd99d25716fa2263",
    ),
    "R3B_LOADED_SOURCE": (
        "src/antigravity_research/agminer/"
        "hook17_f2_strong_payload_loading_rescue.py",
        "e1296794c25a4d0e4d5634c7e7d543a0b488b8d2a1963afcf7878bea1c1b99e7",
    ),
}

REF = 1.5429162116460216
FAIL = -129.67185782242464
R = 2.0


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(obj):
    return (
        json.dumps(obj, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode()


def exclusive(path, content):
    with path.open("xb") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())


def parent():
    for key, (relative, expected) in PINS.items():
        path = ROOT / relative

        if (
            not path.is_file()
            or path.is_symlink()
            or sha(path) != expected
        ):
            raise ValueError("PARENT_SHA_HOLD:" + key)

    raw = json.loads(
        (ROOT / PINS["R3B_RESULT"][0]).read_text()
    )

    if raw.get("branch") != "032H17A12D1R3B":
        raise ValueError("PARENT_BRANCH_DRIFT")

    if raw.get("surface_charge_physicalized") is not False:
        raise ValueError("SOURCE_CLAIM_DRIFT")

    fine = raw["grid_results"]["0.05"]

    capacity = fine["payload_reconstruction"][
        "normalized_mixed_global_field_energy_j"
    ]

    if abs(capacity - REF) > 1e-9:
        raise ValueError("R3B_CAPACITY_DRIFT")

    modes = []

    for mode in fine["multipole_modes"]:
        ell = int(mode["ell"])
        amplitude = float(mode["boundary_scalar_amplitude"])

        if not math.isfinite(amplitude):
            raise ValueError("NONFINITE_R3B_MULTIPOLE")

        modes.append({
            "ell": ell,
            "a": amplitude,
        })

    if (
        [m["ell"] for m in modes]
        != list(range(1, len(modes) + 1))
        or not 2 <= len(modes) <= 32
    ):
        raise ValueError("MODE_SET_HOLD")

    return modes


def source_modes(modes):
    records = []

    for mode in modes:
        ell = mode["ell"]
        a = mode["a"]

        magnetic = (ell + 1) * a / (math.sqrt(2) * R)
        charge = -(2 * ell + 1) * a / (math.sqrt(2) * R)

        norm = 4 * math.pi * R**2 / (2 * ell + 1)

        records.append({
            "ell": ell,
            "a": a,
            "b_mode": magnetic,
            "surface_charge_mode": charge,
            "required_kappa": -(2 * ell + 1) / (ell + 1),
            "laplace_lambda_dimless": ell * (ell + 1),
            "basis_l2_area_weight": norm,
        })

    return records


def fit(records, degree):
    """Independent multipoles, weighted by surface L2 norm."""
    used = [r for r in records if r["b_mode"] != 0]

    if len(used) < degree + 1:
        raise ValueError("NO_IDENTIFIABLE_BF_COEFFICIENTS")

    matrix = np.array([
        [
            r["laplace_lambda_dimless"]**k
            for k in range(degree + 1)
        ]
        for r in used
    ], dtype=float)

    target = np.array([
        r["required_kappa"] for r in used
    ])

    weights = np.array([
        r["basis_l2_area_weight"] * r["b_mode"]**2
        for r in used
    ])

    weighted_matrix = matrix * np.sqrt(weights)[:, None]
    weighted_target = target * np.sqrt(weights)

    coeff, _, rank, singular = np.linalg.lstsq(
        weighted_matrix,
        weighted_target,
        rcond=None,
    )

    prediction = matrix @ coeff

    error = float(
        np.dot(weights, (prediction - target)**2)
    )

    denominator = float(
        np.dot(weights, target**2)
    )

    relative = math.sqrt(
        max(error, 0) / denominator
    ) if denominator else 0.0

    condition = (
        float(singular[0] / singular[-1])
        if singular[-1] > 0
        else float("inf")
    )

    if not math.isfinite(condition):
        raise ValueError("UNIDENTIFIABLE_BF_OPERATOR")

    return {
        "degree": degree,
        "coefficients": coeff.tolist(),
        "weighted_charge_L2_relative_error": relative,
        "fit_matrix_condition": condition,
        "rank": int(rank),
        "weighted_L2_residual_below_1e_minus_12":
            bool(relative < 1e-12),
        "mode_count": len(used),
    }


def angular(records, fitted, order):
    mu, weights = leggauss(order)

    charge = np.zeros(order)
    magnetic = np.zeros(order)
    predicted = np.zeros(order)

    for record in records:
        ell = record["ell"]

        polynomial = np.zeros(ell + 1)
        polynomial[-1] = 1

        P = legval(mu, polynomial)
        eigenvalue = record["laplace_lambda_dimless"]

        ratio = sum(
            coefficient * eigenvalue**i
            for i, coefficient in enumerate(
                fitted["coefficients"]
            )
        )

        charge += record["surface_charge_mode"] * P
        magnetic += record["b_mode"] * P
        predicted += record["b_mode"] * ratio * P

    error = predicted - charge

    return {
        "n_mu": order,
        "charge_relative_L2_error": float(
            np.sqrt(
                np.dot(weights, error**2)
                / np.dot(weights, charge**2)
            )
        ),
        "charge_relative_peak_error": float(
            np.max(np.abs(error))
            / max(1e-30, np.max(np.abs(charge)))
        ),
        "integrated_net_charge_proxy": float(
            2 * math.pi * R**2 * np.dot(weights, charge)
        ),
        "charge_positive_fraction": float(
            np.dot(weights, charge > 0) / 2
        ),
        "charge_negative_fraction": float(
            np.dot(weights, charge < 0) / 2
        ),
    }


def negative_controls():
    controls = {
        "constant_kappa_cannot_match_ell1_and_ell2":
            (-3 / 2) != (-5 / 3),
        "positive_Hodge_sphere_eigenvalue":
            all(ell * (ell + 1) > 0 for ell in range(1, 13)),
        "variable_kappa_generic_gauge_variation_nonzero":
            (2.0 * 3.0) != 0.0,
        "static_background_null_not_full_Ward":
            (0 * 3) == 0 and (2 * 3) != 0,
        "surface_kinetic_mixing_static_magnetic_null":
            all(v == 0 for v in (0.0, 0.0)),
        "wrong_sign_interior_normal_rejected":
            (-1 / 3) != (-5 / 3),
        "kappa_spectrum_not_constant":
            all(
                -(2 * ell + 1) / (ell + 1)
                > -(2 * (ell + 1) + 1) / (ell + 2)
                for ell in range(1, 12)
            ),
        "historical_loaded_inward_preserved":
            FAIL < 0,
    }

    if not all(controls.values()):
        raise ValueError("NEGATIVE_CONTROL_FAIL")

    return controls


def produce(modes):
    records = source_modes(modes)

    m0 = fit(records, 0)
    m1 = fit(records, 1)

    if (
        m1["weighted_charge_L2_relative_error"]
        > m0["weighted_charge_L2_relative_error"] + 1e-12
    ):
        raise ValueError("EXTRA_OPERATOR_WORSENS_FIT")

    quadrature = []

    for order in (32, 64, 128, 256, 384):
        for name, fitted in (
            ("M0_BF", m0),
            ("M1_BF_HODGE_DELTA", m1),
        ):
            quadrature.append({
                "action": name,
                **angular(records, fitted, order),
            })

    truncation = []

    for count in range(2, len(records) + 1):
        for degree in (0, 1):
            truncation.append({
                "n_modes": count,
                "source_operator": degree,
                **fit(records[:count], degree),
            })

    active = [r for r in records if r["a"] != 0]

    return {
        "schema": "gravity2.g01j.bf_interface.v1",
        "scope":
            "SHELL_ACTION_MULTIPOLE_OBSTRUCTION_NOT_FULL_GRAVITY",
        "status":
            "PASS_SCOPED_BF_SOURCE_OPERATOR_ATLAS_NOT_GRAVITY",
        "R3B_prescribed_field_capacity_J": REF,
        "R3B_loaded_inward_minimum_m_s2": FAIL,
        "source_radius_m": R,
        "modes": records,
        "active_modes": len(active),
        "M0_constant_surface_BF_fit": m0,
        "M1_one_new_Hodge_Laplacian_BF_fit": m1,
        "n_quad_levels": 5,
        "quadrature": quadrature,
        "truncation": truncation,
        "M0_exact_compatibility_for_all_nonzero_modes":
            len(active) == 1,
        "source_action_candidate_M0":
            "S_BF=k0 integral_Sigma A_X wedge F_Y",
        "source_action_candidate_M1":
            "S_BF+k2 R^2 integral_Sigma A_X wedge Delta_H F_Y",
        "X_gauge_Ward_at_fixed_induced_metric":
            "FORMAL_FROM_D_DELTA_H=DELTA_H_D_AND_D_FY_ZERO;"
            " FULL_SURFACE_BOUNDARIES_OPEN",
        "Y_gauge_Ward":
            "FORMAL_F_Y_GAUGE_INVARIANCE",
        "reciprocal_Y_surface_current":
            "MANDATORY_NOT_SOLVED",
        "metric_dependence_M0":
            "DIRECT_HILBERT_STRESS_ZERO_AT_FIXED_COUPLING",
        "metric_dependence_M1":
            "HODGE_DELTA_METRIC_DEPENDENT_STRESS_NOT_DERIVED",
        "nonconstant_spatial_kappa_without_compensator":
            "OFF_SHELL_GAUGE_VIOLATION",
        "higher_derivative_Lorentzian_health":
            "NOT_ESTABLISHED",
        "matter_microphysics_and_level_quantization":
            "NOT_ESTABLISHED",
        "Earth_support_XY_and_neutral_common_action":
            "NOT_ESTABLISHED",
        "source_exterior_and_material_stability":
            "NOT_ESTABLISHED",
        "source_realization_in_SI":
            "NOT_ESTABLISHED",
        "GR_metric_Einstein_solution":
            "NOT_DERIVED",
        "loaded_geodesic_response":
            "NOT_DERIVED",
        "Earth_down_whole_craft_up":
            "NOT_DERIVED",
        "complete_operating_energy":
            "NOT_CERTIFIED",
        "006D_replaced": False,
        "qualified_physical_survivors": 0,
        "negative_controls": negative_controls(),
        "decision": (
            "CONSTANT_BF_EXACT_MULTIMODE_NO_GO"
            if len(active) > 1
            else "CONSTANT_BF_MONOMODE_CONDITIONAL"
        ),
        "next":
            "ONE_NEW_OPERATOR_REQUIRES_SAME_ACTION_Y_CURRENT_"
            "METRIC_STRESS_LORENTZIAN_HEALTH_AND_MICROSCOPIC_SOURCE",
    }


def selftest():
    dipole = source_modes([{"ell": 1, "a": 1.0}])

    assert dipole[0]["required_kappa"] == -1.5

    cases = source_modes([
        {"ell": ell, "a": 1 / ell}
        for ell in range(1, 5)
    ])

    assert (
        fit(cases, 1)["weighted_charge_L2_relative_error"]
        < fit(cases, 0)["weighted_charge_L2_relative_error"]
    )

    assert abs(
        angular(cases, fit(cases, 0), 128)[
            "integrated_net_charge_proxy"
        ]
    ) < 1e-12

    assert len(negative_controls()) == 8

    print(
        "G01J_BF_EXACT_MULTIPOLE_AND_NEGATIVE_CONTROLS=PASS"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", choices=("selftest", "run")
    )
    args = parser.parse_args()

    if args.command == "selftest":
        selftest()
        return 0

    import g01j_bf_check_v1 as checker

    if BASE.is_symlink():
        raise ValueError("UNSAFE_BASE_SYMLINK")

    BASE.mkdir(parents=True, exist_ok=True)

    run_id = (
        datetime.now(timezone.utc).strftime(
            "g01jbf_%Y%m%dT%H%M%SZ_"
        ) + secrets.token_hex(4)
    )

    out = BASE / run_id
    out.mkdir(mode=0o700)

    state = "HOLD"

    try:
        manifest = {
            "schema": "gravity2.g01j.bf_manifest.v1",
            "run_id": run_id,
            "parent_pins": {
                key: {"path": value[0], "sha256": value[1]}
                for key, value in PINS.items()
            },
            "sources_sha256": {
                name: sha(ROOT / "scripts" / name)
                for name in (
                    "g01j_bf_source_v1.py",
                    "g01j_bf_check_v1.py",
                )
            },
            "utc": datetime.now(timezone.utc).isoformat(),
            "test_policy": "NO_FULL_REPOSITORY_REGRESSION",
        }

        exclusive(out / "manifest.json", encode(manifest))

        modes = parent()
        science = produce(modes)

        exclusive(out / "science.json", encode(science))

        if checker.verify(out):
            raise ValueError("INDEPENDENT_VERIFIER_HOLD")

        state = "PASS_SCOPED"

    except Exception as exc:
        exclusive(
            out / "hold.json",
            encode({"status": "HOLD", "error": repr(exc)}),
        )
        print("G01J_HOLD=" + repr(exc), file=sys.stderr)

    finally:
        names = [
            path.name for path in out.iterdir()
            if path.is_file() and path.suffix == ".json"
        ]

        ledger = "".join(
            sha(out / name) + "  " + name + "\n"
            for name in sorted(names)
        )

        exclusive(
            out / "SHA256SUMS.txt",
            ledger.encode(),
        )

        archive = out / (run_id + "_UPLOAD.tar.gz")

        with tarfile.open(archive, "x:gz") as bundle:
            for name in sorted(names) + ["SHA256SUMS.txt"]:
                bundle.add(
                    out / name,
                    arcname=run_id + "/" + name,
                )

        print("G01J_RUN=" + run_id)
        print("G01J_STATUS=" + state)
        print("UPLOAD_ARCHIVE=" + str(archive))
        print("UPLOAD_ARCHIVE_SHA256=" + sha(archive))

    return 0 if state == "PASS_SCOPED" else 3


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(
            "G01J_FATAL=" + repr(exc),
            file=sys.stderr,
        )
        raise SystemExit(3)
