"""032H17A5 — exact protected K3 1+ V24 source-Ward gate.

PURPOSE
-------
Follow 032H17A4 by testing the highest-priority concrete protected
pair-antisymmetric rank-three realization rather than another abstract
representation match.

The selected literature target is model K3 of:

    Barker, Marzo, Santoni
    arXiv:2507.05349

K3 is a gauge-symmetric, ghost/tachyon-free pair-antisymmetric rank-three
model with minimal axial-vector / even-parity 1+ propagation.

The published K3 spectrograph reports:

    two massless physical polarizations;
    one free kinetic coefficient;
    unitarity condition kappa3^(4) < 0;
    twenty-one source constraints.

One of its necessary source-Ward conditions is

    partial_chi partial_beta J^{beta alpha chi} = 0.

In Fourier space, ignoring the irrelevant common i^2 sign,

    q_chi q_beta J^{beta alpha chi} = 0.

This module maps the actual V24 clean Dirac hook source into the index
convention used by the pair-antisymmetric K3 theory and evaluates that
necessary Ward identity exactly.

REPRESENTATION CONVENTIONS
--------------------------
The project V24C representation map uses

    T_abc = H_abc - H_bac,

with

    T_abc = -T_bac.

The Barker-Marzo-Santoni convention instead uses a field/current

    K_abc = -K_acb,

antisymmetric in its last two indices.

The equivalent algebraic permutation is

    J_BMS[a,b,c] = T[b,c,a].

This is an invertible index permutation. It does not alter whether the
underlying representation is present, but it is necessary before comparing
component formulae and Ward constraints.

HELICITY PREFILTER
------------------
The paper supplies explicit source-helicity combinations for a current
J_{a[bc]}.

For the actual mapped clean V24 source this module verifies:

    spin-two helicity seeds = zero;
    zero-helicity seeds     = zero;
    spin-one helicity seeds = nonzero.

Thus the failure, if present, is not a trivial absence of 1+ representation
support.

WARD FALSIFICATION
------------------
Gauge symmetry makes the kinetic operator singular. Consistency of a direct
source term requires the source current to annihilate the gauge null
directions.

A single nonzero value of a necessary Ward residual is therefore sufficient
to reject the direct source coupling.

The high-information witness used here is

    q = (1,0,0,1),

which is lightlike under eta=(-,+,+,+) and hence directly probes the massless
K3 pole kinematics.

LOCALIZED-SOURCE THEOREM
------------------------
For the simple clean-rest-pair source architecture

    J_abc(q) = F(q) J0_abc,

where J0 is the fixed V24 tensor and F is a common scalar envelope, the Ward
condition becomes

    F(q) P^alpha(q) = 0,

where

    P^alpha(q)
      = q_chi q_beta J0^{beta alpha chi}.

If P(q) is not identically zero, a nonzero localized scalar envelope cannot
make the identity hold for generic Fourier support.

This closes only that fixed-tensor scalar-envelope direct K3 realization.

It does NOT close a source whose spinor texture itself depends on momentum or
position in such a way that the full current obeys the Ward identities.

It also does NOT close compensator/current-improvement constructions.

VECTOR-GRAVITON DISCIPLINE
--------------------------
K3's massless axial vector is not silently identified with:

    the A4 Stückelberg invariant W_mu,
    Marzo's 2022 protected nonmetricity vector,
    Barker-Zell's alternative double-vector,
    or Marzo's 2026 nonlinear massive vector-graviton carrier.

Those require explicit same-action maps.

CLAIM LIMITS
------------
This module does NOT establish:

- a complete same-action HOOK17 theory;
- a protected gauge-invariant universal metric for K3;
- a finite-payload antigravity field;
- the complete HOOK17 energy;
- a practical device.

A failure closes only:

    DIRECT CLEAN V24 REST-PAIR SOURCE
    +
    COMMON SCALAR ENVELOPE
    +
    K3 PROTECTED AXIAL 1+ ACTION.

No AGMINER database mutation is performed.
No energy optimization is performed.

CLAIM_CLASSIFICATION=
SCOPED_PROTECTED_1PLUS_DIRECT_SOURCE_WARD_FALSIFICATION_GATE
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .dirac_hook_vector_bridge import (
    hook_to_torsionlike,
    rest_pair_source_parts,
)


ETA = np.diag(
    [
        -1.0,
        1.0,
        1.0,
        1.0,
    ]
)

TOL = 1.0e-12

HOOK17_REFERENCE_CAPACITY_RP1E12_J = 17.0676442196
STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7


def v24_bms_current() -> np.ndarray:
    """Return the clean V24 source in the K3 J_{a[bc]} convention."""
    hook = np.asarray(
        rest_pair_source_parts()[
            "hook"
        ],
        dtype=float,
    )

    torsionlike = np.asarray(
        hook_to_torsionlike(
            hook
        ),
        dtype=float,
    )

    current = np.transpose(
        torsionlike,
        (
            2,
            0,
            1,
        ),
    )

    if not np.allclose(
        current,
        -np.swapaxes(
            current,
            1,
            2,
        ),
        atol=TOL,
        rtol=0.0,
    ):
        raise ValueError(
            "BMS current must be antisymmetric in its last two indices"
        )

    return current


def raise_all_indices(
    tensor_cov: np.ndarray,
) -> np.ndarray:
    """Raise all indices with eta=(-,+,+,+)."""
    tensor = np.asarray(
        tensor_cov,
        dtype=float,
    )

    if tensor.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "tensor must have shape (4,4,4)"
        )

    return np.einsum(
        "ai,bj,ck,ijk->abc",
        ETA,
        ETA,
        ETA,
        tensor,
    )


def source_component_gate() -> dict[
    str,
    Any,
]:
    """Return the exact sparse mapped source."""
    current = (
        v24_bms_current()
    )

    rows: list[
        dict[
            str,
            Any,
        ]
    ] = []

    for indices in np.argwhere(
        np.abs(
            current
        )
        >
        TOL
    ):
        key = tuple(
            int(
                value
            )
            for value in indices
        )

        rows.append(
            {
                "indices":
                    list(
                        key
                    ),

                "value":
                    float(
                        current[
                            key
                        ]
                    ),
            }
        )

    expected = [
        {
            "indices":
                [
                    0,
                    2,
                    3,
                ],

            "value":
                8.0,
        },
        {
            "indices":
                [
                    0,
                    3,
                    2,
                ],

            "value":
                -8.0,
        },
        {
            "indices":
                [
                    3,
                    0,
                    2,
                ],

            "value":
                -8.0,
        },
        {
            "indices":
                [
                    3,
                    2,
                    0,
                ],

            "value":
                8.0,
        },
    ]

    return {
        "last_pair_antisymmetric":
            bool(
                np.allclose(
                    current,
                    -np.swapaxes(
                        current,
                        1,
                        2,
                    ),
                    atol=TOL,
                    rtol=0.0,
                )
            ),

        "component_norm":
            float(
                np.linalg.norm(
                    current
                )
            ),

        "nonzero_component_count":
            len(
                rows
            ),

        "components":
            rows,

        "expected_sparse_identity_pass":
            rows
            ==
            expected,
    }


def bms_helicity_prefilter() -> dict[
    str,
    Any,
]:
    """Evaluate the paper's explicit source-helicity seed combinations."""
    j = (
        v24_bms_current()
    )

    spin2_1 = (
        float(
            j[
                2,
                2,
                3,
            ]
            -
            j[
                1,
                1,
                3,
            ]
        ),

        float(
            j[
                1,
                2,
                3,
            ]
            +
            j[
                2,
                1,
                3,
            ]
        ),
    )

    spin2_2 = (
        float(
            j[
                2,
                0,
                2,
            ]
            -
            j[
                1,
                0,
                1,
            ]
        ),

        float(
            j[
                1,
                0,
                2,
            ]
            +
            j[
                2,
                0,
                1,
            ]
        ),
    )

    spin1 = {
        "eps1":
            (
                float(
                    j[
                        3,
                        2,
                        3,
                    ]
                ),
                float(
                    j[
                        3,
                        1,
                        3,
                    ]
                ),
            ),

        "eps2":
            (
                float(
                    j[
                        0,
                        2,
                        3,
                    ]
                ),
                float(
                    j[
                        0,
                        1,
                        3,
                    ]
                ),
            ),

        "eps3":
            (
                float(
                    j[
                        2,
                        1,
                        2,
                    ]
                ),
                float(
                    j[
                        1,
                        1,
                        2,
                    ]
                ),
            ),

        "eps4":
            (
                float(
                    j[
                        3,
                        0,
                        2,
                    ]
                ),
                float(
                    j[
                        3,
                        0,
                        1,
                    ]
                ),
            ),

        "eps5":
            (
                float(
                    j[
                        2,
                        0,
                        3,
                    ]
                ),
                float(
                    j[
                        1,
                        0,
                        3,
                    ]
                ),
            ),

        "eps6":
            (
                float(
                    j[
                        0,
                        0,
                        2,
                    ]
                ),
                float(
                    j[
                        0,
                        0,
                        1,
                    ]
                ),
            ),
    }

    zero_helicity = [
        float(
            j[
                1,
                1,
                3,
            ]
            +
            j[
                2,
                2,
                3,
            ]
        ),

        float(
            j[
                1,
                2,
                3,
            ]
            -
            j[
                2,
                1,
                3,
            ]
        ),

        float(
            j[
                3,
                1,
                2,
            ]
        ),

        float(
            j[
                0,
                1,
                2,
            ]
        ),

        float(
            j[
                3,
                0,
                3,
            ]
        ),

        float(
            j[
                1,
                0,
                1,
            ]
            +
            j[
                2,
                0,
                2,
            ]
        ),

        float(
            j[
                2,
                0,
                1,
            ]
            -
            j[
                1,
                0,
                2,
            ]
        ),

        float(
            j[
                0,
                0,
                3,
            ]
        ),
    ]

    spin2_norm2 = sum(
        real ** 2
        +
        imag ** 2
        for (
            real,
            imag,
        )
        in (
            spin2_1,
            spin2_2,
        )
    )

    spin1_norm2 = sum(
        real ** 2
        +
        imag ** 2
        for (
            real,
            imag,
        )
        in spin1.values()
    )

    zero_norm2 = float(
        np.dot(
            zero_helicity,
            zero_helicity,
        )
    )

    return {
        "spin2_helicity_seed_norm2":
            float(
                spin2_norm2
            ),

        "spin2_helicity_seed_zero":
            bool(
                spin2_norm2
                <=
                TOL
            ),

        "spin1_helicity_seed_norm2":
            float(
                spin1_norm2
            ),

        "spin1_helicity_seed_nonzero":
            bool(
                spin1_norm2
                >
                TOL
            ),

        "spin1_helicity_pairs":
            {
                name:
                    [
                        real,
                        imag,
                    ]
                for (
                    name,
                    (
                        real,
                        imag,
                    ),
                )
                in spin1.items()
            },

        "zero_helicity_seed":
            zero_helicity,

        "zero_helicity_seed_norm2":
            zero_norm2,

        "zero_helicity_seed_zero":
            bool(
                zero_norm2
                <=
                TOL
            ),

        "representation_overlap_is_ward_compatibility":
            False,
    }


def k3_published_model_gate() -> dict[
    str,
    Any,
]:
    """Encode the published K3 model facts used by this gate."""
    return {
        "family":
            "BARKER_MARZO_SANTONI_K3",

        "arxiv":
            "2507.05349",

        "pair_antisymmetric_rank3":
            True,

        "parity_conserving":
            True,

        "gauge_symmetric":
            True,

        "ghost_tachyon_free":
            True,

        "propagating_sector":
            "AXIAL_VECTOR_EVEN_PARITY_1PLUS",

        "massless":
            True,

        "physical_polarizations":
            2,

        "free_kinetic_parameters":
            1,

        "unitarity_condition":
            "kappa3_4 < 0",

        "published_source_constraint_count":
            21,

        "necessary_source_constraint":
            (
                "q_chi q_beta "
                "J^{beta alpha chi}=0"
            ),

        "source_constraints_are_ward_conditions":
            True,
    }


def minkowski_q2(
    q_cov: np.ndarray,
) -> float:
    """Return q^2 for a covector using eta=(-,+,+,+)."""
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

    return float(
        q
        @
        ETA
        @
        q
    )


def k3_ward_residual(
    q_cov: np.ndarray,
) -> np.ndarray:
    """Return q_chi q_beta J^{beta alpha chi} for the actual V24 current."""
    q = np.asarray(
        q_cov,
        dtype=float,
    )

    if (
        q.shape
        !=
        (
            4,
        )
        or
        not np.all(
            np.isfinite(
                q
            )
        )
    ):
        raise ValueError(
            "q_cov must be finite with shape (4,)"
        )

    current_up = (
        raise_all_indices(
            v24_bms_current()
        )
    )

    return np.einsum(
        "c,b,bac->a",
        q,
        q,
        current_up,
    )


def k3_ward_counterexample_gate() -> dict[
    str,
    Any,
]:
    """Evaluate high-information Ward witnesses."""
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

    rows: dict[
        str,
        Any,
    ] = {}

    for (
        name,
        q,
    ) in momenta.items():
        residual = (
            k3_ward_residual(
                q
            )
        )

        norm = float(
            np.linalg.norm(
                residual
            )
        )

        rows[
            name
        ] = {
            "q_cov":
                q.tolist(),

            "q2":
                minkowski_q2(
                    q
                ),

            "residual":
                residual.tolist(),

            "residual_norm":
                norm,

            "passes_necessary_ward":
                bool(
                    norm
                    <=
                    TOL
                ),
        }

    witness = (
        rows[
            "LIGHTLIKE_Z"
        ]
    )

    return {
        "rows":
            rows,

        "lightlike_physical_pole_witness_q2_zero":
            bool(
                abs(
                    witness[
                        "q2"
                    ]
                )
                <=
                TOL
            ),

        "lightlike_physical_pole_witness_residual_norm":
            witness[
                "residual_norm"
            ],

        "lightlike_physical_pole_witness_fails":
            not witness[
                "passes_necessary_ward"
            ],

        "at_least_one_ward_counterexample":
            any(
                not row[
                    "passes_necessary_ward"
                ]
                for row in rows.values()
            ),

        "direct_v24_k3_source_ward_compatible":
            all(
                row[
                    "passes_necessary_ward"
                ]
                for row in rows.values()
            ),

        "one_counterexample_is_sufficient_to_reject_direct_coupling":
            True,
    }


def localized_scalar_envelope_theorem() -> dict[
    str,
    Any,
]:
    """Apply the Ward polynomial to a fixed-tensor compact-source ansatz."""
    ward = (
        k3_ward_counterexample_gate()
    )

    return {
        "ansatz":
            (
                "J_abc(q)=F(q) J0_abc "
                "with fixed clean-rest-pair tensor J0"
            ),

        "localized_nonzero_source_has_fourier_support_beyond_single_ward_zero_direction":
            True,

        "ward_polynomial_identically_zero":
            False,

        "explicit_nonzero_polynomial_witness_norm":
            ward[
                "lightlike_physical_pole_witness_residual_norm"
            ],

        "compact_scalar_envelope_direct_k3_compatible":
            False,

        "theorem_scope":
            (
                "FIXED_TENSOR_CLEAN_REST_PAIR_"
                "TIMES_COMMON_SCALAR_ENVELOPE"
            ),

        "q_dependent_spinor_texture_closed":
            False,

        "improved_or_compensated_current_closed":
            False,

        "other_protected_axial_vector_actions_closed":
            False,
    }


def vector_graviton_identification_gate() -> dict[
    str,
    Any,
]:
    """Prevent representation-level vector stitching from becoming same action."""
    return {
        "k3_carrier":
            (
                "MASSLESS_AXIAL_1PLUS_FROM_"
                "PAIR_ANTISYMMETRIC_RANK3"
            ),

        "a4_stueckelberg_witness":
            "W_mu=V_mu-partial_mu pi/m",

        "marzo2026_carrier":
            (
                "GAUGE_INVARIANT_MASSIVE_VECTOR_"
                "MIXED_WITH_GRAVITON"
            ),

        "k3_equals_a4_stueckelberg_W_in_same_action":
            False,

        "k3_equals_marzo2026_vector_in_same_action":
            False,

        "field_redefinition_or_duality_identification_derived":
            False,

        "gauge_invariant_hook17_metric_in_k3_same_action":
            False,

        "direct_vector_graviton_identification_pass":
            False,
    }


def protected_rescue_rerank() -> list[
    dict[
        str,
        Any,
    ]
]:
    """Return the next protected rescue order after the K3 direct test."""
    return [
        {
            "priority":
                1,

            "family":
                "BMS_J11_LESS_CONSTRAINING_AXIAL_VECTOR",

            "status":
                "OPEN_EXACT_SOURCE_WARD_REQUIRED",
        },
        {
            "priority":
                2,

            "family":
                "COMPENSATED_OR_IMPROVED_V24_CURRENT_IN_K3_LIKE_1PLUS",

            "status":
                "OPEN_LOCAL_SAME_ACTION_CONSTRUCTION_REQUIRED",
        },
        {
            "priority":
                3,

            "family":
                "MARZO2022_ABELIAN_NONMETRICITY_STUECKELBERG",

            "status":
                "OPEN_V24_SOURCE_MATCH_REQUIRED",
        },
        {
            "priority":
                4,

            "family":
                "BARKER_ZELL_ALT_DOUBLE_VECTOR",

            "status":
                "OPEN_DIRAC_SOURCE_MATCH_REQUIRED",
        },
        {
            "priority":
                5,

            "family":
                "MARZO2026_NONLINEAR_VECTOR_GRAVITON",

            "status":
                "OPEN_SOURCE_IDENTIFICATION_REQUIRED",
        },
    ]


def h17a5_summary() -> dict[
    str,
    Any,
]:
    """Return the conservative H17A5 decision."""
    helicity = (
        bms_helicity_prefilter()
    )

    ward = (
        k3_ward_counterexample_gate()
    )

    envelope = (
        localized_scalar_envelope_theorem()
    )

    bridge = (
        vector_graviton_identification_gate()
    )

    direct_closed = bool(
        helicity[
            "spin1_helicity_seed_nonzero"
        ]
        and
        ward[
            "at_least_one_ward_counterexample"
        ]
    )

    if direct_closed:
        decision = (
            "RED_SCOPED_H17A5_"
            "K3_DIRECT_PROTECTED_1PLUS_V24_SOURCE_WARD_FAIL__"
            "REPRESENTATION_OVERLAP_SURVIVES_"
            "BUT_DIRECT_K3_SAME_ACTION_CLOSED"
        )

        next_step = (
            "JOURNAL_H17A2_TO_A5__THEN_"
            "032H17A6_J11_AND_COMPENSATED_SOURCE_WARD_GATE"
        )

    else:
        decision = (
            "YELLOW_H17A5_"
            "K3_DIRECT_SOURCE_NOT_CLOSED"
        )

        next_step = (
            "032H17A5R1_"
            "FULL_K3_SOURCE_PROJECTOR_AND_METRIC_GATE"
        )

    return {
        "decision":
            decision,

        "next":
            next_step,

        "k3_direct_v24_source_closed":
            direct_closed,

        "k3_representation_spin1_overlap_preserved":
            helicity[
                "spin1_helicity_seed_nonzero"
            ],

        "k3_source_ward_compatible":
            ward[
                "direct_v24_k3_source_ward_compatible"
            ],

        "k3_lightlike_ward_witness_norm":
            ward[
                "lightlike_physical_pole_witness_residual_norm"
            ],

        "clean_scalar_envelope_k3_closed":
            not envelope[
                "compact_scalar_envelope_direct_k3_compatible"
            ],

        "q_dependent_source_engineering_open":
            not envelope[
                "q_dependent_spinor_texture_closed"
            ],

        "compensated_current_open":
            not envelope[
                "improved_or_compensated_current_closed"
            ],

        "j11_open":
            True,

        "k3_vector_graviton_same_action_identification":
            bridge[
                "direct_vector_graviton_identification_pass"
            ],

        "hook17_all_protected_1plus_closed":
            False,

        "same_action_provenance_complete":
            False,

        "full_noether_completion":
            False,

        "journal_now":
            True,

        "h17b_authorized":
            False,

        "energy_optimization_authorized":
            False,

        "sub100j_efficiency_tuning_authorized":
            False,

        "hook17_reference_capacity_rp1e12_j":
            HOOK17_REFERENCE_CAPACITY_RP1E12_J,

        "hook17_complete_energy_j":
            None,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "practical_device_found":
            False,

        "v26d_fallback_status":
            "PRESERVED_PAUSED_V26E_NOT_ACTIVATED",
    }
