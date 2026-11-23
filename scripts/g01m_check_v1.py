"""Independent G01-M physics verifier.

Reconstructs spherical fields using scipy.special Legendre
functions rather than importing the producing science model.

Checks material stationarity, X/Y reciprocity, source current,
full static spectral Hessian, target mismatch, energy derivative,
switching ledger and convergence.

This cannot certify real matter or Einstein gravity.
"""
from __future__ import annotations

import math
import numpy as np
from scipy.special import eval_legendre


def independent_review(science, parent):
    if (
        science["physical_survivors"] != 0
        or science["replaced_006D"]
        or science["matched_original_12_modes"]
        or len(science["modes"]) != 12
    ):
        raise ValueError("FALSE_PHYSICAL_PROMOTION")

    p = science["material_parameters"]

    R = p["R"]
    K = p["K"]
    g = p["g"]
    H = p["H"]
    chi = p["chi_magnetic_coupling"]
    r = p["r_positive_mass"]
    kappa = p["kappa_spatial_gradient"]
    beta = p["beta_negative_quartic_magnitude"]
    gamma = p["gamma_positive_sextic"]

    if (
        abs(K * H - g*g - 0.4) > 1e-11
        or not 0 < kappa <= p["Z_time_kinetic"]
        or gamma <= 0
    ):
        raise ValueError("INVALID_MATERIAL_HYPOTHESIS")

    max_boundary = 0.0

    for row, old in zip(
        science["modes"], parent["modes"]
    ):
        l = row["ell"]
        A = R / (2*l + 1)
        M = R/l + R/(l + 1)
        D = H + M - g*g / (K + A)

        max_boundary = max(
            max_boundary,
            abs(row["A"] - A),
            abs(row["M_full"] - M),
            abs(row["D"] - D),
        )

        expected = (
            old["b_mode"]
            / parent["modes"][0]["b_mode"]
        )

        if abs(row["target_b_over_B0"] - expected) > 2e-14:
            raise ValueError("R3B_REFERENCE_MODE_DRIFT")

        if D <= 0:
            raise ValueError("TWO_SIDED_STATIC_HESSIAN_FAIL")

    if max_boundary > 2e-13:
        raise ValueError("TWO_SIDED_DTN_FAIL")

    levels = science["spectral_solutions"]

    if [
        (x["truncation"], x["quadrature"])
        for x in levels
    ] != [
        (12, 96), (20, 128),
        (32, 160), (32, 224),
    ]:
        raise ValueError("CONVERGENCE_LEVELS_CHANGED")

    last = levels[-1]
    n = last["truncation"]

    coeff = np.array(last["m_coefficients"])
    b = np.array(last["b_coefficients_normalized"])
    q = np.array(last["q_coefficients_normalized"])

    mu, omega = np.polynomial.legendre.leggauss(320)

    P = np.column_stack([
        eval_legendre(l, mu)
        for l in range(n + 1)
    ])

    value = P @ coeff
    area = 2 * math.pi * R**2
    weights = (
        4 * math.pi * R**2
        / (2*np.arange(n + 1) + 1)
    )

    ell_array = np.arange(n + 1)
    a = (
        r + kappa * ell_array * (ell_array + 1)
        / R**2
    ).astype(float)

    max_x = 0.0
    max_y = 0.0

    for l in range(1, n + 1):
        A = R/(2*l + 1)
        M = R/l + R/(l + 1)
        D = H + M - g*g/(K + A)

        a[l] -= chi*chi/D

        max_x = max(
            max_x,
            abs((K + A)*q[l-1] + g*b[l-1]),
        )

        max_y = max(
            max_y,
            abs(
                (H + M)*b[l-1]
                + g*q[l-1]
                - chi*coeff[l]
            ),
        )

    equation = (
        a*coeff
        + area
        * (P.T @ (
            omega * (
                -beta*value**3 + gamma*value**5
            )
        ))
        / weights
    )

    max_material = float(np.max(abs(equation)))

    if max(max_x, max_y, max_material) > 1e-9:
        raise ValueError("INDEPENDENT_ONSHELL_EQUATION_FAIL")

    second = (
        -3*beta*value**2 + 5*gamma*value**4
    )

    hessian = (
        np.diag(weights*a)
        + area*(P.T*(omega*second))@P
    )

    hessian = (hessian + hessian.T)/2
    hessian /= np.sqrt(np.outer(weights, weights))

    min_eigen = float(np.linalg.eigvalsh(hessian)[0])
    min_off = float(np.min(a))

    if (
        min_eigen <= 0
        or min_off <= 0
        or abs(
            min_eigen -
            last["min_full_static_hessian_eigenvalue"]
        ) > 3e-9
        or abs(
            min_off -
            last["min_offstate_hessian_eigenvalue"]
        ) > 3e-9
    ):
        raise ValueError("INDEPENDENT_STATIC_HESSIAN_FAIL")

    def energy(x):
        m = P @ x
        return float(
            0.5*np.dot(weights*a, x*x)
            + area*np.dot(
                omega,
                -beta*m**4/4 + gamma*m**6/6,
            )
        )

    E = energy(coeff)

    if abs(
        E - last["on_state_energy_over_B0_squared"]
    ) > 1e-9:
        raise ValueError("ENERGY_MODEL_DISAGREEMENT")

    max_fd = 0.0

    for l in (0, 1, 3, 5, 11, 20, 32):
        dx = np.zeros(n + 1)
        dx[l] = 1.5e-5

        derivative = (
            energy(coeff + dx) -
            energy(coeff - dx)
        ) / (3e-5)

        max_fd = max(max_fd, abs(derivative))

    if max_fd > 2e-7:
        raise ValueError("ENERGY_VARIATION_FAIL")

    # Independently reconstruct azimuthal Maxwell jump.
    x = np.linspace(-0.99999, 0.99999, 389)

    material = np.zeros_like(x)
    reciprocal = np.zeros_like(x)
    bulk = np.zeros_like(x)

    for l in range(1, n + 1):
        derivative = (
            l * (
                eval_legendre(l-1, x)
                - x*eval_legendre(l, x)
            )
            / (1-x*x)
        )

        gradient = (
            -np.sqrt(1-x*x)*derivative
        )

        M = R/l + R/(l+1)

        material += (
            chi*coeff[l]*gradient
        )

        reciprocal -= (
            H*b[l-1] + g*q[l-1]
        ) * gradient

        bulk += M*b[l-1]*gradient

    max_jump = float(
        np.max(abs(material+reciprocal-bulk))
        / max(1.0, np.max(abs(bulk)))
    )

    if max_jump > 3e-11:
        raise ValueError(
            "INDEPENDENT_CURRENT_JUMP_FAIL"
        )

    target = np.array([
        row["b_mode"]
        for row in parent["modes"]
    ])

    target /= target[0]

    w12 = weights[1:13]

    mismatch = math.sqrt(float(
        np.dot(w12, (b[:12]-target)**2)
        / np.dot(w12, target**2)
    ))

    if abs(
        mismatch -
        science["target_mismatch_relative_surface_L2"]
    ) > 1e-11:
        raise ValueError("SOURCE_TARGET_MISMATCH_DRIFT")

    # Independently force the exact R3B target into
    # the new material Euler-Lagrange equation.
    forced = np.zeros(n + 1)

    for l in range(1, 13):
        D = (
            H + R/l + R/(l+1)
            - g*g/(K+R/(2*l+1))
        )
        forced[l] = D*target[l-1]/chi

    forced_field = P @ forced

    forced_equation = (
        a*forced
        + area
        * (P.T @ (
            omega * (
                -beta*forced_field**3
                + gamma*forced_field**5
            )
        ))
        / weights
    )

    forced_residual = float(
        np.max(abs(forced_equation))
    )

    if abs(
        forced_residual -
        science[
            "forced_R3B_target_material_Euler_Lagrange_max_residual"
        ]
    ) > 1e-10:
        raise ValueError(
            "FORCED_TARGET_EQUATION_DRIFT"
        )

    barrier = science["metastable_source_switching"]

    if not (
        0 <
        barrier["on_energy_over_B0_squared"] <
        barrier["saddle_energy_over_B0_squared"]
    ):
        raise ValueError("SWITCHING_BARRIER_FAIL")

    for earlier in levels[:3]:
        if abs(
            coeff[1] - earlier["m_coefficients"][1]
        ) > 1e-6:
            raise ValueError("SPECTRAL_CONVERGENCE_FAIL")

    if abs(
        levels[-1]["on_state_energy_over_B0_squared"]
        - levels[-2]["on_state_energy_over_B0_squared"]
    ) > 1e-8:
        raise ValueError("QUADRATURE_CONVERGENCE_FAIL")

    if not all(science["controls"].values()):
        raise ValueError("NEGATIVE_CONTROL_FAILURE")

    return {
        "status":
            "PASS_INDEPENDENT_CONDITIONAL_SOURCE_ACTION_NOT_GRAVITY",
        "independently_verified_modes": n,
        "max_two_sided_kernel_error": max_boundary,
        "max_X_equation_residual": max_x,
        "max_Y_equation_residual": max_y,
        "max_material_on_shell_residual": max_material,
        "min_full_static_hessian_eigenvalue": min_eigen,
        "min_offstate_static_hessian_eigenvalue": min_off,
        "energy_finite_difference_max_slope": max_fd,
        "current_jump_relative_residual": max_jump,
        "R3B_12_mode_relative_L2_mismatch": mismatch,
        "R3B_forced_material_equation_residual":
            forced_residual,
        "canonical_onminusoff_energy_per_B0_squared": E,
        "no_gravity_or_SI_certification": True,
        "physical_survivors": 0,
    }
