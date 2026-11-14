"""B17-M4A: finite-footprint Earth-interface obstruction.

A radial family of independent 1D vertical field columns, NOT a 2D PDE.

Each column retains the normal R3B fitted B_Y at the air/ground surface
through specified thin layers, without free surface sheets. Electric
D_X is allowed to optimize independently at each radius.

This supplies a conditional minimum carrier-energy cost within the
frozen-normal-B column class, not a universal lower bound or a
self-consistent Earth-loaded field solution.

The physical metric portal is proportional to E_X*B_Y.
Optimizing D need not preserve the original R3B metric response.

Source apparatus remains aboard the spacecraft. Whole-craft force,
microscopic source work and complete energy are not derived.
"""

from __future__ import annotations

from functools import lru_cache
import math

import numpy as np
from numpy.polynomial.legendre import leggauss

from .hook17_r3b_exterior_transmission import fitted_b_field
from .hook17_r3b_earth_interface import theta_for_density
from .hook17_r3b_layer_variational_gate import (
    CANONICAL_K_J_PER_M3_PER_FIELD2 as K,
)


@lru_cache(maxsize=24)
def _legendre(n):
    if not isinstance(n, int) or n < 4 or n > 256:
        raise ValueError("Quadrature order must be 4..256")
    return leggauss(n)


def local_column(
    theta_a,
    theta_b,
    length_a,
    length_b,
    b,
    e_a_fixed=None,
):
    """Exact frozen-B, two-layer, no-free-sheet algebra."""

    values = (theta_a, theta_b, length_a, length_b, b)
    if not all(math.isfinite(float(x)) for x in values):
        raise ValueError("Nonfinite local input")

    if length_a <= 0 or length_b <= 0:
        raise ValueError("Positive thickness required")

    theta_mean = (
        length_a * theta_a + length_b * theta_b
    ) / (length_a + length_b)

    d_optimal = b * theta_mean
    e_a = (theta_mean - theta_a) * b
    e_b = (theta_mean - theta_b) * b

    optimized = K / 2 * (
        length_a * (b*b + e_a*e_a)
        + length_b * (b*b + e_b*e_b)
    )

    result = {
        "optimized_j_per_m2": optimized,
        "optimal_displacement": d_optimal,
        "optimized_metric_ratio_air_to_r3b":
            theta_mean - theta_a,
        "optimized_metric_ratio_ground_to_r3b":
            theta_mean - theta_b,
        "source_electric_jumps_if_original_held":
            abs((theta_b - theta_a) * b),
    }

    if e_a_fixed is not None:
        if not math.isfinite(e_a_fixed):
            raise ValueError("Nonfinite imposed electric field")

        e_b_fixed = (
            e_a_fixed + (theta_a - theta_b) * b
        )

        fixed = K / 2 * (
            length_a * (b*b + e_a_fixed*e_a_fixed)
            + length_b * (b*b + e_b_fixed*e_b_fixed)
        )

        result["fixed_j_per_m2"] = fixed
        result["fixed_metric_ratio_ground_to_r3b"] = (
            e_b_fixed / b if b else None
        )

    return result


def r3b_normal_flux_integral(
    fit,
    radius_m=2.0,
    center_height_m=3.0,
    order=64,
):
    """Compute 2*pi*integral_0^R rho * B_z(rho)^2 dr."""

    if not (
        math.isfinite(radius_m)
        and radius_m > 0
        and math.isfinite(center_height_m)
        and center_height_m >= 2.02
    ):
        raise ValueError("Invalid source geometry")

    nodes, weights = _legendre(order)

    rho = 0.5 * radius_m * (nodes + 1)
    radial_weights = 0.5 * radius_m * weights

    amplitude = math.sqrt(
        float(fit["amplitude_squared_scale"])
    )

    bz = np.array([
        fitted_b_field(
            fit["coefficients"],
            float(r),
            -center_height_m,
        )[1] * amplitude
        for r in rho
    ])

    return float(
        2 * math.pi * np.dot(
            radial_weights,
            rho * bz * bz,
        )
    )


def finite_footprint(
    fit,
    radius_m=2.0,
    clearance_m=0.0,
    portal_scale_ev=1000.0,
    air_depth_m=0.01,
    ground_depth_m=0.01,
    order=64,
    matched_sigma=False,
):
    """Conditional finite-footprint energy for retained normal B.

    matched_sigma rescales the source field by (M/1keV)^2 to
    preserve the original UNLOADED sigma at the new portal scale.

    This does not preserve the response after material matching.
    """

    if not math.isfinite(clearance_m) or clearance_m < 0:
        raise ValueError("Invalid clearance")

    if (
        not math.isfinite(portal_scale_ev)
        or portal_scale_ev <= 0
    ):
        raise ValueError("Invalid portal scale")

    if (
        not math.isfinite(air_depth_m)
        or not math.isfinite(ground_depth_m)
        or air_depth_m <= 0
        or ground_depth_m <= 0
    ):
        raise ValueError("Invalid layer thickness")

    theta_air = theta_for_density(
        1.2, portal_scale_ev
    )
    theta_ground = theta_for_density(
        2000.0, portal_scale_ev
    )

    normal_flux = r3b_normal_flux_integral(
        fit,
        radius_m,
        3.0 + clearance_m,
        order,
    )

    field_factor = (
        (portal_scale_ev / 1000.0)**2
        if matched_sigma else 1.0
    )

    normal_flux *= field_factor**2

    # The exact local cost is quadratic in B. Since layer densities
    # and thicknesses are constant over the disk, the radial integral
    # factors from the local expression.
    unit = local_column(
        theta_air,
        theta_ground,
        air_depth_m,
        ground_depth_m,
        1.0,
        1.0,
    )

    return {
        "radius_m": float(radius_m),
        "clearance_m": float(clearance_m),
        "portal_scale_ev": float(portal_scale_ev),
        "air_depth_m": float(air_depth_m),
        "ground_depth_m": float(ground_depth_m),
        "radial_order": order,
        "normal_flux_square_integral_field2_m2":
            normal_flux,
        "optimized_conditional_carrier_j":
            normal_flux * unit["optimized_j_per_m2"],
        "fixed_conditional_carrier_j":
            normal_flux * unit["fixed_j_per_m2"],
        "optimized_loaded_sigma_over_unloaded_r3b_air":
            unit["optimized_metric_ratio_air_to_r3b"],
        "optimized_loaded_sigma_over_unloaded_r3b_ground":
            unit["optimized_metric_ratio_ground_to_r3b"],
        "fixed_loaded_sigma_over_unloaded_r3b_ground":
            unit["fixed_metric_ratio_ground_to_r3b"],
        "source_relaxed": True,
        "retains_original_metric_response": False,
        "finite_geometry_coupled_solution": False,
        "global_lower_bound_proven": False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
    }
