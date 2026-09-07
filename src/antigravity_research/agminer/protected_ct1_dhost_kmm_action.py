"""032V26D protected cT=1 DHOST/KMM explicit-action preflight.

PURPOSE
-------
Construct one explicit scalar-tensor action scaffold that satisfies the
structural requirements inherited from V19R5/R6, V21/V22, V24D, V25F,
and V26A-C:

    ONE UNIVERSAL PHYSICAL METRIC

    DEGENERATE SCALAR-TENSOR STRUCTURE

    c_T = 1 COMPATIBLE SUBCLASS

    NO-GRAVITON-DECAY SUBCLASS

    FRAME-INDEPENDENT KINETIC MATTER MIXING

    ACTIVE-STATE-DEPENDENT MIXING

    OFF-STATE TREE-LEVEL SUPPRESSION

    NO PRINCIPAL-EIGENVALUE TUNING AS THE DECLARED GAIN MECHANISM

This is an ACTION-LEVEL PREFLIGHT.

It is deliberately earlier than:

    static spacelike principal-symbol analysis,
    constrained source->metric Green function,
    finite payload,
    or energy optimization.

---------------------------------------------------------------------------
DECLARED X CONVENTION
---------------------------------------------------------------------------

This module uses

    X = g^{mu nu} nabla_mu phi nabla_nu phi.

With this convention consider the quadratic-DHOST action

    S =
    integral d4x sqrt(-g)
    [
        P(X)
        +
        Q(X) Box phi
        +
        F(X) R

        +
        A3(X)
        phi^mu phi^nu phi_munu Box phi

        +
        A4(X)
        phi^mu phi_{mu rho}
        phi^{rho nu} phi_nu

        +
        A5(X)
        (
            phi^mu phi^nu phi_munu
        )^2

        +
        L_hidden
    ]

    +
    S_SM[g, chi].

For the c_T=1 quadratic-DHOST class with

    A1 = A2 = 0,

the degeneracy relations in this convention are

    A4
    =
    [
        48 F_X^2
        -
        8 (F - X F_X) A3
        -
        X^2 A3^2
    ]
    /
    (8 F),

and

    A5
    =
    (
        4 F_X + X A3
    )
    A3
    /
    (2 F).

The special no-graviton-decay branch is

    A3 = 0,

so

    A4 = 6 F_X^2 / F,

    A5 = 0.

The numerical prefactor depends on the convention used for X. The present
module never mixes conventions.

---------------------------------------------------------------------------
COSMOLOGICAL EFT IDENTITY
---------------------------------------------------------------------------

For the same convention, the relevant published EFT combinations can be
written schematically as

    alpha_H
        =
    -2 X F_X / F,

and

    beta_1
        =
    X (F_X + X A3) / F.

Therefore for

    A3 = 0,

one obtains the exact algebraic identity

    alpha_H + 2 beta_1 = 0.

This is the known no-graviton-decay relation.

Crucially,

    beta_1

does NOT have to vanish.

Thus there exists a structural corridor in which:

    non-Horndeski / DHOST kinetic mixing != 0

while

    dangerous cosmological graviton-decay combination = 0.

This is qualitatively different from simply setting all modified-gravity
coefficients to zero.

IMPORTANT:

These alpha_H / beta_1 relations are cosmological-EFT diagnostics.

They do NOT by themselves prove that tensor characteristics remain luminal
on the strongly anisotropic static spacelike background required by a
laboratory source.

That must be derived in V26E.

---------------------------------------------------------------------------
MATTER FRAME
---------------------------------------------------------------------------

Ordinary neutral matter is minimally and universally coupled to

    g_mu_nu.

There is no second physical metric in the declared matter frame.

Published Kinetic Matter Mixing is frame-independent: in a gravity-demixed
frame it can be represented through disformal matter interactions, while in
the matter-minimal frame it lives in the beyond-Horndeski / DHOST kinetic
structure.

Therefore a field redefinition that moves the interaction between sectors
does not by itself prove that the physical KMM vanishes.

This is exactly why the future source->metric response must be reconstructed
from an invariant observable after constraints are eliminated.

---------------------------------------------------------------------------
HIDDEN MICROSCOPIC SOURCE SCAFFOLD
---------------------------------------------------------------------------

The same action may contain the previously studied hidden fermion sector

    L_hidden
        =
    bar(Psi)
    (
        i gamma^mu D_mu - m_Psi
    )
    Psi

    +
    (1/f_Psi)
    nabla_mu phi
    bar(Psi) gamma^mu gamma_5 Psi

    +
    L_confinement/support
    + ...

This supplies an explicit derivative axial source vertex.

V15/V16 established that this type of microscopic source vertex can produce
the required derivative-current source structure in the earlier effective
model.

However:

    THE FULL V15/V16 SOURCE SOLUTION
    HAS NOT YET BEEN RESOLVED
    INSIDE THIS DHOST ACTION.

Therefore this run records:

    SAME_ACTION_SOURCE_VERTEX = EXPLICIT

but:

    SAME_ACTION_MICROSCOPIC_FIELD_SOLUTION = NOT_ESTABLISHED.

---------------------------------------------------------------------------
ACTIVE / OFF-STATE STRUCTURE
---------------------------------------------------------------------------

Take

    F(X)
        =
    F0
    [
        1
        +
        eta X / Lambda^4
    ]

as the simplest dimensionless local scaffold.

Define

    x = X / Lambda^4.

Then

    X F_X / F
        =
    eta x / (1 + eta x).

Consequently:

    beta_1
        =
    eta x / (1 + eta x),

and

    alpha_H
        =
    -2 beta_1.

OFF STATE:

    nabla phi = 0
    =>
    X = 0
    =>
    alpha_H = beta_1 = 0.

The derivative hidden-current vertex is also inactive when nabla phi=0.

The A4 operator contains explicit scalar derivatives and therefore vanishes
on the constant-phi off state even though F_X itself need not vanish.

Assuming

    P(0)=0,

and that Q contributes no off-state tadpole,

the classical off state reduces to Einstein-Hilbert gravity plus ordinary
minimally coupled matter and the dormant hidden sector.

ACTIVE STATE:

    X != 0
    and
    F_X != 0

gives

    beta_1 != 0.

This is a genuine active-background mixing witness.

It is NOT yet the physical source->metric transfer function.

---------------------------------------------------------------------------
WHY THIS DOES NOT REOPEN V21
---------------------------------------------------------------------------

V21's exact integrability theorem concerned an exactly stationary
time-linear field

    partial_t phi = q(x).

Stationarity forced

    grad q = 0,

so a finite smooth localized stationary q reservoir was impossible.

The V26D target instead begins with a static spacelike background:

    partial_t phi = 0,

    grad phi != 0.

Hence the V21 q-integrability theorem does not forbid the selected
background.

This does not prove the static DHOST source exists.

It only establishes that V26D is not the already-closed V21 ansatz.

---------------------------------------------------------------------------
WHY THIS DOES NOT REOPEN V22
---------------------------------------------------------------------------

V22 studied an explicit nonlinear disformal physical metric and found that
an unprotected single-scale implementation naturally generated a dangerous
lower-dimensional off-state disformal operator.

The V26D matter frame instead declares

    g_phys = g,

with ordinary matter minimally coupled to that single metric.

The useful KMM is carried by the degenerate gravitational kinetic structure.

Therefore V22's exact single-scale coefficient mapping is not simply copied
into V26D.

But this is NOT permission to ignore the V22 lesson.

V26E and later gates must still calculate:

    loops,
    radiative descendants,
    off-state material forces,
    UV matching,
    and naturalness.

---------------------------------------------------------------------------
WHAT IS ACTUALLY ESTABLISHED HERE
---------------------------------------------------------------------------

If the algebraic tests pass, V26D establishes only:

    1. one explicit same-action Lagrangian scaffold;

    2. one universal matter metric;

    3. an exact quadratic-DHOST degeneracy relation;

    4. the A3=0 no-decay identity;

    5. a nonzero active KMM witness;

    6. exact classical KMM suppression at X=0;

    7. a source vertex that can be placed in the same action;

    8. separation from the already-closed V21/V22 ansatzes.

It does NOT establish:

    physical antigravity,
    outward sign,
    nonremovable source->metric response,
    canonical health on the static spacelike background,
    anisotropic c_T=1,
    microscopic source solution,
    EFT cutoff control,
    naturalness,
    empirical viability,
    finite payload,
    support,
    stability,
    or sub-10-MJ operation.

---------------------------------------------------------------------------
NEXT GATE
---------------------------------------------------------------------------

If V26D passes:

    032V26E

must build the static-spacelike constrained quadratic operator and determine:

    PRINCIPAL SYMBOL

    KINETIC EIGENVALUES

    CONSTRAINT ELIMINATION

    WARD / DIFFEOMORPHISM PROJECTION

    STATIC HIDDEN-SOURCE -> PHYSICAL-METRIC CROSS GREEN FUNCTION

    FIELD-REDEFINITION INVARIANCE

    ACTIVE NUMERATOR MAGNITUDE

    WHETHER LARGE RESPONSE REQUIRES A SMALL PRINCIPAL EIGENVALUE.

Only after those pass should energy optimization resume.

CLAIM_CLASSIFICATION=
EXPLICIT_ACTION_SCAFFOLD_AND_ACTIVE_OFFSTATE_EFT_IDENTITY_GATE
"""

from __future__ import annotations

import math
from typing import Any


def _finite(
    value: float,
    name: str,
) -> float:
    """Return a finite float."""
    result = float(
        value
    )

    if not math.isfinite(
        result
    ):
        raise ValueError(
            f"{name} must be finite"
        )

    return result


def dhost_degeneracy_coefficients(
    *,
    F: float,
    F_X: float,
    X: float,
    A3: float = 0.0,
) -> dict[str, float]:
    """Return cT=1 quadratic-DHOST A4/A5 in the declared X convention."""
    f = _finite(
        F,
        "F",
    )

    f_x = _finite(
        F_X,
        "F_X",
    )

    x = _finite(
        X,
        "X",
    )

    a3 = _finite(
        A3,
        "A3",
    )

    if f <= 0.0:
        raise ValueError(
            "F must be positive"
        )

    a4 = (
        48.0
        *
        f_x**2
        -
        8.0
        *
        (
            f
            -
            x
            *
            f_x
        )
        *
        a3
        -
        x**2
        *
        a3**2
    ) / (
        8.0
        *
        f
    )

    a5 = (
        (
            4.0
            *
            f_x
            +
            x
            *
            a3
        )
        *
        a3
    ) / (
        2.0
        *
        f
    )

    return {
        "A3":
            a3,

        "A4":
            a4,

        "A5":
            a5,
    }


def cosmological_eft_parameters(
    *,
    F: float,
    F_X: float,
    X: float,
    A3: float = 0.0,
) -> dict[str, float]:
    """Return alpha_H, beta_1 and the no-decay combination.

    These are literature-normalized cosmological-EFT identities in the
    declared X convention.

    They are NOT a static-anisotropic principal-symbol calculation.
    """
    f = _finite(
        F,
        "F",
    )

    f_x = _finite(
        F_X,
        "F_X",
    )

    x = _finite(
        X,
        "X",
    )

    a3 = _finite(
        A3,
        "A3",
    )

    if f <= 0.0:
        raise ValueError(
            "F must be positive"
        )

    alpha_h = (
        -2.0
        *
        x
        *
        f_x
        /
        f
    )

    beta_1 = (
        x
        *
        (
            f_x
            +
            x
            *
            a3
        )
        /
        f
    )

    no_decay = (
        alpha_h
        +
        2.0
        *
        beta_1
    )

    return {
        "alpha_H":
            alpha_h,

        "beta_1":
            beta_1,

        "alpha_H_plus_2_beta_1":
            no_decay,
    }


def normalized_linear_f_model(
    *,
    x: float,
    eta: float,
) -> dict[str, float]:
    """Return dimensionless F/F0 = 1 + eta*x identity diagnostics.

    Here

        x = X / Lambda^4.

    This function is for algebraic mechanism checks, not physical parameter
    optimization.
    """
    x_value = _finite(
        x,
        "x",
    )

    eta_value = _finite(
        eta,
        "eta",
    )

    f_ratio = (
        1.0
        +
        eta_value
        *
        x_value
    )

    if f_ratio <= 0.0:
        raise ValueError(
            "normalized F must remain positive"
        )

    # In normalized variables:
    #
    #     F/F0 = 1 + eta*x
    #
    # and the dimensionless logarithmic derivative is represented by
    # eta in the algebraic scout.
    eft = (
        cosmological_eft_parameters(
            F=
                f_ratio,

            F_X=
                eta_value,

            X=
                x_value,

            A3=
                0.0,
        )
    )

    degeneracy = (
        dhost_degeneracy_coefficients(
            F=
                f_ratio,

            F_X=
                eta_value,

            X=
                x_value,

            A3=
                0.0,
        )
    )

    return {
        "x":
            x_value,

        "eta":
            eta_value,

        "F_over_F0":
            f_ratio,

        "scaled_A4":
            degeneracy[
                "A4"
            ],

        "A5":
            degeneracy[
                "A5"
            ],

        "alpha_H":
            eft[
                "alpha_H"
            ],

        "beta_1":
            eft[
                "beta_1"
            ],

        "alpha_H_plus_2_beta_1":
            eft[
                "alpha_H_plus_2_beta_1"
            ],
    }


def action_specification() -> dict[str, Any]:
    """Return the explicit V26D same-action scaffold."""
    return {
        "phase":
            "032V26D",

        "scalar_kinetic_convention":
            (
                "X=g^{mu nu} nabla_mu(phi) nabla_nu(phi)"
            ),

        "physical_metric":
            "g_mu_nu",

        "ordinary_matter_minimal_to_physical_metric":
            True,

        "ordinary_matter_special_charge_required":
            False,

        "second_physical_metric_required":
            False,

        "A1":
            0.0,

        "A2":
            0.0,

        "A3":
            0.0,

        "A4_relation":
            "A4=6*F_X^2/F in declared X convention",

        "A5":
            0.0,

        "hidden_source_sector":
            (
                "Dirac hidden fermion plus derivative axial-current "
                "coupling"
            ),

        "hidden_source_coupling":
            (
                "(1/fPsi) nabla_mu(phi) "
                "bar(Psi) gamma^mu gamma5 Psi"
            ),

        "same_action_source_vertex_explicit":
            True,

        "same_action_microscopic_source_solution_established":
            False,

        "published_frame_independent_kmm_mechanism":
            True,

        "published_cosmological_ct1_subclass":
            True,

        "published_no_graviton_decay_A3_zero_subclass":
            True,

        "generic_static_spacelike_characteristics_established":
            False,

        "static_spacelike_source_metric_crosspropagator_established":
            False,
    }


def offstate_gate() -> dict[str, Any]:
    """Return exact classical X=0 active/off-state diagnostics."""
    eft = (
        cosmological_eft_parameters(
            F=
                1.0,

            # F_X may be nonzero.
            #
            # The crucial point is that the EFT mixing parameters contain X.
            F_X=
                0.5,

            X=
                0.0,

            A3=
                0.0,
        )
    )

    return {
        "X":
            0.0,

        "constant_phi":
            True,

        "alpha_H":
            eft[
                "alpha_H"
            ],

        "beta_1":
            eft[
                "beta_1"
            ],

        "alpha_H_plus_2_beta_1":
            eft[
                "alpha_H_plus_2_beta_1"
            ],

        "classical_kmm_zero":
            bool(
                eft[
                    "alpha_H"
                ]
                ==
                0.0
                and
                eft[
                    "beta_1"
                ]
                ==
                0.0
            ),

        "explicit_disformal_matter_metric":
            False,

        "derivative_hidden_source_vertex_active":
            False,

        "higher_derivative_A4_operator_active_on_constant_phi":
            False,

        "eh_plus_minimal_matter_limit_if_P0_Q0_vacuum_conditions_hold":
            True,

        "tree_level_active_state_kmm_operator_present":
            False,

        "offstate_quantum_material_descendants_audited":
            False,

        "offstate_radiative_matching_audited":
            False,
    }


def active_background_gate(
    *,
    x: float = 0.10,
    eta: float = 0.50,
) -> dict[str, Any]:
    """Return representative active-background mechanism diagnostics."""
    model = (
        normalized_linear_f_model(
            x=
                x,

            eta=
                eta,
        )
    )

    active_kmm = bool(
        abs(
            model[
                "beta_1"
            ]
        )
        >
        1.0e-15
    )

    no_decay_identity = bool(
        abs(
            model[
                "alpha_H_plus_2_beta_1"
            ]
        )
        <
        1.0e-14
    )

    return {
        **model,

        "background_type":
            "STATIC_SPACELIKE",

        "partial_t_phi":
            0.0,

        "spatial_gradient_nonzero":
            bool(
                abs(
                    x
                )
                >
                0.0
            ),

        "active_kmm_parameter_nonzero":
            active_kmm,

        "cosmological_no_decay_identity_pass":
            no_decay_identity,

        "this_is_physical_source_metric_green_function":
            False,

        "source_to_metric_green_function_derived":
            False,

        "outward_sign_established":
            False,

        "canonical_principal_margin_established":
            False,

        "anisotropic_tensor_characteristics_established":
            False,

        "large_response_from_principal_margin_collapse_assumed":
            False,
    }


def inherited_failure_separation() -> dict[str, Any]:
    """Return why V26D is not a relabeling of V21/V22."""
    return {
        "v21_stationary_time_gradient_q_reopened":
            False,

        "v21_integrability_obstruction_directly_forbids_selected_background":
            False,

        "reason_v21":
            (
                "V26D selects partial_t(phi)=0 with a static spacelike "
                "gradient; V21's theorem targeted spatially varying "
                "stationary partial_t(phi)=q(x)"
            ),

        "v22_explicit_disformal_physical_metric_reopened":
            False,

        "v22_unprotected_single_scale_naturalness_bound_directly_reused":
            False,

        "reason_v22":
            (
                "ordinary matter is minimal to g_mu_nu and the KMM "
                "originates in the degenerate gravitational kinetic "
                "structure, not the V22 explicit physical disformal metric"
            ),

        "v22_offstate_lesson_still_applies":
            True,

        "offstate_loop_audit_still_required":
            True,

        "radiative_naturalness_audit_still_required":
            True,
    }


def identity_scan(
    *,
    x_values: tuple[float, ...] = (
        0.0,
        1.0e-6,
        1.0e-3,
        1.0e-2,
        0.10,
        0.50,
    ),
    eta_values: tuple[float, ...] = (
        0.05,
        0.20,
        1.00,
    ),
) -> list[dict[str, Any]]:
    """Return a small theorem/identity scan, not an optimization."""
    rows: list[
        dict[str, Any]
    ] = []

    for eta in eta_values:
        for x in x_values:
            model = (
                normalized_linear_f_model(
                    x=
                        x,

                    eta=
                        eta,
                )
            )

            rows.append(
                {
                    **model,

                    "no_decay_identity_pass":
                        bool(
                            abs(
                                model[
                                    "alpha_H_plus_2_beta_1"
                                ]
                            )
                            <
                            1.0e-14
                        ),

                    "offstate":
                        bool(
                            x
                            ==
                            0.0
                        ),

                    "active_kmm":
                        bool(
                            x
                            !=
                            0.0
                            and
                            abs(
                                model[
                                    "beta_1"
                                ]
                            )
                            >
                            1.0e-15
                        ),

                    "principal_eigenvalue_tuned":
                        False,

                    "energy_point":
                        False,
                }
            )

    return rows


def v26d_gate() -> dict[str, Any]:
    """Return the conservative V26D promotion state."""
    action = (
        action_specification()
    )

    offstate = (
        offstate_gate()
    )

    active = (
        active_background_gate()
    )

    separation = (
        inherited_failure_separation()
    )

    scan = (
        identity_scan()
    )

    all_no_decay = bool(
        all(
            row[
                "no_decay_identity_pass"
            ]
            for row
            in scan
        )
    )

    all_active_nonzero = bool(
        all(
            row[
                "active_kmm"
            ]
            for row
            in scan
            if not row[
                "offstate"
            ]
        )
    )

    return {
        "phase":
            "032V26D",

        "claim_classification":
            (
                "EXPLICIT_ACTION_SCAFFOLD_AND_"
                "ACTIVE_OFFSTATE_EFT_IDENTITY_GATE"
            ),

        "explicit_same_action_scaffold":
            True,

        "one_universal_physical_metric":
            action[
                "ordinary_matter_minimal_to_physical_metric"
            ],

        "second_physical_metric_required":
            action[
                "second_physical_metric_required"
            ],

        "ordinary_matter_special_charge_required":
            action[
                "ordinary_matter_special_charge_required"
            ],

        "dhost_degeneracy_relation_explicit":
            True,

        "a3_zero_no_decay_identity":
            all_no_decay,

        "published_frame_independent_kmm_structure":
            action[
                "published_frame_independent_kmm_mechanism"
            ],

        "offstate_classical_kmm_zero":
            offstate[
                "classical_kmm_zero"
            ],

        "active_kmm_witness_nonzero":
            all_active_nonzero,

        "active_offstate_separation_at_eft_identity_level":
            bool(
                offstate[
                    "classical_kmm_zero"
                ]
                and
                all_active_nonzero
            ),

        "v21_closed_route_reopened":
            separation[
                "v21_stationary_time_gradient_q_reopened"
            ],

        "v22_closed_route_reopened":
            separation[
                "v22_explicit_disformal_physical_metric_reopened"
            ],

        "microscopic_source_vertex_explicit":
            action[
                "same_action_source_vertex_explicit"
            ],

        "microscopic_source_solution_in_full_dhost_action_established":
            action[
                "same_action_microscopic_source_solution_established"
            ],

        "static_spacelike_source_to_metric_cross_response_established":
            False,

        "cross_response_survives_field_redefinition_audit":
            False,

        "constraint_elimination_completed":
            False,

        "canonical_health_on_static_spacelike_background_established":
            False,

        "anisotropic_tensor_cone_ct1_established":
            False,

        "offstate_quantum_descendants_audited":
            False,

        "naturalness_uv_protection_established":
            False,

        "source_scale_below_cutoff_established":
            False,

        "outward_sign_established":
            False,

        "true_exterior_sidedness_established":
            False,

        "finite_payload_established":
            False,

        "complete_operating_energy_established":
            False,

        "action_oracle_authorized":
            False,

        "energy_optimization_authorized":
            False,

        "agminer_database_mutation_authorized":
            False,

        "v26e_principal_symbol_crossprop_gate_authorized":
            True,

        "next":
            (
                "032V26E_STATIC_SPACELIKE_PRINCIPAL_SYMBOL_"
                "CROSSPROP_AND_NUMERATOR_BOUND"
            ),
    }
