"""032H17A9R1 — Wheeler / Percacci-Sezgin same-action matter Noether preflight.

PURPOSE
-------
Follow the first positive physical-pole result of the HOOK17 rescue chain.

A9 established:

    healthy Percacci-Sezgin Case-I massive 1+ pole;

    convention-matched Wheeler -> P&S connection source;

    required torsion-free source projection;

    exact projective trace PASS for the clean equal-rest e-/e+ pair;

    exact nonzero healthy 1+ pole numerator = 1.44.

But A9 did NOT establish that the Wheeler Dirac matter action itself respects
the Percacci-Sezgin projective gauge symmetry.

That distinction is critical.

A gauge symmetry must constrain the matter source as an action/current
identity.  It is not sufficient that one specially chosen source state
happens to lie on the zero-trace surface.

A9R1 therefore performs two independent theorem-first tests:

1. PROJECTIVE MATTER-SOURCE IDENTITY TEST

   Wheeler's source is a Hermitian quadratic function of a four-component
   complex spinor.

   A Hermitian 4x4 quadratic form has 16 real directions:

       4 diagonal directions
       6 real off-diagonal directions
       6 imaginary off-diagonal directions.

   We probe a complete deterministic basis:

       e_i

       (e_i + e_j)/sqrt(2)

       (e_i + i e_j)/sqrt(2).

   If both P&S projective source traces vanish on all 16 probes, they vanish
   identically over the implemented Wheeler spinor source manifold.

   If even one basis direction is nonzero, the clean A9 source is only a
   special source configuration and the UNMODIFIED Wheeler matter action is
   not accepted as a projectively invariant same-action completion.

2. LOCAL DIFFEOMORPHISM-WARD COMPLETION TEST

   Percacci-Sezgin require

       2 i q^a sigma_ac
       +
       q^a q^b tau_bca
       =
       0.

   Before deriving the actual Wheeler metric stress tensor, A9R1 asks the
   cheaper necessary question:

   Does there exist any LOCAL first-derivative symmetric stress of the form

       sigma_ac(q)
       =
       i S_acd q^d,

       S_acd = S_cad,

   satisfying the polynomial Ward identity for every q?

   This is a finite 40x40 linear system.

   No inverse q, inverse q^2, nonlocal Green function, or momentum-dependent
   fitted coefficient is permitted.

IMPORTANT INTERPRETATION
------------------------
A local algebraic sigma solution is NOT the Wheeler stress tensor.

It demonstrates only that the clean connection current does not encounter a
separate algebraic locality obstruction in the diffeomorphism Ward identity.

The actual sigma must still be obtained by variation of one covariant matter
action.

PUBLISHED SOURCE IDENTITIES
---------------------------
Percacci-Sezgin torsion-free projective symmetry requires:

    tau^nu_{nu mu} = 0

    tau_{mu nu}^nu = 0.

Their diffeomorphism source identity is:

    2 i q^a sigma_ac
    +
    q^a q^b tau_bca
    =
    0.

Wheeler's GL(4) Dirac source is built from the complete Hermitian spinor
bilinear/current space.

EXPECTED PRE-RESULT
-------------------
Direct reconstruction of the existing Wheeler formula predicts:

    Hermitian source probes = 16

    projective-compatible probes = 3

    projective-incompatible probes = 13.

For example:

    D1 = e_1

gives projected trace

    [0, 2, 0, 0].

The largest basis residual is predicted for the I01 probe:

    norm = sqrt(4.5).

Thus:

    UNMODIFIED WHEELER MATTER
        +
    PERCACCI-SEZGIN PROJECTIVE GRAVITY

is expected to fail same-action projective symmetry.

This does NOT invalidate the A9 clean physical-pole overlap.

It says that the clean A9 configuration lies in a special compatible source
subspace.

REMAINING RESCUE
----------------
A genuinely different matter completion remains open:

    a local covariant PROJECTIVELY INVARIANT Dirac coupling

whose variational hypermomentum:

    satisfies the projective identities identically;

    preserves the clean A9 1+ source component;

    preserves the healthy P&S pole;

    supplies the metric stress sigma from the same action.

That is not accepted or constructed in A9R1.

ENERGY POLICY
-------------
No energy optimization is performed.

17.0676442196 J remains only the preserved HOOK17 canonical field-capacity
reference.

Complete operating energy remains unknown.

H17B remains unauthorized.

CLAIM_CLASSIFICATION
--------------------
SAME_ACTION_PROJECTIVE_SOURCE_IDENTITY_FALSIFICATION_PLUS_LOCAL_NOETHER_PREFILTER
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from .dirac_hypermomentum_irrep import (
    dirac_component_bilinears,
    lower_first_index,
    wheeler_trace_altered_nonmetricity,
)

from .hook17_percacci_sezgin_1plus_projector import (
    exact_ps_1plus_pole_source_gate,
    h17a9_summary,
    torsion_free_ps_source,
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


def a9_provenance_gate() -> dict[str, Any]:
    """Require the completed A9 partial-green state."""

    result = h17a9_summary()

    passed = bool(
        result[
            "partial_green"
        ]
        and
        result[
            "exact_projective_1plus_pole_overlap_established"
        ]
        and
        result[
            "projective_source_trace_constraints_pass"
        ]
        and
        not result[
            "full_diffeomorphism_matter_ward_established"
        ]
        and
        not result[
            "same_action_hook17_complete"
        ]
        and
        not result[
            "hook17_closed"
        ]
    )

    return {
        "a9_decision":
            result[
                "decision"
            ],

        "a9_provenance_pass":
            passed,

        "exact_1plus_pole_overlap":
            result[
                "exact_projective_1plus_pole_overlap_established"
            ],

        "exact_1plus_pole_numerator":
            result[
                "exact_ps_1plus_pole_numerator"
            ],

        "clean_projective_trace_pass":
            result[
                "projective_source_trace_constraints_pass"
            ],

        "same_action_open":
            not result[
                "same_action_hook17_complete"
            ],

        "hook17_open":
            not result[
                "hook17_closed"
            ],
    }


def _wheeler_to_ps_raw_for_spinor(
    spinor: np.ndarray,
) -> np.ndarray:
    """Return the convention-matched raw P&S connection source."""

    response_up = (
        wheeler_trace_altered_nonmetricity(
            spinor
        )
    )

    response_cov = lower_first_index(
        response_up
    )

    hypermomentum_abc = np.transpose(
        response_cov,
        (
            2,
            1,
            0,
        ),
    )

    raw = np.transpose(
        hypermomentum_abc,
        (
            2,
            0,
            1,
        ),
    )

    return np.asarray(
        raw,
        dtype=float,
    )


def ps_torsion_free_source_for_spinor(
    spinor: np.ndarray,
) -> np.ndarray:
    """Project one Wheeler spinor source into P&S torsion-free source space."""

    raw = _wheeler_to_ps_raw_for_spinor(
        spinor
    )

    return (
        0.5
        *
        (
            raw
            +
            np.swapaxes(
                raw,
                0,
                2,
            )
        )
    )


def projective_traces(
    source: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the two P&S projective source traces."""

    tau = np.asarray(
        source,
        dtype=float,
    )

    trace_12 = np.einsum(
        "ij,ijk->k",
        ETA,
        tau,
    )

    trace_23 = np.einsum(
        "jk,ijk->i",
        ETA,
        tau,
    )

    return (
        trace_12,
        trace_23,
    )


def hermitian_spinor_probe_set() -> list[dict[str, Any]]:
    """Return a complete 16-real-direction Hermitian quadratic-form probe set."""

    rows: list[dict[str, Any]] = []

    basis = np.eye(
        4,
        dtype=np.complex128,
    )

    for i in range(
        4
    ):
        rows.append(
            {
                "name":
                    f"D{i}",

                "kind":
                    "DIAGONAL",

                "spinor":
                    basis[
                        i
                    ].copy(),
            }
        )

    for i in range(
        4
    ):
        for j in range(
            i + 1,
            4
        ):
            psi = (
                basis[
                    i
                ]
                +
                basis[
                    j
                ]
            ) / math.sqrt(
                2.0
            )

            rows.append(
                {
                    "name":
                        f"R{i}{j}",

                    "kind":
                        "REAL_CROSS",

                    "spinor":
                        psi,
                }
            )

    for i in range(
        4
    ):
        for j in range(
            i + 1,
            4
        ):
            psi = (
                basis[
                    i
                ]
                +
                1j
                *
                basis[
                    j
                ]
            ) / math.sqrt(
                2.0
            )

            rows.append(
                {
                    "name":
                        f"I{i}{j}",

                    "kind":
                        "IMAG_CROSS",

                    "spinor":
                        psi,
                }
            )

    return rows


def analytic_projective_trace_formula(
    spinor: np.ndarray,
) -> np.ndarray:
    """Independently reconstruct the projected P&S trace from Wheeler bilinears.

    For the implemented Wheeler source and alpha/kappa=1, the two projective
    traces after torsion-free projection are identical.

    The resulting vector is:

        t0 =
            -I_mn + I_mr - I_ns - I_rs - R_mn + R_rs

        t1 =
            2 (D_n - D_r + I_mn - I_nr)

        t2 =
            2 I_mr + I_ms - I_nr + 2 R_nr

        t3 =
            I_mn + 2 I_ms - 2 I_ns + I_rs - R_mr + R_ns.
    """

    bil = dirac_component_bilinears(
        spinor
    )

    d = np.asarray(
        bil[
            "D"
        ],
        dtype=float,
    )

    r = np.asarray(
        bil[
            "R"
        ],
        dtype=float,
    )

    im = np.asarray(
        bil[
            "I"
        ],
        dtype=float,
    )

    dm, dn, dr, ds = map(
        float,
        d,
    )

    del dm
    del ds

    i_mn = float(
        im[
            0,
            1
        ]
    )

    i_mr = float(
        im[
            0,
            2
        ]
    )

    i_ms = float(
        im[
            0,
            3
        ]
    )

    i_nr = float(
        im[
            1,
            2
        ]
    )

    i_ns = float(
        im[
            1,
            3
        ]
    )

    i_rs = float(
        im[
            2,
            3
        ]
    )

    r_mn = float(
        r[
            0,
            1
        ]
    )

    r_mr = float(
        r[
            0,
            2
        ]
    )

    r_nr = float(
        r[
            1,
            2
        ]
    )

    r_ns = float(
        r[
            1,
            3
        ]
    )

    r_rs = float(
        r[
            2,
            3
        ]
    )

    return np.array(
        [
            (
                -i_mn
                +
                i_mr
                -
                i_ns
                -
                i_rs
                -
                r_mn
                +
                r_rs
            ),

            2.0
            *
            (
                dn
                -
                dr
                +
                i_mn
                -
                i_nr
            ),

            (
                2.0
                *
                i_mr
                +
                i_ms
                -
                i_nr
                +
                2.0
                *
                r_nr
            ),

            (
                i_mn
                +
                2.0
                *
                i_ms
                -
                2.0
                *
                i_ns
                +
                i_rs
                -
                r_mr
                +
                r_ns
            ),
        ],
        dtype=float,
    )


def projective_hermitian_probe_rows() -> list[dict[str, Any]]:
    """Evaluate all 16 independent Hermitian source directions."""

    rows: list[dict[str, Any]] = []

    for probe in hermitian_spinor_probe_set():
        source = ps_torsion_free_source_for_spinor(
            probe[
                "spinor"
            ]
        )

        trace_12, trace_23 = projective_traces(
            source
        )

        analytic = analytic_projective_trace_formula(
            probe[
                "spinor"
            ]
        )

        source_norm = float(
            np.linalg.norm(
                source
            )
        )

        norm_12 = float(
            np.linalg.norm(
                trace_12
            )
        )

        norm_23 = float(
            np.linalg.norm(
                trace_23
            )
        )

        reconstruction_error = max(
            float(
                np.linalg.norm(
                    trace_12
                    -
                    analytic
                )
            ),
            float(
                np.linalg.norm(
                    trace_23
                    -
                    analytic
                )
            ),
        )

        compatible = bool(
            norm_12
            <=
            TOL
            *
            max(
                source_norm,
                1.0,
            )
            and
            norm_23
            <=
            TOL
            *
            max(
                source_norm,
                1.0,
            )
        )

        rows.append(
            {
                "name":
                    probe[
                        "name"
                    ],

                "kind":
                    probe[
                        "kind"
                    ],

                "source_norm":
                    source_norm,

                "trace_12":
                    trace_12.tolist(),

                "trace_23":
                    trace_23.tolist(),

                "analytic_trace":
                    analytic.tolist(),

                "trace_12_norm":
                    norm_12,

                "trace_23_norm":
                    norm_23,

                "analytic_reconstruction_error":
                    reconstruction_error,

                "projective_compatible":
                    compatible,
            }
        )

    return rows


def wheeler_projective_source_identity_gate() -> dict[str, Any]:
    """Determine whether projective compatibility is a Wheeler source identity."""

    rows = projective_hermitian_probe_rows()

    failed = [
        row
        for row in rows
        if not row[
            "projective_compatible"
        ]
    ]

    passed = [
        row
        for row in rows
        if row[
            "projective_compatible"
        ]
    ]

    max_trace_norm = max(
        max(
            row[
                "trace_12_norm"
            ],
            row[
                "trace_23_norm"
            ],
        )
        for row in rows
    )

    max_reconstruction_error = max(
        row[
            "analytic_reconstruction_error"
        ]
        for row in rows
    )

    row_map = {
        row[
            "name"
        ]:
            row
        for row in rows
    }

    identity = bool(
        len(
            failed
        )
        ==
        0
    )

    return {
        "hermitian_probe_count":
            len(
                rows
            ),

        "expected_hermitian_dimension":
            16,

        "complete_hermitian_probe_basis":
            bool(
                len(
                    rows
                )
                ==
                16
            ),

        "projective_compatible_probe_count":
            len(
                passed
            ),

        "projective_incompatible_probe_count":
            len(
                failed
            ),

        "projective_compatible_probe_names":
            [
                row[
                    "name"
                ]
                for row in passed
            ],

        "projective_incompatible_probe_names":
            [
                row[
                    "name"
                ]
                for row in failed
            ],

        "maximum_projective_trace_norm":
            max_trace_norm,

        "maximum_analytic_reconstruction_error":
            max_reconstruction_error,

        "analytic_trace_formula_reconstruction_pass":
            bool(
                max_reconstruction_error
                <=
                TOL
            ),

        "d1_trace":
            row_map[
                "D1"
            ][
                "trace_12"
            ],

        "d1_trace_norm":
            row_map[
                "D1"
            ][
                "trace_12_norm"
            ],

        "i01_trace":
            row_map[
                "I01"
            ][
                "trace_12"
            ],

        "i01_trace_norm":
            row_map[
                "I01"
            ][
                "trace_12_norm"
            ],

        "unmodified_wheeler_projective_source_identity":
            identity,

        "clean_state_zero_trace_implies_full_action_identity":
            False,

        "interpretation":
            (
                "PROJECTIVE TRACE IS NOT AN IDENTITY OF THE "
                "UNMODIFIED WHEELER DIRAC SOURCE"
                if not identity
                else
                "PROJECTIVE TRACE VANISHES ON COMPLETE WHEELER "
                "HERMITIAN SOURCE BASIS"
            ),

        "rows":
            rows,
    }


def clean_a9_special_source_gate() -> dict[str, Any]:
    """Preserve the exact favorable A9 clean-state result."""

    a9 = h17a9_summary()
    pole = exact_ps_1plus_pole_source_gate()

    return {
        "clean_projective_trace_pass":
            a9[
                "projective_source_trace_constraints_pass"
            ],

        "clean_exact_1plus_pole_overlap":
            a9[
                "exact_projective_1plus_pole_overlap_established"
            ],

        "clean_exact_1plus_pole_numerator":
            a9[
                "exact_ps_1plus_pole_numerator"
            ],

        "clean_exact_1plus_pole_numerator_nonzero":
            pole[
                "exact_ps_1plus_pole_numerator_nonzero"
            ],

        "clean_source_is_special_projective_subspace_witness":
            True,

        "clean_source_alone_proves_matter_action_projective_invariance":
            False,
    }


def _sigma_unknowns() -> list[tuple[tuple[int, int], int]]:
    """Return independent S_acd unknowns with S_acd=S_cad."""

    pairs = [
        (
            a,
            c,
        )
        for a in range(
            4
        )
        for c in range(
            a,
            4
        )
    ]

    return [
        (
            pair,
            d,
        )
        for pair in pairs
        for d in range(
            4
        )
    ]


def clean_local_sigma_completion_gate() -> dict[str, Any]:
    """Solve the complete local symmetric first-derivative sigma ansatz.

    We impose

        sigma_ac = i S_acd q^d

    with

        S_acd = S_cad.

    The P&S Ward identity becomes

        2 q^a S_acd q^d
        =
        q^a q^b tau_bca.

    Matching all 10 quadratic monomials for every free c gives 40 equations
    for 40 independent S coefficients.
    """

    tau = np.asarray(
        torsion_free_ps_source(),
        dtype=float,
    )

    unknowns = _sigma_unknowns()

    index = {
        item:
            position
        for position, item in enumerate(
            unknowns
        )
    }

    monomials = [
        (
            i,
            j,
        )
        for i in range(
            4
        )
        for j in range(
            i,
            4
        )
    ]

    matrix = np.zeros(
        (
            4
            *
            len(
                monomials
            ),
            len(
                unknowns
            ),
        ),
        dtype=float,
    )

    target = np.zeros(
        4
        *
        len(
            monomials
        ),
        dtype=float,
    )

    row = 0

    for c in range(
        4
    ):
        for i, j in monomials:
            if i == j:
                pair = tuple(
                    sorted(
                        (
                            i,
                            c,
                        )
                    )
                )

                matrix[
                    row,
                    index[
                        (
                            pair,
                            i,
                        )
                    ],
                ] += 2.0

                target[
                    row
                ] = tau[
                    i,
                    c,
                    i,
                ]

            else:
                pair_ic = tuple(
                    sorted(
                        (
                            i,
                            c,
                        )
                    )
                )

                pair_jc = tuple(
                    sorted(
                        (
                            j,
                            c,
                        )
                    )
                )

                matrix[
                    row,
                    index[
                        (
                            pair_ic,
                            j,
                        )
                    ],
                ] += 2.0

                matrix[
                    row,
                    index[
                        (
                            pair_jc,
                            i,
                        )
                    ],
                ] += 2.0

                target[
                    row
                ] = (
                    tau[
                        j,
                        c,
                        i,
                    ]
                    +
                    tau[
                        i,
                        c,
                        j,
                    ]
                )

            row += 1

    solution, _, _, _ = np.linalg.lstsq(
        matrix,
        target,
        rcond=None,
    )

    residual = (
        matrix
        @
        solution
        -
        target
    )

    rank = int(
        np.linalg.matrix_rank(
            matrix
        )
    )

    residual_norm = float(
        np.linalg.norm(
            residual
        )
    )

    max_residual = float(
        np.max(
            np.abs(
                residual
            )
        )
    )

    s_tensor = np.zeros(
        (
            4,
            4,
            4,
        ),
        dtype=float,
    )

    for coefficient, item in zip(
        solution,
        unknowns,
    ):
        (
            a,
            c,
        ), d = item

        s_tensor[
            a,
            c,
            d,
        ] = coefficient

        s_tensor[
            c,
            a,
            d,
        ] = coefficient

    symmetry_error = float(
        np.max(
            np.abs(
                s_tensor
                -
                np.swapaxes(
                    s_tensor,
                    0,
                    1,
                )
            )
        )
    )

    mask = np.ones(
        s_tensor.shape,
        dtype=bool,
    )

    mask[
        0,
        3,
        2,
    ] = False

    mask[
        3,
        0,
        2,
    ] = False

    max_other = float(
        np.max(
            np.abs(
                s_tensor[
                    mask
                ]
            )
        )
    )

    exists = bool(
        max_residual
        <=
        1.0e-10
        and
        symmetry_error
        <=
        TOL
    )

    return {
        "equation_count":
            int(
                matrix.shape[
                    0
                ]
            ),

        "unknown_count":
            int(
                matrix.shape[
                    1
                ]
            ),

        "matrix_rank":
            rank,

        "unique_solution":
            bool(
                rank
                ==
                matrix.shape[
                    1
                ]
            ),

        "residual_norm":
            residual_norm,

        "maximum_polynomial_residual":
            max_residual,

        "sigma_coefficient_symmetry_error":
            symmetry_error,

        "local_first_derivative_symmetric_sigma_completion_exists":
            exists,

        "s_032":
            float(
                s_tensor[
                    0,
                    3,
                    2,
                ]
            ),

        "s_302":
            float(
                s_tensor[
                    3,
                    0,
                    2,
                ]
            ),

        "maximum_other_s_coefficient":
            max_other,

        "inverse_q_used":
            False,

        "inverse_q_squared_used":
            False,

        "nonlocal_repair_used":
            False,

        "solution_tensor":
            s_tensor,

        "hand_solved_sigma_is_wheeler_metric_stress":
            False,
    }


def _connection_ward_term(
    tau: np.ndarray,
    q: np.ndarray,
) -> np.ndarray:
    """Return q^a q^b tau_bca."""

    return np.einsum(
        "a,b,bca->c",
        q,
        q,
        tau,
    )


def local_sigma_ward_witness_gate() -> dict[str, Any]:
    """Verify the polynomial sigma solution on independent momenta."""

    sigma_gate = clean_local_sigma_completion_gate()

    s_tensor = np.asarray(
        sigma_gate[
            "solution_tensor"
        ],
        dtype=float,
    )

    tau = np.asarray(
        torsion_free_ps_source(),
        dtype=float,
    )

    pole = exact_ps_1plus_pole_source_gate()

    witnesses = {
        "MASSIVE_1PLUS_REST":
            np.asarray(
                pole[
                    "q_up"
                ],
                dtype=float,
            ),

        "GENERIC_MIXED":
            np.array(
                [
                    1.0,
                    0.0,
                    1.0,
                    0.0,
                ]
            ),

        "FULL_DIRECTION":
            np.array(
                [
                    0.7,
                    -0.2,
                    0.4,
                    0.9,
                ]
            ),

        "SPATIAL_DIAGONAL":
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

    for name, q in witnesses.items():
        sigma = (
            1j
            *
            np.einsum(
                "acd,d->ac",
                s_tensor,
                q,
            )
        )

        connection = _connection_ward_term(
            tau,
            q,
        )

        metric = (
            2j
            *
            np.einsum(
                "a,ac->c",
                q,
                sigma,
            )
        )

        full = (
            metric
            +
            connection
        )

        residual_norm = float(
            np.linalg.norm(
                full
            )
        )

        rows.append(
            {
                "name":
                    name,

                "q":
                    q.tolist(),

                "connection_term":
                    np.real_if_close(
                        connection
                    ).tolist(),

                "metric_term":
                    np.real_if_close(
                        metric
                    ).tolist(),

                "full_ward_residual":
                    np.real_if_close(
                        full
                    ).tolist(),

                "full_ward_residual_norm":
                    residual_norm,

                "pass":
                    bool(
                        residual_norm
                        <=
                        1.0e-10
                    ),
            }
        )

    return {
        "witness_count":
            len(
                rows
            ),

        "all_witnesses_pass":
            all(
                row[
                    "pass"
                ]
                for row in rows
            ),

        "maximum_witness_residual_norm":
            max(
                row[
                    "full_ward_residual_norm"
                ]
                for row in rows
            ),

        "sigma_is_local_first_derivative":
            True,

        "sigma_is_symmetric":
            bool(
                sigma_gate[
                    "sigma_coefficient_symmetry_error"
                ]
                <=
                TOL
            ),

        "sigma_was_derived_from_wheeler_metric_variation":
            False,

        "rows":
            rows,
    }


def h17a9r1_summary() -> dict[str, Any]:
    """Return conservative A9R1 decision."""

    provenance = a9_provenance_gate()
    projective = wheeler_projective_source_identity_gate()
    clean = clean_a9_special_source_gate()
    sigma = clean_local_sigma_completion_gate()
    witnesses = local_sigma_ward_witness_gate()

    direct_unmodified_closed = bool(
        provenance[
            "a9_provenance_pass"
        ]
        and
        not projective[
            "unmodified_wheeler_projective_source_identity"
        ]
    )

    local_diffeo_completion_exists = bool(
        sigma[
            "local_first_derivative_symmetric_sigma_completion_exists"
        ]
        and
        witnesses[
            "all_witnesses_pass"
        ]
    )

    if direct_unmodified_closed:
        decision = (
            "RED_SCOPED_A9R1_UNMODIFIED_WHEELER_DIRAC_MATTER_"
            "FAILS_PERCACCI_SEZGIN_PROJECTIVE_SOURCE_IDENTITY__"
            "CLEAN_A9_POLE_SURVIVES_AND_PROJECTIVE_MATTER_"
            "COMPLETION_REMAINS_OPEN"
        )

        next_step = (
            "032H17A9R2_PROJECTIVELY_COMPLETED_DIRAC_MATTER_ACTION_GATE"
        )

    elif local_diffeo_completion_exists:
        decision = (
            "GREEN_PARTIAL_A9R1_WHEELER_PROJECTIVE_SOURCE_IDENTITY_"
            "AND_LOCAL_DIFFEO_COMPLETION_EXIST__ACTUAL_METRIC_STRESS_"
            "VARIATION_REMAINS_OPEN"
        )

        next_step = (
            "032H17A9R2_WHEELER_COVARIANT_METRIC_STRESS_VARIATION_GATE"
        )

    else:
        decision = (
            "RED_SCOPED_A9R1_LOCAL_MATTER_NOETHER_PREFLIGHT_FAILED"
        )

        next_step = (
            "032H17_PROJECTIVE_MATTER_COMPLETION_RERANK"
        )

    return {
        "branch":
            "032H17A9R1",

        "subgate":
            "PERCACCI_SEZGIN_WHEELER_SAME_ACTION_MATTER_NOETHER_PREFLIGHT",

        "decision":
            decision,

        "a9_provenance_pass":
            provenance[
                "a9_provenance_pass"
            ],

        "a9_exact_1plus_pole_overlap_preserved":
            clean[
                "clean_exact_1plus_pole_overlap"
            ],

        "a9_exact_1plus_pole_numerator":
            clean[
                "clean_exact_1plus_pole_numerator"
            ],

        "clean_a9_projective_special_state_pass":
            clean[
                "clean_projective_trace_pass"
            ],

        "wheeler_hermitian_probe_count":
            projective[
                "hermitian_probe_count"
            ],

        "wheeler_projective_compatible_probe_count":
            projective[
                "projective_compatible_probe_count"
            ],

        "wheeler_projective_incompatible_probe_count":
            projective[
                "projective_incompatible_probe_count"
            ],

        "maximum_projective_trace_norm":
            projective[
                "maximum_projective_trace_norm"
            ],

        "analytic_projective_trace_reconstruction_pass":
            projective[
                "analytic_trace_formula_reconstruction_pass"
            ],

        "unmodified_wheeler_projective_source_identity":
            projective[
                "unmodified_wheeler_projective_source_identity"
            ],

        "direct_unmodified_wheeler_ps_same_action_closed":
            direct_unmodified_closed,

        "source_state_restriction_alone_accepted_as_gauge_invariance":
            False,

        "local_symmetric_sigma_completion_exists":
            sigma[
                "local_first_derivative_symmetric_sigma_completion_exists"
            ],

        "local_sigma_linear_system_rank":
            sigma[
                "matrix_rank"
            ],

        "local_sigma_unique":
            sigma[
                "unique_solution"
            ],

        "local_sigma_s032":
            sigma[
                "s_032"
            ],

        "local_sigma_max_polynomial_residual":
            sigma[
                "maximum_polynomial_residual"
            ],

        "local_sigma_ward_witnesses_pass":
            witnesses[
                "all_witnesses_pass"
            ],

        "local_sigma_is_same_action_wheeler_metric_stress":
            False,

        "diffeomorphism_local_completion_obstruction":
            not local_diffeo_completion_exists,

        "actual_wheeler_metric_stress_derived":
            False,

        "full_diffeomorphism_matter_ward_established":
            False,

        "projectively_completed_wheeler_matter_action_closed":
            False,

        "full_matter_noether_current_established":
            False,

        "localized_onshell_source_established":
            False,

        "v26b1_metric_numerator_same_action_derived":
            False,

        "same_action_hook17_complete":
            False,

        "universal_physical_metric_established":
            False,

        "finite_payload_antigravity_established":
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

        "capacity_recalculation_authorized":
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
            next_step,

        "next_scientific_question":
            (
                "Can one construct a local covariant projectively invariant "
                "Dirac matter action whose variational hypermomentum "
                "satisfies the P&S trace identities identically, preserves "
                "the clean A9 healthy 1+ pole source, and supplies sigma_ab "
                "from the same variational action?"
            ),

        "claim_scope":
            (
                "UNMODIFIED WHEELER DIRAC MATTER SOURCE VERSUS "
                "PERCACCI-SEZGIN PROJECTIVE SYMMETRY, PLUS A LOCAL "
                "DIFFEOMORPHISM-WARD COMPLETION EXISTENCE PREFILTER"
            ),
    }
