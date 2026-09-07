"""032V26A invariant-bridge theorem / preflight gate.

PURPOSE
-------
After V25F closed source-aligned G2+G3 KGB gain obtained from a small
principal-symbol denominator, V26 must search for a genuinely new physical
numerator rather than another normalization, susceptibility, or degeneracy
trick.

This module implements four cheap theorem/preflight tests before any new
expensive field solve:

1. Static first-derivative conformal/disformal metric response.
2. A leading parity-even U(1) field-strength physical-metric portal.
3. Canonically normalized two-mode source/metric cross mixing.
4. A finite-payload Einstein-potential Dirichlet-response norm.

The tests are deliberately scoped. They are designed to reject tempting
shortcuts, not to close DHOST, vector-tensor gravity, or metric-affine gravity
as broad theory classes.

STATIC FIRST-DERIVATIVE METRIC TEST
-----------------------------------
Take a local static scalar background with spatial gradient u_i and a physical
metric perturbation

    delta g_{mu nu}
        =
    c u^2 eta_{mu nu}
        +
    d u_mu u_nu.

For a static background u_0 = 0. Therefore

    delta g_00 = -c u^2,

and the pure disformal term proportional to d contributes no leading g_00
response to nonrelativistic matter at rest. The leading static rest-mass
numerator is therefore conformal in this first-derivative reduction.

This is not a theorem against time-gradient disformal backgrounds, higher
second-derivative DHOST operators, or active-state nonlinear portals.

U(1) FIELD-STRENGTH PORTAL TEST
------------------------------
Normalize the leading parity-even rest-matter interaction to

    L_int = -rho ( e E^2 + b B^2 ).

The retarded two-mediator kernel has the standard electric/magnetic
Casimir-Polder quadratic form

    K_gg(e,b)
        =
    [23(e^2+b^2)-14eb] / (16 pi^3).

The scalar V19 comparison normalization used here is

    K_ss = 15 / (8 pi^3).

At fixed magnetic active response b = 1, unconstrained minimization gives

    e = 7/23,

and K_gg/K_ss = 16/23. Thus a formal cancellation exists.

However the same ordinary medium changes the Maxwell kinetic coefficients to

    Z_E = 1 - 2 rho e,
    Z_B = 1 + 2 rho b.

For positive kinetic terms and propagation no faster than the reference matter
metric,

    Z_E > 0,
    Z_B > 0,
    Z_B <= Z_E.

For rho > 0 and the outward magnetic-sign branch b > 0 this implies

    e <= -b.

The constrained minimum is then e = -b. For normalized b = 1,

    K_gg / K_ss = 2.

Therefore the tempting leading local U(1) field-strength portal does not beat
the V19 scalar quantum-force comparator once this declared causal-medium gate
is imposed.

This result is scoped to the stated local parity-even quadratic portal and the
declared propagation criterion. It does not close all gauge-field portals.

CANONICAL CROSS-MIXING TEST
---------------------------
For two canonically normalized healthy modes with quadratic kinetic matrix

    K = [[1, mu], [mu, 1]],

health requires |mu| < 1. The off-diagonal propagator is

    (K^-1)_12 = -mu / (1-mu^2).

A very large transfer generated only by increasing |mu| therefore requires the
small principal eigenvalue

    lambda_min = 1 - |mu|

to collapse. This is the generic two-mode analogue of the V25F denominator
trap. It does not prohibit a genuinely large independent source numerator.

FINITE-PAYLOAD EINSTEIN RESPONSE NORM
-------------------------------------
For a scalar Newtonian potential Phi over a spherical payload region V, define

    E_D = (1 / 8 pi G) integral_V |grad Phi|^2 dV.

By Cauchy-Schwarz,

    E_D >= V |<grad Phi>|^2 / (8 pi G).

For a sphere of radius R this is

    E_D >= a_cm^2 R^3 / (6 G).

This is a positive Dirichlet response norm, not a gauge-invariant localized GR
energy theorem. It is used only as a preflight against proposals in which a
Planck-normalized Einstein metric itself must carry the complete useful
payload response.

LITERATURE / PROJECT PROVENANCE
-------------------------------
Relevant external theory context includes:

- Zumalacarregui & Garcia-Bellido, arXiv:1308.4685, derivative/disformal
  matter metrics and frame transformations.
- De Felice & Naruko, arXiv:1911.10960, metric transformations built from a
  U(1) field strength.
- Standard retarded electric/magnetic Casimir-Polder kernels provide the
  23/7 electric-magnetic coefficients used in the U(1) oracle.

Project provenance:

- V19R5/R6: tested pure-j0 kinetic-conformal implementation closed by
  off-state material response and exact empirical/energy non-overlap.
- V21/V22: tested time-gradient/localized disformal routes closed.
- V24: intrinsic Dirac hypermomentum preserved; tested protected linear
  vector-to-metric bridges closed.
- V25F: source-aligned G2+G3 KGB denominator-driven gain closed.

CLAIM BOUNDARY
--------------
V26A does NOT establish a new antigravity model, a microscopic field, a
stable field, a complete energy ledger, or a practical device.

It does NOT close all DHOST, all vector portals, or all metric-affine gravity.

Its purpose is to identify which bridge classes should not receive the next
expensive run and to preserve the Riemannian-off-state nonlinear
metric-affine intrinsic-Dirac bridge as a high-priority surviving target.

CLAIM_CLASSIFICATION=
SCOPED_INVARIANT_BRIDGE_THEOREM_AND_PREFLIGHT_GATE
"""

from __future__ import annotations

import math
from typing import Any


GRAVITATIONAL_CONSTANT_M3_KG_S2 = 6.67430e-11
STANDARD_GRAVITY_MPS2 = 9.80665
V17_PAYLOAD_RADIUS_M = 0.10
V17_VOLUME_AVERAGE_ACCEL_MPS2 = 42.530323
STRICT_ENERGY_TARGET_J = 1.0e7

SCALAR_TWO_MEDIATOR_KERNEL = 15.0 / (8.0 * math.pi**3)


def _finite(value: float, name: str) -> float:
    result = float(value)

    if not math.isfinite(result):
        raise ValueError(
            f"{name} must be finite"
        )

    return result


def _positive(value: float, name: str) -> float:
    result = _finite(
        value,
        name,
    )

    if result <= 0.0:
        raise ValueError(
            f"{name} must be positive"
        )

    return result


def static_first_derivative_metric_response(
    *,
    conformal_coefficient: float,
    disformal_coefficient: float,
    gradient_magnitude: float = 1.0,
) -> dict[str, Any]:
    """Return the static rest-payload response of a first-derivative metric.

    The local ansatz is

        delta g_mn = c u^2 eta_mn + d u_m u_n

    with u_0 = 0. Only the structural dependence is tested here.
    """

    c_value = _finite(
        conformal_coefficient,
        "conformal_coefficient",
    )

    d_value = _finite(
        disformal_coefficient,
        "disformal_coefficient",
    )

    gradient = _positive(
        gradient_magnitude,
        "gradient_magnitude",
    )

    u2 = gradient**2

    delta_g00 = (
        -c_value
        *
        u2
    )

    pure_disformal_delta_g00 = 0.0

    delta_g_parallel = (
        c_value
        +
        d_value
    ) * u2

    # For rest matter with T^00 = rho, the leading interaction per unit rho
    # is (1/2) delta g_00 in this local convention.
    rest_interaction_per_density = (
        0.5
        *
        delta_g00
    )

    return {
        "conformal_coefficient":
            c_value,

        "disformal_coefficient":
            d_value,

        "gradient_magnitude":
            gradient,

        "delta_g00":
            delta_g00,

        "delta_g_parallel":
            delta_g_parallel,

        "pure_disformal_delta_g00":
            pure_disformal_delta_g00,

        "rest_interaction_per_density":
            rest_interaction_per_density,

        "pure_static_disformal_has_leading_rest_mass_numerator":
            False,

        "leading_static_rest_mass_response_depends_on_conformal_piece":
            True,

        "time_gradient_disformal_closed_by_this_theorem":
            False,

        "higher_derivative_dhost_closed_by_this_theorem":
            False,
    }


def field_strength_two_mediator_kernel(
    *,
    electric_coefficient: float,
    magnetic_coefficient: float,
) -> dict[str, float]:
    """Return the normalized retarded two-vector kernel coefficient."""

    e_value = _finite(
        electric_coefficient,
        "electric_coefficient",
    )

    b_value = _finite(
        magnetic_coefficient,
        "magnetic_coefficient",
    )

    polynomial = (
        23.0
        *
        (
            e_value**2
            +
            b_value**2
        )
        -
        14.0
        *
        e_value
        *
        b_value
    )

    coefficient = (
        polynomial
        /
        (
            16.0
            *
            math.pi**3
        )
    )

    return {
        "electric_coefficient":
            e_value,

        "magnetic_coefficient":
            b_value,

        "kernel_polynomial":
            polynomial,

        "kernel_coefficient":
            coefficient,

        "scalar_reference_kernel":
            SCALAR_TWO_MEDIATOR_KERNEL,

        "ratio_to_scalar_reference":
            coefficient
            /
            SCALAR_TWO_MEDIATOR_KERNEL,
    }


def field_strength_medium_health(
    *,
    electric_coefficient: float,
    magnetic_coefficient: float,
    density_normalization: float = 1.0,
) -> dict[str, Any]:
    """Return local Maxwell kinetic and causal-medium diagnostics."""

    e_value = _finite(
        electric_coefficient,
        "electric_coefficient",
    )

    b_value = _finite(
        magnetic_coefficient,
        "magnetic_coefficient",
    )

    rho_value = _positive(
        density_normalization,
        "density_normalization",
    )

    z_electric = (
        1.0
        -
        2.0
        *
        rho_value
        *
        e_value
    )

    z_magnetic = (
        1.0
        +
        2.0
        *
        rho_value
        *
        b_value
    )

    positive_kinetic = bool(
        z_electric > 0.0
        and
        z_magnetic > 0.0
    )

    speed_squared = None
    causal_relative_to_reference_metric = False

    if positive_kinetic:
        speed_squared = (
            z_magnetic
            /
            z_electric
        )

        causal_relative_to_reference_metric = bool(
            speed_squared <= 1.0
        )

    return {
        "electric_coefficient":
            e_value,

        "magnetic_coefficient":
            b_value,

        "density_normalization":
            rho_value,

        "z_electric":
            z_electric,

        "z_magnetic":
            z_magnetic,

        "positive_kinetic":
            positive_kinetic,

        "speed_squared":
            speed_squared,

        "causal_relative_to_reference_metric":
            causal_relative_to_reference_metric,

        "healthy_declared_medium":
            bool(
                positive_kinetic
                and
                causal_relative_to_reference_metric
            ),
    }


def normalized_field_strength_portal_bound() -> dict[str, Any]:
    """Return the fixed-active-response b=1 U(1) portal theorem data."""

    b_value = 1.0

    unconstrained_e = (
        7.0
        /
        23.0
    )

    unconstrained = (
        field_strength_two_mediator_kernel(
            electric_coefficient=
                unconstrained_e,

            magnetic_coefficient=
                b_value,
        )
    )

    healthy_boundary_e = (
        -b_value
    )

    healthy = (
        field_strength_two_mediator_kernel(
            electric_coefficient=
                healthy_boundary_e,

            magnetic_coefficient=
                b_value,
        )
    )

    # For rho>0 and b>0 the declared causal-medium condition is e <= -b.
    # The kernel is convex and its unconstrained minimum is at positive e,
    # so its constrained minimum lies exactly at the boundary e=-b.
    return {
        "normalized_magnetic_active_coefficient":
            b_value,

        "unconstrained_optimal_electric_coefficient":
            unconstrained_e,

        "unconstrained_ratio_to_scalar_reference":
            unconstrained[
                "ratio_to_scalar_reference"
            ],

        "unconstrained_exact_ratio":
            16.0
            /
            23.0,

        "declared_causal_medium_constraint":
            "e <= -b for rho>0 and b>0",

        "healthy_optimal_electric_coefficient":
            healthy_boundary_e,

        "healthy_minimum_ratio_to_scalar_reference":
            healthy[
                "ratio_to_scalar_reference"
            ],

        "healthy_exact_ratio":
            2.0,

        "formal_quantum_force_reduction_exists_without_medium_health":
            True,

        "healthy_leading_portal_beats_scalar_reference":
            False,

        "all_u1_portals_closed":
            False,
    }


def two_mode_cross_mixing(
    mu: float,
) -> dict[str, Any]:
    """Return exact canonical two-mode mixing health and cross response."""

    value = _finite(
        mu,
        "mu",
    )

    abs_mu = abs(
        value
    )

    minimum_eigenvalue = (
        1.0
        -
        abs_mu
    )

    maximum_eigenvalue = (
        1.0
        +
        abs_mu
    )

    healthy = bool(
        abs_mu < 1.0
    )

    determinant = (
        1.0
        -
        value**2
    )

    inverse_cross = None
    cross_response_magnitude = None

    if determinant != 0.0:
        inverse_cross = (
            -value
            /
            determinant
        )

        cross_response_magnitude = abs(
            inverse_cross
        )

    return {
        "mu":
            value,

        "abs_mu":
            abs_mu,

        "minimum_eigenvalue":
            minimum_eigenvalue,

        "maximum_eigenvalue":
            maximum_eigenvalue,

        "determinant":
            determinant,

        "healthy":
            healthy,

        "inverse_cross":
            inverse_cross,

        "cross_response_magnitude":
            cross_response_magnitude,

        "large_response_from_mu_to_one_is_denominator_driven":
            True,
    }


def required_cross_mixing_margin_for_transfer(
    transfer: float,
) -> dict[str, float]:
    """Return the largest healthy principal margin compatible with transfer.

    Solve

        mu / (1-mu^2) = T

    for the smallest positive mu that reaches requested transfer T.
    """

    target = _positive(
        transfer,
        "transfer",
    )

    mu_required = (
        math.sqrt(
            1.0
            +
            4.0
            *
            target**2
        )
        -
        1.0
    ) / (
        2.0
        *
        target
    )

    margin = (
        1.0
        -
        mu_required
    )

    return {
        "transfer":
            target,

        "minimum_abs_mu_required":
            mu_required,

        "maximum_minimum_eigenvalue":
            margin,

        "condition_number_at_threshold":
            (
                1.0
                +
                mu_required
            )
            /
            margin,
    }


def einstein_payload_dirichlet_response_norm_j(
    *,
    payload_radius_m: float,
    volume_average_acceleration_mps2: float,
    gravitational_constant_m3_kg_s2: float = (
        GRAVITATIONAL_CONSTANT_M3_KG_S2
    ),
) -> dict[str, Any]:
    """Return the spherical-payload Einstein-potential Dirichlet norm.

    This is not labeled gravitational field energy. It is the positive
    Newtonian/Einstein scalar response norm

        (8 pi G)^-1 integral |grad Phi|^2 dV

    bounded by Cauchy-Schwarz from the volume-average acceleration.
    """

    radius = _positive(
        payload_radius_m,
        "payload_radius_m",
    )

    acceleration = _positive(
        volume_average_acceleration_mps2,
        "volume_average_acceleration_mps2",
    )

    g_constant = _positive(
        gravitational_constant_m3_kg_s2,
        "gravitational_constant_m3_kg_s2",
    )

    volume = (
        4.0
        *
        math.pi
        *
        radius**3
        /
        3.0
    )

    response_norm_j = (
        acceleration**2
        *
        radius**3
        /
        (
            6.0
            *
            g_constant
        )
    )

    return {
        "payload_radius_m":
            radius,

        "volume_m3":
            volume,

        "volume_average_acceleration_mps2":
            acceleration,

        "dirichlet_response_norm_j":
            response_norm_j,

        "dirichlet_response_norm_mj":
            response_norm_j
            /
            1.0e6,

        "strict_10mj_target_j":
            STRICT_ENERGY_TARGET_J,

        "norm_below_strict_10mj_target":
            bool(
                response_norm_j
                <
                STRICT_ENERGY_TARGET_J
            ),

        "is_gauge_invariant_local_gr_energy_theorem":
            False,

        "is_complete_operating_energy":
            False,
    }


def v17_einstein_metric_response_norms() -> dict[str, Any]:
    """Return optimistic 1g and actual V17-average Einstein-response norms."""

    benchmark = (
        einstein_payload_dirichlet_response_norm_j(
            payload_radius_m=
                V17_PAYLOAD_RADIUS_M,

            volume_average_acceleration_mps2=
                STANDARD_GRAVITY_MPS2,
        )
    )

    v17_average = (
        einstein_payload_dirichlet_response_norm_j(
            payload_radius_m=
                V17_PAYLOAD_RADIUS_M,

            volume_average_acceleration_mps2=
                V17_VOLUME_AVERAGE_ACCEL_MPS2,
        )
    )

    return {
        "benchmark_1g":
            benchmark,

        "v17_reported_volume_average":
            v17_average,

        "benchmark_norm_over_10mj":
            (
                benchmark[
                    "dirichlet_response_norm_j"
                ]
                /
                STRICT_ENERGY_TARGET_J
            ),

        "v17_average_norm_over_10mj":
            (
                v17_average[
                    "dirichlet_response_norm_j"
                ]
                /
                STRICT_ENERGY_TARGET_J
            ),
    }


def v26a_gate() -> dict[str, Any]:
    """Return the scoped V26A scientific decision surface."""

    field_strength = (
        normalized_field_strength_portal_bound()
    )

    metric_norms = (
        v17_einstein_metric_response_norms()
    )

    return {
        "phase":
            "032V26A",

        "claim_classification":
            (
                "SCOPED_INVARIANT_BRIDGE_"
                "THEOREM_AND_PREFLIGHT_GATE"
            ),

        "static_pure_disformal_leading_rest_payload_numerator":
            False,

        "static_first_derivative_dhost_class_closed":
            False,

        "all_dhost_closed":
            False,

        "u1_field_strength_leading_portal_healthy_advantage":
            field_strength[
                "healthy_leading_portal_beats_scalar_reference"
            ],

        "all_vector_portals_closed":
            False,

        "near_singular_cross_mixing_as_free_gain_engine_closed":
            True,

        "direct_einstein_metric_response_norm_below_10mj":
            metric_norms[
                "benchmark_1g"
            ][
                "norm_below_strict_10mj_target"
            ],

        "einstein_response_norm_is_energy_theorem":
            False,

        "intrinsic_dirac_hypermomentum_preserved":
            True,

        "tested_linear_metric_affine_bridge_reopened":
            False,

        "all_metric_affine_closed":
            False,

        "riemannian_offstate_exact_nonlinear_mag_target_preserved":
            True,

        "blind_parameter_scan_authorized":
            False,

        "generic_energy_optimization_authorized":
            False,

        "next_action_specific_construction_authorized":
            True,

        "next_phase":
            (
                "032V26B_RIEMANNIAN_OFFSTATE_EXACT_"
                "NONLINEAR_MAG_DIRAC_HYPERMOMENTUM_BRIDGE"
            ),
    }
