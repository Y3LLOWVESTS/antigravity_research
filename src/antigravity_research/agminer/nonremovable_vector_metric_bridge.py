"""032V24D non-removable vector-to-metric bridge preflight.

PURPOSE
-------
Test whether the surviving V24C Dirac hook/torsion-like source can use either
of the two most attractive protected-vector routes as a genuine *linear*
universal physical-metric bridge.

The tested bridge routes are:

1. the universal infrared pair-antisymmetric/torsion-like theories of
   Barker, Marzo and Santoni (2025);

2. the quadratically mixed vector-graviton theory of Marzo (2026).

CENTRAL RESULT TESTED
---------------------
The Marzo quadratic mixed block is a Stückelberg square.

Up to integration by parts,

    M^2 V^2
    + M H div(V)
    - (1/4) H box(H)

becomes

    M^2 [V - dH/(2M)]^2.

The Maxwell kinetic term is invariant under

    V -> V + gradient(scalar),

so defining

    W_a = V_a - d_a H/(2M)

diagonalizes the quadratic action into the Fierz-Pauli graviton and a massive
vector.

For a general linear source

    S_src
      = integral [
            (1/2) H_ab T^ab
            + V_a J^a
        ],

the shared gauge symmetry implies the source Ward identity

    d_a T^ab
      = (1/M) d^b(d_a J^a).

Under the same field redefinition,

    T_tilde^ab
      = T^ab
        - eta^ab (d_a J^a)/M

and the Ward identity guarantees

    d_a T_tilde^ab = 0.

Thus the gauge-compatible source also diagonalizes:

    S_src
      = integral [
            (1/2) H_ab T_tilde^ab
            + W_a J^a
        ].

The vector current does not provide a non-removable linear graviton source.

SCOPE
-----
This closes only the declared linear/quadratic bridge mechanism.

It does NOT close:

- the nonlinear Marzo cubic/quartic interactions;
- a background-dependent mixed phase;
- a different non-removable vector-metric action;
- the Dirac hook/torsion-like microscopic source itself;
- a nonlinear metric response;
- broader metric-affine gravity.

The Barker-Marzo-Santoni universal torsion-like IR theory is separately
classified as lacking a dynamical metric perturbation in its declared
universal IR action. Nonlinear Poincare/MAG completions remain open.

No candidate, rejection, action oracle, mechanism metric, energy result, or
physical antigravity claim is created here.

LITERATURE
----------
Barker, Marzo, Santoni,
"Infrared foundations for quantum geometry II:
 Catalogue of all torsion-like theories including new ghost-tachyon-free
 cases",
arXiv:2507.05349.

Marzo,
"Gravitational mass generation and consistent non-minimal couplings:
 cubics and quartics of a massive vector",
arXiv:2603.24008.

CLAIM_CLASSIFICATION=
PROJECT_DERIVED_FIELD_REDEFINITION_AND_SOURCE_WARD_THEOREM_PREFLIGHT
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .storage import Storage


ETA = np.diag(
    [
        -1.0,
        1.0,
        1.0,
        1.0,
    ]
)


def stueckelberg_square_coefficients(
    mass_scale: float,
) -> dict[str, float]:
    """Return the integrated-by-parts coefficients of the Marzo mixed block.

    Starting from

        M^2 V^2
        + M H div(V)
        - (1/4) H box(H),

    integration by parts gives

        M^2 V^2
        - M V.dH
        + (1/4) (dH)^2.

    This is exactly

        M^2 [V - dH/(2M)]^2.
    """
    mass = float(
        mass_scale
    )

    if not np.isfinite(
        mass
    ) or mass <= 0.0:
        raise ValueError(
            "mass_scale must be positive and finite"
        )

    return {
        "v_squared":
            mass
            *
            mass,

        "v_dot_gradient_h":
            -mass,

        "gradient_h_squared":
            0.25,
    }


def stueckelberg_square_numeric_identity(
    *,
    mass_scale: float,
    v_squared: float,
    v_dot_gradient_h: float,
    gradient_h_squared: float,
) -> dict[str, Any]:
    """Verify the completed-square identity from scalar contractions."""
    mass = float(
        mass_scale
    )

    if not np.isfinite(
        mass
    ) or mass <= 0.0:
        raise ValueError(
            "mass_scale must be positive and finite"
        )

    v2 = float(
        v_squared
    )

    cross = float(
        v_dot_gradient_h
    )

    dh2 = float(
        gradient_h_squared
    )

    if not all(
        np.isfinite(
            value
        )
        for value
        in (
            v2,
            cross,
            dh2,
        )
    ):
        raise ValueError(
            "contractions must be finite"
        )

    original_after_ibp = (
        mass
        *
        mass
        *
        v2
        -
        mass
        *
        cross
        +
        0.25
        *
        dh2
    )

    w_squared = (
        v2
        -
        cross
        /
        mass
        +
        dh2
        /
        (
            4.0
            *
            mass
            *
            mass
        )
    )

    completed_square = (
        mass
        *
        mass
        *
        w_squared
    )

    error = abs(
        original_after_ibp
        -
        completed_square
    )

    relative_error = (
        error
        /
        max(
            abs(
                original_after_ibp
            ),
            abs(
                completed_square
            ),
            1.0,
        )
    )

    return {
        "original_after_integration_by_parts":
            original_after_ibp,

        "completed_square":
            completed_square,

        "absolute_error":
            error,

        "relative_error":
            relative_error,

        "identity_pass":
            relative_error
            <
            1.0e-14,
    }


def maxwell_quadratic_form(
    vector_up: np.ndarray,
    wavevector_cov: np.ndarray,
) -> float:
    """Return a Fourier-space Maxwell quadratic form.

    The overall sign and normalization are irrelevant to the present identity.
    The form

        k^2 V^2 - (k.V)^2

    is invariant under

        V^a -> V^a + alpha k^a.
    """
    vector = np.asarray(
        vector_up,
        dtype=float,
    )

    wavevector = np.asarray(
        wavevector_cov,
        dtype=float,
    )

    if vector.shape != (
        4,
    ):
        raise ValueError(
            "vector_up must contain four components"
        )

    if wavevector.shape != (
        4,
    ):
        raise ValueError(
            "wavevector_cov must contain four components"
        )

    if not np.all(
        np.isfinite(
            vector
        )
    ) or not np.all(
        np.isfinite(
            wavevector
        )
    ):
        raise ValueError(
            "vector and wavevector must be finite"
        )

    wavevector_up = ETA @ wavevector

    k_squared = float(
        wavevector
        @
        wavevector_up
    )

    v_squared = float(
        vector
        @
        ETA
        @
        vector
    )

    k_dot_v = float(
        wavevector
        @
        vector
    )

    return (
        k_squared
        *
        v_squared
        -
        k_dot_v
        *
        k_dot_v
    )


def maxwell_gradient_shift_diagnostic(
    *,
    vector_up: np.ndarray,
    wavevector_cov: np.ndarray,
    shift: float,
) -> dict[str, Any]:
    """Verify Maxwell invariance under a pure-gradient vector shift."""
    vector = np.asarray(
        vector_up,
        dtype=float,
    )

    wavevector = np.asarray(
        wavevector_cov,
        dtype=float,
    )

    alpha = float(
        shift
    )

    if not np.isfinite(
        alpha
    ):
        raise ValueError(
            "shift must be finite"
        )

    wavevector_up = ETA @ wavevector

    shifted = (
        vector
        +
        alpha
        *
        wavevector_up
    )

    before = maxwell_quadratic_form(
        vector,
        wavevector,
    )

    after = maxwell_quadratic_form(
        shifted,
        wavevector,
    )

    error = abs(
        before
        -
        after
    )

    relative_error = (
        error
        /
        max(
            abs(
                before
            ),
            abs(
                after
            ),
            1.0,
        )
    )

    return {
        "before":
            before,

        "after":
            after,

        "relative_error":
            relative_error,

        "gradient_shift_invariant":
            relative_error
            <
            1.0e-12,
    }


def stueckelberg_gauge_invariant_vector_residual(
    *,
    gradient_parameter_cov: np.ndarray,
    mass_scale: float,
) -> dict[str, Any]:
    """Verify W=V-dH/(2M) is invariant under the shared linear symmetry.

    With the convention used in the Marzo action,

        delta H = 2 div(xi)

and therefore

        delta(dH) = 2 d(div xi),

while

        delta V = d(div xi)/M.
    """
    gradient = np.asarray(
        gradient_parameter_cov,
        dtype=float,
    )

    mass = float(
        mass_scale
    )

    if gradient.shape != (
        4,
    ):
        raise ValueError(
            "gradient_parameter_cov must contain four components"
        )

    if not np.all(
        np.isfinite(
            gradient
        )
    ):
        raise ValueError(
            "gradient must be finite"
        )

    if not np.isfinite(
        mass
    ) or mass <= 0.0:
        raise ValueError(
            "mass_scale must be positive and finite"
        )

    delta_v_cov = (
        gradient
        /
        mass
    )

    delta_gradient_h_cov = (
        2.0
        *
        gradient
    )

    delta_w_cov = (
        delta_v_cov
        -
        delta_gradient_h_cov
        /
        (
            2.0
            *
            mass
        )
    )

    return {
        "delta_w_cov":
            delta_w_cov.tolist(),

        "delta_w_norm":
            float(
                np.linalg.norm(
                    delta_w_cov
                )
            ),

        "gauge_invariant":
            bool(
                np.linalg.norm(
                    delta_w_cov
                )
                <
                1.0e-14
            ),
    }


def source_ward_diagonalization(
    *,
    wavevector_cov: np.ndarray,
    vector_current_up: np.ndarray,
    metric_source_upup: np.ndarray,
    mass_scale: float,
) -> dict[str, Any]:
    """Apply the shared-gauge source Ward identity in Fourier space.

    Source convention:

        S_src
          = (1/2) H_ab T^ab
            + V_a J^a.

    The linear gauge transformations imply

        k_a T^ab
          = k^b (k.J)/M.

    The Stückelberg field redefinition changes the metric source to

        T_tilde^ab
          = T^ab
            - eta^ab (k.J)/M.

    Therefore a gauge-compatible source obeys

        k_a T_tilde^ab = 0.
    """
    wavevector = np.asarray(
        wavevector_cov,
        dtype=float,
    )

    current = np.asarray(
        vector_current_up,
        dtype=float,
    )

    source = np.asarray(
        metric_source_upup,
        dtype=float,
    )

    mass = float(
        mass_scale
    )

    if wavevector.shape != (
        4,
    ):
        raise ValueError(
            "wavevector_cov must contain four components"
        )

    if current.shape != (
        4,
    ):
        raise ValueError(
            "vector_current_up must contain four components"
        )

    if source.shape != (
        4,
        4,
    ):
        raise ValueError(
            "metric_source_upup must have shape (4,4)"
        )

    if not np.allclose(
        source,
        source.T,
        atol=1.0e-12,
        rtol=0.0,
    ):
        raise ValueError(
            "metric source must be symmetric"
        )

    if not all(
        np.all(
            np.isfinite(
                item
            )
        )
        for item
        in (
            wavevector,
            current,
            source,
        )
    ):
        raise ValueError(
            "source data must be finite"
        )

    if not np.isfinite(
        mass
    ) or mass <= 0.0:
        raise ValueError(
            "mass_scale must be positive and finite"
        )

    wavevector_up = ETA @ wavevector

    current_divergence = float(
        wavevector
        @
        current
    )

    original_metric_divergence = (
        wavevector
        @
        source
    )

    required_metric_divergence = (
        wavevector_up
        *
        current_divergence
        /
        mass
    )

    ward_residual = (
        original_metric_divergence
        -
        required_metric_divergence
    )

    induced_trace_source = (
        -ETA
        *
        current_divergence
        /
        mass
    )

    transformed_source = (
        source
        +
        induced_trace_source
    )

    transformed_divergence = (
        wavevector
        @
        transformed_source
    )

    source_scale = max(
        float(
            np.linalg.norm(
                source
            )
        ),
        abs(
            current_divergence
            /
            mass
        ),
        1.0,
    )

    ward_pass = bool(
        np.linalg.norm(
            ward_residual
        )
        <
        1.0e-12
        *
        source_scale
    )

    transformed_conserved = bool(
        np.linalg.norm(
            transformed_divergence
        )
        <
        1.0e-12
        *
        source_scale
    )

    return {
        "current_divergence":
            current_divergence,

        "original_metric_divergence":
            original_metric_divergence.tolist(),

        "required_metric_divergence":
            required_metric_divergence.tolist(),

        "ward_residual":
            ward_residual.tolist(),

        "ward_residual_norm":
            float(
                np.linalg.norm(
                    ward_residual
                )
            ),

        "source_ward_identity_pass":
            ward_pass,

        "induced_trace_metric_source":
            induced_trace_source.tolist(),

        "transformed_metric_source":
            transformed_source.tolist(),

        "transformed_metric_source_norm":
            float(
                np.linalg.norm(
                    transformed_source
                )
            ),

        "transformed_metric_divergence":
            transformed_divergence.tolist(),

        "transformed_metric_source_conserved":
            transformed_conserved,

        "vector_source_generates_independent_linear_metric_source":
            False
            if (
                ward_pass
                and
                transformed_conserved
            )
            else
            None,
    }


def pure_vector_ward_compensated_source(
    *,
    wavevector_cov: np.ndarray,
    vector_current_up: np.ndarray,
    mass_scale: float,
) -> dict[str, Any]:
    """Construct the minimal metric compensator required by the Ward identity.

    For arbitrary J, define

        T^ab
          = eta^ab (k.J)/M.

    This satisfies the shared-gauge Ward identity exactly and transforms to

        T_tilde^ab = 0.

    Thus even a nonconserved vector current cannot obtain a free linear metric
    source merely from the Stückelberg mixing.
    """
    wavevector = np.asarray(
        wavevector_cov,
        dtype=float,
    )

    current = np.asarray(
        vector_current_up,
        dtype=float,
    )

    mass = float(
        mass_scale
    )

    if wavevector.shape != (
        4,
    ) or current.shape != (
        4,
    ):
        raise ValueError(
            "wavevector and current must contain four components"
        )

    if not np.isfinite(
        mass
    ) or mass <= 0.0:
        raise ValueError(
            "mass_scale must be positive and finite"
        )

    divergence = float(
        wavevector
        @
        current
    )

    compensator = (
        ETA
        *
        divergence
        /
        mass
    )

    result = source_ward_diagonalization(
        wavevector_cov=
            wavevector,

        vector_current_up=
            current,

        metric_source_upup=
            compensator,

        mass_scale=
            mass,
    )

    result[
        "minimal_ward_compensator"
    ] = compensator.tolist()

    result[
        "compensator_transforms_to_zero_metric_source"
    ] = bool(
        result[
            "transformed_metric_source_norm"
        ]
        <
        1.0e-12
    )

    return result


def independent_conserved_metric_source_demo() -> dict[str, Any]:
    """Show that an independent conserved stress still sources the graviton.

    This protects the claim boundary: V24D removes the *vector-to-metric cross
    source*, not ordinary graviton sourcing by an independent conserved
    stress-energy tensor.
    """
    wavevector = np.array(
        [
            0.0,
            1.0,
            0.0,
            0.0,
        ]
    )

    current = np.array(
        [
            1.0,
            0.0,
            0.4,
            -0.7,
        ]
    )

    source = np.zeros(
        (
            4,
            4,
        )
    )

    source[
        0,
        0,
    ] = 3.0

    source[
        2,
        2,
    ] = 2.0

    source[
        3,
        3,
    ] = 1.0

    result = source_ward_diagonalization(
        wavevector_cov=
            wavevector,

        vector_current_up=
            current,

        metric_source_upup=
            source,

        mass_scale=
            2.0,
    )

    return {
        **result,

        "current_is_conserved":
            abs(
                float(
                    wavevector
                    @
                    current
                )
            )
            <
            1.0e-14,

        "independent_metric_source_nonzero":
            float(
                np.linalg.norm(
                    source
                )
            )
            >
            1.0e-14,

        "transformed_source_equals_original":
            bool(
                np.allclose(
                    np.asarray(
                        result[
                            "transformed_metric_source"
                        ]
                    ),
                    source,
                    atol=1.0e-12,
                    rtol=0.0,
                )
            ),
    }


def marzo_2026_linear_bridge_gate() -> dict[str, Any]:
    """Return the conservative V24D classification of Marzo Eq. 18."""
    square = stueckelberg_square_numeric_identity(
        mass_scale=
            2.7,

        v_squared=
            1.3,

        v_dot_gradient_h=
            -0.4,

        gradient_h_squared=
            0.8,
    )

    maxwell = maxwell_gradient_shift_diagnostic(
        vector_up=
            np.array(
                [
                    0.3,
                    -0.7,
                    0.2,
                    1.1,
                ]
            ),

        wavevector_cov=
            np.array(
                [
                    0.5,
                    0.9,
                    -0.3,
                    0.8,
                ]
            ),

        shift=
            0.37,
    )

    gauge = stueckelberg_gauge_invariant_vector_residual(
        gradient_parameter_cov=
            np.array(
                [
                    0.3,
                    -0.2,
                    0.8,
                    0.1,
                ]
            ),

        mass_scale=
            2.7,
    )

    conserved = source_ward_diagonalization(
        wavevector_cov=
            np.array(
                [
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                ]
            ),

        vector_current_up=
            np.array(
                [
                    1.0,
                    0.0,
                    0.7,
                    -0.4,
                ]
            ),

        metric_source_upup=
            np.zeros(
                (
                    4,
                    4,
                )
            ),

        mass_scale=
            2.7,
    )

    compensated = pure_vector_ward_compensated_source(
        wavevector_cov=
            np.array(
                [
                    0.0,
                    1.0,
                    2.0,
                    -0.5,
                ]
            ),

        vector_current_up=
            np.array(
                [
                    0.4,
                    0.8,
                    -0.2,
                    0.3,
                ]
            ),

        mass_scale=
            2.7,
    )

    return {
        "reference":
            "ARXIV_2603_24008_EQ18",

        "published_description":
            "FIERZ_PAULI_PLUS_MAXWELL_PLUS_STUECKELBERG_COMPLETION",

        "mixed_block_is_exact_stueckelberg_square":
            square[
                "identity_pass"
            ],

        "maxwell_term_gradient_shift_invariant":
            maxwell[
                "gradient_shift_invariant"
            ],

        "redefined_vector_gauge_invariant":
            gauge[
                "gauge_invariant"
            ],

        "conserved_vector_current_ward_pass":
            conserved[
                "source_ward_identity_pass"
            ],

        "conserved_vector_current_transformed_metric_source_zero":
            conserved[
                "transformed_metric_source_norm"
            ]
            <
            1.0e-12,

        "nonconserved_current_minimal_compensator_ward_pass":
            compensated[
                "source_ward_identity_pass"
            ],

        "nonconserved_current_compensator_transforms_to_zero_metric_source":
            compensated[
                "compensator_transforms_to_zero_metric_source"
            ],

        "nonremovable_linear_vector_to_metric_cross_source":
            False,

        "linear_universal_metric_bridge_from_vector_source_established":
            False,

        "quadratic_action_health_closed":
            False,

        "massive_vector_closed":
            False,

        "cubic_quartic_interactions_closed":
            False,

        "background_dependent_mixing_closed":
            False,

        "independent_conserved_metric_source_closed":
            False,

        "full_marzo_model_closed":
            False,

        "direct_dirac_hook_source_match_closed":
            False,
    }


def bms_2025_torsionlike_ir_metric_gate() -> dict[str, Any]:
    """Classify the declared universal torsion-like IR action."""
    return {
        "reference":
            "ARXIV_2507_05349",

        "field":
            "PAIR_ANTISYMMETRIC_RANK_THREE",

        "universal_ir_flat_space_action":
            True,

        "healthy_vector_torsion_modes_exist":
            True,

        "scalar_torsion_modes_promoted":
            False,

        "pseudoscalar_torsion_modes_promoted":
            False,

        "metric_perturbation_present_as_dynamical_field":
            False,

        "published_statement_true_gravity_plays_no_role_in_universal_ir_action":
            True,

        "direct_universal_physical_metric_bridge_in_declared_ir_action":
            False,

        "nonlinear_poincare_completion_closed":
            False,

        "nonlinear_metric_affine_completion_closed":
            False,

        "background_dependent_metric_torsion_mixing_closed":
            False,

        "dirac_hook_source_closed":
            False,

        "full_torsionlike_theory_space_closed":
            False,
    }


def v24d_frontier_rerank() -> list[dict[str, Any]]:
    """Return the post-V24D search ordering."""
    marzo = marzo_2026_linear_bridge_gate()
    bms = bms_2025_torsionlike_ir_metric_gate()

    return [
        {
            "priority":
                0,

            "branch":
                "MARZO_2026_LINEAR_VECTOR_GRAVITON_CROSS_PORTAL",

            "status":
                "CLOSED_AS_NONREMOVABLE_LINEAR_SOURCE_TO_METRIC_BRIDGE",

            "reason":
                (
                    "STUECKELBERG_FIELD_REDEFINITION_PLUS_"
                    "SHARED_GAUGE_SOURCE_WARD_IDENTITY_DIAGONALIZES_"
                    "VECTOR_AND_CONSERVED_METRIC_SOURCES"
                ),

            "nonremovable_cross_source":
                marzo[
                    "nonremovable_linear_vector_to_metric_cross_source"
                ],

            "nonlinear_completion_closed":
                False,
        },
        {
            "priority":
                0,

            "branch":
                "BMS_2025_UNIVERSAL_IR_TORSIONLIKE_VECTOR_AS_METRIC_BRIDGE",

            "status":
                "CLOSED_WITHIN_DECLARED_UNIVERSAL_IR_ACTION",

            "reason":
                "METRIC_PERTURBATION_PLAYS_NO_DYNAMICAL_ROLE_IN_DECLARED_IR_ACTION",

            "healthy_vector_exists":
                bms[
                    "healthy_vector_torsion_modes_exist"
                ],

            "nonlinear_completion_closed":
                False,
        },
        {
            "priority":
                1,

            "branch":
                "NONREMOVABLE_INTRINSIC_SOURCE_TO_UNIVERSAL_METRIC_CROSS_PROPAGATOR",

            "status":
                "HIGHEST_PRIORITY_GLOBAL_AGMINER_TARGET",

            "reason":
                (
                    "V24_SHOWS_SOURCE_EXISTENCE_AND_MEDIATOR_HEALTH_ARE_"
                    "INSUFFICIENT_IF_CROSS_PROPAGATOR_IS_FIELD_REDEFINITION_"
                    "REMOVABLE_OR_METRIC_IS_ABSENT"
                ),

            "tier0_requirements": [
                "INTRINSIC_SOURCE_CHARGE_NOT_FIXED_BY_ORDINARY_STRESS_ENERGY",
                "HEALTHY_CANONICALLY_NORMALIZED_MEDIATOR",
                "NONREMOVABLE_SOURCE_TO_PHYSICAL_METRIC_CROSS_PROPAGATOR",
                "SOURCE_WARD_IDENTITY_COMPATIBLE",
                "STATIC_OR_QUASISTATIC_FINITE_PAYLOAD_RESPONSE",
                "UNIVERSAL_NEUTRAL_MATTER_PHYSICAL_METRIC",
                "EMPIRICAL_OFFSTATE_CONTROL",
                "COMPLETE_OPERATING_ENERGY_LT_10MJ",
            ],
        },
        {
            "priority":
                2,

            "branch":
                "MARZO_2026_NONLINEAR_VECTOR_GRAVITON_COMPLETION_WITH_DIRAC_HOOK",

            "status":
                "OPEN_BUT_LINEAR_BRIDGE_ADVANTAGE_REMOVED",

            "reason":
                (
                    "CUBIC_QUARTIC_INTERACTIONS_ARE_NONTRIVIAL_BUT_"
                    "DIRAC_SOURCE_MATCH_AND_NONLINEAR_METRIC_RESPONSE_"
                    "PER_JOULE_NOT_ESTABLISHED"
                ),

            "linear_cross_portal_closed":
                True,

            "nonlinear_response_closed":
                False,
        },
        {
            "priority":
                2,

            "branch":
                "BACKGROUND_DEPENDENT_PROTECTED_HOOK_VECTOR_METRIC_MIXING",

            "status":
                "OPEN_HIGH_EMPIRICAL_RISK",

            "reason":
                (
                    "NONZERO_BACKGROUND_CAN_CREATE_PHYSICAL_MIXING_BUT_"
                    "BACKGROUND_ENERGY_OFFSTATE_COSMOLOGY_AND_EMPIRICAL_"
                    "COSTS_MUST_BE_INCLUDED"
                ),

            "background_energy_included":
                False,

            "empirical_consistency_established":
                False,
        },
        {
            "priority":
                3,

            "branch":
                "DIRAC_HOOK_TORSIONLIKE_SOURCE",

            "status":
                "PRESERVED_AS_SOURCE_KNOWLEDGE_NOT_ACTIVE_MODEL",

            "reason":
                (
                    "V24C_EXACT_SOURCE_REPRESENTATION_SURVIVES_BUT_"
                    "TESTED_PROTECTED_VECTOR_BRIDGES_DO_NOT_COMPLETE_"
                    "SOURCE_TO_UNIVERSAL_METRIC_CHAIN"
                ),

            "source_closed":
                False,

            "healthy_vector_source_match_established":
                False,

            "universal_metric_bridge_established":
                False,
        },
    ]


def _insert_rule_once(
    storage: Storage,
    *,
    family: str,
    family_version: str,
    rule_type: str,
    rule: dict[str, Any],
    proof_reference: str,
) -> int:
    """Insert one region rule idempotently."""
    existing = storage.connection.execute(
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

    if (
        existing is not None
        and
        int(
            existing[
                "count"
            ]
        )
        >
        0
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


def persist_v24d_region_rules(
    storage: Storage,
) -> int:
    """Persist the two narrow policy-independent V24D closures."""
    inserted = _insert_rule_once(
        storage,
        family=
            "032_VECTOR_GRAVITON_QUADRATIC_MIXING",

        family_version=
            "MARZO_2026_V24D",

        rule_type=
            "STUECKELBERG_REMOVABLE_LINEAR_VECTOR_METRIC_BRIDGE",

        rule={
            "policy_specific":
                False,

            "scope":
                (
                    "MARZO_2026_EQ18_QUADRATIC_ACTION_WITH_LINEAR_"
                    "GAUGE_COMPATIBLE_EXTERNAL_SOURCES"
                ),

            "closed":
                True,

            "mixed_block_exact_stueckelberg_square":
                True,

            "maxwell_gradient_shift_invariant":
                True,

            "source_ward_identity_diagonalizes_sources":
                True,

            "nonremovable_linear_vector_to_metric_cross_source":
                False,

            "conserved_vector_current_linear_metric_source":
                False,

            "nonconserved_current_without_compensator_allowed":
                False,

            "cubic_quartic_interactions_closed":
                False,

            "background_dependent_mixing_closed":
                False,

            "independent_metric_stress_source_closed":
                False,

            "full_marzo_model_closed":
                False,
        },

        proof_reference=
            "032V24D_MARZO_STUECKELBERG_SOURCE_WARD_DIAGONALIZATION",
    )

    inserted += _insert_rule_once(
        storage,
        family=
            "032_PROTECTED_TORSIONLIKE_VECTOR",

        family_version=
            "BMS_2025_V24D",

        rule_type=
            "UNIVERSAL_IR_ACTION_HAS_NO_DYNAMICAL_METRIC_BRIDGE",

        rule={
            "policy_specific":
                False,

            "scope":
                "BARKER_MARZO_SANTONI_2025_UNIVERSAL_FLAT_IR_PAIR_ANTISYMMETRIC_ACTION",

            "closed":
                True,

            "healthy_vector_modes_exist":
                True,

            "metric_perturbation_dynamical_in_declared_ir_action":
                False,

            "direct_universal_physical_metric_bridge":
                False,

            "nonlinear_poincare_completion_closed":
                False,

            "nonlinear_metric_affine_completion_closed":
                False,

            "background_mixing_closed":
                False,

            "dirac_hook_source_closed":
                False,

            "full_torsionlike_theory_space_closed":
                False,
        },

        proof_reference=
            "032V24D_BMS_TORSIONLIKE_UNIVERSAL_IR_METRIC_ABSENCE_GATE",
    )

    return inserted
