"""032V22 localized time-gradient disformal / provenance-repair helpers.

PURPOSE
-------
V21 established:

- a new X-dependent time-gradient disformal outward sign;
- cheap local spatial-gradient energy;
- failure of the canonical smooth stationary GLOBAL-q realization;
- the full time-gradient disformal family remains open.

V22 tests the genuinely different localized/time-dependent remainder

    phi(t,r)
        =
        q f(r) t
        +
        psi(r),

and repairs V20's nonmetricity ranking provenance.

The V20 family labelled

    PROPAGATING_NONMETRICITY_HEALTHY_SINGLE_MODE

is not a new untested family.

032T already tested the Mikura-Percacci healthy symmetric-MAG free-spectrum
class under minimal ordinary-matter coupling and found

    ordinary Q source = 0
    Q response = 0
    neutral-matter response = ordinary attractive GR.

032U then proved that ordinary symmetric T_munu alone cannot provide a local
linear rank-three static monopole.  Its derivative multipole and genuinely
new intrinsic-hypermomentum branches remain open.

LOCALIZED q KINEMATICS
----------------------
Take a spherical active plateau

    f(R)=1

and switch to

    f(R+delta)=0.

Minimizing

    integral r^2 f'(r)^2 dr

gives

    f'(r)
        =
        - R(R+delta)/(delta r^2).

The largest slope is at the inner wall,

    |f'(R)|
        =
        (R+delta)/(R delta).

For

    phi
        =
        q f(r) t

the time-dependent spatial gradient grows as

    |grad phi|_wall
        =
        q c t |f'|.

If it is capped by

    chi Lambda^2,

the corresponding hold-time scout is

    tau
        =
        chi Lambda^2 R delta
        /
        [q c (R+delta)].

The canonical wall-gradient inventory at that moment is

    E_wall
        =
        2 pi chi^2 Lambda^4
        R^3 delta/(R+delta).

Natural-unit eV^4 is converted to J/m^3.

This is a FIELD INVENTORY.

    E_wall/tau

is therefore labelled only a characteristic field-energy swing rate.
It is not automatically dissipated power.

OFF-STATE QUARTIC DISFORMAL NATURALNESS
---------------------------------------
For the V21 scaffold

    gtilde_mu_nu
        =
        g_mu_nu
        +
        [X/M_*^8]
        partial_mu(phi)
        partial_nu(phi),

the q=0 matter coupling begins quartically in scalar fluctuations.

In Euclidean notation, the relevant schematic interaction is

    1/(4 M_*^8)
    T^{mu nu}
    (partial phi)^2
    partial_mu(phi)
    partial_nu(phi).

Split phi into low and high momentum modes and use a rotational hard cutoff.

For one high-mode contraction,

    <partial_a H partial_b H>
        =
        I delta_ab,

    I
        =
        Lambda_UV^4/(128 pi^2).

The two-low-mode contraction contains a constant-disformal term whose metric
coefficient is

    B_ind
        =
        Lambda_UV^4
        /
        (32 pi^2 M_*^8).

There is also a trace-type quadratic term.

IMPORTANT:
This is a Wilsonian HARD-CUTOFF NATURALNESS SCOUT.

It is NOT claimed to be a scheme-independent renormalized observable.
A UV matching counterterm or an explicit protection mechanism can alter the
low-energy coefficient.

Therefore a red result below closes only the declared UNPROTECTED
SINGLE-SCALE realization.

CONSTANT-DISFORMAL MATERIAL RESPONSE
------------------------------------
For

    gtilde
        =
        g
        +
        B dphi dphi

and nonrelativistic matter at rest,

    Z_t
        =
        1 + rho B,

    Z_s
        =
        1.

The finite-slab scalar Casimir calculation therefore differs from both:

- R5 pure-j0 isotropic loading;
- V21 timelike-background anisotropic loading.

The same declared 200-nm finite-Au-film residual is used as a conservative
off-state empirical scout.

OPTIMISTIC LOCALIZED ENERGY FLOOR
---------------------------------
For an unprotected single-scale scaffold,

    Lambda_UV = M_*.

The active coefficient is

    K
        =
        q^2/M_*^8.

At fixed M_* and K,

    q^2
        =
        K M_*^8.

V22 charges only:

1. canonical q energy inside ONE 10-cm payload volume;
2. the V21 spherical-exponential psi-gradient energy needed for 1g.

It omits wall, microscopic source, support, activation/reset, radiation and
backreaction costs.

Therefore:

    E_localized_floor

is an optimistic PARTIAL LOWER BOUND.

If even that exceeds 10 MJ, the declared single-scale branch fails.

CLAIM LIMITS
------------
No result here establishes that the R1 hidden-axial source realizes the V21
spatial-gradient profile.

The near equality of

    b f_psi

and

    sqrt(S2)

is recorded only as a dimensional coincidence.

    MICROSCOPIC_SOURCE_MATCH = FALSE

until an explicit action/profile calculation proves otherwise.

No negative mass is used.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq, minimize_scalar

from .storage import Storage
from .time_gradient_disformal import (
    C_LIGHT,
    ev4_to_j_m3,
    required_s2_for_exponential_acceleration,
    spherical_exponential_gradient_energy_j,
)


PI = math.pi

HBARC_EV_M = 1.973269804e-7
EV_J = 1.602176634e-19


def density_kg_m3_to_ev4(
    density_kg_m3: float,
) -> float:
    """Convert rest-mass density to eV^4."""

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


def _finite_slab_pressure_from_factors_pa(
    *,
    z_t_1: float,
    z_s_1: float,
    z_t_2: float,
    z_s_2: float,
    separation_m: float,
    thickness1_m: float,
    thickness2_m: float,
    y_order: int = 72,
    u_order: int = 56,
    y_max: float = 65.0,
) -> float:
    """Return scalar finite-slab pressure for constant anisotropic factors."""

    zt1 = float(
        z_t_1
    )
    zs1 = float(
        z_s_1
    )
    zt2 = float(
        z_t_2
    )
    zs2 = float(
        z_s_2
    )

    d = float(
        separation_m
    )
    t1 = float(
        thickness1_m
    )
    t2 = float(
        thickness2_m
    )

    if (
        zt1 <= 0.0
        or zs1 <= 0.0
        or zt2 <= 0.0
        or zs2 <= 0.0
        or d <= 0.0
        or t1 <= 0.0
        or t2 <= 0.0
    ):
        raise ValueError(
            "positive material and geometry parameters required"
        )

    y_nodes, y_weights = leggauss(
        int(
            y_order
        )
    )

    u_nodes, u_weights = leggauss(
        int(
            u_order
        )
    )

    y = (
        0.5
        * y_max
        * (
            y_nodes
            + 1.0
        )
    )

    wy = (
        0.5
        * y_max
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

    yg = y[
        :,
        None,
    ]

    ug = u[
        None,
        :,
    ]

    def slab(
        z_t: float,
        z_s: float,
        thickness: float,
    ) -> np.ndarray:
        kappa_ratio = np.sqrt(
            1.0
            -
            ug**2
            +
            (
                z_t
                / z_s
            )
            * ug**2
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
            -yg
            * kappa_ratio
            * thickness
            / d
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

    r1 = slab(
        zt1,
        zs1,
        t1,
    )

    r2 = slab(
        zt2,
        zs2,
        t2,
    )

    product = (
        r1
        * r2
    )

    exponential = np.exp(
        -yg
    )

    integrand = (
        yg**3
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
            * PI**2
            * d**4
        )
        * integral
    )


def constant_disformal_finite_film_pressure_pa(
    *,
    b_ev_m4: float,
    density1_kg_m3: float,
    density2_kg_m3: float,
    separation_m: float,
    thickness1_m: float,
    thickness2_m: float,
) -> float:
    """Return off-state scalar pressure for a positive constant B."""

    b_value = float(
        b_ev_m4
    )

    if b_value <= 0.0:
        raise ValueError(
            "positive B required"
        )

    rho1 = density_kg_m3_to_ev4(
        density1_kg_m3
    )

    rho2 = density_kg_m3_to_ev4(
        density2_kg_m3
    )

    return (
        _finite_slab_pressure_from_factors_pa(
            z_t_1=
                1.0
                +
                rho1
                * b_value,

            z_s_1=
                1.0,

            z_t_2=
                1.0
                +
                rho2
                * b_value,

            z_s_2=
                1.0,

            separation_m=
                separation_m,

            thickness1_m=
                thickness1_m,

            thickness2_m=
                thickness2_m,
        )
    )


def constant_disformal_empirical_b_cap(
    *,
    gold_density_kg_m3: float,
    separation_m: float,
    sphere_gold_thickness_m: float,
    plate_gold_thickness_m: float,
    allowed_extra_pressure_pa: float,
) -> dict[str, float]:
    """Solve positive constant-B cap from the finite-film residual."""

    allowed = float(
        allowed_extra_pressure_pa
    )

    if allowed <= 0.0:
        raise ValueError(
            "positive residual required"
        )

    def pressure(
        value: float,
    ) -> float:
        return (
            constant_disformal_finite_film_pressure_pa(
                b_ev_m4=
                    value,

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
            1.0e-33,
        rtol=
            1.0e-12,
    )

    rho = density_kg_m3_to_ev4(
        gold_density_kg_m3
    )

    return {
        "b_cap_ev_m4":
            cap,

        "pressure_at_cap_pa":
            pressure(
                cap
            ),

        "gold_z_t_at_cap":
            1.0
            +
            rho
            * cap,

        "gold_z_s_at_cap":
            1.0,
    }


def quartic_disformal_hard_cutoff_descent(
    *,
    metric_scale_ev: float,
    cutoff_ratio: float = 1.0,
) -> dict[str, float | bool | str]:
    """Return hard-cutoff Wilsonian naturalness scout.

    B_ind is the metric-level constant-disformal coefficient.

    The finite renormalized coefficient is NOT predicted.
    """

    scale = float(
        metric_scale_ev
    )

    ratio = float(
        cutoff_ratio
    )

    if (
        scale <= 0.0
        or ratio <= 0.0
    ):
        raise ValueError(
            "positive scales required"
        )

    cutoff = (
        ratio
        * scale
    )

    b_induced = (
        cutoff**4
        /
        (
            32.0
            * PI**2
            * scale**8
        )
    )

    return {
        "metric_scale_ev":
            scale,

        "cutoff_ev":
            cutoff,

        "cutoff_over_metric_scale":
            ratio,

        "induced_constant_disformal_b_ev_m4":
            b_induced,

        "hard_cutoff_naturalness_scout":
            True,

        "scheme_independent_physical_prediction":
            False,

        "renormalized_finite_counterterm_fixed":
            False,

        "protection_mechanism_included":
            False,

        "interpretation":
            "ORDER_OF_MAGNITUDE_WILSONIAN_DESCENT_SCOUT",
    }


def single_scale_minimum_metric_scale_ev(
    *,
    empirical_b_cap_ev_m4: float,
    cutoff_ratio: float = 1.0,
) -> float:
    """Return M_* whose hard-cutoff B_ind reaches empirical cap."""

    cap = float(
        empirical_b_cap_ev_m4
    )

    ratio = float(
        cutoff_ratio
    )

    if (
        cap <= 0.0
        or ratio <= 0.0
    ):
        raise ValueError(
            "positive cap and ratio required"
        )

    return (
        ratio
        * (
            1.0
            /
            (
                32.0
                * PI**2
                * cap
            )
        )**0.25
    )


def minimum_gradient_taper_scout(
    *,
    q2_ev4: float,
    lambda_ev: float,
    active_radius_m: float,
    wall_thickness_m: float,
    chi: float = 1.0,
) -> dict[str, float | bool | str]:
    """Return minimum-gradient taper hold time and field inventory."""

    q2 = float(
        q2_ev4
    )

    scale = float(
        lambda_ev
    )

    radius = float(
        active_radius_m
    )

    wall = float(
        wall_thickness_m
    )

    chi_value = float(
        chi
    )

    if (
        q2 <= 0.0
        or scale <= 0.0
        or radius <= 0.0
        or wall <= 0.0
        or chi_value <= 0.0
    ):
        raise ValueError(
            "positive localized-activation parameters required"
        )

    q = math.sqrt(
        q2
    )

    maximum_slope_m1 = (
        radius
        +
        wall
    ) / (
        radius
        * wall
    )

    hold_time_s = (
        chi_value
        * scale**2
        /
        (
            q
            * C_LIGHT
            * maximum_slope_m1
        )
    )

    wall_energy_j = (
        2.0
        * PI
        * chi_value**2
        * scale**4
        * radius**3
        * wall
        /
        (
            radius
            +
            wall
        )
        * ev4_to_j_m3()
    )

    swing_rate_w = (
        wall_energy_j
        / hold_time_s
    )

    plateau_volume_m3 = (
        4.0
        * PI
        * radius**3
        / 3.0
    )

    plateau_q_energy_j = (
        0.5
        * q2
        * plateau_volume_m3
        * ev4_to_j_m3()
    )

    return {
        "maximum_wall_shape_slope_m1":
            maximum_slope_m1,

        "hold_time_s":
            hold_time_s,

        "wall_gradient_field_inventory_j":
            wall_energy_j,

        "field_energy_swing_rate_w":
            swing_rate_w,

        "field_energy_swing_rate_is_dissipated_power":
            False,

        "plateau_q_energy_j":
            plateau_q_energy_j,

        "wall_profile":
            "MINIMUM_INTEGRAL_R2_FPRIME2",

        "complete_control_ledger":
            False,
    }


def optimistic_localized_partial_floor(
    *,
    metric_scale_ev: float,
    target_acceleration_m_s2: float,
    gradient_scale_m: float,
    payload_radius_m: float,
    source_radius_m: float,
) -> dict[str, float | bool]:
    """Optimize K for the most optimistic canonical localized lower bound.

    Charges only:

        canonical q energy inside one payload sphere
        +
        spherical-exponential psi gradient energy.

    Does not charge:
        wall
        microscopic source
        support
        activation/reset
        radiation
        reaction
        quantum completion.
    """

    scale = float(
        metric_scale_ev
    )

    payload_radius = float(
        payload_radius_m
    )

    if (
        scale <= 0.0
        or payload_radius <= 0.0
    ):
        raise ValueError(
            "positive localized-floor inputs required"
        )

    payload_volume = (
        4.0
        * PI
        * payload_radius**3
        / 3.0
    )

    def state_for_logk(
        log10_k: float,
    ) -> dict[str, float]:
        k_value = (
            10.0**float(
                log10_k
            )
        )

        q2 = (
            k_value
            * scale**8
        )

        far_lapse = (
            1.0
            -
            0.5
            * k_value
            * q2
        )

        if far_lapse <= 0.0:
            return {
                "partial_floor_j":
                    1.0e300,
            }

        try:
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

        except ValueError:
            return {
                "partial_floor_j":
                    1.0e300,
            }

        q_energy_j = (
            0.5
            * q2
            * payload_volume
            * ev4_to_j_m3()
        )

        psi_energy_j = (
            spherical_exponential_gradient_energy_j(
                s2_at_radius_ev4=
                    s2,

                radius_m=
                    source_radius_m,

                decay_scale_m=
                    gradient_scale_m,
            )
        )

        return {
            "k_ev_m4":
                k_value,

            "q2_ev4":
                q2,

            "required_s2_ev4":
                s2,

            "q_payload_volume_energy_j":
                q_energy_j,

            "psi_gradient_energy_j":
                psi_energy_j,

            "partial_floor_j":
                q_energy_j
                +
                psi_energy_j,
        }

    optimum = minimize_scalar(
        lambda logk:
            state_for_logk(
                logk
            )[
                "partial_floor_j"
            ],

        bounds=(
            -32.0,
            -16.0,
        ),

        method=
            "bounded",

        options={
            "xatol":
                1.0e-12,
        },
    )

    state = state_for_logk(
        float(
            optimum.x
        )
    )

    state[
        "metric_scale_ev"
    ] = scale

    state[
        "hard_derivative_scale_ev"
    ] = float(
        state[
            "required_s2_ev4"
        ]
    )**0.25

    state[
        "metric_scale_over_hard_derivative_scale"
    ] = (
        scale
        /
        float(
            state[
                "hard_derivative_scale_ev"
            ]
        )
    )

    state[
        "complete_operating_energy"
    ] = False

    state[
        "microscopic_source_included"
    ] = False

    state[
        "wall_included"
    ] = False

    state[
        "support_included"
    ] = False

    return state


def maximum_cutoff_ratio_for_strict_target(
    *,
    empirical_single_scale_m_ev: float,
    target_energy_j: float,
    target_acceleration_m_s2: float,
    gradient_scale_m: float,
    payload_radius_m: float,
    source_radius_m: float,
) -> dict[str, float]:
    """Solve eta=Lambda_UV/M_* where the optimistic floor hits target.

    Empirical radiative safety permits

        M_* >= eta M_single_scale.

    For minimum energy at each eta we take equality.
    """

    single_scale = float(
        empirical_single_scale_m_ev
    )

    target = float(
        target_energy_j
    )

    if (
        single_scale <= 0.0
        or target <= 0.0
    ):
        raise ValueError(
            "positive threshold inputs required"
        )

    def floor_at_ratio(
        ratio: float,
    ) -> float:
        scale = (
            float(
                ratio
            )
            * single_scale
        )

        return float(
            optimistic_localized_partial_floor(
                metric_scale_ev=
                    scale,

                target_acceleration_m_s2=
                    target_acceleration_m_s2,

                gradient_scale_m=
                    gradient_scale_m,

                payload_radius_m=
                    payload_radius_m,

                source_radius_m=
                    source_radius_m,
            )[
                "partial_floor_j"
            ]
        )

    ratio = brentq(
        lambda value:
            floor_at_ratio(
                value
            )
            -
            target,

        0.05,
        1.0,
        xtol=
            1.0e-10,
        rtol=
            1.0e-10,
    )

    return {
        "maximum_cutoff_over_metric_scale_for_lt_target":
            ratio,

        "floor_at_boundary_j":
            floor_at_ratio(
                ratio
            ),

        "strict_pass_requires_smaller_ratio":
            True,
    }


def source_scale_comparison(
    *,
    axial_b_ev: float,
    axial_fpsi_ev: float,
    required_s2_ev4: float,
) -> dict[str, float | bool | str]:
    """Record dimensional proximity without promoting a source match."""

    axial_scale = (
        float(
            axial_b_ev
        )
        * float(
            axial_fpsi_ev
        )
    )

    disformal_scale = math.sqrt(
        float(
            required_s2_ev4
        )
    )

    relative_difference = (
        abs(
            axial_scale
            -
            disformal_scale
        )
        /
        disformal_scale
    )

    return {
        "axial_b_times_fpsi_ev2":
            axial_scale,

        "disformal_required_gradient_ev2":
            disformal_scale,

        "relative_difference":
            relative_difference,

        "same_units":
            True,

        "same_profile_proved":
            False,

        "same_operator_proved":
            False,

        "microscopic_source_match":
            False,

        "interpretation":
            "DIMENSIONAL_PROXIMITY_ONLY",
    }


def provenance_repair_status() -> dict[str, bool | str]:
    """Return V20 A2 provenance correction."""

    return {
        "v20_a2_was_new_untested_family":
            False,

        "minimal_healthy_symmetric_mag_metric_only_already_tested":
            True,

        "minimal_branch_closed_by_032t":
            True,

        "linear_t_only_rank3_monopole_closed_by_032u":
            True,

        "derivative_multipole_frontier_open":
            True,

        "intrinsic_hypermomentum_frontier_open":
            True,

        "full_metric_affine_gravity_closed":
            False,

        "correct_next_mag_scope":
            "DERIVATIVE_MULTIPOLE_OR_NEW_INTRINSIC_HYPERMOMENTUM_PORTAL",
    }


def _insert_region_rule_if_missing(
    storage: Storage,
    *,
    family: str,
    family_version: str,
    rule_type: str,
    proof_reference: str,
    rule: dict[str, Any],
) -> int:
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

        rule=
            rule,

        proof_reference=
            proof_reference,
    )

    return 1


def persist_v22_rules(
    storage: Storage,
    *,
    single_scale_floor_j: float,
    single_scale_metric_ev: float,
    b_cap_ev_m4: float,
    cutoff_ratio_threshold: float,
) -> int:
    """Persist provenance repair and declared single-scale A1 failure."""

    inserted = 0

    inserted += (
        _insert_region_rule_if_missing(
            storage,

            family=
                "032_V20_A2_PROPAGATING_NONMETRICITY_HEALTHY_SINGLE_MODE",

            family_version=
                "V22_PROVENANCE_REPAIR",

            rule_type=
                "DUPLICATE_PRIOR_032T_032U",

            proof_reference=
                "032V22_A2_PROVENANCE_REPAIR",

            rule={
                "policy_specific":
                    False,

                "rerank_as_new_family":
                    False,

                "minimal_metric_only_branch_closed_by_032t":
                    True,

                "linear_t_only_rank3_monopole_closed_by_032u":
                    True,

                "derivative_multipole_frontier_closed":
                    False,

                "intrinsic_hypermomentum_frontier_closed":
                    False,

                "full_metric_affine_gravity_closed":
                    False,
            },
        )
    )

    inserted += (
        _insert_region_rule_if_missing(
            storage,

            family=
                "032_LOCALIZED_TIME_GRADIENT_DISFORMAL_SINGLE_SCALE",

            family_version=
                "V22",

            rule_type=
                "UNPROTECTED_RADIATIVE_DESCENT_ENERGY_LOWER_BOUND",

            proof_reference=
                "032V22_LOCALIZED_DISFORMAL_NATURALNESS_GATE",

            rule={
                "policy_specific":
                    True,

                "policy":
                    "STRICT_COMPLETE_OPERATING_LT_10MJ",

                "scope":
                    (
                        "CANONICAL_LOCALIZED_Q_GAMMA_X_EQ_X_OVER_M8_"
                        "HARD_CUTOFF_EQUAL_M"
                    ),

                "closed":
                    True,

                "single_scale_metric_min_ev":
                    float(
                        single_scale_metric_ev
                    ),

                "constant_disformal_b_cap_ev_m4":
                    float(
                        b_cap_ev_m4
                    ),

                "optimistic_partial_floor_j":
                    float(
                        single_scale_floor_j
                    ),

                "cutoff_ratio_required_below":
                    float(
                        cutoff_ratio_threshold
                    ),

                "full_localized_time_gradient_family_closed":
                    False,

                "protected_multiscale_completion_closed":
                    False,

                "hard_cutoff_coefficient_is_scheme_independent_prediction":
                    False,

                "negative_mass_required":
                    False,
            },
        )
    )

    return inserted
