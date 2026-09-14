"""032H17A6R1 — HOOK17 dynamical-compensator / Noether Ward theorem.

PURPOSE
-------
Follow the completed 032H17A6 gate.

A6 established, in its declared scope:

    DIRECT CLEAN V24 -> J11
    CLOSED

    ZERO-DERIVATIVE TRACE/AXIAL VECTOR IMPROVEMENTS
    CLOSED

    PURE GAUGE-IMAGE STUECKELBERG REPAIR
    CLOSED

while preserving:

    PRODUCTIVE 1+ REPRESENTATION SUPPORT
    NONZERO.

The next question is whether promoting the compensator to an ordinary
massless dynamical gauge field actually removes the source-Ward obstruction.

This module tests that question at the Noether-identity level before any
continuous parameter scan, energy optimization, or PDE solve.

CORE GAUGE STRUCTURE
--------------------
The surviving A5/A6 gauge generator is schematically

    delta K_{beta alpha chi}
    =
    partial_beta
    (
        partial_chi xi_alpha
        -
        partial_alpha xi_chi
    ).

A direct source J couples through

    S_source
    =
    integral K_{beta alpha chi}
             J^{beta alpha chi}.

Gauge invariance requires the Ward operator

    W^alpha[J]
    =
    partial_chi
    partial_beta
    J^{beta alpha chi}

to vanish for a direct massless protected source.

A6 proved that the actual clean V24 source violates this identity.

FIRST-DIVERGENCE TWO-FORM CURRENT
---------------------------------
Define

    S^{alpha chi}
    =
    partial_beta
    J^{beta alpha chi}.

Because J is antisymmetric in its final two indices,

    S^{alpha chi}
    =
    -S^{chi alpha}.

The A5/A6 Ward operator is then

    W^alpha
    =
    partial_chi
    S^{alpha chi}.

A natural dynamical compensator candidate is therefore an antisymmetric
two-form B_{alpha chi}.

Its ordinary healthy massless gauge symmetry is

    delta B_{alpha chi}
    =
    partial_alpha xi_chi
    -
    partial_chi xi_alpha.

A source term

    B_{alpha chi} S^{alpha chi}

is gauge invariant only if

    partial_alpha S^{alpha chi}
    =
    0.

By antisymmetry,

    partial_alpha S^{alpha chi}
    =
    -W^chi.

Therefore the ordinary massless two-form source condition is exactly the
same necessary Ward condition already violated by V24.

This is not a numerical coincidence.

It is a Noether identity.

PURE STUECKELBERG COMPLETION
----------------------------
Likewise define a gauge-invariant combination

    K_hat
    =
    K
    -
    G[C]

for a compensator transforming as

    delta C = xi.

If the protected massless K kinetic action satisfies

    S_kin[K + G[xi]]
    =
    S_kin[K],

then

    S_kin[K_hat]
    =
    S_kin[K].

The compensator drops out of the protected kinetic term.

Expanding the source coupling gives, up to integration by parts,

    K_hat J
    =
    K J
    +
    C_alpha W^alpha[J].

Thus the compensator Euler-Lagrange equation simply imposes

    W^alpha[J]
    =
    0.

A pure exact Stückelberg redundancy therefore cannot repair a fixed
Ward-violating source.

WHAT THIS GATE CAN CLOSE
------------------------
A RED result closes the following declared class:

    exact massless protected K carrier

    +

    one pure gauge-image compensator

or:

    exact massless protected K carrier

    +

    one ordinary healthy massless antisymmetric two-form compensator

with no separate symmetry-breaking / Higgs / mass operator and no additional
microscopic current whose Noether variation participates in the identity.

WHAT THIS GATE DOES NOT CLOSE
-----------------------------
It does NOT close:

- a Higgsed or massive hook completion;
- a soft symmetry-breaking completion;
- a multi-field Stückelberg chain;
- a full same-action matter sector whose additional currents contribute to
  the total Noether identity;
- momentum-dependent or spatially textured Dirac source engineering;
- Marzo's protected metric-affine Stückelberg family;
- Barker-Zell extended-projective / alternative-vector families;
- other protected 1+ carriers;
- protected 2+ carriers;
- V26D DHOST/KMM.

ENERGY POLICY
-------------
No energy optimization is performed.

The preserved approximately 17.0676442196 J quantity remains only the
R_P=1e12 HOOK17 canonical field-capacity reference.

The complete operating energy remains unknown.

CLAIM CLASSIFICATION
--------------------
THEOREM_FIRST_SCOPED_NOETHER_WARD_FALSIFICATION
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .hook17_j11_compensated_ward import (
    HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    h17a6_summary,
)

from .hook17_protected_k3_ward import (
    TOL,
    k3_ward_residual,
    raise_all_indices,
    v24_bms_current,
)


STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7


def a6_provenance_gate() -> dict[str, Any]:
    """Require the exact completed A6 state."""

    result = h17a6_summary()

    provenance_pass = bool(
        result[
            "direct_clean_v24_to_j11_closed"
        ]
        and
        result[
            "minimal_zero_derivative_vector_axial_improvement_closed"
        ]
        and
        result[
            "pure_stueckelberg_gauge_image_rescue_closed"
        ]
        and
        not result[
            "general_local_same_action_compensated_current_closed"
        ]
        and
        result[
            "productive_1plus_representation_survives"
        ]
    )

    return {
        "a6_decision":
            result[
                "decision"
            ],

        "a6_provenance_pass":
            provenance_pass,

        "direct_j11_closed":
            result[
                "direct_clean_v24_to_j11_closed"
            ],

        "minimal_vector_axial_closed":
            result[
                "minimal_zero_derivative_vector_axial_improvement_closed"
            ],

        "pure_gauge_image_stueckelberg_closed":
            result[
                "pure_stueckelberg_gauge_image_rescue_closed"
            ],

        "general_compensated_current_open":
            not result[
                "general_local_same_action_compensated_current_closed"
            ],

        "productive_1plus_survives":
            result[
                "productive_1plus_representation_survives"
            ],
    }


def first_divergence_twoform_current(
    q_cov: np.ndarray,
) -> np.ndarray:
    """Return S^{alpha chi} = q_beta J^{beta alpha chi}.

    The returned rank-two object is antisymmetric.

    Parameters
    ----------
    q_cov:
        Fourier momentum covector in the repository Minkowski convention.

    Returns
    -------
    numpy.ndarray
        Shape (4,4), with indices corresponding to S^{alpha chi}.
    """

    q = np.asarray(
        q_cov,
        dtype=float,
    )

    if q.shape != (
        4,
    ):
        raise ValueError(
            "q_cov must have shape (4,)"
        )

    current_up = raise_all_indices(
        v24_bms_current()
    )

    return np.einsum(
        "b,bac->ac",
        q,
        current_up,
    )


def twoform_antisymmetry_gate(
    q_cov: np.ndarray,
) -> dict[str, Any]:
    """Verify exact final-pair antisymmetry after one divergence."""

    source = first_divergence_twoform_current(
        q_cov
    )

    violation = float(
        np.max(
            np.abs(
                source
                +
                source.T
            )
        )
    )

    return {
        "q_cov":
            np.asarray(
                q_cov,
                dtype=float,
            ).tolist(),

        "max_antisymmetry_violation":
            violation,

        "antisymmetric_twoform_current":
            bool(
                violation
                <=
                TOL
            ),
    }


def ward_from_twoform_current(
    q_cov: np.ndarray,
) -> np.ndarray:
    """Return W^alpha = q_chi S^{alpha chi}."""

    q = np.asarray(
        q_cov,
        dtype=float,
    )

    source = first_divergence_twoform_current(
        q
    )

    return np.einsum(
        "c,ac->a",
        q,
        source,
    )


def twoform_source_conservation_residual(
    q_cov: np.ndarray,
) -> np.ndarray:
    """Return q_alpha S^{alpha chi}.

    For antisymmetric S,

        q_alpha S^{alpha chi}
        =
        -W^chi.
    """

    q = np.asarray(
        q_cov,
        dtype=float,
    )

    source = first_divergence_twoform_current(
        q
    )

    return np.einsum(
        "a,ac->c",
        q,
        source,
    )


def ward_twoform_identity_gate(
    q_cov: np.ndarray,
) -> dict[str, Any]:
    """Independently reconstruct the exact Noether identity.

    Three quantities are compared:

    1. the established A5 direct Ward residual;
    2. W reconstructed through the first-divergence two-form current;
    3. the massless two-form source-conservation residual.

    Exact antisymmetry requires:

        C_twoform = -W.
    """

    q = np.asarray(
        q_cov,
        dtype=float,
    )

    ward_direct = k3_ward_residual(
        q
    )

    ward_reconstructed = ward_from_twoform_current(
        q
    )

    conservation = twoform_source_conservation_residual(
        q
    )

    ward_difference = float(
        np.linalg.norm(
            ward_reconstructed
            -
            ward_direct
        )
    )

    noether_difference = float(
        np.linalg.norm(
            conservation
            +
            ward_direct
        )
    )

    return {
        "q_cov":
            q.tolist(),

        "ward_direct":
            ward_direct.tolist(),

        "ward_reconstructed":
            ward_reconstructed.tolist(),

        "twoform_conservation_residual":
            conservation.tolist(),

        "ward_direct_norm":
            float(
                np.linalg.norm(
                    ward_direct
                )
            ),

        "twoform_conservation_norm":
            float(
                np.linalg.norm(
                    conservation
                )
            ),

        "ward_reconstruction_difference_norm":
            ward_difference,

        "noether_identity_difference_norm":
            noether_difference,

        "ward_reconstruction_pass":
            bool(
                ward_difference
                <=
                TOL
            ),

        "twoform_conservation_equals_minus_ward":
            bool(
                noether_difference
                <=
                TOL
            ),

        "massless_twoform_source_compatible":
            bool(
                np.linalg.norm(
                    conservation
                )
                <=
                TOL
            ),
    }


def witness_atlas() -> list[dict[str, Any]]:
    """Evaluate high-information lightlike and static Ward witnesses."""

    momenta = {
        "LIGHTLIKE_Z":
            np.array(
                [
                    1.0,
                    0.0,
                    0.0,
                    1.0,
                ]
            ),

        "LIGHTLIKE_Y":
            np.array(
                [
                    1.0,
                    0.0,
                    1.0,
                    0.0,
                ]
            ),

        "LIGHTLIKE_X":
            np.array(
                [
                    1.0,
                    1.0,
                    0.0,
                    0.0,
                ]
            ),

        "STATIC_DIAGONAL":
            np.array(
                [
                    0.0,
                    1.0,
                    1.0,
                    1.0,
                ]
            ),
    }

    rows: list[dict[str, Any]] = []

    for name, q in momenta.items():
        gate = ward_twoform_identity_gate(
            q
        )

        rows.append(
            {
                "witness":
                    name,

                "q_cov":
                    q.tolist(),

                "ward_norm":
                    gate[
                        "ward_direct_norm"
                    ],

                "twoform_conservation_norm":
                    gate[
                        "twoform_conservation_norm"
                    ],

                "ward_reconstruction_pass":
                    gate[
                        "ward_reconstruction_pass"
                    ],

                "twoform_noether_identity_pass":
                    gate[
                        "twoform_conservation_equals_minus_ward"
                    ],

                "massless_twoform_source_compatible":
                    gate[
                        "massless_twoform_source_compatible"
                    ],
            }
        )

    return rows


def pure_stueckelberg_noether_theorem() -> dict[str, Any]:
    """State the exact single pure-gauge compensator theorem.

    If:

        K_hat = K - G[C]

    and the protected massless kinetic action obeys

        S_kin[K + G[xi]] = S_kin[K],

    then

        S_kin[K_hat] = S_kin[K].

    C therefore receives no independent kinetic operator from the protected
    massless K action.

    The source term generates

        C_alpha W^alpha[J]

    after integration by parts.

    C's Euler-Lagrange equation is exactly W[J]=0.

    The theorem is algebraic and independent of the numerical size of C.
    """

    q = np.array(
        [
            1.0,
            0.0,
            0.0,
            1.0,
        ]
    )

    ward = k3_ward_residual(
        q
    )

    ward_norm = float(
        np.linalg.norm(
            ward
        )
    )

    return {
        "protected_massless_kinetic_gauge_invariant":
            True,

        "stueckelberg_combination":
            "K_hat=K-G[C]",

        "kinetic_compensator_dependence":
            "DROPS_OUT_BY_EXACT_GAUGE_INVARIANCE",

        "source_after_integration_by_parts":
            "K.J + C_alpha W^alpha[J]",

        "compensator_eom":
            "W^alpha[J]=0",

        "lightlike_z_ward_residual":
            ward.tolist(),

        "lightlike_z_ward_norm":
            ward_norm,

        "pure_exact_massless_stueckelberg_can_repair":
            bool(
                ward_norm
                <=
                TOL
            ),

        "pure_exact_massless_stueckelberg_closed":
            bool(
                ward_norm
                >
                TOL
            ),

        "closure_scope":
            (
                "ONE PURE GAUGE-IMAGE COMPENSATOR WITH NO "
                "SYMMETRY-BREAKING OR ADDITIONAL NOETHER CURRENT"
            ),
    }


def massless_twoform_compensator_theorem() -> dict[str, Any]:
    """Test the natural dynamical antisymmetric two-form compensator.

    The ordinary healthy massless two-form action is based on

        H = dB.

    Its gauge symmetry

        delta B = d xi

    requires any direct antisymmetric source S^{alpha chi} to satisfy

        partial_alpha S^{alpha chi} = 0.

    For the V24-derived source

        S^{alpha chi}
        =
        partial_beta J^{beta alpha chi},

    this condition is exactly minus the A5/A6 Ward operator.
    """

    rows = witness_atlas()

    nonzero_failures = [
        row
        for row in rows
        if (
            row[
                "twoform_noether_identity_pass"
            ]
            and
            not row[
                "massless_twoform_source_compatible"
            ]
        )
    ]

    all_identity_pass = all(
        row[
            "twoform_noether_identity_pass"
        ]
        and
        row[
            "ward_reconstruction_pass"
        ]
        for row in rows
    )

    return {
        "compensator":
            "MASSLESS_ANTISYMMETRIC_TWOFORM_B",

        "healthy_free_action":
            "L=-H_{abc}H^{abc}/12",

        "gauge_symmetry":
            "delta B_{ac}=partial_a xi_c-partial_c xi_a",

        "source":
            "S^{ac}=partial_b J^{bac}",

        "required_source_identity":
            "partial_a S^{ac}=0",

        "identity_equivalent_to":
            "-W^c[J]=0",

        "all_noether_identity_reconstructions_pass":
            all_identity_pass,

        "nonzero_incompatible_witness_count":
            len(
                nonzero_failures
            ),

        "massless_twoform_compensator_can_absorb_v24":
            False
            if nonzero_failures
            else True,

        "massless_twoform_compensator_closed":
            bool(
                all_identity_pass
                and
                nonzero_failures
            ),

        "closure_scope":
            (
                "ORDINARY HEALTHY MASSLESS TWOFORM COMPENSATOR "
                "WITH NO MASS/HIGGS OPERATOR AND NO EXTRA CURRENT"
            ),

        "witnesses":
            rows,
    }


def noether_completion_escape_atlas() -> list[dict[str, Any]]:
    """Classify the remaining physically distinct escapes."""

    stueckelberg = pure_stueckelberg_noether_theorem()
    twoform = massless_twoform_compensator_theorem()

    return [
        {
            "family":
                "PURE_EXACT_STUECKELBERG_GAUGE_IMAGE",

            "status":
                (
                    "RED_SCOPED"
                    if stueckelberg[
                        "pure_exact_massless_stueckelberg_closed"
                    ]
                    else
                    "OPEN"
                ),

            "changes_ward_surface":
                False,

            "adds_physical_longitudinal_mode":
                False,

            "same_action_requirement":
                "DECLARED_EXACT_MASSLESS_PROTECTED_ACTION",

            "next_action":
                "NONE_IN_THIS_SUBCLASS",
        },
        {
            "family":
                "HEALTHY_MASSLESS_TWOFORM_COMPENSATOR",

            "status":
                (
                    "RED_SCOPED"
                    if twoform[
                        "massless_twoform_compensator_closed"
                    ]
                    else
                    "OPEN"
                ),

            "changes_ward_surface":
                False,

            "adds_physical_longitudinal_mode":
                False,

            "same_action_requirement":
                "ORDINARY_H_EQUALS_DB_GAUGE_ACTION",

            "next_action":
                "NONE_IN_THIS_SUBCLASS",
        },
        {
            "family":
                "FULL_NOETHER_COMPLETE_MATTER_PLUS_COMPENSATOR",

            "status":
                "OPEN",

            "changes_ward_surface":
                "POSSIBLY_TOTAL_CURRENT_ONLY",

            "adds_physical_longitudinal_mode":
                "MODEL_DEPENDENT",

            "same_action_requirement":
                (
                    "ALL MATTER AND COMPENSATOR CURRENTS MUST "
                    "COME FROM ONE VARIATIONAL ACTION"
                ),

            "next_action":
                "DERIVE_TOTAL_NOETHER_CURRENT",
        },
        {
            "family":
                "HIGGSED_OR_MASSIVE_HOOK_COMPLETION",

            "status":
                "OPEN",

            "changes_ward_surface":
                True,

            "adds_physical_longitudinal_mode":
                True,

            "same_action_requirement":
                (
                    "EXPLICIT MASS/HIGGS/STUECKELBERG ACTION "
                    "WITH FULL SPECTRAL HEALTH"
                ),

            "next_action":
                "MASSIVE_PRINCIPAL_SYMBOL_AND_SOURCE_PROJECTOR",
        },
        {
            "family":
                "MARZO_PROTECTED_ABELIAN_MAG_STUECKELBERG",

            "status":
                "OPEN_INDEPENDENT_FAMILY",

            "changes_ward_surface":
                "MUST_BE_DERIVED_FOR_V24_SOURCE",

            "adds_physical_longitudinal_mode":
                "PUBLISHED_MASS_EXTENSION_EXISTS",

            "same_action_requirement":
                "MUST_SOURCE_MATCH_V24_INSIDE_THE_PUBLISHED_ACTION",

            "next_action":
                "EXACT_V24_SOURCE_MATCH_GATE",
        },
        {
            "family":
                "OTHER_PROTECTED_1PLUS_OR_2PLUS",

            "status":
                "OPEN",

            "changes_ward_surface":
                "ACTION_DEPENDENT",

            "adds_physical_longitudinal_mode":
                "ACTION_DEPENDENT",

            "same_action_requirement":
                "MANDATORY",

            "next_action":
                "SOURCE_PROJECTOR_BEFORE_ANY_PDE",
        },
    ]


def h17a6r1_summary() -> dict[str, Any]:
    """Return the conservative decision for A6R1."""

    provenance = a6_provenance_gate()
    pure = pure_stueckelberg_noether_theorem()
    twoform = massless_twoform_compensator_theorem()

    declared_red = bool(
        provenance[
            "a6_provenance_pass"
        ]
        and
        pure[
            "pure_exact_massless_stueckelberg_closed"
        ]
        and
        twoform[
            "massless_twoform_compensator_closed"
        ]
    )

    return {
        "branch":
            "032H17A6R1",

        "subgate":
            "DYNAMICAL_COMPENSATOR_NOETHER_WARD_THEOREM",

        "decision":
            (
                "RED_SCOPED_A6R1_EXACT_MASSLESS_SINGLE_COMPENSATOR_"
                "CLASS_RETURNS_TO_SAME_WARD_IDENTITY__"
                "HIGGSED_OR_FULL_NOETHER_COMPLETION_REMAINS_OPEN"
            )
            if declared_red
            else
            "CHECK_A6R1_THEOREM_ASSUMPTIONS",

        "a6_provenance_pass":
            provenance[
                "a6_provenance_pass"
            ],

        "productive_1plus_representation_survives":
            provenance[
                "productive_1plus_survives"
            ],

        "pure_exact_massless_stueckelberg_closed":
            pure[
                "pure_exact_massless_stueckelberg_closed"
            ],

        "healthy_massless_twoform_compensator_closed":
            twoform[
                "massless_twoform_compensator_closed"
            ],

        "declared_exact_massless_single_compensator_class_closed":
            declared_red,

        "full_noether_complete_matter_compensator_closed":
            False,

        "higgsed_or_massive_hook_closed":
            False,

        "marzo_protected_stueckelberg_family_closed":
            False,

        "other_protected_1plus_closed":
            False,

        "protected_2plus_closed":
            False,

        "source_state_engineering_closed":
            False,

        "hook17_closed":
            False,

        "hook17_reference_capacity_rp1e12_j":
            HOOK17_REFERENCE_CAPACITY_RP1E12_J,

        "hook17_complete_energy_j":
            None,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "energy_optimization_authorized":
            False,

        "sub100j_capacity_tuning_authorized":
            False,

        "h17b_authorized":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "practical_device_found":
            False,

        "v26d_fallback_status":
            "PRESERVED",

        "v26e_status":
            "PAUSED_NOT_CLOSED",

        "next":
            (
                "032H17A6R2_HIGGSED_HOOK_OR_FULL_"
                "NOETHER_COMPLETION_PREFLIGHT"
            ),

        "stop_rule_after_next":
            (
                "IF NO EXPLICIT HEALTHY HIGGSED/NOETHER COMPLETION "
                "SURVIVES, MOVE TO MARZO PROTECTED SOURCE-MATCH GATE "
                "RATHER THAN INVENTING MORE FORMAL COMPENSATORS"
            ),

        "escape_atlas":
            noether_completion_escape_atlas(),
    }
