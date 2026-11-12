"""R3X3B11-M4 — Quasistatic R3B independent-source phase gate.

QUESTION
--------
Can arbitrary independent electric/magnetic source amplitudes,
relative phases, polarity reversals and duty cycles give >=1g
cycle-averaged acceleration across the entire sampled loaded
R3B torus, with mean canonical field energy <=1.547304 J?

MATHEMATICAL METHOD
-------------------
With frozen density and the corrected R3X1 Lorentzian action,
the loaded carrier equations are linear in the two source
amplitudes u(t), v(t).

Every local acceleration and the canonical energy is quadratic:

    a_i = A_i*u^2 + B_i*u*v + C_i*v^2

The time averages are determined by the positive-semidefinite
source covariance S = <[u,v][u,v]^T>.

We maximize the minimum local acceleration subject to the
canonical mean-energy limit. The PSD cone is replaced by
64 supporting inequalities that define an OUTER relaxation.
Therefore its optimum is an upper bound, not an achievable
waveform unless physical covariance validity is verified.

We also compute an independent spectral upper bound on
whole-payload COM acceleration.

LIMITATIONS
-----------
No actual time-domain Maxwell evolution, Faraday induction,
microscopic source, B7 shell inserted into the loaded solver,
source reaction, radiation, moving material or device-energy
certificate. A negative result closes only this fixed-density,
quasistatic original-source-shape family.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import linprog

from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    EV_J,
    HBAR_C_EV_M,
    REFERENCE_PORTAL_SCALE_EV,
)

from antigravity_research.agminer.hook17_fdual_f_r3c1_validation import (
    _build_baseline_and_prep,
)

from antigravity_research.agminer.hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    _solve_loaded,
)

from antigravity_research.agminer.hook17_fdual_f_loaded_payload_homotopy import (
    _fields_from_potentials,
    _vectors_to_full_potentials,
)

BRANCH = "032H17A12D1R3X3B11_M4"
G = 9.80665
ENERGY_CAP = 1.5473042949759672

KAPPA = (
    -2 * HBAR_C_EV_M**2
    / REFERENCE_PORTAL_SCALE_EV**4
)


def signed_potentials(setup, electric, magnetic):
    baseline = setup["prep"]
    prep = dict(baseline)

    for name, sign in (
        ("phi0_vec", electric),
        ("d_phi0", electric),
        ("a0_vec", magnetic),
        ("c_a0", magnetic),
    ):
        prep[name] = sign * baseline[name]

    solution = _solve_loaded(prep, 1., 1.)

    if (
        not solution["success"]
        or solution["relative_residual"] >= 1e-8
    ):
        raise RuntimeError(
            f"Loaded source solve failed: "
            f"{electric}, {magnetic}"
        )

    return _vectors_to_full_potentials(
        prep,
        setup["field"],
        electric * setup["phi0"],
        magnetic * setup["a0"],
        solution,
    )


def measure(setup, phi, potential_a):
    field = setup["field"]
    h = float(field["h"])

    em = _fields_from_potentials(
        phi, potential_a, field["rho_grid"], h
    )

    sigma = KAPPA * (
        em["e_rho"] * em["b_rho"]
        + em["e_z"] * em["b_z"]
    )

    acceleration = (
        -C_LIGHT_M_S**2
        * np.gradient(
            sigma, h, axis=0, edge_order=2
        )
    )

    volume = (
        2 * math.pi * field["rho_grid"] * h*h
    )

    energy = (
        0.5
        * sum(
            float(np.sum(volume * em[key]**2))
            for key in (
                "e_rho", "e_z", "b_rho", "b_z"
            )
        )
        * EV_J / HBAR_C_EV_M
    )

    return (
        np.asarray(
            acceleration[field["payload"]],
            dtype=float,
        ),
        float(energy),
    )


def grid_case(h):
    setup = _build_baseline_and_prep(h)

    # Fully re-solved signed source states.
    phi_pp, a_pp = signed_potentials(
        setup, 1, 1
    )

    phi_pm, a_pm = signed_potentials(
        setup, 1, -1
    )

    # Exact independent electric/magnetic source basis.
    phi_e = (phi_pp + phi_pm) / 2
    a_e = (a_pp + a_pm) / 2

    phi_b = (phi_pp - phi_pm) / 2
    a_b = (a_pp - a_pm) / 2

    # Independently check linear source superposition.
    phi_e0, a_e0 = signed_potentials(
        setup, 1, 0
    )

    phi_b0, a_b0 = signed_potentials(
        setup, 0, 1
    )

    for actual, predicted in (
        (phi_e0, phi_e),
        (a_e0, a_e),
        (phi_b0, phi_b),
        (a_b0, a_b),
    ):
        assert np.allclose(
            actual, predicted,
            atol=1e-8, rtol=1e-8
        )

    acc_e, en_e = measure(
        setup, phi_e, a_e
    )
    acc_b, en_b = measure(
        setup, phi_b, a_b
    )
    acc_pp, en_pp = measure(
        setup, phi_pp, a_pp
    )
    acc_pm, en_pm = measure(
        setup, phi_pm, a_pm
    )

    # Coefficients multiply (u², uv, v²).
    Q = np.column_stack((
        acc_e,
        acc_pp - acc_e - acc_b,
        acc_b,
    ))

    H = np.array([
        en_e,
        en_pp - en_e - en_b,
        en_b,
    ])

    assert np.max(abs(
        Q @ np.array([1., -1., 1.])
        - acc_pm
    )) < 1e-7

    assert abs(
        H @ np.array([1., -1., 1.])
        - en_pm
    ) < 1e-8

    # Independent mixed-amplitude quadratic checks.
    for u, v in (
        (.4, -.7),
        (-1.4, .2),
        (.15, 1.2),
    ):
        a_direct, e_direct = measure(
            setup,
            u*phi_e + v*phi_b,
            u*a_e + v*a_b,
        )

        basis = np.array([u*u, u*v, v*v])

        assert np.allclose(
            a_direct, Q @ basis,
            atol=1e-7, rtol=1e-10
        )

        assert abs(
            e_direct - H @ basis
        ) < 1e-8

    field = setup["field"]
    weights = (
        2 * math.pi * field["rho_grid"]
        * h*h * setup["density"]
    )

    mass = float(np.sum(weights))

    normalized = (
        weights[field["payload"]] / mass
    )

    Q_com = normalized @ Q

    energy_matrix = np.array([
        [H[0], H[1]/2],
        [H[1]/2, H[2]],
    ])

    force_matrix = np.array([
        [Q_com[0], Q_com[1]/2],
        [Q_com[1]/2, Q_com[2]],
    ])

    energy_eigenvalues = np.linalg.eigvalsh(
        energy_matrix
    )

    assert min(energy_eigenvalues) > 0

    # Exact generalized-eigenvalue upper bound
    # for cycle-averaged COM acceleration.
    com_upper = (
        ENERGY_CAP
        * max(
            eigh(
                force_matrix,
                energy_matrix,
                eigvals_only=True,
            )
        )
    )

    # Outer approximation to covariance PSD:
    # (cos t, sin t)^T S (cos t, sin t) >= 0.
    angles = np.arange(64) * math.pi / 64

    psd_inequalities = np.array([
        [
            -math.cos(t)**2,
            -2*math.sin(t)*math.cos(t),
            -math.sin(t)**2,
            0.,
        ]
        for t in angles
    ])

    # Decision variables: S11, S12, S22, min_accel.
    n = Q.shape[0]

    A_ub = np.vstack((
        np.column_stack((
            -Q,
            np.ones(n),
        )),
        psd_inequalities,
    ))

    # Setting mean energy equal to the cap gives
    # the most generous normalized positive-force test.
    optimization = linprog(
        c=[0., 0., 0., -1.],
        A_ub=A_ub,
        b_ub=np.zeros(len(A_ub)),
        A_eq=np.array([[
            H[0], H[1], H[2], 0.,
        ]]),
        b_eq=[ENERGY_CAP],
        bounds=[(None, None)]*4,
        method="highs",
    )

    if not optimization.success:
        raise RuntimeError(
            optimization.message
        )

    s11, s12, s22, upper = map(
        float, optimization.x
    )

    covariance_candidate = np.array([
        [s11, s12],
        [s12, s22],
    ])

    covariance_min_eigenvalue = float(
        min(np.linalg.eigvalsh(
            covariance_candidate
        ))
    )

    assert abs(
        H @ optimization.x[:3] - ENERGY_CAP
    ) < 5e-8

    assert min(
        Q @ optimization.x[:3]
    ) >= upper - 5e-7

    print(
        f"h={h:.3f}m "
        f"COM_upper={com_upper:+.8f} "
        f"local_maximin_upper={upper:+.8f} "
        f"fraction_g={upper/G:+.7f}",
        flush=True,
    )

    return {
        "grid_m": h,
        "payload_samples": n,
        "original_loaded_energy_j": en_pp,
        "canonical_energy_matrix_min_eigen_j":
            float(min(energy_eigenvalues)),
        "com_acceleration_upper_bound_m_s2":
            float(com_upper),
        "everywhere_acceleration_outer_upper_bound_m_s2":
            upper,
        "covariance_candidate_min_eigenvalue":
            covariance_min_eigenvalue,
        "mean_field_energy_cap_j": ENERGY_CAP,
        "com_1g_excluded": bool(
            com_upper < G
        ),
        "everywhere_1g_excluded": bool(
            upper < G
        ),
    }


def main():
    results = [
        grid_case(h)
        for h in (.075, .05, .04)
    ]

    summary = {
        "branch": BRANCH,
        "scope":
            "QUASISTATIC_LOADED_R3B_TWO_SOURCE_COVARIANCE",
        "cycle_period_ms": 1.0,
        "r3b_preloaded_energy_reference_j":
            1.5429162116460216,
        "b7_preloaded_energy_reference_j":
            ENERGY_CAP,
        "mean_field_energy_cap_not_device_energy":
            True,
        "actual_time_dependent_maxwell_evolution":
            False,
        "actual_polarity_switching_currents":
            False,
        "B7_shell_inserted": False,
        "microscopic_source_realized": False,
        "whole_craft_lift": False,
        "complete_energy_certified": False,
        "006D_replaced": False,
        "results": results,
    }

    output = Path(
        "results/data/"
        "032h17a12d1r3x3b11_m4_phase_covariance_summary.json"
    )

    output.parent.mkdir(
        parents=True, exist_ok=True
    )

    output.write_text(
        json.dumps(
            summary, indent=2, sort_keys=True
        ) + "\n",
        encoding="utf8",
    )

    print(
        "ALL_GRIDS_COM_1G_EXCLUDED=",
        all(r["com_1g_excluded"] for r in results),
    )

    print(
        "ALL_GRIDS_EVERYWHERE_1G_EXCLUDED=",
        all(
            r["everywhere_1g_excluded"]
            for r in results
        ),
    )

    print(
        "PHYSICAL_TIME_DOMAIN_POLARITY_SWITCH=NOT_TESTED"
    )

    print("SUMMARY=", output)


if __name__ == "__main__":
    main()
