"""032V23 ordinary-stress derivative-hypermomentum multipole gate.

PURPOSE
-------
032U established, under its declared assumptions, that an ordinary symmetric
stress tensor T_munu cannot supply a derivative-free rank-three source.

The leading universal T-only source therefore contains derivatives.

For a compact static ordinary source:

    monopole = 0

but a first moment / dipole survives.

V23 asks whether this surviving derivative multipole can nevertheless become a
practical universal finite-payload antigravity route.

The result is deliberately generous to the candidate.

We grant:

- a healthy positive quadratic propagating longitudinal mode;
- the favorable repulsive Yukawa sign;
- reciprocity between source and payload;
- universal ordinary-mass coupling;
- a point source placed at the most favorable admissible position;
- no source-support, activation, control or field-energy surcharge.

If even that fails by enormous response-per-joule and empirical margins, the
ordinary-stress-only derivative route is not worth a blind parameter scan.

DERIVATIVE-SOURCE MOMENT IDENTITY
---------------------------------
For a simple one-derivative source

    S_i = partial_i rho,

compact support gives

    integral S_i d^3x = 0.

Its first moment is

    integral x_j S_i d^3x
        =
        - delta_ij integral rho d^3x.

Thus the surviving first moment is fixed by total source energy/mass.

There is no independent charge-per-joule enhancement in this minimal
ordinary-T derivative source.

GENEROUS LONGITUDINAL ORACLE
----------------------------
Use a canonical positive static mode Q_i with schematic interaction

    L_int
        =
        g Q_i partial_i rho,

    g
        =
        1/Lambda^2.

Integrating out Q gives a cross interaction

    E_12
        =
        - g^2
        integral
        partial_i rho_1
        G_m
        partial_i rho_2.

For separated compact sources,

    E_12
        =
        + g^2 m^2 M_1 M_2 G_m(r),

because

    nabla^2 G_m
        =
        m^2 G_m

outside the contact source.

Therefore the long-range Yukawa piece is REPULSIVE for equal-sign ordinary
sources.

The massless limit of this particular longitudinal derivative channel has no
separated long-range force because the exterior Laplacian vanishes.

Define the phenomenological repulsive Yukawa potential

    V_Y
        =
        + alpha
        G M1 M2
        exp(-r/lambda)
        / r.

The acceleration magnitude is

    a_Y
        =
        alpha
        G M
        (1+r/lambda)
        exp(-r/lambda)
        / r^2.

FINITE PAYLOAD
--------------
The project payload is a sphere:

    payload radius = 0.10 m.

For this optimistic portal gate:

    source point     = z=0
    payload center   = z=0.20 m.

The entire payload is source-free.

The local +z acceleration is reconstructed over the full payload surface.

For the repulsive central Yukawa field the adverse point is the far payload
pole near z=0.30 m, not the near 0.10-m point.

This is more conservative scientifically than using only the nearest-point
force.

GOODKIND SHAPE-ONLY SCOUT
-------------------------
Goodkind et al., Phys. Rev. D 47, 1290 (1993), publicly report:

    inverse-square law verified to +/-1 percent
    over 0.4 to 1.4 m,

and report 95-percent Yukawa constraints for ranges

    0.2 to 2.0 m.

V23 does NOT digitize their published alpha likelihood.

Instead, it constructs an intentionally loose shape-only scout.

Allow arbitrary normalization of Newton's G and permit the full endpoint
ratio

    R_max
        =
        1.01/0.99.

For

    F r^2
        proportional to
        1 + alpha f(r),

where

    f(r)
        =
        (1+r/lambda)
        exp(-r/lambda),

require only

    [1+alpha f(0.4)]
    /
    [1+alpha f(1.4)]
        <=
        1.01/0.99.

This gives a deliberately loose derived alpha ceiling.

It is:

    NOT_THE_PUBLISHED_ALPHA_LIMIT
    NOT_A_RECONSTRUCTION_OF_THE_95PCT_LIKELIHOOD.

It is only a cheap empirical rejection scout based on the public +/-1-percent
shape statement.

SCALARIZED PORTAL NORMALIZATION
-------------------------------
For the generous scalarized longitudinal oracle,

    alpha
        =
        2 Mpl_bar^2 m^2 / Lambda^4,

where Mpl_bar is the reduced Planck mass.

This normalization is used only to illustrate the enormous target-vs-
empirical portal-scale mismatch.

It is not claimed as the unique tensor normalization of metric-affine gravity.

CLAIM LIMITS
------------
A red result closes only the practical route:

    ORDINARY SYMMETRIC T
    +
    ONE-DERIVATIVE UNIVERSAL SOURCE
    +
    RECIPROCAL UNIVERSAL MASS RESPONSE
    +
    YUKAWA-LIKE HEALTHY LONGITUDINAL MODE

under the finite-payload and strict-10-MJ objective.

It does NOT close:

- all tensor projector structures;
- intrinsic microscopic hypermomentum;
- Dirac hypermomentum;
- extra matter charges;
- nonlinear/environmental screening;
- full metric-affine gravity.

It also does not yet establish a physical-metric bridge.

A universal fifth-force oracle is being granted only as an optimistic upper
bound.

No negative mass is used.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from scipy.integrate import quad

from .storage import Storage


G_NEWTON = 6.67430e-11
C_LIGHT = 299792458.0

HBARC_EV_M = 1.973269804e-7
MPL_REDUCED_EV = 2.435e27


def source_mass_equivalent_kg(
    source_energy_j: float,
) -> float:
    """Return E/c^2."""

    energy = float(
        source_energy_j
    )

    if energy <= 0.0:
        raise ValueError(
            "source energy must be positive"
        )

    return (
        energy
        / C_LIGHT**2
    )


def derivative_gaussian_moments(
    *,
    source_energy_j: float,
    sigma_m: float = 0.05,
    half_width_sigma: float = 12.0,
) -> dict[str, float | bool]:
    """Numerically reconstruct zero monopole and fixed first moment.

    A normalized one-dimensional Gaussian is sufficient to test the exact
    integration-by-parts identity.

    The transverse directions integrate to unity.
    """

    mass = (
        source_mass_equivalent_kg(
            source_energy_j
        )
    )

    sigma = float(
        sigma_m
    )

    half_width = (
        float(
            half_width_sigma
        )
        * sigma
    )

    if (
        sigma <= 0.0
        or half_width <= 0.0
    ):
        raise ValueError(
            "positive Gaussian scales required"
        )

    def gaussian(
        x: float,
    ) -> float:
        return (
            math.exp(
                -(
                    x
                    / sigma
                )**2
            )
            /
            (
                math.sqrt(
                    math.pi
                )
                * sigma
            )
        )

    def derivative(
        x: float,
    ) -> float:
        return (
            -2.0
            * x
            / sigma**2
            * gaussian(
                x
            )
        )

    monopole_norm, _ = quad(
        derivative,
        -half_width,
        half_width,
        epsabs=
            1.0e-13,
        epsrel=
            1.0e-13,
        limit=
            400,
    )

    first_moment_norm, _ = quad(
        lambda x:
            x
            * derivative(
                x
            ),
        -half_width,
        half_width,
        epsabs=
            1.0e-13,
        epsrel=
            1.0e-13,
        limit=
            400,
    )

    monopole_kg = (
        mass
        * monopole_norm
    )

    first_moment_kg = (
        mass
        * first_moment_norm
    )

    expected_first_moment_kg = (
        -mass
    )

    relative_error = (
        abs(
            first_moment_kg
            -
            expected_first_moment_kg
        )
        / mass
    )

    return {
        "source_mass_equivalent_kg":
            mass,

        "derivative_monopole_kg":
            monopole_kg,

        "monopole_relative_to_source_mass":
            abs(
                monopole_kg
            )
            / mass,

        "derivative_first_moment_kg":
            first_moment_kg,

        "expected_first_moment_kg":
            expected_first_moment_kg,

        "first_moment_relative_error":
            relative_error,

        "charge_per_joule_free_parameter":
            False,

        "zero_monopole":
            (
                abs(
                    monopole_norm
                )
                <
                1.0e-10
            ),

        "fixed_first_moment":
            (
                relative_error
                <
                1.0e-10
            ),
    }


def longitudinal_derivative_oracle() -> dict[str, bool | str]:
    """Return the deliberately favorable canonical longitudinal oracle."""

    return {
        "positive_quadratic_hamiltonian_assumed":
            True,

        "derivative_source_monopole":
            False,

        "derivative_source_dipole":
            True,

        "separated_massive_cross_potential_sign":
            "REPULSIVE",

        "massive_yukawa_long_range_piece":
            True,

        "massless_separated_long_range_piece":
            False,

        "universal_source_detector_portal_assumed":
            True,

        "universal_physical_metric_bridge_established":
            False,

        "full_metric_affine_action_established":
            False,

        "claim_class":
            "GENEROUS_RESPONSE_ORACLE",
    }


def yukawa_force_shape(
    *,
    distance_m: float,
    range_m: float,
) -> float:
    """Return (1+r/lambda) exp(-r/lambda)."""

    distance = float(
        distance_m
    )

    range_value = float(
        range_m
    )

    if (
        distance <= 0.0
        or range_value <= 0.0
    ):
        raise ValueError(
            "positive distance and range required"
        )

    x = (
        distance
        / range_value
    )

    return (
        (
            1.0
            +
            x
        )
        * math.exp(
            -x
        )
    )


def finite_payload_surface_metrics(
    *,
    alpha: float,
    source_energy_j: float,
    payload_center_z_m: float,
    payload_radius_m: float,
    range_m: float,
    surface_count: int = 4001,
) -> dict[str, float | bool]:
    """Return full-surface +z acceleration for an optimistic point source."""

    alpha_value = float(
        alpha
    )

    center = float(
        payload_center_z_m
    )

    radius = float(
        payload_radius_m
    )

    range_value = float(
        range_m
    )

    count = int(
        surface_count
    )

    if (
        alpha_value < 0.0
        or center <= radius
        or radius <= 0.0
        or range_value <= 0.0
        or count < 3
    ):
        raise ValueError(
            "invalid finite-payload state"
        )

    source_mass = (
        source_mass_equivalent_kg(
            source_energy_j
        )
    )

    mu = np.linspace(
        -1.0,
        1.0,
        count,
    )

    z = (
        center
        +
        radius
        * mu
    )

    rho = (
        radius
        * np.sqrt(
            np.maximum(
                0.0,
                1.0
                -
                mu**2,
            )
        )
    )

    r = np.sqrt(
        z**2
        +
        rho**2
    )

    x = (
        r
        / range_value
    )

    force_shape = (
        (
            1.0
            +
            x
        )
        * np.exp(
            -x
        )
    )

    axial_kernel_m2 = (
        z
        / r**3
        * force_shape
    )

    acceleration = (
        alpha_value
        * G_NEWTON
        * source_mass
        * axial_kernel_m2
    )

    index_min = int(
        np.argmin(
            acceleration
        )
    )

    index_max = int(
        np.argmax(
            acceleration
        )
    )

    return {
        "surface_min_m_s2":
            float(
                acceleration[
                    index_min
                ]
            ),

        "surface_max_m_s2":
            float(
                acceleration[
                    index_max
                ]
            ),

        "surface_min_mu":
            float(
                mu[
                    index_min
                ]
            ),

        "surface_max_mu":
            float(
                mu[
                    index_max
                ]
            ),

        "surface_min_source_distance_m":
            float(
                r[
                    index_min
                ]
            ),

        "surface_max_source_distance_m":
            float(
                r[
                    index_max
                ]
            ),

        "minimum_axial_kernel_m2":
            float(
                np.min(
                    axial_kernel_m2
                )
            ),

        "maximum_axial_kernel_m2":
            float(
                np.max(
                    axial_kernel_m2
                )
            ),

        "all_surface_points_outward":
            bool(
                np.all(
                    acceleration
                    >=
                    0.0
                )
            ),

        "point_source_is_complete_source_model":
            False,

        "source_support_energy_included":
            False,
    }


def required_alpha_for_finite_payload(
    *,
    target_acceleration_m_s2: float,
    source_energy_j: float,
    payload_center_z_m: float,
    payload_radius_m: float,
    range_m: float,
    surface_count: int = 4001,
) -> dict[str, float | bool]:
    """Return alpha required to make the adverse surface reach target."""

    target = float(
        target_acceleration_m_s2
    )

    if target <= 0.0:
        raise ValueError(
            "positive target acceleration required"
        )

    unit = (
        finite_payload_surface_metrics(
            alpha=
                1.0,

            source_energy_j=
                source_energy_j,

            payload_center_z_m=
                payload_center_z_m,

            payload_radius_m=
                payload_radius_m,

            range_m=
                range_m,

            surface_count=
                surface_count,
        )
    )

    unit_min = float(
        unit[
            "surface_min_m_s2"
        ]
    )

    if unit_min <= 0.0:
        raise RuntimeError(
            "unit-alpha surface response is not outward"
        )

    alpha_required = (
        target
        / unit_min
    )

    nearest_gap = (
        payload_center_z_m
        -
        payload_radius_m
    )

    nearest_shape = (
        yukawa_force_shape(
            distance_m=
                nearest_gap,

            range_m=
                range_m,
        )
    )

    source_mass = (
        source_mass_equivalent_kg(
            source_energy_j
        )
    )

    nearest_point_alpha = (
        target
        * nearest_gap**2
        /
        (
            G_NEWTON
            * source_mass
            * nearest_shape
        )
    )

    return {
        "alpha_required":
            alpha_required,

        "nearest_point_optimistic_alpha":
            nearest_point_alpha,

        "finite_payload_penalty_over_nearest_point":
            alpha_required
            / nearest_point_alpha,

        "surface_min_mu_at_unit_alpha":
            float(
                unit[
                    "surface_min_mu"
                ]
            ),

        "surface_min_source_distance_m":
            float(
                unit[
                    "surface_min_source_distance_m"
                ]
            ),

        "all_surface_points_outward":
            bool(
                unit[
                    "all_surface_points_outward"
                ]
            ),

        "finite_payload_surface_criterion":
            True,
    }


def goodkind_shape_only_alpha_scout(
    *,
    range_m: float,
    near_probe_m: float = 0.4,
    far_probe_m: float = 1.4,
    fractional_precision: float = 0.01,
) -> dict[str, float | bool]:
    """Return a deliberately loose alpha scout from the public +/-1% result.

    We allow arbitrary overall normalization and use only endpoint shape.

    If each endpoint may differ by +/-p, the largest allowed endpoint ratio is

        (1+p)/(1-p).

    This is not the published 95-percent alpha likelihood.
    """

    range_value = float(
        range_m
    )

    near = float(
        near_probe_m
    )

    far = float(
        far_probe_m
    )

    precision = float(
        fractional_precision
    )

    if (
        range_value <= 0.0
        or near <= 0.0
        or far <= near
        or not (
            0.0
            <
            precision
            <
            1.0
        )
    ):
        raise ValueError(
            "invalid Goodkind scout parameters"
        )

    f_near = (
        yukawa_force_shape(
            distance_m=
                near,

            range_m=
                range_value,
        )
    )

    f_far = (
        yukawa_force_shape(
            distance_m=
                far,

            range_m=
                range_value,
        )
    )

    ratio_max = (
        (
            1.0
            +
            precision
        )
        /
        (
            1.0
            -
            precision
        )
    )

    numerator = (
        ratio_max
        -
        1.0
    )

    denominator = (
        f_near
        -
        ratio_max
        * f_far
    )

    if denominator <= 0.0:
        alpha_bound = math.inf
    else:
        alpha_bound = (
            numerator
            / denominator
        )

    return {
        "range_m":
            range_value,

        "near_probe_m":
            near,

        "far_probe_m":
            far,

        "published_force_precision_fraction":
            precision,

        "allowed_endpoint_ratio":
            ratio_max,

        "near_yukawa_force_shape":
            f_near,

        "far_yukawa_force_shape":
            f_far,

        "derived_shape_only_alpha_ceiling":
            alpha_bound,

        "uses_arbitrary_overall_g_normalization":
            True,

        "is_published_95pct_alpha_limit":
            False,

        "is_digitized_experimental_likelihood":
            False,

        "is_deliberately_loose_prefight_scout":
            True,
    }


def source_energy_required_at_alpha(
    *,
    target_acceleration_m_s2: float,
    alpha: float,
    payload_center_z_m: float,
    payload_radius_m: float,
    range_m: float,
    surface_count: int = 4001,
) -> float:
    """Return optimistic source energy required for the adverse payload surface."""

    target = float(
        target_acceleration_m_s2
    )

    alpha_value = float(
        alpha
    )

    if (
        target <= 0.0
        or alpha_value <= 0.0
    ):
        raise ValueError(
            "positive target and alpha required"
        )

    reference_energy = 1.0

    reference = (
        finite_payload_surface_metrics(
            alpha=
                alpha_value,

            source_energy_j=
                reference_energy,

            payload_center_z_m=
                payload_center_z_m,

            payload_radius_m=
                payload_radius_m,

            range_m=
                range_m,

            surface_count=
                surface_count,
        )
    )

    reference_acceleration = float(
        reference[
            "surface_min_m_s2"
        ]
    )

    return (
        target
        / reference_acceleration
    )


def scalarized_portal_scale_ev(
    *,
    alpha: float,
    range_m: float,
) -> dict[str, float]:
    """Return Lambda for alpha=2 Mpl_bar^2 m^2/Lambda^4."""

    alpha_value = float(
        alpha
    )

    range_value = float(
        range_m
    )

    if (
        alpha_value <= 0.0
        or range_value <= 0.0
    ):
        raise ValueError(
            "positive alpha and range required"
        )

    mass_ev = (
        HBARC_EV_M
        / range_value
    )

    portal_scale = (
        2.0
        * MPL_REDUCED_EV**2
        * mass_ev**2
        / alpha_value
    )**0.25

    return {
        "mediator_mass_ev":
            mass_ev,

        "portal_scale_ev":
            portal_scale,

        "normalization":
            "ALPHA_EQ_2_MPLBAR2_M2_OVER_LAMBDA4",

        "full_mag_tensor_normalization":
            False,
    }


def practical_range_gate(
    *,
    source_energy_j: float,
    target_acceleration_m_s2: float,
    payload_center_z_m: float,
    payload_radius_m: float,
    range_m: float,
    surface_count: int = 4001,
) -> dict[str, float | bool]:
    """Return complete cheap-gate diagnostics at one Yukawa range."""

    required = (
        required_alpha_for_finite_payload(
            target_acceleration_m_s2=
                target_acceleration_m_s2,

            source_energy_j=
                source_energy_j,

            payload_center_z_m=
                payload_center_z_m,

            payload_radius_m=
                payload_radius_m,

            range_m=
                range_m,

            surface_count=
                surface_count,
        )
    )

    empirical = (
        goodkind_shape_only_alpha_scout(
            range_m=
                range_m,
        )
    )

    alpha_required = float(
        required[
            "alpha_required"
        ]
    )

    alpha_ceiling = float(
        empirical[
            "derived_shape_only_alpha_ceiling"
        ]
    )

    if not math.isfinite(
        alpha_ceiling
    ):
        raise RuntimeError(
            "declared range produced no shape-only empirical ceiling"
        )

    gap = (
        alpha_required
        / alpha_ceiling
    )

    source_energy_floor = (
        source_energy_required_at_alpha(
            target_acceleration_m_s2=
                target_acceleration_m_s2,

            alpha=
                alpha_ceiling,

            payload_center_z_m=
                payload_center_z_m,

            payload_radius_m=
                payload_radius_m,

            range_m=
                range_m,

            surface_count=
                surface_count,
        )
    )

    allowed_response = (
        finite_payload_surface_metrics(
            alpha=
                alpha_ceiling,

            source_energy_j=
                source_energy_j,

            payload_center_z_m=
                payload_center_z_m,

            payload_radius_m=
                payload_radius_m,

            range_m=
                range_m,

            surface_count=
                surface_count,
        )
    )

    target_scale = (
        scalarized_portal_scale_ev(
            alpha=
                alpha_required,

            range_m=
                range_m,
        )
    )

    empirical_scale = (
        scalarized_portal_scale_ev(
            alpha=
                alpha_ceiling,

            range_m=
                range_m,
        )
    )

    return {
        "range_m":
            float(
                range_m
            ),

        "alpha_required_finite_payload":
            alpha_required,

        "alpha_shape_scout_ceiling":
            alpha_ceiling,

        "required_over_shape_scout":
            gap,

        "source_energy_floor_j_at_shape_scout":
            source_energy_floor,

        "max_surface_acceleration_for_declared_source_j":
            float(
                allowed_response[
                    "surface_min_m_s2"
                ]
            ),

        "target_portal_scale_ev_scalarized":
            float(
                target_scale[
                    "portal_scale_ev"
                ]
            ),

        "empirical_portal_scale_min_ev_scalarized":
            float(
                empirical_scale[
                    "portal_scale_ev"
                ]
            ),

        "portal_scale_ratio_empirical_over_target":
            (
                float(
                    empirical_scale[
                        "portal_scale_ev"
                    ]
                )
                /
                float(
                    target_scale[
                        "portal_scale_ev"
                    ]
                )
            ),

        "finite_payload_penalty_over_nearest_point":
            float(
                required[
                    "finite_payload_penalty_over_nearest_point"
                ]
            ),

        "surface_min_source_distance_m":
            float(
                required[
                    "surface_min_source_distance_m"
                ]
            ),

        "all_surface_points_outward":
            bool(
                required[
                    "all_surface_points_outward"
                ]
            ),

        "strict_lt10mj_possible_under_shape_scout":
            (
                source_energy_floor
                <
                1.0e7
            ),

        "complete_operating_ledger":
            False,
    }


def persist_v23_failure_rule(
    storage: Storage,
    *,
    least_bad_gap: float,
    least_bad_source_energy_floor_j: float,
) -> int:
    """Persist narrow practical closure idempotently."""

    family = (
        "032_ORDINARY_STRESS_DERIVATIVE_MULTIPOLE_RECIPROCAL_YUKAWA"
    )

    family_version = (
        "V23"
    )

    rule_type = (
        "FINITE_PAYLOAD_EMPIRICAL_RESPONSE_PER_JOULE_NO_GO"
    )

    proof_reference = (
        "032V23_DERIVATIVE_HYPERMOMENTUM_MULTIPOLE_PREFLIGHT"
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
                True,

            "policy":
                "STRICT_COMPLETE_OPERATING_LT_10MJ",

            "scope":
                (
                    "ORDINARY_SYMMETRIC_T_ONE_DERIVATIVE_"
                    "UNIVERSAL_RECIPROCAL_YUKAWA_LONGITUDINAL_ROUTE"
                ),

            "closed":
                True,

            "source_charge_per_joule_free_lever":
                False,

            "finite_payload_included":
                True,

            "goodkind_shape_scout_is_exact_published_limit":
                False,

            "least_bad_required_over_empirical_shape_scout":
                float(
                    least_bad_gap
                ),

            "least_bad_source_energy_floor_j":
                float(
                    least_bad_source_energy_floor_j
                ),

            "all_tensor_projector_structures_closed":
                False,

            "intrinsic_hypermomentum_closed":
                False,

            "dirac_hypermomentum_closed":
                False,

            "full_metric_affine_gravity_closed":
                False,

            "universal_metric_bridge_established":
                False,

            "negative_mass_required":
                False,
        },

        proof_reference=
            proof_reference,
    )

    return 1
