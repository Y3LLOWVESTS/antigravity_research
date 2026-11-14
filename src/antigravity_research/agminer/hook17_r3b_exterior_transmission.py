"""B17-M0: R3B exterior-transmission and Earth-facing frozen-field gate.

PURPOSE / SCOPE
---------------
A theorem-first, action-conditional preflight for an onboard source above an
Earth surface, using the actual R3B fitted exterior multipoles. This module
is *not* a fully coupled source/matter/gravity solver.

MODEL
-----
The published reduced portal is g_phys = exp(2*sigma(P)) g, with
P proportional to the mixed F_X *F_Y invariant. In the global mirror sector,
the source-free exterior obeys sigma = (hbar*c)^2*B_fit^2/M^4, after the
original R3B preloaded 1-g normalization. Its frozen low-velocity response
is a_z = -c^2 partial_z sigma, evaluated at points in Earth matter below a
craft-carried source, not for an external torus above a fixed ground device.

TRANSMISSION THEOREM (restricted)
---------------------------------
When both carrier field strengths vanish on an exterior open set, P and its
exterior gradient vanish there. The direct local sigma(P) portal gives ZERO
additional acceleration there. Independent propagating gravitational fields
or mediators are not included in this restricted statement.

GEOMETRY / OBSERVABLES
----------------------
The entire source sphere is onboard: source center is positioned above the
hull bottom. Earth is below z=0; ground contact means hull bottom z=0.
The calculation measures the *unloaded/preloaded response sign* on Earth
surface tracers and altitude decay. It does not integrate Earth's density
into a reciprocal loaded solution or infer force on the craft from an
unloaded tracer. No source current, hull penetration, microscopic carrier
shield, background Earth gravity, or vehicle recoil is assumed.

SOURCE PROVENANCE
-----------------
Multipoles and normalization must be computed afresh from the original R3B
source using reconstruct_a12c_field, fit_exterior_multipoles and
mirror_payload_reconstruction. No arbitrary multipole or target force may be
fed into a promoted result. h=0.05 m is the original anchor grid.

CLAIM CLASSIFICATION
--------------------
CONDITIONAL_PRELOADED_EXTERIOR_GEOMETRY_AND_TRANSMISSION_PREFLIGHT.
Not demonstrated antigravity, physical Earth loading, spacecraft recoil,
external reaction, stable dynamics, or complete energy certification.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from numpy.polynomial.legendre import Legendre

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S, HBAR_C_EV_M, REFERENCE_PORTAL_SCALE_EV, SOURCE_RADIUS_M
)


@dataclass(frozen=True)
class OnboardGeometry:
    """Source-centered spherical preflight; lengths in meters, +z up."""

    hull_bottom_above_ground_m: float = 0.0
    source_bottom_above_hull_bottom_m: float = 1.0
    source_radius_m: float = SOURCE_RADIUS_M

    def __post_init__(self):
        for value in (
            self.hull_bottom_above_ground_m,
            self.source_bottom_above_hull_bottom_m,
            self.source_radius_m,
        ):
            if not math.isfinite(value):
                raise ValueError("Nonfinite craft geometry")
        if (self.hull_bottom_above_ground_m < 0 or
                self.source_bottom_above_hull_bottom_m < 0 or
                self.source_radius_m <= 0):
            raise ValueError("Craft/ground penetration or invalid source radius")
        if abs(self.source_radius_m - SOURCE_RADIUS_M) > 1e-12:
            raise ValueError("This R3B preflight requires original 2m source")

    @property
    def source_center_z_m(self) -> float:
        return (self.hull_bottom_above_ground_m +
                self.source_bottom_above_hull_bottom_m + self.source_radius_m)

    @property
    def source_support_to_earth_gap_m(self) -> float:
        return self.hull_bottom_above_ground_m + self.source_bottom_above_hull_bottom_m


def local_confined_portal_gate(*, exterior_fx_zero: bool,
                               exterior_fy_zero: bool) -> dict:
    """Exact local support theorem; no invented independent metric propagator."""
    both_zero = bool(exterior_fx_zero and exterior_fy_zero)
    return {
        "exterior_both_carriers_zero": both_zero,
        "direct_local_P_and_gradient_zero_proven": both_zero,
        "direct_local_portal_transmits": False if both_zero else None,
        "independent_gravity_or_mediator_channel_evaluated": False,
        "actual_exterior_carrier_source_realized": False,
    }


def fitted_b_field(amplitudes: np.ndarray, radial_m: float,
                   relative_z_m: float, radius_m: float = SOURCE_RADIUS_M):
    """Evaluate R3B source-free fitted B=(B_rho,B_z) at exterior points."""
    amplitudes = np.asarray(amplitudes, dtype=float)
    if amplitudes.ndim != 1 or amplitudes.size < 1 or not np.isfinite(amplitudes).all():
        raise ValueError("Finite R3B multipole coefficients required")
    if not all(map(math.isfinite, (radial_m, relative_z_m, radius_m))):
        raise ValueError("Nonfinite evaluation coordinates")
    if radial_m < 0 or radius_m <= 0:
        raise ValueError("Invalid radius")
    r = math.hypot(radial_m, relative_z_m)
    if r < 1.01 * radius_m:
        raise ValueError("Fitted multipoles are valid only outside source sphere")
    mu = relative_z_m / r
    sint = radial_m / r
    b_r = 0.0
    b_t = 0.0
    for ell, amplitude in enumerate(amplitudes, start=1):
        p = Legendre.basis(ell)
        factor = float(amplitude) * (radius_m / r)**(ell+1) / r
        b_r += (ell+1) * factor * float(p(mu))
        b_t += factor * sint * float(p.deriv()(mu))
    return b_r * sint + b_t * mu, b_r * mu - b_t * sint


def frozen_sigma(amplitudes: np.ndarray, rho_m: float, z_relative_m: float,
                 amplitude_squared_scale: float) -> float:
    """Preloaded mirror sigma. No loaded-Earth field solution is implied."""
    if not math.isfinite(amplitude_squared_scale) or amplitude_squared_scale <= 0:
        raise ValueError("Invalid R3B normalization")
    br, bz = fitted_b_field(amplitudes, rho_m, z_relative_m)
    return (HBAR_C_EV_M**2 / REFERENCE_PORTAL_SCALE_EV**4
            * amplitude_squared_scale * (br*br + bz*bz))


def frozen_earth_tracer_accel(amplitudes: np.ndarray, geometry: OnboardGeometry,
                             rho_m: float, earth_depth_m: float,
                             amplitude_squared_scale: float,
                             difference_step_m: float = 0.0025) -> float:
    """Earth-facing *unloaded* tracer a_z [m/s²]; negative means Earth-down."""
    if (not math.isfinite(earth_depth_m) or earth_depth_m < 0 or
            not math.isfinite(difference_step_m) or difference_step_m <= 0):
        raise ValueError("Invalid Earth depth or derivative step")
    z_rel = -earth_depth_m - geometry.source_center_z_m
    upper = frozen_sigma(amplitudes, rho_m, z_rel + difference_step_m,
                         amplitude_squared_scale)
    lower = frozen_sigma(amplitudes, rho_m, z_rel - difference_step_m,
                         amplitude_squared_scale)
    return -C_LIGHT_M_S**2 * (upper - lower) / (2 * difference_step_m)


def normalized_r3b_fit(h_m: float = 0.05):
    """Reuse only the source code that produced the R3B benchmark."""
    from .hook17_fdual_f_global_mirror_prefight import (
        reconstruct_a12c_field, fit_exterior_multipoles,
        mirror_global_energy_gate, mirror_payload_reconstruction,
        PRIMARY_FIT_RADIUS_M, PRIMARY_LMAX,
    )
    field = reconstruct_a12c_field(h_m)
    fit = fit_exterior_multipoles(field, PRIMARY_FIT_RADIUS_M, PRIMARY_LMAX)
    energy = mirror_global_energy_gate(field, fit)
    payload = mirror_payload_reconstruction(field, fit, energy)
    normalization = float(payload["amplitude_squared_normalization_to_1g"])
    return {
        "grid_m": float(h_m),
        "coefficients": np.asarray(fit["boundary_amplitudes"], dtype=float),
        "amplitude_squared_scale": normalization,
        "preloaded_energy_j": float(payload["normalized_mixed_global_field_energy_j"]),
        "fitted_exterior_rms": float(fit["relative_rms_field_residual"]),
    }
