"""032V19R6 companion-operator positivity and empirical-scale gate.

PURPOSE
-------
R5 falsified the current pure-j=0 kinetic-conformal coefficient through an
off-state two-scalar material Casimir force.

R6 asks two narrower questions.

1. Can the dimension-eight traceless j=2 MATTER companion reduce that force
   while preserving the static outward coefficient?

2. How small must the static coefficient itself become to satisfy the R5
   finite-film Casimir measurement?

The resulting empirical coefficient ceiling is then handed to the exact V17
finite-payload source evaluator by the R6 simulation.

J0 + J2 NONRELATIVISTIC DECOMPOSITION
-------------------------------------
Use the matter operator basis

    C0 X T
    +
    C2
    (
        partial_mu phi partial_nu phi
        -
        1/4 eta_mu_nu X
    )
    T^{mu nu}.

For nonrelativistic matter at rest,

    T^{00} ~= rho,
    T^{ij} ~= 0.

The quadratic scalar coefficients are then

    C_t
        =
        C0 + 3 C2/4

    C_s
        =
        C0 - C2/4.

C_s is the coefficient multiplying the static spatial-gradient response.

If C_s is held fixed at the value required for antigravity,

    C0
        =
        C_s + C2/4

and therefore

    C_t
        =
        C_s + C2.

MATERIAL KINETIC FACTORS
------------------------
For rest-energy density rho in natural units,

    Z_t
        =
        1 + 2 rho C_t

    Z_s
        =
        1 + 2 rho C_s.

At an Euclidean planar interface the vacuum and material decay constants are

    kappa_0^2
        =
        k_perp^2 + xi^2

    kappa_m^2
        =
        k_perp^2
        +
        (Z_t/Z_s) xi^2.

The scalar reflection amplitude is

    r
        =
        (
            Z_s kappa_m - kappa_0
        )
        /
        (
            Z_s kappa_m + kappa_0
        ).

For the positivity-compatible fermionic j=2 sign

    C2 >= 0,

one has

    Z_t >= Z_s

and hence

    kappa_m >= kappa_0.

Therefore, for fixed positive static C_s,

    r(C2 >= 0)
        >=
        r(C2 = 0).

The same ordering survives a finite slab because

    r_slab
        =
        r
        (1-exp(-2 kappa_m t))
        /
        (1-r^2 exp(-2 kappa_m t))

is monotone in both r and kappa_m for

    0 <= r < 1.

Thus a positivity-compatible matter j=2 companion cannot reduce the R5
scalar reflection while preserving the same static outward response.

A reduction through this operator alone requires C2 < 0.

LITERATURE SCOPE
----------------
Jiang et al., JHEP 08 (2024) 114, organize the dimension-eight matter
operators into j=0 and traceless j=2 sectors and obtain the forward
positivity condition

    C2 >= 0.

Their leading forward positivity analysis does not constrain C1.

This module applies that sign result only to the corresponding healthy
dimension-eight matter j=2 sector.

It is NOT a theorem covering every possible additional field/operator.

EMPIRICAL C_s CEILING
---------------------
R5 already implements the nonperturbative homogeneous-material resummation
and the finite 180-nm / 210-nm Au films.

At 200 nm the empirical reference is

    measured
        =
        0.51050 Pa

    standard theory
        =
        0.51126 Pa

    95 percent halfwidth
        =
        0.00840 Pa.

Because the new scalar force is attractive, the largest additional pressure
consistent with that interval is

    P_extra,max
        =
        measured
        +
        halfwidth
        -
        standard theory.

The largest C_s whose finite-film pressure equals this residual is an
optimistic upper bound because positivity-compatible C2 can only increase the
reflection at fixed C_s.

CLAIM LIMITS
------------
A red result closes only the current tested universal dimension-eight
j=0 plus positivity-compatible matter-j=2 cancellation route.

It does not close arbitrary nonlinear material screening, additional light
states, photon-sector cancellation, or fundamentally different low-energy
physics.

No negative mass is used.
"""

from __future__ import annotations

import math

from scipy.optimize import brentq

from antigravity_research.agminer.two_scalar_quantum_force import (
    matter_loading_from_c1,
    metric_scale_from_c1_ev,
    scalar_casimir_pressure_pa,
)


def fixed_static_j0_j2_coefficients(
    *,
    static_spatial_c_ev_m4: float,
    j2_c_ev_m4: float,
) -> dict[str, float | bool]:
    """Return C0, Ct, and Cs while holding the static response fixed."""

    c_s = float(
        static_spatial_c_ev_m4
    )

    c2 = float(
        j2_c_ev_m4
    )

    if c_s <= 0.0:
        raise ValueError(
            "positive static spatial coefficient required"
        )

    c0 = (
        c_s
        +
        0.25
        * c2
    )

    c_t = (
        c_s
        +
        c2
    )

    return {
        "c0_ev_m4":
            c0,

        "c2_ev_m4":
            c2,

        "c_t_ev_m4":
            c_t,

        "c_s_ev_m4":
            c_s,

        "static_outward_coefficient_preserved":
            True,

        "jiang_forward_positivity_compatible":
            (
                c2 >= 0.0
            ),
    }


def material_j0_j2_kinetic_factors(
    *,
    rho_ev4: float,
    static_spatial_c_ev_m4: float,
    j2_c_ev_m4: float,
) -> dict[str, float | bool]:
    """Return temporal and spatial kinetic factors in NR matter."""

    rho = float(
        rho_ev4
    )

    if rho <= 0.0:
        raise ValueError(
            "positive matter density required"
        )

    coefficients = (
        fixed_static_j0_j2_coefficients(
            static_spatial_c_ev_m4=
                static_spatial_c_ev_m4,

            j2_c_ev_m4=
                j2_c_ev_m4,
        )
    )

    z_t = (
        1.0
        +
        2.0
        * rho
        * float(
            coefficients[
                "c_t_ev_m4"
            ]
        )
    )

    z_s = (
        1.0
        +
        2.0
        * rho
        * float(
            coefficients[
                "c_s_ev_m4"
            ]
        )
    )

    return {
        **coefficients,

        "z_t":
            z_t,

        "z_s":
            z_s,

        "z_t_ge_z_s":
            (
                z_t
                >=
                z_s
            ),

        "positive_temporal_kinetic":
            (
                z_t
                > 0.0
            ),

        "positive_spatial_kinetic":
            (
                z_s
                > 0.0
            ),
    }


def normalized_planar_reflection(
    *,
    z_t: float,
    z_s: float,
    xi_over_kappa0: float,
) -> dict[str, float]:
    """Return interface reflection with kappa0 normalized to unity.

    xi_over_kappa0 lies in [0,1].

    Then

        k_perp^2/kappa0^2
            =
            1-u^2

    and

        kappa_m/kappa0
            =
            sqrt(
                1-u^2
                +
                (Z_t/Z_s) u^2
            ).
    """

    zt = float(
        z_t
    )

    zs = float(
        z_s
    )

    u = float(
        xi_over_kappa0
    )

    if (
        zt <= 0.0
        or zs <= 0.0
        or not (
            0.0
            <= u
            <= 1.0
        )
    ):
        raise ValueError(
            "invalid planar-reflection input"
        )

    kappa_ratio = math.sqrt(
        1.0
        -
        u**2
        +
        (
            zt
            / zs
        )
        * u**2
    )

    reflection = (
        zs
        * kappa_ratio
        -
        1.0
    ) / (
        zs
        * kappa_ratio
        +
        1.0
    )

    pure_j0_lower = (
        zs
        -
        1.0
    ) / (
        zs
        +
        1.0
    )

    return {
        "kappa_m_over_kappa0":
            kappa_ratio,

        "reflection":
            reflection,

        "pure_j0_reflection_at_same_static_cs":
            pure_j0_lower,

        "reflection_minus_pure_j0":
            reflection
            -
            pure_j0_lower,
    }


def normalized_finite_slab_reflection(
    *,
    z_t: float,
    z_s: float,
    xi_over_kappa0: float,
    kappa0_times_thickness: float,
) -> dict[str, float]:
    """Return finite-slab reflection in dimensionless variables."""

    tau = float(
        kappa0_times_thickness
    )

    if tau <= 0.0:
        raise ValueError(
            "positive slab optical thickness required"
        )

    interface = (
        normalized_planar_reflection(
            z_t=
                z_t,

            z_s=
                z_s,

            xi_over_kappa0=
                xi_over_kappa0,
        )
    )

    r_value = float(
        interface[
            "reflection"
        ]
    )

    kappa_ratio = float(
        interface[
            "kappa_m_over_kappa0"
        ]
    )

    attenuation = math.exp(
        -2.0
        * kappa_ratio
        * tau
    )

    slab = (
        r_value
        * (
            1.0
            -
            attenuation
        )
        /
        (
            1.0
            -
            r_value**2
            * attenuation
        )
    )

    return {
        **interface,

        "finite_slab_reflection":
            slab,

        "attenuation":
            attenuation,
    }


def positivity_companion_cancellation_gate(
    *,
    rho_ev4: float,
    static_spatial_c_ev_m4: float,
    j2_c_ev_m4: float,
    xi_over_kappa0: float,
) -> dict[str, float | bool]:
    """Test whether one matter j=2 companion reduces the reflection."""

    factors = (
        material_j0_j2_kinetic_factors(
            rho_ev4=
                rho_ev4,

            static_spatial_c_ev_m4=
                static_spatial_c_ev_m4,

            j2_c_ev_m4=
                j2_c_ev_m4,
        )
    )

    reflection = (
        normalized_planar_reflection(
            z_t=
                float(
                    factors[
                        "z_t"
                    ]
                ),

            z_s=
                float(
                    factors[
                        "z_s"
                    ]
                ),

            xi_over_kappa0=
                xi_over_kappa0,
        )
    )

    reduction = (
        float(
            reflection[
                "reflection_minus_pure_j0"
            ]
        )
        <
        -1.0e-14
    )

    return {
        **factors,
        **reflection,

        "reflection_reduced":
            reduction,

        "positivity_compatible_cancellation":
            bool(
                factors[
                    "jiang_forward_positivity_compatible"
                ]
                and
                reduction
            ),
    }


def allowed_extra_attractive_pressure_pa(
    *,
    measured_pressure_pa: float,
    standard_theory_pressure_pa: float,
    confidence_halfwidth_pa: float,
) -> float:
    """Return largest extra attractive pressure within upper 95% edge."""

    measured = float(
        measured_pressure_pa
    )

    theory = float(
        standard_theory_pressure_pa
    )

    halfwidth = float(
        confidence_halfwidth_pa
    )

    if (
        measured <= 0.0
        or theory <= 0.0
        or halfwidth <= 0.0
    ):
        raise ValueError(
            "positive pressure inputs required"
        )

    residual = (
        measured
        +
        halfwidth
        -
        theory
    )

    return max(
        0.0,
        residual,
    )


def finite_gold_film_static_c_cap(
    *,
    current_c_ev_m4: float,
    gold_density_kg_m3: float,
    separation_m: float,
    sphere_gold_thickness_m: float,
    plate_gold_thickness_m: float,
    measured_pressure_pa: float,
    standard_theory_pressure_pa: float,
    confidence_halfwidth_pa: float,
) -> dict[str, float | bool]:
    """Solve the optimistic pure-j0 finite-film empirical C_s ceiling."""

    current_c = float(
        current_c_ev_m4
    )

    if current_c <= 0.0:
        raise ValueError(
            "positive current coefficient required"
        )

    allowed = (
        allowed_extra_attractive_pressure_pa(
            measured_pressure_pa=
                measured_pressure_pa,

            standard_theory_pressure_pa=
                standard_theory_pressure_pa,

            confidence_halfwidth_pa=
                confidence_halfwidth_pa,
        )
    )

    if allowed <= 0.0:
        raise RuntimeError(
            "no positive extra attractive pressure allowed"
        )

    def pressure_for(
        coefficient: float,
    ) -> float:
        return float(
            scalar_casimir_pressure_pa(
                c1_ev_m4=
                    float(
                        coefficient
                    ),

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
            )[
                "pressure_magnitude_pa"
            ]
        )

    current_pressure = (
        pressure_for(
            current_c
        )
    )

    if current_pressure <= allowed:
        return {
            "current_coefficient_already_allowed":
                True,

            "allowed_extra_pressure_pa":
                allowed,

            "current_extra_pressure_pa":
                current_pressure,

            "static_c_cap_ev_m4":
                current_c,

            "metric_scale_min_ev":
                metric_scale_from_c1_ev(
                    current_c
                ),

            "current_over_cap":
                1.0,
        }

    low = (
        current_c
        * 1.0e-9
    )

    cap = brentq(
        lambda value:
            pressure_for(
                value
            )
            -
            allowed,

        low,
        current_c,
        xtol=
            1.0e-32,
        rtol=
            1.0e-13,
    )

    metric_min = (
        metric_scale_from_c1_ev(
            cap
        )
    )

    cap_load = (
        matter_loading_from_c1(
            c1_ev_m4=
                cap,

            density_kg_m3=
                gold_density_kg_m3,
        )
    )

    return {
        "current_coefficient_already_allowed":
            False,

        "allowed_extra_pressure_pa":
            allowed,

        "current_extra_pressure_pa":
            current_pressure,

        "static_c_cap_ev_m4":
            cap,

        "metric_scale_min_ev":
            metric_min,

        "current_over_cap":
            current_c
            / cap,

        "cap_gold_epsilon":
            float(
                cap_load[
                    "epsilon"
                ]
            ),

        "cap_gold_z":
            float(
                cap_load[
                    "z_factor"
                ]
            ),

        "cap_gold_reflection":
            float(
                cap_load[
                    "interface_reflection"
                ]
            ),

        "positive_j2_can_only_tighten_this_cap":
            True,
    }
