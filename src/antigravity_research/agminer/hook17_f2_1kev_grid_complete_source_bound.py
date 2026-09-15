"""032H17A12D1R2B1 — grid-complete arbitrary-current 1-keV source bound.

PURPOSE
-------
A12C established the remarkable unloaded reference:

    portal scale:
        M_X = 1 keV

    canonical field energy:
        2.6568591420597114 J

    finite neutral payload:
        1 kg

    external stand-off:
        1 m

    whole sampled payload:
        >= 1 g outward.

A12D1/R1 showed that finite same-action payload loading invalidates direct
reuse of the unloaded A12C field at 1 keV.

R2 tested 15 compact conserved current modes.

R2B enlarged that to 76 smooth compact modes and produced finite-dimensional
upper bounds.  However its weighted-dual bound was not stable under basis
enlargement.

R2B1 therefore removes the smooth finite-basis ansatz as aggressively as is
reasonable on the existing PDE grid.

Every interior grid cell inside the original 2 m source support is assigned
an independent axisymmetric azimuthal current degree of freedom.

Because

    J = J_phi(rho,z) e_phi

and there is no phi dependence,

    div J = 0

identically.

Thus this source space is still locally conserved, but it is deliberately
more permissive than a realistic smooth microscopic current.

If a low-capacity solution is impossible even in this optimistic grid-cell
space, every smooth source represented on the same grid is also excluded.

STATIC LOADED OPERATOR
----------------------
The same-action payload-loaded magnetostatic equation is

    curl[ Z(x) B ] = J

with

    Z(x)
        =
    1 + 2 rho_E(x)/M_X^4.

The run keeps

    M_X = 1 keV

and the optimistic finite-payload density profile already declared in R1.

The discrete positive loaded operator is

    K A = b.

Each independent source degree of freedom is most conveniently represented
by one independent RHS entry b_a on a source-support grid cell.

Since every source cell has rho > 0,

    b_a = h^2 rho_a J_phi,a

is a one-to-one reparameterization of arbitrary J_phi on those cells.

No physical source freedom is lost by using b rather than J_phi.

LOADED ENERGY
-------------
For arbitrary source RHS vector b restricted to the source cells,

    A = K^{-1} S b,

and the loaded quadratic capacity is

    E_loaded
        =
    C_E b^T S^T K^{-1} S b

where

    C_E
        =
    pi EV_J / (hbar c).

Therefore the source-space loaded-energy matrix is

    H
        =
    C_E S^T K^{-1} S.

Because K is positive definite, H must also be positive definite for
independent source cells.

POINTWISE ACCELERATION BOUND
----------------------------
At one payload point the four linear field observables

    v
        =
    (
        B_rho,
        B_z,
        partial_z B_rho,
        partial_z B_z
    )

are linear in the source vector:

    v = O b.

For the conformal F^2 metric,

    a_z
        =
    -c^2 (hbar c)^2 / M_X^4
    *
    partial_z(B_rho^2 + B_z^2).

Hence

    a_z
        =
    b^T Q b

with Q having rank at most four.

The maximum possible acceleration per loaded joule at that point is exactly

    lambda_max(Q, H).

Any source that accelerates the WHOLE payload outward must accelerate every
individual sampled payload point outward.

Therefore

    R_whole
        <=
    min_k lambda_max(Q_k, H).

This produces a rigorous upper bound for the declared discretized source
space and payload sample.

It is weaker than a multi-point weighted dual, but it is far less sensitive
to dual-weight optimization.

GRID-COMPLETE HERE MEANS
------------------------
Every source-bearing cell of the declared finite-difference grid is free.

It does NOT mean:

- continuum-current space is exhausted;
- non-axisymmetric currents are exhausted;
- derivative/nonlocal portals are exhausted;
- alternative source support is exhausted;
- the A12B carrier is closed;
- the A12C low-capacity clue is discarded.

The calculation is repeated at

    h = 0.125 m
    h = 0.100 m

so that the conclusion is not based on one source discretization.

CAPACITY TARGETS
----------------
For target acceleration g, an energy target E requires

    R_required = g/E.

The run directly tests:

    2.6568591420597114 J
    10 J
    100 J
    1 kJ
    10 kJ
    100 kJ
    1 MJ
    10 MJ.

PRIOR R2B DECISION-STRING REPAIR
--------------------------------
The R2B artifact simultaneously recorded

    A12C_2P656859J_RULED_OUT_IN_TESTED_SPACE = True

and a decision string claiming that few-joule mathematical headroom remained.

Those statements are logically inconsistent.

R2B1 preserves the numeric artifact but explicitly records that historical
decision-string inconsistency rather than silently inheriting it.

CLAIM CLASSIFICATION
--------------------
PROJECT_GRID_COMPLETE_DISCRETE_SOURCE_POINTWISE_CERTIFICATE
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.sparse.linalg import splu

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    EV_J,
    HBAR_C_EV_M,
    SOURCE_RADIUS_M,
    TARGET_ACCELERATION_M_S2,
)
from .hook17_f2_strong_payload_loading_rescue import (
    PRIMARY_DENSITY_MODEL,
    _assemble_weighted_operator,
    _grid,
    loading_coefficient_z,
    payload_density_profile_kg_m3,
)
from .hook17_f2_loaded_source_shape_rescue import (
    optimization_payload_points,
)
from .hook17_f2_1kev_source_upper_bound import (
    A12C_REFERENCE_CAPACITY_J,
    _bilinear_sample_basis,
)


BRANCH = "032H17A12D1R2B1"

PORTAL_SCALE_EV = 1000.0

CERTIFICATE_GRID_SPACINGS_M = (
    0.125,
    0.100,
)

SOURCE_SOLVE_BATCH_SIZE = 24

CAPACITY_TARGETS_J = (
    A12C_REFERENCE_CAPACITY_J,
    10.0,
    100.0,
    1000.0,
    10000.0,
    100000.0,
    1000000.0,
    10000000.0,
)

ENERGY_CONDITION_LIMIT = 1.0e14

GRID_BOUND_STABILITY_RELATIVE_TOL = 0.50


def _repo_root() -> Path:
    return (
        Path(__file__)
        .resolve()
        .parents[3]
    )


@lru_cache(maxsize=1)
def r2b_artifact() -> dict[str, Any]:
    path = (
        _repo_root()
        /
        "results"
        /
        "data"
        /
        "032h17a12d1r2b_hook17_f2_1kev_source_upper_bound_summary.json"
    )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def provenance_gate() -> dict[str, Any]:
    result = (
        r2b_artifact()
    )

    full = (
        result[
            "nested_analyses"
        ][
            "76"
        ]
    )

    numerical_flag = bool(
        result[
            "a12c_2p656859j_ruled_out_in_tested_space"
        ]
    )

    decision_claims_headroom = (
        "STILL_LEAVES_FEW_JOULE_MATHEMATICAL_HEADROOM"
        in
        result[
            "decision"
        ]
    )

    logic_inconsistency = bool(
        numerical_flag
        and
        decision_claims_headroom
    )

    passed = bool(
        result[
            "branch"
        ]
        ==
        "032H17A12D1R2B"

        and

        result[
            "full_basis_certificate_valid"
        ]
        is True

        and

        result[
            "continuous_source_space_exhausted"
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

        and

        full[
            "dual"
        ][
            "pointwise_upper_bound_m_s2_per_j"
        ]
        >
        0.0
    )

    return {
        "pass":
            passed,

        "r2b_branch":
            result[
                "branch"
            ],

        "r2b_full_basis_certificate_valid":
            result[
                "full_basis_certificate_valid"
            ],

        "r2b_numeric_a12c_target_ruled_out":
            numerical_flag,

        "r2b_decision_string_claimed_few_joule_headroom":
            decision_claims_headroom,

        "r2b_decision_string_logic_inconsistent":
            logic_inconsistency,

        "r2b_76d_pointwise_upper_bound_m_s2_per_j":
            full[
                "dual"
            ][
                "pointwise_upper_bound_m_s2_per_j"
            ],

        "r2b_76d_weighted_upper_bound_m_s2_per_j":
            full[
                "dual"
            ][
                "weighted_dual_upper_bound_m_s2_per_j"
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


def prior_bottleneck_point() -> np.ndarray:
    result = (
        r2b_artifact()
    )

    dual = (
        result[
            "nested_analyses"
        ][
            "76"
        ][
            "dual"
        ]
    )

    return np.asarray(
        [
            dual[
                "bottleneck_payload_z_m"
            ],
            dual[
                "bottleneck_payload_rho_m"
            ],
        ],
        dtype=float,
    )


def certificate_payload_points() -> np.ndarray:
    all_points = (
        optimization_payload_points()
    )

    sampled = (
        all_points[
            ::4
        ].copy()
    )

    bottleneck = (
        prior_bottleneck_point()
    )

    distances = np.linalg.norm(
        sampled
        -
        bottleneck[
            None,
            :
        ],
        axis=1,
    )

    if float(
        np.min(
            distances
        )
    ) > 1.0e-12:
        sampled = np.vstack(
            [
                sampled,
                bottleneck,
            ]
        )

    return sampled


def source_support_unknown_indices(
    rhos: np.ndarray,
    zs: np.ndarray,
) -> np.ndarray:
    rho_i, z_i = np.meshgrid(
        rhos[
            1:-1
        ],
        zs[
            1:-1
        ],
    )

    support = (
        rho_i**2
        +
        z_i**2
        <
        SOURCE_RADIUS_M**2
    )

    return np.flatnonzero(
        support.ravel()
    )


def acceleration_bilinear_matrix(
    portal_scale_ev: float = PORTAL_SCALE_EV,
) -> np.ndarray:
    alpha = (
        -C_LIGHT_M_S**2
        *
        HBAR_C_EV_M**2
        /
        float(
            portal_scale_ev
        ) ** 4
    )

    matrix = np.zeros(
        (
            4,
            4,
        ),
        dtype=float,
    )

    matrix[
        0,
        2
    ] = alpha

    matrix[
        2,
        0
    ] = alpha

    matrix[
        1,
        3
    ] = alpha

    matrix[
        3,
        1
    ] = alpha

    return matrix


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


def classify_capacity_targets(
    upper_bound_m_s2_per_j: float,
) -> dict[str, Any]:
    result = {}

    for capacity_j in CAPACITY_TARGETS_J:
        required = (
            target_efficiency_m_s2_per_j(
                capacity_j
            )
        )

        result[
            str(
                capacity_j
            )
        ] = {
            "capacity_target_j":
                capacity_j,

            "required_efficiency_m_s2_per_j":
                required,

            "ruled_out_by_pointwise_upper_bound":
                bool(
                    upper_bound_m_s2_per_j
                    <
                    required
                ),

            "mathematically_allowed_by_pointwise_upper_bound":
                bool(
                    upper_bound_m_s2_per_j
                    >=
                    required
                ),
        }

    return result


def _batch_local_observables(
    solutions: np.ndarray,
    rhos: np.ndarray,
    zs: np.ndarray,
    points: np.ndarray,
    h: float,
) -> np.ndarray:
    batch_size = (
        solutions.shape[
            1
        ]
    )

    fields = np.zeros(
        (
            batch_size,
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
        solutions.T.reshape(
            (
                batch_size,
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

    sampled_b_rho = (
        _bilinear_sample_basis(
            b_rho,
            rhos,
            zs,
            points,
            h,
        )
    )

    sampled_b_z = (
        _bilinear_sample_basis(
            b_z,
            rhos,
            zs,
            points,
            h,
        )
    )

    sampled_d_b_rho_dz = (
        _bilinear_sample_basis(
            d_b_rho_dz,
            rhos,
            zs,
            points,
            h,
        )
    )

    sampled_d_b_z_dz = (
        _bilinear_sample_basis(
            d_b_z_dz,
            rhos,
            zs,
            points,
            h,
        )
    )

    return np.stack(
        [
            sampled_b_rho,
            sampled_b_z,
            sampled_d_b_rho_dz,
            sampled_d_b_z_dz,
        ],
        axis=1,
    )


def _point_generalized_upper_bound(
    observable_matrix: np.ndarray,
    h_cholesky: Any,
    acceleration_matrix: np.ndarray,
) -> float:
    solved = (
        cho_solve(
            h_cholesky,
            observable_matrix.T,
            check_finite=False,
        )
    )

    gram = (
        observable_matrix
        @
        solved
    )

    gram = (
        0.5
        *
        (
            gram
            +
            gram.T
        )
    )

    gram_eigenvalues, gram_eigenvectors = np.linalg.eigh(
        gram
    )

    gram_eigenvalues = np.maximum(
        gram_eigenvalues,
        0.0,
    )

    sqrt_gram = (
        gram_eigenvectors
        @
        np.diag(
            np.sqrt(
                gram_eigenvalues
            )
        )
        @
        gram_eigenvectors.T
    )

    reduced = (
        sqrt_gram
        @
        acceleration_matrix
        @
        sqrt_gram
    )

    reduced = (
        0.5
        *
        (
            reduced
            +
            reduced.T
        )
    )

    eigenvalues = np.linalg.eigvalsh(
        reduced
    )

    return float(
        eigenvalues[
            -1
        ]
    )


def grid_complete_pointwise_certificate(
    h: float,
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
            PORTAL_SCALE_EV,
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

    zero_source = np.zeros_like(
        rho_i
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

    source_unknown_indices = (
        source_support_unknown_indices(
            rhos,
            zs,
        )
    )

    source_count = len(
        source_unknown_indices
    )

    payload_points = (
        certificate_payload_points()
    )

    payload_point_count = len(
        payload_points
    )

    source_green = np.empty(
        (
            source_count,
            source_count,
        ),
        dtype=float,
    )

    observables = np.empty(
        (
            payload_point_count,
            4,
            source_count,
        ),
        dtype=float,
    )

    operator_size = (
        operator.shape[
            0
        ]
    )

    for start in range(
        0,
        source_count,
        SOURCE_SOLVE_BATCH_SIZE,
    ):
        stop = min(
            start
            +
            SOURCE_SOLVE_BATCH_SIZE,
            source_count,
        )

        batch_source_indices = (
            source_unknown_indices[
                start:stop
            ]
        )

        batch_size = len(
            batch_source_indices
        )

        rhs = np.zeros(
            (
                operator_size,
                batch_size,
            ),
            dtype=float,
        )

        rhs[
            batch_source_indices,
            np.arange(
                batch_size
            ),
        ] = 1.0

        solutions = (
            factorization.solve(
                rhs
            )
        )

        source_green[
            :,
            start:stop,
        ] = solutions[
            source_unknown_indices,
            :
        ]

        observables[
            :,
            :,
            start:stop,
        ] = (
            _batch_local_observables(
                solutions,
                rhos,
                zs,
                payload_points,
                h,
            )
        )

    source_green = (
        0.5
        *
        (
            source_green
            +
            source_green.T
        )
    )

    energy_prefactor = (
        math.pi
        *
        EV_J
        /
        HBAR_C_EV_M
    )

    energy_matrix = (
        energy_prefactor
        *
        source_green
    )

    energy_eigenvalues = np.linalg.eigvalsh(
        energy_matrix
    )

    minimum_energy_eigenvalue = float(
        energy_eigenvalues[
            0
        ]
    )

    maximum_energy_eigenvalue = float(
        energy_eigenvalues[
            -1
        ]
    )

    energy_positive_definite = bool(
        minimum_energy_eigenvalue
        >
        0.0
    )

    if not energy_positive_definite:
        return {
            "grid_spacing_m":
                h,

            "certificate_valid":
                False,

            "reason":
                "GRID_COMPLETE_SOURCE_ENERGY_MATRIX_NOT_POSITIVE_DEFINITE",

            "source_dof_count":
                source_count,

            "payload_certificate_point_count":
                payload_point_count,

            "minimum_energy_eigenvalue":
                minimum_energy_eigenvalue,

            "maximum_energy_eigenvalue":
                maximum_energy_eigenvalue,
        }

    energy_condition_number = (
        maximum_energy_eigenvalue
        /
        minimum_energy_eigenvalue
    )

    if (
        not math.isfinite(
            energy_condition_number
        )
        or
        energy_condition_number
        >
        ENERGY_CONDITION_LIMIT
    ):
        return {
            "grid_spacing_m":
                h,

            "certificate_valid":
                False,

            "reason":
                "GRID_COMPLETE_SOURCE_ENERGY_MATRIX_TOO_ILL_CONDITIONED",

            "source_dof_count":
                source_count,

            "payload_certificate_point_count":
                payload_point_count,

            "minimum_energy_eigenvalue":
                minimum_energy_eigenvalue,

            "maximum_energy_eigenvalue":
                maximum_energy_eigenvalue,

            "energy_condition_number":
                energy_condition_number,
        }

    h_cholesky = cho_factor(
        energy_matrix,
        lower=True,
        check_finite=False,
    )

    acceleration_matrix = (
        acceleration_bilinear_matrix(
            PORTAL_SCALE_EV
        )
    )

    local_upper_bounds = np.empty(
        payload_point_count,
        dtype=float,
    )

    for point_index in range(
        payload_point_count
    ):
        local_upper_bounds[
            point_index
        ] = (
            _point_generalized_upper_bound(
                observables[
                    point_index
                ],
                h_cholesky,
                acceleration_matrix,
            )
        )

    bottleneck_index = int(
        np.argmin(
            local_upper_bounds
        )
    )

    whole_payload_upper_bound = float(
        local_upper_bounds[
            bottleneck_index
        ]
    )

    bottleneck_point = (
        payload_points[
            bottleneck_index
        ]
    )

    prior_bottleneck = (
        prior_bottleneck_point()
    )

    prior_distance = np.linalg.norm(
        payload_points
        -
        prior_bottleneck[
            None,
            :
        ],
        axis=1,
    )

    prior_index = int(
        np.argmin(
            prior_distance
        )
    )

    prior_bottleneck_upper_bound = float(
        local_upper_bounds[
            prior_index
        ]
    )

    if whole_payload_upper_bound > 0.0:
        certified_capacity_floor_j = (
            TARGET_ACCELERATION_M_S2
            /
            whole_payload_upper_bound
        )
    else:
        certified_capacity_floor_j = math.inf

    targets = (
        classify_capacity_targets(
            whole_payload_upper_bound
        )
    )

    r2b = (
        r2b_artifact()
    )

    r2b_76d_pointwise = float(
        r2b[
            "nested_analyses"
        ][
            "76"
        ][
            "dual"
        ][
            "pointwise_upper_bound_m_s2_per_j"
        ]
    )

    return {
        "grid_spacing_m":
            h,

        "certificate_valid":
            True,

        "operator_unknown_count":
            operator_size,

        "source_dof_count":
            source_count,

        "payload_certificate_point_count":
            payload_point_count,

        "source_space_is_every_grid_cell_in_original_2m_support":
            True,

        "source_space_is_optimistic_superset_of_smooth_currents_on_grid":
            True,

        "minimum_energy_eigenvalue":
            minimum_energy_eigenvalue,

        "maximum_energy_eigenvalue":
            maximum_energy_eigenvalue,

        "energy_condition_number":
            energy_condition_number,

        "z_max":
            float(
                np.max(
                    z_coefficient
                )
            ),

        "whole_payload_pointwise_upper_bound_m_s2_per_j":
            whole_payload_upper_bound,

        "certified_loaded_capacity_floor_j":
            certified_capacity_floor_j,

        "bottleneck_payload_point_index":
            bottleneck_index,

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

        "prior_r2b_bottleneck_local_upper_bound_m_s2_per_j":
            prior_bottleneck_upper_bound,

        "prior_r2b_bottleneck_z_m":
            float(
                prior_bottleneck[
                    0
                ]
            ),

        "prior_r2b_bottleneck_rho_m":
            float(
                prior_bottleneck[
                    1
                ]
            ),

        "r2b_76d_pointwise_upper_bound_m_s2_per_j":
            r2b_76d_pointwise,

        "grid_complete_upper_bound_over_r2b_76d_bound":
            (
                whole_payload_upper_bound
                /
                r2b_76d_pointwise
            ),

        "capacity_targets":
            targets,

        "continuous_source_space_exhausted":
            False,

        "nonaxisymmetric_source_space_exhausted":
            False,

        "complete_energy_established":
            False,
    }


def claim_policy_gate() -> dict[str, Any]:
    return {
        "few_joule_branch_priority":
            True,

        "exact_1kev_primary":
            True,

        "every_axisymmetric_source_grid_cell_free":
            True,

        "grid_source_space_smoother_than_physical_requirement":
            False,

        "grid_source_space_more_permissive_than_smooth_physical_current":
            True,

        "local_current_conservation_preserved":
            True,

        "continuous_source_space_exhausted":
            False,

        "nonaxisymmetric_source_space_exhausted":
            False,

        "all_possible_source_shapes_closed":
            False,

        "carrier_modified":
            False,

        "metric_modified":
            False,

        "portal_modified":
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
