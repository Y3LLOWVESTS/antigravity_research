"""Shift-symmetric compact-source diagnostics for AGMINER 032V14.

PURPOSE
-------
Provide analytical diagnostics for the source-realization problem exposed by
032V13.

V13 established that a regular, isolated, strictly static, exact-shift-
symmetric scalar with positive effective spatial current coefficient cannot
support the desired nonzero monopolar gradient.

V14 therefore distinguishes:

1. net static scalar monopole charge;
2. compact zero-net derivative sources;
3. the leading dipole exterior field produced by a zero-net source;
4. the canonical exterior energy required for finite-payload acceleration.

ZERO-NET SOURCE PRINCIPLE
-------------------------
An interaction

    L_int = J^mu d_mu(phi)

is exactly invariant under

    phi -> phi + constant.

Variation with respect to phi produces a source proportional to

    -d_mu J^mu.

For a regular static compact spatial current J^i that vanishes at infinity,

    integral d^3x d_i J^i = 0.

Therefore such a source cannot produce net scalar monopole charge, but it can
produce nonzero multipoles.

The leading useful exterior field is consequently dipolar.

DIPOLE CONVENTION
-----------------
For a dipole aligned with +z, define the dimensionless positive kinetic
variable

    Y = |grad phi|^2 / (2 M^4)

outside a compact source.

The harmonic scalar dipole has

    Y(r, theta)
      =
      B (1 + 3 cos^2(theta)) / r^6.

In cylindrical coordinates,

    Y(rho, z)
      =
      B (rho^2 + 4 z^2) / (rho^2 + z^2)^4.

The kinetic-conformal outward-sign target is

    A = 1 + Y

with

    g_phys = A^2 g.

Hence the physical acceleration is

    a = -c^2 grad ln(A).

CLAIM LIMITS
------------
These functions describe only an exterior-field oracle.

They do NOT establish:

- a microscopic derivative-current source;
- source energy;
- support energy;
- activation energy;
- stability;
- naturalness;
- empirical consistency;
- a complete operating-energy ledger;
- a practical antigravity device.
"""

from __future__ import annotations

import math

from antigravity_research.agminer.kinetic_conformal import (
    C_LIGHT,
    ev4_energy_density_j_m3,
)


def m4_energy_rescale(
    energy_reference_j: float,
    scale_reference_ev: float,
    scale_ev: float,
) -> float:
    """Rescale an energy proportional to the fourth power of EFT scale M."""

    energy_reference = float(energy_reference_j)
    reference = float(scale_reference_ev)
    scale = float(scale_ev)

    if energy_reference <= 0.0:
        raise ValueError("energy_reference_j must be positive")

    if reference <= 0.0 or scale <= 0.0:
        raise ValueError("energy scales must be positive")

    return (
        energy_reference
        * (scale / reference) ** 4
    )


def scale_ev_for_m4_energy(
    *,
    target_energy_j: float,
    reference_energy_j: float,
    reference_scale_ev: float,
) -> float:
    """Invert E proportional to M^4."""

    target = float(target_energy_j)
    reference_energy = float(reference_energy_j)
    reference_scale = float(reference_scale_ev)

    if target <= 0.0:
        raise ValueError("target_energy_j must be positive")

    if reference_energy <= 0.0 or reference_scale <= 0.0:
        raise ValueError("reference values must be positive")

    return (
        reference_scale
        * (target / reference_energy) ** 0.25
    )


def regular_static_monopole_requires_evasion(
    *,
    inner_boundary: bool = False,
    singular_source: bool = False,
    time_dependent: bool = False,
    kinetic_critical_branch: bool = False,
) -> bool:
    """Return True when a nonzero static monopole requires an evasion.

    For exact shift symmetry and a regular isolated static configuration,

        div J = 0.

    In spherical symmetry,

        r^2 J^r = constant.

    Regularity at the origin forces that constant to zero. A nonzero exterior
    monopole flux therefore requires at least one declared evasion.
    """

    return not any(
        (
            inner_boundary,
            singular_source,
            time_dependent,
            kinetic_critical_branch,
        )
    )


def compact_derivative_source_net_monopole(
    boundary_flux_at_infinity: float = 0.0,
) -> float:
    """Return integrated source charge for a compact divergence source.

    For source density

        s = div J,

    Gauss' theorem gives

        integral s dV = surface_integral J dot dS.

    A compact current has zero boundary flux and hence zero net monopole.
    """

    return float(
        boundary_flux_at_infinity
    )


def dipole_axis_y_required(
    acceleration_m_s2: float,
    radius_m: float,
) -> float:
    """Return axis Y needed for target acceleration at radius r.

    Along the dipole axis,

        Y proportional to r^-6.

    With A=1+Y,

        a = 6 c^2 Y / [r (1+Y)].
    """

    acceleration = float(
        acceleration_m_s2
    )

    radius = float(
        radius_m
    )

    if acceleration <= 0.0 or radius <= 0.0:
        raise ValueError(
            "acceleration and radius must be positive"
        )

    s = (
        acceleration
        * radius
        / (
            6.0
            * C_LIGHT**2
        )
    )

    if s >= 1.0:
        raise ValueError(
            "requested acceleration is outside this branch"
        )

    return (
        s
        / (1.0 - s)
    )


def dipole_b_m6_for_axis_target(
    acceleration_m_s2: float,
    radius_m: float,
) -> float:
    """Return dipole coefficient B in meters^6."""

    radius = float(
        radius_m
    )

    y_axis = (
        dipole_axis_y_required(
            acceleration_m_s2,
            radius,
        )
    )

    # On the axis:
    #
    #     Y = 4 B / r^6.

    return (
        y_axis
        * radius**6
        / 4.0
    )


def dipole_y(
    b_m6: float,
    rho_m: float,
    z_m: float,
) -> float:
    """Return dimensionless Y for the axisymmetric dipole exterior."""

    b = float(
        b_m6
    )

    rho = float(
        rho_m
    )

    z = float(
        z_m
    )

    r2 = (
        rho**2
        + z**2
    )

    if r2 <= 0.0:
        raise ValueError(
            "dipole exterior is undefined at the origin"
        )

    return (
        b
        * (
            rho**2
            + 4.0 * z**2
        )
        / r2**4
    )


def dipole_axial_acceleration_m_s2(
    b_m6: float,
    rho_m: float,
    z_m: float,
) -> float:
    """Return +z physical acceleration for A=1+Y."""

    rho = float(
        rho_m
    )

    z = float(
        z_m
    )

    r2 = (
        rho**2
        + z**2
    )

    shape = (
        rho**2
        + 4.0 * z**2
    )

    if r2 <= 0.0 or shape <= 0.0:
        raise ValueError(
            "point must lie outside the dipole origin"
        )

    y = (
        dipole_y(
            b_m6,
            rho,
            z,
        )
    )

    # From
    #
    #     Y = B (rho^2 + 4 z^2) / (rho^2 + z^2)^4
    #
    # we have
    #
    #     d_z ln Y
    #       =
    #       8 z/(rho^2+4z^2)
    #       -
    #       8 z/(rho^2+z^2).

    dlny_dz = (
        8.0
        * z
        / shape
        -
        8.0
        * z
        / r2
    )

    dy_dz = (
        y
        * dlny_dz
    )

    return (
        -C_LIGHT**2
        * dy_dz
        / (1.0 + y)
    )


def dipole_exterior_energy_j(
    *,
    scale_ev: float,
    source_radius_m: float,
    far_axis_radius_m: float,
    target_acceleration_m_s2: float,
) -> dict[str, float]:
    """Return canonical exterior dipole-gradient energy.

    The canonical scalar energy density is

        rho = M^4 Y.

    Angular integration gives

        integral Y dV
          =
          8 pi B / (3 R_source^3).

    The integration extends from the declared spherical source radius to
    infinity.

    This is a PARTIAL exterior-field energy only.
    """

    scale = float(
        scale_ev
    )

    source_radius = float(
        source_radius_m
    )

    far_radius = float(
        far_axis_radius_m
    )

    target = float(
        target_acceleration_m_s2
    )

    if scale <= 0.0:
        raise ValueError(
            "scale_ev must be positive"
        )

    if source_radius <= 0.0:
        raise ValueError(
            "source_radius_m must be positive"
        )

    if far_radius <= source_radius:
        raise ValueError(
            "far_axis_radius_m must exceed source radius"
        )

    b_m6 = (
        dipole_b_m6_for_axis_target(
            target,
            far_radius,
        )
    )

    rho_scale = (
        ev4_energy_density_j_m3(
            scale
        )
    )

    integral_y_m3 = (
        8.0
        * math.pi
        * b_m6
        / (
            3.0
            * source_radius**3
        )
    )

    energy = (
        rho_scale
        * integral_y_m3
    )

    y_far = (
        dipole_y(
            b_m6,
            0.0,
            far_radius,
        )
    )

    y_source_axis = (
        dipole_y(
            b_m6,
            0.0,
            source_radius,
        )
    )

    return {
        "scale_ev":
            scale,

        "source_radius_m":
            source_radius,

        "far_axis_radius_m":
            far_radius,

        "target_acceleration_m_s2":
            target,

        "b_m6":
            b_m6,

        "y_far_axis":
            y_far,

        "y_source_axis":
            y_source_axis,

        "exterior_scalar_energy_j":
            energy,
    }
