"""032H17A2 exact V24-to-healthy-hook-MAG source projector gate.

PURPOSE
-------
Strengthen the 032H17A representation-support result into an exact source-to-
healthy-pole calculation for the two surviving hook-symmetric nonmetricity
channels:

    HOOK_2_PLUS
    HOOK_1_PLUS

The calculation uses the actual V24 clean rest-pair hook tensor already stored
in the repository and the canonical two-index source maps published for the
single-state healthy hook-nonmetricity models of Mikura and Percacci.

SCIENTIFIC QUESTION
-------------------
Does the microscopic V24 intrinsic hook source merely transform in an allowed
O(3) representation, or does it actually feed the canonical source seen by a
healthy propagating pole after the required derivative/source projection?

This distinction is decisive. A nonzero raw hook component is not enough.
The action-dependent canonical source must be nonzero.

REFERENCE SOURCE MAPS
---------------------
For a hook source tau_{lambda mu nu}, the relevant published source maps are,
up to the declared Fourier i factor and sign convention,

2+ branch:

    J_{mu nu}
      = sqrt(2 / (-3 m1))
        [
            d_lambda tau^lambda_{ mu nu}
            - d_lambda tau_{(mu}{}^lambda{}_{nu)}
        ]

1+ branch:

    J_{mu nu}
      = 1 / sqrt(-2 m1)
        [
            d_lambda tau_mu{}^lambda{}_nu
            - d_lambda tau_nu{}^lambda{}_mu
        ]

For momentum-space source diagnostics we remove the common factor i and work
with the real numerators N2 and N1. The canonical branch factors are restored
when testing healthy on-shell scaling.

HEALTHY SINGLE-STATE CONDITIONS
-------------------------------
For the reference conventions used by the published branches:

    2+: m1 < 0 and b6 < 0
        pole mass^2 = 3 m1 / (2 b6)

    1+: m1 < 0 and b7 < 0
        pole mass^2 = 2 m1 / b7

The code does not infer phenomenological viability from these inequalities.
They are only the quadratic ghost/tachyon-free branch conditions used for the
projector calculation.

STATIC FOURIER PREFLIGHT
------------------------
A laboratory source is not a carrier-rest-frame on-shell particle. Therefore
this module also evaluates the derivative source maps at q0=0 for spatial
Fourier momenta. For the clean V24 source the exact raw numerator norms are

    ||N2||^2 = 128 k_y^2 + 32 k_z^2

    ||N1||^2 = 128 k_z^2

in the repository's current source orientation. Thus a generic localized
source envelope has nonzero derivative support, but the response is
anisotropic. This is not yet a static Green-function or finite-payload force.

SAME-ACTION DISCIPLINE
----------------------
This gate deliberately separates three facts:

1. Wheeler supplies an explicit Dirac/affine source action.
2. Mikura/Percacci supply explicit healthy hook-nonmetricity free actions and
   the canonical source maps used here.
3. The project has NOT yet derived one complete action containing the chosen
   healthy kinetic branch, the exact Dirac source vertex, and the HOOK17
   universal physical metric simultaneously.

Therefore a nonzero result authorizes an explicit same-action construction
attempt. It does not authorize H17B, energy optimization, or a physical-model
claim.

CLAIM LIMITS
------------
This module does NOT establish:

- a complete same-action HOOK17 theory;
- a gauge/Noether-complete Dirac + healthy-MAG interacting action;
- a universal physical metric in that same action;
- a nonremovable source-to-metric cross response;
- static finite-payload outward acceleration;
- source, compensator, support, or complete operating energy;
- quantum, RG, UV, empirical, nonlinear, or stability closure;
- a practical antigravity device.

No AGMINER candidate insertion is performed.
No energy optimization is performed.

CLAIM_CLASSIFICATION=
EXACT_SOURCE_TO_HEALTHY_POLE_PROJECTOR_NECESSARY_CONDITION_GATE
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .nonlinear_hook_metric_bridge import rest_pair_hook


ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
TOL = 1.0e-12
HOOK17_REFERENCE_CAPACITY_RP1E12_J = 17.0676442196
STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7


def _rank3(value: np.ndarray) -> np.ndarray:
    """Return a validated finite covariant rank-three source tensor."""
    array = np.asarray(value, dtype=float)

    if array.shape != (4, 4, 4):
        raise ValueError(
            "source tensor must have shape (4,4,4)"
        )

    if not np.all(
        np.isfinite(
            array
        )
    ):
        raise ValueError(
            "source tensor must be finite"
        )

    return array


def _momentum(value: np.ndarray) -> np.ndarray:
    """Return a validated real covariant Fourier momentum q_lambda."""
    array = np.asarray(
        value,
        dtype=float,
    )

    if array.shape != (4,):
        raise ValueError(
            "momentum must have shape (4,)"
        )

    if not np.all(
        np.isfinite(
            array
        )
    ):
        raise ValueError(
            "momentum must be finite"
        )

    return array


def raise_first_index(
    tau: np.ndarray,
) -> np.ndarray:
    """Return tau^lambda_{ mu nu} from covariant tau_{alpha mu nu}."""
    source = _rank3(
        tau
    )

    return np.einsum(
        "la,amn->lmn",
        ETA,
        source,
    )


def raise_second_index(
    tau: np.ndarray,
) -> np.ndarray:
    """Return tau_mu{}^lambda{}_nu from covariant tau_{mu alpha nu}."""
    source = _rank3(
        tau
    )

    return np.einsum(
        "la,man->mln",
        ETA,
        source,
    )


def mp_hook_2plus_source_numerator(
    tau: np.ndarray,
    q_cov: np.ndarray,
) -> np.ndarray:
    """Return the real momentum-space numerator of the published 2+ source.

    The common Fourier factor i is intentionally omitted because only source
    support, tensor identities, and squared residue scaling are tested here.
    """
    source = _rank3(
        tau
    )

    q = _momentum(
        q_cov
    )

    first_raised = (
        raise_first_index(
            source
        )
    )

    second_raised = (
        raise_second_index(
            source
        )
    )

    divergence_first = np.einsum(
        "l,lmn->mn",
        q,
        first_raised,
    )

    divergence_second = np.einsum(
        "l,mln->mn",
        q,
        second_raised,
    )

    sym_divergence_second = (
        0.5
        *
        (
            divergence_second
            +
            divergence_second.T
        )
    )

    return (
        divergence_first
        -
        sym_divergence_second
    )


def mp_hook_1plus_source_numerator(
    tau: np.ndarray,
    q_cov: np.ndarray,
) -> np.ndarray:
    """Return the real momentum-space numerator of the published 1+ source."""
    source = _rank3(
        tau
    )

    q = _momentum(
        q_cov
    )

    second_raised = (
        raise_second_index(
            source
        )
    )

    divergence_second = np.einsum(
        "l,mln->mn",
        q,
        second_raised,
    )

    return (
        divergence_second
        -
        divergence_second.T
    )


def clean_v24_source_components() -> dict[
    str,
    Any,
]:
    """Return the exact sparse V24 clean-hook components used by H17A2."""
    tau = _rank3(
        rest_pair_hook()
    )

    rows: list[
        dict[
            str,
            Any,
        ]
    ] = []

    for a in range(
        4
    ):
        for b in range(
            4
        ):
            for c in range(
                4
            ):
                value = float(
                    tau[
                        a,
                        b,
                        c,
                    ]
                )

                if abs(
                    value
                ) > TOL:
                    rows.append(
                        {
                            "indices":
                                [
                                    a,
                                    b,
                                    c,
                                ],

                            "value":
                                value,
                        }
                    )

    return {
        "nonzero_component_count":
            len(
                rows
            ),

        "components":
            rows,

        "euclidean_component_norm2":
            float(
                np.sum(
                    tau
                    *
                    tau
                )
            ),

        "pure_hook_source_inherited_from_v24_v26c":
            True,
    }


def timelike_rest_pole_projector_gate() -> dict[
    str,
    Any,
]:
    """Evaluate exact healthy-source numerators in a timelike rest frame.

    q=(1,0,0,0) isolates the representation content. Overall q0 and
    canonical normalization are handled separately in the branch-scaling
    functions.

    In the massive-pole rest frame the published transverse projectors reduce
    to ordinary spatial spin projectors. These are applied explicitly below.
    """
    tau = _rank3(
        rest_pair_hook()
    )

    q = np.array(
        [
            1.0,
            0.0,
            0.0,
            0.0,
        ]
    )

    n2 = (
        mp_hook_2plus_source_numerator(
            tau,
            q,
        )
    )

    n1 = (
        mp_hook_1plus_source_numerator(
            tau,
            q,
        )
    )

    n2_spatial = np.asarray(
        n2[
            1:,
            1:,
        ],
        dtype=float,
    )

    n1_spatial = np.asarray(
        n1[
            1:,
            1:,
        ],
        dtype=float,
    )

    n2_symmetry_residual = float(
        np.max(
            np.abs(
                n2_spatial
                -
                n2_spatial.T
            )
        )
    )

    n2_trace = float(
        np.trace(
            n2_spatial
        )
    )

    n1_antisymmetry_residual = float(
        np.max(
            np.abs(
                n1_spatial
                +
                n1_spatial.T
            )
        )
    )

    n2_norm2 = float(
        np.sum(
            n2_spatial
            *
            n2_spatial
        )
    )

    n1_norm2 = float(
        np.sum(
            n1_spatial
            *
            n1_spatial
        )
    )

    n2_projected = (
        0.5
        *
        (
            n2_spatial
            +
            n2_spatial.T
        )
    )

    n2_projected -= (
        np.eye(
            3
        )
        *
        np.trace(
            n2_projected
        )
        /
        3.0
    )

    n1_projected = (
        0.5
        *
        (
            n1_spatial
            -
            n1_spatial.T
        )
    )

    n2_projected_norm2 = float(
        np.sum(
            n2_projected
            *
            n2_projected
        )
    )

    n1_projected_norm2 = float(
        np.sum(
            n1_projected
            *
            n1_projected
        )
    )

    return {
        "q_cov":
            q.tolist(),

        "hook_2plus_raw_source_matrix":
            n2.tolist(),

        "hook_1plus_raw_source_matrix":
            n1.tolist(),

        "hook_2plus_spatial_source_matrix":
            n2_spatial.tolist(),

        "hook_1plus_spatial_source_matrix":
            n1_spatial.tolist(),

        "hook_2plus_symmetric":
            (
                n2_symmetry_residual
                <=
                TOL
            ),

        "hook_2plus_symmetry_residual":
            n2_symmetry_residual,

        "hook_2plus_traceless":
            (
                abs(
                    n2_trace
                )
                <=
                TOL
            ),

        "hook_2plus_trace":
            n2_trace,

        "hook_1plus_antisymmetric":
            (
                n1_antisymmetry_residual
                <=
                TOL
            ),

        "hook_1plus_antisymmetry_residual":
            n1_antisymmetry_residual,

        "hook_2plus_raw_spatial_norm2":
            n2_norm2,

        "hook_1plus_raw_spatial_norm2":
            n1_norm2,

        "hook_2plus_projected_spatial_norm2":
            n2_projected_norm2,

        "hook_1plus_projected_spatial_norm2":
            n1_projected_norm2,

        "hook_2plus_projector_retention_fraction":
            (
                n2_projected_norm2
                /
                n2_norm2

                if n2_norm2 > TOL

                else 0.0
            ),

        "hook_1plus_projector_retention_fraction":
            (
                n1_projected_norm2
                /
                n1_norm2

                if n1_norm2 > TOL

                else 0.0
            ),

        "hook_2plus_exact_pole_source_nonzero":
            (
                n2_projected_norm2
                >
                TOL
            ),

        "hook_1plus_exact_pole_source_nonzero":
            (
                n1_projected_norm2
                >
                TOL
            ),

        "expected_hook_2plus_norm2":
            32.0,

        "expected_hook_1plus_norm2":
            128.0,

        "hook_2plus_expected_identity_pass":
            (
                abs(
                    n2_norm2
                    -
                    32.0
                )
                <=
                TOL
            ),

        "hook_1plus_expected_identity_pass":
            (
                abs(
                    n1_norm2
                    -
                    128.0
                )
                <=
                TOL
            ),

        "common_fourier_i_removed":
            True,

        "canonical_normalization_included":
            False,
    }


def healthy_hook_2plus_branch(
    m1: float,
    b6: float,
) -> dict[
    str,
    Any,
]:
    """Evaluate canonical 2+ source strength on the healthy reference branch."""
    m1_value = float(
        m1
    )

    b6_value = float(
        b6
    )

    if (
        not np.isfinite(
            m1_value
        )
        or
        not np.isfinite(
            b6_value
        )
    ):
        raise ValueError(
            "2+ parameters must be finite"
        )

    if (
        m1_value >= 0.0
        or
        b6_value >= 0.0
    ):
        return {
            "healthy":
                False,

            "m1":
                m1_value,

            "b6":
                b6_value,

            "reason":
                (
                    "REFERENCE_HEALTH_REQUIRES_"
                    "M1_LT_0_AND_B6_LT_0"
                ),
        }

    mass2 = (
        3.0
        *
        m1_value
        /
        (
            2.0
            *
            b6_value
        )
    )

    if mass2 <= 0.0:
        raise ValueError(
            "healthy 2+ branch unexpectedly has nonpositive mass2"
        )

    q0 = float(
        np.sqrt(
            mass2
        )
    )

    tau = _rank3(
        rest_pair_hook()
    )

    n2 = (
        mp_hook_2plus_source_numerator(
            tau,
            np.array(
                [
                    q0,
                    0.0,
                    0.0,
                    0.0,
                ]
            ),
        )
        [
            1:,
            1:,
        ]
    )

    raw_norm2 = float(
        np.sum(
            n2
            *
            n2
        )
    )

    prefactor2 = (
        2.0
        /
        (
            -3.0
            *
            m1_value
        )
    )

    canonical_source_norm2 = float(
        prefactor2
        *
        raw_norm2
    )

    expected = float(
        -32.0
        /
        b6_value
    )

    return {
        "healthy":
            True,

        "m1":
            m1_value,

        "b6":
            b6_value,

        "mass2":
            mass2,

        "q0":
            q0,

        "raw_source_norm2_on_pole":
            raw_norm2,

        "canonical_prefactor_squared":
            prefactor2,

        "canonical_source_norm2":
            canonical_source_norm2,

        "expected_canonical_source_norm2":
            expected,

        "canonical_identity_residual":
            abs(
                canonical_source_norm2
                -
                expected
            ),

        "canonical_identity_pass":
            bool(
                np.isclose(
                    canonical_source_norm2,
                    expected,
                    rtol=1.0e-12,
                    atol=1.0e-12,
                )
            ),

        "positive_residue_source_strength":
            (
                canonical_source_norm2
                >
                0.0
            ),
    }


def healthy_hook_1plus_branch(
    m1: float,
    b7: float,
) -> dict[
    str,
    Any,
]:
    """Evaluate canonical 1+ source strength on the healthy reference branch."""
    m1_value = float(
        m1
    )

    b7_value = float(
        b7
    )

    if (
        not np.isfinite(
            m1_value
        )
        or
        not np.isfinite(
            b7_value
        )
    ):
        raise ValueError(
            "1+ parameters must be finite"
        )

    if (
        m1_value >= 0.0
        or
        b7_value >= 0.0
    ):
        return {
            "healthy":
                False,

            "m1":
                m1_value,

            "b7":
                b7_value,

            "reason":
                (
                    "REFERENCE_HEALTH_REQUIRES_"
                    "M1_LT_0_AND_B7_LT_0"
                ),
        }

    mass2 = (
        2.0
        *
        m1_value
        /
        b7_value
    )

    if mass2 <= 0.0:
        raise ValueError(
            "healthy 1+ branch unexpectedly has nonpositive mass2"
        )

    q0 = float(
        np.sqrt(
            mass2
        )
    )

    tau = _rank3(
        rest_pair_hook()
    )

    n1 = (
        mp_hook_1plus_source_numerator(
            tau,
            np.array(
                [
                    q0,
                    0.0,
                    0.0,
                    0.0,
                ]
            ),
        )
        [
            1:,
            1:,
        ]
    )

    raw_norm2 = float(
        np.sum(
            n1
            *
            n1
        )
    )

    prefactor2 = (
        1.0
        /
        (
            -2.0
            *
            m1_value
        )
    )

    canonical_source_norm2 = float(
        prefactor2
        *
        raw_norm2
    )

    expected = float(
        -128.0
        /
        b7_value
    )

    return {
        "healthy":
            True,

        "m1":
            m1_value,

        "b7":
            b7_value,

        "mass2":
            mass2,

        "q0":
            q0,

        "raw_source_norm2_on_pole":
            raw_norm2,

        "canonical_prefactor_squared":
            prefactor2,

        "canonical_source_norm2":
            canonical_source_norm2,

        "expected_canonical_source_norm2":
            expected,

        "canonical_identity_residual":
            abs(
                canonical_source_norm2
                -
                expected
            ),

        "canonical_identity_pass":
            bool(
                np.isclose(
                    canonical_source_norm2,
                    expected,
                    rtol=1.0e-12,
                    atol=1.0e-12,
                )
            ),

        "positive_residue_source_strength":
            (
                canonical_source_norm2
                >
                0.0
            ),
    }


def healthy_branch_identity_scan() -> dict[
    str,
    Any,
]:
    """Verify the canonical source identities over separated healthy points."""
    two_plus_points = [
        (
            -1.0,
            -0.25,
        ),
        (
            -0.3,
            -2.0,
        ),
        (
            -7.0,
            -0.7,
        ),
        (
            -1.0e-4,
            -3.0e2,
        ),
    ]

    one_plus_points = [
        (
            -1.0,
            -0.5,
        ),
        (
            -0.2,
            -4.0,
        ),
        (
            -9.0,
            -0.9,
        ),
        (
            -2.0e-4,
            -5.0e2,
        ),
    ]

    two_rows = [
        healthy_hook_2plus_branch(
            m1,
            b6,
        )
        for (
            m1,
            b6,
        )
        in two_plus_points
    ]

    one_rows = [
        healthy_hook_1plus_branch(
            m1,
            b7,
        )
        for (
            m1,
            b7,
        )
        in one_plus_points
    ]

    return {
        "hook_2plus_rows":
            two_rows,

        "hook_1plus_rows":
            one_rows,

        "hook_2plus_all_healthy":
            all(
                row[
                    "healthy"
                ]
                for row
                in two_rows
            ),

        "hook_1plus_all_healthy":
            all(
                row[
                    "healthy"
                ]
                for row
                in one_rows
            ),

        "hook_2plus_identity_all_pass":
            all(
                row[
                    "canonical_identity_pass"
                ]
                for row
                in two_rows
            ),

        "hook_1plus_identity_all_pass":
            all(
                row[
                    "canonical_identity_pass"
                ]
                for row
                in one_rows
            ),

        "hook_2plus_positive_source_strength_all":
            all(
                row[
                    "positive_residue_source_strength"
                ]
                for row
                in two_rows
            ),

        "hook_1plus_positive_source_strength_all":
            all(
                row[
                    "positive_residue_source_strength"
                ]
                for row
                in one_rows
            ),
    }


def static_fourier_source_gate() -> dict[
    str,
    Any,
]:
    """Evaluate exact q0=0 source support and anisotropy identities."""
    tau = _rank3(
        rest_pair_hook()
    )

    axes = {
        "X":
            np.array(
                [
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                ]
            ),

        "Y":
            np.array(
                [
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                ]
            ),

        "Z":
            np.array(
                [
                    0.0,
                    0.0,
                    0.0,
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
    ) in axes.items():
        n2 = (
            mp_hook_2plus_source_numerator(
                tau,
                q,
            )
        )

        n1 = (
            mp_hook_1plus_source_numerator(
                tau,
                q,
            )
        )

        rows[
            name
        ] = {
            "q_cov":
                q.tolist(),

            "hook_2plus_raw_norm2":
                float(
                    np.sum(
                        n2
                        *
                        n2
                    )
                ),

            "hook_1plus_raw_norm2":
                float(
                    np.sum(
                        n1
                        *
                        n1
                    )
                ),
        }

    pair_q = {
        "XY":
            np.array(
                [
                    0.0,
                    1.0,
                    1.0,
                    0.0,
                ]
            ),

        "XZ":
            np.array(
                [
                    0.0,
                    1.0,
                    0.0,
                    1.0,
                ]
            ),

        "YZ":
            np.array(
                [
                    0.0,
                    0.0,
                    1.0,
                    1.0,
                ]
            ),
    }

    pair_rows: dict[
        str,
        Any,
    ] = {}

    for (
        name,
        q,
    ) in pair_q.items():
        n2 = (
            mp_hook_2plus_source_numerator(
                tau,
                q,
            )
        )

        n1 = (
            mp_hook_1plus_source_numerator(
                tau,
                q,
            )
        )

        pair_rows[
            name
        ] = {
            "hook_2plus_raw_norm2":
                float(
                    np.sum(
                        n2
                        *
                        n2
                    )
                ),

            "hook_1plus_raw_norm2":
                float(
                    np.sum(
                        n1
                        *
                        n1
                    )
                ),
        }

    coeff2 = np.array(
        [
            rows[
                "X"
            ][
                "hook_2plus_raw_norm2"
            ],

            rows[
                "Y"
            ][
                "hook_2plus_raw_norm2"
            ],

            rows[
                "Z"
            ][
                "hook_2plus_raw_norm2"
            ],
        ]
    )

    coeff1 = np.array(
        [
            rows[
                "X"
            ][
                "hook_1plus_raw_norm2"
            ],

            rows[
                "Y"
            ][
                "hook_1plus_raw_norm2"
            ],

            rows[
                "Z"
            ][
                "hook_1plus_raw_norm2"
            ],
        ]
    )

    expected2 = np.array(
        [
            0.0,
            128.0,
            32.0,
        ]
    )

    expected1 = np.array(
        [
            0.0,
            0.0,
            128.0,
        ]
    )

    cross2 = {
        "XY":
            (
                pair_rows[
                    "XY"
                ][
                    "hook_2plus_raw_norm2"
                ]
                -
                coeff2[
                    0
                ]
                -
                coeff2[
                    1
                ]
            ),

        "XZ":
            (
                pair_rows[
                    "XZ"
                ][
                    "hook_2plus_raw_norm2"
                ]
                -
                coeff2[
                    0
                ]
                -
                coeff2[
                    2
                ]
            ),

        "YZ":
            (
                pair_rows[
                    "YZ"
                ][
                    "hook_2plus_raw_norm2"
                ]
                -
                coeff2[
                    1
                ]
                -
                coeff2[
                    2
                ]
            ),
    }

    cross1 = {
        "XY":
            (
                pair_rows[
                    "XY"
                ][
                    "hook_1plus_raw_norm2"
                ]
                -
                coeff1[
                    0
                ]
                -
                coeff1[
                    1
                ]
            ),

        "XZ":
            (
                pair_rows[
                    "XZ"
                ][
                    "hook_1plus_raw_norm2"
                ]
                -
                coeff1[
                    0
                ]
                -
                coeff1[
                    2
                ]
            ),

        "YZ":
            (
                pair_rows[
                    "YZ"
                ][
                    "hook_1plus_raw_norm2"
                ]
                -
                coeff1[
                    1
                ]
                -
                coeff1[
                    2
                ]
            ),
    }

    return {
        "q0":
            0.0,

        "axis_rows":
            rows,

        "pair_rows":
            pair_rows,

        "hook_2plus_quadratic_coefficients_kx_ky_kz":
            coeff2.tolist(),

        "hook_1plus_quadratic_coefficients_kx_ky_kz":
            coeff1.tolist(),

        "hook_2plus_expected_coefficients":
            expected2.tolist(),

        "hook_1plus_expected_coefficients":
            expected1.tolist(),

        "hook_2plus_exact_anisotropy_identity_pass":
            bool(
                np.allclose(
                    coeff2,
                    expected2,
                    rtol=0.0,
                    atol=TOL,
                )
                and
                max(
                    abs(
                        value
                    )
                    for value
                    in cross2.values()
                )
                <=
                TOL
            ),

        "hook_1plus_exact_anisotropy_identity_pass":
            bool(
                np.allclose(
                    coeff1,
                    expected1,
                    rtol=0.0,
                    atol=TOL,
                )
                and
                max(
                    abs(
                        value
                    )
                    for value
                    in cross1.values()
                )
                <=
                TOL
            ),

        "hook_2plus_cross_terms":
            cross2,

        "hook_1plus_cross_terms":
            cross1,

        "hook_2plus_unit_sphere_angular_average_norm2":
            float(
                np.sum(
                    coeff2
                )
                /
                3.0
            ),

        "hook_1plus_unit_sphere_angular_average_norm2":
            float(
                np.sum(
                    coeff1
                )
                /
                3.0
            ),

        "hook_2plus_generic_static_gradient_support_nonzero":
            bool(
                np.sum(
                    coeff2
                )
                >
                TOL
            ),

        "hook_1plus_generic_static_gradient_support_nonzero":
            bool(
                np.sum(
                    coeff1
                )
                >
                TOL
            ),

        "static_green_function_evaluated":
            False,

        "finite_payload_evaluated":
            False,
    }


def same_action_provenance_gate() -> dict[
    str,
    Any,
]:
    """Fail closed on the difference between source overlap and one action."""
    pole = (
        timelike_rest_pole_projector_gate()
    )

    return {
        "wheeler_explicit_dirac_affine_source_action_exists":
            True,

        "mikura_percacci_explicit_healthy_hook_quadratic_actions_exist":
            True,

        "mikura_percacci_reference_matter_interactions_included":
            False,

        "wheeler_reference_supplies_target_healthy_propagating_hook_kinetic":
            False,

        "same_geometric_hook_source_type_can_be_compared_at_linearized_level":
            True,

        "published_canonical_source_map_applied_to_actual_v24_source":
            True,

        "hook_2plus_exact_source_to_pole_nonzero":
            pole[
                "hook_2plus_exact_pole_source_nonzero"
            ],

        "hook_1plus_exact_source_to_pole_nonzero":
            pole[
                "hook_1plus_exact_pole_source_nonzero"
            ],

        "single_reference_contains_dirac_source_plus_healthy_hook_kinetic":
            False,

        "hook17_q2_universal_metric_in_same_action":
            False,

        "same_action_noether_completion_derived":
            False,

        "field_redefinition_survival_derived":
            False,

        "same_action_complete":
            False,

        "literature_stitching_counts_as_same_action":
            False,

        "explicit_same_action_construction_attempt_authorized":
            bool(
                pole[
                    "hook_2plus_exact_pole_source_nonzero"
                ]
                or
                pole[
                    "hook_1plus_exact_pole_source_nonzero"
                ]
            ),
    }


def h17a2_summary() -> dict[
    str,
    Any,
]:
    """Return conservative promotion/falsification logic for 032H17A2."""
    pole = (
        timelike_rest_pole_projector_gate()
    )

    scan = (
        healthy_branch_identity_scan()
    )

    static = (
        static_fourier_source_gate()
    )

    provenance = (
        same_action_provenance_gate()
    )

    both_poles = bool(
        pole[
            "hook_2plus_exact_pole_source_nonzero"
        ]
        and
        pole[
            "hook_1plus_exact_pole_source_nonzero"
        ]
    )

    identities = bool(
        scan[
            "hook_2plus_identity_all_pass"
        ]
        and
        scan[
            "hook_1plus_identity_all_pass"
        ]
    )

    static_support = bool(
        static[
            "hook_2plus_generic_static_gradient_support_nonzero"
        ]
        and
        static[
            "hook_1plus_generic_static_gradient_support_nonzero"
        ]
    )

    authorize_action = bool(
        both_poles
        and
        identities
        and
        static_support
        and
        provenance[
            "explicit_same_action_construction_attempt_authorized"
        ]
    )

    if authorize_action:
        decision = (
            "GREEN_H17A2_"
            "V24_SOURCE_COUPLES_NONTRIVIALLY_TO_HEALTHY_"
            "HOOK_2PLUS_AND_1PLUS_POLE_SOURCES__"
            "SAME_ACTION_STILL_REQUIRED"
        )

        next_step = (
            "032H17A3_"
            "EXPLICIT_SINGLE_ACTION_DIRAC_HOOK_MAG_2PLUS_1PLUS_"
            "NOETHER_UNIVERSAL_METRIC_AND_FIELD_REDEFINITION_GATE"
        )

    else:
        decision = (
            "RED_H17A2_"
            "NO_HEALTHY_HOOK_SOURCE_PROJECTOR_SURVIVOR"
        )

        next_step = (
            "RETURN_TO_H17_F1_F3_OR_V26D_FALLBACK_RERANK"
        )

    return {
        "decision":
            decision,

        "next":
            next_step,

        "hook_2plus_exact_pole_source_nonzero":
            pole[
                "hook_2plus_exact_pole_source_nonzero"
            ],

        "hook_1plus_exact_pole_source_nonzero":
            pole[
                "hook_1plus_exact_pole_source_nonzero"
            ],

        "hook_2plus_raw_rest_norm2":
            pole[
                "hook_2plus_raw_spatial_norm2"
            ],

        "hook_1plus_raw_rest_norm2":
            pole[
                "hook_1plus_raw_spatial_norm2"
            ],

        "hook_2plus_canonical_identity_all_pass":
            scan[
                "hook_2plus_identity_all_pass"
            ],

        "hook_1plus_canonical_identity_all_pass":
            scan[
                "hook_1plus_identity_all_pass"
            ],

        "hook_2plus_static_generic_support_nonzero":
            static[
                "hook_2plus_generic_static_gradient_support_nonzero"
            ],

        "hook_1plus_static_generic_support_nonzero":
            static[
                "hook_1plus_generic_static_gradient_support_nonzero"
            ],

        "hook_2plus_static_unit_sphere_average_norm2":
            static[
                "hook_2plus_unit_sphere_angular_average_norm2"
            ],

        "hook_1plus_static_unit_sphere_average_norm2":
            static[
                "hook_1plus_unit_sphere_angular_average_norm2"
            ],

        "same_action_complete":
            provenance[
                "same_action_complete"
            ],

        "explicit_same_action_construction_attempt_authorized":
            authorize_action,

        "h17b_authorized":
            False,

        "energy_optimization_authorized":
            False,

        "mass_candidate_campaign_authorized":
            False,

        "action_oracle_authorized":
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
