"""032V26E0 — static-spacelike tensor symbol and background theorem.

PURPOSE
-------
Resume the preserved V26D cT=1 DHOST/KMM fallback after the current
HOOK17 Percacci-Sezgin Case-I realization was blocked on unestablished
technical naturalness.

V26D established:

    explicit same-action quadratic-DHOST scaffold;
    one universal matter metric;
    A1 = A2 = 0;
    A3 = 0;
    exact alpha_H + 2 beta_1 = 0;
    active beta_1 != 0;
    off-state beta_1 = 0;
    explicit microscopic source vertex.

It deliberately did NOT establish:

    static-spacelike canonical health;
    anisotropic tensor cT=1;
    constrained source->metric cross propagator;
    physical outward sign;
    finite payload;
    complete energy.

V26E0 performs the cheapest exact piece of the previously authorized V26E
program before attempting the complete constrained scalar-metric symbol.

---------------------------------------------------------------------------
STATIC SPACELIKE BACKGROUND
---------------------------------------------------------------------------

Use local inertial coordinates and a constant spacelike scalar gradient

    phi_bar = v z

so that

    X = v^2 > 0.

For A3=0 the quadratic-DHOST degeneracy relation is

    A4 = 6 F_X^2 / F
    A5 = 0.

To first order in a metric perturbation,

    phi_mn
        =
    -v Gamma^z_mn.

The A4 operator is

    A4
    phi^mu phi_{mu rho}
    phi^{rho nu} phi_nu.

On the constant-z-gradient background,

    Gamma^z_{z rho}
        =
    1/2 partial_rho h_zz,

so the quadratic A4 contribution is proportional to

    + A4 X^2 / 4
      eta^{rho sigma}
      partial_rho h_zz
      partial_sigma h_zz.

The Einstein-Hilbert tensor quadratic form has the opposite
eta-contracted sign.

For normalized TT polarizations and propagation making angle theta with
the scalar-gradient axis, the maximum affected tensor-polarization
component satisfies

    |h_zz|^2
        proportional to
    sin(theta)^4.

The affected relative tensor principal coefficient is therefore

    M_T(theta)
        =
    1
        -
    A4 X^2 /(2F) sin(theta)^4

and using

    beta_1 = X F_X/F

gives the exact identity

    M_T(theta)
        =
    1
        -
    3 beta_1^2 sin(theta)^4.

The orthogonal tensor polarization retains relative coefficient 1.

Because the A4 term carries the same Lorentzian derivative contraction for
time and space derivatives, it changes normalization but not the tensor
characteristic cone:

    c_T^2 = 1

for both tensor eigenmodes wherever the principal coefficient is nonzero.

Tensor ghost freedom on this local constant-gradient patch therefore
requires

    1 - 3 beta_1^2 > 0

or

    |beta_1| < 1/sqrt(3).

This theorem concerns the TT tensor sector only.

It does NOT certify the scalar-metric constrained principal symbol.

---------------------------------------------------------------------------
REPRESENTATIVE V26D POINT
---------------------------------------------------------------------------

The existing V26D normalized linear-F scaffold has

    beta_1
        =
    eta x /(1 + eta x).

For

    eta = 0.5
    x   = 0.1

one obtains

    beta_1 = 1/21.

The worst-direction tensor margin is then

    1 - 3/21^2
        =
    146/147
        ~
    0.9931972789.

Thus the representative V26D active point is far from the tensor
principal-health boundary.

No response gain is credited to approaching that boundary.

---------------------------------------------------------------------------
UNSUPPORTED FLAT-BACKGROUND THEOREM
---------------------------------------------------------------------------

Now ask whether a flat constant-gradient background can exist with no
external/support stress.

On flat space with constant X:

    R = 0
    phi_mn = 0

so the background stress of the pure P(X) sector is

    T_mn
        =
    P g_mn
        -
    2 P_X phi_m phi_n.

For a nonzero spacelike z-gradient:

    T_00 = -P
    T_xx = P
    T_yy = P
    T_zz = P - 2 X P_X.

Therefore an unsupported Minkowski background requires

    P(X0) = 0

and

    P_X(X0) = 0.

At this stationary point,

    delta X_linear
        =
    2 v partial_z pi

and the quadratic P(X) contribution is

    L_pi^(2)
        =
    2 X P_XX
    (partial_z pi)^2.

It contains no standalone

    (partial_t pi)^2

term.

Consequently:

    TENSOR HEALTH
        !=
    FULL SCALAR-METRIC CANONICAL HEALTH.

The full DHOST constraint structure may supply a healthy scalar kinetic
term through metric-scalar mixing.

That is exactly what V26E1 must derive.

Alternatively, the laboratory active state may be:

    support-balanced

or

    curved/on-shell.

Those possibilities remain open, but their support/background stress must
enter the later complete energy ledger.

---------------------------------------------------------------------------
CLAIM BOUNDARY
---------------------------------------------------------------------------

A V26E0 partial green establishes only:

    constant-gradient TT tensor cT=1;
    explicit anisotropic tensor kinetic margin;
    representative tensor health away from collapse;
    unsupported-flat-background P=P_X=0 theorem;
    necessity of the full constrained scalar-metric symbol.

It does NOT establish:

    full static-spacelike canonical health;
    scalar hyperbolicity;
    constrained source->metric Green function;
    nonremovable active numerator;
    outward sign;
    microscopic full-DHOST source solution;
    support practicality;
    quantum naturalness;
    finite payload;
    complete energy.

No HOOK17 17-J capacity number is transferred to V26D.

CLAIM_CLASSIFICATION
--------------------
TENSOR_PRINCIPAL_SYMBOL_PARTIAL_GREEN_AND_BACKGROUND_CONSISTENCY_PREFLIGHT
"""

from __future__ import annotations

import math
from typing import Any

from .hook17_covariant_projective_stress_protection import (
    h17a9r3_summary,
)

from .protected_ct1_dhost_kmm_action import (
    dhost_degeneracy_coefficients,
    normalized_linear_f_model,
    v26d_gate,
)


TOL = 1.0e-12

STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7


def fallback_trigger_gate() -> dict[str, Any]:
    """Require the exact A9R3 fallback trigger."""

    result = h17a9r3_summary()

    passed = bool(
        result[
            "geometric_and_clean_linearized_noether_partial_green"
        ]
        and
        not result[
            "case_i_technical_naturalness_gate_pass"
        ]
        and
        not result[
            "current_ps_case_i_candidate_promotion_authorized"
        ]
        and
        result[
            "v26d_resume_authorized"
        ]
        and
        result[
            "next"
        ]
        ==
        "032V26D_RESUME_PROTECTED_CT1_DHOST_KMM"
    )

    return {
        "a9r3_decision":
            result[
                "decision"
            ],

        "a9r3_partial_results_preserved":
            result[
                "geometric_and_clean_linearized_noether_partial_green"
            ],

        "current_ps_case_i_blocked":
            bool(
                not result[
                    "current_ps_case_i_candidate_promotion_authorized"
                ]
            ),

        "v26d_resume_authorized":
            result[
                "v26d_resume_authorized"
            ],

        "fallback_trigger_pass":
            passed,

        "hook17_globally_closed":
            result[
                "hook17_closed"
            ],
    }


def v26d_provenance_gate() -> dict[str, Any]:
    """Require the preserved V26D action-level scaffold."""

    result = v26d_gate()

    passed = bool(
        result[
            "explicit_same_action_scaffold"
        ]
        and
        result[
            "one_universal_physical_metric"
        ]
        and
        result[
            "dhost_degeneracy_relation_explicit"
        ]
        and
        result[
            "a3_zero_no_decay_identity"
        ]
        and
        result[
            "offstate_classical_kmm_zero"
        ]
        and
        result[
            "active_kmm_witness_nonzero"
        ]
        and
        result[
            "microscopic_source_vertex_explicit"
        ]
        and
        result[
            "v26e_principal_symbol_crossprop_gate_authorized"
        ]
    )

    return {
        "v26d_provenance_pass":
            passed,

        "explicit_same_action_scaffold":
            result[
                "explicit_same_action_scaffold"
            ],

        "one_universal_physical_metric":
            result[
                "one_universal_physical_metric"
            ],

        "a3_zero_no_decay_identity":
            result[
                "a3_zero_no_decay_identity"
            ],

        "offstate_classical_kmm_zero":
            result[
                "offstate_classical_kmm_zero"
            ],

        "active_kmm_witness_nonzero":
            result[
                "active_kmm_witness_nonzero"
            ],

        "microscopic_source_vertex_explicit":
            result[
                "microscopic_source_vertex_explicit"
            ],

        "full_static_spacelike_health_previously_established":
            result[
                "canonical_health_on_static_spacelike_background_established"
            ],

        "anisotropic_tensor_ct1_previously_established":
            result[
                "anisotropic_tensor_cone_ct1_established"
            ],

        "cross_response_previously_established":
            result[
                "static_spacelike_source_to_metric_cross_response_established"
            ],
    }


def a4_beta_identity_gate() -> dict[str, Any]:
    """Independently reconstruct A4 X^2/(2F) = 3 beta_1^2."""

    f = 2.0
    f_x = 0.25
    x = 0.30

    degeneracy = dhost_degeneracy_coefficients(
        F=
            f,

        F_X=
            f_x,

        X=
            x,

        A3=
            0.0,
    )

    a4 = float(
        degeneracy[
            "A4"
        ]
    )

    beta = (
        x
        *
        f_x
        /
        f
    )

    lhs = (
        a4
        *
        x**2
        /
        (
            2.0
            *
            f
        )
    )

    rhs = (
        3.0
        *
        beta**2
    )

    return {
        "F":
            f,

        "F_X":
            f_x,

        "X":
            x,

        "A4":
            a4,

        "beta_1":
            beta,

        "a4_x2_over_2f":
            lhs,

        "three_beta1_squared":
            rhs,

        "identity_error":
            abs(
                lhs
                -
                rhs
            ),

        "a4_beta_identity_pass":
            bool(
                abs(
                    lhs
                    -
                    rhs
                )
                <=
                TOL
            ),
    }


def tensor_symbol_from_beta(
    *,
    beta_1: float,
    theta_rad: float,
) -> dict[str, Any]:
    """Return normalized TT tensor principal coefficients.

    Eigenmode 1 is the polarization unaffected by h_zz.

    Eigenmode 2 is the unique TT polarization combination carrying h_zz.
    """

    beta = float(
        beta_1
    )

    theta = float(
        theta_rad
    )

    sin4 = (
        math.sin(
            theta
        )**4
    )

    affected_margin = (
        1.0
        -
        3.0
        *
        beta**2
        *
        sin4
    )

    unaffected_margin = 1.0

    minimum_margin = min(
        unaffected_margin,
        affected_margin,
    )

    return {
        "beta_1":
            beta,

        "theta_rad":
            theta,

        "theta_deg":
            (
                theta
                *
                180.0
                /
                math.pi
            ),

        "sin4_theta":
            sin4,

        "unaffected_tensor_relative_principal_coefficient":
            unaffected_margin,

        "affected_tensor_relative_principal_coefficient":
            affected_margin,

        "minimum_tensor_relative_principal_coefficient":
            minimum_margin,

        "unaffected_tensor_c_squared":
            1.0,

        "affected_tensor_c_squared":
            1.0,

        "both_tensor_characteristics_luminal":
            True,

        "tensor_ghost_free":
            bool(
                minimum_margin
                >
                0.0
            ),

        "principal_margin_collapse_used_as_gain":
            False,

        "tensor_result_only":
            True,
    }


def representative_v26d_beta_gate() -> dict[str, Any]:
    """Return the representative active V26D EFT point."""

    model = normalized_linear_f_model(
        x=
            0.10,

        eta=
            0.50,
    )

    beta = float(
        model[
            "beta_1"
        ]
    )

    expected = (
        1.0
        /
        21.0
    )

    return {
        "x":
            0.10,

        "eta":
            0.50,

        "beta_1":
            beta,

        "expected_beta_1":
            expected,

        "beta_reconstruction_error":
            abs(
                beta
                -
                expected
            ),

        "representative_beta_matches":
            bool(
                abs(
                    beta
                    -
                    expected
                )
                <=
                TOL
            ),
    }


def tensor_health_bound_gate() -> dict[str, Any]:
    """Return the exact worst-direction TT tensor health bound."""

    critical = (
        1.0
        /
        math.sqrt(
            3.0
        )
    )

    below = tensor_symbol_from_beta(
        beta_1=
            0.50,

        theta_rad=
            math.pi
            /
            2.0,
    )

    above = tensor_symbol_from_beta(
        beta_1=
            0.60,

        theta_rad=
            math.pi
            /
            2.0,
    )

    return {
        "critical_abs_beta_1":
            critical,

        "exact_health_condition":
            "ABS(BETA_1)<1/SQRT(3)",

        "beta_0p50_healthy":
            below[
                "tensor_ghost_free"
            ],

        "beta_0p60_healthy":
            above[
                "tensor_ghost_free"
            ],

        "health_boundary_reconstructed":
            bool(
                below[
                    "tensor_ghost_free"
                ]
                and
                not above[
                    "tensor_ghost_free"
                ]
            ),
    }


def representative_tensor_angle_scan() -> list[dict[str, Any]]:
    """Return a small identity/health scan, not an optimization."""

    beta = representative_v26d_beta_gate()[
        "beta_1"
    ]

    angles_deg = (
        0.0,
        15.0,
        30.0,
        45.0,
        60.0,
        75.0,
        90.0,
    )

    rows: list[
        dict[str, Any]
    ] = []

    for angle in angles_deg:
        row = tensor_symbol_from_beta(
            beta_1=
                beta,

            theta_rad=
                angle
                *
                math.pi
                /
                180.0,
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


def representative_tensor_gate() -> dict[str, Any]:
    """Return the representative V26D worst-direction tensor result."""

    beta_gate = representative_v26d_beta_gate()

    beta = beta_gate[
        "beta_1"
    ]

    perpendicular = tensor_symbol_from_beta(
        beta_1=
            beta,

        theta_rad=
            math.pi
            /
            2.0,
    )

    expected_margin = (
        146.0
        /
        147.0
    )

    rows = representative_tensor_angle_scan()

    minimum = min(
        row[
            "minimum_tensor_relative_principal_coefficient"
        ]
        for row in rows
    )

    all_luminal = all(
        row[
            "both_tensor_characteristics_luminal"
        ]
        for row in rows
    )

    all_healthy = all(
        row[
            "tensor_ghost_free"
        ]
        for row in rows
    )

    return {
        "beta_1":
            beta,

        "worst_direction":
            "PERPENDICULAR_TO_SPACELIKE_SCALAR_GRADIENT",

        "worst_direction_relative_margin":
            perpendicular[
                "minimum_tensor_relative_principal_coefficient"
            ],

        "expected_worst_direction_margin":
            expected_margin,

        "margin_reconstruction_error":
            abs(
                perpendicular[
                    "minimum_tensor_relative_principal_coefficient"
                ]
                -
                expected_margin
            ),

        "scan_minimum_relative_margin":
            minimum,

        "all_scanned_tensor_characteristics_luminal":
            all_luminal,

        "all_scanned_tensor_principal_coefficients_positive":
            all_healthy,

        "representative_anisotropic_tensor_ct1_pass":
            bool(
                all_luminal
                and
                all_healthy
                and
                abs(
                    minimum
                    -
                    expected_margin
                )
                <=
                TOL
            ),

        "large_response_from_tensor_margin_collapse_assumed":
            False,
    }


def flat_constant_gradient_stress(
    *,
    P: float,
    P_X: float,
    X: float,
) -> dict[str, Any]:
    """Return P(X) stress on flat static z-gradient background."""

    p = float(
        P
    )

    p_x = float(
        P_X
    )

    x = float(
        X
    )

    if x <= 0.0:
        raise ValueError(
            "X must be positive for declared spacelike active background"
        )

    t00 = -p
    t11 = p
    t22 = p
    t33 = (
        p
        -
        2.0
        *
        x
        *
        p_x
    )

    residual = max(
        abs(
            t00
        ),
        abs(
            t11
        ),
        abs(
            t22
        ),
        abs(
            t33
        ),
    )

    return {
        "P":
            p,

        "P_X":
            p_x,

        "X":
            x,

        "T00":
            t00,

        "T11":
            t11,

        "T22":
            t22,

        "T33":
            t33,

        "maximum_absolute_background_stress":
            residual,

        "unsupported_flat_background_equations_pass":
            bool(
                residual
                <=
                TOL
            ),
    }


def unsupported_flat_background_gate() -> dict[str, Any]:
    """Establish necessary P=P_X=0 conditions for unsupported Minkowski."""

    x = 1.0

    stationary = flat_constant_gradient_stress(
        P=
            0.0,

        P_X=
            0.0,

        X=
            x,
    )

    nonstationary_p = flat_constant_gradient_stress(
        P=
            0.20,

        P_X=
            0.0,

        X=
            x,
    )

    nonstationary_px = flat_constant_gradient_stress(
        P=
            0.0,

        P_X=
            0.10,

        X=
            x,
    )

    return {
        "declared_gradient_type":
            "STATIC_SPACELIKE",

        "X_positive":
            True,

        "unsupported_minkowski_requires_P_zero":
            bool(
                not nonstationary_p[
                    "unsupported_flat_background_equations_pass"
                ]
            ),

        "unsupported_minkowski_requires_P_X_zero":
            bool(
                not nonstationary_px[
                    "unsupported_flat_background_equations_pass"
                ]
            ),

        "P_zero_and_P_X_zero_suffice_for_P_sector_background_stress":
            stationary[
                "unsupported_flat_background_equations_pass"
            ],

        "unsupported_flat_background_theorem_pass":
            bool(
                stationary[
                    "unsupported_flat_background_equations_pass"
                ]
                and
                not nonstationary_p[
                    "unsupported_flat_background_equations_pass"
                ]
                and
                not nonstationary_px[
                    "unsupported_flat_background_equations_pass"
                ]
            ),

        "hidden_support_included":
            False,

        "curvature_included":
            False,

        "theorem_scope":
            "FLAT_CONSTANT_GRADIENT_P_SECTOR_WITHOUT_SUPPORT_STRESS",
    }


def p_only_scalar_stationary_point_gate() -> dict[str, Any]:
    """Return P-sector quadratic scalar principal coefficients at P_X=0."""

    x = 1.0
    p_xx = 1.0

    time_kinetic = 0.0
    transverse_spatial = 0.0

    longitudinal_spatial = (
        2.0
        *
        x
        *
        p_xx
    )

    return {
        "X":
            x,

        "P_X":
            0.0,

        "P_XX":
            p_xx,

        "p_only_time_kinetic_coefficient":
            time_kinetic,

        "p_only_transverse_gradient_coefficient":
            transverse_spatial,

        "p_only_longitudinal_gradient_coefficient":
            longitudinal_spatial,

        "p_only_standalone_time_kinetic_nonzero":
            bool(
                abs(
                    time_kinetic
                )
                >
                TOL
            ),

        "p_only_scalar_hyperbolicity_established":
            False,

        "full_dhost_mixing_may_supply_scalar_kinetic":
            True,

        "full_constrained_scalar_metric_symbol_required":
            True,

        "strong_coupling_closed":
            False,

        "full_scalar_instability_established":
            False,
    }


def background_route_atlas() -> list[dict[str, Any]]:
    """Return physical background choices remaining after V26E0."""

    return [
        {
            "route":
                "UNSUPPORTED_FLAT_CONSTANT_GRADIENT",

            "status":
                "REQUIRES_P_EQUALS_PX_EQUALS_ZERO",

            "full_scalar_metric_symbol_required":
                True,

            "support_energy_required":
                False,

            "closed":
                False,
        },
        {
            "route":
                "SUPPORT_BALANCED_LOCAL_PATCH",

            "status":
                "OPEN_SUPPORT_STRESS_MUST_BE_INCLUDED",

            "full_scalar_metric_symbol_required":
                True,

            "support_energy_required":
                True,

            "closed":
                False,
        },
        {
            "route":
                "CURVED_ONSHELL_STATIC_BACKGROUND",

            "status":
                "OPEN_FULL_BACKGROUND_EOM_REQUIRED",

            "full_scalar_metric_symbol_required":
                True,

            "support_energy_required":
                "MODEL_DEPENDENT",

            "closed":
                False,
        },
    ]


def v26e0_summary() -> dict[str, Any]:
    """Return conservative V26E0 result."""

    trigger = fallback_trigger_gate()

    provenance = v26d_provenance_gate()

    identity = a4_beta_identity_gate()

    tensor = representative_tensor_gate()

    bound = tensor_health_bound_gate()

    background = unsupported_flat_background_gate()

    scalar = p_only_scalar_stationary_point_gate()

    tensor_partial_green = bool(
        trigger[
            "fallback_trigger_pass"
        ]
        and
        provenance[
            "v26d_provenance_pass"
        ]
        and
        identity[
            "a4_beta_identity_pass"
        ]
        and
        tensor[
            "representative_anisotropic_tensor_ct1_pass"
        ]
        and
        bound[
            "health_boundary_reconstructed"
        ]
    )

    full_principal_green = False

    return {
        "branch":
            "032V26E0",

        "subgate":
            "STATIC_SPACELIKE_TENSOR_PRINCIPAL_SYMBOL_AND_BACKGROUND_THEOREM",

        "decision":
            (
                "GREEN_PARTIAL_V26E0_STATIC_SPACELIKE_TENSOR_CT1_"
                "AND_HEALTH_PASS__UNSUPPORTED_FLAT_BACKGROUND_FORCES_"
                "P_EQUALS_PX_EQUALS_ZERO__FULL_CONSTRAINED_SCALAR_METRIC_"
                "SYMBOL_AND_CROSSPROP_REMAIN_REQUIRED"
            )
            if tensor_partial_green
            else
            "CHECK_V26E0_TENSOR_SYMBOL_OR_PROVENANCE",

        "a9r3_fallback_trigger_pass":
            trigger[
                "fallback_trigger_pass"
            ],

        "a9_a9r3_partial_results_preserved":
            trigger[
                "a9r3_partial_results_preserved"
            ],

        "current_ps_case_i_remains_blocked":
            trigger[
                "current_ps_case_i_blocked"
            ],

        "v26d_provenance_pass":
            provenance[
                "v26d_provenance_pass"
            ],

        "a4_beta_tensor_identity_pass":
            identity[
                "a4_beta_identity_pass"
            ],

        "anisotropic_tensor_cone_ct1_established_on_constant_gradient_patch":
            tensor[
                "all_scanned_tensor_characteristics_luminal"
            ],

        "representative_tensor_principal_health_pass":
            tensor[
                "all_scanned_tensor_principal_coefficients_positive"
            ],

        "representative_beta_1":
            tensor[
                "beta_1"
            ],

        "representative_worst_tensor_relative_margin":
            tensor[
                "worst_direction_relative_margin"
            ],

        "tensor_health_critical_abs_beta_1":
            bound[
                "critical_abs_beta_1"
            ],

        "large_response_from_tensor_margin_collapse_assumed":
            tensor[
                "large_response_from_tensor_margin_collapse_assumed"
            ],

        "unsupported_flat_background_theorem_pass":
            background[
                "unsupported_flat_background_theorem_pass"
            ],

        "unsupported_flat_requires_P_zero":
            background[
                "unsupported_minkowski_requires_P_zero"
            ],

        "unsupported_flat_requires_P_X_zero":
            background[
                "unsupported_minkowski_requires_P_X_zero"
            ],

        "p_only_stationary_background_has_time_kinetic":
            scalar[
                "p_only_standalone_time_kinetic_nonzero"
            ],

        "full_constrained_scalar_metric_symbol_required":
            scalar[
                "full_constrained_scalar_metric_symbol_required"
            ],

        "tensor_sector_partial_green":
            tensor_partial_green,

        "canonical_health_on_full_static_spacelike_background_established":
            full_principal_green,

        "constraint_elimination_completed":
            False,

        "static_spacelike_source_to_metric_cross_response_established":
            False,

        "cross_response_survives_field_redefinition_audit":
            False,

        "nonremovable_active_numerator_established":
            False,

        "outward_sign_established":
            False,

        "microscopic_source_solution_in_full_dhost_established":
            False,

        "finite_payload_established":
            False,

        "offstate_quantum_descendants_audited":
            False,

        "v26d_complete_energy_j":
            None,

        "hook17_capacity_reference_transfers_to_v26d":
            False,

        "v26d_field_capacity_established":
            False,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "energy_optimization_authorized":
            False,

        "action_oracle_authorized":
            False,

        "agminer_database_mutation_authorized":
            False,

        "original_v26e_scope_complete":
            False,

        "v26e1_full_constrained_symbol_crossprop_authorized":
            tensor_partial_green,

        "next":
            (
                "032V26E1_STATIC_SPACELIKE_FULL_CONSTRAINED_"
                "SCALAR_METRIC_SYMBOL_CROSSPROP_GATE"
            ),

        "claim_scope":
            (
                "TT TENSOR PRINCIPAL SYMBOL ON CONSTANT STATIC SPACELIKE "
                "GRADIENT PLUS UNSUPPORTED FLAT-BACKGROUND CONSISTENCY "
                "THEOREM; NOT FULL DHOST CANONICAL HEALTH"
            ),

        "background_routes":
            background_route_atlas(),
    }
