"""032H17A10B — protected spin-one Ward and engineered 1- rerank gate.

PURPOSE
-------
Follow the A10A exact rest-state trace-vector escape with the cheapest
symmetry-level falsification that can distinguish a representation overlap
from a source actually allowed by a protected action.

This module tests two separate questions.

1. BMS totally-symmetric massless spin-one carrier.

   The published rank-two tensor gauge symmetry implies, for a totally
   symmetric source J^{abc}, the momentum-space source identity

       3 q_a J^{abc} - q^{(b} t^{c)} = 0

   with

       t^a = eta_bc J^{abc}.

   We test this first on the two A10A engineered basis pairs and then on the
   complete block-diagonal zero-momentum Dirac rest density-matrix space.

2. Marzo-2022 protected massive 1- carrier.

   A6R2 closed only the historical clean rest pair because its independent
   totally-symmetric and hook 1- representation supports both vanished.

   A10A changes the source state. We therefore test whether its spatial
   totally-symmetric rank-three tensor now contains nonzero spin-one,
   negative-parity representation support.

IMPORTANT CLAIM LIMIT
---------------------
The BMS Ward calculation treats the A10A totally-symmetric Wheeler response
as the candidate current directly coupled to the BMS symmetric rank-three
field.

Failure therefore closes that direct identification in the declared
rest-density source class.

It does not prove that every possible same-action constitutive map from
Dirac hypermomentum to a BMS current is impossible.

Likewise, nonzero Marzo 1- representation support does not establish:

- a same-action source map;
- the complete engineered torsion source;
- the exact physical 1- pole projector;
- a universal physical metric;
- antigravity sign;
- finite-payload stand-off;
- source energy;
- complete operating energy.

SCIENTIFIC STRATEGY
-------------------
This is a theorem-first kill-or-promote gate.

No AGMINER database mutation is authorized.

No energy or geometry optimization is authorized.

CLAIM CLASSIFICATION
--------------------
THEOREM_FIRST_SOURCE_WARD_CLOSEOUT_PLUS_PROTECTED_1MINUS_RERANK
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from typing import Any

import numpy as np
import sympy as sp

from .dirac_hypermomentum_irrep import (
    lower_first_index,
    symmetric_hook_decomposition,
    wheeler_trace_altered_nonmetricity,
)
from .hook17_marzo2022_massive_source_match import (
    marzo2022_published_family_gate,
)
from .hook17_spin_engineered_dirac_source import (
    h17a10a_summary,
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

PAIR_SPECS = {
    "U1_V1":
        (
            0,
            2,
        ),

    "U1_V2":
        (
            0,
            3,
        ),

    "U2_V1":
        (
            1,
            2,
        ),

    "U2_V2":
        (
            1,
            3,
        ),
}

DENSITY_BASIS_LABELS = (
    "P0",
    "P1",
    "PR",
    "PI",
    "A2",
    "A3",
    "AR",
    "AI",
)

SYMMETRIC_INDEX_PAIRS = tuple(
    (
        b,
        c,
    )
    for b in range(
        4
    )
    for c in range(
        b,
        4,
    )
)


def _totally_symmetric_source_for_spinor(
    spinor: np.ndarray,
) -> np.ndarray:
    """Return the fully covariant totally-symmetric Wheeler response piece."""

    q_up = (
        wheeler_trace_altered_nonmetricity(
            spinor
        )
    )

    q_cov = lower_first_index(
        q_up
    )

    pieces = (
        symmetric_hook_decomposition(
            q_cov
        )
    )

    return np.asarray(
        pieces[
            "totally_symmetric"
        ],
        dtype=float,
    )


def engineered_pair_source(
    pair_id: str,
) -> np.ndarray:
    """Return the A10A totally-symmetric source for one rest basis pair."""

    if pair_id not in PAIR_SPECS:
        raise ValueError(
            f"unknown pair_id: {pair_id}"
        )

    (
        particle_index,
        antiparticle_index,
    ) = PAIR_SPECS[
        pair_id
    ]

    basis = np.eye(
        4,
        dtype=np.complex128,
    )

    return (
        _totally_symmetric_source_for_spinor(
            basis[
                particle_index
            ]
        )
        +
        _totally_symmetric_source_for_spinor(
            basis[
                antiparticle_index
            ]
        )
    )


def _raise_all_indices(
    source_cov: np.ndarray,
) -> np.ndarray:
    """Raise all three indices with eta=(-,+,+,+)."""

    source = np.asarray(
        source_cov,
        dtype=float,
    )

    if source.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "source must have shape (4,4,4)"
        )

    return np.einsum(
        "ai,bj,ck,ijk->abc",
        ETA,
        ETA,
        ETA,
        source,
    )


def bms_trace_vector_up(
    source_cov: np.ndarray,
) -> np.ndarray:
    """Return t^a = eta_bc J^{abc} for the candidate BMS current."""

    source_up = _raise_all_indices(
        source_cov
    )

    return np.einsum(
        "bc,abc->a",
        ETA,
        source_up,
    )


def bms_tensor_gauge_ward_residual(
    source_cov: np.ndarray,
    q_cov: np.ndarray
    | list[
        float
    ]
    | tuple[
        float,
        ...
    ],
) -> np.ndarray:
    """Return the exact necessary BMS tensor-gauge source residual.

    The implemented identity is

        W^{bc}
        =
        3 q_a J^{abc}
        -
        q^{(b} t^{c)}

    where parentheses denote symmetrization with factor 1/2.
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

    source_up = _raise_all_indices(
        source_cov
    )

    trace_up = np.einsum(
        "bc,abc->a",
        ETA,
        source_up,
    )

    q_up = (
        ETA
        @
        q
    )

    divergence = (
        3.0
        *
        np.einsum(
            "a,abc->bc",
            q,
            source_up,
        )
    )

    trace_term = (
        0.5
        *
        (
            np.outer(
                q_up,
                trace_up,
            )
            +
            np.outer(
                trace_up,
                q_up,
            )
        )
    )

    residual = (
        divergence
        -
        trace_term
    )

    return (
        0.5
        *
        (
            residual
            +
            residual.T
        )
    )


def engineered_fixed_pair_bms_ward_gate() -> dict[
    str,
    Any,
]:
    """Test the two A10A nonzero basis pairs against the BMS Ward identity."""

    momenta = {
        "NULL_Z":
            np.array(
                [
                    1.0,
                    0.0,
                    0.0,
                    1.0,
                ]
            ),

        "STATIC_Z":
            np.array(
                [
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                ]
            ),
    }

    rows: list[
        dict[
            str,
            Any,
        ]
    ] = []

    for pair_id in (
        "U1_V1",
        "U2_V2",
    ):
        source = engineered_pair_source(
            pair_id
        )

        source_norm = float(
            np.linalg.norm(
                source
            )
        )

        trace_norm = float(
            np.linalg.norm(
                bms_trace_vector_up(
                    source
                )
            )
        )

        for (
            momentum_id,
            q_cov,
        ) in momenta.items():
            residual = (
                bms_tensor_gauge_ward_residual(
                    source,
                    q_cov,
                )
            )

            residual_norm = float(
                np.linalg.norm(
                    residual
                )
            )

            rows.append(
                {
                    "pair_id":
                        pair_id,

                    "momentum_id":
                        momentum_id,

                    "source_norm":
                        source_norm,

                    "trace_norm":
                        trace_norm,

                    "ward_residual_norm":
                        residual_norm,

                    "ward_pass":
                        bool(
                            residual_norm
                            <=
                            TOL
                            *
                            max(
                                source_norm,
                                1.0,
                            )
                        ),
                }
            )

    all_fail = all(
        not row[
            "ward_pass"
        ]
        for row in rows
    )

    minimum_residual = min(
        row[
            "ward_residual_norm"
        ]
        for row in rows
    )

    return {
        "rows":
            rows,

        "both_engineered_pairs_fail_direct_bms_ward":
            bool(
                all_fail
            ),

        "minimum_engineered_ward_residual_norm":
            float(
                minimum_residual
            ),

        "failure_is_numerical_roundoff":
            bool(
                minimum_residual
                <
                1.0e-10
            ),
    }


@lru_cache(
    maxsize=1
)
def _rest_density_basis_sources_cached() -> tuple[
    tuple[
        str,
        np.ndarray,
    ],
    ...,
]:
    """Return the complete 8-real-direction rest density-matrix source basis.

    Each particle/antiparticle 2x2 Hermitian block contributes:

        two population directions
        one real coherence
        one imaginary coherence.

    The resulting eight directions span the complete block-diagonal
    zero-momentum particle/antiparticle rest density-matrix space.
    """

    basis = np.eye(
        4,
        dtype=np.complex128,
    )

    def block_directions(
        i: int,
        j: int,
        prefix: str,
    ) -> list[
        tuple[
            str,
            np.ndarray,
        ]
    ]:
        s_i = (
            _totally_symmetric_source_for_spinor(
                basis[
                    i
                ]
            )
        )

        s_j = (
            _totally_symmetric_source_for_spinor(
                basis[
                    j
                ]
            )
        )

        psi_r = (
            basis[
                i
            ]
            +
            basis[
                j
            ]
        ) / np.sqrt(
            2.0
        )

        psi_i = (
            basis[
                i
            ]
            +
            1j
            *
            basis[
                j
            ]
        ) / np.sqrt(
            2.0
        )

        s_r = (
            _totally_symmetric_source_for_spinor(
                psi_r
            )
            -
            0.5
            *
            s_i
            -
            0.5
            *
            s_j
        )

        s_im = (
            _totally_symmetric_source_for_spinor(
                psi_i
            )
            -
            0.5
            *
            s_i
            -
            0.5
            *
            s_j
        )

        return [
            (
                f"{prefix}{i}",
                s_i,
            ),
            (
                f"{prefix}{j}",
                s_j,
            ),
            (
                f"{prefix}R",
                s_r,
            ),
            (
                f"{prefix}I",
                s_im,
            ),
        ]

    rows = (
        block_directions(
            0,
            1,
            "P",
        )
        +
        block_directions(
            2,
            3,
            "A",
        )
    )

    return tuple(
        (
            label,
            np.asarray(
                source,
                dtype=float,
            ),
        )
        for (
            label,
            (
                _,
                source,
            ),
        )
        in zip(
            DENSITY_BASIS_LABELS,
            rows,
            strict=True,
        )
    )


def rest_density_basis_sources() -> list[
    tuple[
        str,
        np.ndarray,
    ]
]:
    """Return copies of the complete rest density-matrix source basis."""

    return [
        (
            label,
            source.copy(),
        )
        for (
            label,
            source,
        )
        in _rest_density_basis_sources_cached()
    ]


def _fraction_from_float(
    value: float,
) -> Fraction:
    """Recover the exact small rational Wheeler coefficient."""

    fraction = Fraction(
        float(
            value
        )
    ).limit_denominator(
        48
    )

    error = abs(
        float(
            fraction
        )
        -
        float(
            value
        )
    )

    if error > 1.0e-12:
        raise ValueError(
            "source coefficient did not rationalize exactly: "
            +
            repr(
                value
            )
        )

    return fraction


def _sp_rational(
    value: float,
) -> sp.Rational:
    """Return exact SymPy rational form of a repository source coefficient."""

    fraction = _fraction_from_float(
        value
    )

    return sp.Rational(
        fraction.numerator,
        fraction.denominator,
    )


@lru_cache(
    maxsize=1
)
def symbolic_rest_density_bms_matrices() -> tuple[
    tuple[
        sp.Symbol,
        ...,
    ],
    sp.Matrix,
    sp.Matrix,
]:
    """Return exact symbolic BMS Ward matrix A(q) and trace map T.

    A(q) has shape 10x8.

    T has shape 4x8.

    Therefore every possible source in the declared rest-density class is

        J
        =
        sum_i x_i J_i

    and Ward compatibility is

        A(q) x
        =
        0.
    """

    q = sp.symbols(
        "q0 q1 q2 q3"
    )

    eta_sign = (
        -1,
        1,
        1,
        1,
    )

    ward_columns: list[
        list[
            sp.Expr
        ]
    ] = []

    trace_columns: list[
        list[
            sp.Expr
        ]
    ] = []

    for (
        _,
        source_cov_np,
    ) in _rest_density_basis_sources_cached():
        source_cov = [
            [
                [
                    _sp_rational(
                        source_cov_np[
                            a,
                            b,
                            c,
                        ]
                    )
                    for c in range(
                        4
                    )
                ]
                for b in range(
                    4
                )
            ]
            for a in range(
                4
            )
        ]

        source_up = [
            [
                [
                    (
                        sp.Integer(
                            eta_sign[
                                a
                            ]
                            *
                            eta_sign[
                                b
                            ]
                            *
                            eta_sign[
                                c
                            ]
                        )
                        *
                        source_cov[
                            a
                        ][
                            b
                        ][
                            c
                        ]
                    )
                    for c in range(
                        4
                    )
                ]
                for b in range(
                    4
                )
            ]
            for a in range(
                4
            )
        ]

        trace_up = [
            sp.simplify(
                sum(
                    (
                        sp.Integer(
                            eta_sign[
                                b
                            ]
                        )
                        *
                        source_up[
                            a
                        ][
                            b
                        ][
                            b
                        ]
                    )
                    for b in range(
                        4
                    )
                )
            )
            for a in range(
                4
            )
        ]

        q_up = [
            (
                sp.Integer(
                    eta_sign[
                        a
                    ]
                )
                *
                q[
                    a
                ]
            )
            for a in range(
                4
            )
        ]

        ward_values: list[
            sp.Expr
        ] = []

        for (
            b,
            c,
        ) in SYMMETRIC_INDEX_PAIRS:
            divergence = (
                sp.Integer(
                    3
                )
                *
                sum(
                    (
                        q[
                            a
                        ]
                        *
                        source_up[
                            a
                        ][
                            b
                        ][
                            c
                        ]
                    )
                    for a in range(
                        4
                    )
                )
            )

            trace_term = (
                sp.Rational(
                    1,
                    2,
                )
                *
                (
                    q_up[
                        b
                    ]
                    *
                    trace_up[
                        c
                    ]
                    +
                    q_up[
                        c
                    ]
                    *
                    trace_up[
                        b
                    ]
                )
            )

            ward_values.append(
                sp.simplify(
                    divergence
                    -
                    trace_term
                )
            )

        ward_columns.append(
            ward_values
        )

        trace_columns.append(
            trace_up
        )

    ward_matrix = sp.Matrix(
        10,
        8,
        lambda row, column:
            ward_columns[
                column
            ][
                row
            ],
    )

    trace_matrix = sp.Matrix(
        4,
        8,
        lambda row, column:
            trace_columns[
                column
            ][
                row
            ],
    )

    return (
        q,
        ward_matrix,
        trace_matrix,
    )


def _trace_vanishes_on_nullspace(
    ward_matrix: sp.Matrix,
    trace_matrix: sp.Matrix,
) -> tuple[
    bool,
    int,
    int,
    list[
        list[
            str
        ]
    ],
]:
    """Return exact rank/nullity and trace image of every Ward null vector."""

    nullspace = (
        ward_matrix.nullspace()
    )

    images = [
        (
            trace_matrix
            *
            vector
        )
        for vector in nullspace
    ]

    zero = sp.zeros(
        trace_matrix.rows,
        1,
    )

    trace_zero = all(
        image
        ==
        zero
        for image in images
    )

    serialized = [
        [
            str(
                sp.simplify(
                    value
                )
            )
            for value in image
        ]
        for image in images
    ]

    return (
        bool(
            trace_zero
        ),
        int(
            ward_matrix.rank()
        ),
        len(
            nullspace
        ),
        serialized,
    )


@lru_cache(
    maxsize=1
)
def generic_rest_density_bms_ward_theorem() -> dict[
    str,
    Any,
]:
    """Prove that the generic-q Ward-compatible rest-density space is trace silent."""

    (
        _,
        ward_matrix,
        trace_matrix,
    ) = (
        symbolic_rest_density_bms_matrices()
    )

    (
        trace_zero,
        rank,
        nullity,
        images,
    ) = _trace_vanishes_on_nullspace(
        ward_matrix,
        trace_matrix,
    )

    return {
        "rest_density_real_dimension":
            8,

        "generic_symbolic_ward_rank":
            rank,

        "generic_symbolic_ward_nullity":
            nullity,

        "trace_vanishes_on_entire_generic_ward_nullspace":
            trace_zero,

        "generic_trace_images_of_ward_null_basis":
            images,

        "generic_nonzero_trace_escape_exists":
            bool(
                not trace_zero
            ),

        "symbolic_exact_arithmetic":
            True,
    }


def exact_physical_momentum_representatives() -> dict[
    str,
    Any,
]:
    """Test exact null and static momentum representatives.

    The particle and antiparticle 2x2 Hermitian blocks are complete under
    spatial spin rotations.

    The z-axis representatives therefore test the rotationally equivalent
    null/static directions inside the declared rest source class.
    """

    (
        q_symbols,
        ward_matrix,
        trace_matrix,
    ) = (
        symbolic_rest_density_bms_matrices()
    )

    substitutions = {
        "MASSLESS_NULL_Z":
            dict(
                zip(
                    q_symbols,
                    (
                        1,
                        0,
                        0,
                        1,
                    ),
                    strict=True,
                )
            ),

        "STATIC_Z":
            dict(
                zip(
                    q_symbols,
                    (
                        0,
                        0,
                        0,
                        1,
                    ),
                    strict=True,
                )
            ),
    }

    rows: list[
        dict[
            str,
            Any,
        ]
    ] = []

    for (
        momentum_id,
        subs,
    ) in substitutions.items():
        matrix = (
            ward_matrix.subs(
                subs
            )
        )

        (
            trace_zero,
            rank,
            nullity,
            images,
        ) = _trace_vanishes_on_nullspace(
            matrix,
            trace_matrix,
        )

        rows.append(
            {
                "momentum_id":
                    momentum_id,

                "ward_rank":
                    rank,

                "ward_nullity":
                    nullity,

                "trace_vanishes_on_ward_nullspace":
                    trace_zero,

                "trace_images":
                    images,
            }
        )

    return {
        "rows":
            rows,

        "all_physical_representatives_trace_silent":
            bool(
                all(
                    row[
                        "trace_vanishes_on_ward_nullspace"
                    ]
                    for row in rows
                )
            ),

        "rest_density_basis_is_full_two_by_two_hermitian_per_sector":
            True,

        "rest_density_basis_closed_under_spatial_spin_rotations":
            True,
    }


def compact_localized_bms_rest_density_closeout() -> dict[
    str,
    Any,
]:
    """Close the direct compact localized BMS trace-vector rest-density route.

    For compact spatial support, Fourier amplitudes are analytic.

    If the exact BMS Ward identity forces the protected trace amplitude to
    vanish on the generic open momentum set, exceptional lower-dimensional
    momentum strata cannot by themselves support a compact localized
    nonzero trace source.
    """

    generic = (
        generic_rest_density_bms_ward_theorem()
    )

    representatives = (
        exact_physical_momentum_representatives()
    )

    closed = bool(
        generic[
            "trace_vanishes_on_entire_generic_ward_nullspace"
        ]
        and
        representatives[
            "all_physical_representatives_trace_silent"
        ]
    )

    return {
        "generic_open_set_trace_zero":
            generic[
                "trace_vanishes_on_entire_generic_ward_nullspace"
            ],

        "massless_and_static_representatives_trace_zero":
            representatives[
                "all_physical_representatives_trace_silent"
            ],

        "compact_support_fourier_amplitudes_analytic":
            True,

        "exceptional_momentum_strata_can_rescue_compact_trace_source":
            (
                False
                if closed
                else None
            ),

        "direct_bms_trace_vector_rest_density_route_closed":
            closed,

        "closure_scope":
            (
                "DIRECT_IDENTIFICATION_OF_THE_WHEELER_TOTALLY_SYMMETRIC_"
                "RESPONSE_WITH_THE_BMS_CURRENT_FOR_BLOCK_DIAGONAL_ZERO_"
                "MOMENTUM_DIRAC_REST_DENSITY_SOURCES"
            ),

        "nonrest_momentum_bearing_dirac_sources_closed":
            False,

        "new_compensated_or_constitutive_source_maps_closed":
            False,

        "bms_family_globally_closed":
            False,
    }


def engineered_totally_symmetric_1minus_gate() -> dict[
    str,
    Any,
]:
    """Test negative-parity spin-one representation support of A10A states.

    In the rest-frame totally-symmetric rank-three sector, S_ijk has odd
    parity.

    Its 3D trace

        v_i = S_ijj

    is the spatial spin-one component.

    The traceless remainder is spin three.
    """

    delta = np.eye(
        3
    )

    rows: list[
        dict[
            str,
            Any,
        ]
    ] = []

    for pair_id in (
        "U1_V1",
        "U2_V2",
    ):
        source = engineered_pair_source(
            pair_id
        )

        s00i = source[
            0,
            0,
            1:,
        ]

        sijk = source[
            1:,
            1:,
            1:,
        ]

        vector = np.einsum(
            "ijj->i",
            sijk,
        )

        spin1 = np.zeros(
            (
                3,
                3,
                3,
            ),
            dtype=float,
        )

        for i in range(
            3
        ):
            for j in range(
                3
            ):
                for k in range(
                    3
                ):
                    spin1[
                        i,
                        j,
                        k,
                    ] = (
                        delta[
                            i,
                            j
                        ]
                        *
                        vector[
                            k
                        ]
                        +
                        delta[
                            i,
                            k
                        ]
                        *
                        vector[
                            j
                        ]
                        +
                        delta[
                            j,
                            k
                        ]
                        *
                        vector[
                            i
                        ]
                    ) / 5.0

        spin3 = (
            sijk
            -
            spin1
        )

        rows.append(
            {
                "pair_id":
                    pair_id,

                "s00i_norm":
                    float(
                        np.linalg.norm(
                            s00i
                        )
                    ),

                "sijk_norm":
                    float(
                        np.linalg.norm(
                            sijk
                        )
                    ),

                "spatial_spin1_trace_vector":
                    vector.tolist(),

                "spatial_spin1_trace_norm":
                    float(
                        np.linalg.norm(
                            vector
                        )
                    ),

                "spatial_spin1_tensor_norm":
                    float(
                        np.linalg.norm(
                            spin1
                        )
                    ),

                "spatial_spin3_stf_norm":
                    float(
                        np.linalg.norm(
                            spin3
                        )
                    ),

                "totally_symmetric_1minus_representation_support_nonzero":
                    bool(
                        np.linalg.norm(
                            vector
                        )
                        >
                        TOL
                    ),

                "exact_physical_1minus_pole_projector_evaluated":
                    False,
            }
        )

    return {
        "rows":
            rows,

        "both_engineered_pairs_have_nonzero_symmetric_1minus_representation":
            bool(
                all(
                    row[
                        "totally_symmetric_1minus_representation_support_nonzero"
                    ]
                    for row in rows
                )
            ),

        "historical_a6r2_clean_pair_zero_generalizes_to_engineered_states":
            False,

        "representation_support_is_exact_pole_overlap":
            False,
    }


def h17a10b_summary() -> dict[
    str,
    Any,
]:
    """Return the scoped A10B closeout and next protected-carrier target."""

    a10a = h17a10a_summary()

    family = (
        marzo2022_published_family_gate()
    )

    fixed = (
        engineered_fixed_pair_bms_ward_gate()
    )

    generic = (
        generic_rest_density_bms_ward_theorem()
    )

    localized = (
        compact_localized_bms_rest_density_closeout()
    )

    one_minus = (
        engineered_totally_symmetric_1minus_gate()
    )

    bms_closed = bool(
        fixed[
            "both_engineered_pairs_fail_direct_bms_ward"
        ]
        and
        generic[
            "trace_vanishes_on_entire_generic_ward_nullspace"
        ]
        and
        localized[
            "direct_bms_trace_vector_rest_density_route_closed"
        ]
    )

    marzo_reopened = bool(
        one_minus[
            "both_engineered_pairs_have_nonzero_symmetric_1minus_representation"
        ]
    )

    decision = (
        (
            "RED_SCOPED_A10B_DIRECT_BMS_REST_DENSITY_TRACE_ROUTE_CLOSED__"
            "GREEN_MARZO2022_ENGINEERED_1MINUS_REPRESENTATION_REOPENED"
        )
        if (
            bms_closed
            and
            marzo_reopened
        )
        else
        "YELLOW_A10B_REQUIRES_REVIEW"
    )

    return {
        "branch":
            "032H17A10B",

        "decision":
            decision,

        "a10a_source_state_escape_preserved":
            bool(
                a10a[
                    "partial_green"
                ]
            ),

        "current_full_regression_before_a10b":
            918,

        "exact_bms_tensor_gauge_ward_operator_evaluated":
            True,

        "bms_fixed_engineered_pair_direct_ward_fails":
            fixed[
                "both_engineered_pairs_fail_direct_bms_ward"
            ],

        "bms_generic_rest_density_ward_rank":
            generic[
                "generic_symbolic_ward_rank"
            ],

        "bms_generic_rest_density_ward_nullity":
            generic[
                "generic_symbolic_ward_nullity"
            ],

        "bms_generic_ward_compatible_trace_escape_exists":
            generic[
                "generic_nonzero_trace_escape_exists"
            ],

        "bms_compact_localized_rest_density_trace_route_closed":
            localized[
                "direct_bms_trace_vector_rest_density_route_closed"
            ],

        "bms_global_family_closed":
            False,

        "marzo2022_protected_family_published":
            bool(
                family[
                    "explicit_metric_affine_action_published"
                ]
                and
                family[
                    "protecting_abelian_symmetry_published"
                ]
            ),

        "marzo2022_unique_massive_physical_pole_sector":
            family[
                "published_massive_physical_pole_sector"
            ],

        "marzo2022_engineered_1minus_representation_reopened":
            marzo_reopened,

        "marzo2022_exact_same_action_source_ward_established":
            False,

        "marzo2022_exact_physical_1minus_pole_overlap_established":
            False,

        "engineered_full_torsion_source_reconstructed":
            False,

        "universal_physical_metric_established":
            False,

        "finite_payload_outward_response_established":
            False,

        "complete_energy_established":
            False,

        "energy_optimization_authorized":
            False,

        "geometry_optimization_authorized":
            False,

        "agminer_database_mutation_authorized":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "hook17_closed":
            False,

        "next":
            (
                "032H17A10C_MARZO2022_ENGINEERED_1MINUS_"
                "SAME_ACTION_SOURCE_WARD_TORSION_AND_EXACT_POLE_PROJECTOR_GATE"
            ),

        "stop_rule_after_next":
            (
                "IF_ENGINEERED_SOURCE_FAILS_MARZO_SAME_ACTION_WARD_OR_EXACT_"
                "1MINUS_POLE_PROJECTOR_CLOSE_THIS_REST_STATE_PROTECTED_SPIN1_"
                "RESCUE_AND_RETURN_TO_A9R3_ONLY_WITH_A_GENUINELY_NEW_"
                "PROTECTED_FAMILY"
            ),

        "fixed_pair_ward_gate":
            fixed,

        "generic_rest_density_ward_theorem":
            generic,

        "localized_bms_closeout":
            localized,

        "engineered_1minus_gate":
            one_minus,
    }
