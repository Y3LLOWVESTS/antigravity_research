"""032H17A11B — K2 massless torsion-vector / Wheeler source Ward gate.

PURPOSE
-------
After A11A closed the three simplest repairs of the A10F2 ultralight
naturalness obstruction, test a genuinely distinct protected carrier:

    Barker-Marzo-Santoni K2
    massless protected torsion-like vector

against the actual Wheeler Dirac torsion source.

This is deliberately theorem-first.

WHY K2
------
The A10F2 failure arose because the surviving Marzo carrier required a
meter-range mass

    m ~ 1.97e-7 eV

while coupling to an ordinary Dirac threshold.

K2 instead contains a symmetry-protected massless vector.

Therefore the specific ultralight vector-mass naturalness obstruction is
absent at the carrier level.

WHEELER SOURCE
--------------
The existing repository implements only Wheeler's published rest-spin-up
torsion special case.

Wheeler Eq. (27) supplies the complete torsion response for a general
four-component spinor

    psi = (mu, nu, rho, sigma).

This module reconstructs that full 24-component response and first verifies
that it reproduces the existing special case exactly.

The tensor has the torsion symmetry

    T^a_bc = -T^a_cb.

The overall alpha/kappa normalization is irrelevant for the homogeneous K2
Ward test, so the source-shape analysis sets alpha/kappa=1.

K2 SOURCE IDENTITY
------------------
For the pair-antisymmetric source J^{alpha beta gamma}, the published K2
covariant source constraint is

    3 d_chi d^alpha J^{beta chi}{}_beta
    +
    Box J^{beta alpha}{}_beta
    =
    3 d_chi d_beta J^{beta alpha chi}.

In momentum space define

    A^chi = J^{beta chi}{}_beta.

Then the exact polynomial Ward residual is

    W^alpha(q)
      =
    3 q_chi q^alpha A^chi
    +
    q^2 A^alpha
    -
    3 q_chi q_beta J^{beta alpha chi}.

A source is admissible only if this vanishes as a polynomial for arbitrary q.

CRITICAL FALSE-GREEN CONTROL
----------------------------
For the A10 engineered rest sources, the specific lightlike direction

    q = (1,0,0,1)

happens to give zero residual.

Therefore a single lightlike helicity test is insufficient and would produce
a false green.

This gate constructs all 40 exact quadratic-polynomial coefficient
constraints:

    4 Ward components
    x
    10 independent symmetric q_mu q_nu monomials.

COMPLETE REST-DENSITY SOURCE CLASS
----------------------------------
A four-component Dirac spinor has a 16-real-dimensional Hermitian quadratic
density space:

    4 diagonal populations
    6 real coherences
    6 imaginary coherences.

This gate constructs a deterministic basis for that entire class.

For each direction it computes:

    Wheeler torsion source tensor
    exact K2 polynomial Ward coefficients.

It then determines exactly:

    rank(source map)
    rank(Ward map)
    Ward nullity
    rank of source image restricted to Ward nullspace.

If

    source * ker(Ward) = 0,

then every Ward-compatible source in the declared rest-density class is
physically source-silent.

CLAIM LIMIT
-----------
A RED result closes only:

    DIRECT K2 MASSLESS VECTOR
    +
    ZERO-MOMENTUM BLOCK-DIAGONAL / HERMITIAN DIRAC REST-DENSITY
    +
    UNMODIFIED WHEELER TORSION SOURCE.

It does NOT close:

- K2 globally;
- momentum-bearing Dirac bilinears;
- spatially textured on-shell spinor sources;
- derivative-improved currents;
- Noether-completed source sectors;
- other massless torsion-vector families;
- nonlinear carrier completions;
- HOOK17 globally.

No metric, payload, or energy run is authorized unless a nonzero
Ward-compatible protected source survives.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from typing import Any

import math

import numpy as np
import sympy as sp

from .dirac_hypermomentum_irrep import (
    rest_spinup_special_case,
)
from .hook17_exact_current_protection_atlas import (
    h17a11a_summary,
)


ETA = np.diag(
    [
        -1.0,
        1.0,
        1.0,
        1.0,
    ]
)

TOL = 1.0e-11

REST_DENSITY_LABELS = (
    "D0",
    "D1",
    "D2",
    "D3",
    "R01",
    "I01",
    "R02",
    "I02",
    "R03",
    "I03",
    "R12",
    "I12",
    "R13",
    "I13",
    "R23",
    "I23",
)


def _spinor_bilinears(
    spinor: np.ndarray,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """Return Wheeler D, R and I bilinears."""

    psi = np.asarray(
        spinor,
        dtype=np.complex128,
    )

    if psi.shape != (
        4,
    ):
        raise ValueError(
            "spinor must contain four complex components"
        )

    products = (
        np.conjugate(
            psi
        )[
            :,
            None,
        ]
        *
        psi[
            None,
            :,
        ]
    )

    diagonal = (
        np.abs(
            psi
        ) ** 2
    ).astype(
        float
    )

    real = np.real(
        products
    ).astype(
        float
    )

    imaginary = np.imag(
        products
    ).astype(
        float
    )

    return (
        diagonal,
        real,
        imaginary,
    )


def wheeler_full_torsion_response(
    spinor: np.ndarray,
    *,
    alpha_over_kappa: float = 1.0,
) -> np.ndarray:
    """Reconstruct Wheeler Eq. (27), T[a,b,c].

    The last two indices are exactly antisymmetric.

    The formulas below implement the full general-spinor result rather than
    the repository's previous rest-spin-up special case.
    """

    scale = float(
        alpha_over_kappa
    )

    if not np.isfinite(
        scale
    ):
        raise ValueError(
            "alpha_over_kappa must be finite"
        )

    (
        diagonal,
        real,
        imaginary,
    ) = _spinor_bilinears(
        spinor
    )

    mu = 0
    nu = 1
    rho = 2
    sigma = 3

    torsion = np.zeros(
        (
            4,
            4,
            4,
        ),
        dtype=float,
    )

    # Wheeler T^0 matrix.
    torsion[
        0,
        0,
        1,
    ] = (
        -imaginary[
            nu,
            rho,
        ]
        *
        scale
    )

    torsion[
        0,
        0,
        2,
    ] = (
        -imaginary[
            nu,
            sigma,
        ]
        *
        scale
    )

    torsion[
        0,
        1,
        0,
    ] = (
        imaginary[
            nu,
            rho,
        ]
        *
        scale
    )

    torsion[
        0,
        1,
        2,
    ] = (
        -imaginary[
            rho,
            sigma,
        ]
        *
        scale
    )

    torsion[
        0,
        2,
        0,
    ] = (
        imaginary[
            nu,
            sigma,
        ]
        *
        scale
    )

    torsion[
        0,
        2,
        1,
    ] = (
        imaginary[
            rho,
            sigma,
        ]
        *
        scale
    )

    half = (
        0.5
        *
        scale
    )

    # Wheeler T^1 matrix.
    matrix = np.array(
        [
            [
                0.0,
                imaginary[
                    nu,
                    sigma,
                ]
                +
                imaginary[
                    mu,
                    rho,
                ],
                imaginary[
                    rho,
                    sigma,
                ]
                +
                imaginary[
                    mu,
                    nu,
                ],
                0.0,
            ],
            [
                -imaginary[
                    nu,
                    sigma,
                ]
                -
                imaginary[
                    mu,
                    rho,
                ],
                0.0,
                0.0,
                imaginary[
                    mu,
                    nu,
                ]
                -
                imaginary[
                    rho,
                    sigma,
                ],
            ],
            [
                -imaginary[
                    rho,
                    sigma,
                ]
                -
                imaginary[
                    mu,
                    nu,
                ],
                0.0,
                0.0,
                imaginary[
                    mu,
                    rho,
                ]
                -
                imaginary[
                    nu,
                    sigma,
                ],
            ],
            [
                0.0,
                imaginary[
                    rho,
                    sigma,
                ]
                -
                imaginary[
                    mu,
                    nu,
                ],
                imaginary[
                    nu,
                    sigma,
                ]
                -
                imaginary[
                    mu,
                    rho,
                ],
                0.0,
            ],
        ],
        dtype=float,
    )

    torsion[
        1,
        :,
        :,
    ] = (
        half
        *
        matrix
    )

    # Wheeler T^2 matrix.
    matrix = np.array(
        [
            [
                0.0,
                real[
                    mu,
                    rho,
                ]
                -
                real[
                    nu,
                    sigma,
                ],
                -real[
                    mu,
                    nu,
                ]
                -
                real[
                    rho,
                    sigma,
                ],
                diagonal[
                    mu
                ]
                -
                diagonal[
                    sigma
                ],
            ],
            [
                real[
                    nu,
                    sigma,
                ]
                -
                real[
                    mu,
                    rho,
                ],
                0.0,
                diagonal[
                    nu
                ]
                +
                diagonal[
                    rho
                ],
                real[
                    rho,
                    sigma,
                ]
                -
                real[
                    mu,
                    nu,
                ],
            ],
            [
                real[
                    mu,
                    nu,
                ]
                +
                real[
                    rho,
                    sigma,
                ],
                -diagonal[
                    nu
                ]
                -
                diagonal[
                    rho
                ],
                0.0,
                -real[
                    mu,
                    rho,
                ]
                -
                real[
                    nu,
                    sigma,
                ],
            ],
            [
                -diagonal[
                    mu
                ]
                +
                diagonal[
                    sigma
                ],
                real[
                    mu,
                    nu,
                ]
                -
                real[
                    rho,
                    sigma,
                ],
                real[
                    mu,
                    rho,
                ]
                +
                real[
                    nu,
                    sigma,
                ],
                0.0,
            ],
        ],
        dtype=float,
    )

    torsion[
        2,
        :,
        :,
    ] = (
        half
        *
        matrix
    )

    # Wheeler T^3 matrix.
    matrix = np.array(
        [
            [
                0.0,
                imaginary[
                    nu,
                    rho,
                ]
                -
                imaginary[
                    mu,
                    sigma,
                ],
                0.0,
                -imaginary[
                    rho,
                    sigma,
                ]
                -
                imaginary[
                    mu,
                    nu,
                ],
            ],
            [
                imaginary[
                    mu,
                    sigma,
                ]
                -
                imaginary[
                    nu,
                    rho,
                ],
                0.0,
                imaginary[
                    mu,
                    nu,
                ]
                -
                imaginary[
                    rho,
                    sigma,
                ],
                0.0,
            ],
            [
                0.0,
                imaginary[
                    rho,
                    sigma,
                ]
                -
                imaginary[
                    mu,
                    nu,
                ],
                0.0,
                -imaginary[
                    mu,
                    sigma,
                ]
                -
                imaginary[
                    nu,
                    rho,
                ],
            ],
            [
                imaginary[
                    rho,
                    sigma,
                ]
                +
                imaginary[
                    mu,
                    nu,
                ],
                0.0,
                imaginary[
                    mu,
                    sigma,
                ]
                +
                imaginary[
                    nu,
                    rho,
                ],
                0.0,
            ],
        ],
        dtype=float,
    )

    torsion[
        3,
        :,
        :,
    ] = (
        half
        *
        matrix
    )

    return torsion


def wheeler_eq27_validation_gate() -> dict[
    str,
    Any,
]:
    """Validate full Eq.27 reconstruction against old special case."""

    basis = np.eye(
        4,
        dtype=np.complex128,
    )

    electron = (
        wheeler_full_torsion_response(
            basis[
                0
            ]
        )
    )

    positron = (
        wheeler_full_torsion_response(
            basis[
                3
            ]
        )
    )

    expected_electron = np.zeros(
        (
            4,
            4,
            4,
        ),
        dtype=float,
    )

    expected_electron[
        2,
        0,
        3,
    ] = 0.5

    expected_electron[
        2,
        3,
        0,
    ] = -0.5

    expected_positron = (
        -expected_electron
    )

    existing = (
        rest_spinup_special_case()
    )

    antisymmetry_errors = []

    for index in range(
        4
    ):
        source = (
            wheeler_full_torsion_response(
                basis[
                    index
                ]
            )
        )

        antisymmetry_errors.append(
            float(
                np.max(
                    np.abs(
                        source
                        +
                        np.swapaxes(
                            source,
                            1,
                            2,
                        )
                    )
                )
            )
        )

    maximum_antisymmetry_error = max(
        antisymmetry_errors
    )

    return {
        "electron_special_case_exact":
            bool(
                np.allclose(
                    electron,
                    expected_electron,
                    atol=TOL,
                    rtol=0.0,
                )
            ),

        "positron_special_case_exact":
            bool(
                np.allclose(
                    positron,
                    expected_positron,
                    atol=TOL,
                    rtol=0.0,
                )
            ),

        "existing_special_case_reports_opposite_sign":
            bool(
                existing[
                    "equal_amplitude_particle_antiparticle_opposite_torsion_sign"
                ]
            ),

        "existing_special_case_reports_pair_cancellation":
            bool(
                existing[
                    "pair_torsion_response_cancels"
                ]
            ),

        "maximum_pair_antisymmetry_error":
            maximum_antisymmetry_error,

        "full_eq27_pair_antisymmetry_pass":
            bool(
                maximum_antisymmetry_error
                <=
                TOL
            ),

        "full_general_spinor_torsion_reconstruction":
            True,
    }


def _pair_source(
    first: int,
    second: int,
) -> np.ndarray:
    """Return incoherent additive rest-pair torsion source."""

    basis = np.eye(
        4,
        dtype=np.complex128,
    )

    return (
        wheeler_full_torsion_response(
            basis[
                first
            ]
        )
        +
        wheeler_full_torsion_response(
            basis[
                second
            ]
        )
    )


def engineered_torsion_source_gate() -> dict[
    str,
    Any,
]:
    """Evaluate old clean and A10-engineered rest-pair torsion sources."""

    old_clean = (
        _pair_source(
            0,
            3,
        )
    )

    u1v1 = (
        _pair_source(
            0,
            2,
        )
    )

    u2v2 = (
        _pair_source(
            1,
            3,
        )
    )

    return {
        "historical_clean_U1_V2_torsion_norm":
            float(
                np.linalg.norm(
                    old_clean
                )
            ),

        "historical_clean_U1_V2_torsion_zero":
            bool(
                np.linalg.norm(
                    old_clean
                )
                <=
                TOL
            ),

        "U1_V1_torsion_norm":
            float(
                np.linalg.norm(
                    u1v1
                )
            ),

        "U2_V2_torsion_norm":
            float(
                np.linalg.norm(
                    u2v2
                )
            ),

        "U1_V1_torsion_nonzero":
            bool(
                np.linalg.norm(
                    u1v1
                )
                >
                TOL
            ),

        "U2_V2_torsion_nonzero":
            bool(
                np.linalg.norm(
                    u2v2
                )
                >
                TOL
            ),

        "engineered_source_state_reopens_full_wheeler_torsion":
            bool(
                np.linalg.norm(
                    u1v1
                )
                >
                TOL
                and
                np.linalg.norm(
                    u2v2
                )
                >
                TOL
            ),

        "U1_V1_nonzero_components":
            [
                {
                    "index":
                        [
                            int(
                                a
                            ),
                            int(
                                b
                            ),
                            int(
                                c
                            ),
                        ],

                    "value":
                        float(
                            u1v1[
                                a,
                                b,
                                c,
                            ]
                        ),
                }
                for (
                    a,
                    b,
                    c,
                )
                in np.argwhere(
                    np.abs(
                        u1v1
                    )
                    >
                    TOL
                )
            ],

        "U2_V2_nonzero_components":
            [
                {
                    "index":
                        [
                            int(
                                a
                            ),
                            int(
                                b
                            ),
                            int(
                                c
                            ),
                        ],

                    "value":
                        float(
                            u2v2[
                                a,
                                b,
                                c,
                            ]
                        ),
                }
                for (
                    a,
                    b,
                    c,
                )
                in np.argwhere(
                    np.abs(
                        u2v2
                    )
                    >
                    TOL
                )
            ],
    }


def _raise_last_pair(
    source: np.ndarray,
) -> np.ndarray:
    """Raise the antisymmetric pair of T^a_bc."""

    tensor = np.asarray(
        source,
        dtype=float,
    )

    return np.einsum(
        "bd,ce,ade->abc",
        ETA,
        ETA,
        tensor,
    )


def k2_ward_residual(
    source: np.ndarray,
    q_cov: np.ndarray,
) -> np.ndarray:
    """Return exact K2 momentum-space source Ward residual."""

    tensor = _raise_last_pair(
        source
    )

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

    q_up = (
        ETA
        @
        q
    )

    q_squared = float(
        q
        @
        q_up
    )

    # A^chi = J^{beta chi}{}_beta.
    trace = np.einsum(
        "bg,bcg->c",
        ETA,
        tensor,
    )

    q_dot_trace = float(
        np.dot(
            q,
            trace,
        )
    )

    residual = (
        3.0
        *
        q_up
        *
        q_dot_trace

        +
        q_squared
        *
        trace

        -
        3.0
        *
        np.einsum(
            "c,b,bac->a",
            q,
            q,
            tensor,
        )
    )

    return np.asarray(
        residual,
        dtype=float,
    )


def engineered_k2_ward_gate() -> dict[
    str,
    Any,
]:
    """Show why one-direction testing would be a false green."""

    sources = {
        "U1_V1":
            _pair_source(
                0,
                2,
            ),

        "U2_V2":
            _pair_source(
                1,
                3,
            ),
    }

    momenta = {
        "ACCIDENTAL_LIGHTLIKE_Z":
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

        "GENERIC":
            np.array(
                [
                    0.7,
                    -0.4,
                    0.2,
                    1.1,
                ]
            ),
    }

    rows = []

    for pair_id, source in sources.items():
        source_norm = float(
            np.linalg.norm(
                source
            )
        )

        for momentum_id, q_cov in momenta.items():
            residual = (
                k2_ward_residual(
                    source,
                    q_cov,
                )
            )

            norm = float(
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

                    "ward_residual":
                        residual.tolist(),

                    "ward_residual_norm":
                        norm,

                    "ward_pass":
                        bool(
                            norm
                            <=
                            TOL
                        ),
                }
            )

    lightlike_rows = [
        row
        for row
        in rows
        if row[
            "momentum_id"
        ]
        ==
        "ACCIDENTAL_LIGHTLIKE_Z"
    ]

    generic_rows = [
        row
        for row
        in rows
        if row[
            "momentum_id"
        ]
        ==
        "GENERIC"
    ]

    return {
        "rows":
            rows,

        "both_engineered_sources_accidentally_pass_lightlike_z":
            bool(
                all(
                    row[
                        "ward_pass"
                    ]
                    for row
                    in lightlike_rows
                )
            ),

        "both_engineered_sources_fail_generic_k2_ward":
            bool(
                all(
                    not row[
                        "ward_pass"
                    ]
                    for row
                    in generic_rows
                )
            ),

        "single_lightlike_direction_is_sufficient_source_test":
            False,

        "exact_polynomial_ward_test_required":
            True,
    }


def _density_direction_sources() -> list[
    tuple[
        str,
        np.ndarray,
    ]
]:
    """Return complete 16-real Hermitian rest-density torsion basis."""

    basis = np.eye(
        4,
        dtype=np.complex128,
    )

    diagonal_sources = [
        wheeler_full_torsion_response(
            basis[
                index
            ]
        )
        for index in range(
            4
        )
    ]

    rows: list[
        tuple[
            str,
            np.ndarray,
        ]
    ] = []

    for index in range(
        4
    ):
        rows.append(
            (
                f"D{index}",
                diagonal_sources[
                    index
                ].copy(),
            )
        )

    for first in range(
        4
    ):
        for second in range(
            first + 1,
            4,
        ):
            real_spinor = (
                basis[
                    first
                ]
                +
                basis[
                    second
                ]
            ) / math.sqrt(
                2.0
            )

            real_direction = (
                wheeler_full_torsion_response(
                    real_spinor
                )
                -
                0.5
                *
                diagonal_sources[
                    first
                ]
                -
                0.5
                *
                diagonal_sources[
                    second
                ]
            )

            imaginary_spinor = (
                basis[
                    first
                ]
                +
                1j
                *
                basis[
                    second
                ]
            ) / math.sqrt(
                2.0
            )

            imaginary_direction = (
                wheeler_full_torsion_response(
                    imaginary_spinor
                )
                -
                0.5
                *
                diagonal_sources[
                    first
                ]
                -
                0.5
                *
                diagonal_sources[
                    second
                ]
            )

            rows.append(
                (
                    f"R{first}{second}",
                    real_direction,
                )
            )

            rows.append(
                (
                    f"I{first}{second}",
                    imaginary_direction,
                )
            )

    if tuple(
        label
        for label, _ in rows
    ) != REST_DENSITY_LABELS:
        raise AssertionError(
            "unexpected Hermitian density-basis ordering"
        )

    return rows


def rest_density_torsion_basis() -> list[
    tuple[
        str,
        np.ndarray,
    ]
]:
    """Return copies of the full rest-density source basis."""

    return [
        (
            label,
            source.copy(),
        )
        for label, source
        in _density_direction_sources()
    ]


def _to_rational(
    value: float,
) -> sp.Rational:
    """Recover exact small rational coefficients from Wheeler arrays."""

    fraction = Fraction(
        float(
            value
        )
    ).limit_denominator(
        64
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

    if error > 1.0e-10:
        raise ValueError(
            "coefficient failed exact rational reconstruction: "
            +
            repr(
                value
            )
        )

    return sp.Rational(
        fraction.numerator,
        fraction.denominator,
    )


def _exact_source_matrix() -> sp.Matrix:
    """Return 64x16 exact Wheeler torsion-source map."""

    rows = _density_direction_sources()

    return sp.Matrix(
        64,
        16,
        lambda component, direction:
            _to_rational(
                rows[
                    direction
                ][
                    1
                ].reshape(
                    -1
                )[
                    component
                ]
            ),
    )


def _exact_ward_matrix() -> sp.Matrix:
    """Return 40x16 exact K2 quadratic-polynomial Ward map."""

    q = sp.symbols(
        "q0 q1 q2 q3"
    )

    eta_sign = (
        -1,
        1,
        1,
        1,
    )

    monomial_exponents = []

    for first in range(
        4
    ):
        for second in range(
            first,
            4,
        ):
            exponent = [
                0,
                0,
                0,
                0,
            ]

            exponent[
                first
            ] += 1

            exponent[
                second
            ] += 1

            monomial_exponents.append(
                tuple(
                    exponent
                )
            )

    columns = []

    for _, source_np in _density_direction_sources():
        source_up = sp.MutableDenseNDimArray.zeros(
            4,
            4,
            4,
        )

        for alpha in range(
            4
        ):
            for beta in range(
                4
            ):
                for gamma in range(
                    4
                ):
                    source_up[
                        alpha,
                        beta,
                        gamma,
                    ] = (
                        sp.Integer(
                            eta_sign[
                                beta
                            ]
                            *
                            eta_sign[
                                gamma
                            ]
                        )
                        *
                        _to_rational(
                            source_np[
                                alpha,
                                beta,
                                gamma,
                            ]
                        )
                    )

        trace = [
            sp.simplify(
                sum(
                    (
                        sp.Integer(
                            eta_sign[
                                beta
                            ]
                        )
                        *
                        source_up[
                            beta,
                            alpha,
                            beta,
                        ]
                    )
                    for beta in range(
                        4
                    )
                )
            )
            for alpha in range(
                4
            )
        ]

        q_up = [
            sp.Integer(
                eta_sign[
                    alpha
                ]
            )
            *
            q[
                alpha
            ]
            for alpha in range(
                4
            )
        ]

        q_squared = sp.simplify(
            sum(
                q[
                    alpha
                ]
                *
                q_up[
                    alpha
                ]
                for alpha in range(
                    4
                )
            )
        )

        q_dot_trace = sp.simplify(
            sum(
                q[
                    alpha
                ]
                *
                trace[
                    alpha
                ]
                for alpha in range(
                    4
                )
            )
        )

        residuals = []

        for alpha in range(
            4
        ):
            residual = (
                3
                *
                q_up[
                    alpha
                ]
                *
                q_dot_trace

                +
                q_squared
                *
                trace[
                    alpha
                ]

                -
                3
                *
                sum(
                    (
                        q[
                            chi
                        ]
                        *
                        q[
                            beta
                        ]
                        *
                        source_up[
                            beta,
                            alpha,
                            chi,
                        ]
                    )
                    for chi in range(
                        4
                    )
                    for beta in range(
                        4
                    )
                )
            )

            residuals.append(
                sp.expand(
                    residual
                )
            )

        coefficient_column = []

        for residual in residuals:
            polynomial = sp.Poly(
                residual,
                *q,
            )

            for exponents in monomial_exponents:
                coefficient_column.append(
                    polynomial.coeff_monomial(
                        exponents
                    )
                )

        columns.append(
            coefficient_column
        )

    return sp.Matrix(
        40,
        16,
        lambda row, column:
            columns[
                column
            ][
                row
            ],
    )


def _serialize_null_vector(
    vector: sp.Matrix,
) -> list[
    dict[
        str,
        str,
    ]
]:
    """Return sparse named representation of one exact null vector."""

    return [
        {
            "direction":
                REST_DENSITY_LABELS[
                    index
                ],

            "coefficient":
                str(
                    sp.simplify(
                        vector[
                            index
                        ]
                    )
                ),
        }
        for index in range(
            len(
                REST_DENSITY_LABELS
            )
        )
        if (
            sp.simplify(
                vector[
                    index
                ]
            )
            !=
            0
        )
    ]


@lru_cache(
    maxsize=1
)
def exact_rest_density_k2_theorem() -> dict[
    str,
    Any,
]:
    """Prove whether any nonzero rest-density Wheeler source survives K2."""

    source_matrix = (
        _exact_source_matrix()
    )

    ward_matrix = (
        _exact_ward_matrix()
    )

    nullspace = (
        ward_matrix.nullspace()
    )

    if nullspace:
        null_matrix = sp.Matrix.hstack(
            *nullspace
        )

        ward_null_source_image = (
            source_matrix
            *
            null_matrix
        )

        image_rank = int(
            ward_null_source_image.rank()
        )

        image_zero = bool(
            ward_null_source_image
            ==
            sp.zeros(
                source_matrix.rows,
                len(
                    nullspace
                ),
            )
        )
    else:
        image_rank = 0
        image_zero = True

    source_rank = int(
        source_matrix.rank()
    )

    ward_rank = int(
        ward_matrix.rank()
    )

    ward_nullity = len(
        nullspace
    )

    no_nonzero_escape = bool(
        image_zero
    )

    return {
        "rest_density_real_dimension":
            16,

        "wheeler_torsion_source_map_rank":
            source_rank,

        "k2_exact_polynomial_ward_rank":
            ward_rank,

        "k2_exact_polynomial_ward_nullity":
            ward_nullity,

        "ward_nullspace_vectors":
            [
                _serialize_null_vector(
                    vector
                )
                for vector in nullspace
            ],

        "ward_nullspace_source_image_rank":
            image_rank,

        "ward_nullspace_maps_to_exact_zero_torsion_source":
            image_zero,

        "nonzero_ward_compatible_wheeler_torsion_source_exists":
            bool(
                not no_nonzero_escape
            ),

        "direct_k2_zero_momentum_rest_density_route_closed":
            no_nonzero_escape,

        "symbolic_exact_arithmetic":
            True,

        "closure_scope":
            (
                "COMPLETE_16_REAL_DIMENSION_HERMITIAN_ZERO_MOMENTUM_"
                "DIRAC_REST_DENSITY_CLASS_WITH_UNMODIFIED_WHEELER_"
                "TORSION_SOURCE"
            ),
    }


def k2_published_carrier_gate() -> dict[
    str,
    Any,
]:
    """Record only the published K2 carrier facts needed after source Ward."""

    return {
        "family":
            "BARKER_MARZO_SANTONI_K2",

        "field_symmetry":
            "K_alpha_beta_gamma=-K_alpha_gamma_beta",

        "protected_by_symmetry_first_construction":
            True,

        "propagating_particle":
            "MASSLESS_VECTOR",

        "physical_polarizations":
            2,

        "published_residue":
            "-1/kappa1^(4)",

        "unitarity_condition":
            "kappa1^(4)<0",

        "published_1minus_source_copy_constraint":
            "J_1minus_copy1+2*J_1minus_copy2=0",

        "covariant_source_ward_used":
            True,

        "ultralight_mass_parameter_required":
            False,

        "a10f2_specific_ultralight_mass_naturalness_obstruction":
            False,

        "nonlinear_completion_established":
            False,

        "same_action_wheeler_matter_established":
            False,

        "exact_pole_residue_evaluation_needed_after_ward_failure":
            False,
    }


@lru_cache(
    maxsize=1
)
def h17a11b_summary() -> dict[
    str,
    Any,
]:
    """Return the scoped A11B K2 source closeout."""

    a11a = h17a11a_summary()

    validation = (
        wheeler_eq27_validation_gate()
    )

    engineered = (
        engineered_torsion_source_gate()
    )

    sample_ward = (
        engineered_k2_ward_gate()
    )

    theorem = (
        exact_rest_density_k2_theorem()
    )

    carrier = (
        k2_published_carrier_gate()
    )

    provenance = bool(
        a11a[
            "three_minimal_source_protection_repairs_closed"
        ]
        and
        a11a[
            "hook17_closed"
        ]
        is False
    )

    source_closeout = bool(
        provenance
        and
        validation[
            "electron_special_case_exact"
        ]
        and
        validation[
            "positron_special_case_exact"
        ]
        and
        validation[
            "full_eq27_pair_antisymmetry_pass"
        ]
        and
        engineered[
            "engineered_source_state_reopens_full_wheeler_torsion"
        ]
        and
        sample_ward[
            "both_engineered_sources_fail_generic_k2_ward"
        ]
        and
        theorem[
            "direct_k2_zero_momentum_rest_density_route_closed"
        ]
        and
        theorem[
            "ward_nullspace_maps_to_exact_zero_torsion_source"
        ]
    )

    decision = (
        (
            "RED_SCOPED_A11B_DIRECT_K2_ZERO_MOMENTUM_REST_DENSITY_"
            "WHEELER_TORSION_SOURCE_CLOSED__"
            "NONREST_TEXTURED_K2_REMAINS_OPEN"
        )
        if source_closeout
        else
        "YELLOW_A11B_K2_SOURCE_WARD_REQUIRES_REVIEW"
    )

    return {
        "branch":
            "032H17A11B",

        "decision":
            decision,

        "current_full_regression_before_a11b":
            1006,

        "a11a_provenance":
            provenance,

        "wheeler_eq27_validation":
            validation,

        "engineered_torsion_sources":
            engineered,

        "engineered_sample_ward":
            sample_ward,

        "exact_rest_density_theorem":
            theorem,

        "k2_carrier":
            carrier,

        "new_scientific_fact_engineered_states_source_full_wheeler_torsion":
            engineered[
                "engineered_source_state_reopens_full_wheeler_torsion"
            ],

        "single_lightlike_screen_would_have_false_green":
            sample_ward[
                "both_engineered_sources_accidentally_pass_lightlike_z"
            ],

        "nonzero_k2_ward_compatible_rest_density_source_exists":
            theorem[
                "nonzero_ward_compatible_wheeler_torsion_source_exists"
            ],

        "direct_k2_rest_density_wheeler_route_closed":
            source_closeout,

        "k2_massless_family_globally_closed":
            False,

        "k2_nonrest_momentum_textured_dirac_source_closed":
            False,

        "all_massless_torsion_vector_families_closed":
            False,

        "k3_historical_clean_route_reopened":
            False,

        "metric_gate_authorized":
            False,

        "payload_gate_authorized":
            False,

        "energy_optimization_authorized":
            False,

        "hook17_mechanism_knowledge_preserved":
            True,

        "hook17_closed":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "next":
            (
                "032H17A11C_K2_ONSHELL_NONREST_DIRAC_BILINEAR_"
                "EXACT_WARD_AND_MASSLESS_POLE_GATE"
                if source_closeout
                else
                "REVIEW_A11B_SOURCE_CONVENTIONS"
            ),

        "stop_rule":
            (
                "IF_COMPLETE_ONSHELL_TWO_MOMENTUM_DIRAC_BILINEAR_SPACE_"
                "HAS_ZERO_K2_WARD_COMPATIBLE_SOURCE_CLOSE_DIRECT_K2_"
                "WHEELER_ROUTE;_DO_NOT_RUN_METRIC_PAYLOAD_OR_ENERGY"
            ),
    }
