"""B17-M3: finite Earth patch in the FROZEN R3B physical metric.

This is a deliberately non-self-consistent external-field control.

The preloaded R3B source is located entirely aboard the spacecraft.
Earth occupies a finite cylindrical volume below the source.

In the prescribed physical metric g_J = exp(2*sigma) g, a first-order
static matter potential for a frozen finite Earth target is

    U(X_e, X_c) = c^2 integral rho_e(x-X_e) sigma(x-X_c) d^3x.

Rigid translations of the Earth and source yield two force derivatives
of this same reduced potential:

    F_Earth = -dU/dX_e
    F_source_anchor = -dU/dX_c.

U depends on X_e-X_c, so the derivatives are equal and opposite.
This is a conditional reduced-action identity, NOT a demonstration
of complete source reaction or spacecraft propulsion.

Dense Earth/air/hull loading, microscopic source work, full gravity,
field momentum, source hardware and total energy are NOT included.

The finite Earth patch cannot be substituted for the whole Earth.
No gravity cancellation or pure-antigravity lift can be certified here.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import math

import numpy as np
from numpy.polynomial.legendre import Legendre, leggauss

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    HBAR_C_EV_M,
    REFERENCE_PORTAL_SCALE_EV,
    SOURCE_RADIUS_M,
)


@dataclass(frozen=True)
class FiniteEarthCylinder:
    radius_m: float = 2.0
    depth_m: float = 1.0
    density_kg_m3: float = 2000.0

    def __post_init__(self):
        for name in ("radius_m", "depth_m", "density_kg_m3"):
            value = getattr(self, name)
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be positive and finite")

    @property
    def mass_kg(self):
        return (
            math.pi
            * self.radius_m**2
            * self.depth_m
            * self.density_kg_m3
        )


def _check_fit(fit):
    amplitudes = np.asarray(fit["coefficients"], dtype=float)
    normalization = float(fit["amplitude_squared_scale"])

    if (
        amplitudes.ndim != 1
        or not amplitudes.size
        or not np.isfinite(amplitudes).all()
        or not math.isfinite(normalization)
        or normalization <= 0
    ):
        raise ValueError("Invalid normalized R3B multipoles")

    return amplitudes, normalization


def sigma_from_fit(fit, rho_m, z_source_relative_m):
    """Vectorized sigma from actual fitted R3B exterior multipoles."""
    amplitudes, normalization = _check_fit(fit)

    rho, z = np.broadcast_arrays(
        np.asarray(rho_m, dtype=float),
        np.asarray(z_source_relative_m, dtype=float),
    )

    if (
        not np.isfinite(rho).all()
        or not np.isfinite(z).all()
        or np.any(rho < 0)
    ):
        raise ValueError("Invalid evaluation coordinates")

    radius = np.hypot(rho, z)

    if np.any(radius < 1.01 * SOURCE_RADIUS_M):
        raise ValueError("Target enters source-fit exclusion region")

    mu = z / radius
    sint = rho / radius

    b_radial = np.zeros_like(radius)
    b_theta = np.zeros_like(radius)

    for ell, amplitude in enumerate(amplitudes, start=1):
        polynomial = Legendre.basis(ell)

        factor = (
            amplitude
            * (SOURCE_RADIUS_M / radius)**(ell + 1)
            / radius
        )

        b_radial += (
            (ell + 1)
            * factor
            * polynomial(mu)
        )

        b_theta += (
            factor
            * sint
            * polynomial.deriv()(mu)
        )

    b_rho = b_radial * sint + b_theta * mu
    b_z = b_radial * mu - b_theta * sint

    return (
        HBAR_C_EV_M**2
        / REFERENCE_PORTAL_SCALE_EV**4
        * normalization
        * (b_rho*b_rho + b_z*b_z)
    )


@lru_cache(maxsize=20)
def _quadrature(order):
    if not isinstance(order, int) or not 4 <= order <= 128:
        raise ValueError("Quadrature order must be 4..128")
    return leggauss(order)


def _patch_nodes(patch, order):
    x, w = _quadrature(order)

    radial = (x + 1) * patch.radius_m / 2
    depth = (x + 1) * patch.depth_m / 2

    radial_weights = w * patch.radius_m / 2
    depth_weights = w * patch.depth_m / 2

    r, d = np.meshgrid(
        radial, depth, indexing="ij"
    )

    volume_weights = (
        2 * math.pi * r
        * radial_weights[:, None]
        * depth_weights[None, :]
    )

    return r, d, volume_weights


def interaction_energy_j(
    fit,
    patch,
    source_center_z_m,
    order=32,
    earth_vertical_shift_m=0.0,
):
    """Frozen Earth coupling energy; NOT complete operational energy."""
    if (
        not math.isfinite(source_center_z_m)
        or not math.isfinite(earth_vertical_shift_m)
    ):
        raise ValueError("Nonfinite world coordinate")

    if (
        source_center_z_m - earth_vertical_shift_m
        <= 1.01 * SOURCE_RADIUS_M
    ):
        raise ValueError("Source/target exterior clearance violated")

    r, depth, weights = _patch_nodes(patch, order)

    relative_z = (
        earth_vertical_shift_m
        - depth
        - source_center_z_m
    )

    sigma = sigma_from_fit(fit, r, relative_z)

    return float(
        patch.density_kg_m3
        * C_LIGHT_M_S**2
        * np.sum(weights * sigma)
    )


def frozen_volume_force_n(
    fit,
    patch,
    source_center_z_m,
    order=32,
    difference_step_m=0.0025,
):
    """Independent volume integration of preloaded Earth acceleration."""
    if (
        source_center_z_m - difference_step_m
        <= 1.01 * SOURCE_RADIUS_M
    ):
        raise ValueError("Too close to exterior validity boundary")

    r, depth, weights = _patch_nodes(patch, order)

    relative_z = -depth - source_center_z_m

    upper = sigma_from_fit(
        fit, r, relative_z + difference_step_m
    )

    lower = sigma_from_fit(
        fit, r, relative_z - difference_step_m
    )

    acceleration_z = (
        -C_LIGHT_M_S**2
        * (upper - lower)
        / (2 * difference_step_m)
    )

    return float(
        patch.density_kg_m3
        * np.sum(weights * acceleration_z)
    )


def conditional_force_pair(
    fit,
    patch,
    source_center_z_m,
    order=32,
    difference_step_m=0.0025,
):
    """Translate Earth/source separately in one frozen interaction action."""
    step = difference_step_m

    if not math.isfinite(step) or step <= 0:
        raise ValueError("Derivative step must be positive and finite")

    earth_plus = interaction_energy_j(
        fit, patch, source_center_z_m, order, step
    )

    earth_minus = interaction_energy_j(
        fit, patch, source_center_z_m, order, -step
    )

    source_plus = interaction_energy_j(
        fit, patch, source_center_z_m + step, order
    )

    source_minus = interaction_energy_j(
        fit, patch, source_center_z_m - step, order
    )

    earth_force = -(earth_plus-earth_minus)/(2*step)
    source_force = -(source_plus-source_minus)/(2*step)

    volume_force = frozen_volume_force_n(
        fit, patch, source_center_z_m, order, step
    )

    scale = max(
        1.0,
        abs(earth_force),
        abs(source_force),
        abs(volume_force),
    )

    return {
        "earth_frozen_force_z_n": float(earth_force),
        "source_anchor_frozen_force_z_n": float(source_force),
        "earth_force_direct_volume_integral_n": float(volume_force),
        "pair_force_relative_residual":
            abs(source_force + earth_force) / scale,
        "volume_vs_energy_derivative_relative_residual":
            abs(volume_force - earth_force) / scale,
        "interaction_energy_j": interaction_energy_j(
            fit, patch, source_center_z_m, order
        ),
        "earth_patch_mass_kg": patch.mass_kg,
        "quadrature_order": order,
        "difference_step_m": step,
        "conditional_reduced_potential_recoil_only": True,
        "source_current_reaction_derived": False,
        "complete_action_reaction_certified": False,
        "whole_craft_field_force_n": None,
        "gravity_cancellation_certified": False,
        "field_only_lift_certified": False,
    }
