"""HOOK17 J11 common-Ward theorem and minimal compensator prefilter.

PURPOSE
-------
Advance 032H17A6 after the 032H17A5 direct-K3 source-Ward
falsification.

The current bottleneck is not HOOK17 field capacity.  It is whether the
actual intrinsic V24 Dirac source can live on the source-Ward surface of a
healthy symmetry-protected carrier while retaining productive 1+ support.

This module performs three theorem-first tests.

1. J11 COMMON-WARD TEST

   Barker, Marzo, and Santoni arXiv:2507.05349 define the protected J11
   pair-antisymmetric rank-three model by the kinetic relations

       kappa15 = 0
       kappa16 = 0
       kappa2  = 0
       kappa4  = -2 kappa3
       kappa6  = -kappa3
       kappa7  = 0
       kappa9  = -kappa3 / 2

   with all quadratic mass coefficients zero.

   K3 obeys the same displayed relations and additionally imposes

       kappa1 = 0.

   Thus K3 is the kappa1=0 specialization of the relevant J11 coefficient
   surface.

   The H17A5 necessary Ward condition is

       q_chi q_beta J^{beta alpha chi} = 0.

   The corresponding gauge generator may be represented in momentum space
   as

       delta K_{beta alpha chi}
       =
       q_beta
       (
           q_chi xi_alpha
           -
           q_alpha xi_chi
       ).

   The only additional J11 kinetic operator relative to K3 is

       O1
       =
       partial_beta K^delta_{ chi delta}
       partial^chi K^alpha_{ alpha}^beta.

   Pair antisymmetry makes this proportional in Fourier space to the square
   of the divergence of the simple trace vector

       B_mu = K^alpha_{ alpha mu}.

   Under the Ward generator,

       delta B_mu
       =
       q_mu (q.xi)
       -
       q^2 xi_mu,

   and therefore

       q^mu delta B_mu = 0.

   Hence O1 is invariant under this particular K3 gauge generator.

   This means freeing kappa1 does NOT remove this necessary Ward identity.
   J11 may have less total gauge symmetry than K3, but this specific
   A5 source-Ward generator survives.

   The actual V24 current is then tested against that surviving necessary
   identity.

2. ALGEBRAIC VECTOR / AXIAL IMPROVEMENT PREFILTER

   A pair-antisymmetric rank-three tensor contains lower-rank vector and
   axial-vector irreducible embeddings.  At zero derivatives these can be
   written schematically as

       I_{a[bc]}
       =
       eta_ab C_c
       -
       eta_ac C_b

   and

       I_{a[bc]}
       =
       epsilon_abcd A^d.

   The module asks whether ANY constant C or A can make the complete Ward
   polynomial of the fixed clean-rest-pair V24 tensor vanish identically.

   This is a linear coefficient-space theorem, not a momentum scan.

3. PURE STUECKELBERG GAUGE-IMAGE PREFILTER

   A source correction proportional only to the gauge image

       I^{beta alpha chi}
       =
       q^beta
       (
           q^chi C^alpha
           -
           q^alpha C^chi
       )

   has Ward image proportional to q^2.  On the massless lightlike pole it
   therefore cannot cancel the exact nonzero H17A5 V24 residual.

SCIENTIFIC SCOPE
----------------
A negative result from this module closes only:

    DIRECT CLEAN V24 -> J11

plus the declared minimal compensator subclasses:

    FIXED-TENSOR ZERO-DERIVATIVE VECTOR/AXIAL IMPROVEMENT

and:

    PURE GAUGE-IMAGE STUECKELBERG SOURCE REPAIR.

It does NOT close:

- a genuinely dynamical same-action hook compensator;
- a Higgsed hook carrier;
- a full Noether-complete matter-plus-compensator source;
- momentum-dependent Dirac source-state engineering;
- position-dependent spinor textures;
- other protected metric-affine vector families;
- protected 2+ families;
- V26D DHOST/KMM.

NO ENERGY OPTIMIZATION
----------------------
The approximately 17.0676442196 J quantity remains only the preserved
R_P=1e12 canonical field-capacity reference.

This module does not modify or optimize it.

CLAIM CLASSIFICATION
--------------------
THEOREM_FIRST_SCOPED_SOURCE_WARD_FALSIFICATION_AND_COMPENSATOR_PREFILTER
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .hook17_protected_k3_ward import (
    ETA,
    TOL,
    bms_helicity_prefilter,
    k3_ward_counterexample_gate,
    k3_ward_residual,
    minkowski_q2,
    raise_all_indices,
    v24_bms_current,
)


HOOK17_REFERENCE_CAPACITY_RP1E12_J = 17.0676442196
STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7

ARXIV_ID = "2507.05349"


def j11_catalogue_gate() -> dict[str, Any]:
    """Encode only the exact catalogue facts needed by the theorem.

    The relations below are the J11 row of Table II in
    Barker-Marzo-Santoni arXiv:2507.05349.

    K3 is obtained on the relevant branch by adding kappa1_4 = 0.
    """

    j11_relations = {
        "kappa15_4":
            "0",

        "kappa16_4":
            "0",

        "kappa2_4":
            "0",

        "kappa4_4":
            "-2*kappa3_4",

        "kappa6_4":
            "-kappa3_4",

        "kappa7_4":
            "0",

        "kappa9_4":
            "-0.5*kappa3_4",

        "kappa1_2":
            "0",

        "kappa2_2":
            "0",

        "kappa3_2":
            "0",
    }

    return {
        "family":
            "BARKER_MARZO_SANTONI_J11",

        "arxiv":
            ARXIV_ID,

        "field":
            "PAIR_ANTISYMMETRIC_RANK3_K_a_bc",

        "parity_conserving":
            True,

        "published_unitary_case":
            True,

        "published_propagating_sector":
            "AXIAL_VECTOR_EVEN_PARITY_1PLUS",

        "published_description":
            "AXIAL_VECTOR_WITH_LESS_CONSTRAINING_SYMMETRY_THAN_K3",

        "j11_relations":
            j11_relations,

        "j11_free_kinetic_parameters_relevant_here":
            [
                "kappa1_4",
                "kappa3_4",
            ],

        "table_ii_deconfliction":
            (
                "kappa3_4=0 OR kappa1_4=0 "
                "moves to a more specialized catalogue node"
            ),

        "k3_additional_constraint":
            "kappa1_4=0",

        "k3_is_j11_kappa1_zero_specialization":
            True,

        "complete_j11_source_constraint_set_reconstructed_here":
            False,

        "one_shared_necessary_ward_is_enough_for_direct_falsification":
            True,
    }


def _minkowski_dot_cov(
    left_cov: np.ndarray,
    right_cov: np.ndarray,
) -> float:
    """Return left_mu eta^{mu nu} right_nu in the repository signature."""

    left = np.asarray(
        left_cov,
        dtype=float,
    )

    right = np.asarray(
        right_cov,
        dtype=float,
    )

    return float(
        left
        @
        ETA
        @
        right
    )


def common_generator_invariance_gate() -> dict[str, Any]:
    """Verify that the A5 Ward generator leaves the J11 O1 term invariant.

    Let

        B_mu = K^alpha_{ alpha mu}.

    Under

        delta K_{beta alpha chi}
        =
        q_beta
        (
            q_chi xi_alpha
            -
            q_alpha xi_chi
        )

    one obtains

        delta B_mu
        =
        q_mu (q.xi)
        -
        q^2 xi_mu.

    Therefore

        q^mu delta B_mu = 0.

    Since the extra J11 kappa1 operator depends on the longitudinal
    trace-vector contraction, this particular K3 gauge generator remains
    an exact symmetry after kappa1 is restored.
    """

    witnesses = [
        (
            np.array(
                [
                    2.0,
                    1.0,
                    3.0,
                    4.0,
                ]
            ),
            np.array(
                [
                    1.0,
                    2.0,
                    -1.0,
                    3.0,
                ]
            ),
        ),
        (
            np.array(
                [
                    3.0,
                    0.0,
                    1.0,
                    2.0,
                ]
            ),
            np.array(
                [
                    -2.0,
                    1.0,
                    4.0,
                    0.0,
                ]
            ),
        ),
        (
            np.array(
                [
                    1.0,
                    0.0,
                    0.0,
                    1.0,
                ]
            ),
            np.array(
                [
                    0.0,
                    2.0,
                    1.0,
                    -3.0,
                ]
            ),
        ),
    ]

    rows: list[dict[str, Any]] = []

    for q_cov, xi_cov in witnesses:
        q_up = (
            ETA
            @
            q_cov
        )

        q2 = float(
            q_cov
            @
            q_up
        )

        q_dot_xi = (
            _minkowski_dot_cov(
                q_cov,
                xi_cov,
            )
        )

        delta_b_cov = (
            q_cov
            *
            q_dot_xi
            -
            q2
            *
            xi_cov
        )

        divergence = float(
            q_up
            @
            delta_b_cov
        )

        rows.append(
            {
                "q_cov":
                    q_cov.tolist(),

                "xi_cov":
                    xi_cov.tolist(),

                "q2":
                    q2,

                "q_dot_delta_B":
                    divergence,

                "passes":
                    bool(
                        abs(
                            divergence
                        )
                        <=
                        TOL
                    ),
            }
        )

    max_abs = max(
        abs(
            row[
                "q_dot_delta_B"
            ]
        )
        for row in rows
    )

    return {
        "generator":
            (
                "delta K_{beta alpha chi}="
                "q_beta(q_chi xi_alpha-q_alpha xi_chi)"
            ),

        "trace_vector":
            "B_mu=K^alpha_{ alpha mu}",

        "delta_trace_vector":
            (
                "delta B_mu="
                "q_mu(q.xi)-q^2 xi_mu"
            ),

        "exact_identity":
            "q^mu delta B_mu=0",

        "extra_j11_operator":
            (
                "kappa1_4 "
                "partial_beta K^delta_{ chi delta} "
                "partial^chi K^alpha_{ alpha}^beta"
            ),

        "extra_operator_depends_on_longitudinal_trace":
            True,

        "common_generator_survives_j11_kappa1_operator":
            bool(
                max_abs
                <=
                TOL
            ),

        "max_numeric_identity_residual":
            float(
                max_abs
            ),

        "witnesses":
            rows,

        "this_is_complete_j11_gauge_reconstruction":
            False,

        "this_is_one_exact_shared_necessary_generator":
            True,
    }


def ward_coefficient_tensor(
    current_cov: np.ndarray,
) -> np.ndarray:
    """Return symmetric coefficient matrices for W^a(q).

    For

        W^a(q)
        =
        q_c q_b J^{b a c},

    return C[a,b,c] symmetric in b,c such that

        W^a
        =
        C[a,b,c] q_b q_c.
    """

    current = np.asarray(
        current_cov,
        dtype=float,
    )

    if current.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "current_cov must have shape (4,4,4)"
        )

    current_up = (
        raise_all_indices(
            current
        )
    )

    coeff = np.zeros(
        (
            4,
            4,
            4,
        ),
        dtype=float,
    )

    for alpha in range(
        4
    ):
        for beta in range(
            4
        ):
            for chi in range(
                4
            ):
                coeff[
                    alpha,
                    beta,
                    chi,
                ] = (
                    0.5
                    *
                    (
                        current_up[
                            beta,
                            alpha,
                            chi,
                        ]
                        +
                        current_up[
                            chi,
                            alpha,
                            beta,
                        ]
                    )
                )

    return coeff


def evaluate_ward_coefficients(
    coeff: np.ndarray,
    q_cov: np.ndarray,
) -> np.ndarray:
    """Evaluate a stored quadratic Ward polynomial."""

    q = np.asarray(
        q_cov,
        dtype=float,
    )

    return np.einsum(
        "abc,b,c->a",
        coeff,
        q,
        q,
    )


def _flatten_symmetric_coefficients(
    coeff: np.ndarray,
) -> np.ndarray:
    """Flatten independent symmetric momentum-polynomial coefficients."""

    values: list[float] = []

    for alpha in range(
        4
    ):
        for beta in range(
            4
        ):
            for chi in range(
                beta,
                4,
            ):
                values.append(
                    float(
                        coeff[
                            alpha,
                            beta,
                            chi,
                        ]
                    )
                )

    return np.asarray(
        values,
        dtype=float,
    )


def direct_j11_v24_gate() -> dict[str, Any]:
    """Apply the surviving common Ward identity to the actual V24 source."""

    common = (
        common_generator_invariance_gate()
    )

    old_ward = (
        k3_ward_counterexample_gate()
    )

    helicity = (
        bms_helicity_prefilter()
    )

    rows = (
        old_ward[
            "rows"
        ]
    )

    any_failure = any(
        not row[
            "passes_necessary_ward"
        ]
        for row in rows.values()
    )

    return {
        "common_generator_survives_j11":
            common[
                "common_generator_survives_j11_kappa1_operator"
            ],

        "necessary_j11_common_ward":
            (
                "q_chi q_beta "
                "J^{beta alpha chi}=0"
            ),

        "lightlike_z_q2":
            rows[
                "LIGHTLIKE_Z"
            ][
                "q2"
            ],

        "lightlike_z_residual":
            rows[
                "LIGHTLIKE_Z"
            ][
                "residual"
            ],

        "lightlike_z_residual_norm":
            rows[
                "LIGHTLIKE_Z"
            ][
                "residual_norm"
            ],

        "at_least_one_exact_counterexample":
            any_failure,

        "direct_clean_v24_j11_ward_compatible":
            bool(
                common[
                    "common_generator_survives_j11_kappa1_operator"
                ]
                and
                not any_failure
            ),

        "direct_clean_v24_j11_closed":
            bool(
                common[
                    "common_generator_survives_j11_kappa1_operator"
                ]
                and
                any_failure
            ),

        "productive_1plus_representation_overlap_survives":
            helicity[
                "spin1_helicity_seed_nonzero"
            ],

        "productive_1plus_seed_norm2":
            helicity[
                "spin1_helicity_seed_norm2"
            ],

        "closure_scope":
            (
                "DIRECT CLEAN V24 REST-PAIR CURRENT "
                "AND COMMON FIXED-TENSOR SCALAR ENVELOPE "
                "IN BMS J11"
            ),

        "all_protected_1plus_closed":
            False,
    }


def _trace_vector_embedding(
    vector_cov: np.ndarray,
) -> np.ndarray:
    """Return eta_ab C_c - eta_ac C_b."""

    vector = np.asarray(
        vector_cov,
        dtype=float,
    )

    current = np.zeros(
        (
            4,
            4,
            4,
        ),
        dtype=float,
    )

    for alpha in range(
        4
    ):
        for beta in range(
            4
        ):
            for chi in range(
                4
            ):
                current[
                    alpha,
                    beta,
                    chi,
                ] = (
                    ETA[
                        alpha,
                        beta,
                    ]
                    *
                    vector[
                        chi
                    ]
                    -
                    ETA[
                        alpha,
                        chi,
                    ]
                    *
                    vector[
                        beta
                    ]
                )

    return current


def _levi_civita4(
    a: int,
    b: int,
    c: int,
    d: int,
) -> float:
    """Return epsilon_abcd with epsilon_0123=+1."""

    indices = [
        a,
        b,
        c,
        d,
    ]

    if len(
        set(
            indices
        )
    ) != 4:
        return 0.0

    inversions = 0

    for i in range(
        4
    ):
        for j in range(
            i + 1,
            4,
        ):
            if (
                indices[
                    i
                ]
                >
                indices[
                    j
                ]
            ):
                inversions += 1

    return (
        -1.0
        if inversions
        %
        2
        else
        1.0
    )


def _axial_vector_embedding(
    vector: np.ndarray,
) -> np.ndarray:
    """Return epsilon_abcd A^d."""

    axial = np.asarray(
        vector,
        dtype=float,
    )

    current = np.zeros(
        (
            4,
            4,
            4,
        ),
        dtype=float,
    )

    for alpha in range(
        4
    ):
        for beta in range(
            4
        ):
            for chi in range(
                4
            ):
                current[
                    alpha,
                    beta,
                    chi,
                ] = sum(
                    _levi_civita4(
                        alpha,
                        beta,
                        chi,
                        delta,
                    )
                    *
                    axial[
                        delta
                    ]
                    for delta in range(
                        4
                    )
                )

    return current


def minimal_vector_improvement_gate() -> dict[str, Any]:
    """Solve the complete zero-derivative vector/axial improvement problem.

    The test is polynomial, not pointwise in momentum.

    The forty independent coefficients of the four quadratic Ward
    polynomials are assembled into one linear vector space.

    We then ask whether a constant trace vector C_mu and/or axial vector
    A_mu can make every polynomial coefficient vanish.
    """

    base_current = (
        v24_bms_current()
    )

    target = (
        -
        _flatten_symmetric_coefficients(
            ward_coefficient_tensor(
                base_current
            )
        )
    )

    trace_columns: list[
        np.ndarray
    ] = []

    axial_columns: list[
        np.ndarray
    ] = []

    for index in range(
        4
    ):
        basis = np.zeros(
            4,
            dtype=float,
        )

        basis[
            index
        ] = 1.0

        trace_columns.append(
            _flatten_symmetric_coefficients(
                ward_coefficient_tensor(
                    _trace_vector_embedding(
                        basis
                    )
                )
            )
        )

        axial_columns.append(
            _flatten_symmetric_coefficients(
                ward_coefficient_tensor(
                    _axial_vector_embedding(
                        basis
                    )
                )
            )
        )

    trace_matrix = np.column_stack(
        trace_columns
    )

    axial_matrix = np.column_stack(
        axial_columns
    )

    combined_matrix = np.column_stack(
        [
            trace_matrix,
            axial_matrix,
        ]
    )

    trace_solution, _, _, _ = (
        np.linalg.lstsq(
            trace_matrix,
            target,
            rcond=None,
        )
    )

    combined_solution, _, _, _ = (
        np.linalg.lstsq(
            combined_matrix,
            target,
            rcond=None,
        )
    )

    trace_residual = float(
        np.linalg.norm(
            trace_matrix
            @
            trace_solution
            -
            target
        )
    )

    combined_residual = float(
        np.linalg.norm(
            combined_matrix
            @
            combined_solution
            -
            target
        )
    )

    target_norm = float(
        np.linalg.norm(
            target
        )
    )

    axial_map_norm = float(
        np.linalg.norm(
            axial_matrix
        )
    )

    trace_rank = int(
        np.linalg.matrix_rank(
            trace_matrix,
            tol=
                TOL,
        )
    )

    combined_rank = int(
        np.linalg.matrix_rank(
            combined_matrix,
            tol=
                TOL,
        )
    )

    return {
        "source":
            "ACTUAL_FIXED_CLEAN_V24_BMS_CURRENT",

        "ward_polynomial_coefficient_dimension":
            int(
                target.size
            ),

        "target_ward_coefficient_norm":
            target_norm,

        "trace_vector_parameter_dimension":
            4,

        "trace_vector_ward_map_rank":
            trace_rank,

        "trace_vector_best_fit_coefficients":
            trace_solution.tolist(),

        "trace_vector_best_residual_norm":
            trace_residual,

        "trace_vector_exact_repair_exists":
            bool(
                trace_residual
                <=
                TOL
            ),

        "axial_vector_parameter_dimension":
            4,

        "axial_vector_ward_map_norm":
            axial_map_norm,

        "axial_vector_is_ward_silent":
            bool(
                axial_map_norm
                <=
                TOL
            ),

        "combined_vector_axial_ward_map_rank":
            combined_rank,

        "combined_best_fit_coefficients":
            combined_solution.tolist(),

        "combined_best_residual_norm":
            combined_residual,

        "combined_exact_repair_exists":
            bool(
                combined_residual
                <=
                TOL
            ),

        "minimal_vector_axial_fixed_tensor_repair_closed":
            bool(
                combined_residual
                >
                TOL
            ),

        "closure_scope":
            (
                "ZERO-DERIVATIVE TRACE-VECTOR PLUS AXIAL-VECTOR "
                "IRREDUCIBLE IMPROVEMENTS OF THE FIXED V24 TENSOR"
            ),

        "dynamical_hook_compensator_closed":
            False,

        "momentum_dependent_spinor_texture_closed":
            False,
    }


def gauge_image_ward_residual(
    q_cov: np.ndarray,
    compensator_contra: np.ndarray,
) -> np.ndarray:
    """Return the Ward image of a pure gauge-image source correction.

    For

        I^{b a c}
        =
        q^b
        (
            q^c C^a
            -
            q^a C^c
        )

    the Ward image is

        q^2
        [
            q^2 C^a
            -
            q^a (q.C)
        ].
    """

    q = np.asarray(
        q_cov,
        dtype=float,
    )

    compensator = np.asarray(
        compensator_contra,
        dtype=float,
    )

    q_up = (
        ETA
        @
        q
    )

    q2 = float(
        q
        @
        q_up
    )

    q_dot_c = float(
        q
        @
        compensator
    )

    return (
        q2
        *
        (
            q2
            *
            compensator
            -
            q_up
            *
            q_dot_c
        )
    )


def pure_stueckelberg_gate() -> dict[str, Any]:
    """Show that a pure gauge-image correction cannot fix the pole witness."""

    q = np.array(
        [
            1.0,
            0.0,
            0.0,
            1.0,
        ]
    )

    base_residual = (
        k3_ward_residual(
            q
        )
    )

    correction_norms: list[
        float
    ] = []

    for index in range(
        4
    ):
        compensator = np.zeros(
            4,
            dtype=float,
        )

        compensator[
            index
        ] = 1.0

        correction_norms.append(
            float(
                np.linalg.norm(
                    gauge_image_ward_residual(
                        q,
                        compensator,
                    )
                )
            )
        )

    max_correction_norm = max(
        correction_norms
    )

    base_norm = float(
        np.linalg.norm(
            base_residual
        )
    )

    return {
        "q_cov":
            q.tolist(),

        "q2":
            minkowski_q2(
                q
            ),

        "v24_residual":
            base_residual.tolist(),

        "v24_residual_norm":
            base_norm,

        "max_basis_gauge_image_ward_norm":
            max_correction_norm,

        "pure_gauge_image_is_ward_silent_on_massless_pole":
            bool(
                max_correction_norm
                <=
                TOL
            ),

        "pure_stueckelberg_gauge_image_can_cancel_v24_pole_residual":
            bool(
                max_correction_norm
                >
                TOL
                and
                base_norm
                <=
                TOL
            ),

        "pure_stueckelberg_without_independent_dynamics_is_rescue":
            False,

        "dynamical_compensator_with_independent_equations_closed":
            False,

        "interpretation":
            (
                "A pure gauge-image Stückelberg redundancy cannot cancel "
                "the exact nonzero V24 lightlike Ward witness. "
                "A genuinely dynamical same-action compensator remains open."
            ),
    }


def ward_polynomial_reconstruction_gate() -> dict[str, Any]:
    """Independently reconstruct the A5 residuals from polynomial coefficients."""

    coeff = (
        ward_coefficient_tensor(
            v24_bms_current()
        )
    )

    witnesses = {
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

    max_difference = 0.0

    for name, q in witnesses.items():
        reconstructed = (
            evaluate_ward_coefficients(
                coeff,
                q,
            )
        )

        direct = (
            k3_ward_residual(
                q
            )
        )

        difference = float(
            np.linalg.norm(
                reconstructed
                -
                direct
            )
        )

        max_difference = max(
            max_difference,
            difference,
        )

        rows[
            name
        ] = {
            "reconstructed":
                reconstructed.tolist(),

            "direct":
                direct.tolist(),

            "difference_norm":
                difference,
        }

    return {
        "rows":
            rows,

        "max_difference_norm":
            float(
                max_difference
            ),

        "independent_polynomial_reconstruction_pass":
            bool(
                max_difference
                <=
                TOL
            ),
    }


def compensator_prefilter_rows() -> list[dict[str, Any]]:
    """Return human-readable candidate rows for CSV persistence."""

    direct = (
        direct_j11_v24_gate()
    )

    minimal = (
        minimal_vector_improvement_gate()
    )

    stueckelberg = (
        pure_stueckelberg_gate()
    )

    return [
        {
            "candidate":
                "DIRECT_CLEAN_V24_TO_J11",

            "status":
                "RED_SCOPED",

            "ward_residual_norm":
                direct[
                    "lightlike_z_residual_norm"
                ],

            "locality":
                "LOCAL",

            "same_action_status":
                "DIRECT_SOURCE_TEST",

            "productive_1plus":
                direct[
                    "productive_1plus_representation_overlap_survives"
                ],

            "closure_scope":
                direct[
                    "closure_scope"
                ],
        },
        {
            "candidate":
                "ZERO_DERIVATIVE_TRACE_VECTOR_IMPROVEMENT",

            "status":
                "RED_SCOPED",

            "ward_residual_norm":
                minimal[
                    "trace_vector_best_residual_norm"
                ],

            "locality":
                "LOCAL",

            "same_action_status":
                "ALGEBRAIC_PREFILTER_ONLY",

            "productive_1plus":
                "NOT_PROMOTED",

            "closure_scope":
                (
                    "FIXED_V24_TENSOR_PLUS_CONSTANT_TRACE_VECTOR"
                ),
        },
        {
            "candidate":
                "ZERO_DERIVATIVE_AXIAL_VECTOR_IMPROVEMENT",

            "status":
                "RED_SCOPED",

            "ward_residual_norm":
                minimal[
                    "target_ward_coefficient_norm"
                ],

            "locality":
                "LOCAL",

            "same_action_status":
                "ALGEBRAIC_PREFILTER_ONLY",

            "productive_1plus":
                "NOT_PROMOTED",

            "closure_scope":
                (
                    "AXIAL_VECTOR_EMBEDDING_IS_WARD_SILENT"
                ),
        },
        {
            "candidate":
                "PURE_STUECKELBERG_GAUGE_IMAGE",

            "status":
                "RED_SCOPED",

            "ward_residual_norm":
                stueckelberg[
                    "v24_residual_norm"
                ],

            "locality":
                "LOCAL_FORMAL_GAUGE_IMAGE",

            "same_action_status":
                "NO_INDEPENDENT_COMPENSATOR_DYNAMICS",

            "productive_1plus":
                "NOT_PROMOTED",

            "closure_scope":
                (
                    "PURE_GAUGE_IMAGE_ONLY"
                ),
        },
        {
            "candidate":
                "DYNAMICAL_SAME_ACTION_HOOK_COMPENSATOR",

            "status":
                "OPEN_NEXT",

            "ward_residual_norm":
                "",

            "locality":
                "MUST_BE_PROVED",

            "same_action_status":
                "NOT_YET_CONSTRUCTED",

            "productive_1plus":
                "MUST_REMAIN_NONZERO",

            "closure_scope":
                (
                    "NOT_CLOSED_BY_H17A6_PREFILTER"
                ),
        },
    ]


def h17a6_summary() -> dict[str, Any]:
    """Return the conservative scientific decision for this A6 subgate."""

    catalogue = (
        j11_catalogue_gate()
    )

    common = (
        common_generator_invariance_gate()
    )

    direct = (
        direct_j11_v24_gate()
    )

    polynomial = (
        ward_polynomial_reconstruction_gate()
    )

    minimal = (
        minimal_vector_improvement_gate()
    )

    stueckelberg = (
        pure_stueckelberg_gate()
    )

    direct_red = bool(
        catalogue[
            "k3_is_j11_kappa1_zero_specialization"
        ]
        and
        common[
            "common_generator_survives_j11_kappa1_operator"
        ]
        and
        direct[
            "direct_clean_v24_j11_closed"
        ]
    )

    minimal_red = bool(
        minimal[
            "minimal_vector_axial_fixed_tensor_repair_closed"
        ]
        and
        stueckelberg[
            "pure_gauge_image_is_ward_silent_on_massless_pole"
        ]
    )

    return {
        "branch":
            "032H17A6",

        "subgate":
            (
                "J11_COMMON_WARD_AND_MINIMAL_COMPENSATOR_PREFILTER"
            ),

        "decision":
            (
                "RED_SCOPED_H17A6_DIRECT_J11_AND_MINIMAL_"
                "VECTOR_STUECKELBERG_REPAIRS_FAIL__"
                "DYNAMICAL_SAME_ACTION_COMPENSATOR_REMAINS_OPEN"
            ),

        "j11_catalogue_relation_reconstructed":
            True,

        "k3_is_j11_kappa1_zero_specialization":
            catalogue[
                "k3_is_j11_kappa1_zero_specialization"
            ],

        "a5_common_ward_generator_survives_j11":
            common[
                "common_generator_survives_j11_kappa1_operator"
            ],

        "ward_polynomial_independent_reconstruction":
            polynomial[
                "independent_polynomial_reconstruction_pass"
            ],

        "direct_clean_v24_to_j11_closed":
            direct_red,

        "productive_1plus_representation_survives":
            direct[
                "productive_1plus_representation_overlap_survives"
            ],

        "minimal_zero_derivative_vector_axial_improvement_closed":
            minimal[
                "minimal_vector_axial_fixed_tensor_repair_closed"
            ],

        "pure_stueckelberg_gauge_image_rescue_closed":
            stueckelberg[
                "pure_gauge_image_is_ward_silent_on_massless_pole"
            ],

        "declared_minimal_compensator_prefilter_red":
            minimal_red,

        "general_local_same_action_compensated_current_closed":
            False,

        "dynamical_hook_compensator_closed":
            False,

        "full_noether_complete_compensator_closed":
            False,

        "q_dependent_source_state_engineering_closed":
            False,

        "other_protected_vector_families_closed":
            False,

        "protected_2plus_routes_closed":
            False,

        "v26d_fallback_closed":
            False,

        "v26e_status":
            "PAUSED_NOT_CLOSED",

        "hook17_reference_capacity_rp1e12_j":
            HOOK17_REFERENCE_CAPACITY_RP1E12_J,

        "hook17_complete_energy_j":
            None,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "capacity_optimization_authorized":
            False,

        "sub100j_efficiency_tuning_authorized":
            False,

        "energy_optimization_authorized":
            False,

        "h17b_authorized":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "practical_device_found":
            False,

        "next":
            (
                "032H17A6R1_DYNAMICAL_SAME_ACTION_"
                "COMPENSATOR_NOETHER_CURRENT_GATE"
            ),

        "next_scientific_question":
            (
                "Can an explicit dynamical same-action compensator or "
                "Noether-complete matter sector supply a local hook-like "
                "current that cancels the surviving Ward residual while "
                "retaining nonzero physical 1+ overlap and healthy modes?"
            ),

        "claim_scope":
            (
                "DIRECT_J11_PLUS_DECLARED_MINIMAL_COMPENSATOR_"
                "SUBCLASSES_ONLY"
            ),
    }
