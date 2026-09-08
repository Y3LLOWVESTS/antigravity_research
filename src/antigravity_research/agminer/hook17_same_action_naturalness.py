"""032H17A3 — HOOK17 same-action scaffold, field-redefinition, and protection gate.

PURPOSE
-------
Test the strongest surviving HOOK17 path after 032H17A2.

032H17A2 established that the actual V24 intrinsic Dirac hook source has
nonzero exact canonical source overlap with the healthy hook-symmetric
nonmetricity 2+ and 1+ poles.

That result does not yet constitute one physical theory.

This module asks whether the following ingredients can at least coexist in a
single tree-level action scaffold without immediately destroying the
properties that made HOOK17 interesting:

    Einstein gravity

    +

    healthy hook-symmetric nonmetricity kinetic/mass sector

    +

    intrinsic Dirac hypermomentum source

    +

    one universal quadratic physical metric

    +

    neutral payload coupling to that same physical metric.

It then attacks the scaffold on the next blocking invariants:

1. exact healthy-branch coefficient relations;
2. off-state versus active-state physical-metric response;
3. matter-induced source feedback from the universal metric;
4. field-redefinition invariance of the physical response;
5. codimension of the healthy single-mode surface;
6. generic RG tangency;
7. existence or absence of an actual protecting symmetry;
8. same-action / Noether claim discipline.

SCIENTIFIC CONTEXT
------------------
The healthy single-state hook 2+ and 1+ models of Mikura and Percacci are
quadratic free theories in symmetric metric-affine gravity.

The declared simple-model assumptions include:

    only one massive nonmetricity state in addition to the graviton;

    no gauge symmetry beyond diffeomorphisms;

    no higher-derivative metric propagation.

Their matter interactions are not included in the propagator analysis.

The Wheeler Dirac result supplies explicit affine-connection hypermomentum
source provenance, but it is not by itself the Mikura/Percacci healthy kinetic
theory.

Therefore this module deliberately distinguishes:

    TREE_LEVEL_ACTION_SCAFFOLD

from:

    SAME_ACTION_PROVENANCE_COMPLETE.

NATURALNESS LOGIC
-----------------
A healthy branch defined by several exact relations is not automatically
radiatively stable.

For each surviving hook branch this module constructs the constraint surface
in a ten-dimensional coupling space:

    m1
    m3
    b1
    b3
    b6
    b7
    b10
    b14
    bRQ4
    bRQ6.

The Jacobian rank of the branch constraints gives the local codimension.

A deterministic generic beta-vector witness is then contracted with the
constraint Jacobian.

A nonzero normal component proves only:

    GENERIC RG FLOW IS NOT AUTOMATICALLY TANGENT.

It does NOT calculate the actual beta functions.

It therefore does not prove a universal quantum no-go.

The correct conclusion is instead:

    TECHNICAL NATURALNESS / PROTECTION NOT ESTABLISHED.

This is sufficient to block promotion under the project's theorem-first
rules until a symmetry-protected completion is supplied.

FIELD-REDEFINITION TEST
-----------------------
Around an active hook background the universal metric is schematically

    g_phys = g + lambda B(Q,Q).

Its first variation contains

    delta g_phys = delta g + c delta Q.

An invertible change of variables can move c from the explicit matter portal
into the kinetic/source matrix.

The observable response

    J^T K^{-1} M

must remain invariant.

This module verifies that identity using the actual active V26B1 portal slope.

This is a local linearized active-background field-redefinition theorem.

It is NOT a full nonlinear equivalence proof.

SOURCE FEEDBACK
---------------
When all matter couples to the same physical metric,

    delta S_m / delta Q

contains both intrinsic affine hypermomentum and a metric-feedback term

    ~ T^{mu nu} delta g_phys_munu / delta Q.

Because the HOOK17 portal is quadratic in Q, this additional term vanishes
at Q=0 but is generically nonzero on an active background.

This is preserved explicitly so later runs do not reuse the off-state V24
source unchanged inside the active device.

CLAIM LIMITS
------------
Passing this module does NOT establish:

- a complete interacting metric-affine theory;
- the full combined Dirac variation in the restricted hook theory;
- complete diffeomorphism Noether identities with all matter terms;
- quantum or RG stability;
- a protected 2+ or 1+ completion;
- a finite-payload outward field;
- source energy;
- complete operating energy;
- a sub-10-MJ model;
- a practical antigravity device.

No AGMINER database mutation is performed.
No energy optimization is performed.

CLAIM_CLASSIFICATION=
TREE_LEVEL_SAME_ACTION_COMPATIBILITY_AND_PROTECTION_STOP_RULE
"""

from __future__ import annotations

from typing import Any, Callable

import numpy as np

from .hook17_healthy_mag_projector import (
    h17a2_summary,
    timelike_rest_pole_projector_gate,
)
from .nonlinear_hook_metric_bridge import (
    quadratic_active_background_derivative,
    quadratic_metric_descendant,
    rest_pair_hook,
)


TOL = 1.0e-10
HOOK17_REFERENCE_CAPACITY_RP1E12_J = 17.0676442196
STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7

PARAMETER_NAMES = (
    "m1",
    "m3",
    "b1",
    "b3",
    "b6",
    "b7",
    "b10",
    "b14",
    "bRQ4",
    "bRQ6",
)


def _finite_float(
    value: float,
    name: str,
) -> float:
    """Return a finite floating-point value."""
    result = float(
        value
    )

    if not np.isfinite(
        result
    ):
        raise ValueError(
            f"{name} must be finite"
        )

    return result


def _vector_from_coefficients(
    coefficients: dict[str, float],
) -> np.ndarray:
    """Return the canonical ten-coupling vector."""
    return np.array(
        [
            float(
                coefficients[
                    name
                ]
            )
            for name
            in PARAMETER_NAMES
        ],
        dtype=float,
    )


def _coefficients_from_vector(
    vector: np.ndarray,
) -> dict[str, float]:
    """Return named couplings from the canonical ten-vector."""
    value = np.asarray(
        vector,
        dtype=float,
    )

    if value.shape != (
        len(
            PARAMETER_NAMES
        ),
    ):
        raise ValueError(
            "coupling vector has wrong shape"
        )

    if not np.all(
        np.isfinite(
            value
        )
    ):
        raise ValueError(
            "coupling vector must be finite"
        )

    return {
        name:
            float(
                component
            )
        for (
            name,
            component,
        )
        in zip(
            PARAMETER_NAMES,
            value,
        )
    }


def mp_hook_2plus_coefficients(
    *,
    m1: float = -1.0,
    b6: float = -1.0,
    b10: float = 0.5,
) -> dict[str, float]:
    """Construct a representative healthy hook 2+ coefficient point.

    Relations implement the single-state hook 2+ branch used in the
    Mikura/Percacci quadratic propagator analysis.
    """
    m1_value = _finite_float(
        m1,
        "m1",
    )

    b6_value = _finite_float(
        b6,
        "b6",
    )

    b10_value = _finite_float(
        b10,
        "b10",
    )

    if b6_value == 0.0:
        raise ValueError(
            "b6 must be nonzero"
        )

    factor = (
        (
            48.0
            *
            b6_value ** 2
            +
            24.0
            *
            b6_value
            *
            b10_value
            +
            9.0
            *
            b10_value ** 2
        )
        /
        (
            64.0
            *
            b6_value ** 2
        )
    )

    b3 = (
        b10_value ** 2
        /
        (
            8.0
            *
            b6_value
        )
    )

    b14 = -(
        (
            32.0
            *
            b6_value ** 2
            +
            3.0
            *
            b10_value ** 2
        )
        /
        (
            96.0
            *
            b6_value
        )
    )

    m3 = (
        -factor
        *
        m1_value
    )

    return {
        "m1":
            m1_value,

        "m3":
            m3,

        "b1":
            0.0,

        "b3":
            b3,

        "b6":
            b6_value,

        "b7":
            0.0,

        "b10":
            b10_value,

        "b14":
            b14,

        "bRQ4":
            0.0,

        "bRQ6":
            0.0,
    }


def mp_hook_1plus_coefficients(
    *,
    m1: float = -1.0,
    b7: float = -1.0,
    b10: float = 0.5,
) -> dict[str, float]:
    """Construct a representative healthy hook 1+ coefficient point."""
    m1_value = _finite_float(
        m1,
        "m1",
    )

    b7_value = _finite_float(
        b7,
        "b7",
    )

    b10_value = _finite_float(
        b10,
        "b10",
    )

    if b7_value == 0.0:
        raise ValueError(
            "b7 must be nonzero"
        )

    factor = (
        (
            27.0
            *
            b7_value ** 2
            +
            6.0
            *
            b7_value
            *
            b10_value
            +
            b10_value ** 2
        )
        /
        (
            36.0
            *
            b7_value ** 2
        )
    )

    b3 = (
        b10_value ** 2
        /
        (
            18.0
            *
            b7_value
        )
    )

    b6 = (
        -0.25
        *
        b7_value
    )

    b14 = (
        -0.25
        *
        b3
    )

    m3 = (
        -factor
        *
        m1_value
    )

    return {
        "m1":
            m1_value,

        "m3":
            m3,

        "b1":
            0.0,

        "b3":
            b3,

        "b6":
            b6,

        "b7":
            b7_value,

        "b10":
            b10_value,

        "b14":
            b14,

        "bRQ4":
            0.0,

        "bRQ6":
            0.0,
    }


def hook_2plus_constraint_residuals(
    coefficients: dict[str, float],
) -> np.ndarray:
    """Return seven defining residuals for the extended 2+ branch surface."""
    c = coefficients

    m1 = float(
        c[
            "m1"
        ]
    )

    m3 = float(
        c[
            "m3"
        ]
    )

    b1 = float(
        c[
            "b1"
        ]
    )

    b3 = float(
        c[
            "b3"
        ]
    )

    b6 = float(
        c[
            "b6"
        ]
    )

    b7 = float(
        c[
            "b7"
        ]
    )

    b10 = float(
        c[
            "b10"
        ]
    )

    b14 = float(
        c[
            "b14"
        ]
    )

    if b6 == 0.0:
        raise ValueError(
            "2+ constraint evaluation requires nonzero b6"
        )

    factor = (
        (
            48.0
            *
            b6 ** 2
            +
            24.0
            *
            b6
            *
            b10
            +
            9.0
            *
            b10 ** 2
        )
        /
        (
            64.0
            *
            b6 ** 2
        )
    )

    return np.array(
        [
            b1,

            b7,

            b3
            -
            (
                b10 ** 2
                /
                (
                    8.0
                    *
                    b6
                )
            ),

            b14
            +
            (
                (
                    32.0
                    *
                    b6 ** 2
                    +
                    3.0
                    *
                    b10 ** 2
                )
                /
                (
                    96.0
                    *
                    b6
                )
            ),

            m3
            +
            factor
            *
            m1,

            float(
                c[
                    "bRQ4"
                ]
            ),

            float(
                c[
                    "bRQ6"
                ]
            ),
        ],
        dtype=float,
    )


def hook_1plus_constraint_residuals(
    coefficients: dict[str, float],
) -> np.ndarray:
    """Return seven defining residuals for the extended 1+ branch surface."""
    c = coefficients

    m1 = float(
        c[
            "m1"
        ]
    )

    m3 = float(
        c[
            "m3"
        ]
    )

    b1 = float(
        c[
            "b1"
        ]
    )

    b3 = float(
        c[
            "b3"
        ]
    )

    b6 = float(
        c[
            "b6"
        ]
    )

    b7 = float(
        c[
            "b7"
        ]
    )

    b10 = float(
        c[
            "b10"
        ]
    )

    b14 = float(
        c[
            "b14"
        ]
    )

    if b7 == 0.0:
        raise ValueError(
            "1+ constraint evaluation requires nonzero b7"
        )

    factor = (
        (
            27.0
            *
            b7 ** 2
            +
            6.0
            *
            b7
            *
            b10
            +
            b10 ** 2
        )
        /
        (
            36.0
            *
            b7 ** 2
        )
    )

    return np.array(
        [
            b1,

            b3
            -
            (
                b10 ** 2
                /
                (
                    18.0
                    *
                    b7
                )
            ),

            b6
            +
            0.25
            *
            b7,

            b14
            +
            0.25
            *
            b3,

            m3
            +
            factor
            *
            m1,

            float(
                c[
                    "bRQ4"
                ]
            ),

            float(
                c[
                    "bRQ6"
                ]
            ),
        ],
        dtype=float,
    )


def hook_2plus_health(
    coefficients: dict[str, float],
) -> dict[str, Any]:
    """Return the free healthy-pole condition for the 2+ branch."""
    m1 = float(
        coefficients[
            "m1"
        ]
    )

    b6 = float(
        coefficients[
            "b6"
        ]
    )

    mass2 = (
        3.0
        *
        m1
        /
        (
            2.0
            *
            b6
        )
    )

    return {
        "m1_lt_zero":
            bool(
                m1 < 0.0
            ),

        "b6_lt_zero":
            bool(
                b6 < 0.0
            ),

        "mass2":
            mass2,

        "mass2_positive":
            bool(
                mass2 > 0.0
            ),

        "healthy":
            bool(
                m1 < 0.0
                and
                b6 < 0.0
                and
                mass2 > 0.0
            ),
    }


def hook_1plus_health(
    coefficients: dict[str, float],
) -> dict[str, Any]:
    """Return the free healthy-pole condition for the 1+ branch."""
    m1 = float(
        coefficients[
            "m1"
        ]
    )

    b7 = float(
        coefficients[
            "b7"
        ]
    )

    mass2 = (
        2.0
        *
        m1
        /
        b7
    )

    return {
        "m1_lt_zero":
            bool(
                m1 < 0.0
            ),

        "b7_lt_zero":
            bool(
                b7 < 0.0
            ),

        "mass2":
            mass2,

        "mass2_positive":
            bool(
                mass2 > 0.0
            ),

        "healthy":
            bool(
                m1 < 0.0
                and
                b7 < 0.0
                and
                mass2 > 0.0
            ),
    }


def _numerical_jacobian(
    function: Callable[
        [
            dict[
                str,
                float,
            ]
        ],
        np.ndarray,
    ],
    point: dict[str, float],
) -> np.ndarray:
    """Return a central-difference constraint Jacobian."""
    x0 = _vector_from_coefficients(
        point
    )

    base = np.asarray(
        function(
            point
        ),
        dtype=float,
    )

    jacobian = np.zeros(
        (
            base.size,
            x0.size,
        ),
        dtype=float,
    )

    for index in range(
        x0.size
    ):
        step = (
            1.0e-6
            *
            max(
                1.0,
                abs(
                    float(
                        x0[
                            index
                        ]
                    )
                ),
            )
        )

        plus = x0.copy()
        minus = x0.copy()

        plus[
            index
        ] += step

        minus[
            index
        ] -= step

        fp = np.asarray(
            function(
                _coefficients_from_vector(
                    plus
                )
            ),
            dtype=float,
        )

        fm = np.asarray(
            function(
                _coefficients_from_vector(
                    minus
                )
            ),
            dtype=float,
        )

        jacobian[
            :,
            index,
        ] = (
            fp
            -
            fm
        ) / (
            2.0
            *
            step
        )

    return jacobian


def rg_protection_gate(
    mode: str,
) -> dict[str, Any]:
    """Quantify healthy-surface codimension and generic RG normal drift.

    This is NOT an actual loop calculation.

    It tests whether the healthy branch is a lower-dimensional surface and
    whether an arbitrary generic beta vector is automatically tangent to it.
    """
    normalized = str(
        mode
    ).upper()

    if normalized == "HOOK_2_PLUS":
        point = (
            mp_hook_2plus_coefficients()
        )

        residual_function = (
            hook_2plus_constraint_residuals
        )

    elif normalized == "HOOK_1_PLUS":
        point = (
            mp_hook_1plus_coefficients()
        )

        residual_function = (
            hook_1plus_constraint_residuals
        )

    else:
        raise ValueError(
            "mode must be HOOK_2_PLUS or HOOK_1_PLUS"
        )

    residual = np.asarray(
        residual_function(
            point
        ),
        dtype=float,
    )

    jacobian = (
        _numerical_jacobian(
            residual_function,
            point,
        )
    )

    rank = int(
        np.linalg.matrix_rank(
            jacobian,
            tol=1.0e-8,
        )
    )

    nullity = int(
        jacobian.shape[
            1
        ]
        -
        rank
    )

    generic_beta = np.array(
        [
            0.31,
            -0.73,
            1.11,
            0.43,
            -0.29,
            0.61,
            -0.83,
            0.97,
            0.53,
            -0.41,
        ],
        dtype=float,
    )

    normal_drift = (
        jacobian
        @
        generic_beta
    )

    normal_drift_norm = float(
        np.linalg.norm(
            normal_drift
        )
    )

    singular_values = (
        np.linalg.svd(
            jacobian,
            compute_uv=False,
        )
    )

    return {
        "mode":
            normalized,

        "parameter_count":
            int(
                jacobian.shape[
                    1
                ]
            ),

        "constraint_count":
            int(
                jacobian.shape[
                    0
                ]
            ),

        "constraint_residual_norm":
            float(
                np.linalg.norm(
                    residual
                )
            ),

        "constraint_surface_jacobian_rank":
            rank,

        "constraint_surface_local_codimension":
            rank,

        "constraint_surface_tangent_nullity":
            nullity,

        "singular_values":
            singular_values.tolist(),

        "generic_beta_vector":
            generic_beta.tolist(),

        "generic_beta_normal_drift":
            normal_drift.tolist(),

        "generic_beta_normal_drift_norm":
            normal_drift_norm,

        "generic_beta_automatically_tangent":
            bool(
                normal_drift_norm
                <
                TOL
            ),

        "actual_beta_functions_calculated":
            False,

        "only_declared_gauge_symmetry":
            "DIFFEOMORPHISM",

        "additional_protecting_symmetry_established":
            False,

        "matter_loop_stability_calculated":
            False,

        "technical_naturalness_established":
            False,

        "protection_gate_pass":
            False,
    }


def universal_metric_active_offstate_gate() -> dict[
    str,
    Any,
]:
    """Reconstruct the V26B1 B-type quadratic physical-metric tangent."""
    hook = np.asarray(
        rest_pair_hook(),
        dtype=float,
    )

    zero = np.zeros_like(
        hook
    )

    metric_tensor = np.asarray(
        quadratic_metric_descendant(
            hook,
            coefficient_a=0.0,
            coefficient_b=1.0,
            coefficient_c=0.0,
        ),
        dtype=float,
    )

    active = np.asarray(
        quadratic_active_background_derivative(
            hook,
            hook,
            coefficient_a=0.0,
            coefficient_b=1.0,
            coefficient_c=0.0,
        ),
        dtype=float,
    )

    offstate = np.asarray(
        quadratic_active_background_derivative(
            zero,
            hook,
            coefficient_a=0.0,
            coefficient_b=1.0,
            coefficient_c=0.0,
        ),
        dtype=float,
    )

    expected = (
        2.0
        *
        metric_tensor
    )

    identity_residual = float(
        np.linalg.norm(
            active
            -
            expected
        )
        /
        max(
            float(
                np.linalg.norm(
                    expected
                )
            ),
            1.0,
        )
    )

    active_g00 = float(
        active[
            0,
            0
        ]
    )

    offstate_g00 = float(
        offstate[
            0,
            0
        ]
    )

    # For a unit T00 directional witness,
    #
    # delta S_m ~ 1/2 T^{00} delta g_phys_00.
    #
    # This is not the complete rank-three active source.
    directional_feedback = (
        0.5
        *
        active_g00
    )

    return {
        "selected_metric_basis":
            "B",

        "metric_g00_numerator":
            float(
                metric_tensor[
                    0,
                    0
                ]
            ),

        "offstate_linear_metric_response_norm":
            float(
                np.linalg.norm(
                    offstate
                )
            ),

        "offstate_linear_metric_response_zero":
            bool(
                np.linalg.norm(
                    offstate
                )
                <
                TOL
            ),

        "offstate_g00_slope":
            offstate_g00,

        "active_linear_metric_response_norm":
            float(
                np.linalg.norm(
                    active
                )
            ),

        "active_linear_metric_response_nonzero":
            bool(
                np.linalg.norm(
                    active
                )
                >
                TOL
            ),

        "active_g00_slope":
            active_g00,

        "quadratic_homogeneity_identity_relative_error":
            identity_residual,

        "quadratic_homogeneity_identity_pass":
            bool(
                identity_residual
                <
                TOL
            ),

        "unit_t00_active_directional_source_feedback":
            directional_feedback,

        "active_metric_feedback_source_nonzero":
            bool(
                abs(
                    directional_feedback
                )
                >
                TOL
            ),

        "offstate_metric_feedback_source_zero":
            bool(
                abs(
                    offstate_g00
                )
                <
                TOL
            ),

        "full_active_rank3_source_reconstructed":
            False,

        "finite_payload_evaluated":
            False,
    }


def field_redefinition_invariance_gate() -> dict[
    str,
    Any,
]:
    """Verify response invariance under an invertible active-state field change.

    The scalarized tangent model uses

        y = (h, x)

    and physical metric coupling

        M_y = (1, c),

    where c is the actual V26B1 active B-metric g00 slope along the V24 hook
    direction.

    Define

        h' = h + c x
        x' = x.

    The explicit matter portal then becomes M_z=(1,0), but kinetic/source
    mixing appears.

    The observable response must remain unchanged.
    """
    portal = (
        universal_metric_active_offstate_gate()
    )

    c = float(
        portal[
            "active_g00_slope"
        ]
    )

    if abs(
        c
    ) <= TOL:
        raise ValueError(
            "active portal slope unexpectedly vanished"
        )

    kinetic_original = np.array(
        [
            [
                3.0,
                0.4,
            ],
            [
                0.4,
                2.0,
            ],
        ],
        dtype=float,
    )

    source_original = np.array(
        [
            0.0,
            1.7,
        ],
        dtype=float,
    )

    metric_original = np.array(
        [
            1.0,
            c,
        ],
        dtype=float,
    )

    transform = np.array(
        [
            [
                1.0,
                c,
            ],
            [
                0.0,
                1.0,
            ],
        ],
        dtype=float,
    )

    inverse_transform = np.linalg.inv(
        transform
    )

    kinetic_redefined = (
        inverse_transform.T
        @
        kinetic_original
        @
        inverse_transform
    )

    source_redefined = (
        inverse_transform.T
        @
        source_original
    )

    metric_redefined = (
        inverse_transform.T
        @
        metric_original
    )

    response_original = float(
        source_original
        @
        np.linalg.inv(
            kinetic_original
        )
        @
        metric_original
    )

    response_redefined = float(
        source_redefined
        @
        np.linalg.inv(
            kinetic_redefined
        )
        @
        metric_redefined
    )

    scale = max(
        abs(
            response_original
        ),
        abs(
            response_redefined
        ),
        1.0,
    )

    relative_error = (
        abs(
            response_original
            -
            response_redefined
        )
        /
        scale
    )

    original_eigenvalues = (
        np.linalg.eigvalsh(
            kinetic_original
        )
    )

    redefined_eigenvalues = (
        np.linalg.eigvalsh(
            kinetic_redefined
        )
    )

    return {
        "active_portal_slope":
            c,

        "field_transform":
            transform.tolist(),

        "field_transform_determinant":
            float(
                np.linalg.det(
                    transform
                )
            ),

        "field_transform_invertible":
            bool(
                abs(
                    np.linalg.det(
                        transform
                    )
                )
                >
                TOL
            ),

        "original_metric_projection":
            metric_original.tolist(),

        "redefined_metric_projection":
            metric_redefined.tolist(),

        "explicit_portal_removed_in_redefined_metric_projection":
            bool(
                np.allclose(
                    metric_redefined,
                    np.array(
                        [
                            1.0,
                            0.0,
                        ]
                    ),
                    atol=1.0e-10,
                    rtol=0.0,
                )
            ),

        "original_source_projection":
            source_original.tolist(),

        "redefined_source_projection":
            source_redefined.tolist(),

        "response_original":
            response_original,

        "response_redefined":
            response_redefined,

        "response_relative_error":
            relative_error,

        "physical_response_field_redefinition_invariant":
            bool(
                relative_error
                <
                1.0e-10
            ),

        "original_principal_eigenvalues":
            original_eigenvalues.tolist(),

        "redefined_principal_eigenvalues":
            redefined_eigenvalues.tolist(),

        "original_principal_margin_positive":
            bool(
                np.min(
                    original_eigenvalues
                )
                >
                0.0
            ),

        "redefined_principal_margin_positive":
            bool(
                np.min(
                    redefined_eigenvalues
                )
                >
                0.0
            ),

        "full_tensor_nonlinear_field_redefinition_proved":
            False,
    }


def same_action_scaffold(
    mode: str,
) -> dict[str, Any]:
    """Return the conservative one-action manifest for a surviving mode."""
    normalized = str(
        mode
    ).upper()

    pole = (
        timelike_rest_pole_projector_gate()
    )

    portal = (
        universal_metric_active_offstate_gate()
    )

    redefinition = (
        field_redefinition_invariance_gate()
    )

    if normalized == "HOOK_2_PLUS":
        coefficients = (
            mp_hook_2plus_coefficients()
        )

        health = (
            hook_2plus_health(
                coefficients
            )
        )

        projector_nonzero = bool(
            pole[
                "hook_2plus_exact_pole_source_nonzero"
            ]
        )

        residual = (
            hook_2plus_constraint_residuals(
                coefficients
            )
        )

    elif normalized == "HOOK_1_PLUS":
        coefficients = (
            mp_hook_1plus_coefficients()
        )

        health = (
            hook_1plus_health(
                coefficients
            )
        )

        projector_nonzero = bool(
            pole[
                "hook_1plus_exact_pole_source_nonzero"
            ]
        )

        residual = (
            hook_1plus_constraint_residuals(
                coefficients
            )
        )

    else:
        raise ValueError(
            "mode must be HOOK_2_PLUS or HOOK_1_PLUS"
        )

    return {
        "mode":
            normalized,

        "declared_action":
            (
                "S = integral sqrt(-g) ["
                "L_EH(g) + "
                f"L_Q_{normalized}(g,Q_hook) + "
                "L_Dirac(g_phys,A(Q),psi)"
                "] + S_other_matter[g_phys]"
            ),

        "physical_metric":
            (
                "g_phys_mn = g_mn + "
                "lambda_B B_mn(Q_hook,Q_hook)"
            ),

        "single_action_manifest_written":
            True,

        "graviton_term_present":
            True,

        "healthy_hook_quadratic_sector_present":
            True,

        "intrinsic_dirac_affine_source_sector_present":
            True,

        "all_matter_declared_to_use_one_physical_metric":
            True,

        "h17a2_exact_source_projector_nonzero":
            projector_nonzero,

        "free_healthy_mode":
            health[
                "healthy"
            ],

        "branch_constraint_residual_norm":
            float(
                np.linalg.norm(
                    residual
                )
            ),

        "branch_constraints_satisfied":
            bool(
                np.linalg.norm(
                    residual
                )
                <
                TOL
            ),

        "universal_metric_offstate_linear_silence":
            portal[
                "offstate_linear_metric_response_zero"
            ],

        "universal_metric_active_response_nonzero":
            portal[
                "active_linear_metric_response_nonzero"
            ],

        "active_metric_feedback_source_nonzero":
            portal[
                "active_metric_feedback_source_nonzero"
            ],

        "field_redefinition_linear_response_survives":
            redefinition[
                "physical_response_field_redefinition_invariant"
            ],

        "v26c_massless_hook_shift_symmetry_assumed":
            False,

        "v26c_exact_massless_shift_no_go_reopened":
            False,

        "v26c_shift_obstruction_directly_applies_to_this_massive_diffeo_only_scaffold":
            False,

        "manifest_diffeomorphism_covariant":
            True,

        "full_combined_dirac_variation_rederived":
            False,

        "full_hypermomentum_noether_identity_rederived":
            False,

        "full_active_source_feedback_tensor_reconstructed":
            False,

        "full_constraint_elimination_done":
            False,

        "same_action_provenance_complete":
            False,

        "tree_level_action_scaffold_only":
            True,

        "coefficients":
            coefficients,
    }


def protection_and_provenance_gate(
    mode: str,
) -> dict[str, Any]:
    """Combine action scaffold and naturalness/protection diagnostics."""
    scaffold = (
        same_action_scaffold(
            mode
        )
    )

    rg = (
        rg_protection_gate(
            mode
        )
    )

    return {
        "mode":
            scaffold[
                "mode"
            ],

        "tree_level_action_scaffold_exists":
            bool(
                scaffold[
                    "single_action_manifest_written"
                ]
                and
                scaffold[
                    "free_healthy_mode"
                ]
                and
                scaffold[
                    "h17a2_exact_source_projector_nonzero"
                ]
                and
                scaffold[
                    "branch_constraints_satisfied"
                ]
            ),

        "linear_active_response_field_redefinition_survives":
            scaffold[
                "field_redefinition_linear_response_survives"
            ],

        "declared_gauge_symmetry":
            "DIFFEOMORPHISM_ONLY",

        "healthy_surface_codimension":
            rg[
                "constraint_surface_local_codimension"
            ],

        "healthy_surface_tangent_nullity":
            rg[
                "constraint_surface_tangent_nullity"
            ],

        "generic_rg_vector_automatically_tangent":
            rg[
                "generic_beta_automatically_tangent"
            ],

        "actual_beta_functions_calculated":
            False,

        "known_nonaccidental_protecting_symmetry":
            False,

        "radiative_stability_established":
            False,

        "technical_naturalness_established":
            False,

        "naturalness_protection_gate_pass":
            False,

        "same_action_provenance_complete":
            scaffold[
                "same_action_provenance_complete"
            ],

        "tier1_hook17_authorized":
            False,

        "h17b_authorized":
            False,

        "energy_optimization_authorized":
            False,
    }


def h17a3_summary() -> dict[str, Any]:
    """Return the conservative H17A3 decision."""
    h17a2 = (
        h17a2_summary()
    )

    two = (
        protection_and_provenance_gate(
            "HOOK_2_PLUS"
        )
    )

    one = (
        protection_and_provenance_gate(
            "HOOK_1_PLUS"
        )
    )

    portal = (
        universal_metric_active_offstate_gate()
    )

    redefinition = (
        field_redefinition_invariance_gate()
    )

    tree_scaffolds = bool(
        two[
            "tree_level_action_scaffold_exists"
        ]
        and
        one[
            "tree_level_action_scaffold_exists"
        ]
    )

    exact_projectors = bool(
        h17a2[
            "hook_2plus_exact_pole_source_nonzero"
        ]
        and
        h17a2[
            "hook_1plus_exact_pole_source_nonzero"
        ]
    )

    response_survives = bool(
        portal[
            "active_linear_metric_response_nonzero"
        ]
        and
        portal[
            "offstate_linear_metric_response_zero"
        ]
        and
        redefinition[
            "physical_response_field_redefinition_invariant"
        ]
    )

    protection_passes = bool(
        two[
            "naturalness_protection_gate_pass"
        ]
        or
        one[
            "naturalness_protection_gate_pass"
        ]
    )

    if (
        tree_scaffolds
        and
        exact_projectors
        and
        response_survives
        and
        not protection_passes
    ):
        decision = (
            "YELLOW_H17A3_"
            "TREE_LEVEL_DIRAC_HOOK_MAG_2PLUS_1PLUS_SCAFFOLDS_"
            "AND_NONREMOVABLE_ACTIVE_RESPONSE_SURVIVE__"
            "UNPROTECTED_SINGLE_STATE_REALIZATIONS_BLOCKED_"
            "PENDING_SYMMETRY_PROTECTION"
        )

        next_step = (
            "032H17A4_"
            "PROTECTED_MAG_STUECKELBERG_ACTION_ATLAS_"
            "DIRAC_SOURCE_PROJECTOR_AND_GAUGE_INVARIANT_METRIC_GATE"
        )

    else:
        decision = (
            "RED_H17A3_"
            "TREE_LEVEL_SAME_ACTION_OR_RESPONSE_GATE_FAILED"
        )

        next_step = (
            "RERANK_H17_F1_F3_AND_V26D_FALLBACK"
        )

    return {
        "decision":
            decision,

        "next":
            next_step,

        "h17a2_exact_2plus_projector_preserved":
            h17a2[
                "hook_2plus_exact_pole_source_nonzero"
            ],

        "h17a2_exact_1plus_projector_preserved":
            h17a2[
                "hook_1plus_exact_pole_source_nonzero"
            ],

        "hook_2plus_tree_level_action_scaffold":
            two[
                "tree_level_action_scaffold_exists"
            ],

        "hook_1plus_tree_level_action_scaffold":
            one[
                "tree_level_action_scaffold_exists"
            ],

        "hook_2plus_healthy_surface_codimension":
            two[
                "healthy_surface_codimension"
            ],

        "hook_1plus_healthy_surface_codimension":
            one[
                "healthy_surface_codimension"
            ],

        "hook_2plus_protection_gate_pass":
            two[
                "naturalness_protection_gate_pass"
            ],

        "hook_1plus_protection_gate_pass":
            one[
                "naturalness_protection_gate_pass"
            ],

        "unprotected_2plus_1plus_promoted":
            False,

        "active_offstate_metric_structure_preserved":
            bool(
                portal[
                    "active_linear_metric_response_nonzero"
                ]
                and
                portal[
                    "offstate_linear_metric_response_zero"
                ]
            ),

        "active_metric_source_feedback_nonzero":
            portal[
                "active_metric_feedback_source_nonzero"
            ],

        "linear_response_field_redefinition_invariant":
            redefinition[
                "physical_response_field_redefinition_invariant"
            ],

        "full_tensor_nonlinear_field_redefinition_proved":
            redefinition[
                "full_tensor_nonlinear_field_redefinition_proved"
            ],

        "same_action_provenance_complete":
            False,

        "full_noether_completion":
            False,

        "tier1_hook17_mechanism_certified":
            False,

        "h17b_authorized":
            False,

        "energy_optimization_authorized":
            False,

        "mass_candidate_campaign_authorized":
            False,

        "agminer_database_mutation_authorized":
            False,

        "hook17_reference_capacity_rp1e12_j":
            HOOK17_REFERENCE_CAPACITY_RP1E12_J,

        "hook17_complete_energy_j":
            None,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "exactly_target_passes":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "practical_device_found":
            False,

        "v26d_fallback_status":
            "PRESERVED_PAUSED_V26E_NOT_ACTIVATED",
    }
