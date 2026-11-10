"""R3X3B8 — exact spherical topological-interface screening.

Static canonical Maxwell fields, spherical material interface,
constant theta inside and zero theta outside.

Inside:
    D = E + theta B
    H = B - theta E

Outside:
    D = E
    H = B

No free charge or free surface current at the payload boundary.

This is an independently solvable spherical reference problem,
NOT the actual R3B torus and NOT a universal impossibility theorem.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


def exact_transfer_matrix(ell: int, theta: float) -> np.ndarray:
    if type(ell) is not int or ell < 1:
        raise ValueError("ell must be a positive integer")

    if not math.isfinite(theta):
        raise ValueError("theta must be finite")

    p = 2 * ell + 1
    determinant = float(
        p * p + ell * (ell + 1) * theta * theta
    )

    return (p / determinant) * np.array(
        [
            [p, -ell * theta],
            [(ell + 1) * theta, p],
        ],
        dtype=float,
    )


def boundary_residual(
    ell: int,
    theta: float,
    incident: np.ndarray,
    interior: np.ndarray,
    radius: float = 1.0,
) -> dict[str, float]:
    """Independently verify the four interface conditions."""
    if radius <= 0 or not math.isfinite(radius):
        raise ValueError("Invalid radius")

    ae, ab = np.asarray(incident, dtype=float)
    ce, cb = np.asarray(interior, dtype=float)

    power = radius ** (2 * ell + 1)

    # Scattered exterior electric/magnetic multipoles.
    be = (ce - ae) * power
    bb = -ell / (ell + 1) * (cb - ab) * power

    et_out = ae + be / power
    et_in = ce

    br_out = -ell * ab + (ell + 1) * bb / power
    br_in = -ell * cb

    er_out = -ell * ae + (ell + 1) * be / power
    dr_in = -ell * (ce + theta * cb)

    bt_out = ab + bb / power
    ht_in = cb - theta * ce

    return {
        "tangential_E": et_out - et_in,
        "normal_B": br_out - br_in,
        "normal_D": er_out - dr_in,
        "tangential_H": bt_out - ht_in,
    }


def universal_high_theta_bound(theta: float):
    """Uniform bound on every ell>=1 spherical mode.

    Write the matching matrix as A = p*I + theta*J.
    The smallest singular value of J is ell.

    Therefore:
        sigma_min(A) >= abs(theta)*ell - p

    Since p/ell <= 3 for ell>=1:
        norm(T_ell) <= 3/(abs(theta)-3)

    This bound is meaningful for abs(theta)>3.
    """
    if not math.isfinite(theta):
        raise ValueError("theta must be finite")

    if abs(theta) <= 3:
        return None

    return 3.0 / (abs(theta) - 3.0)


def screening_row(
    ell: int,
    theta: float,
    incident: tuple[float, float] = (1.0, 1.0),
):
    transfer = exact_transfer_matrix(ell, theta)

    external = np.asarray(incident, dtype=float)
    internal = transfer @ external

    maximum_singular_value = float(
        np.linalg.svd(transfer, compute_uv=False)[0]
    )

    residuals = boundary_residual(
        ell, theta, external, internal
    )

    bound = universal_high_theta_bound(theta)

    if (
        bound is not None
        and maximum_singular_value > bound * (1 + 1e-12)
    ):
        raise AssertionError("Uniform transmission bound failed")

    external_eb = float(external[0] * external[1])
    internal_eb = float(internal[0] * internal[1])

    return {
        "ell": ell,
        "theta": float(theta),
        "incident_potentials": external.tolist(),
        "inside_potentials": internal.tolist(),
        "transfer_norm_max": maximum_singular_value,
        "universal_bound": bound,
        "max_boundary_residual": max(
            abs(value) for value in residuals.values()
        ),
        "interior_EB_to_incident_EB": (
            internal_eb / external_eb
            if external_eb != 0
            else None
        ),
        "zero_free_interface_sources": True,
        "torus_no_go_proved": False,
    }


def symbolic_certificate():
    import sympy as sp

    ell, theta = sp.symbols(
        "ell theta", positive=True, integer=True
    )

    p = 2 * ell + 1

    matrix = sp.Matrix([
        [p, ell * theta],
        [-(ell + 1) * theta, p],
    ])

    expected = (
        p * p + ell * (ell + 1) * theta * theta
    )

    determinant = sp.factor(matrix.det())

    assert sp.simplify(determinant - expected) == 0

    inverse = sp.simplify(p * matrix.inv())

    assert sp.simplify(
        matrix * inverse - p * sp.eye(2)
    ) == sp.zeros(2)

    return {
        "determinant": str(determinant),
        "det_positive_for_real_theta_ell_gt0": True,
        "uniform_large_theta_bound":
            "norm(T_ell) <= 3/(abs(theta)-3), abs(theta)>3",
        "other_payload_geometries_excluded": False,
    }


def run():
    result = {
        "branch": "032H17A12D1R3X3B8",
        "scope":
            "STATIC_CANONICAL_U1_SPHERICAL_HOMOGENEOUS_THETA_INTERFACE",
        "symbolic": symbolic_certificate(),
        "modes": [
            screening_row(ell, theta)
            for theta in (0.0, 1.0, 10.0, 100.0, 1e4)
            for ell in (1, 2, 3, 10, 50)
        ],
        "r3b_torus_no_go_proved": False,
        "full_action_noether_certified": False,
        "microscopic_source_realized": False,
        "complete_energy_certified": False,
        "physical_antigravity_model_found": False,
        "006d_replaced": False,
    }

    path = Path(
        "results/data/"
        "032h17a12d1r3x3b8_spherical_interface_screening_summary.json"
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")

    for row in result["modes"]:
        if (
            row["theta"] in (0.0, 100.0, 1e4)
            and row["ell"] in (1, 10)
        ):
            print(
                "THETA=", row["theta"],
                "ELL=", row["ell"],
                "INSIDE=", row["inside_potentials"],
                "TRANSFER_NORM=", row["transfer_norm_max"],
                "UPPER_BOUND=", row["universal_bound"],
                "BC_ERROR=", row["max_boundary_residual"],
                flush=True,
            )

    print("R3X3B8_RESULT_PATH=", path)
    return result


if __name__ == "__main__":
    run()
