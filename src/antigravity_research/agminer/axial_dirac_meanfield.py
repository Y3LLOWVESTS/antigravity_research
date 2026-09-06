"""Exact positive-band axial Dirac mean-field diagnostics for 032V16.

This module performs the tree-level occupied-positive-energy-band calculation
for hidden Dirac fermions coupled to a static spacelike axial background.

It deliberately excludes the renormalized Dirac sea. Therefore any result
with non-negligible loop load is a prefield result that requires a subsequent
one-loop vacuum and canonical-normalization calculation.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq

from antigravity_research.agminer.kinetic_conformal import (
    EV_J,
    HBARC_EV_M,
    ev4_energy_density_j_m3,
)

PI = math.pi


def spheroid_volume_m3(a_m: float, c_m: float) -> float:
    """Return axisymmetric spheroid volume in cubic meters."""
    a = float(a_m)
    c = float(c_m)
    if a <= 0.0 or c <= 0.0:
        raise ValueError("semi axes must be positive")
    return 4.0 * PI * a**2 * c / 3.0


def spheroid_demag_z(a_m: float, c_m: float) -> float:
    """Return exact z demagnetization factor for an axisymmetric spheroid."""
    a = float(a_m)
    c = float(c_m)

    if a <= 0.0 or c <= 0.0:
        raise ValueError("semi axes must be positive")

    if abs(a - c) <= 1.0e-12 * max(a, c):
        return 1.0 / 3.0

    if c > a:
        eccentricity = math.sqrt(
            1.0 - a**2 / c**2
        )

        return (
            (1.0 - eccentricity**2)
            / (
                2.0
                * eccentricity**3
            )
            * (
                math.log(
                    (1.0 + eccentricity)
                    / (1.0 - eccentricity)
                )
                - 2.0
                * eccentricity
            )
        )

    xi = math.sqrt(
        a**2 / c**2
        - 1.0
    )

    return (
        (1.0 + xi**2)
        / xi**3
        * (
            xi
            - math.atan(xi)
        )
    )


def _gauss_interval(
    order: int,
    upper: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return Gauss Legendre nodes and weights on [0, upper]."""
    if order < 12:
        raise ValueError(
            "quadrature order must be at least 12"
        )

    if upper <= 0.0:
        return (
            np.zeros(1),
            np.zeros(1),
        )

    nodes, weights = (
        np.polynomial.legendre.leggauss(
            int(order)
        )
    )

    pz = (
        0.5
        * upper
        * (
            nodes
            + 1.0
        )
    )

    w = (
        0.5
        * upper
        * weights
    )

    return pz, w


def axial_positive_band_integrals(
    *,
    mass_ev: float,
    axial_b_ev: float,
    chemical_potential_ev: float,
    order: int = 160,
) -> dict[str, float]:
    """Integrate occupied positive Dirac bands in a constant axial background.

    Convention
    ----------
    The positive-energy branches are

        E_s^2 = p_perp^2 + (sqrt(p_z^2 + m^2) + s b)^2,

    with s in {-1,+1}. The useful axial current is defined by

        J5 = - d E_occupied / d b.

    Natural units hbar=c=1 are used. Returned densities have dimensions eV^3
    for number/current and eV^4 for energy/pressure.

    The occupied p_z interval of each branch is integrated separately. This
    avoids placing a Gauss rule across the Fermi-surface discontinuity.

    This is a positive-band matter calculation only. It omits the renormalized
    vacuum determinant and must not be treated as a complete quantum EFT.
    """
    m = float(mass_ev)
    b = float(axial_b_ev)
    mu = float(chemical_potential_ev)

    if (
        m < 0.0
        or b < 0.0
        or mu <= 0.0
    ):
        raise ValueError(
            "invalid positive-band parameter"
        )

    number = 0.0
    current = 0.0
    energy = 0.0
    p_perp = 0.0
    p_z = 0.0

    for sign in (
        -1.0,
        1.0,
    ):
        if sign > 0.0:
            upper_root = (
                mu
                - b
            )

            if upper_root <= m:
                continue

            lower_root = m

        else:
            upper_root = (
                mu
                + b
            )

            if upper_root <= m:
                continue

            lower_root = max(
                m,
                b - mu,
            )

            if lower_root >= upper_root:
                continue

        lower_pz = math.sqrt(
            max(
                0.0,
                lower_root**2
                - m**2,
            )
        )

        upper_pz = math.sqrt(
            max(
                0.0,
                upper_root**2
                - m**2,
            )
        )

        if upper_pz <= lower_pz:
            continue

        nodes, weights = (
            np.polynomial.legendre.leggauss(
                int(order)
            )
        )

        pzz = (
            lower_pz
            + 0.5
            * (
                upper_pz
                - lower_pz
            )
            * (
                nodes
                + 1.0
            )
        )

        ww = (
            0.5
            * (
                upper_pz
                - lower_pz
            )
            * weights
        )

        root = np.sqrt(
            pzz**2
            + m**2
        )

        am = (
            root
            + sign
            * b
        )

        aam = np.abs(
            am
        )

        pmax2 = np.maximum(
            0.0,
            mu**2
            - aam**2,
        )

        number += float(
            np.sum(
                ww
                * pmax2
            )
        ) / (
            4.0
            * PI**2
        )

        energy += float(
            np.sum(
                ww
                * (
                    mu**3
                    - aam**3
                )
            )
        ) / (
            6.0
            * PI**2
        )

        # Hellmann-Feynman:
        #
        #     J5 = -dE/db.
        #
        # After analytic p_perp integration:
        #
        #     integral p dp a/E
        #       =
        #       a (mu-|a|).

        current += float(
            np.sum(
                ww
                * (
                    -sign
                )
                * am
                * (
                    mu
                    - aam
                )
            )
        ) / (
            2.0
            * PI**2
        )

        # One transverse principal pressure.

        transverse_primitive = (
            mu**3
            / 3.0
            - aam**2
            * mu
            + 2.0
            * aam**3
            / 3.0
        )

        p_perp += float(
            np.sum(
                ww
                * transverse_primitive
            )
        ) / (
            4.0
            * PI**2
        )

        # Longitudinal momentum flux:
        #
        #     p_z dE/dp_z.

        safe_root = np.where(
            root > 0.0,
            root,
            1.0,
        )

        longitudinal_primitive = (
            pzz**2
            / safe_root
            * am
            * (
                mu
                - aam
            )
        )

        p_z += float(
            np.sum(
                ww
                * longitudinal_primitive
            )
        ) / (
            2.0
            * PI**2
        )

    return {
        "number_density_ev3":
            number,

        "axial_current_ev3":
            current,

        "energy_density_ev4":
            energy,

        "pressure_perp_ev4":
            p_perp,

        "pressure_z_ev4":
            p_z,
    }


def solve_mu_for_current(
    *,
    mass_ev: float,
    axial_b_ev: float,
    target_current_ev3: float,
    flavors: int = 1,
    order: int = 160,
) -> dict[str, float]:
    """Solve chemical potential giving the requested total axial current."""
    m = float(
        mass_ev
    )

    b = float(
        axial_b_ev
    )

    target = float(
        target_current_ev3
    )

    nf = int(
        flavors
    )

    if (
        target <= 0.0
        or nf < 1
    ):
        raise ValueError(
            "target current and flavors must be positive"
        )

    def residual(
        mu: float,
    ) -> float:
        values = (
            axial_positive_band_integrals(
                mass_ev=m,
                axial_b_ev=b,
                chemical_potential_ev=mu,
                order=order,
            )
        )

        return (
            nf
            * values[
                "axial_current_ev3"
            ]
            - target
        )

    low = max(
        1.0e-9,
        abs(
            m
            - b
        )
        * 1.0000001,
    )

    if residual(
        low
    ) >= 0.0:
        low = 1.0e-9

    high = max(
        m + b + 1.0,
        2.0
        * max(
            m,
            b,
            1.0,
        ),
    )

    for _ in range(
        80
    ):
        if residual(
            high
        ) > 0.0:
            break

        high *= 1.7

    else:
        raise RuntimeError(
            "failed to bracket chemical potential"
        )

    mu = brentq(
        residual,
        low,
        high,
        xtol=1.0e-11,
        rtol=1.0e-12,
    )

    values = (
        axial_positive_band_integrals(
            mass_ev=m,
            axial_b_ev=b,
            chemical_potential_ev=mu,
            order=order,
        )
    )

    return {
        "chemical_potential_ev":
            mu,

        **{
            key:
                nf
                * value
            for (
                key,
                value,
            )
            in values.items()
        },
    }


def dimensionless_band_integrals(
    *,
    r_mass_over_b: float,
    u_mu_over_b: float,
    order: int = 160,
) -> dict[str, float]:
    """Return positive-band integrals with b set to one eV."""
    r = float(
        r_mass_over_b
    )

    u = float(
        u_mu_over_b
    )

    if (
        r <= 0.0
        or u <= 0.0
    ):
        raise ValueError(
            "dimensionless ratios must be positive"
        )

    return (
        axial_positive_band_integrals(
            mass_ev=r,
            axial_b_ev=1.0,
            chemical_potential_ev=u,
            order=order,
        )
    )


def meanfield_scaling_metrics(
    *,
    q: float,
    metric_scale_ev: float,
    volume_m3: float,
    demag_z: float,
    r_mass_over_b: float,
    u_mu_over_b: float,
    order: int = 160,
) -> dict[str, float]:
    """Return flavor-invariant tree-level positive-band mean-field metrics.

    Self-consistency is

        J5 = q f M^2,

        b = N_z J5/f^2 = N_z q M^2/f.

    If jhat is the one-flavor current at b=1, then

        f^4 = N_f N_z^3 q^2 M^4 jhat.

    At fixed dimensionless ratios r=m/b and u=mu/b, N_f cancels from the
    occupied-band energy, loop proxy, field energy and pressure. It only
    increases the source cutoff margin as sqrt(N_f).
    """
    qv = float(
        q
    )

    mscale = float(
        metric_scale_ev
    )

    volume = float(
        volume_m3
    )

    nz = float(
        demag_z
    )

    if (
        qv <= 0.0
        or mscale <= 0.0
        or volume <= 0.0
        or not (
            0.0
            < nz
            < 1.0
        )
    ):
        raise ValueError(
            "invalid mean-field geometry"
        )

    hats = (
        dimensionless_band_integrals(
            r_mass_over_b=
                r_mass_over_b,

            u_mu_over_b=
                u_mu_over_b,

            order=
                order,
        )
    )

    jhat = hats[
        "axial_current_ev3"
    ]

    if jhat <= 0.0:
        raise ValueError(
            "dimensionless state does not carry useful current"
        )

    volume_nat = (
        volume
        / HBARC_EV_M**3
    )

    energy_base_j = (
        nz
        * qv**2
        * mscale**4
        * volume_nat
        * EV_J
    )

    field_energy_j = (
        0.5
        * energy_base_j
    )

    band_energy_j = (
        energy_base_j
        * hats[
            "energy_density_ev4"
        ]
        / jhat
    )

    pressure_perp_j = (
        energy_base_j
        * hats[
            "pressure_perp_ev4"
        ]
        / jhat
    )

    pressure_z_j = (
        energy_base_j
        * hats[
            "pressure_z_ev4"
        ]
        / jhat
    )

    pressure_mean_j = (
        2.0
        * pressure_perp_j
        + pressure_z_j
    ) / 3.0

    # The exact occupied-band energies already include the axial interaction.
    #
    # Add the positive canonical scalar field energy exactly once.
    #
    # For the static Laue scout, the scalar field stress reduces the net
    # outward fermion pressure that a support sector must balance.

    support_floor_j = abs(
        pressure_mean_j
        - field_energy_j
    )

    partial_floor_j = (
        band_energy_j
        + field_energy_j
        + support_floor_j
    )

    r = float(
        r_mass_over_b
    )

    u = float(
        u_mu_over_b
    )

    # Integrating the derivative axial coupling by parts gives a
    # mass-proportional pseudoscalar Yukawa interaction, motivating
    #
    #     L = N_f m^2/(4*pi^2 f^2).
    #
    # After the dimensionless self-consistency reduction:
    #
    #     L = r^2/(4*pi^2*N_z*jhat).

    loop_proxy = (
        r**2
        / (
            4.0
            * PI**2
            * nz
            * jhat
        )
    )

    # NDA cutoff margin:
    #
    #     Lambda_src/max(mu,m,b)
    #
    #     =
    #
    #     4*pi*sqrt(N_f*N_z*jhat)
    #     /
    #     max(u,r,1).

    hard_denominator = max(
        u,
        r,
        1.0,
    )

    margin_one_flavor = (
        4.0
        * PI
        * math.sqrt(
            nz
            * jhat
        )
        / hard_denominator
    )

    min_flavors_for_margin5 = (
        5.0
        / margin_one_flavor
    ) ** 2

    return {
        "jhat":
            jhat,

        "nhat":
            hats[
                "number_density_ev3"
            ],

        "ehat":
            hats[
                "energy_density_ev4"
            ],

        "pressure_perp_hat":
            hats[
                "pressure_perp_ev4"
            ],

        "pressure_z_hat":
            hats[
                "pressure_z_ev4"
            ],

        "energy_base_j":
            energy_base_j,

        "field_energy_j":
            field_energy_j,

        "band_energy_j":
            band_energy_j,

        "pressure_perp_inventory_j":
            pressure_perp_j,

        "pressure_z_inventory_j":
            pressure_z_j,

        "pressure_mean_inventory_j":
            pressure_mean_j,

        "support_floor_j":
            support_floor_j,

        "partial_conservative_floor_j":
            partial_floor_j,

        "loop_proxy":
            loop_proxy,

        "hard_margin_one_flavor":
            margin_one_flavor,

        "minimum_flavors_continuous_for_margin5":
            min_flavors_for_margin5,
    }


def physicalize_dimensionless_state(
    *,
    q: float,
    metric_scale_ev: float,
    demag_z: float,
    r_mass_over_b: float,
    u_mu_over_b: float,
    flavors: int,
    order: int = 160,
) -> dict[str, float]:
    """Convert a dimensionless self-consistent state to physical eV scales."""
    qv = float(
        q
    )

    mscale = float(
        metric_scale_ev
    )

    nz = float(
        demag_z
    )

    nf = int(
        flavors
    )

    if nf < 1:
        raise ValueError(
            "flavors must be positive"
        )

    hats = (
        dimensionless_band_integrals(
            r_mass_over_b=
                r_mass_over_b,

            u_mu_over_b=
                u_mu_over_b,

            order=
                order,
        )
    )

    jhat = hats[
        "axial_current_ev3"
    ]

    if jhat <= 0.0:
        raise ValueError(
            "state carries no useful current"
        )

    f_ev = (
        nf
        * nz**3
        * qv**2
        * mscale**4
        * jhat
    ) ** 0.25

    b_ev = (
        nz
        * qv
        * mscale**2
        / f_ev
    )

    m_ev = (
        float(
            r_mass_over_b
        )
        * b_ev
    )

    mu_ev = (
        float(
            u_mu_over_b
        )
        * b_ev
    )

    cutoff_ev = (
        4.0
        * PI
        * f_ev
    )

    hard_ev = max(
        mu_ev,
        m_ev,
        b_ev,
    )

    number_density = (
        nf
        * b_ev**3
        * hats[
            "number_density_ev3"
        ]
    )

    total_current = (
        nf
        * b_ev**3
        * jhat
    )

    target_current = (
        qv
        * f_ev
        * mscale**2
    )

    return {
        "flavors":
            float(
                nf
            ),

        "f_psi_ev":
            f_ev,

        "axial_b_ev":
            b_ev,

        "m_psi_ev":
            m_ev,

        "chemical_potential_ev":
            mu_ev,

        "nda_cutoff_ev":
            cutoff_ev,

        "hard_scale_ev":
            hard_ev,

        "hard_scale_margin":
            cutoff_ev
            / hard_ev,

        "number_density_ev3":
            number_density,

        "axial_current_ev3":
            total_current,

        "target_current_ev3":
            target_current,

        "current_relative_error":
            abs(
                total_current
                - target_current
            )
            / target_current,
    }


def stoner_parameter_nr(
    *,
    demag_z: float,
    p_f_over_m: float,
    loop_proxy: float,
) -> float:
    """Return controlled-nonrelativistic Stoner-like polarization parameter.

    For N_f identical species,

        S
          =
          N_z N_f m p_F/(pi^2 f^2)

          =
          4 N_z (p_F/m) L,

    where

        L
          =
          N_f m^2/(4 pi^2 f^2).

    Spontaneous polarization requires S>1 in this quadratic scout.
    """
    nz = float(
        demag_z
    )

    ratio = float(
        p_f_over_m
    )

    loop = float(
        loop_proxy
    )

    if (
        nz <= 0.0
        or ratio < 0.0
        or loop < 0.0
    ):
        raise ValueError(
            "invalid Stoner parameter"
        )

    return (
        4.0
        * nz
        * ratio
        * loop
    )


def minimum_loop_for_nr_stoner(
    *,
    demag_z: float,
    p_f_over_m: float,
) -> float:
    """Return loop proxy required for S=1 in the NR Stoner scout."""
    nz = float(
        demag_z
    )

    ratio = float(
        p_f_over_m
    )

    if (
        nz <= 0.0
        or ratio <= 0.0
    ):
        raise ValueError(
            "positive geometry and pF/m required"
        )

    return (
        1.0
        / (
            4.0
            * nz
            * ratio
        )
    )


def fixed_density_current_susceptibility_hat(
    *,
    r_mass_over_b: float,
    u_mu_over_b: float,
    fractional_step: float = 1.0e-3,
    order: int = 160,
) -> dict[str, float]:
    """Estimate fixed-density occupied-band current susceptibility around b=1.

    The mass and particle density are held fixed as b is varied. The chemical
    potential is re-solved at each neighboring b.

    This is only an occupied-positive-band local curvature proxy. It does not
    contain the vacuum determinant.
    """
    r = float(
        r_mass_over_b
    )

    u = float(
        u_mu_over_b
    )

    step = float(
        fractional_step
    )

    if (
        step <= 0.0
        or step >= 0.1
    ):
        raise ValueError(
            "fractional_step outside scout range"
        )

    reference = (
        axial_positive_band_integrals(
            mass_ev=r,
            axial_b_ev=1.0,
            chemical_potential_ev=u,
            order=order,
        )
    )

    target_n = reference[
        "number_density_ev3"
    ]

    def state_at_b(
        b_value: float,
    ) -> dict[str, float]:
        def density_residual(
            mu_value: float,
        ) -> float:
            state = (
                axial_positive_band_integrals(
                    mass_ev=r,
                    axial_b_ev=b_value,
                    chemical_potential_ev=mu_value,
                    order=order,
                )
            )

            return (
                state[
                    "number_density_ev3"
                ]
                - target_n
            )

        low = 1.0e-8

        high = max(
            u
            * 1.5,
            r
            + b_value
            + 1.0,
        )

        for _ in range(
            50
        ):
            if density_residual(
                high
            ) > 0.0:
                break

            high *= 1.5

        mu_value = brentq(
            density_residual,
            low,
            high,
            xtol=1.0e-11,
            rtol=1.0e-12,
        )

        state = (
            axial_positive_band_integrals(
                mass_ev=r,
                axial_b_ev=b_value,
                chemical_potential_ev=mu_value,
                order=order,
            )
        )

        return {
            "mu_ev":
                mu_value,

            **state,
        }

    lower = state_at_b(
        1.0
        - step
    )

    upper = state_at_b(
        1.0
        + step
    )

    susceptibility = (
        upper[
            "axial_current_ev3"
        ]
        - lower[
            "axial_current_ev3"
        ]
    ) / (
        2.0
        * step
    )

    return {
        "reference_current_hat":
            reference[
                "axial_current_ev3"
            ],

        "susceptibility_hat":
            susceptibility,

        "susceptibility_to_current_ratio":
            susceptibility
            / reference[
                "axial_current_ev3"
            ],
    }


def payload_trace_load(
    *,
    payload_mass_kg: float,
    payload_radius_m: float,
    metric_scale_ev: float,
) -> dict[str, float]:
    """Return weak-field matter-trace loading scout for the physical metric.

    For

        A(X)=1-X/M^4

    and nonrelativistic matter, the scalar equation acquires a local kinetic
    loading of order

        epsilon = rho c^2/M^4.

    A uniform spherical-inclusion linear scout gives

        T = 3/(3+epsilon).

    This is not a substitute for the finite-payload nonlinear PDE.
    """
    mass = float(
        payload_mass_kg
    )

    radius = float(
        payload_radius_m
    )

    scale = float(
        metric_scale_ev
    )

    if (
        mass <= 0.0
        or radius <= 0.0
        or scale <= 0.0
    ):
        raise ValueError(
            "invalid payload trace-load parameter"
        )

    c_si = 299792458.0

    volume = (
        4.0
        * PI
        * radius**3
        / 3.0
    )

    rest_density_j_m3 = (
        mass
        * c_si**2
        / volume
    )

    m4_density_j_m3 = (
        ev4_energy_density_j_m3(
            scale
        )
    )

    epsilon = (
        rest_density_j_m3
        / m4_density_j_m3
    )

    transmission = (
        3.0
        / (
            3.0
            + epsilon
        )
    )

    return {
        "rest_energy_density_j_m3":
            rest_density_j_m3,

        "metric_m4_density_j_m3":
            m4_density_j_m3,

        "epsilon_trace_load":
            epsilon,

        "uniform_sphere_transmission_scout":
            transmission,
    }
