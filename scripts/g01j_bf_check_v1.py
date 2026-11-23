"""Independent G01-J boundary source-action numerical auditor.

Reconstructs the multipole jump identities, normal-equation
coefficients, angular quadratures, and immutable parent locks.

Does not assert full Ward closure, microscopic sourceability,
stability, Einstein gravity, or spacecraft lift.
"""
from __future__ import annotations

import hashlib
import json
import math

import numpy as np
from numpy.polynomial.legendre import leggauss, legval


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(obj):
    return (
        json.dumps(obj, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode()


def close(a, b, rtol=2e-10, atol=2e-12):
    return math.isclose(
        float(a), float(b),
        rel_tol=rtol, abs_tol=atol,
    )


def review(science):
    if science["R3B_prescribed_field_capacity_J"] != (
        1.5429162116460216
    ):
        raise ValueError("CAPACITY_MISMATCH")

    if science["R3B_loaded_inward_minimum_m_s2"] != (
        -129.67185782242464
    ):
        raise ValueError("LOADED_SIGN_DRIFT")

    if (
        science["qualified_physical_survivors"] != 0
        or science["GR_metric_Einstein_solution"]
        != "NOT_DERIVED"
    ):
        raise ValueError("FALSE_PHYSICAL_PROMOTION")

    rows = science["modes"]
    count = len(rows)
    radius = science["source_radius_m"]

    if [r["ell"] for r in rows] != list(range(1, count + 1)):
        raise ValueError("MODE_SEQUENCE_DRIFT")

    for row in rows:
        ell, amplitude = row["ell"], row["a"]

        magnetic = (
            (ell + 1) * amplitude
            / (math.sqrt(2) * radius)
        )

        charge = (
            -(2 * ell + 1) * amplitude
            / (math.sqrt(2) * radius)
        )

        if not (
            close(row["b_mode"], magnetic)
            and close(row["surface_charge_mode"], charge)
            and close(
                row["required_kappa"],
                -2 + 1 / (ell + 1),
            )
        ):
            raise ValueError("BOUNDARY_IDENTITY_DRIFT")

    # Independent moment-equation solution.
    weights = [
        row["basis_l2_area_weight"] * row["b_mode"]**2
        for row in rows
    ]

    total = sum(weights)

    if total <= 0:
        raise ValueError("ZERO_FIELD_PARENT")

    for name, degree in (
        ("M0_constant_surface_BF_fit", 0),
        ("M1_one_new_Hodge_Laplacian_BF_fit", 1),
    ):
        fit = science[name]

        if degree == 0:
            k0 = sum(
                w * row["required_kappa"]
                for w, row in zip(weights, rows)
            ) / total

            if not close(fit["coefficients"][0], k0):
                raise ValueError("M0_FIT_DRIFT")

        else:
            a = sum(
                w * row["laplace_lambda_dimless"]
                for w, row in zip(weights, rows)
            )

            b = sum(
                w * row["laplace_lambda_dimless"]**2
                for w, row in zip(weights, rows)
            )

            c = sum(
                w * row["required_kappa"]
                for w, row in zip(weights, rows)
            )

            d = sum(
                w * row["laplace_lambda_dimless"]
                * row["required_kappa"]
                for w, row in zip(weights, rows)
            )

            determinant = total * b - a * a

            if determinant <= 0:
                raise ValueError("UNIDENTIFIABLE_OPERATOR")

            k2 = (total * d - a * c) / determinant
            k0 = (c - a * k2) / total

            if not (
                close(fit["coefficients"][0], k0, rtol=1e-8)
                and close(fit["coefficients"][1], k2, rtol=1e-7)
            ):
                raise ValueError("M1_FIT_DRIFT")

        predictions = [
            sum(
                coefficient
                * row["laplace_lambda_dimless"]**i
                for i, coefficient in enumerate(
                    fit["coefficients"]
                )
            )
            for row in rows
        ]

        numerator = sum(
            w * (prediction - row["required_kappa"])**2
            for w, prediction, row
            in zip(weights, predictions, rows)
        )

        denominator = sum(
            w * row["required_kappa"]**2
            for w, row in zip(weights, rows)
        )

        relative = math.sqrt(numerator / denominator)

        if not close(
            relative,
            fit["weighted_charge_L2_relative_error"],
            rtol=1e-6,
        ):
            raise ValueError("RESIDUAL_DRIFT")

    if (
        science["M1_one_new_Hodge_Laplacian_BF_fit"][
            "weighted_charge_L2_relative_error"
        ]
        > science["M0_constant_surface_BF_fit"][
            "weighted_charge_L2_relative_error"
        ] + 1e-12
    ):
        raise ValueError("RANK_FAILURE")

    for item in science["quadrature"]:
        mu, weights = leggauss(item["n_mu"])
        charge = np.zeros_like(mu)
        predicted = np.zeros_like(mu)

        fitted = (
            science["M0_constant_surface_BF_fit"]
            if item["action"] == "M0_BF"
            else science["M1_one_new_Hodge_Laplacian_BF_fit"]
        )

        for row in rows:
            polynomial = np.zeros(row["ell"] + 1)
            polynomial[-1] = 1

            P = legval(mu, polynomial)
            eigenvalue = row["laplace_lambda_dimless"]

            kappa = sum(
                coefficient * eigenvalue**i
                for i, coefficient in enumerate(
                    fitted["coefficients"]
                )
            )

            charge += row["surface_charge_mode"] * P
            predicted += kappa * row["b_mode"] * P

        result = float(
            np.sqrt(
                np.dot(weights, (predicted - charge)**2)
                / np.dot(weights, charge**2)
            )
        )

        if not close(
            result,
            item["charge_relative_L2_error"],
            rtol=1e-8,
        ):
            raise ValueError("QUADRATURE_DRIFT")

    if (
        len(science["quadrature"]) != 10
        or len(science["truncation"]) != 2 * (count - 1)
        or len(science["negative_controls"]) != 8
        or not all(science["negative_controls"].values())
    ):
        raise ValueError("INCOMPLETE_SCIENCE")

    return {
        "status": "PASS_INDEPENDENT_BF_SOURCE_ATLAS_NO_GRAVITY",
        "mode_checks": count,
        "quadrature_checks": len(science["quadrature"]),
        "truncation_cases": len(science["truncation"]),
        "negative_controls": 8,
        "physical_survivors": 0,
    }


def verify(folder):
    import g01j_bf_source_v1 as producer

    try:
        manifest = json.loads(
            (folder / "manifest.json").read_text()
        )

        science = json.loads(
            (folder / "science.json").read_text()
        )

        for key, (relative, expected) in producer.PINS.items():
            if manifest["parent_pins"][key] != {
                "path": relative,
                "sha256": expected,
            }:
                raise ValueError("PARENT_MANIFEST_DRIFT")

            if sha(producer.ROOT / relative) != expected:
                raise ValueError("PARENT_SHA_DRIFT")

        for name in (
            "g01j_bf_source_v1.py",
            "g01j_bf_check_v1.py",
        ):
            path = producer.ROOT / "scripts" / name

            if manifest["sources_sha256"][name] != sha(path):
                raise ValueError("SOURCE_CODE_DRIFT")

        result = review(science)

        result.update({
            "science_sha256": sha(folder / "science.json"),
            "manifest_sha256": sha(folder / "manifest.json"),
        })

        destination = folder / "verification.json"
        content = encode(result)

        if destination.is_file():
            if destination.read_bytes() != content:
                raise ValueError("VERIFICATION_DRIFT")
        else:
            with destination.open("xb") as stream:
                stream.write(content)

        print("G01J_INDEPENDENT_VERIFY=" + result["status"])
        return 0

    except Exception as exc:
        print("G01J_VERIFY_HOLD=" + repr(exc))
        return 3
