"""Universal-metric, canonical-RG, and support-geometry helpers for 032V18.

PURPOSE
-------
V17 produced an extremely cheap oblate finite-payload partial corridor but left
three conceptually separate questions open:

1. Does a universal kinetic-conformal physical metric have action-level
   literature provenance?
2. Does a large scalar wavefunction renormalization automatically destroy the
   low-energy response?
3. Can the source morphology be supported by a physically simple positive-
   energy support sector?

This module supplies exact algebraic checks for questions 2 and 3 and an
analytic spherical source expansion used for the support-friendly fallback.

CANONICAL RESCALING
-------------------
For

    L = -(Z/2) (d phi)^2
        + C1 (d phi)^2 O_matter
        + (1/f) d phi J5,

define

    phi_c = sqrt(Z) phi.

Then

    C1_c = C1/Z,
    f_c  = f sqrt(Z),

and therefore

    C1_c f_c^2 = C1 f^2.

A large Delta Z is therefore not itself an operating-energy multiplier. It
means that the low-energy canonical parameters must be obtained by RG running
or UV matching.

SPHERICAL SUPPORT
-----------------
A constant-pressure interior plus constant isotropic surface tension requires a
constant-mean-curvature closed surface. Within the regular compact branch the
support-friendly shape is a sphere.

For a uniformly polarized spherical scalar dipole the integrated canonical
scalar spatial stresses are

    Pi_x = Pi_y = -3 E_phi / 5,
    Pi_z = +E_phi / 5,

whose trace is

    Pi_x + Pi_y + Pi_z = -E_phi.

The corresponding DEC support-energy lower bound is the largest magnitude of
the integrated principal stress that must be canceled.

CLAIM LIMITS
------------
These are analytical lower-level checks. They do not construct a bag wall,
UV completion, activation system, or nonlinear stable source.
"""

from __future__ import annotations

import math

import numpy as np


def canonical_rescaling(
    *,
    c1_bare_ev_m4: float,
    f_bare_ev: float,
    kinetic_z: float,
) -> dict[str, float]:
    """Canonicalize a scalar and expose the invariant C1 f^2."""

    c1 = float(
        c1_bare_ev_m4
    )

    f_value = float(
        f_bare_ev
    )

    z_value = float(
        kinetic_z
    )

    if (
        f_value <= 0.0
        or z_value <= 0.0
    ):
        raise ValueError(
            "f and kinetic Z must be positive"
        )

    c1_canonical = (
        c1
        / z_value
    )

    f_canonical = (
        f_value
        * math.sqrt(
            z_value
        )
    )

    invariant_before = (
        c1
        * f_value**2
    )

    invariant_after = (
        c1_canonical
        * f_canonical**2
    )

    return {
        "c1_canonical_ev_m4":
            c1_canonical,

        "f_canonical_ev":
            f_canonical,

        "invariant_before_ev_m2":
            invariant_before,

        "invariant_after_ev_m2":
            invariant_after,

        "invariant_relative_error":
            (
                abs(
                    invariant_after
                    - invariant_before
                )
                /
                max(
                    abs(
                        invariant_before
                    ),
                    1.0e-300,
                )
            ),
    }


def isotropic_bag_shape_compatible(
    *,
    a_m: float,
    c_m: float,
    relative_tolerance: float = 1.0e-8,
) -> bool:
    """Return whether a spheroid is spherical within declared tolerance.

    This is the morphology gate for the minimal constant-pressure,
    constant-isotropic-tension support ansatz.
    """

    a = float(
        a_m
    )

    c = float(
        c_m
    )

    tolerance = float(
        relative_tolerance
    )

    if (
        a <= 0.0
        or c <= 0.0
        or tolerance < 0.0
    ):
        raise ValueError(
            "invalid support geometry"
        )

    return (
        abs(
            a - c
        )
        /
        max(
            a,
            c,
        )
        <= tolerance
    )


def polarized_sphere_incident_coefficients(
    *,
    source_radius_m: float,
    center_separation_m: float,
    lmax: int,
) -> np.ndarray:
    """Return exact regular Legendre coefficients about the payload center.

    Source
    ------
    A uniformly polarized sphere of radius R has exterior unit-polarization
    potential

        Phi = -(R^3/3) z_s / r_s^3.

    Put the source center a distance D below the payload center.

    For r < D,

        1/|D zhat + r|
          =
          sum_l (-1)^l r^l P_l(cos theta) / D^(l+1).

    Differentiating with respect to D gives the dipole potential and therefore

        a_l
          =
          -(R^3/3)
          (l+1)
          (-1)^l
          / D^(l+2).
    """

    radius = float(
        source_radius_m
    )

    separation = float(
        center_separation_m
    )

    maximum = int(
        lmax
    )

    if (
        radius <= 0.0
        or separation <= radius
        or maximum < 1
    ):
        raise ValueError(
            "invalid spherical expansion geometry"
        )

    dipole_coefficient = (
        radius**3
        / 3.0
    )

    return np.asarray(
        [
            -dipole_coefficient
            * (
                ell + 1.0
            )
            * (
                (-1.0) ** ell
            )
            / separation ** (
                ell + 2
            )
            for ell
            in range(
                maximum + 1
            )
        ],
        dtype=float,
    )


def scalar_sphere_integrated_stresses_j(
    field_energy_j: float,
) -> dict[str, float]:
    """Return integrated canonical scalar stresses of a spherical dipole."""

    energy = float(
        field_energy_j
    )

    if energy < 0.0:
        raise ValueError(
            "field energy must be nonnegative"
        )

    transverse = (
        -3.0
        * energy
        / 5.0
    )

    longitudinal = (
        energy
        / 5.0
    )

    return {
        "pi_x_j":
            transverse,

        "pi_y_j":
            transverse,

        "pi_z_j":
            longitudinal,

        "trace_j":
            (
                2.0
                * transverse
                + longitudinal
            ),
    }


def spherical_anisotropic_dec_support_floor_j(
    *,
    fermion_pressure_perp_inventory_j: float,
    fermion_pressure_z_inventory_j: float,
    scalar_field_energy_j: float,
) -> dict[str, float]:
    """Return anisotropic integrated-stress DEC support lower bound."""

    pressure_perp = float(
        fermion_pressure_perp_inventory_j
    )

    pressure_z = float(
        fermion_pressure_z_inventory_j
    )

    scalar = (
        scalar_sphere_integrated_stresses_j(
            scalar_field_energy_j
        )
    )

    net_perp = (
        pressure_perp
        + scalar[
            "pi_x_j"
        ]
    )

    net_z = (
        pressure_z
        + scalar[
            "pi_z_j"
        ]
    )

    floor = max(
        abs(
            net_perp
        ),
        abs(
            net_z
        ),
    )

    return {
        "net_source_stress_perp_j":
            net_perp,

        "net_source_stress_z_j":
            net_z,

        "support_energy_floor_j":
            floor,
    }
