"""ALPHA-1R8/B17-M5M: normalized carrier action and translation.

The tested source is prescribed, stationary and axisymmetric.
Translate it by evaluating a single continuum current at physical
coordinates, not by interpolating a discrete source vector.

A small mesh-neutrality projection is explicitly audited.
It corrects quadrature error but is NOT a physical source action.
The scalar and azimuthal RHS retain M5K's artificial amplitude.

The converted on-shell functional has reduced-carrier energy units.
Its derivative is NOT certified whole-craft gravitational force.
"""

from __future__ import annotations

import math

import numpy as np
from numpy.polynomial.legendre import leggauss

from .hook17_r3b_m5i_continuum_source import (
    SourceSpec,
    continuum_current,
)
from .hook17_r3b_m5k_matched_coupling import (
    NATIVE_TEST_AMPLITUDE,
    build_matched_source,
)
from .hook17_r3b_m5l_variational_audit import (
    assemble_variational_matrix,
    on_shell_quadratic,
)

BRANCH = "032H17A12D1R3X3B17-ALPHA1R8-M5M"

EV_J = 1.602176634e-19
HBAR_C_EV_M = 1.973269804e-7
PORTAL_SCALE_EV = 21147.0


def carrier_action_conversion_j_per_native(h):
    if not math.isfinite(h) or h <= 0:
        raise ValueError("Invalid grid spacing")

    return (
        2.0 * math.pi * h**2
        * EV_J / HBAR_C_EV_M
    )


def _dual_redeposit(
    spec, radial_nodes, z_nodes, h, zshift, order
):
    if order not in (4, 6) or not math.isfinite(zshift):
        raise ValueError("Invalid quadrature or shift")

    rnodes = np.asarray(radial_nodes, dtype=float)
    znodes = np.asarray(z_nodes, dtype=float)

    rlow = np.maximum(0.0, rnodes - h/2)
    rhigh = rnodes + h/2

    rmid = (rlow + rhigh)/2
    rhalf = (rhigh - rlow)/2

    nodes, weights = leggauss(order)

    shape = (len(znodes), len(rnodes))

    charge = np.zeros(shape)
    compensator = np.zeros(shape)
    current = np.zeros(shape)

    electric_dipole = 0.0
    magnetic_dipole = 0.0
    absolute_charge = 0.0

    for i, xi in enumerate(nodes):
        r = (rmid + rhalf*xi)[None, :]
        wr = rhalf[None, :] * weights[i]

        for j, xj in enumerate(nodes):
            z = (znodes + h/2*xj)[:, None]
            wz = h/2 * weights[j]

            rho_e, j_phi = continuum_current(
                r, z-zshift, spec
            )

            u = (
                (r-spec.radial_center_m)
                /spec.radial_halfwidth_m
            )**2

            v = (
                (z-zshift)
                /spec.axial_halfwidth_m
            )**2

            bump = np.maximum(
                1.0-u-v, 0.0
            )**5

            dv = 2*math.pi*r*wr*wz
            dq = rho_e*dv

            charge += dq
            compensator += bump*dv
            current += j_phi*dv

            electric_dipole += float(
                (z*dq).sum()
            )

            magnetic_dipole += float(
                (0.5*r*j_phi*dv).sum()
            )

            absolute_charge += float(
                np.abs(dq).sum()
            )

    raw_charge = float(charge.sum())
    norm = float(compensator.sum())

    if norm <= 0:
        raise ArithmeticError(
            "Missing compact compensator"
        )

    coefficient = raw_charge/norm

    projected = charge-coefficient*compensator

    return {
        "corrected_charge_cells": projected,
        "current_cells": current,
        "raw_net_charge": raw_charge,
        "raw_relative_net_charge":
            abs(raw_charge)/max(
                absolute_charge, 1e-30
            ),
        "projected_relative_net_charge":
            abs(float(projected.sum()))
            /max(absolute_charge, 1e-30),
        "quadrature_correction_relative":
            abs(coefficient)/max(
                abs(spec.density_amplitude), 1e-30
            ),
        "electric_dipole_before_projection":
            electric_dipole,
        "magnetic_dipole":
            magnetic_dipole,
    }


def redeposit_shifted_source(
    base,
    spec,
    zshift,
    order=6,
    amplitude=NATIVE_TEST_AMPLITUDE,
):
    field = base["field"]
    ops = base["operators"]

    h = float(field["h"])

    if (
        h not in (0.25, 0.2)
        or not math.isfinite(zshift)
        or abs(zshift) > 0.01
    ):
        raise ValueError(
            "Unregistered translation or grid"
        )

    if not math.isfinite(amplitude) or amplitude <= 0:
        raise ValueError("Invalid amplitude")

    rhos = np.asarray(
        field["rhos"], dtype=float
    )

    z = np.asarray(
        field["zs"], dtype=float
    )[1:-1]

    scalar = _dual_redeposit(
        spec,
        rhos[:-1],
        z,
        h,
        zshift,
        order,
    )

    vector = _dual_redeposit(
        spec,
        rhos[1:-1],
        z,
        h,
        zshift,
        order,
    )

    w_phi = rhos[:-1].copy()
    w_phi[0] = h/8

    w_a = rhos[1:-1]

    j_phi = amplitude*(
        scalar["corrected_charge_cells"]
        /(2*math.pi*h*h*w_phi[None, :])
    ).ravel()

    j_a = amplitude*(
        vector["current_cells"]
        /(2*math.pi*h*h*w_a[None, :])
    ).ravel()

    if (
        j_phi.size != ops["k_phi"].shape[0]
        or j_a.size != ops["k_a"].shape[0]
    ):
        raise ValueError("RHS layout mismatch")

    if not (
        np.isfinite(j_phi).all()
        and np.isfinite(j_a).all()
    ):
        raise ArithmeticError("Nonfinite RHS")

    audit = {
        "source_shift_m": float(zshift),
        "raw_relative_net_charge":
            scalar["raw_relative_net_charge"],
        "projected_relative_net_charge":
            scalar["projected_relative_net_charge"],
        "quadrature_correction_relative_to_density_amplitude":
            scalar["quadrature_correction_relative"],
        "electric_dipole_before_projection":
            scalar["electric_dipole_before_projection"],
        "magnetic_dipole":
            vector["magnetic_dipole"],
        "stationary_current_continuity_analytic": True,
        "dynamical_source_Ward_certified": False,
    }

    return {
        **base,
        "j_phi": j_phi,
        "j_a": j_a,
    }, audit


def evaluate_case(
    h, reverse, historical, displacement=0.002
):
    from .hook17_r3b_m4b1_source_recovery import (
        assemble_original_aligned_source,
    )
    from .hook17_r3b_m4b4_paired_translation import (
        shifted_material,
    )
    from .hook17_r3b_m4b_sparse_earth_loading import (
        _solve_fixed_sources,
    )

    if (
        historical.get("branch")
        != "032H17A12D1R3X3B17-ALPHA1R7-M5L"
        or historical.get("h_m") != h
        or historical.get("reverse_magnetic") is not reverse
        or not all(
            historical["diagnostic_gates"].values()
        )
    ):
        raise ValueError("M5L reference mismatch")

    if not 0 < displacement <= 0.002:
        raise ValueError("Invalid translation step")

    spec = SourceSpec(
        azimuthal_current_amplitude=(
            -1.0 if reverse else 1.0
        )
    )

    base = assemble_original_aligned_source(h)

    reference = float(
        historical["M5K_reduced_interaction_action_j"]
    )

    conversion = carrier_action_conversion_j_per_native(h)

    archival_error = abs(
        historical["earth_minus_air_native_functional"]
        * conversion
        - reference
    )

    amplifier = (PORTAL_SCALE_EV/1000)**2

    source_cache = {}
    solve_cache = {}

    def source_at(shift):
        shift = round(float(shift), 12)

        if shift not in source_cache:
            source_cache[shift] = redeposit_shifted_source(
                base, spec, shift
            )

        return source_cache[shift]

    def interaction_at(earth_z, craft_z):
        key = (
            round(float(earth_z), 12),
            round(float(craft_z), 12),
        )

        if key in solve_cache:
            return solve_cache[key]

        moved, source_audit = source_at(key[1])

        active = {
            **moved,
            "j_phi":
                amplifier*moved["j_phi"],
            "j_a":
                amplifier*moved["j_a"],
        }

        values = {}
        energies = {}
        variation_max = 0.0
        asymmetry_max = 0.0

        for name, earth_present in (
            ("earth", True),
            ("air", False),
        ):
            beta, _, _ = shifted_material(
                moved,
                key[0],
                key[1],
                PORTAL_SCALE_EV,
                earth_present=earth_present,
            )

            state = _solve_fixed_sources(
                active, beta, fraction=1.0
            )

            _, H, weights, asymmetry = (
                assemble_variational_matrix(
                    moved["operators"],
                    state["coupling"],
                    moved["field"]["rhos"],
                    h,
                )
            )

            u = np.r_[
                state["phi"][1:-1, :-1].ravel(),
                state["a"][1:-1, 1:-1].ravel(),
            ]

            j = np.r_[
                active["j_phi"],
                active["j_a"],
            ]

            action = on_shell_quadratic(
                u, j, H, weights
            )

            values[name] = (
                action["native_quadratic_functional"]
                * conversion
            )

            energies[name] = float(
                state["carrier_energy_j"]
            )

            variation_max = max(
                variation_max,
                action[
                    "relative_action_variation_residual"
                ],
            )

            asymmetry_max = max(
                asymmetry_max, asymmetry
            )

        result = {
            "interaction_carrier_action_j":
                values["earth"]-values["air"],
            "earth_action_j": values["earth"],
            "air_action_j": values["air"],
            "source_audit": source_audit,
            "carrier_energy_j": energies,
            "maximum_variational_residual":
                variation_max,
            "maximum_matrix_asymmetry":
                asymmetry_max,
        }

        solve_cache[key] = result

        return result

    center = interaction_at(0.0, 0.0)

    zero_shifted, _ = source_at(0.0)

    original, _ = build_matched_source(
        base, spec, order=6
    )

    source_error = max(
        np.linalg.norm(
            zero_shifted[key]-original[key]
        )/max(
            np.linalg.norm(original[key]),
            1.0,
        )
        for key in ("j_phi", "j_a")
    )

    derivatives = {}

    for step in (
        displacement,
        displacement/2,
    ):
        e_plus = interaction_at(
            step, 0.0
        )["interaction_carrier_action_j"]

        e_minus = interaction_at(
            -step, 0.0
        )["interaction_carrier_action_j"]

        c_plus = interaction_at(
            0.0, step
        )["interaction_carrier_action_j"]

        c_minus = interaction_at(
            0.0, -step
        )["interaction_carrier_action_j"]

        common_plus = interaction_at(
            step, step
        )["interaction_carrier_action_j"]

        common_minus = interaction_at(
            -step, -step
        )["interaction_carrier_action_j"]

        earth = (e_plus-e_minus)/(2*step)
        craft = (c_plus-c_minus)/(2*step)

        common = (
            common_plus-common_minus
        )/(2*step)

        derivatives[str(step)] = {
            "earth_only_reduced_action_derivative_j_per_m":
                earth,
            "craft_only_reduced_action_derivative_j_per_m":
                craft,
            "common_shift_reduced_action_derivative_j_per_m":
                common,
            "common_minus_sum_reduced_j_per_m":
                common-earth-craft,
        }

    audits = [
        item[1]
        for item in source_cache.values()
    ]

    max_raw = max(
        row["raw_relative_net_charge"]
        for row in audits
    )

    max_projected = max(
        row["projected_relative_net_charge"]
        for row in audits
    )

    max_correction = max(
        row[
            "quadrature_correction_relative_to_density_amplitude"
        ]
        for row in audits
    )

    max_variation = max(
        row["maximum_variational_residual"]
        for row in solve_cache.values()
    )

    max_asymmetry = max(
        row["maximum_matrix_asymmetry"]
        for row in solve_cache.values()
    )

    steps = list(derivatives.values())

    derivative_difference = {
        name: abs(
            steps[0][name]-steps[1][name]
        )
        for name in (
            "earth_only_reduced_action_derivative_j_per_m",
            "craft_only_reduced_action_derivative_j_per_m",
            "common_shift_reduced_action_derivative_j_per_m",
        )
    }

    center_error = abs(
        center["interaction_carrier_action_j"]
        - reference
    )

    return {
        "branch": BRANCH,
        "grid_m": h,
        "reverse_magnetic": reverse,
        "action_conversion_j_per_native":
            conversion,
        "fixed_native_source_amplitude":
            NATIVE_TEST_AMPLITUDE,
        "center_reduced_carrier_interaction_action_j":
            center["interaction_carrier_action_j"],
        "M5K_reference_reduced_interaction_action_j":
            reference,
        "center_M5K_action_reproduction_abs_error_j":
            center_error,
        "archival_action_unit_conversion_error_j":
            archival_error,
        "zero_shift_RHS_relative_error_vs_M5K":
            source_error,
        "translation_derivatives":
            derivatives,
        "difference_between_two_step_sizes_j_per_m":
            derivative_difference,
        "max_raw_mesh_charge_residual":
            max_raw,
        "max_projected_mesh_charge_residual":
            max_projected,
        "max_mesh_projection_coefficient_relative":
            max_correction,
        "max_fixed_loading_variational_residual":
            max_variation,
        "max_fixed_loading_matrix_asymmetry":
            max_asymmetry,
        "source_translations_evaluated_m":
            sorted(source_cache),
        "evaluation_count": len(solve_cache),
        "diagnostic_gates": {
            "action_unit_conversion_matches_M5K_below_1e_minus_8_j":
                archival_error < 1e-8,
            "zero_shift_source_matches_M5K_below_1e_minus_10":
                bool(source_error < 1e-10),
            "center_action_matches_M5K_within_1e_minus_5_j":
                center_error < 1e-5,
            "projected_charge_below_1e_minus_12":
                max_projected < 1e-12,
            "mesh_correction_coefficient_below_1e_minus_4":
                max_correction < 1e-4,
            "variational_residual_below_1e_minus_8":
                max_variation < 1e-8,
            "matrix_asymmetry_below_1e_minus_9":
                max_asymmetry < 1e-9,
        },
        "mesh_charge_projection_used": True,
        "projection_sensitivity_in_derivatives_excluded":
            False,
        "physical_reciprocity_certified": False,
        "source_dynamical_Ward_certified": False,
        "interface_and_box_convergence_certified":
            False,
        "derivatives_are_complete_mechanical_forces":
            False,
        "exterior_metric_transmission_derived":
            False,
        "Earth_environment_reaction_derived":
            False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
    }
