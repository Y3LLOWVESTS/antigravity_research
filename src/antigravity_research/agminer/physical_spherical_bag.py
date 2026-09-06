"""Physical spherical false-vacuum bag helpers for 032V19.

PURPOSE
-------
Construct a concrete positive-energy support/confinement preflight for the
032V18 spherical hidden-fermion axial source.

SCIENTIFIC QUESTION
-------------------
Can the V18 anisotropic DEC support lower bound be approached by a genuine
microscopic action rather than by a hand-prescribed stress tensor?

PHYSICAL MODEL
--------------
Use a Friedberg-Lee-type false-vacuum fermion bag:

    canonical support scalar chi
    +
    tilted double-well potential V(chi)
    +
    hidden-fermion Yukawa mass barrier
    +
    existing axial derivative coupling to phi.

The false-vacuum energy B contributes

    rho = B
    p   = -B

and therefore supplies positive-energy compressive support.

A spherical thin wall of surface tension sigma obeys

    p_source - B = 2 sigma / R.

This allows support energy to approach the DEC pressure floor while retaining
a finite physical phase boundary.

CLAIM LIMITS
------------
This module is an action-level and thin-wall preflight.

It does not establish:

- a solved coupled chi/Psi/phi field;
- exact local conservation of that solved field;
- nonlinear stability;
- a renormalized axial determinant;
- a UV completion of the outward C1 operator;
- empirical viability;
- a complete operating-energy ledger;
- a practical antigravity device.
"""

from __future__ import annotations

import math

import numpy as np


EV_TO_J = 1.602176634e-19
HBARC_EV_M = 1.973269804e-7

EV4_TO_J_M3 = (
    EV_TO_J
    /
    HBARC_EV_M**3
)


def sphere_volume_m3(
    radius_m: float,
) -> float:
    """Return sphere volume in cubic meters."""

    radius = float(radius_m)

    if radius <= 0.0:
        raise ValueError(
            "radius must be positive"
        )

    return (
        4.0
        * math.pi
        * radius**3
        / 3.0
    )


def sphere_area_m2(
    radius_m: float,
) -> float:
    """Return sphere area in square meters."""

    radius = float(radius_m)

    if radius <= 0.0:
        raise ValueError(
            "radius must be positive"
        )

    return (
        4.0
        * math.pi
        * radius**2
    )


def pressure_decomposition_j(
    *,
    pressure_perp_j: float,
    pressure_z_j: float,
) -> dict[str, float]:
    """Separate isotropic mean pressure from the small axial anisotropy."""

    pressure_perp = float(
        pressure_perp_j
    )

    pressure_z = float(
        pressure_z_j
    )

    mean_pressure = (
        2.0
        * pressure_perp
        + pressure_z
    ) / 3.0

    anisotropy_floor = max(
        abs(
            pressure_perp
            - mean_pressure
        ),
        abs(
            pressure_z
            - mean_pressure
        ),
    )

    return {
        "mean_pressure_inventory_j":
            mean_pressure,

        "anisotropy_reserve_floor_j":
            anisotropy_floor,

        "full_pressure_split_j":
            abs(
                pressure_z
                - pressure_perp
            ),
    }


def friedberg_lee_bag_support(
    *,
    radius_m: float,
    pressure_perp_j: float,
    pressure_z_j: float,
    bag_fraction: float,
) -> dict[str, float]:
    """Return thin-wall false-vacuum bag support accounting.

    Let

        B = x p_mean

    with 0 <= x < 1.

    Young-Laplace balance gives

        p_mean - B = 2 sigma/R.

    The support energy is

        E_support
            =
            B V
            +
            4 pi R^2 sigma
            +
            E_anisotropy_reserve.

    The final term is retained because a perfectly isotropic scalar wall
    cannot by itself cancel the small V18 axial pressure anisotropy.
    """

    radius = float(
        radius_m
    )

    fraction = float(
        bag_fraction
    )

    if (
        radius <= 0.0
        or fraction < 0.0
        or fraction >= 1.0
    ):
        raise ValueError(
            "invalid spherical bag parameter"
        )

    decomposition = (
        pressure_decomposition_j(
            pressure_perp_j=
                pressure_perp_j,

            pressure_z_j=
                pressure_z_j,
        )
    )

    mean_inventory = float(
        decomposition[
            "mean_pressure_inventory_j"
        ]
    )

    if mean_inventory <= 0.0:
        raise ValueError(
            "support branch requires positive mean source pressure"
        )

    volume = sphere_volume_m3(
        radius
    )

    area = sphere_area_m2(
        radius
    )

    mean_pressure_pa = (
        mean_inventory
        / volume
    )

    bag_density = (
        fraction
        * mean_pressure_pa
    )

    residual_wall_pressure = (
        1.0
        - fraction
    ) * mean_pressure_pa

    wall_tension = (
        radius
        * residual_wall_pressure
        / 2.0
    )

    bag_energy = (
        bag_density
        * volume
    )

    wall_energy = (
        wall_tension
        * area
    )

    anisotropy_reserve = float(
        decomposition[
            "anisotropy_reserve_floor_j"
        ]
    )

    support_energy = (
        bag_energy
        + wall_energy
        + anisotropy_reserve
    )

    transverse_pressure_pa = (
        float(
            pressure_perp_j
        )
        / volume
    )

    axial_pressure_pa = (
        float(
            pressure_z_j
        )
        / volume
    )

    equatorial_tension = (
        radius
        * (
            transverse_pressure_pa
            - bag_density
        )
        / 2.0
    )

    polar_tension = (
        radius
        * (
            axial_pressure_pa
            - bag_density
        )
        / 2.0
    )

    return {
        **decomposition,

        "radius_m":
            radius,

        "volume_m3":
            volume,

        "area_m2":
            area,

        "bag_fraction":
            fraction,

        "mean_pressure_pa":
            mean_pressure_pa,

        "bag_energy_density_j_m3":
            bag_density,

        "bag_energy_j":
            bag_energy,

        "wall_pressure_pa":
            residual_wall_pressure,

        "wall_tension_j_m2":
            wall_tension,

        "wall_energy_j":
            wall_energy,

        "equatorial_required_tension_j_m2":
            equatorial_tension,

        "polar_required_tension_j_m2":
            polar_tension,

        "tension_anisotropy_ratio":
            (
                max(
                    equatorial_tension,
                    polar_tension,
                )
                /
                min(
                    equatorial_tension,
                    polar_tension,
                )
            ),

        "support_preflight_j":
            support_energy,
    }


def quartic_wall_parameters(
    *,
    wall_tension_j_m2: float,
    mediator_mass_ev: float,
) -> dict[str, float]:
    """Map a desired wall tension to a canonical quartic kink.

    For the degenerate part

        V0 = lambda/4 (chi^2-v^2)^2

    the small-fluctuation mass and planar tension are

        m_chi = sqrt(2 lambda) v

        sigma = 2 m_chi v^2 / 3.

    Therefore

        v^2 = 3 sigma / (2 m_chi).
    """

    tension = float(
        wall_tension_j_m2
    )

    mass = float(
        mediator_mass_ev
    )

    if (
        tension <= 0.0
        or mass <= 0.0
    ):
        raise ValueError(
            "wall tension and mediator mass must be positive"
        )

    tension_ev3 = (
        tension
        * HBARC_EV_M**2
        / EV_TO_J
    )

    vev = math.sqrt(
        3.0
        * tension_ev3
        / (
            2.0
            * mass
        )
    )

    lambda_value = (
        mass**2
        /
        (
            2.0
            * vev**2
        )
    )

    thickness = (
        2.0
        * HBARC_EV_M
        / mass
    )

    barrier = (
        lambda_value
        * vev**4
        / 4.0
    )

    return {
        "surface_tension_ev3":
            tension_ev3,

        "mediator_mass_ev":
            mass,

        "vev_ev":
            vev,

        "lambda":
            lambda_value,

        "wall_thickness_m":
            thickness,

        "degenerate_barrier_ev4":
            barrier,
    }


def tilted_wall_potential_ev4(
    chi_ev: np.ndarray | float,
    *,
    vev_ev: float,
    lambda_: float,
    bag_density_j_m3: float,
) -> np.ndarray:
    """Return a bounded tilted double-well support potential.

    Use

        H(s)
            =
            1/2
            -
            3s/4
            +
            s^3/4

    so that

        H(+1)=0
        H(-1)=1
        H'(+/-1)=0.

    Thus the two quartic extrema remain stationary while their vacuum energies
    differ by the declared bag constant B.
    """

    chi = np.asarray(
        chi_ev,
        dtype=float,
    )

    vev = float(
        vev_ev
    )

    lambda_value = float(
        lambda_
    )

    bag_density_ev4 = (
        float(
            bag_density_j_m3
        )
        / EV4_TO_J_M3
    )

    if (
        vev <= 0.0
        or lambda_value <= 0.0
        or bag_density_ev4 < 0.0
    ):
        raise ValueError(
            "invalid tilted-wall potential parameter"
        )

    s = (
        chi
        / vev
    )

    tilt_shape = (
        0.5
        - 0.75
        * s
        + 0.25
        * s**3
    )

    return (
        lambda_value
        * (
            chi**2
            - vev**2
        )**2
        / 4.0
        +
        bag_density_ev4
        * tilt_shape
    )


def yukawa_mass_barrier(
    *,
    inside_mass_ev: float,
    chemical_potential_ev: float,
    vev_ev: float,
    outside_mass_factor: float,
) -> dict[str, float]:
    """Return the Yukawa parameters for a hidden-fermion bag mass barrier."""

    inside_mass = float(
        inside_mass_ev
    )

    chemical_potential = float(
        chemical_potential_ev
    )

    vev = float(
        vev_ev
    )

    factor = float(
        outside_mass_factor
    )

    if (
        inside_mass <= 0.0
        or chemical_potential <= 0.0
        or vev <= 0.0
        or factor <= 1.0
    ):
        raise ValueError(
            "invalid mass-barrier parameter"
        )

    outside_mass = (
        factor
        * chemical_potential
    )

    if outside_mass <= chemical_potential:
        raise ValueError(
            "outside mass must exceed the occupied chemical potential"
        )

    m0 = (
        inside_mass
        + outside_mass
    ) / 2.0

    yukawa = (
        outside_mass
        - inside_mass
    ) / (
        2.0
        * vev
    )

    kappa = math.sqrt(
        outside_mass**2
        - chemical_potential**2
    )

    decay_length = (
        HBARC_EV_M
        / kappa
    )

    return {
        "outside_mass_ev":
            outside_mass,

        "outside_mass_over_mu":
            (
                outside_mass
                / chemical_potential
            ),

        "m0_ev":
            m0,

        "yukawa":
            yukawa,

        "evanescent_kappa_ev":
            kappa,

        "decay_length_m":
            decay_length,
    }


def fermion_cw_magnitude_proxy_j(
    *,
    flavors: int,
    inside_mass_ev: float,
    outside_mass_ev: float,
    volume_m3: float,
) -> float:
    """Return a one-loop Coleman-Weinberg natural-scale magnitude proxy.

    The magnitude

        N_f |m_out^4-m_in^4| / (16 pi^2)

    is used only as a naturalness/matching scale.

    It is NOT inserted automatically as an additional device-energy term.
    The finite sign and counterterm matching must be supplied by the
    renormalized UV theory.
    """

    flavor_count = int(
        flavors
    )

    inside_mass = float(
        inside_mass_ev
    )

    outside_mass = float(
        outside_mass_ev
    )

    volume = float(
        volume_m3
    )

    if (
        flavor_count < 1
        or inside_mass <= 0.0
        or outside_mass <= 0.0
        or volume <= 0.0
    ):
        raise ValueError(
            "invalid Coleman-Weinberg proxy input"
        )

    density_ev4 = (
        flavor_count
        * abs(
            outside_mass**4
            - inside_mass**4
        )
        / (
            16.0
            * math.pi**2
        )
    )

    return (
        density_ev4
        * EV4_TO_J_M3
        * volume
    )


def support_loop_naturalness(
    *,
    flavors: int,
    yukawa: float,
    lambda_: float,
    cutoff_ev: float,
    mediator_mass_ev: float,
) -> dict[str, float]:
    """Return conservative support-scalar loop-size proxies."""

    flavor_count = int(
        flavors
    )

    y_value = float(
        yukawa
    )

    lambda_value = float(
        lambda_
    )

    cutoff = float(
        cutoff_ev
    )

    mediator_mass = float(
        mediator_mass_ev
    )

    if (
        flavor_count < 1
        or lambda_value <= 0.0
        or cutoff <= 0.0
        or mediator_mass <= 0.0
    ):
        raise ValueError(
            "invalid support-loop input"
        )

    delta_lambda = (
        flavor_count
        * y_value**4
        / (
            16.0
            * math.pi**2
        )
    )

    delta_m2 = (
        flavor_count
        * y_value**2
        * cutoff**2
        / (
            16.0
            * math.pi**2
        )
    )

    return {
        "delta_lambda_proxy":
            delta_lambda,

        "delta_lambda_over_lambda":
            (
                delta_lambda
                / lambda_value
            ),

        "delta_m2_ev2_proxy":
            delta_m2,

        "delta_m2_over_m2":
            (
                delta_m2
                / mediator_mass**2
            ),
    }


def trace_load_epsilon(
    *,
    energy_density_j_m3: float,
    metric_scale_ev: float,
) -> float:
    """Return rho/M^4 for a support-sector trace-loading scout."""

    density = float(
        energy_density_j_m3
    )

    scale = float(
        metric_scale_ev
    )

    if (
        density < 0.0
        or scale <= 0.0
    ):
        raise ValueError(
            "invalid trace-loading input"
        )

    m4_density = (
        EV4_TO_J_M3
        * scale**4
    )

    return (
        density
        / m4_density
    )


def axial_spacelike_gap(
    *,
    b_ev: float,
    mass_ev: float,
) -> dict[str, float | bool]:
    """Return the minimum spacelike-axial spectral-gap scout."""

    b_value = float(
        b_ev
    )

    mass = float(
        mass_ev
    )

    if (
        b_value < 0.0
        or mass <= 0.0
    ):
        raise ValueError(
            "invalid axial-gap input"
        )

    return {
        "b_over_m":
            (
                b_value
                / mass
            ),

        "gap_ev":
            abs(
                mass
                - b_value
            ),

        "strict_b_below_m":
            (
                b_value
                < mass
            ),
    }


def radial_gamma_threshold(
    bag_fraction: float,
) -> float:
    """Return conditional radial-stability threshold.

    If the fixed-number source pressure scales locally as

        p_f ~ R^(-Gamma)

    while B and sigma are fixed over the perturbation, then stability of

        p_f - B - 2 sigma/R = 0

    requires

        Gamma > 1-B/p_f = 1-x.

    This is a necessary analytical scout, not a coupled mode calculation.
    """

    fraction = float(
        bag_fraction
    )

    if (
        fraction < 0.0
        or fraction >= 1.0
    ):
        raise ValueError(
            "invalid bag fraction"
        )

    return (
        1.0
        - fraction
    )


def l2_wall_stiffness_scout_j(
    wall_energy_j: float,
) -> float:
    """Return the thin-wall l=2 surface-area quadratic stiffness scout.

    For a volume-preserving deformation proportional to P_2,

        Delta E_wall
            =
            0.4 E_wall epsilon^2

    so the second derivative with respect to epsilon is

        0.8 E_wall.

    The source response must still be included in the actual eigenmode.
    """

    wall_energy = float(
        wall_energy_j
    )

    if wall_energy < 0.0:
        raise ValueError(
            "wall energy must be nonnegative"
        )

    return (
        0.8
        * wall_energy
    )
