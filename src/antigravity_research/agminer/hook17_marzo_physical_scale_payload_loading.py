"""032H17A10F0 — physical normalization / payload-loading kill gate.

PURPOSE
-------
Before investing in an exact finite-source and finite-payload BVP, restore
absolute scales to the A10D/E protected Marzo 1- carrier and test three cheap
potential showstoppers:

1. Can the ordinary graviton carry its physical Planck normalization while
   the protected massive 1- mode retains a one-metre range without requiring
   an enormous kinetic coefficient c7?

2. Does canonical normalization destroy the A10D source overlap?

3. Does universal quadratic coupling to an ordinary kilogram payload force
   such severe matter loading that every weak-loading field-capacity corridor
   exceeds the strict <10 MJ operating-energy objective?

This is theorem-first.  A green result preserves a corridor only.

It does NOT establish:
- an exact finite-payload BVP;
- an exact finite source;
- a microscopic source-state energy;
- support or reaction energy;
- complete energy;
- quantum/RG/UV control;
- empirical certification of the complete theory;
- a practical antigravity device.

PHYSICAL FAMILY
---------------
Set

    a4 = a5 = a6 = d2 = 0.

Using Marzo Eq. (3.14) and Eq. (3.17), the pole simplifies identically to

    m_1minus^2 = d1^2 / c7.

The published branch-II health condition is

    a0 < 0,
    c7 > 0,
    A < 0,

with nonzero d1 and 2*d1+5*d2.

For the selected family,

    A = 11*a0 + 18*d1^2.

Hence the physical graviton normalization

    a0 = -Mbar_Pl^2

is compatible with arbitrarily small nonzero d1.  A one-metre pole therefore
does NOT require c7 ~ M_Pl^2/m^2.

CANONICAL NORMALIZATION
-----------------------
For the d2=0 protected 1- pole reconstructed in A10D,

    v^T K'(m^2) v = 3*c7/2,

while the raw engineered-source pole amplitude is 2*sqrt(6).

Therefore

    source saturated residue = 16/c7

and the canonical pole coupling magnitude is

    4/sqrt(c7).

At c7=1 there is no Planck suppression.

PAYLOAD LOADING
---------------
A10E uses

    g_phys = exp(2*sigma) g,
    sigma = lambda * X_mu X^mu,

where X is the canonically normalized physical 1- vector.

For nonrelativistic matter of energy density rho, the static energy contains

    rho * lambda * X^2.

Thus a homogeneous matter region gives the quadratic loading scout

    m_inside^2 = m^2 + 2*lambda*rho.

This is a necessary finite-payload backreaction effect.

It is NOT yet an exact finite-sphere vector transmission solution.

EMPIRICAL QUADRATIC PORTAL
--------------------------
For

    delta g00 = -2*lambda*sum_i X_i^2

the quadratic matrix is -2 I_3.

For one active polarization:

    q_active^2 = 4
    Tr(M^2) = 12

so the three-polarization projector penalty is

    R_P = 3.

We reuse the existing V26B1R1 inverse-cube bound with this penalty.

CAPACITY COMPARATOR
-------------------
To ask whether payload-loading control alone forces >10 MJ, use the existing
canonical spherical Yukawa exterior capacity formula.

This is deliberately classified as an optimistic scalar-Yukawa capacity
comparator, NOT a physical vector finite-source certificate.

A partial capacity below 10 MJ may preserve a corridor but can never promote
a model.
"""

from __future__ import annotations

import math
from functools import lru_cache
from typing import Any

import sympy as sp

from .hook17_marzo2022_quadratic_universal_metric import (
    static_external_g00_gate,
)
from .hook_quadratic_quantum_force import (
    active_coupling_limit_from_beta3,
    spherical_capacity_energy_j,
)


C_LIGHT_M_S = 299792458.0
G_NEWTON_SI = 6.67430e-11
HBAR_J_S = 1.054571817e-34
EV_J = 1.602176634e-19
HBAR_C_EV_M = 1.973269804e-7

STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7

PAYLOAD_MASS_KG = 1.0
PAYLOAD_RADIUS_M = 0.10

DEVICE_RANGE_M = 1.0
STANDOFF_M = 1.0

SELECTED_C7 = 1.0

# A 2 m source radius gives characteristic q/|f| = 0.5 for the one-metre
# Stueckelberg scale.  This remains only a source-gradient control scout.
SOURCE_RADIUS_M = 2.0

# Selected moderate-loading witness.  Vacuum itself has m*R_payload = 0.1.
SELECTED_M_INSIDE_R = 0.20

PROJECTOR_PENALTY = 3.0


def reduced_planck_energy_ev() -> float:
    """Return reduced Planck energy from SI constants."""

    energy_j = math.sqrt(
        HBAR_J_S
        *
        C_LIGHT_M_S**5
        /
        (
            8.0
            *
            math.pi
            *
            G_NEWTON_SI
        )
    )

    return (
        energy_j
        /
        EV_J
    )


def one_metre_mass_ev(
    range_m: float = DEVICE_RANGE_M,
) -> float:
    """Return hbar*c/range in eV."""

    value = float(
        range_m
    )

    if value <= 0.0:
        raise ValueError(
            "range_m must be positive"
        )

    return (
        HBAR_C_EV_M
        /
        value
    )


@lru_cache(maxsize=1)
def symbolic_marzo_scale_identity() -> dict[str, Any]:
    """Prove m^2=d1^2/c7 in the selected protected subfamily."""

    a0, a4, d1, c7 = sp.symbols(
        "a0 a4 d1 c7",
        nonzero=True,
        real=True,
    )

    r1 = (
        -8 * a0
        +
        40 * a4
        -
        4 * d1**2
    )

    r2 = (
        32 * a0
        +
        40 * a4
        +
        16 * d1**2
    )

    r3 = (
        -28 * a0
        +
        40 * a4
        +
        36 * d1**2
    )

    numerator = (
        (2 * d1) ** 2
        *
        (
            50
            *
            (2 * d1)
            *
            d1
            +
            2 * r1
            +
            r2
            -
            r3
        )
    )

    denominator = (
        4
        *
        c7
        *
        (
            50
            *
            d1
            *
            (2 * d1)
            +
            2 * r1
            +
            r2
            -
            r3
        )
    )

    mass_squared = sp.factor(
        numerator
        /
        denominator
    )

    combination = sp.factor(
        2 * r1
        +
        r2
        -
        r3
    )

    identity_pass = bool(
        sp.simplify(
            mass_squared
            -
            d1**2
            /
            c7
        )
        ==
        0
    )

    return {
        "mass_squared_exact":
            str(
                mass_squared
            ),

        "two_r1_plus_r2_minus_r3":
            str(
                combination
            ),

        "mass_identity_pass":
            identity_pass,

        "independent_of_a0":
            bool(
                a0
                not in
                mass_squared.free_symbols
            ),

        "independent_of_a4":
            bool(
                a4
                not in
                mass_squared.free_symbols
            ),
    }


def physical_planck_normalized_family(
    *,
    range_m: float = DEVICE_RANGE_M,
    c7: float = SELECTED_C7,
) -> dict[str, Any]:
    """Return a physically normalized one-metre protected-family witness."""

    c7_value = float(
        c7
    )

    if c7_value <= 0.0:
        raise ValueError(
            "c7 must be positive"
        )

    planck_ev = (
        reduced_planck_energy_ev()
    )

    mass_ev = one_metre_mass_ev(
        range_m
    )

    # m^2 = d1^2/c7.
    d1_ev = (
        mass_ev
        *
        math.sqrt(
            c7_value
        )
    )

    a0_ev2 = (
        -planck_ev**2
    )

    a4_ev2 = 0.0
    a5_ev2 = 0.0
    a6_ev2 = 0.0
    d2_ev = 0.0

    health_a_ev2 = (
        11.0
        *
        a0_ev2
        +
        18.0
        *
        d1_ev**2
    )

    health_b_ev2 = (
        22.0
        *
        a0_ev2
        +
        36.0
        *
        d1_ev**2
    )

    reconstructed_mass_squared_ev2 = (
        d1_ev**2
        /
        c7_value
    )

    reconstructed_range_m = (
        HBAR_C_EV_M
        /
        math.sqrt(
            reconstructed_mass_squared_ev2
        )
    )

    stueckelberg_f_ev = (
        -d1_ev
    )

    pole_derivative_norm = (
        1.5
        *
        c7_value
    )

    raw_source_pole_amplitude = (
        2.0
        *
        math.sqrt(
            6.0
        )
    )

    source_saturated_residue = (
        raw_source_pole_amplitude**2
        /
        pole_derivative_norm
    )

    canonical_source_coupling = math.sqrt(
        source_saturated_residue
    )

    branch_ii_pass = bool(
        a0_ev2 < 0.0
        and
        c7_value > 0.0
        and
        health_a_ev2 < 0.0
        and
        d1_ev != 0.0
        and
        (
            2.0
            *
            d1_ev
            +
            5.0
            *
            d2_ev
        )
        !=
        0.0
    )

    return {
        "reduced_planck_energy_ev":
            planck_ev,

        "a0_ev2":
            a0_ev2,

        "a4_ev2":
            a4_ev2,

        "a5_ev2":
            a5_ev2,

        "a6_ev2":
            a6_ev2,

        "c7":
            c7_value,

        "d1_ev":
            d1_ev,

        "d2_ev":
            d2_ev,

        "stueckelberg_f_ev":
            stueckelberg_f_ev,

        "d1_over_reduced_planck":
            (
                d1_ev
                /
                planck_ev
            ),

        "health_A_over_planck_squared":
            (
                health_a_ev2
                /
                planck_ev**2
            ),

        "health_B_over_planck_squared":
            (
                health_b_ev2
                /
                planck_ev**2
            ),

        "published_health_branch_II_pass":
            branch_ii_pass,

        "target_range_m":
            float(
                range_m
            ),

        "reconstructed_range_m":
            reconstructed_range_m,

        "range_reproduced":
            bool(
                math.isclose(
                    reconstructed_range_m,
                    float(
                        range_m
                    ),
                    rel_tol=1.0e-14,
                    abs_tol=0.0,
                )
            ),

        "planck_normalization_requires_huge_c7":
            False,

        "pole_derivative_norm":
            pole_derivative_norm,

        "source_saturated_residue":
            source_saturated_residue,

        "canonical_source_coupling_magnitude":
            canonical_source_coupling,

        "canonical_source_coupling_planck_suppressed":
            bool(
                canonical_source_coupling
                <
                1.0e-10
            ),

        "ultralight_mass_quantitative_rg_naturalness_certified":
            False,
    }


def payload_energy_density_ev4(
    *,
    payload_mass_kg: float = PAYLOAD_MASS_KG,
    payload_radius_m: float = PAYLOAD_RADIUS_M,
) -> dict[str, float]:
    """Return uniform payload rest-energy density in eV^4."""

    mass_kg = float(
        payload_mass_kg
    )

    radius_m = float(
        payload_radius_m
    )

    if (
        mass_kg <= 0.0
        or
        radius_m <= 0.0
    ):
        raise ValueError(
            "payload parameters must be positive"
        )

    volume_m3 = (
        4.0
        /
        3.0
        *
        math.pi
        *
        radius_m**3
    )

    density_j_m3 = (
        mass_kg
        *
        C_LIGHT_M_S**2
        /
        volume_m3
    )

    one_ev4_j_m3 = (
        EV_J
        /
        HBAR_C_EV_M**3
    )

    density_ev4 = (
        density_j_m3
        /
        one_ev4_j_m3
    )

    return {
        "volume_m3":
            volume_m3,

        "rest_energy_density_j_m3":
            density_j_m3,

        "one_ev4_j_m3":
            one_ev4_j_m3,

        "rest_energy_density_ev4":
            density_ev4,
    }


@lru_cache(maxsize=1)
def empirical_quadratic_metric_gate() -> dict[str, Any]:
    """Return the existing inverse-cube limit for the canonical vector portal."""

    coupling = (
        active_coupling_limit_from_beta3(
            projector_penalty=
                PROJECTOR_PENALTY,
        )
    )

    active_coupling_max = float(
        coupling[
            "active_coupling_max_ev_m2"
        ]
    )

    # delta g00 = -2 lambda X^2.
    lambda_max = (
        active_coupling_max
        /
        2.0
    )

    return {
        "quadratic_metric_matrix":
            "M=-2*I_3",

        "active_background_coefficient_abs":
            2.0,

        "trace_M_squared":
            12.0,

        "projector_penalty":
            PROJECTOR_PENALTY,

        "active_coupling_max_ev_m2":
            active_coupling_max,

        "lambda_empirical_max_ev_m2":
            lambda_max,

        "range_one_m_effectively_massless_at_one_mm":
            True,
    }


def payload_loading_metrics(
    *,
    lambda_ev_m2: float,
    payload_mass_kg: float = PAYLOAD_MASS_KG,
    payload_radius_m: float = PAYLOAD_RADIUS_M,
    range_m: float = DEVICE_RANGE_M,
) -> dict[str, float]:
    """Return homogeneous quadratic matter-loading diagnostics."""

    coupling = float(
        lambda_ev_m2
    )

    if coupling < 0.0:
        raise ValueError(
            "lambda_ev_m2 must be nonnegative"
        )

    density = payload_energy_density_ev4(
        payload_mass_kg=
            payload_mass_kg,

        payload_radius_m=
            payload_radius_m,
    )

    rho = density[
        "rest_energy_density_ev4"
    ]

    mass_ev = one_metre_mass_ev(
        range_m
    )

    radius_ev_inverse = (
        payload_radius_m
        /
        HBAR_C_EV_M
    )

    inside_mass_squared = (
        mass_ev**2
        +
        2.0
        *
        coupling
        *
        rho
    )

    inside_mass = math.sqrt(
        inside_mass_squared
    )

    dimensionless_load = (
        inside_mass
        *
        radius_ev_inverse
    )

    vacuum_dimensionless = (
        mass_ev
        *
        radius_ev_inverse
    )

    return {
        "lambda_ev_m2":
            coupling,

        "vacuum_mass_ev":
            mass_ev,

        "inside_mass_ev":
            inside_mass,

        "vacuum_mR":
            vacuum_dimensionless,

        "inside_mR":
            dimensionless_load,

        "matter_added_mass_squared_ev2":
            (
                2.0
                *
                coupling
                *
                rho
            ),

        "penetration_length_m":
            (
                HBAR_C_EV_M
                /
                inside_mass
            ),
    }


def lambda_for_loading_target(
    *,
    target_inside_mR: float,
    payload_mass_kg: float = PAYLOAD_MASS_KG,
    payload_radius_m: float = PAYLOAD_RADIUS_M,
    range_m: float = DEVICE_RANGE_M,
) -> float:
    """Return lambda giving a requested homogeneous inside mR."""

    target = float(
        target_inside_mR
    )

    density = payload_energy_density_ev4(
        payload_mass_kg=
            payload_mass_kg,

        payload_radius_m=
            payload_radius_m,
    )

    rho = density[
        "rest_energy_density_ev4"
    ]

    mass_ev = one_metre_mass_ev(
        range_m
    )

    radius_ev_inverse = (
        payload_radius_m
        /
        HBAR_C_EV_M
    )

    vacuum_mR = (
        mass_ev
        *
        radius_ev_inverse
    )

    if target <= vacuum_mR:
        raise ValueError(
            "target_inside_mR must exceed vacuum mR"
        )

    target_mass_ev = (
        target
        /
        radius_ev_inverse
    )

    coupling = (
        (
            target_mass_ev**2
            -
            mass_ev**2
        )
        /
        (
            2.0
            *
            rho
        )
    )

    return coupling


def required_canonical_field_at_payload(
    *,
    lambda_ev_m2: float,
) -> float:
    """Return canonical X amplitude using the A10E 1-g sigma."""

    coupling = float(
        lambda_ev_m2
    )

    if coupling <= 0.0:
        raise ValueError(
            "lambda_ev_m2 must be positive"
        )

    sigma = float(
        static_external_g00_gate()[
            "sigma_at_payload"
        ]
    )

    return math.sqrt(
        sigma
        /
        coupling
    )


def scalar_yukawa_capacity_comparator(
    *,
    lambda_ev_m2: float,
    source_radius_m: float = SOURCE_RADIUS_M,
    stand_off_m: float = STANDOFF_M,
    range_m: float = DEVICE_RANGE_M,
) -> dict[str, float]:
    """Return optimistic scalar-Yukawa exterior capacity comparator.

    For a spherical Yukawa profile

        X(r) = X(R) * R/r * exp[-(r-R)/ell],

    a payload-side field amplitude at r=R+h requires

        X(R) = X(R+h) * (R+h)/R * exp(h/ell).

    The resulting exterior capacity uses the already tested repository
    spherical canonical-field formula.

    This is NOT a physical transverse-vector source certificate.
    """

    source_radius = float(
        source_radius_m
    )

    stand_off = float(
        stand_off_m
    )

    range_value = float(
        range_m
    )

    payload_amplitude = (
        required_canonical_field_at_payload(
            lambda_ev_m2=
                lambda_ev_m2
        )
    )

    radial_ratio = (
        (
            source_radius
            +
            stand_off
        )
        /
        source_radius
    )

    source_surface_amplitude = (
        payload_amplitude
        *
        radial_ratio
        *
        math.exp(
            stand_off
            /
            range_value
        )
    )

    capacity = (
        spherical_capacity_energy_j(
            background_amplitude_ev=
                source_surface_amplitude,

            radius_m=
                source_radius,

            range_m=
                range_value,
        )
    )

    return {
        "payload_canonical_amplitude_ev":
            payload_amplitude,

        "source_surface_canonical_amplitude_ev":
            source_surface_amplitude,

        "source_radius_m":
            source_radius,

        "stand_off_m":
            stand_off,

        "range_m":
            range_value,

        "scalar_yukawa_capacity_energy_j":
            float(
                capacity[
                    "energy_j"
                ]
            ),

        "this_is_complete_energy":
            False,

        "this_is_exact_vector_source_capacity":
            False,
    }


def source_stueckelberg_gradient_control(
    *,
    source_radius_m: float = SOURCE_RADIUS_M,
    range_m: float = DEVICE_RANGE_M,
    c7: float = SELECTED_C7,
) -> dict[str, float | bool]:
    """Return characteristic q/|f| for source localization."""

    family = (
        physical_planck_normalized_family(
            range_m=
                range_m,

            c7=
                c7,
        )
    )

    q_ev = (
        HBAR_C_EV_M
        /
        source_radius_m
    )

    f_ev = abs(
        float(
            family[
                "stueckelberg_f_ev"
            ]
        )
    )

    ratio = (
        q_ev
        /
        f_ev
    )

    return {
        "source_radius_m":
            float(
                source_radius_m
            ),

        "characteristic_q_ev":
            q_ev,

        "stueckelberg_f_abs_ev":
            f_ev,

        "q_over_f":
            ratio,

        "q_over_f_at_most_one":
            bool(
                ratio
                <=
                1.0
            ),

        "this_is_full_source_eft_control":
            False,
    }


def loading_capacity_scan() -> list[dict[str, float | bool]]:
    """Return a small theorem-guided payload-loading/capacity scan."""

    empirical = (
        empirical_quadratic_metric_gate()
    )

    empirical_lambda = float(
        empirical[
            "lambda_empirical_max_ev_m2"
        ]
    )

    rows = []

    for target in (
        0.105,
        0.11,
        0.15,
        0.20,
        0.25,
        0.50,
        1.00,
    ):
        coupling = (
            lambda_for_loading_target(
                target_inside_mR=
                    target
            )
        )

        capacity = (
            scalar_yukawa_capacity_comparator(
                lambda_ev_m2=
                    coupling
            )
        )

        rows.append(
            {
                "target_inside_mR":
                    target,

                "lambda_ev_m2":
                    coupling,

                "empirical_lambda_over_selected_lambda":
                    (
                        empirical_lambda
                        /
                        coupling
                    ),

                "payload_canonical_amplitude_ev":
                    capacity[
                        "payload_canonical_amplitude_ev"
                    ],

                "source_surface_canonical_amplitude_ev":
                    capacity[
                        "source_surface_canonical_amplitude_ev"
                    ],

                "scalar_yukawa_capacity_energy_j":
                    capacity[
                        "scalar_yukawa_capacity_energy_j"
                    ],

                "capacity_below_strict_10mj":
                    bool(
                        capacity[
                            "scalar_yukawa_capacity_energy_j"
                        ]
                        <
                        STRICT_COMPLETE_OPERATING_TARGET_J
                    ),
            }
        )

    return rows


def capacity_10mj_loading_threshold() -> dict[str, float]:
    """Find m_inside*R where the comparator crosses exactly 10 MJ."""

    vacuum = payload_loading_metrics(
        lambda_ev_m2=
            0.0
    )[
        "vacuum_mR"
    ]

    low = (
        vacuum
        *
        (
            1.0
            +
            1.0e-8
        )
    )

    high = 1.0

    for _ in range(
        100
    ):
        middle = (
            0.5
            *
            (
                low
                +
                high
            )
        )

        coupling = (
            lambda_for_loading_target(
                target_inside_mR=
                    middle
            )
        )

        energy = (
            scalar_yukawa_capacity_comparator(
                lambda_ev_m2=
                    coupling
            )[
                "scalar_yukawa_capacity_energy_j"
            ]
        )

        if (
            energy
            >
            STRICT_COMPLETE_OPERATING_TARGET_J
        ):
            low = middle

        else:
            high = middle

    threshold = high

    coupling = (
        lambda_for_loading_target(
            target_inside_mR=
                threshold
        )
    )

    energy = (
        scalar_yukawa_capacity_comparator(
            lambda_ev_m2=
                coupling
        )[
            "scalar_yukawa_capacity_energy_j"
        ]
    )

    return {
        "vacuum_mR":
            float(
                vacuum
            ),

        "capacity_10mj_crossing_mR":
            threshold,

        "capacity_10mj_crossing_lambda_ev_m2":
            coupling,

        "capacity_at_crossing_j":
            float(
                energy
            ),
    }


@lru_cache(maxsize=1)
def h17a10f0_summary() -> dict[str, Any]:
    """Return the A10F0 physical-scale/payload-loading decision."""

    symbolic = (
        symbolic_marzo_scale_identity()
    )

    physical = (
        physical_planck_normalized_family()
    )

    empirical = (
        empirical_quadratic_metric_gate()
    )

    empirical_loading = (
        payload_loading_metrics(
            lambda_ev_m2=
                empirical[
                    "lambda_empirical_max_ev_m2"
                ]
        )
    )

    selected_lambda = (
        lambda_for_loading_target(
            target_inside_mR=
                SELECTED_M_INSIDE_R
        )
    )

    selected_loading = (
        payload_loading_metrics(
            lambda_ev_m2=
                selected_lambda
        )
    )

    selected_capacity = (
        scalar_yukawa_capacity_comparator(
            lambda_ev_m2=
                selected_lambda
        )
    )

    source_gradient = (
        source_stueckelberg_gradient_control()
    )

    threshold = (
        capacity_10mj_loading_threshold()
    )

    empirical_lambda = float(
        empirical[
            "lambda_empirical_max_ev_m2"
        ]
    )

    capacity_corridor = bool(
        selected_lambda
        <
        empirical_lambda

        and

        selected_loading[
            "inside_mR"
        ]
        <=
        SELECTED_M_INSIDE_R
        *
        (
            1.0
            +
            1.0e-12
        )

        and

        selected_capacity[
            "scalar_yukawa_capacity_energy_j"
        ]
        <
        STRICT_COMPLETE_OPERATING_TARGET_J
    )

    physical_scale_green = bool(
        symbolic[
            "mass_identity_pass"
        ]
        and
        symbolic[
            "independent_of_a0"
        ]
        and
        physical[
            "published_health_branch_II_pass"
        ]
        and
        physical[
            "range_reproduced"
        ]
        and
        not physical[
            "planck_normalization_requires_huge_c7"
        ]
        and
        not physical[
            "canonical_source_coupling_planck_suppressed"
        ]
    )

    partial_green = bool(
        physical_scale_green
        and
        capacity_corridor
        and
        source_gradient[
            "q_over_f_at_most_one"
        ]
    )

    decision = (
        "GREEN_A10F0_PHYSICAL_NORMALIZATION_PAYLOAD_LOADING_"
        "AND_PARTIAL_CAPACITY_CORRIDOR_OPEN"
        if partial_green
        else
        "RED_A10F0_PHYSICAL_SCALE_OR_PAYLOAD_LOADING_CLOSEOUT"
    )

    return {
        "branch":
            "032H17A10F0",

        "decision":
            decision,

        "current_full_regression_before_a10f0":
            960,

        "physical_scale_identity":
            symbolic,

        "physical_planck_normalized_family":
            physical,

        "empirical_quadratic_metric_gate":
            empirical,

        "payload_loading_at_empirical_portal_limit":
            empirical_loading,

        "selected_loading_target_mR":
            SELECTED_M_INSIDE_R,

        "selected_loading_lambda_ev_m2":
            selected_lambda,

        "selected_payload_loading":
            selected_loading,

        "selected_capacity_comparator":
            selected_capacity,

        "source_stueckelberg_gradient_control":
            source_gradient,

        "loading_capacity_scan":
            loading_capacity_scan(),

        "capacity_10mj_loading_threshold":
            threshold,

        "planck_normalization_kills_one_metre_carrier":
            False
            if physical_scale_green
            else None,

        "huge_c7_required_for_one_metre_range":
            False
            if physical_scale_green
            else None,

        "canonical_source_overlap_planck_suppressed":
            physical[
                "canonical_source_coupling_planck_suppressed"
            ],

        "payload_loading_is_stronger_than_inverse_cube_empirical_limit":
            bool(
                selected_lambda
                <
                empirical_lambda
            ),

        "empirical_portal_limit_is_finite_payload_safe":
            bool(
                empirical_loading[
                    "inside_mR"
                ]
                <=
                1.0
            ),

        "load_controlled_partial_capacity_corridor_open":
            capacity_corridor,

        "selected_partial_capacity_fraction_of_10mj":
            (
                selected_capacity[
                    "scalar_yukawa_capacity_energy_j"
                ]
                /
                STRICT_COMPLETE_OPERATING_TARGET_J
            ),

        "this_capacity_may_reject_but_never_promote":
            True,

        "exact_finite_vector_source_bvp_established":
            False,

        "exact_finite_payload_transmission_established":
            False,

        "finite_source_established":
            False,

        "finite_payload_established":
            False,

        "true_standoff_certified":
            False,

        "source_charge_per_joule_established":
            False,

        "source_support_energy_established":
            False,

        "reaction_energy_established":
            False,

        "full_quantum_rg_uv_certified":
            False,

        "ultralight_mass_quantitative_naturalness_certified":
            False,

        "complete_energy_established":
            False,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "exactly_10mj_passes":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "hook17_closed":
            False,

        "partial_green":
            partial_green,

        "next":
            (
                "032H17A10F1_EXACT_FINITE_TRANSVERSE_VECTOR_SOURCE_"
                "FINITE_PAYLOAD_BVP_SOURCE_ENERGY_EMPIRICAL_UV_"
                "AND_COMPLETE_LEDGER_KILL_GATE"
                if partial_green
                else
                "CLOSE_CURRENT_MARZO_HOOK17_CARRIER"
            ),
    }
