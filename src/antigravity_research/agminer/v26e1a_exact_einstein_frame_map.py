"""032V26E1A — exact Class-Ia Einstein-frame map and invertibility gate.

SCIENTIFIC QUESTION
-------------------
Can the protected V26D A3=0 quadratic-DHOST gravitational sector be mapped
to a simple healthy frame by an EXACT LOCAL INVERTIBLE field redefinition,
without obtaining apparent gain from a singular transformation?

V26D uses

    X = g^{mu nu} phi_mu phi_nu

and

    A1 = A2 = A3 = A5 = 0

    A4 = 6 F_X^2 / F.

This is a Class-Ia quadratic-DHOST surface.

For a disformal transformation

    g_tilde_mn
        =
    A(X) g_mn
        +
    B(X) phi_m phi_n,

the published inverse Class-Ia reconstruction equations are

    A_X/A
        =
    [4 F_X + 2 alpha2 + X alpha3]
    /
    [4(F + X alpha2)]

and

    B_X
        =
    [
        (2 F_X + alpha2) A
        -
        (2F + X alpha2) A_X
    ]
    /
    [
        X(F + X alpha2)
    ].

On the V26D surface

    alpha2 = 0
    alpha3 = 0,

therefore

    A_X/A = F_X/F.

A valid solution is

    A = F/F0.

Then the numerator of B_X vanishes identically:

    B_X = 0.

Choose the constant integration branch

    B = 0.

The transformed Horndeski curvature coefficient is

    F_tilde
        =
    A^(-1/2)
    (A + B X)^(-1/2)
    F.

For B=0 and A=F/F0:

    F_tilde = F0,

a constant.

Thus the V26D quadratic higher-derivative gravitational sector is generated
from the Einstein-Hilbert curvature sector through an X-dependent conformal
transformation.

FORWARD RECONSTRUCTION
----------------------
Starting from constant F_tilde and B=0, the published forward equations give

    alpha1 = 0
    alpha2 = 0
    alpha3 = 0
    alpha5 = 0

and

    alpha4
        =
    6 A_X^2 F_tilde / A.

Since

    F = A F_tilde
    F_X = A_X F_tilde,

this becomes exactly

    alpha4 = 6 F_X^2/F,

which is the V26D degeneracy relation.

INVERTIBILITY
-------------
The disformal-map Jacobian is invertible when

    A != 0

and

    D_map
        =
    A
        -
    X A_X
        -
    X^2 B_X
        !=
    0.

For the declared normalized V26D linear scaffold

    F/F0 = 1 + eta x

with

    x = X/Lambda^4,

we have

    A = 1 + eta x
    A_x = eta
    B_x = 0

and therefore

    D_map = 1

IDENTICALLY.

The map is not approaching its non-invertible/mimetic surface.

KINETIC VARIABLE MAP
--------------------
With B=0,

    x_tilde = x/A(x).

For A=1+eta x,

    d x_tilde / dx
        =
    1/A^2

because D_map=1.

The exact inverse is

    x
        =
    x_tilde
        /
    (1 - eta x_tilde)

on the invertible branch.

IMPORTANT CLAIM BOUNDARY
------------------------
This result does NOT establish full V26D health.

The Einstein-Hilbert-equivalent quadratic gravity sector by itself carries
only tensor degrees of freedom.

The scalar mode must come from the lower-derivative scalar sector P(X),
Q(X) Box(phi), hidden matter, or their transformed counterparts.

Therefore V26E1A establishes:

    exact field-redefinition provenance;
    robust invertibility;
    absence of transformation-Jacobian collapse;
    a simpler frame for the next canonical/source-response calculation.

It does NOT establish:

    healthy scalar principal symbol;
    microscopic full-DHOST source solution;
    nonzero physical source->g00 response;
    outward sign;
    finite payload;
    1g at 1m;
    field capacity;
    complete energy.

MATTER FRAME
------------
Ordinary matter remains physically minimal to the original Jordan/DHOST
metric g_mn.

After the invertible transformation to g_tilde_mn, ordinary matter becomes
derivatively/nonminimally coupled through

    g_mn = g_mn[g_tilde, phi].

Thus a calculation using only the Einstein-frame metric perturbation is NOT
a physical observable.

The next gate must reconstruct the physical g00 observable and demonstrate
that the response agrees between frames.

ENERGY POLICY
-------------
No energy optimization.

The HOOK17 ~17.07 J capacity reference does NOT transfer to V26D.

V26D complete energy remains unknown.

CLAIM_CLASSIFICATION
--------------------
EXACT_INVERTIBLE_CLASS_IA_FRAME_EQUIVALENCE_AND_ANTI_SINGULARITY_GATE
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from .v26e0_static_spacelike_tensor_symbol import (
    v26e0_summary,
)


TOL = 1.0e-12

STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7

MIN_OUTWARD_ACCELERATION_M_S2 = 9.80665
MIN_TRUE_STANDOFF_M = 1.0


def v26e0_provenance_gate() -> dict[str, Any]:
    """Require the completed V26E0 tensor/background result."""

    result = v26e0_summary()

    passed = bool(
        result[
            "tensor_sector_partial_green"
        ]
        and
        result[
            "anisotropic_tensor_cone_ct1_established_on_constant_gradient_patch"
        ]
        and
        result[
            "representative_tensor_principal_health_pass"
        ]
        and
        result[
            "full_constrained_scalar_metric_symbol_required"
        ]
        and
        result[
            "v26e1_full_constrained_symbol_crossprop_authorized"
        ]
    )

    return {
        "v26e0_provenance_pass":
            passed,

        "tensor_partial_green":
            result[
                "tensor_sector_partial_green"
            ],

        "tensor_ct1":
            result[
                "anisotropic_tensor_cone_ct1_established_on_constant_gradient_patch"
            ],

        "tensor_margin":
            result[
                "representative_worst_tensor_relative_margin"
            ],

        "scalar_metric_symbol_still_required":
            result[
                "full_constrained_scalar_metric_symbol_required"
            ],

        "crossprop_still_required":
            not result[
                "static_spacelike_source_to_metric_cross_response_established"
            ],
    }


def inverse_class_ia_map(
    *,
    F: float,
    F_X: float,
    X: float,
    F0: float,
) -> dict[str, float]:
    """Apply the published inverse map for alpha2=alpha3=0."""

    f = float(
        F
    )

    f_x = float(
        F_X
    )

    x = float(
        X
    )

    f0 = float(
        F0
    )

    if f <= 0.0:
        raise ValueError(
            "F must be positive"
        )

    if f0 <= 0.0:
        raise ValueError(
            "F0 must be positive"
        )

    if x <= 0.0:
        raise ValueError(
            "X must be positive for active inverse-map witness"
        )

    conformal_a = (
        f
        /
        f0
    )

    conformal_a_x = (
        f_x
        /
        f0
    )

    alpha2 = 0.0
    alpha3 = 0.0

    eq_290_lhs = (
        conformal_a_x
        /
        conformal_a
    )

    eq_290_rhs = (
        (
            4.0
            *
            f_x
            +
            2.0
            *
            alpha2
            +
            x
            *
            alpha3
        )
        /
        (
            4.0
            *
            (
                f
                +
                x
                *
                alpha2
            )
        )
    )

    bx_numerator = (
        (
            2.0
            *
            f_x
            +
            alpha2
        )
        *
        conformal_a
        -
        (
            2.0
            *
            f
            +
            x
            *
            alpha2
        )
        *
        conformal_a_x
    )

    bx_denominator = (
        x
        *
        (
            f
            +
            x
            *
            alpha2
        )
    )

    b_x = (
        bx_numerator
        /
        bx_denominator
    )

    b = 0.0

    f_tilde = (
        f
        /
        math.sqrt(
            conformal_a
            *
            (
                conformal_a
                +
                b
                *
                x
            )
        )
    )

    invertibility_d = (
        conformal_a
        -
        x
        *
        conformal_a_x
        -
        x**2
        *
        b_x
    )

    return {
        "F":
            f,

        "F_X":
            f_x,

        "X":
            x,

        "F0":
            f0,

        "A":
            conformal_a,

        "A_X":
            conformal_a_x,

        "B":
            b,

        "B_X":
            b_x,

        "eq_2_90_lhs":
            eq_290_lhs,

        "eq_2_90_rhs":
            eq_290_rhs,

        "eq_2_90_error":
            abs(
                eq_290_lhs
                -
                eq_290_rhs
            ),

        "eq_2_89_bx_numerator":
            bx_numerator,

        "F_tilde":
            f_tilde,

        "invertibility_D":
            invertibility_d,

        "A_nonzero":
            bool(
                abs(
                    conformal_a
                )
                >
                TOL
            ),

        "D_nonzero":
            bool(
                abs(
                    invertibility_d
                )
                >
                TOL
            ),

        "map_invertible":
            bool(
                abs(
                    conformal_a
                )
                >
                TOL
                and
                abs(
                    invertibility_d
                )
                >
                TOL
            ),
    }


def forward_eh_reconstruction(
    *,
    A: float,
    A_X: float,
    F_tilde: float,
) -> dict[str, float]:
    """Forward-transform constant-F_tilde EH with B=0."""

    a = float(
        A
    )

    a_x = float(
        A_X
    )

    f_tilde = float(
        F_tilde
    )

    if a <= 0.0:
        raise ValueError(
            "A must be positive"
        )

    f = (
        a
        *
        f_tilde
    )

    f_x = (
        a_x
        *
        f_tilde
    )

    alpha1 = 0.0
    alpha2 = 0.0
    alpha3 = 0.0

    alpha4 = (
        6.0
        *
        a_x**2
        *
        f_tilde
        /
        a
    )

    alpha5 = 0.0

    expected_alpha4 = (
        6.0
        *
        f_x**2
        /
        f
    )

    return {
        "A":
            a,

        "A_X":
            a_x,

        "F_tilde":
            f_tilde,

        "F":
            f,

        "F_X":
            f_x,

        "alpha1":
            alpha1,

        "alpha2":
            alpha2,

        "alpha3":
            alpha3,

        "alpha4":
            alpha4,

        "alpha5":
            alpha5,

        "expected_v26d_alpha4":
            expected_alpha4,

        "alpha4_reconstruction_error":
            abs(
                alpha4
                -
                expected_alpha4
            ),

        "v26d_quadratic_coefficients_reconstructed":
            bool(
                alpha1
                ==
                0.0
                and
                alpha2
                ==
                0.0
                and
                alpha3
                ==
                0.0
                and
                alpha5
                ==
                0.0
                and
                abs(
                    alpha4
                    -
                    expected_alpha4
                )
                <=
                TOL
            ),
    }


def normalized_linear_map(
    *,
    x: float,
    eta: float,
) -> dict[str, float | bool]:
    """Return exact dimensionless map for F/F0=1+eta*x."""

    x_value = float(
        x
    )

    eta_value = float(
        eta
    )

    a = (
        1.0
        +
        eta_value
        *
        x_value
    )

    if a <= 0.0:
        raise ValueError(
            "normalized F/A must remain positive"
        )

    a_x = eta_value
    b_x = 0.0

    d_map = (
        a
        -
        x_value
        *
        a_x
        -
        x_value**2
        *
        b_x
    )

    x_tilde = (
        x_value
        /
        a
    )

    d_xtilde_dx = (
        d_map
        /
        a**2
    )

    return {
        "x":
            x_value,

        "eta":
            eta_value,

        "A":
            a,

        "A_x":
            a_x,

        "B_x":
            b_x,

        "D_map":
            d_map,

        "x_tilde":
            x_tilde,

        "d_x_tilde_d_x":
            d_xtilde_dx,

        "A_positive":
            bool(
                a
                >
                0.0
            ),

        "D_exactly_one":
            bool(
                abs(
                    d_map
                    -
                    1.0
                )
                <=
                TOL
            ),

        "map_invertible":
            bool(
                a
                >
                0.0
                and
                abs(
                    d_map
                )
                >
                TOL
            ),

        "transformation_jacobian_margin_collapse":
            False,
    }


def inverse_normalized_kinetic_map(
    *,
    x_tilde: float,
    eta: float,
) -> float:
    """Invert x_tilde=x/(1+eta*x)."""

    xt = float(
        x_tilde
    )

    eta_value = float(
        eta
    )

    denominator = (
        1.0
        -
        eta_value
        *
        xt
    )

    if abs(
        denominator
    ) <= TOL:
        raise ValueError(
            "inverse kinetic map reached singular branch"
        )

    return (
        xt
        /
        denominator
    )


def representative_frame_gate() -> dict[str, Any]:
    """Evaluate the exact representative V26D active point."""

    row = normalized_linear_map(
        x=
            0.10,

        eta=
            0.50,
    )

    inverse = inverse_normalized_kinetic_map(
        x_tilde=
            float(
                row[
                    "x_tilde"
                ]
            ),

        eta=
            0.50,
    )

    return {
        **row,

        "expected_A":
            1.05,

        "expected_D_map":
            1.0,

        "inverse_roundtrip_x":
            inverse,

        "roundtrip_error":
            abs(
                inverse
                -
                0.10
            ),

        "representative_frame_map_green":
            bool(
                row[
                    "map_invertible"
                ]
                and
                row[
                    "D_exactly_one"
                ]
                and
                abs(
                    float(
                        row[
                            "A"
                        ]
                    )
                    -
                    1.05
                )
                <=
                TOL
                and
                abs(
                    inverse
                    -
                    0.10
                )
                <=
                TOL
            ),
    }


def invertibility_identity_scan() -> list[dict[str, Any]]:
    """Identity scan only; not an optimization."""

    eta_values = (
        -0.75,
        -0.25,
        0.10,
        0.50,
        1.00,
        2.00,
    )

    x_values = (
        0.0,
        0.05,
        0.10,
        0.25,
        0.50,
        1.00,
    )

    rows: list[
        dict[str, Any]
    ] = []

    for eta in eta_values:
        for x in x_values:
            a = (
                1.0
                +
                eta
                *
                x
            )

            if a <= 0.0:
                continue

            row = normalized_linear_map(
                x=
                    x,

                eta=
                    eta,
            )

            rows.append(
                {
                    **row,

                    "identity_scan_only":
                        True,

                    "energy_point":
                        False,
                }
            )

    return rows


def invertibility_scan_gate() -> dict[str, Any]:
    """Require exact D=1 and positive A on every admitted scan point."""

    rows = invertibility_identity_scan()

    minimum_a = min(
        float(
            row[
                "A"
            ]
        )
        for row in rows
    )

    minimum_abs_d = min(
        abs(
            float(
                row[
                    "D_map"
                ]
            )
        )
        for row in rows
    )

    all_d_one = all(
        row[
            "D_exactly_one"
        ]
        for row in rows
    )

    all_invertible = all(
        row[
            "map_invertible"
        ]
        for row in rows
    )

    return {
        "scan_point_count":
            len(
                rows
            ),

        "minimum_A":
            minimum_a,

        "minimum_abs_D_map":
            minimum_abs_d,

        "all_admitted_points_D_exactly_one":
            all_d_one,

        "all_admitted_points_invertible":
            all_invertible,

        "near_noninvertible_points_used":
            False,

        "identity_scan_not_parameter_optimization":
            True,

        "scan_gate_pass":
            bool(
                rows
                and
                all_d_one
                and
                all_invertible
                and
                minimum_abs_d
                >=
                1.0
                -
                TOL
            ),
    }


def explicit_inverse_map_gate() -> dict[str, Any]:
    """Check published inverse equations at a generic active point."""

    result = inverse_class_ia_map(
        F=
            1.30,

        F_X=
            0.40,

        X=
            0.25,

        F0=
            1.0,
    )

    return {
        **result,

        "eq_2_90_pass":
            bool(
                result[
                    "eq_2_90_error"
                ]
                <=
                TOL
            ),

        "B_X_zero":
            bool(
                abs(
                    result[
                        "B_X"
                    ]
                )
                <=
                TOL
            ),

        "F_tilde_constant_F0":
            bool(
                abs(
                    result[
                        "F_tilde"
                    ]
                    -
                    result[
                        "F0"
                    ]
                )
                <=
                TOL
            ),
    }


def forward_reconstruction_gate() -> dict[str, Any]:
    """Independently reconstruct the V26D coefficients from EH."""

    result = forward_eh_reconstruction(
        A=
            1.30,

        A_X=
            0.40,

        F_tilde=
            1.0,
    )

    return {
        **result,

        "eh_forward_reconstruction_pass":
            result[
                "v26d_quadratic_coefficients_reconstructed"
            ],
    }


def frame_observable_discipline_gate() -> dict[str, Any]:
    """Record what invertible frame equivalence does and does not imply."""

    return {
        "jordan_dhost_metric":
            "g_mu_nu",

        "einstein_frame_metric":
            "g_tilde_mu_nu",

        "declared_relation":
            "g_tilde_mu_nu=A(X)*g_mu_nu",

        "ordinary_matter_minimal_in_jordan_frame":
            True,

        "ordinary_matter_minimal_in_einstein_frame":
            False,

        "matter_action_must_be_transformed":
            True,

        "einstein_metric_response_alone_is_physical_observable":
            False,

        "physical_g00_must_be_reconstructed":
            True,

        "field_redefinition_can_erase_physical_kmm_by_relabeling":
            False,

        "same_observable_must_match_between_frames":
            True,

        "physical_cross_response_established":
            False,

        "frame_invariant_cross_response_gate_required":
            True,
    }


def v26e1a_summary() -> dict[str, Any]:
    """Return conservative V26E1A decision."""

    provenance = v26e0_provenance_gate()

    inverse = explicit_inverse_map_gate()

    forward = forward_reconstruction_gate()

    representative = representative_frame_gate()

    scan = invertibility_scan_gate()

    discipline = frame_observable_discipline_gate()

    partial_green = bool(
        provenance[
            "v26e0_provenance_pass"
        ]
        and
        inverse[
            "eq_2_90_pass"
        ]
        and
        inverse[
            "B_X_zero"
        ]
        and
        inverse[
            "F_tilde_constant_F0"
        ]
        and
        inverse[
            "map_invertible"
        ]
        and
        forward[
            "eh_forward_reconstruction_pass"
        ]
        and
        representative[
            "representative_frame_map_green"
        ]
        and
        scan[
            "scan_gate_pass"
        ]
    )

    return {
        "branch":
            "032V26E1A",

        "subgate":
            "EXACT_CLASS_IA_EINSTEIN_FRAME_MAP_AND_INVERTIBILITY",

        "decision":
            (
                "GREEN_PARTIAL_V26E1A_V26D_QUADRATIC_DHOST_"
                "SECTOR_HAS_EXACT_NONSINGULAR_EINSTEIN_FRAME_MAP__"
                "FULL_SCALAR_HEALTH_AND_PHYSICAL_G00_CROSS_RESPONSE_"
                "REMAIN_REQUIRED"
            )
            if partial_green
            else
            "CHECK_V26E1A_CLASS_IA_MAP_OR_INVERTIBILITY",

        "v26e0_provenance_pass":
            provenance[
                "v26e0_provenance_pass"
            ],

        "inverse_class_ia_equations_pass":
            bool(
                inverse[
                    "eq_2_90_pass"
                ]
                and
                inverse[
                    "B_X_zero"
                ]
                and
                inverse[
                    "F_tilde_constant_F0"
                ]
            ),

        "forward_eh_reconstructs_v26d_coefficients":
            forward[
                "eh_forward_reconstruction_pass"
            ],

        "quadratic_dhost_gravity_sector_eh_equivalent":
            partial_green,

        "representative_A":
            representative[
                "A"
            ],

        "representative_D_map":
            representative[
                "D_map"
            ],

        "representative_map_invertible":
            representative[
                "map_invertible"
            ],

        "linear_F_map_D_identically_one":
            scan[
                "all_admitted_points_D_exactly_one"
            ],

        "minimum_scanned_map_jacobian_margin":
            scan[
                "minimum_abs_D_map"
            ],

        "field_redefinition_near_singular":
            False,

        "field_redefinition_margin_collapse_used_for_gain":
            False,

        "einstein_frame_curvature_coefficient_constant":
            True,

        "higher_derivative_gravity_sector_supplies_independent_scalar_mode":
            False,

        "lower_derivative_scalar_completion_required":
            True,

        "full_static_spacelike_scalar_health_established":
            False,

        "ordinary_matter_minimal_in_physical_jordan_frame":
            discipline[
                "ordinary_matter_minimal_in_jordan_frame"
            ],

        "ordinary_matter_minimal_in_einstein_frame":
            discipline[
                "ordinary_matter_minimal_in_einstein_frame"
            ],

        "physical_g00_cross_response_established":
            False,

        "frame_invariant_cross_response_audit_required":
            discipline[
                "frame_invariant_cross_response_gate_required"
            ],

        "constraint_elimination_complete":
            False,

        "microscopic_source_solution_full_dhost_established":
            False,

        "outward_sign_established":
            False,

        "finite_payload_established":
            False,

        "minimum_required_outward_acceleration_m_s2":
            MIN_OUTWARD_ACCELERATION_M_S2,

        "minimum_required_true_standoff_m":
            MIN_TRUE_STANDOFF_M,

        "performance_above_floor_is_favorable":
            True,

        "v26d_field_capacity_j":
            None,

        "v26d_complete_energy_j":
            None,

        "hook17_capacity_reference_transfers_to_v26d":
            False,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "energy_optimization_authorized":
            False,

        "agminer_database_mutation_authorized":
            False,

        "v26e1a_partial_green":
            partial_green,

        "v26e1b_authorized":
            partial_green,

        "next":
            (
                "032V26E1B_EINSTEIN_FRAME_HEALTHY_SCALAR_"
                "AND_PHYSICAL_G00_CROSSPROP_GATE"
            ),

        "claim_scope":
            (
                "EXACT INVERTIBLE FIELD-REDEFINITION PROVENANCE OF "
                "THE V26D QUADRATIC GRAVITATIONAL SECTOR; NOT FULL "
                "SCALAR-METRIC HEALTH OR ANTIGRAVITY RESPONSE"
            ),
    }
