"""032H17A12D1R3C1 — exact variational reciprocity and ultra-small loading validation.

PURPOSE
-------
Validate the strongest unresolved numerical claims in R3C before any new
polarization-node boundary-value problem is authorized.

SCIENTIFIC QUESTIONS
--------------------
1. Does the complete discrete coupled operator admit one weighted quadratic
   action, including the scalar axis stencil and both uncoupled elliptic
   blocks, rather than only the off-diagonal C/D reciprocity relation?
2. Where is the first directly sampled loss of whole-payload outward sign in
   the unresolved ultra-small-loading interval below 1e-4?
3. Does the low-rank Woodbury reconstruction agree with a direct sparse solve
   of the full coupled deviation system?
4. Is the early sign loss associated with a near-singular interface mode, or
   with a large but nonsingular morphology susceptibility?
5. Does the sign-loss conclusion survive the original two grids and a modestly
   finer validation grid?

VARIATIONAL AXIS WEIGHT
-----------------------
The R3C scalar axis stencil for -Delta is

    K[0,0] =  4/h^2
    K[0,1] = -4/h^2

while the adjacent radial row contains

    K[1,0] = -1/(2 h^2).

Weighted self-adjointness requires

    w_0 K[0,1] = w_1 K[1,0]

and therefore

    w_0 / w_1 = 1/8.

Thus the action-consistent scalar radial axis weight is h/8.

R3C used h/4 inside its off-diagonal reciprocity diagnostic. The topological
C block has no active scalar row on the axis, so using h/8 for the complete
variational certificate should leave the actual D coupling unchanged. R3C1
checks this explicitly rather than silently altering the historical R3C run.

SAME-ACTION CERTIFICATE
-----------------------
For radial quadrature weights W_phi and W_A, R3C1 checks

    W_phi K_phi = K_phi^T W_phi
    W_A   K_A   = K_A^T   W_A
    W_A D       = C^T W_phi

and therefore symmetry of the complete weighted Hessian block operator.

Residuals are normalized by the relevant operator magnitude.

ULTRA-SMALL LOADING
-------------------
The scan resolves

    0, 1e-9, 3e-9, ..., 1e-4

and bisects every directly observed sign-change bracket.

The result is a directly bracketed numerical threshold, not interpolation from
zero to 1e-4.

INDEPENDENT RECONSTRUCTION
--------------------------
Selected loadings are independently solved with the full sparse coupled
deviation matrix and compared against R3C's Woodbury reduction.

INTERFACE MODES
---------------
The reduced system is

    (I + lambda M)y = -lambda q.

R3C1 computes its spectrum and the singular structure near the observed first
sign loss. It also tracks field orientation relative to grad(beta).

CLAIM LIMITS
------------
This run does not establish a physical antigravity model, microscopic source,
parity/CP completion, interacting hyperbolicity, nonlinear stability,
quantum naturalness, empirical viability, complete <10 MJ energy, or a
replacement for 006D.

CLAIM CLASSIFICATION
--------------------
PROJECT_SAME_ACTION_VARIATIONAL_AND_NUMERICAL_VALIDATION_GATE
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from scipy.sparse import bmat, csr_matrix, diags
from scipy.sparse.linalg import spsolve

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    HBAR_C_EV_M,
    REFERENCE_PORTAL_SCALE_EV,
)
from .hook17_f2_strong_payload_loading_rescue import (
    PRIMARY_DENSITY_MODEL,
    loading_coefficient_z,
    payload_density_profile_kg_m3,
)
from .hook17_fdual_f_global_mirror_prefight import (
    PRIMARY_FIT_RADIUS_M,
    PRIMARY_LMAX,
    TAPER_THICKNESS_M,
    fit_exterior_multipoles,
)
from .hook17_fdual_f_loaded_payload_homotopy import (
    _a12c_potential_field,
    _construct_global_mirror_phi,
    _fields_from_potentials,
    _prepare_low_rank_loaded_system,
    _solve_loaded_deviation,
    _state_diagnostics,
    _vectors_to_full_potentials,
    provenance_gate as r3c_provenance_gate,
    source_amplitude_factor_for_one_g,
)


BRANCH = "032H17A12D1R3C1"

GRID_SPACINGS_M = (
    0.075,
    0.050,
    0.040,
)

DIRECT_VALIDATION_GRIDS_M = (
    0.075,
    0.050,
)

SPECTRUM_GRIDS_M = (
    0.075,
    0.050,
)

ULTRASMALL_LOADING = (
    0.0,
    1.0e-9,
    3.0e-9,
    1.0e-8,
    3.0e-8,
    1.0e-7,
    3.0e-7,
    1.0e-6,
    3.0e-6,
    1.0e-5,
    3.0e-5,
    1.0e-4,
)

VARIATIONAL_RELATIVE_TOL = 1.0e-12
DIRECT_VECTOR_RELATIVE_TOL = 1.0e-7
DIRECT_ACCEL_ABS_TOL_M_S2 = 1.0e-5
BISECTION_ITERATIONS = 36
BISECTION_ABS_FLOOR = 1.0e-13
EIGEN_REALITY_RELATIVE_TOL = 1.0e-8


def provenance_gate() -> dict[str, Any]:
    prior = r3c_provenance_gate()

    return {
        "pass": bool(prior["pass"] is True),
        "r3c_provenance": prior,
        "physical_antigravity_model_found": False,
        "006d_replaced": False,
        "complete_energy_established": False,
    }


def action_axis_weight_ratio() -> dict[str, float]:
    k01 = -4.0
    k10 = -0.5
    required = k10 / k01

    return {
        "required_w0_over_w1": required,
        "r3c_diagnostic_w0_over_w1": 0.25,
        "variational_w0_over_w1": 0.125,
    }


def _max_abs_sparse(matrix: csr_matrix) -> float:
    if matrix.nnz == 0:
        return 0.0

    return float(
        np.max(
            np.abs(
                matrix.data
            )
        )
    )


def _relative_sparse_difference(
    lhs: csr_matrix,
    rhs: csr_matrix,
) -> dict[str, float]:
    difference = (
        lhs
        -
        rhs
    ).tocsr()

    numerator = (
        _max_abs_sparse(
            difference
        )
    )

    scale = max(
        _max_abs_sparse(
            lhs
        ),
        _max_abs_sparse(
            rhs
        ),
        np.finfo(
            float
        ).tiny,
    )

    return {
        "max_abs":
            numerator,

        "scale_max_abs":
            scale,

        "relative_max_abs":
            numerator
            /
            scale,
    }


def _action_weights(
    field: dict[str, Any],
    prep: dict[str, Any],
) -> tuple[
    np.ndarray,
    np.ndarray,
]:
    h = float(
        field[
            "h"
        ]
    )

    rhos = np.asarray(
        field[
            "rhos"
        ],
        dtype=float,
    )

    nz_inner = int(
        prep[
            "operators"
        ][
            "nz_inner"
        ]
    )

    phi_rho = (
        rhos[
            :-1
        ].copy()
    )

    phi_rho[
        0
    ] = (
        h
        /
        8.0
    )

    a_rho = (
        rhos[
            1:-1
        ].copy()
    )

    return (
        np.tile(
            phi_rho,
            nz_inner,
        ),
        np.tile(
            a_rho,
            nz_inner,
        ),
    )


def _r3c_diagnostic_weights(
    field: dict[str, Any],
    prep: dict[str, Any],
) -> tuple[
    np.ndarray,
    np.ndarray,
]:
    h = float(
        field[
            "h"
        ]
    )

    rhos = np.asarray(
        field[
            "rhos"
        ],
        dtype=float,
    )

    nz_inner = int(
        prep[
            "operators"
        ][
            "nz_inner"
        ]
    )

    phi_rho = (
        rhos[
            :-1
        ].copy()
    )

    phi_rho[
        0
    ] = (
        0.25
        *
        h
    )

    a_rho = (
        rhos[
            1:-1
        ].copy()
    )

    return (
        np.tile(
            phi_rho,
            nz_inner,
        ),
        np.tile(
            a_rho,
            nz_inner,
        ),
    )


def full_variational_certificate(
    field: dict[str, Any],
    prep: dict[str, Any],
) -> dict[str, Any]:
    k_phi = (
        prep[
            "operators"
        ][
            "k_phi"
        ].tocsr()
    )

    k_a = (
        prep[
            "operators"
        ][
            "k_a"
        ].tocsr()
    )

    c = (
        prep[
            "coupling"
        ][
            "c"
        ].tocsr()
    )

    d_existing = (
        prep[
            "coupling"
        ][
            "d"
        ].tocsr()
    )

    w_phi, w_a = (
        _action_weights(
            field,
            prep,
        )
    )

    old_w_phi, old_w_a = (
        _r3c_diagnostic_weights(
            field,
            prep,
        )
    )

    w_phi_matrix = diags(
        w_phi,
        format="csr",
    )

    w_a_matrix = diags(
        w_a,
        format="csr",
    )

    old_w_phi_matrix = diags(
        old_w_phi,
        format="csr",
    )

    old_w_a_matrix = diags(
        old_w_a,
        format="csr",
    )

    phi_action = (
        _relative_sparse_difference(
            w_phi_matrix
            @
            k_phi,
            k_phi.T
            @
            w_phi_matrix,
        )
    )

    phi_old = (
        _relative_sparse_difference(
            old_w_phi_matrix
            @
            k_phi,
            k_phi.T
            @
            old_w_phi_matrix,
        )
    )

    a_action = (
        _relative_sparse_difference(
            w_a_matrix
            @
            k_a,
            k_a.T
            @
            w_a_matrix,
        )
    )

    d_from_action = (
        diags(
            1.0
            /
            w_a,
            format="csr",
        )
        @
        c.T
        @
        w_phi_matrix
    ).tocsr()

    d_unchanged = (
        _relative_sparse_difference(
            d_from_action,
            d_existing,
        )
    )

    cross_action = (
        _relative_sparse_difference(
            w_a_matrix
            @
            d_existing,
            c.T
            @
            w_phi_matrix,
        )
    )

    cross_old = (
        _relative_sparse_difference(
            old_w_a_matrix
            @
            d_existing,
            c.T
            @
            old_w_phi_matrix,
        )
    )

    nr_phi = int(
        prep[
            "operators"
        ][
            "nr_phi"
        ]
    )

    nz_inner = int(
        prep[
            "operators"
        ][
            "nz_inner"
        ]
    )

    axis_rows = (
        np.arange(
            nz_inner,
            dtype=int,
        )
        *
        nr_phi
    )

    axis_c_nnz = int(
        c[
            axis_rows,
            :
        ].nnz
    )

    complete_relative = max(
        phi_action[
            "relative_max_abs"
        ],
        a_action[
            "relative_max_abs"
        ],
        cross_action[
            "relative_max_abs"
        ],
    )

    passed = bool(
        axis_c_nnz
        ==
        0

        and

        d_unchanged[
            "relative_max_abs"
        ]
        <=
        VARIATIONAL_RELATIVE_TOL

        and

        complete_relative
        <=
        VARIATIONAL_RELATIVE_TOL
    )

    return {
        "axis_weight_required_h_over":
            8.0,

        "r3c_diagnostic_axis_weight_h_over":
            4.0,

        "axis_coupling_rows_nnz":
            axis_c_nnz,

        "r3c_old_kphi_weighted_symmetry":
            phi_old,

        "action_kphi_weighted_symmetry":
            phi_action,

        "action_ka_weighted_symmetry":
            a_action,

        "r3c_old_cross_reciprocity":
            cross_old,

        "action_cross_reciprocity":
            cross_action,

        "action_derived_d_vs_existing_d":
            d_unchanged,

        "complete_hessian_relative_max_abs":
            complete_relative,

        "relative_tolerance":
            VARIATIONAL_RELATIVE_TOL,

        "complete_variational_same_action_pass":
            passed,
    }


def _build_baseline_and_prep(
    h: float,
) -> dict[str, Any]:
    field = (
        _a12c_potential_field(
            float(
                h
            )
        )
    )

    fit = (
        fit_exterior_multipoles(
            field,
            PRIMARY_FIT_RADIUS_M,
            PRIMARY_LMAX,
        )
    )

    phi0 = (
        _construct_global_mirror_phi(
            field,
            fit,
        )
    )

    a0 = (
        field[
            "a_phi"
        ]
        /
        math.sqrt(
            2.0
        )
    )

    density = (
        payload_density_profile_kg_m3(
            field[
                "rho_grid"
            ],
            field[
                "z_grid"
            ],
            PRIMARY_DENSITY_MODEL,
        )
    )

    baseline = (
        _state_diagnostics(
            phi0,
            a0,
            field,
            density,
        )
    )

    scale = (
        source_amplitude_factor_for_one_g(
            baseline[
                "minimum_payload_acceleration_m_s2"
            ]
        )
    )

    if scale is None:
        raise RuntimeError(
            "R3C1 baseline lost outward sign"
        )

    phi0 = (
        scale
        *
        phi0
    )

    a0 = (
        scale
        *
        a0
    )

    baseline = (
        _state_diagnostics(
            phi0,
            a0,
            field,
            density,
        )
    )

    z_loading = (
        loading_coefficient_z(
            density,
            REFERENCE_PORTAL_SCALE_EV,
        )
    )

    beta_full = (
        -(
            z_loading
            -
            1.0
        )
    )

    prep = (
        _prepare_low_rank_loaded_system(
            field,
            phi0,
            a0,
            beta_full,
        )
    )

    return {
        "field":
            field,

        "fit":
            fit,

        "phi0":
            phi0,

        "a0":
            a0,

        "density":
            density,

        "beta_full":
            beta_full,

        "baseline":
            baseline,

        "prep":
            prep,
    }


def _full_perturbation_potentials(
    prep: dict[str, Any],
    field: dict[str, Any],
    phi_vec: np.ndarray,
    a_vec: np.ndarray,
) -> tuple[
    np.ndarray,
    np.ndarray,
]:
    phi = np.zeros_like(
        field[
            "rho_grid"
        ],
        dtype=float,
    )

    a_phi = np.zeros_like(
        phi
    )

    phi[
        1:-1,
        :-1,
    ] = (
        phi_vec.reshape(
            prep[
                "operators"
            ][
                "nz_inner"
            ],
            prep[
                "nr_phi"
            ],
        )
    )

    a_phi[
        1:-1,
        1:-1,
    ] = (
        a_vec.reshape(
            prep[
                "operators"
            ][
                "nz_inner"
            ],
            prep[
                "nr_a"
            ],
        )
    )

    return (
        phi,
        a_phi,
    )


def _acceleration_map_from_potentials(
    phi: np.ndarray,
    a_phi: np.ndarray,
    field: dict[str, Any],
) -> np.ndarray:
    fields = (
        _fields_from_potentials(
            phi,
            a_phi,
            field[
                "rho_grid"
            ],
            field[
                "h"
            ],
        )
    )

    dot_eb = (
        fields[
            "e_rho"
        ]
        *
        fields[
            "b_rho"
        ]
        +
        fields[
            "e_z"
        ]
        *
        fields[
            "b_z"
        ]
    )

    sigma = (
        -2.0
        *
        HBAR_C_EV_M**2
        *
        dot_eb
        /
        REFERENCE_PORTAL_SCALE_EV**4
    )

    d_sigma_dz, _ = (
        np.gradient(
            sigma,
            field[
                "h"
            ],
            field[
                "h"
            ],
            edge_order=2,
        )
    )

    return (
        -C_LIGHT_M_S**2
        *
        d_sigma_dz
    )


def linear_loading_susceptibility(
    setup: dict[str, Any],
) -> dict[str, Any]:
    prep = (
        setup[
            "prep"
        ]
    )

    field = (
        setup[
            "field"
        ]
    )

    phi0 = (
        setup[
            "phi0"
        ]
    )

    a0 = (
        setup[
            "a0"
        ]
    )

    phi_prime_vec = (
        -(
            prep[
                "green_phi"
            ]
            @
            prep[
                "c_a0"
            ]
        )
    )

    a_prime_vec = (
        -(
            prep[
                "green_a"
            ]
            @
            prep[
                "d_phi0"
            ]
        )
    )

    phi_prime, a_prime = (
        _full_perturbation_potentials(
            prep,
            field,
            phi_prime_vec,
            a_prime_vec,
        )
    )

    base_fields = (
        _fields_from_potentials(
            phi0,
            a0,
            field[
                "rho_grid"
            ],
            field[
                "h"
            ],
        )
    )

    prime_fields = (
        _fields_from_potentials(
            phi_prime,
            a_prime,
            field[
                "rho_grid"
            ],
            field[
                "h"
            ],
        )
    )

    dot_prime = (
        prime_fields[
            "e_rho"
        ]
        *
        base_fields[
            "b_rho"
        ]
        +
        base_fields[
            "e_rho"
        ]
        *
        prime_fields[
            "b_rho"
        ]
        +
        prime_fields[
            "e_z"
        ]
        *
        base_fields[
            "b_z"
        ]
        +
        base_fields[
            "e_z"
        ]
        *
        prime_fields[
            "b_z"
        ]
    )

    sigma_prime = (
        -2.0
        *
        HBAR_C_EV_M**2
        *
        dot_prime
        /
        REFERENCE_PORTAL_SCALE_EV**4
    )

    d_sigma_prime_dz, _ = (
        np.gradient(
            sigma_prime,
            field[
                "h"
            ],
            field[
                "h"
            ],
            edge_order=2,
        )
    )

    acceleration_prime = (
        -C_LIGHT_M_S**2
        *
        d_sigma_prime_dz
    )

    acceleration0 = (
        _acceleration_map_from_potentials(
            phi0,
            a0,
            field,
        )
    )

    payload = (
        field[
            "payload"
        ]
    )

    a0_payload = (
        acceleration0[
            payload
        ]
    )

    ap_payload = (
        acceleration_prime[
            payload
        ]
    )

    payload_indices = (
        np.argwhere(
            payload
        )
    )

    candidate = (
        np.where(
            ap_payload
            <
            0.0
        )[
            0
        ]
    )

    if len(
        candidate
    ):
        crossing_values = (
            -a0_payload[
                candidate
            ]
            /
            ap_payload[
                candidate
            ]
        )

        positive = (
            np.where(
                crossing_values
                >
                0.0
            )[
                0
            ]
        )

    else:
        crossing_values = (
            np.asarray(
                [],
                dtype=float,
            )
        )

        positive = (
            np.asarray(
                [],
                dtype=int,
            )
        )

    if len(
        positive
    ):
        local = int(
            positive[
                np.argmin(
                    crossing_values[
                        positive
                    ]
                )
            ]
        )

        payload_flat_index = int(
            candidate[
                local
            ]
        )

        predicted = float(
            crossing_values[
                local
            ]
        )

        j, i = (
            payload_indices[
                payload_flat_index
            ]
        )

        rho = float(
            field[
                "rho_grid"
            ][
                j,
                i
            ]
        )

        z = float(
            field[
                "z_grid"
            ][
                j,
                i
            ]
        )

        slope = float(
            ap_payload[
                payload_flat_index
            ]
        )

        base = float(
            a0_payload[
                payload_flat_index
            ]
        )

    else:
        predicted = None
        rho = None
        z = None
        slope = None
        base = None

    return {
        "field_derivative_phi_l2":
            float(
                np.linalg.norm(
                    phi_prime_vec
                )
            ),

        "field_derivative_a_l2":
            float(
                np.linalg.norm(
                    a_prime_vec
                )
            ),

        "payload_acceleration_derivative_min_m_s2_per_lambda":
            float(
                np.min(
                    ap_payload
                )
            ),

        "payload_acceleration_derivative_max_m_s2_per_lambda":
            float(
                np.max(
                    ap_payload
                )
            ),

        "first_order_first_sign_loss_lambda":
            predicted,

        "first_order_crossing_rho_m":
            rho,

        "first_order_crossing_z_m":
            z,

        "first_order_crossing_baseline_acceleration_m_s2":
            base,

        "first_order_crossing_slope_m_s2_per_lambda":
            slope,
    }


def interface_morphology(
    phi: np.ndarray,
    a_phi: np.ndarray,
    setup: dict[str, Any],
) -> dict[str, float]:
    field = (
        setup[
            "field"
        ]
    )

    beta = (
        setup[
            "beta_full"
        ]
    )

    h = float(
        field[
            "h"
        ]
    )

    fields = (
        _fields_from_potentials(
            phi,
            a_phi,
            field[
                "rho_grid"
            ],
            h,
        )
    )

    beta_z, beta_r = (
        np.gradient(
            beta,
            h,
            h,
            edge_order=2,
        )
    )

    grad = (
        np.sqrt(
            beta_r**2
            +
            beta_z**2
        )
    )

    threshold = (
        1.0e-10
        *
        float(
            np.max(
                grad
            )
        )
    )

    mask = (
        grad
        >
        threshold
    )

    inv = np.zeros_like(
        grad
    )

    np.divide(
        1.0,
        grad,
        out=inv,
        where=mask,
    )

    n_r = (
        beta_r
        *
        inv
    )

    n_z = (
        beta_z
        *
        inv
    )

    e_n = (
        fields[
            "e_rho"
        ]
        *
        n_r
        +
        fields[
            "e_z"
        ]
        *
        n_z
    )

    e_t = (
        -fields[
            "e_rho"
        ]
        *
        n_z
        +
        fields[
            "e_z"
        ]
        *
        n_r
    )

    b_n = (
        fields[
            "b_rho"
        ]
        *
        n_r
        +
        fields[
            "b_z"
        ]
        *
        n_z
    )

    b_t = (
        -fields[
            "b_rho"
        ]
        *
        n_z
        +
        fields[
            "b_z"
        ]
        *
        n_r
    )

    dot_eb = (
        fields[
            "e_rho"
        ]
        *
        fields[
            "b_rho"
        ]
        +
        fields[
            "e_z"
        ]
        *
        fields[
            "b_z"
        ]
    )

    dot_z, dot_r = (
        np.gradient(
            dot_eb,
            h,
            h,
            edge_order=2,
        )
    )

    grad_dot = (
        np.sqrt(
            dot_r**2
            +
            dot_z**2
        )
    )

    volume = (
        2.0
        *
        math.pi
        *
        field[
            "rho_grid"
        ]
        *
        h**2
    )

    weight = (
        grad
        *
        volume
        *
        mask
    )

    total_weight = (
        float(
            np.sum(
                weight
            )
        )
        +
        np.finfo(
            float
        ).tiny
    )

    def weighted_rms(
        value: np.ndarray,
    ) -> float:
        return math.sqrt(
            float(
                np.sum(
                    weight
                    *
                    value**2
                )
            )
            /
            total_weight
        )

    e2 = (
        fields[
            "e_rho"
        ] ** 2
        +
        fields[
            "e_z"
        ] ** 2
    )

    b2 = (
        fields[
            "b_rho"
        ] ** 2
        +
        fields[
            "b_z"
        ] ** 2
    )

    e_total = (
        float(
            np.sum(
                weight
                *
                e2
            )
        )
        +
        np.finfo(
            float
        ).tiny
    )

    b_total = (
        float(
            np.sum(
                weight
                *
                b2
            )
        )
        +
        np.finfo(
            float
        ).tiny
    )

    return {
        "interface_weighted_E_normal_rms":
            weighted_rms(
                e_n
            ),

        "interface_weighted_E_tangent_rms":
            weighted_rms(
                e_t
            ),

        "interface_weighted_B_normal_rms":
            weighted_rms(
                b_n
            ),

        "interface_weighted_B_tangent_rms":
            weighted_rms(
                b_t
            ),

        "interface_weighted_Etangent2_fraction":
            float(
                np.sum(
                    weight
                    *
                    e_t**2
                )
            )
            /
            e_total,

        "interface_weighted_Bnormal2_fraction":
            float(
                np.sum(
                    weight
                    *
                    b_n**2
                )
            )
            /
            b_total,

        "interface_gradbeta_dot_B_rms":
            weighted_rms(
                grad
                *
                b_n
            ),

        "interface_gradbeta_cross_E_rms":
            weighted_rms(
                grad
                *
                e_t
            ),

        "interface_E_dot_B_rms":
            weighted_rms(
                dot_eb
            ),

        "interface_grad_E_dot_B_rms":
            weighted_rms(
                grad_dot
            ),
    }


def _state_for_loading(
    setup: dict[str, Any],
    loading_fraction: float,
) -> tuple[
    dict[str, Any],
    dict[str, Any] | None,
]:
    prep = (
        setup[
            "prep"
        ]
    )

    solution = (
        _solve_loaded_deviation(
            prep,
            float(
                loading_fraction
            ),
            coupling_sign=1.0,
        )
    )

    if not solution[
        "success"
    ]:
        return (
            solution,
            None,
        )

    phi, a_phi = (
        _vectors_to_full_potentials(
            prep,
            setup[
                "field"
            ],
            setup[
                "phi0"
            ],
            setup[
                "a0"
            ],
            solution,
        )
    )

    state = (
        _state_diagnostics(
            phi,
            a_phi,
            setup[
                "field"
            ],
            setup[
                "density"
            ],
        )
    )

    state = {
        **state,
        **interface_morphology(
            phi,
            a_phi,
            setup,
        ),
    }

    return (
        solution,
        state,
    )


def ultrasmall_scan(
    setup: dict[str, Any],
) -> list[
    dict[str, Any]
]:
    rows = []

    previous_rho = None
    previous_z = None

    for lam in ULTRASMALL_LOADING:
        solution, state = (
            _state_for_loading(
                setup,
                lam,
            )
        )

        if state is None:
            rows.append(
                {
                    "loading_fraction":
                        lam,

                    "solve_success":
                        False,

                    "reduced_condition_number":
                        solution[
                            "condition_number"
                        ],

                    "relative_solve_residual":
                        solution[
                            "relative_residual"
                        ],

                    "minimum_payload_acceleration_m_s2":
                        None,

                    "maximum_payload_acceleration_m_s2":
                        None,

                    "whole_payload_outward":
                        False,

                    "worst_payload_rho_m":
                        None,

                    "worst_payload_z_m":
                        None,

                    "worst_point_migration_m":
                        None,

                    "canonical_field_energy_j":
                        None,
                }
            )

            continue

        rho = float(
            state[
                "worst_payload_rho_m"
            ]
        )

        z = float(
            state[
                "worst_payload_z_m"
            ]
        )

        if previous_rho is None:
            migration = 0.0

        else:
            migration = math.hypot(
                rho
                -
                previous_rho,
                z
                -
                previous_z,
            )

        rows.append(
            {
                "loading_fraction":
                    lam,

                "solve_success":
                    True,

                "reduced_condition_number":
                    float(
                        solution[
                            "condition_number"
                        ]
                    ),

                "relative_solve_residual":
                    float(
                        solution[
                            "relative_residual"
                        ]
                    ),

                "minimum_payload_acceleration_m_s2":
                    float(
                        state[
                            "minimum_payload_acceleration_m_s2"
                        ]
                    ),

                "maximum_payload_acceleration_m_s2":
                    float(
                        state[
                            "maximum_payload_acceleration_m_s2"
                        ]
                    ),

                "whole_payload_outward":
                    bool(
                        state[
                            "whole_payload_outward"
                        ]
                    ),

                "worst_payload_rho_m":
                    rho,

                "worst_payload_z_m":
                    z,

                "worst_point_migration_m":
                    migration,

                "canonical_field_energy_j":
                    float(
                        state[
                            "canonical_field_energy_j"
                        ]
                    ),

                "interface_weighted_Etangent2_fraction":
                    float(
                        state[
                            "interface_weighted_Etangent2_fraction"
                        ]
                    ),

                "interface_weighted_Bnormal2_fraction":
                    float(
                        state[
                            "interface_weighted_Bnormal2_fraction"
                        ]
                    ),

                "interface_gradbeta_dot_B_rms":
                    float(
                        state[
                            "interface_gradbeta_dot_B_rms"
                        ]
                    ),

                "interface_gradbeta_cross_E_rms":
                    float(
                        state[
                            "interface_gradbeta_cross_E_rms"
                        ]
                    ),

                "interface_E_dot_B_rms":
                    float(
                        state[
                            "interface_E_dot_B_rms"
                        ]
                    ),

                "interface_grad_E_dot_B_rms":
                    float(
                        state[
                            "interface_grad_E_dot_B_rms"
                        ]
                    ),
            }
        )

        previous_rho = rho
        previous_z = z

    return rows


def sign_change_brackets(
    rows: list[
        dict[str, Any]
    ],
) -> list[
    dict[str, Any]
]:
    usable = [
        row
        for row in rows
        if (
            row[
                "solve_success"
            ]
            and
            row[
                "minimum_payload_acceleration_m_s2"
            ]
            is not None
        )
    ]

    brackets = []

    for left, right in zip(
        usable[
            :-1
        ],
        usable[
            1:
        ],
    ):
        a_left = float(
            left[
                "minimum_payload_acceleration_m_s2"
            ]
        )

        a_right = float(
            right[
                "minimum_payload_acceleration_m_s2"
            ]
        )

        if (
            a_left
            ==
            0.0
            or
            a_right
            ==
            0.0
            or
            a_left
            *
            a_right
            <
            0.0
        ):
            brackets.append(
                {
                    "lambda_left":
                        float(
                            left[
                                "loading_fraction"
                            ]
                        ),

                    "lambda_right":
                        float(
                            right[
                                "loading_fraction"
                            ]
                        ),

                    "acceleration_left_m_s2":
                        a_left,

                    "acceleration_right_m_s2":
                        a_right,

                    "direction":
                        (
                            "OUTWARD_TO_INWARD"
                            if (
                                a_left
                                >
                                0.0
                                and
                                a_right
                                <
                                0.0
                            )
                            else
                            "INWARD_TO_OUTWARD"
                        ),
                }
            )

    return brackets


def refine_bracket(
    setup: dict[str, Any],
    bracket: dict[str, Any],
) -> dict[str, Any]:
    left = float(
        bracket[
            "lambda_left"
        ]
    )

    right = float(
        bracket[
            "lambda_right"
        ]
    )

    a_left = float(
        bracket[
            "acceleration_left_m_s2"
        ]
    )

    a_right = float(
        bracket[
            "acceleration_right_m_s2"
        ]
    )

    for _ in range(
        BISECTION_ITERATIONS
    ):
        mid = (
            0.5
            *
            (
                left
                +
                right
            )
        )

        _, state = (
            _state_for_loading(
                setup,
                mid,
            )
        )

        if state is None:
            right = mid
            continue

        a_mid = float(
            state[
                "minimum_payload_acceleration_m_s2"
            ]
        )

        if a_left == 0.0:
            right = left
            a_right = a_left
            break

        if (
            a_left
            *
            a_mid
            <=
            0.0
        ):
            right = mid
            a_right = a_mid

        else:
            left = mid
            a_left = a_mid

        if (
            right
            -
            left
            <=
            BISECTION_ABS_FLOOR
        ):
            break

    midpoint = (
        0.5
        *
        (
            left
            +
            right
        )
    )

    _, state_mid = (
        _state_for_loading(
            setup,
            midpoint,
        )
    )

    return {
        "lambda_left":
            left,

        "lambda_right":
            right,

        "lambda_midpoint":
            midpoint,

        "width":
            right
            -
            left,

        "acceleration_left_m_s2":
            a_left,

        "acceleration_right_m_s2":
            a_right,

        "midpoint_minimum_acceleration_m_s2":
            (
                None
                if state_mid is None
                else
                float(
                    state_mid[
                        "minimum_payload_acceleration_m_s2"
                    ]
                )
            ),

        "midpoint_worst_rho_m":
            (
                None
                if state_mid is None
                else
                float(
                    state_mid[
                        "worst_payload_rho_m"
                    ]
                )
            ),

        "midpoint_worst_z_m":
            (
                None
                if state_mid is None
                else
                float(
                    state_mid[
                        "worst_payload_z_m"
                    ]
                )
            ),
    }


def _direct_loaded_deviation(
    prep: dict[str, Any],
    loading_fraction: float,
) -> dict[str, Any]:
    lam = float(
        loading_fraction
    )

    k_phi = (
        prep[
            "operators"
        ][
            "k_phi"
        ]
    )

    k_a = (
        prep[
            "operators"
        ][
            "k_a"
        ]
    )

    c = (
        prep[
            "coupling"
        ][
            "c"
        ]
    )

    d = (
        prep[
            "coupling"
        ][
            "d"
        ]
    )

    coupled = bmat(
        [
            [
                k_phi,
                lam
                *
                c,
            ],
            [
                lam
                *
                d,
                k_a,
            ],
        ],
        format="csr",
    )

    rhs = (
        -lam
        *
        np.concatenate(
            [
                np.asarray(
                    c
                    @
                    prep[
                        "a0_vec"
                    ]
                ).reshape(
                    -1
                ),
                np.asarray(
                    d
                    @
                    prep[
                        "phi0_vec"
                    ]
                ).reshape(
                    -1
                ),
            ]
        )
    )

    try:
        delta = (
            spsolve(
                coupled,
                rhs,
            )
        )

    except Exception as exc:
        return {
            "success":
                False,

            "exception":
                repr(
                    exc
                ),

            "relative_residual":
                None,

            "delta_phi_vec":
                None,

            "delta_a_vec":
                None,
        }

    n_phi = (
        k_phi.shape[
            0
        ]
    )

    residual = (
        coupled
        @
        delta
        -
        rhs
    )

    relative = float(
        np.linalg.norm(
            residual
        )
        /
        (
            np.linalg.norm(
                rhs
            )
            +
            np.finfo(
                float
            ).tiny
        )
    )

    return {
        "success":
            bool(
                np.all(
                    np.isfinite(
                        delta
                    )
                )
            ),

        "exception":
            None,

        "relative_residual":
            relative,

        "delta_phi_vec":
            np.asarray(
                delta[
                    :n_phi
                ]
            ),

        "delta_a_vec":
            np.asarray(
                delta[
                    n_phi:
                ]
            ),
    }


def direct_vs_woodbury(
    setup: dict[str, Any],
    loading_fraction: float,
) -> dict[str, Any]:
    lam = float(
        loading_fraction
    )

    prep = (
        setup[
            "prep"
        ]
    )

    wood = (
        _solve_loaded_deviation(
            prep,
            lam,
            coupling_sign=1.0,
        )
    )

    direct = (
        _direct_loaded_deviation(
            prep,
            lam,
        )
    )

    if (
        not wood[
            "success"
        ]
        or
        not direct[
            "success"
        ]
    ):
        return {
            "loading_fraction":
                lam,

            "pass":
                False,

            "woodbury_success":
                bool(
                    wood[
                        "success"
                    ]
                ),

            "direct_success":
                bool(
                    direct[
                        "success"
                    ]
                ),

            "direct_exception":
                direct[
                    "exception"
                ],
        }

    direct_norm = math.sqrt(
        float(
            np.linalg.norm(
                direct[
                    "delta_phi_vec"
                ]
            ) ** 2
        )
        +
        float(
            np.linalg.norm(
                direct[
                    "delta_a_vec"
                ]
            ) ** 2
        )
    )

    difference_norm = math.sqrt(
        float(
            np.linalg.norm(
                direct[
                    "delta_phi_vec"
                ]
                -
                wood[
                    "delta_phi_vec"
                ]
            ) ** 2
        )
        +
        float(
            np.linalg.norm(
                direct[
                    "delta_a_vec"
                ]
                -
                wood[
                    "delta_a_vec"
                ]
            ) ** 2
        )
    )

    vector_relative = (
        difference_norm
        /
        (
            direct_norm
            +
            np.finfo(
                float
            ).tiny
        )
    )

    direct_solution = {
        "delta_phi_vec":
            direct[
                "delta_phi_vec"
            ],

        "delta_a_vec":
            direct[
                "delta_a_vec"
            ],
    }

    phi_direct, a_direct = (
        _vectors_to_full_potentials(
            prep,
            setup[
                "field"
            ],
            setup[
                "phi0"
            ],
            setup[
                "a0"
            ],
            direct_solution,
        )
    )

    direct_state = (
        _state_diagnostics(
            phi_direct,
            a_direct,
            setup[
                "field"
            ],
            setup[
                "density"
            ],
        )
    )

    phi_wood, a_wood = (
        _vectors_to_full_potentials(
            prep,
            setup[
                "field"
            ],
            setup[
                "phi0"
            ],
            setup[
                "a0"
            ],
            wood,
        )
    )

    wood_state = (
        _state_diagnostics(
            phi_wood,
            a_wood,
            setup[
                "field"
            ],
            setup[
                "density"
            ],
        )
    )

    accel_abs = abs(
        float(
            direct_state[
                "minimum_payload_acceleration_m_s2"
            ]
        )
        -
        float(
            wood_state[
                "minimum_payload_acceleration_m_s2"
            ]
        )
    )

    energy_rel = (
        abs(
            float(
                direct_state[
                    "canonical_field_energy_j"
                ]
            )
            -
            float(
                wood_state[
                    "canonical_field_energy_j"
                ]
            )
        )
        /
        max(
            abs(
                float(
                    direct_state[
                        "canonical_field_energy_j"
                    ]
                )
            ),
            np.finfo(
                float
            ).tiny,
        )
    )

    passed = bool(
        vector_relative
        <=
        DIRECT_VECTOR_RELATIVE_TOL

        and

        accel_abs
        <=
        DIRECT_ACCEL_ABS_TOL_M_S2

        and

        energy_rel
        <=
        DIRECT_VECTOR_RELATIVE_TOL
    )

    return {
        "loading_fraction":
            lam,

        "pass":
            passed,

        "woodbury_success":
            True,

        "direct_success":
            True,

        "woodbury_relative_residual":
            float(
                wood[
                    "relative_residual"
                ]
            ),

        "direct_relative_residual":
            float(
                direct[
                    "relative_residual"
                ]
            ),

        "field_vector_relative_difference":
            float(
                vector_relative
            ),

        "minimum_acceleration_absolute_difference_m_s2":
            float(
                accel_abs
            ),

        "canonical_energy_relative_difference":
            float(
                energy_rel
            ),

        "woodbury_minimum_acceleration_m_s2":
            float(
                wood_state[
                    "minimum_payload_acceleration_m_s2"
                ]
            ),

        "direct_minimum_acceleration_m_s2":
            float(
                direct_state[
                    "minimum_payload_acceleration_m_s2"
                ]
            ),

        "woodbury_worst_rho_m":
            float(
                wood_state[
                    "worst_payload_rho_m"
                ]
            ),

        "woodbury_worst_z_m":
            float(
                wood_state[
                    "worst_payload_z_m"
                ]
            ),

        "direct_worst_rho_m":
            float(
                direct_state[
                    "worst_payload_rho_m"
                ]
            ),

        "direct_worst_z_m":
            float(
                direct_state[
                    "worst_payload_z_m"
                ]
            ),
    }


def reduced_interface_spectrum(
    setup: dict[str, Any],
    reference_lambda: float | None,
) -> dict[str, Any]:
    prep = (
        setup[
            "prep"
        ]
    )

    r_phi = len(
        prep[
            "coupling"
        ][
            "active_phi"
        ]
    )

    r_a = len(
        prep[
            "coupling"
        ][
            "active_a"
        ]
    )

    matrix = np.zeros(
        (
            r_phi
            +
            r_a,
            r_phi
            +
            r_a,
        ),
        dtype=float,
    )

    matrix[
        :r_phi,
        r_phi:
    ] = (
        prep[
            "c_green_a"
        ]
    )

    matrix[
        r_phi:,
        :r_phi
    ] = (
        prep[
            "d_green_phi"
        ]
    )

    eigenvalues = (
        np.linalg.eigvals(
            matrix
        )
    )

    spectral_radius = (
        float(
            np.max(
                np.abs(
                    eigenvalues
                )
            )
        )
        if len(
            eigenvalues
        )
        else
        0.0
    )

    reality_scale = (
        np.maximum(
            1.0,
            np.abs(
                eigenvalues.real
            ),
        )
    )

    nearly_real = (
        np.abs(
            eigenvalues.imag
        )
        <=
        EIGEN_REALITY_RELATIVE_TOL
        *
        reality_scale
    )

    negative = (
        eigenvalues[
            nearly_real
            &
            (
                eigenvalues.real
                <
                0.0
            )
        ].real
    )

    resonances = (
        np.sort(
            -1.0
            /
            negative
        )
        if len(
            negative
        )
        else
        np.asarray(
            []
        )
    )

    positive_resonances = (
        resonances[
            resonances
            >
            0.0
        ]
    )

    nearest = [
        float(
            value
        )
        for value in positive_resonances[
            :10
        ]
    ]

    q = (
        np.concatenate(
            [
                prep[
                    "c_a0"
                ],
                prep[
                    "d_phi0"
                ],
            ]
        )
    )

    singular_diag = None

    if (
        reference_lambda
        is not None
        and
        math.isfinite(
            reference_lambda
        )
    ):
        reduced = (
            np.eye(
                matrix.shape[
                    0
                ]
            )
            +
            float(
                reference_lambda
            )
            *
            matrix
        )

        u, singular_values, _ = (
            np.linalg.svd(
                reduced,
                full_matrices=False,
            )
        )

        s_min = float(
            singular_values[
                -1
            ]
        )

        s_max = float(
            singular_values[
                0
            ]
        )

        rhs = (
            -float(
                reference_lambda
            )
            *
            q
        )

        rhs_norm = float(
            np.linalg.norm(
                rhs
            )
        )

        if rhs_norm > 0.0:
            overlap = float(
                abs(
                    np.dot(
                        u[
                            :,
                            -1
                        ].conj(),
                        rhs,
                    )
                )
                /
                rhs_norm
            )

        else:
            overlap = 0.0

        singular_diag = {
            "reference_lambda":
                float(
                    reference_lambda
                ),

            "smallest_singular_value":
                s_min,

            "largest_singular_value":
                s_max,

            "condition_number_from_svd":
                s_max
                /
                max(
                    s_min,
                    np.finfo(
                        float
                    ).tiny,
                ),

            "forcing_overlap_with_most_amplified_left_singular_mode":
                overlap,
        }

    return {
        "reduced_dimension":
            int(
                matrix.shape[
                    0
                ]
            ),

        "spectral_radius":
            spectral_radius,

        "maximum_absolute_imaginary_eigenvalue":
            float(
                np.max(
                    np.abs(
                        eigenvalues.imag
                    )
                )
                if len(
                    eigenvalues
                )
                else
                0.0
            ),

        "nearly_real_eigenvalue_fraction":
            float(
                np.mean(
                    nearly_real
                )
                if len(
                    eigenvalues
                )
                else
                1.0
            ),

        "smallest_positive_resonance_lambda":
            (
                None
                if len(
                    positive_resonances
                )
                ==
                0
                else
                float(
                    positive_resonances[
                        0
                    ]
                )
            ),

        "first_ten_positive_resonance_lambdas":
            nearest,

        "reference_singular_diagnostic":
            singular_diag,
    }


def run_grid_validation(
    h: float,
) -> dict[str, Any]:
    setup = (
        _build_baseline_and_prep(
            h
        )
    )

    certificate = (
        full_variational_certificate(
            setup[
                "field"
            ],
            setup[
                "prep"
            ],
        )
    )

    susceptibility = (
        linear_loading_susceptibility(
            setup
        )
    )

    scan = (
        ultrasmall_scan(
            setup
        )
    )

    brackets = (
        sign_change_brackets(
            scan
        )
    )

    refined = [
        refine_bracket(
            setup,
            bracket,
        )
        for bracket in brackets
    ]

    direct_rows = []

    if (
        float(
            h
        )
        in
        DIRECT_VALIDATION_GRIDS_M
    ):
        selected = set()

        if refined:
            selected.update(
                {
                    refined[
                        0
                    ][
                        "lambda_left"
                    ],
                    refined[
                        0
                    ][
                        "lambda_right"
                    ],
                }
            )

        if math.isclose(
            float(
                h
            ),
            0.050,
            rel_tol=0.0,
            abs_tol=1.0e-15,
        ):
            selected.add(
                1.0e-4
            )

        for lam in sorted(
            selected
        ):
            direct_rows.append(
                direct_vs_woodbury(
                    setup,
                    lam,
                )
            )

    reference_lambda = (
        refined[
            0
        ][
            "lambda_midpoint"
        ]
        if refined
        else
        None
    )

    spectrum = None

    if (
        float(
            h
        )
        in
        SPECTRUM_GRIDS_M
    ):
        spectrum = (
            reduced_interface_spectrum(
                setup,
                reference_lambda,
            )
        )

    first_loss = next(
        (
            row
            for row in scan
            if (
                row[
                    "solve_success"
                ]
                and
                row[
                    "minimum_payload_acceleration_m_s2"
                ]
                is not None
                and
                float(
                    row[
                        "minimum_payload_acceleration_m_s2"
                    ]
                )
                <
                0.0
            )
        ),
        None,
    )

    return {
        "grid_spacing_m":
            float(
                h
            ),

        "interface_taper_thickness_m":
            float(
                TAPER_THICKNESS_M
            ),

        "cells_across_interface_taper":
            float(
                TAPER_THICKNESS_M
                /
                h
            ),

        "baseline":
            setup[
                "baseline"
            ],

        "variational_certificate":
            certificate,

        "linear_susceptibility":
            susceptibility,

        "ultrasmall_scan":
            scan,

        "sign_change_brackets":
            brackets,

        "refined_sign_change_brackets":
            refined,

        "first_directly_sampled_inward_loading_fraction":
            (
                None
                if first_loss
                is None
                else
                float(
                    first_loss[
                        "loading_fraction"
                    ]
                )
            ),

        "direct_vs_woodbury":
            direct_rows,

        "interface_spectrum":
            spectrum,
    }


def final_decision(
    grid_results: dict[str, Any],
) -> dict[str, Any]:
    original = [
        grid_results[
            str(
                h
            )
        ]
        for h in DIRECT_VALIDATION_GRIDS_M
    ]

    all_results = [
        grid_results[
            str(
                h
            )
        ]
        for h in GRID_SPACINGS_M
    ]

    variational_pass = all(
        item[
            "variational_certificate"
        ][
            "complete_variational_same_action_pass"
        ]
        for item in all_results
    )

    direct_pass = bool(
        all(
            row[
                "pass"
            ]
            for item in original
            for row in item[
                "direct_vs_woodbury"
            ]
        )
        and
        all(
            item[
                "direct_vs_woodbury"
            ]
            for item in original
        )
    )

    directly_bracketed_original = all(
        any(
            bracket[
                "direction"
            ]
            ==
            "OUTWARD_TO_INWARD"
            for bracket in item[
                "sign_change_brackets"
            ]
        )
        for item in original
    )

    inward_by_1e4_all = all(
        any(
            math.isclose(
                float(
                    row[
                        "loading_fraction"
                    ]
                ),
                1.0e-4,
                rel_tol=0.0,
                abs_tol=1.0e-15,
            )
            and
            row[
                "solve_success"
            ]
            and
            float(
                row[
                    "minimum_payload_acceleration_m_s2"
                ]
            )
            <
            0.0
            for row in item[
                "ultrasmall_scan"
            ]
        )
        for item in all_results
    )

    refined_thresholds = {
        str(
            item[
                "grid_spacing_m"
            ]
        ):
            (
                None
                if not item[
                    "refined_sign_change_brackets"
                ]
                else
                float(
                    item[
                        "refined_sign_change_brackets"
                    ][
                        0
                    ][
                        "lambda_midpoint"
                    ]
                )
            )
        for item in all_results
    }

    if (
        variational_pass
        and
        direct_pass
        and
        directly_bracketed_original
        and
        inward_by_1e4_all
    ):
        decision = (
            "GREEN_SCOPED_R3C1_SIMPLE_PARALLEL_MIRROR_FRAGILITY_VALIDATED__"
            "FULL_VARIATIONAL_CERTIFICATE_PASS__"
            "ULTRASMALL_SIGN_LOSS_DIRECTLY_BRACKETED__"
            "WOODBURY_MATCHES_DIRECT_SOLVE__"
            "AUTHORIZE_R3D0_NODE_INTEGRABILITY_PREFLIGHT"
        )

        next_branch = (
            "032H17A12D1R3D0_"
            "POLARIZATION_NODE_MAXWELL_INTEGRABILITY_PREFLIGHT"
        )

        authorize_r3d0 = True

    elif not variational_pass:
        decision = (
            "RED_HOLD_R3C1_FULL_DISCRETE_ACTION_CERTIFICATE_FAILED__"
            "DO_NOT_DESIGN_R3D_UNTIL_OPERATOR_PROVENANCE_IS_REPAIRED"
        )

        next_branch = (
            "REPAIR_R3C1_VARIATIONAL_DISCRETIZATION"
        )

        authorize_r3d0 = False

    elif not direct_pass:
        decision = (
            "RED_HOLD_R3C1_WOODBURY_DIRECT_DISAGREEMENT__"
            "DO_NOT_PROMOTE_R3C_FRAGILITY"
        )

        next_branch = (
            "REPAIR_R3C1_SOLVER_RECONSTRUCTION"
        )

        authorize_r3d0 = False

    else:
        decision = (
            "YELLOW_R3C1_FRAGILITY_NOT_YET_CERTIFIED_ON_REQUIRED_GRIDS__"
            "REFINE_INTERFACE_OR_LOADING_RESOLUTION_BEFORE_R3D"
        )

        next_branch = (
            "032H17A12D1R3C2_"
            "INTERFACE_RESOLUTION_OR_SHARP_INTERFACE_RECONSTRUCTION"
        )

        authorize_r3d0 = False

    return {
        "decision":
            decision,

        "next":
            next_branch,

        "authorize_r3d0_node_integrability_prefight":
            authorize_r3d0,

        "full_variational_certificate_pass_all_grids":
            variational_pass,

        "direct_vs_woodbury_pass_original_grids":
            direct_pass,

        "outward_to_inward_bracket_directly_sampled_original_grids":
            directly_bracketed_original,

        "inward_by_1e4_all_three_grids":
            inward_by_1e4_all,

        "refined_first_loss_lambdas":
            refined_thresholds,

        "threshold_is_continuum_certified":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "006d_replaced":
            False,

        "complete_energy_established":
            False,
    }
