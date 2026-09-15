"""032H17A11C — exact finite-transfer Wheeler/Dirac -> K2 source theorem.

PURPOSE
-------
Close or promote the last direct ordinary-Dirac Wheeler -> K2 loophole left by
A11B without a momentum scan.

A11B proved that every K2-Ward-compatible zero-momentum Hermitian Dirac rest
density maps to zero Wheeler torsion source. It deliberately left open
momentum-bearing on-shell bilinears. This module treats that class exactly.

COVARIANT REDUCTION
-------------------
For equal-mass same-frequency on-shell matrix elements, every nonzero transfer
q = p' - p is spacelike. Lorentz covariance permits the Breit frame

    q  = (0, 0, 0, Q)
    p  = (E, 0, 0, -Q/2)
    p' = (E, 0, 0, +Q/2)

with z = tanh(eta/2), so every finite nonzero transfer is 0 < z < 1 and

    E/m = (1 + z^2)/(1 - z^2)
    Q/m = 4 z/(1 - z^2).

A common nonzero spinor normalization is omitted because all source constraints
are homogeneous. The continuum problem therefore becomes an exact polynomial
rank theorem in z.

FULL K2 SOURCE SUBSPACE
-----------------------
The K2 action of Barker, Marzo and Santoni is Maxwell-like in the polar trace
vector K^d{}_{mu d}. A pair-antisymmetric source has 24 components. K2 source
admissibility removes the 20 components orthogonal to the trace-vector
subspace, and current conservation adds one more independent constraint,
leaving three source components. This reconstructs the 21 source constraints
reported for K2 in their Figure 6.

For the all-upper source J^{a b c}, define A^c = J^{b c}{}_b. The full K2
source conditions are

    J^{a b c} = -(1/3)(eta^{a b} A^c - eta^{a c} A^b)
    q_c A^c = 0.

The single covariant A11B Ward equation is necessary but is not sufficient once
particle and antiparticle non-rest source textures can cancel one another.

SOURCE CLASS
------------
The basis contains all four complex spin-transition bilinears in the positive-
energy block and all four in the negative-energy block at fixed Breit transfer.
Arbitrary complex linear combinations are allowed. Positive/negative-frequency
interference is excluded because it carries nonzero energy transfer of order
2E and is not stationary in this free on-shell class.

FALSIFIER
---------
If one exact 8x8 minor of the full K2 constraint matrix is nonzero for every
0 < z < 1, the matrix has full column rank throughout the physical domain and
no nonzero source in the declared class is K2-admissible. Then the direct
ordinary-Dirac Wheeler -> K2 route closes before pole, metric, payload,
geometry or energy work.

CLAIM LIMITS
------------
A red result does not close K2 with a different microscopic source,
derivative/composite currents, Noether/compensator completions,
interacting/bound-state Dirac sources outside the declared free class, other
protected torsion-vector families, or HOOK17 globally.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from typing import Any

import numpy as np
import sympy as sp

from .hook17_k2_wheeler_torsion_ward import (
    h17a11b_summary,
    rest_density_torsion_basis,
    wheeler_full_torsion_response,
)

ETA_SIGNS = (-1, 1, 1, 1)
TRANSITION_LABELS = (
    "P_UU", "P_UD", "P_DU", "P_DD",
    "A_UU", "A_UD", "A_DU", "A_DD",
)
FULL_K2_WITNESS_ROWS = (1, 2, 3, 6, 17, 27, 35, 39)


def _small_rational(value: float) -> sp.Rational:
    """Recover exact small rational coefficients from the A11B basis."""

    fraction = Fraction(float(value)).limit_denominator(64)

    if abs(float(fraction) - float(value)) > 1.0e-10:
        raise ValueError(
            "failed rational reconstruction: "
            + repr(value)
        )

    return sp.Rational(
        fraction.numerator,
        fraction.denominator,
    )


@lru_cache(maxsize=1)
def wheeler_torsion_operator_tensor() -> tuple:
    """Reconstruct exact Hermitian operators M[a,b,c] from A11B.

    Wheeler's source is quadratic in a four-spinor,

        J[a,b,c](psi) = psi^dagger M[a,b,c] psi.

    The complete 16-real-dimensional Hermitian density basis already built by
    A11B uniquely determines every 4x4 Hermitian M[a,b,c]. This gives the exact
    sesquilinear transition source <psi_out|M|psi_in> needed at p' != p.
    """

    rows = dict(
        rest_density_torsion_basis()
    )

    operators = [
        [
            [
                sp.zeros(4, 4)
                for _ in range(4)
            ]
            for _ in range(4)
        ]
        for _ in range(4)
    ]

    for alpha in range(4):
        for beta in range(4):
            for gamma in range(4):
                matrix = sp.zeros(4, 4)

                for index in range(4):
                    matrix[index, index] = _small_rational(
                        rows[
                            f"D{index}"
                        ][
                            alpha,
                            beta,
                            gamma,
                        ]
                    )

                for first in range(4):
                    for second in range(
                        first + 1,
                        4,
                    ):
                        real_part = _small_rational(
                            rows[
                                f"R{first}{second}"
                            ][
                                alpha,
                                beta,
                                gamma,
                            ]
                        )

                        # For A11B's
                        # (e_i + i e_j)/sqrt(2)
                        # convention:
                        #
                        # I_ij = -Im(M_ij).
                        imag_direction = _small_rational(
                            rows[
                                f"I{first}{second}"
                            ][
                                alpha,
                                beta,
                                gamma,
                            ]
                        )

                        matrix[
                            first,
                            second,
                        ] = (
                            real_part
                            - sp.I * imag_direction
                        )

                        matrix[
                            second,
                            first,
                        ] = (
                            real_part
                            + sp.I * imag_direction
                        )

                operators[
                    alpha
                ][
                    beta
                ][
                    gamma
                ] = matrix

    return tuple(
        tuple(
            tuple(
                operators[
                    alpha
                ][
                    beta
                ][
                    gamma
                ]
                for gamma in range(4)
            )
            for beta in range(4)
        )
        for alpha in range(4)
    )


def operator_reconstruction_validation() -> dict[str, Any]:
    """Check the reconstructed operator map against Wheeler's direct map."""

    operators = wheeler_torsion_operator_tensor()

    probes = (
        np.array(
            [1.0, 0.0, 0.0, 0.0],
            dtype=np.complex128,
        ),
        np.array(
            [0.0, 1.0, 0.0, 1.0j],
            dtype=np.complex128,
        ),
        np.array(
            [1.0, -2.0j, 0.5, 1.5j],
            dtype=np.complex128,
        ),
    )

    maximum_error = 0.0

    for spinor in probes:
        reconstructed = np.zeros(
            (4, 4, 4),
            dtype=np.complex128,
        )

        for alpha in range(4):
            for beta in range(4):
                for gamma in range(4):
                    matrix = np.asarray(
                        operators[
                            alpha
                        ][
                            beta
                        ][
                            gamma
                        ].tolist(),
                        dtype=np.complex128,
                    )

                    reconstructed[
                        alpha,
                        beta,
                        gamma,
                    ] = (
                        np.conjugate(
                            spinor
                        )
                        @ matrix
                        @ spinor
                    )

        direct = (
            wheeler_full_torsion_response(
                spinor
            )
        )

        maximum_error = max(
            maximum_error,
            float(
                np.max(
                    np.abs(
                        reconstructed
                        - direct
                    )
                )
            ),
        )

    return {
        "operator_reconstruction_pass":
            maximum_error < 1.0e-12,

        "maximum_operator_reconstruction_error":
            maximum_error,

        "transition_matrix_element_extension":
            True,
    }


def _breit_spinors(
    z: sp.Symbol,
) -> dict[
    str,
    dict[
        str,
        sp.Matrix,
    ],
]:
    """Return unnormalised exact Breit-frame particle/antiparticle spinors."""

    return {
        "particle_in": {
            "U":
                sp.Matrix(
                    [1, 0, -z, 0]
                ),

            "D":
                sp.Matrix(
                    [0, 1, 0, z]
                ),
        },

        "particle_out": {
            "U":
                sp.Matrix(
                    [1, 0, z, 0]
                ),

            "D":
                sp.Matrix(
                    [0, 1, 0, -z]
                ),
        },

        "antiparticle_in": {
            "U":
                sp.Matrix(
                    [-z, 0, 1, 0]
                ),

            "D":
                sp.Matrix(
                    [0, z, 0, 1]
                ),
        },

        "antiparticle_out": {
            "U":
                sp.Matrix(
                    [z, 0, 1, 0]
                ),

            "D":
                sp.Matrix(
                    [0, -z, 0, 1]
                ),
        },
    }


def _transition_source(
    outgoing: sp.Matrix,
    incoming: sp.Matrix,
) -> sp.MutableDenseNDimArray:
    """Return the exact Wheeler transition source <out|M|in>."""

    operators = (
        wheeler_torsion_operator_tensor()
    )

    source = (
        sp.MutableDenseNDimArray.zeros(
            4,
            4,
            4,
        )
    )

    bra = (
        sp.conjugate(
            outgoing
        ).T
    )

    for alpha in range(4):
        for beta in range(4):
            for gamma in range(4):
                source[
                    alpha,
                    beta,
                    gamma,
                ] = sp.expand(
                    (
                        bra
                        * operators[
                            alpha
                        ][
                            beta
                        ][
                            gamma
                        ]
                        * incoming
                    )[
                        0
                    ]
                )

    return source


@lru_cache(maxsize=1)
def breit_transition_source_basis() -> tuple:
    """Return all eight complex same-frequency spin transitions at fixed q."""

    z = sp.symbols(
        "z",
        real=True,
    )

    spinors = (
        _breit_spinors(
            z
        )
    )

    sources = []

    blocks = (
        (
            "P",
            "particle_in",
            "particle_out",
        ),
        (
            "A",
            "antiparticle_in",
            "antiparticle_out",
        ),
    )

    transitions = (
        ("U", "U"),
        ("U", "D"),
        ("D", "U"),
        ("D", "D"),
    )

    for (
        prefix,
        incoming_key,
        outgoing_key,
    ) in blocks:
        for (
            outgoing_spin,
            incoming_spin,
        ) in transitions:
            label = (
                f"{prefix}_"
                f"{outgoing_spin}"
                f"{incoming_spin}"
            )

            sources.append(
                (
                    label,
                    _transition_source(
                        spinors[
                            outgoing_key
                        ][
                            outgoing_spin
                        ],
                        spinors[
                            incoming_key
                        ][
                            incoming_spin
                        ],
                    ),
                )
            )

    if (
        tuple(
            label
            for label, _ in sources
        )
        !=
        TRANSITION_LABELS
    ):
        raise AssertionError(
            "unexpected transition-source ordering"
        )

    return tuple(
        sources
    )


def _raise_antisymmetric_pair(
    source: sp.MutableDenseNDimArray,
) -> sp.MutableDenseNDimArray:
    """Raise the last pair with eta=(-,+,+,+), matching A11B."""

    raised = (
        sp.MutableDenseNDimArray.zeros(
            4,
            4,
            4,
        )
    )

    for alpha in range(4):
        for beta in range(4):
            for gamma in range(4):
                raised[
                    alpha,
                    beta,
                    gamma,
                ] = sp.simplify(
                    ETA_SIGNS[
                        beta
                    ]
                    *
                    ETA_SIGNS[
                        gamma
                    ]
                    *
                    source[
                        alpha,
                        beta,
                        gamma,
                    ]
                )

    return raised


def _k2_trace_vector_and_remainder(
    source: sp.MutableDenseNDimArray,
) -> tuple[
    list[
        sp.Expr
    ],
    list[
        sp.Expr
    ],
]:
    """Return A^mu and the source component orthogonal to K2's trace vector."""

    raised = (
        _raise_antisymmetric_pair(
            source
        )
    )

    trace = [
        sp.simplify(
            sum(
                ETA_SIGNS[
                    beta
                ]
                *
                raised[
                    beta,
                    chi,
                    beta,
                ]
                for beta in range(4)
            )
        )
        for chi in range(4)
    ]

    remainder = []

    for alpha in range(4):
        for beta in range(4):
            for gamma in range(4):
                eta_ab = (
                    ETA_SIGNS[
                        alpha
                    ]
                    if alpha == beta
                    else 0
                )

                eta_ag = (
                    ETA_SIGNS[
                        alpha
                    ]
                    if alpha == gamma
                    else 0
                )

                pure_trace = (
                    -sp.Rational(
                        1,
                        3,
                    )
                    *
                    (
                        eta_ab
                        * trace[
                            gamma
                        ]
                        -
                        eta_ag
                        * trace[
                            beta
                        ]
                    )
                )

                remainder.append(
                    sp.simplify(
                        raised[
                            alpha,
                            beta,
                            gamma,
                        ]
                        -
                        pure_trace
                    )
                )

    return (
        trace,
        remainder,
    )


@lru_cache(maxsize=1)
def k2_full_source_constraint_count_validation() -> dict[str, Any]:
    """Independently reconstruct K2's published 21 source constraints."""

    labels = [
        (
            alpha,
            beta,
            gamma,
        )
        for alpha in range(4)
        for beta in range(4)
        for gamma in range(
            beta + 1,
            4,
        )
    ]

    variables = sp.symbols(
        "j0:"
        +
        str(
            len(
                labels
            )
        ),
        real=True,
    )

    source = (
        sp.MutableDenseNDimArray.zeros(
            4,
            4,
            4,
        )
    )

    # Choose mixed components so that raising
    # the last pair yields generic all-upper
    # pair-antisymmetric source variables.
    for (
        variable,
        (
            alpha,
            beta,
            gamma,
        ),
    ) in zip(
        variables,
        labels,
    ):
        mixed = (
            ETA_SIGNS[
                beta
            ]
            *
            ETA_SIGNS[
                gamma
            ]
            *
            variable
        )

        source[
            alpha,
            beta,
            gamma,
        ] = mixed

        source[
            alpha,
            gamma,
            beta,
        ] = (
            -mixed
        )

    (
        trace,
        remainder,
    ) = (
        _k2_trace_vector_and_remainder(
            source
        )
    )

    pure_trace_matrix = (
        sp.Matrix(
            [
                [
                    sp.expand(
                        expression
                    ).coeff(
                        variable
                    )
                    for variable in variables
                ]
                for expression in remainder
            ]
        )
    )

    full_matrix = (
        pure_trace_matrix.col_join(
            sp.Matrix(
                [
                    [
                        sp.expand(
                            trace[
                                3
                            ]
                        ).coeff(
                            variable
                        )
                        for variable in variables
                    ]
                ]
            )
        )
    )

    pure_rank = int(
        pure_trace_matrix.rank()
    )

    full_rank = int(
        full_matrix.rank()
    )

    return {
        "pair_antisymmetric_source_dimension":
            len(
                labels
            ),

        "trace_vector_subspace_dimension":
            len(
                labels
            )
            -
            pure_rank,

        "pure_trace_constraint_rank":
            pure_rank,

        "current_conservation_additional_rank":
            full_rank
            -
            pure_rank,

        "full_k2_independent_constraint_rank":
            full_rank,

        "k2_admissible_source_dimension_at_nonzero_breit_q":
            len(
                labels
            )
            -
            full_rank,

        "published_k2_total_source_constraint_count":
            21,

        "published_constraint_count_match":
            full_rank
            ==
            21,

        "exact_linear_algebra":
            True,
    }


@lru_cache(maxsize=1)
def full_k2_constraint_matrix() -> sp.Matrix:
    """Return 65x8 exact K2 constraints on the A11C transition basis."""

    columns = []

    for (
        _,
        source,
    ) in (
        breit_transition_source_basis()
    ):
        (
            trace,
            remainder,
        ) = (
            _k2_trace_vector_and_remainder(
                source
            )
        )

        # In the static Breit frame q is
        # nonzero and parallel to z, so q.A=0
        # is equivalent to A^3=0 up to a
        # common nonzero q magnitude.
        columns.append(
            remainder
            +
            [
                sp.simplify(
                    trace[
                        3
                    ]
                )
            ]
        )

    return sp.Matrix(
        65,
        8,
        lambda row, column:
            columns[
                column
            ][
                row
            ],
    )


def _a11b_necessary_ward_vector(
    source: sp.MutableDenseNDimArray,
) -> sp.Matrix:
    """Return the weaker A11B covariant Ward projection in the Breit frame."""

    raised = (
        _raise_antisymmetric_pair(
            source
        )
    )

    trace = [
        sp.simplify(
            sum(
                ETA_SIGNS[
                    beta
                ]
                *
                raised[
                    beta,
                    chi,
                    beta,
                ]
                for beta in range(4)
            )
        )
        for chi in range(4)
    ]

    residual = []

    for alpha in range(4):
        third = (
            sp.simplify(
                raised[
                    3,
                    alpha,
                    3,
                ]
            )
        )

        # q_cov=q_up=(0,0,0,1),
        # q^2=1 after dropping a common
        # nonzero transfer scale.
        residual.append(
            sp.factor(
                3
                *
                (
                    1
                    if alpha == 3
                    else 0
                )
                *
                trace[
                    3
                ]
                +
                trace[
                    alpha
                ]
                -
                3
                *
                third
            )
        )

    return sp.Matrix(
        residual
    )


@lru_cache(maxsize=1)
def necessary_ward_matrix() -> sp.Matrix:
    """Return the 4x8 A11B necessary-Ward matrix for the non-rest basis."""

    return sp.Matrix.hstack(
        *[
            _a11b_necessary_ward_vector(
                source
            )
            for _, source in (
                breit_transition_source_basis()
            )
        ]
    )


def _factor_string(
    expression: sp.Expr,
) -> str:
    """Return a stable exact factorization string."""

    return str(
        sp.factor(
            expression
        )
    )


@lru_cache(maxsize=1)
def exact_breit_k2_theorem() -> dict[str, Any]:
    """Prove whether any finite nonzero on-shell Wheeler source survives K2."""

    z = sp.symbols(
        "z",
        real=True,
    )

    necessary = (
        necessary_ward_matrix()
    )

    full = (
        full_k2_constraint_matrix()
    )

    particle_det = sp.factor(
        necessary[
            :,
            0:4,
        ].det()
    )

    antiparticle_det = sp.factor(
        necessary[
            :,
            4:8,
        ].det()
    )

    necessary_rank = int(
        necessary.rank()
    )

    necessary_nullspace = (
        necessary.nullspace()
    )

    source_basis = (
        breit_transition_source_basis()
    )

    source_matrix = sp.Matrix(
        64,
        8,
        lambda row, column:
            source_basis[
                column
            ][
                1
            ][
                row // 16,
                (row // 4) % 4,
                row % 4,
            ],
    )

    if necessary_nullspace:
        null_matrix = (
            sp.Matrix.hstack(
                *necessary_nullspace
            )
        )

        necessary_source_image_rank = int(
            (
                source_matrix
                *
                null_matrix
            ).rank()
        )
    else:
        necessary_source_image_rank = 0

    witness = full[
        list(
            FULL_K2_WITNESS_ROWS
        ),
        :,
    ]

    witness_det = sp.factor(
        witness.det()
    )

    expected_witness = sp.factor(
        z**2
        *
        (z - 1) ** 4
        *
        (z + 1) ** 4
        *
        (z**2 + 1) ** 2
        /
        sp.Integer(
            2592
        )
    )

    witness_identity_pass = bool(
        sp.simplify(
            witness_det
            -
            expected_witness
        )
        ==
        0
    )

    roots_inside = []

    for root in sp.solve(
        sp.Eq(
            witness_det,
            0,
        ),
        z,
    ):
        if root.is_real is True:
            numeric = float(
                sp.N(
                    root
                )
            )

            if (
                0.0
                <
                numeric
                <
                1.0
            ):
                roots_inside.append(
                    str(
                        root
                    )
                )

    sample_rows = []

    for sample in (
        sp.Rational(1, 10),
        sp.Rational(1, 4),
        sp.Rational(1, 2),
        sp.Rational(3, 4),
        sp.Rational(9, 10),
    ):
        matrix = full.subs(
            z,
            sample,
        )

        sample_rows.append(
            {
                "z":
                    str(
                        sample
                    ),

                "q_over_m":
                    str(
                        sp.simplify(
                            4
                            *
                            sample
                            /
                            (
                                1
                                -
                                sample**2
                            )
                        )
                    ),

                "full_k2_constraint_rank":
                    int(
                        matrix.rank()
                    ),

                "full_k2_nullity":
                    int(
                        matrix.cols
                        -
                        matrix.rank()
                    ),

                "witness_minor":
                    str(
                        sp.factor(
                            witness_det.subs(
                                z,
                                sample,
                            )
                        )
                    ),
            }
        )

    zero_matrix = full.subs(
        z,
        0,
    )

    infinite_rapidity_matrix = full.subs(
        z,
        1,
    )

    no_finite_nonzero_escape = bool(
        witness_identity_pass
        and
        not roots_inside
    )

    return {
        "breit_parameter":
            "z=tanh(eta/2)",

        "finite_nonzero_spacelike_transfer_domain":
            "0<z<1",

        "energy_over_mass":
            "(1+z^2)/(1-z^2)",

        "transfer_over_mass":
            "4*z/(1-z^2)",

        "transition_complex_dimension":
            8,

        "positive_negative_frequency_cross_terms_stationary":
            False,

        "operator_reconstruction":
            operator_reconstruction_validation(),

        "k2_constraint_count_validation":
            k2_full_source_constraint_count_validation(),

        "particle_only_necessary_ward_determinant":
            _factor_string(
                particle_det
            ),

        "antiparticle_only_necessary_ward_determinant":
            _factor_string(
                antiparticle_det
            ),

        "combined_necessary_ward_rank":
            necessary_rank,

        "combined_necessary_ward_nullity":
            necessary.cols
            -
            necessary_rank,

        "combined_necessary_ward_source_image_rank":
            necessary_source_image_rank,

        "necessary_ward_nonzero_survivors_exist":
            bool(
                necessary.cols
                -
                necessary_rank
                >
                0
                and
                necessary_source_image_rank
                >
                0
            ),

        "full_k2_constraint_row_count":
            65,

        "full_k2_independent_constraint_count":
            21,

        "full_k2_witness_rows":
            list(
                FULL_K2_WITNESS_ROWS
            ),

        "full_k2_witness_determinant":
            _factor_string(
                witness_det
            ),

        "full_k2_witness_identity_pass":
            witness_identity_pass,

        "full_k2_witness_real_roots_inside_0_1":
            roots_inside,

        "full_k2_rank_is_eight_for_every_finite_nonzero_transfer":
            no_finite_nonzero_escape,

        "nonzero_full_k2_admissible_onshell_dirac_source_exists":
            bool(
                not no_finite_nonzero_escape
            ),

        "sample_rank_checks":
            sample_rows,

        "z0_full_constraint_rank":
            int(
                zero_matrix.rank()
            ),

        "z0_full_constraint_nullity":
            int(
                zero_matrix.cols
                -
                zero_matrix.rank()
            ),

        "z0_interpretation":
            "ZERO_MOMENTUM_TRANSFER_NO_STANDOFF_GRADIENT",

        "z1_full_constraint_rank":
            int(
                infinite_rapidity_matrix.rank()
            ),

        "z1_full_constraint_nullity":
            int(
                infinite_rapidity_matrix.cols
                -
                infinite_rapidity_matrix.rank()
            ),

        "z1_interpretation":
            "INFINITE_RAPIDITY_INFINITE_Q_OVER_M_BOUNDARY",

        "symbolic_exact_arithmetic":
            True,

        "lorentz_covariant_breit_reduction":
            True,

        "full_k2_source_subspace_enforced":
            True,

        "closure_scope":
            (
                "COMPLETE_STATIONARY_FREE_EQUAL_MASS_ONSHELL_BLOCK_DIAGONAL_"
                "PARTICLE_PLUS_ANTIPARTICLE_DIRAC_BILINEAR_CLASS_WITH_"
                "UNMODIFIED_WHEELER_TORSION_SOURCE"
            ),
    }


@lru_cache(maxsize=1)
def h17a11c_summary() -> dict[str, Any]:
    """Return the scoped A11C theorem-first closeout summary."""

    a11b = (
        h17a11b_summary()
    )

    theorem = (
        exact_breit_k2_theorem()
    )

    provenance = bool(
        a11b[
            "direct_k2_rest_density_wheeler_route_closed"
        ]
        and
        a11b[
            "hook17_closed"
        ]
        is False
    )

    direct_route_closed = bool(
        provenance
        and
        theorem[
            "operator_reconstruction"
        ][
            "operator_reconstruction_pass"
        ]
        and
        theorem[
            "k2_constraint_count_validation"
        ][
            "published_constraint_count_match"
        ]
        and
        theorem[
            "necessary_ward_nonzero_survivors_exist"
        ]
        and
        theorem[
            "full_k2_rank_is_eight_for_every_finite_nonzero_transfer"
        ]
        and
        theorem[
            "nonzero_full_k2_admissible_onshell_dirac_source_exists"
        ]
        is False
    )

    decision = (
        (
            "RED_SCOPED_A11C_DIRECT_K2_ORDINARY_DIRAC_ONSHELL_"
            "WHEELER_ROUTE_CLOSED__PROMOTE_GENUINELY_NEW_PROTECTED_"
            "SOURCE_FAMILY"
        )
        if direct_route_closed
        else
        "YELLOW_A11C_K2_ONSHELL_SOURCE_REQUIRES_REVIEW"
    )

    return {
        "branch":
            "032H17A11C",

        "decision":
            decision,

        "a11b_provenance":
            provenance,

        "exact_breit_k2_theorem":
            theorem,

        "important_intermediate_fact_a11b_necessary_ward_can_be_cancelled_nonrest":
            theorem[
                "necessary_ward_nonzero_survivors_exist"
            ],

        "important_final_fact_full_k2_constraints_remove_all_finite_nonzero_survivors":
            theorem[
                "full_k2_rank_is_eight_for_every_finite_nonzero_transfer"
            ],

        "direct_k2_ordinary_dirac_onshell_wheeler_route_closed":
            direct_route_closed,

        "k2_with_other_microscopic_sources_closed":
            False,

        "derivative_or_composite_source_completions_closed":
            False,

        "noether_compensated_source_completions_closed":
            False,

        "interacting_bound_state_dirac_sources_closed":
            False,

        "all_massless_torsion_vector_families_closed":
            False,

        "healthy_pole_evaluation_authorized":
            False,

        "metric_gate_authorized":
            False,

        "payload_gate_authorized":
            False,

        "energy_optimization_authorized":
            False,

        "hook17_closed":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "next":
            (
                "032H17A12_PROTECTED_SOURCE_FAMILY_RERANK_AFTER_DIRECT_K2_"
                "ORDINARY_DIRAC_CLOSEOUT"
                if direct_route_closed
                else
                "REVIEW_A11C_FULL_K2_SOURCE_SUBSPACE"
            ),

        "stop_rule":
            (
                "DO_NOT_RUN_K2_METRIC_PAYLOAD_GEOMETRY_OR_ENERGY_FOR_THE_"
                "CLOSED_DIRECT_ORDINARY_DIRAC_WHEELER_SOURCE;_ONLY_REOPEN_"
                "K2_WITH_A_GENUINELY_NEW_MICROSCOPIC_SOURCE_OR_NOETHER_"
                "COMPLETION"
            ),
    }
