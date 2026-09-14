"""032H17A10F1 — Wheeler-current normalization repair + finite payload BVP.

PURPOSE
-------
Combine two high-value HOOK17 tasks in one theorem-first run:

1. Repair the absolute source normalization.

   Earlier A10 calculations used Wheeler's trace-altered nonmetricity response
   tensor as the convention-matched source shape.  That is sufficient for
   representation and nonzero-overlap questions, but not for absolute source
   number or source-energy calculations.

   Wheeler gives

       Qbar = (4/kappa) dL_source/dQ

   and, in an orthonormal frame,

       Sigma_ab = -Q_ab/2 + Omega_ab.

   His Dirac interaction has overall normalization alpha and Eq. (28) scales
   as alpha/kappa.

   After canonicalizing the fermion,

       Psi = sqrt(alpha) psi,

   the symmetric-connection current corresponding to the repository's
   alpha/kappa=1 Eq. (28) response therefore has magnitude

       |J_Sigma| = |Qbar_unit| / 2.

   The overall sign depends on source/action convention and does not affect
   the pole residue.

   Thus A10D's response-normalized residue 16 must not be used as an absolute
   current normalization.  The corrected connection-current residue is 4 and
   its canonical pole-coupling magnitude is 2.

2. Solve a finite source / finite payload reduced healthy-pole BVP.

   The physical protected transverse 1- pole is represented by the canonical
   azimuthal vector component V_phi in cylindrical coordinates.

   For an axisymmetric transverse source the exact reduced static equation is

       [-d_rho^2
        -(1/rho)d_rho
        -d_z^2
        +1/rho^2
        +m_eff^2] V_phi
       =
       J_phi.

   Using

       u = sqrt(rho) V_phi

   gives the symmetric numerical operator

       [-d_rho^2
        -d_z^2
        +3/(4 rho^2)
        +m_eff^2] u
       =
       sqrt(rho) J_phi.

   The finite source is a smooth compact spherical support carrying the
   divergence-free axisymmetric current

       J_phi
       =
       J0 * (rho/Rs) * (1-r^2/Rs^2)^2

   for r<Rs, and zero outside.

   Because the only component is azimuthal and there is no phi dependence,

       div J = 0

   identically.

FINITE PAYLOAD WITNESS
----------------------
Primary payload:

    mass = 1 kg
    uniform neutral torus
    major radius = 1.0 m
    minor radius = 0.2 m

It lies above the source.  Its center z is fixed analytically so that its
nearest point is exactly 1.0 m outside the finite source sphere.

The payload loading is chosen so that

    m_inside * a_payload = 0.4

with

    m_inside = 2 / m
    m_vacuum = 1 / m.

The required lambda is derived from the actual torus rest-energy density.

For the universal quadratic metric

    sigma = lambda V_phi^2

the local acceleration is

    a_z = -c^2 d_z sigma.

The finite payload acceleration is its uniform-mass center-of-mass average.

GEOMETRY FALSIFICATION CONTROL
------------------------------
A second BVP places the same 1 kg / 0.1 m spherical payload on the symmetry
axis above the source.

A regular azimuthal vector satisfies V_phi=0 on that axis.  This comparator is
expected to be extremely inefficient.

It is retained deliberately:

- a failure closes that source/payload geometry;
- it does NOT close the protected carrier;
- the successful toroidal payload must not be silently generalized to all
  payload geometries.

ENERGY
------
The canonical reduced-mode field/loading energy is

    E
    =
    1/2 integral [
        |grad V_phi|^2
        +V_phi^2/rho^2
        +m_eff^2 V_phi^2
    ] d^3x.

An independent source-work reconstruction

    E = 1/2 integral J_phi V_phi d^3x

is used as a numerical consistency check.

For a canonical pair coupling g_pair, the physical pair density is obtained
from the meter-coordinate field equation by

    n_pair[m^-3]
    =
    J_phi[eV/m^2] / (g_pair * hbar*c[eV m]).

Electron/positron and proton/antiproton rest-energy numbers are reported only
as mass comparators.  They do not include confinement, annihilation,
activation, reaction, support, or control energy.

CLAIM LIMIT
-----------
A green result can establish:

- corrected bare-current normalization;
- nonzero canonically normalized healthy-pole source coupling;
- finite compact divergence-free transverse current support;
- a finite neutral payload BVP;
- >=1 g center-of-mass outward acceleration;
- exactly 1 m reduced-EFT geometric external stand-off;
- converged canonical field/loading energy;
- microscopic source-number and rest-mass lower-bound diagnostics.

It does NOT establish:

- a self-consistent localized Dirac solution producing the prescribed current;
- stable source spin texture;
- source confinement/support;
- annihilation/reaction/radiation cost;
- quantitative ultralight RG/UV naturalness;
- full nonlinear Marzo + matter BVP;
- a complete conservative operating-energy ledger;
- a practical antigravity device.

A partial energy can reject but never promote.
"""

from __future__ import annotations

import math
from functools import lru_cache
from typing import Any

import numpy as np
from scipy.sparse import diags, eye, kron
from scipy.sparse.linalg import spsolve

from .dirac_hypermomentum_irrep import (
    wheeler_trace_altered_nonmetricity,
)
from .hook17_marzo2022_engineered_stueckelberg_noether import (
    engineered_pair_ps_tau,
)
from .hook17_marzo2022_exact_1minus_pole import (
    _benchmark_gate,
    _one_minus_basis_numpy,
)
from .hook17_marzo_physical_scale_payload_loading import (
    empirical_quadratic_metric_gate,
    physical_planck_normalized_family,
)


C_LIGHT_M_S = 299792458.0
HBAR_C_EV_M = 1.973269804e-7
EV_J = 1.602176634e-19

TARGET_ACCELERATION_M_S2 = 9.80665
STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7

SOURCE_RADIUS_M = 2.0

PRIMARY_PAYLOAD_MASS_KG = 1.0
PRIMARY_PAYLOAD_MAJOR_RADIUS_M = 1.0
PRIMARY_PAYLOAD_MINOR_RADIUS_M = 0.2
PRIMARY_STANDOFF_M = 1.0
PRIMARY_TARGET_M_IN_A = 0.4

SPHERE_PAYLOAD_MASS_KG = 1.0
SPHERE_PAYLOAD_RADIUS_M = 0.1
SPHERE_STANDOFF_M = 1.0
SPHERE_TARGET_M_IN_R = 0.2

VACUUM_INVERSE_RANGE_PER_M = 1.0

PRODUCTION_GRID_M = 0.025
COARSE_GRID_M = 0.050

PRODUCTION_RHO_MAX_M = 7.0
PRODUCTION_Z_MIN_M = -5.0
PRODUCTION_Z_MAX_M = 8.0

LARGER_RHO_MAX_M = 8.0
LARGER_Z_MIN_M = -6.0
LARGER_Z_MAX_M = 9.0

ELECTRON_MASS_EV = 510998.95
PROTON_MASS_EV = 938.27208816e6

TOL = 1.0e-11


def primary_payload_center_z_m() -> float:
    """Return z center giving exactly one metre source-surface separation."""

    required_centerline_radius = (
        SOURCE_RADIUS_M
        +
        PRIMARY_STANDOFF_M
        +
        PRIMARY_PAYLOAD_MINOR_RADIUS_M
    )

    return math.sqrt(
        required_centerline_radius**2
        -
        PRIMARY_PAYLOAD_MAJOR_RADIUS_M**2
    )


def primary_geometric_standoff_m() -> float:
    """Return exact minimum sphere-to-torus surface gap."""

    z_center = primary_payload_center_z_m()

    payload_centerline_distance = math.sqrt(
        PRIMARY_PAYLOAD_MAJOR_RADIUS_M**2
        +
        z_center**2
    )

    nearest_payload_radius = (
        payload_centerline_distance
        -
        PRIMARY_PAYLOAD_MINOR_RADIUS_M
    )

    return (
        nearest_payload_radius
        -
        SOURCE_RADIUS_M
    )


def _torus_volume_m3(
    major_radius_m: float,
    minor_radius_m: float,
) -> float:
    """Return torus volume."""

    return (
        2.0
        *
        math.pi**2
        *
        major_radius_m
        *
        minor_radius_m**2
    )


def _sphere_volume_m3(
    radius_m: float,
) -> float:
    """Return sphere volume."""

    return (
        4.0
        /
        3.0
        *
        math.pi
        *
        radius_m**3
    )


def _one_ev4_j_m3() -> float:
    """Return the SI energy density represented by one eV^4."""

    return (
        EV_J
        /
        HBAR_C_EV_M**3
    )


def _payload_energy_density_ev4(
    *,
    mass_kg: float,
    volume_m3: float,
) -> float:
    """Return uniform payload rest-energy density in eV^4."""

    density_j_m3 = (
        mass_kg
        *
        C_LIGHT_M_S**2
        /
        volume_m3
    )

    return (
        density_j_m3
        /
        _one_ev4_j_m3()
    )


def _lambda_for_payload_loading(
    *,
    mass_kg: float,
    volume_m3: float,
    characteristic_radius_m: float,
    target_m_inside_times_radius: float,
) -> float:
    """Return lambda giving the selected homogeneous matter loading."""

    rho_ev4 = _payload_energy_density_ev4(
        mass_kg=
            mass_kg,
        volume_m3=
            volume_m3,
    )

    m_out_ev = (
        HBAR_C_EV_M
        *
        VACUUM_INVERSE_RANGE_PER_M
    )

    m_inside_per_m = (
        target_m_inside_times_radius
        /
        characteristic_radius_m
    )

    m_inside_ev = (
        HBAR_C_EV_M
        *
        m_inside_per_m
    )

    if m_inside_ev <= m_out_ev:
        raise ValueError(
            "target matter loading must exceed the vacuum mass"
        )

    return (
        (
            m_inside_ev**2
            -
            m_out_ev**2
        )
        /
        (
            2.0
            *
            rho_ev4
        )
    )


def primary_lambda_ev_m2() -> float:
    """Return selected toroidal-payload metric coupling."""

    return _lambda_for_payload_loading(
        mass_kg=
            PRIMARY_PAYLOAD_MASS_KG,
        volume_m3=
            _torus_volume_m3(
                PRIMARY_PAYLOAD_MAJOR_RADIUS_M,
                PRIMARY_PAYLOAD_MINOR_RADIUS_M,
            ),
        characteristic_radius_m=
            PRIMARY_PAYLOAD_MINOR_RADIUS_M,
        target_m_inside_times_radius=
            PRIMARY_TARGET_M_IN_A,
    )


def sphere_lambda_ev_m2() -> float:
    """Return selected spherical-payload metric coupling."""

    return _lambda_for_payload_loading(
        mass_kg=
            SPHERE_PAYLOAD_MASS_KG,
        volume_m3=
            _sphere_volume_m3(
                SPHERE_PAYLOAD_RADIUS_M
            ),
        characteristic_radius_m=
            SPHERE_PAYLOAD_RADIUS_M,
        target_m_inside_times_radius=
            SPHERE_TARGET_M_IN_R,
    )


@lru_cache(maxsize=1)
def wheeler_bare_current_normalization_gate() -> dict[str, Any]:
    """Repair Eq.28 response -> canonical symmetric-connection current."""

    basis = np.eye(
        4,
        dtype=np.complex128,
    )

    scaling_errors = []

    for index in range(4):
        reference = wheeler_trace_altered_nonmetricity(
            basis[index],
            alpha_over_kappa=1.0,
        )

        for scale in (
            0.5,
            2.0,
            3.0,
        ):
            candidate = wheeler_trace_altered_nonmetricity(
                basis[index],
                alpha_over_kappa=scale,
            )

            scaling_errors.append(
                float(
                    np.max(
                        np.abs(
                            candidate
                            -
                            scale
                            *
                            reference
                        )
                    )
                )
            )

    maximum_scaling_error = max(
        scaling_errors
    )

    anchor = _benchmark_gate(
        "D2_ZERO_ANCHOR"
    )

    pole_vector = np.asarray(
        anchor[
            "pole_vector"
        ],
        dtype=float,
    )

    derivative_norm = float(
        anchor[
            "pole_derivative_norm"
        ]
    )

    one_minus_basis = _one_minus_basis_numpy(
        1
    )

    rows = []

    for pair_id in (
        "U1_V1",
        "U2_V2",
    ):
        response_tau = np.asarray(
            engineered_pair_ps_tau(
                pair_id
            ),
            dtype=float,
        )

        # Wheeler Eq.13 gives J_Q = kappa*Qbar/4.
        # Canonicalizing Psi=sqrt(alpha)psi removes alpha.
        # Q=-2 Sigma_(ab), so the symmetric connection current is
        # -2 J_Q.  Relative to the repository alpha/kappa=1 response
        # shape this is therefore -Qbar_unit/2.
        connection_current = (
            -0.5
            *
            response_tau
        )

        factor_error = float(
            np.max(
                np.abs(
                    response_tau
                    +
                    2.0
                    *
                    connection_current
                )
            )
        )

        coordinates = np.asarray(
            [
                float(
                    np.sum(
                        connection_current
                        *
                        tensor
                    )
                )
                for tensor in one_minus_basis
            ]
        )

        amplitude = float(
            np.dot(
                coordinates,
                pole_vector,
            )
        )

        saturated_residue = (
            amplitude**2
            /
            derivative_norm
        )

        canonical_coupling = math.sqrt(
            saturated_residue
        )

        response_row = next(
            row
            for row in anchor[
                "source_rows"
            ]
            if row[
                "pair_id"
            ]
            ==
            pair_id
        )

        rows.append(
            {
                "pair_id":
                    pair_id,

                "response_normalized_coordinates":
                    response_row[
                        "x_polarization_source_coordinates"
                    ],

                "canonical_connection_current_coordinates":
                    coordinates.tolist(),

                "response_to_connection_current_factor_magnitude":
                    0.5,

                "connection_current_sign_relative_to_response":
                    -1.0,

                "factor_reconstruction_error":
                    factor_error,

                "response_normalized_pole_residue":
                    float(
                        response_row[
                            "source_saturated_pole_residue"
                        ]
                    ),

                "canonical_connection_current_pole_amplitude":
                    amplitude,

                "canonical_connection_current_pole_amplitude_abs":
                    abs(
                        amplitude
                    ),

                "canonical_connection_current_saturated_residue":
                    saturated_residue,

                "canonical_connection_current_pole_coupling_magnitude":
                    canonical_coupling,

                "pole_overlap_nonzero":
                    bool(
                        abs(
                            amplitude
                        )
                        >
                        TOL
                    ),
            }
        )

    corrected = bool(
        maximum_scaling_error
        <=
        TOL
        and
        all(
            row[
                "factor_reconstruction_error"
            ]
            <=
            TOL
            and
            row[
                "pole_overlap_nonzero"
            ]
            and
            math.isclose(
                row[
                    "canonical_connection_current_saturated_residue"
                ],
                4.0,
                rel_tol=0.0,
                abs_tol=1.0e-10,
            )
            and
            math.isclose(
                row[
                    "canonical_connection_current_pole_coupling_magnitude"
                ],
                2.0,
                rel_tol=0.0,
                abs_tol=1.0e-10,
            )
            for row in rows
        )
    )

    return {
        "wheeler_eq28_object":
            "TRACE_ALTERED_NONMETRICITY_RESPONSE",

        "eq28_response_is_bare_connection_current":
            False,

        "eq28_alpha_over_kappa_scaling_verified":
            bool(
                maximum_scaling_error
                <=
                TOL
            ),

        "maximum_alpha_over_kappa_scaling_error":
            maximum_scaling_error,

        "canonical_fermion_redefinition":
            "Psi=sqrt(alpha)*psi",

        "alpha_cancels_from_canonical_bare_current":
            True,

        "canonical_nonmetricity_current_relative_to_unit_eq28_response":
            0.25,

        "canonical_symmetric_connection_current_relative_to_unit_eq28_response_magnitude":
            0.5,

        "q_to_symmetric_connection_relation":
            "Q_ab=-2*Sigma_(ab)",

        "rows":
            rows,

        "response_normalized_a10d_residue_16_is_absolute_source_residue":
            False,

        "corrected_connection_current_residue":
            4.0,

        "corrected_canonical_pair_pole_coupling_magnitude":
            2.0,

        "corrected_absolute_source_normalization_preflight":
            corrected,

        "a10d_nonzero_pole_overlap_survives_normalization_repair":
            bool(
                all(
                    row[
                        "pole_overlap_nonzero"
                    ]
                    for row in rows
                )
            ),
    }


def _primary_payload_mask(
    rho: np.ndarray,
    z: np.ndarray,
) -> np.ndarray:
    """Return primary torus mask."""

    z_center = primary_payload_center_z_m()

    return (
        (
            rho
            -
            PRIMARY_PAYLOAD_MAJOR_RADIUS_M
        ) ** 2
        +
        (
            z
            -
            z_center
        ) ** 2
        <=
        PRIMARY_PAYLOAD_MINOR_RADIUS_M**2
    )


def _sphere_payload_mask(
    rho: np.ndarray,
    z: np.ndarray,
) -> np.ndarray:
    """Return on-axis spherical comparator mask."""

    z_center = (
        SOURCE_RADIUS_M
        +
        SPHERE_STANDOFF_M
        +
        SPHERE_PAYLOAD_RADIUS_M
    )

    return (
        rho**2
        +
        (
            z
            -
            z_center
        ) ** 2
        <=
        SPHERE_PAYLOAD_RADIUS_M**2
    )


def _source_profile(
    rho: np.ndarray,
    z: np.ndarray,
) -> np.ndarray:
    """Return compact C1 axisymmetric azimuthal source profile."""

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


def _payload_spec(
    payload_kind: str,
) -> dict[str, float]:
    """Return finite-payload parameters."""

    if payload_kind == "TORUS":
        return {
            "lambda_ev_m2":
                primary_lambda_ev_m2(),

            "m_inside_per_m":
                (
                    PRIMARY_TARGET_M_IN_A
                    /
                    PRIMARY_PAYLOAD_MINOR_RADIUS_M
                ),

            "analytic_volume_m3":
                _torus_volume_m3(
                    PRIMARY_PAYLOAD_MAJOR_RADIUS_M,
                    PRIMARY_PAYLOAD_MINOR_RADIUS_M,
                ),

            "mass_kg":
                PRIMARY_PAYLOAD_MASS_KG,

            "stand_off_m":
                primary_geometric_standoff_m(),
        }

    if payload_kind == "SPHERE":
        return {
            "lambda_ev_m2":
                sphere_lambda_ev_m2(),

            "m_inside_per_m":
                (
                    SPHERE_TARGET_M_IN_R
                    /
                    SPHERE_PAYLOAD_RADIUS_M
                ),

            "analytic_volume_m3":
                _sphere_volume_m3(
                    SPHERE_PAYLOAD_RADIUS_M
                ),

            "mass_kg":
                SPHERE_PAYLOAD_MASS_KG,

            "stand_off_m":
                SPHERE_STANDOFF_M,
        }

    raise ValueError(
        "payload_kind must be TORUS or SPHERE"
    )


@lru_cache(maxsize=16)
def _solve_scaled_bvp(
    payload_kind: str,
    grid_spacing_m: float,
    rho_max_m: float,
    z_min_m: float,
    z_max_m: float,
) -> dict[str, Any]:
    """Solve and scale one finite axisymmetric transverse-vector BVP."""

    h = float(
        grid_spacing_m
    )

    if h <= 0.0:
        raise ValueError(
            "grid spacing must be positive"
        )

    spec = _payload_spec(
        payload_kind
    )

    rhos = np.arange(
        0.0,
        rho_max_m
        +
        0.5
        *
        h,
        h,
    )

    zs = np.arange(
        z_min_m,
        z_max_m
        +
        0.5
        *
        h,
        h,
    )

    rho_i = rhos[
        1:-1
    ]

    z_i = zs[
        1:-1
    ]

    nr = len(
        rho_i
    )

    nz = len(
        z_i
    )

    if (
        nr < 3
        or
        nz < 3
    ):
        raise ValueError(
            "grid is too small"
        )

    radial_diag = (
        2.0
        /
        h**2
        +
        3.0
        /
        (
            4.0
            *
            rho_i**2
        )
    )

    radial_off = (
        -np.ones(
            nr
            -
            1
        )
        /
        h**2
    )

    radial_operator = diags(
        [
            radial_off,
            radial_diag,
            radial_off,
        ],
        [
            -1,
            0,
            1,
        ],
        format="csr",
    )

    z_diag = (
        np.ones(
            nz
        )
        *
        2.0
        /
        h**2
    )

    z_off = (
        -np.ones(
            nz
            -
            1
        )
        /
        h**2
    )

    z_operator = diags(
        [
            z_off,
            z_diag,
            z_off,
        ],
        [
            -1,
            0,
            1,
        ],
        format="csr",
    )

    rho_grid_i, z_grid_i = np.meshgrid(
        rho_i,
        z_i,
    )

    if payload_kind == "TORUS":
        payload_i = _primary_payload_mask(
            rho_grid_i,
            z_grid_i,
        )
    else:
        payload_i = _sphere_payload_mask(
            rho_grid_i,
            z_grid_i,
        )

    mass_squared_i = np.where(
        payload_i,
        spec[
            "m_inside_per_m"
        ] ** 2,
        VACUUM_INVERSE_RANGE_PER_M**2,
    )

    operator = (
        kron(
            eye(
                nz,
                format="csr",
            ),
            radial_operator,
        )
        +
        kron(
            z_operator,
            eye(
                nr,
                format="csr",
            ),
        )
        +
        diags(
            mass_squared_i.ravel(),
            0,
            format="csr",
        )
    )

    source_i = _source_profile(
        rho_grid_i,
        z_grid_i,
    )

    rhs = (
        np.sqrt(
            rho_grid_i
        )
        *
        source_i
    ).ravel()

    u = spsolve(
        operator,
        rhs,
    ).reshape(
        nz,
        nr,
    )

    field = np.zeros(
        (
            len(
                zs
            ),
            len(
                rhos
            ),
        ),
        dtype=float,
    )

    field[
        1:-1,
        1:-1,
    ] = (
        u
        /
        np.sqrt(
            rho_grid_i
        )
    )

    source = np.zeros_like(
        field
    )

    source[
        1:-1,
        1:-1,
    ] = source_i

    rho_grid, z_grid = np.meshgrid(
        rhos,
        zs,
    )

    if payload_kind == "TORUS":
        payload = _primary_payload_mask(
            rho_grid,
            z_grid,
        )
    else:
        payload = _sphere_payload_mask(
            rho_grid,
            z_grid,
        )

    mass_squared = np.where(
        payload,
        spec[
            "m_inside_per_m"
        ] ** 2,
        VACUUM_INVERSE_RANGE_PER_M**2,
    )

    d_field_dz, d_field_drho = np.gradient(
        field,
        h,
        h,
        edge_order=2,
    )

    sigma = (
        spec[
            "lambda_ev_m2"
        ]
        *
        field**2
    )

    d_sigma_dz, _ = np.gradient(
        sigma,
        h,
        h,
        edge_order=2,
    )

    acceleration_z = (
        -C_LIGHT_M_S**2
        *
        d_sigma_dz
    )

    payload_weights = (
        rho_grid
        *
        payload
    )

    weight_sum = float(
        np.sum(
            payload_weights
        )
    )

    if weight_sum <= 0.0:
        raise RuntimeError(
            "payload was not resolved on the grid"
        )

    unit_com_acceleration = float(
        np.sum(
            payload_weights
            *
            acceleration_z
        )
        /
        weight_sum
    )

    if unit_com_acceleration <= 0.0:
        raise RuntimeError(
            "unit source did not produce outward +z payload acceleration"
        )

    source_amplitude = math.sqrt(
        TARGET_ACCELERATION_M_S2
        /
        unit_com_acceleration
    )

    field_scaled = (
        source_amplitude
        *
        field
    )

    source_scaled = (
        source_amplitude
        *
        source
    )

    acceleration_scaled = (
        source_amplitude**2
        *
        acceleration_z
    )

    com_acceleration = (
        source_amplitude**2
        *
        unit_com_acceleration
    )

    payload_accelerations = (
        acceleration_scaled[
            payload
        ]
    )

    field_squared_over_rho_squared = np.zeros_like(
        field
    )

    np.divide(
        field**2,
        rho_grid**2,
        out=
            field_squared_over_rho_squared,
        where=
            rho_grid
            >
            0.0,
    )

    energy_density_unit = (
        0.5
        *
        (
            d_field_drho**2
            +
            d_field_dz**2
            +
            field_squared_over_rho_squared
            +
            mass_squared
            *
            field**2
        )
    )

    energy_e_v2_m_unit = (
        2.0
        *
        math.pi
        *
        float(
            np.sum(
                rho_grid
                *
                energy_density_unit
            )
        )
        *
        h**2
    )

    field_loading_energy_j = (
        source_amplitude**2
        *
        energy_e_v2_m_unit
        /
        HBAR_C_EV_M
        *
        EV_J
    )

    source_work_e_v2_m_unit = (
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
                source
                *
                field
            )
        )
        *
        h**2
    )

    source_work_energy_j = (
        source_amplitude**2
        *
        source_work_e_v2_m_unit
        /
        HBAR_C_EV_M
        *
        EV_J
    )

    source_normalization = (
        wheeler_bare_current_normalization_gate()
    )

    pair_pole_coupling = float(
        source_normalization[
            "corrected_canonical_pair_pole_coupling_magnitude"
        ]
    )

    integrated_source_e_v_m = (
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

    source_pair_count = (
        integrated_source_e_v_m
        /
        (
            pair_pole_coupling
            *
            HBAR_C_EV_M
        )
    )

    peak_pair_density_m3 = (
        float(
            np.max(
                source_scaled
            )
        )
        /
        (
            pair_pole_coupling
            *
            HBAR_C_EV_M
        )
    )

    source_volume_m3 = (
        4.0
        /
        3.0
        *
        math.pi
        *
        SOURCE_RADIUS_M**3
    )

    average_pair_density_m3 = (
        source_pair_count
        /
        source_volume_m3
    )

    discrete_payload_volume_m3 = (
        2.0
        *
        math.pi
        *
        float(
            np.sum(
                rho_grid
                *
                payload
            )
        )
        *
        h**2
    )

    source_work_relative_error = (
        abs(
            field_loading_energy_j
            -
            source_work_energy_j
        )
        /
        max(
            abs(
                source_work_energy_j
            ),
            1.0
        )
    )

    return {
        "payload_kind":
            payload_kind,

        "grid_spacing_m":
            h,

        "rho_max_m":
            float(
                rho_max_m
            ),

        "z_min_m":
            float(
                z_min_m
            ),

        "z_max_m":
            float(
                z_max_m
            ),

        "grid_n_rho":
            len(
                rhos
            ),

        "grid_n_z":
            len(
                zs
            ),

        "source_radius_m":
            SOURCE_RADIUS_M,

        "source_profile":
            "J_phi=J0*(rho/Rs)*(1-r^2/Rs^2)^2",

        "source_support_compact":
            True,

        "source_profile_c1_at_boundary":
            True,

        "source_divergence_exactly_zero_by_axisymmetry":
            True,

        "field_divergence_exactly_zero_by_axisymmetry":
            True,

        "vacuum_inverse_range_per_m":
            VACUUM_INVERSE_RANGE_PER_M,

        "inside_inverse_range_per_m":
            spec[
                "m_inside_per_m"
            ],

        "lambda_ev_m2":
            spec[
                "lambda_ev_m2"
            ],

        "analytic_payload_volume_m3":
            spec[
                "analytic_volume_m3"
            ],

        "discrete_payload_volume_m3":
            discrete_payload_volume_m3,

        "payload_volume_relative_error":
            (
                abs(
                    discrete_payload_volume_m3
                    -
                    spec[
                        "analytic_volume_m3"
                    ]
                )
                /
                spec[
                    "analytic_volume_m3"
                ]
            ),

        "payload_mass_kg":
            spec[
                "mass_kg"
            ],

        "payload_neutral":
            True,

        "geometric_external_standoff_m":
            spec[
                "stand_off_m"
            ],

        "source_amplitude_e_v_per_m2":
            source_amplitude,

        "payload_com_outward_acceleration_m_s2":
            com_acceleration,

        "payload_local_outward_acceleration_min_m_s2":
            float(
                np.min(
                    payload_accelerations
                )
            ),

        "payload_local_outward_acceleration_max_m_s2":
            float(
                np.max(
                    payload_accelerations
                )
            ),

        "payload_com_at_least_1g":
            bool(
                com_acceleration
                >=
                TARGET_ACCELERATION_M_S2
                *
                (
                    1.0
                    -
                    1.0e-12
                )
            ),

        "field_loading_energy_j":
            field_loading_energy_j,

        "source_work_energy_j":
            source_work_energy_j,

        "source_work_relative_error":
            source_work_relative_error,

        "canonical_pair_pole_coupling":
            pair_pole_coupling,

        "source_pair_count":
            source_pair_count,

        "peak_pair_density_m3":
            peak_pair_density_m3,

        "average_pair_density_m3":
            average_pair_density_m3,

        "source_volume_m3":
            source_volume_m3,

        "finite_transverse_current_support":
            True,

        "finite_payload_bvp":
            True,

        "microscopic_dirac_source_solution":
            False,

        "full_nonlin_marzo_bvp":
            False,
    }


@lru_cache(maxsize=1)
def primary_torus_bvp_gate() -> dict[str, Any]:
    """Return production finite toroidal-payload witness."""

    return _solve_scaled_bvp(
        "TORUS",
        PRODUCTION_GRID_M,
        PRODUCTION_RHO_MAX_M,
        PRODUCTION_Z_MIN_M,
        PRODUCTION_Z_MAX_M,
    )


@lru_cache(maxsize=1)
def on_axis_sphere_comparator_gate() -> dict[str, Any]:
    """Return compact spherical-payload geometry comparator."""

    return _solve_scaled_bvp(
        "SPHERE",
        PRODUCTION_GRID_M,
        PRODUCTION_RHO_MAX_M,
        PRODUCTION_Z_MIN_M,
        PRODUCTION_Z_MAX_M,
    )


@lru_cache(maxsize=1)
def primary_bvp_convergence_gate() -> dict[str, Any]:
    """Return grid and domain convergence diagnostics."""

    coarse = _solve_scaled_bvp(
        "TORUS",
        COARSE_GRID_M,
        PRODUCTION_RHO_MAX_M,
        PRODUCTION_Z_MIN_M,
        PRODUCTION_Z_MAX_M,
    )

    fine = primary_torus_bvp_gate()

    larger = _solve_scaled_bvp(
        "TORUS",
        PRODUCTION_GRID_M,
        LARGER_RHO_MAX_M,
        LARGER_Z_MIN_M,
        LARGER_Z_MAX_M,
    )

    grid_energy_relative_change = (
        abs(
            coarse[
                "field_loading_energy_j"
            ]
            -
            fine[
                "field_loading_energy_j"
            ]
        )
        /
        fine[
            "field_loading_energy_j"
        ]
    )

    grid_source_count_relative_change = (
        abs(
            coarse[
                "source_pair_count"
            ]
            -
            fine[
                "source_pair_count"
            ]
        )
        /
        fine[
            "source_pair_count"
        ]
    )

    domain_energy_relative_change = (
        abs(
            larger[
                "field_loading_energy_j"
            ]
            -
            fine[
                "field_loading_energy_j"
            ]
        )
        /
        fine[
            "field_loading_energy_j"
        ]
    )

    passed = bool(
        grid_energy_relative_change
        <
        0.03
        and
        grid_source_count_relative_change
        <
        0.03
        and
        domain_energy_relative_change
        <
        0.002
        and
        fine[
            "source_work_relative_error"
        ]
        <
        0.001
        and
        fine[
            "payload_volume_relative_error"
        ]
        <
        0.05
    )

    return {
        "coarse_grid_m":
            COARSE_GRID_M,

        "fine_grid_m":
            PRODUCTION_GRID_M,

        "coarse_energy_j":
            coarse[
                "field_loading_energy_j"
            ],

        "fine_energy_j":
            fine[
                "field_loading_energy_j"
            ],

        "grid_energy_relative_change":
            grid_energy_relative_change,

        "grid_source_count_relative_change":
            grid_source_count_relative_change,

        "larger_domain_energy_j":
            larger[
                "field_loading_energy_j"
            ],

        "domain_energy_relative_change":
            domain_energy_relative_change,

        "fine_source_work_relative_error":
            fine[
                "source_work_relative_error"
            ],

        "fine_payload_volume_relative_error":
            fine[
                "payload_volume_relative_error"
            ],

        "convergence_pass":
            passed,
    }


@lru_cache(maxsize=1)
def source_rest_energy_gate() -> dict[str, Any]:
    """Return source-number and rest-energy lower-bound diagnostics."""

    bvp = primary_torus_bvp_gate()

    pair_count = float(
        bvp[
            "source_pair_count"
        ]
    )

    field_energy = float(
        bvp[
            "field_loading_energy_j"
        ]
    )

    electron_pair_energy_j = (
        pair_count
        *
        2.0
        *
        ELECTRON_MASS_EV
        *
        EV_J
    )

    proton_pair_energy_j = (
        pair_count
        *
        2.0
        *
        PROTON_MASS_EV
        *
        EV_J
    )

    field_plus_electron_j = (
        field_energy
        +
        electron_pair_energy_j
    )

    field_plus_proton_j = (
        field_energy
        +
        proton_pair_energy_j
    )

    maximum_particle_mass_ev = (
        (
            STRICT_COMPLETE_OPERATING_TARGET_J
            -
            field_energy
        )
        /
        (
            2.0
            *
            pair_count
            *
            EV_J
        )
    )

    return {
        "source_pair_count":
            pair_count,

        "electron_positron_rest_energy_floor_j":
            electron_pair_energy_j,

        "proton_antiproton_rest_energy_comparator_j":
            proton_pair_energy_j,

        "field_plus_electron_rest_floor_j":
            field_plus_electron_j,

        "field_plus_proton_rest_comparator_j":
            field_plus_proton_j,

        "maximum_particle_mass_ev_before_field_plus_rest_hits_10mj":
            maximum_particle_mass_ev,

        "maximum_particle_mass_gev_before_field_plus_rest_hits_10mj":
            maximum_particle_mass_ev
            /
            1.0e9,

        "electron_variant_partial_floor_below_10mj":
            bool(
                field_plus_electron_j
                <
                STRICT_COMPLETE_OPERATING_TARGET_J
            ),

        "proton_mass_comparator_partial_floor_below_10mj":
            bool(
                field_plus_proton_j
                <
                STRICT_COMPLETE_OPERATING_TARGET_J
            ),

        "source_confinement_energy_included":
            False,

        "annihilation_reaction_energy_included":
            False,

        "activation_control_energy_included":
            False,

        "support_energy_included":
            False,

        "complete_energy":
            False,
    }


@lru_cache(maxsize=1)
def h17a10f1_summary() -> dict[str, Any]:
    """Return the A10F1 kill-or-promote decision."""

    normalization = (
        wheeler_bare_current_normalization_gate()
    )

    physical_family = (
        physical_planck_normalized_family()
    )

    empirical = (
        empirical_quadratic_metric_gate()
    )

    primary = (
        primary_torus_bvp_gate()
    )

    sphere = (
        on_axis_sphere_comparator_gate()
    )

    convergence = (
        primary_bvp_convergence_gate()
    )

    source_energy = (
        source_rest_energy_gate()
    )

    lambda_margin = (
        empirical[
            "lambda_empirical_max_ev_m2"
        ]
        /
        primary[
            "lambda_ev_m2"
        ]
    )

    source_q_over_f = (
        (
            1.0
            /
            SOURCE_RADIUS_M
        )
        /
        VACUUM_INVERSE_RANGE_PER_M
    )

    finite_reduced_eft_witness = bool(
        normalization[
            "corrected_absolute_source_normalization_preflight"
        ]
        and
        normalization[
            "a10d_nonzero_pole_overlap_survives_normalization_repair"
        ]
        and
        physical_family[
            "published_health_branch_II_pass"
        ]
        and
        primary[
            "source_divergence_exactly_zero_by_axisymmetry"
        ]
        and
        primary[
            "field_divergence_exactly_zero_by_axisymmetry"
        ]
        and
        math.isclose(
            primary[
                "geometric_external_standoff_m"
            ],
            1.0,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        )
        and
        primary[
            "payload_com_at_least_1g"
        ]
        and
        convergence[
            "convergence_pass"
        ]
        and
        primary[
            "field_loading_energy_j"
        ]
        <
        STRICT_COMPLETE_OPERATING_TARGET_J
        and
        lambda_margin
        >
        1.0
        and
        source_q_over_f
        <=
        1.0
    )

    sphere_geometry_rejected = bool(
        sphere[
            "field_loading_energy_j"
        ]
        >
        STRICT_COMPLETE_OPERATING_TARGET_J
    )

    decision = (
        "GREEN_A10F1_BARE_CURRENT_NORMALIZATION_REPAIRED__"
        "FINITE_TORUS_PAYLOAD_1G_1M_REDUCED_EFT_CORRIDOR_OPEN__"
        "ON_AXIS_SPHERE_GEOMETRY_REJECTED"
        if (
            finite_reduced_eft_witness
            and
            sphere_geometry_rejected
        )
        else
        "RED_A10F1_FINITE_PAYLOAD_OR_SOURCE_NORMALIZATION_GATE_FAIL"
    )

    return {
        "branch":
            "032H17A10F1",

        "decision":
            decision,

        "current_full_regression_before_a10f1":
            971,

        "source_normalization":
            normalization,

        "physical_family":
            physical_family,

        "primary_torus_payload_bvp":
            primary,

        "primary_convergence":
            convergence,

        "on_axis_sphere_comparator":
            sphere,

        "source_rest_energy":
            source_energy,

        "corrected_canonical_pair_pole_coupling":
            normalization[
                "corrected_canonical_pair_pole_coupling_magnitude"
            ],

        "primary_lambda_empirical_margin":
            lambda_margin,

        "source_characteristic_q_over_abs_f":
            source_q_over_f,

        "finite_compact_transverse_current_support_established":
            primary[
                "finite_transverse_current_support"
            ],

        "finite_neutral_payload_reduced_eft_bvp_established":
            finite_reduced_eft_witness,

        "reduced_eft_geometric_external_standoff_m":
            primary[
                "geometric_external_standoff_m"
            ],

        "reduced_eft_payload_com_outward_acceleration_m_s2":
            primary[
                "payload_com_outward_acceleration_m_s2"
            ],

        "on_axis_spherical_payload_current_geometry_rejected_by_energy":
            sphere_geometry_rejected,

        "on_axis_spherical_payload_field_energy_j":
            sphere[
                "field_loading_energy_j"
            ],

        "payload_shape_independent_performance_established":
            False,

        "microscopic_dirac_source_solution_established":
            False,

        "source_spin_texture_stability_established":
            False,

        "source_confinement_support_established":
            False,

        "reaction_annihilation_radiation_established":
            False,

        "full_covariant_nonlinear_marzo_matter_bvp_established":
            False,

        "full_quantum_rg_uv_certified":
            False,

        "ultralight_mass_quantitative_naturalness_certified":
            False,

        "source_sector_empirical_consistency_certified":
            False,

        "universal_metric_inverse_cube_preflight_pass":
            bool(
                lambda_margin
                >
                1.0
            ),

        "project_true_standoff_certified":
            False,

        "complete_energy_established":
            False,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "partial_energy_may_promote_model":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "hook17_closed":
            False,

        "partial_green":
            bool(
                finite_reduced_eft_witness
            ),

        "next":
            (
                "032H17A10F2_MICROSCOPIC_SOURCE_STATE_REALIZATION_"
                "ULTRALIGHT_NATURALNESS_SUPPORT_REACTION_NONLINEAR_"
                "AND_COMPLETE_ENERGY_CLOSEOUT"
                if finite_reduced_eft_witness
                else
                "CLOSE_CURRENT_MARZO_HOOK17_CARRIER"
            ),
    }
