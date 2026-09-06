"""Axial-current microscopic source diagnostics for AGMINER 032V15.

PURPOSE
-------
Test a concrete shift-symmetric microscopic source architecture for the
zero-net scalar dipole promoted by 032V14.

SOURCE ACTION
-------------
The source interaction is

    L_src
        =
        (1 / f_psi)
        partial_mu(phi)
        bar(Psi) gamma^mu gamma^5 Psi.

This interaction is exactly invariant under

    phi -> phi + constant.

For a static polarized fermion population, the spatial axial current acts as a
polarization density. A compact uniformly polarized body has zero integrated
scalar monopole source but nonzero dipole moment.

The source considered here is a spheroid with:

    transverse semi-axis a
    axial semi-axis c
    top surface fixed at z = 0
    polarization along +z.

The payload lies above z = 0.

PHYSICAL METRIC
---------------
The V13/V14 outward-sign target is retained:

    Y = |grad phi|^2 / (2 M^4)

    A = 1 + Y

    g_phys = A^2 g.

The field-response calculation therefore remains universal for neutral payload
matter through the one declared physical metric.

MICROSCOPIC INVENTORY
---------------------
For the hidden fermion source this module includes:

- exact relativistic zero-temperature Fermi energy;
- reduction of axial-current efficiency for relativistic particles;
- a naive-dimensional-analysis source cutoff

      Lambda_src = 4 pi f_psi;

- a declared hard-scale safety ratio

      Lambda_src / max(p_F, m_psi);

- a Laue/DEC pressure-support lower bound.

The pressure-support lower bound is not a complete support realization.

CLAIM LIMITS
------------
This module does NOT establish:

- a self-bound hidden-fermion droplet;
- a physical wall or confinement mechanism;
- polarization/control energy;
- nonlinear stability;
- a UV completion of the desired metric Wilson sign;
- empirical closure;
- a complete operating-energy ledger;
- practical antigravity.

A sub-10-MJ result produced here is therefore only a microscopic-source
inventory corridor, never a certified physical model.
"""

from __future__ import annotations

import math

import numpy as np

from antigravity_research.agminer.kinetic_conformal import (
    C_LIGHT,
    EV_J,
    HBARC_EV_M,
    ev4_energy_density_j_m3,
)


def spheroid_volume_m3(
    a_m: float,
    c_m: float,
) -> float:
    """Return volume of an axisymmetric spheroid."""

    a = float(a_m)
    c = float(c_m)

    if a <= 0.0 or c <= 0.0:
        raise ValueError(
            "spheroid semi-axes must be positive"
        )

    return (
        4.0
        * math.pi
        * a**2
        * c
        / 3.0
    )


def spheroid_demag_z(
    a_m: float,
    c_m: float,
) -> float:
    """Return the exact z demagnetizing factor of a spheroid.

    The same dimensionless geometry factor applies to the scalar-polarization
    self-energy used here.
    """

    a = float(a_m)
    c = float(c_m)

    if a <= 0.0 or c <= 0.0:
        raise ValueError(
            "spheroid semi-axes must be positive"
        )

    if abs(a - c) <= 1.0e-12 * max(a, c):
        return 1.0 / 3.0

    if c > a:
        # Prolate.
        eccentricity = math.sqrt(
            1.0
            - a**2 / c**2
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
                - 2.0 * eccentricity
            )
        )

    # Oblate.
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


def axial_current_efficiency(
    mass_over_pf: float,
    order: int = 96,
) -> float:
    """Return axial-current efficiency of a polarized Fermi sphere.

    For a fermion whose rest-frame spin is aligned with +z,

        <J5_z / number density>

    is momentum dependent.

    The isotropic angular average for momentum magnitude p is

        m/E
        +
        p^2 / [3 E (E+m)].

    This function averages that expression over a zero-temperature Fermi
    sphere.

    mass_over_pf is

        m_psi / p_F.
    """

    mu = float(
        mass_over_pf
    )

    if mu < 0.0:
        raise ValueError(
            "mass_over_pf must be nonnegative"
        )

    if mu == 0.0:
        return 1.0 / 3.0

    nodes, weights = (
        np.polynomial.legendre.leggauss(
            int(order)
        )
    )

    p = (
        0.5
        * (
            nodes
            + 1.0
        )
    )

    w = (
        0.5
        * weights
    )

    energy = np.sqrt(
        p**2
        + mu**2
    )

    local = (
        mu / energy
        +
        p**2
        / (
            3.0
            * energy
            * (
                energy
                + mu
            )
        )
    )

    return float(
        3.0
        * np.sum(
            w
            * p**2
            * local
        )
    )


def fermi_average_energy_ev(
    p_f_ev: float,
    mass_ev: float,
) -> float:
    """Return exact average total energy per zero-temperature fermion."""

    p_f = float(
        p_f_ev
    )

    mass = float(
        mass_ev
    )

    if p_f <= 0.0 or mass < 0.0:
        raise ValueError(
            "invalid Fermi momentum or mass"
        )

    if mass == 0.0:
        return (
            0.75
            * p_f
        )

    root = math.sqrt(
        p_f**2
        + mass**2
    )

    integral = (
        0.125
        * (
            p_f
            * root
            * (
                2.0
                * p_f**2
                + mass**2
            )
            -
            mass**4
            * math.asinh(
                p_f / mass
            )
        )
    )

    return (
        3.0
        * integral
        / p_f**3
    )


def fermi_pressure_per_particle_ev(
    p_f_ev: float,
    mass_ev: float,
    order: int = 96,
) -> float:
    """Return P/n in eV for a zero-temperature one-spin-state Fermi gas."""

    p_f = float(
        p_f_ev
    )

    mass = float(
        mass_ev
    )

    if p_f <= 0.0 or mass < 0.0:
        raise ValueError(
            "invalid Fermi momentum or mass"
        )

    nodes, weights = (
        np.polynomial.legendre.leggauss(
            int(order)
        )
    )

    p = (
        0.5
        * p_f
        * (
            nodes
            + 1.0
        )
    )

    w = (
        0.5
        * p_f
        * weights
    )

    energy = np.sqrt(
        p**2
        + mass**2
    )

    numerator = np.sum(
        w
        * p**4
        / (
            3.0
            * energy
        )
    )

    denominator = (
        p_f**3
        / 3.0
    )

    return float(
        numerator
        / denominator
    )


def spheroid_surface_kernel(
    points_m: np.ndarray,
    *,
    a_m: float,
    c_m: float,
    n_t: int = 40,
    n_phi: int = 64,
) -> tuple[np.ndarray, np.ndarray]:
    """Return unit-polarization gradient and Hessian at exterior points.

    Coordinates
    -----------
    The source spheroid is centered at

        z = -c

    and therefore occupies

        -2c <= z <= 0.

    The payload is above z=0.

    For unit polarization along z the surface-source measure simplifies to

        n_z dA
        =
        a^2 t dt dphi,

    where

        t = cos(theta).

    Returns
    -------
    gradient_shape:
        Array shape (N, 3), dimensionless.

    hessian_shape_per_m:
        Array shape (N, 3, 3), units 1/m.

    The physical scalar gradient is

        grad(phi)
        =
        q M^2 gradient_shape

    where

        q
        =
        J5 / (f_psi M^2).
    """

    points = np.asarray(
        points_m,
        dtype=float,
    )

    if (
        points.ndim != 2
        or points.shape[1] != 3
    ):
        raise ValueError(
            "points_m must have shape (N,3)"
        )

    a = float(
        a_m
    )

    c = float(
        c_m
    )

    if a <= 0.0 or c <= 0.0:
        raise ValueError(
            "source dimensions must be positive"
        )

    t, weights_t = (
        np.polynomial.legendre.leggauss(
            int(n_t)
        )
    )

    phi = np.linspace(
        0.0,
        2.0 * math.pi,
        int(n_phi),
        endpoint=False,
    )

    weight_phi = (
        2.0
        * math.pi
        / int(n_phi)
    )

    sin_theta = np.sqrt(
        np.maximum(
            0.0,
            1.0 - t**2,
        )
    )

    tt = np.repeat(
        t,
        int(n_phi),
    )

    ss = np.repeat(
        sin_theta,
        int(n_phi),
    )

    ww = (
        np.repeat(
            weights_t,
            int(n_phi),
        )
        * weight_phi
    )

    pp = np.tile(
        phi,
        int(n_t),
    )

    source = np.stack(
        (
            a
            * ss
            * np.cos(pp),

            a
            * ss
            * np.sin(pp),

            -c
            + c * tt,
        ),
        axis=1,
    )

    oriented_measure = (
        a**2
        * tt
        * ww
    )

    gradients: list[
        np.ndarray
    ] = []

    hessians: list[
        np.ndarray
    ] = []

    identity = np.eye(
        3
    )

    for point in points:
        displacement = (
            point
            - source
        )

        radius2 = np.sum(
            displacement**2,
            axis=1,
        )

        if np.any(
            radius2 <= 0.0
        ):
            raise ValueError(
                "evaluation point intersects source surface"
            )

        radius = np.sqrt(
            radius2
        )

        factor = (
            oriented_measure
            / (
                4.0
                * math.pi
            )
        )

        inverse_r3 = (
            radius**-3
        )

        inverse_r5 = (
            radius**-5
        )

        gradient = np.sum(
            (
                factor
                * inverse_r3
            )[:, None]
            * displacement,
            axis=0,
        )

        hessian = (
            identity
            * np.sum(
                factor
                * inverse_r3
            )
            -
            3.0
            * np.einsum(
                "n,ni,nj->ij",
                factor
                * inverse_r5,
                displacement,
                displacement,
            )
        )

        gradients.append(
            gradient
        )

        hessians.append(
            hessian
        )

    return (
        np.asarray(
            gradients
        ),
        np.asarray(
            hessians
        ),
    )


def required_q2_for_surface(
    gradients: np.ndarray,
    hessians_per_m: np.ndarray,
    *,
    target_acceleration_m_s2: float,
) -> float:
    """Return minimum q^2 satisfying the +z acceleration at all points."""

    gradients = np.asarray(
        gradients,
        dtype=float,
    )

    hessians = np.asarray(
        hessians_per_m,
        dtype=float,
    )

    target = float(
        target_acceleration_m_s2
    )

    if target <= 0.0:
        raise ValueError(
            "target acceleration must be positive"
        )

    hg = np.einsum(
        "nij,nj->ni",
        hessians,
        gradients,
    )

    linear_kernel = (
        -C_LIGHT**2
        * hg[:, 2]
    )

    y_kernel = (
        0.5
        * np.sum(
            gradients**2,
            axis=1,
        )
    )

    denominator = (
        linear_kernel
        -
        target
        * y_kernel
    )

    if np.any(
        denominator <= 0.0
    ):
        return math.inf

    required = (
        target
        / denominator
    )

    return float(
        np.max(
            required
        )
    )


def axial_accelerations_m_s2(
    gradients: np.ndarray,
    hessians_per_m: np.ndarray,
    *,
    q2: float,
) -> np.ndarray:
    """Return +z physical-metric acceleration for declared q^2."""

    gradients = np.asarray(
        gradients,
        dtype=float,
    )

    hessians = np.asarray(
        hessians_per_m,
        dtype=float,
    )

    q_squared = float(
        q2
    )

    hg = np.einsum(
        "nij,nj->ni",
        hessians,
        gradients,
    )

    y = (
        0.5
        * q_squared
        * np.sum(
            gradients**2,
            axis=1,
        )
    )

    return (
        -C_LIGHT**2
        * q_squared
        * hg[:, 2]
        / (
            1.0
            + y
        )
    )


def spheroid_total_scalar_energy_j(
    *,
    q2: float,
    metric_scale_ev: float,
    a_m: float,
    c_m: float,
) -> float:
    """Return complete all-space canonical scalar-gradient energy.

    For a uniformly polarized ellipsoid,

        E_phi
        =
        1/2
        N_z
        (q M^2)^2
        V.

    This includes both interior and exterior scalar-gradient energy.
    """

    q_squared = float(
        q2
    )

    metric_scale = float(
        metric_scale_ev
    )

    if q_squared < 0.0 or metric_scale <= 0.0:
        raise ValueError(
            "invalid q2 or metric scale"
        )

    return (
        0.5
        * spheroid_demag_z(
            a_m,
            c_m,
        )
        * q_squared
        * ev4_energy_density_j_m3(
            metric_scale
        )
        * spheroid_volume_m3(
            a_m,
            c_m,
        )
    )


def hidden_fermion_inventory_floor(
    *,
    q: float,
    metric_scale_ev: float,
    a_m: float,
    c_m: float,
    hard_scale_margin: float,
    mass_over_pf: float,
) -> dict[str, float]:
    """Return hidden-fermion source inventory and support lower bound.

    The source current is

        J5
        =
        eta_A n,

    so

        q
        =
        eta_A n
        /
        (f_psi M^2).

    The one-spin-state Fermi momentum is

        p_F
        =
        (6 pi^2 n)^(1/3).

    The NDA source cutoff is

        Lambda_src
        =
        4 pi f_psi.

    We choose the smallest f_psi satisfying

        Lambda_src
        /
        max(p_F, m_psi)
        =
        hard_scale_margin.

    This deliberately minimizes source energy and is therefore an optimistic
    source-realization floor.

    The support floor uses static Laue balance plus DEC:

        E_support
        >=
        P V.

    It is only a lower bound, not a constructed support.
    """

    q_value = float(
        q
    )

    metric_scale = float(
        metric_scale_ev
    )

    safety = float(
        hard_scale_margin
    )

    mu = float(
        mass_over_pf
    )

    if (
        q_value <= 0.0
        or metric_scale <= 0.0
        or safety <= 0.0
        or mu < 0.0
    ):
        raise ValueError(
            "invalid source inventory parameter"
        )

    eta = axial_current_efficiency(
        mu
    )

    hard_ratio = max(
        1.0,
        mu,
    )

    f_psi = (
        metric_scale
        * math.sqrt(
            3.0
            * q_value
            /
            (
                32.0
                * math.pi
                * eta
            )
        )
        * (
            safety
            * hard_ratio
        ) ** 1.5
    )

    number_density_nat = (
        q_value
        * f_psi
        * metric_scale**2
        / eta
    )

    p_f = (
        6.0
        * math.pi**2
        * number_density_nat
    ) ** (
        1.0 / 3.0
    )

    mass = (
        mu
        * p_f
    )

    cutoff = (
        4.0
        * math.pi
        * f_psi
    )

    hard_scale = max(
        p_f,
        mass,
    )

    volume = (
        spheroid_volume_m3(
            a_m,
            c_m,
        )
    )

    volume_nat = (
        volume
        / HBARC_EV_M**3
    )

    particle_number = (
        number_density_nat
        * volume_nat
    )

    average_energy = (
        fermi_average_energy_ev(
            p_f,
            mass,
        )
    )

    average_pressure = (
        fermi_pressure_per_particle_ev(
            p_f,
            mass,
        )
    )

    fermion_energy = (
        particle_number
        * average_energy
        * EV_J
    )

    pressure_support_floor = (
        particle_number
        * average_pressure
        * EV_J
    )

    gp_equivalent = (
        2.0
        * mass
        / f_psi
    )

    loop_proxy = (
        gp_equivalent**2
        /
        (
            16.0
            * math.pi**2
        )
    )

    return {
        "axial_efficiency":
            eta,

        "f_psi_ev":
            f_psi,

        "p_f_ev":
            p_f,

        "m_psi_ev":
            mass,

        "nda_cutoff_ev":
            cutoff,

        "hard_scale_ev":
            hard_scale,

        "hard_scale_margin":
            cutoff
            / hard_scale,

        "particle_number":
            particle_number,

        "number_density_nat_ev3":
            number_density_nat,

        "average_fermion_energy_ev":
            average_energy,

        "fermion_energy_j":
            fermion_energy,

        "pressure_per_particle_ev":
            average_pressure,

        "laue_dec_pressure_support_floor_j":
            pressure_support_floor,

        "gp_equivalent":
            gp_equivalent,

        "loop_proxy_gp2_over_16pi2":
            loop_proxy,
    }


def ordinary_electron_rest_energy_floor_j(
    *,
    q: float,
    metric_scale_ev: float,
    a_m: float,
    c_m: float,
    hard_scale_margin: float,
    electron_mass_ev: float = 510998.95,
) -> dict[str, float]:
    """Return an extremely optimistic ordinary-electron source lower bound.

    We set axial efficiency to its maximal possible value of one and ignore
    Fermi energy, material ions, polarization hardware, and support.

    The source coupling scale is bounded only by requiring

        4 pi f_e
        >=
        hard_scale_margin * m_e.

    If even this optimistic rest-energy inventory is above the target, the
    ordinary-electron source is decisively unattractive.
    """

    q_value = float(
        q
    )

    metric_scale = float(
        metric_scale_ev
    )

    safety = float(
        hard_scale_margin
    )

    mass = float(
        electron_mass_ev
    )

    f_e = (
        safety
        * mass
        /
        (
            4.0
            * math.pi
        )
    )

    volume_nat = (
        spheroid_volume_m3(
            a_m,
            c_m,
        )
        / HBARC_EV_M**3
    )

    particle_number = (
        q_value
        * f_e
        * metric_scale**2
        * volume_nat
    )

    rest_energy = (
        particle_number
        * mass
        * EV_J
    )

    return {
        "f_e_ev":
            f_e,

        "particle_number":
            particle_number,

        "optimistic_rest_energy_floor_j":
            rest_energy,
    }
