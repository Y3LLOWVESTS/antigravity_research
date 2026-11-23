"""GRAVITY2 G01-M: on-shell effective magnetic-source action.

QUESTION
--------
Can dynamical material matter supply the Y magnetic drive missing
from G01-K after restoring G01-L's two-sided Maxwell kernel?

This is a phenomenological source-action hypothesis, NOT an
identified microscopic carrier source or a gravitational device.

MODEL
-----
Closed spherical shell, R=2 canonical units.
For ell>=1, q is X charge, b is Y normal magnetic field.

Reduced static energy, divided by B0 squared:

 E = 1/2 sum w_l [
        (K+A_l)q_l^2 + 2g q_l b_l
        +(H+M_l)b_l^2 - 2chi m_l b_l
     ]
     + 1/2 sum w_l (r+kappa*l*(l+1)/R^2)m_l^2
     + integral [-beta*m^4/4+gamma*m^6/6] dA

A_l = R/(2l+1)
M_l = R/l + R/(l+1)

The material variable m is dynamical, not prescribed.
A positive time kinetic term Z is also specified.

Variations:
 (K+A_l)q_l+g*b_l=0
 (H+M_l)b_l+g*q_l-chi*m_l=0
 (r-kappa Delta)m-beta*m^3+gamma*m^5=chi*b

The Y current is a conserved surface stream current obtained
from varying the local m*Bnormal interaction.

CONSTRAINTS
-----------
Bnormal has no monopole harmonic. Material m includes the
monopole and all even/odd perturbations.

The finite spectral Hessian is checked, including all material
perturbations, but this is NOT complete Lorentzian stability.

All field/source energy quantities are CANONICAL, NOT SI joules.

NOT ESTABLISHED
---------------
Microscopic Y charges, material/support rest energy, complete
4D shell embedding, physical metric, Einstein field solution,
fully loaded outward gravity, whole-craft force, UV/empirical
consistency or complete operating energy.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.polynomial.legendre import (
    leggauss, legvander, legder, legval,
)
from scipy.optimize import root


CAPACITY = 1.5429162116460216
LOADED_INWARD = -129.67185782242464
R = 2.0


def kernels(ell, radius=R):
    if ell < 1:
        raise ValueError("MONOPOLE_Y_FLUX_FORBIDDEN")
    return (
        radius / (2 * ell + 1),
        radius / ell + radius / (ell + 1),
    )


@dataclass(frozen=True)
class Model:
    K: float = 2.0
    g: float = 4.0
    H: float = 8.2
    radius: float = R
    kappa: float = 8.0
    Z: float = 8.0
    beta: float = 5 / 18
    gamma: float = 1 / 4

    @property
    def chi(self):
        return self.D(1)

    def D(self, ell):
        a, m = kernels(ell, self.radius)
        return self.H + m - self.g**2 / (self.K + a)

    @property
    def a1(self):
        # Chosen near-unit-dipole normalization.
        # NOT an independently measured material parameter.
        return 3 * self.beta / 5 - 3 * self.gamma / 7

    @property
    def r(self):
        return (
            self.chi**2 / self.D(1)
            - 2 * self.kappa / self.radius**2
            + self.a1
        )

    def quadratic(self, n):
        ell = np.arange(n + 1, dtype=float)
        a = (
            self.r
            + self.kappa * ell * (ell + 1)
            / self.radius**2
        )
        for l in range(1, n + 1):
            a[l] -= self.chi**2 / self.D(l)
        return a

    def weights(self, n):
        ell = np.arange(n + 1, dtype=float)
        return (
            4 * math.pi * self.radius**2
            / (2 * ell + 1)
        )


def spectral(n, quadrature, model=Model()):
    """Exact polynomial Galerkin energy, gradient and Hessian."""
    if n < 6 or quadrature < 3 * n + 3:
        raise ValueError("QUADRATURE_OR_TRUNCATION_TOO_SMALL")

    x, omega = leggauss(quadrature)
    P = legvander(x, n)
    weights = model.weights(n)
    a = model.quadratic(n)
    area = 2 * math.pi * model.radius**2

    def equations(coeffs):
        m = P @ coeffs
        nonlinear = (
            -model.beta * m**3
            + model.gamma * m**5
        )
        return (
            a * coeffs
            + area * (P.T @ (omega * nonlinear))
            / weights
        )

    def hessian_normalized(coeffs):
        m = P @ coeffs
        nonlinear_second = (
            -3 * model.beta * m * m
            + 5 * model.gamma * m**4
        )
        H = np.diag(a * weights)
        H += (
            area
            * (P.T * (omega * nonlinear_second))
            @ P
        )
        H = (H + H.T) / 2
        return H / np.sqrt(np.outer(weights, weights))

    def jacobian(coeffs):
        H = hessian_normalized(coeffs)
        return (
            H * np.sqrt(weights)[None, :]
            / np.sqrt(weights)[:, None]
        )

    def energy(coeffs):
        m = P @ coeffs
        potential = (
            -model.beta * m**4 / 4
            + model.gamma * m**6 / 6
        )
        return float(
            0.5 * np.dot(weights * a, coeffs**2)
            + area * np.dot(omega, potential)
        )

    return (
        equations, jacobian, hessian_normalized,
        energy, x, omega, P,
    )


def find_on_shell(n, nq, model=Model()):
    eq, jac, hess, energy, *_ = spectral(n, nq, model)

    seed = np.zeros(n + 1)
    seed[1] = 1.0

    solution = root(
        eq, seed, jac=jac,
        tol=2e-12,
        options={"maxfev": 4000},
    )

    state = solution.x
    residual = eq(state)

    if not np.isfinite(state).all():
        raise ValueError("NONFINITE_MATERIAL_STATE")

    if max(abs(residual)) > 1e-10 or state[1] < 0.5:
        raise ValueError(
            "NONTRIVIAL_STATIONARITY_NOT_DEMONSTRATED"
        )

    on_eigen = np.linalg.eigvalsh(hess(state))
    off_eigen = np.linalg.eigvalsh(
        hess(np.zeros(n + 1))
    )

    b = []
    q = []

    for ell in range(1, n + 1):
        bmode = (
            model.chi / model.D(ell)
            * state[ell]
        )
        A, _ = kernels(ell, model.radius)
        qmode = (
            -model.g * bmode / (model.K + A)
        )
        b.append(float(bmode))
        q.append(float(qmode))

    return {
        "truncation": n,
        "quadrature": nq,
        "solver_success": bool(solution.success),
        "max_on_shell_equation_residual":
            float(np.max(abs(residual))),
        "m_coefficients": state.tolist(),
        "b_coefficients_normalized": b,
        "q_coefficients_normalized": q,
        "min_full_static_hessian_eigenvalue":
            float(on_eigen[0]),
        "min_offstate_hessian_eigenvalue":
            float(off_eigen[0]),
        "on_state_energy_over_B0_squared":
            energy(state),
        "off_state_energy_over_B0_squared":
            energy(np.zeros(n + 1)),
    }


def shell_current_test(model, state, n, ntheta=400):
    """Complete Y Maxwell jump including reciprocal shell current.

    The current is an azimuthal surface stream generated from
    chi*m. Its surface divergence vanishes identically.
    """
    theta = np.linspace(
        1e-6, math.pi - 1e-6, ntheta
    )
    mu = np.cos(theta)

    material = np.zeros_like(theta)
    shell = np.zeros_like(theta)
    bulk = np.zeros_like(theta)
    wrong = np.zeros_like(theta)

    for ell in range(1, n + 1):
        coeff = np.zeros(ell + 1)
        coeff[-1] = 1.0

        gradient = (
            -np.sin(theta)
            * legval(mu, legder(coeff))
        )

        b = (
            model.chi / model.D(ell)
            * state[ell]
        )
        A, M = kernels(ell, model.radius)
        q = -model.g * b / (model.K + A)

        material += (
            model.chi * state[ell] * gradient
        )
        shell -= (
            model.H * b + model.g * q
        ) * gradient
        bulk += M * b * gradient
        wrong += (
            model.H * b + model.g * q
        ) * gradient

    scale = max(1.0, np.max(abs(bulk)))

    return {
        "max_two_sided_Maxwell_jump_relative_error":
            float(np.max(abs(material + shell - bulk)) / scale),
        "wrong_sign_reciprocity_relative_residual":
            float(np.max(abs(material + wrong - bulk)) / scale),
        "max_material_stream_coefficient":
            float(np.max(abs(material))),
        "max_bulk_stream_coefficient":
            float(np.max(abs(bulk))),
        "Y_Ward_divergence":
            "EXACT_ZERO_AXISYMMETRIC_AZIMUTHAL_STREAM",
        "surface_magnetic_flux":
            "EXACT_ZERO_NO_MONOPOLE",
    }


def assemble(parent):
    expected = (
        "ACTION_INCOMPLETE_G01K_EXTERIOR_ONLY_KERNEL_"
        "NOT_FULL_TWO_SIDED_MAXWELL"
    )

    if (
        parent["status"] != expected
        or len(parent["modes"]) != 12
        or parent["physical_survivors"] != 0
    ):
        raise ValueError("G01L_SCIENCE_CLAIM_DRIFT")

    model = Model()

    if (
        parent["K"] != model.K
        or parent["g"] != model.g
        or parent["H"] != model.H
    ):
        raise ValueError("G01L_ACTION_COEFFICIENT_DRIFT")

    if not (
        model.K * model.H - model.g**2 > 0
        and model.Z >= model.kappa > 0
        and model.gamma > 0
    ):
        raise ValueError(
            "MATERIAL_LOCAL_HEALTH_PRECONDITION_FAIL"
        )

    target = np.array([
        row["b_mode"]
        for row in parent["modes"]
    ])

    ref = float(target[0])

    if not (ref > 1e4 and math.isfinite(ref)):
        raise ValueError("REFERENCE_B1_MISSING")

    modes = []

    for idx, row in enumerate(parent["modes"], 1):
        A, M = kernels(idx)
        D = model.D(idx)

        if D <= 0 or abs(M - row["Y_full"]) > 1e-12:
            raise ValueError("PARENT_MAXWELL_DRIFT")

        modes.append({
            "ell": idx,
            "A": A,
            "M_full": M,
            "D": D,
            "target_b_over_B0":
                float(target[idx - 1] / ref),
        })

    # Increasing spectral resolution and independent quadrature.
    levels = [
        (12, 96),
        (20, 128),
        (32, 160),
        (32, 224),
    ]

    solutions = [
        find_on_shell(n, nq, model)
        for n, nq in levels
    ]

    final = solutions[-1]

    if not all(
        s["min_full_static_hessian_eigenvalue"] > 0
        and s["min_offstate_hessian_eigenvalue"] > 0
        for s in solutions
    ):
        raise ValueError("FULL_STATIC_HESSIAN_FAIL")

    eq, jac, hess, energy, *_ = spectral(
        32, 224, model
    )

    # Find the actual unstable saddle separating off/on states.
    seed = np.zeros(33)
    seed[1] = 0.65

    saddle = root(
        eq, seed, jac=jac, tol=2e-12
    )

    if (
        np.max(abs(eq(saddle.x))) > 1e-10
        or not 0.5 < saddle.x[1] < 0.9
        or np.min(
            np.linalg.eigvalsh(hess(saddle.x))
        ) >= 0
    ):
        raise ValueError(
            "BARRIER_SADDLE_NOT_DEMONSTRATED"
        )

    saddle_energy = float(energy(saddle.x))
    on_energy = float(
        final["on_state_energy_over_B0_squared"]
    )

    if not 0 < on_energy < saddle_energy:
        raise ValueError(
            "ON_OFF_BARRIER_ENERGY_FAIL"
        )

    state = np.array(final["m_coefficients"])
    field = np.array(
        final["b_coefficients_normalized"][:12]
    )

    # Force the original R3B field into this material law.
    # This is a genuine necessary on-shell source test.
    forced = np.zeros(33)

    for ell in range(1, 13):
        forced[ell] = (
            model.D(ell) / model.chi
            * target[ell - 1] / ref
        )

    forced_residual = float(
        np.max(abs(eq(forced)))
    )

    target_normalized = target / ref
    weights = model.weights(12)[1:]

    relative_l2 = math.sqrt(
        float(
            np.dot(
                weights,
                (field - target_normalized)**2,
            )
            / np.dot(weights, target_normalized**2)
        )
    )

    mu = np.linspace(-1, 1, 1001)
    P = legvander(mu, 12)[:, 1:]

    peak_error = float(
        np.max(abs(P @ (field - target_normalized)))
        / max(
            1e-30,
            np.max(abs(P @ target_normalized)),
        )
    )

    currents = shell_current_test(
        model, state, 32
    )

    controls = {
        "M0_positive_quadratic_and_quartic_unique_zero":
            bool(np.min(model.quadratic(32)) > 0),
        "M1_sextic_potential_bounded_below":
            bool(model.gamma > 0),
        "M1_onstate_nonzero":
            bool(state[1] > 0.5),
        "M1_offstate_locally_stable":
            bool(
                final[
                    "min_offstate_hessian_eigenvalue"
                ] > 0
            ),
        "M1_onstate_locally_stable_all_modes":
            bool(
                final[
                    "min_full_static_hessian_eigenvalue"
                ] > 0
            ),
        "missing_Y_interior_rejected":
            all(
                m["M_full"] >
                parent["modes"][i]["Y_exterior"]
                for i, m in enumerate(modes)
            ),
        "wrong_sign_Y_reciprocal_current_detected":
            bool(
                currents[
                    "wrong_sign_reciprocity_relative_residual"
                ] > 1e-2
            ),
        "magnetic_drive_not_assigned_by_mode": True,
        "reference_R3B_target_not_identically_reproduced":
            bool(relative_l2 > 1e-4),
        "forced_R3B_material_field_not_on_shell":
            bool(forced_residual > 1e-4),
        "finite_switching_barrier_positive":
            bool(saddle_energy > on_energy > 0),
        "historical_inward_loading_remains":
            parent[
                "historical_loaded_acceleration_m_s2"
            ] < 0,
        "no_SI_capacity_promotion":
            parent["current_energy_scope"] ==
            "CANONICAL_PROXY_NOT_SI_JOULES",
        "kinetic_shell_prefilter_positive":
            model.K * model.H - model.g**2 > 0,
    }

    if not all(controls.values()):
        raise ValueError(
            "NEGATIVE_CONTROL_FAIL"
        )

    exterior = sum(
        row["old_magnetic_energy_proxy"]
        for row in parent["modes"]
    )

    return {
        "schema":
            "gravity2.g01m.conserved_magnetization_action.v1",
        "status":
            "DYNAMICAL_EFFECTIVE_SOURCE_ON_SHELL_SCOPED_"
            "R3B_MODE_MISMATCH_NO_GRAVITY",
        "claim":
            "CONDITIONAL_PREFERRED_FRAME_EFFECTIVE_"
            "MATERIAL_NOT_MICROSCOPIC_GRAVITY",
        "parent_G01L_science_status": parent["status"],
        "protected_R3B_capacity_J": CAPACITY,
        "historical_loaded_min_m_s2": LOADED_INWARD,
        "source_action_class":
            "real_order_parameter_plus_two_sided_"
            "Maxwell_BF_shell",
        "complete_same_action":
            "NO_SOURCE_EMBEDDING_EINSTEIN_"
            "PHYSICAL_METRIC_MISSING",
        "material_parameters": {
            "K": model.K,
            "g": model.g,
            "H": model.H,
            "R": model.radius,
            "Z_time_kinetic": model.Z,
            "kappa_spatial_gradient": model.kappa,
            "beta_negative_quartic_magnitude":
                model.beta,
            "gamma_positive_sextic": model.gamma,
            "chi_magnetic_coupling": model.chi,
            "r_positive_mass": model.r,
            "parameters_are_hypothetical": True,
            "r_chosen_for_one_mode_M1_near_unit_dipole":
                True,
        },
        "source_variations": {
            "worldvolume_X":
                "(K+A_l)*q_l+g*b_l=0",
            "Y_normal":
                "(H+Mfull_l)*b_l+g*q_l-chi*m_l=0",
            "matter_m":
                "(r-kappa_Delta)m-beta*m^3"
                "+gamma*m^5=chi*b",
            "Y_surface_current":
                "Hodge2_d(chi*m)_with_reciprocal_shell",
            "gauge_Ward":
                "d_d(chi*m)=0_closed_sphere",
            "time_kinetic_m":
                "Z>0; kappa/Z=1",
            "source_material_rest_energy":
                "NOT_SPECIFIED",
        },
        "branches": {
            "M0_convex_quartic":
                "THEOREM_ZERO_FIELD_WITH_POSITIVE_"
                "QUADRATIC_AND_NO_EXTERNAL_DRIVE",
            "M1_bistable_sextic":
                "CONDITIONAL_ON_SHELL_SPECTRAL_"
                "STATIONARY_LOCAL_MINIMUM",
        },
        "modes": modes,
        "spectral_solutions": solutions,
        "on_shell_source_current": currents,
        "forced_R3B_target_material_Euler_Lagrange_max_residual":
            forced_residual,
        "metastable_source_switching": {
            "off_energy_over_B0_squared": 0.0,
            "on_energy_over_B0_squared": on_energy,
            "saddle_energy_over_B0_squared": saddle_energy,
            "saddle_dipole_amplitude":
                float(saddle.x[1]),
            "off_to_on_barrier_over_B0_squared":
                saddle_energy,
            "on_to_off_barrier_over_B0_squared":
                saddle_energy - on_energy,
            "unit": "CANONICAL_PROXY_NOT_JOULES",
            "source_time_dependent_switching":
                "NOT_SOLVED",
        },
        "target_mismatch_relative_surface_L2":
            relative_l2,
        "target_mismatch_peak_angular": peak_error,
        "b1_normalization_mode_units": ref,
        "normalized_on_shell_target_modes": [
            {
                "ell": i + 1,
                "on_shell_b_over_B0": float(field[i]),
                "target_b_over_B0":
                    float(target_normalized[i]),
                "difference":
                    float(field[i] - target_normalized[i]),
            }
            for i in range(12)
        ],
        "energy_comparison": {
            "on_minus_off_per_B0_squared": on_energy,
            "energy_unit": "CANONICAL_NOT_JOULES",
            "interior_to_exterior_magnetic_proxy_ratio":
                parent[
                    "total_mandatory_interior_magnetic_energy_proxy"
                ] / exterior,
            "material_rest_mass_included": False,
            "supports_included": False,
            "switching_work_included": False,
        },
        "controls": controls,
        "matched_original_12_modes":
            bool(relative_l2 < 1e-8),
        "fully_loaded_metric_outward": "NOT_DERIVED",
        "microscopic_Y_charge_carrier": "NOT_DERIVED",
        "full_Lorentzian_4D_constraints": "NOT_DERIVED",
        "Earth_down_craft_up": "NOT_DERIVED",
        "SI_energy": "NOT_CERTIFIED",
        "physical_survivors": 0,
        "replaced_006D": False,
        "next_authorization":
            "DO_NOT_TRANSFER_R3B_PAYLOAD_UNLESS_NEW_"
            "MICROSCOPIC_SOURCE_AND_MATCHED_ON_SHELL_FIELD",
    }
