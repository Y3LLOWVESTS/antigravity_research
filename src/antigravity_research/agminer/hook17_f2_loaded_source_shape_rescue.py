"""032H17A12D1R2 — loading-aware source-shape rescue of the A12C few-joule branch.

PURPOSE
-------
A12C established the exceptional unloaded reference

    M_X = 1 keV
    E_field = 2.6568591420597114 J
    1 kg neutral payload
    1 m external stand-off
    >= 1 g throughout the sampled payload.

A12D1R1 then solved the finite-payload same-action loaded operator.

Its central result was not an enormous matter-energy cost.

Instead:

    exact 1-keV original source morphology:
        loses the whole-payload outward sign;

    best simple-source loaded survivor:
        M_X ~ 19 keV
        canonical field ~ 672 kJ
        payload interaction ~ 14.7 J.

Therefore the immediate rescue problem is field topology / source impedance
matching, not payload interaction energy.

At fixed payload density and fixed portal scale, the leading loaded equation

    curl[ Z(x) B ] = J

with

    Z(x) = 1 + 2 rho_E(x) / M_X^4

is linear in J.

For an axisymmetric azimuthal source basis

    J_phi = sum_a c_a J_phi^(a),

the solved vector potential and magnetic field are linear in c.

The physical metric response is quadratic:

    sigma ~ B^2 / M_X^4,

so every sampled payload acceleration has the exact finite-dimensional form

    a_k(c) = c^T Q_k c.

The loaded quadratic capacity similarly has

    E_loaded(c) = c^T H c.

Thus source-shape rescue can be attacked directly as the homogeneous maximin
problem

    maximize_c
        min_k a_k(c) / E_loaded(c).

This is not a blind geometry scan.

It is a deterministic response-basis reduction of the actual loaded PDE.

SOURCE BASIS
------------
Every source basis member is:

- compact inside the original A12C radius R_s = 2 m;
- axisymmetric;
- purely azimuthal;
- therefore divergence-free identically;
- multiplied by the original smooth A12C boundary envelope.

Basis member zero is EXACTLY the original A12C current shape.

The remaining members are smooth localized current patches distributed
through the source support.

Two lanes are tested.

SAME-SIGN LANE
    All coefficients are nonnegative.
    Every local current therefore circulates in the same direction.

SIGNED / MULTIPOLAR LANE
    Coefficients may have either sign.
    Counter-circulating source regions are allowed.
    Their absolute source inventory and negative-current fraction are reported
    explicitly.

NO NEAR-NULL NUMERICAL GAIN
---------------------------
The loaded response-energy matrix H is diagonalized.

Directions below a fixed relative eigenvalue floor are discarded before the
signed optimizer is allowed to act.

Therefore a rescue cannot be manufactured by exploiting a numerically
near-null source-response direction.

PORTAL LADDER
-------------
The primary target remains EXACTLY 1 keV.

A tightly focused ladder is also examined:

    0.5
    0.75
    1.0
    1.25
    1.5
    2
    3
    5
    8
    12 keV.

This is authorized because payload loading introduced genuinely new physics.

Examples of the original unloaded M^4 scaling are:

    1 keV  ->  2.66 J
    2 keV  -> ~42.5 J
    3 keV  -> ~215 J
    5 keV  -> ~1.66 kJ.

Thus a nearby loaded descendant could preserve the extraordinary low-capacity
character even if the exact 1-keV point is not recoverable.

OPTIMIZATION POLICY
-------------------
The broad portal ladder is searched on a coarse grid.

The most promising scales, plus 1 keV unconditionally, are rebuilt at higher
resolution with stronger deterministic/random-restart maximin optimization.

Candidates are then re-solved directly from their physical source
coefficients at finer grids.

The quadratic-form prediction is never accepted by itself.

CLAIM LIMITS
------------
This branch adds no new carrier, metric, hidden matter, or exotic matter.

It does not establish:

- a microscopic source completion;
- source rest/polarization/support energy;
- UV completion;
- radiative stability;
- empirical consistency;
- fully source-loaded same-action matter;
- complete operating energy;
- replacement of 006D;
- a device.

A positive result means only:

    a physically interpretable compact conserved source morphology exists
    that preserves the low-capacity loaded A12 field mechanism at the tested
    portal scale.

CLAIM CLASSIFICATION
--------------------
PROJECT_LOADED_SOURCE_SHAPE_RESCUE_PREFLIGHT
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from scipy.interpolate import RegularGridInterpolator
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
    ROBUSTNESS_DENSITY_MODEL,
    _assemble_weighted_operator,
    _edge_energy_integral,
    _grid,
    _payload_sample_points,
    a12c_artifact,
    geometric_standoff_m,
    loading_coefficient_z,
    payload_density_profile_kg_m3,
    provenance_gate as r1_provenance_gate,
)


BRANCH = "032H17A12D1R2"

SOURCE_BASIS_WIDTH = 0.23

SOURCE_PATCH_CENTERS = (
    (0.25, -0.65),
    (0.55, -0.65),

    (0.25, -0.25),
    (0.55, -0.25),
    (0.80, -0.25),

    (0.25, 0.15),
    (0.55, 0.15),
    (0.80, 0.15),

    (0.25, 0.55),
    (0.55, 0.55),
    (0.75, 0.55),

    (0.25, 0.78),
    (0.88, 0.00),
    (0.60, 0.00),
)

SOURCE_BASIS_COUNT = (
    1
    +
    len(
        SOURCE_PATCH_CENTERS
    )
)

PORTAL_LADDER_EV = (
    500.0,
    750.0,
    1000.0,
    1250.0,
    1500.0,
    2000.0,
    3000.0,
    5000.0,
    8000.0,
    12000.0,
)

BROAD_RESPONSE_GRID_M = 0.125
REFINED_RESPONSE_GRID_M = 0.100

VALIDATION_GRID_M = (
    0.100,
    0.075,
    0.050,
)

PRODUCTION_RHO_MAX_M = 12.0
PRODUCTION_Z_MIN_M = -10.0
PRODUCTION_Z_MAX_M = 13.0

LARGER_RHO_MAX_M = 14.0
LARGER_Z_MIN_M = -12.0
LARGER_Z_MAX_M = 15.0

ENERGY_EIGEN_RELATIVE_FLOOR = 1.0e-8

BROAD_SIGNED_RANDOM_SEEDS = 500
REFINED_SIGNED_RANDOM_SEEDS = 1800
EXACT_1KEV_SIGNED_RANDOM_SEEDS = 4000

BROAD_NONNEGATIVE_RANDOM_SEEDS = 400
REFINED_NONNEGATIVE_RANDOM_SEEDS = 1200
EXACT_1KEV_NONNEGATIVE_RANDOM_SEEDS = 2500

BROAD_RESTARTS = 4
REFINED_RESTARTS = 7
EXACT_1KEV_RESTARTS = 12

ACTIVE_INITIAL_COUNT = 64
ACTIVE_ADD_COUNT = 32
ACTIVE_MAX_LOOPS = 5

GRID_CAPACITY_RELERR_PREFLIGHT_MAX = 0.25
DOMAIN_CAPACITY_RELERR_PREFLIGHT_MAX = 0.12

FEW_JOULE_TARGET_J = 10.0
SUB100J_TARGET_J = 100.0
SUB1KJ_TARGET_J = 1000.0
SUB10KJ_TARGET_J = 10000.0
SUB100KJ_TARGET_J = 100000.0
SUB1MJ_TARGET_J = 1.0e6


def _repo_root() -> Path:
    """Return repository root."""

    return (
        Path(__file__)
        .resolve()
        .parents[3]
    )


@lru_cache(maxsize=1)
def r1_artifact() -> dict[str, Any]:
    """Load completed A12D1R1 result."""

    path = (
        _repo_root()
        /
        "results"
        /
        "data"
        /
        "032h17a12d1r1_hook17_f2_strong_payload_loading_rescue_summary.json"
    )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def source_basis_labels() -> tuple[str, ...]:
    """Return deterministic physical source-basis labels."""

    labels = [
        "A12C_ORIGINAL",
    ]

    for index, (
        rho_center,
        z_center,
    ) in enumerate(
        SOURCE_PATCH_CENTERS
    ):
        labels.append(
            (
                f"PATCH_{index:02d}_"
                f"RHO_{rho_center:.2f}_"
                f"Z_{z_center:+.2f}"
            )
        )

    return tuple(
        labels
    )


def original_a12c_source_profile(
    rho: np.ndarray,
    z: np.ndarray,
) -> np.ndarray:
    """Return exact original A12C source shape."""

    radius_squared = (
        rho**2
        +
        z**2
    )

    inside = (
        radius_squared
        <
        SOURCE_RADIUS_M**2
    )

    profile = np.zeros_like(
        rho,
        dtype=float,
    )

    x = (
        radius_squared[
            inside
        ]
        /
        SOURCE_RADIUS_M**2
    )

    profile[
        inside
    ] = (
        (
            rho[
                inside
            ]
            /
            SOURCE_RADIUS_M
        )
        *
        (
            1.0
            -
            x
        ) ** 2
    )

    return profile


def source_basis_profiles(
    rho: np.ndarray,
    z: np.ndarray,
) -> np.ndarray:
    """Return original source plus positive localized compact patches."""

    base = (
        original_a12c_source_profile(
            rho,
            z,
        )
    )

    profiles = [
        base,
    ]

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

    for (
        rho_center,
        z_center,
    ) in SOURCE_PATCH_CENTERS:
        gaussian = np.exp(
            -(
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
            /
            (
                2.0
                *
                SOURCE_BASIS_WIDTH**2
            )
        )

        profiles.append(
            base
            *
            gaussian
        )

    return np.asarray(
        profiles,
        dtype=float,
    )


def source_basis_gate() -> dict[str, Any]:
    """Record compactness, conservation, and basis provenance."""

    labels = (
        source_basis_labels()
    )

    return {
        "basis_count":
            SOURCE_BASIS_COUNT,

        "labels":
            list(
                labels
            ),

        "basis_zero_exactly_original_a12c":
            True,

        "all_basis_members_axisymmetric":
            True,

        "all_basis_members_pure_azimuthal":
            True,

        "divergence_zero_by_axisymmetry":
            True,

        "all_basis_members_compact_inside_original_source_radius":
            True,

        "all_basis_members_share_original_boundary_envelope":
            True,

        "same_sign_lane_available":
            True,

        "signed_multipolar_lane_available":
            True,

        "source_radius_m":
            SOURCE_RADIUS_M,

        "geometry_modified":
            False,
    }


def provenance_gate() -> dict[str, Any]:
    """Require completed R1 and preserve its scoped interpretation."""

    upstream = (
        r1_provenance_gate()
    )

    r1 = (
        r1_artifact()
    )

    passed = bool(
        upstream[
            "pass"
        ]

        and

        r1[
            "branch"
        ]
        ==
        "032H17A12D1R1"

        and

        r1[
            "one_kev_resolution_audit"
        ][
            "whole_payload_sign_fail_at_all_tested_grids"
        ]
        is True

        and

        r1[
            "a12b_exact_massless_carrier_closed"
        ]
        is False

        and

        r1[
            "a12c_f2_metric_mechanism_closed"
        ]
        is False

        and

        r1[
            "physical_antigravity_model_found"
        ]
        is False
    )

    return {
        "pass":
            passed,

        "r1_branch":
            r1[
                "branch"
            ],

        "r1_exact_1kev_original_shape_failed_loaded_sign":
            r1[
                "one_kev_resolution_audit"
            ][
                "whole_payload_sign_fail_at_all_tested_grids"
            ],

        "r1_strongly_loaded_sub1mj_survivor":
            r1[
                "strongly_loaded_whole_payload_sub1mj_capacity_survivor"
            ],

        "a12b_carrier_preserved":
            not r1[
                "a12b_exact_massless_carrier_closed"
            ],

        "a12c_f2_mechanism_preserved":
            not r1[
                "a12c_f2_metric_mechanism_closed"
            ],
    }


def claim_policy_gate() -> dict[str, Any]:
    """Return strict R2 claim policy."""

    return {
        "primary_target_is_exact_1kev_rescue":
            True,

        "few_joule_branch_given_special_priority":
            True,

        "carrier_modified":
            False,

        "metric_function_modified":
            False,

        "payload_geometry_modified":
            False,

        "source_support_radius_modified":
            False,

        "source_morphology_allowed_to_change":
            True,

        "source_current_conservation_preserved":
            True,

        "near_null_response_gain_allowed":
            False,

        "microscopic_source_completed":
            False,

        "source_support_energy_completed":
            False,

        "uv_completed":
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


def optimization_payload_points() -> np.ndarray:
    """Return fixed dense cross-section sample for the maximin optimizer."""

    points = [
        [
            float(
                _payload_sample_points()[
                    0,
                    0
                ]
            ),
            float(
                _payload_sample_points()[
                    0,
                    1
                ]
            ),
        ]
    ]

    from .hook17_f2_strong_payload_loading_rescue import (
        PAYLOAD_MAJOR_RADIUS_M,
        PAYLOAD_MINOR_RADIUS_M,
        payload_center_z_m,
    )

    radial_fractions = np.linspace(
        0.10,
        0.995,
        13,
    )

    angles = np.linspace(
        0.0,
        2.0
        *
        math.pi,
        48,
        endpoint=False,
    )

    for fraction in radial_fractions:
        radius = (
            PAYLOAD_MINOR_RADIUS_M
            *
            fraction
        )

        for angle in angles:
            rho = (
                PAYLOAD_MAJOR_RADIUS_M
                +
                radius
                *
                math.cos(
                    angle
                )
            )

            z = (
                payload_center_z_m()
                +
                radius
                *
                math.sin(
                    angle
                )
            )

            points.append(
                [
                    z,
                    rho,
                ]
            )

    return np.asarray(
        points,
        dtype=float,
    )


def _interpolate_basis_fields(
    arrays: np.ndarray,
    rhos: np.ndarray,
    zs: np.ndarray,
    points: np.ndarray,
) -> np.ndarray:
    """Interpolate every basis field array to common points."""

    values = []

    for array in arrays:
        interpolator = RegularGridInterpolator(
            (
                zs,
                rhos,
            ),
            array,
            bounds_error=True,
        )

        values.append(
            interpolator(
                points
            )
        )

    return np.asarray(
        values,
        dtype=float,
    ).T


def build_response_problem(
    portal_scale_ev: float,
    h: float,
    density_model: str = PRIMARY_DENSITY_MODEL,
    rho_max_m: float = PRODUCTION_RHO_MAX_M,
    z_min_m: float = PRODUCTION_Z_MIN_M,
    z_max_m: float = PRODUCTION_Z_MAX_M,
) -> dict[str, Any]:
    """Build finite-dimensional loaded source-response problem."""

    (
        rhos,
        zs,
        rho_grid,
        z_grid,
    ) = (
        _grid(
            h,
            rho_max_m,
            z_min_m,
            z_max_m,
        )
    )

    density = (
        payload_density_profile_kg_m3(
            rho_grid,
            z_grid,
            density_model,
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

    source_basis = (
        source_basis_profiles(
            rho_i,
            z_i,
        )
    )

    zero_source = np.zeros_like(
        source_basis[
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
        (
            h**2
        )
        *
        rho_i[
            None,
            :,
            :
        ]
        *
        source_basis
    ).reshape(
        (
            SOURCE_BASIS_COUNT,
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
            SOURCE_BASIS_COUNT,
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
                SOURCE_BASIS_COUNT,
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
        _interpolate_basis_fields(
            b_rho,
            rhos,
            zs,
            points,
        )
    )

    bz = (
        _interpolate_basis_fields(
            b_z,
            rhos,
            zs,
            points,
        )
    )

    dbr = (
        _interpolate_basis_fields(
            d_b_rho_dz,
            rhos,
            zs,
            points,
        )
    )

    dbz = (
        _interpolate_basis_fields(
            d_b_z_dz,
            rhos,
            zs,
            points,
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
        ]
    )

    source_work_prefactor = (
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
        source_work_prefactor
        *
        np.einsum(
            "aij,bij,ij->ab",
            source_basis,
            field_interior,
            rho_i,
            optimize=True,
        )
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

    energy_eigenvalues = np.linalg.eigvalsh(
        energy_matrix
    )

    positive_max = float(
        np.max(
            energy_eigenvalues
        )
    )

    retained_mask = (
        energy_eigenvalues
        >
        positive_max
        *
        ENERGY_EIGEN_RELATIVE_FLOOR
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

        "density_model":
            density_model,

        "source_basis_labels":
            source_basis_labels(),

        "energy_matrix":
            energy_matrix,

        "q_matrices":
            q_matrices,

        "energy_eigenvalues":
            energy_eigenvalues,

        "retained_energy_rank":
            int(
                np.count_nonzero(
                    retained_mask
                )
            ),

        "discarded_near_null_dimension":
            int(
                SOURCE_BASIS_COUNT
                -
                np.count_nonzero(
                    retained_mask
                )
            ),

        "energy_condition_number_retained":
            float(
                positive_max
                /
                np.min(
                    energy_eigenvalues[
                        retained_mask
                    ]
                )
            ),

        "z_max":
            float(
                np.max(
                    z_coefficient
                )
            ),

        "optimization_payload_point_count":
            int(
                len(
                    points
                )
            ),
    }


def _q_values(
    q_matrices: np.ndarray,
    coefficients: np.ndarray,
) -> np.ndarray:
    """Evaluate all quadratic acceleration forms."""

    return np.einsum(
        "i,kij,j->k",
        coefficients,
        q_matrices,
        coefficients,
        optimize=True,
    )


def _energy(
    energy_matrix: np.ndarray,
    coefficients: np.ndarray,
) -> float:
    """Evaluate loaded quadratic source-response energy."""

    return float(
        coefficients
        @
        energy_matrix
        @
        coefficients
    )


def _normalize_coefficients(
    coefficients: np.ndarray,
) -> np.ndarray:
    """Remove irrelevant homogeneous amplitude."""

    coefficients = np.asarray(
        coefficients,
        dtype=float,
    )

    maximum = float(
        np.max(
            np.abs(
                coefficients
            )
        )
    )

    if maximum <= 0.0:
        return coefficients.copy()

    return (
        coefficients
        /
        maximum
    )


def _capacity_from_margin(
    margin_m_s2_per_j: float,
) -> float | None:
    """Return capacity required for 1 g from acceleration-per-joule margin."""

    if (
        not math.isfinite(
            margin_m_s2_per_j
        )
        or
        margin_m_s2_per_j
        <=
        0.0
    ):
        return None

    return (
        TARGET_ACCELERATION_M_S2
        /
        margin_m_s2_per_j
    )


def _random_signed_seeds(
    q_whitened: np.ndarray,
    count: int,
    seed: int,
) -> list[np.ndarray]:
    """Return deterministic high-margin unit-sphere seeds."""

    rng = np.random.default_rng(
        seed
    )

    dimension = (
        q_whitened.shape[
            1
        ]
    )

    random_vectors = rng.normal(
        size=(
            count,
            dimension,
        )
    )

    norms = np.linalg.norm(
        random_vectors,
        axis=1,
    )

    random_vectors = (
        random_vectors
        /
        norms[
            :,
            None,
        ]
    )

    search_q = (
        q_whitened[
            ::3
        ]
    )

    best = []

    chunk_size = 100

    for start in range(
        0,
        count,
        chunk_size,
    ):
        vectors = random_vectors[
            start
            :
            start
            +
            chunk_size
        ]

        values = np.einsum(
            "bi,kij,bj->bk",
            vectors,
            search_q,
            vectors,
            optimize=True,
        )

        minima = np.min(
            values,
            axis=1,
        )

        for local_index, minimum in enumerate(
            minima
        ):
            best.append(
                (
                    float(
                        minimum
                    ),
                    vectors[
                        local_index
                    ].copy(),
                )
            )

    best.sort(
        key=lambda item:
            item[
                0
            ],
        reverse=True,
    )

    return [
        item[
            1
        ]
        for item in best[
            :12
        ]
    ]


def _signed_active_refinement(
    q_whitened: np.ndarray,
    seed: np.ndarray,
) -> dict[str, Any]:
    """Maximize worst-point response on unit-energy sphere."""

    y = np.asarray(
        seed,
        dtype=float,
    )

    norm = float(
        np.linalg.norm(
            y
        )
    )

    if norm == 0.0:
        y = np.zeros_like(
            y
        )

        y[
            0
        ] = 1.0
    else:
        y = (
            y
            /
            norm
        )

    values = (
        _q_values(
            q_whitened,
            y,
        )
    )

    active = list(
        np.argsort(
            values
        )[
            :ACTIVE_INITIAL_COUNT
        ]
    )

    success = False
    message = "NOT_RUN"

    for _ in range(
        ACTIVE_MAX_LOOPS
    ):
        active_array = np.asarray(
            sorted(
                set(
                    active
                )
            ),
            dtype=int,
        )

        q_active = (
            q_whitened[
                active_array
            ]
        )

        values = (
            _q_values(
                q_active,
                y,
            )
        )

        t0 = float(
            np.min(
                values
            )
        )

        x0 = np.concatenate(
            [
                y,
                np.asarray(
                    [
                        t0,
                    ]
                ),
            ]
        )

        dimension = len(
            y
        )

        def objective(
            x: np.ndarray,
        ) -> float:
            return (
                -float(
                    x[
                        -1
                    ]
                )
            )

        def objective_jac(
            x: np.ndarray,
        ) -> np.ndarray:
            gradient = np.zeros_like(
                x
            )

            gradient[
                -1
            ] = -1.0

            return gradient

        def equality(
            x: np.ndarray,
        ) -> float:
            return (
                float(
                    x[
                        :dimension
                    ]
                    @
                    x[
                        :dimension
                    ]
                )
                -
                1.0
            )

        def equality_jac(
            x: np.ndarray,
        ) -> np.ndarray:
            gradient = np.zeros_like(
                x
            )

            gradient[
                :dimension
            ] = (
                2.0
                *
                x[
                    :dimension
                ]
            )

            return gradient

        def inequalities(
            x: np.ndarray,
        ) -> np.ndarray:
            yy = (
                x[
                    :dimension
                ]
            )

            tt = float(
                x[
                    -1
                ]
            )

            return (
                _q_values(
                    q_active,
                    yy,
                )
                -
                tt
            )

        def inequalities_jac(
            x: np.ndarray,
        ) -> np.ndarray:
            yy = (
                x[
                    :dimension
                ]
            )

            gradient_y = (
                2.0
                *
                np.einsum(
                    "kij,j->ki",
                    q_active,
                    yy,
                    optimize=True,
                )
            )

            gradient_t = (
                -np.ones(
                    (
                        len(
                            q_active
                        ),
                        1,
                    )
                )
            )

            return np.concatenate(
                [
                    gradient_y,
                    gradient_t,
                ],
                axis=1,
            )

        result = minimize(
            objective,
            x0,
            method="SLSQP",
            jac=objective_jac,
            constraints=(
                {
                    "type":
                        "eq",

                    "fun":
                        equality,

                    "jac":
                        equality_jac,
                },
                {
                    "type":
                        "ineq",

                    "fun":
                        inequalities,

                    "jac":
                        inequalities_jac,
                },
            ),
            options={
                "maxiter":
                    500,

                "ftol":
                    1.0e-12,

                "disp":
                    False,
            },
        )

        candidate = (
            result.x[
                :dimension
            ]
        )

        candidate_norm = float(
            np.linalg.norm(
                candidate
            )
        )

        if candidate_norm > 0.0:
            y = (
                candidate
                /
                candidate_norm
            )

        success = bool(
            result.success
        )

        message = str(
            result.message
        )

        full_values = (
            _q_values(
                q_whitened,
                y,
            )
        )

        worst = np.argsort(
            full_values
        )[
            :ACTIVE_ADD_COUNT
        ]

        new_active = set(
            active
        )

        new_active.update(
            int(
                index
            )
            for index in worst
        )

        if len(
            new_active
        ) == len(
            set(
                active
            )
        ):
            break

        active = list(
            new_active
        )

    final_values = (
        _q_values(
            q_whitened,
            y,
        )
    )

    return {
        "y":
            y,

        "minimum_margin":
            float(
                np.min(
                    final_values
                )
            ),

        "maximum_margin":
            float(
                np.max(
                    final_values
                )
            ),

        "active_constraint_count":
            len(
                set(
                    active
                )
            ),

        "optimizer_success":
            success,

        "optimizer_message":
            message,
    }


def optimize_signed_lane(
    response: dict[str, Any],
    random_seed_count: int,
    restart_count: int,
    deterministic_seed: int,
) -> dict[str, Any]:
    """Optimize signed/counter-circulating source lane."""

    h_matrix = np.asarray(
        response[
            "energy_matrix"
        ],
        dtype=float,
    )

    q_matrices = np.asarray(
        response[
            "q_matrices"
        ],
        dtype=float,
    )

    eigenvalues, eigenvectors = np.linalg.eigh(
        h_matrix
    )

    maximum = float(
        np.max(
            eigenvalues
        )
    )

    keep = (
        eigenvalues
        >
        maximum
        *
        ENERGY_EIGEN_RELATIVE_FLOOR
    )

    retained_values = (
        eigenvalues[
            keep
        ]
    )

    retained_vectors = (
        eigenvectors[
            :,
            keep
        ]
    )

    transform = (
        retained_vectors
        /
        np.sqrt(
            retained_values
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

    original_c = np.zeros(
        SOURCE_BASIS_COUNT
    )

    original_c[
        0
    ] = 1.0

    original_y = (
        np.sqrt(
            retained_values
        )
        *
        (
            retained_vectors.T
            @
            original_c
        )
    )

    original_norm = float(
        np.linalg.norm(
            original_y
        )
    )

    seeds = []

    if original_norm > 0.0:
        seeds.append(
            original_y
            /
            original_norm
        )

    q_average = np.mean(
        q_whitened,
        axis=0,
    )

    q_average = (
        0.5
        *
        (
            q_average
            +
            q_average.T
        )
    )

    average_eigenvalues, average_eigenvectors = np.linalg.eigh(
        q_average
    )

    order = np.argsort(
        average_eigenvalues
    )[
        ::-1
    ]

    for index in order[
        :4
    ]:
        seeds.append(
            average_eigenvectors[
                :,
                index
            ]
        )

    seeds.extend(
        _random_signed_seeds(
            q_whitened,
            random_seed_count,
            deterministic_seed,
        )
    )

    scored_seeds = []

    for seed in seeds:
        seed = np.asarray(
            seed,
            dtype=float,
        )

        seed = (
            seed
            /
            np.linalg.norm(
                seed
            )
        )

        minimum = float(
            np.min(
                _q_values(
                    q_whitened,
                    seed,
                )
            )
        )

        scored_seeds.append(
            (
                minimum,
                seed,
            )
        )

    scored_seeds.sort(
        key=lambda item:
            item[
                0
            ],
        reverse=True,
    )

    best_result = None

    for _, seed in scored_seeds[
        :restart_count
    ]:
        result = (
            _signed_active_refinement(
                q_whitened,
                seed,
            )
        )

        if (
            best_result
            is None
            or
            result[
                "minimum_margin"
            ]
            >
            best_result[
                "minimum_margin"
            ]
        ):
            best_result = result

    assert (
        best_result
        is not None
    )

    y_best = np.asarray(
        best_result[
            "y"
        ]
    )

    physical_coefficients = (
        transform
        @
        y_best
    )

    physical_coefficients = (
        _normalize_coefficients(
            physical_coefficients
        )
    )

    margin = float(
        best_result[
            "minimum_margin"
        ]
    )

    return {
        "lane":
            "SIGNED_MULTIPOLAR",

        "minimum_acceleration_per_loaded_joule_m_s2_per_j":
            margin,

        "predicted_loaded_capacity_j":
            _capacity_from_margin(
                margin
            ),

        "source_coefficients":
            physical_coefficients.tolist(),

        "source_basis_labels":
            list(
                source_basis_labels()
            ),

        "retained_energy_rank":
            int(
                np.count_nonzero(
                    keep
                )
            ),

        "discarded_near_null_dimension":
            int(
                SOURCE_BASIS_COUNT
                -
                np.count_nonzero(
                    keep
                )
            ),

        "minimum_retained_relative_energy_eigenvalue":
            float(
                np.min(
                    retained_values
                )
                /
                maximum
            ),

        "near_null_gain_exploited":
            False,

        "active_constraint_count":
            best_result[
                "active_constraint_count"
            ],

        "optimizer_success":
            best_result[
                "optimizer_success"
            ],

        "optimizer_message":
            best_result[
                "optimizer_message"
            ],
    }


def _random_nonnegative_seeds(
    h_matrix: np.ndarray,
    q_matrices: np.ndarray,
    count: int,
    seed: int,
) -> list[np.ndarray]:
    """Return deterministic high-margin simplex seeds."""

    rng = np.random.default_rng(
        seed
    )

    candidates = rng.dirichlet(
        np.ones(
            SOURCE_BASIS_COUNT
        ),
        size=count,
    )

    search_q = (
        q_matrices[
            ::3
        ]
    )

    scores = []

    chunk_size = 100

    for start in range(
        0,
        count,
        chunk_size,
    ):
        chunk = (
            candidates[
                start
                :
                start
                +
                chunk_size
            ]
        )

        energies = np.einsum(
            "bi,ij,bj->b",
            chunk,
            h_matrix,
            chunk,
            optimize=True,
        )

        accelerations = np.einsum(
            "bi,kij,bj->bk",
            chunk,
            search_q,
            chunk,
            optimize=True,
        )

        margins = (
            np.min(
                accelerations,
                axis=1,
            )
            /
            energies
        )

        for local_index, margin in enumerate(
            margins
        ):
            scores.append(
                (
                    float(
                        margin
                    ),
                    chunk[
                        local_index
                    ].copy(),
                )
            )

    scores.sort(
        key=lambda item:
            item[
                0
            ],
        reverse=True,
    )

    return [
        item[
            1
        ]
        for item in scores[
            :12
        ]
    ]


def _nonnegative_active_refinement(
    h_matrix: np.ndarray,
    q_matrices: np.ndarray,
    seed: np.ndarray,
) -> dict[str, Any]:
    """Optimize same-current-direction simplex lane."""

    coefficients = np.maximum(
        np.asarray(
            seed,
            dtype=float,
        ),
        0.0,
    )

    coefficient_sum = float(
        np.sum(
            coefficients
        )
    )

    if coefficient_sum <= 0.0:
        coefficients = np.zeros(
            SOURCE_BASIS_COUNT
        )

        coefficients[
            0
        ] = 1.0
    else:
        coefficients = (
            coefficients
            /
            coefficient_sum
        )

    energy = (
        _energy(
            h_matrix,
            coefficients,
        )
    )

    values = (
        _q_values(
            q_matrices,
            coefficients,
        )
        /
        energy
    )

    active = list(
        np.argsort(
            values
        )[
            :ACTIVE_INITIAL_COUNT
        ]
    )

    success = False
    message = "NOT_RUN"

    for _ in range(
        ACTIVE_MAX_LOOPS
    ):
        active_array = np.asarray(
            sorted(
                set(
                    active
                )
            ),
            dtype=int,
        )

        q_active = (
            q_matrices[
                active_array
            ]
        )

        energy = (
            _energy(
                h_matrix,
                coefficients,
            )
        )

        acceleration = (
            _q_values(
                q_active,
                coefficients,
            )
        )

        t0 = float(
            np.min(
                acceleration
                /
                energy
            )
        )

        x0 = np.concatenate(
            [
                coefficients,
                np.asarray(
                    [
                        t0,
                    ]
                ),
            ]
        )

        n = (
            SOURCE_BASIS_COUNT
        )

        def objective(
            x: np.ndarray,
        ) -> float:
            return (
                -float(
                    x[
                        -1
                    ]
                )
            )

        def equality(
            x: np.ndarray,
        ) -> float:
            return (
                float(
                    np.sum(
                        x[
                            :n
                        ]
                    )
                )
                -
                1.0
            )

        def inequality(
            x: np.ndarray,
        ) -> np.ndarray:
            c = (
                x[
                    :n
                ]
            )

            t = float(
                x[
                    -1
                ]
            )

            e = (
                _energy(
                    h_matrix,
                    c,
                )
            )

            a = (
                _q_values(
                    q_active,
                    c,
                )
            )

            return (
                a
                -
                t
                *
                e
            )

        bounds = (
            [
                (
                    0.0,
                    1.0,
                )
                for _ in range(
                    n
                )
            ]
            +
            [
                (
                    None,
                    None,
                ),
            ]
        )

        result = minimize(
            objective,
            x0,
            method="SLSQP",
            constraints=(
                {
                    "type":
                        "eq",

                    "fun":
                        equality,
                },
                {
                    "type":
                        "ineq",

                    "fun":
                        inequality,
                },
            ),
            bounds=bounds,
            options={
                "maxiter":
                    500,

                "ftol":
                    1.0e-12,

                "disp":
                    False,
            },
        )

        candidate = np.maximum(
            result.x[
                :n
            ],
            0.0,
        )

        candidate_sum = float(
            np.sum(
                candidate
            )
        )

        if candidate_sum > 0.0:
            coefficients = (
                candidate
                /
                candidate_sum
            )

        success = bool(
            result.success
        )

        message = str(
            result.message
        )

        full_energy = (
            _energy(
                h_matrix,
                coefficients,
            )
        )

        full_values = (
            _q_values(
                q_matrices,
                coefficients,
            )
            /
            full_energy
        )

        worst = np.argsort(
            full_values
        )[
            :ACTIVE_ADD_COUNT
        ]

        new_active = set(
            active
        )

        new_active.update(
            int(
                index
            )
            for index in worst
        )

        if len(
            new_active
        ) == len(
            set(
                active
            )
        ):
            break

        active = list(
            new_active
        )

    final_energy = (
        _energy(
            h_matrix,
            coefficients,
        )
    )

    final_values = (
        _q_values(
            q_matrices,
            coefficients,
        )
        /
        final_energy
    )

    return {
        "coefficients":
            coefficients,

        "minimum_margin":
            float(
                np.min(
                    final_values
                )
            ),

        "active_constraint_count":
            len(
                set(
                    active
                )
            ),

        "optimizer_success":
            success,

        "optimizer_message":
            message,
    }


def optimize_nonnegative_lane(
    response: dict[str, Any],
    random_seed_count: int,
    restart_count: int,
    deterministic_seed: int,
) -> dict[str, Any]:
    """Optimize same-sign source lane."""

    h_matrix = np.asarray(
        response[
            "energy_matrix"
        ]
    )

    q_matrices = np.asarray(
        response[
            "q_matrices"
        ]
    )

    seeds = [
        np.concatenate(
            [
                np.asarray(
                    [
                        1.0,
                    ]
                ),
                np.zeros(
                    SOURCE_BASIS_COUNT
                    -
                    1
                ),
            ]
        )
    ]

    seeds.extend(
        _random_nonnegative_seeds(
            h_matrix,
            q_matrices,
            random_seed_count,
            deterministic_seed,
        )
    )

    scored = []

    for seed in seeds:
        seed = np.maximum(
            seed,
            0.0,
        )

        seed = (
            seed
            /
            np.sum(
                seed
            )
        )

        energy = (
            _energy(
                h_matrix,
                seed,
            )
        )

        margin = float(
            np.min(
                _q_values(
                    q_matrices,
                    seed,
                )
            )
            /
            energy
        )

        scored.append(
            (
                margin,
                seed,
            )
        )

    scored.sort(
        key=lambda item:
            item[
                0
            ],
        reverse=True,
    )

    best = None

    for _, seed in scored[
        :restart_count
    ]:
        result = (
            _nonnegative_active_refinement(
                h_matrix,
                q_matrices,
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

    coefficients = (
        _normalize_coefficients(
            best[
                "coefficients"
            ]
        )
    )

    margin = float(
        best[
            "minimum_margin"
        ]
    )

    return {
        "lane":
            "NONNEGATIVE_SAME_CURRENT_DIRECTION",

        "minimum_acceleration_per_loaded_joule_m_s2_per_j":
            margin,

        "predicted_loaded_capacity_j":
            _capacity_from_margin(
                margin
            ),

        "source_coefficients":
            coefficients.tolist(),

        "source_basis_labels":
            list(
                source_basis_labels()
            ),

        "source_coefficients_all_nonnegative":
            bool(
                np.all(
                    coefficients
                    >=
                    -1.0e-14
                )
            ),

        "active_constraint_count":
            best[
                "active_constraint_count"
            ],

        "optimizer_success":
            best[
                "optimizer_success"
            ],

        "optimizer_message":
            best[
                "optimizer_message"
            ],
    }


def optimize_response_problem(
    response: dict[str, Any],
    effort: str,
    deterministic_seed: int,
) -> dict[str, Any]:
    """Run both source-shape lanes."""

    if effort == "BROAD":
        signed_random = (
            BROAD_SIGNED_RANDOM_SEEDS
        )

        nonnegative_random = (
            BROAD_NONNEGATIVE_RANDOM_SEEDS
        )

        restarts = (
            BROAD_RESTARTS
        )

    elif effort == "REFINED":
        signed_random = (
            REFINED_SIGNED_RANDOM_SEEDS
        )

        nonnegative_random = (
            REFINED_NONNEGATIVE_RANDOM_SEEDS
        )

        restarts = (
            REFINED_RESTARTS
        )

    elif effort == "EXACT_1KEV":
        signed_random = (
            EXACT_1KEV_SIGNED_RANDOM_SEEDS
        )

        nonnegative_random = (
            EXACT_1KEV_NONNEGATIVE_RANDOM_SEEDS
        )

        restarts = (
            EXACT_1KEV_RESTARTS
        )

    else:
        raise ValueError(
            "unknown effort"
        )

    signed = (
        optimize_signed_lane(
            response,
            signed_random,
            restarts,
            deterministic_seed,
        )
    )

    nonnegative = (
        optimize_nonnegative_lane(
            response,
            nonnegative_random,
            restarts,
            deterministic_seed
            +
            100000,
        )
    )

    candidates = [
        signed,
        nonnegative,
    ]

    positive = [
        candidate
        for candidate in candidates
        if candidate[
            "predicted_loaded_capacity_j"
        ]
        is not None
    ]

    if positive:
        best = min(
            positive,
            key=lambda candidate:
                float(
                    candidate[
                        "predicted_loaded_capacity_j"
                    ]
                ),
        )
    else:
        best = max(
            candidates,
            key=lambda candidate:
                float(
                    candidate[
                        "minimum_acceleration_per_loaded_joule_m_s2_per_j"
                    ]
                ),
        )

    return {
        "effort":
            effort,

        "signed_lane":
            signed,

        "nonnegative_lane":
            nonnegative,

        "best_lane":
            best[
                "lane"
            ],

        "best_result":
            best,
    }


def solve_source_coefficients(
    portal_scale_ev: float,
    coefficients: np.ndarray,
    h: float,
    density_model: str = PRIMARY_DENSITY_MODEL,
    rho_max_m: float = PRODUCTION_RHO_MAX_M,
    z_min_m: float = PRODUCTION_Z_MIN_M,
    z_max_m: float = PRODUCTION_Z_MAX_M,
) -> dict[str, Any]:
    """Directly re-solve one physical source combination."""

    coefficients = (
        _normalize_coefficients(
            np.asarray(
                coefficients,
                dtype=float,
            )
        )
    )

    (
        rhos,
        zs,
        rho_grid,
        z_grid,
    ) = (
        _grid(
            h,
            rho_max_m,
            z_min_m,
            z_max_m,
        )
    )

    density = (
        payload_density_profile_kg_m3(
            rho_grid,
            z_grid,
            density_model,
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
        source_basis_profiles(
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
            "nonfinite direct source-shape solve"
        )

    field = np.zeros_like(
        rho_grid
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
        float(
            portal_scale_ev
        ) ** 4
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

    acceleration_interpolator = RegularGridInterpolator(
        (
            zs,
            rhos,
        ),
        acceleration_unit,
        bounds_error=True,
    )

    sampled_unit = np.asarray(
        acceleration_interpolator(
            payload_points
        )
    )

    minimum_unit = float(
        np.min(
            sampled_unit
        )
    )

    base = {
        "portal_scale_ev":
            float(
                portal_scale_ev
            ),

        "portal_scale_kev":
            float(
                portal_scale_ev
            )
            /
            1000.0,

        "grid_spacing_m":
            float(
                h
            ),

        "density_model":
            density_model,

        "rho_max_m":
            rho_max_m,

        "z_min_m":
            z_min_m,

        "z_max_m":
            z_max_m,

        "source_coefficients":
            coefficients.tolist(),

        "source_basis_labels":
            list(
                source_basis_labels()
            ),

        "unit_source_payload_acceleration_min_m_s2":
            minimum_unit,

        "unit_source_payload_acceleration_max_m_s2":
            float(
                np.max(
                    sampled_unit
                )
            ),

        "whole_payload_outward_sign":
            minimum_unit
            >
            0.0,

        "normalizable_to_1g":
            minimum_unit
            >
            0.0,

        "complete_energy_established":
            False,
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

    acceleration = (
        source_scale**2
        *
        acceleration_unit
    )

    sampled_acceleration = (
        source_scale**2
        *
        sampled_unit
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

    canonical_field_energy_j = (
        energy_prefactor
        *
        canonical_integral
    )

    loaded_capacity_j = (
        energy_prefactor
        *
        loaded_integral
    )

    payload_interaction_j = (
        loaded_capacity_j
        -
        canonical_field_energy_j
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

    source_work_relative_error = (
        abs(
            source_work_j
            -
            loaded_capacity_j
        )
        /
        loaded_capacity_j
    )

    signed_source_ev_m = (
        2.0
        *
        math.pi
        *
        float(
            np.sum(
                rho_grid
                *
                source_scaled
            )
        )
        *
        h**2
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

    negative_source_ev_m = (
        2.0
        *
        math.pi
        *
        float(
            np.sum(
                rho_grid
                *
                np.maximum(
                    -source_scaled,
                    0.0,
                )
            )
        )
        *
        h**2
    )

    negative_l1_fraction = (
        negative_source_ev_m
        /
        absolute_source_ev_m
    )

    a12c = (
        a12c_artifact()
    )

    a12c_source_ev_m = float(
        a12c[
            "massless_f2_finite_payload_bvp"
        ][
            "production"
        ][
            "integrated_canonical_source_ev_m"
        ]
    )

    cylindrical_volume = (
        2.0
        *
        math.pi
        *
        rho_grid
        *
        h**2
    )

    exact_payload_shift_j = float(
        np.sum(
            density
            *
            C_LIGHT_M_S**2
            *
            np.expm1(
                sigma
            )
            *
            cylindrical_volume
        )
    )

    payload_mask = (
        density
        >
        0.0
    )

    sigma_max = float(
        np.max(
            sigma[
                payload_mask
            ]
        )
    )

    return {
        **base,

        "source_scale":
            source_scale,

        "payload_local_acceleration_min_m_s2":
            float(
                np.min(
                    sampled_acceleration
                )
            ),

        "payload_local_acceleration_max_m_s2":
            float(
                np.max(
                    sampled_acceleration
                )
            ),

        "strict_whole_payload_1g_pass":
            bool(
                np.min(
                    sampled_acceleration
                )
                >=
                TARGET_ACCELERATION_M_S2
                *
                (
                    1.0
                    -
                    1.0e-10
                )
            ),

        "canonical_field_energy_j":
            canonical_field_energy_j,

        "payload_interaction_energy_j":
            payload_interaction_j,

        "loaded_quadratic_capacity_j":
            loaded_capacity_j,

        "source_work_j":
            source_work_j,

        "source_work_relative_error":
            source_work_relative_error,

        "integrated_signed_source_ev_m":
            signed_source_ev_m,

        "integrated_absolute_source_ev_m":
            absolute_source_ev_m,

        "absolute_source_ratio_vs_a12c":
            (
                absolute_source_ev_m
                /
                a12c_source_ev_m
            ),

        "negative_source_l1_fraction":
            negative_l1_fraction,

        "source_has_counter_circulating_regions":
            negative_l1_fraction
            >
            1.0e-8,

        "peak_absolute_source_amplitude":
            float(
                np.max(
                    np.abs(
                        source_scaled
                    )
                )
            ),

        "payload_sigma_max":
            sigma_max,

        "exact_payload_conformal_shift_j":
            exact_payload_shift_j,

        "small_sigma_self_consistent":
            abs(
                math.expm1(
                    4.0
                    *
                    sigma_max
                )
            )
            <
            1.0e-10,

        "loaded_capacity_below_10j":
            loaded_capacity_j
            <
            FEW_JOULE_TARGET_J,

        "loaded_capacity_below_100j":
            loaded_capacity_j
            <
            SUB100J_TARGET_J,

        "loaded_capacity_below_1kj":
            loaded_capacity_j
            <
            SUB1KJ_TARGET_J,

        "loaded_capacity_below_10kj":
            loaded_capacity_j
            <
            SUB10KJ_TARGET_J,

        "loaded_capacity_below_100kj":
            loaded_capacity_j
            <
            SUB100KJ_TARGET_J,

        "loaded_capacity_below_1mj":
            loaded_capacity_j
            <
            SUB1MJ_TARGET_J,

        "loaded_capacity_strictly_below_10mj":
            loaded_capacity_j
            <
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "complete_energy_established":
            False,
    }
