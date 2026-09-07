"""032V21 time-gradient X-dependent disformal prefield diagnostics.

PURPOSE
-------
Test the highest-ranked post-V20 AGMINER family:

    SHIFT_SYMMETRIC_TIME_GRADIENT_DISFORMAL_METRIC

without reopening the already-tested 014D-015C constant-B / localized-source
branch.

The minimal genuinely distinct scaffold is

    gtilde_mu_nu
        =
        g_mu_nu
        +
        Gamma(X)
        partial_mu(phi)
        partial_nu(phi),

    X
        =
        -1/2
        g^mu_nu
        partial_mu(phi)
        partial_nu(phi),

with

    Gamma(X)
        =
        beta X/Lambda^8,

and the stationary shift-symmetric ansatz

    phi
        =
        q t
        +
        psi(x).

Define

    Q2 = q^2
    S2 = |grad psi|^2

so that

    X
        =
        (Q2-S2)/2.

Also define the effective background-assisted coefficient

    K
        =
        beta Q2/Lambda^8.

Then

    N^2
        =
        1
        -
        Gamma(X) Q2

        =
        1
        -
        K Q2/2
        +
        K S2/2.

For K>0 and a localized S2 decreasing outward, the direct slow-test-body
lapse acceleration points outward.

This differs from constant disformal B because Gamma_X is nonzero.

STATIONARY-q INTEGRABILITY
--------------------------
If

    partial_t phi = q(x),

then mixed-partial consistency gives

    partial_i phi
        =
        t partial_i q
        +
        partial_i psi.

Therefore a smooth time-independent spatial scalar gradient requires

    partial_i q = 0.

An exactly stationary time-linear q reservoir is thus spatially constant on
a connected regular domain.

A finite local q reservoir must instead be genuinely time dependent,
contain a defect/boundary structure, or use other new physics.

CANONICAL BACKGROUND
--------------------
For the minimal canonical scalar

    P(X)=X,

a homogeneous q background has

    rho_q
        =
        Q2/2

in natural units and equation of state

    w=1.

It is therefore a stiff cosmological component.

MATERIAL QUADRATIC RESPONSE
---------------------------
Expand around the timelike background:

    phi = q t + pi.

For nonrelativistic matter, the quadratic g00 variation of the linear-X
disformal scaffold is

    delta g00^(2)
        =
        K
        [
            3 pi_dot^2
            -
            1/2 |grad pi|^2
        ].

The scalar kinetic factors in homogeneous matter are therefore

    Z_t = 1 + 3 rho K
    Z_s = 1 + rho K/2.

This is anisotropic and is NOT the R5 pure-j0 response.

For Euclidean frequency/transverse momentum,

    kappa_m^2
        =
        k_perp^2
        +
        (Z_t/Z_s) xi^2.

At a vacuum/material interface,

    r
        =
        (
            Z_s kappa_m
            -
            kappa_0
        )
        /
        (
            Z_s kappa_m
            +
            kappa_0
        ).

Finite slabs use the standard multiple-reflection resummation.

DISFORMAL INVERTIBILITY
-----------------------
For

    gtilde = g + Gamma(X) dphi dphi

the metric determinant/signature factor is

    I_metric
        =
        1 - 2 Gamma X.

For Gamma=beta X/Lambda^8,

    I_metric
        =
        1
        -
        2 beta X^2/Lambda^8.

Preserving the Lorentzian branch requires

    I_metric > 0.

The kinetic-invariant map has Jacobian numerator

    I_X
        =
        1
        +
        2 X^2 Gamma_X

        =
        1
        +
        2 beta X^2/Lambda^8.

Thus the relevant failure in the present positive-beta scaffold is the
metric/signature factor, not the X-map Jacobian.

CLAIM LIMITS
------------
A red result here closes only:

    canonical P(X)=X
    +
    smooth stationary global q
    +
    Gamma(X)=beta X/Lambda^8
    +
    the declared 200-nm off-state material gate.

It does not close:

- all time-gradient disformal theories;
- nonlinear/saturating Gamma(X);
- noncanonical low-energy P(X);
- defect-supported q domains;
- explicitly time-dependent activation;
- propagating nonmetricity;
- any other AGMINER family.

No negative mass is used.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq

from .storage import Storage


EV_J = 1.602176634e-19
HBARC_EV_M = 1.973269804e-7

C_LIGHT = 299792458.0
G_NEWTON = 6.67430e-11
MPC_M = 3.085677581491367e22

H0_REFERENCE_KM_S_MPC = 67.4

# Intentionally extremely weak comparison ceiling.
#
# This is NOT the published Planck-level stiff-fluid limit.
LOOSE_OMEGA_STIFF_CEILING = 1.0e-3

# Literature-context value only.
PUBLISHED_STIFF_OMEGA_CONTEXT = 5.0e-23


def ev4_to_j_m3() -> float:
    """Return the natural-unit eV^4 -> J/m^3 conversion."""

    return (
        EV_J
        / HBARC_EV_M**3
    )


def density_kg_m3_to_ev4(
    density_kg_m3: float,
) -> float:
    """Convert rest-mass density to natural-unit energy density."""

    density = float(
        density_kg_m3
    )

    if density <= 0.0:
        raise ValueError(
            "density must be positive"
        )

    return (
        density
        * C_LIGHT**2
        / ev4_to_j_m3()
    )


def critical_energy_density_j_m3(
    *,
    h0_km_s_mpc: float =
        H0_REFERENCE_KM_S_MPC,
) -> float:
    """Return 3 H0^2 c^2/(8 pi G) in J/m^3."""

    h0 = (
        float(
            h0_km_s_mpc
        )
        * 1000.0
        / MPC_M
    )

    if h0 <= 0.0:
        raise ValueError(
            "H0 must be positive"
        )

    rho_mass = (
        3.0
        * h0**2
        /
        (
            8.0
            * math.pi
            * G_NEWTON
        )
    )

    return (
        rho_mass
        * C_LIGHT**2
    )


def stationary_q_integrability(
    *,
    spatial_q_gradient_nonzero: bool,
) -> dict[str, bool | str]:
    """Return the exact mixed-partial stationarity gate."""

    nonzero = bool(
        spatial_q_gradient_nonzero
    )

    return {
        "spatial_q_gradient_nonzero":
            nonzero,

        "stationary_time_independent_spatial_gradient_possible":
            (
                not nonzero
            ),

        "finite_local_stationary_q_reservoir":
            False
            if nonzero
            else
            False,

        "smooth_stationary_q_must_be_spatially_constant":
            True,

        "reason":
            (
                "D_I_PHI_CONTAINS_T_D_I_Q_IF_Q_VARIES_SPATIALLY"
            ),
    }


def constant_gamma_direct_lapse_gradient() -> float:
    """Return direct static lapse-gradient response for constant Gamma.

    With

        phi=q t+psi(x)

    and constant Gamma,

        gtilde_00
            =
            g_00
            +
            Gamma q^2

    has no direct psi-dependent lapse term.

    This preserves the distinction from the old constant-B branch.
    """

    return 0.0


def matching_scale_ev(
    *,
    effective_k_ev_m4: float,
    q2_ev4: float,
    beta: float = 1.0,
) -> float:
    """Return Lambda from K=beta Q2/Lambda^8."""

    k_value = float(
        effective_k_ev_m4
    )

    q2 = float(
        q2_ev4
    )

    beta_value = float(
        beta
    )

    if (
        k_value <= 0.0
        or q2 <= 0.0
        or beta_value <= 0.0
    ):
        raise ValueError(
            "positive K, Q2, and beta required"
        )

    return (
        beta_value
        * q2
        / k_value
    )**0.125


def far_lapse_squared(
    *,
    effective_k_ev_m4: float,
    q2_ev4: float,
) -> float:
    """Return N_infinity^2 for the linear-X scaffold."""

    return (
        1.0
        -
        0.5
        * float(
            effective_k_ev_m4
        )
        * float(
            q2_ev4
        )
    )


def local_lapse_squared(
    *,
    effective_k_ev_m4: float,
    q2_ev4: float,
    s2_ev4: float,
) -> float:
    """Return local N^2."""

    return (
        far_lapse_squared(
            effective_k_ev_m4=
                effective_k_ev_m4,

            q2_ev4=
                q2_ev4,
        )
        +
        0.5
        * float(
            effective_k_ev_m4
        )
        * float(
            s2_ev4
        )
    )


def required_s2_for_exponential_acceleration(
    *,
    effective_k_ev_m4: float,
    q2_ev4: float,
    target_acceleration_m_s2: float,
    gradient_scale_m: float,
) -> float:
    """Solve the exact local lapse equation for an exponential S2 profile.

    Take

        S2(r)
            =
            S2_0 exp[-(r-r0)/h].

    Then

        a
            =
            c^2 K S2
            /
            (4 h N^2).

    Solving exactly for S2 gives

        S2
            =
            A N_inf^2
            /
            [
                K (1-A/2)
            ]

    with

        A=4ah/c^2.
    """

    k_value = float(
        effective_k_ev_m4
    )

    q2 = float(
        q2_ev4
    )

    acceleration = float(
        target_acceleration_m_s2
    )

    scale = float(
        gradient_scale_m
    )

    if (
        k_value <= 0.0
        or q2 <= 0.0
        or acceleration <= 0.0
        or scale <= 0.0
    ):
        raise ValueError(
            "positive response parameters required"
        )

    n_far = (
        far_lapse_squared(
            effective_k_ev_m4=
                k_value,

            q2_ev4=
                q2,
        )
    )

    if n_far <= 0.0:
        raise ValueError(
            "far lapse is non-Lorentzian"
        )

    response = (
        4.0
        * acceleration
        * scale
        / C_LIGHT**2
    )

    if response >= 2.0:
        raise ValueError(
            "requested acceleration leaves weak-device branch"
        )

    return (
        response
        * n_far
        /
        (
            k_value
            * (
                1.0
                -
                0.5
                * response
            )
        )
    )


def acceleration_for_exponential_s2(
    *,
    effective_k_ev_m4: float,
    q2_ev4: float,
    s2_ev4: float,
    gradient_scale_m: float,
) -> float:
    """Return the local slow-test-body acceleration magnitude."""

    k_value = float(
        effective_k_ev_m4
    )

    s2 = float(
        s2_ev4
    )

    scale = float(
        gradient_scale_m
    )

    n2 = (
        local_lapse_squared(
            effective_k_ev_m4=
                k_value,

            q2_ev4=
                q2_ev4,

            s2_ev4=
                s2,
        )
    )

    if (
        k_value <= 0.0
        or s2 <= 0.0
        or scale <= 0.0
        or n2 <= 0.0
    ):
        raise ValueError(
            "invalid local-response state"
        )

    return (
        C_LIGHT**2
        * k_value
        * s2
        /
        (
            4.0
            * scale
            * n2
        )
    )


def disformal_invertibility(
    *,
    effective_k_ev_m4: float,
    q2_ev4: float,
    s2_ev4: float,
    beta: float = 1.0,
) -> dict[str, float | bool]:
    """Return exact metric/signature and X-map margins."""

    k_value = float(
        effective_k_ev_m4
    )

    q2 = float(
        q2_ev4
    )

    s2 = float(
        s2_ev4
    )

    beta_value = float(
        beta
    )

    lambda_ev = (
        matching_scale_ev(
            effective_k_ev_m4=
                k_value,

            q2_ev4=
                q2,

            beta=
                beta_value,
        )
    )

    lambda4 = (
        lambda_ev**4
    )

    lambda8 = (
        lambda_ev**8
    )

    x_value = (
        0.5
        * (
            q2
            -
            s2
        )
    )

    gamma = (
        beta_value
        * x_value
        / lambda8
    )

    metric_margin = (
        1.0
        -
        2.0
        * gamma
        * x_value
    )

    x_map_jacobian_numerator = (
        1.0
        +
        2.0
        * beta_value
        * x_value**2
        / lambda8
    )

    derivative_ratio = (
        s2
        / lambda4
    )

    return {
        "lambda_ev":
            lambda_ev,

        "lambda4_ev4":
            lambda4,

        "x_ev4":
            x_value,

        "gamma_ev_m4":
            gamma,

        "metric_signature_margin":
            metric_margin,

        "x_map_jacobian_numerator":
            x_map_jacobian_numerator,

        "spatial_derivative_expansion_ratio":
            derivative_ratio,

        "lorentzian_invertible_branch":
            (
                metric_margin
                >
                0.0
                and
                x_map_jacobian_numerator
                >
                0.0
            ),
    }


def canonical_background_energy(
    *,
    q2_ev4: float,
    h0_km_s_mpc: float =
        H0_REFERENCE_KM_S_MPC,
) -> dict[str, float]:
    """Return canonical homogeneous q-background energy and Omega."""

    q2 = float(
        q2_ev4
    )

    if q2 <= 0.0:
        raise ValueError(
            "Q2 must be positive"
        )

    density_ev4 = (
        0.5
        * q2
    )

    density_j_m3 = (
        density_ev4
        * ev4_to_j_m3()
    )

    critical = (
        critical_energy_density_j_m3(
            h0_km_s_mpc=
                h0_km_s_mpc,
        )
    )

    return {
        "energy_density_ev4":
            density_ev4,

        "energy_density_j_m3":
            density_j_m3,

        "omega":
            density_j_m3
            / critical,

        "equation_of_state_w":
            1.0,

        "component":
            "CANONICAL_STIFF",
    }


def material_kinetic_factors(
    *,
    density_kg_m3: float,
    effective_k_ev_m4: float,
) -> dict[str, float]:
    """Return Z_t and Z_s around the timelike q background."""

    rho = (
        density_kg_m3_to_ev4(
            density_kg_m3
        )
    )

    k_value = float(
        effective_k_ev_m4
    )

    if k_value <= 0.0:
        raise ValueError(
            "positive K required"
        )

    rho_k = (
        rho
        * k_value
    )

    return {
        "rho_ev4":
            rho,

        "rho_times_k":
            rho_k,

        "z_t":
            1.0
            +
            3.0
            * rho_k,

        "z_s":
            1.0
            +
            0.5
            * rho_k,
    }


def anisotropic_finite_slab_pressure_pa(
    *,
    effective_k_ev_m4: float,
    density1_kg_m3: float,
    density2_kg_m3: float,
    separation_m: float,
    thickness1_m: float,
    thickness2_m: float,
    y_order: int = 64,
    u_order: int = 48,
    y_max: float = 60.0,
) -> float:
    """Return zero-temperature scalar pressure for two finite anisotropic slabs.

    The dimensionless variables are

        y = 2 kappa_0 d
        u = xi/kappa_0.

    The pressure magnitude is

        hbar c
        /(32 pi^2 d^4)
        integral dy y^3
        integral_0^1 du
        R exp(-y)
        /
        [1-R exp(-y)].
    """

    k_value = float(
        effective_k_ev_m4
    )

    separation = float(
        separation_m
    )

    t1 = float(
        thickness1_m
    )

    t2 = float(
        thickness2_m
    )

    if (
        k_value <= 0.0
        or separation <= 0.0
        or t1 <= 0.0
        or t2 <= 0.0
    ):
        raise ValueError(
            "positive slab parameters required"
        )

    state1 = (
        material_kinetic_factors(
            density_kg_m3=
                density1_kg_m3,

            effective_k_ev_m4=
                k_value,
        )
    )

    state2 = (
        material_kinetic_factors(
            density_kg_m3=
                density2_kg_m3,

            effective_k_ev_m4=
                k_value,
        )
    )

    y_nodes, y_weights = (
        leggauss(
            int(
                y_order
            )
        )
    )

    u_nodes, u_weights = (
        leggauss(
            int(
                u_order
            )
        )
    )

    y = (
        0.5
        * float(
            y_max
        )
        * (
            y_nodes
            + 1.0
        )
    )

    wy = (
        0.5
        * float(
            y_max
        )
        * y_weights
    )

    u = (
        0.5
        * (
            u_nodes
            + 1.0
        )
    )

    wu = (
        0.5
        * u_weights
    )

    y_grid = (
        y[
            :,
            None,
        ]
    )

    u_grid = (
        u[
            None,
            :,
        ]
    )

    def slab_reflection(
        state: dict[str, float],
        thickness: float,
    ) -> np.ndarray:
        z_t = float(
            state[
                "z_t"
            ]
        )

        z_s = float(
            state[
                "z_s"
            ]
        )

        kappa_ratio = np.sqrt(
            1.0
            -
            u_grid**2
            +
            (
                z_t
                / z_s
            )
            * u_grid**2
        )

        interface = (
            z_s
            * kappa_ratio
            -
            1.0
        ) / (
            z_s
            * kappa_ratio
            +
            1.0
        )

        attenuation = np.exp(
            -y_grid
            * kappa_ratio
            * thickness
            / separation
        )

        return (
            interface
            * (
                1.0
                -
                attenuation
            )
            /
            (
                1.0
                -
                interface**2
                * attenuation
            )
        )

    r1 = (
        slab_reflection(
            state1,
            t1,
        )
    )

    r2 = (
        slab_reflection(
            state2,
            t2,
        )
    )

    product = (
        r1
        * r2
    )

    exponential = np.exp(
        -y_grid
    )

    integrand = (
        y_grid**3
        * product
        * exponential
        /
        (
            1.0
            -
            product
            * exponential
        )
    )

    integral = float(
        np.sum(
            wy[
                :,
                None,
            ]
            * wu[
                None,
                :,
            ]
            * integrand
        )
    )

    hbar_c_j_m = (
        HBARC_EV_M
        * EV_J
    )

    return (
        hbar_c_j_m
        /
        (
            32.0
            * math.pi**2
            * separation**4
        )
        * integral
    )


def empirical_k_cap(
    *,
    gold_density_kg_m3: float,
    separation_m: float,
    sphere_gold_thickness_m: float,
    plate_gold_thickness_m: float,
    allowed_extra_pressure_pa: float,
) -> dict[str, float]:
    """Solve the finite-film upper K compatible with the declared residual."""

    allowed = float(
        allowed_extra_pressure_pa
    )

    if allowed <= 0.0:
        raise ValueError(
            "positive allowed pressure required"
        )

    def pressure(
        k_value: float,
    ) -> float:
        return (
            anisotropic_finite_slab_pressure_pa(
                effective_k_ev_m4=
                    k_value,

                density1_kg_m3=
                    gold_density_kg_m3,

                density2_kg_m3=
                    gold_density_kg_m3,

                separation_m=
                    separation_m,

                thickness1_m=
                    sphere_gold_thickness_m,

                thickness2_m=
                    plate_gold_thickness_m,
            )
        )

    cap = brentq(
        lambda value:
            pressure(
                value
            )
            -
            allowed,

        1.0e-24,
        1.0e-18,
        xtol=
            1.0e-32,
        rtol=
            1.0e-12,
    )

    material = (
        material_kinetic_factors(
            density_kg_m3=
                gold_density_kg_m3,

            effective_k_ev_m4=
                cap,
        )
    )

    return {
        "k_cap_ev_m4":
            cap,

        "pressure_at_cap_pa":
            pressure(
                cap
            ),

        "gold_rho_times_k":
            material[
                "rho_times_k"
            ],

        "gold_z_t":
            material[
                "z_t"
            ],

        "gold_z_s":
            material[
                "z_s"
            ],
    }


def minimum_q2_for_metric_invertibility(
    *,
    effective_k_ev_m4: float,
    target_acceleration_m_s2: float,
    gradient_scale_m: float,
) -> float:
    """Return Q2 at the Lorentzian metric-signature boundary."""

    k_value = float(
        effective_k_ev_m4
    )

    response = (
        4.0
        * float(
            target_acceleration_m_s2
        )
        * float(
            gradient_scale_m
        )
        / C_LIGHT**2
    )

    approximate = (
        response**2
        /
        (
            2.0
            * k_value
        )
    )

    def margin(
        q2: float,
    ) -> float:
        s2 = (
            required_s2_for_exponential_acceleration(
                effective_k_ev_m4=
                    k_value,

                q2_ev4=
                    q2,

                target_acceleration_m_s2=
                    target_acceleration_m_s2,

                gradient_scale_m=
                    gradient_scale_m,
            )
        )

        return float(
            disformal_invertibility(
                effective_k_ev_m4=
                    k_value,

                q2_ev4=
                    q2,

                s2_ev4=
                    s2,
            )[
                "metric_signature_margin"
            ]
        )

    return (
        brentq(
            margin,
            approximate
            * 0.1,
            approximate
            * 10.0,
            xtol=
                1.0e-30,
            rtol=
                1.0e-12,
        )
    )


def minimum_q2_for_derivative_ratio(
    *,
    effective_k_ev_m4: float,
    target_acceleration_m_s2: float,
    gradient_scale_m: float,
    maximum_ratio: float,
) -> float:
    """Return Q2 required for S2/Lambda^4 <= maximum_ratio."""

    k_value = float(
        effective_k_ev_m4
    )

    ratio_limit = float(
        maximum_ratio
    )

    if ratio_limit <= 0.0:
        raise ValueError(
            "positive derivative ratio required"
        )

    response = (
        4.0
        * float(
            target_acceleration_m_s2
        )
        * float(
            gradient_scale_m
        )
        / C_LIGHT**2
    )

    approximate = (
        response**2
        /
        (
            k_value
            * ratio_limit**2
        )
    )

    def residual(
        q2: float,
    ) -> float:
        s2 = (
            required_s2_for_exponential_acceleration(
                effective_k_ev_m4=
                    k_value,

                q2_ev4=
                    q2,

                target_acceleration_m_s2=
                    target_acceleration_m_s2,

                gradient_scale_m=
                    gradient_scale_m,
            )
        )

        state = (
            disformal_invertibility(
                effective_k_ev_m4=
                    k_value,

                q2_ev4=
                    q2,

                s2_ev4=
                    s2,
            )
        )

        return (
            float(
                state[
                    "spatial_derivative_expansion_ratio"
                ]
            )
            -
            ratio_limit
        )

    return (
        brentq(
            residual,
            approximate
            * 0.1,
            approximate
            * 10.0,
            xtol=
                1.0e-30,
            rtol=
                1.0e-12,
        )
    )


def spherical_exponential_gradient_energy_j(
    *,
    s2_at_radius_ev4: float,
    radius_m: float,
    decay_scale_m: float,
) -> float:
    """Return canonical exterior gradient-energy scout.

    For

        S2(r)
            =
            S2(R)
            exp[-(r-R)/h],

    E_grad
        =
        1/2
        integral_R^infinity
        4 pi r^2 S2(r) dr.
    """

    s2 = float(
        s2_at_radius_ev4
    )

    radius = float(
        radius_m
    )

    scale = float(
        decay_scale_m
    )

    if (
        s2 <= 0.0
        or radius <= 0.0
        or scale <= 0.0
    ):
        raise ValueError(
            "positive gradient profile required"
        )

    radial_integral = (
        radius**2
        * scale

        +
        2.0
        * radius
        * scale**2

        +
        2.0
        * scale**3
    )

    return (
        2.0
        * math.pi
        * s2
        * ev4_to_j_m3()
        * radial_integral
    )


def persist_v21_failure_rule(
    storage: Storage,
    *,
    k_cap_ev_m4: float,
    omega_min_invertible: float,
    omega_loose_ceiling: float,
) -> int:
    """Persist the canonical A1 subbranch closure idempotently."""

    family = (
        "032_TIME_GRADIENT_DISFORMAL_CANONICAL_LINEAR_GAMMA"
    )

    family_version = (
        "V21"
    )

    rule_type = (
        "CASIMIR_COSMOLOGY_INVERTIBILITY_NO_GO"
    )

    proof_reference = (
        "032V21_TIME_GRADIENT_DISFORMAL_PREFLIGHT"
    )

    existing = (
        storage.connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM region_rules
            WHERE family=?
              AND family_version=?
              AND rule_type=?
              AND proof_reference=?
            """,
            (
                family,
                family_version,
                rule_type,
                proof_reference,
            ),
        ).fetchone()
    )

    if (
        existing is not None
        and int(
            existing[
                "count"
            ]
        ) > 0
    ):
        return 0

    storage.add_region_rule(
        family=
            family,

        family_version=
            family_version,

        rule_type=
            rule_type,

        rule={
            "policy_specific":
                False,

            "closed":
                True,

            "scope":
                (
                    "CANONICAL_PX_X_GLOBAL_STATIONARY_Q_"
                    "GAMMA_LINEAR_IN_X"
                ),

            "k_cap_ev_m4":
                float(
                    k_cap_ev_m4
                ),

            "minimum_omega_for_metric_invertibility":
                float(
                    omega_min_invertible
                ),

            "deliberately_loose_omega_stiff_ceiling":
                float(
                    omega_loose_ceiling
                ),

            "stationary_local_q_reservoir":
                False,

            "full_time_gradient_disformal_family_closed":
                False,

            "noncanonical_background_closed":
                False,

            "negative_mass_required":
                False,
        },

        proof_reference=
            proof_reference,
    )

    return 1
