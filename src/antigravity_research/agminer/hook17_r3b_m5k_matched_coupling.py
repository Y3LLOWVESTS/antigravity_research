"""ALPHA-1R6 / B17-M5K: matched-source coupled-field preflight.

PURPOSE
-------
Deposit the same smooth, neutral, axisymmetric M5I continuum source
onto both scalar and azimuthal R3B operator meshes, then solve the
unchanged corrected Lorentzian carrier equations.

SOURCE DISCRETIZATION
---------------------
The electric RHS j_phi represents a scalar charge-density source.
The magnetic RHS j_a represents an azimuthal current source.

Each native RHS is obtained from an actual cylindrical dual-cell
integral divided by the operator's diagonal source-pairing measure:

    scalar: 2*pi*h**2*w_phi, axis weight w_phi[0] = h/8
    vector: 2*pi*h**2*w_a, where w_a = r at interior nodes.

This is a numerical source adapter, not a microscopic source action.
The fixed 1e6 native amplitude is an artificial numerical control,
used identically on both grids. It is not an SI source calibration.

SCIENTIFIC LIMITATIONS
----------------------
The stationary source satisfies analytical current continuity.
No dynamical matter Ward identity, complete gravitational action,
exterior metric transmission, source creation cost, spacecraft
reaction, or complete device energy is derived here.

Historical R3B target arrays remain in the mesh wrapper for
compatibility, but the new RHS is not fitted to those targets.
Zero-RHS and linear scaling controls must be evaluated separately.
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from numpy.polynomial.legendre import leggauss

from .hook17_r3b_m5i_continuum_source import (
    SourceSpec,
    continuum_current,
    reference_moments,
)

BRANCH = "032H17A12D1R3X3B17-ALPHA1R6-M5K"
NATIVE_TEST_AMPLITUDE = 1.0e6


def _dual_integrate(spec, r_nodes, z_nodes, h, order):
    """Integrate charge, azimuthal current and moments over dual cells."""
    r_nodes = np.asarray(r_nodes, dtype=float)
    z_nodes = np.asarray(z_nodes, dtype=float)

    if order not in (2, 4, 6) or h <= 0:
        raise ValueError("Invalid dual-cell quadrature")

    if (
        np.any(r_nodes < 0)
        or not np.isfinite(r_nodes).all()
        or not np.isfinite(z_nodes).all()
    ):
        raise ValueError("Invalid physical node coordinates")

    low_r = np.maximum(0.0, r_nodes - h / 2)
    high_r = r_nodes + h / 2

    dr = (high_r - low_r) / 2
    mid_r = (high_r + low_r) / 2
    dz = h / 2

    nodes, weights = leggauss(order)
    shape = (len(z_nodes), len(r_nodes))

    charge = np.zeros(shape)
    current = np.zeros(shape)
    electric_dipole = 0.0
    magnetic_dipole = 0.0

    for i, x in enumerate(nodes):
        r = (mid_r + dr * x)[None, :]
        wr = dr[None, :] * weights[i]

        for j, y in enumerate(nodes):
            z = (z_nodes + dz * y)[:, None]
            wz = dz * weights[j]

            rho_e, current_phi = continuum_current(
                r, z, spec
            )

            d_volume = 2 * math.pi * r * wr * wz

            dq = rho_e * d_volume
            dj = current_phi * d_volume

            charge += dq
            current += dj

            electric_dipole += float(
                np.sum(z * dq)
            )

            magnetic_dipole += float(
                np.sum(0.5 * r * dj)
            )

    return {
        "charge_cells": charge,
        "current_cells": current,
        "net_charge": float(charge.sum()),
        "absolute_charge": float(
            np.abs(charge).sum()
        ),
        "electric_dipole": electric_dipole,
        "magnetic_dipole": magnetic_dipole,
    }


def build_matched_source(
    base,
    spec=SourceSpec(),
    order=6,
    amplitude=NATIVE_TEST_AMPLITUDE,
):
    """Create two R3B-native RHS vectors from one continuum current."""
    if not math.isfinite(amplitude) or amplitude <= 0:
        raise ValueError("Invalid artificial source amplitude")

    field = base["field"]
    ops = base["operators"]
    h = float(field["h"])

    if h not in (0.25, 0.2):
        raise ValueError("Unregistered comparison grid")

    rhos = np.asarray(field["rhos"], dtype=float)
    zs = np.asarray(field["zs"], dtype=float)

    if len(zs) - 2 != int(ops["nz_inner"]):
        raise ValueError("Inconsistent axial operator layout")

    scalar_r = rhos[:-1]
    vector_r = rhos[1:-1]
    inner_z = zs[1:-1]

    w_phi = scalar_r.copy()
    w_phi[0] = h / 8.0

    w_a = vector_r.copy()

    scalar = _dual_integrate(
        spec, scalar_r, inner_z, h, order
    )

    vector = _dual_integrate(
        spec, vector_r, inner_z, h, order
    )

    rho_rhs = scalar["charge_cells"] / (
        2 * math.pi * h**2 * w_phi[None, :]
    )

    current_rhs = vector["current_cells"] / (
        2 * math.pi * h**2 * w_a[None, :]
    )

    j_phi = (amplitude * rho_rhs).ravel()
    j_a = (amplitude * current_rhs).ravel()

    if (
        j_phi.size != ops["k_phi"].shape[0]
        or j_a.size != ops["k_a"].shape[0]
    ):
        raise ValueError("Incompatible solver RHS dimensions")

    if not (
        np.isfinite(j_phi).all()
        and np.isfinite(j_a).all()
    ):
        raise ArithmeticError("Nonfinite source vectors")

    neutrality = abs(scalar["net_charge"]) / max(
        scalar["absolute_charge"], 1e-30
    )

    if neutrality > 1e-10:
        raise ArithmeticError(
            "Numerical source charge conservation failed"
        )

    reference = reference_moments(spec)

    electric_error = abs(
        scalar["electric_dipole"]
        - reference["electric_dipole_z_integral"]
    ) / max(
        abs(reference["electric_dipole_z_integral"]),
        1e-30,
    )

    magnetic_error = abs(
        vector["magnetic_dipole"]
        - reference["magnetic_dipole_z_integral"]
    ) / max(
        abs(reference["magnetic_dipole_z_integral"]),
        1e-30,
    )

    audit = {
        "grid_m": h,
        "source_spec": asdict(spec),
        "dual_quadrature_order": order,
        "native_rhs_amplitude": amplitude,
        "rhs_normalization":
            "dual_cylindrical_cell_over_2pi_h2_operator_weight",
        "scalar_rhs_shape": list(rho_rhs.shape),
        "azimuthal_rhs_shape": list(current_rhs.shape),
        "relative_net_charge_residual": neutrality,
        "electric_dipole_integral":
            scalar["electric_dipole"],
        "magnetic_dipole_integral":
            vector["magnetic_dipole"],
        "electric_dipole_reference_relative_error":
            electric_error,
        "magnetic_dipole_reference_relative_error":
            magnetic_error,
        "electric_rhs_nonzero_nodes":
            int(np.count_nonzero(j_phi)),
        "magnetic_rhs_nonzero_nodes":
            int(np.count_nonzero(j_a)),
        "rhs_not_fitted_to_inverse_R3B_target": True,
        "stationary_current_continuity_analytic": True,
        "discrete_dynamical_Ward_certified": False,
        "physical_source_unit_conversion_certified": False,
    }

    return {
        **base,
        "j_phi": j_phi,
        "j_a": j_a,
    }, audit


def solve_loaded_controls(source, scale_ev=21147.0):
    """Solve source-off, unloaded, Earth-loaded and air-only controls."""
    from .hook17_r3b_m4b_sparse_earth_loading import (
        _solve_fixed_sources,
    )

    from .hook17_r3b_m4b4_paired_translation import (
        pair_action,
        shifted_material,
    )

    if not math.isfinite(scale_ev) or scale_ev <= 0:
        raise ValueError("Invalid portal scale")

    amplifier = (scale_ev / 1000.0)**2

    active = {
        **source,
        "j_phi": amplifier * source["j_phi"],
        "j_a": amplifier * source["j_a"],
    }

    beta_earth, _, _ = shifted_material(
        source, 0.0, 0.0, scale_ev,
        earth_present=True,
    )

    beta_air, _, _ = shifted_material(
        source, 0.0, 0.0, scale_ev,
        earth_present=False,
    )

    unloaded = _solve_fixed_sources(
        active, beta_air, fraction=0.0
    )

    earth = _solve_fixed_sources(
        active, beta_earth, fraction=1.0
    )

    air = _solve_fixed_sources(
        active, beta_air, fraction=1.0
    )

    zero_active = {
        **active,
        "j_phi": np.zeros_like(active["j_phi"]),
        "j_a": np.zeros_like(active["j_a"]),
    }

    zero = _solve_fixed_sources(
        zero_active, beta_earth, fraction=1.0
    )

    doubled = {
        **active,
        "j_phi": 2 * active["j_phi"],
        "j_a": 2 * active["j_a"],
    }

    twice = _solve_fixed_sources(
        doubled, beta_air, fraction=0.0
    )

    paired = pair_action(
        source, scale_ev, 0.0, 0.0
    )

    rows = {}

    for name, state in (
        ("unloaded", unloaded),
        ("earth_loaded", earth),
        ("earth_free_air_loaded", air),
        ("zero_source", zero),
    ):
        rows[name] = {
            "carrier_field_energy_j":
                float(state["carrier_energy_j"]),
            "relative_solver_residual":
                float(state["residual"]),
            "weighted_operator_reciprocity_defect":
                float(
                    state["relative_weighted_reciprocity"]
                ),
            "max_scalar_potential":
                float(np.max(np.abs(state["phi"]))),
            "max_azimuthal_potential":
                float(np.max(np.abs(state["a"]))),
        }

        if not all(
            math.isfinite(value)
            for value in rows[name].values()
        ):
            raise ArithmeticError(
                f"Nonfinite coupled result: {name}"
            )

    linear_energy_ratio = (
        float(twice["carrier_energy_j"])
        / max(
            float(unloaded["carrier_energy_j"]),
            1e-300,
        )
    )

    interaction = float(
        paired["interaction_action_j"]
    )

    if not math.isfinite(interaction):
        raise ArithmeticError(
            "Nonfinite on-shell interaction diagnostic"
        )

    return {
        "portal_scale_ev": scale_ev,
        "historical_current_amplifier": amplifier,
        "solves": rows,
        "double_RHS_unloaded_energy_ratio":
            linear_energy_ratio,
        "paired_earth_present_action_j":
            float(paired["loaded"]["action_j"]),
        "paired_earth_absent_action_j":
            float(paired["air_only"]["action_j"]),
        "paired_reduced_interaction_action_j":
            interaction,
        "on_shell_action_is_whole_craft_force": False,
        "dynamical_source_action_certified": False,
        "carrier_energy_is_complete_device_energy": False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
    }
