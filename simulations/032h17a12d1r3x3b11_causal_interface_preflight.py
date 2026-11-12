"""R3X3B11 — exact causal-interface carrier preflight.

PURPOSE
-------
Test the frequency-bypass hypothesis in the sharp planar,
fixed-matter limit of corrected R3X1 two-U(1) dynamics.

This is NOT a fully coupled toroidal time-domain simulation.

ACTION
------
L = 1/2 sum_I (E_I^2 - B_I^2)
    + theta * (E_X.B_Y + E_Y.B_X) + L_source.

Canonical units c=1; theta is dimensionless.

The source construction below uses the existing B7 finite
charge layer and an exactly conserved effective current.

LIMITATIONS
-----------
No microscopic source, finite-payload impulse, source reaction,
cycle stability, complete energy, or device certification.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.hook17_fdual_f_r3x3b7_finite_charge_shell import (
    evaluate_r3b_grid,
    source_density_proxy,
)

ROT = np.array([[0., -1.], [1., 0.]])
R = np.kron(np.eye(2), ROT)
Q = np.kron(np.array([[0., 1.], [1., 0.]]), np.eye(2))
I4 = np.eye(4)

# Historical B10 comparator, NOT the actual torus theta field.
THETA_COMPARATOR = 18987.283771593688


def mixed_c(e, b):
    """Two-sector topological mixed invariant."""
    return float(e[0] @ b[1] + e[1] @ b[0])


def carrier(e, b, theta):
    """Constitutive fields and canonical Legendre-energy audit."""
    d = e + theta * b[::-1]
    h = b - theta * e[::-1]

    lagrangian = (
        (np.sum(e*e) - np.sum(b*b))/2
        + theta * mixed_c(e, b)
    )

    energy = (np.sum(e*e) + np.sum(b*b))/2
    legendre = float(np.sum(e*d) - lagrangian)
    poynting = np.cross(e, h).sum(axis=0)

    return d, h, energy, legendre, poynting


def scatter(theta, incident):
    """Independent boundary solve versus exact analytic result."""
    i = np.asarray(incident, dtype=float)

    reflected = np.linalg.solve(
        2*R - theta*Q, theta*Q @ i
    )
    transmitted = i + reflected

    rclosed = (
        (-theta*theta*I4 - 2*theta*R@Q) @ i
        / (4 + theta*theta)
    )
    tclosed = (
        (4*I4 - 2*theta*R@Q) @ i
        / (4 + theta*theta)
    )

    h_left = R @ (i - reflected)
    h_right = R @ transmitted - theta*Q @ transmitted

    p_in = float(i @ i)

    e3 = np.zeros((2, 3))
    b3 = np.zeros((2, 3))

    e3[:, :2] = transmitted.reshape(2, 2)
    b3[:, :2] = (R @ transmitted).reshape(2, 2)

    return {
        "reflection_power":
            float(reflected @ reflected / p_in),
        "transmission_power":
            float(transmitted @ transmitted / p_in),
        "closed_form_relative_error":
            float(max(
                np.linalg.norm(reflected-rclosed),
                np.linalg.norm(transmitted-tclosed),
            ) / math.sqrt(p_in)),
        "boundary_H_error":
            float(np.linalg.norm(
                h_left-h_right
            ) / math.sqrt(p_in)),
        "copropagating_transmitted_C":
            mixed_c(e3, b3),
    }


def pulse(t, tau):
    """Smooth compact-duration source envelope and derivative."""
    if tau <= 0:
        raise ValueError("tau must be positive")

    x = t/tau
    if abs(x) >= 1:
        return 0., 0.

    y = 1 - x*x
    q = math.exp(1 - 1/y)
    qdot = q * (-2*t/(tau*tau*y*y))

    return q, qdot


def b7_source_continuity(ell, r, t, tau):
    """Conserved finite-shell multipole charge/current coefficients."""
    rho_l = source_density_proxy(
        ell, 1., 2., 0.1, r
    )
    q, qdot = pulse(t, tau)

    rho = q * rho_l
    current_t = (
        qdot*r*rho_l/(ell*(ell+1))
    )
    residual = (
        qdot*rho_l
        - ell*(ell+1)*current_t/r
    )

    return rho, current_t, residual


def run():
    baseline = evaluate_r3b_grid(0.05, (0.1,))

    e0 = float(
        baseline["original_preloaded_field_energy_j"]
    )
    e7 = float(
        baseline["shells"][0]["mixed_field_energy_j_normalized"]
    )

    assert abs(e0-1.5429162116460216) < 1e-8
    assert abs(e7-1.5473042949759672) < 1e-8

    rng = np.random.default_rng(32)

    for th in (
        -THETA_COMPARATOR, -1., 0., 1., THETA_COMPARATOR
    ):
        e = rng.standard_normal((2, 3))
        b = rng.standard_normal((2, 3))

        d, h, u, u_leg, s = carrier(e, b, th)

        assert np.allclose(d, e+th*b[::-1])
        assert np.allclose(h, b-th*e[::-1])
        # Scale the floating-point tolerance to the intermediate
        # constitutive terms, not just the small final energy.
        # Large theta causes cancellation in E.D - L.
        roundoff_budget = (
            64.0 * np.finfo(float).eps
            * (
                1.0
                + float(np.sum(np.abs(e*d)))
                + abs(u)
                + abs(u_leg)
            )
        )
        assert abs(u-u_leg) <= roundoff_budget, (
            f"Canonical energy mismatch: "
            f"u={u}, u_leg={u_leg}, "
            f"error={abs(u-u_leg)}, "
            f"budget={roundoff_budget}"
        )
        assert np.allclose(
            s, np.cross(e, b).sum(axis=0),
            atol=1e-11
        )

        for inc in (
            np.array([1., 0., 0., 0.]),
            np.array([1., 2., 3., -4.]),
        ):
            z = scatter(th, inc)

            assert z["closed_form_relative_error"] < 1e-10
            assert z["boundary_H_error"] < 1e-10
            assert abs(
                z["reflection_power"]
                + z["transmission_power"] - 1
            ) < 1e-10
            assert abs(
                z["transmission_power"]
                - 4/(4+th*th)
            ) < 1e-10
            assert abs(
                z["copropagating_transmitted_C"]
            ) < 1e-11

    radii = np.array([
        1.4, 1.8, 1.89, 1.92,
        1.95, 1.98, 2.01, 2.4,
    ])

    continuity_errors = []

    for ell in (1, 2, 3):
        rho, j, res = b7_source_continuity(
            ell, radii, 2e-9, 1e-8
        )

        relative = float(
            np.max(np.abs(res))
            / max(1., np.max(np.abs(rho))/1e-8)
        )

        continuity_errors.append(relative)
        assert relative < 1e-12

        # Relative tolerance avoids magnified floating-point
        # roundoff for nanosecond-scale source derivatives.
        exterior_error = max(
            np.abs(j[:3]).max(),
            np.abs(j[6:]).max(),
        ) / max(1., np.abs(j).max())

        assert exterior_error < 2e-14

    response = scatter(
        THETA_COMPARATOR,
        np.array([1., 0., 0., 0.]),
    )

    result = {
        "branch": "032H17A12D1R3X3B11",
        "scope": "SHARP_PLANAR_FIXED_MATTER_P1_P2_CONTROL",
        "code_sha256":
            hashlib.sha256(
                Path(__file__).read_bytes()
            ).hexdigest(),
        "r3b_preloaded_reproduced_j": e0,
        "b7_10cm_preloaded_reproduced_j": e7,
        "finite_width_source_continuity_max_relative":
            max(continuity_errors),
        "theta_comparator_not_actual_toroidal_theta":
            THETA_COMPARATOR,
        "exact_planar_reflection_power":
            response["reflection_power"],
        "exact_planar_transmission_power":
            response["transmission_power"],
        "ideal_planar_frequency_advantage": False,
        "co_propagating_mixed_invariant_zero": True,
        "carrier_action_energy_identity_pass": True,
        "complete_matter_source_action_verified": False,
        "actual_toroidal_causal_response_tested": False,
        "fully_loaded_finite_payload_impulse_tested": False,
        "whole_craft_lift_tested": False,
        "complete_operating_energy_certified": False,
        "physical_antigravity_model_found": False,
        "006d_replaced": False,
        "classification":
            "RED_SCOPED_IDEAL_PLANAR_FREQUENCY_BYPASS_ONLY",
    }

    path = Path(
        "results/data/"
        "032h17a12d1r3x3b11_causal_interface_preflight_summary.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf8",
    )

    print(f"R3B={e0:.16f} J; B7={e7:.16f} J")
    print(
        "ideal_planar_power_transmission="
        f"{response['transmission_power']:.12g}"
    )
    print(
        "B11 P2 ideal planar frequency bypass: RED_SCOPED"
    )
    print("Actual toroidal loaded impulse: NOT_TESTED")
    print("RESULT=", path)

    return result


if __name__ == "__main__":
    run()
