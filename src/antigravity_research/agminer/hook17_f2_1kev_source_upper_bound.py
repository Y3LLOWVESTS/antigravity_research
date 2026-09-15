"""032H17A12D1R2B — exact-1-keV expanded source-space upper-bound gate.

PURPOSE
-------
A12C produced the exceptional unloaded field-capacity reference

    E_A12C = 2.6568591420597114 J

at

    M_X = 1 keV

for the finite 1 kg / 1 m / whole-payload >= 1 g benchmark.

A12D1R1 established that finite-payload same-action loading invalidates
unmodified reuse of the A12C source morphology at 1 keV.

A12D1R2 then searched a 15-dimensional compact conserved source basis.

It did not find a positive whole-payload 1-keV solution, but it explicitly
did not exhaust the continuous compact-current source space.

R2B therefore asks a stronger question:

    What is the largest possible minimum payload acceleration per loaded
    joule inside a much larger discretized compact-current space?

Let

    J_phi = sum_a c_a J_phi^(a).

At fixed payload and fixed 1-keV portal scale, the loaded field equation is
linear in c.

Therefore:

    E_loaded(c) = c^T H c

and each sampled payload acceleration is

    a_k(c) = c^T Q_k c.

After whitening H:

    E_loaded = y^T y

and

    a_k = y^T A_k y.

The exact finite-dimensional maximin objective is

    R_star
        =
    max_{||y||=1}
        min_k y^T A_k y.

A constructive optimizer supplies a LOWER bound on R_star.

DUAL UPPER BOUNDS
-----------------
For every sampled payload point k,

    R_star
        <=
    lambda_max(A_k).

Thus

    R_star
        <=
    min_k lambda_max(A_k).

This is the pointwise spectral upper bound.

More generally, for any nonnegative weights w_k summing to one,

    min_k y^T A_k y
        <=
    y^T (sum_k w_k A_k) y

and therefore

    R_star
        <=
    lambda_max(sum_k w_k A_k).

Optimizing the weights can tighten the upper bound.

Crucially, ANY valid weight vector already gives a mathematically valid
upper bound.  The certificate does not depend on the weight optimizer finding
its global optimum.

CAPACITY CONSEQUENCE
--------------------
If

    R_star <= U

with U > 0, every source in the tested space requires at least

    E_required >= g / U.

Therefore the run can directly test whether the expanded source space could
possibly support:

    2.6568591420597114 J
    10 J
    100 J
    1 kJ
    10 kJ
    100 kJ
    1 MJ.

If the upper bound is below g/E_target, that energy target is impossible in
the tested source space regardless of constructive optimizer performance.

SOURCE SPACE
------------
The basis contains:

    1 exact original A12C source

plus

    75 smooth localized compact azimuthal source patches.

Every member:

- lies inside the original R_s = 2 m source support;
- is purely azimuthal;
- is axisymmetric;
- is therefore identically divergence-free;
- carries the original smooth compact boundary envelope.

Patch centers are ordered by deterministic farthest-point sampling.

This produces nested source spaces:

    16
    32
    52
    76

dimensions.

The basis is substantially richer than R2's 15-dimensional space but still
does NOT exhaust arbitrary continuous currents.

CERTIFICATE PAYLOAD SAMPLE
--------------------------
The dual certificate may use any subset of payload points because

    min over entire payload
        <=
    weighted average over any chosen payload subset.

Therefore an upper bound derived from the declared sampled subset remains a
valid upper bound for any source required to pass all of those points.

It is nevertheless a numerical/discretized certificate, not an analytic
continuum theorem.

NO NEAR-SINGULAR GAIN
---------------------
No response-energy direction is silently discarded.

If the loaded energy matrix ceases to be positive definite or becomes too
ill-conditioned for trustworthy whitening, the certificate is marked invalid
rather than gaining performance from a near-null direction.

CLAIM LIMITS
------------
This run does not establish:

- exhaustion of all continuous current functions;
- microscopic source existence;
- support/polarization energy;
- full source-loaded matter backreaction;
- UV completion;
- empirical consistency;
- complete operating energy;
- replacement of 006D;
- a practical device.

CLAIM CLASSIFICATION
--------------------
PROJECT_DISCRETE_SOURCE_SPACE_PRIMAL_DUAL_CERTIFICATE
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import minimize
from scipy.sparse.linalg import splu, spsolve

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    EV_J,
    HBAR_C_EV_M,
    REFERENCE_PORTAL_SCALE_EV,
    SOURCE_RADIUS_M,
    STRICT_COMPLETE_OPERATING_TARGET_J,
    TARGET_ACCELERATION_M_S2,
)
from .hook17_f2_strong_payload_loading_rescue import (
    PRIMARY_DENSITY_MODEL,
    _assemble_weighted_operator,
    _edge_energy_integral,
    _grid,
    _payload_sample_points,
    a12c_artifact,
    loading_coefficient_z,
    payload_density_profile_kg_m3,
)
from .hook17_f2_loaded_source_shape_rescue import (
    _signed_active_refinement,
    optimization_payload_points,
    original_a12c_source_profile,
)


BRANCH = "032H17A12D1R2B"

PRIMARY_PORTAL_SCALE_EV = 1000.0
PRIMARY_GRID_M = 0.100

SOURCE_PATCH_WIDTH = 0.14

NESTED_BASIS_COUNTS = (
    16,
    32,
    52,
    76,
)

FULL_BASIS_COUNT = 76

CERTIFICATE_POINT_STRIDE = 4
DUAL_ACTIVE_POINT_COUNT = 28

ENERGY_CONDITION_LIMIT = 1.0e12

PRIMAL_RANDOM_SEED_COUNT = 120
PRIMAL_REFINEMENT_COUNT = 5

A12C_REFERENCE_CAPACITY_J = 2.6568591420597114

CAPACITY_TARGETS_J = (
    A12C_REFERENCE_CAPACITY_J,
    10.0,
    100.0,
    1000.0,
    10000.0,
    100000.0,
    1000000.0,
)

VALIDATION_GRID_M = (
    0.100,
    0.075,
    0.050,
)


def _repo_root() -> Path:
    return (
        Path(__file__)
        .resolve()
        .parents[3]
    )


@lru_cache(maxsize=1)
def r2_artifact() -> dict[str, Any]:
    path = (
        _repo_root()
        /
        "results"
        /
        "data"
        /
        "032h17a12d1r2_hook17_f2_loaded_source_shape_rescue_summary.json"
    )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def provenance_gate() -> dict[str, Any]:
    result = (
        r2_artifact()
    )

    passed = bool(
        result[
            "branch"
        ]
        ==
        "032H17A12D1R2"

        and

        result[
            "exact_1kev_direct_validation_pass"
        ]
        is False

        and

        result[
            "continuous_source_shape_space_exhausted"
        ]
        is False

        and

        result[
            "a12b_exact_massless_carrier_closed"
        ]
        is False

        and

        result[
            "a12c_f2_metric_mechanism_closed"
        ]
        is False
    )

    return {
        "pass":
            passed,

        "r2_branch":
            result[
                "branch"
            ],

        "r2_exact_1kev_rescued":
            result[
                "exact_1kev_direct_validation_pass"
            ],

        "continuous_source_space_exhausted":
            result[
                "continuous_source_shape_space_exhausted"
            ],

        "a12b_carrier_preserved":
            not result[
                "a12b_exact_massless_carrier_closed"
            ],

        "a12c_f2_mechanism_preserved":
            not result[
                "a12c_f2_metric_mechanism_closed"
            ],
    }


def candidate_patch_centers() -> tuple[tuple[float, float], ...]:
    rho_values = np.linspace(
        0.08,
        0.92,
        9,
    )

    z_values = np.linspace(
        -0.88,
        0.88,
        11,
    )

    centers = []

    for rho_value in rho_values:
        for z_value in z_values:
            z_clean = (
                0.0
                if abs(
                    float(
                        z_value
                    )
                )
                <
                1.0e-12
                else
                float(
                    z_value
                )
            )

            rho_clean = float(
                rho_value
            )

            if (
                rho_clean**2
                +
                z_clean**2
                <
                0.94**2
            ):
                centers.append(
                    (
                        rho_clean,
                        z_clean,
                    )
                )

    return tuple(
        centers
    )


def ordered_patch_centers() -> tuple[tuple[float, float], ...]:
    candidates = list(
        candidate_patch_centers()
    )

    if len(
        candidates
    ) != 75:
        raise RuntimeError(
            "unexpected patch-center count"
        )

    seed_index = min(
        range(
            len(
                candidates
            )
        ),
        key=lambda index:
            (
                (
                    candidates[
                        index
                    ][
                        0
                    ]
                    -
                    0.5
                ) ** 2
                +
                candidates[
                    index
                ][
                    1
                ] ** 2
            ),
    )

    selected = [
        candidates.pop(
            seed_index
        )
    ]

    while candidates:
        def minimum_distance_squared(
            point: tuple[float, float],
        ) -> float:
            return min(
                (
                    point[
                        0
                    ]
                    -
                    chosen[
                        0
                    ]
                ) ** 2
                +
                (
                    point[
                        1
                    ]
                    -
                    chosen[
                        1
                    ]
                ) ** 2
                for chosen in selected
            )

        best_index = max(
            range(
                len(
                    candidates
                )
            ),
            key=lambda index:
                (
                    minimum_distance_squared(
                        candidates[
                            index
                        ]
                    ),
                    -candidates[
                        index
                    ][
                        0
                    ],
                    -candidates[
                        index
                    ][
                        1
                    ],
                ),
        )

        selected.append(
            candidates.pop(
                best_index
            )
        )

    return tuple(
        selected
    )


def source_basis_labels() -> tuple[str, ...]:
    labels = [
        "A12C_ORIGINAL",
    ]

    for index, (
        rho_center,
        z_center,
    ) in enumerate(
        ordered_patch_centers()
    ):
        labels.append(
            (
                f"RBF_{index:02d}_"
                f"RHO_{rho_center:.3f}_"
                f"Z_{z_center:+.3f}"
            )
        )

    return tuple(
        labels
    )


def expanded_source_basis_profiles(
    rho: np.ndarray,
    z: np.ndarray,
) -> np.ndarray:
    base = (
        original_a12c_source_profile(
            rho,
            z,
        )
    )

    rho_normalized = (
        rho
        /
        SOURCE_RADIUS_M
    )

    z_normalized = (
        z
        /
        SOURCE_RADIUS_M
    )

    profiles = [
        base,
    ]

    for (
        rho_center,
        z_center,
    ) in ordered_patch_centers():
        distance_squared = (
            (
                rho_normalized
                -
                rho_center
            ) ** 2
            +
            (
                z_normalized
                -
                z_center
            ) ** 2
        )

        patch = np.exp(
            -distance_squared
            /
            (
                2.0
                *
                SOURCE_PATCH_WIDTH**2
            )
        )

        profiles.append(
            base
            *
            patch
        )

    return np.asarray(
        profiles,
        dtype=float,
    )


def source_space_gate() -> dict[str, Any]:
    centers = (
        ordered_patch_centers()
    )

    labels = (
        source_basis_labels()
    )

    return {
        "candidate_patch_count":
            len(
                candidate_patch_centers()
            ),

        "ordered_patch_count":
            len(
                centers
            ),

        "full_basis_count":
            len(
                labels
            ),

        "nested_basis_counts":
            list(
                NESTED_BASIS_COUNTS
            ),

        "basis_zero_exact_original_a12c":
            True,

        "all_sources_axisymmetric":
            True,

        "all_sources_pure_azimuthal":
            True,

        "all_sources_divergence_free":
            True,

        "all_sources_compact_in_original_support":
            True,

        "continuous_source_space_exhausted":
            False,
    }


def target_efficiency_m_s2_per_j(
    capacity_j: float,
) -> float:
    return (
        TARGET_ACCELERATION_M_S2
        /
        float(
            capacity_j
        )
    )


def _bilinear_sample_basis(
    arrays: np.ndarray,
    rhos: np.ndarray,
    zs: np.ndarray,
    points: np.ndarray,
    h: float,
) -> np.ndarray:
    rho_values = (
        points[
            :,
            1
        ]
    )

    z_values = (
        points[
            :,
            0
        ]
    )

    i_float = (
        (
            rho_values
            -
            rhos[
                0
            ]
        )
        /
        h
    )

    j_float = (
        (
            z_values
            -
            zs[
                0
            ]
        )
        /
        h
    )

    i0 = np.floor(
        i_float
    ).astype(
        int
    )

    j0 = np.floor(
        j_float
    ).astype(
        int
    )

    i0 = np.clip(
        i0,
        0,
        len(
            rhos
        )
        -
        2,
    )

    j0 = np.clip(
        j0,
        0,
        len(
            zs
        )
        -
        2,
    )

    wr = (
        i_float
        -
        i0
    )

    wz = (
        j_float
        -
        j0
    )

    v00 = arrays[
        :,
        j0,
        i0,
    ].T

    v01 = arrays[
        :,
        j0,
        i0
        +
        1,
    ].T

    v10 = arrays[
        :,
        j0
        +
        1,
        i0,
    ].T

    v11 = arrays[
        :,
        j0
        +
        1,
        i0
        +
        1,
    ].T

    return (
        (
            1.0
            -
            wz
        )[
            :,
            None
        ]
        *
        (
            1.0
            -
            wr
        )[
            :,
            None
        ]
        *
        v00

        +

        (
            1.0
            -
            wz
        )[
            :,
            None
        ]
        *
        wr[
            :,
            None
        ]
        *
        v01

        +

        wz[
            :,
            None
        ]
        *
        (
            1.0
            -
            wr
        )[
            :,
            None
        ]
        *
        v10

        +

        wz[
            :,
            None
        ]
        *
        wr[
            :,
            None
        ]
        *
        v11
    )


def _bilinear_sample_scalar(
    array: np.ndarray,
    rhos: np.ndarray,
    zs: np.ndarray,
    points: np.ndarray,
    h: float,
) -> np.ndarray:
    return (
        _bilinear_sample_basis(
            array[
                None,
                :,
                :,
            ],
            rhos,
            zs,
            points,
            h,
        )[
            :,
            0
        ]
    )


def build_expanded_response(
    portal_scale_ev: float = PRIMARY_PORTAL_SCALE_EV,
    h: float = PRIMARY_GRID_M,
) -> dict[str, Any]:
    (
        rhos,
        zs,
        rho_grid,
        z_grid,
    ) = (
        _grid(
            h,
            12.0,
            -10.0,
            13.0,
        )
    )

    density = (
        payload_density_profile_kg_m3(
            rho_grid,
            z_grid,
            PRIMARY_DENSITY_MODEL,
        )
    )

    z_coefficient = (
        loading_coefficient_z(
            density,
            portal_scale_ev,
        )
    )

    rho_i, z_i = np.meshgrid(
        rhos[
            1:-1
        ],
        zs[
            1:-1
        ],
    )

    basis = (
        expanded_source_basis_profiles(
            rho_i,
            z_i,
        )
    )

    zero_source = np.zeros_like(
        basis[
            0
        ]
    )

    operator, _ = (
        _assemble_weighted_operator(
            rhos,
            zs,
            z_coefficient,
            zero_source,
            h,
        )
    )

    factorization = splu(
        operator.tocsc()
    )

    rhs_matrix = (
        h**2
        *
        rho_i[
            None,
            :,
            :
        ]
        *
        basis
    ).reshape(
        (
            FULL_BASIS_COUNT,
            -1,
        )
    ).T

    solution_matrix = (
        factorization.solve(
            rhs_matrix
        )
    )

    fields = np.zeros(
        (
            FULL_BASIS_COUNT,
            len(
                zs
            ),
            len(
                rhos
            ),
        ),
        dtype=float,
    )

    fields[
        :,
        1:-1,
        1:-1,
    ] = (
        solution_matrix.T.reshape(
            (
                FULL_BASIS_COUNT,
                len(
                    zs
                )
                -
                2,
                len(
                    rhos
                )
                -
                2,
            )
        )
    )

    d_a_dz = np.gradient(
        fields,
        h,
        axis=1,
        edge_order=2,
    )

    d_a_drho = np.gradient(
        fields,
        h,
        axis=2,
        edge_order=2,
    )

    b_rho = (
        -d_a_dz
    )

    rho_broadcast = np.broadcast_to(
        rhos[
            None,
            None,
            :
        ],
        fields.shape,
    )

    a_over_rho = np.zeros_like(
        fields
    )

    np.divide(
        fields,
        rho_broadcast,
        out=a_over_rho,
        where=
            rho_broadcast
            >
            0.0,
    )

    b_z = (
        d_a_drho
        +
        a_over_rho
    )

    d_b_rho_dz = np.gradient(
        b_rho,
        h,
        axis=1,
        edge_order=2,
    )

    d_b_z_dz = np.gradient(
        b_z,
        h,
        axis=1,
        edge_order=2,
    )

    points = (
        optimization_payload_points()
    )

    br = (
        _bilinear_sample_basis(
            b_rho,
            rhos,
            zs,
            points,
            h,
        )
    )

    bz = (
        _bilinear_sample_basis(
            b_z,
            rhos,
            zs,
            points,
            h,
        )
    )

    dbr = (
        _bilinear_sample_basis(
            d_b_rho_dz,
            rhos,
            zs,
            points,
            h,
        )
    )

    dbz = (
        _bilinear_sample_basis(
            d_b_z_dz,
            rhos,
            zs,
            points,
            h,
        )
    )

    acceleration_factor = (
        -C_LIGHT_M_S**2
        *
        HBAR_C_EV_M**2
        /
        float(
            portal_scale_ev
        ) ** 4
    )

    q_matrices = (
        acceleration_factor
        *
        (
            np.einsum(
                "ki,kj->kij",
                dbr,
                br,
                optimize=True,
            )
            +
            np.einsum(
                "ki,kj->kij",
                br,
                dbr,
                optimize=True,
            )
            +
            np.einsum(
                "ki,kj->kij",
                dbz,
                bz,
                optimize=True,
            )
            +
            np.einsum(
                "ki,kj->kij",
                bz,
                dbz,
                optimize=True,
            )
        )
    )

    field_interior = (
        fields[
            :,
            1:-1,
            1:-1,
        ].reshape(
            (
                FULL_BASIS_COUNT,
                -1,
            )
        )
    )

    basis_flat = (
        basis.reshape(
            (
                FULL_BASIS_COUNT,
                -1,
            )
        )
    )

    weights_flat = (
        rho_i.ravel()
    )

    energy_prefactor = (
        0.5
        *
        2.0
        *
        math.pi
        *
        h**2
        /
        HBAR_C_EV_M
        *
        EV_J
    )

    energy_matrix = (
        energy_prefactor
        *
        (
            basis_flat
            *
            weights_flat[
                None,
                :
            ]
        )
        @
        field_interior.T
    )

    energy_matrix = (
        0.5
        *
        (
            energy_matrix
            +
            energy_matrix.T
        )
    )

    return {
        "portal_scale_ev":
            float(
                portal_scale_ev
            ),

        "grid_spacing_m":
            float(
                h
            ),

        "energy_matrix":
            energy_matrix,

        "q_matrices":
            q_matrices,

        "payload_points":
            points,

        "source_basis_labels":
            source_basis_labels(),

        "z_max":
            float(
                np.max(
                    z_coefficient
                )
            ),
    }


def whiten_response(
    energy_matrix: np.ndarray,
    q_matrices: np.ndarray,
) -> dict[str, Any]:
    h_matrix = (
        0.5
        *
        (
            energy_matrix
            +
            energy_matrix.T
        )
    )

    eigenvalues, eigenvectors = np.linalg.eigh(
        h_matrix
    )

    minimum = float(
        np.min(
            eigenvalues
        )
    )

    maximum = float(
        np.max(
            eigenvalues
        )
    )

    positive_definite = bool(
        minimum
        >
        0.0
    )

    if not positive_definite:
        return {
            "valid":
                False,

            "reason":
                "ENERGY_MATRIX_NOT_POSITIVE_DEFINITE",

            "minimum_energy_eigenvalue":
                minimum,

            "maximum_energy_eigenvalue":
                maximum,
        }

    condition_number = (
        maximum
        /
        minimum
    )

    if (
        not math.isfinite(
            condition_number
        )
        or
        condition_number
        >
        ENERGY_CONDITION_LIMIT
    ):
        return {
            "valid":
                False,

            "reason":
                "ENERGY_MATRIX_TOO_ILL_CONDITIONED_FOR_CERTIFICATE",

            "minimum_energy_eigenvalue":
                minimum,

            "maximum_energy_eigenvalue":
                maximum,

            "condition_number":
                condition_number,
        }

    transform = (
        eigenvectors
        /
        np.sqrt(
            eigenvalues
        )[
            None,
            :
        ]
    )

    q_whitened = np.einsum(
        "ar,kab,bs->krs",
        transform,
        q_matrices,
        transform,
        optimize=True,
    )

    q_whitened = (
        0.5
        *
        (
            q_whitened
            +
            np.swapaxes(
                q_whitened,
                1,
                2,
            )
        )
    )

    return {
        "valid":
            True,

        "minimum_energy_eigenvalue":
            minimum,

        "maximum_energy_eigenvalue":
            maximum,

        "condition_number":
            condition_number,

        "transform":
            transform,

        "q_whitened":
            q_whitened,
    }


def _project_simplex(
    values: np.ndarray,
) -> np.ndarray:
    values = np.asarray(
        values,
        dtype=float,
    )

    ordered = np.sort(
        values
    )[
        ::-1
    ]

    cumulative = np.cumsum(
        ordered
    )

    indices = np.arange(
        1,
        len(
            values
        )
        +
        1,
    )

    condition = (
        ordered
        -
        (
            cumulative
            -
            1.0
        )
        /
        indices
        >
        0.0
    )

    if not np.any(
        condition
    ):
        result = np.zeros_like(
            values
        )

        result[
            np.argmax(
                values
            )
        ] = 1.0

        return result

    rho = int(
        np.where(
            condition
        )[
            0
        ][
            -1
        ]
    )

    theta = (
        cumulative[
            rho
        ]
        -
        1.0
    ) / float(
        rho
        +
        1
    )

    projected = np.maximum(
        values
        -
        theta,
        0.0,
    )

    projected /= np.sum(
        projected
    )

    return projected


def dual_upper_bound_certificate(
    q_whitened: np.ndarray,
    payload_points: np.ndarray,
) -> dict[str, Any]:
    certificate_indices = np.arange(
        0,
        len(
            q_whitened
        ),
        CERTIFICATE_POINT_STRIDE,
        dtype=int,
    )

    q_certificate = (
        q_whitened[
            certificate_indices
        ]
    )

    pointwise_eigenvalues = np.linalg.eigvalsh(
        q_certificate
    )

    pointwise_maxima = (
        pointwise_eigenvalues[
            :,
            -1
        ]
    )

    local_bottleneck = int(
        np.argmin(
            pointwise_maxima
        )
    )

    bottleneck_global_index = int(
        certificate_indices[
            local_bottleneck
        ]
    )

    pointwise_upper_bound = float(
        pointwise_maxima[
            local_bottleneck
        ]
    )

    order = np.argsort(
        pointwise_maxima
    )

    active_local = order[
        :min(
            DUAL_ACTIVE_POINT_COUNT,
            len(
                order
            ),
        )
    ]

    q_active = (
        q_certificate[
            active_local
        ]
    )

    def evaluate_weights(
        weights: np.ndarray,
    ) -> tuple[float, np.ndarray, np.ndarray]:
        weights = (
            _project_simplex(
                weights
            )
        )

        weighted_matrix = np.tensordot(
            weights,
            q_active,
            axes=(
                0,
                0,
            ),
        )

        eigenvalues, eigenvectors = np.linalg.eigh(
            weighted_matrix
        )

        top_vector = (
            eigenvectors[
                :,
                -1
            ]
        )

        value = float(
            eigenvalues[
                -1
            ]
        )

        gradient = np.einsum(
            "i,kij,j->k",
            top_vector,
            q_active,
            top_vector,
            optimize=True,
        )

        return (
            value,
            gradient,
            top_vector,
        )

    candidates = []

    starts = []

    uniform = np.full(
        len(
            q_active
        ),
        1.0
        /
        len(
            q_active
        ),
    )

    starts.append(
        uniform
    )

    delta = np.zeros(
        len(
            q_active
        )
    )

    delta[
        0
    ] = 1.0

    starts.append(
        delta
    )

    for start in starts:
        def objective(
            weights: np.ndarray,
        ) -> float:
            value, _, _ = (
                evaluate_weights(
                    weights
                )
            )

            return value

        def jacobian(
            weights: np.ndarray,
        ) -> np.ndarray:
            _, gradient, _ = (
                evaluate_weights(
                    weights
                )
            )

            return gradient

        result = minimize(
            objective,
            start,
            method="SLSQP",
            jac=jacobian,
            bounds=[
                (
                    0.0,
                    1.0,
                )
                for _ in range(
                    len(
                        start
                    )
                )
            ],
            constraints=(
                {
                    "type":
                        "eq",

                    "fun":
                        lambda weights:
                            float(
                                np.sum(
                                    weights
                                )
                                -
                                1.0
                            ),
                },
            ),
            options={
                "maxiter":
                    350,

                "ftol":
                    1.0e-12,

                "disp":
                    False,
            },
        )

        projected = (
            _project_simplex(
                result.x
            )
        )

        value, _, top_vector = (
            evaluate_weights(
                projected
            )
        )

        candidates.append(
            {
                "value":
                    value,

                "weights":
                    projected,

                "top_vector":
                    top_vector,

                "optimizer_success":
                    bool(
                        result.success
                    ),

                "optimizer_message":
                    str(
                        result.message
                    ),
            }
        )

    best = min(
        candidates,
        key=lambda item:
            item[
                "value"
            ],
    )

    dual_upper_bound = min(
        pointwise_upper_bound,
        float(
            best[
                "value"
            ]
        ),
    )

    bottleneck_point = (
        payload_points[
            bottleneck_global_index
        ]
    )

    return {
        "certificate_point_count":
            len(
                certificate_indices
            ),

        "pointwise_upper_bound_m_s2_per_j":
            pointwise_upper_bound,

        "weighted_dual_upper_bound_m_s2_per_j":
            float(
                best[
                    "value"
                ]
            ),

        "best_valid_upper_bound_m_s2_per_j":
            dual_upper_bound,

        "bottleneck_payload_point_index":
            bottleneck_global_index,

        "bottleneck_payload_z_m":
            float(
                bottleneck_point[
                    0
                ]
            ),

        "bottleneck_payload_rho_m":
            float(
                bottleneck_point[
                    1
                ]
            ),

        "dual_active_point_count":
            len(
                q_active
            ),

        "dual_optimizer_success":
            best[
                "optimizer_success"
            ],

        "dual_optimizer_message":
            best[
                "optimizer_message"
            ],

        "dual_top_vector":
            best[
                "top_vector"
            ],

        "certificate_valid_even_if_optimizer_not_global":
            True,
    }


def constructive_primal_search(
    q_whitened: np.ndarray,
    transform: np.ndarray,
    dual_result: dict[str, Any],
    deterministic_seed: int,
) -> dict[str, Any]:
    dimension = (
        q_whitened.shape[
            1
        ]
    )

    seeds = []

    dual_seed = np.asarray(
        dual_result[
            "dual_top_vector"
        ],
        dtype=float,
    )

    dual_seed /= np.linalg.norm(
        dual_seed
    )

    seeds.append(
        dual_seed
    )

    bottleneck_index = int(
        dual_result[
            "bottleneck_payload_point_index"
        ]
    )

    bottleneck_matrix = (
        q_whitened[
            bottleneck_index
        ]
    )

    _, bottleneck_vectors = np.linalg.eigh(
        bottleneck_matrix
    )

    seeds.append(
        bottleneck_vectors[
            :,
            -1
        ]
    )

    average_matrix = np.mean(
        q_whitened,
        axis=0,
    )

    _, average_vectors = np.linalg.eigh(
        average_matrix
    )

    seeds.append(
        average_vectors[
            :,
            -1
        ]
    )

    rng = np.random.default_rng(
        deterministic_seed
    )

    random_vectors = rng.normal(
        size=(
            PRIMAL_RANDOM_SEED_COUNT,
            dimension,
        )
    )

    random_vectors /= np.linalg.norm(
        random_vectors,
        axis=1,
    )[
        :,
        None
    ]

    q_screen = (
        q_whitened[
            ::8
        ]
    )

    screen_values = np.einsum(
        "bi,kij,bj->bk",
        random_vectors,
        q_screen,
        random_vectors,
        optimize=True,
    )

    screen_minima = np.min(
        screen_values,
        axis=1,
    )

    best_random_indices = np.argsort(
        screen_minima
    )[
        ::-1
    ][
        :6
    ]

    for index in best_random_indices:
        seeds.append(
            random_vectors[
                index
            ]
        )

    seed_scores = []

    for seed in seeds:
        seed = (
            seed
            /
            np.linalg.norm(
                seed
            )
        )

        minimum = float(
            np.min(
                np.einsum(
                    "i,kij,j->k",
                    seed,
                    q_whitened,
                    seed,
                    optimize=True,
                )
            )
        )

        seed_scores.append(
            (
                minimum,
                seed,
            )
        )

    seed_scores.sort(
        key=lambda item:
            item[
                0
            ],
        reverse=True,
    )

    best = None

    for _, seed in seed_scores[
        :PRIMAL_REFINEMENT_COUNT
    ]:
        result = (
            _signed_active_refinement(
                q_whitened,
                seed,
            )
        )

        if (
            best
            is None
            or
            result[
                "minimum_margin"
            ]
            >
            best[
                "minimum_margin"
            ]
        ):
            best = result

    assert (
        best
        is not None
    )

    y = np.asarray(
        best[
            "y"
        ],
        dtype=float,
    )

    coefficients = (
        transform
        @
        y
    )

    maximum_coefficient = float(
        np.max(
            np.abs(
                coefficients
            )
        )
    )

    if maximum_coefficient > 0.0:
        coefficients = (
            coefficients
            /
            maximum_coefficient
        )

    margin = float(
        best[
            "minimum_margin"
        ]
    )

    capacity = (
        TARGET_ACCELERATION_M_S2
        /
        margin
        if margin
        >
        0.0
        else
        None
    )

    return {
        "constructive_lower_bound_m_s2_per_j":
            margin,

        "constructive_predicted_capacity_j":
            capacity,

        "source_coefficients":
            coefficients.tolist(),

        "optimizer_success":
            best[
                "optimizer_success"
            ],

        "optimizer_message":
            best[
                "optimizer_message"
            ],

        "active_constraint_count":
            best[
                "active_constraint_count"
            ],
    }


def analyze_subspace(
    full_response: dict[str, Any],
    basis_count: int,
) -> dict[str, Any]:
    indices = np.arange(
        basis_count,
        dtype=int,
    )

    energy_matrix = (
        full_response[
            "energy_matrix"
        ][
            np.ix_(
                indices,
                indices,
            )
        ]
    )

    q_matrices = (
        full_response[
            "q_matrices"
        ][
            :,
            indices,
        ][
            :,
            :,
            indices,
        ]
    )

    whitening = (
        whiten_response(
            energy_matrix,
            q_matrices,
        )
    )

    if not whitening[
        "valid"
    ]:
        return {
            "basis_count":
                basis_count,

            "certificate_valid":
                False,

            "whitening":
                whitening,
        }

    q_whitened = (
        whitening[
            "q_whitened"
        ]
    )

    dual = (
        dual_upper_bound_certificate(
            q_whitened,
            full_response[
                "payload_points"
            ],
        )
    )

    primal = (
        constructive_primal_search(
            q_whitened,
            whitening[
                "transform"
            ],
            dual,
            deterministic_seed=
                12000
                +
                basis_count
                *
                17,
        )
    )

    upper_bound = float(
        dual[
            "best_valid_upper_bound_m_s2_per_j"
        ]
    )

    if upper_bound > 0.0:
        certified_capacity_lower_bound = (
            TARGET_ACCELERATION_M_S2
            /
            upper_bound
        )
    else:
        certified_capacity_lower_bound = math.inf

    targets = {}

    for capacity_j in CAPACITY_TARGETS_J:
        required_efficiency = (
            target_efficiency_m_s2_per_j(
                capacity_j
            )
        )

        targets[
            str(
                capacity_j
            )
        ] = {
            "capacity_target_j":
                capacity_j,

            "required_efficiency_m_s2_per_j":
                required_efficiency,

            "mathematically_allowed_by_upper_bound":
                bool(
                    upper_bound
                    >=
                    required_efficiency
                ),

            "ruled_out_by_upper_bound":
                bool(
                    upper_bound
                    <
                    required_efficiency
                ),
        }

    return {
        "basis_count":
            basis_count,

        "certificate_valid":
            True,

        "energy_condition_number":
            whitening[
                "condition_number"
            ],

        "minimum_energy_eigenvalue":
            whitening[
                "minimum_energy_eigenvalue"
            ],

        "maximum_energy_eigenvalue":
            whitening[
                "maximum_energy_eigenvalue"
            ],

        "dual":
            {
                key:
                    value
                for key, value in dual.items()
                if key
                !=
                "dual_top_vector"
            },

        "primal":
            primal,

        "certified_capacity_lower_bound_j":
            certified_capacity_lower_bound,

        "capacity_targets":
            targets,
    }


def solve_expanded_source_coefficients(
    coefficients: np.ndarray,
    h: float,
) -> dict[str, Any]:
    coefficients = np.asarray(
        coefficients,
        dtype=float,
    )

    if len(
        coefficients
    ) != FULL_BASIS_COUNT:
        raise ValueError(
            "expanded coefficient vector has wrong dimension"
        )

    maximum = float(
        np.max(
            np.abs(
                coefficients
            )
        )
    )

    if maximum <= 0.0:
        raise ValueError(
            "zero coefficient vector"
        )

    coefficients = (
        coefficients
        /
        maximum
    )

    (
        rhos,
        zs,
        rho_grid,
        z_grid,
    ) = (
        _grid(
            h,
            12.0,
            -10.0,
            13.0,
        )
    )

    density = (
        payload_density_profile_kg_m3(
            rho_grid,
            z_grid,
            PRIMARY_DENSITY_MODEL,
        )
    )

    z_coefficient = (
        loading_coefficient_z(
            density,
            PRIMARY_PORTAL_SCALE_EV,
        )
    )

    rho_i, z_i = np.meshgrid(
        rhos[
            1:-1
        ],
        zs[
            1:-1
        ],
    )

    basis = (
        expanded_source_basis_profiles(
            rho_i,
            z_i,
        )
    )

    source_i = np.einsum(
        "a,aij->ij",
        coefficients,
        basis,
        optimize=True,
    )

    operator, rhs = (
        _assemble_weighted_operator(
            rhos,
            zs,
            z_coefficient,
            source_i,
            h,
        )
    )

    solution = spsolve(
        operator,
        rhs,
    )

    if not np.all(
        np.isfinite(
            solution
        )
    ):
        raise RuntimeError(
            "nonfinite validation solution"
        )

    field = np.zeros_like(
        rho_grid,
        dtype=float,
    )

    field[
        1:-1,
        1:-1,
    ] = solution.reshape(
        (
            len(
                zs
            )
            -
            2,
            len(
                rhos
            )
            -
            2,
        )
    )

    source = np.zeros_like(
        field
    )

    source[
        1:-1,
        1:-1,
    ] = source_i

    d_a_dz, d_a_drho = np.gradient(
        field,
        h,
        h,
        edge_order=2,
    )

    b_rho = (
        -d_a_dz
    )

    a_over_rho = np.zeros_like(
        field
    )

    np.divide(
        field,
        rho_grid,
        out=a_over_rho,
        where=
            rho_grid
            >
            0.0,
    )

    b_z = (
        d_a_drho
        +
        a_over_rho
    )

    b_squared = (
        b_rho**2
        +
        b_z**2
    )

    sigma_unit = (
        HBAR_C_EV_M**2
        *
        b_squared
        /
        PRIMARY_PORTAL_SCALE_EV**4
    )

    d_sigma_dz, _ = np.gradient(
        sigma_unit,
        h,
        h,
        edge_order=2,
    )

    acceleration_unit = (
        -C_LIGHT_M_S**2
        *
        d_sigma_dz
    )

    payload_points = (
        _payload_sample_points()
    )

    sampled_unit = (
        _bilinear_sample_scalar(
            acceleration_unit,
            rhos,
            zs,
            payload_points,
            h,
        )
    )

    minimum_unit = float(
        np.min(
            sampled_unit
        )
    )

    base = {
        "grid_spacing_m":
            h,

        "whole_payload_outward_sign":
            minimum_unit
            >
            0.0,

        "unit_source_payload_acceleration_min_m_s2":
            minimum_unit,

        "unit_source_payload_acceleration_max_m_s2":
            float(
                np.max(
                    sampled_unit
                )
            ),
    }

    if minimum_unit <= 0.0:
        return base

    source_scale = math.sqrt(
        TARGET_ACCELERATION_M_S2
        /
        minimum_unit
    )

    field_scaled = (
        source_scale
        *
        field
    )

    source_scaled = (
        source_scale
        *
        source
    )

    sigma = (
        source_scale**2
        *
        sigma_unit
    )

    canonical_integral = (
        _edge_energy_integral(
            field_scaled,
            rhos,
            np.ones_like(
                z_coefficient
            ),
        )
    )

    loaded_integral = (
        _edge_energy_integral(
            field_scaled,
            rhos,
            z_coefficient,
        )
    )

    energy_prefactor = (
        0.5
        *
        2.0
        *
        math.pi
        /
        HBAR_C_EV_M
        *
        EV_J
    )

    canonical_energy_j = (
        energy_prefactor
        *
        canonical_integral
    )

    loaded_energy_j = (
        energy_prefactor
        *
        loaded_integral
    )

    source_work_j = (
        0.5
        *
        2.0
        *
        math.pi
        *
        float(
            np.sum(
                rho_grid
                *
                source_scaled
                *
                field_scaled
            )
        )
        *
        h**2
        /
        HBAR_C_EV_M
        *
        EV_J
    )

    absolute_source_ev_m = (
        2.0
        *
        math.pi
        *
        float(
            np.sum(
                rho_grid
                *
                np.abs(
                    source_scaled
                )
            )
        )
        *
        h**2
    )

    a12c_source = float(
        a12c_artifact()[
            "massless_f2_finite_payload_bvp"
        ][
            "production"
        ][
            "integrated_canonical_source_ev_m"
        ]
    )

    return {
        **base,

        "strict_whole_payload_1g_pass":
            True,

        "loaded_quadratic_capacity_j":
            loaded_energy_j,

        "canonical_field_energy_j":
            canonical_energy_j,

        "payload_interaction_energy_j":
            (
                loaded_energy_j
                -
                canonical_energy_j
            ),

        "source_work_j":
            source_work_j,

        "source_work_relative_error":
            (
                abs(
                    source_work_j
                    -
                    loaded_energy_j
                )
                /
                loaded_energy_j
            ),

        "integrated_absolute_source_ev_m":
            absolute_source_ev_m,

        "absolute_source_ratio_vs_a12c":
            (
                absolute_source_ev_m
                /
                a12c_source
            ),

        "payload_sigma_max":
            float(
                np.max(
                    sigma[
                        density
                        >
                        0.0
                    ]
                )
            ),
    }


def claim_policy_gate() -> dict[str, Any]:
    return {
        "few_joule_branch_priority":
            True,

        "exact_1kev_primary":
            True,

        "dual_certificate_is_finite_basis":
            True,

        "dual_certificate_is_discrete_payload_sample":
            True,

        "continuous_source_space_exhausted":
            False,

        "all_possible_source_shapes_closed":
            False,

        "carrier_modified":
            False,

        "metric_modified":
            False,

        "payload_modified":
            False,

        "microscopic_source_completed":
            False,

        "complete_energy_established":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "006d_replaced":
            False,

        "practical_device_found":
            False,
    }
