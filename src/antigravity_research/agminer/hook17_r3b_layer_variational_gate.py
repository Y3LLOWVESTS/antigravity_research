"""B17-M2: exact one-dimensional mixed-U(1) slab-energy gate.

The R3X1 Lorentzian static Lagrangian is

L = 0.5*(E_X^2+E_Y^2-B_X^2-B_Y^2)
    + theta*(E_X.B_Y+E_Y.B_X).

For an axial 1D configuration, with no free bulk or sheet sources,
B_Y,z = B and D_X,z = D remain constant through the layers:

    E_X,z = D - theta*B.

For prescribed constant theta, the cross-topological term cancels
from the canonical carrier Hamiltonian:

    u_carrier = 0.5*(B^2+E^2).

Given fixed B, thicknesses L_i, and theta_i,

    U/A = k/2 * sum L_i*[B^2+(D-theta_i*B)^2].

The exact optimal source-side displacement is

    D_star = B*(sum L_i*theta_i)/(sum L_i).

This permits source-side adjustment instead of artificially forcing
the original vacuum electric field to remain unchanged.

CRITICAL SCOPE:
This is a local 1D, frozen-density, fixed-normal-B calculation.
The source and all its hardware are onboard, but microscopic source
currents, hull loading, complete Earth fields, matter energy,
gravity, mechanical reaction, stability and spacecraft motion
are NOT solved. Energy is per area, not an operational energy.
A local R3B axial field sample is not a global planar field.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np

from .hook17_concurrent_u1_fieldstrength_metric import (
    EV_J,
    HBAR_C_EV_M,
)

from .hook17_r3b_earth_interface import theta_for_density

from .hook17_r3b_exterior_transmission import (
    OnboardGeometry,
    fitted_b_field,
    normalized_r3b_fit,
)

CANONICAL_K_J_PER_M3_PER_FIELD2 = EV_J / HBAR_C_EV_M


@dataclass(frozen=True)
class Layer:
    name: str
    thickness_m: float
    density_kg_m3: float

    def __post_init__(self):
        if not self.name:
            raise ValueError("Layer name required")

        if not math.isfinite(self.thickness_m) or self.thickness_m <= 0:
            raise ValueError("Finite positive thickness required")

        if not math.isfinite(self.density_kg_m3) or self.density_kg_m3 < 0:
            raise ValueError("Nonnegative finite density required")


def axial_slab_variational(
    layers: Sequence[Layer],
    b_normal: float,
    portal_scale_ev: float,
    fixed_source_e_normal: float | None = None,
) -> dict:
    """Optimize D while preserving exact 1D source-free interface laws."""

    if len(layers) < 2:
        raise ValueError("At least two layers required")

    if not math.isfinite(b_normal):
        raise ValueError("Finite B required")

    if not math.isfinite(portal_scale_ev) or portal_scale_ev <= 0:
        raise ValueError("Invalid portal scale")

    lengths = np.array(
        [layer.thickness_m for layer in layers],
        dtype=float,
    )

    theta = np.array(
        [
            theta_for_density(layer.density_kg_m3, portal_scale_ev)
            for layer in layers
        ],
        dtype=float,
    )

    if not np.isfinite(theta).all():
        raise ValueError("Nonfinite theta")

    average_theta = float(
        np.dot(lengths, theta) / np.sum(lengths)
    )

    d_optimal = b_normal * average_theta

    def evaluate(d):
        electric = d - theta*b_normal

        density = (
            0.5
            * CANONICAL_K_J_PER_M3_PER_FIELD2
            * (electric**2 + b_normal**2)
        )

        energy_by_layer = lengths*density

        return {
            "source_displacement": float(d),
            "e_normal_per_layer": [
                float(value) for value in electric
            ],
            "carrier_energy_j_per_m2":
                float(np.sum(energy_by_layer)),
            "carrier_energy_by_layer_j_per_m2": [
                float(value) for value in energy_by_layer
            ],
            "absolute_d_continuity_residual": float(
                np.max(np.abs(
                    electric + theta*b_normal - d
                ))
            ),
        }

    optimal = evaluate(d_optimal)

    analytic_energy = (
        0.5
        * CANONICAL_K_J_PER_M3_PER_FIELD2
        * b_normal**2
        * (
            float(np.sum(lengths))
            + float(np.dot(
                lengths,
                (theta-average_theta)**2,
            ))
        )
    )

    if not math.isclose(
        optimal["carrier_energy_j_per_m2"],
        analytic_energy,
        rel_tol=1e-12,
        abs_tol=1e-6,
    ):
        raise ArithmeticError("Variational identity failed")

    result = {
        "layers": [
            {
                "name": layer.name,
                "thickness_m": layer.thickness_m,
                "density_kg_m3": layer.density_kg_m3,
                "theta": float(t),
            }
            for layer, t in zip(layers, theta)
        ],
        "b_normal": float(b_normal),
        "optimal": optimal,
        "analytic_optimum_j_per_m2": analytic_energy,
        "nonzero_B_held_through_layers": True,
        "free_bulk_or_interface_sheet_sources": False,
        "whole_craft_force_n": None,
    }

    if fixed_source_e_normal is not None:
        if not math.isfinite(fixed_source_e_normal):
            raise ValueError("Nonfinite fixed electric field")

        fixed_d = (
            fixed_source_e_normal
            + theta[0]*b_normal
        )

        result["fixed_source"] = evaluate(fixed_d)

    return result


def stationary_nosource_planar_localization_gate(
    left_asymptotic_vanishes: bool,
    right_asymptotic_vanishes: bool,
) -> dict:
    """Restricted planar source-free localization theorem.

    Static 1D Maxwell fields preserve D_n, B_n, E_t and H_t.
    If the field vanishes at a regular asymptotic end, all such
    constants vanish. This does not constrain localized 3D sources.
    """

    return {
        "source_free_planar_fullline_field_zero_proven":
            bool(
                left_asymptotic_vanishes
                or right_asymptotic_vanishes
            ),
        "finite_3d_onboard_source_ruled_out": False,
        "physical_3d_earth_response_derived": False,
    }


def physical_r3b_axial_b(
    grid_m: float,
    clearance_m: float = 0.0,
) -> dict:
    """Obtain normalized R3B axial B from its actual multipole fit."""

    geometry = OnboardGeometry(
        hull_bottom_above_ground_m=clearance_m
    )

    fit = normalized_r3b_fit(grid_m)

    br, bz = fitted_b_field(
        fit["coefficients"],
        0.0,
        -geometry.source_center_z_m,
    )

    if abs(br) > 1e-9*max(1.0, abs(bz)):
        raise ArithmeticError("Axis field is not axial")

    b_normalized = (
        bz
        * math.sqrt(fit["amplitude_squared_scale"])
    )

    return {
        "grid_m": grid_m,
        "clearance_m": clearance_m,
        "fitted_normal_b_r3b_units": float(b_normalized),
        "r3b_preloaded_energy_j": fit["preloaded_energy_j"],
        "r3b_fit_rms": fit["fitted_exterior_rms"],
    }
